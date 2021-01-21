import json
import os
import uuid
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "defects.json")


class DefectManager:

    def __init__(self):
        self.data_file = DATA_FILE
        self._ensure_data_file()

    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(self.data_file, "r") as f:
            return json.load(f)

    def _save(self, defects):
        with open(self.data_file, "w") as f:
            json.dump(defects, f, indent=2)

    def log_defect(self, title, module, severity, steps=None, expected=None, actual=None):
        defects = self._load()
        defect_id = "DEF-" + str(len(defects) + 1).zfill(4)
        defect = {
            "id": defect_id,
            "title": title,
            "module": module,
            "severity": severity,
            "status": "open",
            "steps": steps,
            "expected": expected,
            "actual": actual,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "history": [
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "open",
                    "comment": "Defect logged"
                }
            ]
        }
        defects.append(defect)
        self._save(defects)
        return defect_id

    def update_status(self, defect_id, new_status, comment=None):
        defects = self._load()
        for defect in defects:
            if defect["id"] == defect_id:
                defect["status"] = new_status
                defect["history"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": new_status,
                    "comment": comment or ""
                })
                self._save(defects)
                return True
        return False

    def get_defect(self, defect_id):
        defects = self._load()
        for defect in defects:
            if defect["id"] == defect_id:
                return defect
        return None

    def list_defects(self, status=None, severity=None, module=None):
        defects = self._load()
        if status:
            defects = [d for d in defects if d["status"] == status]
        if severity:
            defects = [d for d in defects if d["severity"] == severity]
        if module:
            defects = [d for d in defects if d["module"].lower() == module.lower()]
        return defects

    def get_summary(self):
        defects = self._load()
        summary = {
            "total": len(defects),
            "by_status": {},
            "by_severity": {},
            "by_module": {}
        }
        for d in defects:
            summary["by_status"][d["status"]] = summary["by_status"].get(d["status"], 0) + 1
            summary["by_severity"][d["severity"]] = summary["by_severity"].get(d["severity"], 0) + 1
            summary["by_module"][d["module"]] = summary["by_module"].get(d["module"], 0) + 1
        return summary
# manager
# filter
# history
# empty file fix
