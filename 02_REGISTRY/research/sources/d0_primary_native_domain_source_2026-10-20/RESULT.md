# Primary nonvacuum family: strict native domain and actual Rayleigh source

Existing owner: Draft #334, `constitutive` / `native_sector`.
Phase: native realization, with a concrete consumer in the primary positive
nonvacuum family imported to main at `0bf309b6260cf5b63e54d6ccabdcdae6734b950a`.
Scientific source snapshot: `61a0b66f2e9512c7e3e64b2d9a0599231b0919fa`.
Integration snapshot: `25bea5bddd54988e32363c1968cdec8f6e4b7801`.

Reuse the exact full40+2 midpoint solution theorem. No geometric root,
Einstein tensor, new physical selector or alternative price is constructed.
The two missing applications addressed here are its map into the original
strict Julia domain, and the Rayleigh part of the unchanged native price
on the resulting SAME prepared family. Other complete-price terms remain.

Owned inputs, with exact source refs and bytes in SOURCE_PINS.json:
the original [all40 reduction](../../../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md),
the [primary midpoint recovery](../../A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md)
(its consumed source snapshot is preserved as inputs/primary_recovery.md),
the [local controlled J2](../../A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md),
the [full reference preparation](../../A4D_MICROHISTORY_EINSTEIN_QUOTIENT_AND_PRICE_EULER_UNIVERSALITY_2026_10_18.md),
the [original labelled source](../../A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md)
sections6.61,8.4-8.5, the [density dictionary](../../A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md),
the [strict coframe chart](../../A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md),
the [positive-adjoint native price](../../A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md)
and the [same-history paid-source identity](../../A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md).

## 1. Objects that cannot be identified by their shared notation

The primary star operator uses sampling legs v=he. The native full128
operator uses INVERSE coframe legs u_r=L_n eta (e^-1)_r^T and transported
creation X_r=C(u_r)Lambda(M_r), with P_r=X_r S_r. Its actual positive
adjoint gives D=ell^-1 sum_r(P_r-C_r)+adjoint. The original domain requires
||C_r||,||X_r||<1. Neither v=u nor D_raw=D_density-dressed is assumed.

The actual primary preparation is in the original ORTHONORMAL rest basis:

    m(Psi)=sqrt(p)|1>+psi_0|0>+psi_4|15>
             +sqrt(1-p-||Psi||^2)|14>,  p=phi^-1.

Here |1> is the timelike first grade, not a null basis vector. The owned
reference128 purification is C_(z,alpha),a=f_a(z)m_z,alpha/sqrt(128),
with 128 orthonormal real site characters and sum_a f_a(z)^2=128/S,
S=number of sites. Thus C*C=I128/128 and Tr C*C=1, including all columns.

Use the geometric owner's rational null-to-rest map

    T=[[1,1/2],[1,-1/2]] direct_sum I2,
    eta_rest=diag(1,-1,-1,-1),  T^T eta_rest T=eta_null.

Its determinant is -1 and its positive Gram is diag(2,1/2,1,1).
The configured star retains the null owner's INTERNAL orientation. In
rest coordinates its definition is the pullback
f_rest(e_r,U_r)=f_null(T^-1 e_r,T^-1 U_r T), with the transported
epsilon/Hodge convention. Replacing it by the canonical rest epsilon
would flip this pseudoscalar while leaving q unchanged, and would not
carry the owned lambda. Only the native positive CAR matrices are
computed in the rest basis; the configured price keeps this explicit
orientation pullback.
The SAME input in null coordinates is

    psi_0|0>+sqrt(p)(|1>/2+|2>)
      +slack(|13>/2-|14>)-psi_4|15>.

It must carry the exterior positive Gram, or its whitening. Reusing the
rest-mask formula as Euclidean null masks changes the clock and the state.
The checker performs all native operators directly in the rest basis.

For the actual density ratio rho_z=w_z/bar_w, the direct primary raw frame
is e_raw=rho_z^-1/2 T e_null(H). Its transverse inverse legs are
-sqrt(rho_z)e_x and -sqrt(rho_z)e_y. A direct unit-transverse substitution
therefore has ||C_r||=sqrt(rho_z). Uniform rho reaches the Julia boundary;
nonuniform positive ratios with average one include a value above it.
An observer change alone cannot fix a spacelike leg: its positive observer
norm is at least its absolute Lorentz norm. This is a TYPE mismatch, not
a failure of the positive geometric solution.

## 2. The owned scale repair has an exact configured-source transport

The coframe/heat owner already supplies the matrix repair F->sF,e->e/s.
What was missing is its transport of the primary source and preparation.
Fix ONE constant s=p^k across a predeclared bounded chart and every mesh.
Define

    Phi_s(e,U,Psi,rho,n)=(e/s,U,Psi/s^2,rho,n).

All original geometric h factors, density ratios, proper links, observer
and source conventions remain explicit. The star legs scale by 1/s;
the inverse native CAR legs scale by s. Quadratic star homogeneity and
the inverse metric in the original Clifford square give EXACTLY

    f_i o Phi_s=s^-2 f_i,       q_i o Phi_s=s^-2 q_i.        (1)

This includes inverse-PF factors and moving field/weight derivatives
under a fixed s. In the configured local source write
J_t=Jcal((t^2 f_i,t^2 q_i)_i), with every original AF/scene multiplicity
and complement retained. Then

    J_(s t) o Phi_s = J_t                                    (2)

OFF SHELL: every E_i,b_i,B_i=4b_i(1-b_i),Q_i,R_i and the configured
returned operator is identical. Its full source transports by the chain
rule, including delta t'=s delta t when this QUERY parameter varies.
This is not an identity of actual executed clocks or compiler work.

With t held at the SAME value on both sides, only on the common stratum
f_i=q_i=0 do the independent FIELD first covectors satisfy

    D_fields(J_t o Phi_s)=s^-2 D_fields J_t.                  (3)

Consequently all 16 coframe, 24 proper-link and two matter zero rows of
the primary family transport. In corresponding native coordinates their
rows scale by s^-1,s^-2,1 respectively. Do not extend (3) to higher
derivatives, variable nonzero baseline prefactors or separate preparations.
Off shell its exact identity is J_t o Phi_s=J_(t/s), not s^-2 J_t.

Let g denote the PRIMARY density-dressed metric e_null^T eta_null e_null.
Since the actual input frame is e_raw=rho^-1/2 T e_null, its scaled RAW
metric is g_raw'=rho^-1 s^-2 g. The already-owned density dictionary gives
hat_g'=rho g_raw'=s^-2 g, while Psi'=s^-2 Psi. The declared calibrated
dictionary is therefore

    g_read=s^2 hat_g'=s^2 rho g_raw',
    Psi_read=s^2 Psi'.                                     (4)

recovers the original finite-mesh primary representatives, with the
owned midpoint placements: metric sampling is exact on the polynomial
subfamily, while the matter representatives approach the same fixed
continuum waveform with the owned O(h^2) error. In the uncalibrated
density-dressed fields (hat_g',Psi') the apparent Einstein coefficient is
s^4 lambda; it is incorrect to retain lambda there without (4). No such
Einstein statement is made for the nonuniform raw metric g_raw'. Keep
the full scaled tetrad, not H/s^2 inserted into
a different canonical g_uv=1 frame. Fixed s preserves the owned O(h^2)
readout estimates and uniform inverse-map bounds.

## 3. Strict domain and the complete reference are retained

On the predeclared chart suppose the ACTUAL positive-observer matrix
budget B0=sup_(h,z,r) max(||C_r||,||X_r||) is finite. Choose the smallest
k>=0 with p^k B0<=p and fix s=p^k on that entire chart. This uses an
existing Golden power and a margin convention, not a coupling added to
the action or a selector of the physical execution. Then

    C_r'=s C_r, X_r'=s X_r, P_r'=s P_r,
    ||C_r'||,||X_r'||<=p<1,
    D'=sD, Delta'=s^2 Delta.                                (5)

The original ell, alpha=p^2 ell^2/128, epsilon=2alpha, number of attempts,
record alphabet128 and existing references are retained. In particular
the owned blank compression obeys

    B'=I-alpha Delta' >=(1-2p^4)I=3p^3 I>p^3 I.

A finite-mesh B0 alone gives a finite-mesh theorem. Uniform refinement
requires a uniform bounded coframe/link/observer/density chart; s(h)->0
is not substituted for it. The primary family permits bounded smooth
wave profiles and sufficiently small matter. First choose s on a larger
bounded chart, then require ||Psi_h||^2<=s^4(1-p-delta) for some delta>0.
This leaves a nonempty infinite-dimensional small-matter/wave family and
avoids choosing s circularly from the rescaled amplitudes. A strict
continuum margin accommodates the owned O(h^2) midpoint matter error.

Use the ACTUAL normalized m(Psi/s^2) and the same Fourier128 construction.
It preserves the full right Gram, fixed rest-clock amplitude and all
ambient grades. This is a compatible supplied preparation, not a free
operation on an arbitrary previous LEFT archive. Its physical synthesis,
oldRIGHT/AF binding and all work/Info/preparation sources remain to be paid.

## 4. A genuine extra source on these representatives: the original R

The unchanged native Rayleigh component in the positive matrix fiber is

    R_s=Tr C_s* Delta' C_s = ||D' C_s||_HS^2,
    C_s,(z,alpha),a=f_a(z)m(Psi_z/s^2)_alpha/sqrt(128).

It is not multiplied into the configured J2 by choice. It is the existing
R component if the original H+J+R price is used. At the rest observer and
fixed actual density, independently vary one original u-link in its proper
N_x or N_y direction, at a free interior site. Keep the actual C_s fixed
for this genuine independent link partial derivative. This does not
claim that its separate preparation Euler equation has already vanished.

Let N_x=E_(-,x)+E_(x,+), N_y similarly, and use
A_u=T exp(K_x N_x+K_y N_y) T^-1. In the REST CAR basis put
w=T e_-=(1/2,-1/2,0,0) and X(K)=C(w)Lambda(A_u). The exact full-CAR
derivatives on the only populated input grades, using the original
EXTERIOR_ORDER=(0,2,3,1), are

    X_x |1>=(|5>+|6>)/4,       X_y |1>=(|9>+|10>)/4,
    X_x*|14>=(-|9>+|10>)/4,    X_y*|14>=(|5>-|6>)/4.       (6)

They are four mutually orthogonal vectors of squared norm1/8. All other
populated input masks give zero for these derivatives. These derivatives
and their adjoints on m are independent of K, exactly, not just at K=0.
The complete nonlinear exterior Lorentz matrices and true positive
adjoints are used. Rest-mask/null-mask or inverse-adjoint substitutions
would change (6).

The projection Pi onto masks5,6,9,10 isolates all K-dependent output.
Changing H in the independent v-role creation has zero Pi-projection on
m; other role coefficients have no H dependence. Site characters and
nonuniform density can give additional baseline Pi-output, but it is
independent of H and K. Therefore the COMPLETE original R has exactly

    partial_(K_a,z) R_s = A_z K_a,z+b_a,z,
    A_z = s^2 rho_z (1-||Psi_z/s^2||^2)/(4 S ell^2)>0,       (7)
    partial_(K_b,z')partial_(K_a,z)R_s
          =A_z delta_ab delta_zz'.

The b term is retained and may depend on the actual density, complete
reference/site characters and preparation. No uniform prior or b=0 is
assumed. Equation (7) follows by applying the forward K derivative at z
and its true adjoint at z+u, summing all128 columns using their exact
local completeness. Clock p and slack 1-p-||Psi/s^2||^2 add to
1-||Psi/s^2||^2. Orthogonality in (6) eliminates all link cross terms.

## 5. Decisive test on the primary exact curved family

Fix its actual matter, density and observer and vary the permitted harmonic
wave coefficient A in W_A=W_0+A W_test, for instance W_test=x^2-y^2.
At EVERY A the original configured J2 all40+2 solution is the already-owned
primary one. Its independent Cartan links satisfy

    K_a,z(A)=K_a,z(0)+A V_a,z,
    V_a,z=[W_test(z+u)-W_test(z+u-a)]/2.

At a free interior site with V_a,z nonzero, the ACTUAL compactly supported
proper-link source of R obeys

    G_R,a,z(A1)-G_R,a,z(A0)=A_z(A1-A0)V_a,z !=0.            (8)

At least one of any two distinct A values has nonzero R link source;
max(|G_R(A0)|,|G_R(A1)|)>=|A_z(A1-A0)V|/2. The test direction changes
only that free link and keeps its original collar fixed. Varying A labels
different prescribed wave/boundary problems; (8) is NOT a comparison of
whole wave prices along a boundary-changing variation or a prospective
choice between different initial conditions.

Hence the configured source identity cannot simply be extended by declaring
the ORIGINAL R inert on this positive family. If a full price J2+R_s+E_s
is asserted stationary at these SAME points, it NECESSARILY satisfies

    partial_(K_a,z)E_s(A)=-G_R,a,z(A),
    difference of these E sources = -A_z(A1-A0)V_a,z.        (9)

This is a test of the actual missing H/Info/work/preparation completion,
not a correction to add or fit. A different actual preparation or stationary
elimination needs its own proved map. Equation (8) does not refute H+J+R
with its other actual sources, physical D0, the configured positive theorem
or all possible source-preserving transports. It supplies a specific
same-family source which that transport must carry.

No unproved continuum norm is substituted into (8). It is exact at each
mesh. If ell=h, the actual density has a uniform positive mass on a fixed
interior probe, and normalized Riemann sums converge, pairing (8) with
smooth supported link tangents delta K_h=h k gives its corresponding
nonzero continuum source difference. The original raw216 comparator and
actual physical normalization remain separate obligations.

The finite checker uses the actual n=20 F/R counts on L=4 (10946 words,
counts29..78), all256 sites, CAR16 and reference128. On its predeclared
chart the smallest admissible Golden exponent is k=3, s=p^3. The actual
largest Julia input norm is below0.451. At the free edge (1,1,2,2), two
wave amplitudes1/8 and1/4 give x-link source difference
-3.54115051413e-6; (7)-(8) give the same value. The independent direct
price finite differences agree with the analytic gradient to1.7e-14 and
Hessian to2.1e-12 in the recorded environment. This periodic storage
regulator supplies a fixed collar around the tested interior, where the
owned Cartan and midpoint source rows hold. Its polynomial wave is not
asserted to solve the periodic seam equations. The local Euler probe has
no seam support; no global periodic polynomial or full-price minimum is
inferred. Exact symbolic controls check the CAR vectors, nonzero off-shell
star homogeneity and the configured query/source scaling. The arbitrary
mesh statements above are analytic, not inferred from the one finite run.

## 6. What is now well typed, and what remains

The original full128 paid/channel source can now be evaluated on C_s,D'
inside its actual matrix domain. Its recycling map T_s is built from the
NEW Julia factors and defects sqrt(I-s^2XX*); generally T_s is not T.
Thus neither old protected-state coefficients nor s^2 times an old full
price can be substituted. Keep all original failure labels and use

    Cost_n=n+p epsilon sum_(r<n)Tr[rho_s (E_s*)^r Delta'],
    Q_s=Delta'-(ell^2/256)(Delta')^2,
    E_s=I+epsilon L_s,   L_s(rho)=T_s(D' rho D')-{Delta',rho}/2.

The physical Info algebra, actual operation generation/paid preparation,
executed registration clock versus Role u, complete H+J+R source and all
additional internal Euler rows are NOT supplied by (1)-(9). The preceding
terminal cap-error theorem also cannot make the nonzero successful R or
readout source disappear. This consumes the primary positive family and
turns its previously ambiguous normalization/price test into an explicit
matrix-domain map and necessary source equation. `GR_closed=false`.
