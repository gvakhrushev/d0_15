# D0

D0 is a finite-first mathematical/physical research corpus with explicit claim ownership, Lean formalization, executable certificates, and separately scoped empirical passports.

The repository has **one canonical architecture**. Development campaigns, audit snapshots, task boards, publication mirrors, and generated status ledgers are not sources of truth.

## Canonical layers

```text
01_BOOKS/           Narrative derivation, read in BOOK_00 -> BOOK_09 order
02_REGISTRY/        Canonical claim/assumption/ownership metadata
03_FORMALIZATION/   Lean proof library
04_CERTIFICATES/    Executable finite/numerical certificates and their input data
05_EXPERIMENTS/     Empirical protocols, pinned data manifests, and results
 tools/             Validators, generators, and certificate runner
 .github/           CI gates
```

### Source-of-truth rules

- **Books explain; they do not define release status.** Claim status and proof ownership live in `02_REGISTRY/claims.csv`.
- **There is one scientific claim registry.** Additional registry files describe assumptions, aliases, explicit Lean support, forcing routes, and the current frontier; they are not competing claim ledgers.
- **Lean ownership is explicit.** `D0.All` is generated from claim owners + assumption owners + `formal_support.csv`, not from every `.lean` file on disk.
- **Certificates are reachable evidence.** A certificate belongs in the release tree only if it is registered by a claim or is a dependency/input of registered evidence.
- **Generated views are reproducible.** They are regenerated from canonical registry data and checked byte-for-byte in CI.
- **Certificate runtime output is disposable.** Executing a certificate may write only under ignored `.build/cert_outputs/`; deleting `.build/` must not remove any proof input or source of truth.
- **The release tree is immutable under verification.** CI runs the certificate suite and then requires `git diff --exit-code`.
- **Empirical results never silently promote a core theorem.** External-data passports stay in `05_EXPERIMENTS` and retain their registered bridge/passport status.

## Registry

Primary file:

```text
02_REGISTRY/claims.csv
```

Supporting canonical metadata:

```text
02_REGISTRY/assumptions.csv
02_REGISTRY/formal_support.csv
02_REGISTRY/aliases.csv
02_REGISTRY/frontier/
02_REGISTRY/forcing_routes.json
02_REGISTRY/presupposition_edges.json
02_REGISTRY/gap_labels.json
```

`notes` describe the **current mathematical scope, owner, controls, and residual gap**. Session history belongs in Git history, not in the release registry.

## Generated Lean views

```bash
python tools/generate_lean_views.py
python tools/generate_lean_views.py --check
```

This owns:

```text
03_FORMALIZATION/D0/All.lean
03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean
```

Do not edit those files by hand.

## Local validation

Fast structural validation:

```bash
python tools/validate_repo.py
python tools/generate_lean_views.py --check
python -m compileall -q tools 04_CERTIFICATES
```

Registered Python evidence:

```bash
python tools/run_registered_certs.py --timeout 90 --exclude vp_scene_bartholdi_typed.py
python 04_CERTIFICATES/vp_scene_bartholdi_typed.py
```

The Bartholdi certificate is intentionally separated because it is substantially slower than the rest of the suite.

Formal build:

```bash
cd 03_FORMALIZATION
lake build D0.All
```

The toolchain is pinned by `03_FORMALIZATION/lean-toolchain`.

## Reading order

Read the books sequentially:

```text
BOOK_00 -> BOOK_01 -> BOOK_02 -> BOOK_03 -> BOOK_04
       -> BOOK_05 -> BOOK_06 -> BOOK_07 -> BOOK_08 -> BOOK_09
```

Later books may sharpen or explicitly demote earlier prose. When prose and metadata differ, use the current registry scope and the actual theorem/certificate owner.
