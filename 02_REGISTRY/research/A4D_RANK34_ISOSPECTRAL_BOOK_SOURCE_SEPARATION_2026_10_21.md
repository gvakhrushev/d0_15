# Rank-34 readout does not entail a Book03 first source: an exact finite isospectral separation

21 October 2026. Research continuation **inside existing Draft PR #334**.
Phase: native realization / Book03 first-source selection. This is an exact
finite mathematical countermodel **and a sufficient anchored-source
construction**, not a new action chosen for D0 or a physical GR theorem.
The target consumer is the existing same-execution common-map gate.
\`GR_closed=false\`.

## 1. Exact obstruction: a full-rank observable chart may be spectrally silent

Book03 section 03.25 fixes the **single** master action

\[
 {\cal B}(y)=\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta(y)}
              -\log\det(I-\zeta F(y)),\quad \beta>0.
 \tag{1}
\]

Here \(\zeta\) is the **feedback fugacity**, not a geometric coordinate.
Assume positive heat, selfadjoint feedback with \(I-\zeta F>0\), and
finite matrices. The complete first-source formula is

\[
 D{\cal B}[v]=-\frac{\operatorname{Tr}(e^{-\beta\Delta}D\Delta[v])}
                         {\operatorname{Tr}e^{-\beta\Delta}}
                  +\zeta\operatorname{Tr}((I-\zeta F)^{-1}DF[v]).
 \tag{2}
\]

This is the derivative of the *actual chosen master scalar*, not a choice
between mean path Cost-Info and log-amplitude pressure.

**Isospectral lemma.** Suppose the field changes \(\Delta\) and \(F\)
only by unitary conjugation (the conjugating unitary may differ for the
two operators). Then \(D{\cal B}=0\), to every order, even if fixed
external reporting effects distinguish all those changes.

Proof: each partition factor in (1) is a class function. Infinitesimally,
\(D\Delta=[K,\Delta]\) and \(DF=[L,F]\) for skew-Hermitian generators.
Both traces in (2) vanish by cyclicity and commutation with their
respective spectral functions. Degenerate eigenvalues cause no exception.
In particular, if \(P(y)\) is any smooth rank-\(r\) orthogonal projection
and both operators are unitarily equivariant *functions of \(P\) alone*,
then all rank-\(r\) projectors lie on one unitary orbit and
\({\cal B}(P(y))\) is exactly constant. QED.

This is not a claim that Book03's **actual native** \(\Delta_N,F_N\)
are projection-only. It rules out using rank, projector orientation,
or local observability **in place of** their native spectral source.

## 2. Exact 34-direction finite witness, with a genuine Hodge square

Work on \(H=\mathbb C^{18}\). Let
\(z_j=x_j+i y_j\) for \(j=1,\dots,17\), and set

\[
 \psi(z)=\frac{e_0+\sum_{j=1}^{17}z_je_j}
                   {\sqrt{1+\sum_j|z_j|^2}},
 \qquad P(z)=|\psi(z)\rangle\langle\psi(z)|.
 \tag{3}
\]

Thus \(P(z)\) always has rank one, on a real 34-dimensional open chart.
For 34 **separately addressed binary tests** fix the reference effects

\[
 R_j=\left|\frac{e_0+e_j}{\sqrt2}\right\rangle
             \left\langle\frac{e_0+e_j}{\sqrt2}\right|,
 \quad
 I_j=\left|\frac{e_0+i e_j}{\sqrt2}\right\rangle
             \left\langle\frac{e_0+i e_j}{\sqrt2}\right|.
\]

Their Born probabilities are

\[
 q_j^R(z)=\frac{1+2x_j+x_j^2+y_j^2}
                  {2(1+\sum_k|z_k|^2)},\quad
 q_j^I(z)=\frac{1+2y_j+x_j^2+y_j^2}
                  {2(1+\sum_k|z_k|^2)}.                 \tag{4}
\]

At \(z=0\) all 34 probabilities equal \(1/2\), and in the ordered
\((x_1,\ldots,x_{17},y_1,\ldots,y_{17})\) coordinates,

\[
 \boxed{D(q^R,q^I)_{z=0}=I_{34},\quad \det Dq=1.}       \tag{5}
\]

Nevertheless choose arbitrary fixed \(a,b>0\) and the two-term finite
cochain complex \(C^0=H\longrightarrow C^1=H\) with differential

\[
 d_P=\sqrt a\,P+\sqrt b\,(I-P).
\]

Its **true nonnegative Hodge Laplacian** is
\(\Delta_P=d_P^\dagger d_P\oplus d_Pd_P^\dagger\);
the eigenvalues are \(a\) (multiplicity two) and \(b\) (multiplicity
34). On the same 36-dimensional space take \(F_P=c(P\oplus P)\),
\(c=\varphi^{-2}\), \(0<\zeta c<1\). The *literal* (1) is

\[
 \boxed{{\cal B}(P)=\beta^{-1}\log(2e^{-\beta a}+34e^{-\beta b})
                    -2\log(1-\zeta c),}                \tag{6}
\]

independent of every one of the 34 parameters. Equations (5)--(6)
give an explicit exact countermodel to

\[
 \operatorname{rank}Dq=34 \;\Longrightarrow\;
 \text{nonzero or determined Book03 Euler source}.
\]

No original D0 CAR16/full128 Hilbert space is claimed to equal this
auxiliary two-term example. It refutes the general **inference**,
not the independent native rank-34 theorem. A Hodge Laplacian and the
Book03 master form alone do not fix the representation/pullback.

A particularly immediate corollary for the **literal one-tick Golden
splitter**, \(F=cP\), is
\(\det(I-\zeta F)=(1-\zeta c)^r\) on any rank-\(r\) projection.
Its normalized feedback source is identically zero on a fixed-rank
chart. The nonlinear field source must involve the **actual moving
multitick return effect** and/or a nontrivial heat response; a splitter
value identity by itself does not supply it.

## 3. Positive minimal interface: a fixed physical reference breaks blindness

The *same* rank-34 probability chart also demonstrates what extra
information is sufficient to create a source-sensitive finite
feedback operator. Retain the fixed external effects \(R_j,I_j\) and
their complements, each with its own paid binary setting if executed.
On a **separate mathematical 68-port reporter** define

\[
 F_{\rm ref}(z)=c\,\operatorname{diag}
       (q_1(z),1-q_1(z),\ldots,q_{34}(z),1-q_{34}(z)),
 \quad \alpha=\zeta c\in(0,1).
 \tag{7}
\]

Every eigenvalue is between 0 and \(c\); thus (1) has a valid positive
feedback determinant. Its complete feedback action is

\[
 A_{\rm ref}(z)=
 -\sum_{j=1}^{34}\log[(1-\alpha q_j(z))
                      (1-\alpha(1-q_j(z)))] .          \tag{8}
\]

The derivative of the \(j\)-th summand with respect to its probability
vanishes at \(q_j=1/2\). The second derivative there is
\(2\alpha^2/(1-\alpha/2)^2\). By (5), at \(z=0\),

\[
 DA_{\rm ref}=0,\qquad
 \boxed{D^2A_{\rm ref}
          =\frac{2\alpha^2}{(1-\alpha/2)^2} I_{34}>0.}   \tag{9}
\]

For the explicit \(\zeta=1/2,\ c=\varphi^{-2}\), the eigenvalue is
\(0.08916494400134596\ldots\). This is a **constructive spectral
sensitivity theorem**: fixed addressed reference effects can turn
the same complete-rank operational chart into a nondegenerate
first-source/Hessian interface, without introducing negative
feedback eigenvalues.

It is **not** a construction of an admitted D0 control/writer or a
claim that the actual Book03 \(F_N(V)\) equals (7). The 34 binary
settings are not one free simultaneous POVM. Their controller,
preparation, failures, retained work, reference and clock would all
have to be included and paid. This convex local source merely pins
operational odds to a reference and does **not** equal the Einstein
action or its known saddle Hessian. It must not be used to fit a
physical selector.

## 4. Strategic substitution into the existing GR common-map gate

The previously proved native 34-readout inverse and this exact
countermodel establish **two distinct mathematical requirements**:

* Observability: \(\operatorname{rank}Dq=34\), already owned on its real
  native carrier. It identifies the field chart, not the selected
  scalar response or reachable same-initial variations.
* Source: the **actual** \(\Delta_N(V)\) and \(F_N(V)\), with their native
  fixed incidence/reference/clock context, must have the correct
  weighted spectral jets (2) along the **actually admitted** field
  and independent-input directions. Unitary-orbit changes alone
  contribute nothing. Full operator reconstruction is stronger than
  needed for the **first** source: the two weighted traces in (2)
  suffice once they have been shown to arise from one selected paid
  history, with its real heat, cut and normalization.

This yields a small decisive test, not another rank scan: on the same
native paid execution, compare \(Dq\) with the two weighted traces
in (2) for the existing 16+24+2 directions **and** the genuine
preparation/controller/clock tangents. Test an explicitly non-gauge
direction on which the Einstein/CAR covector is known to be nonzero.
If both spectral terms are zero there, that chosen complete execution
cannot have the claimed Einstein source even if all measurements
remain invertible. If not, transport their *complete* source including
upstream terms, rather than promote the reference demonstration (7).

This note consumes the existing rank-34 geometric observability and
Book03 §03.25/§03.26, but does **not** discharge original physical
admission, heat identification, native stationary/constraint law,
two-sided GR recovery, raw216 or refinement. It creates no new
selector or task. \`GR_closed=false\`.

## 5. Narrow reproducibility

\`sources/d0_rank34_isospectral_source_2026-10-21/check_rank34_isospectral.py\`
independently evaluates (4) both directly and via complex Born inner
products, all 1,156 first Jacobian entries, the exact isospectral
master value (6), and the anchored first/second-variation controls.
Standard Python library only. It does not replay or replace any
old full128, geometric, Lean or physical Book certificates.
