#!/usr/bin/env python3
"""
SENTINEL - Multi-Source Autonomous IR Correlation Agent
FIND EVIL! Hackathon 2026 | SANS Institute
Author: Jhayke Sales
"""

import os
import json
import subprocess
import logging
import hashlib
import datetime
from pathlib import Path
import anthropic

# ============================================================
# AUDIT LOGGING - Every action is traceable
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('sentinel_audit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SENTINEL')

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ============================================================
# FORENSIC TOOL DEFINITIONS
# ============================================================
TOOLS = [
    {
        "name": "run_volatility",
        "description": "Run a Volatility 3 plugin against a memory image",
        "input_schema": {
            "type": "object",
            "properties": {
                "memory_path": {"type": "string", "description": "Path to memory dump"},
                "plugin": {"type": "string", "description": "Plugin e.g. windows.pslist, windows.netscan, windows.malfind, windows.cmdline"},
                "args": {"type": "string", "description": "Extra args", "default": ""}
            },
            "required": ["memory_path", "plugin"]
        }
    },
    {
        "name": "mount_e01",
        "description": "Mount E01 forensic disk image using ewfmount",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string"},
                "mount_point": {"type": "string"}
            },
            "required": ["image_path", "mount_point"]
        }
    },
    {
        "name": "run_fls",
        "description": "List files in a disk image using fls (The Sleuth Kit) — includes deleted files",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string"},
                "recursive": {"type": "boolean", "default": False},
                "deleted_only": {"type": "boolean", "default": False}
            },
            "required": ["image_path"]
        }
    },
    {
        "name": "run_strings",
        "description": "Extract strings from a file, optionally filtered by grep pattern",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "min_length": {"type": "integer", "default": 6},
                "grep_pattern": {"type": "string", "default": ""}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "calculate_hash",
        "description": "Calculate SHA256 hash of evidence file for integrity verification",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "algorithm": {"type": "string", "default": "sha256"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "search_iocs",
        "description": "Search for IOCs (IPs, domains, hashes, registry keys) in a file or directory",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "pattern": {"type": "string"},
                "context_lines": {"type": "integer", "default": 2}
            },
            "required": ["path", "pattern"]
        }
    },
    {
        "name": "run_regripper",
        "description": "Run RegRipper against a Windows registry hive",
        "input_schema": {
            "type": "object",
            "properties": {
                "hive_path": {"type": "string"},
                "plugin": {"type": "string", "description": "Plugin name or 'all'"}
            },
            "required": ["hive_path", "plugin"]
        }
    },
    {
        "name": "write_finding",
        "description": "Record a confirmed forensic finding to the audit trail",
        "input_schema": {
            "type": "object",
            "properties": {
                "finding_type": {
                    "type": "string",
                    "description": "One of: initial_access, lateral_movement, persistence, c2_communication, data_exfiltration, confirmed_ioc"
                },
                "description": {"type": "string"},
                "evidence_source": {"type": "string", "description": "Exact tool + file that produced this evidence"},
                "confidence": {"type": "string", "description": "high | medium | low"},
                "artifact_timestamp": {"type": "string", "default": ""}
            },
            "required": ["finding_type", "description", "evidence_source", "confidence"]
        }
    },
    {
        "name": "self_correct",
        "description": "Flag an incorrect claim and record the corrected analysis",
        "input_schema": {
            "type": "object",
            "properties": {
                "original_claim": {"type": "string"},
                "correction": {"type": "string"},
                "evidence": {"type": "string"}
            },
            "required": ["original_claim", "correction", "evidence"]
        }
    }
]

# ============================================================
# GUARDRAILS - Architectural, not prompt-based
# ============================================================
BLOCKED = ['rm ', 'dd ', 'shred', 'mkfs', 'wget ', 'curl ', '> /dev', 'chmod 777', ':(){']

findings = []
audit_trail = []
corrections = []


def safe_run(cmd_parts):
    cmd_str = ' '.join(str(c) for c in cmd_parts)
    for blocked in BLOCKED:
        if blocked in cmd_str:
            return f"BLOCKED: Forbidden operation '{blocked}'"
    try:
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=180)
        output = result.stdout or result.stderr
        return output[:6000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "ERROR: Timed out"
    except Exception as e:
        return f"ERROR: {e}"


def log_call(tool, inputs, output, ok):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tool": tool,
        "inputs": inputs,
        "output_sha256": hashlib.sha256(str(output).encode()).hexdigest()[:12],
        "output_preview": str(output)[:300],
        "success": ok
    }
    audit_trail.append(entry)
    logger.info(f"TOOL={tool} OK={ok} IN={json.dumps(inputs)[:120]}")


# ============================================================
# TOOL IMPLEMENTATIONS
# ============================================================
def t_run_volatility(memory_path, plugin, args=""):
    cmd = ['vol', '-f', memory_path, plugin]
    if args:
        cmd += args.split()
    return safe_run(cmd)


def t_mount_e01(image_path, mount_point):
    Path(mount_point).mkdir(parents=True, exist_ok=True)
    return safe_run(['ewfmount', image_path, mount_point])


def t_run_fls(image_path, recursive=False, deleted_only=False):
    cmd = ['fls']
    if recursive:
        cmd.append('-r')
    if deleted_only:
        cmd.append('-d')
    cmd.append(image_path)
    return safe_run(cmd)


def t_run_strings(file_path, min_length=6, grep_pattern=""):
    if grep_pattern:
        return safe_run(['bash', '-c', f'strings -n {min_length} "{file_path}" | grep -iE "{grep_pattern}" | head -100'])
    return safe_run(['strings', '-n', str(min_length), file_path])


def t_calculate_hash(file_path, algorithm="sha256"):
    try:
        h = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return f"{algorithm.upper()}: {h.hexdigest()}"
    except Exception as e:
        return f"ERROR: {e}"


def t_search_iocs(path, pattern, context_lines=2):
    return safe_run(['grep', '-r', '-i', f'-C{context_lines}', '--include=*', pattern, path])


def t_run_regripper(hive_path, plugin):
    return safe_run(['rip.pl', '-r', hive_path, '-p', plugin])


def t_write_finding(finding_type, description, evidence_source, confidence, artifact_timestamp=""):
    f = {
        "id": f"F{len(findings)+1:03d}",
        "logged_at": datetime.datetime.now().isoformat(),
        "artifact_timestamp": artifact_timestamp,
        "type": finding_type,
        "description": description,
        "evidence_source": evidence_source,
        "confidence": confidence
    }
    findings.append(f)
    logger.info(f"FINDING [{f['id']}] [{confidence.upper()}] {finding_type}: {description[:100]}")
    return f"Recorded finding {f['id']}"


def t_self_correct(original_claim, correction, evidence):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "original": original_claim,
        "correction": correction,
        "evidence": evidence
    }
    corrections.append(entry)
    logger.warning(f"CORRECTION #{len(corrections)}: {original_claim[:60]} → {correction[:60]}")
    return f"Self-correction #{len(corrections)} recorded"


def dispatch(tool_name, tool_input):
    try:
        if tool_name == "run_volatility":
            out = t_run_volatility(tool_input['memory_path'], tool_input['plugin'], tool_input.get('args', ''))
        elif tool_name == "mount_e01":
            out = t_mount_e01(tool_input['image_path'], tool_input['mount_point'])
        elif tool_name == "run_fls":
            out = t_run_fls(tool_input['image_path'], tool_input.get('recursive', False), tool_input.get('deleted_only', False))
        elif tool_name == "run_strings":
            out = t_run_strings(tool_input['file_path'], tool_input.get('min_length', 6), tool_input.get('grep_pattern', ''))
        elif tool_name == "calculate_hash":
            out = t_calculate_hash(tool_input['file_path'], tool_input.get('algorithm', 'sha256'))
        elif tool_name == "search_iocs":
            out = t_search_iocs(tool_input['path'], tool_input['pattern'], tool_input.get('context_lines', 2))
        elif tool_name == "run_regripper":
            out = t_run_regripper(tool_input['hive_path'], tool_input['plugin'])
        elif tool_name == "write_finding":
            out = t_write_finding(
                tool_input['finding_type'], tool_input['description'],
                tool_input['evidence_source'], tool_input['confidence'],
                tool_input.get('artifact_timestamp', '')
            )
        elif tool_name == "self_correct":
            out = t_self_correct(tool_input['original_claim'], tool_input['correction'], tool_input['evidence'])
        else:
            out = f"Unknown tool: {tool_name}"
        log_call(tool_name, tool_input, out, True)
        return out
    except Exception as e:
        log_call(tool_name, tool_input, str(e), False)
        return f"ERROR: {e}"


# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM = """You are SENTINEL, an autonomous DFIR agent on the SANS SIFT Workstation.

## Mission
Analyze forensic evidence to identify: initial access, lateral movement, persistence, C2, and exfiltration.

## Analysis Phases (execute in order)
1. TRIAGE — Hash evidence files, identify OS, establish time range, form hypothesis
2. DISK ANALYSIS — Mount E01, list files (including deleted), check persistence locations (Run keys, Startup, Services, Scheduled Tasks)
3. MEMORY ANALYSIS — Run Volatility: pslist, netscan, malfind, cmdline, handles
4. CROSS-SOURCE CORRELATION — Compare disk vs memory. Flag discrepancies with self_correct()
5. SELF-CORRECTION — Audit every claim. Use self_correct() for any unsupported assertion
6. FINAL REPORT — Timeline of compromise, TTPs (MITRE ATT&CK), recommended remediation

## Rules
- Call write_finding() for EVERY confirmed artifact — cite exact tool + file
- Call self_correct() when disk and memory findings contradict each other
- Label confidence: high (directly in tool output), medium (strong inference), low (hypothesis)
- Never claim a finding you cannot trace to a specific tool execution
- Distinguish CONFIRMED vs INFERRED in every finding description"""


# ============================================================
# MAIN AGENT LOOP
# ============================================================
def run_sentinel(disk_path, memory_path, case_name="CASE-001"):
    banner = f"""
╔══════════════════════════════════════════════╗
║  SENTINEL — Autonomous IR Agent              ║
║  FIND EVIL! Hackathon 2026 | SANS Institute  ║
╠══════════════════════════════════════════════╣
║  Case   : {case_name:<34} ║
║  Disk   : {Path(disk_path).name:<34} ║
║  Memory : {Path(memory_path).name:<34} ║
╚══════════════════════════════════════════════╝"""
    print(banner)
    logger.info(f"SENTINEL START | Case={case_name} | Disk={disk_path} | Memory={memory_path}")

    messages = [{
        "role": "user",
        "content": f"""Begin autonomous incident response.

Case ID: {case_name}
Evidence:
  - Disk Image : {disk_path}
  - Memory Dump: {memory_path}

Execute all 6 phases. Start with TRIAGE — hash both files, mount the disk, list the top-level directory.
Use self_correct() whenever you find contradictions between disk and memory.
After Phase 6, provide a complete executive summary with MITRE ATT&CK TTPs."""
    }]

    iteration = 0
    while iteration < 60:
        iteration += 1
        logger.info(f"Iteration {iteration}")

        resp = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages
        )

        asst_content = []
        tool_results = []

        for block in resp.content:
            asst_content.append(block)
            if block.type == "text" and block.text.strip():
                print(f"\n[SENTINEL] {block.text}")
            elif block.type == "tool_use":
                print(f"\n  ⚙ {block.name}({json.dumps(block.input)[:100]})")
                result = dispatch(block.name, block.input)
                print(f"  ↳ {str(result)[:250]}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        messages.append({"role": "assistant", "content": asst_content})

        if resp.stop_reason == "end_turn":
            break
        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    save_report(case_name)


def save_report(case_name):
    case_dir = Path(f"/cases/{case_name}")
    case_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "case": case_name,
        "generated_at": datetime.datetime.now().isoformat(),
        "summary": {
            "total_findings": len(findings),
            "high_confidence": sum(1 for f in findings if f['confidence'] == 'high'),
            "medium_confidence": sum(1 for f in findings if f['confidence'] == 'medium'),
            "low_confidence": sum(1 for f in findings if f['confidence'] == 'low'),
            "self_corrections": len(corrections),
            "tool_executions": len(audit_trail)
        },
        "findings": findings,
        "self_corrections": corrections,
        "audit_trail": audit_trail
    }

    report_path = case_dir / "sentinel_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"""
╔══════════════════════════════════════════════╗
║  SENTINEL COMPLETE                           ║
╠══════════════════════════════════════════════╣
║  Total Findings   : {report['summary']['total_findings']:<25}║
║  High Confidence  : {report['summary']['high_confidence']:<25}║
║  Self-Corrections : {report['summary']['self_corrections']:<25}║
║  Tool Executions  : {report['summary']['tool_executions']:<25}║
║  Report           : {str(report_path):<25}║
╚══════════════════════════════════════════════╝""")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 sentinel.py <disk.E01> <memory.raw> [CASE-ID]")
        sys.exit(1)
    run_sentinel(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "CASE-001")
