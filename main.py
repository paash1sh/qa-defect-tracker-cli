#!/usr/bin/env python3
"""
qa-defect-tracker-cli
A lightweight command-line tool for logging, updating, and tracking QA defects.
"""

import argparse
import sys
from tracker.defect_manager import DefectManager
from tracker.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(
        description="QA Defect Tracker - Log and manage test defects from the CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    # log command
    log_parser = subparsers.add_parser("log", help="Log a new defect")
    log_parser.add_argument("--title", required=True, help="Defect title")
    log_parser.add_argument("--module", required=True, help="Module affected")
    log_parser.add_argument("--severity", choices=["low", "medium", "high", "critical"],
                            default="medium", help="Defect severity")
    log_parser.add_argument("--steps", help="Steps to reproduce")
    log_parser.add_argument("--expected", help="Expected result")
    log_parser.add_argument("--actual", help="Actual result")

    # update command
    update_parser = subparsers.add_parser("update", help="Update defect status")
    update_parser.add_argument("--id", required=True, help="Defect ID")
    update_parser.add_argument("--status", required=True,
                               choices=["open", "in_progress", "resolved", "closed", "reopened"],
                               help="New status")
    update_parser.add_argument("--comment", help="Comment on the status change")

    # list command
    list_parser = subparsers.add_parser("list", help="List defects")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--severity", help="Filter by severity")
    list_parser.add_argument("--module", help="Filter by module")

    # show command
    show_parser = subparsers.add_parser("show", help="Show defect details")
    show_parser.add_argument("--id", required=True, help="Defect ID")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate defect summary report")
    report_parser.add_argument("--format", choices=["text", "csv"], default="text",
                               help="Report output format")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    manager = DefectManager()

    if args.command == "log":
        defect_id = manager.log_defect(
            title=args.title,
            module=args.module,
            severity=args.severity,
            steps=args.steps,
            expected=args.expected,
            actual=args.actual
        )
        print(f"[OK] Defect logged. ID: {defect_id}")

    elif args.command == "update":
        manager.update_status(args.id, args.status, args.comment)
        print(f"[OK] Defect {args.id} updated to '{args.status}'")

    elif args.command == "list":
        defects = manager.list_defects(
            status=args.status,
            severity=args.severity,
            module=args.module
        )
        if not defects:
            print("No defects found matching criteria.")
        else:
            print(f"\n{'ID':<10} {'Title':<35} {'Module':<15} {'Severity':<10} {'Status'}")
            print("-" * 85)
            for d in defects:
                print(f"{d['id']:<10} {d['title'][:33]:<35} {d['module']:<15} {d['severity']:<10} {d['status']}")

    elif args.command == "show":
        defect = manager.get_defect(args.id)
        if defect:
            print(f"\nDefect: {defect['id']}")
            print(f"Title:    {defect['title']}")
            print(f"Module:   {defect['module']}")
            print(f"Severity: {defect['severity']}")
            print(f"Status:   {defect['status']}")
            print(f"Created:  {defect['created_at']}")
            if defect.get("steps"):
                print(f"Steps:    {defect['steps']}")
            if defect.get("expected"):
                print(f"Expected: {defect['expected']}")
            if defect.get("actual"):
                print(f"Actual:   {defect['actual']}")
            if defect.get("history"):
                print("\nHistory:")
                for h in defect["history"]:
                    print(f"  [{h['timestamp']}] {h['status']} - {h.get('comment', '')}")
        else:
            print(f"Defect {args.id} not found.")

    elif args.command == "report":
        reporter = Reporter(manager)
        reporter.generate(fmt=args.format)


if __name__ == "__main__":
    main()
# init
