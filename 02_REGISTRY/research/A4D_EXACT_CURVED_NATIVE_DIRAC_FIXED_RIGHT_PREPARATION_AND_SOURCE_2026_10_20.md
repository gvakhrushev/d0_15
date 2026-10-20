# Exact curved native preparation: the original full16 Dirac has a protected null block, including reference128

20 October 2026. Positive constructive continuation of existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input `e15c19f01e33fd420d4233eaa059ef3f09273a79`.
Follow-ups `bea09e331` and `f6fd07136` consumed: new paid-code, future-MDL,
CAR/Spin and corrected P25/P34 source gates retain their own admission scope.
The operator used below
is precisely the already-defined exterior Λ(U) full-Lorentz interface;
no replacement by a new spinor transport is inferred from those updates.
No new action, survival-reconstructed Dirac, physical preparation law,
carrier truncation, task, BOOK/CORE claim or GR closure.

**Result used by the parent.** On a genuinely curved finite pp-wave chart,
the ORIGINAL positive-adjoint spatial Dirac has an explicit reducing
four-grade subspace, independent of the wave profile. Its exact one-dimensional
difference operator supplies preparations with ANY prescribed jointRIGHT
Gram of sufficient rank capacity. In particular, reference128 can be
faithful and preparation-stationary for the actual conditional H+J+R.
This is exact at finite spacing and has a bounded-energy refining version.
The two lower grades also have identically zero first Rayleigh link source
in all24 independent Lorentz directions. The nonzero coframe and observer
sources are computed below; they are retained in the joint equations.

This directly advances the curved preparation step. It does not rely on
the previous input-only screening argument or introduce a different price
to evade it. Geometry here enters the original operator itself.

## 1. The unchanged operator and carrier

Use [the full-Lorentz original source](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md),
§§1–3, and its actual full16 exterior creators C_a and annihilators I_a.
On all sites and all16 CAR grades:
\[
d_\ell=\ell^{-1}\sum_{r=u,v,x,y}C(v_r(x))
 [\Lambda(U_r(x))S_r-I],\qquad D_\ell=d_\ell+d_\ell^\dagger,
\quad\Delta_\ell=D_\ell^2.\tag{1}
\]
The dagger is the TRUE positive Hilbert adjoint, including shifted
coefficients and \(\Lambda(U)^\dagger\). It is not the Lorentz inverse
transport. Counting-site measure and a fixed observer are used here,
exactly as in that matrix chart. All complementary states remain.

Choose a fixed null internal basis (+,−,2,3),
\(\eta_{+-}=\eta_{-+}=1\), \(\eta_{22}=\eta_{33}=-1\), and
\(n=(e_++e_-)/\sqrt2\). Then the original observer pairing h_n is I.
The null basis is one fixed exterior change of the same CAR16 representation;
it does not add modes or change its dimension. Write q=e_- and Ω for its
oriented top form. The scaled pp-wave coframe is
\[
e^+=\nu^{-1}du,\quad e^-=\nu^{-1}(dv+Hdu/2),\quad
e^2=\nu^{-1}dx,\quad e^3=\nu^{-1}dy,\tag{2}
\]
where H=H(u,x,y) is independent of v. Thus its actual raised inverse legs are
\[
v_u=\nu q,\quad v_v=\nu(e_+-Hq/2),\quad
v_x=\nu e_2,\quad v_y=\nu e_3.\tag{3}
\]
Take U_v=U_x=U_y=I and an actual proper Lorentz U_u with U_u q=q.
In particular the OWNED pp-wave links
\(U_u=\exp(h(K_2N_2+K_3N_3))\), with
\(N_i=E_{-,i}+E_{i,+}\), satisfy this exactly, including the original
half-step coefficients. The theorem needs no approximation of exp(hK).
A nonzero transverse difference of K gives nonidentity based plaquettes
and genuine curvature, as in the owned pp-wave family and exact fixture.
The usual common-null N2,N3 commute; no crossed-null theorem is inferred.

Use periodic shifts, or boundary operators that preserve the constant
transverse modes and the stated adjoint identities. The exact periodic
fixture tests a curved connection, not the owned global vacuum Cartan
equations. A nonconstant vacuum pp-wave on a compact transverse torus
is not asserted. Fixed-collar interior geometry requires its actual boundary
consumer before a global preparation is inferred.

For bounded H,K and h, one fixed sufficiently small ν>0 makes both
C(v_r) and C(v_r)Λ(U_r) strict contractions. Hence this is inside the
declared Julia matrix window. A constant coframe scale leaves the
corresponding Lorentz connection unchanged. Native generation/price of the
preparation and gates is still a physical premise.

## 2. Exact four-grade intertwining, including the nonunitary link

Define the orthonormal quartet
\[
b_0=1,\quad b_1=q,\quad b_3=I_q\Omega,\quad b_4=\Omega.
\tag{4}
\]
The decisive exterior identities are
\[
\Lambda(U)q=q,\quad
\Lambda(U)^\dagger I_q\Omega=I_{U^{-1}q}\Omega=I_q\Omega,
\quad C(q)\Lambda(U)I_q\Omega=\Omega.\tag{5}
\]
Here det U=1 and Uq=q. **Λ(U) itself need not fix I_qΩ.** Replacing
the true adjoint by an inverse or claiming an orthogonal link would lose
the actual proof. The exact checker rejects that incorrect fixed-vector
claim explicitly.

Let δ=(S_u−I)/ℓ, δ†=(S_u^†−I)/ℓ. For ANY scalar sequence f(u), direct
substitution into EVERY raising and lowering row of (1) gives
\[
\begin{array}{ll}
D(fb_0)=\nu(\delta f)b_1,&D(fb_1)=\nu(\delta^\dagger f)b_0,\\
D(fb_3)=\nu(\delta f)b_4,&D(fb_4)=\nu(\delta^\dagger f)b_3.
\end{array}\tag{6}
\]
The potentially dangerous v row cancels because H is independent of v;
the x,y rows cancel on constant transverse profiles. These are exact finite
endpoint cancellations, not continuum d²=0. In particular the finite
full-Lorentz torsion equations are not being silently imposed instead of
the given stencil.

Let J embed the quartet-valued u sequences as normalized transverse
constant states in the FULL site⊗CAR16 Hilbert space. Then
\[
\boxed{D J=J D_\parallel,\qquad
\Delta J=J(\nu^2\delta^\dagger\delta\otimes I_4),}
\tag{7}
\]
where D_parallel consists of the two identical 2×2 blocks in (6).
J is independent of H and U_u. Selfadjointness makes ran J reducing,
not just invariant. For ψ_k(u)=exp(2πiku/L_u),
\[
\boxed{\Delta(\psi_k b_a)=\lambda_{k,\ell}\psi_k b_a,
\quad\lambda_{k,\ell}=4\nu^2\ell^{-2}\sin^2(\pi k/L_u),
\quad a=0,1,3,4.}\tag{8}
\]
Thus curved geometry and the true positive adjoint admit an explicit
preparation block. No flat-to-curved eigenstate perturbation, spectral-gap
IFT or amplitude expansion is needed for this block.

## 3. Faithful fixedRIGHT preparation: no common-energy assumption

The actual [fixedRIGHT Euler owner](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md),
§§6.30 and6.63, already gives the correct criterion. For the SAME positive
Hilbert/whitened amplitude M with prescribed joint Gram
\(M^\dagger M=\Sigma_R\), TrΣ_R=1, the original Rayleigh part is
R=Tr(M†ΔM). Its complete fixed-Gram preparation Euler is
\[
\boxed{[\Delta,\rho]=0,\quad\rho=MM^\dagger,}
\quad\Longleftrightarrow\quad
\Delta M=M\Xi,\quad\Xi^\dagger=\Xi,\quad[\Xi,\Sigma_R]=0.
\tag{9}
\]
Indeed δρ=[K,ρ] for the full LEFT-unitary tangent and
δR=Tr([ρ,Δ]K). All such tangents, including those mixing the protected
block with its full complement, are tested. A common eigenvalue is NOT
required when the complete RIGHT Gram is fixed.

Let \(\Sigma_R=\sum_{a=1}^r\mu_a|r_a\rangle\langle r_a|\).
Choose r orthonormal eigenvectors φ_a from (8), possible when r≤4L_u,
and set
\[
\boxed{M=\sum_a\sqrt{\mu_a}|\phi_a\rangle\langle r_a|.}\tag{10}
\]
Then M†M=Σ_R EXACTLY and (9) holds, even for unequal λ_a and unequal μ_a.
This construction acts on the preparation correlations, not by rotating
or discarding the immutable RIGHT. Singular Σ is handled on its fixed
support. H and J of the ORIGINAL conditional H+J+R do not depend on M,
so (10) solves their full preparation rows as well.

In particular, choose 32 real u Fourier functions (16 complete cosine/sine
pairs) and all four quartet vectors. At L_u≥33 this gives128 orthonormal
nonzero-energy states. Equal weights give reference128 Gram I128/128.
Alternatively, on L_u=32 the entire quartet×u block has dimension128
and a real localized-u purification gives the same Gram; zero-energy
modes are then included honestly. No phase preparation oracle is needed
for this localized example. All16 CAR grades and all128 reference
coordinates remain in the carrier.

There is also a useful low-grade choice: 32 cosine/sine pairs times only
b0,b1 give rank128 at L_u≥65. It solves (9) AND has zero first Rayleigh
source in every proper-link direction, as proved in §5. The Hodge half
is available for retained coherent preparations, but it must not be
misidentified with zero spin source.

This is existence on the declared fixedRIGHT manifold, not a claim that
original chronological primitives prepare it at zero work. An additional
prescribed LEFT clock/grade14 marginal or P1 matter-current constraint
must be checked separately. In particular b1 is a null internal direction;
the fixed native timelike mask1/grade14 condition is not preserved merely
by calling the quartet a basis change.

## 4. Exact curved section and controlled energy at refinement

The occupied states in (10) can be chosen independent of H,K for every
field in this common-null chart. Thus M_H is an EXACT constant-Gram
preparation-stationary section over a curved family, rather than an
approximately stationary flat seed inserted into a curved operator.
For any profile tangent V in that family,
\[
(D_V\Delta)J=0,\qquad
D_VR=0,\qquad D_VD_{prep}R=0.\tag{11}
\]
The last statement holds against every actual preparation tangent: the
operator variation has zero rows and columns on the protected block.
It does not require inversion of a possibly singular preparation Hessian.
It is not a statement that all40 general field sources vanish.

For fixed physical u period T_u, take ℓ=h and L_u h=T_u. Keep a fixed
finite set of modes |k|≤k_max as the grid refines. Then
\[
0\le\lambda_{k,h}\le\nu^2(2\pi k_{max}/T_u)^2,\qquad
\lambda_{k,h}\longrightarrow\nu^2(2\pi k/T_u)^2.\tag{12}
\]
For the rank128 quartet example k_max=16 suffices; for its two-grade
counterpart k_max=32 suffices. Every prescribed Gram of rank fitting
this FIXED occupied set is exact at each h and the residual is identically
zero. No uniform-energy theorem for a growing complete AF-RIGHT rank is
inferred. The proof is independent of transverse
grid size and applies when all four physical periods are held fixed.
This is a bounded-energy refining PREPARATION theorem, not the original
raw#216 response theorem or a refining solution of all metric equations.
The choice ℓ=h is the declared refinement chart, not a new clock-forcing
theorem. Other allowed α,β,z schedules leave the preparation criterion
unchanged wherever the original H+J+R functional is defined.

## 5. Actual first field covector of R, not just its eigen-equation

Here the source convention is the original normalized positive R, at the
fixed n chart of §1. Let a=|z−1|² for a normalized single u plane mode,
V the number of sites, w_r=U_r^{-T}q, and δU_r=X_rU_r with
\(X_r^T\eta+\eta X_r=0\). Independent leg variations are equivalent to
the16 coframe variations by v_r=η(e^{-1})_r^T.

For EACH low-grade state ψb0 or ψb1, direct differentiation of (1) gives
\[
\boxed{\delta R_{low}
 =\frac{2\nu a}{\ell^2 V}\sum_x q\cdot\delta v_u(x),
\qquad\delta_{U_r}R_{low}=0\quad\text{for every }r,X_r.}\tag{13}
\]
All three other leg rows vanish; within v_u only the q component appears.
For b0 the link acts trivially
on the scalar before creation. For b1 the baseline D-image has grade0;
the changed raising row has grade2 and is orthogonal, while the lowering
row reaches a scalar before Λ(U)† acts. This proves all24 link rows,
not just variations of the pp-wave profile or its null generators.

There is a stronger POSITIVE source statement for the original R itself.
Hold the coframe and the normalized grade1 state ψq fixed, but vary ALL
proper links arbitrarily in the same open chart. The lowering row stays
link-independent because contraction reaches a scalar before Λ(U)† acts.
The exact raising row is
\[
d_U(\psi q)=\frac{\psi}{\ell}\sum_r
 z_r\,v_r\wedge(U_rq-q).
\]
Its grade2 output is orthogonal to the scalar lowering output. Consequently
\[
\boxed{R_U(\psi q)=\lambda+
\frac1{\ell^2V}\sum_x
\left\|\sum_rz_rv_r(x)\wedge(U_r(x)q-q)\right\|^2.}\tag{13a}
\]
At the pp-wave links the square is exactly zero while curvature can be
nonzero. Thus this genuine native R attains a GLOBAL minimum with respect
to the link variables at this preparation, and its link Hessian is
\[
\frac2{\ell^2V}\sum_x
\left\|\sum_rz_rv_r\wedge(X_rq)\right\|^2\ge0.
\tag{13b}
\]
Grade0 is entirely link-independent. Positive low-grade mixtures inherit
the sum of these squares. No extra transport penalty or fitted coefficient
has been inserted: this is exactly the existing Rayleigh action. It permits
the parallel NULL vector and nonflat pp curvature; the old parallel-TIMELIKE
restriction is not imposed. The square can have additional zero directions
and cancellations. It does not prove unique Levi–Civita transport or a
positive Schur after jointly eliminating preparation, and H+J still have
their own link Hessians. Those are distinct questions.

For EACH high-grade state ψb3 or ψb4, the actual sources are
\[
\delta_vR_{high}
 =\frac{\nu a}{\ell^2V}\sum_x(w_u+q)\cdot\delta v_u,
\tag{14}
\]
\[
\boxed{\delta_UR_{high}
 =-\frac{2\nu}{\ell^2V}\sum_{x,r}
 \operatorname{Re}[(z^{-1}-1)z_r]\,w_r\cdot X_rv_r,
\quad z_u=z,\ z_{v,x,y}=1.}\tag{15}
\]
Every link role r must be retained: identity transverse links can have
nonzero first variation. All off-diagonal first-source matrix entries
between different quartet grades vanish. Hence coherent combinations
retain their full quantum record, but this first R covector depends on
their diagonal low/high weights. No coherence cancellation of (15) is
asserted. For (10) with its φ_a chosen as plane modes, sum these formulas
with the actual weights. In the reference128 construction I128/128,
each real cosine/sine pair has equal weights and is equivalent to the
corresponding two plane-mode density. Unequally weighted real pairs
require their cross-momentum source entries; they cannot use that shortcut.

**Observer source is real and remains.** In the original moving-pairing
convention, a normalized single mode has
\[
\delta_nR=\frac{\lambda}{V}\sum_x q^T\delta h_n(x)q
\tag{16}
\]
for every quartet grade, with the true adjoint and normalization varied.
For the independent uniform boost
\(n(t)=(e^te_++e^{-t}e_-)/\sqrt2\), h_n(t)=diag(e^{-2t},e^{2t},1,1).
The normalized quartet block has energy e^{2t}λ, so on its fixed-Gram
lift R(t)=e^{2t}R(0) and dR/dt=2R. This gives a direct nonzero
observer equation instead of declaring it solved from preparation.
When observer moves, the fixed Gram is the SAME whitened Gram of (9);
raw Ψ†Ψ is not interchangeable with it.

The positive coframe covector (13) is not automatically the Lorentz
Clifford-square null stress of the separate controlled J2 matter owner.
No stress is defined as the residual needed to match Einstein. Equations
(13)–(16) supply the actual native matter contribution for that comparison.

## 6. Exact substitution into the remaining whole-source problem

On the original conditional H+J+R, preparation rows now have an explicit
nonempty curved solution (10). For its low-grade rank128 choice, the
remaining joint equations are concretely
\[
E_U^{H+J}=0,\qquad
E_e^{H+J}+E_e^R\text{ from (13)}=0,\qquad
E_n^{H+J}+E_n^R\text{ from (16)}=0.\tag{17}
\]
Thus no extra matter spin/link source or unknown preparation residual
has to be guessed on this choice. The same source still has to solve
(17). Any actual additional history/preparation/work cost must be included
by its own definition; it is not proved to vanish here.

The exact reducing block also splits spectral traces:
\(\operatorname{Tr}f(\Delta)=\operatorname{Tr}_{\parallel}f(\Delta_\parallel)
+\operatorname{Tr}_{\perp}f(\Delta_\perp)\).
Its first contribution is independent of the pp-wave profile, while the
original H normalizer contains BOTH. The complementary full operator
and its field source must remain; eigenpreparation is not a reason to
drop it. Existing exact AF/Palatini geometry is a consumer only after
this same whole native source is identified or solved.

**Scoped progress:** the original finite curved fixedRIGHT preparation
problem has a constructive solution and explicit true field covector.
Physical native programme selection, additional current/clock constraints,
full curved H+J+R metric/link/observer roots and raw216 remain open.
GR_closed=false.

## 7. Reproduction

The packet [d0_curved_native_preparation_2026-10-20](sources/d0_curved_native_preparation_2026-10-20/README.md)
contains independently derived original-operator checkers. The exact
SymPy replay checks all3072 finite full16 component identities on48sites,
with nonorthogonal proper links, shifted true adjoint and a nontrivial
curvature profile. The numerical source replay checks all16 leg and24
link directions plus3 observer rows at3sites, including every off-diagonal
quartet source entry; it also constructs rank128 fixedRIGHT purifications
inside the original full Hilbert space. Saved outputs and input hashes
distinguish exact identities from floating diagnostics.

No full old heat/feedback, all40 geometric Cartan, Lean, native compiler
or raw216 replay is claimed. The generic proof above supplies the
arbitrary-spacing and refining statements; a small periodic fixture is
not presented as a global Einstein solution.


## 8. 20 October independent joint-critical audit — exact pp-profile SOURCE-FLATNESS and a STRICT rank128 preparation saddle

Independent extension [\`A4D_CURVED_REFERENCE128_FULL_HJR_PROTECTED_SOURCE_AND_PREPARATION_SADDLE_GATE_2026_10_20.md\`](A4D_CURVED_REFERENCE128_FULL_HJR_PROTECTED_SOURCE_AND_PREPARATION_SADDLE_GATE_2026_10_20.md), with replay [\`check_native_reference128_preparation_saddle_and_protected_ward.py\`](sources/d0_curved_native_preparation_2026-10-20/check_native_reference128_preparation_saddle_and_protected_ward.py), strengthens precisely what the preceding positive theorem does—and does NOT—prove.

Because the exact full16 reducing embedding \(J\) and \(\Delta_\parallel\) in (7) are independent of \(H\) and all common-null profile connections, selfadjoint differentiation gives \((D_{H,K}\Delta)J=0=J^\dagger(D_{H,K}\Delta)\) for **every** such variation at fixed observer \(\nu,\ell\). Hence for ANY protected fixedRIGHT preparation \(M=JB\), the genuine Rayleigh source and the entire preparation cross source are exactly zero on those restricted pp-profile directions:
\[
\boxed{D_{H,K}R=0,\quad D_{H,K}D_MR=0,\quad
R(H,K,JB)=\operatorname{Tr}(B^\dagger\Delta_\parallel B),}
\]
constant to ALL orders in \(H,K\) at fixed B. This is NOT a statement that the true R coframe/observer sources of (13) and (16) vanish: the latter remain and must be solved jointly. A valid 10×10 internal IFT/Schur containing only protected pp-profile link variables cannot attribute its curvature selection to R or its preparation cross block; actual H+J must provide that block.

More importantly, a particular **explicit offered** full-rank reference128 preparation from §3 (32 nonzero cosine/sine pairs × low grades b0,b1, \(L_u\ge65\)) is exact preparation-STATIONARY but NOT a full fixedRIGHT **local minimum**. Two native unoccupied k=0 zero-energy modes remain in the same protected sector. Rotating any occupied positive-energy Fourier vector \(\phi_k\) into such an unoccupied \(\phi_0\) with one actual LEFT-unitary yields a full-Hilbert valid preparation with SAME \(\Sigma_R=I_{128}/128\) and
\[
\boxed{R(\theta)=R(0)-\tfrac{\lambda_k}{128}\sin^2\theta,\qquad
R''(0)=-\lambda_k/64<0.}
\]
With \(h=T_u/L_u\), the negative direction remains bounded away from zero in the fixed physical-period refinement: \(R''(0)\le-\nu^2/(4T_u^2)\) for k=1. H+J is independent of M on the conditional owner, so this is a genuine preparation **saddle direction** of the full conditional H+J+R when there is NO separately selected M-dependent work/constraint. It does not invalidate stationarity or an IFT with an **indefinite** genuinely invertible internal block; it invalidates claims of a positive-minimum \(H_{MM}\) / stable Schur for this particular preparation without actually paying a selector.

The same reasoning applies to the §3 nonzero-only quartet rank128 option with four unoccupied zero modes when \(L_u\ge33\), but **NOT** automatically to the fully occupied \(L_u=32\) quartet block (where no unused protected k0 exists and the full complement must be checked). At \(L_u=2\), the protected quartet carries only 8 dimensions, low grades only 4: neither is the same 128-rank protected execution as the original \(L=2\) 16-site/640-Euler Golden fixture. A curved rank128 finite joint solution must supply its actual \(L_u\), complete reference rank, other grades, boundary collar and admissible full preparation orbit; numerical 10-variable roots may still exist but do not bypass this exact capacity requirement.

Therefore this owner is a robust constructive **stationary preparation** theorem, not a selected stable curved Einstein root. Real physics continues to require: chosen full Book H+J+R+oldRIGHT/clock/Cost-price action, all observer/coframe/link Euler, full z critical quotient, fixed source before candidate and h-uniform raw216 refinement. \`GR_closed=false\`.


## 9. Exact joint coframe-PREPARATION Fredholm test for curved reference128, not only rank/gauge and energy

The consumer [\`A4D_CURVED_REFERENCE128_FULL_HJR_PROTECTED_SOURCE_AND_PREPARATION_SADDLE_GATE_2026_10_20.md\`](A4D_CURVED_REFERENCE128_FULL_HJR_PROTECTED_SOURCE_AND_PREPARATION_SADDLE_GATE_2026_10_20.md) §VII now computes a concrete missing **mixed full native source**. In the actual grade0 positive-adjoint D0 operator, on original u-periodic constant-transverse modes and local inverse-leg variation \(v_u(x)=\nu_x q\), one has the *literal* R quadratic form \(\sum_x\nu_x^2|(\psi(x+1)-\psi(x))/h|^2\). At the rank128 minimum's partially filled \(k=32,L_u=65\) cutoff, choose occupied real \(\cos\) Fourier state \(\phi_c\) and unoccupied equal-energy \(\sin\) state \(\phi_s\). The physical LEFT reference-preserving mixing θ has \(R_{\theta\theta}=0\) at the uniform coframe, but a **single genuine local independent coframe-leg** perturbation \(\nu_x=\nu+\epsilon\mathbf1_{x=0}\) yields
\[
\boxed{
R_{\theta\epsilon}
=\frac{\nu}{16L_uh^2}
 (\cos(2\pi\cdot32/L_u)-1)\sin(2\pi\cdot32/L_u)\ne0.
}
\]
The independent original-stencil checker \`sources/d0_curved_native_preparation_2026-10-20/check_native_coframe_reference128_fredholm_failure.py\` replays the value \(-0.16249816824022978...\) for an explicit positive finite chart, with the SAME unchanged fixedRIGHT Gram. Consequently, the linearized preparation Euler \(R_{\theta\theta}\theta'+R_{\theta\epsilon}=0\) is IMPOSSIBLE for a C¹ stationary preparation continuation **through that chosen** cutoff projector under that independently prescribed local coframe perturbation. This is the Fredholm compatibility condition missing from a curvature-only 10×10 inverse, not a no-go for an alternate preparation projector, constrained observer/coframe boundary or a full physically selected extra M-dependent source.

The pp-H,K protected mixed block itself remains identically zero to all orders (owner (7), research consumer §I), so a pure pp-profile curvature variation is not affected by this particular obstruction. The true full sixteen-coframe and three-observer-source equations of (13)–(16), the actual recorded RIGHT128 and actual collar/boundary operators must be evaluated at the SAME finite joint solution. Literal fixed Dirichlet collars need a new boundary-invariant proof before transporting periodic Fourier rank128 theorems. The result strengthens, rather than rescinds, the valid positive **preparation stationarity** constructed in §§1–7; G0 physical selected complete H+J+R and uniform raw216 GR remain OPEN.


## 10. Whole original fixedRIGHT reference128 source: exact non-C¹ Rayleigh minimum with coframe deformation after the saddle repair

The positive statement §§1–7 (exact protected curved stationary reference128) is correct; it does NOT select the actual M among all its mathematically stationary fixedRIGHT amplitudes. §§8–9 show explicit unstable nonzero-frequency occupation and an original mixed coframe–preparation Fredholm obstruction for a degenerate cutoff minimizer. The independent [full finite/continuum source theorem](A4D_REFERENCE128_LOWEST_SPECTRAL_SELECTION_NONC2_CUSP_FINITE_TO_REFINEMENT_2026_10_20.md) proves a still sharper distinction for the natural candidate **global lowest-128 Rayleigh minimizer inside the protected low2 original carrier**: on a fixed smooth physical coframe Fourier deformation \(\nu(u)=\nu+\epsilon\cos(4\pi32u/T)\), the actual minimum value has a native nonzero \(-\nu q_h|\epsilon|/64\) cusp, \(q_h\to(2\pi32/T)^2\), and two one-sided true LEFT prepared densities differ in trace norm exactly \(1/32\) despite SAME faithful RIGHT128 Gram. This is a genuine impossibility of continuous two-sided LOWEST-R selection under this admitted smooth coframe perturbation — stronger than merely "not positive-definite Hessian". The explicit original shifted positive-adjoint grade0/grade1 \(D_{\rm prot}=[[0,B^\dagger],[B,0]]\), \(B=M_\nu(S-I)/h\), all k32 cutoff source matrices and full finite spectra were independently replayed. This is scoped to the same periodic protected-low2 programme and does not judge a different full16 prepared state, physical extra M-dependent G0 work, or nonperiodic fixed boundary. No full curved physically selected Einstein–CAR solution is claimed. \`GR_closed=false\`.
