#!/usr/bin/env python3
"""Inspect local Codex availability; never start a task or read credentials."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
from typing import Any


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def probe(binary: str = 'codex', inspect: bool = False) -> dict[str, Any]:
    found = shutil.which(binary)
    result: dict[str, Any] = {
        'schema': 'srr.local-host-probe/1',
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'evidence_type': 'LOCAL_ENVIRONMENT_INSPECTION_NOT_INTEGRATION',
        'host_target': 'Codex CLI', 'platform': platform.system(),
        'python_version': platform.python_version(),
        'codex_found': found is not None,
        'resolved_entrypoint': None, 'entrypoint_sha256': None,
        'local_commands_executed': [], 'task_execution_requested': False,
        'credentials_read': False, 'integration_verified': False,
        'limitations': [
            'PATH absence describes this environment only.',
            'Entrypoint hash does not identify every transitive binary or package.',
            'Version/help are not proof of MCP or model-request behavior.'
        ]
    }
    if not found:
        result['status'] = 'CODEX_NOT_FOUND'
        return result
    path = Path(found).resolve(strict=True)
    result['resolved_entrypoint'] = str(path)
    result['entrypoint_sha256'] = digest(path)
    result['status'] = 'ENTRYPOINT_FOUND_NOT_VERIFIED'
    if inspect:
        for flag in ('--version', '--help'):
            record: dict[str, Any] = {'argv': [str(path), flag]}
            try:
                completed = subprocess.run(
                    [str(path), flag], stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=15, check=False,
                )
                record.update({
                    'returncode': completed.returncode,
                    'stdout': completed.stdout[:32768].decode('utf-8', errors='replace'),
                    'stderr': completed.stderr[:8192].decode('utf-8', errors='replace'),
                    'output_truncated': len(completed.stdout) > 32768 or len(completed.stderr) > 8192,
                })
            except (subprocess.TimeoutExpired, OSError) as exc:
                record['error_type'] = type(exc).__name__
            result['local_commands_executed'].append(record)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', default='codex', help='Trusted local executable; no shell interpretation.')
    parser.add_argument('--inspect-local-binary', action='store_true', help='Explicitly run --version and --help, not a model task.')
    parser.add_argument('--output', type=Path, help='Create a new JSON file; existing files are never overwritten.')
    args = parser.parse_args()
    try:
        text = json.dumps(probe(args.binary, args.inspect_local_binary), ensure_ascii=False, indent=2) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(text)
        print(text, end='')
        return 0  # Absence is a successful observation, not a host PASS.
    except (OSError, ValueError) as exc:
        print(json.dumps({'probe_error': type(exc).__name__, 'integration_verified': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
