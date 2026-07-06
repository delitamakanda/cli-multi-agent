from orchestrator.plugins.base import LocalCheck, StackPlugin

class DjangoPlugin(StackPlugin):
    name = "django"

    def supports(self, repository_context) -> bool:
        files = repository_context.files.path
        return (
            "manage.py" in files
            or "django" in repository_context.stack.frameworks
        )
    
    def relevant_patterns(self) -> tuple[str, ...]:
        return (
            "manage.py",
            "requirements.txt",
            "pyproject.toml",
            "settings.py",
            "urls.py",
            "wsgi.py",
            "asgi.py",
            "**/*.py",
        )
    
    def ignored_patterns(self) -> tuple[str, ...]:
        return (
            "venv",
            "env",
            ".venv",
            ".env",
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.db",
            "*.sqlite3",
        )
    
    def recommended_agents(self) -> frozenset[str]:
        return frozenset(
            "architecture",
            "qualité",
            "performance",
            "sécurité",
            "devops",
        )
    
    def prompt_context(self, repository_context) -> str:
        return """
Le dépôt utilise Django

Vérifier notemment:
- La structure du projet et l'organisation des applications
- La configuration des settings et la gestion des secrets
- La sécurité des vues et des modèles
- La performance des requêtes et l'utilisation de l'ORM
- La couverture des tests unitaires et d'intégration
- L'utilisation des migrations et la gestion de la base de données
- La conformité aux bonnes pratiques de Django et de Python
- L'utilisation des middlewares et des signaux
- La gestion des fichiers statiques et des templates
- L'utilisation des formulaires et de la validation des données
"""

    def local_checks(self, repository_context) -> tuple[LocalCheck, ...]:
        return (
            LocalCheck(
                name="django-checks",
                description="Exécute les vérifications intégrées de Django",
                command=["python", "manage.py", "check"],
            ),
            LocalCheck(
                name="django-test",
                description="Exécute les tests unitaires de Django",
                command=["python", "manage.py", "test"],
            ),
        )
    
    