# Native exterior matter: the linear observer readout and its joint derivative

Date: 12 October 2026. Parent: existing Draft #310,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input SOURCE: `e73cd37fda5028609eb412e17751390d2a3bf9f7`, continuing
`48d762ae66ca5f423cd9e40231aa8067a4d95dba` without changing its consumed owners.
Canonical main checked: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.

**Result:** on the timelike first-grade sector of the actual sixteen-component
exterior matter field, a fixed full-O(1,3)-equivariant linear vector readout is
unique up to scale. It supplies the argument of the already owned observer
pairing. The pairing, its complete joint differential in the ten Gram and
sixteen matter coordinates, and the induced weighted-operator differential
are explicit below. This is a kinematic construction and conditional heat
calculus. It does not select a physical constitutive/heat law or complete T0.

## 1. Literal carrier and the exact linear-readout class

Consume the complete [joint quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md):
at each site retain invertible raw solder F, Lorentz links and affine shifts,
and arbitrary real exterior matter psi in grades 0,1,2,3,4 of dimensions
1,4,6,4,1. Its quotient coordinates are

    q = F eta F^T,    D_e = F_x U_e F_y^-1,
    b_e = F_x a_e,    m = rho(F) psi.

The actual local gauge acts by `F -> F Lambda`,
`psi -> rho(Lambda^-1) psi`. Its `IsRoleLorentz` permits the full O(1,3).
Use the explicit coordinate order A,B,C,D; this is not an implicit change
to the enumeration order of `Role`. The representation is the existing
exterior lift, not a sixteen-dimensional spinor representation.

The classified class is a **fixed real linear map**

    T : direct_sum_(k=0)^4 exterior^k(R^1,3) -> R^1,3,
    T rho(Lambda) = Lambda T for every Lambda in O(1,3).

Coefficients do not depend on a coframe orientation, a preferred vector,
other matter grades, or a recorded apparatus. This assumption is essential.
With P1 the grade-one projection,

    Hom_O(1,3)(exterior^* V, V) = R P1.                    (1)

**All-group proof.** Independent diagonal sign flips belong to O(1,3).
Output coordinate i has character epsilon_i; a wedge basis vector with
occupied subset S has character product_(j in S) epsilon_j. Equality for
all sign choices forces S={i}. Thus T is diagonal on grade one and zero on
every other grade. Spatial rotations equate the three spatial diagonal
coefficients; a nonzero time/spatial boost equates them with the time
coefficient. Conversely P1 commutes with every exterior lift. This proves
(1) for the full group, not just a finite sample.

For SO+(1,3), and also for the full determinant-one Lorentz group,

    Hom_SO+(1,3)(exterior^* V, V) = R P1 + R P3,          (2)

where in an oriented wedge basis `P3[i,complement{i}] = eta_ii*(-1)^i`.
The volume contraction identity gives
`P3 rho(Lambda) = det(Lambda) Lambda P3`. Six exact proper boosts/rotations
give a 384-by-64 constraint matrix of rank 62, an upper bound of two on the
all-group Hom space. P1 and P3 are independent all-group witnesses, proving
equality. Adding the four coordinate reflections gives rank 63 and rejects
P3 as an ordinary full-group vector. These ranks support the proof; they are
not extrapolations from approximate floating-point matrices.

Two qualifications prevent an overbroad selector claim. A readout depending
on `sign(det F)` can dress the axial P3 into a full-gauge-invariant quotient
vector, and is outside the fixed T class. Moreover the positive rank-one
pairing made from P3 alone is full-Lorentz covariant: its extra determinant
sign cancels in the square. Thus (1) does **not** classify every nonlinear
matter readout or every possible positive pairing.

## 2. Constructive positive pairing and its precise domain

For a nonzero multiple of P1 set

    v = P1 m = F P1 psi,    A = q^-1,    u = A v,
    k = v^T A v > 0.

There is a nonempty open timelike sector; it is not all native matter. The
zero field, null v and spacelike v are not discarded from the original
carrier, but this observer construction is unavailable there. Set

    Q(q,m) = -q + 2 v v^T/k,
    G(q,m) = Q^-1 = -A + 2 u u^T/k.                      (3)

Writing `j=F^-1 v`, `n=j/sqrt(k)` gives `n^T eta n=1` and exactly

    G = F^-T observerMetric(n) F^-1,
    Q = F [-eta + 2 n n^T] F^T.                         (4)

The existing `A4DObserverPositiveExterior.observerMetric_posDef` and exterior
Gram positivity imply G and Q are positive definite. Direct multiplication
using qA=I and v^TAv=k proves QG=I. The rank-one determinant lemma gives

    det Q = -det q > 0.                                 (5)

For every invertible coordinate map R the construction obeys
`Q(RqR^T,Rv)=R Q(q,v) R^T` and inverse congruence for G. In particular it
descends from the actual raw gauge to the existing complete joint quotient.
The nonzero scale of the linear reading cancels, as does `v -> -v`.
This supplies a timelike **line** for the positive pairing; it does not
derive a physical choice of future. No four-coordinate recorded apparatus
is identified with the full sixteen-component native matter field.

For fixed v!=0, (3) is a bijection from Lorentz q with v timelike to all
positive Q: the inverse is `q=-Q+2vv^T/(v^T Q^-1 v)`. It does not make q
canonical or remove any native quotient coordinate.

The already studied geometric compound heat candidate becomes

    W(q,m)|grade k = omega C_k(G),
    omega = sqrt(abs(det q)) = sqrt(det Q),              (6)

where C_k is the k-th compound, including C_0=1. Every grade and all sixteen
components remain in the positive pairing. Without omega, its pullback by
rho(F) is exactly the existing observer exterior pairing; with omega it is
`abs(det F)` times that pairing. The factor in (6) is the pre-existing heat
candidate's density convention, not a new result of Lorentz symmetry.
Indeed `det W = omega^16 (det G)^8 = 1` on the whole exterior fibre.
This determinant identity does not make its heat spectrum constant.

## 3. The complete joint first derivative

Let `dot q=V=V^T`, `dot m=xi` retain **all sixteen** matter slots, and put
`w=P1 xi`. Ordinary matrix differentiation on k>0 gives

    dot A = -A V A,
    dot u = A w - A V u,
    dot k = 2 u^T w - u^T V u,

    dot Q = -V + (2/k)(w v^T + v w^T)
                   - (2 dot k/k^2) v v^T,              (7)
    dot G = A V A + (2/k)(dot u u^T + u dot u^T)
                   - (2 dot k/k^2) u u^T.

Consequently `dot G=-G dot Q G` and
`dot omega/omega=Tr(A V)/2`. For each compound entry the remaining
derivative in (6) is the sum of its minor cofactors times the corresponding
entries of dot G. This cofactor formula works in every degree and does not
require a nonsingular individual minor.

These are genuine derivatives along q/m curves, not differences between
independently frozen observers. The companion Lean capsule proves the
generic contraction derivative and the rank-one Q-entry derivative with
`HasDerivAt`; (7)'s matrix-inverse simplification and its assembly over
sites are the analytic proof here and the exact controls, not a new supported
Lean matrix-inverse theorem.

On the rest base `q=eta`, `v=e_A`, in A,B,C,D order, `Q=G=I` and (7) reads

    dot Q_AA = V_AA,
    dot Q_Ai = -V_Ai + 2 w_i        (i spatial),
    dot Q_ij = -V_ij               (i,j spatial).       (8)

The amplitude w_A cancels. At fixed q the observer derivative has rank 3
and kernel dimension 13 in the actual sixteen matter slots: twelve other
grades plus the amplitude direction. At fixed m the ten-slot q derivative
has rank 10. On the complete 26-dimensional (q,m) chart its rank is 10 and
kernel dimension 16. Equation (3)'s explicit inverse proves these ranks on
the whole timelike sector, not only at rest. These kernels are only kernels
of the **pairing readout**, not gauge directions of the native field.

For a positive-pairing price whose derivative is `Tr(Z dot Q)`, Z symmetric,
the exact rest-base joint covector is

    coefficient(V_AA) = Z_AA,
    coefficient(V_Ai) = -2 Z_Ai,
    coefficient(V_ij) = -2 Z_ij        (i<j spatial),
    coefficient(V_ii) = -Z_ii         (i spatial),
    coefficient(w_i) = 4 Z_Ai,       coefficient(w_A)=0. (9)

Off-diagonal slots use one symmetric packed coordinate, hence the factors
two. Omitting matter motion loses the last nonzero terms. Omitting observer
motion changes (7) even with the same q/m tangent.

## 4. The actual constrained carrier is retained

The complete joint quotient also has `D_e q_y D_e^T=q_x`; admitted kinematic
tangents satisfy

    dot D_e q_y D_e^T + D_e V_y D_e^T
      + D_e q_y dot D_e^T - V_x = 0.                  (10)

The matter slots and affine shifts have no further kinematic restriction.
Equations (7) are pulled back to this tangent space at both endpoints.
They neither freeze links for arbitrary nonconstant V nor infer a unique
physical metric-source representative modulo the edge conormal.
On a constant flat configuration, common constant V at every site and
`dot D=0` do satisfy (10); arbitrary matter variations remain kinematically
allowed. Native dynamical preparation/field equations remain additional.

If the transported physical metric `hat q=B(D) q B(D)^T` is used, its
consistent matter reading is `hat m=rho(B)m`, `hat v=Bv` on det B!=0.
Then `hat Q=B Q B^T` and
`dot hat Q=dot B Q B^T+B dot Q B^T+B Q dot B^T`.
The incoming-link derivatives in dot B cannot be dropped. Neither raw
nondegeneracy nor k>0 proves det B!=0; the previous quotient already gives
centered-frame degeneracy controls. This route does not replace raw solder
by an independently supplied centered coframe.

## 5. Conditional complete weighted-operator and heat derivative

For the previously constructed positive weighted binding, retain a possibly
moving, degree-raising differential d on the full finite archive. Put

    delta = W^-1 d^T W,    S = W^-1 dot W,
    dot delta = W^-1 dot d^T W + delta S - S delta,
    mathcal D = d + delta,
    dot mathcal D = dot d + dot delta,
    K = mathcal D^2,
    dot K = dot mathcal D mathcal D + mathcal D dot mathcal D. (11)

This is ordinary finite-matrix calculus, with all site/degree/coefficient
rows retained. No d^2=0, flat-link condition or fixed eigenvectors are
required. At fixed beta>0 and fixed finite dimension M the trace identity is

    dot H = -beta Tr(exp(-beta K) dot K)/M,
    dot B_total = dot H + dot R_remaining.              (12)

The moving-pairing terms, all dot d terms and the same-path remaining price
must be kept. If beta or normalization moves, their product-rule terms are
additional. Equations (11)-(12) do not identify this heat candidate with the
native physical price and do not determine the remaining price R.

On `q(t)=exp(2t)q`, with either fixed v or any nonzero rescaling v(t), (3)
gives `Q(t)=exp(2t)Q`. Therefore (6) gives
`W_k(t)=exp((4-2k)t)W_k`. If d is unchanged, the existing graded-similarity
proof gives `K(t)` similar to `exp(-2t)K` and hence

    dot H = 2 beta Tr(K exp(-beta K))/M > 0             (13)

when d is nonzero. Native realization of that path and compensator
`dot R_remaining=-dot H` remain obligations. Deriving the observer from
matter has **not** removed the conditional radial obstruction.

## 6. Literal flat forward-difference witness, including matter motion

For constant Q and the actual counting forward exterior differential the
full sixteen-fold mode spectrum is
`lambda_p=p* G p`, `p_r=L(exp(2 pi i k_r/L)-1)`. It includes all zero modes.
At rest let

    Z = (beta/L^4) sum_p exp(-beta |p|^2) Re(p p*).

Then `dot H=Tr(Z dot Q)` and (9) supplies all ten q slots and all sixteen
matter slots. This formula retains the forward stencil; replacing it by a
centered/continuum stencil would change its off-diagonal response.

For an exact L=2 witness at the **mathematical** value beta=log 2, set
`x=2^-16`, `a=x(1+x)^3`, `c=x^2(1+x)^2`. All four diagonal entries of
`Z/beta` equal a and all six off-diagonal entries equal c>0. Thus, in the
packed q slots and the full matter field,

    dot H/beta = a (V_AA-V_BB-V_CC-V_DD)
                  -2c sum_(i<j) V_ij
                  +4c (w_B+w_C+w_D).                 (14)

Every one of the sixteen Fourier characters is checked with the full
sixteen-dimensional exterior matrix, i.e. all 256 finite cochains. The
compound-pairing differentiation in (11) produces exactly the scalar
`dot lambda I_16` in every character. Equation (14) demonstrates a real
matter contribution at fixed q in this binding. It is neither a fitted
source nor evidence selecting beta=log 2 physically.

## 7. Concurrent factor and multiplier notes: the tangent test

The concurrent [factor note](A4D_PAIRING_Q_FACTOR_JET.md) and
[multiplier note](A4D_CONSTRAINT_MULTIPLIER_SOURCE.md) were added in published
SOURCE `e73cd37f` during this calculation. They declare a session/toy check
and a change of reading, rather than native source theorems. Their preserved
files are not consumed as proof of a physical heat law or a source.

In particular positive Q in (3) cannot have spectrum `{1,-1}` on k>0.
A tilt of v also need not preserve its spectrum. At `q=eta`,
`v=(cosh t,sinh t,0,0)`, its two active eigenvalues are `exp(2t),exp(-2t)`.
This is not an isospectral rotation of a positive pairing.

For `C_e=D_e q_y D_e^T-q_x`, any edge multiplier contributes the conormal
`sum_e Tr(Lambda_e dot C_e)`. On **every** actual tangent of (10) this is
identically zero, regardless of Lambda. An ambient endpoint derivative can
be redistributed by multipliers; a nonzero constrained derivative cannot
be converted into a pure conormal. The full endpoint and link stationarity
equations, plus any other owned price/source, are still required.

Here is an exact nonisotropic factor witness in the present binding:
at every site take

    q=diag(4,-1/4,-1,-1),    v=(2,0,0,0),    D_e=I,
    V=diag(8,1/2,0,0),      dot m=0,       dot D_e=0.

The full curve has q(t)=diag(4 exp(2t),-exp(-2t)/4,-1,-1),
constant v and D. It is timelike and satisfies all edge constraints exactly;
`dot C_e=V-V=0`. Equation (7) gives
`Q=diag(4,1/4,1,1)`, `dot Q=diag(8,-1/2,0,0)`.
For the literal L=2 forward Hodge spectrum at beta=log 2 put
`x0=2^-4`, `x1=2^-64`, `x2=2^-16`. All 256 cochains give

    dot H/beta = [8 x0(1+x1)-128 x1(1+x0)](1+x2)^2/16 > 0. (15)

Thus this genuinely constrained factor derivative is not a multiplier
conormal. It is the same positive-Hodge obstruction, conditional on this
preparation/binding, that requires the complete remaining-price/source
response for stationarity. A new physical admissibility law could exclude
this path, but must be derived on this carrier; an AF increment ratio alone
does not impose such a q/D law. No whole-core no-go follows.

## 8. Evidence and the remaining obligation

The companion exact checker replays its immutable ledger, pins consumed
owner/capsule/compiler bytes, checks all 26 q/m directions on nonrest
timelike data, every exterior degree, non-diagonal metric data, all 256
cochains in the L=2 witness, transported-frame derivatives and (10). It
executes hostile controls for the proper/full-group distinction, axial
pairing loophole, invalid domains, omitted normalization and matter terms,
packed-slot factors, lost density, dropped degrees, false future selection,
and a frozen observer. Compiler evidence contains genuine generic
`HasDerivAt` propositions and their axioms. The Hom classification, full
matrix construction and trace differential are analytic/exact research;
no new supported CORE owner is claimed.

The next required proof is physical admission of a complete same-carrier
preparation/constitutive price on `(q,D,b,m)` and its full constrained
covector, including link/affine effects and R_remaining. A merely positive
formula cannot supply that law. Timelike-domain and future-orientation
admission are also explicit physical obligations. All original #310/#202/
#317 exact-root, raw-owner, Ward, soundness/recovery and GR terminals remain
open; no lifecycle or public claim is promoted by this component.
