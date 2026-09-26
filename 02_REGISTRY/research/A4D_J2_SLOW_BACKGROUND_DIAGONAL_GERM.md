# A4D diagonal slow-background germ

**Task:** `WRK-A4D-J2-SLOW-BACKGROUND-DIAGONAL-GERM`  
**Class:** `WORKER`  
**Research lane:** `EXP-A4D-J2-UNIFORM-COUPLED-NORMAL-RESCUE`  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Certificate:** `02_REGISTRY/research/certificates/a4d_j2_slow_background_diagonal_germ_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-DIAGONAL-SLOW-BACKGROUND-FLAT-SPLITTING-TERM-FOUND}}
\]

This is a hostile control on the owned diagonal quarter-wave. It is not a uniform rescue theorem and not an Einstein equation.

## 1. Declared slow background

The frozen object is the diagonal character \(z_A=z_B=z_C=z_D=i\). The slow parameter is the uniform phase detuning

\[
z_r(t)=i\,e^{it},\qquad r\in\{A,B,C,D\}.
\]

Each torus momentum of the diagonal quarter-wave is shifted by the same angle \(t\). The internal directions are the owned real kernel vectors \(\lambda_0\) and

\[
w=\lambda_2+\lambda_5-\lambda_7,
\]

with real amplitudes \((a,b)\) on \(\lambda_0\) and \((c,d)\) on \(w\), in the cosine/sine splitting recorded with the reduced quartic. No external UV metric source is turned on. A constant internal stretch of the second frame leg is computed only as a negative control: its first kernel derivative vanishes.

The \(0\)- and \(2k\)-range blocks are already inside the owned frozen quartic. At order \(t\) they do not correct the linear kernel term. A range response linear in the resonant amplitude is forced by \(\partial_t H\) and returns to the reduced Euler equation at order \(t^2\).

## 2. Owned frozen germ

The owned reduced potential on this four-dimensional subspace is \(V_4=48P\), with the rational quartic \(P(a,b,c,d)\) frozen by the diagonal certificate. At zero external source the Euler germ is the cubic

\[
\nabla V_4(a,b,c,d)=0.
\]

Its real zero set is exactly the union of the two lines

\[
(a,0,0,0)\qquad\text{and}\qquad(0,b,0,0).
\]

The origin is therefore not an isolated frozen zero. Both lines are genuine zeros of the cubic, and the certificate's Grevlex charts exclude every other real ray.

## 3. First exact correction

Differentiate the owned polarized connection symbol along \(z_r(t)\). On the frozen kernel the quadratic form vanishes at \(t=0\), and its \(t\)-derivative has cross coefficient

\[
\lambda_0^{\mathsf T}(\partial_t H)\,w=6.
\]

The diagonal self-terms of \(\lambda_0\) and of \(w\) remain zero. The Hessian convention of the symbol makes the quadratic action \(\tfrac12\zeta^{\mathsf T}H\zeta\), so the first potential correction is

\[
\boxed{6t(ac+bd)}.
\]

The corrected zero-source Euler germ, through this order, is

\[
\boxed{\nabla V_4(a,b,c,d)+6t(c,d,a,b)=0.}
\]

The linear map \((a,b,c,d)\mapsto(c,d,a,b)\) is invertible. Both frozen lines fail the corrected equation for every \(t\neq0\).

## 4. Square-root sheets

The cubic and the new linear term balance at amplitude \(\sqrt{|t|}\). Set \(t=\sigma s^2\) and \((a,b,c,d)=s(A,B,C,D)\). The leading equation is

\[
\nabla V_4(A,B,C,D)+6\sigma(C,D,A,B)=0.
\]

An Euler term of size \(t|u|^2\) becomes size \(s\) after this scaling, and every higher owned schematic term is \(O(s^2)\). Any such correction moves a nondegenerate leading root by \(O(s)\) and leaves an amplitude \(O(\sqrt{|t|})\).

For both signs the certificate gives a rational center and an infinity-norm Newton ball of radius \(10^{-5}\):

| Sign of \(t\) | Rational center \((A,B,C,D)\) |
|---|---|
| \(+\) | \(\bigl(\tfrac{1966487}{10^8},\tfrac{1992998}{10^8},\tfrac{4512801}{10^8},\tfrac{6075041}{10^8}\bigr)\) |
| \(-\) | \(\bigl(-\tfrac{10075542}{10^9},\tfrac{159833106}{10^9},-\tfrac{36426563}{10^9},\tfrac{237478068}{10^9}\bigr)\) |

Each ball is contracted into itself and stays away from the origin. Therefore both signs have a nonzero real leading root, and the corrected germ has flat-approaching sheets

\[
u(t)=O(\sqrt{|t|}),\qquad u(t)\neq0.
\]

The zero solution \(u=0\) remains a solution of the displayed leading equation. The new sheets are additional.

## 5. Comparison with the abstract model

The abstract control \(u^3-tu\) has an isolated frozen zero and, for one sign of \(t\), two nonzero sheets of size \(\sqrt{|t|}\). The diagonal germ differs in two exact ways, and agrees in the third:

- its frozen zero set is two lines, not an isolated origin;
- the first computed correction is the off-diagonal pairing \(6t(ac+bd)\), not a multiple of \(a^2+b^2+c^2+d^2\);
- that pairing is nondegenerate between \((\lambda_0,w)\), and both signs of \(t\) produce extra real sheets of size \(\sqrt{|t|}\).

So a real flat-splitting mechanism of \(u^3-tu\) type does occur on this orbit. It is not the same polynomial.

## 6. Boundary

The result uses one diagonal character and one uniform phase detuning. It does not enumerate the other polarized orbits, does not construct a global connection section, and does not promote \(-\tfrac12 G\). The constant-stretch control shows that not every background parameter splits the kernel at first order. The unknown \(t\)-derivative of the cubic range vertices is subleading on these sheets; its coefficient is not claimed.

## 7. Validation

```bash
python3 02_REGISTRY/research/certificates/a4d_j2_slow_background_diagonal_germ_check.py
python3 tools/validate_work.py
python3 tools/validate_repo.py
```
