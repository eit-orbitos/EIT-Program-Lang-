"""
EIT Program Lang V2.7.4
Frozen Mutation Guard (preserved from V2.7.x line)

Denies any mutation of a restored frozen registry within the same
major version line. Fail-closed.
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
        "mutation_allowed": False if same_line else False,
        "status": "MUTATION_DENIED" if same_line else "MUTATION_DENIED_FROZEN_REGISTRY",
        "reason": (
            "RESTORED_REGISTRY_REMAINS_FROZEN: mutation inside frozen "
            "version line is always denied."
        ),
        "safety": dict(SAFETY_BLOCK),
    }
