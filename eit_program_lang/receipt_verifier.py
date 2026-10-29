"""EIT V2.7.7 receipt verifier — ISOLATED IMPLEMENTATION CANDIDATE.

SPEC: EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.9.md
SPEC SHA-256: 3fc10557032bfb2ab4acf2953f9654c5bdc0f32db43aee7cfdd69fd0d384f27c
AUTH: EIT_V277_AUTHORIZATION_FOR_IMPLEMENTATION_V0.1.md (Toni Mladenovski, 2026-10-22)
STATUS: CANDIDATE / NOT_RELEASED / RG-4 NOT_RUN
SCOPE: §0.2 — one function. No original modified. EIT_V2_7_6.zip (3b99157e...e22c,
28/28 internal MATCH) is present in this container and was READ AS TEXT ONLY for static
verification; no project code was executed.

IMPLEMENTATION_QUESTIONS:
  Q1: RESOLVED (BYTE-VERIFIED) — EIT_V2_7_6.zip in container, SHA-256 3b99157e...e22c
      EXACT MATCH; original receipt_verifier.py returns
      check_type = "VERIFY_RESTORED_QUERY_RECEIPT".
  Q2: RESOLVED (BYTE-VERIFIED) — original returns safety = dict(SAFETY_BLOCK),
      imported from restored_registry_index (relative import ".restored_registry_index").
  Q3: RESOLVED (BYTE-VERIFIED) — SAFETY_BLOCK copied verbatim from the byte-verified
      original into restored_registry_index_v277_candidate.py (16 fields).
  Q4: OPEN (IMPLEMENTATION_QUESTION) — V0.5.9 §4.2 requires key preservation but does not
      specify declared vs recomputed receipt_sha256. Candidate returns the DECLARED stored value,
      matching V2.7.6 (single return site, `declared`). Any spec-contract change requires author
      decision; on declared/recomputed mismatch the verifier reports via failure codes (1a.1/1a.2).
  Q5: RESOLVED (BYTE-VERIFIED) — V2.7.6 receipt_verifier.py has exactly ONE return site; `safety`
      is dict(SAFETY_BLOCK) on every path. Candidate L0 path corrected to match.
"""

import hashlib
import json
import math
import unicodedata
from datetime import datetime, timezone, timedelta

# SAFETY_BLOCK — Q2/Q3 BYTE-VERIFIED against EIT_V2_7_6.zip (3b99157e...e22c).
# FAIL-CLOSED (F-C1 fix, Tasklet intake review V0.1): no fallback. If the companion
# module cannot be loaded, this import raises and the verifier cannot be used.
# N-1 FIX (Tasklet V0.5): read once, verify hash BEFORE any execution, avoid TOCTOU.
# No execution of companion file — SAFETY_BLOCK extracted via ast.literal_eval from verified bytes.
import os as _os
import hashlib as _hl
import ast as _ast
import re as _re

_mpath = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                       "restored_registry_index_v277_candidate.py")
_COMPANION_SHA256 = "4ba6556ac456601bf9d91608f28ba950b619c51ac123598aeeb480d24444ad65"

if not _os.path.exists(_mpath):
    raise ImportError("SAFETY_BLOCK source module missing: %s" % _mpath)

_comp_bytes = open(_mpath, "rb").read()
if _hl.sha256(_comp_bytes).hexdigest() != _COMPANION_SHA256:
    raise ImportError("SAFETY_BLOCK companion hash mismatch: " + _mpath)

# Verified bytes — extract SAFETY_BLOCK without executing companion
_comp_text = _comp_bytes.decode("utf-8", errors="strict")
_m = _re.search(r"SAFETY_BLOCK\s*=\s*(\{.*?\n\})", _comp_text, _re.S)
if _m is None:
    raise ImportError("SAFETY_BLOCK definition not found in verified companion")
SAFETY_BLOCK = _ast.literal_eval(_m.group(1))

INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 63 - 1
DEPTH_LIMIT = 32
FAILURE_CAP = 32

# §2.1 — MUST call the existing canonical contract; reproduced exactly per V0.5.9 — V2.7.6 tree read as text only for static verification, no execution.
def sha256_json(data):
    payload = json.dumps(data, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

# §2.2
def artifact_sha256(frozen_artifact):
    return hashlib.sha256(json.dumps(frozen_artifact, sort_keys=True,
                          ensure_ascii=False).encode("utf-8")).hexdigest()

# §3.3 typed equality
def teq(a, b):
    ta, tb = type(a), type(b)
    if ta is not tb:
        return False
    if ta is dict:
        if set(a.keys()) != set(b.keys()):
            return False
        return all(teq(a[k], b[k]) for k in a)
    if ta is list:
        return len(a) == len(b) and all(teq(x, y) for x, y in zip(a, b))
    if ta is float:
        if a == b:
            return True
        return math.isnan(a) and math.isnan(b)
    return a == b

# §3.2
def nfc(x):
    return unicodedata.normalize("NFC", str(x))

def role_norm(x, stamp):
    return str(x).upper() if stamp == "2.7.4" else nfc(x).upper()

def family_norm(x, stamp):
    return str(x).upper() if stamp == "2.7.4" else nfc(x).upper()

# §3.4
def candidates(records, role, family, stamp):
    return [r for r in records.values()
            if role != ""
            and role_norm(r.get("symbolic_role", ""), stamp) == role
            and family_norm(r.get("script_family", ""), stamp) == family]

def normalized_surface(r):
    return nfc(r.get("visible_symbol"))

# §10.3 allow-list
ALLOW_LIST = (
    ("2.7.4", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_4"),
    ("2.7.6", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_6"),
    ("2.7.7", "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7"),
)

BOUNDARY_PAIRS = (
    ("read_only_query_mode", True),
    ("restored_registry_remains_frozen", True),
    ("mutation_guard_enforced", True),
    ("real_world_control", False),
)

_STATUS_TR = (
    "TRANSLATED_FROM_FROZEN_REGISTRY",
    "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY",
    "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
    "AMBIGUOUS_NO_SILENT_PICK",
    "INTEGRITY_CHECK_FAILED",
)

class _Collector:  # §5.2 P-2, P-3
    def __init__(self):
        self.entries = []
        self.seen = set()
        self.truncated = False
        self.occurred = 0  # every emitted failure, incl. deduped and post-cap

    def emit(self, code, detail):
        self.occurred += 1
        if self.truncated:
            return
        if (code, detail) in self.seen:
            return
        if len(self.entries) >= FAILURE_CAP:
            self.entries.append(("FAILURES_TRUNCATED", "failures"))
            self.truncated = True
            return
        self.seen.add((code, detail))
        self.entries.append((code, detail))


def _num(n):
    return str(n)  # decimal, no sign, no leading zero (values are non-negative)

def _scan_detail(root, kind, depth, path):
    # §6.3: failing value -> n = depth of value, path has n-1 elements;
    #        rejected key -> n = depth of containing dict, path has n elements.
    s = "%s:depth=%s:path=%s" % (root, _num(depth), ".".join(_num(e) for e in path))
    return s[:120]  # C-3 fix (RG-4): §6.3 truncation to 120 characters

def _l0_scan(node, depth, path):
    """Returns (kind, depth, path) of first failure or None. §6.3 exact order."""
    if depth > DEPTH_LIMIT:
        return ("DEPTH", depth, path)
    t = type(node)
    if t is int:
        if node < INT_MIN or node > INT_MAX:
            return ("RANGE", depth, path)
        return None
    if t is bool or t is float or t is str or t is type(None):
        return None
    if t is list:
        for i, v in enumerate(node):
            r = _l0_scan(v, depth + 1, path + (i,))
            if r:
                return r
        return None
    if t is dict:
        for ord_i, k in enumerate(node.keys()):  # iteration order
            if type(k) is not str:
                return ("KEY", depth, path + (ord_i,))
        for ord_i, k in enumerate(sorted(node.keys())):  # ascending exact str keys
            r = _l0_scan(node[k], depth + 1, path + (ord_i,))
            if r:
                return r
        return None
    return ("TYPE", depth, path)

def _well_formed_hash(v):
    return type(v) is str and len(v) == 64 and all(c in "0123456789abcdef" for c in v)

def _layer_init():
    return {"L0": "PASS", "L1": "NOT_EVALUATED", "L2": "NOT_EVALUATED",
            "L3_BINDING": "NOT_EVALUATED", "L3_ANCHOR": "NOT_EVALUATED",
            "L3_STATE": "NOT_EVALUATED", "L4": "NOT_EVALUATED"}


def verify_restored_query_receipt(
    receipt,
    source_frozen_artifact=None,
    expected_artifact_sha256=None,
    expected_restored_state_sha256=None,
    strict_mode=False,
):
    """Verify a restored registry query receipt against V0.5.9.

    The verifier cannot enforce that expected hashes were obtained from a
    trustworthy independent channel. If the caller computes an expected hash
    from the untrusted artifact being verified, an `ARTIFACT_ANCHORED`
    assurance label does not establish independent provenance or producer
    authenticity. (§4.5 verbatim text)
    """
    layers = _layer_init()
    col = _Collector()

    # ---------- Phase 0 / L0 (§6.2, fail-fast) ----------
    if type(strict_mode) is not bool:  # 0.1a
        return _l0_result(col, layers, ("STRICT_MODE_NOT_BOOL", "strict_mode"), receipt, raw=True)
    if not (expected_artifact_sha256 is None or _well_formed_hash(expected_artifact_sha256)):  # 0.1b
        return _l0_result(col, layers, ("EXPECTED_ANCHOR_MALFORMED", "expected_artifact_sha256"), receipt, raw=True)
    if not (expected_restored_state_sha256 is None or _well_formed_hash(expected_restored_state_sha256)):  # 0.1c
        return _l0_result(col, layers, ("EXPECTED_ANCHOR_MALFORMED", "expected_restored_state_sha256"), receipt, raw=True)
    if type(receipt) is not dict:  # 0.2
        return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "receipt"), receipt, raw=True)

    r = _l0_scan(receipt, 1, ())  # 0.3
    if r:
        kind, depth, path = r
        detail = _scan_detail("receipt", kind, depth, path)
        code = "REJECT_UNTRUSTED_OBJECT_TYPE" if kind in ("KEY", "TYPE") else "RECEIPT_SHAPE_INVALID"
        return _l0_result(col, layers, (code, detail), receipt, raw=True)

    qr = receipt.get("query_result")  # 0.4
    if qr is None:
        qr = {}
    tr = receipt.get("translation_result")
    if tr is None:
        tr = {}
    if type(qr) is not dict:
        return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "query_result"), receipt, raw=True)
    if type(tr) is not dict:
        return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "translation_result"), receipt, raw=True)

    boundary = receipt.get("boundary")  # 0.5
    if type(boundary) is not dict and "boundary" in receipt:
        return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "boundary"), receipt, raw=True)
    if "boundary" not in receipt:
        boundary = None  # absent: treated as {} in L4 (S-6/§10.1)

    if "query_result" in receipt and receipt["query_result"] is not None:  # 0.6
        if "symbol_ids" in qr and type(qr["symbol_ids"]) is not list:
            return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "query_result.symbol_ids"), receipt, raw=True)
        if "records" in qr:
            if type(qr["records"]) is not list:
                return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "query_result.records"), receipt, raw=True)
            for i, rec in enumerate(qr["records"]):
                if type(rec) is not dict:
                    return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "query_result.records[%d]" % i), receipt, raw=True)

    if "translation_result" in receipt and receipt["translation_result"] is not None:  # 0.7
        if "translation_packet" in tr and tr["translation_packet"] is not None and type(tr["translation_packet"]) is not dict:
            return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "translation_result.translation_packet"), receipt, raw=True)
        for side in ("source", "target"):
            if side in tr and type(tr[side]) is not dict:
                return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "translation_result." + side), receipt, raw=True)
        if "ambiguous_candidates" in tr:
            if type(tr["ambiguous_candidates"]) is not list:
                return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "translation_result.ambiguous_candidates"), receipt, raw=True)
            for i, c in enumerate(tr["ambiguous_candidates"]):
                if type(c) is not dict:
                    return _l0_result(col, layers, ("RECEIPT_SHAPE_INVALID", "translation_result.ambiguous_candidates[%d]" % i), receipt, raw=True)

    artifact = source_frozen_artifact
    if artifact is not None:
        if type(artifact) is not dict:  # 0.8
            return _l0_result(col, layers, ("ARTIFACT_SHAPE_INVALID", "artifact"), receipt, raw=True)
        r = _l0_scan(artifact, 1, ())  # 0.9
        if r:
            kind, depth, path = r
            detail = _scan_detail("artifact", kind, depth, path)
            code = "REJECT_UNTRUSTED_OBJECT_TYPE" if kind in ("KEY", "TYPE") else "ARTIFACT_SHAPE_INVALID"
            return _l0_result(col, layers, (code, detail), receipt, raw=True)
        # 0.10
        if "frozen_registry_snapshot" not in artifact or type(artifact["frozen_registry_snapshot"]) is not dict:
            return _l0_result(col, layers, ("ARTIFACT_SHAPE_INVALID", "artifact.frozen_registry_snapshot"), receipt, raw=True)
        snap = artifact["frozen_registry_snapshot"]
        if "registry_records" not in snap or type(snap["registry_records"]) is not dict:
            return _l0_result(col, layers, ("ARTIFACT_SHAPE_INVALID", "artifact.registry_records"), receipt, raw=True)
        records = snap["registry_records"]
        for ord_i, k in enumerate(sorted(records.keys())):
            rec = records[k]
            if type(rec) is not dict:
                return _l0_result(col, layers, ("ARTIFACT_SHAPE_INVALID", "artifact.registry_records:ordinal=%d" % ord_i), receipt, raw=True)
            if "symbol_id" not in rec or type(rec["symbol_id"]) is not str or not teq(rec["symbol_id"], k):
                return _l0_result(col, layers, ("ARTIFACT_SHAPE_INVALID", "artifact.registry_records:ordinal=%d" % ord_i), receipt, raw=True)
    else:
        records = None

    # ---------- derived values ----------
    stamp_raw = receipt.get("receipt_version")
    stamp = stamp_raw if type(stamp_raw) is str else None  # None -> current rules (§3.1)
    legacy = (stamp == "2.7.4")

    P = tr.get("translation_packet")
    packet_is_mapping = "translation_packet" in tr and type(P) is dict

    # ---------- Phase 1 / L1 (§7, H-5) ----------
    layers["L1"] = "PASS"
    rs = receipt.get("receipt_sha256")
    # F2 fix (RG-5): §7 row 1a.1 trigger = "a 64-character str" only (unchanged from V2.7.6;
    # author decision OQ-5 keeps non-hex 64-character behaviour as MISMATCH, not MALFORMED).
    # Hex well-formedness (H-4) still governs the anchor arguments 0.1b/0.1c.
    if not (type(rs) is str and len(rs) == 64):  # 1a.1
        col.emit("RECEIPT_HASH_MALFORMED", "receipt.receipt_sha256")
        layers["L1"] = "FAIL"
    else:
        try:
            h = sha256_json({k: v for k, v in receipt.items() if k != "receipt_sha256"})
        except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
            col.emit("CANONICALIZATION_FAILED", "receipt")  # H-5
            layers["L1"] = "FAIL"
        else:
            if h != rs:  # 1a.2
                col.emit("RECEIPT_HASH_MISMATCH_TAMPER_DETECTED", "receipt.receipt_sha256")
                layers["L1"] = "FAIL"
    if packet_is_mapping:  # 1b
        ps = P.get("packet_sha256")
        if not _well_formed_hash(ps):  # 1b.1
            col.emit("PACKET_HASH_MISSING_OR_MALFORMED", "translation_packet.packet_sha256")
            layers["L1"] = "FAIL"
        else:
            try:
                hp = sha256_json({k: v for k, v in P.items() if k != "packet_sha256"})
            except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
                col.emit("CANONICALIZATION_FAILED", "translation_packet")  # H-5
                layers["L1"] = "FAIL"
            else:
                if hp != ps:  # 1b.2
                    col.emit("PACKET_HASH_MISMATCH_TAMPER_DETECTED", "translation_packet.packet_sha256")
                    layers["L1"] = "FAIL"

    # ---------- Phase 2 / L3 ----------
    AH = None
    ah_ok = False
    layers["L3_BINDING"] = "PASS"
    layers["L3_ANCHOR"] = "NOT_EVALUATED"
    layers["L3_STATE"] = "NOT_EVALUATED"

    if artifact is None:  # B.1
        col.emit("SOURCE_ARTIFACT_REQUIRED_FOR_PROVENANCE_CHECK", "source_frozen_artifact")
        layers["L3_BINDING"] = "FAIL"
    else:
        try:
            AH = artifact_sha256(artifact)
            ah_ok = True
        except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
            col.emit("CANONICALIZATION_FAILED", "artifact")  # H-5; B.2-B.5 do not run
            layers["L3_BINDING"] = "FAIL"
        if ah_ok:
            if not teq(receipt.get("frozen_artifact_sha256"), AH):  # B.2
                col.emit("PROVENANCE_MISMATCH_WITH_SOURCE_ARTIFACT", "receipt.frozen_artifact_sha256")
                layers["L3_BINDING"] = "FAIL"
            if packet_is_mapping and not teq(P.get("frozen_artifact_sha256"), AH):  # B.3
                col.emit("TRANSLATION_PACKET_PROVENANCE_MISMATCH", "translation_packet.frozen_artifact_sha256")
                layers["L3_BINDING"] = "FAIL"
            if qr and qr.get("status") != "INTEGRITY_CHECK_FAILED":  # B.4
                if "frozen_artifact_sha256" not in qr:
                    col.emit("ARTIFACT_HASH_COPY_MISSING", "query_result.frozen_artifact_sha256")
                    layers["L3_BINDING"] = "FAIL"
                elif not teq(qr["frozen_artifact_sha256"], AH):
                    col.emit("ARTIFACT_HASH_COPY_MISMATCH", "query_result.frozen_artifact_sha256")
                    layers["L3_BINDING"] = "FAIL"
            if tr and tr.get("status") != "INTEGRITY_CHECK_FAILED":  # B.5
                # C-1 fix (RG-4): empty sub-object emits nothing (S-1 / §9.1a);
                # status gate mirrors B.4 and the §8.1 applicable-copies matrix.
                if "frozen_artifact_sha256" not in tr:
                    col.emit("ARTIFACT_HASH_COPY_MISSING", "translation_result.frozen_artifact_sha256")
                    layers["L3_BINDING"] = "FAIL"
                elif not teq(tr["frozen_artifact_sha256"], AH):
                    col.emit("ARTIFACT_HASH_COPY_MISMATCH", "translation_result.frozen_artifact_sha256")
                    layers["L3_BINDING"] = "FAIL"

    # L3_ANCHOR (§8.2, §5.3)
    if strict_mode and expected_artifact_sha256 is None:  # A.1
        col.emit("EXTERNAL_ANCHOR_REQUIRED_IN_STRICT_MODE", "expected_artifact_sha256")
        layers["L3_ANCHOR"] = "FAIL"
    elif expected_artifact_sha256 is not None and ah_ok:
        if AH != expected_artifact_sha256:  # A.2
            col.emit("EXPECTED_ARTIFACT_HASH_MISMATCH", "expected_artifact_sha256")
            layers["L3_ANCHOR"] = "FAIL"
        else:
            layers["L3_ANCHOR"] = "PASS"
    # else NOT_EVALUATED (no anchor default mode; or anchor supplied but no artifact/AH)

    # L3_STATE (§8.3)
    copies = []
    if "restored_state_sha256" in receipt:
        copies.append(receipt["restored_state_sha256"])
    if tr.get("status") == "TRANSLATED_FROM_FROZEN_REGISTRY":
        if "restored_state_sha256" in tr:
            copies.append(tr["restored_state_sha256"])
        if packet_is_mapping and "restored_state_sha256" in P:
            copies.append(P["restored_state_sha256"])
    state_fail = False
    if len(copies) >= 2 and not all(teq(copies[0], c) for c in copies[1:]):  # T.1
        col.emit("STATE_HASH_COPY_MISMATCH", "restored_state_sha256")
        state_fail = True
    if expected_restored_state_sha256 is not None:
        if not copies or not all(teq(c, expected_restored_state_sha256) for c in copies):  # T.2
            col.emit("EXPECTED_STATE_HASH_MISMATCH", "expected_restored_state_sha256")
            state_fail = True
    if state_fail:
        layers["L3_STATE"] = "FAIL"
    elif expected_restored_state_sha256 is not None:
        layers["L3_STATE"] = "PASS"
    # else NOT_EVALUATED (no expected hash and T.1 did not fail)

    # ---------- Phase 3 / L2a (§9.1, §9.1a) ----------
    layers["L2"] = "PASS"
    l2a_fail = False
    if not ("receipt_version" in receipt and type(receipt["receipt_version"]) is str):  # V.1
        col.emit("REQUIRED_FIELD_MISSING", "receipt.receipt_version")
        l2a_fail = True

    qr_nonempty = bool(qr)
    tr_nonempty = bool(tr)
    qr_stopped = False
    tr_stopped = False

    if qr_nonempty:
        st = qr.get("status")
        if not legacy and "status" not in qr:  # Q.1
            col.emit("REQUIRED_FIELD_MISSING", "query_result.status")
            l2a_fail = True
        if "status" in qr and st not in ("OK", "NO_MATCH", "INTEGRITY_CHECK_FAILED"):  # Q.2
            col.emit("UNKNOWN_STATUS", "query_result.status")
            l2a_fail = True
        if st == "INTEGRITY_CHECK_FAILED":  # Q.3
            col.emit("INNER_STATUS_INTEGRITY_CHECK_FAILED", "query_result.status")
            l2a_fail = True
            qr_stopped = True
        if not qr_stopped:
            missing_q = [k for k in ("found", "match_count", "symbol_ids", "records")
                         if k not in qr]  # Q.4
            for k in missing_q:
                col.emit("REQUIRED_FIELD_MISSING", "query_result." + k)
                l2a_fail = True
            if "records" in qr:
                for i, rec in enumerate(qr["records"]):
                    if "symbol_id" not in rec:  # Q.4a
                        col.emit("REQUIRED_FIELD_MISSING", "query_result.records[%d].symbol_id" % i)
                        l2a_fail = True
            if "symbol_ids" in qr and "records" in qr \
               and all("symbol_id" in rec for rec in qr["records"]):  # Q.5 (F3 fix: §9.1a exact predicate)
                if not teq(qr["symbol_ids"], [rec["symbol_id"] for rec in qr["records"]]):
                    col.emit("CROSS_FIELD_INCONSISTENT", "query_result.symbol_ids")
                    l2a_fail = True
            if "match_count" in qr and "records" in qr:  # Q.6
                if not teq(qr["match_count"], len(qr["records"])):
                    col.emit("CROSS_FIELD_INCONSISTENT", "query_result.match_count")
                    l2a_fail = True
            if "found" in qr and "records" in qr:  # Q.7
                if not teq(qr["found"], len(qr["records"]) > 0):
                    col.emit("CROSS_FIELD_INCONSISTENT", "query_result.found")
                    l2a_fail = True
            if "status" in qr and "records" in qr:  # Q.8
                ok_expected = len(qr["records"]) > 0
                if (qr["status"] == "OK") != ok_expected:
                    col.emit("CROSS_FIELD_INCONSISTENT", "query_result.status")
                    l2a_fail = True

    if tr_nonempty:
        stt = tr.get("status")
        if "status" not in tr or stt not in _STATUS_TR or \
           (legacy and stt in ("AMBIGUOUS_NO_SILENT_PICK", "INTEGRITY_CHECK_FAILED")):  # X.1
            col.emit("UNKNOWN_STATUS", "translation_result.status")
            l2a_fail = True
            tr_stopped = True
        elif stt == "INTEGRITY_CHECK_FAILED":  # X.2
            col.emit("INNER_STATUS_INTEGRITY_CHECK_FAILED", "translation_result.status")
            l2a_fail = True
            tr_stopped = True
        elif packet_is_mapping != (stt == "TRANSLATED_FROM_FROZEN_REGISTRY"):  # X.3
            col.emit("STATUS_PACKET_INCONSISTENT", "translation_result.translation_packet")
            l2a_fail = True
            tr_stopped = True
        if not tr_stopped:
            required = {
                "TRANSLATED_FROM_FROZEN_REGISTRY": (
                    ["source", "target", "restored_state_sha256"],
                    ["source_symbol_id", "target_symbol_id", "source_script_family",
                     "target_script_family", "source_visible_symbol", "target_visible_symbol",
                     "symbolic_role", "meaning_invariant", "restored_state_sha256"]),
                "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY": ([], []),
                "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY":
                    (["source_symbol_id", "symbolic_role", "target_script_family"], []),
                "AMBIGUOUS_NO_SILENT_PICK":
                    (["source_symbol_id", "symbolic_role", "target_script_family",
                      "ambiguous_candidates"], []),
            }[stt]
            for k in required[0]:  # X.4 (TR keys)
                if k not in tr:
                    col.emit("REQUIRED_FIELD_MISSING", "translation_result." + k)
                    l2a_fail = True
            for k in required[1]:  # X.4 (packet keys, excluding the three owned by L1/L3)
                if k not in P:
                    col.emit("REQUIRED_FIELD_MISSING", "translation_packet." + k)
                    l2a_fail = True
            if stt == "TRANSLATED_FROM_FROZEN_REGISTRY":
                for side in ("source", "target"):
                    if side in tr and "symbol_id" not in tr[side]:  # X.4a
                        col.emit("REQUIRED_FIELD_MISSING", "translation_result.%s.symbol_id" % side)
                        l2a_fail = True
                for side, pk in (("source", "source_symbol_id"), ("target", "target_symbol_id")):
                    if side in tr and "symbol_id" in tr[side] and pk in P:  # X.5
                        if not teq(tr[side]["symbol_id"], P[pk]):
                            col.emit("CROSS_FIELD_INCONSISTENT",
                                     "translation_result.%s.symbol_id" % side)
                            l2a_fail = True
            if stt == "AMBIGUOUS_NO_SILENT_PICK" and "ambiguous_candidates" in tr:
                cands = tr["ambiguous_candidates"]
                if len(cands) < 2:  # X.6 count
                    col.emit("REQUIRED_FIELD_MISSING", "translation_result.ambiguous_candidates")
                    l2a_fail = True
                for i, c in enumerate(cands):
                    for k in ("symbol_id", "visible_symbol"):
                        if k not in c:
                            col.emit("REQUIRED_FIELD_MISSING",
                                     "translation_result.ambiguous_candidates[%d].%s" % (i, k))
                            l2a_fail = True

    # ---------- Phase 3 / L2b (§9.2–§9.4; only if L3_BINDING PASS) ----------
    l2b_ran = False
    l2b_fail = False
    passed_positions = set()

    if layers["L3_BINDING"] == "PASS" and records is not None:
        QR_GATE = qr_nonempty and qr.get("status") != "INTEGRITY_CHECK_FAILED"
        TR_GATE = tr_nonempty and not tr_stopped

        # G-1 positions in §9.2 order (inline below)
        # (rewritten below for clarity)
        if QR_GATE and "symbol_ids" in qr:
            for i, sid in enumerate(qr["symbol_ids"]):
                detail = "query_result.symbol_ids[%d]" % i
                if type(sid) is not str or sid not in records:
                    col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                    l2b_fail = True
                else:
                    passed_positions.add(("q_sym", i))
        if QR_GATE and "records" in qr:
            for i, rec in enumerate(qr["records"]):
                if "symbol_id" in rec:
                    detail = "query_result.records[%d].symbol_id" % i
                    sid = rec["symbol_id"]
                    if type(sid) is not str or sid not in records:
                        col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                        l2b_fail = True
                    else:
                        passed_positions.add(("q_rec", i))
        tr_status = tr.get("status")
        if TR_GATE and tr_status == "TRANSLATED_FROM_FROZEN_REGISTRY":
            for side in ("source", "target"):
                if side in tr and "symbol_id" in tr[side]:
                    detail = "translation_result.%s.symbol_id" % side
                    sid = tr[side]["symbol_id"]
                    if type(sid) is not str or sid not in records:
                        col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                        l2b_fail = True
                    else:
                        passed_positions.add((side,))
            if packet_is_mapping:
                for pk in ("source_symbol_id", "target_symbol_id"):
                    if pk in P:
                        detail = "translation_packet.%s" % pk
                        sid = P[pk]
                        if type(sid) is not str or sid not in records:
                            col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                            l2b_fail = True
                        else:
                            passed_positions.add((pk,))
        if TR_GATE and tr_status in ("NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
                                     "AMBIGUOUS_NO_SILENT_PICK"):
            if "source_symbol_id" in tr:
                detail = "translation_result.source_symbol_id"
                sid = tr["source_symbol_id"]
                if type(sid) is not str or sid not in records:
                    col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                    l2b_fail = True
                else:
                    passed_positions.add(("tr_src",))
            if tr_status == "AMBIGUOUS_NO_SILENT_PICK" and "ambiguous_candidates" in tr:
                for i, c in enumerate(tr["ambiguous_candidates"]):
                    if "symbol_id" in c:
                        detail = "translation_result.ambiguous_candidates[%d].symbol_id" % i
                        sid = c["symbol_id"]
                        if type(sid) is not str or sid not in records:
                            col.emit("SYMBOL_ID_NOT_IN_ARTIFACT", detail)
                            l2b_fail = True
                        else:
                            passed_positions.add(("amb", i))

        # G-2 full-record equality
        if QR_GATE and "records" in qr:
            for i, rec in enumerate(qr["records"]):
                if ("q_rec", i) in passed_positions:
                    if not teq(rec, records[rec["symbol_id"]]):
                        col.emit("RECORD_MISMATCH_WITH_ARTIFACT", "query_result.records[%d]" % i)
                        l2b_fail = True
        for side in ("source", "target"):
            if TR_GATE and tr_status == "TRANSLATED_FROM_FROZEN_REGISTRY" and \
               (side,) in passed_positions:
                rec = tr[side]
                if not teq(rec, records[rec["symbol_id"]]):
                    col.emit("RECORD_MISMATCH_WITH_ARTIFACT", "translation_result." + side)
                    l2b_fail = True

        # G-3 packet derivations
        if TR_GATE and tr_status == "TRANSLATED_FROM_FROZEN_REGISTRY" and packet_is_mapping:
            S = records.get(P.get("source_symbol_id")) if ("source_symbol_id",) in passed_positions else None
            G = records.get(P.get("target_symbol_id")) if ("target_symbol_id",) in passed_positions else None
            # F4 fix (RG-5): G-3 lines in the §9.2 written order (P-7)
            g3_lines = (
                ("source_script_family", S, lambda r: r.get("script_family")),
                ("target_script_family", G, lambda r: r.get("script_family")),
                ("source_visible_symbol", S, lambda r: r.get("visible_symbol")),
                ("target_visible_symbol", G, lambda r: r.get("visible_symbol")),
                ("symbolic_role", S, lambda r: role_norm(r.get("symbolic_role", ""), stamp)),
                ("meaning_invariant", S, lambda r: r.get("meaning_invariant", [])),
            )
            for field, rec, derive in g3_lines:
                if rec is not None and field in P and not teq(P[field], derive(rec)):
                    col.emit("RECORD_MISMATCH_WITH_ARTIFACT", "translation_packet." + field)
                    l2b_fail = True

        # G-4 non-translated
        if TR_GATE and tr_status in ("NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
                                     "AMBIGUOUS_NO_SILENT_PICK") and ("tr_src",) in passed_positions:
            Srec = records[tr["source_symbol_id"]]
            if "symbolic_role" in tr and \
               not teq(tr["symbolic_role"], role_norm(Srec.get("symbolic_role", ""), stamp)):
                col.emit("RECORD_MISMATCH_WITH_ARTIFACT", "translation_result.symbolic_role")
                l2b_fail = True
            if tr_status == "AMBIGUOUS_NO_SILENT_PICK" and "ambiguous_candidates" in tr:
                for i, c in enumerate(tr["ambiguous_candidates"]):
                    if ("amb", i) in passed_positions and "visible_symbol" in c:
                        if not teq(c["visible_symbol"],
                                   records[c["symbol_id"]].get("visible_symbol")):
                            col.emit("RECORD_MISMATCH_WITH_ARTIFACT",
                                     "translation_result.ambiguous_candidates[%d].visible_symbol" % i)
                            l2b_fail = True

        # G-5 frozen_artifact_id
        if "frozen_artifact_id" in artifact:
            if not teq(receipt.get("frozen_artifact_id"), artifact["frozen_artifact_id"]):
                col.emit("FROZEN_ARTIFACT_ID_MISMATCH", "receipt.frozen_artifact_id")
                l2b_fail = True

        # R-1 / R-2 / R-3 (§9.3, §9.4)
        if TR_GATE and tr_status == "TRANSLATED_FROM_FROZEN_REGISTRY" and \
           ("source_symbol_id",) in passed_positions and ("target_symbol_id",) in passed_positions:
            S = records[P["source_symbol_id"]]
            G = records[P["target_symbol_id"]]
            role = role_norm(S.get("symbolic_role", ""), stamp)
            C = candidates(records, role, family_norm(G.get("script_family", ""), stamp), stamp)
            r1_bad = False
            if G not in C:
                r1_bad = True
            if not legacy:
                surfaces = {normalized_surface(r) for r in C}
                if len(surfaces) > 1:
                    r1_bad = True
                first = sorted(C, key=lambda r: str(r["symbol_id"]))[0] if C else None
                if first is not G:
                    r1_bad = True
            if r1_bad:
                col.emit("TARGET_RESOLUTION_INCONSISTENT", "translation_result")
                l2b_fail = True
        if TR_GATE and tr_status == "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY" and \
           ("tr_src",) in passed_positions and "target_script_family" in tr:
            role = role_norm(records[tr["source_symbol_id"]].get("symbolic_role", ""), stamp)
            C = candidates(records, role, family_norm(tr["target_script_family"], stamp), stamp)
            if len(C) != 0:
                col.emit("TARGET_RESOLUTION_INCONSISTENT", "translation_result")
                l2b_fail = True
        r3_pred = (TR_GATE and tr_status == "AMBIGUOUS_NO_SILENT_PICK" and
                   ("tr_src",) in passed_positions and "target_script_family" in tr and
                   "ambiguous_candidates" in tr and
                   all(("amb", i) in passed_positions
                       for i in range(len(tr["ambiguous_candidates"]))))
        if r3_pred:  # C-2 fix (RG-4): rule runs iff its §9.4 predicate is fully met
            role = role_norm(records[tr["source_symbol_id"]].get("symbolic_role", ""), stamp)
            C = candidates(records, role, family_norm(tr["target_script_family"], stamp), stamp)
            ids = [c["symbol_id"] for c in tr["ambiguous_candidates"]]  # all passed (r3_pred)
            r3_bad = False
            if len(set(ids)) != len(ids):
                r3_bad = True
            if set(ids) != {r["symbol_id"] for r in C}:
                r3_bad = True
            if len({normalized_surface(r) for r in C}) <= 1:
                r3_bad = True
            if r3_bad:
                col.emit("TARGET_RESOLUTION_INCONSISTENT", "translation_result")
                l2b_fail = True

        l2b_ran = True

    if l2b_fail or l2a_fail:
        layers["L2"] = "FAIL"
    elif not l2b_ran:
        layers["L2"] = "NOT_EVALUATED" if not l2a_fail else "FAIL"

    # ---------- Phase 4 / L4 (§10) ----------
    layers["L4"] = "PASS"
    if receipt.get("receipt_type") != "EIT_RESTORED_REGISTRY_QUERY_RECEIPT":  # L4.1
        col.emit("WRONG_RECEIPT_TYPE", "receipt.receipt_type")
        layers["L4"] = "FAIL"
    bmap = boundary if type(boundary) is dict else {}
    for k, expected in BOUNDARY_PAIRS:  # L4.2
        if bmap.get(k) is not expected:
            col.emit("BOUNDARY_VIOLATION:" + k, "boundary." + k)
            layers["L4"] = "FAIL"
    if strict_mode:
        pair = (stamp, receipt.get("module_id"))
        versions = [v for v, _ in ALLOW_LIST]
        if stamp not in versions:  # L4.3
            col.emit("POLICY_RECEIPT_VERSION_NOT_ALLOWED", "receipt.receipt_version")
            layers["L4"] = "FAIL"
        elif pair not in ALLOW_LIST:
            col.emit("POLICY_MODULE_ID_NOT_ALLOWED", "receipt.module_id")
            layers["L4"] = "FAIL"
        if packet_is_mapping and not teq(P.get("packet_version"), stamp):  # L4.4
            # F5 fix (RG-5, author option (a)): builders must write packet_version;
            # a missing key now fails the same check instead of being skipped (spec gap decision).
            col.emit("POLICY_RECEIPT_VERSION_NOT_ALLOWED", "translation_packet.packet_version")
            layers["L4"] = "FAIL"
        ts = receipt.get("generated_at_utc")  # L4.5
        ts_ok = False
        if type(ts) is str:
            try:
                dt = datetime.fromisoformat(ts)
                off = dt.utcoffset()
                ts_ok = (off is not None and off == timedelta(0))
            except (ValueError, OverflowError):
                ts_ok = False
        if not ts_ok:
            col.emit("POLICY_TIMESTAMP_MALFORMED", "receipt.generated_at_utc")
            layers["L4"] = "FAIL"

    # ---------- result (§4) ----------
    failures = [c for c, _ in col.entries]
    verified = (col.occurred == 0)
    if not verified:
        assurance = "NONE"
    elif layers["L3_ANCHOR"] != "PASS":
        assurance = "CONSISTENCY_ONLY"
    elif layers["L3_STATE"] != "PASS":
        assurance = "ARTIFACT_ANCHORED"
    else:
        assurance = "ARTIFACT_AND_STATE_ANCHORED"
    # Q4 (OPEN — chosen option: declared): V2.7.6 returns the DECLARED stored receipt_sha256,
    # not a recomputed value (see original receipt_verifier.py return dict).
    declared = receipt.get("receipt_sha256")
    return {
        "check_type": "VERIFY_RESTORED_QUERY_RECEIPT",  # Q1
        "verified": verified,
        "failures": failures,
        "failure_details": [d for _, d in col.entries],
        "receipt_sha256": declared,
        "layers": layers,
        "assurance": assurance,
        "safety": dict(SAFETY_BLOCK),  # Q2 RESOLVED (byte-verified, see module docstring)
    }


def _l0_result(col, layers, failure, receipt, raw=False):
    if raw:
        code, detail = failure
    else:
        # Non-raw path: L0 reports single failure string as both code and detail
        code = failure
        detail = failure
    col2 = _Collector()
    col2.emit(code if raw else failure, detail)
    layers["L0"] = "FAIL"
    # F1 fix (RG-5): §6.1 forbids ANY key lookup on the receipt before its scan passed.
    # On an L0 failure no lookup may occur, so no declared value can be read back.
    # Returned receipt_sha256 = None (author decision recorded with Tasklet; ratification pending).
    declared = None
    return {
        "check_type": "VERIFY_RESTORED_QUERY_RECEIPT",
        "verified": False,
        "failures": [c for c, _ in col2.entries],
        "failure_details": [d for _, d in col2.entries],
        "receipt_sha256": declared,  # Q4: declared passthrough; contract OPEN
        "layers": layers,
        "assurance": "NONE",
        "safety": dict(SAFETY_BLOCK),  # Q5: V2.7.6 single return site; always dict copy
    }
