import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# D0-V15 Work Package A — Raw zone spectral split (`D0/Integration/V15/RawZone.lean`)

**THE (derived from frozen `D₀`).** On the 3-dimensional row space `ran(A)` of the frozen scene `K(9,11,13)`
the adjacency restricts to the equitable-partition divisor matrix `A_W = !![0,11,13; 9,0,13; 9,11,0]` and the
degree operator to `D_W = diag(24,22,20)` (forced by the partition `(9,11,13)` alone — owner
`D0.Claims.KernelZoneSplit`). The derived operator is the **zone commutator generator** `J = i·[D_W, A_W]`.
Everything below is COMPUTED from these two frozen matrices, not assumed.

## The Hermiticity correction (this is what makes A a genuine `THE`, not a CONDITIONAL)

In the *naive* Euclidean inner product `J` is NOT self-adjoint (`A_W` is label-asymmetric), so its eigen-
idempotents are oblique and convention-dependent — an honest `CONDITIONAL`. The fix is the **canonical
part-size inner product** `⟨x,y⟩_G = xᵀ G y` with `G = diag(9,11,13)`, the equitable-partition cell sizes —
a *frozen* structure of the graph, not an external choice. An operator `T` is `G`-self-adjoint iff `G·T` is
symmetric. Over `ℤ`:

* `G·D_W = diag(216,242,260)` is symmetric ⇒ `D_W` is `G`-self-adjoint (`D_selfadjoint_G`).
* `G·A_W = !![0,99,117; 99,0,143; 117,143,0]` is symmetric (entries `nᵢnⱼ`) ⇒ `A_W` is `G`-self-adjoint
  (`A_selfadjoint_G`).
* `G·[D_W,A_W] = !![0,198,468; -198,0,286; -468,-286,0]` is antisymmetric ⇒ `[D_W,A_W]` is `G`-skew, hence
  `J = i·[D_W,A_W]` is genuinely **`G`-Hermitian** (`comm_skew_G`).

Consequently the spectral idempotents are genuine **`G`-orthogonal** projectors (`Pact_orthogonal_G`,
`P0_orthogonal_G`), and the `A_W`-vs-`A_Wᵀ` convention dependence vanishes (both symmetrize to `nᵢnⱼ`).

## Spectrum and split (computed)

* `comm³ = −2840·comm`  (`zone_annihilator`): char. polynomial of `[D_W,A_W]` is `t³ + 2840 t`, so
  `J = i·comm` satisfies `J³ = 2840·J`, spectrum exactly `{0, ±2√710}` (`2840 = 4·710`).
* `R_zone = J² = −comm²`; `P_act = (−1/2840)·comm²`, `P₀ = I + (1/2840)·comm²` are idempotent, complementary
  (`P₀ + P_act = I`), `G`-orthogonal, with `tr P_act = 2` (active sector), `tr P₀ = 1` (neutral sector). The
  integer vector `(143, −234, 99)` spans the neutral sector (`neutral_in_kernel`).

**Negative control** (campaign §11): a diagonal-only adjacency makes `comm = 0`
(`diagonal_only_current_vanishes`) — the split is genuinely sourced by the off-diagonal part-couplings.

**FIREWALL** (campaign A3; `RAW_SELF_READING_OPERATOR_TYPE_FIREWALL.csv`). This is the `G`-orthogonal spectral
decomposition of a frozen-derived operator. It is NOT a physical neutral current, neutrino count, electroweak
charge, or generation count; `J` is neither `QUQ` nor `S_DE`. Any such physical reading needs a separate frozen
selector and is a PROOF-TARGET, not part of this THE.
-/

namespace D0.Integration.V15.RawZone

open Matrix

/-- Degree operator on the 3-dim row space (frozen degrees `24,22,20`). -/
def DW : Matrix (Fin 3) (Fin 3) ℤ := !![24, 0, 0; 0, 22, 0; 0, 0, 20]

/-- Equitable-partition divisor (part-quotient) adjacency on `ran(A)` (frozen part sizes `9,11,13`). -/
def AW : Matrix (Fin 3) (Fin 3) ℤ := !![0, 11, 13; 9, 0, 13; 9, 11, 0]

/-- The zone commutator `[D_W, A_W]` (`J = i·comm`). -/
def comm : Matrix (Fin 3) (Fin 3) ℤ := DW * AW - AW * DW

/-- Canonical part-size inner product weight `G = diag(9,11,13)` (frozen equitable-partition cell sizes). -/
def G : Matrix (Fin 3) (Fin 3) ℤ := !![9, 0, 0; 0, 11, 0; 0, 0, 13]

/-- `[D_W, A_W]` evaluates to the explicit integer matrix. -/
theorem comm_eq : comm = !![0, 22, 52; -18, 0, 26; -36, -22, 0] := by
  native_decide

/-! ### Hermiticity in the canonical part-size inner product `G` (the correction) -/

/-- `D_W` is self-adjoint w.r.t. `G`: `G·D_W` is symmetric. -/
theorem D_selfadjoint_G : (G * DW)ᵀ = G * DW := by native_decide

/-- `A_W` is self-adjoint w.r.t. `G`: `G·A_W` is symmetric (entries `nᵢnⱼ`). -/
theorem A_selfadjoint_G : (G * AW)ᵀ = G * AW := by native_decide

/-- `[D_W,A_W]` is skew-adjoint w.r.t. `G`: `G·comm` is antisymmetric. Hence `J = i·comm` is `G`-Hermitian. -/
theorem comm_skew_G : (G * comm)ᵀ = -(G * comm) := by native_decide

/-! ### Spectrum / annihilator -/

/-- **Annihilating polynomial.** `comm³ = −2840·comm`; char. polynomial of `[D_W,A_W]` is `t³ + 2840 t`.
Equivalently `J = i·comm` satisfies `J³ = 2840·J`, spectrum `{0, ±2√710}`. -/
theorem zone_annihilator : comm * comm * comm = (-2840 : ℤ) • comm := by
  native_decide

/-- The zone generator is nonzero: the active sector is non-trivial. -/
theorem comm_ne_zero : comm ≠ 0 := by
  native_decide

/-- The integer vector `(143, −234, 99)` lies in the neutral sector `ker(comm)`. -/
theorem neutral_in_kernel : comm.mulVec ![143, -234, 99] = 0 := by
  native_decide

/-- Negative control (§11): a diagonal-only adjacency kills the generator. -/
theorem diagonal_only_current_vanishes :
    DW * (!![1, 0, 0; 0, 2, 0; 0, 0, 3] : Matrix (Fin 3) (Fin 3) ℤ)
      - (!![1, 0, 0; 0, 2, 0; 0, 0, 3] : Matrix (Fin 3) (Fin 3) ℤ) * DW = 0 := by
  native_decide

/-! ### `G`-orthogonal spectral projectors over `ℚ` -/

/-- Canonical weight over `ℚ`. -/
def Gq : Matrix (Fin 3) (Fin 3) ℚ := !![9, 0, 0; 0, 11, 0; 0, 0, 13]

/-- Active-sector projector `P_act = (−1/2840)·comm²`. -/
def Pact : Matrix (Fin 3) (Fin 3) ℚ :=
  !![567/710, 143/355, -143/710; 117/355, 121/355, 117/355; -99/710, 99/355, 611/710]

/-- Neutral-sector projector `P₀ = I + (1/2840)·comm²`. -/
def P0 : Matrix (Fin 3) (Fin 3) ℚ :=
  !![143/710, -143/355, 143/710; -117/355, 234/355, -117/355; 99/710, -99/355, 99/710]

theorem Pact_idempotent : Pact * Pact = Pact := by native_decide
theorem P0_idempotent : P0 * P0 = P0 := by native_decide

/-- Complementary: `P₀ + P_act = I`. -/
theorem split_complete : P0 + Pact = (1 : Matrix (Fin 3) (Fin 3) ℚ) := by native_decide

/-- `P_act` is a genuine `G`-orthogonal projector: `G·P_act` is symmetric. -/
theorem Pact_orthogonal_G : (Gq * Pact)ᵀ = Gq * Pact := by native_decide

/-- `P₀` is a genuine `G`-orthogonal projector: `G·P₀` is symmetric. -/
theorem P0_orthogonal_G : (Gq * P0)ᵀ = Gq * P0 := by native_decide

/-- Active sector dimension `tr P_act = 2`. -/
theorem active_dim : Pact.trace = 2 := by native_decide
/-- Neutral sector dimension `tr P₀ = 1`. -/
theorem neutral_dim : P0.trace = 1 := by native_decide

/-- **D0-ZONE-CURRENT-001 + D0-ZONE-NEUTRAL-ACTIVE-SPLIT-001 (THE).** The frozen zone commutator generator
`J = i[D_W,A_W]` is `G`-Hermitian in the canonical part-size inner product `G = diag(9,11,13)`, has annihilating
polynomial `t³ + 2840 t` (spectrum `{0, ±2√710}`), and induces a genuine `G`-orthogonal spectral split of the
3-dim row space into a 1-dim neutral sector and a 2-dim active sector — all computed from the frozen `D_W, A_W`.
(Firewall: no physical neutral-current/charge/generation reading.) -/
theorem zone_current_spine :
    comm = !![0, 22, 52; -18, 0, 26; -36, -22, 0] ∧
    (G * comm)ᵀ = -(G * comm) ∧                       -- J = i·comm is G-Hermitian
    comm * comm * comm = (-2840 : ℤ) • comm ∧          -- spectrum {0, ±2√710}
    comm ≠ 0 ∧
    comm.mulVec ![143, -234, 99] = 0 ∧
    P0 + Pact = (1 : Matrix (Fin 3) (Fin 3) ℚ) ∧
    Pact * Pact = Pact ∧ P0 * P0 = P0 ∧
    (Gq * Pact)ᵀ = Gq * Pact ∧ (Gq * P0)ᵀ = Gq * P0 ∧  -- genuine G-orthogonal projectors
    Pact.trace = 2 ∧ P0.trace = 1 :=
  ⟨comm_eq, comm_skew_G, zone_annihilator, comm_ne_zero, neutral_in_kernel,
    split_complete, Pact_idempotent, P0_idempotent, Pact_orthogonal_G, P0_orthogonal_G,
    active_dim, neutral_dim⟩

end D0.Integration.V15.RawZone
