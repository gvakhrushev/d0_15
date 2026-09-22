> **Scope Notice:** This document is an operating procedure for proof/cert verification, NOT the definition of done. The canonical Definition of Done is located at `02_REGISTRY/CLOSURE_CONTRACT.md`.

# VERIFIED CLOSURE PROTOCOL

**Purpose.** A reusable procedure for closing D0 proof-targets without fake theorem promotion.
While `00_WORK/manifest.json` governs ALL active work, this verification protocol applies specifically
to `EXPENSIVE` and `WORKER` tasks that investigate or implement claim closure, theorems, certificates,
no-go bounds, or empirical passports. `CONTROL` tasks are governed by `00_WORK/README.md`, manifest
invariants, and control review; a CONTROL task is not required to carry a claim ID, book patch,
certificate, or negative control. Guard: `04_CERTIFICATES/vp_verified_closure_protocol.py`.

A closure is **real** only when it has: an exact finite object, a genuinely-provable Lean theorem (or a
finite executable cert / formal no-go / explicit passport over a frozen internal object), reachable
negative controls, a book-source patch, a registry row, and a green gate. Status migration alone is
never a closure.

---

## Phases

### Phase 0 — identify owner and exact blocker
The active work source is `00_WORK/manifest.json`. (`continuation_frontier.csv` is a legacy registry/frontier input, not an active task queue). For `EXPENSIVE` and `WORKER` tasks, `affected_claims` are already fixed by the manifest; `CONTROL` tasks may carry `affected_claims = []`. Read the assigned task brief in `00_WORK/tasks/` and the registry (`02_REGISTRY/claims.csv`). Confirm the claim ID, its current status, and the **exact missing artifact**. Grep the repo for the ID and near-synonyms — if a related claim already exists, update it; never mint a duplicate. Hard-freeze new claim IDs except those explicitly authorized by CONTROL.

### Phase 1 — grounded verification scout
Before any Lean is written, a scout VERIFIES the mathematical route by actually computing the key
finite quantity (a rank, a branch index, a Laurent coefficient, a spectrum sum, a linear-system
solution space) in throwaway code. The supplied construction is a *proposed design*, not a fact.

### Phase 2 — honest scope decision
The scout returns exactly one verdict (see **Verify-then-build rule**). The closable scope is fixed
*before* implementation, so red-flag routes get an honest PARTIAL/NO-GO/NOT-CLOSABLE instead of a faked
theorem. Name the exact remaining artifact for anything not fully closed.

### Phase 3 — Lean / cert implementation
Implement only the verified-closable scope. Use robust finite/decidable tactics (decide, native_decide,
norm_num, ring, linarith, omega, Matrix/Fin decide, div_pos, nlinarith). No `sorry`/`admit`/`axiom`, no
`:= True`/`noGo := True`/`:= rfl`-on-substantive-goal shell, no hardcoded target value presented as a
derivation. If a goal will not close cleanly, NARROW the statement until it is honestly provable. See
**Lean integration recurring fixes**.

### Phase 4 — negative controls
Policy for new and modified certificates: each should print `STRUCTURE_FIXED_BEFORE_NUMBER:` as its first output line and contain at least one reachable `FAIL_*` negative control that actually fires (mutation-tested), with no bare `PASS`. (Note: while this is authoring policy for new/modified certs, it is not globally machine-enforced across all historical certs). Close every docstring `"""` on its own line (a mid-line close false-flags later asserts in `check_cert_can_fail`).

### Phase 5 — book / registry integration
Update the affected registry rows in `02_REGISTRY/claims.csv` and any corresponding documentation. Update active work tracking in `00_WORK/manifest.json` and regenerate status views via `python tools/render_work_status.py`. Cert references in book prose MUST be backtick-wrapped and carry no `04_CERTIFICATES/` path prefix (publication guard). Preserve the existing registry status vocabulary and set lean_status/release_status only according to the literal owned scope and current registry contract. CP1 does not normalize their cross-product.

### Phase 6 — full gate and final report
Run mandatory integration checks:
1. `python tools/validate_repo.py`
2. `python tools/generate_lean_views.py --check`
3. `python tools/validate_work.py --self-test`
4. `python tools/validate_work.py`
5. `python tools/render_work_status.py --check`
6. `python tools/run_registered_certs.py --workers 6 --timeout 90 --exclude vp_scene_bartholdi_typed.py`
7. `lake build D0.All` (when Lean-import-reachable formalization scope is touched)

### Lean build-cache policy (MANDATORY)

For ordinary `WORKER` / `EXPENSIVE` implementation loops, builds are **incremental by default**.

- During editing, build the narrowest affected target/module first.
- Before PR/REVIEW, run one incremental `lake build D0.All` if Lean-import-reachable scope changed.
- Do **not** run `lake clean`, delete `.lake`, remove the Mathlib cache, or otherwise force a cold rebuild as routine proof evidence.
- A cold rebuild is a special CONTROL/release diagnostic only: use it after a Lean/Mathlib/toolchain or dependency-manifest change, after confirmed cache corruption/staleness, or when CONTROL explicitly requests cache-independence evidence.
- GitHub `lean-build` remains the independent integration gate and already uses the pinned Mathlib cache on a fresh checkout.

Repeated `lake build D0.All` after source changes may reuse the local Lake cache; this is expected and desirable. Cache reuse does not weaken theorem checking for changed/import-reachable modules.

Commit one reviewable unit; emit the report template below.

---

## Verify-then-build rule (MANDATORY)

> No high-load proof-target may receive Lean code before a grounded verification scout checks the
> mathematical route.

The scout returns exactly one verdict:

- `CERT-CLOSABLE` — a finite positive owner exists.
- `NO-GO-CLOSABLE` — the route is provably blocked; name the next constructive route.
- `PARTIAL-CLOSABLE` — a narrow piece is closable; name the exact remaining artifact.
- `NOT-CLOSABLE` — no honest owner; keep PROOF-TARGET with the exact missing lemma.
- `DUPLICATE-ALREADY-OWNED` — an existing claim already owns this; do not mint.

The scout MUST explicitly test for: finite-trace poles; hidden continuum assumptions; row-uniqueness
failures; external-theorem imports; status-only closure; data-fitted formulas; vacuous-Lean-theorem
risk.

**Worked red-flag examples (all caught by scouts in prior campaigns):**
- A finite 30-dimensional heat trace has **no** `1/s` pole (`c₋₁=0`, `c₀=dim=30`); a Dixmier residue
  needs the infinite/profinite tower.
- The hypercharge anomaly variety **contains B−L** and is 2-dimensional; the SM row is not unique by
  anomaly-freedom alone.
- Riemann–Hurwitz genus-0 cyclic covers do **not** force lepton branch-index uniqueness.
- Parity alone does **not** exclude CKM class 5 (class 1 and class 5 share the parity fibre).
- CMB `n_s` is **not** determined by the finite spectrum without a canonical smoothing owner.

---

## Cloud formalization draft phase

A \`PLANNED\` worker may have its Lean implementation prepared in advance by a **cloud formalizer** that does not have the local warm Lean/Mathlib cache.

This is a draft phase, not worker acceptance:

- keep the manifest task state \`PLANNED\`;
- use a dedicated branch such as \`draft/<task-slug>\` from the stated canonical baseline;
- prefer isolated owner modules and theorem proofs; avoid editing \`manifest.json\`, \`STATUS.md\`, generated views, claim status, or release metadata;
- run narrow Lean checks only if the cloud environment can do so cheaply; a full \`D0.All\` build is not required;
- never claim \`LEAN_PROVED\`/CORE or move the task to \`REVIEW\`;
- commit and push the candidate implementation;
- finish with a \`CLOUD_DRAFT_READY\` handoff containing base/head SHA, changed files, intended capstones, checks actually run, unchecked gates, and known API/proof risks.

When a local worker slot opens, the worker starts from the cloud draft branch (rebased/merged onto fresh canonical main as needed), tries to compile the draft before redesigning it, fixes concrete Lean/API failures, performs the normal incremental verification gates, updates shared metadata, then moves the task to \`REVIEW\`.


## Worker checkout / dispatch policy

Terminology in user-facing coordination:
- manifest class \`WORKER\` = **worker**;
- manifest class \`EXPENSIVE\` = **researcher**.

Workers mutate repository state; researchers normally do not.

Two workers may execute concurrently only when they use separate git worktrees/checkouts. They may intentionally share the external Lake/Mathlib cache. If only one checkout/working directory is available, worker execution is sequential.

Dispatch each worker task separately. Do not put two worker launch prompts into one combined packet. This keeps branch ownership, generated metadata, and shared-cache behavior explicit.


## Lean integration recurring fixes

- ℝ division definitions often need `noncomputable` (real `Inv`/`Div` is noncomputable; `+`/`*` are fine).
- `div_lt_iff` may need `div_lt_iff₀` in the current Mathlib pin (the `₀` ordered-field variants).
- Avoid theorem/def name collisions across files by using a **sub-namespace** (e.g.
  `D0.Cosmology.CMBLaplacianIDS` rather than redefining `totalMult` in the shared `D0.Cosmology`).
- Do **not** append `norm_num` after `simp` if `simp` already closes the goal ("No goals to be solved").
- `neg_neg` does **not** close by `rfl` (e.g. `1 = -(-1)`); finish with `norm_num`/`ring`.
- `positivity` cannot prove `0 ≤ φ⁻¹^k` without `φ⁻¹ ≥ 0` in scope; supply it (`pow_nonneg ...`).
- Parallel-drafted modules MUST be `lake build`-verified (and fixed) **before** registry promotion.

---

## No-overclaim guard discipline

A no-overclaim guard MUST be **negation-aware**. It must not fail on honest prose such as
"does not claim DESI confirms D0" or "no SM table imported as proof". Prefer scanning registry claim
notes and status rows, or flag an occurrence only when it is NOT preceded by a negation
(`no`, `not`, `never`, `n't`, `without`, `≠`); never grep-scan the guard's own disclaimer text. The
forbidden phrases are licensed only when the blocker file shows zero global blockers.

---

## Closure report template (mandatory)

```
Commit:
Files changed:
Lean modules:
Certificates:
Claims affected:
Active task (00_WORK/manifest.json):
Gate:
  validate_repo:
  generate_lean_views --check:
  validate_work (--self-test and repo):
  render_work_status --check:
  registered certs:
  lake build (if Lean touched):
Remaining exact blockers:
```

No essays. No "almost". No "global closure" language unless the blocker file shows zero blockers.
