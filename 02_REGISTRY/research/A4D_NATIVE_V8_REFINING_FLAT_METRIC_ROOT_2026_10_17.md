# Новый constructive bridge: exact v8 homogeneous metric/matter roots for arbitrarily fine 4D grids

17 October 2026. EXISTING Draft #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. RESEARCH / ANALYTIC EXISTENCE OF REFINING **FLAT** FINITE-GRID ROOTS (restricted original v8 carrier). Not physical GR, not a curved fixed-source root, not the original unweighted raw h^-2/#216 terminal. No new action, code, cost, cut, β, M or z. Consumer: current common GR synthesis and nonempty exact refining-family lower wall.

## 0. Exact same native operator/action, and independently conserved matter

Input from A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md §0.1 and sources/d0_native_flatmoduli_action_2026-10-16/RESULT_RU.md: full thermal spectrum is all L⁴ momenta ×16 CAR, and the actual first shell has eight momenta ±e_r ×16 CAR =128 reference-matter modes. Keep p=φ^-1, z=2^-20, M=128, α_L=p²/(128L²), m_L=256L², β=m_L α_L=2p², n_L=m_L/2. All workspace/reference multiplicities in H are retained; their fixed-field first derivative is zero, not a deleted carrier.

Choose the native constant positive real Gram
    G(d,o)=(d−o)I_4+o 11ᵀ,   d−o>0,d+3o>0.
Represent it by an actual uniform native frame F=G^1/2, internal n=e0 and stored constant links A=I. Both literal stored-adjoint identities hold, and all16 exterior grades remain. For finite h=1/L, z_j(k)=L(exp(2π i k_j/L)−1),

    v_d(k)=sum_j|z_j|²,
    v_o(k)=|sum_j z_j|²−v_d(k),
    λ_L(k)=d v_d(k)+o v_o(k),
    B_k=1−α_L λ_L(k), K_k=B_k^m_L.

The identical original finite functional, modulo field-independent constants, is

    S_L(d,o)=[log(16 sum_k K_k)]/β
             −16M sum_k log(1−z+zK_k)
             +γ_L d,                                        (V1)
    γ_L=4 L² sin²(π/L).

The last term is the actual faithful full-shell matter R=Tr(ρ_Ω Δ)=γ_L d for ρ_Ω=P_Ω/128 with full reference128 purification; it is NOT fitted. On the eight first-shell momenta (only one nonzero Fourier coordinate), λ_Ω=γ_L d exactly and every CAR form is present. The same normalized amplitude therefore solves the full matter first Euler equation Δ C=λ_Ω C in this fixed Gram family, including all reference-column and rank-birth first variations.

**Exact two-source formula** (no root computation or skipped normalized trace): for j=d,o let

    W_k=K_k/B_k,
    A_k=1−z+zK_k,
    F_j(L;d,o)=
        −sum_k W_k v_j(k)/sum_k K_k
        +16M β z sum_k W_k v_j(k)/A_k
        +γ_L 1_(j=d).                                      (V2)

At L=8 the actual certified root from the owner is d=0.0636351915943445350…, o=0.0040167350432317253…. Direct independent evaluation (V2) reproduces this root to the stated digits. **Negative control:** replacing sum K in the heat denominator by sum W leaves an ≈0.00420850 nonzero spurious radial source at the certified point; it fails. The true source normalizer must not be frozen or changed.

## 1. Continuous 2-equation limit has a nondegenerate positive root

Let a=2π and λ_∞(k)=a²[(d−o)|k|²+o(Σ_i k_i)²], k∈ℤ⁴, and w=e^(−β λ∞). On compact SPD charts containing the first-shell root, dominated Gaussian sums and Taylor expansion of B^m give convergence of the **actual source and its Jacobian** F_L→F_∞ in C¹; further F_L=F∞+h² F₂+O_C¹(h⁴) as a consequence of even powers in the real-symmetric Fourier symbol and the summable Gaussian polynomial tails. More precisely:

    |λ_L(k)−λ∞(k)| + ||D_G(λ_L−λ∞)|| ≤ C h² |k|⁴
on the centered Brillouin zone, uniformly on a bounded SPD chart; α_L λ_L≤u_*<1. The K vs exponential mismatch and all first/second G derivatives are bounded by C h² polynomial(k) exp(−c|k|²), with an exponentially small cutoff tail. Thus

    ||F_L−F∞||_{C¹(B)} ≤ C_B h².                            (V3)

The continuum residual is still the ORIGINAL v8 function:

    F_j(∞;G)=−E_w[v_j]
       +16 M β z Σ_k w_k v_j(k)/(1−z+z w_k)
       +a² 1_(j=d).                                         (V4)

At o=0, each v_o(k)=a²[(Σk_i)²−|k|²] is odd under independent sign-reflections in expectation; hence F_o(∞;d,0)=0 **exactly**. Define theta moments

    Θ_r(t)=Σ_{n∈ℤ} n^r exp(−t n²),   t=β a²d,
    Θ_0=Θ(t), Θ_2 and Θ_4.

For q=z/(1−z), elementary product decomposition and absolutely convergent geometric series give

    F_d(∞;d,0)/a² =
      1−4 Θ₂(t)/Θ₀(t)
      +[64 M β z/(1−z)]
          Σ_{n≥1} (−q)^(n−1) Θ₂(nt) Θ₀(nt)^3.            (V5)

The signs are strict:
    −0.891 < F_d(∞;0.059,0)/a²? NO: full unscaled F_d is −0.890215...,
    +1.002 < F_d(∞;0.061,0) < +1.004.

For clarity, use the **unscaled** source F_d in these inequalities:
    −0.891 < F_d(∞;0.059,0) < −0.889,
      1.002 < F_d(∞;0.061,0) < 1.004.                  (V6)

A one-dimensional Gaussian theta tail beyond |n|≥8 is <10^−42 on the entire interval (β a²d>1.77); the feedback series after n=5 has bound C q^5<10^−24 and can be enclosed more tightly if needed. These standard explicit tail estimates make the displayed loose interval signs independent of floating root solves.

The Hessian of original S∞ is block diagonal at o=0 by independent sign parity. Exact analytic expressions:

    S∞,dd=4β a⁴(Θ₄/Θ₀−(Θ₂/Θ₀)²)
          −16 M β² z(1−z) Σ w v_d²/A²,
    S∞,oo=24β a⁴(Θ₂/Θ₀)²
          −16 M β² z(1−z) Σ w v_o²/A²,
    S∞,do=0, A=1−z+z w.                                 (V7)

On d∈[0.059,0.061], θ-moment bounds yield S∞,dd>700 and S∞,oo>1500 (conservative strict inequalities). For S∞,oo, the negative/positive ratio is ≤16 M β z Θ₀^4/(1−z)<0.005; for S∞,dd the Gaussian zero/first-shell variance lower bound exceeds the total O(z) feedback estimate. Therefore both Hessian eigenvalues are positive on the declared interval, independently of sampled rank search.

The intermediate value theorem, strict positivity and (V6) give a **unique nondegenerate** continuum stationary root in this invariant positive sector:

    d_*=0.05992945551128871… , o_*=0,
    S∞,dd≈948.02982028,  S∞,oo≈1794.30131141.          (V8)

This is a fixed **homogeneous flat** continuum root, not a curved Einstein metric. The other large-scale radial root near s≈15.51 is not used; its transverse stability and two-scale finite-grid continuation require separate analysis. No need to select an IR root by fiat.

## 2. Theorem: exact finite roots continue to every sufficiently fine 4D lattice

Let B be a small compact open positive-Gram neighborhood of (d_*,0) where the Hessian of S∞ remains positive definite. From (V3), Hessian of S_L is positive definite on B for all sufficiently large L. Moreover S_L→S∞ uniformly on B up to field-independent additive constants; the unique continuum minimum is strict and lies in B. Its finite-L minimizer lies in the interior of B and is unique by strict convexity. Consequently, without another arbitrary action or a separate extra field,

    **for every sufficiently large integer L there exists a unique**
    (d_L,o_L)∈B with F_d(L;d_L,o_L)=F_o(L;d_L,o_L)=0,
    d_L−o_L>0,d_L+3o_L>0.                              (V9)

The original shell 128 density is an exact normalized preparation critical point at every such finite L because its complete 128 support consists of degenerate eigenvectors of the actual Δ_L. No rank truncation is used.

At G(d_L,o_L) the full finite action is invariant under permutation of the four coordinate directions (including the thermal full Brillouin torus, the equal-population shell and the reference). Its derivative among arbitrary **ten homogeneous real symmetric Gram directions** is therefore a matrix with equal diagonal rows and equal offdiagonal rows, i.e. in span{I,11ᵀ}. The two independent equations F_d=F_o=0 annihilate this entire invariant covector. Thus (V9) gives **all ten constant-metric first-source equations**, not merely one radial derivative, as well as the full normalized matter amplitude first-source equations. This is exactly the same conventional v8 *restricted stored/coefficient* domain as the original L8 root, generalized across L.

Scope: no independent all-edge Lorentz/link Euler, field-dependent observer/current equation, physical primitive preparation, nonconstant fixed source, full unrestricted site-variation image or original raw h^-2 comparator is concluded. Translation covariance can transport this constant-source result when the exact same local field/interface hypotheses hold; it does not enlarge the stored-adjoint tangent image.

## 3. Stronger asymptotic refinement law: the offdiagonal correction is fixed, not fitted

On the centered Brillouin lattice, the identity

    Re z_j(k)=−|z_j(k)|²/(2L)

holds exactly. At isotropic G=dI, every thermal/feedback source weight depends only on the even squares |z_j|²; summation over signed momenta eliminates sin-odd cross terms in ∂oλ. Consequently the first nonzero o-source is order h², not order h:

    F_o(L;d_*,0)=h² B_o+O(h⁴),
    B_o=(1/8)Σ_{k∈ℤ⁴} η_k v_o(k)^2,
    η_k=−w_k/Z+16Mβ z w_k/(1−z+z w_k).               (V10)

The 1/8 arises from the exact even-even Fourier endpoint drift, not from a fitted golden number. The response in the o direction is S∞,oo>0, hence

    o_L=−B_o/S∞,oo ·h²+O(h⁴)
       =0.1636271242849276… L^−2+O(L^−4).              (V11)

The almost exact relation to 1/(8β)=0.16362712429686846… follows because J has a tiny z² correction; **not** a new fundamental identity. In particular the true offdiag correction is a calculated lattice artifact/source forced by the original one-sided stencil and real-symmetric Gram, not an independently physical shear.

The d-source also has an explicit O(h²) coefficient. Let
    v=a²|k|²,  v1=−a⁴ Σ k_i⁴/12,  alpha0=p²/128,
    κ=−β d_* v1 −(β alpha0/2)d_*² v²,
    w=e^(−β d_*v),   D=1−z+z w,
    <f>=Σ w f/Σ w.
Then

    B_d=−<v1>−Cov(v,κ)−alpha0 d_*<v²>
       +16Mβ z Σ(w/D)[v1+(1−z)v κ/D+alpha0 d_*v²]
       −a⁴/12;                                         (V12)
    d_L=d_*−B_d/S∞,dd·h²+O(h⁴)
       =d_*+0.2383372544069484… L^−2+O(L^−4).          (V13)

All sums converge exponentially. κ comes from the genuine finite power K=(1−α λ)^m, not an artificially substituted continuum heat operator. The −a⁴/12 in B_d is the true shell R correction γ_L.

Thus this branch has a **completely determined** continuum metric and first finite corrections:

    G_L(d_L,o_L) → d_* I4,
    F_L=G_L^(1/2) → sqrt(d_*) I4,
    rho_L=P_Ω/128  (all16×8, reference128).            (V14)

All finite roots are genuinely nonempty in this **flat homogeneous metric+matter** sector, for all sufficiently fine L. The limit does not move toward a fixed nonconstant curved Einstein metric and is therefore not an original source/refinement terminal.

## 4. Reproducible numerical evidence and negative controls

The bounded checker sources/d0_native_v8_refining_flat_2026-10-17/check_refining_flat_roots.py evaluates the full exact L⁴ Fourier trace ×16 (without deleting thermal modes) and both true derivatives (V2), with original beta,z,M. The table is **not** the proof of V9; the proof is the theta bounds and C¹ root stability.

| L | d_L | o_L | L² o_L |
|---:|---:|---:|---:|
| 8 | 0.0636351915943 | 0.0040167350432 | 0.257071 |
| 12 | 0.0615907473657 | 0.0013710618540 | 0.197433 |
| 16 | 0.0608633374878 | 0.0007087162833 | 0.181431 |
| 24 | 0.0603439178076 | 0.0002972066924 | 0.171191 |
| 32 | 0.0601624342443 | 0.0001638835242 | 0.167817 |

The L8 line agrees with the EXISTING certified owner, independent numerical reproduction. On all displayed rows the two residuals are <1e−10 in the native source normalization and the Gram eigenvalues d−o, d+3o are positive. The coefficient limits (V11),(V13) are analytically computed from source derivatives; the observed L^−4 approach is a secondary control.

**Negative controls**: (i) alter the H global normalizer ΣK→Σ(K/B): the owner L8 root develops a nonzero >0.004 radial residual; (ii) remove the feedback Mz and the root equations shift, so neither the root nor the correction can be attributed to curvature alone; (iii) do not infer arbitrary site/link Euler rows from the two invariant Gram equations, a prohibited promotion detected by the source contract.

## 5. Integration into the real GR target

This new theorem settles **one nonempty exact refining lower-wall carrier**, instead of iterating disconnected L8 rank checks. More specifically, it gives a domain of *exact finite metric/matter stationary values* for every sufficiently large L and an O(h²) refinement map, with the same original action.

For OTO, the missing nontrivial step is **curved deformation about this true root**, with genuine constrained coframe/connection/observer and matter zero-mode equations, second-order rank-birth/ memory solvability, and a fixed nonconstant smooth metric/tau comparator. Flat G_L→d_* I implies Einstein tensor0, so the original nontrivial Einstein source has not been obtained by (V9). Do not use the two scalar equations to claim general GR.

The immediate consumer is an exact shape/connection perturbation of (V9) at one nonzero Fourier mode q while retaining the original stationary preparation eigenvectors and actual source. The earlier owner A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md conditions (19)–(27) (especially M_perp on the stationary memory fibre) remain mandatory. The original #216 unweighted raw h^-2 all-ten fixed-g, independent-tau target stays OPEN.
