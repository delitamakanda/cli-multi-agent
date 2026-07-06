from orchestrator.plugins.base import LocalCheck, StackPlugin


class FastAPIPlugin(StackPlugin):
    name = "fastapi"

    def supports(self, repository_context) -> bool:
        files = repository_context.files
        return (
            "main.py" in files
            or "app.py" in files
            or "fastapi" in repository_context.stack.frameworks
        )
    
    def relevant_patterns(self) -> tuple[str, ...]:
        return (
            "main.py",
            "app.py",
            "requirements.txt",
            "pyproject.toml",
            "Pipfile",
            "src/**/*.py",
        )
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return (
            "__pycache__",
            ".venv",
            "venv",
            ".mypy_cache",
            ".pytest_cache",
        )
    
    def recommended_agents(self) -> frozenset[str]:
        return frozenset(
            "architecture",
            "qualité",
            "performance",
            "accessibilité",
            "securité",
        )
    
    def prompt_context(self, repository_context) -> str:
        return """
Le dépôt utilise FastAPI
Vérifier notemment:
- La séparation entre présentation, états et acceès aux données
- La gestion des dépendances et des injections
- La gestion des exceptions et des erreurs
- La validation des entrées et des sorties
- La documentation automatique des endpoints
- La sécurité des endpoints et des données
- La couverture des tests unitaires et d'intégration
- L'utilisation correcte des middlewares et des routers
- La performance des endpoints et de l'application
- L'utilisation correcte des background tasks et des events
"""

    def local_checks(self, repository_context) -> tuple[LocalCheck, ...]:
        return ()