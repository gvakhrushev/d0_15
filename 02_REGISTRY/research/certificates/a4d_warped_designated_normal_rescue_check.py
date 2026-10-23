#!/usr/bin/env python3
"""Exact frozen inverse and physical metric-response coefficient for a warped line.

All arithmetic is over Q or Q(i). The polynomial matrix identity is checked
coefficientwise, not inferred from interpolation samples. Analytic variable-
coefficient rescue is proved in A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from a4d_designated_full_gap_check import (
    QI, GEN, PAIRS, SIG, SYM, EYE, flat_symbols, wedge, column, orient,
    mm, pairing)

I = np.eye(24, dtype=object)

def symbol(z,f):
 phase=list(map(QI.of,[1,z,1,1]));a=[[QI() for _ in range(24)] for _ in range(24)]
 weights=[f*f,f,f,f,f,1]
 for face,(r,s) in enumerate(PAIRS):
  u,v=[i for i in range(4) if i not in (r,s)]
  area=wedge(column(EYE,u),column(EYE,v))
  roles=(r,s,r,s)
  direct=(QI.of(1),phase[r],-phase[s],QI.of(-1))
  invers=(QI.of(1),1/phase[r],-1/phase[s],QI.of(-1))
  role=[[QI() for _ in range(4)] for _ in range(4)]
  for i,j in combinations(range(4),2):
   role[roles[i]][roles[j]]+=direct[i]*invers[j]/2
   role[roles[j]][roles[i]]-=invers[i]*direct[j]/2
  for i,xi in enumerate(GEN):
   for j,xj in enumerate(GEN):
    xy,yx=mm(xi,xj),mm(xj,xi)
    bracket=[[xy[k][l]-yx[k][l] for l in range(4)] for k in range(4)]
    val=weights[face]*orient(r,s)*pairing(area,bracket)
    for rr in range(4):
     for ss in range(4):a[6*rr+i][6*ss+j]+=role[rr][ss]*val
 return np.array(a,dtype=object).T

def inverse(a):
    n=len(a);b=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next(i for i in range(j,n) if b[i][j]);b[j],b[p]=b[p],b[j]
        v=b[j][j];b[j]=[x/v for x in b[j]]
        for i in range(n):
            if i!=j and b[i][j]:
                v=b[i][j];b[i]=[x-v*y for x,y in zip(b[i],b[j])]
    return np.array([r[n:] for r in b],dtype=object)

def interpolate(values):
 vals=values.copy();out=[np.zeros_like(values[0]) for _ in values];base=[F(1)]
 for k in range(len(values)):
  for j,t in enumerate(base):out[j]+=t*vals[0]
  vals=[vals[j+1]-vals[j] for j in range(len(vals)-1)]
  if not vals:break
  nxt=[F(0)]*(len(base)+1)
  for j,t in enumerate(base):nxt[j]-=t;nxt[j+1]+=t/F(k+1)
  base=nxt
 return out

def zcoeff(f):
 A=[symbol(z,f) for z in (1,-1,QI(0,1))]
 b0=(A[0]+A[1])/2;bp=(A[0]-b0+(A[2]-b0)/QI(0,1))/2;bm=A[0]-b0-bp
 return np.array([[[x.re for x in row] for row in b] for b in (bm,b0,bp)],dtype=object)


def multiply(left, right):
    out = np.zeros((len(left)+len(right)-1,
                    len(left[0])+len(right[0])-1, 24, 24), dtype=object)
    for i, row in enumerate(left):
        for j, a in enumerate(row):
            if not np.any(a):
                continue
            for k, other_row in enumerate(right):
                for l, b in enumerate(other_row):
                    if np.any(b):
                        out[i+k, j+l] += a@b
    return out


def sparse_ledger(matrix, z_radius):
    return [{'f_degree': i, 'z_degree': j-z_radius,
             'entries': [[r, c, str(block[r, c])] for r in range(24)
                         for c in range(24) if block[r, c]]}
            for i, row in enumerate(matrix) for j, block in enumerate(row)
            if np.any(block)]


def envelope(matrix, f_power, lower, upper, derivative=False):
    row = [F(0)]*24
    column_sum = [F(0)]*24
    for i, blocks in enumerate(matrix):
        degree = i-f_power
        if derivative:
            if degree == 0:
                continue
            multiplier = abs(degree)
            degree -= 1
        else:
            multiplier = 1
        scale = multiplier*max(lower**degree, upper**degree)
        for block in blocks:
            for r in range(24):
                for c in range(24):
                    bound = abs(block[r, c])*scale
                    row[r] += bound
                    column_sum[c] += bound
    return max(row+column_sum)


def polynomial_remainder(polynomial, divisor):
    result = {k: v for k, v in polynomial.items() if v}
    while result and max(result) >= max(divisor):
        shift = max(result)-max(divisor)
        leading = result[max(result)]/divisor[max(divisor)]
        for k, value in divisor.items():
            result[k+shift] = result.get(k+shift, F(0))-leading*value
        result = {k: v for k, v in result.items() if v}
    return result


def normal_einstein_column(q):
    """Half of the standard Einstein normal jet, as a ten-slot Gram covector.

    Only q_ab,11 is nonzero. Ric_ab = d_c Gamma^c_ab-d_b Gamma^c_ac
    at g=eta,dg=0. Off-diagonal Gram slots carry their factor of two.
    """
    trace = sum(SIG[c]*q[c, c] for c in range(4))
    ricci = np.zeros((4, 4), dtype=object)
    for a in range(4):
        for b in range(4):
            ricci[a, b] = F(1, 2)*(SIG[1]*(
                (a == 1)*q[1, b]+(b == 1)*q[a, 1]-q[a, b])
                -(a == 1)*(b == 1)*trace)
    scalar = sum(SIG[c]*ricci[c, c] for c in range(4))
    einstein = ricci.copy()
    for a in range(4):
        einstein[a, a] -= F(1, 2)*SIG[a]*scalar
    return np.array([F(1, 2)*(1 if a == b else 2)*SIG[a]*SIG[b]
                     *einstein[a, b] for a, b in SYM], dtype=object)


def check_mixed_phase_placement():
    """Differentiate the base-site areas, then assemble independent edge rows."""
    z = QI(0, 1)
    powers = [QI.of(1), z, QI.of(-1), -z]
    _, opposite = flat_symbols([1, 1/z, 1, 1])
    _, same = flat_symbols([1, z, 1, 1])
    wrong_placement_detected = False
    for m, (a, b) in enumerate(SYM):
        lift = [[F(0) for _ in range(4)] for _ in range(4)]
        lift[a][b] = F(SIG[a], 2)
        lift[b][a] = F(SIG[b], 2)
        force = np.zeros((4, 24), dtype=object)
        for r, s in PAIRS:
            u, v = [j for j in range(4) if j not in (r, s)]
            first = wedge(column(lift, u), column(EYE, v))
            second = wedge(column(EYE, u), column(lift, v))
            area = [x+y for x, y in zip(first, second)]
            for p in range(4):
                locations = [(p, r, 1), ((p+(r == 1)) % 4, s, 1),
                             ((p+(s == 1)) % 4, r, -1), (p, s, -1)]
                for x, role, sign in locations:
                    for g, generator in enumerate(GEN):
                        force[x, 6*role+g] += sign*powers[p].re*orient(r, s)*pairing(area, generator)
        for p in range(4):
            for j in range(24):
                assert force[p, j] == (powers[p]*opposite[m][j]).re
                wrong_placement_detected |= force[p, j] != (powers[p]*same[m][j]).re
    assert wrong_placement_detected


def response_control(H):
    # H evaluated at f=z=1.
    a0 = sum(block for blocks in H for block in blocks)
    _, c2 = flat_symbols([1, 2, 1, 1])
    derivative = np.array([[v.re for v in row] for row in c2], dtype=object)
    for z in (QI.of(-1), QI(0, 1), QI(F(3, 5), F(4, 5))):
        _, c = flat_symbols([1, z, 1, 1])
        assert all(c[i][j] == (z-1)*derivative[i, j]
                   for i in range(10) for j in range(24))
    response = derivative@inverse(a0)@derivative.T
    expected = np.zeros((10, 10), dtype=object)
    for j, (r, s) in enumerate(SYM):
        q = np.zeros((4, 4), dtype=object)
        q[r, s] = q[s, r] = 1
        expected[:, j] = normal_einstein_column(q)
    assert np.array_equal(response, expected)
    assert np.any(response)
    assert not np.array_equal(-response, expected)
    return response


def run_checks():
    # Every literal phase monomial here has z-degree -1,0,1 and f-degree
    # 0,1,2, from the six complementary area weights (f^2,f,f,f,f,1).
    b0, bm, bp = zcoeff(0), zcoeff(-1), zcoeff(1)
    H = np.array([b0, (bp-bm)/2, (bp+bm)/2-b0])
    by_f = []
    radius, f_power, interpolation_degree = 4, 2, 6
    for f in map(F, range(1, interpolation_degree+2)):
        blocks = sum(f**i*row for i, row in enumerate(H))
        values = []
        for z in map(F, range(1, 2*radius+2)):
            hz = sum(z**(j-1)*block for j, block in enumerate(blocks))
            denominator = 18-4*f*f+(2*f*f-1)*(z*z+1/(z*z))
            values.append(f**f_power*z**radius*denominator*inverse(hz))
        by_f.append(np.array(interpolate(values)))
    P = np.array(interpolate(by_f))
    assert not np.any(P[5:])
    P = P[:5]
    expected = np.zeros((7, 11, 24, 24), dtype=object)
    for f_degree, z_degree, value in [
        (2, 0, 18), (4, 0, -4), (2, 2, -1), (2, -2, -1),
        (4, 2, 2), (4, -2, 2)]:
        expected[f_degree, z_degree+5] = value*I
    assert np.array_equal(multiply(H, P), expected)
    assert np.array_equal(multiply(P, H), expected)
    print('PASS_TWO_SIDED_ALL_PARAMETER_LAURENT_INVERSE', flush=True)
    # Check reconstruction away from the interpolation values using the
    # direct face formula and exact Gaussian-rational physical characters.
    for f, z in [(F(26, 25), QI(F(3, 5), F(4, 5))),
                 (F(3, 7), QI(F(5, 13), F(12, 13)))]:
        reconstructed = np.zeros((24, 24), dtype=object)
        for i, row in enumerate(H):
            for j, block in enumerate(row):
                power = QI.of(1)
                if j == 0:
                    power = 1/z
                elif j == 2:
                    power = z
                reconstructed += block*(f**i*power)
        assert np.array_equal(symbol(z, f), reconstructed)
    at_one = np.sum(P, axis=0)
    flat_row = max(sum(abs(block[r, c]) for block in at_one for c in range(24))
                   for r in range(24))
    flat_column = max(sum(abs(block[r, c]) for block in at_one for r in range(24))
                      for c in range(24))
    assert flat_row == flat_column == 70
    lower, upper = F(1), F(26, 25)
    numerator = envelope(P, 2, lower, upper)
    alpha = 18-4*upper**2
    beta = max(abs(2*lower**2-1), abs(2*upper**2-1))
    gap = alpha-2*beta
    assert gap > 0
    kernel = numerator/gap
    moment = numerator*(4/gap+4*beta/gap**2)
    derivative = envelope(H, 0, lower, upper, derivative=True)
    assert numerator == F(63406, 625)
    assert kernel == F(31703, 3546) and kernel < 9
    assert moment == F(247885757, 6287058) and moment < 40
    assert derivative == F(129, 25)
    assert 40*derivative < 207
    assert 288*upper < 300
    assert 6912*upper**2 < 8192
    # The compact f range matters: at f=2 the denominator has physical
    # zeros. HP=f^2 D I and this nonzero remainder exhibit a kernel there.
    poly = {}
    for i, row in enumerate(P):
        for j, block in enumerate(row):
            poly[j] = poly.get(j, F(0))+2**i*block[1, 9]
    remainder = polynomial_remainder(poly, {0: F(7), 2: F(2), 4: F(7)})
    assert remainder == {3: F(40, 7)}
    print('PASS_KERNEL_MOMENT_BOUNDS_AND_LARGE_WARP_HOSTILE_CONTROL', flush=True)
    check_mixed_phase_placement()
    response = response_control(H)
    print('PASS_PHYSICAL_HALF_EINSTEIN_NORMAL_JET_COEFFICIENT', flush=True)
    return {
        'arithmetic': 'exact Q and Q(i), NumPy object arrays',
        'sector': 'all 24 link coordinates, lambda=(1,z,1,1)',
        'solder': 'diag(1,1,f,f)',
        'inverse_identity': 'H_f(z) P_f(z) = P_f(z) H_f(z) = f^2 D_f(z) I_24',
        'denominator': 'D_f(z)=18-4*f^2+(2*f^2-1)*(z^2+z^-2)',
        'H': sparse_ledger(H, 1), 'P': sparse_ledger(P, 4),
        'P_f_degree': 4, 'P_z_radius': 4,
        'eta_inverse_bound_all_lp': '35/6',
        'warp_interval': ['1', '26/25'],
        'numerator_envelope': str(numerator),
        'denominator_gap': str(gap),
        'uniform_inverse_kernel_bound': str(kernel),
        'uniform_inverse_first_moment_bound': str(moment),
        'frozen_symbol_f_derivative_envelope': str(derivative),
        'variable_coefficient_commutator_constant_upper': 207,
        'coefficient_shift_constant_upper': 300,
        'link_log_jacobian_lipschitz_upper': 8192,
        'curved_left_inverse_defect_bound': 'h*(2907*||f_prime||_infinity+73728*M_A)',
        'curved_inverse_bound_if_defect_at_most_half': 18,
        'nonlinear_rescue_constant_for_small_residual': 36,
        'large_warp_hostile_f': '2',
        'large_warp_unit_root_polynomial': '7*z^4+2*z^2+7',
        'large_warp_P19_remainder_after_z4': '40*z^3/7',
        'normal_response_matrix': [[str(x) for x in row] for row in response],
        'normal_response_convention': 'r=G_standard[J]/2=-K_Schur[J]',
        'independent_base_area_mixed_phase_check': True,
        'same_phase_hostile_control_rejected': True,
        'verdict': 'WARPED_DESIGNATED_SECTOR_UNIFORM_NORMAL_RESCUE_CERTIFIED',
        'nonclaims': ['no transverse-frequency inverse or branch classification',
                      'no imposed joint metric-source equation',
                      'no all-sheet microstructure response terminal']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expect', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run_checks()
    if args.expect:
        assert json.loads(args.expect.read_text()) == report
        print('PASS_PINNED_LEDGER')
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('RESULT: exact frozen inverse, uniform curved-sector rescue and fixed physical normalization.')
