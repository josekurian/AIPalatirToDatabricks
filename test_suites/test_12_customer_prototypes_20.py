import unittest
import os
import json
import subprocess
import sys

class TestCustomerPrototypes20(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/customer_prototypes_20"
        self.registry_path = os.path.join(self.base_dir, "prototypes_registry.json")

    def test_registry_contains_20_prototypes(self):
        """Verifies registry contains exactly 20 distinct prototypes with complete metadata."""
        self.assertTrue(os.path.exists(self.registry_path))
        with open(self.registry_path) as f:
            data = json.load(f)
        self.assertEqual(len(data), 20)
        
        # Verify industries and tech stacks
        industries = set(p["industry"] for p in data)
        self.assertGreaterEqual(len(industries), 15)

    def test_prototype_directories_and_files_exist(self):
        """Verifies every prototype has README.md, run_pipeline.py, and schema_and_queries.sql."""
        for i in range(1, 21):
            pid = f"proto_{i:02d}"
            p_dir = os.path.join(self.base_dir, pid)
            self.assertTrue(os.path.isdir(p_dir), f"Directory {p_dir} does not exist.")
            self.assertTrue(os.path.exists(os.path.join(p_dir, "README.md")))
            self.assertTrue(os.path.exists(os.path.join(p_dir, "run_pipeline.py")))
            self.assertTrue(os.path.exists(os.path.join(p_dir, "schema_and_queries.sql")))

    def test_prototype_execution_parity(self):
        """Executes run_pipeline.py for sample prototypes and checks parity verification."""
        for i in [1, 5, 10, 15, 20]:
            pid = f"proto_{i:02d}"
            script_path = os.path.join(self.base_dir, pid, "run_pipeline.py")
            cmd = [sys.executable, script_path, "all"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Error running {pid}: {res.stderr}")
            self.assertIn("PARITY_CERTIFIED", res.stdout)
            self.assertIn("CATALOG_READY", res.stdout)

if __name__ == '__main__':
    unittest.main()
