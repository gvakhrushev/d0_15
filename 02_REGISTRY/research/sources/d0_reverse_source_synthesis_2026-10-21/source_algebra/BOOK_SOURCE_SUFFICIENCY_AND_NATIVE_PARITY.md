# Native Book feedback: a source-sufficient algebra on the actual full128 execution

21 October 2026. Existing scientific PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`. Scientific input: `2961dc6ee4abcda0a0fb2aa36dc6ecd7e62a6535`. This is a bounded source-interface result. All equality assertions concern the complementary component \(J\), not the complete Cost−Info or \(H+J+R\) price. It does not choose a new Info law, active cut, controller, or physical heat generator. `GR_closed=false`.

## 1. Result and the input actually being reduced

The corrected original normalization owner already gives the exact complementary Book component from **two effects** on the complete input space. For an injective retained amplitude map \(W:H\to E\), the specified active embedding \(i:H\to E\), and its projection \(P=ii^*\), set

\[
 N=W^*W>0,\qquad A=i^*W,\qquad B=W^*PW=A^*A,
 \qquad Q=(1-z)N+zB,
 \quad 0<z<1.
 \tag{1}
\]

Then \(0\le B\le N\). For the normalized map \(\widehat W=WN^{-1/2}\), its original complementary feedback has

\[
 J=r_R\{\operatorname{Tr}\log N-\operatorname{Tr}\log Q\}.
 \tag{2}
\]

Here the trace is the **ordinary full input trace**, and \(r_R\) is the actual fixed spectator multiplicity. Equation (2) is consumed from `d0_full128_normalization_closure_2026-10-21/PROOF.md`, §4, equations (7)–(8); it is not a new normalization prescription. In particular, a cost-marked amplitude and its polar normalization are not thereby a new paid physical isometry. The owner separately retains every failure of an actual attenuation.

The new application is that evaluation of the **first source** does not require recovery of the entire history state, all correlations, or all off-algebra effect derivatives. A trace projection onto an algebra containing the two anchor effects suffices. On the actual original full128 Walsh/Julia/Golden execution, CAR parity provides such an algebra with a **fixed native basis**, at every finite horizon and every scalar cost mark. In the consumed **CAR16 Fourier-block fixture**, its full \(16\times16\) source is exactly the sum of two \(8\times8\) sources, retaining oldRIGHT multiplicity 128. On a full spatial DATA carrier with \(S\) sites, the two parity blocks have dimensions \(8S\), not eight; no spatial trace or off-site correlation is removed. No record is discarded.

The elementary trace-projection calculus is not claimed as new general operator theory. The contribution is its application to the corrected nonscalar normalizer, its exact second-source boundary, and the actual full128 graded history maps. The prior rank-two diagonal first-contact theorem in `book_source/TWO_NATIVE_8D_DETERMINANT_SOURCE.md`, §4, is a special unmarked case, not the nonscalar complete-history application here. The already owned complete-history Petz/code/coherence theorem concerns recovery of a selected relative-entropy component; no such recovery assumption is needed for (2)'s first differential.

## 2. Source sufficiency and its exact algebraic criterion

Let \(\mathcal A\subset\operatorname{End}(H)\) be a fixed unital complex *-subalgebra, and let \(\mathbb E\) be its trace-preserving conditional expectation. In finite dimensions this is the Hilbert–Schmidt orthogonal projection onto \(\mathcal A\); it is unital, positive, trace self-adjoint, and bimodular over \(\mathcal A\). All traces below retain the represented block multiplicities.

Suppose at the anchor

\[
 N_0,B_0\in\mathcal A.
 \tag{3}
\]

For arbitrary smooth ambient variations of \(N,B,z\), define \(N_{\mathcal A}=\mathbb E N\), \(B_{\mathcal A}=\mathbb E B\), and \(J_{\mathcal A}\) by (2) with these effects. Positivity gives a common neighborhood on which both expressions are defined. At the anchor,

\[
 J=J_{\mathcal A},\qquad DJ=DJ_{\mathcal A}
 \quad\text{for every ambient first variation.}
 \tag{4}
\]

**Proof.** Since \(Q_0^{-1},N_0^{-1}\in\mathcal A\), trace self-adjointness gives

\[
 DJ=r_R\operatorname{Tr}
 \left[N_0^{-1}\mathbb E(DN)-Q_0^{-1}\mathbb E(DQ)\right],
 \quad DQ=(1-z)DN+zDB+(B-N)Dz.
 \tag{5}
\]

This is precisely the derivative of \(J_{\mathcal A}\). The derivatives themselves need not lie in the retained algebra. A moving cut contributes

\[
 DB=(DW)^*PW+W^*P\,DW+W^*(DP)W;
 \tag{6}
\]

all three terms must be supplied before applying (5). No fixed-cut identity authorizes dropping the third term.

For fixed \(z\), write the source as

\[
 DJ=r_R\operatorname{Tr}(K_NDN-K_BDB),\qquad
 K_N=N_0^{-1}-(1-z)Q_0^{-1}\succeq0,
 \quad K_B=zQ_0^{-1}\succ0.
 \tag{7}
\]

The sign of \(K_N\) follows from \(Q_0\succeq(1-z)N_0\) and order reversal under inverse. A moving \(z\) adds the retained scalar term
\(r_R Dz\operatorname{Tr}[Q_0^{-1}(N_0-B_0)]\).

There is also an exact necessity statement on the space of **independent arbitrary Hermitian effect jets**: the functional in (7) factors through \((\mathbb E DN,\mathbb E DB)\) if and only if \(K_N,K_B\in\mathcal A\). This follows by testing the Hilbert–Schmidt orthogonal complement in each jet separately. Since

\[
 Q_0=zK_B^{-1},\qquad
 N_0=\left[K_N+\frac{1-z}{z}K_B\right]^{-1},\qquad
 B_0=\frac{Q_0-(1-z)N_0}{z},
 \tag{8}
\]

this is equivalent to (3). Thus \(C^*(N_0,B_0)\) is the minimal unital *-algebra for this **universal** two-effect source interface. A smaller specified physical tangent space may require less information; necessity on all ambient jets is not a claim that every such jet is physically admitted.

If \(N(y),B(y)\in\mathcal A\) throughout the neighborhood, (2) is exactly equal throughout that neighborhood and all its existing smooth jets agree. In a represented decomposition \(\bigoplus_\lambda M_{d_\lambda}\otimes I_{m_\lambda}\), each trace is \(\sum_\lambda m_\lambda\operatorname{Tr}_{d_\lambda}\). Removing the \(m_\lambda\) changes the Book price.

## 3. The second-source term which first-source sufficiency does not erase

For a one-parameter \(C^2\) variation through the anchor, put

\[
 n_\perp=(I-\mathbb E)\dot N,\qquad
 q_\perp=(I-\mathbb E)\dot Q
       =(1-z)n_\perp+z(I-\mathbb E)\dot B.
\]

The equality on the right includes moving \(z\), because \(B_0-N_0\in\mathcal A\). The exact Hessian defect is

\[
 \boxed{\quad
 (J-J_{\mathcal A})''
 =r_R\left[
 \|Q_0^{-1/2}q_\perp Q_0^{-1/2}\|_{\rm HS}^2
 -\|N_0^{-1/2}n_\perp N_0^{-1/2}\|_{\rm HS}^2
 \right].\quad}
 \tag{9}
\]

Indeed, \(D^2\operatorname{Tr}\log X=\operatorname{Tr}(X^{-1}\ddot X-X^{-1}\dot X X^{-1}\dot X)\). The acceleration terms cancel by trace self-adjointness. Mixed retained/orthogonal terms vanish by bimodularity, leaving (9). The same proof gives its polarized bilinear form. No second derivative of the fields or cut has been frozen.

For \(N\equiv I\), the defect is nonnegative; in the marked problem it has no fixed sign. Two exact controls, with ordinary diagonal expectation, \(X=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}\), \(z=1/2\) and \(r_R=1\), show both possibilities:

* \(N=I, B(s)=I/2+sX\) gives \((J-J_{\mathcal A})''(0)=8/9>0\).
* \(N(s)=I/2+sX, B(s)=I/4-sX\) gives constant \(Q=3I/8\) and \((J-J_{\mathcal A})''(0)=-8<0\).

Both obey \(0<B<N\le I\) on a sufficiently small neighborhood (strict \(N<I\) in the second example); they are legitimate finite two-effect controls. They are not asserted to be new native primitive variations. Consequently a first-source quotient alone cannot transport stability, a Hessian, or an apparatus minimum.

## 4. Exact application to the ORIGINAL full128 graded history map

First fix the CAR16 fibre (also the whole input of the consumed Fourier-block fixture), with the canonical mask basis and

\[
 \Pi|m\rangle=(-1)^{\operatorname{popcount}(m)}|m\rangle,
 \quad H=H_+\oplus H_-,\quad\dim H_+=\dim H_-=8.
 \tag{10}
\]

Each original CAR creator and annihilator is odd. The actual exterior proper-link maps are even, so their contracted CAR words \(X_r\) are odd. Both Julia defects \((I-X_rX_r^*)^{1/2}\) and \((I-X_r^*X_r)^{1/2}\) are even. The Walsh mixing combines words only within one of these two columns. Hence the actual 64 first-row blocks \(N_j\) have parity

\[
 \Pi N_j\Pi=(-1)^{1-q_j}N_j,
 \qquad q_j\in\{0,1\},\qquad A_{\rm native}=N_0\text{ odd}.
\]

Here \(q_j=0\) denotes the CAR column and \(q_j=1\) the defect column; in the imported original fixture \(q_j=j\bmod2\). The genuine Golden columns are

\[
 K_{0,j}=\delta_{j0}I-2p^2N_j^*A_{\rm native},\qquad
 K_{1,j}=-2p\sqrt p\,N_j^*A_{\rm native}.
\]

Therefore, for **both ports and every actual label**,

\[
 \boxed{\Pi K_{b,j}\Pi=(-1)^{q_j}K_{b,j}.}
 \tag{11}
\]

This is a structural parity identity, not a numerical eigenvalue coincidence. Every chronological complete history \(K_\omega\) has parity \(\chi_\omega=\sum q_j\pmod2\). For the original costs \(c_b=1+b\), retain every history in

\[
 W_{n,t}=\sum_\omega e^{-tC_\omega/2}|\omega\rangle K_\omega,
 \qquad n\le C_\omega\le2n.
 \tag{12}
\]

Each \(K_\omega^*K_\omega\) is even, so

\[
 N_{n,t}\in\mathcal A_\Pi,
 \qquad\mathcal A_\Pi=\{X:[X,\Pi]=0\}
                    \simeq M_8\oplus M_8.
 \tag{13}
\]

Equivalently, the complete history-space involution
\(\Pi_{\rm out}=\sum_\omega(-1)^{\chi_\omega}|\omega\rangle\langle\omega|\otimes\Pi\)
obeys \(\Pi_{\rm out}W_{n,t}=W_{n,t}\Pi\). It is an identity on the retained output; no history parity is measured.

For the owner's specified blank-history embedding, the corner is

\[
 A_{n,t}=e^{-nt/2}K_{0,0}^{n},\qquad
 B_{n,t}=A_{n,t}^*A_{n,t}\in\mathcal A_\Pi.
 \tag{14}
\]

More generally the same conclusion holds for a specified cut satisfying \([P,\Pi_{\rm out}]=0\). Such invariance is a **condition on that cut**, not proof that Book selects it. Equations (12)–(14) hold for finite \(n\), finite \(t\ge0\), and the same smooth odd-CAR/even-link/Julia chart. They do not assume a scalar normalizer: the actual owner proves

\[
 e^{-2nt}I\preceq N_{n,t}\preceq e^{-nt}I,
 \quad Q_{n,t}\succeq(1-z)e^{-2nt}I.
 \tag{15}
\]

The positive lower bound makes every displayed finite inverse legitimate; no uniform growing-\(n\) or refinement bound is asserted.

Use the **fixed** trace expectation

\[
 \mathbb E_\Pi(X)=\frac{X+\Pi X\Pi}{2}.
 \tag{16}
\]

On this declared CAR16 input, at every anchor of the actual family, arbitrary ambient first effect/cut/normalizer jets have the exact source

\[
 \boxed{
 DJ=128\sum_{\epsilon=\pm}\operatorname{Tr}_{H_\epsilon}
 \left[N_\epsilon^{-1}(DN)_{\epsilon\epsilon}
       -Q_\epsilon^{-1}(DQ)_{\epsilon\epsilon}\right].}
 \tag{17}
\]

Both blocks are retained, with the actual oldRIGHT factor 128 on their sum. Off-diagonal parity effect jets are unnecessary for **this first-source evaluation**. Along the actual parity-preserving family, values and all smooth jets of (2) agree with the two-block evaluation; for arbitrary off-chart variations only first contact is guaranteed and (9) applies.

For the whole \(S\)-site DATA carrier replace \(\Pi\) by \(I_{\rm site}\otimes\Pi\), retain the full spatial matrices, and replace \(M_8\oplus M_8\) by \(M_{8S}\oplus M_{8S}\). The same graded-word proof and trace formula apply, with the genuinely specified spectator multiplicity. Reducing those spatial blocks further to Fourier fibres requires an additional actual translation-invariance/decomposition owner; it is not inferred from parity.

This directly consumes the nontrivial original numerical fixture, without replaying its historical test suite: \(\theta=.08,\ t=.7,\ n=2,\ z=2^{-20}\). Its original `native(theta)` supplies all 128 Kraus and defect derivatives; two calls to the original transfer recurrence give \(N,DN\), and its **actual** corner is \(A=e^{-t}K_{0,0}^2\). The new checker verifies all 128 parities and their jets, both effect blocks, and (17), including added off-parity ambient jets and a moving \(z\). The normalizer has eigenvalue spread about \(9.09\cdot10^{-5}\); the full field source is about \(-4.79118\cdot10^{-6}\), so the application is neither a scalar-normalizer nor a zero-source fixture.

The same Kraus data also give the nonzero first source of the unchanged unmarked execution, \(N_{n,0}=I\), by (17); the checker includes this case separately. The cost-marked normalized case does not identify its polar map with a paid replacement.

The retained work, all 128 ports/labels per round, all oldRIGHT correlations and the meaning of the blank cut remain those of the original owner. Taking a smaller trace, one selected prepared column, or only one parity block is not this theorem. Independent preparation sources, the complete physical heat, and any cost of an actual measurement or forgetting operation remain in their original ledgers.

## 5. What this supplies to Book06, and what it does not select

BOOK_06 §06.1 lists conditional expectation onto a retained algebra among its typed forgetting mechanisms; §§06.4–06.5 require a specified retained/archive quotient; §§06.24–06.25 specify retained tests before an entropy-selected representative. Its archive-fibre condition preserves the full fine distinction. Equations (3)–(8) give a precise **source-preservation contract** for applying that interface to the original Book03 complementary action: the two effects must belong to the represented retained algebra, or the source gradients must annihilate its discarded jet directions. For the actual full128 parity algebra, the required membership is now proved from its native words.

This replaces an excessive demand to recover all retained history states by a smaller exact demand for this one source component. It does not identify a scalar probability, Shannon entropy, or a Petz-recovered state with literal Book Info. It also does not manufacture an admissible quotient operation. In particular:

* The map (16) is used to evaluate an unchanged trace. Implementing it as a physical channel would require its paid native implementation and retained environment.
* BOOK_03 §03.10, “Why the registry is finite,” item (a), bounds tests by a finite code-cost cutoff. Affordable tests need not be closed under products; forming \(C^*\(N,B\)\) mathematically grants no new affordable test, eigenstate preparation, or controller operation.
* The actual active cut and any moving-cut term (6) still require their original owner. A new report cut is not obtained from parity.
* The original heat operator is not derived from \(N,B\). If a separately owned heat term is a spectral function of a parity-even operator, its trace source admits the same elementary parity evaluation; that conditional fact neither binds the heat to this execution nor removes Rayleigh/preparation rows.
* In particular, the already-owned nonzero primary oldRIGHT-preserving preparation source is not canceled by source compression. Nothing here changes that preparation or its price.

The resulting parent substitution is therefore concrete and narrow: **for the actual full128 complete history map and the declared cut, the first normalized Book feedback source needs only its two parity-block effect jets, with the exact nonscalar normalization and full multiplicities.** Binding that map/cut and the remaining heat/Info/controller terms to one compulsory physical execution is still a separate task.

## 6. Evidence and reproducibility

`SOURCE_PINS.json` binds the consumed original Book sections, full128 normalization owner and code, original native reflection, and prior first-contact/Petz boundaries at the stated scientific input. `check_book_source_sufficiency.py` imports only the source functions `native`, `transfer` and matrix helpers from the pinned owner; it never invokes that module's `main`, historical checks, primary geometry, or old test suites. It adds a small exact rational noncommuting two-block source control, both signs of the Hessian defect, and the original full128 parity/source application. Numerical tolerances are numerical checks, not substitutes for the structural proof (11)–(17).

Run with NumPy, SciPy and SymPy available (SymPy is imported by the consumed owner):

```text
python3 check_book_source_sufficiency.py --repo /path/to/d0_15 --output RESULT.json
```

The checker prints JSON when `--output` is omitted. It records its own/proof hashes and historical input pins, not an absolute scratch path. No optimized review receipt is asserted until independently run.
