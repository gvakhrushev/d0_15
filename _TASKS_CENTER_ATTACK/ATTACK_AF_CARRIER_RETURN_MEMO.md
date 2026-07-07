# ATTACK — AF/vNext2 history-carrier via the OWNED four-role RETURN-recurrence D₋

**Status: MEMO-ONLY. No status flip. Do not touch 053040. No commit.**
**Front:** `PRIM-SCENE-HISTORY-REFINEMENT-RULE` / `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`
(3 inequivalent history families: all-walks W=15708, non-backtracking NB=14990, directed-edge 2|E|=718).
**Angle:** the owned four-role detector cycle requires a RETURN-recurrence role D₋; the
non-backtracking carrier is defined by forbidding immediate return; IF backtrack==D₋, NB is excluded.
**Verdict (this pass): PUN-KILLED (fallback SUGGESTIVE-TRANSFER, non-selecting).** The attack does
**not** select the carrier. Honest grade + row-note below. Compute: `attack_af_carrier_check.py`
(5 can-fail checks + 6 mutation tests, all green).

---

## 0. VERIFY-FIRST (±10, verbatim, line-checked 2026-07-07)

| anchor | verbatim | file:line |
|---|---|---|
| four roles | "a completed finite detector cycle requires four typed roles: normalization, conjugate coupling, forward recurrence and return recurrence" | `BOOK_01:715` |
| four roles (restate) | "Its four duties are normalization, conjugate coupling, forward recurrence and return recurrence" | `BOOK_01:1175` |
| D₋ obligation | "`D_-` breaks return/halt descent" | `BOOK_01:417` |
| D₋ role text | "`D_-` \| return branch self-return recursion \| no conjugate return / no closed cycle" | `BOOK_01:713` |
| D₋ operator | "`D_- = T_ψ² − T_ψ`" ; "`D_- : return branch recurrence operator`" | `BOOK_01:414`, `BOOK_02:425` |
| C₊/D₋ split | "the conjugate pair `φ,ψ` is exactly the two-sidedness of `C_+/D_-`" ; "path holonomy could be one-sided, which forbids the *closed* memory cycles that a history requires" | `BOOK_02:540` [THE 2.5.2.factor2] |
| Galois typing | "`C_+` and `D_-` are the recurrences of the conjugate pair `φ,ψ` exchanged by the nontrivial automorphism" (`D0-VIETA-GALOIS-ABCD-001`) | `BOOK_02:430` |
| three families | "all-walks, non-backtracking, and directed-edge families satisfy M1 but are inequivalent (depth-2 carriers 15708 != 14990; transfer dims 33 != 718)…Ihara–Bass links only their *spectra*, not the operator" | `BOOK_02:1291`, `:1303` |
| 718 = backtrack gap | "the E2 backtracking gap (`15708 − 14990 = 718`, bijection (a,b,a) ↔ directed edges)" | `BOOK_07:1789` |
| memory-return | "Memory requires a distinguishable return" ; a loop `γ` "whose frame code returns to its own configuration class, `c_{n+m} ≡_O c_n`" | `BOOK_06:187`, `:179` |
| *-involution | path `*`-algebra "with the involution `(·)*` induced by **path reversal**" | `BOOK_03:55`, `BOOK_02:1850` |

Arithmetic (exact, `attack_af_carrier_check.py`): degrees {24×9, 22×11, 20×13}, N=33,
W=Σd²=15708, NB=Σd(d−1)=14990, **W−NB=Σd=718=2|E|**, |E|=359 (prime), directed-edge=718.
Every quote confirmed at the cited line; every number recomputed and mutation-tested.

---

## 1. The argument as stated (memo THESIS)

1. The owned completed detector cycle **requires** four typed roles; the fourth is
   **return-recurrence D₋** (not optional): removing it "breaks return/halt descent" (`:417`),
   leaves "no conjugate return / no closed cycle" (`:713`).
2. The **non-backtracking** carrier NB is *defined* by forbidding the immediate return step
   (a,b,a). Its return-step count is **0** (`W−NB=718` return steps live only in W).
3. **IF** "walk backtrack step (a,b,a)" **==** "owned operator role D₋", **THEN** NB has zero
   D₋-returns ⟹ NB violates the owned four-role requirement ⟹ NB excluded ⟹ **all-walks W selected over NB**.

The whole attack hinges on the antecedent of (3). That is the pre-registered crux.

**Not the killed capacity route.** Prior forge `CLOSE_AF_PRIMITIVES §R3` tried "**capacity** CAP=718=W−NB
**selects** the carrier" and found it FALSE (718 is the *difference*, ∈ neither {W,NB}). This attack's
selector is the **return-ROLE requirement** (a property NB structurally lacks), not the value 718 being
a carrier. `check_not_capacity_route()` certifies the logical distinction: this route never claims
718∈{W,NB}; it uses CAP>0 only as the *witness* that NB drops return steps. **Confirmed distinct.**

---

## 2. SELF-ATT-1 (pre-registered PRIMARY crux): is walk-backtrack the same object as D₋?

**Grade: PUN-KILLED.** The corpus's "return" family and the walk-level "backtrack" are **different
objects**; the word "return" carries (at least) three distinct meanings, and none of the owned ones is
the immediate walk-backtrack that NB forbids.

### The three "returns" (all owned, all distinct)

**(R-op) D₋ = the operator return-recurrence.** `D_- = T_ψ² − T_ψ` (`BOOK_01:414`), "the recurrence of
the conjugate `ψ`" exchanged with C₊'s φ-recurrence "by the nontrivial automorphism" of ℚ(√5)
(`BOOK_02:430`, `D0-VIETA-GALOIS-ABCD-001`). The "two-sidedness of C₊/D₋" is the **Galois conjugate pair
φ,ψ** and the **path-reversal *-involution** (`BOOK_03:55`, `BOOK_02:1850`, `:540`). This is a *field /
operator / involution* object: forward-vs-conjugate *direction*, not a step on a specific edge. Its
scalar law is `p+p²=1` (the quadratic's two roots), owned entirely by BOOK_01/02's response calculus.
**It never references a graph walk at all** — it is defined before any history tower exists.

**(R-hist) [THE 06.2.A] memory-return.** A history requires a *distinguishable return*: a **loop γ of
any length m** whose frame code "returns to its own configuration class, `c_{n+m} ≡_O c_n`"
(`BOOK_06:179`), with holonomy `Hol_γ = c_{n+m}` and the bit = distinguishability of that return
(`:185`). This is a **closed cycle**, length arbitrary, defined by *returning to a class* — not by
immediate edge-reversal.

**(R-walk) backtrack.** The length-2 walk step (a,b,a): step out on edge b, step back on the same edge.
`W−NB=718` counts exactly these (bijection (a,b,a)↔directed edges, `BOOK_07:1789`). NB forbids **only
this**; it keeps all longer non-reversing closed loops.

### Why the identification (R-walk == R-op) FAILS

- **Type mismatch.** D₋ is an operator/field object (`T_ψ²−T_ψ`, conjugate recurrence, Galois-exchanged,
  reversal involution). Backtrack is a step in a graph walk on the history tower. D₋ is defined
  **upstream of and independently of** the history tower (BOOK_01/02); the tower families are a
  BOOK_06/02.15 construction. There is **no owned text** applying the operator D₋ to a walk step, nor
  identifying "the ψ-recurrence" with "reversing the last edge."
- **The owned "closed cycle" is satisfied by NB.** `:713` says D₋'s failure = "no closed cycle" and
  `:540` says one-sidedness "forbids the *closed* memory cycles that a history requires." **Non-backtracking
  walks still have closed cycles** — Ihara/Hashimoto non-backtracking walks are exactly the cyclically-
  reduced ones, which close into loops (of length ≥ 3, girth permitting; K(9,11,13) is dense, girth 3).
  So NB does **not** kill "closed cycles"; it kills only the *trivial length-2* reversal. The owned
  return-obligation (closed cycle / distinguishable return to a class, R-hist) is **met by NB**. What NB
  drops is R-walk (immediate backtrack), which no owned text elevates to a requirement.
- **The two-sidedness is already present in NB.** The path-reversal *-involution (`BOOK_03:55`) acts on
  path-words of *any* length; a non-backtracking closed loop and its reverse are both non-backtracking.
  NB is closed under reversal. So the C₊/D₋ two-sidedness (R-op) is **intact in the NB carrier** — the
  attack's premise "NB has zero D₋" is false at the level of the actual owned object.

**Conclusion of SELF-ATT-1:** identifying the forbidden backtrack with D₋ is a **pun on "return."** The
owned return (operator conjugate / distinguishable closed loop) is not the length-2 edge-reversal, and
NB retains both the operator two-sidedness and closed cycles. The exclusion of NB does **not** follow.

### Fallback grade if one insists on a bridge: SUGGESTIVE-TRANSFER (non-selecting)

There is a *thematic* resonance — "return" appears in the role name and in the walk step, and both are
about coming-back. One could *postulate* a bridge `PRIM-BACKTRACK-IS-RETURN-ROLE` identifying the
walk-backtrack with D₋ at the history layer. That is a **named external assembly choice**, exactly the
kind M1 forbids as un-owned, and exactly the shape of the underdetermination the NO-GO already records.
Even granting it, see §3: it would not deliver canonicity. So the best honest reading is
SUGGESTIVE-TRANSFER, and it is **non-selecting**.

---

## 3. HONEST SCOPE — the directed-edge (718) residue (pre-registered)

Even in the counterfactual where the crux held (NB excluded, W over NB), the attack is a **W-vs-NB
(vertex-history) test only**. The **directed-edge family 2|E|=718 is a THIRD carrier at a different
level** (edge-history, dim 718 vs vertex dim 33; `BOOK_02:1303` "transfer dims 33 != 718"). The
return-role argument compares depth-2 vertex walks (W vs NB); it says nothing that excludes the
edge-level carrier. `check_directed_edge_residue()` certifies E2∉{W,NB} and E2=W−NB (a different-level
object). **Best conceivable case is therefore PARTIAL** (NB excluded, W over NB, edge-family residual) —
not full canonicity — and even that partial result does not survive §2.

---

## 4. INDEPENDENT SKEPTIC (§05.8.R, kill-mandate) — self-run

- **PRIMARY (crux):** *KILL.* backtrack≠D₋ (three distinct owned "returns"; NB keeps closed cycles and
  the reversal involution; D₋ is upstream field/operator data). PUN-KILLED. — Accepted, no repair
  possible (the identification is simply not in the corpus, and the owned "closed cycle" clause actively
  *contradicts* the premise that NB lacks the return role).
- **Repeat of killed capacity route?** *No.* Selector here is the return-*requirement* (property of NB),
  not CAP∈{W,NB}. `check_not_capacity_route` green. Distinct route, but it still fails — on the crux, not
  on the capacity fallacy.
- **Directed-edge honestly open?** *Yes.* §3 + `check_directed_edge_residue` name E2 as an unexcluded
  third carrier at edge level. Not swept under.
- **Did the arithmetic smuggle anything?** *No.* All five checks can-fail; six mutants (wrong degree,
  broken identity, NB-has-returns, ungated exclusion = capacity fallacy, E2-not-residue, capacity-premise)
  all CAUGHT. The negative control gates exclusion on the *requirement*, not on any count — so the memo
  cannot accidentally re-run "NB has fewer walks ⟹ NB excluded."

**Skeptic verdict: NO-KILL-NEEDED beyond the crux — the attack self-terminates at SELF-ATT-1.**
No over-claim to repair; the memo already reports PUN-KILLED.

---

## 5. VERDICT + proposed row-note

**VERDICT: PUN-KILLED (fallback SUGGESTIVE-TRANSFER, non-selecting).**
The owned four-role RETURN-recurrence D₋ does **not** exclude the non-backtracking carrier. "Backtrack"
(length-2 edge reversal, R-walk) and "return-recurrence D₋" (operator conjugate / reversal involution,
R-op) and the history "distinguishable return" (closed loop to a class, R-hist) are three distinct owned
objects. NB retains closed cycles and the reversal involution, so it does **not** drop the owned return
role; only the trivial immediate backtrack, which is not owned as a requirement. Best conceivable case
was already only PARTIAL (edge-family 718 residual). **No status flip.** `PRIM-SCENE-HISTORY-REFINEMENT-RULE`
and `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001` stay OPEN / NO-GO exactly as recorded.

**Proposed row-note (append-only, for the NO-GO row — NO status change):**
> *Return-role selector attempt (memo `ATTACK_AF_CARRIER_RETURN_MEMO.md`, 2026-07-07): the owned
> four-role D₋ return-recurrence does NOT exclude the non-backtracking family. "Backtrack" (length-2
> edge reversal, `W−NB=718=Σd`) is a distinct object from the operator role D₋ (`T_ψ²−T_ψ`, Galois
> conjugate / path-reversal involution, `BOOK_02:430`, `BOOK_03:55`) and from the history "distinguishable
> return" (closed loop to a configuration class, `BOOK_06:179`). NB retains closed cycles and is closed
> under the reversal involution, so it does not drop the owned return role. PUN-KILLED; capacity route
> distinct and also non-selecting. Underdetermination unchanged; directed-edge (718) remains an
> unexcluded third carrier. Cert `attack_af_carrier_check.py` (5 can-fail + 6 mutants green).*

---

## 6. Provenance / reproduce
```
python3 attack_af_carrier_check.py            # 5 can-fail checks, ALL PASS
python3 attack_af_carrier_check.py --selftest # 6 mutation tests, ALL CAUGHT
```
Degrees {24×9,22×11,20×13} → N=33, W=15708, NB=14990, W−NB=718=2|E|, |E|=359 (prime).
All ±10 quotes line-verified in `01_BOOKS/` on 2026-07-07. No file touched outside this task dir.
```
```
