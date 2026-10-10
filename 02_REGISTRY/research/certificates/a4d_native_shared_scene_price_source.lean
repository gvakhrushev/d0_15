import D0.Synthesis.DenseOperatorSceneRigidity
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

namespace D0.Research.NativeScenePriceSource
noncomputable section
open Matrix
set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false
variable {n : Type*} [Fintype n] [DecidableEq n]
abbrev Mat (n : Type*) := Matrix n n ℝ

/-- The degree normalization is differentiated together with adjacency. -/
theorem normalized_transport_jet (D DI T dD E dT : Mat n)
    (hi : DI*D=1) (hj : dD*T+D*dT=E) :
    dT=DI*(E-dD*T) := by
  rw [←hj]
  have hc : dD*T+D*dT-dD*T=D*dT := by abel
  rw [hc,←Matrix.mul_assoc,hi,Matrix.one_mul]

theorem normalized_jet_keeps_unit (DI T dD E : Mat n) (v : n → ℝ)
    (hu : T.mulVec v=v) (hd : dD.mulVec v=E.mulVec v) :
    (DI*(E-dD*T)).mulVec v=0 := by
  rw [←Matrix.mulVec_mulVec,Matrix.sub_mulVec,←Matrix.mulVec_mulVec,hu,hd,sub_self,
    Matrix.mulVec_zero]

/-- dF = -(dT T + T dT), with a resolvent commuting with T. -/
theorem shared_scene_feedback_source (T V R : Mat n) (z : ℝ)
    (hRT : R*T=T*R) :
    z*(R*(-(V*T+T*V))).trace=(-2*z)*(T*R*V).trace := by
  have hc : (R*(V*T)).trace=(T*R*V).trace := by
    simpa only [Matrix.mul_assoc] using Matrix.trace_mul_cycle R V T
  have hc' : (R*(T*V)).trace=(T*R*V).trace := by rw [←Matrix.mul_assoc,hRT]
  simp only [Matrix.mul_neg,Matrix.mul_add,Matrix.trace_neg,Matrix.trace_add,hc,hc']
  ring

theorem shared_scene_full_source (T V R H : Mat n) (z : ℝ)
    (hRT : R*T=T*R) :
    (H*V).trace+z*(R*(-(V*T+T*V))).trace=((H-(2*z) • (T*R))*V).trace := by
  rw [shared_scene_feedback_source T V R z hRT]
  simp only [Matrix.sub_mul,Matrix.smul_mul,Matrix.trace_sub,Matrix.trace_smul]
  ring

/-- Once the native degree-normalized jet is supplied, only this contraction
of the primitive jet is needed by the scalar price. -/
theorem common_source_pullback (M DI T dD E dT : Mat n)
    (hj : dT=DI*(E-dD*T)) :
    (M*dT).trace=(M*DI*E).trace-(T*M*DI*dD).trace := by
  rw [hj,Matrix.mul_sub,Matrix.mul_sub,Matrix.trace_sub]
  have hc : (M*(DI*(dD*T))).trace=(T*M*DI*dD).trace := by
    simpa only [Matrix.mul_assoc] using Matrix.trace_mul_cycle (M*DI) dD T
  rw [hc]
  simp only [Matrix.mul_assoc]

/-- The exact polynomial functional-calculus quotient at the owned scene. -/
theorem spectral_first_jet_quotient (T V : Mat n) (a0 a1 a2 a3 k : ℝ)
    (h0 : V.trace=0)
    (h2 : (T*T*V).trace=-(T*V).trace)
    (h3 : (T*T*T*V).trace=(1-k)*(T*V).trace) :
    (((a0 • 1+a1 • T)+a2 • (T*T)+a3 • (T*T*T))*V).trace =
      (-a1+a2-(1-k)*a3)*(-(T*V).trace) := by
  simp only [Matrix.add_mul,Matrix.smul_mul,Matrix.one_mul,Matrix.trace_add,
    Matrix.trace_smul,h0,h2,h3]
  ring

/-- Equivalent divided-difference form, with all two invisible sectors kept. -/
theorem two_visible_sector_source (P0 Pd Pp Pm V : Mat n)
    (rp rm m0 md mp mm : ℝ)
    (hparts : P0+Pd+Pp+Pm=1)
    (h0 : (P0*V).trace=0) (hd : (Pd*V).trace=0) (hv : V.trace=0)
    (hne : rp-rm≠0) :
    (((m0 • P0+md • Pd)+mp • Pp+mm • Pm)*V).trace =
      ((mm-mp)/(rp-rm)) * (-((P0+rp • Pp+rm • Pm)*V).trace) := by
  have hs : (Pp*V).trace+(Pm*V).trace=0 := by
    have h := congrArg (fun A : Mat n => (A*V).trace) hparts
    simpa only [Matrix.add_mul,Matrix.trace_add,h0,hd,Matrix.one_mul,hv,zero_add] using h
  simp only [Matrix.add_mul,Matrix.smul_mul,Matrix.trace_add,Matrix.trace_smul,h0,hd]
  have hm : (Pm*V).trace=-(Pp*V).trace := by linarith
  rw [hm]
  field_simp [hne]
  ring

def visiblePencil (k z : ℝ) : ℝ := (1-z)*(1-2*k*z)+k^2*z^2

def feedbackKappaSource (k z : ℝ) : ℝ := 2*z*(1-(1+k)*z)/visiblePencil k z

theorem genuine_visible_feedback_source (k z : ℝ) (hq : visiblePencil k z≠0) :
    HasDerivAt (fun x : ℝ => -Real.log (visiblePencil x z)) (feedbackKappaSource k z) k := by
  have hq' : HasDerivAt (fun x : ℝ => visiblePencil x z)
      (-2*z+2*z^2+2*k*z^2) k := by
    unfold visiblePencil
    convert ((hasDerivAt_const k (1-z)).mul
      ((hasDerivAt_const k 1).sub (((hasDerivAt_id k).const_mul 2).mul_const z))).add
      (((hasDerivAt_id k).pow 2).mul_const (z^2)) using 1 <;> dsimp <;> ring
  convert (hq'.log hq).neg using 1
  unfold feedbackKappaSource visiblePencil
  field_simp
  ring

def scenePartition (beta r : ℝ) : ℝ :=
  1+30*Real.exp (-beta)+Real.exp (-beta*((3/2:ℝ)-r))+Real.exp (-beta*((3/2:ℝ)+r))

def sceneHeat (beta r : ℝ) : ℝ := beta⁻¹*Real.log (scenePartition beta r)

def heatSeparationSource (beta r : ℝ) : ℝ :=
  (Real.exp (-beta*((3/2:ℝ)-r))-Real.exp (-beta*((3/2:ℝ)+r)))/scenePartition beta r

theorem scenePartition_pos (beta r : ℝ) : 0<scenePartition beta r := by
  unfold scenePartition
  positivity

theorem genuine_scene_heat_source (beta r : ℝ) (hb : beta≠0) :
    HasDerivAt (sceneHeat beta) (heatSeparationSource beta r) r := by
  have hp : HasDerivAt (fun x : ℝ => Real.exp (-beta*((3/2:ℝ)-x)))
      (beta*Real.exp (-beta*((3/2:ℝ)-r))) r := by
    convert (((hasDerivAt_const r (3/2:ℝ)).sub (hasDerivAt_id r)).const_mul (-beta)).exp using 1 <;> dsimp <;> ring
  have hm : HasDerivAt (fun x : ℝ => Real.exp (-beta*((3/2:ℝ)+x)))
      (-beta*Real.exp (-beta*((3/2:ℝ)+r))) r := by
    convert (((hasDerivAt_const r (3/2:ℝ)).add (hasDerivAt_id r)).const_mul (-beta)).exp using 1 <;> dsimp <;> ring
  have hZ : HasDerivAt (scenePartition beta)
      (beta*(Real.exp (-beta*((3/2:ℝ)-r))-Real.exp (-beta*((3/2:ℝ)+r)))) r := by
    convert (((hasDerivAt_const r (1+30*Real.exp (-beta))).add hp).add hm) using 1 <;> dsimp <;> ring
  have h := ((hZ.log (ne_of_gt (scenePartition_pos beta r))).const_mul beta⁻¹)
  convert h using 1
  unfold heatSeparationSource
  field_simp [hb]

/-- kappa parameter of the actual two visible eigenvalues, with its real square-root domain. -/
def sceneSeparation (k : ℝ) : ℝ := Real.sqrt ((1/4:ℝ)-k)

theorem genuine_scene_separation (k : ℝ) (hk : k<1/4) :
    HasDerivAt sceneSeparation (-(1/(2*sceneSeparation k))) k := by
  have hn : (1/4:ℝ)-k≠0 := by linarith
  convert (Real.hasDerivAt_sqrt hn).comp k ((hasDerivAt_const k (1/4:ℝ)).sub (hasDerivAt_id k)) using 1 <;>
    simp [sceneSeparation]

def heatKappaSource (beta k : ℝ) : ℝ :=
  -(heatSeparationSource beta (sceneSeparation k)/(2*sceneSeparation k))

theorem genuine_heat_kappa_source (beta k : ℝ) (hb : beta≠0) (hk : k<1/4) :
    HasDerivAt (fun x : ℝ => sceneHeat beta (sceneSeparation x)) (heatKappaSource beta k) k := by
  convert (genuine_scene_heat_source beta (sceneSeparation k) hb).comp k
    (genuine_scene_separation k hk) using 1
  simp [heatKappaSource]
  ring

def sceneWholePrice (beta z k : ℝ) : ℝ :=
  sceneHeat beta (sceneSeparation k)-30*Real.log (1-z)-Real.log (visiblePencil k z)

theorem genuine_scene_whole_kappa_source (beta z k : ℝ)
    (hb : beta≠0) (hk : k<1/4) (hq : visiblePencil k z≠0) :
    HasDerivAt (sceneWholePrice beta z)
      (heatKappaSource beta k+feedbackKappaSource k z) k := by
  have h := ((genuine_heat_kappa_source beta k hb hk).sub_const (30*Real.log (1-z))).add
    (genuine_visible_feedback_source k z hq)
  simpa only [sceneWholePrice,sub_eq_add_neg] using h


variable {m : Type*} [Fintype m] [DecidableEq m]

/-- Exact full-history feedback reduction, including every archive row. -/
theorem weighted_history_feedback (J : Matrix m n ℝ) (C : Matrix n m ℝ)
    (R : Mat m) (hCJ : C*J=1) (hRR : R*R=1) :
    (J*C)*R*(1-J*C)*R*(J*C)=J*(1-(C*R*J)*(C*R*J))*C := by
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.one_mul,Matrix.mul_assoc]
  rw [←Matrix.mul_assoc R R,hRR,Matrix.one_mul,←Matrix.mul_assoc C J,hCJ,Matrix.one_mul]

/-- Ordinary determinant: the full archive's identity block is retained. -/
theorem full_history_det_reduction (J : Matrix m n ℝ) (C : Matrix n m ℝ)
    (F : Mat n) (z : ℝ) (hCJ : C*J=1) :
    Matrix.det (1-z • (J*F*C))=Matrix.det (1-z • F) := by
  have h := Matrix.det_one_sub_mul_comm J (z • (F*C))
  simpa only [Matrix.mul_smul,Matrix.smul_mul,Matrix.mul_assoc,hCJ,Matrix.mul_one] using h

theorem stationary_equation_quadratic (h z : ℝ) :
    h*visiblePencil (39/160) z-2*z*(1-(1+(39/160:ℝ))*z) =
      ((199/80:ℝ)+(14001/25600:ℝ)*h)*z^2-(2+(119/80:ℝ)*h)*z+h := by
  unfold visiblePencil
  ring

theorem stationary_quadratic_discriminant (h : ℝ) :
    (2+(119/80:ℝ)*h)^2-4*((199/80:ℝ)+(14001/25600:ℝ)*h)*h =
      4*(1-h)+h^2/40 := by ring

theorem native_half_feedback_coefficient :
    feedbackKappaSource (39/160) (1/2)=38720/40241 := by
  norm_num [feedbackKappaSource,visiblePencil]

theorem native_feedback_turn :
    feedbackKappaSource (39/160) (160/199)=0 := by
  norm_num [feedbackKappaSource,visiblePencil]

def darkHeatCoefficient (beta r : ℝ) : ℝ :=
  beta*Real.exp (-beta)/scenePartition beta r

theorem dark_heat_coefficient_lt_one (beta r : ℝ) : darkHeatCoefficient beta r<1 := by
  have hb : beta<Real.exp beta := by linarith [Real.add_one_le_exp beta]
  have hnum : beta*Real.exp (-beta)<1 := by
    rw [Real.exp_neg,←div_eq_mul_inv]
    exact (div_lt_one (Real.exp_pos beta)).mpr hb
  have hz : 1<scenePartition beta r := by
    unfold scenePartition
    have h1 := Real.exp_pos (-beta)
    have h2 := Real.exp_pos (-beta*((3/2:ℝ)-r))
    have h3 := Real.exp_pos (-beta*((3/2:ℝ)+r))
    linarith
  exact (div_lt_one (scenePartition_pos beta r)).mpr (lt_trans hnum hz)

theorem upper_branch_balanced_second_variation_negative (beta r z energy : ℝ)
    (hz : (1/2:ℝ)<z) (hz1 : z<1) (he : 0<energy) :
    (darkHeatCoefficient beta r-2*z/(1-z))*energy<0 := by
  have hd : 0<1-z := by linarith
  have hf : 2<2*z/(1-z) := (lt_div_iff₀ hd).mpr (by linarith)
  have hc := dark_heat_coefficient_lt_one beta r
  exact mul_neg_of_neg_of_pos (by linarith) he

/-- Binary incidence is a constraint on a genuine curve, not a frozen degree assumption. -/
theorem binary_curve_derivative_zero (f : ℝ → ℝ) (d t : ℝ)
    (hd : HasDerivAt f d t) (hbinary : ∀ s, f s=0 ∨ f s=1) : d=0 := by
  have hz : (fun s => f s*f s-f s)=(fun _ : ℝ => (0:ℝ)) := by
    funext s
    rcases hbinary s with h | h <;> rw [h] <;> norm_num
  have hp : HasDerivAt (fun s => f s*f s-f s) (d*f t+f t*d-d) t :=
    HasDerivAt.sub (HasDerivAt.mul hd hd) hd
  rw [hz] at hp
  have he := hp.unique (hasDerivAt_const t (0:ℝ))
  rcases hbinary t with h | h <;> rw [h] at he <;> norm_num at he <;> linarith

variable {v w : Type*} [Fintype v] [Fintype w] [DecidableEq v] [DecidableEq w]

theorem binary_matrix_jet_zero (A : ℝ → Matrix v v ℝ) (E : Matrix v v ℝ) (t : ℝ)
    (hd : ∀ i j, HasDerivAt (fun s => A s i j) (E i j) t)
    (hbinary : ∀ s i j, A s i j=0 ∨ A s i j=1) : E=0 := by
  ext i j
  exact binary_curve_derivative_zero (fun s => A s i j) (E i j) t
    (hd i j) (fun s => hbinary s i j)

def normalizedTransport (A : Matrix v v ℚ) : Matrix v v ℚ :=
  fun i j => (∑ k, A i k)⁻¹*A i j

theorem normalized_transport_relabel (A : Matrix v v ℚ) (e : v ≃ w) :
    normalizedTransport (Matrix.reindex e e A)=Matrix.reindex e e (normalizedTransport A) := by
  ext i j
  change (∑ k : w, A (e.symm i) (e.symm k))⁻¹*A (e.symm i) (e.symm j) =
    (∑ k : v, A (e.symm i) k)⁻¹*A (e.symm i) (e.symm j)
  have hs : (∑ k : w, A (e.symm i) (e.symm k))=∑ k : v, A (e.symm i) k :=
    Equiv.sum_comp e.symm (fun k => A (e.symm i) k)
  rw [hs]

def partitionKappa (a b c : ℕ) : ℝ :=
  2*(a:ℝ)*b*c/(((a:ℝ)+b)*((a:ℝ)+c)*((b:ℝ)+c))

theorem recovered_partition_kappa_constant (a b c : ℕ)
    (hm : ({a,b,c}:Multiset ℕ)={9,11,13}) : partitionKappa a b c=39/160 := by
  have hsN : a+b+c=33 := by simpa [add_assoc] using congrArg Multiset.sum hm
  have hpN : a*b*c=1287 := by simpa [mul_assoc] using congrArg Multiset.prod hm
  have hs : (a:ℝ)+b+c=33 := by exact_mod_cast hsN
  have hp : (a:ℝ)*b*c=1287 := by exact_mod_cast hpN
  have hd := congrArg (fun m : Multiset ℕ => (m.map (fun n : ℕ => (33:ℝ)-(n:ℝ))).prod) hm
  norm_num at hd
  have ha : (33:ℝ)-a=b+c := by linarith
  have hb : (33:ℝ)-b=a+c := by linarith
  have hc : (33:ℝ)-c=a+b := by linarith
  have hden : ((a:ℝ)+b)*((a:ℝ)+c)*((b:ℝ)+c)=10560 := by
    calc
      _ = ((33:ℝ)-a)*(33-b)*(33-c) := by rw [ha,hb,hc]; ring
      _ = 10560 := by nlinarith [hd]
  unfold partitionKappa
  rw [show 2*(a:ℝ)*b*c=2*((a:ℝ)*b*c) by ring,hp,hden]
  norm_num

theorem dense_contract_has_canonical_kappa (A : Matrix v v ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank≤3) (hV : Fintype.card v=33) (h2 : Matrix.trace (A*A)=718) :
    ∃ z : v → Fin 3, Function.Surjective z ∧
      (∀ i j, A i j=if z i=z j then 0 else 1) ∧
      partitionKappa (D0.Synthesis.OperatorSceneReconstruction.fibreSize z 0)
        (D0.Synthesis.OperatorSceneReconstruction.fibreSize z 1)
        (D0.Synthesis.OperatorSceneReconstruction.fibreSize z 2)=39/160 := by
  obtain ⟨z,hs,hz,hm,_,_⟩ :=
    D0.Synthesis.DenseOperatorSceneRigidity.dense_operator_recovers_scene A hA hr hV h2
  exact ⟨z,hs,hz,recovered_partition_kappa_constant _ _ _ hm⟩


/-- No smoothness of the reconstructed labels is assumed: the scalar price
is constant on every member of the complete owned passport class. -/
theorem passport_scene_price_source_zero (a b c : ℝ → ℕ) (beta z t : ℝ)
    (hm : ∀ s, ({a s,b s,c s}:Multiset ℕ)={9,11,13}) :
    HasDerivAt (fun s => sceneWholePrice beta z (partitionKappa (a s) (b s) (c s))) 0 t := by
  have hf : (fun s => sceneWholePrice beta z (partitionKappa (a s) (b s) (c s))) =
      (fun _ : ℝ => sceneWholePrice beta z (39/160)) := by
    funext s
    rw [recovered_partition_kappa_constant _ _ _ (hm s)]
  rw [hf]
  exact hasDerivAt_const t _

end
end D0.Research.NativeScenePriceSource

-- Inspect actual propositions and transitive kernel dependencies.
#check D0.Research.NativeScenePriceSource.normalized_transport_jet
#print axioms D0.Research.NativeScenePriceSource.normalized_transport_jet
#check D0.Research.NativeScenePriceSource.normalized_jet_keeps_unit
#print axioms D0.Research.NativeScenePriceSource.normalized_jet_keeps_unit
#check D0.Research.NativeScenePriceSource.shared_scene_feedback_source
#print axioms D0.Research.NativeScenePriceSource.shared_scene_feedback_source
#check D0.Research.NativeScenePriceSource.shared_scene_full_source
#print axioms D0.Research.NativeScenePriceSource.shared_scene_full_source
#check D0.Research.NativeScenePriceSource.common_source_pullback
#print axioms D0.Research.NativeScenePriceSource.common_source_pullback
#check D0.Research.NativeScenePriceSource.spectral_first_jet_quotient
#print axioms D0.Research.NativeScenePriceSource.spectral_first_jet_quotient
#check D0.Research.NativeScenePriceSource.two_visible_sector_source
#print axioms D0.Research.NativeScenePriceSource.two_visible_sector_source
#check D0.Research.NativeScenePriceSource.genuine_visible_feedback_source
#print axioms D0.Research.NativeScenePriceSource.genuine_visible_feedback_source
#check D0.Research.NativeScenePriceSource.scenePartition_pos
#print axioms D0.Research.NativeScenePriceSource.scenePartition_pos
#check D0.Research.NativeScenePriceSource.genuine_scene_heat_source
#print axioms D0.Research.NativeScenePriceSource.genuine_scene_heat_source
#check D0.Research.NativeScenePriceSource.genuine_scene_separation
#print axioms D0.Research.NativeScenePriceSource.genuine_scene_separation
#check D0.Research.NativeScenePriceSource.genuine_heat_kappa_source
#print axioms D0.Research.NativeScenePriceSource.genuine_heat_kappa_source
#check D0.Research.NativeScenePriceSource.genuine_scene_whole_kappa_source
#print axioms D0.Research.NativeScenePriceSource.genuine_scene_whole_kappa_source
#check D0.Research.NativeScenePriceSource.weighted_history_feedback
#print axioms D0.Research.NativeScenePriceSource.weighted_history_feedback
#check D0.Research.NativeScenePriceSource.full_history_det_reduction
#print axioms D0.Research.NativeScenePriceSource.full_history_det_reduction
#check D0.Research.NativeScenePriceSource.stationary_equation_quadratic
#print axioms D0.Research.NativeScenePriceSource.stationary_equation_quadratic
#check D0.Research.NativeScenePriceSource.stationary_quadratic_discriminant
#print axioms D0.Research.NativeScenePriceSource.stationary_quadratic_discriminant
#check D0.Research.NativeScenePriceSource.native_half_feedback_coefficient
#print axioms D0.Research.NativeScenePriceSource.native_half_feedback_coefficient
#check D0.Research.NativeScenePriceSource.native_feedback_turn
#print axioms D0.Research.NativeScenePriceSource.native_feedback_turn
#check D0.Research.NativeScenePriceSource.dark_heat_coefficient_lt_one
#print axioms D0.Research.NativeScenePriceSource.dark_heat_coefficient_lt_one
#check D0.Research.NativeScenePriceSource.upper_branch_balanced_second_variation_negative
#print axioms D0.Research.NativeScenePriceSource.upper_branch_balanced_second_variation_negative
#check D0.Research.NativeScenePriceSource.binary_curve_derivative_zero
#print axioms D0.Research.NativeScenePriceSource.binary_curve_derivative_zero
#check D0.Research.NativeScenePriceSource.binary_matrix_jet_zero
#print axioms D0.Research.NativeScenePriceSource.binary_matrix_jet_zero
#check D0.Research.NativeScenePriceSource.normalized_transport_relabel
#print axioms D0.Research.NativeScenePriceSource.normalized_transport_relabel
#check D0.Research.NativeScenePriceSource.recovered_partition_kappa_constant
#print axioms D0.Research.NativeScenePriceSource.recovered_partition_kappa_constant
#check D0.Research.NativeScenePriceSource.dense_contract_has_canonical_kappa
#print axioms D0.Research.NativeScenePriceSource.dense_contract_has_canonical_kappa
#check D0.Research.NativeScenePriceSource.passport_scene_price_source_zero
#print axioms D0.Research.NativeScenePriceSource.passport_scene_price_source_zero
#check D0.Synthesis.DenseOperatorSceneRigidity.dense_operator_recovers_scene
#print axioms D0.Synthesis.DenseOperatorSceneRigidity.dense_operator_recovers_scene
#check D0.Synthesis.DenseOperatorSceneRigidity.scene_passport_inhabited
#print axioms D0.Synthesis.DenseOperatorSceneRigidity.scene_passport_inhabited
