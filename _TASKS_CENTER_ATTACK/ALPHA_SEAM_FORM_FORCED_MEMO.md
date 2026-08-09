# ALPHA SEAM-FORM-FORCED — reframing the α-line from "CHK 9-digit coincidence" to
# "uniqueness + progressive narrowing": the candidate row D0-ALPHA-SEAM-FORM-FORCED-001 (DRAFT)

**Date:** 2026-07-18 · **Status:** DRAFT candidate (compute + mint package; pre-skeptic).
> **[POST-MINT NOTE 2026-07-18, external review]** Header superseded: row `D0-ALPHA-SEAM-FORM-FORCED-001` (564) is MINTED post-skeptic #19; the four-level ladder is live at §02.13.h:95/:142. §0's sentence "the missing sentence is the CROSS-SCOPE IDENTIFICATION…" is FALSIFIED: the identification exists in print since 2026-06-17 (BOOK_06 §06.30a) — see `SEAM_RATE_IMPORT_MEMO.md` (POST-SKEPTIC #20) and the obligations update in row 564's note. Obligation (ii) is ASSEMBLY-CANDIDATE (owner adoption residual); obligation (i) has a named cert-comment-grade candidate (`|V₁₁|+1` sectors).
**Owner directive (session 2026-07-18):** "α на 9 знаках — не критерий … теория должна доказать
единственность и сужать последовательно пространство вариантов, в итоге доводя до
единственного." This memo implements exactly that criterion for the α-line.
**Pre-flight (recon agent, full read):** `ALPHA_SEAM_NOGO_V2.md` + `CAMPAIGN_FINAL.md` (the
stop-documents) + all α rows + §02.13 section source + seam certs. KEY FRAME: the α scope holds
TWO objects — **object A** (moment REALIZATION `(μ₁,μ₂,μ₃)=(1/3, 12288/5, 0)`, `Δα`, closed by
`D0-ALPHA-SEAM-REALIZATION-NOGO-001` with irreducible external owner `ASSUMP-DIXMIER-TRACE`)
and **object B** (the dressing/holonomy `α_D0⁻¹ = α_top⁻¹ + φ⁻¹⁷(1 + h_KS·sin θ_seam)`). This
memo touches ONLY object B. No existing row states joint form-forcing (recon (c): the forcing
is distributed over three fully-owned THE legs + the split depth leg + one CHK); no duplication.
**Companion cert:** `vp_alpha_seam_form_forced.py` — S1 assembly (two exact ℚ(φ) routes to
`α_top⁻¹`, dressing hits the FROZEN book value at 9 digits), S2 separation (7 rival tuples all
land ≥ 1.6×10⁻⁵ away — every named control can fail the conclusion), S4 firewall guard
(object-B-only, textual). **Default rc=2 (HONEST-OPEN — the registered state);
`--grant-ks-rate` rc=0 (sufficiency demo).**

## §0. The reframe (what changes and what does not)

OLD criterion (the "CHK-coincidence" reading, §02.13.h:95): "the 9-digit agreement … is an
empirical CHK … the cos/exp/wrong-depth controls all FAIL" — a NUMERIC test.
NEW criterion (this row): **the dressing TUPLE is unique among D0-admissible seam dressings** —
a STRUCTURAL claim, with the 9-digit agreement demoted from criterion to CONSEQUENCE.

The tuple and its legs (recon (b), per-leg grades):

| leg | value | owner row | grade |
|---|---|---|---|
| depth (seam factor) | `ξ₅ = φ⁻⁵` | D0-XI5-TORUS-DEFECT-001 (+CROSS-SECTOR-001) | **THE** (Lean) |
| depth (transport factor) | `φ⁻¹²` + composition `φ⁻¹⁷ = ξ₅·φ⁻¹²` | — none — prose 02.13.h:87 only ("the seam ξ₅ times the electroweak transport") | **OPEN — second open sub-leg (skeptic #19 R1)** |
| channel | `sin` (off-diagonal, `G²=−I`) | D0-Q8-SIN-CHANNEL-001 | **THE** (Lean) |
| angle | `θ_seam = 12/5` (exact ℚ(φ)) | D0-PI0-DISCRETE-ANGLE-001 | **THE** (Lean) |
| form | linear `1+h·sin` (`N²=0`) | D0-ALPHA-HOLONOMY-LINEAR-FORM-001 | **THE** (Lean) |
| **rate** | **`h_KS = ln φ`** | identification unowned — near-parents rows 285/243 (see below) | **OPEN — the PROOF-TARGET content** |

Progressive narrowing, made explicit (post-#19 honest count): THREE legs fully owned THE
(channel, angle, form) + the depth leg SPLIT (seam factor ξ₅ THE; transport factor φ⁻¹² and the
composition unowned prose — the corpus's own pre-existing soft spot: 02.13.h:95's blanket
"depth graduates to THE" and row 286's note citing the angle/channel rows as depth owners
repeat on leg 1 the defect this row diagnoses on leg 5). The row's open content is therefore
THREE obligations: (i) leg 1b — own the φ⁻¹² transport factor and the composition; (ii) leg 5 —
the rate: the two owned NEAR-parents are `D0-SEAM-HOLONOMY-001` (row 285, CORE-FORMALIZED —
already registers "the correction multiplier 1+h_KS·sin(θ_seam) applies to alpha and PMNS.
Structure THE") and `D0-FIBONACCI-IF-FORCING-001` (row 243, LEAN_PROVED/CERT-CLOSED — owns
"I_f = log φ is THE for the VALUE and its MECHANISM"); the missing sentence is the CROSS-SCOPE
IDENTIFICATION of 285's registered multiplier rate with 243's owned rate (NOT "rate is
prose-only": the rate VALUE is owned at 243, the dressing-rate identification is not; note
row 253's Lean owns only |λ_max| = φ — the KS-entropy identification there is the external
Pesin/Margulis-Ruelle wrapper); (iii) joint exhaustion (no owned rival on any axis). Status ladder in §02.13.h becomes
four levels: **STRUCTURE THE (legs) → FORM-FORCED PROOF-TARGET (joint uniqueness, THIS row) →
9-digit CHK (consequence; D0-ALPHA-HOLONOMY-002 unchanged) → last ~10⁻⁸ HYP
(D0-ALPHA-MEASUREMENT-LIMIT-001 unchanged).**

## §1. Named failures (the falsifier surface — structural, not numeric)

- **F1 (form):** an owned admissible seam with `N² ≠ 0` (returning/undirected crossing) would
  re-admit the `exp` form — kills the linear leg. (Load-bearing idempotent control `M²=M≠0`
  already in `D0.Spectral.SeamTransportLinear`.)
- **F2 (channel):** an owned admissible diagonal/trace (`cos`) selector — kills the sin leg.
- **F3 (depth):** an owned admissible closing depth `≠ φ⁻¹⁷` — the registry-named seam family
  `φ⁻⁴/φ⁻⁶` (D0-XI5-CROSS-SECTOR-001 controls; total depths `φ⁻¹⁶`/`φ⁻¹⁸`, both in S2); the
  `φ⁻¹⁶` loop-floor is a DIFFERENT named object (the Δα-bound, 02.13:116 — R3 attribution
  fix) — kills the depth leg.
- **F4 (rate):** an owned admissible KS-rate `≠ ln φ` (a second admissible Lyapunov/monodromy
  rate) — kills the OPEN leg 5; this is the likeliest genuine failure mode and is exactly why
  the row is PROOF-TARGET, not CERT-CLOSED.
- **F5 (anti-tuning + firewall redirection):** a free real coefficient re-entering the dressing
  falsifies "zero free real coefficients" (§02.13.h:79). AND — the redirection clause — any
  owned derivation giving π₀ as a seam COEFFICIENT with independent content **beyond the
  assembled form** (hook (iv) verbatim, NOGO_V2:66) is NOT a falsification of form-forcing: it REOPENS
  the realization no-go (object A). The row must never absorb such a result; it must hand it
  to the no-go's owner. This keeps the reform on the correct side of the no-go boundary.

## §2. No-go compliance (the hard boundaries, recon (a))

This row: does NOT claim realization of `(μ₁,μ₂,μ₃)` or `Δα`; does NOT touch `/D_Σ`,
ρ-normalization, within-part structure of zones 11/13, or the ζ/Dixmier route (BLOCKED,
`ASSUMP-LINDEMANN-LNPHI`); does NOT promote the 9-digit value to THE (forbidden twice:
no-go + §02.13:95/:142); does NOT displace `ASSUMP-DIXMIER-TRACE`. The cert's S4 guard makes
the object-B scope machine-visible.

## §3. Pre-registered attack surface

- **ATT-1 (separation ≠ exhaustion).** S2 separates the candidate from 7 NAMED rivals; it does
  not exhaust the rival space (that is the row's open content, stated). A skeptic reading S2 as
  a uniqueness proof should find the memo already grading it as a falsifier surface only.
- **ATT-2 (leg-5 borrow).** The rate VALUE is owned (`D0-FIBONACCI-IF-FORCING-001`, row 243)
  and the multiplier STRUCTURE is registered (`D0-SEAM-HOLONOMY-001`, row 285); the cross-scope
  identification of the two is the candidate sentence, not owned — the row must not silently
  borrow either (trap o: instantiation of an owned parent is an ownership GAIN only when the
  identification itself is owned). Row 253 (`D0-IF-KS-FORMULA-FIX-001`) is the weaker
  reference: its Lean owns only `|λ_max| = φ`; the KS step is the external wrapper.
- **ATT-3 (frozen-value circularity).** S1 compares to the FROZEN book value (02.13.h), not to
  CODATA (printed context-only) — the cert never optimizes toward data; trap (f) audit invited.
- **ATT-4 (which row carries what).** D0-ALPHA-HOLONOMY-002 stays the empirical CHK passport;
  this row owns the STRUCTURAL uniqueness program. If the skeptic finds any clause where this
  row absorbs 002's numeric content, that clause must be cut.

## §4. Ready-to-mint package (owner-authorized session; to apply after skeptic)

1. New row `D0-ALPHA-SEAM-FORM-FORCED-001` (both ledgers): BOOK_02 §02.13.h anchor; type
   frontier; release **PROOF-TARGET**; cert `vp_alpha_seam_form_forced.py` (rc=2 = registered
   honest state); note = §0 table + §1 failures + §2 compliance + cross-refs (three THE legs + split depth leg,
   002 CHK unchanged, MEASUREMENT-LIMIT HYP unchanged, SEAM-REALIZATION-NOGO untouched;
   near-parents D0-SEAM-HOLONOMY-001 (285) + D0-FIBONACCI-IF-FORCING-001 (243);
   D0-IF-KS-FORMULA-FIX-001 (253) weaker reference).
2. §02.13.h "Honest status split" (:95, section source
   `0018__02.13__gauge-and-coefficient-proof-cells.md`): insert the FORM-FORCED level between
   STRUCTURE-THE and 9-digit-CHK; ALSO update the ladder ECHO at :142 (skeptic #19 R6 — the
   ladder appears twice; both must carry the same four levels); reassemble books; guards.
   Cross-ref clause (R6): S2 re-runs 002's cos/exp/wrong-depth control battery against the
   FROZEN book value (a referee 6.7e-8 from CODATA) — same evidence, two roles: 002 owns the
   CODATA match (CHK), this row owns the structural separation; neither absorbs the other.
3. NOT done: no change to rows 286/292/536; no Lean module yet (leg 5 is the open theorem).
