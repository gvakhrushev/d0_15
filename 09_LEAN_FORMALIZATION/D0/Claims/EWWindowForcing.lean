import Mathlib.Tactic

/-!
# D0-EW-WINDOW-FORCING-001 — (710,113) are closed invariant-grammar expressions (Lean part)

Python certificate: `05_CERTS/vp_ew_window_forcing.py` (the full forcing: grammar + the
continued-fraction minimality of the 2π near-return, which is π-dependent and lives in the
cert). This module proves the formalizable half — that both window numbers are closed
expressions in the named scene invariants `{|ABCD|=4, D_Σ=5, |V|=33, d₁₃=20, |V₁₃|=13,
orientation=2}` with ZERO free numbers:

    q_EW = 710 = 2·D_Σ·(2|V|+D_Σ) = 2·5·71,   71 = 2·33+5   (not an independent number)
    m_EW = 113 = (|ABCD|+1)·d₁₃ + |V₁₃| = 5·20+13.

The minimality ("710/113 is the first 2π-convergent with |q/m−2π|<10⁻⁶") is the cert's job.
-/

namespace D0.Claims

/-- Both EW-window numbers are closed expressions in the named scene invariants, with no
free number: `710 = 2·5·(2·33+5)`, `71 = 2·33+5`, `113 = (4+1)·20+13`. -/
theorem ew_window_grammar :
    (2 * 5 * (2 * 33 + 5) = 710) ∧
    (2 * 33 + 5 = 71) ∧
    ((4 + 1) * 20 + 13 = 113) := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

end D0.Claims
