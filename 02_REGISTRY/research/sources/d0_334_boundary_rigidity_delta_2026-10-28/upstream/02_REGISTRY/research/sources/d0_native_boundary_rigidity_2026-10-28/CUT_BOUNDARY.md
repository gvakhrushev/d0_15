# Actual Golden return: endpoint twist and full-history canonical relation

Bounded research subtask for existing PR #334. Input c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a. Derivations below use the original return F=P U†(I-P)U P and the owned moving-cut source. They do not insert ADM variables or claim physical admission of arbitrary endpoint variations.

## 1. Exact rewriting as a pair of actual cuts

Define P0=P and P1=U† P U. Then

F=P0(I-P1)P0,
S_fb(P0,P1)=-log det[I-z P0(I-P1)P0], 0<z<1.

These are operators already in the original formula. No decoder, scalar target or new physical action is introduced. P1 is the pulled-back final measuring cut. The complete bootstrap is still B=H(Delta)+S_fb, H=beta^-1 log Tr exp(-beta Delta). An actual variation obeys

dP1=U† dP0 U+[P1,U†dU].

Therefore treating P0,P1 as independent is a chart on the freely varied operator family; surjectivity of that chart on the actual admitted execution is a separate application premise. It must not be inferred from matrix dimensions.

## 2. Exact mixed Hessian at the original Golden pair, every rank

Let p=phi^-1, c=sqrt(p), s=p, c²+s²=1. Work on the original equal-rank Golden block C^(2r), with P0 frame [I;0] and P1 frame [cI;-sI], exactly U_phi†P0U_phi. Use actual orthonormal Grassmann charts

A(X)=[I;X](I+X†X)^-1/2,
B(Y)=([cI;-sI]+[sI;cI]Y)(I+Y†Y)^-1/2,
P0(X)=A(X)A(X)†, P1(Y)=B(Y)B(Y)†.

X,Y are arbitrary complex r×r matrices; each endpoint chart has real dimension d=2r². Set K=A†B, a=1-zs². Restricted to im P0,

I-zF=(1-z)I+z K K†.

At X=Y=0,

K=cI, K_X=-sX†, K_Y=sY, K_XY=cX†Y,
M_X=-zcs(X+X†), M_Y=zcs(Y+Y†),
M_XY=z[c²(X†Y+Y†X)-s²(X†Y†+YX)], M=aI.

The exact second derivative of -logdet M is

S_XY=-a^-1 Tr M_XY+a^-2 Tr(M_X M_Y)
 =-2z/a [c² ReTr(X†Y)-s² ReTr(XY)]
  -z²c²s²/a² Tr[(X+X†)(Y+Y†)].

Write X=H_X+A_X with H_X†=H_X and A_X†=-A_X, and similarly Y. With real Hilbert-Schmidt pairing <X,Y>=ReTr X†Y, Hermitian and anti-Hermitian parts are orthogonal. Thus

S_XY=-k_H <H_X,H_Y>-k_A <A_X,A_Y>,

k_H=2z[1-(2-z)s²]/(1-zs²)²,
k_A=2z/(1-zs²).

For the actual Golden value s²=p²<1/2,

0<2z(sqrt(5)-2)<k_H<k_A,  0<z<1.

The strict lower inequality follows from 1-2p²=sqrt(5)-2 and z>0. The comparison k_A-k_H=4z(1-z)p²/(1-zp²)²>0. In a real orthonormal HS basis the mixed Hessian has r² copies of -k_H and r² copies of -k_A. For real Gr(r,2r), replace the Hermitian/skew-Hermitian dimensions by r(r+1)/2 and r(r-1)/2; rank one then has only the H mode.

This is an exact Hessian at a finite original Golden angle. It does not take theta or z to zero, and no rank-dependent loss appears in the HS norm.

## 3. Genuine local boundary two-form, with its true gain

Put theta_minus=-D_1 S_fb dX and theta_plus=D_2 S_fb dY. Then dS_fb=theta_plus-theta_minus and dtheta_plus=dtheta_minus. Hence

Omega_fb=-dtheta_plus=-dtheta_minus
         =-sum (S_fb)_(X^a Y^b) dX^a wedge dY^b.

At the Golden pair its matrix has off-diagonal blocks diag(k_H I,k_A I) and their negative transposes. It is nondegenerate on the freely supplied endpoint-pair chart. Its smallest singular value is k_H, so

||Omega_fb^-1||=1/k_H.

Continuity provides a local symplectic neighborhood. Equivalently, the two discrete Legendre transforms from the pair chart to T*Gr are local diffeomorphisms by the ordinary inverse function theorem. This constructs the actual original feedback's finite boundary generating structure; it does not identify its endpoint momentum with a preexisting observed physical momentum.

At the already-used #334 calibration z0=2^-20 (not selected by this theorem):

k_H=4.502649569641923e-7,
k_A=1.907349327604880e-6,
||Omega_fb^-1||=2.22091456271052e6,
condition number=k_A/k_H=4.236059897853796.

The conditioning after dividing by z is bounded, but the absolute inverse carries 1/z. A putative continuum bracket error must retain this actual gain. Erasing z by a mathematical normalization changes the clock/bracket normalization unless an admitted physical calibration proves it.

## 4. Heat, moving Gram and actual admission are retained, not frozen

For a genuinely supplied execution chart (X,Y,zeta), the unchanged original B has mixed block

K_B=D_XD_Y B=K_fb+K_heat.

Here K_heat includes the FULL pullback of H(Delta(X,Y,zeta)). If the actual selected execution separately has further price terms c, call its price S_exec=B+sum c and its mixed block K_full=D_XD_Y S_exec=K_B+K_other. For the defined master alone K_other=0. Controller, memory, clock or preparation dependence that is already inside B is not charged again; genuinely separate prices are neither invented nor discarded. When Delta is an independent spectator coordinate, H contributes no X-Y mixed derivative in that independent coordinate chart; this is not a statement that the actual native field-to-Delta map has zero derivative.

At the Golden base, if an actual bound ||K_heat+K_other|| <= eta k_H with 0<=eta<1 is proved, then sigma_min(K_full)>=(1-eta)k_H and ||Omega_full^-1||<=1/[(1-eta)k_H]. This is a sufficient, testable same-source condition, not a selected physical assumption. On a whole neighborhood replace k_H by a proved uniform lower bound mu for sigma_min(K_fb). Continuity gives some smaller neighborhood with, for example, mu=k_H/2; no explicit neighborhood radius or refinement-uniform lower bound is asserted here.

If the admitted endpoint map j has smaller dimension or rank, j*Omega_full can be degenerate. The symplectic chart theorem on freely supplied endpoint cuts does not prove rank of j or a reduced q_ij/pi^ij phase space. In particular it supplies no normal generator H[N], arbitrary lapse family, or HDA by itself.

## 5. Original Golden gluing defect: the global return is not the sum of its steps

On the actual real rank-one two-port block let P(theta) denote a rotated rank-one cut. The original feedback for angle difference delta is

f(delta)=-log(1-z sin² delta).

Let theta be the original Golden angle, sin² theta=p². The same two consecutive Golden gates have sin²(2theta)=4p³. Therefore

f(2theta)-2f(theta)
 =log[(1-zp²)²/(1-4zp³)]>0

for every 0<z<1: the numerator minus denominator is 2zp²(2p-1)+z²p⁴>0. This is an exact return-sector structural control. It does not change the complete stage/archive cut into a two-port-only cut.

The defect already affects the boundary form. The stationary intermediate-cut composition near the symmetric split gives

G(delta)=stationary_x [f(x)+f(delta-x)]=2f(delta/2)

locally at delta=2theta, because f''(theta)>0 makes the symmetric interior stationary point nondegenerate. Consequently

G''(2theta)=f''(theta)/2=k_H/2>0.

The original composed return instead has

f''(2theta)=2z[1-(2-z)4p³]/(1-4zp³)²,

which is NEGATIVE at z=2^-20 (and for 0<z<2-1/(4p³)). Thus its mixed endpoint Hessian is opposite in sign to that of G. Their difference is not an endpoint coboundary a(X)+b(Y), whose mixed derivative vanishes.

Conclusion: the positive single-return twist cannot license composing native histories by summing separate return actions. The actual cumulative unitary, retained history and terminal price must remain in the gluing law.

## 6. Exact full-history cotangent relation, without adding physical states

Let x_k be the complete retained state in a real smooth chart, including every archive/controller/clock component genuinely retained by the fixed finite execution. Write its actual deterministic update as x_(k+1)=Phi_k(x_k,a_k); a_k are only genuinely admitted controls. Let the actual total scalar price be B_N(x_N)+sum c_k(x_k,a_k). A history-dependent terminal can always be represented in the already retained history state, but a smaller Markov state cannot be silently substituted.

Introduce mathematical multiplier covectors lambda_(k+1) for the actual transition equations. The constrained functional is

A=B_N(x_N)+sum[c_k+lambda_(k+1)·(Phi_k-x_(k+1))].

Variation gives exact backward equations

lambda_N=dB_N,
lambda_k=d_x c_k+(D_x Phi_k)^T lambda_(k+1),
E_(a_k)=d_a c_k+(D_a Phi_k)^T lambda_(k+1).

Every independently admitted control equation E_(a_k)=0 is retained. These are the usual finite chain rule/adjoint identities, not a new action or physical force law. In particular dB_N is the owned moving-cut full source, including dP,dU,dDelta, moving Gram and other declared independent endpoint quantities.

When Phi_k is locally invertible in the full retained chart, its exact cost-shifted cotangent lift satisfies

x_+=Phi(x), lambda=d c+(D Phi)^T lambda_+,
lambda dx-Psi*(lambda_+ dx_+)=d c.

Taking exterior derivatives proves preservation of the canonical boundary 2-form. A noninvertible discarded-state update gives a canonical relation rather than a symplectomorphism; retaining an archive may restore the invertible full update, but one must use that actual update. The terminal condition lambda_N=dB_N defines a Lagrangian graph, since d(dB_N)=0. This graph is not the whole phase space and does not on its own supply a Poisson bracket on geometric fields.

For the original root, using independent real-Frobenius operator coordinates gives

g_Delta=-rho_beta,
g_U=2z C R,
g_P=z(A+A†), A=[R C†,U],

where C=(I-P)UP and R=(I-z C†C)^-1. Thus dB=ReTr(g_Delta†dDelta+g_U†dU+g_P†dP), restricted to genuine tangent directions. The equivalent Kato formula retains the same moving-cut source. The body-frame momentum paired with U†dU is the anti-Hermitian projection of 2z U†C R; subsequent actual word factors transport it by the corresponding coadjoint pullbacks.

These displayed operator gradients keep beta and z fixed. If beta or z is
independently varied in the actual chart, the already-owned full source adds

    g_beta=-log(Z)/beta²-Tr(rho Delta)/beta,
    g_z=Tr(R F),  Z=Tr exp(-beta Delta).

Their terms g_beta d beta and g_z dz, and any actual separate terminal
payment derivative, belong in lambda_N. The mixed heat formula in section 8
and the reported numerical controls have fixed beta,z scope. A map with
moving beta or z must include their complete chain-rule mixed derivatives.

This derives a finite source-consistent mathematical boundary relation for the unchanged history. What remains is physical identification and reduction to the HKT phase space, actual lapse generators and the strong bracket limit. The derived covectors are response/adjoint variables until native physical momentum readout and variations bind them.

## 7. Reused owners and scope change

- `A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md`: the existing constrained operator family and full first feedback variation. Its complementary Q=I-P is not the second endpoint P1=U^dagger P U used here. The present result adds the endpoint mixed Hessian and its nondegeneracy; it does not reclassify that owner's admitted physical tangents.
- `A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md`: exact full first source.
- `A4D_ROOT_CUT_TO_REFOLIATION_CLOSURE_2026_10_28.md`: conditional HKT class and explicit missing native boundary/HDA interface.
- `A4D_BOOK_INFO_ENDPOINT_COHOMOLOGY_FULL_GRAVITY_QUOTIENT_2026_10_19.md`: actual Info allocation differs by an endpoint exact form; it cannot repair the mixed-Hessian gluing defect and does not change a proved boundary 2-form.
- `CANONICAL_GENERATOR_AND_PRICE_INTERFACE.md`: prior toral generator/source cotangent transport, whose physical field/Book binding remains open.
- `A4D_NATIVE_TIME_FIELD_INTERTWINER.md`: the simple native toral-time readout cannot supply general coupled fields through a regular first jet.

New positive content: the unchanged return itself, at the actual Golden gate and every equal block rank, has an exact nondegenerate endpoint mixed Hessian with explicit gain. New boundary: its canonical composition differs from actual cumulative-return pricing already in the rank-one original block. No claim that GR is closed, no generic rejection of a history-aware or continuum route.

## 8. The full heat mixed source and a dimension-free norm bound

For the actual pulled-back self-adjoint Delta(X,Y,zeta) at fixed beta>0,

D_XD_Y H=-Tr(rho Delta_XY)+beta Cov_BKM,rho(Delta_X,Delta_Y),

Cov_BKM,rho(A,B)=integral_0^1 Tr[rho^(1-s)(A-<A>)rho^s(B-<B>)]ds,
<A>=Tr rho A.

Proof: the Duhamel derivative of normalized rho is
D rho[B]=-beta integral_0^1 rho^(1-s)(B-<B>)rho^s ds.
Differentiate D_X H=-Tr rho Delta_X and retain the genuine Delta_XY term. No commutation hypothesis is used. In a rho eigenbasis the BKM kernel is the logarithmic mean L(r_i,r_j); L<= (r_i+r_j)/2 implies Cov_BKM(A,A)<=Var_rho(A), while positive logarithmic means give positivity. Cauchy-Schwarz therefore yields

|Cov_BKM(A,B)|<=sqrt(Var_rho(A)Var_rho(B))<=||A||op ||B||op.

Consequently

|D_XD_Y H|<=||Delta_XY||op+beta||Delta_X||op||Delta_Y||op.

Taking the supremum over unit endpoint graph tangents gives an actual mixed-operator norm budget. The spectral term need not be O(z); it can dominate the small feedback gain unless the native map proves the required bound. It also need not be positive on mixed X-Y directions, although the ambient Delta-only Hessian is positive semidefinite. This is why positivity of H cannot replace the full mixed-block calculation.

The executed NumPy control `check_full_boundary_source.py` uses genuinely noncommuting 3,4,6,8-dimensional matrices and Delta(t,s)=Delta0+tA+sB+tsC. Mixed fourth-order finite differences of the actual logTr exponential agree with the formula within 3.87e-11. Omitting either the Delta_XY or BKM term creates a nonzero defect in each control. Full moving-P/U/Delta first-source checks agree within 5.19e-13. Five actual unitary word-slot derivatives match the complete endpoint adjoint within 1.67e-13, and fixed-endpoint internal frame variations telescope with source residual 1.01e-16. These are finite structural controls, not a replay of an original full42 or continuum physical family.

### Norm conversion

The stated k_H is for graph coordinates ||X||F. The actual projector tangent has ||dP||F=sqrt(2)||X||F. If the endpoint product norm is defined using the projector matrices rather than their graph coordinates, sigma_min(Omega_fb)=k_H/2 and the inverse norm is 2/k_H. No dimension-dependent loss occurs, but the normalization factor must be stated before applying a bracket estimate.
