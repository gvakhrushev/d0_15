# A4D q0 cross-character cokernel and same-carrier transport

**Task:** \`WRK-A4D-Q0-PHYSICAL-FORCING-IMAGE\`  
**Execution:** PR #278  
**Terminal:** \`J2-Q0-CROSS-CARRIER-COKERNEL-SAME-CARRIER-TRANSPORT-EXACT\`

## Result

The finite FUGU residual and the exact moving-kernel transport are both correct, but they are statements on different registered carriers.

Let the census variable be the table character \(\zeta\), and put

\[
\chi=\zeta^{-1}=\bar\zeta
\]

on the L4 unit torus. The merged symbol owner satisfies, on the two tested orbit types,

\[
\boxed{H_{AA}(\zeta)=H_{AA}(\chi)^T}.
\]

Hence the physical lower row written in table coordinates is

\[
P_\zeta=
\bigl[H_{AA}(\zeta)\mid H_{AQ}(\chi)\bigr].
\]

For the moving metric-null line

\[
d_r(z)=z_r^{-1}-1,\qquad
q_0(z)=d(z)d(z)^T,
\]

define

\[
w_j(z)=
\bigl(z_j\partial_{z_j}H_{AQ}(z)\bigr)
\operatorname{vec}_{\rm sym}q_0(z).
\]

The exact certificate separates two questions that were previously written with the same symbol \(z\).

## 1. Cross-character FUGU residual

Insert \(w_j(\zeta)\) into the physical table row \(P_\zeta\), whose metric block lives at \(\chi=\bar\zeta\).

### Orbit 5

\[
\zeta_5=(i,i,-i,-i).
\]

\[
\operatorname{rank}P_{\zeta_5}=23,
\qquad
\dim\operatorname{coker}P_{\zeta_5}=1.
\]

The four directions have image-membership pattern

\[
\boxed{(\mathrm{out},\mathrm{out},\mathrm{in},\mathrm{in})}.
\]

With the exact Hermitian cokernel projection,

\[
\|q_0(\zeta_5)\|^2=40,
\]

and the raw residual squares are

\[
\boxed{\left(\frac85,\frac85,0,0\right)}.
\]

Therefore the old floating residual \(\sqrt{8/5}\) is exact in the raw-\(q_0\) convention.

After unit-\(q_0\) normalization the residual squares are

\[
\boxed{\left(\frac1{25},\frac1{25},0,0\right)},
\]

so the nonzero unit-normalized norm is \(1/5\).

### Orbit 7

\[
\zeta_7=(-1,i,i,-1).
\]

Again

\[
\operatorname{rank}P_{\zeta_7}=23,
\qquad
\dim\operatorname{coker}P_{\zeta_7}=1.
\]

The membership pattern is

\[
\boxed{(\mathrm{out},\mathrm{in},\mathrm{in},\mathrm{out})}.
\]

Here

\[
\|q_0(\zeta_7)\|^2=92,
\]

the raw residual squares are

\[
\boxed{(2,0,0,2)},
\]

and the unit-\(q_0\) residual squares are

\[
\boxed{\left(\frac1{46},0,0,\frac1{46}\right)}.
\]

Thus the orbit-7 nonzero raw residual norm is \(\sqrt2\), and the unit-normalized norm is \(1/\sqrt{46}\).

## 2. Same-carrier moving germ

The exact null identity from #270 is

\[
H_{AQ}(z)q_0(z)=0.
\]

Differentiate it at the physical character \(\chi\):

\[
\boxed{
w_j(\chi)
+
H_{AQ}(\chi)D_jq_0(\chi)=0.
}
\]

The certificate checks this coefficient-by-coefficient for all four directions on both orbit types.

Consequently every same-carrier physical moving-germ forcing satisfies

\[
\boxed{w_j(\chi)\in\operatorname{im}P_\zeta}.
\]

All eight same-carrier obstruction classes are exactly zero.

## 3. What the nonzero FUGU number measures

The nonzero cross-character class is real algebra. It is not numerical noise and it is not removed by changing the cokernel norm.

But it compares

\[
w_j(\zeta)
\]

with a physical mixed block registered at

\[
H_{AQ}(\chi),\qquad \chi=\bar\zeta.
\]

The same-character transported forcing is \(w_j(\chi)\), not \(w_j(\zeta)\).

Therefore the hot residual measures a **carrier mismatch under the character conversion**:

\[
\boxed{
\text{cross-character residual}\neq
\text{same-carrier moving-germ obstruction}.
}
\]

This is an exact instance of the repository's registered-carrier rule: changing the character changes the primitive unless the owner is transported with it.

## 4. Relation to the Einstein / response programme

This result does not close the stationary-sheet stress task.

It removes one possible false shortcut:

- the one-dimensional physical cokernel on orbit types 5 and 7 is genuine;
- the submitted cross-character \(w(\zeta)\) can hit it;
- the actual same-carrier moving germ does not hit it, because its transported metric tangent cancels it exactly.

Thus the next physical question cannot be answered by the linear detune residual alone. It must compute the metric Euler response on a connection-stationary continuation with the source and comparator pinned.

That keeps the \(q_0\) metric lane separate from the #232/Y connection-microstructure lane. In the Y lane, #259/#275 perform genuine Euler corrections rather than character transport.

## Firewall

This memo does **not** claim:

- a stationary-sheet stress theorem;
- a nonlinear joint branch;
- a response anomaly;
- decoupling of #232/Y;
- a nonlinear Einstein theorem;
- that the physical cokernel itself vanishes.

The physical cokernel is nonzero. The theorem is that the same-carrier moving-germ forcing has zero class in it.

## Certificate

\`python3 02_REGISTRY/research/certificates/a4d_q0_physical_forcing_image_check.py\`

Expected terminal:

\`J2-Q0-CROSS-CARRIER-COKERNEL-SAME-CARRIER-TRANSPORT-EXACT\`
