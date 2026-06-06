import D0.Core.MatrixResponse

namespace D0

open scoped BigOperators

structure TwoOutcomeBorn where
  p0 : ℚ
  p1 : ℚ
  nonnegative0 : 0 ≤ p0
  nonnegative1 : 0 ≤ p1
  normalized : p0 + p1 = 1

theorem born_response_sum_one (b : TwoOutcomeBorn) : b.p0 + b.p1 = 1 :=
  b.normalized

theorem born_response_nonnegative (b : TwoOutcomeBorn) : 0 ≤ b.p0 ∧ 0 ≤ b.p1 :=
  ⟨b.nonnegative0, b.nonnegative1⟩

/--
A finite two-channel detector response before probabilistic normalization.
The only physical input here is positivity plus a nonzero total response.
-/
structure TwoChannelPositiveResponse where
  r0 : ℚ
  r1 : ℚ
  nonnegative0 : 0 ≤ r0
  nonnegative1 : 0 ≤ r1
  total_positive : 0 < r0 + r1

/-- Born normalization of the first finite response channel. -/
def responseBornWeight0 (r : TwoChannelPositiveResponse) : ℚ :=
  r.r0 / (r.r0 + r.r1)

/-- Born normalization of the second finite response channel. -/
def responseBornWeight1 (r : TwoChannelPositiveResponse) : ℚ :=
  r.r1 / (r.r0 + r.r1)

/--
A candidate finite readout is admissible when multiplying the reported weight by
the total detector response recovers the corresponding raw response.
This is the finite, two-channel form of the detector rule `probability = response / total response`.
-/
structure TwoChannelReadout (r : TwoChannelPositiveResponse) where
  p0 : ℚ
  p1 : ℚ
  normalized : p0 + p1 = 1
  response_rule0 : p0 * (r.r0 + r.r1) = r.r0
  response_rule1 : p1 * (r.r0 + r.r1) = r.r1

theorem response_born_weights_sum_one (r : TwoChannelPositiveResponse) :
    responseBornWeight0 r + responseBornWeight1 r = 1 := by
  have hden : r.r0 + r.r1 ≠ 0 := ne_of_gt r.total_positive
  unfold responseBornWeight0 responseBornWeight1
  field_simp [hden]

theorem response_born_weights_nonnegative (r : TwoChannelPositiveResponse) :
    0 ≤ responseBornWeight0 r ∧ 0 ≤ responseBornWeight1 r := by
  have hden_nonneg : 0 ≤ r.r0 + r.r1 := le_of_lt r.total_positive
  constructor
  · unfold responseBornWeight0
    exact div_nonneg r.nonnegative0 hden_nonneg
  · unfold responseBornWeight1
    exact div_nonneg r.nonnegative1 hden_nonneg

/-- The detector response itself produces a normalized finite Born readout. -/
def bornReadoutOfResponse (r : TwoChannelPositiveResponse) : TwoOutcomeBorn where
  p0 := responseBornWeight0 r
  p1 := responseBornWeight1 r
  nonnegative0 := (response_born_weights_nonnegative r).1
  nonnegative1 := (response_born_weights_nonnegative r).2
  normalized := response_born_weights_sum_one r

/--
Finite Born uniqueness, two-channel form.
Any admissible readout satisfying the response-recovery rule is forced to be the
normalized positive response.  Thus the probability weights are not an extra
phenomenological choice at this finite level.
-/
theorem finite_born_two_channel_readout_unique
    (r : TwoChannelPositiveResponse) (q : TwoChannelReadout r) :
    q.p0 = responseBornWeight0 r ∧ q.p1 = responseBornWeight1 r := by
  have hden : r.r0 + r.r1 ≠ 0 := ne_of_gt r.total_positive
  constructor
  · unfold responseBornWeight0
    exact (eq_div_iff hden).2 q.response_rule0
  · unfold responseBornWeight1
    exact (eq_div_iff hden).2 q.response_rule1

/--
A finite detector response over an arbitrary finite outcome type.  This is the
Lean-level replacement for the two-channel-only Born closure: the primitive data
are raw nonnegative detector responses and a strictly positive total response.
-/
structure FinitePositiveResponse (ι : Type) [Fintype ι] where
  response : ι → ℚ
  nonnegative : ∀ i, 0 ≤ response i
  total_positive : 0 < ∑ i, response i

/-- Total raw detector response over a finite outcome type. -/
def finiteResponseTotal {ι : Type} [Fintype ι] (r : FinitePositiveResponse ι) : ℚ :=
  ∑ i, r.response i

/-- Born normalization of a finite raw response channel. -/
def finiteResponseBornWeight {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (i : ι) : ℚ :=
  r.response i / finiteResponseTotal r

/-- Candidate finite readout for an arbitrary finite outcome type. -/
structure FiniteBornReadout {ι : Type} [Fintype ι] (r : FinitePositiveResponse ι) where
  probability : ι → ℚ
  normalized : ∑ i, probability i = 1
  response_rule : ∀ i, probability i * finiteResponseTotal r = r.response i

theorem finite_response_total_ne_zero {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) : finiteResponseTotal r ≠ 0 := by
  exact ne_of_gt r.total_positive

theorem finite_response_born_weight_nonnegative {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (i : ι) :
    0 ≤ finiteResponseBornWeight r i := by
  unfold finiteResponseBornWeight
  exact div_nonneg (r.nonnegative i) (le_of_lt r.total_positive)

/-- The normalized Born weight recovers the raw detector response. -/
theorem finite_response_born_weight_recovers_response {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (i : ι) :
    finiteResponseBornWeight r i * finiteResponseTotal r = r.response i := by
  have hden : finiteResponseTotal r ≠ 0 := finite_response_total_ne_zero r
  unfold finiteResponseBornWeight
  field_simp [hden]

/--
Finite Born uniqueness over arbitrary finite outcome sets.
Once the positive detector response and response-recovery rule are fixed, every
admissible probability readout is pointwise equal to the normalized response.
-/
theorem finite_born_readout_unique_on_finite_outcomes {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FiniteBornReadout r) :
    ∀ i, q.probability i = finiteResponseBornWeight r i := by
  intro i
  have hden : finiteResponseTotal r ≠ 0 := finite_response_total_ne_zero r
  unfold finiteResponseBornWeight
  exact (eq_div_iff hden).2 (q.response_rule i)

/--
No alternative finite probability assignment can satisfy the detector recovery
rule while differing from normalized response on any channel.
-/
theorem finite_born_no_alternative_readout {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FiniteBornReadout r)
    (hneq : ∃ i, q.probability i ≠ finiteResponseBornWeight r i) : False := by
  rcases hneq with ⟨i, hi⟩
  exact hi (finite_born_readout_unique_on_finite_outcomes r q i)

end D0
