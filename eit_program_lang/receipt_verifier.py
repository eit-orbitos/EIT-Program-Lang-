"""
EIT Program Lang V2.7.5
Independent Receipt Verifier

F4: verifies a restored query receipt independently — detects a tampered
receipt, and cross-checks the receipt's provenance against the source
frozen artifact. Fail-closed.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .integrity_verifier import artifact_sha256
from .restored_query_receipt import sha256_json
from .restored_registry_index import SAFETY_BLOCK


def verify_restored_query_receipt(
    receipt: Dict[str, Any],
    source_frozen_artifact: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    failures: List[str] = []

    if receipt.get("receipt_type") != "EIT_RESTORED_REGISTRY_QUERY_RECEIPT":
        failures.append("WRONG_RECEIPT_TYPE")

    declared = receipt.get("receipt_sha256")
    if not isinstance(declared, str) or len(declared) != 64:
        failures.append("RECEIPT_HASH_MALFORMED")
    else:
        body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
        if sha256_json(body) != declared:
            failures.append("RECEIPT_HASH_MISMATCH_TAMPER_DETECTED")

    boundary = receipt.get("boundary", {})
    for key, expected in (
        ("read_only_query_mode", True),
        ("restored_registry_remains_frozen", True),
        ("mutation_guard_enforced", True),
        ("real_world_control", False),
    ):
        if boundary.get(key) is not expected:
            failures.append(f"BOUNDARY_VIOLATION:{key}")

    if source_frozen_artifact is not None:
        source_sha = artifact_sha256(source_frozen_artifact)
        if receipt.get("frozen_artifact_sha256") != source_sha:
            failures.append("PROVENANCE_MISMATCH_WITH_SOURCE_ARTIFACT")

        packet = (receipt.get("translation_result") or {}).get("translation_packet") or {}
        if packet and packet.get("frozen_artifact_sha256") != source_sha:
            failures.append("TRANSLATION_PACKET_PROVENANCE_MISMATCH")

    return {
        "check_type": "VERIFY_RESTORED_QUERY_RECEIPT",
        "verified": not failures,
        "failures": failures,
        "receipt_sha256": declared,
        "safety": dict(SAFETY_BLOCK),
    }
