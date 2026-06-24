#!/usr/bin/env python3
# vp_isotropization_residual.py
# Cert for D0-ISOTROPIZATION-MECH-001 (MECH-LIMIT): the falsifiable shape-anisotropy residual.
#
# The graph->space hinge is an isotropizing limit; the INCOMPLETE-isotropization residual is the
# shape-mode splitting of the vacuum cubic lambda^3 - 359*lambda - 2574, whose coefficients are the
# frozen scene symmetric functions (e2=359, 2*e3=2574 for (9,11,13)). Perron mode = volume; the two
# negative roots are the shape modes. Residual: Delta_lambda ~= 2.3208, fractional ~= 0.2126.
# This is the observable of the standing shape-anisotropy falsifier; the dimensionful gap->amplitude
# map is the OPEN MECH-LIMIT realization (NOT a number claimed). Exact symmetric functions + numeric roots.
import numpy as np

ok = True
def chk(name, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    ok = ok and bool(cond)

n1, n2, n3 = 9, 11, 13
e2 = n1 * n2 + n1 * n3 + n2 * n3
e3 = n1 * n2 * n3
chk("cubic coefficients are scene symmetric functions: e2=359, 2*e3=2574", e2 == 359 and 2 * e3 == 2574)

roots = sorted(np.roots([1, 0, -e2, -2 * e3]).real)        # lambda^3 - 359 lambda - 2574
perron = max(roots)
shape = [r for r in roots if r < 0]
chk("three real roots; one Perron (volume) + two negative (shape)", len(shape) == 2 and perron > 0)
chk("Perron ~= 21.8374 (volume mode)", abs(perron - 21.8374) < 1e-3)
dlam = abs(shape[1] - shape[0])
lbar = sum(shape) / 2
frac = dlam / abs(lbar)
chk("absolute shape splitting Delta_lambda ~= 2.3208", abs(dlam - 2.3208) < 1e-3)
chk("fractional splitting Delta_lambda/lbar ~= 0.2126", abs(frac - 0.2126) < 1e-3)

# CONTROL (must FAIL the 'isotropic' reading): an equal-zone scene K(n,n,n) has ZERO shape splitting,
# so a nonzero residual genuinely requires the DISTINCT sizes (9,11,13).
m = 11
e2e = 3 * m * m
roots_eq = sorted(np.roots([1, 0, -e2e, -2 * m ** 3]).real)
shape_eq = [r for r in roots_eq if r < 0]
dlam_eq = abs(shape_eq[1] - shape_eq[0]) if len(shape_eq) == 2 else 0.0
assert dlam_eq < 1e-6, "CONTROL: equal-zone K(n,n,n) must have zero shape splitting (degenerate shape modes)"
print("  CONTROL ok: equal-zone K(11,11,11) shape splitting = 0 (residual needs distinct sizes)")

assert ok, "RESULT: SOME FAIL"
print("\n[STATUS] MECH-LIMIT: residual shape-anisotropy controlled by the exactly-known cubic gap;")
print("         dimensionful gap->amplitude realization stays OPEN (no number claimed).")
print("[CERT-CLOSED] PASS_ISOTROPIZATION_RESIDUAL")
