# CLAUDE_AUDIT_V2_7_7 — NOVA Q / EIT V2.7.7 Research Candidate audit

**Auditor:** Claude (Anthropic), model configuration `claude-opus-5-5`. **Date:** 2026-10-29.
**Directive:** "GO — NOVA Q / EIT V2.7.7 RESEARCH CANDIDATE AUDIT", Track 1 and Track 2 Phase A.
**Primary reference:** `ORIGINAL_V277_TASKLET_FIX_CANDIDATE_V0.3.zip`, SHA-256 `b73b15c7fed0ca5aa4e5ce33c97888a29ae49f6a96e99b1f37d836d5f945f027`.

**Verdict:**
- **V0.3 as delivered:** NEEDS_FIX for release bytes. Its release layer fails its own CI.
- **Proposed R1:** RESEARCH_ELIGIBLE_WITH_REQUIRED_DISCLOSURES, *pending an independent replay and the author's final GO*.
- **Production:** NOT_READY.
- **No gate closed:** FINAL_V277_RELEASE HOLD · C3_E NOT_IMPLEMENTED · F01 0/19 · B4 NOT_CLOSED · RG6 OPEN · GATE_4 NOT_SATISFIED.

**Same-family caveat.** This is a single-vendor audit. The two environments share one cloud container family, so they are *not* independent hardware, and the audit is *not* an independent runtime reproduction in the governance sense.

---

## 1. Custody and hashes

| Item | SHA-256 | Result |
|---|---|---|
| Handoff ZIP `NOVA_Q_V277_CLAUDE_RESEARCH_SOURCE_HANDOFF_2026_10_29.zip` | `43d7e7c8…1884` | received |
| Handoff `SHA256SUMS.txt` (14 entries) | — | 14/14 OK |
| V0.3 candidate ZIP | `b73b15c7…f027` | OK, 166 members |
| V0.3 outer `SHA256SUMS.txt` | — | 164/164 OK, before and after every run |
| Extracted successor tree, 127 files | `2538c8cb…c84c1` | byte-identical to `V277_TASKLET_FIX_PATCH/successor_tree` in V0.3 |
| Option-A original (inside V0.3) | `df60039d…` | separate predecessor, not an alias |
| Spec P0-03 V0.5.9 | `3fc10557…f27c` | OK; matches the verifier header pin |
| Spec V0.6.0 DRAFT V0.5 | `a753ece9…5788` | OK |
| Existing Research Preview V0.1 | `3ec997bb…80e9` | OK, but not reconcilable (§6) |
| Kimi independent review of V0.3 | `03d02657…d55f` | OK |
| C3E isolated host candidate V0.1 | `a497592b…a51` | OK; documentary placeholder |
| `receipt_verifier.py` and its `_v277_candidate` twin | `97b1d148…72ca` | identical in baseline, Option-A and V0.3 |
| Companion `restored_registry_index_v277_candidate.py` | `4ba6556a…ad65` | matches the verifier's internal pin |

**The V0.3 delta against Option-A** matches `SOURCE_DELTA.json` exactly:
- modified: `eit_v277_builder_candidate.py` (`3c1f3ac7…` → `fe305aab…`) and `frozen_translation_lookup.py` (`6b8d649e…` → `6c7bf165…`);
- added: `s1_sp1_adapter.py` and `s1_sp1_core.py`.

No other code changed.

**Finding C-1, release blocker in V0.3, fixed in R1 at the release layer only.** The inner root `successor_tree/SHA256SUMS.txt` was inherited unchanged from Option-A and is stale:
- 3 hash mismatches: builder, frozen_translation_lookup, restored_registry_query;
- 3 files not listed: `lookup_identity.py`, `s1_sp1_adapter.py`, `s1_sp1_core.py`.

As a result, the V0.3 tree's own `tools/ci_release.sh` cannot pass. `ci_inventory_check.py` → INVENTORY_FAIL, and that cascades into `ci_inventory_negative_controls.py` → "control failed: root .git directory explicitly excluded".

**Finding C-2.** The RC12 release docs in the tree (README, CITATION, zenodo, ARTIFACT_REGISTRY) describe RC12, not V0.3. The registry records builder `3d401c47…`, which is not the V0.3 builder `fe305aab…`.

## 2. Two clean environments

CPython 3.12.15 was built from the official tag `v3.12.15` (commit `e848e4b09ca4bc67c0041c9ce7526dae471d4c36`), GCC 13.3.0, glibc 2.39, Unicode 15.0.0. No pre-built 3.12.15 was available, and other interpreters are refused by the project.

| | Env A | Env B |
|---|---|---|
| User | root | separate non-root UID `auditb` (30033), own HOME, own work dir |
| Workdir | fresh, unzip from the original ZIP | fresh, unzip from the original ZIP |
| Env vars | `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8`, `PYTHONPATH` unset | same |

Runner: `tools/audit/claude_audit_run.sh LABEL PYTHON WORKDIR`. Every step's command, output and exit code go into the raw log.

| Step | Env A | Env B |
|---|---|---|
| unzip and SHA-256 of candidate and baseline | 0 | 0 |
| outer manifest (164) | 0 | 0 |
| verifier pin | 0 | 0 |
| **inner_manifest_strict** | **1** (3 FAILED) | **1** |
| **inventory_check** | **1** (3 unlisted) | **1** |
| **inventory_negative_controls** | **1** (cascade) | **1** |
| V2.7.6 reference pin | 0 | 0 |
| venv + `pip --require-hashes` (pytest 8.3.3 lock) | 0 | 0 |
| self-checks v05 / v06 / v07 | 18/18, 10/10, 12/12 | same |
| pytest release modules | 7 passed | 7 passed |
| pytest tests/v276 | 28 passed | 28 passed |
| **regressions (synthetic-only, 51 tests)** | **50 PASS + 1 FAIL** | **identical** |
| post-run outer manifest | 0 | 0 |
| untracked files after the run | none | none |

The exit vectors are byte-identical between A and B (`6a176807…fd9d`), and so are all 51 regression case outcomes.

**The regression FAIL** is `OutputEnvelopeTests.test_builder_envelope_overrun_and_runtime_smaller_envelope`, "S1ResolutionError not raised". It matches V0.3's own `ORACLE_CONFLICT_AND_PATH_ACCOUNTING.json`, classified `ORACLE_CONFLICT_CONFIRMED_BY_STATIC_PATH_ACCOUNTING`:
- the builder receipt has depth 32, which equals the inclusive limit 32;
- `guard_output` rejects depth > 32, not depth == 32;
- `oracle_correction_status = NEEDS_AUTHORIZATION`.

Kimi's review reports the same 50 + 1. **No workaround was applied, and the oracle was not edited.**

A negative control on the interpreter: Python 3.13.18 (Unicode 15.1.0) is refused by `run_regressions.py` (BLOCKED), which is the correct behaviour.

## 3. P0-03 receipt verifier against normative V0.5.9

**Method.** I wrote an independent probe (`tools/audit/claude_conformance_probe.py`), with its expectations derived from the spec text rather than from the implementation. It exercises the public `verify_restored_query_receipt` API on 100 rows covering:
- L0, the exact-type scan: SM1, SM2, T1–T6, T1r, S1, BI1–BI4 for the int domain ±2⁶³, D4(i), RT1, and a hostile colliding-key object armed after construction;
- L1–L4 and assurance labels: A, B, C1–C3, D1, D2, E1, R1–R4, NC8, NC14, F08a, X3b, X6a, X6b, M1–M8, S2, AN1, N1–N4, V1, V2, V4, B2, Q8a, CF1–CF3, S3, O1, O2;
- determinism and caps: P-1–P-4; S4a 32 failures with no truncation; S4b 33 entries ending `FAILURES_TRUNCATED`; S4c, where the cap does not stop evaluation; S5, where no attacker text is echoed and details are ≤120 characters;
- H-5 `CANONICALIZATION_FAILED` and the allow-list.

**Result.** 99 PASS, 1 FAIL, 0 exceptions, identical in A and B (`60251029…1246`).

| Clause | Status | Note |
|---|---|---|
| §2 "MUST call the existing function, do not reimplement" | **NONCONFORMANT (formal)** | The verifier defines its own `sha256_json` and `artifact_sha256`. Its output equals `restored_query_receipt.sha256_json` on every sample probed, but the MUST is not met. **Missing implementation:** an import of the existing function, or an author-ratified deviation. |
| L0 to L4, failure_details, P-1 to P-4, the cap, H-5, the allow-list | conforms on every probed row | probe coverage is partial |
| §11.3 (24 controls) and §11.4 (99 adversarial rows) as tests | **NOT PRESENT in the tree** | Only self-checks (40 checks) and 7 pytest cases are in the tree. The historical RG-4 V1.4 run (121 PASS) is sealed outside the tree and was not re-run here. **Missing implementation:** an in-tree, row-numbered §11.3/§11.4 suite. |
| Legacy v275 fixtures (8) | PASS | `key_id_mismatch.json` is rejected with exactly `ARTIFACT_SHAPE_INVALID`; stamp 2.7.4 and the stored hashes are OK; LQ1 grounding PASS (`8efd20b8…ec31`) |
| Historical Q4/D-6 (declared versus recomputed `receipt_sha256`) | unchanged, not re-adjudicated | carried as a known limitation |
| R-1/R-2/R-3/R-5 acceptance | by design `verified=True` possible | disclosed; Kimi confirms |

**I do not claim the P0-03 patch is complete.** The verifier conforms on what was probed, with one formal deviation and a coverage gap in the in-tree test suite.

## 4. Historical records

- **55 BLOCKED rows.** These come from `55_BLOCKER_BASELINE_DERIVED_FOR_REVIEW.json` (`9b3f233e…00b9`). That file declares itself a "DERIVED EXTRACT … NOT ORIGINAL 64 RECORD REGISTER", and it is preserved and reproduced as such in `REMAINING_BLOCKERS_V2_7_7.json`. Gate counts: RG6 31, IR04-P 20, IR04-O 20, F01 19, B4 16, GATE4 11, PUBLICATION 3. **These 55 rows are not the byte-identical 64-record register.**
- **9 previously VERIFIED rows.** The original `FINAL_BLOCKER_MATRIX_V0.1.json` (reported SHA-256 `1c2b4fe5…88c9`, 143163 bytes) was **not supplied**, so the 9 rows cannot be re-verified from original evidence. Status: `REPORTED_NOT_REVERIFIED`.
- **Kimi's claims.** "50+1" (the V0.3 suite) and "55/55" (a prospective V0.4 suite, a different scope) are kept separate.
- **Archives.** Historical archives and their checksum mismatches were not rewritten. The stale inherited manifest is kept as `docs/historical_rc12/SHA256SUMS_INHERITED_STALE.txt`.

## 5. Licence, secrets and private paths

- `LICENSE` (PolyForm Noncommercial 1.0.0), `NOTICE` and `LICENSE-SCOPE.md` are byte-unchanged and consistent with `CITATION.cff` and the Zenodo licence field.
- Secret scan: there are no credentials, tokens or keys. The only matches are variable names. The only e-mail address is the public project address.
- **Finding P-1 (author decision).** Six historical files contain Tasklet sandbox paths that include thread identifiers (`/tasklet/threads/<id>/work|uploads/…`): `docs/author_decisions/EIT_V277_TASKLET_CLOSURES_AIAssessmentReceipt_V0.1.json`, `docs/prior_evidence/CUSTODY.json`, `docs/prior_evidence/INSPECTED_EVIDENCE.json`, and three files in `docs/governance_review/`. The handoff evidence files contain them too, which is why R1 includes a generated blocker register rather than those raw files. These are not credentials. I did not rewrite them. The author decides whether to publish them as they are or to exclude those files, with disclosure, before the public release.

## 6. Existing Research Preview V0.1: do not release

Of its 64 files, 55 are identical to V0.3, 2 differ (`SHA256SUMS.txt`, `README.md`) and 7 exist only in the preview. **70 V0.3 files are missing**, including `tools/ci_*`, `tests/CI_LOCAL_RUN.log`, `F1_F5_DELIVERY_README.md` and the legacy README/PROVENANCE files. All `eit_program_lang` code is identical. The preview cannot pass the project's own inventory contract and must not be released. R1 is built from V0.3, not from the preview.

## 7. Proposed research release candidate R1

`NOVA_Q_EIT_PROGRAM_LANG_V2.7.7_RESEARCH_CANDIDATE_R1`, version `2.7.7-research.1`, label **RESEARCH_CANDIDATE — NOT FINAL — KNOWN BLOCKERS LISTED**.

- Code, tests, specs, LICENSE and NOTICE are byte-identical to V0.3.
- Release-layer changes are listed in `CHANGELOG.md` and summarised here:
  - the regenerated root manifest;
  - one version constant in `ci_inventory_check.py`;
  - new README, KNOWN_LIMITATIONS, CITATION, RELEASE_NOTES, Zenodo metadata, `.zenodo.json`, CHANGELOG and registry, with the RC11/RC12 originals kept in `docs/historical_rc12/`;
  - the audit and blocker documents;
  - the V0.3 patch documents, copied byte-identical;
  - Claude's audit tools.
- **Regression runner binding.** The V0.3 regression runner (`run_regressions.py`) pins the exact 127-file V0.3 inventory. On the R1 tree it fails closed with `BLOCKED_SOURCE_INTEGRITY: CANDIDATE file inventory mismatch`, which is correct behaviour; I did not work around it. The 50 PASS + 1 FAIL result therefore applies to the V0.3 bytes. It carries over to R1 only by hash identity, because every code, test, spec and fixture file is byte-identical. A runner that accepts R1's release-layer additions would need authorization (AUD-13).
- The `ci_release.sh` result and the archive SHA-256 for R1 are recorded **outside** the tree, in `R1_RELEASE_RECEIPT.json`, to avoid a circular evidence hash.

## 8. Required before any publication (not done)

1. An independent Tasklet replay of the **exact R1 ZIP bytes**: verify the hash, run `ci_release.sh` on 3.12.15, and run the regression suite against V0.3's baseline.
2. An author decision on finding P-1, the Tasklet paths.
3. The author's separate final GO for the GitHub pre-release, the tag and the Zenodo deposit.

**No GitHub or Zenodo action was taken.**
