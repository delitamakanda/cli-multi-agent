from pathlib import Path

import typer
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

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


class CliProgressReporter:
    """Drives a rich progress display from AuditService's progress events."""

    def __init__(self, progress: Progress) -> None:
        self._progress = progress
        self._stage_task = progress.add_task("Initialisation...", total=None)
        self._agents_task: int | None = None

    def stage(self, message: str) -> None:
        self._progress.update(self._stage_task, description=message)

    def agents_planned(self, total: int) -> None:
        if total <= 0:
            return
        self._agents_task = self._progress.add_task("Agents spécialisés", total=total)

    def agent_done(self, name: str, success: bool) -> None:
        if self._agents_task is not None:
            self._progress.advance(self._agents_task)


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

    # spinner_name="line" avoids braille glyphs, which crash on non-UTF-8 Windows consoles.
    with Progress(
        SpinnerColumn(spinner_name="line"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress_bar:
        reporter = CliProgressReporter(progress_bar)

        try:
            reporter.stage(f"Préparation du dépôt {repository}...")
            with resolver.resolve(
                repository,
                ref=ref,
                depth=None if depth == 0 else depth,
                token=token,
            ) as repository_path:
                source = repository if resolver.is_remote(repository) else None
                result = audit_service.analyze(
                    repository_path=repository_path,
                    generate_roadmap=not no_roadmap,
                    source=source,
                    progress=reporter,
                )

                paths = audit_service.write_reports(
                    audit_result=result,
                    output_dir=output,
                    formats=format_,
                    progress=reporter,
                )
        except RepositorySourceError as error:
            typer.secho(str(error), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from error

        reporter.stage("Terminé.")

    for path in paths:
        typer.echo(f"Report written to: {path}")
