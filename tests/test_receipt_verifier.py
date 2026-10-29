"""F-1 migration (spec V0.5.9 §11.1) of the five tests of V2.7.6 tests/test_receipt_verifier.py to a genuine
fixture (artifact with real records, sealed state, results from query_restored_registry and
lookup_translation_from_frozen_registry), plus the F-3 active test. Written by Tasklet for RG-4 suite V1.
The original file is preserved unmodified inside EIT_V2_7_6.zip."""
import copy
import json
import os

from eit_program_lang.restored_registry_query import query_restored_registry
from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.restored_query_receipt import build_restored_query_receipt, sha256_json
from eit_program_lang.receipt_verifier import verify_restored_query_receipt
from eit_program_lang.integrity_verifier import artifact_sha256


def _artifact():
    return {
        "frozen_artifact_id": "FROZEN",
        "frozen_registry_snapshot": {"registry_records": {
            "LATIN-SOURCE": {"symbol_id": "LATIN-SOURCE", "script_family": "LATIN", "visible_symbol": "SOURCE",
                             "sound_hint": "source", "symbolic_role": "SOURCE_NODE",
                             "meaning_invariant": ["source", "origin"], "aliases": ["origin"]},
            "CYRILLIC-ИЗВОР": {"symbol_id": "CYRILLIC-ИЗВОР", "script_family": "CYRILLIC", "visible_symbol": "ИЗВОР",
                               "sound_hint": "izvor", "symbolic_role": "SOURCE_NODE",
                               "meaning_invariant": ["source", "origin"], "aliases": ["извор"]},
        }},
    }


def _receipt():
    art = _artifact()
    st = {"restored_state_id": "R", "release_id": "REL", "frozen_artifact_id": "FROZEN",
          "frozen_artifact_sha256": artifact_sha256(art), "current_version_id": "V2", "frozen_artifact": art}
    st["restored_state_sha256"] = sha256_json({k: v for k, v in st.items() if k != "restored_state_sha256"})
    q = query_restored_registry(st, "SOURCE")
    t = lookup_translation_from_frozen_registry(st, source_query="SOURCE", target_script_family="CYRILLIC")
    assert q["found"] is True and t["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY"
    return copy.deepcopy(build_restored_query_receipt(restored_state=st, query_result=q, translation_result=t))


def test_valid_receipt_verifies():
    r = verify_restored_query_receipt(_receipt(), source_frozen_artifact=_artifact())
    assert r["verified"] is True and r["failures"] == []


def test_tampered_receipt_detected():
    receipt = _receipt()
    receipt["query_result"]["found"] = False
    r = verify_restored_query_receipt(receipt, source_frozen_artifact=_artifact())
    assert r["verified"] is False
    assert "RECEIPT_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"]


def test_provenance_mismatch_detected():
    other = {"frozen_artifact_id": "OTHER", "frozen_registry_snapshot": {"registry_records": {}}}
    r = verify_restored_query_receipt(_receipt(), source_frozen_artifact=other)
    assert r["verified"] is False
    assert "PROVENANCE_MISMATCH_WITH_SOURCE_ARTIFACT" in r["failures"]


def test_boundary_violation_detected():
    body = _receipt()
    body["boundary"]["read_only_query_mode"] = False
    body["receipt_sha256"] = sha256_json({k: v for k, v in body.items() if k != "receipt_sha256"})
    r = verify_restored_query_receipt(body, source_frozen_artifact=_artifact())
    assert r["verified"] is False
    assert "BOUNDARY_VIOLATION:read_only_query_mode" in r["failures"]


def test_missing_source_artifact_fails_closed():
    r = verify_restored_query_receipt(_receipt())
    assert r["verified"] is False
    assert "SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK" in r["failures"]


def test_f3_legacy_invalid_positive_fixture_rejected():
    path = os.path.join(os.path.dirname(__file__), "legacy", "invalid_positive_receipt_v276.json")
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    r = verify_restored_query_receipt(d["receipt"], d["artifact"])
    assert r["verified"] is False
    assert "REQUIRED_FIELD_MISSING" in r["failures"]
