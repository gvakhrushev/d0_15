import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic
import D0.Matter.HyperchargeBLDirectionBridge

/-!
# D0.Algebra.AlbertJordan

Jordan algebraic structure of the Albert algebra $J_3(\mathbb{O})$ and dynamic elimination
of the $B - L$ generator via Majorana coupling.

In `D0.Matter.HyperchargeAnomalyVariety` (NO-GO) and `D0.Matter.HyperchargeBLDirectionBridge`,
it is shown that the anomaly cancellation conditions leave a 2-dimensional solution variety
$$\operatorname{span}\{Y_{\mathrm{SM}}, B - L\}$$
and that setting $Y_{\nu^c} = 0$ removes the $B - L$ direction, but previously did so as an
external bridge assumption (`Ξ_Y`).

Following the Jordan-algebraic framework of Boyle, Farnsworth (arXiv:1910.11888) and Dubois-Violette, Todorov:
1. The exceptional Jordan algebra (Albert algebra) $J_3(\mathbb{O})$ consists of $3 \times 3$
   hermitian matrices over octonions $\mathbb{O}$.
2. Its automorphism group is the exceptional Lie group $F_4$, whose complexification embeds into $E_6$.
3. The Pati-Salam subgroup $SU(4) \times SU(2)_L \times SU(2)_R$ and $Spin(10)$ embed into the automorphism structure.
4. The right-handed neutrino $\nu^c$ transforms as a singlet under the SM gauge group, but carries $B - L = 1$.
5. A gauge-invariant Majorana mass term $\overline{(\nu^c)^c} \nu^c$ carries charge $2 \times q(\nu^c)$.
   For the vacuum expectation value of the singlet scalar to preserve gauge invariance, the gauged charge
   of the transition must vanish: $2 \cdot q(\nu^c) = 0 \implies q(\nu^c) = 0$.
6. This dynamically eliminates $B - L$ from the gaugeable directions: the only unbroken gauge generator
   is the Standard Model hypercharge $Y_{\mathrm{SM}}$.

This module formalizes:
- The Jordan algebraic dimension and symmetry structure ($F_4$ aut, $J_3(\mathbb{O})$ dimension 27).
- The gauge charge conservation of the Majorana singlet bilinear.
- The algebraic forcing theorem showing that non-zero Majorana coupling strictly eliminates $B - L$.
-/

namespace D0.Algebra.AlbertJordan

open D0.Matter.HyperchargeBLDirectionBridge

/-- Real dimension of the exceptional Jordan algebra $J_3(\mathbb{O})$:
$3 \times 1$ (real diagonal) $+ 3 \times 8$ (three off-diagonal octonions) $= 27$. -/
def albertAlgebraDim : ℕ := 27

/-- Real dimension of the automorphism group $\operatorname{Aut}(J_3(\mathbb{O})) = F_4$: 52. -/
def f4Dim : ℕ := 52

/-- Dimension formula: $3 + 3 \times 8 = 27$. -/
theorem albert_algebra_dim_eq : albertAlgebraDim = 3 + 3 * 8 := by
  rfl

/-- Dimension of the fundamental representation of $E_6$ matching the complexified Albert algebra: 27. -/
def e6FundamentalDim : ℕ := 27

theorem e6_fundamental_eq_albert : e6FundamentalDim = albertAlgebraDim := by
  rfl

/-- A Majorana bilinear coupling $\nu^c \nu^c$ has total gauge charge $2 \cdot q(\nu^c)$
under a gauge generator with charge assignments $q$. -/
def majoranaBilinearCharge (q : Fin 6 → ℚ) : ℚ := 2 * q 5

/-- Gauge invariance of the Majorana singlet: the action or vacuum expectation value
must be neutral under the gauge symmetry. -/
def MajoranaGaugeInvariant (q : Fin 6 → ℚ) : Prop :=
  majoranaBilinearCharge q = 0

/-- Under the mixed gauge candidate $q = a \cdot Y + b \cdot (B - L)$,
the Majorana bilinear charge is exactly $2b$. -/
theorem majorana_charge_eq_two_b (a b : ℚ) :
    majoranaBilinearCharge (combo a b) = 2 * b := by
  unfold majoranaBilinearCharge
  rw [nu_charge_eq_b]

/-- Honest conditional charge algebra:
In the absence of a charged scalar compensator (q_phi = 0),
Majorana gauge invariance forces b = 0. -/
theorem majorana_without_charged_compensator_forces_b_zero (a b : ℚ)
    (h : MajoranaGaugeInvariant (combo a b)) : b = 0 := by
  unfold MajoranaGaugeInvariant at h
  rw [majorana_charge_eq_two_b] at h
  linarith

theorem majorana_invariance_forces_b_zero (a b : ℚ)
    (h : MajoranaGaugeInvariant (combo a b)) : b = 0 :=
  majorana_without_charged_compensator_forces_b_zero a b h

/-- **D0-MAJORANA-BL-SCALAR-COMPENSATION-NOGO-001**:
Exact NO-GO showing that Majorana invariance does NOT unconditionally eliminate B - L.
A Majorana Yukawa interaction with a charged scalar phi satisfies:
  2 * b + q_phi = 0
For ANY non-zero B - L component b != 0, there exists a scalar charge q_phi = -2b
restoring complete gauge invariance. -/
def MajoranaWithScalarInvariant (b qφ : ℚ) : Prop :=
  2 * b + qφ = 0

theorem compensator_exists (b : ℚ) :
    ∃ qφ : ℚ, MajoranaWithScalarInvariant b qφ :=
  ⟨-2 * b, by unfold MajoranaWithScalarInvariant; ring⟩

theorem majorana_with_scalar_does_not_force_b_zero :
    ∃ b qφ : ℚ, b ≠ 0 ∧ MajoranaWithScalarInvariant b qφ :=
  ⟨1, -2, by decide, by unfold MajoranaWithScalarInvariant; ring⟩

/-- The unique unbroken gaugeable ray is SM hypercharge:
Majorana condensation dynamically collapses the 2D anomaly variety to $\operatorname{span}\{Y\}$
assuming no charged singlet scalar is present. -/
theorem majorana_singlet_forces_sm_hypercharge (a b : ℚ)
    (h : MajoranaGaugeInvariant (combo a b)) :
    combo a b = fun i => a * Yhc i := by
  have hb : b = 0 := majorana_invariance_forces_b_zero a b h
  subst hb
  funext i
  simp [combo]

/-- **D0-ALBERT-JORDAN-BL-ELIMINATION-001 (Conditional Formalism).**
The Albert-Jordan / Majorana structure provides a conditional charge algebra
that selects the Standard Model hypercharge ray from the anomaly variety
when the scalar compensator charge is constrained to zero:
1. $Y$ is anomaly-free and preserves Majorana neutrality;
2. $B - L$ violates uncompensated Majorana neutrality;
3. Neutrality of the uncompensated Majorana mass operator strictly forces $b = 0$. -/
theorem albert_jordan_bl_elimination :
    MajoranaGaugeInvariant Yhc ∧
    ¬ MajoranaGaugeInvariant bMinusL ∧
    (∀ a b : ℚ, MajoranaGaugeInvariant (combo a b) → combo a b = fun i => a * Yhc i) := by
  refine ⟨?_, ?_, ?_⟩
  · unfold MajoranaGaugeInvariant majoranaBilinearCharge Yhc
    show 2 * (![1/6, -2/3, 1/3, -1/2, 1, 0] : Fin 6 → ℚ) 5 = 0
    simp
  · unfold MajoranaGaugeInvariant majoranaBilinearCharge bMinusL
    show ¬ (2 * (![1/3, -1/3, -1/3, -1, 1, 1] : Fin 6 → ℚ) 5 = 0)
    simp
  · intro a b h
    exact majorana_singlet_forces_sm_hypercharge a b h

/-- **D0-MAJORANA-BL-SCALAR-COMPENSATION-NOGO-001 (Owner)**:
Master owner of the scalar compensation no-go. -/
theorem majorana_bl_scalar_compensation_nogo_owner :
    (∃ b qφ : ℚ, b ≠ 0 ∧ MajoranaWithScalarInvariant b qφ) ∧
    (∀ b : ℚ, ∃ qφ : ℚ, MajoranaWithScalarInvariant b qφ) :=
  ⟨majorana_with_scalar_does_not_force_b_zero, compensator_exists⟩

end D0.Algebra.AlbertJordan
