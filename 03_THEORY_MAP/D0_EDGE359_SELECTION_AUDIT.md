# Edge 359 selection audit

## Exact result

The edge count of a complete tripartite scene is

```text
E(a,b,c)=ab+ac+bc.
```

The source scene satisfies `E(9,11,13)=359`, but it is not the unique positive ordered
preimage. Complete enumeration gives 19:

```text
(1,1,179)   (1,2,119)   (1,3,89)    (1,4,71)
(1,5,59)    (1,7,44)    (1,8,39)    (1,9,35)
(1,11,29)   (1,14,23)   (1,17,19)   (2,9,31)
(3,5,43)    (3,13,20)   (4,11,21)   (5,7,27)
(5,11,19)   (7,10,17)   (9,11,13)
```

In particular:

```text
E(7,10,17)=359,
V(7,10,17)=34,
T(7,10,17)=1190.
```

So `359` does not reconstruct the scene.

## Lean boundary

`D0.Synthesis.Edge359SceneSelectionBoundary` proves:

1. the explicit source/rival collision;
2. edge-only non-injectivity;
3. every edge-only selector accepting `(9,11,13)` also accepts `(7,10,17)`;
4. the repaired theorem:

```text
a≤b≤c,  V(a,b,c)=33,  E(a,b,c)=359
    ⇒ (a,b,c)=(9,11,13).
```

Thus one independent scalar beyond `E` is sufficient. The pair `(V,E)` is selective; `E`
alone is not.

## Consequence for the α claim

The finite identity

```text
ζ_E(−1)=359 φ⁻²−φ⁻⁵
```

is exact on the selected scene. But its scene dependence is only through the edge coefficient.
Every `E=359` rival has the same structural α fingerprint. Therefore the identity cannot be
reversed into:

- an independent derivation of `(9,11,13)`;
- a validation of the scene by the α value;
- a second scene-selection route.

The earlier sweep claim that the D0 value was uniquely close to measured `α⁻¹` already failed
reproduction and is retired in `D0-EDGE-ALPHA-001`.

## Correct logical architecture

```text
explicit scene-selector hypotheses
              ↓
         K(9,11,13)
              ↓
          E = 359
              ↓
 metric / α / Yukawa / EH-proxy / S_DE readouts
```

The final row is a convergence theorem: several inequivalent operators consume one discrete
input. It is not five independent confirmations because the shared integer is a common cause.

## Robustness: the scene is over-determined (T44)

The dual result guards against the opposite error — thinking the scene is fragile or
cherry-picked through one invariant. With `V=a+b+c`, `E=ab+ac+bc`, `T=abc`:

| reading | solutions |
|---|---|
| `V=33` | 91 |
| `E=359` | 19 |
| `T=1287` | 10 |
| `(V,E)=(33,359)` | 1 — `(9,11,13)` |
| `(V,T)=(33,1287)` | 1 — `(9,11,13)` |
| `(E,T)=(359,1287)` | 1 — `(9,11,13)` |

No single count is load-bearing; every pair pins the scene. `(9,11,13)` is the unique common
solution of any two independent count readings (`D0-SCENE-INVARIANT-OVERDETERMINATION-001`).

## Remaining foundational frontier

The central open question is upstream: are all hypotheses used by the scene selector themselves
forced from M1 without an external catalogue? The canonical registry keeps the full cascade and
the extension-completeness joints as proof targets. Closing those joints would strengthen the
scene theorem. Reusing `359` downstream cannot close them.

T45 reduces the GAP-E/window part to one exact obligation. If `n` independent primitive detector
capabilities generate port powers, then

```text
all zones 9+2^k are ≤13  iff  n≤2.
```

The current unstratified comparison model admits history/order as a third primitive, reopening
size `8` and zone `17`. The missing theorem is therefore not another arithmetic bound: it is the
typed statement that every primitive M1-admissible detector comparison factors through current
membership/value data. `CurrentDataFactorization` already owns the quotient mathematics once
that premise is supplied.

T46 proves catalogue-independence: order/history consults an orientation catalogue, while
catalogue-free comparisons factor through current data. T47 shows this is not yet canonical
`M1Forced`: the catalogue-free class is non-singleton, so no unique forced witness exists. T48
identifies catalogue-free and history-invariant comparisons through their common bare
current-data carrier. T49 then proves the typed detector primitive carrier has exactly two
profiles, membership and value, and seals the port-power bound on that typed layer. The only
remaining seam is a class-level M1 representation of physical comparisons into the typed
detector layer.

That interface is now supplied by T50–T51. Class-level M1 admissibility is catalogue invariance;
unique-answer `M1Forced` is its singleton constrained special case. Any physical comparison class
with an explicit `PhysicalDetectorRepresentation` embeds into the typed detector layer and its
primitive images exhaust to membership/value. The foundational seam is therefore closed at
representation-interface grade. Concrete external systems carry the normal obligation to provide
and prove their instance fields.

T52 provides that instance for D0's actual finite observation system. Its two-sided catalogue is
essential for binary comparisons and yields class-M1 admissible iff fully history-invariant.
Therefore the concrete detector model embeds in the typed two-profile layer and closes the
detector-capability/zone-bound application chain.

## Owners

- `D0-SCENE-TRIPLE-UNIQUE-001`
- `D0-EDGE359-SCENE-SELECTION-NOGO-001`
- `D0-EDGE-INVARIANT-CROSS-SECTOR-001`
- `D0-EDGE-ALPHA-001`
- `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (upstream frontier)
- `D0-DETECTION-SCENE-BOUND-EQUIVALENCE-001`
- `D0-DETECTOR-CATALOGUE-FREEDOM-001`
- `D0-DETECTOR-M1-PREDICATE-BOUNDARY-001`
- `D0-DETECTOR-LAYER-EQUIVALENCE-001`
- `D0-TYPED-DETECTOR-PRIMITIVE-EXHAUSTION-001`
- `D0-M1-CLASS-ADMISSIBILITY-001`
- `D0-DETECTOR-M1-CLASS-REPRESENTATION-001`
- `D0-CONCRETE-PHYSICAL-DETECTOR-REPRESENTATION-001`
