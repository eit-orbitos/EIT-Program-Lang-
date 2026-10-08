"""F3: ambiguity, Unicode normalization, conflicts, missing translations."""
import unicodedata

from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.unicode_normalization import (
    nfc,
    detect_registry_conflicts,
    resolve_ambiguous_candidates,
)


def _rec(sid, family, visible, role="SOURCE_NODE", meaning=None, aliases=None):
    return {
        "symbol_id": sid,
        "script_family": family,
        "visible_symbol": visible,
        "symbolic_role": role,
        "meaning_invariant": meaning or ["source"],
        "aliases": aliases or [],
    }


def _restored(records):
    return {
        "restored_state_id": "R",
        "frozen_artifact_sha256": "f" * 64,
        "restored_state_sha256": "s" * 64,
        "frozen_artifact": {"frozen_registry_snapshot": {"registry_records": records}},
    }


def test_unicode_nfc_equivalence():
    decomposed = "ИЗВОР"  # may arrive decomposed from external input
    assert nfc(unicodedata.normalize("NFD", decomposed)) == nfc(decomposed)


def test_missing_target_translation_fails_closed():
    state = _restored({"LATIN-SOURCE": _rec("LATIN-SOURCE", "LATIN", "SOURCE")})
    r = lookup_translation_from_frozen_registry(state, "SOURCE", "HANZI")
    assert r["status"] == "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY"
    assert r["translation_packet"] is None


def test_missing_source_fails_closed():
    state = _restored({"LATIN-SOURCE": _rec("LATIN-SOURCE", "LATIN", "SOURCE")})
    r = lookup_translation_from_frozen_registry(state, "NONEXISTENT", "HANZI")
    assert r["status"] == "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY"


def test_divergent_duplicate_surface_conflict_detected():
    state = _restored({
        "A": _rec("A", "LATIN", "BANK", role="FINANCE_NODE", meaning=["money"]),
        "B": _rec("B", "LATIN", "BANK", role="GEOGRAPHY_NODE", meaning=["river edge"]),
    })
    scan = detect_registry_conflicts(state)
    assert scan["conflict_free"] is False
    assert scan["conflicts"][0]["type"] == "DIVERGENT_DUPLICATE_SURFACE"


def test_identical_duplicate_surface_is_not_conflict():
    state = _restored({
        "A": _rec("A", "LATIN", "SOURCE"),
        "B": _rec("B", "LATIN", "SOURCE"),
    })
    assert detect_registry_conflicts(state)["conflict_free"] is True


def test_ambiguous_candidates_no_silent_pick():
    cands = [
        _rec("A", "CYRILLIC", "БАНКА", meaning=["money"]),
        _rec("B", "CYRILLIC", "БРЕГ", meaning=["river edge"]),
    ]
    r = resolve_ambiguous_candidates(cands)
    assert r["status"] == "AMBIGUOUS_NO_SILENT_PICK"
    assert r["chosen"] is None


def test_identical_surface_candidates_resolve_deterministically():
    cands = [_rec("B", "HANZI", "源"), _rec("A", "HANZI", "源")]
    r = resolve_ambiguous_candidates(cands)
    assert r["status"] == "RESOLVED_IDENTICAL_SURFACES"
    assert r["chosen"]["symbol_id"] == "A"  # deterministic by symbol_id sort


def test_zero_candidates_is_miss():
    assert resolve_ambiguous_candidates([])["status"] == "NO_CANDIDATES"
