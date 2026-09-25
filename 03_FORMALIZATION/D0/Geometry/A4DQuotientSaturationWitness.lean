import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.StdBasis
import D0.Core.DyadABCD
import D0.Geometry.A4DQuotientSaturationPassport

/-!
# Exact quotient-saturation witness

Memo §11.2. At identity transport

`B = (e_A, e_B, e_C, 0)`, `S = (e_B, e_C, e_D, e_A)`,

the vertical defect is the line `ℚ e_A`. Saturation produces
`span(e_A, e_B)`, `span(e_A, e_B, e_C)`, then the whole Role fibre.
Quotient by that line is not a fixed point of (11.3).

Controls: flat Nyquist kills `e_A`, including `4 e_A`; the exact A/B boost
has coinvariant equal to the A/B plane; dropping one of two parallel loops
shrinks the coinvariant; `W = ⊤` is always a fixed point and is not a
classical limit.

The carrier is `Role → ℚ`. No physical readout is inferred.
-/

namespace D0.Geometry

open D0 Module

set_option linter.unusedSimpArgs false

noncomputable section

abbrev RoleCoeff := Role → ℚ

def roleBasisVec (r : Role) : RoleCoeff :=
  Pi.single r (1 : ℚ)

def supported (s : Set Role) : Submodule ℚ RoleCoeff where
  carrier := {v | ∀ r, r ∉ s → v r = 0}
  zero_mem' := by intro r _; rfl
  add_mem' := by
    intro x y hx hy r hr
    simp [hx r hr, hy r hr]
  smul_mem' := by
    intro a x hx r hr
    simp [hx r hr]

lemma mem_supported {s : Set Role} {v : RoleCoeff} :
    v ∈ supported s ↔ ∀ r, r ∉ s → v r = 0 :=
  Iff.rfl

@[simp] lemma roleBasisVec_apply (r t : Role) :
    roleBasisVec r t = if t = r then (1 : ℚ) else 0 := by
  simp [roleBasisVec, Pi.single_apply]

@[simp] lemma smul_roleBasisVec (c : ℚ) (r t : Role) :
    (c • roleBasisVec r) t = if t = r then c else 0 := by
  simp [roleBasisVec_apply, Pi.smul_apply, smul_eq_mul, mul_ite, mul_one, mul_zero]

lemma sum_roleBasis (x : RoleCoeff) :
    (∑ r : Role, x r • roleBasisVec r) = x := by
  ext i
  simp only [Finset.sum_apply, smul_roleBasisVec]
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hj
    simp [if_neg (Ne.symm hj)]
  · intro hi
    exact absurd (Finset.mem_univ i) hi

lemma roleSpan_eq_supported (s : Set Role) :
    Submodule.span ℚ (roleBasisVec '' s) = supported s := by
  apply le_antisymm
  · rw [Submodule.span_le]
    intro v hv t ht
    rcases hv with ⟨r, hr, rfl⟩
    have hne : t ≠ r := by
      intro htr
      exact ht (htr ▸ hr)
    simp [roleBasisVec_apply, if_neg hne]
  · intro x hx
    rw [← sum_roleBasis x]
    refine Submodule.sum_mem _ fun r _ => ?_
    by_cases hr : r ∈ s
    · exact Submodule.smul_mem _ (x r) (Submodule.subset_span ⟨r, hr, rfl⟩)
    · simp [hx r hr, roleBasisVec]

@[simp] lemma A_ne_B : A ≠ B := by decide
@[simp] lemma A_ne_C : A ≠ C := by decide
@[simp] lemma A_ne_D : A ≠ D := by decide
@[simp] lemma B_ne_A : B ≠ A := by decide
@[simp] lemma B_ne_C : B ≠ C := by decide
@[simp] lemma B_ne_D : B ≠ D := by decide
@[simp] lemma C_ne_A : C ≠ A := by decide
@[simp] lemma C_ne_B : C ≠ B := by decide
@[simp] lemma C_ne_D : C ≠ D := by decide
@[simp] lemma D_ne_A : D ≠ A := by decide
@[simp] lemma D_ne_B : D ≠ B := by decide
@[simp] lemma D_ne_C : D ≠ C := by decide

lemma role_eq_ACDB (r : Role) : r = A ∨ r = C ∨ r = D ∨ r = B := by
  rcases r with ⟨i, j⟩
  fin_cases i <;> fin_cases j
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr (Or.inl rfl))
  · exact Or.inr (Or.inr (Or.inr rfl))

def collapseB : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c := c A • roleBasisVec A + c B • roleBasisVec B + c C • roleBasisVec C
  map_add' := by
    intro x y
    ext r
    simp [add_smul, Pi.add_apply]
    ring
  map_smul' := by
    intro a x
    ext r
    simp [Pi.smul_apply, smul_eq_mul, mul_ite]
    split_ifs <;> ring

def collapseS : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c :=
    c A • roleBasisVec B + c B • roleBasisVec C + c C • roleBasisVec D + c D • roleBasisVec A
  map_add' := by
    intro x y
    ext r
    simp [add_smul, Pi.add_apply]
    ring
  map_smul' := by
    intro a x
    ext r
    simp [Pi.smul_apply, smul_eq_mul, mul_ite]
    split_ifs <;> ring

@[simp] lemma collapseB_apply (c : RoleCoeff) (t : Role) :
    collapseB c t =
      (if t = A then c A else 0) + (if t = B then c B else 0) + (if t = C then c C else 0) := by
  change (c A • roleBasisVec A + c B • roleBasisVec B + c C • roleBasisVec C) t = _
  simp only [Pi.add_apply, smul_roleBasisVec]

@[simp] lemma collapseS_apply (c : RoleCoeff) (t : Role) :
    collapseS c t =
      (if t = B then c A else 0) + (if t = C then c B else 0) +
        (if t = D then c C else 0) + (if t = A then c D else 0) := by
  change (c A • roleBasisVec B + c B • roleBasisVec C + c C • roleBasisVec D +
    c D • roleBasisVec A) t = _
  simp only [Pi.add_apply, smul_roleBasisVec]

lemma collapseB_A (c : RoleCoeff) : collapseB c A = c A := by
  simp [collapseB_apply, if_pos (rfl : A = A), if_neg (by decide : A ≠ B),
    if_neg (by decide : A ≠ C)]

lemma collapseB_B (c : RoleCoeff) : collapseB c B = c B := by
  simp [collapseB_apply, if_neg (by decide : B ≠ A), if_pos (rfl : B = B),
    if_neg (by decide : B ≠ C)]

lemma collapseB_C (c : RoleCoeff) : collapseB c C = c C := by
  simp [collapseB_apply, if_neg (by decide : C ≠ A), if_neg (by decide : C ≠ B),
    if_pos (rfl : C = C)]

lemma collapseB_D (c : RoleCoeff) : collapseB c D = 0 := by
  simp [collapseB_apply, if_neg (by decide : D ≠ A), if_neg (by decide : D ≠ B),
    if_neg (by decide : D ≠ C)]

lemma collapseS_A (c : RoleCoeff) : collapseS c A = c D := by
  simp [collapseS_apply, if_neg (by decide : A ≠ B), if_neg (by decide : A ≠ C),
    if_neg (by decide : A ≠ D), if_pos (rfl : A = A)]

lemma collapseS_B (c : RoleCoeff) : collapseS c B = c A := by
  simp [collapseS_apply, if_pos (rfl : B = B), if_neg (by decide : B ≠ C),
    if_neg (by decide : B ≠ D), if_neg (by decide : B ≠ A)]

lemma collapseS_C (c : RoleCoeff) : collapseS c C = c B := by
  simp [collapseS_apply, if_neg (by decide : C ≠ B), if_pos (rfl : C = C),
    if_neg (by decide : C ≠ D), if_neg (by decide : C ≠ A)]

lemma collapseS_D (c : RoleCoeff) : collapseS c D = c C := by
  simp [collapseS_apply, if_neg (by decide : D ≠ B), if_neg (by decide : D ≠ C),
    if_pos (rfl : D = D), if_neg (by decide : D ≠ A)]

attribute [irreducible] collapseB collapseS
attribute [simp 2000] collapseB_A collapseB_B collapseB_C collapseB_D
  collapseS_A collapseS_B collapseS_C collapseS_D roleBasisVec_apply

def lineA : Submodule ℚ RoleCoeff := supported {A}
def lineB : Submodule ℚ RoleCoeff := supported {B}
def planeAB : Submodule ℚ RoleCoeff := supported {A, B}
def spaceABC : Submodule ℚ RoleCoeff := supported {A, B, C}
def lineD : Submodule ℚ RoleCoeff := supported {D}
def planeAD : Submodule ℚ RoleCoeff := supported {A, D}
def spaceABD : Submodule ℚ RoleCoeff := supported {A, B, D}

lemma not_mem_insert {r s t : Role} (hrs : r ≠ s) (hrt : r ≠ t) : r ∉ ({s, t} : Set Role) := by
  simp [hrs, hrt]

lemma lineA_le_plane : lineA ≤ planeAB := by
  intro v hv r hr
  exact hv r (by
    intro hrA
    apply hr
    simp only [Set.mem_singleton_iff] at hrA
    simp [hrA])

lemma plane_le_space : planeAB ≤ spaceABC := by
  intro v hv r hr
  exact hv r (by
    intro hmem
    apply hr
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hmem
    rcases hmem with rfl | rfl <;> simp)

lemma collapse_unitStep (W : Submodule ℚ RoleCoeff) :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) W =
      W ⊔ (Submodule.comap collapseB W).map collapseS := by
  simp [saturationStep, saturationSum, iSup_unique]

lemma ext_role (x y : RoleCoeff) (h : ∀ r, x r = y r) : x = y := by
  ext r; exact h r

lemma comap_collapseB_bot : Submodule.comap collapseB ⊥ = lineD := by
  ext c
  constructor
  · intro hc r hr
    have h0 : collapseB c = 0 := by simpa [Submodule.mem_comap, Submodule.mem_bot] using hc
    have hrD : r ≠ D := by simpa using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · simpa [collapseB_A] using congrFun h0 A
    · simpa [collapseB_C] using congrFun h0 C
    · exact absurd rfl hrD
    · simpa [collapseB_B] using congrFun h0 B
  · intro hc
    rw [Submodule.mem_comap, Submodule.mem_bot]
    apply ext_role
    intro r
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · simpa [collapseB_A] using hc A (by simp)
    · simpa [collapseB_C] using hc C (by simp)
    · simp [collapseB_D]
    · simpa [collapseB_B] using hc B (by simp)

lemma map_collapseS_lineD : lineD.map collapseS = lineA := by
  apply le_antisymm
  · intro v hv
    rcases hv with ⟨c, hc, rfl⟩
    intro r hr
    have hA : c A = 0 := hc A (by simp)
    have hB : c B = 0 := hc B (by simp)
    have hC : c C = 0 := hc C (by simp)
    have hrA : r ≠ A := by simpa using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hrA
    · simp [collapseS_C, hB]
    · simp [collapseS_D, hC]
    · simp [collapseS_B, hA]
  · intro v hv
    refine ⟨v A • roleBasisVec D, ?_, ?_⟩
    · intro r hr
      have hrD : r ≠ D := by simpa using hr
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · simp [smul_roleBasisVec, hrD]
      · simp [smul_roleBasisVec, hrD]
      · exact absurd rfl hrD
      · simp [smul_roleBasisVec, hrD]
    · apply ext_role
      intro r
      have hsrc (t : Role) : (v A • roleBasisVec D) t = if t = D then v A else 0 :=
        smul_roleBasisVec (v A) D t
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · have hvB : v B = 0 := hv B (by simp)
        have hvC : v C = 0 := hv C (by simp)
        have hvD : v D = 0 := hv D (by simp)
        simp [collapseS_A, hsrc, hvD]
      · simp [collapseS_C, hsrc, hv C (by simp)]
      · have hvD := hv D (by simp)
        simp [collapseS_D, hsrc, hvD]
      · simp [collapseS_B, hsrc, hv B (by simp)]

/-- Old vertical defect `M = S(ker B) = ℚ e_A`. -/
theorem collapse_verticalDefect : verticalDefect collapseB collapseS = lineA := by
  have hker : LinearMap.ker collapseB = lineD := by
    unfold LinearMap.ker
    exact comap_collapseB_bot
  unfold verticalDefect
  rw [hker, map_collapseS_lineD]

lemma comap_collapseB_lineA : Submodule.comap collapseB lineA = planeAD := by
  ext c
  constructor
  · intro hc r hr
    have hB : collapseB c B = 0 := by
      have := by simpa [Submodule.mem_comap] using hc
      exact this B (by simp)
    have hC : collapseB c C = 0 := by
      have := by simpa [Submodule.mem_comap] using hc
      exact this C (by simp)
    have hr' : r ≠ A ∧ r ≠ D := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · simpa [collapseB_C] using hC
    · exact absurd rfl hr'.2
    · simpa [collapseB_B] using hB
  · intro hc
    rw [Submodule.mem_comap]
    intro r hr
    have hrA : r ≠ A := by simpa using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hrA
    · simpa [collapseB_C] using hc C (by simp)
    · simp [collapseB_D]
    · simpa [collapseB_B] using hc B (by simp)

lemma map_collapseS_AD : planeAD.map collapseS = planeAB := by
  apply le_antisymm
  · intro v hv
    rcases hv with ⟨c, hc, rfl⟩
    have hB : c B = 0 := hc B (by simp)
    have hC : c C = 0 := hc C (by simp)
    intro r hr
    have hr' : r ≠ A ∧ r ≠ B := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · simp [collapseS_C, hB]
    · simp [collapseS_D, hC]
    · exact absurd rfl hr'.2
  · intro v hv
    refine ⟨v B • roleBasisVec A + v A • roleBasisVec D, ?_, ?_⟩
    · intro r hr
      have hr' : r ≠ A ∧ r ≠ D := by
        simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · exact absurd rfl hr'.1
      · simp [Pi.add_apply, smul_roleBasisVec, (by decide : C ≠ A), (by decide : C ≠ D)]
      · exact absurd rfl hr'.2
      · simp [Pi.add_apply, smul_roleBasisVec, (by decide : B ≠ A), (by decide : B ≠ D)]
    · apply ext_role
      intro r
      have hvC : v C = 0 := hv C (by simp)
      have hvDcoord : v D = 0 := hv D (by simp)
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · simp [collapseS_A, Pi.add_apply, smul_roleBasisVec, (by decide : A ≠ D)]
      · simp [collapseS_C, Pi.add_apply, smul_roleBasisVec, hvC,
          (by decide : C ≠ A), (by decide : C ≠ D)]
      · have hC : (v B • roleBasisVec A + v A • roleBasisVec D) C = 0 := by
          simp [Pi.add_apply, smul_roleBasisVec]
        simp [collapseS_D, hC, hvDcoord]
      · simp [collapseS_B, Pi.add_apply, smul_roleBasisVec]

lemma collapse_step_bot :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) ⊥ = lineA := by
  rw [collapse_unitStep, comap_collapseB_bot, map_collapseS_lineD, sup_eq_right.2 bot_le]

lemma collapse_step_lineA :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) lineA = planeAB := by
  rw [collapse_unitStep, comap_collapseB_lineA, map_collapseS_AD, sup_eq_right.2 lineA_le_plane]

lemma comap_collapseB_plane : Submodule.comap collapseB planeAB = spaceABD := by
  ext c
  constructor
  · intro hc r hr
    have hmem : collapseB c ∈ planeAB := by simpa [Submodule.mem_comap] using hc
    have hC : collapseB c C = 0 := hmem C (by simp)
    have hr' : r ≠ A ∧ r ≠ B ∧ r ≠ D := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · simpa [collapseB_C] using hC
    · exact absurd rfl hr'.2.2
    · exact absurd rfl hr'.2.1
  · intro hc
    rw [Submodule.mem_comap]
    intro r hr
    have hr' : r ≠ A ∧ r ≠ B := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · simpa [collapseB_C] using hc C (by simp)
    · simp [collapseB_D]
    · exact absurd rfl hr'.2

lemma map_collapseS_ABD : spaceABD.map collapseS = spaceABC := by
  apply le_antisymm
  · intro v hv
    rcases hv with ⟨c, hc, rfl⟩
    have hC : c C = 0 := hc C (by simp)
    intro r hr
    have hr' : r ≠ A ∧ r ≠ B ∧ r ≠ C := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · exact absurd rfl hr'.2.2
    · simp [collapseS_D, hC]
    · exact absurd rfl hr'.2.1
  · intro v hv
    refine ⟨v B • roleBasisVec A + v C • roleBasisVec B + v A • roleBasisVec D, ?_, ?_⟩
    · intro r hr
      have hr' : r ≠ A ∧ r ≠ B ∧ r ≠ D := by
        simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · exact absurd rfl hr'.1
      · simp [Pi.add_apply, smul_roleBasisVec, (by decide : C ≠ A), (by decide : C ≠ B),
          (by decide : C ≠ D)]
      · exact absurd rfl hr'.2.2
      · exact absurd rfl hr'.2.1
    · apply ext_role
      intro r
      have hvD : v D = 0 := hv D (by simp)
      rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
      · simp [collapseS_A, Pi.add_apply, smul_roleBasisVec, (by decide : A ≠ B),
          (by decide : A ≠ D)]
      · simp [collapseS_C, Pi.add_apply, smul_roleBasisVec, (by decide : C ≠ A),
          (by decide : C ≠ B), (by decide : C ≠ D)]
      · have hC : (v B • roleBasisVec A + v C • roleBasisVec B + v A • roleBasisVec D) C = 0 := by
          simp [Pi.add_apply, smul_roleBasisVec, (by decide : C ≠ A), (by decide : C ≠ B),
            (by decide : C ≠ D)]
        simp [collapseS_D, hC, hvD]
      · simp [collapseS_B, Pi.add_apply, smul_roleBasisVec, (by decide : B ≠ A),
          (by decide : B ≠ D)]

lemma collapse_step_plane :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) planeAB = spaceABC := by
  rw [collapse_unitStep, comap_collapseB_plane, map_collapseS_ABD, sup_eq_right.2 plane_le_space]

lemma comap_collapseB_space : Submodule.comap collapseB spaceABC = ⊤ := by
  ext c
  constructor
  · intro _ ; trivial
  · intro _
    rw [Submodule.mem_comap]
    intro r hr
    have hr' : r ≠ A ∧ r ≠ B ∧ r ≠ C := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · exact absurd rfl hr'.2.2
    · simp [collapseB_D]
    · exact absurd rfl hr'.2.1

lemma map_collapseS_top : (⊤ : Submodule ℚ RoleCoeff).map collapseS = ⊤ := by
  rw [eq_top_iff]
  intro v _
  refine ⟨(fun r =>
      if r = A then v B else if r = B then v C else if r = C then v D else v A), trivial, ?_⟩
  apply ext_role
  intro r
  rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
  · simp [collapseS_A, (by decide : D ≠ A), (by decide : D ≠ B), (by decide : D ≠ C)]
  · simp [collapseS_C, (by decide : B ≠ A), (by decide : B ≠ C)]
  · simp [collapseS_D, (by decide : C ≠ A), (by decide : C ≠ B)]
  · simp [collapseS_B]

lemma space_le_top : spaceABC ≤ ⊤ := le_top

lemma collapse_step_space :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) spaceABC = ⊤ := by
  rw [collapse_unitStep, comap_collapseB_space, map_collapseS_top, sup_eq_right.2 space_le_top]

private abbrev collapseIter (n : ℕ) : Submodule ℚ RoleCoeff :=
  saturationIter (fun _ : Unit => collapseB) (fun _ => collapseS) n ⊥

theorem collapse_iter_one : collapseIter 1 = lineA := by
  simp [collapseIter, collapse_step_bot]

theorem collapse_iter_two : collapseIter 2 = planeAB := by
  unfold collapseIter
  rw [show (2 : ℕ) = 1 + 1 from rfl, saturationIter_succ, saturationIter_succ,
    saturationIter_zero, collapse_step_bot, collapse_step_lineA]

theorem collapse_iter_three : collapseIter 3 = spaceABC := by
  unfold collapseIter
  rw [show (3 : ℕ) = 2 + 1 from rfl, saturationIter_succ]
  have h2 : saturationIter (fun _ : Unit => collapseB) (fun _ => collapseS) 2 ⊥ = planeAB := by
    simpa [collapseIter] using collapse_iter_two
  rw [h2]
  exact collapse_step_plane

theorem collapse_iter_four : collapseIter 4 = ⊤ := by
  unfold collapseIter
  rw [show (4 : ℕ) = 3 + 1 from rfl, saturationIter_succ]
  have h3 : saturationIter (fun _ : Unit => collapseB) (fun _ => collapseS) 3 ⊥ = spaceABC := by
    simpa [collapseIter] using collapse_iter_three
  rw [h3]
  exact collapse_step_space

theorem roleCoeff_finrank : finrank ℚ RoleCoeff = 4 := by
  rw [Module.finrank_fintype_fun_eq_card, card_role]

theorem collapse_spans :
    lineA = Submodule.span ℚ {roleBasisVec A} ∧
      planeAB = Submodule.span ℚ {roleBasisVec A, roleBasisVec B} ∧
      spaceABC = Submodule.span ℚ {roleBasisVec A, roleBasisVec B, roleBasisVec C} ∧
      (⊤ : Submodule ℚ RoleCoeff) =
        Submodule.span ℚ {roleBasisVec A, roleBasisVec B, roleBasisVec C, roleBasisVec D} := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simpa [lineA, Set.image_singleton] using (roleSpan_eq_supported {A}).symm
  · have : roleBasisVec '' ({A, B} : Set Role) = {roleBasisVec A, roleBasisVec B} := by
      ext v
      simp only [Set.mem_image, Set.mem_insert_iff, Set.mem_singleton_iff]
      constructor
      · rintro ⟨r, hr, rfl⟩
        rcases hr with rfl | rfl <;> simp
      · rintro (rfl | rfl)
        · exact ⟨A, Or.inl rfl, rfl⟩
        · exact ⟨B, Or.inr rfl, rfl⟩
    simpa [planeAB, this] using (roleSpan_eq_supported {A, B}).symm
  · have : roleBasisVec '' ({A, B, C} : Set Role) =
        {roleBasisVec A, roleBasisVec B, roleBasisVec C} := by
      ext v
      simp only [Set.mem_image, Set.mem_insert_iff, Set.mem_singleton_iff]
      constructor
      · rintro ⟨r, hr, rfl⟩
        rcases hr with rfl | rfl | rfl <;> simp
      · rintro (rfl | rfl | rfl)
        · exact ⟨A, Or.inl rfl, rfl⟩
        · exact ⟨B, Or.inr (Or.inl rfl), rfl⟩
        · exact ⟨C, Or.inr (Or.inr rfl), rfl⟩
    simpa [spaceABC, this] using (roleSpan_eq_supported {A, B, C}).symm
  · have htop : supported Set.univ = ⊤ := by
      ext v; simp [mem_supported]
    have himage : roleBasisVec '' (Set.univ : Set Role) =
        {roleBasisVec A, roleBasisVec B, roleBasisVec C, roleBasisVec D} := by
      ext v
      constructor
      · intro hv
        rcases hv with ⟨r, -, rfl⟩
        rcases role_eq_ACDB r with rfl | rfl | rfl | rfl <;> simp
      · intro hv
        simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hv
        rcases hv with rfl | rfl | rfl | rfl
        · exact ⟨A, trivial, rfl⟩
        · exact ⟨B, trivial, rfl⟩
        · exact ⟨C, trivial, rfl⟩
        · exact ⟨D, trivial, rfl⟩
    simpa [himage, htop] using (roleSpan_eq_supported (Set.univ : Set Role)).symm

/-- Quotient by the old vertical defect is not a same-fibre graph. -/
theorem verticalDefect_not_sameFibreGraph :
    ¬ SameFibreQuotientGraph lineA.mkQ collapseB collapseS := by
  intro h
  rw [sameFibreQuotientGraph_mkQ_iff] at h
  have hle : planeAB ≤ lineA := by
    rw [← collapse_step_lineA, collapse_unitStep]
    exact sup_le le_rfl h
  have heB : roleBasisVec B ∈ lineA := hle (by
    intro r hr
    have hrB : r ≠ B := by
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hr
      intro hB
      exact hr (Or.inr hB)
    simp [smul_roleBasisVec, if_neg hrB])
  have hB : roleBasisVec B B = 0 := heB B (by simp)
  simp [smul_roleBasisVec] at hB

/-- Any same-fibre kernel containing `M` is the whole fibre, so the quotient is zero. -/
theorem kernel_containing_verticalDefect_eq_top (W : Submodule ℚ RoleCoeff)
    (hM : lineA ≤ W)
    (hgraph : (Submodule.comap collapseB W).map collapseS ≤ W) :
    W = ⊤ := by
  have hplane : planeAB ≤ W := by
    rw [← collapse_step_lineA, collapse_unitStep]
    exact sup_le hM (le_trans (Submodule.map_mono (Submodule.comap_mono hM)) hgraph)
  have hspace : spaceABC ≤ W := by
    rw [← collapse_step_plane, collapse_unitStep]
    exact sup_le hplane (le_trans (Submodule.map_mono (Submodule.comap_mono hplane)) hgraph)
  have htop : ⊤ ≤ W := by
    rw [← collapse_step_space, collapse_unitStep]
    exact sup_le hspace (le_trans (Submodule.map_mono (Submodule.comap_mono hspace)) hgraph)
  exact le_antisymm le_top htop

theorem maximal_simultaneous_quotient_zero
    (x : RoleCoeff ⧸ (⊤ : Submodule ℚ RoleCoeff)) : x = 0 := by
  induction x using Submodule.Quotient.induction_on with
  | H v =>
      exact (Submodule.Quotient.mk_eq_zero _).2 Submodule.mem_top

/-! ## Nyquist: flat transport kills the live `e_A` response -/

def nyquistS : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c := (4 * c A) • roleBasisVec A
  map_add' := by
    intro x y
    ext r
    simp [add_mul, add_smul, Pi.add_apply, smul_roleBasisVec]
    split_ifs <;> ring
  map_smul' := by
    intro a x
    ext r
    simp [Pi.smul_apply, mul_assoc, mul_left_comm, mul_smul, smul_roleBasisVec]

theorem nyquist_step_bot :
    saturationStep (fun _ : Unit => (0 : RoleCoeff →ₗ[ℚ] RoleCoeff)) (fun _ => nyquistS) ⊥ =
      lineA := by
  have hker : Submodule.comap (0 : RoleCoeff →ₗ[ℚ] RoleCoeff) ⊥ = ⊤ := by
    ext c
    simp [Submodule.mem_comap, Submodule.mem_bot]
  rw [saturationStep, saturationSum, iSup_unique, hker]
  apply le_antisymm
  · refine sup_le bot_le ?_
    intro v hv
    rcases hv with ⟨c, -, rfl⟩
    intro r hr
    have hrA : r ≠ A := by simpa using hr
    simp [nyquistS, smul_roleBasisVec, if_neg hrA]
  · intro v hv
    refine (le_sup_right : (⊤ : Submodule ℚ RoleCoeff).map nyquistS ≤
        ⊥ ⊔ (⊤ : Submodule ℚ RoleCoeff).map nyquistS) ?_
    refine ⟨(v A / 4) • roleBasisVec A, trivial, ?_⟩
    apply ext_role
    intro r
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · have hvB : v B = 0 := hv B (by simp)
      have hvC : v C = 0 := hv C (by simp)
      have hvD : v D = 0 := hv D (by simp)
      simp [nyquistS, smul_roleBasisVec, hvB, hvC, hvD]
    · simp [nyquistS, smul_roleBasisVec, hv C (by simp)]
    · simp [nyquistS, smul_roleBasisVec, hv D (by simp)]
    · simp [nyquistS, smul_roleBasisVec, hv B (by simp)]

theorem nyquist_kills_four_eA :
    (4 : ℚ) • roleBasisVec A ∈ lineA ∧ roleBasisVec B ∉ lineA := by
  refine ⟨?_, ?_⟩
  · intro r hr
    have hrA : r ≠ A := by simpa using hr
    simp [smul_roleBasisVec, if_neg hrA]
  · intro h
    have := h B (by simp)
    simp [smul_roleBasisVec] at this

theorem nyquist_response_is_four_eA :
    nyquistS (roleBasisVec A) = (4 : ℚ) • roleBasisVec A := by
  ext r
  simp [nyquistS, smul_roleBasisVec]

/-! ## Boost coinvariant is the A/B plane -/

def boostL : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c :=
    ((5 / 3 : ℚ) * c A + (4 / 3) * c B) • roleBasisVec A +
    ((4 / 3 : ℚ) * c A + (5 / 3) * c B) • roleBasisVec B +
    c C • roleBasisVec C + c D • roleBasisVec D
  map_add' := by
    intro x y; ext r
    simp [add_mul, add_smul, Pi.add_apply, smul_roleBasisVec]; split_ifs <;> ring
  map_smul' := by
    intro a x; ext r
    simp [Pi.smul_apply, mul_add, mul_assoc, mul_left_comm, mul_smul, smul_roleBasisVec]

def boostInvL : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c :=
    ((5 / 3 : ℚ) * c A + (-4 / 3) * c B) • roleBasisVec A +
    ((-4 / 3 : ℚ) * c A + (5 / 3) * c B) • roleBasisVec B +
    c C • roleBasisVec C + c D • roleBasisVec D
  map_add' := by
    intro x y; ext r
    simp [add_mul, add_smul, Pi.add_apply, smul_roleBasisVec]; split_ifs <;> ring
  map_smul' := by
    intro a x; ext r
    simp [Pi.smul_apply, mul_add, mul_assoc, mul_left_comm, mul_smul, smul_roleBasisVec]

lemma boost_left_inv : boostL.comp boostInvL = LinearMap.id := by
  apply LinearMap.ext
  intro v
  ext r
  rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]; ring
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
    generalize a : v A = a
    generalize b : v B = b
    ring

lemma boost_right_inv : boostInvL.comp boostL = LinearMap.id := by
  apply LinearMap.ext
  intro v
  ext r
  rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]; ring
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
  · simp [LinearMap.comp_apply, LinearMap.id_apply, boostL, boostInvL, Pi.add_apply,
      smul_roleBasisVec, div_eq_mul_inv]
    generalize a : v A = a
    generalize b : v B = b
    ring

def boost : RoleCoeff ≃ₗ[ℚ] RoleCoeff :=
  LinearEquiv.ofLinear boostL boostInvL boost_left_inv boost_right_inv

theorem boost_coinvariant_eq_plane :
    coinvariantImage boost = planeAB := by
  apply le_antisymm
  · intro v hv
    rcases hv with ⟨c, rfl⟩
    rw [loopDeviation_apply]
    intro r hr
    have hr' : r ≠ A ∧ r ≠ B := by
      simpa [Set.mem_insert_iff, Set.mem_singleton_iff] using hr
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · exact absurd rfl hr'.1
    · simp [boost, boostL, Pi.add_apply, smul_roleBasisVec]
    · simp [boost, boostL, Pi.add_apply, smul_roleBasisVec]
    · exact absurd rfl hr'.2
  · intro v hv
    let u : RoleCoeff := (-(1 / 2 : ℚ) * v A + v B) • roleBasisVec A +
      (v A + -(1 / 2 : ℚ) * v B) • roleBasisVec B
    -- `u` is chosen so `(boost - I) u = v` on the A/B plane. Checked by coordinates.
    refine ⟨u, ?_⟩
    rw [loopDeviation_apply]
    apply ext_role
    intro r
    have hvC : v C = 0 := hv C (by simp)
    have hvD : v D = 0 := hv D (by simp)
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · simp [u, boost, boostL, Pi.add_apply, smul_roleBasisVec, hvC, hvD]; ring
    · simp [u, boost, boostL, Pi.add_apply, smul_roleBasisVec, hvC, hvD]
    · simp [u, boost, boostL, Pi.add_apply, smul_roleBasisVec, hvC, hvD]
    · simp [u, boost, boostL, Pi.add_apply, smul_roleBasisVec, hvC, hvD]; ring

/-! ## Both parallel loops must be retained -/

def shearL : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c := c + (c A) • roleBasisVec B
  map_add' := by
    intro x y
    ext r
    simp [Pi.add_apply, add_smul, smul_roleBasisVec]; split_ifs <;> ring
  map_smul' := by
    intro a x
    ext r
    simp [Pi.smul_apply, mul_smul, smul_add, smul_roleBasisVec]; split_ifs <;> ring

def shearInvL : RoleCoeff →ₗ[ℚ] RoleCoeff where
  toFun c := c - (c A) • roleBasisVec B
  map_add' := by
    intro x y
    ext r
    simp [Pi.add_apply, Pi.sub_apply, add_smul, sub_eq_add_neg, smul_roleBasisVec];
      split_ifs <;> ring
  map_smul' := by
    intro a x
    ext r
    simp [Pi.smul_apply, Pi.sub_apply, mul_smul, smul_sub, smul_roleBasisVec];
      split_ifs <;> ring

lemma shear_left_inv : shearL.comp shearInvL = LinearMap.id := by
  ext v r
  simp [LinearMap.comp_apply, LinearMap.id_apply, shearL, shearInvL, Pi.add_apply,
    Pi.sub_apply, smul_roleBasisVec]

lemma shear_right_inv : shearInvL.comp shearL = LinearMap.id := by
  ext v r
  simp [LinearMap.comp_apply, LinearMap.id_apply, shearL, shearInvL, Pi.add_apply,
    Pi.sub_apply, smul_roleBasisVec]

def shear : RoleCoeff ≃ₗ[ℚ] RoleCoeff :=
  LinearEquiv.ofLinear shearL shearInvL shear_left_inv shear_right_inv

def parallelLoops : Bool → RoleCoeff ≃ₗ[ℚ] RoleCoeff
  | false => LinearEquiv.refl ℚ RoleCoeff
  | true => shear

theorem shear_coinvariant_eq_lineB : coinvariantImage shear = lineB := by
  apply le_antisymm
  · intro v hv
    rcases hv with ⟨c, rfl⟩
    rw [loopDeviation_apply]
    intro r hr
    have hrB : r ≠ B := by simpa using hr
    simp [shear, shearL, Pi.add_apply, smul_roleBasisVec, if_neg hrB]
  · intro v hv
    refine ⟨v B • roleBasisVec A, ?_⟩
    rw [loopDeviation_apply]
    apply ext_role
    intro r
    rcases role_eq_ACDB r with rfl | rfl | rfl | rfl
    · have hvA : v A = 0 := hv A (by simp)
      simp [shear, shearL, Pi.add_apply, smul_roleBasisVec, hvA]
    · simp [shear, shearL, Pi.add_apply, smul_roleBasisVec, hv C (by simp)]
    · simp [shear, shearL, Pi.add_apply, smul_roleBasisVec, hv D (by simp)]
    · simp [shear, shearL, Pi.add_apply, smul_roleBasisVec]

theorem dropped_parallel_edge_shrinks :
    coinvariantImage (parallelLoops false) = ⊥ ∧
      coinvariantImage (parallelLoops true) = lineB ∧
      lineB ≠ ⊥ := by
  refine ⟨coinvariantImage_refl, shear_coinvariant_eq_lineB, ?_⟩
  intro h
  have hmem : roleBasisVec B ∈ lineB := by
    intro r hr
    have hrB : r ≠ B := by simpa using hr
    simp [smul_roleBasisVec, if_neg hrB]
  have hzero : roleBasisVec B = 0 := by simpa [h] using hmem
  have := congrFun hzero B
  simp [smul_roleBasisVec] at this

/-- The zero quotient is always a fixed point. It does not select a classical fibre. -/
theorem zero_quotient_always_fixed :
    saturationStep (fun _ : Unit => collapseB) (fun _ => collapseS) ⊤ = ⊤ :=
  top_saturationStep _ _

#print axioms sameFibreQuotientGraph_mkQ_iff
#print axioms coinvariant_le_iff_quotient_id
#print axioms saturation_minimal_fixedPoint
#print axioms collapse_iter_four
#print axioms verticalDefect_not_sameFibreGraph
#print axioms kernel_containing_verticalDefect_eq_top
#print axioms nyquist_kills_four_eA
#print axioms boost_coinvariant_eq_plane
#print axioms dropped_parallel_edge_shrinks

end

end D0.Geometry
