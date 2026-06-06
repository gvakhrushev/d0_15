# BOOK 04 — Spectrum, Matter, and Finite Selector Theory

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
\boxed{\text{finite support is not a physical mass by itself.}}
```

Matter defect/domain-wall operators are finite projected operators on the
1-cochain sector of the graded incidence complex.

A support number becomes a physical comparison only after a typed operator/readout and a declared transfer map have been supplied before seeing the target table.

## 04.2 The theorem owners used by this book

The active matter claims use the following proof owners.

| Function in Book 04 | Owner |
|---|---|
| normalized finite readout | `D0.Core.BornFinite.finite_born_readout_unique_on_finite_outcomes` |
| no alternative response readout | `D0.Core.BornFinite.finite_born_no_alternative_readout` |
| strict finite finite variational selector uniqueness | `D0.Matter.StrictSelectorCertificate`; `D0.Matter.strict_selected_unique` |
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
| П†-quasicrystal tiling hull | `D0.Topology.TilingHull`; `D0.Topology.d0_hull_has_phi_cut_project_origin`; `D0.Topology.d0_hull_is_nonperiodic`; `D0.Topology.d0_hull_supports_gap_labeling` |
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

## 04.3 Matter objects are finite variational selectors, not passports

The previous reading of Book 04 mixed three different things: internal finite objects, dressed Standard-Model comparison values and external data checks. The active reading removes that ambiguity.

A matter object is admitted only through one of the following forms:

1. **Finite support theorem.**  The carrier/support object is proved inside the finite D0 formalism.
2. **Finite response theorem.**  A positive or quadratic response is normalized by the finite Born/readout theorem.
3. **Strict finite variational selector certificate.**  A finite candidate family and score function select a unique internal object.
4. **Basis-origin theorem.**  The up/down operator bases must themselves be outputs of finite basis finite variational selectors.  After those finite variational selectors are fixed, the mismatch matrix is unique up to declared quotient symmetries.
5. **Observable-transfer protocol.**  A frozen D0 object is compared to an external convention through a declared bridge.
6. **No-go.**  The frozen operator family is insufficient to promote a claim.

The word `finite variational selector` is therefore not a stylistic label.  It means a finite candidate set, a score functional and a strict minimizer/maximizer whose uniqueness is protected by the finite variational selector theorems.  Changing the selected object means changing the score functional, not changing a status table.

The quasicrystal matter ontology used later in this book is summarized in 04.4: matter is read as defects, domain walls, holonomies, window weights and K0 gap-labeled spectra over the П†-quasicrystalline tiling hull. This ontology organizes the sector owners; it does not bypass the finite variational selector/readout/passport rules above.

## 04.4 Matter as defects and gap-labeled spectra over the φ-quasicrystalline hull

The D0 vacuum is the condensed/profinite hull of all admissible finite detector registrations, and matter is read as defects, domain walls, holonomies, window weights, and gap-labeled spectra over this φ-quasicrystalline support.

### 04.4.1 Phason-mode generations and baryon S3

The matter generations and baryons as phason modes are theorem-owned by `D0.Matter.PhasonStrainGenerations`. The phason carrier is exactly `D0.Geometry.TorusShell`, so the generation/phason mode count is the already proved three-shell torus count.

The ordered carrier is `BaryonPhasonTriple = PhasonMode x PhasonMode x PhasonMode`, hence dimension `27`. The full baryon multiplet decuplet carrier is not a nucleon-line extension; it is the S3-symmetric phason triple sector of dimension `10`, with `baryon_phason_symmetric_sector_dim_eq_ten`.

### 04.4.2 Mesons as phason domain walls

The lower-Hodge value 400 is not a meson mass. It is the phason domain-wall tension seed. Physical meson transfer requires:

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

The K0 label is not a meson mass and cannot tune the domain-wall operator after comparison. It only records which frozen spectral gap is being transported to an external passport.

### 04.4.4 CKM as noncommutative phason holonomy

CKM is not a fitted mismatch matrix. It is the finite holonomy of phason transport on the Core-13 torus shell carrier.

The core theorem closes the finite holonomy object and the non-permutation overlap response. The passport layer is separate: physical CKM entries, PDG conventions and uncertainty tables are external comparison protocols and cannot feed back into the phason carrier.

### 04.4.5 CKM K-class and oriented CP area

The CP phase is the oriented noncommutative area of this holonomy, classifying the CKM K-class.

### 04.4.6 Window-sector fractional charges

The D0 support is a cut-and-project quasicrystal. Matter as phason/window defects of the φ-quasicrystal vacuum maps the fractional quark charge as a window-sector intersection weight:

- one sector -> 1/3;
- two sectors -> 2/3;
- orientation/sign branch -> +/-.

Hence, quark color/charge = window-sector weights and generations = inflation classes.

### 04.4.7 Window-offset chirality

Weak chirality is represented as a window-offset effect: chirality = acceptance-window offset.

### 04.4.8 Neutrino as neutral bulk phason wave

The neutrino is represented as a neutral bulk phason wave with zero active EM coupling.

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

## 04.6 Finite Born 2.0 in matter language

The finite matter probability chain now starts one step before effects.  A finite channel amplitude `(x,y)` is first reduced to the forced phase-blind quadratic response `x^2+y^2`; matter effects then aggregate these squared norms over the finite support; only then is the response normalized.  Thus a matter-sector probability cannot introduce either a new response functional or a new probability functional.

```text
finite amplitude channel -> DвЂ D squared norm -> finite response -> Born normalization
```


Matter readout may use a normalized weight only after the finite effect frame has been supplied.  A candidate particle sector must identify:

```text
finite candidate support I;
finite detector/support atoms S;
nonnegative effects E_i(s);
nonnegative detector state R(s);
raw responses r_i = ОЈ_s E_i(s)R(s).
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

## 04.7 Electroweak radial depth as a concrete finite variational selector

The matter sector inherits the single action section from Book 03.  Electroweak quantities are therefore read as finite radial depths and comparison outputs, not as independent primitive constants.

The active integration replaces the earlier phrase "depth 35" by an actual Book 04 finite variational selector owner:

```text
D0.Matter.electroweakDepth35FullSupportClaim
D0.Matter.electroweak_depth35_full_support_no_free_alternative
```

The finite finite variational selector window is:

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

## 04.8 Charged leptons as a concrete finite variational selector family

The charged-lepton branch is controlled by a finite operator family rather than three free Yukawa constants. The active integration makes the finite terminal support explicit in Lean:

```text
D0.Matter.ChargedLeptonBranch = {electron, muon, tau}
D0.Matter.chargedLeptonBranchFiniteSupport
D0.Matter.chargedLeptonElectronTerminalClaim
D0.Matter.charged_lepton_terminal_no_free_alternative
```

The electron is now formally the unique terminal calibration register in the charged branch support.  Changing the terminal unit to `muon` or `tau` would require changing the terminal score functional; it cannot be done by a table rewrite.

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

and the bridge-factor row `B_g` as a finite row function.  These entries are read from the selected coefficient origin; they are not free Yukawa constants and they are not inverted from external lepton masses.

The generation action is still written as

```math
\mathcal S_{\ell,gen}[R]
=\sum_{g\in\mathcal G_\ell}\left(\log R_g-\log r_g-p_g\log A_{EW}-\log B_g\right)^2.
```

Stationarity gives

```math
R_g^{D0}=r_gA_{EW}^{p_g}B_g.
```

The theorem-level replacement is the no-retuning statement: at fixed `ChargedLeptonCoefficientOrigin`, changing any of `r_g`, `p_g` or `B_g` is an origin deformation, not a notation change and not a status update. A deeper spectral derivation of the decimal ratio values from a raw graph operator can still refine the origin, but the active Book 04 lepton row no longer has an independent coefficient knob.

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
decoherence comparison belongs to the downstream passport layer.

## 04.10 CKM as finite basis origin, not a free matrix

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

The owner `D0.Matter.CKMBasisOrigin` moves the proof one level upstream. The up and down bases are not silent inputs: each is a strict finite finite variational selector output. The theorem `ckm_origin_candidate_matrix_unique` says that any admissible origin candidate using the same finite basis finite variational selectors returns the same matrix. The theorem `ckm_no_free_matrix_at_fixed_basis_origin` forbids a second matrix at fixed basis origin.

The generation-overlap layer now has a smaller D0-origin owner.  The active source is no longer an unexplained path `0-1-2`: `D0.Geometry.TorusCore13GeometryOrigin` supplies the three torus shell boundaries and proves that radial shell hopping does not commute with shell phase/radius drift.  Lean checks

```text
[A_radial, D_phase]_(0,1) = minor radius != 0
```

and `D0.Matter.GenerationOverlapResponseOrigin` records the corrected overlap interface:

```text
O_ij = |(U_up^H U_down)_ij|^2
IsPermutationWitness O := exists sigma : Equiv.Perm GenCarrier, ...
```

Thus the algebraic source of non-permutation overlap is torus shell noncommutativity, not a fixture matrix.  The certificate `vp_generation_finite variational selector_origin.py` checks the resulting shell-induced unistochastic response, rejects all full permutation witnesses, finds a multi-support row and verifies `F_fl^T F_fl` positivity.  This is an algebraic origin closure, not a derivation of physical CKM entries, angles, CP phase or RG-dressed passport values.

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

Sync token: 04.10 SM-facing finite gauge decomposition.

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

A different gauge factor list or a different one-generation ledger is not a second core solution under the same owner.  It is a new carrier attempt and must be routed to a separate theorem/no-go/bridge target.  This closes the weaker old reading where `SU(3)Г—SU(2)Г—U(1)` could look like a name attached after the fact.

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

The proton and neutron rows are therefore single-section terminal readouts with full-support finite finite variational selector owners.  Measured masses and lifetimes are benchmarks, not inputs.

### 04.12.1 Full-support replacement of local finite variational selector windows

Earlier drafts used nearest-neighbour windows such as `{305,306,307}` and `{18,19,20}` as a quick anti-retuning check. Those windows are no longer the active theory. The active owners are:

```text
D0.Matter.Book04FullSupportSelectors
D0.Matter.electroweakDepth35FullSupportClaim
D0.Matter.protonReadout306FullSupportClaim
D0.Matter.betaUnlockDepth19FullSupportClaim
```

The electroweak radial depth is selected over `Fin 71`, the proton destructive readout over `Fin 613`, and the beta weak-unlock depth over `Fin 39`.  Therefore a critic cannot move the selected value by leaving the local В±1 window while keeping the same finite residual finite variational selector.  Any different value requires a different admissible support or a different score functional, hence a different theory object.

## 04.14 Baryon multiplet boundary as a closed no-go

The frozen operator family proves the nucleon line. It does not prove a full
`N, О”, О›, О©` mass table, and the active book no longer leaves this as an ambiguous вЂњfuture
statusвЂќ row.  The boundary is still theorem-owned, but the decuplet carrier now
has a constructive finite owner:

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

The decuplet carrier is not the rank-one invariant sector of a 3-dimensional
vertex representation.  It is the S3-symmetric sector of the tensor carrier

```text
BaryonTripleCarrier := Fin 3 x Fin 3 x Fin 3
```

so the ordered carrier has dimension `27`, and the sorted-orbit representatives
have cardinality `10`.  This is the finite decuplet carrier; it is not a QCD,
PDG or mass-spectrum claim.

The required typed operator must contain, before comparison,

```text
spin resolution;
flavour resolution;
S3 decuplet carrier closure;
transfer window for unstable-resonance comparison.
```

The active nucleon operator is deliberately the `nucleonLineOnlyBaryonOperator`.
The theorem

```text
nucleon_line_cannot_promote_full_baryon_multiplet
```

says that this operator cannot be re-read as a full baryon multiplet.  The
finite reason is that an antisymmetric line sector is annihilated by the S3
symmetrizer, while the decuplet carrier is fully symmetric.  Therefore the
previous direct `Delta, Lambda, Omega` formula flow is not merely вЂњnot
certifiedвЂќ; it is blocked under the present operator family.  A numerical
agreement with PDG resonance masses cannot supply the missing operator.

## 04.15 Meson/chiral boundary as a closed no-go

The meson lower-Hodge support seed remains

```math
L_{mes}=\partial_1^TW_V\partial_1,
\qquad
\lambda_{mes}^{min}=400.
```

The active theorem-owners are now

```text
D0.Matter.MesonDefectTransferAlgebra
D0.Matter.MesonCarrier
D0.Matter.liftEdge
D0.Matter.liftGen
D0.Matter.mesonDefectTransferOperator
D0.Matter.lower_hodge_seed_not_meson_mass_operator
D0.Matter.MesonTransferOperator
D0.Matter.CanPromoteMesonMasses
D0.Matter.lower_hodge_400_cannot_promote_meson_masses
D0.Matter.meson_mass_promotion_requires_chiral_flavour_vector_operator
```

The rule is not a prose warning.  It is a no-go against the support-only promotion:

```math
400\not\Rightarrow m_\pi,
\qquad
400\not\Rightarrow m_K,
\qquad
400\not\Rightarrow m_\rho.
```

A physical pseudoscalar/vector comparison requires a finite
edge-generation transfer carrier:

```text
MesonCarrier E Gen := Fin E x Fin Gen
```

The typed finite operator is

```math
\mathcal C_{\chi F V}^{D0}
=\Pi_M\bigl(
  \operatorname{liftEdge}(L_M)
 +\operatorname{liftEdge}(\Gamma_\chi^\dagger\Gamma_\chi)
 +\operatorname{liftGen}(F_{fl}^\dagger F_{fl})
 +\operatorname{liftEdge}(V_{sp}^\dagger V_{sp})
\bigr)\Pi_M.
```

The flavour defect is therefore in the total operator through `liftGen`; it is
not added as a mismatched `Gen x Gen` block to an `Edge x Edge` sum.  The bare
lower-Hodge seed lifted as `liftEdge L_M` remains internally generation-blind,
so it cannot separate meson transfer channels by itself.  Until the typed
defect-transfer algebra and a transfer window are supplied, the lower-Hodge seed
is a support seed only.  It cannot be promoted to pion, kaon or rho masses by
changing a table, status vocabulary or unit convention.

## 04.16 Higgs/scalar projector boundary

The electroweak radial finite variational selector closes depth 35 and the vector-boson ratio line. It does not automatically close the Higgs scalar projector or all Yukawa rows. The active book makes this boundary theorem-owned rather than implicit:

```text
D0.Matter.HiggsYukawaProjectorBridge
D0.Matter.CanPromoteHiggsYukawaCore
D0.Matter.higgs_yukawa_requires_scalar_projector
D0.Matter.missing_scalar_projector_cannot_promote_higgs_yukawa_core
```

The finite core can promote a Higgs/Yukawa row only after it supplies:

```text
constructive scalar projector closure on the finite matter-transfer carrier;
Yukawa section;
no-second-mass-anchor certificate;
transfer convention.
```

The current boundary object `missingScalarProjectorBridge` cannot be promoted. This is stronger than saying вЂњHiggs pendingвЂќ: it forbids using `M_Z`, `v`, a measured Higgs mass or a Yukawa table as a hidden second anchor. A future scalar-sector closure must first construct the finite scalar projector and then route any external GeV comparison through the declared bridge.

In the active finite interface, `hasScalarProjector : Prop` is not enough.  The
Higgs/Yukawa bridge must carry an actual constructive closure object:

```text
Option (ConstructiveScalarProjectorClosure finiteEWMatterTransferCarrier)
```

so the old theorem-shaped wrapper cannot smuggle the scalar projector in as an
assumption label.

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
| charged leptons | finite finite variational selector/action family; external mass comparison after electron section |
| neutrinos | neutral leakage support; one-anchor oscillation bridge only |
| CKM | finite up/down basis-origin finite variational selectors; D0 ordinal/adjacency generation finite variational selectors force noncommuting overlap origin; no free matrix at fixed origin; numerical passport remains downstream |
| generation multiplicity | finite three-generation theorem |
| anomaly behavior | finite anomaly-preservation theorem |
| electroweak ratio | finite radial/runtime comparison; Higgs/Yukawa core promotion blocked until scalar projector bridge is supplied |
| proton/neutron | terminal-destructive and beta/archive readouts; benchmarks not inputs |
| full baryon multiplet | S3 tensor decuplet carrier exists; current nucleon-line operator is still blocked from full multiplet promotion | masses and unstable-resonance comparison require spin/flavour transfer and external passport |
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
7. a baryon row promotes the nucleon-line operator to a full multiplet without spin/flavour/S3-decuplet carrier data;
8. a Higgs/Yukawa row uses a second mass anchor before the scalar projector is supplied;
9. an external carrier comparison is used as a D0 axiom.

## 04.22 Remaining matter operator frontiers

The following are not permissions to use old shortcuts. They are operator frontiers requiring explicit carriers:

1. Charged-Lepton: derive the decimal charged-lepton coefficient row from a lower raw graph-spectrum operator, while preserving the already frozen `ChargedLeptonCoefficientOrigin` row.
2. CKM: route the generation-overlap origin through the physical CKM convention/RG passport without post-hoc permutation.
3. Baryons: add spin/flavour transfer and an unstable-resonance passport before comparing baryon multiplet masses.
4. Mesons: add a meson transfer window/passport before comparing pseudoscalar/vector meson masses.
5. Higgs: construct the scalar projector and no-second-anchor certificate if Higgs/Yukawa rows are to be promoted.
6. SM Decomposition: refine the SM carrier decomposition theorem until nearby finite decompositions are excluded by lower operator origins rather than by the frozen ledger alone.

## 04.23 Selector closures now owned by finite operators

The correction pass removes half-closures from the active matter book.

### 04.22.1 Charged-lepton mass transfer is now downstream of the coefficient origin

The charged-lepton block is no longer allowed to stop at "the coefficient row is frozen". The finite row must feed a branch-wise transfer object: `D0.Matter.ChargedLeptonMassTransfer`. These entries are read from the selected coefficient origin, and the theory no longer has an independent coefficient knob.

### 04.22.2 CKM has a frozen finite transfer before external comparison

The CKM block is no longer only "basis finite variational selectors determine a matrix". The finite matrix now has a downstream frozen transfer owner: `D0.Matter.FrozenCKMMatrixTransfer`. A passport may compare the matrix; it cannot choose or retune it.

### 04.22.3 Higgs/Yukawa is decided, not left ambiguous

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

- **Operator Boundaries**:
  - `D0.Matter.book04_operator_boundaries_closed`
  - `Baryon multiplet boundary as a closed no-go`: `nucleon_line_cannot_promote_full_baryon_multiplet`
  - `Meson/chiral boundary as a closed no-go`: `lower_hodge_400_cannot_promote_meson_masses`
  - `Higgs/scalar projector boundary`: `missing_scalar_projector_cannot_promote_higgs_yukawa_core`

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

For baryons, the decuplet carrier is not a nucleon-line extension. It is the S3-symmetric triple sector over the three torus shell roles; the Lean owner `BaryonS3Symmetrizer` exposes `BaryonTripleShellCarrier` and `baryon_triple_shell_card_eq_27`.

For Higgs/Yukawa, the scalar projector is connected but not identical to torus geometry. Torus shell radius is not a Higgs VEV, torus aspect ratio is not a Higgs mass, and radial hopping/phase drift are not the scalar projector. The scalar projector remains the minimal positive idempotent matter-transfer bridge compatible with tick/Lorentz and the frozen gauge ledger.

Constructive Scalar Projector Closure: `FrozenSU2_X` and `FrozenSU2_Z` force
the admissible scalar projector to have form `P=aI`; its trace-rank is 2. Torus
radius is not Higgs VEV, and torus aspect is not Higgs mass. Torus radius is not Higgs VEV.

## 04.V Nuclear shell-contact SRC operator

D0-SRC-001 -- Nuclear Shell-Contact SRC Operator.

Matter as phason/window defects of the phi-quasicrystal vacuum: generations =
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

Certificate owner: `05_CERTS/vp_nuclear_shell_contact_src.py`. The synthetic certificate checks the frozen CaFe shell-contact witness; Nature 2026 source-data comparison is an external passport and may only run from a pinned manifest.

Current external-data runner result:

```text
PASS_NUCLEAR_SHELL_CONTACT_SRC_SYNTHETIC
PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026
```

The Nature 2026 source-data XLSX files are pinned in the manifest. The external
run reads Source Data Fig. 2 and Fig. 3 and returns:

```text
Ca48/Ca40 = 1.097
weighted_mean = 1.0927

Fe54/Ca48 = 1.493
weighted_mean = 1.4741
```

The observed ordering is `Fe54/Ca48 > Ca48/Ca40`; the A-only, N/Z-only and
density-only scalar controls fail this shell-contact ordering.


