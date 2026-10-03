#!/usr/bin/env python3
"""
GHOST HUNTER — Autonomous APT Attribution Engine
Extension of SENTINEL | FIND EVIL! Hackathon 2026 | SANS Institute
Author: Jhayke Sales
"""

import os
import json
import subprocess
import hashlib
import datetime
from pathlib import Path
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Known APT group signatures
APT_SIGNATURES = {
    "APT32": {
        "aliases": ["OceanLotus", "SeaLotus", "APT-C-00"],
        "nation": "Vietnam",
        "known_tools": ["Cobalt Strike", "Denis", "WINDSHIELD", "PHP backdoors", "Wetbot"],
        "known_domains": [".vn", "myvinhlong", "vietnamese"],
        "ttps": ["T1059.001", "T1055", "T1071", "T1105", "T1070.004"],
        "targets": ["government", "media", "manufacturing", "hospitality"]
    },
    "APT28": {
        "aliases": ["Fancy Bear", "Sofacy", "STRONTIUM"],
        "nation": "Russia",
        "known_tools": ["X-Agent", "X-Tunnel", "Mimikatz", "CHOPSTICK"],
        "known_domains": [".ru", "secure", "update"],
        "ttps": ["T1003", "T1059.001", "T1566", "T1078"],
        "targets": ["government", "military", "political"]
    },
    "APT29": {
        "aliases": ["Cozy Bear", "The Dukes", "NOBELIUM"],
        "nation": "Russia",
        "known_tools": ["MiniDuke", "CosmicDuke", "HAMMERTOSS", "Sunburst"],
        "known_domains": [".ru", "cloud", "microsoft-update"],
        "ttps": ["T1195", "T1059.001", "T1078", "T1027"],
        "targets": ["government", "think tanks", "healthcare"]
    },
    "APT41": {
        "aliases": ["Double Dragon", "Winnti", "BARIUM"],
        "nation": "China",
        "known_tools": ["POISONPLUG", "MESSAGETAP", "Cobalt Strike", "ShadowPad"],
        "known_domains": [".cn", "update", "download"],
        "ttps": ["T1190", "T1055", "T1059.001", "T1003"],
        "targets": ["healthcare", "telecom", "technology", "gaming"]
    },
    "Lazarus": {
        "aliases": ["Hidden Cobra", "ZINC", "Guardians of Peace"],
        "nation": "North Korea",
        "known_tools": ["HOPLIGHT", "FALLCHILL", "Manuscrypt", "WannaCry"],
        "known_domains": [".kp", "download", "update"],
        "ttps": ["T1059.001", "T1055", "T1486", "T1105"],
        "targets": ["financial", "cryptocurrency", "defense"]
    }
}

def analyze_iocs(findings: dict) -> dict:
    """Cross-reference findings against APT signature database"""
    scores = {}
    reasons = {}
    
    for apt, sig in APT_SIGNATURES.items():
        score = 0
        reason_list = []
        
        # Check domain matches
        for domain in sig["known_domains"]:
            for ioc in findings.get("c2_domains", []):
                if domain.lower() in ioc.lower():
                    score += 30
                    reason_list.append(f"C2 domain '{ioc}' matches {apt} infrastructure pattern")
        
        # Check tool matches
        for tool in sig["known_tools"]:
            for malware in findings.get("malware", []):
                if tool.lower() in malware.lower():
                    score += 25
                    reason_list.append(f"Malware '{malware}' matches {apt} known tool '{tool}'")
        
        # Check TTP matches
        for ttp in sig["ttps"]:
            for finding_ttp in findings.get("ttps", []):
                if ttp in finding_ttp:
                    score += 10
                    reason_list.append(f"TTP {ttp} matches {apt} known techniques")
        
        scores[apt] = min(score, 95)  # Cap at 95% — never 100% certain
        reasons[apt] = reason_list
    
    return scores, reasons

def run_ghost_hunter(sentinel_findings: dict, case_name: str = "CASE-001"):
    print("""
╔══════════════════════════════════════════════╗
║  GHOST HUNTER — APT Attribution Engine      ║
║  FIND EVIL! Hackathon 2026 | SANS Institute  ║
╠══════════════════════════════════════════════╣
║  Powered by SENTINEL findings                ║
║  Cross-referencing 5 major APT groups        ║
╚══════════════════════════════════════════════╝""")

    # Phase 1: Local signature matching
    print("\n[Phase 1] Cross-referencing against APT signature database...")
    scores, reasons = analyze_iocs(sentinel_findings)
    
    top_apt = max(scores, key=scores.get)
    top_score = scores[top_apt]
    
    print(f"\n[Phase 2] AI-powered deep attribution analysis...")
    
    evidence_str = json.dumps(sentinel_findings, indent=2)
    scores_str = json.dumps(scores, indent=2)
    
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': f'''You are GHOST HUNTER, an autonomous APT Attribution Engine integrated with SENTINEL DFIR.

SENTINEL has discovered these forensic findings:
{evidence_str}

Local signature matching scores:
{scores_str}

Based on this evidence:
1. Confirm or challenge the local attribution scores
2. Identify the most likely nation-state actor with confidence %
3. Explain the specific TTPs that match the attributed group
4. Reference MITRE ATT&CK Group profiles (G-numbers)
5. Identify potential false flag operations
6. Provide final verdict with confidence score and caveats

Be specific about WHY each indicator points to a specific group.'''}],
        max_tokens=2000
    )
    
    ai_analysis = resp.choices[0].message.content
    
    # Generate final report
    report = {
        "case": case_name,
        "generated_at": datetime.datetime.now().isoformat(),
        "sentinel_findings": sentinel_findings,
        "attribution_scores": scores,
        "top_attribution": {
            "apt_group": top_apt,
            "nation": APT_SIGNATURES[top_apt]["nation"],
            "confidence": top_score,
            "aliases": APT_SIGNATURES[top_apt]["aliases"],
            "evidence": reasons[top_apt]
        },
        "ai_analysis": ai_analysis
    }
    
    # Save report
    case_dir = Path(f"/cases/{case_name}")
    case_dir.mkdir(parents=True, exist_ok=True)
    report_path = case_dir / "ghost_hunter_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "="*60)
    print("GHOST HUNTER — FINAL ATTRIBUTION REPORT")
    print("="*60)
    print(f"\n🎯 TOP ATTRIBUTION: {top_apt} ({APT_SIGNATURES[top_apt]['nation']})")
    print(f"   Confidence: {top_score}%")
    print(f"   Aliases: {', '.join(APT_SIGNATURES[top_apt]['aliases'])}")
    print(f"\n📋 KEY EVIDENCE:")
    for r in reasons[top_apt]:
        print(f"   • {r}")
    print(f"\n🤖 AI DEEP ANALYSIS:\n{ai_analysis}")
    print(f"\n✅ Full report saved: {report_path}")
    
    return report

if __name__ == "__main__":
    # SRL-2018 findings from SENTINEL
    sentinel_findings = {
        "case": "SRL-2018-DC",
        "target": "Windows 10 64-bit Domain Controller",
        "incident_date": "2018-09-06",
        "malware": [
            "Backdoor:PowerShell/Listrun.A",
            "Meterpreter.H!attk",
            "Backdoor:PHP/Wetbot.A",
            "VirTool:Win32/RefDllInj.A",
            "Backdoor:Win32/PrintThin.A",
            "mstd32.dll"
        ],
        "c2_domains": [
            "myvinhlong.com",
            "settings.smart-web.me",
            "livestatscounter.com"
        ],
        "ttps": [
            "T1059.001 - PowerShell execution policy bypass",
            "T1055 - DLL injection via RefDllInj",
            "T1071 - C2 via HTTP",
            "T1105 - curl/wget ingress tool transfer",
            "T1070.004 - rm -f file deletion",
            "T1190 - PHP webshell initial access"
        ],
        "anti_forensics": [
            "Hidden PowerShell window",
            "File deletion after execution",
            "Execution policy bypass"
        ]
    }
    
    run_ghost_hunter(sentinel_findings, "SRL-2018-DC")
