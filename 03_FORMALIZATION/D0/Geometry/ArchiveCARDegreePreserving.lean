import Mathlib.Tactic
import D0.Geometry.ArchiveCARRelations
import D0.Geometry.RoleFockPermutation

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# Degree-preserving CAR envelope

`E_sr = c_s† c_r` preserves Fock degree and obeys

  [E_sr, E_tu] = δ_rt E_su - δ_us E_tr.

The degree sectors have dimensions `1,4,6,4,1`, so the associative algebra of all
degree-preserving fibre endomorphisms has dimension `70`.  That algebra is an
available coefficient envelope.  Its unit group is not identified with a physical
gauge or connection group.  Signed role permutations conjugate `E_sr` to
`E_{σ s, σ r}` and preserve the bracket.  This file does not prove that the
CAR bilinears span the 70-dimensional algebra.
-/

/-- `E_sr = c_s† c_r`.  The first index is the creation label. -/
def carEnd (s r : Role) (bra ket : ArchiveFockState) : ℝ :=
  ∑ mid : ArchiveFockState, carCreate s bra mid * carAnnihilate r mid ket

def carEndInt (s r : Role) (bra ket : ArchiveFockState) : ℤ :=
  ∑ mid : ArchiveFockState, carCreateInt s bra mid * carAnnihilateInt r mid ket

theorem carEnd_eq_intCast (s r : Role) (bra ket : ArchiveFockState) :
    carEnd s r bra ket = (carEndInt s r bra ket : ℝ) := by
  unfold carEnd carEndInt
  simp

def carEndCommInt (s r t u : Role) (bra ket : ArchiveFockState) : ℤ :=
  (∑ p : ArchiveFockState, carEndInt s r bra p * carEndInt t u p ket) -
    (∑ p : ArchiveFockState, carEndInt t u bra p * carEndInt s r p ket)

theorem carEnd_degree_preserving (s r : Role) (bra ket : ArchiveFockState)
    (hdeg : fockDegree bra ≠ fockDegree ket) :
    carEnd s r bra ket = 0 := by
  classical
  unfold carEnd
  apply Finset.sum_eq_zero
  intro mid _
  by_cases hc : carCreate s bra mid = 0
  · rw [hc]
    simp
  · by_cases ha : carAnnihilate r mid ket = 0
    · rw [ha]
      simp
    · have hcreate := carCreate_degree_raise s bra mid hc
      have hann := carAnnihilate_degree_lower r mid ket ha
      have : fockDegree bra = fockDegree ket := by omega
      exact absurd this hdeg

theorem carEnd_lie_int :
    ∀ s r t u : Role, ∀ bra ket : ArchiveFockState,
      carEndCommInt s r t u bra ket =
        roleDeltaInt r t * carEndInt s u bra ket -
          roleDeltaInt u s * carEndInt t r bra ket := by
  native_decide

theorem carEnd_lie (s r t u : Role) (bra ket : ArchiveFockState) :
    (∑ p, carEnd s r bra p * carEnd t u p ket) -
        (∑ p, carEnd t u bra p * carEnd s r p ket) =
      roleDelta r t * carEnd s u bra ket -
        roleDelta u s * carEnd t r bra ket := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (carEnd_lie_int s r t u bra ket)
  simpa [carEndCommInt, carEnd_eq_intCast, roleDelta_eq_intCast] using h

theorem fock_sector_card_zero :
    Fintype.card {s : ArchiveFockState // fockDegree s = 0} = 1 := by
  native_decide

theorem fock_sector_card_one :
    Fintype.card {s : ArchiveFockState // fockDegree s = 1} = 4 := by
  native_decide

theorem fock_sector_card_two :
    Fintype.card {s : ArchiveFockState // fockDegree s = 2} = 6 := by
  native_decide

theorem fock_sector_card_three :
    Fintype.card {s : ArchiveFockState // fockDegree s = 3} = 4 := by
  native_decide

theorem fock_sector_card_four :
    Fintype.card {s : ArchiveFockState // fockDegree s = 4} = 1 := by
  native_decide

/-- Dimension of `⊕_k End(F^k)`, the degree-preserving coefficient envelope. -/
theorem degreePreservingEndomorphismDimension :
    Fintype.card {s : ArchiveFockState // fockDegree s = 0} ^ 2 +
      Fintype.card {s : ArchiveFockState // fockDegree s = 1} ^ 2 +
      Fintype.card {s : ArchiveFockState // fockDegree s = 2} ^ 2 +
      Fintype.card {s : ArchiveFockState // fockDegree s = 3} ^ 2 +
      Fintype.card {s : ArchiveFockState // fockDegree s = 4} ^ 2 = 70 := by
  rw [fock_sector_card_zero, fock_sector_card_one, fock_sector_card_two,
    fock_sector_card_three, fock_sector_card_four]
  norm_num

theorem carEndInt_eq_numberBilinear (s r : Role) (bra ket : ArchiveFockState) :
    carEndInt s r bra ket = RoleFockPermutation.numberBilinear s r bra ket := by
  unfold carEndInt RoleFockPermutation.numberBilinear RoleFockPermutation.fockMatMul
  rfl

theorem carEndCommInt_eq_numberCommutator (s r t u : Role) (bra ket : ArchiveFockState) :
    carEndCommInt s r t u bra ket =
      RoleFockPermutation.numberCommutator s r t u bra ket := by
  unfold carEndCommInt RoleFockPermutation.numberCommutator
  simp [carEndInt_eq_numberBilinear, RoleFockPermutation.fockMatMul]

/-- Signed role transport is a bracket automorphism of the CAR number bilinears.
The dimension count `70` remains the count of all degree-preserving endomorphisms. -/
theorem perm_conj_carEndCommInt (σ : Equiv.Perm Role) (s r t u : Role)
    (bra ket : ArchiveFockState) :
    RoleFockPermutation.conjTransport σ (fun b k => carEndCommInt s r t u b k) bra ket =
      carEndCommInt (σ s) (σ r) (σ t) (σ u) bra ket := by
  have hfun : (fun b k => carEndCommInt s r t u b k) =
      RoleFockPermutation.numberCommutator s r t u := by
    ext b k
    exact carEndCommInt_eq_numberCommutator s r t u b k
  rw [hfun, carEndCommInt_eq_numberCommutator]
  exact RoleFockPermutation.perm_conj_numberCommutator σ s r t u bra ket

theorem perm_conj_carEndInt (σ : Equiv.Perm Role) (s r : Role) (bra ket : ArchiveFockState) :
    RoleFockPermutation.conjTransport σ (fun b k => carEndInt s r b k) bra ket =
      carEndInt (σ s) (σ r) bra ket := by
  have hfun : (fun b k => carEndInt s r b k) = RoleFockPermutation.numberBilinear s r := by
    ext b k
    exact carEndInt_eq_numberBilinear s r b k
  rw [hfun, carEndInt_eq_numberBilinear]
  exact RoleFockPermutation.perm_conj_carBilinear σ s r bra ket

end D0.Geometry
