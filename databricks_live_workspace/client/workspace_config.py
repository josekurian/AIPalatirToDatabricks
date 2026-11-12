"""
Databricks Live Workspace Configuration
Coordinates connection to AWS Databricks Workspace (WorkspaceID: 7474649578236440, Region: us-east-2),
Delta Sharing Recipient Activation (OpenSharingID: aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9),
and Service Principal / Personal Access Token (PAT) authentication.
"""

import os
import json
from typing import Dict, Any, Optional

DEFAULT_WORKSPACE_CONFIG = {
    "user_email": "hybridgenai@gmail.com",
    "workspace_id": "7474649578236440",
    "account_id": "c98bdd7d-c782-4d45-9ebc-47458f9ed667",
    "cloud_provider": "AWS",
    "region": "us-east-2",
    "workspace_host": "https://dbc-fe2b9eb9-5caf.cloud.databricks.com",
    "launch_url": "https://dbc-fe2b9eb9-5caf.cloud.databricks.com/?email=hybridgenai%40gmail.com&intent=SIGN_UP&dbx_source=www&autoLogin=true&account_id=c98bdd7d-c782-4d45-9ebc-47458f9ed667&o=7474649578236440",
    "open_sharing_id": "aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9",
    "delta_sharing_recipient": "palantir_oracle_migration_recipient",
    "auth_type": "PAT_OR_OAUTH",
    "token_env_var": "DATABRICKS_TOKEN"
}

CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_workspace_config.json")

def get_workspace_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_WORKSPACE_CONFIG

def save_workspace_config(config_data: Dict[str, Any]):
    merged = {**get_workspace_config(), **config_data}
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(merged, f, indent=2)
    return merged

if not os.path.exists(CONFIG_FILE_PATH):
    save_workspace_config(DEFAULT_WORKSPACE_CONFIG)
