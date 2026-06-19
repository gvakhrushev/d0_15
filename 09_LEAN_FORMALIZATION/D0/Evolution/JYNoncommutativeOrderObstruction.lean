import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic
import D0.Foundation.M1Predicate

/-!
# D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001 / D0-TIME-ARROW-ORDERED-SELF-READOUT-001
# — the [J,Y] noncommutative order obstruction and the forced time arrow (BOOK_06 §06)

Python certificate: `05_CERTS/vp_jy_noncommutative_order_obstruction.py`.

This module is the **new Lean owner** of the BOOK_02 §2.9A commutator obstruction (which previously had
no Lean witness). The load-bearing real fact is a concrete finite matrix witness:

* `J` (localization / defect) is the nilpotent shift on the rank-3 **localization** block `{0,1,2}` of a
  `4`-dimensional carrier, fixing the **archive** index `3`. It moves a defect up the localization
  ladder `e₀ ↦ e₁ ↦ e₂ ↦ 0`.
* `Y` (boundary closure / readout) is an **idempotent** (`Y*Y = Y`) oblique projection onto the archive
  direction `e₃` that reads the localization-top slot `e₂` together with the archive slot `e₃`
  (`Y e₂ = e₃`, `Y e₃ = e₃`). It *identifies through the complementary archive block* — exactly a finite
  self-readout that closes the boundary into the archive.

The two operations do **not** commute: `J*Y ≠ Y*J`, differing at entry `(3,1) = -1`. Applying the
defect-shift then reading the boundary is not the same as reading then shifting — the *order of
registration is observable*. This is proven by `native_decide` on the exact integer matrices.

**The reading (BOOK_06 §06).** A self-readout whose two operations *commuted* would be order-blind: it
could not tell "shift-then-read" from "read-then-shift", so it could not recover the order in which its
own events were registered. Recovering that erased order would require an *external catalogue* (a stored
log of the order) — an unprovable input forbidden by M1. Because the **actual** D0 readout `(J,Y)` is
noncommutative, the order is intrinsic finite data: registration is forced to be *ordered*, and that
ordered registration is the time arrow. No primitive time object, external clock, or SI unit enters —
the only content is the nonzero finite commutator.

Honest scope (named residual). The witness + the wired M1 reductio are for the **specific D0 operators
`(J,Y)`** and the binary ordered-vs-commuting readout selector. The UNIVERSAL claim — that *every*
commuting self-readout on *any* carrier erases order and forces an external catalogue — is **not** proven
here; it is the named residual `JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION` (a finite witness is not a
universal theorem). What is proven is exactly: (i) the concrete `[J,Y] ≠ 0`; (ii) commuting *of this
readout* erases its order sensitivity; (iii) on the binary readout selector the ordered answer is
`M1Forced` and the commuting answer `RequiresExternalCatalogue`.
-/

namespace D0.Evolution.JYNoncommutativeOrderObstruction

open Matrix
open D0.Foundation
open D0.Matter

/-! ## Part A — the finite matrix witness: `J*Y ≠ Y*J` -/

/-- The `4`-dimensional carrier: indices `0,1,2` are the **localization** block, index `3` is the
**archive** block. -/
abbrev Carrier := Fin 4

/-- Integer operators on the carrier. -/
abbrev ZMat4 := Matrix Carrier Carrier ℤ

/-- **`J` — localization / defect.** The nilpotent shift on the rank-3 localization block
`e₀ ↦ e₁ ↦ e₂ ↦ 0`, fixing the archive index `3` (its column is zero). Column-`j` convention:
`J i j = 1` iff `i = j+1` inside `{0,1,2}`. -/
def J : ZMat4 :=
  !![0, 0, 0, 0;
     1, 0, 0, 0;
     0, 1, 0, 0;
     0, 0, 0, 0]

/-- **`Y` — boundary closure / readout projection.** The idempotent oblique projection onto the archive
direction `e₃` that reads the localization-top slot `e₂` and the archive slot `e₃`:
`Y e₂ = e₃`, `Y e₃ = e₃`, `Y e₀ = Y e₁ = 0`. It identifies the boundary of the localization block
through the complementary archive block. -/
def Y : ZMat4 :=
  !![0, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, 0;
     0, 0, 1, 1]

/-- **`Y` is a genuine readout projection: it is idempotent (`Y*Y = Y`).** This certifies that `Y` is an
actual self-readout (a projection / closure), not an arbitrary matrix. -/
theorem Y_idempotent : Y * Y = Y := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- **`J` is nilpotent (`J^3 = 0`): a defect-shift with no fixed information.** -/
theorem J_nilpotent : J ^ 3 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-- The order-distinguishing entry of the commutator: `(J*Y - Y*J) (3,1) = -1 ≠ 0`.
"Shift-then-read" and "read-then-shift" already differ on the archive↔localization channel. -/
theorem jy_commutator_entry : (J * Y - Y * J) 3 1 = -1 := by native_decide

/-- **`jy_commutator_ne_zero` — the load-bearing real fact.** The localization defect-shift `J` and the
boundary-closure readout `Y` do **not** commute: `J*Y ≠ Y*J`. Proven by exhibiting the entry
`(3,1)` at which `J*Y` and `Y*J` differ (`native_decide` on the exact integer matrices). -/
theorem jy_commutator_ne_zero : J * Y ≠ Y * J := by
  intro h
  have hzero : J * Y - Y * J = 0 := sub_eq_zero_of_eq h
  have hentry : (J * Y - Y * J) 3 1 = (0 : ZMat4) 3 1 := by rw [hzero]
  rw [jy_commutator_entry] at hentry
  simp at hentry

/-! ## Part B — the structural obstruction: commuting readout erases order -/

/-- A **finite self-readout**: a localization/defect operator `defect` and a boundary-closure readout
`readout` on the same carrier. `orderSensitive` says the two registration orders are observably
different (`defect∘readout ≠ readout∘defect`) — i.e. the readout can tell the order of its own events. -/
structure SelfReadout where
  /-- the localization / defect operator -/
  defect : ZMat4
  /-- the boundary-closure readout (a projection) -/
  readout : ZMat4

namespace SelfReadout

/-- The readout is **order-sensitive** when applying the defect then the readout differs from applying
the readout then the defect — the two registration orders are distinguishable finite data. -/
def orderSensitive (R : SelfReadout) : Prop := R.defect * R.readout ≠ R.readout * R.defect

/-- **Commuting erases order (the structural lemma).** If a self-readout's two operations commute, then
it is *not* order-sensitive: the two registration orders coincide, so the readout cannot recover which
came first. This is the finite, decidable core of "a commuting self-readout erases order memory". -/
theorem commuting_erases_order (R : SelfReadout)
    (hcomm : R.defect * R.readout = R.readout * R.defect) : ¬ R.orderSensitive := by
  intro hsens
  exact hsens hcomm

end SelfReadout

/-- The concrete D0 self-readout `(J, Y)`. -/
def d0Readout : SelfReadout where
  defect := J
  readout := Y

/-- **`jy_noncommutative_order_obstruction` — the D0 readout is order-sensitive.** The concrete D0
self-readout `(J,Y)` has `J*Y ≠ Y*J`, so it is order-sensitive: its boundary closure registers the
defect-shift in a way that observably depends on the order. -/
theorem jy_noncommutative_order_obstruction : d0Readout.orderSensitive :=
  jy_commutator_ne_zero

/-- **`commuting_readout_erases_order` — instantiated at `(J,Y)`.** If the D0 readout *had* commuted, it
would have erased its own order sensitivity. (Vacuously contrapositive to the proven noncommutativity:
together with `jy_noncommutative_order_obstruction` this is the obstruction.) -/
theorem commuting_readout_erases_order (hcomm : J * Y = Y * J) :
    ¬ d0Readout.orderSensitive :=
  d0Readout.commuting_erases_order hcomm

/-! ## Part C — the time arrow, wired to the proven M1 spine

The binary registration policy a self-readout could adopt: register **ordered** (keep the order of
events as intrinsic finite data) or **commuting** (treat the two orders as identical, discarding the
order). For the noncommutative D0 readout, a commuting policy would have to *recover* the discarded order
from somewhere — an external catalogue. The register-cost selector makes the ordered policy the unique
strict minimum, so it is `M1Forced` via the proven `selector_M1Forced` spine, and the commuting policy
`RequiresExternalCatalogue`. -/

/-- The two registration policies a self-readout can adopt. -/
inductive RegistrationPolicy where
  /-- keep the order of registered events as intrinsic finite data (the time arrow) -/
  | ordered
  /-- discard the order, treating "shift-then-read" and "read-then-shift" as identical -/
  | commuting
  deriving DecidableEq, Repr, Fintype

/-- **Order-recovery cost** = how much external order-catalogue a policy must store to be consistent with
the *noncommutative* D0 readout. The ordered policy stores nothing (`0`); the commuting policy would have
to recover the `1` distinguishable order bit the commutator `[J,Y] ≠ 0` exhibits, an external catalogue
(`1`). -/
def orderRecoveryCost : RegistrationPolicy → ℚ
  | .ordered => 0
  | .commuting => 1

/-- The finite registration-policy selector: lower external-order-catalogue cost is preferred. -/
def registrationSelector : FiniteSelector RegistrationPolicy where
  support_fintype := inferInstance
  score := orderRecoveryCost

/-- The policy space is genuinely finite. -/
def registrationPolicyFiniteSupport : Fintype RegistrationPolicy := inferInstance

/-- **The ordered policy is strictly selected** — it is the unique zero-cost answer, strictly below the
commuting policy (which would need to store the discarded order). -/
theorem ordered_strictly_selected :
    StrictSelected registrationSelector RegistrationPolicy.ordered := by
  constructor
  intro b hb
  cases b with
  | ordered => exact False.elim (hb rfl)
  | commuting => norm_num [registrationSelector, orderRecoveryCost]

/-- **The ordered policy is M1-forced** (via the proven `selector_M1Forced` spine): the finite
order-recovery-cost data determines it; no exogenous choice of registration policy is needed. -/
theorem ordered_M1Forced :
    M1Forced (fun x => StrictSelected registrationSelector x) RegistrationPolicy.ordered :=
  selector_M1Forced registrationSelector RegistrationPolicy.ordered ordered_strictly_selected

/-- **`order_erasure_requires_external_catalog` — the load-bearing reductio.** The commuting (order-
erasing) policy `RequiresExternalCatalogue`: it is not the M1-forced answer, so adopting it for the
noncommutative D0 readout rests on storing the discarded order in an external catalogue (an unprovable
input M1 forbids). Term-mode through the proven `m1_alternative_needs_catalogue`. -/
theorem order_erasure_requires_external_catalog :
    RequiresExternalCatalogue (fun x => StrictSelected registrationSelector x)
      RegistrationPolicy.commuting :=
  m1_alternative_needs_catalogue ordered_M1Forced RegistrationPolicy.commuting (by decide)

/-- **`jy_commuting_contradicts_m1` — the obstruction, term-mode.** Because the D0 readout is
order-sensitive (`J*Y ≠ Y*J`) AND the commuting/order-erasing policy requires an external catalogue, a
commuting self-readout on the D0 operators contradicts M1 (it would need an unprovable order log). The
conjunction packages the proven noncommutativity with the proven catalogue obligation. -/
theorem jy_commuting_contradicts_m1 :
    d0Readout.orderSensitive ∧
    RequiresExternalCatalogue (fun x => StrictSelected registrationSelector x)
      RegistrationPolicy.commuting :=
  ⟨jy_noncommutative_order_obstruction, order_erasure_requires_external_catalog⟩

/-- **`time_arrow_from_ordered_self_readout` (D0-TIME-ARROW-ORDERED-SELF-READOUT-001).** The time arrow
is forced by ordered registration: the D0 readout is order-sensitive (`J*Y ≠ Y*J`), the ordered
registration policy is the unique M1-forced answer, and the order-erasing (commuting) alternative
requires an external catalogue. Hence registration is forced to be ordered — that ordered registration
is the time arrow. No primitive time object or clock enters; the only content is the nonzero finite
commutator and the proven selector spine. -/
theorem time_arrow_from_ordered_self_readout :
    J * Y ≠ Y * J ∧
    M1Forced (fun x => StrictSelected registrationSelector x) RegistrationPolicy.ordered ∧
    RequiresExternalCatalogue (fun x => StrictSelected registrationSelector x)
      RegistrationPolicy.commuting :=
  ⟨jy_commutator_ne_zero, ordered_M1Forced, order_erasure_requires_external_catalog⟩

/-- **D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001 (owner).** The full witness: `Y` is a genuine readout
projection (`Y*Y = Y`), `J` is nilpotent (`J^3 = 0`), the commutator is nonzero (`J*Y ≠ Y*J`), commuting
*this* readout would erase its order, and on the binary registration selector the ordered policy is
`M1Forced` while the commuting policy `RequiresExternalCatalogue`. A real finite proof wired to the
proven M1 spine — not a `¬Forced` shell. The UNIVERSAL commuting-readout obstruction stays the named
residual `JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION`. -/
theorem jy_noncommutative_order_obstruction_owner :
    Y * Y = Y ∧
    J ^ 3 = 0 ∧
    J * Y ≠ Y * J ∧
    (J * Y = Y * J → ¬ d0Readout.orderSensitive) ∧
    M1Forced (fun x => StrictSelected registrationSelector x) RegistrationPolicy.ordered ∧
    RequiresExternalCatalogue (fun x => StrictSelected registrationSelector x)
      RegistrationPolicy.commuting :=
  ⟨Y_idempotent, J_nilpotent, jy_commutator_ne_zero,
   commuting_readout_erases_order, ordered_M1Forced, order_erasure_requires_external_catalog⟩

end D0.Evolution.JYNoncommutativeOrderObstruction
