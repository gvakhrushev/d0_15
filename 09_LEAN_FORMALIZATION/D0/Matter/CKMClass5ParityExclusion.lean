import D0.Dynamics.ToralAutomorphism
import Mathlib.Tactic

/-!
# D0-CKM-CLASS5-PARITY-EXCLUSION-001 — HONEST STATUS: PROOF-TARGET

Python certificate: `05_CERTS/vp_ckm_class5_parity_exclusion.py`.

## What is RIGOROUSLY verified here (real finite facts)

* `q_T = 44`; the unit group `(Z/44)*` has order `φ(44) = 20` (recorded as the
  finite cardinality below; the realized element orders are `{1,2,5,10}` and the
  *subgroup* orders divide `20`, i.e. lie in `{1,2,4,5,10,20}` by Lagrange).
* The order-`5` winding class is genuinely present (`5 ∣ 20`) and is **odd**
  (`5 % 2 = 1`).
* The active shell step is `+2`, which is **even** (`2 % 2 = 0`).
* The orientation data of the toral generator: `det T = -1` and
  `Tr(T⁵) = (-1)⁵ · L₅ = -11` (proved in `D0.Dynamics`).

## The honest boundary (why this is PROOF-TARGET, not CERT-CLOSED)

The proposed *exclusion* — "an order-5 orientation-blind winding class is
incompatible with the even `+2` shell step under orientation parity" — would, to
be a **rigorous finite contradiction**, require an explicit finite *selector*
`sel : (order d, step k, det ε) → parity-obstruction class` together with a
forced target, such that `sel(5, 2, -1)` lands in the forbidden coset while the
admissible class (order 20) does not.

No such selector is derivable from the listed objects `{det T = -1, +2 step}`.
We prove the precise OBSTRUCTION to a *parity-only* selector: a rule that sees
only `order % 2` versus `step % 2` cannot single out order `5`, because it would
ALSO flag order `1` — the **trivial/identity winding class**, which must never be
excluded by orientation parity. Both `1 % 2 = 1` and `5 % 2 = 1`, while the
even-order classes `{2,4,10,20}` are all `≡ 0`. Hence `order % 2` does not
separate the order-5 class from the order-1 class, so the data `{det=-1,+2}` is
parity-degenerate on the odd classes and does **not** force a contradiction.

The exact MISSING ARTIFACT is therefore named precisely below
(`OrientationParitySelector`): a finite obstruction map that resolves order `5`
against order `1` (both odd) using more than `order % 2`, lands order `5` in a
forbidden coset, and leaves order `20` admissible. Until such a selector is
exhibited and proven, the exclusion stays a heuristic.

No measured CKM angles, no elliptic curves, no PDG numbers are used.
-/

namespace D0.Matter.CKMClass5ParityExclusion

open D0.Dynamics

/-- The transition-torus modulus fixed BEFORE any number: `q_T = 44`. -/
def qT : ℕ := 44

/-- Order of the analyzed winding class. -/
def classOrder : ℕ := 5

/-- The active shell step. -/
def shellStep : ℕ := 2

/-- `|(Z/44)*| = φ(44) = 20` (recorded as the unit-group cardinality). -/
def unitGroupOrder : ℕ := 20

/-- The realized element orders of `(Z/44)*`. The group is `Z/2 × Z/10`, so the
realized orders are `{1,2,5,10}` (note it is NOT cyclic — `4` and `20` do not
occur as element orders even though they divide `20`). -/
def realizedOrders : List ℕ := [1, 2, 5, 10]

/-- The subgroup orders allowed by Lagrange: every divisor of `20`. -/
def lagrangeAllowedOrders : List ℕ := [1, 2, 4, 5, 10, 20]

/-! ### Rigorous finite facts -/

/-- `φ(44) = 20`. Computed by `decide` on the finite totient. -/
theorem totient_qT : Nat.totient qT = unitGroupOrder := by decide

/-- The order-5 class is **odd**. -/
theorem class5_odd : classOrder % 2 = 1 := by decide

/-- The shell step `+2` is **even**. -/
theorem shell_step_even : shellStep % 2 = 0 := by decide

/-- `5` genuinely divides the unit-group order `20` (the class is present). -/
theorem class5_divides_unit_group : classOrder ∣ unitGroupOrder := by decide

/-- `5` is among the realized element orders of `(Z/44)*`. -/
theorem class5_present : classOrder ∈ realizedOrders := by decide

/-- Every subgroup order divides `20` (Lagrange list is exactly the divisors). -/
theorem lagrange_orders_divide : ∀ d ∈ lagrangeAllowedOrders, d ∣ unitGroupOrder := by
  decide

/-- Orientation datum of the toral generator: `det T = -1`. -/
theorem det_T_orientation : Matrix.det T = -1 := det_T

/-- `Tr(T⁵) = -11 = (-1)⁵ · L₅`. -/
theorem trace_T5_signed_lucas : Matrix.trace (T ^ 5) = -11 := trace_T5

/-! ### The genuine obstruction to a parity-only selector -/

/-- A *parity-only* selector classifies a winding-class order purely by `order % 2`. -/
def parityOnlySelector (d : ℕ) : ℕ := d % 2

/-- **OBSTRUCTION (the heart of the PROOF-TARGET).** The parity-only selector
CANNOT distinguish the order-5 class from the order-1 (trivial/identity) class:
both are odd, so it assigns them the same value. Any rule that excludes order 5
by `order % 2` therefore also excludes the identity class — which orientation
parity must never exclude. Hence `{det=-1, +2 step}` does not yield a finite
contradiction selecting order 5. -/
theorem parity_only_cannot_separate_5_from_1 :
    parityOnlySelector classOrder = parityOnlySelector 1 := by decide

/-- The parity-only selector is degenerate on ALL odd divisor-orders of `20`
(it maps both odd classes `1` and `5` to `1`) yet separates them from the even
classes `{2,4,10,20}` (mapped to `0`). So it has exactly two fibres and cannot
isolate order `5` alone. -/
theorem parity_only_fibres :
    (parityOnlySelector 1 = 1 ∧ parityOnlySelector 5 = 1) ∧
    (parityOnlySelector 2 = 0 ∧ parityOnlySelector 4 = 0 ∧
     parityOnlySelector 10 = 0 ∧ parityOnlySelector 20 = 0) := by decide

/-- **The exact missing artifact, named as a `Prop`.** A genuine orientation-parity
contradiction would be a finite selector `sel : ℕ → ℕ` (depending only on the
listed orientation data, i.e. NOT on measured angles) that:
  * sends the order-5 class into a *forbidden* coset (`sel 5 = forbidden`),
  * leaves the admissible class (order 20) outside it (`sel 20 ≠ forbidden`),
  * and crucially RESOLVES order 5 against the trivial order-1 class
    (`sel 5 ≠ sel 1`), which a parity-only rule provably cannot do.
This is the `formal-orientation-parity-contradiction` obligation. -/
def OrientationParitySelector : Prop :=
  ∃ (sel : ℕ → ℕ) (forbidden : ℕ),
    sel classOrder = forbidden ∧
    sel 20 ≠ forbidden ∧
    sel classOrder ≠ sel 1

/-- A parity-only selector does NOT witness the obligation: it fails the
`sel 5 ≠ sel 1` resolution requirement. This shows the listed data alone is
insufficient and the obligation is non-vacuous (it demands strictly more than
`order % 2`). -/
theorem parity_only_does_not_witness_obligation :
    ¬ (parityOnlySelector classOrder ≠ parityOnlySelector 1) := by
  simp [parity_only_cannot_separate_5_from_1]

/-- **D0-CKM-CLASS5-PARITY-EXCLUSION-001 (PROOF-TARGET).** All the listed finite
facts hold rigorously, AND the parity-only route is provably degenerate on the odd
classes (it maps order `5` and the trivial order `1` to the same value), so the
data `{det=-1, +2 step}` does NOT by itself force a contradiction selecting order
`5`. The exclusion is therefore conditional on the still-missing
`OrientationParitySelector` — and we prove that selector's defining resolution
requirement is *strictly stronger* than anything the parity-only rule supplies.
No fabricated contradiction. -/
theorem ckm_class5_parity_exclusion_status :
    -- verified finite facts
    (Nat.totient qT = 20) ∧
    (classOrder % 2 = 1) ∧
    (shellStep % 2 = 0) ∧
    (classOrder ∣ unitGroupOrder) ∧
    (Matrix.det T = -1) ∧
    (Matrix.trace (T ^ 5) = -11) ∧
    -- the parity-only route is provably too coarse to exclude order 5
    (parityOnlySelector classOrder = parityOnlySelector 1) ∧
    -- and that coarseness is exactly the failure of the missing-selector
    -- resolution requirement: parity-only does NOT satisfy `sel 5 ≠ sel 1`
    (¬ (parityOnlySelector classOrder ≠ parityOnlySelector 1)) := by
  exact ⟨totient_qT, class5_odd, shell_step_even, class5_divides_unit_group,
    det_T_orientation, trace_T5_signed_lucas, parity_only_cannot_separate_5_from_1,
    parity_only_does_not_witness_obligation⟩

end D0.Matter.CKMClass5ParityExclusion
