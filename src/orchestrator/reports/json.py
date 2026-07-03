import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from orchestrator.domain.models import AuditResult

class JSONReportGenerator:
    extension = "json"

    def generate_report(self, report_data: AuditResult) -> str:
        data = self._to_json_compatible(report_data)

        return json.dumps(data, ensure_ascii=False, indent=4)

    def _to_json_compatible(self, obj: Any) -> Any:
        if is_dataclass(obj) and not isinstance(obj, type):
            return {k: self._to_json_compatible(v) for k, v in asdict(obj).items()}
        
        if isinstance(obj, (list, tuple)):
            return [self._to_json_compatible(i) for i in obj]
        
        if isinstance(obj, dict):
            return {k: self._to_json_compatible(v) for k, v in obj.items()}
        
        if isinstance(obj, set):
            return sorted([self._to_json_compatible(i) for i in obj])
        
        if isinstance(obj, Path):
            return str(obj)
        
        return obj
