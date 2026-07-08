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
Isang suggestion pa, tol.

Palitan mo yung tagline na:

FIND EVIL.

ng mas astig at mas professional tulad ng:

Hunt Threats. Validate Evidence. Reveal the Truth.
Every Artifact Tells a Story. SENTINEL Finds the Truth.
Evidence Never Lies.
Autonomous DFIR. Evidence First.
Investigate Faster. Verify Smarter.
Where Evidence Becomes Intelligence.

Mas "cybersecurity conference" ang dating kaysa "movie hacker," at mas kapani-paniwala sa recruiters at judges.

tol ikaw na mag ayos lahat

Oo tol. Inayos ko na ang buong README para ang dating ay parang open-source project ng isang professional DFIR framework. Tinanggal ko yung paulit-ulit na wording, inayos ang hierarchy, ginawang mas GitHub-friendly, at mas "enterprise / SANS" ang dating kaysa "AI chatbot".

Pwede mo itong gamitin bilang README.md.

# 🛡️ SENTINEL v2.0

## Autonomous Digital Forensic Investigation Operating System

> **FIND EVIL. VERIFY EVERYTHING. TRUST EVIDENCE.**

Built for the **SANS Institute – FIND EVIL Hackathon 2026**

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

## Built for

**SANS Institute — FIND EVIL Hackathon 2026**

Created by **Rofer Jhayke Sales**
