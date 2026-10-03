#!/usr/bin/env python3
import datetime
import hashlib
import json
import logging
import os
from pathlib import Path

import google.generativeai as genai

from sentinel.safe_exec import safe_run
from sentinel.safe_tools import grep_tree, strings_grep

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', handlers=[logging.FileHandler('sentinel_audit.log'), logging.StreamHandler()])
logger = logging.getLogger('SENTINEL')

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

findings = []
audit_trail = []
corrections = []

def run_volatility(memory_path: str, plugin: str, args: str = "") -> str:
    """Run a Volatility 3 plugin against a memory image"""
    cmd = ['vol', '-f', memory_path, plugin]
    if args: cmd += args.split()
    out = safe_run(cmd)
    logger.info("vol argv=%s -> %s", cmd, out[:80].replace("\n", " "))
    if out.startswith("BLOCKED"):
        logger.warning("vol call BLOCKED argv=%s", cmd)
    return out

def run_strings(file_path: str, grep_pattern: str = "") -> str:
    """Extract strings from a file, optionally filtered"""
    if grep_pattern:
        return strings_grep(file_path, grep_pattern)
    return strings_grep(file_path)

def calculate_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate hash of evidence file"""
    try:
        h = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return f"{algorithm.upper()}: {h.hexdigest()}"
    except (OSError, ValueError) as e:
        return f"ERROR: {e}"

def search_iocs(path: str, pattern: str) -> str:
    """Search for IOCs in a file"""
    return grep_tree(pattern, path)

def write_finding(finding_type: str, description: str, evidence_source: str, confidence: str, artifact_timestamp: str = "") -> str:
    """Record a confirmed forensic finding"""
    f = {"id": f"F{len(findings)+1:03d}", "logged_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "artifact_timestamp": artifact_timestamp, "type": finding_type, "description": description, "evidence_source": evidence_source, "confidence": confidence}
    findings.append(f)
    logger.info(f"FINDING [{f['id']}] [{confidence.upper()}] {finding_type}: {description[:80]}")
    return f"Recorded {f['id']}"

def self_correct(original_claim: str, correction: str, evidence: str) -> str:
    """Flag an incorrect claim and record correction"""
    corrections.append({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "original": original_claim, "correction": correction, "evidence": evidence})
    logger.warning(f"CORRECTION #{len(corrections)}: {original_claim[:60]}")
    return f"Correction #{len(corrections)} recorded"

SYSTEM = """You are SENTINEL, an autonomous DFIR agent on the SANS SIFT Workstation.
Analyze forensic evidence across 6 phases:
1. TRIAGE - Hash evidence, identify OS, time range
2. DISK - Run strings on memory, search for persistence IOCs
3. MEMORY - Run Volatility plugins: windows.pslist, windows.netscan, windows.malfind, windows.cmdline
4. CORRELATION - Cross-reference findings, flag discrepancies
5. SELF-CORRECTION - Use self_correct() for any unsupported claim
6. REPORT - Timeline, MITRE ATT&CK TTPs, remediation

Rules:
- Call write_finding() for EVERY confirmed artifact
- Call self_correct() when findings contradict each other
- Label confidence: high/medium/low
- Distinguish CONFIRMED vs INFERRED"""

def run_sentinel(memory_path, case_name="CASE-001"):
    print(f"""
╔══════════════════════════════════════════════╗
║  SENTINEL — Autonomous IR Agent              ║
║  FIND EVIL! Hackathon 2026 | SANS Institute  ║
╠══════════════════════════════════════════════╣
║  Case   : {case_name:<34} ║
║  Memory : {Path(memory_path).name:<34} ║
╚══════════════════════════════════════════════╝""")

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM,
        tools=[run_volatility, run_strings, calculate_hash, search_iocs, write_finding, self_correct]
    )

    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = f"""Begin autonomous incident response.
Case: {case_name}
Memory Image: {memory_path}

Start Phase 1: Calculate the SHA256 hash of the memory file.
Then Phase 3: Run Volatility plugins (windows.pslist, windows.netscan, windows.malfind).
Then search for IOCs in the memory file.
Record all findings and self-correct any inconsistencies.
End with a complete executive summary."""

    print("\n[SENTINEL] Starting analysis...\n")
    response = chat.send_message(prompt)
    print(f"\n[SENTINEL REPORT]\n{response.text}")

    case_dir = Path(f"/cases/{case_name}")
    case_dir.mkdir(parents=True, exist_ok=True)
    report = {"case": case_name, "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "summary": {"total_findings": len(findings), "self_corrections": len(corrections)}, "findings": findings, "corrections": corrections, "audit_trail": audit_trail}
    with open(case_dir / "sentinel_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n✅ Report saved: /cases/{case_name}/sentinel_report.json")
    print(f"   Findings: {len(findings)} | Corrections: {len(corrections)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 sentinel_gemini.py <memory.img> [CASE-ID]")
        sys.exit(1)
    run_sentinel(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "CASE-001")
