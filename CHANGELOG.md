# EIT Program Lang — Changelog

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
