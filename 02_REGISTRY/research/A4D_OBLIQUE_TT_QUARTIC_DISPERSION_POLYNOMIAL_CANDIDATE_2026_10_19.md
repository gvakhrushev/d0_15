# D0 → GR: quartic oblique-graviton dispersion polynomial — exact sampled source, universal identity OPEN

19 October 2026. **RESEARCH / EXACT F1009 AND F65537 FINITE-FIELD SAMPLES / UNIVERSAL FORMULA HYPOTHESIS-TO-CERTIFY.** Same existing scientific integrator Draft #334. Original six-based proper-Lorentz star action, all 16+24 independent Euler, old Book/native actions and all accepted owners remain unchanged. No GR promotion; GR_closed=false.

**Consumption:** [the original full40 generic rank-six Schur](A4D_FULL40_EXACT_FLAT_SCHUR_RANK_SIX_GAUGE_AND_CHARACTERISTIC_2026_10_19.md), [the already-owned full-ten Schur–Einstein direct polynomial theorem](A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION.md), and [the two-null quartic exact amplitude jet](A4D_DOUBLE_NULL_CUBIC_EINSTEIN_QUARTIC_AREA_WARD_2026_10_19.md). The previously known flat S2=Einstein identity is not claimed anew here.

## 1. Same-original-action typed dispersion quotient

At the original flat proper-Lorentz coframe+links:
\[
\mathcal H(z)=\begin{pmatrix}0&C(z)\\B(z)&L(z)\end{pmatrix},\qquad
S(z)=-C(z)L(z)^{-1}B(z).
\]
Both neighboring based faces per varied link, all six original plaquettes, the original null eta/star and all 40 independent variations are included. For an integer Lorentz-null momentum \(k=(u,v,x,y)\), \(2uv=x^2+y^2\), set \(z_\mu=(1+h)^{k_\mu}\). The exact coefficientwise finite Schur expansion is \(S=h^2S_2+h^3S_3+h^4S_4+\cdots\).

The ORIGINAL full-ten accepted owner proves \(S_2\) equals the tetrad output of the linearized Einstein operator, including its fixed normalization. On a null ray, rank S2=4, kernel dimension12 (ten gauge plus two TT). The actual independent proper-Lorentz link elimination fixes the two physical TT continuation equations, not a chosen continuum wave action:
\[
S_2 e_1=-S_3e_0,\qquad
S_2 e_2=-S_4e_0-S_3e_1-\gamma(\partial_vS_2)e_0.
\tag{1}
\]
Here \(\gamma\) is precisely the correction in the exponent \(k_v(h)=v+\gamma h^2+\cdots\), not a Newton/matter coefficient.

The derivative of the principal original-action Schur requires only the two already-owned first jet maps and the accepted flat Cartan inverse:
\[
\boxed{\partial_v S_2=
-C_1(e_v)M^{-1}B_1(k)-C_1(k)M^{-1}B_1(e_v),\quad M=L(1),\quad\det M=256.}
\tag{2}
\]
The numerical source checker was updated to use (2) instead of solving two extra complete 24x24 Schur series at shifted momentum. This is an algebraically identical speedup, not a change of action or input.

A possible false nonuniqueness was separately tested. At four independent positive/signed and diagonal null directions, the EXACT Fp sources satisfy
\[
\boxed{S_3(\ker S_2)\subseteq\operatorname{im} S_2,\quad
\rank S_2=4,\quad\dim\ker S_2=12.}\tag{3}
\]
Thus changing the first-order corrector \(e_1\) by any of the twelve null directions cannot change its following-order cokernel condition **on those tested rays**. This is not yet an all-k theorem.

## 2. ONE quartic direction polynomial recovered from the ORIGINAL Euler responses

With \(Q=x^2+y^2=2uv\), \(P=xy\), define the compact homogeneous quartic polynomial
\[
\boxed{\mathscr D_4(k)=
5Q^2+12PQ-4P^2
-6(u+v)(x+y)Q
+2(u^2+v^2)Q.}\tag{4}
\]
Then the proposed universal directional coefficient is
\[
\boxed{\gamma_{\rm cand}(k)=\mathscr D_4(k)/(48u),\qquad u\ne0.}\tag{5}
\]
The actual original finite all40 Schur/TT equations (1) give the **same gamma for both PLUS and CROSS** on each of 28 original reconstruction directions and 16 genuinely independent held-out rays. All 44 rays pass in BOTH exact fields F1009 and F65537, i.e. 88 ray tests, 176 checked polarization answers. No floating-rank tolerance or second physical detector/source enters this comparison.

Representative EXACT rational values inferred consistently from two exact finite fields and the proposed (5):

| null k=(u,v,x,y) | gamma |
| --- | ---: |
| (1,2,2,0) | -1/2 |
| (1,4,2,2) | -1 |
| (1,5,1,3) | -2 |
| (1,5,1,-3) | +28 |
| (1,5,-1,-3) | +58 |
| (2,1,2,0) | **-1/4** |
| (2,2,2,2) | 0 |
| (2,5,2,4) | -9/4 |

Previous experimental working notation \(+1/4\) for (2,1,2,0) was a SIGN ERROR; the correct actual source result is \(-1/4\), in all exact primes checked. No genuine finite lattice reflection symmetry has been proved; (4) explicitly changes under independent x or y sign flips at this UV order despite being symmetric under exchanging u,v and exchanging x,y in the numerator. Do NOT call this experimental parity violation without a physically selected lattice scale, real wave pole/residue or action binding. The \(h\to0\) principal symbol remains EXACTLY Einstein.

### Why this is a structured reconstruction, not an arbitrary fit

The degree-four polynomial space separately invariant under swapping u/v and x/y has dimension14. On the invariant null hypersurface \(2uv=x^2+y^2\), its degree-four quotient has dimension 14−5=**9**: multiply the invariant null quadratic by each of the five independent invariant degree-two polynomials. The 44-row, 14-column invariant evaluation matrix has exactly rank9 over both F1009 and F65537, and the actual measured \(-2u\gamma\) lies in its column space. Solving within this explicit **9-dimensional declared hypothesis class** gives one compact representative (4), unique on the null hypersurface up to adding a quartic multiple of the null relation.

**Crucial logical firewall:** the finite source evidence does NOT prove that the TRUE arbitrary-k gamma belongs to that 9-dimensional quartic-invariant polynomial class instead of being a rational homogeneous function with an extra denominator. The universal formula is therefore **HYPOTHESIS-TO-CERTIFY**, despite 44 independent exact finite samples and rigorous uniqueness conditional on the class.

## 3. Reproducibility and next single theorem

The [44-direction checker](sources/d0_two_null_crossing_2026-10-19/check_oblique_tt_quartic_polynomial.cjs) reads the ORIGINAL all40 source and checks two TT polarisations, 28 reconstruction rays, 16 unseen holdouts, quartic invariant rank9 and first-corrector freedom. Run in this directory with Node.js, optionally setting D0_SCHUR_PRIME=65537. It independently reported PASS_QUARTIC_CANDIDATE_44_NULL_RAYS_AND_CORRECTOR_INDEPENDENCE on BOTH moduli. The [parent direct momentum derivative](sources/d0_two_null_crossing_2026-10-19/check_oblique_tt_directional_dispersion.cjs) uses exact equation (2). These scripts do not rerun old Lean/refinement/native physical cost owners.

**Next decisive mathematical step:** prove, by symbolic rational cancellation for arbitrary \(k\) on \(2uv=Q\), the complete physical TT solvability of (1) after inserting (5), including the TWO independent transverse projections and actual denominator clearing. In exact symbolic terms the source
\[
\Pi_{\rm TT}^{\rm left}
 [S_4e_0+S_3e_1+\gamma_{\rm cand}\,\partial_vS_2e_0]
\]
must vanish as a polynomial/rational identity, modulo the null quadratic, with no fitted extra source. This is stronger than another ray test. Then establish the real complex-wave characteristic pole/residue and uniform h-refinement; the original nonlinear degree-four crossed-Weyl vacuum jet, all-order joint roots and authentic full-native retained-history Book/Cost−Info selection remain separate OPEN inputs. GR_closed=false.
