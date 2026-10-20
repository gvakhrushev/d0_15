# Test 5: a native Fisher great-circle image does not select a least-price history

Input owner at `41582f57ce2b4bc8c9fad322e3c2d8ecaadb8b70`:
`02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md`,
P8-P10 and section 2.2.

Fix an actual initial vertex u in the original nine-vertex zone, unit edge
Cost, and neutral terminal task. Let c_n=M^n 1 with the exact native matrix

    M = [[0,11,13],[9,0,13],[9,11,0]].

The n-horizon outgoing law has probability
c_(n-1,B)/(11 c_(n-1,B)+13 c_(n-1,C)) at EACH of the 11 B vertices, and
c_(n-1,C)/(11 c_(n-1,B)+13 c_(n-1,C)) at EACH of the 13 C vertices.
This follows from counting every original completed suffix, not from a new
stochastic ansatz. Work on its fixed 24-outcome simplex face; the nine
forbidden same-zone moves remain absent.

Put b_n=11 c_(n-1,B)/(11 c_(n-1,B)+13 c_(n-1,C)).
Let e_B and e_C be the normalized indicator vectors of the actual 11- and
13-vertex outgoing groups, respectively. They are fixed orthonormal vectors.
The square-root embedding of the ENTIRE 24-component law is exactly

    x_n=sqrt(Q_n)=sqrt(b_n)e_B+sqrt(1-b_n)e_C
                 =cos(theta_n)e_B+sin(theta_n)e_C.

Thus all x_n lie on one fixed great circle solely because of the original
two-group symmetry. Under the ordinary Fisher metric
ds^2=sum_i dq_i^2/q_i, this family has ds^2=4 dtheta^2. Multiplication of the
Fisher metric by a fixed Golden normalization only rescales lengths.
No action, trajectory principle, or selected history was used to obtain this.

There is a stronger actual finite countercontrol: the horizon order reverses
along that circle. Exact native counts give

    b_1=11/24,
    b_2=242/502=121/251,
    b_3=5236/11190=2618/5595,
    b_1 < b_3 < b_2.

Hence theta_2 < theta_3 < theta_1. The path through horizons 1,2,3 backtracks,
and

    2|theta_2-theta_1|+2|theta_3-theta_2|
       > 2|theta_3-theta_1|.

It is therefore not even the shortest Fisher path between its horizon-1
and horizon-3 endpoints. Each segment can be interpolated as a geodesic, but
the chronologically ordered sequence is not a single regular geodesic after
an orientation-preserving reparameterization. Discrete horizon n is also not
an affine parameter, and changing n changes the terminal task rather than
following a realized physical trajectory.

The same literal depth-two enumeration separates three different assertions:

1. Zone majority: K13 has 260/502 versus K11's 242/502.
2. Mode of an individual next vertex: EACH K11 neighbor has 22/502, greater
   than EACH K13 neighbor's 20/502. Aggregating by zone changes the mode.
3. Mode of a complete history: ALL 502 two-step histories have the same
   original Cost 2 and the same probability 1/502. There is no unique mode.

Therefore neither great-circle containment, a next-zone majority, nor even a
mode of the next vertex supplies compulsory selection of one minimum full
history. The useful positive result is an exact, computable Fisher geometry
of the native prospective probability laws; a physical geodesic/minimum
principle would still have to derive the parameter, complete action and
constraint class, and show that the actual dynamical law realizes it.

`check_native_fisher_horizon.mjs` enumerates the true 33-vertex depth-two
paths, computes all horizon counts through 32 with BigInt, checks the
strict reversal by integer cross multiplication, and displays the angle and
Fisher-length excess. It does not replace the graph with a freely chosen
two-state model: the two components are its exact fixed-root symmetry quotient.
