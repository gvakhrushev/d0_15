# Periodic one-parameter boost source rigidity

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Parent control: the exact #227 coupled boost family.  
Status: exact class-level source-image rigidity for the whole real temporal
one-parameter \(B=K_1+K_2+K_3\) subgroup; no unrestricted task terminal.

## 1. Why this class matters

The #227 exact connection-stationary family uses the four-phase temporal
pattern
\[
(U(t),I,U(t)^{-1},I)
\]
and has a fast metric response with signs \((1,1,-1,-1)\).  A natural hostile
attempt is to give the four phases independent amplitudes and try to make
their metric response phase-common while preserving stationarity.

This note excludes that attempt for the entire real commuting \(B\)-subgroup,
before any restricted Fourier ansatz or perturbative expansion.

## 2. Arbitrary four-phase temporal field in the subgroup

Let
\[
B=K_1+K_2+K_3,\qquad B^3=3B,
\]
and use the real Cayley chart
\[
U(t)=(I-\tfrac t2B)^{-1}(I+\tfrac t2B),
\qquad |t|<2/\sqrt3.
\]
Equivalently,
\[
U(t)=\exp(\alpha(t)B),\qquad
\alpha(t)=\frac{2}{\sqrt3}\operatorname{artanh}\frac{\sqrt3t}{2}.
\tag{1}
\]
The map \(t\mapsto\alpha(t)\) is strictly increasing and bijective on this
chart.

Take arbitrary
\[
W_p=U(t_p),\qquad p\in\mathbb Z/4,
\]
on the temporal links and identity spatial links.  Since all \(W_p\) are
functions of the same \(B\), they commute.  The three temporal-spatial
plaquettes at phase \(p\) have common holonomy
\[
P_p=W_pW_{p+1}^{-1}
=\exp(\delta_pB),\qquad
\delta_p=\alpha(t_p)-\alpha(t_{p+1}).
\tag{2}
\]

The periodic cycle gives the exact telescoping identity
\[
\boxed{\sum_{p=0}^3\delta_p=0.}
\tag{3}
\]

## 3. Metric response is an injective function of the increment

For \(P=\exp(\delta B)\), the odd curvature is
\[
\frac12(P-P^{-1})=\gamma(\delta)B,
\]
where
\[
\gamma(\delta)=\frac1{\sqrt3}\sinh(\sqrt3\,\delta).
\tag{4}
\]
In Cayley increment \(s\),
\[
\gamma=\frac{4s}{4-3s^2}.
\]
On the real identity chart,
\[
\gamma'(\delta)=\cosh(\sqrt3\,\delta)>0,
\tag{5}
\]
so \(\gamma\) is injective.

At flat solder the ten-component Gram response is the same fixed covector
\[
m=(0,0,0,0,-1,1,1,-1,1,-1)
\]
times \(\gamma(\delta_p)\):
\[
E_Q(p)=\gamma(\delta_p)m.
\tag{6}
\]

No connection equation has been used.

## 4. Phase-common source forces vacuum

Suppose the prescribed source is phase-common in this four-phase cell:
\[
E_Q(0)=E_Q(1)=E_Q(2)=E_Q(3).
\tag{7}
\]
Since \(m\ne0\), equations (5)--(7) imply
\[
\delta_0=\delta_1=\delta_2=\delta_3=\delta.
\]
Using (3),
\[
4\delta=0,
\]
hence
\[
\boxed{\delta=0,\qquad E_Q\equiv0.}
\tag{8}
\]

Therefore the phase-common source image of the entire real temporal
one-parameter boost class is the singleton
\[
\boxed{\mathscr T^{B,\mathrm{phase\text{-}common}}=\{0\}.}
\tag{9}
\]

This is stronger than checking whether one deformation of the #227 pattern
remains connection-stationary.  Even before imposing \(E_K=0\), no nonzero
phase-common source can be produced by arbitrary four phase amplitudes in
this subgroup.

If the full connection equations are added, they only shrink the class
further.

## 5. Smooth-source consequence

For a fixed smooth source sampled on an \(L=4m\) lattice, its four-phase UV
component is super-algebraically small by the owned #216 smooth tail/alias
lemma.  If a sequence stays in a fixed compact real \(B\)-chart, strict
monotonicity of (4) converts this into
\[
\delta_p-\bar\delta=O(h^\infty).
\]
Equation (3) gives \(\bar\delta=O(h^\infty)\), hence
\[
E_Q=O(h^\infty)
\]
in the fast \(B\)-sector.  The final \(h^{-2}\) normalization and polynomial
site-count losses preserve super-algebraic smallness.

Thus the exact #227 connection-stationary curve cannot be retuned within its
full commuting one-parameter completion to carry a nonzero smooth continuum
source.

## 6. M1 reading

The microscopic phase amplitudes \(t_0,\ldots,t_3\) are not the relevant
memory.  The shared-face current sees only the four increments
\(\delta_p\), and periodicity removes their common mode.

The source map factors as
\[
(t_0,\ldots,t_3)
\longmapsto
(\delta_0,\ldots,\delta_3),\quad \sum\delta_p=0
\longmapsto
(\gamma(\delta_p)m)_p.
\]
On the phase-common source quotient this image is one point.

This is precisely a class reduction by conserved current rather than a
catalogue of phase representatives.

## 7. Scope

The theorem uses one commuting real boost subgroup and identity spatial links.
It does not cover noncommuting coupled centers, spatial-link compensation, or
a general varying coframe.  Those are separate parts of the finite quartic
source-image system.

Verdict:
\[
\boxed{\texttt{PERIODIC-COMMUTING-B-PHASE-COMMON-SOURCE-IS-ZERO}.}
\]

No new action, selector, spectral filter, connection uniqueness or task-level
Einstein/no-go terminal is asserted.
