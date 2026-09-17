import D0.Claims.Time2DPisot

/-!
# D0-RANK3-CAUSAL-CONE-001 — (3,1) signature carries a Minkowski causal cone (synthesis)

Python companion: the gravastar compactness LEM (`vp_gravastar_compactness.py`) leaves one
NAMED GAP — "rank-3 transport = the causal light-cone on the 3-sphere seam." This module
SHARPENS that gap by synthesising the owned pieces:

* rank-3 scene adjacency = the spatial sector (owned by `D0.Claims.Signature31Split`),
* one Pisot modular flow = time, with the arrow `|ψ| < 1` (owned by `D0.Claims.Time2DPisot`).

Together they are the signature `(3,1)`, whose Minkowski quadratic form
`Q(a,b,c,d) = a² − b² − c² − d²` is exactly a causal cone: it is indefinite (a timelike and
a spacelike direction) and has a nontrivial null cone. That structural fact is proved here.

NAMED GAP (why this does NOT promote `D0-COMPACTNESS-LIMIT-001` to THE): the identification
of the scene's rank-3 transport modes WITH the spatial axes of this cone is still a
postulated bridge — proving the cone EXISTS for signature `(3,1)` is not the same as proving
the scene's rank-3 IS that spatial sector. So this is a SHARPENED BRIDGE, not a closure: the
`(3,1) → cone` half is now machine-checked; the `scene-rank ↔ cone-space` half remains open.
-/

namespace D0.Synthesis

open D0

/-- The Minkowski quadratic form of signature `(3,1)` (one `+`, three `−`). -/
def mink4 (a b c d : ℝ) : ℝ := a ^ 2 - b ^ 2 - c ^ 2 - d ^ 2

/-- The null cone is nontrivial: `(1,1,0,0)` is a nonzero null direction. -/
theorem mink_null_direction : mink4 1 1 0 0 = 0 := by norm_num [mink4]

/-- A timelike direction exists (`Q > 0`) — the `+1`, the Pisot modular-time axis. -/
theorem mink_timelike : 0 < mink4 1 0 0 0 := by norm_num [mink4]

/-- A spacelike direction exists (`Q < 0`) — one of the rank-3 spatial axes. -/
theorem mink_spacelike : mink4 0 1 0 0 < 0 := by norm_num [mink4]

/-- **D0-RANK3-CAUSAL-CONE-001 (sharpened bridge).** The `(3,1)` signature — rank-3 space
plus one Pisot modular-time flow (`|ψ| < 1`, the arrow) — carries a Minkowski causal cone:
indefinite, with a nontrivial null direction. The `scene-rank ↔ cone-space` identification
remains the named gap, so the compactness lemma is sharpened, not promoted to THE. -/
theorem rank3_causal_cone :
    mink4 1 1 0 0 = 0 ∧
    0 < mink4 1 0 0 0 ∧
    mink4 0 1 0 0 < 0 ∧
    |psi| < 1 :=
  ⟨mink_null_direction, mink_timelike, mink_spacelike, D0.Claims.psi_abs_lt_one⟩

end D0.Synthesis
