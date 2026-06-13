<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 05 — Verification, Proof Ownership, and Certificate Discipline

> **Publication status — v16 publication-proofread draft.**
> Scope: Claim classification, proof ownership, certificate discipline, no-go ledger, and promotion rules.
> Claim discipline: This book decides status; it does not add physical content.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 05.v15 Active closure law
Book 05 classifies every active claim as core theorem, sector theorem, operator scaffold, bridge law, empirical passport, or no-go theorem; completion means a finite operator plus falsification boundary. `OPERATOR-SCAFFOLD-CERTIFIED` is positive internal carrier closure but not an external physical spectrum; `SPIN-FLAVOUR-CARRIER-CERTIFIED` means a finite spin-flavour carrier and its inclusion/decomposition algebra are certified before external physical labels. `SPIN-FLAVOUR-TRANSFER-CERTIFIED` is the prior transfer layer name now refined to carrier certification. `SCALAR-PROJECTOR-CERT-CLOSED`, `YUKAWA-SECTION-CERT-CLOSED` and `MESON-TYPED-TRANSFER-CERT-CLOSED` close the corresponding Book 04 operator boundaries at the finite projector/typed-operator level (no second mass anchor, flavour defect only via liftGen, K0 gap labels after freeze).

### Centralized no-go ledger

All repeated forbidden shortcuts and no-gos from Books 00–08 are collected here. Physical books contain only the pointer: "Forbidden shortcuts are centralized in Book 05, D0_NOGO_LEDGER."

### Phase-unfolding reference

owner: D0.Geometry.PhaseUnfoldingQuasicrystal
Full theorem (tick order -> irrational phi^-2 phase -> finite return modulus -> residue branches, q_T=44, q_EW=710) lives only in Book 01 (and proof spine Book 02). All other occurrences replaced by the cross-reference "By the Phase-Unfolding Theorem (D0.Geometry.PhaseUnfoldingQuasicrystal), ...".

SCALAR-PROJECTOR-CERT-CLOSED: finite rank-2 scalar projector exists, is unique on the frozen doublet, commutes with FrozenSU2_X/Z, and preserves single-section discipline.

YUKAWA-SECTION-CERT-CLOSED: finite Yukawa block map is compatible with the certified scalar projector and introduces no second mass anchor.

MESON-TYPED-TRANSFER-CERT-CLOSED: finite typed edge-generation meson transfer operator exists, is self-adjoint/positive, places flavour defect only via liftGen, and preserves K0 gap-label discipline.

MASTER-BOOTSTRAP-CORE: the stationary condition on the combined heat-trace + feedback-determinant functional is the v15 final bootstrap principle (finite object + variation + no second scale).

GAUGE-BOUNDARY-LAW: color confinement is the commutator obstruction preventing terminal stable poles for non-singlet states (finite lower-bound target on F_N).

HORIZON-EMISSION-LAW: horizon emission is archive-to-retained boundary leakage under capacity saturation (conjugate feedback form certified at finite operator level).

BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED: baryon resonances are anonymous poles of the exchange-symmetric compressed dynamics on the certified 40/56 carriers; eigenvalues computed on the image basis of the projectors.

EDGE-TRACE-COEFFICIENT-TARGET: edge-sector electromagnetic normalization is a theorem target on the 1-skeleton (guardrail form only; no numerology claim).

TORUS-RAMIFICATION-TARGET: lepton hierarchy as torus ramification / Puiseux indices is a theorem target (guardrail form only; no fraction fit claim).

FRACTAL-CONTINUUM-CORE-CLOSED: fractal tick substrate yields the unique continuous semigroup envelope under the corrected multiplicative form \(A(s+t)=A(s)A(t)/A_0\); orbit-averaged emission uses \(|G_8|\) with explicit irreducibility proviso.

RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED: A finite internal observable \(R_n = B_n / A_n\) derived from fractal tick recurrence has strictly positive second finite difference, and its continuum envelope has positive second derivative.

RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED: Weak bridge \(\mathsf P_{rel}=c_R\Delta R_n\) (fixed internal \(c_R>0\)) with positive increment from relative acceleration.

LOGDET-PRESSURE-COUPLING-CERT-CLOSED: Strong internal positive loop-pressure response \(\partial_V[-\log\det(I-zF_N(V))]\) derived from explicit volume dependence of \(F_N(V)\) in the clock sector (correct \(r(V)=1-e^{-\kappa V}\) derivative).

PUBLICATION-MONOGRAPH-STRUCTURE: Corpus organized into coherent chapters with explicit internal finite objects, cert-closed theorems, and clear passport boundaries. Standardized D0 vocabulary enforced in main text.

HORIZON-EMISSION-LAW: horizon emission is archive-to-retained boundary leakage under capacity saturation (conjugate F form, greybody candidates).

Forbidden shortcuts (extended):
H0 value from core topology alone
DESI/SPARC/H0 fit without passport
confusing absolute archive deceleration with relative archive acceleration
survey data entering definition of R_n or its acceleration
using the wrong derivative for r(V) (e.g. treating r(V) as constant)
retuning z or c_R from external survey data
confusing the relative archive ratio with a physical FLRW scale factor
using the expression outside the resolvent domain

EDGE-TRACE-COEFFICIENT-TARGET: electromagnetic normalization reduces to an edge-sector trace/residue invariant on the 1-skeleton (coefficient-origin theorem target).

TORUS-RAMIFICATION-TARGET: charged-lepton hierarchy reduces to branch indices (torus ramification / Puiseux exponents) of the finite Green function over the shell torus.
Sync gates retained here: `## 05.13 Current inherited priority gates`, `D0.Matter.Book04OperatorBoundary`, `nucleon_line_cannot_promote_full_baryon_multiplet`, `lower_hodge_400_cannot_promote_meson_masses`, `IceCube comparison is EMPIRICAL-PASSPORT`, `cannot select or tune the D0 neutrino kernel`, and Gravity closure requires: finite graph/entropy cert, explicit Pi_TT and W_TT, higher-curvature cut, spectral A2/EH bridge, no continuum constants imported as core.

## 05.1 Role of this book

Book 05 is the verification calculus of the D0 corpus.  It does not introduce the
condensed site, the detector algebra, the action stack, matter spectra, gravity
operators or cosmology transfer laws.  Those objects belong to Books 01--04 and
06--08.  Book 05 defines when a statement from those books is admissible as a
D0 theorem, a finite certificate, a no-go, a bridge claim, an empirical external comparison protocol
or a non-active conjecture.

The governing order is:

```text
theory first;
proof owner second;
ledger/status last.
```

A pure change of status vocabulary, table formatting, archive label, guard
script, heading name or release label is non-substantive.  It changes the corpus
only if it follows a changed theorem, executable certificate, formal no-go or
explicit bridge boundary.

The normative verification chain is:

```text
claim
-> standard-language object
-> support object
-> probe/gate/operator
-> positive response or invariant quotient
-> finite certificate / Lean theorem / no-go
-> bridge or external comparison protocol only after the internal object is frozen
-> classification row
```

The classification row is the last artifact, not the proof.

## 05.2 Verification as finite measurement

Verification in D0 is itself a finite detector operation.  A statement is not
release-ready because it is elegant, suggestive or expressed in D0-local words.
It is admissible only if it reduces to at least one of the following finite
objects:

```text
finite record;
finite operator trace;
positive response;
invariant quotient;
strict selector;
finite no-go counterexample;
explicit external comparison protocol with frozen internal input.
```

This rule is the verification form of the foundational condition:

```text
no interaction without information;
no information without detector/register.
```

A verifiable claim is therefore not a beautiful formula.  It is a finite record
with a falsification hook.

## 05.3 Standard-language audit rule

Every active D0-local expression must expose its standard object.  The following
translations are mandatory in proof cells:

| D0 term | Standard-language obligation |
|---|---|
| archive | traced-out complement, environment, quotient store or forgotten support |
| forgetting | conditional expectation, partial trace, quotient, RG map or projection |
| readout | positive operator-valued instrument, response functional or finite selector |
| bridge | typed coupling, functor, EFT matching map, scheme dictionary or comparison kernel |
| external comparison protocol | external comparison protocol with manifest and fixed internal input |
| stiffness | structural uniqueness plus negative controls |
| transfer | explicit map from frozen D0 object to comparison object |
| support | finite/profinite carrier, graph shell, operator support or sector family |

Undefined D0-local terminology is a release blocker.  It is not a stylistic
issue.

## 05.4 Evidence levels

D0 uses five evidence levels.  They must not be merged.

| Level | Meaning | May define the D0 object? |
|---|---|---:|
| theorem | mathematical consequence of active D0 definitions | yes |
| certificate | executable finite witness for a stated theorem, formula, uniqueness or no-go | no, unless the finite object is already specified in the theorem |
| no-go | proof that a promotion is impossible under the current operator set | yes, negatively |
| bridge | typed dictionary from frozen D0 object to external convention | no |
| external comparison protocol | reproducible comparison with external data or scheme | no |

The anti-numerology firewall is:

```text
closed internal object -> declared bridge -> external comparison
```

not:

```text
external table -> search for a D0-looking expression
```

## 05.5 Claim object schema

Every mature claim must be represented by a complete proof cell:

| Field | Required content |
|---|---|
| Claim_ID | stable identifier |
| source location | book and section, plus Lean/cert file if present |
| standard object | standard-language interpretation of the D0 term |
| support | finite/profinite carrier, graph shell, operator support or sector support |
| probe/gate | finite test object, action gate, selector, response or transition operator |
| response/quotient | positive response, trace, quotient, window, selector or no-go residual |
| owner | Lean theorem, executable certificate, no-go, bridge or external comparison protocol |
| negative controls | forbidden shortcuts, neighboring failures or no-hidden-anchor checks |
| falsification hook | what would make the claim fail |
| active status | status after the above fields, not before |

A row without support, owner and falsification hook is not an active claim.

## 05.6 Status vocabulary

Status is not evidence. Status is the final ledger projection of theorem/cert/external comparison protocol ownership.

- `CORE-*`: Foundational detector, spectral, and action theorems.
- `CERT-CLOSED`: Executable finite certificates verifying frozen core invariants.
- `NO-GO`: Formal boundary blocking illegal promotion shortcuts.
- `BRIDGE-CLOSED`: External dictionary mapping frozen core objects.
- `EMPIRICAL-PASSPORT`: External-data comparison with manifest and scheme.
- `CONJECTURE` / `RETIRED`: Unverified statements or obsolete scaffolding.

## 05.7 One promotion process

The active promotion process follows a strict sequence:
support > operator > theorem/cert > book integration > optional external comparison protocol > ledger status.

Demotion is mandatory the moment any link in this sequence is broken. Under no circumstances can a status be promoted without the underlying theorem/cert being finalized and integrated first.

## 05.8 Forbidden shortcuts

The following shortcuts are invalid:

```text
SM-looking factor labels => full SM Lagrangian
Poisson equation alone => GR
symmetric tensor alone => spin-2 dynamics
TT label alone => wave equation / ghost freedom
EW depth + external Higgs mass => Higgs/Yukawa core
rank = 2 assumed as a scalar-projector premise => Higgs/Yukawa core
rank-1 scalar projector promoted to Higgs doublet
rank>2 scalar projector without multiplicity selector
commutant theorem applied to full carrier without frozen doublet/multiplicity selector
Yukawa section introduces second mass anchor
mismatched Gen×Gen block added directly to edge operator
direct 400 to meson mass promotion
gap label before frozen meson operator
CKM basis label => physical CKM angles and CP phase
frozen coefficient row => mass derivation from primitives
BAO/DESI/SDE fit => new D0 primitive
status label changed => theorem closed
selected number written in a table => finite selector theorem
support seed 400 => pion/kaon/rho masses
baryon support gap => full baryon multiplet
rank-40 treated as full baryon carrier
rank-56 pole set assigned to PDG before frozen U_eff poles
complex poles from bare positive F
random non-Hermitian resonance matrix
PDG names used to choose spin/flavour projectors
```

The purpose of Book 05 is to make these shortcuts impossible to miss.

## 05.9 Negative controls and hostile uniqueness

Negative controls are active evidence.  They protect D0 from overfitting and
numerological promotion.

A high-gain claim requires:

```text
operator lock;
finite support or quotient;
explicit selector/response;
nearest-neighbor or full-support negative controls;
no-hidden-anchor proof;
failure meaning inside D0 obligations.
```

For matter and bridge-facing claims, hostile uniqueness must answer not only
"does the chosen value work?" but also:

```text
why can no other admissible support element work under the same operator?
what exact assumption must change for another result to appear?
```

A no-go result is not a weakness when it prevents a false promotion.  It is a
boundary theorem.

## 05.10 Certificate tiers

The certificate surface is deliberately smaller than the historical script
surface.

| Tier | Role | Public meaning |
|---|---|---|
| Tier 1 | canonical core certificate | safe finite theorem witness |
| Tier 2 | bridge/external comparison protocol certificate | external data or convention required |
| Tier 3 | workbench/helper certificate | development aid, not release evidence |
| Tier 4 | retired/generator/mutating script | scaffold, not public evidence |

A claim is release-grade only when its primary certificate is callable from a
release runner or its Lean theorem is part of the active import spine.  A proof
cell without a runner is manuscript support, not release support.

## 05.10a Gap-label certificate discipline

Rules for gap labels:
1. Gap labels are allowed only after the operator is frozen.
2. K-theory cannot tune an operator.
3. A gap-label cert must expose the operator, approximants, gaps and labels.
4. External data may compare, never choose labels.
5. Post-hoc relabeling after PDG/BAO/CKM comparison is a FAIL.

The formal verification owner is `05_CERTS/vp_gap_labeling_d0_tiling_hull.py`, which must print `(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)0_GAP_LABELING_TILING_HULL`. The underlying Lean formalization of gap stability is checked by `D0.Matter.KTheoryGapLabeling`.

## 05.11 External-data and scheme discipline

External data are allowed only in declared external comparison protocols.  A legal comparison has
the form:

```text
O_D0 fixed;
B : O_D0 -> O_ext declared;
residual = d(B(O_D0), O_ext).
```

For QFT, EFT, RG, PDG or collider-facing claims, the bridge must declare:

```text
quantity;
scheme;
input scale;
output scale;
renormalization kernel or matching rule;
threshold convention;
external input;
free-repair-parameter count;
negative controls.
```

No row, phase convention, renormalization convention, likelihood cut, survey
subset or external baseline may be chosen after seeing the comparison residual.

## 05.11a Risky prediction passport discipline

IceCube, LIGO, CMB, BAO and galaxy-lensing external comparison protocols require:
1. data manifest;
2. hash;
3. frozen D0 prediction;
4. parameter-count ledger;
5. no hidden retuning.

The certificate owners are `05_CERTS/vp_phason_domain_wall_mesons.py` (`(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)0_LABELS`), `05_CERTS/vp_ckm_phason_holonomy_k0.py` (`(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)0`), and `05_CERTS/vp_phason_flip_entropy_sde.py` (`(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md)`). They must run under this frozen regime.

## 05.12 Theory-improvement gate

A patch improves the theory only if it removes a mathematical gap. The accepted forms are:
- positive derivation from previous D0 primitives;
- formal no-go that removes an illegal promotion;
- executable finite certificate for a fully specified finite object;
- bridge demotion that prevents an external comparison from being mistaken for core;
- clean rewrite that replaces old ambiguous claims by theorem-first statements.

A patch does not improve the theory if it only adds:
- new status vocabulary;
- new archive name;
- new guard without a new theorem/cert/no-go;
- new owner whose conclusion is already stored as an assumption;
- appendix dump of old text into an active book;
- wording that makes a conditional lemma sound like a full derivation.

This section is the acceptance rule for all later book edits.

## 05.12a Destructive NO-GO stress tests

A destructive certificate attempts an illegal shortcut and reports which invariant collapses. It does not add new physics. It strengthens the boundary by showing why the shortcut cannot be admitted.

Admissible destructive test cases include:
- rank-1 Higgs collapse;
- isolated phason boundary mismatch;
- Euclidean signature leakage;
- direct 400>mass meson failure;
- spin-only LIGO failure;
- second-section anchor failure;
- BAO/SDE root refit failure;
- CKM post-hoc permutation failure.
- K0 label chosen after external comparison failure;
- frozen operator retuned to preserve a desired K0 label failure;
- gap label promoted directly to mass/action scale failure.
- A-only SRC scalar failure;
- N/Z-only SRC scalar failure;
- density-only SRC scalar failure.

The nuclear SRC destructive tests are owned by `D0.Matter.NuclearShellContactSRC`. The CaFe finite witness blocks promotion of a mass-only, neutron-excess-only or density-only scalar because the dominant readout is the matched proton/neutron shell-contact projector overlap.

## 05.13 Current inherited priority gates

(marker moved to 06_AUDIT/internal_sync_and_passport_markers.md): ## 05.13 Active priority gates.

The active high-value gates are the following.  They are listed here not as
status trophies but as audit obligations.

| Sector | Current owner type | What is actually closed | What must not be overstated |
|---|---|---|---|
| Born response | `D0.Core.BornQuadraticResponse` | phase-blind quadratic response reduces to norm-square; finite normalization is unique | full derivation of the quadratic ansatz from detector composition |
| finite effects | `D0.Core.BornFiniteEffects` | finite effect, coarse-grained and tensor readouts are unique after response is fixed | complete quantum measurement theory |
| Book 04 selectors | centered/full-support selector owners | local windows are replaced by full symmetric supports and midpoint uniqueness | complete derivation of all physical masses |
| selector origins | combinatorial selector-origin owners | selected supports are tied to upstream D0 combinatorics | derivation of every upstream integer from first principles if not provided in its own book |
| charged leptons | coefficient and transfer certificate owners | rows and transfer tables are frozen against retuning | mass ratios derived directly from raw graph operators unless shown |
| CKM | basis-origin, generation-overlap origin and matrix certificate owners | CKM is not a free matrix at fixed finite origin; ordinal/adjacency generation selectors give a noncommuting unistochastic overlap source; a finite witness matrix is frozen | physical CKM angles, CP phase or PDG-scale matrix |
| baryon S3 carrier | `D0.Matter.BaryonS3Symmetrizer` | ordered triple carrier has dimension 27; S3-symmetric sorted representatives have dimension 10; antisymmetric nucleon-line sectors are annihilated by the symmetrizer | baryon resonance masses, QCD flavour physics or PDG multiplet fitting |
| meson transfer algebra | `D0.Matter.MesonDefectTransferAlgebra` | edge and generation operators are lifted to a common carrier; lower-Hodge lift is internally degenerate; flavour defect enters via `liftGen` | pion/kaon/rho masses, ChPT/QCD comparison or MeV calibration |
| Higgs/scalar | `D0.Matter.HiggsScalarProjectorConstructive` | frozen rational `X/Z` doublet compatibility forces every nonzero idempotent scalar projector to be `I_2`, hence trace-rank 2; rank 1 is impossible | full Higgs potential, VEV, Yukawa matrices and mass generation |
| Yukawa section | `D0.Matter.HiggsYukawaSectionTransfer` | finite Yukawa block map compatible with certified rank-2 scalar projector; no second mass anchor | Yukawa numerical fitting or PDG mass tables |
| Meson typed transfer | `D0.Matter.MesonDefectTransferAlgebra` | typed E x Gen carrier, C_chiFV self-adjoint/positive, flavour only via liftGen, 400 as seed | direct 400 promotion or generation-blind meson masses |
| toral automorphism / Galois balance | `D0.Dynamics.ToralAutomorphism`; `D0.Dynamics.GaloisConjugateBalance`; `D0.Dynamics.DarkSectorCoarseGrain` | fixed integer matrix `T=[[0,1],[1,-1]]` yields signed Lucas traces, determinant-square balance and even-window archive sign cancellation | PDG/cosmology data choosing `T`, or dark sector promoted as fitted missing component |
| spin-2 | TT quotient, concrete wave-operator, dynamics and DOF owners | TT representative, explicit `ePlus/eCross` projector, trace/gauge annihilation, two-polarization arithmetic and certificate-owned dynamics obligations | full Einstein equation derivation or continuum graviton QFT |
| gravity closure | `D0.Gravity.EntropicArchiveInterface`; `D0.Gravity.MacroEinsteinInterface` | finite graph/entropy cert, explicit Pi_TT and W_TT, higher-curvature cut, spectral A2/EH bridge and no continuum constants imported as core | smooth GR as primitive or fitted continuum constants |
| SM action | gauge and scalar action owners | finite action-term ledger and scalar/Yukawa admission after the constructive rank-2 projector | full smooth SM Lagrangian with RG running |
| cosmology | survey split owners | survey likelihood cannot choose the core cosmology object | fully reproduced survey likelihood without manifests and hashes |

A gate remains conditional where its owner is a certificate object rather than an
upstream derivation from earlier D0 primitives.

Gravity closure requires: finite graph/entropy cert; explicit Pi_TT and W_TT;
higher-curvature cut; spectral A2/EH bridge; no continuum constants imported as
core.

Scalar/Yukawa promotion is accepted only if it points to the constructive
rank-2 scalar projector theorem.  External Higgs mass, VEV, SM potential, or
PDG data cannot promote Yukawa core terms.


The compact owner index for the active priority gates is:

```text
Born finite effects:
  D0.Core.BornFiniteEffects
  finite_effect_born_readout_unique
  finite_coarse_born_readout_unique
  finite_tensor_born_readout_unique
  finite_power_readout_no_alternative

Concrete Book 04 selectors:
  D0.Matter.Book04ConcreteSelectors
  chargedLeptonElectronTerminalClaim
  electroweakDepth35Claim
  protonReadout306Claim
  neutronArchiveSiblingClaim
  betaUnlockDepth19Claim

Full-support Book 04 selectors:
  D0.Matter.Book04FullSupportSelectors
  electroweak_depth35_full_support_strict
  proton_readout306_full_support_strict
  beta_unlock_depth19_full_support_strict

Book 04 coefficient origin:
  D0.Matter.Book04CoefficientOrigin
  chargedLeptonCoefficientTableForced
  chargedLeptonCoefficientsNoFreeRetuning

Book 04 operator boundaries:
  D0.Matter.Book04OperatorBoundary
  nucleon_line_cannot_promote_full_baryon_multiplet
  lower_hodge_400_cannot_promote_meson_masses
  missing_scalar_projector_cannot_promote_higgs_yukawa_core
  D0.Matter.higgs_yukawa_requires_scalar_projector = SCALAR-PROJECTOR-CERT-CLOSED
  D0.Matter.HiggsYukawaSectionTransfer = YUKAWA-SECTION-CERT-CLOSED
  D0.Matter.MesonDefectTransferAlgebra = MESON-TYPED-TRANSFER-CERT-CLOSED

CKM basis-origin theorem:
  D0.Matter.CKMBasisOrigin
  ckm_origin_candidate_matrix_unique
  ckm_no_free_matrix_at_fixed_basis_origin
  closed at the finite selector level by `CKMBasisOrigin`

Generation-overlap origin:
  D0.Matter.GenerationSelectorOrigin
  D0.Matter.GenerationOverlapResponseOrigin
  d0_generation_selectors_force_nonpermutation_overlap
  vp_generation_selector_origin.py
  algebraic D0-origin closure, not a physical CKM external comparison protocol

Spin-2 finite quotient:
  D0.Geometry.FiniteWeakFieldQuotient
  finite_weak_field_quotient_yields_tt_representative
  finite_conserved_stress_spin2_coupling_closed

Spin-2 concrete wave operator:
  D0.Geometry.FiniteSpin2WaveOperator
  PiTT4_idempotent
  PiTT4_is_tt
  PiTT4_kills_trace
  PiTT4_kills_gauge
  WTT4_preserves_tt
  spin2_coupling_depends_only_on_tt_stress
  vp_finite_spin2_wave_operator_concrete.py

SM-facing gauge decomposition:
  D0.Gauge.SMGaugeDecomposition
  frozen_sm_generation_anomaly_free
  sm_eft_bridge_requires_frozen_decomposition

Cosmology reproducibility split:
  D0.Cosmology.SurveyReproducibilitySplit
  no BAO/DESI/SDE likelihood is allowed to promote to core cosmology closure

Tick-gauge / Lorentz strengthening:
  D0.Bridge.TickGaugeLorentz
  finite_lorentz_tick_gauge_cone_speed_closed
  may not introduce a second D0 propagation primitive
```

## 05.14 Sector verification protocols

### Foundations

Foundational claims must expose condensed/profinite support, a finite quotient or
finite carrier, an admissible morphism/operator family, projection/naturality
compatibility, and a positive response or invariant quotient.

### Action and vertices

Action claims must specify the gate, scene functional, single action section,
stationarity condition, and boundary/curvature response.  Runtime and witness
transport must remain finite.

### Matter and selectors

Matter claims are typed as support, selector, transfer, no-go or external comparison protocol.  Hodge
spectra, Schur complements and support seeds are not masses unless a sector
transfer is supplied.  Charged-lepton, CKM, proton/neutron and hadron claims must
state whether they are primitive derivations, finite certificates or bridge
comparisons.

### Electroweak sector

Electroweak claims must distinguish radial-depth closure, gauge-boson pole
comparison, scalar-projector admission, loop dressing and Higgs/Yukawa bridge.
An internal ratio is not a fully dressed electroweak fit.

### CKM sector

CKM verification has four stages:

```text
operator family -> basis selectors -> D0 ordinal/adjacency overlap origin -> finite mismatch matrix -> external convention comparison
```

No row/column convention, phase convention or RG bridge may be chosen after
comparison.  A permutation witness must be a full `Equiv.Perm` on generation
columns; independent row choices are not a CKM closure proof.

### Gravity and cosmology

Gravity and cosmology claims must distinguish archive geometry, weak-field
Poisson response, TT quotient, finite spin-2 dynamics, spectral/EH bridge,
archive entropy flow, survey transfer and external likelihoods.  BAO, DESI,
Hubble or S_DE comparisons are external comparison protocols only after the internal archive object is
frozen.

## 05.15 Falsification matrix

| Claim type | Failure mode |
|---|---|
| foundational algebra | contradiction in finite/profinite construction |
| condensed admissibility | uses a morphism outside halt/readout constraints |
| support spectrum | independent recomputation gives a different invariant |
| action operator | gate/scene functional is not stationary or not single-section compatible |
| Born/readout theorem | response is not positive, finite, quotient-stable or phase-consistent |
| selector theorem | another admissible support element satisfies the same score obligations |
| coefficient transfer | coefficient row changes without changing the declared origin |
| CKM bridge | matrix convention is chosen after comparison, a row-only permutation witness is used, or the comparison does not read the frozen matrix |
| baryon S3 carrier | a 3-dimensional vertex invariant is used as the decuplet instead of the 27-dimensional triple carrier |
| meson transfer algebra | edge-space and generation-space operators are added without a common tensor/lift carrier |
| Higgs/scalar | scalar terms are promoted without constructive rank-2 scalar-projector closure |
| spin-2 | scalar/vector/longitudinal modes couple as physical spin-2 under conserved stress |
| SM action | action term appears without finite ledger owner |
| cosmology external comparison protocol | data manifest, hashes, baseline or parameter-count ledger are missing |
| external bridge | scheme dictionary is incomplete or contains hidden repair parameters |

Spin-2 closure is accepted only with an explicit TT projector, a basis-wide
certificate on all ten elements of `Sym(4)`, trace and gauge annihilation,
the stress-coupling theorem, and no GR constants.  The public certificate name
is `vp_finite_spin2_wave_operator.py`; it checks the same concrete projector as
the Lean owner `D0.Geometry.FiniteSpin2WaveOperator`.

The operator/passport rule is strict: operator first, passport second, no PDG tuning, no geometry diagnostic as core source; Torus geometry is core; PDG shell alignment is passport and may not tune a core operator.

Failure is not hidden.  It is the operational meaning of the claim.

### 05.15.1 PDG Strict Passport Protocol

The Torus/Core13 split is now explicit:

```text
core:
  D0.Geometry.TorusCore13GeometryOrigin
  vp_torus_core13_geometry_origin.py

external comparison protocol:
  vp_core13_shell_geometry_passport.py
  vp_pdg_strict_external comparison protocol.py
```

PDG data can falsify or validate frozen D0 outputs.  PDG data cannot create D0
operators, tune torus radii, choose CKM conventions after comparison, or turn a
Core-13 shell fit into a core theorem.  Core-13 shell fit is an embedding
diagnostic.  Torus geometry is core; PDG shell alignment is external comparison protocol.  Holdout,
dataset pinning and multiple-testing rules are mandatory.  A geometry diagnostic
may not tune a core operator.

The optional `lucas_trace_layer_diagnostic` may compare downstream trace-layer residues, but it cannot choose the time operator `T` or promote PDG agreement to a toral-automorphism theorem.

## 05.16 Reproducibility requirements

Each public archive must include:

1. canonical book set;
2. theorem/status database;
3. claim-to-owner map;
4. primary certificate per active certificate-owned claim where available;
5. external data manifest for each empirical external comparison protocol;
6. reproducibility ledger with PASS, FAIL, MISSING_DATA, MISSING_MODULE,
   MANUAL_ONLY, STALE or EXTERNAL-DATA-REQUIRED;
7. retired-scaffold manifest outside active books;
8. one-command release runner for callable checks;
9. hash sidecars for packaged data and generated release artifacts.

A result that cannot be reproduced must be marked by its exact failure mode, not
absorbed into prose.

## 05.17 ABCD and capacity proof-cell rule

ABCD is not four decorative scalar equations.  A promoted ABCD claim must expose
an operator-cycle proof cell:

```text
condensed/profinite support;
finite quotient or carrier;
operator family;
projection/naturality compatibility;
positive response or invariant quotient;
negative controls for non-admissible alternatives.
```

Claims involving `ABCD`, `Ω8`, `V9`, `K(9,11,13)` or the `φ` split must expose the
capacity chain:

```text
D2 -> ABCD -> Ω8 -> V9 -> (V9,V11,V13)
```

and must state whether the resulting object is support, carrier, readout,
selector, action term or bridge input.

## 05.18 Bridge proof-cell rule

Bridge-facing claims require an executed proof cell, not bridge prose.  The
required fields are:

```text
internal finite object;
external projection/table/law;
response-test class;
coupling or forgetting kernel;
uniqueness or stationarity condition;
residual metric;
negative controls;
scheme or data manifest when external information is used.
```

A bridge may be promoted only after at least one of the following is executed:

```text
finite response grid;
retained response constraints;
explicit coupling/forgetting kernel;
entropy or stationarity proof selecting the kernel;
KKT, moment or trace residual checks;
convex-response or response-order checks;
one-command certificate run.
```

## 05.19 Gauge, matter and anomaly release rule

A gauge-carrier claim is not promoted by writing `8+3+1` or by naming Standard
Model factors.  It must expose the finite D0 isolation cell:

```text
support-shell decomposition;
shell non-mixing condition;
witness fixation;
compact block obligation;
chiral weak obligation;
abelian remainder obligation;
matter representation ledger;
discrete Ward or incidence identity;
exact anomaly sums;
EFT/RG dressing boundary.
```

A complete SM-facing claim must separate three layers:

```text
finite gauge/matter ledger;
finite action-term ledger;
smooth/EFT bridge.
```

Only the first two can be core claims.  The third is a bridge.

## 05.20 Empirical cosmology and survey rule

An empirical cosmology claim may not rely on archived result replay alone.  It
requires:

```text
internal archive object fixed before data;
observable-transfer map;
data manifest;
SHA-256 hashes;
one-command likelihood run;
ΛCDM or declared baseline;
negative controls;
parameter-count ledger;
failure thresholds.
```

A survey likelihood may evaluate a frozen D0 cosmology object, but it may not
create a new primitive, choose a hidden parameter or mutate the archive object.

## 05.21 Lepton magnetic-moment and precision bridge rule
A precision bridge claim must expose finite support, finite transport/trace readout, declared external scheme, uncertainty and negative-control protocol. Matching a central residual is not release evidence by itself.

## 05.22 Transition theorem promotion rule
A continuum transition claim must expose finite support, operator lock, finite algebraic/spectral certificate, bridge hypotheses, external dictionary and negative controls. A continuum word does not replace the finite theorem that feeds it.

## 05.23 What Book 05 proves
Book 05 proves the verification grammar of the corpus: D0 claim status is typed by construction, owner, bridge discipline and falsification hook. Every active claim must route to proof, no-go, certificate, bridge or demotion.

## 05.24 Editorial rule for this book
Book 05 is a coherent contract, not a release diary or storage box. Historical material belongs outside active books unless integrated into the relevant rule.

## 05.25 Standard-language and external-runner compression
D0-local terms are allowed in headings, Lean owners and cert names; prose must pair them with standard finite objects. External protocols run through `05_CERTS/DATA_RUNNERS/run_external_passports.py` and write `08_PASSPORTS/_RESULTS/`; PASS requires pinned data/hash/fields/baseline and no retuning.

## 05.26 Trace-heat-capacity and empirical no-go summary
Trace-heat-capacity gravity is split: core = detector ladder, Lucas traces, heat moments, scene counts and A/4 capacity; bridge = macro gravity witness. No-go controls include SRC scalar-only controls, LIGO spin-only, SPARC arbitrary-kernel repair, DESI root/window/H0/Omega_m/rd refit, continuum topology/theta primitives and continuum Yang-Mills mass-gap import.

## 05.27 CVFT operator admissibility
Closed-vacuum feedback uses `F_N=P_NU_N^\dagger Q_NU_NP_N` as feedback-return and `R_N=D_N^\dagger D_N` as positive readout. Allowed identities are `F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N)`, `F_N=P_N-(P_NU_NP_N)^\dagger(P_NU_NP_N)`, positivity and `F_N=0 iff Q_NU_NP_N=0`; `Q_N != 0 -> F_N != 0` is forbidden. Resolvent/log-det expansions require `|z|rho(F_N)<1` and `-log det`.

The partition function is `Z_N=Tr exp(-beta Delta_N(V)) det(I-zF_N(V))^{-1}` and feedback pressure uses finite `d_V`. Matter candidates may use `F_N psi=r psi`; complex masses/widths require `U_eff=P_NU_NP_N` or Feshbach-Schur. Baryon F3a/F3b/F3c are scaffold/spin-flavour/Core13-link certified before PDG labels.

## 05.28 v15 closure classes
Closure classes: `MASTER-BOOTSTRAP-CORE`, `GAUGE-BOUNDARY-LAW`, `HORIZON-EMISSION-LAW`, `EDGE-TRACE-COEFFICIENT-TARGET`, `SCALAR-PROJECTOR-CERT-CLOSED`, `YUKAWA-SECTION-CERT-CLOSED`, `MESON-TYPED-TRANSFER-CERT-CLOSED`, `SPIN-FLAVOUR-CARRIER-CERTIFIED`. Forbidden shortcuts: continuum volume derivative before finite halt, second mass anchor, rank-40 as full baryon carrier, rank boundary as A/4 proof, complex poles from bare positive `F`, PDG names before frozen poles, thermality as primitive horizon emission and alpha by post-hoc RG fit.

## 05.v15 Informational mechanics and seam closure classes

### Closure classes

- `ONTOLOGICAL-ENTRY-CLOSED`: the theory has a finite self-substrate entry principle with no external observer or background primitive.
- `INFORMATIONAL-MECHANICS-CERT-CLOSED`: a finite golden tick gate realizes stable self-similar trace production and retained/archive recursion.
- `CONTINUUM-ENVELOPE-CERT-CLOSED`: the continuous envelope is the semigroup generated by the logarithmic fractal tick.
- `TOPOLOGICAL-HALTING-CERT-CLOSED`: the signed terminal role cycle closes against the witness \(V_9\) to produce a finite halt quotient.
- `QUADRATIC-PEEL-CERT-CLOSED`: finite readout is the norm-square boundary peel \((QUP)^\dagger(QUP)\).
- `MEASUREMENT-HORIZON-LAW`: nonzero \(QUP\) defines a micro-seam; saturated seams define macroscopic horizons.
- `OPTICAL-JET-BACKREACTION-LAW`: saturated archive seams may emit through the positive conjugate operator \(QU^\dagger PUQ\).

### Forbidden primitives and shortcuts

The following are centralized rejected primitives: external vacuum background; external observer collapse; trace without \(Q_N\); motion without registration trace; global \(F_N=\varphi^{-2}P_N\) without a declared clock sector; linear subtraction model of time; black hole as information deletion; jet emission from a non-positive conjugate operator; horizon without capacity seam.
