import Mathlib.Tactic

/-!
# D0-CMB-NS-LAPLACIAN-IDS-OWNER-001 / IDS staircase + power proxy P(k); spectrum-alone does NOT fix n_s (Lean)

Python certificate: `05_CERTS/vp_cmb_ns_laplacian_ids.py`.

Companion to `D0.Cosmology.ReheatingHeatTraceJump` (the heat-trace JUMP owner). We reuse the SAME finite
object: the EXACT graph-Laplacian spectrum of the connected reheating scene `K(9,11,13)` (33 vertices),

    { 0 : mult 1, 20 : mult 12, 22 : mult 10, 24 : mult 8, 33 : mult 2 }

(complete-tripartite formula; total multiplicity 33; algebraic connectivity `λ₂ = 20`).

Verified mathematics (encoded, not assumed).

* The **integrated density of states (IDS)** staircase `N(λ) = (1/33)·Σ_{λ_i ≤ λ} mult_i` evaluated at the
  jump points `0 < 20 < 22 < 24 < 33` takes the EXACT rationals

      [ 1/33, 13/33, 23/33, 31/33, 1 ]

  (cumulative multiplicities `1, 13, 23, 31, 33` divided by the total `33`). This is decidable from the
  finite spectrum.

* The dimensionless **power proxy** `P(k) = Σ_i mult_i / (k² + λ_i)` is an exact rational at each rational
  `k`. We pin `P(1) = 163196/68425` and `P(2) = 19857/13468`.

* The discrete **tilt proxy** `n_s − 1 := (k/P(k))·P'(k)` with `P'(k) = Σ_i mult_i·(−2k)/(k²+λ_i)²` takes
  GENUINELY DIFFERENT exact rational values at two sample points `k = 1` and `k = 2`:

      (n_s − 1)(1) = −29795504237 / 33500058900 ≠ −119488232 / 200575557 = (n_s − 1)(2).

  Because the proxy varies with the (otherwise free) evaluation point `k`, **the bare Laplacian spectrum
  alone does NOT determine a single scalar `n_s`** — a finite NO-GO. No CMB datum, no Planck `n_s`, no
  inflaton enters; we do NOT assert any `n_s` value.

HONESTY BOUNDARY. CERT-CLOSED here: the spectrum facts (total `33`, `λ₂ = 20`), the IDS staircase
rationals, the exact `P(k)` at the two sample `k`, and the spectrum-alone NO-GO (two evaluation points →
two different tilt-proxy values). What stays PROOF-TARGET: a canonical internally-forced smoothing
functional / evaluation rule fixing the pair `(k, u)` so that `n_s` becomes a single determined value
(`D0-CMB-IDS-SMOOTHING-OWNER-001`); and the spectral map `n_s = f({λ_i})` itself
(`D0-CMB-PHASON-SPECTRUM-OWNER-001`). Both are absent.
-/

namespace D0.Cosmology.CMBLaplacianIDS

/-- A finite Laplacian spectrum: a list of `(eigenvalue, multiplicity)` pairs. Mirrors the sibling
`D0.Cosmology.ReheatingHeatTraceJump.Spectrum`. -/
abbrev IDSSpectrum := List (Nat × Nat)

/-- The EXACT spectrum of the connected scene `K(9,11,13)` (complete-tripartite formula). Same finite
object as the heat-trace-jump owner. -/
def specK : IDSSpectrum := [(0, 1), (20, 12), (22, 10), (24, 8), (33, 2)]

/-- Total multiplicity = sum of all multiplicities = dimension = vertex count (= 33). -/
def totalMult (s : IDSSpectrum) : Nat := (s.map Prod.snd).sum

/-- Multiplicity of a given eigenvalue: sum of multiplicities of pairs with that eigenvalue. -/
def multOf (s : IDSSpectrum) (lam : Nat) : Nat :=
  ((s.filter (fun p => p.1 == lam)).map Prod.snd).sum

/-- **Total multiplicity is `33`** (= number of vertices = dimension). Reuses the sibling fact. -/
theorem totalMult_specK : totalMult specK = 33 := by decide

/-- **Algebraic connectivity `λ₂ = 20`**: eigenvalue `20` carries multiplicity `12`, and no eigenvalue
strictly between `0` and `20` carries any multiplicity. Reuses the sibling fact. -/
theorem algebraic_connectivity_specK :
    multOf specK 20 = 12
      ∧ (∀ lam, 0 < lam → lam < 20 → multOf specK lam = 0) := by
  refine ⟨by decide, ?_⟩
  intro lam h0 h20
  unfold multOf specK
  interval_cases lam <;> rfl

/-! ## IDS staircase (cumulative multiplicity / total), exact rationals -/

/-- Cumulative multiplicity at threshold `λ`: `Σ_{λ_i ≤ λ} mult_i`. -/
def cumMult (s : IDSSpectrum) (lam : Nat) : Nat :=
  ((s.filter (fun p => p.1 ≤ lam)).map Prod.snd).sum

/-- The **integrated density of states** `N(λ) = (1/total)·Σ_{λ_i ≤ λ} mult_i`, as an exact rational. -/
def ids (s : IDSSpectrum) (lam : Nat) : ℚ :=
  (cumMult s lam : ℚ) / (totalMult s : ℚ)

/-- **Cumulative multiplicities at the jump points are `1, 13, 23, 31, 33`.** -/
theorem cumMult_jump_points :
    cumMult specK 0 = 1
      ∧ cumMult specK 20 = 13
      ∧ cumMult specK 22 = 23
      ∧ cumMult specK 24 = 31
      ∧ cumMult specK 33 = 33 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- The IDS at a threshold equals the cumulative-multiplicity natural divided by `totalMult`, with the
Nat parts reduced to concrete numerals (so the remaining goal is pure rational arithmetic). -/
theorem ids_eq (lam : Nat) :
    ids specK lam = (cumMult specK lam : ℚ) / 33 := by
  unfold ids
  rw [totalMult_specK]
  norm_num

/-- **The IDS staircase equals the exact rationals `[1/33, 13/33, 23/33, 31/33, 1]`** at the jump
points `0 < 20 < 22 < 24 < 33`. -/
theorem ids_staircase :
    ids specK 0 = (1 : ℚ) / 33
      ∧ ids specK 20 = (13 : ℚ) / 33
      ∧ ids specK 22 = (23 : ℚ) / 33
      ∧ ids specK 24 = (31 : ℚ) / 33
      ∧ ids specK 33 = 1 := by
  obtain ⟨h0, h20, h22, h24, h33⟩ := cumMult_jump_points
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [ids_eq, h0]; norm_num
  · rw [ids_eq, h20]; norm_num
  · rw [ids_eq, h22]; norm_num
  · rw [ids_eq, h24]; norm_num
  · rw [ids_eq, h33]; norm_num

/-- The IDS is **monotone non-decreasing and reaches `1` at the top**: it is a genuine probability
staircase on the spectrum. -/
theorem ids_monotone_top :
    ids specK 0 < ids specK 20
      ∧ ids specK 20 < ids specK 22
      ∧ ids specK 22 < ids specK 24
      ∧ ids specK 24 < ids specK 33
      ∧ ids specK 33 = 1 := by
  obtain ⟨h0, h20, h22, h24, h33⟩ := cumMult_jump_points
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [ids_eq, ids_eq, h0, h20]; norm_num
  · rw [ids_eq, ids_eq, h20, h22]; norm_num
  · rw [ids_eq, ids_eq, h22, h24]; norm_num
  · rw [ids_eq, ids_eq, h24, h33]; norm_num
  · rw [ids_eq, h33]; norm_num

/-! ## Power proxy `P(k)` and the discrete tilt proxy `n_s − 1`, exact rationals -/

/-- The power proxy `P(k) = Σ_i mult_i / (k² + λ_i)`, exact rational arithmetic. -/
def powerProxy (s : IDSSpectrum) (k : ℚ) : ℚ :=
  (s.map (fun p => (p.2 : ℚ) / (k ^ 2 + (p.1 : ℚ)))).sum

/-- The exact derivative `P'(k) = Σ_i mult_i · (−2k) / (k² + λ_i)²` (term-by-term, exact rational). -/
def powerProxyDeriv (s : IDSSpectrum) (k : ℚ) : ℚ :=
  (s.map (fun p => (p.2 : ℚ) * (-(2 * k)) / (k ^ 2 + (p.1 : ℚ)) ^ 2)).sum

/-- The discrete **tilt proxy** `n_s − 1 := (k / P(k)) · P'(k)` — a genuine function of the free
evaluation point `k`, NOT an asserted physical value. -/
def tiltProxy (s : IDSSpectrum) (k : ℚ) : ℚ :=
  (k / powerProxy s k) * powerProxyDeriv s k

/-- **`P(k)` is the stated exact rational at the two sample points** `k = 1` and `k = 2`. -/
theorem powerProxy_samples :
    powerProxy specK 1 = (163196 : ℚ) / 68425
      ∧ powerProxy specK 2 = (19857 : ℚ) / 13468 := by
  refine ⟨?_, ?_⟩ <;>
    · simp only [powerProxy, specK, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
        Prod.fst, Prod.snd]
      norm_num

/-- **The tilt proxy takes two GENUINELY DIFFERENT exact rationals at `k = 1` and `k = 2`.** -/
theorem tiltProxy_samples :
    tiltProxy specK 1 = (-29795504237 : ℚ) / 33500058900
      ∧ tiltProxy specK 2 = (-119488232 : ℚ) / 200575557 := by
  refine ⟨?_, ?_⟩ <;>
    · simp only [tiltProxy, powerProxy, powerProxyDeriv, specK,
        List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Prod.fst, Prod.snd]
      norm_num

/-- **NO-GO (spectrum alone does NOT fix `n_s`).** The discrete tilt proxy `n_s − 1` evaluates to two
DIFFERENT rationals at the two sample points `k = 1 ≠ k = 2`. Since the bare spectrum supplies no
canonical evaluation point, it does not determine a single scalar `n_s`. -/
theorem spectrum_alone_does_not_fix_ns :
    tiltProxy specK 1 ≠ tiltProxy specK 2 := by
  rw [tiltProxy_samples.1, tiltProxy_samples.2]
  norm_num

/-- **D0-CMB-NS-LAPLACIAN-IDS-OWNER-001.** From the EXACT `K(9,11,13)` Laplacian spectrum (total
multiplicity `33`, `λ₂ = 20`): the IDS staircase equals `[1/33, 13/33, 23/33, 31/33, 1]` at its jump
points, the power proxy `P(k)` is exact at the two sample `k`, and the discrete tilt proxy `n_s − 1`
takes two DIFFERENT values at `k = 1` vs `k = 2` — so the bare spectrum ALONE does not determine a
single `n_s`. (No `n_s` value is asserted; the canonical smoothing/evaluation rule is PROOF-TARGET.) -/
theorem cmb_ns_laplacian_ids_owner :
    totalMult specK = 33
      ∧ multOf specK 20 = 12
      ∧ ids specK 0 = (1 : ℚ) / 33
      ∧ ids specK 20 = (13 : ℚ) / 33
      ∧ ids specK 22 = (23 : ℚ) / 33
      ∧ ids specK 24 = (31 : ℚ) / 33
      ∧ ids specK 33 = 1
      ∧ powerProxy specK 1 = (163196 : ℚ) / 68425
      ∧ powerProxy specK 2 = (19857 : ℚ) / 13468
      ∧ tiltProxy specK 1 ≠ tiltProxy specK 2 := by
  refine ⟨totalMult_specK, ?_, ids_staircase.1, ids_staircase.2.1, ids_staircase.2.2.1,
      ids_staircase.2.2.2.1, ids_staircase.2.2.2.2, powerProxy_samples.1, powerProxy_samples.2,
      spectrum_alone_does_not_fix_ns⟩
  decide

end D0.Cosmology.CMBLaplacianIDS
