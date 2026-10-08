from eit_program_lang.restored_registry_query import query_restored_registry
from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.restored_query_receipt import build_restored_query_receipt


def test_restored_query_roundtrip():
    restored = {
        "restored_state_id": "RESTORED-QUERY",
        "release_id": "RELEASE",
        "frozen_artifact_id": "FROZEN",
        "frozen_artifact_sha256": "f" * 64,
        "restored_state_sha256": "s" * 64,
        "current_version_id": "V1",
        "frozen_artifact": {
            "frozen_registry_snapshot": {
                "registry_records": {
                    "LATIN-SOURCE": {
                        "symbol_id": "LATIN-SOURCE",
                        "script_family": "LATIN",
                        "visible_symbol": "SOURCE",
                        "sound_hint": "source",
                        "symbolic_role": "SOURCE_NODE",
                        "meaning_invariant": ["source", "origin"],
                        "aliases": ["origin"],
                    },
                    "CYRILLIC-ИЗВОР": {
                        "symbol_id": "CYRILLIC-ИЗВОР",
                        "script_family": "CYRILLIC",
                        "visible_symbol": "ИЗВОР",
                        "sound_hint": "izvor",
                        "symbolic_role": "SOURCE_NODE",
                        "meaning_invariant": ["source", "origin"],
                        "aliases": ["извор"],
                    },
                }
            }
        },
    }

    query = query_restored_registry(restored, "SOURCE")
    translation = lookup_translation_from_frozen_registry(
        restored,
        source_query="SOURCE",
        target_script_family="CYRILLIC",
    )

    receipt = build_restored_query_receipt(
        restored_state=restored,
        query_result=query,
        translation_result=translation,
    )

    assert query["found"] is True
    assert translation["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY"
    assert translation["translation_packet"]["target_visible_symbol"] == "ИЗВОР"
    assert receipt["receipt_type"] == "EIT_RESTORED_REGISTRY_QUERY_RECEIPT"
    assert receipt["receipt_sha256"]
    assert receipt["boundary"]["read_only_query_mode"] is True
    assert receipt["boundary"]["restored_registry_remains_frozen"] is True
    assert receipt["boundary"]["not_proof"] is True
