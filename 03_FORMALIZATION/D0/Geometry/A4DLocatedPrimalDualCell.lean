import Mathlib.Tactic
import D0.Geometry.A4DPrimalDualCellPairing

/-!
# Located primal and dual cells

`occupationComplement` and `algebraicComplementPairing` stay the same-site
algebraic owners. This file places the complementary label at a different
archive corner:

`F_PD(x,S) = (x - 1_{Sᶜ}, Sᶜ)` and `F_DP(y,T) = (y + 1_T, Tᶜ)`.

Primal and dual remain distinct types. The placement is an inverse pair on
every cycle length `L = N + 2`, including `L = 2`, and it does not divide by 2.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

/-- A primal archive cell: corner in the role-phase group and an occupation label. -/
structure PrimalCell (N : ℕ) where
  site : ArchiveRolePhaseGroup N
  label : ArchiveFockState

/-- A dual archive cell. The type is not identified with `PrimalCell`. -/
structure DualCell (N : ℕ) where
  site : ArchiveRolePhaseGroup N
  label : ArchiveFockState

def PrimalCell.toBasis {N : ℕ} (c : PrimalCell N) : ArchiveCochainBasis N :=
  (c.site, c.label)

def DualCell.toBasis {N : ℕ} (c : DualCell N) : ArchiveCochainBasis N :=
  (c.site, c.label)

def PrimalCell.ofBasis {N : ℕ} (p : ArchiveCochainBasis N) : PrimalCell N where
  site := p.1
  label := p.2

def DualCell.ofBasis {N : ℕ} (p : ArchiveCochainBasis N) : DualCell N where
  site := p.1
  label := p.2

@[simp] theorem PrimalCell.ofBasis_toBasis {N : ℕ} (c : PrimalCell N) :
    PrimalCell.ofBasis c.toBasis = c := rfl

@[simp] theorem DualCell.ofBasis_toBasis {N : ℕ} (c : DualCell N) :
    DualCell.ofBasis c.toBasis = c := rfl

/-- Indicator `1_S = ∑_{r ∈ S} e_r` in the archive site group. -/
def occupationIndicator (N : ℕ) (S : ArchiveFockState) : ArchiveRolePhaseGroup N :=
  fun r => if S r then 1 else 0

@[simp] theorem occupationIndicator_apply (N : ℕ) (S : ArchiveFockState) (r : Role) :
    occupationIndicator N S r = if S r then 1 else 0 := rfl

theorem occupationIndicator_eq_sum (N : ℕ) (S : ArchiveFockState) :
    occupationIndicator N S =
      ∑ r : Role, if S r then roleStep N r else 0 := by
  classical
  funext s
  simp only [occupationIndicator, Finset.sum_apply]
  rw [Finset.sum_eq_single s]
  · by_cases h : S s <;> simp [h, roleStep]
  · intro r _ hrs
    by_cases h : S r <;> simp [h, roleStep, Ne.symm hrs]
  · simp

theorem occupationIndicator_complement_sum (N : ℕ) (S : ArchiveFockState) :
    occupationIndicator N S + occupationIndicator N (occupationComplement S) =
      fun _ => 1 := by
  funext r
  by_cases h : S r
  · simp [occupationIndicator, occupationComplement, h]
  · simp [occupationIndicator, occupationComplement, h]

theorem occupationIndicator_complement_involutive (N : ℕ) (S : ArchiveFockState) :
    occupationIndicator N (occupationComplement (occupationComplement S)) =
      occupationIndicator N S := by
  simp [occupationComplement_involutive]

/-- Insert one unoccupied role. -/
def insertRole (S : ArchiveFockState) (r : Role) : ArchiveFockState :=
  fun s => if s = r then true else S s

theorem insertRole_degree (S : ArchiveFockState) (r : Role) (h : S r = false) :
    fockDegree (insertRole S r) = fockDegree S + 1 := by
  classical
  unfold fockDegree insertRole
  have hsplit : (Finset.univ.filter fun s => (if s = r then true else S s) = true) =
      insert r (Finset.univ.filter fun s => S s = true) := by
    ext s
    by_cases hs : s = r
    · subst hs
      simp [h]
    · simp [hs]
  have hnot : r ∉ Finset.univ.filter fun s => S s = true := by
    simp [h]
  rw [hsplit, Finset.card_insert_of_notMem hnot]

/-- Delete one role from an occupation label. -/
def removeRole (S : ArchiveFockState) (r : Role) : ArchiveFockState :=
  fun s => if s = r then false else S s

theorem fockDegree_le_four (S : ArchiveFockState) : fockDegree S ≤ 4 := by
  have hcard : Fintype.card Role = 4 := by decide
  simpa [fockDegree, hcard] using
    Finset.card_le_card (Finset.filter_subset (fun r : Role => S r = true) Finset.univ)

theorem removeRole_insertRole (S : ArchiveFockState) (r : Role) (h : S r = false) :
    removeRole (insertRole S r) r = S := by
  funext s
  by_cases hs : s = r
  · simp [removeRole, insertRole, hs, h]
  · simp [removeRole, insertRole, hs]

theorem insertRole_removeRole (S : ArchiveFockState) (r : Role) (h : S r = true) :
    insertRole (removeRole S r) r = S := by
  funext s
  by_cases hs : s = r
  · simp [removeRole, insertRole, hs, h]
  · simp [removeRole, insertRole, hs]

theorem occupationComplement_insertRole (S : ArchiveFockState) (r : Role) :
    occupationComplement (insertRole S r) =
      removeRole (occupationComplement S) r := by
  funext s
  by_cases hs : s = r
  · simp [occupationComplement, insertRole, removeRole, hs]
  · simp [occupationComplement, insertRole, removeRole, hs]

theorem occupationComplement_removeRole (S : ArchiveFockState) (r : Role) :
    occupationComplement (removeRole S r) =
      insertRole (occupationComplement S) r := by
  funext s
  by_cases hs : s = r
  · simp [occupationComplement, insertRole, removeRole, hs]
  · simp [occupationComplement, insertRole, removeRole, hs]

/-- Located placement of a primal cell onto its complementary dual corner. -/
def locatedPrimalToDual {N : ℕ} (c : PrimalCell N) : DualCell N where
  site := c.site - occupationIndicator N (occupationComplement c.label)
  label := occupationComplement c.label

/-- Reverse placement. The added indicator is the dual label, not the complement. -/
def locatedDualToPrimal {N : ℕ} (c : DualCell N) : PrimalCell N where
  site := c.site + occupationIndicator N c.label
  label := occupationComplement c.label

theorem locatedDualToPrimal_leftInverse (N : ℕ) (c : PrimalCell N) :
    locatedDualToPrimal (locatedPrimalToDual c) = c := by
  cases c with
  | mk site label =>
    simp only [locatedPrimalToDual, locatedDualToPrimal, occupationComplement_involutive]
    congr 1
    simp only [sub_eq_add_neg]
    abel

theorem locatedDualToPrimal_rightInverse (N : ℕ) (c : DualCell N) :
    locatedPrimalToDual (locatedDualToPrimal c) = c := by
  cases c with
  | mk site label =>
    simp only [locatedPrimalToDual, locatedDualToPrimal, occupationComplement_involutive]
    congr 1
    simp only [sub_eq_add_neg]
    abel

theorem located_placement_inverse_l2 (c : PrimalCell 0) :
    locatedDualToPrimal (locatedPrimalToDual c) = c :=
  locatedDualToPrimal_leftInverse 0 c

theorem located_placement_inverse_l3 (c : PrimalCell 1) :
    locatedDualToPrimal (locatedPrimalToDual c) = c :=
  locatedDualToPrimal_leftInverse 1 c

theorem located_placement_inverse_l5 (c : PrimalCell 3) :
    locatedDualToPrimal (locatedPrimalToDual c) = c :=
  locatedDualToPrimal_leftInverse 3 c

theorem located_placement_inverse_l2_dual (c : DualCell 0) :
    locatedPrimalToDual (locatedDualToPrimal c) = c :=
  locatedDualToPrimal_rightInverse 0 c

theorem located_placement_inverse_l3_dual (c : DualCell 1) :
    locatedPrimalToDual (locatedDualToPrimal c) = c :=
  locatedDualToPrimal_rightInverse 1 c

theorem located_placement_inverse_l5_dual (c : DualCell 3) :
    locatedPrimalToDual (locatedDualToPrimal c) = c :=
  locatedDualToPrimal_rightInverse 3 c

/-- Complementary degree on every occupation, including degrees 0 through 4. -/
theorem degree_complement_of_degree (k : ℕ) (_hk : k ≤ 4) (S : ArchiveFockState)
    (hS : fockDegree S = k) :
    fockDegree (occupationComplement S) = 4 - k := by
  rw [degree_complement, hS]

theorem complement_degree_even_parity (S : ArchiveFockState) :
    (fockDegree (occupationComplement S)) % 2 = fockDegree S % 2 := by
  rw [degree_complement]
  have hle : fockDegree S ≤ 4 := by
    have hcard : Fintype.card Role = 4 := by decide
    simpa [fockDegree, hcard] using
      Finset.card_le_card (Finset.filter_subset (fun r => S r = true) Finset.univ)
  omega

theorem fockParitySign_occupationComplement (S : ArchiveFockState) :
    fockParitySign (occupationComplement S) = fockParitySign S := by
  unfold fockParitySign
  rw [fockOccupationCount_eq_fockDegree, fockOccupationCount_eq_fockDegree,
    complement_degree_even_parity]

/-- Absolute corner `a(S) = c + 1_S` in the translation-placement class. -/
def centerMatchedCorner (N : ℕ) (c : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    ArchiveRolePhaseGroup N :=
  c + occupationIndicator N S

theorem centerMatchedCorner_insert (N : ℕ) (c : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) (r : Role) (h : S r = false) :
    centerMatchedCorner N c (insertRole S r) =
      centerMatchedCorner N c S + roleStep N r := by
  classical
  funext s
  simp only [centerMatchedCorner, occupationIndicator, insertRole, Pi.add_apply, roleStep]
  by_cases hs : s = r
  · subst hs
    simp [h]
  · simp [hs]

theorem centerMatchedCorner_eq_indicator (N : ℕ) (S : ArchiveFockState) :
    centerMatchedCorner N 0 S = occupationIndicator N S := by
  simp [centerMatchedCorner]

theorem occupationIndicator_insertRole (N : ℕ) (S : ArchiveFockState) (r : Role)
    (h : S r = false) :
    occupationIndicator N (insertRole S r) =
      occupationIndicator N S + roleStep N r := by
  simpa [centerMatchedCorner, centerMatchedCorner_eq_indicator] using
    centerMatchedCorner_insert N 0 S r h

/-- The reference rule meets the existing one-role center-match test. -/
theorem locatedPrimalToDual_centerMatched (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    (locatedPrimalToDual (PrimalCell.mk x (occupationComplement (fockSingletonState D0.A)))).site =
      roleTranslateMinus N D0.A x := by
  classical
  have hcompl : occupationComplement (occupationComplement (fockSingletonState D0.A)) =
      fockSingletonState D0.A := occupationComplement_involutive _
  simp only [locatedPrimalToDual, hcompl, roleTranslateMinus, roleTranslate, sub_eq_add_neg]
  funext s
  have htrue : fockSingletonState D0.A D0.A = true := by simp [fockSingletonState]
  simp only [Pi.add_apply]
  by_cases hs : s = D0.A
  · subst hs
    simp [htrue, roleStep, occupationIndicator, fockSingletonState]
  · have hfalse : fockSingletonState D0.A s = false := by
      simp [fockSingletonState, hs]
    simp [hfalse, roleStep, hs, occupationIndicator]

/-- Primal cochain. The carrier is not the dual cochain type. -/
structure PrimalCochain (N : ℕ) where
  coeff : ArchiveCochain N

/-- Dual cochain. Distinct from `PrimalCochain`. -/
structure DualCochain (N : ℕ) where
  coeff : ArchiveCochain N

theorem PrimalCochain.ext {N : ℕ} {ψ φ : PrimalCochain N}
    (h : ψ.coeff = φ.coeff) : ψ = φ := by
  cases ψ
  cases φ
  cases h
  rfl

theorem DualCochain.ext {N : ℕ} {ψ φ : DualCochain N}
    (h : ψ.coeff = φ.coeff) : ψ = φ := by
  cases ψ
  cases φ
  cases h
  rfl

instance {N : ℕ} : Zero (PrimalCochain N) where
  zero := ⟨0⟩

instance {N : ℕ} : Add (PrimalCochain N) where
  add ψ φ := ⟨ψ.coeff + φ.coeff⟩

instance {N : ℕ} : SMul ℝ (PrimalCochain N) where
  smul a ψ := ⟨a • ψ.coeff⟩

instance {N : ℕ} : Neg (PrimalCochain N) where
  neg ψ := ⟨-ψ.coeff⟩

instance {N : ℕ} : Zero (DualCochain N) where
  zero := ⟨0⟩

instance {N : ℕ} : Add (DualCochain N) where
  add ψ φ := ⟨ψ.coeff + φ.coeff⟩

instance {N : ℕ} : SMul ℝ (DualCochain N) where
  smul a ψ := ⟨a • ψ.coeff⟩

instance {N : ℕ} : Neg (DualCochain N) where
  neg ψ := ⟨-ψ.coeff⟩

end D0.Geometry
