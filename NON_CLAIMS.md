# RC11 non-claims and anchor obligations

Exact §12 and §4.5 text from the hash-bound ratified specification; historical wording is preserved. Current dispositions are separate in docs/RG6_FINAL_RECONCILIATION_MATRIX.md. SOFTWARE / DOCUMENTARY VALIDATION ≠ PHYSICAL LAW ≠ EXTERNAL SCIENTIFIC VALIDATION.

## 12. Residual risks and non-claims

These MUST appear in the V2.7.7 user-facing documentation.

**Non-claims `[DEEPSEEK][CLAUDE]`**

- **Data integrity.** Hashes show agreement with a reference value. They do not show that a claim is true.
- **Artifact grounding.** Ids and fields match the supplied artifact. That does not make the artifact authentic.
- **External provenance.** An out-of-band expected hash ties verification to a committed artifact. If an attacker controls both the artifact and the expected hash, it provides no authenticity.
- **Producer authenticity.** `author`, `module_id`, version stamps and keyless hashes are not signatures.
- **Real-world event truth.** Neither hashes nor `generated_at_utc` establish that a query happened, when, or that any physical event occurred.
- **Version stamp.** An unlisted `receipt_version` in default mode is evaluated under current rules. The verifier does not reject it and does not warn. No stamp, listed or not, is evidence of a specific producer or runtime; a caller MUST NOT read it as such. `[DEEPSEEK V0.5.1 U-C1]`
- **Canonicalization failure.** `CANONICALIZATION_FAILED` means the input could not be hashed under the canonical contract. It is not evidence of authenticity and it is not evidence of tampering. `[DEEPSEEK V0.5.4 H5-C4]`
- **Runtime profile.** With the integer domain of §6.1 the integer-conversion limit of the process cannot change a result (H-6). `nfc` and `.upper()` in §3 follow the Unicode database of the running interpreter; equality of results across interpreters with different Unicode versions is not claimed and was not tested. P-4 is scoped accordingly and the profile is defined in §10.2; disclosure does not remove the dependency. `[TASKLET V056-F03]` `[TASKLET V055-F02][NEW-V0.5.6]`
- No scientific proof or physical-law claim is made.

**Open risks**

| ID | Risk | Status |
|---|---|---|
| R-1 | `index_sha256` is self-declared and not verified. A forged value verifies. It depends on restored-state identifiers and insertion order, and V2.7.5 values are not reproducible by V2.7.6 code `[EXECUTED]` | DEFERRED `[AUTHOR]`; needs a canonical index as a separate, versioned hash-format change |
| R-2 | The query and source resolution are not replayed. A receipt may claim `found: false` for an existing symbol, or list a real record the query would not return | OPEN; fix together with source-side ambiguity (audit N-1) |
| R-3 | Keyless hashes: whoever can rewrite artifact and receipt together passes every check in default mode | OPEN by design; mitigated only by a real anchor (§4.5) |
| R-4 | Canonicalization collisions (H-3) | OPEN; audit N-4 |
| R-5 | Stamp downgrade. Setting `receipt_version` to `2.7.4` selects weaker legacy rules (§9.1 Q.1, §9.3 R-1). A downgraded receipt can still report `ARTIFACT_AND_STATE_ANCHORED` with matching external hashes: these hashes do not attest to the producer runtime version. In default mode with no anchor the same receipt yields `CONSISTENCY_ONLY`; with a correct artifact anchor and a correct state anchor it yields `ARTIFACT_AND_STATE_ANCHORED`. `[DEEPSEEK V0.5.1 RV-C2]` | OPEN / AUTHOR_ACCEPTED_RISK; no mitigation claimed. A future version may add a trusted minimum-stamp policy. `[AMENDMENT_A A-06]` |
| R-6 | Results alias the artifact (audit N-7). The verifier does not mutate, but callers can | OPEN; out of scope |

---


**Mandatory release disclosures (V0.6.0 addition; §12 requirement for any release).** The user-facing documentation of any release MUST contain, at minimum: (a) every §12 non-claim; (b) risks R-1…R-6 with status; (c) the §4.5 caller obligation; (d) the §13 reconciliation table with per-item status; (e) the mutant tables (audit series M1/M6/M10/M12/M13/M15/M16 and RG-5 series M36/M43/M55/M61) with per-mutant CLOSED(path,test)/OPEN(rationale); (f) D-1 (the V0.5.9 "eight survivors" wording is inherited from CLAUDE_AUDIT_V2_7_6 L306; the audit's own table L288–304 records 7 survivors — M16 double-counted; corrected count: 7). The release candidate's NON_CLAIMS.md and KNOWN_LIMITATIONS.md are to be aligned to this section (target: release candidate rc10); they are NOT yet a verified reference implementation of it.


### 4.5 Caller obligation `[DEEPSEEK][CLAUDE]`

`expected_artifact_sha256` and `expected_restored_state_sha256` MUST come from a source the receipt producer cannot write to. A hash computed by the caller from the artifact it is about to verify is not an anchor.

The following text MUST appear verbatim in the function's docstring `[AMENDMENT_A A-05]`:

> The verifier cannot enforce that expected hashes were obtained from a trustworthy independent channel. If the caller computes an expected hash from the untrusted artifact being verified, an `ARTIFACT_ANCHORED` assurance label does not establish independent provenance or producer authenticity.

`assurance` describes the checks performed. It does not certify where an anchor came from.

