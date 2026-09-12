🛡️ SENTINEL v2.0

## Autonomous Digital Forensic Investigation Operating System
<div align="center">
  <img src=https://github.com/0dayjake/sentinel-ir/raw/main/sentinel.png alt="The Sentinel Banner" width="100%">
</div>

<br>
> **FIND EVIL. VERIFY EVERYTHING. TRUST EVIDENCE.**

Built in silence, Roar like a Lion!

---

## Overview

SENTINEL v2.0 is an autonomous Digital Forensics and Incident Response (DFIR) platform that independently investigates forensic evidence, correlates intelligence across multiple sources, validates findings through evidence-driven consensus, and generates executive-ready forensic reports.

Unlike traditional DFIR tools that require continuous analyst interaction, SENTINEL performs complete forensic investigations while maintaining explainability, confidence scoring, and a full forensic audit trail.

Its objective is simple:

**Turn forensic evidence into actionable intelligence with minimal analyst intervention.**

---

# Core Capabilities

- Autonomous Digital Forensic Investigation
- Memory Forensics Analysis
- Disk Artifact Analysis
- Multi-Source Evidence Correlation
- Indicator of Compromise (IOC) Extraction
- MITRE ATT&CK Mapping
- Threat Attribution
- Attack Timeline Reconstruction
- Evidence Validation
- Confidence Scoring
- Anti-Hallucination Reasoning
- Executive PDF Reporting
- Complete Investigation Audit Trail

---

# What SENTINEL Does

Given a forensic memory image or disk image, SENTINEL automatically:

- Performs forensic triage
- Profiles the operating system
- Extracts Indicators of Compromise (IOCs)
- Identifies persistence mechanisms
- Detects malware artifacts
- Maps attacker behavior to MITRE ATT&CK
- Correlates infrastructure and behavioral evidence
- Attributes likely threat actors
- Validates every finding through evidence consensus
- Produces executive-ready investigation reports

---

# Investigation Pipeline

```text
          Forensic Evidence
      (Memory / Disk Images)
                 │
                 ▼
      Memory & Artifact Analysis
                 │
                 ▼
          IOC Extraction Engine
                 │
                 ▼
      Threat Attribution Engine
                 │
                 ▼
       Evidence Correlation Engine
                 │
                 ▼
        Evidence Validation Layer
                 │
                 ▼
          Consensus Engine
                 │
                 ▼
 Executive Report • Timeline
 MITRE ATT&CK • Confidence Score
```

---

# Investigation Workflow

| Phase | Description |
|--------|-------------|
| Evidence Triage | Hash verification, OS identification, forensic profiling |
| Artifact Analysis | Registry, persistence, malware, filesystem analysis |
| Memory Analysis | Processes, DLLs, injected code, network artifacts |
| IOC Correlation | Cross-reference forensic artifacts |
| Threat Attribution | Malware, infrastructure, ATT&CK mapping |
| Evidence Validation | Challenge every finding using supporting evidence |
| Consensus Engine | Resolve contradictions and calculate confidence |
| Reporting | Generate executive PDF, timeline and forensic audit log |

---

# Example Investigation

### Case

```
SRL-2018 Enterprise Compromise
```

### Investigation Result

| Finding | Result |
|----------|--------|
| Compromise Status | ✅ Confirmed |
| Threat Actor | APT32 (OceanLotus) |
| Confidence | **92%** |

### Evidence

- ✔ Infrastructure Correlation
- ✔ PHP/Wetbot Malware
- ✔ PowerShell Persistence
- ✔ Five Confirmed MITRE ATT&CK Techniques
- ✔ Infrastructure Fingerprint Matching

---

# Security Architecture

SENTINEL preserves forensic evidence by preventing destructive operations before execution.

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

Clone the repository.

```bash
git clone https://github.com/0dayjakee/sentinel-ir.git

cd sentinel-ir
```

Install dependencies.

```bash
pip3 install groq reportlab --break-system-packages
```

Generate your Groq API key.

https://console.groq.com/keys

```bash
export GROQ_API_KEY=YOUR_API_KEY
```

---

# Environment Setup (SIFT Workstation)

## Phase 1 — Download & Install

Download VirtualBox

https://virtualbox.org

Download SIFT Workstation (.OVA)

https://www.sans.org/tools/sift-workstation

A free SANS account is required.

Install VirtualBox and import the downloaded appliance.

---

## Phase 2 — Configure the SIFT VM

Import the appliance.

```
VirtualBox

File

Import Appliance

Select the SIFT .OVA

Next

Finish
```

Configure SSH Port Forwarding.

```
Settings

Network

Adapter 1

Advanced

Port Forwarding
```

Add the following rule.

| Field | Value |
|--------|-------|
| Name | SSH |
| Protocol | TCP |
| Host IP | 127.0.0.1 |
| Host Port | 2222 |
| Guest IP | 10.0.2.15 |
| Guest Port | 22 |

Start the VM.

Default credentials

```
Username: sansforensics

Password: forensics
```

Enable SSH.

```bash
sudo systemctl enable ssh

sudo systemctl start ssh
```

---

## Phase 3 — Connect from Windows

```powershell
ssh -p 2222 sansforensics@127.0.0.1
```

Password

```
forensics
```

---

## Phase 4 — Install Dependencies

```bash
pip3 install groq reportlab --break-system-packages
```

---

## Phase 5 — Download the Sample Case

Download the forensic memory image.

https://sansorg.egnyte.com/fl/HhH7crTYT4JK

File

```
base-dc-memory.7z
```

Transfer to the SIFT VM.

```powershell
scp -P 2222 "C:\Users\ADMIN\Downloads\base-dc-memory.7z" sansforensics@127.0.0.1:~/
```

Extract.

```bash
7z x base-dc-memory.7z
```

---

## Phase 6 — Transfer SENTINEL

```powershell
scp -P 2222 "C:\Users\ADMIN\Downloads\sentinel_v2.py" sansforensics@127.0.0.1:~/
```

---

## Phase 7 — Run an Investigation

```bash
export GROQ_API_KEY=YOUR_API_KEY

python3 ~/sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
```

---

# Quick Start

Run an autonomous investigation using a single command.

```bash
python3 sentinel_v2.py /path/to/memory.img CASE-001
```

Example

```bash
python3 ~/sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
```

---

# Generated Output

```
cases/

└── CASE-001/

    ├── sentinel_report.json

    ├── sentinel_audit.log

    └── sentinel_v2_executive_report.pdf
```

| Artifact | Description |
|----------|-------------|
| sentinel_report.json | Structured forensic findings |
| sentinel_audit.log | Complete forensic audit trail |
| sentinel_v2_executive_report.pdf | Executive-ready investigation report |

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

Traditional DFIR platforms help analysts investigate.

SENTINEL performs the investigation.

It autonomously analyzes forensic evidence, correlates artifacts across multiple intelligence sources, validates conclusions using evidence-driven reasoning, reconstructs attacker activity, maps behavior to the MITRE ATT&CK framework, and generates explainable executive reports supported by a complete forensic audit trail.

Every finding is evidence-backed.

Every conclusion is validated.

Every investigation is explainable.

---

# Disclaimer

SENTINEL is intended exclusively for authorized digital forensic investigations, incident response, malware analysis, and cybersecurity research.

Users are responsible for ensuring they have appropriate authorization before analyzing digital evidence.

---


Created by

**Rofer Jhayke Sales**
