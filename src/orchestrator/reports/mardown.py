
class MarkdownReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_report(self):
        report = "# Report\n\n"
        for section in self.data:
            report += f"## {section['title']}\n\n"
            for item in section['items']:
                report += f"- {item}\n"
            report += "\n"
        return report