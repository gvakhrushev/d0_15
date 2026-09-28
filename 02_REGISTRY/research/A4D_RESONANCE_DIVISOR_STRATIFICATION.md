# A4D exact resonance divisor and rank strata

**Task:** `EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION`  
**Status:** `IN_PROGRESS / OPEN`  
**Primary certificate:** [`certificates/a4d_resonance_divisor_slice_check.py`](certificates/a4d_resonance_divisor_slice_check.py)  
**Exact output:** [`certificates/a4d_resonance_divisor_slice_results.json`](certificates/a4d_resonance_divisor_slice_results.json)

## Current exact result

The symbol is the owned 24-by-24 holomorphic connection Hessian `A(Z)` rebuilt with the face orientation, generator order, and `exp4` second-jet convention of the merged #314 certificate. It has 96 nonzero entries. After exact cancellation each entry has at most four numerator monomials, total numerator degree at most two, and denominator in `{1, 2 z_0, 2 z_1, 2 z_2, 2 z_3}`. Every one of its sixteen 6-by-6 role-to-role blocks has generic rank four over `Q(z_0,z_1,z_2,z_3)`.

Two exact matrix identities constrain the global determinant. Swapping either adjacent pair of spatial characters `(z_1,z_2)` or `(z_2,z_3)` lifts to a determinant-one congruence of `A`; these generate the full spatial `S_3` symmetry. Simultaneous inversion of all four characters satisfies
`A(z_0^-1,z_1^-1,z_2^-1,z_3^-1) = A(z_0,z_1,z_2,z_3)^T`.
Thus `det A` is symmetric in the three spatial characters and invariant under simultaneous inversion. The exact congruence and transpose identities are checked at the matrix level in the certificate; they reduce the factorization problem but do not supply the factors.

A further exact Hodge change of basis splits `A` into conjugate 12-by-12 blocks over `Q(i)`: both cross-chiral blocks vanish identically, and the change-of-basis determinant is `4096`. Sparse fraction-free elimination gives

\[
\det A_+(z)=\frac{P_+(z)}{(z_0z_1z_2z_3)^3},\qquad
\det A_-(z)=\frac{\overline{P_+}(z)}{(z_0z_1z_2z_3)^3},
\]

where `P_+` is a degree-18, 671-term polynomial over `Q(i)` and the bar conjugates coefficients while leaving `z` fixed. Consequently the full determinant has the exact global norm representation

\[
\det A(z)=\frac{P_+(z)\,\overline{P_+}(z)}
{4096^2(z_0z_1z_2z_3)^6}.
\]

The sparse coefficient ledger is [`certificates/a4d_resonance_divisor_chiral_numerator.json`](certificates/a4d_resonance_divisor_chiral_numerator.json); each row stores the four exponents followed by the exact coefficient. The certificate recomputes every coefficient and compares the norm formula with fresh exact full-matrix determinants at the three rational-square control points already recorded below.

The same certificate proves `P_+` irreducible over `Q(i)`. Use the determinant-one coordinate change `z_0=u`, `z_1=u+y_1`, `z_2=u+y_2`, `z_3=u+y_3`; in these variables the coefficient of `u^18` is the nonzero scalar `-1024`. Specializing `(y_1,y_2,y_3)=(1,4,8)` and reducing modulo the prime ideal `(13,i-5)` gives the degree-18 polynomial whose descending coefficients are stored in the results JSON. The common coefficient denominator is coprime to 13, and the reduced leading coefficient is `3`, so this reduction is well-defined and preserves degree. The exact Rabin irreducibility test over `F_13` succeeds. A factorization over `Q(i)` would, by Gauss's lemma and the constant leading coefficient in `u`, reduce to a nontrivial factorization of this polynomial; its irreducibility rules that out. Two coefficients (`512` and `-512 i`) have different conjugation ratios, so `P_+` and `\overline{P_+}` are nonassociate. Their product is therefore irreducible over `Q` by the quadratic Galois action. Thus, up to a Laurent unit, the rational determinant has one irreducible factor `P_+\overline{P_+}`; over `Q(i)` it splits into those two distinct conjugate factors, each with multiplicity one.

Over `Q(i)`, the two distinct irreducible arithmetic divisor factors are `P_+` and `\overline{P_+}`. At the generic point of either arithmetic prime divisor, the corresponding 12-by-12 block has determinant valuation one, so its rank is 11 over that divisor's function field (Smith form over the local DVR); the other block is invertible there. Hence the full 24-by-24 matrix has generic rank 23 on each arithmetic codimension-one component. Irreducibility over `Q(i)` does **not** establish absolute irreducibility over `C`, so the number of geometric components after extending constants remains unproved. This is a generic component result, not a classification of higher-codimension intersections.

The exact #314 control point `(-1,-1,i,i)` lies on both conjugate components: the certificate evaluates both factors to zero there, and both 12-by-12 chiral blocks have rank 11, giving full rank 22. This is one certified intersection point, not the intersection ideal or its full rank stratification.

Exact univariate restrictions of the full determinant are:

| Character slice | Exact determinant | Status |
|---|---|---|
| `(x,1,1,1)` | `(3 x^4 - 22 x^2 + 3)^2 / x^4` | exact identity in `Q(x)` |
| `(x,x,1,1)` | `256` | exact identity in `Q(x)` |
| `(x,x^-1,1,1)` | `(x^4 - 2 x^3 - 2 x^2 - 2 x + 1)^4 / x^8` | exact identity in `Q(x)` |
| `(x,x,x,1)` | `(x^8 + 6 x^6 + 18 x^4 + 6 x^2 + 1)^2 / (4 x^8)` | exact identity in `Q(x)` |
| `(x,-1,1,1)` | `(x^6 - 3 x^5 - x^4 - 10 x^3 - x^2 - 3 x + 1)^2 / x^6` | exact identity in `Q(x)` |

On the two-variable spatial diagonal `Z=(y,x,x,x)`, the exact factorization is

\[
\det A(y,x,x,x)=\frac{f_{xy}^2 f_{yx}^2 H(x,y)^2}{64x^{10}y^6},
\quad f_{xy}=xy-x+y+1,\quad f_{yx}=xy+x-y+1,
\]
where
\[
\begin{aligned}
H(x,y)={}&3x^8y^2-x^6y^4+8x^6y^2-x^6+4x^5y^3-4x^5y-4x^4y^4\\
&+22x^4y^2-4x^4-4x^3y^3+4x^3y-x^2y^4+8x^2y^2-x^2+3y^2.
\end{aligned}
\]
This remains a restriction to a codimension-two locus; none of its three factors is thereby asserted to divide the unrestricted four-variable determinant.

The slice identities are checked by `a4d_resonance_divisor_slice_check.py`; the certificate also reproduces the full-rank control at `(1,1,1,1)` and the exact #314 counterexample rank 22 at `(-1,-1,i,i)` over `Q(i)`. The counterexample refutes the earlier count-only nullity formula. PR #315 independently owns the diagonal specialization

\[
\det A(x,x,x,x)=\frac{(x^2+1)^{12}}{16x^{12}}
\]

and local one-variable Smith exponents `(1,1,1,1,2,2,2,2)` at `x=i`.

Although every listed one-variable determinant restriction is a square or a
higher even power, the global Laurent determinant is **not** a rational
Laurent unit times a square. At the square-character points `(4,9,16,25)` and
`(1,4,9,16)`, exact determinants are respectively

\[
\frac{55489071565690103131701193700501}{19349176320000000000},\qquad
\frac{82681547376902231521}{1761205026816}.
\]

Their ratio is
\[
\frac{443912572525520825053609549604008}{7266932874923047692275390625},
\]
which is not a rational square. If `det A = c z^m P(z)^2` for a Laurent
unit `c z^m`, then at points with square coordinates the monomial is a square
and the ratio of any two nonzero determinant values must be a rational
square. This exact contradiction rejects a global-square shortcut; it does
not identify the irreducible factors or their multiplicities.

The repeated powers in these restrictions are suggestive but do **not** establish that the global four-variable determinant is a square, nor do the slice roots identify all irreducible components. The norm representation above is consistent with the exact nonsquare witness; block ranks and determinant multiplicities alone do not classify the matrix kernel on intersections.

## Hodge reduction: exact scope correction

The additional exact replays are [`certificates/a4d_hodge_structural_review_check.py`](certificates/a4d_hodge_structural_review_check.py) and [`certificates/a4d_sd_asd_reduction_check.py`](certificates/a4d_sd_asd_reduction_check.py), with pinned sparse input [`certificates/A_and_mixed_symbol_entries.json`](certificates/A_and_mixed_symbol_entries.json) and outputs [`certificates/a4d_hodge_structural_review_results.json`](certificates/a4d_hodge_structural_review_results.json) and [`certificates/a4d_sd_asd_reduction_results.json`](certificates/a4d_sd_asd_reduction_results.json). The original owner slice checker compares all 96 Laurent entries against its independent reconstruction; the direct SD/ASD builder independently compares all 576 matrix entries to the same table.

For the constant block-diagonal Hodge map `Ω=diag(STAR,STAR,STAR,STAR)`, the replay verifies `Ω²=-I`, `Ωᵀ=-Ω`, and `AΩ+ΩA=0` as Laurent matrix identities. An explicit eigenbasis `T` (`det T=4096`) gives the similarity form `T⁻¹AT=[[0,M],[σ(M),0]]` and the congruence form `TᵀAT=diag(2σ(M),2M)`. These are different transformations, so their block layouts and determinant normalizations must not be conflated. For arbitrary complex characters the valid rank identity is `rank A=rank M+rank σ(M)`; global rank doubling is false.

The exact one-variable slice `Z=(u,1,-1,2)` gives `det M=f(u)/(128u³)` for the sextic recorded in the JSON result. Exact gcd checks show `f` is squarefree, coprime to its coefficient conjugate, and nonzero at zero. At any root `α` of `f`, the simple determinant zero forces `rank M(α)=11`, while coprimality forces `rank σ(M)(α)=12`; thus `rank A(α,1,-1,2)=23`. This is an algebraic complex-torus counterexample to the proposed universal even-rank/Hodge-doubling statement, not a physical character point.

On the physical torus `|z_r|=1`, coefficient conjugation together with exact reciprocal transpose identities `A(Z⁻¹)=A(Z)ᵀ` and `M(Z⁻¹)=M(Z)ᵀ` gives `σ(M)(Z)=M(Z)†`. Only there does the replay conclude `rank A=2 rank M` and `det A=|det M|²≥0`. Consequently physical resonances lie on both conjugate determinant zero sets at once. This narrows the physical rank problem to their intersection; it does not classify that intersection, prove absolute irreducibility, or address a response/stationary-metric theorem.

The sparse cleared entries `2(z₀z₁z₂z₃)M` have coefficients in `Z[i]`, not uniformly in `Z`. At the diagonal quarter-wave point the replay also records `rank M=8` and first-derivative kernel-to-cokernel rank 2; with the existing order-six determinant result, this is consistent with Smith exponents `(1,1,2,2)` for each chiral block, whose multiset union is the known exponent list for `A`.

An independent direct build from the finite star-action formula now matches all 576 entries of the pinned sparse `A` table. Its exact chiral diagonal determinant is
\[
\det M(i+w)=-\frac{w^6(w+2i)^6}{4(w+i)^6}.
\]
The polynomial `-1024 w^6(w+i)^6(w+2i)^6` is instead the determinant after multiplying each of the 12 rows by the common denominator `2(w+i)`, hence is `(2(w+i))^{12}\det M`; it is not `det M` itself.

This replay also embeds the exact complex rank-23 witness from the earlier review in the direct owner reconstruction. Therefore no universal complex even-rank theorem follows from the Hodge split: coefficient conjugation acts on coefficients while keeping `Z` fixed and does not preserve a zero at the same non-real character. The exact general formula remains `rank A=rank M+rank σ(M)`, with doubling only on the physical unit torus.

## Exact computation boundary

The global Laurent factorization over `Q` and generic rank on both arithmetic codimension-one components over `Q(i)` are now certified. The remaining open steps are the absolute geometric factor boundary and exact higher-codimension rank-drop locus: certify whether either arithmetic factor splits over `C`, then certify the ideals/strata where a chiral block drops below generic rank 11 or where the conjugate zero sets meet, and determine the resulting full-matrix ranks. The certificate uses sparse fraction-free Bareiss elimination for one 12-by-12 block and an exact finite-field irreducibility test; it does not rely on a heuristic symbolic `factor` result.

The task remains open for absolute geometric factorization and exact higher-codimension rank-drop ideals/strata and their ranks. The global rational Laurent factorization and generic arithmetic codimension-one ranks are exact algebraic results; no finite character scan substitutes for the remaining ideal-theoretic classification.

## Scope firewall

This is the holomorphic square symbol `A(z)`. The Hodge positivity/even-rank consequence is explicitly restricted to the physical unit torus and does not automatically transfer to the physical conjugated slot `[A(z)|C(bar z)]`. The memo makes no response, residue, stationary-sheet, continuum, or physical-carrier claim. The rejected phase-count law is recorded only as refuted by #314; no replacement count rule is proposed.

## Reproduction

The broader theoretical continuation is specified in [`A4D_THEORY_CLOSURE_HANDOFF.md`](A4D_THEORY_CLOSURE_HANDOFF.md). It connects the open resonance geometry to exact stationary existence, response uniformity, and the designated nonlinear Einstein limit; it does not change this task's algebraic terminal or certify those downstream steps.

```bash
python3 02_REGISTRY/research/certificates/a4d_resonance_divisor_slice_check.py
python3 02_REGISTRY/research/certificates/a4d_hodge_structural_review_check.py
python3 02_REGISTRY/research/certificates/a4d_sd_asd_reduction_check.py
```
