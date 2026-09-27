# A4D registered-carrier gauge taxonomy / multi-layer unfolding correction

**CONTROL status:** roadmap synthesis; no claim/release promotion.  
**Inputs:** merged local-Lorentz quotient, #208 J2 quotient coordinates, #249 flat metric identity, #252 census, merged replay #262.

## 1. Registered-carrier law

An owner may be transported only through a typed map that is itself owned or constructed and checked. Equality of dimensions, a nearby period, a shared name such as "gauge", or a matching integer does not create a functor.

This separates three objects that were compressed in the #257/#262 handoff language.

### Layer L — local proper-Lorentz frame gauge

On nondegenerate solder the star action has an exact finite site-dependent proper-Lorentz symmetry. Its complete quotient coordinates are

[
Q_x=Theta_xetaTheta_x^T,qquad
K_{x,r}=Theta_xL_{x,r}Theta_{x+r}^{-1}.
]

Thus the J2 metric/connection carrier built from variations of ((Q,K)) is already Lorentz-quotiented. A later 68-dimensional Fourier census must not subtract those vertical directions again.

### Layer A — flat forward-coframe / affine node gauge

`A4DGaugeImageResolution` owns instead

```text
flatNodeGaugeMap : LocalRoleVector 0 -> LocalCoframeField 0
rank range D0 = 60, dim kernel D0 = 4, L = 2.
```

This is the flat coframe/translation-type exact image. It is not the six-parameter local Lorentz algebra. The missing construction is whether this flat owner descends or lifts to the L4 ((Q,K)) carrier at all.

### Layer J — L4 joint response carrier

Merged #262 owns the conjugate-paired real carrier
`R^20_metric (+) R^48_connection`, with metric-only dimension two on all nine singular orbit representatives and a six-dimensional connection-only block only on the diagonal quarter-wave orbit.

No affine gauge label is attached to those subspaces until Layer A is mapped to Layer J by an exact typed construction.

## 2. First kill: the naive period-covering explanation is insufficient

The character map

[
pi:(mu_4)^4	o(mu_2)^4,qquad
pi(zeta_0,ldots,zeta_3)=(zeta_0^2,ldots,zeta_3^2)
]

is a legitimate finite map, but the fibre over the fully alternating L2 character is

[
pi^{-1}((-1,-1,-1,-1))={pm i}^4,
]

which has 16 characters. It includes both the diagonal ((i,i,i,i)) orbit and the ((i,i,-i,-i)) orbit type. #262 gives connection-only dimensions 6 and 0 respectively. Therefore the covering alone cannot explain "connection-only exists only on the diagonal". Any such result needs an additional equivariant selector, an actual intertwiner whose matrix vanishes on the other fibre components, or a proof that no nonzero lift exists.

A second independent kill is dimensional. Fourier decomposition of the flat L2 coframe differential has at most four gauge-image dimensions at one nonzero character. Hence the proposed test "image rank must be 0 or 6 because dim so(1,3)=6" cannot follow from `D0`; it mixed Layer A with Layer L.

## 3. Second kill: metric-only two-plane is not an operator two-plane

The #262 metric-only block is a two-dimensional subspace of the **real metric amplitude carrier** (`ker C_real^T`). The accepted E-LIN result `span{E_eta,E_sp}` is a two-dimensional family of **linear response operators**. Direct equality of these two planes is ill-typed.

The meaningful finite question is symbol-level: at the same L4 character, realify the two response symbols on the same 20-dimensional amplitude carrier and compute their kernels, images, restrictions and intersections with `ker C_real^T`. That is registered as a bounded WORKER task.

## 4. Third firewall: seam integers are hostile controls only

The seam packet owns co-vertex cardinality 32, cut 20, capacity 5 and (R_*^{cv}=5/32). The L4 carrier happens to contain the integers 32 (diagonal connection Hessian rank) and 20 (metric real dimension / diagonal joint nullity depending on context). They live on different typed carriers. No map is registered between them. Equality of the integers creates no theorem and no mass/time selector.

In particular this synthesis does not identify (37/32) with any (arphi) power, does not produce (mu_{BH}) or Bondi time, and does not promote a Bianchi or plasma passport.

## 5. New executable fronts

### EXP-A4D-AFFINE-COFRAME-PERIOD-DESCENT

Classify the actual missing bridge: whether the flat L2 forward-coframe/affine image has a canonical typed descent/lift to the L4 ((Q,K)) carrier. The search must classify the character-fibre representation and any required selector, not assume the diagonal root.

Two scientifically useful endings are allowed: a concrete exact induced map with orbit-by-orbit image/intersection data, or a theorem-grade representation/selector obstruction showing that current owners do not define such a map.

### WRK-A4D-METRIC-ONLY-SEED-SYMBOL-RELATION

Put `ker C_real^T` and the realified `E_eta/E_sp` symbols on exactly the same L4 metric-amplitude carrier and compute the exact relation. This either finds a genuine seed/operator interpretation of the two metric-only amplitudes or kills the apparent dimension-two coincidence.

## 6. Consequence for live #259/#260

The diagonal slow-lift and invisible-germ workers remain legitimate finite census/germ tasks. They must not label a direction gauge using `range D0`, nor use the existence of the six-dimensional diagonal connection-only block as a local-Lorentz identification. Their results become hostile data for the new EXP classification, not a substitute for the missing typed descent.

## 7. Current synthesis terminal

```text
LOCAL-LORENTZ-QUOTIENT-ALREADY-DOWNSTAIRS
AFFINE-COFRAME-L2-TO-L4-DESCENT-OPEN
NAIVE-CHARACTER-SQUARE-DIAGONAL-SELECTION-REJECTED
METRIC-AMPLITUDE-PLANE-VS-OPERATOR-SPAN-TYPE-CORRECTED
```

No Einstein equation, remnant law or cross-carrier selector is claimed.
