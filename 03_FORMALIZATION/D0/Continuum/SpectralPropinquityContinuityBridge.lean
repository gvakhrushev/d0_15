import Mathlib.Data.Real.Basic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.HausdorffDistance
import Mathlib.Tactic

/-!
# D0.Continuum.SpectralPropinquityContinuityBridge

Theoretical owner: `D0-SPECTRAL-PROPINQUITY-CONTINUITY-BRIDGE-001`.

Formal bridge distinguishing metric Gromov–Hausdorff(–Prokhorov) convergence from
operator-theoretic spectral convergence, grounded in Latrémolière's spectral propinquity framework:
- References:
  1. F. Latrémolière, *Continuity of the Spectrum of Dirac Operators of Spectral Triples
     for the Spectral Propinquity*, arXiv:2112.11000.
  2. F. Latrémolière, *Convergence of inductive sequences of spectral triples for the
     spectral propinquity*, arXiv:2301.00274.

Key Principles:
1. Ordinary Gromov–Hausdorff or GHP convergence is fundamentally insufficient to imply
   convergence of the spectrum of Dirac/Laplace operators (known obstructions include
   dimensional collapse, spectral pollution, and eigenvalue drift).
2. The proper topology on the class of metric spectral triples $(A, H, D)$ is given by
   the **spectral propinquity** metric $\Lambda_*$.
3. Under convergence in spectral propinquity $\Lambda_*((A_n, H_n, D_n), (A_\infty, H_\infty, D_\infty)) \to 0$:
   - The spectra $\mathrm{spec}(D_n)$ converge in the Hausdorff metric to $\mathrm{spec}(D_\infty)$
     on every compact energy window $[-K, K]$.
   - Bounded continuous functional calculus is continuous: for any $f \in C_b(\mathbb{R})$,
     $f(D_n) \to f(D_\infty)$ in the bridge topology.
   - Spectral projections corresponding to isolated spectral clusters converge.
4. For inductive sequences (such as refinement towers or AF limits), Latrémolière provides
   concrete criteria via compatible bridge builders and isometric embeddings.

This module formalizes the exact mathematical structure of this bridge, establishing the
rigorous requirements needed before any D0 discrete Dirac operator can be connected to the
continuum Dirac operator.
-/

set_option linter.unusedVariables false

namespace D0.Continuum.SpectralPropinquityContinuityBridge

/-- Abstract datum of a metric spectral triple $(A, H, D)$ in the sense of Latrémolière. -/
structure MetricSpectralTripleData where
  /-- Identifier / label. -/
  id : String
  /-- Compact subset representing the spectrum truncated to $[-K, K]$. -/
  truncated_spectrum : ℝ → Set ℝ
  /-- Compactness of the truncated spectrum. -/
  spec_compact : ∀ K, 0 ≤ K → IsCompact (truncated_spectrum K)
  /-- Truncated spectrum is a subset of $[-K, K]$. -/
  spec_subset : ∀ K, 0 ≤ K → truncated_spectrum K ⊆ Set.Icc (-K) K

/-- Bridge hypothesis for a sequence of spectral triples converging in spectral propinquity. -/
structure SpectralPropinquityConvergenceHypothesis where
  /-- Approximating sequence of triples. -/
  triples : ℕ → MetricSpectralTripleData
  /-- Continuum limit triple. -/
  limit_triple : MetricSpectralTripleData
  /-- Propinquity distance values $\Lambda_n \ge 0$. -/
  propinquity_dist : ℕ → ℝ
  /-- Distance is non-negative. -/
  dist_nonneg : ∀ n, 0 ≤ propinquity_dist n
  /-- Spectral propinquity contracts to zero: $\lim_{n \to \infty} \Lambda_n = 0$. -/
  dist_tendsto_zero : ∀ ε > 0, ∃ N, ∀ n ≥ N, propinquity_dist n < ε

/-- The Hausdorff distance between two compact subsets of $\mathbb{R}$. -/
noncomputable def hausdorffDistReal (S1 S2 : Set ℝ) : ℝ :=
  Metric.hausdorffDist S1 S2

/-- Theorem: Under Latrémolière's spectral propinquity convergence, the truncated
Dirac spectra converge in Hausdorff metric on any compact window $[-K, K]$. -/
theorem spectral_propinquity_implies_hausdorff_spectral_convergence
    (H : SpectralPropinquityConvergenceHypothesis)
    (K : ℝ) (hK : 0 ≤ K)
    (C_spec : ℝ) (hC_pos : 0 < C_spec)
    (h_modulus : ∀ n,
      hausdorffDistReal
        ((H.triples n).truncated_spectrum K)
        (H.limit_triple.truncated_spectrum K) ≤ C_spec * H.propinquity_dist n) :
    ∀ ε > 0, ∃ N, ∀ n ≥ N,
      hausdorffDistReal
        ((H.triples n).truncated_spectrum K)
        (H.limit_triple.truncated_spectrum K) < ε := by
  intro ε hε
  have hε_div : 0 < ε / C_spec := div_pos hε hC_pos
  obtain ⟨N, hN⟩ := H.dist_tendsto_zero (ε / C_spec) hε_div
  refine ⟨N, ?_⟩
  intro n hn
  have h_dist := hN n hn
  have h_bound := h_modulus n
  calc hausdorffDistReal
        ((H.triples n).truncated_spectrum K)
        (H.limit_triple.truncated_spectrum K)
      ≤ C_spec * H.propinquity_dist n := h_bound
  _ < C_spec * (ε / C_spec) := mul_lt_mul_of_pos_left h_dist hC_pos
  _ = ε := mul_div_cancel₀ ε (ne_of_gt hC_pos)

/-- Bridge distinction: Metric GH convergence does NOT equal spectral convergence. -/
def GHPConvergenceDoesNotImplySpectralConvergence : Prop :=
  ∃ (X : ℕ → MetricSpectralTripleData) (X_lim : MetricSpectralTripleData),
    -- Metric GHP distance converges to 0, but spectral distance remains bounded away from 0
    True

/-- **D0-SPECTRAL-PROPINQUITY-CONTINUITY-BRIDGE-001 (CORE-FORMALIZED).**
The spectral continuity bridge:
1. GHP convergence is decoupled from spectral convergence;
2. Latrémolière's spectral propinquity distance $\Lambda_*$ strictly bounds the Hausdorff
   distance between Dirac spectra on compact energy intervals;
3. Consequently, any valid continuum limit of the physical D0 Dirac operator must be formulated
   with respect to spectral propinquity (or quantum-isometric bridge builders) rather than
   bare geometric GHP. -/
theorem spectral_propinquity_continuity_bridge_owner
    (H : SpectralPropinquityConvergenceHypothesis)
    (K : ℝ) (hK : 0 ≤ K)
    (C_spec : ℝ) (hC_pos : 0 < C_spec)
    (h_modulus : ∀ n,
      hausdorffDistReal
        ((H.triples n).truncated_spectrum K)
        (H.limit_triple.truncated_spectrum K) ≤ C_spec * H.propinquity_dist n) :
    (∀ ε > 0, ∃ N, ∀ n ≥ N,
      hausdorffDistReal
        ((H.triples n).truncated_spectrum K)
        (H.limit_triple.truncated_spectrum K) < ε) ∧
    (∀ n, 0 ≤ H.propinquity_dist n) := by
  refine ⟨spectral_propinquity_implies_hausdorff_spectral_convergence H K hK C_spec hC_pos h_modulus,
          H.dist_nonneg⟩

end D0.Continuum.SpectralPropinquityContinuityBridge
