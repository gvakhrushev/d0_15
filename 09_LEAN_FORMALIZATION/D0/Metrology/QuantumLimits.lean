import D0.Metrology.PSDPurification
import Mathlib.Tactic

/-!
# D0-QUANT-MET-001 — quantum metrology limits (purification operator lemma)

Metrology layer. Shared cert: `05_CERTS/vp_quantum_metrology_limits.py`.

The cert-closed operator core: when the lab projector `Π` sits inside the system projector `P_N`
(`Π·P_N = Π`), the purification difference `F_lab − Π F_N Π = Π Uᴴ (P_N − Π) U Π` is positive
semidefinite. This module assembles that from `PSDPurification` (the conjugation lemma + the PSD of the
projector difference `P_N − Π`).

The non-Gaussian kurtosis target (`D0-QUANT-MET-004`) and the conditional `φ⁻²` flux value
(`D0-QUANT-MET-003`) are the conditional/equidistribution siblings and stay their own rows.
-/

namespace D0.Metrology

open Matrix

/-- **D0-QUANT-MET-001.** The purification inequality `F_lab − Π F_N Π ≽ 0` in collapsed form:
`Π Uᴴ (P_N − Π) U Π` is positive semidefinite for any `U` and any Hermitian idempotent projectors
`Π ≤ P_N` (`Π·P_N = Π`). -/
theorem quantum_metrology_limits {n : ℕ} (U PN Pi : Matrix (Fin n) (Fin n) ℝ)
    (hPNh : PNᴴ = PN) (hPNi : PN * PN = PN) (hPih : Piᴴ = Pi) (hPii : Pi * Pi = Pi)
    (hsub : Pi * PN = Pi) :
    (Pi * Uᴴ * (PN - Pi) * U * Pi).PosSemidef :=
  psd_purification_inequality U Pi (PN - Pi) hPih
    (proj_diff_posSemidef PN Pi hPNh hPNi hPih hPii hsub)

end D0.Metrology
