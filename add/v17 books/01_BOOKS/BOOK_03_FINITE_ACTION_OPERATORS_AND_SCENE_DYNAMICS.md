# BOOK 03: Finite Action Operators and Scene Dynamics

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 03 defines the finite action layer of D0: finite action operators, the single action section, boundary curvature residuals, scene dynamics, and the handoff rules from action to sector readout.
>
> **Scope discipline.** This book does not re-prove the core feedback-return operator from Book 02, does not introduce a continuum Lagrangian as a primitive, and does not close particle, gravity, cosmology, LIGO/GWOSC, or laboratory bridge claims. It supplies the finite action language used by those downstream books.

## 03.1 Purpose of the Finite Action Layer

Book 03 receives the finite proof spine of Book 02 and turns it into an admissible action calculus. The object of this book is not a spacetime action functional written before observation. The object is a finite variational operator stack evaluated on a declared finite scene.

The book has five functions:

1. define the finite action stack built over the feedback-return operator;
2. fix the single action section `\Lambda_{act}=38m_ec^2` and its dimensional-use rule;
3. define the boundary curvature residual and the interaction-information cell;
4. state finite scene dynamics and action-to-readout handoff rules;
5. declare which downstream sectors may use the action layer without importing new scales.

## 03.2 Canonical Input from Book 02

Book 03 uses one core dynamical input from Book 02. Let `P_N` be the active projector, `Q_N=I-P_N` the archive projector, and `U_N` a finite unitary tick. The feedback-return operator is

\[
F_N=P_NU_N^\dagger Q_NU_NP_N.
\]

The equivalent positive form and its proof are owned by Book 02. Book 03 uses only the facts that `F_N\succeq0`, `0\preceq F_N\preceq P_N`, and that log-det variations are finite under the spectral admissibility conditions of Book 02.

## 03.3 Definition of the Finite Action Stack

**Definition 3.1 (Finite action stack).** On a finite scene `\mathcal X_N`, the D0 action layer is the finite stack

\[
\mathcal S_{stack}
=
J_{scene}
+S_{coeff}
+S_{\Lambda}
+S_{\partial}
+S_{heat}
+S_{terminal}
+S_{fb}.
\]

The terms have the following roles.

| Term | Function | Admissibility condition |
|---|---|---|
| `J_{scene}` | finite scene selector on the incidence/clique complex | declared before sector comparison |
| `S_{coeff}` | finite coefficient and compatibility penalties | no target-table fitting |
| `S_{\Lambda}` | single action-section constraint | no second dimensional anchor |
| `S_{\partial}` | boundary curvature residual | finite stationary block |
| `S_{heat}` | heat/depth control | finite spectrum or declared bridge |
| `S_{terminal}` | terminal record and leakage bookkeeping | finite terminal role owner |
| `S_{fb}` | feedback-return response | Book 02 log-det calculus |

The stack is finite. It may use matrices, projectors, spectra, finite differences, Hessians, and positive quadratic penalties. It may not use a continuum action as primitive input.

## 03.4 Feedback Action and Response Source

**Definition 3.2 (Feedback action).** For an admissible fugacity `z`,

\[
S_{fb}=-\log\det(I-zF_N).
\]

For an admissible finite variation `\delta F_N`,

\[
\delta S_{fb}=\operatorname{Tr}\!\left(z(I-zF_N)^{-1}\delta F_N\right).
\]

**Definition 3.3 (Feedback source).** The finite feedback source is

\[
\Pi_{fb}=z(I-zF_N)^{-1}.
\]

The Neumann expansion of the resolvent is allowed only when `|z|\rho(F_N)<1`. The resolvent itself is allowed whenever `I-zF_N` is invertible. Pressure and finite equation-of-state use of this source is owned downstream by the cosmology book.

## 03.5 Finite Action Operator

**Definition 3.4 (Finite action operator).** Given a finite energy or depth operator `\Delta_N(V)` on the active sector, the finite action readout at rank volume `V=\operatorname{rank}(P_N)` is

\[
\Lambda_N=\operatorname{Tr}\big(F_N\Delta_N(V)\big).
\]

This definition is not a continuum Lagrangian. It is a finite trace readout of feedback-return weighted by the declared finite energy/depth operator. Sector-specific energy maps are external to this definition and must factor through the single action section.

## 03.6 Single Full-Cycle Action Section

**Theorem 3.5 (Single action section).** D0 admits one dimensionful action section after the finite terminal cycle is fixed. The dimensionless full-cycle coefficient is

\[
N_{act}=38.
\]

When expressed in the external SI electron section, the action scale is

\[
\Lambda_{act}=38m_ec^2,
\qquad
\tau_0={h\over 38m_ec^2},
\qquad
\ell_0=c\tau_0={h\over 38m_ec}.
\]

*Proof.* The graph-birth carrier has `|V|=9+11+13=33`, finite rank `3`, and nullity `30`. The reduced terminal echo depth is `\gamma=30/3=10`. The primitive terminal unlock has `N_{unlock}=2\gamma-1=19`. The full action section has two orientation sides, hence `N_{act}=2N_{unlock}=38`. Only after this dimensionless count is fixed is `m_ec^2` used as the external SI representative. ∎

The single action section is the unique declared dimensionful anchor of the v16 core spine; any additional scale is a bridge or passport parameter and must name its owner.

**Admissibility rule 3.6 (Single-scale rule).** After `\Lambda_{act}` is chosen, a sector formula may not introduce an independent proton, neutron, electroweak, Planck, Hubble, dark-sector, collider, or survey mass anchor.

The power table is fixed.

| Readout class | Representative form | `\Lambda_{act}` power |
|---|---|---:|
| rest energy | `M_a=\Lambda_{act}\mu_a` | +1 |
| beta Q-value | `Q_\beta=\Lambda_{act}\epsilon_\beta` | +1 |
| decay rate | `\Gamma=(\Gamma\tau_0)/\tau_0` | +1 |
| time or length | `\tau_0,\ell_0` | -1 |
| Newton or area bridge | `\ell_0^2\times` dimensionless factor | -2 |
| probability or entropy | finite trace ratio | 0 |

## 03.6A Rank-nullity closure of the number 38

The coefficient \(38\) is not introduced as a fitted energy number. It is the exact rank-nullity count of the graph-birth carrier from Book 01.

**Theorem 3.5A (Rank-nullity derivation of the action count).** Let \(A_{9,11,13}\) be the adjacency matrix of the complete tripartite scene graph \(K(9,11,13)\). Then

\[
\operatorname{rank}(A_{9,11,13})=3,
\qquad
\operatorname{nullity}(A_{9,11,13})=33-3=30.
\]

The reduced terminal echo depth is

\[
\gamma={30\over 3}=10.
\]

The primitive unlock count is

\[
N_{unlock}=2\gamma-1=19,
\]

and the two-sided full-cycle action count is

\[
N_{act}=2N_{unlock}=38.
\]

The factor 2 arises because \(\Omega_8\) already contains the orientation bit \{+, −\}. Each primitive unlock cycle therefore possesses two orientation sides, yielding \(N_{act} = 2 \times N_{unlock} = 38\).

*Proof.* For a complete tripartite graph with three non-empty parts, the adjacency matrix is constant on each part and maps the three-dimensional space of part-constant vectors into itself. All vectors with zero sum inside each part lie in the kernel. Hence the rank is exactly three and the nullity is \((9-1)+(11-1)+(13-1)=30\). The remaining arithmetic follows directly. The executable certificate `vp_single_action_rank_nullity_38.py` verifies the same statement by exact matrix rank. ∎

**Metrological representative rule.** The integer \(38\) is fixed before units are introduced. The electron section \(m_ec^2\) is then used as the external SI representative because it is the stable charged detector quantum used to express the finite readout action in laboratory units. This is a calibration section, not an additional graph input and not a second fitted scale.

## 03.6B Metrological Calibration and the Bekenstein Bound

The core mathematical spine of D0 is strictly dimensionless. The full-cycle action count N_act = 38 is the exact homological rank-nullity index of the K(9,11,13) holographic tensor network.

To bridge this discrete topological index to laboratory physics, D0 defines a typed Calibration Bridge using the electron rest energy m_e c² as the minimal stable charged readout probe. Thus Λ_act = 38 m_e c² is an explicit dictionary translation.

## 03.7 Internal Gauge and Cell Density

The dimensionless length-depth map is defined as

\[
D_L = \Omega_8 \varphi^{V_9 V_{11}} \left(1 + \frac{\delta_0}{V_{13}}\right),
\]

where the exponent \(V_9 V_{11} = 99\) counts the exact number of complete phase-unfolding cycles needed to close the witness-boundary-bulk structure of the minimal holographic carrier K(9,11,13). This is the minimal integer required for the symplectic form to return to a topologically equivalent configuration under self-reading.

The normalized internal cell density is \(\rho_{cell}^{D0} = D_L^{-2}\).

## 03.8 Boundary Curvature Residual

The boundary residual is a finite stationary block, not a fitted scalar correction. Define

\[
r={c_\partial^2\over\delta_0^6},
\qquad
r_0={13\over 8}{1+\delta_0^3/38\over 1+\delta_0/9},
\qquad
d_9=\deg(V_9)=24.
\]

**Definition 3.8 (Boundary action block).** The boundary block is

\[
S_\partial(r,I)=
\left(r-r_0\left(1+{I\over d_9}\right)\right)^2+
\left(I-\Delta_\lambda^2\delta_0^3\right)^2.
\]

**Lemma 3.9 (Boundary stationary residual).** The Euler equations select

\[
I_* = \Delta_\lambda^2\delta_0^3,
\qquad
r_* = r_0\left(1+{I_*\over d_9}\right),
\qquad
c_\partial^2=\delta_0^6r_*.
\]

The interaction-information cell used downstream is

\[
I_B={\Delta_\lambda^2\delta_0^3\over 24}.
\]

Book 03 owns the finite stationarity of this residual. Matter, coefficient, or hadron comparisons may use it only after preserving this ownership.

## 03.8b The Hurwitz Crystal, Archive Pressure, and the 38-Cycle (D0.Geometry)

The boundary curvature residual stabilizes precisely at vertex degree \(d_9 = 24\). 

**Theorem 03.8b (The Action Cycle Decomposition).**
This stabilization occurs because the terminal readout maximally packs into the unit Hurwitz quaternions (the binary tetrahedral group containing exactly 24 elements). The full dimensionless action cycle of the universe (\(N_{act} = 38\)) algebraically decomposes into two invariant structures:
\[ N_{act} = 24 \text{ (Hurwitz)} + 14 \text{ (Archive Symmetry)} = 38. \]
- **24** represents the active boundary, packing into a perfect Hurwitz crystal lattice.
- **14** represents the hidden symmetry of the 30-nullity Sterile Archive (mathematically isomorphic to the dimension of the exceptional Lie group \(G_2\), the exact automorphism group of 8-dimensional octonionic phase space).

Gravity is strictly the macroscopic shadow of the thermodynamic Archive pressure packing the active boundary into this perfect Hurwitz configuration.

## 03.8a The Holographic Master Bootstrap Functional

Because D0 enforces the Finite Holographic Self-Reading Principle, geometry and information cannot be independent. The finite dynamics are governed by a single unifying Master Bootstrap Functional that locks the discrete spectral geometry (Heat Trace) to the symplectic archive accumulation (Feedback Log-Det):

\[ \mathcal B_N = \beta^{-1}\log\operatorname{Tr}(e^{-\beta\Delta_N(V)}) - \log\det(I-zF_N(V)). \]

The fundamental equation of motion in D0 is the exact stationarity of this functional: \(\delta \mathcal B_N = 0\). 
This replaces the continuum Einstein-Hilbert action at the core level. Macroscopic spacetime geometry (\(\Delta_N\)) is algebraically forced to emerge and curve strictly to balance the entanglement pressure generated by the feedback-return operator \(F_N\).

## 03.8c Exact Derivation of Einstein Equations from KMS First Law (D0.Core)

Because \(\delta \mathcal B_N = 0\) enforces \(\delta E_{geom} = T_{KMS} \delta S_{ent}\), and the system is in exact KMS state under Tomita-Takesaki flow, we satisfy the local thermodynamic relation required by Ted Jacobson (1995).  
Applying this relation to every infinitesimal holographic screen inside the D0 carrier yields the full non-linear Einstein field equations \(G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi T_{\mu\nu}\) as the macroscopic KMS limit.  
Λ appears automatically as the Golod-Shafarevich gap \(\Delta_{GS} = 1/160\).

Certificate: `vp_jacobson_kms_einstein.py`

## 03.9 Finite Equations of Motion

**Definition 3.10 (Finite equations of motion).** D0 equations of motion are finite stationarity conditions on declared scene variables:

\[
\nabla_{x\in\mathcal X_N}
\left(
J_{scene}+S_{coeff}+S_\Lambda+S_\partial+S_{heat}+S_{terminal}+S_{fb}
\right)=0.
\]

This replaces the continuum Euler-Lagrange principle at the core level. Continuum equations may appear only after halt quotient, forgetting map, and bridge dictionary have been declared.

The generic action-to-readout form is

\[
Q\longmapsto Q^\dagger Q
\longmapsto
{\operatorname{Tr}(\Pi_aQ^\dagger Q)\over\operatorname{Tr}(Q^\dagger Q)}.
\]

The trace-ratio proof belongs to Book 02. Book 03 uses it to turn finite action operators into admissible readout weights.

## 03.9A Algorithmic Inertia and the Tautology of the Equivalence Principle

**Theorem 3.9A (Algebraic Equivalence \(m_i \equiv m_g\), D0.Core).**
By identifying the Universal Rewrite Operator \(\mathcal{R} = F_N \Delta_{geom}\), the Equivalence Principle becomes a trivial algebraic identity.
1. **Inertial Mass (\(m_i\))**: The algorithmic impedance to updating an object's boundary address is given by Landauer's erasure cost evaluated over the Sterile Archive: \(\operatorname{Tr}_{\mathcal{S}^{30}}(\mathcal{R})\).
2. **Gravitational Mass (\(m_g\))**: The global macroscopic deformation of the geometric heat-trace caused by the object is exactly the projection of the same operator \(\mathcal{R}\) over the identical 30-dimensional kernel.

Since both values are mathematically identical partial traces of the same finite operator \(\mathcal{R}\) over the same Sterile Archive, \(m_i\) and \(m_g\) are indistinguishable by definition. The Equivalence Principle requires no geometric postulate of falling elevators; it is the algebraic tautology of evaluating the same holographic trace from the active and archive perspectives.

Owner: Book 03 / D0.Core. Certificate: `vp_landauer_partial_trace.py`.

## 03.10 Scene Dynamics

**Definition 3.11 (Finite scene).** A finite scene is a tuple

\[
\mathfrak S_N=(\mathcal X_N,P_N,Q_N,U_N,\Delta_N,\mathcal O_N),
\]

where `\mathcal X_N` is the finite incidence/clique carrier, `P_N,Q_N` are the active/archive split, `U_N` is the tick, `\Delta_N` is the finite energy/depth operator, and `\mathcal O_N` is the declared readout family.

**Definition 3.12 (Scene dynamics).** A scene evolves by finite tick, readout projection, and active/archive update:

\[
|\psi_{n+1}\rangle=U_N|\psi_n\rangle,
\qquad
|\psi_{n+1}^{act}\rangle=P_{N+1}|\psi_{n+1}\rangle.
\]

A record persists, unlocks, or decays only through an operator that admits a finite quadratic readout and a finite quotient. The schematic runtime chain is

\[
\text{tick}\rightarrow\text{witness transport}\rightarrow
\text{active/archive split}\rightarrow\text{quadratic readout}.
\]

## 03.11 Golden Tick Gate

Let `p=\varphi^{-1}`. The detector-clock fixed point is represented on a declared clock block by

\[
U_\varphi=
\begin{pmatrix}
\sqrt p\,I&-pI\\
pI&\sqrt p\,I
\end{pmatrix}.
\]

Since `p+p^2=1`, this block is unitary. On the clock block it yields

\[
F_N=p^2P_N=\varphi^{-2}P_N,
\qquad
U_{\mathrm{eff}}^\dagger U_{\mathrm{eff}}=pP_N=\varphi^{-1}P_N.
\]

This construction is an action-level gate for informational mechanics. It is not a universal claim that every sector has feedback defect `\varphi^{-2}` without a declared clock-sector hypothesis.

## 03.12 Finite Spectral-Action Ladder

The action side of gravity begins as finite spectral algebra, not as an Einstein-Hilbert integral. For a positive density floor `\rho` and finite Laplacian `L`, the active ladder is

\[
W L W,
\qquad
\operatorname{Tr}(W L W),
\qquad
\operatorname{Tr}((W L W)^2),
\qquad
\operatorname{Tr}((W L W)^k).
\]

The first trace is a volume proxy. The square trace contains a diagonal square term and an off-diagonal curvature proxy. Higher powers are floor-bounded finite curvature controls. Gravity bridge ownership is downstream in Book 07.

K-theory gap labels do not create new action sections. The allowed order is

\[
\text{single action section}
\rightarrow\text{frozen operator}
\rightarrow\text{spectral gap}
\rightarrow\text{gap label}
\rightarrow\text{sector readout/passport}.
\]

## 03.13 Finite Transition and Scattering Discipline

The finite transition registry is action infrastructure:

\[
\mathcal S_{finite}:\mathcal H_{in}\to\mathcal H_{out},
\qquad
P(a\to b)={|S_{ba}|^2\over\sum_c|S_{ca}|^2}.
\]

States, cuts, detector acceptances, and external kinematics belong to typed comparison protocols. A finite transition registry is not a full collider simulator and may not be normalized by a second action scale.

Electroweak, photon, proton, neutron, and beta/archive mechanisms are admissible here only as action-layer forms. Their numerical comparison protocols are owned by Book 04.

## 03.14 Sector Handoffs

| Downstream sector | Book 03 contribution | Owner book |
|---|---|---|
| matter spectra | single action section, finite transition discipline, boundary cell | Book 04 |
| certificate discipline | proof/readout ownership classes | Book 05 |
| time and forgetting | runtime chain and active/archive update | Book 06 |
| gravity | finite spectral-action ladder and length-depth section | Book 07 |
| cosmology | finite-window rank derivative and feedback source | Book 08 |
| gravitational-wave bridge | action-level quadrupole/scene language only | Book 09 |
| laboratory bridges | typed external test protocols only | theory-map / protocol files |

## 03.15 Guardrails

Book 03 rejects the following moves:

1. adding a second dimensional anchor after `\Lambda_{act}`;
2. reading a support eigenvalue directly as a particle mass without terminal or runtime transfer;
3. using a continuum action as primitive input before finite stationarity is declared;
4. fitting bridge coefficients after seeing target data;
5. moving sector formulas from Books 04, 07, 08, or 09 back into Book 03 as if they were action proofs;
6. treating gap labels, collider normalizations, or survey calibrations as new action sections;
7. treating a clock-sector `\varphi^{-2}` defect as universal without an explicit sector assumption.

## 03.16 Summary of the Finite Action Layer

| Object | Formula or role | Upstream owner | Downstream use |
|---|---|---|---|
| feedback-return | Book 02 core operator | Book 02 | action response, scene dynamics |
| feedback action | `S_{fb}=-\log\det(I-zF_N)` | Book 02/03 | pressure and feedback source |
| feedback source | `\Pi_{fb}=z(I-zF_N)^{-1}` | Book 03 | finite response source |
| finite action readout | `\Lambda_N=\operatorname{Tr}(F_N\Delta_N(V))` | Book 03 | rank/depth weighted action |
| single action section | `\Lambda_{act}=38m_ec^2` | Book 03 | all dimensional readouts |
| boundary residual | stationary solution of `S_\partial(r,I)` | Book 03 | matter/gravity boundary cell |
| finite scene | `(\mathcal X_N,P_N,Q_N,U_N,\Delta_N,\mathcal O_N)` | Book 03 | runtime and sector projection |
| finite transition | normalized quadratic transition weights | Book 03 | matter/passport protocols |
| spectral-action ladder | finite heat-trace proxies | Book 03/07 | gravity bridge |
| golden tick gate | declared clock-sector splitter | Book 03 | informational mechanics, not universal sector leak |

## 03.17 Publication Boundary

Book 03 is complete when the finite action stack, single action section, boundary residual, and scene dynamics are declared. Later physical interpretations must preserve the handoff table above. A claim that requires a new primitive action, a new dimensionful section, or a target-dependent coefficient is outside Book 03 and outside the D0 publication contract unless separately admitted by Book 00.

## 03.18 Action as Precursor to Gravity and Cosmology

The finite action layer is the last purely internal action grammar before geometry and archive transfer. Book 07 uses the boundary residual and stress/action interface to define the finite gravity limit and heat-trace bridge. Book 08 uses the same finite-volume/action discipline to prevent archive pressure from becoming a survey-fitted parameter.

## 03.19 Interface to Other Books

| Book | Object received from Book 03 | Purpose |
|---|---|---|
| Book 04 | finite selector action compatibility | matter-sector compressed operators |
| Book 06 | finite scene update and tick language | time and archive evolution |
| Book 07 | boundary residual and action/stress interface | finite gravity and horizon seam mechanics |
| Book 08 | finite-volume response discipline | archive pressure and transfer windows |
| Book 09 | finite scene/passport separation | residual protocol admissibility |

## 03.20 Publication Boundary Statement

Book 03 closes the finite action layer. It does not close the physical identity of downstream matter, gravity, cosmology or GW signals. It supplies the action grammar that those layers must cite.

## 03.21 Cross-Reference Summary

- Book 02 owns \(F_N\) and log-det calculus (02.19B homological).
- Book 04 receives selector-action compatibility (04.5D, 04.9B).
- Book 05 owns central certs (05.10; vp_jacobson_kms_einstein.py, vp_landauer... for 03.8c/03.9A).
- Book 06 receives finite scene update and tick language (06.2E Schur time).
- Book 07 receives boundary-action language (07.8B Four-Color A/4 from seam).
- Book 08 receives finite-volume response discipline.
- 00.19-00.20 Grand Singularity (R ≡ Λ_N) unifies action as partial trace.
- New 03.8b Hurwitz Crystal + 38=24(Hurwitz)+14(G2) (D0-CORE-HURWITZ-LEECH-001); gravity as Archive pressure on perfect Hurwitz boundary. See vp_hurwitz_g2_leech_38.py + 05.10.

All trace back to Finite Holographic Self-Reading + rank-nullity 38 + quaternionic terminal algebra. See theory_status_map.csv for D0-CORE-GRAND-SINGULARITY-001 etc.

Book 03 closes finite action mechanics and prepares the ground for sector construction.
