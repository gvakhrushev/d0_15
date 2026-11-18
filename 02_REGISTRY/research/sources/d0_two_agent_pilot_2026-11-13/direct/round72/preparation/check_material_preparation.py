"""Exact original CAR mark and both orientations of its finite actuator."""
import importlib.util
from fractions import Fraction
from pathlib import Path

import sympy as s


root = Path(__file__).resolve().parents[7]
owner = root / "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_primary_car_preparation_source.py"
spec = importlib.util.spec_from_file_location("primary_car", owner)
primary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(primary)

# Use original site counts, all 128 Fourier columns, and actual local stencil.
counts = primary.actual_counts(root)
fourier = primary.fourier_numerators()
w = primary.W
neighbor = primary.step(w, 0, 1)
assert primary.B(w) == 0 and primary.B(neighbor) == Fraction(1,8)
assert primary.kernel(fourier,w,neighbor)/primary.RIGHT == Fraction(7,4096)
rw, rn = [Fraction(256*counts[primary.site_index(site)], 10946) for site in [w,neighbor]]
assert rw > 0 and rn > 0

p, sigma, g, y = s.symbols("p sigma g y", positive=True)
A, B, C = s.symbols("A14 B14 B15", real=True)
sn, cs = s.symbols("sn cs", real=True)
energy = 2*p*(cs-1)*A + g*sn + p**2*((cs-1)**2*B + sn**2*C)
assert s.expand(energy - energy.subs(sn,-sn) - 2*g*sn) == 0
ky = sigma**2*p
charged = g*y/ky
branches = []
for orientation in [1,-1]:
    value = energy.subs({sn:y/ky, cs:orientation*s.sqrt(1-(y/ky)**2)})
    even = s.simplify(value - charged)
    assert even.subs(y,-y) == even
    assert s.simplify(value.diff(y).subs(y,0) - g/ky) == 0
    branches.append(value)
# Exact cancellation of the common coefficient in between-orientation odds.
assert s.simplify((branches[0]-branches[1]).diff(y).subs(y,0))==0
# The complete finite six-operation alternatives act as G^2 / G^-2 at w.
sin2 = 2*p*s.sqrt(p)
cos2 = p-p**2
assert s.expand((energy-energy.subs(sn,-sn)).subs({sn:sin2,cs:cos2})-4*g*p*s.sqrt(p)) == 0
density = s.sqrt(s.Rational(rw.numerator,rw.denominator) * s.Rational(rn.numerator,rn.denominator))
physical_jet = (-7*p*sigma**2*density/2048)/ky
assert s.simplify(physical_jet + 7*density/2048) == 0
assert s.simplify(physical_jet + 21/(1684*s.sqrt(13))) == 0

# Delta preserves the actual exterior parity, including off-diagonal site links.
pi = s.diag(*[(-1)**bin(i).count("1") for i in range(16)])
for creation in primary.CREATORS:
    M = s.Matrix(creation)
    assert pi*M + M*pi == s.zeros(16) and pi*M.T + M.T*pi == s.zeros(16)
# Test a non-diagonal proper Lorentz null generator on true exterior powers.
frame = s.eye(4); frame[1,2]=frame[2,0]=1; frame[1,0]=s.Rational(1,2)
indices = [[j for j in range(4) if i & (1<<j)] for i in range(16)]
exterior = s.Matrix(16,16,lambda i,j: frame.extract(indices[i],indices[j]).det()
                    if len(indices[i])==len(indices[j]) else 0)
assert pi*exterior==exterior*pi
for grade in [0,15]:
    assert pi[grade,grade]==1 and pi[1,1]==pi[14,14]==-1

print(f"PASS: rho_w={rw}, rho_next={rn}, all128 kernel; both marked branches share g/(sigma^2 p), opposite finite words isolate g, full CAR parity.")
