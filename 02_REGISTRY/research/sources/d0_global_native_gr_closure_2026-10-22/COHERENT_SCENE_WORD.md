# Exact coherent Golden word for the declared combinatorial K(9,11,13) scene

22 October 2026. Existing Draft #334, task
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, native-programme-v1.
Phase: native realization, supporting construction.

This preserves the positive construction developed in the preceding research
turn and rechecks its literal small-word identities in exact arithmetic.
Its parent consumer is the common-programme operator construction:
one actual enlarged unitary, its own initialized cut, and its true Book
return. It does not itself supply a moving field writer or a physical price.

## 1. Exact scope

The interface is the already declared addressed Golden/CNOT interface with
a preserved, paid known-one resource and fresh retained work. Every primitive
letter, inverse echo, preparation, work register and final readout must be
charged. Its physical G0/M1 admission is not inferred from finite unitarity.

Set p=phi^(-1), a=sqrt(p), and
\[
G=\begin{pmatrix}a&-p\\p&a\end{pmatrix},\qquad a^4+a^2=1.
\]
The construction below is a FIXED UNITARY WORD. Former factory measurement
bits are kept coherent. A chosen successful transcript specifies a matrix
corner only; no failed row is deleted or physically postselected.

The scene used here is explicitly the COMBINATORIAL Laplacian L_33 of
K(9,11,13), embedded as L=L_33 direct-sum 0_95 on DATA128.
Book03 defaults to a normalized scene Laplacian unless explicitly flagged.
This lemma does not identify the two, nor identify DATA128 with the entire
much larger programme/work space.

## 2. Exact scalar corners of fixed native words

Consume the literal phase and X-test words from
sources/d0_native_joint_field_minimum_2026-10-20/inputs/GOLDEN_EXACT_DETECTOR.md.
Its adaptive, measured finite-retry implementation and the coherent fixed
word here are different executions; the literal gates can be shared.

The plus-resource word is G on two fresh bits followed by CNOT. Its
second-bit-one corner is
\[
ap(|0\rangle+|1\rangle).
\]

For controls c_1,...,c_k and a fresh target, set W_0=G and use the
chronological recursive word
\[
W_k=CX(c_k,t);W_{k-1}^{-1};CX(c_k,t);W_{k-1}.
\]
With G^(-2^(k-1)) before this word, the target-one corner is
\[
K_Z=-pZ,\quad K_{CZ}=-2a^3CZ,\quad K_{CCZ}=-4a^9CCZ.
\]
An inverse is the actual reversed word; G^(-1)=XGX and each X is a
CNOT controlled by the preserved known-one. No inverse oracle is used.

For the two complete weak X tests, with separate fresh bits,
\[
A_0=pI-p^2X,\quad A_1=ap(I+X),\qquad
B_0=pI+p^2X,\quad B_1=-ap(I-X).
\]
Execute both tests irrespective of their coherent bits. Their (1,0)
corner is B_0 A_1=ap(I+X). Use the plus resource, the CZ corner,
this full X-cycle corner, then the three-CNOT SWAP. Project the old input
work onto computational zero. The resulting input-to-output corner is
\[
K_H=-2a^9\begin{pmatrix}1&1\\1&-1\end{pmatrix}
    =-2\sqrt2\,p^{9/2}H.
\]
The checker propagates both input basis columns through the literal
six-qubit fixed word and verifies the norm of each ENTIRE output column,
not just this corner.

Two such H corners around the target of the CCZ corner, with fresh work
for all three gadgets, give
\[
K_T=-32a^{27}\operatorname{Toffoli},\qquad
K_T^\dagger K_T=1024p^{27}I.
\]
The exact success probability is nonzero but small; its approximate value
is 0.002331490605720107. Numerical evaluation of its expanded algebraic
coefficients suffers cancellation, so the proof uses the exact ring.

Fresh work makes the corners multiply exactly. Thus any finite reversible
Boolean/sign SELECT circuit has a fixed enlarged native word Q with
\[
\langle0_{\rm work}|Q|0_{\rm work}\rangle=\gamma_Q Q_{\rm logical},
\quad \gamma_Q\ne0,
\]
after success-one bits are permuted to zero by charged native X gates.
The known-one remains a separately declared initialized component.
Other rows remain part of the unitary; a bit permutation is not erasure.

Expanded lower counts before the indicated success-bit permutations are:
CZ 6 G +14 CNOT, CCZ 12 G +30 CNOT, and the H construction
12 G +22 CNOT. Its three success-one work bits require three further
CNOTs for the all-zero corner convention. The CCZ corner requires one.
The composed Toffoli therefore uses at least 117 primitive gate ticks on
this convention, before known-one preparation, routing, storage or reading.
No efficiency or continuum-cost bound follows from existence.

## 3. Put the actual scene into the same word

For each of the 359 unordered edges e={u,v}, let S_e transpose u,v on
DATA128 and fix all other basis vectors, including the 95 padding states.
Then
\[
L=\sum_{e}(I-S_e),\qquad
I-S_e=(|u\rangle-|v\rangle)(\langle u|-\langle v|).
\]
There are 718 signed permutation terms.

Prepare 12 independent Golden address bits. Each address of weight six
has amplitude p^9 and probability p^18. There are
binomial(12,6)=924 such addresses, enough to assign separate addresses
to all 718 terms. At one address apply I; at its paired edge address
apply -S_e. For every unused address flip an extra fresh flag.
Every operation is a finite Boolean/sign SELECT on the admitted interface.

Undo the address preparation by its paid inverse. The logical address-zero,
flag-zero corner is
\[
A_0=p^{18}L,\qquad p^{18}=1597-2584p.
\]
Compile the entire SELECT with the fresh-work corner construction above,
using the same fixed schedule for all addresses. Its actual full blank
corner is
\[
A=\gamma_Q p^{18}L.
\]
The graph has the exact spectrum
\[
0^1,\quad20^{12},\quad22^{10},\quad24^8,\quad33^2.
\]
Thus 33p^18<1. The checker proves the integer annihilating polynomial
and the five trace moments that determine these multiplicities, as well
as the edge/transposition sum. It does not infer the spectrum from a
floating eigensolver.

For U=Q and its own initialized projection P, the true Book complement is
\[
F=P-PQ^\dagger P QP=I-\nu L^2,\qquad
\nu=|\gamma_Q|^2p^{36}.
\]
This is an actual corner/return identity, including all factory failure
space, not an assignment of an abstract positive effect.

## 4. A paid outer Golden reflection

Let R_Q=I-2P_Q be the reflection about ALL initialized Q work,
with identity on its DATA. Its finite Boolean predicate can be compiled
with fresh work into a native word V_Z whose own blank corner is
\[
\gamma_R\bigl(|0\rangle\langle0|\otimes I+
 |1\rangle\langle1|\otimes R_Q\bigr).
\]
This is a scalar corner, not a free exact reflection on all rows.

Use the actual full word
\[
U=(G^\dagger\otimes Q^\dagger)V_Z(G\otimes Q).
\]
Its complete port/work initialized corner is
\[
B=\gamma_R[I-2p^2 A^\dagger A]
  =\gamma_R(I-t\nu L^2),\qquad t=2p^2.
\]
Hence its actual complementary return is
\[
\boxed{F=I-r(I-t\nu L^2)^2,\qquad r=|\gamma_R|^2.}
\]
In particular the failure baseline (1-r)I is real and is retained.

If a separate genuine moving writer L(Y) is supplied with the same fixed
topology and factories, then r and nu are fixed and, putting X=L^2,
\[
DX=L\,DL+(DL)L,
\]
\[
DF=rt\nu[(I-t\nu X)DX+DX(I-t\nu X)].
\]
The Book derivative is then exactly
\[
DJ=z\operatorname{Tr}[(I-zF)^{-1}DF].
\]
For a genuinely selected heat term using this same L,
DH=-Tr(rho_beta DL), rho_beta=e^(-beta L)/Tr e^(-beta L).
Neither a moving writer nor that physical heat identification is supplied
by the STATIC word just proved.

Padding also remains physical:
Tr exp(-beta L)=95+Tr exp(-beta L_33).
Deleting 95 inside the logarithm changes the source. Selecting a genuine
33-dimensional scene cut is a separate actual projection/price issue.

## 5. Exact replay and parent boundary

check_coherent_scene.mjs uses only JavaScript BigInt arithmetic in
Z[a]/(a^4+a^2-1), literal G/CNOT column propagation and integer scene
matrices. RESULT_SCENE.json records the executed result. Displayed decimal
values are diagnostics only. The checker was executed in the available
JavaScript tool runtime; it does not assert a shell, Python, CI or Lean run.

This removes the need for a supplied arbitrary Boolean or spectral gate
in this STATIC combinatorial-scene corner construction. The full Q and U
are actual coherent words on the stated interface. It does not select the
Book03 information algebra, normalized scene Hodge, moving 42-field writer,
independent preparation/clock equations, source normalization or refinement.

GR_closed=false. No existing scientific acceptance is promoted.
