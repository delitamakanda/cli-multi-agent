from typing import Any

from orchestrator.domain.models import RepositoryContext

class ContextBuilder:
    def __init__(self, token_budget: int) -> None:
        self._token_budget = token_budget

    def build_for_agent(
        self,
        agent: Any,
        repository_context: RepositoryContext,
        plugins: list[Any] | tuple[Any, ...] | None = None,
    ) -> str:
        sections: list[str] = []

        sections.append(
            self._build_repository_header(repository_context)
        )

        sections.append(
            self._build_stack_section(repository_context)
        )

        sections.append(
            self._build_manifest_section(repository_context)
        )

        sections.append(
            self._build_files_section(repository_context)
        )

        if plugins:
            sections.append(
                self._build_plugins_section(plugins)
            )
        
        context = "\n\n".join(
            section for section in sections if section
        )

        return self._truncate(context)
    
    @staticmethod
    def _build_repository_header(repository_context: RepositoryContext) -> str:
        return (
            "Repository\n\n"
            f"Name: {repository_context.name}\n"
            f"Path: {repository_context.source}\n"
        )
    
    @staticmethod
    def _build_stack_section(repository_context: RepositoryContext) -> str:
        stack = repository_context.stack

        languages = ", ".join(sorted(stack.languages)) or "Unknown"
        frameworks = ", ".join(sorted(stack.frameworks)) or "None"
        tools = ", ".join(sorted(stack.tools)) or "None"
        
        return (
            "# Detected Stack\n\n"
            f"Languages: {languages}\n"
            f"Frameworks: {frameworks}\n"
            f"Tools: {tools}\n"
            f"Monorepo: {'Yes' if stack.is_monorepo else 'No'}\n"
        )
    
    @staticmethod
    def _build_manifest_section(repository_context: RepositoryContext) -> str:
        if not repository_context.manifests:
            return ""
        
        sections = ["# Manifest\n"]

        for path, content in repository_context.manifests.items():
            sections.append(f"## {path}\n\n```\n{content}\n```\n")

        return "\n".join(sections)
    
    @staticmethod
    def _build_files_section(repository_context: RepositoryContext) -> str:
        if not repository_context.files:
            return ""
        
        sections = ["# Files\n"]

        for source_file in repository_context.files:
            if not source_file.content:
                continue

            language = source_file.language or "text"

            sections.append(
                f"## {source_file.path}\n\n"
                f"Size: {source_file.size} bytes\n"
                f"Language: {language}\n"
                f"Content:\n```\n{source_file.content}\n```\n"
            )

        return "\n".join(sections)
    
    @staticmethod
    def _build_plugins_section(plugins: list[Any] | tuple[Any, ...]) -> str:
        names = [
            getattr(plugin, "name", plugin.__class__.__name__) for plugin in plugins
        ]
        
        return (
            "# Plugins\n\n"
            "The following plugins were applied:\n"
            + "\n".join(f"- {name}" for name in names)
        )
    
    def _truncate(self, context: str) -> str:
        max_characters = self._token_budget * 4  # Approximate character count based on token budget

        if len(context) <= max_characters:
            return context
        
        return (
            context[:max_characters] + "\n\n[Context truncated due to token budget]"
        )