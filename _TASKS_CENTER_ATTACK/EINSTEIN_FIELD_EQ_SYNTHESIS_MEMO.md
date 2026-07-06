# EINSTEIN FIELD-EQ SYNTHESIS — the G_A2 divergence obstruction is an exact conserved-completion identity with a capacity source (DRAFT, post-skeptic-repair)

> **VERDICT BANNER (skeptic #9, 2026-07-05 — kills accepted in full, repairs applied; §11 has
> the errors of record).** Original T3 per-node "⟺ Boolean" KILLED (counterexample: non-Boolean
> h on the 4-cycle (0,9),(0,10),(1,9),(1,10) satisfies the law; the old harness iff-check exits 1
> on it) — REPLACED by the UNIVERSAL conformal law + the Boolean-⟹ direction + the corrected
> quantifier, all exact-ℚ verified. T1 re-graded "theorem-grade candidate" → INSTANTIATION of the
> owned Laplacianization clause (BOOK_07:1782; cert vp_hodge_links_carrier_nogo.py:70-82). T4
> superseded by the STRONGER flat-limit separation theorem (ALL correction shapes, bound 32/11).
> Source retyped gravity-natively as boundary-cut/holographic-area density (owned §07.41), with
> the EM-typing tension of "capacity" recorded. §6 book draft SPLIT to avoid the row-107
> collision (D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001, LEAN_PROVED). T2 and §5 SURVIVED unmodified.

**Claim-IDs touched:** D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001 (upgrade of notes, proposal),
D0-SPECTRAL-EINSTEIN-001 (cross-ref only), D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001 (row 107 —
declared collision surface for §6; its text is NOT touched by the safe motion), D0-HODGE-LINKS-001
(unchanged).
**Date:** 2026-07-05 · **Status:** DRAFT / candidate — post-skeptic-repair. No registry/.lean/book edits made.
**Deliverables:** `einstein_field_eq_check.py` (exact-ℚ, can-fail, mutation-tested) + this memo
(+ §6: the BOOK_07:1770–1790 replacement text, DRAFT IN-MEMO ONLY).
**Pre-flight:** ran on `einstein divergence bianchi deg capacity`. Existing content: rows 175
(CORE_BRIDGE_SPLIT) and 548 (NO-GO) of `CLAIM_TO_LEAN_MAP.csv`; certs
`vp_g_a2_einstein_obstruction.py`, `vp_spectral_einstein_response.py`; memo `G_A2_EINSTEIN_MEMO.md`.
The conserved-completion identity below is in NONE of them (row 548 ends at "BRIDGE-A/B/C, none
owned"); its ALGEBRA has an owned parent — the matter-Laplacianization clause of BOOK_07:1782
(F5), cert-implemented at `vp_hodge_links_carrier_nogo.py:70-82` (F17) — which is why T1 is
graded INSTANTIATION, not theorem (post-skeptic re-grade). Not a duplicate row: the
instantiation at `G_A2`, the general-(h,ρ) form, the −2·einsteinResponse equality, the
separation theorem and the conformal law appear nowhere; it is the exact link between the two
existing rows.

---

## 0. Claim (DEF-0.2.2 form), split by status

**T1 (INSTANTIATION-grade — re-graded per skeptic #9; exact ℚ; ALL symmetric edge fields h,
ALL positive vertex measures ρ).** The identity below is the OWNED unique-divergence-free-
completion (Laplacianization) clause of BOOK_07:1782 — already cert-implemented for generic
edge-stress at `05_CERTS/vp_hodge_links_carrier_nogo.py:70-82` — INSTANTIATED at `E := G_A2`.
The algebra has an owned parent (an ownership STRENGTHENING, not a demotion); the new content
is (i) the instantiation at the registry's NO-GO tensor, (ii) the general-(h,ρ) closed form,
(iii) the exact `−2·einsteinResponse` equality, (iv) the exact numerics. With
`M_ij := h_ij/(ρ_i ρ_j)`, `deg_M(j) := Σ_i M_ij`, `D_M := diag(deg_M)`, `L_M := D_M − M`
(a genuine graph Laplacian):

```
G_A2 := ∂S_A2/∂h = 4M ;
(div G_A2)_j = 4·deg_M(j)  =  (div 4D_M)_j ;
X := 4D_M is the UNIQUE diagonal tensor with div(G_A2 − X) = 0
     (uniqueness = one-line corollary of div-linearity, pinned in-script as such,
      NOT an independent test) ;
G_A2 − 4D_M = −4L_M = −2·einsteinResponse(L_M) ,   div(G_A2 − 4D_M) = 0  identically.
```

Equivalently: **G_A2 = 4D_M − 4L_M** — the a2 variational response decomposes exactly into a
diagonal capacity-density part and (−2×) the corpus's own conserved Einstein-response object.
(In-script the `L_M` comparison is a definitional-expansion pin, labelled honestly; the
load-bearing computed facts are `L_M` row sums = 0 and `div G_A2 = 4·deg_M`.)

**T2 (flat point, ties the two registry rows numerically).** At h≡1, ρ≡1: `M = A`,
`G_A2 = 4A`, `X = 4D` with `X_jj = 4·deg(j) ∈ {96,88,80}`, `G_A2 − 4D = −4L`. At Perron ρ=deg:
`X_jj ∈ {23/120, 41/220, 7/40}` per zone, `max|div G_A2| = 23/120` (the NO-GO cert's number,
reproduced), completion conserved.

**T3 (measure-coupling law — REPAIRED; the original "⟺ Boolean" was KILLED by skeptic #9,
kill accepted, see §11).**
- **T3-U (UNIVERSAL, all h, all ρ>0):** in the multiplicative/conformal variable `u_ij`
  (`h_ij → h_ij e^{u_ij}`), the response `G̃ := ∂S_A2/∂u|₀ = h ⊙ G_A2` (entrywise
  `4h²/(ρρ)`, chain rule) satisfies

```
(div G̃)_j = −2 ρ_j · ∂S_A2/∂ρ_j      IDENTICALLY — no scope restriction at all.
```

  **TRIVIALITY PIN (P2-analogue; skeptic #2, accepted):** T3-U is the per-node
  EULER-HOMOGENEITY identity of the per-edge bidegree — it holds for ANY edge action whose
  per-edge h-degree is 2× its per-node ρ-degree, on ANY graph (pinned in-script, T3f: the
  second action `S′ = Σ 2h⁴/(ρρ)²`, bidegree (4,2), obeys the SAME `−2` law). Its sole D0
  content is the ATTRIBUTION that `S_A2` carries bidegree (2,1) per edge — the local conformal
  pairing `h/(ρρ)`. Like P2 for T1: the algebra is generic; the content is which owned action
  carries it.

- **T3-B (the direction used downstream):** `h` Boolean ⟹ per-node
  `(div G_A2)_j = −2ρ_j ∂S_A2/∂ρ_j` (Boolean h makes `G̃ = G_A2`; covers the frozen scene for
  EVERY ρ — flat AND Perron).
- **T3-Q (corrected quantifier):** the per-node h-law holds for ALL ρ>0 SIMULTANEOUSLY ⟺ h
  Boolean (deficit `= (4/ρ_j)Σ_i h_ij(1−h_ij)/ρ_i`; vanishing for every ρ>0 forces
  `h(1−h) = 0` edgewise). Witnessed in-script: the skeptic's non-Boolean counterexample
  satisfies the law at ρ≡1 (T3d REGRESSION) and fails it at `ρ_9 = 2` (T3e). (Nit, recorded
  per skeptic #2: the PASS_T3e print is one shade stronger than what one witness shows; THIS
  wording — the ⟸ by the one-coefficient-per-edge argument, the witness only illustrating —
  is the precise one.)
- Global Euler balance `⟨h,∂S_A2/∂h⟩ + ⟨ρ,∂S_A2/∂ρ⟩ = 0` for ALL (h,ρ) — unchanged (T3a).
- **Error of record:** the original per-node "⟺ Boolean" is FALSE (the parametrization-artifact
  trap (g) fired: in the u-variable the law is universal; the Boolean scope was an artifact of
  differentiating in h rather than log h; and even in the h-variable the converse fails —
  per-node cancellation `Σ_i h(1−h)/ρ_i = 0` is achievable with non-Boolean h).

**T4 (no-decoupling — SUPERSEDED by the stronger flat-limit separation, skeptic #9's argument,
adopted).**
- **T4-diag (retained, narrowed):** on positive backgrounds the forced completion
  `X_jj = 4·deg_M(j) > 0` strictly — the DIAGONAL lane of the ledger's EXACT-MISSING is closed.
  BRIDGE-A *off-diagonal/trace* counterterms are NOT excluded by this. 
- **T4-sep (the load-bearing theorem, ALL correction shapes):** for ANY tensor `T` with
  `archiveDivergence T = 0`: `div(T − G_A2)_j = −4·deg(j)`, and `|div M'_j| ≤ N·||M'||_max`,
  hence on the frozen scene

```
||T − G_A2||_max  ≥  max_j 4·deg(j)/N  =  96/33  =  32/11 .
```

  EVERY conserved tensor is uniformly separated from `G_A2`; "conserved AND reduces to G_A2 in
  a flat/decoupling limit" (rows 175/548 EXACT-MISSING) is impossible for ALL corrections —
  diagonal or not. Dichotomy: accept the capacity diagonal (this identity) or change
  carrier/divergence (BRIDGE-B/C, unchanged). Verified in-script on conserved probes (incl.
  the owned `2L`) with a non-conserved distance-0 control.

**T5 (holographic typing pin — gravity-native, added in repair).** On the frozen scene
`BoundaryCutWeight({j}) = deg(j)` (singleton cut = degree), so with the OWNED
`C(boundary S) = BoundaryCutWeight(S)/4` (F15, BOOK_07 §07.41:1752):

```
(div G_A2)_j = 4·BoundaryCutWeight({j}) = 16·C(∂{j}) .
```

The leak is typed as **boundary-cut / holographic-area density** — the gravity-native owned
route ("boundary cut capacity is holographic area", BOOK_07:1770-1771).

**R (READING — candidate language, NOT a theorem; ownership scoped in §4; repaired typing).**
The NO-GO's "failed Bianchi" is not a defect but the *coupling seam*: the divergence of the
finite variational curvature response equals, exactly, the local boundary-cut density —
`(div G_A2)_j = 4·Cut({j}) = 16·C(∂{j})` on the scene (T5) — and equals, exactly, the action's
coupling to the fixed vertex measure (T3-U in the conformal variable, universally;
T3-B on the scene). Non-conservation ⇔ background-measure dependence; conservation is restored
identically the moment the diagonal capacity response is carried inside the tensor (T1).
Where the words stop being owned is stated in §4; the source is read primarily as
**boundary-cut / holographic-area density** (gravity-native owned typing, F15) and secondarily
as **edge-capacity density** (with the recorded tension that edge-capacity's owned force-typing
is EM, F8) — NOT "matter density"/"T_μν" (unowned), NOT "pressure" (barred by F12).

---

## 1. Owned pre-facts (verbatim, file:line)

**F1 — the NO-GO (input, unchanged).** `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:548`
(D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001), verbatim excerpt:
> "G_A2^{ij}=dS_A2/dh_ij=4 h_ij/(rho_i rho_j) EXISTS and is SYMMETRIC on the frozen scene
> K(9,11,13) ... BUT is NOT archiveDivergence-free: (div G_A2)_j = sum_i 4 h_ij = 4*deg(j) =
> {96,88,80} != 0 for every node (deg>=20), and 23/120 != 0 under Perron rho=deg."

**F2 — the CORE_BRIDGE_SPLIT (input, unchanged).** `CLAIM_TO_LEAN_MAP.csv:175`
(D0-SPECTRAL-EINSTEIN-001), verbatim excerpt:
> "WHAT IS OWNED (LEAN_PROVED): the theorem einstein_response_symmetric_and_conserved is TRUE,
> but it is about G=2L (the graph LAPLACIAN, einsteinResponse L := 2*L) -- it is the discrete
> LAPLACIAN-BIANCHI conservation ... EXACT-MISSING (Einstein-tensor leg only): a trace-adjusted
> rank-2 tensor Ghat with archiveDivergence Ghat = 0 that reduces to G_A2 in a flat/decoupling
> limit, on a single carrier."

**F3 — the a2 scalar being differentiated.** `09_LEAN_FORMALIZATION/D0/Geometry/HeatTraceA2Decomposition.lean:15-19`, verbatim:
> `noncomputable def diagonalSquareTerm ... : ℝ := ∑ i, (L i i)^2 / (ρ i)^2`
> `noncomputable def discreteEHActionProxy ... : ℝ := (1 / 2 : ℝ) * ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0`

Note for §3: at flat weights `L i i = deg(i)`, so the OWNED action-level decomposition already
splits a2 into a *diagonal capacity-squared term* plus the off-diagonal EH proxy. The response-
level identity T1 is the variational mirror of this owned split.

**F4 — the owned conserved object and divergence operator.**
`09_LEAN_FORMALIZATION/D0/VNext2/SpectralEinsteinResponse.lean:32,40`, verbatim:
> `def archiveDivergence (A : Matrix N N ℝ) : N → ℝ := fun i => ∑ j, A i j`
> `def einsteinResponse (L : Matrix N N ℝ) : Matrix N N ℝ := (2 : ℝ) • L`

**F5 — the owned conservation-completion move (the key precedent).**
`01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:1782`, verbatim excerpt:
> "every symmetric edge-stress `E` has a unique divergence-free completion
> `M = E − diag(rowsum E)` (its Laplacianization), so matter conservation is exactly discrete
> transversality."

T1 is EXACTLY this owned move applied to `G_A2` (E := G_A2, completion = G_A2 − 4D_M), with the
extra computed content that the completed object equals −2·einsteinResponse(L_M).

**F6 — shell degrees are owned scene invariants.**
`01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:924-927`, verbatim:
> "and the shell degrees
> d_9=24,\qquad d_{11}=22,\qquad d_{13}=20."

**F7 — degree used as an information-normalizing capacity in an owned action.**
`01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md:349`, verbatim: `d_9=\deg(V_9)=24.`
— inside the §03.7 boundary action `S_∂(r,I)` where the interaction-information `I` enters as
`(1 + I/d_9)`: the degree is the owned normalizer of information per boundary cell.

**F8 — the owned 0/1-skeleton stratification (what the diagonal and the edges ARE).**
`01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md:1626-1627`, verbatim excerpts:
> "**0-skeleton (vertices, `|V|=33`).** `Tr_0(R)` is the global node-closure density. This is
> macroscopic gravity `G_N`" ...
> "**1-skeleton (edges, `|E|=359`).** `Tr_1(R)` is the inter-nodal transport capacity. This is
> electromagnetism"

**F9 — |E| = 359 owned as "topological capacity".**
`01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md:77`, verbatim excerpt:
> "the edge-operator zeta yields `ζ_E(0) = 359 = |E|` (the topological capacity, at `s=0`)"

**F10 — the owned weak-field Poisson skeleton demands a NEUTRAL source.**
`01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:1293-1296`, verbatim:
> "Thus solvability forces
> \sum_i \rho_i = 0,"

**F11 — the one owned CORE field-law shape.** `BOOK_07:1137-1138`, verbatim excerpt:
> "That law is `K(x) ~ ϱ(x)` — curvature-defect proportional to closure-density"

**F12 — the pressure-typing bar.** `D0_CLAIM_CLOSURE_CONTRACT.md:45`, verbatim:
> "Feedback pressure is `P_fb=beta^{-1}d_V log Z_N`; `P_N` is never pressure."

**F13 — the determinant balance (cross-link candidate).** `BOOK_08:883`, verbatim:
> `active localization x archive expansion = 1`

**F14 — the archive-tracing leak (cross-link candidate).**
`_TASKS_CENTER_ATTACK/M1QM_DEPARTURE_SCALE_MEMO.md:51-53`, verbatim excerpt:
> "it loses probability for every carrier/state: trace surviving mean `≈0.095≈φ⁻⁵`, `max<1`
> across 300 carriers). Its per-tick retained-amplitude decay is `A_{t+1}=φ⁻¹A_t`, **FORCED**"

**F15 — the owned holographic boundary capacity (added in repair; the gravity-native typing).**
`01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:1747-1757` (§07.41 Trace-Heat-Capacity
Gravity), verbatim excerpts:
> "For a finite graph region `S`, the admissible finite rule is:" ...
> `C(boundary S) = BoundaryCutWeight(S)/4`
> "The factor `A/4` is read as ABCD boundary capacity: four terminal detector roles count
> boundary distinguishability in quarter-cut units."

and the compact statement, `BOOK_07:1770-1771`, verbatim: "boundary
cut capacity is holographic area". On the unweighted scene `BoundaryCutWeight({j}) = deg(j)`
(computed, T5), so the leak `4·deg(j) = 16·C(∂{j})` is typed by an owned gravity-sector object.

**F16 — the row-107 interface owner (declared collision surface for §6).**
`CLAIM_TO_LEAN_MAP.csv:107` (D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001, LEAN_PROVED,
CORE_BRIDGE_SPLIT), verbatim note:
> "Finite witness yields symmetric divergence-free second-order TT-compatible macro interface;
> no continuum Einstein-Hilbert primitive is imported into core."

Its Lean owners include `Gravity.finite_gravity_witness_yields_einstein_hilbert_interface`.
The BOOK_07 compact-statement closure line (~1777) is this row's book text; the §6 SAFE motion
therefore does NOT touch it.

**F17 — the owned parent of T1 is cert-implemented.**
`05_CERTS/vp_hodge_links_carrier_nogo.py:70-82` (POSITIVE PARTIAL): builds a generic symmetric
off-diagonal edge-stress `E`, forms `M = E − diag(rowsum E)` ("unique divergence-free
completion"), checks `M.sum(1) = 0` and off-diagonal agreement — the Laplacianization clause
of F5, in code. T1 instantiates exactly this at `E := G_A2`.

---

## 2. The computation (all exact ℚ; `einstein_field_eq_check.py`, exit 0, mutation-tested)

Script: `_TASKS_CENTER_ATTACK/einstein_field_eq_check.py`. Backgrounds: flat (h=1,ρ=1), Perron
(h=1,ρ=deg), seeded random rational (h,ρ), signed h. Results (all PASS, exact):

- **T1** on all four backgrounds: `G_A2 = 4M`; `div G_A2 = 4·deg_M`; `div(G_A2 − 4D_M) = 0`;
  `G_A2 − 4D_M = −4L_M = −2·einsteinResponse(L_M)` entrywise (L_M built independently; its
  Laplacian property — zero row sums — checked separately).
- **C2** gradient genuineness: `∂S/∂h` matches exact central differences (S quadratic in h);
  `∂S/∂ρ` matches an exact `a/t+b` two-point model fit with third-point validation (S is
  homogeneous of degree −2 in ρ; a central difference is NOT exact for 1/ρ — the first draft of
  this script used one and correctly FAILED; the exact reconstruction replaced it).
- **T2** flat/Perron numbers as in §0; the NO-GO cert's `{96,88,80}` and `23/120` reproduced.
  (The Perron `div(G−X)=0` re-check is TAUTOLOGICAL given div-linearity and is labelled so
  in-script; T2's non-tautological content is the closed-form values.)
- **T3a** Euler balance on ALL backgrounds. **T3b** UNIVERSAL conformal law
  `div(h⊙G_A2)_j = −2ρ_j∂S/∂ρ_j` on ALL backgrounds (incl. non-Boolean, signed). **T3c**
  Boolean ⟹ per-node h-law (flat AND Perron). **T3d** REGRESSION: skeptic #9's non-Boolean
  counterexample (4-cycle `(0,9),(0,10),(1,9),(1,10)`, `h = 3/5,6/5,6/5,3/5`, ρ≡1) SATISFIES
  the per-node h-law at all 33 nodes — the old iff is FALSE, kept as a permanent regression.
  **T3e** the same h FAILS the law at node 0 under `ρ_9 = 2` — witnesses the corrected
  "for ALL ρ ⟺ Boolean" quantifier.
- **T4b** flat-limit separation: bound `max_j 4·deg(j)/N = 96/33 = 32/11` exact; conserved
  probes (zero, owned `2L`, the completion `−4L`) all at distance ≥ 32/11; non-conserved
  control (`G_A2` itself) at distance 0 — the bound genuinely uses conservation.
- **T5** holographic typing: `Cut({j}) = deg(j)` by independent count;
  `(div G_A2)_j = 4·Cut({j}) = 16·C(∂{j})` exact.
- **P1** `Σ_j (div G_A2)_j = 8|E| = 2872 ≠ 0` — NOT a Poisson-admissible source (F10).
- **P2** triviality pin: at the flat point the identity is exactly `4·(A = D − L)`.
- **P3** ring pin: no rational multiple of `φ⁻⁵ = −8+5φ` equals any integer leak value
  (exact (1,φ)-basis arithmetic); a ℚ(φ) coefficient always exists (field) and is naming freedom.
- **C3** falsifiability (perturbed completion fails). **C6** relabelled ALGEBRA PIN:
  `div(G−X)_j = (div G)_j − X_jj` verified on an arbitrary diagonal probe NOT built from
  `div G`; uniqueness is its one-line corollary (honestly labelled, not an independent test).
  **C7** diagonal-lane no-decoupling (narrowed; superseded as load-bearing by T4b).
- **Mutation tests** (temp copies): `X = 3D_M` → exit 1 (T1); universal-law coefficient
  `−2 → −3` → exit 1 (T3b); separation bound inflated → exit 1 (T4b); counterexample
  cancellation broken (`3/5 → 7/5`) → exit 1 (T3d).

---

## 3. Why this is an UPGRADE and not word-dressing — and exactly where the physics stops

**(a) What was two separate rows is one exact identity.** Row 175 owns `G = 2L` conserved
(Laplacian-Bianchi); row 548 owns `G_A2` non-conserved. T1 shows these are the two halves of
**one** equation: `G_A2 = 4D_M − 4L_M`, i.e. *(a2 response) = (capacity diagonal) − 2·(owned
conserved Einstein response)*. The corpus's conserved gravity object is recovered from the a2
gradient by the corpus's OWN conservation-completion move (F5) — the same Laplacianization that
BOOK_07 already uses to define matter conservation. Nothing new is imported; a loop closes.

**(b) The non-conservation has a Noether-type mechanism, stated exactly (T3, repaired form).**
In field theory, the divergence of a variational response fails to vanish precisely when the
action depends on a non-dynamical background, and the failure equals the background-coupling
term. Discrete mirror, computed: `S_A2` depends on the fixed vertex measure ρ, and in the
conformal variable the leak *is* the measure response, per node and UNIVERSALLY:
`(div h⊙G_A2)_j = −2ρ_j ∂S_A2/∂ρ_j` for ALL (h,ρ) (T3-U) — on the frozen scene `h⊙G_A2 = G_A2`,
giving the h-form (T3-B). The leak is not noise; it is the exact coupling current to the frozen
capacity background. Completing the tensor by the capacity diagonal (making the diagonal part
of the carried object) restores conservation identically. That is a physics statement with an
exact discrete identity behind it — strengthened by the repair: the law is now
parametrization-honest (universal in u = log h; the old h-variable "iff Boolean" was a
parametrization artifact and is retracted, §11), with the global Euler balance as its
integrated form.

**(c) The precise disanalogies with GR (conceded up front, load-bearing for honesty).**
1. In GR `div G = 0` IDENTICALLY (Bianchi), and the field equation is `G = κT` with `div T = 0`
   forced. "`div G_A2 = source`" is NOT the GR field equation and this memo never calls it
   Einstein's equation. The correct continuum analogue of T1+T3 is the *background-dependence /
   Noether* statement, not `G = κT`.
2. The source `4·deg` is NOT Poisson-admissible (P1: non-neutral, total `8|E| = 2872`), so this
   is not the §07.32 weak-field skeleton either; it lives at the tensor-divergence level.
3. The owned CORE law shape `K ~ ϱ` (F11) pairs curvature-defect with *closure-density* (cycle
   frequency). Our identity pairs divergence-defect with *boundary-cut/edge-capacity density*.
   Same shape (local geometric object = local density), DIFFERENT owned types; no
   identification claimed.

**(d) The factor −2 and the trace-mode fact.** `G_A2 − 4D_M = −2·(2L_M)`: the conserved part of
the a2 metric response is *minus twice* the owned einsteinResponse. Consistent with BOOK_07:1782's
`Tr(G) = 4|E| = 1436` for `G = 2L`: the completion diagonal carries total `Σ X = 8|E| = 2872 =
2·Tr(2L)` — arithmetic consistency, recorded, no further claim.

---

## 4. Ownership audit: is "deg = capacity/matter density" ownable?

**PRIMARY TYPING (gravity-native, adopted in repair — the route the pre-skeptic draft missed):**
"deg(j) = BoundaryCutWeight({j}) = 4·C(∂{j})." §07.41 owns `C(boundary S) =
BoundaryCutWeight(S)/4` (F15) inside the gravity sector itself ("Trace-Heat-Capacity Gravity"),
and the compact statement owns "boundary cut capacity is holographic area" (BOOK_07:1770-1771).
On the unweighted scene the singleton cut IS the degree (independent count, T5), so

```
(div G_A2)_j = 4·BoundaryCutWeight({j}) = 16·C(∂{j})
```

types the leak as **boundary-cut / holographic-area density** using only gravity-sector owned
objects — no cross-sector borrowing. This is the load-bearing typing for reading R.

**SECONDARY TYPING (edge-capacity — ownable, but with a recorded cross-sector tension):**
"deg(j) = the node-local edge capacity." Chain: edges are owned as "inter-nodal transport
capacity" (F8, 1-skeleton) with total `|E| = 359` owned as "the topological capacity" (F9);
`deg(j)` is by definition the number of scene edges at j; the shell degrees `{24,22,20}` are
owned scene invariants (F6); and the degree already functions as an information-capacity
normalizer inside an owned action (F7). Also owned at the ACTION level: the a2 diagonal term IS
`Σ deg²/ρ²` (F3) — the "volume"/diagonal half of the owned a2 split.
**TENSION (recorded per skeptic #9):** F8 types the 1-skeleton capacity's FORCE reading as
*electromagnetism* ("This is electromagnetism", BOOK_02:1627), so bare "capacity density" as a
gravity-sector source borrows a quantity whose owned force-typing is EM. Resolution: edge-
capacity language is demoted to secondary; the holographic/boundary-cut typing (same number,
gravity-owned) is primary.

**NOT OWNED (and therefore not claimed):**
- "deg = matter density" / "T_μν". In the owned stratification matter is *edge-stress*
  (BOOK_07:1782, F5) and the VERTEX stratum is owned as *gravity/node-closure density* (F8,
  0-skeleton). If anything, the owned typing of the diagonal runs toward the gravity side, not
  the matter side. The owner-directive phrase "deg = the scene's matter/energy density" is
  therefore **rejected as stated**; the defensible phrase is "capacity density," with the
  0-vs-1-skeleton tension recorded honestly: `deg(j)` is a 1-skeleton quantity (edge capacity)
  localized at a 0-skeleton site (vertex) — it is the seam between the two owned strata, which
  is exactly where a coupling term should sit, but that last sentence is READING, not ownership.
- "pressure". Barred: F12 types pressure uniquely as `P_fb = β⁻¹ d_V log Z_N`. The leak is
  never called pressure here.
- Note also `24 = 11+13`, `22 = 9+13`, `20 = 9+11` (deg = complement-zone capacity sum): a
  correct arithmetic identity linking degrees to the owned zone capacities `9/11/13`; recorded
  as arithmetic, not as an ownership transfer.

---

## 5. Cross-link audit (the "one mechanism, three faces" candidate): TYPES DO NOT MATCH

Tested candidate: *Einstein-sector leak (div G_A2 = 4·deg) = archive-tracing probability loss
(per-tick rate φ⁻¹, trace-survival ≈ φ⁻⁵, F14) = determinant balance (active × archive = 1,
F13) — one owned archive flux seen three ways.* **Verdict: FAILS at ownership level. Exactly
where:**

1. **Ring mismatch (computed, P3).** The Einstein leak is ℤ-valued and static
   (`{96,88,80}`, total `2872`). The tracing scale is `φ⁻⁵ = −8+5φ ∈ ℚ(φ)∖ℚ`. Exact
   (1,φ)-arithmetic: no rational-coefficient identity connects them; a ℚ(φ) coefficient always
   exists because ℚ(φ) is a field — that freedom is a fitted conversion factor, i.e. naming
   freedom (trap j), refused.
2. **Algebraic-type mismatch.** The leak is ADDITIVE (a residual of a linear divergence
   operator, per node, no time evolution). The tracing loss is MULTIPLICATIVE per tick
   (`A_{t+1} = φ⁻¹A_t`); the determinant balance (F13) is multiplicative at the det level. The
   only standard additive↔multiplicative bridge is log-det — and the contract (F12) types the
   log-det object uniquely as feedback pressure `P_fb`, not as an Einstein-sector divergence.
   Retyping it would violate the CVFT hardening rule; not done.
3. **Carrier mismatch.** The leak lives on the 33-vertex scene diagonal (static tensor
   calculus); the tracing channel `ρ ↦ PUρU†P` lives on the archive/tracing carrier with a tick
   dynamics; the determinant balance lives on the time-automorphism spectrum. No owned map
   carries any one onto another (nothing in the campaign ledgers or the books supplies a
   per-node → per-tick transfer).

**What remains true and is recorded:** all three are instances of the M1 accounting *mechanism*
— what a projection removes is re-attributed, never deleted (the Laplacianization re-attributes
the diagonal; the tracing channel re-attributes trace to the archive; the det balance
re-attributes contraction to expansion). That is a mechanism-level rhyme, a READING, and it is
NOT minted. **Reopening hook (falsifiable):** the synthesis would close if an owned object ever
expresses the per-node capacity diagonal `4D_M` as the per-tick trace decrement of an owned
channel (equivalently: an owned map from `deg_M` to a contraction factor). No such owner text
exists today; if one is minted, this section must be revisited before any promotion.

---

## 6. DRAFT replacement text for BOOK_07:1770–1790 (IN-MEMO ONLY — no book edit performed; SPLIT per skeptic #9 to avoid the row-107 collision)

**Collision declared (F16):** the compact-statement closure line (~BOOK_07:1777, "Therefore the
Einstein-Hilbert / Einstein tensor class is the macro-interface ... closed finite-response
status") is the book text of `D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001` (CSV:107, LEAN_PROVED,
CORE_BRIDGE_SPLIT). The pre-skeptic draft rewrote it to "CANDIDATE" — a demotion colliding with
a LEAN_PROVED row. Repair: the motion is SPLIT.

**Motion 6-SAFE (no row-107 text touched):** leave the compact-statement block
(lines ~1766–1778) ENTIRELY unchanged; replace ONLY the stale first Iter26 block (line 1780 —
its "CERT-CLOSED ... `G_ij = dS/dh_ij = 2·L_ij`" contradicts the row-175 split: `2L` is
`dS/dL`, not `∂S_A2/∂h`) with the Iter27 block below, and adjust ONE clause in the line-1782
HODGE-LINKS block ("Positive partial (the closed leg, `D0-SPECTRAL-EINSTEIN-001`)" → "Positive
partial (the Laplacian-Bianchi leg of `D0-SPECTRAL-EINSTEIN-001`, CORE_BRIDGE_SPLIT)").

**Carry-over flag for the owner (skeptic #2, accepted):** wholesale replacement of line 1780
drops TWO TRUE items the stale block contains: (a) the √ρ-weighted Perron conservation remark
("for the weighted a₂ at the Perron measure the conservation holds in the √ρ-weighted sense —
the conformal Laplacian W_ρ L W_ρ annihilates √ρ"); (b) the scene response spectrum
`2·{0,20,22,24,33} = {0,40,44,48,66}`. Neither is falsified by this memo. DECISION REQUIRED at
apply-time: carry both over into the Iter27 block (recommended: append as a closing sentence)
or drop with justification. Not silently discarded.

**Motion 6-EXT (BLOCKED until the row-107 owner signs off):** optionally reword the ~1777
closure parenthetical to cite the completion identity. Any such wording must remain CONSISTENT
with row 107's LEAN_PROVED note ("Finite witness yields symmetric divergence-free second-order
TT-compatible macro interface; no continuum Einstein-Hilbert primitive is imported into core")
— i.e., the interface-class statement stays closed; only the parenthetical's mechanism citation
would change. Not drafted further here; requires the row-107 owner.

Proposed Iter27 block (the Motion 6-SAFE replacement for line 1780):

> **[Iter27 — the finite A2 Einstein sector carries TWO exact tensors, joined by one identity
> (`D0-SPECTRAL-EINSTEIN-001` CORE_BRIDGE_SPLIT + `D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001`;
> cert `einstein_field_eq_check.py`, exact ℚ, post-skeptic).** The a2 metric response
> `G_A2 = ∂S_A2/∂h = 4h_ij/(ρ_iρ_j)` is symmetric but NOT archiveDivergence-free:
> `(div G_A2)_j = 4·deg_M(j)` — on the frozen scene `4·deg(j) = {96,88,80}` — the NO-GO row.
> The conserved object is `G = 2L` (einsteinResponse, Laplacian-Bianchi) — the proved row.
> These are two halves of ONE exact identity: with `M_ij = h_ij/(ρ_iρ_j)`, `D_M` its degree
> diagonal, `L_M = D_M − M`,
>
> ```math
> G_{A2} \;=\; 4D_M \;-\; 4L_M \;=\; 4D_M \;-\; 2\,\mathrm{einsteinResponse}(L_M),
> \qquad \mathrm{div}\,(G_{A2} - 4D_M) \;=\; 0 \ \text{identically},
> ```
>
> with `X = 4D_M` the unique diagonal completion — the same Laplacianization move this book
> already uses for matter conservation (the HODGE-LINKS block below), instantiated at the a2
> response. The divergence failure is therefore not a defect of the finite theory: it is the
> exact statement that the a2 response couples to the frozen vertex-capacity measure. In the
> conformal variable the coupling law is UNIVERSAL: `div(h⊙G_A2)_j = −2ρ_j ∂S_A2/∂ρ_j` for all
> (h,ρ); on the scene (Boolean h) it reads `(div G_A2)_j = −2ρ_j ∂S_A2/∂ρ_j`, and globally
> `⟨h,∂S/∂h⟩ + ⟨ρ,∂S/∂ρ⟩ = 0`. On the scene the source is gravity-natively typed:
> `(div G_A2)_j = 4·BoundaryCutWeight({j}) = 16·C(∂{j})` with the §07.41 boundary capacity
> `C = BoundaryCutWeight/4` — a boundary-cut / holographic-area density. **Candidate reading
> (not a theorem):** this is a sourced divergence law — the finite analogue not of Einstein's
> `G = κT` (where `div G = 0` identically) but of the Noether statement that response-
> conservation fails exactly by the coupling to a non-dynamical background. Honest scope: the
> source is boundary-cut/capacity-typed, NOT "matter/energy density" (matter is edge-stress;
> the vertex stratum is gravity-typed in THE 02.19B; edge-capacity's force-typing is EM), NOT
> pressure (`P_fb` typing bar), NOT a Poisson source (non-neutral, `Σ = 8|E| = 2872`, while
> §07.32 requires neutrality). The EXACT-MISSING of the earlier split — a conserved Ĝ reducing
> to `G_A2` in a flat/decoupling limit — is CLOSED for ALL correction shapes by the flat-limit
> separation `||T − G_A2||_max ≥ 32/11` for every archiveDivergence-free `T` on the frozen
> scene: either the capacity diagonal is accepted as physical (this identity) or the
> carrier/divergence must change (BRIDGE-B/C, unchanged, jointly open with
> `D0-HODGE-LINKS-001`).

---

## 7. Pre-registered attack surface (strongest attacks against this memo, with answers)

**SA1 — "The identity is `L = D − A` times 4; first-year graph theory; the 'field equation' is
word-dressing."** Pre-registered and PINNED IN-SCRIPT (P2). The algebra is conceded to be
elementary — and post-verdict this concession deepened: T1 is now graded an INSTANTIATION of
the owned Laplacianization clause (F5/F17), not new algebra at all. The content is claimed ONLY
in: (i) *which* objects are variational/owned (`G_A2 = ∂S_A2/∂h` is the registry's NO-GO
tensor; `2L` is the registry's proved tensor; the identity welds two existing registry rows,
which no owned text previously did); (ii) the flat-limit separation T4-sep
(`||T − G_A2||_max ≥ 32/11` for every conserved T), which closes the ledger's EXACT-MISSING as
phrased for ALL correction shapes — a genuine registry-state change (uniqueness of the diagonal
completion is carried only as a one-line corollary of div-linearity, honestly labelled);
(iii) the measure-coupling law in its REPAIRED form — DEMOTED per skeptic #2: T3-U is the
generic per-node Euler-homogeneity identity (T3f pin), so leg (iii) reduces to the bidegree
ATTRIBUTION of `S_A2` (a true but thin content). Per the pre-registered fallback, the
ledger-changing content of SA1's answer now rides on **(ii) alone** — the flat-limit
separation T4-sep — with (i) as framing and (iii) as attribution.

**SA2 — "`div G = T` is not GR; in GR div G = 0 and T is separately conserved — so what does
'field equation' even mean here dynamically?"** Conceded and built into every statement: the
reading is the *Noether/background-coupling* analogue, never Einstein's equation (§3c). What it
means dynamically, precisely: for the frozen-scene variational problem, stationarity transfers
between the h-sector and the ρ-sector with zero net flux (T3 global), and the per-node budget
of that transfer is `4·deg_M`. No equation of motion for ρ is claimed (ρ is frozen; that is the
point). Anything stronger requires making ρ dynamical — an unbuilt construction, listed in §9
as the successor target, not claimed.

**SA3 — "4D is the trivial diagonal completion, not 'matter entering'."** Half conceded: the
completion is trivial algebra ONCE the divergence is computed; and the "matter" word is
REJECTED in §4 on the corpus's own stratification (vertex stratum is gravity-typed, F8). What
is not trivial: the completion move is the corpus's OWN owned matter-conservation move (F5),
and applying it to the a2 response lands exactly on −2·(the owned conserved Einstein object) —
a factor and an object nobody chose. The typing of the diagonal as capacity density is a
composition of owned facts (§4), the weakest of which (F7) is a usage, not a definition; if the
skeptic rejects F7 the chain F8+F9+F6 still supports "local edge-capacity" language.

**SA4 — "The Boolean-only scope of T3's per-node law smells post-hoc."**
RESOLVED BY KILL (skeptic #9; §11): the suspicion was CORRECT — the Boolean scope was a
parametrization artifact (trap g). The original "⟺ Boolean" claim is retracted: the law is
UNIVERSAL in the conformal variable u = log h (T3-U, no scope at all), the Boolean statement
survives only as the ⟹ direction where `G̃ = G_A2` (T3-B), and the honest h-variable
quantifier is "for ALL ρ simultaneously ⟺ Boolean" (T3-Q), witnessed both ways in-script
(T3d/T3e). The repaired law is STRONGER than the killed one; the kill is recorded, not defended.

**SA5 — "The breakthrough was supposed to be gravity-leak = archive-leak = decoherence; you
did not deliver it."** Correct, and stated as a computed negative (§5): ring, algebraic-type,
and carrier mismatches, each named; the mechanism-level rhyme is explicitly NOT minted; a
falsifiable reopening hook is registered. The deliverable of this memo is the identity + the
ledger dichotomy, not the triple-face synthesis.

**SA6 — "Registry duplicate: rows 175/548 already say all this."** They do not: row 548 ends
at "a conserved finite Einstein successor needs an explicit trace-reversal counterterm /
cross-carrier binding (BRIDGE-A/B/C), none owned." The instantiation of the Laplacianization at
`G_A2`, the general-(h,ρ) closed form, the flat-limit separation (which closes the BRIDGE-A
phrasing "reduces to G_A2 in a flat/decoupling limit" for ALL correction shapes — while
BRIDGE-A counterterms at general backgrounds remain unexcluded), the −2·einsteinResponse
equality, and the conformal measure-coupling law appear in no row, cert, or memo (pre-flight
§top; the ALGEBRA of T1 does have an owned parent — F5/F17 — which is exactly why T1 is graded
instantiation, not theorem).

**SA7 — "The ρ-derivative verification is circular (closed form checked against itself)."**
No: `∂S/∂ρ` is checked against an `a/t+b` model fit built ONLY from evaluations of `S_A2`
(three points, third validates the model). The first draft used a central difference, which is
exact for the h-sector (quadratic) but NOT for the ρ-sector (rational) — it FAILED, was
diagnosed, and was replaced by the exact reconstruction; the failure is recorded in §2 as
evidence the harness can fail.

---

## 8. What this does NOT show

- No continuum limit, no `G → Ric − ½R g`, no κ, no Λ: the Connes/Rieffel smooth bridge remains
  the external `D0-SMOOTH-MANIFOLD-PASSPORT`, untouched.
- No dynamics for ρ: the "source" is a frozen background's coupling current, not an evolving
  matter field. Making ρ dynamical (so that T3 becomes a two-sector equation of motion) is the
  successor construction, not claimed.
- No TT/graviton content: `D0-HODGE-LINKS-001` unchanged; the completed tensor is (−2×) the
  trace-mode object of BOOK_07:1782 and carries no TT part.
- No archive-flux identification (§5 negative, with hook).
- No new Lean object: T1–T5 are cert-level (exact ℚ). A Lean lift of T1 (pure matrix algebra
  over ℚ) is listed as a cheap candidate in §9, not performed.

---

## 9. Registry motions (PROPOSALS ONLY — nothing edited)

1. **UPGRADE (not demote) the NO-GO row's notes**, `CLAIM_TO_LEAN_MAP.csv:548`
   (D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001): keep status NO-GO for the bare claim
   ("G_A2 archiveDivergence-free" stays FALSE), append (post-skeptic text):
   > "[Iter-CA field-eq synthesis, post-skeptic#9] CONSERVED-COMPLETION IDENTITY (exact Q, all
   > h, all rho>0, cert einstein_field_eq_check.py, exit 0, mutation-tested): with
   > M=h/(rho rho), D_M its degree diagonal, L_M = D_M − M: G_A2 = 4D_M − 4L_M = 4D_M −
   > 2*einsteinResponse(L_M); X = 4D_M is the unique diagonal completion (uniqueness = div-
   > linearity corollary); div(G_A2 − 4D_M) = 0 identically. This INSTANTIATES the owned
   > Laplacianization clause (BOOK_07:1782; vp_hodge_links_carrier_nogo.py:70-82) at E:=G_A2.
   > MEASURE-COUPLING LAW (universal, conformal variable): div(h.G_A2) = −2 rho.dS_A2/drho for
   > ALL (h,rho); Boolean h ==> div G_A2 = −2 rho.dS_A2/drho on the scene for every rho; the
   > naive per-node 'iff Boolean' is FALSE (counterexample on a 4-cycle, regression-kept);
   > correct quantifier: holds for ALL rho simultaneously <=> h Boolean. Global Euler balance
   > <h,dS/dh>+<rho,dS/drho>=0. FLAT-LIMIT SEPARATION (supersedes the diagonal-only
   > no-decoupling): every archiveDivergence-free T has ||T − G_A2||_max >= 32/11 on the frozen
   > scene, so the EXACT-MISSING 'Ghat reducing to G_A2 in a decoupling limit' is UNSATISFIABLE
   > for ALL correction shapes — dichotomy: accept the capacity diagonal or change
   > carrier/divergence (BRIDGE-B/C; BRIDGE-A counterterms per se remain unexcluded, only their
   > flat-limit convergence to G_A2 is closed). TYPING: on the scene div G_A2 = 4*deg =
   > 4*BoundaryCutWeight({j}) = 16*C(boundary {j}) — gravity-native boundary-cut/holographic
   > typing (BOOK_07 07.41); edge-capacity typing secondary (its owned force-typing is EM,
   > BOOK_02:1627 — tension recorded); NOT matter/T_munu, NOT pressure (P_fb bar), NOT Poisson
   > (source non-neutral, total 8|E|=2872). Cross-link to archive tracing loss / det balance:
   > NEGATIVE at ownership (ring Z vs Q(phi), additive-static vs multiplicative-per-tick,
   > carrier mismatch); reopening hook = an owned per-node→per-tick map."
2. **Cross-ref on row 175** (D0-SPECTRAL-EINSTEIN-001), NARROWED per skeptic #9: append one
   sentence — the EXACT-MISSING clause is **superseded in the diagonal lane** and closed in the
   flat-limit reading for all correction shapes (T4-sep); `einsteinResponse(L_M)` appears as
   the conserved half of the a2 response for every (h,ρ) via the completion identity. (No
   claim that BRIDGE-A/B/C routes at general backgrounds are exhausted.)
3. **BOOK_07 edits** per §6 — SPLIT: Motion 6-SAFE (replace line 1780 + one clause in 1782;
   row-107 text untouched) may proceed on owner sign-off; Motion 6-EXT (the ~1777 closure
   parenthetical, row 107's book text) is BLOCKED until the row-107 owner reviews (F16).
   Book edits are outside this task's write scope either way.
4. **Optional cheap Lean lift:** T1 as matrix algebra over ℚ (`G_A2 = 4•D_M − 4•L_M` +
   row-sum-zero of `L_M`) directly extends `SpectralEinsteinResponse.lean`; no new axioms.
5. **No LEAN_ASSUMPTION_LEDGER row** (nothing imported; the reading is flagged as reading).

---

## 10. Summary (candidate, post-skeptic-repair)

The G_A2 divergence obstruction does not demote the Einstein sector — it *localizes the
coupling seam*. Exactly over ℚ, for every metric perturbation and every positive measure, the
a2 variational response splits as `G_A2 = 4D_M − 4L_M`: a forced capacity diagonal plus (−2×)
the corpus's own conserved Einstein response — an INSTANTIATION of the owned Laplacianization
move (BOOK_07:1782) at the registry's NO-GO tensor. The divergence of `G_A2` equals, on the
scene, `4·BoundaryCutWeight({j}) = 16·C(∂{j})` — a gravity-natively typed boundary-cut /
holographic-area density — and equals the action's coupling current to the frozen vertex
measure, UNIVERSALLY in the conformal variable (`div(h⊙G_A2) = −2ρ⊙∂S/∂ρ`, all backgrounds);
conservation is restored identically when the capacity diagonal is carried inside the tensor.
The ledger's open hunt for a "decoupling" conserved successor is CLOSED for all correction
shapes by the flat-limit separation `||T − G_A2||_max ≥ 32/11`. The grand cross-link to archive
trace-loss / determinant balance FAILS at ownership level (ring/type/carrier, each named) and
is left as a hooked negative. The field-equation *reading* is carried strictly as candidate
language with every unowned word flagged; one claim (the per-node "⟺ Boolean") was KILLED by
skeptic #9 and is retracted with a regression check (§11). Outcome: **OBSTRUCTION → IDENTITY
upgrade — instantiation-grade T1/T2, universal law T3-U, separation theorem T4-sep, typing pin
T5, scoped reading R.**

---

## 11. Skeptic verdict and errors of record (kills accepted in full, no defense)

**Skeptic #9 pass (2026-07-05), per-line verdict:** T1 WOUNDED→repaired (re-grade to
instantiation of owned F5/F17; false "built independently" sentence fixed); T2 SURVIVES
(tautological re-check relabelled); T3 **KILLED** (⟺ direction false); T4 WOUNDED→superseded
by the stronger flat-limit separation; R/§4 WOUNDED→repaired (holographic typing adopted;
EM-typing tension recorded); §5 SURVIVES; §6 WOUNDED→split (row-107 collision declared);
§9 WOUNDED→narrowed.

**Follow-up skeptic #2 pass (scoped to the NEW load-bearing text), verdict: ACCEPTABLE-AS-
REPAIRED, one wound — repairs applied:** N1 T3-U WOUNDED→repaired (the universal law is the
generic per-node Euler-homogeneity identity of the per-edge bidegree; triviality pin added in
§0 + in-script T3f with the second action `S′ = Σ2h⁴/(ρρ)²`; SA1 leg (iii) demoted to
attribution, ledger content rides on (ii)); N2 T3-Q SURVIVES (⟸ inference valid — per-edge
coefficients forced to zero by ρ-variation; witness T3d/T3e illustrates, does not carry, the
∀ρ direction; T3e print-nit recorded); N3 T4-sep SURVIVES (inequality chain and 32/11 checked;
scope correctly frozen-scene); N4 T5 SURVIVES with the qualifier that §07.41's rule is
INSTANTIATED at S = {j} (region rule applied to a singleton — within the rule as written);
N5 §6 split SURVIVES with one wound repaired (carry-over flag added: the √ρ-weighted Perron
conservation remark and the response spectrum {0,40,44,48,66} in the stale 1780 block are true
and must be explicitly carried over or dropped at apply-time, owner decision); N6 §11
SURVIVES. No further passes ordered.

**Errors of record:**

1. **E1 (KILL).** The original T3 claimed `(div G_A2)_j = −2ρ_j∂S_A2/∂ρ_j ⟺ h Boolean`.
   FALSE. Counterexample (skeptic #9): `h = 3/5, 6/5, 6/5, 3/5` on the 4-cycle
   `(0,9),(0,10),(1,9),(1,10)`, rest 1, ρ≡1 — non-Boolean, law holds at all 33 nodes
   (per-edge deficits `h(1−h) = ±6/25` cancel pairwise at every touched node). The original
   harness's own iff-check exits 1 on this background: the two "both directions fired" probes
   passed by luck, not proof — a quantifier error (∃ probe failing ≠ ∀ non-Boolean failing).
   Trap (g) also fired: in the conformal variable `u = log h` the law is UNIVERSAL, so the
   Boolean scope was a parametrization artifact. Repair: T3-U/T3-B/T3-Q + regression T3d/T3e.
2. **E2 (over-grade).** T1 was headlined "theorem-grade candidate" while its algebra is the
   owned Laplacianization clause (BOOK_07:1782), cert-implemented at
   `vp_hodge_links_carrier_nogo.py:70-82`. Re-graded to INSTANTIATION (ownership strengthened,
   novelty narrowed). The in-script sentence "L_M built independently" was false; relabelled a
   definitional-expansion pin.
3. **E3 (over-reach in scope wording).** The pre-skeptic T4/SA1(ii) implied BRIDGE-A was
   killed; only its DIAGONAL lane was. Repair: T4-diag narrowed + the stronger T4-sep adopted
   (all correction shapes closed in the flat-limit reading; BRIDGE-A counterterms per se not
   excluded).
4. **E4 (typing gap).** The pre-skeptic §4 used "edge-capacity density" as primary typing,
   missing both the EM force-typing tension (BOOK_02:1627) and the gravity-native owned route
   `C(∂S) = BoundaryCutWeight(S)/4` (§07.41). Repair: holographic typing primary, tension
   recorded.
5. **E5 (collision).** The §6 draft rewrote the BOOK_07 ~1777 closure line — the book text of
   the LEAN_PROVED row 107 — to "CANDIDATE" without declaring the collision. Repair: motion
   split; row-107 text untouched by the safe motion.
6. **E6 (tautological checks presented as tests).** T2's Perron `div(G−X)=0` re-check and the
   original C6 "uniqueness test" were restatements of div-linearity. Relabelled in-script;
   uniqueness now carried as a corollary.
