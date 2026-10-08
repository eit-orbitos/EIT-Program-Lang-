from eit_program_lang.restored_registry_index import build_restored_registry_index


def test_restored_registry_index():
    restored = {
        "restored_state_id": "RESTORED",
        "release_id": "REL",
        "frozen_artifact_id": "FROZEN",
        "frozen_artifact_sha256": "f" * 64,
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

    index = build_restored_registry_index(restored)

    assert index["record_count"] == 2
    assert "LATIN-SOURCE" in index["symbol_id_index"]
    assert "SOURCE" in index["visible_symbol_index"]
    assert "source" in index["alias_index"]
    assert "LATIN" in index["script_family_index"]
    assert "SOURCE_NODE" in index["symbolic_role_index"]
    assert index["index_sha256"]
    assert index["safety"]["read_only_query_mode"] is True
