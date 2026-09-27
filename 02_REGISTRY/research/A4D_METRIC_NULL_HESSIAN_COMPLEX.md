# A4D metric-null Hessian complex

**Task:** \`WRK-A4D-METRIC-NULL-HESSIAN-COMPLEX\`  
**Lifecycle:** IN_PROGRESS  
**Scope:** exact finite symbol algebra and flat smooth-symbol Schur reduction; no BOOK/claim promotion.

## Terminal candidate

\`J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT\`

The finite metric-response block is not an unexplained one-complex-dimensional kernel repeated on nine L=4 orbits. It is the fibre of an exact character-difference complex. Near the trivial character, Schur elimination of the connection block produces exactly the flat linearized Einstein symbol with the owned coefficient \`-1/2\`.

This result changes the interpretation of the FUGU forward scouts. Their nonzero fixed-vector detune derivative is real, but it is the derivative of a moving null line and is therefore not by itself a physical quotient obstruction.

## 1. Exact character-difference owner

Write

\[
d_r=z_r^{-1}-1.
\]

The accepted polarized cross block \`C(z)=H_AQ(z)\` is linear in \(d\). Define the universal symmetric-column Koszul map

\[
\mathcal W_d:\operatorname{Sym}^2(\mathbb C^4)\to
\Lambda^2(\mathbb C^4)\otimes\mathbb C^4,
\qquad
(\mathcal W_d q)_{ab|c}=d_aq_{bc}-d_bq_{ac}.
\]

The checker expands both maps in the forty coefficient slots \(d_rq_{ab}\) and proves

\[
\operatorname{row}_{\mathbb Q}C(d)
=
\operatorname{row}_{\mathbb Q}\mathcal W_d
\]

as a constant rational row module: both coefficient-row spaces have dimension 20 and their joined space still has dimension 20. Therefore the two maps have the same pointwise kernel for every character.

## 2. Global metric-null line

The exact null generator is

\[
\boxed{q_d=d\,d^T.}
\]

Indeed \(C(d)q_d=0\) symbolically. More strongly, if \(\mathcal W_dq=0\) and \(d_j\neq0\), then

\[
d_j^2q_{ac}-d_ad_cq_{jj}
=
d_j(d_jq_{ac}-d_aq_{jc})
+d_a(d_jq_{jc}-d_cq_{jj})=0,
\]

so

\[
q=\frac{q_{jj}}{d_j^2}\,d\,d^T.
\]

Hence for every nontrivial character

\[
\boxed{\ker C(d)=\operatorname{span}_{\mathbb C}\{d\,d^T\}},
\qquad
\boxed{\operatorname{rank}C(d)=9}.
\]

At the trivial character \(d=0\), \(C=0\); that is the only rank jump of this metric-response block.

The conjugate-paired realification therefore gives exactly the already-owned two-real-dimensional metric-only block of #262. The nine-orbit L=4 rank-nine census is a finite sample of this global theorem, not its origin.

## 3. FUGU detune reinterpretation

Let \(D_j=z_j\partial_{z_j}\). Differentiating the exact null identity gives

\[
D_j(Cq_d)=0
\quad\Longrightarrow\quad
\boxed{(D_jC)q_d=-C(D_jq_d)}.
\]

Thus every raw FUGU vector

\[
w_j=(D_jC)q_d
\]

lies identically in \(\operatorname{im}C\), before any use of the connection block \(A\).

The nonzero norms reported by the FUGU v2 scout remain correct as fixed-vector derivatives. What fails is the promotion to a new physical row: the computation held \(q\) fixed while the one-dimensional null fibre itself moves with the character. Transporting the canonical section \(q_d\) cancels the derivative exactly.

Therefore the v3/v4 classification by \(w\in\operatorname{im}A\) versus \(w\notin\operatorname{im}A\) is not an invariant A/B obstruction for the moving metric-only carrier. The correct first compatibility space already contains the metric correction \(D_jq_d\).

This does not construct a nonlinear joint branch. It removes one false linear obstruction.

## 4. Why #264 selected exactly L4 orbits 0 and 4

The flat forward-coframe metric tangent is built from the forward difference

\[
a_r=z_r-1,
\]

whereas the exact null line is built from the backward/state difference

\[
d_r=z_r^{-1}-1=-z_r^{-1}a_r.
\]

The forward-coframe metric image contains the rank-one line \(a\,a^T\). The null line \(d\,d^T\) belongs to that metric image exactly when \(d\parallel a\).

On the nine owned singular L=4 orbit types, the certificate finds exact alignment only on

\[
(0,0,1,1),\qquad (1,1,1,1),
\]

namely orbit 0 and orbit 4. These are exactly the two orbit types for which #264 found that the affine/coframe joint-null intersection equals the full #262 metric-only real plane.

So the #264 pattern is no longer a census accident: it is the equality condition between forward and backward discrete derivatives.

No finite affine gauge symmetry is inferred. #264's finite non-gauge result remains intact.

## 5. Smooth limit: finite mismatch becomes asymptotically invisible

For a smooth character \(z_r=e^{ihk_r}\),

\[
a_r=ihk_r-\frac12h^2k_r^2+O(h^3),
\qquad
d_r=-ihk_r-\frac12h^2k_r^2+O(h^3).
\]

Therefore

\[
d_ad_b-a_aa_b
=
ih^3k_ak_b(k_a+k_b)+O(h^4).
\]

The forward and backward rank-one metric shadows agree through order \(h^2\); their mismatch is \(O(h^3)\), hence \(O(h)\) after an \(h^{-2}\) normalization.

This is a symbol-level statement only. It does not by itself prove the nonlinear decoupling target of #240.

## 6. The whole four-dimensional coframe image becomes asymptotically joint-null

The relation is stronger than the scalar line.

Using the literal #264 forward-coframe map \(G_{\rm cof}(z)\) and the physical polarized joint block

\[
\mathcal H_J(z)=
\begin{pmatrix}
0&C(z)^T\\
C(z)&A(z)
\end{pmatrix},
\]

put \(z_r=1+\tau k_r\). Exact symbolic valuation gives

\[
\boxed{
C^Tx_{\rm cof}=O(\tau^4),
\qquad
Cq_{\rm cof}+Ax_{\rm cof}=O(\tau^3).
}
\]

At finite L=4 the forward-coframe image is not a joint gauge image, exactly as #264 proved. Near the smooth character, however, the complete four-parameter coframe tangent enters the joint kernel asymptotically with extra powers of the character difference.

This is an emergent-Noether statement, not a finite gauge theorem.

## 7. Exact Schur reduction to the linearized Einstein symbol

At the trivial character the connection block is invertible:

\[
\boxed{\det A(1)=256}.
\]

The joint linear equations are

\[
C^Tx=0,
\qquad
Cq+Ax=0.
\]

Eliminating the connection gives the effective metric Euler operator

\[
E_Q^{\rm eff}(q)
=
-C^TA^{-1}C\,q.
\]

Along \(z_r=1+\varepsilon k_r\),

\[
C(z)=\varepsilon C_1(k)+O(\varepsilon^2),
\qquad
A(z)=A(1)+O(\varepsilon).
\]

Therefore the leading effective metric symbol is

\[
-S_2(k),
\qquad
S_2(k)=C_1(k)^TA(1)^{-1}C_1(k).
\]

The checker constructs the standard flat linearized Einstein tensor on the same symmetric covariant metric coordinates and the same Minkowski \(\eta\), raises the output indices, and applies the repository's ten-coordinate Euler convention (factor two on off-diagonal metric variations). It proves the exact polynomial identity

\[
\boxed{
S_2(k)=\frac12\,G^{(1)}_{\rm coord}(k).
}
\]

Hence

\[
\boxed{
E_{Q,\rm eff}^{(2)}
=
-\frac12\,G^{(1)}.
}
\]

No fitted coefficient and no extra action channel enter this identity.

The same certificate proves

\[
\operatorname{rank}S_2=6,
\qquad
\operatorname{rank}F_{\rm cof}^{(1)}=4,
\qquad
S_2F_{\rm cof}^{(1)}=0.
\]

Therefore, over the generic momentum field,

\[
\boxed{
\ker S_2=\operatorname{im}F_{\rm cof}^{(1)}.
}
\]

The full four-parameter infinitesimal coframe/diffeomorphism image is exactly the gauge kernel of the leading metric Schur symbol, even though the corresponding finite L4 image is not an exact gauge image.

This is the central synthesis:

\[
\text{finite joint star system}
\longrightarrow
\text{first-order Koszul cross block}
\longrightarrow
\text{Schur complement}
\longrightarrow
-\frac12\,G^{(1)}
\]

with the four-dimensional diffeomorphism kernel emerging at the same leading order.

## 8. Relation to #232, #240, #237 and the FUGU documents

### #232 / Y family

Keep it separate. The #232 family is a connection-side curved joint-vacuum modulus on flat \(Q=\eta\), controlled by Hodge/pairing orthogonality and commuting connection data. The present theorem concerns the metric-to-connection cross symbol and its Schur reduction. They are two different carriers and two different mechanisms.

The useful common statement is narrower: neither hidden sector may be promoted to an IR observable merely because it is nonzero in UV coordinates. The registered response map decides.

### #240 response-decoupling

The FUGU fixed-vector detune is not a valid counterexample to decoupling. After canonical kernel transport its first derivative is exact in the metric image.

The remaining #240 pressure is now cleaner: test the actual #232 connection microstructure, slow spatial variation, and nonlinear joint compatibility against the Schur/Einstein IR readout. A nonzero counterexample must survive this carrier transport and the full joint equations.

### #237 compactness

The metric cross block has rank nine for every nontrivial character but collapses at \(d=0\). Its loss of coercivity near the trivial character is therefore derivative-like and organized, not an arbitrary resonance. A compactness theorem should use the induced derivative/Koszul norm or quotient, not demand an L-independent raw singular-value gap.

This does not solve the connection-side resonance geometry of #237.

### FUGU forward synthesis v1-v4

The useful FUGU discoveries survive as scouts:

- the nine-orbit real carrier census;
- universal one-complex/two-real metric-only dimension;
- the finite affine distinction between orbit types;
- the fact that fixed metric vectors become visible under character detuning.

The following promotions are retired by the exact owner:

- fixed-vector detune \(\neq\) physical quotient obstruction;
- the v3/v4 A/B table is not an invariant classification of the moving metric-null bundle;
- \(F_4=A+iCC^T\) remains an auxiliary transpose-pairing object and is not needed to obtain the Einstein Schur symbol;
- no even-sector selector is required to explain the universal metric-only line.

## 9. What this means for the Einstein programme

The old target "prove local uniqueness of the joint critical point" is not needed for the linear IR operator.

At the smooth flat symbol the finite theory already supplies:

1. an invertible connection block \(A(1)\);
2. a first-order metric/connection Koszul map \(C_1(k)\);
3. Schur elimination;
4. the exact second-order metric operator \(-\tfrac12G^{(1)}\);
5. its exact four-dimensional diffeomorphism kernel.

The next nontrivial bridge is therefore not another L4 census and not a new selector. It is to lift this flat linear Schur identity to a slowly varying nondegenerate solder and control the remainder uniformly enough for #240/#237.

A successful lift would turn the existing designated-sheet normal-jet result into a structural consequence of the finite joint complex rather than a separate coefficient match.

## Firewall

This memo does **not** claim:

- a nonlinear continuum Einstein theorem;
- full finite diffeomorphism gauge symmetry;
- compactness of arbitrary critical sequences;
- decoupling of the #232 curved connection microstructure;
- equality with \(E_\eta/E_{sp}\);
- an observational anomaly or perihelion prediction.

The exact result is a finite symbol theorem plus its flat smooth Schur limit.

## Certificate

\`python 02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py\`

Expected terminal:

\`J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT\`
