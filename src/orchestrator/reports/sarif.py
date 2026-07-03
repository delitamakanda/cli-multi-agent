import json
class SarifReportGenerator:
    def generate_report(self, report_data: dict) -> str:
        sarif_report = {
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "MyTool",
                            "version": "1.0.0"
                        }
                    },
                    "results": report_data.get("results", [])
                }
            ]
        }
        return json.dumps(sarif_report, indent=4)