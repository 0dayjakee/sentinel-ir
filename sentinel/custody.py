from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path

CASE_ROOT = Path("/cases")
_CASE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}")
LOGGER_NAME = "SENTINEL"


def safe_case_name(name: str) -> str:
    if not _CASE_RE.fullmatch(name) or ".." in name:
        raise ValueError(f"invalid case name: {name!r}")
    return name


def sha256_file(path: str | Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def prepare_case(case_name: str, root: Path | None = None) -> Path:
    """Create the case dir and attach <case>/audit.log to the SENTINEL logger."""
    case_dir = (root or CASE_ROOT) / safe_case_name(case_name)
    case_dir.mkdir(parents=True, exist_ok=True)
    log_path = case_dir / "audit.log"
    logger = logging.getLogger(LOGGER_NAME)
    if not any(
        getattr(h, "baseFilename", None) == str(log_path.resolve())
        for h in logger.handlers
    ):
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
    return case_dir


def finalize(case_dir: Path, report: dict) -> Path:
    """Close the audit log, write the report, then write SHA256SUMS over both."""
    logger = logging.getLogger(LOGGER_NAME)
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler):
            h.flush()
            h.close()
            logger.removeHandler(h)
    report_path = case_dir / "sentinel_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        f"{sha256_file(p)}  {p.name}"
        for p in (report_path, case_dir / "audit.log")
        if p.exists()
    ]
    (case_dir / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path
