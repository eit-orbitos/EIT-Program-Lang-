# DIFF LOG V0.9 → V0.10 (rc10) — workflow layer only

Prepared by Tasklet, 2026-10-24, at the author's instruction (evidence path (i)). Add-only release candidate; V0.9 (`a43ff961…c79a`) is unchanged.

| File | Change | Item |
|---|---|---|
| `.github/workflows/verify.yml` | `permissions: contents: read`; `runs-on: ubuntu-24.04`; actions pinned to full commit SHAs (checkout v4.4.0 `11d5960a…`, setup-python v5.6.0 `a26af69b…`); `persist-credentials: false`; inventory check + stray-file self-test; `pip install --require-hashes -r requirements-ci.txt`; pytest `-p no:cacheprovider` | N-8(a)(d)(e) |
| `tools/ci_inventory_check.sh` | new | N-8(a) |
| `requirements-ci.txt` | new (pytest 8.3.3 + iniconfig, packaging, pluggy with SHA-256) | N-8(d) |
| `DIFF_LOG_V09_TO_V10.md` | new (this file) | — |
| `SHA256SUMS.txt` | regenerated over the full tree | — |

All other files are byte-identical to V0.9, including the verifier (`97b1d148…`), builder, companion, tests, fixtures, license files, README, CITATION and the stale `tests/CI_LOCAL_RUN.log` (documentary issues outside this change).

Residual (disclosed): the `ubuntu-24.04` image is still updated by GitHub; `python-version: "3.12"` resolves to the toolcache patch release; the action SHAs were read from the upstream tags on 2026-10-24 and are trusted as published.
