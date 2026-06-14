<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_09_GRAVITATIONAL_WAVES_AND_QUANTUM_INTERFEROMETRY/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK_09_GRAVITATIONAL_WAVES_AND_QUANTUM_INTERFEROMETRY

> Publication status: v16 publication addendum / GW and interferometry bridge.  This book is a guarded discovery-theory layer.  It does not claim LIGO confirmation of D0.

## 09.00 Scope and claim discipline

Book 09 collects the gravitational-wave and interferometric material that should not be hidden inside Book 07.  The core gravity operators remain in Book 07.  This book states the bridge grammar, passport targets, negative controls, and future residual-observable programme for gravitational-wave data.

Allowed verbs: `defines`, `models`, `predicts as a target`, `tests`, `rejects as current evidence`.

Forbidden verbs: `confirms`, `proves from LIGO`, `fits after tuning`, `establishes astrophysical identity`.

The V3--V12 GWOSC/LIGO scans are admitted as negative-control discovery work.  Raw `phi` ladders, detector-frame `phi`, `mu/tau` ramified ratios, and fixed population `alpha` were not supported as evidence in the current proxy metrics.

## 09.01 Apple torus / spindle torus geometry

The binary horizon-interference picture is represented by a finite toroidal readout geometry: two axial release lobes and a transverse equatorial capacity belt.  The geometry is called the apple-torus or spindle-torus bridge because the retained/archive seam closes around an axial puncture while preserving a finite volume constraint.

The bridge object is not an embedding claim about the literal astrophysical horizon.  It is a finite readout carrier used to organize axial release, transverse saturation, and quadrupole strain.

## 09.02 Volume-preserving quadrupole and spin-2 carrier

Let `Pi_axis` and `Pi_transverse` be frozen axial and transverse readout projectors on the GW bridge carrier.  The trace-balanced quadrupole operator is

\[
Q_2 = 2\Pi_{axis}-\Pi_{transverse},
\]

with the bridge normalization

\[
\operatorname{Tr}(2\Pi_{axis}-\Pi_{transverse})=0.
\]

This is the finite readout expression of volume-preserving quadrupole deformation: axial extension and transverse compression balance at trace level.  The spin-2 interpretation is a bridge target: the TT gravitational-wave carrier in Book 07 is the core finite spin-2 operator, while `Q_2` is the macroscopic interferometric picture.

## 09.03 Horizon hum theorem-target

A single saturated horizon seam need not be perfectly static in the finite theory.  Its retained/archive boundary can support small capacity-preserving micro-vibrations.  In bridge language this is the `horizon hum`: a low-amplitude quadrupole residual of an isolated seam.

Status: `THEOREM-TARGET / PASSPORT-TARGET`.

No LIGO or telescope evidence is claimed here.  The target observable is a residual line or envelope after known ringdown, detector response, and environmental lines have been removed.

**The information rate carried by the hum: `I_f = h_{KS} = \log|\lambda_{\max}(T)| = \log\varphi` (formula fixed).** A proposed record `I_f = \mathrm{Tr}(\log T)/\mathrm{rank}` is *incorrect* and is corrected here: the toral generator `T=\begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}` has eigenvalues `\{\varphi^{-1},-\varphi\}` and `\det T = -1 < 0`, so `\mathrm{Tr}(\log T)=\log(\det T)=\log(-1)=i\pi` is **complex** — an entropy cannot be. The correct quantity is the Kolmogorov–Sinai entropy `h_{KS}=\log|\lambda_{\max}(T)|=\log\varphi\approx0.4812` (claim `D0-IF-KS-FORMULA-FIX-001`, cert `vp_if_kolmogorov_sinai.py`). The *number* `\log\varphi` was always right; only the *formula record* is fixed. It is the same `\log\varphi` reached by the Fibonacci route (BOOK_01 §01.21.4, `D0.Claims.FibonacciIfBridge`, which proves `|-\varphi|=\varphi`).

## 09.04 Binary merger as Born-rule beat bridge

If two finite horizon seams contribute amplitudes `A_1 e^{i\omega_1 t}` and `A_2 e^{i\omega_2 t}`, the macroscopic readout intensity contains the beat term

\[
|A_1e^{i\omega_1t}+A_2e^{i\omega_2t}|^2
= |A_1|^2+|A_2|^2+2\Re(A_1\bar A_2e^{i(\omega_1-\omega_2)t}).
\]

The D0 interpretation is that the observable merger strain is a finite interference readout, not a direct photograph of a continuum geometry.  The beat frequency is a bridge coordinate and must be compared only after external waveform, detector response, and noise models are frozen.

## 09.05 Dimensionless LIGO passport targets

The clean dimensionless passport targets are:

\[
I_A = \varphi^{-1},
\qquad
I_f = \log\varphi.
\]

`I_A` is an amplitude/retained-fraction target.  `I_f` is a logarithmic frequency-spacing target.  Neither target is currently confirmed by the V3--V12 scans.  They are retained only as pre-registered residual-observable targets for future non-saturating metrics.

## 09.06 Negative-control ledger: V3--V12

The discovery sequence produced useful falsification:

```text
V3: GW170814 candidate emerged in raw phi-coherent matching.
V4: raw q=phi frequency ladder failed ratio sweep.
V5: cascade model did not produce single-event significance.
V6: detector-frame phi beat failed against off-source background.
V7/V8: mu-plus phi^(5/4) was interesting but not significant; p≈0.53 in the amplified null.
V9: ramified ratios underperformed base phi in paired population proxy.
V10/V11/V12: fixed alpha was not population-stable and score saturation made best-alpha unreliable.
```

Conclusion:

```text
No LIGO confirmation claim is allowed in v16.
The valid result is a negative-control map and a transfer-corrected residual programme.
```

## 09.07 Residual programme after fixed-alpha failure

The next admissible GW observable is not a fixed ratio.  It must be a transfer-corrected residual:

\[
Z(event,\alpha)=\frac{S(event,\alpha)-\operatorname{median}_\alpha S(event,\alpha)}{\operatorname{MAD}_\alpha S(event,\alpha)}
\]

or a stricter waveform-residual observable after external GR template subtraction.  Publication language must say `target`, `protocol`, or `negative-control`, not `discovery` or `confirmation`.

## 09.08 Relation to Book 07

Book 07 owns the finite gravity operators: horizon capacity, seam emission, TT spin-2 sector, and jet/channel observables.  Book 09 owns the gravitational-wave and interferometric bridge material.  If a future residual observable survives negative controls, it may be promoted to an empirical passport, not to a core theorem.
## 09.09 Horizonless ringdown: a second falsifier

Beyond the `I_f = log φ` horizon-hum target of §09.05, the arrested-collapse picture of BOOK_07 §07.51 supplies an independent, sharper gravitational-wave falsifier. It is stated here strictly as a *prediction-as-target*, in the discipline of §09.00: it is not confirmed, not fitted, and never core.

If a compact remnant sits at the causal compactness ceiling `C = 3/8`, its surface lies at

```math
R = \frac{M}{C} = \frac{8M}{3} \approx 2.667\,M,
```

which is **inside** the photon sphere `r_{ph} = 3M` and **outside** the horizon `2M`. The light-ring potential barrier together with the reflecting surface form a cavity, so the post-merger signal is not a pure prompt ringdown: it carries a train of **gravitational-wave echoes**. A true black hole has no surface outside the horizon, hence no cavity and no echoes. Echo presence is therefore the discriminator — present implies a horizonless seam, absent is consistent with a horizon.

The characteristic echo delay is the light round-trip across the cavity in tortoise coordinate `r* = r + 2M·ln(r/2M − 1)`:

```math
\tau_{\mathrm{echo}} = 2\,\big[\,r^\*(3M) - r^\*(8M/3)\,\big] \approx 2.3\,M .
```

Two features make this falsifiable rather than decorative. First, `τ_echo` is **dimensionless** in units of the remnant mass `M`, so it scales with every event and is not a free fit. Second, it is a *short-delay* train — distinct from the long-delay echoes of objects pressed against the horizon (`R → 2M`, where `r*` diverges); the surface here sits well above `2M`, so the delay is of order a few `M`, a qualitatively different signature.

The echo mechanism for ultracompact horizonless objects is standard (Cardoso–Pani); the D0-specific content is only the surface placement at the causal ceiling `C = 3/8`. This target is frozen as an empirical passport — a clean rejection criterion for the horizon hypothesis — and is not asserted from any current LIGO–Virgo–KAGRA event. As with the `I_f` target, a negative scan does not falsify D0; a confirmed short-delay echo train at the predicted scale would promote the target, never the converse.
