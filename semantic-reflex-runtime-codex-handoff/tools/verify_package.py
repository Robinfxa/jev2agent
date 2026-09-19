#!/usr/bin/env python3
"""Check a sealed directory against SHA256SUMS; not an authenticity signature."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from check_e0_evidence import artifact_path, SHA


def verify(root: Path) -> dict:
    errors = []
    sums = root / 'SHA256SUMS.txt'
    expected = {}
    for line in sums.read_text(encoding='utf-8').splitlines():
        try:
            checksum, name = line.split('  ', 1)
            if not SHA.fullmatch(checksum) or name == 'SHA256SUMS.txt' or name in expected:
                raise ValueError('malformed inventory')
            path = artifact_path(root, name)
            expected[name] = checksum
            with path.open('rb') as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != checksum:
                errors.append(f'Hash mismatch: {name}')
        except (OSError, ValueError):
            errors.append('Invalid, missing, unsafe, or duplicate inventory entry')
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob('*')
                    if p.is_file() and p != sums}
    for name in sorted(actual_files - set(expected)):
        errors.append(f'Unlisted file: {name}')
    if not expected:
        errors.append('Empty manifest')
    return {'package_integrity': 'PASS' if not errors else 'FAIL',
            'listed_files': len(expected), 'errors': errors,
            'authenticity_signature': False, 'host_verified': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.root)
    except (OSError, ValueError) as exc:
        result = {'package_integrity': 'FAIL', 'error_type': type(exc).__name__, 'host_verified': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('package_integrity') == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
