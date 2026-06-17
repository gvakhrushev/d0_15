# D0 Higgs scalar projector closure

**Status:** SCALAR-PROJECTOR-CERT-CLOSED
**Owner:** `D0.Matter.HiggsScalarProjectorConstructive`
**Cert:** `05_CERTS/vp_higgs_scalar_projector_constructive.py`

## 1. Scope

Close the Higgs/Yukawa scalar-projector operator boundary at the finite projector level. The construction does not claim empirical Higgs mass fitting or VEV values. Yukawa numerical comparison remains a transfer/passport layer.

## 2. Frozen scalar doublet subcarrier

Define the frozen scalar doublet subcarrier

\[
\mathcal H_\phi \cong \mathbb C^2
\]

with inclusion

\[
\iota_\phi : \mathbb C^2 \hookrightarrow \mathcal H_{\rm matter}.
\]

## 3. FrozenSU2 (X, Z) generators

On the doublet use the frozen generators

\[
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad
Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}.
\]

## 4. Commutant theorem

If \(P\) is a positive idempotent on the frozen scalar doublet block and commutes with both generators,

\[
[P, X] = 0, \qquad [P, Z] = 0,
\]

then \(P = a I_2\).

A general \(2\times 2\) matrix commuting with \(Z\) must be diagonal. A diagonal matrix commuting with \(X\) must have equal diagonal entries. Hence \(P = a I_2\).

## 5. Positive idempotent rank-2 closure

If additionally \(P^2 = P\) and \(P \ne 0\), then \(a \in \{0,1\}\) and the nonzero solution is \(P = I_2\), \(\operatorname{rank}(P) = 2\).

The certified scalar projector is therefore

\[
P_\phi = I_2, \qquad \operatorname{rank}(P_\phi) = 2.
\]

## 6. Multiplicity rule

If the full matter-transfer carrier contains multiple SU(2) doublet copies, the commutant is of the form \(I_2 \otimes A\). Rank-2 uniqueness therefore requires that the frozen scalar subcarrier \(\iota_\phi(\mathbb C^2)\) (or an explicit multiplicity selector) has been frozen first.

Book 05 rule: commutation with FrozenSU2_X/Z closes rank-2 uniqueness only after the scalar doublet subcarrier or multiplicity selector is frozen.

## 7. Yukawa section admissibility

The certified rank-2 projector \(P_\phi\) admits the Yukawa section

\[
Y : \mathcal H_R \to \mathcal H_L \otimes \mathcal H_\phi
\]

with the compatibility condition \((I_L \otimes P_\phi) Y = Y\) (equivalently the full block operator \(\mathcal Y\) is Hermitian). No second mass anchor is introduced; \(\Lambda_{\rm act}\) remains the sole dimensional action section.

## 8. Negative controls

- Rank-1 projectors (\(P_0, P_1, P_+\) etc.) break commutation with \(X\) or \(Z\).
- Rank >2 requires an explicit extra multiplicity selector.
- Direct use of a second mass anchor (e.g. measured \(v\) or \(m_H\)) for Yukawa admission is forbidden.

## 9. Cert tokens

See `05_CERTS/vp_higgs_scalar_projector_constructive.py` for the exact `PASS_*` and expected rejected-shortcut `FAIL_*` tokens (including `PASS_NONZERO_IDEMPOTENT_FORCES_IDENTITY_DOUBLET`, single-action preservation, etc.).

## 10. Book 04 patch

The open "Higgs/scalar projector boundary" (04.16) is replaced by the positive finite closure statement:

> D0 closes the scalar projector operator boundary by freezing a scalar doublet subcarrier \(\mathcal H_\phi \cong \mathbb C^2\). On this carrier the FrozenSU2-compatible generators \(X\) and \(Z\) have scalar commutant. A positive idempotent \(P\) supported on this doublet and commuting with both must be \(P = I_2\) or \(P = 0\). The nonzero Higgs/Yukawa scalar section therefore has the unique gauge-compatible projector \(P_\phi = I_2\), rank 2.

The Higgs scalar projector operator boundary is closed at the finite projector level. Yukawa numerical comparison remains a transfer/passport layer.
