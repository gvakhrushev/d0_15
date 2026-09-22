import D0.Geometry.ArchiveCARRelations
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# Role permutation action on the archive Fock carrier

`ArchiveFockState` is `Role → Bool`.  A role permutation acts by transporting
occupation labels.  The plain transport preserves degree and is a group
action.  The Jordan-Wigner operators use a fixed role order, so the plain
transport does not intertwine creation and annihilation.  The signed transport
multiplies by the parity of occupied inversions.  Conjugation by that signed
operator sends `c_r` to `c_{σ r}` and `c_r†` to `c_{σ r}†`, and therefore
sends the number bilinear `c_s† c_r` to `c_{σ s}† c_{σ r}`.
-/

namespace D0.Geometry.RoleFockPermutation

open D0
open D0.Geometry

/-- Occupation transported along a role permutation: the label now at `r`
is the label previously at `σ⁻¹ r`. -/
def transportState (σ : Equiv.Perm Role) (s : ArchiveFockState) : ArchiveFockState :=
  fun r => s (σ.symm r)

theorem transportState_one (s : ArchiveFockState) :
    transportState 1 s = s := by
  funext r
  rfl

theorem transportState_mul (σ τ : Equiv.Perm Role) (s : ArchiveFockState) :
    transportState (σ * τ) s = transportState σ (transportState τ s) := by
  funext r
  simp [transportState, Equiv.Perm.mul_def]

theorem transportState_leftInverse (σ : Equiv.Perm Role) :
    Function.LeftInverse (transportState σ.symm) (transportState σ) := by
  intro s
  funext r
  unfold transportState
  rw [Equiv.symm_symm]
  exact congrArg s (σ.symm_apply_apply r)

theorem transportState_bijective (σ : Equiv.Perm Role) :
    Function.Bijective (transportState σ) :=
  ⟨(transportState_leftInverse σ).injective,
   (transportState_leftInverse σ.symm).surjective⟩

theorem fockDegree_transport (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fockDegree (transportState σ s) = fockDegree s := by
  unfold fockDegree transportState
  apply Finset.card_bij (fun r _ => σ.symm r)
  · intro r hr
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hr ⊢
    simpa using hr
  · intro r₁ hr₁ r₂ hr₂ h
    exact σ.symm.injective h
  · intro t ht
    refine ⟨σ t, ?_, σ.symm_apply_apply t⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ht ⊢
    simpa [Equiv.apply_symm_apply] using ht

/-- Pairs of occupied roles whose order is reversed by `σ`. -/
def occupiedInversionCount (σ : Equiv.Perm Role) (s : ArchiveFockState) : ℕ :=
  (Finset.univ.filter fun p : Role × Role =>
    s p.1 = true ∧ s p.2 = true ∧
      roleOrderIndex p.1 < roleOrderIndex p.2 ∧
      roleOrderIndex (σ p.2) < roleOrderIndex (σ p.1)).card

def fermionSign (σ : Equiv.Perm Role) (s : ArchiveFockState) : ℤ :=
  if occupiedInversionCount σ s % 2 = 0 then 1 else -1

/-- Signed permutation matrix on occupation states. -/
def signedTransport (σ : Equiv.Perm Role)
    (bra ket : ArchiveFockState) : ℤ :=
  if bra = transportState σ ket then fermionSign σ ket else 0

theorem signedTransport_one (bra ket : ArchiveFockState) :
    signedTransport 1 bra ket = fockIdentityInt bra ket := by
  classical
  unfold signedTransport fermionSign occupiedInversionCount fockIdentityInt
  by_cases h : bra = ket
  · subst h
    have hempty : (Finset.univ.filter fun p : Role × Role =>
        bra p.1 = true ∧ bra p.2 = true ∧
          roleOrderIndex p.1 < roleOrderIndex p.2 ∧
          roleOrderIndex p.2 < roleOrderIndex p.1) = ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro p _ hp
      exact lt_asymm hp.2.2.1 hp.2.2.2
    simp [transportState_one, hempty, Finset.card_empty]
  · simp [transportState_one, h]

def fockMatMul (M N : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) : ℤ :=
  ∑ mid : ArchiveFockState, M bra mid * N mid ket

/-- The three adjacent transpositions of the fixed Jordan-Wigner order. -/
def swapAB : Equiv.Perm Role := Equiv.swap A B
def swapBC : Equiv.Perm Role := Equiv.swap B C
def swapCD : Equiv.Perm Role := Equiv.swap C D

theorem signedTransport_inv_adjacent (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport swapAB) (signedTransport swapAB.symm) bra ket =
        fockIdentityInt bra ket ∧
    fockMatMul (signedTransport swapBC) (signedTransport swapBC.symm) bra ket =
        fockIdentityInt bra ket ∧
    fockMatMul (signedTransport swapCD) (signedTransport swapCD.symm) bra ket =
        fockIdentityInt bra ket := by
  native_decide +revert

theorem signed_annihilate_intertwining_adjacent (r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (carAnnihilateInt r))
        (signedTransport swapAB.symm) bra ket = carAnnihilateInt (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (carAnnihilateInt r))
        (signedTransport swapBC.symm) bra ket = carAnnihilateInt (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (carAnnihilateInt r))
        (signedTransport swapCD.symm) bra ket = carAnnihilateInt (swapCD r) bra ket := by
  native_decide +revert

theorem signed_create_intertwining_adjacent (r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (carCreateInt r))
        (signedTransport swapAB.symm) bra ket = carCreateInt (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (carCreateInt r))
        (signedTransport swapBC.symm) bra ket = carCreateInt (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (carCreateInt r))
        (signedTransport swapCD.symm) bra ket = carCreateInt (swapCD r) bra ket := by
  native_decide +revert

/-- Number bilinear `E_sr = c_s† c_r`. -/
def numberBilinear (s r : Role) (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (carCreateInt s) (carAnnihilateInt r) bra ket

theorem numberBilinear_intertwining_adjacent (s r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (numberBilinear s r))
        (signedTransport swapAB.symm) bra ket =
          numberBilinear (swapAB s) (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (numberBilinear s r))
        (signedTransport swapBC.symm) bra ket =
          numberBilinear (swapBC s) (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (numberBilinear s r))
        (signedTransport swapCD.symm) bra ket =
          numberBilinear (swapCD s) (swapCD r) bra ket := by
  native_decide +revert

/-- A matrix preserves Fock degree when it has no matrix elements between
distinct occupation numbers. -/
def PreservesFockDegree (T : ArchiveFockState → ArchiveFockState → ℤ) : Prop :=
  ∀ bra ket, fockDegree bra ≠ fockDegree ket → T bra ket = 0

theorem numberBilinear_preserves_degree (s r : Role) (bra ket : ArchiveFockState)
    (hdeg : fockDegree bra ≠ fockDegree ket) :
    numberBilinear s r bra ket = 0 := by
  native_decide +revert

theorem signedTransport_preserves_degree (σ : Equiv.Perm Role) :
    PreservesFockDegree (signedTransport σ) := by
  intro bra ket hdeg
  unfold signedTransport
  by_cases h : bra = transportState σ ket
  · have hdeg' : fockDegree bra = fockDegree ket := by
      rw [h, fockDegree_transport]
    exact (hdeg hdeg').elim
  · simp [h]

end D0.Geometry.RoleFockPermutation
