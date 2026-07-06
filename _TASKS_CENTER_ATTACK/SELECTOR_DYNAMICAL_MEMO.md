# SELECTOR_DYNAMICAL — does the OWNED Pisot time-flow attractor break within-zone symmetry?

**Status: DRAFT — candidate NO-GO (author verdict NO-SELECTOR). Pre-skeptic.**
**Scope:** center-attack M1 front. Asks whether a DYNAMICAL/ATTRACTOR mechanism (the owned
forward-time Pisot flow) selects a UNIQUE within-zone labeling of `K(9,11,13)`, breaking the
symmetry the STATIC structure (M2 memo) provably cannot.

Companion script: `_TASKS_CENTER_ATTACK/selector_dynamical_check.py` (10/10 PASS, exit 0;
negative control demonstrated it CAN print SELECTOR-FOUND).

---

## Claim (DEF-0.2.2 form)

> The owned forward-time flow of D0 — the Pisot toral automorphism `T=[[0,1],[1,-1]]` with
> contraction `|ψ|=φ⁻¹<1` (`D0-PISOT-CONTRACTION-TIME-ARROW-001`), the amplitude tick
> `A_{k+1}=φ⁻¹A_k`, and the transport channel `ρ↦U_NρU_N†` / archive-tracing `ρ↦PUρU†P` —
> does **NOT** select a canonical within-zone labeling of `K(9,11,13)`. Its long-time
> structure is invariant under the full within-zone symmetry `Aut(K)=S₉×S₁₁×S₁₃`. The
> "attractor breaks within-zone symmetry" reading is **NOT owned**; it fails on two
> independent owned grounds (layer-separation + scalar-tick), and any repair that would make
> it work requires an un-owned per-vertex weight — the relocated M1 catalog the trap warns of.

---

## Owned pre-facts (verbatim, audited to exist on disk this session)

**PF-1 — the toral time operator and its Pisot spectrum.**
`01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:375` (§06.7 Route 3), verbatim:
> "The single modular flow is the toral time operator `T=[[0,1],[1,-1]]`, with `det = -1` and
> characteristic polynomial `lambda^2 + lambda - 1`. Its two real eigenvalues split: one root
> in `(0,1)` (contracting) and one in `(-2,-1)` (expanding, `|.|>1`)."

`…:386` (§06.8) verbatim: `spec(T)={phi^-1,-phi}`; `…:387` `det(T)=-1`.

**PF-2 — LAYER SEPARATION (the load-bearing fact).** Same line `:375`, verbatim:
> "The `(3,1)` signature pairs this single time flow against the rank-3 **reversible** spatial
> transport of `K(9,11,13)`, so \"3 space, 1 time-with-arrow\" never conflict."

`…:381` verbatim: "The finite time-transition operator has a **separate** integer
toral-automorphism layer:". → `T` is a 2×2 operator on the 2D time-layer lattice ℤ²; the scene
`K(9,11,13)` carries the **reversible** spatial transport. Distinct layers.

**PF-3 — the Pisot contraction owner.** `09_LEAN_FORMALIZATION/D0/Dynamics/PisotContraction.lean:45`
`theorem pisot_contraction : phi > 1 ∧ |psi| < 1 ∧ phi + psi = 1 ∧ phi * psi = -1`. Registry:
`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:270` (`D0-PISOT-CONTRACTION-TIME-ARROW-001`,
LEAN_PROVED, CORE-FORMALIZED). The contraction is a scalar inequality on ℝ, **not** an operator
on the scene.

**PF-4 — the amplitude tick is a UNIFORM SCALAR.** `…:489` (Block III), verbatim:
> "Each archive-delay tick multiplies the active amplitude by `φ⁻¹`, the unique root of the
> detector self-return split `p+p²=1` in `(0,1)`; hence `A_{k+1}=φ⁻¹A_k`".

One scalar `φ⁻¹`, applied to "the active amplitude" — not a per-vertex-distinct weight.

**PF-5 — the transport channel.** `…:500` verbatim: `\rho_N\mapsto U_N\rho_NU_N^\dagger`.
`U_N` "is a finite transport of an already addressed detector support" (`:503`). The
archive-tracing `ρ↦PUρU†P` (task) is the projected version of the same conjugation channel.

**PF-6 — within-zone symmetry (what must be broken).** `M2_PHASE_LABELING_MEMO.md:112`
verbatim: "the adjacency matrix `A` is invariant under `S9 × S11 × S13`."; `:121`
"`Aut(K(9,11,13)) = S₉×S₁₁×S₁₃` is transitive on the 1287 triangles (a single orbit)".
`BOOK_01…:629` "spectrum (rank 3 = space, kernel 30 = dark archive)".

**PF-7 — the static impossibility this task tries to escape.** `M2_PHASE_LABELING_MEMO.md:1`
verbatim: the owned within-zone labeling is "forced up to G_res, Q₈-typed not μ₉-cyclic;
**canonical cyclic/phase labeling IMPOSSIBLE from owned data**; zones 11/13 own nothing
per-vertex". The static structure leaves a G_res-torsor, never a point.

---

## The two owned computations (from the script, exact ℚ(φ)/ℤ)

**C-1 — the contracting eigendirection lives in the 2D time-layer, not the label space.**
Solving `(T−φ⁻¹)v=0` over ℚ(φ) (φ⁻¹=φ−1, verified `φ·(φ−1)=1`) gives the contracting
eigenvector `v=(1, φ⁻¹) ∈ ℝ²`. Verified `T·v = φ⁻¹·v` exactly. **Ambient dimension 2.** The
within-zone label spaces have dimensions 9, 11, 13. There is **no owned linear map** carrying
the 2D time-layer eigenline into any `V_z` (PF-2: distinct layers; time-flow vs reversible
spatial transport). A φ-power dominance in a 2D layer disjoint from the labels cannot fix a
label. **This is the primary kill of the attractor reading.**

**C-2 — the owned tick/channel on the carriers is S_n-invariant.** The owned tick (PF-4) is the
uniform scalar `φ⁻¹·I` on the active amplitude; the channel (PF-5) is conjugation by a transport
`U_N`. A uniform scalar commutes with **every** permutation of every zone: computed for zones
9/11/13, `[φ⁻¹]*n` commutes with `S_n` (all diagonal entries equal). Therefore the long-time /
attractor structure of the owned tick is **constant on each S_n-orbit** — its "attractor" is the
whole symmetric orbit, a degenerate manifold, **not a point**. No within-zone symmetry is broken.
(A generic `U_N` conjugation could in principle be non-scalar, but nothing owned fixes a
particular non-scalar `U_N`; the owned content of the tick ladder is exactly the scalar `φ⁻¹`.)

---

## Adjudication of the CRUX

**Does the flow select a UNIQUE canonical labeling, or leave a residual degeneracy needing a
catalog?** It leaves a residual degeneracy. On C-1 the flow does not even reach the label space;
on C-2 the part of the flow that does touch the carriers is a scalar, so its attractor is the
**entire** `S₉×S₁₁×S₁₃`-orbit. This is strictly the DEEP TRAP: the "attractor" is a degenerate
manifold (a full symmetric orbit), and picking a point on it still needs the exact catalog the
M2 memo proved is not owned (PF-7). The dynamical framing **relocates** M1's catalog into the
choice of a per-vertex weight; it does not escape it.

**Is "attractor breaks within-zone symmetry" OWNED or a reading?** It is **my reading / the
task's hypothesis, NOT owned.** No owned text asserts that iterating `T`, the tick, or the
channel breaks `S₉×S₁₁×S₁₃`. The owned texts assert the opposite ingredients: `T` is a *separate*
layer (PF-2), the spatial transport is *reversible* (PF-2, so no contraction there), the tick is
a *uniform* scalar (PF-4), and the static labeling is *impossible* to make canonical (PF-7). The
SSB analogy in the task ("a symmetric dynamical system can have an asymmetric attractor") is
sound in general but requires a non-scalar generator on the symmetric space; the owned generator
on the label space is scalar, so no asymmetric attractor is producible from owned data.

**Negative control (test is not rigged).** The script constructs distinct per-vertex weights on
zone 9 and confirms an argmax WOULD select a unique vertex — so the code path `SELECTOR-FOUND`
is reachable. It prints NO-SELECTOR only because that distinct weight is (a) not owned and (b)
exactly the relocated catalog. The conclusion can fail; it does not.

---

## VERDICT

**NO owned dynamical/attractor selector.** The owned forward-time Pisot flow does **not** drive
`K(9,11,13)` to a canonical within-zone labeling. Two independent owned obstructions:
(1) the Pisot contraction lives in a 2D time-layer disjoint from the label space (C-1); (2) the
part of the flow acting on the carriers is a uniform `φ⁻¹` scalar, whose attractor is the full
`S₉×S₁₁×S₁₃`-orbit, not a point (C-2). The "asymmetric attractor" reading is not owned. The
mechanism **fails and relocates the catalog** into an un-owned per-vertex weight (M1 trap, not
escape). This is consistent with — and does not weaken — the M2 static result
(`M2_PHASE_LABELING_MEMO.md`): dynamics does not rescue what the static structure leaves as a
G_res-torsor.

**HONEST outcome:** "no owned mechanism" — a valid and here correct result. No mechanism is
manufactured.

---

## PRE-REGISTERED attack surface (strongest attacks against this NO-GO)

1. **"You used the scalar tick; the real generator is the non-scalar `U_N`."** — Rebuttal
   demand: name owned text that fixes a SPECIFIC non-scalar `U_N` acting per-vertex on `V_z`. PF-4/PF-5
   give only the scalar `φ⁻¹` and an "already addressed" transport with no owned per-vertex spectrum.
   If such text exists, this NO-GO is WOUNDED and must be recomputed with that `U_N`. (Audited: not found;
   M2 X4 records all owned tick consumers are torsor-invariant.)
2. **"The archive-tracing projection `P` is non-scalar and could break the symmetry."** —
   `P` projects onto the retained algebra; unless the retained-algebra decomposition is owned to
   distinguish within-zone vertices, `P` is `S_n`-equivariant (it retains/traces zones, not
   individual vertices — PF-6: zones 11/13 own nothing per-vertex). Attack must exhibit an
   owned `P` that is NOT `S_n`-equivariant.
3. **"Selection of the space/time SPLIT counts as selection."** — Conceded and irrelevant: the
   task explicitly excludes this ("φ-power dominance is not selection unless it canonically fixes
   the WITHIN-ZONE labels, not just the space/time split"). C-1 concerns exactly the within-zone
   labels, where the flow is absent.
4. **Self-attack (strongest): "Adler–Weiss gives `T` a canonical Markov partition — a
   canonical symbolic labeling — so `T` DOES canonically label something."** — True but
   off-target: the Adler–Weiss partition (cert `vp_time_2d_pisot.py`, "the golden Markov
   partition is smooth") canonically labels the **2D torus symbolic dynamics** (the time layer),
   NOT the within-zone vertices of `K(9,11,13)`. It is a canonical labeling of the WRONG object.
   Bridging it to `V_z` requires an owned map time-layer→`V_z` — the very map PF-2 denies. This
   self-attack, pre-registered, actually SHARPENS the NO-GO: even the one place `T` DOES produce a
   canonical labeling is in the disjoint layer.

5. **"The torus address φ⁵ = '11+ξ5' links the torus to the scene, so `T` does reach the
   zones."** — Checked (`BOOK_06/…/06.37…:20`): the torus address `(R+r)/(R−r)=φ⁵` reads as
   integer address `11` plus residual `ξ5`. But `11` is a **zone cardinality** (which zone),
   NOT a within-zone vertex label; it does not distinguish vertices inside a zone, so it is
   `S₁₁`-invariant and breaks nothing within-zone. Near-miss, checked, does not reach the labels.
6. **"The Adler–Weiss / Lucas–Voronoi Markov partition of `T` gives a canonical cell labeling."**
   — Checked (`05_CERTS/vp_lucas_voronoi_markov_partition.py`): the partition is "OPERATOR
   SCAFFOLD only" on the **2-torus** (boundary cuts `L2=3,L3=4,L5=11`); Voronoi-cell-exactness and
   conjugacy are EXTERNAL/PROOF-TARGET, and it labels torus cells, not `V_z` vertices. Same
   layer-separation kill as C-1/self-attack #4.

## Falsification / reopening hook

Reopen if any ONE is exhibited from owned text: (a) an owned linear/affine map carrying the
spec(T)-eigenline (or the Adler–Weiss symbol sequence) into a within-zone label space `V_z`;
(b) an owned per-vertex-DISTINCT tick weight on some `V_z` (contradicting M2 PF-7); (c) an owned
non-`S_n`-equivariant transport `U_N` or archive projection `P` acting inside a zone. Any of
these makes the attractor computation live and this NO-GO must be recomputed.

## Proposals (memo-only; NO edits to registry / ledger / .lean / 053040 rows)

- Candidate row (NOT written): `D0-DYNAMICAL-SELECTOR-WITHINZONE-NOGO-001` — "owned Pisot
  time-flow has no within-zone attractor; layer-separated + scalar-tick; SSB reading un-owned",
  status DRAFT/no-go, would complement `D0-PISOT-CONTRACTION-TIME-ARROW-001` and cross-ref
  `M2_PHASE_LABELING_MEMO`. Mint only via `VERIFIED_CLOSURE_PROTOCOL.md` after skeptic pass.

---

## Independent skeptic verdict + repair log (accepted in full)

**Verdict: ACCEPT-IN-FULL. The NO-GO SURVIVES intact.** Independent re-derivation and on-disk
re-verification of every load-bearing fact confirm the author's headline: **no owned
dynamical/attractor selector.** Checked both leap directions independently; the headline holds.

**Leaps — NONE fires.**
- *Overclaim leap: does not apply.* The verdict IS "no-selector" — no mechanism is manufactured,
  so there is nothing to over-claim. The one real overclaim risk (that the script is a rigged
  tautology) is defused and named: the script's verdict rests on two hand-set booleans
  (`selector_dynamical_check.py:69` `owned_map_timelayer_to_zone=None`;
  `:110` `owned_within_zone_action_nonscalar=False`), so the ARITHMETIC alone does not prove the
  NO-GO. Confirmed on disk this session: the ℚ(φ) arithmetic checks (T det=−1, contracting
  eigenvector `v=(1,φ⁻¹)`, uniform-scalar S_n commutation) are real and pass, but the verdict
  booleans encode **audited absences** (PF-2 layer separation, PF-4 scalar tick, M2 X4 consumer
  split), not a computed impossibility. The memo does not hide this; every load-bearing fact is a
  verbatim-audited absence.
- *Underclaim leap: does not fire.* The two live candidates for a dismissed owned selector both
  provably land on the WRONG object, verified against the certs on disk this session:
  (a) the Adler–Weiss canonical golden Markov partition (`05_CERTS/vp_time_2d_pisot.py:6-7`,
  verbatim "a 2-torus … the golden Markov partition is smooth (Adler-Weiss …), so symbolic time
  dynamics") canonically labels the **2-torus symbolic dynamics** (the time layer), not
  within-zone vertices; (b) the φ⁵ torus address / Lucas–Voronoi cells
  (`05_CERTS/vp_lucas_voronoi_markov_partition.py:2,11-13`, "OPERATOR SCAFFOLD only",
  Voronoi-cell-exactness + conjugacy "EXTERNAL … PROOF-TARGET", boundary cuts `L2=3,L3=4,L5=11`)
  label **torus cells**, and the `11=L₅` is a **zone cardinality**, not a within-zone vertex. The
  bridge each needs is the owned map time-layer→`V_z` that PF-2 (`BOOK_06:375`, "rank-3 reversible
  spatial transport of `K(9,11,13)`") denies. Neither reaches the labels.

**Catalog-relocated: YES — and the memo says so, correctly.** The mechanism does NOT pin a unique
canonical object. Named residual freedom: the FULL `S₉×S₁₁×S₁₃`-orbit (Nambu–Goldstone-style
degenerate manifold). The owned tick `φ⁻¹` is a uniform scalar; a scalar commutes with every
permutation of every zone (re-verified for n=9,11,13: `10/10 PASS, exit 0`), so the "attractor" is
the entire symmetric orbit, not a point. Picking a point on that orbit still needs the exact
per-vertex weight that M2 PF-7 + X4 prove is un-owned. The dynamical framing **relocates** M1's
catalog into the choice of a non-scalar generator; it does not escape it. **A mechanism that
relocates the catalog is DEAD as a selector — confirmed.**

**Strongest kill (load-bearing):** `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:375`
(echoed `:381` "The finite time-transition operator has a separate integer toral-automorphism
layer:") — layer separation. `T=[[0,1],[1,-1]]` is a 2×2 automorphism on a **separate** integer
toral time-layer lattice `ℤ²`, paired against the **rank-3 reversible** spatial transport of
`K(9,11,13)`. Nothing contracts within the scene carriers; the contracting eigenline is trapped in
the disjoint 2D time-layer. Verbatim-verified on disk this session, exactly as PF-2 quotes it.

**Repairs.**
1. NONE required for the verdict — the NO-GO survives intact.
2. (OPTIONAL honesty polish, at author's discretion) Name in the memo body that
   `selector_dynamical_check.py` is a **fact-ledger**: its verdict booleans are hand-set at lines
   69/110 to encode audited absences, so the CITATION AUDIT — not the arithmetic — carries the
   NO-GO. (The memo's "Negative control" paragraph already implies this; making it explicit
   forecloses the "rigged script" attack.)
3. Keep the candidate row DRAFT; mint only via `VERIFIED_CLOSURE_PROTOCOL.md`. No promotion this
   pass.

**Errors of record (this verification session).**
- ER-1 (citation line-offset, NON-verdict-affecting): PF-6 quotes `BOOK_01…:629` for
  "spectrum (rank 3 = space, kernel 30 = dark archive)". That exact phrase lives verbatim one
  block up at **`BOOK_01:618`**; line `:629` holds the paraphrase "`K(9,11,13)` rank 3 / nullity
  30 … Dark memory: the kernel of the adjacency operator." The fact EXISTS verbatim on disk — the
  cited line number is off by the adjacent block. Recommend PF-6 cite `:618` (verbatim) or
  `:618/:629` (verbatim/paraphrase). Not load-bearing for the NO-GO (which rests on PF-2/PF-4/PF-7).
- ER-2 (none other): PF-1, PF-2, PF-3 (Lean `PisotContraction.lean:45` + registry
  `CLAIM_TO_LEAN_MAP.csv:270`), PF-4, PF-5, PF-6 (M2 `:112/:121`), PF-7 (M2 `:1`), and both
  self-attack certs (`vp_time_2d_pisot.py`, `vp_lucas_voronoi_markov_partition.py`) all verified
  to EXIST verbatim on disk this session. No phantom certs, no false rows, no misquotes among the
  load-bearing facts.

**Final status:** NO-GO SURVIVES (ACCEPT-IN-FULL). No owned dynamical/attractor selector; the
mechanism relocates M1's catalog and is DEAD as a selector. Residual = the un-owned per-vertex
weight (the relocated catalog) + the ER-1 line-offset polish; both memo-only, no registry/ledger/
.lean/053040 edits.
