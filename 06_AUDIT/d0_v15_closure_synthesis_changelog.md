# D0 v15 closure synthesis changelog

## 1. What was closed

The v15 synthesis closes the finite feedback operator core as `D0-CVFT-001A`:

```text
F_N = P_N U_N^dagger Q_N U_N P_N
G_N(z) = (I - z F_N)^(-1)
S_fb = -log det(I - z F_N)
mathsf P_fb = beta^(-1) partial_V log Z_N
```

The closed object is finite: retained/traced projections, finite tick, positive feedback-return operator, resolvent, determinant trace expansion, finite variation and pressure law.

## 2. What became sector theorem

Matter, time, gravity and cosmology are now written as sector laws:

- matter: terminally projected near-critical feedback modes;
- time: normalized/coarse-grained entropy channel with `c_D0 = 1 tick gauge`;
- gravity: heat trace, feedback pressure, boundary capacity and UV finite-tail regime;
- cosmology: `S_DE` as two-mode feedback-pressure transfer with boundary derivative feedback.

## 3. What became operator scaffold

The baryon S3 construction is explicitly classified as an operator scaffold:

```text
V_B = V_shell^(tensor 3), dim V_B = 27
Pi_S3 = 1/6 sum_{sigma in S3} P_sigma
dim Pi_S3 V_B = 10
```

`CVFT-F3 = OPERATOR-SCAFFOLD-CERTIFIED` closes the internal finite carrier/symmetrizer construction. It does not close physical spin, flavour, masses, widths or PDG assignment.

## 4. What remains empirical passport

External comparison remains in empirical passport rows: IceCube, SPARC, DESI, CMB, CKM and PDG-facing meson/baryon comparisons. Each passport must freeze data manifest, finite operator, response map, negative controls and pass/fail boundary.

The IceCube sync passport token is:

```text
vp_neutrino_phason_decoherence_passport.py
```

## 5. What no-go statements became constructive operator targets

No-go language was converted into constructive target language where possible:

- DESI/SPARC failure points to boundary-derivative feedback, not arbitrary kernel refit.
- Baryon full-multiplet no-go points to frozen `U_eff^B` pole transfer with S3 scaffold.
- Meson direct-mass no-go points to positive defect/domain-wall transfer.
- Horizon/greybody no-go points to boundary leakage operator and passport target.
- Gauge/confinement language points to boundary leakage/commutator obstruction targets.

## 6. Remaining work before publication

- Freeze the sector projection package `D0-CVFT-001B` against rows `CVFT-F1` through `CVFT-F8`.
- Promote refined UV tail and boundary-rank cert candidates where theorem owners are ready.
- Build frozen `U_eff^B` from actual D0 tick and add spin/flavour transfer.
- Complete pole normalization for resonance programs.
- Keep survey and PDG comparisons in empirical passport form until external manifests and response maps are pinned.
- Run Lean only in the deferred verification phase; current v15 synthesis is non-Lean text/status integration.
