from __future__ import annotations

from pathlib import Path

from .evidence import evidence_metadata
from .models import Case


DEFAULT_CASE_ROOT = Path("/cases")


def create_case(
    case_id: str,
    evidence_path: str,
    case_root: Path = DEFAULT_CASE_ROOT,
) -> Case:
    metadata = evidence_metadata(evidence_path)

    case = Case(
        case_id=case_id,
        evidence_path=metadata["path"],
        evidence_sha256=metadata["sha256"],
        metadata={
            "evidence_size": metadata["size"],
            "read_only_analysis": True,
        },
    )

    case_dir = case_root / case_id
    case.save(case_dir / "case.json")

    return case


def load_case(
    case_id: str,
    case_root: Path = DEFAULT_CASE_ROOT,
) -> Case:
    path = case_root / case_id / "case.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Case not found: {case_id}"
        )

    return Case.load(path)
