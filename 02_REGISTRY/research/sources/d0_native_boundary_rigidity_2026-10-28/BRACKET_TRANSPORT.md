# Full-source to endpoint-bracket transport, with the actual Golden inverse scale

Research notes for the existing D0 scientific owner #334, 28 October 2026.
This note supplies a quantitative application to the concurrently derived
two-endpoint feedback generating function. It does not supply a physical
local-lapse family, identify endpoint coordinates with ADM coordinates, or
assert GR closure.

## 1. Exact endpoint carrier and the complete price

Let `x,y` be real local coordinates on a **genuinely admitted** pair of
endpoint-cut charts, of the same dimension `d`, and let

    S(x,y) = S_fb(x,y) + S_rest(x,y)
    K = D_x D_y S.

Here `S_fb=-log det(I-z P0(I-P1)P0)`, with `P1=U* P0 U`, is the original feedback term; `S_rest`
retains the actual heat, preparation, clock, retained information and any
other separately present physical terms. The decomposition must not count
any term twice. No smallness of `S_rest` is assumed by the notation.

The discrete boundary forms are

    theta_minus = -D_x S dx,
    theta_plus  =  D_y S dy,
    dS = theta_plus - theta_minus.

Consequently

    Omega_S = -d theta_plus = -d theta_minus
            = -sum_ij K_ij dx_i wedge dy_j.

This form is closed. It is nondegenerate exactly when `K` is invertible;
its least singular value, in the declared product Euclidean chart norm,
is `sigma_min(K)`. The discrete left Legendre map

    (x,y) |-> (x,p=-D_x S)

is locally invertible under the same condition. Pulling back the canonical
bracket with `{x_i,p_j}=delta_ij` gives the **explicit** endpoint bracket

    {A,B}_S
      = (D_y A)^T K^(-1) D_x B
        - (D_x A)^T K^(-T) D_y B.                    (1)

Equivalently its Poisson matrix is

    Pi_S = [ 0       -K^(-T) ]
           [ K^(-1)    0    ],
    ||Pi_S|| = 1/sigma_min(K).                       (2)

For verification of the sign in (1), the inverse differential of the
left Legendre map is

    [ I                 0       ]
    [ -K^(-1) S_xx     -K^(-1)  ].

Conjugating the standard Poisson matrix by this map yields (2), since
`S_xx` is symmetric. Another globally consistent sign convention changes
the sign of every bracket and none of the bounds below.

The nondegeneracy is on this specified endpoint-pair chart. The constraint
`P1=U* P0 U` for a fixed physical `U`, a common initial state, or other native
constraints can restrict the tangent image. One must restrict/reduce the
actual form on that image before claiming a physical phase space. An
invertible form on an artificially enlarged pair does not prove that step.

## 2. Original Golden conditioning and the complete-price perturbation

The concurrent endpoint calculation gives, on `Gr(r,2r)` at its original
Golden pair and with Hilbert--Schmidt tangent norm,

    K_fb(X,Y) = -kappa_H <H_X,H_Y> - kappa_A <A_X,A_Y>,
    H_X=(X+X*)/2, A_X=(X-X*)/2,
    kappa_H = 2z[1-(2-z)p^2]/(1-zp^2)^2,
    kappa_A = 2z/(1-zp^2),       p=phi^(-1).

For `0<z<1`, the smaller singular value is

    mu_fb = kappa_H > 2z(sqrt(5)-2).                 (3)

At the repository's `z0=2^(-20)`, direct evaluation gives

    mu_fb = 4.5026495696419226e-7,
    ||Pi_fb|| = 2.22091456271052e6,
    kappa_A/kappa_H = 4.236059897853796.

These decimal values are diagnostic evaluations of the analytic formula;
the strict analytic bound (3), not floating-point rounding, supports the
inequalities.

The displayed mu_fb is its value AT THE GOLDEN BASE. For estimates on a
whole required chart choose a proved positive lower bound
`mu <= inf sigma_min(K_fb)` on that chart. At the base one may take
`mu=mu_fb`; continuity gives a sufficiently small neighborhood with
`mu=mu_fb/2`, but supplies no explicit radius or refinement-uniform bound.

Put `E=D_xD_y S_rest`, with all terms expressed in the same physical
endpoint coordinates and norm. If, on that same required chart,

    ||E|| <= eta mu,        0 <= eta < 1,             (4)

then the full price supplies a nondegenerate endpoint form and

    sigma_min(K) >= (1-eta) mu,
    ||Pi_S|| <= 1/[(1-eta)mu],
    ||Pi_S-Pi_fb||
       <= ||E||/[mu^2(1-eta)].                      (5)

Proof: `||Kv|| >= ||K_fb v||-||Ev||`; the inverse difference is
`K^(-1)-K_fb^(-1)=-K^(-1)E K_fb^(-1)`. The same singular-value estimates
apply to the block Poisson matrices in (2).

If `S_rest=f(x)+g(y)`, then `E=0` exactly and the symplectic form is
unchanged, although its endpoint covectors change. This is the useful exact
case; source neutrality of a general remainder must not be confused with
vanishing mixed Hessian.

The actual base `mu_fb=O(z)` matters: small unnormalized source errors or small
price errors alone do not imply small brackets. To keep the same inverse
scale one needs a mixed-Hessian error strictly smaller than the established `mu`.
For a normalized asymptotic comparison with vanishing relative form error
one needs `||E||/mu -> 0`, hence `o(z)` when a uniform `mu` comparable to `z`
has been proved and `z` varies to zero. A fixed physical `z0` instead has
the pointwise explicit budget and the separately bounded neighborhood (4).

### Transport to actual field coordinates: rank alone does not suffice

For a proved field-to-endpoint map `F:y -> (x,y_endpoint)` with Jacobian
`J`, the pulled-back source and boundary form are exactly

    f_field = J^T f_endpoint,
    Omega_field = J^T Omega_endpoint J.              (5a)

When `J` is square and invertible,

    sigma_min(Omega_field)
      >= sigma_min(Omega_endpoint) sigma_min(J)^2.

For a rectangular `J`, full column rank is **insufficient**. In canonical
four-dimensional phase space, the full-rank inclusion of the two position
coordinates has zero pulled-back symplectic form. Odd-dimensional physical
images are necessarily degenerate. Write `J=UR` with orthonormal columns
in `U`; the correct sufficient condition is that the **restricted** matrix
`U^T Omega_endpoint U` is nondegenerate. Then

    sigma_min(Omega_field)
      >= sigma_min(J)^2 sigma_min(U^T Omega_endpoint U). (5b)

Any remaining null directions require a justified physical constraint/
gauge reduction; adding conjugate variables by declaration does not prove
that reduction. With the same true map on both sides, endpoint source
error `eps` gives field source error at most `||J|| eps`, while the
two-form error is at most `||J||^2 delta`. If the compared maps differ,
their actual Jacobian difference contributes independently. For example,

    ||J^T f-J0^T f0||
      <= ||J|| ||f-f0|| + ||J-J0|| ||f0||.

The native field norm and the symplectic restriction must therefore be
controlled together; a rank42 source map alone cannot establish an
inverse physical boundary form.

## 3. A complete-source bracket estimate

Let `Pi_0` be the reference Poisson tensor on the same chart, and let
`Pi` be the actual full-price tensor. Suppose

    ||Pi|| <= P,
    ||Pi-Pi_0|| <= Delta_P.

For two **actual generator functions** `A,B`, compare their complete
covectors to reference covectors `f_0=dA_0`, `g_0=dB_0`:

    f=dA=f_0+e_A,     g=dB=g_0+e_B,
    ||f_0||<=M_A,    ||g_0||<=M_B,
    ||e_A||<=eps_A,  ||e_B||<=eps_B.

Then

    |{A,B}_Pi - {A_0,B_0}_Pi0|
      <= Delta_P M_A M_B
         + P(eps_A M_B + M_A eps_B + eps_A eps_B).    (6)

This follows by inserting `f=f_0+e_A`, `g=g_0+e_B` into `f^T Pi g` and
using the operator norm on each term. It is independent of the number of
cut coordinates when the stated norms and constants are uniform.

Combining (5) and (6) is an immediate concrete application to the original
Golden feedback carrier. It supplies the missing normalization in any
claim that small full-source residuals imply small deformation brackets:
the inverse-form coefficient is approximately `2.22e6` at `z0`, before
any field-to-cut differential or chart-conditioning factors are applied.
The net error also contains the actual generator-source sizes in (6);
if those scale with `z`, some inverse factors can cancel. It would be
incorrect to infer the net amplification without retaining those sizes.

Only C0 control of the **complete first covectors** is needed for bracket
*values*, provided the inverse symplectic form is controlled. C0 control of
the action values is insufficient. The exact moving-cut Book derivative
from `A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md` is applicable to
the relevant covectors only after a physical generator and its variation
map into `(U,P,Delta)` have been identified. A single scalar `B` does not
automatically define the family `H[N]` for arbitrary local lapses.

## 4. Actual gains and the tangential-generator calibration

Let, on one justified common chart,

    Omega_phys = c_h Omega_hat,
    dH_phys[N] = a_h(f_N+e_N),
    D_phys[xi] = b_h D_hat[xi],

with nonzero **field-independent** physical normalizations. The normal
bracket is scaled by `a_h^2/c_h`, while the tangential generator is scaled
by `b_h`. Thus the relative clock/constraint normalization is

    r_h = a_h^2/(c_h b_h).                            (7)

It must be derived; no redefinition to one is automatic. If the reference
law is `{H_0[N],H_0[M]}=D_0[v_0]`, then the normalized native defect is

    E_HDA = b_h^(-1){H_phys[N],H_phys[M]}_phys
            - b_h^(-1)D_phys[v_h].

When (6) bounds the normalized normal bracket by `E_br`, and
`|D_hat[v_h]-D_0[v_0]|<=E_D`, it follows that

    |E_HDA| <= |r_h| E_br
               + |r_h-1| |D_0[v_0]| + E_D.           (8)

A field-dependent gain must be treated with the full differentiated
formula: `d(aH)=a dH+H da`. Such terms cannot be discarded by invoking (7).

There is a genuine additional issue if only the **source** of `D` is
known. On a star-shaped chart of path-radius `L`, a uniform fixed-smearing
bound

    ||d(D_hat[xi]-D_0[xi])|| <= eps_D ||xi||

and an actual base-point calibration

    |D_hat[xi](x_*)-D_0[xi](x_*)| <= delta_D ||xi||

give the value bound

    |D_hat[xi]-D_0[xi]| <= (delta_D+L eps_D)||xi||.    (9)

The base-point term cannot be inferred from sources: adding a constant
linear functional of `xi` leaves every fixed-smearing source unchanged
but can leave a nonzero strong-algebra defect.

For the state-dependent geometric shift `v(x)=q^(-1)(N dM-M dN)`, and a
generator linear in its smearing,

    d(D[v(x)]) = (d_x D[xi])_(xi=v(x)) + D[dv(x)].    (10)

The second term is required when controlling derivatives of the HDA
defect. A calculation that differentiates only the frozen-shift source
does not establish the full vector-field/constraint transport. A metric
readout error also contributes through `v_h-v_0` in (8).

## 5. Stronger derivative control for Hamiltonian commutators

For clarity take a reference Darboux chart with constant symplectic matrix
`W_0`, `||W_0^(-1)||<=kappa`, and an actual normalized closed matrix
`W=W_0+E`. Assume

    ||E||<=delta_0,    ||DE||<=delta_1,
    kappa delta_0<1,
    P=kappa/(1-kappa delta_0),
    Delta_P=kappa^2 delta_0/(1-kappa delta_0).

Inverse differentiation gives

    ||D Pi|| <= P^2 delta_1.                         (11)

For unit lapse profiles assume uniform reference and error bounds

    ||f_0||,||g_0|| <= M_0,
    ||Df_0||,||Dg_0|| <= M_1,
    ||e_A||,||e_B|| <= eps_0,
    ||De_A||,||De_B|| <= eps_1.

Writing `B=f^T Pi g`, `B_0=f_0^T Pi_0 g_0`, the value error is

    E_0 = Delta_P M_0^2
           + P(2M_0 eps_0+eps_0^2).

The derivative error satisfies

    ||dB-dB_0|| <= E_1,
    E_1 = 2P[(M_0+eps_0)eps_1+M_1 eps_0]
           + 2M_0 M_1 Delta_P
           + P^2 delta_1(M_0+eps_0)^2.              (12)

To prove (12), differentiate the three factors. Each of the two terms
where a source is differentiated is bounded by
`P eps_1(M_0+eps_0)+Delta_P M_1M_0+P M_1 eps_0`;
the middle Poisson-derivative term is bounded using (11).

The Hamiltonian vector-field difference therefore obeys

    ||X_B-X_B0|| <= P E_1+2kappa M_0M_1 Delta_P,      (13)

in the same sign convention. This is a sufficient quantitative bridge to
commutators of Hamiltonian vector fields. To apply it to (8), also control
the complete derivative of the tangential term, including (10), and all
normalization derivatives if the gains are not constant.

### Exact negative controls showing why these hypotheses matter

On one canonical plane with `{q,p}=1`, put `K=p`.

* `H_n=n^(-1) sin(n^2 q)` converges uniformly to zero, but
  `{H_n,K}=n cos(n^2q)` is unbounded. Action-value convergence alone gives
  no bracket convergence.
* `H_n=n^(-3) sin(n^2 q)` has both `||H_n||<=n^(-3)` and
  `||dH_n||<=n^(-1)`. Its bracket value is `n^(-1)cos(n^2q)` and does
  converge uniformly to zero, while its derivative is
  `-n sin(n^2q)dq`. At `q=pi/(2n^2)` this derivative is exactly `-n dq`.
  Thus even convergent first covectors do not imply convergence of the
  induced bracket vector fields without the stronger derivative bounds.
* With `Omega_n=n^(-3)Omega_0`, `H_n=q/n`, `K_n=p/n`, both sources
  converge to zero but their native bracket is `n`. This is the need for
  the inverse-form and actual-gain factors, not a failure of (6).

These are direct symbolic identities, not empirical extrapolations.

## 6. Concrete use of the newest formalization result

At #402 commit `5007f1707932629613d4b846482b8cd8cae9a4a3`,
`D0.Algebra.MovingProjectorTransport` supplies the exact noncommutative
algebra used by the root source formula:

    [[dP,P],P]=dP,
    d((I-P)UP)-[K,(I-P)UP]=(I-P)(dU-[K,U])P.

Its proof does not supply a differentiable native family or the thermal
and logdet derivatives. Those remain the analytic source inputs.

The same #402 snapshot contains the compiled theorem
`archive_doubling_fixed_component_errors` in
`D0.Geometry.ArchiveGradedRefinementComposedReadout`. The literal adjacent
graded pullbacks compose as exact cochain maps, yet at size doubling a
constant one-form component becomes `2` on the original prefix and `0`
on the appended tail. Its normalized fixed-component L1 and L2-squared
errors are exactly `1` at every level.

This result has a specific consumer here: **exact chain compatibility
cannot establish the vanishing readout/source error hypotheses of
(6), (12), or the metric-shift error in (8).** A proof of the actual smooth
test/readout transport is required. The theorem does not rule out a
different justified physical readout, independent refined field solutions,
or a separately controlled limit.

The resulting usable chain is:

1. Use the original complete moving-cut price to obtain actual endpoint
   covectors and mixed Hessian on the admitted endpoint chart.
2. Apply (3)--(5) to establish the full boundary symplectic conditioning.
3. Derive actual locally smeared normal and tangential generators of that
   same process; retain its lapse, clock and tangential calibration.
4. Apply (6)--(13), together with a proved physical field/readout map,
   to transport their finite brackets and, where needed, vector fields.
5. Only after native HDA and the stated local canonical class hold, apply
   the already proved 28 October Einstein--scalar classification.

Steps 1--2 now have a concrete original-feedback seed; steps 3 and the
physical map/limit in step 4 are not supplied by merely writing ADM
variables or by the generic stability estimate. No new decoder, scalar
counterterm or replacement native action is used.

There is a separate exact composition obligation. A one-step feedback
function cannot be summed over ticks without proving the full price's
composition law. Already for an original rank-one rotation,

    f(theta)=-log(1-z sin(theta)^2),

two executed rotations have the actual return price `f(2theta)`, whereas
the symmetric stationary composition of two separately assigned one-step
functions yields `2f(theta)`. At the Golden angle and the original small
`z0`, `f''(theta)>0` but `f''(2theta)<0`; even the local curvature sign
cannot be transferred through the unproved additive identification.
The exact whole-tape price, its gluing/boundary law and the genuine local
generators must be derived together. Equations (6)--(13) transport an
established common structure; they do not create this missing gluing law.
