# A4D diagonal microstructure slow-background response

**Task:** `WRK-A4D-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-RESPONSE`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Inputs:** merged #232 family and flat-solder vanishing; #201 Gram lift \(H(q)=\tfrac12 q\eta\); #226 normalization, applied once to the finished partial.
**Certificate:** `02_REGISTRY/research/certificates/a4d_diagonal_microstructure_slow_background_response_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-DIAGONAL-MICROSTRUCTURE-EINSTEIN-RESPONSE-OBSTRUCTION-FOUND}}
\]

On the declared slow profile, before any amplitude scaling, the \((0,1)\) component of the pointwise metric partial is

\[
\boxed{
\Delta E_Q[E_{01}+E_{10}]
=
-\sigma(p)\,
\frac{h z}{4+3z^2}.
}
\]

The coefficient of the monomial \(h^1 z^1\) is \(-\sigma(p)/4\), with \(\sigma=(+1,+1,-1,-1)\). It is not \(o(h^2)\).

At the declared scaling \(z_h=h\), phase \(0\),

\[
h^{-2}\Delta E_Q[E_{01}+E_{10}]
=
-\frac{1}{4+3h^2}
\to -\frac14.
\]

The identity connection contributes \(0\). The normalized pointwise limit is a nonzero period-4 field.

At \(z_h=h^2\) the same component has normalized limit \(0\). A pure slow gradient, with no local value, also has normalized limit \(0\) at both scalings. Those specializations are not the terminal.

## 1. Conventions

\(Y=J_{12}-J_{13}+J_{23}\), \(U(z)\) its Cayley image, and

\[
(W_0,W_1,W_2,W_3)=(U,I,U^{-1},I),
\qquad
L_0=W_p,\quad L_s=I,
\]

with \(p=x_0+x_1+x_2+x_3\pmod4\). Faces \((0,s)\) have curvature \(\sigma(p)\,c(z)\,Y\), \(c(z)=4z/(4+3z^2)\). Spatial faces are flat. The ten Gram directions use \(H(q)=\tfrac12 q\eta\), so the first-order Gram change is exactly \(q\). The flat control in these ten directions is the zero vector, in agreement with \(E_Q(\eta,K(z))=0\).

\(K_{\mathrm{sm}}\) is the identity connection. Its partial is zero on every tested Gram. No discrete Levi-Civita solver and no numerical value of \(-\tfrac12 G\) are used.

## 2. Declared slow profiles

Both profiles change between \(x_0\) and \(x_0+1\).

Valued slow field:

\[
Q=\eta+h\alpha+h^2 x_0\beta,
\qquad
\alpha=E_{12}+E_{21},
\quad
\beta=E_{01}+E_{10}.
\]

The \((0,1)\) component is exactly \(-\sigma(p)\,hz/(4+3z^2)\). The neighbor slope \(\beta\) first appears in other components, at order \(h^2 x_0\), and does not cancel this term.

Pure gradient, \(\alpha=0\):

\[
Q=\eta+h^2 x_0\beta.
\]

Its first nonzero piece is order \(h^2 z\). After \(h^{-2}\) and either \(z=h\) or \(z=h^2\), the limit is \(0\).

## 3. Phase average

The four phase values of the \(h^1 z^1\) coefficient sum to zero. That average is a separate object. It is not the pointwise partial and it is not this terminal.

## 4. Scope

This is one microstructure, two explicit slow jets, and the identity comparator. It does not promote a continuum Einstein equation, a cell-averaged effective action, or a statement about every Gram. No new density, Holst term, torsion constraint, or selector is introduced.

## 5. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_diagonal_microstructure_slow_background_response_check.py
```
