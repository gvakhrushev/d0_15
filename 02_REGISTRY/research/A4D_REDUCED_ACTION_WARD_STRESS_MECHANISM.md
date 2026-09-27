# A4D — reduced-action Ward mechanism for on-shell stress cancellation

Status: CONTROL synthesis. Owned inputs, reported exact calculations awaiting a
durable certificate, and open proof obligations are separated below.

## 1. Replace frozen NF by an on-shell statement

The old frozen quadratic criterion asks for

\[
v^\dagger D_QH_Q(z)[q]v=0
\]

on every relevant linear joint-kernel vector. PR #240 has exact frozen
counterexamples, while the same shear carrier can still fail to extend to a
nonlinear joint-critical branch. Therefore zero frozen moment is too strong.

After eliminating regular/range connection variables on one finite stratum,
write the reduced action as

\[
\mathcal S_{\rm red}[Q;a],\qquad a=(u,v,\ldots).
\]

On a solution of the eliminated equations, the envelope principle identifies
the metric response with the metric derivative of this reduced action. The
load-bearing question is therefore whether that derivative vanishes on shell.

## 2. Candidate theorem: metric Ward exactness

For each physical metric variation q, seek local amplitude variations
\(X_q^u,X_q^v,\ldots\) and a lattice current \(J_q\) such that

\[
D_Q\mathcal L_{\rm red}[q]
=
E_u(\mathcal L_{\rm red})X_q^u
+
2\operatorname{Re}\!\left(E_v(\mathcal L_{\rm red})^\dagger X_q^v\right)
+\cdots+
\operatorname{Div}J_q.
\tag{W}
\]

If (W) holds, then on a periodic stationary solution all reduced Euler
operators vanish and the integrated metric stress is zero because the total
divergence sums to zero.

This mechanism can simultaneously explain:
- moving-germ continuation as an explicit horizontal lift;
- the response-silent nonlinear #232 sector;
- a nonzero frozen #240 shear moment which becomes Euler-exact only after all
  coupled amplitudes are included.

The theorem is weaker than global frozen NF and stronger than an accidental
numerical cancellation on one branch.

## 3. Homogeneity constraint

For the owned action structure, the connection Hessian is homogeneous in the
metric slot in the relevant convention:

\[
D_QH_Q[Q]=H_Q.
\tag{H}
\]

Hence for \(b\in\ker H_Q\),

\[
b^\dagger D_QH_Q[Q]b=b^\dagger H_Qb=0.
\]

So the quadratic defect covector
\(q\mapsto b^\dagger D_QH_Q[q]b\) annihilates the radial metric direction Q.
At \(Q=\eta\) this is the appropriate Q-trace / scale-trace zero condition;
do not silently replace it by an unrelated Euclidean trace convention.

The reported observation that both known frozen NF defects point along a zero
leg of the solder is compatible with a normal, scale-trace-free defect. It
does not by itself prove (W), but it identifies the first metric directions
for the Ward test.

## 4. New envelope datum and the scope of #240

Current PR #240 owns a shear-only slow-envelope calculation for its declared
ansatz. A newer calculation reports an exact coefficient for an admissible
one-dimensional envelope after the required reduction: the projected
second-order linear response is

\[
\frac{35}{2}.
\tag{E35}
\]

The regular leading envelope therefore satisfies \(U''=0\); on a torus its
leading solution is constant.

This coefficient is not yet present in a merged durable certificate at the
time of this synthesis. Treat (E35) as a reported exact input awaiting owner
pinning, not as a replacement terminal for #240.

More importantly, a shear-only ansatz is structurally incomplete at the same
nonlinear order as the owned \(-432u^5\) term.

## 5. Minimal coupled two-field normal form

Let
- u be the shear amplitude with physical scaling \(u=O(h)\);
- v be a diagonal response-null / joint-invisible amplitude with
  \(v=O(h^2)\).

Then

\[
u|v|^2=O(h^5),
\]

the same amplitude order as \(u^5=O(h^5)\). Thus the first nonlinear reduced
equation cannot be certified from the shear mode alone.

The minimal u-equation has schematic form

\[
\frac{35}{2}\Delta_{\rm slow}u
-432u^5
+\gamma u|v|^2
+\text{other symmetry-allowed weighted-order-5 terms}
=0,
\tag{R_u}
\]

where \(\gamma\) must be computed from the literal reduced action.

If the system is variational, the mixed coefficient is not free. A reduced
potential term

\[
\frac{\gamma}{2}u^2|v|^2
\]

forces a companion \(u^2v\) term in the v-Euler equation with the coefficient
fixed by mixed-partial symmetry.

Mandatory hostile control: a scalar \(u|v|^2\) correction is not accepted as
the mechanism unless the companion v-equation is recovered from the SAME
reduced action with the matching mixed derivative.

A coupled constant branch can satisfy

\[
-432u^5+\gamma u|v|^2+\cdots=0
\]

even when the shear-only equation forces u=0. Therefore the current one-mode
exclusion does not exclude the full \(u=O(h),v=O(h^2)\) stationary system.

## 6. How stress can disappear without restoring frozen NF

Let the reduced metric defect in a physical direction q be

\[
T_q(u,v,\nabla u,\nabla v,\ldots)
=
D_Q\mathcal L_{\rm red}[q].
\]

The desired theorem is not \(T_q\equiv0\) off shell. It is

\[
T_q
=
E_u X_q^u
+
2\operatorname{Re}(E_v^\dagger X_q^v)
+
\operatorname{Div}J_q
\tag{Wq}
\]

through the first load-bearing weighted order.

Then the frozen shear moment may be nonzero, while the \(u|v|^2\) coupling
transfers the defect into the v-Euler equation. On a coupled stationary
solution the metric stress vanishes.

This is the precise mechanism by which #232, the moving germ, and the shear
defect can belong to one variational story without being the same carrier.

## 7. Relation to the merged Veronese programme

The merged Veronese programme owns the linear complex \(P_d\to C(d)\) and
the distinction between metric homology, joint defects, and the
connection-only N0 sector.

The present memo adds the nonlinear layer:

- germ / optical sector: horizontal continuation is the first example of an
  Euler-exact metric variation;
- shear sector: frozen metric moment is nonzero, so any cancellation must be
  nonlinear Ward exactness rather than linear nullity;
- #232 / N0 sector: supplies the natural response-null v-field which can
  couple at the same weighted order as \(u^5\).

The question is no longer whether these carriers are identical. It is whether
their amplitudes occur in one reduced variational system whose metric
derivative is Euler-exact on shell.

## 8. Exact proof programme

### A. Pin the new exact inputs

Durably certify:
1. the two known frozen defects and the claimed zero-solder-leg alignment;
2. homogeneity identity (H) in the exact owner convention;
3. the \(35/2\) projected second-order envelope coefficient, including every
   range correction performed before projection.

Until item 3 is pinned, keep #240 section 8.21 as correct for its narrower
ansatz but do not promote it to a theorem about the full coupled reduction.

### B. Reconstruct one reduced action

Eliminate the regular/range variables to the first order at which

\[
u^5,\qquad u|v|^2
\]

coexist. Record the reduced scalar functional itself, not independently
guessed Euler equations.

Required controls:
- differentiate it independently to recover u- and v-equations;
- verify equality of mixed derivatives;
- include the owned amplitude-reparameterization freedom;
- preserve fixed-source and carrier conventions.

### C. Compute the metric derivative

For the ten metric basis variations compute
\(D_Q\mathcal L_{\rm red}[q]\). Use (H) as a mandatory radial/trace negative
control.

### D. Solve the Ward-exactness system

At the first load-bearing weighted order solve coefficientwise for
\(X_q^u,X_q^v,J_q\) in (W).

Candidate exact terminals:
- A4D-REDUCED-METRIC-STRESS-WARD-EXACT if every physical defect direction is
  Euler-exact modulo divergence;
- A4D-REDUCED-METRIC-STRESS-COHOMOLOGY-NONZERO if a residual functional
  survives the Euler ideal and divergence quotient.

The second object would be the clean nonlinear stress carrier sought by #240:
not a frozen moment, but an on-shell variational cohomology class.

### E. Only then solve periodic branches

If Ward exactness holds, periodic stationary solutions have zero integrated
stress independent of which coupled branch is realized.

If it fails, solve the coupled periodic system and evaluate the surviving
class on those branches. A nonzero value is a genuine response-anomaly
candidate.

## 9. Consequence for active executions

- #240: the shear-only slow envelope remains a valid narrow calculation but
  does not exclude coupled \(u=O(h),v=O(h^2)\) branches.
- #260/#275: the diagonal N0 seam is a candidate v-field in the SAME weighted
  nonlinear system as the shear defect, not merely a later correction.
- #232: remains the key nonlinear response-silent control.
- #270/#278: retain the linear moving-germ / horizontal-lift role and do not
  by themselves prove nonlinear stress cancellation.

## 10. Firewall

This synthesis does not claim:
- that \(35/2\) is merged owner truth before its certificate is pinned;
- that zero-leg alignment proves a Ward symmetry;
- that the coefficient \(\gamma\) is nonzero before literal expansion;
- that integrated zero stress implies pointwise zero stress;
- that #232, shear, and germ are the same carrier.

The new mechanism is the exact test

\[
\boxed{
D_Q\mathcal L_{\rm red}
\in
\langle E_u,E_v,\ldots\rangle+\operatorname{Div}
}
\]

on the relevant weighted reduced sector.

If true, stress cancellation is structural. If false, the remainder is the
correct nonlinear stress observable.
