# CLAUDE_AUDIT_V2_7_6

```
PROJECT:     EIT Program Lang
BASELINE:    V2.7.5  (GitHub eit-orbitos/EIT-Program-Lang- @ 2b7dd628de411b5bb421310ead16b998d61a7f54)
CANDIDATE:   V2.7.6  (EIT_V2_7_6.zip, sha256 3b99157e…408e22c)
AUDIT TYPE:  Static security, correctness & architecture, with execution
ROLE:        Independent reviewer (Claude)
DATE:        2026-10-08 (America/Chicago)

FINAL VERDICT:          NEEDS_FIX
FORMAL_FREEZE:          NO
ZENODO_PUBLICATION:     NOT_AUTHORIZED
SCIENTIFIC_VALIDATION:  NOT_CLAIMED
```

This is an independent software audit. It is not approval for deployment or publication.

---

## 1. Verdict in brief

V2.7.6 is a real improvement. The four high-severity V2.7.5 findings are fixed on the paths they were reported on, the fail-first claim is true (7 regression tests fail on `2b7dd62`, pass on the candidate), and every self-reported number reproduces.

It is still NEEDS_FIX, for three reasons:

1. **A silent, order-dependent pick remains on the source side of translation (N-1, HIGH).** Two artifacts with the *same* `frozen_artifact_sha256` return different translations for the same query (`БАНКА` vs `БРЕГ`). The V2.7.6 fix covered only target candidates.
2. **The receipt verifier accepts forged content (N-2, MEDIUM) and the runtime raises unhandled exceptions on malformed state instead of failing closed (N-3, MEDIUM).** Both contradict what the module docstrings claim.
3. **The test suite does not pin several of the fixes it reports.** Of 17 single-line reverts of V2.7.6 logic, 8 pass all 33 tests and both demos (§6). That includes the `registry_history` fix and the "state hash is mandatory" fix.

One operational item needs attention before any upload: **the new CI inventory step will fail if the candidate is uploaded on top of the current GitHub tree** (N-8a), because two `.gitkeep` files tracked at `2b7dd62` are not in the candidate's manifest.

---

## 2. Scope, method, evidence classes

### 2.1 Inputs

| Item | Source | Identity check |
|---|---|---|
| Baseline V2.7.5 | `git clone` + `git checkout 2b7dd62` (done earlier in this review) | `sha256sum -c` 27/27 OK |
| Candidate V2.7.6 | `EIT_V2_7_6/` inside the uploaded archive | Byte-identical to `EIT_V2_7_6.zip` and to `EIT_CHATGPT_NEW_CHAT_HANDOFF_V1/candidate/EIT_V2_7_6` (`diff -r`) |
| Handoff baseline copy | `…HANDOFF_V1/baseline/EIT_V2_7_5` | Identical to git `2b7dd62` except it lacks `eit_program_lang/.gitkeep` and `tests/.gitkeep.` |
| Uploaded archive | `Kimi_Agent_V2.7.4_Restored_Registry15.zip` | sha256 `4165fd4f…91af126` |

### 2.2 Environment

Linux 6.18, Python 3.12 (as CI) and 3.13.16, pytest 9.1.1, GNU coreutils 9.4. All execution ran against **throwaway copies**. The candidate directory was re-verified after the audit (`sha256sum -c` clean, 29 files, zip hash unchanged). No source file was modified and no manifest was regenerated.

### 2.3 Evidence classes used below

- **VERIFIED**: I ran it or read it at the cited line.
- **AUTHOR-REPORTED**: stated in `EIT_V2_7_6_IMPLEMENTATION_REPORT.md`, `CONTINUITY.md`, `CHANGELOG.md` or the handoff package; not independently established.
- **NOT_RUN**: not checked.

### 2.4 A note on the "eight findings"

The handoff package states that my V2.7.5 review text is `ORIGINAL_UNAVAILABLE` and that findings 5–8 were "reconstructed from the fixes that were mapped to them" (`03_OPEN_FINDINGS.md`). The reconstructed list is not the list I reported. This audit uses my original eight, labelled O-1…O-8.

| Original (my V2.7.5 review) | Package's reconstructed # |
|---|---|
| O-1 target ambiguity → `candidates[0]` | 1 |
| O-2 Unicode NFC not wired in; vacuous NFC test | 2 |
| O-3 mutation guard: battery mutates a copy, result hard-coded, runtime not gated | 3 |
| O-4 `registry_history` fallback outside the artifact hash | 4 |
| O-5 keyless hashes: tamper + recompute passes (state and receipt) | **not in the table** (listed only as a "known limit") |
| O-6 optional checks: state hash skippable; receipt source artifact optional | 5 (receipt half only) |
| O-7 CI coverage: added files, `.gitkeep`, print-only demo, hard-coded `f5`, constant guard | 6, 7, 8 |
| O-8 documentation/version drift | **not in the table** |

Also, `audit/KIMI_VERIFICATION_OF_CLAUDE_FINDINGS.md` records a "detail correction" saying my report claimed `verify_restored_state` returned True after injection. My report said the opposite: the verifier catches it, the runtime does not call it. The underlying defect was understood correctly either way.

---

## 3. Reproduction of the candidate's own claims

| # | Command (run in a copy of `EIT_V2_7_6/`) | Outcome | Status |
|---|---|---|---|
| R1 | `sha256sum -c SHA256SUMS` (also with `--strict`) | 28/28 OK, exit 0 | VERIFIED |
| R2 | Registry self-hash + binding script from `verify.yml:77-100` | `e998db3b…2c027f3` matches; 27/27 bindings; registry hashes equal on-disk bytes | VERIFIED |
| R3 | `python -m pytest tests/ -q` | `33 passed` on 3.12 and 3.13 | VERIFIED |
| R4 | `python3 demo_v2_7_4.py` | 6/6, `assert` executed, exit 0 | VERIFIED |
| R5 | `python3 demo_v2_7_5.py` + report assertion | 8/8 true, exit 0 | VERIFIED |
| R6 | Copy `tests/test_v276_regressions.py` into baseline `2b7dd62`, run it | `7 failed` | VERIFIED |
| R7 | Inventory step (`verify.yml:40-73`) in a fresh git repo of the candidate | `inventory coverage OK: 29 tracked files, 28 manifest entries`, exit 0 | VERIFIED |
| R8 | Anchors in the implementation report §2 | `EIT_V2_7_6.zip`, diff file, `SHA256SUMS`, `ARTIFACT_REGISTRY.json`, `.gitignore`, `registry_sha256` all match. **`verify.yml` does not** (see N-11) | VERIFIED |
| R9 | Action pins | `git ls-remote`: `actions/checkout` v4.2.2 = `11bd7190…`, `actions/setup-python` v5.6.0 = `a26af69b…`; both match `verify.yml:26,28` | VERIFIED |
| R10 | GitHub CI run for V2.7.6 | Candidate is not published; no run exists | NOT_RUN |

---

## 4. Status of the eight original findings

| ID | Original severity | V2.7.6 status | Short reason |
|---|---|---|---|
| O-1 | High | **RESOLVED (target side)** | Source side still picks silently → N-1 |
| O-2 | High | **RESOLVED (surfaces)** | `symbol_id` keys not normalized → N-5; vacuous test still present |
| O-3 | High | **PARTIAL** | Serving is gated; battery is still tautological; state still mutable → N-7 |
| O-4 | High | **RESOLVED in code, NOT covered by tests** | Reverting the fix passes 33/33 |
| O-5 | Medium | **NOT RESOLVED** | Acknowledged as a limit; receipt verifier also skips checks it could do → N-2 |
| O-6 | Medium | **RESOLVED in code; state-hash half untested** | Reverting it passes 33/33 |
| O-7 | Medium | **MOSTLY RESOLVED** | Inventory step works; new CI issues → N-8 |
| O-8 | Low | **MOSTLY RESOLVED** | Version strings fixed; new anchor mismatch → N-11 |

### O-1: silent `candidates[0]` on ambiguous target

- **Baseline evidence:** `frozen_translation_lookup.py:103` (`target = candidates[0]`).
- **Candidate:** `frozen_translation_lookup.py:122-139` routes candidates through `resolve_ambiguous_candidates` (`unicode_normalization.py:54-78`) and returns `AMBIGUOUS_NO_SILENT_PICK` with `translation_packet = None`.
- **Reproduction:** registry with `BANK` (LATIN) and two CYRILLIC records `БАНКА`/`БРЕГ` in the same role; `lookup_translation_from_frozen_registry(state, "BANK", "CYRILLIC")` → `('AMBIGUOUS_NO_SILENT_PICK', None)`. VERIFIED.
- **Test coverage:** adequate. Reverting to `candidates[0]` is caught (mutant M5 killed).
- **Remaining risk:** the same defect exists one step earlier, in source resolution (N-1), and identical surfaces with different meanings are auto-resolved (N-9).

### O-2: NFC normalization not on the runtime path

- **Candidate:** `nfc()` added at `restored_registry_index.py:44-46`; applied to index keys (`:102-116`), query input (`restored_registry_query.py:47`), blob fields (`:100-104`), and source/role/family resolution (`frozen_translation_lookup.py:38,46,53-59,99-106`).
- **Reproduction:** record stored NFC `ЌЕРКА`, query NFD → `found: True`, translation resolves. Record stored NFD, query NFC → also found. VERIFIED.
- **Test coverage:** partial. Query-side reverts are caught (M4, M8, M9 killed). Dropping NFC from index keys is **not** caught (M12 survived), because no test stores a record in NFD.
- **Remaining:** `tests/test_translation_edge_cases.py:37-39` is unchanged and still vacuous (`ИЗВОР` has no decomposable characters). `symbol_id` is excluded from normalization and regressed (N-5). There are now two `nfc()` definitions (`restored_registry_index.py:44`, `unicode_normalization.py:18`).

### O-3: mutation guard gives no protection

- **Candidate, fixed part:** integrity gate at `restored_registry_query.py:30-42` and `frozen_translation_lookup.py:71-81`. In-place write then query → `INTEGRITY_CHECK_FAILED`; translation → `('INTEGRITY_CHECK_FAILED', None)`. VERIFIED. Removing either gate is caught (M2, M3 killed).
- **Candidate, unfixed part:** `deep_mutation_guard.py` is functionally identical to V2.7.5.
  - `:42` still mutates `copy.deepcopy(restored_state)`, so `:51-52` (`intact = before == after`) cannot be false.
  - `:61` still hard-codes `"mutation_applied_to_frozen": False`.
  - Running the battery on an **already tampered** state returns `intact = True`, `applied = False`. VERIFIED.
  - Forcing `intact = True` passes all tests and both demos (M16 survived). `f2_battery_intact` in the adversarial report therefore cannot fail.
  - `tests/test_deep_mutation_guard.py:8-25` still uses an unverifiable fixture (`"f" * 64`, no state hash).
- **Resolved?** Partially. The serving path is protected by detection; the "guard" is still not evidence of anything.
- **Recommended correction:** have the battery run each attack against the real object through the public API and assert the gate refuses to serve afterwards, or delete the battery and report the gate tests instead. Derive `mutation_applied_to_frozen` from a comparison.

### O-4: `registry_history` fallback

- **Baseline evidence:** `restored_registry_index.py:60-66`.
- **Candidate:** `extract_records_from_restored_state(..., allow_history_fallback=False)` at `restored_registry_index.py:60-82`; no caller passes `True`.
- **Reproduction:** empty artifact + `registry_history` containing records, state **re-sealed** so the gate passes → `verified: True`, query `NO_MATCH`, translation `NO_SOURCE_MATCH_IN_FROZEN_REGISTRY`. VERIFIED: the fix works.
- **Test coverage: inadequate.** `tests/test_v276_regressions.py:99-108` and `:110-122` add `registry_history` at lines 101 and 112 **after** the state was sealed. The query is rejected by the state-hash gate (`RESTORED_STATE_HASH_MISMATCH_TAMPER_DETECTED`), not by the fallback default. Flipping the default back to `True` passes 33/33 (M1 survived).
- **Recommended correction:** re-seal the state in both tests and assert `verify_restored_state(st)["verified"] is True` first. Remove the unused `allow_history_fallback` parameter, or gate it.

### O-5: keyless hashes prove consistency, not authenticity

- **Candidate:** unchanged by design; implementation report §4 lists it as a known limit. It is absent from the `CONTINUITY.md` resolution table.
- **Reproduction:** edit a record, delete another, recompute `frozen_artifact_sha256` and `restored_state_sha256` → `verified: True`, runtime serves `EVIL`. VERIFIED.
- **Resolved?** No. Accepting this as a limit is reasonable **only if** the runtime can be given a trusted anchor. Today no function takes one.
- **Recommended correction:** add an `expected_artifact_sha256` parameter (or pinned constant) to `verify_restored_state` and the two serving entry points, so that a caller holding the out-of-band anchor can enforce it. Without that, "INTEGRITY_CHECK" means "internally consistent".

### O-6: checks that could be skipped

- **Candidate:** `integrity_verifier.py:81-87` makes `restored_state_sha256` mandatory; `receipt_verifier.py:50-51` makes `source_frozen_artifact` mandatory.
- **Reproduction:** state without the hash → `['RESTORED_STATE_HASH_MISSING_OR_MALFORMED']`; receipt without source → `['SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK']`. VERIFIED.
- **Test coverage:** receipt half is covered (M7 killed). State half is **not**: making the hash optional again passes 33/33 (M6 survived), and ignoring a state-hash mismatch also passes 33/33 (M10 survived), because every tamper test also breaks the artifact hash.

### O-7: CI and demo coverage

- **Fixed and VERIFIED:** inventory step detects an unlisted tracked file (exit 1); both demos end in real assertions (`demo_v2_7_4.py` tail, `demo_v2_7_5.py:125-126`); `f5_boundary_declared` is computed (`demo_v2_7_5.py:116-120`); `mutation_guard.py:37` states the unconditional deny plainly.
- **Remaining:** `f5` compares a module constant with itself, so it is still always true; `check_frozen_mutation` is still called only by a demo. New CI issues are in N-8.

### O-8: documentation drift

- **Fixed and VERIFIED:** `__init__.py`, module headers, `receipt_version`, `module_id`, `packet_version`, `CONTINUITY.md` commands and governance fields.
- **Remaining:** see N-11.

---

## 5. New findings in V2.7.6

Severity scale: HIGH = wrong or attacker-chosen output served as valid; MEDIUM = a stated guarantee does not hold, or a likely operational failure; LOW = hardening and accuracy.

### N-1 (HIGH): source resolution still picks silently and depends on insertion order

- **Affected code:** `frozen_translation_lookup.py:45-62` (`_resolve_source`). It returns the first record, in dict insertion order, whose `visible_symbol`, any alias, or `sound_hint` matches. All three match types are tried per record, so an alias on an earlier record beats an exact `visible_symbol` on a later one.
- **Reproduction (VERIFIED):**
  - Records `FIN` (`BANK`, role FINANCE), `GEO` (`BANK`, role GEOGRAPHY), `C1` (`БАНКА`, FINANCE), `C2` (`БРЕГ`, GEOGRAPHY).
  - Insertion order `FIN, GEO` → `TRANSLATED_FROM_FROZEN_REGISTRY`, `БАНКА`. Order `GEO, FIN` → `TRANSLATED_FROM_FROZEN_REGISTRY`, `БРЕГ`.
  - `artifact_sha256` is **equal** for both orders (it uses `sort_keys=True`), the gate reports `verified: True`, and `detect_registry_conflicts` reports `conflict_free: False` but is not consulted.
  - Alias case: record `A` (`RIVER`, alias `bank`) before record `B` (`BANK`): query `BANK` → `РЕКА`.
- **Why it matters:** this is O-1 again, one step earlier. It also breaks the provenance claim: the same frozen-artifact hash does not determine the answer.
- **Recommended correction:** collect all source matches, rank by match type (id > visible > alias > sound hint), and return `AMBIGUOUS_SOURCE_NO_SILENT_PICK` when more than one record remains in the top tier with different roles. Iterate records in sorted `symbol_id` order everywhere.

### N-2 (MEDIUM): receipt verifier accepts forged or meaningless receipts

- **Affected code:** `receipt_verifier.py:23-67`; `restored_query_receipt.py:25-69`.
- **Reproduction (VERIFIED):**
  1. Build a valid receipt, set `translation_packet.target_visible_symbol = "FORGED"` (a value not in the artifact), recompute only `receipt_sha256` → `verified: True, failures: []`. The packet's own `packet_sha256` is now wrong and is never checked.
  2. Build a receipt from a tampered state: inner statuses are `INTEGRITY_CHECK_FAILED`, yet the verifier returns `verified: True` against the original artifact.
  3. Call `build_restored_query_receipt` with a hand-written dict and no query at all → `verified: True`.
- **Why it matters:** the source artifact is now mandatory, so the verifier has everything it needs to check content, and it checks only one hash field.
- **Recommended correction:** in the verifier, recompute `packet_sha256`; reject receipts whose inner status is `INTEGRITY_CHECK_FAILED`; confirm that every `symbol_id`/`visible_symbol` in the receipt exists in the supplied artifact (or replay the query against it). Gate `build_restored_query_receipt` with `verify_restored_state`.

### N-3 (MEDIUM): malformed state raises instead of failing closed

- **Affected code:** `restored_registry_index.py:70-72` (chained `.get`), `:104` (alias loop); `integrity_verifier.py:29-32` (`json.dumps` without `default`), `:73`, `:89-95`; `receipt_verifier.py:29,40-47`.
- **Reproduction (VERIFIED):** 12 of 15 malformed inputs raise an unhandled exception from `query_restored_registry`:

| Input | Result |
|---|---|
| `restored_state` is `None` / a list | `AttributeError` |
| `frozen_artifact` is a string / a list | `AttributeError` |
| `frozen_registry_snapshot` is `None` | `AttributeError` |
| `registry_records` is a list | `AttributeError` |
| a record is a string | `AttributeError` |
| a `set` anywhere in the artifact | `TypeError` |
| a lone surrogate (`"\ud800"`, valid in JSON as an escape) in a record | `UnicodeEncodeError` |
| `aliases: 5` in a correctly sealed state | `TypeError` |
| receipt is `None`, or `boundary` is a string | `AttributeError` |

- **Why it matters:** every module header says "Fail-closed". An exception does stop serving, but it is not the documented `INTEGRITY_CHECK_FAILED` result, and a single crafted record can crash any caller.
- **Recommended correction:** validate shape at the top of `verify_restored_state` (types of state, artifact, snapshot, records, each record, list-typed fields) and wrap hashing in `try/except (TypeError, ValueError)` that appends a failure. Do the same in the receipt verifier.

### N-4 (MEDIUM): canonical serialization is not canonical

- **Affected code:** `integrity_verifier.py:29-32` (`artifact_sha256`); four copies of `sha256_json` (`restored_registry_index.py:49-57`, `frozen_translation_lookup.py:23-31`, `integrity_verifier.py:21-26`, `restored_query_receipt.py:14-22`).
- **VERIFIED observations:**
  - Record key `1` (int) and `"1"` (str) give the **same** `artifact_sha256`.
  - `default=str` makes distinct values collide: a `date(2026,1,1)` and the string `"2026-01-01"` hash identically.
  - `NaN`/`Infinity` are accepted (non-standard JSON).
  - Mixed-type keys raise `TypeError` from `sort_keys`.
  - Two different encodings are in use: `artifact_sha256` uses default separators and no `default`; `sha256_json` uses compact separators and `default=str`.
  - `index_sha256` changes with record insertion order while `artifact_sha256` does not (`restored_registry_index.py:97-116` builds lists in iteration order).
  - Hashes are taken over un-normalized text, so an NFC and an NFD artifact behave identically at query time but have different hashes.
  - `generated_at_utc` (`restored_query_receipt.py:33`) makes every receipt hash unique; fine, but it means receipts are not reproducible evidence.
- **Recommended correction:** one `canonical_json()` in one module: `sort_keys=True`, compact separators, `ensure_ascii=False`, `allow_nan=False`, **no** `default`, reject non-`str` keys, NFC-normalize strings before hashing, sort index lists. Use it for all five hashes. Treat the change as a hash-format version bump.

### N-5 (MEDIUM): `symbol_id` lookups regressed for non-NFC keys

- **Affected code:** `restored_registry_index.py:98` (key stored raw); `restored_registry_query.py:47,55,71` and `frozen_translation_lookup.py:46-48` (query normalized, compared with raw keys); `restored_registry_query.py:99` (raw id in blob).
- **Reproduction (VERIFIED):** record keyed by NFD `ЌЕРКА`. `query(mode="symbol_id")` with the NFD string → `found: False`; with NFC → `found: False`. Translation by id → `NO_SOURCE_MATCH`. In V2.7.5 the exact-bytes NFD lookup succeeded, so this is a regression.
- **Recommended correction:** build a normalized `symbol_id` map (`nfc(id) → id`), reject registries where two ids collide after NFC, and look ids up through it.

### N-6 (MEDIUM): `None` fields become the text `"None"`

- **Affected code:** `frozen_translation_lookup.py:53,59` and `unicode_normalization.py:65` (`nfc(x)` is `normalize(str(x))`); `integrity_verifier.py:91-93` checks only that required keys exist.
- **Reproduction (VERIFIED):** a record with `sound_hint: None` is returned as the source for query `"none"` and translated. A record with `visible_symbol: None` passes the gate and is returned for query `"None"`.
- **Recommended correction:** require required fields to be non-empty `str`; make `nfc()` reject non-strings rather than coerce.

### N-7 (MEDIUM): "frozen" state is mutable and several entry points are ungated

- **Affected code:** `restored_registry_query.py:113,123` and `frozen_translation_lookup.py:162-163` return live record objects; `build_restored_registry_index` (`restored_registry_index.py:85`), `detect_registry_conflicts` (`unicode_normalization.py:22`), `registry_surface_sha256` and `build_restored_query_receipt` do not call the gate.
- **Reproduction (VERIFIED):** `query(...)["records"][0]["visible_symbol"] = "X"` changes the state in place; the next query returns `INTEGRITY_CHECK_FAILED`. `build_restored_registry_index` on a tampered state indexes the tampered value while reporting `restored_registry_remains_frozen: True`.
- **Why it matters:** immutability is asserted by `SAFETY_BLOCK` on every result but enforced nowhere. A well-behaved caller can corrupt its own registry by editing a result. The gate also re-hashes the whole state and rebuilds the index on every call (cost grows with registry size).
- **Recommended correction:** verify once and return a frozen view (`MappingProxyType` plus tuples, or a deep copy held in a small `VerifiedRegistry` object that owns the index); return copies from queries; route every public function through that object.

### N-8 (MEDIUM): GitHub Actions workflow and manifest handling

Positive, VERIFIED: actions are pinned to full commit SHAs that match their tags; `permissions: contents: read`; no secrets; no publish or release step; `pull_request` (not `pull_request_target`).

| # | Issue | Evidence | Recommended correction |
|---|---|---|---|
| a | **Uploading the candidate over the existing repo fails CI.** `2b7dd62` tracks `eit_program_lang/.gitkeep` and `tests/.gitkeep.`; the candidate's manifest lists neither. | Simulated: commit baseline, overlay candidate, run step → `TRACKED BUT NOT IN MANIFEST: ['eit_program_lang/.gitkeep', 'tests/.gitkeep.']`, exit 1 | Delete both files in the same commit, or add them to the manifest (that changes `SHA256SUMS`, the registry and all anchors) |
| b | `sha256sum -c` runs without `--strict` (`verify.yml:36`). A malformed line is skipped with a warning. | Corrupted the `ARTIFACT_REGISTRY.json` line and the file: exit 0 non-strict, exit 1 with `--strict` | Use `sha256sum --strict -c`; also assert the line count |
| c | Inventory parsing uses `.stdout.split()` (`verify.yml:54-56`). Paths with spaces are split; non-ASCII paths are C-quoted by git (`"tests/\321\202…"`). | Both fail closed today, but a Cyrillic or Hanzi filename will produce a confusing false failure | `git -c core.quotepath=off ls-files -z` and split on `\0` |
| d | `pip install pytest` is unpinned (`:33`); `ubuntu-latest` floats (`:24`). | The same commit can produce different CI results over time | Pin `pytest==<version>` with `--require-hashes`; pin the runner image |
| e | `actions/checkout` keeps the token in `.git/config` (`:26`). | Low risk with read-only permissions | `with: persist-credentials: false`; add `timeout-minutes` |
| f | `ARTIFACT_REGISTRY.json` is bound only by its manifest line; `SHA256SUMS` is bound by nothing in the repo. Workflow, manifest and registry live in the same commit. | Anyone with push access can regenerate all three and stay green | Expected. Keep stating it; store the two anchors somewhere the pusher cannot edit (signed tag, protected branch, or Zenodo metadata later) |
| g | The report check selects keys with `startswith("f")` (`:116`, `demo_v2_7_5.py:125`). | Fragile | Use an explicit list of expected keys and assert the count |

### N-9 (LOW): identical surface, different meaning is auto-resolved

- **Affected code:** `unicode_normalization.py:65-71` compares only `visible_symbol`.
- **Reproduction (VERIFIED):** two HANZI records `行` in one role with meanings `walk` and `firm` → `TRANSLATED`, `H1` chosen by id sort; the conflict scan flags the pair but is not part of the gate.
- **Recommended correction:** treat differing `meaning_invariant` as ambiguous; run `detect_registry_conflicts` inside the gate or surface its result in every response.

### N-10 (LOW): case handling

`.lower()`/`.upper()` are used instead of `casefold()` (`restored_registry_index.py:105-116`, `restored_registry_query.py:48-49`). VERIFIED: alias `straße` is not found by `strasse`. Normalization is applied before case mapping and not after. Confusables/NFKC are out of scope (AUTHOR-REPORTED limit, accepted).

### N-11 (LOW): documentation and evidence accuracy

- `EIT_V2_7_6_IMPLEMENTATION_REPORT.md:103` gives the `verify.yml` anchor as `205b026a…b93f8afb`. The file in the package, and its line in `SHA256SUMS`, is `565c9b15…f44df30a`. VERIFIED mismatch; the manifest is right and the report is stale.
- "25 original fixtures upgraded to fully-hashed states" (`CHANGELOG.md`, report Phase B): four test files changed. `tests/test_deep_mutation_guard.py:11` and `tests/test_restored_registry_index.py:9` still use `"f" * 64`.
- The eight-findings table in `CONTINUITY.md` and the handoff package is a reconstruction (§2.4); O-5 and O-8 are missing from it.
- `demo_v2_7_4.py:2,76` still prints the `V2_7_4` banner (acceptable if intentional).

### N-12 (INFO): architecture

- `detect_registry_conflicts`, `check_frozen_mutation`, and `allow_history_fallback=True` are reachable only from demos or tests.
- Four copies of `sha256_json` and two of `nfc` will drift.
- `SAFETY_BLOCK` is a constant copied into every result; its fields describe intent and are not measured. A verifier that checks `boundary.read_only_query_mode is True` (`receipt_verifier.py:41-48`) is checking a constant.

---

## 6. Test adequacy

Method: 17 mutants, each a copy of the candidate with one line of V2.7.6 logic reverted or disabled. A mutant is "killed" if pytest or either demo fails. VERIFIED by execution on Python 3.12.

| Mutant | Reverted behaviour | Result |
|---|---|---|
| M1 | `allow_history_fallback` default → `True` | **SURVIVED** |
| M2 | Integrity gate removed from query | killed |
| M3 | Integrity gate removed from translation | killed |
| M4 | `nfc()` → identity | killed |
| M5 | Ambiguity → `candidates[0]` | killed |
| M6 | `restored_state_sha256` optional again | **SURVIVED** |
| M7 | Receipt source artifact optional again | killed |
| M8 | No NFC on query input | killed |
| M9 | No NFC in translation source resolve | killed |
| M10 | State-hash mismatch ignored | **SURVIVED** |
| M11 | Artifact-hash mismatch ignored | killed |
| M12 | NFC dropped from index keys | **SURVIVED** |
| M13 | Packet provenance check dropped | **SURVIVED** |
| M14 | Record key / `symbol_id` check dropped | killed |
| M15 | Required-field check dropped | **SURVIVED** |
| M16 | Mutation battery always reports intact | **SURVIVED** |
| M17 | Boundary check dropped in receipt verifier | killed |

9 killed, 8 survived (seven distinct gaps plus the battery). Conclusion: the tests prove the headline fixes for O-1, O-2 (query side) and O-3 (gates). They do not pin O-4, the state-hash half of O-6, or the record-shape and packet-provenance checks.

Other observations:

- The claim "no assertion was weakened" is consistent with the diff (VERIFIED by reading all four changed test files): fixtures were upgraded; one assertion changed from a literal hash to the fixture's computed hash.
- No test exercises malformed input, source-side ambiguity, NFD-stored data, or a forged-content receipt.

---

## 7. Proposed regression tests

Delivered as a separate file, `test_v277_proposed.py` (25 test cases; not added to the candidate). Run against a copy of V2.7.6: **6 pass, 19 fail**. VERIFIED.

**Group A: coverage gaps (pass today; each kills a surviving mutant, VERIFIED)**

| Test | Kills |
|---|---|
| `test_history_fallback_not_served_even_when_state_hash_is_valid` | M1 |
| `test_missing_state_hash_blocks_serving` | M6 |
| `test_non_artifact_field_tamper_detected` | M10 |
| `test_record_stored_nfd_is_found_by_nfc_query` | M12 |
| `test_translation_packet_provenance_mismatch_detected` | M13 |
| `test_record_missing_required_field_blocks_serving` | M15 |

**Group B: open defects (fail today; fail-first tests for the next version)**

| Test | Finding |
|---|---|
| `test_source_side_ambiguity_never_silent_and_order_independent` | N-1 |
| `test_exact_visible_symbol_beats_alias_of_earlier_record` | N-1 |
| `test_receipt_with_forged_target_is_rejected` | N-2 |
| `test_receipt_of_failed_integrity_check_does_not_verify` | N-2 |
| `test_malformed_state_fails_closed_without_raising` (7 cases) | N-3 |
| `test_int_and_str_keys_do_not_collide_in_artifact_hash` | N-4 |
| `test_index_hash_independent_of_record_insertion_order` | N-4 |
| `test_symbol_id_lookup_is_nfc_insensitive` | N-5 |
| `test_null_fields_never_match_the_text_none` | N-6 |
| `test_results_do_not_alias_frozen_state` | N-7 |
| `test_index_builder_refuses_tampered_state` | N-7 |
| `test_mutation_battery_detects_in_place_tamper` | O-3 residual (M16) |
| `test_same_surface_divergent_meaning_is_ambiguous` | N-9 |

Also recommended, not written: a CI self-test that adds an unlisted file and expects the inventory step to fail; a test that a non-ASCII tracked filename is handled; replacement of the vacuous `test_unicode_nfc_equivalence` with a string that actually decomposes.

---

## 8. Recommended order of work

1. **Before any upload:** resolve N-8a (`.gitkeep`), add `--strict` (N-8b), correct the `verify.yml` anchor in the report (N-11).
2. **Adopt Group A tests** as-is; they need no code change and close the O-4/O-6 evidence gap.
3. **Fix N-1** (source ambiguity, deterministic iteration) with its two Group B tests failing first.
4. **Fix N-3 and N-6 together** (shape and type validation in the gate).
5. **Fix N-2** (verifier checks packet hash, inner status, membership in the artifact).
6. **N-4, N-5, N-7** as one design change: a single canonical serializer and a `VerifiedRegistry` object that owns the verified, immutable records and the index. This is a hash-format change and should be versioned as such.
7. Add an `expected_artifact_sha256` anchor parameter (O-5).
8. Hologram Renderer after the above; Zenodo evaluation after an audit of that version.

---

## 9. What this audit does not establish

- No claim about linguistic correctness of any registry content, and none about the NOVA Q / EIT framework. The `research/` document in the handoff package was not reviewed.
- The out-of-band publication of anchors was not observed by me; anchor values were compared only against the files in the package.
- CI was not run on GitHub for V2.7.6 (candidate unpublished).
- Mutation testing covered 17 hand-picked mutants, not the full mutation space.
- Confusable-character (homoglyph) handling was not tested.

```
FINAL VERDICT:          NEEDS_FIX
FORMAL_FREEZE:          NO
ZENODO_PUBLICATION:     NOT_AUTHORIZED
SCIENTIFIC_VALIDATION:  NOT_CLAIMED
SOURCE_MODIFIED_BY_REVIEWER:      NO
MANIFESTS_REGENERATED_BY_REVIEWER: NO
```
