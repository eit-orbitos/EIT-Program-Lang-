# RC11 — Current limitations and author dispositions

This current summary supplements, and does not rewrite, historical reports carried in `docs/`. Exact ratified §12/§13 text is reproduced in `docs/RELEASE_GOVERNANCE_RC11.md`; current per-item categories are in `docs/RG6_FINAL_RECONCILIATION_MATRIX.md`.

## Scope-limited author closures (2026-10-24)
- M36 CLOSED: `rows_rg5r.py`, TX-N2a; normalization cases on pinned verifier.
- M55 CLOSED: same file, TX-N2b; non-finite typed equality cases, not general security validation.
- M61 CLOSED: same file, TX-N1; packet-version/L4 reporting cases.
- M43 CLOSED WITH LIMITATION: `rg6/tx_m43/tx_m43.py`, TX-M43 V0.2; private class, no contracted public interface. Candidate 4/4 PASS; mutant 3 FAIL and control PASS.
- N-8(b) LOCALLY EVIDENCE-SATISFIED, explicitly NOT GitHub Actions evidence.
- RG-4 / V1.4 PASS · COMPLETE: 121 spec PASS, S4d NOT_APPLICABLE, K1 RISK_PRESENT; separate TX 21 PASS. V1.4 mutations 60/61, with supplemental TX-M43 kept separate.

These earlier executions are Tasklet-run, not independent runtime reproduction. S4d is not retroactively converted into an executed pass by the private-class supplemental test. Original reports remain historical snapshots.

## Open risk and release boundaries
R-1…R-6 remain disclosed in NON_CLAIMS. R-1 index hash, R-2 query/source replay, R-3 keyless rewrites and R-5 downgrade can allow receipts to pass within expressly limited checking semantics; a PASS is not authenticity. K1 concretely recorded `verified=True` and ARTIFACT_AND_STATE_ANCHORED for a downgraded forged target-selection receipt. No mitigation of that path is claimed.

N-1 source selection, N-3 malformed-state query behavior, N-4 canonicalization/runtime index, N-5 lookup normalization, N-6 None rendering and N-7 result aliasing are not fixed by RC11. Follow the ratified caller obligations; no blanket “blocks nothing” statement is made. N-8(a)/(d)/(e) have release-layer controls in RC11, but real GitHub execution remains unavailable and author disposition is not silently assigned.

Audit-series M1/M6/M10/M12/M13/M15/M16 remain OPEN in technical terms, separate from RG-5 numbering. §7 tests have no new PASS attributed here; absence of the original missing script is not permission to fabricate an equivalent and call it original. See final matrix for governance blocker interpretation.

RC11's local job is narrower than RG-4. It executes frozen self-checks plus two pytest modules, not all project/audit suites. Exact candidate-bound output is external to the canonical source tree to avoid circular evidence hashes or post-test source changes. Prior `tests/CI_LOCAL_RUN.log` remains historical, not RC11 evidence.

`ubuntu-24.04` floats in image revision. CPython patch is fixed to 3.12.15 but GitHub tool availability is not demonstrated. The venv's bootstrapped pip is recorded, not claimed as a separately hash-locked runtime. Exact dependency wheels are hash-enforced and all pip-installed dependency entries are explicit. Action ref existence is not an upstream code audit or executed GitHub behavior.

Builder-backed fixtures have producer-provenance limits. Single-environment checks and same-model review do not establish cross-platform equivalence or independent reproduction. Historical Q4/D-6 behavior and out-of-scope runtime paths are not altered.

## Release status
RG6 OPEN · PHASE_1 OPEN · GATE_4 NOT_SATISFIED · FORMAL_FREEZE NO · GITHUB HOLD · ZENODO BLOCKED. No B4 author decision is inferred from this package. SOFTWARE / DOCUMENTARY VALIDATION ≠ PHYSICAL LAW ≠ EXTERNAL SCIENTIFIC VALIDATION.
