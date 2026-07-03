from dataclasses import dataclass, field
from pathlib import Path
import json
import tomllib


@dataclass(slots=True)
class DetectedStack:
    languages: set[str] = field(default_factory=set)
    frameworks: set[str] = field(default_factory=set)
    tools: set[str] = field(default_factory=set)
    is_monorepo: bool = False

    def display_name(self) -> str:
        parts: list[str] = []
        if self.frameworks:
            parts.extend(sorted(self.frameworks))
        elif self.languages:
            parts.extend(sorted(self.languages))
        return ", ".join(parts) if parts else "Inconnu"


class StackDetector:
    def detect(self, repository: Path) -> DetectedStack:
        stack = DetectedStack()

        self._detect_python(repository, stack)
        self._detect_javascript(repository, stack)
        self._detect_dotnet(repository, stack)
        self._detect_java(repository, stack)
        self._detect_monorepo(repository, stack)
        self._detect_infrastructure(repository, stack)

        return stack
    
    def _detect_python(self, repository: Path, stack: DetectedStack):
        # Detect Python language
        if any(repository.glob("**/*.py")):
            stack.languages.add("Python")

        # Detect Python frameworks
        if (repository / "requirements.txt").exists():
            with open(repository / "requirements.txt") as f:
                requirements = f.read()
                if "django" in requirements.lower():
                    stack.frameworks.add("Django")
                if "flask" in requirements.lower():
                    stack.frameworks.add("Flask")
                if "fastapi" in requirements.lower():
                    stack.frameworks.add("FastAPI")

        if (repository / "pyproject.toml").exists():
            with open(repository / "pyproject.toml", "rb") as f:
                pyproject = tomllib.load(f)
                dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
                if "django" in dependencies:
                    stack.frameworks.add("Django")
                if "flask" in dependencies:
                    stack.frameworks.add("Flask")
                if "fastapi" in dependencies:
                    stack.frameworks.add("FastAPI")

    def _detect_javascript(self, repository: Path, stack: DetectedStack):
        # Detect JavaScript language
        if any(repository.glob("**/*.js")) or any(repository.glob("**/*.ts")):
            stack.languages.add("JavaScript")

        # Detect JavaScript frameworks
        if (repository / "package.json").exists():
            with open(repository / "package.json") as f:
                package_json = json.load(f)
                dependencies = package_json.get("dependencies", {})
                dev_dependencies = package_json.get("devDependencies", {})
                all_dependencies = {**dependencies, **dev_dependencies}
                if "react" in all_dependencies:
                    stack.frameworks.add("React")
                if "vue" in all_dependencies:
                    stack.frameworks.add("Vue.js")
                if "angular" in all_dependencies:
                    stack.frameworks.add("Angular")
                if "express" in all_dependencies:
                    stack.frameworks.add("Express.js")

    def _detect_dotnet(self, repository: Path, stack: DetectedStack):
        # Detect .NET language
        if any(repository.glob("**/*.cs")):
            stack.languages.add(".NET")

        # Detect .NET frameworks
        if any(repository.glob("**/*.csproj")):
            stack.frameworks.add(".NET Core")
        if any(repository.glob("**/*.sln")):
            stack.frameworks.add(".NET Framework")
    
    def _detect_java(self, repository: Path, stack: DetectedStack):
        # Detect Java language
        if any(repository.glob("**/*.java")):
            stack.languages.add("Java")

        # Detect Java frameworks
        if (repository / "pom.xml").exists():
            stack.frameworks.add("Maven")
        if (repository / "build.gradle").exists() or (repository / "build.gradle.kts").exists():
            stack.frameworks.add("Gradle")
        if any(repository.glob("**/spring-boot*.jar")):
            stack.frameworks.add("Spring Boot")
    
    def _detect_monorepo(self, repository: Path, stack: DetectedStack):
        # Detect monorepo structure
        if (repository / "lerna.json").exists() or (repository / "pnpm-workspace.yaml").exists():
            stack.is_monorepo = True
        elif any((repository / "packages").glob("*")):
            stack.is_monorepo = True
        elif any((repository / "apps").glob("*")) and any((repository / "libs").glob("*")):
            stack.is_monorepo = True

    def _detect_infrastructure(self, repository: Path, stack: DetectedStack):
        # Detect infrastructure as code tools
        if any(repository.glob("**/*.tf")):
            stack.tools.add("Terraform")
        if any(repository.glob("**/*.yml")) or any(repository.glob("**/*.yaml")):
            stack.tools.add("Ansible")
        if (repository / "docker-compose.yml").exists() or (repository / "docker-compose.yaml").exists():
            stack.tools.add("Docker Compose")
        if (repository / "Dockerfile").exists():
            stack.tools.add("Docker")

    @staticmethod
    def _read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file {path}: {e}"
        
    @staticmethod
    def _read_pyproject_toml(path: Path) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)
    