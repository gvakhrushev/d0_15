# D0 — Open-frontier roadmap (living)

**What this is.** The single, de-duplicated, prioritized map of every place in the theory that is
**not yet closed**, plus the **infrastructure debt** that keeps the gate from being fully green. It is
maintained *from the repository* — every item points to a real registry row
(`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`), a §05.6 obligation, or a named guard, so it
cannot drift into fog. Length, not emptiness, is the honest measure of distance to closure
(BOOK_05 §05.6 register discipline).

**How it is kept fresh.** On each iteration: (1) re-derive the open set from the registry
(PROOF-TARGET / BRIDGE-CALIBRATION / CORE_BRIDGE_SPLIT / OPEN-Lean rows + notes carrying a gap
phrase) and the §05.6 register; (2) move any newly-closed item to "closed since last sync"; (3) add
any new named gap a closure leaves behind; (4) keep the infrastructure-debt list in sync with the
failing `tools/check_*.py` guards. Do **not** silently drop an item — close it (cert+Lean+registry)
or demote it honestly.

**Priority bands.** **P0** = actionable now, makes the corpus publication-clean (gate debt). **P1** =
finite / D0-closeable real next theory work. **P2** = sharpenable but needs a new witness/architecture.
**P3** = passport gates (await external data; falsifiable, not pure-D0 closure). **P4** = external
owners (cited edges, not a D0 action). **P5** = Mathlib-blocked (wait for the formal kernel). **P6** =
hygiene / owner-decision.

_Last synced: 2026-06-17 (Iteration 21). Registry: 288 claims, strength 4217/5114 (82.5%), integrity
demotions 0. Status mix: 162 CORE-FORMALIZED · 50 CERT-CLOSED · 20 BRIDGE-ASSUMPTIONS-EXPLICIT ·
16 EMPIRICAL-PASSPORT · 13 PROOF-TARGET · 16 NO_GO/NO-GO · 5 CORE_BRIDGE_SPLIT · 3 BRIDGE-CALIBRATION ·
2 DEPRECATED · 1 EXTERNAL-BACKGROUND._

---

## ★ Priority summary — what to do next (by importance)

1. **P0 · Make the gate fully green (infrastructure debt).** The theory is honest and the core build
   is green, but ~5–6 `check_v14_*_sync` guards still fail on **book-staleness** + one **missing Lean
   module**. This is concrete, finite, and a publication-ready corpus should not ship red guards. The
   single highest-leverage next task. (See "Infrastructure debt" below.)
2. **P1 · Holonomy residual gaps — finite items now CLOSED.** Iter-21 made α and PMNS *derived* closure
   holonomy at the honest THE/CHK/HYP split. The two **finite / machine-closeable** sub-derivation gaps
   that underpinned both are now closed: the cone-angle `π₀=(6/5)φ²` forcing
   (`D0.Geometry.pi0_forced_by_closure_balance`) and the `Δα` residue route as a closed-negative no-go
   (`D0.Spectral.delta_alpha_residue_route_blocked`, relative to one cited fact `ASSUMP-LINDEMANN-LNPHI`).
   What remains under P1 is **not finite**: the Edge-α dilation/Puiseux leg (analytic continuation, P5-style
   Mathlib-blocked) and the detection-quadratic categorical step (needs a faithful finite model). Next
   real movement is therefore P2 (architecture) / P3 (data), not more P1 finite closes.
3. **P2 · muon §00.9 caveat CLOSED; A2-Einstein/Hodge confirmed architecture-blocked.** Honesty-level
   (done, Iter-21): the muon §00.9 caveat is now cert-backed — the charged-lepton cert is a can-FAIL
   certificate asserting only the THE integer/exponent structure, with the 17-digit decimals + competing
   `206+2φ⁻²` form logged as declared HYP. Architecture-level (verified blocked): the finite
   spectral-Einstein/Hodge witness needs a tensor `G_ij=δS_A2/δh` that does not exist, across mismatched
   ℝ/ℚ carriers, with the Hodge d-forcing colliding with an existing NO-GO — genuinely new architecture,
   not a finite close. So P2's honesty work is complete; its architecture work is a real frontier, not a
   quick win. Next actionable movement is **P3 (data-bound passport gates)**.
4. **P3 · Passport gates (data-bound, falsifiable).** δ_CP (DUNE/JUNO), S_DE→DESI DR3, IceCube, the
   Bragg-spectrum metrology prediction. Pre-registered; closed by data, not by us.
5. **P4–P6 · Cite / wait / tidy.** 20 external-owner bridge edges (confirm-and-cite); K-theory & ergodic
   (Mathlib-blocked); hygiene (DEPRECATED purge decision, apparatus reduction across the other books).

---

## Infrastructure debt — P0 (actionable, finite, NOT theory)

These are guard/text desyncs and one missing module. None are theory gaps; all are mechanical to close
and would take the guard suite to fully green.

| item | symptom | what closes it |
|---|---|---|
| Missing Lean module `D0.Matter.Book04OperatorBoundary` | `check_v14_book04_operator_boundary_sync` FAIL: module + `All.lean`/`FinalBridgeIndex.lean` imports + tokens `book04Meson400Boundary`, `book04HiggsScalarProjectorBoundary`, `book04_operator_boundaries_closed`, `lower_hodge_400_cannot_promote_meson_masses`, `missing_scalar_projector_cannot_promote_higgs_yukawa_core` absent | author the small operator-boundary Lean module (the no-go content already lives in prose) + wire imports |
| Missing Book-07 spin-2 Lean tokens | `check_v14_spin2_derivation_sync` FAIL: `D0.Geometry.FiniteWeakFieldQuotient`, `PiTT4_idempotent`, `PiTT4_kills_trace`, "Poisson response plus a declared TT mode was not yet a derivation" | add the TT-projector lemmas / restore the guard-expected tokens |
| Book heading desyncs (guard wants old/different headings) | `check_v14_clean_corpus` (wants `## 04.14 …closed no-go`, `## 05.13 Active priority gates`), `check_v14_cosmology_split_sync` (wants `08.3.1 v14 active split`, `08.41 P7 reproducibility split closure`), `check_v14_sm_gauge_sync` (`04.10 SM-facing finite gauge decomposition`) | reconcile heading strings in **lockstep** (update guard OR add heading) — same pattern as the Iter-21 `05.13`/`v14→inherited` fix that recovered 3 sync guards |
| `BOOK_05` length heuristic | `check_book05_integrated_rewrite` FAIL: "Book 05 too long (1226 lines)" | the open-joints register was already trimmed (Iter-21); split or condense BOOK_05 further if the heuristic is to be honored, or relax the heuristic |
| Publication-register cert bug (pre-existing) | `vp_publication_claim_register_guardrail.py` FAIL: reads `theory_status_map.csv` for `D0-DUSTY-TABLETOP-BRIDGE-001` / `D0-LIGO-DISCOVERY-NEGATIVE-001`, which live only in the publication register | point the cert at `00_PUBLICATION/D0_CLAIMS_REGISTER.csv`, or sync those ids into the status map |

**P0 outcome (Iteration 21).** ✅ **Closed:** 17 stale `check_v14_*_sync` guards lockstepped to current honest content; the `Book04OperatorBoundary` no-go module re-activated from quarantine (+ FinalBridgeIndex/HardClosure/All wiring); BOOK_07 §07.35 spin-2 owner citations; 5 heading desyncs; the publication-register cert (now reads the register). Gate went **~19 red → 2 red**, `lake build D0.All` green, `d0_score` integrity demotions 0. **2 residual — NOT gate-wiring, not gameable:** (1) `check_condensed_ktheory_module_sync` = **Tier-3 Mathlib-blocked** (demands deep noncommutative-solenoid spectral-triple + K0-gap-labeling theorems; operator K-theory absent from Mathlib 4.30 — see P5; finite shadows certified, deep theorems can't be honestly Lean-proved, stubs declined). (2) `check_standard_language_audit_budget` = **editorial debt** (145 jargon flags vs 125 budget; pre-existing — base-v14 was 118, session-start 149; the cleanup cuts reduced it to 145; closing = a standard-language rewrite pass, which is the audit's purpose, NOT a guard recalibration since the budget must ratchet down).

---

## P1 — finite / D0-closeable (the real next theory work)

**Status (Iter-21):** the two genuinely **finite / machine-closeable** P1 items are now **CLOSED**
(cone-angle `π₀` forcing; `Δα` residue route closed-negative). The remaining two rows are **not
finite identities** — Edge-α is an *analytic* continuation leg (unitary dilation / Puiseux series,
absent from Mathlib 4.30 → frontier, see P5), and detection-quadratic is a *categorical* forcing
step (needs a faithful finite model that does not yet exist). Neither is a verified-closure target;
they are kept here as named, honestly-bounded gaps, not quick wins.

| item | registry anchor | status | what closes it |
|---|---|---|---|
| Cone-angle `2π₀` (`π₀=(6/5)φ²`) micro-derivation | `D0-PI0-DISCRETE-ANGLE-001`, §04.6.π.4 | ✅ **CLOSED (P1, Iter-21)** — Lean + cert | `D0.Geometry.pi0_forced_by_closure_balance` machine-checks that the δ₀-closure balance forces `π₀=(6/5)φ²` (cert `vp_pi0_discrete_angle.py` + control); residual = the deeper origin of the closure ratio (`§04.6.π.4`), a narrower named target |
| `DeltaAlphaResidueBlocked` transcendence lemma | `D0-CVFT-F1` (route **BLOCKED**) | ✅ **CLOSED (P1, Iter-21)** — Lean + 1 cited fact | `D0.Spectral.delta_alpha_residue_route_blocked` proves `1/lnφ` is transcendental (inverse-transcendence) hence `∉ ℚ(φ)`, so no `φ`-graded residue equals the algebraic `Δα` — closed-negative no-go. Relative to the single explicit hypothesis `ASSUMP-LINDEMANN-LNPHI` (transcendence of `lnφ`, Lindemann–Weierstrass; a hypothesis, **not** a global axiom); D0 proves `φ`/`ℚ(φ)`-algebraicity + inverse-transcendence from `φ²=φ+1`. |
| Edge-α dilation / Puiseux leg | `D0-EDGE-002` (trace leg CLOSED as `zetaEdge_neg_one`; finite shadows cert-closed at `D0-EDGE-ALPHA-001`/`D0-EDGE-RAMIFICATION-001`) | PROOF-TARGET — **analytic frontier, not finite** | the unitary-dilation / torus-ramification **Puiseux** leg: analytic continuation of the edge trace through the ramified cover. This is *not* a finite ℚ(φ) identity; unitary-dilation (Sz.-Nagy) + Puiseux-continuation are absent from Mathlib 4.30 → effectively P5-blocked. The finite content (trace identity, ramification shadows) is already CORE/cert. |
| detection-quadratic categorical exhaustiveness as a machine theorem | `D0-DETECTION-QUADRATIC-001` | CORE for the algebra; categorical step is forcing prose | formalize "exactly two comparison kinds" as a decidable statement if a faithful finite model exists |

## P2 — sharpenable but needs a new witness / architecture

| item | registry anchor | status | what would sharpen / close it |
|---|---|---|---|
| Finite A2-Einstein / Hodge matter-gravity witness | `D0-SPECTRAL-EINSTEIN-001`, `D0-HODGE-LINKS-001` | PROOF-TARGET — **architecture-blocked** (Iter-21 P2 audit, verified) | The genuine scalar piece (`a2_is_eh_proxy`) is already CORE under `D0-GEOM-SPECTRAL-ACTION-LADDER-001`. OPEN is the rank-2 `G_ij=δS_A2/δh` (symmetric **and** divergence-free) — *no such object exists in `D0/`*. Two verified blocks: (1) a **carrier mismatch** — `HeatTraceEHProxy` lives over `ℝ Matrix N N`, `FiniteSpin2WaveOperator` over `ℚ SymPert4`; (2) a **missing variational-derivative operator**; and for the Hodge link, the needed d-conservation forcing **collides with an existing NO-GO** (`canonical_stress_conservation_no_go`). Real per-side assets exist (`spin2_coupling_depends_only_on_tt_stress`, `PiTT4_kills_trace/_gauge`) but don't bind across carriers. New architecture, not a finite witness — do NOT anchor an ASSUMP row to the scalar. |
| Muon mass-ratio §00.9 grammar-priority gap | `D0-LEPTON-002` (CERT-CLOSED) / BOOK_04 §04.8 | ✅ **caveat CLOSED (P2, Iter-21)** — cert hardened; value stays **HYP** | The §00.9 caveat is now **cert-backed**: `vp_charged_lepton_transfer_certificate.py` rewritten as a **can-FAIL** cert asserting only the THE structure (computed Lucas `L₁₁+L₄=206`; exponents `0,1/4,1/3`) with reachable negative controls (wrong layers miss 206; free/democratic Yukawa fit rejected), and **logging the 17-digit decimals + the competing `206+2φ⁻²` form (`\|miss\|≈4.35e-3`) as declared HYP**. The prior print-stub (couldn't FAIL) is gone. The mass-ratio *value* remains honestly HYP; *deriving* the decimal ladder from the integers stays a named target (winding `W` is PHYSINPUT, no forced ℚ(φ) operator — not faked). |
| `Δα` analytic owner | §05.6 obligation 4 / `D0-DELTA-ALPHA-MOMENT-001` | **superseded** by the holonomy route (Iter-21) | Δα is now *derived* as the seam closure holonomy (`D0-ALPHA-HOLONOMY-002`, structure THE / data CHK); the old residue-amplitude route is **closed-negative** (transcendental). Remaining: the holonomy's own `2π₀` origin (→ P1). |

## P3 — passport gates (await external data; falsifiable, not pure-D0 closure)

**Passport-honesty sweep (Iter-21).** The data-bound passport *certificates* were audited for
hollow-green over-claims (a cert printing PASS/FAIL with no data, often over a hand-set `status:READY`
manifest for an absent cache file). **Demoted `EMPIRICAL-PASSPORT`→`PROOF-TARGET`/`OPEN` or re-tagged**
(no longer registered as passed data confrontations): `D0-PASSPORT-DESI-BAO-001`,
`D0-PASSPORT-ICECUBE-HESE-001`, `D0-PASSPORT-LIGO-CATALOG-001`, `D0-PASSPORT-SPARC-001`,
`D0-H0-EVOLVING-W-001` (tautology falsifier removed), `D0-DUSTY-PLASMA-001` (SEED),
`D0-CRITICAL-COLLAPSE-001` (fabricated hash-pinning stripped → `CORE_BRIDGE_SPLIT`),
`D0-E8-COLDEA-ANCHOR-001` / `D0-DSI-EXPERIMENTAL-001` / `D0-COSMO-002` (→ `CERT-CLOSED` FORM, fabricated
data legs stripped). Two faked `READY` manifests (DESI, GWOSC) reverted to `MISSING`; the rewritten certs
now split FORM (can-FAIL) from VALUE (honest `SKIP_*_EXTERNAL_DATA_REQUIRED`). **Corrected but kept as
genuine passports:** `D0-PMNS-DELTA0-NUFIT-001` (`sin²θ₁₂` value typo → exact `0.30547`; JUNO citation
flagged unpinned) and `D0-ALPHA-MEASUREMENT-LIMIT-001` (the data-contradicted "from below" bet →
straddle + an asserted falsifier). The rows below are the genuine data-bound targets that remain.

| item | registry anchor | status | gate |
|---|---|---|---|
| `δ_CP ≈ π₀ ≈ π` (CP near-conservation, normal ordering) | `D0-PMNS-DELTACP-PI0-001` | **HYP** prediction | future δ_CP precision (DUNE / JUNO / T2HK) |
| `S_DE` exceptional-point → DESI H₀ | `D0-CVFT-F8` | PROOF-TARGET | frozen two-mode operator + **DESI DR3** |
| `S_DE` cubic-vs-quadratic fork | `D0-VACUUM-CUBIC-WINDOW-001` | both branches exact; discriminator computed | **DESI DR3** selects the branch |
| IceCube dynamic-feedback passport | `D0-CVFT-F5` | PROOF-TARGET | frozen operator + IceCube data manifest |
| Horizon emission / greybody | `D0-CVFT-F2` | PROOF-TARGET | freeze the boundary operator + an observable passport |
| Bragg-spectrum / Φ²-flux metrology | `D0-QUANT-MET-003/004` | PROOF-TARGET (Lean legs resolved; physics is sector-hypothesis / empirical) | a tabletop Bragg / quantum-metrology measurement |

## P4 — external owners (20 cited edges; confirm-and-cite, not a D0 derivation)

`BRIDGE-ASSUMPTIONS-EXPLICIT` (20). Each is a real classical theorem absent from / external to D0; the
D0-side anchor is a real cert, the external step is cited via an `ASSUMP-*` ledger row. Re-attack only
if D0 can internalize one.

- Geometry/operator: `D0-CONNES-RECONSTRUCTION-OWNER-001` (metric = Dirac spectrum; the cone-speed
  residual of `D0-RANK3-CAUSAL-CONE-FORCING-001`), `D0-DIXMIER-RESIDUE-OWNER-001`,
  `D0-RIEFFEL-GHP-CONTINUUM-OWNER-001`, `D0-TIME-MODULAR-FLOW-OWNER-001` (Tomita–Takesaki),
  `D0-ADLER-WEISS-PARTITION-OWNER-001`.
- Physics axioms: `D0-QM-BORN-001/002`, `D0-COMPLEX-QM-FORCING-001`, `D0-M1-INFO-RECONSTRUCTION-001`,
  `D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001` (continuum YM mass gap = Clay), `D0-GAUGE-MATTER-001`,
  `D0-RG-001`, `D0-SMOOTH-001`, `D0-LEAN-BRIDGE-001`, `D0-ENTROPIC-DARK-GRAVITY-001`,
  `D0-LATTICE-FINITENESS-BRIDGE-001` (Wilson-1974).
- Number-theory / complexity edges (M1-reductios, cited): `D0-FROBENIUS-DIVISION-3D-001` (HYP — two
  different 8's), `D0-HODGE-M1-REDUCTIO-001`, `D0-RIEMANN-AXIS-M1-001`, `D0-PVSNP-LYAPUNOV-M1-001`.

## P5 — Mathlib-blocked (wait for the formal kernel)

| item | registry anchor | blocker |
|---|---|---|
| K-theory / spectral-triple / phason-holonomy class | `D0-KTHEORY-001`, `D0-QUASI007/008/009`, `D0-SOLENOID-001/-GRAVITY-001`, `D0-MESON-K0-001` | operator K-theory / Bellissard IDS→K₀ absent from Mathlib 4.30 (finite shadows already certified) |
| topological/measure conjugacy (`φ⁻²` rotation ↔ toral `T` foliation) | §05.6 obligation 6 | Sturm / Morse–Hedlund ergodic machinery not in the formal kernel (symbolic part certified to 4000 symbols) |
| Pisot ≥3-letter conjecture | (cited, time layer) | external number theory |

## P6 — hygiene / owner-decision

| item | disposition |
|---|---|
| 3 `DEPRECATED` tombstones (`D0-GAUGE-BIANCHI-GRADED-DEPRECATED-001`, `D0-EDGE-001` redundant trace target, `D0-EXTERNAL-BACKGROUND-HURWITZ-…-001`) | keep as honest tombstones (replaced/redundant) or purge by owner decision — they are not double-counted in strength |
| Apparatus footnote layer in the **other 9 books** | BOOK_00's was removed (Iter-21); the same internal-provenance "forcing: GOLDEN …" endnotes exist elsewhere (some books — e.g. BOOK_07 — also carry **real external citations** in their apparatus, which must be kept). Owner decision: extend the BOOK_00 removal, keeping genuine citations. |
| `γ_Choptuik ↔ 3/8` packing probe | `D0-PACKING-LIMIT-001` (HYP, D=4 coincidence) — book §07.51.4 removed (Iter-21); claim stays cert-backed as the canonical record. Accept the coincidence or find a common `F(D)`. |
| `nullity 30 = icosahedron edges`; `K(9,11,13)` explicit `33D→3D` projection | confirmed coincidence / resolved by separation (`D0-CARRIER-NOT-ICOSAHEDRAL-001`) — do not promote (anti-numerology) |
| `ℍ→𝕆` octet `|Ω₈|=8` | `D0-FROBENIUS-DIVISION-3D-001` HYP (two different 8's) — needs `dim 𝕆=8` and `|Q₈|=8` identified first |

---

## Closed / changed since last sync (Iter-14 → 21 — do not re-open as "open")

- **α correction: fit → derived closure holonomy (Iter-21).** `q_res` fit retired; `α⁻¹ = 359φ⁻² − φ⁻⁵
  + φ⁻¹⁷(1 + lnφ·sin(12/5)) = 137.035999151` registered at the **honest split**: structure **THE**
  (`D0-SEAM-HOLONOMY-001`, `D0-PI0-DISCRETE-ANGLE-001`, `D0-Q8-SIN-CHANNEL-001`, Lean-proved); 9-digit
  CODATA match **CHK** (`D0-ALPHA-HOLONOMY-002`); last ~10⁻⁸ **HYP** (`D0-ALPHA-MEASUREMENT-LIMIT-001`).
  The residue route to Δα is **closed-negative** (transcendental `ln φ`).
- **PMNS angles: MECH-LIMIT → derived seam-topology rule (Iter-21).** `D0-PMNS-SEAM-TOPOLOGY-001` — the
  δ₀-degree↔cycle-topology rule is **THE** (directional structure Lean-proved + M1-forced via
  `seamDegreeSelector`); the numeric values are **CHK** (<1σ vs JUNO-2026 + NuFIT-6.0); shared `ξ₅`
  (`D0-XI5-CROSS-SECTOR-001`).
- **rank-3 = causal cone: re-scoped FORCED → `CORE_BRIDGE_SPLIT` (Iter-21).** Correction to the prior
  "closed, do not re-open": `D0-RANK3-CAUSAL-CONE-FORCING-001` — the (3,1)+Pisot signature **arithmetic**
  is machine-checked CORE, but the rank↔metric-cone **identification** is a counting-multiplicity
  **named bridge**, not a closed theorem. The cone-speed metric remains the Connes external edge (P4).
- **Muon action-closure: "theorem" → HYP (Iter-21).** The integer `L₁₁+L₄=206` is THE; the value and the
  17-digit decimal ladder are HYP with an explicit §00.9 two-formula caveat (→ P2).
- §05.6 obligation 5 (tower stops at 3) — closed (`D0-TOWER-STOP-NOEXT-001`). obligation 4 Δα exact value
  + bound — closed (`D0-DELTA-ALPHA-EXACT-001`); analytic owner superseded by the holonomy route.
- `D0-OMEGA8-CENTER-001`, `D0-NO-GO-STRESS-SUITE-001` rank-one leg, edge-α trace leg — closed (Iter-15).
- **Repo de-versioning (Iter-21):** all `D0_v14/v15/v16_*` filenames stripped to `D0_*`; books cleaned of
  reader-facing version tags + the BOOK_00 apparatus provenance layer.
