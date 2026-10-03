import hashlib
import importlib.util
from pathlib import Path


def _load_legacy():
    spec = importlib.util.spec_from_file_location(
        "sentinel_legacy", Path("sentinel.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def test_hash_file_matches_hashlib(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    f = tmp_path / "e.bin"
    f.write_bytes(b"evidence" * 1000)
    mod = _load_legacy()
    out = mod.hash_file(str(f))
    assert hashlib.sha256(f.read_bytes()).hexdigest() in out
