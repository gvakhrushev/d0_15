# q=(3,3,0,0): legacy-source mixed crossing and grade-four witness

This package checks one fixed local obstruction in the native second-order
matter operator under the legacy four-link-source interface. It does not
classify all momenta, prove a nonlinear branch, or close the gravity route.

## Certified statement

On the carrier L=8, with all 16 exterior/Fock components retained, the
13-dimensional complete native mean slice at q=(3,3,0,0) has a unique
Schur crossing for the affine pencil between the faithful and old pure-memory
endpoint Hessians in the fixed decimal congruence fixed_B.json. This is the
legacy four-source path; the crossing
lies in [0.43032, 0.430405]. A fixed 12 by 12 approximate inverse
fixed_schur_R.json proves uniform complement invertibility and a strictly
negative Schur derivative on that bracket.

At the actual crossing kernel, the full native second-order operator,
including every occupied and predecessor shell node and the mixed chart
second jet, has

    Re Tr(W M_v)/16 in [0.3110574666, 0.8594475318].

The witness is
W=(gamma_0 i*kappa_0)(gamma_1 i*kappa_1) in the owned ACDB exterior order.
An exact CAR calculation proves that W is Hermitian, squares to identity,
has trace zero, and pairs to zero with all 16 gamma_i*kappa_j source
generators. It also checks all four original link-source rows, their zero
trace, and the seed expectations. Consequently W is a two-sided tangent to
the full-rank density fibre of these four legacy source constraints
rho_t=(1-t)I/16+t|chi><chi| for 0<t<1, with a positive interval of
admissible perturbation size.

Thus this particular legacy-source crossing does not satisfy a stationarity
condition that requires the full second-order operator to pair to zero with
every source-neutral grade-four tangent. The result is local to the stated q,
carrier, fixed chart, and four-row source fibre.

## Full-Lorentz boundary

A separate full-Lorentz source owner now derives 12 independent boost Euler
rows. Its exact source result shows that the old pure seed used by this
interpolation fails those rows; the mixed path certified here is therefore
not a feasible faithful-to-old-pure path for the full-Lorentz matrix
interface. This certificate remains a valid local result for the old
four-source interface, but it is not a full-Lorentz stationary-root or GR
argument. The separate owner gives a different balanced rank-8 preparation;
this checker does not use or certify its Hessian. See the separate owner
02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md (SHA256
0ca27a97b7e8fa5653242415c4bcbe0e946fccd95bb277024fcbe79222c927a8) and its
validation result 8920803d185af11132dfa274a42d0e307ad43db150ef8e87d7ab83c9bf2f4d0d.

## Replay

From the repository root, run:

~~~sh
python3 02_REGISTRY/research/sources/d0_q3300_mixed_crossing_witness_2026-10-16/check_q3300_mixed_crossing.py
python3 -O 02_REGISTRY/research/sources/d0_q3300_mixed_crossing_witness_2026-10-16/check_q3300_mixed_crossing.py
~~~

Both invocations must emit byte-identical JSON with status PASS_LOCAL_Q3300.
The checker pins the interval owner and both fixed inputs. The interval owner
verifies its transitive source hashes during preparation. The check does not
call an eigensolver or search for a root; it encloses the preselected crossing
and its kernel over a fixed decimal bracket.

## Scope boundary

This does not prove a convergent nonlinear solution, source admission or
recovery, an all-q result, a physical history cost, a refinement law, Einstein
dynamics, or full D0 closure. It identifies a specific local obstruction to
the legacy-interface grade-four source-neutral stationarity test. Any broader
conclusion requires a separate argument connecting this tested fibre and
operator to the parent physical variational problem and the expanded
full-Lorentz source rows.
