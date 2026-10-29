# EIT Program Lang V2.7.7 — Research Candidate R2

**RESEARCH_CANDIDATE — NOT FINAL — KNOWN BLOCKERS LISTED**

Author / Founder / Architect: Mr. Toni Mladenovski. Project origin: 18 April 2026.
Version: `2.7.7-research.1`. Proposed tag: `v2.7.7-research.1` (NOT created). Repository: https://github.com/eit-orbitos/EIT-Program-Lang-

```
FINAL_V277_RELEASE = HOLD
C3_E               = NOT_IMPLEMENTED
F01                = 0/19 OPERATIONALLY_VERIFIED
B4                 = NOT_CLOSED
RG6                = OPEN
GATE_4             = NOT_SATISFIED
PUBLICATION        = NOT AUTHORIZED (needs a fresh independent replay + the author's separate final GO)
```

This is research software: a receipt verifier and its builder/runtime candidate. It is not a validated physical theory, not a production deployment and not certified. **SOFTWARE / DOCUMENTARY VALIDATION ≠ PHYSICAL LAW ≠ EXTERNAL SCIENTIFIC VALIDATION.**

## What this package is

The code is the **V2.7.7 Tasklet Fix Candidate V0.3** successor tree, unchanged. The source archive SHA-256 is `b73b15c7fed0ca5aa4e5ce33c97888a29ae49f6a96e99b1f37d836d5f945f027`, and the extracted 127-file tree is `2538c8cb6b56a620455cdee0bcd27ae0e2e94afcf36764fcbbeabb1d0f9c84c1`. Research Candidate R2 changes only the release layer: the docs, the manifest, the registry and one constant in the inventory script. `CHANGELOG.md` lists every change.

| Component | SHA-256 |
|---|---|
| `eit_program_lang/receipt_verifier.py` (and its `_v277_candidate` twin) | `97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca` |
| `eit_program_lang/eit_v277_builder_candidate.py` | `fe305aabe6e4b773ceef5100d8d4eed7a9820f8ba199735e0d3d7cce504be590` |
| `eit_program_lang/restored_registry_index_v277_candidate.py` (companion) | `4ba6556ac456601bf9d91608f28ba950b619c51ac123598aeeb480d24444ad65` |
| `eit_program_lang/s1_sp1_core.py` (added in V0.3) | `a2a9551e9354ee4912aa98567b57685ef4d6fdcbd6721fcf466193185123c7b6` |
| `eit_program_lang/s1_sp1_adapter.py` (added in V0.3) | `caf16413d42a3ffa737b2ea719c38c7d882d27aea5183163c9c52f10542641a3` |
| Verifier contract, P0-03 spec V0.5.9 (immutable) | `3fc10557032bfb2ab4acf2953f9654c5bdc0f32db43aee7cfdd69fd0d384f27c` |
| Release governance, V0.6.0 DRAFT V0.5 | `a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788` |

The RC12 hash (`9326036842…`) and the Option-A hash (`df60039d…`) are **different predecessor artifacts**. They are not aliases of V0.3. The builder hash recorded in the RC12 registry (`3d401c47…`) is also not the V0.3 builder.

## Usage

```python
from eit_program_lang.receipt_verifier import verify_restored_query_receipt
result = verify_restored_query_receipt(receipt, artifact,
    expected_artifact_sha256=trusted_artifact_hash, strict_mode=True)
```

Expected hashes MUST come from a channel the receipt producer cannot write. A verifier PASS does not authenticate the producer and does not replay the query. It is also not evidence that any physical event happened. R-1/R-2/R-3/R-5 can produce `verified=True` by design. See `NON_CLAIMS.md` and `KNOWN_LIMITATIONS.md`.

## Verify locally

Requires **exactly CPython 3.12.15** (Unicode 15.0.0). Other interpreters are refused on purpose.

```sh
python3 tools/ci_inventory_check.py .
sha256sum --strict -c SHA256SUMS.txt
RC11_PYTHON=/path/to/python3.12.15 bash tools/ci_release.sh
```

`ci_release.sh` runs:
- the inventory and content checks;
- a hash-locked dependency install in an external venv;
- the dependency and inventory negative controls;
- the V2.7.6 reference pin;
- the frozen self-checks (v05/v06/v07);
- the two release pytest modules.

It is **not** the full RG-4 suite and not the §11.3/§11.4 tables. A local PASS or a GitHub Actions PASS is CI evidence only. It is not evidence about an owner-controlled or isolated host, and it is not F01/C3-E evidence.

## Evidence (each scoped; do not merge)

- Claude audit 2026-10-29 (`docs/audit/CLAUDE_AUDIT_V2_7_7.md`), run on the exact V0.3 bytes in two clean environments (root user, and a separate non-root UID) on CPython 3.12.15 built from the official tag:
  - self-checks 18/18, 10/10 and 12/12;
  - release pytest 7/7;
  - V2.7.6 legacy pytest 28/28;
  - V0.3 regression suite: **50 PASS + 1 preserved oracle FAIL** (51 tests);
  - independent black-box P0-03 probe: 99/100 (the 1 FAIL is the formal §2 "do not reimplement" deviation);
  - legacy v275 fixture probe: ALL_PASS.
- The prospective V0.4 suite was reported as 55/55 PASS by others. That is a **different scope** and is not merged with the 50+1 result above.
- Earlier Tasklet V1.4 results: 121 spec PASS, 60/61 mutations, TX-M43 separate. These are historical, were run by the author's side and were **not** re-run here.

## Licensing and publication

- Software: PolyForm Noncommercial 1.0.0 (`LICENSE`).
- Author-written documentation: CC BY-NC-SA 4.0.
- `LICENSE-SCOPE.md` lists which file falls under which licence, and the third-party files the package does not licence.
- `LICENSE` and `NOTICE` are byte-unchanged.
- Commercial use requires a separate written agreement.

No tag, push, GitHub release, Zenodo deposit or DOI exists for this candidate. Publication needs a fresh independent replay of these exact bytes **and** the author's separate final approval.


## R2 AUD-06 documentary exclusion (29 October 2026)

This R2 working candidate was generated after author's scoped approval to exclude exactly six historical internal-path files from the proposed public tree. See `docs/release/R2_AUD06_PUBLIC_EXCLUSIONS.md` for the six original paths, original-byte hashes, and the disclosure of historical references. R1 itself is unchanged and separately retained. R1 has an independently reported and documented `REPLAY_MATCH` for its own bytes. **R2 has not undergone independent runtime replay, and is not published.** Prior audit documents retain their original, historical R1 timestamps/status; the R2 addendum is the current release-layer status. No GitHub or Zenodo action is authorized by the R2 build.
