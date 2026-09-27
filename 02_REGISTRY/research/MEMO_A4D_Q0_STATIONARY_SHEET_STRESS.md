# A4D q0 stationary-sheet stress, two modes

**Task:** `EXP-A4D-Q0-STATIONARY-SHEET-STRESS`  
**Class:** `EXPENSIVE`  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Certificate:** `02_REGISTRY/research/certificates/a4d_q0_stationary_sheet_stress_check.py`  
**Terminal:** `A4D-Q0-TWO-MODE-OPTICAL-SHEET-JET`

Owners pinned as ancestors of this branch:

- #216 merge `5523d8f679c1ea02f9b73d757c81649740010d0a`, designated smooth sheet \(h^{-2}E_Q=-\tfrac12 G+O(h)\).
- #262 merge `969ed16fe1de8557e75fd2211c1eb011422a695f`, real conjugate-pair carrier.
- #270 merge `7103412403e672ce7416bbfcc63028988f543494`, \(C(d)\operatorname{vec}(dd^T)=0\) and \(A_0\), \(\det A_0=256\).
- Harmonic-lift terminal `A4D-Q0-HARMONIC-LIFT-SECOND-JET-EXACT` on current main. It owns the identity-link forcing \(F_2\) and explicitly leaves gate (13), \(A_w p_2=-F_2\) and \(T_2=B_w p_2\), to this execution.

PR #240 is open research at head `8b3c93af328d94f3bf43d27a843d4b767a0c4c95`. Its shear witness is used only as an integer vector. Its moment is not recomputed and is not evidence. The unpinned coefficient \(35/2\) in the reduced-action Ward synthesis is not used.

## 0. Terminal

\[
\boxed{\texttt{A4D-Q0-TWO-MODE-OPTICAL-SHEET-JET}}
\]

On the flat center, with the source held at vacuum, the real conjugate-pair path of \(q_0=dd^T\) splits by character.

- Mode B, \(z=(-1,1,-1,1)\). The identity connection is an exact joint vacuum for every real amplitude. The metric Euler is identically zero. Both Einstein symbols \(- \tfrac12 G(d)\) and \(- \tfrac12 G(\arg z)\) vanish.
- Mode A, \(z=(i,i,-i,-i)\). The identity connection kills the order-\(\varepsilon\) connection Euler and fails at order \(\varepsilon^2\). The failure lives at character \((-1,-1,-1,-1)\) and has a unique rational solution. That solution is silent in the metric Euler. Through order \(\varepsilon^2\), with remainder \(O(\varepsilon^3)\), the continued sheet has \(E_Q=0\). This agrees with \(-\tfrac12 G(d)=0\). It disagrees with \(-\tfrac12 G(\arg z)\). The complex amplitude of \(G\) itself is \((\pi^2,-2\pi^2,0,0,\pi^2,0,0,0,0,0)\), so
\[
-\tfrac12 G(q_0;\arg z)=(-\pi^2/2,\ \pi^2,\ 0,0,-\pi^2/2,\ 0,0,0,0,0).
\]

This is not a physical no-go and does not close PR #240.

## 1. Declared path

\[
d_r=z_r^{-1}-1,\qquad q_0(z)=d(z)d(z)^T,
\]

\[
Q_\varepsilon(x)=\eta+\varepsilon\bigl(q_0(z)\chi_z(x)+\overline{q_0(z)\chi_z(x)}\bigr).
\]

\(Q_{\rm sm}\) is the flat center \(\eta\) of the #216 normal chart, not a curved background. \(q_0(z)\) is the Fourier amplitude of one character, paired with its conjugate. It is not a sitewise smooth field \(q_0(z(x))\). The source is vacuum and is not retuned after the response is seen.

The ten coordinates are \((00,01,02,03,11,12,13,22,23,33)\). Off-diagonal Einstein outputs carry the factor \(2\) from the merged Schur-direct convention. The backward-difference momentum \(d\) and the plane-wave momentum \(\arg z\) are different covectors and are never substituted for each other.

| Mode | \(z\) | \(d\) | \(\eta(d,d)\) | support of \(q_0\) | \(d\parallel\arg z\) |
|---|---|---|---|---|---|
| A | \((i,i,-i,-i)\) | \((-1-i,-1-i,-1+i,-1+i)\) | \(4i\) | all ten slots | no |
| B | \((-1,1,-1,1)\) | \((-2,0,-2,0)\) | \(0\) | \(00,02,22\) only | yes |

Slot \(11\) of mode B is zero. \(C(d)q_0=0\) on both modes by specialization of the #270 identity. That identity is the order-\(\varepsilon\) connection equation at the identity links. It is not used as a proof that \(E_Q=0\).

## 2. Where the Gram stays Lorentzian

The brief amplitude on mode B is \(2\chi q_0\) with \(\chi=(-1)^{x_0+x_2}\). Every site has determinant \(-1\). The eigenvalues are \(-1,-1\) and

\[
8\chi\varepsilon\pm\sqrt{64\varepsilon^2+1}.
\]

The identity \(\sqrt{64\varepsilon^2+1}>|8\varepsilon|\) forces one positive and one negative root. The signature is \((1,3)\) for every real \(\varepsilon\).

On mode A the four lattice phases have determinants \(-1\), \(8\varepsilon-1\), \(-1\), \(-8\varepsilon-1\). The odd phases are nondegenerate for \(\varepsilon\neq\pm 1/8\), and their closed-form eigenvalues have signature \((1,3)\) precisely on \(|\varepsilon|<1/8\). The even phases have characteristic polynomial \((\lambda+1)f(\lambda)\) with

\[
f(\lambda)=\lambda^3+\lambda^2-(1+64\varepsilon^2)\lambda-1.
\]

For \(\varepsilon\neq 0\) the discriminant \(2048\varepsilon^2(512\varepsilon^4+26\varepsilon^2+1)\) is positive, and the sign pattern \(f(-1)>0\), \(f(0)<0\), \(f(1)<0\) places the three real roots in \((-\infty,-1)\), \((-1,0)\) and \((1,\infty)\). Together with the root \(-1\), the signature is \((1,3)\) for every real \(\varepsilon\). At \(\varepsilon=0\), \(f(\lambda)=(\lambda-1)(\lambda+1)^2\).

The open Lorentzian interval containing the flat center is therefore \(|\varepsilon|<1/8\) on mode A, and the whole real line on mode B.

## 3. Mode B: exact identity sheet

The frame correction \(H=\tfrac12 q_0\eta\) satisfies \(H\eta H^T=0\). On each site,

\[
\Theta=I+\varepsilon\chi H
\]

has Gram exactly equal to the brief path, with no higher power of \(\varepsilon\). At every identity link the curvature \((P-P^{-1})/2\) is the zero matrix, so every component of \(E_Q\) is the zero function of the legs. The connection Euler, the derivative of the same naked-star density in the six Lorentz generators, is the zero polynomial in \(\varepsilon\) at every link. Both Euler equations hold exactly, not merely at linear order.

A hostile control with the same character and polarization \(q_{11}=1\) has a nonzero order-\(\varepsilon\) connection Euler. The zero on \(q_0\) is not an empty formula.

The flat connection Hessian at this character has rank \(24\). The continuation through the identity sheet is unique at linear order: the connection correction is zero. The recorded #240 witness

\[
(0,0,0,0,0,1,\ 0,0,0,0,0,0,\ 0,0,-1,0,-1,1,\ 2,1,0,1,0,0),
\]

in generator order \(K_1,K_2,K_3,J_{12},J_{13},J_{23}\), is not in that kernel. Its image has seven nonzero integer slots, including \(32\) and \(-32\). Turning that vector on at any nonzero amplitude leaves the connection equation. This certificate does not recompute the shear-solder moment of the vector.

Linearized Einstein agrees with the discrete sheet: \(G(d)[q_0]=0\) and \(G(\arg z)[q_0]=0\), the second because \(d\) is real-parallel to \(\arg z\) and \(k\otimes k\) is a pure gauge polarization. A pure-gauge control at the mode-A momentum is zero, and a spacelike \(h_{12}\) control is not.

## 4. Mode A: jet through order \(\varepsilon^2\)

The real frame is carried through order \(\varepsilon^2\) by \(H=\tfrac12 h\eta\) and \(S=-\tfrac12(H\eta H^T)\eta\). The Gram error of that frame starts at order \(\varepsilon^3\).

With links held at the identity:

- order \(\varepsilon^0\) and order \(\varepsilon^1\) of the connection Euler vanish on the characters \(1,\chi,\chi^2,\chi^3\);
- order \(\varepsilon^2\) vanishes on \(1,\chi,\chi^3\) and not on \(\chi^2\);
- \(\chi^2\) is the real character \((-1,-1,-1,-1)\). The order-\(\varepsilon^2\) field depends only on the phase \(x_0+x_1-x_2-x_3\) and has period \(2\), so those four characters exhaust it.

The vacuum Hessian of the naked-star density at the trivial character is entrywise the owned \(A_0\). At \((-1,-1,-1,-1)\) the same Hessian has rank \(24\). The \(L=4\) Fourier sum of the obstruction is \(16\) times the \(L=2\) sum, checked both on the constant character and on one entry of \(\chi^2\). Because \(z^2=z^{-2}\), the two complex second harmonics occupy one real character. Their merged local amplitude is

\[
F_{2,\mathbb R}=F_2(z)+\overline{F_2(z)},\qquad
F_2(z)=-\frac{d^T\eta d}{4}C(d(z^2))\operatorname{vec}(dd^T).
\]

The \(L=2\) Hessian differentiates the summed action, so its image on \(p_2\) is \(16\) times that one-site amplitude. The unique rational solution of this gate is the same Lorentz element on every role,

\[
p_2=(0,-4,-4,4,4,0),
\]

modulated by \(\chi^2\). Thus \(H p_2\) cancels the order-\(\varepsilon^2\) connection Euler.

The metric Euler of this correction is zero in two independent contractions: \(C(-2,-2,-2,-2)^T p_2=0\), and the position-space metric partial of the linearized curvature against the identity legs is the zero 10-vector. Curvature of a link correction of size \(\varepsilon^2\) is \(O(\varepsilon^2)\). A leg correction of size \(\varepsilon\) multiplies it at order \(\varepsilon^3\). The connection self-energy of an \(O(\varepsilon^2)\) link correction starts at order \(\varepsilon^4\) in the curvature. Therefore both Euler equations of the corrected jet are \(O(\varepsilon^3)\).

The order-\(\varepsilon^3\) equation is not solved. No finite-\(\varepsilon\) existence statement is made on mode A. The Lorentzian interval \(|\varepsilon|<1/8\) is only the range in which the Gram path has signature \((1,3)\).

## 5. Comparison with \(-\tfrac12 G\)

The merged Schur identity is \(K_{\rm Schur}(k)=-\tfrac12 K_{G^{(1)}}(k)\) when the symbol momentum is the backward-difference covector. On \(q_0=dd^T\) that symbol vanishes for every \(d\), because \(G(d)[dd^T]=0\). The discrete sheet agrees: its metric Euler is exactly zero on mode B and \(O(\varepsilon^3)\) on the mode-A jet. Inside this chart the optical section does not source a metric Euler through the computed order.

The continuum tensor of the same trigonometric polynomial, evaluated at momentum \(\arg z\), is a different object. On mode B it vanishes. On mode A the complex amplitude is

\[
G^{\rm coord}(q_0;\arg z)=(\pi^2,-2\pi^2,0,0,\pi^2,0,0,0,0,0),
\]

and the conjugate momentum reproduces the same real vector. The brief field is twice the real part of \(q_0\chi\), so its linearized Einstein tensor is \(2\cos\phi\, G^{\rm coord}\). The designated comparison is half of that with the opposite sign,

\[
-\tfrac12 G^{\rm coord}(\text{brief field})
=
-\cos\phi\,(\pi^2,-2\pi^2,0,0,\pi^2,0,0,0,0,0).
\]

It is not identically zero. The discrete jet is zero at order \(\varepsilon\), so the two differ by this cosine wave.

That mismatch is not a joint-critical counterexample. The discrete Euler equations hold through the stated order with the vacuum source left fixed. The continuum operator at \(\arg z\) is not the discrete Euler, and #216 identifies \(-\tfrac12 G\) with the discrete response only in the slow limit where \(d\) and \(\arg z\) become proportional. They are not proportional on mode A.

## 6. Pre-registered attacks

1. **Reading \(Cq_0=0\) as \(E_Q=0\).** Rejected. \(E_Q\) is computed from the curvature of the links. It vanishes at identity links because every plaquette is \(I\), for an arbitrary leg. The mode-A correction is checked by a second contraction, \(C^T p_2\), and by the position-space metric partial.
2. **A wrong star in the Hessian.** An earlier contraction omitted \(G_2\star\) and still had determinant \(256\). The certificate now requires the period-1 Hessian to equal the owned \(A_0\) entrywise.
3. **Volume factor between \(L=4\) and \(L=2\).** The order-\(\varepsilon^2\) field is checked to have period \(2\). The constant-character Hessian scales by \(16\), and one \(\chi^2\) entry scales by \(16\). The right-hand side is divisible by \(16\).
4. **Back-reaction of \(p_2\) at order \(\varepsilon^2\).** Counted in §4. It starts at \(\varepsilon^3\) in the connection Euler and at \(\varepsilon^3\) in the metric Euler.
5. **Calling the \(\arg z\) mismatch a no-go.** Refused in §5. Both discrete Euler equations and the fixed vacuum source are satisfied through the computed order; the mismatched tensor is not the discrete equation.
6. **Using the shear witness as a flat continuation.** Its flat Hessian image is nonzero, so the branch it spans does not stay connection-stationary on this sheet. The optical mode-B sheet does.
7. **Calling the unhalved Einstein vector \(-\tfrac12 G\).** The tuple \((\pi^2,-2\pi^2,0,0,\pi^2,0,0,0,0,0)\) is \(G^{\rm coord}\). The designated half is \((-\pi^2/2,\pi^2,0,0,-\pi^2/2,0,0,0,0,0)\) on the complex amplitude, and \(-\cos\phi\) times the unhalved tuple on the brief field. The zero pattern is unchanged.

## 7. What remains

Gate (13) of the harmonic lift is solved on mode A: \(p_2\) cancels the collided real forcing and \(T_2=0\). The order-\(\varepsilon^3\) forcing on that corrected branch, which the harmonic lift assigns back to this execution, is not solved here. Mode B's optical sheet is exact and matches both Einstein symbols; it does not absorb the open shear branch. Neither statement closes the global response question owned by PR #240. The degree-6 gate for the quarter-wave sector is untouched.

## 8. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_q0_stationary_sheet_stress_check.py
```
