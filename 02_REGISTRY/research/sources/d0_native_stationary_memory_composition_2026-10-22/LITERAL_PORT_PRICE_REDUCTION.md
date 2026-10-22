# Exact finite-window reduction of the declared literal full128 PORT price

22 October 2026 · same original full128 execution; finite scalar-refinement identity. This is an exact rewriting of **the declared port-report cost minus complete CQ input-entropy gain**, not a choice of compulsory Book03 Info, a new tariff, or physical erasure. `GR_closed=false`.

## Source and literal charges

The original full128 owner [PROOF.md, §§1,7](https://github.com/gvakhrushev/d0_15/blob/7bfd569c151470d2a17e8a2b6d2707ec708d7803/02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/PROOF.md), Git blob `faac1bc80e25cfbcaba951f46b22b3ba1d9f3b84`, fixes the port-report component as

\[
c_b=1+b,\qquad b\in\{0,1\}.
\]

Its §7 explicitly retains this original charge under any mathematical port relabeling; changing the charged clock requires real additional operations. Its §0 keeps full128 separate from the distinct N1 CQ compiler. The instrument constructor `check_uniform_book_source.py`, Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`, orders each actual pair as PORT0 then PORT1 (lines 96–100) and tests the original `1+port` ledger in lines 315–324.

Put `p=phi^-1`, `ell=ln(phi)`. For every original SELECT row `j!=0`, the unchanged Kraus operators have the exact scalar refinement

\[
K_{j,0}=pM_j,\qquad K_{j,1}=\sqrt p\,M_j,
\qquad q_0=p^2,\quad q_1=p,\quad p^2+p=1.
\]

Keep the ordinary blank `(j,b)=(0,0)` and the orphan `(0,1)` as **different** merged labels. There are 65 physical merged labels: these two and the 63 pairs `j!=0`. Structurally zero labels stay part of that carrier.

## Exact statement for arbitrary retained input

Fix any finite **K-tick window** and any normalized initial DATA–reference state `Omega`, including pure, mixed or correlated retained preparations. Both output channels use the same chronological instrument, initial state and reference. Let `Gamma_F,K` retain every fine label, and `Gamma_M,K` merge only the two ports within each `j!=0` row.

For a merged word `z`, let `N_blank(z)`, `N_orphan(z)` and `N_pair(z)` count these three event types; their sum is K. Each fine refinement of `z` multiplies its complete operator product by scalar factors `p` or `sqrt(p)`. These commute with all intervening noncommuting DATA operators and with the retained reference. Thus, conditional on `z`, its paired bits have product probabilities `q_b`, and every refinement has the same normalized conditional quantum state.

Consequently, as exact finite functions of the input and all admitted field parameters,

\[
S(\Gamma_{F,K})
=S(\Gamma_{M,K})+\ell(2-p)\,\mathbb E_\Omega N_{\rm pair}.
\tag{1}
\]

Indeed, every fine block is `q_{b_1}...q_{b_m} X_z`, and expanding its entropy gives (1), using

\[
-p^2\ln(p^2)-p\ln p=\ell(2-p).
\]

The **actual** expected port cost is simultaneously

\[
\mathbb E_\Omega C_{\rm port}
=\mathbb E_\Omega\left[
N_{\rm blank}+2N_{\rm orphan}+(p^2+2p)N_{\rm pair}\right].
\tag{2}
\]

Subtracting the actual fullfine input gain yields the claimed exact identity:

\[
\boxed{\begin{aligned}
\mathbb E_\Omega C_{\rm port}
-\frac{S(\Gamma_{F,K})-S(\Omega)}{\ell}
={}&\mathbb E_\Omega\left[
N_{\rm blank}+2N_{\rm orphan}+p^3N_{\rm pair}\right]\\
&-\frac{S(\Gamma_{M,K})-S(\Omega)}{\ell}.
\end{aligned}}
\tag{3}
\]

The coefficient is forced by the already-bound port charges:

\[
p^2+2p-(2-p)=2p-1=p^3>0.
\]

No stationary-input assumption, DATA reset, diagonalization, independently sampled histories, or entropy approximation enters this proof.

## Source scope and boundaries

Equation (3) is a full function identity on the admissible joint-input space. Hence **every ambient input derivative and admitted field jet agrees wherever those derivatives exist**, including correlation directions; this is stronger than equality only after inserting a stationary preparation. At rank-changing boundaries entropy need not have a finite ordinary derivative, so no unsupported smooth-log gradient is asserted there.

The `p^3` term is the net coefficient after exactly subtracting the retained paired-bit entropy. It is not a new fractional code length, a cost-free deletion of actual bits, or a physically executed erase operation. The fine archive remains retained in the underlying execution.

The proof covers every fixed finite K. It also extends to a finite stopping tree whose stop rule is determined by the merged labels. It must not be transferred without a separate argument to a stop rule that reads the discarded PORT bit: conditioning on such a stop can change the paired-bit law.

All literal fine-label, factory, preparation, controller, and other clock costs outside the declared `1+b` component remain outside (3), as do other choices of physical information valuation or Book03 heat/feedback. If present, those same genuine additional terms must be retained on both sides. The complete physical Book03 price is not identified by this reduction.
