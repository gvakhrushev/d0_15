# Local Raychaudhuri representation and two-readout dark-response boundary

## Verdict

The local pressure-capacity law now has an explicit physical application interface, but no physical
instance is claimed. Conditional on the three registered representation equalities, Lean derives
the local coupled law

```math
a_{measured}(x)=D_{defocus}(x)-F_{focus}(x).
```

Separately and unconditionally, Lean proves that `a_measured` alone cannot identify the two terms.
The decomposition has an infinite-dimensional common-shift gauge. A second independently measured
focusing field is therefore necessary and sufficient to recover the dark/defocusing field.

## Internal owner

`D0.Gravity.LocalPressureCapacityDynamics` owns

```math
\Delta\theta(x)=\kappa(P_{fb}(x)-P_{cap}(x)).
```

It proves balance, acceleration, braking, reversal and local inhomogeneity over arbitrary real
fields. It does not name the fields as matter or dark energy.

## Conditional physical representation

`D0.Bridge.BridgeAssumption.LocalRaychaudhuriRepresentation` must be supplied by an application. It
requires

```math
\kappa P_{cap}=\theta^2/3+\sigma^2+F_{matter},
```

```math
\kappa P_{fb}=\omega^2+D_{archive},
```

```math
a_{measured}=\kappa(P_{fb}-P_{cap}).
```

Here `F_matter` is already normalized to the active gravitational-mass term used by the chosen
continuum convention. The conversion from density/pressure and SI time to these fields is not
derived by this module.

## Structural non-identifiability

For arbitrary local functions `D,F,g`,

```math
(D+g)-(F+g)=D-F.
```

Lean constructs a distinct observational twin for every nonzero `g` and proves by contradiction
that no universal function of the net field can recover `D`. This is not parameter counting: the
obstruction is an exact gauge over the complete function space.

The gauge is removed by an independent focusing readout:

```math
D=(D-F)+F.
```

At fixed net response, any change in the independently measured focusing field forces the recovered
dark field to change as well.

## Required empirical passport

A future application must preregister two non-circular observable blocks on matched local domains:

1. a local expansion/acceleration or velocity-divergence readout with covariance;
2. an independently reconstructed focusing load including matter, shear and the declared kinematic
   corrections.

The dark/archive residual is then computed, never fitted as a free field. Expansion data used in
block 1 cannot also define block 2. Survey names, smoothing scale, domain matching, covariance,
null model and hash-pinned source files must be frozen before evaluating the residual.

Until such an instance is supplied, the correct external verdict is
`NOT_TESTED_NO_LOCAL_RAYCHAUDHURI_REPRESENTATION`. The Lean result closes the information boundary,
not the observational dark-sector claim.
