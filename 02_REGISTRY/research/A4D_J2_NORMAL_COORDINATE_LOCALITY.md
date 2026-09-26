# A4D J² normal-coordinate locality

**Task:** `WRK-A4D-J2-NORMAL-COORDINATE-LOCALITY`  
**Class:** `WORKER`  
**Research lane:** `EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE`  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Inputs read:** merged #201 (`MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md`, `certificates/a4d_star_qr_einstein_detector_check.py`); E-NJET (`ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`); the nonlinear bridge on main (`MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md`). The open parent memo is context for the UV boundary and is not an input theorem.  
**Certificate:** `02_REGISTRY/research/certificates/a4d_j2_normal_coordinate_locality_check.py`

## 0. Terminals

\[
\boxed{\texttt{J2-NONLINEAR-DEGREE-LE2-VANISHES-IN-NORMAL-COORDINATES}}
\]

\[
\boxed{\texttt{J2-IR-POSTQUADRATIC-REMAINDER-O-H}}
\]

The first terminal is the combinatorial vanishing theorem under the hypotheses in §1. The second is the fixed-realization majorant proved in §4. Neither one is an Einstein field equation.

## 1. Hypotheses

These are inputs. This worker does not prove them.

**H-VOL.** The eliminated metric response admits a translation-invariant analytic Volterra expansion about the constant-metric flat branch,

\[
\mathcal R_h[q]
=
\sum_{m\ge 1}
\mathcal R_h^{(m)}[q,\ldots,q],
\]

with analytic symbols \(T_m(\theta_1,\ldots,\theta_m)\). Analytic connection elimination itself stays in the parent lane.

**H-FLAT.** The exact constant-metric flat branch forces

\[
T_m(0,\ldots,0)=0\qquad\text{for every }m\ge 1.
\]

**H-201.** Merged #201 owns the ten small-momentum quadratic coefficient matrices of the naked star: after Schur elimination of the 24 Lorentz-link variables and conversion of the remaining 16 coframe perturbations to the ten symmetric metric perturbations,

\[
K_{\mathrm{star,metric}}(k)=\tfrac14 K_{E_\eta}(k)
\]

over \(\mathbb Q\), on all ten \(k_a k_b\) matrices, with \(c_\eta=1/4\) and \(c_{\mathrm{sp}}=0\). In Volterra notation this recorded linear input is

\[
\boxed{T_1^{[2]}=\tfrac14 E_\eta}.
\]

#201 does not own the symbol at a general lattice momentum. The ten matrices are the quadratic small-momentum Taylor data.

**H-NJET.** E-NJET records the quadratic-form identity \(E_\eta=-2G\) at a normal-coordinate center, in its stated Ricci convention. Reversing that convention reverses the sign. The finite centered-difference estimator in the same memo is a separate statement, \(-2G+O(\varepsilon_N^2)\).

**H-CUBIC.** After the Taylor polynomial of total momentum degree at most 2 is subtracted, the infrared remainder symbol satisfies

\[
|R(\theta)|\le C|\theta|^3
\]

uniformly, for some finite \(C\) independent of the lattice site. Here \(|\cdot|\) is any norm on the momentum space.

**H-FIXED.** The realization \(q\) is fixed and smooth, with finite third Fourier moment

\[
M_3(q)=\sum_n |n|^3|\widehat q_n|<\infty
\]

independent of the mesh \(h>0\). The cutoff radius is not a function of \(h\).

## 2. Conclusions

**C-CLASS.** Every local differential monomial produced by a momentum polynomial of total degree \(d\le 2\) has one of the following derivative-order types. Write \(k_1+\cdots+k_m=d\) for the derivative order on each of the \(m\) inputs. Tensor contractions and index permutations change coefficients, not these orders.

| Degree | Nonlinear order \(m\ge 2\) | Schematic form |
|---|---|---|
| 0 | one empty order tuple | constant, coefficient \(T_m(0,\ldots,0)\) |
| 1 | one factor of order 1, the rest 0 | \(q^{m-1}\partial q\) |
| 2 | one factor of order 2, the rest 0 | \(q^{m-1}\partial^2 q\) |
| 2 | two factors of order 1, the rest 0 | \(q^{m-2}(\partial q)(\partial q)\) |

For \(m=1\) the same list collapses to a constant, a single \(\partial q\), and a single \(\partial^2 q\).

**C-VANISH.** At a normal-coordinate center \(q(x)=0\) and \(\partial q(x)=0\),

\[
\boxed{
m\ge 2
\Longrightarrow
T_m^{[\le 2]}[q,\ldots,q](x)=0.
}
\]

Degree 0 is killed by H-FLAT, as a symbol coefficient, at every point. Degree 1 and both degree-2 shapes each contain a factor of order 0 or 1 whenever \(m\ge 2\), because a tuple with every entry at least 2 would have total degree at least \(2m\ge 4\). Each such factor is zero on the normal jet. The identity is independent of the star symbol and of which index carries the derivative.

The same center kills the linear degree-0 and degree-1 pieces. The only degree-at-most-2 contribution that can be nonzero there is \(T_1^{[2]}\), the second derivative of one factor.

**C-LINEAR.** By H-201 and H-NJET, and only under those inputs,

\[
\boxed{T_1^{[2]}(J)=-\tfrac12 G(J)}.
\]

The arithmetic is \(\tfrac14\cdot(-2)=-\tfrac12\). It does not absorb the E-NJET finite-stencil \(O(\varepsilon_N^2)\), and it does not close the parent UV theorem.

**C-REMAINDER.** Under H-CUBIC and \(h>0\),

\[
h^{-2}\sum_n |R(hn)|\,|\widehat q_n|
\le
C h\sum_n |n|^3|\widehat q_n|.
\]

H-FIXED makes the right-hand side a constant times \(h\), so

\[
\boxed{R_{\mathrm{IR}}(h)=O(h)}.
\]

A homogeneous remainder of degree \(d\ge 3\) normalizes by the same token to \(O(h^{d-2})\), which is \(O(h)\) for \(0<h\le 1\).

**C-TWO.** If two fixed smooth realizations obey H-VOL through H-FIXED, share one normal 2-jet \(J\), and obey one common ultraviolet hypothesis, then each leading infrared term equals \(-\tfrac12 G(J)\) and each infrared remainder is \(O(h)\). The ultraviolet comparison remains the parent theorem.

## 3. Proof of the classification and the vanishing

A translation-invariant monomial \(\theta_1^{\alpha_1}\cdots\theta_m^{\alpha_m}\) of total order \(d=|\alpha_1|+\cdots+|\alpha_m|\) acts as one derivative of order \(|\alpha_j|\) on the \(j\)-th factor. Summing orders therefore classifies the monomial up to the numerical coefficient of the contraction.

For \(d\le 2\) the nonnegative integer solutions are exactly the rows of C-CLASS. The certificate enumerates them for \(1\le m\le 8\) and checks the closed counts

\[
1,\qquad m,\qquad m+\binom{m}{2}.
\]

The last count is the \(m\) placements of a double derivative plus the \(\binom{m}{2}\) placements of two distinct first derivatives.

Evaluation at the center uses the jet

\[
(q,\partial q,\partial^2 q)\mapsto (0,0,1),
\]

where the third slot is a sentinel. It is nonzero so that a surviving second-derivative factor is visible. For every \(m\ge 2\) and every composition of degree 1 or 2, the product contains a 0. The linear composition \((2)\) multiplies only the sentinel, so it survives. The composition \((2,2)\) also multiplies only sentinels: total degree 4 is outside the theorem, and the cutoff is sharp.

Degree 0 is not deduced from \(q(x)=0\). Its coefficient is \(T_m(0,\ldots,0)\), which H-FLAT sets to 0 at every field value. A negative control in the certificate evaluates \(q^{m-1}\partial q\) on the jet \((1,1,1)\) and gets 1, so the degree-1 vanishing really uses \(\partial q(x)=0\).

Any contraction is a rational coefficient times one of these monomials. The certificate multiplies a nonzero rational by a vanishing jet product and gets 0. Permuting which factor carries a double derivative stays inside the single schematic class \(q^{m-1}\partial^2 q\).

## 4. Proof of the remainder bound

Let \(h>0\). Absolute homogeneity gives \(|hn|=h|n|\), hence \(|hn|^3=h^3|n|^3\). H-CUBIC then yields

\[
h^{-2}|R(hn)|
\le
h^{-2}C h^3|n|^3
=
C h\,|n|^3.
\]

Summing against \(|\widehat q_n|\) is the displayed inequality. H-FIXED factors \(M_3(q)\) out of the mesh, and the quotient of the majorant by \(h\) is the \(h\)-independent constant \(C M_3(q)\).

The certificate checks the identity on a fixed positive rational spectrum at four positive rational values of \(h\). It also checks \(h^{-2}h^d=h^{d-2}\) for \(3\le d\le 7\).

The same algebra shows why a shrinking realization is a different lemma. If the third moment is allowed to grow like \(h^{-2}\), the majorant is \(C/h\), which increases as \(h\) decreases. That family is excluded by H-FIXED. The certificate records the growth as a negative control.

## 5. Two-realization corollary

Let \(q\) and \(q'\) be fixed smooth realizations with the same value, first derivative, and second derivative at the center, and suppose both satisfy §1. C-VANISH removes every nonlinear degree-at-most-2 contribution at that point. C-LINEAR evaluates the remaining linear second-jet piece on that common 2-jet. C-REMAINDER bounds each infrared remainder by its own finite moment. Agreement of the leading infrared terms is the equality of those two copies of \(-\tfrac12 G(J)\). The parent lane still has to compare the ultraviolet pieces.

## 6. Regression note

- The realization is fixed. Its third Fourier moment does not depend on \(h\).
- The mesh does not enter through a shrinking cutoff radius.
- #201 is used only for the ten small-momentum quadratic coefficients \(K_{\mathrm{star,metric}}=\tfrac14 K_{E_\eta}\). The full lattice symbol is not attributed to #201.
- No ultraviolet resonance theorem, orbit classification, \(V_6\) calculation, global connection section, Holst term, or \(\varphi\) field is claimed.
- The conditional identity \(T_1^{[2]}(J)=-\tfrac12 G(J)\) is the product of H-201 and H-NJET. It is not a promoted Einstein equation, and the coefficients of #201 are not changed.

## 7. Still owned by the parent lane

`EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE` still owns:

- existence of the eliminated analytic Volterra expansion (H-VOL);
- the ultraviolet resonance theorem, including polarized orbit closure and smooth-sampling invisibility;
- any comparison of ultraviolet remainders between two realizations;
- a global connection section;
- promotion of \(-\tfrac12 G(J)\) from this conditional infrared evaluation to a field equation.

## 8. Pre-registered attacks

1. **Degree 1 without the first-derivative jet.** The monomial \(q^{m-1}\partial q\) is nonzero on a jet with \(\partial q\neq 0\). The certificate's away-from-center control returns 1. The theorem uses both \(q(x)=0\) and \(\partial q(x)=0\).
2. **The quadratic product \((\partial q)(\partial q)\) has no undifferentiated factor when \(m=2\).** It still contains a first derivative, so the normal jet kills it. The classification keeps this shape separate from \(q^{m-1}\partial^2 q\).
3. **A hidden \((\partial^2 q)(\partial^2 q)\) contraction at degree 2.** Two order-2 factors already have total degree 4. The sentinel evaluation of \((2,2)\) is nonzero, so the proof does not pretend that every nonlinear monomial vanishes.
4. **Reading #201 as a lattice multiplier.** H-201 quotes the ten \(k_a k_b\) matrices only. A general lattice value of the symbol would be a new theorem.
5. **Importing a shrinking bump into \(R_{\mathrm{IR}}(h)=O(h)\).** The negative control with third moment \(h^{-2}\) grows like \(1/h\). H-FIXED is load-bearing.
6. **Treating \(-\tfrac12 G\) as unconditional.** Dropping H-NJET leaves the coefficient at \(\tfrac14 E_\eta\). Dropping the parent ultraviolet theorem leaves the infrared evaluation unpromoted.

## 9. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_j2_normal_coordinate_locality_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```
