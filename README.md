# SENTINEL — Multi-Source Autonomous IR Correlation Agent
### FIND EVIL! Hackathon 2026 | SANS Institute

> Stop asking one analyst. SENTINEL deploys history's most powerful forensic toolkit — automatically.

---

## What It Does

SENTINEL is an autonomous DFIR agent that analyzes forensic evidence across **multiple data sources simultaneously** — disk images, memory captures — and correlates findings to reconstruct the full attack timeline.

Unlike single-source tools, SENTINEL:
- **Correlates disk + memory** — catches discrepancies that single-source analysis misses
- **Self-corrects in real time** — flags hallucinations and revises claims based on evidence
- **Produces full audit trails** — every finding is traceable to a specific tool execution
- **Enforces architectural guardrails** — destructive commands are blocked at the code level, not the prompt level

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                SENTINEL AGENT                   │
│         (Claude claude-opus-4-5 + Tools)              │
└──────────────────┬──────────────────────────────┘
                   │
    ┌──────────────┼──────────────────┐
    ▼              ▼                  ▼
┌────────┐  ┌──────────┐  ┌────────────────────┐
│ DISK   │  │ MEMORY   │  │ CORRELATION ENGINE │
│ Layer  │  │ Layer    │  │                    │
│        │  │          │  │  Cross-reference   │
│ ewfmnt │  │ vol3     │  │  disk vs memory    │
│ fls    │  │ pslist   │  │  Flag discrepancy  │
│ log2tl │  │ netscan  │  │  self_correct()    │
│ rip.pl │  │ malfind  │  │                    │
└────────┘  └──────────┘  └────────────────────┘
```

## Analysis Phases

| Phase | Description | Tools Used |
|-------|-------------|-----------|
| 1. TRIAGE | Hash evidence, identify OS, time range | sha256, fls |
| 2. DISK | Mount E01, list files, check persistence | ewfmount, fls, regripper |
| 3. MEMORY | Process list, network, injected code | volatility3 |
| 4. CORRELATION | Cross-reference disk+memory | Internal logic |
| 5. SELF-CORRECTION | Audit every claim | self_correct() |
| 6. REPORT | Timeline, TTPs, remediation | JSON report |

## Security Guardrails

All guardrails are **architectural** — enforced in code, not prompts:

```python
BLOCKED = ['rm ', 'dd ', 'shred', 'mkfs', 'wget ', 'curl ', '> /dev', 'chmod 777']
```

The MCP tool layer physically cannot execute destructive operations.

---

## Installation

```bash
# On SIFT Workstation
git clone https://github.com/YOUR_USERNAME/sentinel-ir.git
cd sentinel-ir
bash install.sh
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
# Basic usage
python3 sentinel.py /cases/evidence/disk.E01 /cases/evidence/memory.raw CASE-001

# With custom case ID
python3 sentinel.py base-dc-cdrive.E01 base-dc-memory.raw SRL-2018-DC
```

## Output

```
/cases/CASE-001/
├── sentinel_report.json    # Structured findings + audit trail
└── sentinel_audit.log      # Every tool call logged
```

## Sample Finding

```json
{
  "id": "F001",
  "type": "persistence",
  "description": "CONFIRMED: Malicious DLL found in HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run via regripper output. Cross-referenced with memory: process loaded at same timestamp.",
  "evidence_source": "run_regripper(SYSTEM hive) + run_volatility(windows.handles)",
  "confidence": "high",
  "artifact_timestamp": "2018-09-07T02:34:11Z"
}
```

---

## License

MIT License — Built for the FIND EVIL! Hackathon 2026
