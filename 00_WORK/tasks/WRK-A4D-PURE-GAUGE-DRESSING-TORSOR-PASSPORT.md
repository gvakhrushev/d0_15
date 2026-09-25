# WRK-A4D-PURE-GAUGE-DRESSING-TORSOR-PASSPORT

## Class
WORKER

## Parent
`CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE`

## State
PLANNED

## Baseline
Start from fresh current `main`, at least `4527bd8937fd4888704197b571e9a3f94dfa6f29`.

## Research owner
Read completely:

- `02_REGISTRY/research/MEMO_A4D_FINITE_GRADED_COFRAME_DRESSING.md`;
- the owned pure-gauge dressing / crossed pure-gauge modules referenced by that memo.

Frozen terminal:

`FINITE-GRADED-COFRAME-DRESSING-MODULI-CLASSIFIED`.

Do not reopen the research question of whether a canonical arbitrary-background dressing is selected.

## Goal

Lean-own the narrow algebraic torsor passport:

> changing a pure-gauge dressing representative by a commuting right orthogonal isotropy factor leaves the descended horizontal letter and constitutive shadow unchanged, while adding a skew tangent leaves the first constitutive derivative unchanged.

This task does **not** construct an arbitrary-background dressing.

## Finite torsor theorem

Let (F) be an invertible dressing representative, (R) an invertible isotropy factor, and (U) an archive translation/operator.

Assume

[
RU=UR.
]

For

[
F'=FR,
]

prove exactly

[
oxed{
F'U(F')^{-1}=FUF^{-1}.
}
]

The theorem must make the commutation hypothesis explicit.

If the existing API supports Role-labelled translations cleanly, also provide the corresponding all-Role specialization without duplicating the algebra.

## Constitutive descent

For the constitutive shadow

[
W(F)=F^{-T}F^{-1},
]

assume (R) is orthogonal:

[
R^TR=I.
]

Prove

[
oxed{
W(FR)=W(F).
}
]

Keep this object distinct from the arbitrary-background constitutive section
`W_flux = I + H(e)`.

## Torsor separation

Provide a typed theorem/corollary showing that two representatives

[
F,qquad FR
]

may be distinct while their descended horizontal and constitutive outputs agree.

A concrete nontrivial (L=3) constant-potential isotropy witness may be added if it reuses the landed archive-difference API without creating a large dependency surface. It is not required for the abstract core theorem.

## First-order skew passport

Define/reuse the tangent constitutive response

[
mathcal D(G)=-(G^T+G).
]

For any skew (A),

[
A^T=-A,
]

prove

[
oxed{
mathcal D(G+A)=mathcal D(G).
}
]

Where the ambient finite-dimensional linear-algebra API makes it clean, also prove the converse form:

[
mathcal D(G_1)=mathcal D(G_2)
]

iff

[
G_1-G_2
]

is skew.

This is the Lean owner for the research statement that (DW_0=H) determines the symmetric tangent part but not the skew part.

## Mandatory negative control

Prove or encode an explicit finite witness showing that orthogonality of (R) alone does **not** imply horizontal-letter descent when (R) fails to commute with (U).

Do not weaken the horizontal theorem by accidentally dropping its commutation hypothesis.

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DPureGaugeDressingTorsorPassport.lean`

Prefer one compact module.

## Reuse / typing requirements

Reuse existing repository definitions where they fit:

- archive translation / shift;
- pure-gauge dressing carrier;
- inverse / transpose or adjoint;
- orthogonality.

If the owned carrier is too specialized for the algebraic theorem, prove the core statement abstractly over a finite-dimensional real inner-product space and then provide a short specialization to the owned carrier.

Do not introduce a competing matrix universe merely to simplify notation.

## Required controls

At minimum:

1. (R=I);
2. a nontrivial commuting orthogonal (R), abstract or concrete;
3. an orthogonal but noncommuting (R) for which horizontal descent fails;
4. nonzero skew (A) with unchanged tangent constitutive response.

## Firewalls

Do not construct or select:

- arbitrary-background (F_e);
- equivariant exact-orbit retraction;
- rank/holonomy resolution (Xi);
- crossed (T_kappa) action;
- second-order Hessian/stress;
- Einstein/continuum;
- physical time;
- golden/AF refinement.

Do not claim the finite torsor freedom and infinitesimal skew freedom are the same modulus without a theorem.

## Exit condition

The task is complete only when Lean owns:

[
(FR)U(FR)^{-1}=FUF^{-1}
]

under commuting right isotropy,

[
W(FR)=W(F)
]

under orthogonal right isotropy,

and

[
mathcal D(G+A)=mathcal D(G)
]

for skew (A), together with the mandatory noncommuting negative control.

No `sorry`.
No new axioms.
Do not self-merge.

## GitHub-first flow

1. refresh from current `main`;
2. run
   `python tools/task_lifecycle.py start WRK-A4D-PURE-GAUGE-DRESSING-TORSOR-PASSPORT`;
3. commit only lifecycle-generated control-plane changes;
4. open Draft PR **before** any Lean implementation edit;
5. implement the theorem package;
6. run narrow build on the new module;
7. run full `D0.All` / repository guards;
8. self-retire the task before Ready;
9. set `Lifecycle: REVIEW`;
10. do not self-merge.
