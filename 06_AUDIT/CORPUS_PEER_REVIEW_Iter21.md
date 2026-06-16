# D0 corpus — full peer review (Iter-21)

**Method.** Deterministic sweep of all ~50 `tools/check_*.py` guards + `lake build D0.All` + `d0_score`,
combined with a 21-agent multi-dimensional review (proof-integrity census over 6 D0 slices; register
honesty; owner-edge ledger; cert integrity; theory coherence; publication-readiness) and an adversarial
verification pass that tried to *refute* every HIGH/CRITICAL finding. 58 findings raised; of 10 HIGH, **5
were confirmed and 5 were rejected as false alarms** on direct re-inspection.

## Verdict

The **machine-checked core is in strong, publication-grade health**; the weaknesses are a bounded,
enumerable class of **over-claims of degree** (vacuous proof-of-record tokens) plus **stale human-facing
books**. No proof holes exist anywhere. Severity: **0 CRITICAL, 5 confirmed HIGH, ~19 MEDIUM.**

| Layer | Health | Evidence |
|---|---|---|
| Lean kernel | ✅ strong | `lake build D0.All` GREEN (3814 jobs); **zero `sorry`/`admit`/`axiom` across all 357 modules** |
| Registry calibration | ✅ strong | 0 LEAN_PROVED rows with dangling modules; external theorems (Jones, Mordell-E8, Connes, Tomita-Takesaki, Wilson, Adler-Weiss, Frobenius) correctly isolated as BRIDGE w/ cited ASSUMP-* |
| Owner-edge ledger | ✅ sound | **no CORE claim is load-bearing on an external assumption**; 3 rows flagged QUESTIONABLE (below) |
| Certs | �︎ mostly | ~162/170 genuinely gate; 8 can't-fail print-stubs already tracked in `check_cert_can_fail` GRANDFATHER |
| Honesty guards | ✅ pass | firewall, cert-can-fail, tautology, dangling(=0), physical-bridge-discipline, d0_score(82.6%, demotions 0) |
| **Books (01_BOOKS)** | ❌ **stale** | ~24 `check_v14_*_sync` / book guards RED — books lag the registry/Lean |
| Publication scaffold | ✅ sound | firewall machine-enforced; DO_NOT_CLAIM / Reviewer Risk Ledger forbid the dangerous over-statements |

## Strengths (confirmed)

- **No holes.** Zero `sorry`/`admit`/`axiom` in 357 modules. The overwhelming majority of CORE/LEAN_PROVED
  theorems are genuine load-bearing proofs (`ring`/`nlinarith`/`linear_combination` over φ; `native_decide`/
  `decide` on non-trivial finite ℤ/ℚ goals; real `calc` ∂∂=0; PSD-Gram; two-sided `Matrix.rank`).
- **Clay/millennium discipline is honest.** The §24–§30 reductios (CriticalAxisM1, HeatTraceLyapunov,
  HodgeAlgebraicRealization) are correctly BRIDGE: `RequiresExternalCatalogue := ¬Forced` is a real negation,
  and RH/PvNP/Hodge content is named as an *assumption*, not derived. The publication abstract does not claim
  any Clay problem solved (a scare to the contrary was raised and **refuted**).
- **The K(9,11,13) / rank-3 / nullity-30=8+10+12 / φ spine is consistent** across 39+ prose files + the registry.
- **Verification is robust to scrutiny:** half the HIGH findings were false alarms (e.g. MIXING-HIERARCHY-INVERSION
  proves the real trace/minors/det; the "uncovered Clay claims" scare is contradicted by the corpus's own docs).

## Confirmed findings

### A. Over-claims of degree — vacuous / definitional proof-of-record (the #1 honesty issue)
A bounded set of CORE/LEAN_PROVED/NO-GO claims have a proof-of-record that is partly or wholly **vacuous**
(`Prop := True`, `D = D := rfl`, a boolean-flag tautology, `¬False`, or the conclusion encoded in a `def`).
None is a hole; each over-states *degree* (the status asserts more than the Lean substantiates). Affected:

- **HIGH** `D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY` — sole backing token `NO_GO_ARCHIVE_PHASE_LOCAL_UNIQUENESS`
  is a `def` whose only field is `noGo : True := trivial`.
- **HIGH** `D0-ARCHIVE-GAUSSIAN-CHANNEL-001` — the "classical Gaussian channel" CORE theorem is *conditional*
  on an external HST theorem (`hHST : ExternalHSTTheorem` as an explicit hypothesis) with `Subgaussian := True`,
  yet registered **CORE-FORMALIZED, uses_bridge_assumptions=False, no ASSUMP**. Should be BRIDGE + a named ASSUMP-HST.
- **MEDIUM** (vacuous conjunct / token, real content also present): `D0-ARCHIVE-PHASE-CURVATURE`,
  `D0-TRACE-HEAT-CAPACITY-GRAVITY-001` (`D=D`), `D0-BRIDGE-SI-CALIBRATION-CLOSURE-001` (`¬False`),
  `D0-LEAN-BRIDGE-001` + `D0-LEAN-CORE-001` (meta tokens), `D0-GAUGE-MATRIX-REP-TRANSFORM-001` (`*_well_typed`),
  `D0-MATTER-SOURCE-NEUTRALITY-001` (source ≡ 0 tautology), `D0-ICECUBE-001` (`Prop:=True` + constant-0 coupling),
  `D0-MASTER-EVOLUTION-001`, `D0-CVFT-001A`, `D0-CVFT-NOGO-001`,
  `D0-QUASICRYSTAL-PHENOMENOLOGY-OPERATOR-ORIGIN-001` (EMCoupling ≡ 0), `D0-RANK3-CAUSAL-CONE-FORCING-001`,
  `D0-HURWITZ-LOCAL-BOUNDARY-001`, `D0-HURWITZ-INTERNAL-DIMENSION-SELECTOR-001`.

**Cure (per lean-stub-audit):** each must be *cured* (replace the vacuous token with a real obstruction/
relation theorem) or *disclosed* (demote to BRIDGE/cert/PROOF-TARGET with the gap named). The existing
`check_no_tautology_proofs` guard catches `True` stubs but is blind to `D=D`/boolean-flag/`¬False` — extend it.

### B. Owner-edge ledger — 3 QUESTIONABLE assumptions (on BRIDGE rows, correctly)
`ASSUMP-HODGE-ALGEBRAIC-FORCING`, `ASSUMP-PACKAGING-REFLECTION-SYMMETRY` (RH content), and
`ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL` are **D0-internal forcing targets parked as external assumptions**, not
classical externals. They sit on BRIDGE claims (so no CORE leaks), and they are exactly the §28/§29/§24
frontier — but they should be labelled "internal target (not yet derived)" rather than implying an external owner.

### C. Print-only / can't-fail certs (disclosed debt, not new)
`vp_desi_bao_sde_failure_diagnostics`, `vp_icecube_hese_baseline_comparison`, `vp_sparc_hull_boundary_response_kernel`,
`vp_canonical_operator_search`, `vp_critical_collapse_dss_echo_lattice`, `vp_qnm_delta0_overtone_ladder` print
hardcoded tokens / discard their computation. All are **already grandfathered** in `check_cert_can_fail` and
typed EMPIRICAL-PASSPORT / NO_GO_PROVED, so the registry does not claim them as proofs. Recommendation: make
each compute-and-assert, or down-type to a pure data passport, to shrink the grandfather toward 0 (as was just
done for the dangling-pointer ratchet).

### D. Books stale (publication-readiness #1 gap) — ~24 guards RED
`check_v14_*_sync`, `check_book_*`, `check_book05_integrated_rewrite` (Book 05 = 1227-line dump),
`check_standard_language_audit_budget` (149 > 125), glossary, ktheory-gaplabel/condensed sync — all fail
because the published books in `01_BOOKS` lag the registry/Lean (missing tokens like `## 05.13`,
`D0.Matter.CKMPhasonHolonomy`, various `vp_*.py`). The **Lean+registry is ahead of the books**; re-assembly
(`tools/assemble_books.py` + re-run the sync guards) is the required publication step.

## Fixed during this review
- `check_physical_bridge_discipline` regression (from this session's CORE-flips): `D0-GRAV-005` + `D0-CVFT-F3B`
  lacked the scope-guard disclaimer word; added "external passport (not core)/(data, not core)". Guard now PASS.

## Prioritized remediation
1. **Reclassify `D0-ARCHIVE-GAUSSIAN-CHANNEL-001`** → BRIDGE-ASSUMPTIONS-EXPLICIT + ASSUMP-HST (highest, a clear mislabel).
2. **Cure-or-disclose the ~16 vacuous-token claims** (class A) — one reviewable commit per cluster; extend
   `check_no_tautology_proofs` to ratchet `D=D`/boolean-flag/`¬False` so it can't regrow.
3. **Re-assemble the books** and turn the ~24 sync guards green (publication blocker).
4. Relabel the 3 QUESTIONABLE ledger rows as internal targets; shrink the can't-fail cert grandfather.

Overall: a corpus whose **formal core is genuinely sound and unusually honest**, with a well-bounded
remediation list dominated by (a) tidying vacuous proof-of-record tokens and (b) re-syncing the prose books.
