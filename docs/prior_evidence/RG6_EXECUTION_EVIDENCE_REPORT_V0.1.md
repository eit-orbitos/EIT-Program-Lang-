# RG-6 — EXECUTION EVIDENCE REPORT — V0.1

Tasklet · 2026-10-24 (runs 15:51–15:56 UTC) · Author authorization: `ledger/EIT_V277_AUTHOR_DECISION_V14_ADDENDUM7_CILOCAL_GO_V0.1.md` (2026-10-24 11:49 GMT-4)
**All runs by Tasklet; not independent.** Same model family as the RG-5 reviewer (Claude). Single environment: Linux x86_64, CPython 3.12.15, unidata 15.0.0, pytest 8.3.3, PYTHONHASHSEED=0.
Unchanged and re-hashed before use: verifier `97b1d148…72ca`, builder `3d401c47…8cec`, companion `4ba6556a…ad65`, spec V0.5.9 `3fc10557…f27c`, ratified V0.6.0 `a753ece9…5788`, V1.3 pins `f868ac6f…a5bdf`.

## 1. RG-4 suite V1.4 (pin list `71030f6a…d59a`, 17 files, `sha256sum -c` OK, byte-identical to the draft)
**1a. Dry fixture build** (row builders only, verifier not called): TX-N1 4 cases, TX-N2a 7, TX-N2b 7 → **18/18 BUILT**, all built-in fixture checks passed. `run_v1_4/DRY_FIXTURE_BUILD.json` (`66389c0c…c9f9`).

**1b. Run** (`run_rg4.sh`, exit 0; outputs `run_v1_4/out/`, `SHA256SUMS_OUT.txt` `4211c016…59f4`, outcomes `4bf37328…c4`):
| Group | Result |
|---|---|
| 123 spec rows | 121 PASS · 1 NOT_APPLICABLE (S4d) · 1 RISK_PRESENT (K1) · 0 FAIL · 0 HARNESS_ERROR · 0 NOT_RUN |
| 21 TX rows (18 from V1.3 + TX-N1, TX-N2a, TX-N2b) | 21 PASS |
| T9-INVENTORY | PASS (123 spec ids) |
| V2.7.6 dual items | 70 PASS (fail-first / control demonstrations) |
| Existing tests | V2.7.6 tree 33 passed · V2.7.7 working copy 35 passed |
| Z1 (no mutation) | 379 checks, 0 violations |
- Compared with V1.3: **no row outcome changed**; only the 3 new rows were added, all PASS. 392 cases (374 + 18).
- PASS means these cases are satisfied by these bytes; not general correctness.

## 2. Mutation re-run (Claude `tools/mutate.py` `a515b9b1…5167`, unchanged; 61 mutants on the V1.4 stage)
- Attempt 1 was interrupted by the sandbox after M47 (background process ended); log kept (`mutate_attempt1_interrupted.log`). Attempt 2 ran complete from scratch.
- **V1.4 suite: 60/61 killed, 0 pattern errors. Survivor: M43.**
- Status changes vs V1.3: **M36 killed by TX-N2a, M55 killed by TX-N2b, M61 killed by TX-N1** — each killed only by its new row. No other mutant changed status. K1 stayed RISK_PRESENT in all mutants.
- Files: `run_v1_4/mutation/mutation_results_v14.json` (`d2dbe743…16d6`), `mutate.log` (`fed619cd…a3f`).
- Limit: the 61 mutants are hand-chosen, not the full mutation space.

## 3. TX-M43 (Addendum 7; supplemental; S4d stays NOT_APPLICABLE)
- Pre-registered proposal `RG6_M43_TEST_PROPOSAL.md` (`5ebb0fe3…22d6`); expectations unchanged.
- **V0.1 = HARNESS_ERROR (Tasklet authoring defect):** stray `+` on line 1; crashed before hash check or import; no result. Kept as `tx_m43_V0.1_DEFECTIVE.py` (`12e864b4…2dbb`).
- **V0.2** (`483b16e1…2475`, one character removed, pinned 15:53:47 UTC) on pinned verifier: **PASS 4/4** (a, b, c, d).
- On M43 mutant (`225db49a…b376`, same textual edit as `mutate.py:58`): first attempt HARNESS_ERROR (companion module not beside the mutant — setup, kept on file); with the unchanged companion beside it: **FAIL — a, b, d fail; control c passes → M43 killed by TX-M43.** Observed: 34 emissions → 33 entries with `FAILURES_TRUNCATED` (dedupe gone), exactly as predicted.
- Limit: tests a private class with no contracted interface; evidence about these bytes only.

## 4. CI-local (V0.9 RC `a43ff961…c79a`, `verify.yml` `f5294f7f…84e5`)
Runner `ci_local/ci_local_runner.py` (`990646a8…37e2`): `bash -e` per step, stop on first failure.
| Step | Result |
|---|---|
| checkout@v4, setup-python@v5 | EMULATED (unzip of RC; local CPython 3.12.15) |
| Install pytest 8.3.3 | PASS |
| `sha256sum --strict -c SHA256SUMS.txt` | **PASS — 82/82 OK, exit 0** |
| V2.7.6 reference pin | PASS |
| Candidate self-checks | PASS — 18/18, 10/10, 12/12 |
| pytest (2 files) | PASS — 7 passed |
| **Job** | **PASS** |
- RC contains `receipt_verifier.py` = `97b1d148…` (both names). The RC's own `tests/CI_LOCAL_RUN.log` (exit 1, pytest NOT RUN) stays stale inside the RC; this run supersedes it as evidence but does not change the RC.
- **This is not GitHub Actions.** It evidences N-8(b) `--strict` execution locally only. N-8(a) (no inventory step), N-8(d) (`ubuntu-latest`, tag pins, no `--require-hashes`), N-8(e) (no `persist-credentials: false`) are unchanged by running CI.

## 5. Not executed
§7 kill tests — BLOCKED_ON_INPUT (`test_v277_proposed.py` absent). Audit mutants M1/M6/M10/M12/M13/M15/M16 — no V2.7.7 evidence.
