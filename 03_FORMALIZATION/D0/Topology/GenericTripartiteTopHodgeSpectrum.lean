import D0.Topology.GenericTripartiteChainRetraction
import D0.VNext2.SceneSpectralFingerprint
import D0.Representation.TypedRepresentationFunctor
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-TOP-HODGE-SPECTRUM-001

For `K(p+1,q+1,r+1)`, the natural upper Hodge Laplacian on triangles
`Δ₂ = ∂₂ᵀ∂₂` has a complete tensor eigenbasis.  Before accidental eigenvalue
collisions, its eight sectors are

```
0                               multiplicity p*q*r
p+1                             multiplicity q*r
q+1                             multiplicity p*r
r+1                             multiplicity p*q
p+q+2                           multiplicity r
p+r+2                           multiplicity q
q+r+2                           multiplicity p
p+q+r+3                         multiplicity 1.
```

For the source scene the spectrum is
`0^960, 9^120, 11^96, 13^80, 20^12, 22^10, 24^8, 33^1`.
The harmonic sector is exactly `ker ∂₂`; the one-difference sectors recover
the owned archive fingerprint `20^12,22^10,24^8`.

Scope: this is the natural top-chain Hodge operator.  It is not asserted to be
a physical Hamiltonian, mass operator, or continuum Hodge realization.
-/

namespace D0.Topology.GenericTripartiteTopHodgeSpectrum
open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

variable {p q r : ℕ}
local notation "A" => Fin (p+1)
local notation "B" => Fin (q+1)
local notation "C" => Fin (r+1)
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

private lemma sum_indicator_one
    {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, (if x=a then (1:ℚ) else 0) * f x) = f a := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact Fintype.sum_ite_eq' a f

private lemma sum_indicator_pair_one
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → ℚ) (a : α) (b : β) :
    (∑ x : α × β,
      (if x.1=a ∧ x.2=b then (1:ℚ) else 0) * f x) = f (a,b) := by
  rw [Fintype.sum_prod_type]
  calc
    _ = ∑ x : α, if x=a then f (x,b) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx:x=a
      · subst x
        simpa using Fintype.sum_ite_eq' b (fun y:β => f (a,y))
      · simp [hx]
    _ = _ := by simpa using Fintype.sum_ite_eq' a (fun x:α => f (x,b))

private lemma sum_indicator_pair_neg
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → ℚ) (a : α) (b : β) :
    (∑ x : α × β,
      (if x.1=a ∧ x.2=b then (-1:ℚ) else 0) * f x) = -f (a,b) := by
  calc
    _ = -(∑ x : α × β,
      (if x.1=a ∧ x.2=b then (1:ℚ) else 0) * f x) := by
      rw [← Finset.sum_neg_distrib]
      apply Fintype.sum_congr
      intro x
      by_cases h:x.1=a ∧ x.2=b <;> simp [h]
    _ = _ := by rw [sum_indicator_pair_one]

/-- Constant mode followed by the `n` root-difference modes. -/
def factorMode {n : ℕ} (i : Fin (n+1)) : Fin (n+1) → ℚ :=
  Fin.cases (fun _ => 1) (fun j => rootDifferenceR ℚ j) i

/-- Dual weight extracting a coefficient in the factor-mode basis. -/
def factorDualWeight {n : ℕ} (i x : Fin (n+1)) : ℚ :=
  Fin.cases
    ((n+1 : ℚ)⁻¹)
    (fun j => (if x=j.succ then 1 else 0) - (n+1 : ℚ)⁻¹)
    i

lemma factorMode_sum {n : ℕ} (i : Fin (n+1)) :
    ∑ x : Fin (n+1), factorMode i x =
      Fin.cases (n+1 : ℚ) (fun _ => 0) i := by
  refine Fin.cases ?_ (fun j => ?_) i
  · simp [factorMode]
  · simp [factorMode, rootDifferenceR_sum]

lemma factorDual_pairing {n : ℕ} (i j : Fin (n+1)) :
    (∑ x : Fin (n+1), factorDualWeight i x * factorMode j x) =
      if i=j then 1 else 0 := by
  refine Fin.cases ?_ (fun ii => ?_) i
  · refine Fin.cases ?_ (fun jj => ?_) j
    · simp [factorDualWeight, factorMode]
      have hn : (n+1:ℚ) ≠ 0 := by positivity
      field_simp
    · change (∑ x : Fin (n+1), (n+1:ℚ)⁻¹ * rootDifferenceR ℚ jj x) = 0
      rw [← Finset.mul_sum, rootDifferenceR_sum]
      simp
  · refine Fin.cases ?_ (fun jj => ?_) j
    · change (∑ x : Fin (n+1),
          ((if x=ii.succ then (1:ℚ) else 0) - (n+1:ℚ)⁻¹) * 1) = 0
      simp only [mul_one, Finset.sum_sub_distrib]
      rw [show (∑ x : Fin (n+1), if x=ii.succ then (1:ℚ) else 0) = 1 by
        simpa using Fintype.sum_ite_eq' ii.succ (fun _ : Fin (n+1) => (1:ℚ))]
      rw [Finset.sum_const, nsmul_eq_mul]
      simp only [Finset.card_univ, Fintype.card_fin]
      have hn : (n+1:ℚ) ≠ 0 := by positivity
      field_simp
      norm_num
    · change (∑ x : Fin (n+1),
        ((if x=ii.succ then (1:ℚ) else 0) - (n+1:ℚ)⁻¹) *
          rootDifferenceR ℚ jj x) = if ii.succ=jj.succ then 1 else 0
      calc
        _ =
            (∑ x : Fin (n+1),
              (if x=ii.succ then (1:ℚ) else 0) *
                rootDifferenceR ℚ jj x) -
              (n+1:ℚ)⁻¹ *
                (∑ x : Fin (n+1), rootDifferenceR ℚ jj x) := by
              simp_rw [sub_mul]
              rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
        _ = _ := by
          rw [sum_indicator_one, rootDifferenceR_sum]
          simp [rootDifferenceR_succ, Fin.succ_inj]

abbrev HodgeModeIndex (p q r : ℕ) := GenericTriangle p q r

def triangleMode (i : HodgeModeIndex p q r) : Triangle → ℚ
  | (a,b,c) => factorMode i.1 a * factorMode i.2.1 b * factorMode i.2.2 c

def triangleDualWeight (i : HodgeModeIndex p q r) : Triangle → ℚ
  | (a,b,c) =>
      factorDualWeight i.1 a * factorDualWeight i.2.1 b * factorDualWeight i.2.2 c

def triangleModeCoordinate (i : HodgeModeIndex p q r) :
    (Triangle → ℚ) →ₗ[ℚ] ℚ :=
  Fintype.linearCombination ℚ (triangleDualWeight i)

private lemma pair_product_sum
    {α β : Type} [Fintype α] [Fintype β]
    (fa ga : α → ℚ) (fb gb : β → ℚ) :
    (∑ x : α × β, (fa x.1 * fb x.2) * (ga x.1 * gb x.2)) =
      (∑ a : α, fa a * ga a) * (∑ b : β, fb b * gb b) := by
  rw [Fintype.sum_prod_type]
  calc
    _ = ∑ a : α, (fa a * ga a) * (∑ b : β, fb b * gb b) := by
      apply Fintype.sum_congr
      intro a
      rw [Finset.mul_sum]
      apply Fintype.sum_congr
      intro b
      ring
    _ = _ := by rw [Finset.sum_mul]

private lemma triple_separable
    (fa ga : A → ℚ) (fb gb : B → ℚ) (fc gc : C → ℚ) :
    (∑ x : Triangle,
      (fa x.1 * fb x.2.1 * fc x.2.2) *
        (ga x.1 * gb x.2.1 * gc x.2.2)) =
      (∑ a:A, fa a * ga a) *
        (∑ b:B, fb b * gb b) *
        (∑ c:C, fc c * gc c) := by
  rw [Fintype.sum_prod_type]
  calc
    _ = ∑ a:A, (fa a * ga a) *
        (∑ bc:B×C, (fb bc.1 * fc bc.2) * (gb bc.1 * gc bc.2)) := by
      apply Fintype.sum_congr
      intro a
      rw [Finset.mul_sum]
      apply Fintype.sum_congr
      intro bc
      ring
    _ = (∑ a:A, fa a * ga a) *
        (∑ bc:B×C, (fb bc.1 * fc bc.2) * (gb bc.1 * gc bc.2)) := by
      rw [Finset.sum_mul]
    _ = _ := by
      rw [pair_product_sum]
      ac_rfl

lemma triangleModeCoordinate_pairing
    (i j : HodgeModeIndex p q r) :
    triangleModeCoordinate i (triangleMode j) = if i=j then 1 else 0 := by
  unfold triangleModeCoordinate
  rw [Fintype.linearCombination_apply]
  simp only [smul_eq_mul, triangleDualWeight, triangleMode]
  rw [show (∑ x : Triangle,
      (factorMode j.1 x.1 * factorMode j.2.1 x.2.1 * factorMode j.2.2 x.2.2) *
        (factorDualWeight i.1 x.1 * factorDualWeight i.2.1 x.2.1 *
          factorDualWeight i.2.2 x.2.2)) =
      (∑ a:A, factorDualWeight i.1 a * factorMode j.1 a) *
      (∑ b:B, factorDualWeight i.2.1 b * factorMode j.2.1 b) *
      (∑ c:C, factorDualWeight i.2.2 c * factorMode j.2.2 c) by
        simpa [mul_comm, mul_left_comm, mul_assoc] using
          triple_separable
            (fa:=factorDualWeight i.1) (ga:=factorMode j.1)
            (fb:=factorDualWeight i.2.1) (gb:=factorMode j.2.1)
            (fc:=factorDualWeight i.2.2) (gc:=factorMode j.2.2)]
  rw [factorDual_pairing, factorDual_pairing, factorDual_pairing]
  by_cases h1:i.1=j.1
  · by_cases h2:i.2.1=j.2.1
    · by_cases h3:i.2.2=j.2.2
      · have h:i=j := by rcases i with ⟨ia,ib,ic⟩; rcases j with ⟨ja,jb,jc⟩; simp_all
        simp [h,h1,h2,h3]
      · have h:i≠j := by intro hij; exact h3 (congrArg (fun x=>x.2.2) hij)
        simp [h,h1,h2,h3]
    · have h:i≠j := by intro hij; exact h2 (congrArg (fun x=>x.2.1) hij)
      simp [h,h1,h2]
  · have h:i≠j := by intro hij; exact h1 (congrArg (fun x=>x.1) hij)
    simp [h,h1]

lemma triangleMode_linearIndependent :
    LinearIndependent ℚ (triangleMode : HodgeModeIndex p q r → Triangle → ℚ) := by
  rw [Fintype.linearIndependent_iff]
  intro g h i
  have hc := congrArg (triangleModeCoordinate i) h
  simp only [map_sum, map_smul, map_zero, triangleModeCoordinate_pairing,
    smul_eq_mul] at hc
  rw [show (∑ j, g j * if i=j then 1 else 0) = g i by simp] at hc
  exact hc

private theorem hodgeModeIndex_card :
    Fintype.card (HodgeModeIndex p q r) = Module.finrank ℚ (Triangle → ℚ) := by
  rw [Module.finrank_fintype_fun_eq_card]

noncomputable def triangleModeBasis :
    Module.Basis (HodgeModeIndex p q r) ℚ (Triangle → ℚ) :=
  basisOfLinearIndependentOfCardEqFinrank'
    triangleMode triangleMode_linearIndependent hodgeModeIndex_card

@[simp] lemma triangleModeBasis_apply (i : HodgeModeIndex p q r) :
    triangleModeBasis i = triangleMode i := by simp [triangleModeBasis]

lemma boundary2R_transpose_mulVec (y : Edge → ℚ) (a:A) (b:B) (c:C) :
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose.mulVec y (a,b,c) =
      y (Sum.inl (a,b)) - y (Sum.inr (Sum.inl (a,c))) +
        y (Sum.inr (Sum.inr (b,c))) := by
  simp only [Matrix.mulVec, dotProduct, transpose_apply, boundary2R,
    Fintype.sum_sum_type]
  rw [sum_indicator_pair_one, sum_indicator_pair_neg, sum_indicator_pair_one]
  ring

def topHodgeLaplacian : Matrix Triangle Triangle ℚ :=
  (boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose *
    boundary2R ℚ (p:=p) (q:=q) (r:=r)

lemma topHodgeLaplacian_mulVec (x : Triangle → ℚ) (a:A) (b:B) (c:C) :
    (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVec x (a,b,c) =
      (∑ a':A, x (a',b,c)) + (∑ b':B, x (a,b',c)) +
        ∑ c':C, x (a,b,c') := by
  unfold topHodgeLaplacian
  rw [← Matrix.mulVec_mulVec, boundary2R_transpose_mulVec,
    boundary2R_mulVec_ab, boundary2R_mulVec_ac, boundary2R_mulVec_bc]
  ring

def factorEigenvalue {n : ℕ} (i : Fin (n+1)) : ℚ :=
  Fin.cases (n+1 : ℚ) (fun _ => 0) i

lemma factorMode_sum_eigen (i : Fin (p+1)) (a:A) :
    (∑ x:A, factorMode i x) = factorEigenvalue i * factorMode i a := by
  refine Fin.cases ?_ (fun j=>?_) i
  · simp [factorMode, factorEigenvalue]
  · simp [factorMode, factorEigenvalue, rootDifferenceR_sum]

def triangleModeEigenvalue (i : HodgeModeIndex p q r) : ℚ :=
  factorEigenvalue i.1 + factorEigenvalue i.2.1 + factorEigenvalue i.2.2

lemma topHodge_triangleMode (i : HodgeModeIndex p q r) :
    (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVec (triangleMode i) =
      triangleModeEigenvalue i • triangleMode i := by
  funext t
  rcases t with ⟨a,b,c⟩
  rw [topHodgeLaplacian_mulVec]
  simp only [triangleMode, Pi.smul_apply, smul_eq_mul, triangleModeEigenvalue]
  rw [show (∑ a':A, factorMode i.1 a' * factorMode i.2.1 b * factorMode i.2.2 c) =
      (∑ a':A, factorMode i.1 a') * factorMode i.2.1 b * factorMode i.2.2 c by
        rw [Finset.sum_mul, Finset.sum_mul]]
  rw [show (∑ b':B, factorMode i.1 a * factorMode i.2.1 b' * factorMode i.2.2 c) =
      factorMode i.1 a * (∑ b':B, factorMode i.2.1 b') * factorMode i.2.2 c by
        rw [Finset.mul_sum, Finset.sum_mul]]
  rw [show (∑ c':C, factorMode i.1 a * factorMode i.2.1 b * factorMode i.2.2 c') =
      factorMode i.1 a * factorMode i.2.1 b * (∑ c':C, factorMode i.2.2 c') by
        rw [Finset.mul_sum]]
  rw [factorMode_sum_eigen (p:=p) i.1 a,
    factorMode_sum_eigen (p:=q) i.2.1 b,
    factorMode_sum_eigen (p:=r) i.2.2 c]
  ring

/-- The displayed eigenvectors are a complete eigenbasis, not merely a family
of examples. -/
theorem topHodge_triangleModeBasis (i : HodgeModeIndex p q r) :
    (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVec
        (triangleModeBasis i) =
      triangleModeEigenvalue i • triangleModeBasis i := by
  rw [triangleModeBasis_apply]
  exact topHodge_triangleMode i


/-- Multiplicity of a basis eigenvalue in the complete tensor eigenbasis. -/
def modeMultiplicity (p q r : ℕ) (lam : ℚ) : ℕ :=
  (Finset.univ.filter
    (fun i : HodgeModeIndex p q r => triangleModeEigenvalue i = lam)).card

/-- The eight tensor sectors before merging accidental eigenvalue collisions. -/
def genericTopHodgeSectorData (p q r : ℕ) : List (ℚ × ℕ) :=
  [(0, p*q*r),
   (p+1, q*r),
   (q+1, p*r),
   (r+1, p*q),
   (p+q+2, r),
   (p+r+2, q),
   (q+r+2, p),
   (p+q+r+3, 1)]

/-- Generic multiplicity and trace passport for the eight tensor sectors. -/
theorem generic_top_hodge_sector_consistency :
    (genericTopHodgeSectorData p q r |>.map Prod.snd).sum =
        (p+1) * (q+1) * (r+1) ∧
      (genericTopHodgeSectorData p q r |>.map
        (fun x => x.1 * (x.2 : ℚ))).sum =
        3 * ((p+1) * (q+1) * (r+1) : ℕ) := by
  constructor
  · simp [genericTopHodgeSectorData]
    ring
  · simp [genericTopHodgeSectorData]
    push_cast
    ring

/-- The source-scene top-Hodge spectrum in increasing eigenvalue order. -/
def sceneTopHodgeSpectrum : List (ℚ × ℕ) :=
  [(0,960), (9,120), (11,96), (13,80),
   (20,12), (22,10), (24,8), (33,1)]

/-- Every scene tensor-basis eigenvalue belongs to the displayed list. -/
theorem scene_top_hodge_eigenvalues_exhaustive :
    ∀ i : HodgeModeIndex 8 10 12,
      triangleModeEigenvalue i ∈ [0,9,11,13,20,22,24,33] := by
  native_decide

/-- Exact multiplicities of all eight distinct source-scene eigenvalues. -/
theorem scene_top_hodge_multiplicities :
    modeMultiplicity 8 10 12 0 = 960 ∧
    modeMultiplicity 8 10 12 9 = 120 ∧
    modeMultiplicity 8 10 12 11 = 96 ∧
    modeMultiplicity 8 10 12 13 = 80 ∧
    modeMultiplicity 8 10 12 20 = 12 ∧
    modeMultiplicity 8 10 12 22 = 10 ∧
    modeMultiplicity 8 10 12 24 = 8 ∧
    modeMultiplicity 8 10 12 33 = 1 := by
  native_decide

/-- Multiplicity and trace checks: `1287` triangle modes and trace `3*1287`. -/
theorem scene_top_hodge_consistency :
    (sceneTopHodgeSpectrum.map Prod.snd).sum = 1287 ∧
      (sceneTopHodgeSpectrum.map
        (fun x => x.1 * (x.2 : ℚ))).sum = 3861 := by
  norm_num [sceneTopHodgeSpectrum]

/-- The top-Hodge spectral gap is `9`; all positive eigenvalues lie in
`[9,33]`. -/
theorem scene_top_hodge_positive_bounds :
    ∀ x ∈ sceneTopHodgeSpectrum,
      x.1 ≠ 0 → (9 : ℚ) ≤ x.1 ∧ x.1 ≤ 33 := by
  native_decide

/-- Ratio of largest to smallest positive top-Hodge eigenvalue. -/
theorem scene_top_hodge_condition_ratio :
    (33 : ℚ) / 9 = 11 / 3 := by
  norm_num

/-- The three high non-top sectors recover the graph degree eigenvalues and
within-part multiplicities. -/
theorem scene_top_hodge_degree_sectors :
    modeMultiplicity 8 10 12 24 = 8 ∧
      modeMultiplicity 8 10 12 22 = 10 ∧
      modeMultiplicity 8 10 12 20 = 12 := by
  native_decide

/-- The zero top-Hodge sector is exactly the `960`-dimensional top homology. -/
theorem scene_top_hodge_zero_sector_eq_beta2 :
    modeMultiplicity 8 10 12 0 = 960 :=
  scene_top_hodge_multiplicities.1

/-- The harmonic top forms are exactly the top cycles. -/
theorem topHodge_kernel_eq_topKernel :
    LinearMap.ker
        (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVecLin =
      LinearMap.ker
        (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVecLin := by
  unfold topHodgeLaplacian
  exact Matrix.ker_mulVecLin_transpose_mul_self _

/-- The single-difference sectors reproduce the three owned zone degrees. -/
theorem scene_top_hodge_single_difference_frame :
    (∀ i : Fin 8,
      triangleModeEigenvalue (p:=8) (q:=10) (r:=12)
        (i.succ, 0, 0) = 24) ∧
    (∀ j : Fin 10,
      triangleModeEigenvalue (p:=8) (q:=10) (r:=12)
        (0, j.succ, 0) = 22) ∧
    (∀ k : Fin 12,
      triangleModeEigenvalue (p:=8) (q:=10) (r:=12)
        (0, 0, k.succ) = 20) := by
  constructor
  · intro i
    norm_num [triangleModeEigenvalue, factorEigenvalue]
  constructor
  · intro j
    norm_num [triangleModeEigenvalue, factorEigenvalue]
  · intro k
    norm_num [triangleModeEigenvalue, factorEigenvalue]

/-- Exact overlap with the owned graph-Laplacian archive sectors.  The `33`
sector is deliberately excluded: it has multiplicity `1` on top chains but
`2` on vertex chains. -/
theorem scene_top_hodge_matches_graph_archive :
    sceneTopHodgeSpectrum.filter
        (fun x => x.1 = 20 ∨ x.1 = 22 ∨ x.1 = 24) =
      [(20,12), (22,10), (24,8)] ∧
    D0.VNext2.SceneSpectralFingerprint.laplacianSpectrum.filter
        (fun x => x.1 = 20 ∨ x.1 = 22 ∨ x.1 = 24) =
      [(20,12), (22,10), (24,8)] := by
  native_decide

/-- The already-owned typed degree frame is the same ordered triple extracted
from the one-difference top-Hodge sectors. -/
theorem scene_top_hodge_recovers_typed_degree_frame :
    (24, 22, 20) =
      (D0.Representation.TypedRepresentationFunctor.zoneDegree 0,
       D0.Representation.TypedRepresentationFunctor.zoneDegree 1,
       D0.Representation.TypedRepresentationFunctor.zoneDegree 2) := by
  decide

end D0.Topology.GenericTripartiteTopHodgeSpectrum
