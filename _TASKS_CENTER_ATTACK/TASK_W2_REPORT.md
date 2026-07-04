# TASK W2 — 8-point witness monodromy: construction and invariant re-run (report)

**Date:** 2026-07-02  **Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`
**Scope:** PURELY COMPUTATIONAL / CONSTRUCTIVE. This task builds the witness-extended monodromy
`σ̂ = σ_A ⊕ id` on 8 points and re-runs every invariant used by the lepton no-go chain. It does
**NOT** decide whether the 8-point extension is *forced* — that is TASK W3 + the architect's memo.

All deliverables live inside `_TASKS_CENTER_ATTACK/`. No file outside this folder was edited. All
decisions use exact integer / rational arithmetic; no floats enter any decision. No
"confirmed/derived/forced/closed" promotion language (BOOK_00 §00.8 / §00.9).

The carrier under construction:
```
σ̂ = (0 1 2 3)(4 5 6)(7)   on Fin 8,   index map ![1,2,3,0,5,6,4,7]
   = σ_A  ⊕  id_{ω₀},   σ_A = (0 1 2 3)(4 5 6) on Fin 7,  ω₀ = 7 (the witness, core rule Ω₈+ω₀=V₉).
cycle type (4,3,1),  orbits {4,3,1},  order lcm(4,3,1) = 12.
```

---

## Deliverables (all in `_TASKS_CENTER_ATTACK/`)

| File | Steps | What it does |
|---|---|---|
| `w2_cycle_type_enum.py` | 1 | Exact enumeration of all partitions of 7 and 8 + lcm; uniqueness of order-12 cycle type. |
| `w2_resolvent_8point.py` | 2, 3, 4 | Exact resolvent invariants on 8 points: fixed points, orbits, order, `det(I−zÛ)`, label-free exponents, exponent-0 branch. |
| `w2_freedom_and_cert_rerun.py` | 3, 4 | Conjugacy-class classification (residual freedom, 7pt-vs-8pt) + exact re-run of the Green-resolvent cert on 8 points, with reachable negative controls. |
| `LeptonWitnessBranchConstruction.lean` | 5 | Lean skeleton mirroring `LeptonBranchFixingNoGo.lean`; compiles standalone against Mathlib. |
| `TASK_W2_REPORT.md` | 6 | This report. |

Reproduce:
```
cd /Users/grigorijvahrusev/Downloads/d0_15/_TASKS_CENTER_ATTACK
python3 w2_cycle_type_enum.py          # PASS_W2_STEP1_CYCLE_TYPE_UNIQUENESS
python3 w2_resolvent_8point.py         # PASS_W2_STEPS_2_3_4_RESOLVENT_8POINT
python3 w2_freedom_and_cert_rerun.py   # PASS_W2_STEP3_STEP4
# Lean (uses the repo's already-built Mathlib; does NOT modify 09_LEAN_FORMALIZATION/):
cd /Users/grigorijvahrusev/Downloads/d0_15/09_LEAN_FORMALIZATION
lake env lean ../_TASKS_CENTER_ATTACK/LeptonWitnessBranchConstruction.lean   # exit 0, no errors
```
Environment: python3 3.9.6 (no 3.10+-only APIs used); Lean 4.30.0 via the repo toolchain (default
elan is 4.31.0; `lake env` selects the pinned 4.30.0 automatically).

---

## VERIFIED (computed, exact)

### Step 1 — cycle-type uniqueness (`w2_cycle_type_enum.py`)
- S₇: 15 partitions; the **unique** order-12 cycle type is `(4,3)`. (Re-checks the frozen no-go premise.)
- S₈: **22** partitions; the **unique** order-12 cycle type is `(4,3,1)`.
- Adversarial cross-check: order 12 = lcm requires **both** a part divisible by 4 and a part divisible
  by 3 (no single part ≤ 8 is divisible by 12). With total 8 the only fit is `4 + 3 + 1`. The
  structural argument reproduces the enumeration exactly → **(4,3,1) is unique**.
- Consequence: the resolvent-invariant argument of the 7-point no-go carries over **verbatim** to
  8 points — the invariants pin the cycle *type*.

### Step 2 — resolvent invariants on 8 points (`w2_resolvent_8point.py`)
- **Fixed points:** exactly one, `ω₀ = 7`. **Orbits:** `{(0 1 2 3), (4 5 6), (7)}`, sizes `{4,3,1}`.
- **Order exactly 12:** `σ̂¹² = id`, and both proper divisors fail: `σ̂⁴ ≠ id`, `σ̂⁶ ≠ id`.
- **`det(I − z·Û) = (1−z)(1−z³)(1−z⁴)`** — verified **three independent ways**, all exact:
  1. product over cycles `∏ (1 − z^{len})` (integer coefficients),
  2. Laplace cofactor determinant of the 8×8 matrix over `ℤ[z]` (independent code path),
  3. Fraction (exact rational) Gaussian elimination of `I − z·Û` at 5 rational points `z ∈ {0, 1/2, 9/10, −2/5, 3}`.
  Expanded: `det = 1 − z − z³ + z⁵ + z⁷ − z⁸`.
- **Non-pole domain nonempty:** `det|_{z=0} = 1 ≠ 0`, so `Ĝ(0) = (I − 0·Û)^{-1} = I` exists; pole
  set `{z=1} ∪ {z³=1} ∪ {z⁴=1}` is finite (cofinite non-pole domain).

### Step 3 — residual freedom, and 7pt-vs-8pt comparison (`w2_freedom_and_cert_rerun.py`)
- **One conjugacy class.** Type `(4,3,1)` is a single S₈ class of size `8!/(4·3·1) = 3360`; a
  brute-force scan of all `8! = 40320` permutations counts exactly 3360, and **every** one has order
  12 and the same `det(I−zÛ)`. So the three orbit *sizes* — hence the resolvent invariants — are
  class functions, invariant under relabeling.
- **Sizes pairwise distinct** `1 ≠ 3 ≠ 4`, so the **size-keyed exponent map is label-free**:
  `{size 1 ↦ 0, size 4 ↦ 1/4, size 3 ↦ 1/3}` needs no choice of underlying points and no
  cycle-vs-cycle labeling. The three exponents `{0, 1/4, 1/3}` are pairwise distinct in ℚ.
- **Residual freedom, stated exactly:**
  - (i) which underlying points carry the 4-/3-/1-cycle = pure relabeling (one S₈ class) → no
    invariant effect;
  - (ii) the size-1 orbit is the **unique** fixed point, so the exponent-0 slot is canonically the
    witness — **not** swappable with 1/4 or 1/3;
  - (iii) which physical name μ vs τ attaches to `1/4` vs `1/3` = external passport naming
    (2 orbits → still `2! = 2` name-choices), **not** carrier data.
- **Verdict vs the 7-point σ_A/σ_B freedom.** The witness does **not** touch the relabeling
  freedom (both carriers already have their cycle type as a single conjugacy class — expected and
  harmless; the "σ_A vs σ_B" pair on 7 points are two members of that one class). What the witness
  changes is the **orbit count 2 → 3**: the size-keyed exponent map now supplies **three** distinct
  branches `{0, 1/4, 1/3}` for **three** generations, and the exponent-0 branch is a *distinguished*
  (unique-fixed-point) slot. The 7-point R4 pigeonhole — 2 orbits `< 3` generations, so the third
  branch→generation row is underdetermined — is precisely what the extra orbit removes **on this
  carrier**. The μ/τ ↔ {1/4, 1/3} naming remains external.
  So on the 8-point carrier the witness **reduces/removes** the R4-style underdetermination of the
  third branch; it does **not** remove the external passport naming freedom (ii/iii).

### Step 4 — Green-resolvent cert re-run on 8 points (`w2_freedom_and_cert_rerun.py`)
- **Located** the cert: `05_CERTS/vp_lepton_finite_green_resolvent_owner.py`, owner
  `D0-LEPTON-SHELL-GREEN-RESOLVENT-001` / cited as `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001`.
  Input format: a fixed cyclic cover `U_eff = diag(P4,P3)` (7×7 permutation), asserting order 12,
  invertibility, `det(I−zU)=(1−z⁴)(1−z³)`, nonempty non-pole domain (z=0), plus three reachable
  negative controls. **The original cert uses numpy floats with a `1e-9` tolerance.**
- **Adapted to 8 points, EXACT.** Same `STRUCTURE_FIXED_BEFORE_NUMBER` discipline: cover
  `Û = diag(P4,P3,P1)` fixed first; order 12, invertibility (`det Û = −1`, computed as an exact
  permutation sign, no float), and `det(I−zÛ) = (1−z)(1−z³)(1−z⁴)` as an **exact polynomial
  identity** (upgraded from the original float spot-checks), non-pole domain nonempty (`z=0`, exact).
- **The adapted question answered:** the size-1 fixed orbit `{7}` contributes the simple factor
  `(1 − z¹) = (1 − z)` to the resolvent determinant — a **well-defined regular / unramified
  (exponent-0) local branch at the fixed point ω₀**, alongside the `1/4` (4-cycle) and `1/3`
  (3-cycle) branches. Branch exponents on 8 points = `{0, 1/4, 1/3}`, three branches for three
  generations. **The machinery adapts cleanly and yields a clean exponent-0 branch.**
- **Reachable negative controls all fire** (the cert can still return FAIL):
  - `FAIL_BRANCH_PROJECTOR_AS_UNIQUE_REJECTED` — canonical branch projectors stay no-go-bounded;
  - `FAIL_MEASURED_MASS_AS_INPUT_REJECTED` — a measured mass ratio is external, not internal;
  - `FAIL_EMPTY_DOMAIN_REJECTED` — empty non-pole domain caught (z=0 witness, exact det=1);
  - `FAIL_FORCING_CLAIM_REJECTED` (**new, W2-specific**) — claiming this construction *proves* the
    8-point carrier is forced is rejected: this cert only builds the branch on a *given* carrier.

### Step 5 — Lean skeleton (`LeptonWitnessBranchConstruction.lean`)
- **Compiles standalone against Mathlib, exit code 0, no errors, no `sorry`, no warnings**
  (type-checked via `lake env lean` using the repo's already-built Mathlib; the file was **not**
  placed in `09_LEAN_FORMALIZATION/` and no repo file was modified).
- Mirrors `LeptonBranchFixingNoGo.lean` style. Defines `sigmaHat : Fin 8 → Fin 8 := ![1,2,3,0,5,6,4,7]`
  and `omega0 := 7`. Proves:
  - `unique_fixed_point : ∀ i, sigmaHat i = i ↔ i = omega0` (`decide`) and
    `exists_unique_fixed_point : ∃! i, sigmaHat i = i` (explicit witness + `decide`);
  - `orbit_count_three : orbitSizes.length = 3` (`decide`);
  - `orbit_sizes_pairwise_distinct : 4≠3 ∧ 4≠1 ∧ 3≠1` (`decide`) and
    `branch_exponents_distinct : 0≠1/4 ∧ 0≠1/3 ∧ 1/4≠1/3` in ℚ (`norm_num`);
  - `sigmaHat_pow12`, `sigmaHat_not_pow4`, `sigmaHat_not_pow6` → `order_exactly_twelve` (`decide`);
  - `branchGenEquiv : Fin 3 ≃ Fin 3` with `exists_branch_gen_bijection` — the explicit
    `Branch(3) ≃ Gen(3)` full-row bijection (contrast: the 7-point no-go proves `Branch(2) ≃ Gen(3)`
    is **impossible**);
  - `witness_branch_construction` bundling all of the above.

**Line-by-line justification of each `decide` / `norm_num` claim** (independently confirmed by the
Python scripts, so valid even without a Lean toolchain):

| Lean claim | Tactic | Why it holds (finite/exact) |
|---|---|---|
| `witness_fixed : sigmaHat 7 = 7` | `decide` | `![…]` at index 7 is `7`. |
| `unique_fixed_point : ∀ i, sigmaHat i = i ↔ i = 7` | `decide` | 8 finite cases; only `i=7` maps to itself (0↦1,1↦2,2↦3,3↦0,4↦5,5↦6,6↦4 all move). |
| `exists_unique_fixed_point : ∃! i, …` | witness `7` + `decide` | existence = `witness_fixed`; uniqueness = the ← half of `unique_fixed_point`, a finite check. (`∃!` itself is not `Decidable`, so the witness is given explicitly.) |
| `orbit_count_three : orbitSizes.length = 3` | `decide` | `orbitSizes = [4,3,1]`, list length 3 by computation. |
| `orbit_sizes_pairwise_distinct : 4≠3 ∧ 4≠1 ∧ 3≠1` | `decide` | ℕ literal inequalities. |
| `branch_exponents_distinct : 0≠1/4 ∧ 0≠1/3 ∧ 1/4≠1/3` | `norm_num` | exact ℚ arithmetic (`decide` is unsuited to ℚ division; `norm_num` evaluates exactly). |
| `sigmaHat_pow12 : ∀ i, sigmaHat^[12] i = i` | `decide` | `Function.iterate` 12× is a finite composition on `Fin 8`; each of 8 inputs returns to itself (lcm(4,3,1)=12). |
| `sigmaHat_not_pow4 : ∃ i, sigmaHat^[4] i ≠ i` | `decide` | e.g. the 3-cycle: `sigmaHat^[4] 4 = 5 ≠ 4`. |
| `sigmaHat_not_pow6 : ∃ i, sigmaHat^[6] i ≠ i` | `decide` | e.g. the 4-cycle: `sigmaHat^[6] 0 = 2 ≠ 0`. |
| `numBranches_eq_three`, `numBranches_eq_numGenerations` | `decide` | `numBranches = orbitSizes.length = 3 = numGenerations`. |
| `exists_branch_gen_bijection : ∃ e:Fin 3≃Fin 3, Bijective e` | term | `Equiv.refl (Fin 3)` is bijective by `Equiv.bijective`. |

---

## OPEN (this task does NOT decide)

**The forcing question is untouched.** Everything above is a *construction on a given carrier*.
Nothing here shows the 8-point carrier is the canonical / forced one.

Explicitly, this task does **NOT** show:
1. **That the 8-point carrier is forced.** Whether the witness rule (Ω₈+ω₀=V₉, BOOK_00 §00.5)
   *forces* the extension `σ̂ = σ_A ⊕ id` — as opposed to merely *permitting* it — is TASK W3 +
   the architect's forcing memo. This task assumed the extension and checked consistency only.
2. **That the 7-point carrier is wrong.** The 7-point no-go (`LeptonBranchFixingNoGo.lean`,
   `LeptonBranchAssignmentNoGo.lean`) remains **true on its own carrier**: on 7 points there is no
   fixed point, hence no in-carrier exponent-0 branch, and 2 orbits `< 3` generations. This task
   neither references nor modifies those files. The 8-point result is a *different carrier*, not a
   refutation of the 7-point one.
3. **That the extension by exactly one point (not two, not a different fixed structure) is unique.**
   We verified `(4,3,1)` is the unique order-12 *cycle type* on 8 points, but a carrier could in
   principle have a different point count or a different rule; ruling those out is provenance/forcing
   work (W3), not done here.
4. **That the electron = witness identification is physical.** Assigning the exponent-0 branch to the
   electron generation is an *interpretation* of the fixed point; the μ/τ ↔ {1/4, 1/3} naming remains
   external passport data. No PDG mass enters; decimals stay EFT/IR.
5. **Any promotion of status.** No cert status, claim, or ledger entry was edited. The re-run cert
   in `w2_freedom_and_cert_rerun.py` is a *construction* cert with a reachable
   `FAIL_FORCING_CLAIM_REJECTED` control precisely so it cannot be misread as a forcing proof.

---

## One-line verdicts (for the orchestrator)

- **(4,3,1) unique order-12 type in S₈?** YES — exhaustively (22 partitions; single order-12 type),
  with an independent structural cross-check. The 7-point invariant argument carries over verbatim.
- **Residual freedom vs 7-point σ_A/σ_B?** The witness leaves the (harmless) relabeling freedom
  unchanged but **reduces/removes** the R4-style third-branch underdetermination by raising the orbit
  count 2 → 3 (three distinct branches for three generations, exponent-0 slot distinguished). The
  external μ/τ naming freedom is unchanged. — CONSTRUCTIVE relief on this carrier only; NOT forcing.
- **Green-resolvent exponent-0 branch?** YES — the size-1 fixed orbit gives the simple factor
  `(1−z)`, a clean regular/unramified exponent-0 branch alongside `1/4` and `1/3`; the machinery
  adapts exactly (upgraded to exact arithmetic) and all negative controls still fire.
- **Lean skeleton?** COMPILED standalone against Mathlib (exit 0, no `sorry`/errors), and additionally
  justified line-by-line.
