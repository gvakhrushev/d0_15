# CLOSING FORGE — matter-sector no-go cluster (construction campaign)

**Goal:** genuinely CLOSE matter-sector no-gos by CONSTRUCTING the missing object from owned
material — not another boundary catalogue. Boundary is the fallback only after real construction
attempts fail.

**Date:** 2026-07-06. No git commit; no registry/book/`.lean`/`053040` edits. Row-notes + Lean
skeletons PROPOSED only. Companion can-fail check: `_TASKS_CENTER_ATTACK/close_matter_check.py`
(14 base checks PASS, 3 mutants KILL). Skill: `d0-adversarial-forcing-loop`.

**Background verified on disk:** `DEEP_M_GENMASS_MEMO.md`, `DEEP_M_COLOUR_HIGGS_MEMO.md`,
`DEEP_M_LEPTON_DECIMALS_MEMO.md`. The whole matter sector is ONE carrier-count wall + a single
external import (the third-generation label / winding `W`).

---

## Executive scoreboard (per target)

| # | Target | Verdict | No-gos reduced |
|---|--------|---------|----------------|
| 1 | third-generation = third-zone | **PARTIAL-CLOSED (reframe, no count drop)** | 0 count; 1 mis-statement corrected |
| 2 | winding `W` from owned pieces | **PARTIAL-CLOSED (order owned, value external)** | 0 count; residue sharpened to metric-only |
| 3 | colour 1-dim deficit as owned | **FAILED-BOUNDARY** | 0 |
| 4 | non-commuting `Q0` from zone off-diagonal | **FAILED-BOUNDARY (carrier mismatch)** | 0 |

**Net:** 0 no-gos drop from the count. Two are genuinely SHARPENED (T1 corrects a false
"existence-wall" framing; T2 splits the residue into owned-order vs external-metric). This is an
honest result: the anti-over-claim record (colour "forced", Higgs "flagship", both burned) is
respected — no construction is manufactured that secretly imports the datum it claims to derive.

---

## Owned material inventory (verbatim, file:line, read past ±10)

**Zone carrier (three shells = three zones).**
- `D0/Geometry/TorusCore13GeometryOrigin.lean:59-63` `inductive TorusShell | innerD9 | coreD11 | outerD13`;
  `:65-67 torus_shell_card_eq_three : Fintype.card TorusShell = 3` (`decide`).
- `D0/Geometry/TorusShellAttachment.lean:46-49` `TorusShell.zoneSize : {9,11,13}`;
  `:52-55 zoneDegree : {24,22,20}`; `:57-60 torusShell_degree_law : zoneDegree = 33 − zoneSize`;
  `:62-66 torusShell_zoneSize_ladder` (the `+2` ladder); `:84-95 torusShell_radius_strictMono`
  (radii `1 < (a+1)/2 < a` for every `a>1`). **This file is a DRAFT attachment** (header: "lives in
  `_TASKS_CENTER_ATTACK` until minted"), so the zone data is attached to the generation carrier but
  NOT YET minted.

**Projective generation carrier (the OTHER 3).**
- `D0/Defect/Basic.lean:17` `BranchRay = {v : F₂² // v ≠ 0}` (3 nonzero vectors = `P¹(F₂)`);
  `:22 defectAction v = (v.2, v.1+v.2)` (Fibonacci/golden action, order 3).
- `D0/Spectrum/BranchDefectProjectiveGeneration.lean:52-53 exactly_three_projective_branch_defect_generations`;
  `:66-68 defect_generation_card = 3` (`rfl`). Registry `CLAIM_TO_LEAN_MAP.csv:36` `D0-GEN-INDEX-001`
  CORE-FORMALIZED.

**The two "3"s are NOT proven isomorphic.** Hard grep: there is NO Lean equivalence
`TorusShell ≃ BranchRay`. The only cross-link is prose: `04.6.M1.gen` (`0008__04.6…:146`) calls the
zone-3 "the structural complement to the `F₂` branch-defect generation index." Two independent
count-3 carriers, linked only in the book.

**The generation-3 is RANK-ONLY (decisive).** `CLAIM_TO_LEAN_MAP.csv:460` (`D0-REP-RECONSTRUCTION-…-NOGO-001`,
R1) verbatim: "the generation count 3 = trivial-isotype multiplicity is RANK-ONLY: commutant block
9>1 (GL(3) basis freedom) ⇒ Weyl-role assignment unforced (≥2 admissible)"; T1-UPLIFT: "commutant =
flavor-frame algebra `End(generation space) ⊕ ℂ³`". So the zone-3 does **not** canonically
distinguish the three generations either — it owns the DIMENSION, not the LABELLED basis.

**The lepton wall (verbatim).** `D0/Extensions/LeptonBranchFixingNoGo.lean:30-33` `numBranches=2`,
`numGenerations=3` (the `3` is the hardcoded def `LeptonSelectorExtension.lean:23 numGenerations := 3`
= the imported zone count, NOT a lepton count); `:41 shell_no_fixed_point`; `:45-55` the three
pigeonhole `decide` no-gos. **The wall is the branch→generation ROW, not third-gen existence.**

**Mass ontology.** `04.6.π.5` (`0008__04.6…:92`): `m_0 = 2π_0 = (12/5)φ²`, `t_0 = (5/12)φ⁻²`,
`m_0·t_0=1` exact in `Q(φ)` (cert `vp_mass_chain_alpha.py`). `04.6.π.6` (`:96`) verbatim: "the
per-particle `W` values are a physical input (a passport/bridge), not core theorems … `W` is not
recovered from any internal derivation."

**Colour.** `vp_colour_generation_typed_carrier_nogo.py:85-87,99-103`: typed collapse
`Comm(diag(24,22,20)) = ℂ³` (dim 3); commutant gap `dim R(Q₈)=8 < 9 = dim M₃(ℂ)`. The deficit is
`9−8=1`.

**Higgs.** `vp_higgs_phason_orbit_nontriviality.py:34-42` + maximality `tPoly_commutes`: a frozen
non-commuting `Q0` with `[T,Q0]≠0` on the **return operator `T` over `ZMod 44`** is required; every
present-core projector is a polynomial `a·1+b·T` and commutes. The generation algebra `⟨D_zone,S_zone⟩`
(`04.10:121`) is prose-only, "qualitative, downstream of F6", NOT in Lean.

---

## TARGET 1 — third generation = third zone? (dissolve the 2<3 existence wall)

### Construction attempt
Make the generation carrier the **zone carrier** `TorusShell = {innerD9, coreD11, outerD13}` (owned,
`torus_shell_card_eq_three`), with the radial order `inner < core < outer` = `e < μ < τ`
(`torusShell_radius_strictMono`). The claim to test: if generations are the three zones, then the
third generation EXISTS in-carrier (it is `outerD13`), so the "2<3 third-branch existence wall"
(DEEP_M framing) DISSOLVES — it was the wrong carrier (the 7-point lepton branch carrier, which only
ever had 2 orbits).

### What actually closes, what does not
1. **The reframe is CORRECT and is a genuine correction.** On disk, `numGenerations := 3` is a
   *hardcoded def* imported into the lepton no-go from the zone count (`LeptonSelectorExtension:23`;
   `LeptonBranchFixingNoGo:33` `numGenerations_eq_three := rfl`, cross-checked to `Tr(T²)=3`). The
   left side of `2<3` is therefore ALREADY the zone-owned 3, and the third generation already EXISTS
   as `outerD13`. **The wall is NOT about third-generation existence.** DEEP_M's phrasing
   ("2<3 third-branch existence wall", GENMASS §(d/e)) over-reads it. The precise wall is the
   **branch→generation ROW**: which of the 2 lepton branch-orbits `{4-cycle, 3-cycle}` maps to which
   of the 3 zone-generations. That row needs an injection/surjection/bijection between a 2-set and a
   3-set — impossible by cardinality (`LeptonBranchFixingNoGo:45-55`).

2. **But relocating to the zone carrier does NOT supply the row, and does NOT close the no-go.**
   Two independent kills:
   - **(K1) The zone-3 is RANK-ONLY** (`csv:460`, R1, on disk): the three zone-lines carry a
     `GL(3)` basis freedom (commutant block `9>1`), so even the ZONE carrier does not canonically
     LABEL its three generations — it owns `dim = 3`, not a distinguished `(e,μ,τ)` basis. So moving
     to the zone carrier does not give a canonical third-generation datum; it inherits the same
     under-determination one level up.
   - **(K2) No owned iso `TorusShell ≃ BranchRay`.** The construction would need to identify the
     zone-3 with the branch/lepton generation index to transport any lepton data (exponents `1/4,1/3`)
     onto it. That iso is NOT owned (prose-only link, `04.6.M1.gen`). Asserting it would SMUGGLE the
     branch→generation row it claims to derive — exactly the forbidden move.

### Verdict — PARTIAL-CLOSED (reframe, no count drop)
The third-generation-EXISTENCE reading of the wall is **retired** (it was the wrong carrier and a
DEEP_M over-statement). The surviving, correctly-stated wall is the branch→generation ROW
(`PRIM-LEPTON-BRANCH-FIXING-OPERATOR`), which the zone carrier does NOT close — it is RANK-ONLY (K1)
and needs an unowned iso (K2). **No no-go count drops.** The gain: the cluster's headline wall is
now correctly named (row-not-existence), and the false "third generation is external" reading is
replaced by "third generation EXISTS as `outerD13`; its *labelled coupling to the lepton branch
data* is external."

---

## TARGET 2 — winding `W` from owned pieces (zone index + `τ⁻¹` + `m₀·t₀=1`)

### Construction attempt
`m_rest = m_0·W`, `W` = memory-winding count. Attempt: `W = W(zone index, branch weight)` assembled
from owned pieces — the zone carrier supplies a strictly-increasing radial order
(`torusShell_radius_strictMono`: `radius(inner)=1 < radius(core)=(a+1)/2 < radius(outer)=a`), and the
branch weights `(φ⁻¹, φ⁻², gap=2δ₀)` are derived (`pPlus_add_pMinus`, `branchGap_eq_two_delta0`). If
`W` is a monotone function of the radial order, the winding's STRUCTURE (its ordering) is owned even
if the decimal value is not.

### What actually closes, what does not
1. **The ORDER is owned.** The zone carrier gives a total order `e < μ < τ` (radii strict-mono for
   *every* admissible `a>1`, so the order is parameter-free). A winding section must satisfy
   `W(e) < W(μ) < W(τ)` — the SIGN of every gap is owned. This is real structure the passport line
   `04.6.π.6` does not state: `W` is not merely "external", it is a **monotone section of the owned
   radial order**.
2. **The VALUE is provably not owned.** A monotone integer section of a 3-chain is NON-UNIQUE: fixing
   `W(e)=1`, any `1<W(μ)<W(τ)` works (infinitely many). The strict order fixes gap SIGNS, never gap
   SIZES. There is no owned metric on `TorusShell` that would pin the integer winding counts (the
   radii `1,(a+1)/2,a` depend on the free parameter `a`, and no owned rule fixes `a`). This matches
   the memory prior verbatim (mass ratios = terminal-passport) and the DEEP_M split (count/ontology
   in, winding/spectrum out).
3. **Adversarial (kill-target): does the branch-weight triple `(φ⁻¹,φ⁻²,gap)` secretly give `W`?**
   No. The triple lives on the 2-BRANCH defect plane (`Pi0BranchDefect`), and is a set of DEFECT
   weights summing to 1 (`pPlus_add_pMinus`), not a winding-count section over the 3 generations. It
   is 2-valued+gap, not a 3-generation metric; and by TARGET 1 (K2) there is no owned iso to transport
   it onto the zone-3. Assembling `W` from it would import the missing row. KILLED as a closure.

### Verdict — PARTIAL-CLOSED (order owned, metric external)
The winding's ORDER-STRUCTURE `W(e)<W(μ)<W(τ)` is CONSTRUCTED from the owned radial monotonicity
(new, not previously assembled). The winding's METRIC (integer values) is provably external — no
owned rule fixes the gaps or the torus parameter `a`. **No no-go count drops**, but the residue of
`D0-GEN-MASS-001` is SHARPENED: not "W is unrecovered" (all-or-nothing), but "W's monotone order is
owned; only its metric section is a passport." Exact minimal missing object: **a scene-forced metric
on `TorusShell` (equivalently, a forced value of the torus parameter `a`) that upgrades the owned
order to integer winding counts.**

---

## TARGET 3 — colour 1-dim deficit `9−8=1` as an owned object?

### Construction attempt
DEEP_M found `8<9` is generation-distinctness (one M1 mechanism). Attempt: is the deficit `9−8=1`
CONSTRUCTIBLE as an owned scene object (the `ω₀` basepoint? the extra generation-distinctness
dimension?) so colour's carrier partially closes without the external `⊗ℂ³`?

### What actually closes, what does not
1. The arithmetic is exact and owned: `dim M₃(ℂ)=9`, typed collapse `Comm(diag(24,22,20))=ℂ³`
   (dim 3), weak commutant ceiling `dim R(Q₈)=8`. Deficit `= 1`.
2. **The deficit is NOT an owned scene scalar.** Hard grep: there is no owned `ω₀` basepoint object
   in the matter Lean layer (no hit in `D0/Matter/*.lean` or `RawZone.lean`). The tempting
   identification "deficit = the extra generation-distinctness dimension" fails numerically: the
   generation algebra is `ℂ³` (dim 3), and `1 ≠ 3` — the 1-dim seam is not the generation line count,
   nor any owned scene scalar. The `1` is exactly `dim M₃ − dim R(Q₈)`, i.e. the width of the gap
   between what the terminal spinor carrier `ℂ⁸=ℂ[Q₈]` owns (8) and what a non-abelian colour `M₃`
   needs (9). That gap is DEFINED by the external `⊗ℂ³` = `𝒜_F` completion `ℋ_q=W₃⊗V₂` — it is the
   interface, not an owned filler.
3. Consistent with verified memory (`colour-su3-not-derived-in-d0`): colour is terminal-passport
   (Mordell/Furey octonion/E8 route), never scene-native.

### Verdict — FAILED-BOUNDARY
The 1-dim deficit is NOT owned; it is the exact width of the external colour seam. Exact minimal
missing object: **the external `⊗ℂ³` = `𝒜_F` completion `ℋ_q=W₃⊗V₂`** (terminal-passport). No
construction; boundary confirmed (as the prior predicted). No no-go reduces.

---

## TARGET 4 — non-commuting `Q0` from the owned zone off-diagonal?

### Construction attempt
Higgs condensation needs a frozen non-commuting `Q0` with `[T,Q0]≠0` (Wall 1). Attempt: construct
it NOT via the fork-open central-extension route, but from the owned zone off-diagonal — the
generation algebra `⟨D_zone, S_zone⟩` (`04.10:121`) has `[D_zone, S_zone] ≠ 0` (structural family
mixing), and the zone commutator generator `J = i[D_W, A_W]` (`RawZone.lean:60-147`) is a genuine
non-commuting owned object. If either supplies `[T,Q0]≠0`, one Higgs wall falls.

### What actually closes, what does not
1. `[D_zone, S_zone] ≠ 0` is real (check T4: commutator entry `(0,1) ~ (24−22)·√(n₀n₁) ≠ 0`), and
   `RawZone.lean` owns a non-commuting `J` with `comm³ = −2840·comm`.
2. **CARRIER MISMATCH — the decisive kill.** The Higgs wall requires `[T, Q0] ≠ 0` where `T` is the
   **return operator over `ZMod 44`** and `Q0` a **frozen idempotent projector** on that carrier
   (`vp_higgs_phason_orbit_nontriviality.py`, maximality `tPoly_commutes` over `ZMod 44`). But:
   - `S_zone` / `D_zone` live on the **`Fin 3` generation carrier** (degree frame), a DIFFERENT
     carrier from `ZMod 44`. Non-commuting there does nothing for `[T, Q0]`.
   - `J = i[D_W,A_W]` from `RawZone` lives on the **zone/active-neutral split of `ℂ³³`**, again not
     the `ZMod 44` return operator, and is a commutator GENERATOR, not a frozen idempotent projector
     `Q0`.
   - `⟨D_zone,S_zone⟩` is moreover prose-only ("qualitative, downstream of F6"), NOT a minted Lean
     frozen projector.
   This is exactly the failure mode that already killed the TorusCore13 candidate
   (`J2_HIGGS_NONCOMMUTE_CHECK.md`, five mismatch axes). The zone off-diagonal reproduces the SAME
   carrier-mismatch kill: right kind of object (non-commuting), wrong carrier (`Fin3`/`ℂ³³` vs
   `ZMod 44`), wrong type (generator/algebra vs frozen idempotent).
3. Even if a carrier bridge existed, DEEP_M's Wall 2 (`z²≥0` never-SSB) remains — `Q0` is
   NECESSARY-BUT-NOT-SUFFICIENT.

### Verdict — FAILED-BOUNDARY (carrier mismatch)
No owned non-commuting object lives on the `ZMod 44` return-operator carrier as a frozen idempotent.
Exact minimal missing object: **a frozen idempotent `Q0` on `ZMod 44` (or a forced carrier bridge
`Fin3/ℂ³³ → ZMod 44`) with `[T,Q0]≠0`** — plus the second (negative-sign) import for Wall 2. No
construction; Higgs stays a SHARPENED OPEN SLOT (unchanged from DEEP_M). No no-go reduces.

---

## §05.8.R — INDEPENDENT SKEPTIC PASS (kill-mandate)

Mandate: find the SMUGGLED external datum in any claimed closure. A closure that imports the
winding/label it claims to derive must be KILLED.

**T1 (reframe).** *Kill attempt: "you claim to dissolve a wall — that IS a closure, so you must have
smuggled the row."* NOT SUSTAINED: T1 explicitly does NOT dissolve the wall. It reclassifies WHICH
wall (row, not existence) and then proves the zone carrier does NOT close the row (K1 rank-only,
K2 no owned iso). The verdict is PARTIAL-CLOSED (reframe) with **0 count drop** — no closure is
claimed, so nothing is smuggled. The correction (existence→row) is backed by the hardcoded
`numGenerations := 3` def on disk. ACCEPT.

**T2 (order owned).** *Kill attempt: "monotone order + branch weights = you have `W`; you smuggled
the metric."* SUSTAINED-AS-SCOPE, not a kill: T2 claims ONLY the order (gap signs), and explicitly
proves the metric (gap sizes / parameter `a`) is external and the branch triple cannot supply it
(§2.3 kill). The order-claim imports nothing (radial mono holds for all `a>1`). The residue is
correctly the metric. ACCEPT (no over-claim: `W`-value is NOT claimed derived).

**T3 (deficit).** *Kill attempt: "you dressed an absence as a boundary."* NOT SUSTAINED: the deficit
`=1` is positively identified as `dim M₃ − dim R(Q₈)` = the external seam width, with the `ω₀`/
generation-scalar identifications numerically refuted (`1≠3`, no owned `ω₀`). Owner-asserted external
(Mordell/Furey). ACCEPT.

**T4 (Q0).** *Kill attempt: "you rejected a real owned non-commuting object too quickly."* NOT
SUSTAINED: the objects ARE non-commuting but on the WRONG carrier (`Fin3`/`ℂ³³` vs `ZMod 44`) and
wrong type (generator/prose-algebra vs frozen idempotent), reproducing the already-owned
`J2_HIGGS_NONCOMMUTE_CHECK.md` kill. Wall 2 independently survives. ACCEPT.

**Skeptic verdict: NO-KILL on any of the four verdicts.** No closure smuggles the winding/label.
Two PARTIAL reframes (T1, T2) drop 0 count but are honest sharpenings; two FAILED-BOUNDARY (T3, T4)
confirm the priors. The cardinal sin (a manufactured derivation of the third-gen label, the winding
value, colour `M₃`, or a frozen `Q0`) is ABSENT.

---

## Proposed row-notes (PROPOSALS ONLY — no CSV/book edits made)

**`D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001`** (`csv:491`, append):
> [CLOSE-MATTER reframe] The wall is the branch→generation ROW, not third-generation EXISTENCE: the
> `3` in `2<3` is the zone-owned count (`numGenerations := 3`, = `Tr(T²)=3` / `TorusShell` card), and
> the third generation EXISTS in-carrier as the third zone `outerD13`. Relocating the generation
> carrier to `TorusShell` does NOT close the row — the zone-3 is RANK-ONLY (`csv:460`, GL(3)
> freedom) and there is no owned iso `TorusShell ≃ BranchRay`, so transporting lepton branch data
> would smuggle the row. Existence-wall reading retired; row-wall reading stands.

**`D0-GEN-MASS-001`** (`csv:37`, append):
> [CLOSE-MATTER sharpen] The winding `W` in `m_rest=m_0·W` has an OWNED order-structure:
> `W(e)<W(μ)<W(τ)` from the parameter-free radial monotonicity `radius(inner)=1 < (a+1)/2 < a`
> (`TorusShellAttachment.torusShell_radius_strictMono`). Only the METRIC (integer values / torus
> parameter `a`) is external — a monotone section of a 3-chain is non-unique. Residue sharpened from
> "W unrecovered" to "W-order owned, W-metric = passport". Exact missing object: a scene-forced
> metric on `TorusShell` (forced `a`).

**`D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`** (`csv:528`, append):
> [CLOSE-MATTER] The `9−8=1` colour deficit is NOT an owned scene object (no owned `ω₀`; `1≠3`=gen
> dim). It is exactly the external seam width `dim M₃ − dim R(Q₈)` = the `⊗ℂ³=𝒜_F` completion
> (terminal-passport). Deficit-construction attempted and failed; boundary confirmed.

**`D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`** (`csv:397`, append):
> [CLOSE-MATTER] Zone-off-diagonal `Q0` route attempted: `[D_zone,S_zone]≠0` (Fin3) and `J=i[D_W,A_W]`
> (`RawZone`, ℂ³³) are genuinely non-commuting but on the WRONG carrier (not `ZMod 44` return
> operator) and wrong type (generator/prose-algebra vs frozen idempotent) — same carrier-mismatch
> kill as `J2_HIGGS_NONCOMMUTE_CHECK.md`. Higgs stays SHARPENED-OPEN-SLOT (Wall 2 also survives).

---

## Proposed Lean skeleton (PROPOSAL ONLY — the ONE object worth minting)

The DRAFT `TorusShellAttachment.lean` is the honest carrier plumbing for T1/T2 (zone data attached
to the generation carrier). The one NEW owned lemma this campaign would add is the **generation
radial order** as the winding's owned skeleton:

```lean
-- proposed: D0/Matter/GenerationWindingOrder.lean  (skeleton, not minted)
namespace D0.Matter
open D0.Geometry
/-- The generation carrier carries a parameter-free strict order e<μ<τ (owned radial monotonicity).
    This is the OWNED skeleton of the winding W in m_rest=m_0·W; the metric (integer W values) is
    NOT owned (a monotone section of a 3-chain is non-unique). -/
theorem generation_winding_order (T : TorusParameter) :
    TorusShell.radius T .innerD9 < TorusShell.radius T .coreD11 ∧
    TorusShell.radius T .coreD11 < TorusShell.radius T .outerD13 :=
  torusShell_radius_strictMono T
/-- NON-uniqueness witness: two admissible integer winding sections agree on order, differ on value
    (proves the METRIC is external, not the order). -/
example : (1 < 2 ∧ 2 < 3) ∧ (1 < 2 ∧ 2 < 5) := ⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩
end D0.Matter
```

This mints nothing beyond what `TorusShellAttachment` already proves; it re-exports the strict order
as the winding skeleton and records the non-uniqueness as the boundary. Promotion via the closure
protocol only.

---

## Can-fail check

`_TASKS_CENTER_ATTACK/close_matter_check.py` — 14 base checks PASS (exact `Fraction`/integer, no
float on load-bearing facts). 3 mutants KILL: `break_zone_ladder` (T1 +2 ladder), `break_degree_law`
(T1 `33−|zone|`), `break_deficit` (T3 `9−8=1` → pretend `dim R(Q₈)=9`). The mutants prove the check
discriminates the zone-carrier arithmetic and the colour deficit by execution.
