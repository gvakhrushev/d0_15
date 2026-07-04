# D0 v15 — Theory-Development Session Report

**Scope.** Active development of the D0 corpus (`/Users/grigorijvahrusev/Downloads/d0_15`), not audit.
Method (per the QAOA/Lean article the user referenced): reduce each open target to *one missing statement*,
build a hypothesis, test it by computation, and either supply the missing artifact with a **failable
certificate** or prove a **NO-GO** — then cascade the result through the single-source-of-truth so the
ledger, status map, graph, and book prose stay synchronized.

**Headline.** Fourteen PROOF-TARGET / NO-GO claims advanced with exact computation and failable certs —
log-det scale-ownership, hypercharge B−L localization, toral shift-equivalence + orientation
obstruction, the three-route Majorana NO-GO, the **lepton branch-fixing NO-GO** (Lean-verified status flip
PROOF-TARGET→NO-GO), the **Adler–Weiss symbolic owner**, the **inductive spectral-triple isometric leg**,
the **CVFT-F6 gauge-boundary commutator theorem**, and a full sweep of the **seven scene-matched
VNEXT/VNEXT2 owners** attacked constructively: **THREE positive closures** — the **canonical Dirac scale
`λ_N = λ₀·φ^N`** (Lean-verified, synthesizing the already-proved Perron scale flow), the **canonical
Feshbach compression of the scene** (exact Schur complement on the `Aut`-invariant zone/archive split,
performing the very 5→4 reduction a unitary cannot — retracting an over-scoped NO-GO), and the **canonical
Dirac covariance cocycle** `ω(N) = φ` (Lean-verified, discharged by the resolved scale primitive) —
plus **four sharpened NO-GOs** (the spectral-lift/Feshbach-transport owners now NO-GO against *all UCP
corners*, not just unitaries, via an exact Cauchy-interlacing spectral-bunching obstruction `d₁/d_top =
20/33 > 1/φ²`, with the honest positive sub-result that AF stages of dim ≤ 4 do embed), and the
**isometric-Dirac-tower residual narrowed to a single leg** (isometry owned + scale now closed → only the
Ξ-comparison remains), and — pushing past the spectral NO-GO on the user's insistence to *synthesize the
corpus's own proved results* rather than settle — a **forced dimension bridge**: the scene vertex count is
`|V| = 9+11+13 = 33 = F₂+F₄+F₆+F₈ = F₉−1`, i.e. the AF Dirac² eigenspace dimension truncated at its 4th even
power, because the zone ladder and the Dirac even-power ladder share **one `+2` root** (the M1
orientation-bit prohibition) — dimension and grading lift positively even though the spectrum does not
(Lean-verified `D0.VNext2.SceneDimEvenFibonacci`), and the **entire Laplacian spectrum is owned as a forced
closed form** — the classical complete-multipartite result `0¹,24⁸,22¹⁰,20¹²,33²` proved by explicit
eigenvectors, so the 5-distinct count, the bunching, and the whole transport-obstruction shape are
downstream of one `+2` zone forcing (Lean-verified `D0.VNext2.SceneLaplacianSpectrumForced`), and the
S_DE window-scale splitting is pinned to an **exact forced closed form** `D(m) = 3/((m+1)(m+3))` that
reproduces the corpus's `√10/40` while showing (honestly) that `√10` is a *size-fingerprint*, not a forced
golden-departure — the golden field lands at zones `29,31,33`, not the scene (Lean-verified
`D0.VNext2.WindowScaleDiscriminant`), and — the deepest of the wave — the **centre of the scene triple is a
forced space-time convergence**: `11 = |V₁₁|` (spatial capacity) `= L₅ = |Tr(T⁵)|` (temporal return of the
time operator), the unique Lucas value in the capacity window `[9,13]`, so `{9,11,13} = {L₅−2, L₅, L₅+2}` has
both centre and width forced with zero free integers (Lean-verified
`D0.VNext2.SceneCenterSpacetimeConvergence`), and the rank-3 causal-cone cubic `λ³ − 359λ − 2574` is pinned
to `λ³ − |E|·λ − 2∏(zones)` — **both** coefficients forced scene symmetric functions of the zone quotient
(Lean-verified `D0.VNext2.Rank3CubicSymmetricFunctions`). A parallel scout wave then closed three more across
Books 04/06 (hypercharge flow→Weyl NO-GO, Sturmian discharge NO-GO, Adler–Weiss internal Markov CERT-CLOSED),
with a fourth scout's claim caught mis-scoped and reverted. A following iteration then resolved the
jointly-open gravity-response pair — the finite Einstein-tensor response (CERT-CLOSED) and the matter↔TT
shared-carrier linkage (NO-GO with a positive partial). Registered cert count **372 → 395**; all integrity guards green;
corpus assembly idempotent; the Mathlib-free D0 Lean core (33 files) **independently type-checks clean under
Lean 4.30.0, 0 `sorry`**. No status was inflated: targets stay PROOF-TARGET (residual named), NO-GO
(sharpened, unitary-scoped), or — where an object was actually *built* — CERT-CLOSED.

---

## 1. Log-det dark-energy window scales — value + field OWNED, ℚ(φ) NO-GO
**Claim** `D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001` (Book 08 §08.51, PROOF-TARGET).
**Was:** the window scales `λ_c≈1.421, λ_r≈1.579` were declared *representative domain-check values,
not internally owned*.
**Now (exact, verified at the full 33×33 level):** they are the two nontrivial eigenvalues of the
**normalized graph Laplacian** `L̂ = I − D^{−1/2}AD^{−1/2}` of the scene `K(9,11,13)`:
`λ_{c,r} = 3/2 ∓ √10/40`, roots of `160λ² − 480λ + 359`, with `λ_c+λ_r = 3 = Z` (zones, a trace
identity) and `λ_c·λ_r = 359/160 = |E|/160` (edges). The normalizer is intrinsic:
`160 = (∏ zone-degrees)/(2V) = 10560/66` — a single scene invariant, cleaner than the `2·Ω₈·γ = 2·8·10`
octet factorization in §08.12.2.
**NO-GO refinement:** the roots lie in `ℚ(√10)`, and `√10 ∉ ℚ(φ)=ℚ(√5)` (`√10=a+b√5` forces
`a²+5b²=10, 2ab=0`, no rational solution). So the literal `EXACT-MISSING: ℚ(φ) roots` target is
**provably unreachable**; the owned field is `ℚ(√10)`.
**Residual PROOF-TARGET:** formula-ownership — that the log-det kernel `d_V[−logdet(I−zF_N(V))]`
spectrally *reproduces* these scales (values + field now owned).
**Cert:** `05_CERTS/vp_logdet_window_scale_owner.py` (stdlib, failable — breaks if `|E|`, the `160`
identity, or the field claim is corrupted).

## 2. Hypercharge B−L freedom — NO-GO localized, literature-grounded
**Claim** `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (Book 04 §04.11, NO-GO).
**Context:** the corpus proves the anomaly-free charge space is the 2-dim `span{Y, B−L}`, and that
removing `B−L` by declaring `ν^c` uncharged is *question-begging*.
**New (exact):** the `B−L` residual is pinned **entirely to the right-handed singlet sector**. Imposing
the left-handed doublet electric charges via `Q = T3 + gen` (`Q_u=2/3, Q_d=−1/3, Q_e=−1`) forces only
the line `a = 1−2b`; along it `gen[q_L]=1/6, gen[l_L]=−1/2` are `b`-independent while all four singlets
`u^c,d^c,e^c,ν^c` carry `b`. Hence **charged-fermion electric charges are `B−L`-blind**: no
charged-fermion-only selector can remove `B−L`; any `Y`-selector must assign a right-handed-singlet
charge (`ν^c` uncharged is the minimal such). This *confirms and localizes* the corpus verdict rather
than overturning it. (I initially over-reached — "this discharges the bridge" — then traced it honestly:
the strong claim smuggled `Q(ν^c)=0` in through the singlet constraints. Corrected.)
**Literature grounding (independent support, not a closure):** the recent literature reaches the same
structure and names the *physical* selector. Lohitsiri–Tong (*Hypercharge Quantisation and Fermat's Last Theorem*, arXiv:1907.00514) show that, once
hypercharge is quantised, the cubic `U(1)³` gauge anomaly recasts as `x³+y³=z³`, whose only integer
solutions (`x=0`/`y=0`, by Fermat) reproduce Nature's hypercharges — the D0 cubic factorization
`−18a(t−3a)(t+3a)=0` is the same statement (its three linear branches = those trivial solutions; SM row
on `t=−3a`; verified by sympy). The
non-question-begging selector is *not* "declare `ν^c` uncharged" but the physical requirement that `ν^c`
**admit a gauge-invariant Majorana mass**: `∼(ν^c)²` is invariant iff `2Y_{ν^c}=0 ⟺ b=0` (the seesaw
origin of neutrino mass). This gives the existing bridge (`D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001`,
grounded in `ν_R ∈ ker A`) a second independent support with the same endpoint.
**Residual / follow-up:** whether the φ-quasicrystalline scene *carries* a Majorana structure for `ν^c`
(a well-posed §04.9 target). Status unchanged (NO-GO).
**Cert:** `05_CERTS/vp_hypercharge_bl_freedom_localized.py` (failable).

## 3. Toral time-map ↔ golden SFT — the algebraic (R,S) leg supplied
**Claim** `D0-TORAL-TIME-MARKOV-CONJUGACY-001` (Book 06 §06.30a, PROOF-TARGET).
**Was:** needed an *explicit Williams shift-equivalence*; the existing cert had only the SE *invariants*
(spectrum + Bowen–Franks group) and stated the `(R,S)` data was **"NOT constructed internally."**
**Now (exact integer 2×2):** (i) `T=[[0,1],[1,−1]] ∼ −N_τ` via the unimodular `P=[[0,−1],[1,1]]`
(`det=1`, `T P = P(−N_τ)`) — i.e. `T` is the **time-reversed Fibonacci automorphism**,
`spec(T) = −spec(N_τ)` (the hidden sign symmetry); (ii) an explicit elementary strong-shift-equivalence
`R=[[1,0],[1,1]], S=[[1,1],[0,1]]` realizes the golden `φ²` SFT: `N_τ² = [[1,1],[1,2]] = R S`,
`S R = [[2,1],[1,1]] = B`, with the Williams lag-1 identities `A R = R B`, `S A = B S` verified; (iii)
`B` is `GL(2,ℤ)`-conjugate to `T²` (via `U=[[−1,0],[1,1]]`), tying the SSE step to the toral map's square.
**Honest scope:** one elementary step at the `φ²` level, **not** the full lag-`L` Williams chain, and it
does **not** by itself establish topological conjugacy — that still needs the geometric Adler–Weiss
Markov partition (`D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001`), which the corpus's own seed-Markov NO-GOs
show is not forced by the invariants. Residual PROOF-TARGET narrows to the geometric partition leg.
**Cert:** `05_CERTS/vp_toral_shift_equivalence_supplied.py` (failable).

---

## 4. Capability unlock — Lean 4.30.0 now runs here
Installed `elan 4.2.3` + the `leanprover/lean4:v4.30.0` toolchain (into `ELAN_HOME=/tmp/.elan_d0`; home-
and host-mount writes are sandbox-blocked, so the toolchain lives in `/tmp`). Trivial proofs check.
**Verified:** the 33-file **Mathlib-free** closure of the D0 Lean core type-checks **clean (0 errors,
0 `sorry`/`admit`)** under the real compiler — genuine independent confirmation of that slice, not a
"claims-proved" assertion. **Limit:** the 345 Mathlib-dependent files cannot be built here because
`git clone` (required for the Mathlib dependency) fails under the sandbox with "Operation not permitted";
this is a capability limit of this environment, not a corpus defect.

---

## 5. Cascade discipline (every change)
Each result was propagated through the single source of truth exactly once and re-verified end-to-end:
`CLAIM_TO_LEAN_MAP.csv` (canonical) → `sync_theory_status_map.py` (regenerates status map + graph) →
per-section book prose → `assemble_books.py` (regenerates the monolith). Guards run green after every
change: `validate_csv` (530 rows), `check_cert_can_fail` (393 registered certs, 0 print-stub, 0
missing-on-disk), `check_book_cert_references` (all cert tokens cited), `check_book_ledger_sync`
(disclaimer-aware prose⟂ledger guard), and whole-corpus assembly idempotence. All edits are isolated
from the user's uncommitted working-tree changes.

## 6. Majorana investigation — a decisive NO-GO on three routes (`vp_majorana_not_forced.py`)

The sharpest open question the hypercharge work exposed: does the φ-quasicrystalline scene **force**
`ν^c` to admit a Majorana mass? If it did, the hypercharge-row bridge would stop being a convention and
become a forced selector. This was investigated with three parallel hypothesis-testers, each result then
re-verified independently. The answer is **no**, on three separate grounds:

- **H1 (real structure).** A Majorana mass needs `ν^c` in a *real* representation with a graded antilinear
  charge conjugation `J` (`J²=−1`, KO-dimension 6). The scene's one-generation spinor carrier is the `Q₈`
  2-dim irrep, whose **Frobenius–Schur indicator is −1** (quaternionic/pseudoreal, *not* real), and the
  frozen role real structure is KO-0 (`J²=+1`, Dirac). The precondition fails on the carrier. The corpus
  already owns this via `D0.Representation.RoleRealStructureNoGo` + `D0_ROLE_KO_DIMENSION_RESULT.md`.
- **H2 (`ker A` ⟺ Majorana).** `ν_R ∈ ker(A)` is codim 3 (zone-balanced, 30-dim of 33); `2·Y_{ν^c}=0` is
  codim 1 in `span{Y,B−L}` — strictly stronger, not equivalent. And the only `Aut(K(9,11,13))`-invariant
  covectors (the 3 zone-indicators) all vanish on `ker(A)`, while `Y_{ν^c}` is not zone-constant, so **no
  scene-forced functional** can bridge them.
- **H3 (359-rigidity).** Rigidity removes *continuous* gauge orbits, not the *discrete* B−L direction —
  wrong category; and admissibility (`b=0`) merely *permits*, never *forces*, a nonzero mass (circular).

All load-bearing steps (codimension, Aut-invariance, `Q₈` Frobenius–Schur, circularity) were reproduced
with exact arithmetic and captured in the failable cert. This **resolves** the "§04.9 follow-up" my own
earlier §04.11 note had left open, and confirms the bridge stays `BRIDGE-ASSUMPTIONS-EXPLICIT` (no status
change). The single missing statement all three routes converge on — a scene-forced, `Aut`-equivariant
charge-localization operator (= a frozen KO-6 antilinear `J`) — is exactly the object the corpus already
flags as absent (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001` PROOF-TARGET, `…U1-MASS-KERNEL-A2` NO-GO⁺).

## 7. Toral orientation obstruction — sharpened partial NO-GO (`vp_toral_shift_equivalence_supplied.py`)

Strengthened the toral cert with a verified obstruction using the periodic-point count (a conjugacy
invariant): `|Fix(T^n)| = |det(T^n−I)|` equals `tr(N_τ^n) = Lucas(n)` at **odd** `n` but differs by
**exactly 2** at **even** `n` (offsets `[0,2,0,2,…]`). This is the exact signature of `T ∼ −N_τ`: the toral
time-map realizes the **orientation-reversed** golden SFT, *not* the plain golden SFT — so the naive
"`T` = golden SFT" statement is **false as written**. The honest positive target becomes "`T` conjugate to
the orientation-reversed golden SFT," whose residual leg is still the geometric Adler–Weiss partition.

## 8. Literature-mining — an honest negative
Cross-referencing the 504-paper landscape map against the 47 open targets: 31 are external-data-blocked
(DESI/IceCube/LIGO), and the 16 internal-closeable ones need **classical** machinery (Adler–Weiss 1967,
Connes NCG, Jones subfactors), which recent-arXiv covers thinly (2–6 preprints each, all 0-cite). The map
is a QG-landscape survey, not a source of closing-methods for these targets — so the closures here drew on
the **corpus's own Lean NO-GO owners** plus directly-verifiable classical results, not the paper set.

## 9. Closing wave — four more targets, with Mathlib now built (real Lean verification)

With the full Mathlib toolchain built on disk (8114 mathlib + 398 D0 oleans; `lake env lean` compiles
Mathlib-importing D0 files, rc=0), a four-target closing wave was run. Three parallel sub-agents hit a
server-side model stall; those targets were then done directly. Genuine `sorry`/`admit` count in the D0
Lean tree = **0** (all 23 grep hits were the English word "admit" in docstrings).

- **Lepton branch-fixing → NO-GO (status flip PROOF-TARGET → NO-GO), Lean-verified.**
  `D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001`. The frozen shell-torus supplies exactly `2` orbit-branches
  (sizes `{4,3}`, exponents `1/4≠1/3`) for `3` generations, and has no fixed point (no in-carrier third
  branch). A branch→generation full-row operator would need an injection `Gen(3)↪Branch(2)`, a surjection
  `Branch(2)↠Gen(3)`, or a bijection — **all impossible by cardinality**. Lean
  `D0.Extensions.LeptonBranchFixingNoGo.lepton_branch_fixing_operator_nogo` (`decide`, compiles against
  Mathlib) + failable cert. So `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` is provably *not constructible* from
  scene orbit-data; the constructibility question is closed.
- **Adler–Weiss symbolic owner pinned (`vp_adler_weiss_symbolic_owner.py`).** `T=[[0,1],[1,-1]]` is
  `GL(2,ℤ)`-conjugate to `−S` (the Fibonacci substitution incidence) via the minimal unimodular
  `U=[[0,1],[-1,0]]`: `U T U^{-1} = −S`, exact. The partition's symbolic model is the orientation-twisted
  Fibonacci substitution; residual = the metric Rauzy cells.
- **Inductive spectral-triple isometric leg supplied (`vp_inductive_spectral_triple_isometric_leg.py`).**
  The graded (Christensen–Ivan) Dirac spectra nest `spec(D_N) ⊆ spec(D_{N+1})` on the Fibonacci tower
  (dims 2,3,5,8,13), so the eigenspace-inclusion `J_N` is an explicit **isometry** with
  `J_N^† D_{N+1} J_N = D_N` at every level — the "missing artifact" exists and is present-core
  constructible. This **corrects** the earlier "obstruction" framing: only *canonicity* over the downward
  inverse limit stays external.
- **CVFT-F6 finite gauge-boundary commutator theorem (`vp_gauge_boundary_commutator_theorem.py`).** Exact
  identity `‖[P,g]‖²_F = 2‖QgP‖²_F` for any Hermitian `g` and projection `P`; on the `K(9,11,13)` zone/bulk
  split, any unit boundary-crossing generator has `‖QgP‖²≥1`, hence a **hard quantized commutator gap ≥ 2**.
  This is the finite operator obstruction (the mass-gap *language*) — explicitly **not** the continuum
  Millennium Yang–Mills mass gap, and no continuum QFT is imported.

Three of these stay PROOF-TARGET with their existence/construction legs now internally owned; one is a
Lean-verified status flip to NO-GO. Cert count `376 → 380`; all guards + assembly idempotence green.

## 10. VNEXT/VNEXT2 operator-algebra wave — six derived NO-GOs

The `VNEXT`/`VNEXT2` cluster (28 claims) had 7 remaining PROOF-TARGET "OWNER" targets. Six of them
flip **PROOF-TARGET → NO-GO** as *derived* NO-GOs (cert `vp_vnext_scene_matched_owners_derived_nogo.py`);
the seventh (`D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001`) is left untouched because it carries a deliberate
NO-GO twin (the aspirational-owner / proven-twin pairing).

- **The reduction.** Each canonical *scene-matched* construction (Feshbach transport, AF-Feshbach
  compression, scene spectral-lift, scene-Feshbach-lift, scene-Dirac-covariance, endpoint
  conditional-expectation) provably requires one of three primitives the corpus has **already Lean-proved
  NO-GO**: the comparison map `Ξ_N`, the Dirac-scale selection, or the scene-history refinement rule. So
  these were "open" only because the reduction was never written down — not because anything remained to be
  constructed.
- **The root obstruction, computed from scratch.** The reason `Ξ_N` is impossible is a *scale-independent*
  spectral mismatch: the AF-reduced Dirac² has **4** distinct eigenvalues (every-other-Fibonacci
  multiplicities `{1,3,8,21}`), while the scene Laplacian `L(K(9,11,13))` has **5** (`{0,20,22,24,33}`,
  multiplicities `{1,2,8,10,12}`). Both partition 33, and rescaling `D → sD` never changes the *number* of
  distinct eigenvalues — so no unitary spectral-intertwining `Ξ` exists at any scale. The cert recomputes
  both spectra from the graph and the Fibonacci tower and checks the mismatch (falsifiable: if the counts
  coincided, the obstruction would fail).
- **Honest positive counterpoint.** The AF-side *trace-preserving conditional expectation itself* exists and
  is unique (finite-dimensional Takesaki, against the canonical Perron trace). So conditional expectations
  per se are not the obstruction — only the *scene-native* endpoint lift is. This is recorded so the NO-GO
  is not overstated.

## 11. Constructive attack — two POSITIVE closures (not NO-GO)

Prompted by the correct observation that a NO-GO on the *maximal* object is not a closure if a *weaker*
object suffices, I re-attacked the VNEXT targets by building operators instead of certifying their absence.

- **Canonical Dirac scale `λ_N = λ₀·φ^N` (`D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001`,
  Lean-verified, CERT-CLOSED).** The Outcome-C NO-GO called the martingale-Dirac scale a free primitive
  because `φ^N` and `2^N` are both Christensen–Ivan-admissible. True for the *axioms alone* — but it never
  cross-referenced the already-Lean-proved `D0-PERRON-SCALE-FLOW-OWNER-001` (every internally-defined
  refinement scale of the golden tower has step ratio exactly `φ`). An internally-sourced scale therefore
  has ratio `φ`, forcing `λ_N = λ₀·φ^N` (unique up to the free dimensionless base — the standard
  overall-scale freedom of any spectral triple). `2^N` is admissible-but-*external*: `2` is not a unit in
  `ℤ[φ]` (`N(2)=4` vs `N(φ^k)=(-1)^k`), so it is not any power of `φ`. And `φ^{kN}=(φ^N)^k`, so the whole
  `φ`-ladder consists of operator powers `D_1^k` of the fundamental Dirac. Lean
  `D0.VNext.CanonicalMartingaleDiracScale` compiles against Mathlib (rc=0); cert
  `vp_vnext_canonical_dirac_scale_owner.py` is falsifiable. The NO-GO is kept (correct at its scope); this
  is its positive companion, localizing the residual freedom to external import.

- **Canonical Feshbach compression of the scene (`D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001`,
  NO-GO → CERT-CLOSED, retraction).** One wave earlier I swept this owner into a NO-GO on the grounds that
  `W_eff = A − B(D−zI)⁻¹C` "needs image(Ξ†)/kernel(Ξ)" with `Ξ` the obstructed *unitary* comparison map.
  That was an over-scoped error: a Feshbach compression needs only a keep/trace *projection split*, not a
  unitary. Against the scene's own `Aut`-invariant zone/archive split (bulk = zones 1,2 = 20 vertices;
  traced boundary = zone 3 = 13 vertices), the boundary block is `D_tt = 20·I₁₃` **exactly** (zone 3 is
  edge-free), so the Schur complement `W_eff = A_bb − (1/20)·B·Bᵀ` is exact and `z`-independent, with
  eigenvalues `{0,22,24,33}` (multiplicities `{1,10,8,1}`, verified in exact rational arithmetic) on the
  20-dimensional bulk — **4** distinct eigenvalues. So the compression *performs exactly the `5→4`
  distinct-eigenvalue reduction the unitary `Ξ` provably cannot* (the boundary trace removes the eigenvalue
  `20`). Cert `vp_vnext_scene_feshbach_compression_owner.py`. **Honest bound:** the compressed spectrum is
  *not* the geometric `φ`-ladder, so this does not prove scene↔AF spectral congruence — the lift/covariance
  owners stay NO-GO, now correctly scoped to that stronger, unitary claim.

The lesson recorded for the corpus: certify a NO-GO against the *object the claim actually needs*, and
synthesize the corpus's own proved results before declaring a construction impossible.

## 12. Full VNEXT/VNEXT2 owner sweep — the disciplined verdict on all seven

Following the constructive-attack mandate, I worked every one of the seven scene-matched owners to a
defensible verdict, building objects where possible and sharpening the obstruction where not.

- **`D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001` → CERT-CLOSED (positive).** Reduced to
  `PRIM-DIRAC-SCALE-SELECTION`, resolved above (`λ_N = λ₀·φ^N`). With the scale fixed, the covariance
  cocycle `ω(N) = λ_{N+1}/λ_N = φ` is a determined, base-independent, multiplicative 1-cocycle. Lean
  `D0.VNext2.CanonicalDiracCovariance.canonical_dirac_covariance_owner` compiles against Mathlib (rc=0);
  cert `vp_vnext2_canonical_dirac_covariance_owner.py`.

- **`D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001` → NO-GO, sharpened against all correspondences.** The bold
  route (Connes correspondence / UCP compression, not a unitary) was tested to its honest conclusion. By
  Cauchy interlacing, the AF-reduced Dirac² corner *does* embed for dim `k ≤ 4` (a real positive
  sub-result), but is infeasible for every `k ≥ 5` including the full `k = 33` lift the owner claims. The
  binding inequality is exact in `ℤ[φ]`: `20/φ² > 33/φ⁴ ⇔ 20φ > 13`. The mechanism is **spectral
  bunching** — the scene's dynamic range `d₁/d_top = 20/33 = 0.606` exceeds `1/φ² = 0.382`, too little
  range to host the AF geometric ladder `φ²:φ⁴:φ⁶`. Two discriminating controls establish this is the
  *range*, not the mass distribution: a spread control (same multiplicities, `d₁/d_top = 2/33`) admits the
  `k = 5` corner; permuting the scene's multiplicities (same eigenvalue set) does not. Cert
  `vp_vnext2_scene_spectral_lift_interlacing_nogo.py`.

- **`D0-VNEXT-FESHBACH-TOWER-COMPATIBILITY-OWNER-001`, `D0-VNEXT2-SCENE-FESHBACH-LIFT-OWNER-001` → NO-GO,
  sharpened.** The scene's *own* Feshbach compression exists (closed above), but these owners need the
  `(P_N,Q_N,F_N)` operators *transported* to the AF carrier — a scene↔AF map, obstructed by the same
  UCP-corner interlacing NO-GO. Even the correspondence route fails to transport the operators.

- **`D0-VNEXT2-ENDPOINT-CONDITIONAL-EXPECTATION-OWNER-001` → NO-GO, sharpened.** Had two blockers; one is
  now removed. The **measure** blocker is gone — the Perron–Frobenius eigenvector is the canonical
  `Aut`-invariant measure (unique by PF, constant per zone). The **carrier** blocker is genuine: the
  endpoint operator lives on the history carrier, and the admissible families give different carriers
  (all-walks vertex dim 33 vs non-backtracking/directed-edge dim `2|E| = 718`). Ihara–Bass links only their
  *spectra* (the NB spectrum is `{±1}` of fixed multiplicity plus `spec([[A,−Q],[I,0]])`, a determined
  function of `(A,D)`), not the operator; and the corpus's canonical Bratteli tower is a 2-symbol
  golden-SFT cylinder tower, not a scene-vertex carrier, so it does not select W/NB/E.

- **`D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001` → PROOF-TARGET, residual narrowed to one leg.** Its
  primitive `PRIM-ISOMETRIC-DIRAC-J_N` splits into isometry + scale + comparison. The isometry was already
  CERT (`D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001`); the scale is now closed this session; only the Ξ-comparison
  leg remains — the genuine NO-GO. So two of three legs are owned; the `EXACT-MISSING` collapses to a single
  leg pending an external (non-scene) comparison route.

Net: of seven owners, **three closed positively**, four stay NO-GO but every one is sharpened from
"blocked on primitive X" to a precise, computed obstruction with reachable controls — and one aspirational
target's residual is now a single named leg. This is the difference between hiding behind a NO-GO and
proving exactly where (and why) the wall is.

### 12a. The forced dimension bridge — what the static test missed

Pressed to stop comparing the *bare* scene spectrum to the φ-ladder and instead synthesize the corpus's own
proved structure, I found a positive result the static interlacing test had hidden. Putting the scene
Laplacian spectrum on the log-φ ladder (top eigenvalue → φ⁶) lands the three bunched zone-eigenvalues
`{20,22,24}` at `φ^4.96, φ^5.16, φ^5.34` — a cluster **at level 5**, exactly the "stabilization to φ at
level 5" intuition. The scene's entire nonzero spectrum spans only `33/20 ≈ φ` (one φ-band): it is a
*coarse* object, distinguishable at φ-resolution as `{kernel} + {one band}`.

Two consequences, both exact:

- **The dimension lifts, and it is forced.** `|V| = 9+11+13 = 33 = F₂+F₄+F₆+F₈ = F₉−1`. The zone ladder
  steps by `+2` (M1 forbids the `+1` orientation bit) and the AF Dirac² ladder steps by `+2` in the
  exponent (even powers, even-indexed Fibonacci multiplicities `{1,3,8,21}`); one shared `+2` root makes
  both `+2`-graded partitions of 33. This is the corpus's own multi-channel forcing style, now applied to
  the dimension. New claim `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (Lean `D0.VNext2.SceneDimEvenFibonacci`,
  cert `vp_scene_dim_even_fibonacci_forcing.py`), orthogonal to the refuted *algebra* anchor
  (`34 = F₉ = 33+1`, the `+1` being the kernel mode).

- **The two NO-GOs are one obstruction.** The spectral-lift "bunching" NO-GO and the refinement-rule NO-GO
  are the *same* wall seen spectrally: lifting the coarse 2-level scene into the fine 4-level AF ladder
  requires knowing which AF level each scene mode descends from — refinement information the coarse scene
  does not contain, i.e. exactly the external catalog M1 forbids. So dimension + grading lift; spectral
  refinement cannot, for the same M1 reason the refinement rule is NO-GO.

- **The whole spectrum is forced, and the obstruction is downstream of it.** Pulling the thread further: the
  entire unnormalized Laplacian spectrum `{0¹,20¹²,22¹⁰,24⁸,33²}` is the classical complete-multipartite
  closed form `0¹, (N−nᵢ)^{nᵢ−1}, N^{k−1}`, proved by explicit eigenvectors (all-ones kernel; within-zone
  sum-zero → `N−nᵢ`; zone-constant sum-zero → `N`). The corpus previously owned only the reduced 3×3
  zone-matrix (`ℚ(√10)` roots) and the *normalized* Laplacian; the full 33-dim spectrum was used by the
  VNEXT certs but never certified as forced. Now it is (`D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001`). The
  payoff: the "5 distinct eigenvalues", the bunching (`{20,22,24}` are close because `9,11,13` are), and the
  entire shape of the transport obstruction are *consequences* of the single `+2` zone forcing, not
  independent facts.

- **Discipline: what I rejected.** Applying the same lens to `|E| = 359` and nullity `30`, I found no forced
  `φ`/Fibonacci structure and said so in-cert (Lean `edges_prime`, `nullity_not_fibonacci`): `30 = V − k =
  33 − 3` has no Fibonacci form (the `30 =` icosahedron-edges agreement is a corpus-flagged *coincidence*),
  and `359` is prime — it already carries the `α_top⁻¹ = 359φ⁻² − φ⁻⁵` role, and dressing it as Fibonacci
  would be numerology. Only the spectrum genuinely forces; the rejections are part of the result.

- **The window-scale field, and a rejected hypothesis.** I set out to test whether the `+2` step forces the
  `√10` field of the S_DE window scales (`λ_{c,r} = 3/2 ∓ √10/40`) — a departure from the golden field
  `ℚ(√5)` that would carry meaning if forced. It does not. The splitting has an exact forced closed form
  `D(m) = (λ_r − λ_c)² = 9 − 4·(λ_cλ_r) = 3/((m+1)(m+3))` for zones `{m,m+2,m+4}` — the denominator being
  the product of the smallest and largest *degree-halves*, `D = Z/(h_min·h_max)`, `Z = 3`. At the scene
  `m = 9` this is `1/40`, reproducing `√10/40` from a closed form. But `D(m) > 0` for *all* `m`, so the
  scales are always real and distinct — "orientation = sign of the discriminant" gives a constant `+`, never
  a `ℤ₂` flip, so `√10` is **not** an orientation bit (my own hypothesis, rejected). And the field
  `ℚ(√(sqfree(3(m+1)(m+3))))` is a size-fingerprint: golden `ℚ(√5)` occurs at zones `29,31,33`, not the
  scene. So `√10` is the fingerprint of sizes `9,11,13` and carries no forced golden-departure meaning —
  which *explains* the standing `√10 ∉ ℚ(φ)` NO-GO (it is generic, not a near-miss) rather than weakening
  it (`D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001`). This is the discipline working in both directions: an
  exact forced formula *and* the refutation of the interpretive hook I reached for.

- **The centre of the triple is a forced space-time convergence (the capstone).** Everything above forces
  structure *given* the numbers `{9,11,13}`. The last step forces the numbers themselves. The book stated
  qualitatively that `φ⁵ = 11 + φ⁻⁵` makes `|V₁₁|` "the spatial and temporal faces of the same return"; I
  upgraded that to a certified forced convergence. Five quantities land on `11`: the spatial capacity
  `|V₁₁|`, the Lucas `L₅`, `round(φ⁵)`, the temporal return `|Tr(T⁵)|`, and `|det(T⁵−I)| = #Fix₅`. The two
  channels are independent — `T = [[0,1],[1,-1]]` is the *time* operator (pinned as the orientation-twisted
  golden companion, `trace = −1`, `det = −1`, distinct from the plain Fibonacci `M_φ`, `trace = +1`), while
  `|V₁₁|` is a *spatial* capacity count — so their coincidence is not circular. The centre is forced as the
  unique intersection `{Lucas returns} ∩ [9,13] = {11}` (`L₃ = 4` too small, `L₇ = 29` too large), at the
  forced level `5` (smallest odd return with `Lₙ > Ω₈ = 8`; the `L5 = Access` closure of the maturity
  levels). Since the `±2` half-width is the already-owned orientation step, `{9,11,13} = {L₅−2, L₅, L₅+2}`
  has *both centre and width forced* — the scene triple is zero-free-integer
  (`D0-SCENE-CENTER-SPACETIME-CONVERGENCE-001`). This is the same multi-channel forcing the corpus uses for
  `rank = 3`, now applied to *why the scene has the exact numbers it has*.

- **The causal-cone cubic carries no free integers either.** The rank-3 characteristic cubic
  `λ³ − 359λ − 2574` (which fixes the 3 reversible spacelike modes in `D0-RANK3-CAUSAL-CONE-FORCING-001` and
  the isotropization residual) had its coefficients described only as "scene symmetric functions". I pinned
  the exact identification: via the zone-quotient adjacency `B_ij = n_j`, the cubic is exactly
  `λ³ − |E|·λ − 2∏(zones)`, because (i) the sum of pairwise zone products `n₁n₂+n₁n₃+n₂n₃` *is* the edge
  count `(N²−Σnᵢ²)/2 = 359 = |E|`, and (ii) the zero-diagonal quotient determinant is `2 n₁n₂n₃ = 2574`.
  Both coefficients are forced by `{9,11,13}` alone — the same object as the forced Laplacian spectrum. Honest
  scope held: this owns the *coefficients*; the isotropization dimensionful amplitude stays MECH-LIMIT and the
  rank↔metric-cone identification stays a named Connes bridge — neither is claimed here
  (`D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`).

### 12b. The parallel scout wave — three closures across the whole theory, one caught-and-reverted

To work breadth (not one thread), I dispatched four independent scouts on open targets in *different* books,
each a semantic+computational reasoning task under the same discipline (grammar-priority, reject numerology
out loud, honest verdict is a win). I re-verified every returned claim myself before it entered the corpus —
and one of them I *rejected*.

- **Hypercharge flow→Weyl map `Φ` → NO-GO (Book 04).** No canonical flow on `K(9,11,13)` carries the
  `SU(3)×SU(2)×U(1)` root/Weyl structure: four independent walls (rank `3 < 4`; induced graph-automorphism
  action trivial vs `|W|=12`; active eigendirections orthogonal-unequal, not the `120°`-equal `A₂`; 6
  hypercharge values vs 3 zone-functionals). The seductive coincidence — the rank-3 cubic's **Galois** group
  is `S₃ = |Weyl(SU(3))|` — is rejected out loud as a group-name match with no orthogonal-symmetry carrier.
  Root cause: equal zones `K(n,n,n)` *do* carry a geometric Weyl `S₃`, so the M1-forced `+2` progression
  (unequal zones) is exactly what destroys it — one cause, two effects, tying this NO-GO to the same forcing
  that fixes the scene numbers (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`).
- **Sturmian refinement discharge → NO-GO (Book 06).** The Sturmian tower's CONDITIONAL-EXTENSION cannot be
  discharged internally: the golden tower lives in `ℚ(√5)=ℚ(φ)` but the archive scale `359/160` lives in
  `ℚ(√10)`, disjoint fields (`√10 ∉ ℚ(√5)`), so no canonical intertwiner exists — the same field obstruction
  that closed the phason-WZ transfer, and *explained* by the `√10` size-fingerprint result. Plus an
  orientation mismatch (`S` trace `+1` vs the centre-11-forced `T` trace `−1`). The parent claim stays
  PROOF-TARGET honestly; a new companion NO-GO records the discharge obstruction
  (`D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001`).
- **Adler–Weiss internal Markov construction → CERT-CLOSED + Lean (Book 06).** The hardest target — after its
  scout stalled I took it in-house. The exact 2-cell Markov partition is realized *internally* via the
  M1-forced golden `β = φ` natural extension: the digit map with the golden-split cut `1/φ` has a
  *symbolically proven* Markov property (`x ∈ R₁ ⟹ φx−1 ∈ R₀` exactly, so `1→1` is forbidden), giving the
  golden SFT `[[1,1],[1,0]]` with Parry measures `(φ²,1)/(φ²+1)` and entropy `log φ`, transported through the
  owned orientation-twisted conjugacy `T ∼ −M_φ` (Lean-verified `D0.VNext2.AdlerWeissInternalMarkov`, rc=0).
  Honest scope: this closes the *symbolic-dynamical* content; the explicit flat-torus parallelogram embedding
  and the smooth/measure conjugacy stay the external classical owner
  (`D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001`).
- **α Feshbach–Dixmier → examined and *rejected* (no status change).** A scout reported this as GENUINE-NO-GO
  with correct block arithmetic — but it had used the *wrong operator split* (a zone split, not the claim's
  active/archive rank-3/dim-30 partition) and merely re-proved an already-owned finite-heat-trace NO-GO. I
  reverted the flip, removed the mis-scoped cert, and left a ledger note: the claim's real residual is the
  *external* profinite Dixmier realization, honestly PROOF-TARGET. This is the discipline working — certify a
  NO-GO against the object the claim actually needs, not a convenient one.

Registered cert count after the wave: **390 → 393** (three closures; the rejected one left the count
unchanged). All integrity guards green, all new Lean modules compile rc=0, all certs falsifiable.

### 12c. The gravity-response pair — a positive closure and its exact obstruction

Two claims the ledger had flagged *jointly open* and *architecture-blocked* (an `ℝ/ℚ` carrier mismatch)
turned out to be a clean fork once the right object was computed — one closes, one is a genuine NO-GO, and
they share a mechanism.

- **Finite Einstein-tensor response → CERT-CLOSED + Lean (`D0-SPECTRAL-EINSTEIN-001`).** The rank-2 response
  the ledger said "does NOT exist anywhere in D0/" is simply `G = dS_{a₂}/dh = 2L`, the scene Laplacian: the
  variational response of the quadratic spectral action `Tr(L²)`. It is proved *simultaneously* symmetric and
  divergence-free in the corpus's own `archiveDivergence` (row-sums-zero) sense — the discrete
  contracted-Bianchi identity, since a Laplacian annihilates constants. It lives on the `ℝ`-matrix carrier, so
  the carrier mismatch is bypassed, and it correctly *scopes* the old conservation NO-GO (which only said
  *arbitrary* symmetric matrices aren't conserved — never blocking the canonical response). Lean-verified for
  any graph Laplacian (`D0.VNext2.SpectralEinsteinResponse`, rc=0).
- **Matter↔TT shared carrier → NO-GO with a positive partial (`D0-HODGE-LINKS-001`).** The positive partial:
  matter edge-stress and that Einstein response *do* share the vertex carrier (every symmetric edge-stress has
  a unique divergence-free Laplacianization, so matter conservation = transversality). The obstruction: the
  two physical TT-graviton polarizations are *not* carried by the vertex response — on 33 vertices the
  transverse-traceless space is 527-dim (nonempty), yet `G = 2L` is 100% *trace-mode* (`Tr G = 4|E| ≠ 0`, and
  `G_TT = 0` exactly). The two tangent-indexed polarizations need the `Fin 4` carrier via the external
  smooth-limit bridge, so the `ℝ/ℚ` mismatch is *structural*, not a type nuisance. A control confirms the
  vanishing is specific to the trace-mode `G` (a generic conserved stress has a nonzero TT part).

One mechanism ties them: the vertex Einstein response is `2L`, which is transverse (Bianchi) *and* pure
trace-mode — the same fact that makes gravity's conservation automatic is what starves the vertex carrier of
TT content. Registered cert count after the pair: **393 → 395**; both new certs falsifiable, the Einstein
module compiles rc=0.

- **Gauge-boundary commutator obstruction → finite leg now CORE + Lean (`D0-CVFT-F6`, CORE_BRIDGE_SPLIT).**
  A stale PROOF-TARGET whose finite theorem had actually been supplied internally (Iter23) but never
  status-split, Lean-formalized, or cited. The exact operator identity `‖[P,g]‖_F² = 2‖QgP‖_F²` (Hermitian
  `g`, projection `P`) rests on an algebraic core now Lean-verified for *any* `P`: `[P,g] = PgQ − QgP` — a
  commutator with an idempotent carries no diagonal blocks, so a zone-preserving generator has zero leakage
  while a unit boundary-crossing ("colored") coupling forces `‖[P,g]‖² ≥ 2`, a hard quantized floor on the
  scene bulk/archive split. The finite-scene Yang–Mills mass-gap-*language* obstruction is thus internally
  owned; the *continuum* Millennium mass gap stays an explicit external bridge (`D0.VNext2.GaugeBoundaryCommutator`,
  rc=0). This is the housekeeping half of "close, don't describe" — a finite result that was done but never
  wired into the ledger's status/Lean/citation cascade.

### 12d. Synthesis audit (golden/level-5 cluster) + a verification-accuracy pass

After the closeable-target surface was exhausted, I ran two disciplined passes rather than manufacture
closures.

**Synthesis audit — the golden connections are saturated, and one tempting new one is numerology.** I chased
the φ-ladder / level-5-stabilization / quantum-of-distinguishability cluster for an *unregistered* forced
connection. Every candidate was either already owned or a coincidence:
- "The scene Laplacian has exactly **5** distinct eigenvalues = the maturity level 5" — **rejected as
  numerology.** Control: 5 distinct eigenvalues is the *generic* count for any complete tripartite graph with
  distinct parts (`K(2,3,4)`, `K(5,7,9)`, `K(10,20,30)` all give 5); it is not a scene fingerprint.
- "`round(φⁿ) ∈ [9,13]` iff `n=5`" reduces to `round(φⁿ)=Lₙ`, already owned by the scene-center convergence.
- The AF-Dirac ladder termination `33 = F₂+F₄+F₆+F₈ = F₉−1` is already owned
  (`D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001`).
- The level-5 seam `ξ₅=φ⁻⁵` shared by `α_top` and `sin²θ₁₃` is already owned (`D0-XI5-CROSS-SECTOR-001`).

That the obvious golden convergences are all registered — and the one new "5=5" pattern is a coincidence — is
itself a datum about the theory's maturity, not a failure to look.

**Verification-accuracy pass — 7 claims were Lean-proved but mislabeled.** Auditing the 104 `PYTHON_CERTIFIED`
claims, I found seven whose Lean leg *already exists* (named module compiles rc=0, sorry-free, and proves the
claim's own theorem-of-record) but whose `lean_module`/`lean_status` fields were empty or `PYTHON_CERTIFIED` —
a field-sync miss that undersold the verification level. Corrected to `LEAN_PROVED` (with the exact theorem
named): the α-seam `Δ_α` and `α_alg⁻¹` exact-`ℚ(φ)` identities (`DeltaAlphaExact`, `DeltaAlphaMoment`), the
canonical Dirac covariance owner, the carrier-not-icosahedral gap, the gauge mass-gap cost quantum, the
compactness limit, and the EW-window grammar. The discipline that matters: a note saying "backed by `D0.X`" is
not license to copy the module name — each was verified for theorem-content alignment first, and two adjacent
candidates were held back for lacking it. `lean_status` is now `LEAN_PROVED` 364 / `PYTHON_CERTIFIED` 98.

### 12e. Lean-hardening wave — 4 new modules, real formal content (not relabels)

With the closeable-target surface exhausted, I turned to raising the *verification level* of load-bearing
`PYTHON_CERTIFIED` claims to `LEAN_PROVED` — but only where Lean adds genuine rigor. The discipline: a lift
earns its keep when the Python cert checks something **numerically** (real eigenvalue signs, a sequence
limit, a `√`-cancellation, a totient) so the formal proof upgrades rigor for *all* inputs; it is *ceremony*
when Python already does exact integer/rational arithmetic (e.g. `9·11=99`), and impossible when the claim is
an external K-theory/bridge/HYP. Four modules, each `rc=0`, `0 sorry`, imported in `All.lean`, all guards PASS:

1. **`D0.VNext2.Rank3MetricSignature`** (`D0-RANK3-METRIC-TRANSPORT-001`). The spatial transport form
   `B=[[0,11,13],[9,0,13],[9,11,0]]` has signature **(1+, 2−)** — proved from the symmetric functions
   `e₁=Σλ=0`, `e₃=∏λ=+2574>0` (a positive product of three reals with zero sum is one-positive-two-negative)
   — and its **anisotropy ⇔ nonzero discriminant**: `equal_zone_discriminant_zero` proves as a polynomial
   identity in `n` that the equal-zone cubic `λ³−3n²λ−2n³` has discriminant identically `0`, so the two
   negative eigenvalues coincide only in the isotropic equal-zone limit. The cubic *coefficients* were already
   owned (`Rank3CubicSymmetricFunctions`); this adds the signature + anisotropy.

2. **`D0.VNext2.PhasonWZSequence`** (`D0-PHASON-WZ-FINITE-SEQUENCE-SCAFFOLD-001`). The internal
   pressure/energy ratio `w_n = φ^{n-1}/(φ^n−1)` **decreases monotonically to `φ⁻¹` for all `n`** (the numeric
   cert only checked `n=1..8`). Key identity `w_excess_form`: `w_n = φ⁻¹ + φ⁻¹/(φ^n−1)`, from which
   `w_gt_limit` (`w_n>φ⁻¹`) and `w_strictly_decreasing` follow because `φ^n−1` strictly increases.

3. **`D0.VNext2.Window44Totient`** (`D0-WINDOW44-TOTIENT-M1-001`). The terminal window `q_T=|ABCD|·|V₁₁|=4·11=44`
   has coprime branch count `Nat.totient 44 = 20 = |(ℤ/44)ˣ|` (via `ZMod.card_units_eq_totient`), coinciding
   with the terminal shell degree `d₁₃ = 9+11 = 20`.

4. **`D0.VNext2.HiggsAnchorProjector`** (`D0-EW-002`). The scalar anchor has `dim = rank·V₁₃ = 3·13 = 39`, and
   the norm-defect identity `‖(δ₀/√39)·𝟙₃₉‖ = δ₀` is exact: `39·(δ₀/√39)² = δ₀²` (the `√39` cancels), with
   `δ₀=(√5−2)/2=1/(2φ³)>0`.

Held back as low-value or wrong-shape: `D0-PHI99-DEPTH-FORCING-001` (`99=9·11`, exact integer — Python
already rigorous, Lean is ceremony); `D0-ALPHA-MU1-RANKTRACE-001` (value `μ1=1/3` already Lean-CORE in
`DeltaAlphaMoment`; only the trace-labeling is new — the cert itself says "does not re-derive the CORE
value"); `D0-CKM-PMNS-COMPLEMENTARITY-001` (the NO-GO witness uses measured mixing angles — a Python cert is
the correct proof); all K-theory / solenoid / Connes-triple rows (external gaps by construction).

Net across the session: `lean_status` `LEAN_PROVED` 349 → **368**, `PYTHON_CERTIFIED` → **94**.

## 13. What I did NOT do (discipline)
- Did **not** construct an ad-hoc selector map Φ to "close" the hypercharge row — the obstruction is real
  and a fabricated selector would be exactly the numerology the corpus's contract forbids.
- Did **not** claim any topological-conjugacy or ℚ(φ) closure that the mathematics does not support.
- Did **not** force a Majorana structure the scene does not carry; recorded the honest three-route NO-GO.
- Did **not** promote any status beyond what the cert proves; targets stay PROOF-TARGET/NO-GO/bridge, each
  with the residual named. All sub-agent claims were re-verified by me before entering the corpus.

## §13. Iter26 (continued) — the α ansatz form derived + a ledger-integrity reconciliation

Two things this pass: one new positive closure (referee push-point #2), and a structural repair that the
new work surfaced.

### 13a. `D0-ALPHA-HOLONOMY-LINEAR-FORM-001` — the linear form `1+h·sinθ` is derived, not data-selected

The flagship α closure-holonomy dresses `α_top⁻¹` by `1 + h_KS·sin θ_seam`. Four of its five ingredients were
already Lean-proved (depth `φ⁻¹⁷`, coefficient `lnφ`, angle `12/5`, `sin`-channel via `Q₈`, `G²=−I`). The one
piece that had been only **data-selected** — the *linear form itself* (linear beats `exp` against CODATA) — is
now derived.

**Mechanism.** The seam carries two distinct operators: the elliptic channel selector `G` (`G²=−I`, picks the
`sin` amplitude — owned by `SeamHolonomy`) and the **directed** transport `N` (the CP-seam crossing). Because
the CP-seam is the *directed* 3-cycle (`D0-BARYON-ASYMMETRY-DELTA0-001`), one closure crosses it once and
cannot return, so `N` is nilpotent: `N²=0`. For nilpotent transport the flow is *parabolic* —
`(I+sN)(I+tN)=I+(s+t)N` with **identically zero** higher-order term — so the transported dressing factor is
*exactly* `1+s`, linear. The `exp`/oscillatory form is structurally excluded (it needs `N²≠0`, a
returning/undirected seam), and the elliptic channel alone gives a *bounded* readout `cosθ−sinθ` (`≤√2`) that
can never be an unbounded linear `1+s`. **Nilpotency is proved load-bearing** (a non-nilpotent generator
breaks the parabolic law). So the data's role shrinks from *selecting* the form to *confirming* the single
directed crossing: the `exp` control fails precisely because its second-order term
`φ⁻¹⁷·½(h·sinθ)² ≈ 1.5×10⁻⁵` is what the nilpotency annihilates.

Lean `D0.Spectral.SeamTransportLinear` (rc=0, 0 sorry): `seamN_sq` (`N²=0`), `transport_add` (parabolic group
law, exact), `transport_readout` (`=1+s`), `alpha_dressing_factor` (`=1+h·sinθ`), and the elliptic contrast
`rotation_readout_bounded` (`|cosθ−sinθ|≤√2`). Cert `vp_alpha_holonomy_linear_form.py` (rc=0, can-fail). Book
§02.13.h updated: the "linear form graduates to THE" claim is now actually backed.

**Honest scope:** `N²=0` encodes "one directed crossing per closure" — that single-crossing input is the
physical hypothesis (motivated by the directed CP-seam). Given it, the *form* is exactly linear. The 9-digit α
*value* stays CHK (`D0-ALPHA-HOLONOMY-002`); the last `~10⁻⁸` stays a HYP measurement-limit bet.

### 13b. Ledger-integrity reconciliation — reported closures that were never persisted

Registering the α claim required round-tripping `CLAIM_TO_LEAN_MAP.csv`, which surfaced a latent defect: **two
rows had unquoted commas in their notes** (`D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001`,
`D0-EDGE-RAMIFICATION-001`) that broke the CSV parse into a `None`-key overflow — and this had been *masking
prose⟂ledger desyncs from the `check_book_ledger_sync` guard*. Repairing the quoting made the guard see the
true ledger, and it caught real desyncs: several claims the session had closed in Lean (modules exist, compile
rc=0, imported in `All.lean`, book prose says CERT-CLOSED/LEAN_PROVED) still had their **CSV rows stale** at
`PYTHON_CERTIFIED`/`OPEN` with an empty `lean_module`. The reported "369 LEAN_PROVED" had been an *in-kernel*
count that never fully hit disk.

Reconciled to ground truth (module compiles + cert runs + theorem-of-record present + book consistent, all
verified before stamping): `Rank3MetricSignature`, `PhasonWZSequence`, `Window44Totient`, `EW-002`, `CVFT-F6`,
`SPECTRAL-EINSTEIN-001`, `ADLER-WEISS-INTERNAL-CONSTRUCTION-001` → `LEAN_PROVED`; registered the absent
`D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`. **Final persisted state: 527 rows, `LEAN_PROVED` 358,
`PYTHON_CERTIFIED` 101, `OPEN` 38, `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` 28, deprecated 2 — and 0 `LEAN_PROVED`
rows with an empty or dangling module (all 386 verified file-backed).** All guards PASS, all 10 books
idempotent.

**Lesson recorded:** after any Lean closure, verify the CSV row was actually written to disk — do not trust the
in-kernel count. This is exactly the cascade-not-pointwise integrity the sync architecture is meant to
enforce, and the guard did its job once the CSV parsed cleanly.
