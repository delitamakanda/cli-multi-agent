from orchestrator.domain.models import AuditResult

class MarkdownReportGenerator:
    extension = "md"

    def generate_report(self, report_data: AuditResult) -> str:
        context = report_data.repository_context
        stack = report_data.stack

        languages = ", ".join(sorted(stack.languages)) or "N/A"
        frameworks = ", ".join(sorted(stack.frameworks)) or "None"
        tools = ", ".join(sorted(stack.tools)) or "None"

        sections = [
            f"# Report d'audit - {context.name}\n",
            "",
            "## Résumé du dépôt",
            "",
            f"- **Source du dépôt**: {context.source}",
            f"- **Langages détectés**: {languages}",
            f"- **Frameworks détectés**: {frameworks}",
            f"- **Outils détectés**: {tools}",
            f"- **Monorepo**: {'Oui' if stack.is_monorepo else 'Non'}",
            "",
            "## Rapport final",
            "",
            report_data.final_report.strip(),
        ]

        if report_data.roadmap:
            sections.extend([
                "",
                "## Feuille de route",
                "",
                report_data.roadmap.strip(),
            ])

        return "\n".join(sections).strip() + "\n"