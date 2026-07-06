# SENTINEL v2.0 — Multi-Agent Autonomous IR Operating System
### FIND EVIL! Hackathon 2026 | SANS Institute

> "Sentinel doesn't generate answers — it conducts investigations."

---

## What It Does

SENTINEL v2.0 is a **Multi-Agent Autonomous Incident Response Operating System** that deploys 6 specialized AI investigators to analyze forensic evidence, debate findings, resolve contradictions, and produce an auditable executive report.

**On the real SRL-2018 enterprise compromise:**

| Agent | Role | Finding |
|-------|------|---------|
| SENTINEL | Memory Forensics | 6 high-confidence IOCs confirmed |
| GHOST HUNTER | APT Attribution | APT32/OceanLotus (Vietnam) — 92% |
| ORACLE | Predictive Intel | Credential harvest in 6-12 hours |
| SKEPTIC | Anti-Hallucination | 1 contradiction detected |
| CONSENSUS | Evidence Correlation | Compromise CONFIRMED — CRITICAL |
| REPORTER | Executive Report | PDF + JSON audit trail |

---

## Architecture

```
                    MISSION
                       │
            ┌──────────┴──────────┐
            │    SENTINEL v2.0    │
            │   IR Operating System│
            └──────────┬──────────┘
                       │
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
┌─────────┐      ┌──────────┐     ┌─────────┐
│SENTINEL │      │  GHOST   │     │ ORACLE  │
│ Memory  │      │ HUNTER   │     │Predictive│
│Forensics│      │Attribution│    │  Intel  │
└────┬────┘      └────┬─────┘     └────┬────┘
     │                │                │
     └────────────────┼────────────────┘
                      ▼
               ┌─────────────┐
               │   SKEPTIC   │
               │Devil's Adv. │
               │Anti-Hallucin│
               └──────┬──────┘
                      ▼
               ┌─────────────┐
               │  CONSENSUS  │
               │  Evidence   │
               │ Correlation │
               └──────┬──────┘
                      ▼
               ┌─────────────┐
               │  REPORTER   │
               │  Executive  │
               │PDF + Audit  │
               └─────────────┘
```

---

## Key Features

### 1. Multi-Agent Debate Engine
6 specialized AI agents with distinct roles argue, challenge, and validate each other's findings — not a single AI answering questions.

### 2. Contradiction Detection
SKEPTIC agent challenges every finding. When SENTINEL and SKEPTIC disagree, CONSENSUS spawns resolution and confidence adjusts automatically.

### 3. Confidence Evolution (41% → 95%)
Confidence is never static — each agent adds evidence and the score evolves:
```
Initial          → 41%
+ Memory         → 68%
+ Timeline       → 89%
+ Threat Intel   → 95%
```

### 4. Attack Timeline
```
2018-09-06 02:34  🔴 INITIAL ACCESS — PHP webshell (Wetbot.A)
2018-09-06 03:12  🔴 C2 ESTABLISHED — myvinhlong.com
2018-09-06 03:45  🔴 BACKDOOR — PowerShell/Listrun.A
2018-09-06 04:21  🔴 EXECUTION — Meterpreter via PowerShell
2018-09-06 05:03  🔴 DLL INJECTION — mstd32.dll
2018-09-06 05:47  🔴 ANTI-FORENSICS — rm -f cleanup
```

### 5. MITRE ATT&CK Mapping
```
T1190  Exploit Public-Facing App    ████████████████████ 95%
T1059  PowerShell Execution         ████████████████████ 95%
T1071  C2 via HTTP                  ███████████████████  92%
T1105  Ingress Tool Transfer        ██████████████████   90%
T1055  Process Injection            █████████████████    88%
T1070  File Deletion                █████████████████    85%
```

### 6. Architectural Guardrails
All security guardrails are **enforced in code**, not prompts:
```python
BLOCKED = ['rm ', 'dd ', 'shred', 'mkfs', '> /dev', 'chmod 777']
```

### 7. Executive PDF Report
One-click generation of a structured incident report with findings table, attribution, MITRE mapping, and recommended actions.

### 8. Audit Trail
Every agent action is timestamped and logged — full explainability:
```
[04:05:52] SENTINEL → Scanning memory for malware signatures
[04:05:55] SENTINEL → Analysis complete. Passing to GHOST HUNTER
[04:06:03] SKEPTIC  → CONTRADICTION DETECTED — flagging for CONSENSUS
[04:06:06] CONSENSUS → Final verdict reached
```

---

## GHOST HUNTER — APT Attribution

After SENTINEL finds the evil, GHOST HUNTER identifies WHO did it.

### SRL-2018 Attribution Result
```
🎯 APT32 / OceanLotus (Vietnam) — 92% confidence
   MITRE ATT&CK Group: G-0047
   
   Evidence:
   • C2 domain myvinhlong.com → Vietnamese infrastructure
   • PHP/Wetbot.A → APT32 known toolset
   • T1059.001, T1055, T1071, T1105, T1070.004 → APT32 TTPs
   • False flag assessment → Ruled out
```

---

## ORACLE — Predictive Intelligence

After attribution, ORACLE predicts the attacker's next 5 moves:

```
Move 1: Internal recon via backdoors      → 2-4 hours    (85%)
Move 2: Credential harvesting (LSASS)     → 6-12 hours   (90%)
Move 3: Lateral movement to file servers  → 12-24 hours  (88%)
Move 4: Data exfiltration — slow & low    → 24-48 hours  (80%)
Move 5: Additional backdoors              → 48-72 hours  (82%)
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/0dayjakee/sentinel-ir.git
cd sentinel-ir

# Install dependencies
pip3 install groq reportlab --break-system-packages

# Set API key
export GROQ_API_KEY=your_groq_api_key
```

## Usage

```bash
# Run SENTINEL v2.0 (full multi-agent analysis)
python3 sentinel_v2.py /path/to/memory.img CASE-001

# Run GHOST HUNTER only (APT attribution)
python3 ghost_hunter.py

# Run ORACLE only (predictive intel)
python3 oracle.py
```

## Output

```
/cases/CASE-001/
├── sentinel_v2_executive_report.pdf  # Executive PDF report
├── sentinel_v2_report.json           # Structured findings + audit trail
├── ghost_hunter_report.json          # APT attribution report
└── oracle_report.json                # Predictive threat forecast
```

---

## Evidence Dataset

- **Source:** SANS FIND EVIL Hackathon Case Data
- **File:** SRL-2018 base-dc-memory.img (5GB Windows 10 DC memory dump)
- **Date:** 2018-09-06 22:57 UTC
- **System:** Windows 10 64-bit Domain Controller

---

## License
MIT License — Built for the FIND EVIL! Hackathon 2026
