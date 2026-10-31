#!/usr/bin/env python3
"""Structural OKF v0.2 validation, not authority enforcement or scientific review."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import re
import sys
import yaml

VALID_LIFECYCLE = {"draft", "stable", "deprecated"}
VALID_VERDICTS = {"HOLD", "SUPPLEMENT", "ESCALATE", "REJECT", "ADMIT_TO_WIKI"}
ACTOR_RE = re.compile(r"^(?:human:[^\s:]+|process:[^\s:]+|[^/\s]+/[^/\s]+)$")

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node):
    result = {}
    for key, value in node.value:
        parsed_key = loader.construct_object(key)
        if parsed_key in result:
            raise ValueError(f"Duplicate YAML key: {parsed_key}")
        result[parsed_key] = loader.construct_object(value)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise ValueError(f"{path}: YAML frontmatter missing or malformed")
    value = yaml.load(match.group(1), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: YAML frontmatter must be a mapping")
    return value, text[match.end():]

def iso_instant(value):
    if isinstance(value, datetime):
        return value.tzinfo is not None and value.utcoffset() is not None
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None

def valid_actor(value):
    return isinstance(value, str) and ACTOR_RE.fullmatch(value) is not None

def validate_time_window(path, label, value):
    if not isinstance(value, dict) or set(value) != {"from", "to"}:
        return [f"{path}: {label} must contain exactly from and to"]
    if not iso_instant(value["from"]) or not iso_instant(value["to"]):
        return [f"{path}: {label} requires timezone-aware ISO 8601 from/to"]
    start = datetime.fromisoformat(str(value["from"]).replace("Z", "+00:00"))
    end = datetime.fromisoformat(str(value["to"]).replace("Z", "+00:00"))
    if start > end:
        return [f"{path}: {label}.from must not be after to"]
    return []

def computation_section(body):
    match = re.search(r"(?ms)^# Computation\s*$\s*(.*?)(?=^#\s|\Z)", body)
    return None if match is None else match.group(1)

def validate_attested_computation(path, meta, body):
    errors = []
    runtime = meta.get("runtime")
    if not isinstance(runtime, str) or not runtime.strip():
        errors.append(f"{path}: Attested Computation requires nonempty runtime")
    parameters = meta.get("parameters", [])
    if not isinstance(parameters, list):
        errors.append(f"{path}: parameters must be a list")
    else:
        names = set()
        for parameter in parameters:
            if (not isinstance(parameter, dict)
                    or set(parameter) != {"name", "type", "required"}
                    or not isinstance(parameter.get("name"), str)
                    or not parameter["name"].strip()
                    or not isinstance(parameter.get("type"), str)
                    or not parameter["type"].strip()
                    or not isinstance(parameter.get("required"), bool)):
                errors.append(f"{path}: each parameter requires name, type and boolean required")
                continue
            if parameter["name"] in names:
                errors.append(f"{path}: duplicate parameter {parameter['name']}")
            names.add(parameter["name"])
    external = meta.get("computation")
    if external is not None and (not isinstance(external, str) or not external.strip()):
        errors.append(f"{path}: computation must be a nonempty path when present")
    section = computation_section(body)
    marker = chr(96) * 3
    pattern = r"(?ms)^" + re.escape(marker) + r"[^\n]*\n.*?^" + re.escape(marker) + r"\s*$"
    fences = [] if section is None else re.findall(pattern, section)
    if external is None:
        if section is None or len(fences) != 1:
            errors.append(f"{path}: inline Attested Computation requires exactly one fenced code block under # Computation")
    elif fences:
        errors.append(f"{path}: external computation path and inline computation are mutually exclusive")
    executor = meta.get("executor")
    if executor is not None:
        if (not isinstance(executor, dict)
                or not isinstance(executor.get("resource"), str)
                or not executor["resource"].strip()
                or not isinstance(executor.get("receipt"), list)
                or not executor["receipt"]
                or any(not isinstance(item, str) or not item.strip() for item in executor["receipt"])):
            errors.append(f"{path}: executor requires nonempty resource and receipt string list")
    attester = meta.get("attester")
    if attester is not None and (not isinstance(attester, dict)
            or not isinstance(attester.get("resource"), str)
            or not attester["resource"].strip()):
        errors.append(f"{path}: attester requires nonempty resource")
    return errors

def validate_concept(path: Path) -> list[str]:
    errors = []
    try:
        meta, body = parse_frontmatter(path)
    except (ValueError, yaml.YAMLError, UnicodeError) as exc:
        return [str(exc)]
    if not isinstance(meta.get("type"), str) or not meta["type"].strip():
        errors.append(f"{path}: missing nonempty type")
    if "status" in meta and meta["status"] not in VALID_LIFECYCLE:
        errors.append(f"{path}: non-OKF lifecycle status")
    if "stale_after" in meta and not iso_instant(meta["stale_after"]):
        errors.append(f"{path}: stale_after requires timezone-aware ISO 8601")
    sources = meta.get("sources", [])
    if not isinstance(sources, list):
        errors.append(f"{path}: sources must be a list")
        sources = []
    source_ids = set()
    for source in sources:
        if (not isinstance(source, dict)
                or not isinstance(source.get("resource"), str)
                or not source["resource"].strip()):
            errors.append(f"{path}: each source must supply a nonempty resource")
            continue
        source_id = source.get("id")
        if source_id is not None:
            if not isinstance(source_id, str) or not source_id.strip():
                errors.append(f"{path}: source id must be nonempty")
            elif source_id in source_ids:
                errors.append(f"{path}: duplicate source id {source_id}")
            else:
                source_ids.add(source_id)
        if "author" in source and not valid_actor(source["author"]):
            errors.append(f"{path}: source author must follow the OKF actor convention")
        if "usage_count" in source and (isinstance(source["usage_count"], bool)
                or not isinstance(source["usage_count"], int)
                or source["usage_count"] < 0):
            errors.append(f"{path}: source usage_count must be a nonnegative integer")
        if "last_modified" in source and not iso_instant(source["last_modified"]):
            errors.append(f"{path}: source last_modified requires timezone-aware ISO 8601")
        if "usage_window" in source:
            errors += validate_time_window(path, "source usage_window", source["usage_window"])
    if "usage_window" in meta:
        errors += validate_time_window(path, "usage_window", meta["usage_window"])
    generated = meta.get("generated")
    if generated is not None:
        if not isinstance(generated, dict) or not valid_actor(generated.get("by")):
            errors.append(f"{path}: generated.by must follow the OKF actor convention")
        if isinstance(generated, dict) and "at" in generated and not iso_instant(generated["at"]):
            errors.append(f"{path}: generated.at requires timezone-aware ISO 8601")
    verified = meta.get("verified", [])
    if isinstance(verified, dict):
        verified = [verified]
    if not isinstance(verified, list):
        errors.append(f"{path}: verified must be a list or object")
    else:
        for event in verified:
            if (not isinstance(event, dict)
                    or not valid_actor(event.get("by"))
                    or not iso_instant(event.get("at"))):
                errors.append(f"{path}: verified event requires an OKF actor and timezone-aware at")
    for footnote_id in set(re.findall(r"\[\^([^]\s]+)\](?!:)", body)):
        if footnote_id not in source_ids:
            errors.append(f"{path}: footnote {footnote_id} has no matching sources[].id")
    if meta.get("type") == "Attested Computation":
        errors += validate_attested_computation(path, meta, body)
    return errors

def validate_index(path: Path, bundle_root: bool):
    errors = []
    text = path.read_text(encoding="utf-8")
    if bundle_root:
        try:
            meta, body = parse_frontmatter(path)
            if set(meta) != {"okf_version"} or str(meta["okf_version"]) != "0.2":
                errors.append(f'{path}: only okf_version: "0.2" allowed in reserved index')
        except (ValueError, yaml.YAMLError, UnicodeError) as exc:
            return [str(exc)]
    else:
        body = text
        if text.startswith("---"):
            errors.append(f"{path}: subdirectory reserved index must have no frontmatter")
    if not re.search(r"(?m)^#\s+\S", body):
        errors.append(f"{path}: index requires at least one level-one section heading")
    return errors

def validate_log(path: Path):
    errors = []
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        errors.append(f"{path}: reserved log cannot have frontmatter")
    headings = re.findall(r"(?m)^## (.+)$", text)
    parsed = []
    for heading in headings:
        try:
            parsed.append(datetime.strptime(heading, "%Y-%m-%d").date())
        except ValueError:
            errors.append(f"{path}: log date must be YYYY-MM-DD: {heading}")
    if parsed != sorted(parsed, reverse=True):
        errors.append(f"{path}: log date headings must be newest first")
    return errors

def validate_okf(root: Path) -> list[str]:
    errors = []
    okf = root / "60-Knowledge-Pilot" / "OKF"
    index = okf / "index.md"
    if not index.is_file():
        return [f"{index}: required by this template"]
    errors += validate_index(index, bundle_root=True)
    for path in sorted(okf.rglob("*.md")):
        if path == index:
            continue
        if path.name == "index.md":
            errors += validate_index(path, bundle_root=False)
        elif path.name == "log.md":
            errors += validate_log(path)
        else:
            errors += validate_concept(path)
    return errors

def validate_decisions(root: Path) -> list[str]:
    errors = []
    folder = root / "60-Knowledge-Pilot" / "DECISIONS"
    for path in sorted(folder.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            meta, _ = parse_frontmatter(path)
        except (ValueError, yaml.YAMLError, UnicodeError) as exc:
            errors.append(str(exc))
            continue
        if meta.get("type") != "admission-record":
            errors.append(f"{path}: type must be admission-record")
        verdict = meta.get("disposition", "HOLD")
        if verdict not in VALID_VERDICTS:
            errors.append(f"{path}: invalid disposition")
        if verdict == "ADMIT_TO_WIKI":
            if not (isinstance(meta.get("reviewer"), str)
                    and meta["reviewer"].startswith("human:")
                    and len(meta["reviewer"]) > 6):
                errors.append(f"{path}: human reviewer required for admission")
            if not iso_instant(meta.get("reviewed_at")):
                errors.append(f"{path}: reviewed_at required for admission")
            if not (isinstance(meta.get("source_ids"), list) and meta["source_ids"]):
                errors.append(f"{path}: source_ids required for admission")
            if not (isinstance(meta.get("candidate"), str) and meta["candidate"].strip()):
                errors.append(f"{path}: exact candidate required for admission")
            if not (isinstance(meta.get("rationale"), str) and meta["rationale"].strip()):
                errors.append(f"{path}: rationale required for admission")
            if meta.get("authorized_effect") != "working-wiki-only":
                errors.append(f"{path}: external effect not permitted")
    return errors

def validate(root: Path) -> list[str]:
    return validate_okf(root) + validate_decisions(root)

if __name__ == "__main__":
    repository_root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    issues = validate(repository_root)
    for issue in issues:
        print("ERROR:", issue)
    if issues:
        print(f"Validation failed: {len(issues)} issue(s)")
        sys.exit(1)
    print("OK: structural OKF v0.2 and admission-record checks passed; human/scientific review NOT performed.")
