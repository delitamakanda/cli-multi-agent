from orchestrator.domain.models import RepositoryContext
from orchestrator.plugins.base import StackPlugin


class PluginRegistry:
    def __init__(
        self,
        plugins: list[StackPlugin],
    ) -> None:
        self._plugins = plugins

    def matching_plugins(self, repository_context: RepositoryContext) -> list[StackPlugin]:
        return [
            plugin
            for plugin in self._plugins
            if plugin.supports(repository_context)
        ]