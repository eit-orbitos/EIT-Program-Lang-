# S1 adapter candidate authoring notes

Status: AUTHORED / UNTESTED / NOT_RELEASED. No project import, execution,
compilation, collection, test, package installation or launch was performed.
No PASS, root-verification, gate-closure or freeze claim is made.

## Exact scope

- Added `eit_program_lang/s1_sp1_adapter.py`. It imports standard-library
  utilities only and receives the same explicit core module/error classes.
  It has no project auto-import, loader, sys.path/sys.modules mutation,
  production callback defaults, invented owner root or hard-coded trusted hash.
- B query, direct translation and joint-receipt entry points gain keyword-only
  `s1_context=None` and a leading opt-in delegation branch. The original
  low-level supplied-result receipt builder and all original legacy bodies,
  stamp constants, hash helpers and dynamic sibling-loader code are unchanged.
- T direct translation gains the same keyword-only opt-in branch, passing its
  unchanged original `verify_restored_state` function and safety constant.
  T packet stamp remains 2.7.6; B remains 2.7.7. Legacy calls remain unprotected.
- No core, tests, Q/L/U/V/IV/I, config, license or original archive was changed.

## Owner callback boundary (unbound)

Construction requires `S1Adapter(core, *, binding_check,
builder_integrity_check, trusted_control_check)`. Missing callbacks block with
the injected core's `S1ReadinessBlocked`; an invalid core unable to provide
that error class gives a configuration `TypeError`, not invented Phase 0.

Callbacks are:

1. `trusted_control_check() -> exact bool`. False, invalid result or exception
   raises the core's `S1ControlStop` (GLOBAL_STOP). Checked after Phase-2 layout
   validation and again before/after Phase-8 staging.
2. `binding_check(snapshot_copy, layout, artifact_sha256) -> exact bool`.
   Layout labels are `builder_direct` and `runtime_nested`. False denies P2
   without invoking integrity. Invalid return/unexpected exception is P2
   INTERNAL_ERROR; timeout/cancellation is P2 OPERATION_ABORTED.
3. `builder_integrity_check(snapshot_copy) -> dict` containing exact-bool
   `verified`. False denies P2; invalid return/unexpected exception is P2
   INTERNAL_ERROR. Runtime instead receives unchanged T IV in that slot.

Callbacks receive independent deep copies, never the pinned lookup snapshot.
This prevents ordinary callback mutation from changing the served snapshot;
it is not process isolation, closure/root immutability or loader authentication.
The owner must establish callback provenance, trusted root/custody, core
identity, exact routing, hash domain and publication boundary before real use.

## Candidate operation contract

P1 admission then private deepcopy; P2 declared layout, trusted control,
owner binding, mandatory matching artifact/state identity and state-body hash,
then B owner integrity or original T IV; P3 identity; P4 arguments; P5 fields;
P6 one source decision; P7 target; P8 private copied result/packet/receipt,
coherence, hashes, final output guard, one return. Direct translation with
None target rejects P4; wrapper None remains query-only. No records are pruned
or normalized in storage. Empty raw ID is distinguished from no source.

P2 requires lowercase 64-hex hashes, `state.frozen_artifact_sha256` equal to
the supplied B artifact parameter (or runtime state declaration), and compact
original-domain state-body hash excluding `restored_state_sha256`. Runtime
also recomputes the original spaced-JSON artifact hash. Direct B has no
declared artifact mapping to recompute; its owner binding must establish that
external artifact connection. This is a disclosed tightening, not proof of
producer authenticity or M6 mutation-battery closure.

M13/M15 candidate checks bind complete original result/packet schemas to the
same selected exact records, raw IDs, requested family, normalized role,
artifact/state hashes, packet-required presence/null rules, safety and packet
digest. Joint receipt must have the original exact schema, stamps/metadata,
same copied query/translation results, boundary and receipt digest. The
unchanged low-level builder is used only after private results are staged.
Candidate checks do not close the original mutation-battery obligations.

## Open limitations and review duties

- No runtime validity, fixture result, oracle approval or compatibility proof
  follows from authoring or static reading. IR04-P/O and independent execution
  authorization remain separate. No original archive was changed.
- `guard_output` comes from the exact injected core. It checks complete final
  logical output with root1/value-depth<=32 and compact strict-UTF8 JSON total
  <=32MiB. Shape/depth maps to P8 OUTPUT_BUILD_ERROR and excess bytes to P8
  OUTPUT_LIMIT_EXCEEDED. This mapping/serialization domain remains a candidate
  for IR04-P/O; it is not silently treated as an accepted executable oracle.
- Construction checks API presence, not code hashes/Unicode runtime profile
  or module custody. The owner must pin one core instance and the intended
  CPython/Unicode profile. Standard-library NFC used for packet coherence is
  the running interpreter's Unicode implementation, not profile attestation.
- Native admission does not prove upstream duplicate-key parser provenance.
  Raw transport callers must explicitly use/bind core `decode_transport`.
- Snapshot publication is logical API staging only, not OS atomicity or
  protection against hostile process-level mutation/concurrent caller writes.
  Root, caller, routing, C3-E, F01 and original test closure remain open.

## AIAssessmentReceipt

```json
{
  "receipt_type": "AIAssessmentReceipt",
  "agent": "v277_adapter",
  "scope": "adapter plus opt-in B/T delegation authoring only",
  "evidence": ["accepted D01-D07 proposal read as text", "corrective overlay V0.2 read as text", "original B/T/IV/hash helpers read as text", "injected core interface read as text"],
  "execution": "NOT_RUN; no project import/compile/test",
  "claims": ["candidate source authored", "owner controls remain unbound"],
  "limitations": ["no independent review", "no fixture/oracle approval", "no root/loader/routing proof", "no original mutation-battery closure"],
  "recommendation": "YELLOW candidate authoring only; not a final ClaimState assignment",
  "meta_audit_status": "NOT_PERFORMED",
  "receipt_hash": null,
  "hash_note": "No cryptographic receipt-hash claim; exact candidate pins are for parent manifest."
}
```
