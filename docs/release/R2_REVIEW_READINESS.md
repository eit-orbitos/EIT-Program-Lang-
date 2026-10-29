# R2 research-candidate handoff / independent review checklist

**R2 created from exact R1 only with approved AUD-06 documentary exclusions and release-layer reindexing.**

The proposed research-release version is `2.7.7-research.1`; the proposed GitHub pre-release tag `v2.7.7-research.1` has **not** been created or reserved. R2 is a *new ZIP byte identity* and must not inherit the R1 ZIP hash or a claim that R2 runtime tests passed.

Independent reviewer should verify:

1. Complete R2 ZIP SHA-256 against the detached receipt; archive CRC, full file inventory and all root `SHA256SUMS.txt` lines.
2. `ARTIFACT_REGISTRY.json` matches every included file except itself and root manifest; root manifest pins registry; no circular self-digest.
3. Exact six AUD-06 file paths removed, with no deletion beyond the six and disclosed release-layer edits/additions; old R1 remains independently preserved.
4. Every `eit_program_lang/`, `tests/`, `reference/` file matches R1 byte-for-byte. Verify existing code pins and preserved normative/spec/test/LICENCE/NOTICE files by digest.
5. All historical references to deleted files are treated as prior evidence links; confirm no release-facing claim requires those six files to be present. Review licensing and external-reviewer rights.
6. Replay applicable inventory/CI probes against the **exact R2 bytes** only with separate scoped execution approval and exact interpreter/dependency profile. Distinguish `REPLAY_MATCH`, `REPLAY_MISMATCH`, `NOT_RUN`. Do not silently rebind the legacy 127-file V0.3 regression runner.
7. Confirm publication blockers, `RESEARCH_CANDIDATE — NOT FINAL` labels, pre-release tagging and separate GitHub/Zenodo authorization.

### Explicitly preserved known failures and independent-evidence limits

- V0.3 historical regressions: 50 PASS + 1 FAIL (oracle conflict; no test changes).
- P0-03 §2: `sha256_json` helper import/reimplementation normative deviation; sampled probe 99/100, not full spec PASS.
- V0.3 source-specific runner on R1: fail-closed `BLOCKED_SOURCE_INTEGRITY`; same protection is expected on R2, but **not executed** under this authorization.
- RT-02 original application oracle remains separate from pre-S1 OS/IPC denial.
- IR04-P and IR04-O not approved operationally; 55 derived blockers not closed; original 64-row register not independently supplied with Claude audit.

**No project execution was authorized by the R2 creation decision.**
