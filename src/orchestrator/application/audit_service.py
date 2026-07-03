from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

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

    def analyze(self, repository_path: Path, generate_roadmap: bool = True) -> AuditResult:
        stack = self.stack_detector.detect(repository_path)

        repository_context = self.scanner.scan(repository_path, stack)

        plugins = self.plugin_registry.resolve(repository_context)

        agents = self.agent_registry.resolve(repository_context, plugins)


        reports = self._run_agents(agents, repository_context, plugins)

        final_report = self.orchestrator.synthesize(repository_context, reports)

        roadmap = None

        if generate_roadmap:
            roadmap = self.product_owner.generate_roadmap(final_report, repository_context)

        return AuditResult(
            stack=stack,
            repository_context=repository_context,
            final_report=final_report,
            roadmap=roadmap,
        )
    
    def _run_agents(self, agents, repository_context, plugins):
        reports: dict[str, str] = {}

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
                except Exception as e:
                    reports[agent_name] = f"Error: {str(e)}"

        return reports
    
    def write_reports(
        self,
        audit_result: AuditResult,
        output_dir: Path,
        formats: list[str] | None = None,
    ) -> list[Path]:
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