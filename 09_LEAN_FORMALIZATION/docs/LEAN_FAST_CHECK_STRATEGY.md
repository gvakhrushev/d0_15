# Lean Fast Check Strategy

D0_v14 uses three validation levels. Do not use the full release replay after
every small edit.

## 1. Local Lean Module

Use this immediately after editing one Lean file:

```powershell
cd 09_LEAN_FORMALIZATION
lake build D0.Geometry.PhaseUnfoldingQuasicrystal
```

This is the normal edit loop.

## 2. Slice Gate

Use this after finishing a theory package. It builds only the affected Lean
modules, runs the matching certificate, and runs the relevant sync guards:

```powershell
python tools\run_hard_theorem_closure.py --mode slice --preset information-quasicrystal
python tools\run_hard_theorem_closure.py --mode slice --preset master-evolution
python tools\run_hard_theorem_closure.py --mode slice --preset trace-heat-gravity
python tools\run_hard_theorem_closure.py --mode slice --preset toral-automorphism
python tools\run_hard_theorem_closure.py --mode slice --preset galois-lorentz-signature
python tools\run_hard_theorem_closure.py --mode slice --preset higgs-scalar
python tools\run_hard_theorem_closure.py --mode slice --preset torus-core13
python tools\run_hard_theorem_closure.py --mode slice --preset ckm-phason-holonomy
python tools\run_hard_theorem_closure.py --mode slice --preset condensed-phi-vacuum
python tools\run_hard_theorem_closure.py --mode slice --preset quasicrystal-phenomenology
python tools\run_hard_theorem_closure.py --mode slice --preset phason-flip-entropy-sde
python tools\run_hard_theorem_closure.py --mode slice --preset quasi002-phason-baryon
python tools\run_hard_theorem_closure.py --mode slice --preset meson-phason-domain-walls
python tools\run_hard_theorem_closure.py --mode slice --preset icecube-phason-decoherence
python tools\run_hard_theorem_closure.py --mode slice --preset no-go-stress-suite
```

Manual slices are also supported:

```powershell
python tools\run_hard_theorem_closure.py --mode slice `
  --module D0.Geometry.PhaseUnfoldingQuasicrystal `
  --cert 05_CERTS/vp_information_quasicrystal_phase_unfolding.py `
  --guard tools/check_v14_information_quasicrystal_phase_unfolding_sync.py
```

Changed Lean files can be passed directly:

```powershell
python tools\run_hard_theorem_closure.py --mode slice `
  --changed 09_LEAN_FORMALIZATION/D0/Geometry/PhaseUnfoldingQuasicrystal.lean
```

## 3. Full Gate

The ordinary full gate builds the hard theorem index once. That index imports
and checks the hard-closure targets, so it covers the Lean target set without
replaying every module as a separate `lake build`.

```powershell
python tools\run_hard_theorem_closure.py --mode full
```

For release audit only, replay every CSV module individually:

```powershell
python tools\run_hard_theorem_closure.py --mode full --release
```

`--release` is intentionally expensive. It should not be part of the normal
edit loop.

`D0.Dynamics.TraceHeatLucasCore` is the light edit-loop owner for Lucas heat
moments and Lefschetz counts. `D0.Dynamics.TraceHeatCapacityGravity` extends it
with capacity/gravity interfaces, so master-evolution checks do not need to
pull the full gravity stack during ordinary theorem edits.
