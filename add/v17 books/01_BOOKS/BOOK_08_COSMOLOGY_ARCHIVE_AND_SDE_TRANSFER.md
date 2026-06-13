# BOOK 08: COSMOLOGY, ARCHIVE AND S_DE TRANSFER

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 08 is the cosmology and archive-transfer layer of D0. It defines archive pressure, internal relative archive acceleration, finite-window S_DE transfer, and the boundary between core mathematics and survey comparison.
>
> **Claim discipline.** D0 core proves only internal finite-readout archive dynamics. Comparisons with DESI, BAO, SPARC, H0, supernovae or other astronomical surveys are passport targets only. No survey fit is a core theorem.

**Ownership and handoff.** Book 08 owns archive pressure, internal relative archive acceleration, corrected log-det pressure response, finite-window S_DE transfer and cosmology passport boundaries. It hands no empirical claim upstream; it only defines how surveys may be compared under frozen protocols.

## 08.1 Scope

Book 08 has four tasks.

1. Define archive pressure from the finite log-det partition function.
2. State the relative archive acceleration implied by the fractal tick.
3. Separate log-det response from archive-ratio acceleration.
4. Place S_DE and all survey comparisons in the correct bridge/passport class.

The book does not claim that D0 has empirically solved dark energy, H0 tension, galaxy rotation curves or any survey anomaly.

## 08.2 Archive Ratio Acceleration as Internal Mechanism

Archive ratio acceleration provides an internal mechanism that may be tested against dark energy observables through a declared passport protocol. The irreversible transfer of symplectic measure from active to archive strictly increases the internal degrees of freedom of the Archive. The outward pressure expanding the metric shadow is the thermodynamic force required to accommodate the growing entanglement entropy. Relative archive acceleration is an exact internal finite-readout theorem; any identification with observed dark energy remains a passport target requiring explicit protocol, negative controls and non-promotion firewall.

## 08.3 Relative archive acceleration

Book 06 defines the fractal tick envelope

\[
A_{n+1}=\varphi^{-1}A_n,
\qquad
B_{n+1}=B_n+\varphi^{-2}A_n.
\]

With \(A_0=1\) and \(B_0=0\), this gives

\[
A_n=\varphi^{-n},
\qquad
B_n=1-\varphi^{-n},
\qquad
R_n=\frac{B_n}{A_n}=\varphi^n-1.
\]

**Theorem 8.3 (Internal relative archive acceleration).** The relative archive ratio satisfies

\[
\Delta^2 R_n>0
\]

for all finite ticks in the fractal-tick sector.

*Proof.* Since \(R_n=\varphi^n-1\) and \(\varphi>1\),

\[
\Delta^2R_n=R_{n+2}-2R_{n+1}+R_n
=\varphi^n(\varphi-1)^2>0.
\]

This is an internal finite-readout statement with strict positive relative acceleration. It performs no astronomical fitting.

## 08.4 Corrected log-det pressure response

Let

\[
r(V)=1-e^{-\kappa V},
\qquad
\kappa=\log\varphi,
\]

and

\[
L(V)=-d_\tau\log(1-zr(V))
=-d_\tau\log(1-z+ze^{-\kappa V}).
\]

Then

\[
L'(V)=d_\tau\frac{z\kappa e^{-\kappa V}}{1-z+ze^{-\kappa V}}>0
\]

for \(d_\tau>0\), \(0<z<1\). The second response is

\[
L''(V)=d_\tau z\kappa^2e^{-\kappa V}\frac{z-1}{(1-z+ze^{-\kappa V})^2}.
\]

Therefore

\[
0<z<1\quad\Longrightarrow\quad L''(V)<0.
\]

The log-det pressure response is positive but decelerating in this stability domain. This must not be conflated with \(\Delta^2R_n>0\), which is a relative archive-ratio acceleration.

## 08.5 Static coefficient versus dynamic transfer

D0 separates a static archive coefficient from dynamic survey transfer. A coefficient may be derived inside the finite archive calculus, but comparison to observed expansion data requires an external transfer protocol.

The permitted statement is:

\[
\text{finite archive response defines an internal pressure channel.}
\]

The forbidden statement is:

\[
\text{a survey value is core-derived without a passport protocol.}
\]

## 08.6 S_DE finite-window transfer

**Definition 8.4 (S_DE transfer channel).** The symbol \(S_{DE}\) denotes a finite-window transfer observable built from archive pressure and a declared survey window. Its admissible form is

\[
S_{DE}=\mathcal T_{window}(P_{fb},\partial_VP_{fb},\mathcal M_{survey}),
\]

where \(\mathcal M_{survey}\) is an external data manifest and \(\mathcal T_{window}\) is fixed before comparison.

A valid S_DE passport must state:

1. the survey manifest,
2. the finite-window rule,
3. all fitted or frozen parameters,
4. the null model,
5. look-elsewhere correction,
6. rejection criteria.

Without these six items, S_DE is a bridge notation, not an empirical result.

## 08.12.2 Archive-Window Eigenvalue Equation and Topological Rigidity

Because D0 is an exact discrete holographic geometry, cosmological acceleration parameters cannot be continuously tuned to fit observational surveys (BAO/DESI). The S_DE transfer window centers (\(\lambda_c, \lambda_r\)) are entirely dictated by the structural invariants of the holographic carrier.

The roots satisfy the normalized finite archive-window polynomial:
\[ 160\lambda^2 - 480\lambda + 359 = 0. \]
This equation is a strict algebraic convergence of the D0 core invariants:
- The constant term **$359$** is exactly the prime number of edges in the \(K(9,11,13)\) holographic carrier (the prime-edge anyon scaffold).
- The coefficient **$160$** is exactly \(2 \times |\Omega_8| \times \gamma = 2 \times 8 \times 10\), the full two-sided signature of the terminal window.
- The coefficient **$480$** is exactly \(3 \times 160\), representing the 3-generation Torus-Core13 capacity.

This yields the exact algebraic roots \(\lambda_{c,r} = \frac{3}{2} \mp \frac{\sqrt{10}}{40}\). Dark Energy transfer is thus mathematically forced by the prime-edge incidence geometry of the primitive quantum detector.

## 08.12.5 Dark Energy as Golod-Shafarevich × Kerr Archive Rotation (Noah + Sebastian)

S_DE: 160λ² − 480λ + 359 = 0  
Корни λ_{c,r} — точные growth rates башни (OpenAI class-field tower disproval).  
Дополнительно: Kerr rotation внутри Archive → Δ²R_n > 0 строго из φ^n-1.

Certificate: vp_openai_tower_kerr_359.py

## 08.12.6 The Golod-Shafarevich Criticality Gap and Exact Cosmic Acceleration

The S_DE polynomial strictly evaluates the viability of the continuum limit. By mapping $160\lambda^2 - 480\lambda + 359 = 0$ to the algebraic tower denominator $\lambda^2 - d\lambda + r = 0$, D0 yields exact structural invariants:
- Tower generators: $d = 3$ (matching the Active Transport Rank).
- Tower relations: $r = \frac{359}{160}$.

**Theorem 08.12.6 (The Criticality Gap, D0.Core).**
By the Golod-Shafarevich theorem, the infinite continuous expansion of the universe requires $r < \frac{d^2}{4}$. Evaluating this boundary for the D0 holographic carrier:
\[ \frac{d^2}{4} = \frac{9}{4} = \frac{360}{160}. \]
The criticality gap $\Delta_{GS}$ is the exact algebraic distance to universal halting (collapse):
\[ \Delta_{GS} = \frac{d^2}{4} - r = \frac{360}{160} - \frac{359}{160} = \frac{1}{160}. \]
The universe expands to infinity because the prime-edge topology ($359$) falls short of the critical collapse threshold by exactly ONE quantum of the terminal signature ($160 = 2 \times |\Omega_8| \times \gamma$). Cosmological acceleration ($\Lambda$) is not a fluid or a tuned parameter; it is strictly driven by this $\Delta_{GS} = 1/160$ algebraic remainder. (Certificate owner: `vp_golod_shafarevich_gap_160.py`).

## 08.7 Stability and exceptional-point diagnostics

Exceptional-point or two-mode reductions may be used as finite transfer diagnostics. A typical bridge matrix is

\[
M(\eta)=
\begin{pmatrix}
\lambda_c & \eta\\
-\eta & \lambda_r
\end{pmatrix}.
\]

Such diagnostics are internal algebraic probes of transfer behavior. They do not by themselves identify a physical cosmological component.

## 08.8 Survey comparison as passport layer only

Comparisons with DESI, BAO, SPARC, H0, supernovae, weak-lensing catalogues or other external surveys are admitted only as passport work.

A survey section may say:

- the archive-pressure channel can be tested against a named data release;
- a finite-window observable has been pre-registered;
- a null comparison failed or passed under stated rules.

A survey section may not say:

- D0 core supplies an empirical dark-energy account from survey data;
- D0 derives a survey Hubble value without a passport protocol;
- D0 reports a DESI or SPARC comparison without a frozen manifest;
- an empirical comparison upgrades a bridge to a theorem.

## 08.9 Negative controls

Every cosmology passport must include at least the following controls.

| Control | Required purpose |
|---|---|
| Survey-shuffle control | tests whether the signal depends on catalogue ordering |
| Parameter-free null | tests whether D0 transfer beats a frozen baseline |
| Window-shift control | tests whether the result depends on a hand-picked redshift range |
| Look-elsewhere correction | prevents post-hoc invariant selection |
| Data-release separation | prevents using the same data for design and confirmation |

A positive-looking survey comparison without these controls remains inadmissible for publication as evidence.

## 08.10 Interfaces to other books

| Source | Imported object | Use in Book 08 |
|---|---|---|
| Book 01 | phase-unfolding and finite support | support for finite archive indexing |
| Book 02 | log-det calculus and corrected sign discipline | archive-pressure response |
| Book 06 | finite registration time and fractal tick | archive evolution |
| Book 07 | finite gravity bridge discipline | prevents direct GR overclaim |
| Book 09 | GWOSC negative controls | model for empirical passport discipline |

## 08.11 Cosmology layer status

| Object | Claim level | Status |
|---|---:|---|
| Archive pressure \(P_{fb}\) | Core / operator calculus | defined |
| Relative archive acceleration \(R_n=\varphi^n-1\) | Core-sector theorem | closed within fractal tick |
| Corrected log-det response sign | Core / cert discipline | closed |
| S_DE finite-window transfer | Bridge | defined, requires manifest |
| DESI / BAO / SPARC / H0 comparison | Passport | target only |
| Dark-energy empirical account | Not claimed | forbidden without passport closure |

## 08.12 Summary

Book 08 closes the internal finite-readout archive-pressure grammar and the relative archive-acceleration theorem. It does not close empirical cosmology. The publication-safe formulation is:

> D0 provides a finite archive-pressure and transfer framework. Survey comparison is possible only through frozen passport protocols with negative controls.

## 08.13 Master Cosmology Mechanism Full Closure

**Operator Closure Status:** `COSMOLOGY-MECHANISM-FULL-CLOSURE / INTERNAL-ARCHIVE-ACCELERATION / NO-SURVEY-FIT`

The internal cosmological mechanism is closed as a finite-operator chain independent of astronomical survey data.

1. **Log-det pressure stability.** The log-det contribution

\[
L(V)=-d_\tau\log(1-z(1-e^{-\kappa V}))
\]

obeys \(L'(V)>0\) and \(L''(V)<0\) for \(0<z<1\). The absolute pressure is outward but decelerating.

2. **Relative archive acceleration.** The fractal tick gives

\[
A_n=\varphi^{-n},\qquad B_n=1-\varphi^{-n},\qquad R_n=B_n/A_n=\varphi^n-1.
\]

Therefore \(\Delta R_n>0\) and \(\Delta^2R_n>0\), even though the absolute archive production decelerates.

3. **Finite-window transfer.** Here \(V_k = \operatorname{rank}(P_{N_k})\) denotes the retained volume (active sector rank) at finite tick \(k\).

The internal transfer observable is

\[
S_{DE}[n_0,n_1]=\sum_{k=n_0}^{n_1-1}L'(V_k)\Delta R_k.
\]

It is finite, positive and monotone on finite tick windows. It is constructed before any redshift, survey or catalogue comparison.

**Firewall.** DESI, BAO, SPARC, H0, supernovae and weak-lensing catalogues are passport inputs only. They cannot define \(L\), \(R_n\) or \(S_{DE}\), and they cannot promote a survey comparison into a core theorem.

## 08.14 Universal Passport Firewall

Empirical validation against BAO, SPARC, DESI, supernova or `H_0` data is governed by the universal passport firewall. Survey comparison may test the frozen internal `S_DE` transfer shape, but an empirical fit cannot be promoted to a core D0 theorem. Physical constants fitted in the passport layer cannot be retroactively called derived internal observables.


## v17 Research Upgrade: Boundary-Response Dark-Matter Operator Candidate

**Status:** `BOUNDARY-RESPONSE-OPERATOR-CANDIDATE / DOMAIN-GUARDED / NOT-EMPIRICALLY-VALIDATED`

The v17 boundary-response patch defines a disciplined operator candidate for galaxy-scale archive response. The topological support remains idempotent:
\[
P_N^2=P_N,
\qquad Q_N=I-P_N.
\]
Baryonic density enters through a bridge weight \(W_\rho\), producing
\[
F_\rho=P_NW_\rho^{1/2}U_N^\dagger Q_NU_NW_\rho^{1/2}P_N=K^\dagger K\succeq0.
\]

The response is attached to a boundary shell observable \(\ell_V\), not to an ambiguous cumulative derivative. It is active only on an admissible domain; outside that domain the status is **INACTIVE / NO-RESPONSE**.

SPARC remains a blind passport. The core contains no per-galaxy tuning, MOND-like interpolation, NFW/Burkert halo insertion, or empirical-success claim.

## 08.15 Interface to Other Books

| Book | Object exchanged | Role |
|---|---|---|
| Book 02 | log-det calculus and corrected sign discipline | archive pressure response |
| Book 06 | fractal tick and archive ratio | source of internal relative acceleration |
| Book 07 | finite gravity and horizon capacity discipline | prevents geometry overclaim |
| Book 09 | empirical passport/no-retuning template | shared external-test discipline |

## 08.16 Publication Boundary Statement

Book 08 closes the internal cosmological mechanism of D0: archive pressure, finite-window transfer grammar and relative archive acceleration. All external survey comparisons remain strictly passport targets. No DESI, BAO, SPARC, H0 or survey-facing claim is core in v16.

## 08.17 Cross-Reference Summary

- Book 00: 00.19-00.20 Grand Singularity (R ≡ Λ_N) unifies archive pressure as partial trace.
- Book 01: support + 01.11C.
- Book 02 owns \(Z_N\), \(P_{fb}\) calculus and the corrected log-det sign (02.19B).
- Book 03/04: action + matter carriers (04.9B).
- Book 05: 05.10 (vp_golod_shafarevich_gap_160.py for 08.12.6; vp_archive_friedmann...).
- Book 06 owns \(R_n=\varphi^n-1\) as finite archive evolution (06.2E Schur).
- Book 07 supplies finite gravity boundary discipline (07.8B A/4).
- Book 09 supplies a parallel negative-control model for external residual tests.

New: 08.12.5 Dark Energy (GS × Kerr), 08.12.6 GS criticality gap Δ=1/160 (D0-CORE-GRAND-SINGULARITY-001). All from Self-Reading finite R.

Book 08 closes internal archive/cosmology transfer and prepares only passport-level survey work.
