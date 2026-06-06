import D0.Dynamics.ToralAutomorphism
import D0.Dynamics.GaloisConjugateBalance
import D0.Dynamics.DarkSectorCoarseGrain

namespace D0.Dynamics

/-- Positive time-energy operator used for heat-moment readout. -/
def TimeEnergyOperator : ZMat2 :=
  T ^ 2

theorem heat_moment_T2_eq_even_lucas_trace (m : Nat) :
    Matrix.trace (TimeEnergyOperator ^ m) =
      Matrix.trace (T ^ (2 * m)) := by
  unfold TimeEnergyOperator
  have h : T ^ (2 * m) = (T ^ 2) ^ m := by
    rw [pow_mul]
  rw [h]

theorem even_trace_eq_lucas_even (m : Nat) :
    Matrix.trace (T ^ (2 * m)) = lucas (2 * m) := by
  rw [trace_T_pow_eq_signed_lucas]
  unfold signedLucasTrace
  have hsign : (-1 : Int) ^ (2 * m) = 1 := by
    exact dark_sign_even m
  rw [hsign]
  simp

theorem heat_moment_eq_even_lucas (m : Nat) :
    Matrix.trace (TimeEnergyOperator ^ m) = lucas (2 * m) := by
  rw [heat_moment_T2_eq_even_lucas_trace, even_trace_eq_lucas_even]

/-- Anti-periodic Lefschetz/Fermion orbit count before absolute-value readout. -/
def NFermionInt (n : Nat) : Int :=
  Matrix.det (T ^ n + 1)

/-- Natural-number readout of the anti-periodic Lefschetz/Fermion orbit count. -/
def NFermion (n : Nat) : Nat :=
  Int.natAbs (NFermionInt n)

theorem lefschetz_spectrum_unfolds_scene :
    NFermion 3 = 4 /\
    NFermion 4 = 9 /\
    NFermion 5 = 11 /\
    NFermion 3 + NFermion 4 = 13 /\
    NFermion 6 = 20 := by
  native_decide

end D0.Dynamics
