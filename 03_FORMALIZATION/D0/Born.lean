import D0.Core.BornFinite
import D0.Core.BornFiniteEffects
import D0.Core.BornQuadraticResponse
import D0.Core.BornQuadraticOrigin

namespace D0

theorem finite_born_sum_one (b : TwoOutcomeBorn) : b.p0 + b.p1 = 1 :=
  born_response_sum_one b

theorem finite_born_nonnegative (b : TwoOutcomeBorn) : 0 ≤ b.p0 ∧ 0 ≤ b.p1 :=
  born_response_nonnegative b

theorem finite_response_born_weights_sum_one (r : TwoChannelPositiveResponse) :
    responseBornWeight0 r + responseBornWeight1 r = 1 :=
  response_born_weights_sum_one r

theorem finite_response_born_weights_nonnegative (r : TwoChannelPositiveResponse) :
    0 ≤ responseBornWeight0 r ∧ 0 ≤ responseBornWeight1 r :=
  response_born_weights_nonnegative r

theorem finite_born_readout_unique
    (r : TwoChannelPositiveResponse) (q : TwoChannelReadout r) :
    q.p0 = responseBornWeight0 r ∧ q.p1 = responseBornWeight1 r :=
  finite_born_two_channel_readout_unique r q


theorem finite_born_weight_recovers_response {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (i : ι) :
    finiteResponseBornWeight r i * finiteResponseTotal r = r.response i :=
  D0.finite_response_born_weight_recovers_response r i

theorem finite_born_unique_on_finite_outcomes {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FiniteBornReadout r) :
    ∀ i, q.probability i = finiteResponseBornWeight r i :=
  D0.finite_born_readout_unique_on_finite_outcomes r q

theorem finite_born_no_alternative_finite_readout {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FiniteBornReadout r)
    (hneq : ∃ i, q.probability i ≠ finiteResponseBornWeight r i) : False :=
  D0.finite_born_no_alternative_readout r q hneq


theorem finite_effect_born_unique {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (q : FiniteEffectBornReadout F) :
    ∀ i, q.probability i = finiteEffectBornWeight F i :=
  D0.finite_effect_born_readout_unique F q

theorem finite_effect_born_no_hidden_response_owner {ι σ : Type} [Fintype ι] [Fintype σ]
    (F : FiniteEffectFrame ι σ) (q : FiniteEffectBornReadout F)
    (hneq : ∃ i, q.probability i ≠ finiteEffectBornWeight F i) : False :=
  D0.finite_effect_born_no_hidden_response F q hneq

theorem finite_coarse_born_unique {ι σ κ : Type} [Fintype ι] [Fintype σ]
    [Fintype κ] [DecidableEq κ]
    (F : FiniteEffectFrame ι σ) (C : FiniteCoarseGraining F κ)
    (q : FiniteCoarseBornReadout F C) :
    ∀ k, q.probability k = finiteCoarseBornWeight F C k :=
  D0.finite_coarse_born_readout_unique F C q

theorem finite_power_readout_no_alternative_owner {ι : Type} [Fintype ι]
    (r : FinitePositiveResponse ι) (q : FinitePowerReadoutCandidate r)
    (hneq : ∃ i, q.probability i ≠ finiteResponseBornWeight r i) : False :=
  D0.finite_power_readout_no_alternative r q hneq

theorem finite_tensor_born_unique {ι κ : Type} [Fintype ι] [Fintype κ]
    (T : FiniteTensorResponse ι κ) (q : FiniteTensorBornReadout T) :
    ∀ x, q.probability x = finiteResponseBornWeight T.response_product x :=
  D0.finite_tensor_born_readout_unique T q


theorem phase_blind_quadratic_response_scaled_owner
    (Q : PhaseQuadraticResponse) (hQ : QuarterTurnInvariant Q) :
    ∀ z, phaseQuadraticEval Q z = Q.xx * amplitudeNormSq z :=
  D0.phase_blind_quadratic_response_is_norm_sq_scaled Q hQ

theorem unit_phase_blind_quadratic_response_owner
    (Q : UnitPhaseQuadraticResponse) :
    ∀ z, phaseQuadraticEval Q.response z = amplitudeNormSq z :=
  D0.unit_phase_blind_quadratic_response_is_norm_sq Q

theorem finite_amplitude_born_unique_owner {ι σ : Type} [Fintype ι] [Fintype σ]
    (A : FiniteAmplitudeEffectFrame ι σ) (q : FiniteAmplitudeBornReadout A) :
    ∀ i, q.probability i = finiteAmplitudeBornWeight A i :=
  D0.finite_amplitude_born_readout_unique A q

theorem finite_amplitude_born_no_alternative_owner {ι σ : Type} [Fintype ι] [Fintype σ]
    (A : FiniteAmplitudeEffectFrame ι σ) (q : FiniteAmplitudeBornReadout A)
    (hneq : ∃ i, q.probability i ≠ finiteAmplitudeBornWeight A i) : False :=
  D0.finite_amplitude_born_no_alternative A q hneq

end D0
