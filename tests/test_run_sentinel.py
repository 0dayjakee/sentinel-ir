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
    spec = importlib.util.spec_from_file_location(
        "sentinel_legacy", Path("sentinel.py")
    )
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
            mod.calculate_hash(str(img))
            mod.write_finding("test", "desc", "calculate_hash", "high")
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
    assert events[-1] == "evidence_hash_post"
    assert "hash" in events and "finding" in events
    assert report["evidence"]["unchanged"] is (not tamper)
    assert (case / "SHA256SUMS").exists()
    assert (case / "audit.log").exists()


def test_bad_case_name_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(custody, "CASE_ROOT", tmp_path / "cases")
    img = tmp_path / "mem.raw"
    img.write_bytes(b"x")
    mod = _load(monkeypatch)
    with pytest.raises(ValueError):
        mod.run_sentinel(str(img), "../../tmp/x")
