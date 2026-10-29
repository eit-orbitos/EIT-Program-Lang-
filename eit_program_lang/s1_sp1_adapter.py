"""Author-only S1 adapter candidate: explicit core and owner callbacks, no loader.

This module does not import project modules or establish a trusted owner root.
Legacy B/T calls remain opt-in and unprotected. Logical return-boundary staging
is not an OS transaction, producer authentication, or C3-E routing enforcement.
Callback contracts and known evidence gaps are recorded in ADAPTER_NOTES.md.
"""

import copy
import hashlib
import json
import types
import unicodedata
from asyncio import CancelledError as AsyncCancelledError
from concurrent.futures import CancelledError as FutureCancelledError


def _sha256_json(value):
    # Unchanged compact state/packet/receipt hash domain, not artifact domain.
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _artifact_sha256(value):
    # Original artifact domain deliberately retains default JSON separators.
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _teq(left, right):
    """Exact native-type equality; bool is not an int and no custom hooks."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (left.keys() == right.keys()
                and all(_teq(left[key], right[key]) for key in left))
    if type(left) is list:
        return (len(left) == len(right)
                and all(_teq(a, b) for a, b in zip(left, right)))
    return left == right


def _digest(value):
    return (type(value) is str and len(value) == 64
            and all(char in "0123456789abcdef" for char in value))


class S1Adapter:
    """One owner-configured context using the exact supplied core/error classes.

    trusted_control_check() -> exact bool
    binding_check(snapshot_copy, declared_layout, artifact_sha256) -> exact bool
    builder_integrity_check(snapshot_copy) -> original-style integrity mapping

    Runtime uses the unchanged T verify_restored_state callback instead. An
    integrity mapping must contain exact-bool ``verified``; no truth coercion.
    Copies passed to callbacks are private, not the operation snapshot. Owner
    root/custody/loader and callback provenance are NOT established here.
    """

    def __init__(self, core, *, binding_check=None, builder_integrity_check=None,
                 trusted_control_check=None):
        # An invalid/missing core cannot supply its own typed readiness class.
        if type(core) is not types.ModuleType:
            raise TypeError("explicit S1 core module is required")
        self.core = core
        required = ("admit_native", "validate_identity", "validate_arguments",
                    "validate_fields", "select_source", "select_target",
                    "guard_output", "S1ResolutionError", "S1ControlStop",
                    "S1ReadinessBlocked")
        if not callable(getattr(core, "S1ReadinessBlocked", None)):
            raise TypeError("core lacks its readiness exception")
        if (any(not callable(getattr(core, name, None)) for name in required)
                or not callable(binding_check)
                or not callable(builder_integrity_check)
                or not callable(trusted_control_check)):
            raise core.S1ReadinessBlocked("owner callbacks/core configuration absent")
        self._binding_check = binding_check
        self._builder_integrity_check = builder_integrity_check
        self._trusted_control_check = trusted_control_check

    def _fail(self, reason, phase):
        raise self.core.S1ResolutionError(reason, phase)

    def _at(self, phase, operation):
        try:
            return operation()
        except (self.core.S1ResolutionError, self.core.S1ControlStop,
                self.core.S1ReadinessBlocked):
            raise
        except (TimeoutError, AsyncCancelledError, FutureCancelledError,
                KeyboardInterrupt, SystemExit) as error:
            raise self.core.S1ResolutionError("S1_OPERATION_ABORTED", phase) from error
        except Exception as error:
            raise self.core.S1ResolutionError("S1_INTERNAL_ERROR", phase) from error

    def _trusted(self):
        try:
            accepted = self._trusted_control_check()
        except BaseException as error:
            raise self.core.S1ControlStop("trusted controls compromised") from error
        if type(accepted) is not bool or not accepted:
            raise self.core.S1ControlStop("trusted controls compromised")

    def _owner_call(self, callback, *args):
        # Owner callback failures are not semantic core rejections. Even a
        # callback-raised S1ResolutionError must not forge a different phase.
        try:
            return callback(*args)
        except (TimeoutError, AsyncCancelledError, FutureCancelledError,
                KeyboardInterrupt, SystemExit):
            raise
        except Exception as error:
            raise self.core.S1ResolutionError("S1_INTERNAL_ERROR", 2) from error

    def _layout(self, state, layout):
        container = state
        path = (("frozen_artifact",) if layout == "runtime_nested" else ())
        path += ("frozen_registry_snapshot", "registry_records")
        for field in path:
            if type(container) is not dict or field not in container:
                self._fail("S1_INVALID_STATE", 2)
            container = container[field]
        if type(container) is not dict:
            self._fail("S1_INVALID_STATE", 2)
        return container

    def _state_coherent(self, state, artifact_hash, layout):
        if (not _digest(artifact_hash)
                or state.get("frozen_artifact_sha256") != artifact_hash
                or not _digest(state.get("restored_state_sha256"))):
            return False
        body = {key: value for key, value in state.items()
                if key != "restored_state_sha256"}
        if _sha256_json(body) != state["restored_state_sha256"]:
            return False
        if layout == "runtime_nested":
            if _artifact_sha256(state["frozen_artifact"]) != artifact_hash:
                return False
        # Direct layout does not identify an artifact mapping to hash; that
        # binding remains the explicit owner's obligation, never synthesized.
        return True

    def _prepare(self, state, artifact_hash, layout, integrity):
        self._at(1, lambda: self.core.admit_native(state))
        # Copy failure is an active Phase-1 failure, never lookup absence.
        snapshot = self._at(1, lambda: copy.deepcopy(state))

        def phase_two():
            records = self._layout(snapshot, layout)
            self._trusted()
            effective_hash = (snapshot.get("frozen_artifact_sha256")
                              if layout == "runtime_nested" else artifact_hash)
            accepted = self._owner_call(self._binding_check, copy.deepcopy(snapshot),
                                        layout, effective_hash)
            if type(accepted) is not bool:
                self._fail("S1_INTERNAL_ERROR", 2)
            if not accepted:
                # Integrity callback is deliberately NOT_INVOKED on denial.
                self._fail("S1_INTEGRITY_DENIED", 2)
            # M6 candidate rule: missing/body-incoherent state hash denies;
            # callback approval never fabricates a hash or bypasses this rule.
            if not self._state_coherent(snapshot, effective_hash, layout):
                self._fail("S1_INTEGRITY_DENIED", 2)
            checked = self._owner_call(integrity, copy.deepcopy(snapshot))
            if type(checked) is not dict or type(checked.get("verified")) is not bool:
                self._fail("S1_INTERNAL_ERROR", 2)
            if not checked["verified"]:
                self._fail("S1_INTEGRITY_DENIED", 2)
            return records, effective_hash

        records, effective_hash = self._at(2, phase_two)
        return snapshot, records, effective_hash

    def _decide(self, records, query, target, translation):
        projection = self._at(3, lambda: self.core.validate_identity(records))

        def arguments():
            self.core.validate_arguments(query, target)
            # None is wrapper omission only, never a valid direct T target.
            if translation and target is None:
                self._fail("S1_TARGET_ARGUMENT_INVALID", 4)

        self._at(4, arguments)
        self._at(5, lambda: self.core.validate_fields(records))
        source_id = self._at(6, lambda: self.core.select_source(records, projection, query))
        resolution = None
        if translation and source_id is not None:
            resolution = self._at(7, lambda: self.core.select_target(records, source_id, target))
        return source_id, resolution

    def _query(self, records, source_id, artifact_hash):
        if source_id is None:
            return {"status": "NO_MATCH", "found": False, "match_count": 0,
                    "symbol_ids": [], "records": [],
                    "frozen_artifact_sha256": artifact_hash}
        record = records[source_id]
        return {"status": "OK", "found": True, "match_count": 1,
                "symbol_ids": [record["symbol_id"]],
                "records": [copy.deepcopy(record)],
                "frozen_artifact_sha256": artifact_hash}

    def _translation(self, state, records, source_id, resolution, query,
                     target_argument, artifact_hash, safety, runtime):
        stamp = "2.7.6" if runtime else "2.7.7"
        if source_id is None:
            result = {"status": "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY",
                      "source_query": query, "target_script_family": target_argument,
                      "frozen_artifact_sha256": artifact_hash,
                      "translation_packet": None}
        else:
            source = records[source_id]
            role = resolution["role"]
            if resolution["status"] == "NO_TARGET":
                result = {"status": "NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY",
                          "source_symbol_id": source_id, "symbolic_role": role,
                          "target_script_family": target_argument,
                          "frozen_artifact_sha256": artifact_hash,
                          "translation_packet": None}
            elif resolution["status"] == "AMBIGUOUS":
                result = {"status": "AMBIGUOUS_NO_SILENT_PICK",
                          "source_symbol_id": source_id, "symbolic_role": role,
                          "target_script_family": target_argument,
                          "ambiguous_candidates": [
                              {"symbol_id": raw_id,
                               "visible_symbol": records[raw_id]["visible_symbol"]}
                              for raw_id in resolution["candidates"]],
                          "frozen_artifact_sha256": artifact_hash,
                          "translation_packet": None}
            elif resolution["status"] == "TRANSLATED":
                target = records[resolution["chosen"]]
                packet = {
                    "packet_type": "FROZEN_REGISTRY_TRANSLATION_PACKET",
                    "packet_version": stamp,
                    "source_symbol_id": source_id,
                    "target_symbol_id": target["symbol_id"],
                    "source_script_family": source["script_family"],
                    "target_script_family": target["script_family"],
                    "source_visible_symbol": source["visible_symbol"],
                    "target_visible_symbol": target["visible_symbol"],
                    "symbolic_role": role,
                    "meaning_invariant": copy.deepcopy(source.get("meaning_invariant", [])),
                    "frozen_artifact_sha256": artifact_hash,
                    "restored_state_sha256": state["restored_state_sha256"],
                    "read_only": True, "boundary": copy.deepcopy(safety)}
                packet["packet_sha256"] = _sha256_json(packet)
                result = {"status": "TRANSLATED_FROM_FROZEN_REGISTRY",
                          "source": copy.deepcopy(source), "target": copy.deepcopy(target),
                          "translation_packet": packet,
                          "frozen_artifact_sha256": artifact_hash,
                          "restored_state_sha256": state["restored_state_sha256"]}
            else:
                self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if runtime:
            result["read_only"] = True
            result["safety"] = copy.deepcopy(safety)
        return result

    def _coherent(self, state, records, source_id, resolution, query_result,
                  translation_result, artifact_hash, query, target_argument, safety, runtime):
        """M13/M15 candidate prepublication checks; not a verifier replacement."""
        layout = "runtime_nested" if runtime else "builder_direct"
        if not self._state_coherent(state, artifact_hash, layout):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if source_id is not None and source_id not in records:
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if query_result is not None:
            if not _teq(query_result, self._query(records, source_id, artifact_hash)):
                self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if translation_result is None:
            return
        packet = translation_result.get("translation_packet")
        translated = (translation_result.get("status") == "TRANSLATED_FROM_FROZEN_REGISTRY")
        if translated != (source_id is not None and resolution is not None
                          and resolution["status"] == "TRANSLATED"):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if translation_result.get("frozen_artifact_sha256") != artifact_hash:
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        if not translated:
            if packet is not None:
                self._fail("S1_INTERNAL_BINDING_ERROR", 8)
            if source_id is None:
                expected_result = {
                    "status": "NO_SOURCE_MATCH_IN_FROZEN_REGISTRY",
                    "source_query": query, "target_script_family": target_argument,
                    "frozen_artifact_sha256": artifact_hash, "translation_packet": None}
            else:
                expected_result = {
                    "status": ("NO_TARGET_SCRIPT_MATCH_IN_FROZEN_REGISTRY"
                               if resolution["status"] == "NO_TARGET"
                               else "AMBIGUOUS_NO_SILENT_PICK"),
                    "source_symbol_id": source_id, "symbolic_role": resolution["role"],
                    "target_script_family": target_argument,
                    "frozen_artifact_sha256": artifact_hash, "translation_packet": None}
                if resolution["status"] == "AMBIGUOUS":
                    expected_result["ambiguous_candidates"] = [
                        {"symbol_id": raw_id,
                         "visible_symbol": records[raw_id]["visible_symbol"]}
                        for raw_id in resolution["candidates"]]
                elif resolution["status"] != "NO_TARGET":
                    self._fail("S1_INTERNAL_BINDING_ERROR", 8)
            if runtime:
                expected_result.update(read_only=True, safety=safety)
            if not _teq(translation_result, expected_result):
                self._fail("S1_INTERNAL_BINDING_ERROR", 8)
            return
        if type(packet) is not dict:
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        source = records[source_id]
        chosen = resolution["chosen"]
        if chosen not in records or chosen not in resolution["candidates"]:
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        target = records[chosen]
        role = unicodedata.normalize("NFC", source["symbolic_role"]).upper()
        family = unicodedata.normalize("NFC", target_argument).upper()
        if (not role or role != resolution["role"]
                or unicodedata.normalize("NFC", target["symbolic_role"]).upper() != role
                or unicodedata.normalize("NFC", target["script_family"]).upper() != family
                or not _teq(translation_result.get("source"), source)
                or not _teq(translation_result.get("target"), target)
                or translation_result.get("restored_state_sha256") != state["restored_state_sha256"]):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        expected = {
            "packet_type": "FROZEN_REGISTRY_TRANSLATION_PACKET",
            "packet_version": "2.7.6" if runtime else "2.7.7",
            "source_symbol_id": source_id, "target_symbol_id": chosen,
            "source_script_family": source["script_family"],
            "target_script_family": target["script_family"],
            "source_visible_symbol": source["visible_symbol"],
            "target_visible_symbol": target["visible_symbol"],
            "symbolic_role": role,
            "meaning_invariant": source.get("meaning_invariant", []),
            "frozen_artifact_sha256": artifact_hash,
            "restored_state_sha256": state["restored_state_sha256"],
            "read_only": True, "boundary": safety}
        expected["packet_sha256"] = _sha256_json(expected)
        if not _teq(packet, expected):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        expected_result = {
            "status": "TRANSLATED_FROM_FROZEN_REGISTRY",
            "source": source, "target": target, "translation_packet": expected,
            "frozen_artifact_sha256": artifact_hash,
            "restored_state_sha256": state["restored_state_sha256"]}
        if runtime:
            expected_result.update(read_only=True, safety=safety)
        if not _teq(translation_result, expected_result):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)

    def _receipt(self, make_receipt, state, query_result, translation_result,
                 artifact_hash, safety):
        # Original builder receives copies; it cannot alter the pinned snapshot
        # or the staged results used for coherence checks.
        receipt = make_receipt(copy.deepcopy(state), copy.deepcopy(query_result),
                               copy.deepcopy(translation_result), artifact_hash)
        expected = {
            "receipt_type": "EIT_RESTORED_REGISTRY_QUERY_RECEIPT",
            "receipt_version": "2.7.7",
            "module_id": "EIT_PROGRAM_LANG_NOVA_Q_ANALYZER_V2_7_7",
            "author": "Mr. Toni Mladenovski", "project_origin_date": "18 April 2026",
            "restored_state_id": state.get("restored_state_id"),
            "release_id": state.get("release_id"),
            "frozen_artifact_id": state.get("frozen_artifact_id"),
            "frozen_artifact_sha256": artifact_hash,
            "restored_state_sha256": state["restored_state_sha256"],
            "current_version_id": state.get("current_version_id"),
            "query_result": query_result, "translation_result": translation_result,
            "boundary": safety}
        if type(receipt) is not dict:
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        # Do not inspect or compare hostile returned objects before admission.
        self.core.guard_output(receipt)
        if (set(receipt) != set(expected) | {"generated_at_utc", "receipt_sha256"}
                or type(receipt.get("generated_at_utc")) is not str
                or not receipt["generated_at_utc"]
                or any(not _teq(receipt.get(key), value) for key, value in expected.items())
                or receipt.get("receipt_sha256") != _sha256_json(
                    {key: value for key, value in receipt.items() if key != "receipt_sha256"})):
            self._fail("S1_INTERNAL_BINDING_ERROR", 8)
        return receipt

    def _publish(self, build):
        def final_stage():
            self._trusted()
            try:
                result = build()
            except (self.core.S1ResolutionError, self.core.S1ControlStop,
                    self.core.S1ReadinessBlocked):
                raise
            except (TimeoutError, AsyncCancelledError, FutureCancelledError,
                    KeyboardInterrupt, SystemExit):
                raise
            except Exception as error:
                raise self.core.S1ResolutionError("S1_OUTPUT_BUILD_ERROR", 8) from error
            self.core.guard_output(result)
            self._trusted()
            return result
        return self._at(8, final_stage)

    def run_builder(self, state, query, target, artifact_sha256, *,
                    make_receipt, safety, operation):
        if operation not in ("query", "translation", "joint") or not callable(make_receipt):
            raise self.core.S1ReadinessBlocked("invalid builder endpoint configuration")
        snapshot, records, artifact_hash = self._prepare(
            state, artifact_sha256, "builder_direct", self._builder_integrity_check)
        translation = operation == "translation" or (operation == "joint" and target is not None)
        source_id, resolution = self._decide(records, query, target, translation)

        def build():
            # Safety is the original endpoint constant, copied and guarded;
            # never obtained from caller state or translated records.
            boundary = copy.deepcopy(safety)
            self.core.guard_output(boundary)
            qr = self._query(records, source_id, artifact_hash) if operation != "translation" else None
            tr = (self._translation(snapshot, records, source_id, resolution, query,
                                    target, artifact_hash, boundary, False)
                  if translation else None)
            self._coherent(snapshot, records, source_id, resolution, qr, tr,
                           artifact_hash, query, target, boundary, False)
            if operation == "joint":
                return self._receipt(make_receipt, snapshot, qr, tr or {}, artifact_hash, boundary)
            return tr if operation == "translation" else qr

        return self._publish(build)

    def run_runtime(self, state, query, target, *, verify_integrity, safety):
        if not callable(verify_integrity):
            raise self.core.S1ReadinessBlocked("runtime integrity callback absent")
        snapshot, records, artifact_hash = self._prepare(
            state, None, "runtime_nested", verify_integrity)
        source_id, resolution = self._decide(records, query, target, True)

        def build():
            boundary = copy.deepcopy(safety)
            self.core.guard_output(boundary)
            result = self._translation(snapshot, records, source_id, resolution, query,
                                       target, artifact_hash, boundary, True)
            self._coherent(snapshot, records, source_id, resolution, None, result,
                           artifact_hash, query, target, boundary, True)
            return result

        return self._publish(build)
