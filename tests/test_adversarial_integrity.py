"""F1: negative tests — tampered artifact, wrong hash, corrupt restore state."""
import copy

from eit_program_lang.integrity_verifier import (
    verify_frozen_artifact,
    verify_restored_state,
    artifact_sha256,
)


def _artifact():
    return {
        "artifact_type": "EIT_FROZEN_REGISTRY_ARTIFACT",
        "frozen_artifact_id": "FROZEN",
        "frozen_registry_snapshot": {
            "registry_records": {
                "LATIN-SOURCE": {
                    "symbol_id": "LATIN-SOURCE",
                    "script_family": "LATIN",
                    "visible_symbol": "SOURCE",
                    "symbolic_role": "SOURCE_NODE",
                    "meaning_invariant": ["source"],
                    "aliases": ["origin"],
                }
            }
        },
    }


def _restored():
    from eit_program_lang.restored_registry_index import sha256_json
    art = _artifact()
    state = {
        "restored_state_id": "R",
        "frozen_artifact_id": "FROZEN",
        "frozen_artifact_sha256": artifact_sha256(art),
        "current_version_id": "V2",
        "frozen_artifact": art,
    }
    state["restored_state_sha256"] = sha256_json(
        {k: v for k, v in state.items() if k != "restored_state_sha256"}
    )
    return state


def test_clean_artifact_verifies():
    art = _artifact()
    r = verify_frozen_artifact(art, artifact_sha256(art))
    assert r["verified"] is True and r["failures"] == []


def test_tampered_artifact_detected():
    art = _artifact()
    declared = artifact_sha256(art)
    art["frozen_registry_snapshot"]["registry_records"]["LATIN-SOURCE"]["visible_symbol"] = "EVIL"
    r = verify_frozen_artifact(art, declared)
    assert r["verified"] is False
    assert "ARTIFACT_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"]


def test_wrong_hash_detected():
    r = verify_frozen_artifact(_artifact(), "0" * 64)
    assert r["verified"] is False
    assert "ARTIFACT_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"]


def test_malformed_hash_detected():
    r = verify_frozen_artifact(_artifact(), "not-a-hash")
    assert r["verified"] is False
    assert "DECLARED_HASH_MALFORMED" in r["failures"]


def test_clean_restored_state_verifies():
    assert verify_restored_state(_restored())["verified"] is True


def test_corrupt_restore_state_detected():
    bad = _restored()
    bad["frozen_artifact"]["frozen_registry_snapshot"]["registry_records"][
        "LATIN-SOURCE"
    ]["symbolic_role"] = "HACKED"
    r = verify_restored_state(bad)
    assert r["verified"] is False
    assert "ARTIFACT_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"]


def test_record_key_mismatch_detected():
    bad = _restored()
    recs = bad["frozen_artifact"]["frozen_registry_snapshot"]["registry_records"]
    recs["LATIN-SOURCE"]["symbol_id"] = "RENAMED-INPLACE"
    # keep artifact hash consistent so ONLY the key mismatch is caught
    from eit_program_lang.integrity_verifier import artifact_sha256 as a
    bad["frozen_artifact_sha256"] = a(bad["frozen_artifact"])
    r = verify_restored_state(bad)
    assert r["verified"] is False
    assert any("RECORD_KEY_SYMBOL_ID_MISMATCH" in f for f in r["failures"])


def test_missing_artifact_in_state_detected():
    bad = _restored()
    del bad["frozen_artifact"]
    r = verify_restored_state(bad)
    assert r["verified"] is False
    assert "RESTORED_STATE_HAS_NO_FROZEN_ARTIFACT" in r["failures"]
