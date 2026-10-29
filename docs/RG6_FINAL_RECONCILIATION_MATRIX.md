# RG6 final reconciliation matrix — RC11 preparation

Tasklet · 2026-10-24 · Ratified V0.6.0 exact hash `a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788`.

**Recommendation: KEEP_RG6_OPEN.** Every row below uses one of the commissioned categories. A technical OPEN residual can have an accepted LIMITED-only treatment; that is not technical closure and does not override B4 or other gates. Named author closures are preserved. No new final ClaimState, RG6 closure or author risk decision is assigned.

| §13 item | Category | Failure mode / affected scope | Evidence, acceptance boundary and mitigation |
|---|---|---|---|
| N-1 source-side selection | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | order-dependent silent source selection; runtime query users | Ratified §13 rationale only, not a new runtime fix; advisory result and future query-path fix; B4 causality/§12 R-2 overlap remains globally blocked below |
| N-3 malformed restored state | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | query-path exception / denial | Ratified §13: fail-closed denial, caller validates state; no technical fix claimed |
| N-4 canonicalization/index | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | serialization collisions and insertion-order index | Ratified §13, verifier L0 constraints and H-6; R-1/R-4 remain disclosed; independent anchors required; no broad runtime repair |
| N-5 symbol_id lookup normalization | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | runtime NFD/NFC lookup misses | Ratified §13; preserve raw identifiers, disclose, fix only in future scoped query work |
| N-6 None rendering | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | misleading runtime surface | Ratified §13 teq/rejection rationale; disclose, not physical correctness |
| N-7 aliasing | ACCEPTED_LIMITATION_FOR_LIMITED_RELEASE | caller mutates aliased runtime result/state | Ratified §13; caller copies before mutation. Earlier V1.4 includes Z1 no-mutation evidence, not a caller-aliasing fix; source historical note is preserved unchanged |
| N-8(a) inventory | OPEN_BLOCKING | unlisted files/cache or missing required release files | RC11 exact root membership, required paths, cache/symlink rejection and negative controls; candidate-bound local result external; real checkout execution/author disposition not supplied |
| N-8(b) strict hash evidence | CLOSED_EVIDENCE | weak or absent strict pin execution | Author LOCALLY EVIDENCE-SATISFIED only; V0.9 82/82, rc10 85/85; **NOT GitHub Actions evidence**. No widening of author closure |
| N-8(d) environment/dependency lock | OPEN_BLOCKING | supply-chain drift / different environment | Exact action commits read-verified, Python patch fixed, explicit hashed wheel lock; local result external. Runner image label still moves; action execution not demonstrated on GitHub; no author acceptance of remaining residual |
| N-8(e) credential persistence | OPEN_BLOCKING | checkout credentials left available | `persist-credentials: false` and read-only contents permission present; GitHub behavior unobserved |
| N-9 | DEFERRED_NONBLOCKING_FOR_LIMITED_RELEASE | same surface/different meanings auto-resolved by runtime | Ratified §13 expressly OUT OF SCOPE/not reconciled; original audit description inspected, not rerun; not fixed or PASS; any demonstrated forged acceptance triggers B4 |
| N-10 | DEFERRED_NONBLOCKING_FOR_LIMITED_RELEASE | lower/upper misses casefold equivalents, e.g. straße/strasse | Same explicit §13 scope treatment, no additional acceptance or future waiver; no runtime lookup change |
| N-11 | DEFERRED_NONBLOCKING_FOR_LIMITED_RELEASE | stale V2.7.6 report workflow hash, overstated fixture upgrades, reconstructed continuity table | Same explicit §13 scope treatment; historical inaccuracies preserved, not recast as current RC11 execution evidence |
| N-12 | DEFERRED_NONBLOCKING_FOR_LIMITED_RELEASE | duplicated helpers and constant SAFETY_BLOCK intent mistaken for measurements | Same explicit §13 scope treatment; no scientific, measured-boundary or functional validation claim |
| D-1 survivor-count record | CLOSED_EVIDENCE | “eight” vs seven in original audit prose/table | Ratified record corrects count to seven, M16 double-counted; original audit bytes unmodified; current documentation includes correction |
| Audit M1 | OPEN_BLOCKING | history fallback may serve pre-frozen state | Technical OPEN; §13 caller frozen-state-only obligation. Conditional reconciliation permitted, but no sufficient B4-specific disposition established; not unconditional requirement to kill mutant |
| Audit M6 | OPEN_BLOCKING | state/receipt served without state hash | Technical OPEN; reject state missing hash; same unresolved B4 sufficiency boundary |
| Audit M10 | OPEN_BLOCKING | tampered state served as matching | Technical OPEN; caller rejects mismatch; verifier-side anchor checking does not prove runtime serving fixed |
| Audit M12 | OPEN_BLOCKING | NFD/NFC index misses | Technical OPEN; index/runtime path deferred; no original kill-test execution established, conditional B4 reconciliation uncompleted |
| Audit M13 | OPEN_BLOCKING | wrong-provenance packet served | Technical OPEN; verifier independently checks receipt-side consequence; original runtime mutation remains unresolved for B4 disposition |
| Audit M15 | OPEN_BLOCKING | incomplete receipt served | Technical OPEN; verifier required-field checks do not establish serving-path fix; reconciliation/B4 evidence insufficient for nonblocking assignment |
| Audit M16 | OPEN_BLOCKING | integrity battery misses in-place tamper | Technical OPEN; independent state verification obligation; no new battery evidence |
| RG-5 M36 | CLOSED_EVIDENCE | stamp-sensitive role normalization | Author scope-limited closure: `rows_rg5r.py::tx_n2a` / TX-N2a on pinned candidate |
| RG-5 M55 | CLOSED_EVIDENCE | typed NaN equality | Author scope-limited closure: same file `tx_n2b` / TX-N2b; stricter mutant killed, not broad security validation |
| RG-5 M61 | CLOSED_EVIDENCE | L4 failure-reporting omission | Author scope-limited closure: same file `tx_n1` / TX-N1 |
| RG-5 M43 | CLOSED_EVIDENCE | collector deduplication | Author CLOSED WITH LIMITATION: separate TX-M43 V0.2, private class; V1.4 remains 60/61 |
| §7 audit test-evidence track | OPEN_BLOCKING | no located original test_v277_proposed.py or execution on this candidate | Not an unconditional standalone LIMITED prerequisite in §13; no explicit blanket exemption either. Original seven named tests found in audit, not original script. Block is unresolved per-item/B4 evidence, not an invented obligation to execute every original test. Overlapping §11 tests remain required by Gate-4. No substitute fabricated |
| B4-0 / §13 / §14A(6) | OPEN_BLOCKING | uncertain boundary between accepted §12 behaviour and forged acceptance caused by OPEN items | R-5 K1 retained verified=True; analysis-only no-additional-path statement is not exhaustive proof or author interpretation. See B4 final record; decision not made |

## Gate interpretation

**RELEASE_BLOCKED_BY_GOVERNANCE.** §14A(4) mandatory applicable test evidence and §14A(5) independent reproduction remain requirements. The LIMITED amendment changes only gate 6. It supplies no permission to publish with Gate-4 NOT_SATISFIED and no independent reproduction. Phase 1 OPEN is also retained, not deemed closed or waived. Passing the local release job does not settle overall Gate-4.

N-1…N-7 categories above describe the ratified LIMITED reconciliation, subject to the unresolved global B4 blocker, not a new blanket author acceptance. The audit-mutant OPEN_BLOCKING assignments are conservative evidence insufficiency for current reconciliation, not proof those runtime issues all cause forged verification. If sufficient author interpretation/evidence later supports LIMITED-only acceptance, change category only through a new add-only decision record; never rewrite technical history.

Current state: V0.5.9 IMMUTABLE; V0.6.0 RATIFIED; RG6 OPEN; PHASE_1 OPEN; GATE_4 NOT_SATISFIED; independent runtime reproduction unfulfilled; FORMAL_FREEZE NO; GITHUB HOLD; ZENODO BLOCKED.
