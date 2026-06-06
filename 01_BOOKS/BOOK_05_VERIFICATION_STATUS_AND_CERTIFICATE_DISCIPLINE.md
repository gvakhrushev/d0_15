# BOOK 05 — Verification, Proof Ownership, and Certificate Discipline

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
explicit external external comparison protocol with frozen internal input.
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
support в†’ operator в†’ theorem/cert в†’ book integration в†’ optional external comparison protocol в†’ ledger status.

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
CKM basis label => physical CKM angles and CP phase
frozen coefficient row => mass derivation from primitives
BAO/DESI/SDE fit => new D0 primitive
status label changed => theorem closed
selected number written in a table => finite selector theorem
support seed 400 => pion/kaon/rho masses
baryon support gap => full baryon multiplet
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

The formal verification owner is `05_CERTS/vp_gap_labeling_d0_tiling_hull.py`, which must print `PASS_D0_GAP_LABELING_TILING_HULL`. The underlying Lean formalization of gap stability is checked by `D0.Matter.KTheoryGapLabeling`.

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

## 05.11a Risky prediction external comparison protocol discipline

IceCube, LIGO, CMB, BAO and galaxy-lensing external comparison protocols require:
1. data manifest;
2. hash;
3. frozen D0 prediction;
4. parameter-count ledger;
5. no hidden retuning.

The certificate owners are `05_CERTS/vp_phason_domain_wall_mesons.py` (`PASS_PHASON_DOMAIN_WALL_MESONS_K0_LABELS`), `05_CERTS/vp_ckm_phason_holonomy_k0.py` (`PASS_CKM_PHASON_HOLONOMY_K0`), and `05_CERTS/vp_phason_flip_entropy_sde.py` (`PASS_PHASON_FLIP_ENTROPY_SDE_GAP_LABELS`). They must run under this frozen regime.

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
- direct 400в†’mass meson failure;
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

## 05.13 Current v14 priority gates

Sync token: ## 05.13 Active priority gates.

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

The operator/external comparison protocol rule is strict: operator first, external comparison protocol second, no PDG tuning,
and no geometry diagnostic as core source.

Failure is not hidden.  It is the operational meaning of the claim.

### 05.15.1 PDG Strict Passport Protocol

The Torus/Core13 split is now explicit:

```text
core:
  D0.Geometry.TorusCore13GeometryOrigin
  vp_torus_core13_geometry_origin.py

external comparison protocol:
  vp_core13_shell_geometry_external comparison protocol.py
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

Claims involving `ABCD`, `О©8`, `V9`, `K(9,11,13)` or the `П†` split must expose the
capacity chain:

```text
D2 -> ABCD -> О©8 -> V9 -> (V9,V11,V13)
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
О›CDM or declared baseline;
negative controls;
parameter-count ledger;
failure thresholds.
```

A survey likelihood may evaluate a frozen D0 cosmology object, but it may not
create a new primitive, choose a hidden parameter or mutate the archive object.

## 05.21 Lepton magnetic-moment and precision bridge rule

A lepton anomalous magnetic-moment bridge claim must expose:

1. finite lepton support shell;
2. finite transport or holonomy operator;
3. positive response / trace readout;
4. external scheme such as on-shell, lattice-HVP, dispersive-HVP or another
   declared convention;
5. QED/EW/HVP/HLbL decomposition being compared;
6. residual D0 trace operator;
7. uncertainty and negative-control protocol.

Matching a central residual is not release evidence by itself.

## 05.22 Transition theorem promotion rule

A claim connecting D0 to Lorentz invariance, renormalization flow, smooth
geometry or continuum field theory must expose a transition proof cell:

```text
finite support;
operator lock;
finite algebraic or spectral certificate;
bridge hypotheses;
external dictionary;
negative controls for non-admissible limits;
statement of what remains bridge-level.
```

Transition claims must not be promoted by analogy.  A continuum word does not
replace the finite theorem that feeds it.

## 05.23 What Book 05 proves

Book 05 proves the verification grammar of the corpus:

```text
D0 claim status is typed by construction, owner, bridge discipline and falsification hook.
```

It does not prove every sector formula.  Instead it prevents sector formulas
from being overstated, under-typed or promoted by analogy.  Its success condition
is not a longer table.  Its success condition is that every active claim in the
other books has a visible route to proof, no-go, certificate, bridge or demotion.

## 05.24 Editorial rule for this book
Book 05 must stay a coherent contract. Historical material may be preserved outside active books, but it must not be appended into Book 05 as a raw dump. A lost rule from an older draft must be integrated into the relevant section above or left outside the active corpus.
The active book is therefore neither a release diary nor a storage box. It is a single audit instrument.

## 05.25 Standard-language compression rule
A D0-local term is allowed in a heading, Lean owner or certificate name.
In explanatory prose, the first occurrence must be paired with its standard
object, and subsequent occurrences should use the standard object unless the
D0 mnemonic prevents ambiguity.

## 05.25 Trace-heat-capacity gravity verification row
`trace-heat-capacity gravity` is accepted only as a split status block: core = fixed detector ladder, signed Lucas traces, even Lucas heat moments, Lefschetz scene counts and A/4 boundary capacity; bridge = macro gravity interface through the finite gravity witness; excluded = continuum singularity primitive, fitted dark component or fitted smooth-GR constant. The certificate `05_CERTS/vp_trace_heat_capacity_gravity.py` checks black-hole capacity saturation as boundary encoding.
QUASI-002 phason/baryon verification gate: `05_CERTS/vp_quasi002_phason_strain_generations_baryon.py` must check the rational S3 projector, rank `10`, invariance and the negative control that nucleon-line extrapolation remains forbidden. IceCube comparison is EMPIRICAL-PASSPORT and cannot select or tune the D0 neutrino kernel.

## 05.26 External data external comparison protocol runner
External empirical external comparison protocols are executed through `05_CERTS/DATA_RUNNERS/run_external_external comparison protocols.py`, which writes `08_PASSPORTS/_RESULTS/external_external comparison protocol_summary.json` and `.md` with the fixed columns `Passport; Dataset; Manifest; Hash; Frozen D0 object; Baseline; Metric; Result; Notes`.
The runner covers Nuclear SRC, IceCube, SPARC halo, CMB, BAO/S_DE, LIGO/GWOSC, CKM and Meson PDG. A missing or partial external manifest must produce `SKIP`, not empirical `PASS`; `PASS` requires pinned dataset/hash/fields/citation/policy plus comparison of the frozen D0 object against the declared baseline without retuning.
Current machine summary: Nature 2026 SRC and GWOSC/LIGO mass-defect are `PASS`;
IceCube HESE has event energy/direction data and a generated D0 curve but still
requires an exposure/flux baseline; SPARC is downloaded and parsed, while the
minimal shape/global-scale archive kernel currently fails diagnostics and is not
promoted. The remaining external rows remain `SKIP_*_DATA_REQUIRED`. The machine
source is `08_PASSPORTS/_RESULTS/external_external comparison protocol_summary.json`.

SRC destructive rule: A-only / N-Z-only SRC scalar fails. Any nuclear SRC model
that promotes mass number, neutron excess or density alone to a core SRC
operator fails the Nature 2026 negative control. The admitted D0 owner is the
shell-contact selector.

D0-SRC-NOGO-001 -- A-only / N-Z-only SRC scalar failure. The admitted owner is
`D0.Matter.NuclearShellContactSRC`: occupied shell projectors pass through the
angular-momentum contact selector into the SRC contact trace.

D0-LIGO-NOGO-001 -- Spin-only mass-defect failure. The GWOSC clean-BBH run uses
the frozen horizon-capacity determinant formula and beats both the mean-loss
baseline and the spin-only negative control.

D0-SPARC-NOGO-001 -- Naive archive-phason halo kernel failure. The first SPARC
run rejects both simple shape-only and one-global-scale kernels. Future
dark-sector halo operators must pass the same SPARC runner without per-galaxy
halo tuning.

D0-GRAV-DSS-NOGO-001 -- Smooth Monotone Collapse Failure.
Purely smooth monotone collapse cannot represent the full critical black-hole
threshold, because the threshold admits a DSS echo lattice (PRL 2026,
arXiv:2601.14358). The certificate is `05_CERTS/vp_critical_collapse_dss_echo_lattice.py`.
The typed no-go lives in `D0.Gravity.CriticalCollapseDSS`.

D0-BH-CAP-NOGO-001 -- Singularity-as-information-deletion rejected.
Black-hole horizon cannot be read as deletion of information. The terminal archive
quotient makes active readout inaccessible while preserving total finite dimension/trace.
Certificate: `05_CERTS/vp_black_hole_capacity_a4_witness.py`. Lean: `D0.Gravity.BlackHoleA4EntropyWitness`.

D0-COSMO-SDE-NOGO-001 -- BAO root/window refit forbidden after DESI failure.
The DESI/BAO real-data run failed for the frozen S_DE transfer.
The internal roots lambda_c and lambda_r remain fixed.
Post-hoc refitting of roots, window centers, window widths, H0, Omega_m or r_d
is forbidden as a core repair.
Certificate: `05_CERTS/vp_desi_bao_sde_failure_diagnostics.py`.

D0-TOPO-CONTINUUM-NOGO-001 — continuum master equations are bridge objects, not core primitives.
D0-TOPO-NOAXION-001 — continuum theta-vacuum rejected as D0-core primitive (CONDITIONAL-CLOSED: exact annihilation theorem conditional on finite exact-density annihilation predicate).

D0-GRAV-FINITE-MINCUT-NOGO-001 — continuum RT surface / minimal surface is a bridge object; finite min-cut is the D0 core object.
D0-GAUGE-SEAM-NOGO-001 — continuum Yang-Mills mass-gap claim is not D0-core; finite seam obstruction gap is the admitted finite theorem.
D0-MATTER-BARYON-SCAFFOLD-001 — tick/S3 baryon asymmetry is a conditional scaffold only; full cosmological baryogenesis requires external model (not closed).

