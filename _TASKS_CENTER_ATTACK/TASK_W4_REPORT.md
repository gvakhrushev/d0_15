# TASK W4 REPORT — Sturmian↔archive intertwiner over K = ℚ(√2,√5)

**Date:** 2026-07-02  **Scope:** re-open the field-disjointness NO-GO over the biquadratic composite
K = ℚ(√2,√5); construct the canonical intertwiner or name the exact next obstruction; audit √2 ownership.

**Label discipline (BOOK_00 §00.8/§00.9):** every statement is tagged
**PROVED-HERE** / **CITED-FROM-CORPUS** / **OPEN**. No "confirmed/derived/forced/closed" promotion language
is used for anything not already so-labelled in the corpus. Deliverables written only inside
`_TASKS_CENTER_ATTACK/`; no repo file edited outside it.

**Exact-arithmetic artifact:** `_TASKS_CENTER_ATTACK/w4_verify.py` (pure `fractions.Fraction` over the ℚ⁴
basis {1,√2,√5,√10}; no float enters any decision). Deterministic; runs on the local python3 3.9.6.
Result: **ALL INTERNAL CHECKS OK (0 failures)**.

---

## (a) The exact no-go statement — what "intertwiner" means there  [CITED-FROM-CORPUS]

**Owner:** `D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001` (NO-GO). Cert
`05_CERTS/vp_sturmian_refinement_discharge_nogo.py`; prose BOOK_06 §06.6 (file
`.../0007__06.6__finite-phi-ordered-finite-evolution-and-depth-co.md`, the "Iter25" paragraph).

The parent claim `D0-STURMIAN-REFINEMENT` carries a **CONDITIONAL-EXTENSION**: its *step 2* would identify
the golden **Sturmian bonding maps** with the frozen **archive/window maps** via a new external primitive
`PRIM-STURMIAN-REFINEMENT-OWNER`. The NO-GO proves this identification is **not dischargeable by internal
forcing** (M1 + the +2 grading + centre-11 convergence).

**What "intertwiner" means in the corpus** (verified across
`vp_sturmian_refinement_discharge_nogo.py`, `vp_phason_wz_transfer_owner.py`,
`vp_vnext2_tripartite_scene_xi_intertwiner.py`, `vp_x5_no_trace_as_intertwiner.py`,
`vp_five_primitive_no_trace_as_intertwiner.py`, `vp_self_reading_archive_operator_typing.py`):
an intertwiner is a **typed operator map / operator conjugation** — an invertible `U` realizing
`U·A·U⁻¹ = B` (equivalently eigenvalue-matching / an equivariant map between the two carriers). It is
**explicitly NOT** a trace/det coincidence (`vp_x5_no_trace_as_intertwiner`,
`vp_five_primitive_no_trace_as_intertwiner` reject that planted claim by name). So "no canonical intertwiner"
means: no forced invertible operator conjugation ties the ℚ(√5) golden carrier `S` to the ℚ(√10) archive
carrier. It is **operator conjugation**, not a measure-isomorphism and not a mere trace identity.

**The precise mathematical question the no-go closed** — is the golden substitution incidence

```
S = [[1,1],[1,0]]   (trace +1, charpoly t²−t−1, Perron root φ; the M1-forced Fibonacci substitution)
```

canonically conjugate/intertwined with the frozen **archive** carrier, whose scale
`359/160 = λ_c·λ_r` is the product of the two nontrivial normalized-Laplacian eigenvalues
`λ_{c,r} = 3/2 ∓ √10/40` (roots of `160λ²−480λ+359`, discriminant `640 = 64·10`) — and with the
centre-11-forced **time operator**

```
T = [[0,1],[1,-1]]   (trace −1, charpoly t²+t−1; forced by |Tr(T⁵)| = L₅ = 11)?
```

The no-go answers **NO**, on **two independent, exact grounds**:

- **(i) FIELD DISJOINTNESS** (the reason the brief targets). The golden tower lives in `ℚ(√5)=ℚ(φ)`;
  the archive scale lives in `ℚ(√10)`. `√10 ∉ ℚ(√5)` (`√10 = a+b√5 ⇒ a²+5b²=10, 2ab=0`, no rational
  solution), so `ℚ(√5) ∩ ℚ(√10) = ℚ` — the fields are disjoint over ℚ, "no canonical intertwiner ties a
  ℚ(√5) carrier to a ℚ(√10) carrier." (Explained-as-generic by
  `D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001`: `√10 = sqfree(3·10·12)` is the size-9,11,13 fingerprint.)
- **(ii) ORIENTATION.** Centre-11 convergence forces `T` (trace **−1**, orientation-reversed).
  The Sturmian tower uses `S` (trace **+1**, orientation-preserving). **Trace is a conjugacy invariant**,
  so `S` is **not** conjugate to `T`; the scene pins `T ∼ −S` (the *opposite* orientation), with
  periodic-point offset `Lₙ − |Fix(Tⁿ)| = [0,2,0,2,…]`.

The recorded no-go additionally rejects the golden back-fit out loud: `φᵏ = 359/160 ⇒ k = 1.679…`,
non-integer.

---

## (b) Re-posed over K — construction, or the named next obstruction  [PROVED-HERE]

**Representation.** K = ℚ(√2,√5) as ℚ⁴, basis {1,√2,√5,√10}, with the biquadratic multiplication table
(√2²=2, √5²=5, √2·√5=√10, √2·√10=2√5, √5·√10=5√2, √10²=10). Verified exactly (`w4_verify.py` block [A]):
`[K:Q]=4`; `√10/√5 = √2` exactly; `√10 ∉ ℚ(√5)` (its √2,√10 components exclude the {1,√5} plane); √10 is
not a ℚ-combination of {1,√2,√5}.

**Obstruction (i) is VOID in K** [PROVED-HERE]. Both √5 and √10 embed in K (√10 = √2·√5). So the
field-disjointness reason evaporates: there is no longer a "no common field" barrier between a ℚ(√5)
carrier and a ℚ(√10) carrier — they live in the *same* field K.

**Obstruction (ii) SURVIVES in K, unchanged** [PROVED-HERE — this is the load-bearing result].
The orientation obstruction is `tr S = +1 ≠ −1 = tr T`. **Trace is a similarity invariant over every field**
(if `U S U⁻¹ = T` then `tr S = tr T`). Field extension cannot change a trace. Mechanically confirmed:

- The intertwining space `{U : U·S = T·U}` has **ℚ-dimension 0** — the *only* solution is `U = 0`
  (hence no invertible `U`; there is nothing to make invertible). So **no isomorphism `S ≅ T` exists over K**,
  for the identical reason it fails over ℚ: `charpoly(S) = t²−t−1 ≠ t²+t−1 = charpoly(T)`.

Therefore **the intertwiner `S → T` is NOT constructible over K.** The next obstruction is named exactly:

> **NEXT OBSTRUCTION = ORIENTATION / TRACE (a conjugacy invariant), NOT field-disjointness.**
> `tr S = +1 ≠ −1 = tr T`; equivalently `charpoly(S) ≠ charpoly(T)`; non-conjugate spectra over *any* field.

**What the extension to K *does* let us do, and its exact limit** [PROVED-HERE]:

- The scene's own pinned relation `T ∼ −S` is realizable — and needs **no field extension at all**: an
  explicit **SL₂(ℤ)** witness `U = [[1,1],[-2,-1]]` (det `+1`) satisfies `U·T·U⁻¹ = −S` exactly **over ℚ**
  (verified over ℚ⊂K; block [D]). `charpoly(T) = charpoly(−S) = t²+t−1`. This reproduces the corpus
  relation `T ∼ −S, det U = +1` and shows the *only* honest conjugacy in this triple was already available
  over ℚ.
- **Spectral inertness of K here** [PROVED-HERE, block [E]]: every eigenvalue of `S`, `T`, `−S` is
  `(±1±√5)/2 ∈ ℚ(√5) ⊂ K`. The archive surd **√10 does not appear in any of these spectra**. So passing to
  K adds **no new eigenvalue-matching** between the golden carrier and the archive carrier — the extension is
  *spectrally inert* on the very operators whose intertwining is in question. K unifies the *scalar fields*
  but supplies no new conjugating operator, because the barrier was never a field barrier.

**Verdict for (b): NO intertwiner over K.** The exact next obstruction is the **orientation/trace
conjugacy invariant** (`tr S = +1 ≠ tr T = −1`), which is field-independent. It is *not* a dimension
mismatch (both 2×2), *not* absence-of-a-field (K contains both surds), but **non-conjugate spectra**.

---

## (c) √2-ownership verdict  [PROVED-HERE + CITED-FROM-CORPUS]

**Search** (grep `sqrt2`, `√2`, `\sqrt{2}`, `silver`, `ℤ[√2]`, `Darboux`, `conjugate symplectic`) surfaced
these √2 occurrences; classified by whether √2 sits in a **frozen operator spectrum / normalization**:

| Occurrence | Owner | √2 role | D0-native surd? |
|---|---|---|---|
| **Yukawa shell-overlap** `M=[[0,1,0],[1,0,1],[0,1,0]]`, charpoly `t³−2t`, spectrum **{0,±√2}** | `D0-YUKAWA-SHELL-OVERLAP-MATRIX-001` (cert `vp_yukawa_shell_overlap_matrix.py`, Lean `D0.Matter.YukawaShellOverlapMatrix`) | **√2 IS an eigenvalue of a frozen operator** | **YES (candidate owner)** — but OPERATOR-SCAFFOLD |
| `m_H ≈ √2·m_Z` cube face-diagonal | `D0-HIGGS-CUBE-DIAGONAL-001` (`vp_higgs_cube_forcing.py`) | √2 = face-diagonal/edge of an orthogonal cell | Geometric √2, status **BRIDGE-PREDICTOR** (not a frozen spectral surd) |
| CHSH / Tsirelson `2√2`, Bell settings `/√2` | BOOK_01 §01.17, BOOK_02 §02.22 | Pauli-stage operator norm | Standard QM √2, not a scene invariant |
| `\|cosθ−sinθ\| ≤ √2` (elliptic-channel bound) | `D0-ALPHA-HOLONOMY-LINEAR-FORM-001` | rotation-readout bound | Bounding constant, not a spectral surd |
| `sin θ_C = 1/√20 = 1/(2√5)` | Cabibbo bridge | `√20 = 2√5` → this is **ℚ(√5)**, not ℚ(√2) | No (it is golden) |

**Darboux "+2 conjugate symplectic pair" audit** [CITED + PROVED-HERE].
BOOK_00 §00.2 / §00.2 primitive-thesis: "*the structural carrier expands strictly via conjugate symplectic
pairs (+2)*", generating K(9,11,13); zones step **9 → 11 → 13 by +2**. The three shells V9,V11,V13 of the
Torus-Core13 geometry carry the shell-**adjacency** operator `M` above — which is exactly the **path-graph
P₃ adjacency** on the +2 ladder. Its spectrum is `{0, +√2, −√2}` (verified exactly:
`tr=0, e₂=−2, det=0 ⇒ t³−2t = t(t²−2)`; `w4_verify` cross-check). So:

> **√2-ownership VERDICT: PARTIAL / QUALIFIED "yes".** There **is** a D0-native occurrence of √2 in a frozen
> operator spectrum — the ±√2 eigenvalues of the +2 Darboux shell-adjacency (path-graph P₃) matrix
> `D0-YUKAWA-SHELL-OVERLAP-MATRIX-001`. This is an *independent* origin for √2 (not a golden near-miss:
> √2 ∉ ℚ(√5), proven). **HOWEVER** that claim's status is **OPERATOR-SCAFFOLD** — its own cert flags the
> physical identification of {0,±√2} with the fermion hierarchy as an **OPEN PROOF-TARGET**
> (`D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`). And this √2 belongs to the **matter/shell adjacency**
> operator, **not** to the golden-time layer nor to the archive-window flow — the two carriers the W4
> intertwiner is actually about.

**Consequence for T3.** √2 is *not owned by a frozen invariant that connects the Sturmian and archive
towers*. Its D0-native home (shell adjacency) is a **third, unrelated** operator. So for the specific
intertwiner question, ℚ(√2) is **merely the third subfield forced by the composite** K = ℚ(√5)·ℚ(√10),
with **no independent role bridging the two towers**. This is the **honest weaker version of T3** the brief
anticipated: K is a real biquadratic field with a genuine √2 elsewhere in the corpus, but that √2 does not
supply the missing intertwiner.

---

## (d) Galois compatibility result  [PROVED-HERE for the V4 structure; CITED for the sign datum]

**V4 verified explicitly** (block [B]). Three nontrivial involutions, each an order-2 field automorphism,
with the closure `g2∘g5 = g10` (and cyclic variants), fixing the three quadratic subfields:

| Automorphism | √2 | √5 | √10 | Fixed subfield |
|---|---|---|---|---|
| `g2` | −√2 | +√5 | −√10 | **ℚ(√5)** |
| `g5` | +√2 | −√5 | −√10 | **ℚ(√2)** |
| `g10`| −√2 | −√5 | +√10 | **ℚ(√10)** |

**Sign-forcing extension** [CITED: `D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001`,
`vp_phason_wde_sign_normalization_owner.py`]. On ℚ(√5) the sign is forced by `σ: φ ↦ ψ = 1−φ`, i.e.
`σ(√5) = −√5`, giving `σ(φ⁻¹) = ψ⁻¹ = −φ` (the **specific field conjugate**, *not* the naive negation
`−(φ⁻¹) = (1,−1)` — a different number; verified in block [C]).

**Which V4 elements restrict to this sign on ℚ(√5)?** Exactly those that **negate √5**: `g5` (fixes √2) and
`g10` (fixes √10). `g2` (fixes √5) does **not** produce `σ(φ⁻¹) = −φ`. Both `g5` and `g10` agree on ℚ(√5)
(they give `σ(φ⁻¹) = −φ`) but **disagree on √2**: `g5(√2)=+√2`, `g10(√2)=−√2`. So:

> **Galois compatibility VERDICT** [PROVED-HERE]: the sign-forcing datum `σ(φ⁻¹) = −φ` (an element of
> `Gal(K/ℚ)|_{ℚ(√5)}`) **has two distinct lifts to Gal(K/ℚ)** — `g5` and `g10` — and the ℚ(√5) datum
> **does not choose between them**. The choice = the action on √2 (equivalently, which of ℚ(√2), ℚ(√10)
> is fixed). **Nothing in the sign-forcing owner forces this bit** — the sign datum lives entirely in
> ℚ(√5) and is silent on √2.

**Does the choice matter for any owned invariant?** [PROVED-HERE, honest] For the operators actually at
issue (`S`, `T`, `−S`), the choice is *inert*: all their eigenvalues are in ℚ(√5), fixed-set-wise the √2
action is irrelevant to them. **No owned invariant currently on the books depends on the g5-vs-g10 bit**,
because the only √2-carrying frozen operator (the shell-adjacency ±√2, §(c)) is a separate OPERATOR-SCAFFOLD
whose physical reading is itself OPEN. **Therefore the choice is recorded as the candidate obstruction to any
*future* K-level canonicalization** (it is the precise "if a choice matters and nothing forces it" case from
step 4): should T3 ever try to make K itself the canonical closure field carrying a Galois-forced sign, it
must first supply an owner that fixes the √2-lift (g5 vs g10). That owner does not exist in the corpus. **[OPEN]**

---

## (e) Honest assessment — does T3 upgrade the no-go to a theorem-over-K, or merely relocate it?

**T3 RELOCATES the no-go; it does not upgrade it to a favourable theorem-over-K, and it does not dissolve
it.** Precisely [PROVED-HERE]:

1. **T3 genuinely kills obstruction (i).** Field disjointness — the reason the brief and the cert lead with —
   is **void over K**: both √5 and √10 embed, `√10 = √2·√5`, `ℚ(√5)∩ℚ(√10)=ℚ` is no longer a barrier because
   we are inside their compositum. This is a **real, exact gain** and it is the correct mathematical content
   of T3. **[PROVED-HERE]**

2. **But obstruction (ii) is the load-bearing one, and it is field-independent.** The Sturmian→time
   intertwiner fails because `tr S = +1 ≠ −1 = tr T` — a **conjugacy invariant that survives every field
   extension**. Over K the intertwining space `{U : US=TU}` is still `{0}`; `charpoly(S) ≠ charpoly(T)`.
   **So the no-go, as an operator-conjugation statement, becomes a *theorem over K* — a NEGATIVE one: the
   intertwiner still does not exist, now provably for a reason field extension cannot touch.** T3 upgrades
   our *certainty about why* it fails (from "wrong field" to "wrong orientation, permanently"), not the
   existence of the map. **[PROVED-HERE]**

3. **The residual is relocated, twice.** (a) The only honest conjugacy in the triple, `T ∼ −S`, was already
   available over ℚ via `SL₂(ℤ)` — K adds nothing there. (b) The remaining freedom moves into the **Galois
   layer**: the sign-forcing element has **two lifts to Gal(K/ℚ)** (g5, g10) and nothing forces the √2-bit
   between them; and the only D0-native √2 (shell-adjacency ±√2) is an **OPERATOR-SCAFFOLD** with an OPEN
   physical reading, unrelated to the two towers. So the "catalog-free closure field" hope of T3 inherits a
   **new, smaller open choice** (the √2-lift owner) in place of the old field-disjointness wall. **[OPEN]**

**One-line assessment:** *T3 dissolves the field-disjointness half of the no-go exactly (a real theorem over
K), but the intertwiner still does not exist over K — the load-bearing orientation/trace obstruction is a
field-independent conjugacy invariant — so T3 relocates the barrier from "disjoint fields" to "non-conjugate
orientation," and pushes the only remaining freedom into an unforced V4 √2-lift choice that no corpus owner
fixes.*

---

## Status ledger

| Statement | Label |
|---|---|
| No-go = operator-conjugation intertwiner `S→T`, two grounds (field, orientation) | CITED-FROM-CORPUS |
| "intertwiner" = typed operator conjugation, not trace/det coincidence | CITED-FROM-CORPUS |
| K = ℚ(√2,√5) is degree-4 biquadratic; `√10=√2·√5`; `√10∉ℚ(√5)` | PROVED-HERE (exact, `w4_verify.py` [A]) |
| Field-disjointness obstruction (i) is VOID over K | PROVED-HERE ([A]) |
| Orientation obstruction (ii) survives over K: `tr S=+1≠−1=tr T`, `{U:US=TU}={0}` | PROVED-HERE ([D],[E]) |
| Intertwiner `S→T` NOT constructible over K; next obstruction = orientation/trace | PROVED-HERE ([D]) |
| `T∼−S` via `U=[[1,1],[-2,-1]]∈SL₂(ℤ)`, exact over ℚ⊂K | PROVED-HERE ([D]) |
| Every eigenvalue of S,T,−S lies in ℚ(√5); K spectrally inert on them | PROVED-HERE ([E]) |
| √2 has a D0-native home: shell-adjacency P₃ spectrum {0,±√2} | PROVED-HERE ([c]) + CITED (`D0-YUKAWA-SHELL-OVERLAP-MATRIX-001`) |
| that √2 owner is OPERATOR-SCAFFOLD; hierarchy identification | OPEN (cited) |
| √2 does not bridge the two towers ⇒ honest weaker T3 | PROVED-HERE ([c]) |
| V4 = {id,g2,g5,g10}, involutions fixing ℚ(√5),ℚ(√2),ℚ(√10); `g2∘g5=g10` | PROVED-HERE ([B]) |
| sign-forcing `σ(φ⁻¹)=−φ` has TWO lifts to K (g5,g10); √2-bit unforced | PROVED-HERE ([C]) + CITED (sign owner) |
| owner that fixes the g5-vs-g10 √2-lift | OPEN (does not exist in corpus) |
| T3 relocates (not upgrades-favourably, not dissolves) the no-go | PROVED-HERE (assessment) |

**Reproduce:** `cd _TASKS_CENTER_ATTACK && python3 w4_verify.py` → prints all blocks, ends
`ALL INTERNAL CHECKS OK (0 failures)`.
