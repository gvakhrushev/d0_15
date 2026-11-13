#!/usr/bin/env python3
"""Check the actual 7fy archive on the stated LC4 polar section.

This checks the classical information identities, not the H.1 compiler,
the physical readout price, nor an identification with Book03 Info.
"""
from itertools import product
from math import log, sqrt


p = (sqrt(5) - 1) / 2
ell = -log(p)


def h(x):
    return -x * log(x) - (1 - x) * log(1 - x)


def archive(r, t):
    return (r, t, r, t, t, r)


def parsed(raw):
    return ''.join(str(bit) for bit, keep in zip(raw[:4], (1, 1, raw[4], raw[5])) if keep)


expected = {(0, 0): '00', (0, 1): '010', (1, 0): '100', (1, 1): '1111'}
assert {rt: parsed(archive(*rt)) for rt in product((0, 1), repeat=2)} == expected
assert len({archive(*rt) for rt in product((0, 1), repeat=2)}) == 4
assert abs(h(p*p) - (1+p*p)*ell) < 1e-14

checks = 0
for i in range(1001):
    q = p*p + (0.5-p*p)*i/1000
    probabilities = ((1-q)*p, (1-q)*p*p, q)
    entropy = -sum(x*log(x) for x in probabilities)
    mean_length = sum(x*n for x, n in zip(probabilities, (2, 3, 3)))
    coarse = h(q)
    extra = (1-q)*h(p*p)
    fine_derivative = log((1-q)/q)-h(p*p)
    assert abs(sum(probabilities)-1) < 1e-14
    assert abs(entropy-coarse-extra) < 1e-14
    assert abs(mean_length-(2+p*p+p*q)) < 1e-14
    assert abs(mean_length-entropy/ell-(1+2*q-coarse/ell)) < 1e-14
    assert fine_derivative <= -p*p*ell+1e-14
    checks += 5

print(f'PASS: {checks} numerical identities/bounds across 1001 collar points;')
print('PASS: all four physical archive maps and exact parser lookup;')
print(f'p={p:.12f}, h(p^2)={h(p*p):.12f}, fine slope upper bound={-p*p*ell:.12f}.')
print('Analytic proof, scope and unverified physical obligations: ROUND14_READER_LEDGER_RU.md')
