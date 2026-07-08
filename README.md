SENTINEL v2.0
Autonomous Digital Forensic Investigation Operating System

FIND EVIL! Hackathon 2026 | SANS Institute

SENTINEL v2.0 autonomously investigates digital forensic evidence, correlates findings across multiple intelligence sources, validates conclusions, and generates executive-ready forensic reports—all from a single command.

Unlike traditional DFIR tools that require constant analyst interaction, SENTINEL independently performs forensic investigations while maintaining a complete audit trail and evidence-backed reasoning.

Features
Autonomous Digital Forensic Investigation
Memory Forensics Analysis
Disk Artifact Analysis
Multi-source Evidence Correlation
IOC Extraction
MITRE ATT&CK Mapping
Threat Attribution
Attack Timeline Reconstruction
Confidence Scoring
Evidence Validation
Anti-Hallucination Reasoning
Executive PDF Reporting
Complete Investigation Audit Trail
What SENTINEL Does

Given forensic evidence such as memory captures or disk images, SENTINEL automatically:

Performs forensic triage
Extracts Indicators of Compromise (IOCs)
Correlates evidence across multiple forensic sources
Maps attacker activity to the MITRE ATT&CK Framework
Attributes likely threat actors through infrastructure and behavioral correlation
Validates findings using evidence-driven consensus
Generates executive-ready investigation reports
Example Investigation
Case
SRL-2018 Enterprise Compromise
Investigation Result
Finding	Result
Compromise Status	✔ Confirmed
Threat Actor	APT32 (OceanLotus)
Confidence	92%
Evidence
✔ C2 Infrastructure Correlation
✔ PHP/Wetbot.A Malware Family
✔ PowerShell Persistence
✔ Five Confirmed MITRE ATT&CK Techniques
✔ Infrastructure Fingerprint Matching
Investigation Pipeline
Forensic Evidence
(Disk / Memory)
        │
        ▼
Memory & Artifact Analysis
        │
        ▼
Threat Attribution Engine
(Malware • Infrastructure • MITRE)
        │
        ▼
Predictive Intelligence
        │
        ▼
Evidence Validation
        │
        ▼
Consensus Engine
(Correlate • Verify • Score)
        │
        ▼
Executive Report
Timeline
MITRE ATT&CK Mapping
Confidence Assessment
Investigation Workflow
Phase	Description
Evidence Triage	Hash verification, OS identification, forensic profiling
Artifact Analysis	Registry, persistence, malware, filesystem analysis
Memory Analysis	Processes, DLLs, injected code, network artifacts
Evidence Correlation	Cross-reference forensic artifacts
Threat Attribution	Correlate malware, infrastructure, and ATT&CK techniques
Evidence Validation	Challenge findings and resolve contradictions
Reporting	Timeline reconstruction, ATT&CK mapping, executive reporting
Security Architecture

SENTINEL protects forensic evidence by blocking potentially destructive commands before execution.

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

This ensures forensic evidence remains immutable throughout the investigation.

Installation
Clone Repository
git clone https://github.com/0dayjakee/sentinel-ir.git
cd sentinel-ir
Install Dependencies
pip3 install groq reportlab --break-system-packages
Configure Groq API Key

Create your API key at:

https://console.groq.com/keys

Linux / SIFT:

export GROQ_API_KEY=your_groq_api_key
Environment Setup (SIFT Workstation)
Phase 1 — Download & Install

Download VirtualBox (Windows Hosts)

https://virtualbox.org

Download SIFT Workstation (.OVA)

https://www.sans.org/tools/sift-workstation

A free SANS account is required.

Install VirtualBox and import the downloaded SIFT Workstation appliance.

Phase 2 — Configure the SIFT VM

Import the appliance:

VirtualBox
→ File
→ Import Appliance
→ Select the SIFT .OVA
→ Next
→ Finish

Configure SSH Port Forwarding

VM Settings
→ Network
→ Adapter 1
→ Advanced
→ Port Forwarding

Add the following rule:

Field	Value
Name	SSH
Protocol	TCP
Host IP	127.0.0.1
Host Port	2222
Guest IP	10.0.2.15
Guest Port	22

Start the VM.

Default credentials:

Username:
sansforensics

Password:
forensics

Enable SSH inside SIFT:

sudo systemctl enable ssh
sudo systemctl start ssh
Phase 3 — Connect from Windows PowerShell
ssh -p 2222 sansforensics@127.0.0.1

Password:

forensics
Phase 4 — Install Dependencies

Inside the SIFT terminal:

pip3 install groq reportlab --break-system-packages
Phase 5 — Download the Case Dataset

Download the sample forensic memory image:

https://sansorg.egnyte.com/fl/HhH7crTYT4JK

File:

base-dc-memory.7z

Transfer it to SIFT:

scp -P 2222 "C:\Users\ADMIN\Downloads\base-dc-memory.7z" sansforensics@127.0.0.1:~/

Extract:

7z x base-dc-memory.7z
Phase 6 — Transfer SENTINEL

Copy the investigation engine to the SIFT VM:

scp -P 2222 "C:\Users\ADMIN\Downloads\sentinel_v2.py" sansforensics@127.0.0.1:~/
Phase 7 — Run an Autonomous Investigation

Configure your API key:

export GROQ_API_KEY=your_groq_api_key

Run the investigation:

python3 ~/sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
Quick Start

Run a complete autonomous forensic investigation with a single command.

python3 sentinel_v2.py /path/to/memory.img CASE-001

Example:

python3 ~/sentinel_v2.py ~/base-dc-memory.img SRL-2018-DC
Generated Output
cases/
└── CASE-001/
    ├── sentinel_report.json
    ├── sentinel_audit.log
    └── sentinel_v2_executive_report.pdf
Artifact	Description
sentinel_report.json	Structured forensic findings
sentinel_audit.log	Complete investigation audit trail
sentinel_v2_executive_report.pdf	Executive-ready investigation report
Sample Finding
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
Why SENTINEL?

Traditional DFIR platforms assist investigators.

SENTINEL performs the investigation.

It autonomously analyzes forensic evidence, correlates artifacts across multiple sources, validates conclusions, attributes attacker activity, and produces explainable, evidence-backed reports with complete auditability.

Security teams don't need another AI chatbot.

They need an autonomous digital forensic investigator.
