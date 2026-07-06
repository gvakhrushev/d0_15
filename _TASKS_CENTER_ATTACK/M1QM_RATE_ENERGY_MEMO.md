# M1-QM / IceCube RATE→ENERGY bridge — is the departure ENERGY owned, or only the rate?

**Status:** DRAFT / forge (self-contained). Companion can-fail script:
`_TASKS_CENTER_ATTACK/m1qm_rate_energy_check.py` (6 gates, all PASS, exit 0; NOT a minted cert).
No registry row edited, no cert minted, no book/`.lean` touched. All registry content below is a
**proposal**. No `053040` row touched. **Date:** 2026-07-05.

> **HEADLINE (owned exactly, no leap).** The per-tick departure **rate** is owned+forced (`φ⁻¹`,
> `06.6.A:296`) **and the per-tick TIME is also owned+forced** (`τ₀ = h/(38 m_e c²)`, `03.6:14` /
> `03.19:12` via `C_e = 1/(2(2γ−1)) = 1/38`). Combining them gives a **genuinely owned physical
> decoherence RATE `Γ₀ = φ⁻¹/τ₀ ≈ 2.90×10²¹ s⁻¹`, equivalently `ħ`-free `hΓ₀ = φ⁻¹·Λ_act ≈ 12.0
> MeV`.** But `Γ₀` is a **single, ENERGY-INDEPENDENT constant.** The IceCube kernel
> `Γ(E,z) = δ₀²·log(1+z)·H_φ(E/E₀)` needs the decoherence to **scale with neutrino energy E**;
> **no owned object supplies that E-dependence.** The energy axis `E₀`/knee, the redshift scale in
> `log(1+z)`, and the width in `H_φ` are all bare, unowned constants in the passport code. **OUTCOME
> = EXTERNAL on the E-dependence:** the rate AND its SI clock are owned; the **rate→energy MAP (how
> decoherence grows with E) is the single named external input.** This is *stronger* than the parent
> `M1QM_DEPARTURE_SCALE_MEMO` (which owned only the rate and left the whole SI clock implicit): the
> physical *rate* is now nailed to a real MeV-scale number — and that makes it *sharper* that the
> number is energy-flat and therefore **cannot be the IceCube kernel by itself**.

---

## 0. The question, pinned

To make the M1-QM/IceCube departure QUANTITATIVE you must own the map

```
per-tick departure rate (φ⁻¹)  ──÷ tick time τ₀──▶  physical rate Γ  ──E-dependence──▶  Γ(E,z) kernel
```

The parent memo (`M1QM_DEPARTURE_SCALE_MEMO.md`) established the **rate** `φ⁻¹` is owned+forced and
left "the rate→knee-ENERGY map" as external. This memo forges the middle and the last arrow and asks
STRICTLY: does the owned tick `τ₀` + owned scene give the kernel's **E-dependence** and `E₀`, or is
only a *constant* rate owned while the **E-dependence stays external**? The discipline bar
(anti-numerology): a φ-power near an IceCube energy is NOT ownership — the **E-dependence must be
owned by a MECHANISM** (energy entering the tick count by an owned law).

## 1. What IS owned (verbatim file:line, each read on disk 2026-07-05)

| owned object | verbatim anchor | status |
|---|---|---|
| per-tick departure rate `W_ext = φ⁻¹` | `BOOK_06…:296` **[THE 6.1.2]** "Golden split of the evolution step — `W_ext=φ⁻¹`, `W_int=φ⁻²`"; proof `:308` `W_ext²+W_ext−1=0` | **FORCED** |
| per-tick TIME `τ₀ = h/(38 m_e c²)` | `BOOK_03/0007__03.6…:14` "τ₀ = h/(38 m_e c²)"; `:18` "Λ_act = h/τ₀ = 38 m_e c²" | owned (SI section) |
| the `38` coefficient | `BOOK_03/0021__03.19…:12` "C_e = 1/(2(2γ−1)) = 1/38"; `:14` "Λ_act = 38 m_e c²" | owned (γ integer-pinned: `2(2γ−1)=38 ⇔ γ=10`, unique — script GATE 1) |
| tick is a **fixed clock unit** (no E slot) | `BOOK_07/0005__07.4…:6` "ℓ₀=1, τ₀=1, c=1"; `:74-79` SI export `τ₀=h/(38 m_e c²)` "used only as metrology" | owned (metrological section, energy-independent) |
| internal heat-trace tick `τ₀=φ⁻¹⁶` | `BOOK_06…:73` "tau0 = epsilon^2 = phi^-16", `:329,949`, `:952` **FORCED** | owned but **DIMENSIONLESS** (phase↔time map `u=ε²t`); *distinct* object, `:77` "must not be conflated" with the SI `τ₀` |
| δ₀ = 1/(2φ³) | passport `vp_neutrino_phason_decoherence_passport.py:176-177` `delta0 = 1.0/(2.0*phi**3)` | owned coefficient (the kernel *prefactor*) |

**Combining the first three (the forge):** `Γ₀ = φ⁻¹ / τ₀`. Numerically (script GATE 2, CODATA
SI representatives for the external unit section only):

```
τ₀ = h/(38 m_e c²) = 2.1298×10⁻²² s
Λ_act = 38 m_e c²  = 19.418 MeV
Γ₀ = φ⁻¹/τ₀        = 2.9018×10²¹ s⁻¹
hΓ₀ = φ⁻¹·Λ_act    = 12.001 MeV      ← the owned physical decoherence rate, as an energy
```

This is a **real, owned, non-Planck, non-vacuous decoherence rate**. It is owned by MECHANISM on
both factors: `φ⁻¹` by `W_ext²+W_ext−1=0` (`:308`), `τ₀` by the electron full-cycle Euler point with
the integer-pinned `38` (`03.19:12`). **No numerology:** `12 MeV` is *not* tuned to any IceCube
energy — it sits `~10⁶` *below* the HESE window (`10 TeV..few PeV = 10⁷..10⁹ MeV`), so there is no
φ-power/IceCube coincidence being seized (script GATE 2/5).

## 2. What is NOT owned — the E-dependence (the strict check, where the leap would happen)

The IceCube kernel is `Γ(E,z) = δ₀²·log(1+z)·H_φ(E/E₀)` (frozen model string,
`vp_neutrino_phason_decoherence_passport.py:61`, `icecube_phason_decoherence_protocol.json`). Its
**energy content** lives in two factors: `log(1+z)` and `H_φ(E/E₀)`. Read on disk
(`vp_neutrino_phason_decoherence_passport.py:126-130,188`):

```python
def hurwitz_gap_density(x):            # this IS H_phi
    alpha = 1.0/(phi*phi)              # φ⁻²  — OWNED number
    nearest = abs(x*alpha - round(x*alpha))
    return 1.0/(1.0 + 100.0*nearest)   # ← "100" width: BARE, UNOWNED
...
z_proxy = max(energy/1.0e6, 0.0)       # ← "1e6" redshift scale: BARE, UNOWNED
gamma = delta0**2 * log1p(z_proxy) * hurwitz_gap_density(max(energy, 1.0))
```

Three strict findings, each verified:

1. **There is NO owned `E₀`.** The model *string* says `H_φ(E/E₀)`, but the code feeds **bare
   `energy`** into `x·φ⁻²` — `E₀` is absent (grep of `08.42` and the passport: no `E₀`, no `E*`, no
   knee; §1 of the companion `ICECUBE_DECOHERENCE_FORM_MEMO` §6-G1 concurs "the values of ζ, E*, L0…
   NOT owned"). The φ⁻² *inside* `H_φ` is owned, but **an owned dimensionless number times an
   UNOWNED-scale energy does not own the energy axis.** What integer `E·φ⁻²` "lands near" depends
   entirely on the (unowned) physical units of `E`. This is the anti-numerology trap made concrete:
   the φ-flavor is real, the **energy scale it multiplies is external**.
2. **The redshift/`z` scale is bare.** `z_proxy = energy/1e6` — the `1e6` is a raw proxy
   (`ICECUBE_DECOHERENCE_FORM_MEMO §0` flags `z` as a REDSHIFT proxy, `08.42:16` fixes only the
   *domain* `0<z<1`, no value). `log(1+z)`'s energy dependence is entirely this unowned scale.
3. **The owned rate is ENERGY-FLAT (the decisive structural fact).** `φ⁻¹`, `τ₀`, `Λ_act` carry **no
   neutrino-energy argument.** `Γ₀ = φ⁻¹/τ₀` is a single constant (script GATE 3: `Γ₀(E)` identical
   across `E ∈ {1, 10³, 10⁶, 10⁹} MeV`). The IceCube kernel is **non-constant in E** (script GATE 4:
   `Γ(E)` varies across the same grid). **A constant cannot be an E-dependent kernel.** So the owned
   material supplies the *prefactor scale* (rate `Γ₀`, coefficient `δ₀`) but **not the E-profile.**

**The mechanism bar fails for the E-dependence.** For the E-dependence to be OWNED, some owned law
would have to make the **archive-tracing tick COUNT depend on the neutrino energy E** (e.g. "a
neutrino of energy `E` traverses `N(E)` archive circulations before observable return, `N(E) =
f(E, owned scene)`"). Grep of BOOK_06 (tick/Neumann owners) and BOOK_08 §08.42 finds **no such law**:
the scene `K(9,11,13)` is fixed, the tick `τ₀` is a fixed clock unit (`07.4:6` "τ₀=1"), the per-tick
rate is fixed. Nothing internal tells you how many ticks an energy-`E` neutrino decoheres over. That
map — physical `E` → internal tick-count / archive depth — **is exactly the unowned `κV(E)` bridge**
named in both parent memos (`ICECUBE_DECOHERENCE_FORM_MEMO §6-G1` "the composite bridge `κV(E)`… NOT
owned"; `M1QM_DEPARTURE_SCALE_MEMO §4/F-DIMENSION`).

## 3. Verdict — EXTERNAL on the E-dependence (rate + clock owned; E-map is the one residual)

**OUTCOME = external.** Precisely:

- **OWNED (rate + clock):** the physical decoherence **rate** `Γ₀ = φ⁻¹/τ₀ ≈ 2.90×10²¹ s⁻¹
  (≈ 12.0 MeV as an energy)` — both factors owned by mechanism (golden split `:308`; electron
  full-cycle `38` `:12`). This *upgrades* the parent memo: the rate is no longer just a per-tick
  ratio, it is a real SI number with an owned clock.
- **EXTERNAL (E-dependence — the single named input):** the map from that constant rate to the
  **E-dependent kernel** `Γ(E,z)`. Concretely three unowned scale-objects: (i) the energy axis `E₀`
  (absent; `H_φ` gets bare energy), (ii) the redshift scale in `log(1+z)` (`z=E/1e6`, bare), (iii)
  the `H_φ` width (`100`, bare). **None is owned by a mechanism that lets neutrino energy enter the
  archive-tracing tick count.**

**No leap, both directions.** (a) I do **not** under-claim: the rate *and its SI clock* are owned, so
`Γ₀` is a real owned number — stating "only a ratio is owned" would repeat the parent's understatement.
(b) I do **not** over-claim: `12 MeV` being a clean owned number is **not** an IceCube prediction —
it is energy-flat and `~10⁶` below the HESE window, so it *cannot* be the kernel. The inferential step
"the E-dependence is external" is **owned by the disk facts** (no owned `E₀`; owned rate provably
constant-in-E; no owned law feeding E into tick-count) — it is not a D0-internal reading, it is what
the code and books literally contain.

## 4. Can-fail check (`m1qm_rate_energy_check.py`, 6 gates, all PASS)

Each gate CAN fail if the verdict is wrong (not a tautology gate):

- **GATE 1 `OWNED_TICK_38_IS_INTEGER_PINNED`** — `2(2γ−1)=38 ⇔ γ=10` unique integer ⇒ `τ₀` clock is
  mechanism-pinned, not fit. *Fails if `38` needed a non-integer γ.*
- **GATE 2 `OWNED_PHYSICAL_RATE_IS_REAL`** — `hΓ₀ = φ⁻¹·Λ_act = 12.00 MeV`, non-Planck, non-vacuous.
  *Fails if the owned rate were vacuous/Planck-scale.*
- **GATE 3 `OWNED_RATE_IS_ENERGY_INDEPENDENT`** (load-bearing) — `Γ₀(E)` constant across the HESE
  decades. *Fails if an owned E-slot existed.*
- **GATE 4 `ICECUBE_KERNEL_IS_ENERGY_DEPENDENT`** — reproduces the passport kernel; it varies with E.
  *Fails if the kernel were E-flat (then the constant `Γ₀` could be it).*
- **GATE 5 `E_AXIS_IS_EXTERNAL_SCALE_ARBITRARY`** — rescaling `E` by an arbitrary `1.7` changes
  `Γ(E)` ⇒ the absolute E-scale is unowned. *Fails if an owned `E₀` fixed the scale.*
- **GATE 6 `CTRL_IF_OWNED_E0_THEN_KNEE_OWNED`** (counterfactual) — marks the SINGLE edit that flips
  the verdict: own a law `E₀ = f(owned scene)` tying neutrino `E` to tick-count. *No such `f` on disk.*

**How the whole verdict could be overturned (the honest reopening hook):** produce an **owned law**
`N(E) = f(E, K(9,11,13))` — the number of archive-tracing circulations a neutrino of energy `E`
undergoes — from owned material (e.g. baseline/energy entering the Neumann index `k` of
`D0-ARCHIVE-NEUMANN-TICK-OWNER-001` by an owned rule). That would convert the owned constant `Γ₀`
into an owned `Γ(E)` and flip the knee **energy** from external to owned. Until such `f` exists, the
E-dependence is the single external input.

## 5. Registry implication (proposal only — NOT applied)

- **Proposed note** on `D0-ICECUBE-001` (row 119, EMPIRICAL-PASSPORT) / `D0-PASSPORT-ICECUBE-HESE-001`
  (row 202, OPEN): the IceCube departure has an **owned physical rate** `Γ₀ = φ⁻¹/τ₀ ≈ 12 MeV`
  (owned golden split `06.6.A:296` ÷ owned tick `03.6:14`/`03.19:12`); what remains **external** is
  only the **E-dependence** of the kernel (the `E₀`/knee, the `log(1+z)` scale, the `H_φ` width — no
  owned law feeds neutrino energy into the archive tick-count). Upgrades "silent on magnitude" →
  "**rate-and-clock owned (≈12 MeV, energy-flat); E-dependence external**."
- **No edit** to `CLAIM_TO_LEAN_MAP.csv` / `LEAN_ASSUMPTION_LEDGER` / any `.lean` / any `053040` row.

## 6. Citation integrity (verified on disk 2026-07-05)

- `06.6.A:296` **[THE 6.1.2]** golden split `W_ext=φ⁻¹, W_int=φ⁻²`, proof `:308` — VERBATIM, per-book
  `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` (single concatenated file exists; line 296).
- `τ₀=h/(38 m_e c²)`, `Λ_act=38 m_e c²` — VERBATIM in per-section files
  `0007__03.6…:14,18` and `0021__03.19…:12,14,30,34`; also `BOOK_07/0005__07.4…:77,87`. (The
  parent memo's `BOOK_03:296/:300` concatenated-line anchor is content-verified here at the
  per-section `03.6:14`.)
- `06.40 tau0 = phi^-16` — VERBATIM `BOOK_06…:73`, FORCED `:952`; flagged DIMENSIONLESS and
  explicitly "must not be conflated" with the SI `τ₀` (`:77`) — so it is **not** the clock used for
  `Γ₀` (using it would be a category error: it is a phase↔time map, not a second-valued duration).
- passport kernel code `:61,126-130,176-177,188` — VERBATIM read; `δ₀=1/(2φ³)` owned, `H_φ` uses
  owned `φ⁻²` but bare `100`; `z=E/1e6` bare; no `E₀`.
- No `053040` row touched; no cert minted; script is a check, not a cert.
