# Validation receipt and trust boundary

The final check_scene_heat.py was run normally and with python -O; both completed
and their JSON outputs were byte-identical. All 105 guards use explicit
exceptions, not removable assert statements. The two input files are verified
against their original Git blob hashes at runtime.

The interval coefficient calculation ran with90-decimal-digit mpmath.iv arithmetic.
The scene reduction retains3 collective and30 within-part eigenmodes. Its
ordered Laurent recurrence does not assume commuting matrices. Positive
series avoid catastrophic FFT cancellation at winding coefficient15 and above.
A degree64 exponential remainder bounds each coefficient by less than1.014e-97.
Serialization uses directed Decimal rounding of exact binary interval endpoints.
The source majorants sum the ENTIRE infinite winding tail with a positive
factorial/geometric bound, not a finite numerical sample.

Native matrix applications are double precision. The maximum direct matrix
or heat identity discrepancy was2.843e-14. Derivatives independently rebuild
the original Julia/Walsh constructor at two neighboring rapidities. Stable
winding-term finite differences agree with the reported native heat sources
to relative error below9.8e-9. They do not subtract two nearly identical large
absolute heat values. These are numerical controls, not interval enclosures
of the native matrices or a certified stationary field.

The inhomogeneous scene guard is load-bearing: the actual K2 x C15 heat
source is not small in the same sense. The theorem never removes this source
from a spatially varying physical model by calling it gauge.

An initial development run failed because a nonzero-width interval cannot be
cast directly to float. The replay now passes explicit coefficient midpoints
to floating matrix controls, while preserving interval endpoints and all
majorants in the independent interval calculation. No action or threshold
was changed to force that fix, and the failed run is not reported as a pass.

No Lean build, new full42 root, independent external review, or repository-wide
CI was run. The larger physical statements remain explicitly open.
