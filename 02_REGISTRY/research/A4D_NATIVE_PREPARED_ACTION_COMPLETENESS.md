# G0: complete prepared action fiber and a genuine observable root distinction

Research input: `9488c133312768580bdad43bb570a0bed836432f`, existing #310.
Supported owner tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.
Status: **complete boundary of the literal prepared-pair ActionProtocol
interface**. Native history preparation, admission, geometric action and
full refinement remain OPEN. Countermodels below are not adopted D0 actions.

This consumes the primitive price classification in
[dynamical ownership](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md), rather than reopening
it. The new step is a necessary-and-sufficient theorem for **every**
independently given preparation, followed by actual field derivatives,
stationary sets and native frame/refinement controls. Thus primitive freedom
is no longer supported only by different transition numbers or off-shell
examples. Its scope is nevertheless a typed interface, not the whole core.

## 1. Exact interface and complete theorem

The primary owners are `D0/Foundation/VerifiabilityNecessity.lean` and
`D0/Foundation/EndogenousActionQuantum.lean`. For an arbitrary actual protocol
P, let X be an independently specified domain and let u,v:X→P.State be the
two prepared endpoint maps. Neither their existence nor their physical
meaning is assumed to follow from verification. Fix f:X→R.

There exists an actual `ActionProtocol P` satisfying

```text
A.action(u(x),v(x)) = f(x)             for every x in X
```

**if and only if all three conditions hold**:

```text
u(x)=v(x)                         => f(x)=0;
u(x)!=v(x)                        => f(x)>=1;
(u(x),v(x))=(u(y),v(y))            => f(x)=f(y).
```

Necessity follows respectively from `action_refl`, `action_nontrivial` and
the fact that action is a function on state pairs. For sufficiency define
the action on **all** pairs, not only prepared ones: it is zero on identities;
on a prepared nonidentity pair use f at any representative; on every other
nonidentity pair use one. The fiber condition makes the representative
irrelevant and the gap condition proves admission. This construction and
both implications are compiled as `complete_prepared_action_fiber`.

Under the actual `VerificationContract`, pair equality is equivalent to
equality of both records, by the owner's `record_injective` theorem. Thus
the third condition is an observable record-fiber condition, not an imposed
identification of histories with fields.

For preparations that stay off the diagonal, the whole fiber is exactly
the functions f>=1 that descend through the prepared record-pair quotient.
If that quotient faithfully retains a field readout s, **every nonnegative
function E(s)** gives f=1+E(s). If it loses s, it cannot support that faithful
readout. This is a precise factorization alternative, not the previously
rejected isotropy/readout dichotomy. No converse involving physical D0
nonuniqueness is asserted. Canonical minimum cost remains exactly one on
this whole off-diagonal preparation; its excess field action is zero.

The theorem is for each **fixed P and fixed u,v**, without replacing the
native protocol by a convenient carrier. It does not select u,v or E.
Identity-based infinitesimal readings retain the earlier discontinuity
obstruction; a moving pair that remains nonidentity is a different case.
An identity cost and a prepared off-diagonal cost are never conflated.

## 2. Actual native observables and complete quadratic field consumer

Use the actual `ArchiveCochain N = (ArchiveRolePhaseGroup N ×
ArchiveFockState)→R`, with all sixteen Fock components and L=N+2. At each
size take the two points with all phase coordinates zero except Role A,
which has index k=0 or k=1. These points are distinct at every L>=2; the
Fin/phase-group conversion is the owned `archiveRolePhasePointGroupEquiv`.
Read the literal vacuum component:

```text
s_k(psi) = scalarComponent N psi (anchor_k),       k=0,1.
```

The map s to R² is surjective: the two owned scalar cochains supported at
the corresponding points give the coordinate directions. All other sites
and fifteen non-vacuum grades remain in the domain and variation space.

For **every** real symmetric positive-semidefinite 2×2 matrix M, the
nonnegative quadratic excess E_M=s^T M s is an admitted prepared cost
reading whenever the preparation retains s. Its genuine variation is

```text
delta E_M[direction] = 2 (M s)^T delta s.
```

Since the two coordinate directions are admitted, full matter stationarity
is **equivalent** to M s=0. The projected stationary output is exactly
ker M. Hence two members have the same entire scalar-output stationary
correspondence exactly when their kernels agree. The dimension of the full
matter stationary space is 16 L^4 - rank M; its retained directions are not
automatically gauge. This generic finite-dimensional classification is
analytic; its rank/control specializations are exact, and the two complete
native gates below are compiled with actual `HasDerivAt` propositions.

Choose two nonzero members, rather than comparing only with zero action:

```text
M_1=diag(1,0),       E_1=s_0²;
M_2=diag(1,1),       E_2=s_0²+s_1².
```

Their full gates are respectively s_0=0 and s_0=s_1=0. The scalar cochain
with (s_0,s_1)=(0,1) is a genuine matter root of the first and fails the
second with directional derivative two. Both gates have roots, both
energies are nonzero, and the difference cannot be removed by one nonzero
calibration or by an invertible change preserving the scalar readout.
For this quadratic slice d_A=3 and the Euler family has the same three
linear coefficients. After comparing full stationary scalar outputs the
classes are rank zero, the rank-one kernel lines, and rank two; different
nonzero multiples of one M do not create different stationary classes.

## 3. Full raw/link/matter countermodel, source and joint stationarity

The formal countermodel payload retains the actual raw coframe e with
nonzero det(eta+e), a `LorentzAffineExteriorConnection` including **all
affine shifts**, and the full `ArchiveCochain`. The zero coframe/flat affine
connection proves its background nonempty using the owned Lorentz metric
determinant-unit theorem. No raw or centered field is quotiented away.

For the independence test define a verification carrier Bool×payload,
identity persistent records, two Bool lines and one Unit catalogue. Comparison
is the actual equality/difference test. The entire `VerificationContract`
is proved. Its classical equality decision and line labels do not prove a
finite effective apparatus or physical causal independence; the owner's
ordinary representation obligation is retained. The two prepared endpoints
are `(false,z)` and `(true,z)`;
their field readout is literally the same z and the bit keeps the transition
nonidentity. Define costs zero on identical verified states and 1+E_i at
the target's full field payload otherwise. Both satisfy `ActionProtocol`
on **every** state pair; the prepared value is exactly 1+E_i.

This is an explicit **model of the two primitive interfaces with native
field data**. It is not the literal 33-vertex scene, not a derived native
history preparation, and not evidence that these field states are physically
admitted. In particular assigning a number to a record does not prove the
required native-to-physical action transfer. The universal theorem in
Section 1 is independent of this countermodel.

One common geometric action J can be retained in both models. If J is
bounded below by m on the specified domain, the admitted prepared price is
`1+(J-m)+E_i`; the constant has zero variation. No geometric action is
selected. On any independently justified product variation domain, assume
the actual background curves start at the declared background and make J
differentiable. The compiled generic
`genuine_joint_gate_iff` derives, from the derivative of **J+E**,

```text
full joint stationarity <=> geometry stationarity AND full matter stationarity.
```

The background direction carrier must be nonempty and matter variations
must be independent full cochain directions. These are explicit hypotheses,
not inferred from a history map. Given a genuine stationary background of
that same J, the (0,1) scalar field is therefore a joint root for E_1 and
not for E_2. The background-root and differentiability premises remain in
the actual printed proposition. J=0 supplies a nonempty interface test,
not native gravitational dynamics. An empty geometric stationary fiber
does not establish physical inequivalence.

Both E_i are independent of background data. Their coframe, metric,
connection and affine-shift sources are exactly zero on every background
curve; this is compiled as a genuine constant derivative. All ten metric
and 24 link-row directions are finite exact zero-source controls. The common
J derivative is retained equally in the two joint systems. No source is
fitted from the desired equation or independently at each size. Zero source
in these mathematical models is not the required owned physical matter
source, nor does it make the curved resonant metric a GR solution.

## 4. Owned gauge and refinement: what is really preserved

The owned `archiveExteriorFrameLift_vacuum_coeff` proves vacuum-coefficient
invariance for **every** invertible linear frame, not just tested Lorentz
matrices. Applied to the actual `archiveAffineCoChainGauge`, it proves
s_k(g·psi)=s_k(psi) for every affine node gauge. Affine translations are
retained in the connection and absent from this owner's CAR-fiber action.
The same statement applies to the exterior matter dressing of the full
[raw/link/matter quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md). Thus the (0,1)
versus (0,0) distinction survives that owned frame quotient. No unnamed
additional spacetime/history gauge is inferred. Finite frame invariance
gives its finite infinitesimal zero variation; this is not a continuum
diffeomorphism Ward theorem.

The actual `archiveRGPhaseProjection` sends both persistent indices 0 and
1 to themselves at every adjacent size. The pointwise Role product and
owned phase-group equivalence therefore preserve both anchors. For **any**
full graded refinement R whose scalar block is the literal B0 pullback,
s_k(R psi)=s_k(psi). Both E_i and their full fine/coarse matter gates commute
exactly, including newly available fine matter directions. The scalar
block premise is printed explicitly in `ScalarRefinementCompatible`.

The existing [cochain refinement construction](A4D_NATIVE_COCHAIN_REFINEMENT.md)
supplies this scalar block: degree zero uses B0 in every role, while occupied
roles use B1 and the degree-aware normalization. Those other fifteen blocks
are not replaced by B0 and are not discarded in the gate. Prefix restriction
is a left inverse of the full constructed graded lift. The exact checker
tests all sixteen grades, ordinary, wrap and collapsed rows.

Prepared prices consequently commute whenever their background preparation
also commutes. Full pair-cost refinement additionally requires an injective
state transition; otherwise a nonidentity fine pair can collapse to an
identity coarse pair. This requirement cannot be hidden by checking just
one prepared edge. No full admissible coframe/link/background transition,
no compatible J and no commuting native history preparation is supplied by
the scalar theorem. The earlier `4*K` Nyquist frozen-lift mismatch and
nonuniform raw/transported coordinate change remain active obligations.

The two anchor readings are point functionals. Their positive compatible
point weights have the atomic, rather than smooth volume, limits already
classified in [measure refinement](A4D_NATIVE_MEASURE_REFINEMENT_BOUNDARY.md).
They are sharp finite interface controls, not candidate continuum matter
densities. Neither locality, phase/spacetime covariance nor positive volume
recovery is selected by the primitive contracts.

## 5. Consequence for the single G0 target and the next proof

| Question | Result |
|---|---|
| Does a faithful prepared field readout force a primitive action? | No: the complete prepared-pair cost fiber is proved for every P,u,v. |
| Can the remaining cost freedom be only a harmless normalization? | No in the specified full-cochain interface: two nonzero positive readings have different genuine stationary outputs, with the same background source. |
| Does owned frame gauge or scalar B0 refinement erase the witness? | No: exact native invariance and full matter-gate commuting are proved. |
| Are these two readings selected physical D0 actions? | No. They are verification-interface countermodels. |
| Are literal scene histories identified with full native fields? | Not proved. Their all-walk and trace classification is retained without that identification. |
| Is the bounded-potential/small-link curved family physically admitted? | Not decided. Bare verification/action-gap rules can represent it in the countermodel payload, but the owned history preparation and full refinement are still missing. |
| Are G0, GR, global closure or the original parent terminals closed? | No. |

The first missing lemma is now particularly concrete: **derive the native
history/record preparation and its composition/refinement action law on the
full raw/coframe/link/matter carrier, including its variation image**. Show
which restriction on the complete fiber comes from a primary owner, and why
it excludes or identifies the two stationary-distinct countermodels.
If the law instead factors through a supplied input, prove that independence
for the entire consumed interface; do not choose the input by target GR.

This closes the prepared-pair ambiguity of the primitive interface, not the
full physical ownership question. There is no need to repeat another cost
ratio, arbitrary action encoding, fixed-frame scalar or off-shell example.
The next package must supply the missing law or a complete derivability
boundary with all its actual premises. It must also decide admission of
the existing [curved raw/link resonance](A4D_NATIVE_METRIC_COMPACTNESS_AND_LINK_RESONANCE.md)
and reconcile its full coframe refinement. Soundness, recovery, genuine
physical source/Ward and causal constraints remain downstream obligations.

## 6. Verification boundary

The companion Lean capsule prints thirty actual propositions and twenty
definition/theorem types, including the retained joint differentiability,
background-root and scalar-block hypotheses. Its transitive native and
toolchain source pins, compiler output and exact checker are saved together.
Only standard logical axioms are allowed. Generic PSD/kernel statements in
Section 2 are analytic; no compiled infinite tower, physical history map,
positive volume density or joint GR solution is advertised.

The exact checker consumes the previously certified full joint quotient,
cochain refinement and curved resonance by pinned hashes. It independently
checks prepared-pair collisions/identities/gap controls, genuine polynomial
derivatives, root nonemptiness and difference, every Fock grade, all 24 link
and ten packed metric zero-source directions, and false scope/ledger mutations.
Original #310 fixed-source/raw-owner, #202 and #317 contracts, graph statuses,
claims, supported Lean owners and public text remain unchanged.

Artifacts: [capsule](certificates/a4d_native_prepared_action.lean),
[compiler output](certificates/a4d_native_prepared_action_output.txt),
[source receipt](certificates/a4d_native_prepared_action_results.json),
[exact checker](certificates/a4d_native_prepared_action_check.py),
[exact ledger](certificates/a4d_native_prepared_action_certificate.json).
