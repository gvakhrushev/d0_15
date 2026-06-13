import D0.Core.Delta

/-!
# D0-DIM-LADDER-COMPACT-001 — dimension ladder compactifies to phi^(D-4)

Per-claim leaf module mirroring the exact-arithmetic certificate
`05_CERTS/vp_dim_ladder_compact.py`.

The certificate works in `Q(phi)` (no floats) and asserts that the dimension
quantum compactifies to a single exponent centered on the role budget
`|ABCD| = 4`:

    Q(D) = delta0 * 2 * phi^(D-1) = phi^(D-4)

so the quantum equals `1` exactly at `D = 4`, the binary quantum (`D = 1`) is
`phi^-3 = 2 * delta0`, and the delta cascade `delta_{-n} = delta0^(n+1)` is
geometric with ratio `delta0`.

We reuse the frozen `D0.Core.Phi` / `D0.Core.Delta`, where `phi : ℝ` is the
golden ratio and `delta0 = 1 / (2 * phi^3)`. All four certificate facts are
proved exactly over `ℝ` (the golden-ratio identities are exact, `delta0` is a
closed form, and the cascade identity is a pure ring identity).
-/

namespace D0.Claims

open D0

/-- `phi` is strictly positive, hence nonzero — needed to manipulate `zpow`. -/
private theorem phi_pos : (0 : ℝ) < phi := by
  unfold phi; positivity

private theorem phi_ne_zero : (phi : ℝ) ≠ 0 := ne_of_gt phi_pos

/-- The doubled quantum normalizer collapses to a pure power: `delta0 * 2 = phi^(-3)`.
This is the engine of the whole compactification (`delta0 = 1/(2 phi^3)`). -/
theorem two_delta0_eq_phi_negpow : delta0 * 2 = phi ^ (-3 : ℤ) := by
  rw [delta_phi_cubed]
  rw [zpow_neg, zpow_ofNat]
  field_simp

/-- **[1] (THE)** Exact dimension-ladder compactification, for every integer `D`:
the dimension quantum `delta0 * 2 * phi^(D-1)` equals the single centered
exponent `phi^(D-4)`. This is strictly stronger than the certificate's
`D = 1..8` finite check. -/
theorem dim_ladder_compact (D : ℤ) :
    delta0 * 2 * phi ^ (D - 1) = phi ^ (D - 4) := by
  rw [two_delta0_eq_phi_negpow, ← zpow_add₀ phi_ne_zero]
  ring_nf

/-- The certificate's finite instances `D = 1..8` follow immediately, and the
right-hand side is the already-defined dimension quantum `Q`. -/
theorem dim_ladder_compact_eq_Q (D : ℤ) :
    delta0 * 2 * phi ^ (D - 1) = Q D := by
  rw [Q_dimension_ladder]; exact dim_ladder_compact D

/-- **[2]** The quantum equals `1` exactly at `D = 4` (the four-role budget). -/
theorem quantum_one_at_four : delta0 * 2 * phi ^ (3 : ℤ) = 1 := by
  have h := dim_ladder_compact 4
  norm_num at h ⊢
  simpa using h

/-- **[3]** The binary cut quantum (`D = 1`) is `phi^-3 = 2 * delta0`. -/
theorem binary_quantum : phi ^ (-3 : ℤ) = 2 * delta0 := by
  rw [← two_delta0_eq_phi_negpow]; ring

/-- **[4]** The delta cascade `delta_{-n} = delta0^(n+1)` is geometric with ratio
`delta0`: the geometric-mean identity `delta0^n * delta0^(n+2) = (delta0^(n+1))^2`
holds for every `n`. -/
theorem delta_cascade_geometric (n : ℕ) :
    delta0 ^ n * delta0 ^ (n + 2) = (delta0 ^ (n + 1)) ^ 2 := by
  ring

/-- Bundled statement of the whole certificate `PASS_DIM_LADDER_COMPACT`. -/
theorem dim_ladder_compact_cert :
    (∀ D : ℤ, delta0 * 2 * phi ^ (D - 1) = phi ^ (D - 4)) ∧
    (delta0 * 2 * phi ^ (3 : ℤ) = 1) ∧
    (phi ^ (-3 : ℤ) = 2 * delta0) ∧
    (∀ n : ℕ, delta0 ^ n * delta0 ^ (n + 2) = (delta0 ^ (n + 1)) ^ 2) :=
  ⟨dim_ladder_compact, quantum_one_at_four, binary_quantum, delta_cascade_geometric⟩

end D0.Claims
