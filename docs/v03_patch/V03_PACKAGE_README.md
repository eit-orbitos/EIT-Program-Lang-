# V0.3 — targeted envelope diagnosis and regression candidate

TARGETED_FIX_CANDIDATE · EXECUTION_PENDING_KIMI · GOVERNANCE_FREEZE_NOT_AUTHORIZED

**The observed synthetic failure is preserved. No source fix is claimed.**

Tasklet authored the original erroneous test. Static path accounting identifies an oracle conflict, not a missing output guard. The original test and source bytes are preserved; five supplementary, unexecuted diagnostic tests now distinguish admitted depth32, native depth33 rejection and poststaging output depth33 rejection. They include a throwaway in-memory guard-removal control.

## Root cause

`nested(d)` has value-depth d with root1. Builder state record path is root → frozen_registry_snapshot → registry_records → src, so record depth4. Its extension is depth5. The failing fixture sets extension to nested(32−4)=nested28: deepest value is 5+28−1=32.

Builder joint receipt record path is root → query_result → records → list item, also record depth4. Thus the same extension remains exactly depth32. Both `guard_output(receipt)` inside `_receipt` and the final `_publish` guard exist. Their inclusive depth32 limit correctly does not raise. Making this fixture raise would tighten the declared domain without a legitimate source defect.

Runtime state record is depth5; extension nested27 produces input depth32. Runtime output source record is depth2; extension is depth3, producing output depth29. Runtime acceptance is consistent with the smaller envelope. The attributed report's “input depth39” is unsupported by the pinned fixture.

## Preserved and pending

The complete original V0.2 test function is unchanged, including its expectation of P8 S1_OUTPUT_BUILD_ERROR. Therefore the full suite remains expected to fail that assertion unless the oracle receives a separate correction. It is neither skipped nor relabelled PASS. New diagnostic expectations are proposals, not substituted approved oracles. No source guard, verifier, stamp, baseline or release rule is changed.

The requested source correction cannot honestly be implemented while simultaneously preserving the inclusive depth32 contract and this contradictory rejection expectation. Exact expected-result correction needs scoped author disposition. No further general audit is requested. This candidate provides the bytes needed for Kimi to verify the narrower diagnosis independently.

Both uploaded evidence archives are preserved. Their checksums match 5/5 each and both transcripts report 46 tests with one failure, exit1. They are separate supplied records; no new run or authenticated reviewer identity is inferred. Tasklet performed static byte/path analysis only, no project import, compilation, collection or execution.

F01 0/19 VERIFIED · IR04-P/IR04-O distinct pending production/closure obligations · N-1 OPEN_BLOCKING · N-5 FINAL_CLOSURE_PENDING · B4 NOT_CLOSED · RG6 OPEN · Gate-4 NOT_SATISFIED · Formal Freeze NO · GitHub HOLD · Zenodo BLOCKED.
