import json, sys, importlib.util, hashlib, copy
T = sys.argv[1]
spec = importlib.util.spec_from_file_location("rv", T + "/eit_program_lang/receipt_verifier.py"); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
exp = {"full_translation.json": True, "first_pick_multi_target.json": True, "self_translation.json": True, "no_target.json": True,
       "no_source.json": True, "query_only.json": True, "multi_hit_query.json": True, "no_target_none_family.json": True, "key_id_mismatch.json": False}
ok_all = True
for f, want in exp.items():
    try:
        d = json.load(open(f"{T}/tests/legacy/v275/{f}"))
    except FileNotFoundError:
        print("MISSING", f); ok_all = False; continue
    r = d["receipt"]; a = d["artifact"]
    stamp_ok = r.get("receipt_version") == "2.7.4" and r.get("receipt_sha256") == v.sha256_json({k: x for k, x in r.items() if k != "receipt_sha256"})
    res = v.verify_restored_query_receipt(r, a)
    good = (res["verified"] is want) and (want or res["failures"] == ["ARTIFACT_SHAPE_INVALID"]) and stamp_ok
    ok_all &= good
    print(("PASS" if good else "FAIL"), f, "verified=", res["verified"], res["failures"][:3], "stamp/hash ok=", stamp_ok)
# LQ1 legacy grounding: alter one field of records[0], rehash
d = json.load(open(f"{T}/tests/legacy/v275/full_translation.json")); r = copy.deepcopy(d["receipt"]); a = d["artifact"]
k = [x for x in r["query_result"]["records"][0] if x != "symbol_id"][0]; r["query_result"]["records"][0][k] = "ALTERED"
r["receipt_sha256"] = v.sha256_json({kk: x for kk, x in r.items() if kk != "receipt_sha256"}); res = v.verify_restored_query_receipt(r, a)
g = "RECORD_MISMATCH_WITH_ARTIFACT" in res["failures"] and "REQUIRED_FIELD_MISSING" not in res["failures"]; ok_all &= g
print(("PASS" if g else "FAIL"), "LQ1 legacy grounding", res["failures"])
print("LEGACY_SUMMARY", "ALL_PASS" if ok_all else "HAS_FAILURES")
