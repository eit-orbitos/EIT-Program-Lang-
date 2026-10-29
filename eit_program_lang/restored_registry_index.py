"""
EIT Program Lang V2.7.6
Restored Registry Index

Builds read-only indexes from a restored frozen registry.
V2.7.6: NFC-normalized index keys; registry_history fallback removed from
the query path (fail-closed — history is not covered by the artifact hash).

Author:
    Mr. Toni Mladenovski

Project Origin Date:
    18 April 2026
"""

from __future__ import annotations

from typing import Any, Dict, List
import hashlib
import json
import unicodedata


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


def nfc(text: Any) -> str:
    """Canonical NFC normalization for every query/index surface."""
    return unicodedata.normalize("NFC", str(text))


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
    allow_history_fallback: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    V2.7.6: fail-closed by default. Only records inside the hash-covered
    frozen artifact are served. registry_history is NOT covered by the
    artifact hash, so it is never used unless explicitly requested for
    non-serving introspection (allow_history_fallback=True).
    """
    frozen = restored_state.get("frozen_artifact", {})
    snapshot = frozen.get("frozen_registry_snapshot", {})
    records = snapshot.get("registry_records", {})

    if records or not allow_history_fallback:
        return records or {}

    history = restored_state.get("registry_history", {})
    current_version_id = restored_state.get("current_version_id") or history.get("current_version_id")
    version = history.get("versions", {}).get(current_version_id, {})
    snapshot_id = version.get("snapshot_id")
    snapshot = history.get("snapshots", {}).get(snapshot_id, {})
    return snapshot.get("registry_records", {}) or {}


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
        if visible is not None and str(visible) != "":
            visible_symbol_index.setdefault(nfc(visible), []).append(symbol_id)

        for alias in record.get("aliases", []) or []:
            alias_index.setdefault(nfc(alias).lower(), []).append(symbol_id)

        family = record.get("script_family")
        if family:
            script_family_index.setdefault(nfc(family).upper(), []).append(symbol_id)

        role = record.get("symbolic_role")
        if role:
            symbolic_role_index.setdefault(nfc(role).upper(), []).append(symbol_id)

        for meaning in record.get("meaning_invariant", []) or []:
            meaning_index.setdefault(nfc(meaning).lower(), []).append(symbol_id)

    index = {
        "index_type": "EIT_RESTORED_FROZEN_REGISTRY_INDEX",
        "index_version": "2.7.6",
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
