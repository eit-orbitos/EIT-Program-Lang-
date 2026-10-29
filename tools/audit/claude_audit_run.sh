#!/usr/bin/env bash
# Claude independent audit runner for V2.7.7 research candidate (V0.3). Usage: audit_run.sh <ENV_LABEL> <PYTHON> <WORKDIR>
# Never modifies the source; each step's command, stdout/stderr and exit code go to the raw log.
set -u
LABEL=$1; PY=$2; W=$3
H=/tmp/claude-0/-home-claude/efdc2a37-fed5-5984-a822-6ad60ecac1dd/scratchpad/v277/handoff
rm -rf "$W"; mkdir -p "$W"/src "$W"/base "$W"/logs "$W"/home
LOG="$W/logs/RAW_${LABEL}.log"
export HOME="$W/home" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8
unset PYTHONPATH PYTHONHOME || true
step () { local name=$1; shift; { echo; echo "### STEP $name"; echo "\$ $*"; } >> "$LOG"; ( "$@" ) >> "$LOG" 2>&1; local rc=$?; echo "EXIT $rc" >> "$LOG"; echo "$name=$rc" >> "$W/logs/EXITS_${LABEL}.txt"; }
{ echo "ENV_LABEL $LABEL"; date -u +%FT%TZ; uname -a; "$PY" -c 'import sys,unicodedata,platform;print(sys.version);print("unidata",unicodedata.unidata_version);print(platform.platform())'; } > "$LOG" 2>&1
cd "$W"
step unzip_candidate unzip -q "$H/SOURCES/ORIGINAL_V277_TASKLET_FIX_CANDIDATE_V0.3.zip" -d src
step candidate_zip_sha256 bash -c "echo 'b73b15c7fed0ca5aa4e5ce33c97888a29ae49f6a96e99b1f37d836d5f945f027  $H/SOURCES/ORIGINAL_V277_TASKLET_FIX_CANDIDATE_V0.3.zip' | sha256sum --strict -c -"
step unzip_baseline unzip -q src/SOURCE_ARCHIVES/OPTION_A_ORIGINAL.zip -d base
step outer_manifest bash -c "cd src && sha256sum --strict -c SHA256SUMS.txt | tail -3"
T="$W/src/V277_TASKLET_FIX_PATCH/successor_tree"
step verifier_pin bash -c "echo '97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca  $T/eit_program_lang/receipt_verifier.py' | sha256sum --strict -c -"
step inner_manifest_strict bash -c "cd '$T' && sha256sum --strict -c SHA256SUMS.txt"
step inventory_check bash -c "cd '$T' && '$PY' tools/ci_inventory_check.py ."
step inventory_negative_controls bash -c "cd '$T' && '$PY' tools/ci_inventory_negative_controls.py ."
step reference_v276_pin bash -c "cd '$T' && echo '3b99157ebf878dff57eba2c6da755720f07f3a80b9c85dd1db0e6a565408e22c  reference/EIT_V2_7_6.zip' | sha256sum --strict -c -"
step venv "$PY" -m venv "$W/venv"
step pip_install_hashes "$W/venv/bin/python" -m pip --isolated install --disable-pip-version-check --no-cache-dir --only-binary=:all: --require-hashes -r "$T/requirements-ci.txt"
step pip_freeze "$W/venv/bin/python" -m pip --isolated freeze --all
step selfcheck_v05 bash -c "cd '$T/tests' && '$W/venv/bin/python' selfcheck_v277_v05.py"
step selfcheck_v06 bash -c "cd '$T/tests' && '$W/venv/bin/python' selfcheck_v277_v06_regressions.py"
step selfcheck_v07 bash -c "cd '$T/tests' && '$W/venv/bin/python' selfcheck_v277_v07_fixes.py"
step pytest_release_modules bash -c "cd '$T' && '$W/venv/bin/python' -m pytest tests/test_receipt_verifier.py tests/test_legacy_v275_fixtures.py -v -p no:cacheprovider"
step pytest_v276_legacy bash -c "cd '$T' && '$W/venv/bin/python' -m pytest tests/v276 -q -p no:cacheprovider"
step regressions_synthetic_only bash -c "cd '$W/src' && '$PY' -B V277_REGRESSION_TESTS/run_regressions.py --mode synthetic-only --execution-authorized --candidate V277_TASKLET_FIX_PATCH/successor_tree --baseline '$W/base/successor_tree'"
step post_run_outer_manifest bash -c "cd '$W/src' && sha256sum --strict -c SHA256SUMS.txt | tail -1"
step post_run_untracked bash -c "cd '$T' && find . -newer '$W/logs/EXITS_${LABEL}.txt' -type f ! -path './.pytest_cache/*' | head -20; echo end"
sha256sum "$LOG" > "$W/logs/RAW_${LABEL}.log.sha256"
cat "$W/logs/EXITS_${LABEL}.txt"
