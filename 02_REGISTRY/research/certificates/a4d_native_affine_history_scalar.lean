import D0.Geometry.ArchiveAffineCartanConnection
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-! The complete total-transport scalar interface on the actual affine path
owner. A scalar depends only on total affine transport and respects every
native concatenation. These hypotheses are explicit, not physical postulates. -/
namespace D0.Research.NativeAffineHistoryScalar
open D0 D0.Geometry
noncomputable section
variable {V : Type*} [AddCommGroup V] [Module ℝ V]
abbrev Aff := AffineCartanMap ℝ V

structure Character (V : Type*) [AddCommGroup V] [Module ℝ V] where
  value : Aff (V := V) → ℝ
  additive : ∀ a b, value (a*b)=value a+value b

namespace Character
variable (C : Character V)
theorem identity : C.value 1=0 := by
  have h := C.additive 1 1
  simp only [AffineCartanMap.affine_one_mul] at h
  linarith

theorem inverse (a : Aff (V := V)) : C.value a⁻¹= -C.value a := by
  have h := C.additive a a⁻¹
  rw [AffineCartanMap.affine_mul_inv,C.identity] at h
  linarith

theorem conjugation (a b : Aff (V := V)) : C.value (a*b*a⁻¹)=C.value b := by
  rw [C.additive,C.additive,C.inverse]
  ring

theorem conjugate_inverse_zero (a b : Aff (V := V))
    (h : a*b*a⁻¹=b⁻¹) : C.value b=0 := by
  have hc := C.conjugation a b
  rw [h,C.inverse] at hc
  linarith

theorem finite_order_zero (a : Aff (V := V))
    (h : a*a=1) : C.value a=0 := by
  have hc := C.additive a a
  rw [h,C.identity] at hc
  linarith
end Character

def translation (v : V) : Aff (V := V) :=
  ⟨LinearEquiv.refl ℝ V,v⟩
def linearPart (a : Aff (V := V)) : Aff (V := V) := ⟨a.lin,0⟩

def doubleLinear : V ≃ₗ[ℝ] V where
  toFun v := (2:ℝ) • v
  invFun v := (1/2:ℝ) • v
  left_inv v := by simp [smul_smul]
  right_inv v := by simp [smul_smul]
  map_add' _ _ := smul_add _ _ _
  map_smul' _ _ := by simp [smul_smul,mul_comm]

def dilation : Aff (V := V) := ⟨doubleLinear,0⟩

theorem translation_add (v w : V) : translation (v+w)=translation v*translation w := by
  ext <;> simp [translation,AffineCartanMap.mul_lin,AffineCartanMap.mul_shift]

theorem dilation_translation (v : V) :
    dilation*translation v*dilation⁻¹=translation (v+v) := by
  ext
  · simp [dilation,translation,AffineCartanMap.mul_lin,AffineCartanMap.inv_lin]
  · simp [dilation,translation,AffineCartanMap.mul_shift,AffineCartanMap.inv_shift,
      doubleLinear,two_smul]

theorem translation_killed (C : Character V) (v : V) : C.value (translation v)=0 := by
  have h := C.conjugation dilation (translation v)
  rw [dilation_translation,translation_add,C.additive] at h
  linarith

theorem affine_factorization (a : Aff (V := V)) :
    a=translation a.shift*linearPart a := by
  ext <;> simp [translation,linearPart,AffineCartanMap.mul_lin,AffineCartanMap.mul_shift]

theorem character_shift_blind (C : Character V) (a : Aff (V := V)) :
    C.value a=C.value (linearPart a) := by
  calc
    C.value a=C.value (translation a.shift*linearPart a) := congrArg C.value (affine_factorization a)
    _ = C.value (linearPart a) := by rw [C.additive,translation_killed]; ring

theorem same_linear_same_scalar (C : Character V) (a b : Aff (V := V))
    (h : a.lin=b.lin) : C.value a=C.value b := by
  rw [character_shift_blind C a,character_shift_blind C b]
  congr 1
  exact AffineCartanMap.ext h rfl

theorem native_path_additive (C : Character V) {N : ℕ}
    (A : AffineCartanConnection N ℝ V) (p q : List ChainStep)
    (x : ArchiveRolePhaseGroup N) :
    C.value (affinePath A (p++q) x)=C.value (affinePath A p x)+
      C.value (affinePath A q (pathEnd N p x)) := by
  rw [affinePath_append,C.additive]

theorem native_reverse_negates (C : Character V) {N : ℕ}
    (A : AffineCartanConnection N ℝ V) (p : List ChainStep)
    (x : ArchiveRolePhaseGroup N) :
    C.value (affinePath A (p.map reverseStep).reverse (pathEnd N p x))=
      -C.value (affinePath A p x) := by
  rw [affinePath_reverse,C.inverse]

theorem no_positive_reverse_pair (C : Character V) (a : Aff (V := V)) :
    ¬ (1≤C.value a ∧ 1≤C.value a⁻¹) := by
  rw [C.inverse]
  intro h
  linarith [h.1,h.2]

theorem native_gauge_boundary (C : Character V) {N : ℕ}
    (h : AffineNodeGauge N ℝ V) (A : AffineCartanConnection N ℝ V)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    C.value (affinePath (affineGauge h A) p x)=
      C.value (affinePath A p x)+C.value (h x)-C.value (h (pathEnd N p x)) := by
  rw [affinePath_gauge,C.additive,C.additive,C.inverse]
  ring

theorem closed_path_gauge_invariant (C : Character V) {N : ℕ}
    (h : AffineNodeGauge N ℝ V) (A : AffineCartanConnection N ℝ V)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) (hp : pathEnd N p x=x) :
    C.value (affinePath (affineGauge h A) p x)=C.value (affinePath A p x) := by
  rw [native_gauge_boundary,hp]
  ring

theorem native_path_linear_congr {N : ℕ}
    (A B : AffineCartanConnection N ℝ V) (h : ∀ x r, (A x r).lin=(B x r).lin)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    (affinePath A p x).lin=(affinePath B p x).lin := by
  induction p generalizing x with
  | nil => rfl
  | cons s rest ih =>
    simp only [affinePath,AffineCartanMap.mul_lin,ih]
    congr 1
    cases s with
    | fwd r => exact h x r
    | bwd r => simp only [affineStepMap,AffineCartanMap.inv_lin,h]

theorem all_raw_shift_variations_invisible (C : Character V) {N : ℕ}
    (A B : AffineCartanConnection N ℝ V) (h : ∀ x r, (A x r).lin=(B x r).lin)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    C.value (affinePath A p x)=C.value (affinePath B p x) :=
  same_linear_same_scalar C _ _ (native_path_linear_congr A B h p x)

theorem two_free_native_edges {N : ℕ} (r s : Role) (hrs : r≠s)
    (x : ArchiveRolePhaseGroup N) (a b : Aff (V := V)) :
    ∃ A : AffineCartanConnection N ℝ V,
      affinePath A [ChainStep.fwd r] x=a ∧
      affinePath A [ChainStep.fwd s] (stepTarget N (.fwd r) x)=b ∧
      affinePath A [ChainStep.fwd r,ChainStep.fwd s] x=a*b := by
  let A : AffineCartanConnection N ℝ V := fun y t =>
    if y=x ∧ t=r then a
    else if y=roleTranslatePlus N r x ∧ t=s then b else 1
  have ha : A x r=a := by simp [A]
  have hb : A (roleTranslatePlus N r x) s=b := by simp [A,Ne.symm hrs]
  refine ⟨A,?_,?_,?_⟩ <;>
    simp [affinePath,affineStepMap,stepTarget,ha,hb,AffineCartanMap.affine_mul_one]

/-- No character law is imported: it follows by realizing two arbitrary
affine maps as two independently stored native links. -/
theorem native_additivity_forces_character {N : ℕ} (f : Aff (V := V) → ℝ)
    (h : ∀ (A : AffineCartanConnection N ℝ V) p q x,
      f (affinePath A (p++q) x)=f (affinePath A p x)+
        f (affinePath A q (pathEnd N p x))) :
    ∀ a b, f (a*b)=f a+f b := by
  intro a b
  let r : Role := (0,0)
  let s : Role := (0,1)
  let x : ArchiveRolePhaseGroup N := fun _ => 0
  obtain ⟨A,ha,hb,hab⟩ := two_free_native_edges r s (by decide) x a b
  have hh := h A [ChainStep.fwd r] [ChainStep.fwd s] x
  simpa only [List.cons_append,List.nil_append,pathEnd_cons,pathEnd_nil,ha,hb,hab] using hh

theorem complete_native_scalar_class {N : ℕ} (f : Aff (V := V) → ℝ) :
    (∀ (A : AffineCartanConnection N ℝ V) p q x,
      f (affinePath A (p++q) x)=f (affinePath A p x)+
        f (affinePath A q (pathEnd N p x))) ↔
      (∀ a b, f (a*b)=f a+f b) := by
  constructor
  · exact native_additivity_forces_character f
  · intro h A p q x
    rw [affinePath_append,h]

end
end D0.Research.NativeAffineHistoryScalar

#print axioms D0.Research.NativeAffineHistoryScalar.Character.identity
#print axioms D0.Research.NativeAffineHistoryScalar.Character.inverse
#print axioms D0.Research.NativeAffineHistoryScalar.Character.conjugation
#print axioms D0.Research.NativeAffineHistoryScalar.Character.conjugate_inverse_zero
#print axioms D0.Research.NativeAffineHistoryScalar.Character.finite_order_zero
#print axioms D0.Research.NativeAffineHistoryScalar.translation_add
#print axioms D0.Research.NativeAffineHistoryScalar.dilation_translation
#print axioms D0.Research.NativeAffineHistoryScalar.translation_killed
#print axioms D0.Research.NativeAffineHistoryScalar.affine_factorization
#print axioms D0.Research.NativeAffineHistoryScalar.character_shift_blind
#print axioms D0.Research.NativeAffineHistoryScalar.same_linear_same_scalar
#print axioms D0.Research.NativeAffineHistoryScalar.native_path_additive
#print axioms D0.Research.NativeAffineHistoryScalar.native_reverse_negates
#print axioms D0.Research.NativeAffineHistoryScalar.no_positive_reverse_pair
#print axioms D0.Research.NativeAffineHistoryScalar.native_gauge_boundary
#print axioms D0.Research.NativeAffineHistoryScalar.closed_path_gauge_invariant
#print axioms D0.Research.NativeAffineHistoryScalar.native_path_linear_congr
#print axioms D0.Research.NativeAffineHistoryScalar.all_raw_shift_variations_invisible
#print axioms D0.Research.NativeAffineHistoryScalar.two_free_native_edges
#print axioms D0.Research.NativeAffineHistoryScalar.native_additivity_forces_character
#print axioms D0.Research.NativeAffineHistoryScalar.complete_native_scalar_class
