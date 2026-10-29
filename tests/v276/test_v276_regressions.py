"""
V2.7.6 FAIL-FIRST REGRESSION TESTS (findings 1-4 from independent review)

Each test encodes the SECURE behavior. Against the unpatched V2.7.5 code,
every test in this file MUST FAIL. That failure is the proof that the test
actually guards the finding.
"""
import copy
import hashlib
import json
import unicodedata

from eit_program_lang.restored_registry_query import query_restored_registry
from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.integrity_verifier import artifact_sha256
from eit_program_lang.restored_registry_index import sha256_json


def _rec(sid, fam, vis, role="R", meaning=None, aliases=None):
    return {
        "symbol_id": sid, "script_family": fam, "visible_symbol": vis,
        "symbolic_role": role, "meaning_invariant": meaning or ["x"],
        "aliases": aliases or [],
    }


def _verified_state(records):
    """Fully-hashed restored state: artifact hash + state hash, integrity-clean."""
    art = {"frozen_artifact_id": "F", "frozen_registry_snapshot": {"registry_records": records}}
    st = {
        "restored_state_id": "R",
        "frozen_artifact_id": "F",
        "frozen_artifact_sha256": artifact_sha256(art),
        "current_version_id": "V2",
        "frozen_artifact": art,
    }
    st["restored_state_sha256"] = sha256_json(
        {k: v for k, v in st.items() if k != "restored_state_sha256"})
    return st


# --- FINDING 1: silent candidates[0] ---------------------------------------
def test_f1_ambiguous_translation_never_silent():
    st = _verified_state({
        "A": _rec("A", "LATIN", "BANK", meaning=["money"]),
        "B": _rec("B", "CYRILLIC", "БАНКА", meaning=["money"]),
        "C": _rec("C", "CYRILLIC", "БРЕГ", meaning=["river edge"]),
    })
    r = lookup_translation_from_frozen_registry(st, "BANK", "CYRILLIC")
    assert r["status"] == "AMBIGUOUS_NO_SILENT_PICK", \
        f"silent pick happened: {r['status']} -> {r.get('translation_packet') and r['translation_packet']['target_visible_symbol']}"
    assert r["translation_packet"] is None


# --- FINDING 2: NFC/NFD equivalence in query and translation ---------------
def test_f2_nfd_query_matches_nfc_record():
    nfc_word = unicodedata.normalize("NFC", "ЌЕРКА")
    nfd_word = unicodedata.normalize("NFD", "ЌЕРКА")
    assert nfc_word != nfd_word  # fixture sanity: really different byte sequences
    st = _verified_state({"MK": _rec("MK", "CYRILLIC", nfc_word)})
    assert query_restored_registry(st, nfd_word)["found"] is True


def test_f2_nfd_translation_source_resolves():
    nfc_word = unicodedata.normalize("NFC", "ЌЕРКА")
    nfd_word = unicodedata.normalize("NFD", "ЌЕРКА")
    st = _verified_state({
        "MK": _rec("MK", "CYRILLIC", nfc_word, role="X"),
        "LA": _rec("LA", "LATIN", "KERKA", role="X"),
    })
    r = lookup_translation_from_frozen_registry(st, nfd_word, "LATIN")
    assert r["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY"
    assert r["translation_packet"]["target_visible_symbol"] == "KERKA"


# --- FINDING 3: tampered frozen state must not be served --------------------
def test_f3_direct_write_to_frozen_state_blocks_queries():
    st = _verified_state({"MK": _rec("MK", "CYRILLIC", "ИЗВОР")})
    # attacker writes directly into the frozen structure
    st["frozen_artifact"]["frozen_registry_snapshot"]["registry_records"]["MK"]["visible_symbol"] = "TAMPERED"
    r = query_restored_registry(st, "TAMPERED")
    assert r["found"] is False
    assert r.get("status") == "INTEGRITY_CHECK_FAILED", \
        "tampered state was served without integrity gating"


def test_f3_direct_write_blocks_translation():
    st = _verified_state({
        "MK": _rec("MK", "CYRILLIC", "ИЗВОР", role="X"),
        "LA": _rec("LA", "LATIN", "SOURCE", role="X"),
    })
    st["frozen_artifact"]["frozen_registry_snapshot"]["registry_records"]["LA"]["visible_symbol"] = "FORGED"
    r = lookup_translation_from_frozen_registry(st, "ИЗВОР", "LATIN")
    assert r.get("status") == "INTEGRITY_CHECK_FAILED"
    assert r["translation_packet"] is None


# --- FINDING 4: registry_history fallback must be fail-closed ---------------
def test_f4_history_fallback_records_never_served():
    st = _verified_state({})  # artifact present, zero records
    st["registry_history"] = {
        "current_version_id": "V2",
        "versions": {"V2": {"snapshot_id": "S1"}},
        "snapshots": {"S1": {"registry_records": {"INJECTED": _rec("INJECTED", "LATIN", "INJECTED")}}},
    }
    r = query_restored_registry(st, "INJECTED")
    assert r["found"] is False, "record from un-hashed registry_history was served"


def test_f4_history_fallback_translation_blocked():
    st = _verified_state({})
    st["registry_history"] = {
        "current_version_id": "V2",
        "versions": {"V2": {"snapshot_id": "S1"}},
        "snapshots": {"S1": {"registry_records": {
            "INJ": _rec("INJ", "LATIN", "INJ", role="X"),
            "INJ2": _rec("INJ2", "HANZI", "源", role="X"),
        }}},
    }
    r = lookup_translation_from_frozen_registry(st, "INJ", "HANZI")
    assert r["status"] != "TRANSLATED_FROM_FROZEN_REGISTRY"
    assert r["translation_packet"] is None
