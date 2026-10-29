"""F2: mutation battery — add/delete/overwrite/provenance/clear attempts."""
from eit_program_lang.deep_mutation_guard import (
    run_mutation_battery,
    registry_surface_sha256,
)


def _restored():
    return {
        "restored_state_id": "R",
        "frozen_artifact_sha256": "f" * 64,
        "current_version_id": "V2",
        "frozen_artifact": {
            "frozen_registry_snapshot": {
                "registry_records": {
                    "LATIN-SOURCE": {
                        "symbol_id": "LATIN-SOURCE",
                        "script_family": "LATIN",
                        "visible_symbol": "SOURCE",
                        "symbolic_role": "SOURCE_NODE",
                    }
                }
            }
        },
    }


def test_mutation_battery_leaves_frozen_registry_intact():
    state = _restored()
    before = registry_surface_sha256(state)
    report = run_mutation_battery(state)

    assert report["attempt_count"] == 5
    assert report["all_frozen_registry_intact"] is True
    assert report["any_mutation_applied_to_frozen"] is False
    assert registry_surface_sha256(state) == before

    # adversarial attempts were real — they WOULD alter a writable surface
    effects = {r["mutation_label"]: r["attempted_effect_on_shadow"] for r in report["results"]}
    assert effects["ADD_RECORD"] == "WOULD_ALTER_SURFACE"
    assert effects["DELETE_RECORD"] == "WOULD_ALTER_SURFACE"
    assert effects["OVERWRITE_RECORD_FIELD"] == "WOULD_ALTER_SURFACE"
    assert effects["CLEAR_ALL_RECORDS"] == "WOULD_ALTER_SURFACE"
