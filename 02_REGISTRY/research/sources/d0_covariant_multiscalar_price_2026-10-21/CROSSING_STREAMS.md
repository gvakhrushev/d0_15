# An explicit rank-two, non-VSI solution of the same complete continuum price

21 October 2026. Constructive application of [the local covariant representation](PROOF.md)
inside existing PR #334. This is an exact continuum solution for the SAME
fixed-measure, two-query price of that theorem. It is not an exact finite
Cartan-lattice solution or a claim of physical Book03 selection.

## 1. The positive witness

On a local coordinate box `(b,x,y,z)` with `b>0`, choose any constant `d>0`
and set `F(b)=exp(d b^2/2)`. Use the original `(+---)` signature and curvature
convention. Define

```math
ds^2=bF(b)\,db^2-\frac{F(b)}b\,dx^2-b^2(dy^2+dz^2),
\qquad
\psi_1=\frac{b^2}{2},\quad \psi_2=x,\quad
\Lambda=\frac d{b^2}.
```

Constant shifts of either scalar have no effect. Thus a small coordinate
patch can also give arbitrarily small scalar amplitudes around a selected
point. The two gradients are independent on every such patch. Their norms
are respectively `b/F` and `-b/F`, so their TOTAL kinetic scalar is

```math
q=g^{-1}(d\psi_1,d\psi_1)+g^{-1}(d\psi_2,d\psi_2)=0.
```

Take a nondegenerate orthonormal coframe of this metric and its actual
Levi-Civita spin connection. The independent connection equation of the
representation theorem is then satisfied, rather than discarded by varying
a metric ansatz in place of the original first-order fields.

Direct calculation from this metric gives the complete tensor

```math
\operatorname{Ric}_{\mu\nu}
=\operatorname{diag}\left(d,\frac d{b^2},0,0\right),\qquad R=0.
```

Consequently `G=Ric=Lambda(dpsi_1 tensor dpsi_1+dpsi_2 tensor dpsi_2)`
in ALL ten metric components. The volume density is `e=b^2F`. The two
covariant scalar current densities are exactly

```text
e Lambda grad psi_1 = (d,0,0,0),
e Lambda grad psi_2 = (0,-d b,0,0).
```

Both have zero coordinate divergence. Every metric, independent-connection,
two-scalar and multiplier equation of the covariant representation is
therefore satisfied at `q_*=0`. This is a direct full-equation check, not
variation of the action restricted to the displayed ansatz.

Equivalently, the covectors

```math
\ell_\pm=\frac{d\psi_1\pm d\psi_2}{\sqrt2}
```

are individually null and independent, and the source is
`Lambda(ell_+ tensor ell_++ell_- tensor ell_-)`. The total tensor has rank
two. In this particular example each stream is also conserved separately:
its `Lambda ell_+/-` current is a constant linear combination of the two
conserved scalar currents, and its kinetic norm is identically zero.
The identity in the representation proof then gives
`div_g(Lambda ell_+/- tensor ell_+/-)=0`. This stronger property of the
explicit witness is not asserted for arbitrary total-null two-field data.

## 2. The actual native-volume representative

The ORIGINAL finite-fugacity query fixes the positive number

```math
k_0=\frac{r_y(0,0)}{r_x(0,0)}
=-\lambda_-(2^{-20})\approx23.416406751884.
```

It is not fitted to the new metric. Introduce the time coordinate `tau`
by the strictly positive derivative

```math
\frac{d\tau}{db}=\frac d{k_0}\exp(db^2/2).
```

The lower integration endpoint is arbitrary and only shifts `tau`. Since
this derivative never vanishes, the map has a smooth local inverse. In
coordinates `(tau,x,y,z)` the SAME metric and scalar fields have

```math
e_{\rm native}=\frac{k_0b^2}{d},\qquad
e_{\rm native}\Lambda=k_0.
```

Now `x_query=eta^2 e_native R=0` and `y_query=-eta^2 q=0` everywhere,
while their full ambient variations are not set to zero. In these coordinates
the original, undensitized matter equations hold exactly:

```text
g^(tau tau) partial_tau psi_1 = d/k0,
partial_mu(g^(mu nu) partial_nu psi_A)=0, A=1,2.
```

The original metric equations are exactly `e_native G=k0 sum_A dpsi_A^2`.
The common nonzero factor `eta^2 V_N'(r0) r_x(0,0)` multiplies the full
first variation for every admitted finite cap. Therefore this same native
representative is a full stationary point of EVERY `S_N` in the density-
rigidity theorem, including both real material fields and all sixteen
coframe plus twenty-four independent connection equations.

The coordinate transport is essential. The untransformed `b` chart generally
does not solve the original fixed-volume equations, because there
`e Lambda=d exp(db^2/2)` is not the required constant. The checker explicitly
rejects omitting this transformation. Boundary data are transported with it;
there is no assertion that it preserves an arbitrary old fixed collar.

## 3. Why this extends the existing positive solution class

The curvature invariants are

```math
R_{\mu\nu}R^{\mu\nu}
=\frac{2d^2}{b^2}e^{-db^2}>0,
\qquad
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
=\frac{12}{b^6}e^{-db^2}>0.
```

For completeness,

```math
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=\frac{4(d^2b^4+3)}{b^6}e^{-db^2}.
```

Thus this metric is not a coordinate rewriting of the old VSI Brinkmann
family: its Ricci and Weyl contractions are nonzero scalar invariants. Its
rank-two material tensor is also not the earlier single null-direction
source. The two components of the original matter field are both active;
dropping the second leaves a nonzero `xx` equation `d/b^2`.

This is a constructive enlargement of the SAME configured continuum
stationary set, with the SAME original Golden ratio. We do not claim that
the underlying GR/counterstreaming solution is new to the literature.
The new use is its explicit substitution into the complete native-price
equations through the proved volume-gauge equivalence.

Nonzero scalar invariants also mean that the old pp-wave/VSI protection
argument cannot be applied to this metric. No conclusion about an arbitrary
higher-curvature Euler correction is drawn merely from its action density:
such a correction must still be varied and checked on this witness.

## 4. What this does and does not close

The two-scalar covariant representation now has a concrete nonparallel,
non-VSI positive application, rather than only a renamed one-scalar dust
sector. The original finite query coefficient is used exactly. At this
`x_query=y_query=0` source point it is also the coefficient measured by the
separate exact finite Golden source-reconstruction theorem.

Still needed for a physical D0 conclusion: the actual finite-lattice-to-
continuum density/source transport, admitted joint field variations,
independent preparation/controller/clock equations, and compulsory complete
Book valuation. This result proves none of those by changing the action.
No stationary minimum, perturbative stability, global cosmology, singularity
extension, universal GR source, or raw216 completion is claimed.

## 5. Reproduction

Run `python3 examples_crossing_streams.py` in this directory (SymPy required).
The script constructs the Christoffel symbols and Riemann tensor from the
displayed metric, contracts all Ricci components and the curvature
invariants, checks both scalar currents and every metric row, then checks
the coordinate pullback into the original native-volume equations.
It retains the two independent negative controls above. The script does
not import a precomputed Einstein tensor or the old all40 lattice checker.
Analytical identities hold for arbitrary positive `b,d,k0,eta`; no finite
sample scan replaces them. The actual output is `CROSSING_STREAMS_RESULT.json`.
