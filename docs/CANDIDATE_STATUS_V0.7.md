# EIT V2.7.7 — CANDIDATE STATUS V0.7 (SEALED) — RG-5 FIXES F1–F5

**DATE:** 2026-10-23 · **BASIS:** TASKLET_META_AUDIT_RG5_CLAUDE_V0.1 (F1–F5 confirmed) + author instruction "Поправи ги" (EIT_V277_AUTHOR_INSTRUCTION_RG5_FIX_V0.1) · **SPEC:** V0.5.9 untouched

## Fixes applied (verifier bytes changed; builder unchanged)
| Finding | Fix |
|---|---|
| F1 (HIGH) §6.1/H-1/S-4 | L0-failure result no longer performs any key lookup on the receipt (declared=None, no read-back). Hostile-colliding-key probe: no exception on paths 0.3/0.1a/0.1b/0.1c, hostile never called |
| F2 (MEDIUM) §7 1a.1 / OQ-5 | Trigger is length-only (64-char str); non-hex 64-char now reaches 1a.2 → MISMATCH, matching V2.7.6. H-4 hex check retained for anchor arguments |
| F3 (LOW) §9.1a | Q.5 predicate exactly per table (no found/match_count presence condition) |
| F4 (LOW) §5.2 P-7 | G-3 lines emitted in §9.2 written order (single ordered loop) |
| F5 (LOW, spec gap) | **Author option (a)** pending ratification: strict mode, packet mapping without packet_version → POLICY_RECEIPT_VERSION_NOT_ALLOWED (was skipped) |

## Author decisions embedded (ratification requested)
- F1 return value on L0 failure: `receipt_sha256 = None` (Tasklet's recommendation).
- F5: option (a) implemented. Both recorded in SELFCHECK_OUTPUT_V07.log and here.

## Evidence (candidate-only, NOT RG-4)
- selfcheck_v05: 18/18 PASS · selfcheck_v06: 10/10 PASS · selfcheck_v07 (new fix checks): 12/12 PASS.
- Combined artifact-bound log: SELFCHECK_OUTPUT_V07.log.

## Governance
RG-5 = EXECUTED → NEEDS_FIX → V0.7_DELIVERED (Claude re-review + Tasklet V1.3 pin + author addendum pending) ·
RG-4 V1.2 = PASS·COMPLETE on ee20d1ba… (stands as record; superseded for release by the V1.3 re-run) ·
GATE_4 = NOT_SATISFIED · RG-6 = OPEN · FORMAL_FREEZE = NO · GITHUB = HOLD · ZENODO = BLOCKED

**SEAL:** CANDIDATE_V0.7 — F1_F5_FIXED — 18_10_12_ALL_GREEN — AUTHOR_RATIFICATION_PENDING
