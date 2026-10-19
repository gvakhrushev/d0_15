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

This endpoint calculation alone does not show that native D0 physically
admits this preparation or these link variations. A second exact test below
reapplies the same full128 rule at two assigned increments and retains both
round records. It establishes a finite sequential matrix history, while
physical admission of that step, Julia-dilation composition, and selection
and pricing by the compulsory full Cost–Info law remain separate bridges.

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

There is also an exact two-round fresh-record readout for one chosen repeated
matrix program. In round 1 apply the original full128 instrument at
\(M_A=\exp(aN_2)\) or \(M_B=\exp(b\bar N_3)\); in round 2 apply it at the
other link, with a fresh original controller/output record. Start from
\(I_{16}/16\) and retain both records. For the history whose first outcome is
index 0 (blank label, coefficient 0, port 0) and second outcome is index
19 (label 4, coefficient 1, port 1), exact differentiation gives
\[
\left.\partial_a\partial_b
  (q_{A\to B}(0,19)-q_{B\to A}(0,19))\right|_{a=b=0}
=\frac{12640131-5746707\sqrt5}{3276800000000}
\approx -6.405532799495970\times10^{-8}\ne0.
\]
The individual mixed jets are 0 in the \(A\to B\) order and
\(-12640131/3276800000000+5746707\sqrt5/3276800000000\) in the reverse
order. The exact replay builds the 128 Kraus operators from the owned
positive Julia/Walsh/golden definitions, checks their completeness, and
differentiates the two-record history. Thus this selected repeated matrix
instrument is not blind to the assigned increment order, even though the
naive relative single-flag Julia map is not a representation.

This is a scoped finite readout: the two link increments are assigned to
successive applications of the matrix instrument. It does not prove that
native D0 admits this per-increment operation or fix its compulsory
Cost–Info price. The checker reports the original endpoint and Julia tests
plus this two-round certificate; GR remains open.

## Exact rank of the complete 128-outcome probability response to all four links

The same checker now differentiates the full outcome-probability vector with
respect to all 24 independent Lorentz link tangents: each of the four link
roles is varied separately along the six-generator basis

\[
\{N_2,N_3,\bar N_2,\bar N_3,J_{23},B\},\qquad
B=E_{--}-E_{++}.
\]

At the same (L=4) background with phases ((1,1,1,i)), the full128
probability Jacobian is an exact (128\times24) matrix over
\(\mathbb Q(\sqrt5)\). Its exact rank is 6 and its nullity is 18. Every
column sums to zero, as required by normalization, and the role-2 (J_{23})
entry reproduces the exact positive pointer derivative above. This is an exact
field-rank result, not a numerical singular-value threshold.

The conclusion is limited to the 128 classical outcome probabilities, the
fixed (I_{16}/16) system marginal, this single Fourier background, and these
independent link tangents. It does not imply blindness of the retained
quantum output states, of a different preparation or a joint multi-background
experiment, and it does not characterize the physically compulsory native
Cost–Info price. It does show that this particular single-background
probability readout cannot itself identify all 24 link variations.

The retained quantum outputs carry the missing directions in this same
finite experiment. For each original outcome j, form the unnormalized branch
state sigma_j = K_j (I16/16) K_j* and its first variation
dot_sigma_j = dot_K_j K_j*/16 + K_j dot_K_j*/16. All 128 Hermitian CAR16
branch-state tangents give 32768 real coordinates. Floating QR selects 24
candidate coordinates; the checker then verifies their 24x24 minor exactly
over Q(sqrt(5)), with rank 24. Thus the outcome-labelled conditional CAR16
states locally distinguish all 24 independent link tangents, although their
128 scalar probabilities distinguish only six combinations. The checker
output records the exact minor coordinate indices; floating pivoting is used
only to choose the minor, not to establish its rank.

This is a statement about the retained mathematical output states and their
linear distinguishability. It does not prove that native D0 physically
admits these link variations, permits the required state readout, or selects
a price that includes it. The exact replay now reports 326 checks. Physical
admission, sequential D0 word execution, compulsory Cost-Info selection, and
positive GR closure remain open.

## Two-round complete classical record: one more direction, not full rank

The same 128-outcome instrument was applied twice with a fresh record at each
round, retaining all 16,384 ordered outcome pairs. Each of the 24 link
tangents is shared across both rounds. A floating QR chooses 24 history rows;
the corresponding 24x24 probability-Jacobian minor has exact rank 7 over
\(\mathbb Q(\sqrt5)\). This certifies a lower bound of seven for the full
two-round classical Jacobian. The one-round probability Jacobian has exact
rank 6, so the repeated record resolves at least one additional tangent
combination. The full Jacobian's exact upper rank is not established; its
numerical rank diagnostic is 7.

The minor's history indices are emitted by the checker. This remains a
finite repeated-matrix-instrument result with the fixed \(I_{16}/16\)
preparation and reference128 spectator. It does not show physical D0
admission of per-increment execution, selection/pricing by the compulsory
full Cost-Info law, or positive GR closure.

## Complete 128-outcome Shannon first source along the opposite-null commutator

At the same (L=4), (h=1/4), mode (k=(0,0,0,1)), role-2 link and
(I_{16}/16) preparation, differentiate the **entire original 128-outcome
probability law** along (J_{23}=[N_2,\bar N_3]). The exact checker verifies
all Kraus effects sum to (I_{16}), all 128 probability derivatives sum to
zero, and each of the 86 zero-probability outcomes at the base has a zero
Kraus operator. Thus those zero branches contribute zero to the first entropy
jet: their probabilities are (O(t^2)), and (q\log q=o(t)).

For the complete pointer Shannon term

\[
H_\varphi(q)=-\frac{1}{\log\varphi}\sum_{j=1}^{128}q_j\log q_j,
\]

the remaining 42 positive outcomes give the exact grouped-log derivative
\[
D_{J_{23}}H_\varphi
=-\frac{1}{\log\varphi}\sum_{q_j>0}\dot q_j\log q_j
=-0.0315467843124857334404386750261\ldots .
\]
The JSON receipt lists the exact algebraic base probabilities and summed
derivatives for every probability class. Rational interval arithmetic using
atanh-series bounds for the logarithms encloses this source in
\([-0.031546784312485733440439,
-0.031546784312485733440438]\), proving its sign without relying on a
floating-point evaluation. This establishes a nonzero first information
source on the actual complete finite pointer law at the stated background.

The already-owned binary golden port code assigns lengths (1,2) to
port-0/port-1. Its known code-cost contribution has first source
\[
D\mathbb E[C_{\rm port}]
=\frac{9}{800}-\frac{9\sqrt5}{1600}
=-0.0013278823734363170\ldots .
\]
Subtracting the complete pointer Shannon source from **this port-code piece
alone** leaves (+0.0302189019390494164\ldots). The other 64-record-label
costs, controller/work cost, normalization and physical event binding are not
assigned by this calculation, so this difference is not the full Book
Cost-Info source.

The zero branches also prevent promoting this first-jet result to a smooth
second-order Shannon order jet. In particular, the general mixed
\((a,b)\)-order identity for a (C^2) scalar readout cannot be applied here
without a separate rank-birth analysis. The result therefore supplies a
first-source bridge from the complete finite record toward the geometric
commutator, while keeping physical admission, the total price and the
second-order order test open.

Exact replay:

```text
python3 02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_complete_shannon_order_source.py
```
