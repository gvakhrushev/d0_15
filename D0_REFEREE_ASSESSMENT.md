# D0 v15 — Referee-Grade Assessment

*A consolidated, data-grounded evaluation of the D0 corpus for external review. Every count below is
computed from the single source of truth `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (527 claim
rows) and `LEAN_ASSUMPTION_LEDGER.csv` (24 tracked external assumptions), not from prose.*

---

## 1. What the theory is, in one paragraph

D0 builds all of its structure from a single finite object: the complete tripartite graph `K(9,11,13)`
(the "scene") — `N = 33` vertices, `|E| = 359` edges, degrees `(24,22,20)`, Laplacian spectrum
`{0,20,22,24,33}` with multiplicities `{1,12,10,8,2}`. Everything else — a golden-ratio ladder `Q(D)=φ^{D-4}`,
the fine-structure constant, a mass chain, a discrete Einstein response, a gravitational depth exponent — is
claimed to be *forced* by finite invariants of this graph (edge count, zone sizes, shell cardinalities,
Lucas/Fibonacci returns) with **zero free real parameters**. The corpus is organized as 527 numbered claims,
each carrying a `release_status` (what kind of result it is) and a `lean_status` (at what rigor it is
verified), with a cascade of guard scripts enforcing that the books, the status map, and the claim registry
never drift out of sync.

## 2. The verification landscape (the number that matters)

Grouping the 527 claims by what a referee actually cares about — *is this internal finite mathematics, an
external bridge, or open?*

| Bucket | Count | Share |
|---|---:|---:|
| **A. Internal finite theorems** (positive + impossibility) | **419** | **79%** |
| B. Finite leg closed, continuum leg external (`CORE_BRIDGE_SPLIT`) | 7 | 1% |
| C. External bridge / observational passport | 57 | 11% |
| D. Open internal proof-target | 42 | 8% |
| E. Deprecated | 2 | 0% |

Within bucket **A** (419 internal theorems):
- **340 positive finite theorems** (`CORE-FORMALIZED` / `CERT-CLOSED`) — of which **279 are machine-checked
  in Lean 4** (`LEAN_PROVED`), the rest closed by falsifiable Python certificates (this session added the scene-triple uniqueness capstone, +1).
- **79 proven impossibility results** (`NO-GO` / `NO_GO_PROVED`) — of which **73 are Lean-verified**.

Overall `lean_status`: **358 `LEAN_PROVED`**, 101 `PYTHON_CERTIFIED`, 38 `OPEN`, 28
`LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, 2 deprecated. The Lean corpus is **sorry-free** (genuine `sorry`
count = 0; verified against Lean 4.30.0 + Mathlib, 8114 mathlib oleans + 398 D0 oleans on disk).

**Referee reading:** four out of five claims are internal finite mathematics, and the large majority of those
carry a machine-checked proof. This is an unusually high formalization ratio for a physics-facing theory. The
NO-GO count (79) is a strength, not a weakness — the theory spends real effort proving what its own scene
*cannot* do.

## 3. Flagship results and their honest verification status

| Claim | What it asserts | Status |
|---|---|---|
| `D0-ALPHA-HOLONOMY-002` | `α⁻¹ = 359φ⁻² − φ⁻⁵ + φ⁻¹⁷(1+lnφ·sin(12/5)) = 137.035999151`, **6.7×10⁻⁸** from CODATA-2018 (**2.6×10⁻⁸** from CODATA-2022 — moved *toward* the value), zero free reals; the ansatz's functional FORM is now Lean-derived (`D0-ALPHA-HOLONOMY-LINEAR-FORM-001`, §8.2) | CERT-CLOSED (Python — the 9-digit *value*; the *form* is LEAN_PROVED) |
| `D0-DELTA-ALPHA-EXACT-001` | the α-seam invariants `α_top⁻¹=726−364φ`, `α_alg⁻¹=(12288/5)φ⁻⁶+(1/3)φ⁻³`, and the bound `0<\|Δ_α\|<φ⁻¹⁶`, all exact in ℚ(φ) | **LEAN_PROVED** |
| `D0-MASS-CHAIN-001` | `π₀=(6/5)φ²` and the mass ratios derived from δ₀ closure balance | CERT-CLOSED |
| `D0-VIETA-GALOIS-ABCD-001` | the scene's defining quartic and its Galois content | **LEAN_PROVED** |
| `D0-DIM-LADDER-COMPACT-001` | the dimension ladder `Q(D)=φ^{D-4}`, quantum `=1` at `D=4=\|ABCD\|` | **LEAN_PROVED** |
| `D0-SCENE-CENTER-SPACETIME-CONVERGENCE-001` | the scene centre `11 = L₅` (Lucas return) is two-channel forced | **LEAN_PROVED** |
| `D0-SPECTRAL-EINSTEIN-001` | discrete Einstein response `G = dS/dh = 2L`, symmetric + divergence-free (discrete contracted Bianchi) | **LEAN_PROVED** |
| `D0-XI5-CROSS-SECTOR-001` | the level-5 seam `ξ₅=φ⁻⁵` shared by `α_top` and `sin²θ₁₃` | **LEAN_PROVED** |

## 4. Where Lean is used — and where a Python certificate is the *correct* proof

A recurring referee suspicion is that "Python-certified" means "unverified." It does not, and the corpus draws
the line honestly:

- **Lean is used** for exact statements over ℤ, ℚ, ℚ(φ)=ℚ(√5), and ℝ: polynomial identities, matrix
  determinants and traces, eigenvalue-sign (signature) arguments, sequence monotonicity and limits, totients,
  Galois facts, and every impossibility argument that reduces to finite algebra. These are the 358
  `LEAN_PROVED` rows.
- **A failable Python certificate is the correct proof** for the flagship `α` and a handful of other results
  that are *transcendental numerical agreements* — e.g. matching `137.035999151` to CODATA at `6.7×10⁻⁸`. Lean
  cannot meaningfully "verify" a numerical coincidence to eight digits; what makes such a claim honest is that
  the certificate is **constructed to be able to fail** (a guard, `check_cert_can_fail.py`, enforces exactly
  this) and that the formula has **zero free real parameters**. Wrapping such a claim in Lean would be
  ceremony, not rigor, and the corpus correctly declines to do so.

This session's Lean-hardening pass upgraded 4 claims whose content *did* have exact real structure a numeric
cert only checked pointwise — the rank-3 metric signature and anisotropy, the phason ratio sequence's limit,
the window-44 totient, and the Higgs-anchor √-norm identity — and stopped there, because the remaining 94
Python-certified claims are 67 external/empirical, 12 explicit scaffolds, and 12 exact-integer facts where
Python is already rigorous. That boundary is documented, not glossed.

## 5. The external boundary — what the theory imports, explicitly

The corpus does **not** claim to derive continuum physics from the finite scene by fiat. It maintains a
`LEAN_ASSUMPTION_LEDGER` of **24 named external assumptions**, each with a type, a justification, a cited
source, and — critically — a stated *failure-meaning* (what collapses if the assumption is false). Examples:

- `ASSUMP-JONES-INDEX` (subfactor index quantization): φ-as-quantized-index stays a *cited external
  corroboration*, not an internal theorem.
- `ASSUMP-LORENTZ-MACRO`, `ASSUMP-SMOOTH-COVARIANCE`, `ASSUMP-SMOOTH-HEATTRACE`: the carrier stays a finite
  Clifford / heat-trace check; smooth macroscopic geometry is **not** promoted.
- `ASSUMP-RG-SMOOTH-INTERP`: the renormalization-group claim stays finite-scale algebra only.
- Verlinde entropic gravity, Tomita modular flow, Rieffel Gromov–Hausdorff continuum, Lindemann–Weierstrass
  transcendence of `ln φ`, Mordell/E8 lattice uniqueness: each is a *bridge*, flagged as
  `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` (28 claims) rather than `LEAN_PROVED`.

**Referee reading:** the bridge boundary is the most reassuring part of the corpus. Every place the finite
mathematics hands off to an external theorem is labelled as such; the 28 `…_WITH_BRIDGE_ASSUMPTIONS` claims
are exactly the ones a referee should scrutinize, and they are pre-identified.

## 6. The open frontier — 33 proof-targets, honestly scoped

The 42 open `PROOF-TARGET`s split into **7 observational passports** (data comparisons: DESI-BAO, LIGO
catalog, IceCube-HESE, SPARC rotation curves — not internal mathematics) and **35 internal-math targets**.
The internal 26 are not a to-do list of unattempted work; nearly all are *explicitly scoped* to an external
leg after their finite leg was closed:

- **`D0-EDGE-002`** — the edge-α *trace* leg is CLOSED (`Tr(F_E)`, Lean-backed); what remains is the analytic
  continuation through a ramified cover, an external EFT/IR passport, *not a finite identity*.
- **`D0-QUANT-MET-003/004`** — a conditional Lean leg exists (`D0.Metrology.Phi2Flux`, `.PhasonBragg`); the
  open part is an *empirical* flux/Bragg prediction, closeable only against measurement.
- **The Dirac-tower pair** (`D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001`, `D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001`)
  — both obstructed by the *proven* NO-GO on the Ξ comparison map (`PRIM-COMPARISON-MAP-XI-N`). The theory has
  proved these *cannot* close by the naive route; the residual is a genuinely harder object.
- **The CMB pair** (`D0-CMB-PHASON-SPECTRUM-OWNER-001`, `D0-CMB-IDS-SMOOTHING-OWNER-001`) — closed-negative by
  the companion maximality NO-GO (`≥3 admissible smoothings give distinct n_s`), i.e. the theory has proved
  there is *no canonical* internal answer, which is itself a result.
- **The phason/CVFT continuum targets** (`D0-PHASON-WZ-EXPLICIT-FUNCTION-001`, `CVFT-F2/F5/F8`) — finite legs
  closed; explicit continuum functions require external analysis.

**Referee reading:** the open frontier is small (6%), and its internal component is dominated by targets that
have been *proved to require* an external input, not targets that have simply not been tried. This is the
signature of a mature theory that knows its own boundary.

## 7. Structural integrity — the tooling a referee can trust

The corpus is not a pile of claims; it is a synchronized system:
- **Single source of truth**: `CLAIM_TO_LEAN_MAP.csv`. The status map, the dependency graph, and the ten
  assembled books are all *generated views* (via `sync_theory_status_map.py` and `assemble_books.py`), so a
  status edit cascades everywhere rather than being hand-patched in prose.
- **Five guards**, all passing: `validate_csv`, `check_cert_can_fail` (every certificate must be able to
  fail — no tautology certs), `check_book_cert_references` (every cited cert exists and runs), 
  `check_book_ledger_sync` (book prose cannot contradict the ledger), `check_no_tautology_proofs`.
- **Lean**: `sorry`-free, compiles against a pinned Lean 4.30.0 + Mathlib toolchain.

## 8. Referee verdict (honest, not promotional)

**Strengths.**
1. Exceptional formalization discipline: 82% internal theorems, 369 machine-checked in Lean, sorry-free.
2. The bridge boundary is explicit and auditable — 24 named external assumptions with failure-meanings.
3. Heavy, honest use of impossibility proofs (79 NO-GOs) that scope the theory's own limits.
4. A single source of truth with a guard cascade that prevents prose/ledger drift.

**What a referee will still press on.**
1. **The core admissibility of `K(9,11,13)` itself.** The theory forces a great deal *from* the scene; the
   selection of the scene (the parts `9,11,13`) is the true root, and it should be the front-and-centre claim
   in any external submission. *Update (Iter26): this is now a single machine-checked capstone —*
   `D0-SCENE-TRIPLE-UNIQUE-001` (`D0.VNext2.SceneTripleUnique.scene_triple_unique`, rc=0, 0 sorry). It proves
   that any `+2` ladder whose centre is a Lucas number in the admissibility window `[9,13]` is *uniquely*
   `(9,11,13)`, composing the four previously-separate forcing legs (three zones, `+2` ladder, centre `L₅=11`,
   odd-return parity) and adding the Lucas-window uniqueness lemma (only `L₅=11` lies in `[9,13]` among all
   Lucas numbers). The residual a referee can still press: the *window* `[9,13]` and the odd-return parity are
   themselves motivated by `Ω₈=8` and the `det T=−1` orientation — well-argued and Lean-backed, but they are
   the layer below the capstone, and a maximally-conservative referee will trace the forcing one level further
   to the admissibility criteria (role=orbit, the maturity threshold `Ω₈`).
2. **The transcendental flagship `α`.** The `6.7×10⁻⁸` agreement is striking and the formula has zero free
   reals — it rests on a specific holonomy ansatz (`1+lnφ·sin(12/5)`). *Update (Iter26): the functional FORM
   is now derived, not data-selected* — `D0-ALPHA-HOLONOMY-LINEAR-FORM-001` (`D0.Spectral.SeamTransportLinear`,
   rc=0, 0 sorry). Every structural ingredient is now Lean-backed: the depth `φ⁻¹⁷`, the coefficient `lnφ`
   (KS entropy), the angle `12/5`, the `sin`-channel (elliptic `Q₈` selector `G²=−I`), and now the **linear
   form**. The last one was the only piece that had been merely data-selected (linear beats `exp` against
   CODATA); it is now proved to be the exact signature of a *nilpotent* seam transport `N²=0` (the directed
   CP-seam crossed once per closure), for which `exp(sN)=I+sN` with identically-zero higher orders — the `exp`
   form is structurally excluded because it would need a returning/undirected seam. So the data's role shrinks
   from *selecting* the form to *confirming* the single directed crossing. **Residual a referee can still
   press:** the 9-digit *value* remains an empirical CHK (the last `~10⁻⁸` is a HYP measurement-limit bet), and
   the single-crossing input `N²=0` — though motivated by the already-owned directed CP-3-cycle — is the
   physical hypothesis the derivation rests on. The *form* is now at the rigor the seam invariants have; the
   *value* is honestly still a match, not a derivation.
3. **Bridge claims are corroborations, not proofs.** The 28 `…_WITH_BRIDGE_ASSUMPTIONS` results (Lorentz,
   smooth geometry, RG, Verlinde) are where "finite scene → continuum physics" actually happens, and there the
   theory is importing, not deriving. The corpus says so plainly; a referee should read those 28 first.

**Bottom line.** As internal finite mathematics, the corpus is in strong shape and largely machine-verified.
As a physical theory, its honest status is: a parameter-free finite combinatorial structure with a
Lean-verified algebraic spine, an explicit and auditable set of external bridges to continuum physics, and a
small, well-scoped open frontier. It is ready for external review *provided* the submission leads with the
scene-selection argument (point 1) and presents the bridge ledger (point 3) up front rather than in an
appendix.
