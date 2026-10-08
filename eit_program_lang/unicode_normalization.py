"""
EIT Program Lang V2.7.5
Unicode Normalization & Ambiguity Handling

F3: NFC-normalize queries and record surfaces so canonically equivalent
Unicode matches; expose ambiguity and conflicts explicitly instead of
silently picking one candidate. Fail-closed on unresolved ambiguity.
"""

from __future__ import annotations

from typing import Any, Dict, List
import unicodedata

from .restored_registry_index import extract_records_from_restored_state, SAFETY_BLOCK


def nfc(text: Any) -> str:
    return unicodedata.normalize("NFC", str(text))


def detect_registry_conflicts(restored_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Conflicts: two records with same (script_family, visible_symbol) but
    different symbolic_role, or duplicate symbol surfaces with divergent
    meaning_invariant. Reported, never silently resolved.
    """
    records = extract_records_from_restored_state(restored_state)
    conflicts: List[Dict[str, Any]] = []
    seen: Dict[str, str] = {}

    for sid, rec in records.items():
        key = f"{nfc(rec.get('script_family','')).upper()}::{nfc(rec.get('visible_symbol',''))}"
        if key in seen:
            other = records[seen[key]]
            if rec.get("symbolic_role") != other.get("symbolic_role") or \
               rec.get("meaning_invariant") != other.get("meaning_invariant"):
                conflicts.append({
                    "surface": key,
                    "symbol_ids": [seen[key], sid],
                    "type": "DIVERGENT_DUPLICATE_SURFACE",
                })
        else:
            seen[key] = sid

    return {
        "check_type": "REGISTRY_CONFLICT_SCAN",
        "conflict_free": not conflicts,
        "conflicts": conflicts,
        "safety": dict(SAFETY_BLOCK),
    }


def resolve_ambiguous_candidates(
    candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    F3: ambiguity is explicit. Zero candidates -> miss; one -> resolved;
    many with identical visible surfaces -> resolved deterministically;
    many divergent -> AMBIGUOUS, no silent pick.
    """
    if not candidates:
        return {"status": "NO_CANDIDATES", "chosen": None, "candidates": []}

    surfaces = {nfc(c.get("visible_symbol")) for c in candidates}
    if len(candidates) == 1 or len(surfaces) == 1:
        return {
            "status": "RESOLVED" if len(candidates) == 1 else "RESOLVED_IDENTICAL_SURFACES",
            "chosen": sorted(candidates, key=lambda c: str(c.get("symbol_id")))[0],
            "candidates": candidates,
        }

    return {
        "status": "AMBIGUOUS_NO_SILENT_PICK",
        "chosen": None,
        "candidates": candidates,
        "safety": dict(SAFETY_BLOCK),
    }
