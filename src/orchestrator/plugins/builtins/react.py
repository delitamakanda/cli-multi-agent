from orchestrator.plugins.base import LocalCheck, StackPlugin


class ReactPlugin(StackPlugin):
    name = "react"

    def supports(self, repository_context) -> bool:
        files = repository_context.files
        return (
            "package.json" in files
            and "react" in repository_context.stack.frameworks
        )
    
    def relevant_patterns(self) -> tuple[str, ...]:
        return (
            "package.json",
            "src/**/*.js",
            "src/**/*.jsx",
            "src/**/*.ts",
            "src/**/*.tsx",
            "public/index.html",
        )
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return (
            "node_modules",
            "build",
            "dist",
            "coverage",
        )
    
    def recommended_agents(self) -> frozenset[str]:
        return frozenset(
            "architecture",
            "qualité",
            "performance",
            "accessibilité",
            "ui/ux",
            "mentor",
        )
    
    def prompt_context(self, repository_context) -> str:
        return """
Le dépôt utilise React

Vérifier notemment:
- La séparation entre présentation, états et acceès aux données
- La gestion des composants et des hooks
- La gestion des dépendances et des injections
- La gestion des exceptions et des erreurs
- La validation des entrées et des sorties
- La documentation des composants et des props
- La sécurité des composants et des données
- La couverture des tests unitaires et d'intégration
- L'utilisation correcte des middlewares et des routers
- La performance des composants et de l'application
- L'utilisation correcte des contextes et des providers
- L'utilisation correcte des lazy loading et des suspense
"""

    def local_checks(self, repository_context) -> tuple[LocalCheck, ...]:
        return (
            LocalCheck(
                name="React Linter",
                command=("npm", "run", "lint"),
                timeout_seconds=120,
                required=True,
        ),
        LocalCheck(
            name="React Tests",
                command=("npm", "run", "test"),
                timeout_seconds=300,
                required=True,
        )
        )
    