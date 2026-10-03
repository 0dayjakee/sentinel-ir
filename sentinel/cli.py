from __future__ import annotations

import argparse
import sys

from .case import create_case, load_case


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="SENTINEL evidence-first DFIR platform",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    investigate = sub.add_parser(
        "investigate",
        help="Create a forensic case from evidence",
    )

    investigate.add_argument(
        "evidence",
        help="Path to forensic evidence",
    )

    investigate.add_argument(
        "--case",
        default="CASE-001",
        help="Case identifier",
    )

    triage = sub.add_parser(
        "triage",
        help="Inspect an existing case",
    )

    triage.add_argument(
        "case",
        help="Case identifier",
    )

    verify = sub.add_parser(
        "verify",
        help="Verify case evidence integrity",
    )

    verify.add_argument(
        "case",
        help="Case identifier",
    )

    report = sub.add_parser(
        "report",
        help="Generate a case summary",
    )

    report.add_argument(
        "case",
        help="Case identifier",
    )

    return parser


def cmd_investigate(args) -> int:
    case = create_case(
        case_id=args.case,
        evidence_path=args.evidence,
    )

    print(f"[+] Case created: {case.case_id}")
    print(f"[+] Evidence:    {case.evidence_path}")
    print(f"[+] SHA-256:     {case.evidence_sha256}")

    return 0


def cmd_triage(args) -> int:
    case = load_case(args.case)

    print(f"Case:     {case.case_id}")
    print(f"Evidence: {case.evidence_path}")
    print(f"SHA-256:  {case.evidence_sha256}")
    print(f"Findings: {len(case.findings)}")

    return 0


def cmd_verify(args) -> int:
    from .evidence import sha256_file

    case = load_case(args.case)

    current = sha256_file(case.evidence_path)

    if current != case.evidence_sha256:
        print("[!] EVIDENCE INTEGRITY FAILURE")
        print(f"    Expected: {case.evidence_sha256}")
        print(f"    Current:  {current}")
        return 2

    print("[+] Evidence integrity verified")
    print(f"    SHA-256: {current}")

    return 0


def cmd_report(args) -> int:
    case = load_case(args.case)

    print("=" * 60)
    print("SENTINEL CASE REPORT")
    print("=" * 60)
    print(f"Case:       {case.case_id}")
    print(f"Evidence:   {case.evidence_path}")
    print(f"SHA-256:    {case.evidence_sha256}")
    print(f"Findings:   {len(case.findings)}")
    print(f"Evidence:   {len(case.evidence)}")

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "investigate":
            return cmd_investigate(args)

        if args.command == "triage":
            return cmd_triage(args)

        if args.command == "verify":
            return cmd_verify(args)

        if args.command == "report":
            return cmd_report(args)

        parser.print_help()
        return 1

    except Exception as exc:  # noqa: BLE001 - top-level CLI boundary
        print(f"[!] SENTINEL ERROR: {exc}", file=sys.stderr)
        return 1
