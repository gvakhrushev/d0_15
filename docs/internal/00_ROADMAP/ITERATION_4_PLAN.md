# Iteration 4 — Autonomous front (owner ТЗ ⊕ session groundwork)

**Context.** Owner away ~2h, authorised full autonomous execution. This plan merges the
owner's big autonomous ТЗ with what was already closed earlier this session, so no work is
redone and the front is exactly the genuinely-remaining items.

**Already DONE this session (do NOT redo):** Phase-0 guards exist + pass
(`validate_csv.py`, `check_firewall.py`, `regen_graph.ps1`); Root A α/ζ_D (cb09e4a);
Root B ℤ₂ spinor cover (ce732e4); Root C carrier forcing — roles-orbital / tower-stop /
class-5 aliasing / symplectic-Gleason (9726a99); §4 S_DE fork (745e836); signature 3+1
already CORE-FORMALIZED (two owners). So ТЗ Phases 2,3,4 and T5.2,T5.3 are closed.

**Premise correction that stands (IRON RULE §0.2):** the ТЗ's T2.3 "Δ_α = φ⁻⁵" is WRONG —
φ⁻⁵ = ξ₅ is the proved seam term INSIDE the α formula; Δ_α (~4.15e-4 top-vs-alg residual)
is distinct and has no analytic owner. Δ_α stays a theorem-target; forcing Δ_α=φ⁻⁵ would be
the fit the rules forbid.

**Baseline (HEAD 745e836, tag base-pre-autonomous):** 216 claims — 92 CORE-FORMALIZED,
71 CERT-CLOSED, 12 PROOF-TARGET, 10 EMPIRICAL-PASSPORT, 16 NO-GO(+PROVED); strength
2753/3907 (70.5%); hygiene 100/100; 0 firewall violations.

## Iron rules (enforced every step)
Firewall (no rhetorical promotion; CORE only if empty assumption_ids; passport never core).
α-honesty (structural form, not precision prediction). No v17 overshoots. Each change =
CSV row + artifact + graph regen + INTEGRATION_LOG. OWNER-DECISION-NEEDED for owner-level
calls (never decide a core-form fork / new principle / core demotion alone). Guillotine
(every cert must be able to FAIL). Positive closure delta.

## Front (execution order)

**Phase 0 finish** — tag `base-pre-autonomous` (done); record baseline in INTEGRATION_LOG.

**Phase 1 — GRAVASTAR (fresh result, do first, risk of loss).**
- T1.1 `D0-GRAVASTAR-FORMATION-BRIDGE-001` (BRIDGE, gravity, Book 07) + `vp_gravastar_os_arrest.py`
  (OS-arrest, dS bubble, junction conditions, C_max from master eq). cite PRD 113 L121502.
- T1.2 `D0-COMPACTNESS-LIMIT-001` (LEM, named-gap, Book 07) + `vp_gravastar_compactness.py`:
  symbolic C=3/8 from {photon χ₂≤θ⋆, OS-closure 2C=sin²χ₂, cycle cosθ⋆=4C−1} ⟹ 2C(8C−3)=0;
  structural 3/8 = rank/|Ω₈| = 3/8. NAMED GAP: rank-3 transport = causal cone is postulated,
  not M1-derived → NOT THE. Small Lean `D0.Gravity.CompactnessLimit` for the 3/8 algebra.
- T1.3 `D0-GRAVASTAR-GW-FALSIFIER-001` (EMPIRICAL-PASSPORT, Book 09): horizonless ringdown ≠
  BH — second GW falsifier beyond I_f=log φ.
- T1.4 attempt rank-3=lightcone via Connes triple; if not clean → notes "attempted, open".

**Group A — Lean wave (the autonomous Lean grind; 5–40 min builds).** Triage the ~38
cert-only PYTHON_CERTIFIED claims; write per-claim Lean for the finite/Mathlib-reachable,
core-eligible subset (build only that module). Promote ONLY genuine sorry-free builds;
passports / empirical / Mathlib-blocked stay cert (honest). Interleave prose work during builds.

**T5.1 — phason debt (publication-critical).** One authoritative Book 08 status section +
`vp_phason_status.py`: cert the STRUCTURAL part (phason = perp-space shift DOF of the proved
cut-project carrier; gaplessness = continuous shift symmetry) and declare the dark/radiative
phenomenology BRIDGE. Do NOT fake the dark-matter physics. Sync CSV.

**T5.4/T5.5 — anchors + H0 passport.** Coldea/CoNb₂O₆, JUNO, NuFIT 6.0 into books as
EXTERNAL-ANCHOR passport targets; `D0-H0-EVOLVING-W-001` passport (H0(z) from R_n=φⁿ−1,
falsifier H0↑/S8). All EMPIRICAL-PASSPORT, firewall-blocked.

**T3.5 (light) — Connes–Rovelli thermal-time BRIDGE** note on the existing time-modular-flow.

**Phase 6 — sync + report.** Sync `D0_THEORY_DOSSIER.md` (Connes triple primitive + gravastar
+ new claim_ids); final guards; `00_ROADMAP/AUTONOMOUS_SESSION_REPORT.md` (honest delta +
OWNER-DECISION-NEEDED list).

**Skill — universal `verified-closure-protocol`** (non-D0-specific hammer): Explore audit →
FAIL-able cert with HONEST_* tokens → Lean depth where reachable → registry → integration →
guards → commit. SKILL.md + tools/ (cert template, honesty checklist, commit-via-file note).

## Verification
Per claim: cert PASS (exit 0, FAIL-able) → CSV row → validate_csv + check_firewall →
generate_lean_aggregates (if Lean) → regen_graph → d0_score → INTEGRATION_LOG → commit per phase.
End: all guards green, hygiene ≥ baseline, positive PROOF-TARGET delta, report written.
