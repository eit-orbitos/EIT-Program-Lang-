"""S1/SP1 candidate pure producer semantics. NOT executed or released.

No owner root, configuration, installed caller or scientific claim is supplied.
The unchanged verifier remains the receipt authority in its exact scope.
"""
from __future__ import annotations

import json
import math
import unicodedata

MAX_TRANSPORT = 33_554_432
MAX_DEPTH = 32
MAX_VISITS = 262_144
MAX_TEXT = 16_777_216
MAX_RECORDS = 10_000
MAX_ID = 1_024
MAX_QUERY = 4_096
MAX_TOKEN = 4_096
MAX_ROLE = 256
MAX_ALIASES = 128
MAX_ALL_ALIASES = 65_536
MAX_MEANING = 64
MAX_DERIVED = 16_384
MAX_OUTPUT = 33_554_432
INT_MIN = -(2**63)
INT_MAX = 2**63 - 1

_REASONS = {
    1: frozenset(('S1_INVALID_TRANSPORT', 'S1_INPUT_SHAPE_INVALID', 'S1_LIMIT_EXCEEDED')),
    2: frozenset(('S1_INVALID_STATE', 'S1_INTEGRITY_DENIED')),
    3: frozenset(('S1_IDENTITY_INVALID', 'S1_LIMIT_EXCEEDED',
                  'S1_DERIVED_LIMIT_EXCEEDED', 'S1_CANONICAL_ID_COLLISION')),
    4: frozenset(('S1_QUERY_INVALID', 'S1_ARGUMENT_LIMIT_EXCEEDED', 'S1_TARGET_ARGUMENT_INVALID')),
    5: frozenset(('S1_RECORD_FIELDS_INVALID', 'S1_LIMIT_EXCEEDED', 'S1_DERIVED_LIMIT_EXCEEDED')),
    6: frozenset(('S1_SOURCE_AMBIGUOUS',)),
    7: frozenset(),
    8: frozenset(('S1_INTERNAL_BINDING_ERROR', 'S1_OUTPUT_BUILD_ERROR', 'S1_OUTPUT_LIMIT_EXCEEDED')),
}


class S1ResolutionError(Exception):
    """Exact reason+phase channel, never a receipt status or a genuine miss."""
    def __init__(self, reason, phase):
        if type(reason) is not str or type(phase) is not int or phase not in _REASONS:
            raise ValueError('invalid S1 reason/phase contract')
        if reason not in _REASONS[phase] and reason not in ('S1_INTERNAL_ERROR', 'S1_OPERATION_ABORTED'):
            raise ValueError('reason not allowed at this phase')
        self.reason = reason
        self.phase = phase
        super().__init__(reason, phase)


class S1ControlStop(Exception):
    """Trusted control compromise: GLOBAL_STOP, not an ordinary S1 response."""


class S1ReadinessBlocked(Exception):
    """Missing trusted bootstrap/control: no response and no invented Phase 0."""


def _fail(reason, phase):
    raise S1ResolutionError(reason, phase)


def _utf8(text, phase, invalid):
    if type(text) is not str:
        _fail(invalid, phase)
    try:
        return text.encode('utf-8', errors='strict')
    except UnicodeError:
        _fail(invalid, phase)


def admit_native(value):
    """Inclusive per-root budgets; exact types, root1, value-only depth.

    Active-path membership uses id(), not equality/hash of supplied objects.
    Shared acyclic objects are visited again, never mistaken for cycles.
    """
    visits = 0
    text_bytes = 0
    active = set()

    def visit(node, depth, key=False):
        nonlocal visits, text_bytes
        t = type(node)
        # Recognize exact containers without invoking user hooks. Cycle wins
        # over this occurrence's budget test, not over an earlier failure.
        container = t is dict or t is list
        if container and id(node) in active:
            _fail('S1_INPUT_SHAPE_INVALID', 1)
        if depth > MAX_DEPTH or visits >= MAX_VISITS:
            _fail('S1_LIMIT_EXCEEDED', 1)
        visits += 1
        if t not in (dict, list, str, int, float, bool, type(None)):
            _fail('S1_INPUT_SHAPE_INVALID', 1)
        if key and t is not str:
            _fail('S1_INPUT_SHAPE_INVALID', 1)
        if t is str:
            text_bytes += len(_utf8(node, 1, 'S1_INPUT_SHAPE_INVALID'))
            if text_bytes > MAX_TEXT:
                _fail('S1_LIMIT_EXCEEDED', 1)
        elif t is int:
            if node < INT_MIN or node > INT_MAX:
                _fail('S1_INPUT_SHAPE_INVALID', 1)
        elif t is float:
            if not math.isfinite(node):
                _fail('S1_INPUT_SHAPE_INVALID', 1)
        elif container:
            # Bound sorting/key-list allocation before building the key list.
            minimum = len(node) * (2 if t is dict else 1)
            if minimum > MAX_VISITS - visits:
                _fail('S1_LIMIT_EXCEEDED', 1)
            if t is dict:
                for k in node:
                    if type(k) is not str:
                        _fail('S1_INPUT_SHAPE_INVALID', 1)
            active.add(id(node))
            try:
                if t is dict:
                    for k in sorted(node):
                        visit(k, depth, key=True)  # keys add visits, not a value edge
                        visit(node[k], depth + 1)
                else:
                    for child in node:
                        visit(child, depth + 1)
            finally:
                active.remove(id(node))

    visit(value, 1)
    return value


def decode_transport(raw):
    """Strict bounded JSON transport. No file reads or native object hooks."""
    if type(raw) is not bytes:
        _fail('S1_INVALID_TRANSPORT', 1)
    if len(raw) > MAX_TRANSPORT:
        _fail('S1_LIMIT_EXCEEDED', 1)
    try:
        text = raw.decode('utf-8', errors='strict')
    except UnicodeError:
        _fail('S1_INVALID_TRANSPORT', 1)

    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                _fail('S1_INVALID_TRANSPORT', 1)
            result[k] = v
        return result

    def constant(_):
        _fail('S1_INVALID_TRANSPORT', 1)

    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except S1ResolutionError:
        raise
    except RecursionError:
        _fail('S1_LIMIT_EXCEEDED', 1)
    except (ValueError, UnicodeError):
        _fail('S1_INVALID_TRANSPORT', 1)
    return admit_native(value)


def _bounded(text, maximum, phase, invalid, limit):
    encoded = _utf8(text, phase, invalid)
    if len(encoded) > maximum:
        _fail(limit, phase)
    return text


def _derived(text, phase, method='nfc'):
    result = unicodedata.normalize('NFC', text)
    if len(result.encode('utf-8')) > MAX_DERIVED:
        _fail('S1_DERIVED_LIMIT_EXCEEDED', phase)
    if method == 'lower':
        result = result.lower()
    elif method == 'upper':
        result = result.upper()
    if len(result.encode('utf-8')) > MAX_DERIVED:
        _fail('S1_DERIVED_LIMIT_EXCEEDED', phase)
    return result


def validate_identity(records):
    if type(records) is not dict:
        _fail('S1_IDENTITY_INVALID', 3)
    # Full structural pass before any NFC projection or query serving.
    for raw, rec in records.items():
        if type(raw) is not str or type(rec) is not dict:
            _fail('S1_IDENTITY_INVALID', 3)
        for k in rec:
            if type(k) is not str:
                _fail('S1_IDENTITY_INVALID', 3)
        if 'symbol_id' not in rec or type(rec['symbol_id']) is not str or rec['symbol_id'] != raw:
            _fail('S1_IDENTITY_INVALID', 3)
    if len(records) > MAX_RECORDS:
        _fail('S1_LIMIT_EXCEEDED', 3)
    for raw in sorted(records):
        _bounded(raw, MAX_ID, 3, 'S1_IDENTITY_INVALID', 'S1_LIMIT_EXCEEDED')
    projection = {}
    for raw in sorted(records):
        key = _derived(raw, 3)
        if key in projection:
            _fail('S1_CANONICAL_ID_COLLISION', 3)
        projection[key] = raw
    return projection


def validate_arguments(query, target=None):
    _bounded(query, MAX_QUERY, 4, 'S1_QUERY_INVALID', 'S1_ARGUMENT_LIMIT_EXCEEDED')
    if target is not None:
        _bounded(target, MAX_ROLE, 4, 'S1_TARGET_ARGUMENT_INVALID', 'S1_ARGUMENT_LIMIT_EXCEEDED')


def validate_fields(records):
    alias_total = 0
    required = (('visible_symbol', MAX_TOKEN), ('symbolic_role', MAX_ROLE), ('script_family', MAX_ROLE))
    optional = ('aliases', 'sound_hint', 'meaning_invariant')
    for raw in sorted(records):
        rec = records[raw]
        for name, maximum in required:
            if name not in rec:
                _fail('S1_RECORD_FIELDS_INVALID', 5)
            _bounded(rec[name], maximum, 5, 'S1_RECORD_FIELDS_INVALID', 'S1_LIMIT_EXCEEDED')
        for name in optional:
            if name not in rec:
                continue
            field = rec[name]
            if name == 'sound_hint':
                _bounded(field, MAX_TOKEN, 5, 'S1_RECORD_FIELDS_INVALID', 'S1_LIMIT_EXCEEDED')
                continue
            if type(field) is not list:
                _fail('S1_RECORD_FIELDS_INVALID', 5)
            maximum = MAX_ALIASES if name == 'aliases' else MAX_MEANING
            if len(field) > maximum:
                _fail('S1_LIMIT_EXCEEDED', 5)
            if name == 'aliases':
                alias_total += len(field)
                if alias_total > MAX_ALL_ALIASES:
                    _fail('S1_LIMIT_EXCEEDED', 5)
            for token in field:
                _bounded(token, MAX_TOKEN, 5, 'S1_RECORD_FIELDS_INVALID', 'S1_LIMIT_EXCEEDED')
    # Transform only after every raw selected field has passed.
    for raw in sorted(records):
        rec = records[raw]
        _derived(rec['visible_symbol'], 5)
        _derived(rec['symbolic_role'], 5, 'upper')
        _derived(rec['script_family'], 5, 'upper')
        for token in rec.get('aliases', []):
            _derived(token, 5, 'lower')
        if 'sound_hint' in rec:
            _derived(rec['sound_hint'], 5, 'lower')


def select_source(records, projection, query):
    # Query normalization is a Phase-5 derivation, after raw fields passed.
    nq = _derived(query, 5)
    lq = _derived(query, 5, 'lower')
    if nq in projection:
        return projection[nq]
    if query == '':
        return None
    tiers = ([], [], [])
    for raw in sorted(records):
        rec = records[raw]
        visible = _derived(rec['visible_symbol'], 5)
        if visible != '' and visible == nq:
            tiers[0].append(raw)
        if any(token != '' and token == lq for token in
               (_derived(a, 5, 'lower') for a in rec.get('aliases', []))):
            tiers[1].append(raw)
        sound = _derived(rec.get('sound_hint', ''), 5, 'lower')
        if sound != '' and sound == lq:
            tiers[2].append(raw)
    for ids in tiers:
        if len(ids) > 1:
            _fail('S1_SOURCE_AMBIGUOUS', 6)
        if ids:
            return ids[0]
    return None


def select_target(records, raw_source_id, target):
    role = _derived(records[raw_source_id]['symbolic_role'], 5, 'upper')
    family = _derived(target, 5, 'upper')
    candidates = []
    if role != '':
        for raw in sorted(records):
            rec = records[raw]
            if (_derived(rec['symbolic_role'], 5, 'upper') == role and
                    _derived(rec['script_family'], 5, 'upper') == family):
                candidates.append(raw)
    if not candidates:
        return {'status': 'NO_TARGET', 'candidates': [], 'chosen': None, 'role': role}
    surfaces = {_derived(records[raw]['visible_symbol'], 5) for raw in candidates}
    if len(surfaces) > 1:
        return {'status': 'AMBIGUOUS', 'candidates': candidates, 'chosen': None, 'role': role}
    return {'status': 'TRANSLATED', 'candidates': candidates, 'chosen': candidates[0], 'role': role}


def guard_output(value):
    """Fail before return; output shape/depth uses unchanged §6.3 edge count.

    D01 input budgets are not reapplied to duplicated receipt outputs. Output
    total has its own 32MiB ceiling. Candidate output-depth mapping is Phase8
    S1_OUTPUT_BUILD_ERROR, explicitly subject to IR04-P/O approval.
    """
    active = set()

    def shape(node, depth):
        t = type(node)
        if depth > MAX_DEPTH or t not in (dict, list, str, int, float, bool, type(None)):
            _fail('S1_OUTPUT_BUILD_ERROR', 8)
        if t is int and not INT_MIN <= node <= INT_MAX:
            _fail('S1_OUTPUT_BUILD_ERROR', 8)
        if t is float and not math.isfinite(node):
            _fail('S1_OUTPUT_BUILD_ERROR', 8)
        if t is str:
            _utf8(node, 8, 'S1_OUTPUT_BUILD_ERROR')
        elif t in (dict, list):
            if id(node) in active:
                _fail('S1_OUTPUT_BUILD_ERROR', 8)
            active.add(id(node))
            try:
                if t is dict:
                    for k in node:
                        if type(k) is not str:
                            _fail('S1_OUTPUT_BUILD_ERROR', 8)
                        _utf8(k, 8, 'S1_OUTPUT_BUILD_ERROR')
                    for k in sorted(node):
                        shape(node[k], depth + 1)
                else:
                    for item in node:
                        shape(item, depth + 1)
            finally:
                active.remove(id(node))

    shape(value, 1)
    try:
        encoder = json.JSONEncoder(sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
        count = 0
        for chunk in encoder.iterencode(value):
            count += len(chunk.encode('utf-8', errors='strict'))
            if count > MAX_OUTPUT:
                _fail('S1_OUTPUT_LIMIT_EXCEEDED', 8)
    except S1ResolutionError:
        raise
    except (ValueError, TypeError, UnicodeError, RecursionError):
        _fail('S1_OUTPUT_BUILD_ERROR', 8)
    return value
