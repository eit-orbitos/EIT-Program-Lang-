# AUD-06 — R2 public-candidate documentary exclusion notice

**Status:** RESEARCH_CANDIDATE R2 — NOT FINAL — NOT PUBLISHED — INDEPENDENT R2 REPLAY NOT_RUN.

**Approval scope:** On 2026-10-29, the author approved creation of a separate R2 candidate with exclusion of **exactly six** AUD-06 documents, renewed hashes and static verification. This chat approval is not a signature, final-release GO, GitHub/Zenodo permission, or technical gate closure.

**Origin:** The exact R1 archive SHA-256 is `266464cd6b16fe175644942e9191cddac7ab5d9daa493b6889f0deea0cc3c7a1`. Tasklet's independently executed R1 replay reported `REPLAY_MATCH` with important preserved failures, but that result is attached **only to the unchanged R1 bytes**, not this R2 archive.

## The only six excluded repository-relative files

These are historical documentary provenance and reviewer files with internal Tasklet thread paths. This is a disclosure-minimization decision, **not a conclusion that these files contain credentials, that their review was invalid, or that the cited findings are closed**. They remain unchanged in privately retained original R1 evidence.

| Excluded path | Original R1 SHA-256 | Original bytes |
|---|---|---:|
| `docs/author_decisions/EIT_V277_TASKLET_CLOSURES_AIAssessmentReceipt_V0.1.json` | `c5601bf679e85c8a73b3fa4d0dee6428695814c3abacadc545e1c3cf2239cc8e` | 3009 |
| `docs/prior_evidence/CUSTODY.json` | `ece267814002f0280653d80572290d58ccc013a0d4a30901e7ecb3542ac8fcde` | 2695 |
| `docs/prior_evidence/INSPECTED_EVIDENCE.json` | `bee7ce3d7cc45a22fb2a7481da60e44d6ad54706b3231612e3462844feea1a81` | 12127 |
| `docs/governance_review/AIAssessmentReceipt.json` | `1f056333b522715c28de33f802ce40ba0212fbf3f873e74e7f382dd1d0c37efc` | 2341 |
| `docs/governance_review/CONTROL_REVIEW_RECEIPT.json` | `7de247eb0a70c1dd4802f4b5b85c3a7d6de6307d440e5361d03c199cf0b3a787` | 2258 |
| `docs/governance_review/REPORT.md` | `ca23cff9f05bf0d7d4ec05510f3b908c7f85cc27750b17bd1bea43b747d8316d` | 7199 |

## Historical references retained

References to these six files may still appear in *unchanged historical documents*, including `docs/audit/`, `docs/historical_rc12/`, `docs/v03_patch/`, `docs/KIMI_RG4_V12_PASS_REGISTRATION_V0.1.md`, `docs/governance_review/CONTROL_REVIEW.md` and `tests/legacy/PROVENANCE.md`. Such references are **historical or external custody links, not statements that those six records remain packaged in R2**. Historical manifests and lineage records are not the current R2 manifest and must not be rewritten as if they originated here. The entire original R1 archive and its independently observed evidence must be preserved separately.

The two retained documents `KNOWN_LIMITATIONS.md` and `docs/audit/CLAUDE_AUDIT_V2_7_7.md` contain only a generic `/tasklet/threads/<id>/...` pattern and are intentionally **not** among the six concrete exclusions. No additional historical files were deleted. No hidden replacement stubs were added at the six original paths.

## Verification and governance scope

- Exact source/test/reference bytes are inherited from R1, not changed or re-executed by R2 packaging.
- R2 `ARTIFACT_REGISTRY.json` and `SHA256SUMS.txt` are regenerated to reflect the actually packaged members; earlier manifests remain historical.
- R2’s own ZIP hash is an **external detached** receipt, never embedded in the ZIP itself.
- The R1 CI/replay outcome may be cited only as **prior exact-R1 evidence**; R2 program execution and independent replay remain `NOT_RUN`.
- Known V0.3 regression outcome: **50 PASS + 1 FAIL**; P0-03 sampled probe: **99 PASS + 1 FAIL**; R1's original regression runner rejected the R1 inventory with `BLOCKED_SOURCE_INTEGRITY`.
- C3-E `NOT_IMPLEMENTED`; F01 `0/19`; B4 `NOT_CLOSED`; RG6 `OPEN`; Gate-4 `NOT_SATISFIED`. Final V2.7.7 remains `HOLD`.
- No GitHub push/tag/release, no Zenodo deposit, no DOI, no publication authorization from this R2 creation.
