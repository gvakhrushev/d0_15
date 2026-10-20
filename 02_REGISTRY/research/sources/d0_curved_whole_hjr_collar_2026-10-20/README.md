# Exact curved whole-HJR interior roots: proof and reproduction

Consumer: existing Draft334 / native-programme-v1, positive curved joint
existence for the declared ORIGINAL full-Lorentz spatial H+J+R.
[Proof](../../A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md).

The analytic implicit-function theorem plus the rigorous interval derivative
certificate proves exact local finite fixed-collar roots. Ten scalar rows
imply all unrestricted interior coframe and incident-link rows by finite
symmetry averaging. The true observer equations follow by Ward, and the
full Riesz projector solves every fixedreference128 preparation row.
Actual based plaquettes are nonidentity for all sufficiently small nonzero
boundary parameters. No nonlinear epsilon radius is supplied.

Exact checks use Python3.12/SymPy1.14:

```bash
python check_exact_ward.py
python check_exact_collar_symmetry.py
python check_exact_seed_balance.py
```

The rigorous Hessian checker requires NumPy2.3.5 and python-flint0.9.0
(Arb128bit); run from anywhere inside the checkout:

```bash
python 02_REGISTRY/research/sources/d0_curved_whole_hjr_collar_2026-10-20/check_collar_hessian_arb.py
```

It reads only the owned v8 root center, uses its certified radius1e-12,
and recomputes the full finite-B/Riesz Hessian with exact integer
Q(sqrt2,i) feature traces and rigorous ball arithmetic. The root-moment
simplification is valid at the exact stationary root; its enclosing
formula is not asserted to equal off-root Hessians throughout the box.
All4096momenta are retained via960 exact S3 orbits. Every Neumann row is
bounded by the exact rational1/10^4; transverse responses6,7,8 exclude0.
The saved COLLAR_HESSIAN_ARB.json includes the rational preconditioner.

A separately built actual D on all512 transverse blocks of128components
checks the nonlinear source, moving Riesz preparation and exact fixed-Gram
purification. It requires NumPy/SciPy and uses the OLD exploratory K9 only
as a numerical iteration preconditioner, not as proof:

```bash
python 02_REGISTRY/research/sources/d0_curved_whole_hjr_collar_2026-10-20/check_nonlinear_full_source.py --output /tmp/collar-diagnostic.json
```

NONLINEAR_DIAGNOSTIC.json is floating evidence, clearly distinct from
COLLAR_HESSIAN_ARB.json and the analytic existence theorem.
VALIDATION.json pins all relevant inputs, code, proof and saved evidence.

The collar is all exterior coframes and exterior-to-exterior links;
BOTH time links incident to the interior slice vary. Exterior equations,
global periodic stationarity, original clock/current constraints, physical
native programme/action/preparation price, Levi-Civita/Einstein source
identification and uniform refinement/raw216 remain OPEN. GR_closed=false.


The stronger seven-slice bulk theorem is section10. Run
`python check_wide_collar_arb.py` inside this packet (same NumPy/python-flint
dependencies). It reads ONLY the saved final COLLAR_HESSIAN_ARB.json,
pins that receipt, constructs the64variable principal compression and
certifies every Neumann row<3/1000 and response error<1/100. It prints its result; `--output /tmp/wide-collar.json` saves an independent
receipt without changing the pinned evidence. No full spectral replay is needed. Seven eighths of
the sites are interior; one exterior slice remains. This is still finite
conditional existence, not uniform refinement or physicalGR closure.


Section11 is the analytic uniform first-order/Riesz preparation theorem.
`python check_uniform_riesz_linf_control.py` (SymPy1.14) verifies the exact
full16 hostile control: alternating coefficients keep Linf amplitude fixed
but produce a2epsilon/h response on a constant top form. This establishes
why discreteC1 is a real hypothesis. The analytic contour proof, not the
small-grid control, supplies uniform rank128/Gram, first-source and Hessian bounds.
No uniform whole-HJR root or raw216 claim follows.

Both Arb checkers leave saved evidence unchanged by default. Use explicit
`--output /tmp/name.json` to create a fresh receipt for comparison.


Section12 completes the uniform first-source/Hessian estimate for the
ENTIRE unchanged conditional finite-B H+J+R action on the same C1 chart.
Minmax spectral counting controls full traces; two-endpoint divided
differences and row/column operator-norm bounds retain noncommuting jets
without ambient-dimension loss. The true global normalizer and moving
preparation remain. The full-dimension FIELD-INDEPENDENT feedback offset
is kept explicitly; no bounded total price or physical GR is inferred.
T14 gives a uniform Lipschitz source comparison in the ACTUAL C1 dual norm.

`python check_whole_price_mixed_jets.py` needs only python-flint0.9.0. It
builds the actual four-role periodic L2 operator with ALL16 sites and
ALL16 CAR fibers (256 dimensions), true shifted adjoint and genuine
coframe/proper-boost jets. Exact rational differentiation of the literal
finite-B power and log determinant agrees with both independent full spectral
divided differences and DIRAC-functional polynomial Frechet calculus for
both first sources and all three mixed Hessians.
Deleting the global normalizer or the proper mixed second jet gives
nonzero exact defects. Its depth3/calibration is a SMALL IDENTITY CONTROL,
not a native-depth root or a numerical proof of uniform refinement.
`--output /tmp/whole-price.json` writes a fresh receipt; default is read-only.
The analytic section12 proves the full native m=256L^2 family.
