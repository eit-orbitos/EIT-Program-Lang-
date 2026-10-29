# RC11 release-layer static control review — ADD_ONLY

## Scope and conclusion

Reviewed only the four files in `../rc11_templates/`: `ci_inventory_check.py`, `ci_inventory_negative_controls.py`, `ci_release.sh`, and `verify.yml`. No project code, tests, CI, or dependency commands executed; originals and prior evidence were not modified. This is a separate same-model static review, not independent runtime reproduction. No final claim states assigned.

The shared entrypoint provides substantial release-integrity checks, but contains **one concrete fail-open traversal bug**. This blocks an unqualified claim that inventory always covers every nonexcluded file; it is **not evidence that the already-tested candidate exploited the bug or failed CI**. Other findings below are bounded coverage limitations, not demonstrated candidate failures.

## Concrete defect requiring correction for fail-closed inventory assurance

**C1 — directory scan failures are silently omitted.** `ci_inventory_check.py:50` uses `os.walk(root, followlinks=False)` without an `onerror` handler. Python's default suppresses `scandir` errors. A nonexcluded directory that the running user cannot enumerate can therefore contain unlisted files without adding them to `actual`. If its contents are also absent from the manifest and all REQUIRED paths remain readable elsewhere, both set equality (`:74`) and the subsequent manifest-only `sha256sum` can succeed. The outer `except OSError` (`:82`) does not repair errors already swallowed by `os.walk`.

This is a specific static counterexample, not an executed reproduction. It depends on a directory scan error under the invoking identity; ordinary readable GitHub checkouts need not encounter it. Fix by propagating every traversal error (e.g. an `onerror` callback that raises), and add a targeted negative control. Permission-based controls must account for privileged users, for whom mode-bit denial may not deny access.

## Adequate controls and bounded blind spots

### Paths and exclusions

- Manifest checks reject absolute paths, backslashes, empty/dot/dot-dot components, ASCII control characters, duplicate paths, and non-UTF-8 input; require lowercase digests, two-space records, LF termination, and UTF-8-byte ordering (`inventory:29–48`). No Unicode normalization or case folding is performed: this is an exact Linux path contract, not a cross-platform normalization claim.
- Symlink directories and nonregular files, including symlink files, are rejected (`:54–65`). Only root `SHA256SUMS.txt` and real root `.git` are excluded. Nested `SHA256SUMS.txt`, `.gitkeep`, and nested `.git` files must be inventoried. Empty ordinary directories are not inventoried; the contract is a file inventory.
- `str.splitlines()` also recognizes certain Unicode line separators beyond LF (`:35`), so some otherwise valid UTF-8 filenames are rejected. This is conservative rejection, not an acceptance bypass; avoid claiming support for every possible UTF-8 POSIX filename.
- Negative-control copying ignores a name `.git` **at every depth** (`negative_controls:15`), whereas the checker excludes only root `.git`. A legitimate manifest-listed nested `.git` subtree will disappear from control copies and can make controls fail. This is a fail-closed control-harness mismatch, not a demonstrated false acceptance. Use a root-only copy exclusion if supporting such trees.

### Mandatory inventory

- The REQUIRED set is actually enforced independently of manifest equality (`inventory:12–24,72–75`): removing both a REQUIRED file and its manifest line still fails. Both initial and final inventory/hash checks are mandatory in the shell, under `set -euo pipefail` (`release:3,13–16,52–54`).
- The `missing required README` negative control removes only the file (`negative_controls:27`). Ordinary manifest equality would reject this even if REQUIRED enforcement were removed. Add a control removing both README and its manifest record to test the distinctive mandatory-membership property.
- The three selfchecks and reference archive are not in REQUIRED, but the entrypoint directly invokes/checks them (`release:42,46–48`), so their absence still fails the complete CI. Conversely, **no `zenodo/` metadata path is REQUIRED or semantically checked by these four files**. Listed metadata is hash-checked, but stale `rc9` content can be perfectly hash-consistent. The reported metadata correction is therefore outside what these controls establish; no metadata files or corrected archive were inspected here.

### Hash lock and dependencies

- Exact manifest membership plus `sha256sum --strict -c` before and after tests detects listed content tampering and additions/deletions, subject to C1. A reference ZIP also has a literal independent-in-script digest pin (`release:42`). A rebuilt manifest is not an external trust anchor: editing files and their manifest together is not prevented or claimed to be prevented.
- Dependency installation uses a fresh external venv, explicit index, binary-only wheels, no cache, and `--require-hashes`; dependency consistency and installed versions are printed (`release:18–21`). Negative download controls require both nonzero exit and the relevant hash-rejection text (`:28–37`), reducing the risk that arbitrary network failure counts as the intended rejection.
- Those controls mutate/remove only the first matching hash and assume that changing that hash makes the requirement invalid. That is not a general test for future multi-hash requirement entries; alternate valid hashes could make controls fail. `requirements-ci.txt` itself was out of scope, so its exact lock completeness, pip bootstrap version, and wheel set were not assessed.

### Workflow equivalence and evidence boundaries

- Workflow calls the same `bash tools/ci_release.sh`, pins checkout/setup-python actions by commit, selects Python 3.12.15, grants read-only contents permission, and disables persisted checkout credentials (`verify:3–21`). Thus **shared validation procedure** is supported statically. It does not establish an observed GitHub run, identical local/GitHub environments, or independent reproduction. Action commit contents/availability were not independently checked.
- Interpreter code asserts the version tuple and prints platform/Unicode versions (`release:12`); it does not explicitly assert `sys.implementation.name == 'cpython'`. Workflow setup normally supplies CPython, but the local `RC11_PYTHON` override is not implementation-checked. This is a narrower assertion than the error message, not a demonstrated wrong interpreter.
- The script accurately labels selfchecks as **NOT RG-4** and pytest as only two modules (`release:43,50–51`). Its final shared-CI PASS must not be upgraded into Phase 1/Gate 4, §7 kill-test, B4, or independent-reproduction evidence.
- Prior local PASS and unchanged source hashes were supplied context, not verified by this review. Correcting metadata changes release bytes/manifest/archive identity. Preserve earlier archive/logs as instructed, but bind any corrected-candidate validation to its own final manifest/archive hashes; prior PASS is not by itself a run on that revision.

## Disposition

**NEEDS_FIX for the unqualified exact-inventory control claim (C1).** No unconditional runtime failure of the current candidate is established. Remaining items are explicit limits or targeted test-strengthening recommendations. Neither stale metadata correction nor shared CI resolves the separate governance questions from `REPORT.md`.
