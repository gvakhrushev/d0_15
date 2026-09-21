# EXP-ACAP-A1-RIESZ-LEAKAGE-CAPACITY-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Test a new internal selector route for the exact four-modulus finite gravity family
[
(\mu,\gamma,u,v)
]
classified by A-WEIGHT-DYN.

The proposed mechanism is **shared-interface enforcement cost / archive-capacity saturation**:

> if a nonuniform A1 metric and the owned Euclidean Hodge/common-carrier metric require independent correction information to coexist on one finite self-reading interface, and if that correction information consumes an already-owned non-reusable archive capacity, then capacity saturation may force the correction to vanish and hence force the uniform A1 weight ray.

This is a research hypothesis, not a premise.

The task must determine whether D0 actually owns enough typed structure to make that argument a theorem.

A terminal NO-GO or bridge classification is fully acceptable and is preferable to importing a new cost functional under D0 terminology.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Research baseline:
the current `main` commit containing this brief.

Treat the task as fully stateless.

Repository edits: **none**.

## Methodological inspiration — not an assumption

The route was motivated by two external methodological patterns discussed during CONTROL review:

1. **shared-interface capacity / pairwise enforcement cost**: multiple independently constrained sectors sharing one finite interface may incur superlinear or pairwise correction costs, so an additional sector can fail by capacity overflow rather than by arbitrary exclusion;
2. **typed bridge discipline**: a physical bridge is accepted only when the internal and external signatures are separately typed and an explicit match theorem exists.

Do **not** cite either methodology as proof of any D0 statement.

All positive conclusions must be derived from literal D0 owners below.

---

# Frozen accepted research

Read first:

- `02_REGISTRY/RESEARCH_LEDGER.md`
- `02_REGISTRY/research/AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`
- `02_REGISTRY/research/AWEIGHT_GENERAL_WEIGHT_REDUCED_HESSIAN.md`
- `02_REGISTRY/research/ANORM_FINITE_GRAVITY_NORMALIZATION.md`
- `02_REGISTRY/CLOSURE_CONTRACT.md`
- `00_WORK/tasks/CTRL-GRAVITY-DYNAMICS-CLOSURE.md`

If available, read the source research memo:

- `MEMO_17_AWEIGHT_GENERAL_WEIGHT_REDUCED_HESSIAN.md`

Frozen results:

1. A-WEIGHT is `WEIGHT-SELECTOR-NOGO-TERMINAL` under the previously audited selector class.
2. A-WEIGHT-DYN is accepted as research with verdict `FOUR-FINITE-MODULI-PROVED`.
3. For positive block-scalar
   [
   W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13},
   ]
   the exact compensator-reduced A1 Hessian is known.
4. The uniform locus is exactly
   [
   x=y=z
   \iff
   u=v=1.
   ]
5. The general finite family is
   [
   Q_{\rm gen}=\kappa_H[Q_H+\mu D(u,v)],
   ]
   with observable moduli
   [
   (\mu,\gamma,u,v).
   ]
6. Do not reopen the old H-symmetry/C1/Perron/`rho1=1`/`S_min=1` selector routes.
7. Do not assume capacity saturation forces uniformity. That is the question to be tested.

---

# Required literal D0 owners

Read literally.

## A1 / common carrier

- `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`
- current A1 compensator/Noether owner if merged by the time this task runs;
- otherwise:
  - `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`
  - `04_CERTIFICATES/vp_a2_compensator_noether.py`

## Zone/archive decomposition

- `03_FORMALIZATION/D0/Synthesis/ZoneIsGeneration.lean`
- `03_FORMALIZATION/D0/Spectral/DarkArchiveStructure.lean`
- `03_FORMALIZATION/D0/SelfReading/TypedCapacityRawScene.lean`

## Capacity / verification / memory

- `03_FORMALIZATION/D0/Representation/PreparationMemoryBound.lean`
- `03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean`
- `03_FORMALIZATION/D0/Dynamics/TraceHeatCapacityGravity.lean`
- `03_FORMALIZATION/D0/Gravity/LocalPressureCapacityDynamics.lean`
- `03_FORMALIZATION/D0/Synthesis/SceneTraceHeatCapacity.lean` if relevant
- any literal owner of archive-capacity or memory-capacity claims discovered from `ClaimMap.lean`

## Pairing/source typing

- `02_REGISTRY/research/ASOURCE_ACTION_NATURALITY_SELECTOR.md`
- literal A1/Hodge pairing owners used by A-WEIGHT/A-WEIGHT-DYN
- any current source-dual/Riesz owner actually present in Lean

## Registry rows

Audit at least:

- `D0-HODGE-LINKS-001`
- `D0-A2-COMPENSATOR-NOETHER-RESEARCH-001`
- `D0-ZONE-IS-GENERATION-001`
- `D0-VERIFIABILITY-FORCES-FUNCTIONAL-TUPLE-001`
- `D0-TRACE-HEAT-CAPACITY-GRAVITY-001`
- `D0-LOCAL-PRESSURE-CAPACITY-DYNAMICS-001`
- `D0-PACKING-LIMIT-HOMOGENEITY-NOGO-001`

from `02_REGISTRY/claims.csv` / ClaimMap.

---

# Research programme

## 1. First decide what the canonical mismatch map actually is

A tempting candidate is the failure of the A1 Riesz map to preserve the Euclidean Ward/common carrier:
[
L_W
:=
B_+W^{-1}\big|_{K_+}.
]

However this map must **not** be declared physical merely because its rank is useful.

Audit the literal A1/source/Hodge typing and answer:

- Is (W^{-1}) the actually owned coordinate-to-Riesz or source-dual transport at the interface in question?
- Is (K_+=\ker B_+) the correct domain before and after that transport?
- Is (B_+W^{-1}h) a typed violation/correction datum that some owned protocol must retain?
- Would (BW), (A_W), (P_W), or another map be the correct object instead?

If (L_W) is not canonically justified, identify the correct map or terminate the physical-selector route while still classifying the algebraic candidate.

No selector theorem may depend on an arbitrarily chosen mismatch functional.

## 2. Exact algebraic leakage theorem

For the candidate/correct mismatch map, compute its exact action on
[
K_+
=
Z_{9,11}\oplus Z_{9,13}\oplus Z_{11,13}
\oplus A_9\oplus A_{11}\oplus A_{13}.
]

For
[
L_W=B_+W^{-1}|_{K_+},
]
the CONTROL conjecture to verify, not assume, is:

- all three tensor sectors lie in the kernel;
- on (A_9), the image is nonzero iff (x\ne y);
- on (A_{11}), the image is nonzero iff (x\ne z);
- on (A_{13}), the image is nonzero iff (y\ne z).

Candidate exact rank formula:
[
\boxed{
\operatorname{rank}L_W
=
8\,\mathbf1_{x\ne y}
+
10\,\mathbf1_{x\ne z}
+
12\,\mathbf1_{y\ne z}.
}
]

Therefore candidate strata:
[
\begin{array}{c|c}
x=y=z & 0\\
x=y\ne z & 22\\
x=z\ne y & 20\\
y=z\ne x & 18\\
x,y,z\text{ all distinct} & 30.
\end{array}
]

Derive exact coefficients, not just ranks.

Use exact symbolic algebra and a literal finite-matrix check.

## 3. Identify the leakage images

The numbers
[
8,10,12
]
match the three balanced vertex standard representations in the accepted zone/archive decomposition
[
9=1+8,qquad11=1+10,qquad13=1+12.
]

Determine whether this is a literal carrier identity or only an isomorphic dimension match.

Required questions:

- Is (operatorname{im}L_W|_{A_9}) literally the zone-9 balanced/dark block?
- Similarly for zones 11 and 13?
- Are the three images orthogonal/direct under an owned pairing?
- Does generic nonuniformity really fill the complete 30-dimensional dark/archive vertex carrier?

Give an explicit intertwiner/equality if one exists.

Do not promote a dimension coincidence to archive ownership.

## 4. Separate linear dimension from information capacity

This is load-bearing.

D0 owns finite-capacity theorems of at least two kinds:

- linear/rank/dimension capacities in scene/archive decompositions;
- finite-cardinality memory lower bounds, e.g. injective provenance/archive results from verifiability.

Do **not** silently identify them.

Determine whether an exact typed theorem converts an (r)-dimensional leakage/correction space into:

- (r) independent verification lines;
- at least (r) archive states;
- at least (2^r) correction configurations;
- or any other explicit finite memory requirement.

If such a theorem does not exist, state the type mismatch precisely.

## 5. Build the strongest possible verification protocol

If the correction modes are genuine independently checkable data, construct the smallest finite protocol that represents them.

Use the existing `VerifiabilityNecessity` and `PreparationMemoryBound` theorems where legitimate.

Required:

- define signal/correction states;
- define record/provenance carrier;
- prove injectivity requirement;
- derive a lower bound on archive capacity;
- state exactly what notion of capacity is bounded.

Try both conservative and strong encodings:

1. basis-label distinguishability only;
2. binary occupancy of independent correction modes if the dynamics really admits independent on/off combinations.

Do not assume all linear combinations are operationally distinguishable.

## 6. Is the relevant archive already saturated?

Audit every plausible saturation owner.

In particular, `TraceHeatCapacityGravity.lean` currently defines
[
RequiresBoundaryEncoding := SaturatedRegion.
]

Therefore the theorem
[
saturated\_region\_forces\_boundary\_encoding
]
may be only definitional and may provide no residual-capacity budget.

Determine whether any stronger owned theorem says:

> the archive/memory carrier is fully occupied by already-required information, so an additional independent correction record cannot be stored or reused.

Candidates include:

- generation/zone visible+dark decomposition;
- verification provenance archive;
- preparation/reset memory;
- rank-3 + nullity-30 archive structure;
- boundary heat/capacity;
- M1/MDL deletion minimality.

Keep distinct capacity notions distinct unless a literal theorem connects them.

## 7. Reuse versus additive enforcement cost

Even if correction information is nonzero, it may reuse an already-present archive carrier.

This is the decisive adversarial control.

Ask:

- Can the leakage correction be encoded in the same 8/10/12 dark modes without increasing total capacity?
- Does independent verification require a *new copy* of those modes, or only access to the existing copy?
- Is there a no-cloning/direct-sum/product requirement?
- Does composition force additive or pairwise cost?
- Is the proposed cost
  [
  E(N)=N\varepsilon+\binom N2\eta
  ]
  derivable from D0, or would (eta>0) be a new modelling constant?

If reuse is possible under all owned constraints, construct an explicit negative-control model.

## 8. Capacity-selector theorem target

A positive result must have an explicit chain of the form

[
\text{nonuniform }W
\Rightarrow
\text{typed nonzero correction datum}
\Rightarrow
\text{independent extra memory requirement}
\Rightarrow
\text{owned archive capacity already saturated}
\Rightarrow
\bot.
]

Only then may one conclude
[
x=y=z
\iff
u=v=1.
]

Every arrow must name a literal theorem/owner or a new theorem proved in the memo.

If even one arrow requires a new physical principle, classify the result as conditional bridge rather than CORE.

## 9. PLEC / least-enforcement-cost audit

As a secondary route, test whether D0 already owns a cost principle strong enough to select zero leakage.

Possible candidate observables:

- correction rank;
- minimal provenance-memory cardinality;
- exact code/MDL cost;
- action cost already owned by D0.

Do **not** define
[
C(W)=\sum_{a<b}(\lambda_a-\lambda_b)^2
]
or any similar mismatch penalty and then call its minimum a theorem unless that functional is itself derived from an owned protocol.

If the only way to select uniformity is to posit a new least-enforcement-cost functional, classify that as a new modelling/action principle.

## 10. Relation to A-SEL intrinsic locality

A-WEIGHT-DYN proved:
[
A_W\in\operatorname{span}\{I,Q_H,\varepsilon_{A_{11}}\}
\iff
u=v=1.
]

Determine whether the capacity/leakage theorem is genuinely independent of simply imposing A-SEL intrinsic degree-1 locality on the full reduced dynamics.

Do not repackage the locality assumption as capacity.

If capacity implies locality/uniformity by a distinct theorem, state the implication.

## 11. Secondary generation-count test

Only after the A1 capacity question is settled, test whether the same typed enforcement mechanism says anything nontrivial about generation multiplicity.

D0 already owns multiple exact appearances of the number three, including the zone/generation identification. Do not count another copy of “3” as progress.

The useful question is stronger:

> Is three the maximal admissible number of independently enforced shared-interface generation channels under an independently owned capacity ceiling, with a fourth channel excluded by a theorem rather than by the frozen scene definition?

Required safeguards:

- ceiling must be derived independently of already assuming three zones;
- pairwise interaction cost must be derived, not inserted;
- distinguish current exact three-generation ownership from a new maximality theorem.

If this cannot be done without circularity, return a no-go and stop.

## 12. Ω-style truncation / healing ideas: explicit deferral test

Do not spend the main research budget on these unless they unexpectedly close the capacity chain.

Record only whether:

- D0's (kappa)-equivalence quotients sub-resolution residuals rather than physicalizing them;
- any finite-stage residual survives as a typed observable;
- the current forgetting channel admits only a trivial one-step Lyapunov decay.

These are secondary frontier notes, not primary deliverables.

## 13. Strong negative controls

If capacity does not force uniformity, provide explicit nonuniform models, preferably
[
\rho=(1,2,3)
]
and
[
\rho=(2,3,5),
]
that:

- have the exact nonzero leakage pattern;
- satisfy all accepted A1/C1/Hodge algebraic identities;
- fit within every actually owned archive/memory capacity condition by reuse or alternative encoding;
- differ observably from the uniform branch.

This is required for a terminal selector no-go.

## 14. Strong positive control

If capacity does force uniformity, explicitly show:

- the correction carrier;
- its required independent memory size;
- the already-occupied capacity budget;
- the strict overflow for every nonuniform stratum;
- zero overflow exactly at (u=v=1).

No qualitative “saturation” prose is sufficient.

## 15. Impact on the four-modulus family

Return the exact consequence for
[
(\mu,\gamma,u,v).
]

Possible outcomes:

- (u=v=1) is forced, reducing to ((m^2,\gamma));
- capacity fixes only one relation among (u,v);
- capacity leaves both weight-shape moduli;
- the capacity route itself is untyped/bridge-only.

Do not attempt to fix (mu) or (gamma) unless the same proved capacity theorem genuinely constrains them.

## 16. Parent-action handoff

If capacity kills (u,v), state whether the next expensive task should attack only
[
(m^2,\gamma)
]
with a common generating action.

If capacity fails, state whether the parent-action selector remains the smallest positive closure route for all four
[
(\mu,\gamma,u,v).
]

## 17. Terminal verdict

Return exactly one primary verdict:

- `CORE-CAPACITY-FORCES-UNIFORM-WEIGHT`
- `LEAKAGE-THEOREM-PROVED-CAPACITY-BRIDGE-OPEN`
- `CAPACITY-SELECTOR-CONDITIONAL-BRIDGE`
- `CAPACITY-WEIGHT-SELECTOR-NOGO-TERMINAL`
- `CAPACITY-MEASURE-TYPE-MISMATCH-NOGO`

## Required final block

```text
canonical mismatch/Riesz map:
is that map physically owned:
exact sector action:
exact leakage rank formula:
uniform iff zero-leakage theorem:
leakage image by zone:
relation to 8+10+12 archive blocks:
literal carrier identity or only isomorphism:
owned capacity notions audited:
rank-to-memory typing theorem:
minimal verification protocol:
derived memory lower bound:
is the relevant archive demonstrably saturated:
is correction capacity additional or reusable:
pairwise/additive enforcement cost derived or assumed:
strongest capacity selector theorem:
strongest nonuniform negative control:
effect on (mu,gamma,u,v):
generation maximality consequence:
truncation/healing frontier note:
smallest remaining positive theorem:
impact on D0-HODGE-LINKS-001:
terminal verdict:
```

## Deliverable

`MEMO_18_ACAP_A1_RIESZ_LEAKAGE_CAPACITY_SELECTOR.md`

Separate rigorously:

- repository-owned theorem;
- accepted research;
- new exact theorem;
- exact finite computation;
- representation isomorphism;
- information-capacity theorem;
- modelling bridge;
- methodological analogy;
- external calibration.
