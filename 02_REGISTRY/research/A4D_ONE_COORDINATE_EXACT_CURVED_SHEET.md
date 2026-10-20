# Exact curved connection sheet and raw Einstein-response transfer

15 October 2026. Existing SOURCE #310, RESEARCH. Scientific input
`a9212b19bb5779a9dd2e0d94109af26677236399`.

[Analytic proof and scope](sources/d0_one_coordinate_exact_curved_sheet_2026-10-15/RESULT.md)
[Exact and interval replay](sources/d0_one_coordinate_exact_curved_sheet_2026-10-15/verify.py)
[Validation](sources/d0_one_coordinate_exact_curved_sheet_2026-10-15/VALIDATION.json)

The unchanged naked-star action has a unique small exact connection root for
all sufficiently small smooth periodic coframes depending on one coordinate,
on every sufficiently fine periodic mesh. The actual full 24-component symbol
on `(1,z,1,1)` is inverted without a frequency cutoff, with period-independent
unnormalized l1/l-infinity bound `35/6`. The full Laurent identities, not only
the determinant, are checked. A finite-stencil contraction then exactifies the
owned smooth Palatini germ uniformly. No unknown-solution derivative bound is
imposed on the small one-coordinate class.

Transverse translation symmetry proves that this root annihilates all
`24 L^4` actual local connection equations, not just selected ansatz rows.
The metric response difference to the Mth smooth comparator is bounded in the
original unweighted norm by `h^-2 ||Xi_exact-Xi_smooth||_raw,1 <= C_M h^(M-5)`.
Thus M=6 gives O(h), and the exact reconstructed response inherits the owned
nonlinear Einstein limit `-G/2` with its stated curvature sign.

Independently, at L=8 and `E=diag(1,1,f,f)`, `f=1+cos(2pi*x1)/100`, a genuine
192-variable outward-interval contraction proves an exact root in the box of
radius `2^-30`: contraction <3/40, center displacement <2^-40, image radius
<2^-33. An odd plaquette entry is strictly between 1/200 and 3/500. Hence the
root is nonflat and obeys all 98,304 full connection rows. The exact zero is
not inferred from floating-point residual size.

Scope: this closes an explicitly nonempty curved designated subclass of the
geometric naked-star sector. It does NOT prove the full D0 Cost-Info binding,
generic multi-coordinate/UV microstructure decoupling, prescribed-source joint
metric/matter solvability, physical coupling normalization, or full GR.
Original #310/#202/#317 remain open. No CORE/BOOK/claim changes or new task.

Local verification: 61 named exact algebraic checks, full 192x192 interval
Jacobian, optimized algebra replay, five executed mathematical mutants, and
separately labelled numerical diagnostics. No new Lean compilation or local
full-repository CI pass is claimed. Historical source receipts are untouched.

Run `python 02_REGISTRY/research/certificates/a4d_one_coordinate_exact_curved_sheet_check.py`.
