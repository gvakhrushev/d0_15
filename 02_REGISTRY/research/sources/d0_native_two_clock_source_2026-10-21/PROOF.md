# Same native input, two physical clock scales: finite joint minima and a non-uniform preparation inverse

21 October 2026. Supporting continuation of the existing research owner #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1.
Inspected integration input: `c28187555ef973b7bdb80e48655a2ac5ae8c85b0`.

**Status:** analytical finite-dimensional theorem plus author computational checks.
No new price, information rule, gate admission, physical clock selector, all42
Einstein root, raw216 assertion, or physical GR closure. `GR_closed=false`.

## 0. What is consumed and what changes

The original full-record owner already proves the flat recycling formula below.
The 20 October complete-record price owner already proves the coherent physical
horizon h^-4, its binary limiting entropy, the number
Lambda_*=0.4890273339156223744..., and the different record-plus-RIGHT source.
Those facts are INPUTS, not new discoveries here.

The 21 October retained-entropy input theorem proves free-input strict convexity
when the Choi matrix is faithful and a fixed-mesh long-horizon Gibbs/Poisson
reduction. Its constants are explicitly NOT uniform in spatial refinement.

This packet supplies the missing simultaneous input/clock calculation on one
actual invariant axial Fourier block of that SAME full128 instrument:

* the exact native mixing gap is of order h^6, not h^4;
* every n>=8 has a faithful block Choi matrix, and both specified coherent
  information cuts have the SAME exact unique free-density minimizer I16/16;
* its actual finite coherent price has an exact interior joint input/scale
  minimum at every h=1/L, L>=4, on the specified h^-4 programme;
* these minima converge in C2 source calculus to the already-owned scalar
  minimum, while 254 input Hessian directions become soft;
* actual equilibration uses the different h^-6 scale, whose optimized paid
  field source grows positively as h^-2. The declared original blank-work
  feedback source is then exponentially small, not a compensator.

This is not another root search on a chosen geometric action. It identifies
which of two already-owned limits can be used in the paid-input-to-field
source argument. It does NOT extend an axial homogeneous block to the whole
spatial 16+24+2 problem.

### Carrier, boundary and source convention

DATA is one ORIGINAL axial Fourier sector k=(2pi,0,0,0) on a period-one flat
L^4 lattice, with all CAR16 components. Original links are identity and the
observer is fixed. All 128 original outcomes, both ports, both Julia defects,
and all chronological words remain. Tensor with the original retained
oldRIGHT128 throughout. The full-density variational theorem uses 16 active
Schmidt columns inside that space; it is NOT the spatial primary state's
full rank128 preparation. A prescribed different RIGHT spectrum is not
silently varied into this one. Complex Fourier decomposition is an analytical
invariant-sector restriction; this packet does not build its native input
writer or claim exact Golden preparation of Fourier phases.

The only field variable newly solved is the homogeneous native amplitude a.
No other coframe/link/matter Euler equation is asserted. Norms are finite
Hilbert-Schmidt/operator norms and ordinary first/second a derivatives.
Neither point-slot raw norms nor a mesh-uniform inverse is inferred.

The valuation is the ALREADY DECLARED original port cost minus coherent
record entropy, in base-phi units. Other actual label, preparation, compiler,
controller, work and clock charges remain separate. No formula below identifies
that valuation with mandatory Book03 or adds feedback to it without a binding.

## 1. Literal channel and its exact axial reduction

Put p=phi^-1, ell=ln(phi), h=1/L, nu=ha, 0<a<h^-1, and

    w_h=4 sin^2(pi h),    epsilon_h=p^2 h^2/64,
    lambda_h=nu^2 w_h/h^2=a^2 w_h,
    q_h=epsilon_h lambda_h=p^2 a^2 h^2 w_h/64,
    b_h=sqrt(1-nu^2).                                             (1)

We use q_h for a single-step channel strength, NOT a probability of a
particular history. The actual ordinary blank amplitude is
B_h=(1-q_h/2)I. The original all-label port-one effect is
E_port1=p q_h I. Therefore, for EVERY initial DATA density,

    C_port,n=n(1+p q_h).                                          (2)

Every mandatory tick remains paid. It is legitimate to display F-n when
varying a at a fixed h,n; it is not legitimate to delete n when comparing
programmes or physical clocks.

Let gamma_0,...,gamma_7 be the original eight Majoranas, and Z_r the four
occupation involutions. The actual flat recycling map is

    T_h(X)=w_I X+w_M sum_j gamma_j X gamma_j
                     +w_Z sum_r Z_r X Z_r,
    w_I=(1+b_h)^2/4, w_M=nu^2/16, w_Z=(1-b_h)^2/16.                 (3)

All three weights are positive on the strict chart, and w_I+8w_M+4w_Z=1.
The true Dirac block D_h has D_h^2=lambda_h I and U_h=D_h/sqrt(lambda_h)
is an involution in the first Majorana plane. Rotation in this plane leaves
(3) unchanged. A known h-dependent, a-INDEPENDENT coordinate rotation thus
puts U_h=gamma_0. This is an analytical basis choice, not a free physical
operation or a changed cut. The EXACT original marginal channel becomes

    Phi_h=(1-q_h)Id+q_h T_h Ad_gamma0.                             (4)

`native_axial.py` independently reconstructs all128 Kraus matrices from the
original repeated Walsh/Julia words and checks (1)-(4). No marginal Kraus
recombination is adopted as the physical labelled instrument.

## 2. Exact spectral gap: the record and equilibration clocks differ

For a Clifford monomial indexed by S subset {0,...,7}, let k=|S|, o the
number of role pairs containing exactly one member, and

    u_S=(-1)^(k-1_{0 in S}).

The actual eigenvalues are

    t_S=w_I+w_M (-1)^k(8-2k)+w_Z(4-2o),
    m_S=1-q_h+q_h u_S t_S.                                       (5)

The owned recycling estimate is sharp: for S nonempty,
b_h^2 <= t_S <= (3+b_h)/4. The checker verifies the associated quadratic
polynomial inequalities exactly, but the formula itself follows simply by
commuting one Majorana or occupation involution past the monomial. Equality
at the upper endpoint is attained at degree seven. Seven such monomials
contain gamma_0 and hence have u_S=+1. Modes with u_S=-1 obey
m_S<=1-q_h, while all eigenvalues are positive (q_h<1/2 here).
Consequently the ACTUAL traceless HS gap is exactly

    g_h=1-max_{S nonempty} m_S=q_h(1-b_h)/4,
    g_h=(pi^2 p^2 a^4/128)h^6+O(h^8).                            (6)

This proves the scale, rather than extrapolating a finite spectrum scan.

At the already-owned physical record horizon n_h=128h^-4, define

    tau(a)=8pi^2p^2a^2.

Then n_h q_h -> tau, but n_h g_h ->0. There are 128 monomials with u_S=+1.
Thus

    Phi_h^n_h -> P_+ + exp(-2tau) P_-,
    P_+=(Id+Ad_gamma0)/2, P_-=(Id-Ad_gamma0)/2.                    (7)

This is the already-owned dephasing limit, now read against its exact mixing
gap. It is NOT the fully equilibrated replacement channel X->I Tr(X)/16.
For example a nonidentity commuting degree-seven mode survives with
m_S^n_h->1, whereas replacement sends it to zero.

For actual slow mixing set n_h=floor(128 u h^-6), u>0 fixed, and
sigma=8pi^2p^2 u a^4. Since

    t_S=1-nu^2 d_k+O(nu^4),
    d_k=[8-(-1)^k(8-2k)]/16,

(5) gives the different limit

    Phi_h^n_h -> P_+ exp(sigma R),
    R=(1/16)sum_j(Ad_gamma_j-Id).                              (8)

On commuting monomials its eigenvalues are exp(-sigma d_k); on the
anticommuting subspace they are zero. The smallest nonzero d_k on P_+
is 1/8. Equation (8) is CP and trace preserving: R is a random-unitary
Lindblad generator and P_+ commutes with it. It converges to I Tr/16
only as u tends to infinity. The proof is direct diagonalization (5), not
an invocation of an unverified unbounded adiabatic theorem.

In particular convergence to the full equilibrium on this family requires
n_h g_h->infinity, equivalently n_h h^6->infinity on compact positive a
charts. Nontrivial record information only requires order h^-4. These are
different requirements on the SAME execution.

## 3. Exact input minimum at every finite n>=8

Modulo phases, (4) is a Pauli random-unitary channel on the group F_2^8.
Its positive one-step species include gamma_0 and gamma_j gamma_0,
j=1,...,7, as well as identity. These eight species generate the entire
Pauli group. Every error can be written in at most eight such species;
positive identity padding extends it to every n>=8. Therefore EVERY
Pauli error probability pi_{h,n}(g) is positive for n>=8. The block Choi
matrix is faithful at that uniform finite threshold; this does NOT assert
a uniform lower bound on its smallest eigenvalue.

For general input rho, complementary entropy is concave. Conjugating rho
by any Pauli conjugates the complementary output unitarily: phases simply
multiply its Kraus rows. Twirling rho over this group gives I16/16, so this
state maximizes coherent record entropy. The port charge (2) is independent
of rho. The existing faithful-Choi strict-convexity theorem now proves

    argmin_rho F^E_{h,n}(rho)={I16/16}, n>=8.                      (9)

This closes ALL255 free density equations, not merely one preparation ray.
A purification uses 16 active oldRIGHT columns and leaves its chosen whole
RIGHT Gram fixed. Other fixed spectra retain their own orbit problem.

For the separate record-plus-RIGHT cut, S(ER)=S(Phi_h^n(rho))<=log_phi16.
All m_S are strictly positive, so Phi_h^n is an invertible linear map and
only rho=I16/16 gives the maximum I16/16 output. Thus (9) is also the
unique input minimum for F^ER. The two cuts share the input minimum, not
the same field price.

### The exact whole-record spectrum, without 128^n enumeration

Let chi_S(g)=(-1)^(|S||g|-|S intersect g|). Then

    pi_{h,n}(g)=2^-8 sum_S chi_S(g)m_S^n.                         (10)

The 256 characters are orthogonal. At the maximally mixed input the
normalized Choi eigenvalues, hence the nonzero coherent-record eigenvalues,
are precisely pi_{h,n}(g). Therefore

    min_rho F^E_{h,n}=n(1+p q_h)-H_phi(pi_{h,n}),
    min_rho F^ER_{h,n}=n(1+p q_h)-log_phi16.                       (11)

The pi are SPECTRAL eigenvalues of the coherent tape. They are NOT its
128^n pointer probabilities, and no physical phase/memory record has been
erased. Entropy equality is invariant under Stinespring isometries; a
field-dependent Kraus-basis change does not change the scalar entropy or
its derivative. It does NOT preserve an unspecified Book return cut.
The Book comparison in section7 instead uses the ORIGINAL blank corner.

Only 28 triples (k,o,u_S) occur in (5), so (10) can be evaluated using
28 scalar powers and an exact fixed character table. This evaluates the
finite actual price for very large n; it does not claim the experiment's
rounds were physically executed or were free.

## 4. Actual finite joint input/scale minima exist on every refining mesh

Fix the ORIGINAL physical horizon n_h=128 L^4 and define the displayed
field-dependent part

    f_h(a)=p n_h q_h-H_phi(pi_{h,n_h}).                            (12)

The full paid price is n_h+f_h(a). All derivatives hold n_h fixed.

As a tends to zero at fixed h, q_h is a positive constant times a^2,
T_h tends to identity, and the error probabilities have
pi_0=1-n_h q_h+O(a^4), pi_gamma0=n_h q_h+O(a^4), with the remaining
mass O(a^4). The negative entropy contribution -O(a^2 log(1/a))
dominates the positive O(a^2) surplus cost. Hence f_h(a)<0 for all
sufficiently small positive a, while f_h(0)=0 by continuity.

For L>=4, w_h/h^2>=32. Since H_phi(pi)<=log_phi256<12 and
64p^3>15, every a>=1 on the strict native chart satisfies

    f_h(a)>=64p^3 a^2-log_phi256>3.                              (13)

Thus a GLOBAL minimum exists at some 0<a_h<1, strictly inside the actual
0<a<h^-1 chart, for EVERY L>=4. For n_h>=8 its input is uniquely (9),
and f_h is differentiable there. It solves exactly all255 input rows and
the actual scalar field row partial_a F=0 of this specified price.
It does not solve the other39 geometric plus2 matter directions.

## 5. Source-preserving refinement and eventual uniqueness

The limiting value in (12) is the already-owned

    f_0(a)=p tau(a)-h_phi((1+exp(-2tau(a)))/2).                    (14)

We strengthen its application here to C2 convergence of the OPTIMIZED
finite input/field price on every compact positive a interval:

    ||f_h-f_0||_{C2(a)} <= C h^2(1+|log h|).                      (15)

Here is a finite argument retaining the support births. Write x=h^2.
In (5), q_h=x^2 Q(x,a), where Q is analytic at x=0, and t_S is analytic
in x. At n_h=128/x^2,

    m_S^n_h=exp[(128/x^2)log(1+x^2 Q(u_S t_S-1))]

has an analytic extension to x=0, with all a derivatives on compact
positive intervals. Thus every pi in (10) is analytic in x,a.

For g=0,gamma0 the limiting probabilities are the two positive values
in (14). For other g, let r_g be the number of its Majorana bits among
1,...,7. Then 1<=r_g<=7 and

    pi_g=x^r_g b_g(x,a),    b_g(0,a)>0.                          (16)

To see the leading positivity without assuming a spectral floor, use the
positive one-step walk behind (4). A jump gamma_j gamma0 has total
Poisson rate n_h q_h w_M=O(x) with a strictly positive leading coefficient.
The extra Z_r gamma0 species have rate O(x^2) and contain at most two
nonzero bits away from0. Any path reaching g therefore has weighted order
at least r_g. Taking each required gamma_j gamma0 once, and zero or one
ordinary gamma0 jump to fix bit0, gives a strictly positive leading term
of order x^r_g. Summing all permutations and arbitrary ordinary gamma0
jumps keeps positivity. The finite-step logarithm differs from this
compound-Poisson expression by terms with an extra q_h=O(x^2); the same
bit-count grading shows these cannot alter that leading term. Equivalently,
expand the commuting group-algebra generating polynomial: to affect r_g
nonzero bits requires at least that weighted degree. All its leading
coefficients are sums of positive path terms. These statements are uniform
on compact a intervals bounded away from zero.

Consequently b_g and its first two a derivatives are bounded and b_g stays
positive for small x on such intervals. In pi log pi, each rare contribution
and both a derivatives are O(x^r_g(1+|log x|)); the term (partial_a pi)^2/pi
in the second entropy derivative is O(x^r_g). The two old probabilities
have ordinary analytic entropy derivatives. Summing the finite256 terms
proves (15). No C2 estimate across arbitrary moving rank births is asserted.

The owned scalar g(tau)=p tau-h_phi((1+exp(-2tau))/2) has

    g'(tau)=p-2exp(-2tau)atanh(exp(-2tau))/ell,
    g''(tau)=[4u atanh(u)+4u^2/(1-u^2)]/ell>0,
    u=exp(-2tau).

Hence exactly one positive root exists, tau_*=0.4890273339156223744...,
and a_*=sqrt(tau_*/(8pi^2p^2))=0.12733838610533197569....
This number and the limiting root are consumed from the old owner.

To exclude loss of minima toward a=0, the one-step nonidentity error
probability is <=q_h. Hence the n_h-word error probability is <=n_h q_h
<=8pi^2p^2 a^2. The entropy bound h_phi(delta)+delta log_phi255 tends
uniformly to zero with a. A fixed trial near a_* has negative limiting
value, so minimizing a_h remain in a compact interval away from zero.
Together with (13), (15), and strict positivity of f_0'' near a_*, this
proves for all sufficiently large L:

* the global scalar minimum is UNIQUE;
* a_h=a_*+O(h^2(1+|log h|));
* it is a strict joint minimum with all255 input rows, since their
  Hessian is positive for each finite h and the input minimizer I16/16
  is independent of a, so the mixed input/a Hessian vanishes there.

No numerical finite threshold or interval enclosure for the reported roots
is asserted. The proof establishes existence/effective asymptotics; the
finite root table is a high-precision diagnostic.

## 6. Why this is still not a mesh-uniform input inverse

Write rho(r)=(I+r P_s)/16 for a nonidentity Hermitian Pauli direction.
At the exact input minimum its second variation is

    H_s=(1/ell)sum_g pi_g pi_(g+s)
                [log pi_g-log pi_(g+s)]/[pi_g-pi_(g+s)],           (17)

with continuous diagonal value 1/pi. This follows by inserting the affine
Choi density derivative into the matrix-log divided difference. Pauli
covariance makes the Hessian diagonal in these tangent directions.

At the fast physical limit only pi_0 and pi_gamma0 remain positive.
Therefore H_gamma0 tends to a strictly positive number, while

    H_s=O(h^2(1+|log h|)) ->0,    s notin {0,gamma0}.              (18)

All254 other input directions become soft. Equivalently, the limiting
complementary entropy depends only on Tr(rho gamma0), and its full minimizing
fibre is Tr(rho gamma0)=0, of dimension254 near I16/16. Finite h selects
I16/16 uniquely but no h-uniform Hessian inverse survives. This is an
actual countercontrol to applying the previous fixed-mesh input IFT with
unstated uniform constants.

The two information cuts were already known to give different limiting field
sources. Equations (9)-(11) now show this persists AFTER their exact common
finite input optimization. On the SAME input and same port ledger,

    partial_a min F^ER = p n_h partial_a q_h>0,

while min F^E has the exact finite roots above. At a_h tending to a_*, the
ER source tends to 2p tau_*/a_*=4.74696630028898... . It is not a new
choice of Info and not a physical rejection of one cut.

## 7. Actual mixing cannot be added as a free preparation step

At n_h=floor(128u h^-6), (8) has positive Pauli probabilities at every
u>0,a>0. Its entropy and a derivatives are bounded on compact positive
u,a charts. From (1)-(2), however,

    h^2 partial_a [min_rho F^E_{h,n_h}-n_h]
       ->16pi^2p^3 u a>0.                                      (19)

The same leading result holds for the ER cut. The actual surplus charge,
not a fictitious mandatory-tick source, produces (19). Thus a price
with only an additional uniformly bounded terminal first source cannot
have an interior a-critical point in that chart at this clock. No claim
is made for real extensive or comparably growing remaining charges/Info.

For the separately DECLARED original blank-work Book corner, not an
invented effective Pauli cut, B_h=(1-q_h/2)I and oldRIGHT multiplicity128
supply exactly

    J_blank=-2048 log[1-z+z(1-q_h/2)^(2n_h)], z=2^-20,
    partial_a J_blank=
      2048 z (1-q_h/2)^(2n_h) n_h partial_a q_h /
       [(1-q_h/2)(1-z+z(1-q_h/2)^(2n_h))] >=0.                  (20)

At the slow clock it is exponentially small in 1/h^2 on compact positive
charts. This known terminal feedback component cannot cancel (19). It has
NOT been silently added to the coherent price or identified with the full
Book memory/Info/clock stack. The compulsory actual clock cut is separate.

Equations (6),(19),(20) are the strategic source budget: the physical
information horizon h^-4 is not a fully equilibrating writer, and extending
it until mixing changes the paid field source at leading order. The useful
finite minima in section4 do not require that illicit equilibration step.

## 8. Replays, controls and remaining physical scope

The checker reconstructs the ORIGINAL128 outcomes on an axial CAR16 block,
retains every two-round word, compares its full Choi matrix with (10), and
independently differentiates the 4096-round native matrix power. It checks
the full255 input gradient, exact Golden/group inequalities, both clock
laws, high-precision finite minima, source derivatives and soft directions.
The 256-term spectral calculation is NOT a 128^n history simulation.

The limiting scale, the limiting information-cut contrast, and the generic
strict-convexity principle are old inputs. New claims concern the exact
finite input optimizer/threshold, attained native h^6 gap, slow generator,
C2 same-price refinement with support births, finite joint minima and loss
of input coercivity, and the actual slow-clock source budget. Standard
entropy/channel background is available in J. Watrous, *The Theory of
Quantum Information* (2018), https://cs.uwaterloo.ca/~watrous/TQI/ . The
fast/slow projection has the usual finite dissipative/Zeno interpretation;
no result from that literature is needed beyond the explicit proof (5)-(8).

All local numerical checks are author checks with stated tolerances, not
an independent review or interval-certified physical root. No prior heavy
full-spatial/all42/Lean suite is replayed. A source-matched native Book03
valuation, independent writer/controller/cut equations, nonvacuum all42
recovery and original raw216 remain open. In particular this block theorem
is not a substitute for the actual independently varied Lorentz/coframe
source or a claim that scalar-source stationarity is Einstein's equation.
