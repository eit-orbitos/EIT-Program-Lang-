"""F-2: preserve the retired invalid positive fixture of V2.7.6 tests/test_receipt_verifier.py
(_artifact / _receipt, lines 10-33, reproduced verbatim) as a data file. Run with the V2.7.6 tree on PYTHONPATH."""
import json
import os
import sys

from eit_program_lang.restored_query_receipt import build_restored_query_receipt
from eit_program_lang.integrity_verifier import artifact_sha256

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def _artifact():
    return {
        "frozen_artifact_id": "FROZEN",
        "frozen_registry_snapshot": {"registry_records": {}},
    }


def _receipt():
    art = _artifact()
    restored = {
        "restored_state_id": "R",
        "release_id": "REL",
        "frozen_artifact_id": "FROZEN",
        "frozen_artifact_sha256": artifact_sha256(art),
        "restored_state_sha256": "s" * 64,
        "current_version_id": "V2",
    }
    return build_restored_query_receipt(
        restored_state=restored,
        query_result={"query": "SOURCE", "found": True},
        translation_result={
            "status": "TRANSLATED_FROM_FROZEN_REGISTRY",
            "translation_packet": {"frozen_artifact_sha256": artifact_sha256(art)},
        },
    )


doc = {"artifact": _artifact(), "receipt": _receipt(),
       "provenance": {"source": "EIT_V2_7_6.zip tests/test_receipt_verifier.py _artifact()/_receipt() (lines 10-33)",
                      "builder": "V2.7.6 build_restored_query_receipt", "python": sys.version,
                      "status": "RETIRED invalid positive fixture (D-1, F-2): negative evidence only"}}
with open(os.path.join(OUT, "invalid_positive_receipt_v276.json"), "w", encoding="utf-8") as fh:
    json.dump(doc, fh, ensure_ascii=False, indent=1)
with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
    fh.write("# tests/legacy — retired fixture (spec V0.5.9 §11.1 F-2)\n\n"
             "`invalid_positive_receipt_v276.json` preserves the fixture that the five V2.7.6 receipt-verifier tests\n"
             "shared: it claims `found: True` and a translation over an artifact with zero records. It is negative\n"
             "evidence: one active test (F-3, row M9) asserts V2.7.7 rejects it with REQUIRED_FIELD_MISSING.\n"
             "This directory contains no test_*.py file, so pytest does not collect it.\n")
print("wrote invalid_positive_receipt_v276.json")
