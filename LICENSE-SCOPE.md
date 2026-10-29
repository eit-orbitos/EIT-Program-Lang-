# LICENSE SCOPE — EIT Program Lang V2.7.7

Rights holder: Toni Mladenovski (https://orcid.org/0009-0009-8343-662X).
Affiliation / licensing contact: EITNetworks LLC — info@eitnetworks.org.

This file applies to this package the same two-license framework the author already uses for
EIT Analyzer Lambda V4.2.1 (Zenodo record 23544132). It introduces **no new license**. It does not
change `LICENSE`, `NOTICE` or `COMMERCIAL-USE-POLICY.md`. The original text of
`LICENSE-DOCUMENTATION.md` is unchanged; one pointer to this file is appended to it.

## 1. Which license applies to which file

| Rule | Material | License |
|---|---|---|
| S | Every file that is **not** a Markdown (`.md`) file, except those named in sections 2 and 3: source code (`eit_program_lang/`), tests and test fixtures (`tests/`), CI and tooling (`tools/`, `.github/`, `requirements-ci.txt`, `.gitignore`), reference code (`reference/generators/`, `reference/v276/`), manifests and metadata (`SHA256SUMS.txt`, `ARTIFACT_REGISTRY.json`, `CITATION.cff`, `zenodo/zenodo_metadata.json`, nested manifests), and machine-readable results and logs | PolyForm Noncommercial License 1.0.0. Full text in `LICENSE` |
| D | Every Markdown (`.md`) file, except those named in sections 2 and 3: README, release notes, non-claims, limitations, diff logs, specifications, governance and decision records, test READMEs, Zenodo description | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode |

If a file states its own license, that statement applies to that file.

## 2. Third-party and external-reviewer material: not licensed by this package

These files are included **unmodified, as audit evidence or reference**. They are **not** claimed as the
author's own work and are **not** licensed by `LICENSE` or `LICENSE-DOCUMENTATION.md`. Any rights in
them remain with their respective holders.

| File | Origin |
|---|---|
| `reference/PolyForm-Noncommercial-1.0.0.official.md` | PolyForm Project. Official license text, reproduced verbatim |
| `docs/KIMI_RG4_V12_PASS_REGISTRATION_V0.1.md` | Independent reviewer Kimi |
| `docs/KIMI_V07_ADDONLY_RELEASE_NOTE_V0.1.md` | Independent reviewer Kimi |
| `docs/KIMI_V277_V05_FIXED_CONFIRMATION_V0.1.md` | Independent reviewer Kimi |
| `docs/SHA256SUMS_V0.7_PACKAGE.txt` | Independent reviewer Kimi (package manifest) |
| `docs/V07_PACKAGE_VERIFICATION_LOG.txt` | Independent reviewer Kimi (verification log) |
| `docs/prior_evidence/CLAUDE_AUDIT_V2_7_6.md` | Independent reviewer Claude |
| `tests/legacy/PROVENANCE.md` | Independent reviewer Claude (fixture provenance note) |
| `docs/governance_review/CONTROL_REVIEW.md` | Separate reviewer (GPT-6.1 Sol), RC11 governance/control review |
| `docs/action_pin_evidence/checkout_result.txt` | Repository metadata of the third-party GitHub Action `actions/checkout`, retrieved read-only |
| `docs/action_pin_evidence/setup-python_result.txt` | Repository metadata of the third-party GitHub Action `actions/setup-python`, retrieved read-only |

## 3. Licensing instruments

`LICENSE` (official PolyForm Noncommercial 1.0.0 text, PolyForm Project), `NOTICE`, `LICENSE-DOCUMENTATION.md`,
`COMMERCIAL-USE-POLICY.md` and this file state the terms. They are not themselves offered for adaptation.
Every line of `NOTICE` that begins with `Required Notice:` must be kept, as the PolyForm license requires.

## 4. Nested archives

`reference/EIT_V2_7_6.zip` and `docs/author_decisions/EIT_V277_RG6_CLOSURES_REGISTERED_V0.1.zip` are
byte-pinned historical evidence. Their members follow rules S and D to the extent they are the author's
work. Third-party members are excluded as in section 2. Including an earlier version here does not revoke
any permission validly held under an earlier distribution.

## 5. Extent of the grant

The licenses are granted only to the extent of Toni Mladenovski's rights. Some files carry origin tags
(for example `[CLAUDE]`, `[DEEPSEEK]`, `[KIMI]`, `[TASKLET]`). These tags record contributions made during
drafting and review at the author's direction. They are provenance records, and this file claims no right
that the author does not hold.

## 6. Attribution

When sharing or adapting documentation under CC BY-NC-SA 4.0, credit:

> Toni Mladenovski, *EIT Program Lang V2.7.7*, EIT Networks, https://github.com/eit-orbitos/EIT-Program-Lang- (ORCID 0009-0009-8343-662X)

## 7. Commercial use

Neither license permits commercial use. Commercial use requires a separate written agreement with
Toni Mladenovski that includes agreed financial terms. See `COMMERCIAL-USE-POLICY.md`.

## 8. Third-party tools

Python, pytest and its dependencies, and the GitHub Actions used by the CI workflow remain under their own
licenses. They are not distributed in this package and are not covered by this file.

## 9. Note on the LICENSE text

`LICENSE` is the official PolyForm Noncommercial 1.0.0 text, SHA-256
`ffcca38841adb694b6f380647e15f17c446a4d1656fed51a1e2041d064c94cc8` (author license decision V0.1, Decision 1).
The copy distributed with EIT Analyzer Lambda V4.2.1 and on this repository's `main` branch
(SHA-256 `c0ea4a896d2c8c394b29f9427589996db826cd501c512279ff0ed3ef48fabbe5`) has the same words with
different line breaks. The terms are identical. The file is not rewrapped (Decision 1).

## R2 exclusion scope addendum (2026-10-29)

The three RC11 governance_review files above were listed in the **unmodified R1 LICENSE-SCOPE.md**, but are among the exactly six historical AUD-06 documents not packaged in R2. The remaining three excluded files are in docs/author_decisions/ and docs/prior_evidence/. Exclusion does not change their original attribution or ownership and does not change the license on any retained file. For all six exact file paths and R1 hashes, see docs/release/R2_AUD06_PUBLIC_EXCLUSIONS.md. R1 remains preserved separately. No license grant is asserted for omitted third-party review material.
