import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from databricks_live_workspace.client.workspace_config import get_workspace_config
from databricks_live_workspace.client.live_workspace_client import DatabricksLiveWorkspaceClient

class TestDatabricksLiveWorkspaceIntegration(unittest.TestCase):
    def setUp(self):
        self.client = DatabricksLiveWorkspaceClient()

    def test_live_workspace_credentials_configured(self):
        """Verifies live workspace ID, user email, region, and OpenSharingID are loaded."""
        config = get_workspace_config()
        self.assertEqual(config["workspace_id"], "7474649578236440")
        self.assertEqual(config["user_email"], "hybridgenai@gmail.com")
        self.assertEqual(config["open_sharing_id"], "aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9")
        self.assertEqual(config["region"], "us-east-2")
        self.assertEqual(config["cloud_provider"], "AWS")

    def test_client_connection_status(self):
        """Verifies client connection status and configuration payload."""
        status = self.client.get_connection_status()
        self.assertIn("user_email", status)
        self.assertEqual(status["workspace_id"], "7474649578236440")
        self.assertEqual(status["open_sharing_id"], "aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9")

    def test_delta_sharing_recipient_inspection(self):
        """Verifies Delta Sharing recipient configuration for open sharing ID."""
        ds_info = self.client.inspect_live_delta_sharing()
        self.assertEqual(ds_info["open_sharing_id"], "aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9")
        self.assertEqual(ds_info["sharing_type"], "DATABRICKS_TO_DATABRICKS_OPEN_SHARING")
        self.assertGreaterEqual(len(ds_info["shares_accessible"]), 1)
        self.assertEqual(ds_info["status"], "READY_FOR_FEDERATED_EXCHANGE")

    def test_unity_catalog_modeled_scan(self):
        """Verifies Unity Catalog preview and table governance status."""
        uc_scan = self.client.execute_live_unity_catalog_scan()
        self.assertIn(uc_scan["status"], ["READY", "CONNECTED"])
        self.assertEqual(uc_scan["target_workspace"], "7474649578236440")

if __name__ == '__main__':
    unittest.main()
