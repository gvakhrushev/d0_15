# TASK W8 REPORT — Π sweep + the "simultaneously" dig

**Executed by:** chief researcher (Charge B + adjudication) and a sweep agent (Charge A inventory).
Status language: findings only; no registry row edited; no promotion claimed.

## Charge A — Π sweep: verdict FAILS-AS-STATED, but the failure mode transforms the reduction

**Sweep inventory (agent, adjudicated by architect).** ~19 generation-tagged owned rows classified:
7 EQUIVARIANT (cardinality counts, Q₈ ranks, return orders, anomaly sums, Lucas traces, S₃-symmetric
baryon sector), 3 BRANCH-KEYED (typed frame degrees 24/22/20; the (1,4,3) pattern; P¹(F₂) count),
3 PASSPORT (PMNS, CKM decimals, K-theory), and a cluster flagged Π-VIOLATOR rooted at
`D0/Matter/GenerationSelectorOrigin.lean` (ordinal selector `diag(0,1,2)`, adjacency selector on the
chain 0-1-2, commutator = −1 at (0,1); inherited by `GenerationOverlapResponseOrigin`,
`CKMNontrivialFlavourAlgebra`, `MesonDefectTransferOrigin`, claims `D0-TORUS-GENERATION-SELECTOR-001`,
`D0-TORUS-GENERATION-OVERLAP-001`).

**Adjudication of the violator call (architect, from the source file):**

1. The agent's falsification mechanism ("relabel 0↔1 and the commutator becomes 0") freezes the
   selector definitions while moving labels. Conjugating BOTH selectors — the correct transport —
   moves the −1 entry to (σ0, σ1): `[σAσ⁻¹, σBσ⁻¹] = σ[A,B]σ⁻¹`. The exported property
   `SelectorsDoNotCommute` (GenerationSelectorOrigin.lean:44–47) is an **existential** and hence
   S₃-invariant. The noncommutation rows are covariant, not label-pinned: **not Π-violators in the
   outcome-affecting sense.**
2. What the sweep DID correctly expose: the chain order 0-1-2 is not a bare convention — its owned
   source is **torus shell geometry** (`torus_geometry_forces_generation_selector_noncommute`,
   lines 58–67: `radialAdjacency` vs `phaseDrift`, from `D0.Geometry.TorusCore13GeometryOrigin`).
   Radial shells are ordered by radius. **The scene-side generation triple is therefore plausibly
   NOT S₃-symmetric but intrinsically radially ordered** — premise Π was wrong in formulation, not
   in spirit.

**Consequence for the T2′ reduction (transformed, not killed):** if both triples are intrinsically
ordered — Q₈ by ranks (1,4,3), scene by the radial chain — the S₃ freedom collapses on each side
separately, and the residual object is no longer a 3!-bijection but a single **order-matching rule**
(which owned order corresponds to which). The reduction's conclusion revises to: the X5 contract's
content = (order-matching rule) + (P_iso scene half, below). Strictly smaller than a free bijection;
not zero.

## Charge B — the "simultaneously" dig: no-touch at proof-term level, then PAID internally

**No-touch (as suspected).** `UnifiedTheorem.lean` is a conjunction of independently proved facts:
`Q8Terminal.branch_orders` (traces of explicit 8×8 idempotent literals) ∧ `TerminalReturn.Umu_order4 /
Utau_order3` (bare 4×4 / 3×3 permutation literals). No shared definition; the "simultaneously" of the
docstring is, at proof-term level, `[1,4,3] = [1,4,3]`. The module header itself marks the chain
CONDITIONAL-EXTENSION ("the holonomy λ, … are chosen, not forced").

**The touch exists and is now exhibited** (`w8_holomorph_check.py`, exact ℚ arithmetic, RESULT: PASS,
11 checks, 1 reachable negative control):

ONE module — ℂ[Q₈] with the holomorph pair (left translation `L_i`, automorphism `α = (i j k)`) —
carries all three structures simultaneously:

- `α` is a genuine algebra automorphism (intertwines the regular rep: `P_α L_g P_α⁻¹ = L_{α(g)}`,
  all g; the non-automorphism i↔j swap fails this — negative control);
- `α` preserves each Fourier block E₀, E₄, E₃ and **3-cycles the character idempotents inside E₃**
  (`e_B → e_C → e_D → e_B`) — the Utau pattern, now as an owned action;
- `L_i` has order exactly 4 and its restriction to the ⟨i⟩-span `{1, i, −1, −i}` **is verbatim the
  Umu literal** of `TerminalReturn.lean`;
- E₀ is the common fixed block of both actions (`αE₀α⁻¹ = E₀`, `L_i E₀ = E₀`) — the unramified
  electron as the fixed point of the holomorph action.

The choice of axis i (over j, k) is Out(Q₈) ≅ S₃-covariant — the same naming gauge as everywhere
else; no new catalog enters.

**What this pays and what it does not.** It pays the **Q₈-internal half of P_iso**: the Fourier ranks
(1,4,3) and the return cycles (4,3) with fixed block are readings of one owned-constructible module,
not an integer coincidence. It does NOT pay: (i) the **scene half** — connecting this module to the
phason generation modes (`PhasonStrainGenerations`, Tr(T²)=3) and the radial shell chain; (ii) the
**order-matching rule** of Charge A's consequence. Sharpened P_iso: *exhibit the owned map from the
torus-shell radial chain to the holomorph module under which radial order corresponds to the
rank/return structure* — one object, precisely posed.

## Skeptic's paragraph (strongest surviving objection)

The holomorph module lives entirely on the Q₈ side; the zone correspondence `Q₉↔E₀, Q₁₁↔E₄, Q₁₃↔E₃`
is documented in `Q8Terminal.lean` as a "fixed correspondence (consumed downstream)" — i.e. a frozen
choice, and the unified chain is CONDITIONAL-EXTENSION by its own header. Nothing above forces the
scene zones to route through this module at all; a hostile reader may grant every check here and
still say the generation triple's connection to Q₈ is an attractive convention. The reduction now
hangs on exactly two nails — the order-matching rule and the scene half of P_iso — and if either is
unforceable, the honest endpoint is a minimal X5 contract with those two (and only those two) as its
postulated content. That endpoint would still be strictly smaller than the current contract.
