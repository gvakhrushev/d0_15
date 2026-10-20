# D0→GR: native full128 port is field-score redundant but CODE-price relevant — exact source recovery from counts

**19 October 2026 / EXISTING ORIGINAL FULL128 RETAINED INSTRUMENT / bounded research consumer within Draft #334.**
Use only [actual complete 128-channel first-source owner](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) §§3,6–9 and its [original J23 port-price split](A4D_NATIVE_FULL128_J23_PORT_SOURCE_SPLIT_AND_PHYSICAL_COARSE_READOUT_2026_10_19.md), not any new instrument. Source type: ORIGINAL complete 128 pointer per round with all future/RIGHT/ref128 retained. **This is neither the separate k-Golden Slater filled-return detector nor the compulsory physical Book03 action.** No full D0→GR claim.

## 1. EXACT factorization of the complete tape, with no missing port or future

In one genuine original 128-outcome round, for EVERY nonblank original label/coefficient \(k\), the two existing physical port Kraus operators are proportional to the SAME original data operator \(L_k\). The exact owner gives

\[
K_{0k}=pL_k,\qquad K_{1k}=aL_k,\qquad
r=(r_0,r_1)=(p^2,p),\quad p=\varphi^{-1},\quad p^2+p=1.
\]

Their normalized post-outcome data state and every future conditional distribution are **identical** at fixed \(k\), regardless of port. Their actual primitive Golden port code has reference \(\mu_{\mathrm{port}}=(p,p^2)\), distinct from actual \(r\).

Define a precise **reduced retained label record** \(\eta(\gamma)\) that forgets ONLY which port was recorded at each NONBLANK label/coefficient; it keeps the exact label, its order, every special blank-label/port0 and blank-label/port1 outcome *separately*, all other original record coordinates, the original full tape physically stored, and the fixed round clock. This is a deterministic readout of the existing complete original pointer tape; it is not a new POVM or a deletion of the physical archive. (Directly measuring a new coarse projector, instead of first recording the complete tape, would be a different instrument.)

For every original positive full tape \(\gamma\) and corresponding \(\eta\), the *actual measured* field-dependent probability factorizes:

\[
\boxed{
q_y(\gamma)=\bar q_y(\eta)
\prod_{j\in {\mathsf{nonblank}}(\eta)}
r_{\mathrm{port}_j},\qquad
r=(p^2,p)\ \text{field independent}.
}\tag{1}
\]

Proof: at each nonblank event the two Kraus outputs differ only in scalar factors; conditional data after the label is port-independent. Induction over the entire recorded future gives the product, even if the data undergoes noncommuting other Kraus operations on intervening steps. **No classical iid label assumption** or loss of original future history is needed. Special blank ports are not factored.

## 2. The FIELD Fisher information lost by forgetting ONLY this native port is exactly ZERO

Let \(V,W\) be any true smooth coframe, link, scalar, preparation or fixed-cut controller tangents on a positive-history support chart of the same original instrument (p and the discrete code held fixed). Then (1) gives for every fine history

\[
D_V\ln q(\gamma)=D_V\ln\bar q(\eta(\gamma)).
\tag{2}
\]

Hence the complete classical score is ALREADY measurable in the reduced label record. The full Fisher bilinear form on this chart is exactly

\[
\boxed{
\mathcal I_{\rm full}(V,W)
=\sum_\gamma q_\gamma(D_V\ln q_\gamma)(D_W\ln q_\gamma)
=\sum_\eta\bar q_\eta(D_V\ln\bar q_\eta)(D_W\ln\bar q_\eta)
=\mathcal I_{\rm reduced}(V,W).
}\tag{3}
\]

No claim is made about Fisher regularity at a parameter point where a formerly dark probability first becomes positive; (3) applies on fixed positive support and by controlled limits as permitted. Coarse-graining further to a binary OR-of-exit event is NOT covered by (3). Likewise (3) does not imply equality of Book price, coherent information or absolute source.

This is a sharply positive result about the **real original** detector: one need not physically observe the nonblank port to retain *its full classical information about an admitted smooth field parameter* given the detailed label tape. It is NOT a theorem permitting the port record or its cost to be deleted from D0.

## 3. The same redundant port has a fixed, NONZERO original Cost−Info source, exactly recoverable from observed count

The original reference conditional port code is \(\mu=(p,p^2)\), while actual probabilities are \(r=(p^2,p)\). Exact golden arithmetic gives

\[
\begin{aligned}
\mathbb E_r C_{\rm port}&=p^2+2p=1+p,\\
H_\varphi(r)&=2p^2+p=2-p,\\
\boxed{D_\varphi(r\Vert\mu)}&=
p^2\log_\varphi p+p\log_\varphi(1/p)
=p-p^2=p^3=2p-1>0.
\end{aligned}\tag{4}
\]

Now apply the SAME complete-history chain rule with original code reference. If \(N_{\rm nz}(\eta)\) is the number of actual nonblank LABEL occurrences in the port-forgotten recorded label tape (not an invented new count), exact conditional factorization of BOTH q and code yields

\[
\boxed{
D_\varphi(q_{\rm full}\Vert\mu_{\rm full})
-D_\varphi(\bar q\Vert\bar\mu)
=p^3\mathbb E_q N_{\rm nz};
}\tag{5}
\]

and the exact complete pointer Shannon difference is

\[
\boxed{
H_\varphi(q_{\rm full})-H_\varphi(\bar q)
=(2-p)\mathbb E_q N_{\rm nz}.
}\tag{6}
\]

These are exact VALUES on the full complete stored tape, not arguments that the full Book action equals either KL or Shannon. Their genuine field/preparation source in ANY differentiable direction V is

\[
\boxed{
D_V\Delta\mathrm{KL}=p^3 D_V\mathbb E N_{\rm nz},
\qquad
D_V\Delta H=(2-p)D_V\mathbb E N_{\rm nz}.
}\tag{7}
\]

**Key source reconstruction:** the ENTIRE native original port information correction can be reconstructed from **one already observed reduced-tape statistic** \(N_{\rm nz}\), with the original *fixed* coefficient \(p^3\), even though the hidden fine port is not measured. No new external port oracle, independent experiment, fit, or compensating counterterm is required for this *accounting identity*. The underlying fine record still exists and its primitive Cost remains physical. This solves a typed data-reduction/readout-source interface, **not** its full Book action selection.

The actual arbitrary finite-depth derivative of \(\mathbb E N_{\rm nz}\) uses the ALREADY owned complete recycled-channel recursion, including differentiated intermediate states and return operators:

\[
\begin{gathered}
\rho_{j+1}=\Phi_h(\rho_j),\quad
D\rho_{j+1}=\Phi_h(D\rho_j)+(D\Phi_h)(\rho_j),\\
D\mathbb E N_{\rm nz}
=\sum_{j<n}\mathrm{Tr}\big[(D E_{\rm nz})\rho_j+
E_{\rm nz}D\rho_j\big],\\
E_{\rm nz}=\epsilon_h\Delta_h(I-h^2\Delta_h/256).
\end{gathered}\tag{8}
\]

One MUST NOT replace (8) with \(n\,D\mathrm{Tr}(E_{\rm nz}\rho_0)\) on arbitrary J23/curved directions. For genuine flat scalar-shell-preserving variations only, the existing closed form becomes
\(\mathbb E N_{\rm nz}=\beta_h\lambda_h(1-h^2\lambda_h/256)\) and its derivative follows directly.

## 4. One original J23 cross-check: both hidden port sources reproduced without running 128 matrices again

On the actually pinned original one-round L=4,h=1/4,J23 test,

\[
DP_{\rm nz}=
\frac{-42957+14319\sqrt5}{5120000}
=-0.0021364731699571311205\ldots .
\]

Using only original p and this original source, (7) reproduces both independently reported complete native quantities:

\[
\boxed{
\begin{aligned}
D_{J23}\Delta\mathrm{KL}
&=p^3 DP_{\rm nz}
=-0.0005043529002143444\ldots,\\
D_{J23}\Delta H
&=(2-p)DP_{\rm nz}
=-0.0029525333048285245\ldots .
\end{aligned}}\tag{9}
\]

These are the EXACT old J23 hidden-port code- and entropy-source components, not a fitted new geometric effect. **Fisher equality (3) coexists with nonzero original CODE-information source (9).** Sufficiency for statistical FIELD inference does not imply sufficiency for native historical price.

## 5. A hostile opposite example: binary any-exit readout is NOT score-sufficient

The companion [full128 history-class MAP inversion](A4D_FULL128_NATIVE_MEMORY_CLASS_MODAL_INVERSION_AND_SOURCE_2026_10_19.md) is a different, much coarser statistic: merely asking whether ANY exit from blank-port0 occurred in n rounds.

On the original flat first-shell scalar-intensity family, the actual exit indicators are iid Bernoulli with \(e=1-q_0\), \(q_0=(1-\epsilon\lambda/2)^2\), as proved by the original full-channel owner. The full EXIT COUNT \(K\sim\mathrm{Bin}(n,e)\) has Fisher information in \(\lambda\)

\[
I_K=n\frac{(De)^2}{e(1-e)};
\]

the binary OR statistic \(\mathbf 1_{\{K\ge1\}}\) has
\(P_{\rm hit}=1-(1-e)^n\), hence the exact ratio is

\[
\boxed{
\frac{I_{\rm OR}}{I_K}
=\frac{ne(1-e)^{n-1}}{1-(1-e)^n}
\ \xrightarrow[n\epsilon\to\beta]{}
\frac{\beta\lambda}{e^{\beta\lambda}-1}
<1 \quad(\beta\lambda>0).
}\tag{10}
\]

At the original L=4, h=1/4, n=1024 first-shell BASE, this ratio equals
**0.0545955509471...**: the OR class retains only about **5.46% of the
CLASSICAL COUNT Fisher information about this scalar shell-intensity
parameter**, not 5.46% of all128 field Fisher information and NOT an
established ratio for the genuine spatial J23 tangent, which may leave
the scalar-shell family. At any \(\beta\lambda>0\), further OR compression
strictly loses some counting-field resolution; port-forgotten detailed
labels in (3) do not.

**Physical integrator decision:** a complete native history can carry
geometric *scores*, code-relative *information price*, and coherent
memory simultaneously. The original nonblank-port **score** is redundant
given labels, and its **expected price/source** is fully reconstructable
from the original count, but the more extreme binary OR statistic is not
information-sufficient. None of this identifies the complete D0
Cost−Info/clock/work action with original Palatini/CAR, which remains
open. Do not use missing observed port bits as an excuse to add a
new geometric source or to discard native code-price variation.
\`GR_closed=false\`.

**Independent calculation:** [port sufficiency, primitive code/source and binary-OR hostile control](sources/d0_native_history_class_map_2026-10-19/check_original_port_score_and_code_source.mjs).
This consumes the pinned original 128-Kraus factorization and J23 source
without re-enumerating its 16x16x128 matrices.
