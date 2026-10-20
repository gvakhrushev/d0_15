# Preserving Einstein roots is weaker than preserving their scalar source

20 October 2026. Bounded mathematical continuation for existing PR #334.
Repository inspected at `20d976647fa52e247d15139d3f4f14351f175b70`.
This note proposes no native action, Euler oracle, new field, reference law,
or change of the admitted variations. It separates a legitimate mathematical
escape from the already excluded scalar-source completion, then tests the
actual available record against that escape.

## 1. Exact local equation-equivalence criterion

Let U be a contractible open finite real field chart, J=J2 in C2(U), and
M in C1(U,GL(n,R)) act on covector columns. Set j=dJ and alpha=M j.
There exists S in C2(U) with dS=alpha exactly when alpha is closed:

    (partial_l M_i^k-partial_i M_l^k) J_k
      + M_i^k J_kl-M_l^k J_ki = 0,       for every i,l.       (1)

Necessity is equality of mixed partials; sufficiency is the Poincare lemma
on U. On a smaller ball no global topology is involved. Invertibility then
gives dS=0 iff dJ=0 throughout that same neighborhood. A positive definite
matrix field or pointwise matching of Hessians alone does not imply (1).

At a target root y*, the derivative of M multiplies j(y*)=0, so

    H_S=M_* H_J,
    M_* H_J=H_J M_*^T,
    ker H_S=ker H_J.                                      (2)

These are necessary root conditions, not sufficient off-root integrability.
The kernel statement matters before making any gauge quotient: a stabilizer
cannot lift a true target Hessian kernel while retaining invertible equation
equivalence. A quotient may be taken only for already justified gauge
directions, not to delete a negative or matter direction.

If M_* is symmetric positive definite and H_J has a negative direction,
M_*H_J cannot be a positive semidefinite Hessian. Indeed it is similar to
M_*^(1/2) H_J M_*^(1/2), which has the inertia of H_J. Equivalently, a negative
eigenvector v of H_J has v^T M_* H_J v=lambda v^T M_*v<0. The latter argument
also excludes M_* with positive definite symmetric part. Thus a positive
information metric used merely as a source preconditioner does not turn
this saddle into a minimum. An invertible multiplier with other signs can.

A genuine field-coordinate pullback is different. If S=J composed with a
local diffeomorphism Phi, then at corresponding roots

    H_S=(D Phi)^T H_J (D Phi).

This congruence preserves inertia. Its source involves dJ evaluated at
Phi(y); it is not permission to replace the action by an arbitrary
integrable M(y)dJ(y).

## 2. A necessary hostile control: the matrix escape really exists

In two variables let J(x,u)=-xu-u^2. With the auxiliary Euclidean coordinates
used only for this control, define S=J+|dJ|^2/2. Exactly,

    H_J=[[0,-1],[-1,-2]],             det H_J=-1,
    dS=(I+H_J)dJ,
    M=I+H_J=[[1,-1],[-1,-1]],         det M=-2,
    H_S=H_J+H_J^2=[[1,1],[1,3]]>0.                    (3)

The unique critical point is unchanged and becomes a strict minimum. Thus
the scalar-source ridge theorem does not exclude all equation-equivalent
prices. Formula (3) is NOT a native price construction: the Euclidean norm
and access to the Euler derivative have not been supplied or paid by D0.
It is a countercontrol against overstating the previous no-go.

More generally the formal control J+alpha|dJ|^2/2 has multiplier
I+alpha H_J. At a nondegenerate root sufficiently large positive alpha
turns every negative eigenvalue lambda into lambda+alpha lambda^2>0;
the multiplier remains invertible nearby. With a kernel this alone proves
neither a strict minimum nor a justified quotient.

There is also a useful warning about fitting M after the fact. Assume
J and S are C3 for this ancillary C1-multiplier construction. Near a
nondegenerate root, p=dJ is a local coordinate. For such an S with the
same root and invertible Hessian, put f(p)=dS(y(p)). Then

    f(p)=[integral_0^1 Df(sp) ds] p.

The bracket is invertible near zero. Therefore post-hoc local M existence
can be almost vacuous at an isolated root. The scientific task is to derive
the actual complete price and its equation-equivalence on the specified
field domain, including boundary, kernel and preparation data.

## 3. Same cleaned record: preserve the saddle or add spurious roots

Consume the independently checked
[full-record tangent theorem](FULL_RECORD_TANGENT_AND_MATCHED_INFO.md),
SHA-256 `9a233771fbb052057c3d3dd81b5592a67eae22b4c17ac32b17ecc24d385d585b`.
For the actual three-query cleanup and any fixed admitted k stopped tape,
including all fine work, clock, and fixed oldRIGHT-entangled input, it gives

    sigma_y=sigma_*+t(y)L+O(t(y)^2),                    (4)

with the SAME sigma_* and L on the whole common-null stratum Sigma. At Sigma
the one-trial QFI is 16 dt tensor dt; the fixed-k stopped QFI is
(16/q_k) dt tensor dt. The complete output has no hidden first-order work
direction. At a stationary root Dt=0, every smooth matched divergence of
this output has zero field quadratic form. Its finite reverse CQ KL is
8t^2/(q_k ln phi)+O(t^3); a singular forward KL is not a finite stabilizer.

Here is the stronger equation-equivalence consequence. Suppose the declared
field chart is encoded in this W(y), the input and reporting interface are
fixed, and Phi is ONE fixed Frechet C1 functional of the resulting complete
state, with no additional explicit field or moving-price dependence. Add it
to the actual fixed-k price F_k. On Sigma the owned source theorem and (4)
give, for ALL directions in that declared field chart,

    d(F_k+Phi(sigma_y))=(kappa_k+c) dt,
    c=D Phi(sigma_*)[L],                              (5)

where c is constant along Sigma. The accepted original shared-link/coframe
curve has t(a,0)=0 and t_u(a,0)=g(1-a), g>0. Hence precisely:

* If kappa_k+c is nonzero, the constant-ridge argument still gives both
  increasing and decreasing nearby values. There is no local minimum.
* If kappa_k+c=0, (5) vanishes in every declared ambient direction throughout
  Sigma. This introduces spurious critical fields wherever DJ2 is nonzero.

The latter fields are owned, not hypothetical. The original same-family
fixed-collar perturbation H_s=H_*+s chi with its original Cartan links has
f_i=q_i=0 for every s, while an interior unit spike gives the actual coframe
row DJ2[partial_(v_v^+(z))]=2 C_h s/h^3 !=0. Thus, on this declared chart,
invertible dS=M dJ is impossible in the cancellation case. The simple
a!=1,u=0 curve also has a nonzero shared-link target source.

Consequently a smooth fixed revaluation of this same final record cannot
both stabilize the known root and preserve the target critical set. A
matched divergence is the special case c=0: it preserves the saddle.
Replacing the price by a matched divergence alone makes all of Sigma
minimizing, including the displayed off-shell fields.

The all-directions qualifier is essential. If only a pullback to a slice is
known to vanish, one may not infer a full critical point or exclude a full
matrix that mixes transverse covectors. Here (4)-(5) apply to all field
dependence actually passed through the supplied W, not to independently
moving upstream material/programme inputs. They do not assert that a larger
physical Book price or preparation register is a fixed functional of sigma.
Likewise an adaptive lower envelope need not be differentiable; this theorem
concerns an actual fixed branch or a separately proved smooth fixed record
valuation. The existing adaptive descent result remains separate.

## 4. What an actual additional record would have to pass

For two strictly positive normalized laws P(y),Q(y) agreeing at a root, a
matched KL in base phi has the exact quadratic form

    K=(1/ln phi) A^T diag(1/P_*) A,
    A=D(P-Q)|_*.                                      (6)

If the penalty is meant to vanish on a family of target roots, P=Q must hold
on that family; A kills its tangents. A fixed anchor matching one root is
not evidence of this property at other roots. Vanishing of a source at all
roots, moreover, is weaker than the closed invertible factorization (1).

Given an independently paid record and reference, the smallest relevant test
is to differentiate their actual mismatch on the existing admitted field
directions. It must provide a nonzero second form on every negative direction
left uncorrected by the base price, while the TOTAL Hessian must satisfy (2)
and the TOTAL source must satisfy (1). For example if K is nonnegative and
v belongs to ker A with H_base[v,v]<0, stabilization already fails. No rank
scan or claim that positive Fisher information selects the action is needed.
Nor may H_base be replaced by a scalar H_J: for the actual stopped query,
H_t=gamma_h(H_J-Q_F), with the owned nonnegative Q_F term retained.

If an actual freely varied reference parameter z has derivative B=D_z Q,
stationary elimination of the matched quadratic cost gives

    K_eff=(1/ln phi) A^T[D-D B(B^T D B)^+B^T D]A,
    D=diag(1/P_*),                                   (7)

on the permitted normalized tangent spaces. This is the exact weighted
least-squares Schur form; the pseudoinverse merely treats redundant reference
coordinates. If reference variations span A, the form vanishes. The owned
complete-Book self-code theorem proves the stronger exact zero envelope for
its freely matched conditional law, retaining every label. A constrained
future/reference law could avoid this cancellation only if that constraint
and its whole cost were actually supplied.

The inspected native coherent AF preparation owner likewise supplies an
actual relative-entropy residual and its Gibbs stationary preparation. Its
residual vanishes along the freely optimized preparation; the surviving
terminal envelope 6-ln Z(E)/ln phi is a separate geometric source. The owner
does not identify its full derivative with an invertible transform of DJ2,
and explicitly excludes summing other preparation stages. This is not the
missing complete physical-price theorem.

The separate homogeneous full128 Jones score can have a nonzero tangent;
its frozen-anchor KL has born dark support and can be infinite, while its
support-safe Hellinger score is well defined. Those facts do not transport
that experiment to the current normalized curved field/preparation chart
or establish (1). No different-carrier rank is used here as a parent result.

## 5. The actual live CAR actuator supplies the next minimal record test

There IS a newly owned same-primary-family access path beyond the cleaned
null record. The existing paid CAR word changes the live top amplitude by
a nonzero delta and the original inverse-PF query reads

    q_i(H)=rho_z^-1 s_cal^2(2 v_4 delta/h-H_z delta^2/h^2).

The original matter, calibration s_cal, true density, addressing, preparation
and full readiness/abort record are as specified by its owner. Write

    zeta=p+sigma p^2 eta'^2 q_i,
    B=4 zeta^2(1-zeta^2),          1/2<zeta<2/3,
    C=sigma p^2 eta'^2 rho_z^-1 s_cal^2 delta^2/h^2 !=0.

At fixed supplied probe data its exact metric response is

    B_H=-8 C zeta(1-2 zeta^2) !=0.                    (8)

With genuine fixed readiness r>0 the complete coarse law is
(r B,r(1-B),1-r); its H Fisher coefficient is

    I_H=r B_H^2/[B(1-B)]>0.                           (9)

The possible identically absent abort at r=1 is omitted only from the Fisher
sum, not from the defined instrument. Thus an actual admissible probe can
restore a first-order metric response; (8) is not postprocessing of (4).
Its field-dependent amplitude binding and all preparation costs remain due.

This closes sensing, not equation-equivalence. Against a fixed reference
H_ref, the binary law is strictly monotone on this chart, so a matched score
vanishes exactly when H_z=H_ref,z. That tests a metric mismatch, not the
Einstein field equation. If boundary data are allowed to vary, different
exact Einstein solutions can have different such responses. With fixed
matter and fixed Dirichlet collar the owned finite Einstein Poisson solution
is unique; no pair of distinct roots under those same data is asserted.
In that case using its response as a target requires an independently owned
way to produce that reference, rather than an oracle for the unknown root.

The next genuine test is therefore concrete: derive the actual future
comparison/reference and its COMPLETE price, include its moving-input,
controller, clock and information derivatives, then test (1)-(2) on the
existing original field chart. The available actuator supplies access for
this test; none of the inspected owners yet supplies the required complete
root-preserving price. This is a scoped source inspection, not a universal
impossibility theorem for native D0 dynamics.

### 5.1 A nonzero information direction on the actual saddle slice

The same paid actuator can be substituted directly into the original saddle
slice, without using the separate homogeneous Jones fixture. Retain one fixed
calibration s_cal>0 and use the operational coframe

    ehat_0(a)=s_cal^-1 diag(1,a,1,a^-1)

at the central site, with other coframes fixed at s_cal^-1 I, original null
eta_01=eta_10=1, eta_22=eta_33=-1, and the same shared link U_(0,2)(u).
The coframe determinant is independent of a. At s_cal=1 this is exactly the
reviewed slice. The owned fixed calibration transports the price with its
declared query parameters; with calibrated gains this is an exact off-shell
pullback. The slice therefore retains its form H_t=[[0,-g],[-g,-2gD]] with
the actual g,D>0 and its negative determinant. No Hessian rescaling is
inferred merely from a first-source equality. The calibration is fixed under
the whole variation, not fitted to the measured field.

These coframes and eta are the owner's NULL geometric representation. The
four-mask preparation and actuator below are in its ORTHONORMAL REST CAR
basis, with the actual map

    T=[[1,1/2],[1,-1/2]] direct_sum I2,
    T^T eta_rest T=eta_null,
    e_raw=rho^-1/2 T ehat,         U_rest=T U_null T^-1.

The original epsilon/Hodge orientation is pulled back exactly as in the
primary domain owner. The rest masks must not be read as Euclidean null
masks: that would change the clock, norm, actuator and possibly the star
sign. The displayed inverse metric is a tensor calculation in null
coordinates; the native CAR operation and positive Gram stay in REST.

Start with the actual constant normalized four-mask CAR state with positive
complement slack. At site 0 the owned W^(2k), or six-letter compiled word,
changes only its top component by a fixed small nonzero delta. At that site
every top forward difference is -delta/h. The inverse metric is EXACTLY

    ghat^-1=s_cal^2 [[0,1/a,0,0],[1/a,0,0,0],
                    [0,0,-1,0],[0,0,0,-a^2]].

Thus the actual inverse-PF local query is

    q_i(a)=s_cal^2 delta^2/(rho_0 h^2) (2/a-1-a^2),
    q_i(1)=0,       partial_a q_i(1)=-4 s_cal^2 delta^2/(rho_0 h^2),
    partial_u q_i=0.                                  (10)

The other affected backward neighbors have one changed forward derivative;
their coframes are held along this slice, so their q_i have no a or u
derivative. All their actual baseline responses are nevertheless retained.
Taking the native rotation sufficiently small keeps every affected query
in its same open chart. The fixed current, oldRIGHT Gram, all CAR masks and
original shared-link stencil are preserved. This actuation is a diagnostic
future experiment on each supplied field, not a claim that the actuated
matter still solves Einstein's equation.

For the original native 8D two-tick block the FIXED minus preparation has
cut probability B=4b(1-b), b=(p+sigma p^2 eta'^2 q_i)^2. This is independent
of the geometric AF input E, not an E-dependent eigenvector preparation.
The original full retained compression is
(1-2b)[[1-E,-E],[-E,1-E]]; its minus eigenvalue is 1-2b, proving the claim
without discarding the plus rail or any other output. Consequently

    L=B_* =4p^3,
    B_a=-32 sigma p^6 eta'^2 s_cal^2 delta^2/(rho_0 h^2) !=0,
    B_u=0.                                            (11)

Use the actual fixed positive address masses omega_x, not a uniform prior
or postselection. Here the address index covers the ENTIRE normalized
retained address law, sum_x omega_x=1, including all inactive and unchanged
addresses. Equivalently their remaining constant mass may be kept as one
additional coarse outcome. Omega_0 is the total genuine mass of the central
address class, not its renormalization among the active sites. The retained
joint coarse law omega_x Bernoulli(B_x), optionally preceded by genuine
fixed readiness r, has the matched base-phi
likelihood statistic whose exact slice Hessian is

    K_B=diag(K_aa,0),
    K_aa=r omega_0 B_a^2/[ln(phi) L(1-L)]>0.            (12)

All changed-neighbor baselines and the readiness abort are included; their
slice derivatives vanish. If a real addressed preparation is used instead,
its admission/address/preparation cost is explicit and omega_0 is not
silently set to one. Formula (12) is a scalar statistic computable from the
retained full record. It is not claimed to be the selected physical Info.
The finer full record has at least this Fisher information when its metric
is defined; a born-support singular full KL need not be finite. No fine
output is erased or removed from the complete price by using this statistic.

This is precisely an information direction absent from the cleaned final
tape. If the actual complete price were independently proved to add exactly
this statistic with no other second sources, its slice second form would be

    [[K_aa,-kappa g],[-kappa g,-2kappa gD]].

For kappa<0 it is positive semidefinite exactly when

    K_aa >= -kappa g/(2D),                             (13)

and positive definite for strict inequality. For kappa>0 this single
coframe-direction statistic cannot repair the negative u-u entry. Equation
(13) is a test of the one actual coefficient (12), NOT permission to choose
a multiplier, number of probes, readiness or information value to satisfy
it. Every repeated experiment, preparation and retained output must be paid,
and all its field-dependent first and second sources included. No assertion
that (13) holds for the full native price is made.

The positive result is therefore narrow and useful: an already owned word
provides the missing first-order coframe sensing on the SAME saddle slice.
What remains is the actual compulsory comparison law, its full residual
price, and preservation of Einstein roots through (1). Sensing by itself
does not supply any of those three premises.

## 6. Provenance and narrow verification

Repository paths are relative to the inspected root. The following blobs
pin exactly the consumed content:

* `02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md`,
  blob `d9702cefb97f8da9f3435c5c88b26943ce64e838`, section 5: the same-collar
  off-shell Sigma control and its nonzero original coframe row.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_CAR_ACTUATED_METRIC.md`,
  blob `601f4a6aeb093ab547692015b31a92be48b41c61`, sections 4-6: actual
  live-query binding, metric response and all admissibility qualifications.
* `02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md`,
  blob `75c40d133a23973a36ba5b95d34b4eb36ca96663`, sections 1-2: literal
  inverse-transpose Clifford query, inverse-PF compensation and scene jet.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_two_query_native8d_no_exterior.py`,
  blob `caf7f24801464f448fd3cae9e20399d13ec76754`: original 8D compression
  and fixed minus preparation, with the entire output complement retained.
* `02_REGISTRY/research/A4D_P25_NATIVE_COST_FLOOR_PSD_MIXED_PALATINI_VACUUM_NO_GO_2026_10_20.md`,
  blob `030b4d4db2fe2bacd80dffbeedfdf0b268e75d70`: original shared-link,
  unimodular coframe and null-metric convention used by the saddle slice.
* `02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md`,
  blob `ed00d6609c6f9f88391c7ff076abc65a3524dbd1`: actual REST preparation,
  null-to-rest map, orientation pullback and fixed calibrated source transport.
* `02_REGISTRY/research/A4D_COMPLETE_BOOK_GOLDEN_SELF_CODE_STATIONARY_ENVELOPE_AND_ODD_GEOMETRY_2026_10_20.md`,
  blob `c2eb7bd59b16fe9871580fd7002110d80f9275fa`: exact self-code cancellation.
* `02_REGISTRY/research/A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md`,
  blob `e2475112b9e8a66e3558c828c15615d7238e1025`: native AF residual/envelope.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/SCREEN_RECORD_PROPER_SCORE_MIXED_SOURCE_GATE.md`,
  blob `56c5dc2a546496d84018c20ccdb4f23e419931ae`: distinct Jones support scope.

The accepted `STOPPED_FIELD_SADDLE.md` has SHA-256
`aad562832df891bf042379ff5f11df28b7cb507168de56ba4ef376ca9906d19c`;
`CORRECTION_SECOND_JET.md` has SHA-256
`439cc3de63db6788e5a8fb6c0d42c9c3e32bc34cf297971e590a83e4688b9505`.
The small accompanying `check_equation_equivalence.py` checks exact algebra
in (1), (3), (7)-(13), kernel and source-cancellation hostile controls. It is
not a numerical field acceptance, global minimization or refinement claim.
