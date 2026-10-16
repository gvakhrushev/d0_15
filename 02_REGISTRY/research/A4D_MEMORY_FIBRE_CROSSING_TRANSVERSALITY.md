# Rank-aware memory fibre blocks the pure q3300 second jet

Date: 2026-10-16. This is an additive continuation of [the memory-source and nonlinear-selection result](A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md), using its actual full action, source rows, rank-aware Hessian and second-order compatibility equation. The checker and interval output are in [`sources/d0_memory_fibre_crossing_2026-10-16/`](sources/d0_memory_fibre_crossing_2026-10-16/README.md).

## Result

Let \(H_t\) be the complete 13-coordinate reduced field Hessian for the existing price at the \(q=(3,3,0,0)\) mode, with the actual preparation moving on the already-owned stationary memory segment

\[
\sigma_t=(1-t)I_{16}/16+t\,|\chi\rangle\langle\chi|,
\qquad
\chi=(e_1-e_{15})/\sqrt2.
\]

Its dependence on \(t\) is affine: \(H_t=H_0+t\Delta\). The interval owner encloses the analytic pencil over the certified \((d,o)\) rectangle; it equals the native reduced Hessian at the owned stationary root, while other rectangle points are enclosure parameters rather than additional D0 roots. The endpoint inertia is outward-certified uniformly on that rectangle. The table is for the **complex 13-coordinate Fourier block**; the real field uses the associated \(q,-q\) pair:

| (t) | positive | negative | certified minimum absolute midpoint eigenvalue | interval congruence error |
|---:|---:|---:|---:|---:|
| 0.42 | 12 | 1 | 0.01311448 | < 0.00009317 |
| 0.44 | 11 | 2 | 0.01248829 | < 0.00009260 |

The decimal bases used for these comparisons are certified invertible, and each congruence residual is smaller than the smallest absolute diagonal eigenvalue. For every fixed \((d,o)\) pair in the rectangle, the analytic Hermitian pencil changes its negative index by one, so continuity gives a crossing at some \(t_*(d,o)\in(0.42,0.44)\); in particular this holds at the owned stationary root. A certified complementary block stays invertible throughout this interval, so each crossing kernel is one-dimensional over the complex Fourier amplitudes. Realification gives the corresponding two-dimensional \(q,-q\) mode pair before any orbit quotient; both real directions cross with the same sign. The strict slope bound below at every root, together with this endpoint index change, gives exactly one crossing parameter for each fixed \((d,o)\) pair.

The same interval bounds control every normalized kernel vector at any crossing in the interval. In the fixed 13-coordinate chart, its distance from a normalized reference vector is at most 0.100455805. The exact density-direction pairing at the reference vector lies in

\[
[-1.280329830,-1.280327071],
\]

and the certified operator norm of \(\Delta\) is at most 2.170773049. Therefore every unit crossing vector \(v\) obeys the strict bound

\[
\langle v,\Delta v\rangle < -0.8441.
\]

In the pinned complex-block normalization this is the memory-fibre contraction
\(\operatorname{Tr}((|\chi\rangle\langle\chi|-I_{16}/16)M_v)\), with (M_v) the full CAR second-response operator of the source-capacity owner; the associated real (q,-q) pairing is its owner-defined realification and has the same strict nonzero sign. The tangent \(|\chi\rangle\langle\chi|-I/16\) is an actual source-neutral stationary-fibre tangent: it has zero trace and zero pairing with all three owned sources. It is not an invented detector or fitted source. The owner’s reduced/full envelope identity lifts this variation to the genuine full-space kernel direction, including the field-dependent reconstruction; it does not freeze that reconstruction.

For the **pure \(q,-q\) field velocity** and its prescribed off-shell matter response, the second-order stationary-jet equation requires this contraction to vanish against every kernel direction. The strict negative bound contradicts that necessary condition. The first-order spectral-flow mode therefore has no second-order stationary extension with memory held fixed to first order. Every crossing in the stated interval is transverse in this memory direction; combined with the endpoint index change, this gives a unique crossing on this segment.

## Why this is a nonlinear test

A first-order zero mode alone does not establish a branch. The preparation segment supplies one explicit real tangent \(\delta\sigma\); its corresponding full-space Hessian-kernel vector is used only as a cokernel test against the pure \(q,-q\) field velocity, whose first-order memory component is zero. The calculation uses the actual derivative of the reduced Hessian along that preparation direction. No source equation is removed.

The 13-coordinate matrix represents the original q=(3,3,0,0) block by the owned spatial S3 and CAR-parity restoration [symmetry](sources/d0_native_joint_kernel_2026-10-16/PURE_MEMORY_SHELL_RESTRICTION.md): the permutation (1\leftrightarrow3) fixes the time coordinate, and the restoration sends \(\chi\) to itself up to a common sign, leaving its density projector and source-neutral tangent unchanged. The root parameters (d,o) range over the existing certified rectangle; (t_*) is not fitted to its floating midpoint.

## Scope

This closes one bounded child question: the velocity supported solely on the unique q3300 spectral-flow mode pair, with zero first-order memory velocity, fails the necessary second-order compatibility test on this specified mixed-memory segment. A branch whose first velocity also contains other field modes or moves within the memory fibre has additional bilinear terms and is not classified here. The result does not prove or exclude all curved native roots, all preparation ranks, or every nonlinear continuation. It does not select a physical preparation law, prove physical operation admission, establish soundness/recovery, or identify the result with Einstein dynamics. No action, source, selector, or physical postulate is added.

The validation reruns only this 13-coordinate interval consumer. It retains the full 4096-mode heat data, all 16 Fock components, and the existing reference carrier through the pinned owner; it neither reruns the prior full symbol suites nor uses their floating diagnostics as evidence.
