import D0.Algebra.GrowingClockFrame

/-!
# Orthogonal clock frames from genuine distinct stage carriers

For finite, possibly differently sized stages `H j`, the sigma type is the
coordinate carrier of their orthogonal direct sum. An isometric initial frame
`V` transported by each isometry `A j` gives the `J j` consumed by the clock
factorization. This construction does not build the owner's actual stages,
`A j`, or clock, and does not establish any physical admission. To identify
this projector with the owner's cut additionally requires `P₀ = V Vᴴ` and
the specified owner transport; neither is assumed to follow from the frame.
Owner: #334 `afd99daf54d26ef7e1b47a94f380557213e9c6d5`,
`GROWING_CLOCK_RU.md` §§1–3, blob `370e8fb572e85fedeebe2e72531c01d5b68b0a91`.
-/
open scoped BigOperators Matrix
open Matrix
namespace D0.Algebra.GrowingClockFrame
variable {n : ℕ} {H : Fin (n+1) → Type*} [∀ j, Fintype (H j)]
variable {r : Type*} [Fintype r] [DecidableEq r]
noncomputable def stageFrame (A : ∀ j, Matrix (H j) r ℂ) (j : Fin (n+1)) : Matrix (Σ k, H k) r ℂ :=
  fun x v => if h : x.1 = j then A j (h ▸ x.2) v else 0

omit [Fintype r] in
theorem stageFrame_orthogonal (A : ∀ j, Matrix (H j) r ℂ)
    (hA : ∀ j, (A j)ᴴ * A j = 1) :
    ∀ i j, (stageFrame A i)ᴴ * stageFrame A j = if i = j then 1 else 0 := by
  intro i j
  classical
  ext a b
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, stageFrame]
  rw [Fintype.sum_sigma]
  by_cases h : i = j
  · subst j
    have hh := congrArg (fun M : Matrix r r ℂ => M a b) (hA i)
    simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.one_apply] at hh
    simpa using hh
  · simp only [h, ↓reduceIte, Matrix.zero_apply]
    apply Finset.sum_eq_zero
    intro k hk
    apply Finset.sum_eq_zero
    intro x hx
    by_cases hi : k = i <;> by_cases hj : k = j <;> simp_all

variable {h0 : Type*} [Fintype h0] [DecidableEq h0]

omit [Fintype r] in
/-- A transported initial frame is an isometry on each stage. -/
theorem transported_isometry (A : ∀ j, Matrix (H j) h0 ℂ)
    (V : Matrix h0 r ℂ) (hA : ∀ j, (A j)ᴴ * A j = 1)
    (hV : Vᴴ * V = 1) (j : Fin (n+1)) :
    (A j * V)ᴴ * (A j * V) = 1 := by
  simp only [Matrix.conjTranspose_mul, Matrix.mul_assoc]
  rw [← Matrix.mul_assoc (A j)ᴴ (A j) V, hA j, Matrix.one_mul, hV]

/-- The derived frames directly supply the hypothesis of the existing clock theorem. -/
theorem stage_clock_determinant [∀ j, DecidableEq (H j)]
    (A : ∀ j, Matrix (H j) h0 ℂ) (V : Matrix h0 r ℂ)
    (hA : ∀ j, (A j)ᴴ * A j = 1) (hV : Vᴴ * V = 1)
    (T : Matrix (Σ j, H j) (Σ j, H j) ℂ) (hT : Tᴴ * T = 1)
    (hstep : ∀ j : Fin n,
      T * stageFrame (fun k => A k * V) j.castSucc =
        stageFrame (fun k => A k * V) j.succ) (z : ℂ) :
    let J := stageFrame (fun k => A k * V)
    let P := frameProjector J
    let C := frameReturn J T
    (1 - z • ((D0.Algebra.MovingProjectorTransport.cut P T)ᴴ *
      D0.Algebra.MovingProjectorTransport.cut P T)).det =
      ((1 - z) • (1 : Matrix r r ℂ) + z • (Cᴴ * C)).det := by
  classical
  exact clock_cut_determinant _
    (stageFrame_orthogonal _ (transported_isometry A V hA hV)) T hT hstep z

/-- A non-isometric zero frame does not satisfy even the diagonal condition. -/
example :
    ¬ (stageFrame (H := fun _ : Fin 1 => Fin 1)
        (fun _ => (0 : Matrix (Fin 1) (Fin 1) ℂ)) 0)ᴴ *
      stageFrame (H := fun _ : Fin 1 => Fin 1)
        (fun _ => (0 : Matrix (Fin 1) (Fin 1) ℂ)) 0 = 1 := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 1) (Fin 1) ℂ => M 0 0) h
  norm_num [stageFrame, Matrix.mul_apply, Matrix.conjTranspose_apply] at hh

end D0.Algebra.GrowingClockFrame
