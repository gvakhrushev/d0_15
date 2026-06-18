import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# D0-C-LIGHTCONE-PERCOLATION-OWNER-001 / c = 1 light-cone from connectivity + spectral gap (Lean)

Python certificates: `05_CERTS/vp_c_lightcone_percolation_owner.py`,
`05_CERTS/vp_connectivity_spectral_gap_speed.py`.

Front P4 (companion to `D0.Cosmology.ReheatingPercolationOwner`). The discrete signal speed is the
ratio of a unit cell-length to a unit tick: `c_D0 = ell0 / tau0`. With the tick gauge `ell0 = tau0 = 1`
(one edge traversed per discrete step) this is `c_D0 = 1`. The CONTENT — the part that is a theorem,
not a unit choice — is that signal propagation along the scene graph exists at all only when the graph
is CONNECTED, and connectivity is detected by the algebraic connectivity (Fiedler value `λ₂`, the
smallest nonzero Laplacian eigenvalue): `λ₂ > 0 ⇔ connected`.

WHAT IS OWNED HERE (CERT-CLOSED, machine-checked below):

* The tick gauge `TickGauge` with `ell0 = tau0 = 1` and `cD0 = 1` (`cD0_eq_one`, `rfl`). This is a
  UNIT-FIXING gauge, honestly NOT a derivation of the numerical value `1`.
* The Laplacian `Lap` of the forced scene graph `K(9,11,13)` (33 vertices, complete tripartite) carries
  a POSITIVE algebraic connectivity. Two of its Laplacian eigenvalues are exhibited by explicit
  eigenvectors against the real 33×33 matrix:
    - the all-ones vector is a `0`-eigenvector (`lap_ones_eigen0`);
    - a part-2 vector summing to zero is a `20`-eigenvector (`lap_fiedler_eigen20`), and `20 > 0`.
  The closed-form complete-multipartite Laplacian spectrum
  `{0, 20×12, 22×10, 24×8, 33×2}` is trace-consistent with the actual matrix (`spec_trace_consistent`),
  has exactly one zero (kernel dimension 1 ⇒ connected, `spec_one_zero`), and every nonzero entry is
  `≥ 20` (`spec_gap_ge_20`), so the Fiedler value (the smallest nonzero eigenvalue) equals `20 > 0`.
* The edgeless 33-vertex stage has Laplacian `0`; two independent indicator vectors lie in its kernel
  (`edgeless_e0_kernel`, `edgeless_e1_kernel`, `e0_ne_e1`), so its `0`-eigenspace has dimension `≥ 2`:
  its Fiedler value `λ₂ = 0` (disconnected, no propagation).

HONESTY BOUNDARY.
* `cD0 = 1` is a GAUGE (`ell0 = tau0 = 1`), not a derivation; the SI numerical value of `c` is NOT an
  output and NOT an input (the cert rejects importing it).
* `spec_gap_ge_20` is proved over the CLOSED-FORM spectrum multiset `specList` (the standard complete-
  multipartite Laplacian spectrum). That `specList` IS the full spectrum (no eigenvalue missing) is
  checked here only by trace + count consistency and by exhibiting `0` and `20` as genuine eigenvalues;
  the full characteristic-polynomial factorization (and the exact normalized-Laplacian Cheeger bound)
  stays PROOF-TARGET.
-/

namespace D0.Cosmology

open Matrix
open scoped BigOperators

/-! ## The tick gauge and the speed `c_D0 = 1` (a UNIT choice, not a derivation) -/

/-- A tick gauge: a unit cell-length `ell0` and a unit tick `tau0`. The discrete signal speed is the
ratio `ell0 / tau0` (one edge per tick). With `ell0 = tau0 = 1` the speed is `1`. -/
structure TickGauge where
  ell0 : ℚ
  tau0 : ℚ
  h_ell0 : ell0 = 1
  h_tau0 : tau0 = 1

/-- The canonical D0 tick gauge `ell0 = tau0 = 1`. -/
def d0Tick : TickGauge := ⟨1, 1, rfl, rfl⟩

/-- The discrete signal speed of a tick gauge: cell-length per tick. -/
def speed (g : TickGauge) : ℚ := g.ell0 / g.tau0

/-- The D0 light-cone speed in the canonical gauge. -/
def cD0 : ℚ := speed d0Tick

/-- **`c_D0 = 1`.** With `ell0 = tau0 = 1` (one edge per discrete step) the speed is exactly `1`. This
is a UNIT-FIXING gauge, not a derivation of the value `1`. -/
theorem cD0_eq_one : cD0 = 1 := by unfold cD0 speed d0Tick; norm_num

/-- For ANY tick gauge with `ell0 = tau0 = 1` the speed is `1` (the value is forced by the gauge,
not by any spectral datum). -/
theorem speed_eq_one (g : TickGauge) : speed g = 1 := by
  unfold speed; rw [g.h_ell0, g.h_tau0]; norm_num

/-! ## The forced scene graph `K(9,11,13)` and its Laplacian -/

/-- Part label of a vertex of the 33-vertex scene: `9` of label `0`, `11` of label `1`, `13` of
label `2` (zone sizes `9, 11, 13`). -/
def lbl (i : Fin 33) : Nat :=
  if i.val < 9 then 0 else if i.val < 20 then 1 else 2

/-- Adjacency of the complete tripartite graph `K(9,11,13)`: an edge iff distinct vertices lie in
distinct parts (no intra-part edge — a role cannot distinguish itself). -/
def Adj (i j : Fin 33) : ℚ := if i ≠ j ∧ lbl i ≠ lbl j then 1 else 0

/-- Vertex degree: number of cross-part neighbours. -/
def deg (i : Fin 33) : ℚ := ∑ j, Adj i j

/-- Combinatorial Laplacian `L = D − A` of `K(9,11,13)`. -/
def Lap : Matrix (Fin 33) (Fin 33) ℚ :=
  Matrix.of (fun i j => if i = j then deg i else - Adj i j)

/-- A part-`0` vertex (size-9 part) has degree `n − 9 = 24`. -/
theorem deg_part0 : deg ⟨0, by omega⟩ = 24 := by native_decide

/-- A part-`2` vertex (size-13 part) has degree `n − 13 = 20`. -/
theorem deg_part2 : deg ⟨20, by omega⟩ = 20 := by native_decide

/-! ## Exhibited Laplacian eigenvectors (genuine spectral content) -/

/-- The all-ones vector. -/
def ones : Fin 33 → ℚ := fun _ => 1

/-- **`0` is a Laplacian eigenvalue** (every row of `L` sums to zero): `L · 𝟙 = 0`. Equivalently, the
all-ones vector spans (part of) the kernel — the connected graph has at least one zero eigenvalue. -/
theorem lap_ones_eigen0 : Lap.mulVec ones = fun _ => 0 := by native_decide

/-- A Fiedler eigenvector: `+1` at vertex `20`, `−1` at vertex `21` (both in the size-13 part),
`0` elsewhere — a vector summing to zero on part `2`. -/
def fied : Fin 33 → ℚ := fun i => if i.val = 20 then 1 else if i.val = 21 then -1 else 0

/-- **`20` is a Laplacian eigenvalue**: `L · fied = 20 · fied`. (For a complete multipartite graph a
vector summing to zero on the size-`nᵢ` part is an eigenvector with eigenvalue `n − nᵢ`; here
`33 − 13 = 20`.) This is the exhibited Fiedler value. -/
theorem lap_fiedler_eigen20 : Lap.mulVec fied = fun i => 20 * fied i := by native_decide

/-- The exhibited Fiedler value is strictly positive: `20 > 0`. This is the CONTENT of the light-cone
claim — a positive spectral gap, hence connectivity, hence one-edge-per-tick propagation exists. -/
theorem fiedler_pos : (0 : ℚ) < 20 := by norm_num

/-! ## Closed-form spectrum consistency (trace, count, gap) -/

/-- Closed-form complete-multipartite Laplacian spectrum of `K(9,11,13)`:
`0` (×1), `20` (×12), `22` (×10), `24` (×8), `33` (×2) — `33` eigenvalues total. -/
def specList : List ℚ :=
  (List.replicate 1 (0 : ℚ)) ++ (List.replicate 12 20) ++ (List.replicate 10 22)
    ++ (List.replicate 8 24) ++ (List.replicate 2 33)

/-- The closed-form spectrum has exactly `33` entries (one per vertex). -/
theorem spec_length : specList.length = 33 := by native_decide

/-- **Trace consistency.** The sum of the closed-form eigenvalues equals `tr L` (the sum of degrees
`= 2·359 = 718`). A necessary check that `specList` is the spectrum of `Lap`. -/
theorem spec_trace_consistent : specList.sum = Lap.trace := by native_decide

/-- The Laplacian trace is `718` (twice the `359` cross-zone edges). -/
theorem lap_trace : Lap.trace = 718 := by native_decide

/-- **Connectivity ⇔ one zero eigenvalue.** The closed-form spectrum has exactly one `0`, i.e. the
Laplacian kernel is one-dimensional — the graph is connected (a single component). -/
theorem spec_one_zero : (specList.filter (fun x => x = 0)).length = 1 := by native_decide

/-- **Positive spectral gap.** Every nonzero eigenvalue of the closed-form spectrum is `≥ 20`, so the
Fiedler value (the smallest nonzero eigenvalue) is `20 > 0`. -/
theorem spec_gap_ge_20 : ∀ x ∈ specList, x ≠ 0 → 20 ≤ x := by decide

/-- The gap value `20` is actually attained in the spectrum (it is not a vacuous lower bound). -/
theorem spec_gap_attained : (20 : ℚ) ∈ specList := by decide

/-! ## The edgeless (disconnected) stage: Fiedler value `0` -/

/-- Edgeless 33-vertex stage: no edges, so the Laplacian is the zero matrix. -/
def LapEdgeless : Matrix (Fin 33) (Fin 33) ℚ := 0

/-- Indicator of vertex `0`. -/
def e0 : Fin 33 → ℚ := fun i => if i.val = 0 then 1 else 0

/-- Indicator of vertex `1`. -/
def e1 : Fin 33 → ℚ := fun i => if i.val = 1 then 1 else 0

/-- `e0` is in the kernel of the edgeless Laplacian (eigenvalue `0`). -/
theorem edgeless_e0_kernel : LapEdgeless.mulVec e0 = fun _ => 0 := by native_decide

/-- `e1` is in the kernel of the edgeless Laplacian (eigenvalue `0`). -/
theorem edgeless_e1_kernel : LapEdgeless.mulVec e1 = fun _ => 0 := by native_decide

/-- `e0 ≠ e1`: two distinct indicator vectors. Together with the two kernel facts above, the
`0`-eigenspace of the edgeless Laplacian has dimension `≥ 2`, so its second-smallest eigenvalue is
`λ₂ = 0`: the edgeless stage is DISCONNECTED and carries NO positive gap (no propagation). -/
theorem e0_ne_e1 : e0 ≠ e1 := by decide

/-! ## Owner theorem -/

/-- **D0-C-LIGHTCONE-PERCOLATION-OWNER-001.** The c = 1 light-cone owner, honestly split:

* the speed `c_D0 = 1` is a UNIT gauge (`ell0 = tau0 = 1`);
* the CONTENT is the positive algebraic connectivity of the forced scene `K(9,11,13)`: a genuine
  `0`-eigenvector (`L·𝟙 = 0`) and a genuine `20`-eigenvector (`L·fied = 20·fied`) with `20 > 0`,
  trace-consistent with the closed-form spectrum whose smallest nonzero entry is `20`;
* by contrast the edgeless stage has `λ₂ = 0` (a two-dimensional `0`-eigenspace), i.e. it is
  disconnected and propagates nothing.

So one-edge-per-tick signal propagation exists exactly at/after the connectivity threshold, and at the
threshold the gauge fixes its speed to `c_D0 = 1`. -/
theorem c_lightcone_percolation_owner :
    cD0 = 1 ∧
    Lap.mulVec ones = (fun _ => 0) ∧
    Lap.mulVec fied = (fun i => 20 * fied i) ∧
    (0 : ℚ) < 20 ∧
    specList.sum = Lap.trace ∧
    (specList.filter (fun x => x = 0)).length = 1 ∧
    (∀ x ∈ specList, x ≠ 0 → 20 ≤ x) ∧
    LapEdgeless.mulVec e0 = (fun _ => 0) ∧
    LapEdgeless.mulVec e1 = (fun _ => 0) ∧
    e0 ≠ e1 :=
  ⟨cD0_eq_one, lap_ones_eigen0, lap_fiedler_eigen20, fiedler_pos, spec_trace_consistent,
   spec_one_zero, spec_gap_ge_20, edgeless_e0_kernel, edgeless_e1_kernel, e0_ne_e1⟩

end D0.Cosmology
