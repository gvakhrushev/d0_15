# ATTACK: Higgs W1 as a degree-2 / P-ABELIAN corollary

**Scope.** Memo-only. No registry edit, no 053040, no commit. Target = the **W1 wall**
of `D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001` (the commutativity /
conjugation-orbit wall). **W2 (the SSB log-det double-well sign `z²≥0`,
`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`) is UNTOUCHED and stays external.**

Check: `_TASKS_CENTER_ATTACK/attack_higgs_w1_check.py` — BASE 11/11 PASS, 3 mutants each KILL.

---

## 1. Thesis

W1 is the wall

> **W1:** an OWNED idempotent projector on the return-carrier (2×2 over `ZMod 44`)
> commutes with the return operator `T` — so no owned frozen projector supplies the
> non-commuting `Q₀` a finite condensation needs.

The attack claim: **W1 is a corollary of the degree-2 / P-ABELIAN structure of the
present-core**, not an independent "three-property trap." The mechanism:

1. The present-core is `ZMod44[T] = {a·1 + b·T}` — a **2-dimensional commutative**
   algebra, because `T` has a **quadratic** minimal polynomial `T² + T − 1 = 0`
   (`T³ = 2T − 1` reduces into `span{1,T}`; the P-DEGREE2-EXHAUSTION root, T-carrier form).
2. In a commutative algebra every idempotent is a **spectral projection = a polynomial
   in the generator**, hence commutes with `T`. Over `ZMod 44`, `√5 ∈ {7,15,29,37}`
   exists, so there are exactly **8** such idempotents (`0, I` + 6 nontrivial spectral
   projections) — the wall is nontrivially `T`-specific, not the vacuous `{0,I}` case.
3. Therefore: **in-core idempotent ⟹ commutes with `T`** is a THEOREM of the abelian
   degree-2 core (with the converse: commuting idempotent ⟹ in-core). W1 is exactly this
   abelian-ness, restricted to the objects that are actually owned on the carrier.

So W1 = "the present-core is `ℂ[T]`, 2-dim commutative; owned on-carrier idempotents ⊆
`ℂ[T]` ⟹ they commute with `T` ⟹ no owned non-commuting idempotent."

---

## 2. Evidence (R1–R9, from the check)

All arithmetic is exact integer mod 44 — no float on any load-bearing fact.

| # | What it establishes | Grade |
|---|---|---|
| **R1** | `T` has toral order 30 (return operator, not period-44). | context |
| **R2** | min-poly of `T` is **quadratic**: `T²+T−1=0`; `T³=2T−1` reduces into `span{1,T}`. **Degree-2 present-core.** | **THEOREM** (owned; = P-DEGREE2-EXHAUSTION root) |
| **R3** | present-core `ZMod44[T]` is **commutative** (every `a·1+b·T` commutes with `T`; = `tPoly_commutes`). | **THEOREM** (owned Lean) |
| **R4** | the present-core has exactly **8** idempotents, all spectral projections = polynomials in `T`, all commuting. | THEOREM (degree-2 + √5 exists) |
| **R5** | **THE DEGREE-2 EQUIVALENCE:** of all 3484 idempotents of `M₂(ZMod44)`, exactly 8 commute with `T`, and those 8 are exactly the present-core idempotents. So **idempotent ∧ commutes-with-T ⟺ in-core**. | **THEOREM** (exhaustive) |
| **R6** | three-property trap re-derived: no owned named object is simultaneously idempotent ∧ non-commuting; the only owned named idempotent is `I` (in-core). | evidence (enumeration of named owned) |
| **R7** | **THE CRUX:** owned ON-CARRIER idempotents ⊆ present-core (only `I` is idempotent among named owned; `I ∈ core`). | **EVIDENCE-ONLY** — see §3 |
| **R8** | negative control: `diag(1,0)` is idempotent, NOT in core, does NOT commute with `T` — it **would** break W1 if owned. It is unowned (the free-choice `Qnc` witness). | THEOREM (the wall is a real gate, not vacuous) |
| **R9** | scope: the meson support projector is an owned idempotent but OFF the `T`-carrier (`Matrix(MesonCarrier E Gen) Rat`, not 2×2/`ZMod44`) — "commutes with `T`" is untyped for it; out of W1's scope. | scope-carve |

The three mutants confirm the check discriminates on the load-bearing data:
`break_degree2` (scalar `T`) kills R2/R4/R5; `break_frozen_x` (an owned object made
idempotent+non-commuting) kills R6; `break_owned_idem_offcarrier` (a hand-picked non-core
idempotent injected as owned) kills **R7** — i.e. the kill is genuinely gated on
"owned on-carrier ⊆ core."

---

## 3. The load-bearing grade question (the CRUX)

The check settles one half by exhaustion and **cannot** settle the other:

- **PROVEN half (R5, theorem-grade).** *in-core idempotent ⟹ commutes with `T`* — and
  its converse *commuting idempotent ⟹ in-core*. This is the degree-2/abelian content,
  exhaustively verified (8 = 8) and owned in Lean as `tPoly_commutes`.

- **NOT-forced half (R7, the crux).** W1 needs *OWNED idempotent ⟹ in-core* (so that the
  proven half applies to it). The check verifies this only for the **enumerated named
  owned objects** — a finite list on which the sole idempotent is `I`. The question the
  check cannot answer: is *OWNED idempotent ⟹ in-core* **forced** (a theorem — every owned
  projector IS a present-core projector by some reason), or is it **evidence-only** (all
  named owned idempotents happen to be in-core, no exhibited counterexample, but nothing
  forces a *future* owned idempotent to be in-core)?

### Reading the owned anchors verbatim

**`tPoly_commutes`** (`HiggsCondensationPresentCoreMaximalityNoGo.lean:25–29`):

> *Every present-core (polynomial-in-`T`) projector commutes with `T`: for all `a b :
> ZMod 44`, `a•1 + b•T` commutes with `T`.*
> `theorem tPoly_commutes (a b : ZMod 44) : Commute T (a • (1 : …) + b • T) := …`

This quantifies over `a b` — i.e. **over the polynomial class `{a·1+b·T}` by
construction**. It proves *polynomial-in-T ⟹ commutes*. It does **NOT** say *owned ⟹
polynomial-in-T*. It is the PROVEN half of §3, nothing more.

**The maximality no-go's own docstring** (`…MaximalityNoGo.lean:15–18`):

> *A non-commuting `Q₀` exists as a matrix (witness `Qnc = !![1,0;0,0]`, `[T,Qnc] ≠ 0`),
> but it is NOT a polynomial in `T` — i.e. NOT a present-core frozen object; supplying it
> is a NEW independently-forced primitive `(U, Q₀, Π_H)` (extension), not a present-core
> theorem.*

So the corpus's **own** framing is: a non-core (non-commuting) idempotent-family object
is a *possible object* that merely is **not owned/frozen** — it lives "only in a
central-extension/archive layer." Owned-ness excludes it by **fiat of the frozen-input
list**, not by a forcing that no owned object could ever be a non-polynomial idempotent.

**`D0-P-ABELIAN-001`** (registry row 558):

> *every present-core projector is a polynomial `a*1+b*T` and commutes with `T` (Lean-owned
> `tPoly_commutes`, exhaustive over all 44²=1936 polynomials); hence the present-core is the
> MAXIMAL T-commutative (abelian) sub-object. Non-commutativity is extremally excluded: a
> witness `Qnc` with `[T,Qnc]!=0` exists (`Qnc_not_commute`) but lies OUTSIDE the core (not
> a polynomial in `T`) — only in a central-extension/archive layer.*

"MAXIMAL T-commutative sub-object" is maximality **within the algebra** — the polynomial
class is the largest commuting sub-object. It is established by exhaustion **over the 1936
polynomials**, i.e. over the core itself. It does **not** force an arbitrary future owned
projector to lie inside that class.

### Verdict on the grade

**The crux is EVIDENCE-ONLY, with a proven forcing-half.**

- *in-core ⟹ commutes* (and its converse): **THEOREM** (R5 / `tPoly_commutes`, degree-2
  abelian, exhaustive). This is real and owned.
- *owned ⟹ in-core*: **EVIDENCE-ONLY**. No anchor forces it. `tPoly_commutes` proves the
  *polynomial* half; the maximality no-go explicitly treats a non-core idempotent
  (`Qnc = diag(1,0)`) as a *possible-but-unowned* object; P-ABELIAN-001's maximality is
  internal to the polynomial class. R7 is an enumeration over the named owned list (sole
  idempotent = `I`), and R8 shows the excluded object is excluded by being **unowned**,
  not by any structural impossibility.

Consequence: W1 is a **real structural explanation** — "the wall IS the degree-2
abelian-ness of the core, and every owned on-carrier idempotent observed so far sits
inside it" — but it is **NOT** a closed corollary in the strong sense (owned ⟹ commutes is
not theorem-forced end-to-end). The residual is exactly the standard D0 owner-gate:
*owned frozen on-carrier idempotents are, by the frozen-input list, present-core
polynomials* — an enumeration that stays open to a future owned non-polynomial idempotent
(none exists; none is forced not to).

---

## 4. Honest CRUX framing (one sentence)

W1 = [ THEOREM: in-core idempotent ⟺ commutes-with-`T`, degree-2 abelian, R5/`tPoly_commutes` ]
∘ [ EVIDENCE: every owned on-carrier idempotent is in-core, R7, enumeration over the frozen
list, no forcing against a future owned non-polynomial idempotent, R8 witness excluded only
by being unowned ]. The first factor is owned; the second is the crux and is evidence-only.

---

## 5. INDEPENDENT SKEPTIC (§05.8.R, kill-mandate)

Primary target: the crux grade (owned⊆core theorem-or-evidence), plus word-dressing and
trap(f) on the check. Kill-mandate: try to break the memo, then accept/repair in full.

**S1 — Crux over-grade attempt (the main line).** *Does any anchor secretly force
owned ⟹ in-core, which would upgrade to W1-CLOSED?* Read `tPoly_commutes` again: its
binder is `(a b : ZMod 44)` — the object is *constructed* as `a•1+b•T`, so it is a
polynomial by hypothesis. There is no lemma "`IsOwned Q → ∃ a b, Q = a•1+b•T`" anywhere
in the three anchors. The maximality no-go's own prose calls the non-core witness a
"NEW independently-forced primitive … not a present-core theorem" — i.e. it concedes the
non-core object is *possible*, excluded only by not being on the frozen list.
**NO-KILL of the memo; CONFIRMS the memo's EVIDENCE-ONLY grade.** An attempt to claim
theorem-grade here would be the over-claim; the memo already refuses it. ✓ accept.

**S2 — R5 "8=8 equivalence": sampled or exhaustive?** If R5 only *sampled* idempotents,
the "exactly 8 commute" equivalence would be evidence, not theorem, and the PROVEN half
would collapse. Checked: `all_idem = [Q for Q in itertools.product(range(M), repeat=4) …]`
— **full 44⁴ enumeration**, 3484 idempotents total, exactly 8 commuting, and those 8 =
the present-core idempotents. Re-ran independently: confirmed (3484 / 8). The PROVEN half
is genuinely exhaustive-theorem-grade over the carrier. **NO-KILL.** ✓

**S3 — trap(f): is R8's "would break W1" the SAME object the crux excludes?** If R8's
`diag(1,0)` were a different object from the Lean witness, the negative control would be
decorative. Checked: Lean `Qnc = !![1,0;0,0]` (`…MaximalityNoGo.lean:33`) = R8
`Qnc=(1,0,0,0)` = R7-mutant `diag10=(1,0,0,0)`. **One and the same object.** So the wall,
its owned witness, and the negative control are the identical `diag(1,0)` — the gate is
real and the exclusion is precisely "unowned," not "impossible." **NO-KILL; strengthens
the honest framing.** ✓

**S4 — word-dressing sweep.** Flagged phrases and adjudication:
- "corollary" — used only in the *conditional* verdict (§6), gated on the grade; the body
  says "real structural explanation, NOT a closed corollary." OK.
- "THE CRUX" / "THEOREM" tags in the R-table — R7 is tagged EVIDENCE-ONLY, R5/R2/R3 tagged
  THEOREM with owned-Lean citation; no bare "derived/forced/closed" applied to owned⟹core. OK.
- "maximal T-commutative" (quoted from P-ABELIAN-001) — memo explicitly reads it as
  *internal-to-the-polynomial-class* maximality, not a forcing on arbitrary owned objects.
  No smuggle. OK.
- W2 — named "UNTOUCHED / stays external" in the scope line and the table; no leakage. OK.

**S5 — scope smuggle (R9 meson).** Could the off-carrier meson projector be quietly
counted as a W1 counterexample or, worse, as *support* for owned⊆core? It is neither: it
is off-carrier (untyped `Commute T ·`), so it is carved OUT of W1's scope and contributes
to neither side. The memo files it as scope-carve only. **NO-KILL.** ✓

**Skeptic verdict: NO-KILL of the memo.** Every attack either confirmed the memo's stated
grade (S1, S3) or hardened a supporting leg (S2, S4, S5). The one thing the skeptic
*forbids* is upgrading the crux to theorem-grade — which the memo already declines.
**Repairs applied: none needed** (grade was already honest); S2/S3 facts folded into §3/§6.

---

## 6. FINAL VERDICT

**W1-EXPLAINED-NOT-CLOSED.**

- The crux *owned ⟹ in-core* is **EVIDENCE-ONLY** (enumeration over the frozen owned list;
  no anchor — not `tPoly_commutes`, not the maximality no-go, not P-ABELIAN-001 — forces a
  future owned on-carrier idempotent to be a polynomial in `T`; the excluded object
  `diag(1,0)` is excluded only by being *unowned*, R8/S3).
- Therefore W1 does **NOT** upgrade to an owned corollary and its NO-GO status does **NOT**
  flip. It remains the **empirical three-property trap**, now with a genuine structural
  *reason*: the degree-2 abelian core makes *in-core idempotent ⟺ commutes-with-T* a
  theorem (R5/`tPoly_commutes`, exhaustive), so the trap is not a coincidence — every owned
  on-carrier idempotent observed sits inside the abelian core.
- This is a **real structural explanation**, filed as a reading/annotation, not a closure.
- **W2 (log-det double-well sign) UNTOUCHED, stays external.** No status flip beyond what
  the grade earns (none).

### Proposed corollary-of row-note (annotation only — NO status change, NO W2 change)

For `D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001` (row 407), append to the
narrative (do **not** change status/lean_status/owner):

> W1-DEGREE2[2026-07-07, EXPLAINED-NOT-CLOSED, memo ATTACK_HIGGS_W1_DEGREE2_MEMO.md]: the
> commutativity wall W1 is structurally EXPLAINED by the degree-2/abelian present-core —
> *in-core idempotent ⟺ commutes-with-T* is theorem-grade (`tPoly_commutes` + exhaustive
> 8-of-3484, R5), i.e. corollary-of D0-P-ABELIAN-001 / D0-P-DEGREE2-EXHAUSTION-001 on that
> half. The remaining leg *owned on-carrier idempotent ⟹ in-core* is EVIDENCE-ONLY
> (enumeration over the frozen list; the non-core witness `Qnc=diag(1,0)` is excluded by
> being unowned, not by forcing), so W1 stays NO-GO / empirical three-property-trap, NOT
> upgraded to owned corollary. W2 (log-det sign, D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001)
> UNTOUCHED, external.

**Honest grade: W1-EXPLAINED-NOT-CLOSED.** The degree-2 abelian half is theorem-grade and
owned; the owned⟹in-core half is evidence-only; no closure, no status flip, W2 external.
