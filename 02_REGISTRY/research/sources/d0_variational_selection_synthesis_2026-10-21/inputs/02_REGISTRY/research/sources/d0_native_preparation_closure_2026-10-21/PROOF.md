# Original full128: complete dynamical preparation, paid boundary source, and the noncommuting Golden correction

21 October 2026. Existing research PR #334, constitutive/native-programme-v1.
Scientific input: `dda8f5d8ce5950cce4278b1f5b7d63f826b2e8f2`.
No new physical action, information law, task, or acceptance state is introduced.

## 0. The substitution actually obtained

The original record channel, not a freely assigned preparation, determines an
inverse-Dirac-square invariant density. Under an explicit finite recycling gap
we classify **all** fixed operators, including the singular/dark case, and prove
actual relaxation of the same full128 process. Its literal Walsh phases also
supply an all-length reversal identity for the complete reported future tape.
We differentiate that preparation and compute the exact accumulated native
port cost with both endpoint terms retained.

The same recycling operator produces the term missing from extrapolating the
previous Golden clock result away from its scalar-energy shell. We compute it
exactly after TWO original rounds, and obtain a strictly positive full Book
Hessian discrepancy on a real proper-Lorentz-link direction. This is a source
of the existing determinant, not a compensating action added by hand.

The dynamical fixed-state equation is NOT the Euler equation of an arbitrary
price. The derived marginal is not silently substituted for the primary CAR
purification, the supplied Choi programme bank, or the full retained record.
The original port charges are a derived component of Cost, not an assignment
of all label/compiler/work costs or Book03 Info. Full physical GR is not closed.

### Unchanged inputs

- `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md`, especially (2), (3),
  (7), (8), and the flat-only stationary theorem; blob
  `df8611c7fa37fa71e883831b3f01f434532d99ce`.
- `A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md`, fixed-phase rows and the
  genuine noncommuting recycling drift; blob
  `8fe8059b98c60425fb570a10cb8d06c8adb13073`.
- `sources/d0_full128_normalization_closure_2026-10-21/PROOF.md`, true
  complementary determinant; blob `eeae605705b5ee29a098ab9e14c4882034c73795`.
- `sources/d0_book_uniform_source_2026-10-21/PROOF.md`, count-controlled
  normalization and its scalar-first-shell Golden-clock theorem.
- That packet's native numerical definitions, blob
  `ee8de4635d24c668949ac9a0186616ab7d59f2ed`, imported unchanged by the checker.

The general finite-matrix tools here are elementary channel/fixed-point
algebra, not claimed as new general quantum theory. Quantum Doob-transform
background is Carollo et al., arXiv:1711.10951 and Cilluffo et al.,
arXiv:2007.15659. No physical admission or D0 price is borrowed from them.

## 1. Actual finite operator and units

Let D=D* on a finite d-dimensional DATA space, Delta=D^2, and use the actual
paired Julia recycling map

    T(X)=sum_j N_j* X N_j,
    T(I)=I, Tr T(X)=Tr X, T*=T.

The unchanged full128 round is exactly

    Phi(rho)=rho+epsilon [T(D rho D)-{Delta,rho}/2].       (1)

Its complete Stinespring tape is kept; tracing it here only calculates a
marginal. The original Golden construction also gives

    Phi=p Id+p^2 R,   p=phi^-1,   p+p^2=1,               (2)

where R is the CPTP channel obtained from the same reflection and blank
controller. Thus this is not an arbitrary Euler discretization declared CP.
The original port1 cost effect is

    E=p epsilon Delta,     G_port=I+E.                  (3)

On the full stencil one has D=D_h and epsilon=p^2 h^2/64. In the explicit
L4 Fourier check we instead use the literal block A=h D_h/16 and
`epsilon=4p^2`; then `epsilon Delta=4p^2 A^2` is unchanged. The printed
rational energies refer to A^2, not to a retuned physical calibration.
The oldRIGHT tensor is preserved throughout the actual execution.

## 2. Complete stationary-state classification

Assume, for the uniqueness statement only, that on the traceless matrices

    ||T(X)||_HS <= q ||X||_HS,  q<1.                    (4)

### Theorem 1: regular D

If D is invertible, the unique normalized stationary DATA density is

    rho_* = Delta^-1/Z,        Z=Tr Delta^-1.            (5)

Existence needs only unitality: D rho_* D=I/Z, so both terms in (1) equal
I/Z. It does not assume Gibbs weights, a spectral prior, D>0, or a scalar
energy shell.

For uniqueness take any fixed operator rho, not necessarily positive. Put
X=D rho D. The stationary equation is

    T(X)=C_D(X),
    C_D(X)=(D X D^-1+D^-1 X D)/2.                       (6)

In a D eigenbasis the coefficient on entry ij is
`(d_i/d_j+d_j/d_i)/2`, whose absolute value is at least one, including
opposite signs. C_D preserves trace, fixes I, and its inverse has HS norm
at most one. Write X=xI+X_0, Tr X_0=0. Equation (4) and (6) give

    ||X_0|| <= ||C_D X_0|| = ||T X_0|| <= q||X_0||.

Hence X_0=0 and every fixed operator is proportional to Delta^-1.
This proves the full finite classification, not only a density ansatz.

### Theorem 2: singular D

Under the SAME recycling hypothesis (4), if P_0 projects onto ker D, then

    Fix(Phi)={P_0 X P_0 : X arbitrary}.                 (7)

Proof: let P=I-P_0 and X=D rho D=PXP. Restrict (6) to the invertible
D|_P. Norm contraction and compression give

    ||X|| >= ||T X|| >= ||P T(X)P|| = ||C_(D|P)X|| >= ||X||.

Equality in the contraction of a unital trace-preserving map satisfying
(4) forces X to be scalar on the FULL space. Since X=PXP and P_0 is
nonzero, X=0. Equation (1) then gives {Delta,rho}=0, which has exactly the
P_0-P_0 block as its kernel. Conversely every such operator is fixed.
No inverse on a dark subspace or invented low-energy occupation is used.

### Actual convergence and its scope

By (2), every eigenvalue of Phi is `p+p^2 mu`, |mu|<=1. Its only possible
unit-modulus value is 1. Powers of a finite CPTP channel are bounded, so the
unit eigenvalue has no nontrivial Jordan block. Therefore Phi^n converges.
For invertible D and (4), for every joint DATA/oldRIGHT initial state,

    (Phi^n tensor Id)(rho_DR) -> rho_* tensor rho_R.      (8)

Earlier record correlations remain in the global state and are not erased.
In the singular case the limit is a channel into the dark algebra; its
state there need not be unique and can retain reference correlations.

On a fixed finite smooth parameter chart with D invertible and a uniform
strict recycling bound, the inverse and the simple spectral projection are
smooth. On compact subcharts the stable spectral radius is bounded below
one. For a slightly larger number r<1 there are finite chart-dependent
constants with O(r^n) convergence and O(n r^(n-1)) first-derivative error
(after differentiating the limiting projection as well). These constants
are NOT asserted uniform in spatial refinement or approaching a dark mode.
No finite number of rounds is declared to give the limiting state exactly.

## 3. How the native recycling hypothesis is obtained

On the actual Fourier fixture, nu=3/5 and b=sqrt(1-nu^2)=4/5. The unchanged
unshifted half of T has the original full16 traceless bound `(3+b)/4`.
The shifted half remains bistochastic and HS-contractive, including a proper
Lorentz boost on the strict Julia chart. Thus

    q <= (1+(3+b)/4)/2 = 39/40.                         (9)

This proves uniqueness on the fixture without a spectrum census.

There is also a finite spatial sufficient condition, not an assumption that
all curved fields are mixing. Suppose the site graph is connected; each
local coframe is nondegenerate; each forward link transport is invertible;
and the tuples `(|u_0(x)|^2,...,|u_3(x)|^2)` distinguish the finitely many
sites. The unshifted CAR identities put each diagonal scalar
`|u_r(x)|^2 I16` in the algebra of the actual recycling Kraus operators.
Polynomial interpolation then gives the site projections algebraically.
At each site the four independent creators and their adjoints generate M16.
Each nonzero shifted creation/transport block connects adjacent site matrix
algebras. Connectedness therefore generates the full DATA matrix algebra.
This is a commutant argument, not a claim that those polynomials are free
physical operations.

For a bistochastic channel, its fixed algebra is the commutant of its Kraus
operators and their adjoints (the HS equality follows by expanding the sum
of squared commutators). Hence the +1 eigenspace of this selfadjoint T is
only the scalars. A strictly positive native Julia defect is a Kraus operator.
A -1 eigenoperator would anticommute with that positive operator, and must
vanish. The remaining finite spectrum is strictly inside (-1,1), giving (4).

Site separation is a sufficient open condition, not necessary. It excludes
the deliberately homogeneous all-site Fourier conservation case, which must
be handled in its invariant blocks. No mesh-uniform recycling gap follows.
The inverse-D and dark classifications apply separately as stated above.

## 4. Full induced first source and a bounded stationary inverse

For every actual coframe, proper-link or observer tangent on a regular chart,

    d rho_* = -Delta^-1(dDelta)Delta^-1/Z
              +Delta^-1 Tr(Delta^-2 dDelta)/Z^2.         (10)

No dT term is missing: differentiated unitality says dT(I)=0, and
D rho_* D is scalar. Differentiating (1) with (10) gives the entire
dynamical stationary first equation. This is not obtained by freezing rho.

One can solve forced stationary equations without searching new roots.
For trace-zero forcing R, `(I-Phi)rho=R`, Tr rho=0, first solve on the
traceless space

    X_0 = (C_D-T)^-1 (R/epsilon)
        =sum_(k>=0)(C_D^-1 T)^k C_D^-1(R/epsilon).       (11)

It converges in HS norm with bound `1/[epsilon(1-q)]`. Set

    x=-Tr(Delta^-1 X_0)/Z,
    rho=D^-1 X_0 D^-1+x Delta^-1.

This is the exact inverse with the normalization row retained. In particular

    ||rho||_HS <= ||D^-1||^2 (1+sqrt(d)||rho_*||_HS)
                        ||R||_HS/[epsilon(1-q)].        (12)

The d, small eigenvalue, epsilon and recycling-gap factors remain explicit.
They cannot be discarded in the original raw216 or a source-gain division.

## 5. Complete native future-history reversal, with its phase boundary

The actual Walsh rows have fixed adjoint parity. With label l and coefficient
bit a, put `s_j=(-1)^bit1(l)` for a=0 and `s_j=1` for a=1. Zero rows may
carry either sign. The literal word pairs give

    N_j*=s_j N_j.

The coefficient-zero rows are combinations of
`P_r+sigma P_r* - tau(C_r+sigma C_r*)`; coefficient-one rows are real
linear combinations of the four Hermitian defects. This proves the identity
at finite stencil spacing, not merely in a scalar-shell limit.

For the original Kraus operators (and s=1 for the ordinary blank),

    D K_gamma = s_gamma K_gamma* D.                    (13)

For a chronological word omega and its reversed label word rev(omega),

    K_omega D^-1 = s_omega D^-1 K_rev(omega)*.           (14)

At (5), taking the full DATA trace gives for every length n

    q_omega = ||K_omega D^-1||_HS^2/Z
            =q_rev(omega).                             (15)

Every label, both ports, and their zero-probability cases are included.
The identity remains valid for any retained external purification with DATA
marginal rho_*. Its complete first derivative includes (10). Freezing that
preparation generally violates the derivative of (15).

This is the law of the n future rounds from stationary DATA, NOT reversal
of an uncomputed preparation prefix from a different initial state. Also
K_omega and K_rev(omega) need not coincide; their ordered memory operators
remain different. Equality of scalar probabilities does not replace Book03's
noncommutative memory sum by a scalar sum or prove microscopic time reversal.

## 6. Exact paid prefix and surviving preparation source

For the actual charges 1+b, define E from (3) and

    kappa=Tr(rho_* E)=p epsilon d/Z.                    (16)

For invertible D with (4), there is a unique Hermitian Y solving

    (I-Phi*)Y=E-kappa I,        Tr(rho_*Y)=0.             (17)

This follows from the finite spectral decomposition above, or its adjoint
stationary inverse. Y is an analytical cost corrector, not a new operation,
penalty or physical price. Telescoping gives EXACTLY, at every finite n,

    sum_(j<n)(Phi*)^j E=n kappa I+Y-(Phi*)^nY.            (18)

For a normalized initial DATA density rho_0, with every paid round retained,

    C_port,n=n(1+kappa)+Tr(rho_0Y)-Tr(rho_nY),
    rho_n=Phi^n(rho_0).                                 (19)

All field, initial-state and clock-calibration derivatives of this same
identity are retained; n is an integer held fixed in a field variation.
For example

    d kappa=p d (d epsilon)/Z
             +p epsilon d Tr(Delta^-2 dDelta)/Z^2,
    d C_port,n=n d kappa+d Tr(rho_0Y)-d Tr(rho_nY).        (20)

On a fixed regular chart the last term tends to zero, because
Tr(rho_*Y)=0 also has zero total derivative. But the initial term remains.
At fixed fields an independent trace-zero initial variation has

    lim_(n->infty) delta C_port,n=Tr(delta rho_0 Y).       (21)

Thus terminal DATA forgetting does not remove the source of its PAID writer.
Dividing by n would remove this boundary in a rate, but would change an
absolute price comparison. No such division is used here.

The same Poisson construction applies to any actually supplied complete
per-round cost effect G, with mean Tr(rho_*G). We do not assign missing
label/controller/factory prices. A nonlinear information functional of the
whole retained record has its own source and is not determined by (19).

## 7. Explicit noncommuting full16 application

Use the original CAR order (0,2,3,1), nu=3/5, Fourier character
(i,i,-1,-i), and only the actual role-1 boost. Parameterize

    r=tanh(theta/2),   theta=log(5/4) at r=1/9.

The full native A is computed from the literal first Walsh row. Its squared
operator has the exact quadratic minimal polynomial

    Delta^2-2 mu(r) Delta+v(r)I=0,
    mu=9(5r^4+r^3-8r^2-r+5)/[3200(1-r^2)^2],
    v=81(23r^4+6r^3-32r^2-10r+25)/[10240000(1-r^2)^2].   (22)

Both eigenvalue multiplicities are eight on the regular nonzero-r chart.
The inverse identity `(2mu I-Delta)/v` is checked entrywise and does not
require numerically resolving that degeneracy. It gives

    Tr(rho_* Delta)|_(1/9)=69399/5030720,
    partial_r Tr(rho_* Delta)|_(1/9)=-20040939/9885993640.  (23)

These are original A-units. Multiplying by p epsilon gives the true stationary
surplus rate and source, approximately 0.0130262718422 and -0.001914233049.
The entire explicit invariant density is positive and nonscalar.

The checker sums all16,384 ordered two-round probabilities and derivatives.
Reversal holds to its stated floating tolerance; the order-operator norm
gap exceeds 0.011. The exact all-length proof is (13)-(15), not an inference
from that enumeration.

For rho_0=|0><0|, use the normalized initial rotation
`cos(s)|0>+sin(s)|3>`. Its first tangent preserves the external reference
Gram. The actual Poisson boundary gives

    Tr(delta rho_0 Y) approximately 0.309386161947,
    delta C_port,64 approximately 0.0397417357954.        (24)

These are diagnostic values, not rational sign certificates. The exact
boundary identity is (18)-(21). This rank-one initial/reference fixture is
not the primary full-site rank128 preparation. The calculation expressly
keeps that distinction.

## 8. The exact noncommuting Golden normalizer

For the already owned extra port-cost amplitude mark, let

    c=p(1-exp(-t)),    eta=1-c=p^2+p exp(-t).

Stripping the n mandatory scalar marks changes no paid cost. The actual
one-step marked adjoint is exactly

    Phi_t*=Id+epsilon L_eta*,
    L_eta*(X)=eta D T(X)D-{Delta,X}/2.                  (25)

This uses the whole original port1 effect/map, including its orphan blank
label. For TWO original rounds, N_2=(Phi_t*)^2(I). Set
`N_c=(I-c epsilon Delta)^2`. Direct multiplication proves

    N_2-N_c=-c eta epsilon^2 D[T(Delta)-Delta]D.          (26)

N_c is the commuting/spectral replacement, not a newly selected instrument.
Equation (26) is an exact finite formula on the actual noncommuting carrier.

Define the nonnegative native recycling Dirichlet energy

    Drec=Tr Delta(Delta-T(Delta))
        =(1/2)sum_j ||[N_j,Delta]||_HS^2.                (27)

Expanding the squares uses both unitality and trace preservation. Then

    Tr(N_2-N_c)=c eta epsilon^2 Drec.                    (28)

If (4) holds, `Drec>=(1-q)||Delta-(Tr Delta/d)I||_HS^2`.
Thus on a genuinely mixing non-scalar-energy block this missing term is
strictly nonzero. It is produced by the SAME operator which selected (5).
No arbitrary normalization scalar can remove it.

This does not contradict the previous scalar-shell theorem: Drec=0 there.
Nor does (28) alone give the sign of a nonlinear determinant difference.
The full determinant/source test follows separately.

## 9. Positive actual finite Book Hessian discrepancy

On the SAME native proper-link chart (22), Delta(0)=lambda I,
`lambda=9/640`. Let Delta_1=partial_r Delta(0) and use the actual unboosted
recycling T_0. Exact full16 CAR algebra gives

    a=Tr Delta_1(I-T_0)Delta_1=2349/64000000,
    b=||(I-T_0)Delta_1||_HS^2=22761/6400000000.           (29)

Consider the original n=2 blank corner and its genuine oldRIGHT factor128:

    G=(I-epsilon Delta/2)^4,
    J(N,G)=128[logdet N-logdet((1-z)N+zG)], z=2^-20.

Put `t=2 log(phi)` so eta=p and c=p^2. Define scalar functions

    n(l)=(1-c epsilon l)^2, g(l)=(1-epsilon l/2)^4,
    q(l)=(1-z)n(l)+zg(l),
    h(l)=1/n(l)-(1-z)/q(l),
    j(l)=-1/n(l)^2+(1-z)^2/q(l)^2.

Then the exact coefficient of r^2 in the FULL determinant difference is

    K=128{c eta epsilon^2 a [h(lambda)+lambda h'(lambda)]
          +(1/2)j(lambda)(c eta epsilon^2 lambda)^2 b}.  (30)

Proof: write M=N_2-N_c. At r=0, M=0, Tr M_1=0,
Tr M_2=c eta epsilon^2 a, and
`Tr Delta_1 M_1=c eta epsilon^2 lambda a`.
The differentiated identity [D,Delta]=0 implies [D_0,Delta_1]=0;
this is needed when taking the last trace. Also
`Tr M_1^2=(c eta epsilon^2 lambda)^2 b`.
Taylor expansion of the two log determinants gives exactly (30).
All derivatives of T are accounted for through the exact trace identity
(27)-(28); their scalar-base terms cancel by differentiated unitality and
trace preservation, rather than being frozen.

The checker evaluates (30) in Q(sqrt(5)) and proves the rational enclosure

    2418/10^12 < K < 2419/10^12,
    K=2.4185419946151059709... times 10^-9.               (31)

Consequently

    J(N_2(r),G(r))-J(N_c(r),G(r))=K r^2+O(r^3),
    partial_r difference=2K r+O(r^2).                   (32)

An independent evaluation of the original full matrix determinants at
r=+/-0.02 and +/-0.01 checks the same coefficient. This closes the attempted
source-neutral extension of the shell's spectral normalization along this
actual independent proper-link direction. It is NOT a claim that the original
shell identity failed, or that every conceivable curved-clock construction
is excluded. No physical metric Golden scaling follows from the shell alone.

## 10. Parent composition and remaining physical equation

We now have one actual full128 chain connecting D, all Kraus histories,
dynamical invariant preparation, its full derivative, literal accumulated
port cost, and the true finite complementary normalizer. The two former
shortcuts are decided on this SAME carrier:

- Repeated native processing really selects (5) on its regular mixing domain,
  or the dark algebra (7). It does not freely select the previous primary CAR
  pure programme. Its preparation price has the exact source (20)-(21).
- Golden cost marking reduces to a pure clock on the old scalar shell, but
  the real noncommuting extension contains (26) and the nonzero source (32).

Neither result selects Book03's branch Info. In particular (15) is a scalar
record identity, not equality of ordered memory operators. Generated DATA
marginal stationarity also does not imply stationarity under every independent
unitary on DATA plus its retained archive. The initial RIGHT Gram remains
unchanged by the physical channel; it need not equal the Schmidt spectrum of
the DATA marginal after that tripartite evolution.

If a proposed single execution uses this writer, the actual full source must
include `d C_port,n` from (20), every other actually paid cost, the complete
record information source, and the chosen active-cut/clock terms. Only a proved
identity of those terms with the original 42-source and its independent
upstream equations could complete the physical GR application. None is supplied
by replacing the retained history with rho_*, dividing the price by n, dropping
Y, or replacing N_2 by N_c. The original nonvacuum full-price root, compulsory
Info/admission, uniform physical refinement and raw216 remain unproved.

## 11. Reproduction and evidence

`check_native_preparation.py` imports only the pinned old native definitions;
it does not run that previous suite. It contains exact rational/number-field
checks, a direct actual all128 two-round tape, full source/Poisson finite
recursions, retained-reference and hostile controls, and original determinant
secants. Normal and optimized runs, input/output hashes and mutation results
are recorded in VALIDATION.json. Numerical checks have explicit tolerances;
the all-size classifications and source identities are analytical proofs above.
No independent-agent review, fresh Lean build, whole-repository CI or
physical acceptance is claimed. `GR_closed=false`.

### Concurrent integration note

Before publication, the existing owner advanced to 95bab26d. Its paid rational
resource writer supplies finite precompiled orthogonal approximants and a
counted-CQ composition, not a common smooth physical Book valuation. It is a
different input mechanism from repeated native Phi and is not duplicated here.
Its discrete-field/source scope and the concurrent Cartesian star factor
-1/2 / rank-two orientation correction are retained. None of this packet's
operator/preparation proofs uses the disputed continuum/finite normalization
or imports a resulting Einstein coefficient. No older physical admission gap
is asserted closed or absent merely from historical summaries.
