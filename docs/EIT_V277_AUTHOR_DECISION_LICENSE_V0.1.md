# EIT V2.7.7 — Author decision: license, rights holder, NOTICE — V0.1

- Date: 2026-10-24 (GMT-4)
- Author / rights holder / decision owner: Toni Mladenovski
- Author's instruction (verbatim, Macedonian):
  > "važno mi e da go zaštitime softwerot od komercijalna upotreba, za komercijalna upotreba samo so nas nov dogovor i izgotven finansiski plan. All right to Toni Mladenovski"

## Decision 1: software license
1. The software is licensed under the **PolyForm Noncommercial License 1.0.0, official unmodified text**.
2. The authoritative text is `PolyForm-Noncommercial-1.0.0.official.md` (SHA-256 `ffcca38841adb694b6f380647e15f17c446a4d1656fed51a1e2041d064c94cc8`).
   - It comes from the SPDX license list (npm `spdx-license-list@6.9.0`, tarball `6fc54867…`).
   - It was cross-checked against https://polyformproject.org/licenses/noncommercial/1.0.0/: 16 headings including "Notices", and no "security" clause.
3. No rewording, shortening, rewrapping or "summary" of the license text is allowed anywhere.
4. If any other copy, including the LICENSE file in Zenodo 23544132 (`c0ea4a89…`), differs from this text, **the official text governs**. Tasklet compares `c0ea4a89…` against `ffcca388…` and reports the result. If it differs, the Zenodo record is corrected in a future new version, under a separate decision.

## Decision 2: rights holder
- All rights belong to **Toni Mladenovski**. EITNetworks LLC is named only as affiliation and licensing contact.
- Copyright line: `Copyright (c) 2026 Toni Mladenovski. All rights reserved except as expressly licensed.`

## Decision 3: commercial use
- Commercial use is **not** licensed. It is possible only under a **separate written agreement with Toni Mladenovski that includes agreed financial terms** (fees, royalties or another agreed financial plan).
- `COMMERCIAL-USE-POLICY.md` states this. It is a policy pointer, not a license grant. Contact: info@eitnetworks.org.

## Decision 4: documentation
- Documentation and visual materials: **CC BY-NC-SA 4.0** (`LICENSE-DOCUMENTATION.md`), same rights holder.

## Decision 5: NOTICE (approved text, separate file `NOTICE`)
```
Required Notice: Copyright (c) 2026 Toni Mladenovski. All rights reserved except as expressly licensed. https://orcid.org/0009-0009-8343-662X
Required Notice: EIT Program Lang V2.7.7 is licensed under the PolyForm Noncommercial License 1.0.0 (see LICENSE). Documentation and visual materials are licensed under CC BY-NC-SA 4.0 (see LICENSE-DOCUMENTATION.md). Commercial use requires a separate written agreement with Toni Mladenovski, including agreed financial terms: info@eitnetworks.org (see COMMERCIAL-USE-POLICY.md). Please cite as described in CITATION.cff.
```
This supersedes the NOTICE wording in V0.5 and Tasklet's earlier proposal.

## Files in the release
- `LICENSE`: the official text `ffcca388…`, byte for byte, with nothing before or after it.
- `NOTICE`: the text of Decision 5.
- `LICENSE-DOCUMENTATION.md`, `COMMERCIAL-USE-POLICY.md`: consistent with Decisions 2–4.
- The `README.md` "License" section, `CITATION.cff` (`license: PolyForm-Noncommercial-1.0.0`) and `zenodo/zenodo_metadata.json` must be consistent with this record.

## Not granted by this text
- No code changes to pinned files.
- No gate closure, no freeze, no GitHub push, no Zenodo upload.

Statuses unchanged: PHASE_1 OPEN · GATE_4 NOT_SATISFIED · FORMAL_FREEZE NO · GITHUB HOLD · ZENODO BLOCKED.

Author: Toni Mladenovski
