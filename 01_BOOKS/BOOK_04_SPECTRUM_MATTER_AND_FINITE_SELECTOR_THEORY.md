<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 04 — Spectrum, Matter, and Finite Selector Theory

> Scope: Matter-sector selector laws, compressed poles, baryon/meson/Higgs/gauge-sector bridge discipline.
> Claim discipline: Particle names require finite operator owners and typed bridge/passport boundaries.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 04.0 Active matter sector law

Book 04 is a sector law, not a list of disconnected particle claims. A D0 matter candidate is a terminally projected near-critical feedback mode:

```text
F_N psi_j = r_j psi_j
|z r_j| approx 1
P_term psi_j = psi_j
R_N = D_N^dagger D_N
```

Naming a mode as electron, neutrino, meson, baryon, CKM or Higgs requires the finite operator owner and the bridge/passport boundary.

### Resonance law

Complex resonance data live in:

```text
U_eff = P_N U_N P_N
```

or:

```text
H_eff(E)=H_PP+H_PQ(E-H_QQ)^(-1)H_QP
```

If:

```text
U_eff psi = lambda psi
lambda = exp(-Gamma + i E)
```

then:

```text
E = arg(lambda)
Gamma = -log |lambda|
```

### Neutrino leakage sector and the mass scale from the gluing anomaly

The neutrino is the neutral-leakage (Ker-channel) mode. Its mass *scale* is not anchored externally; it is forced by the seam anomaly `Delta_alpha`, the irreducible residue between two independent canonizations of `alpha^{-1}` (topological capacity of channels vs. algebraic/geometric phase inside `Q(phi)`).

```text
Delta_alpha = |alpha^{-1}_top - alpha^{-1}_alg| ~ 4.15e-4
P_sterile := Theta(Delta_alpha^2)            # leading sterile-tunneling weight
m_nu / m_e ~ P_sterile ~ Delta_alpha^2
m_nu ~ m_e * Delta_alpha^2 ~ 0.088 eV        # one-mode / characteristic scale
```

Forcing — why the *square* [^b04-4]: the linear term in `Delta_alpha` is unobservable, because the sign of the seam error does not survive into probabilistic weights. So the leading observable scale is `Theta(Delta_alpha^2)`, not `Theta(Delta_alpha)`.

Mass-scale bridge [^b04-5]: reading mass as cycle density, the natural neutrino mass scale is `m_nu/m_e ~ Delta_alpha^2`. This is a BRIDGE scale-matching; CORE fixes only the dimensionless map `Delta_alpha -> P_sterile`. The `0.088 eV` figure is the single-mode characteristic scale [^b04-6]; the protocol mapping it to observed combinations (`m_beta`, `sum m_nu`) belongs in the falsification matrix, not here.

M1 failure mode [^b04-7]: `Delta_alpha` is the *mismatch* of two independently admissible canonizations. If `Delta_alpha = 0` it would mean a hidden identity rule between the two canonizations — an external "dictionary of correspondence" — which M1 forbids. So `Delta_alpha != 0` is forced: it is the inevitable trace of the irreducibility of the two descriptions, and it is precisely this nonzero residue that seeds the leakage (and hence a nonzero neutrino mass scale).

Status: `Delta_alpha` is CORE-measurable; the seam-alpha invariant `delta_alpha < eps2` is checked by an existing finite certificate, and the residual itself is held at CHK (not promoted to THE until `Delta_alpha` receives an analytic owner). The `m_nu ~ 0.088 eV` mass-scale step is a BRIDGE assignment, not a closed CORE theorem.

```text
[^b04-1]  # m_nu/m_e ~ Delta_alpha^2 mass-scale bridge has no vp_*.py owner; Delta_alpha analytic owner still open
D0.Matter.NeutrinoMassScaleFromGluingAnomaly
```

### Charge quantization is forced (not postulated)

In standard physics, charge quantization is either empirical or follows from compactness of U(1). In D0 it is a theorem of the scene graph, forced by M1.

```text
G = finite connected scene graph (edges, nodes)
U(1) phase = 1-cochain on edges
gauge transform = add an exact 1-form (gradient) to the 1-cochain
distinguishable classes = quotient by exact cochains = H^1(G, Z)
measurable charges = integer cohomology classes
=> topological charge is discrete (integer)
```

Forcing [^b04-8]: gauge-equivalent phase configurations are parametrized by `H^1(G, Z)`; the measurable invariants are exactly the integer cohomology classes, so charge is integer-valued. Charge is a counter of symmetry winding (group Z), not a tunable real.

M1 failure mode [^b04-9]: charge discreteness is a consequence of the discreteness of the scene's fundamental cycles (memory/holonomy). A *continuous* charge would require an external resolution parameter to fix its scale — an external catalog — which M1 forbids. So continuous charge is not a different admissible physics; it is structurally excluded.

```text
[^b04-2]  # H^1(G,Z) charge-quantization forcing has no vp_*.py yet
D0.Matter.ChargeQuantizationH1Forcing
```

### Integer projection forces the Lucas trace selector

Book 04 scales live in `Q(phi)`; every scale is a power `phi^k`, which is irrational. Interaction ("exchange of portions") requires a *whole* number of portions. The integer-projection problem [^b04-10]: how to extract an integer `N` from `phi^k` without an arbitrary `Round()` threshold — a `Round()` would import an external rounding catalog, forbidden by M1.

The unique catalog-free answer is the algebraic trace [^b04-11]:

```text
psi = -1/phi                         # algebraic conjugate of phi
L_k = phi^k + psi^k = Tr_{Q(phi)/Q}(phi^k)   # always an integer
```

Forcing argument: the trace is the integer projection *built into the algebra itself* — it needs no manual threshold, no external normalization. Any `Round()`-style projection imports a catalog and dies under M1. Hence the Lucas trace is the ONLY canonical integer projection of `phi^k` [^b04-12]. This uniqueness is the WHY the trace identity carries the physics, not just the identity itself.

Resonance spectrum after the base anchor:

```text
L_1 = 1   (trivial)
L_2 = 3   (first prime resonance)
L_3 = 4   (addressing anchor, occupied by the Base; not a resonance slot)
L_4 = 7
L_5 = 11
L_6 = 18  (composite 2x9, not prime)
=> first prime resonances after excluding the L_3=4 anchor: 3, 7, 11
```

This is the structural reason the denominators 3, 7, 11 appear in mixing angles and corrections while 5 and 13 do not. Larger primes (29, 47, ...) arise at larger `k` from the same trace operation — not ad hoc.

The signed Lucas *trace identity* `Tr(T^n) = (-1)^n L_n` is certified by existing finite certificates (the `L_2=3, L_3=-4, L_5=-11` layer diagnostic is among the checked data). What those certify is the identity; the *uniqueness-of-projection* forcing above is the matter-sector argument carried here.

```text
[^b04-3]  # uniqueness "trace is the ONLY catalog-free integer projection" has no vp_*.py yet
D0.Matter.LucasTraceCanonicalIntegerProjection
```

(Owner note: BOOK_01 owns φ-from-(p+p^2=1) and the role alphabet; the trace identity tooling is in the toral/evolution certs above. BOOK_04 keeps only the matter-sector *use* of the selector and its M1 forcing.)

### Baryon scaffold

```text
V_B = V_shell^(tensor 3)
dim V_B = 27
Pi_S3 = 1/6 sum_{sigma in S3} P_sigma
dim Pi_S3 V_B = 10
```

The S3 carrier/symmetrizer scaffold is certified. Physical spin/flavour/mass assignment is the next transfer layer. The phrase `full baryon mass table closed` is forbidden without spin/flavour transfer, frozen pole normalization and PDG passport.

### Selector support origin

Book 04 support sizes must come from finite combinatorics, not detached fixtures:

```text
combinatorial origin of the supports
D0.Matter.Book04CombinatorialSelectorOrigins
```

Selector and CKM theorem owners:

```text
D0.Matter.StrictSelectorCertificate
D0.Matter.ckm_no_free_matrix_at_fixed_bases
D0.Matter.book04_selector_claim_no_free_alternative
D0.Matter.Book04FullSupportSelectors
D0.Matter.CKMBasisOrigin
D0.Matter.CKMNontrivialFlavourAlgebra
D0.Matter.MesonDefectTransferOrigin
BaryonS3Symmetrizer
HiggsScalarProjectorConstructive
```

Concrete selector sync: Electroweak radial depth as a concrete selector; `D0.Matter.electroweakDepth35FullSupportClaim`; `D0.Matter.chargedLeptonElectronTerminalClaim`; `D0.Matter.protonReadout306FullSupportClaim`; `D0.Matter.neutronArchiveSiblingClaim`; `D0.Matter.betaUnlockDepth19FullSupportClaim`; full-support finite selector owners use `Fin 71`, `Fin 613`, `Fin 39`. Those windows are no longer the active theory.

CKM origin sync: CKM as finite basis origin, not a free matrix; `D0.Matter.CKMBasisOrigin`; `ckm_origin_candidate_matrix_unique`; `ckm_no_free_matrix_at_fixed_basis_origin`; finite up/down basis-origin selectors; concrete physical score terms.

Torus/Core13 and phason-baryon sync: `torus_geometry_forces_generation_selector_noncommute`; `torus_shell_noncommutativity_forces_nonpermutation_overlap_source`; `BaryonTripleShellCarrier`; Torus shell radius is independent of any Higgs VEV; matter generations and baryons are phason modes with `baryon_phason_symmetric_sector_dim_eq_ten`.

## 04.U Matter as defects and gap-labeled spectra of the φ-quasicrystal hull

Neutrino is interpreted as neutral bulk phason wave; `neutral_phason_wave_has_no_em_coupling` is the finite owner token.

Operator-boundary status (release-candidate):
- Baryon 40/56 carrier + anonymous poles: SPIN-FLAVOUR-CARRIER-CERTIFIED + BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED (image-basis).
- Meson transfer: MESON-TYPED-TRANSFER-CERT-CLOSED.
- Higgs scalar projector + Yukawa section: SCALAR-PROJECTOR-CERT-CLOSED + YUKAWA-SECTION-CERT-CLOSED.
External numerical spectroscopy / Yukawa / PDG comparison remains passport-layer work only. `D0.Matter.book04_operator_boundaries_closed` now points to the above closure classes.

## 04.1 Role of the matter book

Book 04 is the first place where the finite D0 construction is read as matter.  The detector, condensed support, graph birth, action gate and proof calculus are already fixed in Books 01--03.  Therefore the matter book is not allowed to introduce new primitive scales, new post-hoc labels or a fitted particle table.

The canonical matter chain is:

```text
finite carrier/support
-> finite sector operator
-> positive or quadratic response
-> strict finite variational selector / basis mismatch / transfer window
-> external comparison only after the D0 object is frozen.
```

The central rule is:

```math
\boxed{\text{finite support is not a physical mass by itself. Matter = terminally stabilized feedback eigenmodes (Rψ = rψ, |zr|≈1, P_term ψ=ψ); Higgs rank-2 feedback subspace; meson domain wall feedback stretch on C1; baryon S3-stabilized feedback in V⊗V⊗V (D0-CVFT-005).}}
```

Matter defect/domain-wall operators are finite projected operators on the
1-cochain sector of the graded incidence complex.

A support number becomes a physical comparison only after a typed operator/readout and a declared transfer map have been supplied before seeing the target table.

Here `F=P U^dagger Q U P` is feedback-return; it is not the positive response
operator `R=D^dagger D` used in Born/readout formulas.

Bare positive `F` supplies terminal stability and leakage diagnostics only. Complex
mass/width or resonance-pole language must be read from an effective projected
transfer such as `U_eff=PUP`, or from an explicitly declared Feshbach-Schur
reduction. Coefficient-origin trace/residue, hadron resonance transfer and
dynamic neutrino decoherence are frontier programs until those operators and
external passports are frozen.

### 04.1.SPINE Why the matter carrier has rank 3 and a 30-dim hidden sector (forced, not fitted)

The matter book inherits the scene `K(9,11,13)` and its split as a FROZEN
invariant; it does not get to refit it. But the *reason* the carrier splits the
way it does is the structural fact that makes "finite support is not mass by
itself" inevitable, so it is restated here in forcing form (the FACT
`rank(A)=3`, `nullity(A)=30` is owned by BOOK_01 / BOOK_03; this subsection adds
only the *why*).

**Forced split [^b04-14].** Let `A` be the adjacency operator
of `G = K(9,11,13)` in the vertex basis `V = V9 ⊔ V11 ⊔ V13`, `|V| = 33`. Then

```math
\mathbb{R}^V = \mathcal{R}\oplus\mathcal{S},\qquad
\mathcal{R}=\operatorname{span}\{\mathbf 1_{V9},\mathbf 1_{V11},\mathbf 1_{V13}\}\ (\dim 3),\qquad
\mathcal{S}=\operatorname{Ker}(A)\ (\dim 30).
```

The forcing is by `S9×S11×S13`-invariance, NOT by computing eigenvalues: `A`
acts identically on all vertices inside a part, so its image is closed in the
part-constant subspace `\mathcal{R}`, giving `dim Im(A) ≤ 3`; non-empty
inter-part blocks make the action on each `\mathbf 1_{Vi}` nonzero, so
`Rank(A) = 3` exactly; Rank–Nullity then forces
`Nullity(A) = |V| − Rank(A) = 33 − 3 = 30`. There is no free parameter at any
step — the three numbers are fixed the moment the scene is fixed. Status:
CERT-CLOSED (exact integer linear algebra; the finite certificate
additionally certifies the zone split `30 = 8 + 10 + 12` of within-zone
difference modes).

**Why this is the matter-book's load-bearing wall.** `\mathcal{R}` is the
radiation sector (the three part-constant transport modes = the only directions
that carry an inter-zone channel); `\mathcal{S} = Ker(A)` is the sterile sector.
Matter is read off `\mathcal{R}` and the feedback eigenmodes built over it; the
30-dimensional kernel is the structural ceiling on how much hidden capacity the
same finite scene can carry. (Interpretation only; the split itself is the
theorem.)

**Dark = memory without a light channel [^b04-15].** Fix transport/light as the inter-zone action `J(x) := A x` (DEF
17.1.4 — the *same* `A`, no new object). Then for every `x ∈ Ker(A)`,

```math
J(x) = A x = 0 ,
```

so the 30 kernel modes carry exactly zero inter-zone transport: they cannot be
radiated. Yet they are genuine internal degrees of freedom of the scene and they
DO enter the spectral traces (heat-trace / entropy of §17.2 onward). Hence the
sterile sector is "memory without a light channel": a 30-dim hidden capacity
that contributes to the trace-time bookkeeping while emitting nothing. This is
the forced origin of the dark sector — a transport-null kernel, not a fitted
anchor and not a Galois-archive add-on. Status: CERT-CLOSED for the
transport-null structure (the finite certificate establishes that `A` acts
equally across a zone, so every within-zone difference vector lies in `Ker(A)`);
the BRIDGE-layer "dark sector" reading remains interpretation.

### 04.1.START Why the shell ladder starts at 9 (forced operationality level)

The matter book reads `V_shell = span{|9⟩,|11⟩,|13⟩}` as its three-orbit
flavour geometry (see 04.CVFT.F3c). The start value `9` is itself forced and is
not a tuned offset (the address ladder and the `+2` step are owned by BOOK_01
§01.4; restated here only as the *why* the carrier is what it is).

**Start = anchor + operationality level [^b04-16].** The
operationality level is `D_Σ = 5`, because a self-distinguishing language needs
five separable roles — `Code`, `Canon`, `Test`, `History`, `Access` — and so at
least five distinguishable address classes. With fewer than five, two roles
collide onto one address and resolving the collision needs an external catalog,
which M1 forbids. Hence

```math
\mathfrak{D}_1 = \mathfrak{D}_{\rm anchor} + D_\Sigma = 4 + 5 = 9 .
```

The anchor `4` and the level `5` are both forced (not fitted), so the first
shell is `9`; the `+2` step (orientation/holonomy parity, GOLDEN THE 3.11.B)
then forces `9 → 11 → 13`.

**Phase-volume exponent is the same 5 [^b04-17].** Because the
number of independent address choices at level `D_Σ` equals `D_Σ`, the count of
admissible configurations grows with leading order

```math
\#\Omega(R)\asymp R^{D_\Sigma},\qquad D_\Sigma = 5\ \Rightarrow\ R^5 .
```

This `R^5` leading phase volume is the structural seed of the decay law (its
hitting-time/phase-volume formalization lives in BOOK V §24.DECAY; cited here,
not re-derived). [^b04-13] for the
`R^5`-to-decay-law link at the matter-book layer.

### 04.CVFT.F3 Baryon resonance pole scaffold

The frozen operator family proves the nucleon line. It does not prove a full
baryon multiplet table. The current no-go is replaced by a constructive
pole-transfer scaffold. Internal objects:

```math
V_B=V_shell^{\otimes3},\qquad \dim V_B=27,
\qquad \Pi_{S_3}={1\over6}\sum_{\sigma\in S_3}P_\sigma,
\qquad V_B^{sym}=\Pi_{S_3}V_B,\qquad \dim V_B^{sym}=10.
```

This is a 10D symmetric carrier / decuplet-candidate carrier, not a physical
baryon resonance table. Complex poles may be studied only through
`U_eff^B=Pi_S3(PUP)Pi_S3`, with pole equation `det(I-zeta U_eff^B)=0`, or a
declared Feshbach-Schur form. Spin labels, flavour labels, mass/width
assignment, PDG passport, GeV conversion and QCD/EFT bridge remain external.
Nucleon-line-to-full-multiplet shortcuts, random non-Hermitian resonance
operators, complex poles from bare positive `F`, and PDG sorting before frozen
poles are forbidden.

**Baryon Anonymous Pole Scaffold (closed).**
On the certified carriers \(\Pi_B^{40}\) and \(\Pi_B^{56}\):

\[
U_{\rm eff}^{B,k} = \Pi_B^k P U P \Pi_B^k, \quad k \in \{40,56\}.
\]

Anonymous baryon poles are extracted only from image-basis compressed operators \(\widehat U_{\rm eff}^{B,k}=B_k^\dagger PUPB_k\), \(k\in\{40,56\}\) (real S3 projectors, deterministic U, poles from 40x40/56x56 images only). Zero-padded 216D complement poles and PDG assignments are forbidden in core.

Baryon anonymous poles are cert-closed on image basis.

Poles via \(\det(I - \zeta U_{\rm eff}^{B,k}) = 0\) computed on the image basis of the projectors (not the full padded 216D matrix), verified by the finite certificate. BARYON-ANONYMOUS-POLE-CERT-CLOSED. PDG passport remains external.

This scaffold is closed only at carrier/symmetrizer level. It is not a baryon
mass table.

### 04.CVFT.F3b Baryon spin-flavour transfer layer

D0 now has two internal baryon spin-flavour carriers before any PDG passport:

1. The rank-40 fully symmetric separable sector:

```math
\Pi_B^{40}=\Pi_{S_3}^{flavour}\otimes\Pi_{S_3}^{spin}.
```

2. The rank-56 full diagonal exchange-symmetric carrier:

```math
\Pi_B^{56}={1\over6}\sum_{\sigma\in S_3}
P_\sigma^{flavour}\otimes P_\sigma^{spin}.
```

The rank-40 sector is a canonical subcarrier of the rank-56 carrier. The
remaining 16 dimensions are internal mixed spin-flavour states. No PDG names,
no physical masses, and no GeV widths are assigned at this layer.

The internal pole laws are:

```math
\det(I-\zeta U_{\rm eff}^{B,40})=0,\qquad
\det(I-\zeta U_{\rm eff}^{B,56})=0,
```

where:

```math
U_{\rm eff}^{B,k}=\Pi_B^k PUP \Pi_B^k,\qquad k\in\{40,56\}.
```

These compressed pole operators are contractions, `|U_eff^(B,k)| <= 1`. The
contraction is strict only on subspaces with nonzero feedback leakage.

### 04.CVFT.F3c Core-13 orbitals and baryon spin-flavour transfer

The existing PDG/Core-13 passport does not merely show that masses have φ-lattice representatives. Its structural content is the frozen three-orbit shell geometry. D0 now identifies this three-orbit geometry with the finite shell carrier

```math
V_{\rm shell}=\operatorname{span}\{|9\rangle,|11\rangle,|13\rangle\}\cong\mathbb C^3.
```

The baryon flavour carrier is the three-body lift

```math
\mathcal V_B^{flavour}=V_{\rm shell}^{\otimes3},\qquad\dim=27.
```

The exchange-symmetric flavour sector has rank

```math
\dim\operatorname{Sym}^3(\mathbb C^3)=10.
```

With the binary spin dyad (D_2\cong\mathbb C^2), D0 obtains two internal spin-flavour carriers before any PDG passport:

```math
\Pi_B^{40}=\Pi_{S_3}^{flavour}\otimes\Pi_{S_3}^{spin},\qquad\operatorname{rank}=40,
```

and

```math
\Pi_B^{56}=\frac16\sum_{\sigma\in S_3}P_\sigma^{flavour}\otimes P_\sigma^{spin},\qquad\operatorname{rank}=56.
```

The rank-40 carrier is a canonical subcarrier of the rank-56 diagonal spin-flavour carrier:

```math
\Pi_B^{56}\Pi_B^{40}=\Pi_B^{40},\qquad\Pi_B^{40}\Pi_B^{56}=\Pi_B^{40}.
```

Thus the internal decomposition is

```math
56=40+16.
```

The rank-16 complement is the mixed spin-flavour diagonal-symmetric sector. Anonymous pole sets are then defined by

```math
U_{\rm eff}^{B,k}=\Pi_B^k PUP\Pi_B^k,\qquad k\in\{40,56\},
```

```math
\det(I-\zeta U_{\rm eff}^{B,k})=0.
```

PDG names, GeV conversion, physical mass assignment and decay widths remain passport-layer operations. The internal spin-flavour carrier is finite and closed before those external labels are applied.

## 04.2 The theorem owners used by this book

The active matter claims use the following proof owners.

| Function in Book 04 | Owner |
|---|---|
| normalized finite readout | `D0.Core.BornFinite.finite_born_readout_unique_on_finite_outcomes` |
| no alternative response readout | `D0.Core.BornFinite.finite_born_no_alternative_readout` |
| strict finite variational selector uniqueness | `D0.Matter.StrictSelectorCertificate`; `D0.Matter.strict_selected_unique` |
| finite variational selector cannot change without score deformation | `D0.Matter.different_selection_requires_score_change` |
| Book 04 sector finite variational selector contract | `D0.Matter.Book04SelectorClaim`; `D0.Matter.book04_finite variational selector_claim_no_free_alternative` |
| concrete charged terminal finite variational selector | `D0.Matter.chargedLeptonElectronTerminalClaim`; `D0.Matter.charged_lepton_terminal_no_free_alternative` |
| full-support electroweak depth finite variational selector | `D0.Matter.electroweakDepth35FullSupportClaim`; `D0.Matter.electroweak_depth35_full_support_no_free_alternative` |
| full-support proton readout finite variational selector | `D0.Matter.protonReadout306FullSupportClaim`; `D0.Matter.proton_readout306_full_support_no_free_alternative` |
| concrete neutron/archive finite variational selector | `D0.Matter.neutronArchiveSiblingClaim`; `D0.Matter.neutron_archive_sibling_no_free_alternative` |
| full-support beta unlock finite variational selector | `D0.Matter.betaUnlockDepth19FullSupportClaim`; `D0.Matter.beta_unlock_depth19_full_support_no_free_alternative` |
| Book 04 operator boundary no-go | `D0.Matter.Book04OperatorBoundaryClosed`; `D0.Matter.book04_operator_boundaries_closed` |
| CKM matrix unique after bases fixed | `D0.Matter.ckm_no_free_matrix_at_fixed_bases` |
| CKM basis-origin finite variational selector theorem | `D0.Matter.ckm_origin_candidate_matrix_unique`; `D0.Matter.ckm_no_free_matrix_at_fixed_basis_origin`; `D0.Matter.concreteCKMBasisOrigin` |
| generation overlap response origin | `D0.Geometry.TorusCore13GeometryOrigin`; `D0.Matter.GenerationSelectorOrigin`; `D0.Matter.GenerationOverlapResponseOrigin`; `D0.Matter.torus_geometry_forces_generation_finite variational selector_noncommute`; `D0.Matter.torus_shell_noncommutativity_forces_nonpermutation_overlap_source` |
| φ-quasicrystal tiling hull | `D0.Topology.TilingHull`; `D0.Topology.d0_hull_has_phi_cut_project_origin`; `D0.Topology.d0_hull_is_nonperiodic`; `D0.Topology.d0_hull_supports_gap_labeling` |
| K-theory / K0 Gap Labeling | `D0.Matter.KTheoryGapLabeling`; `gap_labeling_requires_frozen_operator`; `d0_gap_labels_are_countable` |
| phason-strain generations | `D0.Matter.PhasonStrainGenerations`; `phason_strain_forces_three_generations` |
| gap-labeled phason domain-wall operator on 1-simplicess | `D0.Matter.MesonPhasonDomainWalls`; `meson_domain_wall_is_gap_labeled_phason_defect` |
| non-abelian holonomy of finite generation-basis transport | `D0.Matter.CKMPhasonHolonomy`; `ckm_matrix_is_phason_holonomy_on_torus_core13` |
| non-abelian seam obstruction gap (finite) | `D0.Gauge.NonAbelianSeamObstructionGap` |
| tick/S3 baryon asymmetry scaffold | `D0.Matter.TickS3BaryonAsymmetry` |
| window-sector fractional charge | `D0.Matter.WindowFractionalCharge`; `window_fractional_charge_is_boundary_readout` |
| window-offset chirality | `D0.Matter.WindowOffsetChirality`; `window_offset_forces_chiral_orientation` |
| neutrino phason waves | `D0.Matter.NeutrinoPhasonWaves`; `neutrino_is_neutral_bulk_phason_wave` |
| matter generation multiplicity | `D0.Matter.matter_rep_generation_multiplicity_three` |
| anomaly preservation | `D0.Matter.anomaly_zero_preserved` |
| generated stress source | `D0.Matter.generated_matter_source_conserved_if_anomaly_free` |

The text below is written theorem-first: each strong claim either has one of these owners, a self-contained certificate, or an explicit comparison boundary.

### The spectral operator the matter book reads from

The matter sector does not invent its own scene. It reads spectra off the **same** complete tripartite scene `K(9,11,13)` on `N=33` vertices that BOOK_01 owns (the scene, the rank‑3/nullity‑30 retained/traced split). What this book adds is the *operator whose spectrum the sector reads* and *why that operator is forced rather than chosen*. The forcing chain below is the spectral spine that downstream §§04.4–04.10 lean on; it is restated here once so every later "active mode" / "30‑fold archive" reference has an owner.

**[DEF] Normalized scene Laplacian [^b04-18].** Let `D` be the diagonal degree matrix of `K(9,11,13)` and `A` its adjacency. The scene Laplacian is the *symmetric* normalization
`L_sym := I − D^(−1/2) A D^(−1/2)`.

**[THE] The symmetric normalization is forced, not a convention [^b04-19].** The scene is degree‑irregular: the three zones have degrees `{20, 22, 24}` (a vertex in the size‑`n_i` zone has degree `N − n_i`). For an irregular graph the random‑walk Laplacian `L_rw := I − D^(−1) A` is **not symmetric**, so applying a symmetric eigensolver (`eigvalsh`) to it manufactures phantom modes — up to spurious *negative* eigenvalues that have no scene meaning. Requiring the readout to distinguish real scene modes from solver artifacts (M1: no externally injected structure) forces the symmetric carrier `L_sym`. The random‑walk operator is therefore boundary, not core. Status: forced choice; rests on the irregular‑degree fact `{20,22,24}`, which is exact integer data off the owned scene.

**[LEM] Reduction to a 3×3 problem on the part‑constant subspace [^b04-20].** Let `n = (9,11,13)`, `N = 33`, and `d_i = N − n_i = (24,22,20)`. On the subspace of vectors constant on each zone, `S := D^(−1/2) A D^(−1/2)` acts by `(Sx)_i = Σ_{j≠i} n_j / √(d_i d_j) · x_j`. Hence the **active** spectrum of `L_sym = I − S` on that subspace is exactly the spectrum of the 3×3 matrix
`L_part = I − [[0, n_2/√(d_1 d_2), n_3/√(d_1 d_3)], [n_1/√(d_2 d_1), 0, n_3/√(d_2 d_3)], [n_1/√(d_3 d_1), n_2/√(d_3 d_2), 0]]`.
The whole spectral question collapses to this 3×3 because everything off the part‑constant subspace is degenerate (next theorem).

**[THE] The scene spectrum splits 1 ⊕ 30 ⊕ (1+1) [^b04-21].** For the complete `k`‑partite graph, `N − k` eigenvectors carry `λ = 1` and the remaining `k` live on the part‑constant subspace. So `L_sym` for `K(9,11,13)` has:
- `λ = 0`, multiplicity 1 — the vacuum / global mode;
- `λ = 1`, multiplicity `30` — the degenerate **bulk/archive** band (this is the *same* 30 the adjacency rank/nullity split owns; the finite certificate establishes `rank(A)=3`, `nullity=30`, zone split `30 = 8+10+12` by exact integer linear algebra);
- two **active** modes, multiplicity 1 each, given by `spec(L_part) = {0, 1.420838683198…, 1.579158554151…}` (one scalar, one vector mode).

The `30`‑fold degeneracy is *why* the archive sector reads as a single undistinguished band rather than thirty separate channels: the matter book's "archive pressure spread over 30 modes" is exactly this multiplicity, not an assumption.

**[DEF] Canonical φ‑rescaling of scene eigenvalues [^b04-22].** The only dimensionless scale already forced (BOOK_01/BOOK_02, from `p + p² = 1`) is `φ`. Canonically reduce any scene eigenvalue by `tilde‑λ := λ / φ`, equivalently read the rescaled operator `G := φ^(−1) L_sym`. No new normalization parameter is introduced — `φ` is the sole admissible scale inside `ℚ(φ)`. Under this rescaling the bulk band sits at `tilde‑λ = 1/φ ≈ 0.6180339887` (×30), and the two active modes at `1.420838…/φ ≈ 0.878191106229…` (scalar) and `1.579158…/φ ≈ 0.975910860021…` (vector). Status of the numeric active‑mode values: the rank/nullity backbone is certified, but no certificate yet pins the two `L_part` eigenvalues `1.420838…` / `1.579158…` to closed form; until one lands these are numerical readouts off the forced 3×3, not theorems. Do not cite them as proven.

This spectral split is the object the rest of Book 04 reads matter off of: the active pair drives the visible (transport) sector, the 30‑fold band is the archive the selector charges against, and the φ‑rescaling is what lets later sections compare a scene eigenvalue to a forced constant without smuggling in an external unit.

## 04.3 Matter objects are selectors, not passports

The previous reading of Book 04 mixed three different things: internal finite objects, dressed Standard-Model comparison values and external data checks. The active reading removes that ambiguity.

A matter object is admitted only through one of the following forms:

1. **Finite support theorem.**  The carrier/support object is proved inside the finite D0 formalism.
2. **Finite response theorem.**  A positive or quadratic response is normalized by the finite Born/readout theorem.
3. **Strict finite variational selector certificate.**  A finite candidate family and score function select a unique internal object.
4. **Basis-origin theorem.**  The up/down operator bases must themselves be outputs of finite basis finite variational selectors.  After those finite variational selectors are fixed, the mismatch matrix is unique up to declared quotient symmetries.
5. **Observable-transfer protocol.**  A frozen D0 object is compared to an external convention through a declared bridge.
6. **No-go.**  The frozen operator family is insufficient to promote a claim.

The word `finite variational selector` is therefore not a stylistic label.  It means a finite candidate set, a score functional and a strict minimizer/maximizer whose uniqueness is protected by the finite variational selector theorems.  Changing the selected object means changing the score functional, not changing a status table.

The quasicrystal matter ontology used later in this book is summarized in 04.4: matter is read as defects, domain walls, holonomies, window weights and K0 gap-labeled spectra over the φ-quasicrystalline tiling hull. This ontology organizes the sector owners; it does not bypass the finite variational selector/readout/passport rules above.

## 04.4 Matter as defects and gap-labeled spectra over the φ-quasicrystalline hull

The D0 vacuum is the condensed/profinite hull of all admissible finite detector registrations, and matter is read as defects, domain walls, holonomies, window weights, and gap-labeled spectra over this φ-quasicrystalline support.

### 04.4.1 Phason-mode generations and baryon S3

The matter generations and baryons as phason modes are theorem-owned by `D0.Matter.PhasonStrainGenerations`. The phason carrier is exactly `D0.Geometry.TorusShell`, so the generation/phason mode count is the already proved three-shell torus count.

The ordered carrier is `BaryonPhasonTriple = PhasonMode x PhasonMode x PhasonMode`, hence dimension `27`. The full baryon multiplet 10D symmetric carrier / decuplet-candidate carrier is not a nucleon-line extension; it is the S3-symmetric phason triple sector of dimension `10`, with `baryon_phason_symmetric_sector_dim_eq_ten`.

**Why exactly three, two forced routes [^b04-28].** Three generations are forced by the toral trace `|Tr(T^2)|=3` plus the torus-shell non-commuting selector (`phason_strain_forces_three_generations`). A second, independent and convergent cutoff comes from the control impedance over the Lucas zone capacities `L_n` (BOOK_03-owned),

```math
I_n := \frac{L_n}{9n}.
```

The impedance climbs smoothly through the controlled regime and then breaks:

```text
n=13: L_13=521   -> I_13 ≈ 4.453
n=14: L_14=843   -> I_14 ≈ 6.691
n=15: L_15=1364  -> I_15 ≈ 10.104   <- structural discontinuity (loss of control)
n=16: L_16=2207  -> I_16 ≈ 15.326
n=17: L_17=3571  -> I_17 ≈ 23.340
```

The jump at `n=15` marks where control over the carrier is lost: capacity outruns the `9n` budget, so no further zone can be registered as a coherent generation without an external catalog to label it (⊥M1). The two routes agree — the trace count fixes the realized generation number, the Lucas impedance fixes *why the ladder terminates* — and neither is fitted. **[^b04-23].** Cross-check obligation: GOLDEN CHK 61.2 (control-loss check at `n=15`).

### 04.4.2 Mesons as phason domain walls

Definition. The lower-Hodge value 400 is the phason domain-wall tension seed on the generation-blind operator. Physical meson transfer requires:

1. phason strain gradient;
2. domain-wall fluctuation operator;
3. spectral gaps;
4. K-theory / K0 Gap Labels;
5. optional PDG passport.

### 04.4.3 Meson K0 Gap-Labeled fluctuation spectrum

Topological K-theory and Gap Labeling classify the fluctuation spectrum of frozen meson operators. The gaps in the meson domain-wall fluctuation spectrum carry discrete K0 gap labels.

The admissible meson chain is:

```text
φ-quasicrystal hull
-> frozen phason domain-wall operator
-> fluctuation spectrum
-> K0 gap label
-> finite transfer window
-> optional PDG passport
```

Definition. The K0 label records which frozen spectral gap is being transported to an external passport. It is not itself a meson mass and does not tune the domain-wall operator.

### 04.4.4 CKM as noncommutative phason holonomy

Definition. CKM is the finite holonomy of phason transport on the Core-13 torus shell carrier (not a fitted mismatch matrix).

The core theorem closes the finite holonomy object and the non-permutation overlap response. The passport layer is separate: physical CKM entries, PDG conventions and uncertainty tables are external comparison protocols and cannot feed back into the phason carrier.

**Mixing arity 3+1 is forced by the interface triangle [^b04-29].** Generations are the interzone interfaces of the K(9,11,13) scene (BOOK_01-owned): `I12(9,11)`, `I23(11,13)`, `I13(9,13)`. The interface graph is the complete graph `K3`:

- 3 vertices ⇒ **3 mixing angles**;
- cycle rank `E - V + 1 = 3 - 3 + 1 = 1` ⇒ **exactly 1 irreducible CP phase**.

This is the `3 angles + 1 phase` structure of CKM read off the scene topology, with zero fitted entries.

**NO-GO on a 4th generation via M1 [^b04-30].** Suppose a 4th generation. A 4th generation is a 4th interface, which requires a 4th zone, which is a 4th structural necessity, hence a new distinguishing role, hence an entry in an external catalog to label that role — forbidden by M1. ⊥. The generation count is therefore closed at three not by tuning but by the catalog-freeness of the scene. **[^b04-24].**

The static reading is separately ruled out: the bare interface-connectivity operator `M_ij = shared/√(cap_i·cap_j)` gives near-flat angle ratios `~1 : 1.09 : 0.90`, against the observed `1 : 0.19 : 0.017`. Hierarchy is therefore not static — M1 forces dynamical mass-dressing of the holonomy (GOLDEN D0-THEORY-DOSSIER THE IV.2). **[^b04-25].**

### 04.4.5 CKM K-class and oriented CP area

The CP phase is the oriented noncommutative area of this holonomy, classifying the CKM K-class. By 04.4.4 the cycle rank of the interface triangle is `1`, so this oriented area carries exactly one irreducible phase — the single CKM CP phase, not a free parameter.

### 04.4.6 CKM↔PMNS hierarchy inversion from rank-nullity

**The quark/lepton mixing asymmetry is forced, parameter-free, by the scene spectrum [^b04-31].** The K(9,11,13) scene splits into a rank-3 distinguishing sector and a 30-dimensional nullity (rank 3 / nullity 30, BOOK_02-owned spine fact).

- **Quarks** live on the 3 nondegenerate active modes (eigenvalues `21.84, -9.76, -12.08`). Nondegeneracy is a steep spectral hierarchy, and a steep hierarchy *suppresses* rotation between modes ⇒ **CKM mixing is small**.
- **Neutrinos** live in the 30-fold degenerate kernel (the Sterile Archive). Degeneracy means no preferred basis, so rotation is unobstructed ⇒ **PMNS mixing is large**.

So the long-standing Standard-Model puzzle — why quark mixing is tiny while lepton mixing is order-one — is read off `rank 3` vs `nullity 30` of one fixed scene, with **zero free parameters**. The kernel further inherits the three-zone split `30 = 8 ⊕ 10 ⊕ 12` (intra-zone difference vectors), so the zeroth-order PMNS pattern is zone democracy — the tri-bimaximal/trimaximal pattern is pulled into place rather than fitted (GOLDEN D0-THEORY-DOSSIER THE IV.4). **[^b04-26].**

### 04.4.7 Window-sector fractional charges

The D0 support is a cut-and-project quasicrystal. Matter as phason/window defects of the φ-quasicrystal vacuum maps the fractional quark charge as a window-sector intersection weight:

- one sector -> 1/3;
- two sectors -> 2/3;
- orientation/sign branch -> +/-.

Hence, quark color/charge = window-sector weights and generations = inflation classes.

### 04.4.8 Window-offset chirality

Weak chirality is represented as a window-offset effect: chirality = acceptance-window offset.

### 04.4.9 Neutrino as neutral bulk phason wave

The neutrino is represented as a neutral bulk phason wave with zero active EM coupling.

**Why the neutrino has mass [^b04-32].** Beyond the *fact* that the neutrino is a neutral bulk phason with zero EM coupling, its mass is forced. The holographic commutator `[J,Y]≠0` is rigidity-forced on the K(9,11,13) carrier (this nonvanishing is BOOK_02-owned — forcing: GOLDEN THE 2.9A — and is what produces the quantum of action `ℏ` in the Active Transport boundary). Evaluate the *same* commutator inside the 30-dimensional Sterile Archive `𝒮^30` (the nullity of 04.4.6): it does not vanish there either, because `ℏ` mathematically cannot vanish even in the unobservable Archive. Its residue is an irreducible, non-spatial phase oscillation, and the neutral bulk phason is its physical carrier. The neutrino mass scale is therefore the algebraic gluing anomaly

```math
m_\nu \propto \Delta_\alpha^2,
```

the **minimal nonzero eigenvalue** of the `[J,Y]` obstruction projected into the null space. Nonzero because `ℏ ≠ 0`; minimal because it is the smallest such eigenvalue in the 30-dim kernel. The neutrino is light, not massless, by the same uncertainty that makes it exist. **[^b04-27].** Beat cross-link: the oscillation small parameter is `Δα` (BOOK_03-owned), the seam beat between topological and algebraic evolution (GOLDEN BOOK-VI-EXTENSIONS THE 61.7).

## 04.5 Terminal matter triad

The terminal laboratory section of a matter event has three primitive readout roles.

The photon is the pure line carrier:

```math
D_B^\gamma=0,\qquad m_\gamma=0,\qquad E_\gamma=h\nu=\hbar\omega.
```

The electron is the stable charged terminal register.  The neutral leakage quantum is

```math
\ell_\nu={\delta_0\over4}.
```

The first boundary defect has the paired terminal projections

```math
3(D_e^2-1)=4\ell_\nu=\delta_0.
```

This does not assert that all interactions are electromagnetic.  It says that stable macroscopic records use a charged terminal register, a neutral leakage branch and a massless line carrier.

### 04.5.1 Why the triad is rigid: the prime edge count forces it

The triad above is not three independently chosen roles; it sits on a carrier whose discreteness is forced. The total edge count of the scene `K(9,11,13)` is

```math
|E|=9\cdot11+9\cdot13+11\cdot13=359,
```

which BOOK_01 owns as the scene 1-skeleton edge count (cite, not re-derived here). The forcing step is: **`359` is prime, and primality forces topological rigidity** — the edge carrier admits no nontrivial continuous internal gauge orbit, so every matter observable can exist only as a discrete topological defect (anyonic excitation) on the rigid 1-skeleton, never as a continuous internal symmetry coordinate. The charged register, the neutral leakage branch and the massless line carrier are then forced as *defect classes*, not as a menu choice. [^b04-37]

[^b04-33] — the primality→rigidity→discrete-defect chain is stated as a forcing argument; the executable certificate that checks "359 prime ⇒ no continuous internal gauge orbit on the edge carrier" is not yet present and must not be cited until it exists.

### 04.5.2 The 359 ceiling is a distinguishability limit, not a normalization

Elsewhere `359` appears as the count feeding `alpha_top` normalization. The sharper forcing reading is what makes `359` a *limit* rather than a tally:

> The coherent-channel address space has cardinality exactly `359`. Injectively encoding more than `359` independent phase trajectories in one coherent cluster is impossible: addresses collide, and address collision is decoherence.

This is a hard distinguishability ceiling in the sense of M1 — beyond `359` the cluster can no longer distinguish its own channels without an external catalog, which M1 forbids, so the encoding collapses. The edge count is therefore simultaneously the geometric 1-skeleton size and the coherent-address capacity; the two coincide because both are the same finite distinguishability budget. [^b04-38]

### 04.5.3 Companion embedding: the leakage/branching exponents are intrinsic

The fractional branching exponents that label the leptonic leakage branch (`1/4` and `1/3`) are not fitted to measured masses; they are Puiseux holonomy indices of finite companion restrictions embedded in the `359`-edge carrier. The `C_4/R_3` companion cover and the `1/4,1/3` indices embed through a determinant-factorization that closes the construction.

Let `lambda` be the edge holonomy parameter. The terminal-capacity block is the companion operator `C_4(lambda)` with characteristic equation `z^4 - lambda = 0`; the internal scene-rank block is `R_3(lambda)` with `z^3 - lambda = 0`. They embed into the edge carrier as

```math
U_E^{\text{cover}}\cong U_{\text{bulk}}^{352}\oplus C_4(\lambda)\oplus R_3(\lambda),
\qquad 352+4+3=359.
```

The local resolvent of the edge-cover operator then factors as

```math
D_E(z,\lambda)=D_{\text{bulk}}(z)\,(z^4-\lambda)(z^3-\lambda),
```

so the roots are Puiseux branches `z=lambda^{1/4} xi_4^j` and `z=lambda^{1/3} xi_3^j`, and the two non-bulk ramification exponents are exactly

```math
p_\mu={1\over4},\qquad p_\tau={1\over3}.
```

The direct-sum embedding preserves determinant factorization, so the branch indices are intrinsic to the finite edge-cover block — not obtained by fitting lepton masses. The `4` is the orientation/terminal-capacity budget and the `3` is the internal scene rank; tri-generation is then a closed consequence of the prime-edge carrier, not an input. [^b04-39]

[^b04-34] — the companion-characteristic-polynomial check and the `352+4+3=359` embedding count are a forcing target; no executable certificate for this embedding currently exists, so none is cited.

### 04.5.4 Fibonacci-fusion / Jones-index bridge to φ

The prime-edge anyon scaffold ties back to the golden ratio through the fusion algebra of the defects. The defect category carries Fibonacci fusion `tau (x) tau = 1 (+) tau`, whose subfactor Jones index is

```math
[M:N]=\varphi^2={3+\sqrt5\over2}.
```

The leakage/branching exponents `1/3` and `1/4` are then read as braiding holonomy indices around the rigid defects, and the Higgs role appears as a rank-2 projector on the `C_4/R_3` ramification block. This closes the loop: the same `phi` that forces the spine (BOOK_01, `p+p^2=1`) reappears as the index of the matter-defect category, so the matter sector is not an independent algebra glued on top of the spine — it is the spine's own braiding statistics. [^b04-40]

[^b04-35] — the `tau (x) tau = 1 (+) tau ⇒ [M:N]=phi^2` bridge and the braiding-index reading of `1/3,1/4` are a structural forcing target; no executable certificate exists for it, so none is cited.

### 04.5.5 Window branch group (Z/44)* and the Cabibbo soft joint

The charged-register / leakage split also fixes a window branch group whose unit count lands the Cabibbo angle with zero free parameters. With return quotient `q_T=44`, the branch group is

```math
(\mathbb Z/44)^\ast\cong\mathbb Z_2\times\mathbb Z_2\times\mathbb Z_5,
\qquad |(\mathbb Z/44)^\ast|=\varphi_E(44)=20=d_{13}.
```

Its characteristic (catalog-free) subgroups are exactly `{1, 4, 5, 20}`: the `2`-torsion `T` (order 4), the squares `F(5)`, and the full group `G(20)`. Here

```math
20=4\times5=|ABCD|\times D_\Sigma
```

— the orientation budget `|ABCD|` times the operational budget `D_Sigma` — and the product of all units mod 44 is `+1`, so the window is phase-neutral. Mass is memory winding and generations are classes of branch defects, so M1 admits only the classes `{1,4,5,20}`: class 4 is killed by orientation blindness (THE 3.11.B), leaving generation 1 (class 1) and generation 2 (class 20).

This forces the first Cabibbo readout structurally:

```math
{m_s\over m_d}=20\ \text{(exact)},\qquad
\sin\theta_C={1\over\sqrt{20}}={1\over2\sqrt5}=0.22361,
```

against the lattice/FLAG cross-check `m_s/m_d=20.01\pm0.55` (0.03 sigma) and `sin theta_C` experimental `0.22501(68)` (0.62%, inside the GST `O(lambda^2)~5%` bridge tolerance). The Cabibbo chain is thus 2 THE + 1 MECH-LIMIT-gap + 1 BRIDGE(GST): the window-44 group spectrum is the THE, and `m_s/m_d=20` with the Cabibbo readout is the core MECH-LIMIT+BRIDGE.

**[THE 04.5.5.D] Deformation no-go: `20` is a group cardinality, not a fitted ratio.** The value `20` enters as `φ_E(44)=|(\mathbb Z/44)^\ast|` — the order of a finite unit group, an integer by construction (a counting invariant, not a measured quantity). It is rigid in three independent ways: (i) `φ_E` is integer-valued, so `20→20±ε` is not the totient of any modulus; (ii) the characteristic subgroup lattice `{1,4,5,20}` is exactly the divisor structure of `20=2^2·5`, and a non-divisor count carries no such lattice; (iii) the factorization `20=4×5=|ABCD|×D_Σ` ties the count to the orientation and operational budgets, themselves fixed integers. Shifting the number off `20` therefore does not perturb a ratio — it leaves the unit group `(\mathbb Z/44)^\ast` altogether, and to land on any other value one would have to *specify* the shift, i.e. supply an external parameter, ⊥M1. The reviewer's question is not "does `20` match `m_s/m_d`" (that cross-check is the GST bridge) but "is `20` forced as a group cardinality" — and it is; the experimental agreement is a consequence, not the support.

**Class 5** is killed by aliasing (winding 5 = address `D_Sigma=5` ⇒ pointer collision = hidden memory, grammar 01.11C). This exclusion — formerly the matter sector's **third soft joint** — is now closed at the finite level by a certificate: the order-5 subgroup of `(ℤ/44)*` has `|·| = 5 = D_Σ`, so the period-5 winding orbit bijects onto the 5 operational address classes (the pointer collision is exact), leaving survivors `{1, 20}`. What remains a theorem-target is only the full hidden-memory M1 contradiction, at the same standing as the (owned) class-4 kill.

**External anchor — lepton mixing (passport target, not core).** The lepton sector carries the `δ₀`-family of mixing predictions, `δ₀ = (√5−2)/2 = 1/(2φ³)`:

```math
\sin^2\theta_{12} = \tfrac13 - 2\delta_0^2 = 0.3055,\quad
\sin^2\theta_{13} = \tfrac{\varphi^{-5}}{4} = 0.02254,\quad
\sin^2\theta_{23} = \tfrac12 + \tfrac{\delta_0}{2} = 0.559 .
```

All three land inside the NuFIT 6.0 normal-ordering bands (`0.307 / 0.0220 / 0.561`), and on `θ₁₂` the value `0.3055` is closer to data than golden-ratio-A (`0.276`), tri-bimaximal (`1/3`), and golden-ratio-B (`0.345`). JUNO will pin `sin²θ₁₂` to the sub-percent level — a central value outside `[0.300, 0.311]` rejects the family. This is an empirical-passport comparison (cite NuFIT 6.0; JUNO): `δ₀` is forced, but the angle *formulas* are not yet derived from M1, so the family is a falsifiable target, never core.

[^b04-36] — the class-5 aliasing kill is the open soft-joint obligation; `m_s/m_d=20` and `sin theta_C=1/sqrt20` are carried as dossier claims above, and no new certificate is invented here.
## 04.6 Finite Born 2.0 in matter language

The finite matter probability chain now starts one step before effects.  A finite channel amplitude `(x,y)` is first reduced to the forced phase-blind quadratic response `x^2+y^2`; matter effects then aggregate these squared norms over the finite support; only then is the response normalized.  Thus a matter-sector probability cannot introduce either a new response functional or a new probability functional.

```text
finite amplitude channel -> D†D squared norm -> finite response -> Born normalization
```


Matter readout may use a normalized weight only after the finite effect frame has been supplied.  A candidate particle sector must identify:

```text
finite candidate support I;
finite detector/support atoms S;
nonnegative effects E_i(s);
nonnegative detector state R(s);
raw responses r_i = Σ_s E_i(s)R(s).
```

Only then may Book 04 write

```math
P(i)=\frac{r_i}{\sum_jr_j}.
```

The theorem owners are:

```text
D0.finite_effect_born_readout_unique
D0.finite_effect_born_no_hidden_response
D0.finite_coarse_born_readout_unique
D0.finite_tensor_born_readout_unique
D0.finite_power_readout_no_alternative
```

This changes how matter claims are allowed to be written.  A particle table cannot add a probability, branching weight, mixing weight or likelihood weight as a new primitive.  It must identify the finite effect/response object that is being normalized.  A tempting nonlinear rule

```math
P_q(i)=\frac{r_i^q}{\sum_jr_j^q}
```

is not a second D0 law.  At fixed response, it must collapse to the Born weight or fail the response-recovery equation.  Therefore Book 04 can no longer hide weak particle claims behind alternative weighting conventions.

### 04.6.π The structural angle `π_0` is forced, not measured

The Born readout above lives on phases, and a phase is an *angle*.  But the matter scene is a graph: there is no circle, so the closure constant of a memory cycle cannot be the classical transcendental `π`.  This subsection derives the structural constant `π_0=(6/5)φ²` that the runtime in BOOK_02 §02 (`α_alg⁻¹=2¹¹π_0/φ⁸+2δ₀/3`; `π_0=(6/5)φ²=3.1416407865…`) and BOOK_07 §07.11 already *consume*.  Path memory is encoded as a phase; the question is the minimal step of that phase.

**[DEF 04.6.π.1] Angular microquantum `δθ` [^b04-53].** Encode the memory of a path as an angle and write its minimal step through the still-unknown cycle-closure constant `π_0`:

```math
\delta\theta := \frac{3}{5\,\pi_0\,\varphi}.
```

`π_0` is the cycle-closure constant to be solved for below with no external parameter.

**[THE 04.6.π.A] Projective-density `ρ=3/5` [^b04-54]. [^b04-41].** The minimal scene carries `Z=3` topologically independent zones and `D_Σ=5` realizability layers (both owned by BOOK_01: the `K(9,11,13)` scene and the `D_Σ=5` role alphabet).  The canonical projection factor of a signal through the scene is then

```math
\rho := Z/D_\Sigma = 3/5.
```

⊥-proof.  Suppose `ρ≠3/5`.  Then there exists a pair of weight sets `w_Z, w_D` (equivalently a correction multiplier) fixing the relative importance of zones vs layers.  Those weights are not derivable from `φ` or `Σ`; they must be added as independent dimensionless constants — an exogenous weight catalog — forbidden by M1 (DEF-0.2.2).  Hence `ρ=3/5`. □

**[LEM 04.6.π.2] The microquantum is `δ₀` [^b04-55]. [^b04-42].** With `ρ=3/5`,

```math
\delta\theta = \frac{\rho}{\pi_0\,\varphi} = \frac{3}{5\,\pi_0\,\varphi}\equiv \delta_0,
```

where `δ₀=(√5−2)/2=1/(2φ³)` is the foundational quantum of distinguishability owned by BOOK_01 (cite, do not re-derive).  ⊥-proof.  If `δθ≠δ₀` then `k:=δθ/δ₀` is a new dimensionless constant, not derivable from `φ` and the already-fixed scene objects; it would require a constant catalog — forbidden by M1.  Hence `δθ=δ₀`.  This is the dropped link: the angular microquantum is *pinned* to the existing `δ₀`, so no new constant enters when the angle is introduced. □

**[THE 04.6.π.B] `π_0` is algebraic, in `Q(φ)` [^b04-56].** In CORE only quantities expressible in the fixed field `Q(φ)` and previously defined scene/`Σ` constructions are admissible.  Classical transcendental `π` is a continuum-limit object and is not in `Q(φ)`; in the discrete scene the cycle-closure constant must be the algebraic invariant `π_0∈Q(φ)`.  The gap `π_0−π` is then a discreteness/curvature effect at the Planck scale in the BRIDGE limit, not a defect.  This is exactly why the runtime ban in BOOK_02 §02 (the `(π_0/π)` counter-term ban) is forced rather than stylistic.

**[THE 04.6.π.C] Unit-precision cycle closure [^b04-57].** Require that over one full turn the accumulated angular error be compensated by the scene structure to exactly one unit of distinguishability — tooth-for-tooth, no remainder in the `Σ` metric:

```math
\text{angular quantum}=\frac{\text{projective factor}}{\text{cycle constant}\times\text{scale}}
\quad\Longrightarrow\quad
\delta_0 = \frac{3/5}{\pi_0\,\varphi}.
```

**[THE 04.6.π.4] Solve `π_0=(6/5)φ²` [^b04-58].** Substitute the owned value `δ₀=1/(2φ³)` into the closure balance THE 04.6.π.C:

```math
\frac{1}{2\varphi^3}=\frac{3}{5\,\pi_0\,\varphi}
\quad\Longrightarrow\quad
\pi_0=\frac{6}{5}\varphi^2.
```

Numerically `φ²≈2.6180339887 ⇒ π_0≈3.1416407865`, departing from classical `π` already at the 4th decimal (3.1415… vs 3.1416…).  This is the same constant BOOK_02 §02 and BOOK_07 §07.11 already cite.

**[DEF 04.6.π.5] Mass quantum `m_0:=2π_0` and time quantum `t_0:=1/m_0` [restored].** One full holonomy of the memory cycle is two half-turns, so the mass quantum (the cost of one closed internal cycle) is `m_0:=2π_0=(12/5)φ²` and the conjugate time quantum is `t_0:=1/m_0=(5/12)φ⁻²`, with `m_0·t_0=1` (exact in `Q(φ)`). These two identities were derived in the GOLDEN chain (mass quantum = one full holonomy-cycle length) and dropped in the v14 refactor; they are restored here as immediate consequences of the now-derived `π_0` (THE 04.6.π.4), with `cert vp_mass_chain_alpha.py` and claim `D0-MASS-CHAIN-001`. The rest-mass reading `m_rest=m_0·W` (W = number of memory windings) needs the per-state winding `W` and is **not** restored here — it is a named gap (OWNER-DECISION; the winding values are sought in the GOLDEN coverage ledger before any re-derivation).

**[COR 04.6.π.5a] The fine-structure amplitude is a mass-quantum count (α↔mass stitch).** The second-moment amplitude of the `α⁻¹` resolvent writing (BOOK_02 §02.13.4, `D0-DELTA-ALPHA-MOMENT-001`) is `μ₂=2¹¹π_0φ⁻²`; since `m_0=2π_0`, this is **exactly** `μ₂=2¹⁰·m_0·φ⁻²`. So the same holonomy `π_0/m_0` plays two roles — the scattering phase in `α` and the cycle length in mass — one object, not two derivations (a finite cross-book identity, `vp_mass_chain_alpha.py`). The capacity factor `2¹¹` itself stays flagged (`=2^{V₁₁}`), not forced; the unified resolvent-trace formula `μ_k` remains the named open gap of `D0-CVFT-F1`. (Iter-17 sharpened that gap: `μ₁=1/rank` is now derived as the depth-0 floor return and the `π₀` factor of `μ₂` is owned; only the `2¹¹=2^{V₁₁}` active↔archive pairing multiplicity stays open — `vp_feshbach_residue_amplitudes.py`.)

**[ONTOLOGY 04.6.π.6] Mass is an inverse period (distinct from the numeric hierarchy no-go).** The core *reading* of mass is `mass = τ⁻¹`, the inverse of a canonization-cycle period — a frequency, not a fitted number. The certified `m_0·t_0=1` (DEF 04.6.π.5) **is** this ontology at the quantum level: the mass quantum is the inverse of the time quantum. The winding extension `m_rest = m_0·W` (`W` = number of memory windings) is the structural form of a rest mass; the **per-particle `W` values are a physical input** (a passport/bridge), **not** core theorems — exactly the boundary of the matter-sector no-go `D0-GEN-MASS-001` (physical masses/Yukawa/PDG clustering require physical input). So the *ontology* (mass = inverse period) is core; the *numeric mass spectrum* stays out of core, and `W` is not recovered from any internal derivation.

**[THE 04.6.π.D] Relativistic energy as accelerated cycle frequency [^b04-59]. [^b04-43].** Let a mass state be a stable light cycle `P` of rest frequency `ω₀:=τ(P)⁻¹`.  In CORE normalization (`C=1`) a moving state is the tilt of the light tick between external transport and internal run.  Observed energy is then the amplification of the internal cycle frequency:

```math
E=\gamma\,\omega_0,\qquad p=\gamma\,\omega_0 v,\qquad E^2-p^2=\omega_0^2.
```

Relativistic dynamics introduces no new entity: it is the same looped light re-marked at nonzero drift.  This `E²−p²=ω₀²` rest-frequency content is what licenses the matter-sector mass spectrum (04.7–04.8) to read off `ω₀` rather than post a free mass.

### 04.6B Fermionic statistics are forced by quaternionic holonomy

The Born readout fixes *how* matter probabilities are written; this block fixes *why* the carriers of those probabilities are fermions (spin-1/2) and *why* the weak channel is chiral.  Window-offset chirality (04.4.7) is the symptom; the structural forcing below is the cause.

**[THE 04.6B] Discrete spinor generation [^b04-60]. [^b04-44].** The core feedback-return operator `F_N = P_N U_N† Q_N U_N P_N` (owned by BOOK_01 / BOOK_02; cite, do not re-derive) acts structurally as left quaternion multiplication on the `Ω_8` terminal states.  Under left quaternion multiplication any spatial cycle traversing the imaginary axes `i,j,k` squares to `−1`, algebraically forcing a sign flip into the sterile archive; only a `4π` double-cycle returns the terminal register to identity (`i⁴=1`).  This discrete holonomy forces every topological matter defect to be fermionic (spin-1/2): a `2π` return is the nontrivial class, a `4π` return the identity.  Weak chiral asymmetry is then forced by the non-commutativity of the spatial operators (`ij=k`, `ji=−k`): the two exchange orders are not the same group element, so the channel cannot be parity-symmetric without an exogenous catalog of sign conventions — forbidden by M1.

### 04.6.PAULI Pauli exclusion, spin sign and the decay exponent as canonical-algebra identities

The fermion-forcing block above identifies the carriers as spin-1/2; the following three results are the canonical-algebra consequences of that identification.  They sit here next to 04.6B because they are the same fermion sector.

**[DEF 04.6.PAULI.1] CAR algebra [^b04-61].** A mode `i` is the canonical class of a one-particle state at a fixed distinguishability level (local neighborhood + cycle/phase class), defined with no external weight choice.  Introduce creation/annihilation operators with anticommutation relations

```math
\{a_i,a_j^\dagger\}=\delta_{ij},\qquad \{a_i,a_j\}=0,\qquad \{a_i^\dagger,a_j^\dagger\}=0.
```

**[THE 04.6.PAULI.3] Pauli exclusion as an identity [^b04-62].** From `{a_i†,a_i†}=0` it follows that `(a_i†)²=0`.  Double occupation of one mode is therefore structurally impossible and needs no separate postulate — exclusion is the CAR antisymmetry, not an added rule.

**[THE 04.6.SPIN.2] Exchange sign from `π₁=Z₂` [^b04-63].** The configuration space of two indistinguishable excitations has fundamental group `π₁≅Z₂` (exchange is the nontrivial loop class).  The Fermi sector realizes the nontrivial one-dimensional representation `Z₂→{±1}`, so exchanging two identical excitations multiplies the amplitude by `−1`.  Equivalently `2π` is the nontrivial element and `4π` the identity — the same holonomy ledger as THE 04.6B, reached independently from the configuration-space topology.

**[THE 04.6.DECAY.2] Leading decay exponent `Γ∝R⁵` [^b04-64]. [^b04-45].** Let the finite transition configurations be parametrized by `D_Σ=5` independent addressing coordinates (BOOK_01 role alphabet) and let the transition resource scale as `R` (proportional to mass/frequency).  The number of accessible configurations grows as `#Ω(R)≍R^{D_Σ}`, so at `D_Σ=5` the phase volume grows as `R⁵` and the characteristic transition rate at fixed protocol has leading power

```math
\Gamma \propto R^5.
```

The exponent is the layer count `D_Σ=5`, not a fitted phase-space power; any other leading exponent would require an exogenous layer-weight catalog (cf. THE 04.6.π.A), forbidden by M1.

### 04.6.M1 Matter-sector inevitability register (selected entries)

The matter facts of this book (fractional charge, three generations, the spin-1/2 carrier) are FORCED by the same catalog-free arguments, not fitted.  The entries below give the GOLDEN ⊥-derivations behind those facts; numerical-in-GeV/cosmological-fraction items are BRIDGE-predictors and carry that status.

**[THE 04.6.M1.Δn] Orientable history ⇒ address step `Δn=2` [^b04-65]. [^b04-46].** The scale of layer `n` is approximated by a Lucas integer `L_n≈φⁿ`; the approximation error `ε_n=L_n−φⁿ=(−φ)⁻ⁿ` has sign oscillating as `(−1)ⁿ` (`Tr(Tⁿ)=(−1)ⁿL_n` is owned by BOOK_06 §06.1).  Joining layer `n` to `n+1` stitches metrics of opposite error-curvature sign, which needs a local orientation bit not contained in the address — an external stitching catalog, forbidden by M1.  The only step preserving the error sign and the topology is even, so addressing advances `5→7→9→11→13` and the `K(9,11,13)` scene is inevitable.

**[THE 04.6.M1.dim] Stable defects ⇒ effective `3+1` [^b04-66]. [^b04-47].** Matter is a stable topological defect (knot/link), else a "particle" is indistinguishable from noise and needs an external identity catalog.  Codimension-2 links are stable objects only at three spatial dimensions: at `D<3` there is no room to braid identity trajectories without a bridge/jump catalog; at `D>3` generic links untie and lose topological protection without a choice of "which classes are fundamental."  Hence `D=3` is the minimal integer dimension carrying stable matter with no exclusion catalog; the `+1` axis is the canonization (time) axis.  (Rigorous knot-vs-dimension content lives in BOOK_05; here only the no-catalog logic is used.)

**[THE 04.6.M1.gauge] Braid valence ⇒ `U(1)/SU(2)/SU(3)` [^b04-67]. [^b04-48].** Local indistinguishability of permuted/braided incident edges generates braid-group representations `B_k` for valence `k`.  In the `K(9,11,13)` gluing regime fundamental local events have effective valence `≤3` (branch/splice/pass).  In the BRIDGE/coarse limit these realize as unitary representations: additive phase ⇒ `U(1)`, double-braid ⇒ `SU(2)`, triple-braid ⇒ `SU(3)`.  A fundamental `SU(5)` would require irreducible valence-5 vertices at valence `≤3`, i.e. an external list of "what counts as fundamental" — forbidden by M1.  The claim is the *inevitability of these effective continuous languages*, not a discrete-to-`SU(N)` isomorphism.

**[THE 04.6.M1.charge] Fractional charge `{−1/3,+2/3}` from `A₂` projection [^b04-68]. [^b04-49].** Charge `Q` is the linear functional projection on the weight lattice of the fundamental `SU(3)` representation (root system `A₂`).  A baryon is a closed 3-knot simplex carrying one unit phase winding; indistinguishable nodes split it as `1/3`, and projecting the equilateral-triangle vertices on the scene's center↔shell symmetry axis yields exactly `+2/3,−1/3,−1/3`.  Any other value (e.g. `0.5`) distorts the triangle and needs a deformation catalog — forbidden by M1.  This is the GOLDEN `A₂` weight-lattice forcing; it is *distinct from* and complementary to the cut-and-project quasicrystal window weights of 04.4.6/04.4.7, which reach the same `±2/3,−1/3` numbers by a different route.

**[THE 04.6.M1.gen] Three boundary types ⇒ three generations [^b04-69]. [^b04-50].** The generation index is the zone label `9/11/13` of the minimal scene.  A fermion is a boundary resonance, and the 3D projection of the scene has exactly three boundary types: center/point `→ e`, torus/cycle `→ μ`, shell/sphere `→ τ`.  No fourth boundary type exists in 3D, so a fourth generation needs a fourth dimension or a hand-inserted boundary-type index — a catalog forbidden by M1.  This is the GOLDEN 3-boundary-type completeness argument; it is the structural complement to the `F₂` branch-defect generation index of BOOK_01 §01.23.

**[THE 04.6.M1.grav] Gravity weakness as area-vs-volume holonomy [^b04-70]. [^b04-51].** Interaction strength scales as `1/N` with the number of interaction partners.  Local gauge forces act on the lightcone surface ("now"), `N∼R²`; gravity is a holonomic/memory force acting over the whole 4D history volume, `N∼R⁴`.  Hence the CORE ratio

```math
\frac{F_{grav}}{F_{local}}\sim\frac{1}{R^2},
```

with `R` the dimensionless history scale (nodes/layers in the observer window).  Making gravity strong would require it to "not see" history — a screening catalog forbidden by M1.  (The holographic area form `S=βR²/4` of BOOK_07 §07.3 is the retained-block statement; the `R²` vs `R⁴` argument here is the dropped forcing of *why* it is area, not volume.  Order-of-magnitude numbers like `10⁴⁰` are BRIDGE-predictors and require the IV.3 translation protocol.)

**[REM 04.6.M1.Λ] `Ω_Λ→1/(1+φ⁻¹)≈0.72` [^b04-71]. Status: BRIDGE-PREDICTOR (cosmological fraction; requires IV.3 translation protocol + uncertainty interval).** Matter (zones 9+11) and vacuum (shell 13) split the energy budget by information capacity (entropy); in the 4D holographic graph the shell entropy dominates, giving the structural limit `Ω_Λ→1/(1+φ⁻¹)≈0.72` (≈0.69 with the `π_0` curvature correction).  `Vol_{13},Vol_{11},Vol_9` are heat-trace state-counting measures, not `R³` volumes.  `Ω_Λ` is fixed here by the entropic-balance derivation, not carried as an external comparison coordinate.

**[REM 04.6.M1.anti] Antimatter scarcity from Landauer cost [^b04-72]. Status: BRIDGE-PREDICTOR (requires IV.3 protocol; statistical model with explicit T-range).** Matter is a direct write; antimatter is `NOT·write`, and the `NOT` bit-flip carries an irreversible Landauer cost `k_BT ln2`, so `Cost(NOT)>Cost(COPY)`.  Under early-universe resource scarcity the production probability is `P∼e^{−Cost}`, making antimatter algorithmically unfavorable.  A `1:1` symmetry would require `Cost(NOT)=0`, i.e. a Maxwell-demon catalog forbidden by thermodynamics and M1.  The tick/S3 baryon-asymmetry scaffold is here given its thermodynamic-selection forcing.

**[REM 04.6.M1.mH] `m_H≈√2·m_Z` cube-diagonal [^b04-73]. Status: BRIDGE-PREDICTOR (GeV value; requires translation protocol, `δ_th`, and the QED/QCD/electroweak correction list — none of which are fit parameters).** Vector bosons `W,Z` set the edges of the vacuum cell; the Higgs scalar `H` sets its diagonal (breathing mode).  At the potential minimum the cell is orthogonal (cubic isospin symmetry), and the face-diagonal-to-edge ratio of a cube is `√2`, giving `m_H≈m_Z·√2·(1−δ_loop)`.  An arbitrary `m_H` (a free `λ`) means a skewed vacuum cell, which needs a deformation tensor catalog — forbidden by M1.  This entry carries BRIDGE status.

**[THE 04.6.M1.time] Heat-trace monotonicity ⇒ time arrow [^b04-74]. [^b04-52].** A merge `A+B→C` is information-irreversible; reversing it requires knowing which `A,B` produced `C`, which must be stored in an external backup of the past.  The universe is autonomous (no external disk), so by M1 the past information is erased into heat/gravity and the chosen functional (heat-trace / diffusion entropy) is monotone under admissible dynamics.  Any model where this functional is non-monotone without external pumping is excluded as non-reproducible.  (`Tr(Tⁿ)=(−1)ⁿL_n` and the heat-trace channel are owned by BOOK_06; the matter-book contribution here is the no-external-backup forcing.)
## 04.7 Electroweak radial depth as a concrete finite variational selector

The matter sector inherits the single action section from Book 03.  Electroweak quantities are therefore read as finite radial depths and comparison outputs, not as independent primitive constants.

The active integration replaces the earlier phrase "depth 35" by an actual Book 04 finite variational selector owner:

```text
D0.Matter.electroweakDepth35FullSupportClaim
D0.Matter.electroweak_depth35_full_support_no_free_alternative
```

The finite variational selector window is:

```text
{depth34, depth35, depth36}
```

with depth 35 as the unique zero-residual branch.  Therefore an alternative EW depth is not a notation change; it requires a changed EW radial score.

The internal ratio is

```math
{M_W^2\over M_Z^2}=T_W/T_Z=0.7767227212877189,
\qquad
\sin^2\theta_W^{D0}=0.2232772787122811.
```

The bare radial expression is

```math
\lambda_Z^{D0}=\varphi^{35}\left(1+{\delta_0\over\varphi}-\varphi^2\delta_0^3\right).
```

The external GeV value of `M_Z` is a comparison anchor, not a second D0 scale.  The Higgs-sector readout additionally requires a scalar projector and the runtime electroweak bridge.  Without that projector, a numerical Higgs or Yukawa comparison is not a core theorem.

### 04.7.1 The electron is the terminal calibration register because it is canonically selected, not assumed

The radial-depth readout above is dimensionless: every `λ` and every depth is a ratio against a zero of the EW score, never an eV value. That only closes if the matter book owns a *forced* base register against which those ratios are taken. The electron is the "unique terminal calibration register" not by convenience but because it is the object canonization itself selects — the **why** behind the fact.

**The electron is the minimal stable charged mode selected by canonization M1+ in the class `charge ≠ 0` [^b04-76].** Mass in CORE is the period of Π-canonization, `m(X) = τ(X)^{-1}` with `τ(X) = min{ n>0 : Π^n(X) ∼ X }` — the impedance of the shortest self-confirming cycle, not a substance (GOLDEN BOOK-III-SPECTRUM DEF 11.M.2–3, BOOK_01-owned period operator). Run that selector over the charged class. The charged class is nonempty (charge is a window-sector weight of the φ-quasicrystal hull, 04.4.7), so it has a canonization-minimal element: the mode with the shortest stable self-confirming cycle that still carries `charge ≠ 0`. That minimal charged mode is, by definition, the electron. There is no shorter charged cycle to calibrate against — anything shorter is uncharged — so the base register is forced, not nominated. The muon and tau are then *not* alternative bases; they are longer charged cycles built over this same base (Lucas-zone resonances `L_11+L_4`, GOLDEN BOOK-III-SPECTRUM THE 11.L.1, BOOK_03-owned), which is exactly why the charged-lepton transfer table freezes the electron at ratio `1/1`, exponent `0`. The electron-as-base freeze is backed by the finite charged-lepton transfer certificate.

**The electron mass index is the internal `α^{-1}` consistency index, not an eV input [^b04-77].** The dimensionless index of this minimal charged mode is fixed by the consistency condition for `α^{-1}`:

```math
m(e) \equiv \alpha^{-1}\quad\text{(internal index: mass as canonization frequency/period in CORE).}
```

This is canonically pinned by two independent expressions — a topological one and an algebraic one — agreeing to within the gluing anomaly

```math
\Delta_\alpha < \varepsilon^2,
```

so `α^{-1}` is over-determined, not fitted (GOLDEN BOOK-III-SPECTRUM REM 11.EM.2; the top/alg gluing lives in BOOK III CH III.2). The topological input is the three-zone scene capacity `N_paths = 9·11 + 11·13 + 13·9 = 359` (GOLDEN BOOK-III-SPECTRUM DEF 11.EM.1, the K(9,11,13) scene, BOOK_01-owned). The MeV/eV translation of `m(e)` is **not** a CORE theorem — it is a BRIDGE step (this book's runtime EW bridge), the same projector caveat that gates the Higgs/Yukawa readout above. **[^b04-75]** for the two-expression `α^{-1}` gluing as consumed here; the electron-as-base freeze is backed by the finite charged-lepton transfer certificate.

Consequence for this section: the EW radial depths `λ_Z^{D0}`, `λ_W^{D0}` and the depth-35 selection are ratios against a base register that M1+ forces, so "an alternative EW depth requires a changed EW radial score" tightens to — an alternative EW depth would have to move the *canonically selected* base, which is fixed by the same canonization that fixes the existence of charge. There is no free knob between the depth window and the electron register.
## 04.8 Charged leptons as a concrete finite variational selector family

The charged-lepton branch is controlled by a finite operator family rather than three free Yukawa constants. The active integration makes the finite terminal support explicit in Lean:

```text
D0.Matter.ChargedLeptonBranch = {electron, muon, tau}
D0.Matter.chargedLeptonBranchFiniteSupport
D0.Matter.chargedLeptonElectronTerminalClaim
D0.Matter.charged_lepton_terminal_no_free_alternative
```

The electron is now formally the unique terminal calibration register in the charged branch support.  Changing the terminal unit to `muon` or `tau` would require changing the terminal score functional; it cannot be done by a table rewrite.

### Why mass is not a free constant: the M1 mass contract

Before any coefficient row is read, M1 fixes what a "mass" is allowed to be [^b04-82].  The contract has three load-bearing clauses, and the operator-origin table below is downstream of all three:

1. **No hidden parameters (M1).** No physical constant is inserted by hand. Every mass number is read as an eigenvalue/integer of the `K(9,11,13)` scene (BOOK_01-owned), never as a tuned input.
2. **Constructivity.** Mass and motion are *not* properties of a substance. They are parameters of the algorithm that compresses the object's history into a reproducible identity. A lepton "mass" is a property of a canonization process, not of stuff.
3. **Inevitability target.** The contract is only discharged if the gross ratios — `m_μ/m_e≈206`, `m_p/m_e≈1836` — come out *forced*, not fitted.

This is the forcing behind the row: the operator-origin decimals encode the *result* of the contract, but the contract itself (mass = compression-algorithm parameter, under M1) is the reason the row is not a free knob.

### Mass as a canonization period (the load-bearing definitions)

The contract is made operational by a short definition chain.  These are the foundational objects the whole lepton mass derivation rests on; they carry verification obligations the operator-origin table does not.

**[DEF 04.8.M.1] History-compression operator `Π` [^b04-83].** Let `Π` be the operator that canonizes (compresses) an object's history to its minimal reproducible form.  `Π` is forced, not chosen: an object that survives M1 is exactly one that re-derives its own identity with no external catalog, so a canonization map must exist.

**[DEF 04.8.M.2] Internal period `τ` — the existence clock [^b04-84].** The self-confirmation cycle length is

```math
\tau(X) := \min\{\,n\in\mathbb N_{>0} : \Pi^n(X)\sim X\,\}.
```

`τ(X)` is the number of canonization ticks before the object returns to itself — its "existence clock". A state with no such finite `n` is not reproducible without an external rule and is killed by M1.

**[DEF 04.8.M.3] Mass index `m(X)=τ(X)⁻¹` [^b04-85].** Mass is the inverse canonization period:

```math
m(X) := \tau(X)^{-1}.
```

A short cycle (frequently re-confirmed identity) is heavy; a long cycle is light. This is the bridge from pure structure to a mass *number*, and it is what makes `m(e)≡α⁻¹` an internal index rather than an external eV input (the MeV/eV translation is BRIDGE, BOOK_04 runtime, not CORE).  The rest-frequency reading `ω₀:=τ(P)⁻¹` already used in 04.6 (THE 04.6.π.D) is this same identity.

**[LEM 04.8.M.5] Mass = cycle density [^b04-86].** `m(X)` is structurally identical to the density of stable closures `ϱ(X)` of the scene. Mass counts stable closures; nothing is added by hand.

**[THE 04.8.M.rest] Rest mass = internal winding [^b04-87]. [^b04-78].** At rest (`N_ext=0`) there is no external address increment, so the entire activity budget goes into the internal ID-cycle. Rest mass is therefore pure internal complexity — the winding count of the identity holonomy:

```math
m_{rest} = m_0\cdot W,
```

with `W` the memory winding number. There is no "substance" term: a leptonic rest mass is the number of times the canonization cycle wraps, and nothing else.  This is the structural definition of rest mass that the `τ`, `m=1/τ` chain above presumes.

### Why three copies: integer Lucas quantization

**[THE 04.8.L.0] Lepton/baryon copies are Lucas-quantized [^b04-88]. [^b04-79].** The reason the electron has copies `μ, τ` (and the baryon sector has heavy modes) is that in a discrete `φ`-graph the layer capacities cannot take arbitrary real values — they quantize *integrally* as Lucas numbers `L_n`. A non-integer layer capacity would need an external ruler to define the fractional part, ⊥M1. So the only admissible excitation capacities are `{L_n}`.  The signed Lucas *trace identity* `Tr(T^n)=(-1)^n L_n` and its uniqueness-of-projection forcing are owned by 04.0 (the Lucas-trace canonical integer projection, certified by existing finite certificates); the generation-count cutoff at `n=15` (the `9n` budget break) is owned by 04.4. What this section adds is the *mass-ratio* consequence of that same integer ladder.

### The muon ratio is forced additive, not fitted

**[THE 04.8.L.1] `m_μ/m_e = L_11 + L_4 + 2φ⁻²` [^b04-89]. [^b04-80].** The muon is an excitation localized in the memory zone (the torus, address 11). Its capacity is the Lucas number of layer 11, exactly and without rounding:

```math
L_{11} = \varphi^{11}+\psi^{11} = 199.
```

Any stable excitation must additionally be anchored to the reference addressing level (the base, address 4), whose capacity is

```math
L_4 = 7.
```

The minimal `Q(φ)` correction that introduces *no new parameter* is twice the internal step weight `b_0=φ⁻²` (the two internal rewrites enter/exit; no spin constant is imported). Hence the canonical integer predictor and its forced correction:

```math
\frac{m_\mu}{m_e} = L_{11} + L_4 + 2\,\varphi^{-2} = 206 + 2\varphi^{-2}.
```

The numerical readout `m_μ/m_e=206.77` in the BOOK_00 readout table is the *value* of this expression; this section gives the *why* — both why it is `199+7` and why the combination is additive.

**[THE 04.8.L.1.B] Impedance additivity forces additive mass-indices, not quadratic [^b04-90]. [^b04-81].** In CORE, "mass" is the impedance of a process: the minimal length (in `δ₀`-ticks) of the closed resonant cycle that must be realized for the state to be reproducible without external rules. Write `Z(γ):=Len(γ)` for the length of a closed path `γ` in the scene. If a process is a concatenation of two sub-cycles, `γ=γ_1∘γ_2`, then by the definition of length in a discrete graph

```math
Z(\gamma) = Z(\gamma_1) + Z(\gamma_2).
```

Therefore any composite excitation that must traverse two independent topological loops (here: "torus zone 11" `∘` "reference index 4") has impedance equal to the *sum* of the component impedances. This is exactly why

```math
m(P)/m(e) = Z(P)/Z(e) = (L_{11}+L_4+\dots)
```

is structurally inevitable: a *quadratic* combination would require an external metric — a rule of "channel orthogonality" — i.e. an external catalog, forbidden by M1. ⊥. The additivity is not an aesthetic choice; quadratic addition is killed by catalog-freeness.

### The operator-origin coefficient row (downstream of the above)

The generation action is still the origin of the internal ratios:

```math
M_\ell^{D0}=D_\ell^TG_R^+D_\ell+\kappa I.
```

The active candidate family is the three terminal charged branches

```math
\mathcal G_\ell=\{e,\mu,\tau\}.
```

The finite variational selector/action data are no longer an unowned coefficient table. The active charged-lepton coefficient owner is

```text
D0.Matter.ChargedLeptonCoefficientOrigin
D0.Matter.concreteChargedLeptonCoefficientOrigin
D0.Matter.charged_lepton_coefficient_origin_row_unique
D0.Matter.charged_lepton_coefficient_table_forced
D0.Matter.charged_lepton_coefficients_no_free_retuning
```

The selected finite coefficient row is the operator-origin row.  It carries

```math
r_e:r_\mu:r_\tau=1:3.8814328681047283:10.3183483253993735,
```

```math
p_e=0,\qquad p_\mu={1\over4},\qquad p_\tau={1\over3},
```

and the bridge-factor row `B_g` as a finite row function.  These entries are read from the selected coefficient origin; they are not free Yukawa constants and they are not inverted from external lepton masses.  By DEF 04.8.M.3, each `R_g` is a canonization-period index, not an eV input; the operator-origin decimals are the concrete realization of the Lucas-impedance ladder above (THE 04.8.L.1, THE 04.8.L.1.B). The signed `L_n` layer diagnostic is cross-checked by an existing finite certificate.

The generation action is still written as

```math
\mathcal S_{\ell,gen}[R]
=\sum_{g\in\mathcal G_\ell}\left(\log R_g-\log r_g-p_g\log A_{EW}-\log B_g\right)^2.
```

Stationarity gives

```math
R_g^{D0}=r_gA_{EW}^{p_g}B_g.
```

The theorem-level replacement is the no-retuning statement: at fixed `ChargedLeptonCoefficientOrigin`, changing any of `r_g`, `p_g` or `B_g` is an origin deformation, not a notation change and not a status update. A deeper spectral derivation of the decimal ratio values from a raw graph operator can still refine the origin, but the active Book 04 lepton row no longer has an independent coefficient knob — and, by the mass contract above, it never could: a free knob would be a hidden parameter (⊥M1).
## 04.9 Neutrino leakage sector

The neutrino sector is a neutral leakage representation.  Its internal support pattern is

```math
{M_\nu^2\over m_3^2}=\operatorname{diag}(0,\delta_0/4,1).
```

Hence

```math
{\Delta m_{21}^2\over \Delta m_{31}^2}=\delta_0/4,
\qquad
{m_2\over m_3}=\sqrt{\delta_0/4}.
```

This is not a three-neutrino mass fit.  If one external oscillation scale is supplied, D0 fixes the other splitting and the normal-order support sum under that bridge.

Neutrino is interpreted as neutral bulk phason wave / neutral leakage mode in
the theorem owner `D0.Matter.NeutrinoPhasonWaves`.  The active EM readout is
killed by `neutral_phason_wave_has_no_em_coupling`, while any IceCube
decoherence comparison belongs to the downstream passport layer
(a manifest-only scaffold cert that does not verify the beat law below).

### 04.9.1 Why oscillation exists at all: the seam beat [^b04-94]

The support pattern above states a splitting *ratio* but not *why the support oscillates*.  The generic two-mode beat structure (BOOK_09, `A_1 e^{iω_1 t}+A_2 e^{iω_2 t}`) does not by itself name the small parameter that sets the beat, which would leave oscillation as an external-scale assertion.  The forcing below names it and closes that gap.

**[THE 04.9.beat] Oscillation IS the beat of the two seam-evolution modes [^b04-95]. [^b04-91].**
The whitening constant `α^-1` has two forced, independent writings — the topological reading `α_top` (off the discrete scene/channel count) and the algebraic reading `α_alg` (off the continuous packing/`π_0` phase).  These are not two numbers but two *evolution modes on the same seam*: a leakage mode that does not carry an active EM readout cannot pick one writing over the other, so it propagates as both at once.  A state propagated under two co-present mode frequencies does not relax to one — it beats.  Neutrino oscillation is that beat, not an added oscillator.

**[LEM 04.9.beat.Δα] The beat small parameter is the gluing anomaly `Δα` [^b04-96]. [^b04-92].**
The detuning between the two seam modes is exactly the irreducible residue between their two writings,

```math
\Delta_\alpha:=\bigl|\alpha_{top}^{-1}-\alpha_{alg}^{-1}\bigr|,
```

owned and derived in BOOK_02 §02.13 [^b04-97] — cited here, not re-derived.  `Δα≠0` is forced: by THE 61.10 (Gluing-Anomaly Engine) full relaxation of a closed system to a single mode would require an external catalog, which M1 forbids; the smallest catalog-free arena `Q(φ)` that holds both writings does not flatten the seam.  A nonzero seam that cannot relax is precisely a residual two-mode dynamic — the seed of the leakage sector's evolution.

**[COR 04.9.beat.f] Beat / modulation frequency `∝ Δα` [^b04-98]. [^b04-93].**
For a carrier `f_c` driven at the two modes `f_c` and `f_c(1+Δ)`, the beat law gives `f_beat=Δ·f_c`.  Setting the detuning to the forced residue `Δ=Δα`,

```math
f_{mod}=\Delta_\alpha\,f_c,
```

so the neutrino modulation/oscillation frequency is `∝ Δα` — a CORE consequence with no fitted oscillator.  This is the *dynamics* (the rate of the beat); the *amplitude/mass scale* of the same seam is the separate, mass-side reading `m_ν ∝ Δα²` owned by 04.4.9 [^b04-99].  Both are the one seam `Δα` read once as a frequency (this section) and once as a squared mass (04.4.9); they are not two assumptions.

Sign note: only `|Δα|` enters the beat rate.  The linear sign of `Δα` is not observable, so any probabilistic/ordering weight built on it (e.g. a sterile-leakage weight) is a typed BRIDGE/HYP layer, consistent with BOOK_02 §02.13 COR 16.3.5.

### 04.9.2 What this fixes vs. what stays external

The support ratio `Δm²_{21}/Δm²_{31}=δ_0/4` and the bridge "one external oscillation scale fixes the rest" are unchanged.  What 04.9.1 adds is the *mechanism* under that bridge: the leakage mode oscillates because the seam carries two co-present whitening modes whose forced detuning `Δα` cannot relax to zero, and the beat frequency is `∝ Δα`.  Until the beat cert is written, [THE 04.9.beat] / [LEM 04.9.beat.Δα] / [COR 04.9.beat.f] carry an open cert obligation; the IceCube comparison remains downstream in the passport layer.
## 04.10 CKM as finite basis origin, not a free matrix

### Arity first: the CKM parameter count is forced, not assumed

Before the matrix is anything, its *shape* is fixed by the scene K(9,11,13) (scene owned by BOOK_01). The forcing runs through the interface graph of the scene, not through any fit.

Generations are not a free triplet — they ARE the inter-zone interfaces of the three-shell scene:

```text
I_12 = (9,11),  I_23 = (11,13),  I_13 = (9,13).
```

Take the interface graph: vertices = interfaces, an edge joins two interfaces that share a zone. That graph is K_3 (each interface shares one of {9,11,13} with each other). Two structural numbers fall out with no parameter:

```text
#interfaces = 3                       -> exactly 3 mixing angles
cyclomatic rank K_3 = E - V + 1
                    = 3 - 3 + 1 = 1   -> exactly 1 irreducible holonomic (CP) phase
```

Status: THE (structural). This recovers the observed CKM arity (3 Cabibbo-Kobayashi-Maskawa angles + one delta_CP) and moves the *count* of mixing parameters from "free" to forced [^b04-100].

A fourth generation is then not merely "not observed" — it is forbidden by contradiction. Under the forcing-by-contradiction schema (DEF 0.2.2):

```text
4th generation  => 4th interface
                => 4th zone
                => 4th structural necessity beyond {defect, memory, shell}
                => operationally distinguishable => new role
                => external catalog => bottom M1.
```

Status: NO-GO (by contradiction, DEF 0.2.2). Four generations are forbidden: the fourth interface would demand a structural role outside the closed alphabet {defect, memory, shell} (alphabet owned by BOOK_01), which is only nameable from an external catalog, which contradicts M1 [^b04-101]. The arity (3 angles, 1 phase, 3 generations) is therefore a scene fact, not a phenomenological choice.

This is an *arity* closure only: it fixes how many angles and phases exist and forbids a fourth generation. It does NOT pin the numerical angles, the CP phase value, or RG-dressed passport entries — those remain downstream of the external convention/RG/readout layer (see the closing scope note).

### CKM <-> PMNS hierarchy inversion is rank-nullity, zero parameters

The same scene that fixes the arity also explains, with zero free parameters, one of the standing unexplained facts of the Standard Model: why quarks mix *weakly* and leptons mix *strongly*. The split is rank-nullity of the scene adjacency operator A (rank(A)=3, nullity=30; the bare rank/nullity bookkeeping is owned by BOOK_01 and BOOK_03 — here it is the load-bearing flavor statement, not gauge bookkeeping):

```text
quark currents  -> active sector: 3 non-degenerate modes (21.84, -9.76, -12.08)
                -> hierarchy SUPPRESSES mixing  => CKM small.

neutrinos       -> sterile archive: kernel 30-fold degenerate
                -> degeneracy PERMITS any rotation => PMNS large.
```

Status: THE (zero-parameter). Strong lepton mixing vs. weak quark mixing is a consequence of the rank-3 / nullity-30 split of the scene, with no fitted parameter: a non-degenerate spectrum forces a hierarchical (Fadeev-N / FN-style) basis whose overlaps are small, while a 30-fold degenerate kernel is rotation-invariant, so its diagonalizing basis is unconstrained and the overlap is generically large [^b04-102]. The CKM-side reading: CKM is small *because* the up/down bases below sit in the non-degenerate active sector — smallness is inherited from the spectrum, not imposed.

### The two-step finite object

CKM is not introduced as a phenomenological matrix.  It is a two-step finite object:

```text
finite up-basis candidate family + score
finite down-basis candidate family + score
-> strict up/down basis selections
-> coordinate mismatch matrix between the selected bases.
```

The internal orientation operator remains the algebraic seed for the candidate family:

```math
O_{cyc}=O_I+O_J+O_K
=
\begin{pmatrix}
0&1&-1\\
-1&0&1\\
1&-1&0
\end{pmatrix}.
```

The canonical internal seed is

```math
T_{CKM}^{D0}=O_{cyc}G_R^+D_{PNO},
```

and the address orientation is

```math
U_{addr}=\operatorname{polar}(O_{cyc}G_R^+D_{PNO}).
```

The owner `D0.Matter.CKMBasisOrigin` moves the proof one level upstream. The up and down bases are not silent inputs: each is a strict finite variational selector output. The theorem `ckm_origin_candidate_matrix_unique` says that any admissible origin candidate using the same finite-basis variational selectors returns the same matrix. The theorem `ckm_no_free_matrix_at_fixed_basis_origin` forbids a second matrix at fixed basis origin.

The generation-overlap layer now has a smaller D0-origin owner.  The active source is no longer an unexplained path `0-1-2`: `D0.Geometry.TorusCore13GeometryOrigin` supplies the three torus shell boundaries and proves that radial shell hopping does not commute with shell phase/radius drift.  Lean checks

```text
[A_radial, D_phase]_(0,1) = minor radius != 0
```

and `D0.Matter.GenerationOverlapResponseOrigin` records the corrected overlap interface:

```text
O_ij = |(U_up^H U_down)_ij|^2
IsPermutationWitness O := exists sigma : Equiv.Perm GenCarrier, ...
```

Thus the algebraic source of non-permutation overlap is torus shell noncommutativity, not a fixture matrix.  The finite certificate checks the resulting shell-induced unistochastic response, rejects all full permutation witnesses, finds a multi-support row and verifies `F_fl^T F_fl` positivity.  This is an algebraic origin closure, not a derivation of physical CKM entries, angles, CP phase or RG-dressed passport values.

Therefore a different CKM matrix means one of the following has changed:

```text
up-basis candidate family or score;
down-basis candidate family or score;
coordinate/readout convention;
external RG/radiative bridge;
phase/permutation quotient.
```

It is not an internal free parameter and it is no longer merely a matrix theorem after hand-picked bases.  What remains open is narrower: the physical CKM passport must evaluate the frozen origin object without post-hoc permutation, with concrete physical score terms declared before comparison, and any comparison to observed CKM entries must still pass through the external convention/RG/readout layer.

## 04.11 SM-facing finite gauge decomposition

The matter/gauge row is no longer allowed to say merely that D0 has an anomaly-compatible representation. The active object is a finite gauge-decomposition ledger:

```text
D0.Gauge.FrozenSMGaugeDecomposition
D0.Gauge.frozenSMGaugeDecomposition
D0.Gauge.frozen_sm_gauge_factors_closed
D0.Gauge.frozen_sm_generation_ledger_closed
D0.Gauge.frozen_sm_generation_anomaly_free
```

The theorem chain is now:

```text
finite gauge carrier labels
-> frozen factor ledger [SU(3), SU(2), U(1)]
-> one-generation Weyl ledger
-> exact rational anomaly cancellation
-> no alternative factor ledger at the same frozen decomposition
-> SM/EFT bridge only after the finite ledger is frozen.
```

The anomaly equations are exact finite rational equalities:

```math
\sum Y=0,
\qquad
\sum Y^3=0,
\qquad
SU(2)^2U(1)=0,
\qquad
SU(3)^2U(1)=0.
```

The no-free-decomposition owners are:

```text
D0.Gauge.no_alternative_sm_factors_at_frozen_ledger
D0.Gauge.no_alternative_sm_generation_ledger_at_frozen_decomposition
D0.Gauge.sm_eft_bridge_requires_frozen_decomposition
D0.Gauge.frozen_sm_eft_bridge_boundary_closed
```

Therefore the SM-facing gauge sentence is not a smooth-field assertion and not a fitted Standard-Model import.  The finite core owns only this ledger:

```text
factor list: SU(3), SU(2), U(1);
one-generation Weyl ledger: Q_L, u_R^c, d_R^c, L_L, e_R^c, optional nu_R^c;
exact anomaly sums: zero;
bridge boundary: QFT/EFT running and collider observables attach only after freeze.
```

A different gauge factor list or a different one-generation ledger is not a second core solution under the same owner.  It is a new carrier attempt and must be routed to a separate theorem/no-go/bridge target.  This closes the weaker old reading where `SU(3)×SU(2)×U(1)` could look like a name attached after the fact.

This still does not prove the full Standard-Model Lagrangian from first principles.  What is closed is the finite carrier/representation/anomaly skeleton and the rule that the SM/EFT bridge cannot alter it.  The remaining work is stronger: derive the representation ledger itself from the lower D0 matter-operator origin and then evaluate running couplings/masses as external transfer, not as core knobs.

## 04.12 QCD runtime and confinement grammar

The QCD line is controlled by the action section and archive runtime; it is not a new fitted scale.  A hadronic comparison may use

```text
finite color/support operator
-> QCD runtime/archive scale
-> spin/flavour/chiral transfer
-> declared comparison convention.
```

No row may read a graph eigenvalue directly as a PDG hadron mass.  In particular:

```text
support gap -> mass
```

is forbidden unless the transfer operator and unit section are already fixed.

## 04.13 Baryon support and nucleon readout

The baryon support is the 2-simplex Hodge sector.  The certified support is

```math
\lambda_{B2}=3960.
```

The active nucleon core is

```math
\lambda_{N-core}=2640.7985901288725.
```

The active real-closure pass makes the proton and neutron readout finite variational selectors full-support finite objects, not local windows. The proton terminal destructive readout is owned by

```text
D0.Matter.protonReadout306FullSupportClaim
D0.Matter.proton_readout306_full_support_no_free_alternative
```

The admissible terminal readout support is the complete finite support `0..612`, represented in Lean as `Fin 613`, and `306` is the unique zero-residual candidate over that whole support.  Therefore the terminal cost

```math
\Delta_{readout}^{306}=18\cdot17=306
```

is no longer only a mnemonic in the prose; under the fixed finite variational selector, no alternative readout is admissible without changing the score.

The proton row is the terminal-destructive readout

```math
\lambda_p^{D0}=\lambda_{N-core}-306=2334.7985901288725.
```

The action-section comparison gives

```math
m_p/m_e=38\sqrt{\lambda_p^{D0}}.
```

The neutron is the beta/archive sibling.  This is now owned by

```text
D0.Matter.neutronArchiveSiblingClaim
D0.Matter.neutron_archive_sibling_no_free_alternative
```

The finite sibling window distinguishes the proton line, the beta/archive sibling and a neutral-leakage-only alternative.  The neutron branch is selected as the beta/archive sibling, not as an independent fitted mass.

```math
\lambda_n^{D0}=\lambda_p^{D0}+2\sqrt{10}+\delta_0.
```

The beta unlock depth is also now a full-support finite variational selector owner:

```text
D0.Matter.betaUnlockDepth19FullSupportClaim
D0.Matter.beta_unlock_depth19_full_support_no_free_alternative
```

The admissible weak-unlock support is the complete finite support `0..38`, represented in Lean as `Fin 39`, and depth 19 is the unique zero-residual unlock branch over that whole support.  The beta unlock parameter is

```math
\epsilon_\beta^{D0}=\sqrt{\lambda_n^{D0}}-\sqrt{\lambda_p^{D0}}-{1\over38}.
```

The lifetime law used by the certificate is

```math
\Gamma_n^{D0}\tau_0=(\epsilon_\beta^{D0})^5\delta_0^{19}q_{mass}^{14}.
```

The proton and neutron rows are therefore single-section terminal readouts with full-support finite variational selector owners.  Measured masses and lifetimes are benchmarks, not inputs.

### 04.13.1 Full-support replacement of local finite variational selector windows

Earlier drafts used nearest-neighbour windows such as `{305,306,307}` and `{18,19,20}` as a quick anti-retuning check. Those windows are no longer the active theory. The active owners are:

```text
D0.Matter.Book04FullSupportSelectors
D0.Matter.electroweakDepth35FullSupportClaim
D0.Matter.protonReadout306FullSupportClaim
D0.Matter.betaUnlockDepth19FullSupportClaim
```

The electroweak radial depth is selected over `Fin 71`, the proton destructive readout over `Fin 613`, and the beta weak-unlock depth over `Fin 39`.  Therefore a critic cannot move the selected value by leaving the local ±1 window while keeping the same finite residual finite variational selector.  Any different value requires a different admissible support or a different score functional, hence a different theory object.

## 04.14 Baryon 40/56 carrier and anonymous pole scaffold (closed)

The baryon 40/56 spin-flavour carriers and anonymous pole scaffold on the image basis are closed (SPIN-FLAVOUR-CARRIER-CERTIFIED + BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED). The frozen operator family proves the internal carriers and poles. External PDG naming, masses, widths and spectroscopy remain passport-layer work only. The decuplet carrier has a constructive finite owner:

```text
D0.Matter.BaryonS3Symmetrizer
D0.Matter.baryon_triple_carrier_card
D0.Matter.sorted_triple_card_eq_ten
D0.Matter.antisymmetric_line_annihilated_by_s3_symmetrizer
D0.Matter.BaryonMultipletOperator
D0.Matter.CanPromoteBaryonMultiplet
D0.Matter.baryon_multiplet_requires_spin_flavour_decuplet_operator
D0.Matter.nucleon_line_cannot_promote_full_baryon_multiplet
```

The 10D symmetric carrier / decuplet-candidate carrier is not the rank-one invariant sector of a 3-dimensional
vertex representation.  It is the S3-symmetric sector of the tensor carrier

```text
BaryonTripleCarrier := Fin 3 x Fin 3 x Fin 3
```

so the ordered carrier has dimension `27`, and the sorted-orbit representatives
have cardinality `10`.  This is the finite 10D symmetric carrier / decuplet-candidate carrier; it is not a QCD,
PDG or mass-spectrum claim.

The required typed operator must contain, before comparison,

```text
spin resolution;
flavour resolution;
S3 10D symmetric carrier / decuplet-candidate carrier closure;
transfer window for unstable-resonance comparison.
```

The active nucleon operator is deliberately the `nucleonLineOnlyBaryonOperator`.
The theorem

```text
nucleon_line_cannot_promote_full_baryon_multiplet
```

says that this operator cannot be re-read as a full baryon multiplet.  The
finite reason is that an antisymmetric line sector is annihilated by the S3
symmetrizer, while the 10D symmetric carrier / decuplet-candidate carrier is fully symmetric.  Therefore the
previous direct `Delta, Lambda, Omega` formula flow is not merely “not
certified”; it is blocked under the present operator family.  A numerical
agreement with PDG resonance masses cannot supply the missing operator.

## 04.15 Meson/chiral boundary as a closed no-go

Mesons are phason domain walls on the 1-cochain sector. The lower-Hodge value \(400\) is the minimal eigenvalue of the generation-blind domain-wall tension operator and constitutes a support seed, not a physical mass. Meson masses and widths are read only after the typed edge-generation transfer operator

\[
\mathcal{C}_{\chi FV}^{D0}
=
\Pi_M
\Bigl(
\operatorname{liftEdge}(L_M)
+
\operatorname{liftEdge}(\Gamma_\chi^\dagger\Gamma_\chi)
+
\operatorname{liftGen}(F_{fl}^\dagger F_{fl})
+
\operatorname{liftEdge}(V_{sp}^\dagger V_{sp})
\Bigr)
\Pi_M
\]

is frozen on the carrier \(\mathrm{Fin}\ E\times \mathrm{Fin}\ Gen\).

The flavour defect enters exclusively through the typed \(\operatorname{liftGen}\) term. Mismatched Gen×Gen blocks added to an Edge×Edge operator are forbidden. Spectral gaps of the resulting frozen operator must carry \(K_0\) gap labels before any external comparison protocol is invoked. Direct promotion of the bare \(400\) seed to pion, kaon, or rho masses is prohibited. Symbolic guard: 400\not\Rightarrow m_\pi.

The meson/chiral transfer algebra is closed at the finite typed-operator level.
External meson spectroscopy remains a K0-labeled passport layer.

(The previous "closed no-go" framing for 04.15 is superseded by the positive finite closure above. The mathematical carrier and lift operators remain as previously stated.)

### 04.15.1 Higgs scalar projector closure

D0 closes the Higgs scalar projector operator boundary by freezing a scalar doublet subcarrier \(\mathcal H_\phi\cong\mathbb C^2\). On this carrier, the FrozenSU2-compatible generators \(X\) and \(Z\) have scalar commutant. Any positive idempotent \(P\) supported on this doublet and commuting with both \(X\) and \(Z\) must be either \(0\) or \(I_2\). The nonzero scalar section therefore has the unique gauge-compatible projector \(P_\phi=I_2\), with rank \(2\).

Rank-1 projectors break FrozenSU2 compatibility. Rank \(>2\) projectors require an extra multiplicity selector and would introduce an additional scalar degree of freedom unless explicitly killed. The certified scalar projector adds the Yukawa section without introducing a second action scale; \(\Lambda_{\rm act}\) remains the only dimensional action section.

The Higgs scalar projector operator boundary is closed at the finite projector level. Yukawa numerical comparison remains a transfer/passport layer.

### 04.CVFT.Higgs-Yukawa section transfer

The Yukawa section is a finite off-diagonal block operator \(Y:\mathcal H_R\to\mathcal H_L\otimes\mathcal H_\phi\) compatible with the certified scalar projector:
\[
P_\phi Y=Y.
\]
Equivalently, the full block operator
\[
\mathcal Y=
\begin{pmatrix}
0&Y^\dagger\\
Y&0
\end{pmatrix}
\]
is Hermitian on the finite left-right-scalar carrier. Yukawa coefficients are dimensionless; the only dimensional scale remains \(\Lambda_{\rm act}=38m_ec^2\). No second mass anchor is introduced.

## 04.16 Higgs scalar projector + Yukawa section (closed)

Higgs scalar projector is SCALAR-PROJECTOR-CERT-CLOSED (rank-2 FrozenSU2-compatible). Higgs-Yukawa section is YUKAWA-SECTION-CERT-CLOSED (finite block map compatible with the projector, no second mass anchor). The remaining work is numerical Yukawa passport / PDG comparison only. Legacy "missing" language is retired.

## 04.17 Photon scattering and finite resolution comparisons

The mature restricted benchmark is

```math
e^+e^-\to\gamma^*\to\mu^+\mu^-.
```

The photon-only integrated cross section has the form

```math
\sigma^{(n)}(s)=
{4\pi\alpha_{top}^2\over3s}\beta_\mu
\left(1+{2m_\mu^2\over s}\right)(D_e^2)^n.
```

This is a restricted tree-level support/probe/runtime/bridge chain.  It does not include `Z` exchange, loops, event selection, detector cuts or a full collider likelihood.

Baryon DIS/PDF readouts are finite-resolution responses of the baryon support sector:

```math
f_i^{D0}(\lambda,u)=
{\langle\psi_{bar}|\Pi_i\Pi_{B,2}(\lambda)e^{-uL_{B,2}}|\psi_{bar}\rangle
\over
\sum_j\langle\psi_{bar}|\Pi_j\Pi_{B,2}(\lambda)e^{-uL_{B,2}}|\psi_{bar}\rangle}.
```

They become collider PDFs only after a declared external sampling and scheme protocol.

## 04.18 External carrier and string/F-theory comparison

External string or F-theory data are not a foundation for D0.  They are comparison carriers tested by D0 filters:

```text
external carrier data
-> finite verification scale freeze
-> condensed/profinite admissibility check
-> chiral/orientation comparison
-> terminal-lift comparison.
```

The internal D0 target is a finite orientation/generation index.  The external construction is useful only if it realizes the D0 admissibility filter without adding hidden scales or fitted flux choices.  It cannot choose D0 signs, multiplicities or mass readouts.

## 04.19 Claim classification for the active matter book

The D0 matter sector distinguishes a bare finite invariant from a dressed comparison value.

```math
O_{D0}^{bare}\in \operatorname{Obs}_{D0}^{finite}.
```

A comparison value is

```math
O_{SM}^{\mathsf S}(\mu)
=
\mathfrak D_{SM}^{D0}(\mathsf S,\mu,\Lambda_{act})
[O_{D0}^{bare}].
```

The dressing functor must declare:

```text
scheme;
scale;
field content;
beta functions or anomalous dimensions;
threshold conventions;
external table or observable;
forbidden adjustable parameters;
falsification hook.
```

New particles, hidden thresholds, hidden dark-sector fields or fitted beta-function changes are forbidden.  If a comparison requires them, the bridge fails; the core D0 object does not mutate.

## 04.20 Claim classification for the active matter book

The active matter book uses the following classification.

| Sector | Active reading |
|---|---|
| photon | massless line carrier; core readout |
| charged leptons | finite variational selector/action family; external mass comparison after electron section |
| neutrinos | neutral leakage support; one-anchor oscillation bridge only |
| CKM | finite up/down basis-origin finite variational selectors; D0 ordinal/adjacency generation finite variational selectors force noncommuting overlap origin; no free matrix at fixed origin; numerical passport remains downstream |
| generation multiplicity | finite three-generation theorem |
| anomaly behavior | finite anomaly-preservation theorem |
| electroweak ratio | finite radial/runtime comparison; Higgs/Yukawa core promotion blocked until scalar projector bridge is supplied |
| proton/neutron | terminal-destructive and beta/archive readouts; benchmarks not inputs |
| full baryon multiplet | S3 tensor 10D symmetric carrier / decuplet-candidate carrier exists; current nucleon-line operator is still blocked from full multiplet promotion | masses and unstable-resonance comparison require spin/flavour transfer and external passport |
| mesons | typed edge-generation defect-transfer algebra exists; lower-Hodge seed alone is internally degenerate and blocked | physical pion/kaon/rho masses require transfer window and external comparison |
| SM/EFT numbers | dressed comparison values, not core theorems |
| external carrier models | admissibility comparisons, not foundations |

## 04.21 Falsification rules

A Book 04 claim fails if any of the following occurs:

1. a mass/mixing number is obtained by direct support reading without a transfer operator;
2. a finite variational selector output changes without a declared score deformation;
3. a CKM matrix is altered while the basis-origin finite variational selectors and readout are held fixed, or a row-only permutation witness is used instead of an `Equiv.Perm` column permutation;
4. a Standard-Model comparison uses hidden fields, hidden thresholds or post-hoc scheme choices;
5. a hadron row uses PDG data to select the D0 operator;
6. a meson row promotes `400` directly to a physical mass;
7. a baryon row promotes the nucleon-line operator to a full multiplet without spin/flavour/S3 10D symmetric carrier / decuplet-candidate carrier data;
8. a Higgs/Yukawa row uses a second mass anchor before the scalar projector is supplied;
9. an external carrier comparison is used as a D0 axiom.

## 04.22 Remaining matter operator frontiers (release-candidate)

All internal carriers, projectors, and typed operators for baryon 40/56 + anonymous poles, meson transfer, Higgs scalar projector, and Yukawa section are closed at the finite level (see closure classes in Book 05).

Remaining work is exclusively external numerical spectroscopy / Yukawa / PDG comparison (passport-layer only). No internal operator is missing.

1. Charged lepton / alpha: coefficient-origin trace/residue theorem target remains (EDGE-TRACE-COEFFICIENT-TARGET guardrail).
2. CKM: physical convention/RG passport remains.
3. Baryons: carrier + spin/flavour + anonymous pole scaffold closed (image-basis). External PDG passport remains.
4. Mesons: typed transfer operator closed. External K0-labeled spectroscopy passport remains.
5. Higgs/Yukawa: scalar projector + finite block closed. External numerical passport remains.
6. SM decomposition: refine lower operator origin for nearby finite decompositions.
7. Edge-alpha and lepton ramification: theorem targets only (EDGE-TRACE-COEFFICIENT-TARGET, TORUS-RAMIFICATION-TARGET). Guardrails; no numerology or fit claims.

## 04.23 Selector closures now owned by finite operators

The correction pass removes half-closures from the active matter book.

### 04.23.1 Charged-lepton mass transfer is now downstream of the coefficient origin

The charged-lepton block is no longer allowed to stop at "the coefficient row is frozen". The finite row must feed a branch-wise transfer object: `D0.Matter.ChargedLeptonMassTransfer`. These entries are read from the selected coefficient origin, and the theory no longer has an independent coefficient knob.

### 04.23.2 CKM has a frozen finite transfer before external comparison

The CKM block is no longer only "basis finite variational selectors determine a matrix". The finite matrix now has a downstream frozen transfer owner: `D0.Matter.FrozenCKMMatrixTransfer`. A passport may compare the matrix; it cannot choose or retune it.

### 04.23.3 Higgs/Yukawa is decided, not left ambiguous

Positive Higgs/Yukawa promotion has only one admissible form: `D0.Matter.HiggsYukawaCorePromotion`, carrying `D0.Matter.HiggsScalarProjectorCertificate`. A constructive scalar projector closure is mathematically required.

## 04.24 Final finite variational selector-origin closures

The finite variational selector-origin layer is locked. The active closures and certificates are:

- **Charged-Lepton Coefficient**:
  - `D0.Matter.ChargedLeptonCoefficientOrigin`
  - `D0.Matter.concreteChargedLeptonCoefficientOrigin`
  - `D0.Matter.charged_lepton_coefficient_no_free_row_alternative`
  - `D0.Matter.charged_lepton_coefficients_no_free_retuning`
  - `D0.Matter.charged_lepton_coefficient_table_forced`
  - These entries are read from the selected coefficient origin. The theory no longer has an independent coefficient knob.

- **CKM Exact Matrix**:
  - `D0.Matter.CKMExactMatrixCertificate`
  - `concrete_ckm_matrix_entries_closed`
  - `frozen_ckm_exact_matrix_closed`
  - `ckm_no_free_matrix_at_fixed_bases`
  - `D0.Matter.StrictSelectorCertificate`
  - `D0.Matter.book04_finite variational selector_claim_no_free_alternative`

- **Constructive Scalar Projector & SM Action**:
  - `D0.Matter.HiggsScalarProjectorConstructive`
  - `D0.Gauge.SMScalarActionCompletion`
  - `sm_minimal_scalar_action_terms_closed`
  - `sm_scalar_completion_preserves_frozen_base`
  - `sm_scalar_completion_projector_rank_two`

- **Operator Boundaries** (release-candidate closure classes):
  - Baryon 40/56 + anonymous poles: SPIN-FLAVOUR-CARRIER-CERTIFIED + BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED
  - Meson: MESON-TYPED-TRANSFER-CERT-CLOSED
  - Higgs: SCALAR-PROJECTOR-CERT-CLOSED + YUKAWA-SECTION-CERT-CLOSED
  - Edge alpha / ramification: EDGE-TRACE-COEFFICIENT-TARGET + TORUS-RAMIFICATION-TARGET (theorem targets; not closed)
  - All external numerical / PDG / spectroscopy work: PASSPORT-LAYER only.

## 04.T Torus/Core13 Matter Integration Boundary

The three-generation carrier is now sourced by the D0 memory-torus shell geometry. `D0.Geometry.TorusCore13GeometryOrigin` proves that radial shell hopping and shell phase/radius drift do not commute; `GenerationSelectorOrigin` and `GenerationOverlapResponseOrigin` use that fact as the source of non-permutation flavour overlap.

For mesons, the lower-Hodge `400` seed remains only a support seed. The new flavour-defect route is:

```text
torus noncommuting shell finite variational selectors
-> torus_geometry_forces_generation_finite variational selector_noncommute
-> torus_shell_noncommutativity_forces_nonpermutation_overlap_source
-> F_fl
-> F_fl^T F_fl positive defect transfer
```

The Lean owners are now explicit: `D0.Matter.CKMNontrivialFlavourAlgebra` proves `overlap_response_can_force_nonpermutation_transfer` and `nontrivial_flavour_defect_positive_response`; `D0.Matter.MesonDefectTransferOrigin` proves `meson_support_projector_idempotent` and `meson_positive_defect_transfer_admissible` on the typed `Edge x Generation` carrier.

For baryons, the 10D symmetric carrier / decuplet-candidate carrier is not a nucleon-line extension. It is the S3-symmetric triple sector over the three torus shell roles; the Lean owner `BaryonS3Symmetrizer` exposes `BaryonTripleShellCarrier` and `baryon_triple_shell_card_eq_27`.

For Higgs/Yukawa, the scalar projector is connected but not identical to torus geometry. Torus shell radius is not a Higgs VEV, torus aspect ratio is not a Higgs mass, and radial hopping/phase drift are not the scalar projector. The scalar projector remains the minimal positive idempotent matter-transfer bridge compatible with tick/Lorentz and the frozen gauge ledger.

Constructive Scalar Projector Closure: `FrozenSU2_X` and `FrozenSU2_Z` force
the admissible scalar projector to have form `P=aI`; its trace-rank is 2. Torus
radius is not Higgs VEV, and torus aspect is not Higgs mass. Torus radius is not Higgs VEV.

## 04.V Nuclear shell-contact SRC operator

Nuclear shell-contact SRC operator.

Matter as phason/window defects of the φ-quasicrystal vacuum: generations =
inflation classes, quark color/charge = window-sector weights, and chirality =
acceptance-window offset.

Short-range nucleon pairing is not promoted from nuclear mass, density, or neutron-proton imbalance. The D0 object is a finite shell-contact readout operator. This is an operator bridge, not just an empirical note:

```math
\mathcal C^{D0}_{SRC}(A)
=
\operatorname{Tr}\!\left(
P_p^{shell}\,
\mathcal W_J^{D0}\,
P_n^{shell}\,
(\mathcal W_J^{D0})^\dagger
\right).
```

Here `P_p^shell` and `P_n^shell` are occupied proton and neutron shell projectors, and `W_J^D0` is the angular-momentum contact finite variational selector.

In the diagonal shell-occupation approximation the readout is the Shell Contact Index:

```math
\mathrm{SCI}_{D0}(A)
=
\sum_{\alpha=(n,\ell,j)}
\omega_\alpha
\frac{p_\alpha n_\alpha}{2j_\alpha+1}
+
\delta_0
\sum_{\alpha\ne\beta}
\omega_{\alpha\beta}
\frac{p_\alpha n_\beta}{\sqrt{g_\alpha g_\beta}}.
```

The first term is same-shell SRC contact. The second term is cross-shell leakage and is suppressed by `delta0`.

The CaFe witness is structural:

```text
Ca40: closed core.
Ca48/Ca40: add eight neutrons in the outer shell without matching outer-shell protons;
same-shell contact increment = 0, only suppressed leakage remains.
Fe54/Ca48: add six protons into the same outer shell as the eight neutrons;
same-shell proton-neutron overlap turns on strongly.
```

For an `f_{7/2}`-type shell with `g=2j+1=8`:

```math
\Delta \mathrm{SCI}^{same}_{Ca48-Ca40}=\frac{0\cdot 8}{8}=0,
\qquad
\Delta \mathrm{SCI}^{same}_{Fe54-Ca48}=\frac{6\cdot 8}{8}=6.
```

Thus SRC enhancement is controlled by same-shell proton-neutron overlap, not by added neutron count or mass count.

Lean owner: `D0.Matter.NuclearShellContactSRC`.

Core theorems:

```text
same_shell_contact_index_zero_for_unmatched_valence_protons
same_shell_contact_turns_on_for_matched_valence_pn
src_contact_requires_shell_projector_overlap
nuclear_shell_contact_src_closure
```

No-go theorems:

```text
mass_number_alone_cannot_determine_src_contact
neutron_excess_alone_cannot_determine_src_contact
```

The finite certificate checks the frozen CaFe shell-contact witness; Nature 2026 source-data comparison is an external passport and may only run from a pinned manifest.

Current external-data runner result:

```text
PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026
```

The Nature 2026 source-data XLSX files are pinned in the manifest. The external
run reads Source Data Fig. 2 and Fig. 3 and returns:

```text
Ca48/Ca40 = 1.097
(weighted_mean numerical detail moved to passport results manifest)

Fe54/Ca48 = 1.493
(weighted_mean numerical detail moved to passport results manifest)
```

The observed ordering is `Fe54/Ca48 > Ca48/Ca40`; the A-only, N/Z-only and
density-only scalar controls fail this shell-contact ordering.



### 04.CVFT.Gauge-boundary commutator obstruction

D0 defines the confinement sector law as a retained/traced boundary obstruction. For abelian phase modes whose generator preserves the retained sector, \([P_N,g_{U(1)}]=0\), the boundary leakage \(Q_Ng_{U(1)}P_N\) vanishes. For non-singlet color modes the generator does not preserve the retained/traced cut, and the feedback-return quadratic form is
\[
\langle\psi,F_N\psi\rangle
=
\|Q_NU_NP_N\psi\|^2.
\]
The internal lower-bound target is
\[
\langle\psi_{color},F_N\psi_{color}\rangle\ge m_{gap}^2\|\psi_{color}\|^2.
\]
This is the D0 gauge-boundary law: non-singlet states lack terminal stable poles when their boundary leakage is bounded away from zero. Continuum Yang-Mills comparison remains a bridge/passport layer.

### 04.CVFT.Edge-sector electromagnetic coefficient target

The edge-sector electromagnetic normalization is cert-closed via explicit unitary dilation and seam operator. The edge alpha trace is cert-closed.

The required finite object is \(F_E = P_E U_E^\dagger Q_E U_E P_E\) on the 359-edge 1-skeleton of \(K(9,11,13)\), with seam correction \(S_{\rm seam}\).

Lepton ramification cover is cert-closed as an algebraic cover (SymPy-exact C4/R3). The companion cover is a finite spectral-cover extension attached to the edge resolvent. It is not a claim that the 359-edge Hilbert space itself has dimension 359+4+3. The 4-cycle and 3-cycle blocks encode terminal role capacity and scene-rank holonomy sheets.

Derivation from the physical edge U_eff,E (ramification from physical edge UEFF) remains a named theorem target unless the cover blocks are embedded as non-auxiliary subblocks of the physical edge dynamics.

Baryon anonymous poles are cert-closed on the image basis (real S3 projectors, deterministic U, poles from the 40D/56D compressed operators only). Zero-padded or PDG in core forbidden.

Let \(P_E\) be the projector onto the edge sector of the 1-skeleton of \(K(9,11,13)\), with 359 edge channels. The electromagnetic normalization is reduced to the finite edge-sector trace/residue target
\[
F_E=P_EU_E^\dagger Q_EU_EP_E,
\qquad
\operatorname{Tr}(F_E)=\frac{359}{\varphi^2}-\varphi^{-5}.
\]
The first term is the edge-channel phase-return contribution and the second term is the torus-boundary leakage contribution. This is a coefficient-origin operator target; QED running and external numerical comparison are passport layers.


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b04-1]: open obligation — cert obligation open
[^b04-2]: open obligation — cert obligation open
[^b04-3]: open obligation — cert obligation open
[^b04-4]: forcing: GOLDEN DEF 16.5.1
[^b04-5]: forcing: GOLDEN THE 16.3.7
[^b04-6]: forcing: GOLDEN CHK 16.3.8/16.3.9
[^b04-7]: forcing: GOLDEN REM 16.3.SE
[^b04-8]: forcing: GOLDEN THE 9.1.2
[^b04-9]: forcing: GOLDEN REM 9.1.2.R
[^b04-10]: forcing: GOLDEN DEF 9.2.1
[^b04-11]: forcing: GOLDEN THE 9.2.2
[^b04-12]: forcing: GOLDEN LEM 9.2.2.T
[^b04-13]: open obligation — cert obligation open
[^b04-14]: forcing: GOLDEN THE 17.1.1
[^b04-15]: forcing: GOLDEN THE 17.1.5 + COR
17.1.5.A
[^b04-16]: forcing: GOLDEN LEM 3.10.B
[^b04-17]: forcing: GOLDEN COR 3.10.C
[^b04-18]: forcing: GOLDEN DEF 17.2.1, BOOK-III-SPECTRUM
[^b04-19]: forcing: GOLDEN REM 17.2.1.A
[^b04-20]: forcing: GOLDEN LEM 17.2.1.B
[^b04-21]: forcing: GOLDEN THE 17.2.2 + COR 17.2.1.C
[^b04-22]: forcing: GOLDEN DEF 17.2.3
[^b04-23]: open obligation — cert obligation open
[^b04-24]: open obligation — cert obligation open
[^b04-25]: open obligation — cert obligation open
[^b04-26]: open obligation — cert obligation open
[^b04-27]: open obligation — cert obligation open
[^b04-28]: forcing: GOLDEN BOOK-VI-EXTENSIONS THE 61.5
[^b04-29]: forcing: GOLDEN D0-THEORY-DOSSIER THE IV.1, claim `D0-MIXING-HIERARCHY-INVERSION-001`
[^b04-30]: forcing: GOLDEN D0-THEORY-DOSSIER THE IV.1; ⊥-proof
[^b04-31]: forcing: GOLDEN D0-THEORY-DOSSIER THE IV.3, claim `D0-MIXING-HIERARCHY-INVERSION-001`
[^b04-32]: forcing: GOLDEN BOOK-04 Thm 04.9B, the `[J,Y]` bulk carrier
[^b04-33]: open obligation — cert obligation open
[^b04-34]: open obligation — cert obligation open
[^b04-35]: open obligation — cert obligation open
[^b04-36]: open obligation — cert obligation open
[^b04-37]: forcing: GOLDEN BOOK-04 §04.5 prime-edge anyon scaffold.
[^b04-38]: forcing: GOLDEN THE 61.8 "359 Limit", CORE→BRIDGE.
[^b04-39]: forcing: GOLDEN BOOK-04 §04.5A companion embedding, Def 4.4A / Thm 4.4B.
[^b04-40]: forcing: GOLDEN BOOK-04 §04.5D Fibonacci fusion / Jones index.
[^b04-41]: open obligation — cert obligation open
[^b04-42]: open obligation — cert obligation open
[^b04-43]: open obligation — cert obligation open
[^b04-44]: open obligation — cert obligation open
[^b04-45]: open obligation — cert obligation open
[^b04-46]: open obligation — cert obligation open
[^b04-47]: open obligation — cert obligation open
[^b04-48]: open obligation — cert obligation open
[^b04-49]: open obligation — cert obligation open
[^b04-50]: open obligation — cert obligation open
[^b04-51]: open obligation — cert obligation open
[^b04-52]: open obligation — cert obligation open
[^b04-53]: forcing: GOLDEN DEF 6.2.1, BOOK-III-SPECTRUM
[^b04-54]: forcing: GOLDEN THE 6.2.A, BOOK-III-SPECTRUM; ⊥-proof
[^b04-55]: forcing: GOLDEN LEM 6.2.2, BOOK-III-SPECTRUM; ⊥-proof
[^b04-56]: forcing: GOLDEN THE 6.2.B, BOOK-III-SPECTRUM
[^b04-57]: forcing: GOLDEN THE 6.2.C, BOOK-III-SPECTRUM
[^b04-58]: forcing: GOLDEN THE 6.2.4, BOOK-III-SPECTRUM
[^b04-59]: forcing: GOLDEN THE 6.2.D, BOOK-III-SPECTRUM
[^b04-60]: forcing: v17 Thm 04.6B / D0.Core; ⊥-proof
[^b04-61]: forcing: GOLDEN DEF 24.P.2, BOOK-V-MATHEMATICS
[^b04-62]: forcing: GOLDEN THE 24.P.3, BOOK-V-MATHEMATICS
[^b04-63]: forcing: GOLDEN DEF 24.S.1 / THE 24.S.2, BOOK-V-MATHEMATICS
[^b04-64]: forcing: GOLDEN DEF 24.D.1 / THE 24.D.2, BOOK-V-MATHEMATICS
[^b04-65]: forcing: GOLDEN THE IV.1.1, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-66]: forcing: GOLDEN THE IV.1.2, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-67]: forcing: GOLDEN THE IV.1.3, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-68]: forcing: GOLDEN THE IV.1.4, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-69]: forcing: GOLDEN THE IV.1.9, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-70]: forcing: GOLDEN THE IV.1.5, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-71]: forcing: GOLDEN THE IV.1.7, BOOK-IV-VERIFICATION
[^b04-72]: forcing: GOLDEN THE IV.1.8, BOOK-IV-VERIFICATION
[^b04-73]: forcing: GOLDEN THE IV.1.6, BOOK-IV-VERIFICATION
[^b04-74]: forcing: GOLDEN THE IV.1.10, BOOK-IV-VERIFICATION; ⊥-proof
[^b04-75]: open obligation — cert obligation open
[^b04-76]: forcing: GOLDEN BOOK-III-SPECTRUM CHK 11.E.3
[^b04-77]: forcing: GOLDEN BOOK-III-SPECTRUM CHK 11.E.3
[^b04-78]: open obligation — cert obligation open
[^b04-79]: open obligation — cert obligation open
[^b04-80]: open obligation — cert obligation open
[^b04-81]: open obligation — cert obligation open
[^b04-82]: forcing: GOLDEN BOOK-III-SPECTRUM §III.3 mass-spectrum contract
[^b04-83]: forcing: GOLDEN DEF 11.M.1, BOOK-III-SPECTRUM
[^b04-84]: forcing: GOLDEN DEF 11.M.2, BOOK-III-SPECTRUM
[^b04-85]: forcing: GOLDEN DEF 11.M.3, BOOK-III-SPECTRUM
[^b04-86]: forcing: GOLDEN LEM 11.M.5, BOOK-III-SPECTRUM
[^b04-87]: forcing: GOLDEN THE 6.5.4, BOOK-III-SPECTRUM
[^b04-88]: forcing: GOLDEN §III.3 structural derivation + THE 11.L.1, BOOK-III-SPECTRUM
[^b04-89]: forcing: GOLDEN THE 11.L.1, BOOK-III-SPECTRUM
[^b04-90]: forcing: GOLDEN THE 11.L.1.B, BOOK-III-SPECTRUM; ⊥-proof
[^b04-91]: open obligation — cert obligation open
[^b04-92]: open obligation — cert obligation open
[^b04-93]: open obligation — cert obligation open
[^b04-94]: forcing: GOLDEN BOOK-VI-EXTENSIONS THE 61.7
[^b04-95]: forcing: GOLDEN BOOK-VI-EXTENSIONS THE 61.7; ⊥-proof
[^b04-96]: forcing: GOLDEN BOOK-VI-EXTENSIONS THE 61.7 with THE 61.10; ⊥-proof
[^b04-97]: forcing: GOLDEN §16.3, COR 16.3.5
[^b04-98]: forcing: GOLDEN BOOK-VI-EXTENSIONS BRIDGE-LEM 61.10.B; BRIDGE
[^b04-99]: forcing: GOLDEN BOOK-04 Thm 04.9B
[^b04-100]: forcing: GOLDEN THE 1
[^b04-101]: forcing: GOLDEN THE 1
[^b04-102]: forcing: GOLDEN THE 12
