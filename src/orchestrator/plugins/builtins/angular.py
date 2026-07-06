from orchestrator.plugins.base import LocalCheck, StackPlugin


class AngularPlugin(StackPlugin):
    name = "angular"

    def supports(self, repository_context) -> bool:
        files = repository_context.files
        return (
            "angular.json" in files
            or "angular" in repository_context.stack.frameworks
        )
    
    def relevant_patterns(self) -> tuple[str, ...]:
        return (
            "angular.json",
            "package.json",
            "src/environments",
            "tsconfig.json",
            "src/**/*.ts",
            "src/**/*.html",
            "src/**/*.scss",
            "src/**/*.css",
        )
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return (
            "node_modules",
            "dist",
            "out-tsc",
            "coverage",
            ".angular",
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
Le dépôt utilise Angular

Vérifier notemment:
- La séparation entre présentation, états et acceès aux données
- les composants standalone
- Le lazy loading des routes
- Les subscriptions aux observables et la gestion des unsubscribe
- Les performances des composants et de l'application
- La taille du bundle et la gestion des assets
- La duplication de code et la réutilisation des composants
- La couverture des tests unitaires et e2e
- L'utilisation correcte des signals
"""

    def local_checks(self, repository_context) -> tuple[LocalCheck, ...]:
        return (
            LocalCheck(
                name="Angular lint",
                command=('npm', 'run', 'lint'),
                timeout_seconds=120,
                required=True,
            ),
            LocalCheck(
                name="Angular tests",
                command=('npm', 'run', 'test', '--', '--watch=false', '--browsers=ChromeHeadless'),
                timeout_seconds=300,
                required=True,
            ),
        )