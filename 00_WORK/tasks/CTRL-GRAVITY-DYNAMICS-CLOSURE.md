# CTRL-GRAVITY-DYNAMICS-CLOSURE

## Class
CONTROL

## State
IN_PROGRESS

## Objective

Supervise the current finite gravity/matter closure seam without reopening already terminal lanes.

The flux-kernel, located-star and second-order theorem packages are landed.

PR #80 Lean-owns the second-order covariance algebra and scalar advective boundary; PR #98 owns the endpoint/overlap comparison boundary. The later sequence PR #101/#102, PR #107, PR #108 and PR #103 narrows the fixed-level seam further.

PR #109/#110/#111 move the frontier again.

The labelled word skeleton is Lean-owned. The linear exterior channel and its affine-shift blindness are Lean-owned. Most importantly, affine translation sensitivity itself is no longer missing: PR #109 constructs the exact research-theorem-ready nilpotent response

[
T_b=I+C^\dagger(b)P_0,\qquad
R_{\rm nil}(L,b)=T_b\rho(L),
]

with the correct affine semidirect law and a site-aware weighted-shift realization.

The earliest unresolved fixed-N datum is now the **solder–Cartan edge mismatch/comparison** joining two already-existing descriptions of the same Role edge:

```text
affine Cartan translation b_(x,r)
            ↕
raw solder/coframe edge datum
```

The candidate notation

```text
kappa_N(A,e; x,r) : V_x
```

is a packaging to construct or terminally classify, not a proved unique factorization theorem.

Current lanes are intentionally ordered:

```text
PR #113 nilpotent affine response + grading firewall
  → LEAN-OWNED

PR #112 transported-reference mismatch
  → EXP-A4D-SOLDER-REFERENCE-LEG-SECTION
  → construct/classify the source reference-leg / affine-origin datum q

parallel theorem-ready formalization
  → WRK-A4D-TRANSPORTED-REFERENCE-MISMATCH
  → WRK-A4D-AFFINE-ORIGIN-COVARIANCE-BOUNDARY

arbitrary-background finite graded E dressing
  → EXP-A4D-FINITE-GRADED-COFRAME-DRESSING
  → BLOCKED until a usable q/origin datum lands
```

The current durable synthesis is

`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md`.

Two typing firewalls are now central:

- `F_phi` is an invertible background trivialization, while `W_flux = I + H(e)` is a constitutive/Riesz section. `DW = H` does not imply `D F = H`.
- Degree-preserving conjugation cannot erase a nonzero degree-mixing `T_b`. The disappearance of the extra affine response on the exact pure-gauge diagonal must occur in the mismatch/comparison layer, not through a commutator shortcut.

The golden Tower-C↔Tower-B correspondence/index problem remains a separate inter-level lane. No `phi`, AF index or `k=n` rule belongs in the fixed-N elementary matter letter.

The scalar reverse-star no-go remains a separate object, not `J` and not the constitutive assembly `W`. The topological placement, positive matter energy, Lorentzian exterior form, local frame covariance, connection transport and gravity-source variation stay distinct typed layers until a theorem identifies them.

## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.


## Three-tower dictionary — do not conflate level indices

The nearby roadmap uses three distinct finite systems.

| Tower | Literal carrier / owner | Bonding or refinement | Meaning |
|---|---|---|---|
| A — record/profinite | `ArchivePoints n = Fin ((n+2)^4)` | flat integer-mod `archiveProjection` | informational inverse-limit record carrier |
| B — Role-phase/CAR | `ArchiveRolePhaseGroup N = Role -> ZMod (N+2)` | coordinatewise finite-set projection is owned; stronger group/operator naturality is separate | carrier of `D_H`, `J`, `H(e)`, coframes and Cartan geometry |
| C — golden Bratteli/AF | golden cylinder language / `M_phi` | Bratteli incidence, AF inclusion, Perron trace/scale | canonical golden refinement at algebra/trace/scale level |

Frozen separation:

- Tower A and the natural coordinate-wise product refinement underlying Tower B are NOT stagewise isomorphic under their accepted bondings; the first-step zero-fiber sizes are `6` and `16`.
- Tower C already has a recovered golden refinement owner and forced dimensionless Perron scale ratio `phi`.
- Tower B already has a surjective coordinatewise finite-set projection, but exact nearest-neighbor Laplacian projective compatibility is proved to fail for the accepted one-dimensional projection when `n>1`.
- What is missing is a typed Tower-C <-> Tower-B weld that explains the correct carrier/operator comparison. A common scale ratio is not a carrier map.
- `ArchiveSpatialHistorySplit` keeps history tick, cyclic A-phase, phi-ladder and observer structure distinct.

Durable synthesis:

`02_REGISTRY/research/ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`.

The current constitutive seam lives inside one Tower-B level. The golden/Role-phase weld is an adjacent strategic lane, not permission to reinterpret record refinement or physical time.

## Frozen now

The following are frozen current inputs to this CONTROL lane:

- the diagonal Role action `diagonalRoleTransport` / signed site-Fock transport and its commutation with the corrected `D_H`;
- the typed Role-cut owner with coefficients `143/117/99`, together with the `BalancedRole ≃ SpatialRole` weld/`iota` lane used by the landed flux owner;
- the solder metric with `eta=(+---)` and the internal `1+3` Role split;
- the corrected difference Hodge Dirac and the owned spatial shell of `D_H^2`, including the rank-96 shell for `L≥3`; the older cosine-hopping directional operator remains a different operator and must not be conflated with this shell;
- the moving differential `d_T`, curvature as its square, pairing-forced dual action and mixed moving Ward;
- PR #69: 24-dimensional self-adjoint radius-one Ward class, one-dimensional simultaneous Role-relabel invariant subspace, nonlinear constitutive nonselection and holonomy-compatibility nonuniqueness;
- PR #70: finite affine Cartan path geometry, exact flat translation gauge equal to `forwardGaugeCoframe`, open curvature/torsion, scalar Lie closure and the uniform bounded-radius closure no-go;
- PR #36 unit-weight guards (`rho1 ≡ 1`, including `rho1_inverse_edge_weight_eq_one` / `rho1_c1_middle_polar_discriminant`); this is flat/counting normalization, not a Lorentz-invariant metric statement.

Current frontier labels:

```text
LABELLED-LIST-CHAINSTEP-HOLONOMY-DESCENT-SKELETON-LEAN-OWNED
CHANNEL-L-EXTERIOR-AFFINE-SHIFT-BLINDNESS-LEAN-OWNED
AFFINE-TRANSLATION-SITE-RESPONSE-CONSTRUCTED-LEAN-OWNER-PENDING
SOLDER-CARTAN-TRANSPORTED-REFERENCE-MISMATCH-CLASSIFIED
SOLDER-REFERENCE-LEG-ORIGIN-SECTION-OPEN
FINITE-GRADED-E-DRESSING-BLOCKED-ON-REFERENCE-SECTION
```

Landed prerequisites:

```text
WRK-A4D-PRIMAL-DUAL-FLUX-ENERGY-KERNEL  (#75)
WRK-A4D-LOCATED-PRIMAL-DUAL-STAR        (#76)
```

Landed second-order formalization:

```text
MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY
+ MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION
→ PR #80
```

PR #80 owns the theorem-ready second-order and scalar advective packages while retaining `FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED` for the still-unselected general comparison jet / nonlinear action.

Active formalization lanes:

```text
PR #113
→ nilpotent affine T_b / R_nil + literal degree/parity boundary LEAN-OWNED

MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH
→ WRK-A4D-TRANSPORTED-REFERENCE-MISMATCH
→ Lean-own conditional kappa_q and T_(kappa_q) controls

MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH
→ WRK-A4D-AFFINE-ORIGIN-COVARIANCE-BOUNDARY
→ Lean-own full-affine origin covariance and the linear-only solder translation defect
```

Active fixed-level research lane:

```text
MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH  (#112)
→ EXP-A4D-SOLDER-REFERENCE-LEG-SECTION
→ derive, select, or terminally classify the source-fibre reference/origin section q
```

Blocked next research lane:

```text
EXP-A4D-FINITE-GRADED-COFRAME-DRESSING
→ do not start merely because #112 merged
→ start only after a usable q/origin datum lands or is explicitly adopted
→ then classify a finite graded background dressing with exact pure-gauge restriction and induced DW|_0 = H
```

PR #111 has landed the labelled-path skeleton and exact L=2 period. PR #110 has landed the Channel-L affine-shift blindness boundary. PR #109 constructed Channel B at research level, and PR #113 now Lean-owns that nilpotent affine response together with its literal degree/parity boundary. PR #112 closed the row/vector ambiguity and constructed the conditional target-fibre mismatch

```text
kappa_q(A,e;x,r) = A_(x,r)(q_r(x+r)) - solderLegVector(e,x,r)
```

with exact pure-linear frame covariance and flat/pure-gauge/pure-shift controls, conditional on a supplied reference leg.

The current research target is therefore no longer the B/E edge comparison itself. It is the selection/construction of the source reference-leg or affine-origin section `q`.

Fixed-level endpoint research is terminal in PR #84:

```text
MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION
→ MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW
→ ENDPOINT-OVERLAP-COMPARISON-NEW-PRIMITIVE-REQUIRED
```

The inter-level refinement research is terminal in PR #86:

```text
ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS
→ MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD
→ GOLDEN-SCALE-WELD-OWNED-CARRIER-WELD-MISSING
```

PR #86 owns the research-level three-tower audit and a defect-bearing renormalization interface based on the existing RG residual prototype. It does not own a Tower-C→Tower-B carrier map, period subsequence, located-`J` square, `D_H` intertwiner, `H(e)` transport, trace factor, or physical-time bridge. This strategic terminal does not enlarge this CONTROL's fixed-level constitutive exit condition.

`WRK-A4D-LOCAL-REVERSE-STAR-NOGO` is an independent scoped no-go. It does not repair, replace or block the located `J`.

## Current accepted owners

Do not reopen as generic searches:

- corrected cubical/CAR differential and Hodge Dirac;
- difference-Laplacian square, constant-fiber kernel and spatial shell;
- simultaneous signed Role/site-Fock symmetry;
- internal archive 1+3 split, with Role A only an internal positive label;
- typed Role opposite-cut weld and the 143/117/99 residual algebra;
- moving differential, pairing-forced dual action, path-Hodge stabilizer and moving parent Ward;
- finite chain link transport/curvature;
- solder Gram completion and centered coframe readout;
- affine Cartan path geometry, including exact `affineTranslation_flat_eq_forwardGaugeCoframe`;
- scalar Cartan Lie closure and the no-go on a lattice-size-independent uniformly bounded Lie-closed radius;
- constitutive radius-one Ward class, nonlinear nonselection, determinant-density freedom and holonomy-compatibility nonuniqueness;
- record/profinite vs Role-phase bonding separation (`6 ≠ 16` first-step fiber witness);
- golden Bratteli refinement `M_phi`, its trace ratio, and forced dimensionless Perron scale flow.

Merged formal owners relevant to this seam include PRs #64–#70, #74–#76 and #80; PR #75 owns the flux/first-jet kernel, PR #76 owns the located two-color `J`, and PR #80 owns the second-order / scalar-advective theorem package.

## Current frontier

### Flux-energy kernel

`WRK-A4D-PRIMAL-DUAL-FLUX-ENERGY-KERNEL` landed in PR #75. The algebraic complementary pairing, complete uncentered staggered first jet `H(e)`, independent flux energy, polarization/Riesz identity, Nyquist/corner controls and spatial-triad representation weld are Lean-owned. This does not select a nonlinear physical constitutive law.

### Located topological star

`WRK-A4D-LOCATED-PRIMAL-DUAL-STAR` landed in PR #76. The center-matched two-color placement, independent typed dual incidence, topological square, parity-even complement law, S4 orientation pseudoequivariance and chirality-correct Dirac conjugacy are Lean-owned. This is a placement/counting owner, not a Lorentzian metric star.

### Reverse-star locality no-go

`WRK-A4D-LOCAL-REVERSE-STAR-NOGO` landed in PR #74. The scoped theorem rules out uniformly bounded translation-covariant forward/reverse scalar stars with exact inverse composition for the accepted neighboring scalar first jet. Inverse-free parents, nonlocal inverses, enlarged fibers and the located two-color `J` remain outside that no-go.

### Frame/CAR lift

PR #103 landed terminal

`FRAME-CAR-PATH-TRANSPORT-SUBSTRATE-OWNED-CONSTITUTIVE-WORD-ACTION-MISSING`.

The repository now Lean-owns the 16-state exterior frame lift, observer-positive form, raw solder frame action, Lorentz-restricted affine-link lift, covariant linked differential, exact exterior path transport, relative holonomy, frame covariance, located-anchor obstruction and Nyquist/pointwise boundaries.

This closes Channel L as a substrate. It does not make the current exterior path action affine-translation sensitive and it does not assemble the complete `H(e)` as the derivative of a finite elementary matter letter.

### Second-order Cartan/cell-energy integrability

PR #80 lands the accepted second-order package. Lean now owns the exact two-jet congruence algebra, generic/L=5 witnesses, scoped background-independent representation no-go, constants-preserving rejection of c=1,2 under its explicit ansatz, action-groupoid and moving-differential second jets, transverse coframe Hessian modulus, reference strict-cell weights, the forced output-site-local advective derivative and K_xi=M_(xi^2) D^2, plus the scoped direct elementary-cell obstruction.

The terminal `FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED` remains: PR #80 does not select a universal `K`, a coefficient `c`, the comparison jet `S`, or an all-order physical action.

### Common-center matter action

The durable packet `MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md` sharpens the nonlinear frontier.

Within the output-site-local scalar class, exact groupoid composition forces

```text
(D_e g_xi)_0[h] = - M_xi H_0(h) D
K_xi = M_(xi^2) D^2
```

and the induced Hessian has unavoidable same-axis distance-two entries, excluding a direct elementary-cell invariant energy in that scoped class.

For general scalar lifts, the remaining flat comparison freedom is

```text
B(xi,h) = B_adv(xi,h) + S(h_xi,h)
S : Sym^2(im d_f) -> End(C^0)
```

with strict cell support already forcing nontrivial distance-two components of `S+S^T`. The graded pure-gauge benchmark reproduces all blocks of `H(d_f xi)`, including Nyquist/corner, but does not extend to arbitrary uncentered coframes, harmonic strain or boosted raw solder backgrounds.

PR #84 sharpens the fixed-level seam terminally. An unlabelled single-center factorization is scoped-obstructed by nontrivial relative holonomy, while the scalar support constraints themselves are soluble and nonselecting: an explicit two-edge `S_patch` cancels the forced distance-two entries and a continuous nearest-neighbor family preserves the same mandatory constraints. The earliest fixed-level datum is therefore a typed path-resolved incidence comparison primitive with relative-holonomy response, full-`H(e)` flat derivative, observer/frame law and fixed-`J` dualization. No all-order physical action is selected.


### Endpoint comparison / overlap terminal

PR #84 lands `MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW.md` with terminal `ENDPOINT-OVERLAP-COMPARISON-NEW-PRIMITIVE-REQUIRED`.

At research level it owns a scoped loop obstruction for one unlabelled center on nontrivial relative holonomy, a minimal path-resolved incidence comparison signature and overlap law, an explicit constants-preserving two-edge scalar comparison jet satisfying the mandatory L=5 distance-two constraints, and a continuous nonselection family. Harmonic/curl, L=2 Nyquist, L=3 corner, observer/frame, fixed-`J`, locality and transverse-modulus boundaries are explicit.

This is not a universal matter/comparison no-go. A path-resolved primitive and inverse-free local parent remain possible but are not owned.

The older path-word and three-channel synthesis packets remain provenance, but the active frontier is now `SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md`.

Channel B is constructed at research level, so "affine-shift response missing" is stale. The immediate missing datum is a covariant B/E edge comparison. Only after that comparison lands may the blocked finite graded E-dressing task ask for an arbitrary-background extension of the pure-gauge `F_phi` chart.

The owned `H(e)` constrains the induced constitutive tangent, not the full tangent generator of an arbitrary finite dressing; its skew part remains a classification problem away from the exact-coframe orbit.

### Adjacent inter-level refinement seam### Adjacent inter-level refinement seam

PR #86 terminally classifies the current golden/Role-phase research lane as

`GOLDEN-SCALE-WELD-OWNED-CARRIER-WELD-MISSING`.

D0 owns the internal Tower-C golden Bratteli/trace/scale law and the existing Tower-B finite-set projection / RG residual machinery. The memo strengthens “shared scale only” to a falsifiable defect-bearing interface:

```text
R_N(c) = L^B_(N+1) - c · pb_(p_N)(L^B_N)
R_N(c) = 0  iff  declared renormalized compatibility holds
```

but the scalar `c` becomes golden only after a separately typed assignment `sigma_C`; no Tower-C state, word, measure or carrier is transported by this interface.

The earliest missing inter-level datum is therefore the typed comparison package

```text
(B_N, p_N, L_N^B, pb_(p_N), sigma_C)
```

with source/target types and Role equivariance. Located `J`, corrected `D_H`, `H(e)`, trace/measure and physical time remain separate downstream obligations.

PR #99 Lean-owns the scalar golden/RG defect interface while preserving the carrier-weld terminal. `EXP-A4D-GOLDEN-ROLE-PHASE-CARRIER-OPERATOR-WELD` now asks for the first actual carrier/function-space/algebra/operator comparison beyond the scalar probe. This strategic lane is adjacent to, not part of, the fixed-level constitutive exit condition.

### Stress/source

No provenance-bearing Lorentz stress is promoted until one all-order matter action exists. Stress must then be defined by variation of that same action. Independent connection Euler terms from the moving Ward remain unless their own EOM is imposed.

Existing `A4DLinearizedMetricResponse` is a finite response owner on `LocalSymRoleField`; it is not BOOK F_N, matter stress or an Einstein tensor without a bridge.

## Scene boundary

The typed Role residual, if coupled, follows:

```text
99-cut → e_spatial → Q(e) → S_J(e) → matter
```

Do not use a direct scene-to-shell embedding as the canonical coupling. The 48-dimensional shell intertwiner space answers a different representation question.

## Truth firewalls

Do NOT:

- identify Role A with physical causal time;
- identify the topological located J with a Lorentzian metric star;
- identify a positive counting/observer energy with the Lorentzian exterior form;
- identify shell compression with BOOK F_N;
- identify scene residual with matter state or stress;
- suppress moving connection/differential terms in Ward identities;
- use numeric refinement traces as action-level refinement maps;
- identify flat record `archiveProjection` with Role-phase geometric refinement;
- identify Bratteli/AF depth, Role-phase period, record depth or history tick merely because each is indexed by a natural number;
- infer physical time from the golden refinement scale;
- re-open the historical cosine-hopping mismatch as if it applied to the corrected difference Hodge Dirac;
- infer continuum Einstein dynamics from a finite Role-matrix response;
- treat the PR #108 infinitesimal cycle-sum/plaquette theorems as if they were already exact nonlinear relations of the unknown finite letter;
- insert golden `phi`, AF index data or a `k=n` rule into the fixed-N elementary matter letter;
- reopen `Q`, `S` or `K` as independent selectors before the current edge-comparison / graded-dressing seam is resolved;
- use `[H,T_b]` as a mechanism for erasing a nonzero degree-mixing affine translation response;
- identify the pure-gauge trivialization `F_phi` with the constitutive/Riesz section `W_flux`, or infer `D F = H` from `D W = H`;
- claim uniqueness of the finite graded E dressing from `H` alone; at first order `H` fixes only the symmetric part of the dressing generator.

## Throughput policy

Preserve the warm Lean/Mathlib cache. Use narrow builds during implementation and one incremental `lake build D0.All` before PR/REVIEW. Do not run `lake clean` or delete caches without an explicit CONTROL/release reason.

## Exit condition

This control closes the current research/formalization gate when:

1. the located two-color `J` is Lean-owned;
2. the complete first jet `DW|_0 = H` / flux-energy kernel is Lean-owned;
3. `D^2W|_0` and the matter second-jet boundary are either classified or terminally no-go;
4. the frame/CAR lift is independently classified in its parallel lane;
5. the post-PR-112 B/E seam is closed in order: the nilpotent affine translation response is Lean-owned with its grading boundary; the conditional transported-reference mismatch is made intrinsic by constructing/selecting a source-fibre reference-leg or affine-origin section `q` (or terminally identifying the earliest full-affine-solder/selection primitive needed for it); and only after a usable `q` exists is an arbitrary-background finite graded E dressing constructed or terminally classified with exact pure-gauge specialization and induced constitutive first derivative equal to the complete owned `H(e)`, including transverse skew-generator freedom.

Provenance-bearing stress/source and continuum Lorentz/Einstein promotion remain downstream gates; this CONTROL must not claim them closed merely because the current constitutive seam is classified.
