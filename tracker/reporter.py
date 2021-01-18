import csv
import sys
from datetime import datetime


class Reporter:

    def __init__(self, manager):
        self.manager = manager

    def generate(self, fmt="text"):
        summary = self.manager.get_summary()
        defects = self.manager.list_defects()

        if fmt == "text":
            self._text_report(summary, defects)
        elif fmt == "csv":
            self._csv_report(defects)

    def _text_report(self, summary, defects):
        print("\n" + "=" * 50)
        print(f"  QA DEFECT REPORT — {datetime.now().strftime('%Y-%m-%d')}")
        print("=" * 50)
        print(f"\nTotal Defects: {summary['total']}")

        print("\nBy Status:")
        for status, count in summary["by_status"].items():
            print(f"  {status:<15} {count}")

        print("\nBy Severity:")
        for severity, count in summary["by_severity"].items():
            print(f"  {severity:<15} {count}")

        print("\nBy Module:")
        for module, count in summary["by_module"].items():
            print(f"  {module:<20} {count}")

        open_critical = [d for d in defects if d["severity"] == "critical" and d["status"] == "open"]
        if open_critical:
            print(f"\n⚠  Open Critical Defects ({len(open_critical)}):")
            for d in open_critical:
                print(f"  [{d['id']}] {d['title']} — {d['module']}")
        print()

    def _csv_report(self, defects):
        writer = csv.DictWriter(sys.stdout,
                                fieldnames=["id", "title", "module", "severity", "status", "created_at"])
        writer.writeheader()
        for d in defects:
            writer.writerow({
                "id": d["id"],
                "title": d["title"],
                "module": d["module"],
                "severity": d["severity"],
                "status": d["status"],
                "created_at": d["created_at"]
            })
# reporter
