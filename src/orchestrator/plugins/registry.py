from orchestrator.domain.models import RepositoryContext


class PluginRegistry:
    def __init__(
        self,
        repository_context: RepositoryContext | None = None,
    ) -> None:
        self._repository_context = repository_context

    def resolve(self, repository_context: RepositoryContext) -> list:
        """
        Resolve the plugins for the given repository context.
        """
        self._repository_context = repository_context
        return []