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
