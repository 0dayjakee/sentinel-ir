import hashlib
import importlib.util
import sys
import types
from pathlib import Path


def _load_legacy(monkeypatch):
    # Stub google.generativeai para hindi kailangan ang package sa test env
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


def test_hash_file_matches_hashlib(tmp_path, monkeypatch):
    f = tmp_path / "e.bin"
    f.write_bytes(b"evidence" * 1000)
    mod = _load_legacy(monkeypatch)
    out = mod.calculate_hash(str(f))
    assert hashlib.sha256(f.read_bytes()).hexdigest() in out


def test_calculate_hash_md5_and_error_paths(tmp_path, monkeypatch):
    f = tmp_path / "e.bin"
    f.write_bytes(b"abc")
    mod = _load_legacy(monkeypatch)
    assert mod.calculate_hash(str(f), "md5").startswith("MD5: 900150983cd24fb0d6963f7d28e17f72")
    assert mod.calculate_hash(str(tmp_path / "missing.bin")).startswith("ERROR")
    assert mod.calculate_hash(str(f), "notanalgo").startswith("ERROR")
