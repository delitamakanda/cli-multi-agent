import json

class JSONReportGenerator:
    def generate_report(self, report_data: dict) -> str:
        return json.dumps(report_data, indent=4)

