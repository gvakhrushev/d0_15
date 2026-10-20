# P25/P34: exact native reference128 lowest-energy selection has a CUSP in the true coframe Euler — surviving fixed-period refinement

**20 October 2026. NEW EXACT NATIVE-SOURCE COUNTERTERMINAL FOR A PRECISELY SPECIFIED SELECTOR, not a no-go for all D0 / conditional full H+J+R.** Input original #334 \`A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md\` §§1–5 (literal full16 exterior Dirac + true positive adjoint), \`A4D_CURVED_REFERENCE128_FULL_HJR_PROTECTED_SOURCE_AND_PREPARATION_SADDLE_GATE_2026_10_20.md\` §§I–VII (true fixedRIGHT preparation saddle, protected pp null and local coframe Fredholm). All statements below are exact mathematical consequences of the ORIGINAL **protected low-two-grade** native Dirac reduction and its fully admitted fixedRIGHT rank128 orbit. They do not assert that G0 physically selects that orbit, its R-only minimizer, or even a periodic boundary in the user-reported fixed-collar curved 10-variable problem. GR_closed=false.

## 1. Why the natural "repair the saddle by picking the lowest 128" fails a different, STRONGER full-source test

The prior owner proves the explicitly offered rank128 preparation occupying **all 128 NONZERO Fourier modes** in the original two protected grades at \(L_u=65\) is a stationary SADDLE: two unoccupied true zero modes lower R, and this is an allowed full LEFT fixedRIGHT rotation. One might try to repair the physical criterion by choosing the **global 128 lowest eigenstates** of the same original positive Rayleigh action, with fixedRIGHT Gram \(\Sigma_R=I_{128}/128\). The exact Ky Fan variational principle makes that mathematically canonical inside the declared two-grade protected subspace:
\[
R_{\min}(\nu_x)=\frac1{128}\sum_{j=1}^{128}\lambda_j(\Delta_{\rm protected}(\nu_x)),\quad \lambda_1\le\cdots\le\lambda_{2L_u}.
\tag{1}
\]
It remains an OPTIONAL mathematical selector until D0's actual M1/G0/oldRIGHT programme forces and pays it.

For any odd original u-periodic grid \(L=L_u\ge65\), spacing \(h=T/L\), original positive observer, and a constant transverse pp block, the original two protected Fock grades \(b_0=1,b_1=q\) have literal real native
\[
D_{\rm prot}(\nu_x)=
\begin{pmatrix}0&B_{\nu}^\dagger\\B_{\nu}&0\end{pmatrix},
\quad B_\nu=M_\nu\delta_h,\quad
\delta_h=\frac{S_u-I}{h},\quad (M_\nu f)(x)=\nu_x f(x),
\tag{2}
\]
and
\(\Delta_{\rm prot}=\operatorname{diag}(B_\nu^\dagger B_\nu,B_\nu B_\nu^\dagger)\).
The TWO blocks have exactly the same full nonzero spectrum (singular-value identity). This is not a replacement by a toy Laplacian: it is the actual original grade0/grade1 subblock of the full16 positive-adjoint Dirac, with the exact field-dependent inverse-u coframe leg; the remaining 14 grades still exist.

At \(\nu_x\equiv\nu>0\), both blocks have eigenvalues
\[
\lambda_{k,h}=4\nu^2h^{-2}\sin^2(\pi k/L),\quad k=0,\ldots,L-1.
\tag{3}
\]
The total rank128 lowest-energy cutoff has: two exact grade-zero \(k=0\) states, all four real states for \(1\le k\le31\) (124 states), and TWO of the FOUR exactly degenerate \(k=32\) states. Rank count \(2+4(31)+2=128\). Therefore the native minimizer has a fourfold cutoff with a real \(\mathrm{Gr}(2,4)\) choice, exactly as previously owned, and the minimum VALUE need not be differentiable when the fourfold energy splits.

## 2. EXACT ORIGINAL FOUR-BY-FOUR SOURCE: a SMOOTH nonconstant coframe variation splits the cutoff in BOTH signs

Use ONE admitted real coframe-leg field chart (all other original inverse legs remain unchanged), with a fixed continuum Fourier frequency:
\[
\boxed{
\nu_x(\epsilon)=\nu+\epsilon\cos\frac{4\pi kx}{L},
\qquad k=32,\qquad |\epsilon|<\nu.
}\tag{4}
\]
This is the restriction of the SAME smooth macroscopic physical profile
\(\nu(u,\epsilon)=\nu+\epsilon\cos(4\pi k\,u/T)\)
to every grid \(h=T/L\); its spatial frequency \(2k=64\) is FIXED under refinement. This is NOT a single-site delta impulse whose influence might disappear as \(L\to\infty\). Its local u-leg variation corresponds to a genuinely invertible original coframe neighborhood around the base, and requires no new source field or coupling.

Set \(w=2\pi k/L\), \(q_h=4h^{-2}\sin^2(w/2)\), and let \(E_k=\operatorname{span}_\mathbb R\{\sqrt{2/L}\cos(wx),\sqrt{2/L}\sin(wx)\}\). For all odd \(L\ge65\), elementary exact discrete Fourier orthogonality (no 2k/4k alias) gives
\[
\left.W\right|_{E_k}\ \sim\ \frac12
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\qquad W(x)=\cos(2wx).
\]
The first perturbation of the TRUE grade0 block is \(2\nu\delta_h^\dagger W\delta_h\). Since \(\delta_h\) is \(\sqrt{q_h}\) times a **rotation** on \(E_k\), this compressed 2×2 perturbation has eigenvalues \(\pm\nu q_h\). The corresponding grade1 first perturbation is \(\nu(W\,\delta_h\delta_h^\dagger+\delta_h\delta_h^\dagger W)\), which likewise compresses to eigenvalues \(\pm\nu q_h\). Therefore the original FOUR cutoff-mode first-order source matrix has the EXACT spectrum
\[
\boxed{
\operatorname{spec}(D_\epsilon\Delta_{\rm cutoff})
=\{-\nu q_h,-\nu q_h,+\nu q_h,+\nu q_h\}.
}\tag{5}
\]
NO mass normalization, fitted price, missing 14-mode truncation or continuum simulation is used in this exact finite-dimensional first-order source result. The four-dimensional first-source block is an unavoidable part of the **declared protected two-grade rank128** programme; whether the full physical source selects this programme is independently open.

For \(\epsilon>0\) the minimum rank128 chooses both NEGATIVE-slope cutoff states. For \(\epsilon<0\) it chooses both POSITIVE-slope states. All 126 lower occupied modes have separated eigenvalues and contribute the SAME analytic first derivative from both sides. Thus their presence cannot cancel the CUT-OFF source jump:
\[
\boxed{
R_{\min}'(0^-)-R_{\min}'(0^+)
=\frac{4\nu q_h}{128}=\frac{\nu q_h}{32}>0.
}\tag{6}
\]
Equivalently, with \(A_h\) the smooth common first source contribution,
\[
\boxed{
R_{\min}(\epsilon)
=R_{\min}(0)+A_h\epsilon
-\frac{\nu q_h}{64}|\epsilon|+O(\epsilon^2).
}\tag{7}
\]
The finite original MINIMIZED scalar R is continuous and Lipschitz but **NOT C¹**, hence no ordinary C² geometry Hessian or standard smooth stationary Schur exists on this selected minimization prescription AT THE EXACT UNIFORM BACKGROUND.

## 3. A REAL continuum/refinement obstruction, not a vanishing single-cell alias

Take fixed physical u-period \(T>0\), fixed original occupied cutoff index k=32, and any odd refining sequence \(L\to\infty\), \(h=T/L\). Because \(\sin(\pi k/L)\sim \pi k/L\):
\[
\boxed{
q_h=\frac{4}{h^2}\sin^2(\pi k/L)
\longrightarrow \left(\frac{2\pi k}{T}\right)^2,\qquad
\frac{\nu q_h}{64}\longrightarrow
\frac{\nu}{64}\left(\frac{2\pi k}{T}\right)^2>0.
}\tag{8}
\]
Thus the nondifferentiable \(-|\epsilon|\) term **survives with a strictly positive coefficient** in the true fixed-physical-period refining family for ONE smooth physical coframe profile, rather than disappearing as the lattice gets finer. The owner already bounds the protected R eigenenergies uniformly when occupied mode k is fixed, so this is compatible with the existing energy-refinement theorem; it obstructs the **differentiability of the MINIMIZED effective action**, not bounded energy itself.

**Independent original full finite-spectrum numerical regression** (not the theorem's proof) replays actual \(B_\nu\), \(B^\dagger B\) (and duplicated nonzero grades) at \(L=65,131,257\), parameters \(\nu=7/10,T=13/10\). The EXACT source matrix cutoff eigenvalues are \(\pm\nu q_h\) each twice. The measured left-minus-right derivatives of the complete rank128 minimum converge, respectively, to the exact finite positive values \(218.6222748098\), \(428.2791094976\), \(497.1137734676\), as the field step tends to zero. The true asymptotic cusp magnitude tends to \(261.6321166679\) (fixed \(k=32,T=1.3,\nu=.7\)), not zero. No unverified numeric ten-variable curved IFT root is used.

## 4. What precisely this closes — and what it DOES NOT

**Exact negative terminal on one very tempting action-selection completion:** claiming that the true physical selected preparation should be the 128 **lowest** eigenmodes of the already-owned positive original R, with no extra M-dependent H/J/native prep cost, does NOT provide a smooth \(\mathcal C^2\) effective action at a uniform pp background on the declared protected two-grade chart, even though it fixes the earlier nonminimal-saddle problem. The obstruction is the exact ORIGINAL cutoff eigenvalue crossing (5), and persists on the fixed-period refinement via (8). No C² selected Einstein–CAR field source or smooth Schur can be inferred from that minimizer without handling its nonsmooth projection/spectral kink or proving an additional physical selector.

**Different legitimate outcomes remain OPEN:** (i) a specific signed/charged original G0/M1/oldRIGHT preparation rule breaks the \(k=32\) tie at the physical source reference and yields a smooth physical branch, (ii) the actual full16 selected preparation includes different grades and sources, (iii) a true constrained fixed-boundary programme excludes the smooth coframe perturbation (4), (iv) a fully admitted critical-stationary **saddle** with an honest invertible larger mixed Hessian and Lyapunov–Schmidt compatible source is selected, or (v) the real physical theory does not minimize R over this protected subspace at all. NO choice may be made simply to hide the kink. The old 10×10 finite curved IFT of the user, if true, proves only what its actual full admitted jacobian and boundary conditions cover; this theorem neither refutes nor verifies that branch.

**Exactly requested next physical gate:** within ONE selected original H+J+R at fixedRIGHT rank128 and genuine oldRIGHT/programme price, write the ACTUAL projector/state occupation at the k32 band edge and test its true mixed Euler response to the smooth coframe perturbation (4). If it claims a positive/minimizing Schur, the source must remove or physically resolve (5) with real measured work. If it claims a saddle/conditional IFT, show the full Fredholm projection and constraint tangent instead of treating a singular prep-only block as invertible. Then, independently, include all 16 coframe/24 links/observer stress, actual Einstein source and uniform #216/RAW refinement. GR_closed=false.

**Exact finite source derivation + independent full spectral checks:** \`sources/d0_curved_native_preparation_2026-10-20/check_native_reference128_lowest_cutoff_cusp_and_refinement.py\`. It replays the original periodic \(B=M_\nu(S_u-I)/h\) and 2×2+2×2 compressed cutoff matrices with all finite positive energies; finite-difference CUSP is used only to witness the already exact algebraic source jump. No new Lean owner for this theorem yet.
