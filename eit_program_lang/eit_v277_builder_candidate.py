"""EIT V2.7.7 builder candidate — query + translation lookup + receipt/packet builders.

SPEC: EIT_V277_P003_NORMATIVE_PATCH_SPEC_V0.5.9.md (3fc10557...d384f27c), §10.3 stamps.
AUTH: EIT_V277_AUTHORIZATION_FOR_FAILFIRST_V0.2 + author decision "go + builder" (20:36,
EIT_V277_AUTHOR_DECISION_RG4_GO_AND_BUILDER_V0.1.md, 64357ac7...fd2f00).
SEMANTICS: ported by STATIC READING of V2.7.6 sources (EIT_V2_7_6.zip 3b99157e...e22c;
restored_registry_query.py, frozen_translation_lookup.py, unicode_normalization.py,
restored_query_receipt.py). No project code executed. Stamps are the §10.3 2.7.7 triple.
STATUS: CANDIDATE / NOT_RELEASED. Builder assumes a well-formed state (the V2.7.6
integrity gate is exercised separately through the verifier tests).
artifact_sha256 is ALWAYS a parameter: the hash of the artifact mapping as supplied,
never a field inside the artifact (self-reference would change the hash).
"""
import sys, os, importlib.util, copy
from datetime import datetime, timezone

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("receipt_verifier_v277_candidate",
                                               os.path.join(_here, "receipt_verifier_v277_candidate.py"))
_v = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_v)
sha256_json = _v.sha256_json
nfc = _v.nfc
SAFETY_BLOCK = _v.SAFETY_BLOCK

# Successor-only sibling helper load preserves standalone file loading.
_lookup_spec = importlib.util.spec_from_file_location(
    "eit_successor_lookup_identity", os.path.join(_here, "lookup_identity.py"))
_lookup = importlib.util.module_from_spec(_lookup_spec)
_lookup_spec.loader.exec_module(_lookup)
LookupIdentityError = _lookup.LookupIdentityError
build_id_projection = _lookup.build_id_projection
resolve_id = _lookup.resolve_id
get_lookup_records = _lookup.get_lookup_records

STAMP = "2.7.7"
MODULE_ID = "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7"


def _records(state):
    return get_lookup_records(state)


# ---------- query (ported semantics: blob-id -> surface -> aliases -> sound_hint) ----------
def query_restored_registry(state, query, artifact_sha256=None, *, s1_context=None):
    if s1_context is not None:
        return s1_context.run_builder(
            state, query, None, artifact_sha256,
            make_receipt=build_restored_query_receipt, safety=SAFETY_BLOCK,
            operation="query")
    records = _records(state)
    projection = build_id_projection(records, nfc)
    raw_id = resolve_id(projection, query, nfc)
    q = nfc(query)
    if raw_id is not None:
        blob = records[raw_id]
        return {"status": "OK", "found": True, "match_count": 1, "symbol_ids": [blob.get("symbol_id")],
                "records": [copy.deepcopy(blob)], "frozen_artifact_sha256": artifact_sha256}
    ql = q.lower()
    for rec in records.values():
        if nfc(rec.get("visible_symbol", "")) == q:
            return {"status": "OK", "found": True, "match_count": 1, "symbol_ids": [rec.get("symbol_id")],
                    "records": [copy.deepcopy(rec)], "frozen_artifact_sha256": artifact_sha256}
    for rec in records.values():
        if ql in [nfc(a).lower() for a in rec.get("aliases", []) or []]:
            return {"status": "OK", "found": True, "match_count": 1, "symbol_ids": [rec.get("symbol_id")],
                    "records": [copy.deepcopy(rec)], "frozen_artifact_sha256": artifact_sha256}
    for rec in records.values():
        if ql == nfc(rec.get("sound_hint", "")).lower():
            return {"status": "OK", "found": True, "match_count": 1, "symbol_ids": [rec.get("symbol_id")],
                    "records": [copy.deepcopy(rec)], "frozen_artifact_sha256": artifact_sha256}
    return {"status": "NO_MATCH", "found": False, "match_count": 0, "symbol_ids": [], "records": [],
            "frozen_artifact_sha256": artifact_sha256}


def _resolve_source(records, query):
    projection = build_id_projection(records, nfc)
    raw_id = resolve_id(projection, query, nfc)
    q = nfc(query)
    if raw_id is not None:
        return records[raw_id]
    ql = q.lower()
    for rec in records.values():
        if nfc(rec.get("visible_symbol", "")) == q:
            return rec
    for rec in records.values():
        if ql in [nfc(a).lower() for a in rec.get("aliases", []) or []]:
            return rec
    for rec in records.values():
        if ql == nfc(rec.get("sound_hint", "")).lower():
            return rec
    return None


def _resolve_candidates(cands):
    if not cands:
        return {"status": "NO_CANDIDATES", "chosen": None, "candidates": []}
    surfaces = {nfc(c.get("visible_symbol")) for c in cands}
    if len(cands) == 1 or len(surfaces) == 1:
        return {"status": "RESOLVED" if len(cands) == 1 else "RESOLVED_IDENTICAL_SURFACES",
                "chosen": sorted(cands, key=lambda c: str(c.get("symbol_id")))[0],
                "candidates": sorted(cands, key=lambda c: str(c.get("symbol_id")))}
    return {"status": "AMBIGUOUS_NO_SILENT_PICK", "chosen": None,
            "candidates": sorted(cands, key=lambda c: str(c.get("symbol_id")))}


# ---------- translation lookup ----------
def lookup_translation_from_frozen_registry(state, source_query, target_script_family, artifact_sha256=None, *, s1_context=None):
    if s1_context is not None:
        return s1_context.run_builder(
            state, source_query, target_script_family, artifact_sha256,
            make_receipt=build_restored_query_receipt, safety=SAFETY_BLOCK,
            operation="translation")
    records = _records(state)
    source = _resolve_source(records, source_query)
    if source is None:
        return {"status": "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY", "source_query": source_query,
                "target_script_family": target_script_family, "frozen_artifact_sha256": artifact_sha256,
                "translation_packet": None}
    role = nfc(source.get("symbolic_role", "")).upper()
    tf = nfc(target_script_family).upper()
    cands = [r for r in records.values()
             if nfc(r.get("symbolic_role", "")).upper() == role and nfc(r.get("script_family", "")).upper() == tf]
    if not cands:
        return {"status": "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
                "source_symbol_id": source.get("symbol_id"), "symbolic_role": role,
                "target_script_family": target_script_family,
                "frozen_artifact_sha256": artifact_sha256, "translation_packet": None}
    res = _resolve_candidates(cands)
    if res["status"] == "AMBIGUOUS_NO_SILENT_PICK":
        return {"status": "AMBIGUOUS_NO_SILENT_PICK", "source_symbol_id": source.get("symbol_id"),
                "symbolic_role": role, "target_script_family": target_script_family,
                "ambiguous_candidates": [{"symbol_id": c.get("symbol_id"),
                                          "visible_symbol": c.get("visible_symbol")}
                                         for c in res["candidates"]],
                "frozen_artifact_sha256": artifact_sha256, "translation_packet": None}
    target = res["chosen"]
    packet = {"packet_type": "FROZEN_REGISTRY_TRANSLATION_PACKET", "packet_version": STAMP,
              "source_symbol_id": source.get("symbol_id"), "target_symbol_id": target.get("symbol_id"),
              "source_script_family": source.get("script_family"), "target_script_family": target.get("script_family"),
              "source_visible_symbol": source.get("visible_symbol"), "target_visible_symbol": target.get("visible_symbol"),
              "symbolic_role": role, "meaning_invariant": copy.deepcopy(source.get("meaning_invariant", [])),
              "frozen_artifact_sha256": artifact_sha256,
              "restored_state_sha256": state.get("restored_state_sha256"),
              "read_only": True, "boundary": dict(SAFETY_BLOCK)}
    packet["packet_sha256"] = sha256_json(packet)
    tr = {"status": "TRANSLATED_FROM_FROZEN_REGISTRY", "source": copy.deepcopy(source),
          "target": copy.deepcopy(target), "translation_packet": packet,
          "frozen_artifact_sha256": artifact_sha256,
          "restored_state_sha256": state.get("restored_state_sha256")}
    return tr


# ---------- receipt builder (§10.3 stamps) ----------
def build_restored_query_receipt(state, query_result=None, translation_result=None, artifact_sha256=None):
    receipt = {
        "receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT",
        "receipt_version": STAMP,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "module_id": MODULE_ID,
        "author": "Mr. Toni Mladenovski",
        "project_origin_date": "18 April 2026",
        "restored_state_id": state.get("restored_state_id"),
        "release_id": state.get("release_id"),
        "frozen_artifact_id": state.get("frozen_artifact_id"),
        "frozen_artifact_sha256": artifact_sha256,
        "restored_state_sha256": state.get("restored_state_sha256"),
        "current_version_id": state.get("current_version_id"),
        "query_result": query_result or {},
        "translation_result": translation_result or {},
        "boundary": dict(SAFETY_BLOCK),
    }
    receipt["receipt_sha256"] = sha256_json(receipt)
    return receipt


def run_query_with_receipt(state, query, target_script_family=None, artifact_sha256=None, *, s1_context=None):
    """Convenience: query (+ optional translation), receipts attached per §8.1 copy matrix.
    artifact_sha256 is the hash of the artifact AS SUPPLIED (parameter, not stored in it)."""
    if s1_context is not None:
        return s1_context.run_builder(
            state, query, target_script_family, artifact_sha256,
            make_receipt=build_restored_query_receipt, safety=SAFETY_BLOCK,
            operation="joint")
    # Preflight before either result or any receipt is built.
    resolve_id(build_id_projection(_records(state), nfc), query, nfc)
    qr = query_restored_registry(state, query, artifact_sha256)
    tr = {}
    if target_script_family is not None:
        tr = lookup_translation_from_frozen_registry(state, query, target_script_family, artifact_sha256)
    return build_restored_query_receipt(state, qr, tr, artifact_sha256)
