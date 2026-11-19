# Full finite execution → one declared Book03 clock sector

This packet makes the finite execution data into actual matrices on every
column. It applies the existing Book03 scalar

\[
 B_{\beta,z}(\Delta,F)=\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta}
                         -\log\det(I-zF),\qquad \beta>0,\quad0<z<1.
\]

The scalar is [Book03 §03.25](../../../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#0325-cvft-master-bootstrap-action).
The chronological clock/Hodge construction is already owned by
[same-representative §7k, (101)–(102)](../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#7k-recover-the-original-spatial-operator-from-the-same-complete-recorded-clock)
and [paid writer §13.3](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#133-all-33-scene-modes-the-literal-cyclic-clock-and-their-source).
The data here declare its bare finite execution sector. They do not identify
that sector with an originally selected spatial operator, the full scene, a
Cost−Info law, or an Einstein action. In particular, the Book03 stationarity
sentence does not prove that the current execution is stationary.

## Actual domain and full carrier

`native_execution.py` specifies the finite alphabet, bounded wire/primitive
counts, fresh zero blanks, arbitrary nonblank input and immutable oldRIGHT.
Its `gate_matrix(execution, gate)` returns each exact **full** primitive matrix;
`cut_projector(execution)` returns \(P_0=J_0J_0^\dagger\), including all arbitrary
input columns. Supply these matrices to `book_price.build_clock`. A successful
matrix-unitarity test establishes a matrix identity, not membership in this
native alphabet; primitive validation belongs to `native_execution.py`.

There is no selected internal programme/key block in this construction. If a
programme is an internal register of one decoder, its entire carrier and all
decoder branches enter each supplied gate and the heat trace, even when the
input projector prepares one key. Different externally specified words are
different operator configurations. These two representations cannot be
exchanged inside a heat trace.

Let the complete chronological primitive list be \(g_0,\ldots,g_{N-1}\), each
unitary on \(\mathcal H\cong\mathbb C^D\), and require \(N\ge1\). All actual
preparation, flags, dirty workspace, retained programme/environment, required
copying, closing inverse and middle stages belong to this list. A macro is not
one stage. No free closing identity is inserted. The empty native word has no
clock instance in this implementation; adding a real stage changes the word.

Write

\[
 W_0=I,\quad W_j=g_{j-1}\cdots g_0,\quad W=g_{N-1}\cdots g_0,
 \qquad
 T(|j\rangle\otimes v)=|j+1\bmod N\rangle\otimes g_jv.
\]

The full stage carrier has dimension \(ND\); every primitive is represented on
all columns. \(T^\dagger T=TT^\dagger=I\). With the unitary identification of
edge and vertex copies, define

\[
 d=(I-T)/\sqrt2:\mathcal H_0\longrightarrow\mathcal H_1,
 \quad\Delta_0=d^\dagger d,\quad\Delta_1=dd^\dagger,
 \quad\Delta=\Delta_0\oplus\Delta_1.
\]

Both blocks equal \(I-(T+T^\dagger)/2\), and \(0\le\Delta\le2I\). The heat
carrier has dimension **\(2ND\)**. Its trace has no input projector and no
division by dimension or rank. Every zero mode contributes one. The evaluator
diagonalizes one complete \(ND\)-block and multiplies its heat trace by two;
this uses the exact equality of the two blocks, rather than discarding modes.
The formulas work for \(N=1,2\); extracting oriented edges from the Laplacian
alone has the separate small-cycle qualification in the existing owner.

## Literal prefix cut and closing return

The stage cut and the chosen paired cut are

\[
 P_j=W_jP_0W_j^\dagger,\qquad
 P_{\rm hist}=\bigoplus_{j=0}^{N-1}P_j,\qquad
 \widehat P=P_{\rm hist}\oplus0,
 \quad\widehat T=T\oplus T.
\]

This explicitly puts the input cut in degree zero. Its rank is \(N r\), where
\(r=\operatorname{rank}P_0\). The corresponding actual return defect is

\[
 C=(I-P_{\rm hist})TP_{\rm hist},\qquad
 F_{\rm hist}=C^\dagger C
 =P_{\rm hist}T^\dagger(I-P_{\rm hist})TP_{\rm hist},\qquad
 \widehat F=F_{\rm hist}\oplus0.
\]

`build_clock` computes every block of \(C\) from this full-carrier formula and
then \(C^\dagger C\). For each nonclosing edge,
\((I-P_{j+1})g_jP_j=0\), by the actual prefix identity. The sole possible
nonzero feedback block is at input stage \(N-1\). Conjugating that block by
\(W_{N-1}\) gives exactly

\[
 E_W=P_0W^\dagger(I-P_0)WP_0,\qquad0\le E_W\le P_0,
 \qquad\operatorname{rank}F_{\rm hist}\le r.
\]

Consequently, on the full specified carriers,

\[
 \det(I_{2ND}-z\widehat F)
 =\det(I_{ND}-zF_{\rm hist})
 =\det(I_D-zE_W),\qquad
 B=\beta^{-1}\log\bigl(2\operatorname{Tr}_{ND}e^{-\beta\Delta_0}\bigr)
       -\log\det(I_D-zE_W).
\]

Feedback occurs once, independently of the \(N\) copies of the input-cut
rank. The pair \(P_{\rm hist}\oplus P_{\rm hist}\) would instead double the
feedback term; this is a different explicitly chosen cut. The full \(D\)-mode
endpoint determinant includes its zero modes and is only an exact spectral
reduction of feedback. It never replaces the full heat by a prepared block.
For input isometry \(J_0\), the equivalent compressed defect is
\(I_r-(J_0^\dagger WJ_0)^\dagger(J_0^\dagger WJ_0)\).

The Python API returns the exact operators and prefixes. `feedback_expression`
returns the exact determinant expression. `exact_price` produces a spectral
expression only when its exact eigensolver returns **all** heat modes within
the explicit fixture limit. `evaluate_price` evaluates the actual finite
matrices numerically, includes both degrees and zero modes, and uses a stable
logarithmic heat sum. It is a floating point evaluation, not a rigorous interval
certificate. Its dimension limits are computational guards, not new physical
admission rules.

## Finite edits and comparison derivatives

For fixed qubit/stage bounds and primitive profile the native code domain is
finite. A permitted replacement must validate its own blank/oldRIGHT/source
interface and complete expanded primitive schedule. Its price difference is
the difference of the **complete** two prices above. Effects, source
readiness, compulsory classical transcripts and generated work must be priced
at their actual declared interfaces; postselection is not an uncharged edit.
Increasing the wire or stage bound moves to a larger domain. A minimum over
one finite nonempty domain exists, but gives neither continuous Euler
stationarity nor stationarity of the current execution, nor a field/refinement
limit.

For two configurations on the same carrier, at common \(\beta,z\), the exact
comparison bound is

\[
 |B'-B|\le\|\Delta'-\Delta\|_{\rm op}
       +\frac{z}{1-z}\|E_{W'}-E_W\|_1.
\]

The same bound uses \(\widehat F'-\widehat F\) instead of the endpoint
difference. The heat derivative has unit density-matrix trace norm; the
feedback resolvent has norm at most \((1-z)^{-1}\). Integrating along straight
positive-matrix interpolants proves the bound. Those interpolants are a
functional-calculus proof device and are not thereby admitted native words.

A differentiable comparison lift, if supplied, has the full source

\[
 \dot B=-\operatorname{Tr}(\rho_\beta\dot\Delta)
  +\operatorname{Tr}[(I-z\widehat F)^{-1}
                   (z\dot{\widehat F}+\dot z\widehat F)]
  -\left[\frac{\log Z}{\beta^2}
          +\frac{\operatorname{Tr}(\rho_\beta\Delta)}{\beta}\right]\dot\beta,
 \quad Z=\operatorname{Tr}e^{-\beta\Delta},\quad
 \rho_\beta=Z^{-1}e^{-\beta\Delta}.
\]

Every primitive, preparation and cut derivative remains in this formula. At
fixed \(\beta,z\), the feedback trace may equivalently be computed using
\(E_W,\dot E_W\) by the determinant identity. In particular,

\[
 \dot W=\sum_jg_{N-1}\cdots g_{j+1}\dot g_jg_{j-1}\cdots g_0,
 \quad
 \dot P_j=\dot W_jP_0W_j^\dagger+W_j\dot P_0W_j^\dagger
                                      +W_jP_0\dot W_j^\dagger,
\]
\[
 \dot C=-\dot P_{\rm hist}TP_{\rm hist}
 +(I-P_{\rm hist})\dot TP_{\rm hist}
 +(I-P_{\rm hist})T\dot P_{\rm hist},\qquad
 \dot F_{\rm hist}=\dot C^\dagger C+C^\dagger\dot C.
\]

The moving input \(\dot P_0\) is retained. A unitary comparison lift requires
\(g_j^\dagger\dot g_j\) skew-Hermitian. These matrix derivatives do not supply
a free native pulse angle: the fixed G/CX alphabet is discrete. Paid code
secants require their actual source/lift norm, readiness and approximation
budgets; a continuous closure requires a separate proved topology and limit.
No source-changing normal can be declared zero merely because a prepared
expectation or a semantic output law is fixed.

## Carrier and physical-stack boundaries

* A new passive **blank** wire with \(g'_j=g_j\otimes I_2\) and
  \(P'_0=P_0\otimes|0\rangle\langle0|\) doubles the full heat trace. It adds
  \(\beta^{-1}\log2\) to heat, leaves feedback and input rank unchanged, and
  still retains the other wire column in heat.
* A new arbitrary protected input wire instead has
  \(P'_0=P_0\otimes I_2\). It doubles input rank and feedback multiplicity,
  and also adds \(\beta^{-1}\log2\) to heat. Protection is not a prepared
  blank. With an entangled unknown reference, a controlled operation on
  oldRIGHT need not preserve its coherences; the native domain forbids acting
  on immutable oldRIGHT at all.
* An added clock stage changes \(N\), the full spectrum and dimensions.
  Recompute both full prices; the fixed-carrier edit bound does not compare
  different matrix dimensions. Equal word monodromies at unequal lengths
  need not have equal heat. The rank step is not multiplication of a
  normalized heat trace.
* Exact source-enabled inverses must use their full admitted native expansion.
  The positive G/CX profile receives no free \(G^\dagger\). A positive-word
  approximation carries its original error and additional stages. Raw retained
  garbage, failed flags and old records cannot be replaced by a success Kraus
  block or erased from heat. A generated coherent helper may be uncomputed by
  real gates; an already required measured transcript is another interface.
* Generic effect-preserving edits can change heat. Exact heat neutrality is a
  proved property of the special common-inventory conjugate echo, not a law
  of this entire word domain. Actual work, readiness, source, cut, clock and
  any further admitted response-effect variations remain computable rows of
  the full matrices. This packet grants none of them stationarity for free.

An optional homogeneous scene must retain its **actual owned** operator and
normalization. For example, paid writer §13.3 uses
\(\mathcal L=I-B_S\otimes I-C_S\otimes(T+T^\dagger)\) with the specified
33-mode scene, actual register multiplicities and its own \(\beta\). Its heat
is the full trace of that operator, not the bare paired clock heat above.
Nor is the original spatial \(D_{\rm sp}^2\) equal to this clock by definition.
Any chosen extra Hodge degree or passive tensor factor must be justified and
counted explicitly. This implementation does not substitute the clock for
either owner or silently add their prices together.

The resulting positive application is a finite, executable matrix definition
and full Book-price comparison for a declared native execution sector. The
remaining physical proposition is an actual same-execution identification
with the originally admitted operator/cut and a justified native variation or
selection law, including mandatory stopping, Cost−Info, work and source
interfaces. It is not supplied by a finite domain definition, a computed
minimum over words, or a successful circuit test. No Einstein field equation,
`GR_closed`, or compulsory full-scene stationarity is asserted here.
