#!/usr/bin/env python3
"""Conservative public-publishing tripwire, not a complete security scan."""
from __future__ import annotations
import re
import sys
from pathlib import Path

SCAN_EXT={'.md','.txt','.json','.yml','.yaml','.py','.sh','.toml','.csv'}
# Regexes intentionally avoid containing any actual private IDs, URLs or token values.
CHECKS=[
 ('Google Drive or Docs object URL', re.compile(r'https?://(?:drive|docs)\.google\.com/[^\s<)>]+',re.I)),
 ('Email address',re.compile(r'\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b',re.I)),
 ('Common personal access token',re.compile(r'\b(?:ghp_|gho_|ghu_|github_pat_)[A-Za-z0-9_]{14,}')),
 ('OpenAI-shaped API token',re.compile(r'\bsk-[A-Za-z0-9_-]{20,}')),
 ('Private key header',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
]
SKIP={'scripts/audit_public.py'}

def scan(root:Path)->list[str]:
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file():continue
        relative=p.relative_to(root).as_posix()
        if relative in SKIP or '.git' in p.parts or p.suffix.lower() not in SCAN_EXT:continue
        if p.stat().st_size>1_000_000:
            findings.append(f'{relative}: file over 1 MB; manual review required');continue
        try:content=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            findings.append(f'{relative}: non-UTF8 text, inspect manually');continue
        for label,pattern in CHECKS:
            if pattern.search(content):findings.append(f'{relative}: {label} detected')
    return findings

if __name__=='__main__':
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    problems=scan(root)
    for v in problems:print('BLOCK:',v)
    if problems:print('Public-disclosure tripwire failed. Manually inspect every file.');sys.exit(1)
    print('OK: no configured disclosure patterns detected; this is NOT a comprehensive privacy/secret review.')
