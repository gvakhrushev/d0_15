# One common exact native phase from complete words

This compiler consumes the existing addressed G/CX/source-I interface in
[native_execution.py](../d0_native_execution_domain_2026-10-24/native_execution.py)
and its full-column inverse. Its strongest mode supplies one **exact native
phase** in a certified generic stability interval, shared exactly by different
predicates. It admits no new complex, variable-angle, H, Toffoli or heralded
phase primitive. An optional comparison with π/3 remains available but is not
needed in exact-native-phase mode. Source-port availability retains the
physical qualification of that owner. Every emitted stage is an actual native
letter and belongs in the full clock and work inventory.

## Exact all-column parity identity

Let \(G=\exp(\theta J)\), where
\(J=\begin{psmallmatrix}0&-1\\1&0\end{psmallmatrix}\),
\(\cos\theta=a=\sqrt p\), \(\sin\theta=p\), and
\(p=(\sqrt5-1)/2\). Choose a distinct already allocated blank rebit \(r\),
addressed controls \(q_1,\ldots,q_K\), and a desired bit pattern
\(b\in\{0,1\}^K\). The predicate is the whole computational projector

\[
 P_b=\prod_{j=1}^K|b_j\rangle\langle b_j|_{q_j},
\]

with identity on every other register, including \(r\). For a subset
\(S\subseteq\{1,\ldots,K\}\), put

\[
 X_S=\prod_{j\in S}\operatorname{CX}(q_j,r),\qquad
 \sigma_S=(-1)^{\sum_{j\in S}b_j}.
\]

For every computational control input \(x\), and either input column of
\(r\), \(X_SJ_rX_S=(-1)^{\sum_{j\in S}x_j}J_r\). Thus, for a positive
integer \(k\), the complete native word obeys

\[
 \prod_{S\subseteq[K]}X_SG_r^{\sigma_S k}X_S
 =\exp\left[J_r k\theta\sum_S
              (-1)^{\sum_{j\in S}(b_j+x_j)}\right]
 =\exp[J_r\,2^Kk\theta\,P_b].
\]

The first displayed exponent is its control-block value; equivalently its
operator sum is \(\sum_S\sigma_S\prod_{j\in S}Z_{q_j}=2^KP_b\).
All conjugated rotations commute. Off the predicate the result is **exactly
identity**; on it the result is the indicated real rotation. This proves the
identity on the entire carrier, including control superpositions, arbitrary
unknown entangled DATA and arbitrary dirty source-port/spin input. It is not
an equality only on an all-blank or successful column.

With the conventional complex-to-real identification
\(v=u+iv'\leftrightarrow(u,v')\), multiplication by \(i\) is \(J_r\).
Consequently the formula is the realification of
\(\exp(i\phi_kP_b)\), where \(\phi_k=2^Kk\theta\). The added rebit is
an actual wire. It is not a free scalar complex phase in the original
physical carrier.

## Exact stable phase shared by different predicates

Choose a maximum predicate size \(K_{\max}\). The function
`find_stable_native_phase(Kmax, max_k, bits=96)` searches positive integer
\(k\) up to its explicit finite budget. It returns \(k\),
\(m=2^{K_{\max}}k\), and **rational enclosing intervals** for the cosine and
sine of the actual native power \(G^m\). A successful return certifies

\[
 \tfrac12<\cos\beta<\tfrac{17}{32},\qquad \sin\beta>0,
 \qquad e^{J\beta}=G^{2^{K_{\max}}k}.
\]

There is no approximation to an external phase and no phase-precision debt.
The rational bounds certify the **exact native** phase. Its coefficients
\(\cos\beta,\sin\beta\) belong to the existing field \(\mathbb Q(a)\).
`native_rotation_intervals(m, bits=...)` exposes the same integer-root and
outward dyadic powering certificate without searching. An unsuccessful
bounded search reports only failure to certify within that `max_k` and
precision. Density of the owned irrational-angle powers in this nonempty
open interval, together with convergence of the interval enclosures, gives
termination of an unbounded dovetailed search; no useful uniform resource
bound is claimed.

For each actual predicate size \(K_i\le K_{\max}\), use

\[
 k_i=2^{K_{\max}-K_i}k,
 \qquad 2^{K_i}k_i\theta=2^{K_{\max}}k\theta.
\]

`matched_phase_index(Kmax, predicate_bits, k)` returns this exact positive
integer. Thus `phase_word` for each predicate implements **the same phase**
\(\beta\) on all columns. This is an equality of native powers, rather than
two independent approximations whose mismatch would need to be priced.
The integer choice is fixed before any field variation.

The coarse interval above is chosen for generic amplification stability,
independently of an Einstein field, action, root or fitted source. It gives

\[
 b=2\cos\beta-1\in(0,1/16),\qquad a=1-b=2-2\cos\beta\in(15/16,1).
\]

In the separately justified scalar-readiness two-projector block, using this
same phase on both projectors gives failure amplitude
\(e^{i\beta}\sqrt\varepsilon(b+a\varepsilon)\). Therefore its exact failure
recurrence and derivative are

\[
 f(\varepsilon)=\varepsilon(b+a\varepsilon)^2,\qquad
 f'(\varepsilon)=(b+a\varepsilon)(b+3a\varepsilon).
\]

For \(0\le\varepsilon<1\), \(f(\varepsilon)<\varepsilon\) unless
\(\varepsilon=0\). On a compact initial range bounded away from one, a finite
uniform warmup reaches \(\varepsilon\le1/48\). There,
\(f'(\varepsilon)<(1/12)(1/8)=1/96\). This exact native choice therefore
allows the scalar failure and its first derivative to contract without any
π/3 approximation remainder. It does not itself prove the required scalar
success law, actual reflection/cut relation or whole physical source bound.

At `bits=64`, the bounded searches return the following concrete examples.
Both choose the same native exponent \(m=624\); their certified intervals in
particular lie inside
\(503/1000<\cos\beta<504/1000\) and
\(863/1000<\sin\beta<865/1000\).

| Maximum predicate size | Search bound | Returned k | Native exponent m |
| --- | --- | --- | --- |
| 2 | 156 | 156 | 624 |
| 3 | 78 | 78 | 624 |

These are bounded examples, not a general efficiency assertion. All literal
word counts below still apply to the matched \(k_i\). In particular, if
\(M=2^{K_{\max}}k\), every matched phase uses exactly \(M\) positive G
letters after inverse expansion. A zero-pattern \(K_i\)-predicate uses no
SourceI and \(K_i2^{K_i}\) CX, for \(M+K_i2^{K_i}\) total stages. A
nonzero pattern, necessarily \(K_i\ge1\), uses \(2M\) SourceI and
\(3M+K_i2^{K_i}\) CX, for \(6M+K_i2^{K_i}\) total stages. For \(M=624\)
and nonzero patterns of sizes 1, 2 and 3 these totals are respectively
3746, 3752 and 3768. No source/routing stage is absorbed into the exact phase.

## Negative letters and exact inventory

`phase_word(layout, controls, pattern, rebit, k, max_qubits=...,
max_expanded_stages=...)` returns native `Gate` objects imported from the
owned sibling packet. The interface validates the whole supplied layout,
requires the already declared blank rebit, and allocates nothing implicitly.
The return value is the macro's full word. Its caller must concatenate all
preparations, iterations, inverses and measurements at their actual interfaces
and validate the **entire** resulting execution against the full resource
bound. A bound on one phase macro is not a bound on the complete algorithm.

The rebit is distinct from the existing source port and spin. For every
negative \(G_r\) the compiler calls the owner's literal inverse expansion:
route \(r\) and the source port by SWAP; apply
`SourceI;SourceI;G(port);SourceI;SourceI`; route back. Since
\(\mathrm{SourceI}^2=Z_{\rm port}\otimes I_{\rm spin}\) and
\(ZGZ=G^\dagger\), this is exactly \(G_r^\dagger\) and identity on the
port/spin, on **all** columns. Each SWAP has three CX. The compiler keeps
these letters for each negative occurrence and credits no cancellation,
special success input or free reset. Intermediate dirty port/spin states are
part of the complete circuit and clock.

Before inverse expansion the literal product uses \(2^Kk\) signed G steps
and \(2\sum_S|S|=K2^K\) parity CX. If every desired bit is zero, all
\(\sigma_S=1\), so there are no negative steps. Otherwise exactly
\(2^{K-1}\) subsets have negative sign. Let
\(n_-=0\) in the former case and \(n_-=2^{K-1}\) in the latter. The actual
emitted primitive counts are

\[
 \#G=2^Kk,\qquad \#\mathrm{SourceI}=4kn_-,\qquad
 \#\mathrm{CX}=K2^K+6kn_-,
 \qquad N_{\rm phase}=2^Kk+K2^K+10kn_-.
\]

`phase_counts` returns these exact integers. The zero-pattern phase needs no
negative-word capability and also compiles in the G/CX profile. Other patterns
require the declared source-I profile. In particular, conjunctions of READY
ones cannot receive an uncharged inverse in the positive-only profile.

## Optional comparison with π/3

In this optional mode the target is the constant \(\phi=\pi/3\). The
external compile parameter remains the positive integer \(k\). The already owned irrational-angle theorem
implies that positive powers of \(G^{2^K}\) are dense in the rotation circle;
therefore for every fixed \(K\) and positive accuracy there is a finite
positive integer \(k\) approaching this one constant. This is not an oracle
for a field-dependent angle or a continuous native selector.

If \(G^{2^Kk}=\begin{psmallmatrix}c&-s\\s&c\end{psmallmatrix}\), the exact
full-operator error is

\[
 \|\exp(J_r\phi_kP_b)-\exp(J_r\pi P_b/3)\|_{\rm op}
 =2|\sin((\phi_k-\pi/3)/2)|,\qquad
 \varepsilon_k^2=2-c-\sqrt3\,s.
\]

All quantities in the squared-error expression are algebraic. No numerical
angle reduction or equality of transcendental prices is needed to certify a
chosen word. `phase_error_squared` returns this exact expression using the
owned algebraic-field binary matrix power.

`phase_error_bound(..., bits=96)` supplies a rational upper bound. It encloses
\(p,a,\sqrt3\) using integer square roots and outward-rounded dyadic
intervals, powers \(c+is\) by binary multiplication, and rounds the final
nonnegative square root upwards. Each component interval is intersected with
the known unit-rotation range \([-1,1]\). Its precision parameter controls arithmetic
accuracy and introduces no physical gate. Each returned upper bound is
certified even when the precision is insufficient to resolve a small error.
One can dovetail positive \(k\) and precision: at search stage \(h\), inspect
\(1\le k\le h\) at `bits=16+h`, and stop when a rational bound is below the
desired rational tolerance. Density and interval convergence guarantee
termination; this supplies a finite search procedure
without a free phase oracle. The result can be very long; its full stage count
is retained.

For a product of \(m\) unitary phase replacements, the full operator error is
at most the sum of their individual errors, by telescoping. This bound does
not discard any failed/unused/garbage column. A source-derivative bound also
requires the actual intervening preparation/unitary derivatives or paid
secant norm; constant phase accuracy alone does not prove that bound.

## Typed limitations of an amplification application

The compiler forbids controls on immutable oldRIGHT and on the source-spin
wires: the admitted interface has no individual G/CX addressing of that spin.
The source port itself may be a control because a complete inverse block
restores it on every column. An initial reflection including a blank spin
factor is **not** implemented by omitting that factor. The emitted predicate
instead has identity on spin. To use it in an amplification proof one must
establish the relevant enlarged spin-spectator invariant, scalar success law
and the relation of its reflection projector to the actual Book input cut.
This code does not assert that an arbitrary spin-selective apparatus has
that property.

The reflection predicate also excludes the realification rebit. If the actual
Book input cut fixes that rebit to zero, its return/compression is a distinct
object. A gamma-dependent common complex phase in an ideal success amplitude
can preserve the conditional DATA channel while rotating the physical rebit
and changing that actual return. Unknown DATA, controlled coherences, success
and failure flags, all raw garbage and the final rebit therefore remain in the
whole pipeline proof and in the physical Book price. This phase compiler alone
does not annul a readiness-source row or prove stationary GR dynamics.
