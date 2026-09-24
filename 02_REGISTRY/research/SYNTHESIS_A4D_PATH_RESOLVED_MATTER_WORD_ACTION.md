# A4D path-resolved matter word synthesis

## Status

SYNTHESIS / RESEARCH TARGET.

This packet is not a proof owner and does not claim existence or uniqueness of the all-order matter comparison law below.

It integrates the terminal fixed-level results of PRs #70, #75, #76, #80 and #84 with the frame/observer packet and the separate golden refinement terminal of PR #86.

## 0. Executive synthesis

The fixed-level constitutive seam should no longer be phrased as “choose a coefficient c”, “choose a comparison jet S”, “insert a half-edge site”, or “find another Hodge star”.

PR #84 rules out the unlabelled single-center factorization on cells with nontrivial relative holonomy and simultaneously shows that the mandatory scalar two-edge second-jet constraints are soluble but nonselecting.

The surviving research target is therefore a path-resolved matter comparison/action on the already-owned archive path words.

Write schematically

```text
C_N(w ; e, n) : matter fiber at source(w) -> matter fiber at target(w)
```

where:

- `w` is an already-owned finite path word / incidence path from the PR #70 Cartan geometry;
- `e` is the uncentered solder/coframe background;
- `n` is an observer argument only if the frame law actually requires it;
- the located two-color placement `J` remains fixed and separate.

The central research question is whether one law `C_N` can simultaneously account for:

1. one-letter / first-jet data that reproduce the owned complete staggered `H(e)`;
2. two-letter mixed second-jet data whose scalar shadow contains the allowed `S`;
3. loop response equal to the owned relative/open holonomy rather than telescoping to the identity;
4. observer/frame covariance;
5. fixed-`J` contragredient dualization with the correct shifted anchors.

If such a law exists, the previously separate objects `c`, `S`, and parts of the nonlinear constitutive response become jets or shadows of one typed word action. If it does not exist, the obstruction must be stated at the level of typed word composition, background covariance, observer transport or located dualization.

## 1. Owned inputs

### Path geometry

PR #70 owns finite affine Cartan path geometry, oriented words, concatenation, endpoint/open transport, curvature/torsion diagnostics and the flat translation identity.

Path resolution is therefore not permission to introduce a new midpoint carrier. The missing datum is a matter representation/comparison of already-owned path information.

### First jet

PR #75 owns the complete uncentered staggered first jet `H(e)`, including:

- scalar endpoint polarization;
- half-average `A_r`;
- mixed Fock blocks;
- both corner paths;
- L=2 Nyquist and L=3 corner controls.

Any candidate `C_N` or induced energy law must reproduce this literal first jet rather than only a centered or pure-gauge shadow.

### Second jet

PR #80 owns the exact two-jet covariance algebra and the scoped output-site-local advective package.

In that restricted class:

```text
K_xi = M_(xi^2) D^2
```

while a universal `K`, coefficient `c`, and general comparison jet `S` remain unselected.

### Endpoint/overlap terminal

PR #84 owns:

- the scoped obstruction to one unlabelled common center in the presence of nontrivial relative holonomy;
- an explicit constants-preserving two-edge `S_patch`;
- a continuous nearest-neighbor family with the same mandatory distance-two constraints.

Therefore exact composition plus scalar support do not select `S).

### Frame / observer

`MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md` derives:

- the exterior lift on the existing 16-state carrier;
- observer-positive `h_n`;
- moving creators/contractions;
- raw solder frame action;
- Lorentz-restricted affine-link lift;
- the shifted-anchor boundary for located `J`.

The current Lean worker formalizes this substrate. It does not own the missing all-order comparison law.

### Golden refinement

PR #86 owns an internal Tower-C golden scale/trace law and a defect-bearing Tower-B RG residual interface.

It does not own a Tower-C -> Tower-B carrier map.

No `phi`, Bratteli state, measure, or record projection may be inserted into `C_N` as a construction input.

## 2. Typed separation that the research must preserve

There are at least two compositions and they must not be silently identified.

### A. Path concatenation at fixed background

For composable archive words:

```text
w1 : x -> y
w2 : y -> z
```

a path representation candidate should satisfy an appropriately oriented composition law such as

```text
C_N(w2 ++ w1 ; e, n) = C_N(w2 ; e, n) * C_N(w1 ; e, n)
```

after source/target fibers are typed correctly.

### B. Background / Cartan action groupoid

Pure-gauge or frame transformations alter the background. Their cocycle law may require evaluation at the transformed background:

```text
R(zeta ; e + d_f xi) R(xi ; e) = R(xi + zeta ; e)
```

The research must prove a bridge before identifying this law with path concatenation.

A candidate may use both structures, but must state which argument transforms and which composition is being applied.

## 3. Candidate energy-congruence hypothesis

A motivating hypothesis is that the same word action transports the constitutive energy, schematically

```text
W(e') = C_N(w ; e,n)^(-T) W(e) C_N(w ; e,n)^(-1).
```

This is a research hypothesis, not an owned formula.

The task must first determine:

- for which words `w` an induced background relation `e -> e'` is defined;
- whether `e'` is a path comparison, a frame/gauge transformation, or a genuine background deformation;
- whether the inverse exists in the relevant local category;
- whether the law is local/inverse-free after a parent formulation;
- whether the flat derivatives actually reproduce `H` and the accepted second-order constraints.

Do not write an untyped symbol `h_w` and assume every path word is a coframe deformation.

## 4. Word-length diagnostics

The research should organize exact controls by word type.

### Length one: edge letter

Recover the accepted first-jet edge data and distinguish:

- link transport;
- solder insertion;
- scalar bond/volume contribution.

The flat covariant differential alone is known not to reproduce the full energy jet.

### Length two, same axis

Recover the mandatory distance-two scalar comparison constraints and compare with `S_patch`.

A successful law may select one member of the continuous `S` family, but this must be derived from the word/frame law rather than imposed.

### Length two, mixed axes

Recover the literal corner structure and L=3 coefficient.

The two geometric paths must remain distinguishable before any holonomy relation is imposed.

### Loop / two paths with common endpoints

The relative response must retain the owned open/relative holonomy.

A law that telescopes every cell loop to the identity has fallen back into the terminally excluded unlabelled-center class.

## 5. Observer question

The observer `n` is a possible argument of the same law, not a new independent constitutive theory.

The central test is whether the moving observer-positive form removes or fixes the residual counting family while preserving the full first jet.

Possible outcomes:

1. observer/frame covariance selects the residual and the same `C_N` reproduces `H(e)`;
2. observer covariance is compatible but leaves the residual modulus free;
3. observer dependence is incompatible with Nyquist/corner/path data, so `h_n` remains a separate positive form rather than an argument of the constitutive comparison.

Do not identify `n=e_A` with physical time.

## 6. Located dual

The topological located `J` remains fixed.

For a typed primal word action, derive the dual action by endpoint-aware contragredience. The exact formula must use the correct source/target located maps; a schematic common-fiber expression

```text
C_D ~ J^(-T) C_P^(-T) J^T
```

is not sufficient on the archive because the anchors depend on Fock degree/subset.

The research must preserve:

- topological square/sign;
- Fock parity;
- shifted-anchor placement;
- distinction between common-fiber cofactor identities and sitewise archive covariance.

## 7. Exact hostile controls

At minimum:

- flat background;
- constant matter;
- pure gauge;
- constant harmonic strain outside `im d_f`;
- plaquette curl / two-path relative holonomy;
- L=2 raw Nyquist witness;
- L=3 corner witness;
- L=5 delta and non-delta second-order matrices;
- all Fock degrees and parity;
- signed Role permutations;
- exact rational A/B Lorentz boost with moving observer;
- fixed located `J` anchor comparison.

Use exact rational/symbolic controls rather than floating-point evidence.

## 8. Golden firewall

The fixed-level law must be constructed or obstructed without using `phi`.

Only after a typed `C_N` exists may a later task ask whether it survives inter-level coarse graining through the separately owned package

```text
(B_N, p_N, L_N^B, pb_(p_N), sigma_C).
```

That later question is not part of the fixed-level construction.

## 9. Truth firewall

Do not promote:

- a path transport into a physical all-order matter action without the energy law;
- the exterior lift into Spin;
- observer counting into Lorentzian spacetime norm;
- located `J` into a metric Hodge star;
- a pure-gauge cocycle into arbitrary-coframe covariance;
- `S_patch` into a unique selector;
- the output-site-local `K` into a universal second jet;
- golden scale into a carrier map;
- any fixed-N result into provenance-bearing stress or Einstein dynamics.

## 10. Research target

The next heavy research task is:

`EXP-A4D-PATH-RESOLVED-MATTER-WORD-ACTION`.

Its purpose is to construct or terminally classify the single fixed-N word law before any new stress/source task is opened.
