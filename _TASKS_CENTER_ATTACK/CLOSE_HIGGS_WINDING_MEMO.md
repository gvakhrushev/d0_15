# CLOSING FORGE — Higgs condensation + matter-winding residues (construction campaign)

**Date:** 2026-07-06 · **Status:** DRAFT memo (verification only). Memo-only.
**No registry/book/`.lean`/`053040` edits. No git commit.** Row-notes PROPOSED at foot for owner.
**Companion can-fail:** `_TASKS_CENTER_ATTACK/close_higgs_winding_check.py`
— **15 base checks PASS (rc=0), 2 mutants KILL** (`break_return`, `break_frozen_x`). Exact integer
arithmetic mod 44 + `Fraction`; no float on any load-bearing fact.
**Skill:** `d0-adversarial-forcing-loop`.

Builds on `CLOSE_MATTER_MEMO.md` (T1–T4) and `DEEP_M_COLOUR_HIGGS_MEMO.md` (two-wall Higgs). This pass
attacks the two matter residues once more with the SHARP carrier the prior passes named but did not
drill: for Higgs W1 the **exact 2×2 return-operator carrier over `ZMod 44`** (not the `Fin3`/`ℂ³³`
carriers already killed), and for winding the **actual `TorusParameter` structure on disk**.

---

## Executive scoreboard (per residue)

| # | Residue | Route | Verdict |
|---|---------|-------|---------|
| 1 | Higgs W1 — non-commuting frozen `Q0` on `ZMod 44` | build from owned return/frozen-SU(2) | **FAILED-BOUNDARY (sharpened: the three-property trap)** |
| 2 | Higgs W2 — the SSB double-well sign | search owned negative-sign input | **SHARP-EXTERNAL (confirmed; sign NOT manufactured)** |
| 3 | Winding `W` metric — torus parameter `a` | pin `a` from owned datum | **SHARP-EXTERNAL-PRIM (`PRIM-WINDING-METRIC`, exact I/O)** |
| 4 | Branch→generation ROW | is the row owned? | **SHARP-EXTERNAL-PRIM (`PRIM-LEPTON-BRANCH-FIXING`, exact I/O)** |

**Net: 0 no-gos drop from the count.** The two Higgs residues are confirmed external (W1 sharpened to a
new "three-property trap" characterisation; W2 sign NOT manufactured, per the burn record). The two
winding residues get the **SHARP terminal-passport typings the task requested** — clean `PRIM` names with
exact INPUT/OUTPUT that the owner accepts as a form of closure. No derivation of the Higgs sign, the
winding value, colour `M₃`, or a frozen `Q0` is manufactured.

---

## Owned material inventory (verbatim, file:line, read past ±10)

**The Higgs return operator `T` (the RIGHT carrier).**
- `D0/Matter/HiggsReturnQuotientAction.lean:20` `def T : Matrix (Fin 2) (Fin 2) (ZMod 44) := !![0, 1; 1, -1]`
  (charpoly `x²+x−1`, golden). `:23 return_action_period_30 : T ^ 30 = 1` (`native_decide`);
  `:26 return_modulus_44_not_toral_period : T ^ 44 ≠ 1`. So the "`ZMod 44`" is the **entry modulus of a
  2×2 return matrix**, and `T` has toral order **30**, NOT a period-44 cyclic shift.
- `D0/Matter/HiggsCondensationPresentCoreMaximalityNoGo.lean:27-29`
  `theorem tPoly_commutes (a b : ZMod 44) : Commute T (a • 1 + b • T)`. The **present-core class is
  `{a•1 + b•T}`** — the 2-dim commutative subalgebra `ℤ/44[T] ⊂ M₂(ZMod 44)` (all higher powers reduce
  by `T² = −T + 1`). `:33 def Qnc := !![1,0;0,0]`; `:35 Qnc_not_commute : ¬ Commute T Qnc` — the
  non-commuting witness is a **hand-picked** rank-1, not present-core.

**The owned frozen SU(2) (a genuine non-commuting object, on a 2×2 carrier).**
- `D0/Matter/HiggsScalarProjectorConstructive.lean:32` `def FrozenSU2_X : M2 := !![0, 1; 1, 0]`;
  `:35 FrozenSU2_Z := !![1, 0; 0, -1]` (`M2 = Matrix (Fin 2) (Fin 2) ℚ`).
  `:48 commutes_XZ_forces_scalar_matrix` (a projector commuting with both X and Z is scalar);
  `:63 nonzero_gauge_idempotent_eq_identity` (the ONLY nonzero gauge-compatible idempotent is `I₂`);
  `:82 rank1_scalar_projector_breaks_su2_gauge_compatibility` (`diag(1,0)` is idempotent but does NOT
  commute with X). This is the FIRST owned frozen non-commuting object living on a 2×2 carrier — the
  prior memo (T4) only found `Fin3`/`ℂ³³` objects.

**The torus parameter `a` (the winding metric knob).**
- `D0/Geometry/TorusCore13GeometryOrigin.lean:15-17` `structure TorusParameter where a : Rat;
  h_gt_one : 1 < a`. `:21-23` `inner := 1`, `core := (a+1)/2`, `outer := a`.
  `:12` comment verbatim: "The concrete passport **may instantiate** `a = phi^5`". So `a` is a **free
  `Rat`** constrained only by `1 < a`; `a = φ⁵` is an instantiation, **not a theorem**.
- `D0/Geometry/TorusShellAttachment.lean:85-95 torusShell_radius_strictMono` — `1 < (a+1)/2 < a` for
  **every** `a > 1` (order parameter-free).

**The branch→generation row (the lepton residue).**
- `D0/Extensions/LeptonBranchFixingNoGo.lean:33 numGenerations_eq_three := rfl` (the `3` = zone count),
  `:~30 numBranches = 2`; `:41 shell_no_fixed_point`; the three pigeonhole `decide` no-gos
  (`no_injective_gen_into_branch`, `no_surjective_branch_onto_gen`, `no_bijection_branch_gen`). Header
  names the third row `D0-X5-LEPTON-CONTRACT-001` = **"POSTULATED HYP"** (external).

---

## RESIDUE 1 — HIGGS W1: non-commuting frozen `Q0` on the `ZMod 44` return carrier

### Construction attempt (the task's Route 1, done on the RIGHT carrier)
The prior kill (T4) was carrier-mismatch: owned non-commuting objects lived on `Fin3`/`ℂ³³`, not the
`ZMod 44` return operator. This pass builds **directly on the `T`-carrier `M₂(ZMod 44)`** and asks the
sharp question: **is there an owned idempotent on this carrier that fails to commute with `T`?**

### What actually happens (all computed, `close_higgs_winding_check.py`)
1. **The wall, reproduced exactly.** Every present-core element `a•1+b•T` commutes with `T` (R1b), and
   the present-core has exactly **8 idempotents, ALL commuting with `T`** (R1c). Trivial orbit ⇒ no
   double-well. Confirmed by execution, not just cited.
2. **The crack the prior missed — a genuine owned non-commuting object DOES live on this carrier.**
   `FrozenSU2_X = !![0,1;1,0]` satisfies `[T, X] ≠ 0` **and** `X ∉ present-core` (R1d) — it is not a
   polynomial in `T`. So the T4 verdict "no owned non-commuting object on the `ZMod 44` carrier" is
   **too strong**: there is one, `FrozenSU2_X`, owned and frozen (minted in
   `HiggsScalarProjectorConstructive.lean`).
3. **But `FrozenSU2_X` fails the idempotent leg — it is an INVOLUTION** (`X² = I₂`, R1e), a conjugator,
   not a projector `Q0`. And the owned gauge analysis proves the only idempotent commuting with **both**
   frozen generators is scalar `I₂` (trivial-orbit). So the owned frozen SU(2) supplies the non-commuting
   *action* but never a non-commuting *idempotent*.
4. **THE SHARP WALL (new characterisation): the three-property trap.** A Higgs `Q0` must be
   simultaneously **(i) idempotent, (ii) `[T,Q0]≠0`, (iii) owned/frozen**. The owned named 2×2 objects
   `{I, T, T², FrozenSU2_X, FrozenSU2_Z, XZ}` realise **any TWO but never all THREE** (R1f, table below).
   This is strictly sharper than "no non-commuting object on the carrier".

   | owned object | idempotent | `[T,·]≠0` | frozen/owned |
   |---|:---:|:---:|:---:|
   | present-core idempotents (8) | ✔ | ✘ | ✔ |
   | `FrozenSU2_X`, `FrozenSU2_Z`, `XZ` | ✘ | ✔ | ✔ |
   | hand-picked `Qnc=diag(1,0)` | ✔ | ✔ | ✘ (chosen) |

5. **It is an OWNERSHIP wall, not an existence wall.** Non-commuting idempotents mod 44 exist in
   abundance — **3476** of the 3484 total idempotents fail to commute with `T` (R1g) — but none is an
   owned/frozen scene object. Exactly the `Qnc` row: idempotent + non-commuting but a free CHOICE.

### Verdict — FAILED-BOUNDARY (sharpened: the three-property trap)
No construction. But the T4 statement is **corrected and sharpened**: an owned frozen non-commuting
object DOES live on the exact `ZMod 44` return carrier (`FrozenSU2_X`) — the wall is not carrier-absence.
The precise wall is that **idempotent ∧ non-commuting ∧ owned** is jointly unrealised: the owned frozen
material gives any two legs, never all three. Exact minimal missing object: **a frozen idempotent
`Q0 ∈ M₂(ZMod 44)` with `[T,Q0]≠0`, derived (not chosen)** — plus W2 (below). No no-go reduces.

---

## RESIDUE 2 — HIGGS W2: the SSB double-well sign

### Construction attempt
Is the negative (double-well) quadratic sign owned anywhere — the branch defect gap `2δ₀`, a cost-vs-info
crossing, any owned scalar that flips `z² ≥ 0` to negative?

### What actually happens
1. The log-det quadratic coefficient is `z² ≥ 0`, a structural **square** (`DEEP_M` §W2 verbatim:
   `assert sp.simplify(quad_coeff - z**2) == 0`; F6, BOOK_04 §04.16). Reproduced as a nonnegative square
   (R2 check).
2. **The negative sign is NOT owned.** Per the verified burn record: *"Higgs SSB sign was a generic
   entropy artifact 20/20 random, NOT forced."* I did NOT search for a candidate to promote, and I do
   **not** manufacture one — that is precisely the forbidden move the anti-over-claim record guards. The
   branch gap `2δ₀` is a defect-plane weight (sums into the branch triple), not a sign on the log-det
   quadratic; there is no owned iso carrying it onto the condensation potential (same no-owned-iso wall
   as the winding row).

### Verdict — SHARP-EXTERNAL (confirmed)
W2 is genuinely external. **Sharp typing:**
`PRIM-HIGGS-SSB-SIGN` — **INPUT:** an external negative-sign datum (a double-well/instability input, e.g.
a measured `μ² < 0`). **OUTPUT:** flips the owned `z² ≥ 0` log-det coefficient to the SSB sign, enabling
condensation. **Owned side returned:** the structural fact that absent this import the coefficient is a
nonnegative square (no in-scene double-well). No sign manufactured. Consistent with the two-wall
`DEEP_M` result: W1 and W2 are **two independent external imports**.

---

## RESIDUE 3 — WINDING `W` metric: the torus parameter `a`

### Construction attempt (the task's Route 3)
Is `a` fixed by any owned datum — the zone sizes `{9,11,13}`, `φ`, the `τ⁻¹` quantum, `m₀·t₀=1`?

### What actually happens (verified on disk)
1. **The ORDER is owned and parameter-free.** `torusShell_radius_strictMono`: `1 < (a+1)/2 < a` for
   **every** `a>1` (R3 order check), so `W(e) < W(μ) < W(τ)` — every gap SIGN is owned.
2. **`a` is a FREE passport parameter.** `TorusParameter` on disk carries only `a : Rat` with `1 < a`,
   and the source comment says `a = φ⁵` is a passport **instantiation**, not a theorem. Hard grep: `a` is
   never forced — no owned lemma pins it from zone sizes, `φ`, `τ⁻¹`, or `m₀·t₀=1`. The zone sizes
   `{9,11,13}` live on the COMBINATORIAL carrier (degrees `33−|zone|`); they do not determine the
   geometric radius parameter `a`.
3. **The metric is provably non-unique** (R3): the integer winding sections `(1,2,3)` and `(1,2,5)` agree
   on order, differ on value — a monotone section of a 3-chain is non-unique. The order fixes gap signs,
   never gap sizes.

### Verdict — SHARP-EXTERNAL-PRIM (exact I/O)
`PRIM-WINDING-METRIC` (equivalently `PRIM-TORUS-PARAMETER-a`) —
- **INPUT (external, measured):** the torus parameter `a > 1` (or, equivalently, the integer winding
  section, i.e. the measured lepton mass-ratio data via `m_rest = m₀·W`).
- **OUTPUT (owned invariant returned):** the parameter-free radial order
  `W(e) < W(μ) < W(τ)` (`torusShell_radius_strictMono`), i.e. the winding's gap SIGNS and the total order
  `e < μ < τ`. The **metric** (integer gap SIZES) is the passport; the **order** is the owned skeleton the
  PRIM sits on top of.

This is the clean terminal-passport typing the task requested: exact external INPUT (`a`), exact owned
OUTPUT (the strict order), matching the verified memory (mass ratios = terminal-passport).

---

## RESIDUE 4 — branch→generation ROW

### Construction attempt (the task's Route 4)
Is the map from the 2 lepton branch-orbits `{4-cycle, 3-cycle}` to the 3 zone-generations owned?

### What actually happens (verified on disk)
`LeptonBranchFixingNoGo` proves by `decide`: `numBranches = 2`, `numGenerations = 3`, no fixed point
(`shell_no_fixed_point`), and the three pigeonhole no-gos — **no injection `Gen(3)↪Branch(2)`, no
surjection `Branch(2)↠Gen(3)`, no bijection** (R4 checks reproduce all three). The `3` is the
zone-owned count; the third generation EXISTS as `outerD13` (per `CLOSE_MATTER` T1), but the **labelled
row** `branch → (e,μ,τ)` is impossible in-carrier by cardinality. Header names the third row
`D0-X5-LEPTON-CONTRACT-001` = **"POSTULATED HYP"**.

### Verdict — SHARP-EXTERNAL-PRIM (exact I/O)
`PRIM-LEPTON-BRANCH-FIXING-OPERATOR` —
- **INPUT (external):** a branch→generation assignment (the third-row label / the `X5-LEPTON-CONTRACT`
  hypothesis) fixing which branch-orbit maps to which zone-generation.
- **OUTPUT (owned invariant returned):** the in-carrier structure `numBranches=2 < 3=numGenerations`
  with the three pigeonhole obstructions — i.e. the row cannot be supplied internally (proven), and the
  zone-3 that receives it is RANK-ONLY (`csv:460`, `GL(3)` freedom). The PRIM imports exactly the row the
  scene provably cannot own, and returns the owned cardinality wall it must respect.

---

## §05.8.R — INDEPENDENT SKEPTIC PASS (kill-mandate)

Mandate: find the SMUGGLED external datum, OR the over-claim, in any verdict.

**R1 (three-property trap).** *Kill attempt: "you found an owned non-commuting object on the right
carrier (`FrozenSU2_X`) — that CONTRADICTS T4's carrier-mismatch kill, so one of you is wrong / you
over-claim a crack."* **Sustained as a correction, not a kill.** T4 said "no owned non-commuting object
on the `ZMod 44` carrier"; that is literally false (`FrozenSU2_X` is one, `[T,X]≠0`, `X∉present-core`,
R1d). But the crack does NOT open the wall: `FrozenSU2_X` is an involution, not an idempotent (R1e), and
the sharp wall is the joint `idempotent ∧ non-commuting ∧ owned` (R1f), which stays unrealised. Verdict
stays FAILED-BOUNDARY; the T4 statement is corrected (sharper wall), no closure claimed, nothing
smuggled. ACCEPT (with the T4 correction logged).

**R2 (SSB sign).** *Kill attempt: "you dressed a refusal-to-search as a boundary — maybe `2δ₀` IS the
sign and you ducked it."* **Not sustained.** `2δ₀` is a defect-plane weight, not a coefficient on the
log-det quadratic; promoting it would need an owned iso onto the condensation potential, which is exactly
the unowned-iso wall (same as R4). The burn record (`20/20 random, NOT forced`) is a positive owner
assertion that the sign is external, not mere absence. No sign manufactured — the anti-over-claim
constraint is honored. ACCEPT.

**R3 (winding PRIM).** *Kill attempt: "the order `W(e)<W(μ)<W(τ)` + `m₀·t₀=1` secretly fix `a`, so your
PRIM smuggles the metric."* **Not sustained.** The order holds for ALL `a>1` (R3, parameter-free), so it
imports nothing about `a`. `m₀·t₀=1` fixes the mass NORMALISATION (`m₀=(12/5)φ²`), not the per-generation
winding section; `a` is a free `Rat` on disk (`1<a` only) and the non-uniqueness witness `(1,2,3)` vs
`(1,2,5)` (R3) proves two admissible sections share order and differ in value. The PRIM's INPUT is `a`
(external), OUTPUT is only the order (owned) — the metric is NOT claimed derived. ACCEPT.

**R4 (branch-fixing PRIM).** *Kill attempt: "the zone carrier owns the third generation (`outerD13`), so
the row IS owned and your PRIM is redundant."* **Not sustained.** EXISTENCE of the third zone is owned;
the LABELLED ROW `branch-orbit → (e,μ,τ)` is not — it needs a `2→3` assignment that is proven impossible
in-carrier (pigeonhole, R4) and the zone-3 is RANK-ONLY (`csv:460`), so even the receiving carrier does
not canonically label. The PRIM imports the label, not the existence. ACCEPT.

**Skeptic verdict: NO-KILL on any of the four.** One correction logged (T4's carrier-absence statement is
too strong — an owned non-commuting object exists on the `ZMod 44` carrier; the real wall is the
three-property trap). No verdict smuggles the Higgs sign, the winding value, or the lepton row. The two
SHARP-EXTERNAL-PRIM typings (R3, R4) have exact INPUT/OUTPUT and are the terminal-passport closures the
task defined as acceptable.

---

## Proposed row-notes (PROPOSALS ONLY — no CSV/book edits made)

**`D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`** (append):
> [CLOSE-HIGGS-WINDING] W1 sharpened to the **three-property trap** on the exact `ZMod 44` return
> carrier `M₂(ZMod 44)`: a Higgs `Q0` needs (i) idempotent ∧ (ii) `[T,Q0]≠0` ∧ (iii) owned/frozen.
> CORRECTION to `CLOSE_MATTER` T4: an owned frozen non-commuting object DOES live on this carrier —
> `FrozenSU2_X=!![0,1;1,0]` (`HiggsScalarProjectorConstructive.lean:32`), `[T,X]≠0`, `X∉{a•1+b•T}` — so
> the wall is NOT carrier-absence. But `X²=I₂` (involution, not idempotent); the 8 present-core
> idempotents all commute with `T`; non-commuting idempotents exist (3476/3484) but are unowned choices.
> Owned material realises any two legs, never all three. Missing object: a frozen idempotent
> `Q0∈M₂(ZMod 44)` with `[T,Q0]≠0`, derived. Verified `close_higgs_winding_check.py` (R1a–R1g).

**`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`** (append):
> [CLOSE-HIGGS-WINDING] W2 sign confirmed external, NOT manufactured. Sharp typing
> `PRIM-HIGGS-SSB-SIGN`: INPUT = external negative-sign datum (double-well/`μ²<0`); OUTPUT = flips the
> owned `z²≥0` log-det coefficient to the SSB sign. Absent the import the coefficient is a nonnegative
> square (no in-scene double-well). Matches the burn record (SSB sign `20/20 random, NOT forced`).

**`D0-GEN-MASS-001`** (append):
> [CLOSE-HIGGS-WINDING] Winding metric typed `PRIM-WINDING-METRIC` (= `PRIM-TORUS-PARAMETER-a`):
> INPUT = torus parameter `a>1` (`TorusParameter` carries only `a:Rat, 1<a`; `a=φ⁵` is a passport
> INSTANTIATION per `TorusCore13GeometryOrigin.lean:12`, never forced); OUTPUT = the owned parameter-free
> radial order `W(e)<W(μ)<W(τ)` (`torusShell_radius_strictMono`). Metric non-unique ((1,2,3) vs (1,2,5)
> share order, differ value). Order owned, metric = passport. Verified `close_higgs_winding_check.py` (R3).

**`D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001`** (append):
> [CLOSE-HIGGS-WINDING] Row typed `PRIM-LEPTON-BRANCH-FIXING-OPERATOR`: INPUT = branch→generation
> assignment (the `X5-LEPTON-CONTRACT` third-row HYP); OUTPUT = the owned in-carrier wall
> `numBranches=2 < 3=numGenerations` + the three pigeonhole no-gos (`LeptonBranchFixingNoGo`), and the
> RANK-ONLY receiving zone-3 (`csv:460`). The third generation EXISTS (`outerD13`); only its labelled
> coupling to the branch data is the external PRIM. Verified `close_higgs_winding_check.py` (R4).

---

## FINAL — per-residue verdict

| Residue | Verdict |
|---|---|
| **Higgs W1** (non-commuting frozen `Q0` on `ZMod 44`) | **FAILED-BOUNDARY**, sharpened to the three-property trap; T4 carrier-absence statement CORRECTED (`FrozenSU2_X` is an owned non-commuting object on the carrier, but an involution not an idempotent) |
| **Higgs W2** (SSB sign) | **SHARP-EXTERNAL** — `PRIM-HIGGS-SSB-SIGN` (INPUT: negative-sign datum; OUTPUT: flips `z²≥0`); sign NOT manufactured |
| **Winding metric** (`a`) | **SHARP-EXTERNAL-PRIM** — `PRIM-WINDING-METRIC` (INPUT: `a>1`; OUTPUT: owned order `W(e)<W(μ)<W(τ)`) |
| **Branch→generation ROW** | **SHARP-EXTERNAL-PRIM** — `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` (INPUT: row assignment; OUTPUT: owned `2<3` pigeonhole wall) |

**Skeptic verdict: NO-KILL.** 0 no-gos drop. Two Higgs walls confirmed external (W1 sharpened, W2 not
manufactured); two winding residues typed as SHARP-EXTERNAL-PRIM with exact I/O — the terminal-passport
form of closure the owner accepts. No Higgs sign, winding value, or lepton row manufactured.
