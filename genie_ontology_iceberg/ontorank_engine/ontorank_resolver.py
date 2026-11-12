"""
OntoRank Algorithmic Authority Engine & Steward Review Queue
Evaluates candidate definitions, calculates authority scores using page-rank style signals,
resolves semantic conflicts across business domains, and routes ambiguous prompts to stewards.
"""

import math
import datetime
from typing import Dict, Any, List, Optional

class OntoRankEngine:
    def __init__(self):
        # In-memory dictionary of registered definitions / snippets
        self.definitions: Dict[str, Dict[str, Any]] = {}
        # Review queue for low-confidence or conflicting definitions
        self.review_queue: List[Dict[str, Any]] = []

    def register_definition(
        self,
        def_id: str,
        metric_name: str,
        domain: str,
        author: str,
        author_seniority: float, # 0.0 to 1.0 (e.g. Lead Steward = 1.0)
        sql_template: str,
        is_certified: bool = False,
        monthly_executions: int = 100,
        days_since_update: int = 5
    ) -> Dict[str, Any]:
        """
        Registers a business definition or metric snippet into the ontology.
        """
        def_obj = {
            "def_id": def_id,
            "metric_name": metric_name.upper(),
            "domain": domain,
            "author": author,
            "author_seniority": author_seniority,
            "sql_template": sql_template,
            "is_certified": is_certified,
            "monthly_executions": monthly_executions,
            "days_since_update": days_since_update,
            "authority_score": 0.0
        }
        def_obj["authority_score"] = self.compute_authority_score(def_obj)
        self.definitions[def_id] = def_obj
        return def_obj

    def compute_authority_score(self, def_obj: Dict[str, Any]) -> float:
        """
        Formula:
        Score = w1 * Cert + w2 * Seniority + w3 * log10(1 + Execs) + w4 * Freshness
        Weights: w1 = 0.40, w2 = 0.25, w3 = 0.20, w4 = 0.15
        """
        w1, w2, w3, w4 = 0.40, 0.25, 0.20, 0.15

        cert_val = 1.0 if def_obj["is_certified"] else 0.0
        seniority_val = min(max(def_obj["author_seniority"], 0.0), 1.0)
        exec_val = min(math.log10(1 + def_obj["monthly_executions"]) / 4.0, 1.0) # max normalized around 10k execs
        
        # Freshness decays if older than 90 days
        days = def_obj["days_since_update"]
        freshness_val = max(1.0 - (days / 180.0), 0.1)

        raw_score = (w1 * cert_val) + (w2 * seniority_val) + (w3 * exec_val) + (w4 * freshness_val)
        return round(raw_score, 4)

    def resolve_metric_query(self, user_prompt: str, metric_name: str) -> Dict[str, Any]:
        """
        Retrieves matching definitions for a metric, arbitrates between competing definitions,
        and either returns the authoritative certified SQL or routes to the Review Queue.
        """
        target_metric = metric_name.upper()
        candidates = [d for d in self.definitions.values() if d["metric_name"] == target_metric]

        if not candidates:
            # Route to review queue as an unmapped business query
            item = {
                "queue_id": f"Q-{len(self.review_queue)+1:03d}",
                "user_prompt": user_prompt,
                "metric_name": target_metric,
                "reason": "NO_DEFINITION_FOUND",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "PENDING_STEWARD"
            }
            self.review_queue.append(item)
            return {
                "status": "QUEUED_FOR_STEWARD",
                "message": f"Metric '{target_metric}' is not yet certified in the Genie Ontology.",
                "queue_item": item
            }

        # Sort by authority score descending
        ranked = sorted(candidates, key=lambda x: x["authority_score"], reverse=True)
        top = ranked[0]

        # Check for conflict: if runner-up is very close and also uncertified
        if len(ranked) > 1 and (ranked[0]["authority_score"] - ranked[1]["authority_score"] < 0.05) and not top["is_certified"]:
            item = {
                "queue_id": f"Q-{len(self.review_queue)+1:03d}",
                "user_prompt": user_prompt,
                "metric_name": target_metric,
                "reason": "SEMANTIC_CONFLICT_AMBIGUITY",
                "competing_ids": [r["def_id"] for r in ranked[:2]],
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "PENDING_STEWARD"
            }
            self.review_queue.append(item)
            return {
                "status": "AMBIGUOUS_CONFLICT",
                "top_choice": top,
                "message": "Multiple conflicting definitions found. Escalated to Steward Review Queue.",
                "queue_item": item
            }

        return {
            "status": "RESOLVED_AUTHORITATIVE",
            "selected_definition": top,
            "authority_score": top["authority_score"],
            "sql_to_execute": top["sql_template"]
        }

    def steward_approve_and_certify(self, def_id: str, steward_name: str) -> Dict[str, Any]:
        """
        Enables a data steward to promote an inferred definition to Certified Gold status.
        """
        if def_id not in self.definitions:
            return {"status": "ERROR", "message": f"Definition {def_id} not found."}

        d = self.definitions[def_id]
        d["is_certified"] = True
        d["certified_by"] = steward_name
        d["authority_score"] = self.compute_authority_score(d)

        # Clear matching items in review queue
        self.review_queue = [q for q in self.review_queue if q.get("metric_name") != d["metric_name"]]

        return {
            "status": "PROMOTED_AND_CERTIFIED",
            "def_id": def_id,
            "new_authority_score": d["authority_score"],
            "steward": steward_name
        }

if __name__ == "__main__":
    engine = OntoRankEngine()
    # Register candidate 1: Certified Finance definition by Lead Steward
    engine.register_definition(
        def_id="DEF-FIN-01",
        metric_name="ARR",
        domain="Finance",
        author="Dana Whitlock",
        author_seniority=1.0,
        sql_template="SELECT SUM(net_amount) FROM gold.finance.fact_transactions WHERE transaction_type = 'RECURRING'",
        is_certified=True,
        monthly_executions=15000,
        days_since_update=2
    )

    # Register candidate 2: Uncertified Sales team interpretation
    engine.register_definition(
        def_id="DEF-SALES-02",
        metric_name="ARR",
        domain="Sales",
        author="Junior Analyst",
        author_seniority=0.4,
        sql_template="SELECT SUM(gross_amount) * 1.1 FROM raw.crm_pipeline",
        is_certified=False,
        monthly_executions=300,
        days_since_update=45
    )

    result = engine.resolve_metric_query("What is our total ARR for this quarter?", "ARR")
    print("Resolution outcome:", result["status"], "Chosen:", result["selected_definition"]["def_id"])
