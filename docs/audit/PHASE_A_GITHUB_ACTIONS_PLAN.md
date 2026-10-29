# Track 2 — Phase A: GitHub Actions verification plan

## Separate-UID Broker · F01 bindings · C3-E controls

**PLANNING DOCUMENT — NOT IMPLEMENTED — NOTHING EXECUTED.** Prepared by Claude (Anthropic) on 2026-10-29.

## 0. The boundary this plan never crosses

A GitHub-hosted runner is an ephemeral VM owned and operated by GitHub. The repository owner does not control it. Every result produced there is therefore **CI evidence** about the behaviour of the code on a third-party Linux image. It **is not**:

- evidence about an owner-controlled host or an isolated production host;
- an operational F01 binding (none of the 19 fields can become `OPERATIONALLY_VERIFIED` from CI);
- C3-E implementation or deployment evidence;
- B4, RG6 or Gate-4 closure.

Every Phase A artifact carries the label `EVIDENCE_CLASS = GITHUB_HOSTED_CI_ONLY` and `OWNER_HOST_EVIDENCE = NONE`. A self-hosted runner on an owner machine would be a *different* evidence class. It would need its own authorization, its own custodian record and an independent reviewer. It is out of scope for Phase A.

## 1. What Phase A can legitimately show

| ID | Claim tested on a GitHub-hosted runner | Evidence class | Gate effect |
|---|---|---|---|
| PA-1 | `tools/ci_release.sh` passes on the exact R1 bytes with CPython 3.12.15 | CI reproduction #3 (after Claude envs A and B) | none, informative only |
| PA-2 | Mechanics of a broker running under a separate UID, on a disposable VM: the worker UID cannot read the broker key or write the publisher sink, and only the broker UID can publish | design-feasibility evidence | none; does not satisfy F01-17/18 or C3-E |
| PA-3 | The negative bypass tests fail closed on the runner. This covers the 23 source routes (11 serving plus 12 other surfaces), so the 22/23 bypass finding can be measured before and after a future broker | regression oracle for a future implementation | none |
| PA-4 | F01 field *schema* validation: the owner response template (19 fields) validates against a JSON schema, and empty or `null` owner fields stay `NEEDS_OWNER_EVIDENCE` | documentary tooling | none; the owner must supply the values |
| PA-5 | Workflow hardening: pinned action SHAs, `permissions: contents: read`, `persist-credentials: false`, no secrets, artifact hashes uploaded | supply-chain hygiene | none |

## 2. Proposed workflows (draft; not added to the tree, so the tested bytes are not changed)

### 2.1 `verify.yml` (exists already)
Re-run it unchanged on a branch push of the exact R1 bytes. Record:
- the runner image version (`ImageOS`, `ImageVersion`);
- `uname -a`;
- the Python build info;
- `pip freeze`;
- the SHA-256 of the checked-out tree, recomputed from `SHA256SUMS.txt`.

### 2.2 `phase-a-broker-uid.yml` (proposal only)

```yaml
name: phase-a-broker-uid (DESIGN FEASIBILITY — NOT OWNER HOST EVIDENCE)
on: [workflow_dispatch]
permissions: { contents: read }
jobs:
  uid-separation:
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with: { persist-credentials: false }
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
        with: { python-version: "3.12.15", check-latest: false }
      - name: Create disposable UIDs (runner VM only)
        run: |
          sudo useradd --system --no-create-home eitbroker
          sudo useradd --system --no-create-home eitworker
          sudo useradd --system --no-create-home eitpublisher
          sudo install -d -o eitbroker -g eitbroker -m 0700 /srv/eit/broker
          sudo install -d -o eitpublisher -g eitpublisher -m 0750 /srv/eit/sink
          sudo install -d -o root -g root -m 0555 /srv/eit/snapshot
      - name: Read-only snapshot of the exact R1 tree
        run: |
          sudo cp -a . /srv/eit/snapshot/tree
          sudo chown -R root:root /srv/eit/snapshot/tree
          sudo chmod -R a-w /srv/eit/snapshot/tree
          (cd /srv/eit/snapshot/tree && sha256sum --strict -c SHA256SUMS.txt)
      - name: Negative controls (must all be DENIED)
        run: |
          set +e
          sudo -u eitworker test -r /srv/eit/broker && exit 1
          sudo -u eitworker touch /srv/eit/sink/x && exit 1
          sudo -u eitworker touch /srv/eit/snapshot/tree/x && exit 1
          echo "NEGATIVE_CONTROLS=DENIED_AS_EXPECTED"
      - name: Record evidence class
        run: echo "EVIDENCE_CLASS=GITHUB_HOSTED_CI_ONLY OWNER_HOST_EVIDENCE=NONE" | tee phase_a_class.txt
```

The broker program itself does **not exist yet**. `broker/broker.py` in the C3E host candidate V0.1 (`a497592b…a51`) is a placeholder that exits with status 78. Phase A tests only the OS permission scaffolding. The authenticated IPC, the trusted-publication path and the TOCTOU-free snapshot binding must first be specified, independently reviewed (IR04-O) and authorized for implementation.

### 2.3 `phase-a-bypass-matrix.yml` (proposal only)
A table-driven job enumerates the 23 routes. Each route has an expected outcome under two configurations:
- **(a)** the current V0.3 tree with no broker, where 22 or 23 routes are expected to be reachable. This is the *measured baseline* of Kimi's finding.
- **(b)** a future broker build, where every non-broker route must be denied.

Configuration (b) stays `NOT_RUN` until the broker exists. Fixture hashes are frozen before execution. RT-02 stays an application-level fixture, separate from OS/IPC denial.

## 3. F01: what CI can and cannot do

| F01 fields | Phase A contribution | Still required from the owner |
|---|---|---|
| 1 intended_offline_application, 2 owner_authenticated_identity, 3 offline_context_id, 19 owner_signed_or_chat_confirmed_scope_decision | none | an authentic owner statement or signature and its context binding |
| 4 entrypoint_routes, 5 direct/wrapper/dynamic caller inventory, 6 module loader/dependency closure | can generate a static *candidate* inventory from the tree | confirmation that it matches the actual deployment |
| 7 trusted_root_locator, 8 root custodian/permissions/revocation/rollback | none | custodian record from the actual host |
| 9–13 artifact and state hash domains, state layout | can recompute hashes of *supplied* artifacts | the authentic artifacts and their provenance from the owner context |
| 14 request/source/query/target binding, 15 check-before-use/snapshot/mutation exclusion, 16 caller-visible publication boundary | design tests on a disposable VM (PA-2, PA-3) | enforcement observed on the real host |
| 17 absolute isolated workspace, 18 absolute output dir and static ops | none (a runner path is not the owner workspace) | owner-host observation |

Result after Phase A: **F01 = 0/19 OPERATIONALLY_VERIFIED, unchanged.**

## 4. C3-E controls (all `NOT_IMPLEMENTED`)
- C3E-CONSUMER-BINDINGS
- CE-10A-STAMPS
- CE-10B-C5
- C3E-BYPASS-ROLLBACK

Phase A can only provide test oracles for these: stamp-downgrade rejection and rollback-attempt fixtures that fail today and must pass after implementation. Their failing state is recorded honestly.

## 5. Sequencing and authorizations
1. Author final GO for publishing R1. This is a separate decision from Phase A.
2. Author authorizes Phase A CI on a **private branch or fork**. No tag and no release.
3. Run PA-1 and PA-5 first. They are the cheapest and give the first GitHub reproduction.
4. Freeze the PA-2/PA-3 fixtures with hashes, then run them.
5. Hand the results to the independent reviewer (IR04-O). No gate changes state automatically.
6. Phase B: host custodian, owner host and self-hosted or offline host evidence. Out of scope here.

## 6. Non-claims
No account, runner, cloud resource or workflow was created by this plan. No credentials are needed or requested. A GitHub Actions PASS never establishes an owner-controlled, isolated production host.
