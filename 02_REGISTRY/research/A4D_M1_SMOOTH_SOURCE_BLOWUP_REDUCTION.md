# Smooth-source blow-up reduction to constant-coframe joint vacua

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Input head: `824e1c8471f5a91f944efe29a82d0292941e35ed`.  
Status: unconditional compactness reduction under the stated compact-chart/source hypotheses; not a task terminal.

## 1. Purpose

The response problem must not be replaced by an enumeration of frozen Bloch
zeros.  For a smooth independently prescribed metric source, the literal
finite Euler equations themselves give a stronger first reduction: every
microscopic blow-up limit is a **full joint vacuum of the constant-coframe
problem**.  Thus a nonzero continuum response gap cannot be a new leading
frozen response class.  It must live in the approach/modulation memory of a
joint-vacuum component.

This is the response-side analogue of fixing the observational quotient before
counting classes.

## 2. Setup

Let (h_j=1/L_j	o0), (L_jin4mathbb N), and let a fixed smooth
nondegenerate coframe (S) on the unit four-torus have compact image in one
nondegenerate Gram chart.  Sample

[
S_j(x)=S(h_jx),qquad Q_j(x)=S_j(x)^Teta S_j(x).
]

Let (K_j) be exact finite fields satisfying the unchanged naked-star
equations with an independently fixed smooth-source family

[
E_K(Q_j,K_j)=0,qquad
E_Q(Q_j,K_j)=h_j^2	au_j,
	ag{1}
]

where the ten owner components obey

[
sup_j|	au_j|_{ell^infty}<infty.
	ag{2}
]

Assume, after genuine local Lorentz gauge, that every link value occurring in
the sequence lies in one fixed compact subset (mathcal K) of a valid
finite link chart.  This compact-chart hypothesis is essential because the
proper Lorentz group is noncompact.  No Fourier support, envelope ansatz,
connection uniqueness or inverse estimate is assumed.

The literal star Euler operators have a fixed finite stencil and are analytic
in the finitely many coframe and link entries on this compact set.

## 3. Blow-up theorem

Choose arbitrary lattice sites (x_j), and after a subsequence assume
(h_jx_j	o x_*) on the continuum torus.  Translate the finite fields so
(x_j) becomes the origin.

For each fixed integer radius (R), only finitely many links occur in the
radius-(R) patch.  Compactness of (mathcal K) gives a convergent
subsequence on that patch.  A diagonal extraction over (R=1,2,ldots)
produces a link field

[
K_infty:mathbb Z^4	imes{0,1,2,3}	omathcal K
]

defined on the entire lattice.

For every fixed (ninmathbb Z^4),

[
S_j(x_j+n)longrightarrow S(x_*)
]

because (S) is continuous and (h_jn	o0).  Hence all coframes in every
fixed Euler stencil converge to the **same constant coframe** (S_*=S(x_*)).

Evaluate any fixed connection Euler row at the translated site (n).  Its
arguments converge coefficientwise and its value is identically zero by (1).
Continuity of the literal finite stencil therefore gives

[
E_K(S_*,K_infty)(n)=0.
]

For a metric Euler row, (1)--(2) give

[
|E_Q(Q_j,K_j)(x_j+n)|le C h_j^2longrightarrow0,
]

so the same finite-stencil passage yields

[
E_Q(S_*,K_infty)(n)=0.
]

Since (n) was arbitrary,

[
oxed{
E_K(S_*,K_infty)=0,qquad E_Q(S_*,K_infty)=0
quad	ext{on all of }mathbb Z^4 .
}
	ag{3}
]

Thus every microscopic blow-up limit of the declared smooth-source class is
an **entire constant-coframe full joint vacuum**.  This is a nonlinear
statement: no linearized symbol or rank classification enters the proof.

The result is gauge-covariant.  A gauge slice is used only for compactness;
two convergent gauge representatives related by a convergent proper-Lorentz
field give gauge-equivalent limits.

## 4. Consequence for the canonical response memory

The stationary-response owner derives the exact local metric memory

[
Xi=rac12operatorname{sym}(Q^{-1}S^TH)
]

in the owner ten-slot convention and proves that it is precisely the
sitewise Gram Euler readout on (E_K=0).

Equation (3) therefore implies for every blow-up limit

[
oxed{Xi(S_*,K_infty)equiv0.}
	ag{4}
]

Consequently the leading frozen response-memory image of the whole
smooth-source class is a singleton, **without** classifying the frozen Bloch
zero set.  Curved nongauge #232/Y vacua, the eight constant-coframe quarter
axes, and any other as-yet-unclassified bounded entire joint vacuum all have
the same leading frozen response memory: zero.

This does not identify their connections and does not call them gauge.

## 5. Why the #227 family is not a counterexample to the reduction

For the exact #227 connection-stationary family with (t_h=ah^2), the
unscaled metric response tends to zero and the unscaled microscopic blow-up
is the identity vacuum.  Its nontrivial datum is instead

[
h^{-2}Xi_{11}(0)	o-a.
]

Therefore #227 illustrates exactly the distinction proved here:
zeroth-order frozen memory can collapse while a **second-order approach
memory** remains nonzero.  #227 is excluded from the task's joint-source
class because its metric response is not an independently prescribed smooth
source, but it is a hostile control showing that (4) alone is insufficient.

## 6. The remaining object is not a new frozen solution class

Define (mathcal V(S_*)) to be the set of bounded entire solutions of (3)
in the compact chart, modulo genuine local Lorentz gauge.  The theorem above
says that arbitrary microscopic subsequences land in

[
mathcal V(S_*)subsetXi^{-1}(0).
]

Hence any task-level nonzero normalized response gap must come from how a
field approaches or modulates this vacuum set as the coframe varies on scale
(h).  It cannot be certified merely by finding another frozen kernel,
another torsion point or another constant-background joint vacuum.

The single remaining nonlinear object is therefore the **horizontal
second-order response of the joint-vacuum bundle**:

[
oxed{
mathfrak H_{m resp}
=
	ext{the order-}h^2	ext{ response memory generated by smooth modulation of }
mathcal V(S).
}
	ag{5}
]

A positive terminal is obtained if the literal equations force, for every
admissible modulation generated by an exact sequence,

[
mathfrak H_{m resp}
=
mathfrak H_{m designated}
]

in the declared testing topology; #216/#201/E-NJET then identify the latter
with (-G/2).  A negative terminal requires one exact smooth-source sequence
whose horizontal memory differs.

The existing constant-coframe nonlinear quarter theorem, exact moving-plane
Y family, one-coordinate nonregular isolation theorem, and corrected
normal-jet compatibility are scoped computations of (5) on particular pieces
of (mathcal V).  They are evidence about the same object, not independent
classes that must each become a separate terminal.

## 7. Scope and topology

The blow-up theorem uses the sitewise (O(h^2)) source bound because this is
what makes the microscopic metric Euler equation converge strongly to zero.
A merely weak/tested source does not imply (3).

The theorem itself is local and therefore does not convert a pointwise
(o(h^2)) estimate into the unweighted owner (ell^1) norm; the growing
number of sites must still be handled by the eventual horizontal-response
identity or estimate.  Likewise it proves no existence theorem for a
prescribed general four-dimensional source.

What it removes is the need to classify arbitrary frozen connection
microstructures as separate response candidates.

## 8. Verdict

[
oxed{	exttt{SMOOTH-SOURCE-MICROSCOPIC-BLOWUP-IS-JOINT-VACUUM}}
]

and

[
oxed{	exttt{LEADING-FROZEN-RESPONSE-MEMORY-COLLAPSES}}
]

under the explicit compact-chart and sitewise smooth-source assumptions.

The task remains `PARTIAL / OPEN` only at the horizontal/modulation response
(5), equivalently at proving its universal equality with the designated
second jet or producing an exact independently sourced counterexample.

No action change, selector, Fourier cutoff, connection uniqueness,
`H_TORUS` premise, BOOK/CORE promotion or task terminal is asserted.
