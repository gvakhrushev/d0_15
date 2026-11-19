# Original retained memory: an exact nonlocal gate-only source test

Input: `gvakhrushev/d0_15`, PR #334,
`172876cdf38bfce6f87fdd4a059d524b60c10eb9`.

This consumes the original G/SourceI execution grammar, the INTERNAL
scene-stage incidence realization in primary source §§7bh/7bi/7bw, the full
spectral Hessian and the retained determinant sewing. Its consumer is the
proposed inference from bounded primitive arity and widely separated paid
stages to a local reduced action. We disprove that inference on an explicit
four-word family, while retaining all clocks, cuts and thermal modes.

This is not a no-go for spatially local dynamics with a retained memory state,
nor for a proved continuum reduction on a smooth field chart. The two varied
blocks address the SAME memory. Neither their clock separation nor their
three-wire arity establishes disjoint spatial support. No physical metric or
mesh map is inferred from N. Native syntactic membership does not select the
physical X_N or one compulsory task equivalence class.

## 1. Four literal equal-inventory words

Use exactly the owned gates on a port and quaternion spin:

    p=(sqrt(5)-1)/2, a=sqrt(p),
    G=[[a,-p],[p,a]] tensor I_spin,
    X=SourceI=diag(I_4,L_i), X^4=I,
    Z=X^2=diag(I_4,-I_4), ZGZ=G^{-1}.

Let M+ be the chronological word X X X X G, and M- the chronological
word X X G X X. Each consists of one G and four X. Its endpoint is G or
G^{-1}, respectively. No inverse primitive, arbitrary angle or free idle is
used. For an integer L>=1 set

    W_(sigma,tau)= M_sigma X^(4L) M_tau X^(4L),
    N=10+8L,                 sigma,tau in {+1,-1}.

Both padding blocks are actually executed; the four words have exactly two
G, 8+8L SourceI, the same complete carrier, same duration and same cut.
Equal inventory is not an assertion that separate complete programme-description
costs or any additional physical Info have equal values or derivatives.
On all input columns their endpoints are

    U_(sigma,tau)=G^(sigma+tau).

The smallest checker includes an unknown oldRIGHT bit: four qubits, only
the port blank, spin unrestricted, oldRIGHT immutable. Thus internal dimension
d=16 and true input rank r=8. Taking no oldRIGHT instead gives d=8,r=4;
an actually present further protected factor multiplies d and r honestly.

For P_in=|0><0|_port tensor I_spin tensor I_oldRIGHT, all microscopic outputs
remain and the original complementary cut is Q=I-P_in. Put

    A=sin^2(2theta)=4p^3=4sqrt(5)-8,   sin(theta)=p.

The original return, without a substitute report function, is

    F_++=F_--=A P_in,    F_+-=F_-+=0,
    J_++=J_--=-r log(1-z A),   J_+-=J_-+=0.

Consequently its exact four-corner difference is

    C_J=J_++-J_+--J_-++J_--=-2r log(1-z A)>0.       (1)

It is independent of L. At z=2^-20, C_J/(r z) is about 1.88854467.
In general C_J/(r z)>=2A=8p^3>0. No small-z normalization erases it.
Here r z is the actual return response scale for this fixture, not an
identified geometric gain Gamma_h. A proposed field map must retain its
own Gamma_h and norm in addition.

## 2. The full paid scene-stage heat cannot cancel (1)

Apply the existing DECLARED INTERNAL incidence realization: g_t=I_scene
tensor u_t, S=K(9,11,13), all 33 scene vertices and 359 edges, with

    R=(D_S+2I)^(-1/2), B=R A_S R,
    Delta_0=I-B-R(T_g+T_g*)R,
    Z_0=Tr exp(-beta Delta_0),
    Z_01=2 Z_0+359 N d,    H_j=beta^-1 log Z_j.

The actual same-carrier completion is U_hist=T_g^N on C0 and identity on
C1; P_hist is stage0 tensor one fixed scene ray tensor P_in, zero on C1.
This is the already owned §7bh interface, not a new selection of Delta_N.
All n0=33Nd and n1=392Nd modes remain. For Book03's different fixed default
tensor heat, H is independent of these internal words and the contrast is
exactly (1); that default is not identified with the incidence operator.

The actual prefix frame reduces the INTERNAL word to a single closing
holonomy U without changing B,R. Let M_U=I-Delta_0(U). The existing positive
incidence bound 0<=Delta_0<=2I gives ||M_U||<=1. For k<N,

    Tr M_U^k=Tr M_I^k.                                  (2)

Proof: every matrix product contributing to this trace is a closed path
in the stage cycle with possible scene moves. Dependence on the closing
holonomy requires a nonzero winding. It requires at least N temporal moves,
and hence at least N factors. An unwound path has U and U^{-1} cancelling;
scene factors commute with U. This proof needs INTERNAL placement at every
base stage, not just endpoint equality.

For all k, |Tr M_U^k-Tr M_I^k|<=2n0. Therefore the ENTIRE trace satisfies

    |Z_0(U)-Z_0(I)| <=2n0 e^-beta t_N(beta),
    t_N(beta)=sum_(k>=N) beta^k/k!.

Since Z_0>=n0 e^(-2beta), the mean-value inequality for log yields

    |H_0(U)-H_0(I)| <=(2 e^beta/beta) t_N(beta).        (3)

The same bound holds for H_01: trace differences double, while its positive
lower bound is at least twice the one just used. The index 359Nd is retained
inside the logarithm and only improves the bound. No truncation of a trace,
counterterm or unmatched-clock subtraction is used.

At the owned beta=2p^2, 1/2<beta<1 and e^beta<3. For N>=2,

    t_N(beta) <= (N+1)/(N N!),
    |H_j(U)-H_j(I)| < 12 (N+1)/(N N!).                 (4)

U_++ and U_-- are inverse holonomies, whose heat traces are equal by
clock reversal/complex conjugation. U_+-=U_-+=I. Thus

    C_B=C_J+2[H_j(G^2)-H_j(I)],
    |C_B-C_J| < 24 (N+1)/(N N!).                       (5)

For d=16,r=8,z=2^-20 and EVERY L>=1 (N>=18), exact rational arithmetic
from (4)-(5) proves

    C_B/(r z)>179/100.                                (6)

In fact at N=18 the error bound divided by r z is <5.2e-10, and it
decreases with N. At fixed beta,z and actual fixed carrier factors,

    lim_(L->infinity) C_B/(r z)=-2 log(1-z A)/z>=8p^3.

The clocks really become longer; their absolute heat and its N-dependence
are retained. The limit concerns this four-corner comparison at each common N,
not equality of actions at different N or a physical continuum limit.
No factorial statement is made if beta grows with N.

## 3. Optional local differential test at actual native base

The finite-code result above does not require a continuously variable gate.
For the structural full-matrix chart only, replace the existing G matrix in
the first block by exp(sJ)G and that in the second by exp(tJ)G, with
J=[[0,-1],[1,0]] tensor I. The stage count is unchanged. At the actual
++ native base the endpoint is G^2 exp((s+t)J). Consequently

    partial_s partial_t J = r f''(2theta),
    f(alpha)=-log(1-z sin^2 alpha),
    f''(alpha)=2z cos(2alpha)/(1-z sin^2 alpha)
       +z^2 sin^2(2alpha)/(1-z sin^2 alpha)^2.         (7)

At z=2^-20 this is negative, nonzero and independent of L. A uniform
heat-Hessian bound follows without a commuting-variation shortcut.
The closed-path expansion has nonnegative scalar coefficients and
Tr U(alpha)^w=d cos(w alpha). A path of k factors has |w|<=k/N.
The absolute coefficient sum is Tr M_I^k<=n0. Hence, writing

    T_m(N)=sum_(k>=N) (k/N)^m/k!,

the full H0 or H01 satisfies, for 1/2<beta<1,

    |d^2 H_j(U(alpha))/d alpha^2| <=6 T_2+18 T_1^2,
    T_1<=N/[(N-1)N!],
    T_2<=N^2/[(N^2-N-1)N!].                            (8)

The bounds use Z>=n0 e^-2beta and the full logarithm's -(Z'/Z)^2 term;
both grades again obey the same bound. At N>=18 the bound is <1.1e-15,
whereas |r f''(2theta)| is about 1.36e-5 for r=8. This is a genuine
full-Hessian countercheck on the matrix extension of the native base;
it is NOT proof that exp(sJ) is a primitive or an admitted physical
continuous variation.

## 4. Exact implication for the final composition

Consider any purported gate-only price whose terms each depend on a clock
window of at most R consecutive raw positions, plus functions of sigma alone
or tau alone. Choose L so both clock gaps between the five-stage variable
blocks exceed R. Then no term sees both sigma and tau, so its four-corner
difference is exactly zero. Equation (6) excludes equality to the original
B, and excludes an approximation whose total four-corner error, divided by
r z, tends to zero. A uniform value error epsilon_N per word would require
4 epsilon_N>=|C_B|. No assumption about differentiating a compiler enters.

This applies after ELIMINATING the retained intermediate state. A local
description with x_(t+1)=g_t x_t and a complete terminal price can of course
retain the interaction through x. Its elimination produces (1), which is
precisely why an associative operator Schur calculation is not a proof of a
local metric-only action. That enlarged local state still needs the actual
physical reduction, admissible normal generator and spatial readout required
by the HDA consumer. Temporal range alone proves none of these.

The four words have different terminal returns and are not claimed to be
equivalent solutions of one compulsory future task; no D_min selection is
inferred. Their role is an exact witness against a claimed structural
implication for the same defined root functional. A legitimate restriction
that excludes these interventions would need its own native task/variation
proof, not their silent deletion. Separate selected costs and variable cut,
scene, beta,z or preparation would require their actual derivatives; none is
silently identified with the fixed-data comparison here. `GR_closed=false`.

## Verification scope

The companion checker imports and pins the ORIGINAL native grammar, computes
all16 columns for all four words at L=1,2,4, validates identical inventories,
the immutable oldRIGHT and original rank8 cut, and verifies the full return
matrices in the Golden number field. Exact rational bounds certify (6) and
the heat-Hessian budget. No numerical diagonalization of the enormous full
Hodge matrix is claimed; the all-mode trace is bounded analytically by (2)-(8).
This does not rerun the original full42 or original CAR128 solver, Lean or CI.
