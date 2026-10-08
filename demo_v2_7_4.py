"""
EIT Program Lang V2.7.4 — Demo
RestoredRegistryQueryRuntimeTest

Simulates the V2.7.4 program chain:

IMPORT_RELEASE_ARCHIVE ... AS imported_archive
RESTORE_FROZEN_REGISTRY imported_archive AS restored_registry
VERIFY_RESTORED_REGISTRY ...
BUILD_RESTORED_REGISTRY_INDEX restored_registry AS restored_index
QUERY_RESTORED_REGISTRY restored_registry SOURCE AS source_query
TRANSLATE_FROM_RESTORED_REGISTRY restored_registry SOURCE TO CYRILLIC AS source_cyrillic
CHECK_FROZEN_MUTATION restored_registry VERSION 2.x AS mutation_check_same_version
EXPORT_RESTORED_QUERY_RECEIPT restored_registry
"""

import hashlib
import json
import zipfile
from pathlib import Path

from eit_program_lang.restored_registry_index import (
    build_restored_registry_index,
    extract_records_from_restored_state,
    sha256_json,
)
from eit_program_lang.restored_registry_query import query_restored_registry
from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.restored_query_receipt import build_restored_query_receipt
from eit_program_lang.mutation_guard import check_frozen_mutation

DIST = Path(__file__).parent / "dist"
DIST.mkdir(exist_ok=True)


def make_frozen_artifact():
    return {
        "artifact_type": "EIT_FROZEN_REGISTRY_ARTIFACT",
        "frozen_artifact_id": "FROZEN-REGISTRY-V2",
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
        },
    }


def main():
    print("=" * 64)
    print("EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4")
    print("RESTORED_REGISTRY_QUERY_RUNTIME — demo run")
    print("=" * 64)

    # --- IMPORT_RELEASE_ARCHIVE (build + import a frozen zip archive) ---
    artifact = make_frozen_artifact()
    artifact_sha = hashlib.sha256(
        json.dumps(artifact, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    archive_path = DIST / "RELEASE-VERIFY-ARCHIVE.zip"
    with zipfile.ZipFile(archive_path, "w") as z:
        z.writestr("frozen_artifact.json", json.dumps(artifact, ensure_ascii=False, indent=2))
        z.writestr("frozen_artifact_sha256.txt", artifact_sha)

    with zipfile.ZipFile(archive_path) as z:
        imported_artifact = json.loads(z.read("frozen_artifact.json").decode("utf-8"))
        imported_sha = z.read("frozen_artifact_sha256.txt").decode().strip()

    print(f"\n[IMPORT_RELEASE_ARCHIVE] {archive_path.name}")
    print(f"  artifact_sha256 = {imported_sha[:32]}...")

    # --- RESTORE_FROZEN_REGISTRY ---
    restored_registry = {
        "restored_state_id": "RESTORED-FROZEN-REGISTRY-V2",
        "release_id": "RELEASE-VERIFY",
        "frozen_artifact_id": imported_artifact["frozen_artifact_id"],
        "frozen_artifact_sha256": imported_sha,
        "current_version_id": "V2",
        "frozen_artifact": imported_artifact,
    }
    restored_registry["restored_state_sha256"] = sha256_json(restored_registry)
    print(f"\n[RESTORE_FROZEN_REGISTRY] restored_state_id = {restored_registry['restored_state_id']}")
    print(f"  restored_state_sha256 = {restored_registry['restored_state_sha256'][:32]}...")

    # --- VERIFY_RESTORED_REGISTRY ---
    recomputed = hashlib.sha256(
        json.dumps(imported_artifact, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    verify_ok = recomputed == restored_registry["frozen_artifact_sha256"]
    print(f"\n[VERIFY_RESTORED_REGISTRY] verified = {verify_ok}")
    assert verify_ok

    # --- BUILD_RESTORED_REGISTRY_INDEX ---
    restored_index = build_restored_registry_index(restored_registry)
    print(f"\n[BUILD_RESTORED_REGISTRY_INDEX] records = {restored_index['record_count']}")
    print(f"  index_sha256 = {restored_index['index_sha256'][:32]}...")

    # --- QUERY_RESTORED_REGISTRY ---
    source_query = query_restored_registry(restored_registry, "SOURCE")
    print(f"\n[QUERY_RESTORED_REGISTRY] query=SOURCE mode={source_query['mode']} "
          f"found={source_query['found']} matches={source_query['match_count']}")

    # --- TRANSLATE_FROM_RESTORED_REGISTRY ---
    source_cyrillic = lookup_translation_from_frozen_registry(
        restored_registry, source_query="SOURCE", target_script_family="CYRILLIC",
    )
    packet = source_cyrillic["translation_packet"]
    print(f"\n[TRANSLATE_FROM_RESTORED_REGISTRY] SOURCE -> CYRILLIC")
    print(f"  status  = {source_cyrillic['status']}")
    print(f"  result  = {packet['source_visible_symbol']} -> {packet['target_visible_symbol']}")
    print(f"  provenance (frozen_artifact_sha256) = {packet['frozen_artifact_sha256'][:32]}...")

    # --- CHECK_FROZEN_MUTATION (must be denied) ---
    mutation_check = check_frozen_mutation(restored_registry, "2.x", mutation_request="UPDATE_RECORD")
    print(f"\n[CHECK_FROZEN_MUTATION] VERSION 2.x -> {mutation_check['status']}")
    print(f"  mutation_allowed = {mutation_check['mutation_allowed']}")

    # --- EXPORT_RESTORED_QUERY_RECEIPT ---
    receipt = build_restored_query_receipt(
        restored_state=restored_registry,
        query_result=source_query,
        translation_result=source_cyrillic,
    )
    receipt_path = DIST / "restored_query_receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[EXPORT_RESTORED_QUERY_RECEIPT] receipt_sha256 = {receipt['receipt_sha256'][:32]}...")
    print(f"  written -> {receipt_path}")

    print("\n" + "=" * 64)
    print("EXPECTED RESULT CHECK:")
    print(f"  restored registry index built           : {restored_index['record_count'] == 3}")
    print(f"  SOURCE query found                      : {source_query['found']}")
    print(f"  SOURCE -> CYRILLIC = ИЗВОР              : {packet['target_visible_symbol'] == 'ИЗВОР'}")
    print(f"  provenance from frozen artifact hash    : {packet['frozen_artifact_sha256'] == artifact_sha}")
    print(f"  mutation denied inside 2.x              : {not mutation_check['mutation_allowed']}")
    print(f"  query receipt generated                 : {bool(receipt['receipt_sha256'])}")
    print("=" * 64)


if __name__ == "__main__":
    main()
