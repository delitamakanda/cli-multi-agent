from abc import ABC, abstractmethod
from pathlib import Path

from orchestrator.domain.models import RepositoryContext

class StackPlugin(ABC):
    name: str

    @abstractmethod
    def supports(self, repository_context: RepositoryContext) -> bool:
        pass

    def relevant_patterns(self) -> tuple[str, ...]:
        return ()
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return ()
    
    def recommended_agents(self) -> set[str]:
        return set()
    
    def prompt_context(self, repository_context: RepositoryContext) -> str:
        return ""
    
    def local_checks(self, repository_context: RepositoryContext) -> list[list[str]]:
        return []