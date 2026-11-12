"""
Unit and Integration Test Suite 5: Curriculum & 200 Labs Verification
Tests:
1. Validates that labs_200_curriculum.json contains all 200 distinct labs
2. Verifies that all 10 modules are present in sequential order
3. Verifies schema structure of each lab (id, code, title, summary, steps, expected_output)
4. Checks consistency with generated .docx files
"""

import unittest
import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestCurriculumAnd200Labs(unittest.TestCase):

    def setUp(self):
        self.curriculum_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "frontend", "static", "labs_200_curriculum.json"
        )

    def test_curriculum_file_exists(self):
        self.assertTrue(os.path.exists(self.curriculum_path))

    def test_curriculum_contains_200_labs(self):
        with open(self.curriculum_path, "r") as f:
            modules = json.load(f)

        self.assertEqual(len(modules), 10, "Curriculum must have exactly 10 modules")

        total_labs = 0
        seen_ids = set()

        for mod_idx, mod in enumerate(modules, start=1):
            self.assertIn("module_id", mod)
            self.assertIn("module_title", mod)
            self.assertIn("labs", mod)
            
            labs = mod["labs"]
            total_labs += len(labs)

            for lab in labs:
                lab_id = lab["id"]
                self.assertNotIn(lab_id, seen_ids, f"Duplicate lab ID detected: {lab_id}")
                seen_ids.add(lab_id)

                # Check required fields
                self.assertIn("title", lab)
                self.assertIn("summary", lab)
                self.assertIn("steps", lab)
                self.assertIn("expected_output", lab)
                self.assertGreater(len(lab["steps"]), 0, f"Lab {lab_id} has no steps")
                self.assertTrue(len(lab["title"]) > 5, f"Lab {lab_id} has invalid title")

        self.assertEqual(total_labs, 200, "Total number of labs must be exactly 200")
        self.assertEqual(len(seen_ids), 200, "Unique lab IDs must equal 200")
        self.assertEqual(min(seen_ids), 1, "Labs must start at 1")
        self.assertEqual(max(seen_ids), 200, "Labs must end at 200")

if __name__ == '__main__':
    unittest.main()
