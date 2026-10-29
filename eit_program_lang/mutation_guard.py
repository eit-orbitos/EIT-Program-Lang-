"""
EIT Program Lang V2.7.6
Frozen Mutation Guard (preserved from V2.7.x line)

Denies any mutation of a restored frozen registry. V2.7.6 honesty fix:
mutation is denied unconditionally (any version line), and the returned
fields say so plainly instead of a dead conditional.
"""

from __future__ import annotations

from typing import Any, Dict

from .restored_registry_index import SAFETY_BLOCK


def check_frozen_mutation(
    restored_state: Dict[str, Any],
    version_spec: str,
    mutation_request: str | None = None,
) -> Dict[str, Any]:
    current = str(restored_state.get("current_version_id") or "2.x")
    req_major = str(version_spec).split(".")[0]
    cur_major = current.split(".")[0].lstrip("Vv")

    same_line = req_major.lstrip("Vv") == cur_major

    return {
        "check_type": "CHECK_FROZEN_MUTATION",
        "mutation_request": mutation_request,
        "version_spec": version_spec,
        "current_version_id": current,
        "same_major_version_line": same_line,
        # Honest invariant: mutation of a frozen registry is denied
        # unconditionally. same_major_version_line is reported for
        # information only; it does NOT influence the decision.
        "mutation_allowed": False,
        "status": "MUTATION_DENIED",
        "reason": (
            "RESTORED_REGISTRY_REMAINS_FROZEN: mutation of a frozen "
            "registry is always denied, on any version line."
        ),
        "safety": dict(SAFETY_BLOCK),
    }
