# Golden determinant compiler: from a matrix return to the finite curvature reading

16 October 2026. SOURCE #310, pinned input `df9b5b7a4fa473279695100348db7e3feadf4910`.

**Status:** analytical finite-operator construction with exact checks. This is not
native primitive admission, a physical Info selection, or GR closure. No prior
readout is silently promoted to the full action.

## 0. Actual consumer and the premise removed

The [golden-cylinder curvature owner](A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md)
is already integrated. Its four retained histories and three radial settings
produce a calibrated scalar-curvature reading. Its equation (5) realizes the
positive observable `h=det(I-u A)` by inserting that scalar into an effect h/C.
That is a valid existence proof, but leaves a determinant-valued control input.

This continuation removes that particular input: a block unitary consumes the
**matrix** A and scale u. Its exterior-power return computes the determinant.
At u=0 the block is exactly the previously used golden rotation; no new blank
angle or adjustable upper-bound calibration C is needed. The same finite block
also supplies the existing logdet feedback reading at the explicitly declared
value z=1. These are identities of actual programs, not fitted source values.

Consumed separately:

- [Price -> metric -> source lift](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md).
- [Geometric normal-volume proof](A4D_RECORD_NORMAL_VOLUME_SOURCE.md).
- [Full prepared source and joint compatibility](A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md).
- [Actual canonical second AF record](A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md).

The last owner is not rederived or overridden. Its real nonzero complete source
must still enter the native theory on its own carrier. The construction here
uses an auxiliary exterior algebra, not an identification with that AF state.

## 1. A basis-independent unitary with the existing golden blank

Write p=phi^-1, a=sqrt(p), p+p^2=1. Let A be a self-adjoint operator on a
four-dimensional positive tangent space. For a real u assume

    ||u A||op <= 1/2.

Define, without using det(A) or a selected eigenbasis,

    D_u = p (I4-u A),
    C_u = positive_sqrt(D_u),
    S_u = positive_sqrt(I4-D_u),
    U_u = [[C_u,-S_u],[S_u,C_u]] on C4 (+) C4.          (1)

Then `p I/2 <= D_u <= 3p I/2 < I`. The last strict inequality follows from
p<2/3. Both square roots are positive and commute because they are functions
of one D_u. Hence U_u* U_u=I8. At the blank:

    U_0 = [[a I4,-p I4],[p I4,a I4]].                 (2)

Thus (2) is four copies of the actual golden two-coordinate rotation, at the
matrix level. It is not asserted to be the full state-conditioned CAR executor
or its native AF refinement. Functional calculus and exterior realization
remain explicit operations whose physical admission must be proved.

For a fixed lower retained subspace dimension four, a unitary completion of
C_u needs at least four complementary dimensions: `rank(I-C_u* C_u)=4`.
The eight-dimensional dilation (1) is minimal in this specific completion
problem. This is not a minimum dimension of physical spacetime or D0 memory.

## 2. General exterior-return identity, with the full carrier retained

Let U be ANY unitary on C^N and P a rank-r orthogonal projector. Choose an
orthonormal frame e_1,...,e_r of im P and let

    Omega_P=e_1 wedge ... wedge e_r,
    Gamma(U)=direct_sum_(j=0)^N wedge^j U.

Gamma(U) is unitary on the complete exterior space of dimension 2^N. It
preserves grades but no grade is removed from its definition. Multilinearity
and antisymmetry give

    <Omega_P, Gamma(U) Omega_P> = det(C),
    C_ij=<e_i,U e_j>.

Therefore the ordinary return-event probability is

    Pr(return)=|det C|^2=det(C* C).                   (3)

No postselection defines the dynamics: the state Gamma(U)Omega_P retains
all other occupation outcomes. The event is a readout of that full state.
Changing the occupied orthonormal frame changes Omega_P by a phase and
leaves (3) invariant. The identity remains valid on moving frames and
arbitrary smooth unitary germs, with their complete derivatives included.

For (1), N=8,r=4, C=C_u, so

    Pr_u(return)=det D_u=p^4 det(I-u A).                (4)

The fixed probability p^4 at u=0 is produced by the golden blank itself.
It is not a freely fitted calibration. The accessible number-four sector
has binomial(8,4)=70 occupation outcomes; the complete exterior space has
256 states. Four detector-history labels give a 1024-dimensional auxiliary
carrier before any spectator factors. This is not the old native 16-state
Fock representation renamed; an identification would require a real map.

## 3. The feedback determinant and the return probability are the same price

On the original N-dimensional carrier define the literal feedback

    F=P U* (I-P) U P.

On im P it is `I_r-C* C`; on its complement it is zero. When C is invertible,

    J_1(P,U)=-log det_N(I-F)=-log det(C* C).

On the full exterior carrier use the rank-one projector P_Omega. Its feedback
is `(1-Pr(return)) P_Omega`, with 2^N-1 zero eigenvalues. Consequently

    J_1(P,U)
      =J_1(P_Omega,Gamma(U))
      =-log Pr(return).                               (5)

All zero-feedback directions remain in both determinants. Equation (5) is
universal at **z=1**; at general z the two determinant prices need not agree.
For (1), invertibility is guaranteed and

    F_u|im P = p^2 I4+p u A,
    J_u=4 log(phi)-log det(I-u A),
    exp(-J_u)=Pr_u(return).                            (6)

Thus the same block yields the known logdet price and an actual finite
probability whose golden-calibrated value is the desired Jacobian. One no
longer programs an ancilla with a previously computed scalar determinant.
One still supplies the matrix A and constructs the square-root block (1).

Equation (5) does not identify determinant price on a controlled direct sum
with a PF-weighted average of its branch prices. Counting trace, AF trace,
defining-block entropy and conditional event mass remain distinct owners.

## 4. Attach the already-owned four golden cylinders

Use the existing literal weight convention from
`03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean`:
true/F is direct, weight p; false/R is return, weight p^2.

    omega       FF      FR       RF      RR
    weight      p^2     p^3      p^3     p^4
    epsilon      0       1       -1       0

Each history controls Gamma(U_(epsilon u)) from (1). The block-diagonal
controlled unitary retains coherences of the history register. The return
readout is diagonal in that register; that does not dephase the actual state.
For a normalized canonical cylinder state its probability is

    P_j(u)=p^4 sum_omega mu(omega) det(I-u epsilon A_j).

Here j is one setting of the complete normal Parseval family from the parent.
Its settings are summed, not reinterpreted as a new uniform PF preparation.

For arbitrary positive, possibly unnormalized, history/spectator state sigma,
write tau=Tr sigma and b=Tr(sigma E_mix)>0. At both signs of u run the same
preparation and keep the symmetric mean of the two return readings. The full
represented **effect** identity is

    (E_(j,u)+E_(j,-u))/2
       =p^4[I+(u^2 e2(A_j)+u^4 det A_j) E_mix].         (7)

This follows directly from (4) and the degree-four determinant. It holds
against every sigma, including coherences and rank-deficient states. Thus

    Pbar_j(u)=p^4[tau+b(u^2 e2(A_j)+u^4 det A_j)],
    Pbar_j(0)=p^4 tau.                                 (8)

FF/RR outcomes, failure outcomes, and the derivative of the blank are retained.
The **total** mass of all success+failure histories is tau, not (8). Hence this
is a selected event mass of a complete experiment, not an assertion that the
unconditional history normalizer of D0 is curvature-dependent.

## 5. Feed the existing three-setting source, rather than invent a new action

For the same normal Parseval family A_j of the parent and scales
0,t,phi*t, assume `|phi*t| max_j||A_j||op<=1/2`. Set

    N_j=phi^4[Pbar_j(t)-Pbar_j(0)]
                  -[Pbar_j(phi*t)-Pbar_j(0)],
    R_comp=sum_j 2p^3 N_j/(p^4 b_j t^2).                (9)

Preparations may differ across j, as in the parent, but the three readings
and b_j for each j must use the same state/transported state. By (8),
`p^3(phi^4-phi^2)=1` and the exact quartic cancellation,

    2p^3 N_j/(p^4 b_j t^2)=2 e2(A_j),
    R_comp=sum_j[(tr A_j)^2-tr(A_j^2)]=R[q].             (10)

The final equality is precisely the parent's complete normal Parseval/Gauss
identity, not a new assumption about ten selected graph-normal directions.
Noncommuting A_j, overcomplete settings and zero-shape spectators are covered.
The field-dependent normal-frame quartic artifact is removed before variation.

For a genuine joint variation, with p fixed, the full quotient derivative is

    dR_j = (2p^3/(p^4 b_j t^2))
           [dN_j-N_j db_j/b_j-2N_j dt/t].              (11)

The actual unitary and preparation derivatives in dPbar give `dR_j=2de2(A_j)`.
This includes dt, moving mixed-event calibration, raw tau, and frame changes.
On each branch the explicit matrix formula is

    d Pr_u = -p^4 det M Tr[M^-1(A du+u dA)],
    M=I-u A.                                          (12)

Neither [A,dA]=0 nor fixed eigenvectors is required. Formula (12) follows
from the same moving full program, not an independently chosen source.
The exact checker uses a dense dilation with a noncommuting dD and verifies
all seventy amplitude jets, their zero total-mass derivative, and (12)'s
Jacobi counterpart. Shape jets are labelled as shape jets, not metric jets.

For compactly supported metric variations or the parent's closed/boundary
conditions, integration consumes the already-proved Einstein variation:

    d integral R_comp dVol_q
      =-integral G(q)^(mu nu) delta q_mu nu dVol_q.       (13)

The existing phase-complete source lift supplies all ten metric tests.
Equations (9)-(13) remain a calibrated Riemannian geometric reading. They do
not select it as the full native Cost-Info action, solve the link/matter
stationarity equations, or prove Lorentz/spatial refinement.

## 6. Regularity is explicit, but precision and admission are not free

Put d_*=p/2 and e_*=1-3p/2>0. For any Hermitian dD, the derivatives of the
positive square roots solve the Sylvester equations

    C dC+dC C=dD,
    S dS+dS S=-dD.

In Hilbert-Schmidt norm,

    ||dC|| <= ||dD||/(2 sqrt(d_*)),
    ||dS|| <= ||dD||/(2 sqrt(e_*)),
    ||dU|| <= sqrt(1/(2d_*)+1/(2e_*)) ||dD||.           (14)

Proof: diagonalize C only for the estimate; each matrix-entry denominator
is c_i+c_j>=2sqrt(d_*). The construction itself chooses no eigenbasis.
The exterior derivative on the occupied grade is bounded by
`||d wedge^4 U||op<=4||dU||op`, by differentiation of the four tensor factors
and restriction to the antisymmetric subspace. These constants are finite
uniformly in the displayed domain, including eigenvalue collisions.
There is no entropy-support log or missing eigenvalue-gap assumption here.

Equations (14) control the compiler given dA,du. They do not derive those jets
from the native constrained (q,D,b,m) fields. In a refining theory the full
normal family, domain and raw/source error budget still require their own
estimates. Measurement errors in (9) retain the factors b_j^-1 t^-2, and
b_j=0 has no calibratable signal. No fixed finite sample certifies an exact
real-number expectation. The carrier size, number of settings and repetition
budget must be accounted for in an eventual operational realization.

## 7. Native integration boundary after this constructive step

**Removed:** a scalar determinant oracle and an arbitrary large C in the
parent's positive-effect existence construction. The new finite block is
matrix-defined, has the golden blank, and provides both the determinant
price and its return probability with full preparation/operation derivatives.

**Not removed:** a physically admitted construction of the shape-operator
block, controlled matrix functional calculus and the exterior carrier from
the actual AF/CAR primitives. Generic finite-dimensional unitarity is not
native admission. Nor is the choice of the calibrated signed contrast a
consequence of producing its event probabilities.

The known actual second-record source in
`A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md` is not replaced by (13).
Its active- versus passive-record and operator- versus left-readout distinctions
remain in force. A real nonzero retained source must be joined through the
common physical action, not defined as the difference from (13).

The next decisive statement should bind the native **matrix** return/transport
jet to (1), or prove a source-equivalent representation, and derive which
complete price consumes (9). The expensive integration problem is now more
specific than 'find an arbitrary observable having a chosen expectation'.
Repeated finite examples or a fresh postulate S=integral R_comp would not
complete that statement. Original #310/#202/#317 terminals remain open.

## 8. Composition with the concurrent complete AF price, without a new scalar oracle

During this continuation SOURCE advanced to
`1f936ebfa1b3556245ba708fdeebb0a24500ec4b`. Its new
[Jacobian-controlled native record owner](A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md)
constructs the literal AF four-copy W_E for any supplied positive left effect E.
For equal-cost disjoint setting cylinders Q_i and

    E_old=p^2[I+sum_i u_i Q_i],

its second active **complete** old-contract spectral price is exactly

    A_second=B_n+sum_i G(u_i),
    G(0)=0, G'(0)=alpha_n>0.                           (15)

The canonical state, blank price B_n, positive coefficient and full source
calculus are consumed from that owner; they are not rediscovered here.
That price is not the scalar branch-code cost and is not physical Info by
virtue of its name.

There is a finite effect-level way to join (1) with this owner, using only
additional golden cylinder probabilities, without an externally supplied
fair-coin average or multiplication of an unknown probability by a factor >1.
For one setting let u_i=t^2 e2(A_i)+t^4 det A_i. Two fresh golden letters
control the sign epsilon as in Section 4. Keeping all four sign histories,
the compiled signal-return probability is

    P_signal=p^4(1+2p^3 u_i).

Use a golden selector: with direct weight p read this signal, and with return
weight p^2 read the background event 'not FR' in two fresh golden letters.
That event has probability 1-p^3. Preserve both selector branches and all
success/failure outcomes. The actual effect value is then

    e_eff=p P_signal+p^2(1-p^3)
         =p^2(1+gamma u_i), gamma=2p^6>0.              (16)

Outside the addressed normal settings use A=0, which gives exactly e_eff=p^2.
Thus on the old left algebra the composite effect is

    E_eff=p^2[I+gamma sum_i u_i Q_i].                   (17)

It remains strictly between zero and identity because it is a convex mixture
of strict effects in the prescribed domain. No conditional event is discarded.
At every blank address it is the literal golden effect; gamma is fixed by
these actual branch weights, not fitted to an Einstein source.

**Precise compositional scope.** Equation (17) is an effect identity. Feed this
operator, as a coefficient, into the existing owner's canonical W_E. Since
it is in the same old left algebra, the owned AF frame, complement and
right-module identities apply. Equation (15) gives the exact substitution

    A_second,eff=B_n+sum_i G(gamma u_i).                (18)

This supplies an explicit matrix-defined candidate on that actual AF
spectral-price family. It is NOT a proof that running the auxiliary compiler
and then replacing its Stinespring realization by the canonical W_E preserves
all histories or their physical cost. Equal effects alone do not imply equal
instruments, complete preparations or actions. Such a cost-preserving native
compilation is still an admission theorem, not an algebraic consequence of
(17). The additional controller's preparation and archive cannot be omitted
from a claimed implementation of the complete physical process.

Within the declared W_E family, (18) nevertheless gives a definite positive
curvature coefficient of ONE complete price, without a signed subtraction
of prices or a freely added remainder. With the parent's Gauss identity,

    A_second,eff
      =B_n+(gamma alpha_n t^2/2) R[q]+Rem_eff,
    Rem_eff=gamma alpha_n t^4 sum_i det A_i
          +sum_i[G(gamma u_i)-gamma alpha_n u_i].      (19)

For |gamma u_i| in the parent's safe interval and M2=sup|G''|,

    |Rem_eff| <= gamma alpha_n t^4 sum_i|det A_i|
                              +(M2 gamma^2/2)sum_i u_i^2,
    |dRem_eff| <= gamma alpha_n |d(t^4 sum_i det A_i)|
                              +M2 gamma^2 sum_i |u_i||du_i|.         (20)

Here gamma and n are fixed; moving preparation masses and n-dependent
coefficients require the existing owner's additional source terms. There is
no new assumption that the source can be read from gate values alone.
For bounded shape and shape jets and fixed t, the error is O(t^4). The old
positive alpha_n depth bounds and p^(2(n-n0)) rate carry through with factor
gamma. These are operator-depth statements, not spatial mesh convergence.

If the separate geometric integration law dVol_q is supplied, the metric
source of (19) includes BOTH

    (B_n/2) q^(mu nu) - (gamma alpha_n t^2/2) G(q)^(mu nu)

plus the full remainder/volume/preparation terms. The blank contribution
has not vanished. For field-dependent coefficients, derivatives of that
coefficient cannot be dropped. This is stronger than another isolated
curvature observable, but still not a selected physical D0 action or an
exact all-scale Einstein equation.

## 9. Evidence and context

The associated checker has 59 named exact conditions. They include the golden
blank, all four cylinders, all ten independent symmetric SHAPE slots,
noncommuting shapes, dense eight-mode unitarity, all 70 occupation probabilities,
a true noncommuting unitary jet, both complete feedback determinants, raw
coherent preparation and calibration/scale/blank derivatives. The explicit golden effect composition and its inherited complete AF-price
coefficient are also checked. Six actually changed programs fail mathematical tests. Ordinary and optimized Python
outputs agree. These finite tests supplement, not replace, the general proofs.
No new Lean declaration, independent full scientific review, or whole-repository
local replay is claimed. Repository source pins are checked separately by the
narrow certificate. Historical proofs and receipts are not rewritten.

Exterior-power determinant amplitudes and unitary dilations are established
mathematics. Relevant context is Terhal--DiVincenzo,
`https://arxiv.org/abs/quant-ph/0108010`; the inherited tube/geometric source
context is Willison, `https://arxiv.org/abs/0904.3224`. No world-first claim for
these general tools is made. The contribution here is their explicit golden
composition and differentiated use in the already-owned cylinder consumer.
