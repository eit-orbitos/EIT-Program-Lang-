# EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.9

Project: NOVA Q / EIT — EIT Program Lang
Author / Founder / Architect: Toni Mladenovski
Project origin: 18 April 2026
Specification date: 08 October 2026
Drafted by: Claude drafted V0.3, V0.5, V0.5.1, V0.5.2, V0.5.3, V0.5.4, V0.5.5, V0.5.6, V0.5.7, V0.5.8 and this V0.5.9. V0.4 was consolidated in the author's workflow from V0.3, Amendment A and the review corrections.
Status: CONSOLIDATED_DRAFT / INDEPENDENT_REVIEW_REQUIRED / SPECIFICATION_ONLY

This file is self-contained. No rule in it is incorporated by reference to an earlier draft.

Supersedes, as the single normative review draft:

| Document | SHA-256 |
|---|---|
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.8 | `f33c69af08409f0df6b14b2717f9c07252b16568dbbe470f4b73399604dc8733` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.7 | `024b89cefd4b2c4721021d322565625126883e6037c4ba3f5698287797514e3e` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.6 | `2868d783442bafcd628e5d37b37ec64273541615c1ff72fdc2778bae1a575250` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.5 | `b35a0626d7e3b6ed1accb314e792f8af7ca7f3d0febd8cbebcd7615ca69a593f` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.4 | `3caebc00eee78c932a86123ab9277a18533becf817f46f2dbd8af195482fdbba` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.3 | `12b37d59140a20531bae5156cbda9a76746c1efddb477387f619f5f87d0a8673` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.2 | `f2350233dd59c5a1f2b54f4ccb8f42a014252d164ae9374efd3b1b09bd7016fa` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.1 | `38cc687b5f106fa5e2a1c8b7c85b924a194171eac85747d4a9154411778d0aef` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5 | `4d7879ee522412274b6286708fc0c96f080d15884b6d33061ea0881c33731d87` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.4 | `6eddc2a360665e96697dec4a6fd37652477d8eb61ce3c2acb84004d7a2cac2cf` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.3_AMENDMENT_A | `3430ec91739bc8618d5484c52c12e124c4bf9fa6d6e070600d98690efe80637e` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.3 | `d4a8e52d4950d80c0a1d4d2bd4ef6c2cbcf5be09ad861ecce83f7fd92457bcd0` |
| EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.2 | `00bab4b0e6b350231595c982e1c736f36fa2acdce3a0c43a77932c15fc6dddb5` |

None of those files is modified by this one.

---

## 0. Governance, scope, conventions

### 0.1 Governance

```
V2.7.5 @ 2b7dd62      = IMMUTABLE_BASELINE
V2.7.6                = DEVELOPMENT_CANDIDATE
V2.7.7                = PROPOSED / NOT_IMPLEMENTED
IMPLEMENTATION_APPROVAL = NO
GITHUB_UPDATE           = HOLD
FORMAL_FREEZE           = NO
ZENODO                  = BLOCKED
```

This document changes no file. It authorizes nothing. No V2.7.7 code exists and no V2.7.7 test result is claimed anywhere in it.

### 0.2 Scope

One function: `verify_restored_query_receipt` in `eit_program_lang/receipt_verifier.py`, plus the tests and fixtures that exercise it, plus the version stamps written by the receipt and packet builders (§10.3). Everything else is out of scope (§13).

### 0.3 Normative language

"MUST", "MUST NOT", "MAY" are requirements on a future implementation. Authority of the sections `[TASKLET V055-F07][NEW-V0.5.6]`:

- **Normative for verifier behaviour and test requirements:** sections 2 to 11.
- **Binding governance requirements:** the governance block of §0.1; the documentation requirement and the non-claims and open-risk disclosures of §12; the release-blocking list of §13; the release gates of §14A; and the author decisions recorded as resolved in §15. A "MUST" in those places binds the documentation, the release process or the reviewer, not the verifier.
- **Informative:** the review history, reconciliation matrices and change logs of §14, the historical question record in §15, and the appendices. A statement there does not establish execution or closure merely by being included.

This classification states what the earlier sentence ("Sections 2 to 11 are normative. Sections 12 to 15 and the appendices are informative.") left contradictory; it changes the meaning of no clause in sections 2 to 15.

### 0.4 Origin labels

Each requirement carries one or more labels:

| Label | Meaning |
|---|---|
| `[AUTHOR]` | Decision by the author (D-1…D-4 and the V0.3 go decision) |
| `[CLAUDE]` | From `CLAUDE_V277_P003_ARCHITECTURAL_REVIEW_V0.1` or `CLAUDE_V277_P003_SPEC_V0.2_REVIEW` (K-01…K-11) |
| `[DEEPSEEK]` | From `DEEPSEEK_V277_V02_CONTENT_ADVERSARIAL_REVIEW` or the DeepSeek V0.1 report (DS-N1…DS-N5) |
| `[EXECUTED]` | Established by running V2.7.6 (`EIT_V2_7_6.zip`, sha256 `3b99157e…408e22c`) or V2.7.5 (`2b7dd62`) on 2026-10-08 |
| `[NEW-V0.3]` | Introduced in V0.3; reviewed since by the author's workflow, not yet confirmed by an independent reviewer on these bytes |
| `[AMENDMENT_A …]` | From `EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.3_AMENDMENT_A` (A-01…A-07) |
| `[CLAUDE AA-n]` | From `CLAUDE_V277_P003_V0.3_AMENDMENT_A_REVIEW` (AA-1…AA-7) |
| `[CLAUDE F-n]`, `[CLAUDE m-n]` | From `CLAUDE_V277_P003_SPEC_V0.4_REVIEW` (F-1…F-3, m-1…m-12) |
| `[AUTHOR_APPROVED]` | Author decision on OQ-1…OQ-5 |
| `[NEW-V0.5]` | Introduced in V0.5; not yet confirmed to the drafter by any reviewer |
| `[AUTHOR-TASK V0.5.1]` | Topic named in the author's V0.5.1 task statement (items 4–8). Reported there as arising from the DeepSeek V0.4 and V0.5 reviews, whose text the drafter has not seen (§14) |
| `[NEW-V0.5.1]` | Wording and design introduced in V0.5.1; reviewed in `DEEPSEEK_V277_V051_ADVERSARIAL_REVIEW_V0.1` |
| `[DEEPSEEK V0.5.1 <id>]` | Correction from `DEEPSEEK_V277_V051_ADVERSARIAL_REVIEW_V0.1`, read in full by the drafter. `<id>` is DeepSeek's correction id |
| `[NEW-V0.5.2]` | Introduced in V0.5.2. Not yet confirmed by a review of the actual V0.5.2 bytes (§14) |
| `[DEEPSEEK V0.5.2 <id>]` | Point raised in `DEEPSEEK_V277_V052_FINAL_ADVERSARIAL_REVIEW_V0.1`, read in full by the drafter |
| `[NEW-V0.5.3]` | Introduced in V0.5.3; reviewed in `TASKLET_V277_V053_INDEPENDENT_REVIEW_V0.1` |
| `[TASKLET Fnn]` | Finding F01…F12 of `TASKLET_V277_V053_INDEPENDENT_REVIEW_V0.1` (byte-verified review of V0.5.3, verdict NEEDS_FIX), read in full by the drafter |
| `[AUTHOR F08]`, `[AUTHOR F09]` | Author decisions of 2026-10-08 on Tasklet F08 (candidate uniqueness) and F09 (record-key identity) |
| `[NEW-V0.5.4]` | Introduced in V0.5.4; content-reviewed in `DEEPSEEK_V277_V054_INDEPENDENT_ADVERSARIAL_REVIEW_V0.1`, not yet byte-verified by any reviewer |
| `[DEEPSEEK V0.5.4 <id>]` | Correction from `DEEPSEEK_V277_V054_INDEPENDENT_ADVERSARIAL_REVIEW_V0.1` (content review; byte verification reported as not verifiable), read in full by the drafter |
| `[NEW-V0.5.5]` | Introduced in V0.5.5; reviewed in `TASKLET_V277_V055_INDEPENDENT_REVIEW_V0.1` |
| `[TASKLET V055-Fnn]` | Finding V055-F01…V055-F08 of `TASKLET_V277_V055_INDEPENDENT_REVIEW_V0.1` (byte-verified review of V0.5.5, all 1233 lines read, verdict NEEDS_FIX), read in full by the drafter. Distinct from `[TASKLET Fnn]`, which refers to the review of V0.5.3 |
| `[AUTHOR V0.5.6]` | Author decision of 2026-10-08 for V0.5.6: Option A, the 64-bit integer domain |
| `[NEW-V0.5.6]` | Introduced in V0.5.6; reviewed in `TASKLET_V277_V056_INDEPENDENT_REVIEW_V0.1` |
| `[TASKLET V056-Fnn]` | Finding V056-F01…V056-F05 of `TASKLET_V277_V056_INDEPENDENT_REVIEW_V0.1` (byte-verified review of V0.5.6, all 1328 lines read, verdict NEEDS_FIX), read in full by the drafter |
| `[AUTHOR V0.5.7]` | Author instruction of 2026-10-08 for V0.5.7 (items F01…F05 of the build task) |
| `[CODE_VERIFIED]` | Established by reading the cited source lines; not by running them |
| `[NEW-V0.5.7]` | Introduced in V0.5.7; reviewed in `TASKLET_V277_V057_INDEPENDENT_REVIEW_V0.1` |
| `[TASKLET V057-Fnn]` | Finding V057-F01, V057-F02 of `TASKLET_V277_V057_INDEPENDENT_REVIEW_V0.1` (byte-verified review of V0.5.7, all 1400 lines read, verdict NEEDS_FIX), read in full by the drafter |
| `[AUTHOR V0.5.8]` | Author decisions of 2026-10-08 for V0.5.8: accept V057-F01 and V057-F02 |
| `[NEW-V0.5.8]` | Introduced in V0.5.8; reviewed in `TASKLET_V277_V058_INDEPENDENT_REVIEW_V0.1` |
| `[TASKLET V058-F01]` | Finding V058-F01 of `TASKLET_V277_V058_INDEPENDENT_REVIEW_V0.1` (byte-verified review of V0.5.8, all 1444 lines and the diff from V0.5.7 read, verdict NEEDS_FIX, one MINOR finding), read in full by the drafter |
| `[AUTHOR V0.5.9]` | Author decision of 2026-10-08 for V0.5.9: accept V058-F01 |
| `[NEW-V0.5.9]` | Introduced in this file; not yet seen by any reviewer other than the drafter |

Code references are to V2.7.6 unless marked `@2b7dd62`.

---

## 1. Author decisions

**D-1 `[AUTHOR]`** The invalid positive fixture is preserved as historical evidence and replaced in active tests by a genuine one. Mechanism in §11.1.

**D-2 `[AUTHOR]`** A receipt whose inner query or translation status is `INTEGRITY_CHECK_FAILED` yields `verified = False` with `INNER_STATUS_INTEGRITY_CHECK_FAILED`. No crash. No bypass mode.

**D-3 `[AUTHOR]`** Identity verification uses exact, type-sensitive equality of stored values (§3.3). It does not normalize. Query-input normalization is a separate runtime concern.

**D-4 `[AUTHOR]`** Strict-mode allow-lists contain the legitimate historical stamps and the V2.7.7 stamp (§10.3). Legacy inclusion never bypasses hashes or grounding.

**D-5 `[AUTHOR]`** `index_sha256` is DEFERRED. The risk stays open and is documented (§12).

---

## 2. Canonical hashing contracts

`[DEEPSEEK]` required these to be named. `[EXECUTED]` they exist in the code and are reproduced here exactly. The implementation MUST call the existing functions and MUST NOT reimplement them.

### 2.1 `sha256_json(data)`: receipts and packets

Source: `restored_query_receipt.py:14-22`, imported by the verifier at `receipt_verifier.py:19`. Three identical copies exist in other modules.

```python
payload = json.dumps(data, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":"), default=str)
return hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

- Receipt hash input: the receipt mapping without the key `receipt_sha256`.
- Packet hash input: the packet mapping without the key `packet_sha256`.

### 2.2 `artifact_sha256(frozen_artifact)`: artifacts

Source: `integrity_verifier.py:29-32`.

```python
hashlib.sha256(json.dumps(frozen_artifact, sort_keys=True,
                          ensure_ascii=False).encode("utf-8")).hexdigest()
```

Note the difference: default separators (`", "` and `": "`) and no `default`. The two functions are not interchangeable.

### 2.3 Rules

- **H-1 `[CLAUDE]`** Every call to either function inside the verifier MUST be guarded. `TypeError`, `ValueError`, `UnicodeEncodeError` and `RecursionError` MUST become the failure `CANONICALIZATION_FAILED` for the layer that was hashing. No exception may escape.
- **H-5 Consequences of a hashing failure `[TASKLET F10][NEW-V0.5.4]`** `[EXECUTED]` A `str` holding a lone surrogate passes the type scan, can arrive through `json.loads`, and makes both hash functions raise `UnicodeEncodeError`; on V2.7.6 that exception escapes the verifier.
  - Receipt hashing fails in check 1a.2: emit `CANONICALIZATION_FAILED` with detail `receipt`. L1 is `FAIL`. Everything else continues.
  - Packet hashing fails in check 1b.2: emit `CANONICALIZATION_FAILED` with detail `translation_packet`. Check 1b.2 runs only if 1b.1 passed (§7). A defect inside the packet yields two `CANONICALIZATION_FAILED` entries, details `receipt` then `translation_packet`, only when 1b.1 passed and both hash operations raised. If 1b.1 failed, 1b.2 does not run: the entries are then one `CANONICALIZATION_FAILED` (detail `receipt`) followed by `PACKET_HASH_MISSING_OR_MALFORMED`. If the defect lies only in the value of `packet_sha256`, 1b.1 fails for the same reason. Phase order and P-2 are unchanged. `[TASKLET V055-F04][NEW-V0.5.6]`
  - Artifact hashing fails when computing `AH`: emit `CANONICALIZATION_FAILED` with detail `artifact` in L3_BINDING. B.2 to B.5 and A.2 do not run. `L3_BINDING` is `FAIL`, `L3_ANCHOR` follows §5.3, L2b does not run.
  - `CANONICALIZATION_FAILED` entries are ordinary entries: P-2 and the cap of P-3 apply to them like any other. `[DEEPSEEK V0.5.4 H5-C2]`
  - When `source_frozen_artifact` is `None`, no attempt is made to hash an artifact and the third case cannot occur; B.1 emits `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK`. The first two cases are unaffected. `[DEEPSEEK V0.5.4 H5-C3]`
- **H-6 Integer domain and runtime settings `[TASKLET V055-F01, V055-F02][AUTHOR V0.5.6][NEW-V0.5.6]`** L0 admits an `int` only in the range of §6.1. `[EXECUTED]` On CPython 3.12 and 3.13 with the default limit of 4300 digits, `json.dumps` and `str()` raise `ValueError` for `10**4300`, and with the limit disabled they succeed; so without a bound the failure list depended on a process setting. `[EXECUTED]` The two bounds `-2**63` and `2**63 - 1` convert identically with the limit set to 0, 640 and 4300 (640 is the smallest limit CPython accepts; the bounds have 19 digits). Inside the admitted domain the integer-conversion limit therefore cannot change any hash or any derivation of §3. The verifier MUST NOT read or change that process setting.
- **H-2 `[EXECUTED]`** Legacy compatibility: a packet built by V2.7.5 code is reproduced exactly by `sha256_json` of V2.7.6. No legacy exemption from the packet hash is needed or allowed.
- **H-3 `[CLAUDE]`** Known limits of these functions, inherited and not fixed here: `default=str` lets distinct values serialize alike; integer and string mapping keys collide; `NaN` is accepted. See §12.
- **H-4 `[CLAUDE]`** A hash value is "well-formed" when it is a `str` of 64 characters from `0-9a-f`.

---

## 3. Definitions

### 3.1 Stamp

`stamp` is the value of `receipt["receipt_version"]`. It selects version-specific rules. It is self-declared (§12, R-5).

**Stamp resolution `[AUTHOR-TASK V0.5.1][NEW-V0.5.1]`**

| `receipt_version` | Effect |
|---|---|
| exactly the `str` `"2.7.4"` | legacy rules where this document says `stamp == "2.7.4"` |
| any other `str` | current rules (the stricter set). In strict mode the value is also checked against the allow-list (§10.2) |
| key absent, or value not exactly `str` | failure `REQUIRED_FIELD_MISSING` (§9.1, V.1), and current rules are used for the rest of the evaluation. Never an exception, never legacy rules |

`[EXECUTED]` Both builders always write `receipt_version`. On V2.7.6 and V2.7.5 a receipt with the key deleted, with the value `2.76`, or with `"9.9.9"`, verifies today.

`[EXECUTED]` Stamps written by existing code:

| Producer | `receipt_version` | `module_id` | `packet_version` |
|---|---|---|---|
| V2.7.5 code (and V2.7.4 line) | `2.7.4` | `EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4` | `2.7.4` |
| V2.7.6 code | `2.7.6` | `EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_6` | `2.7.6` |

No code writes `2.7.5`.

### 3.2 Normalization functions used for derived fields only

```
nfc(x)             = unicodedata.normalize("NFC", str(x))
role_norm(x, stamp)   = str(x).upper()   if stamp == "2.7.4"   else nfc(x).upper()
family_norm(x, stamp) = str(x).upper()   if stamp == "2.7.4"   else nfc(x).upper()
```

`[EXECUTED]` V2.7.6 derives with `nfc(...).upper()` (`frozen_translation_lookup.py:38,99,100,106`). `[CLAUDE]` V2.7.5 derives with `str(...).upper()` (`frozen_translation_lookup.py:34,81,82,88 @2b7dd62`).

### 3.3 Typed equality `teq(a, b)` `[CLAUDE][AUTHOR]`

Python `==` treats `True`, `1` and `1.0` as equal. Identity comparison MUST use:

```
teq(a, b) is True iff
  type(a) is type(b), and
  - mappings: same key set, and teq on every value
  - lists:    same length, and teq element by element, in order
  - floats:   a == b, or both are the same non-finite value
  - otherwise: a == b
```

No normalization, no case folding, no coercion. `teq` operates only after L0 exact-type validation: permitted types are exactly `NoneType`, `bool`, `int`, `float`, `str`, `list`, `dict` (not subclasses), with string keys for dicts. It never calls custom object comparison methods. `[AMENDMENT_A][CLAUDE_AA-1][DEEPSEEK]` `[EXECUTED]` With this rule a stored NFD value and its NFC equivalent are different, and `1`, `True`, `1.0` are different.

### 3.4 Record map and candidates

```
RECORDS = source_frozen_artifact["frozen_registry_snapshot"]["registry_records"]
```

```
candidates(role, family, stamp) =
  [ r for r in RECORDS.values()
    if role != ""
    and role_norm(r.get("symbolic_role", ""), stamp) == role
    and family_norm(r.get("script_family", ""), stamp) == family ]
```

This mirrors the runtime's target selection (`frozen_translation_lookup.py:34-42,99-107`).

**Normalized surface `[TASKLET V056-F01][AUTHOR V0.5.7][NEW-V0.5.7]`.**

```
normalized_surface(r) = nfc(r.get("visible_symbol"))
```

The value used for an absent `visible_symbol` key is `None`, exactly as in G-3 (§9.2), so an absent key and a stored `None` both give the surface `"None"`, and a stored empty string gives `""`. Every phrase "distinct `nfc(visible_symbol)`" in R-1 and R-3 means the set `{ normalized_surface(r) for r in C }`. The derivation needs no `visible_symbol` key, is never skipped, and cannot raise (`nfc` applies `str()` to a value admitted by L0, H-6). It is the existing normalization made explicit, not a new one: `[CODE_VERIFIED]` V2.7.6 computes `{nfc(c.get("visible_symbol")) for c in candidates}` (`unicode_normalization.py:65`). It is used only where the rules already used it, that is for stamps other than `2.7.4`; the legacy rules of R-1 do not look at surfaces and are unchanged. `[CODE_VERIFIED]` The V2.7.6 integrity gate refuses a state with a record lacking `visible_symbol` (`integrity_verifier.py:35,91-93`), so the absent-key case arises only for hand-made artifacts; the verifier still defines it. L0 does not require the key (row 0.10 is unchanged).

### 3.5 Positive claim `[DEEPSEEK]`

A receipt "positively claims a match" when any of these holds: `query_result.found is True`; `query_result.match_count > 0`; `query_result.records` or `query_result.symbol_ids` is non-empty; `translation_result.status == "TRANSLATED_FROM_FROZEN_REGISTRY"`. `AMBIGUOUS_NO_SILENT_PICK`, `NO_MATCH`, `NO_SOURCE_MATCH_IN_FROZEN_REGISTRY` and `NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY` are not positive translation claims.

---

## 4. API and result

### 4.1 Signature `[DEEPSEEK][CLAUDE]`

```python
verify_restored_query_receipt(
    receipt,
    source_frozen_artifact=None,
    expected_artifact_sha256=None,
    expected_restored_state_sha256=None,
    strict_mode=False,
)
```

The existing positional two-argument call keeps working.

### 4.2 Result

Existing keys MUST be preserved: `check_type`, `verified`, `failures`, `receipt_sha256`, `safety`.

New keys:

| Key | Content |
|---|---|
| `failure_details` | List parallel to `failures`. Each entry is exactly the string that §4.6 assigns to the check that produced the failure. At most 120 characters. It MUST NOT contain any value taken from the receipt or the artifact. `[CLAUDE][TASKLET F01]` |
| `layers` | Mapping with keys `L0`, `L1`, `L2`, `L3_BINDING`, `L3_ANCHOR`, `L3_STATE`, `L4`; each value is `PASS`, `FAIL` or `NOT_EVALUATED`. `[CLAUDE]` |
| `assurance` | One of `NONE`, `CONSISTENCY_ONLY`, `ARTIFACT_ANCHORED`, `ARTIFACT_AND_STATE_ANCHORED` (§4.4). `[DEEPSEEK][NEW-V0.3]` |

### 4.3 `verified`

`verified` is `True` iff `failures` is empty.

### 4.4 `assurance` `[DEEPSEEK]`

DeepSeek asked for a machine-checkable signal so that a caller cannot read `verified = True` as "authentic".

| Condition | `assurance` |
|---|---|
| `verified` is `False` | `NONE` |
| `verified` and `L3_ANCHOR != PASS` | `CONSISTENCY_ONLY` |
| `verified`, `L3_ANCHOR == PASS`, `L3_STATE != PASS` | `ARTIFACT_ANCHORED` |
| `verified`, `L3_ANCHOR == PASS`, `L3_STATE == PASS` | `ARTIFACT_AND_STATE_ANCHORED` |

### 4.5 Caller obligation `[DEEPSEEK][CLAUDE]`

`expected_artifact_sha256` and `expected_restored_state_sha256` MUST come from a source the receipt producer cannot write to. A hash computed by the caller from the artifact it is about to verify is not an anchor.

The following text MUST appear verbatim in the function's docstring `[AMENDMENT_A A-05]`:

> The verifier cannot enforce that expected hashes were obtained from a trustworthy independent channel. If the caller computes an expected hash from the untrusted artifact being verified, an `ARTIFACT_ANCHORED` assurance label does not establish independent provenance or producer authenticity.

`assurance` describes the checks performed. It does not certify where an anchor came from.

### 4.6 Failure detail strings `[TASKLET F01][NEW-V0.5.4]`

Tasklet showed that with unspecified details, two conforming implementations could merge or keep two failures of the same code and so return different lists. This table closes that. One check instance produces at most one failure, with exactly this detail. `i` is a decimal list index. Angle brackets name a key from this specification's own tables, never a key taken from the input.

| Check | Detail |
|---|---|
| 0.1a, 0.1b, 0.1c | the argument name (S-5) |
| 0.2 | `receipt` |
| 0.3, 0.9 | the scan form of §6.3 |
| 0.4 | `query_result`, else `translation_result` (first failing, in this order) |
| 0.5 | `boundary` |
| 0.6 | first failing of: `query_result.symbol_ids`, `query_result.records`, `query_result.records[i]` (lowest `i`) |
| 0.7 | first failing of: `translation_result.translation_packet`, `translation_result.source`, `translation_result.target`, `translation_result.ambiguous_candidates`, `translation_result.ambiguous_candidates[i]` (lowest `i`) |
| 0.8 | `artifact` |
| 0.10 | first failing of: `artifact.frozen_registry_snapshot`, `artifact.registry_records`, `artifact.registry_records:ordinal=<n>` where `<n>` is the zero-based ordinal of the record's key in ascending order of the exact `str` keys (lowest `<n>`), written as in §6.3 `[TASKLET V055-F06]` |
| 1a.1, 1a.2 | `receipt.receipt_sha256` |
| 1b.1, 1b.2 | `translation_packet.packet_sha256` |
| `CANONICALIZATION_FAILED` | `receipt`, `translation_packet` or `artifact` (H-5) |
| B.1 | `source_frozen_artifact` |
| B.2 | `receipt.frozen_artifact_sha256` |
| B.3 | `translation_packet.frozen_artifact_sha256` |
| B.4 | `query_result.frozen_artifact_sha256` |
| B.5 | `translation_result.frozen_artifact_sha256` |
| A.1, A.2 | `expected_artifact_sha256` |
| T.1 | `restored_state_sha256` |
| T.2 | `expected_restored_state_sha256` |
| V.1 | `receipt.receipt_version` |
| Q.1, Q.2, Q.3, Q.8 | `query_result.status` |
| Q.4 | `query_result.<key>` |
| Q.4a | `query_result.records[i].symbol_id` |
| Q.5 | `query_result.symbol_ids` |
| Q.6 | `query_result.match_count` |
| Q.7 | `query_result.found` |
| X.1, X.2 | `translation_result.status` |
| X.3 | `translation_result.translation_packet` (also when the key is absent) |
| X.4 | `translation_result.<key>` or `translation_packet.<key>` |
| X.4a, source side / target side | `translation_result.source.symbol_id` / `translation_result.target.symbol_id` |
| X.5, source side / target side | `translation_result.source.symbol_id` / `translation_result.target.symbol_id`. Always the record side, never a packet path `[DEEPSEEK V0.5.4 FD-C1]` |
| X.6 | `translation_result.ambiguous_candidates` (fewer than two entries), else, per element in ascending `i` and in this field order, `translation_result.ambiguous_candidates[i].symbol_id` then `translation_result.ambiguous_candidates[i].visible_symbol`. `i` is the zero-based list index, written as in §6.3 `[TASKLET V055-F05]` |
| G-1 | the position path as written in §9.2, with `[i]` for list positions |
| G-2 | `query_result.records[i]`, `translation_result.source` or `translation_result.target` |
| G-3 | `translation_packet.<field>` (the left side of the line) |
| G-4 | `translation_result.symbolic_role` or `translation_result.ambiguous_candidates[i].visible_symbol` |
| G-5 | `receipt.frozen_artifact_id` |
| R-1, R-2, R-3 | `translation_result` |
| L4.1 | `receipt.receipt_type` |
| L4.2 | `boundary.<key>` (one of the four constants) |
| L4.3 | `receipt.receipt_version` or `receipt.module_id` |
| L4.4 | `translation_packet.packet_version` |
| L4.5 | `receipt.generated_at_utc` |
| `FAILURES_TRUNCATED` | `failures` |

X.5 compares a record id with a packet id; its failure is one entry per side, and the detail is fixed to the record side so that it is a single string, not a choice. A packet id key that is missing is X.4's failure with detail `translation_packet.<key>`; a packet id that is not a `str` or not in the artifact is G-1's failure with detail `translation_packet.source_symbol_id` or `translation_packet.target_symbol_id`. X.4a and X.5 share a detail on each side but have different codes. `[DEEPSEEK V0.5.4 FD-C1]`

Every `[i]` in this table is a zero-based list index and every `ordinal=<n>` a zero-based ordinal, both written in decimal digits with no sign and no leading zero (`0` for zero). No detail string in this table contains an ellipsis or any other abbreviation; `<key>` and `<field>` stand for one exact key name from the tables of §8 and §9. `[TASKLET V055-F05, V055-F06][NEW-V0.5.6]`

Because each check instance has its own detail or its own code, P-2 never merges failures from two different checks.

---

## 5. Verification order and failure precedence

### 5.1 Order `[CLAUDE]`

```
Phase 0  L0  shape                         fail-fast: exactly one failure, then return
Phase 1  L1a receipt hash
         L1b packet hash                   when a packet mapping is present
Phase 2  L3_BINDING                        supplied artifact vs hash copies in the receipt
         L3_ANCHOR                         supplied artifact vs external anchor
         L3_STATE                          state-hash copies; optional external anchor
Phase 3  L2a internal consistency          needs no artifact
         L2b grounding and target resolution   only if L3_BINDING is PASS
Phase 4  L4  policy
```

Phases 1 to 4 always all run after Phase 0 passes, and collect failures. Failure emission follows phase order, not dependency order: L3_BINDING failures precede L2a failures; within Phase 3, L2a failures precede L2b failures. Skipped checks emit no success signal. `[AMENDMENT_A A-02][DEEPSEEK]`

### 5.2 Determinism `[DEEPSEEK][CLAUDE]`

- **P-1** `failures` is ordered by the phase order above, then by the order in which checks are listed in §6 to §10, then by any per-instance order that the check itself assigns, and where the check assigns none, by field order as listed, then by list index. X.6 assigns its own order (§4.6): the count failure alone if the list has fewer than two entries; otherwise ascending candidate index, and within one candidate `symbol_id` before `visible_symbol`. That order takes precedence over the default for X.6 only. `[TASKLET V056-F02][AUTHOR V0.5.7][NEW-V0.5.7]`
- **P-2** Identical `(code, detail)` pairs appear once.
- **P-3** At most 32 entries are collected. If more would be added, collection stops and `FAILURES_TRUNCATED` is appended as entry 33. The count is of entries that remain after P-2: an emission that P-2 discards does not count and cannot cause truncation. `[TASKLET F12]` Only the collection of entries stops. Every phase and every applicable check still runs after the cap is reached (§5.1), and each layer value in `layers`, `verified` and `assurance` are computed from the outcomes of all checks, including those whose entry was not collected. `[TASKLET V056-F04][NEW-V0.5.7]`
- **P-4** Two implementations given the same input MUST return the same `failures` list in the same order. Scope `[TASKLET V056-F03][NEW-V0.5.7]`: this holds within one conformance profile (§10.2). The integer-conversion limit of the process is not part of the profile, because H-6 makes results independent of it. Equality across different profiles is not claimed.
- **P-5** The emission order differs from V2.7.6, where `WRONG_RECEIPT_TYPE` and `BOUNDARY_VIOLATION:*` come before provenance codes (`receipt_verifier.py:29-59`). `[EXECUTED]` Existing tests assert membership, not position, except `failures == []`.
- **P-6 `[AMENDMENT_A A-04][CLAUDE m-9]`** Every equality check between two input values, or between an input value and a caller-supplied expected value, MUST use `teq` (§3.3), unless the rule names a derivation function (§3.2). Comparisons written with `==` in §7, §8.1 and §10 are against a string computed by the verifier or a literal; after L0 they behave identically under `teq` and MAY be implemented with it.
- **P-7 Explicit order inside Phase 3 `[DEEPSEEK V0.5.2 D-C1, reworded][NEW-V0.5.3]`** This spells out P-1; it changes nothing.
  - L2a, in this order: V.1; for `query_result`: Q.1, Q.2, Q.3, Q.4, Q.4a, Q.5, Q.6, Q.7, Q.8; for `translation_result`: X.1, X.2, X.3, X.4, X.4a, X.5, X.6.
  - L2b, after all of L2a, in this order: G-1 over the positions in the order listed in §9.2; G-2 for `query_result.records` in list order, then `translation_result.source`, then `.target`; G-3 lines in the order written; G-4 role line, then candidates in list order; G-5; R-1; R-2; R-3.
  - Every check named Q.n or X.n belongs to L2a, including X.4. No L2b rule reports a missing key.

### 5.3 Layer values

| Layer | `PASS` | `FAIL` | `NOT_EVALUATED` |
|---|---|---|---|
| L0 | shape valid | shape invalid | never |
| L1 | all applicable hashes match | any L1 failure | never after L0 passes |
| L3_BINDING | all applicable copies match | any binding failure, including artifact `None` | never after L0 passes |
| L3_ANCHOR | anchor supplied, artifact supplied, `AH` computed, and equal | anchor supplied and different (A.2); or strict mode without anchor (A.1), whether or not an artifact is supplied | no anchor in default mode; or anchor supplied but no comparison possible because the artifact is `None` or `AH` could not be computed (H-5) `[TASKLET F03]` |
| L3_STATE | expected state hash supplied and equal to every applicable copy | applicable copies disagree (T.1); or expected supplied and T.2 fails | no expected hash, and T.1 did not fail. L3_STATE does not depend on the artifact |
| L2 | L2a and L2b ran with no failure | any L2 failure | L2b skipped and L2a had no failure |
| L4 | no L4 failure | any L4 failure | never after L0 passes |

---

## 6. L0 shape and exact-type guard (fail-fast)

`[AMENDMENT_A A-03][CLAUDE AA-1…AA-4][CLAUDE F-1, F-2]`

### 6.1 Principles

- L0 returns the first failure alone, with `layers.L0 = FAIL`. Nothing else is evaluated.
- Supported values are exactly the built-in types `NoneType`, `bool`, `int`, `float`, `str`, `list`, `dict`. Subclasses, `tuple`, `set`, `bytes` and custom instances are unsupported. A `dict` key MUST be exactly `str`.
- **Integer domain `[TASKLET V055-F01, V055-F02][AUTHOR V0.5.6][NEW-V0.5.6]`.** Every value whose type is exactly `int`, anywhere in the receipt or in the artifact, MUST satisfy `-2**63 <= x <= 2**63 - 1`. `bool` is a different exact type and is not range-checked. The test MUST be made by integer comparison (or `int.bit_length`), never by `str()`, `repr()`, formatting or serialization. A value outside the range is a shape failure of its root: `RECEIPT_SHAPE_INVALID` in the receipt, `ARTIFACT_SHAPE_INVALID` in the artifact. `float` is not restricted: `[EXECUTED]` `str()` and `json.dumps` do not raise for any `float`, `nan` and the infinities included (H-3).
- Type tests MUST use `type(x) is T`. Before the scan of an object has passed, the verifier MUST NOT call `isinstance`, `str()`, `repr()`, `==`, `hash()`, `sorted(..., key=str)`, attribute access, or any key lookup on it.
- **Scan before lookup `[NEW-V0.5][EXECUTED]`.** A key lookup such as `d.get("frozen_registry_snapshot")` on a `dict` that holds a hostile key object with a colliding hash invokes that object's `__eq__`. Therefore each object is scanned (rows 0.3, 0.9) before any of its keys is looked up (rows 0.4–0.7, 0.10).
- L0 does not check the presence of keys inside a well-typed mapping. Missing keys are collected later (§8, §9.1), which keeps the existing failure codes reachable. `[CLAUDE K-01]`
- L0 MUST NOT hash, copy for hashing, or mutate its inputs.

### 6.2 Checks, in this order

| Order | Check | Single failure code |
|---|---|---|
| 0.1a | `type(strict_mode) is bool` | `STRICT_MODE_NOT_BOOL` |
| 0.1b | `expected_artifact_sha256` is `None`, or is exactly `str` and well-formed (H-4) | `EXPECTED_ANCHOR_MALFORMED` |
| 0.1c | `expected_restored_state_sha256` is `None`, or is exactly `str` and well-formed (H-4) | `EXPECTED_ANCHOR_MALFORMED` |
| 0.2 | `type(receipt) is dict` | `RECEIPT_SHAPE_INVALID` |
| 0.3 | Scan of `receipt` (§6.3) | `REJECT_UNTRUSTED_OBJECT_TYPE` for an unsupported type or key; `RECEIPT_SHAPE_INVALID` for depth over 32 or an `int` outside the domain of §6.1 |
| 0.4 | `query_result` and `translation_result` are each absent, `None`, or exactly `dict` | `RECEIPT_SHAPE_INVALID` |
| 0.5 | `boundary` is absent or exactly `dict` | `RECEIPT_SHAPE_INVALID` |
| 0.6 | If present: `query_result.symbol_ids` is exactly `list`; `query_result.records` is exactly `list` and every element is exactly `dict` | `RECEIPT_SHAPE_INVALID` |
| 0.7 | If present: `translation_result.translation_packet` is `None` or exactly `dict`; `translation_result.source` and `.target` are exactly `dict`; `translation_result.ambiguous_candidates` is exactly `list` and every element is exactly `dict` | `RECEIPT_SHAPE_INVALID` |
| 0.8 | If `source_frozen_artifact` is not `None`: `type(source_frozen_artifact) is dict` | `ARTIFACT_SHAPE_INVALID` |
| 0.9 | If the artifact is not `None`: scan of the artifact (§6.3) | `REJECT_UNTRUSTED_OBJECT_TYPE` for an unsupported type or key; `ARTIFACT_SHAPE_INVALID` for depth over 32 or an `int` outside the domain of §6.1 |
| 0.10 | If the artifact is not `None`: `frozen_registry_snapshot` is present and exactly `dict`; its `registry_records` is present and exactly `dict`; **every value of `registry_records` is exactly `dict`**; and **record-key identity** `[TASKLET F09][AUTHOR F09]`: every record has the key `symbol_id`, its value is exactly `str`, and it is `teq` to the record's key in `registry_records` | `ARTIFACT_SHAPE_INVALID` |

Mapping to earlier drafts: rows 0.3, 0.8–0.10 here correspond to 0.2a/0.3, 0.8, 0.8a in V0.4.

### 6.3 Scan

```
scan(node, depth):                       # the root object is depth 1
    if depth > 32:                 -> depth failure
    if type(node) is int:                # exactly int; bool never reaches this line's test
        if node < -2**63 or node > 2**63 - 1:    -> range failure
        return
    if type(node) is one of NoneType, bool, float, str:        return
    if type(node) is list:
        for i in ascending index order:  scan(node[i], depth + 1)
        return
    if type(node) is dict:
        for key in the dict's own iteration order:
            if type(key) is not str:     -> type failure
        for key in ascending order of the (now plain str) keys:
            scan(node[key], depth + 1)
        return
    -> type failure
```

- The first failure met in this order is the one reported.
- A cycle needs no separate detection: it exceeds the depth limit and is reported as a depth failure. `[EXECUTED]` `json.dumps` raises on a cyclic value, so a cycle must not reach hashing; the depth limit guarantees that.
- A range failure is reported with the shape code of its root (rows 0.3 and 0.9), a depth failure likewise; a type failure with `REJECT_UNTRUSTED_OBJECT_TYPE`. The order of the scan alone decides which failure is first; no kind of failure has priority over another. `[NEW-V0.5.6]`
- `failure_details` for a scan failure has the fixed form `<root>:depth=<n>:path=<e1>.<e2>.<e3>` with as many elements as the path has, joined by single full stops, where `<root>` is `receipt` or `artifact`. No key text, no value text, no type name. `[CLAUDE AA-4]` Exact formatting `[TASKLET V055-F06][NEW-V0.5.6]`:
  - Every number (`<n>` and each path element) is written in decimal digits with no sign and no leading zero; zero is `0`.
  - A path element for a list is the zero-based index. A path element for a `dict` value is the zero-based ordinal of its key in ascending order of the exact `str` keys.
  - **Failing value** (unsupported type, depth, integer range): `<n>` is the depth of that value, and the path leads from the root to it. The path then has exactly `<n> - 1` elements.
  - **Rejected non-`str` key:** the failing node is the `dict` that contains the key. `<n>` is the depth of that `dict`; the path is the path to that `dict` followed by one further element, the zero-based ordinal of the rejected key in that `dict`'s own iteration order. The path then has exactly `<n>` elements, which distinguishes it from every failing-value detail.
  - The path is never empty: the root is a `dict` (rows 0.2 and 0.8), so a failing value is at depth 2 or more and a rejected key adds an element.
  - If the string is longer than 120 characters, its first 120 characters are kept.
  - Examples: a non-`str` key that is the second key iterated in the receipt root gives `receipt:depth=1:path=1`; an out-of-range `int` in the first element of the list stored under the receipt's third key in sorted order gives `receipt:depth=3:path=2.0`.

### 6.4 Rules

- **S-1** For `query_result` and `translation_result`, absent and `None` mean `{}`. `[EXECUTED]` The builder writes `{}` for both when called without them (`restored_query_receipt.py:45-46`).
- **S-2** `source_frozen_artifact is None` is not an L0 failure. It yields the existing `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK` in L3_BINDING (§8.1). `[CLAUDE K-01]`
- **S-3** An artifact with one malformed record fails row 0.10 even if the receipt does not reference that record. This is intended. `[CLAUDE F-2]`
- **S-7 Record-key identity `[TASKLET F09][AUTHOR F09][EXECUTED]`** Row 0.10 makes the stored `symbol_id` of every record equal to its map key, so §3.4, R-1 and R-3 may use either. `[EXECUTED]` V2.7.6 already refuses such artifacts at its integrity gate (`integrity_verifier.py:89-95`): with a stored id that is a list, absent, or different from the key, queries return `INTEGRITY_CHECK_FAILED`. Every artifact that the 33 existing tests and the demo pass to the verifier satisfies the rule.
  **Intentional rejection.** V2.7.5 has no gate. `[EXECUTED]` V2.7.5 answers queries over an artifact whose record has a stored id different from its key, and the resulting `2.7.4` receipt verifies under the V2.7.6 verifier. Under V2.7.7 it is rejected with `ARTIFACT_SHAPE_INVALID`. This is the only legacy receipt class, among those identified by the executed checks, that V0.5.4 newly rejects; the specification does not establish that no other class exists. `[DEEPSEEK V0.5.4 F09-C1]`
- **S-4** After L0 passes, no later phase may raise. Exact types alone do not give this: it rests on the exact-type scan together with the integer domain of §6.1 and the guarded hashing of H-1. `[TASKLET V055-F01]` An unexpected exception in a later phase is an implementation defect, never a successful verification.
- **S-5 `[AUTHOR-TASK V0.5.1][NEW-V0.5.1]`** Argument checks come first and in the order 0.1a, 0.1b, 0.1c. A malformed `strict_mode` is reported even when an anchor argument or the receipt is also malformed. `failure_details` is exactly the argument name and nothing else: `strict_mode`, `expected_artifact_sha256` or `expected_restored_state_sha256`. `[DEEPSEEK V0.5.1 S-C1]` A non-`bool` `strict_mode` is never interpreted by truthiness: `[EXECUTED]` in Python the string `"False"` is truthy, so coercion would silently enable or disable strict mode.
- **S-6 `[AUTHOR-TASK V0.5.1]`** `boundary` is not covered by S-1. `boundary: None` fails row 0.5 with `RECEIPT_SHAPE_INVALID`. An absent `boundary` key passes L0 and yields the four existing `BOUNDARY_VIOLATION:<key>` codes in L4 (§10.1). `[EXECUTED]` On V2.7.6 and V2.7.5, `boundary: None` raises `AttributeError`; an absent key and `{}` both return the four codes. V0.5.1 turns the exception into a controlled rejection and leaves the other two behaviours unchanged.

### 6.5 Compatibility and effect

`[EXECUTED]` Every receipt and artifact that the 33 existing V2.7.6 tests and `demo_v2_7_5.py` pass to the verifier, and in-memory receipts built by V2.7.6 and V2.7.5 code, contain only supported types with `str` keys; maximum depth 6 with the root counted as 1. External callers that pass tuples, subclasses or `OrderedDict` lose compatibility; this is intended.

Two further behaviour changes relative to V2.7.5 and V2.7.6, both for hand-made receipts that no builder in this codebase produces `[DEEPSEEK V0.5.1 V-C2, BN-C1][EXECUTED]`:

- A receipt whose `receipt_version` is absent or not a `str` verifies on V2.7.5 and V2.7.6 and does not verify on V2.7.7 (`REQUIRED_FIELD_MISSING`). This is an intentional compatibility break.
- `boundary: None` raises `AttributeError` on V2.7.5 and V2.7.6 and becomes a controlled `RECEIPT_SHAPE_INVALID` on V2.7.7. An absent `boundary` key and `{}` behave identically across versions.
- A value that cannot be hashed (a lone surrogate) makes the V2.7.5 and V2.7.6 verifiers raise `UnicodeEncodeError`; V2.7.7 returns `CANONICALIZATION_FAILED` (§2.3 H-5). `[DEEPSEEK V0.5.4 V-C2][EXECUTED on V2.7.6]`
- A `2.7.4` receipt over an artifact that violates record-key identity verifies on V2.7.6 and is rejected on V2.7.7 with `ARTIFACT_SHAPE_INVALID` (§6.4 S-7). Unlike the three items above, V2.7.5 code can produce such a receipt.
- A receipt or artifact holding an `int` outside `-2**63 … 2**63 - 1` is rejected at L0 on V2.7.7 (§6.1). On V2.7.5 and V2.7.6 its treatment depends on the value and on the process integer-conversion limit; that behaviour was not run against either verifier and REQUIRES_EXECUTION. `[EXECUTED]` The largest integer in the JSON files of the two trees available to the drafter (one file at `2b7dd62`, three in `EIT_V2_7_6.zip`) is 27. The integers the builders write (`match_count` and counts of the same kind) are bounded by the registry size `[LOGICALLY_INFERRED]`. No builder in this codebase is known to produce an out-of-range integer. `[TASKLET V055-F01][AUTHOR V0.5.6]`

Inside the verifier the guard makes `default=str` and non-string-key collisions unreachable. They remain reachable in the runtime and builder paths. R-4 stays OPEN. `[CLAUDE AA-6]`

---

## 7. L1 integrity

| # | Check | Code | Status |
|---|---|---|---|
| 1a.1 | `receipt_sha256` is a 64-character `str` | `RECEIPT_HASH_MALFORMED` | existing, trigger unchanged |
| 1a.2 | `sha256_json(receipt without receipt_sha256) == receipt_sha256` | `RECEIPT_HASH_MISMATCH_TAMPER_DETECTED` | existing |
| 1b.1 | If `translation_packet` is a mapping: `packet_sha256` is well-formed (H-4) | `PACKET_HASH_MISSING_OR_MALFORMED` | new `[CLAUDE]` |
| 1b.2 | If 1b.1 passed: `sha256_json(packet without packet_sha256) == packet_sha256` | `PACKET_HASH_MISMATCH_TAMPER_DETECTED` | new `[CLAUDE]` |

`[EXECUTED]` V2.7.6 writes `packet_sha256` (`frozen_translation_lookup.py:158`) and never reads it; receipts with a stale or deleted packet hash verify today.

---

## 8. L3 provenance

### 8.1 L3_BINDING: receipt versus supplied artifact

Let `AH = artifact_sha256(source_frozen_artifact)`.

| # | Check | Code |
|---|---|---|
| B.1 | `source_frozen_artifact is None` | `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK` (existing). Skip B.2 to B.5 and L3_ANCHOR's comparison; L2b is not evaluated |
| B.2 | `receipt.frozen_artifact_sha256 == AH` | `PROVENANCE_MISMATCH_WITH_SOURCE_ARTIFACT` (existing; fires for absent and `None` too) |
| B.3 | If packet is a mapping: `packet.frozen_artifact_sha256 == AH` | `TRANSLATION_PACKET_PROVENANCE_MISMATCH` (existing) |
| B.4 | For `query_result`, when it is non-empty and its status is not `INTEGRITY_CHECK_FAILED`: key `frozen_artifact_sha256` present | `ARTIFACT_HASH_COPY_MISSING` |
| | …and equal to `AH` | `ARTIFACT_HASH_COPY_MISMATCH` |
| B.5 | Same two checks for `translation_result` | same two codes |

`[EXECUTED]` Applicable copies, from running both versions:

| Sub-object and status | carries `frozen_artifact_sha256` | carries `restored_state_sha256` |
|---|---|---|
| `query_result`, `OK` / `NO_MATCH` / status absent (stamp `2.7.4`) | yes | no |
| `query_result`, `INTEGRITY_CHECK_FAILED` | no | no |
| `translation_result`, `TRANSLATED_FROM_FROZEN_REGISTRY` | yes | yes |
| its `translation_packet` | yes | yes |
| `translation_result`, `NO_SOURCE_MATCH_…`, `NO_TARGET_SCRIPT_MATCH_…`, `AMBIGUOUS_NO_SILENT_PICK` | yes | no |
| `translation_result`, `INTEGRITY_CHECK_FAILED` | no | no |
| `{}` | no | no |

### 8.2 L3_ANCHOR

| # | Check | Code |
|---|---|---|
| A.1 | `strict_mode` and `expected_artifact_sha256 is None` | `EXTERNAL_ANCHOR_REQUIRED_IN_STRICT_MODE` |
| A.2 | Anchor supplied, artifact supplied, and `AH != expected_artifact_sha256` | `EXPECTED_ARTIFACT_HASH_MISMATCH` |

### 8.3 L3_STATE

Applicable copies `[TASKLET F04]`. A copy is applicable only when its key is **present**. An absent key is not a copy and is not `None`; a present key whose value is `None` is a copy (T-R2).

| Copy | Applicable when |
|---|---|
| `receipt.restored_state_sha256` | the key is present |
| `translation_result.restored_state_sha256` | `translation_result.get("status") == "TRANSLATED_FROM_FROZEN_REGISTRY"` and the key is present |
| `translation_packet.restored_state_sha256` | the same status, `translation_packet` is exactly `dict`, and the key is present |

The status is read directly here; L3_STATE runs before L2a and does not wait for X.1. T.1 runs when at least two copies are applicable. A missing key in a translated result is reported by X.4, not by L3_STATE.

| # | Check | Code |
|---|---|---|
| T.1 | All applicable copies are `teq` to each other | `STATE_HASH_COPY_MISMATCH` |
| T.2 | If `expected_restored_state_sha256` is supplied: at least one applicable copy exists and every applicable copy is `teq` to it | `EXPECTED_STATE_HASH_MISMATCH` |

Rules:

- **T-R1 `[DEEPSEEK]`** A supplied expected state hash is a hard check in both modes. "Optional" means only that the caller may omit it.
- **T-R2 `[EXECUTED]`** A copy may legitimately be `None`: the builder copies with `.get` (`restored_query_receipt.py:42`). All-`None` copies agree under T.1; with T.2 they fail.
- **T-R3** Strict mode does **not** make the state anchor mandatory. State provenance is always reported separately through `L3_STATE` and `assurance`. `[CLAUDE][AUTHOR]`

---

## 9. L2 grounding

### 9.1 L2a internal consistency (no artifact needed)

Receipt-level check, evaluated first `[AUTHOR-TASK V0.5.1][NEW-V0.5.1]`:

| # | Check | Code |
|---|---|---|
| V.1 | Key `receipt_version` is present and its value is exactly `str` | `REQUIRED_FIELD_MISSING`, detail `receipt.receipt_version`. Evaluation continues with current rules (§3.1) |

Within L2a, V.1 is evaluated before Q.1. L2a collects: if both would fail, both are reported, V.1 first (§5.2 P-1). `[DEEPSEEK V0.5.1 V-C1]`

Apply to `query_result` (QR) when non-empty:

| # | Check | Code |
|---|---|---|
| Q.1 | `status` key present, unless `stamp == "2.7.4"` | `REQUIRED_FIELD_MISSING` |
| Q.2 | `status`, when present, is one of `OK`, `NO_MATCH`, `INTEGRITY_CHECK_FAILED` | `UNKNOWN_STATUS` |
| Q.3 | `status == "INTEGRITY_CHECK_FAILED"` | `INNER_STATUS_INTEGRITY_CHECK_FAILED`; skip Q.4 to Q.8 and all L2b checks for QR |
| Q.4 | Keys `found`, `match_count`, `symbol_ids`, `records` present | `REQUIRED_FIELD_MISSING` (one per missing key) |
| Q.4a | Every element of `records` has the key `symbol_id` `[NEW-V0.5.2]` | `REQUIRED_FIELD_MISSING` (one per element, detail `query_result.records[i].symbol_id`) |
| Q.5 | `teq(symbol_ids, [r.get("symbol_id") for r in records])` | `CROSS_FIELD_INCONSISTENT` |
| Q.6 | `teq(match_count, len(records))` | `CROSS_FIELD_INCONSISTENT` |
| Q.7 | `teq(found, len(records) > 0)` | `CROSS_FIELD_INCONSISTENT` |
| Q.8 | If `status` present: `status == "OK"` iff `len(records) > 0` | `CROSS_FIELD_INCONSISTENT` |

`[EXECUTED]` Q.5 to Q.8 hold for every genuine result of both versions (`restored_registry_query.py:113-122`).

Apply to `translation_result` (TR) when non-empty; let `P` be `translation_packet`:

| # | Check | Code |
|---|---|---|
| X.1 | `status` is one of the five strings in the table below; `AMBIGUOUS_NO_SILENT_PICK` and `INTEGRITY_CHECK_FAILED` are not valid when `stamp == "2.7.4"` | `UNKNOWN_STATUS`; skip the rest for TR |
| X.2 | `status == "INTEGRITY_CHECK_FAILED"` | `INNER_STATUS_INTEGRITY_CHECK_FAILED`; skip the rest for TR |
| X.3 | `packet_is_mapping` (defined below) is true iff `status == "TRANSLATED_FROM_FROZEN_REGISTRY"` | `STATUS_PACKET_INCONSISTENT`; skip the rest for TR |
| X.4 | Required keys for the status (table below) present | `REQUIRED_FIELD_MISSING` (one per missing key) |
| X.4a | `TRANSLATED…`: `source` and `target` each have the key `symbol_id` `[NEW-V0.5.2]` | `REQUIRED_FIELD_MISSING` |
| X.5 | `TRANSLATED…`: `teq(source.symbol_id, P.source_symbol_id)` and `teq(target.symbol_id, P.target_symbol_id)` | `CROSS_FIELD_INCONSISTENT` |
| X.6 | `AMBIGUOUS…`: `ambiguous_candidates` has at least two entries, each with `symbol_id` and `visible_symbol` | `REQUIRED_FIELD_MISSING` |

**Packet presence `[TASKLET V055-F03][NEW-V0.5.6]`.** `packet_present` is true when `translation_result` has the key `translation_packet`. `packet_is_mapping` is true exactly when `packet_present` and the value under that key is exactly `dict`; the value is looked at only after the key has been found, so an absent key is never looked up and nothing is substituted for it. An absent key and a present `None` are both "not a mapping" (row 0.7 allows no third kind of value). `P` denotes that value and is defined only when `packet_is_mapping`; every phrase "`translation_packet` is a mapping", "a packet is present" or "exactly `dict`" about the packet in §7, §8, §9 and §10 means `packet_is_mapping`. Consequences for X.3: a `TRANSLATED…` result whose packet key is absent or `None` fails X.3; any other status with a packet mapping fails X.3; any other status with the key absent or `None` passes X.3. In each failing case the code is `STATUS_PACKET_INCONSISTENT`, the detail is `translation_result.translation_packet`, and the remaining TR checks are skipped as before.

`[EXECUTED]` Closed status set and required keys:

| `translation_result.status` | `translation_packet` | Required keys |
|---|---|---|
| `TRANSLATED_FROM_FROZEN_REGISTRY` | mapping | TR: `source`, `target`, `frozen_artifact_sha256`, `restored_state_sha256`. P: `source_symbol_id`, `target_symbol_id`, `source_script_family`, `target_script_family`, `source_visible_symbol`, `target_visible_symbol`, `symbolic_role`, `meaning_invariant`, `frozen_artifact_sha256`, `restored_state_sha256`, `packet_sha256` |
| `NO_SOURCE_MATCH_IN_FROZEN_REGISTRY` | `None` | `frozen_artifact_sha256` |
| `NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY` | `None` | `source_symbol_id`, `symbolic_role`, `target_script_family`, `frozen_artifact_sha256` |
| `AMBIGUOUS_NO_SILENT_PICK` (stamp `2.7.6`+) | `None` | `source_symbol_id`, `symbolic_role`, `target_script_family`, `ambiguous_candidates`, `frozen_artifact_sha256` |
| `INTEGRITY_CHECK_FAILED` (stamp `2.7.6`+) | `None` | none (rejected by X.2) |

**Key ownership `[NEW-V0.5.3]`.** Three keys in the table above are reported by another layer and MUST NOT also be reported by X.4, so that a single missing key yields a single failure:

| Key | Reported by | Code |
|---|---|---|
| `translation_packet.packet_sha256` | L1b, check 1b.1 | `PACKET_HASH_MISSING_OR_MALFORMED` |
| `translation_packet.frozen_artifact_sha256` | L3_BINDING, check B.3 | `TRANSLATION_PACKET_PROVENANCE_MISMATCH` |
| `translation_result.frozen_artifact_sha256` | L3_BINDING, check B.5 | `ARTIFACT_HASH_COPY_MISSING` |

X.4 reports every other missing key in the table, including both `restored_state_sha256` keys. When `source_frozen_artifact` is `None`, checks B.3 and B.5 do not run (B.1) and those two missing copies go unreported; the receipt already fails with `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK`.

**Q.4a and X.4a add requirements `[NEW-V0.5.3]`.** They apply to every stamp, including `2.7.4`. Neither relaxes any rule. This document contains no exemption from Q.4, X.4, `found`, `match_count`, `symbol_ids`, `records` or the status tables for any stamp, other than the single one in Q.1 (the `status` key of a `2.7.4` query result) and the stamp-dependent statuses in X.1.

### 9.1a Execution predicates for L2a `[TASKLET F02][NEW-V0.5.4]`

Tasklet showed that the L2a expressions were undefined when an operand was missing. Principle: **a check runs if and only if every operand it names is present; a missing operand has already been reported by an earlier check.** No value is ever substituted for a missing operand. After L0 every container below has its exact type, so no check can raise. X.3 is the one presence predicate in this table: its operand is the fact `packet_is_mapping` (§9.1), which is defined when the key is absent, so X.3 runs without a packet and still substitutes nothing. `[TASKLET V055-F03]`

`QR` stands for a non-empty `query_result`; `TR` for a non-empty `translation_result`. "Stopped" means Q.3, X.1, X.2 or X.3 fired.

| Check | Runs if and only if |
|---|---|
| V.1 | always |
| Q.1 | `QR` |
| Q.2 | `QR` and key `status` present |
| Q.3 | `QR` and key `status` present |
| Q.4 | `QR` and not stopped by Q.3 |
| Q.4a, per element | Q.4 ran and key `records` present |
| Q.5 | Q.4 ran, keys `symbol_ids` and `records` present, and every element of `records` has the key `symbol_id` |
| Q.6 | Q.4 ran, keys `match_count` and `records` present |
| Q.7 | Q.4 ran, keys `found` and `records` present |
| Q.8 | Q.4 ran, keys `status` and `records` present |
| X.1 | `TR`. An absent `status` key fails X.1 |
| X.2 | `TR` and X.1 did not fire |
| X.3 | `TR` and neither X.1 nor X.2 fired. No presence condition on `translation_packet`: its absence is an input of X.3, not a reason to skip it |
| X.4 | `TR` and none of X.1, X.2, X.3 fired |
| X.4a, per side | X.4 ran, status `TRANSLATED…`, and the key `source` (respectively `target`) present |
| X.5, per side | X.4 ran, status `TRANSLATED…`, the record key present, the record has the key `symbol_id`, and `P` has the corresponding id key |
| X.6 | X.4 ran, status `AMBIGUOUS…`, and key `ambiguous_candidates` present. First the count; then, per element, the two keys |

An empty sub-object is not `QR` or `TR`: when `query_result` is `{}`, `None` or absent, no Q check runs, Q.1 included, and nothing is emitted for it; likewise for `translation_result`. `[NEW-V0.5.5]`

A check that did not run emits nothing. For every reason a check does not run, other than an empty sub-object or an inapplicable status, the missing operand was reported by Q.1, Q.4, Q.4a, X.4 or X.4a, or evaluation was stopped by Q.3, X.1, X.2 or X.3.

### 9.2 L2b grounding against the artifact (only if L3_BINDING is PASS)

`[DEEPSEEK]` DS-N1: every identity-bearing field is grounded, not only the packet. `[CLAUDE]` field list and full-record rule.

**G-1 Membership.** Before any lookup, `type(id) is str` MUST be checked; non-string ids (including lists and dicts) emit `SYMBOL_ID_NOT_IN_ARTIFACT` and MUST NOT be used as map keys. Each valid-string id MUST be a key of `RECORDS`; otherwise the same code is emitted. Failed ids skip dependent comparisons and target-resolution rules. `[CLAUDE AA-5]`

```
query_result.symbol_ids[*]
query_result.records[*].symbol_id
translation_result.source.symbol_id
translation_result.target.symbol_id
translation_result.source_symbol_id                 (NO_TARGET…, AMBIGUOUS…)
translation_result.ambiguous_candidates[*].symbol_id
translation_packet.source_symbol_id
translation_packet.target_symbol_id
```

**G-2 Full-record equality.** For each full record in `query_result.records[*]`, `translation_result.source`, `translation_result.target` whose id passed G-1: `teq(record, RECORDS[id])`; otherwise `RECORD_MISMATCH_WITH_ARTIFACT`. The whole mapping is compared, so every present or future record field is covered and no field list is needed. `[DEEPSEEK]` raised the open-ended field list; this closes it.

**G-3 Packet derivations** (`TRANSLATED…`; `S = RECORDS[P.source_symbol_id]`, `G = RECORDS[P.target_symbol_id]`). Each MUST hold under `teq`; otherwise `RECORD_MISMATCH_WITH_ARTIFACT`:

```
P.source_script_family   == S.get("script_family")
P.target_script_family   == G.get("script_family")
P.source_visible_symbol  == S.get("visible_symbol")
P.target_visible_symbol  == G.get("visible_symbol")
P.symbolic_role          == role_norm(S.get("symbolic_role", ""), stamp)
P.meaning_invariant      == S.get("meaning_invariant", [])
```

`[EXECUTED]` These match the builder (`frozen_translation_lookup.py:144-151`). `meaning_invariant` comes from the **source** record.

**G-4 Non-translated results.** For `NO_TARGET…` and `AMBIGUOUS…`: `teq(TR.symbolic_role, role_norm(RECORDS[TR.source_symbol_id].get("symbolic_role", ""), stamp))`; for each ambiguous candidate, `teq(candidate.visible_symbol, RECORDS[candidate.symbol_id].get("visible_symbol"))`. Otherwise `RECORD_MISMATCH_WITH_ARTIFACT`.

**G-5 `frozen_artifact_id`.** If the artifact mapping has the key `frozen_artifact_id`: `teq(receipt.frozen_artifact_id, artifact.frozen_artifact_id)`; otherwise `FROZEN_ARTIFACT_ID_MISMATCH`. If the artifact lacks the key the check is skipped. `[EXECUTED]` A genuine fixture exists where the artifact has no such key and the state does (`tests/test_restored_query_roundtrip.py:36`).

### 9.3 L2b target resolution (source–target semantic grounding)

`[AMENDMENT_A A-01][CLAUDE AA-5][CLAUDE F-3]` **Prerequisites.** R-1…R-3 run when L3_BINDING is PASS, L2b is reached, and the status of the translation result is not `INTEGRITY_CHECK_FAILED`. The only prerequisites are:

| Rule | Needs |
|---|---|
| R-1 | `P.source_symbol_id` and `P.target_symbol_id` passed G-1 |
| R-2 | `TR.source_symbol_id` passed G-1; key `TR.target_script_family` present (X.4) |
| R-3 | `TR.source_symbol_id` and every `TR.ambiguous_candidates[*].symbol_id` passed G-1; key `TR.target_script_family` present (X.4) |

There is **no** type prerequisite and **no** non-emptiness prerequisite on `target_script_family` or on any role. `family_norm` and `role_norm` apply `str()` to values that L0 has already limited to exact built-in types and, for `int`, to the domain of §6.1 (H-6), so the conversion cannot raise, and an empty role yields an empty candidate set by §3.4.

**No silent skip.** The exact condition under which each L2b rule runs is given in §9.4. A rule runs if and only if its condition holds. The finite code list that stood here in V0.5.1 is withdrawn: it read as exhaustive and was not. `[DEEPSEEK V0.5.1 TR-C1][NEW-V0.5.2]`

**Codes.** Missing id key → `REQUIRED_FIELD_MISSING`. Non-`str` or unknown id → `SYMBOL_ID_NOT_IN_ARTIFACT`. Valid ids, inconsistent resolution → `TARGET_RESOLUTION_INCONSISTENT`.

`[EXECUTED]` On V2.7.6: the integrity gate accepts a record whose `symbolic_role` is `""`, and the runtime answers `NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY` for such a source, so a `TRANSLATED…` receipt with an empty role is never genuine and R-1 rejects it. A genuine `NO_TARGET…` result stores `target_script_family` exactly as the caller passed it (`None` and `5` were observed), so the rules must accept non-`str` values there.

`[CLAUDE]` K-07, `[AUTHOR]` go decision, `[NEW-V0.3]` for the rules below. Without them, a receipt naming a real source and an unrelated real target passes G-1 to G-4.

Let `role = role_norm(S.get("symbolic_role", ""), stamp)`.

**R-1 `TRANSLATED…`.** Let `C = candidates(role, family_norm(G.get("script_family", ""), stamp), stamp)`.

- `G` MUST be a member of `C`.
- If `stamp != "2.7.4"`: the candidates MUST NOT be ambiguous (more than one candidate with more than one distinct `nfc(visible_symbol)`, as defined by `normalized_surface` in §3.4), and `G` MUST be the first element of `C` sorted by `str(symbol_id)`.
- Otherwise `TARGET_RESOLUTION_INCONSISTENT`.

**Self-translation `[AUTHOR-TASK V0.5.1][EXECUTED]`.** `G` may be the same record as `S`. On V2.7.6 and V2.7.5, translating a symbol into its own script family returns `TRANSLATED_FROM_FROZEN_REGISTRY` with `source_symbol_id == target_symbol_id` when the source is the only record of its role in that family. With two same-role records of identical surface in that family, V2.7.6 returns the one that sorts first, which can differ from the source. With two of different surface, V2.7.6 returns `AMBIGUOUS_NO_SILENT_PICK` and V2.7.5 returns the first in insertion order. R-1 accepts all of these as written. No rule in this document may reject a receipt because source and target are the same record.

**The requested family is not recorded `[EXECUTED][NEW-V0.5.2]`.** A `TRANSLATED…` result and its packet carry the target record's own `script_family`; they do not carry the family the caller asked for. On V2.7.6, a self-translation receipt whose target is rewritten consistently to the same-role record of another family is identical, apart from `generated_at_utc` and `receipt_sha256`, to the genuine receipt for that other family. Such a receipt MUST verify (control NC22). A test that expects it to be rejected, as proposed in `DEEPSEEK_V277_V051_ADVERSARIAL_REVIEW_V0.1` ST-C1, would force rejection of genuine receipts and is not adopted.

**R-2 `NO_TARGET_SCRIPT_MATCH…`.** `candidates(role, family_norm(TR.target_script_family, stamp), stamp)` MUST be empty; otherwise `TARGET_RESOLUTION_INCONSISTENT`.

**R-3 `AMBIGUOUS_NO_SILENT_PICK`.** Let `C` be as in R-2. The `symbol_id` values in `ambiguous_candidates` MUST be pairwise distinct `[TASKLET F08][AUTHOR F08]`, the set of them MUST equal the set of `symbol_id` in `C`, and `C` MUST contain more than one distinct `nfc(visible_symbol)` (`normalized_surface`, §3.4); otherwise `TARGET_RESOLUTION_INCONSISTENT`. Equivalently: the candidate list is a permutation of `C`. Its order is not checked, because the artifact hash does not preserve insertion order. `[EXECUTED]` The runtime builds candidates from distinct records, so a genuine list never repeats an id; V2.7.6 accepts `[A, B, A]` today. This rule applies to `ambiguous_candidates` only. It MUST NOT be applied to `query_result.symbol_ids` or `records`: `[EXECUTED]` on V2.7.6 and V2.7.5 a query by an alias that one record lists twice genuinely returns that record twice.

`[EXECUTED]` R-1 to R-3 mirror the runtime (`frozen_translation_lookup.py:99-139`, `unicode_normalization.py:54-78`). For stamp `2.7.4` the runtime took the first candidate in insertion order (`frozen_translation_lookup.py:103 @2b7dd62`), which the artifact hash does not preserve, so only membership can be checked.

**What §9.3 does not do.** It does not replay the query, and it does not replay source resolution (which record a query string selects). See §12, R-2.

### 9.4 Execution predicates for L2b rules `[DEEPSEEK V0.5.1 TR-C1][NEW-V0.5.2]`

Each rule below MUST run when its predicate is true and MUST NOT run when it is false. There is no discretion: this is what makes `failures` identical across implementations (§5.2 P-4).

Gates:

```
L2B      = (layers.L3_BINDING == PASS)
QR_GATE  = L2B and query_result is non-empty and its status is not "INTEGRITY_CHECK_FAILED"
TR_GATE  = L2B and translation_result is non-empty and none of X.1, X.2, X.3 fired
passed(p) = position p exists, its key is present, and its value passed G-1
```

| Rule | Runs if and only if |
|---|---|
| G-1 at `query_result.symbol_ids[i]` | `QR_GATE` and key `symbol_ids` present |
| G-1 at `query_result.records[i].symbol_id` | `QR_GATE`, key `records` present, and that element has the key `symbol_id` |
| G-1 at `translation_result.source.symbol_id`, `.target.symbol_id` | `TR_GATE`, status `TRANSLATED…`, the record key (`source` / `target`) present, and it has the key `symbol_id` |
| G-1 at `translation_packet.source_symbol_id`, `.target_symbol_id` | `TR_GATE`, status `TRANSLATED…`, and the key present in `P` |
| G-1 at `translation_result.source_symbol_id` | `TR_GATE`, status `NO_TARGET…` or `AMBIGUOUS…`, and the key present |
| G-1 at `translation_result.ambiguous_candidates[i].symbol_id` | `TR_GATE`, status `AMBIGUOUS…`, key `ambiguous_candidates` present, and that element has the key `symbol_id` |
| G-2 for a full record | `passed` for that record's `symbol_id` |
| G-3, each line that uses `S` | `TR_GATE`, status `TRANSLATED…`, `passed(P.source_symbol_id)`, and the packet key on the left of that line present |
| G-3, each line that uses `G` | `TR_GATE`, status `TRANSLATED…`, `passed(P.target_symbol_id)`, and the packet key on the left of that line present |
| G-4, role line | `TR_GATE`, status `NO_TARGET…` or `AMBIGUOUS…`, `passed(TR.source_symbol_id)`, and key `symbolic_role` present |
| G-4, line for candidate `i` | `TR_GATE`, status `AMBIGUOUS…`, `passed` for that candidate's `symbol_id`, and that candidate has the key `visible_symbol` |
| G-5 | `L2B` and the artifact mapping has the key `frozen_artifact_id`. An absent `receipt.frozen_artifact_id` is a mismatch |
| R-1 | `TR_GATE`, status `TRANSLATED…`, `passed(P.source_symbol_id)` and `passed(P.target_symbol_id)` |
| R-2 | `TR_GATE`, status `NO_TARGET…`, `passed(TR.source_symbol_id)`, and key `target_script_family` present |
| R-3 | `TR_GATE`, status `AMBIGUOUS…`, `passed(TR.source_symbol_id)`, key `target_script_family` present, key `ambiguous_candidates` present, and `passed` for every candidate's `symbol_id` |

**Consequence (to be checked by reviewers, not an extra rule).** Whenever a predicate is false for a reason other than "that status does not apply", "that sub-object is empty", or the one permitted case below, a failure has already been emitted, by exactly one of these:

| Reason the predicate is false | Failure already in `failures` |
|---|---|
| `L2B` false | an L3_BINDING code (§8.1) |
| `QR_GATE` false through status | `INNER_STATUS_INTEGRITY_CHECK_FAILED` (Q.3) |
| `TR_GATE` false | `UNKNOWN_STATUS` (X.1), `INNER_STATUS_INTEGRITY_CHECK_FAILED` (X.2) or `STATUS_PACKET_INCONSISTENT` (X.3) |
| a key is absent | `REQUIRED_FIELD_MISSING` from Q.4, Q.4a, X.4, X.4a or X.6 |
| G-5 only: the artifact has no `frozen_artifact_id` key | **none; this is the one permitted skip without a failure** (§9.2 G-5) `[TASKLET F06]` |
| an id did not pass G-1 | `SYMBOL_ID_NOT_IN_ARTIFACT` |

No predicate in this section depends on whether `S` and `G` are the same record; the Self-translation paragraph of §9.3 stays in force. `[DEEPSEEK V0.5.2 E-C3]`

A failed id does not make a G-1 predicate false: G-1 runs on a present key and reports the bad id itself. `[TASKLET F06]`

**G-1 does not depend on `passed` `[DEEPSEEK V0.5.4 L2B-C1, reworded]`.** A G-1 predicate depends only on its gate and on the presence of the key at that position. The value there may be of any supported type. G-1 then emits `SYMBOL_ID_NOT_IN_ARTIFACT` when the value is not exactly `str`, or is a `str` that is not a key of `RECORDS`; otherwise the position has `passed`. The review's proposed wording made the predicate require that the value be a record key, which would stop G-1 from reporting an unknown id; that wording is not adopted.

**A missing query `status` never closes `QR_GATE` `[DEEPSEEK V0.5.4 L2B-C2, reworded]`.** `QR_GATE` is closed only by the exact value `"INTEGRITY_CHECK_FAILED"`. An absent `status` key leaves it open for every stamp. So Q.1's `REQUIRED_FIELD_MISSING` (stamp other than `2.7.4`) is not a reason any L2b rule fails to run and does not belong in the table above, and a `2.7.4` query result without `status` is grounded by G-1 and G-2 exactly like any other. For `translation_result`, an absent `status` fails X.1 and closes `TR_GATE`; that case is in the table.

**Single owner for a missing key `[DEEPSEEK V0.5.4 E-C2]`.** Every key that a §9.4 predicate requires to be present has exactly one L2a check that reports its absence. No L2b rule reports a missing key (P-7), so one missing key yields one failure.

| Key required by a §9.4 predicate | Owner |
|---|---|
| `query_result.symbol_ids`, `query_result.records` | Q.4 |
| `query_result.records[i].symbol_id` | Q.4a |
| `translation_result.source`, `.target`, `.source_symbol_id`, `.symbolic_role`, `.target_script_family`, `.ambiguous_candidates` | X.4 |
| `translation_result.source.symbol_id`, `.target.symbol_id` | X.4a |
| `translation_packet.source_symbol_id`, `.target_symbol_id` and the packet keys on the left of G-3 lines | X.4 |
| `ambiguous_candidates[i].symbol_id`, `[i].visible_symbol` | X.6 |

The three hash keys of §9.1 "Key ownership" are not required by any §9.4 predicate and keep their owners there.

`CROSS_FIELD_INCONSISTENT` and `RECORD_MISMATCH_WITH_ARTIFACT` never stop a later rule. A rule that did not run never emits `TARGET_RESOLUTION_INCONSISTENT` and is never reported as passed: `layers.L2` is `FAIL` through the earlier failure.

`[EXECUTED]` On V2.7.6, a `TRANSLATED…` receipt whose `source` lacks `symbol_id`, and a query result whose record lacks `symbol_id` while `symbol_ids` is `[None]`, both verify today. Q.4a and X.4a give these cases their own failure, so that G-2 is never left unevaluated without one.

---

## 10. L4 policy

### 10.1 Always evaluated

| # | Check | Code |
|---|---|---|
| L4.1 | `receipt_type == "EIT_RESTORED_REGISTRY_QUERY_RECEIPT"` | `WRONG_RECEIPT_TYPE` (existing) |
| L4.2 | `boundary.get(key) is expected` for the four fixed pairs below | `BOUNDARY_VIOLATION:<key>` (existing) |

`[EXECUTED]` `<key>` is one of exactly four constants in the code (`receipt_verifier.py:41-46`): `read_only_query_mode` (True), `restored_registry_remains_frozen` (True), `mutation_guard_enforced` (True), `real_world_control` (False). It is never taken from the receipt. `[DEEPSEEK]` asked for this bound to be stated. Extra keys in `boundary` are ignored. An absent `boundary` key is evaluated as `{}` here and yields all four codes; `boundary: None` never reaches L4 (§6.4, S-6).

### 10.2 Strict mode only

| # | Check | Code |
|---|---|---|
| L4.3 | `(receipt_version, module_id)` is one of the pairs in §10.3, compared as exact, case-sensitive strings | `POLICY_RECEIPT_VERSION_NOT_ALLOWED` if the version is not listed; else `POLICY_MODULE_ID_NOT_ALLOWED` |
| L4.4 | If a packet is present: `teq(packet_version, receipt_version)` | `POLICY_RECEIPT_VERSION_NOT_ALLOWED` |
| L4.5 | `generated_at_utc` is a `str`, `datetime.fromisoformat` parses it, and its UTC offset is zero | `POLICY_TIMESTAMP_MALFORMED` |

L4.5 assumes Python 3.11 or later; CI uses 3.12 (`verify.yml:30`).

**Conformance profile `[TASKLET V056-F03][AUTHOR V0.5.7][NEW-V0.5.7]`.** A conformance profile is the triple: Python implementation name, its version (`sys.version_info`), and the Unicode database version (`unicodedata.unidata_version`). Three things in this document depend on it: `nfc` (§3.2), `.upper()` (§3.2), and `datetime.fromisoformat` (L4.5). Everything else is defined without reference to the interpreter. This document does not pin a single profile and does not claim that two profiles agree on every input; no cross-profile comparison has been run. Every test report for V2.7.7 MUST record the profile it ran under. A verifier MUST NOT try to detect or compensate for the profile at run time.

### 10.3 Allow-list and builder stamps `[AUTHOR][EXECUTED]`

| `receipt_version` | `module_id` |
|---|---|
| `2.7.4` | `EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4` |
| `2.7.6` | `EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_6` |
| `2.7.7` | `EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7` |

The V2.7.7 builders MUST stamp `receipt_version`, `module_id` and `packet_version` with the `2.7.7` values. The allow-list is a constant tuple of pairs in `receipt_verifier.py`.

Policy checks are conformance checks. They do not authenticate a producer (§12).

---

## 11. Tests

### 11.1 Fixtures (D-1) `[AUTHOR][CLAUDE][DEEPSEEK]`

- **F-1 `[EXECUTED]`** All five tests in `tests/test_receipt_verifier.py` (`:36-76`) share `_receipt()` (`:16-33`), which claims `found: True` and a translation over an artifact with zero records. All five MUST move to a genuine fixture: an artifact with real records, a sealed state, results produced by `query_restored_registry` and `lookup_translation_from_frozen_registry`.
- **F-2** The retired fixture is preserved as a data file, `tests/legacy/invalid_positive_receipt_v276.json`, with a `README.md` beside it. Because the directory contains no `test_*.py` or `*_test.py` file, pytest does not collect it. Both files are listed in `SHA256SUMS` and `ARTIFACT_REGISTRY.json`.
- **F-3** One active test loads that file and asserts that V2.7.7 rejects it with `REQUIRED_FIELD_MISSING`. The legacy fixture becomes negative evidence.
- **F-4** V2.7.5 at `2b7dd62` is not touched.
- **F-5 Legacy data fixtures `[DEEPSEEK V0.5.1 NCN-C1, NCN-C2][NEW-V0.5.2]`** The V2.7.7 candidate does not contain V2.7.5 code, so legacy controls MUST NOT build receipts at test time. They load static JSON files from `tests/legacy/v275/`:

  | File | Used by | Content |
  |---|---|---|
  | `full_translation.json` | NC9 | query hit + `TRANSLATED…` |
  | `first_pick_multi_target.json` | NC18 | several same-role targets; runtime took the first |
  | `self_translation.json` | NC19 | source translated into its own family |
  | `no_target.json` | NC19 | `NO_TARGET_SCRIPT_MATCH…` |
  | `no_source.json` | NC19 | `NO_SOURCE_MATCH…` |
  | `query_only.json` | NC19 | no translation result |
  | `multi_hit_query.json` | NC19 | query matching several records |
  | `key_id_mismatch.json` | F09b | receipt over an artifact with a record whose stored `symbol_id` differs from its key; expected to be **rejected** |
  | `no_target_none_family.json` | NC21 | `NO_TARGET_SCRIPT_MATCH…` produced with `target_script_family=None` |

  Each file is a JSON object with exactly the keys `artifact`, `receipt` and `provenance`. `provenance` records the commit (`2b7dd628de411b5bb421310ead16b998d61a7f54`), the Python version, and the call that produced the receipt. The files are generated once, outside the candidate tree, by running the unmodified code of commit `2b7dd62`, and are never regenerated by the test suite. `tests/legacy/v275/README.md` gives the generation commands. All files are listed in `SHA256SUMS` and `ARTIFACT_REGISTRY.json`. The directory contains no `test_*.py` or `*_test.py` file. Except for `key_id_mismatch.json`, the artifact of every fixture MUST satisfy record-key identity (§6.2 row 0.10); `[EXECUTED]` the artifacts used for the legacy evidence in Appendix B do. One active test asserts for every fixture that `receipt.receipt_version == "2.7.4"` and that the stored `receipt_sha256` equals `sha256_json` of the stored receipt, so a damaged fixture cannot pass as a control.

### 11.2 Harness rules `[CLAUDE]`

- **T-1** Forged receipts are built from a deep copy of a genuine receipt. `[EXECUTED]` Result records alias the artifact (`restored_registry_query.py:113`); forging in place corrupts the artifact.
- **T-2** The artifact snapshot for the no-mutation check is taken before the receipt is built.
- **T-10 Outcome classes `[TASKLET V058-F01][AUTHOR V0.5.9][NEW-V0.5.9]`** A test report assigns every row of §11.3 and §11.4 exactly one of six outcomes and lists the rows of each outcome separately: executed and passed (`PASS`); executed and failed (`FAIL`); not executed (`NOT_RUN`); `NOT_APPLICABLE`; known-risk characterization (`RISK_PRESENT` or `RISK_MITIGATED`, T-5); harness error. `NOT_APPLICABLE` is none of the other five. It is not an executed test and not a passed test, and it MUST NOT be counted or displayed as either. It is available for exactly one row, S4d, under the condition stated in that row, and for no other row of either table. A successful exit of the test runner is not a statement that every listed row was executed.
- **T-9 Unique identifiers `[TASKLET V057-F02][AUTHOR V0.5.8][NEW-V0.5.8]`** Every row of §11.3 and §11.4 has an identifier that no other row of either table has. An inventory check of the test tables MUST fail on a repeated identifier.
- **T-3** Every rejecting test asserts the specific code in the table below, not only `verified is False`.
- **T-4** Labels:
  - `FAIL_FIRST`: fails by assertion on V2.7.6 and must pass on V2.7.7.
  - `NEW_API`: uses new parameters or result keys; cannot run on V2.7.6.
  - `CONTROL`: must pass on V2.7.6 and V2.7.7.
  - `CONTROL_FOR_V277`: a control that needs the V2.7.7 builder; must pass on V2.7.7. `[AMENDMENT_A A-07]`
  - `KNOWN_RISK`: characterization of an accepted open risk. `[AMENDMENT_A A-06]`
- **T-6 Hash feasibility `[TASKLET V056 review §6][NEW-V0.5.7]`** The table heading "all hashes recomputed unless stated" cannot apply where the forged object cannot be hashed or must not be: in CF1, CF2, CF2a and CF3 the stored hashes are kept well-formed from the genuine receipt and the surrogate is inserted afterwards without recomputing; in BI1 and BI2 the out-of-range value is inserted into a genuine receipt or artifact afterwards without recomputing. L0 and H-5 decide those cases before any stored hash matters.
- **T-7 Hostile objects `[TASKLET V056-F04][AUTHOR V0.5.7][NEW-V0.5.7]`** A hostile object used as a value or key is built unarmed: its `__eq__`, `__str__`, `__repr__` and `__hash__` behave normally while the fixture is constructed, so that it can be inserted as a `dict` key. After construction the test arms it (from then on each of the four methods sets a flag and raises) and clears every flag, immediately before the verifier is called. The test asserts after the call that every flag is still clear. A fixture that cannot be constructed is a harness error, never a verifier result.
- **T-8 Profile record `[TASKLET V056-F03][NEW-V0.5.7]`** Each test report records the conformance profile of §10.2.
- **T-5 `KNOWN_RISK` handling `[AMENDMENT_A A-06][CLAUDE m-6]`** A `KNOWN_RISK` test runs in the ordinary test suite and MUST NOT fail it on either outcome. It records the observed outcome in the test report (for example with pytest's `record_property`) as `RISK_PRESENT` or `RISK_MITIGATED`. It MUST NOT assert that the vulnerable behaviour persists. No change to `.github/workflows/verify.yml` is required, so §0.2 is unchanged. A changed outcome is reviewed by a person; it is not an automatic regression.

### 11.3 Controls (must verify, `failures == []`, default mode)

| ID | Case | V2.7.6 today |
|---|---|---|
| NC1 | Genuine query + translation | `[EXECUTED]` verifies |
| NC2 | Query-only; `translation_result` omitted or `None` | `[EXECUTED]` verifies |
| NC3 | Artifact with zero records, genuine miss | `[EXECUTED]` verifies |
| NC4a | NFC-stored record, NFD query | `[EXECUTED]` verifies |
| NC4b | NFD-stored record, NFC query | `[EXECUTED]` verifies |
| NC5 | Boundary block intact | `[EXECUTED]` verifies |
| NC6 | `NO_MATCH` query with `NO_SOURCE_MATCH…` translation | `[EXECUTED]` verifies |
| NC7 | `NO_TARGET_SCRIPT_MATCH…` | `[EXECUTED]` verifies |
| NC8 | `AMBIGUOUS_NO_SILENT_PICK` | `[EXECUTED]` verifies |
| NC9 | Receipt built by V2.7.5 code (stamp `2.7.4`, query result without `status`) | `[EXECUTED]` verifies |
| NC10 | Target chosen among identical surfaces (`RESOLVED_IDENTICAL_SURFACES`) | `[NEW-V0.3]` |
| NC11 | Query matching several records (by role or family) | `[NEW-V0.3]` |
| NC12 | Receipt with neither query nor translation | `[NEW-V0.3]` |
| NC13 | Genuine V2.7.7-builder receipt, default mode, artifact supplied, no external anchors | `verified=True`, `failures=[]`, `layers.L3_ANCHOR=NOT_EVALUATED`, `layers.L3_STATE=NOT_EVALUATED`, `layers.L2=PASS`, `assurance=CONSISTENCY_ONLY`; `CONTROL_FOR_V277 / NEW_API`, not runnable until the V2.7.7 builder exists |
| NC14 | Genuine `NO_TARGET_SCRIPT_MATCH…` receipt produced with `target_script_family` of `None`, and of `5` `[CLAUDE F-3]` | `[EXECUTED]` verifies; CONTROL |
| NC15 | Genuine `NO_TARGET_SCRIPT_MATCH…` receipt whose source record has `symbolic_role` `""` `[CLAUDE F-3]` | `[EXECUTED]` verifies; CONTROL |
| NC16 | Genuine self-translation: unique source translated into its own family; `source_symbol_id == target_symbol_id` `[AUTHOR-TASK V0.5.1]` | `[EXECUTED]` verifies; CONTROL |
| NC17 | Genuine self-family translation with two identical-surface records; target is the first by `str(symbol_id)` and differs from the source `[AUTHOR-TASK V0.5.1]` | `[EXECUTED]` verifies; CONTROL |
| NC18 | Legacy: receipt built by V2.7.5 code where several same-role targets exist and the runtime took the first (stamp `2.7.4`, status `TRANSLATED…`) `[AUTHOR-TASK V0.5.1]` | `[EXECUTED]` verifies on V2.7.6; satisfies R-1 membership; CONTROL |
| NC19 | Legacy: V2.7.5-built self-translation, `NO_TARGET…`, `NO_SOURCE_MATCH…`, query-only and multi-hit query receipts `[AUTHOR-TASK V0.5.1]` | `[EXECUTED]` each verifies on V2.7.6 and violates no rule of §8–§9; CONTROL |
| NC20 | Genuine receipt whose `receipt_version` is an unlisted string, default mode `[NEW-V0.5.1]` | verifies under current rules; in strict mode fails with `POLICY_RECEIPT_VERSION_NOT_ALLOWED`; NEW_API |
| NC21 | Legacy: V2.7.5-built `NO_TARGET_SCRIPT_MATCH…` receipt with `target_script_family` of `None` (fixture, F-5) `[DEEPSEEK V0.5.1 RV-C1]` | `[EXECUTED]` stamp is `2.7.4`; verifies on V2.7.6; violates no rule of §8–§9; CONTROL |
| NC23 | Genuine query by an alias that one record lists twice: `symbol_ids` and `records` contain that record twice `[TASKLET F08][EXECUTED]` | verifies on V2.7.6 and V2.7.5; MUST verify. Guards against applying the uniqueness rule of R-3 to query results; CONTROL |
| NC22 | Cross-family: a genuine self-translation receipt with `target`, `target_symbol_id`, `target_script_family` and `target_visible_symbol` rewritten consistently to the same-role record of another family, hashes recomputed `[NEW-V0.5.2]` (replaces DeepSeek ST-C1) | MUST verify. `[EXECUTED]` on V2.7.6 it equals the genuine receipt for that family except for `generated_at_utc` and `receipt_sha256`; CONTROL. The base receipt is produced by the builder under test, so it carries stamp `2.7.6` on V2.7.6 and `2.7.7` on V2.7.7 `[DEEPSEEK V0.5.2 N-C1]`. `[EXECUTED]` The same equality holds for V2.7.5 code (stamp `2.7.4`); no extra legacy fixture is needed because `full_translation.json` (F-5) already is a genuine `2.7.4` cross-family receipt |

### 11.4 Adversarial cases

| ID | Forgery (all hashes recomputed unless stated) | Required code | Label |
|---|---|---|---|
| A | Nonexistent packet ids; packet hash left stale | `PACKET_HASH_MISMATCH_TAMPER_DETECTED` and `SYMBOL_ID_NOT_IN_ARTIFACT` | FAIL_FIRST |
| B | Nonexistent packet ids | `SYMBOL_ID_NOT_IN_ARTIFACT` | FAIL_FIRST |
| B-full | Nonexistent ids mirrored in every id field | `SYMBOL_ID_NOT_IN_ARTIFACT` | FAIL_FIRST |
| C1 | `P.source_symbol_id` is another existing record | `CROSS_FIELD_INCONSISTENT` | FAIL_FIRST |
| C2 | Target id kept, `target_visible_symbol` from another record | `RECORD_MISMATCH_WITH_ARTIFACT` | FAIL_FIRST |
| C3 | `symbol_ids` differs from `records[*].symbol_id` | `CROSS_FIELD_INCONSISTENT` | FAIL_FIRST |
| E1 | Record field `1` replaced by `True`; and by `1.0` | `RECORD_MISMATCH_WITH_ARTIFACT` | FAIL_FIRST |
| E2 | Stored NFD value replaced by its NFC form in a receipt copy `[DEEPSEEK]` | `RECORD_MISMATCH_WITH_ARTIFACT` | FAIL_FIRST |
| E3 | `match_count` wrong; `found` wrong | `CROSS_FIELD_INCONSISTENT` | FAIL_FIRST |
| R1 | Real source paired with a real target of another role, written consistently as in ST1 `[TASKLET F07]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| R2 | Same-role target that the runtime would not choose, written consistently as in ST1 `[TASKLET F07]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| R3 | `AMBIGUOUS…` with one candidate removed | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| R4 | `NO_TARGET…` claimed for a family that has targets | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| M1 | Packet id keys deleted | `REQUIRED_FIELD_MISSING` | FAIL_FIRST |
| M2 | `packet_sha256` deleted | `PACKET_HASH_MISSING_OR_MALFORMED` | FAIL_FIRST |
| M3 | Status `TRANSLATED…`, packet `None` | `STATUS_PACKET_INCONSISTENT` | FAIL_FIRST |
| M4 | Unknown status string | `UNKNOWN_STATUS` | FAIL_FIRST |
| M5 | Query copy of the artifact hash removed; and altered | `ARTIFACT_HASH_COPY_MISSING`; `ARTIFACT_HASH_COPY_MISMATCH` | FAIL_FIRST |
| M6 | State hash copies disagree | `STATE_HASH_COPY_MISMATCH` | FAIL_FIRST |
| M7 | `frozen_artifact_id` forged, artifact carries the key | `FROZEN_ARTIFACT_ID_MISMATCH` | FAIL_FIRST |
| M8 | Receipt recording a failed integrity gate | `INNER_STATUS_INTEGRITY_CHECK_FAILED` | FAIL_FIRST |
| M9 | Legacy fixture file (F-3); zero-record artifact with a positive claim `[DEEPSEEK]` | `REQUIRED_FIELD_MISSING` | FAIL_FIRST |
| S1 | `receipt=None`; `translation_result=[1]`; `query_result="x"`; artifact `"str"`; records map a list | `RECEIPT_SHAPE_INVALID` / `ARTIFACT_SHAPE_INVALID`, exactly one entry in `failures`, no exception | FAIL_FIRST |
| S2 | Artifact `None` | `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK` | CONTROL (existing test) |
| S3 | Three simultaneous defects: wrong `receipt_type`; packet hash left stale after altering `packet_type`; wrong `match_count` `[DEEPSEEK]` | `failures` equals exactly, in this order: `PACKET_HASH_MISMATCH_TAMPER_DETECTED`, `CROSS_FIELD_INCONSISTENT`, `WRONG_RECEIPT_TYPE` | NEW_API |
| S4 | More than 32 defects | 32 entries then `FAILURES_TRUNCATED` | NEW_API |
| S4a | Exactly 32 distinct failures: a consistent query result with 16 unknown ids (`symbol_ids`, `records`, `match_count`, `found` all agreeing), binding passing `[TASKLET F12]` | 32 entries, all `SYMBOL_ID_NOT_IN_ARTIFACT`; `FAILURES_TRUNCATED` absent | NEW_API |
| S4b | The same with 17 unknown ids (34 distinct failures) `[TASKLET F12]` | exactly 33 entries: 32 `SYMBOL_ID_NOT_IN_ARTIFACT`, then `FAILURES_TRUNCATED` | NEW_API |
| S5 | Attacker-chosen text in ids and extra `boundary` keys `[DEEPSEEK]` | No such text in `failures` or `failure_details` | NEW_API |
| N1 | Strict mode, no anchor | `EXTERNAL_ANCHOR_REQUIRED_IN_STRICT_MODE` | NEW_API |
| N2 | Anchor differs; state anchor differs (default mode and strict mode) `[DEEPSEEK]` | `EXPECTED_ARTIFACT_HASH_MISMATCH`; `EXPECTED_STATE_HASH_MISMATCH` | NEW_API |
| N3 | Strict mode: `module_id` not paired; version not listed; `packet_version` differs; timestamp not ISO or not UTC | the three `POLICY_*` codes | NEW_API |
| N4 | Strict mode, genuine receipts stamped `2.7.4`, `2.7.6`, `2.7.7` with a correct anchor | verifies; `assurance == "ARTIFACT_ANCHORED"` | NEW_API |
| N5 | Default mode, genuine receipt | `layers.L3_ANCHOR == "NOT_EVALUATED"`, `assurance == "CONSISTENCY_ONLY"` | NEW_API |
| N6 | Malformed `expected_*` argument | `EXPECTED_ANCHOR_MALFORMED` | NEW_API |
| R5 | `AMBIGUOUS…` with a non-`str` `target_script_family` and a candidate list of arbitrary existing ids `[CLAUDE F-3]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| R6 | `TRANSLATED…` whose source record has `symbolic_role` `""` `[CLAUDE F-3]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| P1 | Packet or result id key missing `[AMENDMENT_A A-01]` | `REQUIRED_FIELD_MISSING`; `TARGET_RESOLUTION_INCONSISTENT` absent | FAIL_FIRST |
| P2 | Id that is an `int`, `None`, a `list`, a `dict` `[CLAUDE AA-5]` | `SYMBOL_ID_NOT_IN_ARTIFACT`; `TARGET_RESOLUTION_INCONSISTENT` absent; no exception | FAIL_FIRST |
| T1 | `tuple`, `set`, `bytes`, custom instance, `dict` subclass, `int` subclass, `str` subclass, each **inside** the input: as the value of a top-level key of the receipt, nested deeper in the receipt, as the value of a top-level key of the artifact, and nested inside a record `[AMENDMENT_A A-03][CLAUDE AA-7][TASKLET F05]` | exactly one entry, `REJECT_UNTRUSTED_OBJECT_TYPE`; `layers.L0 == "FAIL"` | NEW_API |
| T1r | The same unsupported types **as the root**: `receipt` itself, and `source_frozen_artifact` itself `[TASKLET F05]` | exactly one entry: `RECEIPT_SHAPE_INVALID` (row 0.2), respectively `ARTIFACT_SHAPE_INVALID` (row 0.8). The scan is never reached | NEW_API |
| T2 | Non-`str` `dict` key: as a top-level key of the receipt, nested inside `query_result`, as a top-level key of the artifact, and nested inside a record `[DEEPSEEK V0.5.1 RV-C9]` | exactly one entry, `REJECT_UNTRUSTED_OBJECT_TYPE` | NEW_API |
| T3 | Cyclic value and 33 levels of nesting, each in four placements: starting at the receipt root, nested inside `query_result`, starting at the artifact root, nested inside a record `[DEEPSEEK V0.5.1 RV-C11]` | exactly one entry, `RECEIPT_SHAPE_INVALID` / `ARTIFACT_SHAPE_INVALID` | NEW_API |
| T4 | Objects whose `__eq__`, `__str__`, `__repr__`, `__hash__` raise, as values and as keys, including a key whose hash collides with `"frozen_registry_snapshot"` `[NEW-V0.5]` | `REJECT_UNTRUSTED_OBJECT_TYPE`; none of those methods was called. Each hostile object carries a flag that every one of the four methods sets before raising; the test clears the flags after the input structure has been built (inserting an object as a key calls its `__hash__`) and asserts they are all still clear after the call `[DEEPSEEK V0.5.1 L0S-C1]`. Construction and arming follow T-7: the objects are unarmed while the structure is built and armed after it `[TASKLET V056-F04]` | NEW_API |
| T5 | A record in `registry_records` that is a `str`, a `list`, `None`; not referenced by the receipt `[CLAUDE F-2]` | exactly one entry, `ARTIFACT_SHAPE_INVALID` | NEW_API |
| T6 | Malformed `expected_*` together with an unsupported type in the receipt | exactly one entry, `EXPECTED_ANCHOR_MALFORMED` (S-5) | NEW_API |
| T7 | Scan failure deep under attacker-named keys | `failure_details` matches `<root>:depth=<n>:path=<digits and dots>` only | NEW_API |
| T8 | A number or `bool` where a hash or version string is expected (state-hash copy, `packet_version`) `[AMENDMENT_A A-04]` | `STATE_HASH_COPY_MISMATCH`; in strict mode `POLICY_RECEIPT_VERSION_NOT_ALLOWED` | NEW_API |
| O1 | Simultaneous defects with binding failing: altered query copy of the artifact hash; wrong `match_count`; wrong `receipt_type` `[AMENDMENT_A A-02][CLAUDE m-5]` | `failures` equals exactly, in order: `ARTIFACT_HASH_COPY_MISMATCH`, `CROSS_FIELD_INCONSISTENT`, `WRONG_RECEIPT_TYPE`; `layers.L2 == "FAIL"` | NEW_API |
| O2 | Simultaneous defects with binding passing: wrong `match_count`; one altered field in `records[0]`; wrong `receipt_type` `[CLAUDE m-5]` | `failures` equals exactly, in order: `CROSS_FIELD_INCONSISTENT`, `RECORD_MISMATCH_WITH_ARTIFACT`, `WRONG_RECEIPT_TYPE` | NEW_API |
| V1 | `receipt_version` key deleted `[AUTHOR-TASK V0.5.1]` | `REQUIRED_FIELD_MISSING`; no exception; legacy rules not applied | FAIL_FIRST |
| V2 | `receipt_version` is a number, `None`, a `list` `[AUTHOR-TASK V0.5.1]` | `REQUIRED_FIELD_MISSING`; no exception | FAIL_FIRST |
| V3 | Stamp `2.7.4` with status `AMBIGUOUS_NO_SILENT_PICK` or `INTEGRITY_CHECK_FAILED`; stamp `2.7.6` with a query result lacking `status` | `UNKNOWN_STATUS`; `REQUIRED_FIELD_MISSING` | FAIL_FIRST |
| B1 | `boundary: None` `[AUTHOR-TASK V0.5.1]` | exactly one entry, `RECEIPT_SHAPE_INVALID`; no exception | FAIL_FIRST (V2.7.6 raises) |
| B2 | `boundary` key absent; `boundary: {}` | the four `BOUNDARY_VIOLATION:<key>` codes | CONTROL (unchanged behaviour) |
| SM1 | `strict_mode` is `"False"`, `"True"`, `0`, `1`, `None`, a `list`, and a custom object whose `__bool__` returns `True` and sets a flag (the flag MUST remain clear) `[AUTHOR-TASK V0.5.1][DEEPSEEK V0.5.1 RV-C3]` | exactly one entry, `STRICT_MODE_NOT_BOOL`; strict checks neither applied nor skipped by truthiness | NEW_API |
| SM2 | Malformed `strict_mode` together with a malformed anchor and an unsupported type in the receipt | exactly one entry, `STRICT_MODE_NOT_BOOL` (S-5) | NEW_API |
| ST1 | Self-translation receipt with the target replaced **consistently** by another same-family record of a different role: `translation_result.target` is that full record, and `P.target_symbol_id`, `P.target_script_family`, `P.target_visible_symbol` are taken from it; hashes recomputed `[TASKLET F07]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| V4 | Genuine receipt with `receipt_version` rewritten to `"9.9.9"`, hashes recomputed, default mode, correct artifact and state anchors `[DEEPSEEK V0.5.1 U-C2]` | verifies; no `POLICY_*` code; `assurance == "ARTIFACT_AND_STATE_ANCHORED"`. Characterizes the non-claim in §12; companion of NC20 | NEW_API |
| Q8a | `status` `"OK"` with `records` `[]`, and `symbol_ids`, `match_count`, `found` set consistently with empty `[DEEPSEEK V0.5.1 RV-C13]` | `CROSS_FIELD_INCONSISTENT` (Q.8) | FAIL_FIRST |
| Q8b | `status` `"NO_MATCH"` with one genuine record, and `symbol_ids`, `match_count`, `found` set consistently with one `[DEEPSEEK V0.5.1 RV-C13]` | `CROSS_FIELD_INCONSISTENT` (Q.8) | FAIL_FIRST |
| X3b | `NO_SOURCE_MATCH…` with a packet mapping `[DEEPSEEK V0.5.1 RV-C14]` | `STATUS_PACKET_INCONSISTENT` | FAIL_FIRST |
| G0a | `TRANSLATED…` whose `source` lacks `symbol_id`; query result whose record lacks `symbol_id` with `symbol_ids` `[None]` `[NEW-V0.5.2]` | `REQUIRED_FIELD_MISSING`; `TARGET_RESOLUTION_INCONSISTENT` absent | FAIL_FIRST |
| PR1 | For each row of §9.4 and for each dependency that the row's predicate names (a key that must be present, or a `passed(p)` term): one input that makes exactly that dependency false. Rows with no such dependency have no PR1 case. G-1 rows have only the missing-key case. G-5 has only the case "artifact has no `frozen_artifact_id`" `[NEW-V0.5.2][TASKLET F06]` | the failure named in the consequence table is present and the rule's own code is absent; for the G-5 case, no failure at all from G-5 and the receipt verifies | NEW_API |
| X4o | Three inputs: packet without `packet_sha256`; packet without `frozen_artifact_sha256`; translation result without `frozen_artifact_sha256` `[NEW-V0.5.3]` | respectively `PACKET_HASH_MISSING_OR_MALFORMED`; `TRANSLATION_PACKET_PROVENANCE_MISMATCH`; `ARTIFACT_HASH_COPY_MISSING`. In each, `REQUIRED_FIELD_MISSING` is absent | NEW_API |
| O3 | L2b ordering, binding passing: one altered field in `query_result.records[0]`, and the target of case R2 (a same-role record the runtime would not choose, written consistently) `[DEEPSEEK V0.5.2 D-C1][NEW-V0.5.3]` | `failures` equals exactly, in order: `RECORD_MISMATCH_WITH_ARTIFACT`, `TARGET_RESOLUTION_INCONSISTENT` | NEW_API |
| F08a | `AMBIGUOUS…` receipt with candidates `[A, B]` changed to `[A, B, A]` (exact copy of A's entry), receipt hash recomputed `[TASKLET F08][AUTHOR F08]` | `TARGET_RESOLUTION_INCONSISTENT` | FAIL_FIRST |
| F09a | Artifact with one record, not referenced by the receipt, whose stored `symbol_id` is (i) a `list`, (ii) absent, (iii) a `str` different from its key `[TASKLET F09][AUTHOR F09]` | each: exactly one entry, `ARTIFACT_SHAPE_INVALID`, detail `artifact.registry_records:ordinal=<n>`; no exception | NEW_API |
| F09b | Legacy: a `2.7.4` receipt built by V2.7.5 code over an artifact with a key/id mismatch (static fixture `key_id_mismatch.json`, F-5) `[AUTHOR F09]` | `ARTIFACT_SHAPE_INVALID`. Documents the intentional rejection of S-7 | FAIL_FIRST |
| D1 | Detail contract: one-record query with `match_count` set to 2 and `found` set to `False` `[TASKLET F01]` | `failures` equals exactly two `CROSS_FIELD_INCONSISTENT`; `failure_details` equals exactly `query_result.match_count`, `query_result.found` | NEW_API |
| L2a1 | Key `records` deleted from an otherwise valid positive query `[TASKLET F02]` | L2a emits exactly one failure for the query result: `REQUIRED_FIELD_MISSING`, detail `query_result.records`. Q.4a, Q.5, Q.6, Q.7, Q.8 emit nothing | NEW_API |
| L2a2 | Key `source` deleted from a `TRANSLATED…` result `[TASKLET F02]` | L2a emits exactly one failure for the translation result: `REQUIRED_FIELD_MISSING`, detail `translation_result.source`. X.4a and X.5 emit nothing for the source side and still run for the target side | NEW_API |
| AN1 | Well-formed `expected_artifact_sha256`, `source_frozen_artifact=None`, default mode and strict mode `[TASKLET F03]` | `SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK`; `layers.L3_BINDING == "FAIL"`; `layers.L3_ANCHOR == "NOT_EVALUATED"` | NEW_API |
| SC1 | `TRANSLATED…` result with key `translation_result.restored_state_sha256` deleted, the other two copies equal; with and without a matching expected state hash `[TASKLET F04]` | `REQUIRED_FIELD_MISSING`, detail `translation_result.restored_state_sha256`; `STATE_HASH_COPY_MISMATCH` and `EXPECTED_STATE_HASH_MISMATCH` absent | NEW_API |
| CF1 | Lone surrogate (`"\ud800"`) in a receipt field outside the packet `[TASKLET F10]` | `CANONICALIZATION_FAILED`, detail `receipt`; no exception; `layers.L1 == "FAIL"` | FAIL_FIRST (V2.7.6 raises) |
| CF2 | Lone surrogate in a packet field other than `packet_sha256`; `packet_sha256` present and well-formed (H-4) `[TASKLET F10][TASKLET V055-F04]` | two `CANONICALIZATION_FAILED`, details `receipt` then `translation_packet`; no exception | FAIL_FIRST (V2.7.6 raises) |
| CF3 | Lone surrogate in an artifact record field `[TASKLET F10]` | `CANONICALIZATION_FAILED`, detail `artifact`; `layers.L3_BINDING == "FAIL"`; no L2b failure; no exception | FAIL_FIRST (V2.7.6 raises) |
| G3a | Valid `P.source_symbol_id`, unknown `P.target_symbol_id`, forged `P.source_visible_symbol` `[TASKLET F11]` | `SYMBOL_ID_NOT_IN_ARTIFACT` and `RECORD_MISMATCH_WITH_ARTIFACT` with detail `translation_packet.source_visible_symbol`: the source lines of G-3 ran | FAIL_FIRST |
| G3b | The converse: unknown source id, valid target id, forged `P.target_visible_symbol` `[TASKLET F11]` | `SYMBOL_ID_NOT_IN_ARTIFACT` and `RECORD_MISMATCH_WITH_ARTIFACT` with detail `translation_packet.target_visible_symbol` | FAIL_FIRST |
| D2 | Detail contract for X.5: the input of case C1 (`P.source_symbol_id` set to another existing record) `[DEEPSEEK V0.5.4 FD-C1]` | the `CROSS_FIELD_INCONSISTENT` entry has detail exactly `translation_result.source.symbol_id`; no entry has a `translation_packet.*` detail with that code | NEW_API |
| LQ1 | Legacy grounding: fixture `full_translation.json` (stamp `2.7.4`, query result without `status`) with one field of `query_result.records[0]` altered and hashes recomputed; and the same alteration on a current-stamp receipt whose `status` key is deleted `[DEEPSEEK V0.5.4 L2B-C2]` | legacy: `RECORD_MISMATCH_WITH_ARTIFACT` and no `REQUIRED_FIELD_MISSING`; current: `REQUIRED_FIELD_MISSING` (detail `query_result.status`) and `RECORD_MISMATCH_WITH_ARTIFACT`. In both, G-2 ran | FAIL_FIRST |
| CF2a | The input of CF2 with `packet_sha256` (i) deleted, (ii) set to a 63-character string `[TASKLET V055-F04]` | each: `failures` contains exactly one `CANONICALIZATION_FAILED` (detail `receipt`) followed by `PACKET_HASH_MISSING_OR_MALFORMED`; no entry with detail `translation_packet`; no exception | NEW_API |
| BI1 | Integer domain, receipt: `NO_TARGET_SCRIPT_MATCH…` receipt with `translation_result.target_script_family` set to (i) `2**63`, (ii) `-2**63 - 1`, (iii) `10**4300`, (iv) a `list` holding `10**4300`; binding copies correct `[TASKLET V055-F01][AUTHOR V0.5.6]` | each: exactly one entry, `RECEIPT_SHAPE_INVALID`; `layers.L0 == "FAIL"`; detail in the scan form of §6.3; no exception | NEW_API (V2.7.6 behaviour REQUIRES_EXECUTION) |
| BI2 | Integer domain, artifact: `2**63` (i) as the value of a top-level artifact key, (ii) in a field of a record the receipt does not reference `[TASKLET V055-F01]` | each: exactly one entry, `ARTIFACT_SHAPE_INVALID`; `layers.L0 == "FAIL"`; no exception | NEW_API |
| BI3 | Integer domain, boundary control: a genuine receipt with an extra receipt field holding `[2**63 - 1, -2**63, True, False, 0]`, hashes recomputed `[NEW-V0.5.6]` | no L0 failure; verifies. `bool` values are not range-checked | NEW_API |
| BI4 | Integer domain, precedence: one receipt holding an out-of-range `int` and an unsupported type, in both scan orders `[NEW-V0.5.6]` | exactly one entry: the code of whichever the scan of §6.3 meets first (`RECEIPT_SHAPE_INVALID` or `REJECT_UNTRUSTED_OBJECT_TYPE`) | NEW_API |
| RT1 | Runtime setting: inputs BI1 (i), BI1 (iii), BI3 and a genuine receipt, each verified with `sys.set_int_max_str_digits` at 0, 640 and 4300; the harness restores the setting `[TASKLET V055-F02]` | for each input the complete result (`failures`, `failure_details`, `layers`, `assurance`, `receipt_sha256`) is equal across the three settings; the verifier does not change the setting | NEW_API |
| X3c | Packet presence: for each of the four statuses that reach X.3, the key `translation_packet` (i) deleted, (ii) set to `None`; hashes recomputed `[TASKLET V055-F03]` | `TRANSLATED…`, both variants: exactly one L2a failure for the translation result, `STATUS_PACKET_INCONSISTENT`, detail `translation_result.translation_packet`; no X.4, X.4a or X.5 entry; no exception. Other three statuses: X.3 emits nothing in either variant | NEW_API (V2.7.6 behaviour REQUIRES_EXECUTION) |
| X6a | Exact X.6 details on an `AMBIGUOUS…` result: (i) one candidate; (ii) candidate 0 without `visible_symbol`; (iii) candidate 1 without `symbol_id`; (iv) candidate 0 without both keys `[TASKLET V055-F05]` | `REQUIRED_FIELD_MISSING` with details exactly: (i) `translation_result.ambiguous_candidates`; (ii) `translation_result.ambiguous_candidates[0].visible_symbol`; (iii) `translation_result.ambiguous_candidates[1].symbol_id`; (iv) `translation_result.ambiguous_candidates[0].symbol_id` then `translation_result.ambiguous_candidates[0].visible_symbol` | NEW_API |
| D3 | Record ordinal: artifact with three records whose keys sort as `a < b < c`; record-key identity broken in (i) `a`, (ii) `b`, (iii) `a` and `c` `[TASKLET V055-F06]` | detail exactly (i) `artifact.registry_records:ordinal=0`, (ii) `artifact.registry_records:ordinal=1`, (iii) `artifact.registry_records:ordinal=0` | NEW_API |
| D4 | Scan detail: (i) a non-`str` key inserted as the second key of the receipt root; (ii) a non-`str` key inside `query_result`; (iii) a `tuple` as the first element of a list under a receipt key; (iv) a scan failure whose detail exceeds 120 characters `[TASKLET V055-F06]` | (i) detail exactly `receipt:depth=1:path=1`; (ii) `receipt:depth=2:path=<k>.<m>` with `<k>` the sorted ordinal of `query_result` and `<m>` the iteration ordinal of the key; (iii) depth 3 and a two-element path ending `.0`; (iv) the first 120 characters of the full string | NEW_API |
| D5 | Detail contract for X.5, target side: `P.target_symbol_id` set to another existing record `[TASKLET V055-F03 review note on D2]` | the `CROSS_FIELD_INCONSISTENT` entry has detail exactly `translation_result.target.symbol_id` | NEW_API |
| LQ2 | Legacy grounding of ids: fixture `full_translation.json` (stamp `2.7.4`, query result without `status`) with `query_result.symbol_ids[0]` and the matching `records[0].symbol_id` set to an id absent from the artifact, hashes recomputed `[TASKLET V055 review note on LQ1]` | `SYMBOL_ID_NOT_IN_ARTIFACT`; no `REQUIRED_FIELD_MISSING`; G-1 ran | FAIL_FIRST (V2.7.6 behaviour REQUIRES_EXECUTION) |
| S4c | Cap does not stop evaluation (named S4a in V0.5.7, renamed `[TASKLET V057-F02][AUTHOR V0.5.8]`): a receipt with at least 32 distinct failures in L2a and L2b (after P-2) and, in addition, a wrong `receipt_type` `[TASKLET V056-F04][AUTHOR V0.5.7]` | `failures` has 33 entries and the last is `FAILURES_TRUNCATED`; `WRONG_RECEIPT_TYPE` is not among them; `layers.L4 == "FAIL"`; `verified is False`. The same input with a genuine `receipt_type` gives `layers.L4 == "PASS"` | NEW_API |
| S4d | **Collector primitive control; not a receipt-level fixture** `[TASKLET V057-F01][AUTHOR V0.5.8]`. The component that applies P-2 and P-3 is given, in isolation, 32 distinct `(code, detail)` pairs followed by two pairs that repeat earlier ones. No receipt is involved: by §4.6 no conforming receipt makes the verifier emit the same pair twice, and this row does not assert that one can. If the implementation exposes no separately callable collector, this row is recorded as not applicable; it MUST NOT be replaced by an end-to-end receipt test. `NOT_APPLICABLE` is recorded separately from `PASS`, `FAIL`, `NOT_RUN` and harness errors (T-10) and MUST NOT count as an executed or passed test. The report MUST state the reason, namely that the implementation has no separately callable collector and why, and MUST disclose that the duplicate-stream behaviour was not tested against the implementation. If a collector is exposed and the test cannot run or fails, the outcome is a harness error or `FAIL`, never `NOT_APPLICABLE`. This exception waives nothing else: S4a, S4b and S4c, the rules P-2 and P-3, and every other applicable test remain mandatory `[TASKLET V058-F01][AUTHOR V0.5.9]` | exactly 32 entries retained, in first-occurrence order; `FAILURES_TRUNCATED` absent | NEW_API (primitive) |
| X6b | X.6 order: `ambiguous_candidates == [{}, {}]`; and the same with a wrong `receipt_type` and a stale `receipt_sha256` `[TASKLET V056-F02][AUTHOR V0.5.7]` | the `REQUIRED_FIELD_MISSING` entries of X.6 have details exactly, in this order: `translation_result.ambiguous_candidates[0].symbol_id`, `translation_result.ambiguous_candidates[0].visible_symbol`, `translation_result.ambiguous_candidates[1].symbol_id`, `translation_result.ambiguous_candidates[1].visible_symbol`. The test asserts the complete ordered `failures` and `failure_details` lists, not membership. Second input: `RECEIPT_HASH_MISMATCH_TAMPER_DETECTED` precedes those four and `WRONG_RECEIPT_TYPE` follows them | NEW_API |
| VS1 | Normalized surface: a hand-made artifact with two records `a < b` of the same role and family; `a` has no `visible_symbol` key. Variant (i): `b.visible_symbol` is `None`. Variant (ii): `b.visible_symbol` is `""`. For each variant a current-stamp `TRANSLATED…` receipt with target `a`, and a current-stamp `AMBIGUOUS…` receipt listing `a` and `b`; hashes recomputed. A third record of that role and family that the receipt does not mention is added in a further variant `[TASKLET V056-F01][AUTHOR V0.5.7]` | no exception in any case. (i) one distinct surface: the `TRANSLATED…` receipt has no R-1 failure; the `AMBIGUOUS…` receipt fails R-3 with `TARGET_RESOLUTION_INCONSISTENT`. (ii) two distinct surfaces: the `TRANSLATED…` receipt fails R-1 with `TARGET_RESOLUTION_INCONSISTENT`; the `AMBIGUOUS…` receipt has no R-3 failure. With the third record the `AMBIGUOUS…` receipt fails R-3 (set of ids differs) | NEW_API |
| K1 | Receipt of case R2 with `receipt_version`, `module_id` and `packet_version` rewritten to the `2.7.4` values, verified with correct artifact and state anchors `[AMENDMENT_A A-06]` | Records `RISK_PRESENT` if `verified` is `True` (then `assurance` is `ARTIFACT_AND_STATE_ANCHORED`), else `RISK_MITIGATED`. Never fails the suite (T-5) | KNOWN_RISK |
| Z1 | After every test: artifact equal to its pre-build snapshot; no exception escaped | — | all |

`[EXECUTED]` On V2.7.6 today, cases A, B, B-full, C1, C2, C3, E3 (`match_count`), M1, M2, M3, M5 (altered), M6, M7 and M8 return `verified = True`, and `receipt=None` and `translation_result=[1]` raise. They are valid fail-first cases. `[EXECUTED]` R5, R6, V1, V2 (number), Q8a, Q8b, X3b and both G0a inputs also return `verified = True` on V2.7.6, and B1 raises `AttributeError` there. V3 and ST1 have not been run against V2.7.6. E1, E2, E3 (`found`), R1 to R4, M4, M5 (removed), M9, P1 and P2 have not been run against V2.7.6; their V2.7.6 behaviour REQUIRES_EXECUTION by the implementer. By code reading, V2.7.6 checks none of these fields.

**Row inventory `[TASKLET V055-F08][NEW-V0.5.6]`.** Counted mechanically from this file by the build that produced it: the table of §11.4 has **95** data rows (header and separator excluded) and the table of §11.3 has 24 control rows. V0.5.5 had 83 rows in §11.4; the figure 84 given in the drafter's delivery message for V0.5.5 was wrong and appeared nowhere in that file. V0.5.6 adds 12 rows (CF2a, BI1–BI4, RT1, X3c, X6a, D3, D4, D5, LQ2) and changes the input column of CF2. A row is a case family, not one executable test: several rows are parameterized, and Z1 is a suite-wide invariant. None of the rows added in V0.5.6 has been run against anything.

**Row inventory for V0.5.7 `[NEW-V0.5.7]`.** Counted mechanically by the build of this file: §11.4 has **99** data rows and §11.3 has 24 control rows. Tasklet independently counted 95 and 24 in V0.5.6. V0.5.7 adds 4 rows (now S4c, S4d, X6b, VS1; the first two were named S4a and S4b in V0.5.7), extends the expectation of T4 by a reference to T-7, and changes no other row. No row has a V2.7.7 result; none of the four added rows has been run against anything.

**Row inventory and uniqueness for V0.5.8 `[TASKLET V057-F02][NEW-V0.5.8]`.** Counted mechanically by the build of this file: §11.4 has **99** data rows with **99** distinct identifiers; §11.3 has 24 control rows with 24 distinct identifiers; no identifier occurs in both tables. V0.5.7 had 99 rows and 97 distinct identifiers, because the rows added there reused `S4a` and `S4b`. V0.5.8 adds no row and removes none: it renames one row (S4c), and replaces the content and name of one row (S4d). S4a and S4b again denote only the two boundary cases of V0.5.4.

**Row inventory for V0.5.9 `[NEW-V0.5.9]`.** Counted mechanically by the build of this file: §11.4 has 99 data rows with 99 distinct identifiers, §11.3 has 24 control rows with 24 distinct identifiers, no identifier occurs in both tables, and the sequence of identifiers is identical to that of V0.5.8. Tasklet independently counted the same in V0.5.8. V0.5.9 adds, removes and renames no row; it extends the input cell of S4d.

---

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

## 13. Out of scope, still blocking any release

From `CLAUDE_AUDIT_V2_7_6`, not addressed by P0-03:

1. Source-side silent, order-dependent pick in `_resolve_source` (N-1).
2. Malformed restored state raises in the query path (N-3).
3. Canonical serialization (N-4); `symbol_id` NFC regression (N-5); `None` rendered as `"None"` (N-6); aliasing (N-7).
4. CI: `.gitkeep` files break the inventory step on upload; `sha256sum` without `--strict` (N-8).
5. Test-coverage gaps shown by mutation testing (eight surviving mutants).

V0.2 §10 referred to "P0-01/P0-02" and "P1" items. Those identifiers are not defined in any document supplied to the drafter and are not used here.

---

## 14. Consolidation and review status

This V0.5.9 is V0.5.8 (`f33c69af…04dc8733`) with the one finding of `TASKLET_V277_V058_INDEPENDENT_REVIEW_V0.1` reconciled. That review was supplied to the drafter and read in full. It reports `BYTE_VERIFICATION = PASS` on the V0.5.8 file (SHA-256, 157555 bytes, 1444 lines), that all 1444 lines and the full diff from V0.5.7 were read, an independent inventory of 99 and 24 distinct identifiers, closure by specification of V057-F01 and V057-F02, no open MAJOR finding, and verdict `NEEDS_FIX` with one MINOR process finding. The finding is correct; it concerns an applicability exception that the drafter added to S4d in V0.5.8 without reconciling it with gate 4. V0.5.9 was built from the V0.5.8 bytes by exact, asserted, single-occurrence text replacements; every V0.5.8 line not named in the change log below is preserved byte for byte. No reviewer has yet seen these exact bytes.

This is a process reconciliation. No verifier rule changes. No failure code, check, L0 condition, API parameter, result key, hash contract, fixture or test identifier is added or changed.

**Byte verification.** V0.5.3, V0.5.5, V0.5.6, V0.5.7 and V0.5.8 were byte-verified by Tasklet. V0.5.4 was not byte-verified by any reviewer. This file has not been byte-verified by anyone other than the drafter. Gate 1 of §14A is not met for V0.5.9.

**Evidence limits and exclusions.** The paragraphs "Evidence limits" and "Excluded" in the V0.5.7 status below remain in force unchanged for V0.5.9.

### Reconciliation matrix for the Tasklet V0.5.8 review

| Finding | Severity (Tasklet) | Author decision | Disposition | Where in V0.5.9 |
|---|---|---|---|---|
| V058-F01 S4d may be not applicable, while gate 4 requires NEW_API tests to pass | MINOR | ACCEPT | `NOT_APPLICABLE` defined as an outcome distinct from `PASS`, `FAIL`, `NOT_RUN` and harness error; never counted as executed or passed; reason and untested behaviour disclosed in the report; available to S4d only; gate 4 requires all applicable tests, separate enumeration of six outcome classes, and is not satisfied by a missing execution or a harness error | §11.2 T-10; §11.4 S4d; §14A gate 4 |
| V058-E01 runtime behaviour and historical compatibility unexecuted | INFORMATIONAL | — | No change; the limitation stands | §14 |

### V0.5.8 → V0.5.9 change log

| # | Change | Source | Text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | S4d: `NOT_APPLICABLE` distinguished; reason and disclosure required; nothing else waived | V058-F01, AUTHOR V0.5.9 | §11.4 S4d | none | S4d | None |
| 2 | Gate 4: all applicable tests; S4d the only permitted exception; six outcome classes reported separately; missing executions and harness errors do not satisfy the gate | V058-F01, AUTHOR V0.5.9 | §14A gate 4 | none | — | None on the verifier; tightens the release gate |
| 3 | Harness rule T-10: outcome classes | V058-F01, AUTHOR V0.5.9 | §11.2 | none | — | None |
| 4 | Inventory statement for V0.5.9 | — | §11.4 | none | — | None |
| 5 | Header, labels, supersedes table, §14 status, §14A gate 1, Appendix B, END line | — | — | none | — | None |

### Explicitly unresolved in V0.5.9

- Byte verification and content review of these V0.5.9 bytes by a reviewer other than the drafter.
- No V2.7.7 implementation exists; no row of §11.3 or §11.4 has a V2.7.7 outcome of any class.
- Whether the implementation will expose a separately callable collector (S4d).
- Every item of the V0.5.7 unresolved list below other than its first.

### Review status recorded in V0.5.8 (superseded by the paragraphs above, kept as history)

This V0.5.8 is V0.5.7 (`024b89ce…97514e3e`) with the two findings of `TASKLET_V277_V057_INDEPENDENT_REVIEW_V0.1` reconciled. That review was supplied to the drafter and read in full. It reports `BYTE_VERIFICATION = PASS` on the V0.5.7 file (SHA-256, 151075 bytes, 1400 lines), that all 1400 lines and the full diff from V0.5.6 were read, closure by specification of the surface, X.6 order, continued evaluation and profile items, and verdict `NEEDS_FIX` with one MAJOR and one MINOR finding, both in the test table. The drafter checked both against the V0.5.7 file; both are correct and both were introduced by the drafter in V0.5.7. V0.5.8 was built from the V0.5.7 bytes by exact, asserted, single-occurrence text replacements; every V0.5.7 line not named in the change log below is preserved byte for byte. No reviewer has yet seen these exact bytes.

This is a limited reconciliation. No verifier rule changes. No failure code, check, L0 condition, API parameter or result key is added or changed. `sha256_json`, `artifact_sha256`, the signed 64-bit integer domain, `normalized_surface`, the X.6 order, P-3, P-4, T-6 to T-8, the legacy rules, OQ-1…OQ-5 and residual risks R-1…R-6 are as in V0.5.7.

**Byte verification.** V0.5.3, V0.5.5, V0.5.6 and V0.5.7 were byte-verified by Tasklet. V0.5.4 was not byte-verified by any reviewer. This file has not been byte-verified by anyone other than the drafter. Gate 1 of §14A is not met for V0.5.8.

**Evidence limits and exclusions.** The two paragraphs "Evidence limits" and "Excluded" in the V0.5.7 status below remain in force unchanged for V0.5.8.

### Reconciliation matrix for the Tasklet V0.5.7 review

| Finding | Severity (Tasklet) | Author decision | Disposition | Where in V0.5.8 |
|---|---|---|---|---|
| V057-F01 the S4b row added in V0.5.7 requires duplicate emissions that §4.6 excludes | MAJOR | ACCEPT | That row is replaced by S4d, a collector primitive control: 32 distinct pairs followed by two repeats, 32 retained, no `FAILURES_TRUNCATED`. It is stated not to be a receipt-level fixture. The single-emission rule and key ownership are not weakened | §11.4 S4d |
| V057-F02 `S4a` and `S4b` each name two rows | MINOR | ACCEPT | Original S4a and S4b (V0.5.4) kept unchanged. The continued-evaluation row is renamed S4c; the collector control is S4d. Uniqueness required by T-9 and asserted by the build: 99 rows, 99 identifiers | §11.2 T-9; §11.4 S4c, S4d, inventory |

Tasklet's informational items (V057-C01 to C05, E01) record closure or non-verifiability and need no change. Its remark that "Everything else is defined without reference to the interpreter" (§10.2) must not be read as demonstrated interpreter-independent serialization is accepted: that sentence concerns which rules name the interpreter, and `json.dumps` and `str()` remain the inherited Python contracts of §2 and §3. No text is changed for it.

### V0.5.7 → V0.5.8 change log

| # | Change | Source | Text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | Continued-evaluation row renamed S4a → S4c; content unchanged | V057-F02, AUTHOR V0.5.8 | §11.4 | none | S4c | None |
| 2 | Row "Cap and P-2" renamed S4b → S4d and replaced by a collector primitive control | V057-F01, AUTHOR V0.5.8 | §11.4 | none | S4d | None |
| 3 | Harness rule T-9: unique identifiers | V057-F02 | §11.2 | none | — | None |
| 4 | Inventory and uniqueness statement; current references to the two rows updated; references to the V0.5.4 rows S4a, S4b left as they are | V057-F02 | §11.4; §14; Appendix B | none | — | None |
| 5 | Header, labels, supersedes table, §14 status, §14A gate 1, END line | — | — | none | — | None |

### Explicitly unresolved (as recorded in V0.5.8)

- Byte verification and content review of these V0.5.8 bytes by a reviewer other than the drafter.
- No V2.7.7 implementation exists; none of the 99 rows of §11.4 and none of the 24 controls has a V2.7.7 result.
- Whether the implementation will expose a separately callable collector (S4d).
- Every item of the V0.5.7 unresolved list below other than its first.

### Review status recorded in V0.5.7 (superseded by the paragraphs above, kept as history)

This V0.5.7 is V0.5.6 (`2868d783…1a575250`) with the five findings of `TASKLET_V277_V056_INDEPENDENT_REVIEW_V0.1` reconciled. That review was supplied to the drafter and read in full. It reports `BYTE_VERIFICATION = PASS` on the V0.5.6 file (SHA-256, 136562 bytes, 1328 lines), that all 1328 lines were read, closure by specification of V055-F01 and V055-F03 to V055-F08 (V055-F02 partially), and verdict `NEEDS_FIX` with 2 MAJOR, 2 MINOR and 1 INFORMATIONAL finding. The drafter checked each finding against the V0.5.6 file and found all five correct. V056-F02 was introduced by the drafter in V0.5.6; V056-F01 is inherited from V0.3. V0.5.7 was built from the V0.5.6 bytes by exact, asserted, single-occurrence text replacements; every V0.5.6 line not named in the change log below is preserved byte for byte. No reviewer has yet seen these exact bytes.

No failure code is added. No check is added. No L0 condition is added. The API and its positional parameters, the result keys, `sha256_json`, `artifact_sha256`, L0 fail-fast, the layers, `teq`, exact-type validation, the signed 64-bit integer domain, F08 candidate uniqueness, F09 record-key identity, OQ-1…OQ-5, residual risks R-1…R-6 and the legacy fixtures are unchanged. No existing test row is removed; T4 gains a reference to T-7; 4 rows are added.

**Byte verification.** V0.5.3, V0.5.5 and V0.5.6 were byte-verified by Tasklet. V0.5.4 was not byte-verified by any reviewer. This file has not been byte-verified by anyone other than the drafter. Gate 1 of §14A is not met for V0.5.7.

**Evidence limits `[TASKLET V056-F05][AUTHOR V0.5.7]`.** Every `[EXECUTED]` label in this document reports a run by the drafter on 2026-10-08. No reviewer has reproduced any of them: Tasklet states that it had no access to the V2.7.5 or V2.7.6 trees, their fixtures or the earlier reports. Until reproduced by another party they are `REPORTED_NOT_VERIFIED` for every reader other than the drafter, and historical compatibility beyond the classes named in §6.5 is NOT_VERIFIABLE from this document. No text is changed to suggest otherwise.

**Excluded.** Any Google-authored summary or separate proposal with `ERR_*` codes, wrapper schemas, a `presentation_time_action` wrapper or new API fields is NON_NORMATIVE and not incorporated. The NOVA Q / EIT / TIE conceptual research (Zero Phase, PRESENT_TIME, energy and information transformations, resonance, and related candidate definitions) is a separate body of work; nothing from it is part of this verifier specification, and this document makes no claim about it.

### Reconciliation matrix for the Tasklet V0.5.6 review

| Finding | Severity (Tasklet) | Disposition | Where in V0.5.7 | Tests |
|---|---|---|---|---|
| V056-F01 missing candidate `visible_symbol` has no rule | MAJOR | Fixed: `normalized_surface(r) = nfc(r.get("visible_symbol"))`, the absent-key value being `None` as in G-3. This is what V2.7.6 computes (`unicode_normalization.py:65`, CODE_VERIFIED). No structural requirement added | §3.4; §9.3 R-1, R-3 | VS1 |
| V056-F02 P-1 and X.6 order differ | MAJOR | Fixed: P-1 yields to a per-instance order assigned by a check; X.6 is index first, then `symbol_id`, then `visible_symbol` | §5.2 P-1 | X6b |
| V056-F03 P-4 scope against the runtime non-claim | MINOR | Fixed: P-4 scoped to one conformance profile; profile defined; reports record it. No cross-profile claim | §5.2 P-4; §10.2; §11.2 T-8; §12 | — (report content) |
| V056-F04 harness gaps | MINOR | Fixed for the two items named by the author and for the hash-feasibility note: arming after construction; evaluation continues past the cap. Not adopted: pairwise missing / present-invalid id combinations; full ordered-list assertions in every deterministic test (done for X6b only) | §5.2 P-3; §11.2 T-6, T-7; §11.4 T4 | S4c, S4d (named S4a, S4b in V0.5.7), T4 |
| V056-F05 historical compatibility not verifiable | INFORMATIONAL | No rule changed. Limitation stated in §14; unresolved list updated | §14 | — |

Tasklet's remark that X6a's one-candidate case can also produce an R-3 failure is correct and needs no change: X6a requires its code and does not forbid others.

### V0.5.6 → V0.5.7 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | `normalized_surface` defined; R-1 and R-3 refer to it | V056-F01, AUTHOR V0.5.7 | §3.4; §9.3 | `TARGET_RESOLUTION_INCONSISTENT` (existing) | VS1 | None for receipts of any builder: same computation as V2.7.6; legacy `2.7.4` rules untouched. Defines a case that was undefined |
| 2 | P-1 admits a per-instance order; X.6 order stated there | V056-F02, AUTHOR V0.5.7 | §5.2 P-1 | none | X6b | Order of entries only |
| 3 | P-3: collection stops, evaluation does not | V056-F04, AUTHOR V0.5.7 | §5.2 P-3 | none | S4c, S4d (named S4a, S4b in V0.5.7) | None; §5.1 already required all phases to run |
| 4 | P-4 scoped to a conformance profile; profile defined | V056-F03, AUTHOR V0.5.7 | §5.2 P-4; §10.2; §12 | none | T-8 | Narrows a claim; no receipt rule changes |
| 5 | Harness rules T-6 (hash feasibility), T-7 (arming), T-8 (profile record); T4 refers to T-7 | V056-F04, Tasklet §6 | §11.2; §11.4 T4 | none | T4, CF1–CF3, BI1, BI2 | None |
| 6 | Row inventory for V0.5.7 | — | §11.4 | none | — | None |
| 7 | Evidence limits stated; header, labels, supersedes table, §14, §14A gate 1, Appendix B, END line | V056-F05 | §14 | none | — | None |

### Explicitly unresolved (as recorded in V0.5.7)

- Byte verification and content review of these V0.5.7 bytes by a reviewer other than the drafter.
- Everything added in V0.5.7 is text only. No V2.7.7 implementation exists; none of the 99 rows of §11.4 and none of the 24 controls has a V2.7.7 result.
- No `[EXECUTED]` statement has been reproduced by a second party (V056-F05).
- Cross-profile behaviour of `nfc`, `.upper()` and `datetime.fromisoformat` (§10.2).
- V2.7.5 and V2.7.6 behaviour on out-of-range integers and on an absent packet key (BI1, X3c, LQ2 carry REQUIRES_EXECUTION).
- Tasklet test-design suggestions not adopted: pairwise missing / present-invalid id combinations; full ordered-list assertions in every deterministic-output test.
- Residual risks R-1…R-6 and the out-of-scope items of §13.
- Whether any legacy receipt class other than those named in §6.5 is newly rejected.

### Review status recorded in V0.5.6 (superseded by the paragraphs above, kept as history)

This V0.5.6 is V0.5.5 (`b35a0626…a69a593f`) with the eight findings of `TASKLET_V277_V055_INDEPENDENT_REVIEW_V0.1` reconciled. That review was supplied to the drafter and read in full. It reports `BYTE_VERIFICATION = PASS` on the V0.5.5 file (SHA-256, 115814 bytes, 1233 lines), that all 1233 lines were read, and verdict `NEEDS_FIX` with 5 MAJOR and 3 MINOR findings. The drafter checked each finding against the V0.5.5 file and found all eight correct. V0.5.6 was built from the V0.5.5 bytes by exact, asserted, single-occurrence text replacements; every V0.5.5 line not named in the change log below is preserved byte for byte. No reviewer has yet seen these exact bytes.

No failure code is added. One L0 condition is added: the integer domain of §6.1, reported with the existing codes `RECEIPT_SHAPE_INVALID` and `ARTIFACT_SHAPE_INVALID` `[AUTHOR V0.5.6]`. The API and its positional parameters, `sha256_json`, `artifact_sha256`, L0 fail-fast, the layers, the L2a/L2b separation, `teq`, F08 candidate uniqueness, F09 record-key identity, OQ-1…OQ-5 and residual risks R-1…R-6 are unchanged. No existing test row is removed; the input column of CF2 is made precise; 12 rows are added.

**Byte verification.** V0.5.3 and V0.5.5 were byte-verified by Tasklet. V0.5.4 was not byte-verified by any reviewer. This file has not been byte-verified by anyone other than the drafter. Gate 1 of §14A is not met for V0.5.6.

**Excluded.** Any Google-authored summary or separate proposal with `ERR_*` codes or wrapper schemas, including the Google summary of a "V0.5.6", is NON_NORMATIVE and not incorporated.

### Reconciliation matrix for the Tasklet V0.5.5 review

| Finding | Severity (Tasklet) | Disposition | Where in V0.5.6 | Tests |
|---|---|---|---|---|
| V055-F01 exact built-ins do not make derivations exception-free | MAJOR | Fixed by Option A `[AUTHOR V0.5.6]`: 64-bit integer domain at L0, checked without string conversion; `bool` excluded | §2.3 H-6; §6.1; §6.2 rows 0.3, 0.9; §6.3; §6.4 S-4; §6.5; §9.3 | BI1–BI4 |
| V055-F02 runtime conversion policy changes failures | MAJOR | Fixed for the integer-conversion limit by the same domain. The Unicode-version dependency is disclosed as a non-claim, not removed | §2.3 H-6; §12 | RT1 |
| V055-F03 missing packet has no operand semantics | MAJOR | Fixed: `packet_present` / `packet_is_mapping`; X.3 is a presence predicate; code and skip rule unchanged | §9.1 X.3 and "Packet presence"; §9.1a; §4.6 | X3c |
| V055-F04 H-5 overstates the two-entry consequence | MINOR | Fixed: two entries only when 1b.1 passed and both hash operations raised | §2.3 H-5; §11.4 CF2 | CF2, CF2a |
| V055-F05 ellipsis in the X.6 detail | MAJOR | Fixed: full paths, field order, zero-based index | §4.6 | X6a |
| V055-F06 mapping ordinals and rejected-key depth | MAJOR | Fixed: zero-based, exact number format, depth and path for a rejected key, truncation rule, examples. The key-depth convention (depth of the containing `dict`) is a choice made here, as Tasklet proposed | §4.6 row 0.10; §6.3 | D3, D4 |
| V055-F07 normative authority against informative labels | MINOR | Fixed: three classes of authority; no clause changes meaning | §0.3 | — (documentation) |
| V055-F08 83 rows, not 84 | MINOR | Confirmed. The file never said 84; the drafter's delivery message did, wrongly. Inventory now stated and counted by the build | §11.4 "Row inventory" | — |

Tasklet's review notes on D2 and LQ1 are met by the new rows D5 and LQ2.

### V0.5.5 → V0.5.6 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | Integer domain `-2**63 … 2**63 - 1` for every exact `int`; `bool` excluded; no string conversion | V055-F01, AUTHOR V0.5.6 | §6.1; §6.2 rows 0.3, 0.9; §6.3 | `RECEIPT_SHAPE_INVALID`, `ARTIFACT_SHAPE_INVALID` (existing) | BI1–BI4 | New rejection of out-of-range integers; none known from any builder (§6.5) |
| 2 | Runtime independence of the integer-conversion limit stated; verifier must not touch the setting | V055-F02 | §2.3 H-6; §12 | none | RT1 | None |
| 3 | S-4 and the §9.3 "cannot raise" statements tied to the integer domain | V055-F01 | §6.4 S-4; §9.3 | none | BI1 | None |
| 4 | Packet presence defined; X.3 runs on an absent packet | V055-F03 | §9.1; §9.1a; §4.6 | `STATUS_PACKET_INCONSISTENT` (existing) | X3c | A `TRANSLATED…` result with no packet key is rejected by X.3; V0.5.5 left this case undefined |
| 5 | Two canonicalization entries made conditional | V055-F04 | §2.3 H-5 | `CANONICALIZATION_FAILED`, `PACKET_HASH_MISSING_OR_MALFORMED` (existing) | CF2, CF2a | None |
| 6 | X.6 detail paths written in full | V055-F05 | §4.6 | `REQUIRED_FIELD_MISSING` (existing) | X6a | Diagnostic only |
| 7 | Zero-based ordinals, number format, rejected-key depth and path, truncation | V055-F06 | §4.6; §6.3 | none | D3, D4 | Diagnostic only |
| 8 | Authority of sections classified | V055-F07 | §0.3 | none | — | None |
| 9 | Row inventory stated and counted | V055-F08 | §11.4 | none | — | None |
| 10 | Target-side X.5 detail test; legacy unknown-id test | Tasklet notes on D2, LQ1 | §11.4 | existing | D5, LQ2 | None |
| 11 | Header, labels, supersedes table, §14, §14A gate 1, Appendix B, END line | — | — | none | — | None |

### Explicitly unresolved (as recorded in V0.5.6)

- Byte verification and content review of these V0.5.6 bytes by a reviewer other than the drafter.
- Everything added in V0.5.6 is text only. No V2.7.7 implementation exists; none of the 95 rows of §11.4 has a V2.7.7 result.
- V2.7.5 and V2.7.6 behaviour on out-of-range integers and on an absent packet key was not run (BI1, X3c, LQ2 carry REQUIRES_EXECUTION).
- Unicode-version dependence of `nfc` and `.upper()` (§12, Runtime profile).
- Tasklet §7 test-design suggestions not adopted in this file and left for the author: an explicit arming step for hostile keys in T4; tests at the failure-cap boundary and of layer states surviving truncation; pairwise missing / present-invalid id combinations; full ordered-list assertions in every deterministic-output test.
- Residual risks R-1…R-6 and the out-of-scope items of §13.
- Whether any legacy receipt class other than the one in S-7 is newly rejected.

### Review status recorded in V0.5.5 (superseded by the paragraphs above, kept as history)

This V0.5.5 is V0.5.4 (`3caebc00…482fdbba`) with the eleven corrections of `DEEPSEEK_V277_V054_INDEPENDENT_ADVERSARIAL_REVIEW_V0.1` reconciled. That review was supplied to the drafter and read in full. It reports `BYTE_VERIFICATION = NOT_VERIFIABLE` (pasted text) and verdict `ACCEPT_WITH_CORRECTIONS`. Unlike the review of V0.5.2, its descriptions of the clauses match the V0.5.4 file. All other V0.5.4 text is preserved byte for byte. No reviewer has yet approved these exact bytes.

No failure code is added. No check is added. The API, the hash functions, L0 fail-fast, the L2a/L2b separation, the author decisions and residual risks R-1…R-6 are unchanged. No existing test row is changed or removed; two rows are added (D2, LQ1).

**Byte verification.** V0.5.3 was byte-verified by Tasklet. V0.5.4 and this file have not been byte-verified by any reviewer. Gate 1 of §14A is not met. (Since then Tasklet byte-verified V0.5.5.)

**Excluded.** Any Google-authored summary or separate proposal with `ERR_*` codes or wrapper schemas is NON_NORMATIVE and not incorporated.

### Reconciliation matrix for the DeepSeek V0.5.4 review

| ID | Requested | Clause in V0.5.4 | Disposition | Where in V0.5.5 |
|---|---|---|---|---|
| H5-C2 | H-5 entries count toward the cap | §2.3 H-5, §5.2 P-3 | Adopted | §2.3 H-5 |
| H5-C3 | H-5 does not apply to a `None` artifact | §2.3 H-5, §8.1 B.1 | Adopted, limited to the artifact case; the receipt and packet cases still apply | §2.3 H-5 |
| H5-C4 | Non-claim for `CANONICALIZATION_FAILED` | §12 | Adopted | §12 |
| FD-C1 | Packet-side details for X.4a / X.5 | §4.6 | Adopted in a deterministic form: one fixed detail per side (the record side). An "or" between record and packet paths would have reintroduced the ambiguity §4.6 exists to remove | §4.6 |
| L2B-C1 | G-1 does not depend on `passed` | §9.4 | Adopted, reworded. The proposed sentence required the value to be a record key, which would suppress G-1's own failure | §9.4 |
| L2B-C2 | Add Q.1 to the "key is absent" consequence row | §9.4 | Not adopted as written; clarified instead. A missing query `status` does not close `QR_GATE`, so it is not a reason any L2b rule does not run. Adding it would have implied that legacy `2.7.4` query results are not grounded | §9.4 |
| F09-C1 | Soften "only legacy receipt class" | §6.4 S-7 | Adopted | §6.4 S-7 |
| RG-C1 | Reviewer states which sections were read | §14A gate 1 | Adopted | §14A |
| E-C2 | One failure for a key shared by X.4 and §9.4 | §9.4, §5.2 P-7 | Already true through the predicates; made explicit with an owner table | §9.4 |
| V-C2 | §6.5 covers the H-5 behaviour change | §6.5 | Adopted; the record-key identity rejection is cross-referenced there as well | §6.5 |
| L-C1 | Fixture-integrity test covers `key_id_mismatch.json` | §11.1 F-5 | Already present: the test is stated "for every fixture", and the exception in the preceding sentence concerns record-key identity only. No change | — |

One statement in the review does not match the specification and led to no change: its item L2A-11 says that for `query_result == {}` check Q.1 runs. §9.1 applies the Q checks only to a non-empty query result. A sentence in §9.1a now says so directly.

### V0.5.4 → V0.5.5 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | H-5: entries are subject to P-2 and P-3; artifact case cannot occur with a `None` artifact | DEEPSEEK H5-C2, H5-C3 | §2.3 H-5 | `CANONICALIZATION_FAILED` | CF1–CF3, AN1 (existing) | None |
| 2 | Non-claim for canonicalization failure | DEEPSEEK H5-C4 | §12 | none | — | None |
| 3 | X.4a and X.5 detail rows split; X.5 detail fixed to the record side | DEEPSEEK FD-C1 | §4.6 | `REQUIRED_FIELD_MISSING`, `CROSS_FIELD_INCONSISTENT` | D2 | None; the detail string was already this one |
| 4 | G-1 independence from `passed` stated | DEEPSEEK L2B-C1 | §9.4 | `SYMBOL_ID_NOT_IN_ARTIFACT` | P2 (existing) | None |
| 5 | Missing query `status` never closes `QR_GATE` | DEEPSEEK L2B-C2 | §9.4 | none | LQ1 | None. Confirms that `2.7.4` query results are grounded |
| 6 | Owner table for keys required by §9.4 | DEEPSEEK E-C2 | §9.4 | `REQUIRED_FIELD_MISSING` | P1, PR1, X4o (existing) | None |
| 7 | "Only legacy class" claim limited to executed checks | DEEPSEEK F09-C1 | §6.4 S-7 | none | — | None |
| 8 | Compatibility section lists the H-5 and record-key identity changes | DEEPSEEK V-C2 | §6.5 | as before | CF1–CF3, F09b (existing) | None; documentation of V0.5.4 behaviour |
| 9 | Reviewer must state which sections were read | DEEPSEEK RG-C1 | §14A | — | — | None |
| 10 | Empty sub-object runs no L2a check | NEW-V0.5.5 | §9.1a | none | NC12 (existing) | None |
| 11 | Labels, supersession table, review status | drafter | header, §0.4, §14 | — | — | None |

### Explicitly unresolved (as recorded in V0.5.5)

- Byte verification of V0.5.4 and V0.5.5 by a reviewer other than the drafter.
- §4.6, §9.1a, H-5 and the owner table are text only; nothing has exercised them.
- Residual risks R-1…R-6 and the out-of-scope items of §13.
- Whether any legacy receipt class other than the one in S-7 is newly rejected (F09-C1).

### F01–F12 reconciliation matrix

| Finding | Class (Tasklet) | Disposition | Where | Tests |
|---|---|---|---|---|
| F01 unspecified details defeat determinism | AMBIGUITY | Fixed: one exact detail string per check | §4.2, §4.6 | D1 |
| F02 L2a has no missing-operand policy | AMBIGUITY | Fixed: exact predicates; nothing is substituted for a missing operand | §9.1a | L2a1, L2a2 |
| F03 anchor without artifact has no layer value | AMBIGUITY | Fixed: `NOT_EVALUATED` | §5.3 | AN1 |
| F04 absent translated state copies | AMBIGUITY | Fixed: a copy is applicable only when its key is present | §8.3 | SC1 |
| F05 T1 contradicts fail-fast for root objects | CONTRADICTION | Fixed: T1 limited to values inside the input; roots moved to T1r with the shape codes | §11.4 | T1, T1r |
| F06 PR1 unsatisfiable; G-5 skip without failure | CONTRADICTION | Fixed: PR1 limited to applicable dependencies; the G-5 skip named as the one permitted exception | §9.4, §11.4 | PR1 |
| F07 ST1 does not specify the packet rewrite | AMBIGUITY | Fixed: ST1, R1, R2 state the consistent rewrite | §11.4 | ST1, R1, R2 |
| F08 duplicate ambiguity entries accepted | FALSE_POSITIVE_PATH | Fixed by author decision: candidate ids pairwise distinct. Not applied to query results (runtime evidence) | §9.3 R-3 | F08a, NC23 |
| F09 candidate-record id domain incomplete | AMBIGUITY | Fixed by author decision: record-key identity at L0 | §6.2 row 0.10, §6.4 S-7 | F09a, F09b |
| F10 canonicalization failure untested | MISSING_TEST | Fixed: consequences defined and three tests added | §2.3 H-5 | CF1, CF2, CF3 |
| F11 partial G-3 execution untested | MISSING_TEST | Fixed: two complementary positive cases | §11.4 | G3a, G3b |
| F12 deduplication at the cap boundary untested | MISSING_TEST | Fixed: counting rule stated; boundary cases added | §5.2 P-3 | S4a, S4b |

### V0.5.3 → V0.5.4 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | Exact detail string for every check | TASKLET F01 | §4.2, §4.6 | all (details only) | D1 | None on `verified`. Fixes the content of `failure_details` and the effect of P-2 |
| 2 | L2a execution predicates | TASKLET F02 | §9.1a | none new | L2a1, L2a2 | None for genuine receipts |
| 3 | `L3_ANCHOR` and `L3_STATE` layer values completed | TASKLET F03 | §5.3 | none | AN1 | None |
| 4 | State-hash copy applicability | TASKLET F04 | §8.3 | `REQUIRED_FIELD_MISSING` via X.4 | SC1 | None for builder output |
| 5 | Record-key identity for every artifact record | TASKLET F09; AUTHOR F09; EXECUTED | §6.2 row 0.10, §6.4 S-7 | `ARTIFACT_SHAPE_INVALID` (existing in this spec) | F09a, F09b | **Intentional rejection:** `2.7.4` receipts over artifacts with a key/id mismatch, which V2.7.5 could produce and V2.7.6 verified. No artifact in the existing suite, demo or legacy evidence is affected |
| 6 | Candidate ids pairwise distinct in R-3; not applied to query results | TASKLET F08; AUTHOR F08; EXECUTED | §9.3 R-3 | `TARGET_RESOLUTION_INCONSISTENT` | F08a, NC23 | None for genuine receipts: the runtime never repeats a candidate |
| 7 | Consequences of a hashing failure | TASKLET F10; EXECUTED | §2.3 H-5 | `CANONICALIZATION_FAILED` (existing in this spec) | CF1, CF2, CF3 | V2.7.6 raises `UnicodeEncodeError`; V2.7.7 returns a structured failure |
| 8 | Failure-cap counting after deduplication | TASKLET F12 | §5.2 P-3 | `FAILURES_TRUNCATED` | S4a, S4b | None |
| 9 | §9.4 consequence statement corrected for G-1 and G-5 | TASKLET F06 | §9.4 | none | PR1 | None |
| 10 | Test rows corrected or made exact | TASKLET F05, F06, F07 | §11.4 T1, T1r, PR1, ST1, R1, R2 | as listed | same | None |
| 11 | Partial G-3 execution tests | TASKLET F11 | §11.4 | `RECORD_MISMATCH_WITH_ARTIFACT` | G3a, G3b | None |
| 12 | Legacy fixture set: identity requirement and one rejection fixture | AUTHOR F09 | §11.1 F-5 | — | F09b, fixture-integrity test | None |
| 13 | Evidence statement corrected for R-3 | drafter | Appendix B | — | — | None |
| 14 | Labels, supersession table, review status | drafter | header, §0.4, §14, §14A | — | — | None |

### V0.5.2 → V0.5.3 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | Key ownership: three hash keys are reported only by the layer that owns them, not also by X.4 | drafter, found while checking DeepSeek E-C2 | §9.1 "Key ownership" | existing: `PACKET_HASH_MISSING_OR_MALFORMED`, `TRANSLATION_PACKET_PROVENANCE_MISMATCH`, `ARTIFACT_HASH_COPY_MISSING` | X4o | None on `verified`. Removes an ambiguity in the content of `failures` (P-4): V0.5.2 could be read as emitting `REQUIRED_FIELD_MISSING` as well |
| 2 | Statement that Q.4a and X.4a add requirements and that no stamp exemption exists beyond Q.1 and X.1 | drafter, in response to the misreading above | §9.1 | none | G0a (unchanged) | None; no rule changes |
| 3 | Explicit order of checks inside Phase 3 | DEEPSEEK V0.5.2 D-C1, reworded | §5.2 P-7 | none | O3, O1, O2 | None; restates P-1 |
| 4 | Self-translation cross-reference in §9.4 | DEEPSEEK V0.5.2 E-C3 | §9.4 | none | NC16, NC17 | None |
| 5 | NC22 stamp stated; legacy companion recorded as executed and already covered by a fixture | DEEPSEEK V0.5.2 N-C1; EXECUTED | §11.3 NC22 | none | NC22, NC9 | None |
| 6 | Labels, supersession table and review status updated | drafter | header, §0.4, §14, §14A | — | — | None |

### V0.5.1 → V0.5.2 change log

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | V.1 evaluated before Q.1; both reported | DEEPSEEK V-C1 | §9.1 | `REQUIRED_FIELD_MISSING` | V1, V3 | None |
| 2 | Compatibility breaks for absent `receipt_version` and `boundary: None` stated in the compatibility section | DEEPSEEK V-C2, BN-C1 | §6.5 | as before | V1, B1 | None; documentation of V0.5.1 behaviour |
| 3 | Non-claim for version stamps | DEEPSEEK U-C1 | §12 | none | V4, NC20 | None |
| 4 | Unlisted-stamp characterization case | DEEPSEEK U-C2 | §11.4 V4 | none; absence of `POLICY_*` asserted | V4 | None |
| 5 | Exact `failure_details` for argument checks | DEEPSEEK S-C1 | §6.4 S-5 | `STRICT_MODE_NOT_BOOL`, `EXPECTED_ANCHOR_MALFORMED` | SM1, SM2, T6 | None |
| 6 | Hostile-object tests use flags; flags cleared after construction | DEEPSEEK L0S-C1; drafter (reset) | §11.4 T4 | `REJECT_UNTRUSTED_OBJECT_TYPE` | T4 | None |
| 7 | Exact execution predicates for every L2b rule; code list withdrawn | DEEPSEEK TR-C1, reformulated; NEW-V0.5.2 | §9.3, §9.4 | none new | PR1 | None for genuine receipts. Fixes the order and content of `failures` |
| 8 | Presence of `symbol_id` in full records checked in L2a | NEW-V0.5.2; EXECUTED | §9.1 Q.4a, X.4a | `REQUIRED_FIELD_MISSING` | G0a | None for builder output: records come from artifacts that passed the integrity gate, which requires `symbol_id`. Such receipts were already rejected in V0.5.1 through `CROSS_FIELD_INCONSISTENT` or `SYMBOL_ID_NOT_IN_ARTIFACT`; they now also carry the specific code |
| 9 | Requested family is not recorded; cross-family receipt must verify; DeepSeek ST-C1 not adopted | EXECUTED; NEW-V0.5.2 | §9.3 | none (control) | NC22 | None. Prevents a regression that ST2 would have introduced |
| 10 | Legacy control for `NO_TARGET…` with `None` family | DEEPSEEK RV-C1; EXECUTED | §11.3 | none (control) | NC21 | None |
| 11 | R-5 states both `assurance` outcomes | DEEPSEEK RV-C2 | §12 R-5 | none | K1 | None |
| 12 | `strict_mode` custom object with `__bool__` | DEEPSEEK RV-C3 | §11.4 SM1 | `STRICT_MODE_NOT_BOOL` | SM1 | None |
| 13 | T2 and T3 placements enumerated | DEEPSEEK RV-C9, RV-C11 | §11.4 | as before | T2, T3 | None |
| 14 | Status-versus-records and status-versus-packet cases | DEEPSEEK RV-C13, RV-C14; EXECUTED | §11.4 | `CROSS_FIELD_INCONSISTENT`, `STATUS_PACKET_INCONSISTENT` | Q8a, Q8b, X3b | None; rules existed, tests were missing |
| 15 | Legacy controls use static JSON fixtures generated once from `2b7dd62` | DEEPSEEK NCN-C1, NCN-C2; AUTHOR | §11.1 F-5 | none | NC9, NC18, NC19, NC21, fixture-integrity test | None. Removes a dependency on V2.7.5 code at test time |
| 16 | Labels, supersession table and review status updated | drafter | header, §0.4, §14, §14A | — | — | None |

### V0.5 → V0.5.1 change log

Every change: source, normative text location, failure code, test, compatibility impact.

| # | Change | Source | Normative text | Failure code | Tests | Compatibility impact |
|---|---|---|---|---|---|---|
| 1 | Missing or non-`str` `receipt_version` is a controlled rejection; current rules apply | AUTHOR-TASK item 4; EXECUTED | §3.1 "Stamp resolution"; §9.1 V.1 | `REQUIRED_FIELD_MISSING` (existing in this spec) | V1, V2, NC20 | None for builder output: both builders always write the key. A hand-made receipt without it verified on V2.7.6 and will not on V2.7.7 |
| 2 | Unlisted stamp string: current rules in default mode | NEW-V0.5.1 | §3.1 | none in default mode; `POLICY_RECEIPT_VERSION_NOT_ALLOWED` in strict mode | NC20 | None |
| 3 | `boundary: None` stays invalid, as a controlled L0 rejection; absent key and `{}` unchanged | AUTHOR-TASK item 5; EXECUTED | §6.4 S-6; §10.1 | `RECEIPT_SHAPE_INVALID`; four `BOUNDARY_VIOLATION:<key>` | B1, B2 | `None` raised `AttributeError` before; now a structured failure. Absent and `{}` identical to V2.7.6 |
| 4 | `strict_mode` checked first, with its own code; anchors next, in fixed order | AUTHOR-TASK item 6 | §6.2 rows 0.1a–0.1c; §6.4 S-5 | `STRICT_MODE_NOT_BOOL` (new); `EXPECTED_ANCHOR_MALFORMED` | SM1, SM2, T6 | New parameter, so no existing caller is affected. Callers passing `0`/`1` are rejected by design |
| 5 | Self-translation confirmed valid from runtime evidence; rule text added | AUTHOR-TASK item 7; EXECUTED | §9.3 "Self-translation" | none (a control); `TARGET_RESOLUTION_INCONSISTENT` for the forged variant | NC16, NC17, ST1 | None. R-1 already accepted these; the text now forbids a future rule that would not |
| 6 | Legacy and adversarial controls added | AUTHOR-TASK item 8; EXECUTED | §11.3, §11.4 | as listed per row | NC18, NC19, V3 | None |
| 7 | Labels and supersession table updated; status of the two unseen reviews recorded | drafter | header, §0.4, §14 | — | — | None |

### V0.4 → V0.5 change log

| # | Change | Section | Origin |
|---|---|---|---|
| 1 | L0 container checks restored in full; the reference to V0.3 removed; the file is self-contained | §6.2 rows 0.4–0.7 | CLAUDE F-1 |
| 2 | Every value of `registry_records` must be exactly `dict`; S-3 restored | §6.2 row 0.10, §6.4 | CLAUDE F-2 |
| 3 | "Structurally usable" prerequisite removed. Prerequisites reduced to G-1 and key presence; no-silent-skip invariant added | §9.3 | CLAUDE F-3 |
| 4 | Artifact scan moved before any key lookup on the artifact; rows renumbered 0.1–0.10; scan pseudocode added | §6.1–§6.3 | NEW-V0.5, EXECUTED |
| 5 | Depth origin defined (root is depth 1); `expected_*` must be exactly `str`; fixed `failure_details` form for scan failures | §6.2, §6.3 | CLAUDE m-7, m-8, AA-4 |
| 6 | Rules S-1…S-5 restated as a list | §6.4 | CLAUDE F-1 |
| 7 | Header corrected; superseded files listed by hash | header | CLAUDE m-1 |
| 8 | Missing origin labels defined | §0.4 | CLAUDE m-2 |
| 9 | Docstring requirement stated once, with the verbatim text | §4.5 | CLAUDE m-11 |
| 10 | General `teq` rule added as P-6 | §5.2 | CLAUDE m-9, AMENDMENT_A A-04 |
| 11 | `KNOWN_RISK` handled inside the test suite, no CI workflow change; labels merged into T-4, T-5 | §11.2 | CLAUDE m-6 |
| 12 | Prose test paragraphs replaced by table rows R5, R6, P1, P2, T1–T8, O1, O2, K1; ordering test split in two | §11.4 | CLAUDE m-5, m-10 |
| 13 | Controls NC14, NC15 added | §11.3 | CLAUDE F-3, EXECUTED |
| 14 | Release gates refer to V0.5; resolved open questions removed from the gates | §14A | CLAUDE m-3 |
| 15 | Evidence statement extended and scoped | Appendix B | CLAUDE m-4 |
| 16 | DeepSeek V0.4 review recorded as not received | §14 | CLAUDE m-12 |

### V0.3 → V0.4 change log (from V0.4, unchanged)

1. Consolidated A-01 and its rule prerequisites, G-1 typed ID checks, and exact R-test codes.
2. Clarified L3-before-L2a and L2a-before-L2b deterministic failure ordering.
3. Replaced L0 container-only validation with exact-type guarded traversal and explicit precedence, shape/depth/cycle codes.
4. Restricted `failure_details` to fixed roots, depths, and ordinal indices.
5. Applied `teq` to expected state-hash and packet-version comparisons.
6. Added trusted-anchor docstring disclaimer without claiming authentication.
7. Kept R-5 OPEN / ACCEPTED_RISK and defined non-gating characterization in CI. (Superseded by change 11 above.)
8. Added NC13 and V2.7.7 builder dependency.
9. Added adversarial tests for custom methods, subclasses, non-string keys, and precedence.
10. Preserved existing canonical hash contracts, version stamps, baseline and governance boundaries.

## 14A. Release gates

1. Independent review of this V0.5.9 text by a reviewer other than the drafter who has received the file itself, not pasted text, and who quotes clause text in the review so that the reviewed content can be matched to the file; and a SHA-256 computed over the file by a party other than the drafter. The review MUST state which sections were read in full and which were not, and MUST NOT claim to have reviewed a section it could not read. `[DEEPSEEK V0.5.4 RG-C1]`
2. Separate author authorization for implementation.
3. Implementation on an isolated candidate; V2.7.5 untouched.
4. All CONTROL tests pass on V2.7.6 and V2.7.7; all FAIL_FIRST tests fail on V2.7.6 and pass on V2.7.7; all applicable NEW_API and CONTROL_FOR_V277 tests pass on V2.7.7; KNOWN_RISK outcomes recorded; the existing 33 tests pass with the fixture change of §11.1. Every row is applicable except that S4d alone MAY be recorded as `NOT_APPLICABLE` under the condition stated in its row; that outcome is a disclosed applicability exception, not an executed pass. The test report MUST enumerate separately the executed passes, the failures, the not-run cases, the non-applicable cases, the known-risk characterizations and the harness errors (§11.2 T-10). A required execution that is missing, and a harness error, do not satisfy this gate. `[TASKLET V058-F01][AUTHOR V0.5.9][NEW-V0.5.9]`
5. Independent reproduction.
6. Items in §13 closed separately.

Passing tests does not authorize publication or formal freeze.

---

## 15. Author decisions and reviewer questions

`[AUTHOR_APPROVED]` OQ-1 KEEP R-1–R-3; OQ-2 ACCEPT R-5 as OPEN risk; OQ-3 depth limit 32 / failure cap 32; OQ-4 KEEP `assurance`; OQ-5 retain existing nonhex 64-character receipt-hash mismatch behavior. These are specification decisions only. Independent reviewers MUST assess the consolidated clauses, particularly L0 exact types and precedence, R-rule prerequisites, the non-gating risk characterization, and legacy compatibility.

### Historical V0.3 question record (now author-resolved)

| # | Question | Drafter's position |
|---|---|---|
| OQ-1 | Is §9.3 (target resolution) in scope for V2.7.7, or should it move to the version that fixes source-side ambiguity? | Keep. It is cheap, deterministic, and closes the wrong-pair forgery |
| OQ-2 | Accept residual risk R-5 (stamp downgrade) for V2.7.7? | Accept and document |
| OQ-3 | Are the depth limit (32) and failure cap (32) acceptable? | Yes; both are arbitrary and can be raised |
| OQ-4 | Is `assurance` wanted, or is `layers` enough? | Keep; it is one derived field |
| OQ-5 | Should a non-hex 64-character `receipt_sha256` remain `RECEIPT_HASH_MISMATCH…` as today (1a.1 checks length only)? | Yes, for compatibility |

---

## Appendix A. Change log V0.2 → V0.3

| # | Change | Section | Origin |
|---|---|---|---|
| 1 | Canonical hash functions named and reproduced; guarded hashing rule | §2 | DEEPSEEK, EXECUTED, CLAUDE |
| 2 | Typed equality `teq` replaces undefined "exact equality" | §3.3 | CLAUDE (K-06), AUTHOR |
| 3 | "Positive claim" predicate defined | §3.5 | DEEPSEEK |
| 4 | Result gains `failure_details` and `assurance`; caller obligation stated | §4 | CLAUDE (K-05), DEEPSEEK |
| 5 | Failure precedence made deterministic (P-1…P-5); layer values defined | §5 | CLAUDE (K-01), DEEPSEEK |
| 6 | L0 limited to container types; artifact `None` keeps its existing code; `EXPECTED_ANCHOR_MALFORMED` added | §6 | CLAUDE (K-01, K-05) |
| 7 | L3_BINDING copy matrix from executed shapes; `ARTIFACT_HASH_COPY_MISSING` added | §8.1 | CLAUDE (K-04, K-05), EXECUTED |
| 8 | Expected state hash is a hard check in both modes; `None` copies defined | §8.3 | DEEPSEEK, CLAUDE (K-10) |
| 9 | L2 split into L2a (no artifact) and L2b (grounding) | §5.1, §9 | NEW-V0.3 |
| 10 | Closed status sets by exact string; legacy absent status; `UNKNOWN_STATUS`, `REQUIRED_FIELD_MISSING` added | §9.1 | CLAUDE (K-03, K-05), EXECUTED |
| 11 | Full-record equality by whole mapping; open field list removed | §9.2 G-2 | DEEPSEEK, CLAUDE |
| 12 | Legacy derivation for stamp `2.7.4` | §3.2, §9.2 G-3 | CLAUDE (K-09) |
| 13 | `FROZEN_ARTIFACT_ID_MISMATCH` added | §9.2 G-5 | CLAUDE (K-05), DEEPSEEK |
| 14 | Target-resolution rules R-1…R-3; `TARGET_RESOLUTION_INCONSISTENT` added | §9.3 | CLAUDE (K-07), AUTHOR, NEW-V0.3 |
| 15 | `BOUNDARY_VIOLATION:<key>` bounded to four constants | §10.1 | DEEPSEEK, EXECUTED |
| 16 | Allow-list pairs listed, `2.7.7` added, builder stamps required, `packet_version` rule, timestamp definition | §10.2, §10.3 | AUTHOR, CLAUDE (K-08, K-11), EXECUTED |
| 17 | D-1 mechanism: five tests, data-file legacy fixture, manifest, negative test | §11.1 | CLAUDE (K-02), DEEPSEEK, AUTHOR |
| 18 | One required code per adversarial case; new cases E1, E2, R1…R4, M4, M9, S3…S5, N2, N4…N6; controls NC10…NC12 | §11.3, §11.4 | CLAUDE (K-11), DEEPSEEK, NEW-V0.3 |
| 19 | `index_sha256` recorded as DEFERRED with the risk open; new risks R-2, R-5 and the replay non-claim | §12 | AUTHOR, CLAUDE (K-07), NEW-V0.3 |
| 20 | Undefined "P0-01/P0-02/P1" references removed; blockers listed by audit id | §13 | CLAUDE (K-11) |
| 21 | DeepSeek proposal `ANCHOR_EQUALS_SOURCE` not adopted: an anchor equal to the artifact's hash is the success condition | §4.5 | CLAUDE |

## Appendix B. Evidence statement

- Shapes, stamps, legacy packet-hash reproduction and V2.7.6 behaviour on the fail-first cases were obtained by running unmodified copies of V2.7.6 and V2.7.5.
- The predicates of §8, §9.1, §9.2 and §9.3 were checked with a throwaway script against genuine receipts from both versions (eleven receipt shapes each): no genuine receipt violated a rule. The same script confirmed that each of cases A, B, C1, C2, C3, E1, E2, E3, R1 to R4, M3 to M6 violates the rule assigned to it, and that the downgraded-stamp case (R-5) is not caught. That script is not an implementation of V2.7.7, was not added to any source tree, and is not a test result for V2.7.7.
- That script used the V0.3 forms of §8 and §9. The V0.5 form of the §9.3 prerequisites is the same predicate (no type or non-emptiness prerequisite), and was additionally checked on V2.7.6 against NC14, NC15 (no violation) and R5, R6 (each violates R-3 or R-1).
- The exact-type guard was checked only in this sense: a type scan of every input the existing suite and demo pass to the verifier found no unsupported type. The guard itself, its ordering, and `failure_details` have not been exercised.
- Python behaviours relied on in §6 were run directly: `sorted(keys, key=str)` and `dict.get` with a colliding hostile key invoke custom methods; `isinstance` accepts subclasses; a list used as a mapping key raises `TypeError`; `json.dumps` raises on a cycle.
- For V0.5.1, run on unmodified V2.7.6 and V2.7.5: self-translation in three configurations (statuses and ids as stated in §9.3), none violating the §8–§9 predicates; receipts with `receipt_version` deleted, numeric, or unlisted verify today; `boundary: None` raises `AttributeError`, an absent key and `{}` return the four boundary codes; both builders always write `receipt_version` and a `dict` boundary.
- For V0.5.2, run on unmodified V2.7.6 and V2.7.5: the cross-family rewrite of a self-translation receipt equals the genuine receipt for that family; a V2.7.5-built `NO_TARGET…` receipt with `target_script_family=None` carries stamp `2.7.4`, verifies under the V2.7.6 verifier and violates no predicate; cases Q8a, Q8b, X3b and both G0a inputs verify on V2.7.6 today and each violates the rule assigned to it.
- The execution predicates of §9.4 restate the conditions the throwaway script already used; the table itself and the consequence table have not been exercised by anything.
- For V0.5.3: on V2.7.5 code, the cross-family rewrite of a self-translation receipt equals the genuine `2.7.4` cross-family receipt and violates no predicate. The key-ownership rule and P-7 are text only and have not been exercised.
- **Correction to the script statement above `[TASKLET F08]`.** For R-3 the throwaway script compared sorted lists of candidate ids, which is stricter than the set comparison that V0.3 to V0.5.3 specified. It therefore rejected `[A, B, A]` while the specified rule accepted it. V0.5.4 changes the rule to match what the script checked. The earlier sentence that the script used "the same predicate" was wrong for R-3.
- For V0.5.4, run on unmodified V2.7.6 and V2.7.5: V2.7.6 verifies an `AMBIGUOUS…` receipt with candidates `[A, B, A]`; a query by an alias listed twice on one record returns that record twice on both versions; V2.7.6 returns `INTEGRITY_CHECK_FAILED` for artifacts whose record has a stored id that is a list, absent or different from its key, while V2.7.5 answers and its receipt verifies under V2.7.6; `json.loads` yields a lone-surrogate `str`, and such a value in a receipt field, a packet field or an artifact record makes the V2.7.6 verifier raise `UnicodeEncodeError`; all six artifacts that the existing suite and demo pass to the verifier satisfy record-key identity.
- §4.6, §9.1a, H-5 and the corrected test rows are text only and have not been exercised.
- For V0.5.6, run directly in CPython 3.13 (limit 4300): `json.dumps` and `str()` raise `ValueError` for `10**4300`; `2**63 - 1` and `-2**63` convert identically with the limit at 0, 640 and 4300. With the limit at 0 both calls succeed for `10**4300`. Tasklet reports the same on 3.12. A scan of the JSON files in the two trees (one and three files) found a largest integer of 27. Nothing else in V0.5.6 was executed: the integer-domain rule, packet presence, the conditional H-5 wording, the detail formats and all 12 added rows are text only.
- For V0.5.7 nothing was executed. Two statements rest on reading V2.7.6 source: the surface set at `unicode_normalization.py:65` and the required record fields at `integrity_verifier.py:35,91-93`. `normalized_surface`, the P-1 exception, the P-3 clarification, the conformance profile, T-6 to T-8 and the rows now named S4c, S4d, X6b and VS1 are text only.
- For V0.5.8 nothing was executed by the drafter. Tasklet reports an isolated run of a synthetic collector stream (32 distinct pairs plus two repeats: 32 retained, no truncation); that is a reviewer's primitive probe, not a V2.7.7 result. T-9 and the reworded S4d are text only.
- For V0.5.9 nothing was executed. T-10, the extended S4d cell and the amended gate 4 are text only.
- Phase 0, the failure cap, `failure_details`, `layers`, `assurance`, strict mode and policy checks have not been exercised by anything. REQUIRES_EXECUTION after implementation.

**END — V0.5.9 CONSOLIDATED / SPECIFICATION_ONLY / INDEPENDENT_REVIEW_PENDING**
