# B4 final evidence record — RC11 preparation

Author / Founder / Architect: Mr. Toni Mladenovski. Tasklet · 2026-10-24.

**B4_STATUS = ANALYSIS_ONLY**  
**B4_CLAIM = NO_ADDITIONAL_PATH_IDENTIFIED_IN_REVIEWED_SCOPE**  
**B4-0 = OPEN_BLOCKING · AUTHOR_DECISION_NOT_MADE**

“Final” means this commission's evidence record, not final gate satisfaction. No new B4 experiment or exhaustive forged-receipt search is claimed. Earlier stored execution and current code-reading are distinguished below. Closed RG-5 findings remain closed in their author-approved test scope.

## Governing text

Ratified V0.6.0 DRAFT V0.5 SHA-256 `a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788`, §13: if failure of an item could make the verifier return `verified=True` for a forged receipt, it remains blocking for any release. §14A(6) requires complete per-item reconciliation and a recorded B4 check. §12 retains R-1/R-2/R-3/R-5 non-authenticity behaviours. No explicit “additional beyond §12” exception is silently inserted here.

Pinned verifier SHA-256: `97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca`. Source reading found no `index_sha256` verification and no `_resolve_source` replay. Lines 306–307 select legacy from self-declared stamp; 389–394 implement external-anchor presence/comparison; 757 computes `verified = (col.occurred == 0)`; 761 assigns CONSISTENCY_ONLY in the unanchored success case. These are static observations, not execution of each exploit.

## Required path table

“Counter-example” here means a path contradicting an unrestricted authenticity/no-forged-PASS claim. It does NOT automatically establish a newly discovered causal B4 violation of a specific OPEN §13 item. A NO means no new executed counterexample was found in this review, not proof of absence.

| Risk | Input / control path | Expected behaviour under pinned semantics | Can forged claims reach verified=True? | Evidence type | Counter-example found? |
|---|---|---|---|---|---|
| R-1 | Alter self-declared index_sha256; reseal receipt hashes; keep required grounded fields consistent. Control: change hashed content without resealing | Resealed index claim is not authenticated; unresealed content fails receipt hash | YES for an otherwise conforming resealed receipt; index truth is not checked | CODE_READ + §12 ANALYSIS; no fresh R-1 exploit execution | NO new executed case; documented positive possibility already explicit |
| R-2 | Claim NO_MATCH for a real symbol with consistent empty result, or name a genuine record not actually selected by the claimed query. Control: violate required cross-field/grounding constraints | Internal consistency/grounding do not replay the original query/source intent; inconsistent fields are rejected | YES is expressly within §12's non-replay limitation; not every arbitrary forgery is accepted | CODE_READ + §12 ANALYSIS; no fresh R-2 exploit execution | NO new executed case; documented positive possibility already explicit |
| R-3 | Attacker rewrites artifact and receipt jointly, recalculates all binding/hash fields, default mode without trusted anchor. Control: supply independently pre-established different artifact hash, or strict mode without anchor | Default may give CONSISTENCY_ONLY; independent mismatching anchor rejects, missing strict anchor rejects | YES under no-authenticity/default assumptions. A self-computed “anchor” does not mitigate this | CODE_READ A.1/A.2 + §4.5/§12 ANALYSIS; retained suite evidence is supporting, not a new exploit run | NO new executed case; by-design acceptance documented |
| R-5 | K1: forged target-selection receipt downgraded consistently to 2.7.4, supplied with matching artifact and state anchors. Control: current-stamp target-resolution rules | K1 records risk instead of failing the suite; stamps and hash anchors do not attest producer/runtime version | **YES — stored K1 observed verified=True, no failures, ARTIFACT_AND_STATE_ANCHORED** | **EXECUTION (earlier retained V1.4 K1 record)** + source reading; not newly rerun | **YES, retained known-risk case** against blanket no-forged-PASS/authenticity claim; not a newly discovered path |

K1 source: `rg4/suite_v1_4/rows_adversarial.py::k1` in thread `a_03tszwf78edg4fzaxgk0`, lines 1259 onward. It calls `forge(r2_forgery(f), m)` then verifies with both matching expected hashes. Result: `rg4/run_v1_4/out/rg4_outcomes.json`, K1/v277. Exact output/suite hashes are in the copied pre-closure evidence appendix. Prior source output checksum rechecks were 15/15; suite 17/17. The evidence was Tasklet-run, not independently reproduced.

## What is and is not established

- R-1/R-2/R-3/R-5 are not made universally safe by disclosure or an author decision. R-5 is explicitly unmitigated in §12. R-4/R-6 also remain disclosed; this table does not erase them.
- A trusted external anchor mitigates joint content substitution relative to that reference, not producer identity, query truth or stamp authenticity.
- The closed M36/M55/M61 tests and supplemental M43 establish their named behaviours on exact bytes. M55's stricter rejection mutation is not evidence of a forged-acceptance bug. V1.4 remains 60/61; M43 is separate.
- §13's runtime/process generalization cannot be used for the RG-5 verifier mutations without item-specific evidence. Those named defects now have author closures, but other interactions are not exhaustively excluded.
- No original §7 script or new audit-mutant execution is supplied here. The original audit's test descriptions do not establish performed tests. Process-side N-8 failures can change delivered/executed bytes even though they do not change the pinned function mathematically.

## Author decision input — not a prefilled acceptance

The commissioned question was: “Based on the recorded evidence, does the author accept that the documented by-design R-1/R-2/R-3/R-5 paths do not provide an unmitigated path for a forged receipt to obtain verified=True within the pinned verifier's defined scope?”

**Do not answer that proposition as an established fact:** §12 and K1 retain positive, unmitigated acceptance behaviours. A more precise decision is needed:

> For §13/§14A(6), what is the intended scope of “forged receipt” and its causal link to an OPEN item, given the acceptance behaviours retained by §12 R-1/R-2/R-3/R-5? For each relevant path, record whether it triggers B4 or is outside its scope, the exact threat/anchor/caller boundary, the evidence required, and whether the residual risk is accepted for LIMITED release. Do not describe an accepted residual as mitigated. If the proposed boundary changes rather than interprets the binding rule, require a separately reviewed amendment.

Until this reconciliation is recorded and sufficient, **KEEP_RG6_OPEN**. This record does not make that author decision, close other gates or authorize release.
