# A4D exact resonance divisor and rank strata

**Task:** `EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION`  
**Status:** `IN_PROGRESS / OPEN` (geometric codimension-one step is CANDIDATE; higher-codimension strata are not certified)  
**Primary certificate:** [`certificates/a4d_resonance_divisor_slice_check.py`](certificates/a4d_resonance_divisor_slice_check.py)  
**Candidate geometric certificate:** [`sources/a4d_resonance_divisor_geometric_component/check.py`](sources/a4d_resonance_divisor_geometric_component/check.py)  
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

Over `Q(i)`, the two distinct irreducible arithmetic divisor factors are `P_+` and `\overline{P_+}`. At the generic point of either arithmetic prime divisor, the corresponding 12-by-12 block has determinant valuation one, so its rank is 11 over that divisor's function field (Smith form over the local DVR); the other block is invertible there. Hence the full 24-by-24 matrix has generic rank 23 on each arithmetic codimension-one component. The Rabin test above is only an irreducibility proof over `Q(i)`. It does not by itself prove absolute irreducibility over `C`. That geometric step is the candidate in the next section. Neither statement classifies higher-codimension intersections.

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

## Candidate geometric components

**Status:** CANDIDATE. No skeptic pass has been run. This section does not close the task and does not use a finite character grid as a stratification.

**Claim.** On the carrier of the owned holomorphic connection Hessian `A(z)` for `z in (C*)^4`, the numerator `P_+` of `det A_+` is absolutely irreducible in `C[z_0,z_1,z_2,z_3]`, and so is its coefficient conjugate. These are the only two geometric irreducible components of the determinant divisor on the torus. The generic rank of `A` on each is 23 (nullity 1). The count law `nullity = 2 max(n_{+i}, n_{-i})` remains false.

**Owned pre-facts.** The phase-count counterexample is already owned, not recomputed as a new theorem. `02_REGISTRY/research/A4D_RESONANCE_DIVISOR_RANK_LAW.md` lines 11–17 say, verbatim:

> exact elimination over \(\mathbb Q(i)\) gives
> \[\operatorname{rank}A=22,\qquad \operatorname{nullity}A=2.\]
> Here \(n_{+i}=2\) and \(n_{-i}=0\), so the proposed rule
> \(\operatorname{nullity}=2\max(n_{+i},n_{-i})\) predicts 4. This is an
> exact counterexample on the full character torus.

The arithmetic factorization `P_+ \overline{P_+}` over `Q(i)`, with multiplicity one and generic arithmetic rank 23, is the earlier certificate in this memo. The new check recomputes the numerator by an independent matching expansion and requires it to equal that Bareiss ledger.

**Computation.** `A_+` has 48 nonzero entries. Its support has 2304 perfect matchings. The signed expansion is the Laurent polynomial `(z_0 z_1 z_2 z_3)^{-3} P_+`, with `P_+` of 671 terms in `Z[i][z]`, degree at most 6 in each variable, and not divisible by any `z_r`. After `z_0=u`, `z_1=u+y_1`, `z_2=u+y_2`, `z_3=u+y_3` (determinant 1), the coefficient of `u^{18}` is the constant `-1024`. The image `H(u,y)=P_+(u,u+y,u+1,u+4)` therefore still has `u`-degree 18. For `p in {1009,1021}`, both larger than `(2·18-1)·deg_y H` and both splitting `i`, the Ruppert system

`H(∂g/∂y - ∂h/∂u) + h ∂H/∂u - g ∂H/∂y = 0`,

with `deg g ≤ (17, deg_y H)` and `deg h ≤ (18, deg_y H - 1)`, has solution dimension 1, and `gcd(H, ∂H/∂u)=1` over `F_p`. Dimension 1 means there is no second solution over an algebraic closure: a factor of positive `u`-degree with nonzero `u`-derivative would give one, and matrix rank does not grow under field extension. A proper power is excluded by the gcd. So `H`, and then `P_+`, is absolutely irreducible. The same holds for the coefficient conjugate. The witnesses `512` and `-512 i` have conjugation ratios `+1` and `-1`, so the two polynomials are nonassociate. On `(C*)^4` the denominator `(z_0 z_1 z_2 z_3)^6` is a unit, and `det A = P_+ \overline{P_+} / (4096^2 (z_0 z_1 z_2 z_3)^6)`. The zero set therefore has exactly these two geometric codimension-one components. Along the DVR at the generic point of `V(P_+)`, `det A_+` has valuation 1 and `det A_-` has valuation 0, so the generic rank is `11+12=23`.

**Negative controls.** The same Ruppert matrix returns dimension 2 for `u^2+y^2` over the inert prime `1031` (irreducible over `F_p`, reducible over the algebraic closure) and dimension 1 for `u^2+y^2-1`. The owned point `(1,1,1,1)` has rank 24. The owned point `(-1,-1,i,i)` has rank 22, lies on both components, and is the counterexample to predicted nullity 4. These controls can fail the claim: a blind solver that always returned dimension 1 would fail the sum-of-squares control, and a dropped `u`-degree would fail the leading-coefficient check.

**Pre-registered attack.** The strongest attack is to treat this codimension-one result as the full rank stratification, or to read the nullity-2 point `(-1,-1,i,i)` as the generic rank on `V(P_+)`. It is not. That point is an intersection point. A second attack is that a Gao dimension computed in small characteristic, or a specialization that kills a factor, was mistaken for absolute irreducibility. The certificate uses primes above the degree bound, a constant leading coefficient `-1024`, a square-free gcd, and a control that sees an absolutely reducible polynomial. A third attack is carrier drift onto `[A(z)|C(\bar z)]`, a phase-count replacement, a finite grid, or a diagonal germ. None of those is used.

**What this does not show.** It does not compute the nullity-`≥ 2` stratum. The missing stratum is the closed locus in `(C*)^4` where `nullity(A) ≥ 2`. That locus contains the conjugate intersection `V(P_+) ∩ V(\overline{P_+})`. Every irreducible component of the intersection that passes through `(-1,-1,i,i)` has generic nullity 2, because the intersection lies in `{nullity ≥ 2}` and `{nullity ≥ 3}` is Zariski-closed, but the ideal of the intersection is not computed and other components are not listed. Also missing is the Fitting locus inside `V(P_+)` where `rank(A_+) ≤ 10` while `\overline{P_+} ≠ 0`, and the symmetric locus on the conjugate component. No coefficient, no action, and no physical source is chosen. This is not a statement about the conjugated slot `[A(z)|C(\bar z)]`.

## Exact computation boundary

The rational Laurent factorization, the two arithmetic codimension-one ranks, and — as a candidate, by the certificate below — the two geometric codimension-one components with generic rank 23, are exact algebraic statements. The task stays open at the first missing stratum: the nullity-`≥ 2` locus, including the conjugate-intersection ideal and the chiral Fitting ideals of corank at least 2. No finite character sample, diagonal germ, or phase count is that stratum. The count law `nullity = 2 max(n_{+i}, n_{-i})` stays refuted, and `(-1,-1,i,i)` stays a counterexample rather than a generic point.

## Scope firewall

This is the holomorphic square symbol `A(z)`. The Hodge positivity/even-rank consequence is explicitly restricted to the physical unit torus and does not automatically transfer to the physical conjugated slot `[A(z)|C(bar z)]`. The memo makes no response, residue, stationary-sheet, continuum, or physical-carrier claim. The rejected phase-count law is recorded only as refuted by #314; no replacement count rule is proposed.

## Reproduction

The broader theoretical continuation is specified in [`A4D_THEORY_CLOSURE_HANDOFF.md`](A4D_THEORY_CLOSURE_HANDOFF.md). It connects the open resonance geometry to exact stationary existence, response uniformity, and the designated nonlinear Einstein limit; it does not change this task's algebraic terminal or certify those downstream steps.

```bash
python3 02_REGISTRY/research/certificates/a4d_resonance_divisor_slice_check.py
python3 02_REGISTRY/research/certificates/a4d_hodge_structural_review_check.py
python3 02_REGISTRY/research/certificates/a4d_sd_asd_reduction_check.py
python3 02_REGISTRY/research/sources/a4d_resonance_divisor_geometric_component/check.py
```
