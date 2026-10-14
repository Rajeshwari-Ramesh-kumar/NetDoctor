
import json
from datetime import datetime


def save_report(hostname, results):
    report = {
        "project": "Automated Network and Service Diagnostics",
        "hostname": hostname,
        "generated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "results": results,
        "overall_status": (
            "PASS"
            if all(item["status"] == "PASS" for item in results)
            else "FAIL"
        )
    }

    filename = "diagnostic_report.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nReport saved to:", filename)
    print("Overall Status:", report["overall_status"])
