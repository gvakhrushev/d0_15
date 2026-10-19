# Original full128 pointer detects an opposite-null order jet

Date: 19 October 2026. This is a finite exact extension of the existing
full128 record instrument in the same Draft #334. It tests whether an
already-defined native pointer outcome can read the commutator of two
opposite-null Lorentz links. It introduces no new gate, action, source term,
or record space.

On the original 16-component CAR carrier, use the existing retained-history
operator
\[
P_r=C_r M_r\,\mathrm{shift}_r,\qquad
d_h=h^{-1}\sum_r(P_r-C_r),\qquad D_h=d_h+d_h^*,
\]
and the original full128 golden instrument. Set \(L=4\), \(h=1/4\),
coframe weight \(\nu=3/5\), and Fourier mode \(k=(0,0,0,1)\), whose role-3
shift is \(i\). Keep all links at identity except role 2. Compare the two
proper Lorentz links
\[
M_2^{AB}=\exp(aN_2)\exp(b\bar N_3),\qquad
M_2^{BA}=\exp(b\bar N_3)\exp(aN_2).
\]
At the base point each \(C_r\) is a partial isometry, so
\(\|P_r\|=\nu=3/5<1\). The original positive Julia defects therefore
remain defined on an open neighborhood of the order jet; no new dilation
or contraction rule is introduced.
The common system preparation has marginal \(I_{16}/16\); tensoring any
fixed full-rank state on reference128 leaves the reference carrier present
and gives the same probabilities for every output.

For the actual port-0/blank-label outcome, the original golden and
reflection formulas reduce exactly to
\[
K_{00}=pI+p^2(I-2A^2)=I-2p^2A^2,\qquad
A=hD_h/16,\qquad p=(\sqrt5-1)/2.
\]
This outcome is one of the 128 physical outputs. The rest of the instrument
remains in the original complete, normalized program; the full record
channel's existing exact checker passes 60 controls.

The opposite-null commutator is
\[
[N_2,\bar N_3]=J_{23}=E_{23}-E_{32}.
\]
Direct exact differentiation of the full16 CAR lift and the native pointer
effect gives
\[
\left.\frac{\partial q_{00}(\exp(tJ_{23}))}{\partial t}\right|_{t=0}
=\left.\partial_a\partial_b
\big(q_{00}(M_2^{AB})-q_{00}(M_2^{BA})\big)\right|_{a=b=0}
=\frac{42633-14157\sqrt5}{5120000}
\approx 0.0021439425083077104>0.
\]
Thus the original complete pointer record is not blind to this Lorentz
commutator on the stated nonzero Fourier shell. The result is not the
13-effect construction: it uses an existing outcome of the original
golden128 process, with the original CAR16 and reference128 tensor factor.

The zero-momentum hostile control has \(D_h=A=0\) at the base point, so the
same pointer's first order source is exactly zero there. This confirms the
signal depends on the nonzero background Dirac mode and is not a generic
normalization artifact.

Exact replay:
python3 02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_native_full128_order_readout.py

The general 128-outcome Kraus completeness replay is:
python3 02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_record_channel.py

This closes only the finite endpoint-link readout test. It does not show
that native D0 physically admits this preparation or these link variations,
that two Lorentz steps are executable as sequential memory words, that
their Julia dilations compose, or that this pointer outcome is selected and
priced by the compulsory full Cost–Info law. The actual same-programme
composition and price remain the next physical bridge; GR remains open.

There is now an exact controlled defect for the naive one-flag candidate.
On the role-2 link with shift phase \(1\), put
\[
P(M)=\nu C_2\Lambda(M),\qquad
V(M)=\mathcal J(P(I))^*\mathcal J(P(M)),\qquad
X_\xi=D V_I[\xi],
\]
where \(\mathcal J(P)\) is the existing positive Julia dilation and
\(\Lambda(M)\) is its full16 exterior action. This relative unitary has
\(V(I)=I\). Exact Sylvester differentiation of both positive defect roots
gives
\[
\operatorname{Def}_{\rm Julia}
=[X_{N_2},X_{\bar N_3}]-X_{J_{23}}\ne0,\qquad
\operatorname{rank}(\operatorname{Def}_{\rm Julia})=10,\qquad
\|\operatorname{Def}_{\rm Julia}\|_F^2=\frac{1789}{500}.
\]
Therefore this same-flag relative Julia map is not a representation of the
Lorentz link group. This rules out that naive single-flag composition rule;
it is not a no-go for the complete program with fresh records, whose
physical per-increment operation and price are still unspecified.
The reversed-order Lie convention also fails: its defect has the same
nonzero squared Frobenius norm \(1789/500\).

The typing boundary is explicit in the owned tape: its Julia word dilates
\(P_r=C_rM_r\,\mathrm{shift}_r\), not the Lorentz matrix \(M_r\) by itself.
The result evaluates the complete instrument at an already-composed
endpoint link. Until D0 admits an operation that maps each Lorentz increment
to an executable fresh-record step on this same carrier, a direct comparison
of the Julia dilation of \(P_{AB}\) with the product of the dilations of
\(P_A,P_B\) remains only a chosen matrix comparison, not a certified
physical composition defect.
