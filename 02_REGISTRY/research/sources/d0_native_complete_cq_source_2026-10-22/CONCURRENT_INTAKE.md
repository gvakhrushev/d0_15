# Concurrent stopped-price, preparation-Poisson and stage-cut intake

22 October 2026. Existing scientific Draft #334. Read-only source comparison;
no concurrent checker is replayed, no frozen proof/checker/receipt is changed,
and no physical Book03 or GR status is promoted.

## 1. Exact inspected sources

The following files were read through the GitHub connector at the immutable
commit **e02855b68a1de758436b0e80c1ee98171bc5c4f4**:

| Source | Git blob at inspected commit | Scope actually inspected |
|---|---|---|
| [check_native_entropy_poisson.mjs](https://github.com/gvakhrushev/d0_15/blob/e02855b68a1de758436b0e80c1ee98171bc5c4f4/02_REGISTRY/research/sources/d0_native_preparation_entropic_poisson_2026-10-22/check_native_entropy_poisson.mjs) | d546707c0051a8a9ecf3f3d9f9b1472960fb4ef9 | Complete finite stopped price and preparation cotangent on the existing noncommuting two-Kraus fixture; generic stationary-Poisson application |
| [A4D_BOOK03_STAGE_CLOCK_INTERNAL_CUT_NECESSITY_2026_10_22.md](https://github.com/gvakhrushev/d0_15/blob/e02855b68a1de758436b0e80c1ee98171bc5c4f4/02_REGISTRY/research/A4D_BOOK03_STAGE_CLOCK_INTERNAL_CUT_NECESSITY_2026_10_22.md) | 7ed483d072d88efaca1b768a12ecf0704070ce66 | Exact clock-only blindness, a declared internal Q8 cut, and the conditional Golden cost-as-clock fork |

The Poisson checker originated in commit
ccfa9ca0314838f1704079a700839d2534101546. The version above includes the
subsequent supplied-mixed-input and moving-stationary-input corrections.
Only that corrected version is consumed here. No claim about the outcome of
replaying its executable is made by this intake.

## 2. The preparation calculation is complementary to the full128 result

The concurrent executable uses the already owned two-dimensional channel

\[
K_0=\begin{pmatrix}a&0\\0&b\end{pmatrix},\qquad
K_1=\begin{pmatrix}0&\sqrt{1-b^2}\\
\sqrt{1-a^2}&0\end{pmatrix},
\]

with its unique stationary density

\[
\rho_*=\frac{\operatorname{diag}(1-b^2,1-a^2)}{2-a^2-b^2}.
\]

It retains every matched and capped-abort first-return word. Its cost ledger
is the **declared** binary length \(\sum_j(1+b_j)\); the source explicitly
does not identify those lengths with a physically selected Golden price of
this two-Kraus channel. The Kraus operators do not commute, but diagonal
initial DATA stays diagonal on every complete word. Thus the code can compute
the complete conditional DATA entropy from its actual diagonal eigenmasses
without pretending that a generic full128 DATA block is diagonal.

For a complete word \(L_\gamma\), quantum block
\(X_\gamma=L_\gamma\rho L_\gamma^\dagger\), probability
\(p_\gamma=\operatorname{Tr}X_\gamma\), and
\(\ell=\log\varphi\), its two separately declared objectives have actual
initial-density cotangents

\[
\begin{aligned}
\mathscr S_{\rm ptr}
&=\sum_\gamma c_\gamma p_\gamma
+\ell^{-1}\sum_\gamma p_\gamma\log p_\gamma,\\
M_{\rm ptr}
&=\sum_\gamma
\left[c_\gamma+\ell^{-1}(\log p_\gamma+1)\right]
L_\gamma^\dagger L_\gamma,
\end{aligned}
\tag{1}
\]

and, on the stated smooth-support domain,

\[
\begin{aligned}
\mathscr S_{\rm CQ}
&=\sum_\gamma c_\gamma p_\gamma-S(\Gamma)/\ell,\\
M_{\rm CQ}
&=\sum_\gamma L_\gamma^\dagger
\left[c_\gamma I+\ell^{-1}(\log X_\gamma+I)\right]L_\gamma.
\end{aligned}
\tag{2}
\]

The corresponding general stationary-channel adjoint is

\[
(I-\Phi^*)Y=M-\operatorname{Tr}(\rho_*M)I,
\qquad \operatorname{Tr}(\rho_*Y)=0.
\tag{3}
\]

Where the original channel has the owned unique stationary state and strict
mixing inverse, (3) gives the full preparation source

\[
\boxed{
\operatorname{Tr}(M\,\mathrm d\rho_*)
=\operatorname{Tr}\big[Y\,(\mathrm d\Phi)(\rho_*)\big].
}
\tag{4}
\]

It follows by differentiating \(\Phi(\rho_*)=\rho_*\), not by setting the
input source to zero. In particular the constrained density Euler row of
\(\mathscr S+\operatorname{Tr}Y(\Phi(\rho)-\rho)\), with normalization
multiplier retained, closes at (3). The selected physical stationary-input
constraint, an exact finite preparation, its retained prefix and its full
price still require their actual application; a Poisson multiplier does not
select those assumptions.

This is useful input for the same-execution source chain. The present packet
adds a **different concrete application**: the original CAR16/full128
Fourier/boost instrument, its actual inverse-square preparation, both original
parameter jets, complete one/two-round quantum blocks, and explicit
purification/spectator and retained-algebra comparisons. The concurrent
two-Kraus test is not a full128 calculation or a substitute for those values.
Conversely our full128 entropy calculation does not yet evaluate the entire
original stopped Cost-plus-all-Info cotangent \(M\). Neither result is a
new all42 physical Book03 root.

## 3. CQ entropy and maximum-entropy gain are different objectives

The new complete-history theorem supplies the actual pinching maximizer for
the declared full block-diagonal history/work tests:

\[
I_{\rm gain}=S(\Gamma)-S(\rho).
\]

The concurrent CQ-price code uses \(S(\Gamma)\), not that difference.
They can be composed exactly, but must not be identified without its
initial-state term. If

\[
\mathscr S_{\rm gain}=\mathbb EC-I_{\rm gain}/\ell,
\]

then

\[
\boxed{
\mathscr S_{\rm gain}=\mathscr S_{\rm CQ}+S(\rho)/\ell,
\quad
M_{\rm gain}=M_{\rm CQ}-(\log\rho+I)/\ell,
\quad
\mathrm d\mathscr S_{\rm gain}
=\mathrm d\mathscr S_{\rm CQ}+\mathrm dS(\rho)/\ell.
}
\tag{5}
\]

For the same stationary channel, obtain its actual preparation multiplier
by applying the existing Poisson inverse to the correspondingly centered
right-hand side. In the canonical \(\rho_*\)-mean-zero gauge,

\[
Y_{\rm gain}=Y_{\rm CQ}
-\ell^{-1}(I-\Phi^*)^{-1}_{\perp}
\left[\log\rho_*-\operatorname{Tr}(\rho_*\log\rho_*)I\right].
\tag{6}
\]

The source correction in (5) is therefore a genuine same-input transport,
not a fitted residual or an erased preparation source. In particular, the
current native diagnostic has
\(\partial_rS(\rho_*)\simeq-0.0153666676011\), so treating that term as
constant would materially change the result.

On an actually retained **pure** preparation graph, the initial joint entropy
is zero and each conditional DATA/reference block is pure. Then CQ entropy,
fine pointer entropy and the above forgetting gain coincide on that graph.
An independently mixed DATA input is a different retained-algebra case.
The concurrent code explicitly checks this purification distinction, in
agreement with the present packet. An additional independent oldRIGHT128
spectator adds \(\log128\) to normalized entropy; it does not multiply the
entropy source by 128.

## 4. The stage-cut theorem constrains the remaining Book map

The concurrent clock theorem addresses the original reversible sixteen-stage
machine

\[
\mathcal U=\sum_{c\in\mathbb Z_{16}}
|c+1\rangle\langle c|\otimes V_c(y).
\]

For a clock-only active cut
\(P_S=\sum_{c\in S}|c\rangle\langle c|\otimes I\), its actual
complementary feedback is

\[
J_S^{(j)}
=-d\,\#\{c\in S:c+j\notin S\}\log(1-z),
\qquad D_yJ_S^{(j)}=0.
\tag{7}
\]

This is independent of the internal field-dependent unitary products. It
does not imply that the full retained record has zero Shannon/CQ information
source. It proves instead that a varying record distribution cannot, by
itself, identify that information source with this **particular** Book
feedback.

For an internal stage-diagonal cut \(P=\bigoplus_cQ_c\), the retained
principal-angle operators act on \(\operatorname{ran}Q_c\); each identity
and trace below is on that active range:

\[
T_c=Q_cV_c^{(j)*}Q_{c+j}V_c^{(j)}Q_c,\qquad
J_P=-\sum_c\operatorname{Tr}\log[(1-z)I+zT_c].
\tag{8}
\]

The original Q8 consumer supplies a positive **discrete program contrast**
for one expressly declared record0-selective start/end cut. It does not
select that cut physically or give a continuous all42 source. The Golden
cost-clock residue argument is separately conditional on identifying the
code-cost counter with that elapsed stage register; the source does not
make that identification.

Our entropy conditional expectation \(E\) acts on the **operator algebra**,
while the Book active projector \(P_N\) acts on the physical Hilbert space.
They are different mathematical objects. The new block-algebra pinching
maximum-entropy theorem does not select an internal \(Q_c\), and the Q8
projector does not select the pinching Info convention.

The remaining same-execution application must therefore provide the actual
retained test algebra, internal stage-conditioned Book cut, native heat,
complete price and real preparation map, with their source transport.
The two concurrent inputs strengthen and delimit that application; they
neither invalidate the frozen full128 information calculation nor identify
its selected physical Book03 scalar. Physical GR remains open.
