import D0.Representation.GoldenCoherentMemory
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-! Complete future-response equivalence and exact archive elimination.
The actual recorded golden operator is reused, including its internal record.
No new action, external clock, physical refinement or source is selected. -/
namespace D0.Research.NativeHistoryResponseDescent
noncomputable section

section Histories
variable {S O L : Type*}

def run (T : L → S → S) : List L → S → S
  | [], x => x
  | a :: w, x => run T w (T a x)

def FutureEq (T : L → S → S) (read : S → O) (x y : S) : Prop :=
  ∀ w, read (run T w x) = read (run T w y)

def futureSetoid (T : L → S → S) (read : S → O) : Setoid S where
  r := FutureEq T read
  iseqv := ⟨fun _ _ => rfl, fun h w => (h w).symm,
    fun h₁ h₂ w => (h₁ w).trans (h₂ w)⟩

theorem future_keeps_present (T : L → S → S) (read : S → O)
    {x y : S} (h : FutureEq T read x y) : read x = read y := h []

theorem future_stable (T : L → S → S) (read : S → O)
    {x y : S} (h : FutureEq T read x y) (a : L) :
    FutureEq T read (T a x) (T a y) := fun w => h (a :: w)

def quotientStep (T : L → S → S) (read : S → O) (a : L) :
    Quotient (futureSetoid T read) → Quotient (futureSetoid T read) :=
  Quotient.map (T a) (fun _ _ h => future_stable T read h a)

def quotientRead (T : L → S → S) (read : S → O) :
    Quotient (futureSetoid T read) → O :=
  Quotient.lift read (fun _ _ h => future_keeps_present T read h)

theorem quotient_retains_every_future (T : L → S → S) (read : S → O)
    (w : List L) (x : S) :
    quotientRead T read (run (quotientStep T read) w (Quotient.mk _ x)) =
      read (run T w x) := by
  induction w generalizing x with
  | nil => rfl
  | cons a w ih => exact ih (T a x)

theorem complete_history_quotient (T : L → S → S) (read : S → O) (x y : S) :
    Quotient.mk (futureSetoid T read) x = Quotient.mk _ y ↔
      FutureEq T read x y := Quotient.eq

/-- Every exact process factor can identify only future-indistinguishable states. -/
theorem any_exact_factor_preserves_future {C : Type*}
    (T : L → S → S) (read : S → O) (q : S → C)
    (next : L → C → C) (out : C → O)
    (step : ∀ a x, q (T a x) = next a (q x))
    (obs : ∀ x, read x = out (q x))
    {x y : S} (h : q x = q y) : FutureEq T read x y := by
  intro w
  have lift (w : List L) (x : S) : q (run T w x) = run next w (q x) := by
    induction w generalizing x with
    | nil => rfl
    | cons a w ih => simpa [run, step] using ih (T a x)
  rw [obs, obs, lift, lift, h]

end Histories

section ResponseTower
universe u
variable {S : Type*} {O L : Type u}

/-- A finite observation depth records the present and every admitted next operation. -/
def ResponseTree (O L : Type u) : ℕ → Type u
  | 0 => O
  | n+1 => O × (L → ResponseTree O L n)

def responseTree (T : L → S → S) (read : S → O) :
    (n : ℕ) → S → ResponseTree O L n
  | 0, x => read x
  | n+1, x => (read x, fun a => responseTree T read n (T a x))

def trimTree : (n : ℕ) → ResponseTree O L (n+1) → ResponseTree O L n
  | 0, r => r.1
  | n+1, r => (r.1, fun a => trimTree n (r.2 a))

def childTree (n : ℕ) (a : L) (r : ResponseTree O L (n+1)) :
    ResponseTree O L n := r.2 a

def presentTree : (n : ℕ) → ResponseTree O L n → O
  | 0, r => r
  | _+1, r => r.1

theorem tower_keeps_present (T : L → S → S) (read : S → O) (n : ℕ) (x : S) :
    presentTree n (responseTree T read n x) = read x := by
  cases n <;> rfl

theorem canonical_truncation (T : L → S → S) (read : S → O) (n : ℕ) (x : S) :
    trimTree n (responseTree T read (n+1) x) = responseTree T read n x := by
  induction n generalizing x with
  | zero => rfl
  | succ n ih =>
    apply Prod.ext
    · rfl
    · funext a
      exact ih (T a x)

theorem canonical_process_descent (T : L → S → S) (read : S → O)
    (n : ℕ) (a : L) (x : S) :
    childTree n a (responseTree T read (n+1) x) =
      responseTree T read n (T a x) := rfl

/-- Truncation and an actual operation commute, with the correct depth shift. -/
theorem process_truncation_naturality (n : ℕ) (a : L) (r : ResponseTree O L (n+2)) :
    trimTree n (childTree (n+1) a r) =
      childTree n a (trimTree (n+1) r) := rfl

def RealizedResponse (T : L → S → S) (read : S → O) (n : ℕ) :=
  Set.range (responseTree T read n)

/-- Only realizable trees are admitted; empty or arbitrary fibers are not inserted. -/
def truncateRealized (T : L → S → S) (read : S → O) (n : ℕ) :
    RealizedResponse T read (n+1) → RealizedResponse T read n := fun r =>
  ⟨trimTree n r.1, by
    rcases r.2 with ⟨x,hx⟩
    exact ⟨x, by rw [← hx, canonical_truncation]⟩⟩

def advanceRealized (T : L → S → S) (read : S → O) (n : ℕ) (a : L) :
    RealizedResponse T read (n+1) → RealizedResponse T read n := fun r =>
  ⟨childTree n a r.1, by
    rcases r.2 with ⟨x,hx⟩
    exact ⟨T a x, by rw [← hx, canonical_process_descent]⟩⟩

theorem realized_process_naturality (T : L → S → S) (read : S → O)
    (n : ℕ) (a : L) (r : RealizedResponse T read (n+2)) :
    truncateRealized T read n (advanceRealized T read (n+1) a r) =
      advanceRealized T read n a (truncateRealized T read (n+1) r) := by
  apply Subtype.ext
  rfl

theorem realized_truncation_surjective (T : L → S → S) (read : S → O) (n : ℕ) :
    Function.Surjective (truncateRealized T read n) := by
  rintro ⟨r,x,hx⟩
  refine ⟨⟨responseTree T read (n+1) x, x, rfl⟩, ?_⟩
  apply Subtype.ext
  exact (canonical_truncation T read n x).trans hx

theorem future_determines_every_depth (T : L → S → S) (read : S → O)
    {x y : S} (h : FutureEq T read x y) (n : ℕ) :
    responseTree T read n x = responseTree T read n y := by
  induction n generalizing x y with
  | zero => exact future_keeps_present T read h
  | succ n ih =>
    apply Prod.ext
    · exact future_keeps_present T read h
    · funext a
      exact ih (future_stable T read h a)

theorem depth_retains_its_experiments (T : L → S → S) (read : S → O)
    (w : List L) {x y : S}
    (h : responseTree T read w.length x = responseTree T read w.length y) :
    read (run T w x) = read (run T w y) := by
  induction w generalizing x y with
  | nil => exact h
  | cons a w ih =>
    apply ih
    exact congrArg (fun r : ResponseTree O L (w.length+1) => r.2 a) h

/-- Infinite compatibility preserves exactly the full process, not merely one marginal. -/
theorem all_depths_iff_full_history (T : L → S → S) (read : S → O) (x y : S) :
    (∀ n, responseTree T read n x = responseTree T read n y) ↔
      FutureEq T read x y := by
  constructor
  · intro h w
    exact depth_retains_its_experiments T read w (h w.length)
  · exact fun h n => future_determines_every_depth T read h n

/-- An autonomous law at one depth is an additional factorization obligation. -/
theorem finite_depth_autonomy_forces_full_history (T : L → S → S) (read : S → O)
    (n : ℕ) (next : L → ResponseTree O L n → ResponseTree O L n)
    (owned : ∀ a x, responseTree T read n (T a x) = next a (responseTree T read n x))
    {x y : S} (h : responseTree T read n x = responseTree T read n y) :
    FutureEq T read x y :=
  any_exact_factor_preserves_future T read (responseTree T read n) next (presentTree n)
    owned (fun x => (tower_keeps_present T read n x).symm) h

/-- Finite operation and output types suffice for finiteness of every response-table type. -/
instance responseTreeFinite [Finite O] [Finite L] (n : ℕ) : Finite (ResponseTree O L n) := by
  induction n with
  | zero => exact inferInstanceAs (Finite O)
  | succ n ih => exact inferInstanceAs (Finite (O × (L → ResponseTree O L n)))

theorem realized_depth_finite [Finite O] [Finite L]
    (T : L → S → S) (read : S → O) (n : ℕ) :
    Finite (RealizedResponse T read n) := inferInstance

end ResponseTower

section NativeProfinite
universe u
variable {X : Type*} [TopologicalSpace X] {O L : Type u} [Finite L]

theorem finite_family_locally_constant (f : L → X → O)
    (hf : ∀ l, IsLocallyConstant (f l)) : IsLocallyConstant (fun x l => f l x) := by
  apply (IsLocallyConstant.iff_eventually_eq _).2
  intro x
  have h := Filter.eventually_all.2 (fun l => (hf l).eventually_eq x)
  exact h.mono (fun _ hy => funext hy)

theorem complete_response_locally_constant (T : L → X → X) (read : X → O)
    (hT : ∀ l, Continuous (T l)) (hr : IsLocallyConstant read) (n : ℕ) :
    IsLocallyConstant (responseTree T read n) := by
  induction n with
  | zero => exact hr
  | succ n ih =>
    exact hr.prodMk (finite_family_locally_constant
      (fun l x => responseTree T read n (T l x))
      (fun l => ih.comp_continuous (hT l)))

/-- Compactness gives a finite realized image even if the nominal output type is infinite. -/
theorem compact_response_range_finite [CompactSpace X]
    (T : L → X → X) (read : X → O)
    (hT : ∀ l, Continuous (T l)) (hr : IsLocallyConstant read) (n : ℕ) :
    (Set.range (responseTree T read n)).Finite :=
  (complete_response_locally_constant T read hT hr n).range_finite

open CategoryTheory in
/-- Consume the actual native profinite owner for the entire future response table. -/
theorem complete_response_owned_finite_factorization (S : Profinite)
    (T : L → S → S) (read : S → O)
    (hT : ∀ l, Continuous (T l)) (hr : IsLocallyConstant read) (n : ℕ) :
    ∃ (j : DiscreteQuotient S)
      (g : LocallyConstant (S.diagram.obj j) (ResponseTree O L n)),
      (⟨responseTree T read n, complete_response_locally_constant T read hT hr n⟩ :
        LocallyConstant S (ResponseTree O L n)) =
          g.comap (S.asLimitCone.π.app j).hom.hom :=
  D0.CondensedAnchor.readout_factors_through_finite_level S
    ⟨responseTree T read n, complete_response_locally_constant T read hT hr n⟩

/-- Compact native support closes the infinite-fiber gap for these admitted observations. -/
theorem compact_compatible_history_realized [CompactSpace X]
    (T : L → X → X) (read : X → O)
    (hT : ∀ l, Continuous (T l)) (hr : IsLocallyConstant read)
    (c : (n : ℕ) → RealizedResponse T read n)
    (hc : ∀ n, truncateRealized T read n (c (n+1)) = c n) :
    ∃ x, ∀ n, responseTree T read n x = (c n).1 := by
  let fibers : ℕ → Set X := fun n => {x | responseTree T read n x = (c n).1}
  have closed : ∀ n, IsClosed (fibers n) := fun n =>
    (complete_response_locally_constant T read hT hr n).isClosed_fiber _
  have inhabited : ∀ n, (fibers n).Nonempty := by
    intro n
    obtain ⟨x,hx⟩ := (c n).2
    exact ⟨x,hx⟩
  have nested : ∀ n, fibers (n+1) ⊆ fibers n := by
    intro n x hx
    change responseTree T read n x = (c n).1
    calc
      responseTree T read n x = trimTree n (responseTree T read (n+1) x) :=
        (canonical_truncation T read n x).symm
      _ = trimTree n (c (n+1)).1 := congrArg (trimTree n) hx
      _ = (c n).1 := congrArg Subtype.val (hc n)
  obtain ⟨x,hx⟩ := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed
    fibers nested inhabited ((closed 0).isCompact) closed
  exact ⟨x, fun n => Set.mem_iInter.mp hx n⟩

open D0.CondensedAnchor in
/-- Local cylinder expectations descend with the owned golden weights, for every reading. -/
theorem golden_cylinder_expectation_descent (w : List Bool) (v : ℝ) :
    cylWeight (w.concat true)*v + cylWeight (w.concat false)*v = cylWeight w*v := by
  rw [← add_mul, cylWeight_refine]

open D0.CondensedAnchor in
/-- The same identity holds for every finite collection of parent cylinders. -/
theorem golden_partition_expectation_descent (W : Finset (List Bool)) (f : List Bool → ℝ) :
    (∑ w ∈ W, (cylWeight (w.concat true)*f w + cylWeight (w.concat false)*f w)) =
      ∑ w ∈ W, cylWeight w*f w := by
  apply Finset.sum_congr rfl
  intro w hw
  exact golden_cylinder_expectation_descent w (f w)

end NativeProfinite

section GoldenRefinement
open Matrix D0.Representation.GoldenOrderInterferometer
open scoped goldenRatio

/-- Squared coefficients of cylindrical Hilbert inclusion are the owned branch weights. -/
theorem owned_cylinder_amplitude_weights (a : ℝ) (ha : a^2 = (φ : ℝ)⁻¹) :
    a^2 = D0.CondensedAnchor.cylWeight [true] ∧
    ((φ : ℝ)⁻¹)^2 = D0.CondensedAnchor.cylWeight [false] := by
  simp [D0.CondensedAnchor.cylWeight,ha]

/-- In the normalized cylinder basis, refinement is x ↦ (a x,p x). -/
def goldenRefine {E : Type*} [SMul ℝ E] (a p : ℝ) (x : E) : E × E :=
  (a • x, p • x)

theorem golden_refinement_preserves_pairing {I : Type*} [Fintype I]
    (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) (f g : I → ℝ) :
    (∑ i, ((a*f i)*(a*g i)+(p*f i)*(p*g i))) = ∑ i, f i*g i := by
  apply Finset.sum_congr rfl
  intro i hi
  have h : a^2+p^2=1 := by rw [ha]; exact hp
  calc
    (a*f i)*(a*g i)+(p*f i)*(p*g i) = (a^2+p^2)*(f i*g i) := by ring
    _ = f i*g i := by rw [h,one_mul]

/-- Every already-owned linear operator has its coherent tensor extension. -/
theorem golden_operator_refinement_natural {E F : Type*}
    [AddCommGroup E] [Module ℝ E] [AddCommGroup F] [Module ℝ F]
    (A : E →ₗ[ℝ] F) (a p : ℝ) (x : E) :
    goldenRefine a p (A x) =
      (A (goldenRefine a p x).1, A (goldenRefine a p x).2) := by
  simp [goldenRefine]

/-- A refined golden factor can be prepared blank by the inverse of the owned gate. -/
theorem golden_refinement_factor_to_blank (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (gate a p).transpose.mulVec ![a,p] = ![1,0] := by
  ext i
  fin_cases i <;> simp [gate,Matrix.mulVec,dotProduct,Fin.sum_univ_succ] <;> nlinarith

end GoldenRefinement

section JointSystem
variable {E F : Type*} [AddCommGroup E] [Module ℝ E]
  [AddCommGroup F] [Module ℝ F]

def jointStep (A : E →ₗ[ℝ] E) (B : F →ₗ[ℝ] E)
    (C : E →ₗ[ℝ] F) (D : F →ₗ[ℝ] F) (s : E × F) : E × F :=
  (A s.1 + B s.2, C s.1 + D s.2)

/-- Necessary and sufficient; a current-only update cannot silently reset archive. -/
theorem current_factor_iff (A : E →ₗ[ℝ] E) (B : F →ₗ[ℝ] E) :
    (∃ f : E → E, ∀ x y, A x + B y = f x) ↔ B = 0 := by
  constructor
  · rintro ⟨f,h⟩
    ext y
    have hz := h 0 0
    have hy := h 0 y
    simpa using hy.trans hz.symm
  · rintro rfl
    exact ⟨A, fun x y => by simp⟩

def archiveHom (D : F →ₗ[ℝ] F) (y : F) : ℕ → F
  | 0 => y
  | n+1 => D (archiveHom D y n)

def archiveForced (C : E →ₗ[ℝ] F) (D : F →ₗ[ℝ] F) (x : ℕ → E) : ℕ → F
  | 0 => 0
  | n+1 => C (x n) + D (archiveForced C D x n)

/-- An internally indexed trajectory retains the initial archive and every prior input. -/
theorem full_archive_history (C : E →ₗ[ℝ] F) (D : F →ₗ[ℝ] F)
    (x : ℕ → E) (y : ℕ → F)
    (hy : ∀ n, y (n+1) = C (x n) + D (y n)) (n : ℕ) :
    y n = archiveHom D (y 0) n + archiveForced C D x n := by
  induction n with
  | zero => simp [archiveHom,archiveForced]
  | succ n ih =>
    rw [hy,ih]
    simp only [archiveHom,archiveForced,map_add]
    abel

theorem complete_active_memory_equation
    (A : E →ₗ[ℝ] E) (B : F →ₗ[ℝ] E)
    (C : E →ₗ[ℝ] F) (D : F →ₗ[ℝ] F)
    (x : ℕ → E) (y : ℕ → F)
    (hx : ∀ n, x (n+1) = A (x n) + B (y n))
    (hy : ∀ n, y (n+1) = C (x n) + D (y n)) (n : ℕ) :
    x (n+1) = A (x n) + B (archiveHom D (y 0) n) +
      B (archiveForced C D x n) := by
  rw [hx,full_archive_history C D x y hy n,map_add]
  abel

/-- All coupled source equations survive elimination, with exact reconstruction. -/
theorem joint_source_schur_iff
    (A : E →ₗ[ℝ] E) (B : F →ₗ[ℝ] E)
    (C : E →ₗ[ℝ] F) (D V : F →ₗ[ℝ] F)
    (left : ∀ y, V (D y) = y) (right : ∀ y, D (V y) = y)
    (f x : E) (g y : F) :
    (A x+B y=f ∧ C x+D y=g) ↔
      (y=V (g-C x) ∧ A x-B (V (C x))=f-B (V g)) := by
  constructor
  · rintro ⟨hx,hy⟩
    have hy' : D y=g-C x := by rw [← hy]; abel
    have he : y=V (g-C x) := by rw [← hy',left]
    refine ⟨he,?_⟩
    calc
      A x-B (V (C x)) = (A x+B (V (g-C x)))-B (V g) := by
        simp only [map_sub]; abel
      _ = f-B (V g) := by rw [← he,hx]
  · rintro ⟨hy,hx⟩
    constructor
    · calc
        A x+B y = (A x-B (V (C x)))+B (V g) := by
          rw [hy]; simp only [map_sub]; abel
        _ = f := by rw [hx]; abel
    · rw [hy,right]; abel

/-- Any exact multistage reconstruction agrees with direct reconstruction. -/
theorem archive_reconstruction_unique
    (D V : F →ₗ[ℝ] F) (left : ∀ y, V (D y)=y)
    (b y₁ y₂ : F) (h₁ : D y₁=b) (h₂ : D y₂=b) : y₁=y₂ := by
  calc y₁ = V (D y₁) := (left y₁).symm
       _ = V (D y₂) := by rw [h₁,h₂]
       _ = y₂ := left y₂

end JointSystem

section Action
open Matrix
variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

/-- Apply this to the existing feedback pencil I-zF, without replacing F by U. -/
theorem full_feedback_determinant (A : Matrix m m ℝ) (B : Matrix m n ℝ)
    (C : Matrix n m ℝ) (D : Matrix n n ℝ) [Invertible D] :
    (fromBlocks A B C D).det = D.det * (A-B*⅟D*C).det :=
  Matrix.det_fromBlocks₂₂ A B C D

theorem full_feedback_action (A : Matrix m m ℝ) (B : Matrix m n ℝ)
    (C : Matrix n m ℝ) (D : Matrix n n ℝ) [Invertible D]
    (hD : D.det ≠ 0) (hS : (A-B*⅟D*C).det ≠ 0) :
    -Real.log (fromBlocks A B C D).det =
      -Real.log D.det - Real.log (A-B*⅟D*C).det := by
  rw [full_feedback_determinant, Real.log_mul hD hS]
  ring

/-- Genuine derivatives of both determinant factors; archive variation is retained. -/
theorem full_feedback_source {u v : ℝ → ℝ} {u' v' t : ℝ}
    (hu : HasDerivAt u u' t) (hv : HasDerivAt v v' t)
    (hun : u t ≠ 0) (hvn : v t ≠ 0) :
    HasDerivAt (fun s => -Real.log (u s*v s))
      (-u'/u t-v'/v t) t := by
  convert ((hu.mul hv).log (mul_ne_zero hun hvn)).neg using 1
  simp only [Pi.mul_apply]
  field_simp
  ring

end Action

section NativeGolden
open Matrix D0.Representation.GoldenCoherentMemory
open D0.Representation.GoldenOrderInterferometer

def remembered (a p : ℝ) (sign : ℝ) : Fin 4 → ℝ := ![a,0,0,sign*p]
def retainedMarginal (v : Fin 4 → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![v 0^2+v 1^2, v 0*v 2+v 1*v 3;
     v 0*v 2+v 1*v 3, v 2^2+v 3^2]
def archiveMarginal (v : Fin 4 → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![v 0^2+v 2^2, v 0*v 1+v 2*v 3;
     v 0*v 1+v 2*v 3, v 1^2+v 3^2]
def readZ (v : Fin 4 → ℝ) : ℝ := v 0^2+v 1^2-v 2^2-v 3^2

theorem same_present_both_marginals (a p : ℝ) :
    retainedMarginal (remembered a p 1)=retainedMarginal (remembered a p (-1)) ∧
    archiveMarginal (remembered a p 1)=archiveMarginal (remembered a p (-1)) := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [retainedMarginal,archiveMarginal,remembered]

theorem normalized_joint_histories (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (∑ i, (remembered a p 1 i)^2)=1 ∧
    (∑ i, (remembered a p (-1) i)^2)=1 := by
  simp [remembered,Fin.sum_univ_succ,ha,hp]

theorem owned_recorded_state (a p : ℝ) :
    (fullStep a p).mulVec ![1,0,0,0]=remembered a p 1 := by
  ext i
  fin_cases i <;> simp [fullStep,remembered,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem native_two_return_gap_raw (a p : ℝ) :
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p 1))) -
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p (-1)))) =
      8*a^2*p^2*(p^2-a^2) := by
  simp [readZ,fullStep,remembered,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]
  ring

theorem native_two_return_gap (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p 1))) -
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p (-1)))) =
      -8*p^6 := by
  rw [native_two_return_gap_raw,ha]
  have hc : p^2-p= -p^3 := by linarith [golden_cube p hp]
  rw [hc]
  ring

/-- Autonomous reuse of the actual joint gate exposes retained correlations. -/
theorem actual_native_future_distinguishes (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hpos : 0<p) :
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p 1))) ≠
    readZ ((fullStep a p).mulVec ((fullStep a p).mulVec (remembered a p (-1)))) := by
  have h := native_two_return_gap a p ha hp
  have hh : 0 < p^6 := pow_pos hpos _
  intro he
  rw [he,sub_self] at h
  linarith

theorem actual_native_depth_two_separates (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hpos : 0<p) :
    responseTree (fun (_ : Unit) => (fullStep a p).mulVec) readZ 2 (remembered a p 1) ≠
    responseTree (fun (_ : Unit) => (fullStep a p).mulVec) readZ 2 (remembered a p (-1)) := by
  intro h
  have he := depth_retains_its_experiments
    (fun (_ : Unit) => (fullStep a p).mulVec) readZ [(), ()] h
  exact actual_native_future_distinguishes a p ha hp hpos he

end NativeGolden
end
end D0.Research.NativeHistoryResponseDescent

-- Audit the actual propositions and their transitive logical dependencies.
#check D0.Research.NativeHistoryResponseDescent.future_keeps_present
#print axioms D0.Research.NativeHistoryResponseDescent.future_keeps_present
#check D0.Research.NativeHistoryResponseDescent.future_stable
#print axioms D0.Research.NativeHistoryResponseDescent.future_stable
#check D0.Research.NativeHistoryResponseDescent.quotient_retains_every_future
#print axioms D0.Research.NativeHistoryResponseDescent.quotient_retains_every_future
#check D0.Research.NativeHistoryResponseDescent.complete_history_quotient
#print axioms D0.Research.NativeHistoryResponseDescent.complete_history_quotient
#check D0.Research.NativeHistoryResponseDescent.any_exact_factor_preserves_future
#print axioms D0.Research.NativeHistoryResponseDescent.any_exact_factor_preserves_future
#check D0.Research.NativeHistoryResponseDescent.tower_keeps_present
#print axioms D0.Research.NativeHistoryResponseDescent.tower_keeps_present
#check D0.Research.NativeHistoryResponseDescent.canonical_truncation
#print axioms D0.Research.NativeHistoryResponseDescent.canonical_truncation
#check D0.Research.NativeHistoryResponseDescent.canonical_process_descent
#print axioms D0.Research.NativeHistoryResponseDescent.canonical_process_descent
#check D0.Research.NativeHistoryResponseDescent.process_truncation_naturality
#print axioms D0.Research.NativeHistoryResponseDescent.process_truncation_naturality
#check D0.Research.NativeHistoryResponseDescent.realized_process_naturality
#print axioms D0.Research.NativeHistoryResponseDescent.realized_process_naturality
#check D0.Research.NativeHistoryResponseDescent.realized_truncation_surjective
#print axioms D0.Research.NativeHistoryResponseDescent.realized_truncation_surjective
#check D0.Research.NativeHistoryResponseDescent.future_determines_every_depth
#print axioms D0.Research.NativeHistoryResponseDescent.future_determines_every_depth
#check D0.Research.NativeHistoryResponseDescent.depth_retains_its_experiments
#print axioms D0.Research.NativeHistoryResponseDescent.depth_retains_its_experiments
#check D0.Research.NativeHistoryResponseDescent.all_depths_iff_full_history
#print axioms D0.Research.NativeHistoryResponseDescent.all_depths_iff_full_history
#check D0.Research.NativeHistoryResponseDescent.finite_depth_autonomy_forces_full_history
#print axioms D0.Research.NativeHistoryResponseDescent.finite_depth_autonomy_forces_full_history
#check D0.Research.NativeHistoryResponseDescent.realized_depth_finite
#print axioms D0.Research.NativeHistoryResponseDescent.realized_depth_finite
#check D0.Research.NativeHistoryResponseDescent.finite_family_locally_constant
#print axioms D0.Research.NativeHistoryResponseDescent.finite_family_locally_constant
#check D0.Research.NativeHistoryResponseDescent.complete_response_locally_constant
#print axioms D0.Research.NativeHistoryResponseDescent.complete_response_locally_constant
#check D0.Research.NativeHistoryResponseDescent.compact_response_range_finite
#print axioms D0.Research.NativeHistoryResponseDescent.compact_response_range_finite
set_option pp.explicit true in
#check D0.Research.NativeHistoryResponseDescent.complete_response_owned_finite_factorization
#print axioms D0.Research.NativeHistoryResponseDescent.complete_response_owned_finite_factorization
#check D0.Research.NativeHistoryResponseDescent.compact_compatible_history_realized
#print axioms D0.Research.NativeHistoryResponseDescent.compact_compatible_history_realized
#check D0.Research.NativeHistoryResponseDescent.golden_cylinder_expectation_descent
#print axioms D0.Research.NativeHistoryResponseDescent.golden_cylinder_expectation_descent
#check D0.Research.NativeHistoryResponseDescent.golden_partition_expectation_descent
#print axioms D0.Research.NativeHistoryResponseDescent.golden_partition_expectation_descent
#check D0.Research.NativeHistoryResponseDescent.owned_cylinder_amplitude_weights
#print axioms D0.Research.NativeHistoryResponseDescent.owned_cylinder_amplitude_weights
#check D0.Research.NativeHistoryResponseDescent.golden_refinement_preserves_pairing
#print axioms D0.Research.NativeHistoryResponseDescent.golden_refinement_preserves_pairing
#check D0.Research.NativeHistoryResponseDescent.golden_operator_refinement_natural
#print axioms D0.Research.NativeHistoryResponseDescent.golden_operator_refinement_natural
#check D0.Research.NativeHistoryResponseDescent.golden_refinement_factor_to_blank
#print axioms D0.Research.NativeHistoryResponseDescent.golden_refinement_factor_to_blank
#check D0.Research.NativeHistoryResponseDescent.current_factor_iff
#print axioms D0.Research.NativeHistoryResponseDescent.current_factor_iff
#check D0.Research.NativeHistoryResponseDescent.full_archive_history
#print axioms D0.Research.NativeHistoryResponseDescent.full_archive_history
#check D0.Research.NativeHistoryResponseDescent.complete_active_memory_equation
#print axioms D0.Research.NativeHistoryResponseDescent.complete_active_memory_equation
#check D0.Research.NativeHistoryResponseDescent.joint_source_schur_iff
#print axioms D0.Research.NativeHistoryResponseDescent.joint_source_schur_iff
#check D0.Research.NativeHistoryResponseDescent.archive_reconstruction_unique
#print axioms D0.Research.NativeHistoryResponseDescent.archive_reconstruction_unique
#check D0.Research.NativeHistoryResponseDescent.full_feedback_determinant
#print axioms D0.Research.NativeHistoryResponseDescent.full_feedback_determinant
#check D0.Research.NativeHistoryResponseDescent.full_feedback_action
#print axioms D0.Research.NativeHistoryResponseDescent.full_feedback_action
#check D0.Research.NativeHistoryResponseDescent.full_feedback_source
#print axioms D0.Research.NativeHistoryResponseDescent.full_feedback_source
#check D0.Research.NativeHistoryResponseDescent.same_present_both_marginals
#print axioms D0.Research.NativeHistoryResponseDescent.same_present_both_marginals
#check D0.Research.NativeHistoryResponseDescent.normalized_joint_histories
#print axioms D0.Research.NativeHistoryResponseDescent.normalized_joint_histories
#check D0.Research.NativeHistoryResponseDescent.owned_recorded_state
#print axioms D0.Research.NativeHistoryResponseDescent.owned_recorded_state
#check D0.Research.NativeHistoryResponseDescent.native_two_return_gap_raw
#print axioms D0.Research.NativeHistoryResponseDescent.native_two_return_gap_raw
#check D0.Research.NativeHistoryResponseDescent.native_two_return_gap
#print axioms D0.Research.NativeHistoryResponseDescent.native_two_return_gap
#check D0.Research.NativeHistoryResponseDescent.actual_native_future_distinguishes
#print axioms D0.Research.NativeHistoryResponseDescent.actual_native_future_distinguishes
#check D0.Research.NativeHistoryResponseDescent.actual_native_depth_two_separates
#print axioms D0.Research.NativeHistoryResponseDescent.actual_native_depth_two_separates
