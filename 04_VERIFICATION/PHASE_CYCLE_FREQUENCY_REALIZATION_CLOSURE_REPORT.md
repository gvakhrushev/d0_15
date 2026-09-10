# Finite phase-cycle frequency realization — closure report

Date: 2026-08-26

## Verdict

The abstract self-return frequency passport now has a concrete finite in-repository realization,
and its deletion boundary is proved structurally:

1. `D0-FINITE-PHASE-CYCLE-FREQUENCY-REALIZATION-001` — `CORE-FORMALIZED`;
2. `D0-RAW-CYCLE-WINDOW-REDSHIFT-NOGO-001` — `NO-GO`.

Lean owner: `D0.Cosmology.PhaseCycleFrequencyRealization`.

Certificate: `05_CERTS/vp_phase_cycle_frequency_realization.py`.

## Constructive chain

The existing phase action is not treated as a continuum angle. It acts on a finite rational
quadrature by a quarter turn. Lean proves:

- four quarter turns return every quadrature;
- three turns fail to return a concrete nonzero quadrature;
- every finite count of four-turn blocks returns.

A protocol then freezes one positive completed-cycle count `N` and one positive base window `W`
before comparison. Its depth-`n` window is `W*phi^n`, and its readout is the ordinary finite rate
`nu(n)=N/(W*phi^n)`. Lean derives `nu(n+1)=nu(n)*phi^-1` and constructs the already-verified
`PreregisteredSelfReturnFrequencyProtocol`. The physical/internal frequency-ratio equality and the
one-tick drift theorem then follow as corollaries. The count and absolute window normalization
cancel; neither is tuned to the output.

## Universal factorization and reductio

For arbitrary raw positive emitter/observer registrations define the normalized window
`Wbar=W/phi^depth`. Lean proves for every such comparison:

`nu_em/nu_obs = (N_em/N_obs) * (Wbar_obs/Wbar_em) * phi^(o-e)`.

Equal cycle count and equal normalized window therefore force the D0 ratio. Taking the
contrapositive gives the M1-shaped result: a different ratio at the same registered depths must
change the completed-cycle count or the normalized window. This quantifies over the whole raw
carrier and does not enumerate rival models.

A second parametric theorem constructs, for every positive `r`, raw registrations whose ratio is
`r`. Thus cycle-count vocabulary alone does not force `phi`; the preregistered window covariance is
load-bearing.

## Mutation controls

The executable certificate rejects:

- three turns renamed as a completed phase cycle;
- varying the cycle count between the two sides while claiming cancellation;
- varying the normalized base window while claiming cancellation;
- claiming that raw cycle/window registration forces `phi`.

## Exact boundary

The internal representation is now constructive and assumption-free. No claim is made that an
arbitrary astronomical instrument already realizes it. A physical application must still map a
specified laboratory fringe return to the finite four-turn cycle and its preregistered clock gate
to the transported detector window. Without that representation, the raw NO-GO applies.

No SI scale, spectral catalogue, FLRW model, Hubble parameter, or survey datum enters the theorem.
