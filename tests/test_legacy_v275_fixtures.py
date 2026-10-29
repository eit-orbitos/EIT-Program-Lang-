"""F-5 active fixture-integrity test (spec V0.5.9 §11.1 F-5, last sentence). Written by Tasklet for RG-4 suite V1.
For every static V2.7.5 legacy fixture: exactly the keys artifact/receipt/provenance; receipt_version == "2.7.4";
stored receipt_sha256 == sha256_json(receipt without receipt_sha256); provenance names commit 2b7dd62...;
record-key identity (§6.2 row 0.10) holds for every fixture except key_id_mismatch.json.
A damaged fixture therefore cannot pass as a control."""
import json
import os

from eit_program_lang.restored_query_receipt import sha256_json

COMMIT = "2b7dd628de411b5bb421310ead16b998d61a7f54"
NAMES = ["full_translation.json", "first_pick_multi_target.json", "self_translation.json", "no_target.json",
         "no_source.json", "query_only.json", "multi_hit_query.json", "key_id_mismatch.json",
         "no_target_none_family.json"]
DIR = os.path.join(os.path.dirname(__file__), "legacy", "v275")


def test_f5_legacy_fixtures_integrity():
    present = sorted(n for n in os.listdir(DIR) if n.endswith(".json"))
    assert present == sorted(NAMES), "fixture set %r" % present
    assert not any(n.startswith("test_") or n.endswith("_test.py") for n in os.listdir(DIR))
    for n in NAMES:
        with open(os.path.join(DIR, n), encoding="utf-8") as fh:
            d = json.load(fh)
        assert set(d) == {"artifact", "receipt", "provenance"}, n
        r = d["receipt"]
        assert r["receipt_version"] == "2.7.4", n
        assert r["receipt_sha256"] == sha256_json({k: v for k, v in r.items() if k != "receipt_sha256"}), n
        assert d["provenance"].get("commit") == COMMIT, n
        recs = d["artifact"]["frozen_registry_snapshot"]["registry_records"]
        identity = all(type(v) is dict and v.get("symbol_id") == k for k, v in recs.items())
        if n == "key_id_mismatch.json":
            assert not identity, n
        else:
            assert identity, n
