import D0.Gauge.SMCharges
import Mathlib.Tactic

namespace D0

def gravU1Sum : ℚ :=
  6 * (1 / 6) + 3 * (-2 / 3) + 3 * (1 / 3) + 2 * (-1 / 2) + 1 * 1 + 1 * 0

def cubicU1Sum : ℚ :=
  6 * (1 / 6)^3 + 3 * (-2 / 3)^3 + 3 * (1 / 3)^3 + 2 * (-1 / 2)^3 + 1 * 1^3 + 1 * 0^3

def su2su2u1Sum : ℚ :=
  3 * (1 / 6) + 1 * (-1 / 2)

def su3su3u1Sum : ℚ :=
  2 * (1 / 6) + (-2 / 3) + (1 / 3)

theorem grav_U1_anomaly_sum : gravU1Sum = 0 := by
  norm_num [gravU1Sum]

theorem U1_cubic_anomaly_sum : cubicU1Sum = 0 := by
  norm_num [cubicU1Sum]

theorem SU2_SU2_U1_anomaly_sum : su2su2u1Sum = 0 := by
  norm_num [su2su2u1Sum]

theorem SU3_SU3_U1_anomaly_sum : su3su3u1Sum = 0 := by
  norm_num [su3su3u1Sum]

end D0
