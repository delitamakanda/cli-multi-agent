from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from orchestrator.domain.models import RepositoryContext

@dataclass(frozen=True)
class LocalCheck:
    name: str
    command: str
    timeout_seconds: int = 60
    required: bool = False
    working_directory: Path | None = None

class StackPlugin(ABC):
    name: str

    @abstractmethod
    def supports(self, repository_context: RepositoryContext) -> bool:
        raise NotImplementedError

    def relevant_patterns(self) -> tuple[str, ...]:
        return ()
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return ()
    
    def recommended_agents(self) -> set[str]:
        return frozenset()
    
    def prompt_context(self, repository_context: RepositoryContext) -> str:
        return ""
    
    def local_checks(self, repository_context: RepositoryContext) -> tuple[LocalCheck, ...]:
        return ()
