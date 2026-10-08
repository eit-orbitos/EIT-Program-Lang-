"""F4: independent receipt verification — tampered receipt / provenance mismatch."""
import copy

from eit_program_lang.restored_query_receipt import build_restored_query_receipt
from eit_program_lang.receipt_verifier import verify_restored_query_receipt
from eit_program_lang.integrity_verifier import artifact_sha256


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


def test_valid_receipt_verifies():
    receipt = _receipt()
    r = verify_restored_query_receipt(receipt, source_frozen_artifact=_artifact())
    assert r["verified"] is True and r["failures"] == []


def test_tampered_receipt_detected():
    receipt = _receipt()
    receipt["query_result"]["found"] = False  # silent edit
    r = verify_restored_query_receipt(receipt, source_frozen_artifact=_artifact())
    assert r["verified"] is False
    assert "RECEIPT_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"]


def test_provenance_mismatch_detected():
    receipt = _receipt()
    other_artifact = {"frozen_artifact_id": "OTHER", "frozen_registry_snapshot": {"registry_records": {}}}
    r = verify_restored_query_receipt(receipt, source_frozen_artifact=other_artifact)
    assert r["verified"] is False
    assert "PROVENANCE_MISMATCH_WITH_SOURCE_ARTIFACT" in r["failures"]


def test_boundary_violation_detected():
    receipt = _receipt()
    body = copy.deepcopy(receipt)
    body["boundary"]["read_only_query_mode"] = False
    # re-seal so only the boundary check can fire
    from eit_program_lang.restored_query_receipt import sha256_json
    body["receipt_sha256"] = sha256_json({k: v for k, v in body.items() if k != "receipt_sha256"})
    r = verify_restored_query_receipt(body)
    assert r["verified"] is False
    assert "BOUNDARY_VIOLATION:read_only_query_mode" in r["failures"]
