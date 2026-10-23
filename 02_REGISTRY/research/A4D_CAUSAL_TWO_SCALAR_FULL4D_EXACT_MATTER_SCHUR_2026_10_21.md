# D0 — genuine full-4D two-scalar N=1 causal material Schur: 2592 Euler equations reduce to 1296 local 2×2 implicit inverses

21 October 2026. Existing scientific Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constituent native-programme-v1. **Positive finite exact ANALYTIC small-data existence theorem for two original scalar fields on a Cauchy/inflow chart**, plus numerical nonzero-amplitude verification on the ORIGINAL n24/L8 Golden boxes. Not a root with four-sided Dirichlet constraints, not a complete 16-coframe/24-proper-Lorentz stationary state, not compulsory Book03 physical valuation/admission or physical GR closure. \`GR_closed=false\`.

## 0. The NEW resolved parent interface (not a renamed fixed-metric Newton witness)

The current branch has already solved 72 original scalar Euler variables on a 2D finite slab and numerically solved **2592 original scalar Euler variables** on a full 8×8×8×8 Role grid with genuinely unequal original Golden PF weights, fixing the entire spacetime Dirichlet collar (owners: \`A4D_NATIVE_GOLDEN_PF_MATERIAL_FLUX_2026_10_21.md\` §6 and \`check_native_n1_two_scalar_full4d.py\`). That computation DOES NOT by itself give a finite exact existence theorem or a scalable source elimination, because a global 2592×2592 Jacobian is inverted and its numerical small residual is not an interval proof.

**Here the type of boundary changes explicitly:** choose true *Cauchy data* on two consecutive time layers and fixed spatial **inflow** faces at all time layers. Final-time and downstream spatial values are OUTPUTS of evolution, not independently fixed Dirichlet constraints. For this genuine causal variational boundary class, the original N1 discrete nonlinear material equations are triangular: **each pair of material values on the next time layer is obtained by ONE two-component local implicit solve**. The full material Jacobian is block lower triangular, and its determinant is an exact product of genuine 2×2 blocks. Thus a finite analytic small-data root exists for every finite original Golden lattice, with arbitrary positive site PF and a supplied fixed diagonal Lorentzian background. This is stronger than a numerical giant Newton while distinct from the fixed-four-boundary result.

## 1. Same original signed Golden N=1 price, with ALL three genuine spatial fluxes

Consume literally the owner \`sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_scalar_flux.py\`, \`native_master.py\`, the original six based-face non-VSI rank-two metric \`check_star_rank2_seam.py\` and original 4D Golden address census \`check_original_inverse_pf_quantile.mjs\`.

On each anchored 4D cell \(z=(i,j,k,\ell)\) and its four TRUE forward links, retain the two original real scalar fields \(\Psi_A\) (A=0,1), the unchanged fixed positive Golden PF density \(\rho_z=L^4n_z/F_{n+1}>0\), the real proper-Lorentz/coframe geometry and exact based-six-face star scalar \(f_i\). Let
\[
 q_z(\Psi)=\sum_{A=0}^1\sum_{\mu=0}^3 g_i^{\mu\mu}
       (D_\mu^+\Psi_A(z))^2,\qquad
 g_i^{00}>0,\quad g_i^{aa}<0\ (a=1,2,3),
\tag{1}
\]
in the OWNED diagonal rank-two chart. The actual negative-orientation cap-N=1 complete CQ field price is, apart from genuinely field-independent fixed bank/compiler terms,
\[
\boxed{
 S_{\rm N1}[\Psi;g]=h^4\sum_{\rm forward\ cells}\rho_z
 F_{\rm N1}(-\tau f_i/\rho_z,\ \tau q_z/\rho_z),\quad \tau=1/20.
}
\tag{2}
\]
Here the SAME \(F_{\rm N1}(x,y)=-\alpha\beta[h_\varphi(r(x,-y))-h_\varphi(r_0)]\), \(\alpha\beta>0\), and the actual two-band \(r\), p=φ⁻¹, z_eff=2⁻²⁰, ALL losses and the original signed matter orientation are retained from \`GoldenMaster\`. A new affine matter action has not been inserted. The common \(\alpha\beta\) may be divided out of the MATERIAL Euler only because it is fixed and strictly positive on this admitted fixed-inventory chart; it still belongs to the actual paid full value. Absolute Book03 and any moving factory/preparation/clock variation must be added separately if they are physically in the same action.

Let \(W_z(q)=F_{{\rm N1},y}(-\tau f_i/\rho_z,\tau q/\rho_z)/F_{{\rm N1},y}(0,0)\), a nonzero analytic function in the strict original Golden positive chart. For the two-vectors
\[
 \mathbf u_z=D_0^+\boldsymbol\Psi(z),\qquad
 \mathbf s_{a,z}=D_a^+\boldsymbol\Psi(z)
\]
define the genuine currents
\[
 \mathbf J_z^0=W_z(q_z)g_i^{00}\mathbf u_z,\qquad
 \mathbf J_z^a=W_z(q_z)g_i^{aa}\mathbf s_{a,z}.
\tag{3}
\]
**Differentiating the actual complete (2)**, not postulating a conserved continuum current, gives every two-component interior material Euler row (up to the fixed nonzero \(2\tau h^3 F_{y}(0,0)\) factor):
\[
\boxed{
 \mathbf E_z=\mathbf J_{z-e_0}^{0}-\mathbf J_z^0+
       \sum_{a=1}^3(\mathbf J_{z-e_a}^a-\mathbf J_z^a)=0 .
}
\tag{4}
\]
The true PF factor cancels only *outside* W, via the original \(\rho_z\) prefactor and \(\rho_z^{-1}\) source query; the full spatially varying \(\rho_z\) remains in BOTH arguments of \(F_y\). Neither scalar is frozen; they couple through the same genuine nonlinear q.

## 2. THE exact causal inversion: all 2592 Euler rows become 1296 independent 2×2 local operations

Fix \(\boldsymbol\Psi\) on the FIRST TWO complete time layers, and on the spatial inflow faces \(j=0\) OR \(k=0\) OR \(\ell=0\) of every future time layer, compatibly with those first layers. Upper spatial faces may be given as output controls for gradients on the known current layer; they are NOT independently constrained as final-state Euler/Dirichlet roots.

Process time \(i=1,2,\ldots,L-2\). At one fixed time process spatial cells in increasing lexicographic order \((j,k,\ell)\) (the immediate predecessor for each of three spatial directions is earlier). At site z, the WHOLE previous-time current and all three incoming spatial currents are ALREADY computed, while all three spatial forward differences of the CURRENT time layer are already known:
\[
 \mathbf R_z=\mathbf J^0_{z-e_0}+\sum_{a=1}^3\mathbf J^a_{z-e_a},
 \quad
 \mathbf c_z=\sum_{a=1}^3 g_i^{aa}\mathbf s_{a,z},
 \quad q_{\rm space}=\sum_{a=1}^3g_i^{aa}\|\mathbf s_{a,z}\|^2 .
\]
The only unknown is the TWO-vector \(\mathbf u_z\), and (4) is EXACTLY
\[
\boxed{
 \mathcal T_z(\mathbf u)
 :=W_z(g_i^{00}\|\mathbf u\|^2+q_{\rm space})
       (g_i^{00}\mathbf u+\mathbf c_z)
 =\mathbf R_z.
}
\tag{5}
\]
Then assign
\(\boldsymbol\Psi_{i+1,j,k,\ell}=
\boldsymbol\Psi_{i,j,k,\ell}+h\mathbf u_z\).
NO other future material unknown is needed in (5). This is true for all three spatial directions; it is not a one-dimensional temporal flux assumption.

Write \(w=W_z(q)\), \(w_y=\partial W_z/\partial y\) for the derivative of W with respect to its SECOND native Golden input argument \(y=\tau q/\rho_z\), and \(g_t=g_i^{00}>0\). The actual exact 2×2 differential is
\[
D_{\mathbf u}\mathcal T_z
 =g_t w I_2
   +\frac{2\tau g_t}{\rho_z}w_y\,
        (g_t\mathbf u+\mathbf c_z)\otimes\mathbf u .
\tag{6}
\]
Sherman–Morrison and the determinant lemma give
\[
\boxed{
 \det D_{\mathbf u}\mathcal T_z
 =(g_tw)^2\Delta_z,\qquad
 \Delta_z=1+
 \frac{2\tau}{\rho_z}\frac{w_y}{w}\,
 \mathbf u\cdot(g_t\mathbf u+\mathbf c_z).
}
\tag{7}
\]
At ZERO two-scalar field \(\mathbf u=\mathbf s_a=0\), \(\Delta_z=1\) EXACTLY, while \(g_tw>0\) for the original N1 Golden chart (any finite positive original PF field and sufficiently small fixed \(f_i\)). The REAL analytic implicit-function theorem therefore gives a unique analytic local inverse of (5) for every site sufficiently near the zero-history reference. Since a finite grid contains only finitely many sites, **causal induction proves an exact nonzero small-Cauchy-data solution of ALL full-4D two-scalar interior Euler rows on every finite mesh**, with positive original site counts, without globally inverting any hyperbolic operator. The small-data threshold is mesh dependent unless a separate uniform stability estimate is proved. This is an **exact existence theorem**, not an assertion that the particular large numerical amplitude below has an interval-certified exact root.

### The whole HUGE Jacobian determinant is a finite product, not an unknown rank

Order the \(2(L-2)^4\) material output variables as
\(\boldsymbol\Psi_{i+1,j,k,\ell}\) in increasing \((i,j,k,\ell)\), for each interior material Euler equation at \((i,j,k,\ell)\). Its dependence on future variables is only at its OWN site and lower causal predecessors. Thus the full material Euler Jacobian is **block LOWER TRIANGULAR**. With the normalized divergence convention (4), its precise diagonal blocks are \(-h^{-1}D_{\mathbf u}\mathcal T_z\). In particular
\[
\boxed{
 \det D_{\Psi_{\rm future}}\mathbf E
 =\prod_{\rm interior\ } h^{-2}(g_i^{00}w_z)^2\Delta_z .
}
\tag{8}
\]
The sign is positive because each block has size two. Under \(\Delta_z\ne0\), the FULL 2592-dimensional Jacobian is invertible. Its inverse action on any geometric variation is computed by the SAME triangular forward substitution of 1296 **2×2** linear blocks. This is the genuinely reusable material Schur interface for future simultaneous coframe+connection source solving.

For a full sourced action, varying geometry after this CAUSAL matter solution introduces the genuine **OUTFLOW boundary generating-form term** from the final time and spatial outgoing fields, as well as the interior geometric source:
\[
D_g S[g,\Psi_{\rm causal}(g)]
 =D_gS|_{\Psi}
 +\underbrace{(D_{\Psi_{\rm out}}S)
                  D_g\Psi_{\rm out}}_{\rm real\ boundary\ flux}.
\tag{9}
\]
The interior matter Euler term vanishes identically. It would be WRONG to delete the outflow term and declare full all42 stationarity; double-sided Dirichlet is a different boundary problem. The attached material Schur formula keeps this distinction explicit.

## 3. ORIGINAL full 4D numerical nonvacuum stress test (not a claimed interval certificate)

Independent author execution of \`check_causal_4d_two_scalar_all_euler.py\` and a longer independent exact-price complex-step control ran against the TRUE original \`check_native_n1_scalar_flux.py\` data at n=24,L=8, same signed GoldenMaster N1, original 75025 nested-box words, all 4096 genuine Role sites and highly unequal PF \(0.2183805398\le\rho_z\le2.3475908031\). The metric is the unchanged original non-VSI rank-two time-dependent diagonal coframe and the six-face scalar \(f_i\); no standard affine scalar action substituted.

Take the original two-species seed \(\Psi_0\) with time derivative \(D_t\Psi_0=\epsilon A(t)^2\), \(\Psi_1=\epsilon x\), \(\epsilon=(2\kappa)^{-1/2}\), full two-time Cauchy data and all spatial inflow data fixed to this seed. The source before is NONZERO:
\[
 \|\mathbf E_{\rm seed}\|_\infty=1.98483546655\cdot10^{-4}.
\]
After sequential 1296 two-component implicit solutions:
| Actual full-4D original check | Measured |
|---|---:|
| ALL two-field Euler rows | 2592 |
| Maximum FULL divergence residual | \(1.9540\cdot10^{-16}\) |
| Species0 / species1 residual | \(1.9540\cdot10^{-16}\) / \(1.2075\cdot10^{-16}\) |
| Maximum original scalar value correction | \(1.06437\cdot10^{-4}\) |
| Maximum genuinely generated nonlinear \(q\) | \(3.61801\cdot10^{-4}\) |
| Maximum iterations of any local 2×2 Newton | 4 |
| Range of true local rank-one determinant factors | \([1.00233,1.01610]\) |
| Range of local \(w\,g^{00}\) | \([1.65114,1.72749]\) |
| Full Jacobian logarithmic determinant from (8) | \(\sim6738.94\) |

No artificial PF smoothing was used: these are the ORIGINAL jagged native n24 counts. The output is NOT required to satisfy both the initial AND final Dirichlet boundaries. Numerical residuals are not interval proofs; exact analytic small-data local existence is established independently by (7) and finite induction.

**Direct full-CQ negative/positive control.** At six independent actual sites/species, recomputing the FULL original N1 binary entropy price (not just its flux formula) by 70-digit complex-step gives derivatives within \(1.3\cdot10^{-17}\) of zero after the evolution, while the original seed has true nonzero price gradients up to \(4.7052\cdot10^{-10}\) (without the common αβ/h factors). The nonzero seed gradients agree with the independent flux predictor to absolute error \(<2\cdot10^{-17}\). This checks that the causal recursion is an Euler solve of the SAME full N1 CQ price, not of a different kinetic action.

## 4. Critical HOSTILE join with Ward42→12: exact material stationarity changes SOURCE SUPPORT

The existing \`check_ward12_spatial_source_equivalence.py\` proves that ON THE SPECIFIC spatially homogeneous DIAGONAL COFRAME/PURE BOOST and TWO-FIELD profile with only the original two supported gradient directions, the 42 geometric+material Euler ZERO test reduces via exact rank-six SO Ward identities to twelve named spatial-link sources. **After genuinely solving the full 4D material equations on unequal PF, the scalar gradients acquire off-axis components.** The genuine material stress matrix
\(\sum_A D_\mu^+\Psi_A D_\nu^+\Psi_A\) then has nonzero off-diagonal entries. At the same n24/L8 causal solution:
\[
\begin{array}{ll}
\max|T_{tx}|=1.68481\cdot10^{-4},&
\max|T_{ty}|=7.36183\cdot10^{-5},\\
\max|T_{tz}|=6.99433\cdot10^{-5},&
\max|T_{xy}|=9.40879\cdot10^{-5}.
\end{array}
\tag{10}
\]
Thus the special Ward12 COFRAME SUPPORT premise is no longer satisfied even though the full material Euler is solved. The underlying gauge Ward identity survives, but its *specific six pivot + twelve target subset* does not automatically remain a complete zero test for these corrected fields. **Do not claim 12 remaining equations unless the exact source support is reproved after this matter correction**, or simultaneously solve the added non-diagonal coframe/link rows.

This is a concrete interaction of two genuine derived owners that rules out an appealing FALSE completion route. The positive usable route is: first causal-exclude all matter interiors by (5)–(8) with actual retained outflow; then form and solve the true enlarged coframe/connection Schur and boundary source, including the newly generated mixed matter stress, on the SAME original finite 4D carrier. The Book03 absolute Info/clock/writer/selection gate remains independent and OPEN.

## 5. Integration statement, sharply typed

**DISCHARGED on this literal positive N1 CQ geometric-input chart:** the mathematically exact local small-data existence of TWO simultaneously nonzero original CAR material fields satisfying every interior Euler equation at ANY given finite genuine Golden PF mesh, and the global matter Jacobian invertibility/implicit derivative via only local 2×2 blocks with one causal boundary. One actual large-amplitude full n24/L8 field has a numerical small-residual witness. The superseded all-sided 2592D Newton and this causal solution solve DIFFERENT boundary problems; neither is physically admitted automatic time dynamics until its initial/inflow rule is sourced.

**STILL OPEN:** genuinely all-sided Dirichlet root of the same matter system (only the earlier numerical witness), mixed matter+geometry full 16+24 field variation/collar and gauge-fixed compatible inverse, any independent input/observer/source, the unique ACTUAL Book03 branch Info/feedback/clock and compulsory field-writer/execution selection, and uniform continuum Einstein–CAR recovery. No global statement about arbitrary off-diagonal Lorentz coframe or Book heat carrier is smuggled in. \`GR_closed=false\`.

**Reproduction:** \`sources/d0_causal_full4d_scalar_schur_2026-10-21/check_causal_4d_two_scalar_all_euler.py\` consumes the OWNED \`sources/d0_native_golden_pf_material_flux_2026-10-21/check_native_n1_scalar_flux.py\`; no new independent addresses. Full independent-price/derivative replay and local analytical proof are retained in this document and the bounded author evidence. No Lean or independent interval acceptance claimed.
