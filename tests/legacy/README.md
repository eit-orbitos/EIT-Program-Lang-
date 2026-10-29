# tests/legacy — retired fixture (spec V0.5.9 §11.1 F-2)

`invalid_positive_receipt_v276.json` preserves the fixture that the five V2.7.6 receipt-verifier tests
shared: it claims `found: True` and a translation over an artifact with zero records. It is negative
evidence: one active test (F-3, row M9) asserts V2.7.7 rejects it with REQUIRED_FIELD_MISSING.
This directory contains no test_*.py file, so pytest does not collect it.
