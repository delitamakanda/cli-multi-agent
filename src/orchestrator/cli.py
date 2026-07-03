from pathlib import Path

import typer

from orchestrator.application.audit_service import AuditService
from orchestrator.bootstrap import build_application
from orchestrator.discovery.repository_source import (
    RepositorySourceError,
    RepositorySourceResolver,
)

app = typer.Typer(
    help="A command line tool to audit a git repository for security vulnerabilities and license compliance issues.",
    no_args_is_help=True
)

@app.command()
def analyze(
    repository: str = typer.Argument(
        ".",
        help="Local repository path or remote Git URL to audit.",
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
    no_roadmap: bool = typer.Option(
        False,
        "--no-roadmap",
    ),
    ref: str | None = typer.Option(
        None,
        "--ref",
        help="Branch, tag, or commit to check out before analysis.",
    ),
    depth: int | None = typer.Option(
        1,
        "--depth",
        help="Clone depth for remote repositories. Use 0 for a full clone.",
    ),
    token: str | None = typer.Option(
        None,
        "--token",
        envvar="REPO_AUDIT_TOKEN",
        help="Access token for authenticating with a private remote repository.",
    ),
) -> None:
    """
    Analyze a git repository for security vulnerabilities and license compliance issues.
    """
    audit_service: AuditService = build_application(config)
    resolver = RepositorySourceResolver()

    try:
        with resolver.resolve(
            repository,
            ref=ref,
            depth=None if depth == 0 else depth,
            token=token,
        ) as repository_path:
            result = audit_service.analyze(
                repository_path=repository_path,
                generate_roadmap=not no_roadmap,
            )

            paths = audit_service.write_reports(
                audit_result=result,
                output_dir=output,
                formats=format_
            )
    except RepositorySourceError as error:
        typer.secho(str(error), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from error

    for path in paths:
        typer.echo(f"Report written to: {path}")
