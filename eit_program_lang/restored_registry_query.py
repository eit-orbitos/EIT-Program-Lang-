"""
EIT Program Lang V2.7.4
Restored Registry Query

Read-only query functions for restored frozen registry state.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .restored_registry_index import (
    build_restored_registry_index,
    extract_records_from_restored_state,
    SAFETY_BLOCK,
)


def query_restored_registry(
    restored_state: Dict[str, Any],
    query: str,
    mode: str = "auto",
) -> Dict[str, Any]:
    records = extract_records_from_restored_state(restored_state)
    index = build_restored_registry_index(restored_state)

    q = str(query)
    q_lower = q.lower()
    q_upper = q.upper()

    matched_ids: List[str] = []
    reason = ""

    if mode == "auto":
        if q in index["symbol_id_index"]:
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
        if q in records:
            matched_ids = [q]
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
                    str(record.get("visible_symbol", "")),
                    str(record.get("sound_hint", "")),
                    str(record.get("symbolic_role", "")),
                    " ".join(map(str, record.get("meaning_invariant", []) or [])),
                    " ".join(map(str, record.get("aliases", []) or [])),
                ]
            ).lower()

            if q_lower in blob:
                matched_ids.append(symbol_id)

        reason = "MATCH_BLOB"

    results = [records[sid] for sid in matched_ids if sid in records]

    return {
        "query": query,
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
