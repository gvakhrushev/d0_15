# Endpoint pairing, the forced metric correction and the actual two-record jet

Date: 13 October 2026. Existing Draft #310; input SOURCE
`a7ad40cd3cb5410c2c50332eb4e47c2ed437fc95`, canonical main
`fa2b04b9c8aae5a0b8470322d6091712ce56567a`.

This continues [the full Fock binding](A4D_NATIVE_FOCK_RECORD_BINDING.md)
and [the native matter pairing](A4D_NATIVE_MATTER_OBSERVER_PAIRING.md).
It tests a specific missing arrow: applying the literal record, keeping its
full positive pairing, updating the metric from the recorded matter, and
then applying the literal record again. The original price readout and all
sixteen components are retained. No new blank is prepared between ticks.

**Result.** Conditional on endpoint isometry of that binding, the next
positive metric is unchanged and the next Lorentz metric is uniquely
determined wherever the new first grade is nonzero. The second gate is
generally different from the first. Its full chronological feedback price
and its actual differential are given below. It has nonzero matter jets,
but its factor-imbalance jet is exactly zero on a complete congruently
prepared factor curve, including the metric correction and the second
gate. The existing nonzero heat factor jet therefore survives on that
curve in this binding. Physical admission of this transition and of the
price remains an open hypothesis, not a conclusion of endpoint isometry.

## 1. What is assumed, and what is solved

Use the full real exterior fibre, q of signature (+---),
v=m^1, k=v^T q^-1 v>0, and the previous explicit pairing

    Q=-q+2vv^T/k,  G=Q^-1,  S=C_*(G),
    W=omega S,  omega=sqrt(abs(det q))=sqrt(det Q).

The actual current record is U=U_F(q,m), with the native positive constants
a^2=p, p+p^2=1. It is W-orthogonal. Its full state output is prescribed by
the literal operator, m_plus=U m. All other grades remain present. Now ask
whether a next metric in the **same pairing construction** can satisfy

    U^T W(q_plus,m_plus) U = W(q,m).                    (1)

Since U is invertible and already preserves W(q,m), (1) is equivalent to
W_plus=W. The grade-zero block of W gives omega_plus=omega, and the
grade-one block then gives G_plus=G. Thus Q_plus=Q. This is an exact
necessity, not a selected compensating metric. It also shows that replacing
the endpoint pairing by its old value without solving its field arguments
would omit an equation.

Put w=(m_plus)^1. If w!=0, positive G gives s=w^T G w>0, and the unique
solution of (1) in the timelike first-grade construction is

    q_plus = -Q + 2ww^T/s.                             (2)

Indeed q_plus^-1=-G+2(Gw)(Gw)^T/s, w^T q_plus^-1 w=s,
Q(q_plus,w)=Q, and det q_plus=-det Q. Conjugating by a positive square
root of Q reduces (2) to 2nn^T-I for a unit n, proving its Lorentz signature.
Conversely Q=-q_plus+2ww^T/(w^T q_plus^-1 w) forces (2), by contracting
with Q^-1 w. The raw solder can be realized by any Q-orthonormal frame
whose first column is w/sqrt(s); residual spatial frames are retained.

This solves the metric correction **under (1)**. Neither the finite
orthogonality owner nor this calculation proves that (1), this local
matter/pairing construction, or its field-dependent gate is the physical
native transition. There is no new admission condition defining a source
to be zero. This is also not a theorem that all native metric transitions
must preserve Q.

The **whole-operator** premise in (1) is stronger than norm preservation
of the single realized state. For the actual blank m=n+Omega at rest,
its output has only scalar, n, spatial-top and full-top components. Every
`Q_alt=diag(1,l,1/l,1)`, l>0, gives these four components their old weights,
so it preserves that state's norm; nevertheless its full W differs when
l!=1. Thus single-state probability conservation cannot be used as a proof
of (1). This protected distinction prevents (2) becoming an imported law.

## 2. Orientation memory and the actual singular set

The former top-grade condition is needed for the initial whole
gate/price/blank tuple. It is not needed anew for a retained-record second
gate. In the Q-orthonormal frame let c_n be the actual exterior creator
along the unit observer n=v/sqrt(k), let b_n=c_n^dagger and N=c_n b_n.
Let H be the projection onto spatial exterior degree at least two; spatial
degree is total exterior degree minus N. Then the same full gate and cut
from the preceding signed CAR basis are

    U_n = a[(I-H)+H(I-2N)]
             +p[(I-H)(c_n-b_n)-H(c_n+b_n)],
    P_n = I-N.                                        (3)

On spatial grades 0,1, (3) is [[a,-p],[p,a]]; on spatial grades 2,3 it is
[[a,-p],[-p,-a]]. These are precisely the two blocks of the literal fullStep
under the published change of basis. The formula retains every grade and
uses no spatial orientation. Flipping the initial top-grade orientation
changes the blank plane but leaves U_n and P_n unchanged. Consequently a
zero output top grade is not by itself an obstruction to a second retained
record. It still prevents silently preparing a new blank from that grade.

The nonzero-first-grade condition cannot be removed this way. In the old
rest frame, with Omega its initial top form, the genuine blank input

    m=-(a/p)(1+volume_E)+n+Omega

has k=1 and nonzero top grade, but its actual output is
`-(1/p)(1+volume_E)`: its first and fourth grades both vanish. Normalizing
the input preserves these facts. Equation (2) is undefined there, and
there is no timelike first-grade realization in the stated construction.
Information remains in the other grades; no new readout or branch rule is
installed to bypass the singularity.

The preceding spacelike-output example has w=n a-2p e_1!=0. It is repaired
by the uniquely solved q_plus in (2), rather than by claiming that w stays
timelike for the old q. These are different statements. The preceding
top-zero but w=a n example admits a second gate through (3). These tests
separate the actual remaining singularity from an unnecessary per-tick
blank requirement. A global closed native sector is still not proved.

## 3. The complete metric and matter differential

Let V=dot q, xi=dot m, r=q^-1 v and u=xi^1. On the initial domain,

    dot k=2r^T u-r^T V r,
    dot Q=-V+(2/k)(uv^T+vu^T)-(2 dot k/k^2)vv^T,
    dot G=-G dot Q G.                                 (4)

The full recorded-state differential is
`dot m_plus=dot U_n m+U_n xi`. Differentiating (3) includes changes of
the observer, its adjoint, N and H. Freezing any of those is not (4)'s
joint lift. With w= (m_plus)^1 and dot w=(dot m_plus)^1, (2) gives

    dot s=2w^T G dot w-w^T G dot Q G w,
    dot q_plus=-dot Q+(2/s)(dot w w^T+w dot w^T)
                         -(2 dot s/s^2)ww^T.           (5)

At fixed Q the range of (5) has dimension three, with the amplitude of w
in its kernel. At Q=I,w=e_0 it consists of the three symmetric 0i slots.
Equivalently `q_plus G q_plus=Q`; at fixed Q its tangent satisfies

    dot q_plus G q_plus + q_plus G dot q_plus=0.        (6)

This rank restriction is on the next-metric response at fixed Q, not on
all initial q/m variations and not a quotient by physical gauge. In
particular it cannot be advertised as ten-component GR dynamics. Formulae
(4)-(5) keep all ten initial q slots and all sixteen matter slots; unused
grades are not removed from the carrier or made gauge. These are derivatives
on the full open timelike chart, including directions leaving the initial
blank submanifold. A native admission theorem would have to specify which
of them, and which additional equations, belong to the physical experiment.

There is a useful independent check on the operator jet. For G-unit n,
every joint (dot G,dot n) satisfies `2 n^T G dot n+n^T dot G n=0`. Put

    u=dot n+(1/2)G^-1 dot G n,
    A=-(1/2)G^-1 dot G+u n^T G-n u^T G.

Then `A n=dot n` and `-A^T G-G A=dot G`. Exterior naturality gives
`dot U=[rho_*(A),U]`, including the pairing change. The checker independently
compares this with direct differentiation of (3), and uses it for the
second gate. This is a moving matrix frame identity, not a claim that the
physical q variation is gauge or that the chronological price is constant.

Spatial links still satisfy `D_e q_y D_e^T=q_x`, with their full differentiated
constraint. For the homogeneous periodic factor family in Section 5, set
every spatial D_e=I and b_e=0 on each slice; both endpoints have the same
q on that slice, before and after the simultaneous local record. This
satisfies every spatial constraint. No temporal edge equation or curved
link evolution is invented from this homogeneous example.

## 4. Actual two-step price, with the original readout retained

For w!=0, let n_plus=w/sqrt(s). Both U_n and U_n_plus are orthogonal in the
**same** W by (1)-(2). Keep the original P=P_n and set

    K=U_n_plus U_n,
    F=P K^dagger(I-P)K P,  J=-log det(I_16-z F), 0<z<1. (7)

This is the existing feedback functional evaluated on the two actual
successive gates. It is not U_n squared. Replacing the final occurrence
of P by P_n_plus would be a different readout, not a simplification of (7).
All zero eigenvalue factors and all sixteen rows are retained. Full
orthogonality proves 0<=F<=I and hence a positive pencil for every 0<z<1.
If the second output is also to be assigned a metric by (2), its first
grade must again be nonzero. This holds on a nonempty open neighbourhood
of the explicit example below and is checked exactly. It is not claimed
for every initial input or for arbitrarily long trajectories.

Define the signed angle invariant `c=n^T G n_plus`, -1<=c<=1. Spatial
orthogonal covariance of (3) reduces the exact calculation to a rotation
in the (n,e_1) plane. Its complement remains in the full sixteen-dimensional
calculation. In the eight active coordinates the feedback splits into two
scalar blocks, two identical 2-by-2 blocks, and one further 2-by-2 block.
With p^j denoting the actual powers of the golden root, put

    l = p^2 (1+c)(1+p^3 c),
    t = 2(p^2+p^5 c^2),             d = p^4(1-c^2)^2,
    t0 = 2(1-c)[2p^4 c^3+2p c^2+(3p-1)c+p^2],
    d0 = (1-c)^2[5p^4 c^2+(14p-8)c+p^4].

Their traces and determinants give the **whole** pencil

    A=1-z l,  B=1-z t+z^2 d,  C=1-z t0+z^2 d0,
    det(I_16-zF)=A^2 B^2 C,
    J(c)=-2 log A-2 log B-log C.                       (8)

The matrix proof ensures each A,B,C is positive on the stated domain;
positivity is not inferred merely from the sign of their product. At c=1,
(8) is `(1-4zp^3)^4`, as required by the previous same-frame result.
At general c it is different. The checker derives all blocks from the
literal full CAR operator and independently differentiates their entries.

For a same-process variation, at fixed native p,z,

    dot J = j(c) dot c,
    j(c)=2z l'/A+2(z t'-z^2 d')/B+(z t0'-z^2 d0')/C,
    dot c=dot n^T G n_plus+n^T dot G n_plus+n^T G dot n_plus. (9)

Here n=v/sqrt(k), n_plus=w/sqrt(s), with their actual derivatives from
(4)-(5). Thus all ten metric slots, matter motion and the moving pairing
enter the single invariant through the same path. At coincident observers,
dot c=0 for every differentiable jointly unit pair; this does not assert
that every chronological price jet is zero.

The invariant can also be read directly from the input state. Let
`e=contraction_(G n)(m^2)`, which is G-orthogonal to n, and put
`alpha=p m^0+a sqrt(k)`, `E2=e^T G e`. The literal gate gives

    w=alpha n-p e,  s=alpha^2+p^2 E2,
    c=alpha/sqrt(s),
    dot c=p^2(E2 dot alpha-alpha dot E2/2)/s^(3/2).     (9a)

Thus the singular set is exactly alpha=0 and e=0. The other grades remain
in the process, even though this particular two-record scalar price only
reads these invariants. Derivative kernels are not physical gauge.

For example a normalized genuine blank family proportional to

    n+Omega+r(n wedge e_1+n wedge star_E e_1)

has `w` proportional to `a n-p r e_1` and
`c=a/sqrt(a^2+p^2 r^2)`. At r=4/(3a), c=3/5 and
`dc/dr=-36a/125`. At the exact test value z=1/2, j(3/5)!=0. This is a
nonzero matter derivative of (7), not a fitted source, chosen phase or a
proof that z=1/2 is the physical fugacity.
The first output has unit direction `(3/5,-4/5,0,0)`. Applying its actual
next gate gives a nonzero first grade at the second output as well; (2)
therefore supplies both consecutive metric corrections in this example.

For an explicit full-coordinate comparison, take q=diag(4,-1/4,-1,-1)
and initial matter with occupation-mask coefficients
`m_1=2, m_3=1, m_13=2, m_15=1`, all others zero. This is the transformed
genuine blank input at r=1, with c=a. The actual angle differential is

    dot c = -2a p^2 V_11 + p^3 xi_0
                      +(a p^2/2) xi_1-a p^2 xi_3.     (9b)

Indices 0,1,2,3 on q are physical matrix indices; indices on xi are the
sixteen occupation masks. In particular xi_3 is the 01 two-form slot,
not the fourth vector component. The other nine packed q coefficients
and thirteen matter coefficients vanish. The checker retains and tests
all of them, and compares the direct full-matrix Jacobi derivative with
`j(a) dot c` in all 26 directions. At z=1/2, j(a) is nonzero.

## 5. The requested factor jet on a whole corrected preparation

Use the same nonzero-r blank preparation and its literal first output.
Let `F_t=diag(2 exp(t), exp(-t)/2,1,1)` and transport the full initial
state by the **actual exterior representation** `m_t=rho(F_t)m_0`.
Then

    q_t=F_t eta F_t^T,
    Q_t=F_t F_t^T=diag(4 exp(2t),exp(-2t)/4,1,1),
    m_plus,t=rho(F_t)m_plus,0,
    q_plus,t=F_t q_plus,0 F_t^T.                       (10)

Equations (1)-(2), the actual first state output, the next gate, and the
unchanged original readout all obey (10) by exterior congruence. In
particular `c_t=c_0`, including the nonparallel example c_0=3/5. Hence

    R'_tf = dJ(K_t,P_t)/dt = 0.                       (11)

The raw q tangent is diag(8,1/2,0,0), satisfies
`Tr(q^-1 dot q)=0`, and obeys every spatial q/D constraint with D=I.
All sixteen matter components and their tangent are carried in (10);
they are not fixed while the prepared input changes. For N sites the
literal determinant price is N J, and (11) remains zero without a new
normalization. Density and determinant of Q are constant on this curve.
At the reference point of (9b), `xi_1=2, xi_13=2` on this curve. Its
q contribution to dot c is -a p^2 and its matter contribution is +a p^2.
Keeping only the metric partial would therefore give a false nonzero
factor source for the chronological record.

For the existing full positive Hodge heat binding on the same periodic
four-dimensional carrier, the before- and after-record heat operators use
the same Q_t. The published factor result therefore applies without
freezing the recorded state:

    d/dt [ beta^-1 log Tr exp(-beta Delta_Qt) + J_t ]
        = 2(E_1-E_2) > 1/10000                        (12)

at beta=log 2 for every L>=2, in particular L in 4N. This all-L bound is
the already published analytic theorem, not an extrapolation from the
new finite controls. The homogeneous Lorentz metric is flat, so the
geometric rho0 comparator is zero. A constraint multiplier gives zero
on this tangent and cannot cancel (12). There is no claim that matter
stress vanishes, or that this comparison supplies a source-subtracted
native equation.

For clarity, all ten **homogeneous** coefficients of this whole candidate
price can be written at the same reference point. Let N=L^4 be the actual
number of full local record copies, j=j(a), and retain the prior heat
moments E_0,...,E_3 (here using zero-based indices). Packed off-diagonals
have the factor two:

| q slot | coefficient of the whole price | flat geometric rho0 |
|---|---|---|
| 00 | E_0/4 | 0 |
| 01 | -E_0 E_1/(2 L^2) | 0 |
| 02 | -E_0 E_2/(2 L^2) | 0 |
| 03 | -E_0 E_3/(2 L^2) | 0 |
| 11 | -4E_1-2N a p^2 j | 0 |
| 12 | -E_1 E_2/(2 L^2) | 0 |
| 13 | -E_1 E_3/(2 L^2) | 0 |
| 22 | -E_2 | 0 |
| 23 | -E_2 E_3/(2 L^2) | 0 |
| 33 | -E_3 | 0 |

The accompanying matter covector is

    N j[p^3 xi_0+(a p^2/2)xi_1-a p^2 xi_3]
       +(2E_0/L^2)(E_1 xi_2+E_2 xi_4+E_3 xi_8).       (13)

The unmodified feedback multiplicity N is essential; no intensive price
has been substituted. These coefficients concern spatially constant
variations of the full finite price. They are not a local stress tensor
or a ten-row source-subtracted native Einstein equation. Combining the
table with (13) on the actual factor tangent gives precisely (12).

Thus updating the metric by endpoint isometry and using genuine record
chronology does not furnish the missing factor compensator in this named
binding. Stationarity or O(h) physical contrast transfer still needs the
independently owned full price/source and its actual admitted variations.
Excluding (10) requires an admission theorem and equations for omitted
directions; (11) is not placed into a native gate definition.

## 6. Evidence and the next obligation

The paired exact checker verifies the full CAR formula, the solved
endpoint equation, singular blank input, all active determinant blocks,
hostile alternative readouts/resets/frozen metrics, complete 26-slot
initial, next-metric and two-gate price derivatives, the next-metric rank, and a genuine
nonzero chronological matter jet. Baseline hashes are pinned to the
published input. The group reduction and universal analytic statements
above are proved in the text; finite controls do not formalize them all
in Lean.

The next obligation is admission of a closed joint preparation and its
complete constitutive price, including link/affine dependence, singular
state handling and refinement. Equation (2) is a solved conditional
transition, not proof that its hypothesis is core-forced. Equations
(9)-(12) now give a concrete complete chronological component to consume
in that proof. Native source/Ward, curved on-shell roots, soundness/recovery,
GR and the original #310/#202/#317 terminals remain open.
