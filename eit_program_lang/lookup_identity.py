"""Successor Option A: NFC search projection over unchanged exact identities.

Producer errors only; these are not receipt statuses. No artifact mutation,
coercion, case folding, compatibility normalization or cross-artifact cache.
"""


class LookupIdentityError(ValueError):
    """Serving must abort; callers must not substitute an absence receipt."""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


def get_lookup_records(state, artifact_nested=False):
    """Read only the declared frozen snapshot; never fall back or coerce."""
    container = state
    path = (("frozen_artifact",) if artifact_nested else ()) + (
        "frozen_registry_snapshot", "registry_records")
    for field in path:
        if type(container) is not dict or field not in container:
            raise LookupIdentityError("INVALID_LOOKUP_INPUT")
        container = container[field]
    if type(container) is not dict:
        raise LookupIdentityError("INVALID_LOOKUP_INPUT")
    return container


def build_id_projection(records, normalizer):
    """Validate the entire exact-dict registry, then derive unique NFC keys.

    Call sites supply their pinned NFC normalizer. This helper is not a
    cryptographic integrity check and does not validate every record field.
    """
    if type(records) is not dict:
        raise LookupIdentityError("INVALID_LOOKUP_INPUT")
    # Complete structural validation before any normalization or lookup.
    for raw_id, record in records.items():
        if (type(raw_id) is not str or type(record) is not dict
                or type(record.get("symbol_id")) is not str
                or record["symbol_id"] != raw_id):
            raise LookupIdentityError("INVALID_LOOKUP_INPUT")
    projection = {}
    for raw_id in records:
        key = normalizer(raw_id)
        if type(key) is not str:
            raise LookupIdentityError("INVALID_LOOKUP_INPUT")
        if key in projection:
            raise LookupIdentityError("CANONICAL_ID_COLLISION")
        projection[key] = raw_id
    return projection


def resolve_id(projection, query, normalizer):
    """Return the original ID or None; the empty string is a valid ID."""
    if type(query) is not str:
        raise LookupIdentityError("INVALID_LOOKUP_INPUT")
    return projection.get(normalizer(query))
