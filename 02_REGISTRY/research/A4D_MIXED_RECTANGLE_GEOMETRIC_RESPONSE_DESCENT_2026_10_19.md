# A4D geometry-first synthesis: mixed-rectangle response descent

**Date:** 2026-10-19  
**Status:** RESEARCH / CONDITIONAL; no GR promotion, no claim registry edit  
**Repository:** `gvakhrushev/d0_15`  
**Reference:** main `5d23e90af703efee7f0deb24517d3ead4780fdfc`; live #334 and #381 advanced afterward.  
**Owners consumed, not replaced:** merged #377 geometric probe law, #334 original finite full action / quartic Cartan, #381 full-history code KL and physical-source boundary, A4D Schur–Einstein direct linear identification, #232 exact Y stationary family.

## 1. Core distinction

For a geometric projection `pi_h: X_h -> G_h`, equality of coarse metrics does not imply equality of **native** physical metric responses. A geometry-only Einstein action may descend while the native complete record/preparation/clock Cost–Info still sees internal degrees of freedom. Nor does vertical stationarity alone imply common horizontal response when the stationary fiber has disconnected components.

The correct target is the **mixed geometry/fiber action rectangle**, computed on one and the same admitted original finite action, with all its full native contributions retained.

For two admissible connection/matter/preparation/clock state sections `z_0(g), z_1(g)` and the same endpoint metric pencil `g_± = g ± eps v`, define

```
R_h,eps(g;v,z0,z1) =
 [A_h(g+,z1+) - A_h(g-,z1-)]
-[A_h(g+,z0+) - A_h(g-,z0-)].
C_h,eps = R_h,eps / (2 eps).
```

All four values must be the **same native complete action** under legal endpoint preparations. This is a rectangle contrast (two geometric endpoints x two internal sections), not a newly proposed physical action or counterterm.

It measures the difference of the two finite native metric contrasts **exactly**, by algebra:

```
C_h,eps = D_h,eps^native[z1] - D_h,eps^native[z0].
```

Thus a uniform `C_h,h^(1/3) -> 0` is the literal response-descent / microstructure-erasure obligation. If one physically admitted section is already matched to the accepted #377 geometric probe, every other admitted section with vanishing rectangle shares its metric response. No full connection convergence or uniqueness is needed.

## 2. Smooth local identity, and its caveat

On a differentiable two-parameter local chart `A(g(t),z(s))` with fixed admissible chart and **fixed** internal interpolation sections, the fundamental theorem of calculus yields

```
A(g+,z1)-A(g-,z1)-A(g+,z0)+A(g-,z0)
  = ∫_{-eps}^{eps}∫_0^1 ∂_s ∂_t A(g(t),z(s)) ds dt.
```

With varying endpoint sections `z_i(g)`, this formula must include their motion, or be expressed as the difference of the two **total** stationary response derivatives. Do not silently replace total derivatives by partial derivatives without native joint stationarity, boundary terms and a valid envelope identity.

A sufficient *chartwise* criterion is a uniform mixed-derivative bound whose integral tends to zero at the relevant finite-action normalization. But the rectangle definition and test remain meaningful even with disconnected stationary fibers or no interpolating smooth joint-critical path.

Vertical first variation `D_z A=0` at two isolated stationary points is **not** enough for rectangle zero: it gives a zero derivative only at those points, not along the curve between them. A finite example is `A(t,z)=(z^2-1)^2+t z`: at `t=0`, both `z=±1` are stationary, yet their metric derivatives are `±1`. This is a toy mathematical control, not a D0 counterexample.

## 3. Apply the owner boundaries

- The merged #377 probe yields `P_geom = delta S_EH + O(h/eps + eps^2)` under its smooth geometry and endpoint-domain assumptions, with `eps=h^(1/3)` giving `O(h^(2/3))`.
- #334 has a fully checked nontrivial finite Cartan quartic amplitude jet on a representative unwrapped crossing, not a periodic exact stationary recovery nor a full native price selection.
- The exact #232 Y connection family is a null **geometric** response control only on its registered carrier. Its existence does not establish native full-history Cost–Info rectangle cancellation.
- #381 distinguishes binary return, fine conditional record and quantum coherence terms. Exact relative-entropy chain decomposition is **not** proof that conditional and coherent field derivatives vanish. The whole native source must be carried, including immutable RIGHT, AF preparation, controller, clock, and work. No isolated binary-odds or invented task-conditioned pressure is the complete original action.

## 4. Operational attack

1. Choose one already admitted geometric endpoint pencil and a pair of sections sharing its geometric projection. Reuse #377's endpoint restrictions; do not promote its external smooth preparation to native admission.
2. Evaluate all four **original complete** physical action values and the native 40 + matter + prep + clock rows where defined, without summand omission or double pricing.
3. Compute `C_h,eps` and separately compute contributions of binary odds, fine conditional KL, coherence loss, AF preparation and clock/work. Their sum must be the real original action, not a synthetic recombination.
4. Check the representative Y center, then the crossed-null quartic Cartan jet, **only where each has an admitted finite physical realization**. Label absent endpoints as absent, not as zero rectangle.
5. Run a hostile witness: equal binary odds but different fine conditional/coherent record; #381 establishes that information-source differences can be nonzero on such fibers. The test discriminates geometry-invisible from native-action-invisible.
6. Prove (or refute with a true admitted joint-critical sequence) `sup |C_h,h^(1/3)| -> 0` in a precisely declared physical class.
7. Independently prove one admitted native section transfers to the accepted #377 probe and source, with any metric normalization / cosmological term identified from the same action.

## 5. Conditional closure statement

Assume: (i) nonempty complete admitted stationary endpoint sections in the stated physical class; (ii) the native whole-action rectangle contrast is `o(1)` uniformly in sections and unit smooth metric probes; (iii) a section has native-to-#377 geometric contrast error `o(1)`; (iv) matter/source action and Ward are identified natively, including normalization; (v) joint stationary-to-contrast refinement transfer and realization-independence are proved. Then all sections have the same limiting physical metric first variation, and under the #377 hypotheses this geometric component is the Einstein–Hilbert variation. Source equations follow only with (iv)-(v), not by definition of T as G.

**Status:** Conditional proposition and new computable diagnostic. No numerical rectangle value has been calculated here; no native admissible section has been constructed by this memo. `GR_closed=false`.

## 6. Why this route differs from old all-sheet rescue

It does not force exact nongauge Y roots into a LC connection sheet. It asks whether distinct admissible joint stationary centers give the **same physical action response** under **the same metric perturbation**. It can succeed with connection nonuniqueness, and it exposes fine/coherent Cost–Info response precisely where earlier binary compression would hide it.

**Proposed next owner:** `EXP-A4D-NATIVE-MIXED-RECTANGLE-RESPONSE-DESCENT`, dependent on the native admitted same-history full action and physical endpoint admission. Do not duplicate #334/#381 result ownership.
