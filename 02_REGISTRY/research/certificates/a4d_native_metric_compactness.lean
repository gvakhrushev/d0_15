import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import D0.Geometry.A4DRawSolderFrameAction

/-! Finite native Korn estimate and the small centered-gradient chart.
Continuum compactness/regularity and the UV-link sequence are analytic
assemblies in the companion proof, not imported physical axioms. -/
namespace D0.Research.NativeMetricCompactness
open D0 D0.Geometry
open scoped BigOperators
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
