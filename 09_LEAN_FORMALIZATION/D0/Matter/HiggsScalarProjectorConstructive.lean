import D0.Core.DyadABCD
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic

namespace D0.Matter

open Matrix
open scoped BigOperators

/-- Frozen finite SU(2) doublet carrier. -/
abbrev Doublet := Fin 2

/-- Rational 2x2 matrices on the frozen doublet carrier. -/
abbrev QMat2 := Matrix Doublet Doublet Rat

/-- First frozen rational doublet generator. -/
def FrozenSU2_X : QMat2 :=
  fun i j =>
    if (i.val = 0 ∧ j.val = 1) ∨ (i.val = 1 ∧ j.val = 0) then 1 else 0

/-- Second frozen rational doublet generator. -/
def FrozenSU2_Z : QMat2 :=
  fun i j =>
    if i = j then
      if i.val = 0 then 1 else -1
    else 0

/-- Gauge compatibility is finite commutation with the two frozen doublet generators. -/
def IntertwinesFrozenSU2 (P : QMat2) : Prop :=
  P * FrozenSU2_X = FrozenSU2_X * P ∧
  P * FrozenSU2_Z = FrozenSU2_Z * P

/-- Scalar/tick compatibility in the finite doublet response is self-adjointness. -/
def TickScalarCompatible (P : QMat2) : Prop :=
  P.transpose = P

/-- Finite quadratic response of a rational projector. -/
def quadraticResponse2 (P : QMat2) (v : Doublet -> Rat) : Rat :=
  dotProduct v (P.mulVec v)

/-- Concrete finite scalar projector on the frozen SU(2) doublet carrier. -/
structure FiniteScalarProjector2 where
  P : QMat2
  idempotent : P * P = P
  symmetric : TickScalarCompatible P
  nonzero : P ≠ 0
  positiveResponse : forall v : Doublet -> Rat, 0 <= quadraticResponse2 P v
  gaugeCompatible : IntertwinesFrozenSU2 P

/-- Trace-rank proxy, valid for finite idempotents in this doublet module. -/
def scalarProjectorTraceRank (P : FiniteScalarProjector2) : Rat :=
  Matrix.trace P.P

def IsRankOneScalarProjector (P : FiniteScalarProjector2) : Prop :=
  scalarProjectorTraceRank P = 1

def IsRankTwoScalarProjector (P : FiniteScalarProjector2) : Prop :=
  scalarProjectorTraceRank P = 2

/-- Commuting with `Z` kills the off-diagonal entries. -/
theorem commutes_Z_forces_offdiag_zero
    (P : QMat2)
    (hZ : P * FrozenSU2_Z = FrozenSU2_Z * P) :
    P 0 1 = 0 ∧ P 1 0 = 0 := by
  have hz01 := congrArg (fun M : QMat2 => M 0 1) hZ
  have hz10 := congrArg (fun M : QMat2 => M 1 0) hZ
  simp [Matrix.mul_apply, FrozenSU2_Z] at hz01 hz10
  constructor <;> linarith

/-- Commuting with `X` equates the two diagonal entries once the matrix is diagonal. -/
theorem commutes_X_forces_diag_equal_of_diagonal
    (P : QMat2)
    (hX : P * FrozenSU2_X = FrozenSU2_X * P)
    (_hp01 : P 0 1 = 0)
    (_hp10 : P 1 0 = 0) :
    P 0 0 = P 1 1 := by
  have hx01 := congrArg (fun M : QMat2 => M 0 1) hX
  simpa [Matrix.mul_apply, FrozenSU2_X, Fin.sum_univ_two] using hx01

/-- The finite commutant of the frozen `X,Z` doublet action is exactly scalar matrices. -/
theorem commutes_XZ_forces_scalar_matrix
    (P : QMat2)
    (h : IntertwinesFrozenSU2 P) :
    exists a : Rat, P = fun i j => if i = j then a else 0 := by
  rcases h with ⟨hX, hZ⟩
  rcases commutes_Z_forces_offdiag_zero P hZ with ⟨hp01, hp10⟩
  have hdiag := commutes_X_forces_diag_equal_of_diagonal P hX hp01 hp10
  refine ⟨P 0 0, ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;> simp [hp01, hp10, hdiag]

/-- A scalar idempotent on the frozen doublet is either zero or the identity. -/
theorem scalar_idempotent_eq_zero_or_id
    (a : Rat)
    (P : QMat2)
    (hP : P = fun i j => if i = j then a else 0)
    (hid : P * P = P) :
    a = 0 ∨ a = 1 := by
  have h00 := congrArg (fun M : QMat2 => M 0 0) hid
  simp [hP, Matrix.mul_apply] at h00
  have hfac : a * (a - 1) = 0 := by
    nlinarith
  rcases mul_eq_zero.mp hfac with hzero | hone
  · exact Or.inl hzero
  · right
    linarith

/-- Any nonzero gauge-compatible finite scalar idempotent is the doublet identity. -/
theorem nonzero_gauge_idempotent_eq_identity
    (P : FiniteScalarProjector2) :
    P.P = 1 := by
  rcases commutes_XZ_forces_scalar_matrix P.P P.gaugeCompatible with ⟨a, ha⟩
  rcases scalar_idempotent_eq_zero_or_id a P.P ha P.idempotent with hzero | hone
  · exfalso
    apply P.nonzero
    rw [ha]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [hzero]
  · rw [ha]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [hone]

theorem trace_identity_2 :
    Matrix.trace (1 : QMat2) = 2 := by
  native_decide

/-- Rank one is impossible for a nonzero finite scalar projector commuting with `X,Z`. -/
theorem rank1_scalar_projector_breaks_su2_gauge_compatibility
    (P : FiniteScalarProjector2) :
    Not (IsRankOneScalarProjector P) := by
  intro hrank1
  have hI : P.P = 1 := nonzero_gauge_idempotent_eq_identity P
  unfold IsRankOneScalarProjector scalarProjectorTraceRank at hrank1
  rw [hI, trace_identity_2] at hrank1
  norm_num at hrank1

/-- The identity doublet response is positive. -/
theorem identity_positive_response :
    forall v : Doublet -> Rat, 0 <= quadraticResponse2 (1 : QMat2) v := by
  intro v
  unfold quadraticResponse2
  simp [Matrix.mulVec, dotProduct]
  nlinarith [sq_nonneg (v 0), sq_nonneg (v 1)]

/-- Concrete identity scalar projector on the frozen doublet. -/
def identityScalarProjector2 : FiniteScalarProjector2 where
  P := 1
  idempotent := by simp
  symmetric := by
    unfold TickScalarCompatible
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.transpose_apply]
  nonzero := by
    intro h
    have h00 := congrArg (fun M : QMat2 => M 0 0) h
    simp at h00
  positiveResponse := identity_positive_response
  gaugeCompatible := by
    constructor <;>
      ext i j <;>
      fin_cases i <;>
      fin_cases j <;>
      simp [FrozenSU2_X, FrozenSU2_Z, Matrix.mul_apply, Fin.sum_univ_two]

theorem rank2_scalar_projector_exists :
    exists P : FiniteScalarProjector2, IsRankTwoScalarProjector P := by
  refine ⟨identityScalarProjector2, ?_⟩
  unfold IsRankTwoScalarProjector scalarProjectorTraceRank identityScalarProjector2
  exact trace_identity_2

/-- Strong minimality: every finite nonzero compatible scalar projector has trace-rank two. -/
theorem minimal_positive_scalar_projector_rank_two
    (P : FiniteScalarProjector2) :
    IsRankTwoScalarProjector P := by
  unfold IsRankTwoScalarProjector scalarProjectorTraceRank
  rw [nonzero_gauge_idempotent_eq_identity P, trace_identity_2]

/-- Uniqueness of the finite scalar projector in the frozen doublet convention. -/
theorem minimal_positive_scalar_projector_unique
    (P Q : FiniteScalarProjector2) :
    P.P = Q.P := by
  rw [nonzero_gauge_idempotent_eq_identity P,
    nonzero_gauge_idempotent_eq_identity Q]

/-- Concrete scalar/Yukawa transfer legality object. -/
structure HiggsYukawaCorePromotion where
  projector : FiniteScalarProjector2
  rank_two : IsRankTwoScalarProjector projector
  unique_owner : projector.P = identityScalarProjector2.P

/-- Scalar/Yukawa legality is witnessed by the unique rank-two finite doublet projector. -/
def higgs_yukawa_core_promotion_valid :
    HiggsYukawaCorePromotion := by
  refine
    { projector := identityScalarProjector2
      rank_two := ?_
      unique_owner := ?_ }
  · unfold IsRankTwoScalarProjector scalarProjectorTraceRank identityScalarProjector2
    exact trace_identity_2
  · rfl

/--
Finite left/right matter-transfer carrier.

The electroweak scalar projector is not a free vacuum scalar here.  It acts on
the finite transfer atoms that carry a left weak-doublet ledger into the right
matter-readout ledger.
-/
structure FiniteMatterTransferCarrier where
  leftDim : Nat
  rightDim : Nat
  nonzero_left : 0 < leftDim
  nonzero_right : 0 < rightDim

/-- The finite EW matter-transfer carrier: a left doublet and one right readout slot. -/
def finiteEWMatterTransferCarrier : FiniteMatterTransferCarrier where
  leftDim := 2
  rightDim := 1
  nonzero_left := by norm_num
  nonzero_right := by norm_num

/-- Frozen finite SU(2) doublet component in the matter-transfer Hom-space. -/
inductive FrozenSU2DoubletComponent where
  | up
  | down
  deriving DecidableEq, Repr, Fintype

/-- The finite weak-doublet action used for the rank-one obstruction. -/
def weakSwap : FrozenSU2DoubletComponent -> FrozenSU2DoubletComponent
  | .up => .down
  | .down => .up

/-- Concrete finite scalar projector: a Boolean idempotent mask on transfer atoms. -/
structure FiniteScalarProjector (C : FiniteMatterTransferCarrier) where
  keep : FrozenSU2DoubletComponent -> Bool

namespace FiniteScalarProjector

/-- Complex rank proxy for the finite doublet-transfer carrier. -/
def rank {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C) : Nat :=
  (if P.keep FrozenSU2DoubletComponent.up then 1 else 0) +
    (if P.keep FrozenSU2DoubletComponent.down then 1 else 0)

/-- Project a finite transfer atom, returning no atom when the projector kills it. -/
def project {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) :
    FrozenSU2DoubletComponent -> Option FrozenSU2DoubletComponent :=
  fun x => if P.keep x then some x else none

end FiniteScalarProjector

/-- Zero projector on the finite matter-transfer carrier. -/
def zeroMatterTransferProjector (C : FiniteMatterTransferCarrier) :
    FiniteScalarProjector C where
  keep := fun _ => false

/-- Rank-two doublet projector on the finite matter-transfer carrier. -/
def rankTwoMatterTransferProjector (C : FiniteMatterTransferCarrier) :
    FiniteScalarProjector C where
  keep := fun _ => true

/-- Boolean projector composition on finite transfer atoms. -/
def composeProjected {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) :
    Option FrozenSU2DoubletComponent -> Option FrozenSU2DoubletComponent
  | none => none
  | some x => P.project x

/-- Idempotence is concrete Boolean projection idempotence. -/
def Idempotent {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) : Prop :=
  forall x, composeProjected P (P.project x) = P.project x

/-- Nonzero finite projector rank. -/
def Nonzero {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) : Prop :=
  0 < P.rank

/-- Positive response is the finite nonzero readout condition. -/
def PositiveResponse {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) : Prop :=
  Nonzero P

/-- Tick/ABCD action on scalar transfer atoms: scalars do not rotate the doublet index. -/
def tickABCDAction (_r : D0.Role) :
    FrozenSU2DoubletComponent -> FrozenSU2DoubletComponent :=
  id

/-- Scalar compatibility is finite commutation with every tick/ABCD role. -/
def ScalarCompatible {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) : Prop :=
  forall r x, P.project (tickABCDAction r x) =
    Option.map (tickABCDAction r) (P.project x)

/-- Gauge compatibility is finite intertwining with the frozen SU(2) doublet action. -/
def GaugeCompatible {C : FiniteMatterTransferCarrier}
    (P : FiniteScalarProjector C) : Prop :=
  forall x, P.project (weakSwap x) = Option.map weakSwap (P.project x)

/-- Fixed-readout equivalence of two finite scalar projectors. -/
def ReadoutEquivalent {C : FiniteMatterTransferCarrier}
    (P Q : FiniteScalarProjector C) : Prop :=
  forall x, P.keep x = Q.keep x

/-- Every Boolean finite projector is idempotent. -/
theorem finite_scalar_projector_idempotent
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C) :
    Idempotent P := by
  intro x
  by_cases h : P.keep x <;>
    simp [composeProjected, FiniteScalarProjector.project, h]

/-- Every Boolean finite projector commutes with the scalar tick/ABCD action. -/
theorem finite_scalar_projector_scalar_compatible
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C) :
    ScalarCompatible P := by
  intro r x
  cases x <;> simp [tickABCDAction, FiniteScalarProjector.project]

/-- Finite doublet-transfer rank is bounded by two. -/
theorem finite_scalar_projector_rank_le_two
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C) :
    P.rank <= 2 := by
  cases hUp : P.keep FrozenSU2DoubletComponent.up <;>
    cases hDown : P.keep FrozenSU2DoubletComponent.down <;>
      simp [FiniteScalarProjector.rank, hUp, hDown]

/-- Rank two means that both frozen doublet transfer atoms are retained. -/
theorem finite_scalar_projector_rank_eq_two_iff
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C) :
    P.rank = 2 <->
      P.keep FrozenSU2DoubletComponent.up = true /\
        P.keep FrozenSU2DoubletComponent.down = true := by
  cases hUp : P.keep FrozenSU2DoubletComponent.up <;>
    cases hDown : P.keep FrozenSU2DoubletComponent.down <;>
      simp [FiniteScalarProjector.rank, hUp, hDown]

/--
Rank-one no-go: a one-atom projector selects a direction in the frozen SU(2)
doublet, so it cannot intertwine the doublet action.
-/
theorem finite_scalar_projector_rank_one_no_go
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C)
    (hrank : P.rank = 1) :
    Not (GaugeCompatible P) := by
  intro hg
  cases hUp : P.keep FrozenSU2DoubletComponent.up <;>
    cases hDown : P.keep FrozenSU2DoubletComponent.down
  · simp [FiniteScalarProjector.rank, hUp, hDown] at hrank
  · have h := hg FrozenSU2DoubletComponent.up
    simp [FiniteScalarProjector.project, weakSwap, hUp, hDown] at h
  · have h := hg FrozenSU2DoubletComponent.up
    simp [FiniteScalarProjector.project, weakSwap, hUp, hDown] at h
  · simp [FiniteScalarProjector.rank, hUp, hDown] at hrank

/-- The concrete rank-two matter-transfer projector has rank two. -/
theorem rank_two_matter_transfer_projector_rank
    (C : FiniteMatterTransferCarrier) :
    (rankTwoMatterTransferProjector C).rank = 2 := by
  simp [rankTwoMatterTransferProjector, FiniteScalarProjector.rank]

/-- The concrete rank-two matter-transfer projector is positive. -/
theorem rank_two_matter_transfer_projector_positive
    (C : FiniteMatterTransferCarrier) :
    PositiveResponse (rankTwoMatterTransferProjector C) := by
  norm_num [PositiveResponse, Nonzero, rank_two_matter_transfer_projector_rank]

/-- The concrete rank-two matter-transfer projector intertwines the frozen SU(2) doublet. -/
theorem rank_two_matter_transfer_projector_gauge_compatible
    (C : FiniteMatterTransferCarrier) :
    GaugeCompatible (rankTwoMatterTransferProjector C) := by
  intro x
  cases x <;>
    simp [rankTwoMatterTransferProjector, FiniteScalarProjector.project, weakSwap]

/-- Any nonzero gauge-compatible finite scalar projector has rank at least two. -/
theorem finite_scalar_projector_minimal_rank_two
    {C : FiniteMatterTransferCarrier} (P : FiniteScalarProjector C)
    (hnonzero : Nonzero P)
    (_hidempotent : Idempotent P)
    (_hpositive : PositiveResponse P)
    (_hscalar : ScalarCompatible P)
    (hgauge : GaugeCompatible P) :
    2 <= P.rank := by
  have hposRank : 0 < P.rank := by
    simpa [Nonzero] using hnonzero
  have hnot1 : Not (P.rank = 1) := by
    intro h
    exact finite_scalar_projector_rank_one_no_go P h hgauge
  cases h : P.rank with
  | zero =>
      rw [h] at hposRank
      exact False.elim (Nat.lt_irrefl 0 hposRank)
  | succ n =>
      cases n with
      | zero =>
          exact False.elim (hnot1 h)
      | succ m =>
          omega

/-- Rank-two projectors are unique in the fixed finite readout convention. -/
theorem finite_scalar_projector_rank_two_readout_unique
    {C : FiniteMatterTransferCarrier} (P Q : FiniteScalarProjector C)
    (hP : P.rank = 2) (hQ : Q.rank = 2) :
    ReadoutEquivalent P Q := by
  have hp := (finite_scalar_projector_rank_eq_two_iff P).mp hP
  have hq := (finite_scalar_projector_rank_eq_two_iff Q).mp hQ
  intro x
  cases x <;> simp [hp.1, hp.2, hq.1, hq.2]

/-- Constructive rank-two witness on a finite matter-transfer carrier. -/
structure RankTwoScalarWitness (C : FiniteMatterTransferCarrier) where
  P : FiniteScalarProjector C
  rank_two : P.rank = 2
  idem : Idempotent P
  pos : PositiveResponse P
  scalar : ScalarCompatible P
  gauge : GaugeCompatible P

/-- Constructive closure package for the finite Higgs/scalar projector. -/
structure ConstructiveScalarProjectorClosure (C : FiniteMatterTransferCarrier) where
  witness : FiniteScalarProjector C
  witness_rank_two : witness.rank = 2
  witness_idempotent : Idempotent witness
  witness_positive : PositiveResponse witness
  witness_scalar : ScalarCompatible witness
  witness_gauge : GaugeCompatible witness
  rank1_no_go :
    forall P : FiniteScalarProjector C, P.rank = 1 -> Not (GaugeCompatible P)
  minimal_rank :
    forall P : FiniteScalarProjector C,
      Nonzero P ->
      Idempotent P ->
      PositiveResponse P ->
      ScalarCompatible P ->
      GaugeCompatible P ->
      2 <= P.rank
  rank_two_unique :
    forall P : FiniteScalarProjector C, P.rank = 2 ->
      ReadoutEquivalent P witness

/-- Concrete rank-two witness for the finite EW matter-transfer carrier. -/
def finiteEWRankTwoScalarWitness :
    RankTwoScalarWitness finiteEWMatterTransferCarrier where
  P := rankTwoMatterTransferProjector finiteEWMatterTransferCarrier
  rank_two := rank_two_matter_transfer_projector_rank finiteEWMatterTransferCarrier
  idem := finite_scalar_projector_idempotent _
  pos := rank_two_matter_transfer_projector_positive finiteEWMatterTransferCarrier
  scalar := finite_scalar_projector_scalar_compatible _
  gauge := rank_two_matter_transfer_projector_gauge_compatible finiteEWMatterTransferCarrier

/--
Constructive closure: rank two is the minimal positive gauge-compatible scalar
projector rank on the finite EW matter-transfer carrier.
-/
def higgs_scalar_projector_constructive_closure :
    ConstructiveScalarProjectorClosure finiteEWMatterTransferCarrier := by
  refine
    { witness := rankTwoMatterTransferProjector finiteEWMatterTransferCarrier
      witness_rank_two := ?_
      witness_idempotent := ?_
      witness_positive := ?_
      witness_scalar := ?_
      witness_gauge := ?_
      rank1_no_go := ?_
      minimal_rank := ?_
      rank_two_unique := ?_ }
  · exact rank_two_matter_transfer_projector_rank finiteEWMatterTransferCarrier
  · exact finite_scalar_projector_idempotent _
  · exact rank_two_matter_transfer_projector_positive finiteEWMatterTransferCarrier
  · exact finite_scalar_projector_scalar_compatible _
  · exact rank_two_matter_transfer_projector_gauge_compatible finiteEWMatterTransferCarrier
  · intro P hP
    exact finite_scalar_projector_rank_one_no_go P hP
  · intro P hnonzero hidem hpos hscalar hgauge
    exact finite_scalar_projector_minimal_rank_two P hnonzero hidem hpos hscalar hgauge
  · intro P hP
    exact finite_scalar_projector_rank_two_readout_unique P
      (rankTwoMatterTransferProjector finiteEWMatterTransferCarrier) hP
      (rank_two_matter_transfer_projector_rank finiteEWMatterTransferCarrier)

end D0.Matter
