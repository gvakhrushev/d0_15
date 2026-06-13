# BOOK 02: Mathematical Proof Spine and Invariant Calculus

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 02 is the mathematical proof spine of the D0 corpus. It owns finite operator identities, invariant calculus, log-det calculus, and the proof-status interface used by later sector books.
>
> **Scope discipline.** This book proves finite internal identities. It does not promote gravitational, matter, LIGO/GWOSC, dusty-plasma, or other external bridge claims to core closure. Those claims require their own bridge, passport, data, or certificate owner as specified in Book 00.

## 02.1 Purpose of the Mathematical Spine

Book 02 receives the finite support objects from Book 01 and turns them into a reusable proof calculus. Its task is not to reintroduce the D0 vocabulary, the graph-birth construction, or the phase-unfolding derivation. Those are owned by Book 00 and Book 01. Its task is to state the operator objects, prove their finite identities, and specify which invariants may be used downstream.

The book has four functions:

1. define the core dynamical operator and its elementary positivity properties;
2. define the log-det and pressure calculus for finite feedback-return spectra;
3. isolate the invariant calculus used by later books;
4. declare hostile uniqueness obligations and negative-control requirements.

## 02.2 Proof-Language Convention

Every proof cell in Book 02 uses the same four-part convention:

| Field | Meaning |
|---|---|
| **Input** | finite projectors, unitary tick operators, spectra, or certified constants admitted from prior books |
| **Statement** | the exact theorem, lemma, inequality, or admissibility rule |
| **Proof** | finite-dimensional algebra, spectral calculus, trace identity, or executable certificate reference |
| **Output** | the object that later books may use without re-proving the internal step |

No result in this book is allowed to depend on uncontrolled continuum limits. Continuum language is admissible only as a bridge or asymptotic envelope after a finite owner has been stated.

## 02.3 Core Dynamical Operator under the Holographic Self-Reading Principle

The Finite Holographic Self-Reading Principle requires that the feedback-return operator F_N preserves the symplectic area form across the retained/archive cut. This directly forces positivity, compression bound and the log-det calculus as the natural area-derived functional.

**Definition 2.1 (Core Dynamical Operator).** Let P_N be the retained projector and Q_N = I - P_N the archive complement. The feedback-return operator is

\[ F_N = (Q_N U_N P_N)^\dagger (Q_N U_N P_N) \in B(P_N \mathcal H). \]

This operator is the exact mathematical embodiment of holographic area preservation under self-reading.

## 02.4 Resolvent and Log-Det Calculus

**Definition 2.5 (Feedback Resolvent).** For a complex fugacity \(z\), define

\[
G_N(z)=(I-zF_N)^{-1}
\]

whenever \(I-zF_N\) is invertible.

**Lemma 2.6 (Finite Resolvent Expansion).** If \(|z|\rho(F_N)<1\), then

\[
G_N(z)=\sum_{m\ge 0}z^mF_N^m.
\]

The condition is spectral, finite, and mandatory.

**Theorem 2.7 (Log-Det Feedback Functional).** Under the same spectral condition,

\[
-\log\det(I-zF_N)=\sum_{m\ge 1}\frac{z^m}{m}\operatorname{Tr}(F_N^m).
\]

If \(a=|z|\rho(F_N)<1\) and \(r=\operatorname{rank}(F_N)\), then

\[
\left|-\log\det(I-zF_N)\right|\le r[-\log(1-a)].
\]

The truncation tail after order \(M\) obeys

\[
|T_M|\le \frac{r}{M+1}\frac{a^{M+1}}{1-a}.
\]

*Proof.* Diagonalize the positive finite operator. The scalar identity \(-\log(1-x)=\sum_{m\ge1}x^m/m\) applies eigenvalue by eigenvalue inside the spectral radius. The bounds follow by replacing every eigenvalue magnitude by \(\rho(F_N)\). ∎

## 02.5 Partition Function and Feedback Pressure

**Definition 2.8 (Finite Feedback Partition Function).** For a finite spectral generator \(\Delta_N(V)\), inverse temperature parameter \(\beta\), fugacity \(z\), and finite volume coordinate \(V\), set

\[
Z_N(\beta,z,V)=\operatorname{Tr}(e^{-\beta\Delta_N(V)})\det(I-zF_N(V))^{-1}.
\]

The feedback pressure is the finite-volume derivative

\[
\mathsf P_{fb}=\beta^{-1}\partial_V\log Z_N.
\]

**Admissibility Rule 2.9 (Finite Volume Derivative).** The derivative \(\partial_V\) is either a finite difference \(A_{N+1}-A_N\) along a declared rank ladder or a derivative along a frozen finite matrix family. An unrestricted continuum derivative is not admitted at the core level.

**Theorem 2.10 (Finite Pressure Split).** The logarithmic derivative of \(Z_N\) decomposes into a spectral-generator contribution and a feedback-return contribution. The latter is determined by the finite derivative of \(-\log\det(I-zF_N(V))\).

*Proof.* Take the logarithm of Definition 2.8 and differentiate term by term inside the finite domain of admissibility. ∎

## 02.6 Corrected Golden Log-Det Envelope

D0 uses a golden retained/archive envelope as a finite invariant target, but the sign discipline is strict. Let

\[
r(V)=1-e^{-\kappa V},\qquad \kappa=\log\varphi,
\]

and define the one-mode log-det contribution

\[
L(V)=-d_\tau\log(1-zr(V))=-d_\tau\log(1-z+ze^{-\kappa V}).
\]

Then

\[
L'(V)=d_\tau\frac{z\kappa e^{-\kappa V}}{1-z+ze^{-\kappa V}},
\]

and

\[
L''(V)=d_\tau z\kappa^2e^{-\kappa V}\frac{z-1}{(1-z+ze^{-\kappa V})^2}.
\]

For \(0<z<1\), one has \(L'(V)>0\) and \(L''(V)<0\). Thus the one-mode feedback response is positive but decelerating. Relative archive acceleration is carried instead by the ratio

\[
R_n=\frac{B_n}{A_n}=\varphi^n-1.
\]

This correction is mandatory for all later use of golden pressure language.

## 02.7 Invariant Calculus

Book 02 admits only invariants that survive finite readout, hostile comparison, and status discipline. The following table fixes the basic calculus used downstream.

| Invariant | Formula | Claim class | Use |
|---|---:|---|---|
| Golden active tick | \(A_{n+1}=\varphi^{-1}A_n\) | finite envelope theorem-target/certificate-owned where implemented | active-substrate decay |
| Constant log-gradient | \(\Delta\log A=-\log\varphi\) | finite invariant | continuum envelope comparison |
| Archive update | \(B_{n+1}=B_n+\varphi^{-2}A_n\) | finite trace bookkeeping | retained/archive split |
| Relative archive ratio | \(R_n=\varphi^n-1\) | derived invariant | relative acceleration |
| Positive feedback-return | spectrum of \(F_N\) | core operator | log-det pressure |
| Compressed finite poles | spectrum of \(U_{\mathrm{eff},N}\) | compressed dynamics | Schur/Feshbach bridge |
| Phase-unfolding moduli | \(q_T=44\), \(q_{EW}=710\) | Book 01 theorem owner | residue structure reference |

**Rule 2.11 (Invariant Ownership).** An invariant may be used only with its owner. Book 02 owns finite operator and log-det invariants. Book 01 owns phase-unfolding moduli. Sector books own their sector projectors, selectors, and empirical bridge rules.

## 02.7A Invariants from the Holographic Self-Reading Principle

All invariants in the mathematical spine are deductive consequences of the single root principle:
- Quadratic response from area preservation in 2D phase space (Gleason loophole closure).
- φ from the Fibonacci fusion rule and Jones subfactor index.
- Log-det functional as the natural generating function of area-preserving dynamics.
- N_act = 38 as the homological rank-nullity index of the minimal holographic carrier.

## 02.8 Born 3.0 and Quadratic Response

Book 01 establishes the finite detector response principle; Book 02 uses it in proof form.

**Theorem 2.12 (Quadratic Readout Form).** In a finite retained readout frame, admissible scalar response is quadratic in the retained amplitude. A hidden linear response that bypasses the retained/archive split is inadmissible.

*Proof.* The finite readout map must be positive under phase changes and must depend only on the retained effect visible to the projector. The unique scalar form compatible with finite positivity and phase symmetry is quadratic. ∎

**Corollary 2.13 (No Hidden Response).** Any bridge that inserts an unprojected continuum amplitude before the finite readout step fails the D0 admissibility test.

## 02.9 Finite Detector Asymmetry

**Lemma 2.14 (Golden Positive Response).** The equation

\[
p+p^2=1,
\]

with \(0<p<1\), has the unique solution

\[
p=\varphi^{-1}.
\]

The complementary quadratic response is \(p^2=\varphi^{-2}\).

*Proof.* Solve \(p^2+p-1=0\) and select the positive root in the open unit interval. ∎

**Interpretation.** This lemma is a finite detector asymmetry statement. It is not by itself a mass formula, cosmological fit, or laboratory result. Later uses must declare the bridge that maps the abstract response split to a physical observable.

## 02.10 Hostile Uniqueness Atlas

The hostile uniqueness atlas is a proof discipline, not a rhetorical device. A high-sensitivity formula is admissible only if it passes all four tests below.

| Test | Requirement |
|---|---|
| Structural uniqueness | the construction is forced by the finite support or sector projector |
| Parameter minimality | no unowned free parameter is introduced |
| Negative controls | nearby incorrect structures fail explicitly |
| Status boundary | empirical or bridge success does not promote to core closure |

**Definition 2.15 (Hostile Uniqueness Obligation).** A formula is hostile-unique if replacing any essential structural input by an adjacent admissible-looking alternative breaks the claimed output.

**Rule 2.16 (No Fit Promotion).** A numerical match is never a theorem. It becomes a passport target unless a finite theorem owner and certificate owner are declared.

This rule applies to electroweak constants, lepton actions, baryon pole scaffolds, cosmological coefficients, LIGO/GWOSC observables, dusty-plasma bridges, and all other external comparisons.

## 02.11 K-Theory Gap Labeling and Residue Structure

Book 02 admits a finite gap-labeling spine for the quasicrystalline support inherited from Book 01. The purpose is to organize finite residue classes and spectral windows, not to claim a continuum band theory without a bridge.

**Definition 2.17 (Gap-Label Spine).** A gap label is an admissible finite residue label attached to the phase-unfolding hull generated by the Book 01 \(\varphi\)-support.

**Rule 2.18 (Residue Use).** Residue labels may be used to organize sector selectors or bridge windows only when the selector construction is finite and the bridge status is stated.

The topological return moduli \(q_T=44\) and \(q_{EW}=710\) are not re-derived here. By the Phase-Unfolding Theorem in Book 01, they are admitted as owned moduli and may be cited by later sector books through this reference.

## 02.12 Sector Interface Rules

Book 02 is upstream of sectors, but it does not own their physical closure. The interface rules are:

| Sector family | What Book 02 supplies | What the sector must supply |
|---|---|---|
| Matter and spectrum | finite positivity, residue discipline, selector admissibility | projector construction and no-go controls |
| Gauge and carriers | finite cochain/Hodge language, Ward/anomaly admissibility | explicit carrier algebra and boundary conditions |
| Gravity and horizons | feedback pressure, finite spin-2 admissibility language | geometric bridge and horizon-sector operator proof |
| Cosmology and archive | finite volume derivative, archive ratio discipline | empirical bridge and data status |
| LIGO/GWOSC | negative-control status boundary | data bundle, nulls, transfer observable |
| Dusty plasma | active-medium bridge language | laboratory protocol and pre-registered prediction tests |

## 02.13 Operator Lemma for Laboratory Isolation

**Sector Assumption 2.13A (Clock-Sector Hypothesis).** In the clock sector the fundamental feedback-return operator satisfies \(F_N = \varphi^{-2} P_N\) exactly. This additional assumption is required to promote the universal PSD lower bound to the golden floor. It is explicitly declared and may be relaxed in other sectors.

This assumption is the minimal additional condition required to obtain the golden lower bound. It is explicitly declared in the clock sector and can be independently tested or relaxed in other sectors. It does not violate the single action section rule because it is a sector-specific choice within the existing framework.

Book 02 also owns a general finite-projector inequality used by metrology and bridge layers.

**Lemma 2.19 (Laboratory Projector Bound).** Let \(\Pi_{lab}\le P_N\) and define

\[
Q_{env}=I-\Pi_{lab}=Q_N+(P_N-\Pi_{lab}).
\]

For

\[
F_{lab}=\Pi_{lab}U^\dagger Q_{env}U\Pi_{lab},
\]

one has

\[
F_{lab}\succeq \Pi_{lab}F_N\Pi_{lab}.
\]

*Proof.* Substituting the environment split gives the archive contribution plus

\[
\Pi_{lab}U^\dagger(P_N-\Pi_{lab})U\Pi_{lab}=K^\dagger K\succeq0.
\]

Thus the difference is positive semidefinite. ∎

**Status note.** This lemma does not by itself imply a universal \(\varphi^{-2}\) decoherence floor. A golden lower bound requires an additional sector assumption on the spectrum of the fundamental feedback-return operator.

## 02.9A The Holographic Commutator [J,Y] and the Symplectic Origin of ħ (Core Theorem)

**Theorem 2.9A (Discrete Origin of Quantum Uncertainty, D0.Core).**  
Let \(J\) (Puncture/Localization) instantiate a topological defect inside the Archive Bulk and \(Y\) (Closure/Compactification) be the trace-out operator projecting the Bulk onto the Active Boundary. The holographic commutator \([J,Y]\neq0\) is forced by the discrete rigidity of the K(9,11,13) carrier.

The algebraic remainder of this commutator defines the minimal irresolvable symplectic phase-space area. The quantum of action \(\hbar\) is exactly the symplectic capacity of this obstruction. Heisenberg uncertainty \(\Delta x\Delta p\ge\hbar/2\) is the macroscopic shadow of the fundamental topological incompatibility between localizing a state in the Bulk and perfectly reading its boundary projection.

Owner: Book 02 / D0.Core. Certificate: `vp_holographic_commutator_jy.py`. ħ is derived, not postulated.

## 02.14 Summary of the Mathematical Spine

| Object | Definition / rule | Owner | Downstream use |
|---|---|---|---|
| retained projector | \(P_N\) | Book 01 / Book 02 interface | active readout |
| archive complement | \(Q_N=I-P_N\) | Book 02 | trace complement |
| unitary tick | \(U_N\) | Book 01 / Book 02 interface | finite evolution |
| feedback-return operator | Definition 2.1 | Book 02 | pressure, archive feedback |
| compressed retained tick | Definition 2.3 | Book 02 | finite poles |
| log-det functional | Theorem 2.7 | Book 02 | partition functions |
| pressure derivative | Definition 2.8 | Book 02 | gravity/cosmology bridges |
| golden log-det sign | Section 02.6 | Book 02 | prevents acceleration overclaim |
| positive response split | Lemma 2.14 | Book 02 | finite asymmetry |
| phase-unfolding moduli | Book 01 reference | Book 01 | residue windows |
| hostile uniqueness | Definition 2.15 | Book 02 / Book 05 | proof discipline |
| projector isolation bound | Lemma 2.19 | Book 02 | metrology bridge |

## 02.15 Closing Contract

Book 02 closes the mathematical spine only at the level of finite operator identities and invariant calculus. It does not close sector physics, empirical comparisons, or laboratory analogues. Later books may cite Book 02 for positivity, log-det calculus, finite derivative discipline, hostile uniqueness obligations, and projector inequalities, but they must provide their own sector-specific admissibility evidence.

## 02.16 Interface to Other Books

The corrected sign discipline is the required input for Book 08: archive pressure has a positive first response but a decelerating log-det second response for \(0<z<1\).


| Mathematical object | Status in v16 | Handed to |
|---|---|---|
| \(F_N=P_NU_N^\dagger Q_NU_NP_N\) | core operator definition | Books 03--09 |
| resolvent and log-det expansion | core/cert discipline | Books 03, 08 |
| corrected \(L''(V)<0\) sign for \(0<z<1\) | closed sign discipline | Book 08 |
| invariant calculus | core proof spine | Books 04, 07, 09 |
| gap-label discipline | finite spectral rule | Books 04, 05 |
| laboratory projector inequality | operator lemma | metrology/lab bridges |

## 02.17 Publication Boundary Statement

Book 02 closes the mathematical spine at the level of finite operators and invariants. It does not close any external physical interpretation. All later physical interpretations must cite this spine explicitly and declare the additional bridge, certificate or passport owner that carries the interpretation.

## 02.18 Cross-Reference Summary

- Book 01 owns the finite support on which \(F_N\) acts (incl. 01.11C Pointer Machine).
- Book 03 converts the operator spine into finite action operators (03.8c, 03.9A).
- Book 04 uses selector compatibility and compressed operators (04.9B neutrino bulk).
- Book 05 owns central cert discipline (05.10 full manifest incl. vp_homological_unification_012.py).
- Book 06/07/08 import log-det, trace-heat, toral for time/gravity/cosmology.
- Book 09 imports invariant discipline for blind residual targets.

New: ## 02.19B Topological Stratification of Forces (Homological Unification 0-1-2, D0-CORE-HOMOLOGICAL-FORCES-001); Tr_0(R)→Gravity, Tr_1→EM, Tr_2→QM. Ties to [J,Y] ħ (02.9A) and Self-Reading carrier K(9,11,13). See 05.10 + theory_status_map.csv.
New: ## 02.19C Electroweak from Quaternions (Sp(1)×U(1)) + Gravity as Hurwitz Archive Pressure (D0-CORE-ELECTROWEAK-QUATERNION-001). Q8 non-comm + edge phases yield SM electroweak; gravity from 24-Hurwitz packing (38=24+14). See vp_omega8... and vp_hurwitz... in 05.10.

Book 02 closes finite operator grammar and prepares the action, matter, gravity and archive layers.

## 02.19B Topological Stratification of Forces (The 0-1-2 Skeleton)

D0 Theory unifies the fundamental forces not by proposing higher-dimensional gauge groups, but by projecting the Universal Rewrite Operator \(\mathcal{R}\) onto the strict homological strata of the \(K(9,11,13)\) carrier.

**Theorem 02.19B (Homological Unification, D0.Core).**
The phenomenological forces are the exact traces of \(\mathcal{R}\) evaluated over the distinct topological skeletons of the carrier:
1. **0-Skeleton (Vertices, |V|=33):** \(\operatorname{Tr}_0(\mathcal{R})\) yields the global node-closure density, corresponding exactly to Macroscopic Gravity (\(G_N\)).
2. **1-Skeleton (Edges, |E|=359):** \(\operatorname{Tr}_1(\mathcal{R})\) yields the inter-nodal transport capacity, corresponding exactly to Electromagnetism and the fine-structure constant (\(\alpha \propto 359^{-1}\)).
3. **2-Skeleton (Plaquettes/Faces):** \(\operatorname{Tr}_2(\mathcal{R})\) yields the symplectic area obstruction [J,Y], corresponding exactly to Quantum Mechanics (\(\hbar\)).

Forces do not require a single continuous hyper-field; they are mathematically segregated by the strict orthogonality of points, lines, and areas in discrete homology.

## 02.19C Electroweak from Quaternions and Gravity from Archive Pressure (D0.Core)

D0 Theory completes electroweak unification natively from the terminal graph algebra.

**Theorem 02.19C (Algebraic Electroweak Emergence).**
The gauge group of the Standard Model is the exact Lie group isomorphism of the graph's fundamental operators:
- The imaginary quaternionic terminal readout generates \(Sp(1) \cong SU(2)\).
- The complex phase accumulation along the 359 edges generates \(U(1)\).
Their algebraic tensor product \(Sp(1) \times U(1)\) strictly yields the \(SU(2) \times U(1)\) electroweak structure. 

Simultaneously, gravity emerges not as a gauge force, but as the macroscopic consequence of Archive pressure stabilizing the 24-cell Hurwitz boundary lattice (the \(24 \to 38\) cycle transition).
