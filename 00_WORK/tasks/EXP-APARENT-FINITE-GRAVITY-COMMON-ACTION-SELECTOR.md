# EXP-APARENT-FINITE-GRAVITY-COMMON-ACTION-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Classify whether the currently owned finite gravity ingredients can arise from a **genuinely common finite parent action / generating law** that removes any of the four observable moduli
[
(\mu,\gamma,u,v),
]
without inserting the desired metric or coefficient relations as assumptions disguised as “one action”.

This is now the smallest high-value internal selector frontier after A-WEIGHT, A-WEIGHT-DYN and A-CAP.

A negative theorem is fully acceptable.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Research baseline:
the current `main` containing this brief.

Treat the task as fully stateless.

Repository edits: **none**.

## Frozen accepted results

Read first:

- `02_REGISTRY/RESEARCH_LEDGER.md`
- `02_REGISTRY/research/AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`
- `02_REGISTRY/research/AWEIGHT_GENERAL_WEIGHT_REDUCED_HESSIAN.md`
- `02_REGISTRY/research/ACAP_A1_RIESZ_LEAKAGE_CAPACITY_SELECTOR.md`
- `02_REGISTRY/research/ANORM_FINITE_GRAVITY_NORMALIZATION.md`
- `02_REGISTRY/CLOSURE_CONTRACT.md`
- `00_WORK/tasks/CTRL-GRAVITY-DYNAMICS-CLOSURE.md`

Frozen facts:

1. The finite nondegenerate family has exactly four observable moduli
   [
   (\mu,\gamma,u,v).
   ]
2. Uniform A1 weight is exactly
   [
   u=v=1.
   ]
3. On that locus (mu) may be renamed (m^2).
4. Current H-symmetry, C1 isometry, Ward identities, spectral `rho1=1`, action-quantum normalization and archive capacity do not select (u,v).
5. A-CAP is terminally `CAPACITY-WEIGHT-SELECTOR-NOGO-TERMINAL`.
6. The exact bare-metric self-duality condition
   [
   W^{-1}(K_+)\subseteq K_+
   ]
   would force (u=v=1), but that condition is not currently derived.
7. Do not reopen the previous selector searches.

## Required literal owners

Read literally:

- `03_FORMALIZATION/D0/Gravity/A2CompensatorNoether.lean`
- `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
- `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean`
- `03_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean`
- `03_FORMALIZATION/D0/Dynamics/TwoTickSymplectic.lean`
- `03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean`
- any literal finite variational/action owner discovered from ClaimMap or the books that is actually load-bearing.

Audit the registry rows:

- `D0-A2-COMPENSATOR-NOETHER-RESEARCH-001`
- `D0-C1-COMMON-CARRIER-RESEARCH-001`
- `D0-TWO-TICK-SYMPLECTIC-GENERATOR-001`
- `D0-ENDOGENOUS-ACTION-QUANTUM-001`
- `D0-HODGE-LINKS-001`.

---

# Critical anti-smuggling rule

The statement

> “all terms occur in one action”

does **not** imply:

- one edge metric;
- one Riesz map;
- one coefficient;
- one time scale;
- one normalization of the Hodge and A1 sectors.

For example a single written functional may contain
[
\kappa_H S_H
+
\kappa_A S_A(W)
+
S_{time}(\alpha)
]
with arbitrary positive (W,kappa_H,kappa_A,alpha).

Such a sum is a common action syntactically but is **not a selector theorem**.

A positive result must derive the relation it uses.

---

# Research programme

## 1. Type every current finite field and pairing

Make an explicit table of:

- configuration variables;
- edge/vertex carriers;
- Euclidean Hodge pairing;
- A1 weighted pairing (W);
- compensator variable;
- spatial Hodge operator;
- two-tick phase-space variables;
- temporal symplectic form;
- coefficients (kappa_H,kappa_A,alpha);
- action-quantum / verification state carrier.

State which objects are already in one type and which require a bridge.

## 2. Define levels of “common parent action”

Distinguish at least:

### Level 0 — syntactic common sum
Independent terms written in one scalar functional.

### Level 1 — common field carrier
The Hodge and A1 terms act on the same physical (K_+) edge field but may use different Riesz metrics.

### Level 2 — common edge metric
Both Hodge and A1 variations arise from one underlying edge pairing/Riesz structure.

### Level 3 — common spacetime/discrete-time generator
The spatial operator and the two-tick temporal law are Euler-Lagrange / generating-function consequences of one finite action.

### Level 4 — normalized parent action
The theory itself fixes all relative coefficients up to one irrelevant overall scale.

For each level, determine what is owned, what is constructible, and what is a new premise.

## 3. Classify the most general quadratic H-invariant parent action

On the frozen finite carriers, classify the most general quadratic parent functional compatible with the owned symmetries and semantic firewalls.

At minimum include:

- Hodge kinetic term;
- compensator-completed A1 contact term with general positive H-invariant (W);
- allowed cross terms;
- finite two-tick kinetic/generating term.

Do not assume cross terms vanish unless a symmetry/typing theorem kills them.

Determine the dimension of the admissible coefficient/metric family before quotients.

## 4. Test whether a common metric is forced

The Euclidean Hodge pairing is fixed by the literal Hodge owner.

Ask whether any **owned** variational/naturality principle forces the A1 Riesz metric to be proportional to that same pairing.

If yes, prove:
[
W=cI
\Rightarrow
u=v=1.
]

If no, construct two explicit common-parent functionals with nonproportional positive (W) satisfying every owned Level-0/Level-1 condition.

This is the decisive uniformity test.

## 5. Test the stronger self-duality route

A-CAP proves algebraically:
[
W^{-1}(K_+)\subseteq K_+
\iff
u=v=1.
]

Determine whether a genuine parent variational principle forces this self-duality/common-Riesz condition.

Do not assume it.

If the only positive proof begins by postulating one Riesz map, classify the result as conditional common-metric bridge.

## 6. Relative spatial coefficient (mu)

After any metric reduction, determine whether the parent action fixes the relative Hodge/A1 coefficient.

Audit:

- overall action rescaling;
- canonical field rescaling;
- `S_min=1`;
- current verification `ActionProtocol`;
- any owned action additivity/minimality theorem.

The key question is not whether one can *choose* normalization, but whether two different positive relative coefficients define inequivalent parent actions satisfying the same owned principles.

Construct explicit negative controls if they do.

## 7. Temporal coefficient (gamma)

Use the literal `TwoTickSymplectic` owner.

Determine whether the two-tick recurrence is merely compatible with a continuum/family of generating functions, or whether a finite discrete variational generator canonically fixes the spatial-to-temporal coefficient.

Required:

- derive an explicit discrete quadratic generating function if possible;
- classify its coefficient freedom;
- account for the exact (Q\leftrightarrow\alpha) reciprocal scaling already frozen by A-NORM;
- determine whether (gamma) survives as an observable modulus.

Do not infer a coefficient from the fact that the map is symplectic.

## 8. Cross-term exhaustion

Search for H-invariant bilinear cross terms between the Hodge and A1/contact structures and between spatial and two-tick variables.

Classify whether they are:

- forbidden by typing/symmetry;
- removable by canonical field redefinition;
- physically observable;
- or additional moduli.

If the common-parent class is actually larger than the frozen four-modulus family, explain why those extra terms were absent from the previous lane and whether the parent-action hypothesis itself introduces new model freedom.

Do not silently enlarge the theory and then claim closure.

## 9. ActionProtocol typing audit

`EndogenousActionQuantum.ActionProtocol` is an action cost over transitions in a `VerificationProtocol.State`.

Determine whether the physical finite gravity quadratic functional is actually typed as that action.

If not, `S_min=1` cannot normalize its coefficients.

If a typed map can be built from owned data, give it explicitly and test whether (S_{min}) fixes only overall scale or any relative coefficient.

## 10. Strong negative controls

Unless a positive selector theorem is derived, construct at least two explicit parent actions on the same frozen scene that satisfy all owned constraints but differ in:

- (u,v), or
- (mu), or
- (gamma),

as appropriate.

A particularly strong no-go would exhibit a continuous family of common actions containing the full frozen ((\mu,\gamma,u,v)) family.

## 11. Strong positive control

If a stronger Level-2/3 parent principle selects parameters, state every additional premise explicitly and prove exactly which moduli it kills.

For example:

- one fixed Euclidean edge Riesz structure may kill (u,v);
- one overall action normalization may still leave (mu);
- a discrete-time generator may or may not fix (gamma).

Do not collapse these logically separate steps.

## 12. Observable quotient audit

After the parent-action classification, redo the genuine quotient analysis:

- overall action scale;
- field-coordinate rescaling;
- (Q\leftrightarrow\alpha) reciprocal scaling;
- symplectic conjugacy;
- branch/time-orientation equivalence.

Return the actual number of observable continuous moduli left.

## 13. Smallest next theorem

If current D0 does not select all remaining moduli, identify the single smallest new theorem/principle that would.

Prefer a typed theorem statement over a slogan such as “one natural action”.

## 14. Terminal verdict

Return exactly one:

- `PARENT-ACTION-SELECTS-ALL-FINITE-MODULI`
- `PARENT-ACTION-FORCES-UNIFORM-WEIGHT-MU-GAMMA-LEFT`
- `PARENT-ACTION-REDUCES-MODULI-PARTIALLY`
- `COMMON-PARENT-ACTION-SELECTOR-NOGO-TERMINAL`
- `PARENT-ACTION-TYPING-BRIDGE-OPEN`
- `PARENT-ACTION-INTRODUCES-NEW-MODULI`

## Required final block

```text
finite fields and carriers:
owned pairings/Riesz maps:
owned action functionals:
levels of common-parent structure:
most general quadratic H-invariant parent action:
allowed cross terms:
common metric forced or assumed:
self-duality W^-1(KPlus) consequence:
uniform-weight consequence:
relative spatial coefficient mu:
ActionProtocol/S_min typing:
two-tick generating function:
temporal coefficient gamma:
genuine quotient group:
observable parameter tuple after parent audit:
number of continuous moduli:
strongest positive theorem:
strongest negative-control family:
smallest missing principle:
impact on A-NORM:
impact on A-WEIGHT/A-CAP:
impact on D0-HODGE-LINKS-001:
terminal verdict:
```

## Deliverable

`MEMO_19_APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md`

Repository edits: **none**.

Separate rigorously:

- repository-owned theorem;
- accepted research;
- newly derived theorem;
- coefficient convention;
- field redefinition;
- modelling premise;
- bridge/passport;
- external calibration.
