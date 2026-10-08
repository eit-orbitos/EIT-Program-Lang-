from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry


def test_frozen_translation_lookup():
    restored = {
        "restored_state_id": "RESTORED",
        "frozen_artifact_sha256": "f" * 64,
        "restored_state_sha256": "s" * 64,
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
                    "HANZI-SOURCE-源": {
                        "symbol_id": "HANZI-SOURCE-源",
                        "script_family": "HANZI",
                        "visible_symbol": "源",
                        "sound_hint": "yuan",
                        "symbolic_role": "SOURCE_NODE",
                        "meaning_invariant": ["source", "origin"],
                        "aliases": ["source"],
                    },
                }
            }
        },
    }

    result = lookup_translation_from_frozen_registry(
        restored_state=restored,
        source_query="SOURCE",
        target_script_family="HANZI",
    )

    assert result["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY"
    assert result["translation_packet"]["source_visible_symbol"] == "SOURCE"
    assert result["translation_packet"]["target_visible_symbol"] == "源"
    assert result["translation_packet"]["frozen_artifact_sha256"] == "f" * 64
    assert result["read_only"] is True
    assert result["safety"]["restored_registry_remains_frozen"] is True
