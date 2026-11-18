#!/usr/bin/env python3
"""Independent exact special-family check of B103's original Julia32 target.

A pure rotation in adjacent Fock modes 2,3 has exterior matrix known
directly and both Julia defects exactly 3I/4. No SVD or B103 determinant
formula is used to construct this comparator.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial, isqrt
from hashlib import sha256
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
B = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round103')
spec = importlib.util.spec_from_file_location('root_b103_link', B/'regular_link_julia.py')
link = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = link
spec.loader.exec_module(link)


def trig(t):
    # Alternating Taylor series; |t|<1, first omitted term bounds the tail.
    sine = sum((-1)**k*t**(2*k+1)/factorial(2*k+1) for k in range(9))
    cosine = sum((-1)**k*t**(2*k)/factorial(2*k) for k in range(9))
    es = abs(t**19/F(factorial(19)))
    ec = abs(t**18/F(factorial(18)))
    return (sine-es, sine+es), (cosine-ec, cosine+ec)


def reference(t):
    zero = (F(0), F(0))
    one = (F(1), F(1))
    sine, cosine = trig(t)
    exterior = [[zero for _ in range(16)] for _ in range(16)]
    for mask in range(16):
        n2, n3 = bool(mask & 4), bool(mask & 8)
        if n2 == n3:
            exterior[mask][mask] = one
        else:
            exterior[mask][mask] = cosine
            exterior[mask ^ 12][mask] = sine if n2 else (-sine[1], -sine[0])
    C = [[(a/2, b/2) for a, b in row] for row in exterior]
    bits = 512
    root = isqrt(3*(1 << (2*bits)))
    d = (F(root, 1 << (bits+1)), F(root+1, 1 << (bits+1)))
    result = [[zero for _ in range(32)] for _ in range(32)]
    for i in range(16):
        for j in range(16):
            result[i][j] = C[i][j]
            result[16+i][16+j] = (-C[j][i][1], -C[j][i][0])
        result[i][16+i] = result[16+i][i] = d
    return result


def main():
    cases = []
    for t in (F(0), F(1, 1 << 34), -F(1, 1 << 33)):
        offsets = (F(0),)*5+(t,)
        iv, J, _ = link.target_intervals(offsets, None, None, 240, 160)
        expected = reference(t)
        radius = F(0)
        for i in range(32):
            for j in range(32):
                a, b = expected[i][j]
                lo, hi = (F(int(v), int(iv.S)) for v in J[i][j])
                assert max(a, lo) <= min(b, hi), (t, i, j, 'independent Julia mismatch')
                radius = max(radius, abs((a+b-lo-hi)/2))
        assert 32*radius < F(1, 1 << 154)
        cases.append({'offset': str(t), 'all_matrix_entries_checked': 1024,
                      'direct_Fock_rotation_and_exact_Julia_defects': True})
    # Explicit numerical margin used in the analytic QR termination proof.
    q = 16
    delta = F(1, 1 << (q+15))
    assert (2*delta+delta*delta)/(1-delta) < 3*delta
    assert 96*delta < F(1, 1 << q)
    out = {'status': 'PASS_ROOT_INDEPENDENT_ADJACENT_FOCK_ROTATION_AND_JULIA_SIGN_CHECK',
           'cases': cases,
           'QR_fixed_Newton_floor_margin_verified': True,
           'general_family_proof_is_not_replaced_by_these_special_cases': True,
           'native_whole_SOURCE_or_price_proved': False,
           'physical_C_closed': False, 'GR_closed': False,
           'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest() for f in
                             [Path(__file__), B/'regular_link_julia.py']}}
    (P/'ROOT_B103_SPATIAL_ROTATION_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(out['status'])


if __name__ == '__main__':
    main()
