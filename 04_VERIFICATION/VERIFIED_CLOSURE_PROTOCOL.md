# VERIFIED CLOSURE PROTOCOL

**Purpose.** A reusable procedure for closing D0 proof-targets without fake theorem promotion. This
protocol is part of the D0 working method: future agents MUST follow it before attempting any remaining
blocker in `FINAL_CONTINUATION_BLOCKERS.csv`. It was distilled from six closure campaigns (Layer-0 gate
repair, eight-front, static-to-dynamics, Nature constrained-Hamiltonian bridge, continuation
consolidation, reheating energy budget). Guard: `05_CERTS/vp_verified_closure_protocol.py`.

A closure is **real** only when it has: an exact finite object, a genuinely-provable Lean theorem (or a
finite executable cert / formal no-go / explicit passport over a frozen internal object), reachable
negative controls, a book-source patch, a registry row, and a green gate. Status migration alone is
never a closure.

---

## Phases

### Phase 0 — identify owner and exact blocker
Read `04_VERIFICATION/FINAL_CONTINUATION_BLOCKERS.csv` and the registry
(`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`). Confirm the claim ID, its current status, and the
**exact missing artifact**. Grep the repo for the ID and near-synonyms — if a related claim already
exists, update it; never mint a duplicate. Hard-freeze new claim IDs except those the task allows.

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
Every cert prints `STRUCTURE_FIXED_BEFORE_NUMBER:` as its first output line and contains at least one
reachable `FAIL_*` negative control that actually fires (mutation-tested), with no bare `PASS`. Close
every docstring `"""` on its own line (a mid-line close false-flags later asserts in
`check_cert_can_fail`).

### Phase 5 — book / registry integration
Edit only source fragments (never generated `BOOK_*.md`); reassemble with `tools/assemble_books.py`.
Register the row; regenerate aggregates (`tools/generate_lean_aggregates.py`) and the status map. Cert
references in book prose MUST be backtick-wrapped and carry no `05_CERTS/` path prefix (publication
guard). PROOF-TARGET registry rows use `lean_status = OPEN`; passport rows use `PYTHON_CERTIFIED`.

### Phase 6 — full gate and final report
Run the full gate and `lake build D0.All`; commit one reviewable unit; emit the report template below.

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
Claims CERT-CLOSED:
Claims NO-GO:
Claims still PROOF-TARGET:
FINAL_CONTINUATION_BLOCKERS.csv delta:
Gate:
  validate_csv:
  check_sync:
  assemble_books:
  registered certs:
  d0_score --strict:
  lake build:
Remaining exact blockers:
```

No essays. No "almost". No "global closure" language unless the blocker file shows zero blockers.
