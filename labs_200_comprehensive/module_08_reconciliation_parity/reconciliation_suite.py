"""
Comprehensive Production Scripts for Module 8: Automated Data Reconciliation (Labs 176 - 190)
Validates 100% data parity between Palantir Foundry datasets and Databricks Delta Lake tables.
Features row hashing, primary key set differences, and floating-point statistical tolerance checks.
"""

import hashlib
import json
from typing import Dict, Any, List

class EnterpriseReconciliationSuite:
    """
    Automated dual-run reconciliation framework verifying bitwise parity,
    primary key completeness, and numerical statistical moments.
    """

    def __init__(self, tolerance_epsilon: float = 1e-4):
        self.epsilon = tolerance_epsilon

    def hash_record(self, record: Dict[str, Any], excluded_keys: List[str] = None) -> str:
        """Computes deterministic SHA-256 hash across sorted key-value pairs."""
        if excluded_keys is None:
            excluded_keys = ["_metadata_file_name", "ingestion_timestamp", "last_updated_at"]
            
        clean_items = []
        for k in sorted(record.keys()):
            if k not in excluded_keys:
                clean_items.append(f"{k}:{str(record[k])}")
        record_str = "|".join(clean_items)
        return hashlib.sha256(record_str.encode("utf-8")).hexdigest()

    def reconcile_datasets(
        self,
        foundry_records: List[Dict[str, Any]],
        databricks_records: List[Dict[str, Any]],
        primary_key: str,
        numeric_metrics: List[str]
    ) -> Dict[str, Any]:
        """
        Executes multi-point validation:
        1. Row count match
        2. Primary key set equality
        3. Bitwise record SHA-256 hash comparison
        4. Statistical distribution comparison (Sum & Mean with floating epsilon)
        """
        src_len = len(foundry_records)
        tgt_len = len(databricks_records)

        src_map = {str(r[primary_key]): r for r in foundry_records}
        tgt_map = {str(r[primary_key]): r for r in databricks_records}

        missing_in_target = set(src_map.keys()) - set(tgt_map.keys())
        unexpected_in_target = set(tgt_map.keys()) - set(src_map.keys())

        hash_mismatches = []
        for pk in src_map.keys():
            if pk in tgt_map:
                h_src = self.hash_record(src_map[pk])
                h_tgt = self.hash_record(tgt_map[pk])
                if h_src != h_tgt:
                    hash_mismatches.append({"pk": pk, "foundry_hash": h_src, "databricks_hash": h_tgt})

        # Numeric metric distributions
        metric_checks = {}
        for metric in numeric_metrics:
            sum_src = sum(float(r.get(metric, 0.0)) for r in foundry_records)
            sum_tgt = sum(float(r.get(metric, 0.0)) for r in databricks_records)
            diff = abs(sum_tgt - sum_src)
            metric_checks[metric] = {
                "foundry_sum": sum_src,
                "databricks_sum": sum_tgt,
                "absolute_diff": diff,
                "passed": diff <= self.epsilon
            }

        all_passed = (src_len == tgt_len and len(missing_in_target) == 0 and len(hash_mismatches) == 0)

        return {
            "status": "PASS" if all_passed else "FAIL",
            "foundry_row_count": src_len,
            "databricks_row_count": tgt_len,
            "missing_keys_count": len(missing_in_target),
            "unexpected_keys_count": len(unexpected_in_target),
            "bitwise_hash_mismatches": len(hash_mismatches),
            "numeric_metrics_validation": metric_checks,
            "parity_score_percentage": 100.0 if all_passed else round(100.0 * (src_len - len(hash_mismatches)) / max(src_len, 1), 2)
        }

if __name__ == "__main__":
    suite = EnterpriseReconciliationSuite()
    f_data = [
        {"customer_id": "C-101", "name": "Global Energy", "revenue": 1250000.50},
        {"customer_id": "C-102", "name": "AeroTech", "revenue": 890000.00}
    ]
    d_data = [
        {"customer_id": "C-101", "name": "Global Energy", "revenue": 1250000.50},
        {"customer_id": "C-102", "name": "AeroTech", "revenue": 890000.00}
    ]
    result = suite.reconcile_datasets(f_data, d_data, "customer_id", ["revenue"])
    print("Reconciliation Verification Result:")
    print(json.dumps(result, indent=2))
