#!/usr/bin/env python3
"""Validate that the public template manifest exactly describes the file tree."""
from __future__ import annotations
import json
from pathlib import Path
import sys

GENERATED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
MANIFEST_NAME = "template-manifest.json"

def repository_files(root: Path) -> set[str]:
    result = set()
    for path in root.rglob("*"):
        if any(part in GENERATED_DIRECTORIES for part in path.parts):
            continue
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
    return result

def validate_manifest(root: Path) -> list[str]:
    errors = []
    path = root / MANIFEST_NAME
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{path}: unreadable manifest: {exc}"]
    listed = manifest.get("files")
    excluded = manifest.get("manifest_excludes")
    if not isinstance(listed, list) or any(not isinstance(item, str) or not item for item in listed):
        return [f"{path}: files must be a list of nonempty paths"]
    if len(listed) != len(set(listed)):
        errors.append(f"{path}: files contains duplicates")
    if excluded != [MANIFEST_NAME]:
        errors.append(f"{path}: manifest_excludes must contain only {MANIFEST_NAME}")
        excluded = []
    actual = repository_files(root)
    expected = set(listed) | set(excluded)
    for missing in sorted(actual - expected):
        errors.append(f"{path}: unlisted repository file: {missing}")
    for absent in sorted(expected - actual):
        errors.append(f"{path}: listed file does not exist: {absent}")
    if MANIFEST_NAME in set(listed):
        errors.append(f"{path}: manifest must be declared through manifest_excludes, not files")
    return errors

if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems = validate_manifest(root)
    for problem in problems:
        print("ERROR:", problem)
    if problems:
        print(f"Manifest validation failed: {len(problems)} issue(s)")
        sys.exit(1)
    print("OK: template manifest exactly matches the distributable file tree.")
