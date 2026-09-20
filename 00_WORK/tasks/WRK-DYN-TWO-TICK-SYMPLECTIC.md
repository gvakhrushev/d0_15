# WRK-DYN-TWO-TICK-SYMPLECTIC

## Class
WORKER

## Objective
Formalize the finite two-tick algebraic structure already implied by `ToralAutomorphism.T`: $T^2$ entries, one-tick anti-symplecticity, two-tick symplecticity, invariant Lorentzian form, invariant-form classification, and the exact two-tick recurrence/generating relations, without promoting Hodge coupling normalization or a physical branch interpretation.

## Scope
1. Define the symplectic form $J = \begin{pmatrix}0 & 1 \\ -1 & 0\end{pmatrix}$ and Lorentzian metric $G = \begin{pmatrix}-2 & 1 \\ 1 & 2\end{pmatrix}$ on the toral plane $\mathbb{Z}^2$.
2. Prove $T^T J T = -J$, $(T^2)^T J (T^2) = J$, $T^T G T = -G$, $(T^2)^T G (T^2) = G$, and $\det(G) = -5$.
3. Prove that no non-zero bilinear form is invariant under the one-tick map $T$ ($T^T B T = B \implies B = 0$).
4. Formally classify all two-tick invariant bilinear forms: $(T^2)^T B (T^2) = B \iff B = \begin{pmatrix}-a & a-c \\ c & a\end{pmatrix}$.
5. Formalize the two-tick discrete generating relations over $\mathbb{Q}$ derived from $S_1(q, q') = \frac{1}{2}q^2 - qq' + q'^2$, and the exact Euler-Lagrange recurrence $q_{k+1} = 3q_k - q_{k-1}$.
6. **Hard Firewall:** Do not formalize Hodge coupling $\alpha$, ellipticity bounds, physical $q/p$ branch assignment, continuous Hamiltonian, physical $\hbar$, or claim full gravity dynamics derivation.

## Affected Claims
- `D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001`
- `D0-STATIC-TO-DYNAMICS-OWNER-001`
- `D0-TIME-2D-PISOT-001`
- `D0-HODGE-LINKS-001`

## Exit Condition
Formalize the finite two-tick algebraic structure already implied by ToralAutomorphism.T: T² entries, one-tick anti-symplecticity, two-tick symplecticity, invariant Lorentzian form, invariant-form classification, and the exact two-tick recurrence/generating relations, without promoting Hodge coupling normalization or a physical branch interpretation.
