<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 03 — Finite Action Operators and Scene Dynamics

> **[Standard Physics Isomorphism].** D0's coined terms in this book read, in mainstream physics, as:
>
> - archive → integrated-out environment / environment bath (open-system trace-out)
> - forgetting map / coarse-graining → Wilsonian coarse-graining / CPTP decoherence channel
> - archive pressure → trace anomaly / entropic backreaction
> - terminal (destructive) readout → projective (von Neumann) / POVM measurement
> - golden tick / toral time → discrete Floquet operator / modular (Tomita–Takesaki) flow
> - carrier → representation (state) space
> - readout → measurement outcome (POVM effect)
>
> Genuinely-D0 (kept, defined in-text against the standard notion): the scene `K(9,11,13)`, the M1 admissibility axiom (no obligatory external catalogue), `δ₀`, `φ`, and *forcing* (= reductio ad absurdum against M1). Full crosswalk: the language-normalization Rosetta (`00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md`).


> Scope: Finite action/variation language, scene dynamics, and admissible finite equations of motion.
> Claim discipline: This book supplies operator dynamics, not standalone empirical claims.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 03.0 Active action/variation layer

Book 03 supplies the finite action and variation language for the feedback operator. It does not make empirical claims.

```text
S_fb = -log det(I - z F_N)
```

For an admissible finite variation `delta F_N`:

```text
delta S_fb
= Tr[(I - z F_N)^(-1) z delta F_N]
```

The universal feedback source is:

```text
Pi_fb = z(I - z F_N)^(-1)
```

Book 03 supplies the response source used by matter, gravity and cosmology sector reductions. Physical meaning is assigned only after sector projection and bridge/passport boundary.

## 03.1 Standard reading of action and finite incidence/clique complex terminology

The D0 `finite incidence/clique complex` is a finite incidence/clique complex with cochains and boundary/coboundary operators. The D0 `finite variational operator stack` is a finite variational functional on this complex. A `tick` is a discrete evolution endomorphism, and a `single dimensional calibration section` is a single scale-section fixing dimensionalization without introducing a second mass anchor.

The standard-language names above are the downstream reading. What they package is a finite spectral triple over the scene; the *why* behind them is given in the three forced readings below. The scene `K(9,11,13)` itself (rank 3 / nullity 30, the ABCD→Ω8 role alphabet) is owned by BOOK_01 §01.8 and is cited here, not re-derived.

### 03.1.1 The finite spectral triple `X_D0 = (A, H, D)` (DEF 15.2.1)

The action operators of this book are not free instruments laid over an a-priori metric space; they are the data of a **finite spectral triple** `X_D0 = (A, H, D)` carried by the scene [^b03-2]:

1. **Algebra `A`** — the finite **path \*-algebra** of the scene `K(9,11,13)` over `Q(φ)`, with the involution `(·)*` induced by **path reversal**. `A` is *non*commutative, and that noncommutativity is not optional decoration: it is what records order memory (holonomy) along a path. Interaction in D0 is therefore an effect of scene topology — the failure of two path-words to commute — not an exogenous force catalog laid on top of it.
2. **Hilbert space `H`** — finite-dimensional, `H = ℓ²(V)` (equivalently any faithful representation of `A` on a finite module), forced finite because `|V| < ∞`. No completion-to-infinity step is admitted in CORE.
3. **Operator `D`** — the discrete **distinguishability operator** (Dirac-type) on the scene. Its *spectrum*, not a postulated ruler, fixes the geometry.

The metric is then *derived from the spectrum of `D`*, not assumed. Distance on the scene is the **Connes distance** [^b03-3]:

```math
d(x,y) = \sup\{\, |a(x) - a(y)| : a \in \mathcal{A},\ \lVert [\mathcal{D}, a] \rVert \le 1 \,\}.
```

This is the load-bearing inversion: the noncommutative-solenoid *gravity* approximation (BOOK_07) is downstream and approximate, whereas the **finite scene triple** — `A` = path \*-algebra over `Q(φ)` with reversal involution, metric forced out of `spec(D)` by the Connes formula — is the primitive. Status: CORE-FORCING [^b03-4]. The Clifford/Dirac operator bridge that lets this finite triple be read against the relativistic operator stack is carried by the finite certificate.

### 03.1.2 Spectral-action reading of mass and `α`; the zeta-residue route (THE 15.4.2)

Once `D` is the carrier, the Laplacian is `Δ_G = D²` (default the normalized `L_sym` of the scene; a combinatorial Laplacian is flagged explicitly when used — either choice is fixed by the graph and adds no exogenous dimensionless parameter). Its spectrum sets the mass levels. The associated **spectral zeta-function** is [^b03-5]:

```math
\zeta_\mathcal{D}(s) = \operatorname{Tr}\!\big(|\mathcal{D}|^{-s}\big) = \sum_n \lambda_n^{-s/2}.
```

The forcing here: the interaction coupling is **not** an input, it is read off the spectral action. The route is **THE 15.4.2** — `α⁻¹` is fixed by the **residue of `ζ_D` at the dimension pole**, i.e. `ζ_D(0)` at that pole [^b03-6]. This residue route is what connects the coupling to the **topological capacity 359** (BOOK_03 III.1 / D0 §9) and to the `Δ_α` **seam** that canonicalizes the numerical value of `α` (BOOK_03 III.2 / D0 §16.3). The *outputs* of this — the A0 (volume) / A2 (EH-proxy) spectral-action ladder (BOOK_08 §08.32–08.34) and the `α_top⁻¹ = 359/φ² − φ⁻⁵` number (BOOK_02 §834) — rest on the *mechanism* that derives the coupling from `Res ζ_D`. That mechanism is the "why this `α`."

The A0/A2 ladder stability that the residue route rides on is already certified by the finite certificate. The spectral zeta `ζ_D` is now **defined** on the scene (it was previously absent), and its finite spectral moments are closed by certificate and Lean: the edge-operator zeta yields `ζ_E(0) = 359 = |E|` (the topological capacity, at `s=0`) and `ζ_E(−1) = 359·φ⁻² − φ⁻⁵ = α_top⁻¹` (the fine-structure value as the `s=−1` moment — i.e. the edge trace), with the seam `φ⁻⁵ = ξ₅` proved separately. The **full** residue-at-the-dimension-pole derivation remains a **theorem target**: the scene is finite, so `ζ_D` is an entire finite sum with no dimension pole — `α` is recovered as a spectral *moment*, not a residue, and the genuine residue route would need the profinite/archive limit. Accordingly `α` is a **structural form** good to ~`3.7·10⁻⁴` (not a precision prediction), and the residual seam `Δ_α` — distinct from `φ⁻⁵` — still lacks an analytic second-order owner. [^b03-1] for the `ζ_D`-residue → `α⁻¹` step [^b03-7]; the spectral-action ladder it sits on is CORE.

### 03.1.3 Why the wavefunction is an algebraic sum of path memory-classes (THE 4.1.2)

The triple also fixes *why* the state is what it is. A path `γ` on the scene contributes **not a number but a memory-class** — its **holonomy** in the path algebra [^b03-8]:

```math
\mathrm{Hol}(\gamma) := q(\gamma) \in \mathcal{Q} \subset \mathcal{A}.
```

The state at `x` is then the **algebraic sum of these memory-classes**, an element of the path algebra, not a pre-supposed complex amplitude [^b03-9]:

```math
\Psi(x) := \sum_{\gamma:\,0 \to x} \mathrm{Hol}(\gamma) \in \mathbb{Q}(\varphi)[\mathcal{Q}] \subset \mathcal{A}.
```

**The forcing — amplitudes add, not probabilities.** Suppose one summed `P(γ)` (probabilities) instead of `Hol(γ)` (memory-classes). Then the information distinguishing the paths — their relative order/phase — is destroyed: distinct histories that the scene *can* tell apart collapse to one number. That is loss of part of the history, which the completeness axiom forbids (no distinction the scene supports may be discarded). Therefore the sum must be over the algebraic memory-classes, and the classes interfere wherever the scene has cycles (`D ≥ 6`); constructive interference is the classical/geodesic trajectory. Status: CORE-FORCING [^b03-10].

**Complex phase is packaging, not a primitive.** In CORE `Ψ(x)` is an algebraic sum in `A` and assumes no prior complex structure. To match quantum dynamics one needs a unitary representation of order memory; the *minimal* choice introducing no new parameter is the one-dimensional unitary representation `ρ : Q → U(1)`, `ρ(q(γ)) = e^{iθ(γ)}`. Complex numbers (modulus + phase) thus enter only as the minimal **U(1) BRIDGE-packaging** that secures unitarity and interference — not as a new CORE entity [^b03-11]. This is the "why QM" forcing. The CKM phason holonomy (BOOK_04 §04.4.4) is a distinct downstream construct, not this path-algebra memory sum. The Born step that turns `|Ψ|` into a probability is the separate quadratic-origin result, verified by the finite certificate, kept off this CORE line.
## 03.2 Role and boundary of this book

Book 03 contains the finite action mechanism. It does not re-prove the condensed/profinite detector object, and it does not complete the particle, gravity or cosmology comparison protocols. Those are adjacent books.

The boundary rule is:

```math
S_{D0}^\varphi\ \text{and the response theorem} \in Books 01--02,
\qquad
S_{finite variational test functional},J_{finite incidence/clique complex},\Lambda_{act},S_\partial\in\text{Book 03},
```

```math
\text{particle/coefficient comparison protocols}\in\text{Book 04},
\qquad
\text{gravity and cosmology transfers}\in\text{Books 07--08}.
```

Thus this book is a bridge from invariant finite registration to finite dynamics.

## 03.3 Action as a finite admissible operator stack

Once a finite incidence/clique complex has been constructed, D0 does not introduce a continuum Lagrangian and then regulate it. The action is a finite admissible stack of operators, projectors, spectra, boundary terms and quadratic responses:

```math
\mathcal S_{stack}=J_{finite incidence/clique complex}+S_{coeff}+S_\Lambda+S_\partial+S_{heat}+S_{terminal}.
```

The order is not cosmetic. Scene selection comes first; finite variational test functional coefficients follow; the full-cycle action section fixes the single dimensional dictionary; the boundary block fixes the non-diagonal curvature residual; heat depth controls the length map; terminal terms record the final charged or leaking shell.

The admissibility condition is:

```math
\text{new sector scale}=\varnothing
\quad\text{after}\quad
\Lambda_{act}\ \text{has been chosen}.
```

A sector formula that requires a new GeV, metre, second, Planck, nucleon, collider, or dark-sector anchor is not an action theorem.

### 03.3.0 Why an action exists at all: the statistical sum over histories

D0 does not postulate a Lagrangian `\mathcal L` and integrate `e^{i\int\mathcal L}`. It asks the prior question — *how do you score the statistics of all admissible histories at finite resolution without an external choice rule?* — and the action falls out as the answer. The carrier is the CORE statistical sum over histories [^b03-13]:

```math
Z_D(k):=\sum_{\gamma\in\Gamma_D(k)} w(\gamma)\,[q(\gamma)],
```

with `\Gamma_D(k)` the admissible histories at refinement level `k`, `w(\gamma)` the history weight, and `[q(\gamma)]` the memory class (topological charge/phase) in the role algebra `\mathcal A`.

**The weight is forced to be `w=\varphi^{-S}` — exponential, base `\varphi`** [^b03-14]. The form is not a postulate; three constraints close it with no freedom:

1. **Multiplicativity.** The probability of a composite history `A\to B\to C` of independent steps must factor: `w(A\to C)=w(A\to B)\,w(B\to C)`.
2. **Additivity of cost.** Code length of a composite history adds: `S_{total}=S_1+S_2`.
3. **Unique sum-to-product map.** The only function carrying a sum to a product is the exponential, `w(S)=b^{-S}`. A non-exponential weight would need an external table reconciling addition with multiplication — an exogenous catalog, ⊥M1 (DEF-0.2.2).
4. **Unique base.** The only scale number available in CORE is `\varphi` (the `p+p^2=1` fixed point, owned by BOOK_01 §01.6), so `b=\varphi`.

Hence `w(\gamma)=\varphi^{-S(\gamma)}`. The BRIDGE packaging `\varphi^{-S}=e^{-S\ln\varphi}` recovers the Boltzmann/Gibbs form, and the analytic continuation `S\to iS` recovers the quantum amplitude. Status: CORE-FORCING [^b03-15].

**Locality is a theorem, not an assumption** [^b03-16]. If a scene splits into two parts with no path between them, then `Z_{total}=Z_1\cdot Z_2`. This cluster decomposition is guaranteed by the structure of the algebra `\mathcal A` and is exactly the statement that "physics here" does not depend on "physics in another galaxy". Status: CORE-FORCING [^b03-17].

### 03.3.0a Action is assembly cost, not an imported functional

With the weight fixed, the action `S(\gamma)` of a history is forced to be its net assembly cost — resolution friction minus distinguishability gain [^b03-18]:

```math
S(\gamma):=\sum_{e\in\gamma}\operatorname{Cost}(e)\;-\;\sum_{v\in\gamma}\operatorname{Info}(v).
```

The edge sum `\sum_e\operatorname{Cost}(e)` is the resolution (UV-cutoff `\kappa`) price of traversing edges — the "friction" of the medium. The vertex sum `\sum_v\operatorname{Info}(v)` is the distinguishability gain: at each branch the history commits a choice (a bit), lowering uncertainty entropy. There is no place to insert an imported continuum Lagrangian density: the action is read off the graph history.

**No coupling constant may be multiplied in front** [^b03-19]. Standard QFT writes `\tfrac{1}{g^2}\int\dots`. In CORE this prefactor is forbidden: any `\lambda\notin\{1,\varphi^n\}` is an external Catalog of interaction strength, ⊥M1. Interaction strength must be *derived* from graph topology — as `\alpha^{-1}` is derived from the 359-channel scene count downstream — never inserted as a multiplier into the action. Status: CORE-FORCING [^b03-20].

**Least action `\delta S=0` is the Minimum Description Length tautology** [^b03-21]. Because the most probable history is the cheapest to encode in `\Sigma`, stationarity of `S` is not an additional physical postulate layered on the weight `\varphi^{-S}`; it is the same statement read at the classical limit. "Most probable" = "shortest code" = `\delta S=0` (MDL). Status: CORE-FORCING [^b03-22].

**A Feynman diagram is an equivalence class of histories, not a drawn line** [^b03-23]. A diagram is `[\gamma]_\sim` — the class of all histories sharing one topology (loop count, branch vertices, external legs). A loop is literally a closed memory cycle `P` (the light-cycle of the spectrum book); loops therefore *create* mass and charge here rather than merely correcting them, and the standard QFT divergences are the artifact of treating finite-size cycles as points (structural limit `\kappa_k`). Status: CORE-FORCING [^b03-24].

### 03.3.0b The smooth limit: how the variational/Lagrangian language is recovered

The `t,v,\nabla` language and the variational calculus are a BRIDGE packaging of the smooth limit — the CORE content is: *classical motion is the dominance of the minimal-code history under coarse-graining* [^b03-25]. Newton's laws are then a theorem of the Information Economy Principle, not an input.

**Information Economy Principle** [^b03-26]. Tracking a macro-object is continuous prediction of its position. The description cost `J` of a trajectory splits into:

- **Potential `V` (cost of position).** The price of sitting at an "expensive" graph location — where cycle density `\varrho` is high. High cycle density is exactly what gravity is in D0; so `\operatorname{Cost}_{pos}=V(x)`.
- **Kinetic `T` (prediction savings of inertia).** If the object coasts on its velocity vector, the predictor "it is where the vector says" guesses with zero error; the faster the coast, the more strongly the predictor compresses the data. In the smooth limit this packages as `T(v,m)`, written `T=\tfrac12 mv^2` after a unit/normalization choice (BRIDGE).

**Lagrangian as balance, least action from path probability** [^b03-27]. The code length of a history is the balance

```math
L_{code}=\operatorname{Cost}_{pos}-\operatorname{Benefit}_{pred}=V-T,
```

equal up to sign convention to the physicists' `L=T-V`. Inheriting the weight of §03.3.0, the path realization probability is `P\sim\varphi^{-L_{code}}`. In the classical limit only the minimal-code path survives, so

```math
\delta\!\int (T-V)\,dt=0,
```

which is the Principle of Least Action — derived, not assumed. The packaged stationarity gives `\tfrac{d}{dt}(mv)=-\nabla V`, i.e. `F=ma`: force is the gradient of informational complexity, and a body "rolls" to where computing its existence is cheapest. Status: CORE-FORCING [^b03-28]. This is the smooth-limit twin of the finite stationarity condition stated in §03.8; the finite stationarity `\nabla_{x\in\mathcal X_N}\mathcal S_{stack}=0` is the primitive, and `\delta\int(T-V)dt=0` is its coarse-grained image.

### 03.3.0c Renormalization is forbidden except for the `\kappa`-residual

D0 keeps the counterterm ban absolutely: in CORE, renormalization is *not* a free choice of scheme plus added counterterms. Any hand-chosen counterterm is an exogenous correction parameter, ⊥M1 [^b03-29]. The *only* admissible "renormalization" is the `\kappa`-residual `r_k` that arises from finite level resolution and is controlled by the `\kappa`-bound: it is not selected by hand and it vanishes on refinement (`r_k\to 0` as `k\to\infty`; see BOOK_05 `\kappa`-stabilization). Running couplings are then an artifact of information compression under the forgetting projection `\pi_{k+1\to k}`, and the RG equation is the conservation-of-information law across scale — adding no new fields or thresholds. Status: CORE-FORCING [^b03-30].

### 03.3.1 Operator non-commutativity is the structural time arrow

The assembly operators of §03.3 do not freely permute, and that is forced. With `J` the puncture/localize operator (distributed core/memory mode `\odot 9` → local observed-event mode `5`) and `Y` the closure/shell-glue operator (compactify the outer scene zone `13` into effective `4D+64` boundary conditions), their commutator is non-zero:

```math
[J,Y]=J\circ Y-Y\circ J\neq 0.
```

**This is a necessary consequence of M1** [^b03-31]. If assembly order were irrelevant — if `J` and `Y` commuted — then "what to fix, and when" would have to be supplied by an external ordering catalog (rules of assembly priority), which is ⊥M1 (DEF-0.2.2). Order-independence demands the very catalog M1 forbids, so order must matter; `[J,Y]\neq 0` is the structural arrow of time, not a metaphysical add-on. Status: CORE-FORCING [^b03-32].

This is a distinct forcing from BOOK_01's torus-shell non-commutativity (torus radius vs phase drift) and BOOK_04's generation-selector non-commutativity: those concern a different operator pair. The `[J,Y]\neq 0` arrow is owned here, at the assembly-operator level.

**Constructive witness (no metaphysics).** The non-commutativity has an explicit, finite witness on the history space `H` of pairs `(\Gamma,\approx)`, where `\Gamma` is the set of paths/events and `\approx` is the indistinguishability (equivalence) relation after canonization `Can` [^b03-33]:

- `Y` acts as the **shell**: first it changes the equivalence relation (`\approx\to\approx_Y`), gluing events that were distinguishable only by the outer scene part (zone `13`), then it applies `Can` on the new relation.
- `J` acts as the **puncture**: first it generates a localization (inserts/marks a defect, zone `9`) in `\Gamma`, then it applies `Can` under the *old* relation.

Because `Can` depends on the equivalence-class structure, changing `\approx` before `Can` changes the localization result in `\Gamma` after `Can`. So `Y\circ J` ("event then packaging" → reproducible memory) is distinguishable from `J\circ Y` ("packaging/description then attempted localization" → noise with no access to history) without introducing any external priority rule. This is `[J,Y]\neq 0` realized as a concrete order-dependence of `Can`, not an assertion. [^b03-12]

### 03.3.2 The closed feedback action component

The closed feedback action component is `S_fb = -log det(I - z F_N)`, where `F_N=P_N U_N^dagger Q_N U_N P_N` is feedback-return, not positive response. The source is

```math
\Pi_{fb}=z(I-zF_N)^{-1},\qquad dS_{fb}=\operatorname{Tr}(\Pi_{fb}\,dF_N).
```

The log/Neumann expansion is allowed only under `|z|\rho(F_N)<1`; the resolvent itself only requires `z^{-1}` outside the spectrum. Its variation is represented by the finite feedback source owner; pressure and finite PVT are owned by the finite feedback equation of state, each verified by the finite certificate. The ideal-gas postulate is a no-go core shortcut, not the D0 pressure law. This feedback action is the finite, resolvent-form instance of the same `-\log`-of-an-operator-determinant structure that the statistical sum `Z_D` of §03.3.0 produces under `w=\varphi^{-S}`: the partition function over histories and the feedback determinant are the same admissible object read at two scene scales.
## 03.4 Scene/finite variational test functional backbone

The finite incidence/clique complex is not background spacetime. It is the finite register on which action can be evaluated. The active action spine is:

```math
K(9,11,13)
\to
S_{finite variational test functional},J_{finite incidence/clique complex}
\to
\mathcal G_{spec}
\to
\Lambda_{act}
\to
\text{quadratic readout}.
```

The finite incidence/clique complex action is the finite selector of persistent records, unlocks, decays, bridges and readouts. It is therefore closer to a variational detector functional than to a continuum field postulate.

The finite variational test functional stack is allowed to use finite matrices, graph degrees, projectors, Hessians, spectra, finite differences and positive quadratic penalties. It is not allowed to use a sector target table as an input.

## 03.5 Internal action gauge

Let the length-depth map selected by finite incidence/clique complex, heat and terminal terms be

```math
D_L=\Omega_8\varphi^{V_9V_{11}}\left(1+\frac{\delta_0}{V_{13}}\right).
```

The normalized internal cell density is

```math
\rho_{cell}^{D0}=D_L^{-2}.
```

The internal gauge block is

```math
S_{gauge}^{D0}(\lambda,\rho)=
(\lambda-1)^2+(\rho-D_L^{-2})^2+
(\lambda^2\rho-D_L^{-2})^2.
```

Its positive stationary solution is

```math
\lambda_*=1,
\qquad
\rho_*=D_L^{-2}.
```

This is an internal action class and density class. It is not a kilogram, joule or electronvolt.

## 03.6 Single full-cycle action section

The physical SI section is chosen once, through the minimal charged terminal full-cycle:

```math
S_\Lambda(\tau,\Lambda)=
(\Lambda\tau/h-1)^2+
\left(38\tau/(h/(m_ec^2))-1\right)^2.
```

The Euler point is

```math
\tau_0=\frac{h}{38m_ec^2},
\qquad
\ell_0=c\tau_0=\frac{h}{38m_ec},
\qquad
\Lambda_{act}=\frac{h}{\tau_0}=38m_ec^2.
```

D0 does not fail to derive kilograms or joules. Kilogram, joule, metre and second are external unit sections, not invariants. D0 derives the invariant finite action-section structure. The electron terminal record prints this structure into the SI convention. Once this section is chosen, every later mass or rate readout must use the same section.

The mass map is therefore

```math
M_a^2=(\Lambda_{act}^{SI})^2\lambda_a.
```

The single dimensional calibration section rank rule is:

```text
mass, Q_beta, rate        : Lambda_act^(+1)
time, length, ellP        : Lambda_act^(-1)
G_N, cross-section area   : Lambda_act^(-2)
Born/entropy probabilities: Lambda_act^(0)
```

## 03.6a Gap labels do not create action sections

K-theory / K0 Gap Labeling records spectral gap ownership for frozen operators on the tiling hull. It does not introduce a second action section, a tunable scalar parameter, or a new mass anchor.

The allowed order is:

```text
single action section
-> frozen operator
-> spectral gap
-> K0 gap label
-> sector readout/passport
```

The forbidden shortcut is:

```text
gap label -> new action scale.
```

## 03.7 Boundary curvature and interaction-information cell

The scalar boundary residual is fixed by a non-diagonal boundary block, not by a free correction series. Define

```math
r=\frac{c_\partial^2}{\delta_0^6},
\qquad
r_0=\frac{13}{8}\frac{1+\delta_0^3/38}{1+\delta_0/9},
\qquad
d_9=\deg(V_9)=24.
```

The finite boundary action is

```math
S_\partial(r,I)=
\left(r-r_0\left(1+{I}\over d_9}\right)\right)^2+
\left(I-\Delta_\lambda^2\delta_0^3\right)^2.
```

Its stationary solution is

```math
I_*=\Delta_\lambda^2\delta_0^3,
\qquad
r_*=r_0\left(1+\frac{\Delta_\lambda^2\delta_0^3}{d_9}\right),
\qquad
c_\partial^2=\delta_0^6r_*.
```

The interaction-information cell used later is

```math
I_B=\frac{\Delta_\lambda^2\delta_0^3}{24}.
```

Book 04 may use this cell in hadron or coefficient comparison protocols, but Book 03 owns the variational reason that the cell is non-diagonal and finite.

## 03.8 Finite equations of motion

The D0 equation of motion is not a continuum Euler-Lagrange equation at fundamental level. It is a finite stationarity condition on the finite incidence/clique complex variables:

```math
\nabla_{x\in\mathcal X_N}\left(J_{finite incidence/clique complex}+S_{finite variational test functional}+S_\Lambda+S_\partial+S_{heat}+S_{terminal}\right)=0.
```

After the halt quotient and forgetting map, continuum equations may appear as limits or bridge dictionaries. They are not the primitive input.

The generic action-to-readout form is:

```math
\text{finite operator}\ Q
\quad\mapsto\quad
Q^\dagger Q
\quad\mapsto\quad
{\operatorname{Tr}(\Pi_aQ^\dagger Q)}\over{\operatorname{Tr}(Q^\dagger Q)}.
```

The proof of the trace law is in Book 02; Book 03 uses it as the admissible dynamics-to-readout finite variational test functional.

## 03.9 Runtime, forgetting and witness transport

The runtime stack consists of finite tick/witness transport followed by active/archive forgetting. The action consequence is that a record may persist, unlock or decay only through an operator that has a quadratic readout and a finite quotient.

The normalized witness transport is schematically

```math
\text{tick}\rightarrow\text{witness transport}\rightarrow\text{active/archive split}\rightarrow\text{quadratic readout}.
```

Finite-window entropy and dynamic witness transport are proof-referenced to Book 02. Book 03 uses them to control when an action block is a real runtime mechanism and when it is only a formal expression.

## 03.10 Vertex registry and finite scattering discipline

The vertex registry belongs here as action infrastructure. The finite S-matrix is not a complete collider simulator, but a registry of admissible transition operators:

```math
\mathcal S_{finite}: \mathcal H_{in}\to\mathcal H_{out},
\qquad
P(i\to f)=|\langle f|\mathcal S_{finite}|i\rangle|^2
```

provided the states are finite detector states and the bridge to external kinematics is typed. Collider and scattering comparison protocols are handed to Book 04.

### Why the registry is finite, and why amplitudes (not probabilities) populate it

The discipline above is not a stylistic choice — every clause is forced. A vertex registry is *admissible at all* only because the deep-QM forcing chain [^b03-34] closes each escape route to an external catalog. We integrate that chain here in place, because §03.10 is where the transition operator and its vertices live; the downstream FACTS (positive Born response `R = D^\dagger D`, the feedback partition object, readout → ordered update) are stated elsewhere, and their *why* is supplied here.

**(a) Finite alphabet ⇒ finite vertex set — the Fundamental Finiteness Theorem.** Fix a level `k` with resolution cutoff `\(\kappa_k := \varphi^k\)` (forcing: GOLDEN DEF II.3.APPX4.1.1; the single scale `\(\varphi\)` is owned by BOOK_01, no external scale is admitted). A test `T` is a distinguishing procedure with a finite code; only tests of cost `\(\mathrm{Cost}(T)=|D_{\min}(T)|\le\lfloor\kappa_k\rfloor\)` are admissible at level `k`. Then the set `\(V_k\)` of distinguishable states is finite:

```math
\kappa_k<\infty,\;\;|C|<\infty\;\Longrightarrow\;\#\{\text{codes of length}\le\kappa_k\}<\infty\;\Longrightarrow\;\#\{\text{outcome profiles}\}<\infty\;\Longrightarrow\;|V_k|<\infty.
```

Status: FORCED [^b03-35]. Consequence for this section: the vertex registry `\(\mathcal S_{finite}\)` is a *finite* table at every level. There are no continuum vertices in CORE. QFT-style divergences are not physical — they are the artifact of an unphysical limit `\(k\to\infty\)` taken without carrying the level structure of `\(V_k\)`. This is exactly the "finite detector states" hypothesis above, now derived rather than assumed.

**(b) Minimal refinement arity = 2 — vertices are binary with `\(\varphi^{-1}/\varphi^{-2}\)` weights.** A vertex is the elementary act by which a node `\(v\in V_k\)` splits into `\(m\)` children in `\(V_{k+1}\)`. The arity is forced to `m = 2` by M1:
- `m = 1`: no new distinction — the refinement is vacuous, not a vertex at all.
- `m > 2`: the split needs branch weights `\(p_1,\dots,p_m\)`. From the scalar `\(\varphi\)` alone no symmetry group fixing `m>2` equiprobable branches is derivable; any hand-chosen weights are an *external catalog of branch weights* — banned.
- `m = 2`: the only survivor. The two weights are fixed by the canonical partition of unity `\(\varphi^{-1}+\varphi^{-2}=1\)` (owned by BOOK_01 §01.6), giving the asymmetric vertex weights `\(S_\pm=(\varphi^{-1},\varphi^{-2})\)`.

Status: FORCED [^b03-36]. So every admissible transition operator factors through binary, `\(\varphi\)`-weighted vertices: the registry alphabet is fixed, not free.

**(c) Why amplitudes, not probabilities — order-memory forbids scalar summation.** Distinct paths `\(\gamma_1,\gamma_2\)` between the same endpoints carry distinct holonomies `\(\mathrm{Hol}(\gamma_1)\neq\mathrm{Hol}(\gamma_2)\)` (order memory, owned by BOOK_01's `\(F_N\)`/`\(\Sigma\)` history structure). If the registry summed scalar probabilities, `\(P(u\to v)=\sum_i P(\gamma_i)\)`, it would erase `\(\mathrm{Hol}\)` — and an erased order-memory leaves `\(\Sigma\)` incomplete, contradicting its definition. The only summation that preserves order is over (weight, holonomy) pairs, i.e. over **vectors**:

```math
D_k(u\to v):=\sum_{\gamma\in\mathrm{Path}_k(u\to v)} W(\gamma)\,[\mathrm{Hol}(\gamma)],\qquad W(\gamma)=\prod_i\varphi^{-a_i}.
```

The sum is finite (path length bounded by `\(\kappa_k\)`, by (a)). Status: FORCED [^b03-37]. This is why the registry stores transition *amplitudes* `\(\langle f|\mathcal S_{finite}|i\rangle\)` and squares only at the readout step — the "wave function" is a registry of alternative histories tagged by their topological holonomy class, nothing more.

**(d) Readout = parameter-free Bayesian conditioning — the only catalog-free collapse.** When outcome `i` lands the state in `\(A_i\subset V_k\)`, the operational measure `\(\sigma_k\)` updates by the unique parameter-free operation:

```math
\sigma_{new}(v)=\frac{\sigma_{old}(v)\,\mathbf 1[v\in A_i]}{\sum_{u\in A_i}\sigma_{old}(u)}.
```

Any *dynamical* collapse (GRW-style wave-packet contraction) imports a free "compression rate"/"compression shape" constant — an external catalog — and is therefore banned. Status: FORCED [^b03-38]. For the registry this fixes the post-scattering update: the readout `→` ordered-update step (the FACT recorded downstream) is *forced* to be conditioning, not a tunable channel.

**(e) Born = Gleason — the unique phase-invariant additive translation vectors → probabilities.** To read a probability off the amplitude vector `\(\Psi\)`, map holonomies to the `\(U(1)\)` representation `\([\mathrm{Hol}]\mapsto e^{i\theta}\)`. Physics may not depend on the global phase offset, so the translation `\(f:\Psi\mapsto\mathbb R_{\ge0}\)` must be (i) additive on orthogonal events and (ii) phase-blind `\(f(e^{i\alpha}\Psi)=f(\Psi)\)`. The unique such form is the quadratic `\(\langle\Psi|\Psi\rangle\)` — Gleason, adapted. Status: FORCED. The finite certificate verifies this: quarter-turn probes force the quadratic form `(a,b,c)=(1,0,1)`, with phase-blindness and the parallelogram law verified on a rational grid [^b03-39]. This is the derivation of the `\(|\cdot|^2\)` in `\(P(i\to f)=|\langle f|\mathcal S_{finite}|i\rangle|^2\)` above: the square is not postulated, it is the only honest vectors→probabilities translation. (The positive Born response `\(R=D^\dagger D\)` and the entropy/`\(\Lambda_{act}^0\)` probability weighting are stated in §03.6 — owner — and not re-derived here.)

**(f) Geometry sum is background-independent — vertices live on a dynamical graph, not a fixed lattice.** The graph `\(G_k\)` carrying the registry cannot be fixed in advance: a fixed adjacency table is a huge arbitrary *external catalog of edges* (banned by M1), so the graph must itself be a refinement variable. The catalog-free statistics over geometries is the QG partition object

```math
\mathcal Z_k:=\sum_{(G,J)}\varphi^{-A(G,J)},
```

with `\(A(G,J)\)` the assembly cost (minimal code length of the geometry). Status: FORCED [^b03-40]. Caveat for cross-references: this `\(\mathcal Z_k\)` is the *diagram/geometry* sum — it is **not** the same object as the feedback partition `\(Z_N=\mathrm{Tr}\,e^{-\beta\Delta}\det(I-zF)^{-1}\)` used elsewhere in the action machinery; do not conflate them.

**Net.** Clauses (a)–(f) discharge, one by one, every external-catalog escape a scattering registry could smuggle in: finiteness of the vertex table (a), fixed binary `\(\varphi\)`-weighted vertex alphabet (b), amplitude-valued (not probability-valued) entries (c), forced conditioning readout (d), the forced `\(|\cdot|^2\)` translation (e), and a dynamical-graph carrier (f). The "finite S-matrix registry" stated at the top is therefore the *only* M1-admissible transition object; the collider/kinematic comparison that consumes it is handed to Book 04.
## 03.11 Electroweak and photon channels as action layers

The electroweak material is retained as an action-layer owner block. Book 03 owns the action layer:

```math
\text{EW channel}=\text{single dimensional calibration section action layer}+\text{finite radial depth}+\text{typed weak unlock}.
```

Particle masses, charged-lepton generation, CKM orientation and gauge coefficient normalization are Book 04 matters. Book 03 only states the admissibility rule: the electroweak formulas must use the single action section and may not import an independent `M_Z`, `M_W`, proton or collider anchor.

The photon channel is the straight transit/phase channel of the terminal section. It is admissible as a benchmark action channel only because it preserves the invariant causal section and does not introduce a rest-return mass section.

## 03.12 Proton, neutron and beta/archive blocks as action mechanisms

The proton terminal-destructive readout and neutron beta/archive split blocks are not full hadron theory. They are action mechanisms handed to Book 04.

Book 03 keeps only the generic operator form:

```math
\text{terminal destructive readout}:
\quad
\lambda_{support}\rightarrow\lambda_{active}-\Delta_{readout},
```

and

```math
\text{beta/archive unlock}:
\quad
\text{finite active support}\rightarrow\text{weak unlock}\rightarrow\text{archive leakage/rate}.
```

The exact proton/neutron numerical comparison protocols remain in the matter book.

## 03.13 Gravity and cosmology cross-reference

The finite variational operator stack supplies one-section metrology and length-depth action. Gravity receives this in Book 07. Cosmology receives the finite-window archive-transfer mechanism in Book 08.

The S_DE insertion is therefore not a cosmology derivation inside Book 03. It is the action-side rule:

```math
\text{closed static coefficient}\rightarrow\text{finite spectrum}\rightarrow\text{finite window}\rightarrow\text{typed transfer}.
```

The actual BAO/archive pressure derivation belongs to Book 08.

## 03.14 Guardrails

Book 03 rejects the following moves:

1. adding a second dimensional anchor after `Lambda_act`;
2. reading a support eigenvalue directly as a particle mass without terminal/runtime transfer;
3. using a continuum action as primitive input before the finite halt quotient;
4. fitting bridge coefficients after seeing target data;
5. moving sector formulas from Book 04/07/08 back into the action book as if they were action proofs.

## 03.15 Claims covered or handed off

| Claim | Status | Canonical placement | Name | Forbidden shortcut | Falsification hook |
|---|---|---|---|---|---|
| `D0-SCENE-002` | CORE-ACTION | BOOK_03 | J_finite incidence/clique complex selects K(9,11,13) | Do not read J_finite incidence/clique complex as fitted polynomial for later constants. | Different admissible zero of the same typed obligations or wrong graph invariants. |
| `D0-MATH-001` | D0-RESOLUTION-EXACT | BOOK_03 | Finite phi-runtime and stop ideal | Do not add infinite correction layers below I12. | A physical scalar claim requires distinguishing below I12 inside D0 grammar. |
| `D0-ACTION-001` | CORE-ACTION | BOOK_03 | S_finite variational test functional/J_finite incidence/clique complex backbone | Do not close Born, entropy, leptons, or dynamics by unrelated formulas. | Mismatch between books or failure of Boundary Residual Eigenvalue r_∂ / I_B / action-spine consistency. |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | BOOK_03 | Lambda_act single action section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | Any closed prediction requiring an independent sector scale. |
| `D0-BOUND-001` | D0-RESOLUTION-EXACT | BOOK_03 | Boundary Residual Eigenvalue r_∂ and boundary curvature residual | Do not fit q_res with arbitrary scalar factor or reopen an infinite residual spiral. | Boundary residual cannot be produced below I12 by admissible cell. |
| `D0-QM-001` | CORE-MEASUREMENT | BOOK_02/BOOK_03 | Born/Hilbert finite trace ratio | Do not postulate continuum Hilbert space before finite trace. | Negative or unnormalized probabilities from finite Hessian readout. |
| `D0-VERTEX-001` | CORE-RUNTIME | BOOK_03 | Finite S-matrix registry | Do not compare raw graph amplitude directly to event count. | Failure of finite amplitude normalization or type split. |
| `D0-GAUGE-001` | CORE-RUNTIME | BOOK_04 via BOOK_03 operator mechanism | U(1) topological normalization and photon benchmark | Do not treat gamma/Z interference or event counts as closed by photon-only cert. | Failure of whitening identity or photon benchmark arithmetic. |
| `D0-EW-001` | CORE-RUNTIME | BOOK_03 | W/Z runtime ratio and on-shell angle | Do not use 3/13 or common-kernel variants as physical angle. | Failure to derive asymmetric kernels or trace ratio. |

## 03.16 Integrated calibration DAG and single action-section power matrix

The single dimensional calibration section rule is stated as an active action theorem, not as an index note.

D0 does not fail to derive kilograms or joules. Kilogram, joule, metre and second are external unit sections, not invariants. D0 derives the invariant finite action-section structure. The electron terminal record prints this structure into the SI convention. Once the external SI realization of the terminal charged cycle is chosen, all dimensional readouts must use the same section:

```math
C_e=\frac1{2(2\gamma-1)}=\frac1{38},
\qquad
\Lambda_{act}=38m_ec^2,
```

```math
\tau_0=\frac{h}{\Lambda_{act}},
\qquad
\ell_0=c\tau_0.
```

The integrated calibration DAG is

```text
finite verification algebra
  -> delta0, Omega8, K(9,11,13), rank/nullity data
  -> S_finite variational test functional / J_finite incidence/clique complex
  -> spectral and boundary invariants
  -> single action section Lambda_act
  -> matter, weak-rate, gravity, entropy, dynamics and survey readouts.
```

The power matrix is the operational content of the single dimensional calibration section theorem:

| object | D0 form | \(\Lambda_{act}\) power |
|---|---|---:|
| rest energy | \(M_a=\Lambda_{act}\mu_a\) | +1 |
| beta Q-value | \(Q_\beta=\Lambda_{act}\epsilon_\beta\) | +1 |
| decay rate | \(\Gamma=(\Gamma\tau_0)/\tau_0\) | +1 |
| tick/time | \(\tau_0=h/\Lambda_{act}\) | -1 |
| line length | \(\ell_0=ch/\Lambda_{act}\) | -1 |
| Planck length from depth | \(\ell_P=\ell_0/D_L\) | -1 |
| Newton bridge | \(G\sim\ell_P^2c^3/\hbar\) | -2 |
| cross-section area | \(\sigma\sim \ell_0^2\times\) dimensionless factor | -2 |
| trace probabilities and entropy weights | finite ratios | 0 |

Equivalently, the metrological DAG has one nonzero scale column.  Adding a proton, neutron, electroweak, Planck, dark-sector, collider or survey mass anchor raises the rank of the section matrix and is forbidden.

The section constraint may be represented in the finite variational operator stack by

```math
S_\Lambda(\tau,\Lambda)
=
(\Lambda\tau/h-1)^2
+
\left(38\tau/(h/(m_ec^2))-1\right)^2,
```

whose Euler point is

```math
\tau_0=\frac{h}{38m_ec^2},
\qquad
\Lambda_{act}=\frac h{\tau_0}=38m_ec^2.
```

This integrated block makes explicit that the single dimensional calibration section rule is a typed
metrology theorem, not a stylistic guardrail.  The Lean bridge types are
`DimensionlessCoreTraces` for the core trace shapes, `ExternalSICalibration`
for the SI dictionary, `SIMacroscopicPhysics` for SI outputs, and
`derive_physical_observables` for the typed bridge map.  The core trace object
does not produce SI constants by itself.

### 03.16.B Metrological gauge axiom: the single anchor is forced by dimensional analysis [THE]

The single-action-section rule is not a deficiency ("D0 cannot derive the kilogram"); it is the
Buckingham-Π theorem applied to a finite theory, and it is a strength. The Buckingham-Π theorem
states that any physical law relating quantities of `n` independent dimensions reduces to a relation
among dimensionless Π-groups *together with a choice of `n` dimensional standards*: the dimensionless
content is fixed by the theory, but mapping it onto numerical SI values requires fixing the
standards, and that choice is external to the dimensionless content by construction. A theory that
claimed to "derive the kilogram" from pure structure would be violating Buckingham-Π, not obeying it.

For D0 the count is exact. The power matrix above has **one** nonzero scale column, so the entire
dimensional content is carried by a **single** anchor `Λ_act = 38 m_e c²` (one mass/energy gauge;
length and time follow by `c` and `h`, which are themselves unit-defining conventions). Adding a
proton, neutron, electroweak, Planck, dark-sector, collider, or survey anchor raises the rank of the
section matrix and is forbidden (it would over-determine the gauge). So D0 carries:

- **zero** dimensionless free parameters — every dimensionless observable is a fixed finite invariant
  of the verification algebra (`δ₀, Ω₈, K(9,11,13)`, the rank/nullity data), with nothing to tune;
- **exactly one** dimensional anchor, the metrological gauge `Λ_act`.

This is the minimum a dimensional theory can carry and still speak SI numbers — one standard, no
tunable dimensionless freedom. The Standard Model, by contrast, carries on the order of two dozen
free dimensionless parameters (the gauge couplings, the Yukawas/masses, the CKM and PMNS mixing
angles and phases, the Higgs self-coupling, `θ_QCD`) *plus* its own dimensional anchors. The
contrast is structural: D0's dimensionless sector is rigid (a classification, §05.8a), and only the
metrological gauge is chosen.

The anchor is a **gauge choice in the metrological sense**, exactly like the former platinum–iridium
kilogram prototype or the modern convention `c ≡ 299\,792\,458\ \mathrm{m/s}`: declaring `Λ_act` fixes
the standard against which every dimensionless D0 invariant is read, and the choice has no physical
content of its own — it is the unit, not a prediction. Calling this a "failure to derive the
kilogram" mistakes the gauge for an observable. The forced statement is the rank-1 metrological
section with zero dimensionless freedom; the one anchor is the gauge that section analysis requires.

## 03.17 Integrated beta/scattering comparison protocol as finite transition discipline

The beta-operator and scattering-comparison protocol notes clarify that collider or scattering formulas are downstream finite-transition comparison protocols, not raw event-count or continuum-field oracles.

A scattering comparison must declare

```math
P(a\to b)=\frac{|S_{ba}|^2}{\sum_c |S_{ca}|^2},
```

with the finite transition operator typed by the detector/finite variational operator stack and the external detector cuts placed only in the comparison protocol layer.  The allowed chain is

```text
finite variational operator stack -> finite transition operator -> quadratic transition weights -> detector comparison protocol.
```

Forbidden shortcuts are: collider normalization as a second action scale, post-hoc channel relabelling, and treating a finite D0 transition registry as a full detector simulator.

## 03.18 Terminal-cycle derivation of the `38` action section

The action section `Λ_act=38m_ec^2` is not a definition of the electron mass and not a fit to electron data.  The dimensionless coefficient `38` is fixed before SI units enter.

The graph-birth carrier has

```math
|V|=9+11+13=33,
\qquad Rank=3,
\qquad nullity=|V|-Rank=30.
```

The reduced terminal echo depth is therefore

```math
\gamma={nullity\over Rank}=10.
```

The primitive weak/terminal unlock uses a forward-return audit with the halt section counted once:

```math
N_{unlock}=2\gamma-1=19.
```

The full terminal action section has two orientation sides, hence

```math
N_{act}=2N_{unlock}=2(2\gamma-1)=38.
```

Only after this dimensionless finite-cycle number is fixed is the SI electron rest-energy used as a section dictionary:

```math
\Lambda_{act}=N_{act}m_ec^2=38m_ec^2.
```

Thus the electron mass is not predicted from itself.  The finite theorem predicts the dimensionless full-cycle action coefficient `38`; the external electron rest energy supplies the SI unit section used to express the D0 action scale in joules or MeV.

## 03.19 Integrated single dimensional calibration section and boundary-residual closure cells

This section closes the action/metrology rows that cannot remain as ledger-only claims.  The active theorem text now carries the proof-cell content required for release status.

### 03.19.1 Lambda action-section rigidity

**Theorem.**  All dimensionful mass/action readouts in D0 factor through one and only one action section.  The finite theory determines the admissible section type and slot-count; SI units supply only the external representative.

The electron full-cycle section is

```math
C_e={1\over 2(2\gamma-1)}={1\over 38},
\qquad
\Lambda_{act}=38m_ec^2.
```

The causal line/tick dictionary is

```math
\ell_0^{D0}=1,
\qquad
\tau_0^{D0}=1,
\qquad
c_{D0}=\ell_0^{D0}/\tau_0^{D0}=1.
```

In SI representatives the same section is

```math
\tau_0={h\over 38m_ec^2},
\qquad
\ell_0=c\tau_0={h\over 38m_ec},
\qquad
\Lambda_{act}={h\over\tau_0}=38m_ec^2.
```

The active certificate records

```text
τ0 = 2.1298157324596072e-22 s,
ℓ0 = 6.3850269352113602e-14 m,
ℓ0/τ0 = 299792458 m/s,
Λ_act = 19.417960126286623 MeV.
```

**Closure.**  The quotient/resolution field is explicit: the quotient is not another sector scale, but the equivalence class of all dimensionful readouts under the single action section.  A second proton, W/Z, Planck, Hubble or dark-sector anchor falsifies the claim.

This closure is verified by the finite certificate.

### 03.19.2 q-mass and boundary curvature residual

The boundary residual is not a fitted scalar.  It is the stationary solution of the boundary block of the finite variational test functional action:

```math
S_\partial(r,I)=\left(r-r_0(1+I/d_9)\right)^2+
\left(I-\Delta_\lambda^2\delta_0^3\right)^2.
```

The Euler equations select

```math
I_* = \Delta_\lambda^2\delta_0^3,
\qquad
r_* = r_0(1+I_*/d_9),
\qquad
c_\partial^2=\delta_0^6r_*.
```

The same action-gauge closure fixes

```math
S_\Lambda(\tau,\Lambda)=
(\Lambda\tau/h-1)^2+
\left(38\tau/(h/(m_ec^2))-1\right)^2,
```

hence

```math
\tau_0=h/(38m_ec^2),
\qquad
\Lambda_{act}=h/\tau_0=38m_ec^2.
```

**Closure.**  The linear/operator field is explicit: the boundary residual comes from the finite boundary Euler block of the global action, not from a post-hoc scalar correction.  The `q_mass` bridge remains a quotient dictionary only after the stationary residual has been fixed.

This closure is verified by the finite certificate.

## 03.20 Single-section hostile uniqueness: the integer 38

The action section uses the finite graph finite variational operator stack before particle-sector finite readouts.  Let

```math
|V|=33,
\qquad \operatorname{rank}(A)=3,
\qquad \nu=|V|-\operatorname{rank}(A)=30.
```

Then the terminal coefficient is

```math
\gamma=\nu/\operatorname{rank}(A)=10,
\qquad
N_{unlock}=2\gamma-1=19,
\qquad
N_{act}=2N_{unlock}=38.
```

The dimensionful section is therefore

```math
\Lambda_{act}=38m_ec^2.
```

The electron unit is a section for comparison, not the source of the integer.  Nearest-neighbour controls fail as follows: `37` leaves one half-cycle channel missing; `39` adds a non-D0 channel; `40` double-counts the fixed witness endpoint.  Thus `38` is an operator lock of the closed two-direction action section, not a fitted electroweak coefficient.

## 03.21 Finite spectral-action ladder

The primary D0 gravity/action statement is finite spectral algebra, not a continuum Einstein-Hilbert integral. The continuum integral is a later bridge reading after finite heat-trace support has been declared.

For a density floor `rho` and finite Laplacian `L`, the active ladder is:

```text
W L W = conformalLaplacian L rho
Tr(W L W) = a0 volume proxy
Tr((W L W)^2) = diagonal square term + 2 * discreteEHActionProxy
|Tr((W L W)^k)| has floor-bounded absolute control for higher powers.
```

The off-diagonal action proxy carries a factor `1/2` because the double sum counts both orientations of an undirected edge:

```text
2 * discreteEHActionProxy
  = sum_i sum_j if i != j then L_ij^2 / (rho_i rho_j) else 0.
```

Lean ownership:

```text
D0.Geometry.HeatTraceA2Decomposition.heat_trace_sq_exact_decomposition
D0.Geometry.HeatTraceA2Decomposition.double_count_factor_guard
D0.Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor
D0.Geometry.SpectralActionLadder.a0_is_volume_proxy
D0.Geometry.SpectralActionLadder.a2_is_eh_proxy
D0.Geometry.SpectralActionLadder.higher_powers_floor_bounded
```


## 03.21a Gap labels do not create new action sections

The topological gap labels assigned to spectral gaps do not introduce new action sections or ad-hoc scalar field parameters. They serve as discrete indices of existing sectors on the tiling hull rather than defining new energy anchors. All calculations remain strictly constrained by the single metrological section $\Lambda_{act} = 38 m_e c^2$. The Lean owner records that gap labeling requires a frozen operator, and the integration is checked by the final bridge index.

## 03.22 Action-to-selector closure rule

An action operator becomes a particle-sector statement only after it induces a finite selector or a finite response readout.  The finite variational operator stack alone is not enough.  The required chain is:

```text
finite action support
→ response / score functional
→ strict selector certificate or normalized response theorem
→ observable transfer only after the internal object is fixed.
```

This removes the previous bridge-only reading in which a large action number could be quoted as if it directly selected a particle mass. The active theory requires the intermediate operator: response for probability claims, strict selector for particle identity claims, and transfer operator for mass/comparison claims.
## 03.23 K(9,11,13) Torus Shell Interpretation

The preceding dynamic source is the D0 time-transition matrix:

```text
T time evolution
-> |Tr(T^2)|=3 generation carrier
-> |Tr(T^3)|=4 ABCD capacity
-> |Tr(T^5)|=11 memory torus
-> K(9,11,13) torus shell geometry
```

The finite action/topology spine now gives the structural home for the D0 memory
torus:

```text
D=9  puncture/interface shell  = R-r = 1
D=11 memory torus core shell   = R
D=13 outer shell               = R+r
```

The dimensionless torus aspect is frozen as

```text
(R+r)/(R-r) = phi^5
```

with the algebraic core owner being the torus-core geometry origin.  Book 03
does not use PDG data to create this geometry; PDG Core-13 is an external
embedding passport (a PDG diagnostic, not the forcing certificate).

The trace ladder above states the FACTS (`3`, `4`, `11`, the K(9,11,13) home).
What follows gives the *forcing*: each of the four shell
quantities is not read off the `T`-traces by analogy — it is the unique M1
survivor of a distinguish-itself-without-a-catalog requirement.  The chain runs
outside-in: anchor 4 -> two loops -> torus -> defect -> closing shell + phi ->
address step +2 -> nested 9-11-13.

### 03.23.1 D_anchor = 4 is irreducible (the ABCD capacity)

Status: FORCED [^b03-41].

`|Tr(T^3)| = 4` is the ABCD capacity; the forcing says *why a closed scene needs
exactly 4*.  A minimal closed scene must realize exactly the four ABCD roles of
the role alphabet (alphabet owned at BOOK_01 01.7 / BOOK_02 02.4; cite, do not
re-derive):

```text
A = Scale    (closure phi/psi)
B = Memory   (the torus, below)
C = Defect   (novelty / order)
D = Closure  (the boundary shell)
```

The "4" is the minimal count of realizable roles, not a count of space
dimensions. The fork is M1:

- `D_anchor < 4`: some role is unrealized -> the scene is not closed -> an
  external prop is needed to stand in for the missing role. Banned.
- `D_anchor > 4`: empty address slots appear; to tell an empty slot from a
  significant one you must import an exogenous significance catalog. Banned.

Both deviations re-introduce the external catalog M1 forbids, so `D_anchor = 4`
is the unique survivor. This anchor 4 is the start summand of the address
ladder (03.23.6).

### 03.23.2 One loop cannot carry memory -> a second independent loop is forced

Status: FORCED [^b03-42].

`|Tr(T^5)| = 11` is named the "memory torus"; the forcing says *why memory needs
two cycles, not one*. Reduction to a mode catalog:

1. Suppose a single loop `gamma`, topology `Z`. Its state is one integer `k`
   (the class `gamma^k`); every operation just changes `k`.
2. `k` alone cannot say which mode produced it: Write (change `k`) vs Read
   (sample `k` without changing it) are indistinguishable from the value.
3. Separating the modes needs an exogenous flag `M in {R,W}`.
4. `M` is not derivable from the topology `Z` -> it is an external catalog. Banned
   by M1.

The only M1-admissible fix is a *second independent loop*: one cycle carries the
Value, the other carries the Operation/Access. A lone `Z` is structurally blind
to write-vs-read; two independent cycles is the minimum that is not.

### 03.23.3 The torus T^2 is the minimal two-cycle carrier

Status: FORCED [^b03-43].

Given two independent closed loops (write/read) that are not powers of one
another, the minimal orientable compact carrier is the genus-`g=1` surface, i.e.
the torus `T^2`:

- For an orientable surface of genus `g`, the first homology `H_1` has rank `2g`.
- Two independent cycles therefore force `g >= 1`.
- `g = 1` (the torus) is the minimal case and realizes exactly two independent
  cycles.
- `g >= 2` over-supplies cycles: choosing *which* pair is write/read is a
  non-canonical basis choice = an external catalog. Banned by M1.

So `T^2` is the unique minimal home of the two forced loops — this is the
homology-rank derivation behind the `D=11` "memory torus core shell".

### 03.23.4 A defect is necessary: pure T^2 loses order

Status: FORCED [^b03-44].

The `D=9` shell is named a "puncture/interface" shell; the forcing says *why a
puncture/defect is mandatory*, not decorative. By contradiction:

1. On a pure torus the fundamental group `pi_1(T^2) = Z^2` is abelian — any two
   base loops commute.
2. Then "Write then Read" and "Read then Write" lie in the same path class: the
   *order* of the two operations is not encoded.
3. But history-memory (03.2) requires order to leave a distinguishable effect,
   else history collapses to a mere counter.
4. The minimal way to break commutativity without adding extra cycles (which
   would demand a choice catalog) is a single defect `(.)`, injecting a
   non-commutative holonomy on the same loop basis.

The contradiction is removed only with one defect. The `D=9` puncture is thus the
minimal noncommutativity injection that recovers order memory — forced, not a
labelling convenience.

### 03.23.5 The outer shell + φ-scaling are necessary for closure

Status: FORCED [^b03-45].

The aspect `(R+r)/(R-r) = phi^5` is a result of the torus-core geometry. The
forcing supplies the necessity of `D=13`:

- An interior defect (03.23.4) plus a memory-circulation zone (03.23.3) leaves
  the global topology open; closing it requires an outer shell (the Closure role
  `D` of 03.23.1).
- The shell's scaling cannot carry a free parameter (M1). The only
  self-consistent parameter-free scale is the positive root of

```text
r^2 - r - 1 = 0   =>   r = phi
```

equivalently the coarse-graining fixed point `r = 1 + 1/r` (shell contribution
`1` plus inversion/memory contribution `1/r`, normalized by one constant fixed to
`c := 1` in CORE). So the outer shell *must* exist and *must* scale by `phi`;
nothing else closes the topology without an exogenous scale catalog. The `phi^5`
aspect (03.23.6) is then the orientation-preserving address gap between the
defect shell and the outer shell, not an independent input.

### 03.23.6 Address step +2 forces the spectrum {9, 11, 13}

Status: FORCED (forcing: GOLDEN THE 3.11.B; Lucas/orientation machinery owned at
BOOK_05 §05 and BOOK_06 06.36, `Tr(T^n) = (-1)^n L_n`).

The signed-Lucas machinery attaches to the toral time operator; here it drives
the *address ladder*. Forcing of the step and the exact triple:

1. In CORE the scale powers `phi^n` are approximated by integer Lucas numbers
   `L_n = phi^n + psi^n`, `psi = -phi^-1`.
2. The approximation error fixes a `Z_2` orientation class:

```text
eps_n := phi^n - L_n = -psi^n = (-1)^{n+1} phi^-n
```

   so `n=5` carries holonomy parity `+`, `n=6` carries parity `-`.
3. A step `+1` (`5 -> 6`) flips the orientation/holonomy class; gluing the layers
   then needs an exogenous `Z_2` orientation bit not stored in the address. That
   is an external catalog. Banned by M1. (Equivalently: `+1` makes time-gluing a
   twist rather than a cylinder, requiring an external choice of global heat-trace
   direction.)
4. A step `+2` (`5 -> 7`) preserves the orientation class; the gluing closes with
   no external parameter. So the address step is forced to `+2`. This `+2`-invariance
   is now machine-checked: the address step is the identity element of the double
   cover `Z(Q8)`, proved as `det(T^{n+2}) = det(T^n)` (with the `+1` flip
   `det(T^{n+1}) = -det(T^n)` as the negative control), so the orientation class is the
   single `Z_2 = Z(Q8)` of the seven-incarnation concentrator (BOOK_02 §02.34).

Starting from `D_anchor = 4` (03.23.1) plus the operational start `D_Sigma = 5`
(5 distinguished address classes, below which roles collide), the ladder is:

```text
Defect : 4 + 5 = 9
Memory : 9 + 2 = 11
Shell  : 11 + 2 = 13
```

Any step other than `+2` re-imports an external gluing parameter, so `{9,11,13}`
is the unique M1-admissible spectrum. The address gap defect->shell is `13 - 9`
in integer addresses; in the continuous `phi`-scale it is the `phi^5` aspect of
03.23.5 (Lucas `L_5 = 11`, the integer image of the same return — cf. BOOK_06
06.37 for the `phi^5 = 11 + xi5` split).

### 03.23.7 Nested three-zone: Shell(13) ⊃ Torus(11) ⊃ Defect(9)

Status: FORCED [^b03-46].

The three shells are not three independent radii; they nest, and the nesting has
a direction. The minimal configuration is

```text
Shell (13)  ⊃  Memory-torus (11)  ⊃  Defect (9)
R+r            R                     R-r
```

forced by closing the scale *from outside inward*: there is no external scale
catalog to anchor an absolute radius, so the only self-consistent assignment is
the relative nesting where the outer Closure shell (13) contains the memory zone
(11) which contains the defect core (9). This nesting is a structural reading of
the aspect ratio; the forcing is that the outside-in closure is the *only*
parameter-free way to order the three zones.

### 03.23.8 Embedding boundary

The geometry above is forced internally (03.23.1–03.23.7) with no SI length and
no external mass unit. The PDG Core-13 passport is an external-data *diagnostic*
that reproduces the frozen Core-13 embedding discipline against pinned PDG masses;
it does not create, tune, or promote any of the operators forced here. The downstream
flavour/generation use of this geometry lives at BOOK_04 04.T (Torus/Core13 matter
integration boundary).
## 03.24 Lefschetz finite incidence/clique complex counts from the time ladder

The anti-periodic finite incidence/clique complex count is read as
`NFermion(n)=|det(T^n+I)|`.  The first active closure checks are:

```text
NFermion(3)=4
NFermion(4)=9
NFermion(5)=11
NFermion(3)+NFermion(4)=13
NFermion(6)=20
```

These are finite trace/automorphism counts.  They are not empirical particle
multiplicities and do not replace downstream selector or passport protocols.

## 03.25 CVFT master bootstrap action

The D0 action layer uses a single finite bootstrap functional:
\[
\mathcal B_N
=
\beta^{-1}\log\operatorname{Tr}(e^{-\beta\Delta_N(V)})
-
\log\det(I-zF_N(V)).
\]
The stationarity condition \(\delta\mathcal B_N=0\) locks finite spectral geometry to feedback-return thermodynamics. The discrete derivative \(\partial_V A_N=A_{N+1}-A_N\) acts over rank evolution \(V_N=\operatorname{rank}(P_N)\). The single action section is unchanged by this rank step; no second mass anchor is introduced.

## 03.26 Golden tick gate

Let \(p=\varphi^{-1}\). The detector-clock fixed point is realized by the finite active/archive splitter

\[
U_\varphi=
\begin{pmatrix}
\sqrt p\,I&-pI\\
pI&\sqrt p\,I
\end{pmatrix}.
\]

Since \(p+p^2=1\), this block is unitary. It yields

\[
F_N=p^2P_N=\varphi^{-2}P_N,
\qquad
U_{\rm eff}^\dagger U_{\rm eff}=pP_N=\varphi^{-1}P_N
\]

on the declared detector-clock block. This construction supplies the finite action-level gate for informational mechanics.


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b03-1]: open obligation — cert obligation open
[^b03-2]: forcing: GOLDEN DEF 15.2.1, BOOK-II-MECHANISM
[^b03-3]: forcing: GOLDEN FORMALISM 15.2.2, BOOK-II-MECHANISM
[^b03-4]: forcing: GOLDEN DEF 15.2.1 + FORMALISM 15.2.2, BOOK-II-MECHANISM
[^b03-5]: forcing: GOLDEN DEF 15.4.1, BOOK-II-MECHANISM
[^b03-6]: forcing: GOLDEN THE 15.4.2, BOOK-II-MECHANISM
[^b03-7]: forcing: GOLDEN THE 15.4.2, BOOK-II-MECHANISM
[^b03-8]: forcing: GOLDEN DEF II.3.1, BOOK-II-MECHANISM
[^b03-9]: forcing: GOLDEN THE 4.1.2, BOOK-II-MECHANISM
[^b03-10]: forcing: GOLDEN THE 4.1.2, BOOK-II-MECHANISM; completeness ⊥-argument
[^b03-11]: forcing: GOLDEN REM II.3.A.1, BOOK-II-MECHANISM
[^b03-12]: open obligation — cert obligation open
[^b03-13]: forcing: GOLDEN DEF II.3.APPX8.2.1, BOOK-II-MECHANISM
[^b03-14]: forcing: GOLDEN THE II.3.APPX8.2.1a, BOOK-II-MECHANISM
[^b03-15]: forcing: GOLDEN THE II.3.APPX8.2.1a, BOOK-II-MECHANISM; ⊥-proof, three-constraint closure
[^b03-16]: forcing: GOLDEN LEM II.3.APPX8.2.2, BOOK-II-MECHANISM
[^b03-17]: forcing: GOLDEN LEM II.3.APPX8.2.2, BOOK-II-MECHANISM
[^b03-18]: forcing: GOLDEN DEF, BOOK-II-MECHANISM §II.3.APPX8.3.A
[^b03-19]: forcing: GOLDEN THE, BOOK-II-MECHANISM §II.3.APPX8.3.2
[^b03-20]: forcing: GOLDEN THE II.3.APPX8.3.2, BOOK-II-MECHANISM; ⊥M1 on the coupling prefactor
[^b03-21]: forcing: GOLDEN COR II.3.APPX8.3.A.2, BOOK-II-MECHANISM
[^b03-22]: forcing: GOLDEN COR II.3.APPX8.3.A.2, BOOK-II-MECHANISM; tautology, not postulate
[^b03-23]: forcing: GOLDEN DEF, BOOK-II-MECHANISM §II.3.APPX8.4.1
[^b03-24]: forcing: GOLDEN DEF II.3.APPX8.4.1, BOOK-II-MECHANISM
[^b03-25]: forcing: GOLDEN BRIDGE 11.C, BOOK-III-SPECTRUM
[^b03-26]: forcing: GOLDEN DEF 11.C.1, BOOK-III-SPECTRUM
[^b03-27]: forcing: GOLDEN THE 11.C.2, BOOK-III-SPECTRUM
[^b03-28]: forcing: GOLDEN THE 11.C.2, BOOK-III-SPECTRUM; least action from `P\sim\varphi^{-L_{code}}` survival
[^b03-29]: forcing: GOLDEN REM II.D.RG.NOCT, BOOK-II-MECHANISM
[^b03-30]: forcing: GOLDEN REM II.D.RG.NOCT + THE II.3.APPX8.5.2, BOOK-II-MECHANISM; counterterm ban + `\kappa`-residual as the unique admissible residual
[^b03-31]: forcing: GOLDEN THE 51.4, BOOK-VI-EXTENSIONS
[^b03-32]: forcing: GOLDEN THE 51.4, BOOK-VI-EXTENSIONS; ⊥M1 on an external ordering catalog
[^b03-33]: forcing: GOLDEN LEM 51.4.A, BOOK-VI-EXTENSIONS
[^b03-34]: forcing: GOLDEN Appendix II.C / APPX-4, THE II.3.APPX4.*
[^b03-35]: forcing: GOLDEN THE II.3.APPX4.2.2a
[^b03-36]: forcing: GOLDEN THE II.3.APPX4.0A.7
[^b03-37]: forcing: GOLDEN THE II.3.APPX4.10A.6, DEF II.3.APPX4.13.1
[^b03-38]: forcing: GOLDEN THE II.3.APPX4.9.3
[^b03-39]: forcing: GOLDEN THE II.3.APPX4.B.2
[^b03-40]: forcing: GOLDEN LEM II.3.APPX4.15.2, DEF II.3.APPX4.16.3
[^b03-41]: forcing: GOLDEN THE 3.4.B
[^b03-42]: forcing: GOLDEN THE 3.5.A
[^b03-43]: forcing: GOLDEN THE 3.6.A
[^b03-44]: forcing: GOLDEN THE 3.7.B
[^b03-45]: forcing: GOLDEN THE 3.9.A
[^b03-46]: forcing: GOLDEN THE 3.12.B
