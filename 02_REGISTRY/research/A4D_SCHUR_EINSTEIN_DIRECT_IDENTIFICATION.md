# A4D Schur–Einstein direct identification

**Task:** \`WRK-A4D-SCHUR-EINSTEIN-DIRECT-IDENTIFICATION\`  
**Lifecycle:** IN_PROGRESS  
**Scope:** exact flat linear-symbol cross-check; no nonlinear continuum promotion.

## Result

The merged #270 owner proved the leading finite-star metric Schur weld through the already-owned operator \(E_\eta\),

\[
K_{\rm Schur}(k)
=
-C_1(k)^TA_0^{-1}C_1(k)
=
\frac14 K_{E_\eta}(k),
\]

and then used the owned relation \(E_\eta=-2G\).

This worker removes that intermediate identification from the check.

It independently reconstructs the standard flat linearized Einstein tensor from its index formula in Minkowski signature, converts it to the repository's ten symmetric metric coordinates, and proves the exact polynomial identity

\[
\boxed{
K_{\rm Schur}(k)
=
-\frac12 K_{G^{(1)}}(k)
}
\]

coefficient-by-coefficient.

The certificate is deliberately cut before #270 constructs \(E_\eta\). Therefore this is an independent hostile cross-check of the Einstein name and normalization, not a second owner of the metric-null complex.

## 1. Finite input

Consume the merged #270 exact owner only through the construction of

\[
A_0=H_{AA}(1),\qquad
C_1(k),
\qquad
K_{\rm Schur}(k)=-C_1(k)^TA_0^{-1}C_1(k).
\]

The trivial-character connection block remains regular:

\[
\boxed{\det A_0=256}.
\]

No \(E_\eta\), \(K_{E_\eta}\), or \(E_\eta=-2G\) object is available in the checker namespace at the comparison point.

## 2. Independent Einstein symbol

Let \(h_{\mu\nu}\) be a symmetric covariant metric perturbation and \(k_\mu\) a momentum covector. With

\[
k^\mu=\eta^{\mu\nu}k_\nu,\qquad
k^2=\eta^{\mu\nu}k_\mu k_\nu,\qquad
h=\eta^{\mu\nu}h_{\mu\nu},
\]

the checker constructs

\[
G^{(1)}_{\mu\nu}(h;k)
=
\frac12\Big(
k_\mu k^\rho h_{\nu\rho}
+k_\nu k^\rho h_{\mu\rho}
-k^2h_{\mu\nu}
-k_\mu k_\nu h
-\eta_{\mu\nu}(k^\rho k^\sigma h_{\rho\sigma}-k^2h)
\Big).
\]

It then raises the output indices,

\[
G^{(1)\mu\nu}
=
\eta^{\mu\rho}\eta^{\nu\sigma}G^{(1)}_{\rho\sigma},
\]

because the metric Euler covector pairs with the covariant symmetric coordinates \(q_{\mu\nu}\).

For the ten coordinates \((00,01,02,03,11,12,13,22,23,33)\), an off-diagonal variation changes both matrix entries. Therefore the Euler-coordinate output is

\[
G^{\rm coord}_{aa}=G^{aa},\qquad
G^{\rm coord}_{ab}=2G^{ab}\quad(a<b).
\]

Differentiating these ten outputs with respect to the ten symmetric input coordinates gives the direct \(10\times10\) polynomial matrix \(K_{G^{(1)}}(k)\).

## 3. Exact direct identity

The exact comparison is

\[
\boxed{
K_{\rm Schur}(k)+\frac12K_{G^{(1)}}(k)=0_{10\times10}.
}
\]

All 100 polynomial entries vanish identically.

Thus the coefficient \(-\tfrac12\) is not only inherited from the name \(E_\eta\). It is reproduced directly by eliminating the regular connection block of the finite joint star symbol and comparing with the standard tensor formula.

This is still a **linear flat-symbol theorem**. It does not prove nonlinear Einstein dynamics on variable solder backgrounds.

## 4. Hostile convention controls

Three nearby convention choices are checked and all fail the exact equality:

1. keep the Einstein output indices lowered instead of raising them;
2. omit the factor \(2\) on off-diagonal symmetric output coordinates;
3. reverse the Schur sign.

Therefore the match is not an artifact of an adjustable sign or coordinate normalization. The repository convention is fixed by a three-way hostile control.

## 5. Bianchi identity

The independently constructed tensor satisfies

\[
\boxed{
k_\mu G^{(1)\mu\nu}=0
\qquad
(\nu=0,1,2,3)
}
\]

as four exact polynomial identities for arbitrary symmetric \(h_{\mu\nu}\).

This supplies a direct Noether/Bianchi check on the same standard Einstein object used in the Schur comparison.

## 6. Generic gauge kernel

Let \(F_{\rm cof}^{(1)}(k)\) be the leading metric shadow of the four-parameter forward-coframe variation. In tensor form it is the usual vector-symmetrized direction

\[
h_{\mu\nu}
=
k_\mu\xi_\nu+k_\nu\xi_\mu
\]

after the repository's coframe-to-metric \(\eta\)-conversion.

The checker proves

\[
\operatorname{rank}F_{\rm cof}^{(1)}=4,
\qquad
K_{\rm Schur}F_{\rm cof}^{(1)}=0.
\]

It also proves, over the generic momentum field,

\[
\operatorname{rank}K_{\rm Schur}=6.
\]

Since the metric carrier has dimension ten,

\[
\dim\ker K_{\rm Schur}=4.
\]

Hence

\[
\boxed{
\ker K_{\rm Schur}
=
\operatorname{im}F_{\rm cof}^{(1)}
}
\]

generically.

This is precisely the linearized diffeomorphism kernel of the Einstein symbol. It does **not** turn the finite L4 coframe image into an exact UV gauge image; #264's finite non-gauge result remains unchanged.

## 7. Characteristic hostile controls

Exact rank checks give

\[
\begin{array}{c|c}
k & \operatorname{rank}K_{\rm Schur}
\\ \hline
(1,0,0,0) & 6\\
(0,1,0,0) & 6\\
(1,2,3,4) & 6\\
(1,1,0,0) & 4
\end{array}
\]

and the independently constructed \(K_{G^{(1)}}\) has the same ranks on every control.

The null covector therefore carries the expected two-dimensional characteristic excess beyond the four gauge directions. This is a symbol statement, not yet a propagation or graviton theorem.

## 8. Synthesis with #270, #264 and #240

The direct check makes the structural chain sharper:

\[
\boxed{
\text{finite joint star symbol}
\;\xrightarrow{\ \text{regular connection elimination}\ }\;
K_{\rm Schur}
\;=\;
-\frac12G^{(1)}
}
\]

with

\[
\boxed{
\ker_{\rm generic}K_{\rm Schur}
=
\text{four-dimensional leading coframe/diffeomorphism image}.
}
\]

So the Einstein IR seed no longer rests on two independent observations that merely agree:

- #201 / \(E_\eta=-2G\);
- #270 / Schur \(=\frac14E_\eta\).

The same result is now obtained by a direct standard-tensor comparison.

This does not close #240. The #232 \(Y\)-family is a connection-side curved microstructure, whereas this theorem is the smooth flat metric Schur symbol. The real remaining "Mercury" test is the first slow-background coefficient of the #232-type joint microstructure **after** connection/range correction and exact carrier transport, projected against this direct Schur/Einstein IR readout.

## Terminal

\`J2-SCHUR-DIRECT-LINEAR-EINSTEIN-IDENTIFICATION-EXACT\`

## Firewall

This memo does not claim:

- a nonlinear continuum Einstein theorem;
- finite exact diffeomorphism gauge symmetry;
- decoupling of the #232 microstructure;
- compactness of arbitrary critical sequences;
- a graviton propagation theorem;
- an observational anomaly.

It is an exact independent identification of the leading flat Schur symbol.

## Certificate

\`python3 02_REGISTRY/research/certificates/a4d_schur_einstein_direct_identification_check.py\`
