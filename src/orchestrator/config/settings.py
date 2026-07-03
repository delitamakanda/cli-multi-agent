
import os
import json
from pathlib import Path


class Settings:
    def __init__(self, config):
        self.config = config

    def get(self, key, default=None):
        return self.config.get(key, default)
    
def load_settings(config_path: Path | None = None) -> Settings:
    # Load settings from a configuration file or environment variables
    config = {}
    if config_path:
        # Load from the specified config file
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        # Load from environment variables or default values
        config = {
            "mistral": {
                "api_key": os.getenv("MISTRAL_API_KEY", ""),
            },
            "execution": {
                "max_retries": int(os.getenv("MAX_RETRIES", 3)),
                "initial_backoff": float(os.getenv("INITIAL_BACKOFF", 1.0)),
                "token_budget_per_agent": int(os.getenv("TOKEN_BUDGET_PER_AGENT", 100)),
            },
            "scanner": {
                "ignored": os.getenv("SCANNER_IGNORED", "").split(","),
            },
            "orchestrator": {
                "agent_id": os.getenv("ORCHESTRATOR_AGENT_ID", ""),
            },
            "product_owner": {
                "agent_id": os.getenv("PRODUCT_OWNER_AGENT_ID", ""),
            },
        }
    return Settings(config)