# BOOK 01 — Condensed Foundations, Finite Registration, and Construction of the Finite Incidence Graph

> **Publication status — v16 publication-proofread draft.**
> Scope: Finite/profinite support, graph birth, retained/archive split, and terminal-role construction.
> Claim discipline: This book owns support construction; matter, gravity, and empirical claims are downstream.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 01.v15 Active support/foundation layer

Book 01 is support and foundation only. It does not prove matter, gravity or cosmology claims. It supplies the finite/profinite carrier on which later books build operators.

```text
finite/profinite support -> graph birth -> retained/traced split -> P_N,Q_N -> finite tick U_N -> Book 02 feedback operator
```

At finite stage `N`:

```text
H_N = H_N^ret direct_sum H_N^tr,
P_N + Q_N = I,
P_N Q_N = 0.
```

`P_N` is the retained/readout projection. `Q_N` is the traced/archive projection. `U_N` is the finite tick. The handoff to Book 02 is:

```text
F_N = P_N U_N^dagger Q_N U_N P_N.
```

The support may be read as condensed/profinite quasicrystalline support: finite local pieces are visible, while projective/profinite organization prevents replacing the theory by a primitive smooth background lattice.

Finite Born support owners:

```text
D0.finite_effect_born_readout_unique
D0.finite_effect_born_no_hidden_response
```

## 01.19a Cut-and-project reading of phase unfolding

The phase-unfolding master chain is tick order -> irrational phi^-2 phase -> finite return modulus -> residue branches, with owner `D0.Geometry.PhaseUnfoldingQuasicrystal`.

## 01.1 Standard-language reading of the foundation

The foundational object is a profinite support represented as a condensed set on profinite test objects:

```math
S_{D0}=\varprojlim_N S_N,\qquad
\underline S_{D0}(T)=\operatorname{Hom}_{\mathrm{cont}}(T,S_{D0}).
```

A physical observable is not an arbitrary morphism out of this object. It is an element of an admissible subfunctor:

```math
\operatorname{Obs}^{D0}(S_{D0})\subset \operatorname{Obs}(S_{D0}),
```

with finite-stage factorization, projection compatibility, a positive response operator, and a halt quotient. Thus D0 words `registration`, `readout`, `four terminal roles A,B,C,D`, and `eight oriented terminal-role states Ω8` are local names for finite instruments and quotient data on this profinite/condensed support.

## 01.2 Role of this book

Book 01 is the first construction book. Book 00 states the entry contract; Book 01 constructs the first mathematical object to which that contract applies. The construction is deliberately before particle ontology, smooth geometry, continuum fields and SI calibration.

Definition. The primitive object is a finite-verifiable registration system. In mathematical language, D0 starts from a profinite/condensed support equipped with a restricted class of admissible morphisms and finite detector operators. In physical language, this is the minimal structure required for a completed measurement record.

The proof path of the book is:

\[
\text{no-monopoly verification}\Rightarrow
S_{D0}^{\varphi}\Rightarrow
\mathcal M^{D0}\subset\mathcal M\Rightarrow
\mathcal H_N,\mathcal D_N,R_N\Rightarrow
x^2=x+1\Rightarrow
\delta_0\Rightarrow
four terminal roles A,B,C,D\times\{\pm\}\Rightarrow
\Omega_8\Rightarrow
V_9\Rightarrow
K(9,11,13).
\]

The feedback-return object is derived, not primitive, and it is kept distinct
from the positive response operator `R_N = D_N^dagger D_N`:

```text
F_N = P_N U_N^dagger Q_N U_N P_N
```

ABCD determines what can be terminally registered; `F_N` determines what returns from the non-registered complement. The Lean owner is `D0.Dynamics.InternalFeedbackResolvent`, with `internal_feedback_forced_by_split`. Book 01 only hands this retained/traced split to downstream operator books; it does not import matter masses, electroweak constants, baryon data, cosmological surveys or neutrino passports.

The book therefore proves construction of the finite incidence graph from finite registration, not by choosing a convenient graph, but by imposing the obligations of address, comparison, halt, response and invariant readout.

## 01.3 No-monopoly verification and the measurement dyad

A physical record cannot be a monopoly assertion. A single unopposed line of information has no internal way to distinguish state from registration, source from detector, or signal from unchecked naming. The first admissible object is therefore a dyad: two independently addressable sides plus a comparison.

D0 writes this as a detector/object exchange:

\[
D\otimes O\longrightarrow O\oplus\mathfrak q.
\]

Here `D` is not a laboratory instrument in the late sense; it is the minimal detector role. `O` is not a particle at this layer; it is the object role presented to comparison. The symbol `\mathfrak q` is the irreducible addressable record quantum. The dyad closes only when the comparison produces a finite registration.

This gives the no-monopoly theorem:

\[
\text{interaction}\Rightarrow\text{information},\qquad
\text{information}\Rightarrow\text{detector/register}.
\]

The converse guardrail is equally important. D0 does not allow a bare information line to count as physics:

\[
\text{information line}\not\Rightarrow\text{physics}.
\]

Physics begins only when the information line enters a finite detector/register relation and admits a positive response functional.

## 01.4 Condensed/profinite support

The support of the first detector is an inverse system of finite address words. Let

\[
S_n=\{A,B\}^n,
\]

with projection maps

\[
\pi_{n+1,n}:S_{n+1}\to S_n.
\]

The profinite support is

\[
S_{D0}=\varprojlim_n S_n=\{A,B\}^{\mathbb N}.
\]

D0 does not use the ambient condensed mapping space without restriction. The physical subfunctor is the D0-admissible one:

\[
\mathcal M^{D0}(S_{D0}^{\varphi})\subset \mathcal M(S_{D0}).
\]

A morphism is D0-admissible only if it is visible through finite stages, has a halt quotient, produces a positive quadratic response, respects direct/return asymmetry, and does not introduce a second hidden calibration section.

The weighted detector path object is

\[
\boxed{ S_{D0}^{\varphi}=(S_{D0},\mu_{\varphi}) }
\]

where cylinder weights are

\[
\mu_{\varphi}([w])=\prod_{i=1}^{|w|}\mu(w_i),\qquad
\mu(A)=p,
\qquad
\mu(B)=p^2,
\qquad
p+p^2=1.
\]

Thus the continuum is not rejected. It is demoted from ontology to test object: a continuum statement is physical only after it factors through finite D0-admissible registration.

### 01.4.1 The D0 condensed site and admissible subfunctor

The previous paragraph gives the support.  The present paragraph fixes the category-level meaning.  Let `\mathsf{ProfFin}` denote the test category of finite sets and profinite limits with continuous maps, equipped with the usual finite-cover topology.  D0 uses the condensed representative

\[
\underline S_{D0}:\mathsf{ProfFin}^{op}\to\mathsf{Set},
\qquad
T\mapsto\operatorname{Hom}_{\mathrm{cont}}(T,S_{D0}).
\]

At finite stage `N`, every admissible section must factor through a clopen quotient:

\[
T\times S_{D0}\longrightarrow T\times S_N\longrightarrow V_N,
\]

where `V_N` is a finite readout object or a finite-dimensional vector space assigned to the detector stage.  The full ambient condensed mapping object is too large because it contains maps with no finite halt, no positive response, and no stable terminal quotient.

D0 therefore uses the subfunctor

\[
\underline{\mathrm{Obs}}^{D0}(S_{D0}^{\varphi})(T)
\subset
\underline{\mathrm{Obs}}(S_{D0})(T)
\]

whose sections are exactly those satisfying the following descent obligations:

1. **finite quotient:** locally on `T`, the section factors through some `S_N`;
2. **operator lift:** the finite factor carries a channel `\mathcal D_N` on `\mathcal H_N=\mathbb C^{S_N}`;
3. **positive response:** `R_N=\mathcal D_N^\dagger\mathcal D_N`;
4. **projection compatibility:** refinement from `N+1` to `N` preserves the readout after applying the projection `S_{N+1}\to S_N`;
5. **halt quotient:** the comparison has a terminal finite quotient, rather than an infinite request for metadata;
6. **single section:** dimensionful external representatives factor through the declared D0 section, not through a hidden second scale.

This is the point at which condensed mathematics enters the physical theory.  A continuum expression is allowed as a test object or an external representative only after it descends to a D0-admissible finite-stage section.  Conversely, a finite numerical expression that does not define such a section is not a physical D0 theorem.

## 01.4a Condensed φ-quasicrystalline support

The D0 condensed/profinite support is a finite information quasicrystal. It is not a smooth primitive continuum and it is not a periodic lattice.

The primitive return phase is φ-rigid:

```math
\alpha_{D0}=\varphi^{-2},
\qquad
\Delta\theta=\frac{2\pi}{\varphi^2}.
```

Because this phase is irrational and has the golden continued-fraction class, it suppresses low-denominator rational locking. The unresolved archive geometry therefore does not collapse into uncontrolled periodic arms.

Visible spatial branches appear only when a finite readout quotient chooses a return modulus `q`. The residue classes modulo `q` become detector-visible geometry:

```text
ordered tick chain
-> irrational φ phase
-> finite return modulus
-> residue branches
-> visible spatial arms
-> tiling-hull patches
```

Thus D0 geometry is finite, ordered, aperiodic and readout-generated. Smooth macro-geometry is the coarse-grained shadow of this non-resonant finite branch order.
### 01.4.2 four terminal roles A,B,C,D as a natural operator cycle over the condensed support

The four terminal roles A,B,C,D roles live inside this admissible subfunctor.  Let `T_\varphi` and `T_\psi` be the two branch endomorphisms of the finite comparison module.  Their finite-stage representatives must form a compatible family

\[
P_{N+1,N}T_{\bullet,N+1}=T_{\bullet,N}P_{N+1,N},
\]

where `P_{N+1,N}:\mathcal H_{N+1}\to\mathcal H_N` is induced by the projection of address words.  Thus the four operators

\[
A_\Sigma=T_\varphi+T_\psi,
\quad
B_N=T_\varphi T_\psi,
\quad
C_+=T_\varphi^2-T_\varphi,
\quad
D_-=T_\psi^2-T_\psi
\]

are not merely scalar equations.  They are natural finite-stage obligations of the condensed detector object.  Removing one of them breaks a different descent condition: `A_\Sigma` breaks the unit section, `B_N` breaks conjugate coupling, `C_+` breaks forward refinement, and `D_-` breaks return/halt descent.

## 01.5 Finite Hilbert stage, response and halt

At finite stage `N` the detector has the finite support

\[
S_N=\{A,B\}^N
\]

and finite state space

\[
\mathcal H_N=\mathbb C^{S_N}.
\]

A detector channel is a finite operator

\[
\mathcal D_N:\mathcal H_N\to \mathcal H_N,
\]

with positive response

\[
R_N=\mathcal D_N^\dagger\mathcal D_N.
\]

For an event projector `\Pi_a`, the finite readout law is

\[
P_N(a)=\frac{\operatorname{Tr}(\Pi_aR_N)}{\operatorname{Tr}(R_N)}.
\]

The amplitude layer, archive layer and probability layer are separated:

\[
\rho_N=|\psi_N\rangle\langle\psi_N|,
\]

\[
\Delta(\rho_N)=\operatorname{diag}(\mu_\varphi([w])),
\]

\[
P_N(a)=\operatorname{Tr}(\Pi_aR_N)/\operatorname{Tr}(R_N).
\]

The archive map `\Delta` is not a loss of rigor. It is the finite operation by which non-terminal continuum metadata is removed from active readout and stored as forgotten/addressed structure. The halt quotient is the statement that a registration is completed when further refinement cannot change the finite event class without violating the D0 admissibility constraints.

## 01.6 Minimal positive-response closure and the equation `p+p^2=1`

The quadratic branch equation is a theorem of the D0 primitive detector skeleton, not an isolated numerical choice. The primitive skeleton consists of the following finite obligations.

The same quadratic response equation `x^2+x-1=0` that defines the finite response split also gives the time automorphism spectrum of `T = [[0,1],[1,-1]]`; the time layer uses the conjugate pair only through finite integer traces.

**Finite stage.** A registration must factor through some finite quotient `S_N` of the profinite support.

**Non-monopoly dyad.** A record cannot be only a direct assertion. It must contain a direct branch and a return branch which checks the direct branch.

**Constructive composition.** Primitive branch weights are produced by finite composition of registered channels. Non-integer powers are not primitive finite-stage morphisms.

**Positive response.** A completed readout is a positive response

```math
R_N=\mathcal D_N^\dagger\mathcal D_N.
```

Thus the first primitive self-return of one registered channel is quadratic. If the direct branch has weight `p`, the first admissible return branch has weight

```math
p\cdot p=p^2.
```

**Single halt.** The primitive audit has one direct exposure and one positive self-return. Additional powers such as `p^3` or `p^4` describe further unresolved iterations before halt; they are runtime descendants, not the primitive return.

**Normalization.** The primitive two-branch audit has one unit section, hence

```math
p+p^2=1.
```

The solution in the physical interval is unique. Since

```math
f(p)=p^2+p-1,
\qquad
f'(p)=2p+1>0\quad (0<p<1),
```

there is exactly one root in `(0,1)`:

```math
p=\frac{\sqrt5-1}{2}=\varphi^{-1}.
```

The conjugate scalar representative is

```math
\psi=1-\varphi=\frac{1-\sqrt5}{2}.
```

The direct and return branch weights are therefore

```math
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1.
```

The detector asymmetry quantum is the centered half-gap

```math
\delta_0=\frac{p_+-p_-}{2}=\frac{\sqrt5-2}{2}=\frac1{2\varphi^3}.
```

This is the active convention. The formula `\delta_0=\varphi^{-3}` is not the active D0 convention. Any script, book section or external bridge using that older convention must be rejected or migrated.

### 01.6.1 Why alternative branch equations are not primitive D0 equations

The equation is not selected because it is pretty. It is selected because all competing primitive equations violate one of the finite-detector obligations.

| candidate | failure |
|---|---|
| `p+p=1` | no positive self-return; symmetric naming rather than verification |
| `p+p^k=1`, `k>2` | hidden intermediate memory before halt; an iterated runtime, not the first return |
| `p+p^\alpha=1`, non-integer `\alpha` | not a finite constructive channel composition on the profinite stages |
| `p+q=1`, free `q` | second hidden branch scale; violates single-section closure |

Thus the primitive assumptions of D0 are the finite detector obligations. The scalar branch equation is the first theorem of those obligations.

### 01.6.2 Recursive distinguishability and the detector ladder

Define

```math
\delta^{(0)}=\delta_0,
\qquad
\delta^{(n+1)}=\delta_0\delta^{(n)}.
```

Then

```math
\delta^{(n)}=\delta_0^{n+1},
\qquad
\frac{\delta^{(n+1)}}{\delta^{(n)}}=\delta_0.
```

The dimension-graded detector quantum is therefore

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

It gives

```math
Q(1)=2\delta_0,
\quad
Q(2)=\varphi^{-2},
\quad
Q(3)=\varphi^{-1},
\quad
Q(4)=1,
\quad
Q(5)=\varphi.
```

The factor `2` is structural: `\delta_0` is half of the branch asymmetry, while `2\delta_0` is the full one-dimensional branch gap.

The split is not numerology. It is the unique minimal normalized finite two-branch audit with a quadratic positive-return response.

## 01.7 The four terminal roles A,B,C,D operator roles

The pair `\varphi,\psi` gives a scalar presentation of the quadratic relation, but D0 does not use the four terminal roles A,B,C,D entries merely as four algebraic equations.  At the scalar level some relations imply others.  At the detector level, however, the four entries are four typed operator roles in one completed readout cycle.

Let `T_\varphi` and `T_\psi` denote the two conjugate branch operators acting on the finite two-branch comparison module.  The four terminal roles A,B,C,D roles are:

\[
A_\Sigma:\quad T_\varphi+T_\psi=I,
\]

\[
B_N:\quad T_\varphi T_\psi=-I,
\]

\[
C_+:\quad T_\varphi^2=T_\varphi+I,
\]

\[
D_-:\quad T_\psi^2=T_\psi+I.
\]

They reduce on scalar representatives to

\[
A:\ \varphi+\psi=1,
\qquad
B:\ \varphi\psi=-1,
\qquad
C:\ \varphi^2=\varphi+1,
\qquad
D:\ \psi^2=\psi+1.
\]

The point is not algebraic independence.  The point is operator completeness:

| role | operator obligation | failure if removed |
|---|---|---|
| `A_\Sigma` | additive normalization / unit section | no finite unit, no normalized halt |
| `B_N` | multiplicative conjugate coupling / norm section | branches become unrelated labels |
| `C_+` | forward branch self-return recursion | no positive branch runtime calculus |
| `D_-` | return branch self-return recursion | no conjugate return / no closed cycle |

Thus four terminal roles A,B,C,D is the minimal four-role operator cycle of the `\varphi` detector relation.  It is not a claim that four scalar equations are independent axioms.  It is a claim that a completed finite detector cycle requires four typed roles: normalization, conjugate coupling, forward recurrence and return recurrence.

The centered distinguishability quantum is then the half-gap of the two normalized branches:

\[
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1,
\]

\[
\delta_0={p_+-p_-\over2}={\sqrt5-2\over2}={1\over2\varphi^3}.
\]

Equivalently,

\[
p_+=\frac12+\delta_0,
\qquad
p_-=\frac12-\delta_0.
\]

The factor `2` is therefore not a convention: it is the passage from full branch asymmetry to centered half-gap.

The dimension-graded quantum follows from the same centered split:

\[
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
\]

This is the active `\varphi`-ladder relation used downstream.

### 01.7.1 Terminal two-port realization of four terminal roles A,B,C,D

The physical two-port detector gives a terminal representation of the same four-role cycle.  For two inputs and two outputs there are four terminal registration roles:

\[
A=(3,3),\qquad
B=(4,4),\qquad
C=(3,4),\qquad
D=(4,3).
\]

This representation is not a new axiom and not a proof by analogy.  It says that the abstract four-role operator cycle has a minimal terminal readout realization: two coalescent roles and two separated/exchange roles.  The sign/phase branch then gives

\[
\Omega_8=four terminal roles A,B,C,D\times\{+,-\}.
\]

The associated role representatives are recorded as

\[
U_A=Id,
\qquad
U_B=I,
\qquad
U_C=J,
\qquad
U_D=K.
\]

The detector closure is therefore not `8` as a graph vertex count.  It is a closed signed terminal role cycle.  The graph begins only after this cycle is lifted.

### 01.7.2 Proof cell: `D0-SCENE-001` eight oriented terminal-role states Ω8 detector cycle

**Claim.**  The first closed detector cycle is the signed four-role cycle

```math
\Omega_8=\{A,B,C,D\}\times\{+,-\}.
```

**Support.**  The support is the terminal four-role readout algebra obtained after the `\varphi` halt quotient.  Its two-port representation is

```math
A=(3,3),\qquad B=(4,4),\qquad C=(3,4),\qquad D=(4,3).
```

**Probe/gate.**  The finite probe is the two-input/two-output detector role comparison.  The sign branch is the orientation/phase branch of the same finite comparison, not an extra fitted degree of freedom.

**Finite operator.**  The four typed branch operators are `A_\Sigma`, `B_N`, `C_+`, `D_-`.  They have scalar shadows `\varphi+\psi=1`, `\varphi\psi=-1`, `\varphi^2=\varphi+1`, and `\psi^2=\psi+1`, but their D0 role is operator-complete rather than algebraically independent.  The terminal representatives `U_A,U_B,U_C,U_D` give four terminal role classes.  Tensoring with the sign representation gives exactly eight signed classes.

**Quadratic readout.**  Observable readout is not the role label itself but the positive response of the corresponding finite channel.  Bosonic and fermionic two-particle quotients select different surviving subspaces of this same eight-state cycle.

**Quotient.**  The quotient is the halt from unresolved continuum metadata to the finite signed terminal role algebra.  The construction of the finite incidence graph marker `V_9` comes only after this quotient.

**Falsification hook.**  If the minimal terminal detector role algebra can be completed without one of the four typed roles `A_\Sigma,B_N,C_+,D_-`, or if the two-port terminal representation requires fewer or more than four pre-sign roles, then `D0-SCENE-001` fails.  A downstream graph or carrier theorem may not repair this failure.

## 01.8 From eight oriented terminal-role states Ω8 to V9 and construction of the finite incidence graph

The signed detector cycle must acquire a graph-birth marker:

\[
V_9=\Omega_8+\omega_0.
\]

Thus

\[
8\quad\text{belongs to detector closure},
\]

while

\[
9\quad\text{belongs to construction of the finite incidence graph}.
\]

The scene is selected by a finite variational obligation, not by a fitted polynomial. The scene functional is

\[
J_{scene}=(\Omega-8)^2+(n_1-\Omega-1)^2+(n_2-n_1-2)^2+(n_3-n_2-2)^2+J_{coup}.
\]

The admissible order constraint is

\[
0<\Omega<n_1<n_2<n_3.
\]

The minimum is

\[
(\Omega,n_1,n_2,n_3)=(8,9,11,13).
\]

Hence

\[
\Omega_8\rightarrow (V_9,V_{11},V_{13})\rightarrow K(9,11,13).
\]

For the selected scene,

\[
|V|=33,
\qquad
|E|=9\cdot11+9\cdot13+11\cdot13=359,
\qquad
|T|=9\cdot11\cdot13=1287.
\]

The graph invariants used downstream include

\[
|V|=33,\qquad rank(A)=3,\qquad nullity(A)=30,\qquad \gamma=10,
\]

and the shell degrees

\[
d_9=24,\qquad d_{11}=22,\qquad d_{13}=20.
\]

Book 01 stops at construction of the finite incidence graph. The action, boundary, matter, gravity and cosmology books may use this scene, but they may not refit it.

## 01.9 Internal causality and the single line/tick section

The internal metrological section is defined before SI calibration:

\[
\ell_0=1,\qquad \tau_0=1,
\]

and therefore

\[
\boxed{c_{D0}=\ell_0/\tau_0=1.}
\]

This is not an external speed postulate. It is the statement that two independent finite records can be compared only through one common invariant line/tick section. External SI speed is a section map:

\[
c_{SI}:\quad [\ell_0]/[\tau_0]\mapsto \mathrm{m/s}.
\]

At the causal-information level, photon and neutrino roles must not be confused with rest-mass ontology. The photon is the neutral line without rest return:

\[
T_B^\gamma=I,
\qquad
D_B^\gamma=T_B^\gamma-I=0,
\]

so

\[
m_\gamma^2\propto \|D_B^\gamma\gamma\|^2=0.
\]

The neutrino is a neutral return without electromagnetic charge. Both appear only after the line/tick and detector support have already been constructed.

## 01.10 Boundary, mass forgetting and cross-book placement

Book 01 does not use downstream bridge formulas to define the foundation. It keeps only the handoff map needed by later books.

| object | Book 01 role | owner book |
|---|---|---|
| boundary/mass forgetting factor (retired q_mass) | now Boundary Residual Eigenvalue r_∂ | Books 03, 04, 07 (migration note in audit) |
| baryon-boundary information coefficient `I_B` | handed off as boundary-response data | Books 03, 04 |
| residual smallness order `I_12` | kept as a finite-cycle audit scale | Books 03, 05 |
| electron terminal coefficient `C_e=1/38` | section dictionary, not a foundation axiom | Books 03, 04 |
| non-reduced Compton section and `Λ_act` | single-section metrology bridge | Book 03 |
| finite circle audit `π_0` | phase-closure audit, not continuum replacement | Books 02, 05 |

The foundation rule is simple: Book 01 constructs support, response and construction of the finite incidence graph. It does not import mass, baryon, electroweak or cosmological bridges back into the primitive layer.
## 01.11 Contradiction theorems

Book 01 closes by rejecting three common false starts.

### 01.11.1 No interaction without information

Any interaction that cannot alter or constrain an addressable registration is not physical inside D0.

### 01.11.2 No information without detector/register

A bare information line is not a physical event. It becomes physical only through finite detector response.

### 01.11.3 Particles are not the bottom layer

Particles are stable re-detection classes over finite detector records. They are not primitive objects of Book 01.

## 01.12 Active guardrails

1. Do not derive `\varphi` from aesthetic decorative φ numerology. Derive it from minimal non-monopoly self-return closure.
2. Do not use `\delta_0=\varphi^{-3}`. The active convention is `\delta_0=1/(2\varphi^3)`.
3. Do not read `\Omega_8` as a graph. It is detector closure; `V_9` is construction of the finite incidence graph.
4. Do not use `K(9,11,13)` as a chosen model space. It is selected by scene obligations.
5. Do not introduce a second scale anchor. `c_{D0}=1`, `\ell_0=1`, `\tau_0=1` are internal; SI values are section maps.
6. Do not treat bridge formulas like `q_{mass}`, `I_B`, `38`, or `\pi_0` as foundation primitives. They are preserved here as cross-references.

## 01.13 Claim coverage from theorem database

| Claim | Status | Name | Forbidden shortcut | Primary/related certs |
|---|---:|---|---|---|
| `D0-FOUND-001` | CORE-FOUNDATION | No-monopoly verification algebra | Do not derive phi from generic unitary contact, Helstrom scans, or entropy linearity alone. | vp_information_line_exchange.py; minimal Popper/dyad certs |
| `D0-FOUND-002` | CORE-FOUNDATION | Minimal addressable record split | Do not use delta0=phi^-3; active convention is 1/(2 phi^3). | vp_information_line_exchange.py |
| `D0-SCENE-001` | CORE-SUPPORT | eight oriented terminal-role states Ω8 detector cycle | Do not treat phi alone as physical geometry before eight oriented terminal-role states Ω8 closure. | d0_core_certificates.py; vp_information_line_exchange.py |
| `D0-SCENE-002` | CORE-ACTION | J_scene selects K(9,11,13) | Do not read J_scene as fitted polynomial for later constants. | d0_graph.py; d0_core_certificates.py; vp_sgate_jscene_backbone_20260522.py |
| `D0-METRO-001` | CORE-FOUNDATION | Single causal line/tick invariant | Do not count c as a second sector anchor. | vp_c_time_length_single_section_closure.py |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | Lambda_act single action section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | vp_calibration_dag_lambda_section_20260522.py; vp_c_time_length_single_section_closure.py |

## 01.14 Integrated theorem: φ-rigidity and dimension-graded detector quantum

This rigidity theorem belongs in the foundation book because it answers the first external objection to the φ split: whether the value can be perturbed and compensated later by a convention.

Let

```math
C(x)=x^2-x-1,
```

and compare the three detector definitions which coincide at the φ point:

```math
p_+(x)+p_-(x)=x^{-1}+x^{-2},
```

```math
\delta_{split}(x)=\frac{x^{-1}-x^{-2}}2,
\qquad
\delta_{linear}(x)=x-\frac32,
```

```math
\delta_{norm}(x)=\frac{x^{-1}-x^{-2}}{2(x^{-1}+x^{-2})}.
```

At

```math
x=\varphi,
\qquad
\varphi^2-\varphi-1=0,
\qquad
\varphi^{-1}+\varphi^{-2}=1,
```

these definitions collapse to the same detector quantum

```math
\delta_0=\frac{\varphi^{-1}-\varphi^{-2}}2
=\varphi-\frac32
=\frac1{2\varphi^3}.
```

Away from \(\varphi\), normalization, algebraic closure and detector asymmetry no longer agree.  Therefore a shifted value of \(\varphi\) is not another member of a smooth D0 family; it requires a new external catalogue choosing which definition to preserve.  Such a catalogue violates the no-monopoly verification rule.

The dimension-graded detector quantum is retained as a foundation invariant:

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

Hence

```math
Q(1)=\varphi^{-3}=2\delta_0,
\quad
Q(2)=\varphi^{-2},
\quad
Q(3)=\varphi^{-1},
\quad
Q(4)=1,
\quad
Q(5)=\varphi.
```

The factor of two is structural: \(\delta_0\) is half of the two-branch asymmetry, while \(Q(1)=2\delta_0\) is the full one-dimensional quantum.  This is the integrated ``phi-ladder quantization'' guardrail.

**Theorem 12.1 — φ-rigidity.**  The φ root is structurally isolated as the unique point where finite detector normalization, quadratic recursion and detector asymmetry coincide.  Perturbing the root separates these three definitions before any particle or cosmological formula is used.

## 01.15 Condensed/profinite formal specification

D0 uses condensed/profinite language as a formal support layer, not as terminology.  Let `Prof` be the category of profinite sets with continuous maps.  The D0 support is a filtered inverse system

\[
S_{D0}=\varprojlim_N S_N,
\qquad
S_N=\{A,B,C,D\}^{N}/\sim_N,
\]

where the equivalence relation is generated only by finite halt, address-stability and role-preserving quotient relations.

The associated representable test functor is

\[
\underline S_{D0}(T)=\operatorname{Hom}_{cont}(T,S_{D0})
\]

for profinite test objects `T`.  The physically admissible observables are not all maps out of this functor.  They form a subfunctor

\[
\operatorname{Obs}^{D0}\subset \operatorname{Obs}
\]

whose sections satisfy the following finite obligations:

1. finite-stage factorization through some `S_N` before comparison;
2. lift to a finite operator family `D_N` compatible with projections;
3. positive response `R_N=D_N^\dagger D_N`;
4. trace or finite quadratic readout;
5. halt quotient and stable re-detection class;
6. naturality under finite refinements:

\[
P_{N+1,N}D_{N+1}=D_NP_{N+1,N},
\qquad
P_{N+1,N}R_{N+1}=R_NP_{N+1,N}.
\]

The `four terminal roles A,B,C,D` cycle is therefore a natural finite-stage operator cycle, not a detached alphabet.  Its four duties are normalization, conjugate coupling, forward recurrence and return recurrence.  Their scalar equations may be algebraically related, but their operator roles are distinct in the admissible detector cycle.

## 01.16 Condensed finite stages and response-order comparison

The D0 condensed/profinite support is not used merely to name an infinite object. It supplies finite stages on which external comparisons can be tested. For a finite quotient `S_N`, every admissible comparison must be phrased in terms of finite response tests:

```math
\Phi_N(\rho)=F(\operatorname{Tr}(\rho R_{N,a_1}),\ldots,\operatorname{Tr}(\rho R_{N,a_k})),
\qquad F\ \text{convex}.
```

A continuum or external observable is admitted only through a projective family of finite approximations preserving these response tests. This adds a bridge-level condition to the D0-admissible subfunctor:

```math
\underline{Obs}^{D0}_{bridge}
\subset
\underline{Obs}^{D0}
\subset
\underline{Obs}.
```

Thus the condensed support does not authorize arbitrary continuum dressing. It forces a finite response-order comparison at each stage.

## 01.17 Finite-frame Born and EPR closures

The foundational detector stage now carries two executed finite proof cells.

### 01.17.1 Finite-frame Born 2.0: effects, coarse-graining and tensor consistency

The detector-stage Born rule is now stated at the finite-effect level, not merely as a two-channel or raw-list normalization.  A finite D0 readout consists of:

```text
finite outcome support I
finite detector support S
nonnegative effects E_i(s) >= 0
nonnegative detector state R(s) >= 0
strictly positive total response Σ_i Σ_s E_i(s)R(s) > 0
```

The raw response of outcome `i` is therefore

```math
r_i=\sum_{s\in S}E_i(s)R(s).
```

The probability readout is forced to be

```math
p_i=\frac{r_i}{\sum_j r_j}.
```

This is not imported from Hilbert-space quantum mechanics.  The matrix trace expression

```math
P_N(a)=\frac{\operatorname{Tr}(\Pi_aR_N)}{\operatorname{Tr}(R_N)}
```

is now only the matrix presentation of the finite-effect sum.  The Lean owner is

```text
D0.finite_effect_born_readout_unique
```

with the no-hidden-response form

```text
D0.finite_effect_born_no_hidden_response
```

This closes the previous weakness: D0 now identifies the finite effect frame that supplies the responses and forbids a second hidden positive state or probability functional at the same detector stage.

Coarse-graining is also not a new probability postulate.  If a map `π : I -> K` merges fine outcomes into a coarse outcome `k`, the coarse response is the aggregate

```math
r_k^{coarse}=\sum_{i:\,\pi(i)=k}r_i.
```

The coarse probability must be the normalized aggregate response.  The Lean owner is

```text
D0.finite_coarse_born_readout_unique
```

Therefore a calculation cannot normalize before and after coarse-graining using different hidden rules.  The same finite response object controls both levels.

Tensor/product readout is treated the same way.  Once a finite product response over `I x K` is frozen, the joint probability assignment is unique:

```text
D0.finite_tensor_born_readout_unique
```

A nonlinear or power readout, for example a rule of the form `p_i ∝ r_i^q`, is admissible only if it still satisfies the response-recovery equation

```math
p_i\sum_jr_j=r_i.
```

At fixed response this collapses pointwise to the Born weight.  If it differs anywhere, it is not a D0 readout.  The Lean owner is

```text
D0.finite_power_readout_no_alternative
```

The active claim is therefore finite and exact:

```text
finite effects + positivity + response recovery + coarse/tensor consistency
=> unique normalized detector readout;
no independent probability knob;
no alternative power readout at fixed response.
```


### 01.17.1a Born 3.0: phase blindness forces the quadratic response

The previous finite-effect theorem still assumed that a positive raw response had already been supplied.  The measurement-theory gap was therefore not the normalization step; it was the origin of the raw response itself.  The active closure is now one level earlier.

At one finite detector atom the amplitude is a two-component phase quadrature

```math
z=(x,y).
```

The most general quadratic detector response on this atom is

```math
Q(z)=a x^2+bxy+c y^2.
```

A detector readout cannot depend on the arbitrary internal quarter-turn of the phase quadrature,

```math
(x,y)\mapsto(-y,x).
```

Imposing `Q(x,y)=Q(-y,x)` for all finite amplitudes gives, by evaluating at `(1,0)` and `(1,1)`,

```math
a=c,\qquad b=0.
```

Hence every phase-blind quadratic detector response has the forced form

```math
Q(z)=a(x^2+y^2).
```

After unit calibration of the detector channel,

```math
Q(z)=x^2+y^2.
```

This is the finite D0 content of the usual `D†D` response.  The probability rule is then not postulated: a finite family of amplitude channels first produces raw responses

```math
r_i=\sum_s\bigl(x_{i,s}^2+y_{i,s}^2\bigr),
```

and the already-proved finite Born readout gives

```math
p_i={r_i\over\sum_j r_j}.
```

The Lean owners are

```text
D0.phase_blind_quadratic_response_is_norm_sq_scaled
D0.unit_phase_blind_quadratic_response_is_norm_sq
D0.finite_amplitude_born_readout_unique
D0.finite_amplitude_born_no_alternative
```

The closure is therefore stronger than finite normalization.  D0 now has the chain

```text
finite phase quadrature
+ quadratic detector closure
+ internal phase blindness
=> squared-norm response D†D
=> unique finite Born normalization.
```

What remains outside this finite theorem is not the Born rule itself, but only the continuum Hilbert-space presentation and analytic-limit comparison.

### 01.17.2 Shared-support EPR representation

Before geometric projection, an entangled pair is a shared finite support, not two independent objects connected by a signal in a pre-existing continuum. With Pauli-stage observables

```math
A_0=\sigma_z,\quad A_1=\sigma_x,\quad
B_0=(\sigma_z+\sigma_x)/\sqrt2,\quad
B_1=(\sigma_z-\sigma_x)/\sqrt2,
```

the finite CHSH operator

```math
\mathcal C=A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1)
```

satisfies

```math
\|\mathcal C\|=2\sqrt2.
```

The D0 statement is therefore not superluminal collapse. It is finite shared-support correlation before the metric shadow is taken.

Entangled readouts are shared-support effects before metric projection.
Two visible regions may be distant after metric projection while still sharing the same archive/cut-and-project source.
No superluminal update is required; the correlation is a support identity before the metric readout.

## 01.18 Spatial branch emergence from finite phase return

D0 does not treat spatial arms, rays, or coordinate branches as primitive continuum objects. A finite ordered registration chain can acquire visible spatial structure when it is read through a cyclic phase quotient. If the tick index is `n` and the phase is `n mod τ`, a near-return `qв‰€mτ` decomposes the tick line into residue branches `n=a+tq`. The phase drift along each branch is controlled by `q-mτ`.

For the D0 circumference surrogate `τ_0=2π_0`, the first nontrivial stable return `44≈7τ_0` yields `φ_Euler(44)=20` admissible branches. This gives the terminal shell count `d_13=20` a dynamical phase-unfolding interpretation: it is the admissible branch count of the first stable finite return, not a free shell label.

## 01.19 Phase-unfolding master chain

D0 no longer treats spatial branching as a primitive geometric background.  An ordered finite registration can generate visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

The strengthened chain is:

```text
tick order
-> irrational phi^-2 phase
-> finite return modulus
-> residue branches
-> detector-visible geometry.
```

The irrational phase is not an optional decoration.  It prevents rational
locking before the detector chooses a finite quotient.  The finite quotient is
then what makes branches visible: residue classes modulo `q` are geometry only
after the readout modulus is fixed.

The D0 structural return

\[
q_T=|four terminal roles A,B,C,D|\,|V_{11}|=4\cdot11=44,
\qquad
m_T=|four terminal roles A,B,C,D|+\operatorname{rank}(A_K)=4+3=7
\]

is the first terminal phase-return window.  Its admissible coprime branch count is

\[
\varphi_E(44)=20=d_{13}.
\]

Thus the terminal shell degree is the branch count of the first stable phase unfolding.

The second return is

\[
q_{EW}=2(|four terminal roles A,B,C,D|+1)(2|V|+|four terminal roles A,B,C,D|+1)=710,
\qquad
m_{EW}=(|four terminal roles A,B,C,D|+1)d_{13}+|V_{13}|=113.
\]

Since \(710/113\) is a near-return for the Euclidean phase circumference, and

\[
\varphi_E(710)=280=|\Omega_8|\cdot 35,
\]

the electroweak radial depth is the per-\(\Omega_8\)-sector branch depth:

\[
D_{EW}=35.
\]

This section upgrades phase unfolding from an illustration to a structural theorem: later scale depths are repeated applications of the same finite tick \(\to\) phase quotient \(\to\) return modulus \(\to\) residue branch \(\to\) quotient mechanism.

Lean owner: `D0.Geometry.PhaseUnfoldingQuasicrystal`.

```text
phi_phase_is_nonperiodic;
finite_return_modulus_unfolds_branches;
quasicrystal_order_not_periodic_lattice.
```

## 01.19a Cut-and-project origin of visible branches

Phase unfolding is a cut-and-project mechanism, not a visual metaphor. The ordered tick chain supplies a non-periodic φ phase; a finite readout quotient chooses a return modulus; the quotient residues become detector-visible branches.

```text
higher-dimensional archive support
-> irrational φ active slice
-> finite quotient window
-> residue branches modulo q
-> visible spatial arms
-> tiling-hull patches
```

The active slice is irrational, so it is not a translational lattice. The quotient window is finite, so the detector still sees coherent branch order. This is the D0 sense in which smooth macro-geometry is the coarse-grained shadow of ordered aperiodic finite support.
## 01.20 Capacity closure of four terminal roles A,B,C,D, Ω8 and V9

The terminal readout alphabet is fixed by finite information capacity. A primitive two-port detector has a binary terminal dyad `D2`. The complete terminal role set is therefore `D2 × D2`, with four roles. This is the four terminal roles A,B,C,D alphabet:

\[
four terminal roles A,B,C,D=D_2\times D_2,
\qquad |four terminal roles A,B,C,D|=4.
\]

The orientation/phase extension adds the unique sign bit:

\[
\Omega_8=four terminal roles A,B,C,D\times\{+,-\},
\qquad |\Omega_8|=8.
\]

A reusable shell also requires a stationary marked witness section `ω0`. Hence

\[
V_9=\Omega_8\sqcup\{\omega_0\},
\qquad |V_9|=9.
\]

The next two shell extensions are the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square. Therefore

\[
V_{11}=V_9\sqcup D_2,
\qquad
V_{13}=V_9\sqcup four terminal roles A,B,C,D.
\]

This gives the first complete scene sizes `(9,11,13)`. The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role.

## 01.21 Hurwitz-rigid phase generator and non-resonant spatial unfolding

The normalized D0 phase generator is not an arbitrary irrational angle.  The
primitive positive-response theorem gives `p+p²=1`, hence the return branch is

```math
\alpha_{D0}=p^2=\varphi^{-2}.
```

The physical phase increment is therefore `2π/φ²`.  By the Hurwitz/continued-
fraction extremality of the `φ` class, this rotation is maximally resistant to
low-denominator rational locking.  In D0 terminology, it is the admissible phase
increment that suppresses uncontrolled metric arms in the unresolved complement.

In the active formalization this is the information-quasicrystal phase:
`D0.Geometry.HurwitzRigidPhaseGenerator` proves `phi_phase_is_nonperiodic`, and
`D0.Geometry.PhaseUnfoldingQuasicrystal` packages the non-periodic phase with
the finite return branch counts.  D0 geometry is therefore ordered but
aperiodic before it is smoothed.

This does not eliminate finite branches.  Branches appear only after a finite
readout quotient chooses a return modulus.  Thus the same chain has two layers:

```text
φ^{-2} irrational rotation  > non-resonant archive smoothing;
finite return modulus q  > residue branch geometry.
```

This closes the compatibility between macroscopic smoothness and finite branch
unfolding.

## 01.22 Forced return windows and non-post-hoc phase unfolding

The phase-unfolding windows used by D0 are not chosen by searching for rational approximants to a circle.  They are forced by terminal capacity.

Let the direct/return dyad have cardinality `D2=2`.  Then the terminal role square has cardinality

```math
|four terminal roles A,B,C,D|=D_2^2=4,
```

the oriented terminal set is

```math
|\Omega_8|=2|four terminal roles A,B,C,D|=8,
```

and the pointed witness shell is

```math
V_9=|\Omega_8|+1=9.
```

The first dyadic extension and terminal-role extension are

```math
V_{11}=V_9+D_2=11,
\qquad
V_{13}=V_9+|four terminal roles A,B,C,D|=13.
```

The first terminal phase-return modulus must saturate all unsiged terminal roles over the first moving dyadic shell.  Therefore

```math
q_T=\operatorname{lcm}(|four terminal roles A,B,C,D|,V_{11})=4\cdot 11=44.
```

The turn count is fixed by terminal role closure plus the three incidence directions of the scene:

```math
m_T=|four terminal roles A,B,C,D|+\operatorname{rank}(A_K)=4+3=7.
```

Thus `44/7` is checked as a phase near-return only after `44` and `7` have been capacity-derived.  Its admissible branch count is

```math
\varphi_{Euler}(44)=20=d_{13}.
```

The second return window is similarly forced after the terminal shell exists.  Define the pointed terminal alphabet

```math
B=|four terminal roles A,B,C,D|+1=5
```

and the bilateral scene line

```math
L=2|V|+B=2\cdot 33+5=71.
```

A full oriented return must include the two-sided orientation, the pointed terminal alphabet and the full bilateral scene line:

```math
q_{EW}=2BL=2\cdot 5\cdot 71=710.
```

The associated turn count is

```math
m_{EW}=B d_{13}+V_{13}=5\cdot 20+13=113.
```

Therefore the second return ratio `710/113` is also not selected by approximation; it is checked after the capacity derivation.  Its admissible branch count is

```math
\varphi_{Euler}(710)=280,
\qquad
280/|\Omega_8|=35.
```

This gives the electroweak radial depth as the per-oriented-role branch depth of the second forced return window.


## 01.23 Final finite-support closures

The following finite-support structures and operators close the foundation of the D0 vacuum:

### Lorentz carrier from terminal role capacity
The terminal role capacity `four terminal roles A,B,C,D = D₂ × D₂` fixes the minimal external quadratic carrier:
$$\eta = \operatorname{diag}(+1,-1,-1,-1).$$
- **Role in the chain**: It is the finite carrier forced by the terminal role obligations of the detector.
- **Guardrail**: A Lorentz-facing bridge is admissible only after a finite Clifford realization satisfies $\{\gamma^\mu,\gamma^\nu\} = 2\eta^{\mu\nu}I$. It does not postulate a background spacetime.

### Projective closure of the two-branch defect plane
The active branch, return branch, and their distinguishability gap form the three nonzero rays of the two-dimensional branch-defect plane over $\mathbb{F}_2$.
- **Lean Owner**: `D0.Spectrum.BranchDefectProjectiveGeneration` (`BranchDefectProjectiveGeneration`).
- **Guardrail**: This is the algebraic origin of the core generation index; it is not a graph-spectrum claim and not a mass formula.

### Topological tick-gauge and archive floor projection
The archive tick parameter is fixed as a topological gauge convention: $\eta = 1$.
- **Lean Owners**: `D0.Geometry.ArchiveTickGaugeFixing` (`eta_absorbs_into_response`), `D0.Probability.ArchiveFloorWaterFilling` (`waterFill_preserves_floor`, `waterFill_mass_if_root`), `D0.Cosmology.ArchiveHomogeneousState` (`canonical_archive_density_is_uniform`).
- **Guardrail**: Changing $\eta$ is not a physical readout. Ad hoc localization coefficients do not define the D0 core density and cannot mutate the topological tick-gauge.

### Born readout as finite effect-frame theorem
A finite detector supplies effects, a detector state, raw responses, coarse-grained responses, and product responses before probability is reported.
- **Lean Owner**: `D0.Core.BornFiniteEffects` (`finite_effect_born_readout_unique`, `finite_coarse_born_readout_unique`, `finite_tensor_born_readout_unique`, `finite_power_readout_no_alternative`).
- **Guardrail**: Probability is not a free normalization convention or a downstream passport weight. Under fixed finite response, every admissible readout collapses to the same Born weight.

### Born 4.0 composition to norm-square
The phase-blind quadratic response of a finite phase-quadrature atom.
- **Lean Owner**: `D0.Core.BornQuadraticOrigin` (`phase_blind_quadratic_response_is_norm_sq_scaled`, `unit_phase_blind_quadratic_response_is_norm_sq`).
- **Certificate**: `05_CERTS/vp_born_quadratic_origin.py` (`(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)`).
- **Guardrail**: Parallelogram quadratic response and quarter-turn phase blindness select the unit norm-square response before Born normalization.

### Torus shell overlap response (Torus Shell Overlap And Born Readout)
The generation/flavour overlap is a finite phase-blind quadratic response: $O_{ij} = |\langle\text{phase}_i | \text{mixed}_j\rangle|^2$.
- **Lean Owner**: `D0.Matter.GenerationOverlapResponseOrigin` (`torus_shell_noncommutativity_forces_nonpermutation_overlap_source`).
- **Guardrail**: The torus supplies the finite shell carrier and noncommuting selector source; Born readout supplies the normalized quadratic response.

### Fixed detector time ladder
The detector is fixed; the division ladder evolves by $T^n$:
$$\psi_n = T^n \psi_0,\qquad R_n = D^\dagger D(\psi_n),\qquad D_{n+1} = D_n = D.$$
The detector is fixed; the division ladder evolves by T^n.
Readout is D^dagger D applied to the T^n-state.
- **Lean Owner**: `D0.Core.FixedDetectorTimeLadder`.
- **Guardrail**: The detector itself is not a hidden dynamical parameter and cannot be retuned between ticks.

### Cut-and-project quasicrystal operator origin
Aperiodic geometry generated by $\varphi^{-2}$ irrational phase return:
- **Lean Owner**: `D0.Physics.QuasicrystalPhenomenology` (`quasicrystal_phenomenology_operator_origin`, `D0PhiCutProject`, cut-and-project quasicrystal geometry).
- **Certificate**: `05_CERTS/vp_quasicrystal_phenomenology_operator_origin.py` (`(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)`).
- **Guardrail**: Generational inflation, archive phason strain, chiral window offset, phason-flip drag, and fractional charge weights are read from a common cut-and-project vacuum support.

## 01.v15 Mobius-Witness topological halting

The signed terminal role cycle is

\[
\Omega_8=ABCD\times\{+,-\}.
\]

The witness/basepoint \(\omega_0\) gives the first addressable graph-birth shell

\[
V_9=\Omega_8\sqcup\{\omega_0\}.
\]

Continuous circulation inside \(\Omega_8\) accumulates the logarithmic trace gradient. The finite event occurs when the circulation closes against \(\omega_0\); this is the terminal halt quotient. The archive sector is not external emptiness. It is the traced complement inside the same finite support, whose self-organization supplies the topological memory layer used downstream by Core-13, tiling hulls, phason strain and boundary capacity.

**Witness Halt Proof (corrected orbit average, Researcher A integration).**
Because the trace gradient has traversed the full signed role cycle before halt, the emitted archive trace is an orbit-averaged shell emission over the group \(G_8\) of symmetries of \(\Omega_8\):

\[
E_\Omega = \frac{1}{|G_8|} \sum_{g \in G_8} P_g F_N P_g^\dagger.
\]

This average is invariant, but it is **not** a scalar multiple of the identity unless irreducibility of the representation on the trace space is separately proved. See also `03_THEORY_MAP/D0_v15_FRACTAL_CONTINUUM_AND_WITNESS_HALTING_PROOF.md`.
