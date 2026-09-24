import Mathlib.Tactic
import D0.Geometry.A4DSecondOrderEnergyCovariance
import D0.Geometry.A4DLocatedPrimalDualCell
import D0.Geometry.A4DLocatedTopologicalStar
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveMovingDifferential
import D0.Geometry.A4DPathWordParentWard

set_option maxRecDepth 8192
set_option maxHeartbeats 0

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# Scalar Cartan second-order witness

This module owns exact finite matrix controls on the five-cycle. It does not
select `c`, a matter second jet `K`, or a physical finite action.
-/

abbrev FiveCycleMatrix := Matrix (Fin 5) (Fin 5) ℚ
abbrev FiveCycleVector := Fin 5 → ℚ

def fiveCycleSucc (x : Fin 5) : Fin 5 := ⟨(x.val + 1) % 5, by omega⟩

def fiveCycleShift : FiveCycleMatrix := fun x y =>
  if y = fiveCycleSucc x then 1 else 0

def fiveCycleDelta (x : Fin 5) : ℚ := if x.val = 0 then 1 else 0

def fiveCycleD : FiveCycleMatrix :=
  (5 / 2 : ℚ) • (fiveCycleShift - fiveCycleShift.transpose)

def fiveCycleBackgroundDerivative : FiveCycleMatrix :=
  (5 : ℚ) • (fiveCycleShift - 1)

def fiveCycleGaugeVector : FiveCycleVector := fun x =>
  if x.val = 0 then -5 else if x.val = 4 then 5 else 0

theorem fiveCycleGaugeVector_eq_delta_difference :
    fiveCycleGaugeVector = fun x =>
      (5 : ℚ) * (fiveCycleDelta (fiveCycleSucc x) - fiveCycleDelta x) := by
  funext x
  fin_cases x <;>
    norm_num [fiveCycleGaugeVector, fiveCycleDelta, fiveCycleSucc]

def fiveCycleCartanTangent : FiveCycleMatrix := fun x y =>
  if x.val = 0 ∧ y.val = 1 then (5 / 2 : ℚ)
  else if x.val = 0 ∧ y.val = 4 then -(5 / 2 : ℚ)
  else 0

def scalarCellFirstJet (a : FiveCycleVector) : FiveCycleMatrix :=
  fun x y =>
    if y.val = (x.val + 1) % 5 then a x / 2
    else if x.val = (y.val + 1) % 5 then a y / 2
    else 0

def scalarCellHessian (c : ℚ) : FiveCycleMatrix :=
  (2 * c : ℚ) • Matrix.diagonal (fun x => fiveCycleGaugeVector x ^ 2)

theorem fiveCycleGaugeVector_values :
    fiveCycleGaugeVector 0 = -5 ∧
      fiveCycleGaugeVector 1 = 0 ∧ fiveCycleGaugeVector 4 = 5 ∧
      fiveCycleGaugeVector 2 = 0 ∧ fiveCycleGaugeVector 3 = 0 := by
  norm_num [fiveCycleGaugeVector] <;> decide

/-- On the five-cycle, the owned scalar first jet is the negative symmetric
Cartan tangent. -/
theorem fiveCycle_scalar_firstWard :
    scalarCellFirstJet fiveCycleGaugeVector =
      -(fiveCycleCartanTangent + fiveCycleCartanTangent.transpose) := by
  ext x y
  fin_cases x <;> fin_cases y <;>
    norm_num [scalarCellFirstJet, fiveCycleGaugeVector, fiveCycleDelta,
      fiveCycleSucc, fiveCycleCartanTangent, Fin.ext_iff] <;> ring

/-- The delta Cartan tangent is supported only in row zero, so its square
vanishes. -/
theorem fiveCycleCartanTangent_sq :
    fiveCycleCartanTangent * fiveCycleCartanTangent = 0 := by
  ext x y
  rw [Matrix.mul_apply]
  fin_cases x <;> fin_cases y <;>
    norm_num [fiveCycleCartanTangent, Fin.sum_univ_succ] <;> decide

/-- The transpose tangent is supported only in column zero, so its square
also vanishes. -/
theorem fiveCycleCartanTangent_transpose_sq :
    fiveCycleCartanTangent.transpose * fiveCycleCartanTangent.transpose = 0 := by
  calc
    fiveCycleCartanTangent.transpose * fiveCycleCartanTangent.transpose =
        (fiveCycleCartanTangent * fiveCycleCartanTangent).transpose := by
          rw [Matrix.transpose_mul]
    _ = 0 := by rw [fiveCycleCartanTangent_sq]; exact Matrix.transpose_zero

/-- Every scalar first-jet matrix in this stencil has zero diagonal. -/
theorem scalarCellFirstJet_diagonal (a : FiveCycleVector) (x : Fin 5) :
    scalarCellFirstJet a x x = 0 := by
  fin_cases x <;>
    norm_num [scalarCellFirstJet, fiveCycleSucc, Fin.ext_iff]

/-- The nonzero `2 GᵀG` diagonal at the forward neighbour of the delta. -/
theorem twiceCartanGram_forward_diagonal :
    ((2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent)) 1 1 =
      25 / 2 := by
  change 2 * (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) 1 1 = 25 / 2
  rw [Matrix.mul_apply]
  norm_num [fiveCycleCartanTangent, Fin.sum_univ_succ] <;> decide

/-- Exponential completion cannot match either diagonal cell Hessian model;
the forward-neighbour diagonal is independent of `a` and `c`. -/
theorem deltaCartan_exponentialSecondOrder_noCellDiagonalCompletion
    (c : ℚ) (a : FiveCycleVector) :
    scalarCellFirstJet a + scalarCellHessian c ≠
      secondOrderCongruenceCoefficient fiveCycleCartanTangent
        (fiveCycleCartanTangent * fiveCycleCartanTangent) := by
  intro heq
  have hcoeff : secondOrderCongruenceCoefficient fiveCycleCartanTangent
      (fiveCycleCartanTangent * fiveCycleCartanTangent) =
      (2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) := by
    rw [secondOrderCongruenceCoefficient_eq, fiveCycleCartanTangent_sq,
      fiveCycleCartanTangent_transpose_sq]
    simp [Matrix.transpose_zero]
  have hdiag := congrFun (congrFun heq 1) 1
  rw [hcoeff] at hdiag
  have hzero := scalarCellFirstJet_diagonal a 1
  have hz : (scalarCellFirstJet a) 1 1 = 0 := hzero
  simp only [Matrix.add_apply] at hdiag
  rw [hz] at hdiag
  have hcell : scalarCellHessian c 1 1 = 0 := by
    simp [scalarCellHessian, fiveCycleGaugeVector, fiveCycleDelta,
      fiveCycleSucc, Matrix.diagonal]
  rw [hcell, twiceCartanGram_forward_diagonal] at hdiag
  norm_num at hdiag

/-- The same forward-neighbour obstruction rejects the zero matter second
jet, for every scalar diagonal coefficient and background acceleration. -/
theorem deltaCartan_zeroSecondJet_noCellDiagonalCompletion
    (c : ℚ) (a : FiveCycleVector) :
    scalarCellFirstJet a + scalarCellHessian c ≠
      secondOrderCongruenceCoefficient fiveCycleCartanTangent 0 := by
  intro heq
  have hcoeff : secondOrderCongruenceCoefficient fiveCycleCartanTangent 0 =
      (2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) := by
    rw [secondOrderCongruenceCoefficient_eq, fiveCycleCartanTangent_sq,
      fiveCycleCartanTangent_transpose_sq]
    simp [Matrix.transpose_zero]
  have hdiag := congrFun (congrFun heq 1) 1
  rw [hcoeff] at hdiag
  have hzero := scalarCellFirstJet_diagonal a 1
  have hz : (scalarCellFirstJet a) 1 1 = 0 := hzero
  simp only [Matrix.add_apply] at hdiag
  rw [hz] at hdiag
  have hcell : scalarCellHessian c 1 1 = 0 := by
    simp [scalarCellHessian, fiveCycleGaugeVector, fiveCycleDelta,
      fiveCycleSucc, Matrix.diagonal]
  rw [hcell, twiceCartanGram_forward_diagonal] at hdiag
  norm_num at hdiag

/-- For an arbitrary matter second jet, the Ward equation determines only its
symmetric part. This keeps the antisymmetric freedom visible. -/
theorem deltaCartan_generalSecondJet_symmetric_part (c : ℚ)
    (K : FiveCycleMatrix)
    (hward : scalarCellFirstJet 0 + scalarCellHessian c =
      secondOrderCongruenceCoefficient fiveCycleCartanTangent K) :
    K.transpose + K =
      (2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) -
        scalarCellHessian c := by
  rw [secondOrderCongruenceCoefficient_eq, fiveCycleCartanTangent_sq,
    fiveCycleCartanTangent_transpose_sq] at hward
  have hzero : scalarCellFirstJet 0 = 0 := by
    ext x y
    fin_cases x <;> fin_cases y <;>
      norm_num [scalarCellFirstJet, fiveCycleSucc, Fin.ext_iff]
  rw [hzero] at hward
  have hsmul : (2 : ℚ) • (0 : FiveCycleMatrix) = 0 := smul_zero _
  rw [hsmul] at hward
  simp only [zero_add, add_zero] at hward
  have hward' : scalarCellHessian c =
      (2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) -
        (K.transpose + K) := by
    exact hward
  have hA : (2 : ℚ) • (fiveCycleCartanTangent.transpose * fiveCycleCartanTangent) =
      scalarCellHessian c + (K.transpose + K) :=
    (sub_eq_iff_eq_add.mp hward'.symm)
  rw [hA]
  abel

/-- The full symmetric block for the owned delta witness at zero background
acceleration. The off-diagonal endpoint condition is retained. -/
theorem deltaCartan_generalSecondJet_full_symmetric_block (c : ℚ)
    (K : FiveCycleMatrix)
    (hward : scalarCellFirstJet 0 + scalarCellHessian c =
      secondOrderCongruenceCoefficient fiveCycleCartanTangent K) :
    K 1 1 + K 1 1 = 25 / 2 ∧
      K 0 0 + K 0 0 = -50 * c ∧
      K 4 4 + K 4 4 = 25 / 2 - 50 * c ∧
      K 1 4 + K 4 1 = -25 / 2 := by
  have hsym := deltaCartan_generalSecondJet_symmetric_part c K hward
  have h11 := congrFun (congrFun hsym 1) 1
  have h00 := congrFun (congrFun hsym 0) 0
  have h44 := congrFun (congrFun hsym 4) 4
  have h14 := congrFun (congrFun hsym 1) 4
  norm_num [scalarCellHessian, fiveCycleGaugeVector, fiveCycleDelta,
    fiveCycleSucc, fiveCycleCartanTangent, Matrix.diagonal,
    Matrix.transpose_apply, Matrix.mul_apply, Fin.sum_univ_succ] at h11 h00 h44 h14
  ring_nf at h11 h00 h44 h14
  constructor
  · nlinarith [h11]
  constructor
  · nlinarith [h00]
  constructor
  · nlinarith [h44]
  · simpa [add_comm] using h14

/-! ## Generic occupied three-site block

The next algebra is parameterized by the cycle length. The three coordinates
are `0,+1,-1`; the hypothesis `3 ≤ L` is the distinct-site condition. This
is the exact nonzero-support block, with every other cycle row and column zero.
-/

abbrev GenericDeltaBlock := Matrix (Fin 3) (Fin 3) ℚ

def genericDeltaCartanTangent (L : ℕ) : GenericDeltaBlock := fun i j =>
  if i.val = 0 ∧ j.val = 1 then (L : ℚ) / 2
  else if i.val = 0 ∧ j.val = 2 then -((L : ℚ) / 2)
  else 0

/-- Tangent for the translated delta at site `+1` in the same three-site
window. -/
def genericDeltaCartanTangentShifted (L : ℕ) : GenericDeltaBlock := fun i j =>
  if i.val = 1 ∧ j.val = 2 then (L : ℚ) / 2
  else if i.val = 1 ∧ j.val = 0 then -((L : ℚ) / 2)
  else 0

def genericDeltaGaugeVector (L : ℕ) : Fin 3 → ℚ := fun i =>
  if i.val = 0 then -(L : ℚ) else if i.val = 2 then (L : ℚ) else 0

def genericDeltaGram (L : ℕ) : GenericDeltaBlock := fun i j =>
  if i.val = 1 ∧ j.val = 1 then (L : ℚ) ^ 2 / 4
  else if i.val = 1 ∧ j.val = 2 then -((L : ℚ) ^ 2 / 4)
  else if i.val = 2 ∧ j.val = 1 then -((L : ℚ) ^ 2 / 4)
  else if i.val = 2 ∧ j.val = 2 then (L : ℚ) ^ 2 / 4
  else 0

def genericDeltaCellHessian (L : ℕ) (c : ℚ) : GenericDeltaBlock :=
  (2 * c : ℚ) • Matrix.diagonal (fun i => genericDeltaGaugeVector L i ^ 2)

theorem genericDeltaCartanTangent_sq (L : ℕ) :
    genericDeltaCartanTangent L * genericDeltaCartanTangent L = 0 := by
  ext i j
  rw [Matrix.mul_apply]
  fin_cases i <;> fin_cases j <;>
    norm_num [genericDeltaCartanTangent, Fin.sum_univ_succ] <;> ring

theorem genericDeltaCartanTangent_transpose_sq (L : ℕ) :
    (genericDeltaCartanTangent L).transpose *
      (genericDeltaCartanTangent L).transpose = 0 := by
  calc
    (genericDeltaCartanTangent L).transpose *
        (genericDeltaCartanTangent L).transpose =
        (genericDeltaCartanTangent L * genericDeltaCartanTangent L).transpose := by
          rw [Matrix.transpose_mul]
    _ = 0 := by rw [genericDeltaCartanTangent_sq]; exact Matrix.transpose_zero

/-- The owned abelian translations have noncommuting scalar Cartan tangents;
the `(0,0)` commutator is `-L²/4` for every `L ≥ 3`. -/
theorem genericDeltaCartanTangent_noncommuting (L : ℕ) (_hL : 3 ≤ L) :
    (genericDeltaCartanTangent L * genericDeltaCartanTangentShifted L -
      genericDeltaCartanTangentShifted L * genericDeltaCartanTangent L) 0 0 =
        -((L : ℚ) ^ 2 / 4) := by
  rw [Matrix.sub_apply, Matrix.mul_apply, Matrix.mul_apply]
  norm_num [genericDeltaCartanTangent, genericDeltaCartanTangentShifted,
    Fin.sum_univ_succ] <;> ring

/-- A background-independent additive representation has commuting
infinitesimal generators. The two owned delta translations violate that
necessary condition, so no such representation can realize both tangents.
This is scoped to the stipulated tangent assignment. -/
theorem no_commuting_representation_of_genericDelta_tangents
    (L : ℕ) (hL : 3 ≤ L)
    (hcomm : genericDeltaCartanTangent L * genericDeltaCartanTangentShifted L =
      genericDeltaCartanTangentShifted L * genericDeltaCartanTangent L) : False := by
  have hentry := congrFun (congrFun hcomm 0) 0
  have hnonzero := genericDeltaCartanTangent_noncommuting L hL
  rw [Matrix.sub_apply] at hnonzero
  have hzero :
      (genericDeltaCartanTangent L * genericDeltaCartanTangentShifted L) 0 0 -
        (genericDeltaCartanTangentShifted L * genericDeltaCartanTangent L) 0 0 = 0 := by
    rw [hentry]
    ring
  rw [hzero] at hnonzero
  norm_num at hnonzero
  have hLq : (3 : ℚ) ≤ (L : ℚ) := by exact_mod_cast hL
  have hLcast : (L : ℚ) = 0 := by exact_mod_cast hnonzero
  linarith

theorem genericDeltaCartanTangent_gram (L : ℕ) :
    (genericDeltaCartanTangent L).transpose * genericDeltaCartanTangent L =
      genericDeltaGram L := by
  ext i j
  rw [Matrix.mul_apply]
  fin_cases i <;> fin_cases j <;>
    norm_num [genericDeltaCartanTangent, genericDeltaGram,
      Fin.sum_univ_succ] <;> ring

/-- The complete generic-`L` symmetric-second-jet equation. An arbitrary
zero-diagonal background first jet is retained, so this records precisely
what the quadratic Ward fixes without guessing a matter `K`. -/
theorem genericDelta_secondJet_symmetric_part (L : ℕ) (c : ℚ)
    (H K : GenericDeltaBlock) (hdiag : ∀ i, H i i = 0)
    (hward : H + genericDeltaCellHessian L c =
      secondOrderCongruenceCoefficient (genericDeltaCartanTangent L) K) :
    K.transpose + K =
      (2 : ℚ) • genericDeltaGram L - H - genericDeltaCellHessian L c := by
  have hcoeff : secondOrderCongruenceCoefficient (genericDeltaCartanTangent L) K =
      (2 : ℚ) • genericDeltaGram L - (K.transpose + K) := by
    rw [secondOrderCongruenceCoefficient_eq,
      genericDeltaCartanTangent_sq L,
      genericDeltaCartanTangent_transpose_sq L,
      genericDeltaCartanTangent_gram L]
    simp [smul_zero, Matrix.transpose_zero]
  rw [hcoeff] at hward
  have hsum : (2 : ℚ) • genericDeltaGram L - (K.transpose + K) =
      H + genericDeltaCellHessian L c := hward.symm
  have hA : (2 : ℚ) • genericDeltaGram L =
      H + genericDeltaCellHessian L c + (K.transpose + K) :=
    sub_eq_iff_eq_add.mp hsum
  rw [hA]
  abel

/-- All three generic diagonal conditions and the full mixed endpoint
condition; the latter explicitly retains the first-jet entry for `L=3`. -/
theorem genericDelta_secondJet_diagonals_and_mixed (L : ℕ) (hL : 3 ≤ L)
    (c : ℚ) (H K : GenericDeltaBlock) (hdiag : ∀ i, H i i = 0)
    (hward : H + genericDeltaCellHessian L c =
      secondOrderCongruenceCoefficient (genericDeltaCartanTangent L) K) :
    K 1 1 + K 1 1 = (L : ℚ) ^ 2 / 2 ∧
      K 0 0 + K 0 0 = -2 * c * (L : ℚ) ^ 2 ∧
      K 2 2 + K 2 2 = (L : ℚ) ^ 2 / 2 - 2 * c * (L : ℚ) ^ 2 ∧
      K 1 2 + K 2 1 = -(L : ℚ) ^ 2 / 2 - H 1 2 := by
  have hsym := genericDelta_secondJet_symmetric_part L c H K hdiag hward
  have h11 := congrFun (congrFun hsym 1) 1
  have h00 := congrFun (congrFun hsym 0) 0
  have h22 := congrFun (congrFun hsym 2) 2
  have h12 := congrFun (congrFun hsym 1) 2
  simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply] at h11 h00 h22 h12
  rw [hdiag 1] at h11
  rw [hdiag 0] at h00
  rw [hdiag 2] at h22
  simp [genericDeltaGram, genericDeltaCellHessian, genericDeltaGaugeVector,
    Matrix.diagonal] at h11 h00 h22 h12
  constructor
  · nlinarith [h11]
  constructor
  · nlinarith [h00]
  constructor
  · nlinarith [h22]
  · nlinarith [h12]

/-- Under the explicit finite-parameter constant-preservation condition
`K 1 = 0`, the scalar diagonal ansatz `c M_(h²)` can satisfy the symmetric
Ward block only when `c=0`. The input zero-sum condition is the first-jet
constant contraction; this theorem makes no claim that `c=0` is a physical
action. -/
theorem genericDelta_constant_preservation_forces_zero_coefficient
    (L : ℕ) (hL : 3 ≤ L) (c : ℚ) (K : GenericDeltaBlock)
    (hKrows : ∀ i, ∑ j : Fin 3, K i j = 0)
    (hward : (-(genericDeltaCartanTangent L +
          (genericDeltaCartanTangent L).transpose)) +
        genericDeltaCellHessian L c =
      secondOrderCongruenceCoefficient (genericDeltaCartanTangent L) K) : c = 0 := by
  let H : GenericDeltaBlock :=
    -(genericDeltaCartanTangent L + (genericDeltaCartanTangent L).transpose)
  have hsym := genericDelta_secondJet_symmetric_part L c H K
    (by intro i; fin_cases i <;> norm_num [H, genericDeltaCartanTangent,
      Matrix.add_apply, Matrix.neg_apply, Matrix.transpose_apply])
    hward
  have hsumK : (∑ i : Fin 3, ∑ j : Fin 3, K i j) = 0 := by
    simp [hKrows]
  have hsumKt : (∑ i : Fin 3, ∑ j : Fin 3, K j i) = 0 := by
    calc
      _ = ∑ j : Fin 3, ∑ i : Fin 3, K j i := Finset.sum_comm
      _ = 0 := by simp [hKrows]
  have hsumSym : (∑ i : Fin 3, ∑ j : Fin 3,
      (K.transpose + K) i j) = 0 := by
    simp only [Matrix.add_apply, Matrix.transpose_apply]
    simp [Finset.sum_add_distrib, hsumKt, hsumK]
  have hsumGram : (∑ i : Fin 3, ∑ j : Fin 3,
      genericDeltaGram L i j) = 0 := by
    norm_num [genericDeltaGram, Fin.sum_univ_succ] <;> ring
  have hsumH : (∑ i : Fin 3, ∑ j : Fin 3,
      (-(genericDeltaCartanTangent L +
        (genericDeltaCartanTangent L).transpose)) i j) = 0 := by
    norm_num [genericDeltaCartanTangent, Matrix.add_apply,
      Matrix.neg_apply, Matrix.transpose_apply, Fin.sum_univ_succ] <;> ring
  have hsumCell : (∑ i : Fin 3, ∑ j : Fin 3,
      genericDeltaCellHessian L c i j) = 4 * c * (L : ℚ) ^ 2 := by
    norm_num [genericDeltaCellHessian, genericDeltaGaugeVector,
      Matrix.diagonal, Fin.sum_univ_succ] <;> ring
  have hsumRhs : (∑ i : Fin 3, ∑ j : Fin 3,
      ((2 : ℚ) • genericDeltaGram L -
        H - genericDeltaCellHessian L c) i j) = 0 := by
    calc
      _ = ∑ i : Fin 3, ∑ j : Fin 3, (K.transpose + K) i j := by
        apply Finset.sum_congr rfl
        intro i hi
        apply Finset.sum_congr rfl
        intro j hj
        exact (congrFun (congrFun hsym i) j).symm
      _ = 0 := hsumSym
  have hsumLinear :
      (∑ i : Fin 3, ∑ j : Fin 3, (2 : ℚ) • genericDeltaGram L i j) -
        (∑ i : Fin 3, ∑ j : Fin 3, H i j) -
        (∑ i : Fin 3, ∑ j : Fin 3, genericDeltaCellHessian L c i j) = 0 := by
    simpa only [Matrix.sub_apply, Matrix.smul_apply,
      Finset.sum_sub_distrib] using hsumRhs
  have hsumScale : (∑ i : Fin 3, ∑ j : Fin 3,
      (2 : ℚ) • genericDeltaGram L i j) = 0 := by
    simp only [smul_eq_mul]
    simp_rw [← Finset.mul_sum]
    rw [hsumGram]
    norm_num
  rw [hsumScale, hsumH, hsumCell] at hsumLinear
  have hLq : (3 : ℚ) ≤ L := by exact_mod_cast hL
  have hprod : c * (L : ℚ) ^ 2 = 0 := by nlinarith [hsumLinear]
  rcases mul_eq_zero.mp hprod with hc | hLsq
  · exact hc
  · have hLne : (L : ℚ) ≠ 0 := by
      exact ne_of_gt (lt_of_lt_of_le (by norm_num) hLq)
    exact False.elim ((pow_ne_zero 2 hLne) hLsq)

end D0.Geometry
