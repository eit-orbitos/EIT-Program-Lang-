"""V2.7.7 candidate SELF-CHECK script V0.5 — re-runnable, read-only re originals.

FIXES vs V0.4 (per TASKLET_V277_KIMI_V04_CORRECTION_REVIEW_V0.1):
- F-1/F-2: check 1d uses ast.literal_eval (NON-EXECUTING) — no exec() of any V2.7.6 fragment.
- F-3: checks 12/13 assert the SPECIFIC ImportError message (missing companion vs hash-pin mismatch).
- F-4: check 11 asserts equality AND non-identity vs SAFETY_BLOCK (not just shape).
- F-5: checks 2 and 3 restored (stale packet hash; unknown id) with correct rehash ordering.
- F-6: 1e/1f annotated: they encode the CHOSEN option of OPEN Q4, not a contract result.
- F-7: log header binds verifier SHA-256, UTC timestamp, Python version, exit code.

Candidate code only. No V2.7.5/V2.7.6 project code executed (RG-2 Exclusion 2).
Exit 0 = all pass. NOT a T-10 outcome (RG-4 NOT_RUN).
"""
import ast, copy, hashlib, importlib.util, os, shutil, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
VPATH = next(p for p in [
    os.path.join(HERE, "receipt_verifier_v277_candidate.py"),
    os.path.join(HERE, "eit_program_lang", "receipt_verifier_v277_candidate.py"),
    os.path.join(HERE, "..", "eit_program_lang", "receipt_verifier_v277_candidate.py"),
    os.path.join(HERE, "..", "eit_program_lang", "receipt_verifier.py"),
] if os.path.exists(p))
def _find(*rel):
    for base in (HERE, os.path.normpath(os.path.join(HERE, ".."))):
        q = os.path.join(base, *rel)
        if os.path.exists(q):
            return q
    raise FileNotFoundError(os.path.join(*rel))
CPATH = _find("eit_program_lang", "restored_registry_index_v277_candidate.py")
VHASH = hashlib.sha256(open(VPATH, "rb").read()).hexdigest()
print("SELF-CHECK V0.5")
print("verifier under test :", VHASH)
print("verifier bytes      :", os.path.getsize(VPATH))
import datetime as _dt
print("utc timestamp       :", _dt.datetime.now(_dt.timezone.utc).isoformat())
print("python              :", sys.version.split()[0])
print("-" * 60)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

v = load(VPATH, "v_selfcheck")
results = []
def check(name, ok):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name)

def make_fixture():
    artifact = {"frozen_registry_snapshot": {"registry_records": {
        "alpha": {"symbol_id": "alpha", "script_family": "LATIN", "symbolic_role": "LETTER",
                  "visible_symbol": "A", "meaning_invariant": []},
        "beta":  {"symbol_id": "beta", "script_family": "CYRILLIC", "symbolic_role": "LETTER",
                  "visible_symbol": "\u0411", "meaning_invariant": []}}},
        "frozen_artifact_id": "ART-1"}
    AH = v.artifact_sha256(artifact)
    packet = {"source_symbol_id": "alpha", "target_symbol_id": "beta",
              "source_script_family": "LATIN", "target_script_family": "CYRILLIC",
              "source_visible_symbol": "A", "target_visible_symbol": "\u0411",
              "symbolic_role": "LETTER", "meaning_invariant": [],
              "frozen_artifact_sha256": AH, "restored_state_sha256": None,
              "packet_version": "2.7.7"}
    packet["packet_sha256"] = v.sha256_json({k: val for k, val in packet.items() if k != "packet_sha256"})
    tr = {"status": "TRANSLATED_FROM_FROZEN_REGISTRY",
          "source": copy.deepcopy(artifact["frozen_registry_snapshot"]["registry_records"]["alpha"]),
          "target": copy.deepcopy(artifact["frozen_registry_snapshot"]["registry_records"]["beta"]),
          "frozen_artifact_sha256": AH, "restored_state_sha256": None, "translation_packet": packet}
    qr = {"status": "OK", "found": True, "match_count": 1, "symbol_ids": ["alpha"],
          "records": [copy.deepcopy(artifact["frozen_registry_snapshot"]["registry_records"]["alpha"])],
          "frozen_artifact_sha256": AH}
    receipt = {"receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT", "receipt_version": "2.7.7",
               "module_id": "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7",
               "generated_at_utc": "2026-10-22T12:00:00+00:00",
               "boundary": {"read_only_query_mode": True, "restored_registry_remains_frozen": True,
                            "mutation_guard_enforced": True, "real_world_control": False},
               "frozen_artifact_sha256": AH, "frozen_artifact_id": "ART-1",
               "query_result": qr, "translation_result": tr}
    receipt["receipt_sha256"] = v.sha256_json({k: val for k, val in receipt.items() if k != "receipt_sha256"})
    return artifact, receipt

def rehash(r):
    r["receipt_sha256"] = v.sha256_json({k: val for k, val in r.items() if k != "receipt_sha256"})
    return r

art, rc = make_fixture()
r = v.verify_restored_query_receipt(rc, art)
check("1 genuine verifies (CONSISTENCY_ONLY)", r["verified"] and r["assurance"] == "CONSISTENCY_ONLY")
check("1b check_type", r["check_type"] == "VERIFY_RESTORED_QUERY_RECEIPT")
check("1c safety dict copy, non-identity (main)", type(r["safety"]) is dict and r["safety"] is not v.SAFETY_BLOCK)

# F-1/F-2 FIX: non-executing comparison via ast.literal_eval
import re as _re
zip_cands = [os.path.join(HERE, "..", "reference", "EIT_V2_7_6.zip"),
             os.path.join(HERE, "..", "..", "upload", "EIT_V2_7_6.zip"), "/mnt/agents/upload/EIT_V2_7_6.zip"]
zip_path = next((z for z in zip_cands if os.path.exists(z)), None)
if zip_path is None:
    check("1d SAFETY_BLOCK == V2.7.6 bytes (16 fields) [zip absent]", False)
else:
    with zipfile.ZipFile(zip_path) as _zf:
        orig_txt = _zf.read("EIT_V2_7_6/eit_program_lang/restored_registry_index.py").decode()
    m = _re.search(r"SAFETY_BLOCK = (\{.*?\n\})", orig_txt, _re.S)
    orig_block = ast.literal_eval(m.group(1))  # NON-EXECUTING (F-1 fix)
    check("1d SAFETY_BLOCK == V2.7.6 bytes (16 fields, ast.literal_eval)",
          v.SAFETY_BLOCK == orig_block and len(v.SAFETY_BLOCK) == 16)

# F-6 annotation: 1e/1f encode the CHOSEN option of OPEN Q4 (declared), not a contract result
check("1e Q4-CHOSEN declared passthrough", r["receipt_sha256"] == rc["receipt_sha256"])
rt = copy.deepcopy(rc); rt["query_result"]["found"] = False; rehash(rt)
r = v.verify_restored_query_receipt(rt, art)
check("1f Q4-CHOSEN declared passthrough on failure", r["receipt_sha256"] == rt["receipt_sha256"] and not r["verified"])

# F-5 FIX: restored checks 2 and 3 (correct order: mutate, then rehash)
r2 = copy.deepcopy(rc); r2["translation_result"]["translation_packet"]["target_visible_symbol"] = "\u0412"; rehash(r2)
r = v.verify_restored_query_receipt(r2, art)
check("2 stale packet hash -> PACKET_HASH_MISMATCH_TAMPER_DETECTED", "PACKET_HASH_MISMATCH_TAMPER_DETECTED" in r["failures"])
r3 = copy.deepcopy(rc); r3["query_result"]["symbol_ids"] = ["ghost"]; rehash(r3)
r = v.verify_restored_query_receipt(r3, art)
check("3 unknown id -> SYMBOL_ID_NOT_IN_ARTIFACT", "SYMBOL_ID_NOT_IN_ARTIFACT" in r["failures"])

r4 = copy.deepcopy(rc); r4["extra"] = 2**63
r = v.verify_restored_query_receipt(r4, art)
check("4 int domain exact detail", r["failures"] == ["RECEIPT_SHAPE_INVALID"] and r["failure_details"] == ["receipt:depth=2:path=1"])
r5 = copy.deepcopy(rc); r5["evil"] = (1, 2)
r = v.verify_restored_query_receipt(r5, art)
check("5 hostile tuple -> REJECT", r["failures"] == ["REJECT_UNTRUSTED_OBJECT_TYPE"])
r = v.verify_restored_query_receipt(rc, art, strict_mode=True)
check("6 strict no anchor", "EXTERNAL_ANCHOR_REQUIRED_IN_STRICT_MODE" in r["failures"])
r6 = copy.deepcopy(rc); del r6["receipt_version"]; rehash(r6)
r = v.verify_restored_query_receipt(r6, art)
check("7 missing version exact detail", r["failures"] == ["REQUIRED_FIELD_MISSING"] and r["failure_details"] == ["receipt.receipt_version"])
r = v.verify_restored_query_receipt(rc, art, strict_mode=True, expected_artifact_sha256=v.artifact_sha256(art))
check("8 strict anchored (ARTIFACT_ANCHORED)", r["verified"] and r["assurance"] == "ARTIFACT_ANCHORED")
r = v.verify_restored_query_receipt(rc, None)
check("9 artifact None", "SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK" in r["failures"] and r["layers"]["L3_ANCHOR"] == "NOT_EVALUATED")
r7 = copy.deepcopy(rc); r7["translation_result"]["status"] = "AMBIGUOUS_NO_SILENT_PICK"
r7["translation_result"]["ambiguous_candidates"] = [{"symbol_id": "alpha", "visible_symbol": "A"}]
r7["translation_result"]["source_symbol_id"] = "alpha"; r7["translation_result"]["symbolic_role"] = "LETTER"
r7["translation_result"]["target_script_family"] = "LATIN"
for k in ("target", "source", "translation_packet"): r7["translation_result"].pop(k, None)
rehash(r7)
r = v.verify_restored_query_receipt(r7, art)
check("10 ambiguous 1-cand -> TARGET_RESOLUTION_INCONSISTENT", "TARGET_RESOLUTION_INCONSISTENT" in r["failures"])

# F-4 FIX: equality AND non-identity on L0 path too
rx = copy.deepcopy(rc); rx["bad"] = (1,)
r = v.verify_restored_query_receipt(rx, art)
check("11 L0 safety == SAFETY_BLOCK, dict copy, 16 keys (Q5/D-4)",
      type(r["safety"]) is dict and r["safety"] == v.SAFETY_BLOCK and r["safety"] is not v.SAFETY_BLOCK and len(r["safety"]) == 16)

# F-3 FIX: assert the SPECIFIC ImportError messages
tmp = tempfile.mkdtemp()
shutil.copy(VPATH, os.path.join(tmp, os.path.basename(VPATH)))
try:
    spec2 = importlib.util.spec_from_file_location("v_nocompanion", os.path.join(tmp, os.path.basename(VPATH)))
    m2 = importlib.util.module_from_spec(spec2)
    try:
        spec2.loader.exec_module(m2)
        check("12 missing companion -> ImportError 'missing'", False)
    except ImportError as e:
        check("12 missing companion -> ImportError 'missing'", "missing" in str(e))
    shutil.copy(CPATH, os.path.join(tmp, os.path.basename(CPATH)))
    with open(os.path.join(tmp, os.path.basename(CPATH)), "a") as f:
        f.write("\n# tampered\n")
    spec3 = importlib.util.spec_from_file_location("v_tampered", os.path.join(tmp, os.path.basename(VPATH)))
    m3 = importlib.util.module_from_spec(spec3)
    try:
        spec3.loader.exec_module(m3)
        check("13 tampered companion -> ImportError 'hash mismatch' (D-1)", False)
    except ImportError as e:
        check("13 tampered companion -> ImportError 'hash mismatch' (D-1)", "hash mismatch" in str(e))
finally:
    shutil.rmtree(tmp)

npass = sum(1 for _, ok in results if ok)
print("-" * 60)
print("%d/%d self-checks PASS" % (npass, len(results)))
print("exit code:", 0 if npass == len(results) else 1)
print("NOTE: candidate self-checks only; NOT RG-4 evidence; no T-10 outcome.")
sys.exit(0 if npass == len(results) else 1)
