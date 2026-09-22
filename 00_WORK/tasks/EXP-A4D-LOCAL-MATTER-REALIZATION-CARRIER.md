# EXP-A4D-LOCAL-MATTER-REALIZATION-CARRIER

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Attempt the first provenance-bearing nonzero anomaly-free local matter realization on the actual 4D gravity carrier.

The target is not another abstract stress matrix.

It is an actual finite matter state/data object whose local metric response produces
[
T_N\in LocalSymRoleField(N)
]
and can eventually couple to the gravity response on the same carrier.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/ATORUS_MATTER_STRESS_EINSTEIN_COUPLING.md`
- `02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`
- `02_REGISTRY/research/ASOURCE_ACTION_NATURALITY_SELECTOR.md`
- matter representation/generation owners;
- matter localization and localization no-go owners;
- local trace / partial trace owners;
- archive stress and field-equation owners;
- any actual matter Hamiltonian/action/operator already defined over refinement-indexed carriers;
- role-phase group and local SymRole field owners.

## Non-negotiable starting facts

Do not reuse the minimal anomaly stress as a positive source:
it is zero for anomaly-free matter.

Do not count an arbitrary supplied neutral profile as derived matter localization.

Do not silently identify archive matrix indices with tangent Role indices.

Do not erase the A-STRESS three-coefficient / A-SOURCE selector no-go if using the scene route.

## Search order

### Route A — direct 4D role-phase matter

Look for an owned matter state that can naturally be indexed over
[
X_N=(\mathbb Z/(N+2))^4
]
or lifted there functorially.

Candidates may include:

- matter amplitudes;
- internal finite Hilbert/module states;
- generation/species carriers;
- local trace densities;
- finite Dirac/CAR states;
- gauge field matter amplitudes;
- phase/archive states.

Determine whether there is an owned evolution/action that makes this localization physical rather than arbitrary.

### Route B — archive matter operator

Test whether an owned operator
[
\Gamma_N
]
on internal×archive or internal×(X_N) can yield a local stress through actual metric variation.

A positive result needs the metric dependence to be part of the action, not inserted after the fact.

### Route C — scene quadratic source

If the scene route is still the best option, identify:

1. the missing actual matter→SceneC0 amplitude;
2. whether any new owned matter object now supplies it;
3. the surviving three block coefficients;
4. the transport needed from frozen scene tensor sector to (X_N\to Sym^2(Role)).

Do not declare the route closed if those maps remain absent.

## Stress target

A real positive endpoint requires:

1. an actual anomaly-free finite matter state;
2. an actual local realization (psi_N);
3. a concrete nonzero
   [
   T_N[m_N,\psi_N]\in LocalSymRoleField(N);
   ]
4. symmetry by type;
5. a declared local finite conservation/Ward identity;
6. an action or equally strong physical-response provenance;
7. no free arbitrary profile hidden in the definition.

## Variational route

Prefer an actual matter action
[
S_{m,N}[m_N,\psi_N]
]
with a theorem of the form
[
\delta_mS_{m,N}[h]
=
\frac12\langle T_N,h\rangle.
]

Audit the normalization convention but do not try to determine Newton's constant in this task.

## Conservation

If the matter action has a finite gauge/reparametrization symmetry, derive the corresponding Ward identity.

Do not substitute:

- charge neutrality;
- archive row sums;
- scene incidence divergence;

for centered Role tensor divergence unless an explicit intertwining theorem is proved.

## Strong positive controls

A successful candidate must include at least one explicit anomaly-free matter state with
[
T_N\ne0.
]

If possible, provide a localized excitation rather than only a constant vacuum-like source.

## Vacuum branch

Audit separately whether any natural constant/state-independent matter action yields a metric-proportional zeroth-order source.

Keep this separate from ordinary matter stress.

## Terminal verdict

Return exactly one:

- `LOCAL-MATTER-REALIZATION-CARRIER-REACHED`
- `DIRECT-4D-MATTER-CARRIER-MISSING`
- `MATTER-METRIC-VARIATION-ACTION-MISSING`
- `SCENE-MATTER-CARRIER-REMAINS-MISSING`
- `LOCAL-MATTER-STRESS-SELECTOR-UNDERDETERMINED`
- `MATTER-WARD-CONSERVATION-BRIDGE-MISSING`

## Deliverable

`MEMO_34_A4D_LOCAL_MATTER_REALIZATION_CARRIER.md`
