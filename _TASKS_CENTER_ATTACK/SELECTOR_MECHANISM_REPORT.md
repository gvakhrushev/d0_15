# SELECTOR_MECHANISM_REPORT — consolidation of the D0 within-zone selector search

**Status:** DRAFT consolidation (audit, not merge). **No registry row minted, no cert added, no `.lean` edited, no `053040` row touched.** One candidate registry row is *proposed* below (DRAFT) for minting only via `04_VERIFICATION/VERIFIED_CLOSURE_PROTOCOL.md`.
**Date:** 2026-07-05.
**Scope:** the four center-attack selector arms — DYNAMICAL (attractor), BASEPOINT (ω₀-propagation), SSB (spontaneous symmetry breaking / vacuum extremum), OBSTRUCTION (equivariant torsor-section cohomology) — each already forged → independent-skeptic'd → repaired. This report does not re-run the arms; it consolidates them and adjudicates the **meta-question**: *is there an OWNED, M1-legal mechanism that internally provides the canonical within-zone labeling of K(9,11,13)?*

**Meta-verdict (one line):** **NO owned M1-legal internal selector exists.** The equivariant class is a decidable theorem-grade impossibility; every non-equivariant/SSB/dynamical/basepoint evader **relocates the M1 catalog** rather than escaping it, and any datum that *would* select is, by C1, a privileged within-zone vertex = ⊥M1. **The honest closure for every downstream frontier (GAP-E, Rule-R, lane-A / Ξ / Dirac) is a FORCED explicit external bridge** — forced *by the relocation test*, with one narrow reopening hook that survives (a non-class-function owned SSB primitive / an owned graph-side identification of ω₀ with an ordered shell).

---

## 1. The load-bearing common root (why all four arms share one wall)

All four arms terminate at the **same owned contract**, C1 (BOOK_01:1570, verbatim on disk):

> **(C1) Exchangeability.** No permutation inside a part may change the physics, i.e. the adjacency matrix `A` is invariant under `S9 × S11 × S13`. A part-internal exception would name a privileged vertex — an exogenous parameter — violating M1.

Strengthened at BOOK_01:1576: "From (C1), `A` is constant on the orbits of `S9 × S11 × S13`." Plus the graph is **complete between zones** (all-to-all, DEF 17.0.2, BOOK_01:1588-1592) and `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃` acts as a **direct product** (BOOK_01:1518; cert `vp_raw_self_reading_actual_aut_group.py:25`; Lean `D0.SelfReading.RawHistoryCategory`).

Everything a selector could be built from — the adjacency A, the Laplacian L = D−A, the Feshbach projectors P/Q, the heat trace, the spectral action, the archive RG chain — is a **function of G-invariant data**, hence a **G-class function**. A G-class function cannot have a unique non-symmetric minimizer; and a direct-product factor with all-to-all coupling cannot be broken by fixing data in another factor. That single fact is the wall each arm hits from a different direction.

---

## 2. Per-mechanism outcome

Outcome vocabulary: **owned-legal** (an internal owned rule picks a unique canonical object, no residual freedom) / **relocates-catalog** (selects, but onto a degenerate manifold whose point-choice is itself the un-owned catalog) / **not-owned** (no owned mechanism of this class found) / **impossible** (decidable no-go for the class).

| Arm | Outcome | Killing owned fact | Residual after the mechanism | Artifact + probe result |
|---|---|---|---|---|
| **DYNAMICAL** (Pisot time-flow attractor) | **not-owned** (relocates on its only live channel) | **Layer separation**: T=[[0,1],[1,-1]] is a 2×2 automorphism on a **separate** integer toral time-layer ℤ², paired against the **rank-3 REVERSIBLE** spatial transport of K(9,11,13); the contracting eigenline v=(1,φ⁻¹) is trapped in the disjoint 2D time-layer (BOOK_06:375, echoed :381). Second independent kill: the owned tick A_{k+1}=φ⁻¹A_k is a **uniform scalar** (BOOK_06:489), which commutes with all of S₉×S₁₁×S₁₃. | Whole S₉×S₁₁×S₁₃-orbit (scalar tick ⇒ orbit attractor, not a point). | `SELECTOR_DYNAMICAL_MEMO.md` + `selector_dynamical_check.py` — 10/10 PASS, exit 0; negative control (per-vertex-distinct weight) genuinely prints SELECTOR-FOUND. **Fact-ledger caveat:** verdict booleans hand-set at lines 69/110 encode audited absences — the citation audit, not the arithmetic, carries the NO-GO. |
| **BASEPOINT** (ω₀ propagates into zones 11/13) | **not-owned** (dies one step *earlier* than relocation — no breaking at all) | Fixing ω₀ constrains only the S₉ factor (→S₈=Stab(ω₀)); the S₁₁ and S₁₃ factors are **untouched and fully transitive** under all-to-all completeness. Computed on the 33-vertex scene: Stab(ω₀)-orbits are 11/11 and 13/13 (**maximal**). Owned NO-GO one categorical level up: oriented Aut transitive on the 1287 triangles (BOOK_04:1399, `D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`, Lean `D0.Matter.DSigmaRoleCycleCarrierNoGo`). | Full S₁₁×S₁₃ (maximal orbit = entire zone); strictly *larger* than a degenerate sub-manifold. | `SELECTOR_BASEPOINT_MEMO.md` + `selector_basepoint_check.py` — rc=0, 4/4 PASS; mutation test injecting a distinction into the LIVE channel collapses orbit 11→1 (falsifiable, not rigged). |
| **SSB** (owned action/energy extremum breaks G, selects a vacuum) | **impossible** for outcome (c) unique-broken-minimizer; the one firing break **relocates-catalog** | **Class-function trichotomy** (Y1+Y2): every owned functional (F1 archive action, F2 log-det feedback, F3 heat trace, F4 A₂ spectral action) is a G-class function of its carrier, so its extrema are either **(a)** G-fixed (no breaking) or **(b)** a degenerate G-orbit; **(c)** a unique non-symmetric minimizer is impossible. Root = C1 (A is G-invariant). | For the only firing break (F2 on the tri-phase U₃): the **full** S₉×S₁₁×S₁₃ within-zone torsor — a Nambu-Goldstone manifold; and U₃ itself is un-owned (TICK S2). | `SELECTOR_SSB_MEMO.md` + `selector_ssb_check.py` — **26 PASS / 2 FAIL** (see §5 EoR-A: the 2 "FAIL"s are a Reynolds-sampling artifact in a *supplementary* general-commutant check, non-load-bearing; the memo's stale "26/26" header should read 26/2). Core class-function no-go and F2 firing (S_fb(U₃)=2.079442, orbit spread 8.9e-16) verified. |
| **OBSTRUCTION** (equivariant torsor-section / cohomology) | **impossible** for the equivariant class (X3a); **not-owned** for any-owned-rule (X3b) | Within-zone labelings of each zone form a **single free-transitive Sₙ-torsor**; the count of Aut-equivariant sections (Sₙ-fixed bijections) = 0 for n≥2, hence 0 jointly over S₉×S₁₁×S₁₃. An Sₙ-invariant function Vₙ→Lₙ is constant on the single vertex-orbit ⇒ not injective (the invariance wall). | Equivariant class: 0 sections (decidable). Any-owned-rule: every inspected evader relocates; strongest evader ω₀ shrinks S₉ only to a residual torsor (Stab=S₈=40320, or Aut(Q₈)=24 via owned Ω₈≅Q₈, BOOK_01:780-802) — never to a unique labeling. | `SELECTOR_OBSTRUCTION_MEMO.md` v1 + `selector_obstruction_check.py` — 25/25 PASS, exit 0 (enumeration n≤4 + simply-transitive theorem for n=9,11,13). X3b is honestly scoped "no owned mechanism found + all inspected evaders relocate," **not** a universal impossibility theorem; obstruction stated as section-non-existence, not a computed H¹ cocycle. |

---

## 3. The SSB-vs-obstruction interplay (does the obstruction impossibility leave the other arms alive or dead?)

This is the crux the meta-question turns on. The obstruction arm proves a **decidable impossibility for exactly one class** — the **Aut-equivariant** selectors (X3a). That scope does **not** by itself kill SSB, dynamical, or basepoint, because those are proposals for a **non-equivariant** rule (an SSB vacuum, an attractor, a marked basepoint) that could in principle break G. So the equivariant no-go alone leaves the other three **formally alive**. The real question is whether any of them delivers a *legal* break.

The answer, consolidated across the three: **they are alive as proposals but dead as selectors**, and they die for the *same reason* the equivariant class is impossible — one meta-level up:

- **The equivariant no-go and the class-function SSB no-go are the same wall.** An owned SSB action is a **G-class function** (SSB Y1), so its broken extremum is *always* a G-orbit (outcome (b)), never a unique point (outcome (c)). Outcome (c) would require an action built from **non-G-invariant** data — but any such datum is a privileged within-zone vertex, i.e. ⊥M1 by C1. So SSB does **not** add a new escape hatch; it **re-expresses the obstruction as the degeneracy of the vacuum manifold**. The obstruction's "0 equivariant sections" and SSB's "broken extremum is a Goldstone orbit" are two readings of the identical fact.

- **Dynamical and basepoint are the *degenerate* corners of that same picture.** The dynamical tick is a **uniform scalar** — the maximally-symmetric special case of an owned action, whose attractor is the *whole* orbit (outcome (b) at its most degenerate). The basepoint fixes one S₉-vertex and dies *one step earlier* than (b): it never breaks S₁₁×S₁₃ at all (outcome closer to (a) on those zones). Neither escapes; both land inside the manifold the obstruction arm already quantified.

**Net interplay verdict:** the obstruction arm's impossibility is *narrow* (equivariant-only) but its **root (C1 ⇒ class-function)** is *wide* and is what actually kills the other three. The three non-equivariant arms are not left alive by the narrow scope — they are independently closed by the **relocation test**, and each relocation is a shadow of the same C1 wall. **No arm survives as a legal selector; every arm that could select must import a non-G-invariant datum, which is definitionally the external catalog.**

---

## 4. Decisive meta-verdict

**A legal (owned, M1-internal) within-zone selector does NOT exist.** Specifically:

1. **Equivariant selectors: IMPOSSIBLE** (decidable, theorem-grade). 0 sections; free-transitive Sₙ-torsor. This is the one arm that is a clean impossibility, not merely a null search.

2. **Any-owned-rule selector (incl. SSB / dynamical / basepoint): M1-FORBIDDEN-by-relocation.** No owned mechanism found; every inspected evader relocates the catalog onto a residual manifold (full S₉×S₁₁×S₁₃, or S₁₁×S₁₃, or S₈/Aut(Q₈)) whose point-choice is exactly the un-owned per-vertex datum C1 forbids. A datum that *would* select is a privileged vertex = ⊥M1. This is closed as **FORCED-EXTERNAL-BY-RELOCATION-TEST**, *not* as a universal impossibility theorem — the honest distinction the obstruction repair insisted on.

3. **Therefore the honest closure for the downstream frontiers is a FORCED explicit external bridge.** GAP-E (exhaustiveness), Rule-R (membership; `RULE_R_MEMBERSHIP_MEMO.md:14,47,199` explicitly names "the C1-forbidden graph-slot attachment" and "the full within-zone relabeling torsor S₉×S₁₁×S₁₃" as its exact blocker), and lane-A / Ξ / Dirac all converge on the *same* missing object: a canonical per-slot within-zone labeling. That object is M1-forbidden internally, so each frontier's correct closure is an **EXTERNAL-THEOREM-APPLIED / BRIDGE** row (external owner supplies the labeling as a declared assumption), not a claimed internal derivation.

**Still-open residual (the exact next probe).** The verdict is "no owned selector found + relocation forces external," which by construction is falsifiable. It reopens iff owned text exhibits **any one** of:
- **(a)** a linear/affine map carrying the spec(T)-eigenline or the Adler–Weiss symbol sequence **into** a within-zone V_z (dynamical hook);
- **(b)** a **per-vertex-distinct** (non-scalar) tick weight on some V_z (dynamical/SSB hook);
- **(c)** a **non-Sₙ-equivariant** transport U_N or archive projection P acting **inside** a zone (basepoint/obstruction hook);
- **(d)** an owned **graph-side** identification V₉^graph = Ω₈⊔{ω₀} with an **ordered** shell (the A2 obstruction hook — BOOK_01:1987 "first addressable graph-birth shell" vs :778/:1541 pre-graph reading is a genuine *unadjudicated* corpus-layer tension; but note that even if resolved graph-side, it fixes **one** vertex and leaves the S₈/Aut(Q₈)=24 residual torsor, so it does **not** yield a unique full labeling — demoted to non-reopening for full-labeling selection);
- **(e)** a **non-class-function** owned SSB primitive outside {archive action, log-det feedback, heat trace, A₂ spectral action} (SSB A3 hook).

**The single sharpest next probe:** resolve hook (d)/(e) jointly — grep the corpus for any owned functional or transport that is *not* a class function of S₉×S₁₁×S₁₃ (i.e. reads individual within-zone vertices), and adjudicate whether BOOK_01:1987's "first addressable graph-birth shell" ordering is owned graph-side structure or narration. If both come back negative (as the P1–P8 / four-functional sweeps suggest), the external bridge is closed as forced with no live hook.

---

## 5. Registry / bridge-ledger proposal (DRAFT — do not mint without VERIFIED_CLOSURE_PROTOCOL)

**Proposed consolidated candidate row** (memo-only; mint only via `04_VERIFICATION/VERIFIED_CLOSURE_PROTOCOL.md`, after a skeptic pass):

```
claim_id:  D0-WITHINZONE-SELECTOR-M1FORBIDDEN-EXTERNAL-FORCED-001
book:      BOOK_01/04/06/07 (center-attack consolidation)
section:   §05.8.R selector-mechanism search
lean_status:   (none — meta/no-go consolidation; equivariant sub-no-go is the only theorem-grade arm)
release_status: DRAFT
uses_bridge_assumptions: True
assumption_ids: ASSUMP-WITHINZONE-LABELING-EXTERNAL   (NEW, DRAFT — the external owner supplies the canonical per-slot within-zone labeling)
python_cert:  selector_obstruction_check.py (equivariant no-go, 25/25);
              selector_ssb_check.py; selector_basepoint_check.py; selector_dynamical_check.py
notes:  No owned M1-legal within-zone selector. Equivariant class IMPOSSIBLE (0 sections,
        free-transitive Sn-torsor). SSB/dynamical/basepoint all RELOCATE the catalog
        (Goldstone orbit / scalar-tick whole-orbit / full S11xS13). Downstream frontiers
        (GAP-E, Rule-R, lane-A/Xi/Dirac) closed as EXTERNAL-THEOREM-APPLIED/BRIDGE.
        Reopening hooks (a)-(e) in SELECTOR_MECHANISM_REPORT.md §4.
```

**Bridge-ledger action:** register `ASSUMP-WITHINZONE-LABELING-EXTERNAL` as a declared external-owner assumption consumed by the Rule-R, GAP-E, and lane-A/Ξ/Dirac rows. Those rows should carry `uses_bridge_assumptions=True` with this assumption id, matching the registry's existing `BRIDGE` / `EXTERNAL owner` vocabulary (registry: `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`; edit the source + regen `theory_status_map.csv`/`theory_graph.json`, never the generated files). **Not minted this pass.**

**Errors of record (carried, non-verdict-affecting):**
- **EoR-A (SSB probe, NEW this consolidation):** `selector_ssb_check.py` reports **26 PASS / 2 FAIL**, not the memo header's "26/26". The 2 FAILs are the two *supplementary* general-commutant checks (lines 271-276): `reynolds_average(M, samples=400)` averages only 400 random samples of a group of order ~10¹⁹, so `Ugen` is an **approximate** (not exact) commutant projector — hence `commutes=False` and `||P Ugen Q||≈0.50` are **sampling noise**, not a real trivial↔std P↔Q cross-block. The exact statement (R1 cert `vp_root_r1_representation_reconstruction.py:2`: commutant dim 12, no cross-block ⇒ PUQ=0 for every equivariant U) is the load-bearing one and **stands**; the core F2 no-go does **not** depend on these two checks. *Recommend:* replace the 400-sample Reynolds with an exact block-projector build, or relabel the two checks as a known-approximate diagnostic and correct the memo header to 26/2.
- **EoR-B (dynamical):** `selector_dynamical_check.py` verdict booleans hand-set at lines 69/110 encode audited absences; the citation audit, not the arithmetic, carries the NO-GO (already disclosed by the memo).
- **EoR-C (obstruction):** residual-torsor figures (Stab(ω₀)=8!=40320, Aut(Q₈)=24) are asserted in prose but **not yet machine-checked** in `selector_obstruction_check.py` — candidate can-fail hardening, non-blocking.
- **EoR-D (basepoint, FIXED):** phantom secondary cite "BOOK_01 §05:411" repointed to the real owner BOOK_04:1399 in the memo.

---

## 6. One-paragraph consolidation

Four independent attacks (dynamical attractor, basepoint propagation, SSB vacuum, equivariant obstruction) on the missing canonical within-zone labeling of K(9,11,13) all terminate at the single owned contract C1 (A is S₉×S₁₁×S₁₃-invariant, all-to-all completeness, Aut a direct product). The **equivariant** class is a decidable theorem-grade impossibility (0 sections, free-transitive Sₙ-torsor). Every **non-equivariant** evader — an owned SSB action (always a G-class function ⇒ broken extrema are Goldstone orbits), the scalar Pisot tick (whole-orbit attractor), the marked basepoint (fixes S₉ only, never touches S₁₁×S₁₃) — **relocates** the catalog onto a residual symmetry manifold whose point-choice is exactly the un-owned per-vertex datum C1 forbids. No owned datum can select without being a privileged within-zone vertex, which is ⊥M1 by definition. **The selector is therefore M1-forbidden, and the honest closure for GAP-E / Rule-R / lane-A / Ξ / Dirac is a FORCED explicit external bridge** (`ASSUMP-WITHINZONE-LABELING-EXTERNAL`), with five narrow, pre-registered reopening hooks — the sharpest being an owned non-class-function functional or an owned *ordered* graph-side shell identification of ω₀ — none of which the current owned sweep exhibits.
