# DIFF LOG — RC11 revision 2 → RC12

Base: RC11 revision 2, archive SHA-256 `b7044de29f42616200b262fe597c2e98a8b4a723f575c3145d78a5a787bb2cee` (121 files).
Author instruction: "GO — TASKLET EIT V2.7.7 RC12 FINAL PREPARATION" (Mr. Toni Mladenovski, 24 October 2026). Isolated build; no publication.

## Unchanged protected bytes

- `LICENSE` `ffcca38841adb694b6f380647e15f17c446a4d1656fed51a1e2041d064c94cc8`
- `docs/EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.9.md` `3fc10557032bfb2ab4acf2953f9654c5bdc0f32db43aee7cfdd69fd0d384f27c`
- `docs/EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.6.0_DRAFT_V0.5.md` `a753ece9932c43937c58349dc580f59e2eafcb544b408cf3f8194a2ed2235788`
- `eit_program_lang/eit_v277_builder_candidate.py` `3d401c47e49f9abb5f94d95480bf6dff157e0be17ff0b0eadbfcac86d6898cec`
- `eit_program_lang/receipt_verifier_v277_candidate.py` `97b1d148d11490e2105dc4ceee68d1fc19ac72bff79378fe866e97db6bd072ca`
- `eit_program_lang/restored_registry_index_v277_candidate.py` `4ba6556ac456601bf9d91608f28ba950b619c51ac123598aeeb480d24444ad65`
- `reference/EIT_V2_7_6.zip` `3b99157ebf878dff57eba2c6da755720f07f3a80b9c85dd1db0e6a565408e22c`
- `NOTICE`, `COMMERCIAL-USE-POLICY.md`, `NON_CLAIMS.md`, `KNOWN_LIMITATIONS.md`, all `docs/` records, all `tests/` files including frozen fixtures, `.github/workflows/verify.yml`, `tools/ci_release.sh`, `tools/ci_inventory_negative_controls.py`: byte-identical.

## Added

- `LICENSE-SCOPE.md` `f15079f793635cf6fa7d05b6aebcb70a9f271a955b09f451a59bc0b54a808670`
- `docs/LICENSE_PROVENANCE_V2.7.7.md` `795167129d297afa1268f975399d2779ae3dbd1324aaffac6f00161fea5ecc2c`
- `DIFF_LOG_V11_TO_V12.md` (this file; hash in root SHA256SUMS.txt)

## Modified (RC11 → RC12)

- `README.md` `6bff21c67382c156bcb50c7ec3f2edfa7b879ae10afeb4cd47db1e75e8dfe52e` → `c98a8b3732b3897218544fcc35f619f076c7f42e9bbf3870daccbeb8603e3097` — RC12 identity, tag name, RC12 lineage paragraph, license-scope pointers
- `CITATION.cff` `a1e1cd75b98d051563f212e2a5919b8f5d3fcf4e8f4533861ff0797ed5c709c1` → `f2ce6af49fe1552b836617808efdce8e296f98c8033f05ed3e3a6ab66a51c4a9` — title and version RC12; single software license retained
- `zenodo/DESCRIPTION.md` `2784b9e1f063a005527f53d4624317abc66afdf14b51802895856166d27c2ff5` → `7e456f75b7f575c626acc6cd81e2c5238db9a983a6b9105c2b1ce6d9e6588845` — RC12 title; two-domain licensing paragraph appended
- `zenodo/zenodo_metadata.json` `68b809b5a5a855779c59f0cd82f2f77c1e0e2907f846a5c406e0436407a39b54` → `4608cc7ae40656c6f0d2ec2d2ff48501044750b5d814b25c12d90f91dd3645ee` — title/version RC12; notes: proposed tag/relation text RC11→RC12, extended (scope file, 23544132 distinction)
- `LICENSE-DOCUMENTATION.md` `abdd8843cbcd6cbb8e2ebf1a08f03fb837f1412b4a31f5e75f06c85b1ccf04e2` → `1fa52483060c0fe82c2f6a1c30c16642caa851f8d657971e78207148cbbaa4ba` — RC11 bytes kept as exact prefix; one pointer sentence to LICENSE-SCOPE.md appended
- `tools/ci_inventory_check.py` `8d6e88b1ed458a568ccd1ef50b3e0e5796ea4e326cd9f620b796f835cb85d600` → `7f3740d671fca1f2c06d9f8bace10c210678bc8996597d334783f6dd0fe2466a` — version constant '2.7.7-rc11'→'2.7.7-rc12' (required by RC12 metadata); LICENSE-SCOPE.md added to REQUIRED
- `ARTIFACT_REGISTRY.json`, `SHA256SUMS.txt`: regenerated (hashes recorded externally to avoid cycles).

## Not changed on purpose

- `LICENSE`: formatting-only difference from the Zenodo 23544132 / repository-main copy; no necessity to alter locked bytes (author Decision 1).
- Workflow name "RC11 limited-release candidate validation" and the `eit-rc11-ci` temp-dir prefix in `tools/ci_release.sh`: cosmetic, left to avoid touching CI execution files.
- `docs/RELEASE_GOVERNANCE_RC11.md`, `RELEASE_NOTES_V2.7.7.md`, `RELEASE_CHECKLIST.md`: historical RC11 records; governance content applies unchanged.

Statuses unchanged: RG6 OPEN · PHASE_1 OPEN · GATE_4 NOT_SATISFIED · FORMAL_FREEZE NO · GITHUB HOLD · ZENODO BLOCKED.
