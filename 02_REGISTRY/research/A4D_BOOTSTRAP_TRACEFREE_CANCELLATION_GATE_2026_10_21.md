# Bootstrap tracefree cancellation necessity on the native flat carrier

21 October 2026. Existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.

This packet composes two already-owned first-source results on the Book03
§03.25 master bootstrap and turns their previous qualitative boundary into
one exact quantitative gate.

No new action, heat, feedback law, field, selector or calibration is
introduced. The theorem is conditional on identifying the bootstrap heat with
the stated soldered Hodge square on the declared homogeneous positive
observer carrier. It then proves what the bootstrap feedback **must** do on
one tracefree tangent, and excludes the existing fixed-golden-compression
two-tick feedback class as that compensator.

`GR_closed=false`.

## 1. The action-layer scalar is fixed

Book03 §03.25 selects

[
 mathcal B_N
 =eta^{-1}logoperatorname{Tr}(e^{-etaDelta_N})
  -logdet(I-zF_N).
	ag{1}
]

Write

[
 B_H=eta^{-1}logoperatorname{Tr}(e^{-etaDelta_N}),qquad
 J_F=-logdet(I-zF_N).
]

Thus every admitted first variation satisfies

[
 Dmathcal B_N=DB_H+DJ_F.
	ag{2}
]

This theorem does not use a mean Cost-Info action or a Shannon replacement.

## 2. Existing heat result fixes one exact nonzero tracefree source

Consume `A4D_NATIVE_SOLDERED_HEAT_SOURCE.md`, section 5. On its literal
homogeneous full16 Hodge/CAR square, at

- (L=4),
- (eta=log(2)/32),
- flat (Q=I),
- rest observer,

the packed heat covector is exactly

[
 operatorname{pack}(C)=
 left(
 -rac{64}{3},
 rac{128}{9},rac{128}{9},rac{128}{9},
 rac{64}{3},
 rac{128}{9},rac{128}{9},
 rac{64}{3},rac{128}{9},rac{64}{3}
 ight).
	ag{3}
]

For the Lorentz-tracefree off-diagonal metric tangent

[
 H_{01}=E_{01}+E_{10},
	ag{4}
]

the packed-coordinate convention already includes the factor two and gives

[
 oxed{DB_H[H_{01}]=rac{128}{9}.}
	ag{5}
]

The target flat Einstein comparator on the same metric is zero in this
direction. A pure volume term also has zero response on (4).

The statement (5) is conditional only in the sense already recorded by the
heat owner: the soldered square must actually be the bootstrap
(Delta_N). The matrix derivative itself is exact once that identification
is made.

## 3. Therefore the feedback source is not optional

If the Book03 bootstrap is stationary on this flat tracefree tangent, (2)
and (5) force

[
 oxed{DJ_F[H_{01}]=-rac{128}{9}.}
	ag{6}
]

Equivalently, for the native feedback operator,

[
 oxed{
 z,operatorname{Tr}!left[
  (I-zF_N)^{-1}DF_N[H_{01}]
 ight]=-rac{128}{9}.
 }
	ag{7}
]

No normalization convention, endpoint scalar, field-independent baseline or
volume-only remainder can change (6).

Equation (6) is the exact cancellation target for any proposed same-execution
bootstrap feedback map paired with this heat.

## 4. The existing fixed-golden-compression feedback class cannot supply it

Now consume `A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md`. For the actual
ordinary and recorded Golden operations, throughout its declared
fixed-golden-compression orthogonal completion class with arbitrary finite
archive size, the complete two-step feedback price satisfies

[
 oxed{DJ_2=0}
	ag{8}
]

for every differentiable curve staying in that class with fixed (p,z).

The proof keeps the full archive and permits nonzero operator first jets; the
vanishing is the scalar log-determinant source, not a statement that
(DF_2=0).

Combining (6) and (8),

[
 0
e-rac{128}{9}.
]

Hence:

### Theorem

If the bootstrap heat is identified with the soldered Hodge square used in
(3)--(5), then the Book03 bootstrap feedback on the same flat tracefree
physical tangent **cannot** remain inside the existing
fixed-golden-compression two-step completion class.

This excludes the direct composition

[
 Delta_N=Delta_{m soldered},
 qquad
 F_N=F_{2,m fixed Golden compression}
	ag{9}
]

as a stationary flat bootstrap realization on tangent (4).

It does **not** exclude:

- a feedback map whose field variation leaves the fixed-compression class;
- moving (p,z) if those are independently derived physical variables;
- a different active cut/projector with its actual source;
- a different native Hodge pairing/square;
- additional genuine Book03 action terms if the core definition is extended.

Every such alternative must carry its actual derivative and satisfy (6) if
the heat identification is retained.

## 5. What this changes in the closure architecture

The open bootstrap map is no longer merely

[
 Xlongmapsto(Delta(X),P(X),U(X),G(X)).
]

Under the natural soldered-heat candidate it has the quantitative
first-source constraint

[
 oxed{
 D J_{m feedback}^{m tracefree}
 =-D B_H^{m tracefree},
 qquad
 D J_{m feedback}[H_{01}]=-rac{128}{9}
 }
	ag{10}
]

already at the flat reference.

Therefore the next useful construction is sharply typed:

1. retain the owned positive observer pairing (G(X)) and its unique
   moving adjoint (d^{\dagger_G}=G^{-1}d^*G);
2. build the actual same-execution (P(X),U(X)) on that carrier;
3. differentiate its complete feedback (F=P U^dagger(I-P)UP);
4. test (7) on the ten independent metric directions and the observer/link
   tangents before attempting a curved Einstein root.

A candidate that keeps the old Golden compression at first order is rejected
immediately by (6)--(8). This removes a large class of otherwise plausible
same-name identifications.

## 6. Exact checker

The companion `check_bootstrap_tracefree_gate.py` verifies the rational
source target, the impossibility of zero feedback cancellation, the
Book03 sign convention, and several false-sign/factor controls. The
all-size feedback-zero theorem and the soldered heat derivative are consumed
from their pinned analytical owners rather than numerically re-derived.

No independent review, fresh Lean build, repository-wide CI, curved
stationary solution or GR closure is claimed here.

`GR_closed=false`.
