from pathlib import Path

import typer

from orchestrator.application.audit_service import AuditService
from orchestrator.bootstrap import build_application

app = typer.Typer(
    help="A command line tool to audit a git repository for security vulnerabilities and license compliance issues.",
    no_args_is_help=True
)

@app.command()
def analyze(
    repository_path: Path = typer.Argument(
        Path("."),
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    output: Path = typer.Option(
        Path(".repo-audit"),
        "--output",
        "-o",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
    ),
    format_: list[str] = typer.Option(
        ["markdown"],
        "--format",
    ),
    no_readmap: bool = typer.Option(
        False,
        "--no-readmap",
    ),
) -> None:
    """
    Analyze a git repository for security vulnerabilities and license compliance issues.
    """
    audit_service: AuditService = build_application(config)

    result = audit_service.analyze(
        repository_path=repository_path,
        generate_roadmap=not no_readmap,
    )

    paths = audit_service.write_reports(
        audit_result=result,
        output_dir=output,
        formats=format_
    )

    for path in paths:
        typer.echo(f"Report written to: {path}")
