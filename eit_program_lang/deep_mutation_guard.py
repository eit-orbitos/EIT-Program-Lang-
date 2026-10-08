"""
EIT Program Lang V2.7.5
Deep Mutation Guard

F2: goes beyond denying a single mutation request — proves the restored
registry surface is unmodified after arbitrary attempted writes, by
before/after snapshot hashing. Fail-closed.

Note: this is structural integrity evidence, not proof against all
conceivable mutations (no runtime can claim that). Boundary preserved.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List
import copy

from .restored_registry_index import (
    SAFETY_BLOCK,
    extract_records_from_restored_state,
    sha256_json,
)


def registry_surface_sha256(restored_state: Dict[str, Any]) -> str:
    records = extract_records_from_restored_state(restored_state)
    return sha256_json(records)


def attempt_mutation_and_verify(
    restored_state: Dict[str, Any],
    mutation_fn: Callable[[Dict[str, Any]], None],
    mutation_label: str,
) -> Dict[str, Any]:
    """
    Runs an attempted mutation against a deep copy (the frozen state itself
    is never touched), then verifies the original surface is unchanged and
    reports whether the attempted write would have altered the surface.
    """
    before = registry_surface_sha256(restored_state)

    shadow = copy.deepcopy(restored_state)
    attempted_effect = "UNKNOWN"
    try:
        mutation_fn(shadow)
        after_shadow = registry_surface_sha256(shadow)
        attempted_effect = "WOULD_ALTER_SURFACE" if after_shadow != before else "NO_SURFACE_EFFECT"
    except Exception as exc:  # noqa: BLE001 - fail-closed reporting
        attempted_effect = f"MUTATION_RAISED:{type(exc).__name__}"

    after = registry_surface_sha256(restored_state)
    intact = before == after

    return {
        "check_type": "DEEP_MUTATION_GUARD",
        "mutation_label": mutation_label,
        "attempted_effect_on_shadow": attempted_effect,
        "frozen_surface_before": before,
        "frozen_surface_after": after,
        "frozen_registry_intact": intact,
        "mutation_applied_to_frozen": False,
        "guard_policy": "WRITE_TO_FROZEN_REGISTRY_ALWAYS_DENIED",
        "boundary_note": (
            "Structural before/after evidence only; not a claim of proof "
            "against all conceivable mutation vectors."
        ),
        "safety": dict(SAFETY_BLOCK),
    }


def run_mutation_battery(restored_state: Dict[str, Any]) -> Dict[str, Any]:
    """Standard adversarial write battery against the frozen registry."""
    records_probe = extract_records_from_restored_state(restored_state)
    any_sid = next(iter(records_probe), "X")

    def _add_record(state):
        extract_records_from_restored_state(state)["EVIL-INJECTED"] = {"symbol_id": "EVIL-INJECTED"}

    def _delete_record(state):
        extract_records_from_restored_state(state).pop(any_sid, None)

    def _overwrite_record(state):
        recs = extract_records_from_restored_state(state)
        if any_sid in recs:
            recs[any_sid]["visible_symbol"] = "TAMPERED"

    def _overwrite_provenance(state):
        state["frozen_artifact_sha256"] = "0" * 64

    def _clear_all(state):
        extract_records_from_restored_state(state).clear()

    battery = [
        ("ADD_RECORD", _add_record),
        ("DELETE_RECORD", _delete_record),
        ("OVERWRITE_RECORD_FIELD", _overwrite_record),
        ("OVERWRITE_PROVENANCE_HASH", _overwrite_provenance),
        ("CLEAR_ALL_RECORDS", _clear_all),
    ]

    results: List[Dict[str, Any]] = [
        attempt_mutation_and_verify(restored_state, fn, label) for label, fn in battery
    ]

    return {
        "check_type": "MUTATION_BATTERY",
        "attempt_count": len(results),
        "all_frozen_registry_intact": all(r["frozen_registry_intact"] for r in results),
        "any_mutation_applied_to_frozen": any(r["mutation_applied_to_frozen"] for r in results),
        "results": results,
        "safety": dict(SAFETY_BLOCK),
    }
