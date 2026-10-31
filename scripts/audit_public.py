#!/usr/bin/env python3
"""Conservative public-publishing tripwire, not a complete security scan."""
from __future__ import annotations
from pathlib import Path
import re
import sys

ALLOWED_TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
ALLOWED_EXTENSIONLESS_NAMES = {"LICENSE", ".gitignore", ".gitkeep"}
MAX_TEXT_BYTES = 1_000_000
CHECKS = [
    ("Google Drive or Docs object URL", re.compile(r"https?://(?:drive|docs)\.google\.com/[^\s<)>]+", re.I)),
    ("Email address", re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.I)),
    ("Common personal access token", re.compile(r"\b(?:ghp_|gho_|ghu_|github_pat_)[A-Za-z0-9_]{14,}")),
    ("OpenAI-shaped API token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("Private key header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]
SKIP_CONTENT_SCAN = {"scripts/audit_public.py"}
GENERATED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}

def allowed_text_file(path: Path):
    return path.suffix.lower() in ALLOWED_TEXT_SUFFIXES or path.name in ALLOWED_EXTENSIONLESS_NAMES

def scan(root: Path) -> list[str]:
    findings = []
    for path in root.rglob("*"):
        if any(part in GENERATED_DIRECTORIES for part in path.parts) or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            findings.append(f"{relative}: symbolic links are not allowed")
            continue
        if not allowed_text_file(path):
            findings.append(f"{relative}: unapproved file type; explicit public-review approval required")
            continue
        if path.stat().st_size > MAX_TEXT_BYTES:
            findings.append(f"{relative}: file over 1 MB; manual review required")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{relative}: non-UTF8 content; manual review required")
            continue
        if relative in SKIP_CONTENT_SCAN:
            continue
        for label, pattern in CHECKS:
            if pattern.search(content):
                findings.append(f"{relative}: {label} detected")
    return findings

if __name__ == "__main__":
    repository_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems = scan(repository_root)
    for problem in problems:
        print("BLOCK:", problem)
    if problems:
        print("Public-disclosure tripwire failed. Remove or explicitly review every reported file before changing the allowlist.")
        sys.exit(1)
    print("OK: repository contains only approved UTF-8 text types and no configured disclosure patterns; this is NOT a comprehensive privacy/secret review.")
