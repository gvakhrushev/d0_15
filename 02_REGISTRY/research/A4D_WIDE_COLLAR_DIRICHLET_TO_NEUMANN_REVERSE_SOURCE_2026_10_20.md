# D0 -> GR: exact-source reverse test from the seven-slice HJR collar

20 October 2026. Research-only, inside existing Draft #334 (EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE), with no new task, action, claim or physical selection. This note is a **new bounded consumer of existing, independently reviewed finite Arb data**, not an independent replay of the 65,536-state spectral operator. The available file-level interval certificates and the finite-dimensional analytic IFT together give the result below.

## 1. The question is a boundary source, not a new Einstein tensor

The owner A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md, sections 1-10, proves an exact analytic nonflat family for the **same full conditional H+J+R** on the L8 carrier. The interior has time slices 0,...,6, all coframe, incident proper-link, observer Ward and exact Riesz reference128 preparation equations; time slice 7 has a prescribed isotropic spatial-coframe deformation and fixed spatial links. Exterior equations and physical Cost-Info selection remain open.

Rather than attempt another root search or assume that a fixed collar solves its own free equation, calculate the **actual remaining Euler traction** after solving the original interior variables. This is the reverse-source datum a physical native history/clock/archive boundary relation would have to reproduce or replace.

The original action is

\[
 S=\frac{\log(CZ)}{\beta}-128\operatorname{Tr}_{H}\log F
     +\operatorname{Tr}(M^*\Delta M),
\quad
 Z=\operatorname{Tr}_{H}(1-\alpha\Delta)^m,\quad
 F=1-z+z(1-\alpha\Delta)^m .
\]

Its original full CAR16, 4096 momenta, full thermal complement, global normalizer, moving spectral Riesz reference128 preparation, observer and all incident proper Lorentz links are retained. No scalar Palatini action, physical work or archive price has been substituted.

## 2. The exact 64+1 analytic reduced Hessian

Use the owner's invariant coordinates: nine interior coframe/outgoing-link coefficients on each of seven slices, plus the incoming time-link coefficient at slice 7. This is x in R^64. Prescribe the sole exterior variable epsilon by
\(V(7,\epsilon)=(I+\epsilon I_{\rm sp})V_0\).
All other exterior coframes and spatial links stay fixed. The finite averaging/Ward/Riesz arguments establish every unrestricted **interior** Euler equation for the analytic solution x(epsilon).

At the EXACT owned flat root, the full reduced Hessian in (x,epsilon) is

\[
 D^2S_{\mathrm{red}}(0,0)
 =\frac18\begin{pmatrix}A&b\\b^\top&C\end{pmatrix},
\]

with A the owner's certified 64-by-64 principal compression, b the owner's certified 64-by-1 boundary column, and

\[
 C=H(0)_{2,2}=\frac18\big[K_9(0)_{2,2}
       +2K_9(1)_{2,2}+2K_9(2)_{2,2}
       +2K_9(3)_{2,2}+K_9(4)_{2,2}\big].
\]

These definitions use the **same K9 symbol**, component labels and Fourier normalization as the owner. In particular the incoming time-link at slice 7 is **inside** A, not erroneously fixed outside. The full site count and normalization are unchanged.

The owner's independently accepted bound \(\|I-RA\|_\infty<3/1000\) proves A invertible. Its 64-decimal response x0 and rigorous preconditioned error satisfy

\[
 x'(0)=-A^{-1}b,\qquad \|x'(0)-x_0\|_\infty<1/100.
\]

The analytic effective boundary action is \(S_{\rm eff}(\epsilon)=S_{\rm red}(x(\epsilon),\epsilon)\). Differentiating the true interior Euler equations gives the Dirichlet-to-Neumann Schur formula

\[
 \boxed{\;
 S_{\rm eff}''(0)=\frac18\mathcal K_\partial,\quad
 \mathcal K_\partial=C-b^\top A^{-1}b
                  =C+b^\top x'(0).
 \;}
\]

The equality is analytic and exact; it does not assume positivity of A, which indeed has negative directions.

## 3. New rigorous consequence of the EXISTING published intervals

Source data, fixed original paths in the existing #334 branch:

- sources/d0_curved_whole_hjr_collar_2026-10-20/COLLAR_HESSIAN_ARB.json, accepted K9 interval enclosure, SHA256 a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4;
- sources/d0_curved_whole_hjr_collar_2026-10-20/WIDE_COLLAR_ARB.json, accepted full 64-by-64 preconditioner and x0 response, SHA256 dee20425e01aeba2f090a55e2b1d221d57160a667eff9240a1c58368cd87e305.

Parse **the printed interval midpoints/radii as exact rational decimals**, not rounded floating point eigenvalues, and bound the desired scalar directly:

\[
 |\mathcal K_\partial-(C_{\rm mid}+b_{\rm mid}^\top x_0)|
 \le C_{\rm rad}+\sum_i b_{i,\rm rad}|x_{0,i}|
        +\frac1{100}\sum_i (|b_{i,\rm mid}|+b_{i,\rm rad}).
\tag{1}
\]

No broad re-inversion or full thermal replay enters this one-scalar conclusion. Evaluating (1) on the original fields:

\[
\begin{aligned}
 C_{\rm mid}&=3.434354467500000\ldots,\qquad
 C_{\rm rad}\le 3.129625\cdot10^{-8},\\
 b_{\rm mid}^\top x_0&=-3.161297078005912\ldots,\\
 \sum_i b_{i,\rm rad}|x_{0,i}|&\le 1.301\cdot10^{-6},\\
 \sum_i (|b_{i,\rm mid}|+b_{i,\rm rad})&<21.546.
\end{aligned}
\]

A strictly conservative RATIONAL enclosure is therefore

\[
 \boxed{\qquad \frac{57}{1000}<\mathcal K_\partial<\frac{49}{100}.\qquad}
\tag{2}
\]

The all-decimal rational calculation yields a narrower diagnostic enclosure approximately \((0.05759828,0.48851650)\) and central value \(0.273057389494\). The margin to each rational endpoint in (2) is much greater than the parser/printing precision and is already covered by the source-ball radii.

In particular the response is **strictly nonzero and positive** after allowing **all 64 interior variables** to respond, despite the conditional action having nongauge negative Hessian directions in that interior. The full original boundary Euler derivative is

\[
 \boxed{\qquad
 \partial_\epsilon S_{\rm eff}
   =\frac{\mathcal K_\partial}{8}\epsilon+O(\epsilon^2).
 \qquad}
\tag{3}
\]

The IFT supplies a genuine analytic family, so (2)-(3) imply: for each sufficiently small nonzero epsilon the free boundary equation in **this one-parameter exterior direction** is not solved. This does NOT prohibit other joint exterior deformations, boundary-value Einstein solutions, field sources or a different physically admitted native action.

## 4. Reverse GR interpretation: what an actual same-history source must do

This traction is a **computed target for a junction/source identification**, not an instruction to add a counterterm. If the physical complete Book03 Cost-Info of the SAME execution has an additional genuine paid component \(E\), and if the physical stationary branch uses the **same** x(epsilon), then necessarily its real interior variation obeys \(D_xE(x(\epsilon),\epsilon)=0\), and the free-collar Euler equation requires

\[
 \partial_\epsilon E(x(\epsilon),\epsilon)
 =-\frac{\mathcal K_\partial}{8}\epsilon+O(\epsilon^2).
\tag{4}
\]

At the base, the required archive/clock/work traction has **negative linear coefficient**, with magnitude strictly bounded between \(57/8000\) and \(49/800\) in the original reduced normalization. This is a *conditional necessary test*, NOT a fitted physical source. If E also moves the interior root, its complete joint Hessian and Schur complement must be computed instead: (4) is NOT a universal equation for any E.

For a literally admitted one-sided Perron cylinder, the earlier original-history owner supplies its full unnormalized-to-normalized score including the pressure and endpoint:

\[
 D\log \mathbb P(\gamma)
 =-(\log\varphi)\sum_{e\in\gamma}Ds_e
  -N D\log\rho+D\log r(v_N).
\]

For every **fixed fully recorded observable** O, its exact source is
\(D\mathbf E O=\mathbf E[(O-\mathbf E O)D\log\mathbb P]\).
An honest physical use of (4) must differentiate the actual full record/Book value **including all feedback, oldRIGHT, preparation, work, reference, observer and clock sources** and prove an actual same-carrier map to the coframe boundary tangent. Merely reading a feedback scalar J from one 718-edge history cannot supply the signed boundary force.

There is an independent on-shell/off-shell warning: the unchanged complete conditional H+J+R has a separately proved **nonzero coframe gradient along flat-holonomy, Palatini-density-zero frames** (d0_hjr_flat_density_zero_2026-10-20/RESULT.md). Hence (4) cannot be satisfied simply by declaring the full HJR action to be a function only of the original six-face curvature densities and invoking an invertible squared-ideal dressing. The flat pressure is a real source of the existing action and must be accounted for.

## 5. Correct consuming step, without another loop

The existing main #386 foundation/operational-transfer theorem already handles the generic record/process diagram. The exact Palatini/Einstein tensor and its 40-row geometric representation are also available. The next ONE physical substitution is:

1. choose the **same admitted full execution** whose whole Cost−Info is supposed to select geometry;
2. compute its real first source/score on the above fixed-collar perturbation and its full interior equations; 
3. map them to the actual coframe/link/observer/reference128 source and compare against the computable traction (2)-(3);
4. only then pursue genuinely compatible fixed-width smooth collars and an h-uniform full-joint inverse/refinement estimate.

A separately composed counter-source, new clock, fictitious condition, reweighted original outcomes or a new physically selected action is not a solution. The existing exact seven-slice branch remains a valuable finite **stationary** curved geometry, not a strict prospective minimum; the already accepted negative Hessian direction proves the distinction. Nothing here solves the exterior/full-periodic physical root, proves native admission or source equality, establishes a uniform GR limit, discharges raw216 or promotes any Book/claim. **GR_closed=false**.

## 6. Reproduction

Independent of any root search, an exact-decimal rational checker can read the two saved JSON files, combine the five q-symbol diagonal balls and all 64 response / boundary balls, use the published uniform response error 1/100, and verify (1)-(2). The result needs no new eigenvalues or elimination certificate. It can be run with ordinary decimal/rational arithmetic using only those preserved input arrays; the scalar check above was independently evaluated with exact BigInt rational arithmetic, with both inequalities in (2) returning true. The **source Hessian/IFT certificates are reused, not relabeled as newly reproduced**.

Status: bounded algebraic consequence and strategic source target inside existing research Draft #334; independent publication/acceptance of this new bound has NOT yet occurred.
