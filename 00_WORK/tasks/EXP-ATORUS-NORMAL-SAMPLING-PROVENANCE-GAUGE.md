# EXP-ATORUS-NORMAL-SAMPLING-PROVENANCE-GAUGE

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Classify the epistemic status of the normal-coordinate sampling used in E-NJET.

The estimator theorem is already frozen:

[
E_{\eta,N}
\xrightarrow[\text{normal sampling}]{}
-2G[g](x).
]

The remaining question is whether the metric-dependent normal realization is merely a gauge/coordinate representation of an intrinsic finite-to-continuum response, or a genuinely new modelling choice that D0 does not derive.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`
- `02_REGISTRY/research/ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`
- `02_REGISTRY/research/ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`
- `02_REGISTRY/research/A4D_ANISOTROPIC_RAYS_NATURALITY_SELECTOR.md`
- `02_REGISTRY/research/A4D_LINEARIZED_NOETHER_UNIQUENESS.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- the current finite linearized response worker output if it has landed by the time you run.

## Main distinction

Separate three statements:

1. **coordinate choice**:
   once a smooth metric (g) exists, normal coordinates are ordinary gauge/representation data;

2. **sampling prescription**:
   deciding that the abstract finite Role lattice samples (g) through the exponential normal chart at each evaluation point;

3. **dynamical provenance**:
   deriving from D0 finite variables why those samples are the physical finite metric degrees of freedom.

The first is standard geometry.

The second may be a BRIDGE/PASSPORT convention.

The third is a much stronger emergence theorem.

Do not conflate them.

## Exact questions

1. Is the E-NJET estimator independent of all admissible normal-coordinate constructions with the same orthonormal frame?
2. Is it independent of the orthonormal frame after geometric reconstruction?
3. Can the sampling be characterized intrinsically as evaluation along metric geodesics from (x), without a preferred global torus grid?
4. Does this make the sampling canonical enough for a continuum BRIDGE, even if not CORE-derived?
5. Does current D0 finite geometry contain any object that can be proved equivalent to these sampled metric components?
6. Does the existing conductance/local-Laplacian variation carrier map naturally into the sitewise `SymRoleTensor` field used by E-NJET?
7. Is there any theorem deriving the metric-gauge law
   [
   \delta h_{ab}=D_a\xi_b+D_b\xi_a
   ]
   from finite relabelling/reparametrization rather than adding it as a modelling principle?
8. Does the local exponential realization depend on arbitrary choices beyond metric + orthonormal frame?
9. Can the normal-sampling bridge be classified as harmless coordinate gauge while the metric input remains an explicit external continuum bridge?
10. What exact theorem would be required before saying “D0 derives the Einstein tensor” rather than “D0 contains a stencil that estimates the Einstein tensor under an externally supplied metric realization”?

## Strong controls

- Same (g,x), two orthonormal frames related by a local Lorentz transformation.
- Same geometric 2-jet, two normal charts differing by higher-order coordinate terms.
- Same finite Role field, two inequivalent geometric reconstructions if one allows arbitrary non-normal frames.
- Flat metric, where all legitimate normal realizations must return zero response.

## Terminal verdict

Return exactly one:

- `NORMAL-SAMPLING-GAUGE-PASSPORT-SUFFICIENT`
- `NORMAL-SAMPLING-PROVENANCE-BRIDGE-OPEN`
- `NORMAL-SAMPLING-REQUIRES-NEW-METRIC-PRIMITIVE`
- `FINITE-METRIC-CARRIER-NOT-COMPATIBLE`
- `FINITE-METRIC-GAUGE-PRINCIPLE-MISSING`

## Required final section

State separately:

- what is pure coordinate gauge;
- what is BRIDGE/PASSPORT input;
- what is missing CORE provenance;
- whether E-NJET may honestly be called a D0→Einstein bridge;
- the smallest next theorem/worker if positive;
- the exact stopping boundary if negative.

## Deliverable

`MEMO_31_ATORUS_NORMAL_SAMPLING_PROVENANCE_GAUGE.md`
