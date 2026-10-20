# D0 → GR: EXACT finite second-order Lorentz-star Palatini bootstrap beyond pp waves

19 October 2026. **EXACT SYMBOLIC QUADRATIC INTERACTION THEOREM / same Draft #334.** The original six based plaquettes, unmodified Lorentz-star contraction and ALL 16 independent coframe plus ALL 24 independent proper-Lorentz left-link first variations are used. On a family with TWO independent null amplitudes a,b, an original-action, rational, universal *finite-mesh* mixed Cartan correction eliminates every link Euler coefficient of a*b, while the remaining complete 16 coframe source is precisely the Einstein-type scalar overlap. For orthogonal transverse affine gradients the ENTIRE original all40 source has zero coefficient a*b despite nonzero mixed Weyl plaquette curvature. This is a genuine NONCOMMUTATIVE finite second-order GR bootstrap, NOT an all-order finite root, nonflat global exact vacuum, native physical controller/Cost–Info selection, or fixed-g/independent-tau raw #216 result. GR_closed=false.

**Owned inputs:** [original arbitrary-Brinkmann exact all40](A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md); [continuum two-null Cartan and local crossing invariants](A4D_DOUBLE_NULL_CARTAN_CROSSING_RICCI_WEYL_SPLIT_2026_10_19.md); [native source and exact readout boundary](A4D_OPPOSITE_NULL_LIE_COMPLETE_JULIA_ORDER_MEMORY_BOOK_SOURCE_2026_10_19.md); [same PR strategic route](A4D_STRATEGIC_SYNTHESIS_FOUNDATIONS_TO_GR_2026_10_17.md). The finite action and event gates are not replaced.

## 1. Exact original finite variables, two independent amplitudes

Use the SAME original orientation and null \(\eta_{+-}=\eta_{-+}=1,\eta_{22}=\eta_{33}=-1\), coframe entries \(v_{z,r}^a=h\,e_r^a(z)\), the same six based plaquettes
\(P_{rs}(z)=U_r(z)U_s(z+\hat r)U_r(z+\hat s)^{-1}U_s(z)^{-1}\), odd curvature \(\mathcal R(P)=(P-P^{-1})/2\), and the same fixed original star pairing. **Vary** all16 independent coframe components and all24 left proper-Lorentz link components at every interior site BEFORE substituting the specified connection or treating \(a,b\) as field variables.

For constant real transverse vectors \(A=(A_x,A_y)\), \(B=(B_x,B_y)\), put
\[
H=a(A_xx+A_yy),\quad J=b(B_xx+B_yy),\quad
e^+=du+\tfrac J2dv,\quad e^-=dv+\tfrac H2du,\quad e^2=dx,e^3=dy .\tag{1}
\]
The formal parameters \(a,b\) index a two-variable source Taylor germ. The certificate computes exactly in \(\mathbb Q[a,b]/(a^2,b^2)\), so it extracts precisely the joint coefficient \([ab]\) without numerical amplitudes, neglecting neither based face nor independent variation. Pure a or pure b sectors are the already owned exact flat affine pp roots.

Let \(\omega^{LC}\) be the exact CONTINUUM torsion-free connection of (1), in the prior two-null note. It is a TRIAL finite link at this point, NOT the answer to the independent finite Palatini equations:
\[
U^{LC}_{z,r}=\exp[h\,\omega_r^{LC}(z)] .\tag{2}
\]
Write \(N_i=E_{-,i}+E_{i,+}\), \(\bar N_i=E_{+,i}+E_{i,-}\),
\(R_\perp=E_{23}-E_{32}\), \(\mathsf B=E_{--}-E_{++}\), and
\[
d_x=A_xB_x,\quad d_y=A_yB_y,\quad
d=d_x+d_y,\quad w=A_xB_y-A_yB_x.\tag{3}
\]
The original proper-Lorentz independent variation convention is
\(\delta U=X_{ij}U,\ X_{ij}=(E_{ij}-E_{ji})\eta\);
hence **\(X_{23}=-R_\perp\)**. All source signs below are in this actual \(X\)-basis.

## 2. First load-bearing theorem: the flat 24×24 Cartan block is EXACTLY invertible

At \(e^a=h\,dx^a,\ U_r=I\), restrict the connection-input to 24 homogeneous Lie-coefficients \(\omega_{r,ij}\) with \(U_r=\exp(h\omega_r)\). The original six-based action's quadratic \(\omega\)-part is the rational bilinear form
\[
\mathcal Q(\omega)
=\sum_{r<s}\epsilon_{rsuv}\,
G_2(I_u\wedge I_v,\star\,\mathfrak b([\omega_r,\omega_s])) .\tag{4}
\]
Its 24×24 symmetric Hessian \(M\), in the 24 *original* generators \(X_{ij}\), has
\[
\boxed{\operatorname{rk}M=24,\quad\det M=256,\quad
\operatorname{spec} M=\{2^{[4]},(-2)^{[4]},1^{[8]},(-1)^{[8]}\}.}\tag{5}
\]
For the original left-link Euler differentiated with respect to the homogeneous \(\omega\) correction, \(D_\omega E_{\mathrm{link}}|_0=h^3M\). Thus \(\det D_\omega E=h^{72}256\ne0\) for each fixed \(h>0\). The pure homogeneous-link Jacobian is NONDEGENERATE and an analytic implicit function theorem supplies a unique small homogeneous correction solving the 24 link equations **at any one fixed selected interior site**, for sufficiently small fixed amplitude inputs. This last exact local existence statement does NOT assert one constant correction solves all sites at finite nonzero a,b: neighboring site equations may differ at cubic order and higher.

## 3. The entire uncorrected MIXED finite connection source is four real rotation rows

The EXACT coefficient \([ab]\) of the original 24 unrestricted link Euler for the continuum-LC trial (2), at **arbitrary symbolic transverse lattice node \(x,y\)**, has 20 zeros; its only nonzero rows are
\[
\boxed{\begin{aligned}
[ab]E_{U_u,X_{23}}&=-\frac{h^4}{4}\,w,\\
[ab]E_{U_v,X_{23}}&=+\frac{h^4}{4}\,w,\\
[ab]E_{U_x,X_{23}}&=+\frac{h^4}{4}\,d_y,\\
[ab]E_{U_y,X_{23}}&=-\frac{h^4}{4}\,d_x.
\end{aligned}}\tag{6}
\]
They are genuine original independent-Lorentz Cartan rows, not torsion-free equations imposed externally. All 24 coefficients are tensorially bilinear in the two transverse gradient vectors, so verifying the four ordered basis pairs \((e_i,e_j)\), with symbolic x,y and exact rational coefficients, establishes (6) for arbitrary A,B.

## 4. Universal forced discrete correction, no new gauge group/price

Solving \(\Delta\omega=-h M^{-1}r\) with (5)–(6), the UNIQUE mixed correction in this 24-dimensional homogeneous local chart is
\[
\boxed{
\begin{aligned}
\delta\omega_u&=\frac{ab\,h}{8}
   \big[d_x\bar N_2+d_y\bar N_3+wR_\perp\big],\\
\delta\omega_v&=\frac{ab\,h}{8}
   \big[d_x N_2+d_yN_3-wR_\perp\big],\\
\delta\omega_x&=\frac{ab\,h}{8}
   \big[w(\bar N_3-N_3)-d_yR_\perp\big],\\
\delta\omega_y&=\frac{ab\,h}{8}
   \big[w(N_2-\bar N_2)+d_xR_\perp\big].
\end{aligned}}\tag{7}
\]
Take the ORIGINAL proper-Lorentz links, not an added action,
\[
\boxed{U_r(z)=\exp\bigl(h[\omega^{LC}_r(z)+\delta\omega_r]\bigr).}\tag{8}
\]
The correction is analytic and uses only original SO(1,3) link directions. Its coefficients \(1/8\) are fixed by the original based-face discretization and exact Cartan inverse, not fitted to Einstein, CAR or the Golden price.

**Exact first nonlinear Cartan closure:**
\[
\boxed{[ab]E_{U_r,X_{ij}}(z)=0\quad
\text{for every one of the 24 original independent rows at EVERY interior z.}}\tag{9}
\]
The statement is coefficientwise in a,b, not all-order stationarity at nonzero amplitudes. The exact symbolic test retains all six plaquettes, two adjacent based faces per link, the full odd derivative \(D\mathcal R[P][dP]=(dP+P^{-1}dP P^{-1})/2\), original Eta and all proper-Lorentz generators.

## 5. Second theorem: the same 16 coframe rows become the Einstein overlap

AFTER the full independent 24 Cartan rows are solved at mixed order, substitute (7)–(8) and compute all SIXTEEN genuine original coframe variations. Exactly,
\[
\boxed{
[ab]E_{v^2_x}(z)=[ab]E_{v^3_y}(z)
=-\frac{h^3}{4}(A\cdot B),\qquad
[ab]E_{v_r^a}(z)=0\ \text{otherwise}.}\tag{10}
\]
This is true for arbitrary symbolic site coordinates, every h>0 at the declared mixed coefficient, and arbitrary affine real A,B by bilinearity. In particular the Levi–Civita crossed metric at the intersection has
\(\operatorname{Ric}_{uv}=-ab(A\cdot B)/4,\ R=-ab(A\cdot B)/2\);
its Einstein tensor has \(G_{xx}=G_{yy}=-ab(A\cdot B)/4\), all other Einstein components zero at this order. Thus (10) is the original finite Palatini Einstein contraction with the correct \(h^3\) normalization; it is not a redefined scalar postulate.

**GENUINE QUADRATIC CURVED VACUUM:**
\[
\boxed{
A\cdot B=0,\ w\ne0
\quad\Longrightarrow\quad
[ab]E_{\mathrm{entire\ original}\ 16+24}=0,
\quad\text{but }[ab]\mathcal R(P)\ne0 .}\tag{11}
\]
At the crossing, e.g. \(H=ax,\ J=by\),
\[
[ab]P_{uv}=\frac{h^2w}{4}R_\perp,\qquad
[ab]P_{xy}=-\frac{h^2w}{4}\mathsf B. \tag{12}
\]
More generally \([ab]P_{uv}=h^2(d\mathsf B+w R_\perp)/4\).
The other transverse-tilted plaquettes are nonzero and preserve the full Weyl Riemann data. The constant connection repair (7) has zero discrete gradient, so it does NOT erase these \([ab]\) plaquette curvatures. In the smooth metric at the origin the Kretschmann coefficient is \(-3 a^2 b^2 w^2/4\) when d=0, providing a nonflat gauge-invariant curvature witness.

The word "vacuum" in (11) is *only* coefficientwise at the first mixed order: the complete untruncated finite Euler may contain \(a^2b,ab^2,a^2b^2,\dots\). The existing all-order original 40→3→1 pp theorem is a different, exact stratum.

## 6. Exact reproducible certificate + independent numerical check

**Symbolic source:** [check_mixed_cartan_exact.py](sources/d0_two_null_crossing_2026-10-19/check_mixed_cartan_exact.py).

The checker forms an exact four-component matrix algebra in \(\mathbb Q[a,b]/(a^2,b^2)\), with independent symbolic x,y, and:

1. derives the exact flat Hessian eigenvalue multiplicities/determinant (5);
2. computes every one of the 24 true based-face link Euler mixed coefficients, including all return faces, and confirms (6);
3. forms \(-M^{-1}r\) and proves the explicit connection (7) matches it;
4. re-evaluates all24 link rows after correction: zero exactly;
5. re-evaluates all16 independent coframe rows after correction and obtains (10) coefficientwise;
6. verifies the nonzero \(P_{uv},P_{xy}\) plaquettes; four ordered basis pairs prove the arbitrary real bilinear A,B statement.

**Independent original numerical source:** [check_finite_all40_two_null.mjs](sources/d0_two_null_crossing_2026-10-19/check_finite_all40_two_null.mjs), now also tests the analytic h/8 correction at h=1/8, A=(0.1,0), B=(0,0.1) and A=(0.1,0), B=(0.1,0):
- orthogonal link max: 6.10351556×10⁻⁷ → 1.91330889×10⁻⁹ (factor 319);
- parallel link max: 6.10351562×10⁻⁷ → 1.91732005×10⁻⁹ (factor 318);
- orthogonal coframe max remains 7.6532×10⁻⁹ (cubic/higher residual);
- parallel coframe max remains 4.8829×10⁻⁶ (Einstein overlap survives).

These numeric values independently support the exact cancellation of the bilinear source. They are NOT a claim of exact all-order finite roots or uniform h→0 control. The exact rational/symbolic statements have also been checked in a separate local SymPy execution; full repository CI, expensive previous-root/Lean suites and native all-history source were not re-run.

## 7. The precise consuming next problem

The quadratic order is now DONE for the entire original all40 *field* system in the perpendicular crossed affine sector. The next geometric problem is **cubic and higher mixed source**: using the same original action and link variables, solve
\[
D_\omega E_{\omega}(0)\,\delta\omega_{mn}
=-\bigl[E_\omega\bigr]_{a^m b^n}^{\mathrm{known}}
\qquad (m+n\ge3) \tag{13}
\]
without assuming a uniform-site inverse or a new action. The proved 24×24 homogeneous inverse resolves a ONE-SITE normal coefficient; cross-site/periodic compatibility and independent 16 coframe rows have to be checked separately. Any higher-order coframe correction must retain the nonzero w Weyl mode and original CAR/RIGHT/clock variations. One should next compute the cubic source and its exact range rather than repeat rank searches or pp-wave polynomial extensions.

**Native selection remains a DISTINCT mandatory same-programme obligation:** physical admission and price of the full active-L/LEFT, old RIGHT/reference, exterior/Julia order reference, CAR/matter, clock/controller/work and full Book H+J+R; then true joint source-normalized refinement, global Ward and the original raw #216. Neither this coefficientwise vacuum result nor the separate positive full16 Julia order detector makes that price physically compulsory. The established nine-null/Bianchi theorem is a conditional consumer, not a substitute for this missing native source. GR_closed=false.
