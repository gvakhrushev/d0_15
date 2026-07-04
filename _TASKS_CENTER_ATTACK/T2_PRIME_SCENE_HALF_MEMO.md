# T2′ SCENE-HALF MEMO — both remaining nails have candidate owners (DRAFT, no status claimed)

**Author:** chief researcher. Status: DRAFT; candidate closure of the two nails left by
`TASK_W8_REPORT.md`; submitted for adversarial review; edits no registry row. Computational leg:
`w8_holomorph_check.py` (14 checks, RESULT: PASS, exit 0, reachable negative control).

## Nail 2 (scene half of P_iso): paid at the definitional level

The scene-side generation triple is not merely "some S₃-set of size 3":

1. `GenerationPhasonMode := PhasonMode := D0.Geometry.TorusShell` — **definitional** abbrev chain
   (`PhasonStrainGenerations.lean:25,38`). Generations ARE torus shells by definition, in owned Lean.
2. `TorusShell = {innerD9, coreD11, outerD13}` (`TorusCore13GeometryOrigin.lean:59–63`) — the shells
   are (a) radially ordered by owned radii `inner = 1 < core = (a+1)/2 < outer = a`, and (b)
   zone-degree-labeled (D9/D11/D13). Note `inner ≡ 1` is **parameter-independent** — the unit shell.

So "generation mode" is already a scene-geometric object with owned order and owned zone labels; the
scene half of P_iso reduces to: torus shells ↔ Q₈ Fourier blocks.

## Nail 1 (the matching rule): type-keyed, not order-keyed — and each leg has an owner

Both triples carry three pairwise-distinct **owned types**; matching by type is then unique — no S₃
freedom, no residual bit, no order-matching convention needed.

**Zone types (owned, BOOK_01 §01.8):** the three zones exist because there are exactly three
structural necessities — `9 = defect/base` (born from `Ω₈ ⊔ {ω₀}`), `11 = memory` (the torus),
`13 = shell` (terminal roles).

**Block types (verified exact, `w8_holomorph_check.py` typing checks):** read off the holomorph
module (L_i, α) on ℂ[Q₈]:
- `E₀` — the unique block fixed by BOTH actions (translation and automorphism);
- `E₄` — the unique block where translation has order exactly 4 (`L₋₁ = −1` there; `+1` elsewhere);
- `E₃` — the unique block whose three internal idempotents are nontrivially 3-cycled by α; and by the
  **forced role dictionary** `A↦1, B↦i, C↦j, D↦k` (§01.7.1A, status THEOREM) the three character
  kernels `⟨i⟩,⟨j⟩,⟨k⟩ = ⟨B⟩,⟨C⟩,⟨D⟩` — the E₃ triple IS the terminal-role triple `{B,C,D}`
  (already so named in `TerminalReturn.lean`: carrier `r_B, r_C, r_D`).

**The type-keyed matching and its per-leg witnesses:**

| zone (type) | block (type) | witness of the leg |
|---|---|---|
| 9 — defect/base, hosts `Ω₈⊔{ω₀}`; unit shell `inner ≡ 1` | E₀ — both-fixed, unramified, unit isotype | "Q₉↔E₀ (rank 1, unramified)" (`Q8Terminal.lean` header); electron = terminal calibration register (§04.7.1); parameter-free ↔ action-fixed |
| 11 — memory/torus | E₄ — unique translation-order-4 block | THE 04.8.L.1 (BOOK_04 §04.8): the exponent-1/4 lepton is "localized in the memory zone (the torus, address 11)" — an owned THE row welding branch 1/4 to zone 11 |
| 13 — shell/terminal roles | E₃ — the `{B,C,D}` character triple | forced dictionary §01.7.1A + the `r_B,r_C,r_D` carrier of the 3-cycle |

**Consequence if this survives review:** P_iso is fully paid — Q₈-internal half by the holomorph
module (`TASK_W8_REPORT.md` Charge B), scene half by the definitional shell identity plus the
type-keyed matching. The postulated content of `D0-X5-LEPTON-CONTRACT-001` then empties: existence
(E₀, internal), assignment (type-keyed, unique). The third-generation "genuinely external" datum
would become eliminable.

## Named obligations before any status motion (honest list)

1. **Adversarial review of the type-keying itself.** The sharpest attack: is "match by type" a rule
   the corpus owns, or a third convention besides order-matching? Defense sketch: with three
   pairwise-distinct owned types per side, any matching that respects typed provenance is unique —
   a which-type-goes-where register would be exactly an M1-banned catalog; but this must be written
   in the DEF-0.2.2 schema and reviewed against §05.8.R.
2. **Owner status of the zone typing** {defect, memory, shell} — prose-owned in BOOK_01 §01.8;
   locate or create its Lean/cert owner.
3. **THE 04.8.L.1's localization premise** ("muon in memory zone 11") — cite its own derivation chain
   precisely; if the localization is narrative rather than derived, the 11↔E₄ leg drops to a named
   assumption.
4. **Minting**: promote `w8_holomorph_check.py` (14 checks) into a proper cert + a Lean module
   (`native_decide`-checkable: all matrices are exact ℚ literals), per `VERIFIED_CLOSURE_PROTOCOL.md`
   — scout, owner, negative controls, gate. The chain currently sits at the CONDITIONAL-EXTENSION
   level of `UnifiedTheorem.lean` and inherits that status until promoted.
5. **Tau leg sanity**: the muon Lucas row L₁₁+L₄ = 206 welds (11,4); no analogous owned (13,3) Lucas
   row exists (τ mass ratio ≠ L₁₃+L₃ — checked, 525 vs ~3477) — the 13↔E₃ leg rests on the role
   dictionary, NOT on a Lucas row; do not claim a Lucas symmetry that is not there.
