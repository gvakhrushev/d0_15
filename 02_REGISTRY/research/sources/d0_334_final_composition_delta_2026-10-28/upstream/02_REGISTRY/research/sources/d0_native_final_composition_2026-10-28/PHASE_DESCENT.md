# Retained archive phases: exact Hamiltonian descent and the finite momentum test

28 October 2026. Existing PR #334. Changed input:
`1d29848fa0775485f7d48ab63f4a6625f9b705ad`, primary source §7cv,
equations (846)–(850). This consumes the NEW retained-history form rather
than treating the earlier cut-pair form or terminal graph as its substitute.
No new action, physical phase actuator, expectation Hamiltonian, or HDA is
postulated. The purpose is to decide the descent premise explicitly left
open in (848).

## 1. The exact new carrier

On a fixed finite bright support of m recorded outcomes let

    Psi(x,phi)=sum_b sqrt(w_b(x)) exp(i phi_b)|b> chi_b(x),
    sum_b w_b=1, w_b>0, ||chi_b||=1,
    J_bA=partial_A w_b, rank J=d,
    beta_A=-i sum_b w_b <chi_b,partial_A chi_b>.

The real x-chart is open in R^d; all displayed data are smooth. The fixed
record labels are orthogonal even when the conditional states are not.
The fixed support and real local phase lifts are precisely those of (846).
Dark-flag births, moving complex structure, or additional unresolved metadata
require their own chart and are not removed here. Normalization implies
J^T 1=0 and d<=m-1.

The owned form is

    theta=sum_b w_b dphi_b+beta_A dx^A
          =d(sum_b w_b phi_b)-Pi_A dx^A,
    Pi=J^T phi-beta,
    omega=sum_A dx^A wedge dPi_A.                          (1)

Define pi_map(x,phi)=(x,Pi). Because J has full column rank, pi_map is a
submersion. Its kernel, and the kernel of omega, are exactly

    V_(x,phi)={(delta x,delta phi):delta x=0,
                                  J(x)^T delta phi=0}.    (2)

In particular the canonical rank is 2d. The phase kernel has dimension m-d
and includes global phase. This is a local statement on phase lifts; it does
not assert that Pi is a globally single-valued coordinate on a phase torus.

## 2. Exact descent criterion for a represented finite expectation

Consider the specific represented class of (848),

    h_N(x,phi)=<Psi(x,phi),H_N(x)Psi(x,phi)>,                (3)

where H_N(x) is Hermitian on the actual finite full carrier and has no
additional relative-phase dependence. No assertion that Book price equals
this generator is made. Let

    a^N_bc(x)=sqrt(w_b w_c)
              < b tensor chi_b, H_N(x)(c tensor chi_c) >,
    f_bc=e_c-e_b,  D_N=sum_b a^N_bb.

Then a_cb=conjugate(a_bc), and the complete expectation is the finite Fourier
sum

    h_N=D_N+sum_(b!=c) a^N_bc exp(i f_bc dot phi).           (4)

Every frequency f_bc of an ordered pair b!=c is distinct. Conditional-state
matrix elements are essential: a bare off-diagonal block of H_N need not
have a nonzero a_bc on the actual conditional states.

**Theorem.** At a fixed x, (3) is locally constant along the fibres (2) for
all phi in a nonempty open phase chart if and only if

    a^N_bc(x)!=0  =>  f_bc belongs to im J(x)              (5)

for every ordered pair b!=c. For descent over an x-neighborhood, (5) must hold
at EVERY x there. To construct the whole lapse family, it must hold for every
actual N, and the analogous condition applies to every represented shift.

**Proof.** For k in ker J^T, the exact vertical derivative is

    dh_N(0,k)=i sum_(b!=c) a^N_bc (f_bc dot k)
                                     exp(i f_bc dot phi). (6)

Distinct finite Fourier characters are linearly independent on any open
subset of R^m. Thus (6) vanishes identically there iff every coefficient
a_bc(f_bc dot k) vanishes. Requiring this for all k in ker J^T gives exactly
f_bc in (ker J^T)^perp=im J whenever a_bc!=0. Conversely (5) makes (6) zero.
The fibres are locally connected affine subspaces, so this differential
condition is precisely local descent. QED.

This removes an existential ambiguity in the new phase route: full column
rank J and canonical rank 2d do NOT by themselves prove that a proposed
physical Hamiltonian descends. Its actual conditional off-diagonal matrix
elements must pass the finite test (5).

## 3. The descended function and every x-reaction are explicit

Put J^+=(J^T J)^(-1)J^T. For every active permitted edge set

    k_bc=J^+ f_bc,             J k_bc=f_bc.

Then the unique local descended function is

    hbar_N(x,Pi)=D_N(x)
       +sum_(b!=c) a^N_bc(x)
             exp(i k_bc(x) dot (Pi+beta(x))).             (7)

The same expression follows by the owned affine representative
phi=J(J^T J)^(-1)(Pi+beta). Equation (5) ensures independence of every excess
phase. Without (5), evaluation on that representative is a choice of a
section, not a Hamiltonian on the physical quotient.

At fixed x,

    partial_(Pi_A) hbar_N
       =sum i a^N_bc (k_bc)_A exp(i k_bc dot (Pi+beta)).   (8)

On a region where a permitted edge remains active,

    partial_A k_bc=-J^+ (partial_A J) k_bc,                (9)

because differentiating J k_bc=f_bc gives the identity and f_bc is constant.
The full coordinate derivative retains both reactions:

    partial_A hbar_N=partial_A D_N
      +sum [partial_A a^N_bc
        +i a^N_bc{(partial_A k_bc) dot (Pi+beta)
                              +k_bc dot partial_A beta}]
                        exp(i k_bc dot (Pi+beta)).        (10)

Alternatively differentiate the smooth J^+ expression directly at zeros of
coefficients, without assuming their support is locally unchanged. The
coefficient derivatives themselves contain the actual w, chi and H_N
derivatives. Freezing J or beta would generally change (10).

## 4. Quantified vertical obstruction and the decoder reaction

Let P_V=I-J(J^T J)^(-1)J^T be the Euclidean orthogonal projector onto the
phase kernel. On the mathematical full phase torus, Fourier orthogonality
gives the exact identity

    integral ||P_V grad_phi h_N||^2 dphi/(2pi)^m
      =sum_(b!=c) |a^N_bc|^2 ||P_V f_bc||^2.             (11)

A single active bad unordered edge therefore contributes
2|a_bc|^2 dist(f_bc,im J)^2. A phase-kernel residual bounded by epsilon
uniformly on this torus must satisfy RHS<=epsilon^2. Conversely the triangle
inequality gives sup ||P_V grad_phi h_N|| <=sum |a_bc| ||P_V f_bc||.
These are actual phase-Euclidean norms, not automatically field or gate-max
norms. A bound only on a small physical phase patch is not silently promoted
to the torus-wide bound in (11). Nonvanishing on every open patch follows
from analyticity, but a pointwise positive lower bound at every phase does
not follow and is not claimed.

The self-reading correction in (848) cannot cancel (6) while q is resolved
by the phase-independent x. In full-state notation,

    dh_N=Tr(H_N dvarrho)+sum_a c_Na dq^a.

For a vertical phase k, dq^a(0,k)=0. Hence the second term vanishes on it
and the vertical source is still exactly (6). If the true decoder is phase
sensitive, q=q(x,phi), the operational map and presymplectic comparison must
be recomputed; (5) is not asserted unchanged for that different carrier.

There is an equivalent probability-velocity test. Let E_b be the fixed full
record projector. The actual ambient candidate gradient is A_N from (848),
and its density flow gives

    dot w_b=-i Tr(varrho [E_b,A_N])=partial_(phi_b) h_N.   (12)

The equality uses dq^a/partial phi_b=0 on this phase extension, so the
decoder reaction contributes zero to these probability velocities. A
necessary condition for tangency to w=w(x) is dot w in im J. Equations
(5)–(6) make this condition precise at all phases. Even if it holds, the
conditional states chi_b, untouched operator columns, clock and other
retained coordinates can supply further tangency constraints. Descent is
not the whole admission proof.

## 5. Positive escape and a concrete structural failure

If d=m-1, normalization and full rank give im J=1^perp. Every edge f_bc
then belongs to im J, so all finite expectations (3) descend. Thus the new
carrier can provide nontrivial canonical Hamiltonians; there is no generic
no-go against the phase construction. It retains all independent record
probabilities as coordinates. A later physical metric reduction is another
application, not supplied by discarding the extra coordinates.

Lower-rank families can also pass. For

    w=(1/3+x,1/3-x,1/3), J=(1,-1,0)^T,

the 1↔2 edge lies in im J. With constant conditional states, beta=0 and
H=|1><2|+|2><1|, one obtains the nontrivial descended Hamiltonian

    hbar=2 sqrt(1/9-x^2) cos(Pi), Pi=phi_1-phi_2.          (13)

In contrast, for

    w=(1/3+x,1/3+2x,1/3-3x), J=(1,2,-3)^T,

none of the three edge directions lies in im J. Every descended expectation
in class (3) must therefore be phase independent. The same H above at x=0
has h=(2/3)cos(phi_2-phi_1). The kernel direction k=(2,-1,0) has J^T k=0,
yet at phi_2-phi_1=pi/2 its derivative is 2. The exact squared residual
average (11) is 3/7. These are structural probability charts, not new
native physical record preparations; an original-native witness must use
its own actual probabilities and conditional states.

More generally, if no edge f_bc lies in im J at a given x, (5) forces every
off-diagonal coefficient to vanish there. The descended hbar_N then depends
only on x and cannot supply nonzero momentum kinetics at that x. This is an
exact stated-input conclusion, not a genericity assumption about the actual J.

## 6. Finite expectations cannot be exactly quadratic in these momenta

For each fixed x, restriction of (3) to the AFFINE representative in §3 is a
finite real-analytic Fourier sum in Pi. It is bounded for all Pi in R^d:

    |hbar_N(x,Pi)|<=||H_N(x)||op.                          (14)

If it equals a polynomial of degree at most two on ANY nonempty open
Pi-domain, the real-analytic identity theorem extends equality to R^d.
A bounded polynomial is constant. Therefore a nonconstant quadratic or
linear kinetic polynomial in the specific canonical Pi of (847) cannot
equal a single finite expectation (3) exactly on an open momentum chart.
This applies even when (5) passes. A finite scalar gain or x-dependent
momentum translation does not change this conclusion at fixed x.

The statement concerns these fixed x,Pi readouts and this represented
Hamiltonian class. It does not exclude an infinite carrier, a genuinely
different nonlinear state Hamiltonian, a different proved physical metric
readout, or a controlled continuum/local limit. An arbitrary nonlinear
coordinate change that also changes the metric coordinates is not an
identity in the original (847) variables.

The precise elementary limit escape is

    K_epsilon(Pi)=(1-cos(epsilon Pi))/epsilon^2.

For |Pi|<=R,

    |K_epsilon-Pi^2/2| <=epsilon^2 R^4/24,
    |partial_Pi K_epsilon-Pi| <=epsilon^2 R^3/6,
    |partial_Pi^2 K_epsilon-1| <=epsilon^2 R^2/2.          (15)

These follow from integral Taylor remainders of cosine and sine. The
convergence is locally uniform through the displayed source derivative.
It uses an actual frequency/gain scaling and unbounded amplitude 1/epsilon^2;
no such native scaling is selected here. A physical application must carry
its actual J, gain, norm, allowed momentum region and full-source error.
The owned bracket-transport estimates can consume those errors only once
the genuine generators and inverse physical form have been established.

## 7. The residual (849) after the missing descent has been checked

If the actual normal AND shift functions pass (5), and their ambient
Hamiltonian flows are tangent to the admitted history chart, the inherited
bracket agrees with the reduced canonical one. On that stated common chart
the exact residual can be evaluated as

    A_h[N,M]=sum_A[(partial_A hbar_N)(partial_(Pi_A)hbar_M)
                 -(partial_(Pi_A)hbar_N)(partial_A hbar_M)]
                      -dbar_(q^ij(N partial_j M-M partial_j N)).  (16)

Equations (8)–(10) retain the conditional-state, decoder, J and beta
reactions. This is the actual phase-reduced version of (849) under the
stated tangency, not a claim that (16) vanishes. Descent without tangency
provides an intrinsic Hamiltonian on the quotient but does not identify it
with the proposed ambient normal evolution; a physical constrained reduction
would then need its own proof. If (5) fails, the proposed (848) function
does not even supply this quotient Hamiltonian, so the HDA consumer cannot
be reached by that candidate.

The new input (847) therefore makes the next question finite and explicit:
compute the actual J and conditional H_N/D_X matrix elements, test (5),
retain all actual reactions, and evaluate (16) in the true source norm.
The earlier cut-pair moment obstruction does not substitute for this new
test, because the two boundary forms are not assumed identical.
No physical phase admission, exact ADM kinetic law, HDA or full GR closure
has been proved by the present calculation.
