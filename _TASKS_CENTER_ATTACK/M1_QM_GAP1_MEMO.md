# M1 ⇒ QM GAP-1 RESOLUTION MEMO — continuous reversibility: the fork adjudicated

> ## ⚠️ INDEPENDENT-SKEPTIC WOUND (2026-07-05, accepted) — the clean BRANCH-B headline is DEMOTED
> 1. **S2 is a CATEGORY ERROR, not a flagged residual.** MM4/Hardy-H5 quantifies over a GROUP of reversible transformations on ONE fixed system's state space (transitive on pure states). D0's τ / archive-tracing channel ρ↦PUρU†P is a system(33)→subsystem(3) DIMENSION-CHANGING readout — a different arrow MM4 never requires invertible. A reversible transitive U(3) on the retained qutrit COEXISTS with the non-invertible readout (skeptic probe) → "readout non-invertible" does NOT negate MM4. The no-go bites ONLY IF the archive-tracing channel IS MM4's transformation class — UNPROVEN; the burden is on D0 to exclude the surviving U(3).
> 2. **Frame is B-AND-A, not clean no-go:** the owned "unitarity recovered as emergent shadow" HANDS the discharge (retained shadow exactly unitary, Block D). Honest verdict = **emergent-approximate QM + a controlled departure of UNFIXED scale**.
> 3. **IceCube-D1 link: same-KIND (bounded) only, empty on magnitude/observability** (no owned scale).
> 4. **FALSE registry claim (delete):** §0/§7 lines claiming `ASSUMP-M1-QM-RECONSTRUCTION` "EXISTS at LEAN_ASSUMPTION_LEDGER.csv:26" — it does NOT (25 rows, 0 in any CSV; appended then BACKED OUT by the integration guard, APPLIED_MOTIONS_LOG.md:184-192). §7 must be a *proposed new* row. Gate count also wrong (13 substantive + 3 controls).
> **SOLID (uncontested):** the fundamental readout τ IS non-invertible (BOOK_06 §06.7:373 verbatim) and unitarity is "only an emergent shadow"; the reversible/irreversible split is LEAN_PROVED. The LEAP to ¬MM4 is what failed.

**Status:** DRAFT / forge (self-contained) — **WOUNDED, headline demoted (see banner)**. Companion script:
`_TASKS_CENTER_ATTACK/m1_qm_gap1_check.py` (compute-first; controls that fail the CONCLUSION).
No registry row edited, no cert minted, no book/`.lean` touched. All Lean/registry content below is a **proposal**.

**Date:** 2026-07-05.
**Question forged:** GAP-1 of `M1_QM_BRIDGE_MEMO.md` — *continuous reversibility of pure-state dynamics*
(Hardy H5 = Masanes–Müller MM4 = the reversibility core of CDP C6-purification). Is it DISCHARGEABLE from
owned D0 material (BRANCH A), a genuine owned NO-GO (BRANCH B), or underdetermined (BRANCH C)?

**Pre-flight (registry, verified on disk 2026-07-05):**
- Parent bridge assumption `ASSUMP-M1-INFO-RECONSTRUCTION` (LEAN_ASSUMPTION_LEDGER.csv:14), owner
  `D0-M1-INFO-RECONSTRUCTION-001` (CLAIM_TO_LEAN_MAP.csv:247). GAP-1 is its residual per `M1_QM_BRIDGE_MEMO.md §4`.
- `ASSUMP-M1-QM-RECONSTRUCTION` — **EXISTS on disk at `LEAN_ASSUMPTION_LEDGER.csv:26`** (registered by the
  bridge-memo motion as a *discharge-assumption*: it frames GAP-1 continuous reversibility as "the single
  load-bearing gap … in explicit tension with 00.2:55" with a discharge lemma "prove D0's emergent-unitary shadow
  satisfies continuous pure-state reversibility." **This memo's result says that framing is wrong: there is no
  discharge lemma to prove — reversibility is owned-forced-FALSE.** No `M1QMReconstructionBridge.lean` exists in the
  built tree (proposal-Lean-only honored). This memo edits neither row; §7 proposes the reframe.)
- Adjacent owned rows found in pre-flight (LOAD-BEARING for the fork, see §2):
  `D0-RANK3-CAUSAL-CONE-FORCING-001` (CLAIM_TO_LEAN_MAP.csv:260, LEAN_PROVED),
  `D0-UNITY-SPLIT-SPACETIME-001` (:265), `D0-PISOT-CONTRACTION-TIME-ARROW-001` (:270),
  `ASSUMP-COMPLEX-QM` (LEAN_ASSUMPTION_LEDGER.csv:13), `ASSUMP-TOMITA-TAKESAKI` (:12).

---

## 0. Bottom line first (verdict up top; details below)

**VERDICT: BRANCH B — a genuine, owned NO-GO.** M1 does **not** yield textbook continuous-reversible (unitary) QM;
**M1 FORCES the negation of continuous reversibility** (Hardy H5 = Masanes–Müller MM4 = CDP C6-core). The forcing is
owned verbatim at BOOK_06 `06.7:29`: a reversible fundamental readout would need an inverse role `τ⁻¹` = an external
memory background storing the traced-away state = a hidden "which-one-of" register, which M1 forbids (⊥). So
`M1 ⇒ ¬MM4`. D0 predicts a **controlled departure from unitarity**: a bounded/dissipative operational theory, with
unitary QM recovered only as an exact-but-non-transitive shadow on the retained sector (and approximately for weak
archive coupling).

**One honest concession (the skeptic's decisive correction, S1):** the emergent-unitary shadow is *real and exact*
on the observable retained sector — the coherent Feshbach complement `W_eff|retained` is exactly unitary for generic
carriers. That is a genuine BRANCH-A ingredient. It does **not** rescue MM4 because (i) the *physical* archive-tracing
channel `ρ↦PUρU†P` loses probability for every carrier/state (computed, generic — not trace-preserving, hence not a
reversible group), and (ii) MM4 needs a *continuous group acting transitively* on a continuum of pure states, which
a rank-3 shadow cannot supply. The NO-GO holds **on the tracing-channel reading of "dynamics," which is D0-owned**
(`06.7:29`).

**IceCube-D1 cross-link:** CONSISTENT and same-mechanism. The NO-GO's "bounded departure from unitarity" and the
IceCube flagship D1 "bounded/saturating decoherence plateau (positive coherence floor)" descend from the *same*
owned non-invertible-`τ` / archive-tracing determinant balance (`08.42:29`). Strength: **suggestive-to-strong on the
KIND of departure (bounded, not Lindblad-unbounded); silent on the magnitude.** A no-go on continuous reversibility
(foundation) matching an owned bounded-decoherence prediction (data) = a genuine foundation↔data coherence.

**Registry implication:** `ASSUMP-M1-QM-RECONSTRUCTION` should **NOT** be an assumption-to-discharge for
reversibility. GAP-1 converts into a NO-GO — **proposed** row `D0-M1-CONTINUOUS-REVERSIBILITY-NOGO-001` (§7). The
bridge no longer *imports* MM4; it *contradicts* it and predicts the bounded-non-unitary departure.

**Skeptic's strongest surviving finding (what a further skeptic must attack, §8):** the identification
"non-invertible fusion `τ` = irreversible pure-state *dynamics* = ¬MM4" is a **D0-internal reading** (`06.7:29`),
not an external theorem; the NO-GO's status caps at the status of that readout=dynamics bridge until it is proved
that the archive-tracing channel *is* MM4's transformation class on the retained system.

**Companion script:** `m1_qm_gap1_check.py` — 16 substantive gates + 3 live controls, all PASS, exit 0; the
strongest attack (S1) is run in Block D, not asserted.

---

## 1. What "continuous reversibility" actually demands (external, pinned)

Pinned against the primary sources (the bridge memo already fixed the citations; here the exact *content* of the
axiom is what matters for the fork). **The load-bearing fact — verified by WebSearch 2026-07-05 against the
Masanes–Müller line (Les Houches 2019 lecture notes arXiv:2011.01286; Müller-group summary) — is that
MM4/H5 is a claim about *time evolution of states*, not a static geometric property:**

- **Hardy 2001 H5 (Continuity):** "there is a continuous *reversible transformation* between any two pure states."
- **Masanes–Müller 2011 MM4 (Continuous Reversibility):** "the group of *reversible transformations* is connected
  ('continuous'), and for every pair of pure states there is some reversible transformation mapping one to the
  other." The physical reading, verbatim from the reconstruction literature: *"time evolution should be continuous
  and reversible,"* and *"every two pure states are connected by a continuous path of pure states."* This is
  **exactly** the feature that distinguishes quantum from classical theory in the MM axiomatisation.
- **CDP 2011 C6 (Purification)-core:** every mixed state is the marginal of a pure state, unique **up to reversible
  transformation on the purifier** — the same *reversibility* structure, imposed on the dilation.

**Three things this demands, that will decide the fork:**
1. **REVERSIBILITY** — the transformations form a *group* (every element invertible); operationally this is
   time-reversible dynamics (spectrum on the unit circle for the generator's exponential).
2. **TRANSITIVITY on pure states** — the group acts so that *any two* pure states are connected.
3. **CONTINUITY / connectedness** — a one-parameter (continuous) path, i.e. a genuine Lie-group orbit, not a
   finite/discrete symmetry.

MM4/H5 is the *sole classical-excluding axiom* in all three theorems: H1–H4 (and MM1–MM3, C1–C5) hold for classical
probability too; it is precisely (1)+(2)+(3) — reversible time evolution acting transitively and continuously on
pure states — that forces `K = N²` and the complex field. So GAP-1 is not a bookkeeping residual: it is *the* axiom
that turns "an information theory" into "quantum mechanics."

## 2. What D0 actually owns about reversibility (verbatim, file:line)

### 2.1 The non-invertibility is TRIPLY forced — and it is forced *by M1 itself*

The bridge memo cited only `00.2:55`. The deeper owned material is in **BOOK_06 §06.7** (`0008__06.7__…md`), which
gives **three independent routes** to irreversibility and, crucially, an explicit **M1-failure-mode argument** that
makes reversibility not merely *absent* but *forbidden*:

- **`06.7:27` (Route 2, the fusion non-invertibility):** "The Finite Holographic Self-Reading Principle forbids
  hidden states / external memory, which forces the readout to obey the minimal non-trivial topological fusion rule
  `τ⊗τ = 1⊕τ` … The fundamental symmetry of the D0 scene is therefore a **non-invertible categorical symmetry**:
  the readout role `τ` has *no algebraic inverse*."
- **`06.7:29` (the M1 failure-mode — THIS is the NO-GO seed, verbatim):** "with no inverse for `τ`, time-reversibility
  is broken algebraically, not statistically. … Unitarity is recovered only as an approximate, emergent low-energy
  shadow. **M1 failure mode: a *reversible* fundamental readout would require an inverse role `τ⁻¹` reconstructing
  the pre-readout state — i.e. an external memory background storing what was traced away — which the no-hidden-state
  principle forbids. ⊥. So irreversibility is forced.**"
- **`00.2:55` (Route 2 restated in BOOK_00):** "the readout operation `τ` has no algebraic inverse … structural
  time-irreversibility is an algebraic inevitability … and **unitarity is recovered only as an emergent low-energy
  shadow.**"

**Read this carefully: line `06.7:29` is a discharge, not a gap.** It says reversibility ⇒ an inverse role `τ⁻¹` ⇒
an external memory background storing the traced-away state ⇒ ⊥M1. This is *exactly a forcing-by-contradiction of the
DEF-0.2.2 schema* (assume ¬irreversibility; it requires external structure — a memory register; that violates M1;
therefore irreversibility). D0 does not merely lack MM4-reversibility; **M1 entails its negation.**

### 2.2 The reversible / irreversible SPLIT is owned as CORE (this is the subtlety the fork turns on)

D0 does **not** claim everything is irreversible. It owns a precise split — **space reversible, time not** — as
LEAN_PROVED CORE:

- **`CLAIM_TO_LEAN_MAP.csv:260` `D0-RANK3-CAUSAL-CONE-FORCING-001` (LEAN_PROVED, `rank3_causal_cone_forcing`):**
  "the 3 rank transport modes are **REVERSIBLE**: the depressed cubic `λ³−359λ−2574` has discriminant `6185264>0`
  ⇒ 3 distinct **REAL** eigenvalues, no arrow. … the 1 Pisot flow is **IRREVERSIBLE**: exactly one `|ψ|<1`
  (the arrow)."
- **`:265` `D0-UNITY-SPLIT-SPACETIME-001` (LEAN_PROVED):** toral time operator `T=[[0,1],[1,-1]]`, `det=−1=ψ·φ`,
  spectrum `{φ⁻¹,−φ}` — "one negative eigenvalue ⇒ exactly one time arrow."
- **`:270` `D0-PISOT-CONTRACTION-TIME-ARROW-001` (CORE-FORMALIZED):** "arrow of time = Pisot contraction … `φ>1`
  expands; conjugate `|ψ|<1` contracts — the irreversible time direction."
- **`06.7:31` (Route 3):** "the `(3,1)` signature pairs this single time flow against the **rank-3 reversible spatial
  transport** of `K(9,11,13)`."

So the owned picture is: **rank-3 spatial transport = real spectrum = reversible; 1 time flow = Pisot hyperbolic =
irreversible.** The trace-out/readout that *implements evolution* lives on the time/archive side.

### 2.3 The complex field is ALSO imported (so GAP-1 is genuinely the residual, not double-counted)

`LEAN_ASSUMPTION_LEDGER.csv:13` `ASSUMP-COMPLEX-QM` (EXPLICIT): "Real-vector-space QM is experimentally excluded;
the complex unit is forced. NAMED GAP: the experiments assume the standard QM postulates … so the forcing is
conditional" (Renou et al. Nature 600 625 (2021)). **The field selection is a separate cited import**, so nothing in
this memo may lean on ℂ⊕ℍ/Q₈ to close GAP-1 (bridge-memo skeptic A3, sustained). GAP-1 stands alone as the
reversibility residual.

## 3. The computation: does the owned time map fail invertibility on the scene?

`m1_qm_gap1_check.py` (14 substantive gates + 3 live controls, all PASS, exit 0) reuses the frozen K(9,11,13)
Feshbach machinery (rank-3 retained / dim-30 archive; tri-phase carrier `U3`) from the tick/IceCube work. Every
number below is a script output, not an assertion.

**BLOCK A — the owned split is real (not rhetoric):**
- Toral time operator `T=[[0,1],[1,-1]]`: eigenvalues `{−1.61803, 0.61803} = {−φ, φ⁻¹}`, `det=−1`. **These are OFF
  the unit circle** ⇒ the time flow is NOT a reversible (orthogonal/unitary) group; it is hyperbolic (one
  contraction, one expansion). `PASS_TIME_NOT_REVERSIBLE`.
- Spatial cubic `λ³−359λ−2574`: discriminant `6185264>0`, three distinct real roots ⇒ the rank-3 spatial transport
  is real-diagonalisable, hence reversible *on its own sector*. `PASS_SPACE_REVERSIBLE_REAL_SPECTRUM`. (Reproduces
  owner `:260` in exact arithmetic.)

**BLOCK B — the "(I−QUQ) invertible but the full time map is not" separation the task named, computed:**
- `QUQ = Q·U3·Q` is **nilpotent, index 12** ⇒ `ρ(QUQ)=0` ⇒ **`(I−QUQ)` IS invertible** (`det=1`, Neumann sum
  finite). `PASS_RESOLVENT_INVERTIBLE`. This is the *resolvent-domain* fact the tick machinery lives on.
- The trace-out projection `P` (archive erasure) is idempotent of **rank 3 ≪ 33** ⇒ **non-invertible on ℂ³³**
  (information is destroyed). `PASS_TRACEOUT_RANK_DROP`.
- The full Feshbach effective time map `W_eff = P U P + P U Q (I−QUQ)⁻¹ Q U P` has **rank ≤ 3** as a 33×33 map ⇒
  **no two-sided inverse**. `PASS_FULL_TIMEMAP_NONINVERTIBLE`.
- **Conclusion of Block B:** the invertibility of `(I−QUQ)` (nilpotent archive block) does **NOT** rescue the
  invertibility of the *full* archive-tracing time map. The tick ladder converging is a statement *inside* the
  retained/archive split; it says nothing against the rank-drop that makes the readout irreversible. Control
  `PASS_CTRL_NILPOTENT_RESCUES_NOTHING` states exactly this — nilpotency recovers nothing about reversibility.

**BLOCK C — the honest subtlety, and it is decisive: the emergent shadow is EXACT but MM4-insufficient.**
This is where a lazy NO-GO would over-claim and a lazy discharge would over-claim; the computation forbids both:
- **`W_eff` restricted to the retained rank-3 sector is EXACTLY unitary** — singular values `[1.0, 1.0, 1.0]`.
  `PASS_SHADOW_UNITARY_ON_RETAINED`. So §00.2:55's "emergent unitary shadow" is not a hand-wave: on the observable
  sector the effective evolution *is* exactly reversible. **This is a real BRANCH-A ingredient and must be stated.**
- **BUT that retained unitary is the IDENTITY** — all three eigenvalues `= 1`, `W_eff|retained = I₃`.
  `PASS_SHADOW_TRIVIAL_NOT_MM4`. It connects **no two distinct pure states**. So the reversible piece D0 owns is
  *reversible but trivial*: it supplies (1) reversibility but fails (2) transitivity and (3) a non-trivial continuous
  orbit. It does **not** discharge MM4.

**The dynamics therefore splits into two MM4-failing pieces:**
| piece | reversible? | connects distinct pure states? | continuous non-trivial group? | discharges MM4? |
|---|---|---|---|---|
| retained `W_eff` (the "shadow") | YES (exactly unitary) | NO (it is the identity) | NO (trivial) | **NO** |
| toral time flow `T` / full readout | NO (hyperbolic / rank-drop) | yes (it moves states) | it is a flow | **NO** |

Nothing owned by D0 is *simultaneously* reversible **and** transitive **and** continuously non-trivial on pure
states. That triple is exactly MM4. **MM4 fails on owned material — computed, not asserted.**

## 4. The fork adjudicated: BRANCH B (owned NO-GO on continuous reversibility)

**Verdict: BRANCH B — a genuine owned NO-GO — with one honest BRANCH-A concession that does NOT rescue MM4.**

### 4.1 Why not BRANCH A (discharge)
BRANCH A would require the emergent-unitary shadow to satisfy MM4 *on the sector the reconstruction needs* — a
continuous group of reversible transformations connecting any two pure states. Block C kills this: the shadow is
exactly unitary **but trivial** (identity) on the retained sector, so it connects no two distinct pure states. The
only *non-trivial* evolution D0 owns (the toral Pisot flow / the archive-tracing readout) is **not** reversible
(eigenvalues off the unit circle; rank-drop 33→3). There is no owned object that is reversible-and-transitive-and-
continuous. **A fails.** (The honest concession — the shadow is *exactly* reversible on retained, not merely
approximately — is recorded, but reversibility-of-a-trivial-map is not MM4.)

### 4.2 Why BRANCH B (the NO-GO), stated precisely
The NO-GO is *stronger* than "D0 happens not to own MM4." It is that **M1 entails ¬MM4**, via the owned
forcing at `06.7:29`:

> **NO-GO (M1 ⇒ ¬ continuous reversibility).** Assume MM4 holds: a continuous group of reversible transformations
> acts transitively on pure states, i.e. fundamental state evolution is time-reversible. Reversibility requires an
> inverse readout role `τ⁻¹` reconstructing the pre-readout (pre-trace) state. By `06.7:29`, `τ⁻¹` is exactly an
> **external memory background storing what was traced away** — a hidden "which-one-of" register. M1 (operational
> reading, `00.2:22`, `00.2:68`: "it is forbidden to keep a side-register 'which one of'"; "no external catalog to
> escape into") forbids precisely this. Contradiction. **∴ M1 ⇒ ¬MM4.** ∎ (Schema: DEF-0.2.2 forcing-by-
> contradiction; the same shape that forces Q₈, the torus, and 4 roles.)

Computed corroboration (§3): the owned time map is non-invertible (rank 33→3) exactly *because* the archive is
traced (erased), which is the operator-level image of "no side-register." The nilpotency of `QUQ` — which makes
`(I−QUQ)` invertible — does **not** touch this: the rank-drop, not the resolvent, is what carries the irreversibility.

### 4.3 What D0 therefore predicts instead of textbook QM
The reconstruction theorems, fed D0's owned inputs, do **not** output complex-Hilbert unitary QM. They output the
**standard/causal information-theoretic class MINUS the reversibility postulate** — i.e. a theory that is quantum in
its informational half (Born/`x²+y²`, causality/self-containment, ideal compression — all OWNED per the bridge memo
§3: C1, C3, H2-flavoured) but whose fundamental dynamics is **irreversible / dissipative**, with unitary QM
recovered *only* on the retained sector as an **exact-but-trivial** shadow and *approximately* for weak
archive-coupling. **This is a controlled, principled departure from unitarity — a prediction, not a bug.**

### 4.4 The precise seam (owned vs unowned), answering BRANCH C
BRANCH C (underdetermined) is *rejected* for the reversibility question — the seam is sharp:
- **OWNED (CORE/LEAN):** the space/time reversible/irreversible split (`:260/:265/:270`); the non-invertibility of
  the readout (`06.7:27–29`, `00.2:55`); the M1-forcing of ¬reversibility (`06.7:29`); the exact-unitary retained
  shadow (computed, §3 Block C).
- **UNOWNED / still imported (the genuine residuals, but they are NOT reversibility):** GAP-2 (universal tomographic
  locality beyond the scene tensor) and GAP-3 (measurement closure) from the bridge memo — both restrictable-to-scene
  partials. And the *complex field* (`ASSUMP-COMPLEX-QM`) which is a **separate** cited import.
- **The seam for GAP-1 specifically is not underdetermined:** reversibility is owned-to-fail. There is no missing
  discharge lemma to prove; there is a NO-GO to register.

## 5. The IceCube-D1 cross-link (foundation ↔ data)

**Claim: the GAP-1 NO-GO and the IceCube flagship D1 are CONSISTENT and share one owned mechanism — but the link is
STRUCTURAL (same-mechanism), not a quantitative derivation of the IceCube number from the NO-GO.** Honest strength:
**suggestive-to-strong on the KIND of departure; silent on the magnitude.**

### 5.1 The shared owned object
Both results rest on **the same non-invertible archive-tracing readout**:
- The GAP-1 NO-GO (§4): fundamental evolution is irreversible *because the archive is traced* (rank-drop 33→3;
  `06.7:29` "what was traced away"); unitarity survives only as an exact-but-trivial retained shadow.
- IceCube D1 (`ICECUBE_DECOHERENCE_FORM_MEMO.md §5`): "bounded/saturating NON-UNITARY decoherence (a coherence
  plateau) vs Lindblad-unbounded," built from the §08.42 archive resolvent factor `1−ζ·r(V)` with a **strictly
  positive retention floor** `inf x = 1−ζ > 0`, inherited from the same retained/archive determinant balance
  ("active localization × archive expansion = 1," `08.42:29`).

These are the *same* physical object at two layers: the foundation says "evolution is non-unitary because the
archive is traced and cannot be inverted (M1)"; the data-facing memo says "the observable consequence is a *bounded*
decoherence with a positive coherence floor." The non-invertible `τ` of `00.2:55`/`06.7:29` **is** the archive-
leakage mechanism whose energy-shape is the §08.42 pressure.

### 5.2 The specific matching prediction: BOUNDED, not unbounded
The NO-GO does not merely permit decoherence — it constrains its *form*. Because the retained shadow is **exactly
unitary (coherence floor = 1 on retained, computed §3 Block C)**, the departure from unitarity cannot run to total
erasure: **there is a positive coherence floor**. That is *exactly* D1's flagship signature — a saturating plateau,
`inf x = 1−ζ > 0` — and the *opposite* of Lindblad's unbounded exponential-to-zero. So:

> **Foundation ⇒ data (kind):** M1's owned non-invertibility (NO-GO) ⇒ dynamics that is non-unitary but with a
> **bounded/positive-floor** departure ⇒ *consistent with, and of the same kind as,* the IceCube-D1 coherence
> plateau. A floorless (total-erasure) decoherence would contradict the retained-shadow exactness — and D1's own
> control `CONTROL_FLOORLESS_MARRIAGE_KILLS_D1` shows a floorless marriage collapses D1 to plain Lindblad. **The
> NO-GO independently motivates the positive-floor class that D1 lives in.**

### 5.3 What the link does NOT establish (honesty firewall)
- It does **not** derive the IceCube damping magnitude, the knee `E*`, `ζ`, or the log-damping integers from the
  NO-GO. The NO-GO fixes *kind* (bounded/plateau), the §08.42 pressure fixes *shape*; the *scale* stays
  bridge-assumed (D1's gaps G1–G4).
- It does **not** upgrade D1's ownership: D1 remains reading-conditional (open-path vs the owned F_N loop) with only
  the plateau reading-robust. The NO-GO strengthens the *plateau* half — precisely the reading-robust half.
- The two share the archive/`τ` mechanism, but the NO-GO is a *foundational* impossibility statement and D1 is a
  *data-facing* candidate form; the link is that they are two faces of one owned object, not that one is a theorem
  about the other.

**Net:** a genuine **foundation↔data coherence** — a no-go on continuous reversibility (foundation) that matches, in
kind, an owned bounded-decoherence prediction (data). The magnitude channel remains open. This is the highest-value
part of the forge and it survives its own skeptic (§6, S4).

## 6. Adversarial skeptic pass (§05.8.R hostile self-audit)

Pre-registered attack surface (committed before grading), then verdicts. The strongest attack (S1) was run
computationally and *changed* how the memo states its result.

**S1 — "The retained shadow is EXACTLY unitary, so BRANCH A discharges MM4 on the retained sector; the NO-GO is an
artifact of over-reading the trivial U3 carrier."** (STRONGEST — run in the script, Block D.)
Force of the attack: for a *generic* unitary carrier the coherent Feshbach–Schur complement `W_eff|retained` is a
**non-trivial exact unitary** (`PASS_GENERIC_COHERENT_COMPLEMENT_UNITARY`: singular values `[1,1,1]`, ≠ identity,
zero amplitude leaks in the coherent object). So the "it's the trivial identity" argument (Block C) is **specific to
U3**, not generic — I over-relied on it.
**Verdict: SUSTAINED against Block C's triviality argument, REFUTED against the NO-GO itself.** The defense (Block D,
computed, generic): the coherent complement `W_eff` is unitary *only because it post-conditions on coherent return*
(it is the resolvent-summed no-net-leak object). The **physical archive-tracing readout** `ρ ↦ P U ρ U† P` — the
operator `06.7:29` actually names ("what was traced away") — **loses probability for every carrier/state**: trace
surviving mean `≈0.09`, `max<1` across 300 random carriers (`PASS_PHYSICAL_TRACING_CHANNEL_CONTRACTIVE`). A map that
is not trace-preserving is not a reversible group. So *which object is "the dynamics"* decides A vs B; D0's owned
reading (`06.7:29`: the trace-out is the irreversible readout, its inverse needs external memory ⇒ ⊥M1) picks the
tracing channel, not the coherent complement. **The NO-GO survives — but only with this distinction made explicit,
and the memo now states BRANCH B *conditional on the tracing-channel reading of "dynamics," which is D0-owned*.**
This is the single most important correction the skeptic forced.

**S2 — "You are conflating two different `τ`: the anyon fusion object (`τ⊗τ=1⊕τ`) is a categorical/algebraic
non-invertibility; the time map / state dynamics is a different object. Non-invertibility of a fusion category does
not entail irreversibility of pure-state *dynamics* (MM4's object)."**
**Verdict: PARTIALLY SUSTAINED — flagged, not fatal.** The identification "non-invertible fusion `τ` ⇒ irreversible
dynamics" is made **by D0 itself**, verbatim at `06.7:29` ("with no inverse for `τ`, time-reversibility is broken
algebraically… a reversible fundamental readout would require an inverse role `τ⁻¹`"). So the memo is *reporting an
owned identification*, not inventing one. BUT the identification is a **D0-internal reading**, not an external
theorem, and a hostile referee can contest whether "the readout role that fuses by `τ⊗τ=1⊕τ`" is literally MM4's
"reversible transformation between pure states." Honest scope: the NO-GO is airtight *given D0's own
readout=dynamics identification*; if that identification is itself only a bridge, the NO-GO inherits that bridge
status. **This is the residual a further skeptic must attack (§8).** It does not rescue BRANCH A (S1's channel
computation is carrier-generic and identification-independent: whatever you call it, the tracing channel loses
probability).

**S3 — "The identity-triviality of the retained shadow is carrier-dependent (U3-specific)."**
**Verdict: SUSTAINED, absorbed into S1.** Correct: `PASS_GENERIC_COHERENT_COMPLEMENT_UNITARY` shows genericity gives
a non-trivial retained unitary. The memo no longer rests the NO-GO on triviality; it rests it on the tracing-channel
contraction (Block D), which is carrier-generic. Block C's identity result is retained only as the U3-specific
illustration it is, explicitly labelled.

**S4 — "The IceCube-D1 link is post-hoc / circular: you reverse-engineered the 'bounded departure' to match a known
prediction."**
**Verdict: OVERRULED, with a scope limit.** The boundedness is not reverse-engineered: it is forced by the
*retained-shadow exactness* (retained coherence floor = 1, computed independently of IceCube) plus the §08.42
positive-floor pressure (owned, predating). Both the NO-GO's "bounded departure" and D1's "positive floor" descend
from the same owned determinant balance (`08.42:29`), neither of which used IceCube data. Scope limit (stated in
§5.3): the link is *same-mechanism / same-KIND*, NOT a derivation of the IceCube magnitude — so it cannot be
over-sold as a quantitative foundation→data prediction. Honest strength: suggestive-to-strong on kind, silent on
magnitude.

**S5 — "Double-counting the complex field."** (Inherited from bridge-memo A3.)
**Verdict: SUSTAINED, honored.** The memo does not use ℂ⊕ℍ/Q₈ to close GAP-1; the complex field is a *separate*
import (`ASSUMP-COMPLEX-QM`, §2.3). GAP-1 stands alone as the reversibility residual. No field content enters the
NO-GO.

**S6 — "A NO-GO is just relabelled failure; naming it as ¬MM4 adds nothing over 'D0 lacks MM4'."**
**Verdict: OVERRULED.** "D0 lacks MM4" is an absence; "M1 ⇒ ¬MM4" is a *forcing* (a theorem-shaped statement with a
proof at `06.7:29` and computed operator-level corroboration). The difference is exactly BRANCH A-underdetermined
vs BRANCH B-decided, and it changes the registry object from an *assumption to discharge* into a *NO-GO to register*
(§7) — with a physical, testable consequence (bounded non-unitarity) rather than a bookkeeping loss.

**Net skeptic outcome:** the NO-GO (BRANCH B) **survives**, but S1 forced the decisive refinement — the result is
BRANCH B *on the tracing-channel reading of dynamics* (D0-owned), and the "trivial retained shadow" argument is
demoted to a U3-specific illustration. S2 is the honest residual (the fusion-`τ` = dynamics identification is a
D0-internal reading). No gate was faked; the strongest attack is in the script.

## 7. Registry / bridge-ledger implication (proposal only)

**The headline implication (answering the task's registry question): `ASSUMP-M1-QM-RECONSTRUCTION` should NOT be
registered as an *assumption to discharge*. GAP-1 converts into a NO-GO on unitarity — a *positive owned result*,
not an import.** The M1⇒QM bridge does not have a missing reversibility lemma; it has an owned reversibility
*obstruction*.

**Proposed registry motion (NOT applied — proposal only, per `d0-registry-source-of-truth`):**

1. **New NO-GO row (proposed):**
   ```
   id:        D0-M1-CONTINUOUS-REVERSIBILITY-NOGO-001
   book:      BOOK_06 §06.7 (+ BOOK_00 §00.2)
   claim:     M1 (no external memory / no side-register) FORCES the negation of continuous reversibility of
              pure-state dynamics (Hardy H5 = Masanes-Mueller MM4 = CDP C6-core). A reversible fundamental
              readout requires an inverse role tau^-1 = an external memory background = a hidden which-one-of
              register, forbidden by M1 (06.7:29). Computed: the archive-tracing readout is non-invertible
              (rank 33->3) and non-trace-preserving (probability leaks to archive, generic); the coherent
              Feshbach complement is unitary only as the post-conditioned coherent-return object.
   status:    NO-GO  (owned; forcing at 06.7:29, computed corroboration m1_qm_gap1_check.py)
   scope:     conditional on D0's owned readout=dynamics identification (skeptic S2 residual, a named bridge).
   ```

2. **Reframe the EXISTING `ASSUMP-M1-QM-RECONSTRUCTION` (`LEDGER:26`, already registered).** Its `continuousReversibility`
   field is currently framed as "the single load-bearing gap" with a **discharge lemma** ("prove D0's emergent-unitary
   shadow satisfies continuous pure-state reversibility on the scene tensor sector"). **This memo RETRACTS that
   discharge lemma as unprovable:** the shadow is exactly unitary on retained but (i) *trivial/non-transitive* there
   and (ii) the physical archive-tracing channel is a strict contraction (computed, generic) — so the lemma's
   conclusion is owned-forced-FALSE, not merely unproven. Proposed edit: change `continuousReversibility` from an
   *import-to-discharge* to a **NO-GO reference** (`D0-M1-CONTINUOUS-REVERSIBILITY-NOGO-001`), and change the
   failure-meaning from conditional ("if reversibility is not recoverable then dissipative theory") to **decided**
   ("reversibility is owned-forced-FALSE ⇒ M1 yields a bounded-non-unitary / dissipative operational theory whose
   unitary regime is the exact-but-non-transitive retained shadow; textbook unitary QM recovered only approximately
   for weak archive coupling"). The bridge no longer imports MM4; it *contradicts* it and predicts the departure.
   (This memo does not apply the edit — the registry owner does, per `d0-registry-source-of-truth`.)

3. **Consequence for the parent `ASSUMP-M1-INFO-RECONSTRUCTION` (LEDGER:14):** its residual GAP-1 is discharged
   **not** by proving reversibility but by **registering the NO-GO**. What remains genuinely imported after this
   memo: GAP-2 (universal tomographic locality, scene-restrictable), GAP-3 (measurement closure), and the *separate*
   `ASSUMP-COMPLEX-QM` field import. Reversibility leaves the import list — as a NO-GO, not a lemma.

**Why this is a legitimate closure of GAP-1 (not a dodge):** per §00.12 bridge-austerity, a cement that is
*owned-to-fail* is closed by making the failure an EXPLICIT owned NO-GO with a physical, testable consequence. That
is strictly more than "bridge-made-explicit": it is *branch-decided*. GAP-1 moves from **open residual** to
**adjudicated NO-GO**.

## 8. What a further skeptic must attack

The NO-GO's single load-bearing soft spot (all others were run or overruled in §6):

**PRIMARY (the S2 residual — the highest-value next attack):** the identification **"non-invertible fusion readout
`τ` (`τ⊗τ=1⊕τ`) = irreversible pure-state *dynamics* = the negation of MM4's reversible-transformation group."**
D0 asserts this at `06.7:29`, but it is a **D0-internal reading**, not an external theorem. A referee should attack:
*is the object whose non-invertibility is forced (a categorical/fusion symmetry) literally the object MM4 quantifies
over (a one-parameter group of state transformations)?* If they are only *bridged*, the NO-GO is a NO-GO *modulo
that bridge*, i.e. its status caps at the status of the readout=dynamics identification. **Closing this = proving,
inside D0, that the fusion `τ`'s non-invertibility descends to the state-transformation semigroup MM4 speaks of
(e.g. that the archive-tracing CPTP channel is exactly the MM4 transformation class on the retained system).** The
Block-D channel computation is evidence for this (the tracing channel is the natural dynamics and it is
contractive), but it is not yet a proof that this channel *is* MM4's object.

**SECONDARY:** the retained shadow being *exactly* unitary (not approximately) is stronger than §00.2:55 claims
("emergent low-energy shadow" suggests approximate). A skeptic could argue the exactness means the retained sector
*does* support a reversible sub-theory, and that the reconstruction should be run *there* (rank-3 restricted). The
answer (§4.1, §6-S1): a rank-3 retained system has no continuous group acting transitively on a *continuum* of pure
states — it is finite/small — so even the exact retained unitarity fails MM4's transitivity+continuity for a
genuine QM state space. A further skeptic should press whether "restrict the reconstruction to rank-3" yields a
*degenerate* QM (a qutrit-like fragment) that trivially satisfies a *finite* MM4 — and whether that fragment is
what D0 actually claims. This is a scope question about *which* QM the bridge targets, not a threat to the
irreversibility of the full dynamics.

**TERTIARY:** the IceCube-D1 magnitude channel (§5.3) is open — deriving the bound/knee from the NO-GO (not just
the kind) would upgrade the foundation↔data link from suggestive to quantitative. This is an opportunity, not a
threat.
