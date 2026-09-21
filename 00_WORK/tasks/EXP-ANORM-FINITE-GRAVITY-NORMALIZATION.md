# EXP-ANORM-FINITE-GRAVITY-NORMALIZATION

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Terminally classify the **relative-normalization** freedom in the finite gravity lane.

Previous research has separately found:

- a canonical literal Hodge kinetic candidate `Q_H`;
- an A1 compensator/contact Hessian that is scalar on the physical carrier;
- a two-tick symplectic temporal skeleton;
- an unfixed temporal coupling `alpha`;
- an apparent Hodge-plus-shift spatial family `Q = c (Q_H + m^2 I)`.

The current open question is not “find another operator”.

It is:

> After quotienting all genuine scale redundancies, canonical transformations, sign/time-orientation equivalences and unit conventions, how many physically distinct finite normalization moduli remain, and does any currently owned D0 principle fix them?

A terminal negative result is fully acceptable.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Research baseline:
`4febeb6e9e0f39cdf8f4768f0d33dc33cf801b8a`

Treat this task as fully stateless. Do not assume conversational memory.

## Required CONTROL context

Read first:

- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/RESEARCH_LEDGER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ASOURCE_ACTION_NATURALITY_SELECTOR.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/CLOSURE_CONTRACT.md

Do not reopen A-STRESS/A-SOURCE. Their boundaries are frozen:

- matter→SceneC0 carrier: `SOURCE-CARRIER-MISSING`;
- quadratic block selector inside the current owned class: `SELECTOR-NOGO-TERMINAL`.

## Required literal repository files

Read literally before doing new algebra:

1. Two-tick finite dynamics:
   - `03_FORMALIZATION/D0/Dynamics/TwoTickSymplectic.lean`

2. Scene Hodge and spectral action:
   - `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
   - `03_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean`
   - `03_FORMALIZATION/D0/Synthesis/HodgeThreeLevelSpectrum.lean`

3. A1 finite action research:
   - `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`

4. Endogenous action scale:
   - `03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean`

5. Physical-hbar boundary:
   - `04_CERTIFICATES/vp_hbar_symplectic_capacity_status.py`

6. Current gravity source/carrier owner:
   - `03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean`

7. Current active C1 brief, for semantic boundaries only:
   - `00_WORK/tasks/WRK-C1-COMMON-CARRIER.md`

8. Registry rows:
   - `D0-HODGE-LINKS-001`
   - `D0-SPECTRAL-EINSTEIN-001`
   - `D0-TWO-TICK-SYMPLECTIC-GENERATOR-001`
   - `D0-SCENE-SPECTRAL-ACTION-001`
   - `D0-ENDOGENOUS-ACTION-QUANTUM-001`
   - `D0-HBAR-SYMPLECTIC-CAPACITY-MECH-LIMIT-001`

from:
https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/claims.csv

## Required attached research inputs

If available, attach:

- `MEMO_10_ASEL_EXHAUSTIVE_DYNAMICS_CLASSIFICATION.md`
- `MEMO_08_ACPL_WEIGHTED_SOURCE_ACTION_COUPLING.md`
- the prior A-Omega / alpha-normalisation memo if available;
- `MEMO_14_ASOURCE_ACTION_NATURALITY_SELECTOR.md` only as current roadmap context.

These are research evidence, not proof owners.

---

# Frozen starting facts to audit, not blindly repeat

The following are accepted research-level starting points and must be checked against the literal repository conventions.

## A. Hodge kinetic candidate

On the literal physical carrier, accepted research gives six H-irreducible sectors with Hodge eigenvalues

[
13,;11,;9,;24,;22,;20.
]

The literal Hodge operator preserves the common unsigned carrier and commutes with the C1 isometry at research level.

## B. A1 contact sector

Accepted A-X/A1 research gives, after compensator elimination and for unit edge weight, a physical Hessian proportional to

[
4 I
]

on the unsigned physical carrier.

This is contact/constraint stiffness, not a spatial propagation operator.

Do not assume that the coefficient 4 is automatically in the same physical normalization as the Hodge kinetic term.

## C. Spatial selector reduction

Accepted A-SEL research suggests that imposing Hodge form after kinetic locality reduces the spatial family to

[
Q = c,(Q_H + m^2 I),
]

up to the exact convention used for `m^2`.

The tempting specialization

[
Q=Q_H+4I
]

is **conditional** on a relative action-normalisation statement that is not currently owned.

Audit this carefully.

## D. Two-tick temporal law

`TwoTickSymplectic.lean` owns the algebraic two-tick skeleton and recurrence.

Previous research coupled spatial eigenvalues (lambda) through a dimensionless coefficient (alpha), producing sector transfer matrices whose characteristic polynomial depends on the combination (alphalambda) (with branch-dependent sign).

The exact branch formulas must be re-derived from the actual chosen coupled dynamics convention rather than copied blindly.

## E. Action and physical units

`EndogenousActionQuantum.lean` owns an endogenous minimum action statement and relative-scale facts.

It does **not** follow automatically that every independent quadratic action term has unit relative coefficient.

The physical dimensionful (hbar) identification remains a bridge/mechanism-limit.

Do not use SI (hbar,c,G) to fix a CORE dimensionless coefficient.

---

# Research programme

## 1. Write the fully parameterised finite quadratic dynamics

Construct the most general finite quadratic model compatible with the already accepted Hodge/contact split, before quotienting redundancies.

At minimum distinguish:

- Hodge kinetic coefficient (kappa_H);
- A1/contact coefficient (kappa_A);
- optional overall action coefficient (kappa_0);
- temporal/spatial coupling coefficient (alpha);
- any branch/sign variable that is only orientation/conjugacy.

Write the sector operator explicitly.

Do not prematurely set any coefficient to 1 or 4.

## 2. Quotient by genuine redundancies

Classify exactly which transformations do **not** change the finite observable dynamics:

- overall multiplication of the action;
- field rescaling;
- simultaneous (Q	o sQ,;alpha	oalpha/s);
- canonical/symplectic conjugacy;
- sign conjugacy;
- time reversal / branch orientation;
- basis change inside H-irreducible sectors.

Give the quotient parameter space.

The core deliverable is not a raw coefficient count but the number of inequivalent moduli after these redundancies.

## 3. Define invariant dimensionless parameters

Find a minimal set of invariant combinations.

Candidates include something like

[
m^2=kappa_A/kappa_H,
qquad
gamma=alphakappa_H,
]

but do not assume this parameterisation if another is cleaner.

Prove that two parameter sets with the same invariants are dynamically equivalent under the allowed redundancy group, and that differing invariants are distinguishable by a finite observable such as sector traces or characteristic polynomials.

## 4. Exact stability region with the mass/contact shift

For

[
Q=kappa_H Q_H+kappa_A I,
]

derive the exact elliptic/stability inequalities for every Hodge sector under each admissible two-tick coupling branch.

Do this as a function of the quotient parameters, not only at (m^2=0).

Determine:

- whether the stability region is empty/nonempty;
- whether it reduces a modulus to an interval or a point;
- which sector controls each boundary;
- whether positivity of a conserved quadratic energy adds independent constraints.

Use exact rational inequalities where possible.

## 5. Does the A1 coefficient 4 fix (m^2=4)?

Audit the strongest possible argument for

[
m^2=4.
]

Required checks:

1. Are the Hodge and A1 terms derived from one single owned action?
2. Are their field variables literally the same typed variable?
3. Are their inner products the same owned pairing?
4. Is there a theorem fixing the relative coefficient rather than each term's internal convention?
5. Does C1 isometry provide only norm transport, or also an action-normalisation identification?

If any required arrow is missing, the statement (m^2=4) remains conditional.

Construct two inequivalent models satisfying all owned statements if possible.

## 6. SceneSpectralAction as a potential normaliser

Test whether the unit (ho_1), EH proxy, trace identities, or any coefficient in `SceneSpectralAction` can fix:

- (kappa_H);
- (kappa_A/kappa_H);
- (alpha).

Distinguish background operator normalization from physical action coefficient.

If no theorem links them, produce an explicit counterfamily with the same spectral-action identities.

## 7. EndogenousActionQuantum

Read the exact theorem statements, especially any relative-scale invariance.

Determine whether

[
S_{min}=1
]

is:

- a lower bound on nontrivial transitions;
- a convention fixing one global action unit;
- a theorem fixing relative coefficients of independent action terms.

Do not conflate these.

If relative coefficients remain free under the owned theorem, state that as a formal boundary.

## 8. Physical-hbar / symplectic-capacity boundary

Audit whether the finite symplectic-capacity mechanism can fix any of the dimensionless relative coefficients before SI calibration.

If the normalization to physical (hbar) is itself a bridge, it cannot be used to close a CORE relative-normalisation theorem unless the required ratio is already dimensionless and internally fixed.

State exactly what is and is not transferable.

## 9. Discrete tick / time normalization

D0 has owned or certified discrete tick structures elsewhere in the repository.

Determine whether the two-tick map already fixes the time unit strongly enough that (alpha) cannot be absorbed into a time rescaling.

Separate:

- relabelling one tick;
- changing the coupling strength per fixed tick;
- continuous Hamiltonian interpolation time.

If the tick is combinatorially fixed, show whether distinct (alpha) values remain finite-dynamically distinguishable.

## 10. Real Hamiltonian logarithm / generator

The two-tick map admits a real quadratic Hamiltonian interpolation.

Determine whether choosing the canonical real logarithm/generator fixes the spatial coupling coefficient or merely maps each already-chosen finite transfer matrix to a corresponding Hamiltonian.

Do not claim uniqueness of the physical generator from uniqueness inside a chosen branch if different (alpha,m^2) produce different transfer matrices.

## 11. C1/common-carrier normalization

Condition on the research C1 isometry.

Ask whether

[
U^*U=I
]

fixes any relative action coefficient, or only transports an already-chosen Euclidean normalization between carriers.

Likewise test whether the (omega) complement/decomposition introduces or removes a normalization modulus.

## 12. Source reciprocity

Use the accepted A-SOURCE result.

For a fixed quadratic source (sigma), ask whether requiring one reciprocal quadratic action for source and response imposes any equation on (m^2) or (gamma).

If reciprocity works for every admissible parameter pair, prove it and remove this route from the selector search.

## 13. Strong negative control

If no owned principle fixes the quotient moduli, construct at least **two fully explicit finite models** satisfying the same audited owned constraints but with different invariant normalization parameters.

They must differ in an observable invariant, for example:

- sector transfer trace;
- characteristic polynomial;
- oscillation angle;
- conserved-energy matrix.

Prefer both models inside the strict stability/positivity region.

This is required for a terminal NO-GO verdict.

## 14. Count what remains physical

Return an exact hierarchy such as:

```text
raw coefficients:
after overall action scale:
after Q/alpha reciprocal rescaling:
after branch/sign quotient:
after stability/positive-energy constraints:
after C1/source reciprocity:
final dimension of finite normalization moduli:
```

Do not call an interval “fixed”.

## 15. Relationship to continuum calibration

Determine which remaining finite modulus, if any, could later be fixed only by:

- continuum wave speed;
- Newton coupling;
- SI time calibration;
- physical (hbar);
- empirical matching.

Classify each as an external calibration/passport rather than an internal theorem when appropriate.

## 16. Terminal verdict

Return exactly one primary verdict:

- `CORE-NORMALIZATION-FOUND`
- `ONE-FINITE-MODULUS-LEFT`
- `TWO-FINITE-MODULI-LEFT`
- `RELATIVE-NORMALIZATION-NOGO-TERMINAL`
- `EXTERNAL-CALIBRATION-PASSPORT`

You may give a secondary boundary, but choose one primary verdict.

## 17. Required final block

```text
raw finite coefficients:
redundancy group:
minimal invariant parameters:
does overall action scale matter:
does Q/alpha rescaling remove one parameter:
exact shifted Hodge spectrum:
exact stable region:
positive-energy region:
does A1 coefficient 4 fix the shift:
does SceneSpectralAction fix any relative coefficient:
does S_min=1 fix any relative coefficient:
does finite hbar mechanism fix any relative coefficient:
is alpha removable by tick/time rescaling:
does Hamiltonian interpolation fix alpha:
does C1 isometry fix normalization:
does source reciprocity fix normalization:
strongest two inequivalent surviving models:
number of finite normalization moduli after all owned constraints:
which remaining moduli are external-calibration candidates:
smallest future theorem/certificate:
impact on D0-HODGE-LINKS-001:
terminal verdict:
```

## Deliverable

`MEMO_15_ANORM_FINITE_GRAVITY_NORMALIZATION.md`

No repository edits.

The memo must separate:

- repository-owned theorem;
- accepted prior research;
- new theorem;
- redundancy/convention;
- modelling choice;
- external calibration.

Do not use SI constants or continuum GR to close a CORE finite normalization unless the required bridge is already owned.
