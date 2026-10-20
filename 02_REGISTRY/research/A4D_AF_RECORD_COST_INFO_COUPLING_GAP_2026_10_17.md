# AF-record price does not supply the Lorentz source (DRAFT candidate)

**Status:** DRAFT candidate. No `claims.csv` row edited. Pre-flight on `origin/main` `02_REGISTRY/claims.csv`: no row owns this AF probe-price coupling. `D0-HODGE-LINKS-001` stays OPEN. `D0-SPECTRAL-EINSTEIN-001` remains the graph Laplacian `G=2L`. Quotes below are from PR #334 head `f74b618c`, read-only; that PR is not edited.

## Claim

On the owned second-AF price, the boxed arrow

`D(Cost−Info)_native → c_AF D S_EH[g] + D S_matter[g,Ψ]`

does not hold. The price's partial derivatives on the lapse, on a constant shift, and on a matter amplitude are not the Einstein-Hilbert interior sources. This is scoped to Jacobian formulas (3) and (6) and to AF-memo formula (7). It is not a claim that no future primitive can couple them.

## Owned pre-facts

PR #334 `A4D_NATIVE_OPERATIONAL_GAIN_AND_MEMORY.md:14-16`:

> Consequently, IF native Info means this complete maximal gain, Cost-Info is S_vN(sigma)/log(phi), not D(sigma||mu)/log(phi). The prior coherent-AF package assumed Info=S_vN/log(phi); that different explicit contract remains unchanged.

PR #334 `A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md:19-22`:

> This construction does not yet select this spectral contract as physical Cost-Info, derive the geometric integration measure or admit the controlled operations as native primitives. It supplies an explicit mathematical candidate for those remaining tests, rather than defining a missing term by subtraction.

Same file `:241-250`:

> u_i=t² e_i+t4 d_i. These are exactly the even Jacobian observable coefficients of the cylinder owner. Gauss and Parseval give sum_i e_i=R[q]/2. Equations (2)–(4) therefore imply for this one complete price A_second(P,t)=B_n+(alpha t²/2) R[q]+Rem.

The sentence after that assignment, `:257-258`:

> This is not an assertion that physical Info has already selected that contract.

Same file `:285-304`:

> If a geometric integration law dVol_q is separately supplied, fixed t and the canonical preparation give S= B_n Vol(q)+(alpha t²/2) integral R[q] dVol_q + integral Rem dVol_q. ... the source contains (B_n/2) q^(mu nu) - (alpha t²/2) G^(mu nu) ... The blank volume coefficient cannot be silently removed.

PR #334 `A4D_GLOBAL_GOLDEN_AF_VOLUME_FREE_CURVATURE_2026_10_17.md:113`:

> Here B_n=6+x_n f_0(p²)+(1-x_n)f_1(p²), the single complete blank price ... It is mathematically incorrect to replace this ONE complete operator baseline by B_n times the number of addresses.

Same file `:169`:

> the physical field→AF-gate admission, independent matter and exact stationary roots remain distinct.

Same file `:183` and `:189` keep the geometry-controlled gate, the observer/coframe, matter, and the original Cost−Info selection open, and ask to differentiate the true cost on the lapse row and on a shift row.

## What was computed

The type-0 fine probabilities of the Jacobian owner give `f_0'(p²)=0.58484529751693897635` and probe coefficient `κ_AF a_∞=0.07631948564573339023`. Conditional coordinate moments at costs 8, 12, 16, 20, 24 match the AF memo's printed table. At the golden gate the relative entropy is `1.1018481227433831325` and `S/log φ` is `2.0784917647555653496`. The central-cost probe derivative `-6p^{10}` is `-0.048783712534700092486`. The polylog ratio at `z=2^{-20}` gives `β|Λ_eff|=6.0000007152561857364`.

Any differentiable function of the external probes alone has vanishing partials in the lapse `N`, the shift `ε`, and a matter amplitude `ψ`. The owned formulas do not define those probes as functions of `N`, `ε`, or `ψ`. The chain rule therefore gives zero. The nonzero number `0.0763…` is `∂A/∂u`, not `∂A/∂g`.

On `g=diag(-N²,1,a²,a² sin²θ)` the scalar curvature is `2/a²`. The raised Einstein contraction against `∂g/∂N` is `-2/(N a²)`. The angular integral of `R√−g` is `8π N`. On the same metric with `g_tx=ε`, the contraction against `∂g/∂ε` is `-2ε/(a²(N²+ε²))`, which is zero at `ε=0` and nonzero at `ε=1`. A separate density `ψ²/2` has derivative `ψ`.

Multiplying a positive blank price by `√−g` restores a nonzero lapse derivative. That is the Jacobian §6 law, not formula (7).

The equal-cost mixed-length operator identity was not recomputed as a matrix. The gap already appears on the owned fixed-family price.

## Verification

`check_af_cost_info_coupling.py`. Negative controls that can fail the conclusion: the lapse contraction is required to be nonzero; the shift contraction is required to be nonzero at `ε=1`; the matter derivative `ψ` is required to differ from 0; copying the Einstein contraction into the AF derivative is rejected; a cell-counted baseline is required to see the cell count, so a silent volume factor would not pass as the owned price.

## Named risks and pre-registered attacks

The strongest self-attack: the differentiated AF expression is the chain-rule skeleton `F(u)`, not a dense AF matrix, and the Einstein witness is an ordinary Lorentzian metric rather than an owned D0 carrier. That attack does not restore the coupling. Formula (7) is already a scalar function of the probes `u_w`. If a dense matrix reduced to a different function of the metric, that reduction is not in the owned formula. The Lorentzian witness is exactly the kind of `S_EH` named in the boxed arrow; a place where its interior source moves and the AF partial does not is a counterexample to equality.

Second attack: at `ε=0` the shift contraction vanishes, so the first sources agree at that point. Agreement at one point is not identity of the two functions of `ε`.

Third attack: setting `u_i=t² e_2(A_i)` makes curvature appear. That sentence is a `Let` in the Jacobian memo, and the following sentence says physical Info has not selected the contract. The curvature it produces belongs to the positive metric `q`. The same memo's integration law then multiplies `B_n` by volume. Neither step is the lapse-and-shift derivative of Cost−Info plus independent matter.

Fourth attack: the other information contract, Info `= S_vN/log φ`, might still make Cost−Info equal the relative entropy. The operational-gain paragraph does not say that. It identifies Cost−Info with `S_vN/log φ` under the maximal-gain reading, and it leaves the other contract unchanged. The two entropies computed here are not equal.

## What this does not show

It does not show that the golden equidistribution or the probe coefficient is wrong. It does not close reconstruction (20), synthesis (28), `D0-HODGE-LINKS-001`, or a global absence of every possible later gate. Reopening hook: one admitted operation whose Cost−Info arguments include the lapse and a shift, and whose interior derivatives equal the Einstein-Hilbert covector plus an independent matter covector, without choosing the coefficient and without defining the matter source as the Einstein tensor.
