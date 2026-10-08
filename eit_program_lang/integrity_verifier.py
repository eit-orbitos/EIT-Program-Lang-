"""
EIT Program Lang V2.7.5
Integrity & Adversarial Validation — Artifact / Restore Verifier

Fail-closed verification of:
  - frozen artifact hash vs declared hash
  - restored state consistency vs frozen artifact
  - registry record structural integrity

Author: Mr. Toni Mladenovski
Project Origin Date: 18 April 2026
"""

from __future__ import annotations

from typing import Any, Dict, List
import hashlib
import json

from .restored_registry_index import SAFETY_BLOCK, extract_records_from_restored_state


def sha256_json(data: Any) -> str:
    payload = json.dumps(
        data, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def artifact_sha256(frozen_artifact: Dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(frozen_artifact, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


REQUIRED_RECORD_FIELDS = ("symbol_id", "script_family", "visible_symbol", "symbolic_role")


def verify_frozen_artifact(
    frozen_artifact: Dict[str, Any],
    declared_sha256: str,
) -> Dict[str, Any]:
    """F1: detect tampered artifact or wrong declared hash. Fail-closed."""
    failures: List[str] = []

    if not isinstance(frozen_artifact, dict) or not frozen_artifact:
        failures.append("ARTIFACT_MISSING_OR_NOT_A_MAPPING")
    if not isinstance(declared_sha256, str) or len(declared_sha256) != 64:
        failures.append("DECLARED_HASH_MALFORMED")

    computed = artifact_sha256(frozen_artifact) if isinstance(frozen_artifact, dict) else None
    if computed is not None and computed != declared_sha256:
        failures.append("ARTIFACT_HASH_MISMATCH_TAMPER_DETECTED")

    return {
        "check_type": "VERIFY_FROZEN_ARTIFACT",
        "verified": not failures,
        "failures": failures,
        "computed_sha256": computed,
        "declared_sha256": declared_sha256,
        "safety": dict(SAFETY_BLOCK),
    }


def verify_restored_state(restored_state: Dict[str, Any]) -> Dict[str, Any]:
    """F1: detect corrupt restore state / record-level tampering. Fail-closed."""
    failures: List[str] = []

    declared = restored_state.get("frozen_artifact_sha256")
    artifact = restored_state.get("frozen_artifact")
    if artifact is None:
        failures.append("RESTORED_STATE_HAS_NO_FROZEN_ARTIFACT")
    else:
        art_check = verify_frozen_artifact(artifact, declared or "")
        failures.extend(art_check["failures"])

    declared_state_sha = restored_state.get("restored_state_sha256")
    if declared_state_sha:
        body = {k: v for k, v in restored_state.items() if k != "restored_state_sha256"}
        if sha256_json(body) != declared_state_sha:
            failures.append("RESTORED_STATE_HASH_MISMATCH_TAMPER_DETECTED")

    records = extract_records_from_restored_state(restored_state)
    for sid, rec in records.items():
        for field in REQUIRED_RECORD_FIELDS:
            if field not in rec:
                failures.append(f"RECORD_{sid}_MISSING_FIELD_{field}")
        if rec.get("symbol_id") != sid:
            failures.append(f"RECORD_KEY_SYMBOL_ID_MISMATCH:{sid}")

    return {
        "check_type": "VERIFY_RESTORED_STATE",
        "verified": not failures,
        "failures": failures,
        "record_count": len(records),
        "safety": dict(SAFETY_BLOCK),
    }
