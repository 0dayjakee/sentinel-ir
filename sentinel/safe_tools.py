from __future__ import annotations

import contextlib
import subprocess
import threading
from pathlib import Path

from sentinel import safe_exec as sx

MAX_PATTERN = 200


def _confined(path: str) -> Path | None:
    """Resolve to an absolute path; return it only if inside ALLOWED_ROOTS."""
    try:
        p = Path(path).expanduser().resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    return p if any(p.is_relative_to(r) for r in sx.ALLOWED_ROOTS) else None


def _kill(procs: list[subprocess.Popen[str]]) -> None:
    for p in procs:
        with contextlib.suppress(OSError):
            p.kill()


def _read_bounded(procs: list[subprocess.Popen[str]]) -> str:
    """Read at most MAX_OUTPUT chars from the last process; kill all on limit/timeout."""
    last = procs[-1]
    if last.stdout is None:
        _kill(procs)
        return "ERROR: no stdout"
    timer = threading.Timer(sx.TIMEOUT_S, _kill, args=(procs,))
    timer.start()
    try:
        out = last.stdout.read(sx.MAX_OUTPUT)
    finally:
        timer.cancel()
        _kill(procs)
        last.stdout.close()
        for p in procs:
            p.wait()
    return out or "(no output)"


def strings_grep(path: str, pattern: str = "", limit: int = 50) -> str:
    """strings -n 6 <path>, optionally filtered by grep -iE. No shell."""
    target = _confined(path)
    if target is None:
        return "BLOCKED: path outside allowed roots"
    if len(pattern) > MAX_PATTERN:
        return "BLOCKED: pattern too long"
    limit = max(1, min(limit, 200))
    procs: list[subprocess.Popen[str]] = []
    try:
        strings = subprocess.Popen(  # nosec B603, B607
            ["strings", "-n", "6", str(target)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            errors="replace",
        )
        procs.append(strings)
        if pattern:
            grep = subprocess.Popen(  # nosec B603, B607
                ["grep", "-i", "-E", "-m", str(limit), "-e", pattern],
                stdin=strings.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
            )
            if strings.stdout:
                strings.stdout.close()
            procs.append(grep)
    except (OSError, ValueError) as e:
        _kill(procs)
        return f"ERROR: {e}"
    return _read_bounded(procs)


def grep_tree(pattern: str, path: str) -> str:
    """grep -r -i -m 20 <pattern> <path>, confined to ALLOWED_ROOTS. No shell."""
    target = _confined(path)
    if target is None:
        return "BLOCKED: path outside allowed roots"
    if len(pattern) > MAX_PATTERN:
        return "BLOCKED: pattern too long"
    try:
        grep = subprocess.Popen(  # nosec B603, B607
            ["grep", "-r", "-i", "-m", "20", "-e", pattern, str(target)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
    except (OSError, ValueError) as e:
        return f"ERROR: {e}"
    return _read_bounded([grep])
