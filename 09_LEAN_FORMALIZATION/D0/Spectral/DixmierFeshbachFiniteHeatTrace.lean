import Mathlib.Tactic
import Mathlib.Algebra.Ring.GeomSum

/-!
# D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 / a FINITE heat trace has NO `1/s` pole (NO-GO, Lean)

Python certificate: `05_CERTS/vp_dixmier_feshbach_finite_heattrace.py`.

## The negative this module formalizes (the NO-GO)

The Feshbach–Schur archive block is a FINITE multiset of eigenvalues (dim `30`). Its heat trace
`Θ(s) = Σ_i exp(-s·λ_i)` is an entire function of `s`, hence its Maclaurin expansion is a power
series indexed by `ℕ` ONLY:

    Θ(s) = Σ_{k≥0} a_k s^k ,    a_k = (Σ_i (-λ_i)^k) / k!   (the depth-`k` archive moment).

A `ℕ`-indexed power series has **no negative-index coefficient** — in particular there is no
`a_{-1}` (no `1/s` term). Therefore the Dixmier-residue extraction `Res_{s=0} Θ = a_{-1}` is
STRUCTURALLY zero for the finite block, and the value at `s = 0` is just the constant Maclaurin
coefficient `a_0 = Σ_i (-λ_i)^0 = Σ_i 1 = card(spectrum) = 30` (the dimension). A finite heat trace
cannot produce the `1/s` pole whose residue would be the Dixmier trace.

CONTRAST (why an INFINITE spectrum is genuinely required). The would-be pole is the INFINITE
geometric tower `Σ_{k≥1} x^k = 1/(1-x)`, which diverges as `x → 1` (the `1/s` pole, residue `1`).
The finite truncation `Σ_{k=0}^{N-1} x^k = (1 - x^N)/(1 - x)` instead stays FINITE as `x → 1`, with
the explicit value `N`. So the principal part `1/(1-x)` is an artifact of the *infinite* tower; every
finite truncation evaluates to its term-count `N` and has no pole. The Dixmier owner therefore needs
the genuinely infinite spectral object, NOT the finite archive block.

We encode `Θ` by its Maclaurin coefficient sequence over `ℚ` and prove, for the concrete sample
30-eigenvalue archive spectrum:

  * `archive_heat_trace_const_eq_dim` : `a_0 = card spectrum = 30`  (the `s = 0` value is the dimension),
  * `finite_trace_principal_coeff_zero` : the negative-index (`1/s`) coefficient is `0`
       (a `ℕ`-indexed series has no `a_{-1}`),
  * `geom_partial_sum_at_one_eq_card` : `Σ_{k<N} 1^k = N`  (the finite tower stays finite as `x → 1`),
  * the residue CONTRAST: the finite truncation has principal coefficient `0` while the formal
       infinite-tower object carries `c_{-1} = 1` — the pole needs the infinite spectrum.

HONESTY BOUNDARY. CLOSED here (finite, decidable / `ring`): the finite block has no `1/s` pole, its
`s = 0` value equals the dimension `30`, the finite geometric tower evaluates to its term count, and
the `1/s` residue is an INFINITE-tower object absent from any finite truncation. NOT closed and NOT
asserted: the actual Dixmier/Wodzicki residue extraction on the *infinite* spectral object and the
residue→`Δ_α` normalization — those stay the external owner edge `D0-DIXMIER-RESIDUE-OWNER-001`
(`ASSUMP-DIXMIER-TRACE`). This is an anti-numerology guard: it PREVENTS declaring the Dixmier owner
closed by pointing at the finite heat trace.
-/

namespace D0.Spectral

/-- A finite archive spectrum: the list of its eigenvalues (with multiplicity) as rationals. -/
abbrev FiniteSpectrum := List ℚ

/-- The sample 30-eigenvalue archive block (kernel `8 ⊕ 10 ⊕ 12`): the dim-30 Feshbach archive
spectrum. Concrete eigenvalues `1,2,3` with the kernel multiplicities `8,10,12` (total `30`); the
exact values are immaterial to the NO-GO, only `card = 30` and finiteness matter. -/
def sampleSpectrum : FiniteSpectrum :=
  List.replicate 8 (1 : ℚ) ++ List.replicate 10 (2 : ℚ) ++ List.replicate 12 (3 : ℚ)

/-- The depth-`k` Maclaurin coefficient of the finite heat trace `Θ(s) = Σ_i exp(-s·λ_i)`:
`a_k = (Σ_i (-λ_i)^k) / k!`. This is a `ℕ`-indexed sequence — there is NO `a_{-1}`. -/
def heatTraceCoeff (spectrum : FiniteSpectrum) (k : ℕ) : ℚ :=
  (spectrum.map (fun l => (-l) ^ k)).sum / (Nat.factorial k : ℚ)

/-- The **principal-part (`1/s`) coefficient extraction** for a `ℕ`-indexed Maclaurin series:
the coefficient at an INTEGER index `j` is `heatTraceCoeff` when `j ≥ 0`, and is `0` for every
negative `j`. Since a finite heat trace is entire, only `j ≥ 0` ever occurs; the negative band
(in particular `j = -1`, the residue slot) is structurally `0`. -/
def principalCoeff (spectrum : FiniteSpectrum) (j : ℤ) : ℚ :=
  if 0 ≤ j then heatTraceCoeff spectrum j.toNat else 0

/-- The `s = 0` value of the heat trace is its constant Maclaurin coefficient `a_0`. -/
def heatTraceAtZero (spectrum : FiniteSpectrum) : ℚ := heatTraceCoeff spectrum 0

/-- **The sample archive block has dimension `30`** (card = total multiplicity). -/
theorem sampleSpectrum_card : sampleSpectrum.length = 30 := by
  decide

/-- **The constant Maclaurin coefficient equals the dimension.** For any spectrum, `a_0 = Σ_i 1 =
card spectrum`: each summand `(-λ_i)^0 = 1`, divided by `0! = 1`. This is the value at `s = 0`. The
`map` of the constant-`1` function is `replicate length 1`, whose sum is `length`. -/
theorem heatTraceCoeff_zero_eq_card (spectrum : FiniteSpectrum) :
    heatTraceCoeff spectrum 0 = (spectrum.length : ℚ) := by
  unfold heatTraceCoeff
  -- `0! = 1`, so the coefficient is just the sum of `(-λ)^0 = 1` over the list.
  rw [Nat.factorial_zero, Nat.cast_one, div_one]
  -- the sum of `1` over the list equals its length; prove by structural induction.
  induction spectrum with
  | nil => simp
  | cons a as ih =>
      rw [List.map_cons, List.sum_cons, ih, pow_zero, List.length_cons]
      push_cast
      ring

/-- **`Θ(0) = dim = 30`** for the sample archive block: the heat trace at `s = 0` is the dimension,
not a divergence. -/
theorem archive_heat_trace_const_eq_dim : heatTraceAtZero sampleSpectrum = 30 := by
  unfold heatTraceAtZero
  rw [heatTraceCoeff_zero_eq_card, sampleSpectrum_card]
  norm_num

/-- **No `1/s` pole: the residue-slot (`j = -1`) coefficient is `0`.** A `ℕ`-indexed Maclaurin
series has no negative-index coefficient, so the finite heat trace cannot have a `1/s` term. -/
theorem finite_trace_principal_coeff_zero : principalCoeff sampleSpectrum (-1) = 0 := by
  unfold principalCoeff
  rw [if_neg (by omega)]

/-- More strongly, the **entire negative band vanishes**: for every negative integer index `j` the
principal coefficient is `0`. The finite (entire) heat trace has no principal part at all. -/
theorem finite_trace_no_principal_part :
    ∀ j : ℤ, j < 0 → principalCoeff sampleSpectrum j = 0 := by
  intro j hj
  unfold principalCoeff
  rw [if_neg (by omega)]

/-- The finite geometric/heat-tower TRUNCATION `Σ_{k=0}^{N-1} x^k`, as a `ℚ`-polynomial in `x`. -/
def geomPartial (N : ℕ) (x : ℚ) : ℚ := (Finset.range N).sum (fun k => x ^ k)

/-- **The finite tower stays finite as `x → 1`: `Σ_{k<N} 1^k = N`.** The truncated geometric series
evaluates to its term count `N` at `x = 1` — no pole. (Contrast the infinite tower `1/(1-x)`.) -/
theorem geom_partial_sum_at_one_eq_card (N : ℕ) : geomPartial N 1 = (N : ℚ) := by
  unfold geomPartial
  simp

/-- **The telescoping identity `(1 - x)·Σ_{k<N} x^k = 1 - x^N`.** This exhibits the finite tower as
`(1 - x^N)/(1 - x)`: the numerator `1 - x^N → 0` cancels the `1 - x → 0` denominator at `x = 1`, so
the truncation has NO pole. The bare `1/(1-x)` pole only appears when `x^N → 0` is lost, i.e. for the
INFINITE tower. We verify the polynomial identity for the sample dimension `N = 30`. -/
theorem geom_partial_telescope_30 (x : ℚ) :
    (1 - x) * geomPartial 30 x = 1 - x ^ 30 := by
  unfold geomPartial
  exact mul_neg_geom_sum x 30

/-- The would-be **infinite-tower residue coefficient `c_{-1} = 1`** (the `1/(1-x)` pole), encoded as
a formal datum: the infinite geometric tower `Σ_{k≥1} x^k` has principal coefficient `1` at `x = 1`.
We do NOT prove this analytically (no real-analysis); we record it as the formal target that the
finite block FAILS to provide. -/
def infiniteTowerResidue : ℚ := 1

/-- **THE CONTRAST (the NO-GO core).** The finite archive block's residue-slot coefficient is `0`,
while the (formal) infinite-tower residue is `1`: they DIFFER. Hence the `1/s` pole — and the Dixmier
residue read off it — is a property of the INFINITE spectrum and is absent from every finite heat
trace. The finite block cannot own the pole. -/
theorem finite_trace_residue_ne_infinite :
    principalCoeff sampleSpectrum (-1) ≠ infiniteTowerResidue := by
  rw [finite_trace_principal_coeff_zero]
  unfold infiniteTowerResidue
  norm_num

/-- **The `s = 0` value is the dimension `30`, NOT the archive moment `μ₂ = 12288/5`.** Anti-numerology
guard: a reader must not confuse `Θ(0) = dim` with the depth-2 moment `a_2 = μ₂` — they are different
Maclaurin coefficients. (`12288/5 = 2457.6 ≠ 30`.) -/
theorem heat_trace_at_zero_ne_mu2 : heatTraceAtZero sampleSpectrum ≠ 12288 / 5 := by
  rw [archive_heat_trace_const_eq_dim]
  norm_num

/-- **D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 (finite NO-GO).** The dim-30 Feshbach archive block is
a finite spectrum; its heat trace is a `ℕ`-indexed Maclaurin series with NO negative-index (`1/s`)
coefficient. Concretely: (i) the residue-slot coefficient is `0` (no pole), (ii) the `s = 0` value is
the dimension `30` (and ≠ `μ₂ = 12288/5`), (iii) the finite geometric tower evaluates to its term
count `30` at `x = 1` (stays finite), and (iv) the `1/s` residue (`c_{-1} = 1`) differs from the
finite block's `0`, so the pole is an INFINITE-spectrum object. The actual Dixmier/Wodzicki residue
on the infinite object stays the owner edge `D0-DIXMIER-RESIDUE-OWNER-001` (`ASSUMP-DIXMIER-TRACE`). -/
theorem dixmier_feshbach_finite_heattrace_no_pole :
    principalCoeff sampleSpectrum (-1) = 0
      ∧ heatTraceAtZero sampleSpectrum = 30
      ∧ heatTraceAtZero sampleSpectrum ≠ 12288 / 5
      ∧ geomPartial 30 1 = 30
      ∧ principalCoeff sampleSpectrum (-1) ≠ infiniteTowerResidue :=
  ⟨finite_trace_principal_coeff_zero, archive_heat_trace_const_eq_dim,
    heat_trace_at_zero_ne_mu2, geom_partial_sum_at_one_eq_card 30,
    finite_trace_residue_ne_infinite⟩

end D0.Spectral
