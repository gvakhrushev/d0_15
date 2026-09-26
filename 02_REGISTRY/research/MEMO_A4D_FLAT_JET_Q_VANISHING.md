# MEMO A4D — flat 2-jet vanishing of quadratic joint-residual completions

**Lane:** Wall B / OTO seed–completion split (research checkpoint)  
**Execution:** Draft research PR on `research/a4d-discrete-palatini-target-span`  
**Status:** EXACT / CERTIFIED  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`  
**Certificate:** `02_REGISTRY/research/certificates/a4d_flat_jet_q_vanishing_check.py`

## 0. Verdict

For the owned polynomial two-holonomy residual

\[
R_{2|1}
=
\det(X_1)\,t_2
-
X_2\,\operatorname{adj}(X_1)\,t_1,
\qquad
X_i=I-P_i,
\tag{0.1}
\]

every constant-matrix quadratic readout

\[
Q(R)=R^{T}HR
\tag{0.2}
\]

(including the Q-family generators \(I^\eta=R^{T}\eta R\) and \(I^n=R^{T}h_n R\))
satisfies

\[
\boxed{
R_{2|1}=O(X^{4}t),
\qquad
Q=O(X^{8}t^{2})
}
\tag{0.3}
\]

in four dimensions.  In the flat simultaneous scaling \(X=O(\varepsilon)\),
\(t=O(\varepsilon)\) one has the sharper

\[
\boxed{Q=O(\varepsilon^{10})}.
\tag{0.4}
\]

Consequently the flat 2-jet vanishes identically,

\[
\boxed{j^{2}_{\mathrm{flat}}Q=0},
\tag{0.5}
\]

and the seed / completion split is locked:

\[
\boxed{
j^{2}_{\mathrm{flat}}(S_{\star}+Q)
=
j^{2}_{\mathrm{flat}}S_{\star}.
}
\tag{0.6}
\]

Terminal:

\[
\boxed{\texttt{DISCRETE-FLAT-JET-Q-VANISHES}}.
\]

No continuum Einstein equation is imported.  No Holst / \(\varphi\) channel is
introduced.  This packet does not edit `#201` / `#202` primary files.

## 1. Exact order algebra

In dimension \(d=4\), the determinant is a homogeneous polynomial of degree 4
and the adjugate is homogeneous of degree 3:

\[
\det(\lambda X)=\lambda^{4}\det(X),
\qquad
\operatorname{adj}(\lambda X)=\lambda^{3}\operatorname{adj}(X).
\tag{1.1}
\]

(The Cayley identity \(X\operatorname{adj}(X)=\det(X)\,I\) is recorded as a
control.)  Substituting the multi-homogeneous scaling
\(X_i=\lambda A_i\), \(t_i=\mu u_i\) into (0.1) therefore yields

\[
R_{2|1}(\lambda A,\mu u)
=
\lambda^{4}\mu\,R_{2|1}(A,u).
\tag{1.2}
\]

Any quadratic form \(Q=R^{T}HR\) then scales as

\[
Q(\lambda A,\mu u)
=
\lambda^{8}\mu^{2}\,Q(A,u).
\tag{1.3}
\]

This is the exact content of (0.3).  The certificate verifies (1.1)–(1.3) on
several rational matrix / vector witnesses and for \(H\in\{\eta,h_n,
\eta+\tfrac37 h_n,H_{\mathrm{gen}}\}\).

## 2. Flat 2-jet

Specialize to a flat perturbation parameter \(\varepsilon\) in two regimes.

### 2.1 Translation held fixed

Take \(X=\varepsilon A\), \(t\) fixed.  Then \(Q=O(\varepsilon^{8})\).  All
derivatives of order \(\le 2\) (in fact all of order \(\le 7\)) vanish at
\(\varepsilon=0\), and the order-8 leading coefficient is nonzero on the
chosen witnesses.

### 2.2 Simultaneous flat jet

Take \(X=\varepsilon A\), \(t=\varepsilon u\).  Then \(Q=O(\varepsilon^{10})\).
All derivatives of order \(\le 2\) (in fact \(\le 9\)) vanish at
\(\varepsilon=0\), with nonzero order-10 leading coefficient.

In both regimes

\[
j^{2}_{\mathrm{flat}}Q=0.
\tag{2.1}
\]

The owned channels \(I^\eta\) and \(I^n\) inherit the same vanishing because
they are instances of (0.2).

## 3. Seed / completion split

Let \(S_{\star}\) be any seed density whose flat expansion is defined through
order 2 (in particular the accepted star density of
`MEMO_A4D_STAR_DENSITY_VARIATION_PRESSURE.md`).  Adding any quadratic
completion \(Q(R)\) of the form (0.2) cannot change the flat 2-jet:

\[
\frac{d^{k}}{d\varepsilon^{k}}\Big|_{0}(S_{\star}+Q)
=
\frac{d^{k}}{d\varepsilon^{k}}\Big|_{0}S_{\star}
\qquad(k=0,1,2).
\tag{3.1}
\]

Thus every linearized / Hessian-level detector that depends only on
\(j^{2}_{\mathrm{flat}}\) (including the flat Einstein-ray comparison of the
star seed) is insensitive to the choice of quadratic joint-residual
completion coefficients.  This is a finite algebraic split, not a continuum
claim.

## 4. Scope and non-claims

- Exact on the polynomial residual (0.1) and quadratic readouts (0.2).
- Does not select coefficients inside the Q-family.
- Does not assert a continuum Einstein field equation.
- Does not construct a discrete Palatini\((+\Lambda+T^{2})\) target (deferred
  to the companion Wall-B packet on this branch).
- Does not promote Lean / claims / BOOK.

## 5. Validation

```
python 02_REGISTRY/research/certificates/a4d_flat_jet_q_vanishing_check.py
```

Expected terminal line:

```
TERMINAL: DISCRETE-FLAT-JET-Q-VANISHES
```

with process exit code 0.
