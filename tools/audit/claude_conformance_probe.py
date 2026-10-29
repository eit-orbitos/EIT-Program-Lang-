"""Claude independent black-box conformance probe for P0-03 V0.5.9 (sha 3fc10557...).

Written by Claude from the SPEC TEXT, not from the candidate's tests. Read-only: the candidate tree
is never modified. Each row id refers to §11.3 / §11.4 (or a § clause). Output: one line per row,
PASS / FAIL / HARNESS_ERROR, then a JSON summary on the last line.
Usage: python3 claude_conformance_probe.py <successor_tree>
"""
import copy, hashlib, importlib.util, json, re, sys, platform, unicodedata

TREE = sys.argv[1]
spec = importlib.util.spec_from_file_location("rv_probe", TREE + "/eit_program_lang/receipt_verifier.py")
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
spec2 = importlib.util.spec_from_file_location("rqr_probe", TREE + "/eit_program_lang/restored_query_receipt.py")
V = v.verify_restored_query_receipt
results = []

def row(rid, ok, note=""):
    results.append((rid, "PASS" if ok else "FAIL", note))
    print(f"{'PASS' if ok else 'FAIL'}  {rid}  {note}")

def guarded(rid, fn):
    try:
        fn()
    except Exception as e:  # any escape is a verifier defect (S-4) or harness error
        results.append((rid, "EXCEPTION", repr(e)[:160])); print(f"EXCEPTION  {rid}  {e!r}"[:200])

def sj(d):  # independent re-statement of §2.1
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str).encode()).hexdigest()
def ah(a):  # §2.2
    return hashlib.sha256(json.dumps(a, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def rehash(r, packet=True):
    tr = r.get("translation_result")
    if packet and isinstance(tr, dict) and isinstance(tr.get("translation_packet"), dict) and "packet_sha256" in tr["translation_packet"]:
        p = tr["translation_packet"]; p["packet_sha256"] = sj({k: x for k, x in p.items() if k != "packet_sha256"})
    r["receipt_sha256"] = sj({k: x for k, x in r.items() if k != "receipt_sha256"})
    return r

REC = {
    "a1": {"symbol_id": "a1", "script_family": "LATIN", "symbolic_role": "LETTER", "visible_symbol": "A", "meaning_invariant": ["m"]},
    "c1": {"symbol_id": "c1", "script_family": "CYRILLIC", "symbolic_role": "LETTER", "visible_symbol": "А", "meaning_invariant": []},
    "c2": {"symbol_id": "c2", "script_family": "CYRILLIC", "symbolic_role": "DIGIT", "visible_symbol": "1", "meaning_invariant": []},
    "g1": {"symbol_id": "g1", "script_family": "GREEK", "symbolic_role": "LETTER", "visible_symbol": "Α", "meaning_invariant": []},
    "g2": {"symbol_id": "g2", "script_family": "GREEK", "symbolic_role": "LETTER", "visible_symbol": "Β", "meaning_invariant": []},
}
STATE = "e" * 64

def artifact():
    return {"frozen_registry_snapshot": {"registry_records": copy.deepcopy(REC)}, "frozen_artifact_id": "ART-X"}

def translated(art, src="a1", tgt="c1"):
    R = art["frozen_registry_snapshot"]["registry_records"]; A = ah(art); S, G = R[src], R[tgt]
    p = {"source_symbol_id": src, "target_symbol_id": tgt, "source_script_family": S["script_family"],
         "target_script_family": G["script_family"], "source_visible_symbol": S["visible_symbol"],
         "target_visible_symbol": G["visible_symbol"], "symbolic_role": S["symbolic_role"].upper(),
         "meaning_invariant": S.get("meaning_invariant", []), "frozen_artifact_sha256": A,
         "restored_state_sha256": STATE, "packet_version": "2.7.7", "packet_sha256": None}
    return {"status": "TRANSLATED_FROM_FROZEN_REGISTRY", "source": copy.deepcopy(S), "target": copy.deepcopy(G),
            "frozen_artifact_sha256": A, "restored_state_sha256": STATE, "translation_packet": p}

def receipt(art, qr=None, tr=None, stamp="2.7.7"):
    A = ah(art); R = art["frozen_registry_snapshot"]["registry_records"]
    if qr is None:
        qr = {"status": "OK", "found": True, "match_count": 1, "symbol_ids": ["a1"], "records": [copy.deepcopy(R["a1"])], "frozen_artifact_sha256": A}
    if tr is None:
        tr = translated(art)
    r = {"receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT", "receipt_version": stamp,
         "module_id": "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V" + stamp.replace(".", "_"),
         "generated_at_utc": "2026-10-29T12:00:00+00:00",
         "boundary": {"read_only_query_mode": True, "restored_registry_remains_frozen": True,
                      "mutation_guard_enforced": True, "real_world_control": False},
         "frozen_artifact_sha256": A, "frozen_artifact_id": "ART-X", "restored_state_sha256": STATE,
         "query_result": qr, "translation_result": tr}
    return rehash(r)

def genuine():
    a = artifact(); return a, receipt(a)

# ---------------------------------------------------------------- API / contract
def api():
    a, r = genuine(); snap = copy.deepcopy(a); res = V(r, a)
    row("NC1/NC13 genuine verifies, default mode", res["verified"] and res["failures"] == [], str(res["failures"]))
    row("§4.2 result keys", set(res) >= {"check_type", "verified", "failures", "receipt_sha256", "safety", "failure_details", "layers", "assurance"})
    row("§4.2 layers keys", set(res["layers"]) == {"L0", "L1", "L2", "L3_BINDING", "L3_ANCHOR", "L3_STATE", "L4"})
    row("NC13/N5 layers+assurance default", res["layers"]["L3_ANCHOR"] == "NOT_EVALUATED" and res["layers"]["L3_STATE"] == "NOT_EVALUATED" and res["layers"]["L2"] == "PASS" and res["assurance"] == "CONSISTENCY_ONLY", f"{res['layers']} {res['assurance']}")
    row("Z1 artifact not mutated", a == snap)
    doc = re.sub(r"\s+", " ", V.__doc__ or "")
    want = "The verifier cannot enforce that expected hashes were obtained from a trustworthy independent channel. If the caller computes an expected hash from the untrusted artifact being verified, an `ARTIFACT_ANCHORED` assurance label does not establish independent provenance or producer authenticity."
    row("§4.5 docstring verbatim", want in doc)
    row("§10.3 allow-list constant tuple", isinstance(v.ALLOW_LIST, tuple) and set(v.ALLOW_LIST) == {("2.7.4", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4"), ("2.7.6", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_6"), ("2.7.7", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7")})
    # §2 'MUST call existing functions, MUST NOT reimplement': check equivalence and provenance
    import importlib
    s2 = importlib.util.spec_from_file_location("rqr", TREE + "/eit_program_lang/restored_query_receipt.py")
    try:
        m = importlib.util.module_from_spec(s2); s2.loader.exec_module(m); orig = m.sha256_json
    except Exception:
        orig = None
    samples = [r, {"x": [1, 2.5, None, True, "é"]}, a]
    eq = orig is not None and all(orig(s) == v.sha256_json(s) for s in samples)
    row("§2.1 sha256_json equivalent to restored_query_receipt.sha256_json", eq)
    row("§2 MUST call existing function (not reimplement)", orig is not None and v.sha256_json is orig, "verifier defines its own copy" if orig is not None and v.sha256_json is not orig else "")
    res2 = V(copy.deepcopy(r), copy.deepcopy(a)); row("P-4 determinism (same input twice)", res2 == V(copy.deepcopy(r), copy.deepcopy(a)))
    a2, r2 = genuine(); res = V(r2, a2, expected_artifact_sha256=ah(a2), expected_restored_state_sha256=STATE)
    row("assurance ARTIFACT_AND_STATE_ANCHORED", res["verified"] and res["assurance"] == "ARTIFACT_AND_STATE_ANCHORED", res["assurance"])
    res = V(r2, a2, expected_artifact_sha256=ah(a2), strict_mode=True)
    row("N4 strict + anchor (2.7.7) -> ARTIFACT_ANCHORED", res["verified"] and res["assurance"] == "ARTIFACT_ANCHORED", str(res["failures"]))

# ---------------------------------------------------------------- L0
def l0():
    a, r = genuine()
    for bad in ("False", "True", 0, 1, None, []):
        res = V(r, a, strict_mode=bad)
        row(f"SM1 strict_mode={bad!r}", res["failures"] == ["STRICT_MODE_NOT_BOOL"] and res["failure_details"] == ["strict_mode"])
    class B:
        flag = False
        def __bool__(self): B.flag = True; return True
    res = V(r, a, strict_mode=B()); row("SM1 custom __bool__ not called", res["failures"] == ["STRICT_MODE_NOT_BOOL"] and not B.flag)
    rr = copy.deepcopy(r); rr["x"] = (1,)
    res = V(rr, a, expected_artifact_sha256="zz", strict_mode="x"); row("SM2 strict first", res["failures"] == ["STRICT_MODE_NOT_BOOL"])
    res = V(rr, a, expected_artifact_sha256="zz"); row("T6/N6 malformed anchor first", res["failures"] == ["EXPECTED_ANCHOR_MALFORMED"] and res["failure_details"] == ["expected_artifact_sha256"])
    res = V(None, a); row("S1/T1r receipt None", res["failures"] == ["RECEIPT_SHAPE_INVALID"] and res["layers"]["L0"] == "FAIL")
    res = V(r, "str"); row("S1 artifact str", res["failures"] == ["ARTIFACT_SHAPE_INVALID"])
    for name, mut in [("translation_result=[1]", lambda x: x.__setitem__("translation_result", [1])),
                      ("query_result='x'", lambda x: x.__setitem__("query_result", "x")),
                      ("boundary None (B1)", lambda x: x.__setitem__("boundary", None))]:
        rr = copy.deepcopy(r); mut(rr); res = V(rr, a); row(f"S1 {name}", res["failures"] == ["RECEIPT_SHAPE_INVALID"])
    aa = artifact(); aa["frozen_registry_snapshot"]["registry_records"] = []
    res = V(r, aa); row("S1 records map a list", res["failures"] == ["ARTIFACT_SHAPE_INVALID"])
    class Sub(dict): pass
    class IS(int): pass
    class SS(str): pass
    for tname, val in [("tuple", (1,)), ("set", {1}), ("bytes", b"x"), ("object", object()), ("dict-sub", Sub()), ("int-sub", IS(1)), ("str-sub", SS("x"))]:
        rr = copy.deepcopy(r); rr["extra"] = val; res = V(rr, a)
        ok1 = res["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"] and res["layers"]["L0"] == "FAIL"
        aa = artifact(); aa["frozen_registry_snapshot"]["registry_records"]["a1"]["x"] = val; res2 = V(r, aa)
        row(f"T1 {tname} in receipt and in record", ok1 and res2["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"])
    rr = copy.deepcopy(r); rr[1] = "k"; res = V(rr, a); row("T2 non-str key receipt root", res["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"])
    deep = cur = {}
    for _ in range(33):
        cur["k"] = {}; cur = cur["k"]
    rr = copy.deepcopy(r); rr["deep"] = deep; res = V(rr, a); row("T3 33-level nesting", res["failures"] == ["RECEIPT_SHAPE_INVALID"])
    cyc = {}; cyc["self"] = cyc; rr = copy.deepcopy(r); rr["cyc"] = cyc; res = V(rr, a); row("T3 cyclic value", res["failures"] == ["RECEIPT_SHAPE_INVALID"])
    # T4 hostile key colliding with 'frozen_registry_snapshot', armed after construction (T-7)
    class H:
        armed = False; touched = False
        def __hash__(self):
            if H.armed: H.touched = True; raise RuntimeError("hash")
            return hash("frozen_registry_snapshot")
        def __eq__(self, o):
            if H.armed: H.touched = True; raise RuntimeError("eq")
            return False
        def __str__(self):
            if H.armed: H.touched = True; raise RuntimeError("str")
            return "H"
        __repr__ = __str__
    aa = artifact(); aa[H()] = 1; H.armed = True
    res = V(r, aa); H.armed = False
    row("T4 hostile colliding key: rejected, no method called", res["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"] and not H.touched)
    for kind, val in [("str", "x"), ("list", []), ("None", None)]:
        aa = artifact(); aa["frozen_registry_snapshot"]["registry_records"]["zz"] = val; res = V(r, aa)
        row(f"T5 record is {kind}", res["failures"] == ["ARTIFACT_SHAPE_INVALID"])
    for label, val in [("2**63", 2**63), ("-2**63-1", -2**63 - 1), ("10**4300", 10**4300), ("[10**4300]", [10**4300])]:
        rr = copy.deepcopy(r); rr["translation_result"] = {"status": "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY", "source_symbol_id": "a1", "symbolic_role": "LETTER", "target_script_family": val, "frozen_artifact_sha256": ah(a), "translation_packet": None}
        try:
            res = V(rr, a); ok = res["failures"] == ["RECEIPT_SHAPE_INVALID"] and res["layers"]["L0"] == "FAIL" and re.fullmatch(r"receipt:depth=\d+:path=[\d.]+", res["failure_details"][0]) is not None
        except Exception as e:
            ok = False
        row(f"BI1 int {label}", ok)
    aa = artifact(); aa["big"] = 2**63; res = V(r, aa); row("BI2 int in artifact", res["failures"] == ["ARTIFACT_SHAPE_INVALID"])
    rr = copy.deepcopy(r); rr["extra"] = [2**63 - 1, -2**63, True, False, 0]; rehash(rr); res = V(rr, a)
    row("BI3 boundary ints accepted", res["verified"], str(res["failures"]))
    rr = copy.deepcopy(r); rr["a_first"] = 2**63; rr["b_second"] = (1,); res = V(rr, a); row("BI4 range first by scan order", res["failures"] == ["RECEIPT_SHAPE_INVALID"])
    rr = copy.deepcopy(r); rr["a_first"] = (1,); rr["b_second"] = 2**63; res = V(rr, a); row("BI4 type first by scan order", res["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"])
    # D4(i): non-str key as 2nd iterated key of receipt root
    rr = {}; it = iter(r.items()); k0, v0 = next(it); rr[k0] = v0; rr[7] = "x"
    for k, x in it: rr[k] = x
    res = V(rr, a); row("D4(i) detail receipt:depth=1:path=1", res["failure_details"] == ["receipt:depth=1:path=1"], str(res["failure_details"]))
    # RT1 integer-conversion limit independence
    import sys as _s
    old = _s.get_int_max_str_digits(); outs = []
    for lim in (0, 640, 4300):
        _s.set_int_max_str_digits(lim); outs.append(json.dumps(V(copy.deepcopy(r), copy.deepcopy(a)), sort_keys=True, default=str))
    _s.set_int_max_str_digits(old)
    row("RT1 results independent of int_max_str_digits", len(set(outs)) == 1 and _s.get_int_max_str_digits() == old)

# ---------------------------------------------------------------- L1 / L3 / L2 / L4
def later():
    a, r = genuine()
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["source_symbol_id"] = "nope"; rr["translation_result"]["translation_packet"]["target_symbol_id"] = "nope2"; rehash(rr, packet=False)
    res = V(rr, a); row("A stale packet hash + unknown ids", "PACKET_HASH_MISMATCH_TAMPER_DETECTED" in res["failures"] and "SYMBOL_ID_NOT_IN_ARTIFACT" in res["failures"])
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["source_symbol_id"] = "nope"; rehash(rr)
    res = V(rr, a); row("B unknown packet id", "SYMBOL_ID_NOT_IN_ARTIFACT" in res["failures"])
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["source_symbol_id"] = "g1"; rehash(rr)
    res = V(rr, a); row("C1/D2 X.5 detail record side", ("CROSS_FIELD_INCONSISTENT", "translation_result.source.symbol_id") in zip(res["failures"], res["failure_details"]))
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["target_visible_symbol"] = "Z"; rehash(rr)
    res = V(rr, a); row("C2 RECORD_MISMATCH_WITH_ARTIFACT", "RECORD_MISMATCH_WITH_ARTIFACT" in res["failures"])
    rr = copy.deepcopy(r); rr["query_result"]["symbol_ids"] = ["c1"]; rehash(rr)
    res = V(rr, a); row("C3 symbol_ids vs records", "CROSS_FIELD_INCONSISTENT" in res["failures"])
    for label, val in [("True", True), ("1.0", 1.0)]:
        aa = artifact(); aa["frozen_registry_snapshot"]["registry_records"]["a1"]["n"] = 1
        rr = receipt(aa); rr["query_result"]["records"][0]["n"] = val; rehash(rr)
        res = V(rr, aa); row(f"E1 1 -> {label}", "RECORD_MISMATCH_WITH_ARTIFACT" in res["failures"])
    rr = copy.deepcopy(r); rr["query_result"]["match_count"] = 2; rr["query_result"]["found"] = False; rehash(rr)
    res = V(rr, a); row("D1 exact two failures + details", [f for f in res["failures"]] == ["CROSS_FIELD_INCONSISTENT"] * 2 and res["failure_details"] == ["query_result.match_count", "query_result.found"], str(list(zip(res["failures"], res["failure_details"]))))
    # R1 real target of other role (c2 DIGIT), consistent
    aa = artifact(); rr = receipt(aa, tr=translated(aa, "a1", "c2")); res = V(rr, aa)
    row("R1 other-role target -> TARGET_RESOLUTION_INCONSISTENT", "TARGET_RESOLUTION_INCONSISTENT" in res["failures"], str(res["failures"]))
    # R2 same-role target the runtime would not choose: GREEK has g1,g2 LETTER (distinct surfaces -> ambiguous) -> TRANSLATED invalid
    aa = artifact(); rr = receipt(aa, tr=translated(aa, "a1", "g2")); res = V(rr, aa)
    row("R2 non-chosen same-role target", "TARGET_RESOLUTION_INCONSISTENT" in res["failures"], str(res["failures"]))
    # AMBIGUOUS genuine and R3 / F08a
    aa = artifact(); A = ah(aa)
    amb = {"status": "AMBIGUOUS_NO_SILENT_PICK", "source_symbol_id": "a1", "symbolic_role": "LETTER", "target_script_family": "GREEK",
           "ambiguous_candidates": [{"symbol_id": "g1", "visible_symbol": "Α"}, {"symbol_id": "g2", "visible_symbol": "Β"}],
           "frozen_artifact_sha256": A, "translation_packet": None}
    rr = receipt(aa, tr=copy.deepcopy(amb)); res = V(rr, aa); row("NC8 genuine AMBIGUOUS verifies", res["verified"], str(res["failures"]))
    t = copy.deepcopy(amb); t["ambiguous_candidates"] = t["ambiguous_candidates"][:1]; rr = receipt(aa, tr=t); res = V(rr, aa)
    row("R3/X6a(i) one candidate", "REQUIRED_FIELD_MISSING" in res["failures"] and "translation_result.ambiguous_candidates" in res["failure_details"])
    t = copy.deepcopy(amb); t["ambiguous_candidates"].append(copy.deepcopy(t["ambiguous_candidates"][0])); rr = receipt(aa, tr=t); res = V(rr, aa)
    row("F08a duplicate candidate", "TARGET_RESOLUTION_INCONSISTENT" in res["failures"])
    t = copy.deepcopy(amb); t["ambiguous_candidates"] = [{}, {}]; rr = receipt(aa, tr=t); res = V(rr, aa)
    exp = ["translation_result.ambiguous_candidates[0].symbol_id", "translation_result.ambiguous_candidates[0].visible_symbol", "translation_result.ambiguous_candidates[1].symbol_id", "translation_result.ambiguous_candidates[1].visible_symbol"]
    row("X6b exact order", [d for f, d in zip(res["failures"], res["failure_details"]) if f == "REQUIRED_FIELD_MISSING"] == exp, str(res["failure_details"]))
    # R4 NO_TARGET for a family that has targets
    nt = {"status": "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY", "source_symbol_id": "a1", "symbolic_role": "LETTER", "target_script_family": "CYRILLIC", "frozen_artifact_sha256": A, "translation_packet": None}
    rr = receipt(aa, tr=copy.deepcopy(nt)); res = V(rr, aa); row("R4 NO_TARGET false claim", "TARGET_RESOLUTION_INCONSISTENT" in res["failures"])
    nt2 = dict(nt, target_script_family=None); rr = receipt(aa, tr=nt2); res = V(rr, aa); row("NC14 NO_TARGET family None verifies", res["verified"], str(res["failures"]))
    nt3 = dict(nt, target_script_family=5); rr = receipt(aa, tr=nt3); res = V(rr, aa); row("NC14 NO_TARGET family 5 verifies", res["verified"], str(res["failures"]))
    # M-series
    rr = copy.deepcopy(r); del rr["translation_result"]["translation_packet"]["source_symbol_id"]; rehash(rr); res = V(rr, a)
    row("M1/P1 packet id key deleted", "REQUIRED_FIELD_MISSING" in res["failures"] and "TARGET_RESOLUTION_INCONSISTENT" not in res["failures"])
    rr = copy.deepcopy(r); del rr["translation_result"]["translation_packet"]["packet_sha256"]; rehash(rr, packet=False); res = V(rr, a)
    row("M2/X4o packet_sha256 deleted", "PACKET_HASH_MISSING_OR_MALFORMED" in res["failures"] and "REQUIRED_FIELD_MISSING" not in res["failures"], str(res["failures"]))
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"] = None; rehash(rr); res = V(rr, a)
    row("M3 TRANSLATED with packet None", res["failures"].count("STATUS_PACKET_INCONSISTENT") == 1)
    rr = copy.deepcopy(r); rr["translation_result"]["status"] = "WHATEVER"; rehash(rr); res = V(rr, a); row("M4 unknown status", "UNKNOWN_STATUS" in res["failures"])
    rr = copy.deepcopy(r); del rr["query_result"]["frozen_artifact_sha256"]; rehash(rr); res = V(rr, a); row("M5 copy removed", "ARTIFACT_HASH_COPY_MISSING" in res["failures"])
    rr = copy.deepcopy(r); rr["query_result"]["frozen_artifact_sha256"] = "0" * 64; rehash(rr); res = V(rr, a); row("M5 copy altered", "ARTIFACT_HASH_COPY_MISMATCH" in res["failures"])
    rr = copy.deepcopy(r); rr["translation_result"]["restored_state_sha256"] = "f" * 64; rehash(rr); res = V(rr, a); row("M6 state copies disagree", "STATE_HASH_COPY_MISMATCH" in res["failures"])
    rr = copy.deepcopy(r); rr["frozen_artifact_id"] = "FORGED"; rehash(rr); res = V(rr, a); row("M7 frozen_artifact_id forged", "FROZEN_ARTIFACT_ID_MISMATCH" in res["failures"])
    rr = copy.deepcopy(r); rr["query_result"] = {"status": "INTEGRITY_CHECK_FAILED"}; rehash(rr); res = V(rr, a)
    row("M8/D-2 INTEGRITY_CHECK_FAILED", "INNER_STATUS_INTEGRITY_CHECK_FAILED" in res["failures"] and not res["verified"])
    res = V(r, None); row("S2 artifact None", "SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK" in res["failures"])
    res = V(r, None, expected_artifact_sha256=ah(a)); row("AN1 anchor w/o artifact", res["layers"]["L3_BINDING"] == "FAIL" and res["layers"]["L3_ANCHOR"] == "NOT_EVALUATED")
    res = V(r, a, strict_mode=True); row("N1 strict no anchor", "EXTERNAL_ANCHOR_REQUIRED_IN_STRICT_MODE" in res["failures"])
    res = V(r, a, expected_artifact_sha256="0" * 64, expected_restored_state_sha256="1" * 64); row("N2 anchors differ", "EXPECTED_ARTIFACT_HASH_MISMATCH" in res["failures"] and "EXPECTED_STATE_HASH_MISMATCH" in res["failures"])
    rr = copy.deepcopy(r); rr["module_id"] = "X"; rr["generated_at_utc"] = "2026-10-29T12:00:00+02:00"; rehash(rr); res = V(rr, a, expected_artifact_sha256=ah(a), strict_mode=True)
    row("N3 strict policy codes", "POLICY_MODULE_ID_NOT_ALLOWED" in res["failures"] and "POLICY_TIMESTAMP_MALFORMED" in res["failures"])
    rr = copy.deepcopy(r); rr["receipt_version"] = "9.9.9"; rehash(rr); res = V(rr, a, expected_artifact_sha256=ah(a), expected_restored_state_sha256=STATE)
    row("V4/NC20 unlisted stamp default mode verifies (non-claim)", res["verified"] and res["assurance"] == "ARTIFACT_AND_STATE_ANCHORED")
    rr = copy.deepcopy(r); del rr["receipt_version"]; rehash(rr); res = V(rr, a); row("V1 receipt_version deleted", "REQUIRED_FIELD_MISSING" in res["failures"])
    for vv in (2.76, None, []):
        rr = copy.deepcopy(r); rr["receipt_version"] = vv; rehash(rr); res = V(rr, a); row(f"V2 receipt_version {vv!r}", "REQUIRED_FIELD_MISSING" in res["failures"])
    rr = copy.deepcopy(r); del rr["boundary"]; rehash(rr); res = V(rr, a)
    row("B2 boundary absent -> 4 codes", sorted(f for f in res["failures"] if f.startswith("BOUNDARY_VIOLATION")) == sorted("BOUNDARY_VIOLATION:" + k for k in ("read_only_query_mode", "restored_registry_remains_frozen", "mutation_guard_enforced", "real_world_control")))
    rr = copy.deepcopy(r); rr["query_result"].update(status="OK", records=[], symbol_ids=[], match_count=0, found=False); rehash(rr); res = V(rr, a); row("Q8a OK with no records", "CROSS_FIELD_INCONSISTENT" in res["failures"])
    rr = copy.deepcopy(r); rr["translation_result"] = {"status": "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY", "frozen_artifact_sha256": ah(a), "translation_packet": {"x": 1}}; rehash(rr); res = V(rr, a)
    row("X3b NO_SOURCE with packet", "STATUS_PACKET_INCONSISTENT" in res["failures"])
    # CF1/CF2/CF3 lone surrogate (T-6: inserted after hashing)
    rr = copy.deepcopy(r); rr["note"] = "\ud800"; res = V(rr, a)
    row("CF1 surrogate in receipt", "CANONICALIZATION_FAILED" in res["failures"] and res["layers"]["L1"] == "FAIL")
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["meaning_invariant"] = ["\ud800"]; res = V(rr, a)
    cf = [d for f, d in zip(res["failures"], res["failure_details"]) if f == "CANONICALIZATION_FAILED"]
    row("CF2 surrogate in packet -> receipt, translation_packet", cf == ["receipt", "translation_packet"], str(cf))
    aa = artifact(); rr = receipt(aa); aa["frozen_registry_snapshot"]["registry_records"]["c2"]["visible_symbol"] = "\ud800"; res = V(rr, aa)
    row("CF3 surrogate in artifact", ("CANONICALIZATION_FAILED", "artifact") in zip(res["failures"], res["failure_details"]) and res["layers"]["L3_BINDING"] == "FAIL")
    # S3 / O1 / O2 exact order
    rr = copy.deepcopy(r); rr["receipt_type"] = "WRONG"; rr["translation_result"]["translation_packet"]["packet_type"] = "x"; rr["query_result"]["match_count"] = 9; rehash(rr, packet=False); res = V(rr, a)
    row("S3 exact order", res["failures"] == ["PACKET_HASH_MISMATCH_TAMPER_DETECTED", "CROSS_FIELD_INCONSISTENT", "WRONG_RECEIPT_TYPE"], str(res["failures"]))
    rr = copy.deepcopy(r); rr["query_result"]["frozen_artifact_sha256"] = "0" * 64; rr["query_result"]["match_count"] = 9; rr["receipt_type"] = "WRONG"; rehash(rr); res = V(rr, a)
    row("O1 exact order", res["failures"] == ["ARTIFACT_HASH_COPY_MISMATCH", "CROSS_FIELD_INCONSISTENT", "WRONG_RECEIPT_TYPE"] and res["layers"]["L2"] == "FAIL", str(res["failures"]))
    rr = copy.deepcopy(r); rr["query_result"]["match_count"] = 9; rr["query_result"]["records"][0]["visible_symbol"] = "Q"; rr["receipt_type"] = "WRONG"; rehash(rr); res = V(rr, a)
    row("O2 exact order", res["failures"] == ["CROSS_FIELD_INCONSISTENT", "RECORD_MISMATCH_WITH_ARTIFACT", "WRONG_RECEIPT_TYPE"], str(res["failures"]))
    # S4a / S4b / S4c caps
    def many(n):
        aa = artifact(); ids = [f"u{i:02d}" for i in range(n)]
        qr = {"status": "OK", "found": True, "match_count": n, "symbol_ids": ids, "records": [{"symbol_id": i} for i in ids], "frozen_artifact_sha256": ah(aa)}
        return aa, receipt(aa, qr=qr, tr={})
    aa, rr = many(16); res = V(rr, aa); row("S4a 32 failures, no truncation", len(res["failures"]) == 32 and set(res["failures"]) == {"SYMBOL_ID_NOT_IN_ARTIFACT"} and "FAILURES_TRUNCATED" not in res["failures"], str(len(res["failures"])))
    aa, rr = many(17); res = V(rr, aa); row("S4b 33 entries ending FAILURES_TRUNCATED", len(res["failures"]) == 33 and res["failures"][-1] == "FAILURES_TRUNCATED")
    aa, rr = many(17); rr["receipt_type"] = "WRONG"; rehash(rr); res = V(rr, aa)
    row("S4c cap does not stop evaluation", len(res["failures"]) == 33 and "WRONG_RECEIPT_TYPE" not in res["failures"] and res["layers"]["L4"] == "FAIL" and res["verified"] is False)
    # S5 attacker text never echoed
    rr = copy.deepcopy(r); rr["translation_result"]["translation_packet"]["source_symbol_id"] = "ATTACKER_TEXT_XYZ"; rr["boundary"]["ATTACKER_KEY_XYZ"] = 1; rehash(rr); res = V(rr, a)
    blob = json.dumps(res["failures"]) + json.dumps(res["failure_details"])
    row("S5 no attacker text echoed; details <=120", "ATTACKER" not in blob and all(len(d) <= 120 for d in res["failure_details"]))

for f in (api, l0, later):
    guarded(f.__name__, f)
summary = {"profile": [platform.python_implementation(), platform.python_version(), unicodedata.unidata_version],
           "PASS": sum(1 for _, s, _ in results if s == "PASS"), "FAIL": sum(1 for _, s, _ in results if s == "FAIL"),
           "EXCEPTION": sum(1 for _, s, _ in results if s == "EXCEPTION"),
           "failed_rows": [rid for rid, s, _ in results if s != "PASS"]}
print("SUMMARY " + json.dumps(summary))
