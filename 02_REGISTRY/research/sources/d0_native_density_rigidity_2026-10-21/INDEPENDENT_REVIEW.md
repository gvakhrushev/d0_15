# Independent review of fixed-measure density rigidity and dust realization

21 October 2026. Reviewer: bounded read-only `preparation_composition`
assistant of the existing #334 integrator. This review did not author the
proof or its checker and did not modify either. It is scientific review
of the stated conditional continuum theorem, not a physical Book03 or GR
assembly acceptance.

## Frozen result examined

* `PROOF.md`:
  `23794bfbfbbe8c3524f370461ccc616d2c7653318e4a578250354db378fa26a2`.
* `check_density_rigidity.py`:
  `ecac5ea134d01f1b9d4b1521a7879788bd7ac69586dd75072834afb65b656531`.
* `SOURCE_PINS.json`:
  `d12f14b6b3f11cad97e6981b6055012e0d5731d7140209e4535d715d6496abc1`.
* `README.md`:
  `d57450deffe7b96cb4cc7dff9c5eb295f7149c5b0deb8e194e3761675ba25557`.
* `RESULT.json`:
  `38f72c05c75a82ca2e4174d7dbdd28336283be0ba1d687bccab2151b8747e98b`.
* Preserved spatial-source snapshot:
  `b13ef78db2ef108ce0435bc3b678822b4518d6e0eaa4d8610f4672cd5798eafd`.

All seven files listed in `FROZEN.json` matched their final hashes during
review. The eight scientific source hashes were independently checked by
the replay and compared with their exact historical git blobs. The relevant
original continuum dictionary and Euler rows were
read directly in
`A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE_2026_10_21.md`, §§2–3;
the actual domain, unique trace branch and cap-uniform inequalities were
read directly in
`A4D_EXACT_NATIVE_RADIAL_MINIMIZATION_ALL_ORDERS_2026_10_21.md`, §§3–5.

### Provenance preservation after the concurrent source append

The final binding above includes a separately reviewed provenance-only
amendment. The source
`A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21.md`
advanced concurrently after the packet's recorded read head
`dfc0275eea67ebc21ffe539de9b6ea96713863a5`. Its original 18,886 bytes are
now preserved in
`inputs/A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21_dfc0275e.md`.

The reviewer directly compared that snapshot against `git show` at the
recorded read head and independently checked its original git blob
`4d637bae96f94ab0b18c9509bcf64e8609d47375` and SHA256 stated above.
All bytes agree. The version at `8463b0a4` contains those same 18,886 bytes
as an exact prefix and appends 1,270 bytes comprising the new Section 7
composition pointer. The reviewed mathematical input was not replaced by
that later section.

The amendment is exactly bounded by independently reproduced prior hashes:

* Removing only the new `snapshot_path` member from `SOURCE_PINS.json`
  reproduces its prior hash
  `4483b7e1332eb794875d62ae8327c98dad8de26f974440f1763c840fd2210c6f`.
  Its original path, read head, git blob and expected SHA256 remain intact;
  all seven other entries are unchanged.
* Reversing only the checker's source-routing change reproduces its prior
  hash `5a23285b2be2a40b6060267ac4f92c88eb2ead5ae58a86854a2a5f01810c77fb`.
  The new `packet=Path(__file__).resolve().parent` locates the manifest and
  its explicit snapshot; an entry without `snapshot_path` still reads
  `args.repo/item['path']`. Every entry is still checked against the same
  original expected SHA256. No symbolic identity, numerical fixture,
  tolerance, scientific condition or failure behavior changed.
* Removing only the README's new preserved-input explanation reproduces
  its prior hash
  `f11241e3e04c02f527e0c079294945de8b9a4081e6cbb243e2c2a9de8f8af406`.
* `PROOF.md`, `RESULT.json` and `RESULT_OPTIMIZED.json` are byte-identical
  to the previously reviewed versions. Both new independent checker runs,
  normal and `python3 -O`, reproduce those same result bytes.

**The mathematical verdict and its acceptance boundary are unchanged.**
This is preservation of the previously examined evidence, not a blind hash
refresh: the historical source bytes and git identity were independently
verified, the newer append was inspected, the previous code and manifest
hashes were reconstructed by reversing only the stated routing amendment,
and the original expected scientific-input hashes were retained.

## Verdict

**PASS on the stated fixed-coordinate-measure continuum chart.** The new
results are substantive applications of the pinned owners:

1. every full stationary field has constant `x,y` on a connected domain;
2. all admissible fixed finite caps have the same entire field critical set;
3. at any such common background, the full coupled Jacobi kernels agree
   on the same perturbation space vanishing on a fixed collar;
4. regular local timelike and null irrotational dust geometries have
   representatives in this common set in explicitly chosen mass coordinates.

The results do not require a homogeneous or Bianchi ansatz. They do require
the precise fixed measure, scalar query, constant internal parameters and
independent field variations stated in the proof.

## Analytical checks

### Full-domain nonvanishing before the radial division

The use of `V_N' != 0` is not circular. The radial owner's §3.3 already
proves `z<r<2z` on the **whole** rectangle, before its cap-slope argument.
The new self-contained bound is also correct: the Golden brackets give
`1/4<E<1/2` and `1/2<b<2/3`; hence `3/4<ell,B,A<1` and
`1<3/2-z<r/z<2`. Only after that nonvanishing is established does the
radial Euler equation imply `T=0` and use the unique branch `x=tau(y)`.

### Fixed-measure variation and pressure constraint

Under the permitted compactly supported active Lie variations, `eR` is a
weight-one density and `q` is a scalar. Holding the coordinate measure
fixed gives

```
delta S = integral [x F_x-F] div(xi)
        = integral xi^mu partial_mu(F-xF_x).
```

The sign in the integration by parts and the pressure definition are
correct. This derives `dP=0` from the full field equations; it does not
assume diffeomorphism invariance or vary an external volume field. The
exclusion of an externally varying additive baseline from this calculation
is necessary and is correctly stated.

On the trace branch, direct differentiation gives
`P'=Q-tau M'=Q(1-yM'/M)`. The rational products in the stated bounds are
exactly `2475/266` and `80512/1845`, so the normalized slope lies between
9 and 44. Its actual nonzero factor `a_N` is retained. This proves constant
`x,y`; no homogeneous ansatz or early connection elimination is used.

### Full critical sets and connection equations

At constant queries the response `r_*` and every `V_N'(r_*)` are spatially
constant. Therefore the equality of full first variations for different
caps holds for **all** compactly supported independent variations, not
only those preserving the densities. The usual nondegenerate Lorentz
Palatini connection equation has no independent material source and forces
the torsion-free connection here. The resulting metric and scalar rows
match the original owner's equations. The absence of the densitized
massless-scalar `-g q/2` term is correctly retained.

The all-cap result is an equality of stationary sets, not a field-price
normalization or a comparison of different horizons as prospective tasks.
The retained `V_N''` term correctly prevents an unjustified assertion of
equal Hessians or equal minima.

### Full Jacobi kernels, including nonintegrable kernel vectors

The strengthening in §8 is valid without assuming that a Jacobi vector
integrates to a nonlinear solution. Differentiate the off-shell identity
`DS[L_xi Phi]=integral xi dP`. At a stationary background, the additional
term from differentiating `L_xi Phi` is multiplied by `DS=0`. A full
Hessian-kernel vector therefore implies `d(delta P)=0`. The same argument
with the actual radial variation gives `delta T=0`.

Since `T_x != 0` and the branch pressure slope is nonzero,
`delta x,delta y` are constant. Perturbations that vanish on a collar force
both constants to zero, including all derivatives entering the densities.
Thus `delta_v r=0`, which kills the entire extra density-product bilinear
term in `H_M-(V_M'/V_N')H_N` against every test variation. Reversing the
argument proves equality of kernels. A condition only on boundary values,
without the stated collar or another argument fixing the density constants,
must not be silently substituted. The proof explicitly excludes larger
boundary-mode spaces and equality of the Hessian operators.

### Timelike and null dust converses

For one timelike scalar, the normalization `u=dpsi/sqrt(q_*)` gives a unit
gradient with geodesic flow, and the metric row is Einstein pressureless
matter with `rho=(r_y/r_x)q_*/e>0`. The undensitized scalar equation gives
the dust continuity equation because `e rho` is constant.

Conversely in proper-time/comoving coordinates of a regular irrotational
dust solution, conservation gives `e rho=C(X)>0`. The displayed spatial
relabeling has Jacobian `C/k`, so the new density is exactly `e_new rho=k`;
it is time independent and preserves the proper-time potential. The chosen
`k=-tau_branch(y_*)/eta^2` is positive and obeys
`r_x k=r_y q_*`. With the original curvature convention, tracing
`G=rho u tensor u` gives `R=-rho`, so the signs in the query reconstruction
and all original rows agree.

For null dust, the nonvanishing potential differential allows it to remain
one coordinate while a transverse coordinate normalizes the positive form
`varrho vol_g`. The required density `e varrho=L0 c^2` gives the original
metric row and, via conservation, its undensitized scalar row. Its scalar
curvature and scalar kinetic query are both zero, so the null case does
not require a Brinkmann or VSI ansatz. These are local representative
constructions in selected coordinates, not a claim that arbitrary
coordinate changes are physical symmetries of the nonlinear action.

### Finite PF remainder

The independent optional finite-lattice normal-form calculation retains
the actual `m_i=C rho_i`, `epsilon_i=eta_h^2/rho_i` and query signs.
The normalization `m_i/a_h=1/(a epsilon_i)` gives exactly the displayed
residual and its first/second derivative bounds. Link-independence follows
from the stipulated undensitized material query with independently varied
links. No continuum Lie variation is automatically available on that
finite or spatially inhomogeneous ledger; the proof preserves this boundary.

## Independent execution

Executed the final frozen checker with

```
PYTHONPATH=/tmp/d0_pydeps python3 /tmp/d0_native_density_rigidity/check_density_rigidity.py --repo /workspace/scratch/75286bd77d4e/d0_15
```

It passed **101 explicit checks**. The independent normal and `python3 -O`
stdout in `INDEPENDENT_REPLAY.json` and
`INDEPENDENT_REPLAY_OPTIMIZED.json` is byte-identical to the unchanged
frozen `RESULT.json` and `RESULT_OPTIMIZED.json`.
The maximum normalized pressure-identity numerical error is
`2.29735755304e-81` in the declared 85-digit fixture. The finite cap samples
are controls of the new identity and do not replace the all-cap analytical
proof. No old Bianchi, full40, native spectral, compiler or Lean suite was
rerun, and no remote CI result is asserted by this review.

## Acceptance boundary

This review supports the conditional continuum theorem and its exact parent
substitution. It does not promote compulsory Book valuation, arbitrary
native field writing, internal preparation/observer/clock equations,
finite-lattice continuum admission, uniform refinement, off-shell natural
metric-source descent, generic GR or raw216. In particular a mass-coordinate
dust representative is not the missing off-shell Diff-natural physical
source required by the separate Golden universality theorem.
