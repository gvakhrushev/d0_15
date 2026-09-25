import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic
import D0.Geometry.A4DQuotientSaturationPassport
import D0.Geometry.A4DRelativeAEComparisonSpan

/-!
# Quotient saturation collapse witness

Exact algebraic witness for memo §11.2 / (11.4):

```
B = (e_A, e_B, e_C, 0),
S = (e_B, e_C, e_D, e_A)
```

Saturation of `⊥` yields dimensions `1,2,3,4` and collapses the fibre.
Also `verticalDefect` alone fails (11.1).
-/

namespace D0.Geometry.A4DQuotientSaturationWitness

open D0
open D0.Geometry.A4DRelativeAEComparisonSpan
open D0.Geometry.A4DQuotientSaturationPassport

noncomputable section

/-- Every Role is one of the four named labels. -/
private theorem role_eq_ABCD (r : Role) : r = A ∨ r = B ∨ r = C ∨ r = D := by
  rcases r with ⟨x, y⟩
  fin_cases x <;> fin_cases y <;> simp [A, B, C, D]

/-- Role basis vector in the labelled coefficient / fibre space. -/
def e (r : Role) : LabelCoeff := EuclideanSpace.single r 1

theorem e_apply (r s : Role) : e r s = if s = r then (1 : ℝ) else 0 := by
  simp [e, PiLp.single_apply]

theorem e_ne_zero (r : Role) : e r ≠ 0 := by
  intro h
  have := congrArg (fun v : LabelCoeff => v r) h
  simp [e, PiLp.single_apply] at this

/-- Research witness `B` via Role-coordinate functionals. -/
def witnessB : LabelCoeff →ₗ[ℝ] LabelCoeff :=
  (coeffRole A).smulRight (e A) +
    (coeffRole B).smulRight (e B) +
    (coeffRole C).smulRight (e C)

/-- Research witness `S`. -/
def witnessS : LabelCoeff →ₗ[ℝ] LabelCoeff :=
  (coeffRole A).smulRight (e B) +
    (coeffRole B).smulRight (e C) +
    (coeffRole C).smulRight (e D) +
    (coeffRole D).smulRight (e A)

theorem witnessB_apply (c : LabelCoeff) :
    witnessB c = c A • e A + c B • e B + c C • e C := by
  simp [witnessB, coeffRole, LinearMap.add_apply, LinearMap.smulRight_apply]

theorem witnessS_apply (c : LabelCoeff) :
    witnessS c = c A • e B + c B • e C + c C • e D + c D • e A := by
  simp [witnessS, coeffRole, LinearMap.add_apply, LinearMap.smulRight_apply]


@[simp] theorem witnessB_single_A : witnessB (e A) = e A := by
  simp [witnessB_apply, e, PiLp.single_apply,
    show B ≠ A by decide, show C ≠ A by decide]

@[simp] theorem witnessB_single_B : witnessB (e B) = e B := by
  simp [witnessB_apply, e, PiLp.single_apply,
    show A ≠ B by decide, show C ≠ B by decide]

@[simp] theorem witnessB_single_C : witnessB (e C) = e C := by
  simp [witnessB_apply, e, PiLp.single_apply,
    show A ≠ C by decide, show B ≠ C by decide]

@[simp] theorem witnessB_single_D : witnessB (e D) = 0 := by
  simp [witnessB_apply, e, PiLp.single_apply,
    show A ≠ D by decide, show B ≠ D by decide, show C ≠ D by decide]

@[simp] theorem witnessS_single_A : witnessS (e A) = e B := by
  simp [witnessS_apply, e, PiLp.single_apply,
    show B ≠ A by decide, show C ≠ A by decide, show D ≠ A by decide]

@[simp] theorem witnessS_single_B : witnessS (e B) = e C := by
  simp [witnessS_apply, e, PiLp.single_apply,
    show A ≠ B by decide, show C ≠ B by decide, show D ≠ B by decide]

@[simp] theorem witnessS_single_C : witnessS (e C) = e D := by
  simp [witnessS_apply, e, PiLp.single_apply,
    show A ≠ C by decide, show B ≠ C by decide, show D ≠ C by decide]

@[simp] theorem witnessS_single_D : witnessS (e D) = e A := by
  simp [witnessS_apply, e, PiLp.single_apply,
    show A ≠ D by decide, show B ≠ D by decide, show C ≠ D by decide]

theorem ker_witnessB :
    LinearMap.ker witnessB = Submodule.span ℝ {e D} := by
  refine le_antisymm ?_ ?_
  · intro c hc
    have hA : c A = 0 := by
      have := congrArg (fun v : LabelCoeff => v A) (LinearMap.mem_ker.mp hc)
      simpa [witnessB_apply, e, PiLp.single_apply,
        show A ≠ B by decide, show A ≠ C by decide] using this
    have hB : c B = 0 := by
      have := congrArg (fun v : LabelCoeff => v B) (LinearMap.mem_ker.mp hc)
      simpa [witnessB_apply, e, PiLp.single_apply,
        show B ≠ A by decide, show B ≠ C by decide] using this
    have hC : c C = 0 := by
      have := congrArg (fun v : LabelCoeff => v C) (LinearMap.mem_ker.mp hc)
      simpa [witnessB_apply, e, PiLp.single_apply,
        show C ≠ A by decide, show C ≠ B by decide] using this
    have : c = c D • e D := by
      ext r
      rcases role_eq_ABCD r with rfl | rfl | rfl | rfl
      · simp [hA, e, PiLp.single_apply, show A ≠ D by decide]
      · simp [hB, e, PiLp.single_apply, show B ≠ D by decide]
      · simp [hC, e, PiLp.single_apply, show C ≠ D by decide]
      · simp [e, PiLp.single_apply]
    rw [this]
    exact Submodule.smul_mem _ _ (Submodule.subset_span (by simp))
  · refine Submodule.span_le.mpr ?_
    intro x hx
    simp only [Set.mem_singleton_iff] at hx
    subst hx
    exact LinearMap.mem_ker.mpr witnessB_single_D

theorem verticalDefect_witness :
    verticalDefect witnessB witnessS = Submodule.span ℝ {e A} := by
  change (LinearMap.ker witnessB).map witnessS = _
  rw [ker_witnessB, Submodule.map_span]
  refine congrArg (Submodule.span ℝ) ?_
  ext x
  simp [Set.image_singleton, Set.mem_singleton_iff, witnessS_single_D]

/-- Explicit saturation tower. -/
def chain (n : ℕ) : Submodule ℝ LabelCoeff :=
  if n = 0 then ⊥
  else if n = 1 then Submodule.span ℝ {e A}
  else if n = 2 then Submodule.span ℝ ({e A, e B} : Set LabelCoeff)
  else if n = 3 then Submodule.span ℝ ({e A, e B, e C} : Set LabelCoeff)
  else ⊤

@[simp] theorem chain_zero : chain 0 = ⊥ := by simp [chain]
@[simp] theorem chain_one : chain 1 = Submodule.span ℝ {e A} := by simp [chain]
@[simp] theorem chain_two :
    chain 2 = Submodule.span ℝ ({e A, e B} : Set LabelCoeff) := by simp [chain]
@[simp] theorem chain_three :
    chain 3 = Submodule.span ℝ ({e A, e B, e C} : Set LabelCoeff) := by simp [chain]
theorem chain_of_four_le {n : ℕ} (h : 4 ≤ n) : chain n = ⊤ := by
  simp only [chain]
  split_ifs <;> try omega
  rfl

private theorem mem_inducedImage_of
    {W : Submodule ℝ LabelCoeff} {c : LabelCoeff} (hc : witnessB c ∈ W) :
    witnessS c ∈ inducedImage witnessB witnessS W :=
  Submodule.mem_map_of_mem (Submodule.mem_comap.mpr hc)

private theorem coords_of_Bc_in_spanA {c : LabelCoeff}
    (hc : witnessB c ∈ Submodule.span ℝ {e A}) : c B = 0 ∧ c C = 0 := by
  obtain ⟨α, hα⟩ := Submodule.mem_span_singleton.mp hc
  have hB := congrArg (fun v : LabelCoeff => v B) hα
  have hC := congrArg (fun v : LabelCoeff => v C) hα
  simp [witnessB_apply, e, PiLp.single_apply,
    show B ≠ A by decide, show B ≠ C by decide,
    show C ≠ A by decide, show C ≠ B by decide] at hB hC
  exact ⟨hB.symm, hC.symm⟩

private theorem coordC_of_Bc_in_spanAB {c : LabelCoeff}
    (hc : witnessB c ∈ Submodule.span ℝ ({e A, e B} : Set LabelCoeff)) : c C = 0 := by
  have hle : Submodule.span ℝ ({e A, e B} : Set LabelCoeff) ≤
      LinearMap.ker (coeffRole C) := by
    refine Submodule.span_le.mpr ?_
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · simp [LinearMap.mem_ker, coeffRole, e, PiLp.single_apply, show C ≠ A by decide]
    · simp [LinearMap.mem_ker, coeffRole, e, PiLp.single_apply, show C ≠ B by decide]
  have hker : witnessB c ∈ LinearMap.ker (coeffRole C) := hle hc
  have : (witnessB c) C = 0 := by
    simpa [LinearMap.mem_ker, coeffRole] using hker
  simpa [witnessB_apply, e, PiLp.single_apply,
    show C ≠ A by decide, show C ≠ B by decide] using this

theorem saturateStep_chain0 :
    saturateStep witnessB witnessS (chain 0) = chain 1 := by
  simp only [chain_zero, chain_one, saturateStep]
  simp only [bot_sup_eq]
  change inducedImage witnessB witnessS ⊥ = Submodule.span ℝ {e A}
  simpa [inducedImage, Submodule.comap_bot, verticalDefect] using verticalDefect_witness

theorem saturateStep_chain1 :
    saturateStep witnessB witnessS (chain 1) = chain 2 := by
  simp only [chain_one, chain_two]
  refine le_antisymm ?_ ?_
  · rw [saturateStep]
    refine sup_le (Submodule.span_mono (by simp)) ?_
    intro v hv
    rcases Submodule.mem_map.mp hv with ⟨c, hc, rfl⟩
    have ⟨hB0, hC0⟩ := coords_of_Bc_in_spanA (Submodule.mem_comap.mp hc)
    have : witnessS c = c D • e A + c A • e B := by
      simp [witnessS_apply, hB0, hC0, add_comm, add_assoc]
    rw [this]
    exact add_mem
      (Submodule.smul_mem _ _ (Submodule.subset_span
        (by simp : e A ∈ ({e A, e B} : Set LabelCoeff))))
      (Submodule.smul_mem _ _ (Submodule.subset_span
        (by simp : e B ∈ ({e A, e B} : Set LabelCoeff))))
  · refine Submodule.span_le.mpr ?_
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact (le_saturateStep witnessB witnessS _)
        (Submodule.subset_span (Set.mem_singleton (e A)))
    · refine (le_sup_right :
          inducedImage witnessB witnessS (Submodule.span ℝ {e A}) ≤
            saturateStep witnessB witnessS (Submodule.span ℝ {e A})) ?_
      have hmem : witnessB (e A) ∈ Submodule.span ℝ {e A} := by
        simpa [witnessB_single_A] using
          (Submodule.subset_span (Set.mem_singleton (e A)) :
            e A ∈ Submodule.span ℝ {e A})
      simpa [witnessS_single_A] using mem_inducedImage_of hmem

theorem saturateStep_chain2 :
    saturateStep witnessB witnessS (chain 2) = chain 3 := by
  simp only [chain_two, chain_three]
  refine le_antisymm ?_ ?_
  · rw [saturateStep]
    refine sup_le (Submodule.span_mono (by
      intro x hx; simp [Set.mem_insert_iff] at hx ⊢
      rcases hx with rfl | rfl <;> simp)) ?_
    intro v hv
    rcases Submodule.mem_map.mp hv with ⟨c, hc, rfl⟩
    have hC0 := coordC_of_Bc_in_spanAB (Submodule.mem_comap.mp hc)
    have : witnessS c = c D • e A + c A • e B + c B • e C := by
      simp [witnessS_apply, hC0, add_comm, add_left_comm, add_assoc]
    rw [this]
    exact add_mem (add_mem
      (Submodule.smul_mem _ _ (Submodule.subset_span
        (by simp : e A ∈ ({e A, e B, e C} : Set LabelCoeff))))
      (Submodule.smul_mem _ _ (Submodule.subset_span
        (by simp : e B ∈ ({e A, e B, e C} : Set LabelCoeff)))))
      (Submodule.smul_mem _ _ (Submodule.subset_span
        (by simp : e C ∈ ({e A, e B, e C} : Set LabelCoeff))))
  · refine Submodule.span_le.mpr ?_
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    have hA : e A ∈ chain 2 := by
      simp [chain_two]; exact Submodule.subset_span (by simp)
    have hB : e B ∈ chain 2 := by
      simp [chain_two]; exact Submodule.subset_span (by simp)
    rcases hx with rfl | rfl | rfl
    · exact (le_saturateStep _ _ _) (by simpa [chain_two] using hA)
    · exact (le_saturateStep _ _ _) (by simpa [chain_two] using hB)
    · refine (le_sup_right :
          inducedImage witnessB witnessS (chain 2) ≤
            saturateStep witnessB witnessS (chain 2)) ?_
      have hmem : witnessB (e B) ∈ chain 2 := by
        simpa [chain_two, witnessB_single_B] using hB
      simpa [chain_two, witnessS_single_B] using mem_inducedImage_of hmem

theorem saturateStep_chain3 :
    saturateStep witnessB witnessS (chain 3) = chain 4 := by
  have h4 : chain 4 = ⊤ := chain_of_four_le (by norm_num)
  rw [h4]
  refine le_antisymm le_top ?_
  have hA : e A ∈ saturateStep witnessB witnessS (chain 3) :=
    (le_saturateStep _ _ _) (by
      simp [chain_three]; exact Submodule.subset_span (by simp))
  have hB : e B ∈ saturateStep witnessB witnessS (chain 3) :=
    (le_saturateStep _ _ _) (by
      simp [chain_three]; exact Submodule.subset_span (by simp))
  have hC : e C ∈ saturateStep witnessB witnessS (chain 3) :=
    (le_saturateStep _ _ _) (by
      simp [chain_three]; exact Submodule.subset_span (by simp))
  have hD : e D ∈ saturateStep witnessB witnessS (chain 3) := by
    refine (le_sup_right :
        inducedImage witnessB witnessS (chain 3) ≤
          saturateStep witnessB witnessS (chain 3)) ?_
    have hmem : witnessB (e C) ∈ chain 3 := by
      simp [chain_three, witnessB_single_C]
      exact Submodule.subset_span (by simp : e C ∈ ({e A, e B, e C} : Set LabelCoeff))
    simpa [chain_three, witnessS_single_C] using mem_inducedImage_of hmem
  have hspan : Submodule.span ℝ (Set.range e) ≤
      saturateStep witnessB witnessS (chain 3) := by
    refine Submodule.span_le.mpr ?_
    intro x hx
    rcases hx with ⟨r, rfl⟩
    rcases role_eq_ABCD r with rfl | rfl | rfl | rfl
    · exact hA
    · exact hB
    · exact hC
    · exact hD
  have htop : Submodule.span ℝ (Set.range e) = ⊤ := by
    refine eq_top_iff.mpr ?_
    intro v _
    have hv : v = v A • e A + v B • e B + v C • e C + v D • e D := by
      ext i
      rcases role_eq_ABCD i with rfl | rfl | rfl | rfl
      · simp [e, PiLp.single_apply,
          show A ≠ B by decide, show A ≠ C by decide, show A ≠ D by decide]
      · simp [e, PiLp.single_apply,
          show B ≠ A by decide, show B ≠ C by decide, show B ≠ D by decide]
      · simp [e, PiLp.single_apply,
          show C ≠ A by decide, show C ≠ B by decide, show C ≠ D by decide]
      · simp [e, PiLp.single_apply,
          show D ≠ A by decide, show D ≠ B by decide, show D ≠ C by decide]
    rw [hv]
    refine add_mem (add_mem (add_mem ?_ ?_) ?_) ?_
    · exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨A, rfl⟩)
    · exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨B, rfl⟩)
    · exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨C, rfl⟩)
    · exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨D, rfl⟩)
  simpa [htop] using hspan

theorem saturateStep_chain_ge4 {n : ℕ} (hn : 4 ≤ n) :
    saturateStep witnessB witnessS (chain n) = chain (n + 1) := by
  have h1 := chain_of_four_le hn
  have h2 := chain_of_four_le (Nat.le_succ_of_le hn)
  simp [h1, h2, saturateStep]

theorem saturateIter_eq_chain (n : ℕ) :
    saturateIter witnessB witnessS (⊥ : Submodule ℝ LabelCoeff) n = chain n := by
  induction n with
  | zero => simp [saturateIter_zero]
  | succ n ih =>
    rw [saturateIter_succ, ih]
    match n with
    | 0 => exact saturateStep_chain0
    | 1 => exact saturateStep_chain1
    | 2 => exact saturateStep_chain2
    | 3 => exact saturateStep_chain3
    | k + 4 => exact saturateStep_chain_ge4 (by omega)

private theorem linIndep_AB : LinearIndependent ℝ ![e A, e B] := by
  refine LinearIndependent.pair_iff.mpr ?_
  intro a b hab
  constructor
  · have := congrArg (fun v : LabelCoeff => v A) hab
    simpa [e, PiLp.single_apply, show A ≠ B by decide] using this
  · have := congrArg (fun v : LabelCoeff => v B) hab
    simpa [e, PiLp.single_apply, show B ≠ A by decide] using this

private theorem linIndep_ABC : LinearIndependent ℝ ![e A, e B, e C] := by
  refine Fintype.linearIndependent_iff.mpr ?_
  intro g hg i
  have hA := congrArg (fun v : LabelCoeff => v A) hg
  have hB := congrArg (fun v : LabelCoeff => v B) hg
  have hC := congrArg (fun v : LabelCoeff => v C) hg
  simp [Fin.sum_univ_three, e, PiLp.single_apply,
    show A ≠ B by decide, show A ≠ C by decide,
    show B ≠ A by decide, show B ≠ C by decide,
    show C ≠ A by decide, show C ≠ B by decide] at hA hB hC
  fin_cases i <;> simp_all

theorem saturate_dims :
    Module.finrank ℝ (saturateIter witnessB witnessS ⊥ 1) = 1 ∧
    Module.finrank ℝ (saturateIter witnessB witnessS ⊥ 2) = 2 ∧
    Module.finrank ℝ (saturateIter witnessB witnessS ⊥ 3) = 3 ∧
    Module.finrank ℝ (saturateIter witnessB witnessS ⊥ 4) = 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [saturateIter_eq_chain, chain_one]
    exact finrank_span_singleton (e_ne_zero A)
  · rw [saturateIter_eq_chain, chain_two]
    have eqr : Submodule.span ℝ ({e A, e B} : Set LabelCoeff) =
        Submodule.span ℝ (Set.range ![e A, e B]) := by
      refine congrArg _ ?_
      ext x
      constructor
      · intro hx
        simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
        rcases hx with rfl | rfl
        · exact ⟨0, rfl⟩
        · exact ⟨1, rfl⟩
      · intro ⟨i, hi⟩
        fin_cases i <;> simp_all [Set.mem_insert_iff]
    rw [eqr]
    simpa using (finrank_span_eq_card linIndep_AB)
  · rw [saturateIter_eq_chain, chain_three]
    have eqr : Submodule.span ℝ ({e A, e B, e C} : Set LabelCoeff) =
        Submodule.span ℝ (Set.range ![e A, e B, e C]) := by
      refine congrArg _ ?_
      ext x
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff, Set.mem_range]
      constructor
      · intro h; rcases h with rfl | rfl | rfl
        · exact ⟨0, rfl⟩
        · exact ⟨1, rfl⟩
        · exact ⟨2, rfl⟩
      · intro ⟨i, hi⟩; fin_cases i <;> simp_all
    rw [eqr]
    simpa using (finrank_span_eq_card linIndep_ABC)
  · rw [saturateIter_eq_chain, chain_of_four_le (by norm_num : 4 ≤ 4)]
    rw [finrank_top, finrank_euclideanSpace, card_role]

theorem saturate_collapses_fibre :
    saturateIter witnessB witnessS (⊥ : Submodule ℝ LabelCoeff) 4 = ⊤ := by
  rw [saturateIter_eq_chain, chain_of_four_le (by norm_num : 4 ≤ 4)]

theorem verticalDefect_not_sameFibreGraphClosed :
    ¬ SameFibreGraphClosed witnessB witnessS (verticalDefect witnessB witnessS) := by
  rw [verticalDefect_witness, sameFibreGraphClosed_iff_mem witnessB witnessS]
  push Not
  refine ⟨e A, ?_, ?_⟩
  · simpa [witnessB_single_A] using
      (Submodule.subset_span (Set.mem_singleton (e A)) : e A ∈ Submodule.span ℝ {e A})
  · intro h
    have heB : e B ∈ Submodule.span ℝ {e A} := by simpa [witnessS_single_A] using h
    obtain ⟨α, hα⟩ := Submodule.mem_span_singleton.mp heB
    have hB := congrArg (fun v : LabelCoeff => v B) hα
    simp [e, PiLp.single_apply, show B ≠ A by decide] at hB

theorem verticalDefectNotUniversalRepair_witness :
    VerticalDefectNotUniversalRepair :=
  ⟨witnessB, witnessS, verticalDefect_not_sameFibreGraphClosed⟩

end

end D0.Geometry.A4DQuotientSaturationWitness
