# EXP-AWEIGHT-DYN-GENERAL-WEIGHT-HESSIAN

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Compute the **exact compensator-reduced A1 quadratic operator for arbitrary positive H-invariant conformal weights**, decompose it on the six common-carrier H-sectors, and determine the true observable finite modulus count when the A1 weight is not assumed uniform.

This task follows the accepted terminal A-WEIGHT result:

[
\rho=(r_9,r_{11},r_{13})>0,
]
with two projective shape moduli
[
u=r_9/r_{11},\qquad v=r_{13}/r_{11},
]
and
[
W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13}.
]

A-WEIGHT proved that all currently owned selector constraints leave (u,v) free. It did **not** prove that the nonuniform reduced A1 Hessian is a scalar contact shift.

The present task must close exactly that gap.

A terminal negative result or a correction of the anticipated parameter count is fully acceptable.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Task baseline:
the current `main` commit containing this brief.

Treat the task as fully stateless.

## Required CONTROL context

Read first:

- `02_REGISTRY/RESEARCH_LEDGER.md`
- `02_REGISTRY/research/AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`
- `02_REGISTRY/research/ANORM_FINITE_GRAVITY_NORMALIZATION.md`
- `02_REGISTRY/CLOSURE_CONTRACT.md`
- `00_WORK/tasks/CTRL-GRAVITY-DYNAMICS-CLOSURE.md`

If available, read the source research memo:

- `MEMO_16_AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`

Frozen boundaries:

- A-WEIGHT is `WEIGHT-SELECTOR-NOGO-TERMINAL`;
- do not search again for a rho selector using H-symmetry, C1 isometry, Perron, `rho1=1`, `S_min=1`, reciprocity or naturality;
- `W=I` remains conditional on an unowned common-metric/common-parent-action theorem;
- A-NORM's exact two-modulus result `(m^2,gamma)` is valid on its declared unit/uniform A1 branch;
- outside the uniform branch, do **not** assume that the A1 contact term is (4I) or that the symbol (m^2) remains a scalar mass shift.

## Required literal owners

Read literally:

- `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`
- `04_CERTIFICATES/vp_a2_compensator_noether.py`
- `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean`
- `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
- `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean`
- `03_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean`
- the current two-tick/symplectic owner used by A-NORM;
- relevant rows of `02_REGISTRY/claims.csv` for
  - `D0-A2-COMPENSATOR-NOETHER-RESEARCH-001`
  - `D0-C1-COMMON-CARRIER-RESEARCH-001`
  - `D0-HODGE-LINKS-001`.

Do not modify the repository.

---

# Frozen algebra

Let
[
K_+=\ker B_+.
]

For positive block-scalar A1 weight
[
W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13},
\qquad x,y,z>0,
]
the compensator reduction is defined by
[
w=h-B_+^T\phi,
]
with
[
B_+WB_+^T\phi=B_+Wh,
]
and physical response
[
G_{\rm phys}=4Ww,
\qquad B_+G_{\rm phys}=0.
]

The Euclidean common carrier has the six accepted H-sectors
[
K_+
=
Z_{9,11}\oplus Z_{9,13}\oplus Z_{11,13}
\oplus A_9\oplus A_{11}\oplus A_{13},
]
up to the literal repository naming/order.

The Hodge kinetic candidate is already sector-diagonal with the accepted six-sector spectrum from A-NORM.

The research question is the exact reduced A1 operator on this decomposition for arbitrary (x,y,z).

---

# Research programme

## 1. Define the correct reduced A1 operator

Do not confuse:

- the field representative (w);
- the coordinate response (4Ww);
- the Hessian/quadratic form on (K_+);
- the Euclidean Riesz operator representing that quadratic form.

Give a typed finite-dimensional definition of the compensator-minimized quadratic form
[
q_W(h)=\min_\phi 2\langle h-B_+^T\phi,,W(h-B_+^T\phi)\rangle
]
for (h\in K_+), and the associated self-adjoint operator (A_W) with respect to the **fixed Euclidean Hodge/C1 pairing**:
[
q_W(h)=\frac12\langle h,A_Wh\rangle
]
or the repository's exact convention factor.

Track the factor (4) exactly.

## 2. Prove H-equivariance and sector preservation

For block-scalar (W), prove that the reduced quadratic form/operator is H-equivariant.

Determine whether the six accepted sectors are invariant and whether (A_W) is scalar on each irreducible sector.

Do not assume scalarity from the uniform case; prove it from the representation structure or by exact calculation.

## 3. Tensor-sector eigenvalues

For the three zero-marginal tensor blocks, compute the exact A1 eigenvalues.

Candidate formulas to verify, not assume:
[
\lambda_{Z_{9,11}}=4x,\qquad
\lambda_{Z_{9,13}}=4y,\qquad
\lambda_{Z_{11,13}}=4z.
]

Give exact proofs.

## 4. Standard-sector eigenvalues

Compute the compensator reduction on (A_9,A_{11},A_{13}).

A useful candidate arising from weighted minimisation is:
[
\lambda_{A_9}
=
4\frac{xy(11+13)}{11x+13y},
]
[
\lambda_{A_{11}}
=
4\frac{xz(9+13)}{9x+13z},
]
[
\lambda_{A_{13}}
=
4\frac{yz(9+11)}{9y+11z}.
]

These formulas are **conjectural targets**. Verify them from the literal (B_+), sector embeddings and convention factors. If any coefficient/order is wrong, replace it with the correct theorem.

Required controls:

- exact rational/symbolic derivation;
- direct finite-matrix check on the literal scene;
- uniform specialization (x=y=z) recovers the known scalar A1 result.

## 5. Uniform locus

Prove exactly when the reduced A1 operator is proportional to the identity on all six physical sectors.

Key question:
[
A_W=cI\quad\Longleftrightarrow\quad x=y=z?
]

If true, prove it. If false, classify the full exceptional locus.

This determines whether A-NORM's scalar-contact branch is precisely the uniform-weight ray.

## 6. Projective weight coordinates

Use the A-WEIGHT quotient
[
\rho=r(u,1,v)
]
and remove the common (r^{-2}) factor into the overall A1/Hodge relative strength.

Express all six reduced A1 eigenvalues in terms of (u,v) and one overall contact coefficient.

Do not call that coefficient (m^2) until you prove the general operator can be meaningfully parameterized as a scalar mass shift. Prefer a neutral symbol such as
[
\mu=\text{overall A1/Hodge strength}.
]

## 7. Combine with the Hodge operator

Form the exact finite spatial operator
[
Q_{\rm gen}
=
\kappa_H Q_H+\kappa_A A_W
]
on the six sectors.

Give the complete six-sector eigenvalue tuple as a function of the genuine quotient variables.

Determine:

- whether any sector crossings or accidental degeneracies occur generically;
- whether nonuniform A1 weights introduce new operator directions beyond the previously audited Hodge-local class;
- how this result sits relative to A-SEL's
  [
  \operatorname{span}\{I,Q_H,\varepsilon_{A_{11}}\}
  ]
  result.

If there is a tension, resolve the hypotheses rather than declaring a contradiction.

## 8. True modulus count

Audit all genuine redundancies again in the **general-weight** family:

- overall action scale;
- common rho scale vs (kappa_A);
- Q↔alpha reciprocal scaling from A-NORM;
- canonical field-coordinate rescaling;
- symplectic conjugacy;
- branch/sign/time-orientation equivalence;
- basis changes inside irreducible sectors.

Then determine the minimal observable continuous parameter count.

Candidate, not assumed:
[
(\mu,\gamma,u,v)
]
with four moduli.

Required: exhibit an exact finite observable tuple (for example sector transfer traces/eigenvalues) that recovers the surviving parameters locally or globally, or else identify additional degeneracies.

## 9. Temporal law and stability

Keeping the owned two-tick temporal skeleton fixed, compute the sector transfer traces for the general spatial spectrum.

Determine the exact strict ellipticity / positive-energy domain in the surviving parameter space if it can be expressed cleanly.

Do not use stability to select a point unless it actually reduces the dimension.

## 10. Strong negative controls

At minimum compare:

[
\rho_U=(1,1,1)
]
and
[
\rho_N=(1,2,3).
]

Compute their **full six-sector** reduced A1 spectra, not only tensor rectangles.

Show exactly which observables distinguish them after every allowed common normalization quotient.

Also test at least one second nonuniform rational zone triple to ensure no accidental special property of ((1,2,3)) is driving the conclusion.

## 11. Parent-action handoff

At the end, state the exact family that a future common-parent-action selector would need to collapse.

Do not perform the full parent-action search in this task.

The output should make the next task mechanically precise:

- which parameters must be fixed;
- which operator equalities would kill the weight-shape freedom;
- which coefficient must be fixed to recover the uniform A-NORM branch;
- which temporal parameter remains.

## 12. Terminal verdict

Return exactly one primary verdict:

- `FOUR-FINITE-MODULI-PROVED`
- `FEWER-FINITE-MODULI-AFTER-QUOTIENT`
- `MORE-FINITE-MODULI-REQUIRED`
- `GENERAL-WEIGHT-HESSIAN-CLASSIFIED-MODULI-OPEN`
- `GENERAL-WEIGHT-ASSUMPTION-INCONSISTENT`

## Required final block

```text
exact reduced A1 quadratic form:
exact Euclidean Riesz operator:
six invariant H-sectors:
tensor-sector A1 eigenvalues:
standard-sector A1 eigenvalues:
uniform specialization:
uniform locus iff condition:
projective weight variables:
general spatial operator:
six-sector spatial spectrum:
relation to A-SEL locality class:
genuine quotient group:
observable parameter tuple:
number of finite continuous moduli:
two-tick transfer traces:
strict stability/energy domain:
uniform negative control spectrum:
nonuniform negative control spectrum:
smallest parent-action target:
impact on A-NORM:
impact on D0-HODGE-LINKS-001:
terminal verdict:
```

## Deliverable

`MEMO_17_AWEIGHT_GENERAL_WEIGHT_REDUCED_HESSIAN.md`

Repository edits: **none**.

Separate rigorously:

- repository-owned theorem;
- accepted research;
- new theorem;
- exact finite computation;
- convention/redundancy;
- modelling bridge;
- external calibration.
