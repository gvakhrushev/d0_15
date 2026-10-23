# Phi/pi0 synthesis: completed probes and obstruction to an exact-source tower

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Inputs: 8e6ecc0297f5aab22dea6abf8f387432345ae9d6 and its existing proof owners.
Status: **completed centered-probe factor; exact sampled-Einstein tower
impossible on the selected warp; original raw-owner comparison OPEN**.

The two finite objects must be specified before invoking a refinement limit.
The probe has nonempty finite preparations and one Einstein limit. The
exact joint-source tower on the selected curved geometry has no finite
states. A Cauchy completion of the former cannot supply states of the latter.

## 1. The centered observable allows every physical central state

Fix the smooth metric and probe before any links, and use the unchanged
action \(I_h=h^2\mathscr A_h\). Write \(\mathcal L_h(g)\) for the entire
finite physical Lorentz link space on that sampled metric. Every member
has a finite action; no identity-log chart is required.

The endpoint preparation domain \(\mathcal P_h(g_s;R,M)\) is the one
already proved constructively nonempty in the
[finite-probe owner](A4D_NATIVE_FINITE_PROBE_COMPLETION.md):
logs at most \(Rh\), all 24 connection rows at most \(Mh^2\).
Now take
\[
 (K_0,A_+,A_-)\in
 \mathcal L_h(g)\times
 \mathcal P_h(g+\epsilon V;R,M)\times
 \mathcal P_h(g-\epsilon V;R,M).
 \tag{P1}
\]
Read the actual three actions and retain the original \(K_0,\Xi(K_0)\).
The same central record is reused in both signed increments. Their sum is exactly
\[
 T_{h,\epsilon}
 =\frac12\left[
 \frac{I_h(g+\epsilon V,A_+)-I_h(g,K_0)}{\epsilon}
 +\frac{I_h(g,K_0)-I_h(g-\epsilon V,A_-)}{\epsilon}
 \right]
 =\frac{I_h(g+\epsilon V,A_+)-I_h(g-\epsilon V,A_-)}
        {2\epsilon}.
 \tag{P2}
\]
This cancellation also holds for a finite-precision central record, however
large its value or its error. If the two recorded endpoint actions have
errors \(e_+,e_-\), the centered error is at most
\((|e_+|+|e_-|)/(2\epsilon)\); the common central error cancels.
Only the endpoints enter the error proof. Therefore the existing theorem
extends, with the same constants, to every central state in (P1):
\[
 \sup_{(P1)}
 |T_{h,\epsilon}-DI(g)[V]|
 \le C(h/\epsilon+\epsilon^2).
 \tag{P3}
\]
No bound on central links, stationarity, source, derivative, curvature or
relation to the endpoint links is used. The separate one-sided increments
need not converge on this enlarged domain. This extension concerns their
centered sum and does not extend the stationary-action stability theorem.

In particular the signed Q8/Klein-four joint vacuum on the curved warp can
be retained as the central state. Its raw response stays zero and its
centered limit is the nonzero Einstein variation for suitable \(V\).
It is in this probe fiber; it need not be excluded to make that fiber's
limit unique. The exact positive theorem is a **coarser observation**,
rather than equality with the instantaneous response of every central state.

## 2. An actual golden Cauchy sequence of readings

Let \(\delta_0=1/(2\phi^3)=3/(5\pi_0\phi)\). On the owned geometric dyadic
meshes \(h_j=(4\cdot2^j)^{-1}\), put \(\epsilon_j=h_j^{1/3}\).
Choose a fixed \(C_*\ge\max(1,2C)\) and a threshold \(h_*\) respecting the fixed
metric/probe thresholds, including \(\epsilon_j\le s_0\). Set \(j_{-1}=-1\) and predetermine recursively
\[
 j_n=\min\{j>j_{n-1}:h_j\le h_*,
                  \ C_*h_j^{2/3}\le\delta_0^n/4\}.
 \tag{P4}
\]
These integers exist and depend on the experiment, never on central or
endpoint choices. Let \(t_n\) be the actual centered reading on mesh \(j_n\).
Writing \(\ell=DI(g)[V]\), (P3) gives
\[
 |t_n-\ell|\le\delta_0^n/4,\qquad
 |t_{n+1}-t_n|\le(1+\delta_0)\delta_0^n/4.
 \tag{P5}
\]
This supplies the step premise of the existing
[GoldenTower theorem](../../03_FORMALIZATION/D0/Geometry/GHPGoldenCauchySequence.lean)
for this concrete scalar readout. Its complete-space conclusion gives one
limit, and (P5) identifies that limit from the actual finite readings.

For a finite precision record \(q_n\in\mathbb Q(\phi)\) with certified
rounding error \(|q_n-t_n|\le\delta_0^n/4\), the same proof gives
\[
 |q_n-\ell|\le\delta_0^n/2,\qquad
 |q_{n+1}-q_n|\le(1+\delta_0)\delta_0^n/2.
 \tag{P6}
\]
Rational outward intervals, as in the finite-probe owner, provide such
readout encodings. This is a finite precision recording operation; it
does not assert algebraicity of the underlying smooth metric or action.
Any two allowed recordings at precision \(n\) differ by at most
\(\delta_0^n\le\phi^{-n}\). Thus the Book 07 operational tolerance is
satisfied by a proved readout inequality, without requiring holonomy to
approach an identity preparation.

Here \(n\) is a measurement precision and \(j_n\) is its explicitly chosen
mesh index. The construction does not identify those indices with the
archive role-phase or Bratteli carrier indices, or prove an interlevel
pullback of gravitational operators. It supplies the observational
Catalogue/M1 instance from the finite-probe owner. Localized ten-component
readings use its separately controlled bump/mesh diagonal.

## 3. The exact sampled-Einstein tower is empty

Use the one fixed nonconstant cosine metric and its predeclared smooth
Einstein source in the unchanged ten-slot Gram covector convention:
\[
 f=1+(1-\cos(2\pi y_1))/50,\quad
 g=\operatorname{diag}(1,-1,-f^2,-f^2),\quad
 \tau=(-ff''-(f')^2/2,0,0,0,(f')^2/2,0,0,f''/(2f),0,f''/(2f)).
\]
For \(L\in4\mathbb N\), define the complete physical finite joint fiber
\[
 \mathcal X_L=
 \{K\in\mathcal L_{1/L}(g):
   E_K=0,\quad \Xi=L^{-2}\tau(x/L)\}.
 \tag{J1}
\]
The [algebraic-critical-value theorem](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md)
proves both necessary equations for a putative member:
\[
 \mathscr A_{1/L}(g,K)\in\mathbb R_{\rm alg},\qquad
 \mathscr A_{1/L}(g,K)=\pi^2L^2/1250.
 \tag{J2}
\]
The first follows from full connection stationarity of the polynomial
Lorentz action over the algebraic sampled coframe; it does not assume
algebraic link entries or a regular stationary locus. The second is the
exact Gram homogeneity identity and exact cyclotomic sum of the prescribed
source. Its nonzero rational multiple of \(\pi^2\) is transcendental.
Consequently
\[
 \boxed{\mathcal X_L=\varnothing
      \quad\hbox{for every allowed finite }L.}
 \tag{J3}
\]

This gives an unconditional obstruction to a proposed exact-source
realization map from any inhabited native finite stage into (J1).
Restricting the target by a small chart, golden coherence, a phase seam,
or any other native admission condition leaves it empty. For any refining
mesh sequence \(L_n\) and any bonding maps, a thread would first require
\(K_n\in\mathcal X_{L_n}\); (J3) prevents even one such term. The conclusion
requires no carrier weld or chosen rate of refinement.

The existing proof also covers every nonzero rational warp amplitude
\(a>-1/2\), with the forced value \(2a^2\pi^2L^2\). Such curved metrics
can be arbitrarily close to the flat metric. This is a universal
exact sampled-source realization obstruction, not a large-background
exception.

It does **not** refute an Einstein limit of approximate finite records:
the endpoint domains in (P1) impose no exact prescribed metric source.
Their nonemptiness and (J3) are fully compatible. Nor does emptiness yield
the parent response-gap NO-GO, which needs an admissible rooted sequence.

## 4. Pi0 preserves the fixed geometry when its phase is converted faithfully

The structural \(\pi_0=(6/5)\phi^2\in\mathbb Q(\phi)\) and seam \(12/5\)
retain their owned algebraic meanings. They do not alter the derivative
of the already specified smooth metric. Under a faithful smooth one-turn
bridge, with structural coordinate \(a=2\pi_0y\),
\[
 \cos_0(a)=\cos(\pi a/\pi_0),\qquad
 \cos_0(2\pi_0y)=\cos(2\pi y).
 \tag{J4}
\]
The [coordinate calculation](A4D_CANONICAL_CONSTITUTIVE_GERM_SYNTHESIS.md#42-a-structural-turn-cannot-change-a-fixed-smooth-einstein-source-by-relabeling-its-angle)
therefore preserves (J1)--(J3). Derivatives, metric coordinates and volume
must be converted together. Replacing only a source coefficient changes
the prescribed source; ordinary \(\cos(2\pi_0y)\) is not unit-periodic.

The signed Q8 witness uses integer proper rotations and the literal
Omega8 cocycle. Its support is unaffected by relabeling a half-turn with
the structural angle. Its nonidentity faces have defect at least two,
which proves exclusion from the probe's shrinking **endpoint** chart.
That fact does not prove exclusion from all native states or from the
unrestricted central slot in (P1).

Book 07's scalar operational tolerance and Cauchy stability of a flat
reference do not state the earlier proposed condition
\(\|P(K)-P(I)\|\le\phi^{-k}\) for every physical connection at every floor.
The generic GoldenTower owner takes a supplied metric and step inequality;
the archive owner preserves record kernels. Neither supplies that
connection-holonomy admission test. We do not add it as a selector.

## 5. The remaining original obligation is unchanged

On an actual exact fixed-source root,
\[
 h^{-2}(\Xi-\Xi_{\rm sm})(x)
       =\tau(hx)-\rho_{{\rm sm},h}(hx).
\]
The [finite comparator-jet endpoint](A4D_SOURCE_IMAGE_END_TO_END_ATTEMPT.md#2-the-complete-logical-endpoint)
requires \(\tau=\rho_0\) and
\(\rho_1=\rho_2=\rho_3=\rho_4=0\) on every realizable fixed pair.
Neither (P3) nor the Cauchy bound (P5) is an estimate on this response
error. For the selected Einstein-source warp the exact root fiber is
empty, so (J3) cannot be promoted to a separated-gap witness.

The synthesis establishes two finished conclusions: the centered
measurement admits every physical center and has a constructive golden
completion; a nonempty native-to-exact sampled-Einstein realization on
the selected geometry is impossible. It does not establish either
original small-chart/raw-owner task terminal. That task remains
PARTIAL / OPEN, Draft / BLOCKED, with no retirement, merge or public
claim promotion.

## 6. Validation

The center-cancellation extension, endpoint recording-error bound and
golden mesh/step estimates are the analytic proofs above. The existing
fixed-source checker passes its independent Christoffel convention,
literal Gram homogeneity, cyclotomic sums and full-Euler hostile controls.
The existing signed Q8/Klein-four checker passes all signed lifts,
shared-link, unrestricted solder and metric rows with its pinned ledger.
The pi0 owner certificate and repository architecture, generated views,
work/agent protocol, claim strength, formalization-debt, artifact-freshness,
PR-contract self-test and whitespace guards pass locally.
These checks retain the input theorems; they do not certify the unproved
full-class raw-response estimate. No Lean owner, public claim, source,
comparator, action or original task admission rule changed.
