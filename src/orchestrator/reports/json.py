import json
from dataclasses import asdict

from orchestrator.domain.models import AuditResult

class JSONReportGenerator:
    extension = "json"

    def generate_report(self, report_data: AuditResult) -> str:
        data = asdict(report_data)

        data['repository_context']['repository_path'] = str(
            report_data.repository_context.repository_path
        )
        for source_file in data['repository_context']['files']:
            source_file['path'] = str(source_file['path'])

        data["stack"]["languages"] = sorted(report_data.stack.languages)
        data["stack"]["frameworks"] = sorted(report_data.stack.frameworks)
        data["stack"]["tools"] = sorted(report_data.stack.tools)
        return json.dumps(data, ensure_ascii=False, indent=4)

