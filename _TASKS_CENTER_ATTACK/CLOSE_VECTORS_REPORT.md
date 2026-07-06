# CLOSE VECTORS REPORT — D0 vector-closure campaign consolidation

**Date:** 2026-07-05. **Scope:** consolidate the vector-closure campaign items after the
forge → independent-skeptic → repair loop. **Registry motion:** none applied — all registry
actions below are PROPOSALS. No `CLAIM_TO_LEAN_MAP.csv` row, no `LEAN_ASSUMPTION_LEDGER` row,
no `.lean`, no book file, no `053040` row was touched.

Verification basis: memo + repaired script re-read/re-run on disk 2026-07-05
(`m1qm_departure_scale_check.py` → all gates PASS, exit 0; parent `M1_QM_GAP1_MEMO.md:304-312`
Block-D adjudication confirmed verbatim).

---

## Item 1 — `m1qm-departure-scale`

**Final status: SHARPENED (headline RETRACTED and rebuilt; net result narrower + honest).**
The forge shipped verdict "scale-external / no owned object fixes the departure RATE." The
independent skeptic returned **WOUNDED** (leap in the headline). The repair was **accepted in
full** — all five repairs (R1–R5) applied and re-verified. The item is NOT closed-as-forged; it
is closed-as-repaired at a strictly narrower claim.

### What is OWNED (survives, verified)

- **The departure RATE is owned + FORCED.** D0's owned emergent-QM dynamics that genuinely
  departs from unitarity is the **archive-tracing channel** `ρ↦PUρU†P` (`06.7:29`; parent
  M1_QM_GAP1 **Block D**, `M1_QM_GAP1_MEMO.md:304-312`). It loses probability for every carrier
  (script gate `F_OWNED_TRACING_CHANNEL_DEPARTS_AT_PHIM1`: trace mean 0.0948 ≈ φ⁻⁵, max
  0.293 < 1 over 300 carriers). Its per-tick retained-amplitude decay `A_{t+1}=φ⁻¹A_t` is
  **FORCED** at `06.40` (owner BOOK_01, `p+p²=1`). So an owned+forced rate `φ⁻¹` DOES govern the
  departing owned dynamics.
- **The owned SI tick scale.** `Λ_act = h/τ₀ = 38 m_e c² ≈ 19.42 MeV` (`BOOK_03`, content-verified;
  line-anchor unresolved — see risk flag). Non-Planck, non-IceCube-tuned (≈5×10⁵ below the HESE
  floor). This is the SI scale the owned rate carries.
- **Citation integrity: PASS** (skeptic KILL GATE 1). τ non-invertibility, emergent-shadow phrase,
  per-tick φ⁻¹ FORCED, α-depth, δ₀ cascade, determinant-balance, Pisot LEAN_PROVED, IceCube
  NOT-OWNED, 25-row ledger — all verbatim. No phantom/misquoted citation.

### What stays OPEN / honestly EXTERNAL

- **The IceCube plateau-knee ENERGY `E*` is external.** Mapping the owned per-tick rate to a knee
  *energy* needs the composite bridge `κV(E)` and the floor value `ζ`, both explicitly NOT-OWNED
  (`08.42:16` domain `0<z<1` only; `ICECUBE_DECOHERENCE_FORM_MEMO.md:332`). This is the single
  genuinely external object (script assertion `ASSERT_KNEE_ENERGY_ESTAR_IS_EXTERNAL`).
- **Scoped wall (survives):** `φ⁻¹` is O(1)/tick → floorless collapse, so it is **not the
  positive-floor PLATEAU-knee rate** (gate `F_MAGNITUDE_...`). This bounds only `φ⁻¹`-vs-plateau-
  knee, NOT `φ⁻¹`-vs-any-departure-rate.

### The leap that was corrected

The forge equivocated on "the dynamics": it defined "the departure" against the **post-conditioned
exactly-unitary complement** `W_eff|retained` (singular values `[1,1,1]`) — which by construction
does not depart — and concluded "no owned object fixes the departure rate." But the parent's own
load-bearing correction (Block D) already ruled that complement is NOT the dynamics. The departing
object D0 owns has a forced rate. Net: "no owned rate" was a **tautology dressed as a finding**
("the object that does not depart, does not depart"). The book itself calls `A_t=φ⁻ᵗ` the
**retained** component (`06.40:19,23`), contradicting the forge's relabel as "leakage."

### Script hygiene (skeptic KILL GATE 3, fixed)

The forge's load-bearing gate `F_SECTOR_RETAINED_SHADOW_UNITARY` was a **tautology** — it computed
`|∏ unit-modulus phases| ≡ 1 ∀n`, could not fail, and did not reproduce the Feshbach K(9,11,13)
shadow. Replaced with the real `B†W_effB` SVD plus a tracing-channel trace-loss gate that actually
departs. Two hardcoded `None` "gates" relabeled as owned-fact assertions. Re-run: all PASS, exit 0,
now non-tautological.

### Vector disposition

**SHARPENED**, not closed and not simply "honestly-external." The *knee ENERGY* is honestly
external; the *rate* is owned. The forge's binary ("owned vs external") was resolved into a
**split**: rate-owned, knee-energy-external.

---

## Registry / bridge-ledger motion (PROPOSAL ONLY)

**SAFE (no owner gate) — recommended:**

- **Note on the IceCube slot** (`D0-PASSPORT-ICECUBE-HESE-001` / D1 flagship): upgrade the existing
  "silent on magnitude" caveat to the *checked* status **"rate-owned (`φ⁻¹`, archive-tracing
  channel, `06.7:29` / Block D, FORCED `06.40`, SI tick `τ₀=h/38 m_e c²`); knee ENERGY `E*`
  external (unowned `κV(E)`/`ζ`)."** This is a pure annotation — it mints no owner, edits no proof
  row, and records only what the repaired memo + passing non-tautological script establish.
- **Citation-anchor correction (bookkeeping):** register that `06.7:373` and `BOOK_03:300` are
  concatenated-book line refs; the content is verbatim in the per-section files
  (`0008__06.7...:27,29` and `0007__03.6...:14,18`). Anchor status: "content-verified,
  line-number-unresolved."

**OWNER-GATED (do NOT apply without an owner) — deferred:**

- **Any energy-owner row for `E*`** is owner-gated on the `κV(E)` bridge + `ζ` (G1 of
  `ICECUBE_DECOHERENCE_FORM_MEMO`). Owning both is the single edit that flips the knee energy from
  external to owned. Until then, no energy owner is warranted.
- **Any claim tying `φ⁻¹` to the plateau-knee rate** is owner-gated on the determinant-balance
  floor-restoring composition (`08.42`) — which is itself the unowned `κV(E)` marriage. Circular
  until `κV(E)` is owned; do not mint.

---

## Highest-value honest result (single)

**D0 owns a FORCED per-tick departure rate `φ⁻¹` for the object it genuinely owns as the
emergent-QM dynamics — the archive-tracing channel (`06.7:29`, Block D) — and the ONLY genuinely
external object in the IceCube link is the map from that rate to the knee ENERGY `E*` (unowned
`κV(E)`/`ζ`).** This is more valuable than the forge's original headline because it (a) is TRUE
against the object D0 actually owns rather than a tautology against a non-departing object, and
(b) localizes the entire external residual to one named bridge, making the reopening condition
explicit and single.

---

## Residual over-claim risk (flagged)

1. **"The dynamics" reading is a settled-parent adjudication, not a theorem.** The whole
   rate-ownership rests on `06.7:29` + Block D picking the tracing channel as "the dynamics." This
   is D0-owned and adjudicated against the complement — but it is a *reading*, not a `.lean` proof.
   If a future reading owns a different object as the dynamics whose rate is not `φ⁻¹`, the rate-
   ownership reopens. **Do not upgrade "rate-owned" to CORE-FORMALIZED.** It is an owned+forced
   *reading-conditional* result.
2. **`BOOK_03:300` line anchor is unresolved.** The content (`Λ_act=38 m_e c²`) is verbatim in the
   per-section file, but no concatenated BOOK_03 exists on disk to resolve `:300`. Cite the
   per-section anchor, not `:300`, in any registry note.
3. **Near-miss / same-number trap.** `φ⁻¹` appears as (a) the tracing-channel departure rate, (b)
   the Pisot arrow modulus, and (c) numerically near several φ-powers. Only (a) is the departure
   rate; (b) is orientation (wrong KIND), and the φ-power/IceCube-energy coincidence is explicitly
   guarded against (`CTRL_PHIPOWER_COINCIDENCE_GUARD`). Keep the wrong-KIND labels on (b) so
   "rate-owned" is never read as "energy-owned via a φ-power."
4. **Scope discipline on F-MAGNITUDE.** The surviving wall is `φ⁻¹`-is-not-the-plateau-knee only.
   Do not let it drift back into "`φ⁻¹` is not a departure rate" — that was the retracted leap.

---

## EXEC SUMMARY

| item | forge verdict | skeptic | final status |
|---|---|---|---|
| `m1qm-departure-scale` | scale-external (no owned rate) | WOUNDED (leap), repair accepted in full | **SHARPENED** — rate-owned (`φ⁻¹`, tracing channel, FORCED `06.40`), only knee ENERGY `E*` external |

**Highest-value honest closure:** D0 owns a **FORCED per-tick departure rate `φ⁻¹`** for the
archive-tracing channel it owns as the emergent-QM dynamics (`06.7:29` / Block D); the sole external
residual is the rate→knee-**ENERGY** map (`κV(E)`/`ζ`, unowned). Registry motion: SAFE note only
(IceCube slot: "rate-owned, knee-energy-external"); energy-owner rows stay owner-gated on `κV(E)`.
Over-claim watch: "rate-owned" is reading-conditional on the Block-D "which object is the dynamics"
adjudication — not a Lean theorem.
