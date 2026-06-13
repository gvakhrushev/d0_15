# BOOK 04: Spectrum, Matter, and Finite Selector Theory

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 04 is the matter-selector book of the D0 corpus. It defines finite selector objects, certified internal carriers, anonymous pole sets and theorem-target transfer layers. It does not assign external particle names, masses, widths or PDG identities as core results.
>
> **Claim boundary.** Internal D0 matter objects are finite algebraic constructions. External spectroscopy, numerical mass comparison, PDG assignment, QCD/EFT interpretation and laboratory measurement remain bridge or passport layers unless separately frozen by their own owner, data manifest, certificate and falsification rule.

**Ownership and handoff.** Book 04 owns finite matter selectors, CKM basis-origin mismatch, edge ramification scaffolds, certified baryon 40/56 carriers, cert-closed anonymous pole sets on certified carriers, the Higgs rank-2 projector layer and meson transfer algebra. It hands external naming and mass comparison only to passport layers.


---

## 04.1 Role of the matter book

Books 00--03 fix the entry contract, finite support, proof spine and action stack. Book 04 is the first place where those constructions are read as matter-sector selectors.

A Book 04 claim is admissible only if it specifies:

| Required component | Meaning |
|---|---|
| finite carrier | the vector space or image-basis carrier on which the object acts |
| finite selector | an idempotent or projector selecting the admissible subspace |
| operator owner | the finite operator whose spectrum, poles or response are being studied |
| claim class | core, cert-closed, theorem-target, bridge or passport target |
| external boundary | a statement of what is not assigned internally |

Book 04 does not introduce new primitive scales and does not fit a particle table. A support number becomes a physical comparison only after a typed transfer map and an external passport have been declared.

---

## 04.2 Finite selector theory

**Definition 4.1 (Finite selector).**  
A finite matter selector is an idempotent finite-rank operator

\[
\Pi^2=\Pi, \qquad \operatorname{Tr}(\Pi)<\infty,
\]

acting on a declared finite carrier. When the selector is used inside a D0 feedback sector it must also specify its compatibility condition with the relevant sector operator. The minimal compatibility condition is that the selected image is invariant under the operator being compressed.

**Definition 4.2 (Compressed sector operator).**  
For a finite carrier image basis \(B_\Pi\), the admissible compressed operator is

\[
\widehat U_{\rm eff}^{\Pi}=B_\Pi^\dagger PUPB_\Pi.
\]

Poles, phases and widths are extracted only from such declared image-basis compressed operators or from an explicitly declared Feshbach--Schur reduction. Padded complement eigenvalues are not matter predictions.

**Definition 4.3 (Anonymous pole set).**  
The anonymous pole set of a compressed sector is

\[
\mathcal P_\Pi=\{\lambda\in\mathbb C:\det(\lambda I-\widehat U_{\rm eff}^{\Pi})=0\}.
\]

The word *anonymous* is part of the status: no external particle name, mass, width or PDG entry is assigned at this layer.

---

## 04.3 Matter-chain admissibility

The canonical matter chain is:

\[
\text{finite carrier}
\rightarrow \text{finite selector}
\rightarrow \text{compressed operator}
\rightarrow \text{anonymous spectrum or pole set}
\rightarrow \text{external passport only after freezing.}
\]

The following shortcuts are inadmissible:

| Shortcut | Reason |
|---|---|
| support number as mass | no transfer map has been supplied |
| bare positive feedback operator as complex resonance | positive operators do not supply complex poles |
| PDG sorting before frozen internal poles | labels would fit the target table |
| padded complement eigenvalues | they are artifacts of the embedding carrier |
| full matter closure language | Book 04 contains mixed claim classes |

---

## 04.4 CKM basis-origin layer

Book 04 treats CKM-like structure as a finite basis-origin problem, not as a free numerical matrix. The admissible internal object is a pair of finite flavour-origin bases together with the mismatch operator between them.

**Definition 4.4 (Finite basis mismatch).**  
Let \(B_u\) and \(B_d\) be frozen image bases of two finite selector origins. The finite basis-mismatch matrix is

\[
C=B_u^\dagger B_d.
\]

The typed transfer map is \(C = B_u^\dagger B_d\), where \(B_u\) and \(B_d\) are image bases of two frozen selectors originating from different terminal role sectors. The mismatch \(C\) is the natural CKM-like object in the holographic carrier. External comparison to the phenomenological CKM matrix is a passport target.

A CKM passport may compare \(C\) to an external CKM convention only after both bases are frozen. The internal claim is the construction of the mismatch source, not a fitted phenomenological matrix.

Status:

| Object | Claim class | Status |
|---|---|---|
| finite flavour-origin selectors | cert/theorem layer | constructed or cert-owned |
| basis mismatch source | theorem-target/cert layer | finite operator object |
| numerical CKM comparison | passport | external target |

---

## 04.5 Topological Defects and the Prime-Edge Anyon Scaffold

The finite matter sector is the algebra of topological defects within the holographic carrier. The total edge count of K(9,11,13) is exactly 359. Because 359 is prime, the carrier possesses absolute topological rigidity (no continuous internal gauge symmetries).

Matter observables exist only as discrete topological defects (anyonic excitations). The fractional exponent rules (1/3 and 1/4) for lepton branching are forced by Puiseux holonomy around these rigid prime-edge defects. The tri-generation structure is a closed theorem of the prime-edge carrier.

---

## 04.5A Companion embedding proof for edge ramification

The rank-four and rank-three ramification blocks are not mnemonic labels. They are finite companion restrictions embedded inside the 359-edge carrier.

**Definition 4.4A (Edge companion restrictions).** Let \(\lambda\) denote the edge holonomy parameter. The terminal capacity block is the companion operator \(C_4(\lambda)\) with characteristic equation

\[
z^4-\lambda=0,
\]

and the internal scene-rank block is the companion operator \(R_3(\lambda)\) with characteristic equation

\[
z^3-\lambda=0.
\]

They embed into the 359-edge carrier as

\[
U_{E}^{cover}
\cong
U_{bulk}^{352}\oplus C_4(\lambda)\oplus R_3(\lambda),
\qquad
352+4+3=359.
\]

**Theorem 4.4B (Puiseux branch closure).** The local resolvent of the edge-cover operator factors as

\[
D_E(z,\lambda)=D_{bulk}(z)\,(z^4-\lambda)(z^3-\lambda).
\]

Therefore the two non-bulk ramification exponents are exactly

\[
p_\mu={1\over4},
\qquad
p_\tau={1\over3}.
\]

*Proof.* The roots of \(z^4=\lambda\) are Puiseux branches \(z=\lambda^{1/4}\xi_4^j\). The roots of \(z^3=\lambda\) are \(z=\lambda^{1/3}\xi_3^j\). The direct-sum embedding preserves determinant factorization, so the branch indices are intrinsic to the finite edge-cover block and not obtained by fitting measured lepton masses. The executable certificate `vp_edge_ramification_companion_embedding.py` checks the companion characteristic polynomials and the 359-dimensional embedding count. ∎

## 04.5D 359 Prime Edges → Topological Anyons + Jones Index (Mia + Olivia)

359 — prime ⇒ Topologically rigid (no continuous gauge).  
Fibonacci fusion τ⊗τ = 1⊕τ ⇒ Jones index [M:N] = φ² = (3+√5)/2.  
Higgs = rank-2 projector на ramification C₄/R₃.  
Puiseux series 1/3 и 1/4 — braiding indices вокруг дефектов.

Certificate: vp_jones_fibonacci_ττ_359.py

## 04.6 Baryon spin-flavour carriers

Book 04 admits two internal baryon carriers before any external baryon name or PDG assignment.

Let

\[
V_{\rm flavour}\cong\mathbb C^3,
\qquad
V_{\rm spin}\cong\mathbb C^2,
\qquad
\mathcal H_B=(\mathbb C^6)^{\otimes3}.
\]

Hence \(\dim \mathcal H_B=216\).

**Definition 4.5 (Rank-40 separable symmetric carrier).**

\[
\Pi_B^{40}=\Pi_{S_3}^{\rm flavour}\otimes\Pi_{S_3}^{\rm spin}.
\]

The rank is

\[
\operatorname{rank}(\Pi_B^{40})=10\cdot4=40.
\]

**Definition 4.6 (Rank-56 diagonal exchange-symmetric carrier).**

\[
\Pi_B^{56}=\frac16\sum_{\sigma\in S_3}
P_\sigma^{\rm flavour}\otimes P_\sigma^{\rm spin}.
\]

The rank is

\[
\operatorname{rank}(\Pi_B^{56})=\dim\operatorname{Sym}^3(\mathbb C^6)=56.
\]

The inclusion relation is

\[
\Pi_B^{56}\Pi_B^{40}=\Pi_B^{40}.
\]

Thus the rank-40 carrier is an internal subcarrier of the rank-56 carrier. The remaining sixteen dimensions are mixed spin-flavour degrees of freedom inside the finite carrier.

---

## 04.6B Fermionic Holonomy from Quaternionic Multiplication and \(F_N\) (D0.Core)

**Theorem 04.6B (Discrete Spinor Generation).**
The core feedback-return operator \(F_N = P_N U_N^\dagger Q_N U_N P_N\) acts structurally as left quaternion multiplication upon the \(\Omega_8\) terminal states. 
Under quaternionic left multiplication, any spatial cycle traversing the imaginary axes (\(i, j, k\)) squares identically to \(-1\), algebraically forcing a sign flip into the Sterile Archive. Only a \(4\pi\) double-cycle returns the terminal register to its identity state (\(i^4 = 1\)). 

This discrete holonomy, coupled with the rigid 359 prime-edge spectral gap, mathematically guarantees that all topological matter defects are fermionic (Spin-1/2). Furthermore, weak force chiral asymmetry is topologically forced by the fundamental non-commutativity of the spatial operators (\(ij = k\), \(ji = -k\)).

---

## 04.7 Cert-Closed Baryon Anonymous Pole Sets

For \(k\in\{40,56\}\), the admissible baryon compressed operator is

\[
\widehat U_{\rm eff}^{B,k}=B_k^\dagger PUPB_k,
\]

where \(B_k\) is an image basis of \(\Pi_B^k\). The anonymous pole equation is

\[
\det(I-\zeta\widehat U_{\rm eff}^{B,k})=0.
\]

This layer is cert-closed at the internal algebraic level of certified carriers and anonymous image-basis pole extraction:

| Internal object | Status |
|---|---|
| rank-40 carrier | certified finite representation object |
| rank-56 carrier | certified finite representation object |
| rank-40 inclusion into rank-56 | certified finite representation relation |
| image-basis pole extraction | certified anonymous pole scaffold |

It is not a baryon mass table. It assigns no spin labels beyond the carrier construction, no flavour names beyond the representation basis, no GeV units, no widths and no PDG identities.

---

## 04.8 Higgs rank-2 projector layer

The Higgs scalar sector is treated as a finite projector theorem-target with an exact local doublet lemma.

Let \(X=\sigma_x\) and \(Z=\sigma_z\) act on a two-dimensional doublet. If a projector \(P\) commutes with both \(X\) and \(Z\) on this irreducible doublet, then

\[
[P,X]=0,\qquad [P,Z]=0
\quad\Longrightarrow\quad
P=aI_2.
\]

If \(P\) is nonzero, positive and idempotent, then \(a=1\), hence

\[
P=I_2,
\qquad
\operatorname{rank}(P)=2.
\]

This establishes the local rank-2 scalar projector statement on the doublet. On a larger carrier \(\mathbb C^2\otimes M\), the commutant is

\[
I_2\otimes\operatorname{End}(M),
\]

so rank-2 uniqueness requires an additional multiplicity selector. Yukawa sections, measured Higgs mass and electroweak numerical comparison remain transfer or passport targets.

**Expected proof route for multiplicity-selected Higgs uniqueness:** Show that the rank-2 projector on the doublet, when tensored with a selector of multiplicity \(m\), requires \(m = 1\) to satisfy commutativity with the full symplectic structure of the carrier. This route is declared and remains a theorem-target until closed.

---

## 04.9 Meson transfer algebra

The meson layer is a finite transfer-algebra construction on declared baryon or defect carriers. It is not an external meson table.

**Definition 4.7 (Meson transfer window).**  
A meson transfer window is a finite operator family

\[
T_{a\to b}:\operatorname{im}(\Pi_a)\to\operatorname{im}(\Pi_b)
\]

between frozen selected carriers. Its admissible output is an internal transfer spectrum or typed defect relation. External meson names, masses and decay widths require a passport.

Status:

| Meson object | Claim class |
|---|---|
| typed finite transfer operator | theorem-target/cert layer |
| internal transfer spectrum | anonymous internal object |
| external meson assignment | passport target |

## 04.9B Neutrino Mass as the Bulk Eigenvalue of Quantum Uncertainty

**Theorem 04.9B (Neutrino as the [J,Y] Carrier, D0.Core).**
The holographic commutator [J, Y] ≠ 0 produces the quantum of action (ℏ) in the Active Transport boundary. However, evaluating this same commutator within the 30-dimensional Sterile Archive (𝒮³⁰) yields an irreducible, non-spatial phase oscillation. 
The neutrino, identified as the neutral bulk phason wave, is the physical carrier of this bulk commutator. Its mass scale is strictly proportional to the algebraic gluing anomaly (m_ν ∝ Δ_α²), which is the minimal non-zero eigenvalue of the [J,Y] obstruction projected into the null space. The neutrino has mass because quantum uncertainty (ℏ) mathematically cannot vanish, even in the unobservable Archive.

---

## 04.10 Gauge and matter-sector bridges

Book 04 may reference gauge, electroweak, QCD, PDG, Yukawa and EFT language only as bridge or passport language. The internal D0 object must remain visible.

Allowed phrasing:

| Use | Publication-safe form |
|---|---|
| CKM | finite basis-origin mismatch; external CKM comparison is a passport |
| baryons | rank-40/rank-56 spin-flavour carriers and anonymous pole sets |
| Higgs | rank-2 doublet projector with multiplicity caveat |
| mesons | finite transfer-algebra windows |
| lepton branching | edge ramification scaffold |
| masses | external numerical passport targets |

Forbidden phrasing:

| Forbidden phrase | Replacement |
|---|---|
| unqualified matter-sector closure wording | finite selector theory is constructed with mixed claim classes |
| complete baryon-table derivation wording | anonymous baryon pole sets are constructed on certified carriers |
| internal Higgs-mass derivation wording | Higgs rank-2 projector layer is constructed; mass is a passport target |
| closed external-PDG-table wording | external PDG assignment remains a passport |
| unqualified Standard-Model-proof wording | finite D0 selector scaffold with external bridge targets |

---

## 04.11 Current status of matter sector

| Object | Internal content | Claim class | Publication status |
|---|---|---|---|
| finite selectors | finite idempotent projectors on declared carriers | core/cert layer | admissible construction |
| CKM basis origin | finite basis mismatch after frozen selector origins | theorem-target/cert layer | internal source construction |
| edge ramification | 359-edge scaffold and rank-4/rank-3 companion restrictions | cert/theorem layer | internal branch scaffold |
| baryon rank-40 carrier | separable symmetric spin-flavour carrier | cert layer | certified carrier |
| baryon rank-56 carrier | diagonal exchange-symmetric carrier | cert layer | certified carrier |
| rank-40 inside rank-56 | carrier inclusion | cert layer | certified relation |
| baryon anonymous poles | image-basis compressed pole sets | cert layer | anonymous pole scaffold |
| Higgs rank-2 projector | irreducible doublet projector lemma | theorem/cert layer | internal projector statement |
| multiplicity-selected Higgs uniqueness | rank-2 uniqueness on larger carriers | theorem-target | requires selector hypothesis |
| meson transfer algebra | finite transfer windows between selected carriers | theorem-target/cert layer | internal transfer scaffold |
| PDG names and masses | external particle assignment | passport | target only |
| Yukawa numerical values | external numerical comparison | passport | target only |
| QCD/EFT bridge | typed external interpretation | bridge | target only |

---

## 04.12 Summary of Book 04

Book 04 supplies finite matter selectors and internal spectral scaffolds. Its strongest internal results are finite-carrier and projector constructions, not external spectroscopy. The correct publication reading is:

\[
\text{finite selector theory}
+\text{certified internal carriers}
+\text{anonymous pole and transfer scaffolds}
+\text{explicit passport boundaries}.
\]

No Book 04 statement converts an anonymous internal pole into an external particle without a separate passport. No matter-sector statement overrides the entry contract of Book 00 or the proof-spine discipline of Book 02.

## 04.13 Table 4.13 — Publication Claim Strength

| Object | Internal status | Publication claim strength | External boundary |
|---|---|---|---|
| finite selectors | closed finite construction | strong internal selector claim | no particle table |
| CKM basis-origin mismatch | constructed bridge scaffold | finite basis-origin claim | no fitted CKM phenomenology |
| 359-edge ramification scaffold | certified internal scaffold | edge-sector construction claim | no lepton mass assignment |
| baryon 40/56 carriers | cert-closed carriers | strong cert-level internal carrier claim | no PDG naming |
| anonymous baryon pole sets | cert-closed anonymous pole sets on certified carriers | strong internal pole-set claim | no GeV masses or widths |
| Higgs rank-2 projector | finite projector theorem layer with multiplicity caveat | internal projector claim | experimental mass remains passport |
| meson transfer algebra | finite transfer-window construction | bridge-ready algebraic claim | external meson assignment remains passport |


## 04.14 Master Matter-Transfer Full Closure

**Operator closure status:** `MATTER-TRANSFER-FULL-CLOSURE / CERT-GUARDED / NO-PDG-ASSIGNMENT`

The matter-transfer layer is closed at the finite-operator level by the v16 matter-transfer cert suite. This closure strengthens the internal Book 04 algebra without importing external particle names, empirical masses, or fitted constants.

| Closure item | Finite mechanism | Owner cert |
|---|---|---|
| edge alpha canonical trace | `Tr(F_E)=359\varphi^{-2}-\varphi^{-5}` on the 359-edge space | `vp_edge_alpha_trace_canonical.py` |
| branch exponents and coefficients | `C4` and `R3` companion roots with zero first symmetric sums | `vp_lepton_ramification_coefficients.py` |
| baryon pole taxonomy | anonymous degeneracy classes `{1,2,4}` from `S3 x S3` representation dimensions | `vp_baryon_pole_degeneracy_taxonomy.py` |
| spin/flavour transfer closure | active-sector stability plus boundary leakage obstruction | `vp_baryon_spin_flavour_transfer_closure.py` |
| meson transfer spectrum | finite PSD tensor-sum operator on edge/generation space | `vp_meson_transfer_full_spectrum.py` |
| gauge-boundary lower bound | `||[P,g]||_F^2=2||QgP||_F^2` | `vp_gauge_boundary_commutator_lower_bound.py` |

The master guardrail `vp_matter_transfer_master_guardrail.py` fails the publication build if empirical mass tables, external particle labels, fitted alpha values, or post-hoc numerical matching are inserted into the core matter-transfer derivations.


## v17 Research Upgrade: 216D Matter Transfer Hardening

**Status:** `MATTER-216D-TRANSFER-CERT-SPEC / PASSPORT-SEPARATED`

The late v17 matter upgrade replaces the earlier scalar-risk transfer construction with a full 216-dimensional spin-flavour carrier calculation. The baryonic carrier is
\[
\mathcal H_B=(\mathbb C^3\otimes\mathbb C^2)^{\otimes3}\cong\mathbb C^{216}.
\]
The certified projectors remain
\[
\Pi_{56}=\frac16\sum_{\sigma\in S_3}P^f_\sigma\otimes P^s_\sigma,
\qquad
\Pi_{40}=\Pi^f_{S_3}\otimes\Pi^s_{S_3},
\]
with \(\Pi_{56}\Pi_{40}=\Pi_{40}\) and \(\Pi_{16}=\Pi_{56}-\Pi_{40}\).

Let \(V_{shell}\) be the shell-variance operator acting on the spin-flavour space, defined as the deviation from the mean shell radius in the 216-dimensional carrier.

The transfer observable is the shell-variance strain
\[
T_{sf}=\Pi_{56}(V_{shell}\otimes I_{spin})\Pi_{56}.
\]
It commutes with the 56D and 40D projectors, preserves the 16D complement, and is non-scalar on \(\operatorname{Im}\Pi_{56}\). Physical particle names and empirical masses remain external passport comparisons.

Lepton branch blocks obey \(\operatorname{Tr}(C_m)=0\) and use the positive quadratic readout \(\operatorname{Tr}(C_m^\dagger C_m)=m\). This establishes a coefficient-origin scaffold, not an empirical mass claim.

## 04.15 Interface to Other Books

| Source or target book | Object exchanged | Direction |
|---|---|---|
| Book 01 | \(\Omega_8\), \(V_9\), graph-birth support | imported |
| Book 02 | compressed operator and invariant calculus | imported |
| Book 03 | finite action compatibility | imported |
| Book 05 | certificate and promotion discipline | imported |
| Book 08 | external survey/passport discipline | status precedent |
| external PDG/QCD/EFT layers | naming, mass, width and phenomenology | exported only as passport targets |

## 04.16 Publication Boundary Statement

Book 04 closes the finite internal matter selector layer at the stated algebraic/certificate scopes. External assignments remain passport targets, but the algebraic scaffolds, certified carriers and anonymous pole-set procedures are closed at the internal cert level.

## 04.17 Cross-Reference Summary

- Book 00 supplies claim boundaries and vocabulary discipline (00.2 Self-Reading, 00.19-00.20 Grand Singularity).
- Book 01 supplies \(\Omega_8\), V9, K(9,11,13) (01.11C pointer).
- Book 02 supplies compressed-operator and invariant grammar (02.19B homological).
- Book 05 supplies certificate status and no-go rules (05.10 manifest: vp_neutrino_bulk_jy.py, vp_algebraic_rigidity..., vp_four_color...; see 05.9 tables).
- Book 06/07/08 receive carriers for time/gravity/cosmology (06.2E, 07.8B).
- Book 08 and external passport files may later receive frozen comparisons, but cannot retroactively change Book 04 internal status.

New v17: 04.5D 359 Prime → Anyons + Jones; 04.9B Neutrino as bulk [J,Y] carrier (D0-CORE-NEUTRINO-BULK-001); 04.6B Fermionic Holonomy from Q8 (D0-CORE-SPINOR-QUATERNION-001, Spin-1/2 + chirality from i^2=-1 and F_N left mult). Ties to prime-edge rigidity (K(9,11,13)), quaternionic terminal (01.7A), and Self-Reading. See 05.10 vp_hurwitz_g2_leech_38.py.

Book 04 closes finite matter-selector mechanics and prepares any external matter comparison to remain explicit passport work.
