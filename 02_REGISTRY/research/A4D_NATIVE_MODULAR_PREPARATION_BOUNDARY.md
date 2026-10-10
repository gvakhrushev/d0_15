# Native preparation: the modular-state route and the full price

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing PR #310.
Input SOURCE: `8207558224ee7c419d58f1f468d01b1187e21951`.
Date: 10 October 2026.
Status: **a complete finite state-to-heat reconstruction boundary and a
literal modular-time test; common native preparation T0 remains open**.

The specific proposed implication tested here is:

> The state prepared by the retained/archive process determines a modular
> flow; therefore it determines the heat operator and its full-price source.

BOOK_06 §06.8.M makes the relevant modular-time identification. Its actual
Lean owner, `D0.Bridge.tomita_modular_flow_conditional`, returns two witnesses
supplied in `TomitaModularFlow`. In particular `timeEqualsModularFlow` is a
supplied proposition with a supplied proof `cited`. It does not construct a
density, a modular operator, a heat generator, or a field-dependent map.
The original [Connes--Rovelli paper](https://arxiv.org/abs/gr-qc/9406019)
also distinguishes modular theory from the **thermal-time hypothesis**
identifying its flow with physical time. No new physical identification is
installed in this packet.

The complete reconstruction calculation below reduces the ambiguity to a
scalar on a fixed finite factor when the entire faithful density and beta
are known. A separately owned positive ground-zero condition removes that
scalar. Both statements are retained: normalization freedom must not be
claimed after a condition fixing it has been imposed.

## 1. A retained sector and a tensor-factor reduction are different inputs

Let P be an orthogonal projector on a finite Hilbert space and psi a pure
unit vector. On the full retained matrix algebra `B(PH)`, conditioning on
the retained sector gives, whenever P psi is nonzero,

\[
 \rho_P={|P\psi\rangle\langle P\psi|\over\|P\psi\|^2}.       \tag{1}
\]

This has rank one. If rank P is greater than one, it is not faithful on
`B(PH)`. If rank P is one, that algebra has only a trivial modular flow.
This proves the statement for every orthogonal P and pure psi; a direct
sum `PH + QH` alone does not supply an entangled mixed active density.
Restricting further to a smaller observable algebra can change faithfulness
and requires that algebra to be named. It is not covered by replacing
`B(PH)` silently.

A genuine tensor-factor partial trace can instead be mixed. The existing
`GoldenCoherentMemory.fullStep` and `blank_record_evolution` give, in basis
00,01,10,11 and with a^2=p, p+p^2=1, 0<p<1,

\[
 U(1,0,0,0)^T=(a,0,0,p)^T,
 \qquad \rho_S=\operatorname{diag}(p,p^2).                  \tag{2}
\]

Here both system and record remain in the full preparation. The partial
trace is a stated readout, not deletion of the complementary modes from
the action. Equation (2) is faithful on M2. Faithfulness is nevertheless
not true for every input of the same declared gate interface:

\[
 a^2+(-p)^2=1,\qquad U(a,0,-p,0)^T=(1,0,0,0)^T.           \tag{3}
\]

The latter reduced density has a zero eigenvalue. No finite Hermitian heat
matrix at finite positive beta has that Gibbs density: its exponential is
strictly positive. A support restriction, an infinite energy, or a thermal
limit needs its own admission; none is introduced. Equations (2)--(3)
are exact gate/input statements, not a theorem that every such input or
apparatus is physically prepared by M1.

## 2. The full finite Gibbs reconstruction class

Fix one finite factor M_d with its ordinary matrix trace and beta>0.
For a Hermitian heat matrix H put

\[
 Z_H=\operatorname{Tr}e^{-\beta H},\qquad
 \rho_H=Z_H^{-1}e^{-\beta H},\qquad
 B_H=\beta^{-1}\log Z_H.                                 \tag{4}
\]

For **every** faithful density rho (rho>0, Tr rho=1), the complete fiber is

\[
 \rho_H=\rho\quad\Longleftrightarrow\quad
 H=-\beta^{-1}\log\rho+cI,
 \quad c\in\mathbb R.                                   \tag{5}
\]

Proof. Taking the unique Hermitian logarithm of
`exp(-beta H)=Z_H rho` gives the forward implication, with
`c=-beta^-1 log Z_H`. Conversely the exponential of the right side is
`exp(-beta c) rho`, whose trace is `exp(-beta c)`. This proves all of (5),
not only a commuting family of examples. In particular

\[
                         B_H=-c.                        \tag{6}
\]

Thus a normalized prepared state does not by itself provide the full
thermal price. For the existing bootstrap with the same feedback term,
the replacement `H(X) -> H(X)+c(X)I` leaves rho and its modular flow
unchanged but changes the **same** price and its restricted covector by

\[
 \mathcal B\longmapsto\mathcal B-c(X),\qquad
 d\mathcal B|_{T_X}\longmapsto d\mathcal B|_{T_X}-dc|_{T_X}. \tag{7}
\]

No new action is selected here. This is the exact fiber of the existing
normalized-state interface; its scalar functions are not declared native.
A fixed constant changes no source, but a field-dependent scalar need
not be trace-only. For example the existing joint carrier admits
`q_s(t)=q_t(t)=eta+t diag(1,1,0,0), D(t)=I` near zero, with
`eta=diag(1,-1,-1,-1)`. Its tangent is eta-tracefree and satisfies
the full differentiated metric-transport constraint. The scalar coordinate
`c(q)=q_00` has derivative one there. Ten packed symmetric-coordinate
controls retain the off-diagonal dual factor two. This countercontrol is
not a physical preparation, fitted source, or comparison with rho0.

The formula applies on the complete joint tangent, including link, affine
and matter coordinates wherever c depends on them. It does not quotient
out a link equation, declare response-null directions gauge, or exchange
raw and transported physical readouts.

### 2.1 Positive heat with a genuine zero mode fixes the scalar

If the actual heat owner additionally requires H>=0 and min spec H=0,
then (5) has exactly one representative:

\[
 H_0=\beta^{-1}\bigl(\log\lambda_{\max}(\rho)I-\log\rho\bigr),
 \qquad B_{H_0}=-\beta^{-1}\log\lambda_{\max}(\rho).       \tag{8}
\]

Indeed the smallest eigenvalue in (5) is
`c-beta^-1 log lambda_max(rho)`. Setting it to zero proves existence and
uniqueness in the whole stated class. If a particular vector must be a
zero mode, that vector must belong to the largest-eigenvalue space of
rho; faithful rho alone does not imply this. If rho is nonfaithful, no
finite H exists on the full carrier, including under the ground-zero
condition. Possible multiplicity changes of the maximal eigenvalue also
prevent assuming a smooth H_0 without checking the actual preparation.

Equation (8) is a reconstruction theorem **conditional on equality of
the prepared state with the Gibbs state of the already-owned heat**. It
does not prove that equality, choose a temperature, identify either
operator with the archive Laplacian, or define X from rho. A protected
zero mode cannot be discarded to use (7), and (8) cannot be inserted as
a new physical heat law merely because it is available mathematically.

## 3. Real modular flow is not the hyperbolic two-coordinate step

In the finite faithful-state representation, the modular operator on the
full Hilbert--Schmidt space is

\[
 M_\rho(X)=\rho X\rho^{-1},\qquad
 \sigma_s(X)=\rho^{is}X\rho^{-is}.                        \tag{9}
\]

Every real-s step sigma_s is a norm-isometric linear automorphism.
The positive operator M_rho and the real automorphism sigma_s are
different objects. In general modular theory the same norm-isometry
holds for the bounded observable algebra; no physical time premise is
needed for this algebraic property.

Here is the complete linear intertwiner obstruction. Let U be any
norm-isometric real linear operator on a normed space E, with no finite
dimension assumption. If a,b in E satisfy the columns of the literal
toral T=[[0,1],[1,-1]],

\[
                    Ua=b,\qquad Ub=a-b,                 \tag{10}
\]

then a=b=0. The two vectors
`a+p b` and `a-(1+p)b` have U eigenvalues p and -(1+p).
Their absolute values differ from one. Norm-isometry implies that each
vector is zero; subtracting the two equations gives `(1+2p)b=0`, then
a=0. This proof applies to every bounded-observable linear realization of
(10), not only to an orthonormal or eigenvector basis. Four propositions
in the companion Lean capsule check this argument and the native outputs
(2)--(3); the actual conditional bridge and gate types are printed too.

This does **not** rule out the toral map acting nonlinearly on coordinates,
an infinite-dimensional Koopman realization, unbounded observables, a
separately justified encoding, or all possible modular descriptions of
D0. On a commutative algebra by itself, a faithful state's modular flow
is trivial; a noncommutative extension is another specified representation.
No such exception is silently identified with (10).

### 3.1 The golden modular operator is a positive control, not a rejection

For the actual density (2), on the **full** ordered basis
E00,E01,E10,E11 one has

\[
        M_\rho=\operatorname{diag}(1,1/p,p,1).            \tag{11}
\]

The square restricted to the off-diagonal span, ordered E10,E01, has
eigenvalues p^2 and (1+p)^2. With

\[
 S=\begin{pmatrix}1&1\\p&-(1+p)\end{pmatrix},
 \quad \det S=-(1+2p),
 \quad T^2S=S\operatorname{diag}(p^2,(1+p)^2),            \tag{12}
\]

there really is an algebraic match for this **restricted positive
modular square**. Both diagonal modes in (11) remain; their trace
contribution cannot be removed to identify the full operator with T^2.
Equation (12) is not a real modular-time step, the full Gibbs heat, an
allowed physical operation, or a field-dependent preparation. It is a
negative control against incorrectly banning phi from modular theory.

## 4. Consequence for the single T0 obligation

The named modular route does not presently fill the joint preparation
arrow. Its ordinary sector split does not supply the faithful tensor
density it invokes; its literal linear toral-flow reading fails (10);
and even a supplied faithful state determines the full heat price only
after the normalization/ground data in (5)--(8) are fixed by the actual
heat owner. These are complete statements in their stated interfaces,
not absence of every F in D0.

The next required native statement is still one common admitted
preparation yielding the observable algebra/state, heat and feedback,
their X=(q,D,b,m) readout, and the actual refinement. If this route is
used, prove its state/Gibbs identification, faithfulness or its full
nonfaithful treatment, and its existing normalization law. Do not install
thermal time, H_0, a central function, or a source as an additional law.
All archive modes, original terminals, source/Ward, quantitative contrast,
native stationarity, curved roots and soundness/recovery remain required.

## 5. Reproduction and scope

Companion stem:
`certificates/a4d_native_modular_preparation_boundary`.
The all-size matrix-logarithm reconstruction and modular interpretation
are analytic proofs. The Lean capsule proves four named norm/gate
propositions and prints the actual owner propositions and axioms. The
exact checker reconstructs the literal native gate outputs and partial
traces, all four modular modes, (12), the Gibbs shift, the zero-mode
exception, and ten constrained symmetric-coordinate controls. Executed
mathematical mutations and scope mutations are recorded separately: 60 exact
controls, seven executed mathematical mutants and sixteen false ledgers.
Each mutant must fail with a mathematical assertion; each false ledger must
fail at the scope/input gate. The receipt pins nine primary/transitive source
files and the toolchain, with six actual axiom reports using only standard
Lean axioms. Reproduction from the repository root is:

```
python3 02_REGISTRY/research/certificates/a4d_native_modular_preparation_boundary_check.py
```

The Lean receipt is independently reproducible from `03_FORMALIZATION` by
running `lake env lean` on the companion `.lean` file. The checker replays
finite identities and validates that receipt; it does not recompile Lean.
No new supported Lean owner, physical admission or T0--T3 closure is
claimed.
