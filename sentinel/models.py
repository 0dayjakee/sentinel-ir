from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Evidence:
    evidence_id: str
    kind: str
    source: str
    description: str
    data: dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Finding:
    finding_id: str
    title: str
    severity: str
    confidence: str
    status: str
    description: str
    evidence_ids: list[str] = field(default_factory=list)
    techniques: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Case:
    case_id: str
    evidence_path: str
    evidence_sha256: str
    created_at: str = field(default_factory=utc_now)
    evidence: list[Evidence] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "evidence_path": self.evidence_path,
            "evidence_sha256": self.evidence_sha256,
            "created_at": self.created_at,
            "evidence": [x.to_dict() for x in self.evidence],
            "findings": [x.to_dict() for x in self.findings],
            "metadata": self.metadata,
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> Case:
        data = json.loads(path.read_text(encoding="utf-8"))

        evidence = [Evidence(**item) for item in data.get("evidence", [])]

        findings = [Finding(**item) for item in data.get("findings", [])]

        return cls(
            case_id=data["case_id"],
            evidence_path=data["evidence_path"],
            evidence_sha256=data["evidence_sha256"],
            created_at=data["created_at"],
            evidence=evidence,
            findings=findings,
            metadata=data.get("metadata", {}),
        )
