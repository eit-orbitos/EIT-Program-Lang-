"""Actual unittest source, authored but NOT imported/collected/executed.

Every fixture and oracle: UNAPPROVED. Synthetic callbacks do NOT establish an
owner root, artifact authenticity, installed routing, or mutation-battery closure.
The runner must inject CONTEXT using explicit candidate file loading.
"""
import copy
import hashlib
import importlib.util
import json
import unittest
from unittest.mock import patch

CONTEXT = None
ARTIFACT_HASH = "a" * 64  # synthetic placeholder, not a genuine artifact digest
MAX_VISITS = 262_144
MAX_TEXT = 16_777_216
MAX_OUTPUT = 33_554_432


def nested(depth, leaf=None):
    """Root1: scalar is depth1; each list adds one value edge."""
    result = leaf
    for _ in range(depth - 1):
        result = [result]
    return result


def record(sid, visible="source", family="LATIN", role="ROLE", **extras):
    result = dict(symbol_id=sid, visible_symbol=visible, script_family=family,
                  symbolic_role=role, aliases=[], sound_hint="", meaning_invariant=["meaning"])
    result.update(extras)
    return result


def sample_records():
    return {"src": record("src"), "dst": record("dst", "target", "GREEK")}


def seal_synthetic(state):
    """Existing distinct hash domains; computed consistency is NOT owner binding."""
    if "frozen_artifact" in state:
        raw = json.dumps(state["frozen_artifact"], sort_keys=True, ensure_ascii=False).encode("utf-8")
        state["frozen_artifact_sha256"] = hashlib.sha256(raw).hexdigest()
    body = {k: v for k, v in state.items() if k != "restored_state_sha256"}
    raw = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")
    state["restored_state_sha256"] = hashlib.sha256(raw).hexdigest()
    return state


def state_for(records=None, runtime=False):
    # Synthetic hash-consistent control-flow fixtures, NOT owner-authenticated states.
    snapshot = {"registry_records": sample_records() if records is None else records}
    state = dict(restored_state_id="SYNTHETIC", release_id="SYNTHETIC",
                 frozen_artifact_id="SYNTHETIC", current_version_id="SYNTHETIC",
                 frozen_artifact_sha256=ARTIFACT_HASH)
    if runtime:
        state["frozen_artifact"] = {"frozen_registry_snapshot": snapshot}
    else:
        state["frozen_registry_snapshot"] = snapshot
    return seal_synthetic(state)


class Harness(unittest.TestCase):
    def setUp(self):
        if CONTEXT is None:
            self.fail("Use run_regressions.py with an explicit candidate root; discovery alone is unsupported")
        self.c = CONTEXT.core
        self.b = CONTEXT.builder
        self.t = CONTEXT.runtime
        self.events = []

    def error(self, reason, phase, function, *args, **kwargs):
        with self.assertRaises(self.c.S1ResolutionError) as caught:
            function(*args, **kwargs)
        self.assertEqual((caught.exception.reason, caught.exception.phase), (reason, phase))
        return caught.exception

    def adapter(self, binding=True, integrity=True, control=True, mutate_original=None):
        # Deliberately SYNTHETIC test doubles, not provisioned owner callbacks.
        def trusted():
            self.events.append("control")
            return control
        def bind(snapshot, layout, artifact_sha256):
            self.events.append("binding")
            if mutate_original is not None:
                mutate_original()
            return binding
        def verify(*args, **kwargs):
            self.events.append("integrity")
            return {"verified": integrity, "failures": [] if integrity else ["SYNTHETIC_DENIAL"]}
        return CONTEXT.adapter.S1Adapter(self.c, binding_check=bind,
                                        builder_integrity_check=verify,
                                        trusted_control_check=trusted)

    def receipt(self, *args, **kwargs):
        self.events.append("receipt")
        return self.b.build_restored_query_receipt(*args, **kwargs)

    def build(self, state, query="src", target="GREEK", adapter=None, operation="joint"):
        return (adapter or self.adapter()).run_builder(
            state, query, target, ARTIFACT_HASH, make_receipt=self.receipt,
            safety=self.b.SAFETY_BLOCK, operation=operation)

    def runtime(self, state, query="src", target="GREEK", adapter=None, verified=True):
        def verify(snapshot):
            self.events.append("runtime_integrity")
            return {"verified": verified, "failures": [] if verified else ["SYNTHETIC_DENIAL"]}
        return (adapter or self.adapter()).run_runtime(
            state, query, target, verify_integrity=verify, safety=self.t.SAFETY_BLOCK)


class AdmissionTests(Harness):
    def test_depth32_inclusive_and_depth33_rejected(self):
        value = nested(32)
        self.assertIs(self.c.admit_native(value), value)
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native, nested(33))

    def test_cycle_at_depth33_precedes_current_depth_failure(self):
        root = []
        current = root
        for _ in range(31):  # the last new list is depth32
            child = []
            current.append(child)
            current = child
        current.append(root)  # cycle occurrence would be depth33
        self.error("S1_INPUT_SHAPE_INVALID", 1, self.c.admit_native, root)

    def test_earlier_budget_failure_precedes_later_cycle(self):
        cycle = []
        cycle.append(cycle)
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native,
                   {"a": "x" * (MAX_TEXT + 1), "z": cycle})

    def test_node_preallocation_limit_precedes_bad_child(self):
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native,
                   [object()] + [None] * (MAX_VISITS - 1))

    def test_shared_acyclic_counted_on_each_occurrence(self):
        shared = [None]
        self.c.admit_native([shared, shared])
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native,
                   [shared] * ((MAX_VISITS // 2) + 1))

    def test_keys_count_as_visits_and_text_but_not_depth(self):
        value = {"k": None}
        for _ in range(30):
            value = [value]
        self.c.admit_native(value)  # dict depth31, key31, scalar32
        exact = [None] * (MAX_VISITS - 1)
        self.c.admit_native(exact)  # root plus each occurrence
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native, exact + [None])
        self.c.admit_native({"x" * MAX_TEXT: None})
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native, {"x" * MAX_TEXT: "y"})

    def test_dictionary_key_at_depth32_adds_no_depth(self):
        value = {}
        # A nonempty dict at depth32 necessarily has a value at33 and refuses;
        # empty dict at32 accepts. Separate key-only depth case is not representable.
        self.c.admit_native(nested(32, value))
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.admit_native, nested(32, {"k": None}))

    def test_exact_types_no_conversion_or_comparison_hooks(self):
        calls = []
        class Hostile(dict):
            def __iter__(self):
                calls.append("iter")
                raise AssertionError("hook invoked")
            def __len__(self):
                calls.append("len")
                raise AssertionError("hook invoked")
            def __deepcopy__(self, memo):
                calls.append("deepcopy")
                raise AssertionError("hook invoked")
            def __str__(self):
                calls.append("str")
                raise AssertionError("hook invoked")
        class HostileString(str):
            def encode(self, *args, **kwargs):
                calls.append("encode")
                raise AssertionError("hook invoked")
        for value in (Hostile(), HostileString("s"), (), type, object(), {1: None}, 2**63,
                      -(2**63)-1, float("nan"), float("inf"), "\ud800"):
            with self.subTest(type_name=type(value).__name__):
                self.error("S1_INPUT_SHAPE_INVALID", 1, self.c.admit_native, value)
        self.assertEqual(calls, [])
        self.c.admit_native([-(2**63), 2**63 - 1, False, None, 1.25])

    def test_strict_transport_duplicate_nonfinite_utf8_surrogate(self):
        for raw in (b'{"x":1,"x":2}', b'{"a":{"x":1,"x":2}}', b'NaN', b'Infinity',
                    b'-Infinity', b'"\xff"', b'{} trailing'):
            with self.subTest(raw=raw):
                self.error("S1_INVALID_TRANSPORT", 1, self.c.decode_transport, raw)
        # JSON escape parses to a lone surrogate; strict native UTF8 stage rejects.
        self.error("S1_INPUT_SHAPE_INVALID", 1, self.c.decode_transport, b'"\\ud800"')
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.decode_transport, b" " * (MAX_OUTPUT + 1))
        self.assertEqual(self.c.decode_transport(b'{"ok":[1,true,null]}'), {"ok": [1, True, None]})

    def test_transport_recursion_is_typed_refusal_never_miss(self):
        # On the pinned CPython default recursion profile this reaches parser or
        # admission refusal, both S1_LIMIT_EXCEEDED at phase1, never a domain miss.
        self.error("S1_LIMIT_EXCEEDED", 1, self.c.decode_transport,
                   b"[" * 2000 + b"0" + b"]" * 2000)


class SourceIdentityFieldTests(Harness):
    def select(self, records, query):
        projection = self.c.validate_identity(records)
        self.c.validate_arguments(query)
        self.c.validate_fields(records)
        return self.c.select_source(records, projection, query)

    def test_n1_global_tier_order_not_record_iteration(self):
        records = {"a": record("a", "other", aliases=["needle"]),
                   "z": record("z", "needle"),
                   "needle": record("needle", "different")}
        for ordered in (records, dict(reversed(list(records.items())))):
            self.assertEqual(self.select(ordered, "needle"), "needle")
        del records["needle"]
        for ordered in (records, dict(reversed(list(records.items())))):
            self.assertEqual(self.select(ordered, "needle"), "z")

    def test_n1_complete_ties_and_per_record_dedup(self):
        records = {"b": record("b", "v", aliases=["match", "MATCH", "match"]),
                   "a": record("a", "x", sound_hint="match")}
        self.assertEqual(self.select(records, "MATCH"), "b")
        records["a"]["aliases"] = ["match"]
        for ordered in (records, dict(reversed(list(records.items())))):
            self.error("S1_SOURCE_AMBIGUOUS", 6, self.select, ordered, "match")
        records["a"]["visible_symbol"] = "same"
        records["b"]["visible_symbol"] = "same"
        self.error("S1_SOURCE_AMBIGUOUS", 6, self.select, records, "same")

    def test_empty_inert_no_trim_no_casefold_no_nfkc(self):
        records = {"s": record("s", "", aliases=["", "Straße", " "], sound_hint="")}
        self.assertIsNone(self.select(records, ""))
        self.assertIsNone(self.select(records, "STRASSE"))
        self.assertIsNone(self.select(records, "Ｓ"))
        self.assertEqual(self.select(records, " "), "s")
        records[""] = record("", "")
        self.assertEqual(self.select(records, ""), "")

    def test_n5_raw_nfc_ids_and_negative_equivalence(self):
        raw = "e\u0301"
        records = {raw: record(raw), "A": record("A", "v")}
        before = copy.deepcopy(records)
        self.assertEqual(self.select(records, "é"), raw)
        self.assertIsNone(self.select(records, "a"))
        self.assertIsNone(self.select(records, "Ａ"))
        self.assertIsNone(self.select(records, "A "))
        self.assertIsNone(self.select(records, "А"))  # Cyrillic, not Latin
        self.assertEqual(records, before)

    def test_n5_collision_and_exact_identity_before_lookup(self):
        records = {"e\u0301": record("e\u0301"), "é": record("é")}
        self.error("S1_CANONICAL_ID_COLLISION", 3, self.c.validate_identity, records)
        self.error("S1_IDENTITY_INVALID", 3, self.c.validate_identity,
                   {"e\u0301": record("é")})

    def test_n6_none_and_string_alias_whole_registry_rejection(self):
        for field, value in (("visible_symbol", None), ("symbolic_role", None),
                             ("script_family", None), ("aliases", None), ("aliases", "abc"),
                             ("aliases", [None]), ("sound_hint", None), ("meaning_invariant", None),
                             ("meaning_invariant", "abc")):
            records = sample_records()
            records["dst"][field] = value
            with self.subTest(field=field, value=value):
                self.error("S1_RECORD_FIELDS_INVALID", 5, self.select, records, "src")

    def test_optional_defaults_are_views_not_storage_edits(self):
        records = {"s": record("s")}
        for name in ("aliases", "sound_hint", "meaning_invariant"):
            del records["s"][name]
        before = copy.deepcopy(records)
        self.assertEqual(self.select(records, "s"), "s")
        self.assertEqual(records, before)

    def test_n5_translation_preserves_raw_ids_and_lexical_choice(self):
        raw = "e\u0301"
        records = {raw: record(raw), "z": record("z", "é", "GREEK"),
                   "a": record("a", "e\u0301", "GREEK")}
        source = self.select(records, "é")
        self.assertEqual(source, raw)
        result = self.c.select_target(records, source, "greek")
        self.assertEqual(result["status"], "TRANSLATED")
        self.assertEqual(result["candidates"], ["a", "z"])
        self.assertEqual(result["chosen"], "a")
        records["z"]["visible_symbol"] = "divergent"
        result = self.c.select_target(records, source, "GREEK")
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertIsNone(result["chosen"])
        self.assertEqual(result["candidates"], ["a", "z"])

    def test_s1_empty_role_no_target_separate_from_legacy_prediction(self):
        records = {"s": record("s", role=""), "t": record("t", "target", "GREEK", "")}
        self.c.validate_fields(records)
        result = self.c.select_target(records, "s", "GREEK")
        self.assertEqual(result["status"], "NO_TARGET")
        self.assertEqual(result["candidates"], [])
        self.assertIsNone(result["chosen"])


class AdapterOrderingPublicationTests(Harness):
    def test_missing_callbacks_is_readiness_not_phase0(self):
        with self.assertRaises(self.c.S1ReadinessBlocked):
            CONTEXT.adapter.S1Adapter(self.c)

    def test_phase1_before_callbacks_and_layout(self):
        for runtime in (False, True):
            self.events.clear()
            state = {"bad": object()}
            call = self.runtime if runtime else self.build
            self.error("S1_INPUT_SHAPE_INVALID", 1, call, state)
            self.assertEqual(self.events, [])

    def test_layout_denial_before_controls_or_alternate_layout(self):
        for runtime in (False, True):
            self.events.clear()
            state = state_for(runtime=not runtime)
            self.error("S1_INVALID_STATE", 2, self.runtime if runtime else self.build, state)
            self.assertEqual(self.events, [])

    def test_binding_denial_does_not_invoke_integrity(self):
        self.error("S1_INTEGRITY_DENIED", 2, self.build, state_for(), adapter=self.adapter(binding=False))
        self.assertEqual(self.events, ["control", "binding"])

    def test_compromised_control_is_global_stop_not_domain_refusal(self):
        with self.assertRaises(self.c.S1ControlStop):
            self.build(state_for(), adapter=self.adapter(control=False))
        self.assertEqual(self.events, ["control"])

    def test_m6_missing_hash_denies_before_integrity_or_serve(self):
        for runtime in (False, True):
            self.events.clear()
            state = state_for(runtime=runtime)
            del state["restored_state_sha256"]
            self.error("S1_INTEGRITY_DENIED", 2, self.runtime if runtime else self.build, state)
            self.assertEqual(self.events, ["control", "binding"])

    def test_integrity_denial_before_identity_query_fields(self):
        state = state_for({"x": record("wrong", aliases=None)})
        self.error("S1_INTEGRITY_DENIED", 2, self.build, state, object(), adapter=self.adapter(integrity=False))
        self.assertNotIn("receipt", self.events)

    def test_integrity_exception_or_non_boolean_return_is_internal_error(self):
        def broken(snapshot):
            raise RuntimeError("synthetic integrity callback error")
        for callback in (broken, lambda snapshot: {"verified": 1}, lambda snapshot: None):
            adapter = CONTEXT.adapter.S1Adapter(self.c, binding_check=lambda *args: True,
                                                builder_integrity_check=callback,
                                                trusted_control_check=lambda: True)
            self.error("S1_INTERNAL_ERROR", 2, self.build, state_for(), adapter=adapter)

    def test_runtime_integrity_denial_precedes_source_resolution(self):
        state = state_for(runtime=True)
        self.error("S1_INTEGRITY_DENIED", 2, self.runtime, state, object(), verified=False)
        self.assertEqual(self.events, ["control", "binding", "runtime_integrity"])

    def test_identity_then_arguments_then_all_fields(self):
        state = state_for({"x": record("wrong", aliases=None)})
        self.error("S1_IDENTITY_INVALID", 3, self.build, state, 123)
        state["frozen_registry_snapshot"]["registry_records"]["x"]["symbol_id"] = "x"
        seal_synthetic(state)
        self.error("S1_QUERY_INVALID", 4, self.build, state, 123)
        self.error("S1_RECORD_FIELDS_INVALID", 5, self.build, state, "x")
        self.assertNotIn("receipt", self.events)

    def test_runtime_direct_none_target_is_invalid_not_query_only(self):
        self.error("S1_TARGET_ARGUMENT_INVALID", 4, self.runtime, state_for(runtime=True), target=None)

    def test_builder_translation_direct_none_target_is_invalid(self):
        self.error("S1_TARGET_ARGUMENT_INVALID", 4, self.build, state_for(), target=None, operation="translation")

    def test_b_t_native_depth32_and33_extension_paths(self):
        # Extension is not emitted; record copies would add envelope depth, tested separately.
        for runtime in (False, True):
            for depth in (32, 33):
                self.events.clear()
                state = state_for(runtime=runtime)
                state["extension"] = nested(depth - 1)  # state is root depth1
                seal_synthetic(state)
                call = self.runtime if runtime else self.build
                with self.subTest(runtime=runtime, depth=depth):
                    if depth == 32:
                        result = call(state)
                        self.assertIsInstance(result, dict)
                    else:
                        self.error("S1_LIMIT_EXCEEDED", 1, call, state)
                        self.assertEqual(self.events, [])

    def test_n7_deepcopy_joint_single_source_and_no_aliasing(self):
        state = state_for()
        original = copy.deepcopy(state)
        calls = []
        real_select = self.c.select_source
        def counted(*args, **kwargs):
            calls.append(1)
            return real_select(*args, **kwargs)
        with patch.object(self.c, "select_source", counted):
            receipt = self.build(state)
        self.assertEqual(calls, [1])
        qr, tr = receipt["query_result"], receipt["translation_result"]
        self.assertEqual(qr["symbol_ids"], ["src"])
        self.assertEqual(tr["source"]["symbol_id"], "src")
        self.assertEqual(tr["translation_packet"]["source_symbol_id"], "src")
        qr["records"][0]["meaning_invariant"].append("changed")
        self.assertEqual(tr["source"]["meaning_invariant"], ["meaning"])
        self.assertEqual(state, original)

    def test_n7_private_snapshot_ignores_later_caller_mutation(self):
        state = state_for()
        def mutate():
            state["frozen_registry_snapshot"]["registry_records"]["src"]["visible_symbol"] = "later"
        result = self.build(state, adapter=self.adapter(mutate_original=mutate))
        self.assertEqual(result["query_result"]["records"][0]["visible_symbol"], "source")
        self.assertEqual(result["translation_result"]["source"]["visible_symbol"], "source")

    def test_n7_translation_structural_failure_never_builds_receipt(self):
        state = state_for()
        self.error("S1_TARGET_ARGUMENT_INVALID", 4, self.build, state, target=object())
        self.assertNotIn("receipt", self.events)
        state["frozen_registry_snapshot"]["registry_records"]["dst"]["aliases"] = None
        seal_synthetic(state)
        self.error("S1_RECORD_FIELDS_INVALID", 5, self.build, state)
        self.assertNotIn("receipt", self.events)

    def test_final_guard_failure_returns_no_receipt_to_caller(self):
        published = []  # local return-observation only, not an external sink monitor
        def refuse(value):
            raise self.c.S1ResolutionError("S1_OUTPUT_LIMIT_EXCEEDED", 8)
        with patch.object(self.c, "guard_output", refuse):
            with self.assertRaises(self.c.S1ResolutionError) as caught:
                published.append(self.build(state_for()))
        self.assertEqual((caught.exception.reason, caught.exception.phase), ("S1_OUTPUT_LIMIT_EXCEEDED", 8))
        self.assertEqual(published, [])

    def test_m13_receipt_callback_packet_provenance_mutation_denied_before_return(self):
        # Explicit make_receipt injection is in the public adapter interface.
        # This receipt-side synthetic variant is NOT the old runtime mutant.
        def altered(*args):
            receipt = self.receipt(*args)
            packet = receipt["translation_result"]["translation_packet"]
            packet["frozen_artifact_sha256"] = "c" * 64
            packet["packet_sha256"] = hashlib.sha256(json.dumps(
                {k: v for k, v in packet.items() if k != "packet_sha256"},
                sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
            receipt["receipt_sha256"] = hashlib.sha256(json.dumps(
                {k: v for k, v in receipt.items() if k != "receipt_sha256"},
                sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
            return receipt
        published = []
        with self.assertRaises(self.c.S1ResolutionError) as caught:
            published.append(self.adapter().run_builder(state_for(), "src", "GREEK", ARTIFACT_HASH,
                              make_receipt=altered, safety=self.b.SAFETY_BLOCK, operation="joint"))
        self.assertEqual((caught.exception.reason, caught.exception.phase), ("S1_INTERNAL_BINDING_ERROR", 8))
        self.assertEqual(published, [])

    def test_m15_receipt_callback_required_field_removal_denied_before_return(self):
        def incomplete(*args):
            receipt = self.receipt(*args)
            del receipt["restored_state_id"]
            receipt["receipt_sha256"] = hashlib.sha256(json.dumps(
                {k: v for k, v in receipt.items() if k != "receipt_sha256"},
                sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
            return receipt
        self.error("S1_INTERNAL_BINDING_ERROR", 8, self.adapter().run_builder,
                   state_for(), "src", "GREEK", ARTIFACT_HASH, make_receipt=incomplete,
                   safety=self.b.SAFETY_BLOCK, operation="joint")

    def test_m13_original_runtime_mutant_proposal_not_implemented(self):
        self.skipTest("NOT_IMPLEMENTED: no owner-approved prepublication mutation/sink injection contract; positive coherence is not M13 battery closure")

    def test_m13_synthetic_runtime_provenance_guard_kills_throwaway_mutant(self):
        # New candidate mechanism test, not recovered original M13 mutant bytes.
        adapter = self.adapter()
        original = adapter._translation
        def forged(*args, **kwargs):
            result = original(*args, **kwargs)
            packet = result["translation_packet"]
            packet["frozen_artifact_sha256"] = "b" * 64
            body = {k: v for k, v in packet.items() if k != "packet_sha256"}
            packet["packet_sha256"] = hashlib.sha256(json.dumps(
                body, sort_keys=True, ensure_ascii=False,
                separators=(",", ":"), default=str).encode("utf-8")).hexdigest()
            return result
        with patch.object(adapter, "_translation", forged):
            self.error("S1_INTERNAL_BINDING_ERROR", 8, self.runtime,
                       state_for(runtime=True), adapter=adapter)
            # Throwaway in-memory guard-removal mutant; no file is changed.
            with patch.object(adapter, "_coherent", lambda *a, **k: None):
                accepted = self.runtime(state_for(runtime=True), adapter=adapter)
                self.assertEqual(accepted["translation_packet"]["frozen_artifact_sha256"], "b" * 64)
        # Expected acceptance under a deliberately removed guard is a mutation
        # control observation, never a safety PASS or real forged receipt proof.

    def test_m15_synthetic_required_field_guard_kills_throwaway_mutant(self):
        state = state_for()
        del state["frozen_registry_snapshot"]["registry_records"]["dst"]["visible_symbol"]
        seal_synthetic(state)
        self.error("S1_RECORD_FIELDS_INVALID", 5, self.build, state, target=None)
        # ID hit, query-only: unrelated missing field would be unseen without
        # whole-registry validation. Explicit new-core mutant, not historical M15.
        with patch.object(self.c, "validate_fields", lambda records: None):
            accepted = self.build(state, target=None)
            self.assertTrue(accepted["query_result"]["found"])

    def test_m15_original_required_record_check_mutant_proposal_not_implemented(self):
        self.skipTest("NOT_IMPLEMENTED: original required-record-check mutant and exact independent kill test unavailable; receipt callback variant is not M15 battery closure")

    def test_legacy_runtime_fake_integrity_preserves_denial_status(self):
        calls = []
        def fake(state):
            calls.append(state)
            return {"verified": False, "failures": ["SYNTHETIC_DENIAL"]}
        # Test-only module attribute patch. Production source is never modified.
        state = state_for(runtime=True)
        with patch.object(self.t, "verify_restored_state", fake):
            result = self.t.lookup_translation_from_frozen_registry(state, "src", "GREEK")
        self.assertEqual(calls, [state])
        self.assertEqual(result["status"], "INTEGRITY_CHECK_FAILED")
        self.assertEqual(result["integrity_failures"], ["SYNTHETIC_DENIAL"])
        self.assertIsNone(result["translation_packet"])

    def test_opt_in_public_builder_and_runtime_routes(self):
        result = self.b.run_query_with_receipt(state_for(), "src", "GREEK", ARTIFACT_HASH,
                                               s1_context=self.adapter())
        self.assertEqual(result["receipt_version"], "2.7.7")
        self.assertEqual(result["translation_result"]["translation_packet"]["packet_version"], "2.7.7")
        def fake(snapshot):
            return {"verified": True, "failures": []}
        with patch.object(self.t, "verify_restored_state", fake):
            result = self.t.lookup_translation_from_frozen_registry(state_for(runtime=True), "src", "GREEK",
                                                                    s1_context=self.adapter())
        self.assertEqual(result["translation_packet"]["packet_version"], "2.7.6")


class OutputEnvelopeTests(Harness):
    def test_output_depth32_and33(self):
        value = nested(32)
        self.assertIs(self.c.guard_output(value), value)
        self.error("S1_OUTPUT_BUILD_ERROR", 8, self.c.guard_output, nested(33))

    def test_output_exact_serialized_bytes_not_just_text(self):
        value = "x" * (MAX_OUTPUT - 2)  # JSON quotation bytes included
        self.assertIs(self.c.guard_output(value), value)
        self.error("S1_OUTPUT_LIMIT_EXCEEDED", 8, self.c.guard_output, value + "x")
        self.error("S1_OUTPUT_BUILD_ERROR", 8, self.c.guard_output, "\ud800")

    def test_builder_envelope_overrun_and_runtime_smaller_envelope(self):
        for runtime in (False, True):
            state = state_for(runtime=runtime)
            snapshot = (state["frozen_artifact"] if runtime else state)["frozen_registry_snapshot"]
            # Source record is depth4(B)/5(T). The final scalar is depth32 input;
            # emitted query/translation/receipt nesting introduces extra levels.
            record_depth = 5 if runtime else 4
            snapshot["registry_records"]["src"]["extension"] = nested(32 - record_depth)
            seal_synthetic(state)
            self.c.admit_native(state)
            if runtime:
                # T source copy has LESS nesting than nested input layout. Do not
                # invent a T overrun merely to mirror the builder receipt case.
                self.assertEqual(self.runtime(state)["status"], "TRANSLATED_FROM_FROZEN_REGISTRY")
            else:
                self.error("S1_OUTPUT_BUILD_ERROR", 8, self.build, state)


class EnvelopeDiagnosticV03Tests(Harness):
    """Additional proposed oracles; original V0.2 failure remains unchanged."""

    @staticmethod
    def value_depth(node):
        if type(node) is dict:
            return 1 + max((EnvelopeDiagnosticV03Tests.value_depth(v) for v in node.values()), default=0)
        if type(node) is list:
            return 1 + max((EnvelopeDiagnosticV03Tests.value_depth(v) for v in node), default=0)
        return 1

    def test_v03_builder_depth31_and32_fit_unchanged_receipt_envelope(self):
        for maximum in (31, 32):
            with self.subTest(input_and_receipt_depth=maximum):
                state = state_for()
                state["frozen_registry_snapshot"]["registry_records"]["src"]["extension"] = nested(maximum - 4)
                seal_synthetic(state)
                self.assertEqual(self.value_depth(state), maximum)
                result = self.build(state)
                self.assertEqual(self.value_depth(result), maximum)

    def test_v03_runtime_depth32_input_has_depth29_output(self):
        state = state_for(runtime=True)
        state["frozen_artifact"]["frozen_registry_snapshot"]["registry_records"]["src"]["extension"] = nested(32 - 5)
        seal_synthetic(state)
        self.assertEqual(self.value_depth(state), 32)
        result = self.runtime(state)
        self.assertEqual(self.value_depth(result), 29)

    def test_v03_native_depth33_is_phase1_not_output_phase8(self):
        state = state_for()
        state["frozen_registry_snapshot"]["registry_records"]["src"]["extension"] = nested(33 - 4)
        seal_synthetic(state)
        self.assertEqual(self.value_depth(state), 33)
        self.error("S1_LIMIT_EXCEEDED", 1, self.build, state)

    def test_v03_final_guard_rejects_poststaging_depth33_before_builder_return(self):
        adapter = self.adapter()
        original = adapter._receipt
        def perturb(*args, **kwargs):
            result = original(*args, **kwargs)
            result["synthetic_poststaging_probe"] = nested(32)
            return result
        with patch.object(adapter, "_receipt", perturb):
            self.error("S1_OUTPUT_BUILD_ERROR", 8, self.build, state_for(), adapter=adapter)

    def test_v03_shared_publication_guard_boundary_and_removal_control(self):
        adapter = self.adapter()
        accepted = nested(32)
        refused = nested(33)
        self.assertIs(adapter._publish(lambda: accepted), accepted)
        self.error("S1_OUTPUT_BUILD_ERROR", 8, adapter._publish, lambda: refused)
        # Deliberate throwaway in-memory control only. No source file edit.
        with patch.object(self.c, "guard_output", lambda value: value):
            self.assertIs(adapter._publish(lambda: refused), refused)


class PinnedLegacyBaselineTests(Harness):
    def test_baseline_empty_role_prediction_not_corrected_oracle(self):
        if CONTEXT.baseline is None:
            self.skipTest("UNAPPROVED/NOT_RUN baseline prediction requires explicit immutable --baseline successor_tree")
        source = CONTEXT.baseline / "eit_program_lang" / "eit_v277_builder_candidate.py"
        # Exact member pin derived from BASELINE_INVENTORY.json, never candidate bytes.
        expected = "3c1f3ac799211c298d378ad87556975c38447023f92cc3d18d4bda7dd48ab331"
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected,
                         "baseline pin must match original successor inventory")
        spec = importlib.util.spec_from_file_location("_v277_pinned_legacy_b", str(source))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = {"s": record("s", role=""), "t": record("t", "target", "GREEK", "")}
        result = module.lookup_translation_from_frozen_registry(state_for(records), "s", "GREEK", ARTIFACT_HASH)
        # Static predicted historical B behavior, NOT an approved historical oracle.
        self.assertEqual(result["status"], "TRANSLATED_FROM_FROZEN_REGISTRY")
        self.assertEqual(result["translation_packet"]["target_symbol_id"], "t")
