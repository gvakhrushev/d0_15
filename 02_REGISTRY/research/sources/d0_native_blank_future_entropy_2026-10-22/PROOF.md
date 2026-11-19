# Native blank futures select the inverse-square entropy representative

22 October 2026. Existing scientific Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Phase: native realization / same-execution source composition.
Input checkpoint: `82d27e83b0ba0869911de80919de50c42f2944d8`.

## 0. Exact parent substitution

The [previous maximum-entropy result](../d0_native_complete_cq_source_2026-10-22/MAXIMUM_ENTROPY_PREPARATION.md)
retained only the original one-port moment. For that declared forgetting
problem, the actual invariant marginal
`rho_* = Delta^-1 / Tr(Delta^-1)` is its entropy maximizer exactly when
`Delta` has at most two distinct eigenvalues. Its gain has a nonzero
second variation when a degenerate band splits.

This note supplies a different, explicitly executable retained-test map.
Its strongest application is **inside the original finite-cap stopped
first-match process**. Anchor on its actual outcome `1` (blank label,
port one), then observe `n` ordinary blank outcomes `0`. Because the
original comparator retains the port bit, every such zero is a mismatch
with anchor one. These are legal prefixes until the already declared
cap `K`, with every later match and cap-abort leaf retained. Their exact
effects are `4p^3 Delta^2 B^(2n)`, where
`B=I-2p^2 Delta > 0` is the original ordinary-blank Kraus operator.
For `K >= d-1`, the probabilities with `0 <= n <= d-1` make `rho_*`
the **unique** entropy maximizer for every positive native `Delta`, with
no two-band hypothesis or change to that stopped execution. Any more
informative retained family containing these tests has the same
maximizer **at this invariant input**.

There is also a simpler fixed-horizon realization: one full continuation
of `N=d-1` original rounds contains the ordinary-blank prefix effects
`B^(2n)`. Sections 1--2 prove its entropy identity; section 2a gives the
stronger same-stopped-tape application, using the second actual Kraus
outcome as an invertible native anchor.

Consequently the marginal forgetting gain, pulled back to the actual
native invariant section, is identically zero, including every total
field derivative and higher jet. Its independent DATA-input first
reaction is zero there, so its canonical native Poisson adjoint is zero.
This removes the extra marginal-gain source from that specified future
retention problem; it does not cancel the complete history information,
preparation price, or continuation price.

**Execution boundary.** Under the original first-anchor/first-match rule,
an all-blank tape has already stopped after its second round. It does not
contain `blank^n` for `n>2`. The valid stopped words are instead `1,0^n`.
The stopped theorem requires the declared cap `K >= d-1`; increasing a
smaller cap is still a paid change, not an automatic free extension.
The fixed-horizon alternative has its own full continuation charge.
Neither construction selects the compulsory Book03 Info or removes the
complete stopped-history source. `GR_closed=false`.

### Owned inputs, consumed without repeating their suites

- [Original complete channel](../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md),
  sections 1--3: the actual Kraus outcomes, blank map, retained old records,
  original port cost, and no DATA reset between rounds.
- [Native preparation](../d0_native_preparation_closure_2026-10-21/PROOF.md),
  sections 1--4 and 6: inverse-square invariant DATA state, its derivative,
  mixing/Poisson hypotheses, and finite paid-prefix boundary price.
- [Book06](../../../../01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md),
  sections 06.24--06.25: the entropy representative is conditional on the
  specified retained response tests and does not destroy a complete archive.
- [Complete quantum history](../d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_SOURCE.md):
  full finite-tree CQ entropy and its exact source, including all moving
  preparations and conditional work.
- [Original sequential stopped execution](../d0_first_match_wald_2026-10-22/SEQUENTIAL_FULL128_BOOK_RETURN.md),
  sections 2--4: original full128 anchor labels, retained mismatches and
  cap-aborts, the exact stopped subtree normalizer `R_{a,k}(0)=I`,
  and the complete paid comparison/port recursion.
- [Native entropic Poisson source](../../A4D_COMPLETE_NATIVE_FIRST_MATCH_ENTROPIC_POISSON_PREPARATION_AND_HESSIAN_2026_10_22.md),
  sections 3--4: the DATA-input cotangent and actual stationary adjoint,
  with the independent oldRIGHT zero modes preserved.
- [Stationary-section composition](../d0_coupled_cut_partition_2026-10-22/STATIONARY_SECTION_AND_WRITER.md):
  pull back the actual whole source along its true preparation/constraint
  section; do not freeze a moving input or discard independent equations.

The finite-matrix entropy and interpolation arguments below are elementary
tools, not new claims about quantum theory in general. The contribution
is their explicit application to these original native future outcomes.

## 1. The actual blank and a single complete finite continuation

Use the literal finite operator normalization

\[
p=\varphi^{-1},\qquad A=A^*,\qquad \Delta=A^2,\qquad
K_{j,0}=\delta_{j0}I-2p^2N_j^*A,\qquad
K_{j,1}=-2p\sqrt p\,N_j^*A,\qquad N_0=A.
\tag{1}
\]

The label `0` in `K_{0,0}` includes the original blank label, coefficient
qubit and port zero. It is one physical outcome of the full128
instrument, not the union of all port-zero outcomes. Thus

\[
K_{0,0}=B=I-2p^2\Delta,\qquad
\sum_{j,b}K_{j,b}^*K_{j,b}=I.
\tag{2}
\]

The native compression `A` is a contraction. Equivalently, its first
Walsh row is an average of the actual contraction words, and the
adjoint-paired construction makes it selfadjoint. Therefore
`0 <= Delta <= I`. On the regular sector considered here `Delta>0`, and

\[
I\ge B\ge (1-2p^2)I=(\sqrt5-2)I>0.
\tag{3}
\]

This strict positivity is essential: squaring `B` cannot merge its
positive eigenvalues. A hypothetical blank with both positive and
negative eigenvalues would require a separate argument and is not used.

Fix `N=d-1`, with `d=dim(DATA)` on the actual finite invariant carrier.
Execute exactly `N` original full128 rounds. Each round uses its actual
fresh controller; old records and oldRIGHT remain retained. There is no
DATA reset, postselection, repeat-until-success selection, or spectral
projector measurement. Let `omega=(a_1,...,a_N)` and
`K_omega=K_{a_N}...K_{a_1}`. The full instrument is complete:

\[
\sum_{\omega\in\{1,\ldots,128\}^{N}}K_\omega^*K_\omega=I.
\tag{4}
\]

For `0 <= n <= N`, read the prefix event
`C_n={a_1=...=a_n=(0,0)}` from this same full tape; `C_0` is the whole
sample space. Summing all later outcomes gives the exact effect

\[
E_n=\sum_{\omega\in C_n}K_\omega^*K_\omega
 =B^n\left(\sum_{\eta:\,|\eta|=N-n}K_\eta^*K_\eta\right)B^n
 =B^{2n}.
\tag{5}
\]

Thus one horizon supplies the entire finite family. No separately
prepared copies are assumed to define these probabilities. Estimating
them from repeated experimental episodes would require actual repeated
preparations and their costs; exact probability constraints are not an
assertion of exact estimation from finitely many samples.

If `Delta` has `m` distinct eigenvalues and that smaller number is known,
`N=m-1` already suffices. Using the fixed `d-1` avoids changing the
declared test family when bands split or collide. For one native CAR16
Fourier carrier the bound is fifteen rounds. For a larger spatial
carrier `d` is its true dimension, not automatically sixteen.

## 2. Exact entropy selection, with a polynomial certificate

Write the spectral decomposition, for proof only,

\[
\Delta=\sum_{a=1}^{m}\lambda_a P_a,\quad
d_a=\operatorname{rank}P_a,\quad
Z=\operatorname{Tr}\Delta^{-1},\quad
\rho_*=\frac{\Delta^{-1}}Z,
\quad \nu_a=(1-2p^2\lambda_a)^2.
\tag{6}
\]

The positive `lambda_a` are distinct and (3) makes the `nu_a` distinct.
For any density matrix `sigma`, the retained blank moments are

\[
\operatorname{Tr}(\sigma B^{2n})
 =\sum_a\nu_a^n\operatorname{Tr}(P_a\sigma).
\tag{7}
\]

The Vandermonde matrix for `n=0,...,m-1` is invertible, so equality of
the moments of `sigma` and `rho_*` is equivalent to

\[
\operatorname{Tr}(P_a\sigma)=\frac{d_a}{Z\lambda_a}
\quad\text{for every }a.
\tag{8}
\]

No off-diagonal matrix element or within-band quantum state has been
declared observable by these classical tests. Their entropy maximizer
nevertheless follows exactly. Define the Lagrange polynomial

\[
q(x)=\sum_{a=1}^{m}\big[-\log(Z\lambda_a)\big]
       \prod_{b\ne a}\frac{x-\nu_b}{\nu_a-\nu_b}.
\tag{9}
\]

It has degree at most `m-1 <= d-1` and

\[
\log\rho_*=q(B^2).
\tag{10}
\]

For every `sigma` matching the actual moments (5), (10) implies
`Tr(sigma log rho_*)=Tr(rho_* log rho_*)`. Hence, using natural-log
entropy and the ordinary quantum relative entropy,

\[
\boxed{\quad
S(\rho_*)-S(\sigma)=D(\sigma\Vert\rho_*)\ge0.
\quad}
\tag{11}
\]

Equality holds exactly for `sigma=rho_*`. This proves **unique maximum
entropy**, including noncommuting candidate states. The coefficients in
(9) are a mathematical certificate. The execution performs the original
rounds and classical prefix readouts, not `q`, a matrix inverse, a
logarithm detector, or the spectral projectors.

At coincident bands one simply forms (9) over the distinct eigenvalues.
No uniform bound on its coefficients or on a Vandermonde inverse is
claimed. Spectral reconstruction from noisy probabilities and estimates
uniform in a refining dimension require their own conditioning bounds.

## 2a. Stronger application on the original stopped first-match tape

Use the actual full128 flattened labels `0=(j=0,b=0)` and
`1=(j=0,b=1)`. From (1), the second special outcome is

\[
D_1:=K_1=-2p\sqrt p\,\Delta,\qquad D_1^*D_1=4p^3\Delta^2.
\tag{11a}
\]

It is invertible on the same regular sector; no inverse is physically
executed. The original stopped programme retains its first full label
`a`, then compares each later full128 label with `a`, stopping at its
first match or after `K` comparisons. Its actual seven-bit comparator
preserves the port bit. Thus a prefix

\[
w_n=(1,\underbrace{0,\ldots,0}_{n\text{ mismatches}}),
\qquad 0\le n\le K,
\tag{11b}
\]

is valid and has never already matched. When `n=K` it is a retained
cap-abort leaf. For smaller `n`, sum **all** subsequent first-match and
cap-abort leaves. The already owned stopped subtree identity is
`R_{1,K-n}(0)=I`; hence this actual unconditioned prefix effect is

\[
F_n=D_1^*B^nR_{1,K-n}(0)B^nD_1
 =4p^3\Delta^2B^{2n}.
\tag{11c}
\]

This is a sum of genuine retained stopped-leaf probabilities. It is
not a conditional law obtained by discarding other anchors, and the
execution pays for every other anchor and all its subsequent records.
The event `F_0` is simply "the first outcome was 1."

**Stopped entropy theorem.** If the already declared cap obeys
`K >= d-1`, matching the actual probabilities (11c), for
`n=0,...,d-1`, fixes the weights of every spectral block. Indeed

\[
\operatorname{Tr}(\sigma F_n)
 =4p^3\sum_a\lambda_a^2\nu_a^n\operatorname{Tr}(P_a\sigma).
\tag{11d}
\]

The same distinct-node Vandermonde now determines the weighted entries
`lambda_a^2 Tr(P_a sigma)`. Positivity of `Delta` removes the positive
factors and determines the weights themselves. Explicitly, the
polynomial

\[
r(x)=\sum_a\frac{-\log(Z\lambda_a)}{4p^3\lambda_a^2}
       \prod_{b\ne a}\frac{x-\nu_b}{\nu_a-\nu_b}
\quad\text{satisfies}\quad
\log\rho_*=4p^3\Delta^2r(B^2).
\tag{11e}
\]

Thus the logarithm is a real linear combination of the **actual
stopped-prefix effects** `F_n`. The KL certificate (11), unique
maximizer, and all source conclusions below follow on this same
original stopped carrier. No spectral oracle, inverse filter,
postselection, or continuation after a completed stop is inserted.

For a known `m`-band spectrum `K >= m-1` suffices (the original
first-match definition also requires `K>=1`). At the original
two-band CAR16 fixture, even its two-round cap `K=1` already contains
the two needed anchored moments. To retain the theorem throughout an
arbitrary positive sixteen-dimensional native chart, choose the fixed
declared cap `K=15`; then every episode has at most sixteen rounds.
Any larger fixed cap also suffices and has at most `K+1` rounds.
This is an application to the existing capped programme family, not
a proof that G0 chooses that cap. A smaller fixed cap does not inherit
the arbitrary-spectrum statement, and cap/refinement conditioning is
not declared uniform.

## 3. Larger future families and an input-source bound

For a fixed `Delta`, define the mathematical central conditional
expectation

\[
\mathcal E_\Delta(\rho)=
 \sum_a\frac{\operatorname{Tr}(P_a\rho)}{d_a}P_a.
\tag{12}
\]

This is the unique entropy maximizer for the blank moments of an
arbitrary input `rho`. Indeed those moments fix all the block weights;
the maximizer has no between-block coherence and is uniform within each
block. Equivalently the same logarithm argument gives

\[
I_{\rm blank}(\rho,\Delta)
 :=S(\mathcal E_\Delta\rho)-S(\rho)
 =D(\rho\Vert\mathcal E_\Delta\rho).
\tag{13}
\]

For a zero block weight positivity forces the corresponding row and
column of `rho` to vanish, so the support convention in (13) is valid.
In particular `E_Delta(rho_*)=rho_*`.

Now let `F_y` be **any declared set of actual retained future effects**
containing either all (5), or all the stopped effects (11c), on the
same DATA carrier and field value `y`. Each family fixes exactly the
same central block weights for an arbitrary input.
Additional fine-label probabilities or further future experiments may
be retained. Let `M_F(rho,y)` be the maximum-entropy state satisfying
`Tr(sigma T)=Tr(rho T)` for every `T in F_y`. A finite-dimensional
closed feasible set contains `rho`; strict concavity gives a unique
maximizer. The statement also applies to an infinite collection of
effects, as the intersection of their closed affine constraints is
compact. Set

\[
I_F(\rho,y)=S(M_F(\rho,y))-S(\rho).
\tag{14}
\]

The larger constraint set can only lower the maximum entropy. The
central representative (12) need **not** preserve its other future
tests, and is not asserted to equal `M_F` away from `rho_*`. The exact
statement is

\[
0\le I_F(\rho,y)\le I_{\rm blank}(\rho,\Delta_y)
\le D(\rho\Vert\rho_*(\Delta_y)).
\tag{15}
\]

The last inequality is the following exact Pythagorean identity:

\[
D(\rho\Vert\rho_*)=
D(\rho\Vert\mathcal E_\Delta\rho)
+D(\mathcal E_\Delta\rho\Vert\rho_*).
\tag{16}
\]

Both `log rho_*` and the support logarithm of `E_Delta rho` are scalar
on every spectral block, proving (16) by taking traces. No assumption
that `rho` commutes with `Delta` is used.

For completeness, (15) gives a quantitative, rank-change-safe local
source bound. If normalized positive states `rho,sigma` and the segment
between them have least eigenvalue at least `eta>0`, then

\[
D(\rho\Vert\sigma)\le
\frac{\|\rho-\sigma\|_{\rm HS}^{2}}{2\eta}.
\tag{17}
\]

To see this, put `delta=rho-sigma`. Relative entropy with fixed second
argument is the Bregman remainder of `Tr rho log rho`, and

\[
D(\rho\Vert\sigma)=
\int_0^1(1-t)\operatorname{Tr}
 [\delta\,D\log_{\sigma+t\delta}(\delta)]\,dt.
\]

The resolvent formula for `D log` bounds its Hilbert--Schmidt operator
norm by `1/eta`, since `integral_0^infty (eta+s)^(-2) ds=1/eta`.
This proves (17). Applied with `sigma=rho_*(Delta_y)`, it yields

\[
0\le I_F(\rho,y)
\le\frac{\|\rho-\rho_*(\Delta_y)\|_{\rm HS}^{2}}{2\eta}
\tag{18}
\]

on a small faithful neighborhood. Therefore **all first differentials
of this marginal gain vanish at the invariant input**, with respect to
independent trace-zero DATA variations and smooth native field changes.
This conclusion does not require differentiability of a maximizing
state map or spectral projectors at a band collision. A full second
derivative in arbitrary off-section input directions may be nonzero,
and need not be smooth when the constraint rank changes.

## 4. Application to the native preparation and stationary source

The original primitive DATA preparation theorem, on its stated regular
mixing domain, selects exactly

\[
\Phi_y(\rho_*(y))=\rho_*(y),\qquad
\rho_*(y)=\Delta_y^{-1}/Z_y.
\tag{19}
\]

Its actual derivative is retained:

\[
D\rho_*[v]=
-\frac{\Delta^{-1}(D\Delta[v])\Delta^{-1}}Z
+\frac{\Delta^{-1}}{Z^2}
       \operatorname{Tr}(\Delta^{-2}D\Delta[v]).
\tag{20}
\]

Equations (11)--(15) identify the required entropy representative on
this same section without a new preparation:

\[
M_F(\rho_*(y),y)=\rho_*(y),\qquad
\boxed{\ I_F(\rho_*(y),y)\equiv0\ }.
\tag{21}
\]

The right-hand identity is exact on every smooth positive native chart.
All its total jets vanish, including band splitting/collision directions
and derivatives of the retained effects themselves. It is an identity
of the composed scalar even where an off-section maximizing-state map
is not smooth. It removes the previous *one-port* transverse gain
Hessian from this more informative, explicitly specified forgetting
problem; that older one-port theorem remains correct on its own tests.

For the consumed DATA Poisson source formula, write the contribution
of this marginal gain to the physical score as `-I_F/ln(phi)` if Golden
information units are used. At the invariant input (18) gives its
input cotangent `M_I=0` on all trace-zero Hermitian DATA variations.
Choosing the zero representative, its canonical adjoint solves

\[
(I-\Phi_y^*)Y_I=M_I-\operatorname{Tr}(\rho_*M_I)I=0,
\qquad \operatorname{Tr}(\rho_*Y_I)=0.
\tag{22}
\]

Under the already owned primitive DATA hypothesis this gives `Y_I=0`.
Its direct field first source is zero by (18), and its preparation
reaction `Tr[Y_I (D Phi_y)rho_*]` is zero. The stationary-section
pullback therefore removes this **particular marginal** contribution
from `F_phys=a F_ref+R`, whenever that score really contains the declared
gain (14). No other term of `R` is changed. Without primitive uniqueness,
(21) remains true for the stated inverse-square section, but no new
claim that dynamics selects its spectral weights is made.

For a genuinely finite paid preparation producing `rho_L`, not exactly
`rho_*`, the honest residual remains and has the useful bound

\[
0\le I_F(\rho_L,y)\le D(\rho_L\Vert\rho_*(y)).
\tag{23}
\]

This is an exact finite-preparation error bound, not a claim that a
finite prefix prepares the invariant state or that value bounds alone
bound every moving-field derivative. The full finite-prefix source is
still computed by the original forward/backward channel recursion.

## 5. Actual continuation price and the surviving history source

### 5a. The unchanged stopped programme's full charged operator

For the primary stopped application (11c), consume the original charged
recursion without changing its cap, labels or comparison rule. Let
`c_b` be each actual outcome charge and `kappa_ab` its comparison charge,
including every registered fine factory mark on its true carrier. In the
original scalar-mark case define

\[
\mathcal T_a^*(X)=\sum_{b\ne a}K_b^*XK_b,
\quad L_a=\sum_b(c_b+\kappa_{ab})K_b^*K_b,
\quad Q_{a,0}=0,
\quad Q_{a,k}=L_a+\mathcal T_a^*(Q_{a,k-1}).
\tag{24a}
\]

The complete stopped charge, including the first anchor, every
mismatch, final match and capped abort, is the existing exact operator

\[
\mathcal C_K=\sum_a\left(c_aK_a^*K_a+K_a^*Q_{a,K}K_a\right),
\qquad C_K(\rho,y)=\operatorname{Tr}(\rho\mathcal C_K).
\tag{24b}
\]

Its source is the full product-rule derivative
`D C_K=Tr[(D rho) C_K_operator + rho D C_K_operator]`, with every
`D K_b`, moving charge and comparison charge retained in (24a).
For the derived port component, `c_b=1+(b mod 2)` and comparison charge
zero give `L_a=I+4p^3 Delta` for every anchor. The actual comparison
compiler additionally has its owned 28 CNOT, 15 X and 11 Toffoli
logical gates per full128 comparison, whose physical factory charges
are not assumed to equal that integer count. Such additions stay in
the complete charged recursion.

The entropy theorem only uses functions of the records this process
already retains. It does not charge only the rare anchor-one branch,
delete another branch, or replace (24b) by a constant. If those prefix
functions are physically computed by additional work, that work is
also retained and charged. With the same declared cap, no additional
round is required to apply the stopped theorem.

### 5b. Explicit price of the alternative fixed-horizon realization

The charged extension in section 1 is a fixed `N` original rounds.
For each retained word its already derived original port code charge
is `sum_{j=1}^N(1+b_j)`, between `N` and `2N`. Put

\[
E_{\rm port}=4p^3\Delta,\qquad
\rho_j=\Phi_y^j(\rho_0),\qquad
\kappa=\operatorname{Tr}(\rho_*E_{\rm port})=4p^3d/Z.
\]

The exact expected charge and all its source terms are

\[
C_{{\rm port},N}=N+\sum_{j=0}^{N-1}\operatorname{Tr}(\rho_jE_{\rm port}),
\quad
DC_{{\rm port},N}
=\sum_{j=0}^{N-1}\operatorname{Tr}
 [(D\rho_j)E_{\rm port}+\rho_j DE_{\rm port}].
\tag{24}
\]

At the actual invariant input, with fixed `p` and `N`,

\[
C_{{\rm port},N}=N(1+\kappa),\qquad
DC_{{\rm port},N}=N D\kappa,
\quad
D\kappa=\frac{4p^3d}{Z^2}
               \operatorname{Tr}(\Delta^{-2}D\Delta).
\tag{25}
\]

This source is generally nonzero even though (21) vanishes. For another
initial state the existing port Poisson solution
`(I-Phi^*)Y_C=E_port-kappa I`, `Tr(rho_*Y_C)=0`, gives exactly

\[
C_{{\rm port},N}=N(1+\kappa)
+\operatorname{Tr}(\rho_0Y_C)-\operatorname{Tr}(\rho_NY_C).
\tag{26}
\]

Every derivative of these boundary terms remains. The full execution
must additionally pay its actually specified label, coefficient,
controller, fresh-register preparation, clock and archive costs. These
are not determined by the port charge and are not declared free here.
The prefix readout is a function of retained outcomes; any separately
executed computation of that function also retains its actual work and
charge. No zero marginal gain is used to cancel those charges.

### 5c. Complete history information remains

The fixed-horizon extension has a genuine complete measured state
`Gamma_N=direct_sum_omega K_omega rho_0 K_omega^*` on pointer plus
quantum DATA/work. Its separate complete-history gain is

\[
I_{{\rm history},N}=S(\Gamma_N)-S(\rho_0),\qquad
DI_{{\rm history},N}=DS(\Gamma_N)-DS(\rho_0).
\tag{27}
\]

The complete-history theorem supplies its exact finite-tree chain rule,
including all conditional work, moving probabilities and preparation
terms. Equation (21) makes no assertion that (27) is zero. In
particular, the already evaluated original one/two-round history gain
has nonzero sources. The two quantities ask different specified
retention questions and are not added or subtracted twice.

For the primary stopped application, replace the fixed-length words in
`Gamma_N` by the original complete prefix-free stopped leaf set, with
all capped aborts. The same full-tree entropy identity applies. Its
whole stopped-history source survives the zero marginal gain exactly
as (24b)'s charged source does.

If a first-match experiment is stopped on its second blank, using
`N>2` requires a declared actual continuation after that stopping event,
with its original stopped record retained, or a separate fixed-horizon
future experiment with its real preparation and charges. The probability
of a continuation conditional on a stopped state is computed on that
state; it is not substituted for the uninterrupted prefix law (5).
The original stopped task itself is not changed by this proof.

## 6. oldRIGHT and the exact retained scope

Every native test above acts as `E_n tensor I_R` or `F_n tensor I_R`
on a retained RIGHT.
Its probability depends on the actual DATA marginal, whether or not
that marginal is correlated with RIGHT. Therefore the DATA theorem
applies to that marginal with no discarded physical RIGHT register.

It does not identify a joint maximum-entropy representative from DATA
constraints alone. If the actual input is an independent product with
a fixed specified RIGHT marginal `omega_R`, and those marginal
constraints are retained, subadditivity shows the maximum at the
invariant DATA input is `rho_* tensor omega_R`. An independent uniform
oldRIGHT128 then adds `log(128)` to both entropies and zero to their
gain/source. A correlated or pure DATA--RIGHT input can carry a
nonzero joint entropy gain even when its DATA gain is zero; additional
joint constraints must be handled explicitly. Likewise the DATA
Poisson inverse in (22) does not invert the untouched RIGHT zero modes.

The exact new consumer is therefore: on the original complete finite-cap
first-match DATA carrier with declared `K>=d-1`, its already retained
anchored mismatch prefixes supply the unique entropy representative
`rho_*` at every positive spectrum. The fixed-horizon blank-prefix
continuation is a separate sufficient realization. This marginal gain
and its first input reaction are removed from the residual source
without a two-band premise or fitted Info. Compulsory choice of the
full Book03 task/Info, its joint
preparation, absolute charges, Hodge/cut transport and whole geometric
source comparison remain separate inputs.

## 7. Bounded validation

`check_blank_future_entropy.py` loads only the six needed definitions
from the unchanged native constructor (Git blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`). It does not run its suite or
the previous 173 checks. It checks both actual special Kraus outcomes,
the complete anchored first-match prefix effects and their first jets,
the alternative fixed-horizon prefix effects,
the native invariant input's entropy/KL identity against a noncommuting
competitor, its real finite continuation charge/source, and exact
three-band algebraic controls. The three-band control validates the
general linear algebra; it is not claimed to be another physically
selected native fixture.

The proof, rather than a floating-point Vandermonde inversion, supplies
the statement for arbitrary dimension and colliding bands. Numerical
diagnostics are bounded checks, not interval certificates, preparation
admission proofs or mesh-uniform GR estimates. The receipt reports the
precise scientific scope and preserves `GR_closed=false`.
