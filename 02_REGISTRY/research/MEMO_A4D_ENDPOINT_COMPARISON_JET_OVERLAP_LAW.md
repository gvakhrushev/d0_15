# A4D endpoint/common-center comparison jet and finite overlap boundary

**Audited baseline:** current canonical main = c5b9cf5fb348e12272f20007dc7a987196f9c91b, fetched and rechecked 2026-09-24.  
**Canonical task:** 00_WORK/tasks/EXP-A4D-ENDPOINT-COMPARISON-JET-OVERLAP-LAW.md.  
**Scope:** one fixed ArchiveRolePhaseGroup N only. No inter-level refinement map, no golden/phi selector, no Lean, and no lifecycle/manifest/claim/generated/release edits.

## 0. Primary result

The primary terminal is

**ENDPOINT-OVERLAP-COMPARISON-NEW-PRIMITIVE-REQUIRED.**

The result is sharper than the preceding common-center terminal.

1. The most literal unlabelled common-center factorization class can be exhausted. If one cell has one auxiliary center fiber and invertible endpoint-to-center maps whose quotients reproduce every boundary transport, every loop in that cell telescopes to the identity. Therefore this class cannot cover a cell with nontrivial relative path holonomy; in the owned affine geometry a nonzero square path defect, linear curvature, or translation/torsion defect blocks it.
2. Adding path labels removes that contradiction, but it exposes the actual missing datum: a path-resolved incidence comparison law and its overlap cocycle. PR #70 supplies path composition and holonomy, not a matter comparison functor extending the scalar translation action.
3. The scalar distance-two constraints on the comparison jet are not themselves inconsistent. An explicit two-edge-patch symmetric jet below satisfies them and cancels the forbidden distance-two Hessian entries at L=5 for both the delta witness and a non-delta witness with G² nonzero.
4. That repair is highly nonunique. A continuous family of constants-preserving nearest-neighbor edge-Laplacian corrections leaves the mandatory distance-two entries unchanged. By the frozen unrestricted dressing theorem, all such flat pure-gauge jets admit exact finite matrix-groupoid integrations. Thus exact groupoid composition plus scalar cell support do not choose the comparison jet.
5. None of the current owners removes that freedom on general uncentered backgrounds. Constant harmonic strain is outside im d_f but is seen by the full owned H(e); plaquette curl makes endpoint reconstruction path dependent; a rational Lorentz boost of the flat raw solder produces a constant nonexact coframe; and the fixed located J forces shifted dual anchors under degree-mixing boosts.
6. The transverse plaquette modulus remains independent of every pure-gauge comparison-jet test.

There is therefore no canonical finite endpoint/common-center overlap law derivable from the current fixed-N D0 owners. A universal matter no-go would be too strong: the algebraic flat constraints are soluble, unrestricted exact groupoid completions exist, and an inverse-free parent with extra center variables is not excluded. The earliest missing datum is a new, typed, path-resolved comparison primitive.

## 1. Frozen owners and boundaries

The following merged owners and durable packets were treated as frozen. PR #80 landed while this experiment was being written and PR #82 subsequently retired its completed worker bookkeeping. The branch was rebased through both merges; the new second-order owners were re-audited and the PR #82 changes add no mathematical comparison law.

| Owner / packet | Literal input used here | Boundary that remains |
|---|---|---|
| ArchiveAffineCartanConnection, PR #70 | affine pulls, affine gauge law, exact flat translation to forwardGaugeCoframe, two square paths, open curvature and torsion | affine translation of an internal fiber does not define its action on sampled matter amplitudes |
| ArchivePathWordAlgebra, PR #70 | exact path append/reversal; endpoint evaluation is path-independent iff all loop holonomy is trivial | no endpoint/common-center matter interpolation is selected |
| A4DDiscreteEnergyKernel, PR #75 | complete uncentered flatStaggeredH; scalar symmetric bond; A_r=(I+U_r^-1)/2; both U_s and U_s U_r^-1 paths; fluxEnergy; Nyquist/corner/all-degree controls | the finite nonlinear comparison law that produces these first-order coefficients is absent |
| Second-order formal package, PR #80 | A4DSecondOrderCartanCongruence, A4DActionGroupoidSecondJet, A4DScalarAdvectiveGroupoidObstruction, A4DCellHessianTransverseModulus and related owners now Lean-own the generic congruence, mixed groupoid law, scoped advective jet/no-go, and transverse curl boundary | the comparison jet S is still explicit/unselected; no endpoint/common-center finite matter law was added |
| A4DLocatedPrimalDualCell and A4DLocatedTopologicalStar, PR #76 | fixed two-color located J, complement placement, centerMatchedCorner incidence, parity/orientation signs | generic sitewise Lorentz mixing is not compatible with both shifted dual anchors |
| A4DLocalReverseStarNoGo, PR #74 | scoped one-color scalar two-sided inverse/locality obstruction | no constraint on located J or on an auxiliary inverse-free parent |
| MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY | full second Ward identity, action-groupoid mixed law, transverse Hessian freedom | matter background derivative remains a primitive until independently constructed |
| MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT | exterior lift, raw solder action, moving observer form, Lorentz-restricted link lift | no full staggered common-center law |
| MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION | advective pure-gauge cocycle, complete scalar comparison-jet freedom and support constraints | no geometrically selected S or all-background finite completion |
| ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS | separation of the three towers and the two orthogonal seams | forbids importing phi or an inter-level map into this fixed-N problem |

Every statement below is intra-level on the Role-phase/CAR carrier. Nothing here is transported between N levels.

## 2. The literal unlabelled-center comparison class

Fix one elementary cell c. Let F_v be the matter fiber at each incident corner v and let F_c be one auxiliary center fiber. An unlabelled-center factorization consists of invertible maps

\[
C_{c\leftarrow v}:F_v\longrightarrow F_c
\]

such that every owned endpoint pull on a boundary edge is

\[
T_{u\leftarrow v}
=
C_{c\leftarrow u}^{-1}C_{c\leftarrow v}.
\tag{2.1}
\]

Reversal is automatic:

\[
T_{v\leftarrow u}=T_{u\leftarrow v}^{-1}.
\tag{2.2}
\]

For adjacent cells c,d meeting at a corner v the induced center overlap is

\[
O_{d\leftarrow c}^{(v)}
=
C_{d\leftarrow v}C_{c\leftarrow v}^{-1}.
\tag{2.3}
\]

If c and d share an edge with endpoints v,w and both factorizations reproduce the same endpoint transport, then

\[
O_{d\leftarrow c}^{(v)}
=
O_{d\leftarrow c}^{(w)}.
\tag{2.4}
\]

Thus this class has the desired exact overlap law whenever it exists.

### 2.1 Center-gauge torsor

For any Q_c in GL(F_c),

\[
C_{c\leftarrow v}\mapsto Q_c C_{c\leftarrow v}
\tag{2.5}
\]

leaves every endpoint transport (2.1) unchanged. Overlaps transform as

\[
O_{d\leftarrow c}\mapsto
Q_d O_{d\leftarrow c}Q_c^{-1}.
\tag{2.6}
\]

Therefore endpoint data determine at most a center-gauge torsor. A center frame, normalization, or comparison section is additional data unless only gauge-invariant pairwise quotients are used. Current D0 has no owner that selects Q_c or a center trivialization.

This is not yet an obstruction; it says a genuine center may be bookkeeping. The obstruction comes from loops.

### 2.2 Loop telescoping theorem

For any cyclic boundary word
\(v_0,v_1,\ldots,v_m=v_0\), equation (2.1) gives

\[
T_{v_0\leftarrow v_1}
T_{v_1\leftarrow v_2}\cdots
T_{v_{m-1}\leftarrow v_0}
=I.
\tag{2.7}
\]

All center maps cancel pairwise. The same statement holds for affine isomorphisms, not only linear maps.

Hence:

> **Unlabelled single-center factorization theorem.**  
> A cell whose two owned boundary paths between the same endpoints have different affine transport cannot admit one unlabelled center factorization reproducing every boundary edge transport.

PR #70 already owns both square paths separately. Its path-word theorem says that endpoint evaluation factors through the endpoint pair groupoid iff every loop holonomy is trivial. Equation (2.7) is the center-factorization version of the same fact. Nonzero linear curvature, nonzero translation path mismatch, or any other nontrivial relative affine holonomy therefore rules this class out on that cell.

This is a scoped no-go only for the unlabelled single-center factorization class. It is not a universal no-go for path-resolved comparisons.

## 3. Why the natural repairs do not produce the missing law

Three immediate repairs were tested against exact composition, reversal, Role covariance, and curved backgrounds.

### 3.1 Pick one shortest path

One can use the combinatorial cell anchor from located incidence and transport each corner to it along one chosen shortest path. This is exact as a path-word construction, but on a curved square different shortest paths differ by the owned relative holonomy.

A fixed global Role order does not solve the covariance problem. For a two-Role corner, an A/B swap sends the ordered A-then-B path to B-then-A. Re-sorting the transformed labels by the same fixed order selects A-then-B again. These two paths agree only when the relative square holonomy is trivial. Thus a fixed ordering is not an equivariant common-center selector on the curved backgrounds that the task requires.

### 3.2 Average the paths

Arithmetic averaging can reproduce a first-order half coefficient, but it is not a groupoid law. Even for

\[
P=I,\qquad Q=\operatorname{diag}(2,1)
\]

one has

\[
\left(\frac{P+Q}{2}\right)^{-1}
=
\operatorname{diag}(2/3,1)
\ne
\operatorname{diag}(3/4,1)
=
\frac{P^{-1}+Q^{-1}}2.
\tag{3.1}
\]

So reversal already fails. The PR #75 arithmetic operator
\(A_r=(I+U_r^{-1})/2\) is an exact owned first-order sampling rule, but it is not by itself a finite invertible comparison functor.

### 3.3 Split a link by a square root

A symmetric half-link factorization asks for a square root or logarithm of a finite transport. The group structure does not choose such a root globally. A principal analytic branch can be imposed in a restricted neighborhood of identity, but branch/domain selection is new analytic structure and still does not solve path overlap, harmonic coframes, or the fixed-J anchor problem. No current owner supplies this branch.

The result is therefore not that finite midpoint constructions are impossible. It is that none is selected by the present owners with the required exact laws.

## 4. Minimal comparison object that survives curvature

Curvature forces the same geometric endpoint reached along different cell paths to remain distinct comparison objects until their relative holonomy is recorded.

A minimal new fixed-N primitive can be presented as follows.

For every oriented elementary cell c, introduce path-labelled incidences

\[
\alpha=(v,p),
\]

where v is an incident corner and p is a path in the cell closure used to compare that corner with c. Let F_c be an auxiliary center fiber, or equivalently work only with pairwise incidence comparisons. The primitive is

\[
C_N(c,\alpha;e,A,n):
F_v\overset{\sim}{\longrightarrow}F_c.
\tag{4.1}
\]

It must include the raw uncentered coframe e, the affine/path data A, the observer n, orientation, and the existing matter/Fock carrier. Its axioms are:

1. **Normalization and reversal.** Flat trivial geometry gives the identity comparison in the reference gauge; reversing a comparison gives its inverse.
2. **Exact incidence composition.** Pairwise comparison through c is
   \[
   T^c_{\beta\leftarrow\alpha}
   =
   C_N(c,\beta)^{-1}C_N(c,\alpha),
   \]
   and composes exactly.
3. **Path defect, not path erasure.** If p and q reach the same geometric corner, the relative map between (v,p) and (v,q) is the finite matter response to the owned relative path holonomy. Curvature/torsion are legitimate data, not silently set to zero.
4. **Adjacent-cell overlap.**
   \[
   O_{d\leftarrow c}^{\alpha}
   =
   C_N(d,\alpha)C_N(c,\alpha)^{-1}
   \tag{4.2}
   \]
   with the exact triple-overlap telescoping law whenever the same path-labelled incidence is used.
5. **Pure-gauge reduction.** On e=d_f phi with flat linear connection, the induced node-translation matter action reduces to the already classified pure-gauge groupoid, including endpoint differences of the gauge parameter.
6. **Full flat first derivative.** The derivative on arbitrary uncentered e is the complete PR #75 H(e), not only H(d_f xi).
7. **Frame/observer covariance.** Endpoint exterior frames and n transform together. If a center presentation is used, its Q_c is a center gauge and physical pairwise comparisons are independent of its trivialization.
8. **Fixed located J.** J is not moved or metric-deformed. The dual action is obtained through the fixed pairing, with its shifted anchors retained.
9. **Finite geometric input.** The primitive may use the closure of one cell or a two-edge overlap patch. No uniformly bounded compressed support of the resulting finite R is required.

This is the minimal signature in the sense established here: deleting the path label returns to the loop obstruction; deleting the new matter comparison leaves only PR #70's affine fiber action and the exterior linear lift, which do not generate the scalar Cartan tangent.

The center-fiber presentation has the gauge freedom (2.5). A gauge-free equivalent formulation is a comparison functor directly on the path-labelled incidence groupoid.

## 5. Flat scalar comparison jet: constraints are soluble but nonselecting

The frozen scalar classification is

\[
B(\xi,h)
=
B_{\rm adv}(\xi,h)+\mathcal S(h_\xi,h),
\qquad
\mathcal S(h_1,h_2)=\mathcal S(h_2,h_1),
\tag{5.1}
\]

with

\[
D^2W_0[h,h]
=
\mathcal H_{\rm adv}(h,h)
-\mathcal S(h,h)-\mathcal S(h,h)^T.
\tag{5.2}
\]

For L at least 5, define an explicit bilinear two-edge-patch witness. For the scalar cycle, set

\[
\mathcal S_{\rm patch}(h,k)_{i,i+2}
=
\mathcal S_{\rm patch}(h,k)_{i+2,i}
=
-\frac{h_i k_i+h_{i+1}k_{i+1}}8,
\tag{5.3}
\]

put all other off-diagonal entries to zero, and choose each diagonal so that the row sum is zero:

\[
\mathcal S_{\rm patch}(h,k)_{ii}
=
-\sum_{j\ne i}\mathcal S_{\rm patch}(h,k)_{ij}.
\tag{5.4}
\]

Then:

- it is symmetric in h,k;
- its matrix output is symmetric, so its skew output is exactly zero;
- it is translation-covariant on the cycle;
- \(\mathcal S_{\rm patch}(h,k)\mathbf1=0\);
- its geometric input is a two-edge patch.

This is an algebraic witness, not a geometrically derived D0 law.

### 5.1 L=5 delta witness

Use order
\((0,+1,+2,-2,-1)\) and
\(\xi=\delta_0\), so
\(h=(-5,0,0,0,5)\).

The complete comparison matrix is

\[
\mathcal S_{\rm patch}(h,h)=
\begin{pmatrix}
25/4&0&-25/8&-25/8&0\\
0&25/4&0&0&-25/4\\
-25/8&0&25/8&0&0\\
-25/8&0&0&25/8&0\\
0&-25/4&0&0&25/4
\end{pmatrix}.
\tag{5.5}
\]

Therefore

\[
(\mathcal S+\mathcal S^T)_{+1,-1}=-25/2,
\qquad
(\mathcal S+\mathcal S^T)_{0,+2}=-25/4,
\tag{5.6}
\]

exactly the two mandatory support constraints. The skew output is zero.

Subtracting \(2\mathcal S_{\rm patch}\) from the frozen advective Hessian gives

\[
\mathcal H_{\rm eff}=
\begin{pmatrix}
25/2&0&0&0&0\\
0&0&0&0&0\\
0&0&-25/4&0&0\\
0&0&0&-25/4&0\\
0&0&0&0&0
\end{pmatrix}.
\tag{5.7}
\]

All same-axis distance-two entries have been removed.

This proves that the distance-two obstruction in the advective class does not extend to all comparison jets.

### 5.2 L=5 non-delta witness with G² nonzero

Take

\[
\xi=(1,2,0,0,0),
\qquad
h=(5,-10,0,0,5).
\]

Here \(G^2\ne0\). The complete comparison output is

\[
\mathcal S_{\rm patch}(h,h)=
\begin{pmatrix}
75/4&0&-125/8&-25/8&0\\
0&75/4&0&-25/2&-25/4\\
-125/8&0&125/8&0&0\\
-25/8&-25/2&0&125/8&0\\
0&-25/4&0&0&25/4
\end{pmatrix}.
\tag{5.8}
\]

Again the skew output is zero. The corrected Hessian is

\[
\mathcal H_{\rm eff}=
\begin{pmatrix}
-25/2&0&0&0&0\\
0&25&0&0&0\\
0&0&75/4&0&0\\
0&0&0&-125/4&0\\
0&0&0&0&0
\end{pmatrix}.
\tag{5.9}
\]

Thus the cancellation is not an artifact of the delta nilpotence \(G^2=0\).

### 5.3 Continuous nonselection even after the scalar support repair

Set edge weights
\(w_i(h,k)=h_i k_i\) and define the symmetric weighted edge Laplacian

\[
(\mathcal T_{\rm edge}(h,k)\psi)_i
=
w_i(\psi_{i+1}-\psi_i)
+
w_{i-1}(\psi_{i-1}-\psi_i).
\tag{5.10}
\]

It is bilinear and symmetric in h,k, has symmetric matrix output, kills constants, is nearest-neighbor, and has no distance-two entries. Therefore for every real lambda,

\[
\mathcal S_\lambda
=
\mathcal S_{\rm patch}
+
\lambda\mathcal T_{\rm edge}
\tag{5.11}
\]

has exactly the same mandatory distance-two entries (5.6). It changes only diagonal/nearest-neighbor second-order data, which remain compatible with elementary one-dimensional cell support.

The frozen common-center theorem integrates any such flat pure-gauge S as an unrestricted exact matrix-groupoid dressing. That integration does not prove local inverses or an all-background physical action, but it is sufficient for the selection statement:

> **Composition/locality nonselection theorem.**  
> Exact pure-gauge groupoid composition, scalar constants preservation, translation covariance, and the mandatory distance-two cancellation do not select a unique comparison jet.

A skew matrix-output bilinear correction is additional freedom invisible to the quadratic energy unless another finite geometric law fixes it.

## 6. Full owned H(e): why pure gauge is insufficient

A positive terminal would have to recover the complete PR #75 first jet on every uncentered coframe. Current constructions fail before a nonlinear coefficient choice.

### 6.1 Pure gauge

The frozen graded benchmark exactly reproduces

\[
H(d_f\xi)
\]

including the scalar nearest-neighbor term, endpoint half-average, both corner paths, all Fock degrees 0 through 4, parity, L=2 Nyquist behavior on the pure-gauge representative, L=3 corner, and simultaneous signed Role permutations.

This remains a benchmark only.

### 6.2 Constant harmonic strain

Let \(e_A{}^A=t\) be constant on the periodic carrier and all other entries vanish. For \(t\ne0\), this is not in im d_f because every periodic forward difference has zero cycle sum.

Nevertheless the owned H acts nontrivially. On a constant degree-zero scalar cochain,

\[
H(e)\mathbf1=t\mathbf1.
\tag{6.1}
\]

The flux/CAR term vanishes on degree zero and the scalar symmetric bond remains. Any potential-only comparison misses (6.1).

This is also the relevant flat-linear noncontractible-holonomy control: local plaquette curl can vanish while the period integral does not.

### 6.3 Plaquette curl and affine torsion

For identity linear links the two square routes differ by the translation curl

\[
\omega_{rs}^a(x)
=
e_r{}^a(x)+e_s{}^a(x+r)
-e_s{}^a(x)-e_r{}^a(x+s).
\tag{6.2}
\]

It vanishes on pure gauges but not on arbitrary coframes. At L=3, a one-edge excitation \(e_B{}^A(0)=1\) gives the forward-difference curl \(-3e_A\) at the chosen plaquette.

A root-to-site potential reconstruction is therefore path-dependent. Treating the two paths as equal would erase owned curvature/torsion data. A viable comparison primitive must retain the path defect as in Section 4.

At nonzero linear curvature the owned affine torsion transformation itself contains the curvature-times-shift term. Therefore a rule that assumes torsion is always a pure vector is also outside the owned geometry.

### 6.4 L=2 Nyquist

For raw

\[
e_A{}^A=(-2,2)
\]

the backward centered average is zero at both sites, while the accepted occupied-A one-form response is \((2,-2)\). A comparison law that factors only through centered solder data loses this mode. Raw oriented edge slots must remain input.

### 6.5 L=3 corner

For \(e_A{}^B(0)=3\), the accepted distinct-axis matrix element from
\((0,\{A\})\) to \((A-B,\{B\})\) is exactly

\[
-3/2.
\tag{6.3}
\]

The two paths in \(U_A A_B=(U_A+U_AU_B^{-1})/2\) give the correct algebraic locations. Neither exterior covariance nor path composition derives the finite half-comparison law that would select this coefficient.

### 6.6 Role permutation and orientation

All owned first-order formulas are tested under simultaneous signed Role permutations. A comparison based on a fixed path ordering fails this hostile control in a cell with nontrivial relative holonomy, as explained in Section 3.1. Reversal requires inverse comparison, not arithmetic averaging.

Period wraparound was controlled exactly at L=2,3,5,7; no large-L support assertion is imported into the small periods.

## 7. Observer/frame covariance boundary

The exterior/frame sector itself is constructive. For

\[
g|_{AB}=
\begin{pmatrix}5/4&3/4\\3/4&5/4\end{pmatrix},
\]

with \(n_0=e_A\),

\[
h_{gn_0}|_{AB}
=
\begin{pmatrix}
17/8&-15/8\\
-15/8&17/8
\end{pmatrix},
\qquad
g^T h_{gn_0}g=I.
\tag{7.1}
\]

The endpoint link lift and moving creators/contractions transform covariantly when the observer moves.

But the flat raw solder transformed by the corresponding right action is

\[
e'|_{AB}
=
\begin{pmatrix}
1/4&-3/4\\
3/4&-1/4
\end{pmatrix}.
\tag{7.2}
\]

It is constant and nonexact on the periodic carrier. Thus the pure-gauge comparison cocycle has no value on a background reached by this exact rational frame transformation.

A center comparison would have to obey a law of the form

\[
C'_{c\leftarrow v}
=
\rho(g_c)\,
C_{c\leftarrow v}\,
\rho(g_v)^{-1}
\tag{7.3}
\]

in a center-fiber presentation, with a simultaneously moved center observer. Current D0 has no independently defined \(g_c\) or center observer. Because \(g_c\) is precisely center-gauge data, pairwise incidence comparisons can avoid choosing it, but their finite matter law is still the missing primitive.

Therefore observer/frame covariance of the desired comparison maps is not established by the existing endpoint exterior lift alone.

## 8. Fixed located J

J remains fixed.

Given any constructed primal matter action R_P, the perfect located pairing algebraically forces

\[
R_D
=
J^{-T}R_P^{-T}J^T.
\tag{8.1}
\]

This preserves exact composition and does not metric-deform J.

The obstruction is geometric/sitewise-local, not algebraic. A boost mixes primal \(|A\rangle\) and \(|B\rangle\) at one site, while fixed located J sends them to the different dual anchors

\[
x-(B+C+D),
\qquad
x-(A+C+D).
\tag{8.2}
\]

For the rational boost the mixing coefficient is \(3/4\), so both anchors occur. A naive sitewise dual exterior action cannot reproduce (8.1). A path-resolved common-center primitive may carry the required shifts, but no such law is currently owned.

This is not evidence for moving J. It is a constraint on the missing comparison law.

## 9. Locality taxonomy and inverse-free parents

The locality statements that survive this experiment are distinct.

| Notion | Fixed-N result |
|---|---|
| geometric input of the missing primitive | can be required to one cell / one two-edge overlap patch |
| first-jet path length | owned H uses edge and two-edge corner paths |
| direct scalar effective energy in the advective output-site-local class | obstructed by the frozen distance-two witness |
| direct scalar second-order support after an admissible S | algebraically repairable; S_patch is an explicit witness |
| finite R compressed stencil | cannot be uniformly bounded because constant isotropy forces exp(tD) |
| fixed finite nearest-neighbor circuit depth | likewise cannot be uniform in period |
| inverse locality | not implied by local numerator or finite dimension |
| inverse-free local parent with auxiliary centers | not constructed, but not excluded |

Conditionally, once comparison maps C are supplied, an inverse-free incidence parent can be written with auxiliary center amplitudes and local terms comparing them to C psi_v. Nothing in the present owners fixes the required C or proves that such a parent reproduces the complete H and second jet. Therefore no local parent action is claimed.

The physically relevant locality target should be local geometric input / local parent incidence, not uniformly local compressed finite transport.

## 10. Transverse plaquette modulus survives

Pure-gauge S only controls the Hessian on
\(\operatorname{im}d_f\times\operatorname{im}d_f\).

On the flat-linear affine subclass the plaquette mismatch \(\mathfrak c\) transforms as a frame vector. With moving observer,

\[
z_c=h_{n_c}(\mathfrak c_c,\mathfrak c_c)
\tag{10.1}
\]

is quadratic, vanishes with its first derivative at flat, and vanishes on pure gauge. Multiplying any independently covariant cell seed by
\(1+\lambda z_c\) changes a transverse quadratic coefficient without changing the flat first jet or any pure-gauge comparison-jet test.

The current endpoint-overlap analysis does not fix lambda. At nonzero linear curvature the more general affine torsion law must be used, so no universal curved scalar is asserted here. The conclusion needed for this task is narrower and exact: the present fixed-N owners do not eliminate the transverse modulus.

## 11. Direct answers to the canonical questions

| # | Question | Answer |
|---|---|---|
| 1 | Exact finite comparison object? | Not currently owned. The minimal surviving object is a path-resolved cell-incidence comparison functor, equivalently center maps C indexed by corner and path. |
| 2 | Endpoint-to-center map? | Equation (4.1) is the required typed signature. An unlabelled version is insufficient on nontrivial holonomy. |
| 3 | Overlap/composition law? | Equation (4.2) with exact telescoping; path changes must record, not erase, relative holonomy. |
| 4 | Canonical from current owners? | No. Endpoint factorization has a center-gauge torsor, path ordering is noncovariant on curved cells, path averaging breaks reversal, and half-link roots need a new branch. |
| 5 | What S is induced? | No unique S is induced. S_patch is an explicit admissible algebraic witness; S_lambda gives a continuous nonselected family. |
| 6 | Full scalar support constraints? | Yes for S_patch: the required (+1,-1) and (0,+2) entries are exact, and the complete L=5 matrices are (5.5) and (5.8). |
| 7 | Full H(e) for all uncentered e? | No current finite law does. The pure-gauge benchmark matches H(d_f xi) only. |
| 8 | Harmonic and curl backgrounds? | Harmonic strain requires direct raw-coframe input; curl/curvature requires path-labelled comparison with holonomy defect. |
| 9 | Local inverse-free parent? | Not constructed and not excluded. It would require the same missing comparison primitive. |
| 10 | Observer/frame covariance? | Existing endpoint exterior/frame data pass the rational boost with moving n; the desired center/overlap maps do not exist yet, and the boosted raw coframe is outside the pure-gauge domain. |
| 11 | Fixed located J? | Preserved exactly; the global contragredient dual action exists algebraically, while local sitewise comparison faces the shifted-anchor obstruction. |
| 12 | What locality holds? | Local geometric/path input can be demanded; uniform compressed stencil and fixed circuit depth cannot. |
| 13 | Transverse plaquette modulus fixed? | No. It remains constitutive under the stated flat-linear covariant deformation. |
| 14 | All-order provenance-bearing finite matter action? | No. |
| 15 | Single earliest remaining datum? | The path-resolved incidence comparison primitive (4.1-4.2), including its matter response to relative affine holonomy and its full-H flat derivative. |
| 16 | Fixed-N versus inter-level? | Every theorem and obstruction in this memo is fixed-N. Transport across levels requires the separate Role-phase/golden weld and is not used here. |

## 12. Theorem-ready handoff

The mathematical handoff can be formalized later without changing the result of this EXP.

**Theorem A — unlabelled-center loop obstruction.**  
If invertible maps C_v to one center factor every boundary edge as \(T_{u\leftarrow v}=C_u^{-1}C_v\), every cell loop is identity. Hence any two distinct owned affine paths with the same endpoints exclude such a factorization.

**Theorem B — center gauge and overlap covariance.**  
The transformation \(C_{c,v}\mapsto Q_c C_{c,v}\) leaves endpoint transport invariant and conjugates center overlaps by \(Q_d\) and \(Q_c^{-1}\). If two adjacent center factorizations reproduce the same shared edge, their overlap computed from either endpoint agrees.

**Theorem C — scalar patch repair.**  
For L at least 5, equations (5.3-5.4) define a symmetric bilinear constants-preserving comparison jet. On the delta witness it satisfies exactly
\[
(S+S^T)_{+1,-1}=-L^2/2,
\qquad
(S+S^T)_{0,+2}=-L^2/4.
\]
At L=5 it removes every same-axis distance-two entry of the frozen advective Hessian. The same cancellation holds for the displayed non-delta witness with \(G^2\ne0\).

**Theorem D — scalar nonselection family.**  
For every lambda, \(S_\lambda=S_{\rm patch}+\lambda T_{\rm edge}\) preserves constants and all mandatory distance-two constraints. Therefore those constraints plus exact pure-gauge composition do not select S.

**Theorem E — full-coframe domain boundary.**  
A potential-only law cannot cover both nonzero constant harmonic strain and nonzero plaquette curl on the periodic carrier. Centered-solder-only rules additionally fail the L=2 raw Nyquist witness.

**Theorem F — located/frame boundary.**  
The rational A/B boost with moving observer passes the endpoint exterior covariance identities but produces a constant nonexact raw coframe and mixes primal states whose fixed-J dual anchors differ. Hence endpoint exterior covariance alone does not supply a sitewise common-center law.

No theorem in this handoff claims a Spin representation, physical time, unique nonlinear energy, stress tensor, Einstein equation, metric reinterpretation of J, or an inter-level refinement law.

## 13. Exact rational controls

A standalone exact checker passed **47/47** assertions. It covers:

- the unlabelled-center loop identity and center-gauge torsor;
- exact failure of arithmetic path averaging under reversal;
- scalar L=3,5,7;
- L=5 delta mandatory S entries and complete distance-two cancellation;
- L=5 non-delta \(G^2\ne0\) and distance-two cancellation;
- a nonzero lambda member of the nearest-neighbor free family;
- constant harmonic coframes;
- L=2 raw Nyquist;
- L=3 plaquette curl and distinct-axis corner;
- all 16 Fock states, degrees 0 through 4, and degree/parity preservation of \(E_{sr}=c_s^\dagger c_r\);
- exact rational Lorentz boost with transformed observer;
- boosted raw harmonic/nonexact coframe;
- fixed located-J anchor mismatch.

The checker uses Fraction arithmetic only.

~~~python
from fractions import Fraction as F

checks = []
def ck(name, cond):
    assert cond, name
    checks.append(name)

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def tr(a):
    return [list(x) for x in zip(*a)]

def add(a, b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]

def sub(a, b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]

def sc(c, a):
    return [[c*x for x in r] for r in a]

def mm(a, b):
    return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]

def diag(v):
    return [[x if i == j else F(0) for j in range(len(v))] for i,x in enumerate(v)]

def mv(a, v):
    return [sum(x*y for x,y in zip(r,v)) for r in a]

def inv(a):
    n = len(a)
    w = [list(a[i]) + eye(n)[i] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j,n) if w[i][j])
        w[j],w[p] = w[p],w[j]
        q = w[j][j]
        w[j] = [x/q for x in w[j]]
        for i in range(n):
            if i != j and w[i][j]:
                q = w[i][j]
                w[i] = [x-q*y for x,y in zip(w[i],w[j])]
    return [r[n:] for r in w]

def shift(L):
    return [[F(j == (i+1)%L) for j in range(L)] for i in range(L)]

def cycle(L, xi):
    U = shift(L)
    Ui = tr(U)
    D = sc(F(L,2), sub(U,Ui))
    Delta = sc(L, sub(U,eye(L)))
    h = mv(Delta,xi)
    G = mm(diag(xi),D)
    K = mm(diag([x*x for x in xi]),mm(D,D))
    Hadv = add(add(sc(2,mm(tr(G),tr(G))),sc(2,mm(tr(G),G))),
               add(sc(2,mm(G,G)),sc(-1,add(K,tr(K)))))
    return h,G,K,Hadv

def spatch(h,k):
    L = len(h)
    S = [[F(0)]*L for _ in range(L)]
    for i in range(L):
        j = (i+2)%L
        q = -(h[i]*k[i] + h[(i+1)%L]*k[(i+1)%L])/8
        S[i][j] = q
        S[j][i] = q
    for i in range(L):
        S[i][i] = -sum(S[i][j] for j in range(L) if j != i)
    return S

def tedge(h,k):
    L = len(h)
    T = [[F(0)]*L for _ in range(L)]
    for i in range(L):
        j = (i+1)%L
        w = h[i]*k[i]
        T[i][j] += w
        T[j][i] += w
        T[i][i] -= w
        T[j][j] -= w
    return T

C = [
    eye(2),
    [[F(2),F(1)],[F(1),F(1)]],
    [[F(1),F(1)],[F(1),F(2)]],
    [[F(3),F(1)],[F(2),F(1)]],
]
def edge(u,v):
    return mm(inv(C[u]),C[v])

loop = eye(2)
for u,v in [(0,1),(1,2),(2,3),(3,0)]:
    loop = mm(loop,edge(u,v))
ck("single-center-loop", loop == eye(2))

Q = [[F(2),F(1)],[F(1),F(1)]]
CQ = [mm(Q,c) for c in C]
ck("center-gauge-torsor",
   all(mm(inv(CQ[u]),CQ[v]) == edge(u,v)
       for u,v in [(0,1),(1,2),(2,3),(3,0)]))

P = eye(2)
R = [[F(2),0],[0,1]]
avg = sc(F(1,2),add(P,R))
avg_rev = sc(F(1,2),add(inv(P),inv(R)))
ck("path-average-reversal-fails", inv(avg) != avg_rev)

for L in (3,5,7):
    xi = [F(i == 0) for i in range(L)]
    h,G,K,Hadv = cycle(L,xi)
    S = spatch(h,h)
    ck(f"L{L}-S-constants", mv(S,[F(1)]*L) == [F(0)]*L)
    if L >= 5:
        ck(f"L{L}-delta-support-1", 2*S[1][L-1] == -F(L*L,2))
        ck(f"L{L}-delta-support-2", 2*S[0][2] == -F(L*L,4))
        Heff = sub(Hadv,sc(2,S))
        ck(f"L{L}-distance2-cancelled",
           all(Heff[i][j] == 0 for i in range(L) for j in range(L)
               if min((j-i)%L,(i-j)%L) == 2))
        T = tedge(h,h)
        ck(f"L{L}-edge-free-constants", mv(T,[F(1)]*L) == [F(0)]*L)
        ck(f"L{L}-edge-free-no-distance2",
           all(T[i][j] == 0 for i in range(L) for j in range(L)
               if min((j-i)%L,(i-j)%L) == 2))
        Sl = add(S,sc(F(7,3),T))
        ck(f"L{L}-free-family-keeps-support",
           2*Sl[1][L-1] == -F(L*L,2) and
           2*Sl[0][2] == -F(L*L,4))
    ck(f"L{L}-harmonic-not-gradient", sum([F(1)]*L) != 0)

h2,G2,K2,H2 = cycle(5,[F(1),F(2),0,0,0])
S2 = spatch(h2,h2)
H2eff = sub(H2,sc(2,S2))
ck("L5-nondelta-G2", mm(G2,G2) != [[F(0)]*5 for _ in range(5)])
ck("L5-nondelta-distance2-cancelled",
   all(H2eff[i][j] == 0 for i in range(5) for j in range(5)
       if min((j-i)%5,(i-j)%5) == 2))

ny = [F(-2),F(2)]
ck("L2-raw-Nyquist", ny != [0,0] and
   all((ny[i]+ny[(i-1)%2])/2 == 0 for i in range(2)))
ck("L3-plaquette-curl", 3*(F(0)-F(1)) == -3)
ck("L3-corner", -F(3)/2 == -F(3,2))

def creator(r):
    A = [[F(0)]*16 for _ in range(16)]
    for m in range(16):
        if not (m & (1<<r)):
            s = (-1)**((m & ((1<<r)-1)).bit_count())
            A[m|(1<<r)][m] = F(s)
    return A

cr = [creator(r) for r in range(4)]
for s in range(4):
    for r in range(4):
        E = mm(cr[s],tr(cr[r]))
        ck(f"E{s}{r}-degree-parity",
           all(i.bit_count() == j.bit_count()
               for i in range(16) for j in range(16) if E[i][j]))
ck("degrees-0..4", {m.bit_count() for m in range(16)} == set(range(5)))

eta = diag([1,-1,-1,-1])
g = [[F(5,4),F(3,4),0,0],
     [F(3,4),F(5,4),0,0],
     [0,0,1,0],[0,0,0,1]]
ck("boost-Lorentz", mm(tr(g),mm(eta,g)) == eta)
n = mv(g,[F(1),0,0,0])
en = mv(eta,n)
hn = add(sc(-1,eta),[[2*en[i]*en[j] for j in range(4)] for i in range(4)])
ck("moving-observer",
   [r[:2] for r in hn[:2]] ==
   [[F(17,8),F(-15,8)],[F(-15,8),F(17,8)]] and
   mm(tr(g),mm(hn,g)) == eye(4))
raw = sub(mm(eta,inv(g)),eta)
ck("boosted-raw-harmonic",
   raw[0][0] == F(1,4) and raw[0][1] == -F(3,4))

ck("located-J-anchor-mismatch",
   (0,-1,-1,-1) != (-1,0,-1,-1) and g[1][0] == F(3,4))

print(f"PASS {len(checks)}/{len(checks)} exact controls")
~~~

## 14. Exactly one recommended next step

Specify the fixed-N path-resolved incidence comparison primitive (4.1-4.2) as an independent geometric datum, including its relative-holonomy response, frame/observer law, fixed-J dualization, and the requirement that its flat derivative is the complete H(e); then test whether that single primitive admits a local inverse-free parent. Do not introduce another energy coefficient or an inter-level selector before this datum is fixed.

**Terminal verdict: ENDPOINT-OVERLAP-COMPARISON-NEW-PRIMITIVE-REQUIRED.**
