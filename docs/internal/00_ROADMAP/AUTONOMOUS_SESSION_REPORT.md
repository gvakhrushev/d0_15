# D0 — Autonomous session report (Iteration 4)

Owner away ~2h; full autonomous front executed under the iron rules (firewall, α honesty,
no v17 overshoots, CSV+artifact+graph+log per change, OWNER-DECISION-NEEDED for owner-level
calls, guillotine, positive closure delta). Source of truth: `09_LEAN_FORMALIZATION/docs/
CLAIM_TO_LEAN_MAP.csv` (canonical) → generated `03_THEORY_MAP/theory_status_map.csv`.

**Headline.** strength **2753 → 2867 (+114)**; CORE-FORMALIZED **92 → 97**; PROOF-TARGET
**12 → 12** (no new open targets — closure delta positive); hygiene **100/100**; firewall
violations **0**; all guards green. 5 commits on `master` after tag `base-pre-autonomous`.

## What was closed (this session)

**Note on scope.** The owner ТЗ's Phases 2/3/4 (Roots A/B/C: α via ζ_D, the one-ℤ₂ spinor
cover, full carrier forcing) and §4 items T5.2/T5.3 (S_DE fork, signature-3+1) were ALREADY
closed earlier this session (commits cb09e4a, ce732e4, 9726a99, 745e836). The autonomous
front below executed the genuinely-remaining work.

1. **Phase 1 — gravastar (fresh result, real hole filled).** `bf85aff`. D0 had the static
   horizon=seam and horizon birth, but no collapse-ARREST. External anchor: Jampolski–
   Rezzolla PRD 113 L121502 (2026). Three claims, three passing certs, BOOK_07 §07.51 +
   BOOK_09 §09.09:
   - `D0-GRAVASTAR-FORMATION-BRIDGE-001` (CERT-CLOSED, bridge to external GR): 3-region
     dS/shell/Schwarzschild, Israel junction, horizonless `2M<R<L`, seam closes at C=3/8.
   - `D0-COMPACTNESS-LIMIT-001` (CERT-CLOSED / LEM, **named gap**): `−2C(8C−3)=0 ⟹ C=3/8`
     (exact); 1/3<3/8<4/9<1/2; structural 3/8=rank/|Ω₈|. Supporting Lean
     `D0.Gravity.CompactnessLimit` proves the 3/8 roots over ℚ (compiles). NAMED GAP:
     rank-3=causal-cone postulated, NOT THE.
   - `D0-GRAVASTAR-GW-FALSIFIER-001` (EMPIRICAL-PASSPORT): surface inside the photon sphere
     ⟹ GW echoes (BH has none); echo delay ~2.29M, dimensionless. Never core.
2. **T5.1 — phason language debt closed by FORCING** (the publication blocker). `8c0bfe5`.
   `D0-PHASON-FORCING-001` (CERT-CLOSED) + BOOK_08 §08.51: the phason is the forced
   perpendicular-space mode of the (already forced) cut-and-project carrier; phason shift
   preserves the Sturmian factor set ⟹ gapless Goldstone ⟹ dark radiation-free. The ~99
   uses now inherit a derivation rather than borrowed vocabulary.
3. **Phase G — Group A Lean wave (+5 CORE).** `c20ef8e`. Five finite/Mathlib-reachable
   cert-only claims promoted to CORE-FORMALIZED via per-claim Lean modules (sorry-free):
   `D0-CKM-EXACT-001`, `D0-BOOK04-SELECTORS-001`, `D0-NONABELIAN-SEAM-001`,
   `D0-CLASS5-ALIASING-001`, `D0-BARYON-S3-SYM-001`. Mathlib-blocked candidates left
   cert-level, NOT faked.
4. **T5.4/T5.5 — external anchors + H0 passport.** `b824b06`. Three EMPIRICAL-PASSPORT
   claims wired into the books (were 0 corpus occurrences): `D0-PMNS-DELTA0-NUFIT-001`
   (δ₀-family vs NuFIT 6.0, beats GRA/TBM/GRB, JUNO falsifier), `D0-H0-EVOLVING-W-001`
   (R_n=φⁿ−1 convexity ⟹ evolving-w, DESI falsifier), `D0-E8-COLDEA-ANCHOR-001` (CoNb₂O₆
   E8 criticality m₂/m₁=φ). All firewall-blocked from core.

## What stays open (honest theorem-targets / named gaps)

- **Δ_α analytic owner** — the one fully-open obligation (BOOK_05 §05.6 obl. 4). Δ_α ≈
  4.15e-4 (top-vs-alg residual) is DISTINCT from φ⁻⁵=ξ₅; no analytic owner yet.
- **rank-3 = causal cone** (T1.4) — attempted via the Connes distance (BOOK_03 §03.1),
  OPEN. Closing it lifts `D0-COMPACTNESS-LIMIT-001` from LEM to THE.
- **PMNS δ₀-family angle formulas** — `δ₀` is forced; the `sin²θ` formulas are passport
  predictions, their forcing from M1 is not done.
- **Downstream phason K-theory / spectral-triple holonomy** (QUASI007/008/009) — stay
  cert-closed with explicit EXTERNAL-GAP (Mathlib 4.30 lacks the K-theory).

## OWNER-DECISION-NEEDED

1. **S_DE cubic-vs-quadratic fork** (Iteration 3, `D0-VACUUM-CUBIC-WINDOW-001`): both
   branches are exact, discriminator computed (cubic 0.808 vs quadratic 0.900). The choice
   is DESI DR3's to make; not decided here.
2. **PMNS angle-formula forcing**: whether to invest in deriving `sin²θ₁₂=1/3−2δ₀²` etc.
   from M1 (would promote the passport), or leave as an empirical target.
3. **Print-stub certs — integrity finding.** The Group-A triage found that several cert
   files are pure `print("PASS")` stubs with NO computation (`vp_finite_hodge_complex_core.py`,
   `vp_no_axion_finite_cochain.py`, and per one triage `vp_black_hole_capacity_a4_witness.py`
   — the two triages disagreed on the last). These VIOLATE the guillotine (a cert that
   cannot fail is not a cert). They were NOT promoted. Owner decision: write real finite
   witnesses for `D0-HODGE-001` / `D0-NOAXION-001` / `D0-SPECTRAL-EINSTEIN-001`, or demote
   those rows. (Out of autonomous scope — touches existing core-adjacent claims.)

## Reusable asset created

`~/.claude/skills/verified-closure-protocol/` — a universal (domain-agnostic) skill
encoding the honest-closure protocol used across Iterations 3–4: scout → executable cert
that can FAIL → formalize where reachable (else named theorem-target) → registry →
prose → guards → commit, with the honesty ladder + boundary discipline. Includes
`tools/cert_template.py` and `tools/honesty_checklist.md`.

## Discipline confirmation

Zero v17 overshoots reintroduced. α honesty boundary intact (α stays a structural form,
not promoted to precision prediction). No passport promoted to core. Every promoted claim
has a passing artifact. Passport-summary timestamp noise was reverted before each commit
(a background task was filed to make those summaries deterministic). All 7 guards green:
validate_csv, check_firewall, no_tautology, apparatus --check, check_book_publication,
assemble_books --check, no_sorry_in_core.

---

# Iteration 5 — audit-driven 3-track strategy (executed)

Audit → updated scoring → balanced execution of three tracks (closure / synthesis /
cleanup). strength **2867 → 2963** (CORE-FORMALIZED 97 → 105); all 8 guards green; hygiene
100/100 (penalty −0.4 → −0.2). Five commits (ab351f6, 3814908, 2a65aa9, 51ed635, + this wrap).

**What closed.** Track 1: bless ZETA→CORE + 6 CORE promotions (SPIN2, HIGGS-YUKAWA, 4×
ARCHIVE — the latter were under-credited already-proved modules). Track 2: Z2SpinorCover
7/7, RankCausalCone (sharpened the gravastar gap, not faked to THE), registry repoints,
Δ_α→CVFT-F1 owner edge. Track 3: new `check_cert_can_fail` guillotine guard; 3 print-stubs
rewritten with real finite witnesses, 2 demoted; float→exact on 2 certs; stale doc pointers
fixed.

## OWNER-DECISION-NEEDED (Iteration 5)

1. **Cert can't-fail debt is 24, not 5.** The new guard found 19 *compute-theater* certs
   (compute values but print PASS without gating) beyond the 5 approved print-stubs. They are
   grandfathered in an explicit, printed ratchet (`tools/check_cert_can_fail.py` GRANDFATHER,
   now 19) that blocks new stubs and must only shrink. Decide appetite for rewriting/demoting
   the remaining 19 in a future iteration.
2. **ZETA bless to CORE** — done on the judgment that `zeta_residue_alpha_finite` is gap-free;
   please confirm `D0.Traceability.StatusTaxonomy` treats a gap-free LEAN_PROVED theorem as
   CORE-eligible (the firewall already passed).
3. **EDGE-001 trace-leg split.** The phantom `D0.Edge.AlphaRamificationConstructive` path was
   cleared; the trace identity is already proved as `ZetaResidueAlpha.zetaEdge_neg_one`. Decide
   whether to formally split EDGE-001 into a closeable trace leg + an open unitary-dilation leg.
4. **Δ_α / residue-at-pole** remain the one fully-open frontier obligation, now routed to the
   CVFT-F1 feedback-resolvent-trace engine (not a finite cert — owner decision to invest).
5. **Deferred (noted, not done):** 41 process-tag (`v15`/`NOID`/`CVFT`) section-id renames
   (cosmetic); the 9 registered-but-missing cert paths (audit which rows name absent certs).

## Carried-forward open items (unchanged)
- S_DE cubic-vs-quadratic fork → DESI DR3 decides (discriminator computed).
- PMNS angle-formula forcing (passport; formulas not yet M1-derived).
- Topological conjugacy (Mathlib-blocked); rank-3↔cone-space identification (named gap).

---

# D0 — Iteration 6 report: forcing-owner integration (Frobenius-class theorems)

Owner supplied a catalog of 9 classical **uniqueness/classification** theorems as candidate
forcing-owners for D0 links. The discipline: *raise by forcing OR name the gap's owner;
enumeration as an argument is banned* (§05.8.R). Reconnaissance (3 Explore agents) found most
links already owned, so the work split three honest ways with **zero enumeration-demotions**.

**Headline.** strength **3031 → 3113 (+82)**; CORE-FORMALIZED **107 → 110 (+3)**; external
owners machine-tracked (ledger ASSUMP) **7 → 11 (+4)**; integrity demotions **0**; hygiene
**100/100**; firewall violations **0**; all registry/cert guards green. Each of the 5 new Lean
modules compiles **sorry-free** (individual `lake build` + dependency closures). 5 commits
(`bffa7b8`, `4a4aaf5`, `0bdb1eb`, `86cdb76`, `62dc73a`).

**Build-hygiene finding (pre-existing, NOT from this work).** The first full `lake build D0.All`
of the session is RED: **17 modules fail to compile** — a stale `Mathlib.Data.Rat.Basic` import
cascade, several malformed `theorem _ : Prop := <prop>` (should be `def`), and missing
identifiers. CI never runs `lake build` (it scores off declared `lean_status` + module
existence), so this was masked. **16/17 are orphan modules** (no claim → registry/firewall/score
unaffected); the one exception is `D0.NoGo.StressTestSuite` (`D0-NO-GO-STRESS-SUITE-001`,
declared `LEAN_PROVED`) which references non-existent `D0.Matter.*` symbols — a real
`LEAN_PROVED`-but-uncompilable discrepancy. Spun off as a dedicated Lean build-hygiene task; the
forcing-owner deliverables are unaffected (every new module + its closure compiles).

## The delta the ТЗ asked for: closed-by-forcing vs named-owner vs honestly-rejected

**Closed by FORCING — decidable shadows (CERT + Lean, CORE):**
| claim | what is now forced (exact) | external owner (named) |
|---|---|---|
| `D0-ICOSIAN-E8-GRAM-001` | E8 Gram even (diag 2) + unimodular (det=1), rank 8=2·4 | Mordell 1938 (`ASSUMP-MORDELL-E8`) |
| `D0-JONES-INDEX-PHI-001` | φ²=4cos²(π/5)=(3+√5)/2 = Fibonacci quantum dim (n=5 slot) | Jones 1983 (`ASSUMP-JONES-INDEX`) |
| `D0-DIM8-NETWORK-001` | 8-network skeleton: 8=2·4, tower 8\|24\|120, E8, D4 triality | 6 owners (Hurwitz…triality) |

**Named the OWNER — BRIDGE owner-edges (≤11 pts, honesty not points):**
- `D0-CONNES-RECONSTRUCTION-OWNER-001` — "metric = spectrum of the Dirac operator" (Connes
  reconstruction); routes the rank-3=causal-cone / Connes-distance NAMED GAP (§07.51.3).
- `D0-TIME-MODULAR-FLOW-OWNER-001` — "time = modular flow" (Tomita–Takesaki + Connes); deepens
  the Pisot time layer (§06.30a), M1-aligned (time fixed by the (algebra,state) pair).
- Second channels (cited prose): Busch 2003 (Born on dim-2 where Gleason fails) + Masanes–Müller
  2019 (d=3); Baer 1933 (Q8×B×D structure).

**Honestly REJECTED — anti-numerology calibration (§00.9 + §05.8.R):** Leech Λ₂₄↔K=30 (24≠30);
triality⇒3 generations (3 = #D4 reps, not families); C_max=3/8 not owned by Weinberg; Pisot
≥3-letter conjecture OPEN; Frobenius integrability is a scaffold. Also reconciled the firewall's
own (710,113) numerology-failure example with the EW-window forcing via grammar-priority.

## Honesty boundaries held
- Every external theorem is a NAMED bridge owner with a Lean assumption object + ledger entry —
  never a hidden assumption, never promoted to CORE.
- Each shadow proves only its decidable part; the genuinely-frontier remainder (Mordell genus
  uniqueness, Jones quantization obstruction, Connes reconstruction, Tomita modular uniqueness)
  is named EXTERNAL, not faked.
- The "8 forces 3 generations" and "C_max=3/8 from Weinberg" temptations were refused in writing.

## Carried-forward / not done
- Optional solenoid-Dirac integer-trace shadow for the Connes edge (deferred; the owner-edge
  stands without it).
- rank-3=causal-cone identification stays a named gap (now with a named external owner).
- φ-network ↔ 8-network meet at the icosians; the deeper "φ and 8 are one object" remains a
  synthesis statement, not a single Lean theorem.

---

# D0 — Iteration 7 report: cross-domain bridges after the deep-research self-check filter

A second deep-research front (8 areas) arrived **pre-calibrated** — the owner had already run
the self-check and downgraded the inflated statuses. This iteration's whole discipline was to
integrate at the honest (downgraded) status and **never re-inflate from the report text**.

**Headline.** strength **3113 → 3179 (+66)**; integrity demotions **0** (zero re-inflations);
hygiene **100/100**; firewall violations **0**; all registry/cert guards green; 4 new Lean
modules build sorry-free individually; 4 new certs PASS + can-FAIL. 6 commits
(`976e829`, `c8fdcf9`, `d52af3b`, `67b8248`, `3810cf5`, + this wrap). The deep-research filter
is now law (BOOK_05 §05.8.S).

## The delta the ТЗ asked for: downgrades held, statuses earned by mechanism check

| research label | honest status landed | named gap |
|---|---|---|
| Fibonacci `d_τ=φ` ⇒ `I_f=logφ` (FORCING) | **LEM** `D0-FIBONACCI-IF-FORCING-001` | categorical↔toral isomorphism unwritten |
| `γ_Choptuik ↔ 3/8` (BRIDGE-owner) | **HYP** `D0-PACKING-LIMIT-001` | derive a common `F(D)` or accept the `D=4` coincidence |
| Bekenstein `S≤A/4` (FORCING) | **BRIDGE** (Jacobson cite on Connes edge) | thermodynamic owner, not a D0 derivation |
| complex QM necessary | **BRIDGE** `D0-COMPLEX-QM-FORCING-001` | experiments assume standard QM postulates |
| M1 ⇒ QM structure | **BRIDGE** `D0-M1-INFO-RECONSTRUCTION-001` | reconstruction assumes continuity + tomographic locality |
| time ↔ flavor "one modular" | **LEM** `D0-MODULAR-TIME-FLAVOR-001` (SL(2,ℤ) group, NOT Tomita–Takesaki) | full golden-element ↔ A5-quotient map |
| DSI log-periodicity in matter | **EMPIRICAL-PASSPORT** `D0-DSI-EXPERIMENTAL-001` | `λ`=Coulomb≠`φ` (form, not value) |
| Verlinde dark↔gravity | **BRIDGE** `D0-ENTROPIC-DARK-GRAVITY-001` | criticizable program, never core |

## Discipline held (the point of this iteration)
- **Zero re-inflations.** Every status is the minimum that survived the mechanism + limits gates.
- **The strongest temptation was refused twice:** Fibonacci stayed LEM (no isomorphism), packing
  stayed HYP (limits diverge); neither was promoted on a coincident number.
- **A conflation was caught:** "modular flavor" (SL(2,ℤ) group) vs "thermal time" (Tomita–Takesaki
  automorphism) are different senses of *modular* — kept apart, not fused.
- **The filter itself is now corpus law** (§05.8.S): deep-research is a candidate generator;
  coincidence at one point ≠ identity.

## Carried-forward / not done
- **F.1 dossier sync: N/A** — `D0_THEORY_DOSSIER.md` was removed in Iteration 2; its content lives
  in the books. No dossier to update.
- The two LEM gaps (Fibonacci iso; golden-element↔A5-quotient) and the packing-law common
  mechanism are the open obligations this front names.
- The pre-existing 17-module `lake build D0.All` breakage (Iteration-6 finding) remains its own
  spun-off task — untouched here.

---

# D0 — Iteration 8 report: researcher contributions developed into closures

Two researcher documents were developed under the owner's directive *develop into closures,
reforge errors into tasks, bring over-statements to honest level keeping the core* (now law,
BOOK_05 §05.8.T). Errors were never discarded; over-statements never inserted as-is.

**Headline.** strength **3179 → 3226 (+47)**; integrity demotions **0** (zero discards, zero
re-inflations); hygiene **100/100**; firewall violations **0**; all registry/cert guards green.
9 new certs (all PASS + can-FAIL); 1 new Lean module (`GluingAnomalyTime`, `native_decide`)
builds. 6 commits (`bbb24ce`, `9034e59`, `d8e6228`, `3c7f0bd`, `197ee0b`, + this wrap).

## The main closure
**`D0-GENERATIVE-DYNAMICS-001` (LEM): D0 is a generator of dynamics, not a static classifier.**
Feshbach–Schur on the rank-3(active)/kernel-30(archive) split gives an effective dynamics
`W_eff` whose poles are the resonances (exact Schur determinant identity), with the excursion
index = algorithmic time; the seam anomaly `C_n≠0` (Lean-checked) forces time; the loop floor
`ε²=φ⁻¹⁶` makes loops finite (no UV divergence); RG is typed forgetting. This closes a real
standing hole and discharges the §06.34 open obligation at the finite level.

## The reforge table (errors → tasks, over-statements → honest level + kept core)
| contribution | check verdict | landing |
|---|---|---|
| §02.21 zone-matrix → φ⁻¹ | **error** (M is stochastic, ρ=1) | reforged: 3 numbers separated (spec M / S_DE window / envelope tick); §02.18.4 |
| §06.42 α⁻¹ closed identity | **over-statement** | core `ξ₅=φ⁻⁵` kept THE; α-line CHK, `Δα` open; §02.13 |
| §09.8 `I_f=Tr(log T)/rank` | **wrong formula** | number `log φ` kept; fixed to `h_KS=log\|λ_max\|`; §09.03 |
| §07.22 A/4 via Four-Color | **forcing attempt** | "4" forced, "1/4" named gap; §07.40 |
| §04.12 `V_CKM U_PMNS^T=I` | **error** | reforged to complementarity `θ_C+θ_12≈45°` (HYP); §06.30a |
| §01.25 φ_E(44)=20 | **correct** | entered as-is with the M1 totient argument; §07.23 |

## Discipline held
- **Zero ideas discarded.** Every arithmetic/attribution error became a clarification or a
  named gap; the error marked where the work was unfinished, not where the idea was wrong.
- **Zero over-statements inserted.** Each was split into a kept core (true status) and a named
  gap (lower status) — `ξ₅` THE while α stays CHK is the template.
- **The constructive rule is now corpus law** (§05.8.T), the dual of the deep-research filter
  (§05.8.S) and the audit rule (§05.8.R).

## Carried-forward / not done
- **F.1 dossier sync: N/A** (`D0_THEORY_DOSSIER.md` removed in Iteration 2; content lives in books).
- The generative-dynamics THE step (an explicit D0 S-matrix simulation) and the A/4-coefficient
  owner (Bekenstein/Jacobson route) are the open obligations this front names.
- The pre-existing 17-module `lake build D0.All` breakage stays its own spun-off task.

---

# D0 — Iteration 9 report: obligation 5 closed (the tower stops at 3 zones)

**Headline.** The last open meta-step of the carrier forcing — BOOK_05 §05.6 **obligation 5**,
the M1 no-extension no-go — is **closed** (`D0-TOWER-STOP-NOEXT-001`, CORE-FORMALIZED +
LEAN_PROVED). This is the **root of the rank-3 cascade**. strength **3226 → 3246 (+20)**;
open §05.6 obligations **2 → 1** (only `Δα`/obligation 4 remains open all the way down);
integrity demotions **0**; all guards green; `D0.Tower.NoExtension` builds.

## The no-go (two cases, both ⊥M1)
- **CASE 2 (repeat)** — a fourth zone repeating an existing type has `≥2` indistinguishable
  copies with a nontrivial copy-symmetry (`|S₂|=2>1`); the copy-choice is an external catalogue
  ⇒ `⊥M1`. Same forcing as `Ω₈≅Q₈` via Dedekind (§01.7.1A). **No gap.**
- **CASE 1 (new type)** — the necessity types are the three slots of the forced quadratic
  `p²+p=1` (`p=φ⁻¹`): distinguish/preserve/close = `2` terms `+ 1` closure (degree-2, **not a
  list**). No fourth independent slot: `p³=2p−1` reduces into `span{1,p}` (Lean-proved), so a
  `p³`-type is iterated runtime = a repeat ⇒ CASE 2.

## Honesty held (per the ТЗ boundary)
- **"Three" from degree-2, never a list.** The count is derived from the quadraticity of
  `p²+p=1` (`2` terms `+ 1` closure), not enumerated.
- **Bijection written, not asserted.** The 3 slots ↔ 3 necessity-types map is exhibited, the
  COUNT and no-4th are Lean-proved; the role-*names* cite forced primitives (registration /
  self-application / M1+) — an assembly of forced pieces.
- **Cascade not over-promoted.** Closing obligation 5 forces the 3-*count* (`rank=3`). The
  leaves (`3/8` ceiling, Choptuik `γ`, `3+1` signature, spacetime-from-unit) also depend on the
  **geometric** reading `rank-3 = causal cone`, which stays a **separate** named gap (§07.51.3,
  the Connes owner-edge). The count is forced; the geometric identification is **not** flipped on
  the strength of this closure. Nothing certified was reopened.

## What this unblocks (count-level only)
`rank=3` is now forced as the number of zones / graph parts. The remaining work to fully force
the four leaves is each leaf's own geometric/physical identification — the `rank-3=causal-cone`
gap — which is the natural next root, tracked at §07.51.3.

---

# D0 — Iteration 10 report: quasicrystal carrier (a bridge closed to a forcing)

**Headline.** A lattice **bridge** is upgraded to a **forcing**: `φ` is forced as the carrier
from non-perturbative rigour (Wilson) + M1 + Penrose/de Bruijn, not postulated
(`D0-QUASICRYSTAL-CARRIER-FORCING-001`, FORCING). strength **3246 → 3260 (+14)**; external
`φ`-channels **4 → 5**; rank-3 channels **2 → 3**; integrity demotions **0**; all guards green.

## What closed and what stayed an honest gap
- **Closed (forcing).** Finite-is-rigorous-only (Wilson, YM Clay) + no-preferred-step
  (self-similar by `φ`, no `a→0`) + M1 (no exogenous step) + aperiodic-5-fold⇒`φ` (Penrose).
- **Honest named-gap (outcome b), not a fit.** The icosahedral `6D→3D` projection has rank 3
  (matches the physical slice) but cannot give `K(9,11,13)`'s `nullity 30` (it is `6D→3D`,
  internal dim 3; `30 = ` icosahedron edges is a coincidence). The missing object is a precise
  `33D→3D` cut-and-project — recorded, **not** manufactured by fitting.
- **Consistency, not over-claim.** The icosahedral QC slices `E₈` (Elser–Sloane), the same `E₈`
  the icosian roles generate — one object, two faces; this is consistency, not a new derivation
  of the zones.

## The triple, now three-channel
`rank = 3` is reached by three **independent** forcings — Frobenius (`ℍ`'s three imaginary
axes), the LA tripartite-rank theorem, and the icosahedral `3D` slice (`A₅⊂SO(3)`) — converging
with the tower-stop no-go's three zones. Independent forcings: their convergence strengthens, it
is **not** summed as one proof (per the honesty boundary).

## Carried-forward / not done
- **F.1 dossier sync: N/A** (`D0_THEORY_DOSSIER.md` removed in Iteration 2; content lives in books).
- The `33D→3D` icosahedral cut-and-project (the explicit `K(9,11,13)` identification) is the
  named open screw; the `rank-3=causal-cone` geometric gap (§07.51.3) remains the next root.
- The pre-existing 17-module `lake build D0.All` breakage stays its own spun-off task.
