import D0.Core.BornFinite

namespace D0

open scoped BigOperators

/--
A finite detector effect frame.  The hidden state space `σ` is finite, every
finite effect is nonnegative on every state atom, and the detector state is
nonnegative.  The strictly positive total response is the only normalization
assumption.

This is the finite-frame owner of the trace notation
`Tr(E_i R) / Tr(R)`: the trace language is only one matrix presentation of the
finite sums below.
-/
structure FiniteEffectFrame (ι σ : Type) [Fintype ι] [Fintype σ] where
  effect : ι → σ → ℚ
  detector : σ → ℚ
  effect_nonnegative : ∀ i s, 0 ≤ effect i s
  detector_nonnegative : ∀ s, 0 ≤ detector s
  total_response_positive : 0 < ∑ i, ∑ s, effect i s * detector s

/-- Raw response of one finite effect against the detector state. -/
def finiteEffectResponse {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (i : ι) : ℚ :=
  ∑ s, F.effect i s * F.detector s

/-- Effect responses are nonnegative because both the effect and detector state are nonnegative. -/
theorem finite_effect_response_nonnegative {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (i : ι) :
    0 ≤ finiteEffectResponse F i := by
  unfold finiteEffectResponse
  exact Finset.sum_nonneg (fun s _ => mul_nonneg (F.effect_nonnegative i s) (F.detector_nonnegative s))

/-- The finite effect frame induces an ordinary finite positive response. -/
def finiteEffectFramePositiveResponse {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) : FinitePositiveResponse ι where
  response := finiteEffectResponse F
  nonnegative := finite_effect_response_nonnegative F
  total_positive := by
    simpa [finiteResponseTotal, finiteEffectResponse] using F.total_response_positive

/-- Born weight of a finite effect frame. -/
def finiteEffectBornWeight {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (i : ι) : ℚ :=
  finiteResponseBornWeight (finiteEffectFramePositiveResponse F) i

/-- Candidate readout for a finite effect frame. -/
abbrev FiniteEffectBornReadout {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) :=
  FiniteBornReadout (finiteEffectFramePositiveResponse F)

/--
Finite-frame Born 2.0 uniqueness.
For a finite effect frame, any admissible readout that recovers the raw effect
response is forced to be the normalized detector response.
-/
theorem finite_effect_born_readout_unique {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (q : FiniteEffectBornReadout F) :
    ∀ i, q.probability i = finiteEffectBornWeight F i := by
  intro i
  exact finite_born_readout_unique_on_finite_outcomes (finiteEffectFramePositiveResponse F) q i

/--
No hidden positive state: at fixed finite effect frame, a different probability
assignment cannot also recover the same raw detector responses.
-/
theorem finite_effect_born_no_hidden_response {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (q : FiniteEffectBornReadout F)
    (hneq : ∃ i, q.probability i ≠ finiteEffectBornWeight F i) : False := by
  rcases hneq with ⟨i, hi⟩
  exact hi (finite_effect_born_readout_unique F q i)

/-- Aggregated raw response for a finite coarse-graining map. -/
def finiteCoarseResponse {ι σ κ : Type} [Fintype ι] [Fintype σ] [Fintype κ]
    [DecidableEq κ] (F : FiniteEffectFrame ι σ) (π : ι → κ) (k : κ) : ℚ :=
  (Finset.univ.filter (fun i => π i = k)).sum (fun i => finiteEffectResponse F i)

/-- A finite coarse-graining is admissible when its aggregated total response is positive. -/
structure FiniteCoarseGraining {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (κ : Type) [Fintype κ] [DecidableEq κ] where
  map : ι → κ
  total_positive : 0 < ∑ k, finiteCoarseResponse F map k

/-- Positive-response object induced by a finite coarse-graining. -/
def finiteCoarsePositiveResponse {ι σ κ : Type} [Fintype ι] [Fintype σ]
    [Fintype κ] [DecidableEq κ]
    (F : FiniteEffectFrame ι σ) (C : FiniteCoarseGraining F κ) :
    FinitePositiveResponse κ where
  response := finiteCoarseResponse F C.map
  nonnegative := by
    intro k
    unfold finiteCoarseResponse
    exact Finset.sum_nonneg (fun i _ => finite_effect_response_nonnegative F i)
  total_positive := C.total_positive

/-- Coarse-grained Born weight: aggregate first, then normalize. -/
def finiteCoarseBornWeight {ι σ κ : Type} [Fintype ι] [Fintype σ]
    [Fintype κ] [DecidableEq κ]
    (F : FiniteEffectFrame ι σ) (C : FiniteCoarseGraining F κ) (k : κ) : ℚ :=
  finiteResponseBornWeight (finiteCoarsePositiveResponse F C) k

/-- Candidate readout for a finite coarse-graining. -/
abbrev FiniteCoarseBornReadout {ι σ κ : Type} [Fintype ι] [Fintype σ]
    [Fintype κ] [DecidableEq κ]
    (F : FiniteEffectFrame ι σ) (C : FiniteCoarseGraining F κ) :=
  FiniteBornReadout (finiteCoarsePositiveResponse F C)

/-- Coarse-graining cannot introduce a second probability rule. -/
theorem finite_coarse_born_readout_unique {ι σ κ : Type} [Fintype ι] [Fintype σ]
    [Fintype κ] [DecidableEq κ]
    (F : FiniteEffectFrame ι σ) (C : FiniteCoarseGraining F κ)
    (q : FiniteCoarseBornReadout F C) :
    ∀ k, q.probability k = finiteCoarseBornWeight F C k := by
  intro k
  exact finite_born_readout_unique_on_finite_outcomes (finiteCoarsePositiveResponse F C) q k

/--
A candidate nonlinear/power readout is harmless only if it still satisfies the
same detector recovery rule.  Then it collapses pointwise to the finite Born
weight; if it differs anywhere, it is not an admissible D0 readout.
-/
structure FinitePowerReadoutCandidate {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) where
  exponent : ℕ
  probability : ι → ℚ
  normalized : ∑ i, probability i = 1
  response_rule : ∀ i, probability i * finiteResponseTotal r = r.response i

/-- Power/nonlinear readout no-go at fixed finite response. -/
theorem finite_power_readout_collapses_to_born {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FinitePowerReadoutCandidate r) :
    ∀ i, q.probability i = finiteResponseBornWeight r i := by
  let qBorn : FiniteBornReadout r :=
    { probability := q.probability
      normalized := q.normalized
      response_rule := q.response_rule }
  exact finite_born_readout_unique_on_finite_outcomes r qBorn

/-- Any alleged power readout that differs from Born fails D0 admissibility. -/
theorem finite_power_readout_no_alternative {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FinitePowerReadoutCandidate r)
    (hneq : ∃ i, q.probability i ≠ finiteResponseBornWeight r i) : False := by
  rcases hneq with ⟨i, hi⟩
  exact hi (finite_power_readout_collapses_to_born r q i)

/--
Tensor/product readout certificate.  The product response is an explicit finite
positive response over the product outcome type.  A different joint probability
assignment cannot be inserted once that product response is fixed.
-/
structure FiniteTensorResponse (ι κ : Type) [Fintype ι] [Fintype κ] where
  response_left : FinitePositiveResponse ι
  response_right : FinitePositiveResponse κ
  response_product : FinitePositiveResponse (ι × κ)
  product_rule : ∀ i k,
    response_product.response (i, k) = response_left.response i * response_right.response k

/-- Candidate readout for the product response. -/
abbrev FiniteTensorBornReadout {ι κ : Type} [Fintype ι] [Fintype κ]
    (T : FiniteTensorResponse ι κ) :=
  FiniteBornReadout T.response_product

/-- Tensor consistency: once the product response is fixed, the joint readout is unique. -/
theorem finite_tensor_born_readout_unique {ι κ : Type} [Fintype ι] [Fintype κ]
    (T : FiniteTensorResponse ι κ) (q : FiniteTensorBornReadout T) :
    ∀ x, q.probability x = finiteResponseBornWeight T.response_product x := by
  exact finite_born_readout_unique_on_finite_outcomes T.response_product q

end D0
