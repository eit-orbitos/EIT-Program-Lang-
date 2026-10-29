# R2 change record — 2026-10-29 (NOT PUBLISHED)

**R2 is a distinct research-candidate tree, NOT an automatic release.**

Changes from the exact, independently replayed **R1** archive (`266464cd6b16fe175644942e9191cddac7ab5d9daa493b6889f0deea0cc3c7a1`):
- Excluded exactly six AUD-06 historic documentary files. No source code, test, reference, normative specification, `LICENSE` or `NOTICE` file was removed or modified. The six files' relative paths and original hashes appear in `docs/release/R2_AUD06_PUBLIC_EXCLUSIONS.md`.
- Added `docs/release/R2_AUD06_PUBLIC_EXCLUSIONS.md` and `docs/release/R2_REVIEW_READINESS.md`.
- Refreshed R2 README, KNOWN_LIMITATIONS, CHANGELOG, release notes, CITATION, both Zenodo descriptions/metadata, and LICENSE-SCOPE to declare exact R2 contents and evidence status.
- Regenerated `ARTIFACT_REGISTRY.json` and root `SHA256SUMS.txt` from packaged bytes. The exact R2 ZIP SHA-256 is recorded externally to avoid a self-referential hash.
- Historical R1 audit/patch/history documents remain byte-identical and may reference R1-only documents; no historical evidence was rewritten. The original R1 archive and its Tasklet replay remain separately preserved.

**R2 runtime: NOT_RUN.** Independent R1 replay ≠ independent R2 replay. Proposed tag `v2.7.7-research.1` is not created. No GitHub/Zenodo action; final V2.7.7 remains HOLD.

---

## Historic R1 change record (carried byte-content below, with this heading added)

# CHANGELOG

## 2.7.7-research.1 — Research Candidate R1 (prepared 2026-10-29, UNPUBLISHED)

**RESEARCH_CANDIDATE — NOT FINAL — KNOWN BLOCKERS LISTED**

Base: the V2.7.7 Tasklet Fix Candidate V0.3 successor tree, unchanged in code (V0.3 archive `b73b15c7…f027`; 127-file tree `2538c8cb…c84c1`).

### Unchanged (byte-identical to V0.3)
- Every file in `eit_program_lang/`, `tests/` and `reference/`.
- The specifications, `LICENSE`, `NOTICE`, `NON_CLAIMS.md` and `LICENSE-SCOPE.md`.
- The workflow, `requirements-ci.txt`, `tools/ci_release.sh` and `tools/ci_inventory_negative_controls.py`.
- All historical documents in `docs/`.

### Release-layer changes (disclosed one by one)
1. **`SHA256SUMS.txt` regenerated.** The inherited root manifest was stale. It was unchanged since Option-A, and the V0.3 patch did not update it:
   - 3 hash mismatches: `eit_v277_builder_candidate.py`, `frozen_translation_lookup.py`, `restored_registry_query.py`;
   - 3 files missing from the manifest: `lookup_identity.py`, `s1_sp1_adapter.py`, `s1_sp1_core.py`.

   As a result, the inherited `tools/ci_release.sh` **failed** on the unmodified V0.3 tree (inventory FAIL, which then cascaded into a negative-control FAIL). The original manifest is kept as `docs/historical_rc12/SHA256SUMS_INHERITED_STALE.txt`.
2. **`tools/ci_inventory_check.py`:** one constant changed, the expected metadata version `'2.7.7-rc12'` → `'2.7.7-research.1'`. Nothing else in the script changed. The negative control "stale Zenodo metadata version rejected" still applies.
3. **New:** `README.md`, `KNOWN_LIMITATIONS.md`, `CITATION.cff`, `RELEASE_NOTES_V2.7.7.md`, `zenodo/zenodo_metadata.json`, `zenodo/DESCRIPTION.md`, `.zenodo.json` and `CHANGELOG.md`. The RC11/RC12 versions they replace are kept byte-identical in `docs/historical_rc12/`.
4. **`ARTIFACT_REGISTRY.json` regenerated** for this tree. The RC12 registry recorded builder `3d401c47…`; the actual V0.3 builder is `fe305aab…`.
5. **Added evidence:**
   - `docs/audit/`: the Claude audit, the remaining-blockers register (JSON and Markdown) and the Phase A GitHub Actions plan;
   - `docs/v03_patch/`: the V0.3 delta, the oracle-conflict accounting, the regression runner and the fix report, copied byte-identical from the V0.3 archive;
   - `tools/audit/`: Claude's runner and probe scripts.

### Not changed, on purpose
- The preserved oracle conflict: `test_builder_envelope_overrun_and_runtime_smaller_envelope` FAILs and needs authorization to correct.
- The §2 "reuse the existing function" deviation in `receipt_verifier.py`. No P0-03 patch is claimed.
- The Tasklet sandbox paths that appear in 6 historical files. Whether to publish them is the author's decision (see the blockers register). They were not rewritten.

## Predecessors (separate artifacts, not aliases)
- V0.3 Tasklet Fix Candidate: `b73b15c7fed0ca5aa4e5ce33c97888a29ae49f6a96e99b1f37d836d5f945f027`
- Option-A original: `df60039d…` (inside V0.3 as `SOURCE_ARCHIVES/OPTION_A_ORIGINAL.zip`)
- RC12: `9326036842…`, and RC11 revision 2: `b7044de29f42616200b262fe597c2e98a8b4a723f575c3145d78a5a787bb2cee`
- Existing Research Preview V0.1 (`3ec997bb…`): **not** a predecessor of R1. It is not reconciled and must not be released (see the audit, §6).

Earlier history: `DIFF_LOG_V01_TO_V02.md` … `DIFF_LOG_V11_TO_V12.md`, and `docs/historical_rc12/RELEASE_NOTES_V2.7.7_RC11.md`.
