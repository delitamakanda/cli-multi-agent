from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from orchestrator.application.progress import NullProgressReporter, ProgressReporter
from orchestrator.domain.models import AuditResult

class AuditService:
    def __init__(
            self,
            scanner,
            stack_detector,
            plugin_registry,
            agent_registry,
            context_builder,
            orchestrator,
            product_owner,
            report_generators,
            max_workers: int = 5,
        ) -> None:
        self.scanner = scanner
        self.stack_detector = stack_detector
        self.plugin_registry = plugin_registry
        self.agent_registry = agent_registry
        self.context_builder = context_builder
        self.orchestrator = orchestrator
        self.product_owner = product_owner
        self.report_generators = report_generators
        self.max_workers = max_workers

    def analyze(
        self,
        repository_path: Path,
        generate_roadmap: bool = True,
        source: str | None = None,
        progress: ProgressReporter | None = None,
    ) -> AuditResult:
        progress = progress or NullProgressReporter()

        progress.stage("Détection de la stack technique...")
        stack = self.stack_detector.detect(repository_path)

        progress.stage("Analyse des fichiers du dépôt...")
        repository_context = self.scanner.scan(repository_path, stack, source=source)

        progress.stage("Résolution des agents spécialisés...")
        plugins = self.plugin_registry.matching_plugins(repository_context)

        agents = self.agent_registry.resolve(repository_context, plugins)

        reports = self._run_agents(agents, repository_context, plugins, progress)

        progress.stage("Synthèse du rapport final...")
        final_report = self.orchestrator.synthesize(repository_context, reports)

        roadmap = None

        if generate_roadmap:
            progress.stage("Génération de la feuille de route...")
            roadmap = self.product_owner.generate_roadmap(final_report, repository_context)

        return AuditResult(
            stack=stack,
            repository_context=repository_context,
            final_report=final_report,
            roadmap=roadmap,
        )

    def _run_agents(self, agents, repository_context, plugins, progress: ProgressReporter):
        reports: dict[str, str] = {}

        progress.stage(f"Exécution de {len(agents)} agent(s) spécialisé(s)...")
        progress.agents_planned(len(agents))

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}

            for agent in agents:
                context = self.context_builder.build_for_agent(agent, repository_context, plugins)

                future = executor.submit(agent.run, context)
                futures[future] = agent.name

            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    report = future.result()
                    reports[agent_name] = report
                    progress.agent_done(agent_name, success=True)
                except Exception as e:
                    reports[agent_name] = f"Error: {str(e)}"
                    progress.agent_done(agent_name, success=False)

        return reports

    def write_reports(
        self,
        audit_result: AuditResult,
        output_dir: Path,
        formats: list[str] | None = None,
        progress: ProgressReporter | None = None,
    ) -> list[Path]:
        progress = progress or NullProgressReporter()
        progress.stage("Écriture des rapports...")

        output_dir.mkdir(parents=True, exist_ok=True)

        written_files: list[Path] = []

        for format_name in formats:
            normalized_format = format_name.lower().strip()

            generator = self.report_generators.get(normalized_format)

            if generator is None:
                available_formats = ", ".join(
                    sorted(self.report_generators)
                )
                raise ValueError(f"Unsupported format: {format_name}. Available formats: {available_formats}")
            content = generator.generate_report(audit_result)
            extension = getattr(generator, "extension", normalized_format)
            output_file = output_dir / f"report.{extension}"
            output_file.write_text(content, encoding="utf-8")
            written_files.append(output_file)

        return written_files