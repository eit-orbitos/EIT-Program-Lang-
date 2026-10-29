# RC10 CI-LOCAL EVIDENCE

Tasklet · 2026-10-24 · **Local reproduction, not GitHub Actions.** Not independent.
Input: rc10 ZIP `f6f28e3a…c4b0`, extracted fresh. Runner: same harness as for V0.9, `rg6/ci_local/ci_local_runner.py` `990646a8…37e2` (unchanged). Fresh Python venv without pytest (so the hash-pinned install really downloads and checks). CPython 3.12.15, Linux x86_64.

## Job result: **PASS** (`ci_local_out/CI_LOCAL_RESULT.json` `62719576…0387`)
| # | Step | Result |
|---|---|---|
| 0–1 | checkout (SHA-pinned), setup-python (SHA-pinned) | EMULATED (unzip; local interpreter) |
| 2 | Inventory check | PASS — `INVENTORY_OK: 85 files, all listed, none missing` |
| 3 | Inventory self-test | PASS — stray `.gitkeep` detected (`INVENTORY_FAIL` inside, step exit 0) |
| 4 | `pip install --require-hashes -r requirements-ci.txt` | PASS — installed iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pytest 8.3.3 |
| 5 | `sha256sum --strict -c SHA256SUMS.txt` | **PASS — 85/85 OK** |
| 6 | V2.7.6 reference pin | PASS |
| 7 | Self-checks | PASS — 18/18, 10/10, 12/12 |
| 8 | pytest | PASS — 7 passed |

## Negative controls (`negative_controls/`)
| Control | Expected | Observed |
|---|---|---|
| NC1 wrong wheel hash in requirements | pip refuses | exit 1, "DO NOT MATCH THE HASHES" |
| NC2 requirement without hash under `--require-hashes` | pip refuses | exit 1 |
| NC3 stray `tests/.gitkeep` in the release tree, full job | job FAIL at inventory, later steps skipped | job FAIL at step 2; steps 3–8 SKIPPED (`NC3_out/CI_LOCAL_RESULT.json` `05f5d3de…648e`) |
| NC4 static workflow check | no `latest`; 40-hex action SHAs; `persist-credentials: false`; `--require-hashes`; inventory first | all true |

## What this evidences and what it does not
- N-8(a): executed locally, positive and negative. N-8(b): executed locally (85/85). N-8(d): hash-pinned install executed locally (with refusals); runner label and action SHAs **static only**. N-8(e): **static only** — credential persistence is GitHub checkout behaviour and cannot be observed locally.
- Only a real GitHub Actions run can show the pinned actions, runner and credential setting in operation. GitHub = HOLD; such a run needs a separate author decision.
