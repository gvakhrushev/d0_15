# Actual archive seam action and the signed Palatini action: audited boundary

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `cc6cc38f3e7053b6473cdeee65c17fadad6275d7`.
Status: proved restricted transfer obstruction with exact finite controls;
the original parent remains PARTIAL / OPEN. No BOOK, claim, Lean owner or
task lifecycle is changed.

The positive detector on the golden prefix support in
`A4D_NATIVE_FINITE_PROBE_COMPLETION.md` Sections 13–15 faithfully encodes
already measured signed records. It does not yet identify the physical
Palatini action with the archive seam action. The following gives an
actual action-and-variation obstruction to one proposed identification,
and identifies the exact exception for independent doubled sectors.

## 1. The actual owner, rather than an arbitrary encoded D

`ArchiveSeamCurvature` fixes the cyclic phase lift

\[
 J_{ij}=1_{\{i\bmod m=j\}},\qquad
 D=L_{m+1}J-JL_m,\qquad S=\|D\|_{HS}^2.
\]

`ArchiveVariation` fixes the fine operator and lift and varies the coarse
operator only:

\[
 \delta D=-J\delta L,\qquad
 dS[\delta L]=-2\langle D,J\delta L\rangle.
\tag{1}
\]

The old `LaplacianVariation` requires symmetry and row-sum zero. Its
`local_support : Prop` field does not enforce a support predicate.
`ArchiveLocalLaplacianVariation` independently owns the genuine nearest
neighbor support condition and identifies this space with arbitrary real
edge conductance variations. Neither space makes the matrix logarithm of
a Lorentz connection into a Laplacian variation without an additional map.

The literal definition `ArchiveStationary n` evaluates (1) on the fixed
canonical pair at level n. The variable-L stationary examples below are
an affine extension of precisely this formula and variation space; they
are not a claim that the frozen canonical predicate has become true.

## 2. Exact canonical gate failure

Let both Laplacians be their canonical unit-conductance cycles, m≥3.
The only nonzero D rows are

\[
 D_{0,:}=-e_0^T+e_{m-1}^T,\qquad
 D_{m,:}=-e_0^T+e_1^T.
\]

Thus rank(D)=2 and S=4, exactly as the existing seam certificate records.
For the legitimate nearest-neighbor conductance variation
\(E_{01}=(e_0-e_1)(e_0-e_1)^T\), (1) gives exactly

\[
 dS[E_{01}]=6.
\tag{2}
\]

In the complete cyclic edge basis the gradient is
\((6,0,\ldots,0,6)\). Therefore these canonical native states are not
`ArchiveStationary`, even after restricting to genuine local variations.
An identity transfer taking stationary Palatini endpoints directly to
these canonical pairs fails the gate already at one finite level.
This is not a no-go for a newly parameterized archive sector.

## 3. Even the natural variable-coarse extension is convex

To give the proposed transfer its strongest immediate interpretation,
allow arbitrary affine coarse variations while retaining the fixed fine
operator and lift. Then

\[
 S(L+\delta L)
 =S(L)+dS_L[\delta L]+\|J\delta L\|_{HS}^2,\qquad
 D^2S[\delta L,\delta L]=2\|J\delta L\|_{HS}^2.
\tag{3}
\]

Since \(J^TJ=\operatorname{diag}(2,1,\ldots,1)\), J is injective.
Consequently (3) is strictly positive on every nonzero allowed variation.
There is a unique stationary point in each chosen affine variation
space, and that point is its global minimum. In any edge basis E_a,

\[
 H_{ab}=2\langle JE_a,JE_b\rangle
\]

has full rank. The finite checker verifies both the full symmetric
row-sum-zero spaces and the local spaces at m=3,4,5,6. This is a replay
of the general injectivity proof, not a search over carriers.

The literal Palatini action has a different stationary local structure.
At the flat solder and identity links, all 24 full physical connection
Euler rows vanish. The owned 24×24 zero-phase connection Hessian has

\[
 \operatorname{spec}H_0=\{-2\ (4),-1\ (8),1\ (8),2\ (4)\};
 \qquad \operatorname{inertia}H_0=(12,12,0).
\tag{4}
\]

For an exact finite, rather than formal, control let

\[
 U_0=C(tG_{02}),\quad U_1=C(\pm tG_{12}),\quad U_2=U_3=I,
 \quad C(X)=(I-X/2)^{-1}(I+X/2).
\]

These are constant physical Lorentz links. Every face except (0,1) is
flat. Their literal cell action with the unchanged odd plaquette
curvature is

\[
 \mathscr A_\pm(t)
 =\mp\frac{16t^2(t^4+16)}{(t-2)^2(t+2)^2(t^2+4)^2}.
\tag{5}
\]

Both signs occur arbitrarily close to the stationary identity field,
within any fixed small physical chart and at log-O(h) amplitudes. At fixed
g and external source, the source term in Section 15's J_h is independent
of the connection. Hence J_h−J_h(flat) has these same two signs, multiplied
by the positive counting normalization; adding the prescribed source does
not remove this obstruction.

**Restricted transfer obstruction.** There is no local transfer which
(a) fixes fine L and J when the Palatini connection varies, (b) takes
its allowed connection variations to allowed coarse Laplacian variations,
(c) takes the flat full-stationary Palatini field to a stationary point
of this seam extension, and (d) preserves the action up to one fixed
nonzero affine calibration. Equation (3) makes every native stationary
point a minimum; (5) has both increasing and decreasing paths through
its stationary base. This contradiction requires no differentiability
assumption on the transfer. A C² version follows immediately from (4)
and the positive Hessian in (3).

This excludes the direct fixed-fine action/gate bridge. It does not
exclude a larger state sector where fine L, the lift, sources or the
variational action itself also change with the connection; those changes
require explicit owners and do not follow from the current formula.

## 4. Positive Born readout is legitimate and does not automatically carry the gate

A signed contrast of positive response effects is mathematically valid;
its failure here is specifically the missing stationarity identity.
Two exact controls use the actual D above, not an encoded replacement.

For m=3, the cycle is complete. The affine coarse extension has the
unique full stationary minimum with edge conductances

\[
 (w_{01},w_{12},w_{20})=(3/5,6/5,3/5),\qquad S_*=8/5.
\]

All old full variation equations vanish there. Form the positive fine
response \(R_f=D_*D_*^T\) and the genuine coordinate-effect contrast
\(Z_f=\operatorname{diag}(1,-1,0,0)\). Its unnormalized signed output
\(F_f=\operatorname{Tr}(Z_fR_f)\) has edge gradient

\[
 \nabla F_f=(4/5,0,8/5),\qquad
 \nabla(F_f/\operatorname{Tr}R_f)=(1/2,0,1).
\tag{6}
\]

Thus a legitimate Born probability contrast varies at a stationary
native action. This fine response is the Gram operator of the same
rectangular seam and is positive, although it is not the coarse
operator D*D. At m=3 the latter has an accidental stationary first jet
for every constant coarse effect; the checker does not conceal this
scope distinction.

For m=4, use the genuine local edge-variation owner. Its stationary
minimum has positive conductances

\[
 (8/13,14/13,14/13,8/13),\qquad S_*=22/13.
\]

For the coarse positive response \(R_c=D_*^TD_*\) and the coordinate
contrast \(Z_c=\operatorname{diag}(1,-1,0,0)\),

\[
 \nabla \operatorname{Tr}(Z_cR_c)=(4/13,6/13,0,2/13)\ne0.
\tag{7}
\]

This solves all genuine local variation equations, not the old
unrestricted equation whose support field is vacuous. Every conductance
is positive, so small two-sided local probes remain real weighted
Laplacians. Positivity of these Born responses is an exact Gram identity.

At either stationary minimum, the actual centered seam-action contrast
in an allowed coarse direction is exactly zero. Distinct endpoints in
that direction are not stationary, by (3). Arbitrary source records
can therefore not be substituted into such a same-fine stationary
contrast by the decoder alone. Varying the fine operator as a metric
probe changes the boundary of this statement and needs an independent
intertwining theorem.

## 5. Polarization and independent doubling: keep the real exception

The polarization identity

\[
 (\|D+V\|^2-\|D-V\|^2)/4=\langle D,V\rangle
\]

constructs signed measurements. It is the first variation of S only
when V is the actual image −JδL. Replacing V by arbitrary encodings
does not preserve its native variation type or stationary gate.

A difference of two independent positive sector actions cannot be
rejected on stationarity alone. On a product with independent full
variations,

\[
 d(S_++S_-)=0\ \Longleftrightarrow\ dS_+=dS_-=0
 \ \Longleftrightarrow\ d(S_+-S_-)=0.
\tag{8}
\]

Thus doubling can provide an indefinite readout while retaining the
product critical set. Its variational functional is nevertheless the
signed difference, whereas the currently owned archive action is the
positive sum. This is a new action/readout sector identity to prove.
It also does not map the physical finite Euler equations or source
metric probes to that product merely by applying polarization.
Equations (6)–(7) show why arbitrary effects on a single sector are
insufficient; equation (8) prevents overstating a general doubling no-go.

## 6. Deliverable and replay

The [immutable checker](certificates/a4d_native_seam_action_gate_check.py)
and its [pinned ledger](certificates/a4d_native_seam_action_gate_results.json)
replay all finite identities and both sign controls.

The checker pins every imported owner by SHA256 and defaults to immutable
ledger replay. Exact finite checks PASS. The report proves a restricted
fixed-fine transfer obstruction and concrete signed-readout gate failures;
it does not claim the original theory or the enlarged native bridge closed.
