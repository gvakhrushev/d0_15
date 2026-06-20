import D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-!
# D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001 — n_s is not forced by present-core

Maximality strengthening of `D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001`. The discrete spectral tilt
`n_eff − 1 = (k/P)·P'(k)` of the heat-smoothed phason power proxy on the nonzero modes `{20,22,24,33}`
depends on the smoothing measure (the positive weighting `w_i` of the modes). The previous no-go showed
two admissible measures differ; here we exhibit **three distinct admissible smoothing measures**, all
legitimate positive weightings of the same spectrum, that give **three distinct tilts**:

- `A` = flat multiplicity `(12,10,8,2)` (the `u=0` reading),
- `B` = low-`λ` emphasis `(12,5,2,1)`,
- `C` = high-`λ` emphasis `(2,4,8,12)`.

So the induced tilt (hence `n_s`) is a genuinely non-constant function of an unfixed admissible parameter:
**no canonical `(k,u)` is forced by present-core**. The value `n_s` therefore requires an EXTERNAL
selector (Planck-comparison passport) — it is not a present-core theorem. This is closed-negative, NOT a
performative gap: any single `n_s` claim would have to privilege one admissible smoothing over the others
with no internal forcing.
-/

namespace D0.Cosmology.CMBCanonicalSmoothingMaximalityNoGo

open D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-- **Three admissible smoothing measures give three distinct tilts** (all at `k=1`): flat multiplicity
`A`, low-`λ` `B`, high-`λ` `C` are pairwise distinct. -/
theorem three_admissible_smoothings_distinct_tilt :
    tilt 1 12 10 8 2 ≠ tilt 1 12 5 2 1
      ∧ tilt 1 12 10 8 2 ≠ tilt 1 2 4 8 12
      ∧ tilt 1 12 5 2 1 ≠ tilt 1 2 4 8 12 := by
  refine ⟨?_, ?_, ?_⟩ <;> (unfold tilt; norm_num)

/-- **D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001 (closed-negative).** The tilt (hence `n_s`) is
non-constant across the admissible-smoothing family: three legitimate positive weightings of the spectrum
give three distinct values, and the tilt also varies with `k` (`tilt_varies_with_wavenumber`). No
canonical `(k,u)` is forced by present-core; the `n_s` value needs an external selector. -/
theorem cmb_canonical_smoothing_maximality_nogo :
    (tilt 1 12 10 8 2 ≠ tilt 1 12 5 2 1
      ∧ tilt 1 12 10 8 2 ≠ tilt 1 2 4 8 12
      ∧ tilt 1 12 5 2 1 ≠ tilt 1 2 4 8 12)
    ∧ tilt 1 12 10 8 2 ≠ tilt 2 12 10 8 2 :=
  ⟨three_admissible_smoothings_distinct_tilt, tilt_varies_with_wavenumber⟩

end D0.Cosmology.CMBCanonicalSmoothingMaximalityNoGo
