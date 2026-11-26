import Mathlib.Tactic

def heatTiltSq (q w20 w22 w24 w33 : ℚ) : ℚ :=
  (-2 * q) *
    (w20 / (q + 20)^2 + w22 / (q + 22)^2 +
     w24 / (q + 24)^2 + w33 / (q + 33)^2) /
    (w20 / (q + 20) + w22 / (q + 22) +
     w24 / (q + 24) + w33 / (q + 33))

theorem at_zero :
    heatTiltSq 20 12 10 8 2 = -(1080004747 : ℚ) / 1135648437 := by
  norm_num [heatTiltSq]

theorem at_log_two :
    heatTiltSq 20 12 (5 / 2) (1 / 2) (1 / 4096) =
      -(1126676931656 : ℚ) / 1138552807161 := by
  norm_num [heatTiltSq]

theorem different :
    heatTiltSq 20 12 10 8 2 -
      heatTiltSq 20 12 (5 / 2) (1 / 2) (1 / 4096) =
      (332684708845 : ℚ) / 8626237020293 := by
  norm_num [heatTiltSq]

theorem at_twice_log_two :
    heatTiltSq 20 12 (5 / 8) (1 / 32) (1 / 33554432) =
      -(7916899768391752 : ℚ) / 7936343423567097 := by
  norm_num [heatTiltSq]

theorem positive_times_differ :
    heatTiltSq 20 12 (5 / 2) (1 / 2) (1 / 4096) -
      heatTiltSq 20 12 (5 / 8) (1 / 32) (1 / 33554432) =
      (481105434667074560 : ℚ) / 60283426820877473033 := by
  norm_num [heatTiltSq]
