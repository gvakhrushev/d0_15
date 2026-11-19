# v8: record-generated heat and a shared H + J_program + R critical point

SOURCE #310. Scientific input: `681a631c3a0f0c8e262d49074561ecc21b67aa9e`.
14 October 2026. RESEARCH, not physical admission, a CORE claim, or GR closure.

## 1. Removed assumption and retained assumptions

The heat generator is no longer independently supplied once the particular
instrument below is fixed. Its positive heat factor, the actual program feedback,
and the quadratic matter reading are computed from the same Dirac operator.
The resulting full functional has a certified finite critical point and a
periodic refining family. This is stronger than a feedback-only critical point.

Inputs still include a positive finite carrier, four isometric returns, CAR
creators and their positive geometric pairing, a length calibration, controlled
operation/blank resources, and the stated preparation and fugacity. Their physical
selection from M1 is NOT proved. The program is not identified with the old
state-conditioned two-tick chronology. Apparatus registers are geometric
spectators in the tested full action; v6/v7 are still required for an active bath.

Consumed input: v2 `FORCING_FROM_RECORDS_RU.md`, sections 1 and 4, under
`02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/v2_snapshot/d0_research_v2/`;
`D0.Representation.GoldenOrderInterferometer.gate`; v1 `MATTER_BRIDGE_RU.md`,
sections 4-9. Linear-combination-of-unitaries methods are prior art, not claimed
as a D0 invention: Childs and Wiebe, arXiv:1202.5822.

## 2. A structural block encoding, including noncommuting geometry

Let p=phi^-1, a=sqrt(p), p+p^2=1. On the entire finite carrier set

    d=ell^-1 sum_r c_r(T_r-I), D=d+d*, Delta=D^2.

At unit pairing beta_r=c_r+c_r* and zeta_r=c_r-c_r* are unitary. The literal
v2 expansion of ell D has five coefficients (1/2,1/2,1/2,-1/2,-1) per role.
Duplicate the last term and use six SIGNED words per role:

    beta_r T_r, zeta_r T_r, T_r* beta_r, -T_r* zeta_r, -beta_r, -beta_r.

Append four I and four -I. The sum of these 32 unitary words is 2 ell D.
Preparing a uniform 32-label register, applying SELECT, and unpreparing gives

    Q=(H32/sqrt32) SELECT(V_j) (H32/sqrt32),
    <0|Q|0>=sum_j V_j/32=ell D/16.

No spectral decomposition, eigenstate catalogue, commuting-return condition,
or commuting-creator condition is used. The full curvature terms in D^2 stay.

For local positive geometry 0<G(x)<I, beta_r^2=u_r(x)^2 I,
zeta_r*=-zeta_r, zeta_r^2=-u_r(x)^2 I, u_r=sqrt(G_rr).
Their coefficients need not commute with shifts. Introduce ONE coefficient
qubit and the pointwise scalar s_r=sqrt(1-u_r^2). The full matrices

    BetaHat_r=[[beta_r,s_r],[s_r,-beta_r]],
    ZetaHat_r=[[zeta_r,s_r],[s_r,zeta_r]]

are unitary. Extend T_r by identity on that qubit. Use the same 32 signed words
with Hats and the same uniform label preparation. Compress BOTH label and
coefficient qubit to zero. The result is still A=ell D/16, now including
noncommuting local coefficients. In particular BetaHat T compresses to beta T,
not to sqrt(u) T sqrt(u). Differentiation includes the actual derivative of s_r.
The exact checker rejects that symmetric-sandwich shortcut and a frozen s_r jet.

This uses scalar local square roots, not sqrt(Delta) or a spectral oracle.
The coherent controls, reflection and preparation are explicit circuit resources;
v5 gives conditional approximate G/CNOT implementation, not a physical admission
or an exact finite native compilation of every field-dependent coefficient.

## 3. The golden port produces a positive survival block

On the full 64*dim(H) carrier let P select zero label and coefficient qubit.
Set W=Q*(I-2P)Q. Thus W*=W and W^2=I. The literal golden comparator between
I and W has ports K0=pI+p^2W and K1=ap(W-I). Their full effects sum to I.
Keeping the port record and all coefficient/label registers gives survival block

    B=P K0 P|im(P)=I-2p^2 A*A=I-alpha Delta,
    alpha=p^2 ell^2/128,  p^3 I <= B <= I.                       (1)

The remaining 127 output blocks are retained; their effects sum to I-B^2.
This is a registered event, not a deterministic nonlinear evolution by B.

n rounds use fresh workspace without resetting old records. The compression
of their actual unitary product on the original all-blank workspace is B^n.
For a trace input its all-blank probability is Tr(B^(2n))/dim(H). Therefore

    Lambda_alpha=-log(B)/alpha, beta=2n alpha,
    exp(-beta Lambda_alpha)=B^(2n)                              (2)

exactly. Lambda is the unique selfadjoint logarithm of this positive B. This
uniqueness does not assert that M1 selects the circuit. Beta encodes an integer
record count; no physical continuous clock is inserted. For field variations
ell, p and n are fixed. Lambda differs from Delta at finite ell. The matter
reading below remains <Delta>, NOT <Lambda> chosen to match the heat.

## 4. All three price terms on one complete carrier

Let b=128 be the retained purifying-reference dimension and Wdim=128^n the
workspace dimension. On H tensor C^b tensor workspace define the tested class

    L_full=Lambda_alpha tensor I_b tensor I_workspace,
    D_matter=Delta tensor I_b tensor I_workspace,
    P_full=I_H tensor I_b tensor |blank><blank|.

The explicit identity action on apparatus is a substantive hypothesis, not a
derivation of archive invisibility. No all-data/active-apparatus claim follows.
For the actual U_n, F=P_full U_n*(I-P_full)U_n P_full has active block
(I-B^(2n)) tensor I_b and vanishes on the full complementary input space. Hence

    H_full=beta^-1 log[b Wdim Tr_H B^(2n)],
    J_program=-b Tr_H log[(1-z)I+z B^(2n)],
    R=<Psi,D_matter Psi>, ||Psi||=1, S=H_full+J_program+R.       (3)

Reference multiplicity b in J is retained. All workspace heat multiplicities
are retained; their logarithm has zero field derivative only for this fixed
experiment. The feedback is generally NONZERO and is not frozen or replaced by
a one-frame square. It is NOT the historic state-conditioned chronological J.

## 5. Actual source, including noncommuting first variations

Variation on the full matter sphere gives D_matter Psi=epsilon Psi. At such
a point, with reduced rho_m, tau=B^(2n)/Tr(B^(2n)), and arbitrary Hermitian
X=delta Delta, cyclic trace differentiation of (3) gives

    dS[X]=Tr{[rho_m-tau B^-1
       +b beta z B^(2n-1)((1-z)I+zB^(2n))^-1]X}.               (4)

No [X,Delta]=0 premise is required. For an arbitrary moving preparation add
Tr(delta rho_m Delta); it vanishes on the sphere only at the stated eigenstate.
This does not erase v3's preparation term for an arbitrary prescribed preparation.

The exact matrix logarithm derivative is

    D Lambda[X]=integral_0^infty (B+tI)^-1 X (B+tI)^-1 dt,
    ||D Lambda|| <= p^-3.                                     (5)

The bound follows by integrating (p^3+t)^-2. It is independent of carrier size
and mesh. All operator/coefficient/return derivatives enter through the proven
block identity (1), rather than a frozen field-to-instrument substitution.

## 6. Certified finite common root, with the full feedback multiplicity

On the untwisted periodic Hodge carrier H=C^(L^4) tensor C^16 put
z_r(k)=L(exp(2pi i k_r/L)-1), lambda_k=z(k)*G z(k).
Take the whole first positive shell +/-e_r with weights 1/8 and Fock I16/16.
Its full pure realization uses the 128-dimensional reference, as in v1. Its
physical preparation from pi0 is not asserted. Fix, before solving:

    L=8, ell=1/8, n=128 L^2=8192,
    alpha=p^2/8192, beta=2p^2, z=2^-20, b=128.

z is a diagnostic value of the existing parameter, not a derived physical
constant. It is not legitimate to claim a root for an arbitrary native z.
Let G=(d-o)I+o 11^T, A_k=sum|z_r|^2, C_k=|sum z_r|^2-A_k,
s_k=1-alpha(d A_k+o C_k), e_k=s_k^(2n), Z=sum e_k,
r_k=z e_k/(1-z+z e_k), lambda1=128-64sqrt(2). Equation (4) is equivalent to

    sum_k [(e_k/Z-2048 beta r_k)/s_k] A_k=lambda1,
    sum_k [(e_k/Z-2048 beta r_k)/s_k] C_k=0.                   (6)

2048=16*128, not 16. All ten metric coefficients reduce to these two by the
permutation symmetry of their actual full value; no transverse equations are
silently dropped. Both dropping J and dropping the reference fail the checker.

An outward-rounded contraction maps the radius-10^-12 rectangle about

    d=0.063635191594344535042829697433316630182693569761541,
    o=0.0040167350432317252873844519148251220686807163526359

strictly into itself, with derivative infinity norm <10^-6. Banach gives a
unique root IN THIS RECTANGLE. All 4096 modes are grouped into 119 exact
Q(sqrt2) feature pairs with integer multiplicities. d-o>.059, d+3o>.075, G<I,
and every other positive Delta mode is separated from the chosen shell by >.5.
The full prepared Psi is an eigenvector, so all sphere directions, including
reference/workspace directions, have zero first variation. It is not asserted
to be a stable minimum.

### Local metric and linear-link rows

Use the translation-covariant variable-field Hodge extension with its true
moving adjoint. At the homogeneous point the reduced densities and operator
are translation invariant. Thus each local metric row is the homogeneous row
/ L^4, and all ten vanish at every site. For arbitrary local linear exterior
K use the full v1 identity Tr(a_i c_r Gamma(K))=4(G_ir trK-(GK)_ir).
The link coefficients are linear combinations of sum_k c_k Re(z_i* z_r) and
sum_k c_k Re(z_i*)=-sum_k c_k |z_i|^2/(2L), where c_k are the weights in (4).
Both vanish by (6); sum_k c_k=0 is not needed. This proves all 64 local linear
rows of the algebraic Hodge extension, hence its isometric subdirections.
Arbitrary GL-link variations are NOT thereby physically admitted or compiled
into the unitary circuit. The affine shift sector is not included. These
boundaries separate algebraic source completeness from native tangent admission.

## 7. A refining family, not numerical extrapolation from L=8

For n_L=128L^2, beta stays exactly 2p^2. On bounded frequencies Lambda tends
to Delta; this is not a full UV operator-norm convergence. On a compact positive
G neighbourhood, lambda_k>=16c sum dist(k_r,L Z)^2, Lambda>=lambda and
s_k^-1<=p^-3. Polynomial-Gaussian bounds therefore dominate the full source
maps and their first derivatives uniformly.

At G=dI in the limit put a=4 beta pi^2 d, K=sum k_r^2. The offdiagonal equation
is zero by coordinate reflections. The diagonal equation becomes

    F(a)=E_a K-2048 beta sum_{k in Z^4}
            [z exp(-aK)/(1-z+z exp(-aK))] K-1=0.               (7)

The certificate includes the infinite tails beyond [-8,8]^4: a one-dimensional
moment tail is bounded by 2*9^(2j)*exp(-1.80*81) divided by
1-(10/9)^(2j)*exp(-1.80*19). Union bounds and Z1<3, M2,M4<10 bound the
four-dimensional tails. Outward intervals give F(1.80)>0, F(1.82)<0 and
F'(a)<-.67 throughout. The feedback correction to the offdiagonal Jacobian
is <.005 times its strictly negative thermal part, since
2048 beta z Z/(1-z)<.005. The mixed entry is zero by reflection symmetry.

The invertible two-variable Jacobian and C1 convergence imply a joint critical
point for each sufficiently large L (also L in 4N), at the SAME fixed z=2^-20.
The first-shell gap persists by the low-mode limit and uniform high-mode bound.
This is an analytic implicit-function argument, not a finite census. The family
is flat and periodic; it is not an ArchiveProjection/AF refinement or Einstein
limit. J and workspace heat have growing field-independent constants, so no
convergence of the full price values is claimed.

A necessary adverse parameter gate is also explicit. On an allowed radial
Delta ray with R>0, denominator<=1 shows that 16 b beta z>=1 prevents
stationarity. In particular z=1/2 fails. The small test z proves nonemptiness
of a parameterized class, not its physical selection.

## 8. Exact boundary of the advance

The circuit now supplies its generator, genuine source, actual program feedback
and a shared critical family. It does not supply M1 admission, physical ell/z,
pi0 placement, an identification with the old matter-conditioned J, active-bath
action, native AF/field refinement, physical Ward, curved roots, or GR. Inserting
a phase in an arbitrary return does not establish the native pi0 seam; the
untwisted critical point is not silently a phase-twisted solution.

Run `python verify.py` and `python hostile.py`. Receipts are immutable unless
`--write` is explicitly requested. No new Lean result is claimed. Factor
identities verify the huge full workspace without pretending to execute it.
