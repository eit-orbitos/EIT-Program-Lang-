# License provenance report — EIT Program Lang V2.7.7 (RC12)

Author / rights holder: Mr. Toni Mladenovski · Prepared by Tasklet, 24 October 2026, under the author's
instruction "GO — TASKLET EIT V2.7.7 RC12 FINAL PREPARATION" (item 1). Documentary record, not legal advice.

## 1. Source of the framework

The author designated Zenodo record 23544132 (EIT Analyzer Lambda V4.2.1, concept 23544131, published
21 October 2026) as the existing licensing framework. It was read from the public record on 24 October 2026:

| Item in 23544132 | Observed |
|---|---|
| Archive `EIT_Analyzer_V4.2.1_rc.zip` | SHA-256 `01ef66da501adef91ee7b2f1c9a720aa138eccc525d32342f26db4ff674cd531` (matches the record's own statement) |
| Record license field | `polyform-noncommercial-1.0.0` |
| Description | Software: PolyForm Noncommercial 1.0.0. Documentation and visual materials: CC BY-NC-SA 4.0. Commercial use: separate written agreement |
| `LICENSE` | SHA-256 `c0ea4a896d2c8c394b29f9427589996db826cd501c512279ff0ed3ef48fabbe5` |
| `LICENSE-DOCUMENTATION.md` | Two-row scope table (software incl. manifests, metadata and machine-readable results; written material); "If a file states its own license, that statement applies to that file"; third-party section |

V2.7.7 uses the same framework: the same two licenses, the same split between software and documentation, and the same commercial-use rule. **No new license is introduced.**

## 2. V2.7.7-specific author decisions (preserved)

`docs/EIT_V277_AUTHOR_DECISION_LICENSE_V0.1.md` (2026-10-24) governs this package:
- **Decision 1:** official unmodified PolyForm text `ffcca388…4cc8` governs. No rewording or rewrapping.
- **Decision 2:** all rights belong to Toni Mladenovski. EITNetworks LLC is named only as affiliation and contact.
- **Decision 3:** commercial use requires a separate written agreement that includes agreed financial terms.
- **Decision 5:** exact NOTICE text.

Where V2.7.7 wording differs from 23544132, the difference comes from these existing V2.7.7 decisions, not from a new license. Examples: the copyright line, and the phrase "including agreed financial terms".

## 3. LICENSE comparison (instruction 1)

| Copy | SHA-256 | Bytes | LF count |
|---|---|---|---|
| V2.7.7 RC11/RC12 `LICENSE` (governing) | `ffcca38841adb694b6f380647e15f17c446a4d1656fed51a1e2041d064c94cc8` | 4,563 | 131 |
| Zenodo 23544132 `LICENSE` | `c0ea4a896d2c8c394b29f9427589996db826cd501c512279ff0ed3ef48fabbe5` | 4,563 | 73 |
| Repository `main@6ff36a61` `LICENSE` | `c0ea4a89…be5` (byte-identical to 23544132) | 4,563 | 73 |

After every run of whitespace is collapsed to a single space, the two texts are **identical**. The difference is **formatting only** (line wrapping). So it is not necessary to change locked bytes, and `LICENSE` is **unchanged** in RC12. Decision 1.4 governs any correction of record 23544132: that happens only in a future new version, under a separate decision. Nothing was changed there.

## 4. What RC12 changes for licensing

| File | Change |
|---|---|
| `LICENSE` | unchanged (`ffcca388…`) |
| `NOTICE` | unchanged (Decision 5 text) |
| `COMMERCIAL-USE-POLICY.md` | unchanged |
| `LICENSE-DOCUMENTATION.md` | original RC11 bytes kept as an exact prefix; one pointer sentence to `LICENSE-SCOPE.md` appended |
| `LICENSE-SCOPE.md` | **added**. File-by-file application of the framework (rules S/D), list of third-party and external-reviewer files, extent-of-rights clause |
| `CITATION.cff` | version/title RC12. Keeps the single software license, because CFF reads multiple licenses as alternatives |
| `README.md`, `zenodo/*` | aligned to RC12 and to the two-domain statement |

## 5. Third parties

Fourteen files are identified as third-party or external-reviewer material (PolyForm Project text; Kimi and Claude reports and logs; the separate GPT-6.1 Sol RC11 governance/control review and its receipts; GitHub Action metadata). They are excluded from the author's grant. The authorship of contributions made with AI assistance at the author's direction is not adjudicated here. The grant is limited to the extent of the author's rights, and no third-party right is appropriated.

## 6. Repository history

On `main`, `LICENSE-HISTORY.md` records that no license existed before commit `a0c7026e…`, and it records preserved rights. It also describes `LICENSE` as `c0ea4a89…`. Under branch Option B that file stays in git history and is not carried into the RC12 tree, because a verbatim copy would misdescribe the governing `LICENSE` bytes. The preserved-rights principle is restated in `LICENSE-SCOPE.md` §4.
