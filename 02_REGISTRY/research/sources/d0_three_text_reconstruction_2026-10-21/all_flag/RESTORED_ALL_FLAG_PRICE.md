# Reconstructed full-flag Julia/CAR16 measurement and resource theorem

21 October 2026. New reconstruction from the supplied text and extant original
owners at `8ba0bd929499e639b0fe4640ffa448631f3b024b`. This is not recovery of the
bytes of `3bf6ca63759f0aa58441152e0e98962fa662920a`: that object was unavailable
in the inspected repository. No historical test count or publication status
is adopted. The accompanying checker is newly written and separately run.

## 1. The exact existing detector and the declared complete execution

The detector is the one in
`A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md`,
sections 1–3 and 5, not a newly selected frame. Its real null basis has
`eta_(+-)=eta_(-+)=1`, `eta_22=eta_33=-1`, rest observer
`n=(1/sqrt(2),1/sqrt(2),0,0)` and positive Hilbert metric
`-eta+2(eta n)(eta n)^T=I`. The ordered original Lie basis is

    G=(N2,N3,Nbar2,Nbar3,J,B),
    Na=E_(-,a)+E_(a,+), Nbara=E_(+,a)+E_(a,-),
    J=E_23-E_32, B=E_(--)-E_(++).

It satisfies `Tr(G_a^T G_b)=2 delta_ab` and `Tr G_a=0`. All16 exterior
grades remain in the CAR space. The fixed prepared vector is

    Omega=(1/2) sum_mu |1<<mu>_CAR16 |mu>_freshR4,
    f_a=sqrt(2)(G_a tensor I)Omega,
    v_(a,eps)=(Omega+eps f_a)/sqrt(2),
    E_(a,eps)=|v_(a,eps)><v_(a,eps)|/12, eps=+1,-1,
    E_rest=I-|Omega><Omega|/2-sum_a |f_a><f_a|/12.

The f_a are orthonormal and orthogonal to Omega. Thus E_rest has eigenvalues
1/2 on Omega, 11/12 on the six signatures and 1 on their complement. These
are exactly thirteen effects on CAR16 times freshR4. OldRIGHT/reference128
are fixed tensor spectators; this is not a replacement of either by R4.

Fix positive numbers e_j with sum e_j=1, j=1,...,n, and let
`X=sum_a x_a G_a`, `U_j(X)=exp(e_j X)`. These are substeps of ONE net
holonomy exp X; n is not a spatial refinement parameter. Each substep uses
the original full-CAR contraction and positive-Hilbert Julia dilation

    T_j=Lambda(U_j)/2,
    D_j=(I-T_j^T T_j)^(1/2),
    J(T_j)=[[T_j,(I-T_j T_j^T)^(1/2)],[D_j,-T_j^T]].

Each flag starts fresh, is retained, and never controls an active gate.
The active data continue through every substep, including failure branches.
For each full flag string b in {good,bad}^n the data amplitude is
`K_b=F_n ... F_1`, with F_j=T_j or D_j. Read the same thirteen-effect
detector after every flag string, retaining all fine output states too.
There are 13*2^n positive pointer probabilities at the flat point. This is
a mathematical full execution in the owner's generous active-orthogonal
class; literal G0 admission and physical prices are not inferred.

For sufficiently small X each full16 contraction is strict. For example,
`||X||<=1/10` gives `||Lambda(exp(e_jX))/2||<=exp(0.4)/2<1`.
At every fixed finite n all pointer probabilities stay positive on some
neighbourhood of zero, so the following ordinary score calculation is
regular. No uniform neighbourhood in n is claimed.

## 2. Exact arbitrary-partition first jet

Let R(X)=(X-X^T)/2 and S(X)=(X+X^T)/2. Both lie in this Lorentz algebra.
Their coordinate projectors Pi_R, Pi_S are orthogonal for its stated
Frobenius metric. Explicitly Pi_R has blocks
`[[1,-1],[-1,1]]/2` on pairs (N2,Nbar2), (N3,Nbar3), entry1 on J, entry0
on B; Pi_S=I-Pi_R.

At zero the good amplitude is I/2, the bad amplitude sqrt(3)I/2. If
L=dLambda is the exterior Lie representation, differentiation of
`D_j^2=I-T_j^T T_j` gives

    dT_j=(e_j/2)L(X),
    dD_j= -e_j/(4 sqrt(3)) (L(X)+L(X)^T).

These are first jets of the actual full16 matrices. On the prepared grade1
sector they give, with g_b the number of good flags,

    a_b=2^(-n) 3^((n-g_b)/2), w_b=a_b^2,
    r_b=sum_(j good) e_j,
    z_b=(4r_b-1)/3,
    A_b(X)=r_b R(X)+z_b S(X),
    (K_b tensor I)Omega=a_b[Omega+(A_b(X) tensor I)Omega]+O(||X||^2).

In particular every flag mass has zero first derivative since Tr A_b=0.
Writing M_b=r_b Pi_R+z_b Pi_S, the true complete pointer law has

    q_(b,a,eps)(0)=w_b/24,
    grad q_(b,a,eps)(0)=eps w_b/(12 sqrt(2)) M_b e_a,
    q_(b,rest)(0)=w_b/2, grad q_(b,rest)(0)=0.

The score is therefore **sqrt(2)** eps M_b e_a, not twice that coefficient;
it is zero on rest. No outcome is postselected or divided by w_b.

At zero the flag law is an independent Bernoulli product with good chance
1/4. This statement follows from the scalar flat Kraus operators, and is
not an independence assertion away from zero. Set s2=sum_j e_j^2. Then

    E r=1/4, E z=0,
    E r^2=(1+3s2)/16, E z^2=s2/3.

Summing all positive outcomes gives the exact classical Fisher form

    I_full=(1+3s2)/96 Pi_R + s2/18 Pi_S.                 (1)

This is a local six-coordinate measurement theorem for one holonomy, not
a six-coordinate inversion of an arbitrary larger field chart.

## 3. Explicit finite-sample estimator and quantum lower bound

For one recorded pair (b,d), form the known score vector

    score(b,a,eps)=sqrt(2) eps M_b e_a; score(b,rest)=0.

For m independently prepared and executed copies define

    xhat=I_full^(-1) (1/m) sum_(i=1)^m score(b_i,d_i).

Exactly at zero, E xhat=0, D_x E_x xhat|_0=I6 and
`Cov_0(xhat)=I_full^(-1)/m`. This is exact covariance and local
unbiasedness, not global unbiasedness, finite-radius error control or a
tail-probability guarantee. All m preparations and n*m Julia calls are
real executions and their flags/records are retained.

For equal e_j=1/n, the two variances per sample are
`96n/(n+3)` and `18n`. For n>=3, `m=ceil(18n/eps^2)` suffices for
variance <=eps^2 in every unit coordinate direction at zero. For n=1,2
use `ceil(max(96n/(n+3),18n)/eps^2)` instead.

The pre-detector full pure output is `Psi_X=sum_b |b>K_b(X)Omega`.
Its tangent has zero overlap with Psi_0 and squared Gram
`(1/2) E M_b^2`. The pure-state QFI is consequently

    F_Q=2 E M_b^2=12 I_full
       =(1+3s2)/8 Pi_R + (2s2/3) Pi_S.                 (2)

A parameter-independent complete detector dilation preserves this QFI;
dephasing or discarding some fine records can only lower accessible
information. A one-dimensional unit boost has QFI 2/(3n) at equal steps.
For m identical independently prepared outputs, even a collective
measurement and a locally unbiased estimator obey

    Var_0(xhat_boost)>=3n/(2m).

Thus the necessary condition for variance <=eps^2 is
`m>=3n/(2eps^2)` in this fixed-input/fixed-output experiment. This does not
bound biased estimators at a point, different preparations, cross-run
entangled inputs, adaptive gates or a different task. The lower bound is
single-parameter, so does not require simultaneous attainability of all
SLD bounds. The explicit classical estimator supplies the simultaneous
upper bound. For n>=3 their Julia-call count is
`Theta(n^2/eps^2)` in the local small-error regime (with integer rounding).
This counts calls, not complete physical Cost−Info; the detector is within
factor12 of QFI as a quadratic form.

## 4. Original Golden J+ source without the all-good attenuation

Append the owner's original Golden split (p,p^2), p=phi^(-1), to the fresh
J+ detector label for EVERY retained flag string. This can be one fixed
complete refined effect frame; no older flag selects an active gate.
The increment of the complete declared pointer entropy is

    Delta H_phi=(2-p) sum_b q_(b,J,+).

The symmetric unsplit pointer has zero first Lie source, because each
label pair has equal base probability and opposite derivatives, and rest
and flag masses have zero derivatives. Since J is antisymmetric and
E r=1/4, the added source is exactly

    D_J Delta H_phi(0)=(2-p)/(48 sqrt(2)),               (3)

independent of n and the positive partition. Its other five original Lie
components vanish. Retaining J+ only on the all-good branch would instead
give `(2-p)4^(-n)/(12 sqrt(2))`; that is a different recorded programme.
Equation (3) is a pointer-information increment. It becomes a selected
mean Book price only if the same complete cut, w=q binding, normalizer
and all real work/preparation/controller sources are supplied.

## 5. Existing experiment distinctions and remaining admission

The original Golden two-fresh-flag owner uses contractions p Lambda(U_i),
reads the thirteen effects only on GG, and retains GB/BG/BB as three
separate failure labels: sixteen outcomes. The fixed-Bell programmed
extension adds a Bell failure, making seventeen. Its ideal Bell rate
1/4096 and the later native coherent rate p^36 have distinct owners and
prices. Those experiments are NOT this 13*2^n full-flag, T=Lambda(U)/2
experiment, and none of their absolute source coefficients is imported.
In particular existence of a native heralded Bell component does not
compile this whole 13-effect detector at unit success or select its price.

The more recent original sequential owner is
`A4D_NATIVE17_OPTIMAL_STOPPED_ORIENTATION_AND_INFO_2026_10_21.md`.
It fixes two hypotheses exp(+/- xi N2), pays a fresh known input per
seventeen-outcome trial, and retains the Bell factor in
`c=p^4/(24*4096)`. Its only unequal pair is
`u=c(1+xi/sqrt(2))^2`, `v=c(1-xi/sqrt(2))^2`.
Its stopping threshold and expected trial count solve a binary
orientation task at a specified nonzero xi. Our theorem instead estimates
six infinitesimal coordinates at the flat point using the full 13*2^n
record. The number of Julia substeps n, the number of independent trials
m and that owner's stopping threshold are different variables. Its
fixed-accuracy xi^(-2) trial scaling neither contradicts nor is removed
by the present n^2/eps^2 call scaling. The common underlying detector
signatures do not identify preparations, failure readouts or task prices.

Full40 source recovery, observer/basepoint transport, actual field-to-link
maps, literal physical admission, the compulsory complete action and a
controlled geometric refinement remain separate. The positive primary
Einstein–CAR family is unchanged. No GR closure is claimed here.

See `BORN_BOOK_SOURCE_SHAPE.md` for the reconstructed nonlinear price gate.
`SOURCE_PINS.json` pins the literal owners and supplied input used here.
