from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def sha256_file(path: str | Path) -> str:
    """
    Calculate SHA-256 without modifying the source evidence.
    """
    source = Path(path)

    if not source.is_file():
        raise FileNotFoundError(f"Evidence file not found: {source}")

    digest = hashlib.sha256()

    with source.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)

    return digest.hexdigest()


def evidence_metadata(path: str | Path) -> dict:
    source = Path(path)

    if not source.is_file():
        raise FileNotFoundError(f"Evidence file not found: {source}")

    stat = source.stat()

    return {
        "path": str(source.resolve()),
        "name": source.name,
        "size": stat.st_size,
        "sha256": sha256_file(source),
        "read_only_analysis": True,
    }
