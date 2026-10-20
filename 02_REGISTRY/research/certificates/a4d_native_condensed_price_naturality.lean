import D0.Geometry.ArchiveLightProfinite
import D0.Condensed.OperatorNaturality
import D0.Spectral.CanonicalRefinementScaleFlow
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic

namespace D0.Research.CondensedPrice
noncomputable section
open Matrix
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false
variable {c f : Type*} [Fintype c] [Fintype f] [DecidableEq c] [DecidableEq f]
abbrev Mat (n : Type*) := Matrix n n ℝ

def lift (pi : f → c) : Matrix f c ℝ := fun i a => if pi i=a then 1 else 0

def fibreCard (pi : f → c) (a : c) : ℕ :=
  (Finset.univ.filter (fun i => pi i=a)).card

def average (pi : f → c) : Matrix c f ℝ :=
  fun a i => if pi i=a then ((fibreCard pi a : ℝ))⁻¹ else 0

theorem fibreCard_pos (pi : f → c) (hp : Function.Surjective pi) (a : c) :
    0 < fibreCard pi a := by
  obtain ⟨i, hi⟩ := hp a
  apply Finset.card_pos.mpr
  exact ⟨i, by simp [hi]⟩

theorem fibre_count_real (pi : f → c) (a : c) :
    (∑ i : f, if pi i=a then (1:ℝ) else 0)=(fibreCard pi a:ℝ) := by
  simp [fibreCard, Finset.sum_ite]

theorem average_lift (pi : f → c) (hp : Function.Surjective pi) :
    average pi * lift pi=1 := by
  ext a b
  by_cases hab : a=b
  · subst b
    have hd : (fibreCard pi a:ℝ)≠0 := by exact_mod_cast (Nat.ne_of_gt (fibreCard_pos pi hp a))
    simp only [Matrix.mul_apply, average, lift]
    have hs : (∑ i : f, (if pi i=a then (fibreCard pi a:ℝ)⁻¹ else 0) *
        (if pi i=a then (1:ℝ) else 0))=
        (fibreCard pi a:ℝ)⁻¹ * ∑ i : f, if pi i=a then (1:ℝ) else 0 := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      by_cases h : pi i=a <;> simp [h]
    rw [hs, fibre_count_real, inv_mul_cancel₀ hd]
    simp
  · simp only [Matrix.mul_apply, average, lift, Matrix.one_apply_ne hab]
    apply Finset.sum_eq_zero
    intro i _
    by_cases h : pi i=a
    · have hb : pi i≠b := by intro hb; exact hab (h.symm.trans hb)
      simp [h,hab]
    · simp [h]

theorem lift_gram_is_point_kernel (pi : f → c) :
    lift pi*(lift pi).transpose=fun i j => if pi i=pi j then (1:ℝ) else 0 := by
  ext i j
  simp only [Matrix.mul_apply,Matrix.transpose_apply,lift]
  rw [Finset.sum_eq_single (pi i)]
  · simp [eq_comm]
  · intro a _ ha
    have hi : pi i≠a := Ne.symm ha
    simp [hi]
  · intro h; exact False.elim (h (Finset.mem_univ _))

theorem record_kernel_operator_readout (pi : f → c) (hp : Function.Surjective pi) :
    average pi*(lift pi*(lift pi).transpose)=(lift pi).transpose := by
  rw [←Matrix.mul_assoc,average_lift pi hp,Matrix.one_mul]

theorem split_projection (J : Matrix f c ℝ) (C : Matrix c f ℝ) (hCJ : C*J=1) :
    (J*C)*(J*C)=J*C := by
  calc (J*C)*(J*C)=J*(C*J)*C := by simp only [Matrix.mul_assoc]
       _=J*C := by rw [hCJ]; simp

theorem complement_lift_zero (J : Matrix f c ℝ) (C : Matrix c f ℝ) (hCJ : C*J=1) :
    (1-J*C)*J=0 := by
  simp only [Matrix.sub_mul,Matrix.one_mul,Matrix.mul_assoc,hCJ,Matrix.mul_one,sub_self]

theorem average_complement_zero (J : Matrix f c ℝ) (C : Matrix c f ℝ) (hCJ : C*J=1) :
    C*(1-J*C)=0 := by
  simp only [Matrix.mul_sub,Matrix.mul_one,←Matrix.mul_assoc,hCJ,Matrix.one_mul,sub_self]

theorem natural_extension_complete (J : Matrix f c ℝ) (C : Matrix c f ℝ)
    (A : Mat c) (L : Mat f) (hCJ : C*J=1)
    (hL : L*J=J*A) (hC : C*L=A*C) :
    L=J*A*C+(1-J*C)*L*(1-J*C) := by
  have hPL : J*C*L=J*A*C := by simp only [Matrix.mul_assoc,hC]
  have hLP : L*(J*C)=J*A*C := by rw [←Matrix.mul_assoc,hL]
  have hB : (1-J*C)*L*(1-J*C)=L-J*A*C := by
    simp only [Matrix.sub_mul,Matrix.one_mul,Matrix.mul_sub,Matrix.mul_one]
    rw [hPL,hLP]
    have hX : J*A*C*(J*C)=J*A*C := by
      calc J*A*C*(J*C)=J*A*(C*J)*C := by simp only [Matrix.mul_assoc]
           _=J*A*C := by rw [hCJ]; simp
    rw [hX]
    abel
  rw [hB]
  abel

theorem completion_is_natural (J : Matrix f c ℝ) (C : Matrix c f ℝ)
    (A : Mat c) (B : Mat f) (hCJ : C*J=1) (hBJ : B*J=0) (hCB : C*B=0) :
    (J*A*C+B)*J=J*A ∧ C*(J*A*C+B)=A*C := by
  constructor
  · simp only [Matrix.add_mul,Matrix.mul_assoc,hCJ,Matrix.mul_one,hBJ,add_zero]
  · simp only [Matrix.mul_add,←Matrix.mul_assoc,hCJ,Matrix.one_mul,hCB,add_zero]

theorem scalar_complement_is_natural (J : Matrix f c ℝ) (C : Matrix c f ℝ)
    (A : Mat c) (s : ℝ) (hCJ : C*J=1) :
    (J*A*C+s • (1-J*C))*J=J*A ∧ C*(J*A*C+s • (1-J*C))=A*C := by
  apply completion_is_natural J C A _ hCJ
  · rw [Matrix.smul_mul,complement_lift_zero J C hCJ]; simp
  · rw [Matrix.mul_smul,average_complement_zero J C hCJ]; simp

theorem natural_composites {b : Type*} [Fintype b] [DecidableEq b]
    (J : Matrix f c ℝ) (C : Matrix c f ℝ) (K : Matrix c b ℝ) (D : Matrix b c ℝ)
    (hCJ : C*J=1) (hDK : D*K=1) : (D*C)*(J*K)=1 := by
  calc (D*C)*(J*K)=D*(C*J)*K := by simp only [Matrix.mul_assoc]
       _=1 := by rw [hCJ]; simpa using hDK

theorem complement_trace (J : Matrix f c ℝ) (C : Matrix c f ℝ) (hCJ : C*J=1) :
    (1-J*C).trace=(Fintype.card f:ℝ)-(Fintype.card c:ℝ) := by
  rw [Matrix.trace_sub,Matrix.trace_mul_comm,hCJ]
  simp

theorem complement_keeps_symmetry (R P : Mat f) (hRP : R*P=P*R) :
    R*(1-P)=(1-P)*R := by
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.one_mul,hRP]

theorem uniform_gap_completion {b : Type*} [Fintype b] [DecidableEq b]
    (J : Matrix f c ℝ) (C : Matrix c f ℝ) (K : Matrix c b ℝ) (D : Matrix b c ℝ)
    (A : Mat b) (s : ℝ) :
    J*(K*A*D+s • (1-K*D))*C+s • (1-J*C)=
      (J*K)*A*(D*C)+s • (1-(J*K)*(D*C)) := by
  simp only [Matrix.mul_add,Matrix.add_mul,Matrix.mul_smul,Matrix.smul_mul,
    Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.one_mul,smul_sub,
    Matrix.mul_assoc]
  abel

theorem uniform_gap_all_level_compatibility {b : Type*} [Fintype b] [DecidableEq b]
    (J : Matrix f c ℝ) (C : Matrix c f ℝ) (K : Matrix c b ℝ) (D : Matrix b c ℝ)
    (A : Mat b) (s : ℝ) (hCJ : C*J=1) :
    ((J*K)*A*(D*C)+s • (1-(J*K)*(D*C)))*J=J*(K*A*D+s • (1-K*D)) ∧
    C*((J*K)*A*(D*C)+s • (1-(J*K)*(D*C)))=(K*A*D+s • (1-K*D))*C := by
  rw [←uniform_gap_completion J C K D A s]
  exact scalar_complement_is_natural J C _ s hCJ

theorem gap_shift_trace (J : Matrix f c ℝ) (C : Matrix c f ℝ)
    (A : Mat c) (s t : ℝ) (hCJ : C*J=1) :
    (J*A*C+s • (1-J*C)-(J*A*C+t • (1-J*C))).trace=
      (s-t)*((Fintype.card f:ℝ)-(Fintype.card c:ℝ)) := by
  have h : J*A*C+s • (1-J*C)-(J*A*C+t • (1-J*C))=(s-t) • (1-J*C) := by
    rw [sub_smul]; abel
  rw [h,Matrix.trace_smul,complement_trace J C hCJ]
  simp only [smul_eq_mul]

theorem actual_archive_split (n : ℕ) :
    average (D0.archiveProjection n) * lift (D0.archiveProjection n)=1 :=
  average_lift _ (D0.archive_projection_surjective n)

theorem actual_archive_hidden_dimension_positive (n : ℕ) :
    0 < (Fintype.card (D0.ArchivePoints (n+1))-Fintype.card (D0.ArchivePoints n)) := by
  simpa only [Fintype.card_fin] using Nat.sub_pos_of_lt (D0.spectral_modes_strictly_increase n)

theorem actual_archive_initial_dimensions :
    Fintype.card (D0.ArchivePoints 0)=16 ∧ Fintype.card (D0.ArchivePoints 1)=81 ∧
    Fintype.card (D0.ArchivePoints 2)=256 := by
  norm_num [D0.ArchivePoints,D0.archiveTower,D0.archiveModes,D0.archiveFibers]

theorem actual_archive_hidden_trace (n : ℕ) :
    (1-lift (D0.archiveProjection n)*average (D0.archiveProjection n)).trace=
      (Fintype.card (D0.ArchivePoints (n+1)):ℝ)-(Fintype.card (D0.ArchivePoints n):ℝ) :=
  complement_trace _ _ (actual_archive_split n)

theorem actual_archive_root_hidden_positive (n : ℕ) (hn : 1≤n) :
    0 < Fintype.card (D0.ArchivePoints n)-Fintype.card (D0.ArchivePoints 0) := by
  have hm : StrictMono (fun n : ℕ => (D0.archiveTower n).modes) :=
    strictMono_nat_of_lt_succ D0.spectral_modes_strictly_increase
  have hlt := hm (show 0<n by omega)
  simpa only [Fintype.card_fin] using Nat.sub_pos_of_lt hlt

theorem actual_record_matrix_first_arrow :
    lift (D0.archiveProjection 0)*(lift (D0.archiveProjection 0)).transpose=
      fun i j => D0.archiveDelta 1 i j := by
  rw [lift_gram_is_point_kernel]
  ext i j
  simp [D0.archiveDelta,Fin.ext_iff]

theorem actual_record_operator_naturality_fails :
    average (D0.archiveProjection 0)*
      (lift (D0.archiveProjection 0)*(lift (D0.archiveProjection 0)).transpose)≠
      (1:Mat (D0.ArchivePoints 0))*average (D0.archiveProjection 0) := by
  rw [record_kernel_operator_readout _ (D0.archive_projection_surjective 0),Matrix.one_mul]
  let a0 : D0.ArchivePoints 0 := ⟨0, by norm_num [D0.archiveTower,D0.archiveModes,D0.archiveFibers]⟩
  let i0 : D0.ArchivePoints 1 := ⟨0, by norm_num [D0.archiveTower,D0.archiveModes,D0.archiveFibers]⟩
  have hd : fibreCard (D0.archiveProjection 0) a0=6 := by decide
  have hz : D0.archiveProjection 0 i0=a0 := by apply Fin.ext; rfl
  intro h
  have hh:=congrArg (fun M => M a0 i0) h
  norm_num [lift,average,Matrix.transpose_apply,hd,hz] at hh

def partition (Z r beta s : ℝ) : ℝ := Z+r*Real.exp (-beta*s)
def heat (Z r beta s : ℝ) : ℝ := beta⁻¹*Real.log (partition Z r beta s)
def heatSource (Z r beta s : ℝ) : ℝ := -r*Real.exp (-beta*s)/partition Z r beta s

theorem partition_pos (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    0<partition Z r beta s := by unfold partition; positivity

theorem genuine_hidden_heat_source (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    HasDerivAt (heat Z r beta) (heatSource Z r beta s) s := by
  have hp := partition_pos Z r beta s hZ hr
  have he : HasDerivAt (fun x : ℝ => Real.exp (-beta*x))
      (-beta*Real.exp (-beta*s)) s := by
    convert ((hasDerivAt_id s).const_mul (-beta)).exp using 1 <;> dsimp <;> ring
  have hq : HasDerivAt (partition Z r beta) (r*(-beta*Real.exp (-beta*s))) s :=
    by
    convert (hasDerivAt_const s Z).add (he.const_mul r) using 1 <;> dsimp [partition] <;> ring
  convert (hq.log (ne_of_gt hp)).const_mul beta⁻¹ using 1
  unfold heatSource
  field_simp [hb]

theorem hidden_heat_source_neg (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    heatSource Z r beta s<0 := by
  unfold heatSource
  exact div_neg_of_neg_of_pos (mul_neg_of_neg_of_pos (neg_lt_zero.mpr hr) (Real.exp_pos _)) (partition_pos Z r beta s hZ hr)

theorem hidden_heat_source_error (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    heatSource Z r beta s+1=Z/partition Z r beta s := by
  have hp := ne_of_gt (partition_pos Z r beta s hZ hr)
  unfold heatSource partition at *
  field_simp
  ring

theorem hidden_heat_source_lower (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    -1<heatSource Z r beta s := by
  have he := hidden_heat_source_error Z r beta s hZ hr
  have hz : 0<Z/partition Z r beta s := div_pos hZ (partition_pos Z r beta s hZ hr)
  linarith

theorem genuine_full_price_source (Z r beta s feedback : ℝ)
    (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    HasDerivAt (fun x => heat Z r beta x+feedback) (heatSource Z r beta s) s := by
  simpa using (genuine_hidden_heat_source Z r beta s hZ hr hb).add_const feedback

theorem no_independent_hidden_heat_stationarity (Z r beta s feedback : ℝ)
    (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    deriv (fun x => heat Z r beta x+feedback) s≠0 := by
  rw [(genuine_full_price_source Z r beta s feedback hZ hr hb).deriv]
  exact ne_of_lt (hidden_heat_source_neg Z r beta s hZ hr)

def tailRatio (Z r beta s : ℝ) : ℝ := Z*Real.exp (beta*s)/r

theorem partition_factor (Z r beta s : ℝ) (hr : r≠0) :
    partition Z r beta s=r*Real.exp (-beta*s)*(1+tailRatio Z r beta s) := by
  unfold partition tailRatio
  rw [neg_mul,Real.exp_neg]
  field_simp
  ring

theorem source_tail_form (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    heatSource Z r beta s= -1/(1+tailRatio Z r beta s) := by
  have he := Real.exp_pos (-beta*s)
  have hu : 0<tailRatio Z r beta s := by unfold tailRatio; positivity
  unfold heatSource
  rw [partition_factor Z r beta s (ne_of_gt hr)]
  field_simp

theorem source_tail_error_bounds (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) :
    0<heatSource Z r beta s+1 ∧
    heatSource Z r beta s+1≤tailRatio Z r beta s := by
  have hu : 0<tailRatio Z r beta s := by unfold tailRatio; positivity
  have hd : 0<1+tailRatio Z r beta s := by positivity
  have hh : heatSource Z r beta s+1=tailRatio Z r beta s/(1+tailRatio Z r beta s) := by
    rw [source_tail_form Z r beta s hZ hr]
    field_simp
    ring
  rw [hh]
  constructor
  · exact div_pos hu hd
  · apply (div_le_iff₀ hd).mpr
    nlinarith [sq_nonneg (tailRatio Z r beta s)]

theorem normalized_heat_identity (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    heat Z r beta s-beta⁻¹*Real.log r=
      -s+beta⁻¹*Real.log (1+tailRatio Z r beta s) := by
  have hu : 0<1+tailRatio Z r beta s := by unfold tailRatio; positivity
  unfold heat
  rw [partition_factor Z r beta s (ne_of_gt hr),
    Real.log_mul (ne_of_gt (mul_pos hr (Real.exp_pos _))) (ne_of_gt hu),
    Real.log_mul (ne_of_gt hr) (Real.exp_ne_zero _),Real.log_exp]
  field_simp
  ring

theorem normalized_heat_error_bounds (Z r beta s : ℝ) (hZ : 0<Z) (hr : 0<r) (hb : 0<beta) :
    0<heat Z r beta s-beta⁻¹*Real.log r+s ∧
    heat Z r beta s-beta⁻¹*Real.log r+s≤beta⁻¹*tailRatio Z r beta s := by
  have hu : 0<tailRatio Z r beta s := by unfold tailRatio; positivity
  rw [normalized_heat_identity Z r beta s hZ hr (ne_of_gt hb)]
  have hlo : 0<Real.log (1+tailRatio Z r beta s) := Real.log_pos (by linarith)
  have hhi : Real.log (1+tailRatio Z r beta s)≤tailRatio Z r beta s := by
    have h:=Real.log_le_sub_one_of_pos (show 0<1+tailRatio Z r beta s by positivity)
    linarith
  have hi : 0<beta⁻¹ := inv_pos.mpr hb
  constructor
  · nlinarith [mul_pos hi hlo]
  · nlinarith [mul_le_mul_of_nonneg_left hhi (le_of_lt hi)]

theorem affine_state_gap_source (Z r beta s v feedback : ℝ)
    (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    HasDerivAt (fun x : ℝ => heat Z r beta (s+v*x)+feedback)
      (heatSource Z r beta s*v) 0 := by
  have hl : HasDerivAt (fun x : ℝ => s+v*x) v 0 := by
    simpa only [mul_one] using ((hasDerivAt_id (0:ℝ)).const_mul v).const_add s
  have hf : HasDerivAt (fun x => heat Z r beta x+feedback) (heatSource Z r beta s) (s+v*0) := by
    simpa only [mul_zero,add_zero] using genuine_full_price_source Z r beta s feedback hZ hr hb
  have h:=hf.comp 0 hl
  exact h

theorem complete_scalar_price_jet_fibre (Z r beta s feedback a : ℝ)
    (hZ : 0<Z) (hr : 0<r) (hb : beta≠0) :
    ∃ v : ℝ, HasDerivAt (fun x : ℝ => heat Z r beta (s+v*x)+feedback) a 0 := by
  have hc : heatSource Z r beta s≠0 := ne_of_lt (hidden_heat_source_neg Z r beta s hZ hr)
  refine ⟨a/heatSource Z r beta s, ?_⟩
  convert affine_state_gap_source Z r beta s (a/heatSource Z r beta s) feedback hZ hr hb using 1
  field_simp


theorem actual_phi_scale_ratio (n : ℕ) :
    D0.Spectral.CanonicalRefinementScaleFlow.Lambda (n+1)/
      D0.Spectral.CanonicalRefinementScaleFlow.Lambda n=D0.phi :=
  D0.Spectral.CanonicalRefinementScaleFlow.scale_ratio_forced n

theorem actual_phi_gt_one : 1<D0.phi := by
  have hp:=D0.Spectral.CanonicalRefinementScaleFlow.phi_pos
  have hs:=D0.phi_sq
  by_contra h
  have hle : D0.phi≤1 := le_of_not_gt h
  nlinarith [mul_nonneg (le_of_lt hp) (sub_nonneg.mpr hle)]

theorem fixed_phi_shape_source (Z beta s feedback : ℝ) (hZ : 0<Z) (hb : beta≠0) :
    HasDerivAt (fun x : ℝ => heat (Z+5*Real.exp (-beta*D0.phi)) 60 beta (D0.phi*x)+feedback)
      (D0.phi*heatSource (Z+5*Real.exp (-beta*D0.phi)) 60 beta (D0.phi*s)) s := by
  have hZp : 0<Z+5*Real.exp (-beta*D0.phi) := by positivity
  have hl : HasDerivAt (fun x : ℝ => D0.phi*x) D0.phi s := by
    simpa only [mul_one] using (hasDerivAt_id s).const_mul D0.phi
  have h:=(genuine_full_price_source (Z+5*Real.exp (-beta*D0.phi)) 60 beta
    (D0.phi*s) feedback hZp (by norm_num) hb).comp s hl
  convert h using 1
  ring

theorem fixed_phi_shape_source_nonzero (Z beta s : ℝ) (hZ : 0<Z) :
    D0.phi*heatSource (Z+5*Real.exp (-beta*D0.phi)) 60 beta (D0.phi*s)≠0 := by
  have hp:=D0.Spectral.CanonicalRefinementScaleFlow.phi_pos
  have hZp : 0<Z+5*Real.exp (-beta*D0.phi) := by positivity
  exact ne_of_lt (mul_neg_of_pos_of_neg hp
    (hidden_heat_source_neg _ 60 beta _ hZp (by norm_num)))

theorem fixed_budget_mode_minimum (beta lam ceiling : ℝ) (hb : 0<beta) (hl : lam≤ceiling) :
    Real.exp (-beta*ceiling)≤Real.exp (-beta*lam) := by
  apply Real.exp_le_exp.mpr
  nlinarith

theorem fixed_budget_mode_equality (beta lam ceiling : ℝ) (hb : 0<beta) :
    Real.exp (-beta*lam)=Real.exp (-beta*ceiling) ↔ lam=ceiling := by
  rw [Real.exp_eq_exp]
  constructor
  · intro h; nlinarith
  · intro h; rw [h]


theorem fixed_budget_partition_minimum (beta ceiling : ℝ) (lam : c → ℝ)
    (hb : 0<beta) (hl : ∀i, lam i≤ceiling) :
    (Fintype.card c:ℝ)*Real.exp (-beta*ceiling)≤∑i, Real.exp (-beta*lam i) := by
  calc (Fintype.card c:ℝ)*Real.exp (-beta*ceiling)=∑i:c, Real.exp (-beta*ceiling) := by simp
       _≤∑i, Real.exp (-beta*lam i) := Finset.sum_le_sum (fun i _ => fixed_budget_mode_minimum _ _ _ hb (hl i))

theorem fixed_budget_partition_equality (beta ceiling : ℝ) (lam : c → ℝ)
    (hb : 0<beta) (hl : ∀i, lam i≤ceiling) :
    (∑i, Real.exp (-beta*lam i))=(Fintype.card c:ℝ)*Real.exp (-beta*ceiling) ↔
      ∀i, lam i=ceiling := by
  constructor
  · intro he
    have hnon : ∀i∈(Finset.univ:Finset c), 0≤Real.exp (-beta*lam i)-Real.exp (-beta*ceiling) := by
      intro i _
      exact sub_nonneg.mpr (fixed_budget_mode_minimum beta (lam i) ceiling hb (hl i))
    have hsum : (∑i:c, (Real.exp (-beta*lam i)-Real.exp (-beta*ceiling)))=0 := by
      rw [Finset.sum_sub_distrib]
      simpa only [Finset.sum_const,Finset.card_univ,nsmul_eq_mul] using sub_eq_zero.mpr he
    have hall:=(Finset.sum_eq_zero_iff_of_nonneg hnon).mp hsum
    intro i
    apply (fixed_budget_mode_equality beta (lam i) ceiling hb).mp
    exact sub_eq_zero.mp (hall i (Finset.mem_univ i))
  · intro h
    simp [h]


end
end D0.Research.CondensedPrice

-- Real declarations and transitive hypotheses, not name-only bindings.
#check D0.Research.CondensedPrice.fibreCard_pos
#print axioms D0.Research.CondensedPrice.fibreCard_pos
#check D0.Research.CondensedPrice.fibre_count_real
#print axioms D0.Research.CondensedPrice.fibre_count_real
#check D0.Research.CondensedPrice.average_lift
#print axioms D0.Research.CondensedPrice.average_lift
#check D0.Research.CondensedPrice.lift_gram_is_point_kernel
#print axioms D0.Research.CondensedPrice.lift_gram_is_point_kernel
#check D0.Research.CondensedPrice.record_kernel_operator_readout
#print axioms D0.Research.CondensedPrice.record_kernel_operator_readout
#check D0.Research.CondensedPrice.split_projection
#print axioms D0.Research.CondensedPrice.split_projection
#check D0.Research.CondensedPrice.complement_lift_zero
#print axioms D0.Research.CondensedPrice.complement_lift_zero
#check D0.Research.CondensedPrice.average_complement_zero
#print axioms D0.Research.CondensedPrice.average_complement_zero
#check D0.Research.CondensedPrice.natural_extension_complete
#print axioms D0.Research.CondensedPrice.natural_extension_complete
#check D0.Research.CondensedPrice.completion_is_natural
#print axioms D0.Research.CondensedPrice.completion_is_natural
#check D0.Research.CondensedPrice.scalar_complement_is_natural
#print axioms D0.Research.CondensedPrice.scalar_complement_is_natural
#check D0.Research.CondensedPrice.natural_composites
#print axioms D0.Research.CondensedPrice.natural_composites
#check D0.Research.CondensedPrice.complement_trace
#print axioms D0.Research.CondensedPrice.complement_trace
#check D0.Research.CondensedPrice.complement_keeps_symmetry
#print axioms D0.Research.CondensedPrice.complement_keeps_symmetry
#check D0.Research.CondensedPrice.uniform_gap_completion
#print axioms D0.Research.CondensedPrice.uniform_gap_completion
#check D0.Research.CondensedPrice.uniform_gap_all_level_compatibility
#print axioms D0.Research.CondensedPrice.uniform_gap_all_level_compatibility
#check D0.Research.CondensedPrice.gap_shift_trace
#print axioms D0.Research.CondensedPrice.gap_shift_trace
#check D0.Research.CondensedPrice.actual_archive_split
#print axioms D0.Research.CondensedPrice.actual_archive_split
#check D0.Research.CondensedPrice.actual_archive_hidden_dimension_positive
#print axioms D0.Research.CondensedPrice.actual_archive_hidden_dimension_positive
#check D0.Research.CondensedPrice.actual_archive_initial_dimensions
#print axioms D0.Research.CondensedPrice.actual_archive_initial_dimensions
#check D0.Research.CondensedPrice.actual_archive_hidden_trace
#print axioms D0.Research.CondensedPrice.actual_archive_hidden_trace
#check D0.Research.CondensedPrice.actual_archive_root_hidden_positive
#print axioms D0.Research.CondensedPrice.actual_archive_root_hidden_positive
#check D0.Research.CondensedPrice.actual_record_matrix_first_arrow
#print axioms D0.Research.CondensedPrice.actual_record_matrix_first_arrow
#check D0.Research.CondensedPrice.actual_record_operator_naturality_fails
#print axioms D0.Research.CondensedPrice.actual_record_operator_naturality_fails
#check D0.Research.CondensedPrice.partition_pos
#print axioms D0.Research.CondensedPrice.partition_pos
#check D0.Research.CondensedPrice.genuine_hidden_heat_source
#print axioms D0.Research.CondensedPrice.genuine_hidden_heat_source
#check D0.Research.CondensedPrice.hidden_heat_source_neg
#print axioms D0.Research.CondensedPrice.hidden_heat_source_neg
#check D0.Research.CondensedPrice.hidden_heat_source_error
#print axioms D0.Research.CondensedPrice.hidden_heat_source_error
#check D0.Research.CondensedPrice.hidden_heat_source_lower
#print axioms D0.Research.CondensedPrice.hidden_heat_source_lower
#check D0.Research.CondensedPrice.genuine_full_price_source
#print axioms D0.Research.CondensedPrice.genuine_full_price_source
#check D0.Research.CondensedPrice.no_independent_hidden_heat_stationarity
#print axioms D0.Research.CondensedPrice.no_independent_hidden_heat_stationarity
#check D0.Research.CondensedPrice.partition_factor
#print axioms D0.Research.CondensedPrice.partition_factor
#check D0.Research.CondensedPrice.source_tail_form
#print axioms D0.Research.CondensedPrice.source_tail_form
#check D0.Research.CondensedPrice.source_tail_error_bounds
#print axioms D0.Research.CondensedPrice.source_tail_error_bounds
#check D0.Research.CondensedPrice.normalized_heat_identity
#print axioms D0.Research.CondensedPrice.normalized_heat_identity
#check D0.Research.CondensedPrice.normalized_heat_error_bounds
#print axioms D0.Research.CondensedPrice.normalized_heat_error_bounds
#check D0.Research.CondensedPrice.affine_state_gap_source
#print axioms D0.Research.CondensedPrice.affine_state_gap_source
#check D0.Research.CondensedPrice.complete_scalar_price_jet_fibre
#print axioms D0.Research.CondensedPrice.complete_scalar_price_jet_fibre
#check D0.Research.CondensedPrice.actual_phi_scale_ratio
#print axioms D0.Research.CondensedPrice.actual_phi_scale_ratio
#check D0.Research.CondensedPrice.actual_phi_gt_one
#print axioms D0.Research.CondensedPrice.actual_phi_gt_one
#check D0.Research.CondensedPrice.fixed_phi_shape_source
#print axioms D0.Research.CondensedPrice.fixed_phi_shape_source
#check D0.Research.CondensedPrice.fixed_phi_shape_source_nonzero
#print axioms D0.Research.CondensedPrice.fixed_phi_shape_source_nonzero
#check D0.Research.CondensedPrice.fixed_budget_mode_minimum
#print axioms D0.Research.CondensedPrice.fixed_budget_mode_minimum
#check D0.Research.CondensedPrice.fixed_budget_mode_equality
#print axioms D0.Research.CondensedPrice.fixed_budget_mode_equality
#check D0.Research.CondensedPrice.fixed_budget_partition_minimum
#print axioms D0.Research.CondensedPrice.fixed_budget_partition_minimum
#check D0.Research.CondensedPrice.fixed_budget_partition_equality
#print axioms D0.Research.CondensedPrice.fixed_budget_partition_equality
#check D0.archive_record_kernel_projectively_compatible
#print axioms D0.archive_record_kernel_projectively_compatible
#check D0.archive_projection_surjective
#print axioms D0.archive_projection_surjective
#check D0.archive_tower_defines_profinite_object
#print axioms D0.archive_tower_defines_profinite_object
#check D0.archiveFintypeDiagram_succ
#print axioms D0.archiveFintypeDiagram_succ
#check D0.archiveDiagram_transition_surjective
#print axioms D0.archiveDiagram_transition_surjective
#check D0.Spectral.CanonicalRefinementScaleFlow.scale_ratio_forced
#print axioms D0.Spectral.CanonicalRefinementScaleFlow.scale_ratio_forced
#check D0.CompatibleOperatorFamily
#print axioms D0.CompatibleOperatorFamily
#check D0.inducedLimitOperator
#print axioms D0.inducedLimitOperator
#check D0.archiveLightProfinite
#print axioms D0.archiveLightProfinite
#print D0.CompatibleOperatorFamily
