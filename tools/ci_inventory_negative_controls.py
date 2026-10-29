"""Release-layer controls only. Work exclusively on temporary copies."""
import json, os, runpy, hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

source = Path(sys.argv[1]).resolve()
results = []

def check(label, mutate, expected=1, hash_check=False):
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / 'tree'
        def ignore_root_git(directory, names):
            return ['.git'] if Path(directory).resolve() == source and '.git' in names else []
        shutil.copytree(source, target, ignore=ignore_root_git)
        mutate(target)
        cmd = ['sha256sum', '--strict', '-c', 'SHA256SUMS.txt'] if hash_check else [sys.executable, str(target/'tools/ci_inventory_check.py'), str(target)]
        r = subprocess.run(cmd, cwd=target, capture_output=True, text=True)
        ok = r.returncode == expected
        results.append({'control':label, 'expected_exit':expected, 'actual_exit':r.returncode, 'pass':ok})
        if not ok:
            print(r.stdout, r.stderr)
            raise RuntimeError('control failed: '+label)

check('unlisted .gitkeep', lambda t: (t/'.gitkeep').write_text(''))
check('nested SHA256SUMS.txt is not excluded', lambda t: (t/'tests/SHA256SUMS.txt').write_text(''))
check('missing required README', lambda t: (t/'README.md').unlink())
def remove_required_and_entry(t):
    (t/'README.md').unlink()
    p=t/'SHA256SUMS.txt'
    p.write_text(''.join(line for line in p.read_text().splitlines(True) if not line.endswith('  README.md\n')))
check('REQUIRED independently enforced when file and manifest entry removed', remove_required_and_entry)
check('bytecode file', lambda t: (t/'tests/stray.pyc').write_bytes(b'x'))
check('cache directory', lambda t: (t/'tests/__pycache__').mkdir())
check('symlink', lambda t: (t/'stray-link').symlink_to('README.md'))
check('duplicate manifest path', lambda t: (t/'SHA256SUMS.txt').write_bytes((t/'SHA256SUMS.txt').read_bytes()*2))
check('content tamper caught by canonical hash check', lambda t: (t/'README.md').write_bytes(b'tampered'), hash_check=True)
check('root .git directory explicitly excluded', lambda t: ((t/'.git').mkdir(), (t/'.git/config').write_text('test')), expected=0)
def add_listed_files(t, names):
    additions=[]
    for name in names:
        p=t/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'positive-control')
        additions.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+name+'\n')
    m=t/'SHA256SUMS.txt'
    lines=m.read_text().splitlines(True)+additions
    m.write_text(''.join(sorted(lines,key=lambda line:line[66:].encode('utf-8'))))
check('listed nested .git is not excluded', lambda t: add_listed_files(t,['tests/nested/.git/config']), expected=0)
check('UTF-8 spaces and distinct raw Unicode paths', lambda t: add_listed_files(t,['tests/Ќ path.txt','tests/é.txt','tests/e\u0301.txt']), expected=0)
def stale_metadata(t):
    p=t/'zenodo/zenodo_metadata.json'
    d=json.loads(p.read_bytes());d['version']='2.7.7-rc9';p.write_text(json.dumps(d))
check('stale Zenodo metadata version rejected', stale_metadata)
namespace=runpy.run_path(str(source/'tools/ci_inventory_check.py'),run_name='inventory_control')
with patch('os.scandir', side_effect=PermissionError('injected traversal denial')):
    try:
        namespace['inventory'](source)
    except PermissionError:
        results.append({'control':'enumeration errors fail closed (injected)', 'pass':True})
    else:
        raise RuntimeError('enumeration error swallowed')
print(json.dumps({'controls':results, 'outcome':'PASS'}, indent=2))
