# Complete retained quantum information of the original sequential instrument

22 October 2026. Existing scientific Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`;
`constitutive` / `native-programme-v1`.

## 0. Parent substitution and actual novelty

The parent source comparison needs the information of the **same complete
execution and retained algebra**, including preparation and conditional quantum
work. A two-port Shannon or mutual-information bound is not a bound on that
quantity. This packet computes a missing concrete component: the original
CAR16/full128 instrument, its generated inverse-square **marginal** preparation,
and the full dephased-record/DATA quantum state after one and two rounds, with
the real moving preparation and original proper-boost source. It also gives the
exact finite-stopping-tree form that keeps an actual preparation prefix.

The generic entropy chain rule, pinching identity and Gram purification facts
are standard finite-dimensional identities. They are **reused**, not claimed
as new quantum theory. The repository already owns the general coherent-record
source and a distinct primary-geometric-preparation information application:

- `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md`, §§7, 12–16;
- `A4D_PRIMARY_FULL128_COMMON_RECORD_INFORMATION_SOURCE_2026_10_20.md`;
- `A4D_NATIVE_CORRELATED_RETURN_MODULAR_HEAT_COMPATIBILITY_2026_10_22.md`,
  §§4, 6: the actual finite native predictive **pointer** information;
- `sources/d0_generated_thermal_source_2026-10-22/PRICE_AND_CAUSAL_PULLBACK.md`,
  §2: the complete CQ ledger and its conditional-work term;
- `sources/d0_native_preparation_closure_2026-10-21/PROOF.md`, §§1–5:
  the original inverse-square stationary marginal and its full source.

Those calculations are not replayed. Here the changed input is the **actual
inverse-square original Fourier/boost preparation with all native labels**, its
two-round conditional quantum work, and the exact distinction between a mixed
DATA input, a retained purification, and a separate independent spectator.
The finite-tree theorem supplies the bookkeeping map for later same-execution
substitution; it does not select a physical information functional.

The native constructor consumed by the checker is pinned to Git blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, path
`sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`.
Only its six definitions `adj, herm, tr, root, creators, native` are AST-loaded.
Its original suite is not executed. No old primary-field/root/Lean suite runs.

## 1. Exact complete-quantum telescope, including a real preparation prefix

Let a finite prefix tree describe an **efficient** instrument: each retained
label is one Kraus outcome, and all extra Kraus indices are retained as fine
labels. On a live node \(w\), let the actual operators satisfy

\[
\sum_b K_{b|w}^{\dagger}K_{b|w}=I.
\]

Keep every conditional quantum degree of freedom to which the proposed
information refers. This can include DATA, a correlated reference and additional
work. The Kraus maps act on that **whole** space, with identity factors only
where the execution really has spectators. Put

\[
X_\varnothing=\rho_0,\quad
X_{wb}=K_{b|w}X_wK_{b|w}^{\dagger},\quad
P(w)=\operatorname{Tr}X_w,\quad \rho_w=X_w/P(w).
\tag{1}
\]

The finite tree retains every terminal match and every capped abort. A paid
preparation prefix is simply an earlier part of this same tree; its records
are not replaced by a reduced stationary density. The complete final measured
CQ state is

\[
\Gamma=\bigoplus_{\gamma\in\mathrm{leaves}}X_\gamma.
\tag{2}
\]

Write \(s(X)=-\operatorname{Tr}(X\log X)\), with \(0\log0=0\).
Then

\[
\boxed{
S(\Gamma)-S(\rho_0)
=\sum_{w\in\mathrm{live}}
\left[\sum_b s(X_{wb})-s(X_w)\right].}
\tag{3}
\]

This identity follows by cancelling every nonroot internal node once with
positive and once with negative sign. It does not assume iid trials, a
classical Markov state, fresh preparations, successful postselection or a
fixed history length.

There is a useful **same-operator** interpretation of each summand. Define
the actual isometry and pinching

\[
V_w=\sum_b|b\rangle\otimes K_{b|w},\qquad
\mathcal D_w(Y)=\sum_b (|b\rangle\langle b|\otimes I)
Y(|b\rangle\langle b|\otimes I).
\]

The coherent operator \(Y_w=V_wX_wV_w^\dagger\) has the same nonzero
spectrum as \(X_w\), while

\[
\mathcal D_w(Y_w)=\bigoplus_bX_{wb}.
\]

Since \(\log\mathcal D_w(Y_w)\) is block diagonal,
\(\operatorname{Tr}Y_w\log\mathcal D_w(Y_w)
=\operatorname{Tr}\mathcal D_w(Y_w)\log\mathcal D_w(Y_w)\).
Consequently, using equal-mass relative entropy,

\[
\boxed{
\sum_bs(X_{wb})-s(X_w)
=D\!\left(Y_w\middle\|\mathcal D_w(Y_w)\right)
=P(w)D\!\left(V_w\rho_wV_w^\dagger\middle\|
\mathcal D_w(V_w\rho_wV_w^\dagger)\right)\ge0.}
\tag{4}
\]

The support required by relative entropy is automatic for a positive operator
and its pinching. Equation (4) measures the actual coherence removed by that
specific pointer cut. It is not a new heat operator or an instruction to erase
that coherence physically. Its field derivative need not be nonnegative.

Equivalently, with the true conditional law \(q_{b|w}=P(wb)/P(w)\),

\[
\boxed{
S(\Gamma)=S(\rho_0)+\sum_{w\in\mathrm{live}}P(w)
\left[H(q_{\cdot|w})+\sum_bq_{b|w}S(\rho_{wb})-S(\rho_w)\right].}
\tag{5}
\]

The familiar pointer chain rule is the first term inside the bracket.
The remaining terms telescope into the genuine conditional-quantum endpoint
term. They cannot be discarded merely because the unconditional DATA marginal
is stationary.

### A concrete Book06 maximum-entropy forgetting map

There is an exact positive application to the declared retained algebra, beyond
calling (3) an entropy candidate. Let the complete coherent stopped isometry be

\[
W=\sum_\gamma|\gamma\rangle\otimes K_\gamma,
\qquad \Omega=W\rho_0W^\dagger.
\]

Completeness of the finite tree gives \(W^\dagger W=I\). If the retained
tests are **all** block-diagonal history-by-quantum-work observables, their
expectations fix precisely the diagonal blocks \(X_\gamma\). Let
\(E\) pinch the entire final history register. Then

\[
E(\Omega)=\Gamma,
\qquad
\boxed{\Gamma=\mathop{\mathrm{argmax}}_{\sigma\ge0,\,
\operatorname{Tr}\sigma=1,\ E(\sigma)=\Gamma}S(\sigma).}
\tag{5a}
\]

**Proof.** Every such \(\sigma\) satisfies
\(\operatorname{Tr}\sigma\log\Gamma
=\operatorname{Tr}\Gamma\log\Gamma\), since the logarithm is block
diagonal. Positivity also confines \(\sigma\) to the support permitted by
its diagonal blocks. Hence

\[
D(\sigma\|\Gamma)=S(\Gamma)-S(\sigma)\ge0,
\]

with equality only for \(\sigma=\Gamma\). This proves the maximizer and
its uniqueness, including rank-deficient blocks. Applying it to \(\Omega\)
and using its isometric spectrum proves

\[
\boxed{I_{\mathrm{gain}}=S(\Gamma)-S(\rho_0)
=D(\Omega\|\Gamma),\qquad
\mathrm dI_{\mathrm{gain}}=\mathrm dS(\Gamma)-\mathrm dS(\rho_0).}
\tag{5b}
\]

Thus the exact finite execution supplies a concrete entropy-maximizing
representative for this specified Book06-style retention/loss interface. The
conditional application still requires that these are the **actually
selected** physical retained tests and the relevant Info convention. Keeping
the full coherent algebra instead gives the identity conditional expectation
and zero forgetting gain. No source is created by choosing a name for either
algebra.

In particular, the gain in (5b) is not \(S(\Gamma)\) alone when the initial
mixed marginal moves. For the native diagnostic in §5 its one-round proper
boost gain source is approximately \(-0.0148923366769\), and its one-port
invisible gain source is \(+0.0046905577066\). A real retained purification has
zero initial joint entropy and uses the corresponding distinct row in §4.

## 2. Full source on the same generated graph

On a smooth fixed-support chart, each actual source is generated by

\[
\mathrm dX_{wb}=(\mathrm dK_{b|w})X_wK_{b|w}^{\dagger}
+K_{b|w}(\mathrm dX_w)K_{b|w}^{\dagger}
+K_{b|w}X_w(\mathrm dK_{b|w})^{\dagger}.
\tag{6}
\]

The whole CQ first source is

\[
\boxed{
\mathrm dS(\Gamma)
=-\sum_\gamma\operatorname{Tr}
\big[(\mathrm dX_\gamma)\log X_\gamma\big].}
\tag{7}
\]

The terms \(+I\) in the derivative of \(s\) cancel because the complete
tree is normalized. Differentiating (3) yields exactly the sum of its full
local sources, including \(\mathrm dP(w)\), every real gate/control jet,
the initial preparation derivative, and the selected clock's actual tree.
At a support birth, a fixed-support logarithm is not a differentiability proof;
one must evaluate the actual entropy limit. A change in an integer cap is also
not an ordinary smooth derivative.

The direct pointer/work split is

\[
S(\Gamma)=H(P_\gamma)+\sum_\gamma P_\gamma S(\rho_\gamma),
\]

\[
\boxed{
\mathrm dS(\Gamma)=\mathrm dH(P_\gamma)
+\sum_\gamma\left[(\mathrm dP_\gamma)S(\rho_\gamma)
+P_\gamma\,\mathrm dS(\rho_\gamma)\right].}
\tag{8}
\]

Thus the complete Cost-minus-this-CQ-information convention, **if actually
supplied**, has source

\[
\mathrm d\mathscr S
=\mathrm d\mathbb E C-\frac{\mathrm dS(\Gamma)}{\log\varphi}.
\tag{9}
\]

All real clock/preparation/comparison/work charges stay in \(\mathbb EC\).
Equation (9) does not identify that convention with the literal bare Book03

\[
\mathcal B_N(V)=\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta_N(V)}
-\log\det(I-zF_N(V)).
\]

That identification still needs the physical retained algebra and original
operator/aggregation map; no energy term is silently inserted.

## 3. Original stationary blocks simplify without losing their work spectra

Use the unchanged original CAR16 Fourier instrument. Let

\[
p=\varphi^{-1},\quad A=A^\dagger,\quad \Delta=A^2>0,
\quad Z=\operatorname{Tr}\Delta^{-1},\quad
\rho_*=\Delta^{-1}/Z.
\]

Its actual Walsh/Julia rows are \(N_j\), \(j=0,\ldots,63\), with
\(N_0=A\). The original Kraus operators are

\[
K_{j,0}=\delta_{j0}I-2p^2N_j^\dagger A,
\qquad K_{j,1}=-2p\sqrt p\,N_j^\dagger A.
\tag{10}
\]

For every fine label, set \(G_j=N_j^\dagger N_j/Z\), and retain the
ordinary blank \(B=I-2p^2\Delta\). Direct multiplication gives

\[
\boxed{
X_{j,1}=4p^3G_j\quad(0\le j<64),\qquad
X_{j,0}=4p^4G_j\quad(j\ne0),\qquad
X_{0,0}=B^2\Delta^{-1}/Z.}
\tag{11}
\]

This is an exact simplification of the **quantum blocks**, not only their
probabilities. The nonblank output DATA is generally mixed: replacing each

\(X_{j,b}\) by its scalar trace loses its spectrum and its first source.
For two rounds the actual blocks are
\(X_{(j,b)(k,c)}=K_{k,c}X_{j,b}K_{k,c}^\dagger\); there is no iid
replacement. All \(128^2=16,384\) word slots remain in the carrier, including
the algebraically dark ones.

The actual preparation source is the owned inverse-square derivative

\[
\boxed{
\mathrm d\rho_*=-\frac{\Delta^{-1}(\mathrm d\Delta)\Delta^{-1}}Z
+\frac{\Delta^{-1}}{Z^2}\operatorname{Tr}
\left(\Delta^{-2}\mathrm d\Delta\right).}
\tag{12}
\]

It is included in (6). Dynamical stationarity of this reduced marginal does
not by itself grant a free exact preparation, erase the preparation tape,
or solve an independently varied upstream Euler equation.

## 4. The retained algebra determines which entropy the calculation means

These are different concrete output states on the same instrument. A trace or
a dephasing is specified only for computing the corresponding candidate
readout; it is not silently installed as the physical D0 choice.

| Actual initial/output convention | Complete entropy after dephasing the fine record |
|---|---|
| Mixed DATA \(\rho_*\), no correlated reference included | \(H(P_\gamma)+\sum_\gamma P_\gamma S(\rho_\gamma^{D})\) |
| A real pure purification \(\lvert\sqrt{\rho_*}\rangle\) with its reference retained in WORK | \(H(P_\gamma)\), because each conditional DATA/reference state is pure |
| Previous pure purification, but reference omitted from the readout algebra | The mixed-DATA expression in the first row |
| An additional independent, fixed maximally mixed oldRIGHT128 spectator | Add \(\log128\) to the applicable normalized entropy; add zero to its total first source |

The purifying reference and an independent spectator are not interchangeable.
If oldRIGHT itself is the purification register, it is not also counted as
an independent maximally mixed tensor factor. A moving independent spectator
has its actual additional entropy source.

For the real purification, its field jet is also retained: with
\(C=\sqrt{\rho_*}\),

\[
C\,\mathrm dC+(\mathrm dC)C=\mathrm d\rho_*,\qquad
v_\gamma=\operatorname{vec}(K_\gamma C).
\]

The conditional joint block \(v_\gamma v_\gamma^\dagger\) has only one
nonzero eigenvalue \(P_\gamma\). Its entropy/source is exactly the pointer
term. The total **coherent** DATA/reference/record state is pure, with entropy
zero; the entropy of the coherent **record marginal** is instead the owned
Gram/system-reference entropy. These three states must not share a name.

An independent oldRIGHT spectator multiplies an unnormalized log determinant
by its dimension, but it does **not** multiply normalized von Neumann entropy
by 128. Exactly,

\[
S(\Gamma\otimes I_{128}/128)=S(\Gamma)+\log128.
\tag{13}
\]

## 5. Bounded original-native source values

The checker evaluates the original Fourier phases \((i,i,-1,-i)\),
\(\nu=3/5\), \(r=1/9\), where the actual proper boost has

\[
\theta=2\operatorname{arctanh}r,\qquad
\frac{\mathrm d\theta}{\mathrm dr}=\frac2{1-r^2}=\frac{81}{40}.
\]

All displayed source units are derivatives with respect to \(r\), **not**
\(\theta\), and entropies use natural logarithms. The original stationary
input has

\[
S(\rho_*)=2.7717836482766933,\qquad
\partial_rS(\rho_*)=-0.0153666676010827.
\]

| Native execution and mixed-DATA readout | Pointer entropy source | Conditional DATA entropy source | Complete CQ entropy source |
|---|---:|---:|---:|
| One round, \(\partial_r\) | −0.0144689074544 | −0.0157900968236 | −0.0302590042780 |
| Two rounds, \(\partial_r\) | −0.0289378392451 | −0.0162134205128 | −0.0451512597578 |

The actual one-port-invisible tangent is

\[
v=\partial_r-\frac{\nu\,\partial_rh}{2h}\partial_\nu,
\qquad h=16/Z,
\]

where \(h\approx0.0137950432542459\) and the \(\partial_\nu\)
coefficient is approximately \(0.0440855159212652\). Since
\(\Delta\propto\nu^2\), this tangent exactly preserves the whole one-port
Born distribution. It nevertheless changes the full fine record and DATA:

| Native execution, direction \(v\) | Pointer entropy source | Conditional DATA entropy source | Complete CQ entropy source |
|---|---:|---:|---:|
| One round | +0.00518850954 | −0.01586461944 | −0.01067610989 |
| Two rounds | +0.01037699454 | −0.01636246289 | −0.00598546836 |

The sign changes between pointer-only and complete-CQ sources demonstrate why
one-port or two-port information cannot stand for the complete retained
information. They do not demonstrate that this full CQ readout is the
compulsory physical algebra. The input-state source in (12) is a large part
of this specific mixed-marginal diagnostic; if a genuine preparation/reference
is retained, §4 supplies the corresponding different calculation.

The new checker also retains two complete preparation rounds and all match
and abort histories on an exact rational noncommuting two-outcome fixture.
Its mass and first-source normalization are rational equalities, and its
complete entropy/source agrees with the local telescope (3). Deleting the
conditional-work source fails that comparison. This finite fixture is a
verification of the general bookkeeping theorem, not a substitute for the
original physical preparation.

## 6. What is established, and the remaining physical map

The exact result is the full finite-tree source identity, the explicit
maximum-entropy retained-algebra application, and the original native block
formula. Numerical original-native checks retain the **whole actual
amplitude** \(A_\gamma=K_\gamma\sqrt{\rho_*}\) and its derivative. They
use all squared singular values, including zeros, with no eigenvalue clipping
and no positive-mode cutoff. Only the odd Walsh rows that vanish identically
by adjacent duplicated-word cancellation are pruned from numerical work;
every physical slot remains in the carrier dimension and error bound.

The spectral calculation uses

\[
S_\eta(X)=-\operatorname{Tr}X\log(X+\eta I),\qquad
\mathrm dS_\eta=-\operatorname{Tr}\left[
\log(X+\eta I)+X(X+\eta I)^{-1}\right]\mathrm dX,
\tag{14}
\]

at \(\eta=10^{-22}\), with an additional \(\eta=10^{-24}\) diagnostic.
For a \(D\)-dimensional positive operator \(X=AA^\dagger\), the elementary
regularization bounds are

\[
0\le S(X)-S_\eta(X)\le D\eta,
\qquad
|\mathrm dS-\mathrm dS_\eta|
\le4\sqrt{D\eta}\,\|\mathrm dA\|_{\mathrm{HS}}.
\tag{15}
\]

For the second bound, differentiate
\(\lambda\log(1+\eta/\lambda)\). Its derivative is
\(b_\eta(\lambda)=\log(1+\eta/\lambda)-\eta/(\lambda+\eta)\), and
\(\sqrt\lambda\,b_\eta(\lambda)\le2\sqrt\eta\). In the eigenbasis,
\(\|b_\eta(X)A\|_{\mathrm{HS}}\le2\sqrt{D\eta}\); differentiating
\(AA^\dagger\) and using Cauchy–Schwarz proves (15), including the
amplitude limit at zero singular values. The same bound is already the
repository's owned regularization technique, used here on the new carrier.

For \(n\) actual rounds the checker keeps \(D=16\cdot128^n\) and bounds
the entire concatenated amplitude derivative by

\[
\|\mathrm dA_{\mathrm{all}}\|_{\mathrm{HS}}
\le n\left\|\sum_b(\mathrm dK_b)^\dagger\mathrm dK_b\right\|^{1/2}
+\|\mathrm d\sqrt{\rho_*}\|_{\mathrm{HS}}.
\tag{16}
\]

This follows by differentiating the product of the original isometries,
each of operator norm one. The direct computed norm is also checked against
(16). Both value and source error bounds appear in the receipt. A source
bound for the gain subtracting the initial entropy adds the initial
\(D=16\) instance of (15).

Independent five-point derivatives of the original one-round value agree
within \(2\cdot10^{-9}\). These numerical checks and their analytic
regularization bounds are not interval enclosures of floating arithmetic,
full 4D all42 tests or a uniform refinement theorem. Both ordinary and
optimized Python retain explicit checks; only `--write` creates the receipt.

This supplies the previously explicit **conditional quantum-work** term for
the specified native stationary-marginal execution and the exact map needed
to retain a finite preparation prefix. The full source comparison can now
insert that term, with the selected algebra and preparation convention stated.
It cannot use a coarse mutual-information bound to erase it or multiply it by
the oldRIGHT log-determinant factor.

The remaining parent application is still the original Book03 operator and
retained-algebra identification on one paid native execution, followed by its
real upstream equations and source/refinement map. No particular entropy in
the table is selected by this calculation. `physical_Book03_Info_identified=false`,
`GR_closed=false`; no BOOK, lifecycle or acceptance state is changed.
