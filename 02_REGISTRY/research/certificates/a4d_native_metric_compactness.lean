import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import D0.Geometry.A4DRawSolderFrameAction

/-! Finite native Korn estimate and the small centered-gradient chart.
Continuum compactness/regularity and the UV-link sequence are analytic
assemblies in the companion proof, not imported physical axioms. -/
namespace D0.Research.NativeMetricCompactness
open D0 D0.Geometry
open Filter
open scoped BigOperators Topology
noncomputable section
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000
variable {i s : Type*} [Fintype i] [Fintype s]

def pair (x y : s → ℝ) : ℝ := ∑ a, x a*y a
def matrixSquare (A : i → i → ℝ) : ℝ := ∑ r, ∑ a, (A r a)^2
def fieldSquare (A : s → i → i → ℝ) : ℝ := ∑ x, matrixSquare (A x)
def signedGram (sign : i → ℝ) (A B : i → i → ℝ) : i → i → ℝ :=
  fun r a => ∑ k, A r k*sign k*B a k
def metric (sign : i → ℝ) (A : i → i → ℝ) : i → i → ℝ :=
  by
    classical
    exact fun r a => (if r=a then sign r else 0)+A r a+A a r+signedGram sign A A r a

private lemma pair_symm (x y : s → ℝ) : pair x y=pair y x := by
  simp [pair,mul_comm]
private lemma pair_neg_right (x y : s → ℝ) : pair x (-y) = -pair x y := by
  simp [pair,Finset.sum_neg_distrib]
private lemma pair_sum_left (f : i → s → ℝ) (y : s → ℝ) :
    pair (fun a => ∑ r, f r a) y=∑ r, pair (f r) y := by
  simp only [pair,Finset.sum_mul]
  rw [Finset.sum_comm]
private lemma pair_sum_right (x : s → ℝ) (f : i → s → ℝ) :
    pair x (fun a => ∑ r, f r a)=∑ r, pair x (f r) := by
  simp only [pair,Finset.mul_sum]
  rw [Finset.sum_comm]
private lemma pair_square_add (x y : s → ℝ) :
    pair (x+y) (x+y)=pair x x+pair y y+2*pair x y := by
  unfold pair
  simp only [Pi.add_apply]
  have hh : ∀ a, (x a+y a)*(x a+y a)=x a*x a+y a*y a+2*(x a*y a) := by
    intro a;ring
  simp_rw [hh]
  simp only [Finset.sum_add_distrib,←Finset.mul_sum]

theorem matrixSquare_nonneg (A : i → i → ℝ) : 0≤matrixSquare A := by
  exact Finset.sum_nonneg fun r _ => Finset.sum_nonneg fun a _ => sq_nonneg (A r a)
theorem matrixSquare_add_le (A B : i → i → ℝ) :
    matrixSquare (A+B) ≤ 2*matrixSquare A+2*matrixSquare B := by
  calc
    _ ≤ ∑ r, ∑ a, (2*(A r a)^2+2*(B r a)^2) := by
      apply Finset.sum_le_sum;intro r _
      apply Finset.sum_le_sum;intro a _
      change (A r a+B r a)^2≤_
      nlinarith [sq_nonneg (A r a-B r a)]
    _ = _ := by simp [matrixSquare,Finset.sum_add_distrib,Finset.mul_sum]

theorem signedGram_square_le (sign : i → ℝ) (hsign : ∀ r, (sign r)^2=1)
    (A B : i → i → ℝ) :
    matrixSquare (signedGram sign A B) ≤ matrixSquare A*matrixSquare B := by
  have hrow (r a : i) : (signedGram sign A B r a)^2 ≤
      (∑ k, (A r k)^2)*(∑ k, (B a k)^2) := by
    have hh := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
      (fun k => A r k*sign k) (fun k => B a k)
    simpa [signedGram,mul_pow,hsign] using hh
  calc
    _ ≤ ∑ r, ∑ a, (∑ k, (A r k)^2)*(∑ k, (B a k)^2) := by
      apply Finset.sum_le_sum;intro r _
      apply Finset.sum_le_sum;intro a _;exact hrow r a
    _ = _ := by simp only [matrixSquare,←Finset.mul_sum,←Finset.sum_mul]

def metricError (sign : i → ℝ) (A B : i → i → ℝ) : i → i → ℝ :=
  signedGram sign A (A-B)+signedGram sign (A-B) B

theorem metric_difference (sign : i → ℝ) (A B : i → i → ℝ) :
    metric sign A-metric sign B =
      (fun r a => (A-B) r a+(A-B) a r)+metricError sign A B := by
  funext r a
  unfold metric metricError signedGram
  simp only [Pi.sub_apply,Pi.add_apply]
  have hh : (∑ k, A r k*sign k*A a k)-(∑ k, B r k*sign k*B a k)=
      (∑ k, A r k*sign k*(A a k-B a k))+
        (∑ k, (A r k-B r k)*sign k*B a k) := by
    rw [←Finset.sum_sub_distrib,←Finset.sum_add_distrib]
    apply Finset.sum_congr rfl;intro k _;ring
  linarith

theorem metricError_small_chart (sign : i → ℝ) (hsign : ∀ r, (sign r)^2=1)
    (A B : i → i → ℝ) (hA : matrixSquare A≤1/16) (hB : matrixSquare B≤1/16) :
    matrixSquare (metricError sign A B) ≤ matrixSquare (A-B)/4 := by
  have hx := signedGram_square_le sign hsign A (A-B)
  have hy := signedGram_square_le sign hsign (A-B) B
  have hn := matrixSquare_nonneg (A-B)
  have ha := mul_le_mul_of_nonneg_right hA hn
  have hb := mul_le_mul_of_nonneg_left hB hn
  have he := matrixSquare_add_le (signedGram sign A (A-B)) (signedGram sign (A-B) B)
  unfold metricError
  nlinarith

def gradient (D : i → (s → ℝ) →ₗ[ℝ] (s → ℝ)) (w : i → s → ℝ) : s → i → i → ℝ :=
  fun x r a => D r (w a) x
def symField (A : s → i → i → ℝ) : s → i → i → ℝ :=
  fun x r a => A x r a+A x a r
def divergence (D : i → (s → ℝ) →ₗ[ℝ] (s → ℝ)) (w : i → s → ℝ) : s → ℝ :=
  fun x => ∑ r, D r (w r) x

theorem korn_identity (D : i → (s → ℝ) →ₗ[ℝ] (s → ℝ))
    (hskew : ∀ r x y, pair (D r x) y = -pair x (D r y))
    (hcomm : ∀ r a x, D r (D a x)=D a (D r x)) (w : i → s → ℝ) :
    fieldSquare (symField (gradient D w)) =
      2*fieldSquare (gradient D w)+2*pair (divergence D w) (divergence D w) := by
  have cross (r a : i) : pair (D r (w a)) (D a (w r))=
      pair (D r (w r)) (D a (w a)) := by
    rw [hskew,hcomm,←hskew,pair_symm]
  have swap : (∑ r, ∑ a, pair (D a (w r)) (D a (w r)))=
      ∑ r, ∑ a, pair (D r (w a)) (D r (w a)) := by rw [Finset.sum_comm]
  have rewriteEnergy (A : s → i → i → ℝ) : fieldSquare A =
      ∑ r, ∑ a, pair (fun x => A x r a) (fun x => A x r a) := by
    simp only [fieldSquare,matrixSquare,pair,pow_two]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl;intro r _;rw [Finset.sum_comm]
  rw [rewriteEnergy,rewriteEnergy]
  change (∑ r, ∑ a, pair (D r (w a)+D a (w r)) (D r (w a)+D a (w r)))=_
  simp_rw [pair_square_add,cross]
  simp only [Finset.sum_add_distrib,←Finset.mul_sum]
  rw [swap]
  have divexp : pair (divergence D w) (divergence D w)=
      ∑ r, ∑ a, pair (D r (w r)) (D a (w a)) := by
    unfold divergence
    rw [pair_sum_left]
    apply Finset.sum_congr rfl;intro r _;rw [pair_sum_right]
  rw [divexp]
  simp only [gradient]
  ring

theorem korn_coercive (D : i → (s → ℝ) →ₗ[ℝ] (s → ℝ))
    (hskew : ∀ r x y, pair (D r x) y = -pair x (D r y))
    (hcomm : ∀ r a x, D r (D a x)=D a (D r x)) (w : i → s → ℝ) :
    2*fieldSquare (gradient D w)≤fieldSquare (symField (gradient D w)) := by
  rw [korn_identity D hskew hcomm]
  have hn : 0≤pair (divergence D w) (divergence D w) :=
    Finset.sum_nonneg fun x _ => mul_self_nonneg _
  linarith

theorem nonlinear_inverse_square (sign : i → ℝ) (hsign : ∀ r, (sign r)^2=1)
    (A B : s → i → i → ℝ)
    (hA : ∀ x, matrixSquare (A x)≤1/16) (hB : ∀ x, matrixSquare (B x)≤1/16)
    (hk : 2*fieldSquare (A-B)≤fieldSquare (symField (A-B))) :
    fieldSquare (A-B) ≤ (4/3:ℝ)*fieldSquare (fun x => metric sign (A x)-metric sign (B x)) := by
  have he : fieldSquare (fun x => metricError sign (A x) (B x))≤fieldSquare (A-B)/4 := by
    unfold fieldSquare
    calc
      _ ≤ ∑ x, matrixSquare (A x-B x)/4 :=
        Finset.sum_le_sum fun x _ => metricError_small_chart sign hsign (A x) (B x) (hA x) (hB x)
      _ = _ := by simp [Finset.sum_div]
  have ht : fieldSquare (symField (A-B))≤
      2*fieldSquare (fun x => metric sign (A x)-metric sign (B x))+
      2*fieldSquare (fun x => metricError sign (A x) (B x)) := by
    unfold fieldSquare
    calc
      _ ≤ ∑ x, (2*matrixSquare (metric sign (A x)-metric sign (B x))+
          2*matrixSquare (metricError sign (A x) (B x))) := by
        apply Finset.sum_le_sum;intro x _
        have hh := matrixSquare_add_le (metric sign (A x)-metric sign (B x))
          (-metricError sign (A x) (B x))
        have hdiff := metric_difference sign (A x) (B x)
        have hs : symField (A-B) x=(metric sign (A x)-metric sign (B x))+
            -metricError sign (A x) (B x) := by
          funext r a
          have hentry := congrFun (congrFun hdiff r) a
          simp only [symField,Pi.sub_apply,Pi.add_apply,Pi.neg_apply] at hentry ⊢
          linarith
        rw [hs]
        simpa [matrixSquare] using hh
      _ = _ := by simp [Finset.sum_add_distrib,Finset.mul_sum]
  linarith

def nativeCentered (N : ℕ) (xi : LocalRoleVector N) :=
  centeredCoframeMatrix N (forwardGaugeCoframe N xi)

theorem native_centered_binding (N : ℕ) (xi : LocalRoleVector N) :
    nativeCentered N xi=gradient (centeredDifference N) (fun a x => xi x a) := by
  funext x r a
  exact (congrFun (centeredDifference_eq_average_forward N r (fun y => xi y a)) x).symm
theorem native_centered_sub (N : ℕ) (xi psi : LocalRoleVector N) :
    nativeCentered N (xi-psi)=nativeCentered N xi-nativeCentered N psi := by
  simp_rw [native_centered_binding]
  funext x r a
  exact congrFun ((centeredDifference N r).map_sub (fun y => xi y a) (fun y => psi y a)) x
theorem native_centered_curl (N : ℕ) (xi : LocalRoleVector N) (r a b : Role) :
    centeredDifference N r (fun x => nativeCentered N xi x a b)=
      centeredDifference N a (fun x => nativeCentered N xi x r b) := by
  simp_rw [native_centered_binding]
  exact centeredDifference_comm N r a _
theorem native_korn_identity (N : ℕ) (xi : LocalRoleVector N) :
    fieldSquare (symField (nativeCentered N xi))=2*fieldSquare (nativeCentered N xi)+
      2*pair (divergence (centeredDifference N) (fun a x => xi x a))
        (divergence (centeredDifference N) (fun a x => xi x a)) := by
  rw [native_centered_binding]
  exact korn_identity _ (fun r x y => centeredDifference_skew_adjoint N r x y)
    (centeredDifference_comm N) _
theorem native_metric_binding (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (forwardGaugeCoframe N xi) x=
      metric roleLorentzSign (nativeCentered N xi x) := by
  rw [solderMetric_expand]
  funext r a
  simp [metric,nativeCentered,signedGram,Matrix.mul_apply,roleLorentzMetric,Matrix.diagonal_apply]

theorem native_metric_inverse_square (N : ℕ) (xi psi : LocalRoleVector N)
    (hxi : ∀ x, matrixSquare (nativeCentered N xi x)≤1/16)
    (hpsi : ∀ x, matrixSquare (nativeCentered N psi x)≤1/16) :
    fieldSquare (nativeCentered N xi-nativeCentered N psi)≤(4/3:ℝ)*
      fieldSquare (fun x => solderMetricMatrix N (forwardGaugeCoframe N xi) x-
        solderMetricMatrix N (forwardGaugeCoframe N psi) x) := by
  simp_rw [native_metric_binding]
  apply nonlinear_inverse_square roleLorentzSign
  · intro r;simpa [pow_two] using roleLorentzSign_mul_self r
  · exact hxi
  · exact hpsi
  · have hd : (fun x r a => nativeCentered N xi x r a-nativeCentered N psi x r a)=
        gradient (centeredDifference N) (fun a x => xi x a-psi x a) := by
      funext x r a
      simp only [native_centered_binding,gradient]
      exact congrFun ((centeredDifference N r).map_sub
        (fun y => xi y a) (fun y => psi y a)).symm x
    change 2*fieldSquare (fun x r a => nativeCentered N xi x r a-nativeCentered N psi x r a)≤
      fieldSquare (symField (fun x r a => nativeCentered N xi x r a-nativeCentered N psi x r a))
    rw [hd]
    exact korn_coercive _ (fun r x y => centeredDifference_skew_adjoint N r x y)
      (centeredDifference_comm N) _

/-- Actual bounded native potential, not an arbitrary numeric archive code.
The all-even-carrier phase construction is supplied analytically in the proof. -/
theorem native_nyquist_raw_translation (N : ℕ) (z : ArchiveRolePhaseGroup N → ℝ)
    (v : Role → ℝ) (hp : ∀ r x, z (roleTranslatePlus N r x) = -z x) :
    forwardGaugeCoframe N (fun x a => -z x*v a/2) =
      fun x _r a => (archiveFibers N : ℝ)*z x*v a := by
  funext x r a
  simp only [forwardGaugeCoframe,forwardDifference_apply,hp,forwardDifferenceScale]
  ring
theorem native_nyquist_center_zero (N : ℕ) (z : ArchiveRolePhaseGroup N → ℝ)
    (v : Role → ℝ) (hp : ∀ r x, z (roleTranslatePlus N r x) = -z x)
    (hm : ∀ r x, z (roleTranslateMinus N r x) = -z x) :
    nativeCentered N (fun x a => -z x*v a/2)=0 := by
  rw [native_centered_binding]
  funext x r a
  simp [gradient,centeredDifference_apply,hp,hm]

open Matrix
private lemma vec_four_two {α : Type*} (a : α) (u : Fin 3 → α) :
    vecCons a u (2:Fin 4)=u 1 := rfl
private lemma vec_four_three {α : Type*} (a : α) (u : Fin 3 → α) :
    vecCons a u (3:Fin 4)=u 2 := rfl
private lemma vec_three_two {α : Type*} (a : α) (u : Fin 2 → α) :
    vecCons a u (2:Fin 3)=u 1 := rfl
def eta4 : Matrix (Fin 4) (Fin 4) ℝ := !![1,0,0,0;0,-1,0,0;0,0,-1,0;0,0,0,-1]
def raw4 (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1+a,a,0,0;a,-1+a,0,0;a,a,-1,0;a,a,0,-1]
def boostAD (s : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![(1+s^2)/(1-s^2),0,0,2*s/(1-s^2);0,1,0,0;0,0,1,0;
    2*s/(1-s^2),0,0,(1+s^2)/(1-s^2)]
def boostAC (s : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![(1+s^2)/(1-s^2),0,2*s/(1-s^2),0;0,1,0,0;
    2*s/(1-s^2),0,(1+s^2)/(1-s^2),0;0,0,0,1]
def read4 (z h f : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,-1,0,0;
    -z*h*f^2/(1-h^2*f^2),0,-1,z*f/(1-h^2*f^2);
    -z*h*f^2/(1-h^2*f^2),0,-z*f/(1-h^2*f^2),-1]
def pull4 (h f : ℝ) (r : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  if r.val=2 then boostAD (-h*f) else if r.val=3 then boostAC (h*f) else 1

theorem raw4_det (a : ℝ) : (raw4 a).det = -1 := by
  have h0 : raw4 a 0 3=0 := rfl
  have h1 : raw4 a 1 3=0 := rfl
  have h2 : raw4 a 2 3=0 := rfl
  have h3 : raw4 a 3 3= -1 := rfl
  have hm : (raw4 a).submatrix (3:Fin 4).succAbove (3:Fin 4).succAbove=
      !![1+a,a,0;a,-1+a,0;a,a,-1] := by
    ext r c;fin_cases r <;> fin_cases c <;> rfl
  rw [Matrix.det_succ_column _ (3:Fin 4),Fin.sum_univ_four,h0,h1,h2,h3]
  simp only [mul_zero,zero_mul,zero_add,add_zero]
  rw [hm,Matrix.det_fin_three]
  change ((-1:ℝ)^(6:ℕ)) * (-1) *
    ((1+a)*(-1+a)*(-1)-(1+a)*0*a-a*a*(-1)+a*0*a+0*a*a-0*(-1+a)*a)= -1
  ring
theorem boostAD_lorentz (s : ℝ) (hs : 1-s^2≠0) :
    boostAD s*eta4*(boostAD s).transpose=eta4 := by
  ext r a
  fin_cases r <;> fin_cases a <;>
    norm_num [boostAD,eta4,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    field_simp [hs] <;> ring
theorem boostAC_lorentz (s : ℝ) (hs : 1-s^2≠0) :
    boostAC s*eta4*(boostAC s).transpose=eta4 := by
  ext r a
  fin_cases r <;> fin_cases a <;>
    norm_num [boostAC,eta4,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    field_simp [hs] <;> ring

/-- Literal row-pull centering of the two parity endpoints. -/
theorem resonance_center (z h f : ℝ) (hh : h≠0) (hd : 1-h^2*f^2≠0) :
    (fun r a => (raw4 (z/h) r a+(raw4 (-z/h)*pull4 h f r) r a)/2)=read4 z h f := by
  have h0 : pull4 h f 0=1 := rfl
  have h1 : pull4 h f 1=1 := rfl
  have h2 : pull4 h f 2=boostAD (-h*f) := rfl
  have h3 : pull4 h f 3=boostAC (h*f) := rfl
  funext r a
  fin_cases r
  · change (raw4 (z/h) 0 a+(raw4 (-z/h)*pull4 h f 0) 0 a)/2=read4 z h f 0 a
    rw [h0,Matrix.mul_one]
    fin_cases a <;> norm_num [raw4,read4] <;> ring
  · change (raw4 (z/h) 1 a+(raw4 (-z/h)*pull4 h f 1) 1 a)/2=read4 z h f 1 a
    rw [h1,Matrix.mul_one]
    fin_cases a <;> norm_num [raw4,read4] <;> ring
  · change (raw4 (z/h) 2 a+(raw4 (-z/h)*pull4 h f 2) 2 a)/2=read4 z h f 2 a
    rw [h2]
    fin_cases a <;>
      norm_num [raw4,boostAD,read4,Matrix.mul_apply,Fin.sum_univ_succ,vec_four_two,vec_four_three,vec_three_two] <;>
      field_simp [hh,hd] <;> ring
  · change (raw4 (z/h) 3 a+(raw4 (-z/h)*pull4 h f 3) 3 a)/2=read4 z h f 3 a
    rw [h3]
    fin_cases a <;>
      norm_num [raw4,boostAC,read4,Matrix.mul_apply,Fin.sum_univ_succ,vec_four_two,vec_four_three,vec_three_two] <;>
      field_simp [hh,hd] <;> ring

theorem resonance_gram (z h f : ℝ) (hz : z^2=1) (hd : 1-h^2*f^2≠0) :
    read4 z h f*eta4*(read4 z h f).transpose=
      !![1,0,-z*h*f^2/(1-h^2*f^2),-z*h*f^2/(1-h^2*f^2);
         0,-1,0,0;
         -z*h*f^2/(1-h^2*f^2),0,-1-f^2/(1-h^2*f^2),h^2*f^4/(1-h^2*f^2)^2;
         -z*h*f^2/(1-h^2*f^2),0,h^2*f^4/(1-h^2*f^2)^2,-1-f^2/(1-h^2*f^2)] := by
  ext r a
  fin_cases r <;> fin_cases a <;>
    norm_num [read4,eta4,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    field_simp [hd] <;> ring_nf <;> simp only [hz] <;> ring

/-- Coordinate formula for the already classified composed frozen vertex map.
This is a research construction, not a newly selected physical refinement. -/
def frozenPhaseCap (Nc Nf : ℕ)
    (y : ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint Nf) :
    ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint Nc :=
  fun r => if h : (y r).val < Nc+2 then ⟨(y r).val,h⟩ else 0

/-- The scale-corrected composed one-form block, in the literal point/group
coordinates. Internal frame columns are not discarded. -/
def frozenNativeCoframe (Nc Nf : ℕ) (e : LocalCoframeField Nc) :
    LocalCoframeField Nf :=
  fun x r a =>
    let y := (archiveRolePhasePointGroupEquiv Nf).symm x
    if (y r).val < Nc+2 then
      ((Nf+2 : ℝ)/(Nc+2 : ℝ)) *
        e (archiveRolePhasePointGroupEquiv Nc (frozenPhaseCap Nc Nf y)) r a
    else 0

theorem frozen_native_tail_zero (Nc Nf : ℕ) (e : LocalCoframeField Nc)
    (x : ArchiveRolePhaseGroup Nf)
    (hx : ∀ r, Nc+2 ≤ (((archiveRolePhasePointGroupEquiv Nf).symm x) r).val) :
    rawSolderMatrix Nf (frozenNativeCoframe Nc Nf e) x = roleLorentzMetric := by
  ext r a
  simp [rawSolderMatrix,frozenNativeCoframe,not_lt_of_ge (hx r)]

/-- All incoming rows use the actual native transported-center owner. -/
theorem native_flat_bulk_center (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) (hx : E x=roleLorentzMetric)
    (hm : ∀ r, E (roleTranslateMinus N r x)=roleLorentzMetric) (r a : Role) :
    transportedSolderCenter N E R x r a-roleLorentzMetric r a =
      roleLorentzSign r *
        (R (roleTranslateMinus N r x) r r a-(1 : Matrix Role Role ℝ) r a)/2 := by
  simp only [transportedSolderCenter,hx,hm,roleLorentzMetric,Matrix.diagonal_mul]
  by_cases hra : r=a
  · simp [Matrix.one_apply,hra]; ring
  · simp [hra]

private lemma native_sign_abs (r : Role) : |roleLorentzSign r|=1 := by
  have h := roleLorentzSign_mul_self r
  nlinarith [sq_abs (roleLorentzSign r),abs_nonneg (roleLorentzSign r)]

theorem native_flat_bulk_center_bound (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) (hx : E x=roleLorentzMetric)
    (hm : ∀ r, E (roleTranslateMinus N r x)=roleLorentzMetric)
    (δ : ℝ) (hR : ∀ r a,
      |R (roleTranslateMinus N r x) r r a-(1 : Matrix Role Role ℝ) r a|≤δ)
    (r a : Role) :
    |transportedSolderCenter N E R x r a-roleLorentzMetric r a|≤δ/2 := by
  rw [native_flat_bulk_center N E R x hx hm r a,abs_div,abs_mul,native_sign_abs]
  norm_num only [abs_of_pos (by norm_num : (0:ℝ)<2),one_mul]
  exact div_le_div_of_nonneg_right (hR r a) (by norm_num)

/-- Exact expansion at the flat bulk, with every matrix component retained. -/
theorem native_flat_gram_expansion (H : Matrix Role Role ℝ) :
    (roleLorentzMetric+H)*roleLorentzMetric*(roleLorentzMetric+H).transpose=
      metric roleLorentzSign H := by
  rw [Matrix.transpose_add,roleLorentzMetric_transpose]
  simp only [Matrix.add_mul,Matrix.mul_add,roleLorentzMetric_sq,Matrix.one_mul]
  rw [Matrix.mul_assoc H roleLorentzMetric roleLorentzMetric,
    roleLorentzMetric_sq,Matrix.mul_one]
  ext r a
  simp [metric,signedGram,Matrix.mul_apply,roleLorentzMetric,Matrix.diagonal_apply]
  ring

theorem native_flat_gram_entry_bound (H : Matrix Role Role ℝ) (δ : ℝ)
    (hδ : 0≤δ) (hH : ∀ r a, |H r a|≤δ/2) (r a : Role) :
    |((roleLorentzMetric+H)*roleLorentzMetric*(roleLorentzMetric+H).transpose)
       r a-roleLorentzMetric r a| ≤ δ+δ^2 := by
  rw [native_flat_gram_expansion]
  have hterm (k : Role) : |H r k*roleLorentzSign k*H a k|≤δ^2/4 := by
    rw [abs_mul,abs_mul,native_sign_abs,mul_one]
    have hh := mul_le_mul (hH r k) (hH a k) (abs_nonneg (H a k))
      (by positivity : 0≤δ/2)
    nlinarith
  have hsum : |signedGram roleLorentzSign H H r a|≤δ^2 := by
    calc
      _ ≤ ∑ k : Role, |H r k*roleLorentzSign k*H a k| := by
        exact Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ _k : Role, δ^2/4 := Finset.sum_le_sum fun k _ => hterm k
      _ = δ^2 := by simp;ring
  have hmetric : metric roleLorentzSign H r a-roleLorentzMetric r a=
      H r a+H a r+signedGram roleLorentzSign H H r a := by
    simp [metric,roleLorentzMetric,Matrix.diagonal_apply]
    ring
  rw [hmetric]
  calc
    _ ≤ |H r a+H a r|+|signedGram roleLorentzSign H H r a| := abs_add_le _ _
    _ ≤ (|H r a|+|H a r|)+|signedGram roleLorentzSign H H r a| := by
      linarith [abs_add_le (H r a) (H a r)]
    _ ≤ δ+δ^2 := by linarith [hH r a,hH a r]

theorem native_transported_gram_frame_invariant (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R R' : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) (hΛ : ∀ y, IsUnit (Λ y).det)
    (hL : IsRoleLorentz (Λ x))
    (hR : ∀ r, R' (roleTranslateMinus N r x) r=
      (Λ (roleTranslateMinus N r x))⁻¹*R (roleTranslateMinus N r x) r*Λ x) :
    transportedSolderCenter N (fun y => E y*Λ y) R' x*roleLorentzMetric*
      (transportedSolderCenter N (fun y => E y*Λ y) R' x).transpose=
    transportedSolderCenter N E R x*roleLorentzMetric*
      (transportedSolderCenter N E R x).transpose := by
  rw [transportedSolderCenter_covariance N E Λ R R' x hΛ hR]
  exact rawSolderGram_frame_invariant _ _ hL

theorem resonance_two_component_gap (f d : ℝ) (hf : (1/32:ℝ)≤f)
    (hd : 0<d) (hd1 : d≤1) :
    2/(32:ℝ)^4 ≤ 2*(f^2/d)^2 := by
  have hs : (1/1024:ℝ)≤f^2 := by nlinarith
  have hg : f^2≤f^2/d := by
    apply (le_div_iff₀ hd).mpr
    exact mul_le_of_le_one_right (sq_nonneg f) hd1
  nlinarith [sq_nonneg (f^2/d-1/1024)]

/-- The fixed-background affine version of doubling also fails to preserve
the full nondegenerate raw carrier. This is an input-state witness, not an
on-shell counterexample. -/
theorem affine_frozen_doubling_degeneracy :
    (roleLorentzMetric+(-1/2:ℝ) • roleLorentzMetric).det≠0 ∧
    roleLorentzMetric+(2:ℝ) • ((-1/2:ℝ) • roleLorentzMetric)=0 := by
  have hd : roleLorentzMetric.det≠0 := by
    intro h
    have hh := congrArg Matrix.det roleLorentzMetric_sq
    rw [Matrix.det_mul,h,zero_mul,Matrix.det_one] at hh
    norm_num at hh
  have hm : roleLorentzMetric+(-1/2:ℝ) • roleLorentzMetric=
      (1/2:ℝ) • roleLorentzMetric := by ext r a;simp;ring
  refine ⟨?_,?_⟩
  · rw [hm,Matrix.det_smul]
    exact mul_ne_zero (pow_ne_zero _ (by norm_num)) hd
  · ext r a;simp;ring

/-- Pointwise full raw binding of the already owned composed frozen block.
The phase projection and row weights are data, not selected physical arrows. -/
theorem frozen_native_pointwise_affine_binding (Nc Nf : ℕ)
    (e : LocalCoframeField Nc) (x : ArchiveRolePhaseGroup Nf) :
    let y := (archiveRolePhasePointGroupEquiv Nf).symm x
    let z := archiveRolePhasePointGroupEquiv Nc (frozenPhaseCap Nc Nf y)
    let d : Role → ℝ := fun r => if (y r).val<Nc+2 then
      ((Nf+2 : ℝ)/(Nc+2 : ℝ)) else 0
    rawSolderMatrix Nf (frozenNativeCoframe Nc Nf e) x =
      roleLorentzMetric+Matrix.diagonal d*
        (rawSolderMatrix Nc e z-roleLorentzMetric) := by
  dsimp
  ext r a
  simp only [rawSolderMatrix,frozenNativeCoframe,Matrix.add_apply,
    Matrix.sub_apply,Matrix.diagonal_mul]
  split_ifs <;> simp

/-- The full tangent of the actual raw Gram map, with a genuine derivative. -/
theorem native_flat_gram_curve_derivative (H : Matrix Role Role ℝ) (r a : Role) :
    HasDerivAt (fun t : ℝ =>
      ((roleLorentzMetric+t • H)*roleLorentzMetric*
        (roleLorentzMetric+t • H).transpose) r a) (H r a+H a r) 0 := by
  have hp : HasDerivAt (fun t : ℝ => roleLorentzMetric r a+
      t*(H r a+H a r)+t^2*signedGram roleLorentzSign H H r a)
      (H r a+H a r) 0 := by
    simpa using ((hasDerivAt_const (0:ℝ) (roleLorentzMetric r a)).add
      ((hasDerivAt_id 0).mul_const (H r a+H a r))).add
      (((hasDerivAt_id 0).pow 2).mul_const (signedGram roleLorentzSign H H r a))
  convert hp using 1
  funext t
  rw [native_flat_gram_expansion]
  simp only [metric,signedGram,Matrix.smul_apply,smul_eq_mul,
    roleLorentzMetric,Matrix.diagonal_apply]
  simp_rw [show ∀ k, (t*H r k)*roleLorentzSign k*(t*H a k)=
    t^2*(H r k*roleLorentzSign k*H a k) from fun k => by ring]
  rw [Finset.mul_sum]
  ring

/-- Every infinitesimal proper Lorentz frame yields an antisymmetric raw
coframe tangent S=eta*A. Unequal external row weights have a metric defect. -/
theorem gauge_mask_jet_iff_constant (d : i → ℝ) :
    (∀ S : Matrix i i ℝ, S.transpose = -S →
      ∀ r a, d r*S r a+d a*S a r=0) ↔ ∀ r a, d r=d a := by
  classical
  constructor
  · intro h r a
    by_cases he : r=a
    · simp [he]
    let S : Matrix i i ℝ := fun u v =>
      (if u=r ∧ v=a then 1 else 0)-(if u=a ∧ v=r then 1 else 0)
    have hs : S.transpose = -S := by
      ext u v
      change S v u= -S u v
      simp only [S,and_comm]
      ring
    have hh := h S hs r a
    simp [S,he,Ne.symm he] at hh
    linarith
  · intro h S hs r a
    have hh := congrArg (fun M : Matrix i i ℝ => M r a) hs
    change S a r= -S r a at hh
    rw [hh,h a r]
    ring

def rotationBC4 (c z : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,c,z,0;0,-z,c,0;0,0,0,1]
def maskedRotation4 (b k c z : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,-1+b*(1-c),-b*z,0;
    0,k*z,-1+k*(1-c),0;0,0,0,-1]

/-- Proper spatial rotation; its future component is one. The determinant
and connected rational path are checked independently in the exact capsule. -/
theorem rotationBC4_lorentz (c z : ℝ) (h : c^2+z^2=1) :
    rotationBC4 c z*eta4*(rotationBC4 c z).transpose=eta4 := by
  ext r a
  fin_cases r <;> fin_cases a <;>
    norm_num [rotationBC4,eta4,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    nlinarith

/-- All row masks, rather than only a selected fine point. -/
theorem masked_rotation_metric_BC (b k c z : ℝ) :
    (maskedRotation4 b k c z*eta4*(maskedRotation4 b k c z).transpose) 1 2=
      (k-b)*z := by
  norm_num [maskedRotation4,eta4,Matrix.mul_apply,Fin.sum_univ_succ,
    vec_four_two,vec_four_three,vec_three_two]
  ring

theorem masked_rotation_partial_det (b c z : ℝ) :
    (maskedRotation4 b 0 c z).det= -1+b*(1-c) := by
  have hm : (maskedRotation4 b 0 c z).submatrix
      (3:Fin 4).succAbove (3:Fin 4).succAbove=
      !![1,0,0;0,-1+b*(1-c),-b*z;0,0,-1] := by
    ext r a
    fin_cases r <;> fin_cases a <;>
      first | rfl | (change (0:ℝ)*z=0;ring) |
        (change -1+(0:ℝ)*(1-c)= -1;ring)
  have h0 : maskedRotation4 b 0 c z 0 3=0 := rfl
  have h1 : maskedRotation4 b 0 c z 1 3=0 := rfl
  have h2 : maskedRotation4 b 0 c z 2 3=0 := rfl
  have h3 : maskedRotation4 b 0 c z 3 3= -1 := rfl
  rw [Matrix.det_succ_column _ (3:Fin 4),Fin.sum_univ_four,h0,h1,h2,h3]
  simp only [mul_zero,zero_mul,zero_add,add_zero]
  rw [hm,Matrix.det_fin_three]
  change ((-1:ℝ)^(6:ℕ))*(-1)*
    (1*(-1+b*(1-c))*(-1)-1*(-b*z)*0-0*0*(-1)+0*(-b*z)*0+
      0*0*0-0*(-1+b*(1-c))*0)= -1+b*(1-c)
  ring

/-- The curve may be nonlinear. Only its first sine jet is used. For the
proper Cayley rotation z(t)=2t/(1+t^2), dz=2 at zero. -/
theorem masked_rotation_genuine_metric_derivative (b k : ℝ) (c z : ℝ → ℝ)
    (dz : ℝ) (hz : HasDerivAt z dz 0) :
    HasDerivAt (fun t : ℝ =>
      (maskedRotation4 b k (c t) (z t)*eta4*
        (maskedRotation4 b k (c t) (z t)).transpose) 1 2)
      ((k-b)*dz) 0 := by
  simpa only [masked_rotation_metric_BC] using hz.const_mul (k-b)

/-- Actual proper rational frame curve: the sine jet is derived, not a
hypothesis carrying the wanted nonzero metric derivative. -/
theorem cayley_rotation_actual_metric_derivative (b k : ℝ) :
    HasDerivAt (fun t : ℝ =>
      (maskedRotation4 b k ((1-t^2)/(1+t^2)) (2*t/(1+t^2))*eta4*
        (maskedRotation4 b k ((1-t^2)/(1+t^2)) (2*t/(1+t^2))).transpose) 1 2)
      (2*(k-b)) 0 := by
  have hn := (hasDerivAt_id (0:ℝ)).const_mul 2
  have hd := (hasDerivAt_const (0:ℝ) (1:ℝ)).add ((hasDerivAt_id 0).pow 2)
  have hz : HasDerivAt (fun t : ℝ => 2*t/(1+t^2)) 2 0 := by
    simpa using hn.div hd (by norm_num)
  simpa only [mul_comm] using masked_rotation_genuine_metric_derivative
    b k (fun t => (1-t^2)/(1+t^2)) (fun t => 2*t/(1+t^2)) 2 hz

/-- A real nonzero metric jet cannot be the constant metric of one Lorentz
orbit. This includes every differentiable completion with the same jet. -/
theorem nonzero_metric_jet_not_orbit_constant (f : ℝ → ℝ) (v : ℝ)
    (h : HasDerivAt f v 0) (hv : v≠0) :
    ¬ f =ᶠ[𝓝 (0:ℝ)] (fun _ => f 0) := by
  intro hc
  have hh := (h.congr_of_eventuallyEq hc.symm).unique
    (hasDerivAt_const (0:ℝ) (f 0))
  exact hv hh

/-- The same literal fixed-reference raw formula, in the certificate's
four-index order. No replacement transition is selected. -/
def frozenAffineRaw4 (d : Fin 4 → ℝ) (F : Matrix (Fin 4) (Fin 4) ℝ) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  fun r a => eta4 r a+d r*(F r a-eta4 r a)

/-- At a B-active/C-inactive prefix point, the entire fine raw metric's
BC entry reads the coarse BC entry. Other rows and all links are arbitrary. -/
theorem frozen_partial_metric_reads_any_raw_row
    (d : Fin 4 → ℝ) (F : Matrix (Fin 4) (Fin 4) ℝ)
    (rho : ℝ) (hb : d 1=rho) (hc : d 2=0) :
    (frozenAffineRaw4 d F*eta4*(frozenAffineRaw4 d F).transpose) 1 2 =
      rho*F 1 2 := by
  simp [frozenAffineRaw4,eta4,Matrix.mul_apply,Matrix.transpose_apply,
    Fin.sum_univ_four,hb,hc]

def rotationCD4 (c z : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1,0,0,0;0,1,0,0;0,0,c,z;0,0,-z,c]

/-- Four fixed connected proper frames suffice; no open admission domain
or continuum family is assumed. -/
def columnCFrames4 : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ :=
  ![rotationBC4 (255/257) (32/257),
    rotationBC4 (255/257) (-32/257),
    boostAC (1/16),rotationCD4 (255/257) (32/257)]

theorem rotationCD4_lorentz (c z : ℝ) (h : c^2+z^2=1) :
    rotationCD4 c z*eta4*(rotationCD4 c z).transpose=eta4 := by
  ext r a
  fin_cases r <;> fin_cases a <;>
    norm_num [rotationCD4,eta4,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    nlinarith [h]

theorem columnCFrames4_lorentz (j : Fin 4) :
    columnCFrames4 j*eta4*(columnCFrames4 j).transpose=eta4 := by
  fin_cases j
  · exact rotationBC4_lorentz _ _ (by norm_num)
  · exact rotationBC4_lorentz _ _ (by norm_num)
  · exact boostAC_lorentz _ (by norm_num)
  · exact rotationCD4_lorentz _ _ (by norm_num)

/-- Constancy of a single row's C component under these four actual
Lorentz changes forces every component of that row to vanish. -/
theorem four_proper_frames_force_raw_row_zero
    (F : Matrix (Fin 4) (Fin 4) ℝ) (r : Fin 4)
    (h : ∀ j, (F*columnCFrames4 j) r 2=F r 2) :
    ∀ a, F r a=0 := by
  have h0 := h 0
  have h1 := h 1
  have h2 := h 2
  have h3 := h 3
  norm_num [columnCFrames4,rotationBC4,rotationCD4,boostAC,
    Matrix.mul_apply,Fin.sum_univ_four,vec_four_two,vec_four_three,vec_three_two] at h0 h1 h2 h3
  have hC : F r 2=0 := by linarith
  have hB : F r 1=0 := by linarith
  have hA : F r 0=0 := by linarith
  have hD : F r 3=0 := by linarith
  intro a
  fin_cases a <;> assumption

/-- Universal admission obstruction: no invertible coarse raw matrix can
have a frozen partial-mask output whose Gram stays constant on its entire
proper Lorentz orbit. The finite four-frame test already contradicts det≠0. -/
theorem nondegenerate_raw_orbit_has_frozen_metric_defect
    (d : Fin 4 → ℝ) (F : Matrix (Fin 4) (Fin 4) ℝ) (rho : ℝ)
    (hb : d 1=rho) (hc : d 2=0) (hrho : rho≠0) (hF : F.det≠0) :
    ∃ j, (frozenAffineRaw4 d (F*columnCFrames4 j)*eta4*
        (frozenAffineRaw4 d (F*columnCFrames4 j)).transpose) 1 2 ≠
      (frozenAffineRaw4 d F*eta4*(frozenAffineRaw4 d F).transpose) 1 2 := by
  by_contra hn
  have heq : ∀ j, (F*columnCFrames4 j) 1 2=F 1 2 := by
    intro j
    have he := not_not.mp ((not_exists.mp hn) j)
    rw [frozen_partial_metric_reads_any_raw_row d _ rho hb hc,
      frozen_partial_metric_reads_any_raw_row d _ rho hb hc] at he
    exact mul_left_cancel₀ hrho he
  have hz := four_proper_frames_force_raw_row_zero F 1 heq
  exact hF (Matrix.det_eq_zero_of_row_eq_zero (1:Fin 4) hz)

/-- The obstruction also rules out isolated or nonlinear solution sets:
any claimed full-state admission that is gauge closed and has the literal
raw frame binding must be empty if this frozen Gram descends to its orbits.
Links, shifts and matter may be arbitrary fields inside X. -/
theorem frozen_gauge_saturated_admission_empty
    {X : Type*} (raw : X → Matrix (Fin 4) (Fin 4) ℝ)
    (act : Fin 4 → X → X) (admit : X → Prop)
    (d : Fin 4 → ℝ) (rho : ℝ) (hb : d 1=rho) (hc : d 2=0) (hrho : rho≠0)
    (hraw : ∀ j x, raw (act j x)=raw x*columnCFrames4 j)
    (hclosed : ∀ j x, admit x → admit (act j x))
    (hnondeg : ∀ x, admit x → (raw x).det≠0)
    (hGram : ∀ j x, admit x → admit (act j x) →
      (frozenAffineRaw4 d (raw (act j x))*eta4*
        (frozenAffineRaw4 d (raw (act j x))).transpose) 1 2 =
      (frozenAffineRaw4 d (raw x)*eta4*(frozenAffineRaw4 d (raw x)).transpose) 1 2) :
    ¬ ∃ x, admit x := by
  rintro ⟨x,hx⟩
  obtain ⟨j,hj⟩ := nondegenerate_raw_orbit_has_frozen_metric_defect
    d (raw x) rho hb hc hrho (hnondeg x hx)
  have he := hGram j x hx (hclosed j x hx)
  rw [hraw] at he
  exact hj he

/-- Every strict native cycle refinement has an actual B-prefix/C-tail
point. This is not a flat-state or large-scale hypothesis. -/
theorem native_partial_mask_exists (Nc Nf : ℕ) (h : Nc<Nf) :
    ∃ x : ArchiveRolePhaseGroup Nf,
      let y := (archiveRolePhasePointGroupEquiv Nf).symm x
      (y (0,1)).val<Nc+2 ∧ Nc+2≤(y (1,0)).val := by
  let y : ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint Nf :=
    fun r => if r=(1,0) then ⟨Nc+2,by change Nc+2<Nf+2; omega⟩ else 0
  refine ⟨archiveRolePhasePointGroupEquiv Nf y,?_⟩
  simp [y]

end
end D0.Research.NativeMetricCompactness
open D0.Research.NativeMetricCompactness
#print axioms matrixSquare_nonneg
#print axioms matrixSquare_add_le
#print axioms signedGram_square_le
#print axioms metric_difference
#print axioms metricError_small_chart
#print axioms korn_identity
#print axioms korn_coercive
#print axioms nonlinear_inverse_square
#print axioms native_centered_binding
#print axioms native_centered_sub
#print axioms native_centered_curl
#print axioms native_korn_identity
#print axioms native_metric_binding
#print axioms native_metric_inverse_square
#print axioms native_nyquist_raw_translation
#print axioms native_nyquist_center_zero
#print axioms raw4_det
#print axioms boostAD_lorentz
#print axioms boostAC_lorentz
#print axioms resonance_center
#print axioms resonance_gram
#print axioms frozen_native_tail_zero
#print axioms native_flat_bulk_center
#print axioms native_flat_bulk_center_bound
#print axioms native_flat_gram_expansion
#print axioms native_flat_gram_entry_bound
#print axioms native_transported_gram_frame_invariant
#print axioms resonance_two_component_gap
#print axioms affine_frozen_doubling_degeneracy
#check signedGram_square_le
#check metricError_small_chart
#check korn_identity
#check nonlinear_inverse_square
#check native_centered_binding
#check native_korn_identity
#check native_metric_binding
#check native_metric_inverse_square
#check native_nyquist_raw_translation
#check native_nyquist_center_zero
#check raw4_det
#check resonance_center
#check resonance_gram
#check frozen_native_tail_zero
#check native_flat_bulk_center
#check native_flat_bulk_center_bound
#check native_flat_gram_expansion
#check native_flat_gram_entry_bound
#check native_transported_gram_frame_invariant
#check resonance_two_component_gap
#check affine_frozen_doubling_degeneracy

#print axioms frozen_native_pointwise_affine_binding
#check frozen_native_pointwise_affine_binding
#print axioms native_flat_gram_curve_derivative
#check native_flat_gram_curve_derivative
#print axioms gauge_mask_jet_iff_constant
#check gauge_mask_jet_iff_constant
#print axioms rotationBC4_lorentz
#check rotationBC4_lorentz
#print axioms masked_rotation_metric_BC
#check masked_rotation_metric_BC
#print axioms masked_rotation_partial_det
#check masked_rotation_partial_det
#print axioms masked_rotation_genuine_metric_derivative
#check masked_rotation_genuine_metric_derivative
#print axioms nonzero_metric_jet_not_orbit_constant
#check nonzero_metric_jet_not_orbit_constant

#print axioms cayley_rotation_actual_metric_derivative
#check cayley_rotation_actual_metric_derivative

#print axioms frozen_partial_metric_reads_any_raw_row
#check frozen_partial_metric_reads_any_raw_row
#print axioms rotationCD4_lorentz
#check rotationCD4_lorentz
#print axioms columnCFrames4_lorentz
#check columnCFrames4_lorentz
#print axioms four_proper_frames_force_raw_row_zero
#check four_proper_frames_force_raw_row_zero
#print axioms nondegenerate_raw_orbit_has_frozen_metric_defect
#check nondegenerate_raw_orbit_has_frozen_metric_defect
#print axioms frozen_gauge_saturated_admission_empty
#check frozen_gauge_saturated_admission_empty
#print axioms native_partial_mask_exists
#check native_partial_mask_exists
