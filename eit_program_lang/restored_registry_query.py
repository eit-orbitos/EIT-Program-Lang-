"""
EIT Program Lang V2.7.6
Restored Registry Query

Read-only query functions for restored frozen registry state.
V2.7.6: integrity-gated (verify before serve, fail-closed) and
NFC-normalized matching.
"""

from __future__ import annotations

from typing import Any, Dict, List
import copy

from .lookup_identity import build_id_projection, resolve_id, get_lookup_records
from .unicode_normalization import nfc

from .restored_registry_index import (
    build_restored_registry_index,
    SAFETY_BLOCK,
)
from .integrity_verifier import verify_restored_state


def query_restored_registry(
    restored_state: Dict[str, Any],
    query: str,
    mode: str = "auto",
) -> Dict[str, Any]:
    # V2.7.6 — F3: integrity gate. A tampered or unverifiable frozen state
    # is never served, no matter what the records contain.
    integrity = verify_restored_state(restored_state)
    if not integrity["verified"]:
        return {
            "query": query,
            "status": "INTEGRITY_CHECK_FAILED",
            "integrity_failures": integrity["failures"],
            "found": False,
            "match_count": 0,
            "symbol_ids": [],
            "records": [],
            "read_only": True,
            "safety": dict(SAFETY_BLOCK),
        }

    records = get_lookup_records(restored_state, artifact_nested=True)
    projection = build_id_projection(records, nfc)
    raw_id = resolve_id(projection, query, nfc)
    index = build_restored_registry_index(restored_state)

    q = nfc(query)  # V2.7.6 — F2: canonical Unicode normalization
    q_lower = q.lower()
    q_upper = q.upper()

    matched_ids: List[str] = []
    reason = ""

    if mode == "auto":
        if raw_id is not None:
            mode = "symbol_id"
        elif q in index["visible_symbol_index"]:
            mode = "visible_symbol"
        elif q_lower in index["alias_index"]:
            mode = "alias"
        elif q_upper in index["script_family_index"]:
            mode = "script_family"
        elif q_upper in index["symbolic_role_index"]:
            mode = "symbolic_role"
        elif q_lower in index["meaning_index"]:
            mode = "meaning"
        else:
            mode = "blob"

    if mode == "symbol_id":
        if raw_id is not None:
            matched_ids = [raw_id]
            reason = "MATCH_SYMBOL_ID"

    elif mode == "visible_symbol":
        matched_ids = index["visible_symbol_index"].get(q, [])
        reason = "MATCH_VISIBLE_SYMBOL"

    elif mode == "alias":
        matched_ids = index["alias_index"].get(q_lower, [])
        reason = "MATCH_ALIAS"

    elif mode == "script_family":
        matched_ids = index["script_family_index"].get(q_upper, [])
        reason = "MATCH_SCRIPT_FAMILY"

    elif mode == "symbolic_role":
        matched_ids = index["symbolic_role_index"].get(q_upper, [])
        reason = "MATCH_SYMBOLIC_ROLE"

    elif mode == "meaning":
        matched_ids = index["meaning_index"].get(q_lower, [])
        reason = "MATCH_MEANING_INVARIANT"

    elif mode == "blob":
        for symbol_id, record in records.items():
            blob = " ".join(
                [
                    symbol_id,
                    nfc(record.get("visible_symbol", "")),
                    nfc(record.get("sound_hint", "")),
                    nfc(record.get("symbolic_role", "")),
                    " ".join(nfc(m) for m in record.get("meaning_invariant", []) or []),
                    " ".join(nfc(a) for a in record.get("aliases", []) or []),
                ]
            ).lower()

            if q_lower in blob:
                matched_ids.append(symbol_id)

        reason = "MATCH_BLOB"

    results = [copy.deepcopy(records[sid]) for sid in matched_ids if sid in records]

    return {
        "query": query,
        "status": "OK" if results else "NO_MATCH",
        "mode": mode,
        "reason": reason,
        "found": bool(results),
        "match_count": len(results),
        "symbol_ids": matched_ids,
        "records": results,
        "index_sha256": index["index_sha256"],
        "frozen_artifact_sha256": restored_state.get("frozen_artifact_sha256"),
        "read_only": True,
        "safety": dict(SAFETY_BLOCK),
    }
