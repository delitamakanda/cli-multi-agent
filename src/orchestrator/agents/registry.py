from typing import Any
from orchestrator.agents.specialist import SpecialistAgent
from orchestrator.domain.models import RepositoryContext

class AgentRegistry:
    def __init__(
        self,
        provider: Any,  # Replace 'Any' with the actual type of your provider if known
        settings: Any,  # Replace 'Any' with the actual type of your settings if known
    ):
        self.provider = provider
        self.settings = settings

    def resolve(
        self,
        repository_context: RepositoryContext,
        plugins: list[Any] | tuple[Any, ...] | None = None,
    ) -> list[SpecialistAgent]:
        agents: list[SpecialistAgent] = []

        for name, config in self.settings.agents.items():
            if not config.enabled:
                continue
            if not config.agent_id:
                continue
            if not self._supports_stack(config, repository_context):
                continue

            agents.append(
                SpecialistAgent(
                    name=name,
                    agent_id=config.agent_id,
                    provider=self.provider,
                    description=config.description,
                )
            )
        return agents
    
    def _supports_stack(self, config: Any, repository_context: RepositoryContext) -> bool:
        supported_frameworks = set(config.frameworks)
        if not supported_frameworks:
            return True  # If no specific frameworks are defined, assume support for all
        
        detected_frameworks = repository_context.stack.frameworks
        return bool(supported_frameworks & detected_frameworks)