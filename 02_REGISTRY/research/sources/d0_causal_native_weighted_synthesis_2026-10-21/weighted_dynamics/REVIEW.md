# Independent mathematical review: actual weighted Ward and dust transport

21 October 2026. Reviewer: `clock_synthesis`, independently of the weighted
proof's author. Existing owner #334; source snapshot
`086fab99d8aaed7f712e9a3d2858c516b61901fc`.

**Verdict: PASS in the stated local continuum domain, together with the
stated exact finite-source substitution.** No mathematical blocker remains.
The continuum Ward identity, the arbitrary prescribed-weight dust
construction, the original/reduced metric distinction, and the coupled
fixed-collar Jacobi comparison are valid. Neither finite-lattice Ward
rigidity nor compulsory physical Book valuation follows from this review.

## 1. Reviewed bytes and the one clarification

| Artifact | SHA256 |
| --- | --- |
| `WEIGHTED_WARD_AND_DUST.md` | `dfb7ef92acbf21ea2154d9d197e9884c59ddc13fdfa912d293403696c283e01d` |
| `check_weighted_ward.py` | `34eac4356cae034429aab0b4807db1cdc8506f3017b92025b3815cf70ec14582` |
| `SOURCE_PINS.json` | `5c5a582e2016a04b7d65f24ec8ec9d5caccbcda4377f4dc52a19d718ad93cd94` |
| `RESULT.json` | `7c94a1213ee6064c0cf3c86cbb7ec6dbb24d9332cca8ec5b9bbb00bf95297e2b` |

The first proof read had SHA256
`e0b67c3535744585e697bd3a715c46233287738db9e24666d1ddd130b55dd9a6`.
With the parent's authorization, the reviewer added only the clarification
before equation (26): at a general finite stationary point, its coefficient
is `k_z=K'(tau q_tilde,z/rho_z)` evaluated at that point. The earlier
`K'(tau q0/rho_z)` specialization is available only after constant q has
independently been established. No equation, scientific premise, checker
or result receipt was changed.

All six consumed source files were independently checked against BOTH their
SHA256 hashes and git blob IDs at the pinned commit. Their current repository
bytes also matched those pins during review. The original constitutive
normal form, its actual N=1 law/readiness constants, the old density-rigidity
proof, and the declared original coframe/difference and collar conventions
were read for this comparison.

## 2. The weighted Ward identity and invariant

I rederived the variation with rho fixed. Since f is a weight-one density
and q is an undensitized scalar,

    delta x = xi.dx + x div(xi) + x xi.dlog(rho),
    delta y = xi.dy + y xi.dlog(rho).

The integration by parts gives exactly

    delta S = M integral xi.[rho d(F-xF_x)+y F_y d rho].

In particular the sign and coefficient of the extra weight term in (5)
are correct. No variation of rho, coordinate measure, or external baseline
has been used. These Lie variations are admissible field directions; the
argument does not require the action to have diffeomorphism symmetry.

The independent local coframe scale gives `xF_x-yF_y=0`: holding omega
independent is essential, and introduces no derivatives of the scale into
f. On the regular trace branch, with `m=F_x`, `n=F_y`, and `chi m=y n`,

    d_y(F-chi m)=n(1-y m'/m).

Combining this with (5) gives exactly `d(rho y/m)=0`. This derivation divides
by m and n, which are nonzero on the declared chart, but never divides by
y. It therefore applies through the null branch. It does not imply that
the original operands x and y are constant when rho varies.

## 3. The actual auxiliary map and full reduced equations

The auxiliary equations in (8) are precisely those of the pinned actual
weighted constitutive owner. Differentiating its K while using both
auxiliary equations cancels the s' and P' terms and gives

    K'(t)=U(t)F_y(s(t),U(t)t),

including the required factor U. The same scale satisfies
`f_tilde=U f`, `q_tilde=q/U`, and `e_tilde=U^2 e` in four dimensions.
Consequently `rho y/m=(tau/a)q_tilde`, which proves the stated reduced
material-norm rigidity. This uses stationary auxiliary equivalence, not
an off-shell equality of the two physical-only actions.

I independently varied (9). The constant-coefficient Palatini connection
equation is torsion-free for the reduced coframe. The metric equation is
`a e_tilde G+K' sum dpsi tensor dpsi=0`, and the material equation is
`partial_mu(K' g_tilde^(mu nu) partial_nu psi_A)=0`. The absence of an
additional material pressure term follows from the undensitized material
measure. The six antisymmetric coframe rows are accounted for by internal
Lorentz invariance and the connection equations; no ansatz precedes the
field variation.

The independent reduced Lie identity (14) is exact even when rho varies.
The alternative Bianchi argument also works: the divergence of
`(K'/e_tilde) sum dpsi tensor dpsi` is
`K'/(2e_tilde) d q_tilde` after the full scalar-current equations are used.
All rho derivatives are included in those currents.

## 4. Arbitrary prescribed rho, dust, and the indispensable shift

For one timelike scalar, equations (15)--(17) yield positive irrotational
dust because `a<0`, `K'>0`, and `q0>0`. A unit gradient is geodesic, and
the scalar equation is exactly dust-current conservation with the
prescribed mass-coordinate law `e_tilde varrho=H_rho`.

For the converse, a regular proper-time/comoving source chart has mass
volume `C(X)dT d^3X` by dust conservation. The implicit construction (18)
preserves T and has positive full Jacobian `H_rho/C`. Pulling back both
the source geometry and its dust fields therefore gives the required
mass-volume density exactly. The target rho is not adjusted. A relatively
compact box and sufficiently small q0 ensure one common operand chart;
shrinking the local coordinate patch ensures the implicit map exists.

Time dependence of X^1 is essential. I checked the FLRW example directly:
`g_tilde^(TT)=1`, `g_tilde^(xT)=-k' x/k`, and its scalar current cancels as
`partial_T K'-K' k'/k=0` because k is proportional to K'. Dropping this
shift loses an actual current term. The construction is a way to produce
a solution for the fixed target coefficient, not a physical gauge
symmetry of that coefficient.

The null extension is also valid locally. A positive mass-volume form
can be flattened while preserving a regular null coordinate T, without
needing a timelike comoving chart. At q=0, U=1 and K'=b for every rho;
the scalar current follows from the supplied null-dust conservation and
the prescribed constant mass-volume density. Collars must be transported
as stated; no global or arbitrary-boundary existence theorem follows.

## 5. Original connection, conformal formula, and sign

The distinction between the original affine connection and LC(g) is
correct and essential. From `e_tilde=sqrt(U)e`,

    D_omega e = -(dl/2) wedge e,
    Gamma_tilde = Gamma(e,omega) + (dl/2) I.

As matrix-valued connection forms their curvature difference is
`d(dl/2) I=0`. This compares Gamma(e,omega) with LC(g_tilde), and does not
compare LC(g) with LC(g_tilde). Applying the four-dimensional conformal
Einstein formula with `g_tilde=exp(l)g` gives precisely every sign in (21).
The matter coefficient agrees because
`K'/(a e_tilde)=F_y/(e F_x)`.

For the actual reflected native law, the positive raw first derivatives,
negative raw mixed/xx derivatives, and entropy derivatives imply
`F_xx(0)>0`, `F_xy(0)<0`. With `a<0<b`, the formula in (22) gives
`U'(0)>0`. On a sufficiently small chart, a nonnull constant-q_tilde
branch has zero original-coframe torsion only if d rho=0. The proof
therefore does not silently identify its reduced dust metric with the
original operational metric. On the null branch this distinction does
disappear because U=1.

## 6. Coupled Jacobi comparison and its collar hypothesis

At a stationary background, the two actions have the same full first
differential. The only Hessian difference is the rank-one-in-material-norm
form displayed in (23), with the actual spatial factor `K''/rho`.

Differentiating (14) gives `d(delta q_tilde)=0` for a full Jacobi vector:
the derivative of the Lie test direction multiplies DS=0, and the
coefficient derivative multiplies d q_tilde=0. A compactly supported
variation or fixed collar on a connected domain forces this constant
delta q_tilde to vanish. The affine comparison has the same Ward identity
with its actual frozen coefficient k_rho, so the reverse inclusion follows
by the same argument. Equation (24) is therefore valid for the full coupled
fixed-collar kernel.

Without that collar/support hypothesis a constant variation of q need not
vanish, so this argument would not identify the kernels. The proof does
not claim equality of off-shell Hessians, inertia, frozen-metric scalar
propagators, different caps, or a constant J2 slope. The stationary
auxiliary map and observable map must be transported, as stated.

## 7. Exact finite consequence and explicit remaining step

Equation (25) is an exact chain rule for the already-owned finite normal
form. At a configuration having constant q_tilde=q0, it is exactly the
affine weighted source with `k_z=K'(tau q0/rho_z)`. Thus an affine full root
with those q-values is a nonlinear full root, without a continuum Ward
assumption. The independent-link equation and material adjoint use the
original dictionary; no additional material link term is introduced.

For a general finite stationary point, (26) uses the actual state-dependent
k_z and is a direct substitution of the two DEFINED stencil defects into
(25). It does not make either defect vanish. Proving small defects with
the actual nonzero gain and correct collar is still required to infer
refinement rigidity. No discrete Lie identity, constant-q theorem for all
finite roots, finite representative of every continuum dust geometry, or
finite Jacobi-kernel equality has been certified here.

## 8. Narrow replay and retained limits

I audited the new checker's explicit actual N=1 polynomial, its reflected
source signs, the auxiliary Newton derivative, and its shifted-current
test. I ran only `check_weighted_ward.py` once. Its **42 checks passed**,
and its complete independently generated JSON was byte-identical to the
pinned `RESULT.json`.

Reported diagnostics include weighted Ward residual `2e-99`, invariant
error `2.2e-86`, and a nonzero `-5.413279...e-9` current residual when the
induced shift is omitted. These are 90-digit Decimal diagnostics, not
interval certificates and not replacements for the analytic proof.
No old-root, finite all42, continuum source-replay, or broad suite was run.

The accepted positive advance is the extension of the exact continuum
stationary reduction to arbitrary actual positive PF profiles, including
a constructive local dust class and its determined original observables.
The declared continuum density dictionary, finite/refinement defect bounds,
actual metric readout, query admission, complete Book valuation, and genuine
upstream stationarity retain their stated independent scopes.
`GR_closed=false`.
