# Independent review: covariant solution map and non-VSI crossing streams

21 October 2026. Review within existing PR #334 by the independent
`preparation_closure` executor. The reviewer did not author the two reviewed
proofs or their checkers. No source files were changed by this review.

Reviewed bytes:

| File | SHA256 |
|---|---|
| `PROOF.md` | `e7a71e11ac1f8d6fd8fc49101aa231ccea4c5c23352f913a041d33995ebeccb2` |
| `CROSSING_STREAMS.md` | `c2cc72d1bcacbee21271c99549d70f86ee708439502211a1555d027e68b83326` |

## 1. Verdict and actual scope

**Accepted as an analytical theorem about the specified continuum price.**
The local forward/reverse solution map, its positive-volume gauge, the
fixed-sector Jacobi correspondence in an already common gauge, and the
explicit two-scalar non-VSI witness are mathematically consistent. The
non-VSI witness was checked independently through proper-time Bianchi-I
equations and electric Weyl curvature, rather than by importing the author's
coordinate Riemann calculation.

The accepted substitution is into the *same conditional fixed-measure
continuum dictionary* of the density-rigidity owner. It is not a finite
Cartan-lattice solution, a proof of physical Book03 admission, an absolute
price equality, or off-shell covariance of the original nonlinear price.
Its two scalar components have an undensitized kinetic query and no
independent spin-connection source. These hypotheses are essential.

## 2. Full variation, gauge and the total-null sector

For fixed `q_*`, independent variation of

    I = integral vol_g [R-Lambda(q-q_*)]

gives the multiplier constraint `q=q_*`, the independent Palatini equation,
both equations `div_g(Lambda grad psi_A)=0`, and

    G_mu_nu - Lambda K_mu_nu
      + (Lambda/2)(q-q_*)g_mu_nu = 0.

The Einstein-Hilbert coefficient is one, so the constrained metric equation
is exactly `G=Lambda K`. There is no missing factor of two and no omitted
metric-volume term. The term proportional to the metric vanishes because
of the independently varied multiplier equation.

On the positive branch, `Lambda vol_g` is a positive local volume form.
The one-coordinate integration in PROOF (9) has Jacobian
`e Lambda/k_*`; it therefore proves the exact local gauge
`e_new Lambda=k_*`. The trace and scalar equations then give

    y=-eta^2 q_*=y_*,
    x=eta^2 eR=k_* y_*=tau(y_*),
    div_g(Lambda grad psi_A)
      =(k_*/e) partial_mu(g^(mu nu)partial_nu psi_A).

This verifies both directions of the native stationary-solution map. At
`q_*=0`, the proof uses `k_*=r_y(0,0)/r_x(0,0)` directly and never divides
by the vanishing kinetic scalar. The two scalars need not be aligned;
`q=0` is a total contraction, not a rank-one condition on their source.

The Bianchi consistency identity

    div_g(Lambda K)_nu
      = sum_A div_g(Lambda grad psi_A) partial_nu psi_A
        +(Lambda/2)partial_nu q

is valid for both independent scalar fields and confirms conservation on
the constrained solutions. No separate conservation of each stress dyad
is needed for the theorem.

The review requested two precision corrections, now present in the reviewed
bytes: use the owner's open operand domain `|y|<2^-12`, and formulate the
Jacobi row multiplier as an identity of Euler covector densities before
stripping nonzero factors such as `2e` from the displayed equations.

## 3. Fixed-sector Jacobi transfer

The consumed density-rigidity theorem gives `delta x=delta y=0` for every
full native Jacobi field with the stated compact-support/fixed-collar
condition. Set

    delta Lambda=-(Lambda/e)delta e.

Then `delta(e Lambda)=0` and `delta q=0`. The variations of all native
coefficient functions `V_N'(r)r_x` and `V_N'(r)r_y` vanish pointwise.
Their spacetime derivatives therefore introduce no missing connection or
scalar rows. With the common coordinate volume, the full linearized
native Euler covector equals the nonzero factor
`a_N=eta^2 V_N'(r_*)r_x(x_*,y_*)` times the covariant one on these
perturbations.

Conversely a covariant Jacobi field in the fixed sector and already common
linearized volume gauge has `delta q=0` and `delta(e Lambda)=0`. The
linearized trace implies

    delta(eR)=-q_* delta(e Lambda)-e Lambda delta q=0.

Thus `delta x=delta y=0` and the same covector identity proves every
native Jacobi equation. This includes the independent connection rows.
There is no division by `q_*` or `R`, so the argument includes the
total-null sector used by the example.

This is a kernel correspondence on the stated common support/collar and
gauge. It does not prove equality of off-shell Hessians, energies, their
signatures, or symplectic structures. The nonlinear local volume-gauge
construction need not preserve an arbitrary old collar, and the proof
correctly refrains from claiming that it does.

## 4. Independent Bianchi-I derivation of the new metric

Use the example's coordinates and parameters `b>0,d>0`. Write its lapse
and spatial scale factors as

    N=sqrt(b) exp(db^2/4),
    a_1=b^(-1/2) exp(db^2/4),  a_2=a_3=b.

Let a dot denote the proper-time derivative `N^(-1)d/db`, and define

    s=db^2,       f=1/(bN)=b^(-3/2)exp(-db^2/4).

The actual Hubble rates and useful derivatives are

    H_1=(s-1)f/2,  H_2=H_3=f,
    Theta=(s+3)f/2,
    dot f=-(s+3)f^2/2,       dot s=2s f.

These imply

    dot H_1+H_1^2=f^2,
    dot H_2+H_2^2=dot H_3+H_3^2=-(s+1)f^2/2,
    dot H_1+Theta H_1=s f^2,
    dot H_2+Theta H_2=dot H_3+Theta H_3=0.

In the retained `(+---)` curvature convention, the diagonal Bianchi-I
identities are

    Ric_hat00=-sum_i(dot H_i+H_i^2),
    Ric_hatii=dot H_i+Theta H_i.

Consequently the full orthonormal Ricci tensor is

    Ric_hat=diag(s f^2,s f^2,0,0),  R=0.

Transforming back to the coordinate coframe gives exactly

    Ric=diag(d,d/b^2,0,0).

For `psi_1=b^2/2`, `psi_2=x`, and `Lambda=d/b^2`, this is precisely
`Lambda(dpsi_1 tensor dpsi_1+dpsi_2 tensor dpsi_2)` in every component.
The lapse equation is included in `Ric_hat00`; no lapse was frozen during
an ansatz variation to obtain it.

The magnetic Weyl tensor is zero for this diagonal homogeneous geometry.
With `R=0`, its electric components follow independently as

    C_hat0i0i=(dot H_i+H_i^2)
                 -(Ric_hatii-Ric_hat00)/2
              =(f^2,-f^2/2,-f^2/2).

Hence

    Ric_mu_nu Ric^mu_nu=2s^2 f^4
       =2d^2 exp(-db^2)/b^2,
    C_mu_nu_rho_sigma C^mu_nu_rho_sigma=8 sum_i C_hat0i0i^2
       =12 exp(-db^2)/b^6.

Both are strictly positive. The Riemann-square formula follows from
`Riemann^2=C^2+2 Ricci^2-R^2/3` and agrees with the example. This proves
that the witness is non-VSI and cannot be a coordinate rewriting of the
earlier VSI Brinkmann family.

## 5. Currents and native coordinate transport checked independently

The actual original volume is `e=b^2 exp(db^2/2)`. Direct multiplication
gives the two current densities

    e Lambda grad psi_1=(d,0,0,0),
    e Lambda grad psi_2=(0,-db,0,0).

Their coordinate divergences vanish. The gradients have opposite nonzero
norms, so their total contraction is zero while the combined tensor has
rank two. An orthogonal scalar rotation gives two independent null
covectors `(dpsi_1 +/- dpsi_2)/sqrt(2)` with the same source tensor.

For `J=d tau/db=(d/k_0)exp(db^2/2)`, the transformed volume and the
undensitized first scalar flux are

    e_native=e/J=k_0 b^2/d,
    e_native Lambda=k_0,
    g^(tau tau)partial_tau psi_1=(J/N^2)b=d/k_0.

The other undensitized scalar equation differentiates only in the `x`
direction, while its coefficient depends only on `b(tau)`, so it also
vanishes. Thus both native query values are zero and every field equation
of the same constant-query continuum source vanishes with its true
nonzero finite-cap factor. Omitting this coordinate transport would leave
`e Lambda=d exp(db^2/2)` nonconstant and would not establish the native
equations.

An independent temporary SymPy calculation computed the Hubble rates from
these lapse/scale-factor definitions and passed twelve exact identities:
the four Ricci components, scalar curvature, Ricci square, electric-Weyl
square, two current densities, native volume, native first scalar flux,
and native volume gauge. It used `PYTHONPATH=/tmp/d0_pydeps python3` and did
not import `examples_crossing_streams.py`, its Riemann calculation or its
saved outputs. The analytical derivation above is the reproducible review
argument; no historical all40/Lean or compiler run is claimed by this review.

## 6. Retained limits and correct consuming step

The new witness legitimately enlarges the configured continuum stationary
set beyond aligned null matter and VSI geometry. It retains the exact
native `k_0=-lambda_minus(2^-20)` and both original real scalar components.
The specific model, coefficient and volume-gauge substitution have been
checked rather than inferred from analogy to dust or a named theory.

This review accepts no transport to the original finite lattice, no
finite-mesh 42-row theorem for this metric, no absolute Book valuation,
no independent upstream preparation/clock stationarity, and no physical
minimum or universal metric-only GR source. The witness also retains
`R=0`; its nonzero Ricci/Weyl squares do not by themselves exclude every
higher-curvature Euler correction. Such corrections require their own
variation on this field. `GR_closed=false` remains appropriate.
