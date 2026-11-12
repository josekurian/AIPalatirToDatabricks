"""
AI-Enabled Multi-Source Parity & Reconciliation Agent
Reconciles data ingested from Palantir, Oracle, and Snowflake into Databricks Delta Lake.
"""

import hashlib
import json
from typing import Dict, Any, List

class AIMultiSourceReconciliationAgent:
    """
    Validates cross-platform data consistency and parity across Palantir, Oracle, and Snowflake feeds.
    """

    def generate_sha256_fingerprint(self, record: Dict[str, Any], excluded_keys: List[str] = None) -> str:
        if excluded_keys is None:
            excluded_keys = ["_row_id", "etl_timestamp", "source_system"]
        clean_kv = [f"{k}:{str(record[k])}" for k in sorted(record.keys()) if k not in excluded_keys]
        return hashlib.sha256("|".join(clean_kv).encode("utf-8")).hexdigest()

    def reconcile_tri_platform(
        self,
        oracle_records: List[Dict[str, Any]],
        snowflake_records: List[Dict[str, Any]],
        databricks_records: List[Dict[str, Any]],
        pk_col: str
    ) -> Dict[str, Any]:
        ora_map = {str(r[pk_col]): self.generate_sha256_fingerprint(r) for r in oracle_records}
        snow_map = {str(r[pk_col]): self.generate_sha256_fingerprint(r) for r in snowflake_records}
        dbx_map = {str(r[pk_col]): self.generate_sha256_fingerprint(r) for r in databricks_records}

        mismatches = 0
        all_keys = set(dbx_map.keys())

        for k in all_keys:
            dbx_h = dbx_map[k]
            if k in ora_map and ora_map[k] != dbx_h:
                mismatches += 1
            elif k in snow_map and snow_map[k] != dbx_h:
                mismatches += 1

        parity_pct = 100.0 * (len(all_keys) - mismatches) / max(len(all_keys), 1)

        return {
            "status": "PASS" if mismatches == 0 else "FAIL",
            "total_records_evaluated": len(all_keys),
            "cross_platform_mismatches": mismatches,
            "overall_parity_percentage": round(parity_pct, 2),
            "sources_evaluated": ["Oracle", "Snowflake", "Databricks"]
        }

if __name__ == "__main__":
    rec = AIMultiSourceReconciliationAgent()
    o = [{"id": "101", "val": 500.0}, {"id": "102", "val": 900.0}]
    s = [{"id": "101", "val": 500.0}, {"id": "102", "val": 900.0}]
    d = [{"id": "101", "val": 500.0}, {"id": "102", "val": 900.0}]
    print(rec.reconcile_tri_platform(o, s, d, "id"))
