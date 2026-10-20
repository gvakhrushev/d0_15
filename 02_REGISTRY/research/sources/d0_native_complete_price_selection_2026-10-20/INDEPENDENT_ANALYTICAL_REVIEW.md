# Independent analytical review of the complete-price selection packet

Reviewer: `cost_variation`, bounded read-only subtask of existing PR #334.
Date: 20 October 2026. No repository sources were modified by this reviewer.
This is a correctness review of three stated mathematical applications and
their main synthesis. It
does not re-certify the older full128 theorem, native primitive admission,
complete Book03 payment, the GR source match, or raw216.

## Reviewed artifacts and exact hashes

All paths are relative to the source checkout. SHA-256:

| Artifact | SHA-256 |
|---|---|
| `02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/FULL128_COHERENT_LIMIT_AND_INFO_PRICE.md` | `755fb3b181bfdc989235f54c518372404e72c008a70fbe9071a400da389b2530` |
| `02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/TASK_INVARIANCE_AND_TERMINAL_MINIMUM.md` | `59ad221195a386b037a615c8275989d4b3d9782009b14179c2c324a3159e9949` |
| `02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/NATIVE_BINARY_TASK_MINIMUM.md` | `fe1bd6a907ad13ff454de7e22b323b0065b7eecf75c127f74243df26ea435284` |
| `02_REGISTRY/research/A4D_NATIVE_COMPLETE_RECORD_INFO_PRICE_SELECTION_2026_10_20.md` | `93d530eaa84df942bafb174006210047adb6588ec017d14d22bfa91ce800eaeb` |

Inspected owned analytical inputs:

| Input | SHA-256 |
|---|---|
| `02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md` | `d1c3cff174b2e4d03481ca6b3d18a1da2d3b65baba1f2dbf886324d8ce7f607d` |
| `02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md` | `577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e` |

The review used the input definitions preserved at `c7a2e7c3`. The later
remote note concerning conditional fixed-void code units does not change
these definitions or the reviewed mean-versus-fixed-evidence distinction.

## Decision and resolved scope clarification

**The mathematical statements and proofs are accepted in their explicit
scopes.** No incorrect source coefficient, dropped native outcome, invalid
entropy continuity step, or unjustified reset was found.

The strict unique minimum belongs to the **limiting finite part** `g` in
section 8, while finite-h minimizers are proved to exist, lie in an interior
bracket for small h, and converge to that minimum. Finite-h strictness or
uniqueness is not proved. The final introduction now expresses precisely
this distinction, resolving the review's earlier wording qualification.
The mathematical body and the main synthesis preserve the same scope.

The earlier possible blank-index ambiguity is already corrected in the
reviewed version: among the 127 nonblank labels only 18 and 19 survive in
the rescaled limit; the other 125 vanish, while the ordinary blank remains
the scalar drift. All 128 outcomes remain at each finite h.

## 1. Literal full128 instrument and coherent factorization

The displayed SELECT limit follows from the actual duplicated word order.
As `nu=ha` tends to zero, the first word coefficients vanish and the second
coefficients are `++++----` repeated four times. Under the owned Walsh
normalization `1/32`, this is character 4. Its coefficient-qubit entry is
1, hence flattened SELECT index `2*4+1=9`, and the two actual Kraus indices
are `2*9=18` and `2*9+1=19`. This is a consequence of the literal retained
labels, not a rotated probability basis.

On each signed first Fourier block,
`D_h(ha)/(ha) -> 2 pi i sign(c_r-c_r*)` in the owned C1 sense. Its division
by `2 pi` is a selfadjoint, trace-zero involution Q, including all CAR16
grades. With `tau=epsilon h^2`, the original coefficients become
`-2 pi a p Q` and `-2 pi a sqrt(p) Q`. Their total effect is
`4 pi^2 a^2 (p^2+p)I = 4 pi^2 a^2 I`. In particular the event marks have
probabilities `(p^2,p)`; reversing these marks would change the paid return
factor and is not done.

The `Y_k` normalization is correct: the ordered time simplex has measure
`T^k/k!`, the squared sum of mark amplitudes is 1, and Q is unitary. Multiplying
the coherent coefficient `Lambda^(k/2)/sqrt(k!)` by `sqrt(k!/T^k)` gives the
actual jump amplitude `lambda^(k/2)`; no factorial or extra CAR/reference
multiplicity is missing. Sector orthogonality gives one parameter-independent
isometry on the full DATA/oldRIGHT input.

The coherent cross coefficient is consequently
`exp[-2 pi^2 T(a-b)^2]`, consistent with the original finite scalar cross.
The count Fisher information is `16 pi^2 T=32 pi^2 p^2`, equal to the
coherent quantum Fisher information for this one real parameter. This
does not make count measurement quantum-reversible or globally optimal
for separated hypotheses; the proof preserves that boundary.

## 2. Complete pointer entropy and its first variation

Scalar `K_blank=bI` and scalar nonblank total effect `uI` imply the exact
position/mark factorization. The data need not reset after an event.
Successive normalized jump operators form an isometry, so their k-step
amplitude derivative has norm at most kB. Its classical Fisher bound
`4k^2B^2` is valid for the full `127^k` mark distribution.

For `Z=-log q`, the bound `Pr(Z>s)<=min(1,M exp(-s))` indeed yields
`E Z^2 <= (log M)^2+2 log M+2`. Cauchy--Schwarz therefore gives a polynomial
bound on the entropy derivative, uniformly in h. At zero outcomes, the
function `-||v||^2 log||v||^2` has continuous zero gradient, so there is
no hidden positive-probability floor.

The passage from fixed k to all k is justified. In particular,
`Pr(K=k)<=Lambda_h^k/k!`, and its parameter derivative is bounded by a
constant times `(k+Lambda_h)Pr(K=k)` on the compact positive a-chart.
This factorial majorant controls both the polynomial entropy bound and
its first derivative. The limiting jump-mark law is genuinely IID with
probabilities `(p^2,p)`, whence `M_h -> Lambda h_2(p)` in C1.

The expansion
`n h_2(u)=Lambda_h log(1/tau)+Lambda(1-log lambda)+o_C1(1)`
follows from `u=tau lambda_h`, `Lambda_h=n u`, and the stated C1 `O(h^2)`
error for lambda_h. The replacement of Lambda_h by Lambda in the leading
term is legitimate because `h^2 log(1/h)->0`. The resulting coefficient
`-64 pi^2 p^2 a/log(phi)` in the derivative normalized by `log(1/h)` is
correct. This is a whole fine-pointer theorem and cannot be inferred
merely from a binary lower bound.

The exact differential-entropy correction has the correct sign: each
k-event cell has volume `tau^k`, so integrating its density gives
`H_differential = H_discrete + E K log(tau)`.
The text correctly treats it as a change of reference measure, not an
already paid timestamp operation or a free subtraction from Book03.

## 3. Coherent entropy, exact finite unitality, and the minimum

The limiting channel is the actual parity mixture
`P_even rho+P_odd Q rho Q`. For a fixed purification, its two branch
overlap is `r=Tr rho Q`; this gives the displayed two eigenvalues of the
fresh record and, at maximally mixed DATA, `S(F)=h_2(P_odd)`.

The finite-h assertion `S(FR)=log128` has an exact native algebraic
justification. Walsh Parseval gives

`sum_alpha N_alpha* N_alpha = (1/32) sum_j (P_j*P_j+L_j*L_j)`.

For each role, the duplicated paired `(P,L)`, `(P*,R)`, `(-C,-L)`,
`(-C*,-R)` words contribute `8I`: `P=phase*C`, `L^2=I-CC*`, and
`R^2=I-C*C`. Summing four roles yields `32I`. Thus this native recycling
map is unital as well as trace preserving. On the homogeneous shell
`A^2` is scalar; inserting `sum N* N=I` into the complete actual 128 Kraus
sum gives `sum K K*=I`. Hence maximally mixed DATA remains exactly
maximally mixed at every finite round. Purity of DATA/R/F then gives
`S(FR)=S(DATA)=log128`. This argument does not assert energy conservation
on an arbitrary nonuniform carrier.

The coherent entropy C1 argument is valid despite record-space growth.
For the fixed pure input the Schmidt-amplitude operator has the fixed
finite domain DATA tensor R of dimension `128^2`. Reshaping the owned
full amplitude C1 limit gives Hilbert--Schmidt C1 convergence. The entropy
gradient in singular values is `-2s(log(s^2)+1)`, continuous at zero.
The fixed domain dimension makes the corresponding operator gradient
continuous. This is sufficient; C1 convergence of density matrices by
itself would not have been sufficient.

Direct differentiation confirms both formulas for g' and g'' and their
endpoint limits. Independent standard-library bisection gives

`x_*=0.3760419142141336`,
`Lambda_*=0.48902733391562236`,
`a_*=0.12733838610533196`.

Uniform value convergence on a compact interval containing a_* gives
convergence of finite-h minimizers. C1 convergence gives interior bracketing
for sufficiently small h. Neither supplies finite-h uniqueness, which is
correctly withheld in the body. Including oldRIGHT instead leaves the
strictly increasing known port price, so the two information-algebra
choices really do have different minima on the same retained execution.
Neither is selected as compulsory native Info.

## 4. Postrotation task invariance and exact terminal minima

The reporter-conjugated map `R G^(l-k) R*+(I-RR*)` is unitary on the
complete output space. A fixed known prefix-clock relabelling can also
be extended to a unitary. Its action is independent of the unknown field
and transfers every POVM, including oldRIGHT-correlated inputs. The
statistical-equivalence conclusion is correct, with physical decoder
admission and its cost properly excluded from the theorem.

At the common-null stratum, the clean amplitude has tangent norm
`2|dt|`, orthogonal to the clean base, giving QFI `16 dt tensor dt`.
Nonclean amplitude is O(t^2), so it contributes no first-jet Fisher term.
For `c_k s_k !=0`, the two clean pointer probabilities give exactly the
same Fisher tensor. The treatment of k=0 as a rank-singular signed
pointer experiment is necessary and correct.

The relative-entropy lower bound proves the stated all-k minimum with
its actual ell_G hypothesis. For a required regular signed pointer task,
k=1 is feasible and cheaper than every k>=2 for every ell_G>0. Its
Cost-minus-Shannon first source is zero by the exact Golden code match.
This genuinely excludes using that information requirement to force G^2;
it does not declare physically restricted decoders free.

The complete pointer decrease off the stratum is also correct. For k=0,
each coarse port effect is the scalar `q_b I`, so oldRIGHT conditioned on
the coarse port keeps its fixed marginal. Adding a classical fine-work
label cannot lower `S(BR)`. Hence the cq entropy increment is at least
the binary entropy, with no false assumption of independent conditional
oldRIGHT states on each fine branch. The signal bound `|t|<=z/2` supplies
`0<q_1<=z^2<p`; its strict entropy decrease and the coefficient
`-8a^2 epsilon^2 log(1/|epsilon|)/log(phi)` follow. Nearby nonzero t must
exist for the local-minimum exclusion, exactly as stated.

## 5. Exact binary task, minimax error, and paid horizon

The stable expression for f follows from
`(1-xy)^2-(1-x^2)(1-y^2)=(x-y)^2` and is correct on positive x,y<1.
The scalar cross gives two orthogonal isometric embeddings J_0,J_1.
Their normal form factors the same arbitrary mixed/entangled input out
of the two hypotheses, so the binary trace distance and optimal error
hold uniformly in that input. The qubit spectral test has equal
conditional errors and therefore attains the minimax, not merely
equal-prior, bound.

Solving the inequality gives the exact displayed ceiling. The port ledger
increases strictly with n under each hypothesis, so the least feasible
fixed horizon also minimizes that known payment in the specified class.
It does not minimize a decoder-dependent total cost or adaptive protocol.

The constants in `h^4 n_min`, `tau_h n_min`, and the finite excess return
price follow from `-log c_h=(p^2 pi^2/32)(a-b)^2 h^4+O(h^6)`; no factor
of two is missing. Perfect zero-error finite discrimination and coincident
hypotheses are correctly excluded. The integer optimum is not
misrepresented as a smooth gravitational source.

## Verification boundary

The main synthesis faithfully states the three applications and their
limits. In particular, the recovered L^4 all-launch and L^6 conditioned
prices belong to an occupation-weighted determinant realization; their
physical admission is separate from the present single-run h^-4 protocol.
No equation identifying those apparatus payments is claimed. The synthesis
also keeps the selected entropy algebra, the binary verification task,
native decoder compilation and its complete payment, and the physical
source-selection premise explicit. The retained historical 437-check
certificate and its proposed fresh replay are outside this review.

This review is analytical, with an independent elementary numerical
evaluation only of the one-dimensional minimum. The separate new native
checker was being assembled by another agent and is not claimed as
executed or accepted in this review. The already owned history proof and
literal native matrices were inspected only as inputs; no old expensive
certificate, Lean build or global source suite was rerun.

The three results form a consistent packet: one actual experiment yields
explicit coherent and pointer information quantities; a supplied binary
task determines a positive paid horizon; known information-invariant
requirements fail to select the desired terminal postrotation. The missing
native information algebra/task/full payment is therefore a specific
physical premise, not an already established Einstein/GR theorem.
