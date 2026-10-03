from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

ALLOWED_BINARIES = {"vol", "strings", "sha256sum", "md5sum", "file"}
ALLOWED_ROOTS = (Path("/cases").resolve(), Path("/evidence").resolve())  # ayusin ayon sa setup
MAX_OUTPUT = 4000
TIMEOUT_S = 120


def _path_allowed(arg: str) -> bool:
    """Non-path args pass; path-like args must resolve inside ALLOWED_ROOTS."""
    value = arg.split("=", 1)[1] if arg.startswith("-") and "=" in arg else arg
    if not (value.startswith(("/", "./", "../", "~")) or "/" in value):
        return True
    try:
        resolved = Path(value).expanduser().resolve()
    except (OSError, RuntimeError):
        return False
    return any(resolved.is_relative_to(root) for root in ALLOWED_ROOTS)


def run_command(cmd: str) -> str:
    """Run an allowlisted forensic binary. No shell, no pipes."""
    try:
        argv = shlex.split(cmd)
    except ValueError as e:
        return f"BLOCKED: malformed command ({e})"

    if not argv:
        return "BLOCKED: empty command"
    if argv[0] not in ALLOWED_BINARIES:
        return f"BLOCKED: '{argv[0]}' not in allowlist"
    if not all(_path_allowed(a) for a in argv[1:]):
        return "BLOCKED: path outside allowed roots"

    try:
        r = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return f"ERROR: timed out after {TIMEOUT_S}s"
    except (OSError, ValueError) as e:
        return f"ERROR: {e}"
    return (r.stdout or r.stderr or "(no output)")[:MAX_OUTPUT]
