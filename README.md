🛡️ SENTINEL v2.0

### Autonomous Digital Forensic Investigation Operating System

> **FIND EVIL. VERIFY EVERYTHING. TRUST EVIDENCE.**

Built for **SANS Institute – FIND EVIL Hackathon 2026**

---

## Overview

SENTINEL v2.0 is an autonomous Digital Forensics and Incident Response (DFIR) platform designed to conduct evidence-driven investigations with minimal analyst interaction.

Instead of acting as an AI assistant, SENTINEL independently analyzes forensic artifacts, correlates intelligence from multiple sources, validates every conclusion, and produces executive-ready investigation reports backed by verifiable evidence.

Every finding is challenged, correlated, scored, and documented before reaching a final conclusion.

---

# Core Capabilities

✔ Autonomous Digital Forensic Investigation

✔ Memory Forensics Analysis

✔ Disk Artifact Analysis

✔ Multi-Source Evidence Correlation

✔ IOC Extraction

✔ MITRE ATT&CK Mapping

✔ Threat Attribution

✔ Attack Timeline Reconstruction

✔ Confidence Scoring

✔ Evidence Validation Engine

✔ Anti-Hallucination Reasoning

✔ Executive PDF Reporting

✔ Complete Investigation Audit Trail

---

# Investigation Pipeline

```
Forensic Evidence
(Disk Image / Memory Dump)
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
Evidence Correlation
           │
           ▼
Validation Engine
           │
           ▼
Consensus Engine
           │
           ▼
Executive Report
MITRE ATT&CK Mapping
Timeline Reconstruction
Confidence Assessment
```

---

# Autonomous Investigation Workflow

| Phase | Description |
|--------|-------------|
| Evidence Triage | Identify operating system, hashes, forensic profile |
| Artifact Analysis | Registry, persistence, malware, filesystem |
| Memory Analysis | Processes, DLLs, injected code, network artifacts |
| IOC Correlation | Cross-reference forensic evidence |
| Threat Attribution | Infrastructure, malware, TTP correlation |
| Validation | Challenge every conclusion against evidence |
| Consensus | Remove contradictions and assign confidence |
| Reporting | Executive PDF, Timeline, MITRE ATT&CK Mapping |

---

# Example Investigation

### Case

```
SRL-2018 Enterprise Compromise
```

### Investigation Result

| Finding | Result |
|---------|--------|
| Compromise | ✅ Confirmed |
| Threat Actor | APT32 (OceanLotus) |
| Confidence | 92% |

### Evidence

- ✔ Infrastructure Correlation
- ✔ PHP/Wetbot Malware
- ✔ PowerShell Persistence
- ✔ Five Confirmed MITRE ATT&CK Techniques
- ✔ Infrastructure Fingerprint Matching

---

# Security by Design

SENTINEL preserves forensic integrity by preventing destructive operations before execution.

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

This prevents accidental evidence modification and maintains forensic integrity throughout the investigation.

---

# Installation

```bash
git clone https://github.com/0dayjakee/sentinel-ir.git

cd sentinel-ir

pip3 install groq reportlab --break-system-packages
```

Generate your Groq API key

https://console.groq.com/keys

```bash
export GROQ_API_KEY=YOUR_API_KEY
```

---

# SIFT Workstation Setup

## Phase 1 — Download

Download VirtualBox

https://virtualbox.org

Download SIFT Workstation (.OVA)

https://www.sans.org/tools/sift-workstation

---

## Phase 2 — Configure SIFT

Import the appliance

```
File
 └── Import Appliance
```

Configure SSH Port Forwarding

| Field | Value |
|--------|-------|
| Name | SSH |
| Protocol | TCP |
| Host IP | 127.0.0.1 |
| Host Port | 2222 |
| Guest IP | 10.0.2.15 |
| Guest Port | 22 |

Enable SSH

```bash
sudo systemctl enable ssh

sudo systemctl start ssh
```

---

## Phase 3 — Connect

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

## Phase 5 — Download Sample Evidence

Download

https://sansorg.egnyte.com/fl/HhH7crTYT4JK

Transfer

```powershell
scp -P 2222 base-dc-memory.7z sansforensics@127.0.0.1:~/
```

Extract

```bash
7z x base-dc-memory.7z
```

---

## Phase 6 — Transfer SENTINEL

```powershell
scp -P 2222 sentinel_v2.py sansforensics@127.0.0.1:~/
```

---

## Phase 7 — Launch Investigation

```bash
export GROQ_API_KEY=YOUR_API_KEY

python3 ~/sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
```

---

# Quick Start

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

└── CASE-001

    ├── sentinel_report.json

    ├── sentinel_audit.log

    └── sentinel_v2_executive_report.pdf
```

---

# Why SENTINEL?

Traditional DFIR platforms assist investigators.

SENTINEL conducts the investigation.

It autonomously analyzes forensic evidence, correlates intelligence, validates findings, reconstructs attacker behavior, maps techniques to MITRE ATT&CK, and produces explainable investigation reports with a complete audit trail.

Every conclusion is supported by evidence.

Every finding is traceable.

Every report is explainable.
