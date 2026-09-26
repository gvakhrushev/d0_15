# MEMO A4D — discrete Palatini(+Λ+T²) target vs span{S_★, I^η, I^n}

**Lane:** Wall B / OTO (research checkpoint; after flat-jet split)  
**Execution:** Draft research PR on `research/a4d-discrete-palatini-target-span`  
**Status:** EXACT / CERTIFIED  
**Baseline:** `75fc9eec99dcb8b5b15a0bc0de5662c9453175f4`  
**Certificates:**
- `a4d_flat_jet_q_vanishing_check.py` (seed/completion split; prerequisite)
- `a4d_discrete_palatini_target_span_check.py` (this packet)

## 0. Verdict

On the Role / `ArchiveRolePhaseGroup` \(L=2\) carrier, using only owned
discrete tensors (based plaquettes, \(G_2\), \(\star\), solder legs, joint
residual \(R_{2|1}\)), the typed target

\[
S_{\mathrm{target}}
=
S_{\star}
+
\lambda\,\mathrm{Vol}_\eta(e)
+
\alpha\,I^\eta
+
\beta\,I^n
\tag{0.1}
\]

satisfies:

- \(\lambda=0\): \(S_{\mathrm{target}}\in\operatorname{span}\{S_{\star},I^\eta,I^n\}\);
- \(\lambda\neq0\): \(S_{\mathrm{target}}\) requires the additional owned
  channel \(\mathrm{Vol}_\eta\).

Single-plaquette \(T_{\mathrm{open}}^2\) is a full-affine NO-GO; the minimal
legal torsion-square is \(I^\eta\) (or \(I^n\)).

No Holst / \(\varphi\) channel is introduced.  Low-order alternative Palatini
seeds with a nonzero flat 2-jet are Plan B only if an Einstein-ray detector
reports a nonzero \(E_{\mathrm{sp}}\) coefficient; this packet does not invent
such a seed.

Terminal:

\[
\boxed{\texttt{DISCRETE-PALATINI-TARGET-NEEDS-INVARIANT: Vol\_eta}}.
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

### 1.3 Cosmological candidate \(\mathrm{Vol}_\eta\)

\[
\mathrm{Vol}_\eta(e,x)
=
\varepsilon_\eta\bigl(e_A(x),e_B(x),e_C(x),e_D(x)\bigr)
=
\det\bigl(e_A|e_B|e_C|e_D\bigr),
\tag{1.4}
\]

the Lorentz volume of the four Role solder legs, normalized so that the
\(\eta\)-orthonormal identity coframe has volume \(1\).  This uses only the
owned solder legs and the volume form of \(\eta\).  It is \(SO^+(1,3)\)
invariant and site-local.

## 2. Span comparison (exact \(\mathbb Q\))

### 2.1 Flat-link locus

On identity Lorentz links \(P_S=I\):

- \(\mathcal R(P)=0\Rightarrow S_{\star}=0\);
- \(X=0\Rightarrow R_{2|1}=0\Rightarrow I^\eta=I^n=0\);
- \(\mathrm{Vol}_\eta\) still varies with the coframe
  (\(\mathrm{Vol}(e_{\mathrm{id}})=1\),
  \(\mathrm{Vol}(e_{\mathrm{scaled}})=3/2\), and a third generic frame).

Hence \(\mathrm{Vol}_\eta\notin\operatorname{span}\{S_{\star},I^\eta,I^n\}\)
as functionals.  The evaluation matrix with an added \(\mathrm{Vol}\) column
raises rank by exactly one over \(\mathbb Q\).

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

On the flat-link locus,
\(S_{\mathrm{target}}=\lambda\,\mathrm{Vol}_\eta\).  For \(\lambda\neq0\) this
is nonzero while every star-Q combination vanishes, so the full
Palatini\((+\Lambda+T^2)\) target needs the owned invariant \(\mathrm{Vol}_\eta\).

## 3. Compatibility with the flat-jet split

From the companion packet:

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

\(\mathrm{Vol}_\eta\) is independent of the curvature flat jet (it is a pure
coframe 0-jet); its obstruction is span membership, not jet order.  This is
why a nonzero-\(\Lambda\) target is a finite enlargement by an owned tensor,
not a competitor to the Einstein-ray 2-jet of \(S_{\star}\).

## 4. Scope and non-claims

- Exact finite typing and \(\mathbb Q\)-span comparison only.
- Does not claim continuum Einstein field equations.
- Does not select numerical \((\lambda,\alpha,\beta)\).
- Does not promote Lean / claims / BOOK.
- Does not edit `#201` / `#202` primary files.
- Four-orbit evaluation matrix for
  \((I^\eta_{\mathrm{adj}},I^\eta_{\mathrm{opp}},I^n_{\mathrm{adj}},I^n_{\mathrm{opp}})\)
  has exact rank 4 on the certificate sample set (so a single rank-1 witness
  does not kill the \(a=b\) ray globally).  A structural adj/opp identity, if
  any, remains open.

## 5. Validation

```
python 02_REGISTRY/research/certificates/a4d_flat_jet_q_vanishing_check.py
python 02_REGISTRY/research/certificates/a4d_discrete_palatini_target_span_check.py
```

Expected terminals (both exit 0):

```
TERMINAL: DISCRETE-FLAT-JET-Q-VANISHES
TERMINAL: DISCRETE-PALATINI-TARGET-NEEDS-INVARIANT: Vol_eta
```
