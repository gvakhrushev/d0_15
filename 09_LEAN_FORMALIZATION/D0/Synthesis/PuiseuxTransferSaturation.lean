import D0.Synthesis.CanonicalPuiseuxShellTransfer

/-!
# Puiseux transfer saturation: outer shell is the unique vertex, increments compress 3:1

T41 identified the unique minimal shell-coordinate transfer

`P(u) = u/3 - u²/12`.

Its completed-square form yields new structure:

`P(2) - P(u) = (u-2)²/12`.

Hence `u=2` is the unique global maximum over `ℚ`. Since the normalized shell coordinates are
`0,1,2`, the outer/tau shell is the unique saturation point of the canonical transfer.

The two generation increments are

`P(1)-P(0)=1/4`,  `P(2)-P(1)=1/12`,

so the first is exactly three times the second. This is a structural diminishing-increment law,
not a statement about physical mass differences.
-/

namespace D0.Synthesis.PuiseuxTransferSaturation

open D0.Geometry
open D0.Matter
open D0.Synthesis.CanonicalPuiseuxShellTransfer

/-- Factorized form of the canonical Puiseux quadratic. -/
theorem puiseuxQuadraticShape_factor (u : ℚ) :
    puiseuxQuadraticShape u = u * (4 - u) / 12 := by
  simp [puiseuxQuadraticShape]
  ring

/-- Completed-square vertex identity. -/
theorem puiseuxQuadraticShape_vertex_identity (u : ℚ) :
    puiseuxQuadraticShape 2 - puiseuxQuadraticShape u = (u - 2) ^ 2 / 12 := by
  simp [puiseuxQuadraticShape]
  ring

/-- The canonical transfer is globally bounded above by its value at `u=2`. -/
theorem puiseuxQuadraticShape_le_vertex (u : ℚ) :
    puiseuxQuadraticShape u ≤ puiseuxQuadraticShape 2 := by
  have hs : 0 ≤ (u - 2) ^ 2 := sq_nonneg (u - 2)
  have hdiv : 0 ≤ (u - 2) ^ 2 / 12 := div_nonneg hs (by norm_num)
  have hv := puiseuxQuadraticShape_vertex_identity u
  linarith

/-- The maximum is unique: equality with the vertex value forces `u=2`. -/
theorem puiseuxQuadraticShape_eq_vertex_iff (u : ℚ) :
    puiseuxQuadraticShape u = puiseuxQuadraticShape 2 ↔ u = 2 := by
  constructor
  · intro h
    have hv := puiseuxQuadraticShape_vertex_identity u
    rw [h] at hv
    norm_num at hv
    have hs : (u - 2) ^ 2 = 0 := by linarith
    have hz : u - 2 = 0 := sq_eq_zero_iff.mp hs
    linarith
  · rintro rfl
    rfl

/-- Exact first generation increment. -/
theorem puiseux_first_increment :
    puiseuxQuadraticShape 1 - puiseuxQuadraticShape 0 = 1 / 4 := by
  norm_num [puiseuxQuadraticShape]

/-- Exact second generation increment. -/
theorem puiseux_second_increment :
    puiseuxQuadraticShape 2 - puiseuxQuadraticShape 1 = 1 / 12 := by
  norm_num [puiseuxQuadraticShape]

/-- **Threefold compression.** The inner→core increment is exactly three times the
core→outer increment. -/
theorem puiseux_increment_compression_three :
    puiseuxQuadraticShape 1 - puiseuxQuadraticShape 0
      = 3 * (puiseuxQuadraticShape 2 - puiseuxQuadraticShape 1) := by
  norm_num [puiseuxQuadraticShape]

/-- The outer shell is the unique maximizer of the canonical transfer on the three-shell
carrier, for every admissible torus metric. -/
theorem canonicalPuiseuxShellReadout_outer_unique_max (T : TorusParameter) :
    ∀ s : TorusShell,
      canonicalPuiseuxShellReadout T s ≤ canonicalPuiseuxShellReadout T .outerD13
      ∧ (canonicalPuiseuxShellReadout T s =
          canonicalPuiseuxShellReadout T .outerD13 ↔ s = .outerD13) := by
  intro s
  cases s
  all_goals simp [p_e, p_mu, p_tau]
  all_goals norm_num

/-- Shell-level increments inherit the exact `3:1` compression independently of `g`. -/
theorem canonical_shell_increment_compression_three (T : TorusParameter) :
    canonicalPuiseuxShellReadout T .coreD11 -
        canonicalPuiseuxShellReadout T .innerD9
      = 3 * (canonicalPuiseuxShellReadout T .outerD13 -
        canonicalPuiseuxShellReadout T .coreD11) := by
  norm_num [p_e, p_mu, p_tau]

/-- Capstone: the unique minimal transfer is a saturating concave law with outer-shell vertex
and exact threefold compression of adjacent increments. -/
theorem puiseux_transfer_saturation :
    (∀ u : ℚ,
        puiseuxQuadraticShape 2 - puiseuxQuadraticShape u = (u - 2) ^ 2 / 12)
    ∧ (∀ u : ℚ, puiseuxQuadraticShape u ≤ puiseuxQuadraticShape 2)
    ∧ (∀ u : ℚ, puiseuxQuadraticShape u = puiseuxQuadraticShape 2 ↔ u = 2)
    ∧ (puiseuxQuadraticShape 1 - puiseuxQuadraticShape 0
        = 3 * (puiseuxQuadraticShape 2 - puiseuxQuadraticShape 1))
    ∧ (∀ T : TorusParameter,
        ∀ s : TorusShell,
          canonicalPuiseuxShellReadout T s ≤ canonicalPuiseuxShellReadout T .outerD13
          ∧ (canonicalPuiseuxShellReadout T s =
              canonicalPuiseuxShellReadout T .outerD13 ↔ s = .outerD13)) :=
  ⟨puiseuxQuadraticShape_vertex_identity, puiseuxQuadraticShape_le_vertex,
    puiseuxQuadraticShape_eq_vertex_iff, puiseux_increment_compression_three,
    canonicalPuiseuxShellReadout_outer_unique_max⟩

end D0.Synthesis.PuiseuxTransferSaturation
