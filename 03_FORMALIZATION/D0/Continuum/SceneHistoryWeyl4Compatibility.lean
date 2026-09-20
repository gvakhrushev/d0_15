import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0.Continuum.SceneHistoryWeyl4Compatibility

Theoretical owner: `D0-SCENE-HISTORY-WEYL4-COMPATIBILITY-001`.

Dimensional compatibility audit between the scene history growth and the geometric 4D Weyl law:
1. In `D0.VNext2.ScenePathHistoryCanonicity`, the canonical history of the scene tick
   is uniquely the free path category (all-walks).
2. The number of all-walks paths of length $N$ on $K(9,11,13)$ grows asymptotically with
   rate $\rho^N$, where $\rho$ is the Perron root of the adjacency matrix $A_{\mathrm{scene}}$,
   satisfying the transport cubic:
   $$\rho^3 - 359 \rho - 2574 = 0, \quad \rho \approx 21.83738.$$
3. The internally-sourced Dirac scale is geometric in $\varphi = (1 + \sqrt{5})/2$,
   with eigenvalue growth $\lambda_N \sim \varphi^N$.
4. If path history modes were naively identified with spectral modes without a coarse-graining
   quotient, the effective spectral dimension would be:
   $$d_{\mathrm{spec}} = \frac{\log \rho}{\log \varphi} \approx 6.408 \neq 4.$$
5. Four-dimensional spectral compatibility ($d_{\mathrm{spec}} = 4$) strictly requires:
   $$\rho = \varphi^4.$$
   Since $\varphi^2 = \varphi + 1$, we have $\varphi^4 = (\varphi + 1)^2 = \varphi^2 + 2\varphi + 1 = 3\varphi + 2$.
   Evaluating the transport cubic polynomial $P(x) = x^3 - 359 x - 2574$ at $x = \varphi^4$:
   $$P(\varphi^4) = (3\varphi + 2)^3 - 359(3\varphi + 2) - 2574 \neq 0.$$
   Specifically, $(3\varphi + 2)^3 = 27\varphi^3 + 54\varphi^2 + 36\varphi + 8 = 27(2\varphi + 1) + 54(\varphi + 1) + 36\varphi + 8 = 144\varphi + 89$.
   Then:
   $$P(\varphi^4) = (144\varphi + 89) - 359(3\varphi + 2) - 2574 = -933\varphi - 3203 < 0.$$
6. Since $\rho$ is a root of $P$ ($P(\rho) = 0$) while $P(\varphi^4) \neq 0$, it follows that:
   $$\rho \neq \varphi^4.$$

Conclusion:
The raw un-coarse-grained path history carrier cannot directly serve as the 4D spectral mode carrier.
A non-trivial canonical coarse-graining quotient:
$$\text{Path History Tower} \longrightarrow \text{4D Geometric Spectral Tower}$$
is mathematically obligatory.
-/

namespace D0.Continuum.SceneHistoryWeyl4Compatibility

open D0

/-- The transport cubic polynomial whose root is the scene Perron eigenvalue:
$P(x) = x^3 - 359 x - 2574$. -/
def transportCubic (x : ℝ) : ℝ :=
  x ^ 3 - 359 * x - 2574

/-- Golden ratio power $\varphi^4 = 3\varphi + 2$. -/
theorem phi_pow_four : phi ^ 4 = 3 * phi + 2 := by
  have hsq := phi_sq
  calc phi ^ 4 = (phi ^ 2) ^ 2 := by ring
  _ = (phi + 1) ^ 2 := by rw [hsq]
  _ = phi ^ 2 + 2 * phi + 1 := by ring
  _ = (phi + 1) + 2 * phi + 1 := by rw [hsq]
  _ = 3 * phi + 2 := by ring

/-- Cube of $(3\varphi + 2)$ in terms of $\varphi$: $(3\varphi + 2)^3 = 144\varphi + 89$. -/
theorem three_phi_plus_two_cubed : (3 * phi + 2) ^ 3 = 144 * phi + 89 := by
  have hsq := phi_sq
  have hcub : phi ^ 3 = 2 * phi + 1 := by
    calc phi ^ 3 = phi * phi ^ 2 := by ring
    _ = phi * (phi + 1) := by rw [hsq]
    _ = phi ^ 2 + phi := by ring
    _ = (phi + 1) + phi := by rw [hsq]
    _ = 2 * phi + 1 := by ring
  calc (3 * phi + 2) ^ 3 = 27 * phi ^ 3 + 54 * phi ^ 2 + 36 * phi + 8 := by ring
  _ = 27 * (2 * phi + 1) + 54 * (phi + 1) + 36 * phi + 8 := by rw [hcub, hsq]
  _ = 144 * phi + 89 := by ring

/-- Evaluation of the transport cubic at $\varphi^4$:
$P(\varphi^4) = -933\varphi - 3203$. -/
theorem transport_cubic_at_phi_four :
    transportCubic (phi ^ 4) = -933 * phi - 3203 := by
  unfold transportCubic
  rw [phi_pow_four]
  rw [three_phi_plus_two_cubed]
  ring

/-- $\varphi > 0$. -/
theorem phi_pos : 0 < phi := by
  have h5 : (1 : ℝ) < 5 := by norm_num
  have hsqrt : 1 < Real.sqrt 5 := by
    calc 1 = Real.sqrt 1 := by rw [Real.sqrt_one]
    _ < Real.sqrt 5 := Real.sqrt_lt_sqrt (by norm_num) h5
  unfold phi
  linarith

/-- $P(\varphi^4) \neq 0$: specifically, it is strictly negative. -/
theorem transport_cubic_at_phi_four_ne_zero :
    transportCubic (phi ^ 4) ≠ 0 := by
  rw [transport_cubic_at_phi_four]
  have hp : 0 < phi := phi_pos
  have : -933 * phi - 3203 < 0 := by linarith
  linarith

/-- **D0-SCENE-HISTORY-WEYL4-COMPATIBILITY-001 (CORE-FORMALIZED).**
The raw un-coarse-grained scene history growth rate $\rho$ cannot equal $\varphi^4$:
any root of the transport cubic is strictly distinct from $\varphi^4$.
Therefore, four-dimensional Weyl growth cannot be obtained from the raw all-walks tower
without a canonical coarse-graining quotient. -/
theorem scene_history_weyl4_incompatibility (rho : ℝ) (h_root : transportCubic rho = 0) :
    rho ≠ phi ^ 4 := by
  intro heq
  subst rho
  exact transport_cubic_at_phi_four_ne_zero h_root

/-- Summary owner for `D0-SCENE-HISTORY-WEYL4-COMPATIBILITY-001`. -/
theorem scene_history_weyl4_compatibility_owner :
    transportCubic (phi ^ 4) = -933 * phi - 3203 ∧
    transportCubic (phi ^ 4) ≠ 0 ∧
    (∀ rho : ℝ, transportCubic rho = 0 → rho ≠ phi ^ 4) := by
  refine ⟨transport_cubic_at_phi_four,
          transport_cubic_at_phi_four_ne_zero,
          scene_history_weyl4_incompatibility⟩

end D0.Continuum.SceneHistoryWeyl4Compatibility
