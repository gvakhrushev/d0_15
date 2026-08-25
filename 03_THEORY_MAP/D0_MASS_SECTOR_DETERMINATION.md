# D0 mass sector: exact determination ladder and final scalar frontier

## Result

The mass sector is no longer described by an undifferentiated statement that “a Yukawa
selector or metric is missing.” The internal theory now factors the problem into seven exact
stages:

| stage | theorem | exact information state |
|---|---|---|
| qualitative Yukawa profile | T32 / N8 | infinite coefficient fiber |
| unordered transport spectrum | T33 | fiber cardinality at most `3! = 6` |
| real-root order | T34 | unique increasing root enumeration |
| abstract orientation audit | T35 | increasing/decreasing residue is `ℤ/2` |
| structural generation bridge | T36 | shell order fixes the increasing orientation |
| physical branch naming | T37 | `electron/muon/tau` uniquely map to `inner/core/outer` |
| shell metric classification | T38 / N9 | exactly one positive modulus `g`; order cannot select it |
| joint completion boundary | T39 / N10 | coefficient and metric coarse profiles remain jointly non-selective |
| transfer shape | T40 / N11 | linear shell readout is equally spaced; the transfer must be nonlinear |
| minimal nonlinear completion | T41 | unique normalized quadratic `u/3−u²/12`; degree exactly two |
| saturation law | T42 | outer shell is the unique vertex; exponent increments compress exactly `3:1` |

The resulting typed chain is

```text
electron → innerD9 → lowest transport root
muon     → coreD11 → middle transport root
tau      → outerD13 → highest transport root
```

and contains no metric parameter.

## New synthesis: the residual is one-dimensional

For every admissible `TorusParameter a` define

```text
g = radius(coreD11) − radius(innerD9).
```

The Lean owner `D0.Synthesis.MassSectorMetricUnderdetermination` proves

```text
g = (a−1)/2 > 0,
radius(innerD9) = 1,
radius(coreD11) = 1+g,
radius(outerD13) = 1+2g.
```

The second adjacent gap is also `g`. Conversely any positive rational `g` reconstructs the
unique admissible parameter `a=1+2g`. Therefore

```text
TorusParameter ≃ { g : ℚ // 0 < g }.
```

This is stronger than saying that metric values are unknown. It proves that:

1. the shell-profile shape is fixed;
2. equal spacing is fixed;
3. the unit inner normalization is fixed;
4. only one positive scalar remains;
5. changing that scalar does not change any branch/shell/root label.

## Exact no-go

The currently owned radial-order code records only

```text
inner < core,   core < outer.
```

It equals `(true,true)` for every `g>0`. In particular:

```text
a=2  ↔  g=1/2  ↔  (1, 3/2, 2),
a=3  ↔  g=1    ↔  (1, 2,   3).
```

These metrics are different but their order, physical naming and transport-root labeling are
identical. Lean proves the general statement: any predicate on `TorusParameter` that factors
only through this order code is constant on the admissible family and cannot have a unique
winner.

## Final mass-sector frontier

The remaining owner `D0-PRIM-WINDING-METRIC-001` is now narrowed to one input:

```text
select one positive scalar g.
```

The needed completion must be genuinely gap-sensitive. Viable information types include:

- a dynamical stationarity equation for `g`;
- a Green-resolvent pole or residue condition;
- an EFT/IR matching functional;
- a measured, preregistered metric passport.

Repeating non-degeneracy, irrationality, ordering, shell naming or root-labeling arguments
cannot close this frontier: T38 proves that all of those data are constant while `g` varies.
The empirical mass spectrum is still external, and no theorem here identifies shell radii
directly with PDG masses.

## Joint completion theorem

There are two residual axes:

```text
k = non-scalar Yukawa coefficient triple,
g = positive shell gap.
```

The current theorem-level readout of `k` is its qualitative equality/rationality profile; the
current readout of `g` is its radial order. T39 proves that the combined readout is constant on
the full product of non-scalar coefficient candidates and positive metrics.

The stronger statement is an information contract for any proposed completion:

1. If it is coefficient-profile blind, even exact knowledge of `g` leaves infinitely many
   coefficient candidates.
2. If it is radial-order blind, even exact coefficient sensitivity leaves the positive metric
   fiber.
3. Hence unique selection must break both equivalence relations.

This does not force two separate fitting parameters. A single cross-functional
`F(k,g)` can in principle distinguish both axes. But a claimed completion must demonstrate
load-bearing dependence on both `k` and `g`; dependence on only one axis is theoremically
insufficient.

## Transfer must be nonlinear (T40)

The completion is further constrained in *shape*, not only in which variables it touches. A
linear readout of the shell radii,

```text
m(s) = α + β · radius(s),
```

has, on `(1,1+g,1+2g)`, both adjacent gaps equal to `β·g`. Its discrete second difference is
identically zero and its total span is exactly `2·(first gap)`, for every `g, α, β`. Equal
spacing is therefore a parameter-free structural invariant of every linear shell map.

The owned charged-lepton Puiseux row `(0, 1/4, 1/3)` has gaps `1/4` and `1/12`. Because these
are unequal, the row is not affine-reachable: no `(g, α, β)` produces it. The generation
transfer is genuinely nonlinear in the shell radius, consistent with the Green-function/Puiseux
owner and inconsistent with a linear rescaling of the shells.

## Unique minimal nonlinear transfer (T41)

The positive shell gap provides the intrinsic dimensionless coordinate

```text
u(s) = (radius(s)−1)/g.
```

For every admissible shell metric:

```text
u(innerD9)=0,  u(coreD11)=1,  u(outerD13)=2.
```

The unique quadratic interpolating the owned Puiseux row is

```text
P(u)=u/3−u²/12,
P(0)=0,  P(1)=1/4,  P(2)=1/3.
```

Lean proves that any quadratic matching these three values has coefficients
`(c₀,c₁,c₂)=(0,1/3,−1/12)`. Thus:

- the quadratic is independent of the free metric modulus after normalization;
- the discrete curvature is exactly `−1/6`;
- `c₂=−1/12<0`, so the transfer is strictly concave;
- T40 excludes degree ≤1;
- T41 constructs a unique degree-2 realization.

Hence the minimal polynomial degree is exactly two. This is not yet a derivation from a Green
resolvent: it is the exact interpolation shape that any successful resolvent construction must
reproduce.

## Saturation and increment compression (T42)

The unique polynomial also satisfies

```text
P(2)−P(u)=(u−2)²/12.
```

Hence `P(u)≤P(2)` for every rational `u`, with equality only at `u=2`. On the structural shell
carrier this makes `outerD13/tau` the unique saturation point, independently of `g`.

The two increments are

```text
P(1)−P(0)=1/4,
P(2)−P(1)=1/12,
```

so the first is exactly three times the second. This `3:1` law is an exponent-transfer result,
not a claim about physical mass differences.

## Owners

- `D0-YUKAWA-QUALITATIVE-SELECTOR-NOGO-001`
- `D0-YUKAWA-SPECTRAL-FIBER-LADDER-001`
- `D0-TRANSPORT-ROOT-LABELING-CANONICAL-001`
- `D0-MASS-SECTOR-ORIENTATION-BIT-001`
- `D0-GENERATION-ROOT-ORDER-BRIDGE-001`
- `D0-CHARGED-LEPTON-SHELL-BRIDGE-001`
- `D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001`
- `D0-MASS-SECTOR-COMPLETION-NOGO-001`
- `D0-AFFINE-SHELL-READOUT-NOGO-001`
- `D0-CANONICAL-PUISEUX-SHELL-TRANSFER-001`
- `D0-PUISEUX-TRANSFER-SATURATION-001`
- `D0-PRIM-WINDING-METRIC-001` (one scalar selection frontier)
