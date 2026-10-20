# G0: complete scene-history valuations and the canonical trace consumer

Research input: `27175008f7dbba9a98bc739f6cde0958a53858e8` in existing #310.
Supported owner tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **complete statements for the explicitly typed history interfaces;
G0 physical-system ownership remains OPEN**. No action, logarithmic rule,
symmetry quotient, field constraint or physical postulate is selected.

This consumes the missing history-composition premise in
[G0](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md) and the already accepted
[A-PARENT boundary](APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md).
It does not reopen common finite-generator existence or the external report's
rejected isotropy shortcut. The source #310 and independent #202/#317 terminals
are unchanged.

## 1. Actual owners and exact interfaces

Under `03_FORMALIZATION/D0/` the consumed definitions are:

| Owner | Actual proposition/data | Boundary |
|---|---|---|
| `VNext2/ScenePathHistoryCanonicity.lean` | `SceneStep`, `IsSceneWalk`, `composePath`, `SceneHistoryFamily`; composition completeness equals all valid walks | Determines the carrier of histories, not a real scalar on it. Immediate returns are included. |
| `Claims/Signature31Split.lean` | `Adj31`, `zone31`, the literal graph K(9,11,13) | 33 vertices and 718 directed edges; not a periodic 4D field carrier. |
| `Foundation/EndogenousActionQuantum.lean` | `ActionProtocol.action_refl`, `.action_nontrivial`, `canonicalActionProtocol` | Pair costs are zero on the diagonal and at least one off it. History additivity is not a field of this structure. |
| `VNext2/ScenePerronTraceCanonicity.lean` | Unique positive root rho of x³−359x−2574 and normalized positive eigenprofile r | A positive eigenprofile is classified. An arbitrary history measure does not thereby become endpoint-central. |
| `VNext2/SceneHistoryPerronTrace.lean` | Exact depth-1/depth-2 counts, distinction from simple random walk, full-scene eigen-equation | The printed capstone contains the finite counts and random-walk distinction. Its header's all-depth cylinder assertion is not a conjunct of that capstone. Section 4 below supplies an analytic all-depth proof with explicit hypotheses. |
| `VNext2/SceneEndpointReynoldsExpectation.lean` | Endpoint fiber averaging C1, lifts Js/Jt and C1 Js=fullTransport | This is a backward conditional expectation, not the forward Perron transition law. |

The research capsule prints the actual `scene_history_perron_trace_owner`
type; names/comments are not promoted into additional propositions. Its
20 new/reused capsule declarations have only standard logical axioms.
The old finite owner is printed for scope inspection, not included in that
standard-axiom claim.

## 2. Complete additive action fiber on the actual path carrier

Let H be **all** nonempty valid scene walks, including singleton identities.
For composable p,q use the actual operation `p ++ q.tail`. Consider exactly
the real-valued maps S on H satisfying

```text
S([u]) = 0,
S(p ∘ q) = S(p) + S(q).
```

These are explicit hypotheses on a scalar reading; the canonicality of H
does not derive them. There is a bijection

```text
{all such S}  ≃  {all w : directed scene edges → R},
S_w([v0,...,vn]) = sum_{i=0}^{n-1} w(vi,vi+1).
```

Proof: restriction gives w(u,v)=S([u,v]). Every path is the concatenation
of its actual one-step arrows, so induction forces the displayed formula.
Conversely this formula respects the identity and composition laws.
Restriction and extension are inverse, on the full carrier, not a finite
sample. This is `completeAdditiveFiber` in Lean and directly consumes
`composition_complete_eq_all_walks`.

If the vertices are represented by a verification protocol with their
identity records, two verification lines and catalogue-independent equality,
the **entire** restriction of actual ActionProtocol costs to scene edges is

```text
w(e) >= 1 independently for all 718 directed edges.
```

Necessity is the literal primitive lower bound. Sufficiency: use the supplied
w on edges, cost one on other distinct pairs and zero on equal pairs.
The protocol satisfies the actual verification contract, as proved in Lean.
This is an explicit valid realization of that interface, not a claim that
the full physical D0 state equals Fin 33. A different physical state map has
its own admission obligation.

The canonical primitive cost restricts to w=1. Its unique additive extension
is the number of edges, n. In particular, `[u,v,u]` has additive cost at least
two for every primitive completion, while the primitive pair cost (u,u) is
zero. Therefore **forgetting a path to its endpoints does not preserve that
positive additive cost**. Reversal is a legal path; it is not the inverse
arrow in the free path category. No inverse cancellation is assumed.

## 3. Complete endpoint-boundary quotient, without physical-gauge promotion

For a connected graph, an additive scalar depends only on its initial and
final vertices exactly when

```text
w(u,v) = b(v) - b(u).
```

Proof: the displayed form telescopes. Conversely choose a path from a fixed
root o to every vertex v and set b(v) to its endpoint-dependent value.
Concatenate a root-to-u path with any u-to-v path. Endpoint dependence gives
b(v)=b(u)+S(path). The graph is connected: vertices in different zones are
adjacent; those in the same zone have a two-edge path through another zone.
No path-independence is silently imposed on a general w.

Thus the space of endpoint-boundary terms has dimension 33−1=32. A
nonnegative weight on both orientations can be a pure boundary only if it
vanishes on every edge. In particular no primitive unit-gap weight descends
to endpoints. The Lean capsule proves telescoping and the positivity
obstruction; connectedness/dimension and the converse above are analytic,
with exact incidence-rank controls.

For clarity, the full mathematical dimensions are:

| Scalar valuation class | Dimension | Modulo endpoint boundaries inside that class |
|---|---:|---:|
| All directed weights | 718 | 686 |
| Reversal-symmetric weights | 359 | 359 |
| Invariant under all scene graph automorphisms | 6 | 4 |
| Automorphism-invariant and reversal-symmetric | 3 | 3 |

Degrees 24,22,20 distinguish the zones, so every graph automorphism preserves
them; arbitrary within-zone permutations are automorphisms. There are exactly
six directed zone-pair edge orbits, or three after reversal. An invariant
boundary has a zone-constant b modulo a constant, giving dimension two.
A symmetric boundary is zero. This proves completeness of each row.

These are dimensions of scalar-action spaces and their stated mathematical
quotient. They are **not** dimensions of independent field Euler equations
or physical response. Those latter objects need a native field map and
admitted variations. Even after fixing w(0,9)=1, positive symmetric invariant
weights retain independent zone-pair values. Canonical scene/trace data do
not by themselves equate these supplied values.

### 3.1 What the actual endpoint average sees: a complete decomposition

The supplementary external certificate raises a different quotient: the
kernel of C1 on one-step edge readings. This has dimension 718−33=685,
because C1 Jt=I. It must not be confused with the 686-dimensional quotient
by endpoint-boundary actions above. There is a complete relation between them.
Write delta=Jt−Js, T=C1 Js, and 1_E for the constant edge reading. Then

```text
C1 delta = I−T,
R^E = ker(C1) ⊕ im(delta) ⊕ span{1_E}.
```

Proof: T is the actual connected simple random-walk matrix. If Tb=b, take
a vertex maximizing b; its value equals a positive average of all neighbors,
so every neighbor also attains the maximum. Connectivity gives b constant.
Thus rank(I−T)=32. The positive left stationary vector is deg(v); detailed
balance gives deg^T(I−T)=0. The range is therefore exactly the codimension-one
subspace of vertex readings with zero degree-weighted mean.

For any edge reading w put `c=(sum_e w(e))/718`. The vertex vector C1 w−c1
has zero degree-weighted mean. There is a unique b satisfying
`(I−T)b=C1 w−c1` and `sum_v deg(v)b(v)=0`. Then

```text
h = w−delta b−c1_E,      C1 h=0.
```

If such a decomposition is zero, applying C1 and the stationary mean first
gives c=0; then b is constant and its normalization makes it zero; h=0.
This proves directness and existence for every w. The dimensions add as
685+32+1=718. On fixed-length, fixed-endpoint histories only h can change
the additive value. This is a mathematical action quotient, not physical
gauge or a statement about native field Euler equations.

The hidden sector survives scene automorphism invariance. On directed
zone pairs define h_01=13, h_21=−9 and all other h_ab=0. Incoming sums vanish:
9·13+13·(−9)=0 at zone 1, and zero at the other zones. Thus C1 h=0,
while h is invariant under every graph automorphism. Both w0=2 and
w1=2+h/13 satisfy the actual unit-gap edge condition and C1 w0=C1 w1=2.
They share the fixed canonical history carrier and its trace. Nevertheless
the length-three paths `[0,9,1,20]` and `[0,20,9,20]` have identical
endpoints and their w1 values differ by 22/13; w0 gives equal values.
This is a full exact positive control against selection by those interfaces.
It does not assert physical nonuniqueness. Reversal invariance is an
additional restriction and is not satisfied by this witness; it is retained
as a distinct class in the table, not silently discarded.

## 4. All-depth endpoint-central trace: existence and uniqueness

Let A=Adj31, r(v)=1/(rho+n_zone(v)), sum_v r(v)=1, and
rho³−359rho−2574=0. The literal positive root satisfies 20<rho<24.

State the full class independently. A trace in this section assigns the
same nonnegative value f_n(v) to **every** length-n path ending at v,
is normalized at depth zero, and is consistent under all one-edge forward
extensions:

```text
f_n(v) >= 0,       sum_v f_0(v) = 1,
f_n = A f_{n+1},   for every n >= 0.
```

There is exactly one such infinite family:

```text
f_n(v) = rho^(-n) r(v).
```

Existence follows from Ar=rho r. If m_n=A^n 1 counts paths ending at v,
then A=A^T gives sum_v m_n(v) f_n(v)=sum_v r(v)=1 at every depth.
Consequently the formula defines a normalized measure on each finite H_n
and has exact cylinder consistency.

Here is an elementary uniqueness proof, including the needed uniform bound.
Put

```text
P_uv = A_uv r(v)/(rho r(u)),
g_n(v) = rho^n f_n(v)/r(v).
```

Then P is row-stochastic and g_n=P g_{n+1}. Every entry of A² is at least 9:
same-zone pairs have their common outside neighbors, different-zone pairs
have the third zone. Hence

```text
(P²)_uv = (A²)_uv r(v)/(rho² r(u))
         >= 9(rho+9)/(rho²(rho+13)) > 1/100.
```

The last inequality follows already from 20<rho<24: the numerator exceeds
261 and the denominator is below 576·37, so the ratio exceeds 1/100.
This arithmetic bound and the actual root bounds are compiled in Lean.
All higher P^m, m>=2, have the same entry lower bound, since multiplying
P² on the left by a stochastic matrix preserves it.

Writing P² as `(1/100) 11^T + (67/100) Q`, Q row-stochastic, shows
osc(P² x) <= (67/100) osc(x). This holds for all real vectors x.
For n>=2, g_0=P^n g_n and g_n>=0 imply

```text
max_v g_n(v) <= 100 max_v g_0(v).
```

For any fixed k, iterate g_k=P^{2m}g_{k+2m}. Its oscillation is at most
`(67/100)^m * 100 max g_0`, which tends to zero. Thus each g_k is a constant
vector. The recurrence makes the constants equal; depth-zero normalization
and sum r=1 give that constant one. This proves uniqueness for **all**
nonnegative endpoint-central infinite towers, without assuming stationarity
of f_n or extrapolating finite-depth eigenvector checks.

The all-depth contraction proof is analytic, not a compiled limit theorem.
Endpoint centrality is an essential hypothesis: a simple random walk with
initial mass 1/33 on each vertex defines another positive normalized,
exactly cylinder-consistent all-walks law. At depth one the paths `[9,0]`
and `[20,0]` have the same endpoint but masses 1/(33·22) and 1/(33·20).
Thus cylinder consistency alone does not select the Perron family.
Likewise a finite-horizon endpoint-central tower admits arbitrary nonnegative
terminal data, propagated backward and normalized. Finite depth does not
prove the infinite uniqueness theorem. Both exceptions are exact controls.

## 5. The actual Perron likelihood contains only length and boundary

Under the proved endpoint-central law, the probability of extending a path
at u by a legal edge (u,v) is

```text
p(u,v) = f_{n+1}(v)/f_n(u) = r(v)/(rho r(u)).
```

This is a derived forward conditional probability. Taking its negative
logarithm is an explicitly specified scalar reading, not a native physical
action postulate. It gives

```text
a(u,v) = -log p(u,v) = log rho + log r(u) - log r(v),
sum_path a = n log rho + log r(start) - log r(end).
```

These identities hold on every finite path, and are proved in Lean with
the literal sceneRho and fullScenePerronVector, not a numerical Perron fit.
The unconditional path mass is rho^(-n)r(end), whose negative log is
`n log rho - log r(end)`; adding the initial mass r(start) explains the
difference. The unconditional negative log is not identity-zero additive:
its composition defect is log r(junction). Conditional normalization removes
that defect. Neither form contains an interior path term at fixed length
and endpoints. Every normalized average supported on those paths has the
same scalar value. The weighted-constant identity is also compiled.

This forward transition is distinct from the simple random walk. From
vertex 0, the per-edge probabilities to zones 1 and 2 differ, whereas the
simple walk assigns 1/24 to both. Conversely, conditioning the Perron
history law on a fixed endpoint makes all paths in that fiber equiprobable;
at depth one this is exactly the owned uniform Reynolds average C1.
The two operators answer different conditional questions.

For any proposed field reading that uses only this fixed canonical
likelihood, preserves path length/endpoints, and introduces no extra
field-dependent weights or observable, its contrast is exactly zero.
This remains true for normalized mixtures supported in that fiber.
If an admitted physical metric probe has
`Delta I_h = c_V epsilon_h + o(epsilon_h)` with c_V nonzero, such a reading
cannot transfer it with a fixed nonzero calibration and O(h) error at
epsilon_h=h^(1/3): the contrast divided by epsilon_h has a nonzero limit,
whereas Ch/epsilon_h tends to zero. A merely nonzero finite contrast with
vanishing leading variation is insufficient for this inference.
This is a conditional consumer, not an
assertion that D0 supplies those field maps or that all its realizations
have fixed endpoints and length. Field-dependent coarse-graining,
changing carrier/length, variable conditional ensembles and additional
owned observables lie outside that zero-contrast statement.

## 6. What this settles and what remains in G0

Settled: the complete additive scalar family on the genuine all-walks scene
carrier; the complete primitive unit-gap edge restriction; the canonical
unit cost's length law; the endpoint-boundary quotient; the unique
nonnegative infinite endpoint-central trace; and the exact length/boundary
form of its logarithmic reading. The last two are not premises smuggled
in through the old capstone's comments.

Not derived: a native map from scene histories/records to the periodic
coframe/link/matter carrier, the admissible coupled field variations,
field-dependent scalar weights/observables and their refinement law,
or the Euler equations of a resulting geometric and matter action.
Canonical counting, a fixed positive trace and path additivity do not
specify that map. If a different history owner is used, its identification
with these scene paths must be proved; similarity of names is insufficient.

The next exact G0 obligation is therefore the **field-dependent history
readout/composition law**, or a complete independence theorem for the full
typed interface actually used by the field owner. Its admissible family
and physical response must be assessed together. A standalone choice of
edge weights, or an arbitrary functional on paths, does not supply it.
The own matter source/Ward, quantitative contrast, genuine stationarity,
joint curved solutions, soundness and recovery remain on the critical path.

The [Lean capsule](certificates/a4d_native_history_action.lean),
[compiler output](certificates/a4d_native_history_action_output.txt),
[source receipt](certificates/a4d_native_history_action_results.json),
[exact checker](certificates/a4d_native_history_action_check.py) and
[immutable control ledger](certificates/a4d_native_history_action_certificate.json)
separate compiled statements, analytic universal proofs and finite controls.
No supported source, claim, BOOK entry or task lifecycle is changed.
