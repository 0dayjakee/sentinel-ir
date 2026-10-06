import importlib.util
import sys
import types
from pathlib import Path

import pytest


def _load(monkeypatch):
    groq = types.ModuleType("groq")
    groq.Groq = lambda **kw: object()  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "groq", groq)
    spec = importlib.util.spec_from_file_location("ghost_hunter_mod", Path("ghost_hunter.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def test_import_without_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    _load(monkeypatch)  # hindi dapat mag-crash


def test_get_client_requires_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    mod = _load(monkeypatch)
    with pytest.raises(RuntimeError):
        mod.get_client()


def test_get_client_with_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy")
    mod = _load(monkeypatch)
    assert mod.get_client() is mod.get_client()
