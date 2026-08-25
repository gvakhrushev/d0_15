# TORAL-COMPOSITION-SEVENTEEN — the depth composition 17 = 5 + 12 acquires a toral LAW (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: WOUNDED-FIXABLE, no kill; R1-R3 applied,
errors of record enumerated in the Repairs section. Pre-flight run: `3571`, `322`, `L17`,
`seventeen` — `3571` appears only in `D0-TRANSPORT-FORK-ENDGAME-001` (the `native_decide`-
carrying `trace_T17`, excluded from its own assembly); `322` only in an unrelated packing-probe
row. ERROR OF RECORD (R1, accepted): the draft claimed 'no even-return-defect ownership
anywhere' — FALSE at the real level: `D0-LUCAS-DEFECT-SIGN-001` (`LucasDefectSign.lean:22`,
`lucas_defect`, THE) owns `phi^n - lucasR n = (-1)^(n+1) (phi^n)^-1` for ALL n. What has no
prior carrier: the integer bridge (`lucas_gold` — lucasR is never identified with the
recursive integer lucas), the numeral 12-instantiation, the composition law and the trace
transport. Target context:
obligation (i) of `D0-ALPHA-SEAM-FORM-FORCED-001`; hypothesis (γ) of
`D0-SEAM-CROSSING-WEIGHT-001`.

## Claim X (DEF-0.2.2 form)

X: three unconditional theorems on the toral side (Lean
`D0.Synthesis.ToralCompositionSeventeen`, clean axioms `propext/Classical.choice/Quot.sound`
throughout — machine-checked by `#print axioms`, no `native_decide`):

1. **Both factors of the registered total are return defects.** The general address
   `(φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)` (`golden_return_defect` — the INTEGER-BRIDGE upgrade, via
   `lucas_gold`, of the owned real-level defect identity `D0-LUCAS-DEFECT-SIGN-001`
   `lucas_defect`, THE; the identity SHAPE is not new) gives `ξ₅ = φ⁻⁵ = φ⁵ − 11` (integer
   level owned at `D0-XI5-TORUS-DEFECT-001`, real level at row 538 — joined clean here) AND
   the numeral-instantiated `φ⁻¹² = 322 − φ¹² = L₁₂ − φ¹²` (`transport_factor_toral_address`)
   — the OPEN transport factor acquires the same defect shape as the owned seam factor, at
   the twelfth return; new content = bridge + instantiation + law, not the shape.
2. **The composition is a return law, not exponent arithmetic.** `L_{m+n} = L_m·L_n −
   (−1)ⁿ·L_{m−n}` (`lucas_composition`, via the golden closed form `Lₙ = φⁿ + (1−φ)ⁿ`),
   transported through the owned dictionary `Tr(Tᵏ) = (−1)ᵏLₖ` (`trace_T_pow_clean`,
   `D0-LEFSCHETZ-ZONE-EXCLUSION-001`): `Tr(T^{m+n}) = Tr(T^m)Tr(T^n) − (det T)ⁿTr(T^{m−n})`
   (`trace_return_composition`). At `(m,n) = (12,5)`: `Tr(T¹⁷) = Tr(T¹²)Tr(T⁵) −
   (det T)⁵Tr(T⁷)`, i.e. `L₁₇ = L₁₂L₅ + L₇` (3571 = 322·11 + 29) with the `+L₇` correction
   FORCED by the orientation reversal of the odd return (`det T⁵ = −1`).
3. **The registered total in toral addresses.** `φ⁻¹⁷ = (φ⁵ − 11)(322 − φ¹²)`
   (`registered_total_toral_form`).

Grade claimed: **unconditional toral-side mathematics; (γ) NOT owned; the primitive
SHARPENED on the toral route only.** SCOPE (R2, accepted — universal-over-unexhausted-class
guard): on the TORAL (door-2-adjacent) route the missing step narrows from "own the φ⁻¹²
transport factor + composition" to "identify the seam transport with the twelfth toral
return". Door 1 (`dim g_light`) remains the live rival: a door-1 discharge would own the
transport factor with NO seam-return identification, so the obligation's missing step over
ALL routes does not narrow.

## Owned pre-facts (verbatim, file:line)

- `BOOK_02 02.13.h` (0018__02.13:95): "the depth's **transport factor** `\varphi^{-12}` and
  the composition `\varphi^{-17}=\xi_5\cdot\varphi^{-12}` are **owned only as prose above** —
  a **named open sub-leg**, not THE."
- `TRANSPORT_TWELVE_FORK_MEMO.md` P1: "the ONLY mechanism content is the word 'electroweak'."
- `09_LEAN_FORMALIZATION/D0/Synthesis/TransportForkEndgame.lean:127-128` (`seventeen_ticks`):
  "Unconditionally this is arithmetic of the number `φ⁻¹`, nothing about the seam"; `:139`
  `trace_T17` carries `Lean.ofReduceBool` and is excluded from the assembly.
- `D0.Synthesis.LefschetzZoneExclusion.trace_T_pow_clean : ∀ n, Matrix.trace (T ^ n) =
  signedLucasTrace n` and `detT_clean : Matrix.det T = -1` — clean, minted this session
  (`D0-LEFSCHETZ-ZONE-EXCLUSION-001`).
- `09_LEAN_FORMALIZATION/D0/Foundation/LucasDefectSign.lean:22` (`D0-LUCAS-DEFECT-SIGN-001`,
  THE): `lucas_defect : φⁿ − lucasR n = (−1)^(n+1)·(φⁿ)⁻¹` with `lucasR n = φⁿ + ψⁿ` — the
  owned real-level defect identity; it never identifies `lucasR` with the recursive integer
  `D0.Dynamics.lucas` (the integer bridge is this module's `lucas_gold`).
- `D0.Claims.Xi5TorusDefect.xi5_torus_defect : lucas 5 = 11 ∧ Matrix.trace (T ^ 5) = -(lucas 5)`
  (`D0-XI5-TORUS-DEFECT-001`, CORE-FORMALIZED).
- `TransportForkEndgame.lean:60-63`: "the owned seam transport is parabolic-additive
  (`SeamTransportLinear`: `N² = 0`, composition adds) … unconditionally the seam has no
  per-crossing contraction at all" — the adverse owned fact, UNTOUCHED by this module (we add
  no seam claim).

## The forcing / construction (every constant computed, exact)

Python pre-check (session log): L₁₇ = 3571 = L₁₂L₅ + L₇ = 322·11 + 29; trace composition on
the integer matrix T verified directly; `φ⁻ⁿ = (−1)ⁿ(Lₙ − φⁿ)` verified in exact ℤ[φ] pairs
for n = 1..17; `(φ⁵−11)(322−φ¹²) = φ⁻¹⁷` exact in ℤ[φ]. Lean: module builds standalone (2954
jobs) and inside `D0.All` (4470 jobs GREEN); axioms clean (propext/Classical.choice/
Quot.sound) on ALL eleven row theorems + `lucas_gold` (R3; skeptic verified 13 names;
`lucas_seventeen_composition` needs only propext). Skeptic edge-case sweep: lucas_composition
verified for all n<=m<=14; n=0 and n=m degenerate correctly; the n<=m guard is load-bearing
(m=0,n=1 falsifies the unguarded form).

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest self-attack — "this is just algebra").** Every identity here follows
  from the golden quadratic; a skeptic can say the module adds rearrangements of known
  Fibonacci–Lucas facts. Defense, pre-registered: the CONTENT claimed is not the identities
  but (1) the corpus-internal ADDRESS — the open transport factor now has an owned toral-defect
  form parallel to the owned ξ₅, where before it had only the word "electroweak"; (2) the
  clean-axiom re-derivation of `Tr(T¹⁷) = −3571` (removing an `ofReduceBool` exclusion); and
  (3) the composition-law transport through the owned trace dictionary. The row text must
  claim exactly this and no more. A kill must name an existing corpus text already carrying
  the 12-return defect address or the composition law.
- **ATT-B (kill-shape 2: carrier mismatch via the numeral 12).** The twelfth RETURN is not a
  dim-12 carrier. The module and row explicitly do NOT bind the return index to door 1/2/5.
  Any future binding is new work with its own skeptic pass.
- **ATT-C (grade inflation risk: "narrows the primitive").** Saying the missing step "narrows"
  could be read as progress on (γ)'s truth. Scope: the narrowing is of the STATEMENT of what
  remains (the transport factor's form is now owned; the seam↔return identification is not),
  exactly parallel to how C4 shrank the primitive to (α)∧(β)∧(γ). The row must keep row-583's
  framing: conditional on the open composition, never derived-from-owned.
- **ATT-D (adverse owned fact).** The owned seam transport is parabolic-ADDITIVE (N²=0) — a
  multiplicative per-crossing reading is unconditionally absent on the seam. This module makes
  NO seam claim; the law lives on the toral side only. A kill via `SeamTransportLinear` would
  be a carrier mismatch (torus ≠ seam operator).
- **ATT-E (duplication).** `lucas_composition` is classical (Lucas 1878-grade). The corpus
  convention for classical results is ownership-by-formalization with external classics NOT
  re-claimed as discoveries; the row text says "classical identity, formalized clean, new to
  the tree" — grep confirmed no prior formalization OF THE COMPOSITION LAW in
  `09_LEAN_FORMALIZATION` (narrowed per R1: `lucasR` at row 538 is a prior closed-form
  formalization at the definitional level; all four in-tree lucas definitions checked, none
  carries a composition law).

## What this does NOT show

(γ) is not owned; no seam statement; no per-crossing mechanism; no door adjudication; no
binding of the return index 12 to any carrier; `seventeen_ticks`'s conditionality analysis and
row 583's obligations are unchanged. The module's value to the obligation is address + law;
on the TORAL ROUTE what remains is the sharpened primitive "one seam crossing sector = one
toral tick, with the seam transport identified with the twelfth return" — door 1 stays the
live rival and is untouched (R2 scope).

## Repairs (errors of record, accepted in full)

- R1: pre-flight false negative — `D0-LUCAS-DEFECT-SIGN-001` owns the real-level defect
  identity for all n; uncited in the draft. Repaired: cited in pre-facts, claim 1 reframed as
  integer-bridge + instantiation, ATT-E grep claim narrowed to the composition law.
- R2: "narrows the primitive" quantified over an unexhausted class (the fork's doors).
  Repaired: scoped to the toral route in memo Grade paragraph, closing paragraph, and module
  docstring; door 1 named as live rival with row-625 phrasing.
- R3: "axioms clean on all four exported theorems" undersold/mismatched the row list.
  Repaired: all eleven row theorems + lucas_gold verified.
- Advisories adopted: `lucas_gold` + `lucas_seventeen_composition` in the row theorem list;
  seventeen_ticks-style scoping sentence in the row note; row-625 AXIOM SPLIT cross-link
  (trace_T17 exclusion bypassable via trace_T17_clean); joint credit rows 186+538; classifier
  guardrails (no gauge/spectral+action/heat-trace/cosmo tokens; door 1 written as dim
  g_light).
