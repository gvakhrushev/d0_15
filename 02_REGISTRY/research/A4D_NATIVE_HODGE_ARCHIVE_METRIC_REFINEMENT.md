# Actual archive forgetting cannot give an O(h) refinement of the full Hodge point metric

Task: existing `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input SOURCE: `025bf30c3d7c2cfba1a1d57676d65e536453b66b`.
Main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Supported D0 tree: `fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.

**Result:** the literal archive forgetting maps have a growing collapsed fibre.
For the full scalar point algebra and the owned Hodge/CAR Connes metrics,
no levelwise bijective identification of archive points with Hodge sites makes
these actual maps metric refinements with uniform error O(h). This covers
**every** such identification, not just a proposed radix encoding. It tests
the actual native transition immediately after the operator-to-metric result;
it does not introduce a heat family, action, selector or physical field law.

The exact all-level fibre statement is compiled in Lean. The metric packing
and asymptotic lower bound below are analytic, using the preceding analytic
[all-size Hodge metric theorem](A4D_NATIVE_HODGE_CONNES_METRIC.md). Neither
metric theorem is advertised as fully Lean-formalized. All eleven new Lean
propositions have only `propext`, `Classical.choice`, `Quot.sound` as applicable.

## 1. Use the actual two carriers and the actual maps

Put L=n+2. The archive points are the **flat-indexed** set

    A_L = ArchivePoints (L-2) = Fin (L^4).

Its successor projection is literally `a -> a mod L^4` from A_(L+1).
Let pi_(K,L) be the composite of these maps, for 2<=L<K. It is not
direct modulo L^4 and is not coordinatewise modulo L. For example
pi_(4,2)(81)=0 whereas `81 mod 16=1`.

The Hodge point carrier is X_L=(Z/L)^4. The previously proved actual
counting Hodge/CAR operator, on every site and all sixteen grades, gives

\[
d_L(x,y)=L^{-1}\sqrt{\sum_r\ell_r(x,y)^2},
\quad \ell_r=\min(|x_r-y_r|,L-|x_r-y_r|).                 \tag{1}
\]

Cardinality alone does not identify A_L with X_L. Consider the **complete
class of all bijections** e_L:A_L->X_L. This includes any native admitted
bijective point identification, if one is later derived. No such admission
is inferred here. The transported actual forgetting map is

\[
p^e_{K,L}=e_L\,\pi_{K,L}\,e_K^{-1}.
\]

Define its full metric distortion by

\[
\eta^e_{K,L}=\max_{x,y\in X_K}
 |d_K(x,y)-d_L(p^e_{K,L}x,p^e_{K,L}y)|.                  \tag{2}
\]

This states exactly the observable, rate and class being tested. It is not
the source-subtracted action contrast or the original raw Euler norm.

## 2. An actual growing fibre, without a substitute projection

For each integer t with L<=t<K, the label t^4 belongs to A_K. Descending
from K to t+1 leaves it unchanged: every modulus j^4 at those steps is
strictly larger. At the real arrow t+1->t, it becomes zero. Every remaining
arrow fixes zero. Therefore

\[
\pi_{K,L}(t^4)=0,\qquad \pi_{K,L}(0)=0.
\]

The labels are positive and pairwise distinct. Consequently

\[
 |\pi_{K,L}^{-1}(0)|\ge K-L+1.                          \tag{3}
\]

The Lean capsule defines the typed composite from `archiveProjection`,
proves that its value is the successive-modulus recursion, constructs these
labels and proves (3) for **all** n,k. It neither assumes regular fibre sizes
nor uses direct modulo for a long arrow. Surjectivity and record-kernel
compatibility remain the actual imported propositions.

## 3. Packing makes relabeling powerless

Let B=e_K(pi_(K,L)^-1(0)). It has at least K-L+1 distinct points. All have
the same coarse image, so (2) implies their d_K diameter is at most eta.
Choose one point of B as centre. If d_K(x,y)<=eta, each cyclic coordinate
distance is at most K eta. At most `2 floor(K eta)+1` coordinate values
are possible, with wrapping only reducing that count. Four coordinates give

\[
 K-L+1\le |B|\le(2\lfloor K\eta\rfloor+1)^4
                 \le(2K\eta+1)^4.
\]

Thus, for every e_L,e_K,

\[
\boxed{\eta^e_{K,L}\ge
       \frac{(K-L+1)^{1/4}-1}{2K}.}                     \tag{4}
\]

There is no coordinate assumption or dimension estimate from a numerical
rank in this proof. The native fibre cardinality and the exact full Hodge
metric suffice. Changing the common nonzero distance calibration multiplies
both sides by its absolute value and does not repair the rate.

## 4. The declared physical mesh family already witnesses the obstruction

Take L in 4N and K=2L, also in 4N. These are real archive levels and their
real composite arrow; a new one-step map is not installed. Equation (4) gives

\[
\eta^e_{2L,L}\ge\frac{(L+1)^{1/4}-1}{4L},\qquad
\frac{\eta^e_{2L,L}}{h_L}\ge\frac{(L+1)^{1/4}-1}{4}
                  \longrightarrow\infty,
\quad h_L=L^{-1}.                                     \tag{5}
\]

Equivalently, eta<=C/L would require L+1<=(4C+1)^4. For any fixed C this
fails at all sufficiently large L in 4N. This proves the complete stated
O(h) obstruction. Its lower bound is of order h^(3/4); **optimality or
an upper bound of that order is not proved**. It does not rule out o(1)
distortion at a slower rate.

The ordinary finite metric nets still approximate the flat torus within 1/L
using other correspondences. That fact does not make the owned pi maps those
correspondences. A bound on each immediate arrow also does not supply the
uniform long-arrow estimate in (5).

## 5. Consequence for the preparation question

The actual fixed Hodge triple supplies a flat metric, but its full scalar
point reading cannot simply be declared the O(h) physical refinement of the
actual condensed archive. Searching another numbering cannot fix this:
the tested class already contains all numberings.

The next T0 arrow must derive the **physically admitted represented
observable algebra/readout and its transitions** from the internal
preparation, retaining the complete archive in the full price. It may be
different from the full bijective scalar reading tested here; the native
detector, recording and comparison rules must establish that difference.
No new quotient, deletion of memory, clock, time calibration or selector is
chosen to evade (5). A weaker physical refinement requirement must be stated
and proved sufficient for its actual contrast/source theorem.

This is not an obstruction to every operator preparation or every physical
metric. It does not identify phi archive scale with h_L, establish failure
of O(h) action contrasts, imply absence of Gamma/F throughout the core, or
prove a source/Ward/curved-root/GR terminal. The full joint X=(q,D,b,m),
its true constraint tangent, all ten metric slots and independent link
equations remain required. All 44 dependency contracts and original
#310 fixed-source/raw-owner, #202 and #317 obligations are preserved.

