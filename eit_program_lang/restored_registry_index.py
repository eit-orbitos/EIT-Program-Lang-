"""
EIT Program Lang V2.7.4
Restored Registry Index

Builds read-only indexes from a restored frozen registry.

Author:
    Mr. Toni Mladenovski

Project Origin Date:
    18 April 2026
"""

from __future__ import annotations

from typing import Any, Dict, List
import hashlib
import json


SAFETY_BLOCK = {
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
}


def sha256_json(data: Any) -> str:
    payload = json.dumps(
        data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def extract_records_from_restored_state(
    restored_state: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    frozen = restored_state.get("frozen_artifact", {})
    snapshot = frozen.get("frozen_registry_snapshot", {})

    records = snapshot.get("registry_records", {})

    if not records:
        history = restored_state.get("registry_history", {})
        current_version_id = restored_state.get("current_version_id") or history.get("current_version_id")
        version = history.get("versions", {}).get(current_version_id, {})
        snapshot_id = version.get("snapshot_id")
        snapshot = history.get("snapshots", {}).get(snapshot_id, {})
        records = snapshot.get("registry_records", {})

    return records or {}


def build_restored_registry_index(
    restored_state: Dict[str, Any],
) -> Dict[str, Any]:
    records = extract_records_from_restored_state(restored_state)

    symbol_id_index = {}
    visible_symbol_index = {}
    alias_index = {}
    script_family_index = {}
    symbolic_role_index = {}
    meaning_index = {}

    for symbol_id, record in records.items():
        symbol_id_index[symbol_id] = symbol_id

        visible = record.get("visible_symbol")
        if visible:
            visible_symbol_index.setdefault(str(visible), []).append(symbol_id)

        for alias in record.get("aliases", []) or []:
            alias_index.setdefault(str(alias).lower(), []).append(symbol_id)

        family = record.get("script_family")
        if family:
            script_family_index.setdefault(str(family).upper(), []).append(symbol_id)

        role = record.get("symbolic_role")
        if role:
            symbolic_role_index.setdefault(str(role).upper(), []).append(symbol_id)

        for meaning in record.get("meaning_invariant", []) or []:
            meaning_index.setdefault(str(meaning).lower(), []).append(symbol_id)

    index = {
        "index_type": "EIT_RESTORED_FROZEN_REGISTRY_INDEX",
        "restored_state_id": restored_state.get("restored_state_id"),
        "release_id": restored_state.get("release_id"),
        "frozen_artifact_id": restored_state.get("frozen_artifact_id"),
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "record_count": len(records),
        "symbol_id_index": symbol_id_index,
        "visible_symbol_index": visible_symbol_index,
        "alias_index": alias_index,
        "script_family_index": script_family_index,
        "symbolic_role_index": symbolic_role_index,
        "meaning_index": meaning_index,
        "safety": dict(SAFETY_BLOCK),
    }

    index["index_sha256"] = sha256_json(index)
    return index
