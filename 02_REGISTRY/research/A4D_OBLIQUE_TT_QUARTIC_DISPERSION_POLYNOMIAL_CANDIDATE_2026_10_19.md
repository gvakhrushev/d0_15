# D0 → GR: exact arbitrary-null quartic TT Taylor completion; finite-h dispersion and native action remain open

19 October 2026. **RESEARCH / EXACT RATIONAL IDENTITY THROUGH THE h^4 TT JET, WITH ORIGINAL-SOURCE REPLAY.** Same existing scientific integrator Draft #334. The earlier F1009/F65537 reconstruction is now superseded at quartic Taylor order by an exact corrector construction over the rational-function field \(\mathbb Q(u,x,y)\) on the real null cone, including both null-exponent branches and exceptional real charts. Original six-based proper-Lorentz star action, all 16+24 independent Euler, old Book/native actions and accepted owners remain unchanged. No GR promotion; GR_closed=false.

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
The directional correction inferred from the original Schur equations is
\[
\boxed{\gamma_{\rm cand}(k)=\mathscr D_4(k)/(48u),\qquad u\ne0.}\tag{5}
\]
The actual original finite all40 Schur/TT equations (1) give the **same gamma for both PLUS and CROSS** on each of 28 original reconstruction directions and 16 genuinely independent held-out rays. All 44 rays pass in BOTH exact fields F1009 and F65537, i.e. 88 ray tests, 176 checked polarization answers. No floating-rank tolerance or second physical detector/source enters this comparison. The later exact rational proof is recorded in §4.

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

**Historical logical firewall:** those finite samples alone did NOT prove that the arbitrary-k correction belonged to the 9-dimensional polynomial class. Section §4 closes that specific quartic Taylor-jet question by constructing exact rational correctors directly from the original Schur equations. It does not turn the displayed coefficient into an all-order lattice dispersion law.

## 3. Reproducibility and remaining gates

The [44-direction checker](sources/d0_two_null_crossing_2026-10-19/check_oblique_tt_quartic_polynomial.cjs) reads the ORIGINAL all40 source and checks two TT polarisations, 28 reconstruction rays, 16 unseen holdouts, quartic invariant rank9 and first-corrector freedom. Run in this directory with Node.js, optionally setting D0_SCHUR_PRIME=65537. It independently reported PASS_QUARTIC_CANDIDATE_44_NULL_RAYS_AND_CORRECTOR_INDEPENDENCE on BOTH moduli. The [parent direct momentum derivative](sources/d0_two_null_crossing_2026-10-19/check_oblique_tt_directional_dispersion.cjs) uses exact equation (2). These scripts do not rerun old Lean/refinement/native physical cost owners.

The arbitrary-null quartic Taylor identity is now proved in §4. The next geometric steps are to determine the actual finite-h characteristic pole/residue and a refinement-uniform estimate. The nonlinear finite-root and authentic full-native retained-history Book/Cost−Info selection remain separate open inputs. GR_closed=false.

## 4. Exact rational completion on both null-exponent branches

The new [symbolic checker](sources/d0_two_null_crossing_2026-10-19/check_oblique_tt_quartic_symbolic.py) rebuilds the original six-face \(L/B/C\) Taylor blocks through order three, forms the exact \(S_2,S_3,S_4\) Schur coefficients using the original \(\det L_0=256\) inverse, and substitutes \(v=Q/(2u)\). Before restricting to the cone, it verifies both exact momentum-derivative identities

\[
\partial_uS_2=-C_1(e_u)L_0^{-1}B_1(k)-C_1(k)L_0^{-1}B_1(e_u),\qquad
\partial_vS_2=-C_1(e_v)L_0^{-1}B_1(k)-C_1(k)L_0^{-1}B_1(e_v).
\]

For each of the two TT polarizations it constructs rational \(e_1,e_2\) over \(\mathbb Q(u,x,y)\) and exactly verifies

\[
S_2e_0=0,\qquad S_2e_1+S_3e_0=0,
\]
\[
S_2e_2+S_3e_1+S_4e_0+\gamma_v(\partial_vS_2)e_0=0,\quad
\gamma_v=\frac{\mathscr D_4}{48u},
\]
and, when \(v\ne0\),
\[
S_2e_2+S_3e_1+S_4e_0+\gamma_u(\partial_uS_2)e_0=0,\quad
\gamma_u=\frac{\mathscr D_4}{48v}.
\]
Here \(\mathscr D_4\) is the same numerator in (4), not a newly fitted source. Exact checks on the real exceptional strata \(y=0\) and \(x=y=0\) cover the denominators of the generic correctors: for every real null ray in the \(u\ne0\) chart, the \(v\)-branch works, and for \(v\ne0\) the \(u\)-branch works as well. On the null axis \(x=y=0\), only the \(v\)-branch is asserted. The checker reports rank \(4\) for \(S_2\) and for each augmented corrector system, with every residual identically zero in the corresponding rational-function field.

As a hostile source control, the symbolic \(L/B/C\) Taylor blocks and \(S_2,S_3,S_4\) are compared to the original JavaScript implementation at four independent null rays modulo \(1009\); both branch coefficients are compared there too. The [saved exact result](sources/d0_two_null_crossing_2026-10-19/oblique_tt_quartic_symbolic_result.json) and [SHA-pinned receipt](sources/d0_two_null_crossing_2026-10-19/oblique_tt_quartic_symbolic_receipt.json) bind the checker and both source owners. This exact calculation replaces the 44-ray polynomial-class hypothesis for the stated Taylor equations.

**Scope boundary:** this proves formal TT solvability through \(h^4\), not convergence of the Taylor series, an all-order finite-\(h\) pole or residue, a nonlinear periodic root, a refinement-uniform continuum limit, or selection of the same-run physical Book/Cost−Info action. The detector and complete-instrument sources in the linked CAR owners are information/readout candidates until their preparation, clock, work, and full history price are bound to the compulsory native execution. GR_closed=false.
