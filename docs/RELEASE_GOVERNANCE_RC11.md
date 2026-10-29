# RC11 release governance — preserved normative text and current record

V0.6.0 DRAFT V0.5 exact SHA-256 a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788. The excerpts below preserve historical statuses in the ratified bytes, not current runtime claims. Current dispositions: RG6_FINAL_RECONCILIATION_MATRIX.md. Ratification and author closures are separate exact copies under author_decisions/. LIMITED changes gate 6 only; no waiver of gate 4 or independent reproduction.

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


## 13. Out-of-scope items — reconciliation for a LIMITED release (V0.6.0 amendment)

This section replaces V0.5.9 §13. Per author decision (option b, 2026-10-24), the items below no longer block a LIMITED release unconditionally; each is reconciled individually. An item is marked CLOSED only with a named test in V2.7.7 (path and name) or other recorded evidence; otherwise it stays OPEN with a stated failure mode, who is affected, why it is accepted, and the mitigation or caller obligation. The blocking rule of B4 applies throughout: if failure of an item could make the verifier return verified=True for a forged receipt, that item REMAINS BLOCKING for any release. Analysis for each item is given against the pinned V0.7 verifier (97b1d148…) and the §12 disclosures.

**Definition (normative).** A "LIMITED release" of EIT Program Lang V2.7.7 is: (1) exactly the pinned artifacts — verifier candidate SHA-256 97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca, builder 3d401c47e49f9abb5f94d95480bf6dff157e0be17ff0b0eadbfcac86d6898cec, companion 4ba6556ac456601bf9d91608f28ba950b619c51ac123598aeeb480d24444ad65 — plus the file set of one numbered release-candidate package, nothing else; (2) labelled research/limited in the package, the repository and the archive record; (3) carrying no claim beyond the §12 non-claims, with every §13 reconciliation item and both mutant series disclosed in the shipped documentation; (4) published to GitHub/Zenodo only after an explicit author decision; (5) not for production or commercial use without a separate agreement (see NOTICE). Anything outside this scope is not a LIMITED release and §13 items revert to BLOCKING for it.

| ID | Item (source: CLAUDE_AUDIT_V2_7_6) | Status | Failure mode | Affected | Why accepted | Mitigation / caller obligation |
|---|---|---|---|---|---|---|
| N-1 | Source-side silent, order-dependent pick in `_resolve_source` | OPEN — accepted residual limitation | Order-dependent source pick in genuine query operations | Runtime query path | The verifier does not replay source resolution (§12 R-2 non-claim); a forged receipt exploiting resolution ambiguity still fails the verifier's R-1/R-3 target-resolution rules for current stamps; not argued to yield verified=True for a forged receipt through the verifier (analysis, not tested) | Caller treats resolution as advisory; fix lands only in a version that touches the query path |
| N-3 | Malformed restored state raises in the query path | OPEN — accepted residual limitation | Crash (denial) on malformed state | Runtime query path | Fail-closed behaviour (no forged acceptance); no verified=True vector | Caller validates state before serving |
| N-4 | Canonical serialization (H-3 collisions; int/str key collision; insertion-order-dependent index) | ACCEPTED with R-4 disclosure | Distinct values may serialize alike; index hash order-dependent | Runtime/builder paths | Inside the verifier the guard makes default=str and non-string-key collisions unreachable (§6.5); H-6 bounds integers; not argued to yield verified=True for a forged receipt through the verifier (analysis, not tested) | R-4 stays OPEN by design; real anchor per §4.5; index_sha256 DEFERRED (R-1) |
| N-5 | `symbol_id` NFC regression in runtime lookup | OPEN — accepted residual limitation | Runtime lookup may miss NFD/NFC variant | Runtime lookup path | Verifier surfaces use nfc() (§3.4); a forged NFC-variant receipt fails R-1/R-3; no verified=True vector | Disclosed; runtime fix in a future version |
| N-6 | `None` rendered as `"None"` | OPEN — accepted residual limitation | Mis-rendered symbol surface | Runtime builder path | Verifier compares values under teq; mismatch is rejection, never verification | Disclosed |
| N-7 | Results alias the artifact | OPEN — accepted residual limitation | Caller mutating results corrupts its own state | Callers | Verifier never mutates (T-1; Z1 evidence 316/316 was recorded on the V1.2 run of the earlier candidate ee20d1ba… and is NOT bound to the pinned verifier 97b1d148…; for the pinned verifier no Z1-bound execution record exists in this thread — REPORTED, to be cited with file and SHA-256 when such a record is delivered) | Caller must copy before mutation (T-1) |
| N-8 | CI: (a) `.gitkeep` breaks inventory; (b) `sha256sum` without `--strict`; (d) environment lock (`ubuntu-latest` floats; no `--require-hashes`; action tags @v4/@v5 instead of full commit SHAs); (e) no `persist-credentials: false` | PARTIAL/OPEN — only N-8(b) addressed | (a) upload-time inventory break; (b) pin-check weakness; (d) supply-chain drift; (e) credential exposure via checkout | Release process | N-8(b): `sha256sum --strict` defined in V0.9 CI workflow — DEFINED, NOT EXECUTED (CI never ran). (a),(d),(e): NOT addressed; (d) is a regression (audit recorded SHA pinning as a positive). | N-8(b) keep --strict and EXECUTE CI; (a) add inventory check for stray files; (d) pin runner image + full commit SHAs + --require-hashes; (e) persist-credentials: false. CLOSED only when executed and evidenced |
| N-9…N-12 | Audit items N-9, N-10, N-11 (LOW), N-12 (INFO) | OUT OF SCOPE — not reconciled in this amendment | per audit | Runtime/test-hygiene items | Inherited silence from V0.5.9; no release-blocking analysis claimed | Future version that touches the affected paths must reconcile them |
| D-1 | V0.5.9 §13 wording "eight surviving mutants" | RECORDED | Wording discrepancy (audit L306 vs its own table L288–304: 7 survivors; M16 double-counted) | Records | Corrected count: 7 — M1, M6, M10, M12, M13, M15, M16 (Tasklet intake ae89a1bb…, Claude clarification f1ea5c0e…) | This table stands as the corrected record |

**Mutants (audit series, CLAUDE_AUDIT_V2_7_6 §6):** 17 mutants, 10 killed, 7 survived — M1, M6, M10, M12, M13, M15, M16. The audit's §7 kill tests (6 Group A tests + 1 Group B battery test) were delivered separately; whether they exist in V2.7.7 is UNVERIFIED. Per-mutant, with the runtime gap stated explicitly and the caller obligation where one exists.

| Mutant | Reverted behaviour | Status | Failure mode | Affected | Why accepted | Mitigation / caller obligation |
|---|---|---|---|---|---|---|
| M1 | `allow_history_fallback` default → True | OPEN | History fallback may serve pre-frozen state | Runtime query path | Verifier requires applicable state copies (T.1/T.2), but the RUNTIME gap itself is unmitigated | Serve frozen state only; treat history fallback as non-authoritative |
| M6 | `restored_state_sha256` optional again | OPEN | Receipts/state without state hash served | Runtime builder/query path | Verifier enforces copy consistency when copies exist (T.1/T.2; AN1/SC1 rows) | Reject state objects lacking restored_state_sha256 before serving |
| M10 | State-hash mismatch ignored | OPEN | Tampered state served as matching | Runtime query path | Verifier rejects mismatches (EXPECTED_STATE_HASH_MISMATCH) | Reject on mismatch before serving |
| M12 | NFC dropped from index keys | OPEN | Index lookup misses NFD/NFC variant | Runtime index path | Index hashing is runtime-side (R-1 deferred); receipt rules unaffected | Disclosed; runtime fix in a future version |
| M13 | Packet provenance check dropped | OPEN | Packets with wrong provenance served | Runtime lookup path | Verifier independently checks packet provenance (B.3, X4o) | None beyond verifier reliance; fix in a future version |
| M15 | Required-field check dropped | OPEN | Incomplete receipts served | Runtime builder path | Verifier enforces required fields (Q.4/X.4/Q.4a/X.4a/X.6) | None beyond verifier reliance; fix in a future version |
| M16 | Mutation battery always reports intact | OPEN (§7 Group B) | Runtime mutation goes undetected | Runtime integrity battery | Battery is runtime-side; O-3 residual remains | Independent state verification before trusting runtime output |

B4 (ANALYSIS, NOT TESTED): each M-mutant lives in the runtime serving path; the verifier enforces the receipt-side consequence independently, so failure of the runtime check is not argued to yield verified=True for a forged receipt through the pinned verifier. A demonstrated counter-example re-opens the mutant as BLOCKING.

**Mutants (RG-5 series, separate numbering):** M36, M43, M55, M61 — survivors of the RG-5 mutation run (57/61 killed). V1.4 rows are scheduled for N1/M61 and N2/M36/M55; M43 has no scheduled test. Full columns per the Tasklet addendum.

| Mutant | Status | Failure mode | Affected | Why accepted | Mitigation / caller obligation |
|---|---|---|---|---|---|
| M36 | OPEN | V1.4 row N2/M36 scheduled but NOT_RUN | Verifier under RG-5 mutation | Not accepted as resolved; remains OPEN pending V1.4 evidence; no verified=True conclusion drawn | Run V1.4 |
| M43 | OPEN | No scheduled test | Verifier under RG-5 mutation | Not accepted as resolved; remains OPEN; no test scheduled | Schedule a test |
| M55 | OPEN | V1.4 row N2/M55 scheduled but NOT_RUN | Verifier under RG-5 mutation | Not accepted as resolved; remains OPEN pending V1.4 evidence | Run V1.4 |
| M61 | OPEN | V1.4 row N1/M61 scheduled but NOT_RUN | Verifier under RG-5 mutation | Not accepted as resolved; remains OPEN pending V1.4 evidence | Run V1.4 |

B4 check (ANALYSIS, NOT TESTED): none of the OPEN items above is argued to yield verified=True for a forged receipt through the pinned V0.7 verifier; each either (a) lives outside the verifier (runtime paths), with the verifier independently enforcing the receipt-side consequence, or (b) is process-side (N-8: PARTIAL/OPEN — sub-item N-8(b) is defined-not-executed per the table above; the stale word "closed" that stood here in V0.2 was corrected by this amendment, per finding G1 of the Grok review and Tasklet intake d2406abb…). These B4 entries are analysis, not tests: a single demonstrated counter-example — a forged receipt that verifies because of any OPEN item — re-opens that item as BLOCKING immediately. Any future version that modifies the query path, canonicalization, or the integrity battery must re-open the corresponding items as BLOCKING until closed with evidence.

V0.2 §10 referred to "P0-01/P0-02" and "P1" items. Those identifiers are not defined in any document supplied to the drafter and are not used here.

## 14A. Release gates

1. Independent review of this V0.5.9 text by a reviewer other than the drafter who has received the file itself, not pasted text, and who quotes clause text in the review so that the reviewed content can be matched to the file; and a SHA-256 computed over the file by a party other than the drafter. The review MUST state which sections were read in full and which were not, and MUST NOT claim to have reviewed a section it could not read. `[DEEPSEEK V0.5.4 RG-C1]`
2. Separate author authorization for implementation.
3. Implementation on an isolated candidate; V2.7.5 untouched.
4. All CONTROL tests pass on V2.7.6 and V2.7.7; all FAIL_FIRST tests fail on V2.7.6 and pass on V2.7.7; all applicable NEW_API and CONTROL_FOR_V277 tests pass on V2.7.7; KNOWN_RISK outcomes recorded; the existing 33 tests pass with the fixture change of §11.1. Every row is applicable except that S4d alone MAY be recorded as `NOT_APPLICABLE` under the condition stated in its row; that outcome is a disclosed applicability exception, not an executed pass. The test report MUST enumerate separately the executed passes, the failures, the not-run cases, the non-applicable cases, the known-risk characterizations and the harness errors (§11.2 T-10). A required execution that is missing, and a harness error, do not satisfy this gate. `[TASKLET V058-F01][AUTHOR V0.5.9][NEW-V0.5.9]`
5. Independent reproduction.
6. Items in §13 closed separately. (V0.6.0 amendment: for a LIMITED release, gate 6 is satisfied by the §13 reconciliation — each item individually marked CLOSED with evidence or OPEN with failure mode, affected party, acceptance rationale and mitigation/caller obligation, and the B4 check recorded that no OPEN item yields verified=True for a forged receipt through the pinned verifier. Full closure with evidence remains required for any future version that modifies the affected paths. Per-mutant status for both mutant series is part of this gate's evidence.)

Passing tests does not authorize publication or formal freeze.

---

