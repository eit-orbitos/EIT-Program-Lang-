# KIMI — RG-4 V1.2 PASS·COMPLETE — REGISTRATION V0.1

**DATE:** 2026-10-23 · **SOURCE:** TASKLET RG4_RUN_V1_2_REPORT.md (verified in Kimi container)

## Independent verification performed here
- Outputs zip: 21,556 B — SHA-256 `5ac4d02143a26168ca5c84dec042ae78f258e8a328d8af4d9c0862f15f4f1930` — EXACT MATCH, CRC PASS, 18 hash-bound entries (pin check, stage, fixtures, outcomes JSON, both SHA256SUMS).
- Report hash computed: 11123bc328bdd8a7b3a5… (no external claim to compare; recorded).

## Result
- 123 spec rows: 121 PASS · 1 NOT_APPLICABLE (S4d, Addendum 3) · 1 RISK_PRESENT (K1, accepted) · 0 FAIL / 0 HARNESS_ERROR / 0 NOT_RUN.
- All 22 V1 failures now pass (NC12=C-1, X6b/PR1=C-2, D4=C-3).
- Evidence-about-tests: 45/45 fail-first fail on V2.7.6; 24/24 controls pass; 33/33 existing on V2.7.6; 35/35 on isolated V2.7.7 with ee20d1ba….
- Invariants: Z1 316/316 clean; result contract 319/319 clean; 0 escaped exceptions.
- TX extras 7/7 incl. TX-BLD (builder hashes == V2.7.6 hash function).

## Honest limits (Tasklet's, accepted)
- Suite written by Tasklet alone; PASS ≠ proof of correctness.
- Builder-backed rows = candidate-builder provenance (my builder), not independent evidence.
- S4d duplicate-stream untested against implementation.
- D-6/G-07 open: declared non-str receipt_sha256 returned as-is (matches V2.7.6).
- Single environment; RG-5 not run.

## Status
RG-4 = PASS · COMPLETE (V1.2, ee20d1ba…) · GATE_4 = NOT_SATISFIED pending author decision ·
RG-5 = NOT_RUN (repeatability; same-author limitation) · RG-6 = OPEN · FORMAL_FREEZE = NO ·
GITHUB = HOLD · ZENODO = BLOCKED

**SEAL:** RG4_PASS_COMPLETE — EVIDENCE_VERIFIED — GATE4_AUTHOR_DECISION_PENDING
