# DRAFT — CAR16/Fock and chronological feedback on the dressed metric

18 October 2026. Candidate. Not a derivation of GR. \(T_{\mu\nu}\) is not defined. `claims.csv` is not extended. `D0-HODGE-LINKS-001` is not closed. PR #334 is not edited.

Read-only pin `origin/exp/a4d-joint-response-continuation-2026-10-16`, tip `f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6`, which is strictly after floor `c3ae03b735dbde690bf1774fc3761846aff93248`. The brief string `c3ae03b7b735dbde690bf1774fc3761846aff93248` is not an object.

## Verdict

```text
stress_on_dressed_metric = false
scoped_nogo = true
stress_defined_as_einstein = false
gr_derived = false
grade0_only = true
```

Exactly one of `stress_on_dressed_metric` and `scoped_nogo` is true. Spin is absent from the owned source, so the success of this note is a scoped no-go. The already-owned grade0 channel is cited and is not promoted.

## Consumed inputs, not re-derived

- `A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md` (1), (9), (10), (10d–e). The two-site Fraction witness is `check_dressed_car_metric.py`, blob `e6f391e6497e3f1d8298cb5b9c7309ae532737f3`. Its scope stands: physical tape, cost and clock are not an admitted binding.
- `A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md`, blob `dcf5870fa23d5535bca077d5bcbe2e54404a7c2a`, (3), (18), (19). Grade0 null scalar on \(\widehat g\), proportional on that branch to \((d\psi)_\mu(d\psi)_\nu\). The memo leaves independent spin and quantum dynamics unproved and says the construction is not D0⇒GR. \(\Lambda\), the scene price and the 40-row table are not recomputed. The later LEFT-coded note is the same grade0 channel with a local address; it also inserts no independent stress tensor.
- `A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md`, blob `fda1294b8d9794a62b86faaa19e3cc1a459e031d`, (7)–(9b) and (11). The 16×16 pencil is not rebuilt.

## What was checked

Constant \(\chi\) on the owned two-site weights \(\bar\mu=1/4\), \(\mu\in\{1/9,1/16\}\), \(\chi\in\{9/16,4/9\}\) fixes

```text
ghat = (mu/mubar) g,    Xhat = sqrt(mubar/mu) X
```

and moves raw \(g(v_\chi)\). The CAR16 square of the dressed leg is the symbol of \(\widehat q=(\bar\mu/\mu)q\), not of raw \(q\). The compensator \(d\mu=2\sigma\mu\), \(dX=\sigma X\) kills \(d\widehat X\). The trace of the two-site density commutator jet is zero.

The cited grade0 scalar

```text
q = ghat^{mu nu} (D_mu psi)(D_nu psi) = Tr_16 Gamma(k)^2 / 16
```

has, on the null chart, one nonzero coframe row, \(-2s^2/h\). At \(s=1/3\), \(h=1/5\) the value is \(-10/9\). A spatial bivector is not an argument. This citation is `grade0_only`. It is not \(T_{\mu\nu}\).

The owned angle jet (9b) on the factor curve has metric partial \(-a p^2\neq 0\) and joint value \(0\). Mask 13 moves and is outside that linear form. The contraction \(e=B^T n\) at \(n=e_0\), \(G=I\), sees \(B_{01}\) and misses \(B_{12}\). The nonzero \(\partial_{E_2}c\) is one scalar, not a symmetric tensor on \(\widehat g\).

The chronological frame law and the density dressing are different representations. At \(\chi=4\), grade \(g\) scales by \(\chi^{1-g/2}\) in the frame law and by \(\sqrt\chi\) in the dressing. Grades 0, 2 and 3 disagree. The zero factor jet does not transfer onto \(\widehat g\).

A rational spacetime-dependent profile of the same representative type as dressed-memo §4, not the profile \(\chi=e^{2ku}\),

```text
chi=(1+x/2)^2,  g_raw=chi^{-1} eta,  ghat=eta,
```

has \(g_{\mathrm{raw}}(0)=\widehat g\) but

```text
G(g_raw)(0) = diag(-3/4, 3/4, 3/4, 3/4),    G(ghat)=0.
```

That residual is not a source on \(\widehat g\).

## Pre-registered attacks

The checker raises `StressRefusal` on each operational attack below. The note does not answer them by widening the claim.

1. Promote the cited grade0 covector to a spin-including stress and set `stress_on_dressed_metric`. The spatial bivector misses both \(q\) and \(E_2\). Inserting mask 13 into (9b) spoils the zero joint jet. The flag stays false.
2. Freeze matter and store the partial \(-a p^2\) as a stress. The owned joint jet is zero. `metric_only_chronology` raises.
3. Copy \(G_{\mu\nu}\) into \(T_{\mu\nu}\), including the zero tensor of \(\widehat g\), the raw tensor, and a nonzero multiple. The checker raises `stress_defined_as_einstein`.
4. Infer equal sources from \(g_{\mathrm{raw}}(0)=\widehat g\). The Einstein tensors differ at that point.
5. Add \(\int\sqrt{|g|}(\partial\psi)^2\), or choose a measure that pushes the raw defect onto \(\widehat g\). Both raise. The factor \(\bar\mu/\mu\) is the already fixed dressing, not a measure selected here.
6. Identify the chronological frame law with the density unitary. At \(\chi=4\) the grade weights differ, so the cancellation does not land on \(\widehat g\).
7. Read the two-site Fraction witness as admission of tape, cost or clock. The dressed-checker scope still refuses that binding.
8. Recompute \(\Lambda\) or the 40-row stationarity, or call the finite certificate a derivation of GR. Neither is done. `gr_derived` is false.

Independent pass through these attacks: SURVIVES. The rational profile is not identified with \(\chi=e^{2ku}\).

## Boundary

No owned CAR16 correlator beyond the cited grade0 square, and no derivative of the chronological pencil \(J(c)\), supplies a symmetric tensor on \(\widehat g\). The scoped no-go is that absence. It is not a claim that no later admitted price could couple spin to \(\widehat g\), and it is not D0⇒GR.
