#!/usr/bin/env python3
"""Narrow structural validation, NOT authority enforcement or scientific review."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from datetime import datetime
import yaml

VALID_LIFECYCLE = {"draft", "stable", "deprecated"}
VALID_VERDICTS = {"HOLD", "SUPPLEMENT", "ESCALATE", "REJECT", "ADMIT_TO_WIKI"}

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node):
    result = {}
    for key, value in node.value:
        k = loader.construct_object(key)
        if k in result:
            raise ValueError(f"Duplicate YAML key: {k}")
        result[k] = loader.construct_object(value)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def parse_frontmatter(path: Path):
    txt=path.read_text(encoding="utf-8")
    m=re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n",txt,re.S)
    if not m:
        raise ValueError(f"{path}: YAML frontmatter missing or malformed")
    value=yaml.load(m.group(1),Loader=UniqueLoader)
    if not isinstance(value,dict):
        raise ValueError(f"{path}: YAML frontmatter must be a mapping")
    return value,txt[m.end():]

def iso_instant(v):
    if isinstance(v,datetime):
        return v.tzinfo is not None
    if not isinstance(v,str):
        return False
    try:
        dt=datetime.fromisoformat(v.replace('Z','+00:00'))
    except ValueError:
        return False
    return dt.tzinfo is not None

def validate_concept(path:Path)->list[str]:
    errors=[]
    try: meta,body=parse_frontmatter(path)
    except (ValueError,yaml.YAMLError,UnicodeError) as ex:
        return [str(ex)]
    if not isinstance(meta.get('type'),str) or not meta['type'].strip():
        errors.append(f'{path}: missing nonempty type')
    if 'status' in meta and meta['status'] not in VALID_LIFECYCLE:
        errors.append(f'{path}: non-OKF lifecycle status')
    sources=meta.get('sources',[])
    if not isinstance(sources,list):
        errors.append(f'{path}: sources must be a list')
        sources=[]
    ids=set()
    for src in sources:
        if not isinstance(src,dict) or not isinstance(src.get('resource'),str) or not src['resource'].strip():
            errors.append(f'{path}: each source must supply a nonempty resource')
            continue
        if 'id' in src:
            if not isinstance(src['id'],str) or not src['id'].strip():
                errors.append(f'{path}: source id must be nonempty')
            elif src['id'] in ids:
                errors.append(f'{path}: duplicate source id {src["id"]}')
            else: ids.add(src['id'])
    gen=meta.get('generated')
    if gen is not None:
        if not isinstance(gen,dict) or not isinstance(gen.get('by'),str) or not gen['by'].strip():
            errors.append(f'{path}: generated.by required if generated is present')
        elif 'at' in gen and not iso_instant(gen['at']):
            errors.append(f'{path}: generated.at requires timezone-aware ISO 8601')
    verified=meta.get('verified',[])
    if isinstance(verified,dict): verified=[verified]
    if not isinstance(verified,list):
        errors.append(f'{path}: verified must be a list or object')
    else:
        for x in verified:
            if not isinstance(x,dict) or not isinstance(x.get('by'),str) or not iso_instant(x.get('at')):
                errors.append(f'{path}: invalid verified event: requires by and timezone-aware at')
    for fid in set(re.findall(r'\[\^([^]\s]+)\](?!:)',body)):
        if fid not in ids: errors.append(f'{path}: footnote {fid} has no matching sources[].id')
    return errors

def validate_okf(root:Path)->list[str]:
    errors=[]
    okf=root/'60-Knowledge-Pilot'/'OKF'
    idx=okf/'index.md'
    if not idx.is_file(): return [f'{idx}: required by this template']
    try:
        meta,_=parse_frontmatter(idx)
        if set(meta)!={'okf_version'} or str(meta['okf_version'])!='0.2':
            errors.append(f'{idx}: only okf_version: "0.2" allowed in reserved index')
    except (ValueError,yaml.YAMLError,UnicodeError) as ex: errors.append(str(ex))
    for p in sorted(okf.rglob('*.md')):
        if p.name=='index.md':
            if p!=idx and p.read_text(encoding='utf-8').startswith('---'):
                errors.append(f'{p}: subdirectory reserved index must have no frontmatter')
            continue
        if p.name=='log.md':
            t=p.read_text(encoding='utf-8')
            if t.startswith('---'): errors.append(f'{p}: reserved log cannot have frontmatter')
            for heading in re.findall(r'^## (.+)$',t,re.M):
                try:datetime.strptime(heading,'%Y-%m-%d')
                except ValueError:errors.append(f'{p}: log date must be YYYY-MM-DD: {heading}')
            continue
        errors+=validate_concept(p)
    return errors

def validate_decisions(root:Path)->list[str]:
    errors=[]
    folder=root/'60-Knowledge-Pilot'/'DECISIONS'
    for p in sorted(folder.glob('*.md')):
        if p.name=='README.md':continue
        try:meta,_=parse_frontmatter(p)
        except (ValueError,yaml.YAMLError,UnicodeError) as ex:
            errors.append(str(ex));continue
        if meta.get('type')!='admission-record':errors.append(f'{p}: type must be admission-record')
        verdict=meta.get('disposition','HOLD')
        if verdict not in VALID_VERDICTS:errors.append(f'{p}: invalid disposition')
        if verdict=='ADMIT_TO_WIKI':
            if not (isinstance(meta.get('reviewer'),str) and meta['reviewer'].startswith('human:') and len(meta['reviewer'])>6):
                errors.append(f'{p}: human reviewer required for admission')
            if not iso_instant(meta.get('reviewed_at')):errors.append(f'{p}: reviewed_at required for admission')
            if not (isinstance(meta.get('source_ids'),list) and meta['source_ids']):errors.append(f'{p}: source_ids required for admission')
            if not (isinstance(meta.get('candidate'),str) and meta['candidate'].strip()):errors.append(f'{p}: exact candidate required for admission')
            if not (isinstance(meta.get('rationale'),str) and meta['rationale'].strip()):errors.append(f'{p}: rationale required for admission')
            if meta.get('authorized_effect')!='working-wiki-only':errors.append(f'{p}: external effect not permitted')
    return errors

def validate(root:Path)->list[str]:
    return validate_okf(root)+validate_decisions(root)

if __name__=='__main__':
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    issues=validate(root)
    for issue in issues:print('ERROR:',issue)
    if issues: print(f'Validation failed: {len(issues)} issue(s)');sys.exit(1)
    print('OK: structural OKF and admission-record checks passed; human/scientific review NOT performed.')
