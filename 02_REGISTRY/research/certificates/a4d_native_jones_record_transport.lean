import D0.Representation.GoldenCoherentMemory
import D0.Representation.GoldenOrderInterferometer
import Mathlib.Tactic

/-! Research kernel for coherent Jones-corner transport. Rectangular frames,
traciality and the AF embedding are explicit hypotheses. The all-level native
path binding is separate exact-certificate evidence. No physical actuation,
metric stationarity, or classification of all native preparations is asserted. -/
namespace D0.Research.JonesRecordTransport
noncomputable section
open Matrix

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

/-- The literal owned two-port gate has the required double angle. -/
theorem owned_gate_square (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    D0.Representation.GoldenOrderInterferometer.gate a p *
      D0.Representation.GoldenOrderInterferometer.gate a p =
      D0.Representation.GoldenOrderInterferometer.gate (p^3) (2*a*p) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [D0.Representation.GoldenOrderInterferometer.gate,
      Matrix.mul_apply, Fin.sum_univ_two]
  all_goals nlinarith [D0.Representation.GoldenOrderInterferometer.golden_cube p hp]

theorem golden_coefficients (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1)
    (ha0 : 0<a) (hp0 : 0<p) :
    p^3=2*p-1 ∧ (p^3)^2+(2*a*p)^2=1 ∧ 0<2*a*p := by
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  have hr := D0.Representation.GoldenOrderInterferometer.golden_response_closure p hp
  refine ⟨by nlinarith, ?_, by positivity⟩
  calc
    _ = p^6+4*p^3 := by nlinarith [sq_nonneg (a*p)]
    _ = 1 := hr

def residual (G F : Matrix m n ℝ) (c s : ℝ) : Matrix m n ℝ :=
  s⁻¹ • (F-c • G)

omit [Fintype n] [DecidableEq m] in
/-- Gram--Schmidt on equal-overlap frames, with the nonzero denominator exposed. -/
theorem residual_frame (G F : Matrix m n ℝ) (c s : ℝ)
    (hG : G.transpose*G=1) (hF : F.transpose*F=1)
    (hFG : F.transpose*G=c • (1 : Matrix n n ℝ))
    (hcs : c^2+s^2=1) (hs : s≠0) :
    G.transpose*residual G F c s=0 ∧
    (residual G F c s).transpose*residual G F c s=1 := by
  have hGF : G.transpose*F=c • (1 : Matrix n n ℝ) := by
    have h := congrArg Matrix.transpose hFG
    simpa using h
  have hn : s⁻¹*s⁻¹*(1-c*c)=1 := by
    field_simp
    nlinarith
  constructor
  · simp [residual, Matrix.mul_sub, hGF, hG]
  · simp only [residual, Matrix.transpose_smul, Matrix.transpose_sub,
      Matrix.smul_mul, Matrix.mul_smul, Matrix.sub_mul, Matrix.mul_sub,
      hG, hF, hGF, hFG]
    calc
      _ = (s⁻¹*s⁻¹*(1-c*c)) • (1 : Matrix n n ℝ) := by module
      _ = 1 := by rw [hn]; simp

/-- Identity on the orthogonal complement is retained in the definition. -/
def plane (G H : Matrix m n ℝ) (c s : ℝ) : Matrix m m ℝ :=
  c • (G*G.transpose) - s • (G*H.transpose) +
  s • (H*G.transpose) + c • (H*H.transpose) +
  (1-G*G.transpose-H*H.transpose)

omit [DecidableEq m] [Fintype n] [DecidableEq n] in
theorem cross_transpose (G H : Matrix m n ℝ) (h : G.transpose*H=0) :
    H.transpose*G=0 := by
  simpa using congrArg Matrix.transpose h

theorem plane_on_frames (G H : Matrix m n ℝ) (c s : ℝ)
    (hG : G.transpose*G=1) (hH : H.transpose*H=1)
    (hGH : G.transpose*H=0) :
    plane G H c s * G = c • G+s • H ∧
    plane G H c s * H = -s • G+c • H := by
  have hHG := cross_transpose G H hGH
  constructor <;>
    simp [plane, Matrix.add_mul, Matrix.sub_mul, Matrix.mul_assoc, hG,hH,hGH,hHG]

omit [DecidableEq n] in
theorem complement_pointwise_fixed (G H Z : Matrix m n ℝ) (c s : ℝ)
    (hGZ : G.transpose*Z=0) (hHZ : H.transpose*Z=0) :
    plane G H c s*Z=Z := by
  simp [plane,Matrix.add_mul,Matrix.sub_mul,Matrix.mul_assoc,hGZ,hHZ]

omit [Fintype m] [DecidableEq n] in
theorem plane_transpose (G H : Matrix m n ℝ) (c s : ℝ) :
    (plane G H c s).transpose=plane G H c (-s) := by
  simp only [plane, Matrix.transpose_add, Matrix.transpose_sub,
    Matrix.transpose_smul, Matrix.transpose_mul, Matrix.transpose_transpose,
    Matrix.transpose_one]
  module

theorem plane_composition (G H : Matrix m n ℝ) (c s u v : ℝ)
    (hG : G.transpose*G=1) (hH : H.transpose*H=1)
    (hGH : G.transpose*H=0) :
    plane G H c s * plane G H u v = plane G H (c*u-s*v) (c*v+s*u) := by
  have hHG := cross_transpose G H hGH
  have hGG (X : Matrix n m ℝ) : G.transpose*(G*X)=X := by
    rw [← Matrix.mul_assoc,hG,Matrix.one_mul]
  have hHH (X : Matrix n m ℝ) : H.transpose*(H*X)=X := by
    rw [← Matrix.mul_assoc,hH,Matrix.one_mul]
  have hGHX (X : Matrix n m ℝ) : G.transpose*(H*X)=0 := by
    rw [← Matrix.mul_assoc,hGH,Matrix.zero_mul]
  have hHGX (X : Matrix n m ℝ) : H.transpose*(G*X)=0 := by
    rw [← Matrix.mul_assoc,hHG,Matrix.zero_mul]
  simp only [plane, Matrix.add_mul, Matrix.sub_mul, Matrix.mul_add,
    Matrix.mul_sub, Matrix.smul_mul, Matrix.mul_smul, Matrix.mul_assoc,
    hGG,hHH,hGHX,hHGX,Matrix.one_mul,Matrix.mul_one,Matrix.mul_zero,
    smul_zero]
  module

theorem plane_orthogonal (G H : Matrix m n ℝ) (c s : ℝ)
    (hG : G.transpose*G=1) (hH : H.transpose*H=1)
    (hGH : G.transpose*H=0) (hcs : c^2+s^2=1) :
    (plane G H c s).transpose*plane G H c s=1 := by
  rw [plane_transpose, plane_composition G H c (-s) c s hG hH hGH]
  have h1 : c*c-(-s)*s=1 := by nlinarith
  have h0 : c*s+(-s)*c=0 := by ring
  rw [h1,h0]
  simp [plane]

theorem owned_plane_square (G H : Matrix m n ℝ) (a p : ℝ)
    (hG : G.transpose*G=1) (hH : H.transpose*H=1)
    (hGH : G.transpose*H=0) (ha : a^2=p) (hp : p+p^2=1) :
    plane G H a p * plane G H a p = plane G H (p^3) (2*a*p) := by
  rw [plane_composition G H a p a p hG hH hGH]
  have hc : a*a-p*p=p^3 := by
    nlinarith [D0.Representation.GoldenOrderInterferometer.golden_cube p hp]
  have hs : a*p+p*a=2*a*p := by ring
  rw [hc,hs]

/-- A concrete transport from the original frame to the adjacent Jones frame. -/
theorem residual_transport (G F : Matrix m n ℝ) (c s : ℝ)
    (hG : G.transpose*G=1) (hF : F.transpose*F=1)
    (hFG : F.transpose*G=c • (1 : Matrix n n ℝ))
    (hcs : c^2+s^2=1) (hs : s≠0) :
    plane G (residual G F c s) c s * G=F := by
  obtain ⟨hGH,hH⟩ := residual_frame G F c s hG hF hFG hcs hs
  rw [(plane_on_frames G (residual G F c s) c s hG hH hGH).1]
  simp only [residual, smul_smul, mul_inv_cancel₀ hs, one_smul]
  module

/-- Two identical applications of the owned gate transport the whole corner.
No inverse trigonometric function or angle chosen by fitting occurs. -/
theorem owned_square_transport (G F : Matrix m n ℝ) (a p : ℝ)
    (hG : G.transpose*G=1) (hF : F.transpose*F=1)
    (hFG : F.transpose*G=(p^3) • (1 : Matrix n n ℝ))
    (ha : a^2=p) (hp : p+p^2=1) (ha0 : 0<a) (hp0 : 0<p) :
    let H := residual G F (p^3) (2*a*p)
    let R := plane G H a p * plane G H a p
    R.transpose*R=1 ∧ R*R.transpose=1 ∧ R*G=F := by
  dsimp only
  obtain ⟨_,hcs,hs0⟩ := golden_coefficients a p ha hp ha0 hp0
  have hs := ne_of_gt hs0
  obtain ⟨hGH,hH⟩ := residual_frame G F (p^3) (2*a*p) hG hF hFG hcs hs
  rw [owned_plane_square G (residual G F (p^3) (2*a*p)) a p hG hH hGH ha hp]
  have horth := plane_orthogonal G _ (p^3) (2*a*p) hG hH hGH hcs
  exact ⟨horth,mul_eq_one_comm.mp horth,
    residual_transport G F (p^3) (2*a*p) hG hF hFG hcs hs⟩

def conjugate (R X : Matrix m m ℝ) : Matrix m m ℝ := R*X*R.transpose

omit [DecidableEq m] [DecidableEq n] in
/-- Every matrix outcome on the frame, not just its unit projection, transports. -/
theorem all_frame_outcomes (R : Matrix m m ℝ) (G F : Matrix m n ℝ)
    (X : Matrix n n ℝ) (h : R*G=F) :
    conjugate R (G*X*G.transpose)=F*X*F.transpose := by
  calc
    _ = (R*G)*X*(R*G).transpose := by
      simp [conjugate, Matrix.transpose_mul, Matrix.mul_assoc]
    _ = _ := by rw [h]

theorem conjugate_multiplication (R X Y : Matrix m m ℝ)
    (hR : R.transpose*R=1) :
    conjugate R (X*Y)=conjugate R X*conjugate R Y := by
  have hc (Z : Matrix m m ℝ) : R.transpose*(R*Z)=Z := by
    rw [← Matrix.mul_assoc,hR,Matrix.one_mul]
  simp [conjugate, Matrix.mul_assoc, hc]

omit [DecidableEq m] in
theorem conjugate_transpose (R X : Matrix m m ℝ) :
    conjugate R X.transpose=(conjugate R X).transpose := by
  simp [conjugate, Matrix.transpose_mul, Matrix.mul_assoc]

/-- The unobserved outcome is transported too; it is never discarded. -/
theorem conjugate_complement (R X : Matrix m m ℝ)
    (hR : R*R.transpose=1) : conjugate R (1-X)=1-conjugate R X := by
  simp [conjugate, Matrix.mul_sub, Matrix.sub_mul, hR]

theorem conjugate_trace (tau : Matrix m m ℝ → ℝ)
    (htrace : ∀ X Y, tau (X*Y)=tau (Y*X))
    (R X : Matrix m m ℝ) (hR : R.transpose*R=1) :
    tau (conjugate R X)=tau X := by
  rw [conjugate,htrace (R*X) R.transpose,← Matrix.mul_assoc,hR,Matrix.one_mul]

/-- Normalized corner expectations are covariant, with nonempty preparation
exposed as a hypothesis. The theorem does not increase its probability. -/
theorem conditioned_state_covariance (tau : Matrix m m ℝ → ℝ)
    (htrace : ∀ X Y, tau (X*Y)=tau (Y*X))
    (R e X : Matrix m m ℝ) (hR : R.transpose*R=1) (he : tau e≠0) :
    tau (conjugate R e)≠0 ∧
    tau (conjugate R e*conjugate R X*conjugate R e)/tau (conjugate R e)=
      tau (e*X*e)/tau e := by
  rw [← conjugate_multiplication R e X hR,
    ← conjugate_multiplication R (e*X) e hR,
    conjugate_trace tau htrace R (e*X*e) hR,
    conjugate_trace tau htrace R e hR]
  exact ⟨he,rfl⟩

omit [DecidableEq n] in
/-- The conjugated inclusion inherits its algebraic and tracial properties
from the stated native inclusion. It is not asserted to be dynamically selected. -/
theorem conjugated_refinement (alpha : Matrix n n ℝ → Matrix m m ℝ)
    (hmul : ∀ X Y, alpha (X*Y)=alpha X*alpha Y)
    (hstar : ∀ X, alpha X.transpose=(alpha X).transpose)
    (tau : Matrix m m ℝ → ℝ) (sigma : Matrix n n ℝ → ℝ)
    (htrace : ∀ X Y, tau (X*Y)=tau (Y*X))
    (hpreserve : ∀ X, tau (alpha X)=sigma X)
    (R : Matrix m m ℝ) (hR : R.transpose*R=1) :
    (∀ X Y, conjugate R (alpha (X*Y))=
      conjugate R (alpha X)*conjugate R (alpha Y)) ∧
    (∀ X, conjugate R (alpha X.transpose)=(conjugate R (alpha X)).transpose) ∧
    (∀ X, tau (conjugate R (alpha X))=sigma X) := by
  refine ⟨?_,?_,?_⟩
  · intro X Y
    rw [hmul,conjugate_multiplication R (alpha X) (alpha Y) hR]
  · intro X
    rw [hstar,conjugate_transpose]
  · intro X
    rw [conjugate_trace tau htrace R (alpha X) hR,hpreserve]

end
end D0.Research.JonesRecordTransport

#print axioms D0.Research.JonesRecordTransport.owned_gate_square
#print axioms D0.Research.JonesRecordTransport.golden_coefficients
#print axioms D0.Research.JonesRecordTransport.residual_frame
#print axioms D0.Research.JonesRecordTransport.cross_transpose
#print axioms D0.Research.JonesRecordTransport.plane_on_frames
#print axioms D0.Research.JonesRecordTransport.complement_pointwise_fixed
#print axioms D0.Research.JonesRecordTransport.plane_transpose
#print axioms D0.Research.JonesRecordTransport.plane_composition
#print axioms D0.Research.JonesRecordTransport.plane_orthogonal
#print axioms D0.Research.JonesRecordTransport.owned_plane_square
#print axioms D0.Research.JonesRecordTransport.residual_transport
#print axioms D0.Research.JonesRecordTransport.owned_square_transport
#print axioms D0.Research.JonesRecordTransport.all_frame_outcomes
#print axioms D0.Research.JonesRecordTransport.conjugate_multiplication
#print axioms D0.Research.JonesRecordTransport.conjugate_transpose
#print axioms D0.Research.JonesRecordTransport.conjugate_complement
#print axioms D0.Research.JonesRecordTransport.conjugate_trace
#print axioms D0.Research.JonesRecordTransport.conditioned_state_covariance
#print axioms D0.Research.JonesRecordTransport.conjugated_refinement
#print axioms D0.Representation.GoldenOrderInterferometer.gate_orthogonal
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
