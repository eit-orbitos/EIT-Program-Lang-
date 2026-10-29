# EIT Program Lang — Changelog

## V2.7.6 (2026-10-09) — HARDENING (candidate, under independent review)
Response to independent dual review of V2.7.5 @ commit 2b7dd62
(REPRODUCIBLE / NEEDS_FIX, findings 1–8).

Fixed (fail-first: 7 regression tests proven FAIL on unpatched V2.7.5):
1. Silent ambiguous translation pick -> AMBIGUOUS_NO_SILENT_PICK, packet=None
2. NFC/NFD mismatch -> NFC normalization at index build, query, translation
3. Direct writes to frozen state served -> mandatory integrity gate on every
   query/translation entry point (INTEGRITY_CHECK_FAILED)
4. registry_history fallback injection -> allow_history_fallback=False default;
   fallback records never served

Hardened:
5. receipt_verifier: source_frozen_artifact now mandatory (no silent skip)
6. demo_v2_7_5: f5_boundary_declared computed, not hardcoded
7. verify.yml: inventory coverage step (git ls-files == SHA256SUMS)
8. demos: real assert blocks; mutation_guard: honest unconditional deny

- tests: 33 total (25 original fixtures upgraded to fully-hashed states —
  fixture strengthening only, no assertion weakened — plus 7 fail-first
  regressions + 1 receipt-hardening test)
- V2.7.5 baseline preserved unchanged at GitHub commit 2b7dd62

Status: DEVELOPMENT / VALIDATION_PENDING. CANONICAL_FREEZE: NO.

## V2.7.5 (2026-10-08) — INTEGRITY_ADVERSARIAL_VALIDATION
Response to V2.7.4 audit (NEEDS_FIX, findings F1–F5).

Added:
- integrity_verifier.py — frozen artifact / restored state verification, fail-closed
- deep_mutation_guard.py — 5-attack mutation battery with before/after surface hashing
- unicode_normalization.py — NFC normalization, conflict scan, explicit ambiguity (no silent pick)
- receipt_verifier.py — independent receipt verification (tamper, provenance mismatch, boundary violation)
- integration_boundary.py — explicit non-claims for CA-Lang / 11D / IFIM / ASI_OS
- 22 new tests (25 total, all PASS)
- demo_v2_7_5.py + dist/adversarial_validation_report.json

Status: DEVELOPMENT / VALIDATION_PENDING. CANONICAL_FREEZE: NO.

## V2.7.4 (2026-10-08) — RESTORED_REGISTRY_QUERY_RUNTIME
Added:
- restored_registry_index.py, restored_registry_query.py
- frozen_translation_lookup.py, restored_query_receipt.py
- mutation_guard.py (demo shim)
- 3 tests (PASS), demo_v2_7_4.py

Audit: NEEDS_FIX (F1–F5). Superseded by V2.7.5.
