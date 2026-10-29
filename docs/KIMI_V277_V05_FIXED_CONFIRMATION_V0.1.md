# KIMI — V0.5 FIXED VERIFIER CONFIRMATION — 18/18 ARTIFACT-BOUND

**DATE:** 2026-10-22 · **RESPONDS TO:** "Испорака на фиксиран верификатор V0.5" packet

## 1. Byte verification
`Receipt-Verifier-V277-Candidate-V05-Fixed.py` installed as `receipt_verifier_v277_candidate.py`:
- Bytes: 38,748 · SHA-256: `11dcbebc0f7c66d7cab6daa1b5c06bfd9ee258170f1dfcbe36bcd8cde83501f2`
- **EXACT MATCH with the claimed manifest value.** Prior version archived as
  `receipt_verifier_v277_candidate_V04_a34070d6.py` (history preserved).

## 2. Static confirmation of the fix (Tasklet N-1 class / TOCTOU)
Loader order in the fixed bytes, read from source:
1. `open(_mpath).read()` — single read of companion bytes;
2. SHA-256 of THOSE bytes compared to pinned `4ba6556a…4444ad65`;
3. mismatch → `ImportError` (fail-closed);
4. only after verification: regex-extract the SAFETY_BLOCK literal, `ast.literal_eval`.
No `exec_module`, no `exec(`, no import of the companion anywhere. Checked bytes == parsed
bytes (single read). Non-execution established statically.

## 3. Diff scope vs a34070d6 (V0.4)
Confined to: loader block (N-1 fix), §2.1 comment (N-2), Q4 comment (N-2, now OPEN),
`_l0_result` non-raw branch cleanup (N-3). **Zero verifier-logic changes.**

## 4. Self-check on the fixed bytes
`selfcheck_v277_v05.py` (749d9bcb…, matches manifest) in an isolated temp dir:
- **18/18 PASS, exit code 0**
- Log: `SELFCHECK_OUTPUT_V05FIXED.log` — binds verifier SHA-256 `11dcbebc…`, 38,748 bytes,
  UTC 2026-10-22T19:17:41Z, Python 3.12.12, exit code.
- Includes 16/16 SAFETY_BLOCK equality vs V2.7.6 bytes (ast.literal_eval) and both
  fail-closed companion demos with specific messages.

## 5. Terminology held
- Closed: the **candidate companion-loading finding** (Tasklet F-1/N-1 class).
- **Spec §13 N-1 (source-side silent pick) remains OPEN under RG-6** — different item.
- Self-checks remain candidate evidence, NOT RG-4.

## 6. Manifest
`SHA256SUMS_V0.7-KIMI-CONFIRMED.txt` — all current artifacts incl. fixed verifier,
archived V0.4, both logs, skeletons, statuses.

**SEAL:** FIXED_BYTES_VERIFIED — LOADER_NON_EXECUTING_STATICALLY_PROVEN — 18_18_ARTIFACT_BOUND — SPEC_N1_STILL_OPEN
