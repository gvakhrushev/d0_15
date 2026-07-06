# M1-QM NON-UNITARY DEPARTURE — the SCALE forged: is it owned or external?

**Status:** DRAFT / forge (self-contained). **REPAIRED after independent skeptic verdict
(WOUNDED, accepted in full) — see §9.** The original headline ("no owned object fixes the
departure RATE") contained a LEAP and has been RETRACTED to exactly what is owned. Companion
can-fail script: `_TASKS_CENTER_ATTACK/m1qm_departure_scale_check.py` (compute-first; the old
tautology gate has been replaced with the real K(9,11,13) Feshbach SVD + a tracing-channel
trace-loss gate). No registry row edited, no cert minted, no book/`.lean` touched. All registry
content below is a **proposal**. No `053040` row touched.

**Date:** 2026-07-05 (repaired 2026-07-05).

> **HEADLINE (repaired).** The owned emergent-QM dynamics that genuinely DEPARTS from unitarity
> is the **archive-tracing channel** `ρ↦PUρU†P` (`06.7:29`; parent M1_QM_GAP1 Block D), which
> loses probability for every carrier (trace mean `≈0.095≈φ⁻⁵`). Its per-tick retained-amplitude
> decay is `A_{t+1}=φ⁻¹A_t`, **FORCED** at `06.40`. So an **owned + forced RATE (`φ⁻¹`) DOES
> govern the departing owned dynamics.** What is genuinely **EXTERNAL** is only the mapping of
> that per-tick rate to the **IceCube plateau-knee ENERGY `E*`** (needs the unowned `κV(E)`/`ζ`
> bridge) — i.e. the *magnitude of the knee*, **not** "the rate." The retracted claim rested on
> the *post-conditioned, exactly-unitary complement* — the object that does **not** depart — and
> so mislabeled the non-departing object as "the departure" (§9, R1/R2).

**Question forged (respecting the M1_QM_GAP1 WOUND).** The clean "M1⇒¬MM4⇒non-unitary QM" was
DEMOTED (M1_QM_GAP1_MEMO.md banner) to *emergent-approximate QM + a controlled departure of
UNFIXED scale*. SOLID/owned: the fundamental readout `τ` is non-invertible
(`BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:373` verbatim), unitarity is "only an approximate,
emergent low-energy shadow" (`:375`). The IceCube-D1 link
(`ICECUBE_DECOHERENCE_FORM_MEMO.md`) is same-KIND (bounded/plateau) only, **silent on
magnitude** (its knee `E*`, `ζ`, `L0` are all NOT-OWNED). So: **is there an OWNED object that
fixes the SCALE at which the emergent unitary shadow departs from exact unitarity?** If yes ⇒
the IceCube link becomes real quantitative physics; if no ⇒ the "prediction" is honestly empty
on magnitude.

---

## 0. Bottom line first (verdict up top) — REPAIRED

**VERDICT: the departure RATE is OWNED + FORCED (`φ⁻¹`); only the IceCube plateau-knee ENERGY
`E*` is external.**

> **RETRACTED (leap):** the original §0 read "*No owned object fixes the departure rate of the
> emergent unitary shadow.*" That is a **leap** and is withdrawn. It defined "the departure"
> against the wrong object — the *post-conditioned, exactly-unitary complement* `W_eff|retained`
> (Block C) — which by construction does **not** depart. D0's owned reading of "the dynamics" is
> the **departing** archive-tracing channel, and *it* has a forced owned rate. See §9.

The object D0 owns as **the emergent-QM dynamics** is the **archive-tracing channel**
`ρ↦PUρU†P` — the operator `06.7:29` names ("what was traced away"), and the object the parent
M1_QM_GAP1 memo's own load-bearing correction (`M1_QM_GAP1_MEMO.md:304-312`;
`m1_qm_gap1_check.py:176-207`, `PASS_PHYSICAL_TRACING_CHANNEL_CONTRACTIVE`) established as the
one that **genuinely departs from unitarity** (it loses probability for every carrier/state:
trace surviving mean `≈0.095≈φ⁻⁵`, `max<1` across 300 carriers). Its per-tick retained-amplitude
decay is `A_{t+1}=φ⁻¹A_t`, **FORCED** at `06.40` (owner BOOK_01, `p+p²=1` ⇒ unique root
`p=φ⁻¹`; the book calls `A_t=φ⁻ᵗ` the **retained component/fraction**, `06.40:19,23`). Therefore:

**an owned + forced RATE (`φ⁻¹`) DOES govern the departing owned dynamics.**

What is genuinely **EXTERNAL** is the single further step of mapping that per-tick rate to the
**IceCube plateau-knee ENERGY `E*`**: that needs the composite bridge `κV(E)` and the floor value
`ζ`, both **NOT-OWNED** (`08.42:16` fixes only the domain `0<z<1`; `ICECUBE_DECOHERENCE_FORM_MEMO.md:332`
"Demo constants ζ=0.3, E*, L/L0=1 are NOT-OWNED"). So the honest cap is **narrower** than the
retracted one:

- **Owned + forced:** the *rate* of departure of the owned dynamics is `φ⁻¹` per tick (with the
  owned SI tick `τ₀=h/(38 m_e c²)` giving the tick a real, non-Planck SI scale, §5).
- **External:** the *IceCube plateau-knee ENERGY `E*`* (the rate→energy map), and separately the
  fact that `φ⁻¹` is **not** the *positive-floor plateau* rate (an O(1) floorless collapse is a
  different signature from the owned plateau — a real, **scoped** obstruction, §4/F-MAGNITUDE).

**Two things that DO survive as computed obstructions (scoped, per §9 R5):**
1. **`φ⁻¹` is not the IceCube positive-floor PLATEAU-knee rate.** `φ⁻¹≈0.618`/tick is **O(1)**:
   under it coherence is gone within a handful of ticks — a *floorless* collapse, whereas the owned
   IceCube-D1 flagship is a **bounded plateau with a strictly positive floor** (`inf x=1−ζ>0`).
   This is a genuine wall — but only between `φ⁻¹` and the *plateau knee*, **not** between `φ⁻¹`
   and "any departure rate." (The tracing channel's own trace loss is the departure `φ⁻¹` governs.)
2. **The knee ENERGY needs an unowned bridge.** `φ⁻¹` is a per-tick *ratio*; turning it into a
   knee *energy* requires the unowned `κV(E)` map. The near-miss cannot self-supply its energy axis.

**Owned SI scale of the tick (genuinely owned):** `Λ_act = h/τ₀ = 38 m_e c² ≈ 19.42 MeV`
(`BOOK_03:300`, `D0-METRO`). **Not** Planck-scale and **not** IceCube-tuned (`≈5×10⁵` below the
HESE floor `~10 TeV`). The owned rate carries this owned SI tick; what it does **not** carry is the
knee *energy* (needs `κV(E)`).

**Honest net:** the IceCube-D1 **knee-ENERGY** channel stays OPEN exactly as
`ICECUBE_DECOHERENCE_FORM_MEMO.md §5.3 / G1` and `M1_QM_GAP1_MEMO.md §8-TERTIARY` already conceded.
This memo does **not** claim the rate is external (that was the leap). It records that the
departure **rate** is owned+forced (`φ⁻¹` on the tracing channel), and that the only external
object is the **rate→knee-energy map**.

---

## 1. What "the departure scale" must be (pinned, so the near-misses can be judged)

The object we need to own, to make the IceCube link quantitative, is **a rate `Γ_dep` (or an
energy scale `E_dep`) at which the emergent unitary evolution on the OBSERVABLE (retained) sector
departs from exact unitarity** — i.e. the coefficient in a law like
`coherence(E) = floor + (1−floor)·f(E/E_dep)`, where `E_dep` sets *where* the plateau knee sits.
Three things it must satisfy to be OWNED-as-the-departure-scale (not merely φ-power-coincident):
1. **RIGHT SECTOR:** it must govern the *retained* observable evolution. **(REPAIRED — §9 R1.)** The
   owned dynamics is the **archive-tracing channel** `ρ↦PUρU†P` (`06.7:29`), and its **retained**-
   amplitude decay is `A_t=φ⁻ᵗ` (`06.40:19,23` calls `A` the *retained* component). So `φ⁻¹`
   satisfies this: it *is* the rate of the retained observable amplitude of the departing channel.
   The original memo mis-read this criterion as excluding `φ⁻¹` by pointing at the *post-conditioned
   complement* (exactly unitary), which the parent already ruled is NOT the dynamics.
2. **RIGHT KIND:** it must be a *rate of unitarity loss*, dimensionally a decoherence rate / knee
   energy, not a static coupling coefficient. `φ⁻¹` is a per-tick decay *rate* (right kind); what it
   is missing to become a knee *energy* is the `κV(E)` map (the external step).
3. **OWNED BY MECHANISM:** the mechanism, not a numerical match, must name it as that rate — the
   discipline's explicit bar (task: "a φ-power ≈ an IceCube energy is NOT ownership"). Here the
   mechanism (`06.40` `p+p²=1`) FORCES `φ⁻¹` as the per-tick retained decay — a *mechanism* naming,
   not a numerical coincidence. (The φ-power/IceCube-*energy* coincidence bar still applies to `E*`,
   which is why the knee **energy** stays external, §5.)

## 2. Candidate scales — verbatim ownership audit (each grepped/read on disk 2026-07-05)

| candidate | owned? (verbatim file:line) | is it a *rate of retained-shadow departure*? |
|---|---|---|
| Pisot contraction `|ψ|=φ⁻¹` | YES, `CLAIM_TO_LEAN_MAP.csv:270` `D0-PISOT-CONTRACTION-TIME-ARROW-001` LEAN_PROVED; book `06.36` | NO — it is the *arrow direction* (Galois-conjugate contraction), a sign/orientation object, not a decoherence rate. §3.1 |
| per-tick decay `A_{t+1}=φ⁻¹A_t` | YES, `06.40:23` FORCED (owner BOOK_01 `p+p²=1`) | **YES (REPAIRED)** — it is the per-tick decay of the **retained** amplitude (`06.40:19,23` "retained component/fraction") of the **departing archive-tracing channel** D0 owns as the dynamics (`06.7:29`; parent Block D). This IS the owned departure rate. §3.2. (Old "wrong sector" claim retracted — §9 R1.) |
| owned SI tick `τ₀=h/(38 m_e c²)`, `Λ_act=38 m_e c²` | YES, `BOOK_03:296,300` `D0-METRO` | it is a *scale* (`≈19.42 MeV`) but of the tick, not of a departure; only relevant IF a departure *rate* per tick were owned (it is not). §3.2 |
| α-seam depth `φ⁻¹⁷=φ⁻⁵·φ⁻¹²` | YES, `BOOK_02 …02.13:82,87` `D0-ALPHA-HOLONOMY-*` | NO — it is the *smallness of the α coupling residual* (seam ξ₅ × EW transport), a **static coupling coefficient**, not a time-domain unitarity-loss rate. §3.3 |
| δ₀ cascade `δ_{-n}=δ₀^{n+1}` | YES, `BOOK_02:548`, `BOOK_01:1122`, cert `vp_dim_ladder_compact.py` | NO — a *dimension-ladder half-gap* quantization, not a decoherence rate. §3.4 |
| archive-tracing determinant balance `active×archive=1` | YES, `08.42:29` verbatim | It fixes the *shape* + the positive floor `1−ζ`, but **ζ is explicitly NOT-OWNED** (`08.42:16`: domain `0<z<1` only). §3.5 — this is the direct proof the magnitude is external. |
| tick nilpotency depth `≤12` | YES (DRAFT), `TICK_COUPLING_SCHUR_MEMO.md:39-46` `(QUQ)^12=0` | NO — a *finite ladder length* (how many circulations before return), not a rate; it bounds the polynomial DEGREE, not the decoherence timescale. §3.6 |

**Reading of the table (REPAIRED — §9 R1/R2).** The per-tick `φ⁻¹` (`06.40`, FORCED) **is** owned
as *the departure rate of the owned dynamics* — the archive-tracing channel `ρ↦PUρU†P` (`06.7:29`;
parent Block D). The book calls `A_t=φ⁻ᵗ` the **retained** component (`06.40:19,23`), so it is not a
"leaked/wrong-sector" object. The Pisot `φ⁻¹` (`06.36`) is the same *number* but owned as the arrow
*orientation* (§3.1), a distinct mechanism; that remains a genuine wrong-KIND note. The genuine
**energy scale** `E*` is *not owned* (needs the `κV(E)`/`ζ` bridge, `08.42:16`,
`ICECUBE…:332`) — **this is the one external object**. `Λ_act` is the owned tick action (`≈19.42
MeV`), the SI scale the owned rate carries. The α-depth and δ₀ cascade are static coefficients
(wrong KIND). Nilpotency-12 is a degree, not a rate. **Net: the rate is owned; only the knee
ENERGY `E*` is external.**

## 3. Per-candidate detail (the mechanism check, where the leap would happen)

### 3.1 Pisot `|ψ|=φ⁻¹` — arrow, not rate
`06.36`/`:270`: "arrow of time = Pisot contraction of the Galois conjugate (`φ>1` expands;
`|ψ|<1` contracts) … the irreversible time direction." The Galois conjugate `ψ` **orients** time
(one contracting eigendirection ⇒ one arrow); its *modulus* `φ⁻¹` is not asserted anywhere as a
per-unit-time coherence-loss rate. Reading `|ψ|` as a decoherence rate is the coincidence-trap:
`|ψ|=φ⁻¹` numerically equals the per-tick decay of §3.2, but the Pisot owner's mechanism is
*sign/orientation of the toral spectrum*, not amplitude bookkeeping.

### 3.2 The departure rate: per-tick decay `A_{t+1}=φ⁻¹A_t` (§06.40) — RIGHT rate, RIGHT object (REPAIRED)
This is the rate that governs the **owned departing dynamics**. Verbatim `06.40:3-23`:
> `A_{t+1}=pA_t`, `B_{t+1}=B_t+p²A_t`, `p=φ⁻¹`; `A_t=p^tA_0`, `B_t=(1-p^t)A_0`. … "The **retained
> component** never vanishes in finite time." "The **retained fraction** `p=φ⁻¹` is **not** a free
> parameter … Status: **FORCED** (owner BOOK_01: `p+p²=1` unique admissible root `p=φ⁻¹`)."

> **CORRECTION (R1/R5 — the original text here was the leap's core mislabel).** The original §3.2
> called `A` "the ACTIVE/RETAINED-flux amplitude … the SHARE that leaks to the archive," reading
> `φ⁻¹` as "the leakage rate of the full amplitude" and therefore "wrong sector." That is **wrong
> on two counts**, both verifiable on disk:
> 1. **The book calls `A` the RETAINED component**, not the leaked share: `06.40:19` "The **retained
>    component** never vanishes," `06.40:23` "The **retained fraction** `p=φ⁻¹`." It is `B`
>    (`B_{t+1}=B_t+φ⁻²A_t`, `:25`) that accumulates the **archived** share `φ⁻²`. So `A_t=φ⁻ᵗ` is
>    the decay of the **retained** amplitude — the observable sector — not of a traced-away flux.
> 2. **"Wrong sector" was an equivocation.** The exactly-unitary object cited to define "the
>    departure" (`W_eff|retained`, singular values `[1,1,1]`) is the **post-conditioned coherent
>    complement**, which the parent M1_QM_GAP1 memo's own load-bearing correction
>    (`M1_QM_GAP1_MEMO.md:304-312`) explicitly ruled is **NOT "the dynamics"** — it is the
>    "resolvent-summed no-net-leak object." D0's owned reading of the dynamics (`06.7:29`) is the
>    **archive-tracing channel** `ρ↦PUρU†P`, which **does** lose probability (parent Block D,
>    `PASS_PHYSICAL_TRACING_CHANNEL_CONTRACTIVE`, trace mean `≈0.095≈φ⁻⁵`). The retained-amplitude
>    decay rate of *that departing channel's* ladder is exactly `φ⁻¹`.

So D0 **owns a forced per-tick departure rate `φ⁻¹`** of its own dynamics, with an owned SI tick
scale `τ₀=h/(38 m_e c²)`. `φ⁻¹` is **not** a different sector from the departure — **it is the
departure rate of the tracing channel D0 owns as the dynamics.** What remains external is only the
map from this per-tick rate to a knee *energy* (§4/F-DIMENSION) and the separate, *scoped* fact that
`φ⁻¹` is not the *positive-floor plateau* rate (§4/F-MAGNITUDE). See §9 for the repair provenance.

### 3.3 α-seam depth `φ⁻¹⁷` — static coupling coefficient, WRONG kind
`02.13:82,87`: `α_{D0}^{-1}=α_top^{-1}+φ⁻¹⁷(1+h_{KS}sinθ_seam)`, "depth `φ⁻¹⁷=φ⁻⁵·φ⁻¹²` — the
seam `ξ₅` times the electroweak transport." This owns the *smallness of the fine-structure residual*
— a dimensionless correction to a **coupling constant**, static in time. A decoherence *rate* has
dimensions of inverse time (or a knee energy); `φ⁻¹⁷` is a pure-number coupling depth. Matching it
to an IceCube energy would be exactly the forbidden coincidence (no mechanism names `φ⁻¹⁷` as a
unitarity-loss rate).

### 3.4 δ₀ cascade `δ₀^{n+1}` — dimension ladder, WRONG kind
`BOOK_02:548`: "the half-gap cascade closes as `δ_{-n}=δ₀^{n+1}`"; `BOOK_01:1122` same, cert
`vp_dim_ladder_compact.py`. This is the `φ`-ladder **dimension** quantization (`Q(D)=φ^{D-4}`), a
static spectral-gap structure. Not a rate.

### 3.5 Determinant balance `08.42:29` — owns SHAPE + floor, but ζ is NOT-OWNED (the direct proof)
`08.42:29` "active localization x archive expansion = 1" and `:16` "positive but bounded and
saturating: `L(V)→−d_τ log(1−z)`." This owns the **functional shape** (bounded, saturating) and the
**existence** of a positive floor `1−ζ`. But `:16` fixes only the **domain** `0<z<1`; **no line
fixes the value of ζ (or κV(E), or E*)**. `ICECUBE_DECOHERENCE_FORM_MEMO.md:247,332` states this
verbatim: "what is NOT owned: the composite bridge `κV(E)`… and the values of `ζ, E*, L0`"; "Demo
constants ζ=0.3, E*, L/L0=1 are NOT-OWNED." **This is the cleanest single proof that the magnitude
is external: the object that would set the knee is the one D0 explicitly declares unowned.**

### 3.6 Nilpotency depth `≤12` — finite ladder LENGTH, not a rate
`TICK_COUPLING_SCHUR_MEMO.md:39-46`: `(QUQ)^12=0` exactly (per-zone indices 8/10/12). This bounds
the Neumann ladder to a **finite polynomial degree** (`≤11` circulations) — how *many* archive
circulations before coherent return — not the *rate* at which coherence is lost per circulation.
It fixes the envelope's polynomial *order* (feeding the `8:10:12` integer triple `D3`, itself
reading-conditional and unowned-carrier), not its energy scale.

## 4. What separates `φ⁻¹` from the IceCube plateau-KNEE — two scoped walls (REPAIRED)

> **RETRACTED (R1/R2):** the original §4 listed **F-SECTOR** as a falsifier of "`φ⁻¹` is the
> departure rate," resting on `W_eff|retained` being exactly unitary. That is withdrawn: the
> exactly-unitary object is the **post-conditioned complement**, which the parent memo already
> ruled is **not "the dynamics"** (`M1_QM_GAP1_MEMO.md:304-312`). The departing owned object is the
> **tracing channel**, whose retained-amplitude rate **is** `φ⁻¹`. So there is **no sector wall**
> between `φ⁻¹` and the departure. What survives are two *narrower* walls — between `φ⁻¹` and the
> **IceCube plateau-KNEE**, not between `φ⁻¹` and "any departure rate":

- **F-SECTOR — RETRACTED (do not use as a wall).** `W_eff|retained` unitary (singular values
  `[1,1,1]`, real `B†W_effB` SVD, script gate `F_COMPLEMENT_POSTCOND_IS_UNITARY_NOT_THE_DYNAMICS`)
  witnesses only that the *post-conditioned complement* does not depart. Per `M1_QM_GAP1_MEMO.md:304-312`
  that object is **not** the dynamics; the dynamics is the tracing channel, which **does** depart
  at rate `φ⁻¹` (script gate `F_OWNED_TRACING_CHANNEL_DEPARTS_AT_PHIM1`, trace mean `≈0.095≈φ⁻⁵`).
  ⇒ **This is not a wall against `φ⁻¹`.**

- **F-MAGNITUDE — SURVIVES, SCOPED (computed).** An O(1) per-tick rate `φ⁻¹` gives coherence
  `~φ⁻ᵗ→0` within a handful of ticks — a *floorless* collapse. The owned IceCube-D1 flagship is a
  **positive-floor plateau** (`08.42:16`, `inf x=1−ζ>0`). So `φ⁻¹` is **not the plateau-knee rate**
  — but this bounds only the *IceCube positive-floor plateau*, **not** "any departure rate." (The
  tracing channel's per-carrier trace loss is the genuine departure `φ⁻¹` governs; it is not a
  positive-floor plateau, and that is consistent — the plateau is a *further* physical object with
  a floor-restoring mechanism, the determinant balance `08.42`, that `φ⁻¹` alone does not encode.)

- **F-DIMENSION — SURVIVES (owned).** The plateau knee `E*` is a *knee energy* set by the unowned
  bridge `κV(E)` and `ζ` (`08.42`), whereas `φ⁻¹` is a dimensionless per-tick ratio. Turning the
  owned per-tick *rate* into a knee *energy* requires the unowned `κV(E)` map (G1). The owned rate
  cannot self-supply its own energy axis. **This is the single genuinely external object.**

**Net (repaired):** the departure **rate** is owned+forced (`φ⁻¹`, tracing channel). The only
external steps are (i) the map from that per-tick rate to a knee **energy** (`κV(E)`, unowned), and
(ii) the separate, *scoped* fact that `φ⁻¹` is not the *positive-floor plateau* rate. The honest
verdict is **rate-owned, knee-energy-external**, not "no owned rate."

## 5. Observability arithmetic (for the record; the ENERGY step remains external)

The departure **rate** `φ⁻¹` is owned+forced (§3.2 REPAIRED) and carries the owned SI tick
`τ₀=h/(38 m_e c²)`, whose action scale is `Λ_act=38 m_e c²≈19.42 MeV` (`BOOK_03:300`). This is the
owned SI scale of the *tick*. Mapping the per-tick rate to a knee **energy** `E*` is the step that
is **not** owned (needs `κV(E)`), so the following is about where the *tick* scale sits, not a knee
prediction:
- **Not Planck-scale** (so the owned scale is a real physical energy, not vacuous): `19.42 MeV ≪ 10¹⁹ GeV`.
- **Not IceCube-tuned:** the HESE window is `~10 TeV .. few PeV` (`≈10⁴..10⁷ GeV`); `Λ_act` sits
  `≈5×10⁵` *below* the window floor. So there is **no** φ-power/IceCube-*energy* coincidence to
  seize — which is *good discipline*: the owned **rate** is genuinely owned by mechanism (`06.40`),
  and the missing knee **energy** is honestly missing (no accidental numerical match papering over
  the unowned `κV(E)`).
- **Net:** the owned rate + owned tick give a real, non-Planck, non-tuned per-tick SI timescale. The
  knee **energy** `E*` is the only external object; §5 records that the tick scale is *not* it, and
  that no coincidence is being over-read to fake it.

## 6. Adversarial skeptic pass (§05.8.R hostile self-audit)

Pre-registered attack surface (committed before grading):

**S1 — "The per-tick `φ⁻¹` (§06.40, FORCED) IS an owned departure rate; you are under-claiming."**
**Verdict: SUSTAINED (reversed by the independent skeptic — §9 R1/R2; this is the load-bearing
correction).** The original memo OVERRULED S1 by calling `φ⁻¹` "the trace-production rate of the
full active amplitude … wrong sector." That rested on an **equivocation**: it defined "the
departure" against the *post-conditioned exactly-unitary complement* `W_eff|retained`, which the
memo's **own parent** (`M1_QM_GAP1_MEMO.md:304-312`, Block D) already ruled is **NOT "the
dynamics."** D0's owned dynamics (`06.7:29`) is the **departing archive-tracing channel**, and the
book calls `A_t=φ⁻ᵗ` the **retained** component (`06.40:19,23`), not a leaked share. So `φ⁻¹` **is**
the forced per-tick departure rate of the owned dynamics. Under-claiming to "no owned rate" was
itself the over-claim pattern in reverse (a tautology dressed as a finding: "the object that does
not depart, does not depart"). **What genuinely remains external is only the rate→knee-ENERGY map
(`κV(E)`, `E*`), not the rate.** Held to the discipline bar in the *other* direction.

**S2 — "`Λ_act=19.42 MeV` is an owned SI scale near the seam; that IS the departure scale."**
**Verdict: PARTIALLY OVERRULED (repaired).** `Λ_act` is the owned scale of the *tick action*
(`h/τ₀`); the owned departure *rate* per tick (`φ⁻¹`, §3.2 REPAIRED) **does** convert to an SI
*per-tick timescale* via `τ₀`. What `Λ_act` does **not** give is the IceCube *knee energy* `E*` —
that still needs the unowned `κV(E)` map (§4/F-DIMENSION). Also `Λ_act` is not IceCube-tuned (§5),
so there is no knee coincidence to over-read.

**S3 — "Determinant balance `08.42:29` owns the floor `1−ζ`, so the departure magnitude IS owned."**
**Verdict: OVERRULED.** It owns floor *existence* and *shape* (bounded/saturating), which is the
KIND already conceded by both parent memos. It does **not** own `ζ`'s value (`08.42:16`: domain
`0<z<1` only; `ICECUBE…:332` "NOT-OWNED"). Shape-owned + value-unowned = KIND without MAGNITUDE.

**S4 — "This is just relabelling the existing 'silent on magnitude' concession; it adds nothing."**
**Verdict: OVERRULED (this is the memo's positive content — repaired).** The parent memos *asserted*
silence on magnitude; this memo **enumerates every owned candidate scale** and, after the repair,
**pins which one IS the owned departure rate** (per-tick `φ⁻¹` on the tracing channel, §3.2) and
**exactly what remains external** (the rate→knee-ENERGY map `κV(E)`, §4/F-DIMENSION). The residual is
now *narrower and sharper* than the parent's "silent on magnitude": rate-owned, knee-energy-external.

**S5 — "Citation integrity: does `06.7:373` / `06.40` / `BOOK_03:300` actually say this?"**
**Verdict: SUSTAINED-AND-HONORED (re-verified 2026-07-05).** Verified on disk: the readout-τ
non-invertibility and the "reversible readout would need an inverse role `τ⁻¹`… storing what was
traced away" language is at the `§06.7` per-section file `0008__06.7__….md:27,29` (verbatim; the
task's "06.7:373" is the concatenated-book line). The emergent-shadow phrase ("Unitarity is
recovered only as an approximate, emergent low-energy shadow") is on the same `:29`. The per-tick
law is `06.40` = `0044__06.v15__….md`, with `A` the **retained** component at `:19,23` (verbatim).
`LEAN_ASSUMPTION_LEDGER.csv` has **25 rows** (no row 26), consistent with the WOUND's phantom-row
finding. **Citation caveat (honored):** `BOOK_03:296/:300` is a **concatenated-book** line reference
and **no concatenated BOOK_03 exists on disk to resolve it**; the *content* (`τ₀=h/(38 m_e c²)`,
`Λ_act=h/τ₀=38 m_e c²`) IS verified verbatim in the per-section file
`0007__03.6__single-full-cycle-action-section.md:14,18`. Treat `BOOK_03:300` as "content-verified,
line-number-unresolved" (same status as `06.7:373`), not as an owned line anchor.

**Net skeptic outcome (REPAIRED):** the original "scale-external" verdict **did not survive** the
*independent* skeptic (§9): S1 is now SUSTAINED — `φ⁻¹` **is** the owned+forced departure rate of
the owned dynamics (the tracing channel). The surviving verdict is **rate-owned, knee-ENERGY-
external**. The internal self-audit above (S1 OVERRULED) was the leap; it is corrected here.

## 7. Registry implication (proposal only — NOT applied)

The honest registry action is a **note**, not a row (no new *energy* owner is warranted; the *rate*
owner `φ⁻¹` already exists via `06.40`/BOOK_01):

- **Proposed note on the IceCube slot** (`D0-PASSPORT-ICECUBE-HESE-001` / the D1 flagship): record
  that the departure **rate** of D0's owned dynamics is the FORCED per-tick `φ⁻¹` (`06.40`, owner
  BOOK_01) of the **archive-tracing channel** (`06.7:29`; parent M1_QM_GAP1 Block D), SI-scaled by
  the owned tick `τ₀=h/(38 m_e c²)`; and that what is **external** is only the map from that per-tick
  rate to the IceCube plateau-knee **ENERGY `E*`** (the unowned `κV(E)`/`ζ` bridge), plus the scoped
  fact that `φ⁻¹` is not the *positive-floor plateau* rate (§4/F-MAGNITUDE). This upgrades the
  existing "silent on magnitude" caveat to a *checked* "rate-owned, knee-energy-external."
- **No edit** to `CLAIM_TO_LEAN_MAP.csv` / `LEAN_ASSUMPTION_LEDGER` / any `.lean` / any `053040` row.

## 8. What a further skeptic must attack

- **PRIMARY (repaired):** contest that the archive-tracing channel is "the dynamics." If a further
  reading owned a *different* object as the emergent-QM dynamics whose departure rate is NOT `φ⁻¹`,
  the rate-ownership would reopen. But `06.7:29` names the tracing channel as the readout, and the
  parent Block D (`M1_QM_GAP1_MEMO.md:304-312`) already adjudicated this against the post-conditioned
  complement — so this attack must overturn a settled parent adjudication.
- **SECONDARY:** own the `κV(E)` bridge (G1 of `ICECUBE…`). Owning `κV(E)` + `ζ` would convert the
  owned per-tick **rate** into an owned knee **energy** — the single edit that would flip the knee
  energy from external to owned. Until then, the knee **energy** (not the rate) is external.
- **TERTIARY:** contest F-MAGNITUDE — argue the physical *plateau* departure composes many `φ⁻¹`
  ticks with the determinant-balance floor-restoring mechanism (`08.42`) so the *effective plateau*
  rate is not O(1). If someone owns that composition explicitly, `φ⁻¹` could additionally be tied to
  the *plateau-knee* rate — but the composition is again the unowned `κV(E)` marriage.

---

## 9. Independent skeptic verdict + repair log (accepted in full)

**Verdict: WOUNDED — leap found in the headline. Accepted in full; all five repairs (R1–R5)
applied and re-verified 2026-07-05.**

**The leap (verbatim):** the memo took the OWNED fact *"`W_eff|retained` is exactly unitary"*
(Block C, `PASS_SHADOW_UNITARY_ON_RETAINED`) and asserted the STRONGER conclusion *"therefore
`φ⁻¹` is wrong-sector and no owned object fixes the departure RATE."* The equivocation: the
exactly-unitary complement is the **post-conditioned no-net-leak object** that the memo's own parent
(`M1_QM_GAP1_MEMO.md:304-312`; `m1_qm_gap1_check.py:176-207`, Block D) already ruled is **NOT "the
dynamics."** D0's owned reading of the dynamics (`06.7:29`) is the **archive-tracing channel**
`ρ↦PUρU†P`, which is NOT trace-preserving (loses probability for every carrier/state, trace mean
`≈0.095≈φ⁻⁵`). The retained-amplitude decay of that departing channel is `A_{t+1}=φ⁻¹A_t`, FORCED
at `06.40`. So an **owned+forced rate (`φ⁻¹`) DOES govern the departing owned dynamics.** The
headline "no owned object fixes the departure RATE" was true only against the departure-identically-
zero shadow — a tautology dressed as a finding — not against the object D0 actually owns as the
dynamics. The book itself (`06.40:19,23`) calls `A_t=φ⁻ᵗ` the **retained component/fraction**,
contradicting the memo's relabel of it as pure "leakage of the full amplitude."

**Repairs applied:**

- **R1 (LEAP, load-bearing) — DONE.** Headline restricted to what survives: the **IceCube
  plateau-knee `E*` magnitude** is external; the broad claim "no owned object fixes the departure
  RATE" is **RETRACTED**. `φ⁻¹` is not a different sector from the departure — it *is* the departure
  rate of the tracing channel (banner, §0, §3.2, §4, table row, §1 criteria). What is external is
  only the per-tick-rate → knee-ENERGY map (`κV(E)`/`ζ`), not the rate.
- **R2 (must engage parent, load-bearing) — DONE.** The memo now cites and rebuts
  `M1_QM_GAP1_MEMO.md:304-312` and Block D explicitly (§0, §3.2, §4/F-SECTOR, §6/S1, §8) — the
  tracing channel loses probability for every carrier (trace mean `≈0.095=φ⁻⁵`). It no longer rests
  F-SECTOR on Block C's unitarity, which the parent demoted. Grep confirmed the pre-repair memo
  never mentioned "tracing channel" / "Block D" / "trace-preserving" — the silent drop that produced
  the equivocation. Now present.
- **R3 (script non-tautology, KILL GATE 3) — DONE.** The old `F_SECTOR_RETAINED_SHADOW_UNITARY` gate
  computed `|∏ unit-modulus phases|`, which is **identically 1 for ANY `n`** (verified: `n∈{2,3,4,5,
  9,11,13,100}` all → `1.0`) — it could not fail and did not reproduce the Feshbach K(9,11,13)
  shadow. Replaced with the **real `B†W_effB` SVD** (from `m1_qm_gap1_check.py:154-161`,
  `F_COMPLEMENT_POSTCOND_IS_UNITARY_NOT_THE_DYNAMICS`) **and** a new gate
  `F_OWNED_TRACING_CHANNEL_DEPARTS_AT_PHIM1` that computes the tracing-channel trace loss (mean
  `0.0948≈φ⁻⁵`, max `0.293<1` over 300 carriers) — the object that DOES depart. The script now tests
  the true adjudication.
- **R4 (script assertions) — DONE.** `F_DIMENSION` and `CTRL_IF_ZETA_OWNED` were hardcoded
  `zeta_owned_value=None` restatements, not computed checks. Relabeled as **owned-fact assertions**
  (`ASSERT_KNEE_ENERGY_ESTAR_IS_EXTERNAL`, `ASSERT_IF_KNEE_BRIDGE_OWNED_ENERGY_FLIPS`) — `ζ`
  NOT-OWNED per `ICECUBE_MEMO:332` (verified verbatim) and `08.42:16` (domain `0<z<1` only,
  verified) — not gates that "can fail the conclusion."
- **R5 (keep what survives) — DONE.** F-MAGNITUDE (`φ⁻ᵗ→0` floorless O(1)) and the observability
  arithmetic (`Λ_act=19.42 MeV`, non-Planck, `≈5×10⁵` below the IceCube HESE floor, no
  φ-power/IceCube coincidence) are arithmetically correct and retained, but **scoped** to "`φ⁻¹` is
  not the IceCube positive-floor-PLATEAU knee" (§4/F-MAGNITUDE, §5) — narrower than "`φ⁻¹` is not any
  departure rate."

**Errors of record (owned-fact provenance, all re-verified on disk 2026-07-05):**
1. **Headline leap (RETRACTED):** "no owned object fixes the departure RATE" ⇒ the actual owned
   status is *rate-owned (`φ⁻¹`, tracing channel), knee-ENERGY-external*. Cause: equivocation on
   which object is "the dynamics" (post-conditioned complement vs departing tracing channel).
2. **Book mislabel (CORRECTED):** the memo called `A_t=φ⁻ᵗ` "leakage of the full amplitude / wrong
   sector"; the book (`06.40:19,23`, verified verbatim) calls it the **retained** component/fraction.
   `B` (`:25`, `B_{t+1}=B_t+φ⁻²A_t`) is the archived share.
3. **Script tautology (FIXED):** `shadow_singular_value(n)=|∏ unit phases|≡1 ∀n` — could not fail;
   replaced with the real SVD + tracing-channel trace-loss gate.
4. **Parent silently dropped (FIXED):** pre-repair memo never cited Block D / `:304-312` / the
   tracing channel; now engaged and rebutted.

**Re-verification:** `python3 m1qm_departure_scale_check.py` → all gates PASS, exit 0, with the
repaired (non-tautological) gates: `F_OWNED_TRACING_CHANNEL_DEPARTS_AT_PHIM1` (trace mean 0.0948,
max 0.293<1), real `B†W_effB` SVD `[1,1,1]`, scoped F-MAGNITUDE, relabeled owned-fact assertions.

**Owned vs still-open (residual):**
- **OWNED (repaired):** the departure **rate** of D0's owned emergent-QM dynamics is the FORCED
  per-tick `φ⁻¹` (`06.40`, owner BOOK_01 `p+p²=1`) of the archive-tracing channel (`06.7:29`; parent
  Block D), carrying the owned SI tick `τ₀=h/(38 m_e c²)`.
- **STILL OPEN / external:** (i) the map from that per-tick rate to the IceCube plateau-knee **ENERGY
  `E*`** (unowned `κV(E)`/`ζ`, `08.42:16`, `ICECUBE_MEMO:332`); (ii) the *scoped* fact that `φ⁻¹` is
  not the *positive-floor plateau* rate unless the determinant-balance composition (itself the
  unowned `κV(E)` marriage) is owned. No registry row edited; §7 note is a proposal only; no `053040`
  row touched.
