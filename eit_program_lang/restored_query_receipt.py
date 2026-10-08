"""
EIT Program Lang V2.7.4
Restored Registry Query Receipt
"""

from __future__ import annotations

from typing import Any, Dict
from datetime import datetime, timezone
import hashlib
import json


def sha256_json(data: Any) -> str:
    payload = json.dumps(
        data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_restored_query_receipt(
    restored_state: Dict[str, Any],
    query_result: Dict[str, Any] | None = None,
    translation_result: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    receipt = {
        "receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT",
        "receipt_version": "2.7.4",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "module_id": "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4",
        "author": "Mr. Toni Mladenovski",
        "project_origin_date": "18 April 2026",

        "restored_state_id": restored_state.get("restored_state_id"),
        "release_id": restored_state.get("release_id"),
        "frozen_artifact_id": restored_state.get("frozen_artifact_id"),
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "restored_state_sha256": restored_state.get("restored_state_sha256"),
        "current_version_id": restored_state.get("current_version_id"),

        "query_result": query_result or {},
        "translation_result": translation_result or {},

        "boundary": {
            "restored_registry_query_runtime": True,
            "read_only_query_mode": True,
            "restored_registry_remains_frozen": True,
            "mutation_guard_enforced": True,
            "not_blockchain": True,
            "not_legal_authority": True,
            "not_official_linguistic_authority": True,
            "not_perfect_translation_claim": True,
            "zero_error_is_model_axiom": True,
            "not_empirical_claim": True,
            "not_biological_consciousness": True,
            "not_sentience": True,
            "not_asi_proof": True,
            "not_physical_quantum_os": True,
            "real_world_control": False,
            "not_proof": True,
        },
    }

    receipt["receipt_sha256"] = sha256_json(receipt)
    return receipt
