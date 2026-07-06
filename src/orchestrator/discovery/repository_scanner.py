
from orchestrator.config import settings
from pathlib import Path
from orchestrator.discovery.stack_detector import DetectedStack
from orchestrator.domain.models import RepositoryContext, SourceFile

DEFAULT_IGNORED_DIRECTORIES = [
    ".git",
    ".github",
    ".vscode",
    "node_modules",
    "venv",
    "__pycache__",
    ".idea",
    "dist",
    "build",
    "__pycache__",
    "coverage",
    ".ruff_cache",
]

TEXT_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".scss",
    ".css",
    ".html",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".sln",
    ".cs",
    ".csproj",
    ".tf",
    ".xml",
]

MANIFEST_NAMES = [
    "package.json",
    "requirements.txt",
    "Pipfile",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Gemfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Cargo.toml",
    "go.mod",
    "composer.json",
]

class RepositoryScanner:
    def __init__(
        self,
        ignored: list[str] | set[str] | None = None,
        max_file_size: int = 200000,
        max_content_length: int = 1000000,
    ) -> None:
        configured_ignored = {
            item.strip() for item in (ignored or []) if item and item.strip()
        }
        self.ignored = configured_ignored or DEFAULT_IGNORED_DIRECTORIES
        self.max_file_size = max_file_size
        self.max_content_length = max_content_length

    def scan(
            self,
            repository_path: Path,
            stack: DetectedStack,
            source: str | None = None,
    ) -> RepositoryContext:
        repository_path = repository_path.resolve()

        files: list[SourceFile] = []
        manifest_files: dict[str, str] = {}

        for path in repository_path.rglob("*"):
            if self._is_ignored(path, repository_path):
                continue

            if not path.is_file():
                continue

            try:
                file_size = path.stat().st_size
            except OSError:
                continue

            if file_size > self.max_file_size:
                continue

            if not self._is_supported_file(path):
                continue

            content = self._read_text(path)
            relative_path = path.relative_to(repository_path)

            source_file = SourceFile(
                path=relative_path,
                language=self._detect_language(path),
                size=file_size,
                content=content[: self.max_content_length],
                importance=self._calculate_importance(path),

            )
            files.append(source_file)

            if path.name in MANIFEST_NAMES:
                manifest_files[str(relative_path)] = content

        files.sort(
            key=lambda file: (-file.importance, str(file.path))
        )

        return RepositoryContext(
            repository_path=repository_path,
            name=repository_path.name,
            stack=stack,
            files=files,
            manifests=manifest_files,
            git_summary="",
            source=source or str(repository_path),
        )
    
    def _is_ignored(
            self,
            path: Path,
            repository_path: Path
    ) -> bool:
        relative_parts = path.relative_to(repository_path).parts
        return any(part in self.ignored for part in relative_parts)
    
    @staticmethod
    def _is_supported_file(path: Path) -> bool:
        return path.suffix.lower() in TEXT_EXTENSIONS or path.name in MANIFEST_NAMES
    
    @staticmethod
    def _read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except (UnicodeDecodeError, OSError):
            return ""
        
    @staticmethod
    def _detect_language(path: Path) -> str:
        extension_to_language = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "JavaScript",
            ".tsx": "TypeScript",
            ".java": "Java",
            ".scss": "SCSS",
            ".css": "CSS",
            ".html": "HTML",
            ".json": "JSON",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".md": "Markdown",
            ".sln": "C#",
            ".cs": "C#",
            ".csproj": "C#",
            ".tf": "Terraform",
            ".xml": "XML",
            ".tf": "Terraform",
            ".toml": "TOML",
            ".gradle": "Gradle",
            ".kts": "Kotlin",
        }
        return extension_to_language.get(path.suffix.lower(), "Unknown")
    
    @staticmethod
    def _calculate_importance(path: Path) -> int:
        score = 0

        if path.name in MANIFEST_NAMES:
            score += 100

        if path.name.lower() in {
            "README.md",
            "manage.py",
            "main.py",
            "app.py",
            "angular.json",
            "settings.py",
            "index.js",
            "index.ts",
            "index.jsx",
            "index.tsx",
            "index.html",
            "index.css",
        }:
            score += 50

        if "test" in path.parts or "tests" in path.parts:
            score += 10

        return score