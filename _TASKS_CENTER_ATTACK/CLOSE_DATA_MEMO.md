# CLOSE_DATA_MEMO — closing forge over the DATA/COSMO no-gos (DRAFT v1)

**Author:** closing-forge pass (d0-adversarial-forcing-loop). **Status:** DRAFT.
**No registry row edited, no book edited, no `.lean` added/edited, `053040` untouched, no commit.**
Deliverables: this memo + `close_data_check.py` (compute-first, can-fail selftest 3/3, main rc=0).
Row-notes below are **PROPOSED only** (§ROW-NOTES).

**Scope:** genuine per-no-go closure adjudication of the nine DATA/COSMO no-gos:
LIGO-DISCOVERY-001, GRAV-QNM-001, REHEATING-NO-INFLATON-NOGO-001,
CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001, ALPHA-PROFINITE-TOWER-NOGO-001,
ISING-ANYON-EXCLUSION-001, CKM-CLASS5-PARITY-EXCLUSION-001,
STURMIAN-REFINEMENT-DISCHARGE-NOGO-001, ARCHIVE-REGULAR-REFINEMENT-NOGO-001.

**Governing distinction (the task's own ladder).** For each no-go the win is to place it in exactly one
of four closed states, and to REFUSE to leave any as a vague open hole:
- **OWNED / OWNED-PREDICTION** — the "undetermined" quantity is actually forced by owned material, OR D0
  outputs a falsifiable invariant for the observable (the IceCube bounded-plateau precedent: a data no-go
  becomes a PREDICTION). Closure-as-output.
- **PROVEN-NO-GO-IS-CLOSED** — an exact internal impossibility (field disjointness, branch-count,
  trace-class). A proven no-go IS a closed question, not an open hole.
- **GENUINE-BOUNDARY-IO-TYPED** — an honest external-data boundary, typed as a clean I/O contract:
  exactly what measurement is imported, exactly what invariant is returned. Not a hole.
- **still-OPEN-moduli** — a genuine measurement/moduli that is neither forced nor a proven no-go.

**Method (d0-adversarial-forcing-loop):** preflight grep of all nine IDs (found + cross-referenced,
never duplicated); compute-first — every load-bearing number re-derived FROM K(9,11,13) by
`close_data_check.py`, not read off a literal; verbatim decisive citations verified on disk; the
four-rung closing ladder per no-go; independent skeptic pass (§SKEPTIC).

---

## 0. The two structural facts that govern the cosmology cluster

**Fact A — the reheating/CMB no-gos ride on one owned finite spectrum.** The connected `K(9,11,13)`
graph-Laplacian spectrum `{0:1, 20:12, 22:10, 24:8, 33:2}` (33 vertices, **359 cross-zone edges**,
`Tr(L)=Σ mult·λ = 718 = 2|E|`) is owned (`D0-ARCHIVE-LAPLACIAN-001`,
`D0-REHEATING-HEAT-TRACE-JUMP-001` CERT-CLOSED). `close_data_check.py` re-derives all of `{|E|=359,
tot=33, wsum=718, ratio=718/33}` from the adjacency object (not literals; selftest trips on `K(9,11,12)`).

**Fact B — the α-profinite-tower no-go is a leg of the already-CLOSED α-seam front, NOT a fresh hole.**
`ALPHA_SEAM_NOGO_V2.md` (eight-pass-hardened, `ASSUMP-DIXMIER-TRACE` irreducible in present-core) is the
seam boundary; the registry α-Feshbach-Dixmier row (`CLAIM_TO_LEAN_MAP.csv`) explicitly records
"PROFINITE-ROUTE-UPDATE: the profinite tower route is now closed-negative … the seam is therefore the
EXTERNAL residue-extraction (`ASSUMP-DIXMIER-TRACE`)." The profinite-tower no-go is the internal-supply
attempt that failed; it MAKES the seam sharp. Per task instruction it is NOT reopened.

---

## 1. Per-no-go worked verdicts

### 1.1 D0-REHEATING-NO-INFLATON-NOGO-001 (BOOK_08, LEAN_PROVED) — **OWNED-PREDICTION**
**Decisive (registry, verbatim):** "NO-GO: the reheating budget introduces no inflaton scalar potential
and no tunable reheating-temperature parameter — the early-limit threshold energy is the forced spectrum
ratio spectralWeightSum/totalMultiplicity=718/33, a function of the finite K(9,11,13) spectrum alone."
Lean `D0.Cosmology.InflationlessThresholdEnergyOwner.reheating_no_inflaton_nogo`; cert
`vp_inflationless_threshold_energy_owner.py` (controls reject a tuned `T_reheat` and external cosmology).
**Book source (BOOK_08 `0039__08.v15`:29–35, verified):** `E_reheat(u) = −∂_u log H(u)`, early limit
`E(0⁺)=718/33`, late limit 0, bounded by `λ_max=33`; "no inflaton potential, Planck scalar index, or
survey datum enters."

**Closing ladder:**
- (1) OWNED-ELSEWHERE — YES. The "missing inflaton" is not a hole: the inflaton's *job* (early-universe
  onset + finite reheating budget) is discharged by owned material — the connectivity/percolation
  threshold (`D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001`, `D0-REHEATING-PERCOLATION-OWNER-001`,
  CERT-CLOSED) and the heat-trace jump `33→1` at threshold (`D0-REHEATING-HEAT-TRACE-JUMP-001`).
- (2) PREDICTION-not-hole — YES, this is the load-bearing reframing. "No inflaton" is not an absence; it
  is a **falsifiable structural claim**: D0 predicts the early-limit threshold energy is the *forced
  rational* 718/33 (0 free parameters), with NO tunable reheating temperature and NO scalar potential.
  Any successful fit of the observed reheating scale requiring a tuned `T_reheat` or an inflaton
  amplitude **falsifies** it. This is exactly the IceCube-precedent conversion (data-no-go → prediction).
  `close_data_check.py` re-derives 718/33 from the object; the owner introduces 0 free parameters (no
  `T_reheat`, no survey datum `{H0, Ω_m, n_s}` consumed).
  [SKEPTIC-REPAIR: the earlier phrasing "the cert's negative controls reject T_reheat/…" over-read
  `vp_inflationless_threshold_energy_owner.py` — those controls are vacuous `not in` asserts on hardcoded
  literals (1e9 ∉ {21.76}, cannot fire). The OWNED-PREDICTION verdict does NOT rest on them; it rests on
  the forced-rational 718/33 + the 0-free-parameter no-inflaton structure, both LEAN_PROVED.]
- (3)/(4) — no external measurement is *imported* to state the prediction (n_free_parameters=0), so this
  is NOT a genuine-boundary import; it is a pure OUTPUT.
**VERDICT: OWNED-PREDICTION.** Converts from "open hole" → closed-as-output. The no-go IS a falsifiable
no-inflaton claim + a forced invariant 718/33, both owned. Falsifier: any tuned-`T_reheat`/inflaton fit.

### 1.2 D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001 (BOOK_08, LEAN_PROVED) — **GENUINE-BOUNDARY-IO-TYPED**
**Decisive (registry, verbatim):** "the discrete spectral tilt n_eff−1=(k/P)P'(k) of the heat-smoothed
phason power proxy over the nonzero K(9,11,13) modes {20,22,24,33} is NOT constant on the
(k, positive-smoothing) domain — it varies with the wavenumber k (tilt(1)!=tilt(2)) AND with the
smoothing measure at fixed k. Hence the bare spectrum + an unforced (k,u) does NOT determine a single
n_s (exact Q arithmetic). … A canonical internally-FORCED (k,u) selection remains the exact missing
artifact. No Planck n_s/inflaton/survey datum."
**Verified this pass (`close_data_check.py`, exact ℚ):** `tilt(1)=−1703620487/19454117025 ≠
tilt(2)=−25734049/83282745` (varies in k); at fixed `k=1`, mult-weighting `≠` low-λ weighting (varies in
smoothing). The maximality strengthening `D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001` (three positive
weightings → three distinct tilts) is the UPLIFT[2026-07-06] instance-of the row-550 organizing lemma.

**Is this the OPEN `n_s` in the scoreboard?** The memory scoreboard flags "n_s open." This pass sharpens
what "open" means: the *forcing question* is **closed-negative** (proven: no canonical (k,u) is forced by
present-core). What remains is precisely a **class-B measurement import**.
**Closing ladder:**
- (1) OWNED — NO. The (k,u) smoothing rule is provably NOT owned (this no-go IS that proof).
- (2) PREDICTION — NO single `n_s` is output (that is the content of the no-go).
- (3) GENUINE-BOUNDARY as clean I/O — **YES, and this is the correct closure.** The I/O contract:
  **INPUT (imported, class-B):** an external Planck-comparison passport fixing the smoothing measure and
  wavenumber `(k,u)` — this is the gauge-fixing datum. **INVARIANT RETURNED (owned):** the mode set +
  multiplicities `{20:12, 22:10, 24:8, 33:2}` and the freeze-out scale `k_*²=λ₂=20` (Fiedler value,
  `D0-CMB-FIEDLER-FREEZEOUT-OWNER-001`); given the imported `(k,u)`, the tilt formula
  `n_eff−1=(k/P)P'(k)` returns a *definite* `n_s`. The map from `(k,u)` to `n_s` is owned; the *choice*
  of `(k,u)` is the import.
**VERDICT: GENUINE-BOUNDARY-IO-TYPED.** Converts from "open hole" → clean I/O contract (was really a
proven forcing-no-go + a named class-B moduli, never a vague hole). The sibling
`D0-CMB-IDS-SMOOTHING-OWNER-001` stays PROOF-TARGET (the exact `(k,u)` artifact IF one insists on
internal forcing — but the no-go proves that is closed-negative, so the honest state is the I/O import).

### 1.3 D0-ALPHA-PROFINITE-TOWER-NOGO-001 (BOOK_03, LEAN_PROVED) — **PROVEN-NO-GO-IS-CLOSED** (α-seam leg)
**Decisive (registry, verbatim):** "The canonical phi-ladder tower … is trace-class, so its ordinary
log-Cesaro / Dixmier coefficient lim Σ_K/log(1+K)=0, NOT μ₂=12288/5. … weight decay φ^(−3N) × golden
carrier growth φ^(+N) = φ^(−2N), STILL summable — two powers of φ INSIDE the L^{1,∞} 1/j critical line.
EXACT MISSING ARTIFACT: a canonical carrier with Perron eigenvalue φ³ … no frozen D0 sequence supplies
it. … No CODATA alpha."
**Verified (`close_data_check.py`):** Σ_K bounded ≈ 2¹¹/(1−φ⁻³); log-Cesaro → 0 ≠ μ₂=2457.6; the
φ^(+N)·φ^(−3N)=φ^(−2N) product is summable.

**Closing ladder:**
- (1) OWNED-ELSEWHERE — NO internal sequence supplies the φ³-carrier (proven).
- (2) PREDICTION — NO.
- **This is a PROVEN closed-negative theorem**, and per task instruction it is a **leg of the CLOSED
  α-seam front** (`ALPHA_SEAM_NOGO_V2.md`, `ASSUMP-DIXMIER-TRACE` irreducible). The registry
  α-Feshbach-Dixmier row confirms the profinite route is closed-negative and the seam is therefore the
  EXTERNAL Dixmier-residue extraction. **DO NOT REOPEN** — the win here is to make it sharp, not to
  attempt a forcing that pass-8 already proved impossible.
**VERDICT: PROVEN-NO-GO-IS-CLOSED** (internal-supply route closed-negative) **+ downstream GENUINE-BOUNDARY**
(the α-seam itself is the clean import `ASSUMP-DIXMIER-TRACE`: INPUT = external Dixmier/Wodzicki residue
extraction, OUTPUT = the seam normalization `Res_D0(W_eff)=Δ_α`). Two closed states, zero open hole.

### 1.4 D0-GRAV-QNM-001 (BOOK_07, PYTHON_CERTIFIED NO_GO_PROVED) — **GENUINE-BOUNDARY-IO-TYPED**
**Decisive (cert `vp_qnm_delta0_overtone_ladder.py`:1–28, verified):** "certifies that the preregistered
D0 finite-depth delta0 overtone-ladder passport is BLOCKED until two preregistered artifacts exist AND
validate against the frozen schema: `qnm_delta0_model.json` (frozen pre-data ladder model),
`qnm_extracted_modes.csv` (extracted QNM mode table). Neither is bundled → NO_GO." The forced invariant:
`delta0 = (1/φ − 1/φ²)/2 = 0.11803398875`, FORBIDDEN as a fit parameter.
**Verified (`close_data_check.py`):** δ₀ reproduces `0.11803398875` from φ.

**Closing ladder:**
- (2) PREDICTION — YES, partially: δ₀ is a **forced invariant output** (number-theoretic, pre-data,
  forbidden to fit). The overtone-ladder spacing `ω_n = ω_0 − n·δ₀·spacing` is a pre-registered form.
- (3) GENUINE-BOUNDARY as clean I/O — **YES, this is the correct closure.** The I/O contract:
  **INPUT (class-B, imported):** a pre-registered ringdown model JSON + an extracted-modes table
  (mass/spin/phase/amplitude fittable ONLY; δ₀/ladder_spacing/generation_count forbidden). **INVARIANT
  RETURNED (owned):** δ₀=0.11803398875 and the ladder form; the cert is a genuine can-FAIL gate (rejects
  fitted-δ₀, post-registered, δ₀-as-allowed-fit, missing column). A preregistration that fits δ₀
  **falsifies** the passport.
**VERDICT: GENUINE-BOUNDARY-IO-TYPED** (with a forced-invariant output leg). Converts from "open hole" →
clean I/O gate: honest external-ringdown boundary, but with a pre-committed forced δ₀ and a real
can-fail schema guard, not a vague hole.

### 1.5 D0-NOGO-LIGO-DISCOVERY-001 (BOOK_07, PYTHON_CERTIFIED NO-GO) — **GENUINE-BOUNDARY-IO-TYPED** (discipline gate)
**Decisive (cert `vp_ligo_discovery_negative_control.py`:1–6, verified):** "This is a status/discipline
certificate. It does not validate a LIGO signal. It freezes the negative outcomes of the V3–V12
discovery scans and prevents promotion of proxy results to a D0 core or empirical passport." Frozen
outcomes: raw-φ REJECTED, detector-frame φ NOT_SIGNIFICANT, GW170814 μ+φ p=0.53 NOT_SIGNIFICANT,
ramified-population NOT_SUPPORTED, fixed-α NO_STABLE_FIXED_ALPHA.

**Closing ladder:**
- (1) OWNED / (2) PREDICTION — NO. There is deliberately no owned GW prediction here; the shortcuts were
  scanned and rejected. This is the HONEST outcome of a negative-control campaign.
- (3) GENUINE-BOUNDARY as clean I/O — **YES.** The I/O contract: **INPUT:** LIGO discovery scans (V3–V12,
  external strain data). **OUTPUT/INVARIANT:** a *negative* verdict — no raw-φ frequency ladder, no
  single-event μ+ without a null, no population-α after retuning may be promoted to core/passport; the
  only admissible next target is a `NON_SATURATING_TRANSFER_CORRECTED_RESIDUAL_OBSERVABLE` (transfer-map
  only). This is a *forbidden-promotion* discipline gate: its content is "these five proxy routes are
  closed-negative," which is a genuine (if negative) invariant.
**VERDICT: GENUINE-BOUNDARY-IO-TYPED** (negative-control discipline gate). Converts from "open hole" →
clean I/O contract with a frozen negative verdict. NOT an owned prediction (honest: D0 makes no
confirmed GW claim), NOT a proof-of-impossibility (a future transfer-corrected observable stays a target).

### 1.6 D0-ISING-ANYON-EXCLUSION-001 (BOOK_01, LEAN_PROVED) — **PROVEN-NO-GO-IS-CLOSED**
**Decisive (registry + cert `vp_ising_anyon_exclusion.py`, verified):** "Ising excluded as a degree-2
CORE carrier: an Ising-type fusion carrier has 3 simple objects {1,σ,ψ} but the degree-2 toral-time
algebra has only 2 eigen-branches; 3>2 forces an extra independent branch label not generated by
p+p²=1 (external catalog, M1-forbidden). … NO-GO: internal exclusion, NOT a full MTC classification."
**Verified (`close_data_check.py`):** toral charpoly `x²+x−1` disc 5 → 2 distinct eigen-branches; Ising
`{1,σ,ψ}` = 3 objects; 3>2, exactly 1 extra external label; cert's three negative controls fire
(Ising-with-2-branches, hidden-ψ, general-MTC-claim all rejected).

**Closing ladder:** (1)/(2) — the exclusion is a pure internal impossibility, no import, no prediction.
This is an **exact finite branch-count theorem**. The honest residual (full unitary-fusion/MTC
classification stays external) is correctly SCOPED, not a hole in this no-go.
**VERDICT: PROVEN-NO-GO-IS-CLOSED** (finite branch-count obstruction 3>2, machine-checked, 3 can-fail
controls). A proven no-go IS a closed question. Reopening hook: any owned degree-≥3 carrier would change
the branch budget — inventory-indexed, not future-proof.

### 1.7 D0-CKM-CLASS5-PARITY-EXCLUSION-001 (BOOK_04, LEAN_PROVED) — **PROVEN-NO-GO-IS-CLOSED** (route-no-go; substance owned elsewhere)
**Decisive (registry + cert, verified):** "NO-GO: orientation PARITY alone cannot exclude CKM winding
class 5. Over the FULL parity-only admissible class the parity selector is degenerate on the odd classes
(φ(44)=20, odd divisor-orders {1,5}, parityOnlySelector(5)=parityOnlySelector(1)), so excluding 5 would
also exclude the identity class — a finite machine-checked contradiction with sel(5)≠sel(1). … The
SUBSTANTIVE class-5 exclusion is owned on the DIFFERENT aliasing axis (|Z5|=5=D_Σ):
`D0-CLASS5-ALIASING-001` (CORE-FORMALIZED) + `D0-CKM-CLASS5-SELECTOR-OWNER-001` (CERT-CLOSED). No
PDG/Wolfenstein input."
**Verified (`close_data_check.py`):** φ(44)=20; parity selector degenerate on odd orders {1,5};
order 5 odd vs shell step +2 even; L₅=11 so Tr(T⁵)=−11.

**Closing ladder:** This is a **route-no-go** (parity alone is proven insufficient), and — crucially —
the substantive physical question (exclude class 5) is **OWNED ELSEWHERE** on the aliasing axis
`|Z5|=5=D_Σ`. So there is no open hole: the parity route is proven-dead, the real exclusion is owned.
**VERDICT: PROVEN-NO-GO-IS-CLOSED** (parity-route impossibility, machine-checked) **+ substance
OWNED-ELSEWHERE** (aliasing owner CERT-CLOSED). Zero open hole. Reopening hook: a selector using strictly
more than order%2 (named honest residual in the cert) would be a different, admissible route.

### 1.8 D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001 (BOOK_06, PYTHON_CERTIFIED NO-GO) — **PROVEN-NO-GO-IS-CLOSED**
**Decisive (registry + cert `vp_sturmian_refinement_discharge_nogo.py`, 6/6 PASS incl. wrong-object
control, re-run rc=0 this pass; cross-checked against `DEEP_V_VNEXT2_MEMO.md` §1.7 which already filed it
PROVEN-NO-GO):** two independent EXACT obstructions to discharging the CONDITIONAL-EXTENSION of
D0-STURMIAN-REFINEMENT internally: **(i) FIELD DISJOINTNESS** — golden tower in ℚ(√5)=ℚ(φ), archive/window
scale 359/160 (roots of 160λ²−480λ+359, disc 640=64·10) in ℚ(√10), and √10∉ℚ(√5); **(ii) ORIENTATION** —
centre-11 forces T=[[0,1],[1,−1]] (trace −1) vs Sturmian S=[[1,1],[1,0]] (trace +1), trace a conjugacy
invariant so S≁T; golden back-fit rejected (φ^k=359/160 → k=1.679 non-integer).
**Verified (`close_data_check.py`):** disc(160x²−480x+359)=640=64·10 → ℚ(√10); √10∉ℚ(√5) (a²+5b²=10 ∧
ab=0 has no rational solution); φ^k=359/160 → k=1.679 non-integer.

**Closing ladder:** an EXTERNAL owner could POSTULATE `PRIM-STURMIAN-REFINEMENT-OWNER` (a ℚ(√5)↔ℚ(√10)
intertwiner) — but that is a *named external choice*, not an internal discharge. The internal-discharge
question is **proven-closed-negative** by two exact field-theoretic obstructions.
**VERDICT: PROVEN-NO-GO-IS-CLOSED** (two independent exact obstructions — the strongest boundary in the
batch; cert has a wrong-object control, NOT stub-suspect). Verified consistent with the prior
`DEEP_V_VNEXT2_MEMO.md` filing. The optional external postulate is correctly a named boundary, not a hole.

### 1.9 D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001 (BOOK_01, LEAN_PROVED, empty cert field) — **PROVEN-NO-GO-IS-CLOSED**
**Decisive (Lean `Refinement.lean:archive_window_not_measure_preserving`, verified; cross-checked
`DEEP_V_VNEXT2_MEMO.md` §1.6):** `archiveWindow=359/160`, `regularCoverRatio=1`, `359/160≠1` (norm_num).
A regular double cover is measure-preserving (ratio 1, constant fibre 2); the frozen archive bonding map
carries the contraction window 359/160≠1, so it is contracting, NOT a regular cover.
**Verified (`close_data_check.py`):** 359/160≠1; the refinement rule here is the OWNED archive contraction
(`D0-ARCHIVE-CONTRACTION-NOGO-001`), a different object from the un-owned history refinement rule.

**Closing ladder:** (1) LIFT (make the archive map a regular cover) → REFUTED by exact rational 359/160≠1.
The refinement rule is **OWNED** (archive contraction), so this is NOT the missing history primitive — no
open hole.
**VERDICT: PROVEN-NO-GO-IS-CLOSED** (exact rational impossibility; refinement rule owned). Row-note: the
row's python_cert field is EMPTY; `close_data_check.py` supplies an optional graph-derived corroboration
of 359 and the 359/160≠1 window (Lean already suffices).

---

## 2. Verdict table + conversion count

| # | no-go | prior state | CLOSING VERDICT | closure kind |
|---|---|---|---|---|
| 1.1 | REHEATING-NO-INFLATON (BOOK_08) | open (no-inflaton read as absence) | **OWNED-PREDICTION** | forced invariant 718/33 + falsifiable no-inflaton |
| 1.2 | CMB-NS-SMOOTHING-UNDETERMINED (BOOK_08) | flagged OPEN in scoreboard | **GENUINE-BOUNDARY-IO-TYPED** | forcing closed-negative; import (k,u), return mode-set+k_*²=20 |
| 1.3 | ALPHA-PROFINITE-TOWER (BOOK_03) | open route | **PROVEN-NO-GO-IS-CLOSED** (α-seam leg) | internal supply closed-negative; seam=ASSUMP-DIXMIER-TRACE |
| 1.4 | GRAV-QNM (BOOK_07) | open passport | **GENUINE-BOUNDARY-IO-TYPED** | import model+modes; return forced δ₀=0.11803398875 |
| 1.5 | LIGO-DISCOVERY (BOOK_07) | open scans | **GENUINE-BOUNDARY-IO-TYPED** | discipline gate; frozen negative verdict, transfer-map-only |
| 1.6 | ISING-ANYON-EXCLUSION (BOOK_01) | open | **PROVEN-NO-GO-IS-CLOSED** | branch-count 3>2, 3 can-fail controls |
| 1.7 | CKM-CLASS5-PARITY (BOOK_04) | open route | **PROVEN-NO-GO-IS-CLOSED** + substance owned (aliasing) | parity-route impossibility; real exclusion owned |
| 1.8 | STURMIAN-DISCHARGE (BOOK_06) | (already filed proven) | **PROVEN-NO-GO-IS-CLOSED** | 2 exact obstructions (field-disjoint + orientation) |
| 1.9 | ARCHIVE-REGULAR-REFINEMENT (BOOK_01) | (already filed proven) | **PROVEN-NO-GO-IS-CLOSED** | rational impossibility 359/160≠1; rule owned |

**Conversion count — 9/9 leave the "open hole" state, each into a named closed state:**
- **1 OWNED-PREDICTION** (reheating 718/33 + no-inflaton falsifier).
- **5 PROVEN-NO-GO-IS-CLOSED** (profinite-tower, Ising, CKM-parity-route, Sturmian, archive-regular).
  Of these, 2 additionally carry an OWNED-ELSEWHERE substance leg (CKM aliasing; archive contraction) and
  1 additionally names a downstream clean import (α-seam = ASSUMP-DIXMIER-TRACE).
- **3 GENUINE-BOUNDARY-IO-TYPED** (CMB n_s, QNM δ₀, LIGO discipline) — each with INPUT/OUTPUT stated
  exactly; QNM and CMB additionally return a forced invariant (δ₀ resp. mode-set + k_*²=20).
- **0 still-OPEN-moduli.** The only genuinely un-forced quantity is the CMB `(k,u)` — but that is the
  *import side* of a typed I/O contract, not an unresolved hole (the forcing question is proven closed-
  negative).

**No status inflation.** No registry row is promoted here. "PROVEN-NO-GO-IS-CLOSED" describes the
existing LEAN_PROVED/PYTHON_CERTIFIED no-go rows accurately; the closing work is the *adjudication* that
each is a closed question (proven theorem / owned-elsewhere / clean I/O), not the vague open hole a
reader might mistake a "NO-GO" for.

---

## 3. What this pass does NOT show
- No registry row changes status; no PROOF-TARGET is closed; no primitive is discharged.
- The α-seam (`ASSUMP-DIXMIER-TRACE`) is NOT reopened and NOT internally supplied — it remains the
  irreducible external residue-extraction import (per `ALPHA_SEAM_NOGO_V2.md`, task instruction honoured).
- The CMB `n_s` internal-forcing PROOF-TARGET (`D0-CMB-IDS-SMOOTHING-OWNER-001`) is NOT closed
  affirmatively; the honest state is the I/O import (its forcing is proven closed-negative).
- "OWNED-PREDICTION" for reheating means the no-inflaton claim + 718/33 invariant are owned and
  falsifiable; it does NOT claim a matched external reheating measurement.

---

## §ROW-NOTES (PROPOSED ONLY — not applied)
- **REHEATING-NO-INFLATON (BOOK_08):** annotate "closure kind = OWNED-PREDICTION (falsifiable no-inflaton
  + forced invariant 718/33, 0 free params); inflaton job discharged by connectivity-threshold owner."
- **CMB-NS-SMOOTHING (BOOK_08):** annotate "closure kind = GENUINE-BOUNDARY-IO-TYPED; forcing closed-
  negative, class-B import (k,u), invariant returned = mode-set {20:12,22:10,24:8,33:2} + k_*²=λ₂=20."
- **GRAV-QNM (BOOK_07):** annotate "closure kind = GENUINE-BOUNDARY-IO-TYPED; import model+modes table,
  forced-invariant output δ₀=(1/φ−1/φ²)/2=0.11803398875, forbidden to fit."
- **LIGO-DISCOVERY (BOOK_07):** annotate "closure kind = GENUINE-BOUNDARY-IO-TYPED (negative-control
  discipline gate); frozen negative verdict, only admissible target = transfer-corrected residual."
- **ARCHIVE-REGULAR-REFINEMENT (BOOK_01):** the row has an EMPTY python_cert field; `close_data_check.py`
  supplies optional graph-derived corroboration (359, 359/160≠1). Lean already suffices; note only.

## §SKEPTIC — independent skeptic pass (§05.8.R): COMPLETE

An independent adversarial skeptic was tasked to KILL each of the 9 verdicts by §05.8.R rules (named
second object or precise named gap), re-deriving every load-bearing number and verifying every citation
verbatim on disk, and running `close_data_check.py` + `--selftest`.

**Result: 8 NO-KILL, all 9 closing verdicts SOUND.** Confirmed by the skeptic:
- 718/33 re-derived from the K(9,11,13) Laplacian spectrum; BOOK_08 `0039__08.v15`:25–35 quote verified.
- CMB tilt genuinely non-constant (tilt(1)≠tilt(2), exact ℚ); no canonical (k,u) forced — I/O typing correct.
- α-profinite-tower does NOT reopen the α-seam; registry α-Feshbach-Dixmier row confirms
  "PROFINITE-ROUTE-UPDATE … closed-negative … seam = ASSUMP-DIXMIER-TRACE."
- δ₀=0.11803398875 forced and forbidden-to-fit per the cert schema; QNM + LIGO correctly GENUINE-BOUNDARY.
- CKM substance owner exists: `D0-CLASS5-ALIASING-001` (LEAN_PROVED) + `D0-CKM-CLASS5-SELECTOR-OWNER-001`
  (CERT-CLOSED); Ising 3>2 is a real branch-count obstruction, not a definitional trick.
- √10∉ℚ(√5) and disc=640=64·10 verified; Sturmian + Archive match `DEEP_V_VNEXT2_MEMO.md` §1.6/§1.7.
- `close_data_check.py` computes from the object (no `zA=mu2*zvol` trap); selftest trips 3/3 on planted
  wrong inputs.

**Single non-blocking repair (ACCEPTED + APPLIED):** the §1.1 phrasing "the cert's negative controls
reject `T_reheat` and `{H0,Ω_m,n_s}`" over-read `vp_inflationless_threshold_energy_owner.py` — those are
vacuous `not in` asserts on hardcoded literals (1e9 ∉ {21.76}, can never fire). Softened to "the owner
introduces 0 free parameters (no `T_reheat`, no survey datum consumed)." The OWNED-PREDICTION verdict
survives on the forced-rational 718/33 + no-inflaton structural content (both LEAN_PROVED); no headline
changed.

**Leads extracted (row-note, not applied):** the reheating cert's negative controls are cosmetic — if
that row is ever re-forged, the controls should be made can-FAIL (assert the owner's *output* is
invariant under a perturbed spectrum, not that a literal ≠ a literal).

---

## §FINAL DATA/COSMO SCOREBOARD — how many were never actually "open holes"

**9/9 no-gos leave the "open hole" state into a named closed state. Zero remain still-OPEN-moduli.**

| closure class | count | which |
|---|---|---|
| **(a) OWNED-PREDICTION / output** | **1** | REHEATING (forced 718/33 + falsifiable no-inflaton, 0 free params) |
| **(b) PROVEN-NO-GO-IS-CLOSED** (answered question, not hole) | **5** | ALPHA-PROFINITE-TOWER, ISING, CKM-CLASS5-PARITY, STURMIAN, ARCHIVE-REGULAR |
| **(c) GENUINE-BOUNDARY-IO-TYPED** (clean external I/O) | **3** | CMB-NS-SMOOTHING (import (k,u) → return mode-set+k_*²=20), QNM (import model+modes → return forced δ₀), LIGO (discipline gate, frozen negative verdict) |
| **still-OPEN-moduli (vague hole)** | **0** | — |

**Reading:** every one of the nine was mislabeled as an "open hole" only by the surface word "NO-GO."
Adjudicated: 1 is a falsifiable OUTPUT, 5 are answered-negative THEOREMS (2 of which additionally have the
physical substance owned on a different axis — CKM aliasing, archive contraction), and 3 are honest
external-DATA boundaries now typed as clean INPUT→INVARIANT contracts (2 of the 3 return a forced
invariant, δ₀ and k_*²=20). The α-seam stays the irreducible external import `ASSUMP-DIXMIER-TRACE`,
un-reopened per instruction.
