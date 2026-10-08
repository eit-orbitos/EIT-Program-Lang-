"""
EIT Program Lang V2.7.5 — Adversarial Validation Demo
Integrity & Adversarial Validation over the V2.7.4 query runtime.
"""

import copy
import json
from pathlib import Path

from eit_program_lang.integrity_verifier import (
    verify_frozen_artifact, verify_restored_state, artifact_sha256,
)
from eit_program_lang.deep_mutation_guard import run_mutation_battery, registry_surface_sha256
from eit_program_lang.restored_registry_query import query_restored_registry
from eit_program_lang.frozen_translation_lookup import lookup_translation_from_frozen_registry
from eit_program_lang.restored_query_receipt import build_restored_query_receipt
from eit_program_lang.receipt_verifier import verify_restored_query_receipt
from eit_program_lang.unicode_normalization import detect_registry_conflicts
from eit_program_lang.integration_boundary import integration_boundary_report
from eit_program_lang.restored_registry_index import sha256_json

DIST = Path(__file__).parent / "dist"
DIST.mkdir(exist_ok=True)

ARTIFACT = {
    "frozen_artifact_id": "FROZEN-REGISTRY-V2",
    "frozen_registry_snapshot": {
        "registry_records": {
            "LATIN-SOURCE": {
                "symbol_id": "LATIN-SOURCE", "script_family": "LATIN",
                "visible_symbol": "SOURCE", "sound_hint": "source",
                "symbolic_role": "SOURCE_NODE",
                "meaning_invariant": ["source", "origin"], "aliases": ["origin"],
            },
            "CYRILLIC-ИЗВОР": {
                "symbol_id": "CYRILLIC-ИЗВОР", "script_family": "CYRILLIC",
                "visible_symbol": "ИЗВОР", "sound_hint": "izvor",
                "symbolic_role": "SOURCE_NODE",
                "meaning_invariant": ["source", "origin"], "aliases": ["извор"],
            },
        }
    },
}

restored = {
    "restored_state_id": "RESTORED-V2",
    "release_id": "RELEASE-VERIFY",
    "frozen_artifact_id": "FROZEN-REGISTRY-V2",
    "frozen_artifact_sha256": artifact_sha256(ARTIFACT),
    "current_version_id": "V2",
    "frozen_artifact": ARTIFACT,
}
restored["restored_state_sha256"] = sha256_json(
    {k: v for k, v in restored.items() if k != "restored_state_sha256"}
)

print("=" * 66)
print("EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_5")
print("INTEGRITY & ADVERSARIAL VALIDATION — demo run")
print("=" * 66)

# --- F1: integrity ---
clean = verify_restored_state(restored)
print(f"\n[F1] clean restored state verified      : {clean['verified']}")

tampered = copy.deepcopy(ARTIFACT)
tampered["frozen_registry_snapshot"]["registry_records"]["LATIN-SOURCE"]["visible_symbol"] = "EVIL"
t = verify_frozen_artifact(tampered, artifact_sha256(ARTIFACT))
print(f"[F1] tampered artifact detected         : {not t['verified']}  {t['failures']}")

bad_hash = verify_frozen_artifact(ARTIFACT, "0" * 64)
print(f"[F1] wrong hash detected                : {not bad_hash['verified']}")

# --- F2: mutation battery ---
before = registry_surface_sha256(restored)
battery = run_mutation_battery(restored)
print(f"\n[F2] mutation battery attempts          : {battery['attempt_count']}")
print(f"[F2] frozen registry intact after all   : {battery['all_frozen_registry_intact']}")
print(f"[F2] surface hash unchanged             : {registry_surface_sha256(restored) == before}")

# --- F3: translation edge cases ---
conflicts = detect_registry_conflicts(restored)
print(f"\n[F3] conflict scan on clean registry    : conflict_free={conflicts['conflict_free']}")
missing = lookup_translation_from_frozen_registry(restored, "SOURCE", "HANZI")
print(f"[F3] missing target fails closed        : {missing['status']}")

# --- F4: receipt verification ---
q = query_restored_registry(restored, "SOURCE")
tr = lookup_translation_from_frozen_registry(restored, "SOURCE", "CYRILLIC")
receipt = build_restored_query_receipt(restored, q, tr)
v = verify_restored_query_receipt(receipt, source_frozen_artifact=ARTIFACT)
print(f"\n[F4] valid receipt verifies             : {v['verified']}")

forged = copy.deepcopy(receipt)
forged["query_result"]["found"] = False
fv = verify_restored_query_receipt(forged, source_frozen_artifact=ARTIFACT)
print(f"[F4] tampered receipt detected          : {not fv['verified']}  {fv['failures']}")

# --- F5: integration boundary ---
ib = integration_boundary_report()
print(f"\n[F5] CA-Lang / 11D / IFIM / ASI_OS       : "
      f"{ib['boundary']['ca_lang_integration']} (declared, not implied)")

report = {
    "module_id": "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_5",
    "upgrade_type": "INTEGRITY_ADVERSARIAL_VALIDATION",
    "f1_clean_verify": clean["verified"],
    "f1_tamper_detected": not t["verified"] and not bad_hash["verified"],
    "f2_battery_intact": battery["all_frozen_registry_intact"],
    "f3_conflict_scan_clean": conflicts["conflict_free"],
    "f3_missing_target_fail_closed": missing["status"] == "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
    "f4_receipt_verifies": v["verified"],
    "f4_forgery_detected": not fv["verified"],
    "f5_boundary_declared": True,
}
out = DIST / "adversarial_validation_report.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

print("\n" + "=" * 66)
print("ADVERSARIAL REPORT:", json.dumps(report, indent=2))
print(f"written -> {out}")
print("=" * 66)
