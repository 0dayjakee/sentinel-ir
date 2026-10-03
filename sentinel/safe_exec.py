from __future__ import annotations

import os
import shlex
import subprocess
from collections.abc import Sequence
from pathlib import Path

ALLOWED_BINARIES = frozenset({"vol", "strings", "sha256sum", "md5sum", "file"})

# Colon-separated override: export SENTINEL_ALLOWED_ROOTS=/cases:/evidence:/mnt/images
ALLOWED_ROOTS = tuple(
    Path(p).resolve()
    for p in os.environ.get("SENTINEL_ALLOWED_ROOTS", "/cases:/evidence").split(":")
    if p
)

VOL_PLUGINS = frozenset(
    {
        "windows.info",
        "windows.pslist",
        "windows.psscan",
        "windows.pstree",
        "windows.psxview",
        "windows.cmdline",
        "windows.envars",
        "windows.dlllist",
        "windows.ldrmodules",
        "windows.handles",
        "windows.netscan",
        "windows.netstat",
        "windows.malfind",
        "windows.svcscan",
        "windows.filescan",
        "windows.registry.hivelist",
        "windows.registry.printkey",
        "linux.pslist",
        "linux.pstree",
        "linux.bash",
        "linux.sockstat",
        "linux.malfind",
    }
)

# Flags na pwedeng magsulat sa labas o mag-load ng code/symbols mula sa labas
VOL_DENIED_FLAGS = frozenset(
    {
        "-o",
        "--output-dir",
        "-p",
        "--plugin-dirs",
        "-s",
        "--symbol-dirs",
        "--cache-path",
        "--write-config",
        "--save-config",
        "--clear-cache",
        "--dump",
    }
)

MAX_OUTPUT = 4000
TIMEOUT_S = 120


def _path_allowed(arg: str) -> bool:
    """Non-path args pass; path-like args must resolve inside ALLOWED_ROOTS."""
    value = arg.split("=", 1)[1] if arg.startswith("-") and "=" in arg else arg
    if not (value.startswith(("/", "./", "../", "~")) or "/" in value):
        return True
    try:
        resolved = Path(value).expanduser().resolve()
    except (OSError, RuntimeError, ValueError):
        return False
    return any(resolved.is_relative_to(root) for root in ALLOWED_ROOTS)


def _is_denied_flag(arg: str) -> bool:
    if not arg.startswith("-"):
        return False
    if arg.split("=", 1)[0] in VOL_DENIED_FLAGS:
        return True
    # combined short form, e.g. -o/tmp
    return not arg.startswith("--") and arg[:2] in {"-o", "-p", "-s"}


def _validate(argv: Sequence[str]) -> str | None:
    if not argv:
        return "empty command"
    binary = argv[0]
    if binary not in ALLOWED_BINARIES:
        return f"'{binary}' not in allowlist"
    if binary == "vol":
        if len(argv) < 4 or argv[1] != "-f":
            return "vol must be: vol -f <image> <plugin> [args]"
        if argv[3] not in VOL_PLUGINS:
            return f"vol plugin '{argv[3]}' not allowed"
        if any(_is_denied_flag(a) for a in argv[4:]):
            return "vol flag not allowed"
    if not all(_path_allowed(a) for a in argv[1:]):
        return "path outside allowed roots"
    return None


def safe_run(argv: Sequence[str]) -> str:
    """Run an allowlisted forensic binary. No shell, no pipes."""
    args = [str(a) for a in argv]
    problem = _validate(args)
    if problem:
        return f"BLOCKED: {problem}"
    try:
        r = subprocess.run(
            args,
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


def run_command(cmd: str) -> str:
    """String wrapper (para sa tests / manual use)."""
    try:
        argv = shlex.split(cmd)
    except ValueError as e:
        return f"BLOCKED: malformed command ({e})"
    return safe_run(argv)
