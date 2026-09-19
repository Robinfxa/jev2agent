#!/usr/bin/env python3
"""Check E0 evidence structure and file identity, never certify a real host."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

CASE_IDS = tuple(f'H{i:02d}' for i in range(1, 15)) + ('ISOLATION',)
SHA = re.compile(r'[0-9a-f]{64}\Z')
BAD_TEXT = {'', 'todo', 'tbd', 'null', 'none', 'unknown', 'not_run', '待填', '待核验', 'latest', 'main', 'master', 'stable'}


def text_is_set(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in BAD_TEXT


def file_sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def artifact_path(root: Path, name: Any) -> Path:
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('invalid relative artifact path')
    rel = PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or rel == PurePosixPath('.'):
        raise ValueError('artifact must remain inside evidence root')
    base = root.resolve(strict=True)
    current = base
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('symlink evidence is not accepted')
    resolved = current.resolve(strict=True)
    if not resolved.is_relative_to(base) or not resolved.is_file():
        raise ValueError('artifact must be a file inside evidence root')
    return resolved


def validate(doc: Any, root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ['Evidence must be a JSON object.']
    if doc.get('schema') != 'srr.codex-e0-evidence/1':
        errors.append('schema: expected srr.codex-e0-evidence/1')
    if not text_is_set(doc.get('release_id')):
        errors.append('release_id: missing')
    host = doc.get('host')
    if not isinstance(host, dict):
        host = {}
        errors.append('host: expected an object')
    if host.get('name') != 'Codex CLI':
        errors.append('host.name: expected Codex CLI')
    for key in ('version', 'distribution_ref', 'provider_build', 'mcp_sdk_version'):
        value = host.get(key)
        if not text_is_set(value) or (isinstance(value, str) and ('*' in value or value.endswith('@latest'))):
            errors.append(f'host.{key}: an explicit observed identity is required')
    for key in ('entrypoint_sha256', 'native_config_sha256', 'run_manifest_sha256'):
        value = host.get(key)
        if not isinstance(value, str) or not SHA.fullmatch(value):
            errors.append(f'host.{key}: missing or invalid SHA-256')
    cases = doc.get('cases')
    if not isinstance(cases, list):
        return errors + ['cases: expected a list']
    seen: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            errors.append('case entry: expected an object')
            continue
        cid = item.get('case_id')
        if not isinstance(cid, str) or cid not in CASE_IDS:
            errors.append('case_id: unexpected or invalid')
            continue
        if cid in seen:
            errors.append(f'{cid}: duplicate case')
        seen.add(cid)
        if item.get('status') != 'PASS':
            errors.append(f'{cid}: not a recorded PASS (N/A is not allowed for this profile)')
        if item.get('evidence_kind') != 'REAL_CODEX_CAPTURE':
            errors.append(f'{cid}: requires real Codex evidence, not a local or synthetic fixture')
        for key in ('expected', 'observed', 'limitations', 'reviewer'):
            if not text_is_set(item.get(key)):
                errors.append(f'{cid}.{key}: missing')
        artifacts = item.get('artifacts')
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f'{cid}: at least one bounded, hashed evidence artifact is required')
            continue
        for evidence in artifacts:
            if not isinstance(evidence, dict):
                errors.append(f'{cid}: invalid artifact entry')
                continue
            expected = evidence.get('sha256')
            if not isinstance(expected, str) or not SHA.fullmatch(expected):
                errors.append(f'{cid}: invalid artifact hash')
                continue
            try:
                path = artifact_path(root, evidence.get('path'))
                if file_sha(path) != expected:
                    errors.append(f'{cid}: evidence hash mismatch')
            except (ValueError, OSError):
                errors.append(f'{cid}: missing, unsafe, or unreadable artifact path')
    for cid in CASE_IDS:
        if cid not in seen:
            errors.append(f'{cid}: planned case is missing')
    return errors


def report(doc: Any, root: Path) -> dict[str, Any]:
    errors = validate(doc, root)
    return {
        'schema': 'srr.e0-evidence-preflight/1',
        'documentation_status': 'NOT_READY' if errors else 'READY_FOR_HUMAN_REVIEW',
        'e0_verified': False, 'automatic_activation': False,
        'scope': 'File identity and required fields only; content truth and host semantics require human review.',
        'errors': errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', required=True, type=Path)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--json-output', type=Path, help='Create a new report file, never overwrite.')
    args = parser.parse_args()
    try:
        doc = json.loads(args.evidence.read_text(encoding='utf-8'))
        result = report(doc, args.root)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.json_output:
            with args.json_output.open('x', encoding='utf-8') as stream:
                stream.write(encoded)
        print(encoded, end='')
        return 2 if result['errors'] else 0
    except (OSError, ValueError) as exc:
        print(json.dumps({'documentation_status': 'NOT_READY', 'e0_verified': False,
                          'automatic_activation': False, 'error_type': type(exc).__name__}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
