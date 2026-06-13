<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 02 — Mathematical Proof Spine and Invariant Calculus

> **Publication status — v16 publication-proofread draft.**
> Scope: Finite operator identities, feedback positivity, log-det calculus, and theorem-spine ownership.
> Claim discipline: This book owns internal finite identities; external measurements require bridge/passport layers.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 02.v15 Active mathematical spine

Book 02 is the theorem spine for the v15 feedback construction. It receives `P_N`, `Q_N` and `U_N` from Book 01 and proves the finite operator identities used by the sector books.

### Feedback construction

```text
F_N = (Q_N U_N P_N)^dagger (Q_N U_N P_N)
F_N = P_N U_N^dagger Q_N U_N P_N
F_N = P_N - (P_N U_N P_N)^dagger(P_N U_N P_N)
F_N >= 0
0 <= F_N <= P_N
R_N = D_N^dagger D_N
```

Finite Born owners:

```text
D0.finite_effect_born_readout_unique
D0.finite_effect_born_no_hidden_response
```

### Resolvent

```text
G_N(z) = (I - z F_N)^(-1)
det(I - z F_N) != 0
```

The expansion

```text
(I - z F_N)^(-1) = sum_{m>=0} z^m F_N^m
```

is valid only if:

```text
|z| rho(F_N) < 1
```

### Log-det and refined bounds

```text
-log det(I - z F_N)
= sum_{m>=1} z^m/m Tr(F_N^m)
```

With `a = |z| rho(F_N) < 1`:

```text
|-log det(I - z F_N)| <= rank(F_N)[-log(1-a)]
|T_M(z,F_N)| <= rank(F_N)/(M+1) * a^(M+1)/(1-a)
```

### Finite deformation and pressure

`partial_V` is a finite difference or a derivative along a frozen finite matrix family.

```text
Z_N = Tr exp(-beta Delta_N(V)) det(I - z F_N(V))^(-1)
mathsf P_fb = beta^(-1) partial_V log Z_N
```

Gravity proof-spine anchors: Entropic archive gravity interface, Finite spin-2 wave operator, Higher-curvature finite cut, Spectral A2 / EH bridge, Macro Einstein interface.

Book 04 operator-boundary anchor: `02.36.3b Book 04 operator-boundary closure`, `D0.Matter.book04_operator_boundaries_closed`, `nucleon_line_cannot_promote_full_baryon_multiplet`, `lower_hodge_400_cannot_promote_meson_masses`, `missing_scalar_projector_cannot_promote_higgs_yukawa_core`.

## 02.1 Standard proof-language convention

Every proof cell in this book is written in the sequence:

```text
support object -> finite operator/instrument -> positive response -> quotient/coupling -> invariant -> certificate.
```

Internal D0 names such as `archive`, `terminal`, `carrier`, `structural uniqueness / negative-control rigidity`, and `comparison protocol` are not primitives here. They abbreviate traced-out complements, absorbing channels, representation carriers, structural-rigidity/negative-control tests, and external comparison protocols.

## 02.2 Role of this book

Book 02 is the mathematical reference for the corpus. Book 01 constructs the finite detector object and graph-birth lift; Book 02 records the proof calculus that later sector books use when they state action, matter, gravity, or cosmological transfer claims. Sector books may state physical comparison protocols and sector-specific lemmas, but proof-level reductions point back here unless the proof is intrinsically sector-specific.

## 02.3 Proof ownership rule

A D0 claim is proof-complete only when the following data are specified:

```math
(\text{support},\ \text{probe/gate},\ \text{operator},\ \text{quadratic response},\ \text{quotient},\ \text{bridge type},\ \text{falsification hook}).
```

A numerical coincidence is not a theorem. A formula can be retained as an active comparison protocol if it is typed, certified and falsifiable, but it is not a completed derivation until this book supplies the finite operator and uniqueness argument.

The proof-reference chain used throughout is:

```math
\text{finite support}\rightarrow
\text{projector/probe}\rightarrow
S_{gate}/J_{scene}\rightarrow
\mathcal G_{spec}\rightarrow
W_A\rightarrow
\operatorname{Tr}_K(\cdot)\rightarrow
\text{normalized readout/comparison protocol}.
```

## 02.3a Active v15 proof spine

The active proof spine is:

```text
finite detector support
-> φ-rigid phase return
-> condensed tiling hull
-> frozen finite operator
-> positive quadratic response or heat trace
-> quotient/window
-> K-theory / K0 Gap Label or finite spectrum certificate
-> typed observable-transfer bridge
-> falsification hook
```

## Finite cochain complex and Hodge Laplacian

The finite graded incidence complex is the common algebraic carrier for
cochain-level defect, response and heat-trace constructions. The D0 core uses
finite boundary maps and finite Hodge Laplacians, not continuum curvature
tensors, as its master topological object.

Closed-vacuum feedback adds the paired operator `(Delta_N, F_N)`: the Hodge Laplacian supplies the geometry spectrum, and the feedback determinant supplies unresolved return cycles. `F_N=P_N U_N^dagger Q_N U_N P_N` is the feedback-return operator; `R_N=D_N^dagger D_N` remains the positive response/readout operator. Owners: `D0.Cosmology.FeedbackPartitionFunction`, `feedback_determinant_return_cycles`, `feedback_variation_universal_source`.

The admissible finite identities are:

```math
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N)
=P_N-(P_NU_NP_N)^\dagger(P_NU_NP_N),
\qquad F_N\ge0,
\qquad F_N=0\Longleftrightarrow Q_NU_NP_N=0.
```

The complement being nonzero does not force feedback: `Q_N\ne0` alone does not imply `F_N\ne0`.

The resolvent `(I-zF_N)^{-1}` exists when `z^{-1}` is outside the finite spectrum of `F_N`. Neumann and loop expansions require the stricter radius condition `|z|\rho(F_N)<1`, and the determinant trace formula is logarithmic:

```math
-\log\det(I-zF_N)=\sum_{m\ge1}{z^m\over m}\operatorname{Tr}(F_N^m).
```

For a finite deformation parameter `V`, `d_V` means either a declared finite-difference operator on a finite matrix family or an ordinary derivative of a smooth finite-dimensional matrix family.

## 02.CVFT.v5 Refined feedback bounds and compressed pole discipline

For `F=(QUP)^\dagger(QUP)`, rank equality is `rank(F)=rank(QUP)`. If `im(QUP) subset B_boundary(P,Q)`, then `rank(F) <= dim B_boundary(P,Q)`; write `|partial(P,Q)|` only after independent boundary channels have been identified with cut edges.

Let `a=|z|rho(F)<1`. With the analytic logarithm branch connected to `z=0`,

```math
\left|-\log\det(I-zF)\right|\le \operatorname{rank}(F)[-\log(1-a)]\le \operatorname{rank}(F){a\over 1-a}.
```

For real positive `z`, `0<z<1/rho(F)` gives `-\log det(I-zF) <= rank(F)[-\log(1-z rho(F))]`. For the tail

```math
T_M(z,F)=\sum_{m>M}{z^m\over m}\operatorname{Tr}(F^m),
```

the target bound is

```math
|T_M(z,F)|\le {\operatorname{rank}(F)\over M+1}{a^{M+1}\over 1-a},
```

with fallback `rank(P)` when only the ambient retained support is known. `U_eff=PUP` is a contraction; complex pole language belongs to `U_eff`, an effective non-Hermitian transfer, or Feshbach-Schur. Bare positive `F` has real nonnegative spectrum.

No sector may skip from a named operator to a physical observable. The owner chain must show whether the claim is core, certificate-closed, a no-go, a calibration bridge, or an empirical passport.

## 02.K K-theory / Gap Labeling proof spine

K-theory / Gap Labeling enters D0 only after the operator and tiling-hull carrier are frozen. A K0 gap label is not an action term, not a tunable mass correction, and not a new continuum field.

The admissible chain is:

```text
tiling hull
-> frozen finite approximants
-> spectral gap of the frozen operator
-> K0 gap label
-> readout sector index
-> optional external passport
```

The proof cells are:

| cell | obligation |
|---|---|
| hull owner | the support is the φ-quasicrystalline tiling hull or a declared finite approximant |
| frozen operator | the operator is fixed before comparison |
| gap label | the label records a spectral gap of that operator |
| negative control | retuning the operator after comparison is forbidden |
| bridge boundary | external masses, CKM entries or survey values require a separate passport |

## 02.4 Uniqueness obligations for high-sensitivity formulas

The source proof spine identifies formulas that are too high-gain to be justified by numerical success alone. They remain active only with explicit uniqueness obligations.

### 02.4.1 Electroweak radial depth

```math
A_{depth}^{EW}=\varphi^{35}\left(1+{\delta_0\over\varphi}-\varphi^2\delta_0^3\right).
```

The exponent and two correction terms must be selected from the gate-action grammar: terminal scalar anchoring, PNO-axis occupancy, one-way chiral lift, and cubic boundary backreaction. Nearby expressions are rejected unless they satisfy the same admissibility constraints.

### 02.4.2 Charged-lepton generation action

```math
R_g^{D0}=r_gA_{EW}^{p_g}B_g,
\qquad
p_e=0,
\quad
p_\mu={1\over4},
\quad
p_\tau={1\over3}.
```

The powers are not fit exponents. They must come from terminal-cycle localization, PNO-quarter echo and rank-three coherent echo. Boundary factors must be selected from the same action grammar, not inverted from the charged-lepton table.

### 02.4.3 Survey scalar amplitude

```math
A_s^{D0}={(1+\delta_0/4)I_B\over2|V||V_{13}|}.
```

The terminal survey normalization is the full-cycle terminal readout count. The rejected direct expression `(1+delta0/4) I_B` is retained only as a scale-error diagnostic.

### 02.4.4 Stiffness uniqueness protocol

Any formula containing a high-gain factor `φ^N`, `δ_0^N`, or a small rational correction exponent is proof-complete only after the exponent has a finite operator source.  A sensitivity calculation is not enough.  The book must specify:

```math
N=N_{support}+N_{orientation}+N_{return}-N_{quotient},
```

or an equivalent finite trace, determinant, rank, cycle-length or endpoint-count identity.  Alternative choices such as sums instead of products, local rank instead of ordered endpoint pairs, or post-hoc reduced exponents are rejected unless they are selected by the same operator.

The protected examples are:

| quantity | active exponent/source | uniqueness condition |
|---|---:|---|
| gravity length-depth | `99=|V_9||V_{11}|` | boundary length-depth is an ordered two-endpoint map from the observed line sector to the comparison sector; `9+11`, rank, or total `33` count only one endpoint or the wrong support |
| weak-unlock depth | `19=2γ-1`, `γ=(|V|-Rank)/Rank=10` | one forward/return terminal cycle with the halt section removed |
| action section | `38=2(2γ-1)` | full terminal response uses both orientation sides of the weak-unlock cycle |
| electroweak radial depth | `35=|V|+Rank-1=33+3-1` | full addressed carrier plus rank echo with the common unit section quotiented once |
| EM residual exponent | `5/8+δ_0/384` | `5/8=(ABCD+1)/Ω_8`; `384=Ω_8·ABCD·dim(g_light)` |

If any listed source is absent from the active book section, the corresponding result must be labelled `STIFFNESS-PROOF-CELL-MISSING`, not promoted as a closed theorem.

## 02.5 The theorem chain inherited from Book 01

Book 02 does not reintroduce D0 foundations rhetorically; it formalizes the proof calculus used after them.

```math
x^2=x+\mathfrak q,
\qquad
x=\varphi,
\qquad
p=\varphi^{-1},
\qquad
p+p^2=1,
\qquad
\delta_0={\sqrt5-2\over2}={1\over2\varphi^3}.
```

The role of these identities in Book 02 is operational. They define the finite terminal quotient ideal and admissible runtime calculus. A sector formula may use a φ lift, echo, boundary correction or archive leakage only if the use is typed by the finite operator grammar.

### 02.5.1 The `φ`-ABCD operator-cycle theorem

The four ABCD entries must be treated as typed operators, not as four independent scalar axioms.  Let `T_φ,T_ψ` be the two conjugate branch operators of the finite comparison module.  Define

```math
A_?(T)=T_?+T_?,
\qquad
B_N(T)=T_?T_?,
\qquad
C_+(T)=T_φ^2-T_φ,
\qquad
D_-(T)=T_ψ^2-T_ψ.
```

The `φ` detector cycle imposes the operator identities

```math
A_Σ=I,
\qquad
B_N=-I,
\qquad
C_+=I,
\qquad
D_-=I.
```

On scalar branch representatives these are exactly

```math
\varphi+\psi=1,
\qquad
\varphi\psi=-1,
\qquad
\varphi^2=\varphi+1,
\qquad
\psi^2=\psi+1.
```

The scalar equations are algebraically linked, but the operators have different typing:

```text
A_Σ : additive normalization / unit-section operator
B_N : multiplicative coupling / norm-orientation operator
C_+ : forward branch recurrence operator
D_- : return branch recurrence operator
```

Therefore the proof obligation is not scalar independence.  The obligation is cycle completeness: remove any one typed operator and the finite detector cycle loses a required boundary condition.  `A_Σ` removes the unit, `B_N` decouples the branches, `C_+` destroys forward runtime recursion, and `D_-` destroys return closure.  This is the operator sense in which ABCD is minimal.

The terminal two-port readout is a representation of this operator cycle by four role classes

```math
(A,B,C,D)=((3,3),(4,4),(3,4),(4,3)),
```

followed by the sign/phase extension

```math
ABCD\times\{+,-\}=\Omega_8.
```

The theorem is intentionally stronger than an equation table and weaker than a false claim of scalar independence: it states that the completed detector cycle has four typed operator obligations and that the two-port terminal readout realizes exactly four pre-sign roles.

#### 02.5.1.1 Condensed descent form of the ABCD cycle

The operator-cycle theorem is a theorem in the finite-stage condensed setting, not an equation table.  At each quotient `S_N`, the branch operators are finite endomorphisms of `\mathcal H_N`.  The family is admissible only when the squares

\[
\begin{array}{ccc}
\mathcal H_{N+1} & \xrightarrow{T_{\bullet,N+1}} & \mathcal H_{N+1} \\
\downarrow P_{N+1,N} && \downarrow P_{N+1,N} \\
\mathcal H_N & \xrightarrow{T_{\bullet,N}} & \mathcal H_N
\end{array}
\]

commute for `\bullet\in\{\varphi,\psi\}`.  The four ABCD identities are then natural transformations of this finite-stage system:

\[
A_{\Sigma,N}:T_{\varphi,N}+T_{\psi,N}\Rightarrow I_N,
\qquad
B_{N}:T_{\varphi,N}T_{\psi,N}\Rightarrow -I_N,
\]

\[
C_{+,N}:T_{\varphi,N}^2\Rightarrow T_{\varphi,N}+I_N,
\qquad
D_{-,N}:T_{\psi,N}^2\Rightarrow T_{\psi,N}+I_N.
\]

This is why scalar derivability does not settle the physical question.  Scalar derivability says that the four numerical equations live in the same quadratic presentation.  D0 requires more: the four natural operators must be present as finite-stage structure maps.  Their roles are different because they control different compatibility conditions of the admissible subfunctor.

The terminal two-port readout is therefore written as a role-preserving representation

\[
\rho_{2}:\mathsf C_{\varphi}^{D0}\longrightarrow\mathsf R_2,
\]

where `\mathsf C_{\varphi}^{D0}` is the four-obligation operator-cycle category and

\[
\operatorname{Ob}(\mathsf R_2)=\{(3,3),(4,4),(3,4),(4,3)\}.
\]

The representation is faithful on typed roles but is not a replacement for the condensed proof.  Its signed extension gives

\[
\operatorname{Ob}(\mathsf R_2)\times\{+,-\}=\Omega_8.
\]

Thus the proof-cell has three layers:

\[
\text{condensed finite-stage descent}
\Rightarrow
\text{four operator obligations}
\Rightarrow
\text{terminal two-port representation}.
\]

A claim that skips the first layer is only an analogy.  A claim that skips the second layer is only a scalar identity.  A claim that skips the third layer has no terminal detector comparison protocol.

### 02.5.2 Centered half-gap and dimension ladder

From the normalized branches

```math
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1,
```

D0 defines the distinguishability quantum as the centered half-gap

```math
\delta_0={p_+-p_-\over2}={1\over2\varphi^3}={\sqrt5-2\over2}.
```

Hence

```math
p_+=\frac12+\delta_0,
\qquad
p_-=\frac12-\delta_0,
```

and the factor `2` in the one-dimensional quantum is forced by the full gap:

```math
Q(1)=p_+-p_-=2\delta_0.
```

The dimension-graded ladder is therefore

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

This derivation is part of the finite operator grammar.  It is not a numerological use of `\varphi`, and it is not an independent scaling convention.

## 02.6 Condensed admissibility and finite response

The ambient condensed mapping space is not physics by itself. D0 works with a restricted subfunctor:

```math
\mathcal M^{D0}(S_{D0}^{\varphi})\subset \mathcal M(S_{D0}^{\varphi}).
```

A morphism is D0-admissible only if it factors through finite stages, has a detector channel, induces a positive response, admits a halt quotient and gives a stable record under re-detection.

At finite stage:

```math
\mathcal H_N=\mathbb C^{S_N},
\qquad
\mathcal D_N:\mathcal H_N\to\mathcal K_N,
\qquad
R_N=\mathcal D_N^\dagger\mathcal D_N\ge0.
```

The normalized finite readout is:

```math
P_N(a)={\operatorname{Tr}(\Pi_a R_N)\over\operatorname{Tr}(R_N)}.
```

This is the mathematical home of the Born/Hilbert trace ratio. Sector books may discuss physical detectors, but the finite positive response functional is defined here.

## 02.7 Action, gate and scene calculus

The action stack is a finite admissible operator family, not a variational metaphor. The key objects are:

```math
S_{gate},\qquad J_{scene},\qquad \mathcal G_{spec},\qquad W_A.
```

The scene functional is a constraint certificate. It selects finite scene structure under addressability, non-monopoly verification and finite response. The graph scene `K(9,11,13)` is therefore not an arbitrary postulate; it is the selected carrier for the finite detector grammar after the `ABCD × {±} -> Omega8 -> V9` lift.

Book 03 will own the action/operator dynamics as a sector of construction. Book 02 owns the proof form and the guardrails: no continuous polynomial fitting, no untyped scene variation, and no external table as an input to `J_scene`.

## 02.8 Universal quadratic readout

D0 observables are quadratic responses of finite operators:

```math
R=\mathcal D^\dagger\mathcal D.
```

The universal readout form is a normalized trace, determinant, Schur complement or finite spectral functional only after the support, probe and quotient have been fixed. This protects the theory against fitting by replacing a free parameter with a typed finite operator.

The general readout grammar is:

```math
\text{support}\rightarrow\text{operator}\rightarrow\text{positive response}\rightarrow\text{finite quotient}\rightarrow\text{comparison protocol}.
```

## 02.9 Minimal positive-response theorem for the base equation

The base equation used in Book 01 is not a free scalar axiom. It is the normalized scalar shadow of the minimal finite positive-response detector.

**Definition.** A primitive D0 detector audit is a finite-stage two-branch system `(L,R)` with a direct branch `L`, a return branch `R`, one halt quotient, and a positive response functional. Let `p\in(0,1)` be the direct branch contraction. Since the return branch is the first completed positive response of the same registered channel, its primitive scalar weight is the finite composition weight

```math
w(R)=p\cdot p=p^2.
```

The primitive audit is normalized by a single unit section:

```math
w(L)+w(R)=1.
```

Therefore

```math
p+p^2=1.
```

**Uniqueness.** The function

```math
f(p)=p^2+p-1
```

is strictly increasing on `(0,1)`, with `f(0)=-1` and `f(1)=1`. Hence the admissible branch weight is unique:

```math
p=\frac{\sqrt5-1}{2}=\varphi^{-1}.
```

**Exclusion of alternatives.**

- `p+p=1` has no nonlinear return response and collapses the audit to symmetric naming.
- `p+p^k=1` with `k>2` is not primitive: it contains the quadratic return plus additional unresolved iterations, hence extra hidden memory before halt.
- `p+p^\alpha=1` with non-integer `\alpha` is not a finite constructive channel composition in the profinite detector category.
- `p+q=1` with free `q` introduces a second independent branch scale and violates the single-section/no-monopoly rule.

Thus the equation is derived relative to the D0 primitive detector obligations. The obligations themselves are the primitive thesis; the scalar equation is their first theorem.

## 02.10 Runtime, entropy and finite S-matrix

For evolution and scattering, Book 02 fixes the algebraic forms; Books 06--08 own the sector interpretations.

Entropy is archive forgetting or finite dephasing, not an independent thermodynamic postulate:

```math
\rho_N\longmapsto\Delta(\rho_N),
\qquad
S_N=-\operatorname{Tr}(\rho_N\log\rho_N).
```

The finite S-matrix registry is typed by admissible vertices and transition probabilities:

```math
P_{i\to f}={|S_{fi}|^2\over\sum_j |S_{ji}|^2}.
```

A scattering formula is admissible only when it names its finite support, vertex class, response and bridge to an external cross-section or detector record.

### 02.10.1 Proof cell: `D0-MATH-001` finite phi-runtime and terminal quotient ideal

**Claim.**  Runtime is finite in the core D0 calculus; continuum evolution is an external bridge.

**Support.**  The support is the finite admissible detector ladder after the φ halt quotient.

**Runtime/window.**  A finite runtime readout is read over the four-step active window

```math
u_{k+1}=\delta_0u_k,\qquad k=0,1,2,3,
```

with response functional

```math
\mathcal R(P,u_0)=
\sum_{k=0}^{3}(1-\delta_0)\delta_0^k
\operatorname{Tr}(PG^+H_k).
```

**Stop ideal.**  Terms below the `I_12` resolution threshold are not active observables.  They may appear only as bridge diagnostics or as archived residuals, not as new physical correction layers.

**Quadratic readout.**  The observable part of the runtime is the positive trace response above; the formal infinite tail is not an observable D0 object.

**Falsification hook.**  If a claimed core scalar requires active discrimination below the terminal quotient ideal, or if the finite four-step window cannot reproduce the declared readout type, the claim is demoted before any external comparison.

## 02.11 Matter, baryon, meson and hadron proof blocks

Book 02 records the proof grammar for matter-sector support. It does not claim full empirical completion of all hadron multiplets. The current theorem status is:

- baryon exact Hodge support: core support;
- Schur-complement nucleon line: core measurement;
- terminal-destructive proton readout: single-section output;
- neutron beta/archive split and lifetime unlock: single-section output;
- meson lower-Hodge seed: support only, not direct pion mass;
- full `N, Delta, Lambda, Omega` transfer: no-go for the current operator set unless a new invariant spin/flavour transfer operator is derived.

This distinction prevents the old error `support = physical mass`.

### 02.11.1 Proof cell: `D0-HADRON-001` Schur-complement nucleon core

**Claim.**  The nucleon core is a Schur-complement readout of the baryon support operator, not a direct baryon mass.

**Support.**  The baryon support is the weighted 2-simplex Hodge sector of `K(9,11,13)` with positive support gap

```math
\lambda_{B2}=3960.
```

**Probe.**  The proton-like charge probe has quadratic charge readout

```math
Q^2={4\over9}+{1\over9}+{1\over9}={2\over3},
```

so the first active nucleon block is

```math
\lambda_0=Q^2\lambda_{B2}=2640.
```

**Finite operator.**  The degenerate gap space has dimension

```math
(V_{11}-1)(V_{13}-1)=120,
```

and the witness projector satisfies

```math
P_{gap}P_wP_{gap}={1\over9}I_{gap}.
```

With witness weight `eta_w=1/8`, the first shift is

```math
\Delta_1={1\over72}.
```

The Schur complement against the complement of the degenerate gap contributes

```math
\Delta_2={1\over1710720}.
```

The bulk gate shift is

```math
\Delta_{bulk}={2\over3}+\delta_0.
```

**Readout.**  The integrated finite readout is

```math
\lambda_{N-core}=2640.7985901288725.
```

**Guardrail.**  `lambda_B2`, `lambda_0` and `lambda_N-core` are support/core readouts.  None of them is a proton mass until the terminal destructive readout and single action section are applied.

### 02.11.2 Terminal-destructive readout and the 306 action-cost theorem

The proton row is not allowed to contain a naked subtraction.  The number `306` is a finite operator trace in the destructive terminal readout channel.

Let the baryon support operator have the active 2-simplex structural uniqueness / negative-control rigidity gap

```math
\lambda_{B2}=3960.
```

Let the terminal shell, active terminal degree and transport layer be

```math
V_{13}=13,
\qquad
 d_{13}=V_9+V_{11}=9+11=20,
\qquad
V_{11}=11,
```

and let the active rank removed by the stop/gauge directions be

```math
\operatorname{Rank}=3.
```

There are two equivalent finite descriptions of the same terminal-destructive cost.

First, the terminal-shell trace plus the transport checksum is

```math
\Delta_p^{terminal}
=
{\lambda_{B2}\over V_{13}}
+
{\lambda_{B2}\over V_{13}d_{13}V_{11}}
=
{3960\over13}
\left(1+{1\over20\cdot11}\right)
=306.
```

Second, the destructive readout space is

```math
\mathcal H_{dest}
=
\mathcal H_{addr}^{\pm}\otimes\mathcal H_{tr}^{red},
```

with

```math
\dim\mathcal H_{addr}^{\pm}=2V_9=18,
\qquad
\dim\mathcal H_{tr}^{red}=d_{13}-\operatorname{Rank}=17.
```

For the canonical identity-cell operator

```math
M_{dest}=I_{18}\otimes I_{17},
```

the Hilbert--Schmidt action cost is

```math
\boxed{
\Delta_{readout}^{306}
=
\operatorname{Tr}(M_{dest}^{\dagger}M_{dest})
=18\cdot17
=306.
}
```

The equivalence of the two forms follows from

```math
\lambda_{B2}=2V_9d_{13}V_{11}=3960,
```

and

```math
d_{13}V_{11}+1
=20\cdot11+1
=221
=(d_{13}-\operatorname{Rank})V_{13}
=17\cdot13.
```

Thus `306` is neither a fitted proton correction nor a reusable lifetime constant.  It is a destructive-readout action trace.  The physical proton row may use it only in the terminal-destructive readout theorem; any use as a free hadronic parameter, second scale, or neutron-lifetime shortcut is invalid.

## 02.12 Gauge, electroweak, lepton and CKM proof obligations

The gauge and flavour claims are finite operator statements. Hypercharge normalization, electromagnetic runtime normalization, QCD runtime/archive scale, charged-lepton generation action and CKM terminal return are retained as typed claims with explicit guardrails.

The CKM rule is especially strict: a matrix or naming convention is not a physical proof unless the mass-basis terminal-return functor is fixed before comparison. A post-hoc permutation is forbidden.

## 02.13 Gauge and coefficient proof cells

### 02.13.1 `D0-CARRIER-001` unique light gauge carrier

A D0-admissible compact positive light gauge carrier must preserve the signed detector cycle, rank and single-section anchor:

```math
\Omega_8=8,\qquad Rank=3,\qquad 1\text{ section anchor}.
```

Hence

```math
\dim\mathfrak g=8+3+1=12,
\qquad
rank\,\mathfrak g=4=ABCD.
```

The compact positive decomposition compatible with the finite carrier action is

```math
\mathfrak g=\mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak u(1),
```

up to finite global quotients and gauge/archive equivalence.  Non-compact real forms and additional light factors fail the positive-response and single-section tests.

### 02.13.2 `D0-CARRIER-002` Lorentz and Einstein--Hilbert carrier

External active readout has one runtime direction and three comparison directions, so the admissible external quadratic form has signature

```math
(1,3).
```

The geometric carrier enters through the four-dimensional heat trace

```math
\operatorname{Tr}e^{-s\Delta}\sim(4\pi s)^{-2}\int\sqrt g\,(a_0+a_1sR+O(s^2)).
```

The `a_1 R` term is the leading curvature channel compatible with locality, second-order dynamics and the four-role finite readout.  This is a carrier theorem, not a complete nonlinear catalogue of all gravitational solutions.

### 02.13.3 `D0-COEFF-001` hypercharge and carrier weak angle

The carrier normalization is

```math
k_Y={ABCD+1\over Rank}={5\over3}.
```

Therefore

```math
g_1^2={5\over3}g_Y^2,
\qquad
g_Y^2={3\over5}g_U^2,
```

and the carrier weak angle is

```math
\sin^2\theta_W^{carrier}
={g_Y^2\over g_2^2+g_Y^2}
={{3/5}\over 1+3/5}={3\over8}.
```

The carrier value is not the low-energy dressed measurement; runtime/radiative dressing is a separate typed layer.

### 02.13.4 `D0-COEFF-002` electromagnetic runtime normalization

The internal U(1) whitening value is

```math
\alpha_{top}^{-1}={359\over\varphi^2}-\varphi^{-5}=137.03562809503825.
```

The runtime electromagnetic normalization is

```math
\alpha_{D0}^{-1}=\alpha_{top}^{-1}q_{res}^{5/8+\delta_0/384},
```

with

```math
q_{res}=1.0000043305576405,
\qquad
5/8+\delta_0/384=0.6253073801790362.
```

Thus

```math
\alpha_{D0}^{-1}=137.035999177578.
```

The exponent is a theorem obligation: active plus anchor over `Omega8` with the finite detector-cell correction.  It is not a fitted real number.

### 02.13.5 `D0-COEFF-003` QCD runtime and archive scale

The strong coupling runtime readout at the electroweak scale is

```math
\alpha_s^{D0}(M_Z)=
2\Omega_8\alpha_{D0}q_{mass}^{-6}
\left({\pi_0\over\pi}\right)^{2d_9-2/Rank}.
```

With

```math
\Omega_8=8,\qquad Rank=3,\qquad d_9=24,
```

```math
q_{mass}=(1+\delta_0^3)^{-1}=0.9983582475962778,
\qquad
\pi_0={6\over5}\varphi^2=3.1416407864998739,
```

this gives

```math
\alpha_s^{D0}(M_Z)=0.117999943841492,
\qquad
g_3^{D0}=1.217715495224055.
```

The archive/confinement scale is typed separately:

```math
\Lambda_{QCD}^{D0}=\Lambda_{act}\varphi^5q_{mass}^{-(d_9+2Rank)}=226.229639977528\,\mathrm{MeV}.
```

The active colour selection rule is triality zero:

```math
(n_q-n_{\bar q})\bmod3=0.
```

### 02.13.6 Analytic proof cell for the electromagnetic residual exponent

The residual exponent in the electromagnetic runtime normalization is not a fit parameter.  It is a finite carrier-cell exponent.

The leading rational part is

```math
{5\over 8}={ABCD+1\over \Omega_8}={4+1\over 8}.
```

The numerator `ABCD+1` is the four terminal readout roles plus the unit section.  The denominator `Ω_8` is the signed terminal octet.

The finite-cell correction is

```math
{1\over384}={1\over \Omega_8\,ABCD\,\dim\mathfrak g_{light}}
={1\over 8\cdot4\cdot12},
```

where

```math
\dim\mathfrak g_{light}=\dim\mathfrak{su}(3)+\dim\mathfrak{su}(2)+\dim\mathfrak u(1)=8+3+1=12.
```

Thus the exponent used in Book 04 is

```math
\eta_{EM}={5\over8}+{\delta_0\over384}.
```

This analytic cell is the proof obligation for `D0-COEFF-002`.  A script may verify the arithmetic, but the script is not the source of the exponent.  If the carrier is changed, `Ω_8`, `ABCD`, or `dim g_light` changes and this exponent is invalidated.

## 02.14 Carrier, coefficient and gravity proof blocks

Carrier claims are not independent metaphysics. They are downstream carriers of the finite detector grammar. The light gauge carrier, Lorentz/EH carrier and F-theory admissible carrier are therefore classified as carrier/support bridges.

Metrology claims follow the single-section rule:

```math
c_{D0}=1,
\qquad
\ell_0/\tau_0=c_{D0}.
```

The Planck/Newton and length-depth maps are shadows of a finite action section, not second anchors. A proof fails if it introduces proton, `W/Z`, `G_N`, `H_0`, Planck or dark-sector data as an extra scale unless the row explicitly has external-bridge status.

## 02.15 Archive pressure and spectral transfer

The current canonical theorem schema for transfer is:

```math
C_{static}^{D0}\rightarrow L_D\rightarrow \operatorname{Spec}(L_D)\rightarrow S_{DE}(u)\rightarrow\mathcal T_{\mathcal O}^{D0}\rightarrow\mathcal O_{obs}.
```

The BAO/archive-pressure comparison protocol is a strong empirical example, but this book records the general typed rule: the static coefficient, finite spectrum and transfer window must be fixed before external comparison.

## 02.16 Archive/cosmology proof cells

### 02.16.1 `D0-COSMO-004` static archive-pressure coefficient closure

The static cosmological coefficient row is closed only as a single-section/bridge-output interface. It does not make `H_0`, `Omega_m`, `Omega_Lambda` or `r_d` primitive D0 constants. Those entries are external comparison coordinates attached after the finite archive coefficient and boundary operator are fixed:

```math
(H_0^{D0},\Omega_m^{D0},\Omega_\Lambda^{D0},r_d^{D0})
```

before any BAO or survey-shape transfer. The proof object is the fixed archive coefficient and associated finite boundary operator; survey residuals may not alter the bridge coordinates, and the coordinates themselves are not advertised as exact internally computed D0 observables.

### 02.16.2 `D0-COSMO-005` S_DE finite-window archive-transfer shape

Given the fixed static tuple, the dynamic archive-pressure transfer has the typed form

```math
H_{D0}(z)=H_{\Lambda CDM}(z)\exp\Theta_{D0}(z),
```

with

```math
\Theta_{D0}(z)=A_cG_{log}(z;z_c,\sigma_c)-A_rG_{log}(z;z_r,\sigma_r)-\theta_0e^{-(z/\xi_5)^2}.
```

The logarithmic window is

```math
G_{log}(z;z_0,\sigma)=\exp\left[-{1\over2}\left({\log(1+z)-\log(1+z_0)\over\sigma}\right)^2\right].
```

The window parameters must be obtained before external comparison:

```math
z_c=\varphi(\lambda_c-1),\qquad z_r=\varphi(\lambda_r-1),
```

```math
\lambda_c=1.420943058495791,
\qquad
\lambda_r=1.5790569415042093,
```

```math
\sigma_c=\Delta D_{SDE}+\epsilon^2=\delta_0,
\qquad
\sigma_r={\sigma_c\over\sqrt\varphi},
```

```math
A_c={\sigma_c\over\sqrt5},
\qquad
A_r=A_c(\lambda_r-1).
```

This is the proof cell that prevents the BAO shape from being a hidden ansatz: centers, widths and amplitudes are derived from the finite spectral window and only then compared to survey data.

## 02.17 Claims owned or cross-owned by this book

| Claim | Status | Name | Stage | Forbidden shortcut | Falsification hook |
|---|---|---|---|---|---|
| `D0-FOUND-001` | CORE-FOUNDATION | No-monopoly verification algebra | Foundation | Do not derive phi from generic unitary contact, Helstrom scans, or entropy linearity alone. | A different internally normalized minimal non-monopoly audit algebra would pressure this row. |
| `D0-FOUND-002` | CORE-FOUNDATION | Minimal addressable record split | Foundation | Do not use delta0=phi^-3; active convention is 1/(2 phi^3). | A different direct/return closure with no external catalogue. |
| `D0-FOUND-003` | CORE-FOUNDATION | Minimal continuum-measurement skeleton | Foundation | Do not claim all mathematical cuts are φ; claim is minimal measured connected division. | A non-φ finite, path-independent, internally normalized detector split. |
| `D0-SCENE-001` | CORE-SUPPORT | Omega8 detector cycle | Detector Cycle | Do not treat phi alone as physical geometry before Omega8 closure. | Failure of detector-cycle construction or cycle count. |
| `D0-SCENE-002` | CORE-ACTION | J_scene selects K(9,11,13) | Gate/Action | Do not read J_scene as fitted polynomial for later constants. | Different admissible zero of the same typed obligations or wrong graph invariants. |
| `D0-MATH-001` | D0-RESOLUTION-EXACT | Finite phi-runtime and terminal quotient ideal | Quotient/Resolution | Do not add infinite correction layers below I12. | A physical scalar claim requires distinguishing below I12 inside D0 grammar. |
| `D0-ACTION-001` | CORE-ACTION | S_gate/J_scene backbone | Gate/Action | Do not close Born, entropy, leptons, or dynamics by unrelated formulas. | Mismatch between books or failure of Boundary Residual Eigenvalue r_∂ / I_B / action-spine consistency. |
| `D0-METRO-001` | CORE-FOUNDATION | Single causal line/tick invariant | Bridge/Dictionary | Do not count c as a second sector anchor. | Reproducible line/tick records require multiple elementary speeds. |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | Lambda_act single action section | Single Section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | Any closed prediction requiring an independent sector scale. |
| `D0-BOUND-001` | D0-RESOLUTION-EXACT | Boundary Residual Eigenvalue r_∂ and boundary curvature residual | Quotient/Resolution | Do not fit q_res with arbitrary scalar factor or reopen an infinite residual spiral. | Boundary residual cannot be produced below I12 by admissible cell. |
| `D0-QM-001` | CORE-MEASUREMENT | Born/Hilbert finite trace ratio | Quadratic Readout | Do not postulate continuum Hilbert space before finite trace. | Negative or unnormalized probabilities from finite Hessian readout. |
| `D0-THERMO-001` | CORE-MEASUREMENT | Finite-window entropy from archive forgetting | Quadratic Readout | Do not import continuum entropy postulate as core. | Non-finite trace or unnormalized window entropy. |
| `D0-DYN-001` | CORE-RUNTIME | Normalized tick and witness transport | Runtime | Reject raw T=A-phi^-1 I as propagation operator. | Non-normalized or non-positive dynamic readout. |
| `D0-VERTEX-001` | CORE-RUNTIME | Finite S-matrix registry | Linear Exchange | Do not compare raw graph amplitude directly to event count. | Failure of finite amplitude normalization or type split. |
| `D0-GAUGE-001` | CORE-RUNTIME | U(1) topological normalization and photon benchmark | Runtime | Do not treat gamma/Z interference or event counts as closed by photon-only cert. | Failure of whitening identity or photon benchmark arithmetic. |
| `D0-EW-001` | CORE-RUNTIME | W/Z runtime ratio and on-shell angle | Runtime | Do not use 3/13 or common-kernel variants as physical angle. | Failure to derive asymmetric kernels or trace ratio. |
| `D0-EW-002` | ACTIVE-PASSPORT | EW radial depth and Higgs anchor | Gate/Action | No M_Z second GeV anchor; no underived phi^35 ansatz. | Gate-action derivation fails or neighbouring admissible formula survives. |
| `D0-LEPTON-001` | CORE-MEASUREMENT | Charged-lepton operator selector | Gate/Action | No Lucas-number or inverse-cycle blow-up formula as premise. | Another admissible branch satisfies all criteria or selected branch fails. |
| `D0-LEPTON-002` | ACTIVE-PASSPORT | Charged-lepton generation action | Single Section | No fit-led Lucas or inverse-target selection. | Branch exponents/boundary factors not uniquely selected by action grammar. |
| `D0-CKM-001` | CORE-MEASUREMENT | PNO cyclic orientation CKM seed | Linear Exchange | No raw node-space RMS or row/column permutation. | PNO algebra does not select O_cyc/order. |
| `D0-CKM-002` | BARE-D0-READOUT | CKM mass-basis terminal-return closure | Quadratic Readout | No post-hoc permutation after seeing data. | Mass-basis/naming matrix not reproduced or not stochastic. |
| `D0-BARYON-001` | CORE-SUPPORT | Exact baryon Hodge spectrum | Finite Support | 3960 => proton mass is forbidden. | Counterexample to exact unweighted or weighted spectra. |
| `D0-BARYON-002` | CORE-MEASUREMENT | Charge-squared PDF minimality | Quadratic Readout | Do not import collider PDFs as D0 input. | Another admissible family point gives same target or Q^2 readout fails. |
| `D0-HADRON-001` | CORE-MEASUREMENT | Hadron Schur-complement nucleon core | Quadratic Readout | Do not read intact core directly as proton mass. | Schur identity or gap perturbation fails. |
| `D0-PROTON-001` | SINGLE-SECTION-OUTPUT | Terminal-destructive proton readout | Single Section | Do not use proton mass as anchor; do not reuse 306 as neutron shortcut. | 306 action trace or terminal formula fails. |
| `D0-NEUTRON-001` | SINGLE-SECTION-OUTPUT | Neutron beta/archive mass split | Single Section | Do not input neutron/proton masses. | Mass split operator fails or sign not justified. |
| `D0-NEUTRON-002` | SINGLE-SECTION-OUTPUT | Neutron beta/archive lifetime unlock rate | Runtime | Rejected 306/13 lifetime shortcut. | Exponent, phase-space power, or normalization cannot be derived/certified. |
| `D0-PHOTON-001` | CORE-MEASUREMENT | Photon massless carrier | Quadratic Readout | Do not introduce photon rest mass without breaking c_D0 line invariant. | Pure line carrier has nonzero rest-return defect. |
| `D0-NEUTRINO-001` | CORE-MEASUREMENT | Neutrino neutral leakage mass-square pattern | Quadratic Readout | Do not fit neutrino masses independently if electron section used. | Oscillation ratio excludes delta0/4 under correct bridge. |
| `D0-CARRIER-001` | CORE-SUPPORT | Unique light gauge carrier | Finite Support | Do not treat SM constants as primitive after carrier closure. | Alternative D0-admissible light carrier survives constraints. |
| `D0-CARRIER-002` | CORE-SUPPORT | Lorentz and Einstein-Hilbert carrier | Finite Support | Do not claim full nonlinear GR catalogue from carrier form alone. | No stable (1,3) or heat-trace R channel. |
| `D0-FTHEORY-001` | EMPIRICAL-PASSPORT | Lin-Weigand 2016 D0 admissible carrier | External Comparison Protocol | Do not promote raw string moduli disappearance or F-theory as D0 axiom. | Any component of F_D0 nonzero after correct quotient. |
| `D0-COEFF-001` | CORE-RUNTIME | Hypercharge normalization and carrier weak angle | Runtime | Do not confuse carrier 3/8 with measured low-energy angle. | Hypercharge index not selected by D0 carrier grammar. |
| `D0-COEFF-002` | CORE-RUNTIME | Electromagnetic runtime normalization | Runtime | Do not fit alpha by changing graph seed or q_res. | Runtime exponent not derived or value fails cert. |
| `D0-COEFF-003` | CORE-RUNTIME | QCD runtime and archive/confinement scale | Runtime | Do not confuse QCD archive scale with cosmological dark/archive pressure. | Coefficient formula or triality-zero selection fails. |
| `D0-MATTER-001` | CORE-RUNTIME | Matter/Yukawa/CKM operator closure | Bridge/Dictionary | No hidden mass scale, post-hoc permutation, or fit-led lepton/CKM constants. | Dressing comparison requires changing D0 source object. |
| `D0-GRAV-001` | SINGLE-SECTION-OUTPUT | Length-depth theorem and Planck/Newton shadow | Bridge/Dictionary | No raw edge-density G_N; no reduced-Compton convention at full-cycle section; no terminal denominator swap. | Semantic alternatives beat canonical depth under same typed obligations or cert fails. |
| `D0-GRAV-002` | SINGLE-SECTION-OUTPUT | Newton coefficient finite-cycle holonomy closure | Bridge/Dictionary | Do not patch hbar by pi0; do not introduce Planck/G anchor. | Holonomy exponent/transfer not derivable or coefficient fails cert. |
| `D0-GRAV-003` | D0-RESOLUTION-EXACT | Higher-curvature finite cut rule | Quotient/Resolution | Do not add free higher-curvature couplings below D0 resolution. | Continuum correction above cut requires active unclosed term. |
| `D0-COSMO-001` | CORE-MEASUREMENT | Archive-pressure operator | Quadratic Readout | Do not fit w_a as CPL free parameter inside D0. | Archive pressure sign/scale excluded under correct survey bridge. |
| `D0-COSMO-002` | ACTIVE-PASSPORT | Scalar survey amplitude comparison protocol | External Comparison Protocol | Do not compare raw (1+delta0/4)I_B directly to survey data. | Terminal normalization not uniquely derived or survey pass fails with fixed seeds. |
| `D0-COSMO-004` | SINGLE-SECTION-OUTPUT | Cosmological archive-pressure coefficient closure | Single Section | Do not alter H0/Omega/r_d to fit BAO; use transfer layer. | Static coefficient tuple excluded by fixed-parameter likelihoods. |
| `D0-COSMO-005` | EMPIRICAL-PASSPORT | S_DE finite-window BAO archive-transfer shape | External Comparison Protocol | Do not move H0/Omega_m/r_d or fit shape amplitudes to target data. | Future BAO/SN releases fail fixed transfer with no refit. |
| `D0-COLLIDER-001` | EXTERNAL-BRIDGE | Collider runtime typed bridge | Bridge/Dictionary | No raw amplitude-to-event-count comparison. | Bridge requires hidden D0 core fit parameters. |
| `D0-PI0-001` | CORE-FOUNDATION | pi0 finite-cycle versus pi continuum generator | Quotient/Resolution | Do not replace pi by pi0 inside hbar or Planck definitions. | Typed finite-cycle/continuum distinction inconsistent with bridges. |
| `D0-MESON-001` | CORE-SUPPORT | Meson lower-Hodge support seed | Finite Support | 400 => pion mass or sqrt(3960/400) => hadron ratio is forbidden. | Lower-Hodge calculation fails. |

## 02.18 Integrated rigidity calculus: local structural uniqueness / negative-control rigidity is a proof obligation, not a fit

The structural uniqueness / negative-control rigidity calculus belongs in the mathematical proof spine because it turns high-gain numerical formulae into uniqueness obligations.

For any downstream dimensionless readout \(Y(\varphi)\), define the local structural uniqueness / negative-control rigidity exponent

```math
\kappa_Y=\left.\frac{d\log Y}{d\log \varphi}\right|_{\varphi=\varphi_0}.
```

A closed D0 formula must declare whether a large \(|\kappa_Y|\) is forced by the detector construction or imported as a fragile numerical coincidence.  The old rigidity audit recorded the following representative structural uniqueness / negative-control rigidityes under the fixed stress convention:

| readout | representative structural uniqueness / negative-control rigidity role |
|---|---:|
| gravity depth / \(G_N\) | large negative exponent from \(D_L\sim\varphi^{99}\), hence \(G_N\sim\varphi^{-198}\) |
| electroweak radial readout | high positive radial exponent |
| charged-lepton ratios | finite generation selector structural uniqueness / negative-control rigidity |
| survey scalar amplitude | archive/window structural uniqueness / negative-control rigidity |
| neutron lifetime | terminal weak factor structural uniqueness / negative-control rigidity, including powers of \(\delta_0\) |

This is not a phenomenological sensitivity table in the active proof path.  It is a no-deformation certificate: a nearby value of \(\varphi\) destroys the agreement between detector split, algebraic closure and downstream typed sections.

**Proof discipline.**  Any high-gain D0 expression must now be accompanied by one of the following:

1. an internal uniqueness proof;
2. a rigidity/no-deformation proof;
3. an explicit demotion to bridge/comparison protocol status.

This integrated rule strengthens the anti-numerology firewall: sensitivity is admissible only when it is the consequence of a closed invariant section.

## 02.19 High-gain uniqueness and structural uniqueness / negative-control rigidity closure

Any formula containing a large exponent or small residual is release-admissible only if the exponent is selected by an operator support rule and neighbouring alternatives are excluded.

### 02.19.1 Electroweak depth `35`

The electroweak radial depth is

\[
35=|V|+\operatorname{Rank}-1=33+3-1.
\]

Here `|V|=9+11+13=33` is the full addressed carrier, `Rank=3` is the three-sector rank echo, and the common unit section is quotiented once.  The alternatives are excluded as follows:

- `33` omits the rank echo and gives only the addressed support.
- `36=33+3` double-counts the unit section.
- `30=|V|-Rank` is the nullity shell and belongs to weak-unlock/action closure, not radial depth.

Thus `35` is not a free exponent but the unique full-support radial depth after unit quotient.

### 02.19.2 Weak-unlock depth `19` and action section `38`

Let

\[
\gamma={|V|-\operatorname{Rank}\over \operatorname{Rank}}={33-3\over 3}=10.
\]

The primitive one-way terminal unlock removes the halt section:

\[
N_{unlock}=2\gamma-1=19.
\]

The action section is the closed forward/return cycle:

\[
N_{act}=2N_{unlock}=38.
\]

Therefore `38` is not calibrated from electron mass; it is the dimensionless finite action-section coefficient.  The electron mass is used only to express the resulting single section in MeV.

### 02.19.3 Gravity line-depth `99`

The gravity line-depth is the ordered bilinear transport from the observed line sector to the comparison sector:

\[
D_L=V_9V_{11}=9\cdot 11=99.
\]

The alternatives fail by type:

- `9+11` counts disconnected endpoints but not ordered line transport;
- `33` counts the full carrier, not a line-depth map;
- rank/nullity counts internal gauge bookkeeping, not length-depth covariance.

Thus `99` is the unique admissible bidegree for the finite length-depth map in Book 07.

### 02.19.4 Electromagnetic residual exponent

The residual exponent in the electromagnetic normalization is

\[
{5\over 8}+{\delta_0\over384},
\qquad
{5\over8}={|ABCD|+1\over |\Omega_8|},
\qquad
{1\over384}={1\over |\Omega_8|\,|ABCD|\,\dim\mathfrak g_{light}}.
\]

Here `|ABCD|=4`, `|Ω8|=8`, and

\[
\dim\mathfrak g_{light}=\dim SU(3)+\dim SU(2)+\dim U(1)=8+3+1=12.
\]

The correction is therefore tied to the terminal role square, signed lift and light gauge carrier dimension.  No empirical value of `α` is used in selecting the exponent.

## 02.20 Convex-response coupling theorem

### 02.20.1 Theorem: D0 bridge closure by response coupling

Let `X_N` be a finite D0 internal observable and `Y_N` a finite external projection. A bridge claim is closed only if there exists a kernel `K_N(y|x)` such that:

```math
X_N \preceq_{D0,cx} Y_N,
```

meaning

```math
\mathbb E\,\Phi_N(X_N) \le \mathbb E\,\Phi_N(Y_N)
\quad
\forall\Phi_N\in Test_{D0}(N),
```

and the response vector is preserved or quotiented by a declared loss map:

```math
\mathbb E_{K_N}[\mathcal R_N(Y_N)\mid X_N]
=
\mathcal R_N(X_N)
```

or

```math
\mathbb E_{K_N}[\mathcal R_N(Y_N)\mid X_N]
=
\pi_{loss}\mathcal R_N(X_N).
```

Among all such kernels, D0 selects the entropy extremal representative:

```math
K_N^*=\arg\max H(Y_N|X_N),
```

after quotienting gauge freedom. The bridge is unique only in this quotient. If such a kernel or uniqueness statement is absent, the claim may remain an internal theorem but cannot be promoted to external bridge closure.

### 02.20.2 Proof-cell role

This theorem imports into D0 the finite-support/order/coupling/entropy pattern: reduce to finite stages, preserve a test class, build a coupling, and select the unique gauge-fixed entropy representative. This closes the earlier gap where some bridge claims had formulas but no explicit bridge object.

Terminology lock: this section uses the words `response tests` and `coupling kernel` literally; bridge closure means an explicit coupling kernel preserving the declared response tests.

## 02.21 Executed finite entropy bridge theorem

A bridge is not closed by a statement of intention.  For finite response grids the bridge must be executed as an entropy-selected kernel.  Let `Y={y_j}` be a finite response grid and let `r` be the retained D0 response.  The admissible bridge kernel is the unique maximizer of

```math
H(q)=-\sum_j q_j\log q_j
```

subject to

```math
q_j\ge 0,\qquad \sum_jq_j=1,\qquad \sum_jq_jy_j=r.
```

For interior `r`, the kernel is forced to be

```math
q_j^*(r)=\frac{\exp(\theta(r)y_j)}{\sum_k\exp(\theta(r)y_k)},
```

where `θ(r)` is uniquely fixed by the mean constraint.  The uniqueness follows because the derivative of the mean map is the variance on the finite grid and is strictly positive for a non-degenerate grid.  Thus the bridge has no free fitting parameter after the response grid and retained response are declared.

This theorem is now the active proof-cell behind the convex-response bridge discipline.  A bridge claim without the executed kernel, KKT check and convex-response check is not promoted beyond bridge-candidate status.

## 02.22 Executed core bridge theorems

### 02.22.1 Theorem: finite positive-frame representation

Let `\mathcal E_N` be the finite effect algebra generated by halted detector projectors. A normalized D0 Born response functional `B_N` on `\mathcal E_N` is admissible iff it is positive, additive on orthogonal joins, and represented by the detector response operator. In finite dimension, positivity and additivity give a unique positive representing matrix `W_N` such that

```math
B_N(E)=\operatorname{Tr}(E W_N).
```

The no-hidden-response rule sets

```math
W_N=R_N/\operatorname{Tr}(R_N),\qquad R_N=D_N^\dagger D_N.
```

Hence the unique normalized finite D0 probability is

```math
P_N(a)=B_N(\Pi_a)=\frac{\operatorname{Tr}(\Pi_a R_N)}{\operatorname{Tr}(R_N)}.
```

The current Lean proof cell separates the finite normalization theorem from the Hilbert-space spelling.  In `D0.Core.BornFinite`, a `FinitePositiveResponse` is a finite family `r_i ≥ 0` with positive total response.  A `FiniteBornReadout` is admissible only when it recovers the raw detector response by

```math
p_i\sum_jr_j=r_i.
```

The theorem

```text
D0.finite_born_readout_unique_on_finite_outcomes
```

proves `p_i=r_i/(Σ_jr_j)` for every finite outcome, and

```text
D0.finite_born_no_alternative_readout
```

proves that an alternative finite probability assignment is impossible under the same detector response.  The finite effect-frame extension `D0.Core.BornFiniteEffects` lifts this from a raw response list to finite effect frames, coarse-graining, tensor/product response and power-readout no-go.  Therefore the proof spine no longer depends on a two-channel-only argument or on importing the continuum Born rule as an axiom.

### 02.22.2 Theorem: finite entropy/coupling macro bridge source

The external HST macro bridge is admissible only after the D0 side supplies a finite centered subgaussian source. With

```math
\mathsf P_{archive}^{D0}=-\frac{\delta_0^8}{30}\Pi_N,
```

the normalized archive atom is bounded and centered. Therefore its moment-generating function obeys the subgaussian estimate required for convex-response comparison. The continuum Gaussian ensemble is not primitive; it enters only through the external macro bridge after the finite archive source has been closed.

### 02.22.3 Theorem: finite CHSH support

The Pauli-stage CHSH operator has norm `2\sqrt2`; therefore the D0 finite shared-support model reaches the quantum Tsirelson bound without a background signal-speed parameter. Spatial separation belongs to the later geometric quotient.

## 02.23 High-gain hostile uniqueness atlas: proof-spine rule

A high-gain scalar is admissible in the proof spine only when it is locked by a finite operator duty.  The atlas uses the following proof-cell form:

```text
operator lock > exact formulation > no-hidden-anchor proof > negative controls > failure meaning.
```

This rule is applied to `306`, `38`, and `99`.  The point is not that these numbers are arithmetically reproducible; the point is that replacing them by a nearest neighbour changes the finite operator being computed.  The atlas is stored in `04_FOUNDATION_CLOSURES/D0_HIGH_GAIN_HOSTILE_UNIQUENESS_ATLAS.md` and is normative for any future high-gain row.

## 02.24 Atlas extension: electroweak depth 35

The high-gain atlas is extended by `D0-UNIQUE-ATLAS-035`.  The electroweak radial-depth exponent is locked by the finite active scene count plus the rank-corrected witness section:
\[
D_{EW}=|V|+\operatorname{rank}(A)-1=33+3-1=35.
\]
The neighbouring tests have nonzero residuals:
\[
\mathrm{res}(34)=-1,
\qquad
\mathrm{res}(36)=+1.
\]
Thus `34` consumes the witness/basepoint section, while `36` introduces a hidden extra active shell.  This proof-cell is structural; it does not use an electroweak mass as input.

---

## 02.25 High-gain hostile uniqueness atlas completion

The high-gain constants are now governed by a single atlas rule: arithmetic reproduction is insufficient. The completed atlas covers 19, 5/8+delta0/384, lambda_c/lambda_r, meson transfers and baryon multiplet transfers in addition to the earlier 306, 38, 99 and 35 entries.

---

## 02.26 External-source proof closure

## 02.27 D0-GAUGE-MATTER-002 — finite cochain Ward/anomaly closure

The gauge-matter bridge must be read in the standard language of a finite oriented cochain complex.  For the clique complex of `K(9,11,13)`:

```math
C^0\xleftarrow{\partial_1}C^1\xleftarrow{\partial_2}C^2,
\qquad \partial_1\partial_2=0.
```

The D0 discrete Ward identity is the active-sector consequence of this finite boundary identity.  Anomaly cancellation is not a prose statement: it is the exact vanishing of the finite rational anomaly ledger before QFT/RG dressing.

The required left-handed Weyl sums are:

```math
A_{33Y}=0,
A_{22Y}=0,
A_{YYY}=0,
A_{grav^2Y}=0.
```

The primary cert is `vp_v1132_gauge_matter_ward_anomaly.py`.

## 02.28 Born/EPR assumption split

The finite trace/Born result is not allowed to hide its assumptions.  A proof-cell must state:

```text
finite outcome support;
nonnegative raw detector responses with positive total response;
response-recovery rule `p_i(Σ_jr_j)=r_i`;
trace-state form only when the sector chooses the Hilbert/projector spelling `r_a=Tr(Π_aR)`;
dimension-2 caveat only for projective-only Gleason arguments, not for the finite response-normalization theorem;
Tsirelson/CHSH operator norm if the claim faces EPR/Bell tests.
```

This does not weaken D0.  It prevents a reviewer from claiming that the Born rule was smuggled in through unspoken Hilbert-space assumptions.

## 02.29 Phase-unfolding and residue-branch theorem

Let `T:n↦n+1` be the finite registration tick and let phase be read modulo a circumference `τ`. If `q≈mτ`, then each residue class `a mod q` defines a branch `a+tq` with phase drift `t(q-mτ)`. Therefore visible arms/rays are residue classes of a finite return modulus.

The admissible branch filter is part of the response structure. In the arithmetic model it is `gcd(a,q)=1`, so the visible branch count is `φ_Euler(q)`. D0 uses the same grammar with a finite detector admissibility filter.

Consequences:

```math
d_{13}=φ_{Euler}(44)=20,
```

and, for the classical large-scale return `710≈113·2π`,

```math
φ_{Euler}(710)=280=|Ω_8|\cdot35.
```

Thus the electroweak depth `35` has a phase-unfolding interpretation as the per-sign branch count after the terminal `Ω_8` quotient.

## 02.30 Phase-unfolding master chain

D0 no longer treats spatial branching as a primitive geometric background.  An ordered finite registration can generate visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

The D0 structural return

\[
q_T=|ABCD|\,|V_{11}|=4\cdot11=44,
\qquad
m_T=|ABCD|+\operatorname{rank}(A_K)=4+3=7
\]

is the first terminal phase-return window.  Its admissible coprime branch count is

\[
\varphi_E(44)=20=d_{13}.
\]

Thus the terminal shell degree is the branch count of the first stable phase unfolding.

The second return is

\[
q_{EW}=2(|ABCD|+1)(2|V|+|ABCD|+1)=710,
\qquad
m_{EW}=(|ABCD|+1)d_{13}+|V_{13}|=113.
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

## 02.31 Φ as primitive positive-response capacity

The number `φ` is not a primitive axiom. The primitive object is the normalized finite positive-response detector skeleton. It has one direct branch of weight `p` and one first self-return branch. Since the first positive response is quadratic, the return branch has weight `p²`. The unit terminal closure is therefore

\[
p+p^2=1.
\]

The polynomial `p²+p−1` is strictly increasing on `(0,1)`, so the positive branch is unique:

\[
p=\varphi^{-1},
\qquad
p^2=\varphi^{-2}.
\]

The distinguishability half-gap is

\[
\delta_0=\frac{p-p^2}{2}=\frac{1}{2\varphi^3}.
\]

The alternatives are excluded by the operator obligations. The equation `p+p=1` is only a linear naming split and has no positive self-return. The equation `p+p^k=1` for `k>2` contains hidden intermediate memory before the first halt and is therefore not primitive. A non-integer exponent is not finite constructive channel composition on profinite stages. A free equation `p+q=1` introduces a second independent scale and violates single-section closure.

## 02.32 Hurwitz-rigid phase generator and non-resonant spatial unfolding

The normalized D0 phase generator is not an arbitrary irrational angle.  The
primitive positive-response theorem gives `p+p²=1`, hence the return branch is

```math
\alpha_{D0}=p^2=\varphi^{-2}.
```

The physical phase increment is therefore `2π/φ²`.  By the Hurwitz/continued-
fraction extremality of the `φ` class, this rotation is maximally resistant to
low-denominator rational locking.  In D0 terminology, it is the admissible phase
increment that suppresses uncontrolled metric arms in the unresolved complement.

This does not eliminate finite branches.  Branches appear only after a finite
readout quotient chooses a return modulus.  Thus the same chain has two layers:

```text
φ⁻² irrational rotation  → non-resonant archive smoothing;
finite return modulus q  > residue branch geometry.
```

This closes the compatibility between macroscopic smoothness and finite branch
unfolding.

## 02.33 Forced return windows and non-post-hoc phase unfolding

The phase-unfolding windows used by D0 are not chosen by searching for rational approximants to a circle.  They are forced by terminal capacity.

Let the direct/return dyad have cardinality `D2=2`.  Then the terminal role square has cardinality

```math
|ABCD|=D_2^2=4,
```

the oriented terminal set is

```math
|\Omega_8|=2|ABCD|=8,
```

and the pointed witness shell is

```math
V_9=|\Omega_8|+1=9.
```

The first dyadic extension and terminal-role extension are

```math
V_{11}=V_9+D_2=11,
\qquad
V_{13}=V_9+|ABCD|=13.
```

The first terminal phase-return modulus must saturate all unsiged terminal roles over the first moving dyadic shell.  Therefore

```math
q_T=\operatorname{lcm}(|ABCD|,V_{11})=4\cdot 11=44.
```

The turn count is fixed by terminal role closure plus the three incidence directions of the scene:

```math
m_T=|ABCD|+\operatorname{rank}(A_K)=4+3=7.
```

Thus `44/7` is checked as a phase near-return only after `44` and `7` have been capacity-derived.  Its admissible branch count is

```math
\varphi_{Euler}(44)=20=d_{13}.
```

The second return window is similarly forced after the terminal shell exists.  Define the pointed terminal alphabet

```math
B=|ABCD|+1=5
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


## 02.34 Master Evolution and φ-quasicrystal proof spine

D0-MASTER-EVOLUTION-001
Owners:
  T_squared_plus_T_minus_identity_eq_zero
  trace_T_pow_eq_signed_lucas
  lefschetz_spectrum_unfolds_scene
  det_T_pow_square_eq_one
  lucas_heat_moment_bridge

D0-QUASI-001
Owners:
  d0_vacuum_is_condensed_phi_quasicrystal_support
  visible_geometry_is_cut_project_shadow
  phi_phase_has_hurwitz_anti_resonance

D0-HULL-001
Owners:
  d0_hull_has_finite_local_complexity
  d0_hull_has_phi_cut_project_origin
  d0_hull_is_nonperiodic
  d0_hull_supports_gap_labeling

D0-KTHEORY-001
Owners:
  gap_label_is_topological_not_fitted
  d0_gap_labels_are_countable
  gap_labeling_requires_frozen_operator

D0-SOLENOID-001
Owners:
  d0_hull_admits_noncommutative_solenoid_model

D0-SOLENOID-GRAVITY-001
Owners:
  finite_spin2_operator_is_tt_sector_of_solenoid_spectral_geometry

## 02.35 Preserved theorem-spine history (formerly 02.101.*)

The 02.101.* rows are preserved theorem-spine history.
The active v15 proof spine is:
Master Evolution > QUASI > HULL/KTHEORY/SOLENOID.

This history records the development of the proof spine and contains the owners for the following components:

- **Born 2.0 / 2.0 Uniqueness**:
  - `Finite Born 2.0 uniqueness`
  - `D0.finite_effect_born_readout_unique`
  - `D0.finite_effect_born_no_hidden_response`
  - `D0.finite_tensor_born_readout_unique`
  - `D0.finite_power_readout_no_alternative`

- **Torus-Core13 Geometry**:
  - `Torus-Core13 Geometry Origin`
  - `D0.Geometry.TorusCore13GeometryOrigin`
  - `torus_geometry_forces_generation_selector_noncommute`
  - `D0.Matter.CKMNontrivialFlavourAlgebra`
  - `D0.Matter.MesonDefectTransferOrigin`
  - `D0.Core.BornQuadraticOrigin`

- **Toral Automorphism / Galois balance**:
  - `Toral automorphism / Galois balance`
  - `trace_evolution_unfolds_d0_geometry`
  - `toral_volume_conservation_square`
  - `dark_sector_even_window_readout_zero`

## 02.36 Theorem spine for formerly weak sectors

Selector uniqueness and concrete Book 04 instances: `chargedLeptonElectronTerminalClaim`,
`electroweakDepth35Claim`, `protonReadout306Claim`,
`neutronArchiveSiblingClaim`, `betaUnlockDepth19Claim`.

The active v15 proof spine replaces the historical development sections with a direct mapping of proof owners.

- **CKM Finite Basis / Selector**:
  - `CKM finite basis origin`
  - `D0.Matter.CKMBasisOrigin`
  - `ckm_origin_candidate_matrix_unique`
  - `ckm_no_free_matrix_at_fixed_basis_origin`
  - `ckm_no_free_matrix_at_fixed_bases`
  - `D0.Matter.StrictSelectorCertificate`
  - `D0.Matter.book04_selector_claim_no_free_alternative`

- **Charged-lepton Coefficient-origin**:
  - `02.36.3a Charged-lepton coefficient-origin closure`
  - `D0.Matter.ChargedLeptonCoefficientOrigin`
  - `charged_lepton_coefficient_table_forced`
  - `changed ratio row, exponent row or bridge-factor row is impossible`

- **Book 04 Operator-boundary**:
  - `02.36.3b Book 04 operator-boundary closure`
  - `D0.Matter.book04_operator_boundaries_closed`
  - `nucleon_line_cannot_promote_full_baryon_multiplet`
  - `lower_hodge_400_cannot_promote_meson_masses`
  - `missing_scalar_projector_cannot_promote_higgs_yukawa_core`

- **SM-facing Gauge Decomposition**:
  - `02.36.6 SM-facing gauge decomposition`
  - `D0.Gauge.SMGaugeDecomposition`
  - `no alternate factor/representation ledger`

- **Spin-2 Derivation / Carrier**:
  - `Spin-2 derivation and internal cone speed`
  - `D0.Geometry.FiniteWeakFieldQuotient`
  - `finite_weak_field_quotient_yields_tt_representative`
  - `finite_conserved_stress_spin2_coupling_closed`
  - `Poisson response plus a named TT mode is not enough`
  - `D0.Geometry.FiniteSpin2WaveOperator`
  - `PiTT4_idempotent`
  - `WTT4_preserves_tt`
  - `finite_spin2_tt_carrier_closed`
  - `D0.Geometry.finite_spin2_tt_carrier_closed`

- **Cosmology**:
  - `02.37 Cosmology reproducibility split`
  - `InternalArchiveCosmologyObject`
  - `SurveyLikelihoodPassport`
  - `survey likelihood cannot promote to core cosmology closure`

- **Tick-gauge / Lorentz**:
  - `02.38 Tick-gauge and Lorentz-compatible cone invariant`
  - `finite_causal_tick_section_cone_speed_eq_one`
  - `finite_lorentz_tick_gauge_no_euclidean_export`
  - `finite_lorentz_tick_rescaling_preserves_closure`

- **Full Support Selectors**:
  - `02.39 Book 04 full-support selector closure`
  - `D0.Matter.Book04FullSupportSelectors`

- **Higgs Projector / SMScalar**:
  - `commutes_XZ_forces_scalar_matrix`
  - `nonzero_gauge_idempotent_eq_identity`
  - `rank1_scalar_projector_breaks_su2_gauge_compatibility`
  - `rank2_scalar_projector_exists`
  - `minimal_positive_scalar_projector_rank_two`
  - `minimal_positive_scalar_projector_unique`
  - `higgs_yukawa_core_promotion_valid`

- **Baryon S3 / Decuplet**:
  - `D0-QUASI-002A`
  - `Phason Strain Generations / Baryon S3`
  - `phason_strain_generations_baryon_closure`

- **Quasicrystal Operator Origin**:
  - `D0-QUASI-002`
  - `quasi_generation_inflation_orbit`
  - `archive_phason_strain_em_dark_metric_visible`
  - `fractional_charge_window_weights`

- **Gravity / Einstein Interface**:
  - `Entropic archive gravity interface`
  - `Finite spin-2 wave operator`
  - `Higher-curvature finite cut`
  - `Spectral A2 / EH bridge`
  - `Macro Einstein interface`


## 02.v15 Master bootstrap and discrete volume derivative

Definition. The finite active volume is the trace-rank of the retained projector:
\[
V_N := \operatorname{rank}(P_N)=\operatorname{Tr}(P_N).
\]
For an admissible one-channel extension of the retained sector, the discrete volume derivative is the forward finite difference
\[
\partial_V A_N := A_{N+1}-A_N.
\]
This is the finite differential structure used by CVFT before any continuum interpolation.

The v15 master bootstrap functional is
\[
\delta\left[
\beta^{-1}\log\operatorname{Tr}(e^{-\beta\Delta_N(V)})
-
\log\det(I-zP_NU_N^\dagger Q_NU_NP_N)
\right]=0.
\]
The heat-trace term supplies the finite spectral geometry. The feedback determinant supplies return-cycle thermodynamics, pole stabilization, pressure, and leakage.

## 02.v15 Self-substrate trace identity and fractal tick

For \(\psi\in P_N\mathcal H_N\), unitarity and orthogonality give

\[
\|\psi\|^2=\|P_NU_NP_N\psi\|^2+\|Q_NU_NP_N\psi\|^2.
\]

The feedback-return operator satisfies

\[
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N),
\qquad
\langle\psi,F_N\psi\rangle=\|Q_NU_NP_N\psi\|^2.
\]

### D0-IM-001 Fractal Tick Fixed Point

Let \(p=\varphi^{-1}\). On a declared detector-clock subspace \(\Pi_\tau\),

\[
\Pi_\tau F_N\Pi_\tau=p^2\Pi_\tau,
\qquad
\Pi_\tau U_{\rm eff}^\dagger U_{\rm eff}\Pi_\tau=p\Pi_\tau.
\]

This is a fixed-point sector law, not a global identity for arbitrary \(U_N\).

### D0-IM-002 Continuum from Fractal Tick

The constant logarithmic gradient

\[
\Delta\log A=-\log\varphi
\]

generates the continuous envelope

\[
\frac{dA}{ds}=-(\log\varphi)A,
\qquad
\frac{dB}{ds}=(\log\varphi)A.
\]

Thus continuum time is the semigroup envelope of infinite self-similar trace production.

**Semigroup Uniqueness Theorem (Researcher A correction).**
The functional equation for the envelope must satisfy the corrected multiplicative form for uniqueness under the retained-archive split:

\[
A(s+t) = \frac{A(s) A(t)}{A_0}.
\]

(The naive additive form is insufficient; the division by \(A_0\) normalizes the initial substrate so that the exponential solution is the unique continuous semigroup compatible with the fractal ratio \(q = \varphi^{-1}\).)

### D0-FOUND-004 Quadratic Peel Theorem

Phase-blind finite readout is quadratic because archive trace is a norm-square boundary peel, not a linear amplitude cut:

\[
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N).
\]
