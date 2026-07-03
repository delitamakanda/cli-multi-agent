
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from orchestrator.domain.models import SpecialistAgentSettings

class MistralSettings(BaseModel):
    api_key: str = ""


class ExecutionSettings(BaseModel):
    max_retries: int = 3
    max_workers: int = 5
    initial_backoff: float = 1.0
    token_budget_per_agent: int = 10000


class ScannerSettings(BaseModel):
    ignored: list[str] = Field(default_factory=lambda: [
        '.git',
        '.idea',
        '__pycache__',
        'node_modules',
        'venv',
        '.env',
        'config.yaml',
        'dist',
        '.venv',
        'build',
    ])


class AgentSettings(BaseModel):
    agent_id: str = " "


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", extra="ignore")

    mistral: MistralSettings = Field(default_factory=MistralSettings)
    execution: ExecutionSettings = Field(default_factory=ExecutionSettings)
    scanner: ScannerSettings = Field(default_factory=ScannerSettings)
    orchestrator: AgentSettings = Field(default_factory=AgentSettings)
    product_owner: AgentSettings = Field(default_factory=AgentSettings)
    agents: dict[str, SpecialistAgentSettings] = Field(default_factory=dict)
    
def load_settings(config_path: Path | None = None) -> Settings:
    load_dotenv()

    if config_path is None:
        return Settings(
            mistral=MistralSettings(api_key=_required_env("MISTRAL_API_KEY"),),
            orchestrator=AgentSettings(agent_id=_required_env("ORCHESTRATOR_AGENT_ID"),),
            product_owner=AgentSettings(agent_id=_required_env("PRODUCT_OWNER_AGENT_ID"),),
            agents={
                "architecture": SpecialistAgentSettings(
                    agent_id=_required_env("ARCHITECTURE_AGENT_ID"),
                    description="Analyse l'architecture du projet et fournit des recommandations pour l'améliorer.",
                ),
                "performance": SpecialistAgentSettings(
                    agent_id=_required_env("PERFORMANCE_AGENT_ID"),
                    description="Analyse les performances du projet et fournit des recommandations pour les améliorer.",
                ),
                "qualité": SpecialistAgentSettings(
                    agent_id=_required_env("QUALITE_AGENT_ID"),
                    description="Analyse la qualité du code et fournit des recommandations pour l'améliorer.",
                ),
                "documentation": SpecialistAgentSettings(
                    agent_id=_required_env("DOCUMENTATION_AGENT_ID"),
                    description="Analyse la documentation du projet et fournit des recommandations pour l'améliorer.",
                ),
                "mentor": SpecialistAgentSettings(
                    agent_id=_required_env("MENTOR_AGENT_ID"),
                    description="Fournit des conseils et des recommandations pour améliorer le projet.",
                ),
                "sécurité": SpecialistAgentSettings(
                    agent_id=_required_env("SECURITE_AGENT_ID"),
                    description="Analyse la sécurité du projet et fournit des recommandations pour l'améliorer.",
                ),
                "accessibilité": SpecialistAgentSettings(
                    agent_id=_required_env("ACCESSIBILITE_AGENT_ID"),
                    description="Analyse l'accessibilité du projet et fournit des recommandations pour l'améliorer.",
                ),
                "devops": SpecialistAgentSettings(
                    agent_id=_required_env("DEVOPS_AGENT_ID"),
                    description="Analyse les pratiques DevOps du projet et fournit des recommandations pour les améliorer.",
                ),
                "ui/ux": SpecialistAgentSettings(
                    agent_id=_required_env("UI_UX_AGENT_ID"),
                    description="Analyse l'interface utilisateur et l'expérience utilisateur du projet et fournit des recommandations pour les améliorer.",
                ),
            }
        )
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with config_path.open("r", encoding="utf-8") as f:
        if config_path.suffix in [".yaml", ".yml"]:
            config_data = yaml.safe_load(f) or {}
        elif config_path.suffix == ".json":
            import json
            config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")
    return Settings.model_validate(config_data)

def _required_env(var_name: str) -> str:
    import os
    value = os.getenv(var_name)
    
    if not value:
        raise ValueError(f"Required environment variable '{var_name}' is not set.")
    return value