import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Tactic

/-! # Fixed-rank affine exterior-compound quotient

The coordinate `Psi_r(M,t)` records the translation class in
`V / range M` on the rank-`r` stratum. It is a kinematic resolution
coordinate only and does not define or select an action channel.
-/

namespace D0.Geometry.A4DRankCompoundAffineQuotient

noncomputable section
open Set
open Set.powersetCard

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- Exterior multiplication on the left by a vector. -/
def wedgeLeft (r : ℕ) (t : V) : (⋀[ℝ]^r V) →ₗ[ℝ] ⋀[ℝ]^(r + 1) V :=
  exteriorPower.alternatingMapLinearEquiv
    ((exteriorPower.ιMulti ℝ (r + 1)).curryLeft t)

@[simp] theorem wedgeLeft_apply_ιMulti (r : ℕ) (t : V) (v : Fin r → V) :
    wedgeLeft r t (exteriorPower.ιMulti ℝ r v) =
      exteriorPower.ιMulti ℝ (r + 1) (Matrix.vecCons t v) := by
  simp [wedgeLeft]

/-- The fixed-rank affine compound coordinate `Psi_r(M,t) = t ∧ Λ^r M`. -/
def psi (r : ℕ) (M : V →ₗ[ℝ] V) (t : V) :
    (⋀[ℝ]^r V) →ₗ[ℝ] ⋀[ℝ]^(r + 1) V :=
  (wedgeLeft r t).comp (exteriorPower.map r M)

/-- A linearly independent family has nonzero top exterior product. -/
theorem ιMulti_ne_zero_of_linearIndependent {n : ℕ} {v : Fin n → V}
    (hv : LinearIndependent ℝ v) : exteriorPower.ιMulti ℝ n v ≠ 0 := by
  let W : Submodule ℝ V := Submodule.span ℝ (Set.range v)
  let b : Module.Basis (Fin n) ℝ W := Module.Basis.span hv
  let e : Fin n ↪o Fin n := OrderEmbedding.id (Fin n)
  let s : powersetCard (Fin n) n := ofFinEmbEquiv e
  have hs : ofFinEmbEquiv.symm s = e := by simp [s]
  have hb : exteriorPower.ιMulti_family ℝ n b s ≠ 0 := by
    have hli := exteriorPower.ιMulti_family_linearIndependent_ofBasis (R := ℝ) (n := n) b
    exact hli.ne_zero s
  have hfamily : exteriorPower.ιMulti_family ℝ n b s = exteriorPower.ιMulti ℝ n b := by
    simp only [exteriorPower.ιMulti_family]
    rw [hs]
    rfl
  have hb' : exteriorPower.ιMulti ℝ n b ≠ 0 := by
    rw [← hfamily]
    exact hb
  have hmap : exteriorPower.map n W.subtype (exteriorPower.ιMulti ℝ n b) =
      exteriorPower.ιMulti ℝ n v := by
    rw [exteriorPower.map_apply_ιMulti]
    congr 1
    funext i
    exact Module.Basis.coe_span_apply hv i
  intro hz
  apply hb'
  apply (exteriorPower.map_injective_field (Submodule.subtype_injective W))
  simpa [hmap] using hz

/-- Naturality, including maps between distinct vector spaces. -/
theorem wedgeLeft_map_naturality {W : Type*} [AddCommGroup W] [Module ℝ W]
    (r : ℕ) (L : W →ₗ[ℝ] V) (t : W) :
    (wedgeLeft r (L t)).comp (exteriorPower.map r L) =
      (exteriorPower.map (r + 1) L).comp (wedgeLeft r t) := by
  apply LinearMap.ext_on (exteriorPower.ιMulti_span ℝ r (M := W))
  rintro _ ⟨v, rfl⟩
  simp only [LinearMap.comp_apply, exteriorPower.map_apply_ιMulti,
    wedgeLeft_apply_ιMulti, Function.comp_def]
  congr 1
  funext i
  exact Fin.cases rfl (fun _ => rfl) i

/-- Naturality of the compound coordinate under any invertible linear frame
change. In particular it applies to every Lorentz transformation. -/
theorem psi_linearEquiv_covariant (r : ℕ) (M : V →ₗ[ℝ] V)
    (g : V ≃ₗ[ℝ] V) (t : V) :
    psi r (g.toLinearMap.comp (M.comp g.symm.toLinearMap)) (g t) =
      (exteriorPower.map (r + 1) g.toLinearMap).comp
        ((psi r M t).comp (exteriorPower.map r g.symm.toLinearMap)) := by
  apply LinearMap.ext_on (exteriorPower.ιMulti_span ℝ r (M := V))
  rintro _ ⟨v, rfl⟩
  have hnat := wedgeLeft_map_naturality (V := V) (W := V) r g.toLinearMap t
  simpa [psi, LinearMap.comp_apply, exteriorPower.map_comp,
    exteriorPower.map_apply_ιMulti] using
      congrArg (fun F => F (exteriorPower.map r (M.comp g.symm.toLinearMap)
        (exteriorPower.ιMulti ℝ r v))) hnat

/-- `Psi` is linear in its affine translation input. -/
theorem psi_add (r : ℕ) (M : V →ₗ[ℝ] V) (t u : V) :
    psi r M (t + u) = psi r M t + psi r M u := by
  ext z
  simp [psi, wedgeLeft]

/-- A shift in the image is killed whenever the next exterior compound
vanishes. -/
theorem psi_eq_zero_of_map_succ_eq_zero (r : ℕ) (M : V →ₗ[ℝ] V)
    (hnext : exteriorPower.map (r + 1) M = 0) (c : V) :
    psi r M (M c) = 0 := by
  change (wedgeLeft r (M c)).comp (exteriorPower.map r M) = 0
  calc
    (wedgeLeft r (M c)).comp (exteriorPower.map r M) =
        (exteriorPower.map (r + 1) M).comp (wedgeLeft r c) :=
          wedgeLeft_map_naturality (V := V) (W := V) r M c
    _ = 0 := by rw [hnext]; simp

/-- Degree `r+1` compounds vanish when the image of `M` has dimension `r`. -/
theorem map_succ_eq_zero_of_finrank_range_eq [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V)
    (hr : Module.finrank ℝ M.range = r) : exteriorPower.map (r + 1) M = 0 := by
  let W : Submodule ℝ V := M.range
  have hdim : Module.finrank ℝ (⋀[ℝ]^(r + 1) W) = 0 := by
    rw [exteriorPower.finrank_eq]
    simp [W, hr]
  have hsub : Subsingleton (⋀[ℝ]^(r + 1) W) := Module.finrank_zero_iff.mp hdim
  have hzero : exteriorPower.map (r + 1) M.rangeRestrict = 0 := by
    apply LinearMap.ext
    intro z
    exact hsub.elim _ _
  have hfac : M = W.subtype.comp M.rangeRestrict := by
    ext x
    rfl
  rw [hfac, exteriorPower.map_comp, hzero]
  simp

/-- The degree-`r` compound vanishes below rank `r`. -/
theorem map_eq_zero_of_finrank_range_lt [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V)
  (hlt : Module.finrank ℝ M.range < r) : exteriorPower.map r M = 0 := by
  let W : Submodule ℝ V := M.range
  have hdim : Module.finrank ℝ (⋀[ℝ]^r W) = 0 := by
    rw [exteriorPower.finrank_eq]
    exact Nat.choose_eq_zero_of_lt (by simpa [W] using hlt)
  have hsub : Subsingleton (⋀[ℝ]^r W) := Module.finrank_zero_iff.mp hdim
  have hzero : exteriorPower.map r M.rangeRestrict = 0 := by
    apply LinearMap.ext
    intro z
    exact hsub.elim _ _
  have hfac : M = W.subtype.comp M.rangeRestrict := by
    ext x
    rfl
  rw [hfac, exteriorPower.map_comp, hzero]
  simp

/-- Below the selected rank, `Psi` collapses to zero and carries no quotient
information. -/
theorem psi_eq_zero_of_finrank_range_lt [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V)
    (hlt : Module.finrank ℝ M.range < r) (t : V) : psi r M t = 0 := by
  rw [psi, map_eq_zero_of_finrank_range_lt r M hlt]
  simp

/-- Full affine covariance under an invertible linear frame change. For a
Lorentz transformation this is the requested Lorentz covariance. The added
`M' c` term is only invisible on the fixed-rank stratum. -/
theorem psi_affine_linearEquiv_covariant [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r)
    (g : V ≃ₗ[ℝ] V) (t c : V) :
    let M' := g.toLinearMap.comp (M.comp g.symm.toLinearMap)
    psi r M' (g t + M' c) =
      (exteriorPower.map (r + 1) g.toLinearMap).comp
        ((psi r M t).comp (exteriorPower.map r g.symm.toLinearMap)) := by
  dsimp only
  let M' : V →ₗ[ℝ] V := g.toLinearMap.comp (M.comp g.symm.toLinearMap)
  have hnext : exteriorPower.map (r + 1) M' = 0 := by
    calc
      exteriorPower.map (r + 1) M' =
          (exteriorPower.map (r + 1) g.toLinearMap).comp
            ((exteriorPower.map (r + 1) M).comp
              (exteriorPower.map (r + 1) g.symm.toLinearMap)) := by
                dsimp [M']
                rw [exteriorPower.map_comp, exteriorPower.map_comp]
      _ = 0 := by
        rw [map_succ_eq_zero_of_finrank_range_eq r M hr]
        simp
  calc
    psi r M' (g t + M' c) = psi r M' (g t) + psi r M' (M' c) :=
      psi_add r M' (g t) (M' c)
    _ = psi r M' (g t) := by
      rw [psi_eq_zero_of_map_succ_eq_zero r M' hnext c]
      simp
    _ = (exteriorPower.map (r + 1) g.toLinearMap).comp
          ((psi r M t).comp (exteriorPower.map r g.symm.toLinearMap)) :=
      psi_linearEquiv_covariant r M g t

/-- Fixed-rank `Psi` is zero on translations in the image. -/
theorem psi_eq_zero_of_mem_range [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r)
    {t : V} (ht : t ∈ M.range) : psi r M t = 0 := by
  change (wedgeLeft r t).comp (exteriorPower.map r M) = 0
  let W : Submodule ℝ V := M.range
  let tW : W := ⟨t, ht⟩
  have hdim : Module.finrank ℝ (⋀[ℝ]^(r + 1) W) = 0 := by
    rw [exteriorPower.finrank_eq]
    simp [W, hr]
  have hsub : Subsingleton (⋀[ℝ]^(r + 1) W) := Module.finrank_zero_iff.mp hdim
  have hfac : M = W.subtype.comp M.rangeRestrict := by
    ext x
    rfl
  have hmapfac : exteriorPower.map r M =
      (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) := by
    calc
      exteriorPower.map r M = exteriorPower.map r (W.subtype.comp M.rangeRestrict) :=
        congrArg (exteriorPower.map r) hfac
      _ = (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) :=
        exteriorPower.map_comp _ _
  have hw : wedgeLeft r tW = 0 := by
    apply LinearMap.ext
    intro z
    exact hsub.elim _ _
  calc
    (wedgeLeft r t).comp (exteriorPower.map r M) =
        (wedgeLeft r t).comp ((exteriorPower.map r W.subtype).comp
          (exteriorPower.map r M.rangeRestrict)) := by rw [hmapfac]
    _ = ((exteriorPower.map (r + 1) W.subtype).comp (wedgeLeft r tW)).comp
          (exteriorPower.map r M.rangeRestrict) := by
          rw [← show W.subtype tW = t by rfl]
          exact congrArg (fun F => F.comp (exteriorPower.map r M.rangeRestrict))
            (wedgeLeft_map_naturality (V := V) (W := W) r W.subtype tW)
    _ = 0 := by rw [hw]; simp

/-- The compound coordinate is nonzero for every translation outside the image. -/
theorem psi_ne_zero_of_not_mem_range [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r)
    {t : V} (ht : t ∉ M.range) : psi r M t ≠ 0 := by
  change (wedgeLeft r t).comp (exteriorPower.map r M) ≠ 0
  let W : Submodule ℝ V := M.range
  let b : Module.Basis (Fin r) ℝ W := Module.finBasisOfFinrankEq ℝ W hr
  let bV : Fin r → V := fun i => W.subtype (b i)
  have hLIbV : LinearIndependent ℝ bV :=
    b.linearIndependent.map' W.subtype (LinearMap.ker_eq_bot.mpr (Submodule.subtype_injective W))
  have hset : Set.range bV = Set.image W.subtype (Set.range b) := by
    change Set.range (W.subtype ∘ b) = Set.image W.subtype (Set.range b)
    rw [Set.range_comp]
  have hspan : Submodule.span ℝ (Set.range bV) = W := by
    rw [hset, Submodule.span_image, b.span_eq, Submodule.map_subtype_top]
  have htW : t ∉ W := ht
  have htspan : t ∉ Submodule.span ℝ (Set.range bV) := by
    rw [hspan]
    exact htW
  have hLI : LinearIndependent ℝ (Fin.cons t bV) := hLIbV.finCons htspan
  have hWedge : exteriorPower.ιMulti ℝ (r + 1) (Matrix.vecCons t bV) ≠ 0 := by
    apply ιMulti_ne_zero_of_linearIndependent
    simpa [Matrix.vecCons] using hLI
  have hsurj : Function.Surjective (exteriorPower.map r M.rangeRestrict) :=
    exteriorPower.map_surjective (LinearMap.surjective_rangeRestrict M)
  let omega : ⋀[ℝ]^r W := exteriorPower.ιMulti ℝ r b
  obtain ⟨z, hz⟩ := hsurj omega
  have hfac : M = W.subtype.comp M.rangeRestrict := by
    ext x
    rfl
  have hmapfac : exteriorPower.map r M =
      (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) := by
    calc
      exteriorPower.map r M = exteriorPower.map r (W.subtype.comp M.rangeRestrict) :=
        congrArg (exteriorPower.map r) hfac
      _ = (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) :=
        exteriorPower.map_comp _ _
  have hvalue :
      ((wedgeLeft r t).comp (exteriorPower.map r M)) z =
        exteriorPower.ιMulti ℝ (r + 1) (Matrix.vecCons t bV) := by
    rw [LinearMap.comp_apply, hmapfac, LinearMap.comp_apply, hz]
    simp [omega, bV, wedgeLeft_apply_ιMulti, Function.comp_def]
  intro hzero
  have hzval : ((wedgeLeft r t).comp (exteriorPower.map r M)) z = 0 := by
    rw [hzero]
    simp
  rw [hvalue] at hzval
  exact hWedge hzval

/-- `Psi` vanishes exactly on the image of `M` on the rank-`r` stratum. -/
theorem psi_eq_zero_iff_mem_range [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r) (t : V) :
    psi r M t = 0 ↔ t ∈ M.range := by
  constructor
  · intro hzero
    by_contra ht
    exact psi_ne_zero_of_not_mem_range r M hr ht (by simpa [psi] using hzero)
  · exact psi_eq_zero_of_mem_range r M hr

/-- The compound coordinate is a complete, basis-free coordinate on the
translation quotient `V / range M`, as long as the rank is fixed to `r`. -/
theorem psi_eq_iff_sub_mem_range [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r) (t t' : V) :
    psi r M t = psi r M t' ↔ t - t' ∈ M.range := by
  have hsub : psi r M t - psi r M t' = psi r M (t - t') := by
    ext z
    simp [psi, wedgeLeft]
  constructor
  · intro hEq
    have hzero : psi r M (t - t') = 0 := by
      rw [← hsub, sub_eq_zero.mpr hEq]
    exact (psi_eq_zero_iff_mem_range r M hr _).mp hzero
  · intro hmem
    have hzero : psi r M (t - t') = 0 :=
      (psi_eq_zero_iff_mem_range r M hr _).mpr hmem
    have hdiff : psi r M t - psi r M t' = 0 := by rw [hsub, hzero]
    exact sub_eq_zero.mp hdiff

/-- A translation by `M c` is invisible on the fixed-rank stratum. -/
theorem psi_translation_invariant [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r)
    (t c : V) : psi r M (t + M c) = psi r M t := by
  apply (psi_eq_iff_sub_mem_range r M hr (t + M c) t).2
  convert (show M c ∈ M.range from ⟨c, rfl⟩) using 1 <;> abel

/-- Scaling the top compound scales `Psi` by the same scalar. -/
theorem psi_smul_of_compound_smul (r : ℕ) (M M' : V →ₗ[ℝ] V) (t : V)
    (a : ℝ) (hcompound : exteriorPower.map r M' = a • exteriorPower.map r M) :
    psi r M' t = a • psi r M t := by
  ext z
  simp [psi, wedgeLeft, hcompound]

/-- The projective top compound determines the image plane on the rank-`r`
stratum: proportional compounds with nonzero proportionality have the same
translation-kernel locus, hence the same image subspace. -/
theorem range_eq_of_projectively_equal_compounds [FiniteDimensional ℝ V]
    (r : ℕ) (M M' : V →ₗ[ℝ] V)
    (hM : Module.finrank ℝ M.range = r) (hM' : Module.finrank ℝ M'.range = r)
    (a : ℝ) (ha : a ≠ 0)
    (hcompound : exteriorPower.map r M' = a • exteriorPower.map r M) :
    M.range = M'.range := by
  ext t
  have hpsi := psi_smul_of_compound_smul r M M' t a hcompound
  have hzero : psi r M' t = 0 ↔ psi r M t = 0 := by
    rw [hpsi]
    simp [ha]
  rw [← psi_eq_zero_iff_mem_range r M hM t,
    ← psi_eq_zero_iff_mem_range r M' hM' t]
  exact hzero.symm

/-- The top compound is nonzero at the matching rank. -/
theorem map_ne_zero_of_finrank_range_eq [FiniteDimensional ℝ V]
    (r : ℕ) (M : V →ₗ[ℝ] V) (hr : Module.finrank ℝ M.range = r) :
    exteriorPower.map r M ≠ 0 := by
  let W : Submodule ℝ V := M.range
  let b : Module.Basis (Fin r) ℝ W := Module.finBasisOfFinrankEq ℝ W hr
  let omega : ⋀[ℝ]^r W := exteriorPower.ιMulti ℝ r b
  have homega : omega ≠ 0 := ιMulti_ne_zero_of_linearIndependent b.linearIndependent
  have hsurj : Function.Surjective (exteriorPower.map r M.rangeRestrict) :=
    exteriorPower.map_surjective (LinearMap.surjective_rangeRestrict M)
  obtain ⟨z, hz⟩ := hsurj omega
  have hfac : M = W.subtype.comp M.rangeRestrict := by
    ext x
    rfl
  have hmapfac : exteriorPower.map r M =
      (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) := by
    calc
      exteriorPower.map r M = exteriorPower.map r (W.subtype.comp M.rangeRestrict) :=
        congrArg (exteriorPower.map r) hfac
      _ = (exteriorPower.map r W.subtype).comp (exteriorPower.map r M.rangeRestrict) :=
        exteriorPower.map_comp _ _
  intro hzero
  have hvalue : exteriorPower.map r W.subtype omega = 0 := by
    calc
      exteriorPower.map r W.subtype omega =
          exteriorPower.map r W.subtype (exteriorPower.map r M.rangeRestrict z) :=
            congrArg (exteriorPower.map r W.subtype) hz.symm
      _ = exteriorPower.map r M z := by rw [hmapfac]; rfl
      _ = 0 := by exact congrArg (fun F => F z) hzero
  apply homega
  apply (exteriorPower.map_injective_field (Submodule.subtype_injective W))
  simpa using hvalue


abbrev NullSpace := Fin 4 → ℝ
def nrotMat (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ := fun i j =>
  if i = 0 then if j = 0 then 1 else if j = 1 then a^2/2 else if j = 2 then a else 0
  else if i = 1 then if j = 1 then 1 else 0
  else if i = 2 then if j = 1 then a else if j = 2 then 1 else 0
  else if i = 3 then if j = 3 then 1 else 0 else 0
def nrot (a : ℝ) : NullSpace →ₗ[ℝ] NullSpace := (nrotMat a).mulVecLin
theorem nrot_apply (a : ℝ) (v : NullSpace) : nrot a v = fun i =>
    if i = 0 then v 0 + a^2/2 * v 1 + a * v 2
    else if i = 1 then v 1 else if i = 2 then a*v 1 + v 2 else v 3 := by
  funext i
  fin_cases i <;> simp [nrot, nrotMat, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

def ndefect (a : ℝ) : NullSpace →ₗ[ℝ] NullSpace := LinearMap.id - nrot a

theorem ndefect_apply (a : ℝ) (v : NullSpace) : ndefect a v = fun i =>
    if i = 0 then -a * v 2 - a^2/2 * v 1
    else if i = 1 then 0 else if i = 2 then -a*v 1 else 0 := by
  simp only [ndefect, LinearMap.sub_apply, LinearMap.id_apply, nrot_apply]
  funext i
  fin_cases i <;> simp <;> ring

theorem ndefect_sq_apply (a : ℝ) (v : NullSpace) :
    (ndefect a).comp (ndefect a) v = fun i => if i = 0 then a^2 * v 1 else 0 := by
  rw [LinearMap.comp_apply, ndefect_apply, ndefect_apply]
  funext i
  fin_cases i <;> simp <;> ring

def parabolicPlane : Submodule ℝ NullSpace where
  carrier := {x | x 1 = 0 ∧ x 3 = 0}
  zero_mem' := by simp
  add_mem' := by
    intro x y hx hy
    constructor <;> simp [hx.1, hy.1, hx.2, hy.2]
  smul_mem' := by
    intro c x hx
    constructor <;> simp [hx.1, hx.2]

theorem ndefect_range_eq_plane (a : ℝ) (ha : a ≠ 0) :
    (ndefect a).range = parabolicPlane := by
  apply le_antisymm
  · rintro y ⟨v, rfl⟩
    change (ndefect a v) 1 = 0 ∧ (ndefect a v) 3 = 0
    rw [ndefect_apply]
    simp
  · intro y hy
    change ∃ v, ndefect a v = y
    let v : NullSpace := fun i =>
      if i = 1 then -y 2 / a else if i = 2 then y 2 / 2 - y 0 / a else 0
    refine ⟨v, ?_⟩
    rw [ndefect_apply]
    funext i
    fin_cases i
    · simp [v] <;> field_simp <;> ring
    · simp [v, hy.1]
    · simp [v] <;> field_simp <;> ring
    · simp [v, hy.2]

def e0 : NullSpace := Pi.single 0 1
def e2 : NullSpace := Pi.single 2 1
def e1 : NullSpace := Pi.single 1 1

def planeVec : Fin 2 → NullSpace := fun i => if i = 0 then e0 else e2

def planeEmbedding : Fin 2 → Fin 4 := fun i => if i = 0 then 0 else 2

theorem planeVec_eq_basis_comp : planeVec = (Pi.basisFun ℝ (Fin 4)) ∘ planeEmbedding := by
  funext i
  fin_cases i <;> simp [planeVec, planeEmbedding, e0, e2, Pi.basisFun_apply]

theorem planeVec_li : LinearIndependent ℝ planeVec := by
  rw [planeVec_eq_basis_comp]
  apply (Pi.basisFun ℝ (Fin 4)).linearIndependent.comp planeEmbedding
  intro i j hij
  fin_cases i <;> fin_cases j <;> simp [planeEmbedding] at hij ⊢

theorem parabolicPlane_eq_span : parabolicPlane = Submodule.span ℝ (Set.range planeVec) := by
  apply le_antisymm
  · intro x hx
    have hxexpr : x = x 0 • e0 + x 2 • e2 := by
      funext i
      fin_cases i <;> simp [e0, e2, hx.1, hx.2] <;> ring
    rw [hxexpr]
    apply Submodule.add_mem
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_range_self 0))
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_range_self 1))
  · apply Submodule.span_le.2
    rintro x ⟨i, rfl⟩
    change (planeVec i) 1 = 0 ∧ (planeVec i) 3 = 0
    fin_cases i <;> simp [planeVec, e0, e2]

theorem ndefect_finrank_range (a : ℝ) (ha : a ≠ 0) :
    Module.finrank ℝ (ndefect a).range = 2 := by
  rw [ndefect_range_eq_plane a ha, parabolicPlane_eq_span]
  calc
    Module.finrank ℝ (Submodule.span ℝ (Set.range planeVec)) = Fintype.card (Fin 2) :=
      Module.finrank_eq_card_basis (Module.Basis.span planeVec_li)
    _ = 2 := by decide

def nullLine : Submodule ℝ NullSpace where
  carrier := {x | x 1 = 0 ∧ x 2 = 0 ∧ x 3 = 0}
  zero_mem' := by simp
  add_mem' := by
    intro x y hx hy
    exact ⟨by simp [hx.1, hy.1], by simp [hx.2.1, hy.2.1], by simp [hx.2.2, hy.2.2]⟩
  smul_mem' := by
    intro c x hx
    exact ⟨by simp [hx.1], by simp [hx.2.1], by simp [hx.2.2]⟩

def ndefectSq (a : ℝ) : NullSpace →ₗ[ℝ] NullSpace := (ndefect a).comp (ndefect a)

theorem ndefect_sq_range_eq_nullLine (a : ℝ) (ha : a ≠ 0) :
    (ndefectSq a).range = nullLine := by
  apply le_antisymm
  · rintro y ⟨v, rfl⟩
    change ((ndefect a).comp (ndefect a) v) 1 = 0 ∧ ((ndefect a).comp (ndefect a) v) 2 = 0 ∧ ((ndefect a).comp (ndefect a) v) 3 = 0
    rw [ndefect_sq_apply]
    simp
  · intro y hy
    change ∃ v, (ndefect a).comp (ndefect a) v = y
    let v : NullSpace := fun i => if i = 1 then y 0 / a^2 else 0
    refine ⟨v, ?_⟩
    rw [ndefect_sq_apply]
    funext i
    fin_cases i
    · simp [v] <;> field_simp [ha] <;> ring
    · simp [v, hy.1]
    · simp [v, hy.2.1]
    · simp [v, hy.2.2]

def lorentzForm (x y : NullSpace) : ℝ := x 0 * y 1 + x 1 * y 0 - x 2 * y 2 - x 3 * y 3

def lorentzPerp (W : Submodule ℝ NullSpace) : Submodule ℝ NullSpace where
  carrier := {x | ∀ y ∈ W, lorentzForm x y = 0}
  zero_mem' := by
    intro y hy
    simp [lorentzForm]
  add_mem' := by
    intro x z hx hz y hy
    calc
      lorentzForm (x + z) y = lorentzForm x y + lorentzForm z y := by
        simp [lorentzForm, Pi.add_apply]
        ring
      _ = 0 := by rw [hx y hy, hz y hy]; simp
  smul_mem' := by
    intro a x hx y hy
    calc
      lorentzForm (a • x) y = a * lorentzForm x y := by
        simp [lorentzForm, Pi.smul_apply, smul_eq_mul]
        ring
      _ = 0 := by rw [hx y hy]; simp

theorem parabolicPlane_inter_perp_eq_nullLine :
    parabolicPlane ⊓ lorentzPerp parabolicPlane = nullLine := by
  ext x
  constructor
  · intro hx
    have hxPi : x 1 = 0 ∧ x 3 = 0 := hx.1
    have he2 : e2 ∈ parabolicPlane := by simp [parabolicPlane, e2]
    have hx2 : lorentzForm x e2 = 0 := hx.2 e2 he2
    have hx2' : x 2 = 0 := by simpa [lorentzForm, e2] using hx2
    exact ⟨hxPi.1, hx2', hxPi.2⟩
  · intro hx
    refine ⟨⟨hx.1, hx.2.2⟩, ?_⟩
    intro y hy
    have hy1 : y 1 = 0 := hy.1
    simp [lorentzForm, hx.1, hx.2.1, hx.2.2, hy1]

theorem ndefect_sq_range_eq_radical (a : ℝ) (ha : a ≠ 0) :
    (ndefectSq a).range = (ndefect a).range ⊓ lorentzPerp ((ndefect a).range) := by
  rw [ndefect_sq_range_eq_nullLine a ha, ndefect_range_eq_plane a ha]
  exact parabolicPlane_inter_perp_eq_nullLine.symm

theorem ndefect_sq_finrank_range (a : ℝ) (ha : a ≠ 0) :
    Module.finrank ℝ (ndefectSq a).range = 1 := by
  rw [ndefect_sq_range_eq_nullLine a ha]
  let lineVec : Fin 1 → NullSpace := fun _ => e0
  have heq : lineVec = (Pi.basisFun ℝ (Fin 4)) ∘ (fun _ : Fin 1 => (0 : Fin 4)) := by
    funext i
    simp [lineVec, e0, Pi.basisFun_apply]
  have hli : LinearIndependent ℝ lineVec := by
    rw [heq]
    apply (Pi.basisFun ℝ (Fin 4)).linearIndependent.comp (fun _ : Fin 1 => (0 : Fin 4))
    intro i j h
    exact Subsingleton.elim i j
  have hspan : nullLine = Submodule.span ℝ (Set.range lineVec) := by
    apply le_antisymm
    · intro x hx
      have hxexpr : x = x 0 • e0 := by
        funext i
        fin_cases i <;> simp [e0, hx.1, hx.2.1, hx.2.2] <;> ring
      rw [hxexpr]
      exact Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_range_self (0 : Fin 1)))
    · apply Submodule.span_le.2
      rintro x ⟨i, rfl⟩
      change e0 1 = 0 ∧ e0 2 = 0 ∧ e0 3 = 0
      simp [e0]
  rw [hspan]
  calc
    Module.finrank ℝ (Submodule.span ℝ (Set.range lineVec)) = Fintype.card (Fin 1) :=
      Module.finrank_eq_card_basis (Module.Basis.span hli)
    _ = 1 := by decide

def nrotGenMat (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ := fun i j =>
  if i = 0 then if j = 2 then a else 0
  else if i = 2 then if j = 1 then a else 0 else 0

def nrotGen (a : ℝ) : NullSpace →ₗ[ℝ] NullSpace := (nrotGenMat a).mulVecLin

theorem nrotGen_apply (a : ℝ) (v : NullSpace) : nrotGen a v = fun i =>
    if i = 0 then a*v 2 else if i = 2 then a*v 1 else 0 := by
  funext i
  fin_cases i <;> simp [nrotGen, nrotGenMat, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

theorem nrotGen_sq_apply (a : ℝ) (v : NullSpace) :
    (nrotGen a).comp (nrotGen a) v = fun i => if i = 0 then a^2 * v 1 else 0 := by
  rw [LinearMap.comp_apply, nrotGen_apply, nrotGen_apply]
  funext i
  fin_cases i <;> simp <;> ring

theorem nrotGen_cube_eq_zero (a : ℝ) :
    (nrotGen a).comp ((nrotGen a).comp (nrotGen a)) = 0 := by
  apply LinearMap.ext
  intro v
  rw [LinearMap.comp_apply, nrotGen_sq_apply, nrotGen_apply]
  funext i
  fin_cases i <;> simp <;> ring

def nilpotentExp3 (N : NullSpace →ₗ[ℝ] NullSpace) : NullSpace →ₗ[ℝ] NullSpace :=
  LinearMap.id + N + (1/2 : ℝ) • (N.comp N)

theorem nrot_eq_nilpotentExp3 (a : ℝ) : nrot a = nilpotentExp3 (nrotGen a) := by
  apply LinearMap.ext
  intro v
  funext i
  fin_cases i <;> simp [nilpotentExp3, LinearMap.add_apply, LinearMap.smul_apply,
    Pi.add_apply, Pi.smul_apply, nrot_apply, nrotGen_apply, nrotGen_sq_apply] <;> ring

theorem nrot_preserves_lorentzForm (a : ℝ) (x y : NullSpace) :
    lorentzForm (nrot a x) (nrot a y) = lorentzForm x y := by
  simp [lorentzForm, nrot_apply]
  ring

theorem nrot_nontrivial (a : ℝ) (ha : a ≠ 0) : nrot a ≠ LinearMap.id := by
  intro h
  have hvec := congrArg (fun f : NullSpace →ₗ[ℝ] NullSpace => f e2) h
  have hcoord := congrArg (fun x : NullSpace => x 0) hvec
  simp [nrot_apply, e2] at hcoord
  exact ha hcoord

theorem nrot_comp_neg (a : ℝ) : (nrot a).comp (nrot (-a)) = LinearMap.id := by
  apply LinearMap.ext
  intro v
  rw [LinearMap.comp_apply, nrot_apply, nrot_apply]
  funext i
  fin_cases i <;> simp <;> ring

theorem nrot_neg_comp (a : ℝ) : (nrot (-a)).comp (nrot a) = LinearMap.id := by
  simpa using nrot_comp_neg (-a)

/-- The explicit nontrivial null rotation has a rank-two defect plane and its
image is the radical of the induced Lorentz form. -/
theorem nontrivial_null_rotation_flag (a : ℝ) (ha : a ≠ 0) :
    Module.finrank ℝ (ndefect a).range = 2 ∧
      (ndefectSq a).range =
        (ndefect a).range ⊓ lorentzPerp ((ndefect a).range) ∧
      Module.finrank ℝ (ndefectSq a).range = 1 := by
  exact ⟨ndefect_finrank_range a ha, ndefect_sq_range_eq_radical a ha,
    ndefect_sq_finrank_range a ha⟩

/-- On the rank-two stratum, equality of projective top compounds recovers the
degenerate plane and therefore the null flag of the displayed parabolic
representative. -/
theorem projective_compound_recovers_parabolic_flag [FiniteDimensional ℝ NullSpace]
    (M : NullSpace →ₗ[ℝ] NullSpace) (hM : Module.finrank ℝ M.range = 2)
    (a q : ℝ) (ha : a ≠ 0) (hq : q ≠ 0)
    (hcompound : exteriorPower.map 2 (ndefect a) = q • exteriorPower.map 2 M) :
    M.range = (ndefect a).range ∧
      (ndefectSq a).range = M.range ⊓ lorentzPerp M.range := by
  have hplane := range_eq_of_projectively_equal_compounds 2 M (ndefect a) hM
    (ndefect_finrank_range a ha) q hq hcompound
  refine ⟨hplane, ?_⟩
  rw [hplane]
  exact ndefect_sq_range_eq_radical a ha

/-- The exact top compound of a nontrivial null rotation is nonzero, so its
projective class is defined. -/
theorem parabolic_top_compound_ne_zero (a : ℝ) (ha : a ≠ 0) :
    exteriorPower.map 2 (ndefect a) ≠ 0 :=
  map_ne_zero_of_finrank_range_eq 2 (ndefect a) (ndefect_finrank_range a ha)

/-- A three-vector witness: outside the rank-two stratum, even the identity
map does not have translation-invariant `Psi_2`. -/
def tripleEmbedding : Fin 3 → Fin 4 := fun i => i.castLE (by omega)

def tripleVec : Fin 3 → NullSpace := (Pi.basisFun ℝ (Fin 4)) ∘ tripleEmbedding

theorem tripleVec_eq_basis_comp :
    tripleVec = (Pi.basisFun ℝ (Fin 4)) ∘ tripleEmbedding := rfl

theorem tripleVec_linearIndependent : LinearIndependent ℝ tripleVec := by
  rw [tripleVec_eq_basis_comp]
  apply (Pi.basisFun ℝ (Fin 4)).linearIndependent.comp tripleEmbedding
  intro i j hij
  fin_cases i <;> fin_cases j <;> simp [tripleEmbedding] at hij ⊢

theorem psi_two_identity_not_translation_invariant :
    psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) e0 ≠
      psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) 0 := by
  have hWedge : exteriorPower.ιMulti ℝ 3 tripleVec ≠ 0 :=
    ιMulti_ne_zero_of_linearIndependent tripleVec_linearIndependent
  let pair : Fin 2 → NullSpace := Fin.tail tripleVec
  have hvec : Matrix.vecCons e0 pair = tripleVec := by
    have he0 : e0 = tripleVec 0 := by simp [tripleVec, tripleEmbedding, e0]
    change Fin.cons e0 (Fin.tail tripleVec) = tripleVec
    rw [he0]
    exact Fin.cons_self_tail tripleVec
  have hvalue : psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) e0
      (exteriorPower.ιMulti ℝ 2 pair) = exteriorPower.ιMulti ℝ 3 tripleVec := by
    simp [psi, pair, wedgeLeft_apply_ιMulti, exteriorPower.map_id, hvec]
  intro heq
  have hzero : psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) e0
      (exteriorPower.ιMulti ℝ 2 pair) =
        psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) 0
          (exteriorPower.ιMulti ℝ 2 pair) := by
    simpa using congrArg (fun F => F (exteriorPower.ιMulti ℝ 2 pair)) heq
  rw [hvalue] at hzero
  have hzeroRhs :
      psi 2 (LinearMap.id : NullSpace →ₗ[ℝ] NullSpace) 0
        (exteriorPower.ιMulti ℝ 2 pair) = 0 := by
    simp [psi, wedgeLeft]
  rw [hzeroRhs] at hzero
  exact hWedge hzero


end
end D0.Geometry.A4DRankCompoundAffineQuotient
