"""RC11 release inventory contract: exact UTF-8 paths, no normalization.
Only the root SHA256SUMS.txt and real root .git directory are excluded.
This validates membership/manifest syntax; sha256sum validates content.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

REQUIRED = {
    'README.md', 'LICENSE', 'NOTICE', 'LICENSE-SCOPE.md', 'CITATION.cff', 'NON_CLAIMS.md',
    'KNOWN_LIMITATIONS.md', 'ARTIFACT_REGISTRY.json', 'requirements-ci.txt',
    'RELEASE_NOTES_V2.7.7.md', '.github/workflows/verify.yml',
    'tools/ci_inventory_check.py', 'tools/ci_inventory_negative_controls.py',
    'tools/ci_release.sh', 'docs/RELEASE_GOVERNANCE_RC11.md',
    'docs/RG6_FINAL_RECONCILIATION_MATRIX.md', 'docs/B4_FINAL_EVIDENCE_RECORD.md',
    'eit_program_lang/receipt_verifier.py',
    'eit_program_lang/receipt_verifier_v277_candidate.py',
    'eit_program_lang/eit_v277_builder_candidate.py',
    'eit_program_lang/restored_registry_index_v277_candidate.py',
    'tests/test_receipt_verifier.py', 'tests/test_legacy_v275_fixtures.py',
    'zenodo/zenodo_metadata.json', 'zenodo/DESCRIPTION.md',
}

def inventory(root):
    root = Path(root)
    manifest = root / 'SHA256SUMS.txt'
    if not manifest.is_file() or manifest.is_symlink():
        raise ValueError('root manifest missing or symlink')
    data = manifest.read_bytes()
    if not data.endswith(b'\n') or b'\r' in data:
        raise ValueError('manifest must use LF and end in LF')
    names = []
    for line in data.decode('utf-8', errors='strict').splitlines():
        m = re.fullmatch(r'([0-9a-f]{64})  ([^\r\n]+)', line)
        if not m:
            raise ValueError('noncanonical manifest record')
        name = m.group(2)
        if name.startswith('/') or '\\' in name or any(p in ('', '.', '..') for p in name.split('/')):
            raise ValueError('unsafe path')
        if any(ord(c) < 32 or ord(c) == 127 for c in name):
            raise ValueError('control character in path')
        if name == 'SHA256SUMS.txt' or name.startswith('.git/') or name == '.git':
            raise ValueError('excluded/self path listed')
        names.append(name)
    if names != sorted(set(names), key=lambda n: n.encode('utf-8')):
        raise ValueError('manifest paths must be unique and UTF-8-byte sorted')
    actual = set()
    def walk_error(error):
        raise error
    for base, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        for name in list(dirs):
            p = Path(base) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                raise ValueError('symlink directory forbidden: ' + rel)
            if rel == '.git':
                dirs.remove(name)
                continue
            if name == '__pycache__' or name == '.pytest_cache':
                raise ValueError('cache directory forbidden: ' + rel)
        for name in files:
            p = Path(base) / name
            rel = p.relative_to(root).as_posix()
            if not stat.S_ISREG(p.lstat().st_mode):
                raise ValueError('nonregular file forbidden: ' + rel)
            if name.endswith(('.pyc', '.pyo')):
                raise ValueError('bytecode forbidden: ' + rel)
            if rel == '.git':
                raise ValueError('root .git must be a real directory, not a worktree file')
            if rel != 'SHA256SUMS.txt':
                actual.add(rel)
    if not REQUIRED.issubset(actual):
        raise ValueError('required paths missing: ' + repr(sorted(REQUIRED - actual)))
    if actual != set(names):
        raise ValueError('inventory mismatch; missing=%r unlisted=%r' % (sorted(set(names)-actual), sorted(actual-set(names))))
    metadata = json.loads((root/'zenodo/zenodo_metadata.json').read_bytes())
    registry = json.loads((root/'ARTIFACT_REGISTRY.json').read_bytes())
    if metadata.get('version') != '2.7.7-research.1' or registry.get('version') != metadata.get('version'):
        raise ValueError('current metadata/registry version mismatch')
    if 'doi' in metadata or 'publication_date' in metadata:
        raise ValueError('unpublished candidate metadata must not assert DOI/date')
    print('INVENTORY_OK: %d files; root-only exclusions; UTF-8 exact paths' % len(actual))
    return actual

if __name__ == '__main__':
    try:
        inventory(sys.argv[1] if len(sys.argv) > 1 else '.')
    except (ValueError, OSError, UnicodeError) as e:
        print('INVENTORY_FAIL: ' + str(e), file=sys.stderr)
        sys.exit(1)
