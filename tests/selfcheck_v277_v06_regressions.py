"""V2.7.7 candidate REGRESSION self-checks V0.6 — RG-4 findings C-1/C-2/C-3 + builder.
Candidate code only. NOT RG-4 evidence. Exit 0 = all pass."""
import copy, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def _find(*rel):
    for base in (HERE, os.path.normpath(os.path.join(HERE, ".."))):
        p = os.path.join(base, *rel)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(os.path.join(*rel))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
v = load("v_reg", _find("eit_program_lang", "receipt_verifier_v277_candidate.py"))
B = load("b_reg", _find("eit_program_lang", "eit_v277_builder_candidate.py"))

results = []
def check(name, ok):
    results.append((name, bool(ok))); print(("PASS " if ok else "FAIL ") + name)

STATE = {"frozen_registry_snapshot": {"registry_records": {
            "alpha": {"symbol_id": "alpha", "script_family": "LATIN", "symbolic_role": "LETTER",
                      "visible_symbol": "A", "meaning_invariant": [], "aliases": ["a-hard"]},
            "beta":  {"symbol_id": "beta", "script_family": "CYRILLIC", "symbolic_role": "LETTER",
                      "visible_symbol": "\u0411", "meaning_invariant": []},
            "gamma": {"symbol_id": "gamma", "script_family": "CYRILLIC", "symbolic_role": "LETTER",
                      "visible_symbol": "\u0412", "meaning_invariant": []}}},
         "frozen_artifact_id": "ART-1"}
AH = v.artifact_sha256(STATE)  # hash of the artifact AS SUPPLIED (pure; no self-hash inside)

# C-1 regressions
r = B.run_query_with_receipt(STATE, "A", artifact_sha256=AH)
check("R1 C-1: query-only receipt verifies (translation absent)", v.verify_restored_query_receipt(r, STATE)["verified"])
r = B.build_restored_query_receipt(STATE, artifact_sha256=AH)
check("R2 C-1: neither query nor translation verifies (NC12)", v.verify_restored_query_receipt(r, STATE)["verified"])

# C-2 regression: ambiguous with one unknown candidate id
art2 = copy.deepcopy(STATE)
art2["frozen_registry_snapshot"]["registry_records"]["delta"] = {"symbol_id": "delta", "script_family": "GREEK",
    "symbolic_role": "LETTER", "visible_symbol": "\u0394", "meaning_invariant": []}
art2["frozen_registry_snapshot"]["registry_records"]["delta2"] = {"symbol_id": "delta2", "script_family": "GREEK",
    "symbolic_role": "LETTER", "visible_symbol": "\u0395", "meaning_invariant": []}
AH2 = v.artifact_sha256(art2)  # AFTER all mutations (R3 fixture-ordering fix)
amb = B.lookup_translation_from_frozen_registry(art2, "alpha", "GREEK", AH2)
check("R3a builder: genuine AMBIGUOUS over two distinct surfaces", amb["status"] == "AMBIGUOUS_NO_SILENT_PICK")
amb["ambiguous_candidates"][1]["symbol_id"] = "ghost"
rc = B.build_restored_query_receipt(art2, translation_result=amb, artifact_sha256=AH2)
res = v.verify_restored_query_receipt(rc, art2)
check("R3 C-2: unknown candidate id -> no TARGET_RESOLUTION_INCONSISTENT",
      "SYMBOL_ID_NOT_IN_ARTIFACT" in res["failures"] and "TARGET_RESOLUTION_INCONSISTENT" not in res["failures"])

# C-3 regression: scan detail truncation to 120
deep = copy.deepcopy(STATE)
d = deep["frozen_registry_snapshot"]["registry_records"]
for i in range(8):
    d["n%d" % i] = {"symbol_id": "n%d" % i, "script_family": "LATIN", "symbolic_role": "LETTER",
                   "visible_symbol": "N%d" % i, "meaning_invariant": []}
node = deep
for k in sorted(d.keys())[:6]:
    node = {"x" * 30 + k: node}
deep2 = {"frozen_registry_snapshot": {"registry_records": {"r": node}}}
r = v.verify_restored_query_receipt({"receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT",
    "receipt_version": "2.7.7", "boundary": {"read_only_query_mode": True}, "receipt_sha256": "z" * 64}, deep2)
ok = all(len(x) <= 120 for x in r["failure_details"])
check("R4 C-3: scan detail <= 120 chars", ok and r["failures"] == ["ARTIFACT_SHAPE_INVALID"])

# Builder checks
r = B.run_query_with_receipt(STATE, "A", "CYRILLIC", AH)
res = v.verify_restored_query_receipt(r, STATE)
check("R5 builder: genuine 2.7.7 query+translation verifies (NC13-like)", res["verified"] and r["module_id"].endswith("V2_7_7"))
r = B.run_query_with_receipt(STATE, "a-hard", artifact_sha256=AH)
res = v.verify_restored_query_receipt(r, STATE)
check("R8 builder: alias query + NO_MATCH translation path verifies", res["verified"])
# NC22-like: cross-family consistent rewrite on 2.7.7 base
# NC22-style: genuine SELF-translation (alpha->LATIN, unique) then consistent rewrite to a
# family with a SINGLE same-role record (GREEK/delta), hashes recomputed.
base_rc = B.run_query_with_receipt(STATE, "alpha", "LATIN", AH)
check("R5b builder: self-translation TRANSLATED", base_rc["translation_result"]["status"] == "TRANSLATED_FROM_FROZEN_REGISTRY")
STATE2 = copy.deepcopy(STATE)
STATE2["frozen_registry_snapshot"]["registry_records"]["delta"] = {"symbol_id": "delta", "script_family": "GREEK",
    "symbolic_role": "LETTER", "visible_symbol": "\u0394", "meaning_invariant": []}
AH3 = v.artifact_sha256(STATE2)
cf = B.run_query_with_receipt(STATE2, "alpha", "LATIN", AH3)
tr = cf["translation_result"]; p = tr["translation_packet"]
delta = STATE2["frozen_registry_snapshot"]["registry_records"]["delta"]
tr["target"] = copy.deepcopy(delta); p["target_symbol_id"] = "delta"
p["target_script_family"] = "GREEK"; p["target_visible_symbol"] = "\u0394"
p["packet_sha256"] = v.sha256_json({k: val for k, val in p.items() if k != "packet_sha256"})
cf["receipt_sha256"] = v.sha256_json({k: val for k, val in cf.items() if k != "receipt_sha256"})
res = v.verify_restored_query_receipt(cf, STATE2)
check("R6 builder: NC22 cross-family rewrite on 2.7.7 base verifies", res["verified"])
# N4-like: strict with correct anchor, all three stamps (2.7.7 here)
res = v.verify_restored_query_receipt(base_rc, STATE, strict_mode=True, expected_artifact_sha256=AH)
check("R7 builder: strict 2.7.7 stamp + correct anchor (ARTIFACT_ANCHORED)",
      res["verified"] and res["assurance"] == "ARTIFACT_ANCHORED")

npass = sum(1 for _, ok in results if ok)
print("\n%d/%d regression+builder checks PASS" % (npass, len(results)))
sys.exit(0 if npass == len(results) else 1)
