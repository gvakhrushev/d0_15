# Signed order-memory pressure and the exact Golden/Q8 source

21 October 2026. Research continuation of existing Draft PR #334, task
\`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`. Scientific consumers:
Book01's actual Golden/Q8 order interferometer, Book03 §§03.1,03.3 and
the current native Cost–Info/Book03 selection barrier. **GR_closed=false.**

## 1. An exact scalar-source interface for a represented memory sum

Let a *specified represented test* assign differentiable memory vectors
\(m_\gamma(y)\) in one finite positive Hilbert space to its finitely many
ordered histories. Let \(s_\gamma=C_\gamma-I_\gamma\) and
\(w_\gamma=\varphi^{-s_\gamma}>0\). This is the positive scalar coefficient
of the Book03 **memory-valued** path sum, not a claim that the full D0
memory algebra is faithfully represented by any chosen test. Define

\[
 A(y)=\sum_\gamma w_\gamma(y)m_\gamma(y),\quad
 {\cal N}=\langle A,A\rangle>0,\quad
 P_{\rm repr}(y)=-\log_\varphi\|A\|
 =-\frac{\ln{\cal N}}{2\ln\varphi}.
\tag{1}
\]

The complete *first source* of this declared norm pressure is

\[
 \boxed{
 dP_{\rm repr}
 =\sum_\gamma \eta_\gamma\, d(C_\gamma-I_\gamma)
 -\frac1{\ln\varphi\,{\cal N}}
    \sum_\gamma w_\gamma\operatorname{Re}
                  \langle A,dm_\gamma\rangle,
 \qquad
 \eta_\gamma=\frac{w_\gamma\operatorname{Re}
                    \langle A,m_\gamma\rangle}{{\cal N}},
 \quad \sum_\gamma\eta_\gamma=1.
 }\tag{2}
\]

Proof: \(dw_\gamma=-\ln\varphi\,w_\gamma ds_\gamma\);
\(d{\cal N}=2\operatorname{Re}\langle A,dA\rangle\). Substitute
\(dA=\sum_\gamma(dw_\gamma m_\gamma+w_\gamma dm_\gamma)\).
The final identity follows by summing the numerator.

**The coefficients \(\eta_\gamma\) need not be probabilities.**
They can be negative and arbitrarily large near destructive interference.
If the memory vectors are pairwise orthogonal and stationary, they reduce
to nonnegative Born weights
\(w_\gamma^2\|m_\gamma\|^2/{\cal N}\). That orthogonal reduction must
not be applied to unresolved order-memory amplitudes.

There is an exact **common-frame Ward identity**: for a common unitary
change \(dm_\gamma=Xm_\gamma\), \(X^*=-X\), the second term of (2)
vanishes since \(\operatorname{Re}\langle A,XA\rangle=0\). Only genuinely
relative order-memory changes contribute. This is a unitary-frame
identity for this component, not diffeomorphism invariance of the full
D0 physical action.

A more economical equivalent input is the *actual selected Gram matrix*
\(G_{\gamma\delta}=\langle m_\gamma,m_\delta\rangle\).
For real positive weights,
\[
 {\cal N}=\sum_{\gamma,\delta}w_\gamma w_\delta
                        G_{\gamma\delta},\qquad
 dP_{\rm repr}
 =-\frac{d(w^*Gw)}{2\ln\varphi\,w^*Gw}.                 \tag{3}
\]
Thus the Gram values and complete first jets plus \(w,dw\) are
sufficient for the first source of this represented pressure: a full
microscopic dilation is excessive **for this consumer only**. A
selected Book03 scene representation/observer, real memory, and its
absolute path gains remain genuine prerequisites. The full heat,
independent preparation, clock and retained-work prices do not follow
from (3).

## 2. The exact original Golden/Q8 witness

The original real Golden gate is
\[
 p=\varphi^{-1},\quad a=\sqrt p,\qquad
 G=\begin{pmatrix}a&-p\\p&a\end{pmatrix},
 \quad p+p^2=1,\quad G^TG=I.
\]
Let \(i,j\) be the two noncommuting Q8 generators. Their commutator
\(iji^{-1}j^{-1}=-1\) acts as the central minus sign in the **declared
order-reference interferometer**. The original two-port comparison uses
\(G^T \operatorname{diag}(1,-1)G\), retaining BOTH outputs. Acting on
the blank first port yields
\[
 A_{\rm dark}=p-p^2=p^3,\qquad
 A_{\rm bright}=-2ap,\qquad
 q_{\rm dark}=p^6,\quad q_{\rm bright}=4p^3,\qquad
 p^6+4p^3=1.                                         \tag{4}
\]
With the trivial (non-loop) holonomy the same full gate sequence yields
\((1,0)\). This is the existing Book01 physical-mathematical Golden
interferometer and its already-owned probability identity, **not**
a newly created physical actuator or paid Book selection.

Read the single dark-port amplitude as the *specified projected
two-path memory sum* with coefficients
\(w_0=p=\varphi^{-1}\), \(w_1=p^2=\varphi^{-2}\)
and represented memories \(m_0=1,m_1=-1\). Its scoped pressure is
\[
 P_{\rm dark}=-\log_\varphi|p-p^2|
             =-\log_\varphi(p^3)=3,\qquad
 P_{\rm trivial}=-\log_\varphi(p+p^2)=0.              \tag{5}
\]
The full unitary two-port state is normalized, hence its *whole-output*
norm pressure is zero for either holonomy. Equation (5) is therefore
an **observer-port contrast**, not the full Book03/H+J+R action.

The two branch-price coefficients of this same dark-port pressure are
exactly
\[
 \eta_0=\frac p{p-p^2}=\varphi^2=2+p,\qquad
 \eta_1=-\frac{p^2}{p-p^2}=-\varphi=-(1+p).
 \tag{6}
\]
They sum to one, but \(\eta_1<0\). Consequently a purported source
\(\sum q_\gamma ds_\gamma\) with \(q_\gamma\ge0\) and \(\sum q=1\)
**cannot agree with (2) on independently varied branch prices**.

There is also a fully algebraic *finite-price* control. Raising the
destructive branch's formal Book weight cost from \(s_1=2\) to \(3\)
changes \(w_1=p^2\) to \(p^3\). Its port amplitude changes from
\(p-p^2=p^3\) to \(p-p^3=p^2\), so its selected-port pressure
**decreases from 3 to 2** even though the branch price increased by
one unit. This is a scored-histories contrast, not a claim that one
fixed physical controller admits an independent branch-specific
extra tick with unchanged clock and task. The full new execution
would have to carry and pay that intervention.

The orthogonal *regular memory* vectors \(e_1,e_{-1}\) have a different
norm \(p^2+p^4\) and a **positive** branch-price derivative
\(p^4/(p^2+p^4)\). Book01 explicitly warns that a two-dimensional
representation faithful on Q8 group elements is NOT faithful on their
whole group algebra: formal \([1]+[-1]\) is nonzero but is mapped to zero
in that representation. Thus neither (5) nor a chosen regular-memory
trace can silently replace the mandatory full history algebra.


## 2a. An exact same-cut bridge to the finite Book feedback determinant

The same two-port interferometer has a **one-dimensional input/output
blank-return cut** \(P_0=|0\rangle\langle0|\). Put
\(U=G^T\operatorname{diag}(1,-1)G\).
Its native feedback operator on this actual declared active line is
\[
 F=P_0U^*(I-P_0)UP_0=(1-q_{\rm dark})P_0
     =4p^3P_0 .
\]
For the SAME cut, the ordinary finite Book feedback component at a
fixed \(0<z<1\) is exactly
\[
 J_z=-\ln\det(I-zF)
     =-\ln[1-z+zq_{\rm dark}]
     =-\ln(1-4zp^3).                                 \tag{7}
\]
No dimension-128 factor is imported into this rank-one experiment.

More generally, if a smooth *unitary* continuation of this same
rank-one cut has \(q(y)=|\langle0|U(y)|0\rangle|^2>0\), then its
port-amplitude pressure
\(P_{\rm port}(y)=-\frac{1}{2\ln\varphi}\ln q(y)\)
and its SAME-CUT feedback source obey the exact identity
\[
 \boxed{dJ_z=
    \frac{2z\,q\,\ln\varphi}{1-z+zq}\,dP_{\rm port}.}   \tag{8}
\]
This factor is **derived**, positive and field-dependent; it is not a
chosen coupling. For the exact Q8 point \(q=p^6\), the continuous
mathematical limit at \(z\uparrow1\) gives
\[
 J_1=-\ln p^6=6\ln\varphi
          =2\ln\varphi\,P_{\rm dark}.                  \tag{9}
\]
The actual configured fugacity need not be \(1\); at \(z=2^{-20}\)
one must use the genuine smaller factor (8), not (9).
The full two-port active cut \(P=I_2\) has \(F=0\) and \(J=0\):
the port selection really matters.

This establishes a precise small-scale **value-and-source bridge**
between the existing Golden interferometer and Book's determinant
calculus without changing the operator or inventing Info. It is not
a binding of the original full128 selected Book cut, where the effects
have higher rank and a nonscalar cost mark. Nor is a branch-cost
deformation in §2 automatically a unitary \(U(y)\): the unitary
hypothesis is essential in (8).

## 3. Exactly what this changes for the GR closure gate

The existing Book03 first-source underdetermination has a second,
independent **memory/observer** aspect even after positive Golden
weights are specified. The source of a represented log-norm action
contains both the signed coefficients (6) and the holonomy/source term
in (2). Terminal Born probabilities, a Shannon entropy and a scalar
mean Cost–Info do not reconstruct these in general. Normalized
probabilities also cannot select the common absolute amplitude mode.

This creates one concrete, falsifiable *same-execution* test rather than
another geometric root search:

1. On the ORIGINAL selected CAR/oldRIGHT full history, derive the
   **actual Book03 memory representation and chosen observer cut**
   before evaluating any scalar pressure.
2. Determine actual \(G,dG\), all absolute \(C_\gamma,I_\gamma\)
   and their jets on the SAME controller, preparation and clock.
3. Evaluate (3) on its selected cut and every field/input tangent;
   independently evaluate all retained cost/heat/archive terms.
4. Compare the resulting full covector against the existing
   \(16+24+2\) Einstein–CAR source, not against the already known
   dark-port probability alone.

A completed GR theorem cannot be inferred from (3) or (5). They
do NOT derive a compulsory scalar aggregator, a physical selection
law, full-Book Info, a native gate for varying loop phase, or the
original raw216 refinement. The new result is a rigorously scoped
**interference-aware source formula and an exact native Golden
counterexample to positive branch-price averaging**. It directly
reuses the historical Q8 order witness and the newer Book03
under\-determination instead of adding a new candidate action.

Reproducibility: the bundled standard-library checker verifies the
Golden polynomial identities, both outgoing port amplitudes,
whole-two-port unitarity, Q8 commutator, exact signed source,
the +1 finite formal branch-price contrast and common-unitary norm
invariance. The calculation is finite/algebraic; it is not a
full128/Book03 input or geometry replay. Keep #334 Draft;
\`GR_closed=false\`.
