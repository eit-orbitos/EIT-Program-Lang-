from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.integrity_verifier import artifact_sha256
from eit_program_lang.restored_registry_index import sha256_json


def test_frozen_translation_lookup():
    art = {
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
    }
    restored = {
        "restored_state_id": "RESTORED",
        "frozen_artifact_sha256": artifact_sha256(art),
        "frozen_artifact": art,
    }
    restored["restored_state_sha256"] = sha256_json(
        {k: v for k, v in restored.items() if k != "restored_state_sha256"})

    result = lookup_translation_from_frozen_registry(
        restored_state=restored,
        source_query="SOURCE",
        target_script_family="HANZI",
    )

    assert result["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY"
    assert result["translation_packet"]["source_visible_symbol"] == "SOURCE"
    assert result["translation_packet"]["target_visible_symbol"] == "源"
    assert result["translation_packet"]["frozen_artifact_sha256"] == restored["frozen_artifact_sha256"]
    assert result["read_only"] is True
    assert result["safety"]["restored_registry_remains_frozen"] is True
