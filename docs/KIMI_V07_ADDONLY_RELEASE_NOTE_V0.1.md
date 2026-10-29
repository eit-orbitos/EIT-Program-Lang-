# KIMI — V0.7 ADD-ONLY RELEASE NOTE V0.1 (N5 corrections)

**DATE:** 2026-10-23 · **AUTHORITY:** Author Option 1 (preparation only)
**PINNED ARTIFACTS UNTOUCHED:** V0.5.9 `3fc10557…`, V1.3 suite pin, V0.7 verifier `97b1d148…`, builder `3d401c47…`, companion `4ba6556a…`, package `41def444…`.

## Corrections recorded (add-only)
1. **Manifest (N3):** superseded manifest is `SHA256SUMS_V0.8.txt` (stale V0.6 references).
   Authoritative for the V0.7 package: `SHA256SUMS_V0.7_PACKAGE.txt` + `V07_PACKAGE_VERIFICATION_LOG.txt`
   (per-entry digests of the EXISTING zip `41def444…`). No repackaging performed.
2. **Outdated wording:** `CANDIDATE_STATUS_V0.7.md` phrases "ratification pending" for F1/F5
   and "DRAFT, not pinned" are **superseded** by the settled record:
   - F1 return value on L0 failure = `receipt_sha256: None` — AUTHOR-RECORDED decision (no longer pending).
   - F5 strict missing `packet_version` → reject — AUTHOR-RECORDED option (a) (no longer pending).
   - V1.3 suite was pinned by Tasklet and executed; "DRAFT, not pinned" referred to an earlier cycle.
   This note corrects the record WITHOUT modifying the status file or the pinned verifier.
3. **N4 (INFO):** L4.4 comparison semantics preserved exactly as pinned; no alteration.
4. **Mutants:** 57/61 killed reported; four survivors (M36, M43, M55, M61) remain OPEN for
   Tasklet V1.4 rows (N1/M61, N2/M36/M55). No "61/61" claim is made or implied.
5. **Q4 contract unchanged:** declared value on L1+; None on L0; mismatch reported via 1a codes.

## Deliverables this cycle
| Artifact | SHA-256 |
|---|---|
| SHA256SUMS_V0.7_PACKAGE.txt | see log |
| V07_PACKAGE_VERIFICATION_LOG.txt | see below |
| KIMI_V07_ADDONLY_RELEASE_NOTE_V0.1.md (this file) | see manifest |
| NOVA_Q_EIT_VMAX_DESIGN_NOTE_V0.8.md | see below |

**SEAL:** ADD_ONLY — N3_N5_CORRECTED — PINNED_BYTES_UNTOUCHED — NO_UNAUTHORIZED_CHANGES
