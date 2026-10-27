# D0 closed self-reading: exact original 128-Kraus Golden port history, temporal information, and full finite source

**27 October 2026 — mathematical research result within the existing scientific owner [#334](https://github.com/gvakhrushev/d0_15/pull/334).** Consumer: native-programme-v1 / original positive Einstein–CAR 16+24+2 source. **No new physical action, primitive, task selector, observer, branch, claim promotion, GR/root completion or new full-history price identification.**

## 0. One actual execution; one genuinely registered subrecord

Consume [the same-source closed DATA derivation](A4D_CLOSED_SELF_READING_DATA_SOURCE_RESOLVENT_2026_10_27.md), C28–C36, and the original 128-label CAR/Julia/Walsh/Golden fine instrument, not a surrogate sampler. Put

\[
p=\varphi^{-1},\quad p+p^2=1,\quad
a=N_0,\quad A=a^\dagger a>0,\quad
Z=\operatorname{Tr}_{16}(A^{-1}),\quad
\rho_A=A^{-1}/Z.
\]

The *unchanged* 128 fine operators satisfy

\[
K_{2j}=\delta_{j0}I-2p^2N_j^\dagger a,\qquad
K_{2j+1}=-2p\sqrt p\,N_j^\dagger a,\qquad
\sum_{j=0}^{63}N_j^\dagger N_j=\sum_{j=0}^{63}N_jN_j^\dagger=I.
\tag{P1}
\]

All originally dark and live fine labels stay present. Define the two **actual port-subinstrument CP maps** (do not replace the full recorded task by them):

\[
\mathcal M_b(X):=\sum_{j=0}^{63} K_{2j+b}XK_{2j+b}^\dagger,\quad b=0,1,\qquad
\Phi=\mathcal M_0+\mathcal M_1.
\tag{P2}
\]

These are obtained by reading the existing terminal port bit of each fine label, not by choosing a new POVM. For a genuine no-reset sequence \(w=(b_1,\dots,b_n)\), define its complete marginal probability

\[
P_{\rho,n}(w):=\operatorname{Tr}_{16}\big[
\mathcal M_{b_n}\circ\cdots\circ\mathcal M_{b_1}(\rho)\big].
\tag{P3}
\]

All prior fine archive labels, oldRIGHT and fresh work stay physically stored in the complete native execution. Tracing them **only to calculate the probability of this original port subrecord** is legitimate: even for an initially entangled DATA+oldRIGHT state, (P3) holds with its initial DATA marginal. It does not state that fine/coherent history Info or its price is a function of (P3).

The actual native binary reporter has codewords 0 and 10, lengths \(\ell(0)=1\) and \(\ell(1)=2\). For the finite port subrecord the truly charged reporting ledger is \(C_n(w)=n+\sum_i b_i\); any extra SOURCE/QUERY/CAR/fine-flag/controller/clock/oldRIGHT costs belong to the complete physical action in addition to this component.

## 1. Theorem P-A: each finite original port word has a positive native probability

By (P1), \(aa^\dagger\preceq I\), hence \(0<A\preceq I\). The two specific **original fine Kraus** operators

\[
K_0=I-2p^2A,\qquad K_1=-2p^{3/2}A
\tag{P4}
\]

are invertible at every original regular point: set

\[
c_0=1-2p^2>0,\qquad
c_1=2p^{3/2}\lambda_{\min}(A)>0.
\]

Their least singular values are at least \(c_0\) and \(c_1\), respectively. Since (P2) includes their actual individual positive contributions, for any strictly positive density \(\rho\), and for every finite port word \(w\) with \(n_0\) zeros and \(n_1\) ones,

\[
\boxed{
P_{\rho,n}(w)\ge
16\,\lambda_{\min}(\rho)\,c_0^{2n_0}c_1^{2n_1}>0.
}
\tag{P5}
\]

Proof: \(\mathcal M_b(X)\succeq K_bXK_b^\dagger\succeq\lambda_{\min}(X)c_b^2I\); iterate and take the trace. For \(\rho=\rho_A\), \(\lambda_{\min}(\rho_A)=1/(Z\lambda_{\max}(A))\). No postselection, assumed generic probability floor, or imported output oracle occurs. The bound is *finite-horizon and regular-chart*, not uniform in word length, mesh or singular \(A\); fine labels may still be dark or suffer support births.

**Application:** the native *binary-port* whole-history Shannon derivative exists on any smooth genuine regular original family at every fixed finite \(n\), without a separately postulated positive probability floor. This does **not** solve the unrelated fine128/coherent/complete-price probability-floor obligations.

## 2. Theorem P-B: complete correlated binary record Cost−Info is exactly a native relative entropy

For the same ORIGINAL Golden reporter define its intrinsic normalized prefix reference

\[
\mu_n(w)=\prod_{i=1}^n p^{1+b_i}=p^{n+\sum_i b_i},\qquad
\sum_{w\in\{0,1\}^n}\mu_n(w)=(p+p^2)^n=1.
\tag{P6}
\]

For any admitted initial DATA state \(\rho\) and any \(n\ge1\), let \(H_\varphi(P_{\rho,n})=-\sum_wP_{\rho,n}(w)\log_\varphi P_{\rho,n}(w)\). The actual code cost and **complete joint binary-port record entropy** satisfy

\[
\boxed{
\mathbb E_\rho C_n-H_\varphi(P_{\rho,n})
=\sum_wP_{\rho,n}(w)\log_\varphi\frac{P_{\rho,n}(w)}{\mu_n(w)}
=:D_\varphi(P_{\rho,n}\Vert\mu_n)\ge0.
}
\tag{P7}
\]

Proof: \(-\log_\varphi\mu_n(w)=C_n(w)\), and (P6) is a true probability distribution. This is an exact finite joint-history identity, not a one-shot approximation, IID postulate, entropy-rate assumption, or an invented full Book03 action.

For each timestamp let \(q_j=\operatorname{Tr}[R_1\Phi^{j-1}(\rho)]\) with the *original* port1 effect \(R_1=\sum_jK_{2j+1}^\dagger K_{2j+1}=4p^3A\). Entropy chain rule gives the more informative exact decomposition

\[
\boxed{
D_\varphi(P_{\rho,n}\Vert\mu_n)
=\sum_{j=1}^n
D_\varphi(\operatorname{Bern}(q_j)\Vert\operatorname{Bern}(p^2))
+\sum_{j=2}^n I_\varphi(B_j;B_{1:j-1}).
}
\tag{P8}
\]

The second term is the *intrinsic temporal memory* of the genuine no-reset register; it is nonnegative and may be positive even when all one-tick marginals are identical. It cannot be deleted by the statement "the system is closed."

At the **endogenous stationary state** \(\rho_A\), C36 gives \(\Phi(\rho_A)=\rho_A\), so

\[
\boxed{
q_j=q_A=\frac{64p^3}{Z},\qquad
D_\varphi(P_{A,n}\Vert\mu_n)
=nD_\varphi(\operatorname{Bern}(q_A)\Vert\operatorname{Bern}(p^2))
+\underbrace{\sum_{j=2}^n I_\varphi(B_j;B_{1:j-1})}_{\text{true correlated memory}}.
}
\tag{P9}
\]

C33 already proves \(\mathbb E_{\rho_A}C_n=n(1+q_A)\) for these same true Kraus; here its **entire joint port Info**, not merely \(nH_\varphi(\mathrm{Bern}(q_A))\), is now included.

## 3. Theorem P-C: an explicit full binary-history first source on the ORIGINAL channel

Assume a **genuinely admitted** differentiable regular family of the unchanged native Kraus, with fixed \(n,p\) and no discontinuous compiler lookup differentiated. For any physical direction \(v\), differentiation of P7 and \(\sum_wDP_w[v]=0\) yields

\[
\boxed{
D\big(\mathbb E C_n-H_\varphi(P_n)\big)[v]
=\sum_{w\in\{0,1\}^n} DP_n(w)[v]
  \log_\varphi\frac{P_n(w)}{\mu_n(w)}.
}
\tag{P10}
\]

No logarithmic singularity occurs for these binary words at finite \(n\), by P5. The derivative of the *endogenous* initial density must be retained:

\[
D\rho_A[v]=
-\frac{A^{-1}(DA[v])A^{-1}}Z
+\frac{A^{-1}}{Z^2}
 \operatorname{Tr}[A^{-1}(DA[v])A^{-1}].
\tag{P11}
\]

For each word \(w\), compute \(DP_n(w)[v]\) by differentiating precisely the \(n\) executed CP maps P3, including both Kraus and adjoint jets, and P11. Writing \(X_0=\rho_A\), \(X_j=\mathcal M_{b_j}(X_{j-1})\), the causal tangent recursion is

\[
DX_0=D\rho_A,\quad
DX_j=(D\mathcal M_{b_j})[X_{j-1}]
       +\mathcal M_{b_j}(DX_{j-1}),\quad
DP_n(w)=\operatorname{Tr}(DX_n).
\tag{P12}
\]

There is no external observer, fluid, scalar stress tensor, smooth metric or invented variation of a discrete code in P10–P12. If the original native alternatives are only **finite literal programmes**, P7 itself gives their exact finite price contrasts; P10 is used only when a true admitted differentiable section has separately been proved.

**Critical consumer:** compare the genuine finite cofield P10, in the original full42 norm and on the SAME geometric/CAR representative, to the already owned configured \(DJ_{2,h}\). It is one *real, nonzero-capable component* of the full price; the other fine128/coherent/oldRIGHT/clock/controller/scene/heat and independently varied apparatus terms stay present. Do not declare the total source P10 by omitting them.

## 4. Complementary fully coherent archive is a DIFFERENT intrinsic information algebra

For any actual isometric completion of the same physical fine Kraus process which stores **all** fresh environmental degrees and old retained purification, if the total initial DATA+retained-archive state is pure, then after \(n\) genuine no-reset ticks the state DATA+FULL ARCHIVE remains pure. Consequently

\[
\boxed{S(\mathrm{FULL\ ARCHIVE}_n)=S(\rho_{\mathrm{DATA},n})\le\ln16.}
\tag{P13}
\]

This is the ordinary finite Schmidt entropy identity and reproduces the previous original maximally-entangled complete-record equality at its own physical input. At the stationary marginal it gives \(S(\mathrm{FULL\ ARCHIVE})=S(\rho_A)\), **provided the initial full state is genuinely pure and its actual archive purifies this marginal**. Genuine finite endogenous preparation retains its past work and must be paid.

Equation P13 is not \(H(B_{1:n})\), not the entropy of the classically dephased fine pointer, and not unconditional on a mixed total input. Indeed, P13 is bounded by \(\ln16\) while the classical recorded-port Shannon entropy can grow with \(n\). The two quantities are both internal and distinguishable; neither may be silently named compulsory Book03 Info. Fully coherent archive operations and fine code costs remain separately typed.

## 5. Exact controls and application boundary

A fully specified two-dimensional **structural** Walsh/Julia control (NOT a substitute for the original CAR16) sets
\(N_0=\operatorname{diag}(1/2,2/3)\),
\(N_1=\operatorname{diag}(\sqrt3/2,\sqrt5/3)\),
\(N_j=0\) otherwise, and uses the *unchanged algebraic* K formula P1. Both two-sided completeness sums equal I, all K are TP, and \(\rho_A=\operatorname{diag}(16/25,9/25)\) is fixed. The stationary port marginal is \(q_A=0.3021670111997309\) and the actual port outcomes are NOT independent.

At horizons 1,2,3,4, respectively, \(D_\varphi(P_n\Vert\mu_n)\) evaluates to

\[
0.0289455137,\quad0.0592889532,\quad0.0909326027,\quad0.1237946758.
\]

The true temporal-memory terms P9 are \(0,0.0013979258,0.0040960616,0.0080126209\). Direct joint Shannon-and-price evaluation reproduces each KL to \(10^{-12}\). At \(n=3\), varying only the first \(N_0\) eigenvalue, explicit analytic differentiation of the full correlated word law gives source \(-1.801093484055646\); the central finite-difference value is approximately \(-1.801093485198635\) for step \(10^{-5}\). The companion narrow checker should test these source and norm identities without touching the old original CAR/spectral/Lean suites.

### What this actually changes

**Closed here, at its specified mathematical scope:** original-port all-word positivity on the regular chart; exact full **correlated binary-port** Cost−Info as Golden relative entropy; explicit entire finite-record port source with endogenous preparation and no support-floor postulate; exact non-IID temporal-memory penalty. It consumes C28–C36 and the original reporter, rather than introducing another primitive.

**Not closed:** fine128/coherent/oldRIGHT complete physical Info, original full Book03 H+J+R/Cost−Info price, task and compiler/admissible field-image selection, exact full42 physical source, mesh-uniform refinement, universal Einstein dynamics, the original raw216 terminal. The fresh coherent total-archive entropy P13 is a different observable algebra, not a free way to equate it with the port Shannon term. **GR_closed=false.**

The decisive next SAME-execution comparison is the *remaining full-price residual*

\[
\mathcal R_h:=D\mathcal B_h^{\mathrm{complete}}
 - D\big[\mathbb E C_{n,h}^{\mathrm{port}}-H_\varphi(B_{1:n})\big]
\tag{P14}
\]

against the configured all42 source, with actual native paid words, source gain, and original norm. The first bracket is a measured source term from the exact 128-Kraus port, not an Einstein source inserted by definition. No new problem/task owner is needed; consume inside existing #334.


## 6. Theorem P-D: exact finite Bellman self-reading, no history census as a new axiom

The relative-entropy identity P7 has an even more direct **closed causal recursion** on the same actual DATA16 instrument. For any full-rank internal conditional DATA density \(\sigma\), set

\[
q(\sigma)=\operatorname{Tr}(R_1\sigma),\quad
P_b(\sigma)=\operatorname{Tr}(\mathcal M_b(\sigma)),\quad
\sigma_b=\mathcal M_b(\sigma)/P_b(\sigma),\ b\in\{0,1\}.
\]

The two port probabilities are strictly positive, since P4's genuine K0/K1 are invertible. Thus there is no forced threshold, external oracle, postselected outcome, or undefined conditional state. Define \(\mu_0=p,\ \mu_1=p^2\), and \(d_\varphi(q\Vert p^2):=D_\varphi(\mathrm{Bern}(q)\Vert\mathrm{Bern}(p^2))\). The unique finite-horizon recursively specified score is

\[
\boxed{
V_0(\sigma)=0,\qquad
V_{k+1}(\sigma)=d_\varphi(q(\sigma)\Vert p^2)
+(1-q(\sigma))V_k(\sigma_0)
+q(\sigma)V_k(\sigma_1).
}\tag{P15}
\]

**Exact statement:**

\[
\boxed{V_n(\sigma)=
\mathbb E_\sigma C_n-H_\varphi(B_{1:n})
=D_\varphi(P_{\sigma,n}\Vert\mu_n)}
\qquad(n\ge0).
\tag{P16}
\]

**Proof by finite induction, without IID.** At a root, the entire word-law decomposes into its genuine first bit \(b\) of probability \(P_b(\sigma)\) followed by the conditional tail law \(P_{\sigma_b,k}\). The chain rule for relative entropy with the PRODUCT golden reference \(\mu_1\otimes\mu_k\) gives precisely \(d_\varphi(q(\sigma)\Vert p^2)+\sum_bP_b(\sigma)D_\varphi(P_{\sigma_b,k}\Vert\mu_k)\). The \(k=0\) statement is 0, so P15/P16 follow. Every conditional state is generated by the actual native CP maps and their stored port prefix. The recurrence is *not* an independent Bellman control assumption, a new native task or a postulated local Lagrangian.

This makes the entire original **binary reporting** Cost−Info law an internally computed causal potential, once its actual registered output and code have been specified. At the stationary native starting state \(\sigma=\rho_A\), it reproduces P9; the branches \(\sigma_0,\sigma_1\) are generally NOT equal to \(\rho_A\), hence the memory term persists despite stationary unobserved DATA.

**Consumer and necessary distinction.** Differentiating P15 through a genuine field family produces the same source P10/P12, including movement of both branch states; it cannot be replaced by differentiating only the one-step term. Nothing in P15 asserts that the *full* original fine/coherent/clock/oldRIGHT Book03 action equals the binary-port score, or that it selects the configured \(DJ_2\). The exact native all42 source comparison remains the scientific parent, not another independent certificate.
