# SENTINEL v2.0

### Autonomous Digital Forensic Investigation Operating System

**FIND EVIL! Hackathon 2026 | SANS Institute**

---

> Autonomously investigate digital evidence, correlate findings, validate conclusions, and generate executive-ready forensic reports—all from a single command.


---

# What It Does

**SENTINEL v2.0** is an **Autonomous Digital Forensic Investigation Operating System** that independently investigates digital evidence, correlates findings across multiple forensic sources, validates conclusions, and produces explainable, evidence-backed incident reports.

Given forensic evidence such as memory captures or disk images, SENTINEL automatically:

- Performs forensic triage
- Extracts Indicators of Compromise (IOCs)
- Correlates evidence across multiple sources
- Maps attacker behavior to the MITRE ATT&CK framework
- Identifies likely threat actors through infrastructure and behavioral correlation
- Validates findings using evidence-driven consensus
- Generates executive-ready investigation reports

Unlike traditional AI assistants, SENTINEL does not simply answer analyst questions—it conducts the investigation autonomously.

---

# Key Capabilities

- Autonomous digital forensic investigation
- Multi-source evidence correlation
- Memory forensic analysis
- Threat attribution
- MITRE ATT&CK mapping
- Attack timeline reconstruction
- Confidence scoring
- Evidence validation
- Anti-hallucination reasoning
- Executive PDF reporting
- Complete forensic audit trail

---

# Example Investigation

### Case

SRL-2018 Enterprise Compromise

### Investigation Result

```
Compromise Status
✔ CONFIRMED

Threat Actor
APT32 / OceanLotus

Confidence
92%

Evidence

✔ C2 infrastructure correlation
✔ PHP/Wetbot.A malware family
✔ PowerShell persistence
✔ 5 confirmed MITRE ATT&CK techniques
✔ Infrastructure fingerprint matching
```

---

# Investigation Pipeline

```text
Forensic Evidence
(Disk / Memory)
        │
        ▼
┌──────────────────────────────┐
│          SENTINEL            │
│ Memory & Artifact Analysis   │
└──────────────────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Threat Attribution Engine    │
│ Malware • Infrastructure     │
│ MITRE • Behavioral Matching  │
└──────────────────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Predictive Intelligence      │
└──────────────────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Evidence Validation          │
│ Challenge Every Finding      │
└──────────────────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Consensus Engine             │
│ Correlate • Verify • Score   │
└──────────────────────────────┘
              │
              ▼
 Executive Report + Timeline + MITRE ATT&CK
```

---

# Investigation Workflow

| Phase | Description |
|--------|-------------|
| **Evidence Triage** | Hash verification, OS identification, forensic profiling |
| **Artifact Analysis** | Registry, persistence, malware, filesystem analysis |
| **Memory Analysis** | Processes, DLLs, injected code, network artifacts |
| **Evidence Correlation** | Cross-reference all forensic artifacts |
| **Threat Attribution** | Correlate malware, infrastructure, and ATT&CK techniques |
| **Evidence Validation** | Challenge findings and resolve contradictions |
| **Reporting** | Generate timelines, ATT&CK mapping, confidence scores, and executive reports |

---

# Security Architecture

SENTINEL enforces security controls at the application layer.

Potentially destructive operations are blocked before execution rather than relying on prompt instructions.

```python
BLOCKED_COMMANDS = [
    "rm ",
    "dd ",
    "shred",
    "mkfs",
    "wget ",
    "curl ",
    "> /dev",
    "chmod 777"
]
```

This ensures forensic evidence remains immutable throughout the investigation.

---

# Installation

## Clone the repository

```bash
git clone https://github.com/0dayjakee/sentinel-ir.git
cd sentinel-ir
```

## Install dependencies

```bash
pip3 install groq reportlab --break-system-packages
```

## Configure your API key

```bash
export GROQ_API_KEY=your_groq_api_key
```

---

# Quick Start

Run a complete autonomous investigation with a single command.

```bash
python3 sentinel_v2.py /path/to/memory.img CASE-001
```

### Example

```bash
python3 sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
```

During execution, SENTINEL automatically performs:

- Memory forensic analysis
- IOC extraction
- Threat attribution
- Evidence validation
- MITRE ATT&CK mapping
- Confidence scoring
- Executive PDF generation

No additional commands are required.

---

# Generated Output

```text
cases/
└── CASE-001/
    ├── sentinel_report.json
    ├── sentinel_audit.log
    └── sentinel_v2_executive_report.pdf
```

| Artifact | Description |
|----------|-------------|
| **sentinel_report.json** | Structured forensic findings |
| **sentinel_audit.log** | Complete investigation audit trail |
| **sentinel_v2_executive_report.pdf** | Executive-ready forensic report |

---

# Sample Finding

```json
{
  "id": "F001",
  "type": "Persistence",
  "confidence": "95%",
  "description": "Malicious DLL persistence confirmed through registry and memory correlation.",
  "evidence": [
    "Registry Run Key",
    "Volatility Process Scan"
  ],
  "mitre": "T1547.001",
  "timestamp": "2018-09-07T02:34:11Z"
}
```

---

# Why SENTINEL?

Traditional DFIR tools assist investigators.

SENTINEL performs the investigation.

It autonomously analyzes forensic evidence, correlates artifacts across multiple sources, validates every conclusion, attributes attacker activity, and produces explainable, evidence-backed reports with a complete audit trail.

Security teams don't need another AI chatbot.

They need an autonomous investigator.
