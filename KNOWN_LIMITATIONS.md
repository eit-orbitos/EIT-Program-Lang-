# KNOWN LIMITATIONS — EIT V2.7.7 Research Candidate R2

**RESEARCH_CANDIDATE — NOT FINAL — KNOWN BLOCKERS LISTED**

This file supplements the historical documents in `docs/` and does not rewrite them. The RC11 version of this file is kept as `docs/historical_rc12/KNOWN_LIMITATIONS_RC11.md`, and everything it lists still applies. The complete machine-readable register is `docs/audit/REMAINING_BLOCKERS_V2_7_7.json`.

## 1. Status constants (none are closed by this package)
FINAL_V277_RELEASE = HOLD · C3_E = NOT_IMPLEMENTED · F01 = 0/19 OPERATIONALLY_VERIFIED · B4 = NOT_CLOSED · RG6 = OPEN · GATE_4 = NOT_SATISFIED · PHASE_1 OPEN · FORMAL_FREEZE NO.

## 2. Verifier-semantics risks (by design, disclosed)
- **R-1:** index hashes are not authenticated.
- **R-2:** the query and source resolution are not replayed.
- **R-3:** a keyless joint rewrite of artifact and receipt passes.
- **R-5:** a stamp downgrade passes.

R-1, R-2, R-3 and R-5 can each yield `verified=True`. K1 recorded `verified=True` and `ARTIFACT_AND_STATE_ANCHORED` for a downgraded forged target-selection receipt, and no mitigation is claimed. R-4 and R-6 also remain, as stated in `NON_CLAIMS.md`.

An independent review (Kimi, of V0.3) found that **22 of 23 source routes can be bypassed without the Separate-UID broker**. Its production verdict was NOT_READY; its research verdict was ELIGIBLE_WITH_REQUIRED_DISCLOSURES.

## 3. Findings of the 2026-10-29 Claude audit (`docs/audit/CLAUDE_AUDIT_V2_7_7.md`)
- **Oracle conflict (preserved).** `test_builder_envelope_overrun_and_runtime_smaller_envelope` fails ("S1ResolutionError not raised"). The V0.3 suite result is 50 PASS + 1 FAIL out of 51. According to the static path accounting, the original oracle expects behaviour that the pinned fixture does not produce. Correcting it is NEEDS_AUTHORIZATION, and no test-specific workaround was applied.
- **§2 deviation.** `receipt_verifier.py` defines its own `sha256_json` and does not call the existing `restored_query_receipt.sha256_json`. The two give identical output on every probed input, but the normative "MUST call the existing function" is not met. No P0-03 patch is claimed.
- **Test coverage.** The §11.3 (24 controls) and §11.4 (99 adversarial rows) tables are **not** in the tree as executable row-by-row tests. Claude's independent probe covers 100 checks taken from the spec text, and that coverage is partial and not authoritative. The historical RG-4 V1.4 suite (121 PASS) was sealed outside the tree and not re-run.
- **Regression runner and R1.** The V0.3 regression runner pins the exact V0.3 inventory and correctly refuses the R1 tree (`BLOCKED_SOURCE_INTEGRITY`). The 50+1 result applies to the V0.3 bytes and carries over to R1 by code hash identity only.
- **Historical Q4/D-6 behaviour** (the declared versus the recomputed `receipt_sha256`) is unchanged and was not re-adjudicated.
- **Original 64-record register missing.** `FINAL_BLOCKER_MATRIX_V0.1.json` (SHA-256 reported as `1c2b4fe5…88c9`, 143163 bytes) was not supplied. The 55 BLOCKED rows here are a **derived extract**, not the original register. The 9 previously VERIFIED rows are **reported only, not re-verified**.
- **AUD-06 documentary exclusion in R2.** Exactly six historical documents with concrete Tasklet sandbox thread paths were excluded from R2 under scoped author approval. They remain unchanged in preserved R1 custody, not in the public-candidate tree. Historical references are retained and may refer to excluded R1-only files. See `docs/release/R2_AUD06_PUBLIC_EXCLUSIONS.md`.
- **Research Preview V0.1** cannot be reconciled with V0.3: 70 candidate files are missing and 2 files differ. It must not be released.

## 4. Reproducibility profile
- Exactly CPython 3.12.15 with Unicode 15.0.0. Python 3.13 (Unicode 15.1.0) is refused by the regression runner, and that refusal is correct behaviour.
- Two environments in one cloud container family (root, and a separate non-root UID) do not demonstrate cross-platform equivalence.
- GitHub Actions has **NOT_RUN** on these bytes. A future GitHub Actions PASS is CI evidence only, not evidence about an owner-bound OS or isolated host (see `docs/audit/PHASE_A_GITHUB_ACTIONS_PLAN.md`).
- The runner label `ubuntu-24.04` does not pin an immutable image. The action SHAs are pinned but were not executed here.

## 5. Remaining blockers — 55 derived rows, all BLOCKED

Gate counts: RG6 31, IR04-P 20, IR04-O 20, F01 19, B4 16, GATE4 11, PUBLICATION 3.

- F01-01
- F01-02
- F01-03
- F01-04
- F01-05
- F01-06
- F01-07
- F01-08
- F01-09
- F01-10
- F01-11
- F01-12
- F01-13
- F01-14
- F01-15
- F01-16
- F01-17
- F01-18
- F01-19
- IR04-P
- IR04-O
- N-1
- N-5
- N-6
- N-7
- M6
- M13
- M15
- B4-FORGED-ACCEPTANCE
- SCHEDULE-B-B1-A-D
- C3E-CONSUMER-BINDINGS
- CE-10A-STAMPS
- CE-10B-C5
- C3E-BYPASS-ROLLBACK
- B4-CLOSURE-AUTHORITY
- S13-N-3
- S13-N-4
- S13-N-8
- S13-N-9
- S13-N-10
- S13-N-11
- S13-N-12
- S13-M1
- S13-M10
- S13-M12
- S13-M16
- 14A-1
- 14A-2
- 14A-3
- 14A-4
- 14A-5
- 14A-6
- FORMAL-FREEZE
- GITHUB-PUBLISH
- ZENODO-PUBLISH

Full text per row: `docs/audit/REMAINING_BLOCKERS_V2_7_7.md`. Plus audit findings AUD-01 … AUD-13 listed there.

SOFTWARE / DOCUMENTARY VALIDATION ≠ PHYSICAL LAW ≠ EXTERNAL SCIENTIFIC VALIDATION.


## R2-specific status (2026-10-29)

Tasklet independently replayed the exact **R1** archive and reported `REPLAY_MATCH`: R1 shared CI PASS; V0.3 synthetic regressions 50 PASS + 1 FAIL; R1 original-runner rejection (`BLOCKED_SOURCE_INTEGRITY`); conformance probe 99 PASS + 1 FAIL; legacy probe ALL_PASS. These are NOT R2 execution results. The R2 ZIP and root manifest differ from R1 because of approved AUD-06 exclusions and release-layer metadata; independent R2 test replay is `NOT_RUN`. No technical/gate closure and no publication authorization are implied.
