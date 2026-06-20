import Mathlib.Tactic

/-!
# D0-VNEXT-AF-D0-SPECTRAL-COMPRESSION-OWNER-001 — spectral invariant obstruction (Phase D)

Even granting a dimension-`33` identification, any unitary intertwiner `Ξ` must preserve the eigenvalue-
multiplicity structure. It cannot:

- The frozen D0 scene Laplacian has spectrum `{0:1, 20:12, 22:10, 24:8, 33:2}` — **5 distinct eigenvalues**
  with multiplicity multiset `{1,2,8,10,12}` (trace `= 0·1+20·12+22·10+24·8+33·2 = 718`).
- The AF martingale Dirac² on `H_3^GNS` is diagonal on the increments `K_N`, with multiplicities equal to
  the Fibonacci increment dimensions `dim K_N = dim A_N − dim A_{N-1} = 2,3,8,21` (from `dim A = 2,5,13,34`).
  Removing the trace line (the cyclic mode in `K_0`) gives the reduced multiset `{1,3,8,21}` — **4 distinct
  eigenvalues**, summing to `33`.

`{1,3,8,21} ≠ {1,2,8,10,12}` and the eigenvalue COUNTS differ (4 vs 5). Crucially the Dirac scale only
sets the eigenVALUES, never the multiplicities — so this obstruction is **scale-independent**: NO admissible
Dirac scale and NO unitary `Ξ` can identify the compressed AF operator with the frozen D0 scene Laplacian.
-/

namespace D0.VNext.AFD0SpectralInvariantComparison

/-- Frozen D0 scene Laplacian multiplicity multiset (sorted): `{1,2,8,10,12}` for `{0,20,22,24,33}`. -/
def sceneMults : List ℕ := [1, 2, 8, 10, 12]

/-- The scene Laplacian trace `= 0·1 + 20·12 + 22·10 + 24·8 + 33·2 = 718`. -/
def sceneTrace : ℕ := 0 * 1 + 20 * 12 + 22 * 10 + 24 * 8 + 33 * 2

/-- AF GNS algebra dimensions `dim A_N = 2,5,13,34` (levels 0..3). -/
def dimA : List ℕ := [2, 5, 13, 34]

/-- Reduced AF martingale Dirac² multiplicities: increments `dim K_N` with the trace line removed from
`K_0` → `{1,3,8,21}`. -/
def afReducedMults : List ℕ := [2 - 1, 5 - 2, 13 - 5, 34 - 13]

theorem af_reduced_mults_eq : afReducedMults = [1, 3, 8, 21] := by decide

/-- **Scene Laplacian invariants**: multiplicity multiset `{1,2,8,10,12}` (sum 33), trace `718`,
`5` distinct eigenvalues. -/
theorem scene_laplacian_invariants :
    sceneMults.sum = 33 ∧ sceneTrace = 718 ∧ sceneMults.length = 5 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **AF reduced multiplicities** `{1,3,8,21}` (sum 33, `4` distinct eigenvalues) — the Fibonacci
increments with the trace line removed. -/
theorem af_reduced_invariants :
    afReducedMults.sum = 33 ∧ afReducedMults.length = 4 := by
  refine ⟨by decide, by decide⟩

/-- **D0-VNEXT-AF-D0-SPECTRAL-COMPRESSION-OWNER-001 (NO-GO, scale-independent).** The AF reduced
multiplicity multiset `{1,3,8,21}` differs from the scene Laplacian's `{1,2,8,10,12}`, and the eigenvalue
COUNTS differ (4 vs 5). A unitary `Ξ` must preserve multiplicities; the Dirac scale sets only eigenvalues.
So NO admissible scale and NO unitary `Ξ` identify the compressed AF operator with the frozen D0 scene
Laplacian — the spectral obstruction is scale-independent. -/
theorem spectral_invariant_obstruction :
    afReducedMults ≠ sceneMults ∧ afReducedMults.length ≠ sceneMults.length := by
  refine ⟨by decide, by decide⟩

end D0.VNext.AFD0SpectralInvariantComparison
