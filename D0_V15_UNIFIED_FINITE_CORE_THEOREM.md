# D0-v15 Unified Finite-Core Theorem

$$
\boxed{\;K(9,11,13)\to\mathcal W\to(Q_9,Q_{11},Q_{13})\to(E_0,E_4,E_3)\to\mathcal H_{\rm term}\to U_E\to F_{\rm term}\to W_{\rm eff}(z)\to G_\ell^{\rm fb}(z,\lambda)\to\mathcal A_n\;}
$$

$$
G_\ell^{\rm fb}(z,\lambda)=\frac{Q_9}{1-z}+\frac{Q_{11}}{1+\lambda z^4}+\frac{1+\lambda z^3/\sqrt2}{1+\sqrt2\,\lambda z^3+\lambda^2 z^6}\,Q_{13}
$$

$$
F_{\rm term}=\tfrac12(P_\mu+P_\tau),\qquad
\det(I-zW_{\rm eff})=(1-z)\,\frac{(1+\lambda z^4)^2}{1-\lambda z^4/4}\,\frac{1+\sqrt2\,\lambda z^3+\lambda^2z^6}{1-\lambda z^3/(2\sqrt2)}
$$

$$
\mathcal A_{n+1}=\mathcal A_n+\mathcal A_{n-1},\qquad
\mathcal A_{n+1}-\varphi\,\mathcal A_n=\psi^{\,n}\mathcal A_1,\qquad |\psi|=\varphi^{-1}<1
$$

> **Status — CONDITIONAL-EXTENSION (one constructed admissible object).** This is a single explicit member
> of the edge-cover holonomy family (the v15 audit classified the physical edge cover `CONDITIONAL`,
> `D0-EDGE-COVER-FAMILY-001`): the holonomy `λ`, the balanced two-port feedback `R_*`, and the line-graph
> contact `K` are **chosen**, not forced by frozen `D₀`. Every identity below is nonetheless derived from raw
> source and verified exactly (SymPy + the real 359-edge graph). **No physical lepton masses, Standard-Model
> charges, redshift, or equation of state are claimed.** The poles are finite return/resonance geometry.

Every arrow is a concrete operator, inclusion, compression, polar isometry, Schur complement, or exact
determinant identity. Lean spine: `D0/UnifiedFiniteCore/` (+ `D0.Integration.V15.RawZone`). Certificates:
`05_CERTS/verify_unified_backbone.py`, `05_CERTS/verify_unified_feedback.py` (build all operators from
combinatorial source — no hard-coded matrices).

## 1. Raw `K(9,11,13)` Fourier quotient

`𝓗_V = ℂ^{V₉}⊕ℂ^{V₁₁}⊕ℂ^{V₁₃}`, adjacency `A`. Constant-part vectors `u_n = n^{-1/2}𝟙_{V_n}` span the
3-dim quotient `𝒲 = ran(A)`, `𝓗_V = 𝒲 ⊕ ker A`, `dim 𝒲 = 3`, `dim ker A = 30`. Symmetrized divisor

$$A|_{\mathcal W}=\begin{pmatrix}0&\sqrt{99}&\sqrt{117}\\\sqrt{99}&0&\sqrt{143}\\\sqrt{117}&\sqrt{143}&0\end{pmatrix},\qquad \chi_{A|_{\mathcal W}}(x)=x^3-359x-2574.$$

(Verified: `verify_unified_backbone.py` §2.1.)

## 2. Canonical zone current and source projectors

`D_𝒲 = 24Q₉+22Q₁₁+20Q₁₃`; `Q_n` recovered by Lagrange interpolation of the distinct degrees. The zone
current `J = i[D_𝒲, A|_𝒲]` has `χ_J(x) = x(x²−Λ²)` with `Λ² = 2840` (derived). Orthogonal spectral split
`P₀ = I − J²/Λ²`, `P_act = J²/Λ²`, `R_zone = J² = Λ²P_act`. In the canonical part-size inner product
`G = diag(9,11,13)`, `J` is `G`-Hermitian (Lean `D0.Integration.V15.RawZone`: `comm³ = −2840·comm`, genuine
`G`-orthogonal projectors). These are source-side response projectors, not physical labels.

## 3. Marked `Q₈` terminal Fourier decomposition

`Ω₈ ≅ Q₈` on `V₉ = {ω₀}⊔Ω₈`; `ℂ[Q₈] ≅ ℂ⁴⊕M₂(ℂ)`. With the left regular rep and `τ(i,j,k)=(j,k,i)`:

$$E_0=\tfrac18\textstyle\sum_q L_q,\quad E_4=\tfrac12(I-L_{-1}),\quad E_3=\tfrac12(I+L_{-1})-E_0,$$

orthogonal idempotents, `E₀+E₄+E₃=I`, **ranks `(1,4,3)`** (Lean `Q8Terminal`, by trace). Fixed correspondence

$$\boxed{Q_9\leftrightarrow E_0,\qquad Q_{11}\leftrightarrow E_4,\qquad Q_{13}\leftrightarrow E_3}$$

forced jointly by `(p_e,p_μ,p_τ)=(0,1/4,1/3)`, `rank(E₀,E₄,E₃)=(1,4,3)`, and edge incidence
`𝓗_μ⊂E(V₉,V₁₁)`, `𝓗_τ⊂E(V₉,V₁₃)`. (Old swapped correspondence removed.)

## 4. Actual 359-edge terminal carrier

`𝓗_E = ℂ^{E(K(9,11,13))}`, `dim = 359`. Star modes `c_q = 11^{-1/2}Σ_{v∈V₁₁}|q,v⟩`,
`d_q = 13^{-1/2}Σ_{w∈V₁₃}|q,w⟩`, orthonormal. `e₀ = 24^{-1/2}(Σ_{V₁₁}|ω₀,v⟩+Σ_{V₁₃}|ω₀,w⟩)`,
`𝓗_μ = span(c₁,c_i,c_{−1},c_{−i})`, `𝓗_τ = span(r_B,r_C,r_D)` with `r_X=(d_X+d_{−X})/√2`.
`𝓗_term = 𝓗_e⊕𝓗_μ⊕𝓗_τ`, `dim = 1+4+3 = 8`, Gram `= I₈`. (Verified: `verify_unified_feedback.py` §4.)

## 5. Bare `C₄ / C₃` return sectors

`U_μ c_q = c_{iq}` (order 4), `U_τ : r_B→r_C→r_D` (order 3). Holonomy `C₄(λ)⁴=λI`, `C₃(λ)³=λI`,
`det(I−zU_term) = (1−z)(1−λz⁴)(1−λz³)`. (Lean `TerminalReturn`: `U_μ⁴=I`, `U_τ³=I`; holonomy det in cert.)

## 6. Canonical lepton channel

Stinespring `V_ℓ = Ω₀⟨e₉| + Ω₄⟨e₁₁| + Ω₃⟨e₁₃|` (maximally-entangled block vectors). `V_ℓ†V_ℓ = I_𝒲`,
`V_ℓ†(E_j⊗I)V_ℓ = Q_j`. Bare kernel `G_ℓ⁰ = Q₉/(1−z) + Q₁₁/(1−λz⁴) + Q₁₃/(1−λz³)` (block-trace identity
`(1/d)tr(I−zC_d)^{-1} = 1/(1−λz^d)`; verified §7).

## 7. Edge feedback from line-graph contact

`Q_bulk = I−P_term`, `P_br = P_μ+P_τ`, line graph `L_E = B_E^*B_E − 2I`. Contact `K = Q_bulk L_E P_br` has
**`rank K = 7`**, `K^*K > 0` (real 359-edge computation). Polar isometry `J_bulk = K(K^*K)^{−1/2}`,
`J_bulk^*J_bulk = P_br`. Balanced two-port `R_* = 2^{−1/2}\begin{psmallmatrix}I&-J^*\\J&I\end{psmallmatrix}`,
`U_E = (I_e⊕U_{\rm br}⊕J U_{\rm br}J^*⊕I_⊥)R_*` is **unitary**. Feedback

$$\boxed{F_{\rm term}=P_{\rm term}U_E^*Q_{\rm bulk}U_EP_{\rm term}=\tfrac12(P_\mu+P_\tau)}$$

`F_term P_e = 0`, `F_term P_μ = ½P_μ`, `F_term P_τ = ½P_τ`. (Verified §8: `max|F−½P_br| = 1e-16`.)

## 8. Feshbach reduction of the same unitary

Block-decompose this `U_E` as `[[A,B],[C,D]]` wrt `P_term⊕Q_bulk`. `W_eff(z)=A+zB(I−zD)^{-1}C`,
`det(I−zU_E)=det(I−zD)det(I−zW_eff(z))`. On the branch sector
`W_br(z)=U_{\rm br}(2^{-1/2}I−zU_{\rm br})(I−2^{-1/2}zU_{\rm br})^{-1}`, giving

$$\det(I-zW_\mu)=\frac{(1+\lambda z^4)^2}{1-\lambda z^4/4},\qquad \det(I-zW_\tau)=\frac{1+\sqrt2\lambda z^3+\lambda^2z^6}{1-\lambda z^3/(2\sqrt2)}.$$

(Verified §9, exactly.) Bare order-`r` poles → feedback-dressed order-`r` poles at `z⁴=4/λ`, `z³=2√2/λ`.

## 9. Feedback-dressed lepton Green theorem

$$\boxed{G_\ell^{\rm fb}(z,\lambda)=\frac{Q_9}{1-z}+\frac{Q_{11}}{1+\lambda z^4}+\frac{1+\lambda z^3/\sqrt2}{1+\sqrt2\lambda z^3+\lambda^2z^6}\,Q_{13}}$$

Check A (zero coupling `R_*→I`): `G_ℓ^fb → G_ℓ⁰`. Check B (pole supports): order-4 poles supported on
`Q₁₁𝒲`, order-3 on `Q₁₃𝒲`. Check C: positive feedback `F_term` is not a source of complex poles — these
come only from `W_eff`. (All verified `verify_unified_feedback.py`.)

## 10. Fibonacci / Pisot replication of the coupled determinant

Replicate `U_E` (not bare `U_term`) with Fibonacci multiplicities: `𝓗_E^{(n)}=𝓗_E^{⊕F_n}`,
`𝒜_n = F_n·𝒜_1`, `𝒜_1 = −log det(I−zU_E)`. Then `𝒜_{n+1}=𝒜_n+𝒜_{n-1}` and, by Binet,
`𝒜_{n+1}−φ𝒜_n = ψⁿ𝒜_1` with `|ψ|=φ⁻¹<1` — a genuine alternating Pisot-decaying tail. (Lean
`PhiReplication`: recurrence + Pisot identity + `|ψ|<1`, all proved over ℝ.)

## 11. Exact pole and residue atlas

| sector | dressed factor | poles | residue support |
|---|---|---|---|
| `e` | `1/(1−z)` | `z=1` | `Q₉𝒲` |
| `μ` (order 4) | `1/(1+λz⁴)` | `z⁴=−1/λ` | `Q₁₁𝒲` |
| `τ` (order 3) | `(1+λz³/√2)/(1+√2λz³+λ²z⁶)` | `λz³=(−1±i)/√2` | `Q₁₃𝒲` |

## 12. Physical boundary — finite resonances are not mass ratios

The poles `z⁴=4/λ`, `z³=2√2/λ` and the residue atlas are **exact finite return/resonance geometry** of the
constructed edge-feedback operator. They are explicitly **not** measured lepton masses, electron/muon/tau
decimal ratios, physical redshift, dark-energy `w`, or Standard-Model charge assignments. The chain is a
CONDITIONAL-EXTENSION on chosen primitives (holonomy `λ`, balanced feedback `R_*`); promoting any pole to a
physical observable requires a separate frozen selector (`PRIM-EDGE-HOLONOMY-SELECTOR`,
`PRIM-EFT-IR-MATCHING-FUNCTIONAL`) and remains a PROOF-TARGET.
