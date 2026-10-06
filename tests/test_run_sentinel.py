import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

from sentinel import custody


def _load(monkeypatch):
    genai = types.ModuleType("google.generativeai")
    genai.configure = lambda **kw: None  # type: ignore[attr-defined]
    google = types.ModuleType("google")
    google.generativeai = genai  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.generativeai", genai)
    spec = importlib.util.spec_from_file_location("sentinel_legacy", Path("sentinel_legacy.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


@pytest.mark.parametrize("tamper", [False, True])
def test_run_sentinel_end_to_end(tmp_path, monkeypatch, tamper):
    monkeypatch.setattr(custody, "CASE_ROOT", tmp_path / "cases")
    img = tmp_path / "mem.raw"
    img.write_bytes(b"x" * 4096)
    mod = _load(monkeypatch)

    class Resp:
        text = "summary"

    class Chat:
        def send_message(self, prompt):
            out = mod.calculate_hash(str(img))
            ref = out.rsplit("evidence_ref: ", 1)[1].rstrip("]")
            mod.write_finding("test", "desc", "calculate_hash", "high", ref)
            if tamper:
                img.write_bytes(b"y" * 4096)
            return Resp()

    class Model:
        def __init__(self, **kw):
            pass

        def start_chat(self, **kw):
            return Chat()

    monkeypatch.setattr(mod.genai, "GenerativeModel", Model, raising=False)
    mod.run_sentinel(str(img), "CASE-T")

    case = tmp_path / "cases" / "CASE-T"
    report = json.loads((case / "sentinel_report.json").read_text())
    events = [e["event"] for e in report["audit_trail"]]
    assert events[0] == "evidence_hash_pre"
    assert "evidence_hash_post" in events
    assert ("integrity_violation" in events) is tamper
    if tamper:
        assert events.index("integrity_violation") > events.index("evidence_hash_post")
    assert "hash" in events and "finding" in events
    assert report["evidence"]["unchanged"] is (not tamper)
    assert report["evidence"]["integrity_violation"] is tamper
    assert (case / "SHA256SUMS").exists()
    assert (case / "audit.log").exists()


def test_bad_case_name_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(custody, "CASE_ROOT", tmp_path / "cases")
    img = tmp_path / "mem.raw"
    img.write_bytes(b"x")
    mod = _load(monkeypatch)
    with pytest.raises(ValueError):
        mod.run_sentinel(str(img), "../../tmp/x")


def test_finding_rejected_with_unknown_ref(monkeypatch):
    mod = _load(monkeypatch)
    out = mod.write_finding("t", "d", "made up", "high", "E9999")
    assert out.startswith("REJECTED")
    assert mod.findings == []


def test_finding_rejected_when_cited_call_was_blocked(monkeypatch):
    mod = _load(monkeypatch)
    out = mod.run_volatility("relative.raw", "windows.pslist")  # BLOCKED, hindi tumatakbo ang vol
    assert out.startswith("BLOCKED")
    assert "evidence_ref" not in out
    ref = mod.audit_trail[-1]["ref"]
    assert mod.write_finding("t", "d", "x", "high", ref).startswith("REJECTED")
    assert mod.findings == []


def test_finding_rejected_when_citing_a_finding_event(monkeypatch, tmp_path):
    mod = _load(monkeypatch)
    f = tmp_path / "a.bin"
    f.write_bytes(b"abc")
    ref = mod.calculate_hash(str(f)).rsplit("evidence_ref: ", 1)[1].rstrip("]")
    assert mod.write_finding("t", "d", "hash", "high", ref).startswith("Recorded")
    finding_ref = next(e["ref"] for e in mod.audit_trail if e["event"] == "finding")
    assert mod.write_finding("t2", "d2", "x", "high", finding_ref).startswith("REJECTED")


def test_finding_accepted_with_hash_ref(monkeypatch, tmp_path):
    mod = _load(monkeypatch)
    f = tmp_path / "a.bin"
    f.write_bytes(b"abc")
    ref = mod.calculate_hash(str(f)).rsplit("evidence_ref: ", 1)[1].rstrip("]")
    assert mod.write_finding("t", "d", "hash", "high", ref).startswith("Recorded")
    assert mod.findings[0]["evidence_ref"] == ref
