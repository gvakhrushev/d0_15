# Simple / coupled response split

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `673b7f8b9a52f53b311fc1e419a6887e7f677c6c`.
Status: class reduction. No task terminal.

## Split

The full commuting spacelike Y-plane is now an exact class, not a sector sample. Literal edge transport forces the Cayley amplitude to be constant on the even carrier: the two-by-two brackets have determinant `-2(X_s^2+Y_s^2)`, nonzero because the plane is nondegenerate, and `xy=4`, `x+y=0` is impossible over the reals. Spatial rigidity then forces an integrable coframe, so every smooth nondegenerate realization is locally flat. Role permutation and proper Lorentz covariance carry the same statement to the other single-role planes.

Therefore this class has continuum Einstein content, and it is the vacuum content:

```text
Riem[g]=0, G[g]=0.
```

It cannot carry a curved zero-source counterexample, and it cannot carry a new `h^{-2}` response over a curved smooth background. Its image under `Xi` is the flat class.

The opposite type is already owned. The #227 family uses `B=K1+K2+K3`, not a simple plane. It is connection-stationary and has nonzero packed `Xi`. Simple-plane rigidity explains why that memory cannot be reproduced inside the commuting class: the real transport obstruction is algebraic.

## What the diameter theorem reduces to

Prescribed-source collapse is no longer a census of Y amplitudes, signs, wavelengths or common-column envelopes. Those are inside the flat class. A curved gap, if it exists, has to be coupled-role / non-simple joint structure, realized with a source fixed before the candidate. #227 is the model of the holonomy, not the witness: its response is not an independent source.

Verdict: simple commuting planes removed from the closure search. Coupled joint structure remains the carrier. Lane stays `PARTIAL / OPEN`.

## Exact follow-up: the original coupled boost is excluded on the curved warp

The [coupled-boost realizability identity](A4D_COUPLED_BOOST_CURVED_REALIZABILITY.md)
now tests the original #227 family itself on the fixed nonconstant
`S_h=diag(1,1,f(hx1),f(hx1))`, with `tau=0` specified before the candidate.
At phase zero,
`E_(K0,J12)=-2t*(f_n^2-f_(n-1)^2)/(4-3t^2)`.
For `f(y)=1+(1-cos(2*pi*y))/50`, this is nonzero at the origin for every
admissible mesh and every nonzero t in the real Cayley chart. The requested
candidate check ends at outcome 1: `COUPLED_BOOST_EXCLUDED`. The flat #227
readout cannot be used as a curved joint-source witness by simply retaining
those links. This does not quantify over arbitrary different coupled fields;
the parent task remains `PARTIAL / OPEN`.

The same owner now removes arbitrary temporal-amplitude retuning as well.
For independent links `L_(x,0)=Cayley(a_x B)` and identity spatial links,
three actual metric components determine the three boost plaquette
coefficients with determinant `-1/4`. Their exact joint flux identity gives
`||E_K||_owner1 >= (102/625)L^3-90M^2` when
`Xi_diag=h^2 tau_diag`, `||tau_diag||_infinity<=M`.
Thus no sign, wavelength, large common rapidity or arbitrary amplitude array
rescues this B family on the fixed warp with a bounded independent source
as the mesh is refined. This is a single whole-profile exclusion; it does
not address different generators or nonidentity spatial links.
