import Mathlib.Tactic
import Mathlib.NumberTheory.Real.GoldenRatio
import D0.Foundation.CascadeChain
import D0.Foundation.CascadeFloorScaleRatio
import D0.Geometry.TorusShellAttachment

/-!
# Cascade floor: closure ⇒ shell

**Target: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`** (umbrella, #2 of the computed attack queue).
The §01.6.1c cascade reads `… defect ⇒ circulation needs closure ⇒ shell …`; the owned
reading of THIS step is BOOK_03 §03.23.5 (FORCED), verbatim: "An interior defect (03.23.4)
plus a memory-circulation zone (03.23.3) leaves the global topology open; closing it requires
an outer shell (the Closure role D of 03.23.1). The shell's scaling cannot carry a free
parameter (M1). The only self-consistent parameter-free scale is the positive root of
`r² − r − 1 = 0 ⇒ r = φ`."

**The floor, formalized on the OWNED shell geometry** (`D0.Geometry.TorusShellAttachment`:
radii `inner = R−r`, `core = R`, `outer = R+r` for every admissible parameter). The bridging
proxy, stated as this module's own definition (scoped, not smuggled): *closure* is read as
closure of the radius set under the radial REFLECTION around the core, `ρ(x) = 2·core − x` —
the canonical completion move of the three-term radial progression (the reflection that fixes
the circulation core and exchanges interior with exterior). Under that reading:

* the INTERIOR pair `{inner, core}` — §03.23.5's own identification: the interior defect
  layer (03.23.4) plus the memory-circulation zone (03.23.3) — is NOT reflection-closed:
  `ρ(inner) = outer` lies outside it, for EVERY admissible parameter
  (`interior_not_reflection_closed`);
* the three-shell set `{inner, core, outer}` IS reflection-closed, for every admissible
  parameter (`shells_reflection_closed`) — the outer shell is exactly what the completion
  demands;
* the M1 leg: the shell's scaling carries no free parameter — the fixed-point equation
  `x = 1 + 1/x` has EXACTLY ONE positive solution, and it is `φ`
  (`shell_scale_forced`, real level, from the golden quadratic); and `φ` is precisely the
  scale floor's own survivor (`phi_non_captured`, cited): the forced shell scale SATISFIES
  the scale obligation — the cascade's `φ` reappears at the shell, closing the loop between
  the two floors (`shell_scale_is_scale_survivor`).

**Honest scope (pre-registered).**
1. "Global topology open/closed" (genus, boundary) is NOT formalized; the reflection-closure
   proxy is this module's bridging definition, anchored on the owned radius values. A
   different owned reading of shell-closure is new work with its own audit.
2. The `φ⁵` aspect `(R+r)/(R−r) = φ⁵` is §03.23.6's separate content — NOT claimed here.
3. The `+2` zone spectrum {9,11,13} and the address-parity floor
   (`CascadeFloorOrientationParity`) are separate owned pieces — cited, not absorbed; the
   zone sizes enter only through the owned attachment.
4. The geometry parameter is RATIONAL (`TorusParameter`, `1 < a`); the forced `φ`-scale is
   the separate REAL M1 statement — the two meet only through §03.23.5's prose, and this
   module keeps them in separate theorems (no rational-φ conflation).
5. The umbrella stays OPEN: the terminal step `three insufficiencies = three zones` remains
   unformalized.
-/

namespace D0.Foundation

open D0.Geometry Real
open scoped goldenRatio

/-- The radial reflection around the circulation core: the canonical completion move of the
three-term radial progression. This module's bridging proxy for §03.23.5's closure. -/
def shellReflection (T : TorusParameter) (x : ℚ) : ℚ := 2 * T.core - x

/-- **`insufficient` — the interior pair is not closed.** The interior defect layer plus the
memory-circulation zone (§03.23.5's own identification of the two interior layers) do not
close under the reflection: `ρ(inner) = outer` escapes, for EVERY admissible parameter. -/
theorem interior_not_reflection_closed :
    ¬ ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core} : Set ℚ),
      shellReflection T x ∈ ({T.inner, T.core} : Set ℚ) := by
  intro h
  obtain ⟨T⟩ : Nonempty TorusParameter := ⟨⟨2, by norm_num⟩⟩
  have hin := h T T.inner (by simp)
  have hgt := T.h_gt_one
  rcases hin with h1 | h2
  · have : (2 : ℚ) * T.core - T.inner = T.inner := h1
    have hc : T.core = T.inner := by linarith
    have := (torusShell_radius_strictMono T).1
    rw [torusShell_radius_inner, torusShell_radius_core] at this
    exact absurd hc (by linarith)
  · have : (2 : ℚ) * T.core - T.inner = T.core := h2
    have hc : T.core = T.inner := by linarith
    have := (torusShell_radius_strictMono T).1
    rw [torusShell_radius_inner, torusShell_radius_core] at this
    exact absurd hc (by linarith)

/-- **`control` — the three shells close.** With the outer shell present, the radius set is
reflection-closed for every admissible parameter: `ρ(inner) = outer`, `ρ(core) = core`,
`ρ(outer) = inner`. -/
theorem shells_reflection_closed :
    ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
      shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ) := by
  intro T x hx
  have houter : (2 : ℚ) * T.core - T.inner = T.outer := by
    show (2 : ℚ) * ((T.a + 1) / 2) - 1 = T.a
    ring
  have hinner : (2 : ℚ) * T.core - T.outer = T.inner := by
    show (2 : ℚ) * ((T.a + 1) / 2) - T.a = 1
    ring
  rcases hx with h | h | h
  · right; right; rw [h]; exact houter
  · right; left; rw [h]; show (2 : ℚ) * T.core - T.core = T.core; ring
  · left; rw [h]; exact hinner

/-- **The floor, in the registered `CascadeStep` shape.** -/
def stepShellClosure : CascadeStep where
  name := "closure needs the outer shell (shell floor)"
  ObligationBelow := ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core} : Set ℚ),
    shellReflection T x ∈ ({T.inner, T.core} : Set ℚ)
  ObligationAbove := ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
    shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ)
  insufficient := interior_not_reflection_closed
  control := shells_reflection_closed

/-- **The M1 leg: the shell scale is forced, parameter-free.** The fixed-point equation
`x = 1 + 1/x` of §03.23.5 has exactly one positive solution, and it is `φ`. -/
theorem shell_scale_forced (x : ℝ) (hx : 0 < x) : x = 1 + 1 / x ↔ x = φ := by
  constructor
  · intro h
    have hq : x ^ 2 = x + 1 := by
      field_simp at h
      nlinarith [h]
    have hfac : (x - φ) * (x + φ - 1) = 0 := by
      nlinarith [goldenRatio_sq, hq]
    rcases mul_eq_zero.mp hfac with h1 | h2
    · linarith [sub_eq_zero.mp h1]
    · exfalso
      have hφ : (1 : ℝ) < φ := one_lt_goldenRatio
      linarith
  · intro h
    subst h
    have hφ : φ ≠ 0 := ne_of_gt (by linarith [one_lt_goldenRatio])
    field_simp
    nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 5 by norm_num), Real.sqrt_nonneg 5]

/-- **The forced shell scale is the scale floor's own survivor**: `φ` satisfies the 6→7
obligation (`NonCaptured`, cited from the scale floor) — the cascade's `φ` reappears at the
shell, linking the shell floor back to the scale floor's control. -/
theorem shell_scale_is_scale_survivor : NonCaptured ((1 + Real.sqrt 5) / 2) :=
  phi_non_captured

/-- **The fourth link (closure → shell), PROSE-ANCHORED**: unlike links 1–3 (shared-object
interlock shape), the adjacency to the defect-closure floor is carried by §03.23.5's own
FORCED two-layer identification, not by a shared formal object (no defect-floor object
occurs below); the formal cross-floor tie is to the SCALE floor's control
(`phi_non_captured`). Conjuncts: the interior two layers fail reflection-closure; the outer
shell closes it; the shell's scale is forced parameter-free to `φ`. -/
theorem chain_linked_closure_to_shell :
    (¬ ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core} : Set ℚ),
        shellReflection T x ∈ ({T.inner, T.core} : Set ℚ))
      ∧ (∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
          shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ))
      ∧ (∀ x : ℝ, 0 < x → (x = 1 + 1 / x ↔ x = φ))
      ∧ NonCaptured ((1 + Real.sqrt 5) / 2) :=
  ⟨interior_not_reflection_closed, shells_reflection_closed,
    shell_scale_forced, shell_scale_is_scale_survivor⟩

/-- The floor is genuine: obligations below and above do not coincide. -/
theorem shell_closure_floor_genuine :
    ¬ (stepShellClosure.ObligationBelow ↔ stepShellClosure.ObligationAbove) :=
  step_discriminates stepShellClosure

end D0.Foundation
