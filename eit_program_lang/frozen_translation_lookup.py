"""
EIT Program Lang V2.7.6
Frozen Translation Lookup

V2.7.6:
- F1: integrity-gated (verify before serve, fail-closed)
- F2: NFC normalization of all lookups
- F3: ambiguity is explicit — never candidates[0] silently.
      Multiple divergent candidates -> AMBIGUOUS_NO_SILENT_PICK.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import hashlib
import json
import copy

from .lookup_identity import build_id_projection, resolve_id, get_lookup_records

from .restored_registry_index import SAFETY_BLOCK
from .integrity_verifier import verify_restored_state
from .unicode_normalization import nfc, resolve_ambiguous_candidates


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
        role = nfc(rec.get("symbolic_role", "")).upper()
        if role:
            out.setdefault(role, []).append(sid)

    return out


def _resolve_source(records: Dict[str, Dict[str, Any]], query: str) -> Optional[Dict[str, Any]]:
    projection = build_id_projection(records, nfc)
    raw_id = resolve_id(projection, query, nfc)
    q = nfc(query)
    if raw_id is not None:
        return records[raw_id]

    q_lower = q.lower()

    for rec in records.values():
        if nfc(rec.get("visible_symbol", "")) == q:
            return rec

        if q_lower in [nfc(a).lower() for a in rec.get("aliases", []) or []]:
            return rec

        if q_lower == nfc(rec.get("sound_hint", "")).lower():
            return rec

    return None


def lookup_translation_from_frozen_registry(
    restored_state: Dict[str, Any],
    source_query: str,
    target_script_family: str,
    *,
    s1_context=None,
) -> Dict[str, Any]:
    if s1_context is not None:
        return s1_context.run_runtime(
            restored_state, source_query, target_script_family,
            verify_integrity=verify_restored_state, safety=SAFETY_BLOCK)
    # V2.7.6 — integrity gate: never serve from a tampered/unverifiable state.
    integrity = verify_restored_state(restored_state)
    if not integrity["verified"]:
        return {
            "status": "INTEGRITY_CHECK_FAILED",
            "integrity_failures": integrity["failures"],
            "source_query": source_query,
            "target_script_family": target_script_family,
            "translation_packet": None,
            "read_only": True,
            "safety": dict(SAFETY_BLOCK),
        }

    records = get_lookup_records(restored_state, artifact_nested=True)
    # Validate every identity before role indexing or serving.
    source = _resolve_source(records, source_query)
    role_index = _build_role_index(records)

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

    role = nfc(source.get("symbolic_role", "")).upper()
    target_family = nfc(target_script_family).upper()

    candidates = []

    for sid in role_index.get(role, []):
        rec = records[sid]
        if nfc(rec.get("script_family", "")).upper() == target_family:
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

    # V2.7.6 — F1: explicit ambiguity resolution, never silent candidates[0]
    resolution = resolve_ambiguous_candidates(candidates)
    if resolution["status"] == "AMBIGUOUS_NO_SILENT_PICK":
        return {
            "status": "AMBIGUOUS_NO_SILENT_PICK",
            "source_symbol_id": source.get("symbol_id"),
            "symbolic_role": role,
            "target_script_family": target_script_family,
            "ambiguous_candidates": [
                {"symbol_id": c.get("symbol_id"), "visible_symbol": c.get("visible_symbol")}
                for c in resolution["candidates"]
            ],
            "translation_packet": None,
            "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
            "read_only": True,
            "safety": dict(SAFETY_BLOCK),
        }

    target = resolution["chosen"]

    packet = {
        "packet_type": "FROZEN_REGISTRY_TRANSLATION_PACKET",
        "packet_version": "2.7.6",
        "source_symbol_id": source.get("symbol_id"),
        "target_symbol_id": target.get("symbol_id"),
        "source_script_family": source.get("script_family"),
        "target_script_family": target.get("script_family"),
        "source_visible_symbol": source.get("visible_symbol"),
        "target_visible_symbol": target.get("visible_symbol"),
        "symbolic_role": role,
        "meaning_invariant": copy.deepcopy(source.get("meaning_invariant", [])),
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "restored_state_sha256": restored_state.get("restored_state_sha256"),
        "read_only": True,
        "boundary": dict(SAFETY_BLOCK),
    }

    packet["packet_sha256"] = sha256_json(packet)

    return {
        "status": "TRANSLATED_FROM_FROZEN_REGISTRY",
        "source": copy.deepcopy(source),
        "target": copy.deepcopy(target),
        "translation_packet": packet,
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "restored_state_sha256": restored_state.get("restored_state_sha256"),
        "read_only": True,
        "safety": dict(SAFETY_BLOCK),
    }
