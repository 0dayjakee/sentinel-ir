from pathlib import Path

from sentinel.case import create_case, load_case


def test_create_and_load_case_roundtrip(tmp_path: Path) -> None:
    evidence = tmp_path / "mem.img"
    evidence.write_bytes(b"forensic-bytes")

    case = create_case(
        case_id="CASE-UNIT-001",
        evidence_path=str(evidence),
        case_root=tmp_path,
    )
    assert case.case_id == "CASE-UNIT-001"
    assert case.evidence_path.endswith("mem.img")
    assert len(case.evidence_sha256) == 64

    loaded = load_case("CASE-UNIT-001", case_root=tmp_path)
    assert loaded.case_id == case.case_id
    assert loaded.evidence_sha256 == case.evidence_sha256
    assert loaded.metadata.get("read_only_analysis") is True
