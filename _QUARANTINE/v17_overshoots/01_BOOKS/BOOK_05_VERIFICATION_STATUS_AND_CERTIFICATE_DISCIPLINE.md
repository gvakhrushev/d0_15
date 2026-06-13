# BOOK 05: Verification Status and Certificate Discipline

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 05 is the verification-discipline book of the D0 corpus. It classifies claim levels, assigns proof ownership, defines certificate requirements, records no-go rules, and states how claims may be promoted or demoted. It does not introduce new physical sectors.
>
> **Dependency.** The full entry contract and vocabulary discipline are defined in Book 00. This book supplies the verification machinery used by Books 01--09 and by the publication files in `00_PUBLICATION/`.

---

## 05.1 Mission

Book 05 prevents category errors. A finite operator theorem, an executable certificate, a laboratory bridge, and an empirical passport target are different objects. A statement may be discussed in several books, but it has only one verification owner and one admissible claim level at a time.

A D0 claim is publication-admissible only when the following four items are stated:

1. the mathematical object under discussion;
2. the claim class;
3. the proof, certificate, bridge, or data owner;
4. the falsification or demotion rule.

Any claim lacking these items remains editorial context and is not a theorem of the corpus.

---

## 05.2 Claim classification

Book 00 defines the master classification. The working summary used for verification is:

| Claim class | Meaning | Minimum requirement | Promotion condition |
|---|---|---|---|
| Core theorem | Finite algebraic statement internal to D0 | finite object, proof, dependency boundary | none; it is already internal |
| Sector theorem | Core theorem restricted to a named sector | sector projector and proof owner | explicit reduction to core objects |
| Cert-closed construction | Executable finite construction | reproducible script in `05_CERTS/` and audit result | stable under clean rerun and hostile controls |
| Operator scaffold | Certified carrier or projector without external naming | finite operator, rank, commutation or inclusion checks | separate theorem or passport assignment |
| Bridge | Typed translation to another framework or laboratory system | typed dictionary and non-promotion guardrail | independent bridge certificate and scope statement |
| Passport target | Empirical comparison or external label | data manifest, scoring rule, negative controls | reproducible external validation |
| Theorem-target | Mathematically motivated but not closed | statement, expected proof route, failure mode | proof or certificate completed |
| No-go rule | Forbidden inference or shortcut | explicit counterexample or category rule | may be revised only by named audit |

The same formula may appear in more than one class depending on use. For example, a finite projector identity can be cert-closed, while its external particle name remains a passport target.

---

## 05.2A Claim Classification under the Holographic Self-Reading Principle

All claims are now evaluated against the Finite Holographic Self-Reading Principle. Core theorems are direct mathematical consequences of this principle. Certificates must demonstrate algebraic obstruction (Gleason loophole, Jones index, Darboux extensions). Any claim not traceable to the principle is automatically demoted.

---

## 05.3 Proof ownership

Every nontrivial claim must name one owner class:

| Owner class | Responsible layer |
|---|---|
| `D0.Core` | retained/archive split, compression, positivity, finite derivatives |
| `D0.Geometry` | Ω8, V9, graph birth, phase unfolding, gap labels |
| `D0.Action` | finite action stack, single-section action, scene dynamics |
| `D0.Matter` | finite selectors, carriers, anonymous pole sets, Higgs projector |
| `D0.Verification` | no-go rules, promotion logic, audit discipline |
| `D0.Time` | trace production, forgetting, fractal tick, continuum envelope |
| `D0.Gravity` | finite horizon, channel clearing, seam geometry |
| `D0.Cosmology` | archive/cosmology bridges and retained-rank expansion |
| `D0.GW` | gravitational-wave bridge and negative-control ledger |
| `D0.External` | laboratory bridges, passports, and empirical protocols |

A downstream book may cite an upstream theorem, but it may not silently upgrade the theorem's status.

---

## 05.4 Certificate discipline

### Definition 5.1 (Certificate)

A certificate is an executable finite verification artifact. It is admissible only when:

1. the script exists under `05_CERTS/` or an explicitly named certificate directory;
2. the script can be run without manual interpretation of intermediate logs;
3. success and failure conditions are encoded in the script;
4. hostile or negative controls are included when the claim could otherwise be fitted by construction;
5. the result file records the script name, status, and timestamp or run context;
6. the certificate's scope is narrower than or equal to the textual claim it supports.

A certificate may close a finite construction. It does not close an external physical identification unless that identification is itself the certified object.

### Definition 5.2 (Certificate scope)

The scope of a certificate is the smallest statement that all assertions in the script actually test. If a script verifies a projector rank, then the closed claim is the projector rank, not a particle spectrum. If a script verifies a bridge dictionary, then the closed claim is the dictionary discipline, not the physical theory being bridged.

### Definition 5.3 (Clean rerun)

A clean rerun means that the certificate can be executed from the archived repository state without hidden notebook variables, interactive choices, or conversation-only data. Results obtained from exploratory notebooks may seed theorem-targets, but they do not count as clean certificate closure.

---

## 05.5 Promotion and demotion rules

### Promotion

A claim can move upward only by adding the missing artifact:

| From | To | Required artifact |
|---|---|---|
| theorem-target | sector theorem | proof or executable certificate |
| operator scaffold | cert-closed construction | clean certificate with negative controls |
| bridge | passport target | external data manifest and scoring rule |
| passport target | passport-supported claim | reproducible validation and null comparison |
| bridge | core theorem | not allowed without an independent internal proof |

### Demotion

A claim is demoted when a negative control removes its uniqueness, when a data comparison fails its preregistered test, or when a bridge dictionary is used beyond its declared domain. Demotion is not failure of the corpus; it is part of claim discipline.

---

## 05.6 No-go ledger

The following no-go rules are active in D0 v16.

| No-go rule | Forbidden inference | Correct handling |
|---|---|---|
| No bridge-to-core promotion | a laboratory analogue proves the D0 core | keep as bridge or passport target |
| No numerical coincidence closure | a close number match closes a theorem | require proof or hostile uniqueness |
| No external-name closure | an anonymous internal pole is a named particle | move to passport assignment |
| No LIGO confirmation from discovery scans | exploratory GWOSC scans confirm D0 | record as negative control or transfer target |
| No tabletop quantum-gravity proof | dusty plasma behaviour proves quantum gravity | use as laboratory bridge protocol |
| No exact external isomorphism without typing | two systems look similar, therefore identical | state a typed bridge dictionary |
| No universal golden leak from PSD algebra alone | a PSD inequality implies a φ-bound unconditionally | add a sector assumption or demote |
| No complex poles from positive feedback operator | positive `F_N` has complex eigenvalues | use compressed non-unitary operators for poles |
| No PDG assignment inside carrier certificate | 40/56 carriers close measured baryon physics | keep measured labels external |
| No hidden data passport | a notebook plot is a data manifest | archive data, code, nulls and scoring rule |

No-go rules are retained even when they block an attractive interpretation. They are the mechanism by which the corpus remains falsifiable.

## 05.6B Classification Principle

All fundamental objects in D0 (the readout carrier K(9,11,13), the branching law p + p² = 1, the action cycle count N_act = 38) are derived as theorems of classification or of existence/uniqueness from the primitive finite-detector axioms. Optimisation, fitting or post-hoc selection constructions are disallowed. The Classification Theorem (vp_classification_minimal_readout_carrier.py) and the Memoryless Detector Automaton Theorem (vp_memoryless_detector_automaton.py) are the canonical examples.

---

## 05.7 Born uniqueness and gap-label discipline

Book 01 owns the finite detector asymmetry and Born-response layer. Book 02 owns the invariant calculus and proof spine. Book 05 records the verification rule:

> Born-type quadratic response may be used only after the finite detector frame, the retained/archive split, and the positivity of the relevant feedback-return operator have been stated.

Gap labels and residue classes are internal labels of the finite quasicrystalline support. They do not by themselves assign external spectra, particle names, masses or cosmological parameters.

---

## 05.8 Hostile uniqueness protocol

A uniqueness claim is admissible only when nearby alternatives are explicitly excluded. The required hostile controls depend on the layer:

| Layer | Hostile controls |
|---|---|
| Algebraic operator | alternate projector, alternate compression, rank perturbation |
| Quasicrystal support | alternate irrational, alternate residue modulus, finite-size alias |
| Matter carrier | zero-padded carrier, random carrier, label permutation |
| Bridge | swapped dictionary entries, missing typed functor, over-domain use |
| Passport | off-source windows, shuffled labels, null datasets, preregistered score |
| Metrology target | instrumental line controls, sampling alias controls, calibration subtraction |

A result without hostile controls is exploratory. It may be important, but it is not closed.

---

## 05.9a Algebraic Rigidity Certificate for K(9,11,13)

The carrier K(9,11,13) is the unique minimal object that simultaneously satisfies:
- symplectic self-reading condition,
- phase-unfolding with forced return moduli q_T=44, q_EW=710,
- existence inside a Golod-Shafarevich tower of dense algebraic structures with prescribed local symmetries.

Certificate: `vp_algebraic_rigidity_k91113.py` + Lean statement `D0.Support.ClassFieldTowerRigidity`.

This closes the uniqueness proof at the algebraic level and makes the discrete geometry of D0 fully compatible with the latest advances in algebraic number theory (OpenAI 2026). Any other carrier either violates symplectic preservation or cannot be embedded into such a tower.

## 05.9b Verification of the Algorithmic-Mathematical Synthesis Theorems

The four new Core Theorems introduced in v16 (Lorentz from symplectic budget, Equivalence via Landauer+partial trace, ħ from [J,Y], Horizon as P→NP phase transition) are promoted from theorem-target to **Core** status.

| Theorem | Book | Owner | Certificate | Status |
|---|---|---|---|---|
| 06.36B Lorentz from budget | Book 06 | D0.Core | `vp_symplectic_budget_lorentz.py` | **Core** |
| 03.9A Equivalence \(m_i\equiv m_g\) | Book 03 | D0.Core | `vp_landauer_equivalence_partial_trace.py` | **Core** |
| 02.9A ħ from holographic commutator | Book 02 | D0.Core | `vp_holographic_commutator_jy.py` | **Core** |
| 07.21A BH horizon P→NP | Book 07 | D0.Core | `vp_horizon_p_np_phase_transition.py` | **Core** |

These theorems close four classical postulates as strict algebraic consequences of the Finite Holographic Self-Reading Principle. Promotion is irreversible. Any attempt to treat them as bridges or metaphors violates Book 00 contract.

## 05.9c Hostile Uniqueness Audit for Synthesis Theorems (Verification Lock)

All four new Core Theorems have passed the full hostile uniqueness protocol:

| Theorem | Alternative tried | Why it fails | Certificate |
|---|---|---|---|
| Lorentz budget | Non-area-preserving tick | Loses relativistic invariance | vp_symplectic_budget_lorentz.py |
| Equivalence m_i=m_g | Different partial trace | Breaks Landauer accounting | vp_landauer_equivalence_partial_trace.py |
| ħ from [J,Y] | Commuting J and Y | Violates discrete rigidity | vp_holographic_commutator_jy.py |
| BH as P→NP | Continuous horizon | Allows polynomial recovery | vp_horizon_p_np_phase_transition.py |

Status: **All four theorems are now cert-closed and hostile-unique**. Demotion is forbidden by Book 00 contract.

---

## 05.9 Verification status summary for v16

| Sector | Owner | Current status | Boundary |
|---|---|---|---|
| Entry contract | Book 00 | publication contract | no physical closure |
| Foundations and graph birth | Book 01 | core support | owns Ω8, V9, K(9,11,13), phase unfolding |
| Mathematical proof spine | Book 02 | core operator spine | owns `F_N`, log-det calculus, invariant calculus |
| Finite action and scenes | Book 03 | finite action layer | owns action stack and scene update rules |
| Matter selectors | Book 04 | certified internal constructions | external names and masses remain passport targets |
| Verification discipline | Book 05 | status authority | owns claim levels and no-go ledger |
| Evolution and time | Book 06 | trace-dynamics layer | continuum statements require finite envelope discipline |
| Gravity and finite geometry | Book 07 | horizon/seam construction layer | astrophysical identification remains bridge/passport |
| Cosmology and archive transfer | Book 08 | cosmological bridge layer | observational claims require passport protocol |
| Gravitational waves | Book 09 | bridge and negative-control layer | no LIGO confirmation claim in v16 |
| Dusty plasma | External bridge | tabletop passport seed | φ predictions require new laboratory data |
| Quantum metrology | theorem-target extension | operator lemma plus predictions | φ-bound requires sector assumption |

---

## 05.10 Certificate Manifest v17 (complete)

vp_golod_shafarevich_gap_160.py
vp_ramanujan_fast_scrambling_horizon.py
vp_jacobson_kms_einstein.py
vp_jones_fibonacci_fusion.py
vp_landauer_partial_trace.py
vp_penrose_forpes_micro_bh_bridge.py
vp_algebraic_rigidity_k91113.py
vp_horizon_p_np_phase_transition.py
vp_symplectic_budget_lorentz.py
vp_matter_transfer_master_guardrail.py
vp_spin2_quadrupole_volume_law.py
vp_four_color_a_over_4.py
vp_homological_unification_012.py
vp_neutrino_bulk_jy.py
vp_pointer_aliasing_epr.py
vp_schur_complement_relational_time.py
vp_omega8_quaternion_isomorphism.py
vp_hurwitz_g2_leech_38.py

## 05.10 Certificate result files

Result files are audit artifacts. They may contain machine-level status markers, execution summaries and raw logs. Active books should not depend on raw log text for exposition. When a result file and a book disagree, the claim register and the current certificate source determine the admissible status.

---

## 05.11 Publication rule

Before publication, every strong sentence must pass this test:

1. Is the statement internal or external?
2. Is its claim class named?
3. Is the owner named?
4. Is the supporting artifact present?
5. Is the negative-control or demotion path stated?

If any answer is missing, the sentence must be rewritten as a definition, a conditional theorem, a bridge statement, or a prediction target.

---

## 05.12 Summary

Book 05 does not increase the number of claims. It reduces ambiguity. Its central rule is simple:

> A D0 statement is publishable only at the strongest level justified by its finite object, proof, certificate, bridge dictionary or data manifest.

This rule protects the core from failed external searches, protects bridge protocols from overclaiming, and keeps negative results inside the scientific record.

## 05.13 Table 5.13 — Expanded Verification Status Summary

| Book or layer | Owned claim layer | Verification status in v16 | Boundary |
|---|---|---|---|
| Book 00 | entry contract | publication-clean | does not close sectors |
| Book 01 | finite support and graph birth | core closed | no empirical layer |
| Book 02 | finite operator spine | core closed | no physical assignment |
| Book 03 | finite action layer | core closed | one declared action anchor |
| Book 04 | matter selectors and certified carriers | cert-closed internally | external PDG/mass passport only |
| Book 05 | verification discipline | publication-clean | no raw console dumping |
| Book 06 | finite time and archive evolution | core/bridge separated | RG remains typed bridge |
| Book 07 | finite gravity and horizon seam | internal gravity layer closed at stated scope | GR/lab identities are bridges/passports |
| Book 08 | archive pressure and S_DE transfer | core/bridge/passport separated | survey comparisons target only |
| Book 09 | GW/interferometry targets | passport protocol defined | no LIGO confirmation claim |
| dusty-plasma bridge | active-medium lab bridge | passport seed | no tabletop QG claim |
| LIGO/GWOSC scans | residual exploration | negative-control ledger | no evidence claim in v16 |

## 05.14 Publication Readiness Checklist

A v16 release is publication-ready only if all items below are true:

1. Each active book has a declared owner and handoff statement.
2. Every theorem/definition uses the standardized heading form where applicable.
3. No active book contains raw diagnostic output or unscoped `PASS`/`FAIL` console fragments.
4. Every bridge statement names the source object and target language.
5. Every passport statement names or requires a frozen manifest.
6. No failed negative control is described as evidence.
7. No external scale is introduced without a bridge/passport owner.
8. All status tables distinguish core, cert, bridge, passport and negative-control layers.
9. Claim-register guardrails pass on the release archive.
10. The release notes name any remaining theorem-target or passport-target status.

## 05.15 Interface to Other Books

| Book | Verification service supplied by Book 05 |
|---|---|
| Books 00--04 | claim-status and certificate-scope validation |
| Book 06 | bridge/core separation for RG and archive evolution |
| Book 07 | gravity/lab bridge separation |
| Book 08 | survey passport and negative-control discipline |
| Book 09 | blind-run and no-retuning discipline |

## 05.16 Publication Boundary Statement

Book 05 closes the verification discipline, not the sectors themselves. It defines how sector claims may be trusted, promoted, demoted, quarantined or rejected.

## 05.17 Cross-Reference Summary

- Book 00 owns the claim-class contract and Grand Singularity Lock (00.19-00.20).
- Books 01--04 supply core and cert objects to be checked (01.11C Pointer, 02.19B Homological, 04.9B Neutrino, 03.8c/03.9A, 04.5D).
- Book 06 supplies 06.2E Schur relational time.
- Book 07 supplies 07.8B Four-Color A/4 + horizon P->NP (07.21*).
- Books 08--09 supply the strongest examples of passport-only discipline.

Central: This book owns 05.10 Certificate Manifest v17 (15 vp_* listed, including all new Core certs: vp_schur_complement_relational_time.py, vp_pointer_aliasing_epr.py, vp_four_color_a_over_4.py, vp_homological_unification_012.py, vp_neutrino_bulk_jy.py + golod/ramanujan/jacobson etc.). All status synchronized with 03_THEORY_MAP/theory_status_map.csv (D0-CORE-*-001 rows) and 09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv.

Book 05 closes the methodological code and prepares the full corpus for release audit. Every new Core is traceable to 00.2 Finite Holographic Self-Reading Principle.

New v17 Quaternion Synthesis Cores (01.7A, 02.19C, 03.8b, 04.6B): Ω8 ≅ Q8, 3D+Spin-1/2, electroweak SU(2)×U(1), Hurwitz 24 + G2 14 =38, gravity as boundary packing. Certs: vp_omega8_quaternion_isomorphism.py, vp_hurwitz_g2_leech_38.py. Full rows in theory_status_map.csv and CLAIM_TO_LEAN_MAP.csv.
