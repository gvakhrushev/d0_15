# Native Jones record transport across actual Fibonacci levels

Research packet, 2026-10-13. Input SOURCE
`01e8047b1effacdbf623ec3189bedb63fb6732f8`; original #310 terminal remains open.
This constructs a full internal operation and an exactly compatible conditional
refinement. Physical execution/preparation and its metric/link variation are
separate obligations. No new action, selector, role or physical postulate is used.

## Result and owners

The adjacent canonical preparation corners have fixed overlap `p^3`, at every
level. Their full internal rotation is **the square of the already owned golden
gate**. It transports every corner outcome, including off-diagonal records, and
fixes its whole orthogonal complement. Ordinary inclusion alone does not
transport the corner: its trace-weighted L2 defect is the same nonzero number at every
level. The explicit composite inclusion does transport it exactly.

Owners are [the actual AF frame and native path identification](A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md),
[the trace-adjoint inclusion and full residual](A4D_NATIVE_GOLDEN_COST_REFINEMENT.md),
[the full-state preparation fiber](A4D_NATIVE_AF_TRACE_PREPARATION.md), and
`D0.Representation.GoldenOrderInterferometer.gate`. The native path proof below
is analytic; the executable certificate binds actual ordered matrices. The Lean
capsule proves 19 real-matrix kernel statements with explicit frame hypotheses;
their complex extension and actual all-level path binding have the separate
analytic/certificate status stated here.

Write `p>0`, `a>0`, `p+p^2=1`, `a^2=p`. Let

\[
 A_n=M_{A}(\mathbb C)\oplus M_B(\mathbb C),\quad
 (A_0,B_0)=(1,1),\quad (A_{n+1},B_{n+1})=(A_n+B_n,A_n),
\]

where subscripts on the pair denote sizes. The literal inclusion is
`alpha(X,Y)=(diag(X,Y),X)` and
`tau_n(X,Y)=p^(n+1)Tr X+p^(n+2)Tr Y`. All full matrix directions remain.

## All-level native path overlap

Let `J_n` be the normalized three-step GNS inclusion in the native six-path
representation from the preceding packet. Set `e_n=J_n J_n*` in `B_n=A_(n+6)`.
In `B_(n+1)`, put `G=alpha(J_n)` blockwise, `F=J_(n+1)`, `e=GG*`, `f=FF*`.
The rectangular meaning of alpha is `G_+=diag(J_n,+,J_n,-)`, `G_-=J_n,+`.
Both frames in final block `j` have rank `r_j=(A_(n+1),B_(n+1))_j`.

A native path is a sequence on the adjacency matrix `[[1,1],[1,0]]` in literal
inclusion order. A column of `J_n` of old type `k` is supported on

\[
 k,x_1,x_2,x_3,x_2,x_1,k,
 \qquad\text{coefficient }p^{(3+x_3-k)/2}.
\]

For a corresponding column of `G` and `F`, the common path is uniquely
`k,j,k,j,k,j,k,j`. Its coefficient product is

\[
 p^{(3+j-k)/2}p^{(3+k-j)/2}=p^3.
\]

Different inherited types or matrix-row coordinates have disjoint support.
Normalization follows from the actual three-step inclusion. Consequently, for
every n and every column, including all internal matrix coordinates,

\[
 G^*G=F^*F=I,\qquad F^*G=cI,\quad c=p^3.                 \tag{1}
\]

Thus `efe=p^6 e`, `fef=p^6 f`, and `tau(e)=tau(f)=p^6`. In particular

\[
 \|e-f\|_{2,\tau}^2=2p^6(1-p^6)=8p^9>0,
 \quad \|[e,f]\|_{2,\tau}^2=2p^{12}(1-p^6)>0.           \tag{2}
\]

Passive actual inclusion fails strict corner coherence uniformly; (2) does not
exclude coherence under an admitted composite operation.

## The full golden rotation is internal

Set `s=2ap>0`; `c^2+s^2=p^6+4p^3=1`. Define

\[
 Z=(F-cG)/s,\quad Z^*Z=I,\ G^*Z=0,\quad
 Q=GG^*+ZZ^*=\frac{(e-f)^2}{1-p^6}.
\]

The full operator is identity on `Q`'s complement and the literal owned
`[[a,-p],[p,a]]` on the ordered frame `[G,Z]`. In native matrices it is

\[
 H=I+\frac{(a-1)(2p+3)}4(e-f)^2
       +\frac{a(3p+5)}2(fe-ef),
\]
\[
 R=H^2=I-\frac{1+p}2(e-f)^2+(2p+3)(fe-ef).             \tag{3}
\]

Both are unitary. `HG=aG+pZ`, `RG=F`, `R e R*=f`, and more strongly
`R G X G* R*=F X F*` for **every** corner matrix X. No failed outcome or
orthogonal component is discarded. `tau(Q)=2p^6` is strictly below one.
The residual coefficient in executable polynomial form is
`Z=a(p+2)(F-p^3G)/2`; it differs from H's skew coefficient. The checker includes
the incorrect shared-coefficient mutation.

This is the oriented minimal-plane rotation fixed by (1), positive s and
identity on the complement. It is not uniqueness among all possible internal
operations. Conjugacy of a gate into a native matrix algebra does not by itself
derive its physical execution, addressing or time order.

## Exact compatible refinement and retained previous record

Define the explicit composite

\[
 \widehat\alpha_n(x)=R_n\alpha(x)R_n^*,\qquad
 \widehat C_n(y)=C_{n+6}(R_n^*yR_n).                    \tag{4}
\]

The actual coarse map splits the first block as `[[X,U],[V,Y]]` and is
`C(Z,W)=(pX+p^2W,Y)`. Thus (4) is a unital, injective, trace-preserving
*-homomorphism with trace-adjoint `widehat C` and `widehat C widehat alpha=I`.
The old Pythagorean residual identity applies after unitary conjugation; all
rectangular off-diagonal residuals are retained. Also

\[
 \widehat\alpha_n(e_n)=e_{n+1},\quad
 \frac{\tau_{n+7}(e_{n+1}\widehat\alpha_n(x))}{p^6}
 =\frac{\tau_{n+6}(e_nx)}{p^6}.                         \tag{5}
\]

The GNS isometry `x -> R alpha(x) R*` preserves the canonical unit vector and
transports the conditional vector `e_n/p^3` exactly. This gives an explicit
compatible conditional family for the composite (4). It does not change the
definition of the separately owned ordinary inclusion.

There are two distinct pictures. Conjugation transports both observable and
record labels. Left multiplication alone sends `e/p^3` to `F G*/p^3`, with
left support f and right support e. Since left and right multiplication
commute, the previous right record remains while the current left support
changes. Neither construction creates an external blank or erases a complement.
Neither construction selects the conditional branch with probability one.

## A genuine new-observable witness, with the trace control

H commutes with the embedded old `A_n`: both G and F intertwine its action.
It need not commute with newly available `A_(n+1)`. At n=0 use the fixed native
`b=(I_2,0)` in A_1, included six more times in A_7. Its exact compressed values
in the two blocks are

| frame | plus block | minus block |
|---|---|---|
| G | diag(p,1) | [p] |
| HG | diag(1-p/4,1) | [1/4] |
| F | I_2 | [0] |

Thus a fixed native observable changes on prepared individual columns. In
particular `[H,b]` in the minus block has entry `(0,2)=(1-ap^2)/4>0`.
The old observable algebra is preserved while this new observable changes.

Two essential controls: the **full tracial conditional mixtures** e/p^6,
HeH*/p^6 and f/p^6 all give b mean `2p^2`; the column changes cancel. The
unprepared canonical trace is invariant under all these inner operations.
There is no global tracial drift. Also the abstract two-plane apparatus state
of `HGx=aGx+pZx` is independent of spectator x. The previous four-frame state
`aJx+pV3x` has the same limitation. The result is transport of all pre-existing
corner outcomes plus change of specific native readouts, not creation of a
record that distinguishes arbitrary x in the apparatus alone.

There is nevertheless a specific classical record. Within the declared
prepared old-type-0 sector (the other old sector is retained), let J be the
unchanged final native block label and B the b outcome. Their joint weights
are initially `(p^2,p^3;p^3,p^4)`: J and B are independent, each with positive
outcome probability p. After R they are `(p,0;0,p^2)`: B records J exactly
and J's distribution is unchanged. This uses the prepared resource and gives
a concrete internal record of a central label, not of an arbitrary input x.

## Complete feedback for this specified Jones cut

For cut e and full operator H, `eHe=ae`, so the leakage feedback on the retained
cut is `F_1=e-eH*eHe=p^2 e`. For R it is `F_2=(1-p^6)e=4p^3 e`. On the full
regular GNS representation of A_(n+7), the rank of left e is

\[
 \sum_j r_jD_j=d_{n+4},\quad
 d_k=A_k^2+B_k^2,\quad D_j=(A_{n+7},B_{n+7})_j.
\]

Hence the complete ordinary determinants, with all ambient unit factors, are
`(1-zp^2)^d_(n+4)` and `(1-4zp^3)^d_(n+4)`. This is the **specified two-plane
gate and Jones cut**. It does not replace the preceding four-row fullStep,
the scene cut, their tensor factors or the complete heat/bootstrap action.

## Full internal correlation: exact remaining preparation freedom

On `L^2(B,tau)`, B=A_(n+7), left and right e commute. The canonical vector
Omega=1 has joint probabilities `(c0,0,0,1-c0)`, where `c0=p^6`. The two
conditional vectors are `e/sqrt(c0)` and `(1-e)/sqrt(1-c0)`; the complete vector
retains their coherence. This is an internal relative record, not an admitted
irreversible measurement or free postselection.

For any full density sigma with **both** left and right native marginals tau,
write `t=Tr(sigma L_e R_e)`. Its entire joint table must be

\[
 \begin{pmatrix}t&c_0-t\\c_0-t&1-2c_0+t\end{pmatrix},
 \qquad 0\le t\le c_0.                                 \tag{6}
\]

Every value occurs. Omega gives t=c0. Let `r=ZZ*`, `v=ZG*` and
`U=I-e-r+v+v*`. U is a full native self-adjoint unitary and `UeU*=r` is
orthogonal to e. The unit vector U has both marginals tau and t=0. Mixtures
give the closed interval. In the faithful full-state class the interval is
exactly `(0,c0)`: all joint sector projectors have positive ranks. The faithful
state `sigma_*=direct_sum_j (w_j/D_j) I_(D_j^2)` has both marginals tau and
`t_*=sum_j w_j r_j^2/D_j` strictly inside the interval. For any desired interior
t choose
`0<epsilon<min(1,t/t_*,(c0-t)/(c0-t_*))` and mix epsilon sigma_* with the two
endpoint states at `q=(t-epsilon t_*)/(1-epsilon)`. This is full and faithful.

Thus two compatible trace marginals still do not select record correlation.
Here t is a joint left/right readout on the full GNS carrier, not a function
of either native marginal. Its admission as a physical observable is not derived.
For a faithful sigma, with m=sum_j r_j(D_j-r_j)>0,
`c0-t >= lambda_min(sigma) m`. Fix beta>0. If a finite Gibbs interface is admitted, with
H>=0, minimum energy zero and maximum Emax, then

\[
 \frac{c_0-t}{c_0}\ge
 \frac{m}{d_{n+7}c_0}\exp(-\beta E_{max})>0.             \tag{7}
\]

This bound includes every mode; pure perfect correlation is a boundary, not a
finite-temperature faithful Gibbs state.

The earlier protected-zero family also has both marginals tau. With
u=w_+D_+, v=w_-D_-, u+v=1, let
`gamma_+=(u-u v^2)/(D_+^2-1)`,
`gamma_-=(v-u^2 v)/(D_-^2-1)`. Its exact mismatch is

\[
 M_R=\sum_j\gamma_j r_j(D_j-r_j)>0,\quad
 t_\lambda=c_0-(1-\lambda)M_R,\quad 1/2\le\lambda<1.
\]

The central Omega and its orthogonal central vector have zero mismatch;
only the traceless full sectors contribute. Consequently its already owned
ground-zero heat price becomes

\[
 B(t)=-\beta^{-1}\log\left(1-\frac{c_0-t}{M_R}\right),
 \quad B'(t)=-\frac1{\beta M_R\lambda}<0,                \tag{8}
\]

on this family's interval `[c0-M_R/2,c0)`. This names the free heat coordinate
as an internal correlation observable. It does not extend (8) to the whole
state fiber or prove that varying t fixes every other term of the action.

## Proof boundary and next necessary arrow

The certificate checks actual ordered frames, full matrices, all old matrix
units at declared levels, preserved complements, the new-observable witness,
ordinary/coarse refinement, feedback multiplicities and correlation controls.
Its primary and prior inputs and the Lean compiler receipt are hash pinned.
All-level identities are proved above; finite samples alone are not promoted
to all-level theorems. The Lean capsule is outside supported CORE imports.

The missing preparation/refinement matrix **now exists** as (3)-(5). What remains
is to derive whether the native preparation law admits and executes this
particular composite with its full state/correlation, and to bind its joint
variation to `(q,D,b,m)` and `D delta(q_t) D* + delta(D) q_t D* +
D q_t delta(D)* = delta(q_s)`. Formula (8) supplies an explicit correlation
direction that such a law must constrain or couple; it is not ten metric
components or their comparison with rho0. Source/Ward, stationarity, curved
native roots, soundness/recovery and physical clock/growth remain open.
The original #310 fixed-source/raw-owner terminal and independent #202/#317
criteria are unchanged.
