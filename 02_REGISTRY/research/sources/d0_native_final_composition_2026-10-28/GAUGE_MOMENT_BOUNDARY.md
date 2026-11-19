# Original return boundary: diagonal moment map and the physical reduction gate

28 October 2026. Bounded analysis for existing PR #334 at input
`172876cdf38bfce6f87fdd4a059d524b60c10eb9`; native realization / final composition.
No repository claim, new physical charge, or full D0→GR closure is asserted.

## 1. Exact consuming step

The owned original return calculation gives a nondegenerate two-endpoint
boundary form near the Golden pair. The owned moving-cut calculation gives
zero full scalar source under simultaneous unitary co-transport. These two
facts cannot be composed by declaring the same co-transport a null direction
of the nondegenerate boundary form. Here the missing contraction is computed
exactly. It gives a precise requirement for the physical reduction, rather
than another presumed ADM or HDA construction.

Inputs in this snapshot:

- `sources/d0_native_boundary_rigidity_2026-10-28/CUT_BOUNDARY.md` and
  `BRACKET_TRANSPORT.md`: original return mixed Hessian and its norm.
- `sources/d0_root_moving_cut_2026-10-28/PROOF_RU.md`: full moving-cut source.
- `sources/d0_root_boundary_reduction_2026-10-28/PROOF_RU.md`: complete
  spectral Hessian, conditional stationary boundary reduction and sewing.

All operators below act on one finite positive Hilbert carrier. Set

    P=P0, T=P1=U†P0U,
    S(P,T)=-log det(I-z P(I-T)P),       0<z<1,
    R=(I-z P(I-T)P)^(-1), A=P R P.

T is the SECOND ENDPOINT PROJECTOR. It is neither the original archive
complement I-P nor the reflection QUERY in §7cu. The free equal-rank
projector-pair chart is the already owned mathematical ambient chart;
physical admission of its directions is not inferred.

## 2. A moment map is actually present

Holding P fixed gives

    D_T S[dT] = -z Tr(A dT),
    theta_plus=-z Tr(A dT),       Omega=-d theta_plus.       (1)

The diagonal unitary action sends (P,T) to (gPg†,gTg†).
It preserves theta_plus, since A transforms to gAg†. For an anti-Hermitian
X let v_X=([X,P],[X,T]). Cartan's formula then gives the exact identity

    i_(v_X) Omega = d mu_X,
    mu_X=theta_plus(v_X)
        =-z Tr(A[X,T])=-z Tr([T,A]X).                     (2)

The last trace is real. Pairing anti-Hermitian matrices by their real trace,
the moment matrix is mu=-z[T,A]. This is the standard moment-map mechanism
for an invariant boundary one-form, here evaluated for the unchanged
return determinant. No new physical canonical field is introduced.

On the full symplectic pair chart the associated Hamiltonians obey

    {mu_X,mu_Y}=mu_[X,Y]                                  (3)

in the convention {q,p}=1 and i_(X_H)Omega=dH. One can verify (3) from
mu(gPg†,gTg†)=g mu(P,T)g†: v_X(mu_Y)=-mu_[X,Y], while
v_X(mu_Y)={mu_Y,mu_X}. This is the diagonal unitary algebra, not a proof of
the geometric hypersurface-deformation algebra.

Invariance of S only implies its two endpoint momenta agree:

    p_minus(v_X at P)=p_plus(v_X at T)=mu_X.                (4)

It does not imply either endpoint momentum is zero.

## 3. Golden value and zero level

At the owned rank-r Golden block put p=phi^(-1), c=sqrt(p), s=p, and

    P=[I 0;0 0], T=[c²I -csI;-csI s²I],
    d=1-zs², J=[0 -I;I 0].

Then A=P/d and direct multiplication yields

    mu=(z c s/d) J != 0.                                  (5)

There is a global exact characterization, not only a Golden computation:

    mu(P,T)=0   iff   [P,T]=0.                             (6)

Proof: relative to im(P)⊕ker(P), A=diag(A0,0) and A0 is strictly positive
and invertible. If [T,A]=0, its off-diagonal block T_21 A0 is zero, hence
T_21=0 and T_12=0; thus [P,T]=0. Conversely, if [P,T]=0, then P(I-T)P,
R, A and T commute. QED.

Thus the zero-moment reduction of THIS FREE RETURN PAIR misses the transverse
Golden pair. This is not a no-go for a complete native reduction: retained
U, Delta, clock, history and apparatus covectors can contribute to the TOTAL
moment, and an actual nonzero momentum sector can be legitimate if its
physical value and constraints are supplied.

## 4. An explicit contraction and quotient on the native real rank-one block

Take two real lines of angles alpha and beta and set delta=alpha-beta.
The unchanged return is

    f(delta)=-log(1-z sin²(delta)),
    Omega=f''(delta) d alpha wedge d beta,
    mu_diag=-f'(delta),
    i_(partial_alpha+partial_beta) Omega=-d f'(delta).     (7)

At the Golden angle, sin²(delta)=p²,

    f''(delta)=2z[1-(2-z)p²]/(1-zp²)²=kappa_H>0.          (8)

In the Euclidean angle-chart norm the contraction of the unit diagonal
vector (partial_alpha+partial_beta)/sqrt(2) has norm exactly kappa_H.
It is therefore NONZERO on the same original chart whose smallest
mixed-Hessian singular value was previously computed. The active symmetry
preserves the two-form but is not a null direction of it.

For a form on a quotient to pull back to this pair chart, it must be
horizontal: contraction with every vertical vector must vanish. Equation
(7) disproves that condition. The invariant coordinate is only delta;
every two invariant functions f1(delta),f2(delta) have zero Poisson bracket.
Locally a fixed moment value at the Golden point fixes delta, since
f''!=0. Dividing the resulting one-dimensional level by the common-angle
rotation gives a point. Hence the same real rank-one pair does not by itself
leave a metric canonical pair after this gauge reduction.

This tiny exact original-return example is the decisive negative control.
It is not a statement about the dimension of the complete retained D0
history or about GR's physical degrees of freedom.

## 5. The small-perturbation route cannot also make all gauge directions null

On a common pair chart suppose the previously derived estimate holds:

    sigma_min(Omega_fb)>=mu>0,
    ||Omega_full-Omega_fb||<=eta mu,      eta<1.

For every unit nonzero diagonal generator tangent v,

    ||i_v Omega_full|| >= (1-eta)mu >0.                   (9)

Consequently, preserving the full nondegeneracy by that perturbation bound
does not simultaneously make the form basic for a nontrivial diagonal
quotient of the WHOLE pair chart. This is just the elementary lower singular
value inequality. It does not forbid a constrained level, followed by a
quotient, or a larger complete phase space with compensating momenta.

For example, if a genuine complete boundary phase space is supplied as a
product with independent retained variables and symplectic form Omega_total,
its diagonal moment is mu_return+mu_retained. It is that sum which must have
the actual chosen level. Under the usual regularity conditions, restriction
to the level and quotient by its stabilizer can produce a symplectic space.
The retained variables, the level, regularity, and operational metric map
must all be derived from the actual execution. Writing a compensating
moment by hand would add the missing physical input rather than prove it.

## 6. Full price covariance gives total momentum balance, not an open phase space

Let M denote the actual finite data manifold carrying P,U,Delta and every
other retained argument. On the mathematical cotangent bundle T*M the
diagonal action has the canonical moment

    J_X(m,lambda)=lambda(v_X(m)).                          (10)

The unchanged root B is invariant under simultaneous co-transport of ALL
its arguments. Its terminal covector section therefore satisfies

    J_X(m,dB_m)=dB_m(v_X)=0.                               (11)

For the P,U feedback sectors this cancellation can also be written directly.
Let C=(I-P)UP, R=(I-zC†C)^(-1), E=[R C†,U]. Then

    g_P=z(E+E†),   g_U=2z C R,
    Tr(g_P[X,P])+Re Tr(g_U†[X,U])=0.                      (12)

The heat term vanishes separately because [rho_beta,Delta]=0. All actual
independent beta,z or additional price arguments retain their covectors;
scalar parameters fixed by conjugation do not change (11).

However the pullback of the cotangent symplectic form to this section is

    (dB)^* Omega_can = -d(dB)=0.                           (13)

Thus (11) supplies a zero total moment on a Lagrangian terminal graph; it
does NOT provide the nondegenerate physical phase space assumed by the
canonical rigidity theorem. Restricting canonical brackets to that graph
without a separate constraint/reduction construction is not justified.
The cost-shifted cotangent lift of an invertible actual retained update
preserves the form, so it also transports a terminal Lagrangian graph to a
Lagrangian graph. Retaining more copies of the same exact terminal gradient
does not undo (13).

If an actual independent two-boundary chart and regular interior stationary
branch exist, the owned full spectral Schur theorem instead supplies a
boundary generating relation. When its symmetry is equivariant, it gives
the conserved equality (4) for the TOTAL endpoint moments. Zero or nonzero
level reduction must then be imposed only by the actual physical boundary
constraints; it is not inferred from scalar invariance.

## 7. Arbitrarily smearing the known full covector is not a local Hamiltonian

There is a second exact missing step. Suppose the actual local coordinates
are partitioned into blocks a, and one tries to create a local generator by
weighting the already known source, without deriving a new lapse-dependent
operator map:

    alpha_N=sum_a N_a sum_i B_(a,i) d y^(a,i),              (14)

where N_a are independent constant weights. If dH[N]=alpha_N on an open
chart, then alpha_N must be closed. Commuting mixed derivatives gives

    d alpha_N=sum_((a,i)<(b,j))
      (N_b-N_a) B_((a,i),(b,j)) d y^(a,i) wedge d y^(b,j). (15)

Therefore the existence of H[N] with this particular differential for EVERY
independent N is equivalent, locally on a contractible chart, to vanishing
of every cross-block Hessian. Necessity follows by choosing two different
weights; sufficiency is the Poincare lemma, since (15) is then zero.
Uniform N is no obstruction: alpha_N=N dB=d(NB).

Two exact controls use the unchanged spectral terms:

1. For the full two-mode heat operator Delta=diag(e1,e2),
   H=beta^(-1)log(exp(-beta e1)+exp(-beta e2)) has
   H_12=-beta rho1 rho2<0. At beta=1,e1=0,e2=log(2) it is exactly -2/9.
   Even direct-sum operator blocks do not remove the shared thermal
   normalizer. This is a mathematical operator chart, not admission of
   independent native energy knobs.
2. The real original-return pair in §4 has S_(alpha beta)=-f''(delta),
   nonzero at the Golden pair. On the rational orthogonal control c=4/5,
   s=3/5,z=1/4 the exact coefficient is -1850/8281. Thus different endpoint
   weights in (14) fail to produce a closed one-form even before a locality
   interpretation is supplied. Endpoint weights are NOT thereby identified
   with spatial lapses.

The concurrent original-native-word locality analysis provides an actual
paid-word cross-Hessian witness with a controlled full heat contribution;
its continuous angle comparison retains its own explicit admission boundary.
Equation (15) can be applied to that witness only on its stated comparison
chart, not silently transferred to the whole physical X_N.

This excludes one particular proposed construction of H[N], not all local
Hamiltonians. For a genuine local density H[N]=integral N h, variation and
integration by parts generally produce DERIVATIVES OF N as well as N times
the unsmeared source. A native lapse-dependent operator or action map could
also contribute additional covectors. Those terms must be derived from the
actual process; copying the single scalar B's covector with different weights
does not create them. The unproved local generator is therefore not supplied
merely because the complete global source has been computed.

## 8. What changes in the final composition attempt

The available diagonal unitary covariance produces (2), (3), and (11).
It does not supply independent local lapse profiles, the metric-dependent
shift q^ij(N partial_j M-M partial_j N), or the actual normalization relating
that shift to physical generators. In particular, verifying zero constraint
values on the terminal graph would be a weak, vacuous check, whereas the
owned HKT consumer needs a strong off-shell identity on its canonical chart.

The immediate native problem is now an explicit physical total-momentum
reduction and independent boundary realization: determine the actual
retained variables and boundary constraints, evaluate their complete moment
balance, prove rank after restriction/quotient, and identify the resulting
metric and lapse deformations. If that succeeds, the owned bracket transport
and canonical rigidity results can be used. Neither a second arbitrary
symplectic form nor an ADM Hamiltonian has been inserted here.

The result closes the incorrect inference from price covariance to a basic
return two-form and the naive source-component smearing construction of local
Hamiltonians. It does not close D0→GR. The separate native source route
to the already owned nonvacuum solution remains available at its actual
source/admission hypotheses.
