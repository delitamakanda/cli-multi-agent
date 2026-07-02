from dataclasses import dataclass, field
from pathlib import Path

from orchestrator.discovery.stack_detector import DetectedStack

@dataclass(slots=True)
class AuditResult:
    stack: DetectedStack
    repository_context: "RepositoryContext"
    final_report: str
    roadmap: str | None = None

@dataclass(slots=True)
class SourceFile:
    path: Path
    language: str | None
    size: int
    content: str | None = None
    importance: int = 0


@dataclass(slots=True)
class RepositoryContext:
    repository_path: Path
    name: str
    stack: DetectedStack
    files: list[SourceFile] = field(default_factory=list)
    manifests: dict[str, str] = field(default_factory=dict)
    git_summary: str = ""

    