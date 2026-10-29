#!/usr/bin/env bash
# One shared local/GitHub CI entrypoint. Evidence and virtualenv stay OUTSIDE the tree.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8
unset PYTHONPATH PYTHONHOME || true
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
PYTHON=${RC11_PYTHON:-python3}
WORK=$(mktemp -d "${RUNNER_TEMP:-/tmp}/eit-rc11-ci.XXXXXXXX")
trap 'rm -rf "$WORK"' EXIT
echo 'STEP: exact interpreter profile'
"$PYTHON" -c 'import sys,unicodedata,platform; print(sys.version); print(platform.platform()); print("unidata",unicodedata.unidata_version); assert sys.version_info[:3] == (3,12,15), "requires CPython 3.12.15"'
echo 'STEP: initial inventory'
"$PYTHON" tools/ci_inventory_check.py .
echo 'STEP: initial canonical hash check'
sha256sum --strict -c SHA256SUMS.txt
echo 'STEP: clean dependency install'
"$PYTHON" -m venv "$WORK/venv"
"$WORK/venv/bin/python" -m pip --isolated install --disable-pip-version-check --no-cache-dir --index-url https://pypi.org/simple --only-binary=:all: --require-hashes -r requirements-ci.txt
"$WORK/venv/bin/python" -m pip --isolated check
"$WORK/venv/bin/python" -m pip --isolated freeze --all
echo 'STEP: dependency negative controls'
"$PYTHON" - "$WORK" <<'PY'
from pathlib import Path
import sys,re
p=Path('requirements-ci.txt').read_text()
d=Path(sys.argv[1])
(d/'bad.txt').write_text(re.sub(r'sha256:[0-9a-f]{64}', 'sha256:'+'0'*64, p, count=1))
(d/'missing.txt').write_text(re.sub(r' --hash=sha256:[0-9a-f]{64}', '', p, count=1))
PY
for control in bad missing; do
  if "$WORK/venv/bin/python" -m pip --isolated download --disable-pip-version-check --no-cache-dir --index-url https://pypi.org/simple --only-binary=:all: --require-hashes -r "$WORK/$control.txt" -d "$WORK/wheels-$control" > "$WORK/$control.log" 2>&1; then
    cat "$WORK/$control.log"; echo 'NEGATIVE_CONTROL_FAIL: dependency rejection missing'; exit 1
  fi
  cat "$WORK/$control.log"
  if [ "$control" = bad ]; then grep -q 'DO NOT MATCH THE HASHES' "$WORK/$control.log"; else grep -q 'Hashes are required' "$WORK/$control.log"; fi
  echo "NEGATIVE_CONTROL_PASS: dependency $control"
done
echo 'STEP: inventory and digest negative controls'
"$PYTHON" tools/ci_inventory_negative_controls.py .
echo 'STEP: V2.7.6 reference archive pin'
echo '3b99157ebf878dff57eba2c6da755720f07f3a80b9c85dd1db0e6a565408e22c  reference/EIT_V2_7_6.zip' | sha256sum --strict -c -
echo 'STEP: frozen candidate self-checks (NOT RG-4 suite)'
(
  cd tests
  "$WORK/venv/bin/python" selfcheck_v277_v05.py
  "$WORK/venv/bin/python" selfcheck_v277_v06_regressions.py
  "$WORK/venv/bin/python" selfcheck_v277_v07_fixes.py
)
echo 'STEP: pytest (two release test modules only)'
"$WORK/venv/bin/python" -m pytest tests/test_receipt_verifier.py tests/test_legacy_v275_fixtures.py -q -p no:cacheprovider
echo 'STEP: final inventory and canonical hash check'
"$PYTHON" tools/ci_inventory_check.py .
sha256sum --strict -c SHA256SUMS.txt
echo 'LOCAL_OR_GITHUB_SHARED_CI=PASS (execution environment recorded externally)'
