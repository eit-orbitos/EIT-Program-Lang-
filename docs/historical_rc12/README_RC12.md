# EIT Program Lang V2.7.7 — RC12 LIMITED/research release candidate

Author / Founder / Architect: Mr. Toni Mladenovski. Project origin: 18 April 2026.

**Prepared, not published. RG6 OPEN · PHASE_1 OPEN · GATE_4 NOT_SATISFIED · FORMAL_FREEZE NO.**
Proposed tag: `v2.7.7-rc12` (NOT created). Repository: https://github.com/eit-orbitos/EIT-Program-Lang-

RC12 = RC11 revision 2 (archive SHA-256 `b7044de29f42616200b262fe597c2e98a8b4a723f575c3145d78a5a787bb2cee`) plus licensing-scope and metadata alignment only. Verifier, builder, companion, both specifications, frozen fixtures, `LICENSE` and `NOTICE` are byte-identical to RC11. See `DIFF_LOG_V11_TO_V12.md`.

This is a software receipt-verifier candidate, not a validated physical theory. **SOFTWARE / DOCUMENTARY VALIDATION ≠ PHYSICAL LAW ≠ EXTERNAL SCIENTIFIC VALIDATION.**

## Exact implementation and governance

- Verifier SHA-256: `97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca`.
- Builder SHA-256: `3d401c47e49f9abb5f94d95480bf6dff157e0be17ff0b0eadbfcac86d6898cec`.
- Companion SHA-256: `4ba6556ac456601bf9d91608f28ba950b619c51ac123598aeeb480d24444ad65`.
- Immutable verifier-contract baseline V0.5.9 SHA-256: `3fc10557032bfb2ab4acf2953f9654c5bdc0f32db43aee7cfdd69fd0d384f27c`.
- Ratified release-governance amendment V0.6.0 DRAFT V0.5 SHA-256: `a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788`.

Both specifications are copied unchanged to `docs/`. V0.6.0's internal pending label is historical; the exact-byte ratification record is supplied separately in `docs/author_decisions/`. This amendment does not replace the pinned verifier contract or close other gates.

## Usage and limitations

```python
from eit_program_lang.receipt_verifier import verify_restored_query_receipt
result = verify_restored_query_receipt(receipt, artifact,
    expected_artifact_sha256=trusted_artifact_hash, strict_mode=True)
```

Expected hashes MUST come from a channel the receipt producer cannot write. Computing an anchor from the same untrusted artifact is not independent provenance. Keyless hashes, self-declared stamps and timestamps do not authenticate a producer or prove an event. R-1 index hashes, R-2 unreplayed query/source resolution, R-3 jointly rewritten artifact/receipt, and R-5 stamp downgrade remain explicit risks. Even anchored assurance is not producer/version authentication. See complete `NON_CLAIMS.md`, `KNOWN_LIMITATIONS.md`, and `docs/RELEASE_GOVERNANCE_RC11.md`.

## Evidence, without overclaim

- Earlier Tasklet V1.4: 121 spec PASS; S4d NOT_APPLICABLE; K1 RISK_PRESENT. Separate 21 TX PASS.
- V1.4 mutation result: **60/61**. M43 is detected by separate TX-M43 V0.2, not by V1.4 itself.
- Author-closed, scope-limited: M36/TX-N2a, M55/TX-N2b, M61/TX-N1; M43 closed with private-class limitation.
- N-8(b): local evidence satisfied, NOT GitHub Actions evidence. Historical V0.9 strict check is 82/82; rc10 is 85/85. RC11/RC12 counts/results are recorded in the external candidate-bound audit, not preclaimed here.
- Existing execution was author-side Tasklet work. Independent runtime reproduction is not established.
- §7 audit tests and audit mutants M1/M6/M10/M12/M13/M15/M16 are not assigned PASS. See the current final reconciliation matrix for conditional LIMITED-release treatment.

## One canonical release inventory and CI

`SHA256SUMS.txt` is the only current root content manifest for both local and GitHub CI. Run:

```sh
python3 tools/ci_inventory_check.py .
sha256sum --strict -c SHA256SUMS.txt
bash tools/ci_release.sh
```

The shared script requires CPython 3.12.15, creates a clean external virtualenv, installs exact hashed wheel dependencies, runs release-layer negative controls, frozen candidate self-checks, two pytest modules and final inventory/content checks. It is **not** the full RG-4 suite. GitHub checkout/setup actions cannot be emulated by claiming local PASS.

Runner label `ubuntu-24.04` is fixed by distribution, not an immutable image. Action commit pins were read-verified through GitHub; they were not executed here. Future GitHub evidence must record actual runner/tool versions and credential behavior. No token should be printed. `persist-credentials: false` is explicit.

Root manifest excludes only itself and a real root `.git/` directory; no cache/bytecode exceptions. Nested manifest-named files must be listed. Historical manifests in `docs/` and fixtures are preserved evidence with their original domains, not alternative RC12 release inventories. `ARTIFACT_REGISTRY.json` is derived descriptive metadata, not a competing validation source.

## Licensing and publication

LICENSE and NOTICE are byte-unchanged (author license decision V0.1). Software: PolyForm Noncommercial 1.0.0; documentation: CC BY-NC-SA 4.0 — the same framework the author uses for EIT Analyzer Lambda V4.2.1 (Zenodo record 23544132, a different work). File-by-file application and the third-party/external-reviewer files that this package does not license: `LICENSE-SCOPE.md`. Provenance and the LICENSE formatting comparison: `docs/LICENSE_PROVENANCE_V2.7.7.md`. Commercial use requires the governed separate agreement. No DOI is assigned to RC12 and no tag, push, GitHub release or Zenodo deposit has been made. Publication remains blocked by governance; a successful local check is not publication permission.
