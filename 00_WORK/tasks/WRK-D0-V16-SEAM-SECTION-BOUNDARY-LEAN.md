# WRK-D0-V16-SEAM-SECTION-BOUNDARY-LEAN

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-D0-V16-CHANNEL-DYNAMICS-INTEGRATION`  
Research lane: post-#247 seam/remnant section boundary formalization

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/d0-v16-seam-section-boundary-lean`  
Primary artifact: `03_FORMALIZATION/D0/Synthesis/SeamSectionBoundary.lean`  
Execution: `GitHub-first`

## Why delegated

Merged #247 closes the unadorned remnant mass/lifetime section with a structural
no-go and isolates a positive internal witness, `R_* = 5/32`, plus the exact
reason dimensional typing alone cannot choose the missing dimensionless mass
and Bondi-clock selectors.  The scientific result is already fixed; the
remaining work is bounded formalization and hostile-control ownership over
existing Lean capacity/metrology APIs.  That is implementation/formalization
work rather than new open-ended research.

## Inputs

Consume, without reopening their scientific status:

- merged #247:
  `02_REGISTRY/research/MEMO_D0_V16_SEAM_PURIFICATION_SECTION_MAP.md`;
- `D0.Synthesis.SceneTraceHeatCapacity`;
- `D0.Dynamics.TraceHeatCapacityGravity`;
- `D0.Synthesis.MassSectorMetricUnderdetermination`;
- `D0.Bridge.RedshiftSITickCalibrationNoGo`.

Do not encode the absence of a physical Bondi or black-hole selector as an
axiom or as a theorem-by-definition.

## Objective

Create a small Lean owner for the exact **formalizable** part of the #247
boundary, while preserving the distinction between machine mathematics and the
meta-level statement that the current corpus does not own two semantic
morphisms.

At minimum formalize:

1. the frozen co-vertex region has exactly 32 vertices;
2. its owned boundary cut is 20 and boundary capacity is exactly 5;
3. its capacity density is exactly
   [
   R_*^{cv}=5/32,
   ]
   with the positive multiplier `1+R_* = 37/32`;
4. a generic selector-nonuniqueness lemma: within a declared class constrained
   only by positivity/type and a fixed dimensional unit, multiplying a positive
   dimensionless selector by a positive nontrivial internal multiplier produces
   a distinct equally well-typed positive selector;
5. instantiate that hostile control with the frozen internal multiplier
   `37/32`, so the formalization witnesses why unit/dimension information
   alone cannot select a unique remnant mass coefficient or clock coefficient.

The module may define a minimal abstract selector API if useful, but it must
not manufacture `mu_BH` or `b_Bondi`, identify internal tick time with Bondi
retarded time, or identify boundary capacity with closure-density black-hole
mass.

## Required gates

1. Reuse `SceneTraceHeatCapacity.covertex_cut` and the actual
   `BoundaryCapacity` definition; do not duplicate the graph computation.
2. Prove the co-vertex cardinality and `5/32` ratio in Lean with exact
   rational arithmetic.
3. Keep the selector theorem abstract enough that its assumptions are visible:
   positivity/type information alone is insufficient.  Do not state the
   stronger meta-claim "no morphism exists" as a Lean theorem.
4. Include at least one hostile control showing the theorem fails to imply
   nonuniqueness once an explicit selector-fixing axiom/equation is supplied.
   This prevents turning a scoped no-go into a universal one.
5. Wire the new module canonically through `formal_support.csv` and generated
   Lean views, without minting a new scientific claim ID unless CONTROL
   explicitly requires one after validation.
6. Run a narrow build for the new module, then one final repository Lean
   integration build according to `00_WORK/README.md`.
7. No book/public prose edits unless a generated view requires them.

## Terminal

`D0-V16-SEAM-SECTION-BOUNDARY-LEAN-CERTIFIED`

requires all exact capacity-ratio theorems, the scoped selector
nonuniqueness theorem, the `37/32` hostile witness, canonical formal-support
wiring, and green Lean/repository guards.

If the existing APIs cannot express the theorem without adding a new semantic
primitive, remain Draft/BLOCKED and identify that exact API gap instead of
inventing the primitive.

## Scope fences

No remnant mass formula, no lifetime formula, no Bondi identification, no
external Bianchi relation as a selector, no PBH/LIGO/cosmology/lab data, no new
dimensional scale, no claim-status promotion, and no change to the scientific
terminal of #247.

## GitHub execution contract

Start from fresh current `main`; run
`python tools/task_lifecycle.py start WRK-D0-V16-SEAM-SECTION-BOUNDARY-LEAN`
as the first branch lifecycle change; open a Draft PR before substantive Lean
edits; use narrow Lean iteration; retire the task in the same PR before Ready;
set `Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return only the PR number/head, terminal or blocker, theorem names added,
whether `R_*=5/32` and `1+R_*=37/32` are Lean-owned, the exact scoped
selector-nonuniqueness statement, and validation commands.  Keep proofs and
derivations in GitHub.
