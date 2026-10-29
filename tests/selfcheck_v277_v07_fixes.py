"""V2.7.7 candidate FIX self-checks V0.7 — RG-5 findings F1..F5 regressions.
Candidate code only. NOT RG-4 evidence. Exit 0 = all pass."""
import copy, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def _find(*rel):
    for base in (HERE, os.path.normpath(os.path.join(HERE, ".."))):
        p = os.path.join(base, *rel)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(os.path.join(*rel))
spec = importlib.util.spec_from_file_location("v_fix", _find("eit_program_lang", "receipt_verifier_v277_candidate.py"))
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
B_spec = importlib.util.spec_from_file_location("b_fix", _find("eit_program_lang", "eit_v277_builder_candidate.py"))
B = importlib.util.module_from_spec(B_spec); B_spec.loader.exec_module(B)

results = []
def check(name, ok):
    results.append((name, bool(ok))); print(("PASS " if ok else "FAIL ") + name)

STATE = {"frozen_registry_snapshot": {"registry_records": {
            "alpha": {"symbol_id": "alpha", "script_family": "LATIN", "symbolic_role": "LETTER",
                      "visible_symbol": "A", "meaning_invariant": []},
            "beta":  {"symbol_id": "beta", "script_family": "CYRILLIC", "symbolic_role": "LETTER",
                      "visible_symbol": "\u0411", "meaning_invariant": []}}},
         "frozen_artifact_id": "ART-1"}
AH = v.artifact_sha256(STATE)

# F1: hostile colliding key; no exception escapes; hostile never called; single L0 failure; hash None
class Hostile:
    def __init__(self):
        self.flag = False; self.armed = False
    def __hash__(self):
        return hash("receipt_sha256")
    def __eq__(self, other):
        if self.armed:
            self.flag = True
            raise RuntimeError("hostile __eq__ called")
        return False
    def __str__(self): return "H"
    def __repr__(self): return "H"

h = Hostile()
bad = {h: "v", "receipt_version": "2.7.7"}
h.armed = True
try:
    r = v.verify_restored_query_receipt(bad, STATE)
    escaped = None
except Exception as ex:
    escaped = repr(ex)
h.armed = False
check("F1a no exception escapes (0.3 path)", escaped is None)
check("F1b hostile never called", h.flag is False)
check("F1c exactly one L0 failure", r["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"] and r["layers"]["L0"] == "FAIL")
check("F1d L0 result receipt_sha256 is None", r["receipt_sha256"] is None)
for kw, code in (({"strict_mode": "x"}, "STRICT_MODE_NOT_BOOL"),
                 ({"expected_artifact_sha256": "bad"}, "EXPECTED_ANCHOR_MALFORMED"),
                 ({"expected_restored_state_sha256": "bad"}, "EXPECTED_ANCHOR_MALFORMED")):
    h2 = Hostile(); h2.armed = True
    bad2 = {h2: "v"}
    try:
        r2 = v.verify_restored_query_receipt(bad2, STATE, **kw)
        esc2 = None
    except Exception as ex:
        esc2 = repr(ex)
    h2.armed = False
    check("F1 %s path: no exception, one failure" % code, esc2 is None and r2["failures"] == [code]
          and r2["receipt_sha256"] is None and h2.flag is False)

# F2: non-hex 64-char -> MISMATCH (not MALFORMED)
base = B.run_query_with_receipt(STATE, "A", "CYRILLIC", AH)
for tag, val in (("upper", base["receipt_sha256"].upper()), ("x64", "x" * 64)):
    rc = copy.deepcopy(base); rc["receipt_sha256"] = val
    res = v.verify_restored_query_receipt(rc, STATE)
    check("F2 %s: MISMATCH present, MALFORMED absent" % tag,
          "RECEIPT_HASH_MISMATCH_TAMPER_DETECTED" in res["failures"]
          and "RECEIPT_HASH_MALFORMED" not in res["failures"])

# F3: found missing + bad symbol_ids -> [RFM(found), CFI(symbol_ids)]
rc = B.run_query_with_receipt(STATE, "A", artifact_sha256=AH)
del rc["query_result"]["found"]
rc["query_result"]["symbol_ids"] = ["beta"]
rc["receipt_sha256"] = v.sha256_json({k: val for k, val in rc.items() if k != "receipt_sha256"})
res = v.verify_restored_query_receipt(rc, STATE)
check("F3 exact [RFM(found), CFI(symbol_ids)]",
      res["failures"] == ["REQUIRED_FIELD_MISSING", "CROSS_FIELD_INCONSISTENT"]
      and res["failure_details"] == ["query_result.found", "query_result.symbol_ids"])

# F4: G-3 order — two-line forgery emits target_script_family BEFORE source_visible_symbol
rc = B.run_query_with_receipt(STATE, "A", "CYRILLIC", AH)
p = rc["translation_result"]["translation_packet"]
p["target_script_family"] = "FORGED_T"; p["source_visible_symbol"] = "FORGED_S"
p["packet_sha256"] = v.sha256_json({k: val for k, val in p.items() if k != "packet_sha256"})
rc["receipt_sha256"] = v.sha256_json({k: val for k, val in rc.items() if k != "receipt_sha256"})
res = v.verify_restored_query_receipt(rc, STATE)
check("F4 G-3 written order",
      res["failures"] == ["RECORD_MISMATCH_WITH_ARTIFACT", "RECORD_MISMATCH_WITH_ARTIFACT"]
      and res["failure_details"] == ["translation_packet.target_script_family",
                                     "translation_packet.source_visible_symbol"])

# F5: strict mode, packet_version deleted -> POLICY_RECEIPT_VERSION_NOT_ALLOWED
rc = B.run_query_with_receipt(STATE, "A", "CYRILLIC", AH)
del rc["translation_result"]["translation_packet"]["packet_version"]
rc["translation_result"]["translation_packet"]["packet_sha256"] = v.sha256_json(
    {k: val for k, val in rc["translation_result"]["translation_packet"].items() if k != "packet_sha256"})
rc["receipt_sha256"] = v.sha256_json({k: val for k, val in rc.items() if k != "receipt_sha256"})
res = v.verify_restored_query_receipt(rc, STATE, strict_mode=True, expected_artifact_sha256=AH)
check("F5 missing packet_version in strict mode -> POLICY code",
      "POLICY_RECEIPT_VERSION_NOT_ALLOWED" in res["failures"] and not res["verified"])

npass = sum(1 for _, ok in results if ok)
print("\n%d/%d fix checks PASS" % (npass, len(results)))
sys.exit(0 if npass == len(results) else 1)
