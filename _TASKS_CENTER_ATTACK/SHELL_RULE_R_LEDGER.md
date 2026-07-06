# SHELL-RULE-R — rules ledger + anti-shopping discipline (FROZEN before any rule is scored)

**Status:** DRAFT campaign anchor. Goal: a mass-blind rule R: {13 core slots} → {A,B,C shells,
excluded} derived from OWNED scene structure, per SHELL_MEMBERSHIP_V2_RESULTS.md's completion
object. The confirmed target (Q2, exact p=8.66e-05) is KNOWN — therefore every rule here is
post-hoc by construction until it passes the out-of-construction tests below.

## Discipline (frozen)

1. A candidate rule must cite its owned-text motivation (file:line) BEFORE its membership match
   is computed; rules invented by staring at the pattern are logged as PATTERN-OBSERVATIONS,
   not derivations.
2. EVERY attempted rule is logged here — failures included. Deleting a failed attempt = fraud.
3. Grading cap: "candidate rule (post-hoc, structurally motivated)" until it ALSO predicts
   something NOT used in its construction, pre-stated: (i) WHICH particle group sits at WHICH
   φ-radius (the passport's owned hierarchy r_A≈φ⁴r₀, r_B=φ²r₀, r_C≈φ⁶r₀ — order prediction);
   (ii) placements of core-extension particles (ν_μ, ν_τ) if the slot list is extended;
   (iii) the {μ,s} exclusion and {b,d} doubling must FOLLOW from the rule, not be inputs.
4. Vocabulary: never "derived/forced" pre-skeptic; registry untouched.

## Computed facts (verified this session, compute-first)

- **Slot 1 = γ (light node)**: the passport's by_id dedup displaces ν_e (idx 1) with the
  gamma-node (vp_core13_shell_geometry_passport.py:152-164). ν_e is NOT in the fitted 13.
- Membership in particle terms:
  A = {γ, b, d, e, u} · B = {τ, W, c, Z} · C = {b, d, t, H} · excluded = {μ, s} · A∩C = {b, d}.

## Pattern-observations (POST-HOC — hypotheses to motivate from owned text, NOT results)

- P-1: excluded {μ, s} = exactly generation-2 ∩ T3=−1/2 (c, the gen-2 up-type, IS included in B).
  Owned hook to test: gen↔zone binding (THE 04.6.M1.gen) puts gen-2 in zone 11 = the TORUS zone,
  and the shells ARE torus boundaries (F3c + TorusCore13GeometryOrigin) — candidate reading:
  the memory-zone's own down-sector cannot sit on the memory-torus boundary it constitutes.
- P-2: A∩C = {d, b} = down-type quarks of gen-1,3 (the gen-2 down-type s is the excluded one);
  down-type LEPTONS split single-shell (e→A, τ→B, μ→out). Quark/lepton multiplicity differs.
- P-3: C = {d, b, t, H} = the EW-breaking pair (t,H) + both surviving down-type quarks;
  B = {τ, W, c, Z} carries both weak bosons.
- P-4: A carries the massless anchor γ + the lightest charged fermions {e, u, d} + b (b is the
  odd one in A — any rule must place b on TWO shells).

## Owned anchors for rule construction (cited; the raw material)

- THE 04.6.M1.gen (BOOK_04:912): generation = zone label; center→e, torus→μ, shell→τ.
- THE 04.8.L.1 (BOOK_04:1046): muon localized in zone 11 (memory torus).
- REM 04.6.M1.Λ (BOOK_04:922): matter = zones 9+11; vacuum/terminal = 13.
- §04.CVFT.F3c (BOOK_04:401-449): 3-orbit geometry ≡ V_shell = span{|9>,|11>,|13>}; PDG naming
  stays passport-layer.
- T2_PRIME_TYPE_FORCING P3: Q₈ Fourier triple {E₀,E₄,E₃} ↔ zones {9,11,13}; E₄ = the unique
  order-memory block (L₋₁=−1); E₀ trivial/unramified.
- TorusCore13GeometryOrigin.lean: 3 shell radii (1, (a+1)/2, a), ratios proved; radial-hopping /
  phase-drift noncommutation.
- V₉ = Ω₈ ⊔ {ω₀} (T2-P1; BOOK_01 §01.8/§01.20): zone-9 role cycle with distinguished ω₀.
- Constraint no-gos to respect: lepton-branch NO-GO (BOOK_04:188; 2 orbit-branches ↛ 3
  generations); R1 representation-reconstruction NO-GO (GL(3) freedom on the trivial isotype);
  D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001.

## Rules attempted (append-only)

### Attempt 1 — "shell = zone(generation)" family (6 bijections; scored 2026-07-04)

Rule: fermion slot -> zone via THE 04.6.M1.gen (gen1->9, gen2->11, gen3->13); H -> zone 13 via
REM 04.6.M1.Λ; gamma/W/Z left UNSCORED (no owned assignment text — recorded gap); shell =
bijection(zone), all 6 bijections scored mechanically. Metric: slot-level set-equality over the
10 scorable slots; subset counted as "partial".

| bijection (9,11,13)-> | exact | partial | note |
|---|---|---|---|
| **A,B,C** | **5/10** | **2** | residuals = EXACTLY the three anomalies: tau->B, {mu,s} excl, {d,b} doubling |
| A,C,B | 3/10 | 1 | |
| B,A,C (naive-radial) | 2/10 | 1 | my spatial reading of radius order — see tension note |
| C,B,A | 1/10 | 2 | |
| C,A,B | 1/10 | 1 | |
| B,C,A | 0/10 | 1 | |

**Calibration (exact, full 69,300 family):** P(random structure-matched assignment agrees with
the best prediction on >=7/10 slots) = **0/69,300**; Bonferroni x6 rules keeps p < 8.7e-5-scale.
The 7/10 agreement (5 exact + 2 subset) of the owned zone=generation rule is far outside the
null family's reach.

**Named tension (open, logged not resolved):** under the winning bijection the zone-11 (torus)
shell is B with the SMALLEST fit radius (phi^2 r0), while a naive spatial reading (9=center
innermost) favors B<->9 — which scores 2/10. Resolution requires an owned chart interpretation
of the (n_abs, H13_u) plane radii; none found yet. Do NOT resolve by fiat.

**Residual structure the rule leaves unexplained (the next completion targets):**
(i) tau sits on the zone-11 boundary B, not its gen-zone 13; (ii) {mu,s} (gen-2 = zone-11
residents) sit on NO boundary; (iii) {d,b} (down-quarks gen-1,3) sit on TWO boundaries (A and C).
Reading consistent with P-1: the zone-11 boundary carries {tau,W,c,Z} while zone-11's own
down-sector {mu,s} is excluded — "the memory zone's boundary is populated by others; its own
down-sector sits on no boundary". Q8-block motivation (E4 = order-memory, L_{-1}=-1) is the
pre-registered next attempt; it must PREDICT (i)-(iii), not restate them.

### Attempt 2 — radius-profile test + E4 coupling anchor (scored/searched 2026-07-04)

**(2a) COMPUTED — "shells = literal Lean-torus boundaries" FAILS on radii.** Observed fit-radius
ratios rA/rB=2.800, rC/rB=6.671. Phi-hierarchy (phi^2, phi^4): devs 6.9% / 2.7% — fits. Lean
torus profile (1,(a+1)/2,a): best JOINT a=5.715 gives devs 19.9% / 14.3%; single-ratio fixes give
31-37% on the other; no phi-power a (phi^3, phi^4) rescues both. VERDICT: the (n_abs,H13) chart
radii are PHI-GRADED, not torus-profile-graded; the literal torus-boundary reading of the three
circles is dead; the chart interpretation of "which zone owns which radius" remains open (the
attempt-1 tension is NOT resolvable via the Lean torus profile).

**(2b) FOUND — owned coupling anchor for the E4 residuals (not yet a selector).**
BOOK_01 §01.7.1B (BOOK_01:804-830; CORE-FORMALIZED via D0-OMEGA8-CENTER-001, Lean
D0.Foundation.Omega8Center, cert vp_omega8_center_collapse.py): [Q8,Q8] = Z(Q8) = Phi(Q8) = {±1}
— "orientation ± bit, order-memory remainder and non-generating remainder are one Z2", and
"fermionic statistics read straight off the orientation bit of the scene: the 4pi periodicity is
the central Z2 ... the spinor double-cover leaf index". T2-P3: E4 is the UNIQUE block seeing this
register (L_{-1}=-1). => The owned bridge exists: E4/zone-11 uniqueness is characterized by the
SAME Z2 that owns fermionic statistics. MISSING (the actual selector, next attempt's target): the
owned rule for WHICH particles couple to the E4 boundary — i.e. why {tau,W,c,Z} sit on B while
{mu,s} sit nowhere and {d,b} sit twice. Attempt 3 must build the selector from the spin/orientation
Z2 + zone-generation binding and PREDICT the three residuals; restating them is forbidden.

### Attempt 3 — axis/register selector family: 4 selectors + 96-variant ablation (2026-07-04)

**Citation correction recorded FIRST (discipline rule 1).** The zone<->E-block matching is NOT
cited below as forced: T2_PRIME_TYPE_FORCING.md's forcing was killed twice (v1+v2, kills accepted
— T2_PRIME_FINAL_STATE.md). What survives and is used: (a) 9<->E0 "agreed by every party and every
key"; (b) the block signatures as machine facts (w8_holomorph_check.py 18/18 PASS: E0 the common
fixed/trivial "unramified" block; E4 the unique L_{-1}=-1 block; Z-coset-function correction of
record applied); (c) m = (9<->E0, 11<->E4, 13<->E3) as the identification "every coherent
owned-material chain converges on" with "zero positive owned support" for m' — an X5-residual
identification (R1 conditionality: the z^4<->Q11 weld is CONDITIONAL-EXTENSION, "lambda chosen,
not forced"; R2 attachment: TorusShellAttachment.lean is DRAFT, unminted), not a theorem. Every
"E4 = the order register of zone 11" statement below carries this dependency. Attempt 2b's
citation of "T2-P3" is hereby narrowed to the surviving machine facts.

**Selectors constructed (motivations cited BEFORE scoring; full tables logged for audit).**
Shared pieces in all four: fermion zone = zone(generation) (THE 04.6.M1.gen, BOOK_04:912);
zone->shell bijection 9->A, 11->B, 13->C (NOT owned — carried from attempt 1's score-selected
winner; the one owned anchor, H as "macroscopic phason condensation in the V13 shell"
(BOOK_04:1615) + REM 04.6.M1.Λ, fixes 13-shell=C only if H∈C is read off the target — circular,
flagged); H->C (owned as above); up-type single-seat at shell(zone(gen)).

- **S1 — zone(gen) + boson anchors** (attempt-1 rule completed to all 13 slots). gamma->A
  (§04.5 terminal matter triad "charged terminal register + neutral leakage branch + massless
  line carrier", BOOK_04:643-665, seated at the zone hosting the terminal role cycle, T2-P1
  V9=Ω8⊔{ω0} — word-match "terminal", connective mine); W,Z->B (REM 04.6.M1.mH "Vector bosons
  W,Z set the edges of the vacuum cell; the Higgs scalar H sets its diagonal", BOOK_04:926;
  edge = the matter|vacuum seam = 11-boundary — reading mine); fermions at zone shells.
  Table: γA bC dA τC WB μB sB cB ZB eA uA tC HC.
- **S2 — the axis/register selector** (the new construction; full motivation chain in
  SHELL_RULE_R_MEMO.md). Rule: (i) up-type quarks = the axis-invariant A2 vertex (THE
  04.6.M1.charge, BOOK_04:910: projection on "the scene's center<->shell symmetry axis" gives
  "+2/3, −1/3, −1/3") -> single seat at zone shell; (ii) down-type quarks = the degenerate
  conjugate pair -> stored BY that same owned projection: axis = span{|9>,|13>} in V_shell
  (F3c, BOOK_04:406), degenerate image -> BOTH axis shells {A,C}; pi_axis|11> = 0 -> the
  zone-11 pair member (s) is annihilated -> excluded; (iii) charged leptons by the exact
  exponent row (0,1/4,1/3) (BOOK_04:1113,1135 THE): e unramified -> the unramified block
  E0 -> A (double word-match; e = forced terminal calibration register, BOOK_04:964-996);
  mu rides the 4-cycle = "terminal role capacity" sheet (BOOK_04:1939) — winds ROLE space,
  not shell space -> invisible to the shell chart -> excluded; tau rides the 3-cycle =
  "scene-rank" sheet — winds the 3-zone/shell triple; a cyclic winding's datum is its loop
  ORDER (BOOK_00:168), which registers only on E4 -> B; (iv) W,Z = the doublet-splitting
  ± register's own quanta (T3=±1/2 owned at BOOK_04:1377; SU(2)=double-braid THE 04.6.M1.gauge
  BOOK_04:908; order-memory = order of operations §01.7.1A) -> seat on the register block
  E4 -> B (consistent with the mH "edges of the vacuum cell" reading); (v) gamma -> A as S1;
  H -> C owned. Table: γA b{AC} d{AC} τB WB μ∅ s∅ cB ZB eA uA tC HC.
- **S3 — base-anchor doubling** (competitor): THE 04.8.L.1 "any stable excitation must
  additionally be anchored to the reference addressing level (the base)" read as "down-sector
  and leptons also seat on the base shell A". Table: γA b{AC} dA τ{AC} WB μ{AB} s{AB} cB ZB
  eA uA tC HC.
- **S4 — strawman control** ("everything Z2-charged to the register"): all T3=−1/2 fermions
  + W,Z -> B; up-type at zone shells; γA HC. Table: γA bB dB τB WB μB sB cB ZB eB uA tC HC.

**Scores (13-slot set-equality; exact 69,300 null via all_assignments() re-run, asserted
69,300 + frozen∈family; metric frozen = attempt-1 metric extended to 13 slots; partial =
nonempty proper subset):**

| selector | exact | partial | miss | null P(agree>=k*) | Bonferroni x4 |
|---|---|---|---|---|---|
| S1 | 8/13 | 2 (b,d) | 3 (τ,μ,s) | 72/69300 = 1.04e-3 | 4.16e-3 |
| **S2** | **13/13** | 0 | 0 | **1/69300 = 1.44e-5** | **5.77e-5** |
| S3 | 9/13 | 1 (d) | 3 (τ,μ,s) | 20/69300 = 2.89e-4 | 1.15e-3 |
| S4 | 8/13 | 0 | 5 (b,d,μ,s,e) | 105/69300 = 1.52e-3 | 6.06e-3 |

S1/S3/S4 all FAIL to reproduce the membership (logged failures). S2 reproduces it exactly;
within the frozen null family only the target itself agrees on >=13 slots.

**T3 ablation (the brutal test: was the selector free at its joints?).** S2 has FOUR connective
choice points not fixed by owned text: P1 down-pair storage {axis-pair, nearest-axis-single,
own-zone, register-B}; P2 non-base lepton placement {register+self-exclusion, register-no-excl,
axis-like-quark, zone-seat}; P4 W,Z {register-B, vacuum-own-C, unplaced}; P5 gamma {terminal-
triad-A, abelian-C}. (e->A, H->C, up-type seats are owned-fixed in all variants.) Full 4x4x3x2
= 96-variant enumeration against the target: agreement histogram {13:1, 12:3, 11:6, 10:12,
9:17, 8:19, 7:20, 6:14, 5:4}. EXACTLY ONE variant hits 13/13 — S2 itself = (axis-pair,
register+selfexcl, register, terminal-triad) — and it is also the ONLY variant whose prediction
even lies inside the 69,300 structure family. Union bound charging the WHOLE connective space:
p <= 1/69300 = 1.44e-5. HONEST READING: the winning connectives were chosen knowing the target
(96 a-priori combinations; the target picked the winner); what the owned text supplies is the
raw material and three post-assembly textual echoes — the verbatim doubled "−1/3, −1/3" in THE
04.6.M1.charge; the owned mu/tau sheet-type ASYMMETRY (4-cycle role-capacity vs 3-cycle
scene-rank, BOOK_04:1939 + "muon through the 4-cycle, tau through the 3-cycle" BOOK_04:1135,
reaffirmed THE-status in T2_PRIME_FINAL_STATE.md); and the W,Z "edges of the vacuum cell" line.
The {μ,s} exclusion and {b,d} doubling FOLLOW mechanically from the frozen rule (outputs, not
membership inputs) — but the rule was assembled post-hoc. Grading cap HOLDS.

**T1 (radius order) — FAIL, logged.** S2 owns no radius functional. The only owned radial order
(TorusShellAttachment.lean:84-95, radii strictly increasing inner9 < core11 < outer13; DRAFT
plumbing) transported through the bijection predicts r_A < r_B < r_C — CONTRADICTED by the
frozen chart order r_B < r_A < r_C. The rung VALUES match the owned AF Dirac² even-power ladder
{φ⁰,φ²,φ⁴,φ⁶} (BOOK_02:1295, D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001) — but no owned text
assigns zones to rungs, and candidate owned orderings (zone size; Laplacian eigenvalue
24/22/20; block dim 1/3/4) ALL fail to give the observed 11 < 9 < 13. Attempt-1's tension
stands UNRESOLVED; the selector does not predict the radius order.

**T2 (ν_μ/ν_τ under core extension) — PRE-REGISTERED PREDICTION: both EXCLUDED (no shell
membership).** Owned basis: §04.4.9 neutrino = "neutral bulk phason wave" (BOOK_04:631-641,
BULK not boundary) + ν_R ∈ ker A is zone-BALANCED, not zone-localized (BOOK_04:1392). The
alternative (T3-mirror: ν_μ->B, ν_τ->C as up-like doublet members) is REJECTED on the owned
bulk text — a target-blind discrimination, since no target exists for neutrinos. Consistency
note (artifact-grade only): ν_e is indeed absent from the fitted 13, but by the by_id dedup
(vp_core13_shell_geometry_passport.py:152-164), not by a fit decision. FALSIFIER: any future
core-extension fit seating ν_μ or ν_τ on a circle kills S2's lepton logic.

**Verdict.** S2 = "candidate selector (post-hoc, structurally motivated)" — the cap does NOT
lift: T1 failed, T2 pending, T3 shows the connectives were target-informed. What attempt 3
adds over attempt 1: +5 slots (8->13 exact), every piece's motivation status EXPLICIT
(owned / owned-with-my-connective / unowned), the exclusion+doubling now DERIVED from a stated
mechanical rule rather than restated, and two forward falsifiers (ν seats; any core-extension
particle now gets a forced assignment). Consolidated memo: SHELL_RULE_R_MEMO.md.

### Skeptic #1 verdict on attempt 3 / S2 — ACCEPTED IN FULL (no defense), 2026-07-04

KILLS (named objects):
- K1 bijection: the ONLY owned radial object (TorusShellAttachment.lean:84-95 strictMono, via
  chart order) selects m_rad=(9->B,11->A,13->C) — the LOSER (2/10). The winning bijection has no
  independent owned support (H/V13->C circular; e->A routes through the bijection itself). All
  13/13 rests on a fitted joint. S2-as-derivation: DEAD in current form.
- K2 N-7 weight-space<->V_shell identification: same shape as Iter25's rejected "seductive
  coincidence" (multiplicity transported between unrelated index spaces); carried s->0, b/d
  doubling showcase slots.
- K3 T2 nu-falsifier: UNTESTABLE, not pending — PDG mcd has no nu masses and the frozen protocol
  skips massless slots; "EXCLUDED" is the pipeline default. Aggravation: the owned triad sentence
  (BOOK_04:643-665) includes the neutral leakage branch, so c4's own principle would SEAT nus.
WOUNDS: connective 96-space gerrymandered — the memo's own principles applied uniformly generate
mu->A (terminal-capacity sheet BOOK_04:1939 + c4 terminal-zone seating) and mu->C (tau-principle +
E3 role-indexing) OUTSIDE the space; the flagship {mu,s} exclusion was never charged against its
own grammar (mu-seat trilemma = strongest finding). {mu,s} two-mechanism compositionality +
stacked justification = overfit tells. No committed ablation script (discipline gap).
WHAT SURVIVES (skeptic's own computation):
- Target-specialness STRENGTHENED: free-exclusion family 5,405,400 enumerated exactly; S2's
  membership P(agree>=13) = 1/5,405,400 = 1.850e-7; agreement-12 combinatorially impossible;
  nearest competitors 66 members at 11/13. The frozen membership is an extraordinarily special
  assignment — a fact about the TARGET independent of S2's motivation quality.
- All 13 citations verbatim-clean; all null counts reproduce exactly.
GRADE (accepted): "candidate selector (post-hoc, owned-VOCABULARY-motivated; structural signals,
where they exist, are net-adverse)". Errors of record: "structurally motivated" over-claim;
untestable falsifier presented as pre-registered; ablation space presented as a-priori.

### Attempt 4 — direction (root-asymmetry rebuild; owner's directive 2026-07-04)

The owner's root-asymmetry program is now the ONLY path, constrained by the kills:
(a) the bijection joint must be resolved FIRST: either derive the winning map from owned
    structure (nothing found; K1 says the owned object votes m_rad), or DROP zone<->circle
    entirely — candidate reframe: circles = delta-degree strata (delta-cascade delta_{-n} =
    delta0^{n+1}, BOOK_01:1122 CERT-BACKED; radii phi^2/phi^4/phi^6 = Q(6)/Q(8)/Q(10) even
    ladder rungs) instead of zone boundaries; the owned m_rad object then has nothing to
    contradict.
(b) connectives only from the owned root asymmetry: branch split (a0,b0)=(phi^-1,phi^-2)=p+p^2=1;
    2*delta0=phi^-3 full branch gap (BOOK_01:669); round-trip factor 2; GaloisConjugateBalance
    (CORE-FORMALIZED) on VALUES only — Iter25 guardrail: never Galois-as-graph-symmetry.
(c) every connective must be charged against its uniform-application competitors (the mu-seat
    trilemma test becomes a mandatory control: a rebuilt selector must have NO bespoke clause).
(d) falsifiers must be computable under the frozen protocol (K3 lesson).

### Attempt 4 — root-asymmetry rebuild: CLEAN UNDERDETERMINATION (executed 2026-07-04; script
### archived: shell_rule_r_attempt4.py — the missing-ablation discipline gap repaired)

**Owned-material sweep for the reframe (grep-verified; quotes checked at file:line).**
- Q(D) ladder: `Q(D)=2δ₀φ^(D−1)=φ^(D−4)`, CERT-BACKED "for D=1..8" ONLY
  (BOOK_01:1105-1122; vp_dim_ladder_compact.py:30-36 loops `for D in range(1, 9)`). Owned
  semantic anchors exist ONLY at D=1 ("binary quantum ... φ⁻³=2δ₀") and D=4 ("centered on the
  four-role budget |ABCD|=4"). NO owned semantics for D=6, D=8, D=10 anywhere in
  BOOK_01/BOOK_02/BOOK_04 (grep "D=6|D=8|D=10|Q(6)|Q(8)|Q(10)|rung": zero semantic hits; the
  word "rung" does not occur in the books). Q(10)=φ⁶ as a DIMENSION rung is outside the cert
  range.
- |Ω₈|=8 is a group order (Ω₈={A,B,C,D}×{+,−}≅Q₈, BOOK_01:763-802), never linked to ladder
  D=8. The "D=8 vs Ω₈=8" question closes negative: two unrelated 8's.
- The even ladder {φ⁰,φ²,φ⁴,φ⁶} IS owned — as the AF Dirac² eigenvalue ladder with eigenspace
  multiplicities {F₂,F₄,F₆,F₈}={1,3,8,21} partitioning 33 (BOOK_02:1295,
  D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001); its +2 evenness root is the holonomy-parity
  no-sign-catalog argument (BOOK_01:1885-1899). CRITICAL adverse companion: the corpus itself
  proves scene↔AF SPECTRAL transport NO-GO — "too little range to host the AF geometric
  ladder φ²:φ⁴:φ⁶" (binding inequality 20φ>13, BOOK_02:1291); only dimension+grading lift.
- Root-asymmetry connectives confirmed owned: p₊=φ⁻¹/p₋=φ⁻² (BOOK_01:522-526); "The factor 2
  is structural: δ₀ is half of the branch asymmetry, while 2δ₀ is the full one-dimensional
  branch gap" (BOOK_01:669); round-trip/4π double-cycle ([Q₈,Q₈]=Z(Q₈)={±1}, BOOK_01:830;
  BOOK_04:872-876); cascade δ₋ₙ=δ₀^(n+1) (BOOK_01:1122 + cert); Galois-on-values only
  (Iter25 wall, BOOK_04:1383).
- Owned mass-blind per-slot data (the complete inventory found): generation=zone label
  (BOOK_04:912); anomaly hypercharge row Y=(1/6,−2/3,1/3,−1/2,1,0) + T3=±1/2 + Q=T3+Y
  (BOOK_04:1377,1397; 5-field row owned, 6-field has the 2-dim B−L freedom); lepton sheet
  keying 0/4-cycle/3-cycle (BOOK_04:1113,1135,1939); e forced base register (BOOK_04:964-996);
  μ zone-11 localization (BOOK_04:1046); terminal triad (BOOK_04:643-665; ℓ_ν=δ₀/4,
  3(D_e²−1)=δ₀); W,Z edges + H diagonal (BOOK_04:926); H V13 condensation (BOOK_04:1615).
  EVERY one of these per-slot values is RATIONAL — Galois conjugation has nothing mass-blind
  to act on (missing piece M2 below). Sector-level only, not per-slot: D_EW=35 branch depth
  (BOOK_01:1450,1885), CKM/PMNS rank-nullity split (BOOK_04:1242), raw commutant
  M₃(ℂ)⊕ℂ⊕ℂ⊕ℂ (BOOK_04:186).

**Reframe gates (computed; archived script sections E1-E3).**
- G1 concentricity: FAILS. Fitted centers A=(6.32,3.00), B=(7.42,5.28), C=(7.37,−8.07);
  |cB−cC|=13.35 vs r_B=2.56. The three circles are NOT concentric strata around any common
  center; "δ-degree strata" survives only as a SIZE-ratio statement.
- G2 multiplicity transport: FAILS. The owned rung object carries eigenspace multiplicities
  {3,8,21} at {φ²,φ⁴,φ⁶}; occupancies are {|B|,|A|,|C|}={4,5,4}. No owned reading connects
  them (K2-shaped mismatch, this time adverse on its face).
- G3 kernel rung: OPEN-adverse. The owned ladder includes φ⁰ (multiplicity 1); the protocol
  has no unit circle; the γ node sits at the origin as a POINT and is a MEMBER of A (=φ⁴).
- VALUE ECHO (the one thing that holds): raw chart-unit circle-size exponents
  (e_B,e_A,e_C)=(log_φ r)=(1.952, 4.091, 5.895) vs (2,4,6), T_obs=max|dev|=0.105, and
  r₀=r_B/φ²=0.977≈1=Q(4) (the unit sits at the role-budget anchor). E2 LOO: nearest-integer
  rounding stays (2,4,6) in 11/13 folds (breaks: drop-Z → e_B→1.47; drop-H → e_C→5.43 — the
  two shells' isolated members). E3 mass-scramble null (200 draws, seed 20260704): 0/200
  scrambles get sorted exponents within T_obs of (2,4,6); 2/200=1.0% get within T_obs of ANY
  even triple. The even-exponent echo is specific to the real masses+membership at the ~1%
  level, not a generic pipeline artifact — but the prereg S1 embedding cap still applies, and
  the rung↔shell identification is by size order (automatic; zero selective content).
- REFRAME VERDICT: δ-strata do NOT survive as the circle MEANING — no owned rung semantics
  (D=6/8/10 unowned), multiplicities mismatch, centers non-concentric. What survives is a
  cert-adjacent VALUE echo (ratios + unit + evenness). Constraint (a) outcome: the bijection
  joint is not RESOLVED by the reframe; it is DISSOLVED — under the rung reading the owned
  radial object m_rad has nothing to contradict (zones are not circles), at the price of
  losing all zone semantics and inheriting an equally-unowned rung-typing joint.

**Uniform-application audits (constraint (c) — run BEFORE scoring; logged in full).**
- R4-S1 cascade↔generation: DEAD pre-score. The offset is unowned; three equally natural
  readings (cascade exponent −3g; −3(g+1); zone address 9/11/13) give parity patterns
  (odd,even,odd) / (even,odd,even) / (odd,odd,odd), and orientation 2g vs 2(4−g) is free.
  Scored as controls anyway.
- R4-L1 pair placement: the root asymmetry's ONLY two-valued structure is the branch pair;
  doubled degree-pairs give rung-sets {2,4} (direct+return), {4,6} (return+gap), {2,6}
  (direct+gap). The target needs {4,6}; only that one matches b,d (2/2 slots; the others
  0/2). Nothing owned selects → the down-pair seat is a 1-of-3 fitted joint, the SAME SHAPE
  as the killed bijection joint. Any 13/13 rebuild would stand on it.
- R4-S2 charge-branch: AUDIT-CLEAN (|3Q| is single-valued per slot; the Y-reading is
  audit-dead — each quark carries two Weyl hypercharges; the T3-reading leaves bosons
  ill-typed). The only audit-clean uniform root-connected selector found.
- R4-S3 sheet-order: mechanizes skeptic #1's μ-wound — the owned keying uniformly applied
  SEATS μ at rung 4 (=A); the flagship {μ} exclusion is ANTI-derived by the owned material.
- Metric lemma (verified over the whole ceiling class): NO single-valued map slot→rung can
  exceed 11/13 exact — the b,d double-membership is unreachable except through a multi-valued
  mechanism, and the only root-native one is R4-L1 with its unowned 1-of-3 joint.

**Scores (frozen metric; exact nulls: fixed 69,300 + free 5,405,400, both enumerated; skeptic
cross-checks reproduced exactly — free hist 13:1, 12:0, 11:66; fixed-family agreement FLOOR=2,
every member agrees on the {μ,s} exclusion; fixed mean=5.000, free mean=2.846):**

| selector | exact | partial | p_fixed(≥k) | p_free(≥k) | audit |
|---|---|---|---|---|---|
| R4-S1a cascade-gen 2g (bosons ∅) | 1/13 (t) | 1 (b) | 1.0000 | 0.9593 | DEAD (offset trilemma) |
| R4-S1b cascade-gen 2(4−g) | 1/13 (τ) | 1 (d) | 1.0000 | 0.9593 | DEAD (same) |
| R4-S2 charge-branch 2·\|3Q\| | 1/13 (u) | 0 | 1.0000 | 0.9593 | CLEAN — and chance-level |
| R4-S3a sheet-order, odd doubled | 1/13 (s) | 0 | 1.0000 | 0.9593 | seats μ→A (anti-derivation) |
| R4-S3b sheet-order, odd excluded | 1/13 (s) | 0 | 1.0000 | 0.9593 | same wound |
| R4-S4 K1-compliant zones (m_rad) | 2/13 (t,H) | 1 (b) | 1.0000 | 0.8100 | owned-object-obedient control |
| CEILING: affine class over (g,\|3Q\|), 210 distinct assignments, bosons both conventions | max 5/13 | — | 0.6076 | 0.1374 | charged as a class, nothing selected |

Every root-asymmetry selector scores AT or BELOW the structure-null floor (2), and the entire
uniform affine class ceilings at exactly the null MEAN (5) — chance level. The target's
1/5,405,400 specialness is untouched from this direction.

**VERDICT: root-asymmetry material UNDERDETERMINES shell membership.** The clean negative
outcome pre-authorized by the directive: no fit was forced. Named missing owned pieces (what
would have to EXIST in owned text for a rebuild to be possible):
- M1: rung semantics — any THE/REM binding particles/zones/roles to even-ladder rungs or
  dimension-quantum levels D∈{6,8,10} (anchors exist only at D=1, D=4).
- M2: an owned mass-blind per-slot ℚ(φ)\ℚ invariant (all current per-slot mass-blind data is
  rational, so Galois-on-values is empty here).
- M3: an owned generation↔cascade-level binding with a FIXED offset (kills the R4-S1
  trilemma).
- M4: a single owned principle covering bosons AND fermions (W/Z/H/γ texts are separate REMs;
  any joint use is compositional = forbidden under (c)).
- M5: an owned multi-valued placement mechanism — which rung-PAIR a degenerate pair occupies
  (resolves R4-L1's 1-of-3 joint; without it 13/13 is unreachable, by the metric lemma).
- M6 (reframe-specific): an owned account of occupancies {4,5,4} vs the owned rung
  multiplicities {3,8,21}, and of the empty φ⁰ rung.

**Forward falsifiers computable under the frozen protocol (constraint (d), replacing the
killed ν-falsifier):** (i) E2 — any protocol refit (new PDG mcd, LOO fold) that rounds the
size-exponent triple away from (2,4,6) kills the value echo; current margin T_obs=0.105,
fragile folds Z and H named. (ii) E3 — the echo's scramble null is 0-2/200; a re-run under a
fresh seed or larger draw count moving this to chance kills it. Both run inside
shell_rule_r_attempt4.py with no new data types.

**What an external skeptic should attack:** (1) E3's statistic T was chosen after seeing
e_obs — the fairer "any even triple" control is 2/200=1%, not 0; (2) LOO 11/13 leans on the
two fragile folds being exactly the isolated members Z,H; (3) the affine-ceiling grid bounds
are mine (though the ≤11 single-valued lemma caps every function-valued class regardless);
(4) R4-S2's audit-clean status (|3Q| vs Y-numerator readings); (5) completeness of the
owned-material inventory — the underdetermination claim is only as strong as the sweep.

## M2 cross-link — phase-labeling campaign result (2026-07-05; append-only)

The named missing piece M2 ("an owned mass-blind per-slot ℚ(φ)\ℚ invariant") was attacked head-on
by the M2-FORGING campaign: can a canonical within-zone labeling of K(9,11,13) be forced from
owned structure and supply the per-slot invariant? Full result: `M2_PHASE_LABELING_MEMO.md` +
`m2_phase_labeling_check.py` (46/46 PASS; DRAFT, pre-skeptic). Verdict for THIS ledger:

- **M2 stays OPEN — and is now bounded on a new side.** The owned within-zone structure exists
  ONLY on zone 9 and forces a Q₈ ⊔ {ω₀}-typed labeling up to G_res ∈ {1, V₄, (ℤ/2)³}
  (reading-dependent, one torsor-orbit each). Its label values are RATIONAL in every reading
  (Q₈ characters are ±1-valued; exponent 4): the ℚ(φ)\ℚ requirement is NOT suppliable by any
  canonical within-zone labeling. A canonical CYCLIC/μ₉ phase labeling (which would carry
  ℚ(ζ₉) irrationals) is IMPOSSIBLE from owned data — type wall (Q₈ has no order-8 element),
  relation wall (typed partition + G₈-averaged emission, no owned successor order), invariance
  wall (under R-mid/R-weak no bijective phase labeling is G_res-statable); freedom quantified:
  ≥ 5040 unselectable cyclic-order classes vs exactly 1 class for the Q₈-typed labeling.
- **Per-slot use is doubly blocked:** values rational (Galois empty, as attempt-4 found) AND the
  vertex↔slot bridge is not torsor-invariant (computed) while C1 (BOOK_01:1570) forbids owning it.
  Any future rule-R attempt that assumes per-vertex zone-9 phases (μ₉-style) now has a named
  impossibility to overcome first; attempts using the CANONICAL system (basepoint indicator,
  χ_B/χ_C/χ_D characters, E-block projectors, the 1+1+3+4 refinement of std₉) are the only
  labeling-native raw material — all of it rational and class-canonical.
- Zones 11/13: nothing owned per-vertex (capacity ladder is count-grade; E₄-extension-invisibility
  + T2′-v2 kill block extension keys) — consistent with this ledger's existing constraint set.

### M2 cross-link addendum — skeptic #1 verdict (2026-07-05, accepted in full, no defense)

VERDICT: **SURVIVES** — torsor forcing, cyclic impossibility (all three walls), 1+1+3+4 module,
zone-11/13 emptiness and the consumer split all upheld; skeptic's independent transitivity
reimplementation closed the count-only gap; tick fingerprint re-verified in exact Fractions
(80/81 all four carriers; ratio −1/9; delay 8/9; ω₀-bit +1/9 & 10/9). His own dyad attack on the
zone-11/13 emptiness DIED — X3 strengthened (extension-key route re-fails as T2′-v2 predicted).
TWO WOUNDS + script repairs, all applied (M2_PHASE_LABELING_MEMO.md v2, repair log inside;
script now 50/50 PASS): W1 pre-ownership — the E₀/E₃/E₄ system was already CORE-FORMALIZED
(D0-Q8-TERMINAL-FOURIER-001, Q8Terminal.lean:24-79, ranks (1,4,3)); preflight missed the row
(error of record); novelty narrowed to {ℂω₀ pointed-shell extension, std₉ refinement 1⊕3⊕4,
reading-independence packaging, carrier application}. W2 framing + false grep sentence — the
owned object is a labeling of the DETECTOR-LAYER pointed shell V₉ = Ω₈ ⊔ {ω₀}, not of K(9,11,13)
graph slots; and ALPHA_SEAM_NOGO_V2.md does contain μ-symbols (seam moments μ₁/μ₂/μ₃, 7 lines) —
"zero μ occurrences" was false as written (errors of record; both sentences corrected — the
substantive no-μ₉-minting point survives). W3 script — self-testing control replaced by an
independent 8!-sweep deriving G_res orders (8,4,1) from the owned relations; free-action argument
exercised; Fraction-exact fingerprints. A1 STRENGTHENED (adopted with credit): BOOK_01:618 ("the
torus is abelian, so order is not encoded ⇒ defect") + the T2′ v1 kill are ACTIVE anti-order
texts, not mere absence — the bar for any owned-traversal-order attack is higher than the memo
v1 stated.
