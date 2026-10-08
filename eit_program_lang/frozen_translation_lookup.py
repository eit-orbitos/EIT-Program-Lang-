"""
EIT Program Lang V2.7.4
Frozen Translation Lookup

Performs translation using records restored from a frozen registry artifact.

This is read-only and provenance-bound.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import hashlib
import json

from .restored_registry_index import extract_records_from_restored_state, SAFETY_BLOCK


def sha256_json(data: Any) -> str:
    payload = json.dumps(
        data,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_role_index(records: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}

    for sid, rec in records.items():
        role = str(rec.get("symbolic_role", "")).upper()
        if role:
            out.setdefault(role, []).append(sid)

    return out


def _resolve_source(records: Dict[str, Dict[str, Any]], query: str) -> Optional[Dict[str, Any]]:
    if query in records:
        return records[query]

    q_lower = query.lower()

    for rec in records.values():
        if str(rec.get("visible_symbol", "")) == query:
            return rec

        if q_lower in [str(a).lower() for a in rec.get("aliases", []) or []]:
            return rec

        if q_lower == str(rec.get("sound_hint", "")).lower():
            return rec

    return None


def lookup_translation_from_frozen_registry(
    restored_state: Dict[str, Any],
    source_query: str,
    target_script_family: str,
) -> Dict[str, Any]:
    records = extract_records_from_restored_state(restored_state)
    role_index = _build_role_index(records)

    source = _resolve_source(records, source_query)

    if source is None:
        return {
            "status": "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY",
            "source_query": source_query,
            "target_script_family": target_script_family,
            "translation_packet": None,
            "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
            "read_only": True,
            "safety": dict(SAFETY_BLOCK),
        }

    role = str(source.get("symbolic_role", "")).upper()
    target_family = str(target_script_family).upper()

    candidates = []

    for sid in role_index.get(role, []):
        rec = records[sid]
        if str(rec.get("script_family", "")).upper() == target_family:
            candidates.append(rec)

    if not candidates:
        return {
            "status": "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
            "source_symbol_id": source.get("symbol_id"),
            "symbolic_role": role,
            "target_script_family": target_script_family,
            "translation_packet": None,
            "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
            "read_only": True,
            "safety": dict(SAFETY_BLOCK),
        }

    target = candidates[0]

    packet = {
        "packet_type": "FROZEN_REGISTRY_TRANSLATION_PACKET",
        "packet_version": "2.7.4",
        "source_symbol_id": source.get("symbol_id"),
        "target_symbol_id": target.get("symbol_id"),
        "source_script_family": source.get("script_family"),
        "target_script_family": target.get("script_family"),
        "source_visible_symbol": source.get("visible_symbol"),
        "target_visible_symbol": target.get("visible_symbol"),
        "symbolic_role": role,
        "meaning_invariant": source.get("meaning_invariant", []),
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "restored_state_sha256": restored_state.get("restored_state_sha256"),
        "read_only": True,
        "boundary": dict(SAFETY_BLOCK),
    }

    packet["packet_sha256"] = sha256_json(packet)

    return {
        "status": "TRANSLATED_FROM_FROZEN_REGISTRY",
        "source": source,
        "target": target,
        "translation_packet": packet,
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "restored_state_sha256": restored_state.get("restored_state_sha256"),
        "read_only": True,
        "safety": dict(SAFETY_BLOCK),
    }
