import D0.Gauge.AnomalySums

namespace D0

theorem SM_anomaly_sums_zero :
    gravU1Sum = 0 ∧ cubicU1Sum = 0 ∧
    su2su2u1Sum = 0 ∧ su3su3u1Sum = 0 := by
  exact ⟨grav_U1_anomaly_sum, U1_cubic_anomaly_sum,
    SU2_SU2_U1_anomaly_sum, SU3_SU3_U1_anomaly_sum⟩

end D0
