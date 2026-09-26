# MEMO A4D — discrete Palatini(+Λ+T²) target vs span{S_★, I^η, I^n}

**Lane:** Wall B / OTO (research checkpoint; after flat-jet split)  
**Execution:** PR #207 / `exp/a4d-discrete-palatini-target-span`  
**Status:** EXACT / CERTIFIED / TERMINAL  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`  
**Prerequisites:** merged #217 (exact star seed / flat-jet completion split), merged #218 (affine relative-solder covariance)  
**Certificate:** `a4d_discrete_palatini_target_span_check.py`

## 0. Verdict

On the Role / `ArchiveRolePhaseGroup` \(L=2\) carrier, using only owned
discrete tensors (based plaquettes, \(G_2\), \(\star\), solder legs, joint
residual \(R_{2|1}\)), the typed target

\[
S_{\mathrm{target}}
=
S_{\star}
+
\lambda\,\mathrm{Vol}_{\rm rel}(\widehat\Theta)
+
\alpha\,I^\eta
+
\beta\,I^n
\tag{0.1}
\]

satisfies:

- \(\lambda=0\): \(S_{\mathrm{target}}\in\operatorname{span}\{S_{\star},I^\eta,I^n\}\);
- \(\lambda\neq0\): \(S_{\mathrm{target}}\) requires one additional
  owned channel, the **full-affine legal relative volume**
  \(\mathrm{Vol}_{\rm rel}=\det\widehat\Theta\).

Single-plaquette \(T_{\mathrm{open}}^2\) is a full-affine NO-GO; the minimal
legal torsion-square is \(I^\eta\) (or \(I^n\)).

No Holst / \(\varphi\) channel is introduced.  Low-order alternative Palatini
seeds with a nonzero flat 2-jet are Plan B only if an Einstein-ray detector
reports a nonzero \(E_{\mathrm{sp}}\) coefficient; this packet does not invent
such a seed.

Terminal:

\[
\boxed{\texttt{DISCRETE-PALATINI-TARGET-NEEDS-INVARIANT: Vol\_rel}}.
\]

## 1. Exact discrete formulae

### 1.1 Palatini seed \(= S_{\star}\)

\[
\mathcal L_{\star}(S,x)
=
c\,\epsilon_S\,
G_2\!\bigl(
B_{S^c}(e,x),
\star\,\mathfrak b(\mathcal R(P_S(A,x)))
\bigr),
\qquad
\mathcal R(P)=\tfrac12(P-P^{-1}),
\tag{1.1}
\]

with counting sum \(S_{\star}=\sum_{x,S}\mathcal L_{\star}(S,x)\).  This is the
owned finite replacement of the conditional continuum pattern
\(\epsilon_{abcd}e^a e^b X^{cd}\) (cf. gravity-gate §2), already typed by the
star-density packet.  It contains no \(R^2\), no volume potential, and no
torsion square.

### 1.2 Legal torsion-square (Q-family)

\[
I^\eta_{2|1}=R_{2|1}^{T}\eta R_{2|1},
\qquad
I^n_{2|1}=R_{2|1}^{T}h_n R_{2|1},
\tag{1.2}
\]

with

\[
R_{2|1}
=
\det(X_1)t_2-X_2\operatorname{adj}(X_1)t_1,
\qquad
X_i=I-P_i.
\tag{1.3}
\]

Open torsion \(T_{\mathrm{open}}\) is translation-transitive on the generic
invertible-\(F\) stratum, so \(T_{\mathrm{open}}^2\) is not a continuous
full-affine scalar.  The certificate gauges a concrete \(T\) to zero while
keeping the legal \(I^\eta\) well-typed on the two-loop residual.

### 1.3 Full-affine legal cosmological channel \(\mathrm{Vol}_{\rm rel}\)

The raw determinant \(\det\Theta\) is only proper-Lorentz invariant; by
itself it is **not** invariant under the selected affine translation action.
Merged #184/#218 supply the required translation-completed solder row

\[
\widehat\Theta_{x,r}
=
\Theta_{x,r}-b_{x,r}^{\flat_{n_x}}.
\tag{1.4}
\]

At the uniquely selected relative factor \(\lambda_{\rm rel}=1\), merged
#218 proves row-by-row

\[
\boxed{
\widehat\Theta'_{x,r}
=
\widehat\Theta_{x,r}g_x^{-1}
}.
\tag{1.5}
\]

Assembling the four Role rows at one site gives

\[
\widehat\Theta'_x=\widehat\Theta_x g_x^{-1}.
\tag{1.6}
\]

The selected finite gauge group is \(SO^+(1,3)\), so
\(\det g_x=1\). Therefore

\[
\boxed{
\mathrm{Vol}_{\rm rel}(x)
:=
\det\widehat\Theta_x,
\qquad
\mathrm{Vol}'_{\rm rel}(x)=\mathrm{Vol}_{\rm rel}(x)
}.
\tag{1.7}
\]

Thus the missing \(\Lambda\)-channel is already built from owned data and
is legal under the **full affine quotient**, not merely under its Lorentz
subgroup.

It also descends to the metric quotient. Define

\[
\widehat Q_x
=
\widehat\Theta_x\eta\widehat\Theta_x^T.
\tag{1.8}
\]

Then \(\widehat Q'_x=\widehat Q_x\), and because
\(\det\eta=-1\),

\[
\boxed{
\det\widehat Q_x
=
-\det(\widehat\Theta_x)^2
=
-\mathrm{Vol}_{\rm rel}(x)^2
}.
\tag{1.9}
\]

Hence on each fixed orientation component

\[
\mathrm{Vol}_{\rm rel}
=
\pm\sqrt{-\det\widehat Q}.
\tag{1.10}
\]

This is the exact zeroth-order metric channel needed to type a cosmological
term. Its coefficient is not selected here.

## 2. Span comparison (exact \(\mathbb Q\))

### 2.1 Flat-link locus

On identity Lorentz links \(P_S=I\):

- \(\mathcal R(P)=0\Rightarrow S_{\star}=0\);
- \(X=0\Rightarrow R_{2|1}=0\Rightarrow I^\eta=I^n=0\);
- on the legal slice \(b^{\flat_n}=0\),
  \(\widehat\Theta=\Theta\), so \(\mathrm{Vol}_{\rm rel}\) reduces to
  the old determinant witness and still varies with the coframe
  (\(1\), \(3/2\), and a third generic rational value).

Hence \(\mathrm{Vol}_{\rm rel}\notin
\operatorname{span}\{S_{\star},I^\eta,I^n\}\) as functionals. The
evaluation matrix with the legal relative-volume column raises rank by exactly
one over \(\mathbb Q\).

### 2.2 Targets without \(\Lambda\)

\[
S_{\star},
\quad
S_{\star}+I^\eta,
\quad
S_{\star}+I^n
\]

lie in \(\operatorname{span}\{S_{\star},I^\eta,I^n\}\) by construction
(certificate checks on a curved plaquette sample with nonzero residual).

### 2.3 Targets with \(\Lambda\)

On the flat-link, zero-relative-shift locus,
\(S_{\mathrm{target}}=\lambda\,\mathrm{Vol}_{\rm rel}\). For
\(\lambda\neq0\) this is nonzero while every star-Q combination vanishes,
so the full Palatini\((+\Lambda+T^2)\) target needs exactly one additional
owned channel, \(\mathrm{Vol}_{\rm rel}\). Unlike the provisional
\(\mathrm{Vol}_\eta(\Theta)\), this replacement has now passed the
full-affine legality gate.

## 3. Compatibility with the flat-jet split

From merged #217:

\[
j^{2}_{\mathrm{flat}}I^\eta
=
j^{2}_{\mathrm{flat}}I^n
=
0.
\]

Therefore, whenever \(\lambda=0\),

\[
j^{2}_{\mathrm{flat}}S_{\mathrm{target}}
=
j^{2}_{\mathrm{flat}}S_{\star}.
\]

\(\mathrm{Vol}_{\rm rel}\) is independent of the curvature flat jet (it
is a zeroth-order relative-solder/metric channel); its role is span
enlargement, not modification of the Einstein-ray 2-jet of \(S_{\star}\).
Thus the derivative seed/completion sector and the cosmological sector remain
separated.

## 4. Scope and non-claims

- Exact finite typing, full-affine legality of the relative volume, metric
  descent, and \(\mathbb Q\)-span comparison only.
- Does not claim continuum Einstein field equations.
- Does not select numerical \((\lambda,\alpha,\beta)\).
- Does not promote Lean / claims / BOOK.
- Uses merged #218's exact relative-solder covariance theorem and the selected
  proper-Lorentz quotient; does not edit #201/#202 primary files.
- Four-orbit evaluation matrix for
  \((I^\eta_{\mathrm{adj}},I^\eta_{\mathrm{opp}},I^n_{\mathrm{adj}},I^n_{\mathrm{opp}})\)
  has exact rank 4 on the certificate sample set (so a single rank-1 witness
  does not kill the \(a=b\) ray globally).  A structural adj/opp identity, if
  any, remains open.

## 5. Validation

```
python 02_REGISTRY/research/certificates/a4d_discrete_palatini_target_span_check.py
```

Expected terminal (exit 0):

```
TERMINAL: DISCRETE-PALATINI-TARGET-NEEDS-INVARIANT: Vol_rel
```
