# WRK-A4D-LOCAL-REVERSE-STAR-NOGO

Object: **scalar two-sided local reverse star** on one color. This is NOT the located two-color `J` and NOT the Lorentz/observer metric star.

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

READY when a WORKER slot is assigned and the scalar kernel `W=I+H` / its one-dimensional restriction is available from the flux API or explicitly accepted by CONTROL. Do not wait for the full located `J`; this no-go is one-color scalar-stencil algebra.

The generic Laurent-width theorem itself is standalone and may be drafted before that API lands.
## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.

## Scope firewall

This no-go does NOT cancel the located two-color `J`, does NOT prove the absence of a Lorentzian metric star, and does NOT select nonlinear `Q(e)`. It only excludes a uniformly local one-color reverse/inverse stencil under its stated hypotheses.

## Objective

Lean-own the research no-go that an exact two-sided scalar star cannot simultaneously have:

- uniformly bounded translation-covariant forward support;
- uniformly bounded translation-covariant reverse support;
- exact scalar composition `±I`;
- the accepted neighboring scalar first jet.

This is a scoped locality/inverse theorem.

It is NOT a no-go for inverse-free parent actions or enlarged auxiliary carriers.

## Suggested module

`D0/Geometry/A4DLocalReverseStarNoGo.lean`

## Package A — explicit L=5 witness

For constant scalar `e_A^A=t=1/2`, formalize:

[
W_1=\frac54I+\frac14(U+U^{-1}),
]

[
W_2=\frac32I+\frac14(U+U^{-1}).
]

Prove exact inverse columns:

[
W_1^{-1}e_0=(116,-24,4,4,-24)/133,
]

[
W_2^{-1}e_0=(41,-7,1,1,-7)/58.
]

Hence both inverses have nonzero distance-two entries.

## Package B — generic Laurent-width theorem

Define a finite-radius translation-covariant scalar stencil as a Laurent polynomial.

For radii `R,R'` and period satisfying

[
L>2(R+R'),
]

show that an identity

[
p(z)q(z)=c
]

modulo `z^L-1` lifts to the Laurent polynomial ring.

Prove a Laurent polynomial unit with scalar inverse is a nonzero monomial.

## Package C — first-jet contradiction

Assume:

[
p_0(z)=1,
]

and

[
\partial_t p_t|_{0}=(z+z^{-1})/2.
]

Prove no uniformly radius-bounded family `p_t,q_t` can satisfy exact scalar inverse/composition for all sufficiently large periods.

## Truth boundary

Do NOT claim impossibility of:

- finite dense inverses;
- reverse support growing with `L`;
- inverse-free primal/dual parent;
- larger local auxiliary fiber;
- Lorentzian star distinct from positive energy Riesz kernel.

## Expected verdict

```text
UNIFORM-TWO-SIDED-LOCAL-REVERSE-STAR-NOGO-OWNED
```
