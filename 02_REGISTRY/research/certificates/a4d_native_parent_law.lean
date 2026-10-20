import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import D0.Geometry.FinitePrimalDualHodgeParent
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DStarFiniteLorentzQuotient

/-! Complete supplied-parent interface. No physical action/seed is selected. -/
namespace D0.Research.NativeParentLaw
open D0.Geometry
open scoped BigOperators Topology
noncomputable section
set_option linter.unusedSectionVars false
variable {n : Type*} [Fintype n]
abbrev End (n : Type*) := (n → ℝ) →ₗ[ℝ] (n → ℝ)
def pair (x y : n → ℝ) : ℝ := ∑ i, x i*y i
def action (M K : End n) (p c l : n → ℝ) : ℝ :=
  (1/2:ℝ)*pair c (M c)+pair l (M c-K p)

private lemma pair_add_left (x y z : n → ℝ) : pair (x+y) z=pair x z+pair y z := by
  simp [pair,add_mul,Finset.sum_add_distrib]
private lemma pair_add_right (x y z : n → ℝ) : pair x (y+z)=pair x y+pair x z := by
  simp [pair,mul_add,Finset.sum_add_distrib]
private lemma pair_sub_right (x y z : n → ℝ) : pair x (y-z)=pair x y-pair x z := by
  simp [pair,mul_sub,Finset.sum_sub_distrib]
private lemma pair_smul_left (t : ℝ) (x y : n → ℝ) : pair (t • x) y=t*pair x y := by
  simp [pair,Finset.mul_sum,mul_assoc]
private lemma pair_smul_right (t : ℝ) (x y : n → ℝ) : pair x (t • y)=t*pair x y := by
  simp [pair,Finset.mul_sum,mul_left_comm]
private lemma pair_nondegenerate (x : n → ℝ) (h : ∀ v, pair v x=0) : x=0 := by
  have hh := h x
  funext i
  have hi := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => mul_self_nonneg (x i))).mp hh i
    (Finset.mem_univ i)
  exact mul_self_eq_zero.mp hi

theorem literal_owner_binding {p q r : Type*} [Fintype p] [Fintype q] [Fintype r]
    (A : FinitePrimalDualHodgeData n p q r)
    (R : (r → ℝ) →ₗ[ℝ] (n → ℝ)) (ψ χ lm : n → ℝ) :
    mixedPrimalDualAction (fun x y => pair x (R y)) A ψ χ lm =
      action (R.comp A.star0) (R.comp (A.dD.comp (A.star1.comp A.dP))) ψ χ lm := by
  simp [mixedPrimalDualAction,mixedCodifferentialConstraint,action,map_sub]

def data (M K : End n) : FinitePrimalDualHodgeData n n n n where
  dP := LinearMap.id
  dD := LinearMap.id
  star0 := M
  star1 := K

theorem every_visible_pair_is_an_owner_input (M K : End n) (p c l : n → ℝ) :
    mixedPrimalDualAction pair (data M K) p c l=action M K p c l := by
  simp [mixedPrimalDualAction,mixedCodifferentialConstraint,data,action]

theorem visible_coefficients_identifiable (M K A B : End n) :
    (∀ p c l, action M K p c l=action A B p c l) ↔ M=A ∧ K=B := by
  constructor
  · intro h
    have hK : K=B := by
      apply LinearMap.ext
      intro p
      apply sub_eq_zero.mp
      apply pair_nondegenerate
      intro l
      have hh : -pair l (K p) = -pair l (B p) := by
        simpa [action,pair] using h p 0 l
      have hb := neg_injective hh
      simpa [pair_sub_right,sub_eq_zero] using hb
    have hM : M=A := by
      apply LinearMap.ext
      intro c
      apply sub_eq_zero.mp
      apply pair_nondegenerate
      intro l
      have hb : pair l (M c)=pair l (A c) := by
        have hh := h 0 c l
        have hz := h 0 c 0
        simp [action,pair] at hh hz ⊢
        linarith
      simpa [pair_sub_right,sub_eq_zero] using hb
    exact ⟨hM,hK⟩
  · rintro ⟨rfl,rfl⟩;simp

def fieldVariation (K : End n) (l v : n → ℝ) : ℝ := -pair l (K v)
def auxiliaryVariation (M : End n) (c l v : n → ℝ) : ℝ :=
  (1/2:ℝ)*(pair v (M c)+pair c (M v))+pair l (M v)
def multiplierVariation (M K : End n) (p c v : n → ℝ) : ℝ := pair v (M c-K p)

theorem field_exact_variation (M K : End n) (p c l v : n → ℝ) (t : ℝ) :
    action M K (p+t • v) c l=action M K p c l+t*fieldVariation K l v := by
  simp only [action,fieldVariation,map_add,map_smul,pair_sub_right,pair_add_right,pair_smul_right]
  ring
theorem auxiliary_exact_variation (M K : End n) (p c l v : n → ℝ) (t : ℝ) :
    action M K p (c+t • v) l=action M K p c l+t*auxiliaryVariation M c l v+
      (t^2/2)*pair v (M v) := by
  simp only [action,auxiliaryVariation,map_add,map_smul,pair_sub_right,pair_add_left,
    pair_add_right,pair_smul_left,pair_smul_right]
  ring
theorem multiplier_exact_variation (M K : End n) (p c l v : n → ℝ) (t : ℝ) :
    action M K p c (l+t • v)=action M K p c l+t*multiplierVariation M K p c v := by
  simp only [action,multiplierVariation,pair_add_left,pair_smul_left]
  ring

theorem field_hasDerivAt (M K : End n) (p c l v : n → ℝ) :
    HasDerivAt (fun t : ℝ => action M K (p+t • v) c l) (fieldVariation K l v) 0 := by
  simp_rw [field_exact_variation]
  convert (hasDerivAt_const (0:ℝ) (action M K p c l)).add
    ((hasDerivAt_id (0:ℝ)).mul_const (fieldVariation K l v)) using 1; simp
theorem auxiliary_hasDerivAt (M K : End n) (p c l v : n → ℝ) :
    HasDerivAt (fun t : ℝ => action M K p (c+t • v) l) (auxiliaryVariation M c l v) 0 := by
  simp_rw [auxiliary_exact_variation]
  convert ((hasDerivAt_const (0:ℝ) (action M K p c l)).add
    ((hasDerivAt_id (0:ℝ)).mul_const (auxiliaryVariation M c l v))).add
    ((((hasDerivAt_id (0:ℝ)).pow 2).div_const 2).mul_const (pair v (M v))) using 1;
    simp [id]
theorem multiplier_hasDerivAt (M K : End n) (p c l v : n → ℝ) :
    HasDerivAt (fun t : ℝ => action M K p c (l+t • v)) (multiplierVariation M K p c v) 0 := by
  simp_rw [multiplier_exact_variation]
  convert (hasDerivAt_const (0:ℝ) (action M K p c l)).add
    ((hasDerivAt_id (0:ℝ)).mul_const (multiplierVariation M K p c v)) using 1; simp

def FullFieldGate (M K : End n) (p c l : n → ℝ) : Prop :=
  (∀ v, deriv (fun t : ℝ => action M K (p+t • v) c l) 0=0) ∧
  (∀ v, deriv (fun t : ℝ => action M K p (c+t • v) l) 0=0) ∧
  (∀ v, deriv (fun t : ℝ => action M K p c (l+t • v)) 0=0)

theorem genuine_gate_equations (M K : End n) (p c l : n → ℝ) :
    FullFieldGate M K p c l ↔
      (∀ v, pair l (K v)=0) ∧ (∀ v, auxiliaryVariation M c l v=0) ∧ M c=K p := by
  simp only [FullFieldGate,(field_hasDerivAt M K p c l _).deriv,
    (auxiliary_hasDerivAt M K p c l _).deriv,
    (multiplier_hasDerivAt M K p c l _).deriv,fieldVariation,multiplierVariation,neg_eq_zero]
  constructor
  · rintro ⟨hp,hc,hl⟩
    exact ⟨hp,hc,sub_eq_zero.mp (pair_nondegenerate _ hl)⟩
  · rintro ⟨hp,hc,hl⟩
    refine ⟨hp,hc,?_⟩
    intro v;simp [hl,pair]

def response (U V : End n) (p c l : n → ℝ) : ℝ :=
  (1/2:ℝ)*pair c (U c)+pair l (U c-V p)
theorem source_exact_variation (M K U V : End n) (p c l : n → ℝ) (t : ℝ) :
    action (M+t • U) (K+t • V) p c l=action M K p c l+t*response U V p c l := by
  simp only [action,response,LinearMap.add_apply,LinearMap.smul_apply,
    pair_sub_right,pair_add_right,pair_smul_right]
  ring
theorem source_hasDerivAt (M K U V : End n) (p c l : n → ℝ) :
    HasDerivAt (fun t : ℝ => action (M+t • U) (K+t • V) p c l) (response U V p c l) 0 := by
  simp_rw [source_exact_variation]
  convert (hasDerivAt_const (0:ℝ) (action M K p c l)).add
    ((hasDerivAt_id (0:ℝ)).mul_const (response U V p c l)) using 1; simp

def Symmetric (B : End n) : Prop := ∀ x y, pair x (B y)=pair y (B x)
theorem diagonal_iff_full_restriction (N : Submodule ℝ (n → ℝ)) (B : End n)
    (hB : Symmetric B) :
    (∀ x∈N,pair x (B x)=0) ↔ (∀ x∈N,∀ y∈N,pair x (B y)=0) := by
  constructor
  · intro h x hx y hy
    have hh := h (x+y) (N.add_mem hx hy)
    simp only [map_add,pair_add_left,pair_add_right] at hh
    rw [h x hx,h y hy,hB y x] at hh
    linarith
  · intro h x hx;exact h x hx x hx

theorem kernel_and_source_comparison (H1 H2 W1 W2 : End n)
    (hW : Symmetric (W2-W1)) :
    ((∀ z,H1 z=0 ↔ H2 z=0) ∧
      (∀ z,H1 z=0 → pair z (W2 z)=pair z (W1 z))) ↔
    (LinearMap.ker H1=LinearMap.ker H2 ∧
      ∀ x∈LinearMap.ker H1,∀ y∈LinearMap.ker H1,pair x ((W2-W1) y)=0) := by
  have hk : (∀ z,H1 z=0 ↔ H2 z=0) ↔ LinearMap.ker H1=LinearMap.ker H2 := by
    constructor
    · intro h;ext z;exact h z
    · intro h z;change z∈LinearMap.ker H1 ↔ z∈LinearMap.ker H2;rw [h]
  rw [hk]
  have hd : (∀ z,H1 z=0 → pair z (W2 z)=pair z (W1 z)) ↔
      ∀ z∈LinearMap.ker H1,pair z ((W2-W1) z)=0 := by
    simp only [LinearMap.mem_ker,LinearMap.sub_apply,pair_sub_right,sub_eq_zero]
  rw [hd,diagonal_iff_full_restriction _ _ hW]

private lemma pair_self_zero (x : n → ℝ) (h : pair x x=0) : x=0 := by
  funext i
  have hi := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => mul_self_nonneg (x i))).mp h i
    (Finset.mem_univ i)
  exact mul_self_eq_zero.mp hi

/-- Full joint equations of the displayed paired native seed family. The
background equation is the computed action derivative, not an Einstein gate. -/
theorem full_joint_block_classification (a theta : ℝ) (ht : theta≠0)
    (x y u v p : n → ℝ)
    (hl : u+v=0) (hx : a • (x+u)=0) (hy : y+v=0)
    (hp : a • x=p) (hpy : -y=p)
    (hs : theta*((1/2:ℝ)*pair x x+pair u x)=0) :
    x=0 ∧ y=0 ∧ u=0 ∧ v=0 ∧ p=0 := by
  have hsig : (1/2:ℝ)*pair x x+pair u x=0 :=
    (mul_eq_zero.mp hs).resolve_left ht
  have huy : u=y := by
    funext i
    have hli := congrFun hl i
    have hyi := congrFun hy i
    simp only [Pi.add_apply,Pi.zero_apply] at hli hyi
    linarith
  have hpzero : p=0 := by
    by_cases ha : a=1
    · have hxu : x+u=0 := by simpa [ha] using hx
      have huneg : u=-x := by
        funext i
        have hh := congrFun hxu i
        simp only [Pi.add_apply,Pi.zero_apply,Pi.neg_apply] at hh ⊢
        linarith
      have hpair : pair x x=0 := by
        rw [huneg] at hsig
        have hn : pair (-x) x = -pair x x := by simp [pair,Finset.sum_neg_distrib]
        rw [hn] at hsig
        linarith
      have hxzero := pair_self_zero x hpair
      simpa [ha,hxzero] using hp.symm
    · funext i
      have hxi := congrFun hx i
      have hpi := congrFun hp i
      have hpyi := congrFun hpy i
      have huyi := congrFun huy i
      simp only [Pi.smul_apply,smul_eq_mul,Pi.add_apply,Pi.neg_apply,Pi.zero_apply] at hxi hpi hpyi
      have hui : u i = -p i := by linarith
      rw [hui] at hxi
      have hprod : (a-1)*p i=0 := by nlinarith [hxi,hpi]
      exact (mul_eq_zero.mp hprod).resolve_left (sub_ne_zero.mpr ha)
  have hyzero : y=0 := by simpa [hpzero] using congrArg Neg.neg hpy
  have huzero : u=0 := huy.trans hyzero
  have hvzero : v=0 := by simpa [huzero] using hl
  have hxzero : x=0 := by
    have hpair : pair x x=0 := by
      rw [huzero] at hsig
      simp only [pair,Pi.zero_apply,zero_mul,Finset.sum_const_zero,add_zero] at hsig
      change pair x x=0
      unfold pair
      linarith
    exact pair_self_zero x hpair
  exact ⟨hxzero,hyzero,huzero,hvzero,hpzero⟩

/-- The computed field and background equations of the paired seed family. -/
def PairedJointGate (a theta : ℝ) (x y u v p : n → ℝ) : Prop :=
  u+v=0 ∧ a • (x+u)=0 ∧ y+v=0 ∧ a • x=p ∧ -y=p ∧
    theta*((1/2:ℝ)*pair x x+pair u x)=0

theorem full_joint_gate_iff (a theta : ℝ) (ht : theta≠0) (x y u v p : n → ℝ) :
    PairedJointGate a theta x y u v p ↔ x=0 ∧ y=0 ∧ u=0 ∧ v=0 ∧ p=0 := by
  constructor
  · rintro ⟨hl,hx,hy,hp,hpy,hs⟩
    exact full_joint_block_classification a theta ht x y u v p hl hx hy hp hpy hs
  · rintro ⟨rfl,rfl,rfl,rfl,rfl⟩
    simp [PairedJointGate,pair]

theorem zero_parameter_gate_iff (x y u v p : n → ℝ) :
    PairedJointGate 1 0 x y u v p ↔ x=p ∧ y=-p ∧ u=-p ∧ v=p := by
  constructor
  · rintro ⟨hl,hx,hy,hp,hpy,_⟩
    have hxp : x=p := by simpa using hp
    have hyneg : y=-p := by
      funext i
      have hh := congrFun hpy i
      simp only [Pi.neg_apply] at hh ⊢
      linarith
    have huneg : u=-p := by
      have hh : p+u=0 := by simpa [hxp] using hx
      funext i
      have hi := congrFun hh i
      simp only [Pi.add_apply,Pi.zero_apply,Pi.neg_apply] at hi ⊢
      linarith
    have hvp : v=p := by
      rw [huneg] at hl
      funext i
      have hi := congrFun hl i
      simp only [Pi.add_apply,Pi.zero_apply,Pi.neg_apply] at hi
      linarith
    exact ⟨hxp,hyneg,huneg,hvp⟩
  · rintro ⟨hxp,hyneg,huneg,hvp⟩
    simp [PairedJointGate,hxp,hyneg,huneg,hvp]

section MatrixFrames
variable {m : Type*} [Fintype m] [DecidableEq n] [DecidableEq m]
abbrev Mat (a b : Type*) := Matrix a b ℝ
def encodeP (G0 : Mat n n) (G1 : Mat m m) (P : Mat m n) := G1⁻¹*P*G0
def encodeB (G0 : Mat n n) (G1 : Mat m m) (B : Mat n m) := G0.transpose*B*G1⁻¹.transpose
def encodeM (G0 M : Mat n n) := G0.transpose*M*G0
def encodeH (G1 H : Mat m m) := G1.transpose*H*G1
private lemma invT_mulT (G : Mat n n) (h : IsUnit G.det) : G⁻¹.transpose*G.transpose=1 := by
  rw [←Matrix.transpose_mul,Matrix.mul_nonsing_inv G h,Matrix.transpose_one]
theorem decode_encode_primal (G0 : Mat n n) (G1 : Mat m m) (P : Mat m n)
    (h0 : IsUnit G0.det) (h1 : IsUnit G1.det) :
    G1*encodeP G0 G1 P*G0⁻¹=P := by
  simp only [encodeP,Matrix.mul_assoc]
  rw [Matrix.mul_nonsing_inv G0 h0,Matrix.mul_one,
    ←Matrix.mul_assoc,Matrix.mul_nonsing_inv G1 h1,Matrix.one_mul]
theorem decode_encode_dual (G0 : Mat n n) (G1 : Mat m m) (B : Mat n m)
    (h0 : IsUnit G0.det) (h1 : IsUnit G1.det) :
    G0⁻¹.transpose*encodeB G0 G1 B*G1.transpose=B := by
  simp only [encodeB,Matrix.mul_assoc]
  rw [invT_mulT G1 h1,Matrix.mul_one,←Matrix.mul_assoc,invT_mulT G0 h0,Matrix.one_mul]
theorem decode_encode_star0 (G0 M : Mat n n) (h0 : IsUnit G0.det) :
    G0⁻¹.transpose*encodeM G0 M*G0⁻¹=M := by
  simp only [encodeM,Matrix.mul_assoc]
  rw [Matrix.mul_nonsing_inv G0 h0,Matrix.mul_one,←Matrix.mul_assoc,invT_mulT G0 h0,Matrix.one_mul]
theorem decode_encode_star1 (G1 H : Mat m m) (h1 : IsUnit G1.det) :
    G1⁻¹.transpose*encodeH G1 H*G1⁻¹=H := by
  simp only [encodeH,Matrix.mul_assoc]
  rw [Matrix.mul_nonsing_inv G1 h1,Matrix.mul_one,←Matrix.mul_assoc,invT_mulT G1 h1,Matrix.one_mul]
theorem encoded_visible_composition (G0 : Mat n n) (G1 : Mat m m)
    (P : Mat m n) (B : Mat n m) (H : Mat m m) (h1 : IsUnit G1.det) :
    encodeB G0 G1 B*encodeH G1 H*encodeP G0 G1 P=encodeM G0 (B*H*P) := by
  simp only [encodeB,encodeH,encodeP,encodeM,Matrix.mul_assoc]
  rw [←Matrix.mul_assoc G1⁻¹.transpose G1.transpose,invT_mulT G1 h1,Matrix.one_mul,
    ←Matrix.mul_assoc G1 G1⁻¹,Matrix.mul_nonsing_inv G1 h1,Matrix.one_mul]

def matrixAction (M K : Mat n n) := action (Matrix.toLin' M) (Matrix.toLin' K)
private lemma pair_move_transpose (T : Mat n n) (x y : n → ℝ) :
    pair (T.mulVec x) y=pair x (T.transpose.mulVec y) := by
  change dotProduct (T.mulVec x) y=dotProduct x (T.transpose.mulVec y)
  rw [Matrix.dotProduct_transpose_mulVec]
  exact dotProduct_comm _ _
theorem auxiliary_equivalence_action (M K T : Mat n n) (p c l : n → ℝ) :
    matrixAction M K p (T.mulVec c) (T.mulVec l)=
      matrixAction (T.transpose*M*T) (T.transpose*K) p c l := by
  simp only [matrixAction,action,Matrix.toLin'_apply]
  rw [pair_move_transpose,pair_move_transpose]
  simp only [Matrix.mulVec_sub,Matrix.mulVec_mulVec,pair_sub_right,Matrix.mul_assoc]
end MatrixFrames

end
end D0.Research.NativeParentLaw

open D0.Research.NativeParentLaw
#print axioms literal_owner_binding
#print axioms every_visible_pair_is_an_owner_input
#print axioms visible_coefficients_identifiable
#print axioms field_exact_variation
#print axioms auxiliary_exact_variation
#print axioms multiplier_exact_variation
#print axioms field_hasDerivAt
#print axioms auxiliary_hasDerivAt
#print axioms multiplier_hasDerivAt
#print axioms genuine_gate_equations
#print axioms source_exact_variation
#print axioms source_hasDerivAt
#print axioms diagonal_iff_full_restriction
#print axioms kernel_and_source_comparison
#print axioms full_joint_block_classification
#print axioms full_joint_gate_iff
#print axioms zero_parameter_gate_iff
#print axioms decode_encode_primal
#print axioms decode_encode_dual
#print axioms decode_encode_star0
#print axioms decode_encode_star1
#print axioms encoded_visible_composition
#print axioms auxiliary_equivalence_action
#check literal_owner_binding
#check every_visible_pair_is_an_owner_input
#check visible_coefficients_identifiable
#check genuine_gate_equations
#check field_hasDerivAt
#check auxiliary_hasDerivAt
#check multiplier_hasDerivAt
#check source_hasDerivAt
#check kernel_and_source_comparison
#check full_joint_block_classification
#check full_joint_gate_iff
#check zero_parameter_gate_iff
#check decode_encode_primal
#check encoded_visible_composition
#check auxiliary_equivalence_action
#check D0.Geometry.archiveExteriorFrameLift_comp
#check D0.Geometry.archiveExteriorFrameLift_inverse
