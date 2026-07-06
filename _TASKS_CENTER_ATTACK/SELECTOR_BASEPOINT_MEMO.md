# SELECTOR_BASEPOINT — can the owned basepoint ω₀ propagate a canonical labeling into zones 11/13?

**Verdict (candidate, computed on the scene): NO. The mechanism is DEAD by an owned structural obstruction — the all-to-all completeness of K(9,11,13). ω₀ distinguishes NO vertex and induces NO ordering in zones 11 or 13. This is not a gap to be closed; it is a NO-GO the corpus already owns in two independent places.**

**Status:** DRAFT memo; no registry row edited; no `.lean` added to the built tree; no `053040`/CSV/ledger touched. Companion can-fail probe: `_TASKS_CENTER_ATTACK/selector_basepoint_check.py` — 4/4 checks PASS incl. a negative control proving the probe CAN print a distinction (rc=0). Every owned fact below is verbatim file:line, verified on disk this session.

---

## The question, stated precisely

Zones 11 and 13 have (verified this session) NO owned per-vertex distinction; C1 forbids a privileged vertex there. Zone 9 DOES own one: the marked witness `ω₀`, `V₉ = Ω₈ ⊔ {ω₀}`. **Basepoint-propagation** would be: ω₀ + the owned inter-zone structure (edges, dynamics, ordering) canonically selects a vertex — or a total order — in zones 11/13, thereby DERIVING the 11/13 distinction from the single owned zone-9 basepoint rather than assuming it. If it worked, the missing per-vertex structure of 11/13 would be owned.

## Owned pre-facts (verbatim, file:line — all verified present on disk)

**P1 — ω₀ is a single marked vertex in zone 9.** `BOOK_01 §01.8:867`: "The signed detector cycle must acquire a graph-birth marker: `V_9=\Omega_8+\omega_0`." And `§01.20:1541`: "A reusable shell also requires a stationary marked witness section `ω0`. Hence `V_9=\Omega_8\sqcup\{\omega_0\}`, `|V_9|=9`." (T2-P1; also `SHELL_RULE_R_LEDGER.md:52`.)

**P2 — the scene is COMPLETE tripartite; every zone-9 vertex has IDENTICAL all-to-all connectivity to 11 and 13.** `BOOK_01 §01.20:1588-1592` (adjacency matrix, DEF 17.0.2): the 9×11 and 9×13 blocks are `𝟏` (all-ones), the within-zone blocks are `0`. So ω₀'s edge set to zone 11 = `{all 11 vertices}`, identical to that of every other zone-9 vertex.

**P3 — the automorphism group is `Aut(K(9,11,13)) = S₉ × S₁₁ × S₁₃`, acting componentwise.** `BOOK_01:1518`: "`Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`, and because the zone sizes are *distinct* the induced symmetry on the three zone-classes … is the **trivial** group." Lean/cert owner: `05_CERTS/vp_raw_self_reading_actual_aut_group.py:25` ("Aut = S9xS11xS13 derived from distinct part sizes"), `D0.SelfReading.RawHistoryCategory` (`part_sizes_distinct`, `commutant_dim_raw`). **Note the factor is the FULL `S₉` — not `S₈`.** Even ω₀ is NOT distinguished at the graph-automorphism level (see §"The self-attack" below).

**P4 — C1: a part-internal exception NAMES A PRIVILEGED VERTEX = exogenous parameter = ⊥M1.** `BOOK_01 §01.20:1570`: "(C1) Exchangeability. No permutation inside a part may change the physics, i.e. the adjacency matrix `A` is invariant under `S9 × S11 × S13`. A part-internal exception would name a privileged vertex — an exogenous parameter — violating M1."

**P5 — the corpus's OWN general no-go: a single-vertex reader is not Aut-invariant and NEEDS AN EXOGENOUS LABEL.** `BOOK_04:1392`: "the only `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`-invariant covectors are the three zone-indicators (distinct zone sizes ⇒ no zone swaps) … `Y_{ν^c}` reads a single vertex, is not zone-constant, hence is not `Aut`-invariant and needs an exogenous label." This is the propagation question's answer in general form, already owned.

**P6 — the strongest owned precedent: `Aut` is TRANSITIVE on the 1287 triangles (single orbit), so no canonical per-vertex/per-cycle injection exists.** `BOOK_04:1399` (verbatim, verified on disk): "the **oriented** automorphism group `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃` is transitive on the 1287 triangles (a single orbit) … any rank-5 carrier is an arbitrary symmetry-breaking choice (`D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`, NO-GO, Lean `D0.Matter.DSigmaRoleCycleCarrierNoGo`)." This is a THEOREM-GRADE owned NO-GO of exactly the mechanism class the task probes (an owned inner structure trying to canonically label vertices/cells via edges and triangles). The corpus's phrase "the **oriented** automorphism group" pre-empts an oriented/directed/weighted-edge objection: even the oriented group does not shrink below `S₉×S₁₁×S₁₃`, so no directed structure breaks the `S₁₁`/`S₁₃` factors either (closes G2 more tightly). [Repair 2026-07-05: the earlier stray secondary citation `BOOK_01 §05:411` was DROPPED — line 411 of BOOK_01 is a LaTeX spacing operator (`\quad`), not the transitivity/NO-GO statement; BOOK_04:1399 is the real and sufficient owner.]

**P7 — the owned dynamics (toral flow, archive tracing) live INSIDE zone 9 and are orbit-SYMMETRIC, not vertex-selecting.** `BOOK_01:1993`: "Continuous circulation inside `Ω₈` … closes against `ω₀`; this is the terminal halt quotient." `:1996`: "the emitted archive trace is an orbit-averaged shell emission over the group `G_8` of symmetries of `Ω₈`: `E_Ω = (1/|G₈|) Σ_g P_g F_N P_g†`." An orbit-average is symmetric by construction — it cannot break a symmetry it averages over, and it acts on `Ω₈` (zone 9), never on 11/13 vertices.

**P8 — the "+2 address ladder" and "zone=generation" are ZONE-level, not vertex-level.** `BOOK_01 §01.22:1889`: "the address ladder is forced to advance by `+2` … the step between successive *addresses*" — the addresses are the zones `9,11,13`. `BOOK_04:912`: "The generation index is the zone label `9/11/13` of the minimal scene." The degree/generation operator `D_zone = diag(24,22,20)` (`BOOK_04:1318`) acts on the THREE **zone-lines** — one constant per zone — so all 11 zone-11 vertices share degree 22, all 13 zone-13 vertices share degree 20. There is no owned per-vertex address in 11 or 13.

## The computation (on the actual scene K(9,11,13))

Companion probe `selector_basepoint_check.py` builds K(9,11,13) explicitly, marks `ω₀ = ("9",0)`, and computes the **pointwise stabilizer of ω₀ inside Aut(K)** acting on zones 11 and 13. Result:

```
[PASS] SCENE_INVARIANTS  |V|=33 |E|=359 tri=1287        (owned invariants reproduced)
[PASS] STAB_OMEGA0_TRANSITIVE_ON_Z11  orbit = 11 / 11   (whole zone; no distinction)
[PASS] STAB_OMEGA0_TRANSITIVE_ON_Z13  orbit = 13 / 13   (whole zone; no distinction)
PROPAGATION VERDICT:
  ω₀ distinguishes some zone-11 vertex : False
  ω₀ distinguishes some zone-13 vertex : False
[PASS] NEGCTRL_BROKEN_COMPLETENESS_SPLITS_Z11  orbit = 1 < 11   (probe is not rigged)
```

**Why it is transitive (the mechanical core).** `Aut(K)` is a DIRECT PRODUCT `S₉ × S₁₁ × S₁₃` (P3), and the graph is COMPLETE between zones (P2). Fixing one zone-9 vertex ω₀ constrains only the `S₉` factor (down to `Stab_{S₉}(ω₀) = S₈`); the `S₁₁` and `S₁₃` factors are UNTOUCHED — they still act with full transitivity on zones 11 and 13. Concretely, the transposition `(i j)` inside zone 11, identity elsewhere, (a) is a genuine graph automorphism (both `i,j` are all-to-all connected to 9 and 13, so swapping them preserves every edge) and (b) fixes ω₀ (it lives in a different factor). So any two zone-11 vertices are swappable by an automorphism fixing ω₀ ⇒ ω₀ distinguishes none of them. The negative control confirms the probe is falsifiable: when completeness is artificially broken (ω₀ wired to only one zone-11 vertex), the orbit collapses to `{1}` and the probe DOES print a distinction.

## Directly confronting the task's crux and the DEEP TRAP

**Crux (all-to-all kills edge-propagation).** Confronted head-on and CONFIRMED: because every zone-9 vertex — ω₀ included — has identical connectivity to zone 11, ω₀'s EDGES distinguish no zone-11 vertex. The task asked whether an owned NON-edge structure (dynamics, phase, ordering) rescues it. Every owned candidate was checked:
- **Toral flow / tick archive-tracing (P7):** acts inside Ω₈ (zone 9); its zone-11/13 output is an orbit-AVERAGE over G₈ — symmetric by construction, selects nothing. DEAD.
- **The +2 address ladder / zone=generation (P8):** a ZONE-level (not vertex-level) address; `D_zone` is constant per zone. No per-vertex address exists to propagate. DEAD.
- **The `ν*=1/9`, 9-step cycle `γ*` (`BOOK_01:1909-1914`):** a within-zone-9 addressor (`D=9` positions = the 9 vertices of V₉); it does not carry an ordering onto 11/13. And even if a cycle were posited on zone 11/13, P6 kills it: `Aut` is transitive on triangles, so no canonical cycle-class injection exists.
- **The Q₈ structure on Ω₈:** internal to zone 9 (`Ω₈ ≅ Q₈`); it has no owned action on zone-11/13 vertices.

**DEEP TRAP (degenerate-manifold relocation of the catalog).** Tested explicitly. Even the most generous reading — "ω₀'s dynamics breaks S₁₁ down to some subgroup H ⊊ S₁₁, leaving a degenerate manifold of labelings" — does NOT escape M1: the computation shows H = S₁₁ (no breaking at all), but *had* it been a proper H, picking a single labeling on the residual H-manifold is exactly a catalog (P4: naming a privileged vertex). A legal mechanism must select a UNIQUE canonical object by an internal owned rule. Here the internal owned rule (Aut-equivariance, P5) FORBIDS any non-zone-constant selection. So there is no degenerate-manifold escape hatch either: the orbit is the *entire* zone, the maximal possible degeneracy, and any point-pick on it is external.

## M1 CATALOG TEST (the discipline gate)

Does the mechanism select a UNIQUE canonical object internally, or relocate the catalog to a degenerate manifold? **NEITHER — it selects nothing at all.** The residual freedom after ω₀ is the FULL `S₁₁ × S₁₃` (the whole symmetric group on each zone, orbit = entire zone), which is strictly larger than a degenerate manifold — it is the maximal orbit. Any pick is an external label (P4, P5). The mechanism does not even reach the trap; it is dead one step earlier at the all-to-all wall.

**Oriented-structure objection, pre-empted (closes G2).** "But maybe a directed/weighted/oriented edge structure — not the plain graph — breaks `S₁₁`/`S₁₃`?" No: BOOK_04:1399 owns the stronger fact that even the **ORIENTED** `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃` is transitive on the 1287 triangles. The oriented group does not shrink below the direct product, so no owned oriented/directed/weighted inter-zone structure can break the `S₁₁`/`S₁₃` factors. There is therefore no owned structure — plain or oriented — off the P1–P8 list that could relocate a catalog onto a residual manifold; the residual is the maximal orbit under both the plain and the oriented automorphism group.

## What is OWNED vs INFERRED

- **OWNED (verbatim, verified):** P1 (ω₀ marked, single vertex), P2 (all-to-all completeness), P3 (`Aut = S₉×S₁₁×S₁₃`, Lean+cert), P4 (C1 privileged-vertex = ⊥M1), P5 (single-vertex reader needs exogenous label), P6 (transitive on 1287 triangles = NO-GO, Lean `D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`), P7 (archive emission is a G₈-orbit-average), P8 (address/generation are zone-level).
- **INFERRED (this memo, computed):** that fixing ω₀ leaves `S₁₁×S₁₃` transitive follows immediately from the direct-product structure (P3) + completeness (P2) — verified constructively by `selector_basepoint_check.py`. This is elementary and the corpus's P6 is the same fact one categorical level up.

## Named gaps / honest residuals

- **G1 (not this task's, but adjacent — flagged, not claimed):** the corpus does NOT explicitly reconcile "ω₀ is a *marked* vertex" (P1) with "`Aut` contains the *full* `S₉`" (P3) — see the self-attack below. This does not change THIS verdict (marking ω₀ still cannot propagate), but it is an unclosed tension in the ω₀-ownership itself. Owned-narration-only; no owner reconciles them. Recorded for a separate task.
- **G2:** the probe tests the *global* scene automorphism channel and the four named owned dynamical channels. A propagation via some owned structure NOT on this list would evade it — but the sweep (P1–P8) found no such owned structure, and P5/P6 are general (any Aut-non-invariant per-vertex reader on 11/13 is ⊥M1), so any future candidate inherits the same wall unless it first breaks `Aut = S₉×S₁₁×S₁₃`, which is Lean-owned.

## The self-attack (strongest)

**"ω₀ is OWNED as distinguished in zone 9 (P1), yet you use `Aut ⊇ S₉` (P3) which says ω₀ is NOT distinguished — you are quietly using the un-marked graph to kill a marked-graph mechanism."** Answer, in candidate language: this cuts BOTH ways and, if anything, STRENGTHENS the no-go. Two cases, both dead:
1. **If `Aut` really is `S₉×S₁₁×S₁₃` (Lean-owned, P3):** then ω₀ is not even distinguished in zone 9 at the graph level; the mechanism has no marked basepoint to propagate FROM. Dead at the source.
2. **If ω₀ IS a genuine mark (P1), so the *effective* symmetry is `S₈ × S₁₁ × S₁₃`:** the probe already computes THIS group (it fixes ω₀ and takes the stabilizer). The `S₁₁ × S₁₃` factor is still full and transitive (direct product + completeness), so the mark propagates nowhere. Dead at the wall.
The mark's reach is exactly `Stab_{S₉}(ω₀) = S₈` — it constrains zone 9 alone. Propagation across a direct-product factor with all-to-all coupling is impossible in either reading. The verdict is robust to how the P1/P3 tension is resolved.

## Bottom line

The basepoint-propagation mechanism is **DEAD**, killed by the owned all-to-all completeness of K(9,11,13) — the same wall the corpus already hit and CLOSED as a NO-GO in `D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001` (P6) and stated generally in `BOOK_04:1392` (P5). Zones 11 and 13 are genuinely undistinguished internally: ω₀ cannot induce a per-vertex distinction or an ordering there without an external catalog (⊥M1). This is a HONEST no-mechanism outcome — the correct one — not a manufactured mechanism, and it relocates no catalog because it selects nothing. Any distinction in 11/13 must come from OUTSIDE the scene graph (a terminal-passport / external-owner route), consistent with the session's map that the hard per-object structure is terminal, not scene-native.

---

## Independent skeptic verdict + repair log (accepted in full) — 2026-07-05

**VERDICT: ACCEPT-IN-FULL. The verdict SURVIVES. Mechanism = DEAD / not-owned.** Reproduced independently: `selector_basepoint_check.py` → **rc=0, 4/4 PASS**, negative control collapses to orbit=1 (probe is falsifiable / not rigged). The memo does not manufacture a selector; it reports an honest no-mechanism outcome, and that outcome reproduces on the actual scene K(9,11,13).

**No leap, either direction.**
- *Over-claim direction:* none. The memo declares DEAD, not "selector found." Correct.
- *Under-claim direction (the dangerous one):* the strongest candidate for a wrongly-dismissed OWNED selector is the corpus's own `V₁₁ = V₉ ⊔ D₂` and `V₁₃ = V₉ ⊔ {A,B,C,D}` (verified verbatim **BOOK_01:1551-1553**), which superficially embeds a distinguished "extra" set inside zones 11/13 that the anonymous-zone probe ignores. **Checked and REJECTED, on disk:** BOOK_01:1568 says the extension "fix[es] only the *partition*; they do not yet fix which edges exist," and **(C3) No-subaddress** (BOOK_01:1572; step-2 reasoning BOOK_01:1577) explicitly forbids realizing any within-part sub-address as owned graph structure ("any within-part edge creates the distinguishable binary property … not codable … without an extra marker (an external distinguishability catalog)"). Treating `V₉ ⊔ D₂` as a per-vertex distinction is itself ⊥M1 by the corpus's own rule. The probe's anonymous-zone model is corpus-correct.

**Catalog-relocation death? NO — it relocates nothing.** A catalog-relocation death needs the mechanism to select onto a degenerate manifold / residual symmetry that still needs a catalog. Here the residual freedom after fixing ω₀ is the FULL `S₁₁ × S₁₃` direct-product factor: the orbit of any zone-11 vertex is the entire 11-vertex zone (11/11), likewise 13/13 — the MAXIMAL orbit, strictly larger than any degenerate sub-manifold. The mechanism dies one step EARLIER than the deep trap: there is no symmetry-breaking at all (H = S₁₁, not proper), so there is no residual manifold to relocate a catalog onto. Any pick of a specific 11/13 vertex is a fresh external catalog by C1/P4 (names a privileged vertex = exogenous parameter = ⊥M1) and by P5 (single-vertex reader not Aut-invariant, needs an exogenous label). The memo's M1-CATALOG-TEST reading is accurate and corpus-grounded.

**Strongest owned NO-GO backing the verdict:** `BOOK_04:1399` (P6) — a theorem-grade, verbatim-verified owned NO-GO of exactly this mechanism class one categorical level up: the **oriented** `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃` is transitive on the 1287 triangles (single orbit), killing any canonical per-cell injection (`D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001`, Lean `D0.Matter.DSigmaRoleCycleCarrierNoGo`). The memo's inferred core (fixing ω₀ leaves S₁₁×S₁₃ fully transitive) is forced by direct-product P3 + all-to-all completeness P2, reproduced by the probe (orbit 11/11 and 13/13, rc=0), and confirmed FALSIFIABLE by the mutation test that injects a distinction into the LIVE channel (orbit collapses 11→1).

**Repairs applied (accepted in full):**
1. **[APPLIED — citation defect]** Dropped the stray secondary citation `BOOK_01 §05:411` from P6 (memo line 25). Verified on disk: BOOK_01:411 = `\quad` (a LaTeX spacing operator), NOT the transitivity/NO-GO statement. P6 repointed to its real and sufficient owner **BOOK_04:1399** (verbatim-verified). No other citation defect in the memo body.
2. **[APPLIED — optional sharpening, now included]** Added the oriented-group clause to the M1-CATALOG-TEST section, citing BOOK_04:1399's verbatim phrase "the **oriented** automorphism group `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`" — pre-empts the "directed/weighted edge structure breaks S₁₁/S₁₃" objection and closes G2 more tightly. Verified the "oriented" phrase is present verbatim at BOOK_04:1399.
3. **[NO substantive repair required]** Verdict DEAD stands: reproduced, falsifiable (mutation-tested), correctly scoped, no leap in either direction, relocates no catalog. NOT promoted (per instruction) — this is an audit, not a merge. The memo remains DRAFT with no registry / CSV / Lean / 053040 row touched, which is correct.

**Errors of record (found this audit):**
- **EoR-1 (memo, FIXED):** P6 carried a phantom secondary citation `BOOK_01 §05:411` → line is `\quad`, not the claimed statement. Repaired (repair 1 above).
- **EoR-2 (skeptic verdict prose, NOT in memo — recorded for accuracy):** the verdict's under-claim rejection cited "BOOK_01:1567" for "fixes only the partition … not which edges exist" and "BOOK_01:1584 (step 2)" for C3/No-subaddress. On disk the true owners are **BOOK_01:1568** (partition line, off-by-one) and **BOOK_01:1572** (C3 statement) + **BOOK_01:1577** (step-2 reasoning). The verdict's SUBSTANCE is fully owned and unchanged — only its two line numbers were off. The memo body does not carry these citations, so nothing in the memo needed changing; logged so the audit trail is exact.
- **EoR-3 (probe docstring, NOT a defect — recorded):** the probe (line 21) cites "BOOK_01 §01.20:1584-1594" for the A-matrix; 1584 is the "Adjacency matrix (DEF 17.0.2)" header and the all-ones off-diagonal blocks are at 1588-1592. The range brackets the DEF correctly and is not a defect; the memo's P2 uses the precise 1588-1592. No change.

**Final status:** mechanism basepoint-propagation = **DEAD / not-owned** (honest no-mechanism outcome, reproduced rc=0 4/4). Verdict accepted in full. Memo remains DRAFT. No promotion; no registry/CSV/Lean/053040 touch.
