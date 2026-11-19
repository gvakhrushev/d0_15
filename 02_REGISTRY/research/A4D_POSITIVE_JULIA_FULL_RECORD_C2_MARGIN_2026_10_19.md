# Strictly positive complete Julia record removes the zero-outcome entropy singularity

19 October 2026. **Exact local result; same Draft #334.** This consumes the
fixed complete positive Julia/POVM tester in
[`A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md`](A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md)
and targets the compiled-record regularity gap described in the preserved
[`C_Y` input](sources/d0_instrument_to_native_price_synthesis_2026-10-19/INPUT_CY_PERRON_GR_SYNTHESIS_RU.txt).
It proves a strictly positive local margin for one specified complete
readout. It does not select Shannon entropy as the physical Book price.

## Complete all-flag readout

For \(X\in\mathfrak{so}(1,3)\) with Euclidean operator norm at most
\(r=1/100\), use the owned full-CAR16 contraction

\[
T_X=\tfrac12\Lambda(e^X),\qquad
D_X=(I-T_X^T T_X)^{1/2}.
\]

The two Julia steps use distinct retained flag banks. Read the same fixed
13-effect POVM on the CAR16 grade-1/fresh-reference output for each of the
four joint flag labels (00,01,10,11), retaining both flags and every pointer
result. This is one complete 52-outcome instrument. No success branch is
renormalized and no failure record is erased.

On the full exterior algebra, \(\|d\Lambda(X)\|\le4\|X\|\). The exact
rational checker bounds

\[
e^{4r}<\frac{1041}{1000},\quad
\|T_X-\tfrac12 I\|<\frac{41}{2000},\quad
\|D_X-\tfrac{\sqrt3}{2}I\|<\frac{13}{1000}.
\]

Consequently every two-step flag operator \(K=F_2F_1\), where each
\(F_j\in\{T_{X_j},D_{X_j}\}\), differs from its flat value by less than
\(41/1000<1/24\). At the flat point its scalar is one of
\(1/4,\sqrt3/4,3/4\). Every rank-one POVM vector has flat Choi overlap at
least \(1/(4\sqrt2)>1/6\); after the perturbation the overlap remains above
\(1/8\). Thus each of the 48 rank-one flag/pointer events has probability

\[
q_\omega>\frac1{768}.
\]

The remaining four events use \(E_{\rm rest}\succeq I/2\). Since each Julia
factor has minimum singular value above \(12/25\), each corresponding Choi
branch has probability \(q_\omega>1/40\). Hence all 52 probabilities have a
uniform positive lower bound throughout this chart. At the flat point the
four flag masses are exactly \(1/16,3/16,3/16,9/16\); summing the 13 POVM
effects within each branch recovers those masses and total probability one.

If the already specified extra Golden (F/R) bit is retained on one
rank-one event, it replaces that event by two probabilities \(p q_\omega\)
and \(p^2q_\omega\). Since \(p^2>3/8\), the resulting 53-outcome complete
record has every probability above \(1/2048\). The exact rational and
exponential bounds are independently replayed by
[`check_full_tester_positive_margin.py`](sources/d0_opposite_null_julia_order_memory_2026-10-19/check_full_tester_positive_margin.py).

## Consequence for the source and the compiled limit

For this complete readout the mean Shannon function
\(H(q)=-\sum_\omega q_\omega\log q_\omega\) is real-analytic on the
local chart. In particular,

\[
D^2H[V,W]=-
\sum_\omega\left[
(1+\log q_\omega)D^2q_\omega[V,W]
+\frac{Dq_\omega[V]Dq_\omega[W]}{q_\omega}
\right]
\]

has no (1/q_\omega) blow-up. If
\(M_1=\sup_\omega\|Dq_\omega\|\) and
\(M_2=\sup_\omega\|D^2q_\omega\|\) on the chart, then
\(\|D^2H\|\le53[(1+\log2048)M_2+2048M_1^2]\) after the optional Golden
split. This removes the zero-probability second-source obstruction for this
tester. It does not supply a parametric (C^2) compiler or prove that this
mean is the compulsory Cost−Info functional.

There is also a direct way to close the spatial \(C^2\) error in the
compiled metric readout, without differentiating the compiler with respect to
field parameters. If the exact reconstruction gives
\(\|\widehat g_h-g_h\|_\infty\le C\epsilon_h\) on every lattice site,
then a nearest-neighbour second difference obeys

\[
\|\delta_h^2(\widehat g_h-g_h)\|_\infty
\le \frac{4C\epsilon_h}{h^2}.
\]

The already owned complete-state compiler schedule has
\(\epsilon_m=16^{-m}\) and supports the refining subsequence
\(h_m=p^{5m/16}\). It gives

\[
\frac{\epsilon_m}{h_m^2}
=\left(\frac{p^{-5/8}}{16}\right)^m
<\left(\frac18\right)^m\longrightarrow0,
\]

using only \(p>1/2\). If each of an \(O(h^{-8})\) collection of site/outcome
source contributions has error \(O(\epsilon_m)\), then the same exponential
precision makes their total error vanish:
\(\epsilon_m h_m^{-8}=(p^{-5/2}/16)^m\to0\), and the existing compiler's
\(\mathrm{poly}(m)9^m\) overhead remains below its \(\varphi^{5m}\) Golden
scale. This is a valid \(C^2\)-recovery schedule provided the local
state-to-metric reconstruction is uniformly Lipschitz and the sitewise
complete-state error is the stated \(\epsilon_m\); those hypotheses must be
bound on the admitted same run. This schedule is not a derivation of the
physical clock law or of the fixed \(t(h)\) used by another price.

## Exact-root route that avoids the failed IFT shortcut

If the proposed uniform first-source estimate is independently established
for this complete instrument, it gives a continuous Euler map close to the
exact finite source. One need not obtain an approximate Hessian to turn that
into an exact finite root. On a finite-dimensional
gauge-fixed chart \(B\subset\mathbb R^n\), if the exact Euler map \(F_0\) has
nonzero Brouwer degree and

\[
\sup_{\partial B}\|F_\epsilon-F_0\|
<\inf_{\partial B}\|F_0\|,
\]

then the straight homotopy avoids zero on \(\partial B\), the degrees agree,
and the compiled map \(F_\epsilon\) has a zero in \(B\). The positive outcome
margin above makes the mean-entropy Euler map continuous on the chart; this
degree argument needs the uniform first-source comparison, not a second
derivative of the compiled price.

The attached input's proposed bound has not been replayed for this 52/53-outcome instrument, and
the degree hypothesis is also open. The next
decisive calculation is the local degree of the exact fixed-collar
\(16+24+\)matter source after its actual gauge/constraint quotient, followed
by the boundary source-error comparison for the same complete native
Cost−Info. The positive tester, the complete-record Shannon mean, the
two-tick \(J_2\), and the original (H+J+R) remain distinct prices until
the native program identifies one. `GR_closed=false`.
