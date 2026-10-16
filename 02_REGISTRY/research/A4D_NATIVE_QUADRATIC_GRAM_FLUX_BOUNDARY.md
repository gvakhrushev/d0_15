# Native quadratic profiles, a Gram-affine curved pencil, and the actual flux gate

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `a30408721a3804e3d0c97fe2a210a556dbff4b67`.
Status: proved scoped research results; no claim/release promotion.

This advances the remaining native realization obligation in
[the inventory](A4D_NATIVE_REALIZATION_CLOSURE.md). The first theorem removes
positivity from the previous quadratic-profile obstruction and treats an
actual nonlinear Gram readout. The second derives the full gate and local
coframe source of the existing `fluxEnergy`. Neither theorem classifies
every nonlinear action/readout in the core. The original #310 terminal,
positive GR and global closure remain OPEN.

## 1. A signed quadratic auxiliary profile is still quadratic

At each mesh, independently specify native variables, an action quadratic
in those variables, affine preparation fibers, and all tangent variations
of each fiber. Coefficients may have either sign and depend on the mesh.
Along an affine input pencil, an affine fiber section reduces the action to

\[
 S_h(s,v)=\tfrac12v^TK_hv+v^T(r_h+s b_h)+c_{0h}+c_{1h}s+c_{2h}s^2,
 \quad K_h=K_h^T.                                             \tag{1}
\]

The gate is its actual auxiliary Euler equation
$K_hv+r_h+s b_h=0$, with no gravitational condition in its definition.
Require a solution at every point of an open pencil interval. Kernels,
saddles and increasing finite dimensions are allowed. There is no inverse,
uniform spectral gap, minimization or positivity assumption.

Choose solutions at two different fixed parameters and interpolate them.
The resulting affine $\widehat v(s)$ solves the equation at every $s$.
For any other solution $v=\widehat v+w$, $K_hw=0$, and

\[
 S_h(s,v)-S_h(s,\widehat v)
 =w^T(K_h\widehat v+r_h+s b_h)+\tfrac12w^TK_hw=0.
\]

Thus all stationary preparations have one quadratic value $F_h(s)$.
The centered difference
$[F_h(s+\epsilon)-F_h(s-\epsilon)]/(2\epsilon)$ is affine in $s$,
for any admitted nonzero $\epsilon$. No stationary root is selected and
no nongauge kernel is discarded.

An $O(h)$ half-contrast transfer with fixed $a\ne0$ and
$\epsilon_h=h^{1/3}$ would, by the owned physical probe law, make these
affine functions converge pointwise to $I'(s)$ with error $O(h^{2/3})$.
A pointwise limit of affine functions on an interval is affine: pass to
the limit in the exact interpolation identity at two anchors and any third
point. This uses neither differentiation of errors nor bounded native
quadratic coefficients. Consequently **$I'''(s)$ must vanish** on that
interval. Affine source subtraction does not change this condition.
Record/refinement errors are included only if their half-contrast error
is $O(h)$ (or $o(\epsilon_h)$ for convergence alone), as in the earlier
error-composition lemma.

## 2. A nonlinear Gram readout with an exactly affine metric pencil

Use the literal raw solder and Gram owners
`rawSolderMatrix = eta + e` and
`a4dSiteGram = Theta * eta * Theta.transpose`.
Order the roles A,B,C,D and let

\[
 \eta=\operatorname{diag}(1,-1,-1,-1),\quad
 \Omega(y)=1+\tfrac1{10}\cos(2\pi y_2),\quad
 u=(1,0,0,0)^T,\ n=(1,1,0,0)^T,
 \quad \Theta_s=\Omega\eta+s u n^T.                         \tag{2}
\]

The raw coframe is $e_s=\Theta_s-\eta$. Since $n^T\eta n=0$,
the quadratic term in its Gram readout vanishes exactly:

\[
 g_s=\Theta_s\eta\Theta_s^T
 =\begin{pmatrix}
 \Omega^2+2s\Omega&s\Omega&0&0\\
 s\Omega&-\Omega^2&0&0\\
 0&0&-\Omega^2&0\\0&0&0&-\Omega^2
 \end{pmatrix}=g_0+sV.                                     \tag{3}
\]

Both $e_s$ and $g_s$ are affine in the **same** parameter. In particular
the native endpoints at $s\pm\epsilon$ are precisely the physical
straight metric-probe endpoints. There is no moving $h$-dependent center
and no unproved transfer from straight to curved parameter paths.
For the physical probe owner's positive-determinant solder convention,
take $E_s=\Theta_s\eta$. This one fixed basis conversion preserves
the Gram metric, is affine in $s$, and has determinant
$\Omega^3(\Omega+s)>0$; it introduces no metric-dependent calibration.

For $|s|<1/4$, $\Omega\ge9/10$, $\Omega+s>0$ and
$g_{00}=\Omega(\Omega+2s)>0$. These are smooth, oriented,
time-oriented nondegenerate Lorentz metrics. Their determinant is
$-\Omega^6(\Omega+s)^2$. The base is curved: at $y_2=0$ its
literal owner scalar curvature is $2400\pi^2/1331\ne0$.
This is an off-shell geometric probe base, not a positive physical solution.

Here is a direct calculation fixing the curvature convention and sign.
Put $w=\Omega$, $p=\Omega'$, $q=\Omega''$. Constructing all Christoffel
and Ricci entries gives the standard-sign scalar

\[
 R_{\rm std}=-\frac{5p^2s^2+4p^2sw-8qs^2w-20qsw^2-12qw^3}
                         {2w^4(s+w)^2}.
\]

The owned action is $I=-\frac12\int\sqrt{|g|}R_{\rm std}$.
Its density before integration by parts is

\[
 \frac{5p^2s^2+4p^2sw-8qs^2w-20qsw^2-12qw^3}{4w(s+w)}.
\]

Periodic integration by parts, retaining every derivative of the
coefficient of $q$, therefore gives

\[
 I(s)=\int_{\mathbb T^4}
 \frac{(s+2\Omega)(5s+6\Omega)}{4\Omega(s+\Omega)}(\Omega')^2,
 \qquad I'''(0)=-\tfrac32\int\frac{(\Omega')^2}{\Omega^3}<0. \tag{4}
\]

Indeed $I'''(0)\le-30\pi^2/1331$. The coefficient has expansion
$3+s/w+s^2/(4w^2)-s^3/(4w^3)+O(s^4)$; at $s=0$ it agrees with
the independent conformal formula $I=3\int(\Omega')^2$.
Equation (4) contradicts Section 1 for every nonzero calibration.

**Scope of the Gram corollary.** It excludes quadratic native actions
with full affine auxiliary fibers over the admitted raw coframe pencil (2),
as well as those with affine fibers over the metric pencil (3).
A profile that descends to the Gram quotient has the same value in any
Lorentz-related representative, so choosing another representative does
not evade the result. Exact quotient descent is an explicit additional
condition for that last sentence. No descent theorem is assumed for an
arbitrary positive counting norm. A nonlinear fiber, metric-dependent
quadratic coefficient, moving lift with nonlinear products, or a restriction
that excludes this pencil is outside the theorem and needs its own owner.

The owned `A4DLinearizedMetricResponse.quadraticAction` is explicitly a
quadratic Euclidean response seed. Used as a standalone action with affine
metric input, it lies in this obstruction class even though it is not a
positive seam norm. Its genuine finite first-variation and gauge theorems
do not by themselves constitute a nonlinear Einstein action.

## 3. The existing flux action has an explicit local source and full gate

`A4DDiscreteEnergyKernel` owns the actual finite action and proves

\[
 E_N(e,\psi)=\tfrac12\langle\psi,(1+H_N(e))\psi\rangle,
 \qquad H_N(e)^*=H_N(e),                                    \tag{5}
\]

where the pairing is positive counting, $H_N$ is linear in $e$ and in its
field argument, and every shift/average/CAR operator is literal. Hence
its independent field equation is $(1+H_N(e))\psi=0$. Its local coframe
Euler covector, obtained from the displayed owner action, is

\[
 J_{sr}(x)=\tfrac12\delta_{sr}\sum_S\psi(x,S)\psi(x+r,S)
  -\sum_S\psi(x,S)[U_s A_r c_s^\dagger c_r\psi](x,S).       \tag{6}
\]

Here $A_r=(1+U_r^{-1})/2$. This source is local on the same carrier,
with its exact coefficient and shift order; it is not fitted to an unknown
solution. Its pairing with a coframe variation $v$ is
$\frac12\langle\psi,H_N(v)\psi\rangle$.
Equation (6) is a **coframe** source. Descent to ten metric components
and a nonlinear Lorentz/diffeomorphism Ward identity are separate issues.

For the standalone action with free coframe and field variations and no
external source, the full gate is precisely

\[
 (1+H_N(e))\psi=0,\qquad
 \langle\psi,H_N(v)\psi\rangle=0\quad\hbox{for every }v.   \tag{7}
\]

Pair the first equation with $\psi$ and use the second at $v=e$.
It gives $\|\psi\|^2=0$. Conversely $\psi=0$ satisfies every field
and coframe row at **every** $e$. Thus the full joint solution set is
exactly $\{(e,0):e\text{ arbitrary}\}$, for all finite stages.
No coframe-smallness, invertibility of $H$, or spectral assumption is used.

The [Lean capsule](certificates/a4d_native_flux_gate.lean) proves this
equivalence for the actual owner operators at arbitrary $N$, the exact
coframe and field first-variation expansions of the literal action, and
the two coercivity consequences below. The actual propositions and their
transitive axioms are captured in the [compiler output](certificates/a4d_native_flux_gate_output.txt),
with a [source-hash ledger](certificates/a4d_native_flux_gate_results.json).
Only `propext`, `Classical.choice` and `Quot.sound` occur in these six
printed axiom dependencies; no `sorryAx` occurs. No vanishing Einstein
contrast is assumed in a native gate.

The general off-shell identity is also quantitative:

\[
 \langle\psi,E_\psi\rangle-2\langle e,J\rangle=\|\psi\|^2.
\]

With all pairings weighted by the same $h^4$, bounded $\|e\|_{2,h}$
and residuals $E_\psi,J\to0$ force $\|\psi\|_{2,h}\to0$ by
Cauchy--Schwarz and $xy\le(x^2+y^2)/2$. This estimate controls this
specific field sector, not the coupled physical metric/connection solver.

## 4. Nonempty curved zero-field sector and the physical boundary

At every $L\in4\mathbb N$, set $N=L-2$ on the owned four-Role carrier,
sample $e_h(x)=(\Omega(hx)-1)\eta$ from (2), and set every cochain
component to zero. Then (7) holds exactly, the raw Gram is the sampled
curved metric $g=\Omega^2\eta$, and every local source (6) is zero.
Yet this metric is not vacuum Einstein: its scalar curvature is nonzero.
Equivalently, along $\Omega_s=1+(1/10+s)\cos(2\pi y_2)$,
$I(s)=6\pi^2(1/10+s)^2$ and $I'(0)=6\pi^2/5\ne0$.

This is a nonvacuous counterexample to obtaining vacuum Einstein
stationarity from the **standalone flux gate**, and an exclusion of that
action as the entire gravity action on this class. It is not an on-shell
solution of a different combined core action. No extra metric-only term
or constraint is added. The owner has no independent physical connection
field; these states are not asserted to solve the 24 naked-star connection
rows. Geometric sample inclusion $x\mapsto2x$ preserves these readouts,
but is not identified with the separate canonical archive modulo lift.
Additional native refinement or admissibility equations must have an
independent owner; this sequence does not certify them.

There is also a direct nonlinear Lorentz obstruction for this action on
its full cochain field space. Take a constant degree-zero field of value
one and $\Theta=\operatorname{diag}(1,-2,-1,-1)$, so only $e_{BB}=-1$.
Every $c_s^\dagger c_r$ kills that field and shifts preserve it. The
energy per site is $(1+\operatorname{tr}e)/2=0$ and the full field
Euler equation holds, while $J_{rr}=1/2$ for each role. This is a
field-stationary control, **not** a joint solution of (7).

Apply the proper rational AB boost with $c=5/4$, $b=3/4$ by
$\Theta\mapsto\Theta\Lambda$. The Gram metric and determinant are
unchanged. The owned exterior lift fixes degree zero, because its
exterior-algebra map fixes the unit. Nevertheless the energy per site
becomes $-1/8$ and its field Euler residual becomes $-1/4$.
Thus this literal action/field gate does not descend to that nonlinear
Lorentz quotient. A scalar coefficient calibration cannot repair a
nonzero orbit difference. A different field representation, restricted
sector or completed action requires an independently justified owner.

## 5. Existing positive polynomial kernels and hostile controls

For the owned family $Q_\alpha=1+H+\alpha H^2$, $H=H^T$, completion of
the square gives

\[
 Q_\alpha=\alpha(H+(2\alpha)^{-1})^2+
             (1-(4\alpha)^{-1})1.                          \tag{8}
\]

For $\alpha>1/4$ the existing positivity owner, now applied to the actual
field gate $Q_\alpha\psi=0$, forces $\psi=0$ at every geometry. It
also gives a uniform counting-norm inverse bound
$\|\psi\|\le(1-(4\alpha)^{-1})^{-1}\|Q_\alpha\psi\|$ for
fixed $\alpha>1/4$. No coefficient is selected by this fact.
At $\alpha=1/4$, $Q=(1+H/2)^2$; nonzero kernel fields can survive but
their first metric/operator variation is zero since $(1+H/2)\psi=0$.
For $\alpha=0$ a field root can have nonzero source, as the exact
constant-coframe control above shows. Zero stationary **value** must not
be confused with zero source at a field-only root.

For the uncompleted flux action, the existing owner proves positivity
when $8196\|e\|_\infty<1$. It already forces zero fields from the field
gate alone. This is a uniform finite counting bound, not a Lorentzian
Hodge coercivity theorem or the required physical range estimate.

Negative controls retain: an auxiliary kernel; indefinite stationary
saddles; a missing auxiliary equation; a nonlinear preparation outside
(1); non-null Gram directions with a genuine quadratic metric term;
field-only roots with nonzero source; and fixed nonzero external forcing.
Free field/coframe variations are essential. A normalization constraint
or an additional sourced action changes the gate and is not silently
covered by (7).

## 6. Verification and remaining gravity arrow

The self-contained [exact checker](certificates/a4d_native_quadratic_gram_flux_check.py)
replays its [immutable ledger](certificates/a4d_native_quadratic_gram_flux_results.json).
Its 60 exact controls reconstruct all Christoffel/Ricci entries of (3), the integration by
parts and strict third-derivative bound, all ten Gram differential slots,
the six Lorentz frame directions, the literal scalar Fock sector and
the proper-boost obstruction. Generic identities and analytic proofs,
rather than a finite mesh census, establish the arbitrary-stage results.

The probe theorem used for the contrast step remains the published
`af221e2fed92821c52afc88a5500774de8cd9a93` all-24/all-ten owner. No
weaker connection gate is used. The new research Lean capsule changes
no supported formalization module or registry status.

The still-open alternatives include genuinely nonquadratic native
profiles, nonlinear constraints, combined owned actions, moving-lift
couplings and physical matter sectors with their actual covariance and
refinement laws. In particular the metric-dependent heat-trace proxy and
nonlinear gauge actions require their own analysis; a file-name census
is not a completeness theorem. Native source/Ward, corrected-metric joint
existence, soundness and recovery remain downstream obligations.
