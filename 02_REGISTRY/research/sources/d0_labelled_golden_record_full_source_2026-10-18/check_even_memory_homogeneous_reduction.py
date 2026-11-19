#!/usr/bin/env python3
"""Bounded exact homogeneous pure-even-memory source reduction.

Only pinned literal CAR definitions and the existing root receipt are read.
Two eight-dimensional C3 determinants prove the new link-amplitude rank;
no thermal/root suite, spatial Hessian or nonlinear spatial replay executes.
Default execution is read-only; --output explicitly saves the receipt.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import json
from math import isqrt
from pathlib import Path
import platform

import sympy as s
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HELPER = '02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py'
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
ROOT_RECEIPT = '02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json'
PINS = {
    HELPER: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    ROOT_RECEIPT: 'da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9',
}


def run(repo=ROOT):
    checks = []

    def check(name, condition):
        if not bool(condition):
            raise ArithmeticError('even_memory_homogeneous:' + name)
        checks.append(name)

    def eq(name, actual, expected):
        difference = actual - expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        check(name, all(s.expand(x).simplify() == 0 for x in entries))

    for path, digest in PINS.items():
        check('pin:' + path, hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest)
    nodes = [node for node in ast.parse((repo/HELPER).read_text()).body
             if isinstance(node, ast.FunctionDef) and node.name == '_creators']
    check('only_literal_creator_loader', len(nodes) == 1)
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
    creators, order = scope['_creators'](repo)
    check('actual_ACDB_order', order == (0, 2, 3, 1))

    eye = s.eye(16)
    vacuum, top = eye[:, 0], eye[:, 15]
    chi = (vacuum + top)/s.sqrt(2)
    eta = s.diag(1, -1, -1, -1)
    pairs = [(a, b) for a in range(4) for b in range(a+1, 4)]
    exterior_basis = []
    for mask in range(16):
        vector = vacuum
        for a in reversed(range(4)):
            if mask & (1 << a):
                vector = creators[a]*vector
        exterior_basis.append(vector)
    signed_basis = s.Matrix.hstack(*exterior_basis)
    eq('full16_exterior_basis_isometry', signed_basis.T*signed_basis, eye)
    eq('actual_even_cat_orientation', signed_basis*chi, chi)
    eq('cat_normalization', (chi.T*chi)[0], s.Integer(1))
    for a in range(4):
        for b in range(4):
            eq('cat_full_quadratic_covariance_%d%d' % (a, b),
               (chi.T*creators[a]*creators[b].T*chi)[0],
               s.Rational(1, 2) if a == b else s.Integer(0))
        for b in range(a+1, 4):
            eq('cat_pair_covariance_%d%d' % (a, b),
               (chi.T*creators[a]*creators[b]*chi)[0], s.Integer(0))
    generic_vector = s.Matrix(s.symbols('v0:4', real=True))
    generic_creation = sum((generic_vector[j]*creators[j] for j in range(4)), s.zeros(16))
    for a, b in pairs:
        omega = s.zeros(4)
        omega[a, b], omega[b, a] = 1, -eta[a, a]*eta[b, b]
        generator = sum((omega[i, j]*creators[i]*creators[j].T
                         for i in range(4) for j in range(4)), s.zeros(16))
        eq('actual_traceless_generator_fixes_cat_%d%d' % (a, b),
           generator*chi, s.zeros(16, 1))
        transformed = omega*generic_vector
        eq('native_generator_on_one_particle_%d%d' % (a, b),
           generator*generic_creation*vacuum,
           sum((transformed[j]*creators[j] for j in range(4)), s.zeros(16))*vacuum)

    # This is the Euclidean CAR Hodge star, with the actual top orientation.
    hodge = s.zeros(6)
    for column, (a, b) in enumerate(pairs):
        remaining = [j for j in range(4) if j not in (a, b)]
        hodge[pairs.index(tuple(remaining)), column] = s.LeviCivita(a, b, *remaining)
    eq('Euclidean_two_form_hodge_square', hodge*hodge, s.eye(6))
    wedge_basis = s.Matrix.hstack(*[creators[a]*creators[b]*vacuum for a, b in pairs])
    qr, qi = s.symbols('qr0:6', real=True), s.symbols('qi0:6', real=True)
    q = s.Matrix([a+s.I*b for a, b in zip(qr, qi)])
    raising = sum((q[j]*creators[a]*creators[b]
                   for j, (a, b) in enumerate(pairs)), s.zeros(16))
    eq('literal_CAR_cat_grade2_hodge_identity',
       wedge_basis.T*(raising+raising.conjugate().T)*chi,
       (q+hodge*s.conjugate(q))/s.sqrt(2))
    invisible = creators[0]*creators[1]-creators[2]*creators[3]
    invisible += invisible.T
    eq('negative_control_vacuum_columns_can_cancel_on_cat',
       invisible*chi, s.zeros(16, 1))
    check('negative_control_vacuum_alone_is_not_cat', invisible*vacuum != s.zeros(16, 1))

    root2 = s.sqrt(2)
    phase = (1+s.I)/root2
    zeta = phase-1
    m = s.Matrix(s.symbols('m0:6', real=True))
    n = s.Matrix(s.symbols('n0:6', real=True))
    bform = m+(root2-1)*n+hodge*n
    pplus, pminus = (s.eye(6)+hodge)/2, (s.eye(6)-hodge)/2
    target = ((root2-2)*pplus+s.I*root2*pminus)*bform
    eq('native_phase_hodge_reduction',
       zeta*m+zeta**2*n+hodge*s.conjugate(zeta*m+zeta**2*n), target)
    check('native_phase_reduction_is_invertible',
          s.simplify(((root2-2)*pplus+s.I*root2*pminus).det()) != 0)

    r = s.Symbol('r', real=True)
    vectors = [eta*s.Matrix([r if a == j else 1 for a in range(4)]) for j in range(4)]

    def wedge(left, right):
        return s.Matrix([left[a]*right[b]-left[b]*right[a] for a, b in pairs])

    columns = []
    for role in range(4):
        for a, b in pairs:
            omega = s.zeros(4)
            omega[a, b], omega[b, a] = 1, -eta[a, a]*eta[b, b]
            rows = []
            for j in range(4):
                mj = wedge(vectors[role], omega*vectors[j])
                nj = wedge(vectors[j], omega*vectors[j]) if j == role else s.zeros(6, 1)
                rows.extend(mj+(root2-1)*nj+hodge*nj)
            columns.append(s.Matrix(rows))
    link_map = s.Matrix.hstack(*columns)

    cycle = (0, 2, 3, 1)
    representation = s.zeros(24)
    for role in range(4):
        for j, (a, b) in enumerate(pairs):
            a, b = cycle[a], cycle[b]
            sign = 1
            if a > b:
                a, b, sign = b, a, -1
            representation[6*cycle[role]+pairs.index((a, b)), 6*role+j] = sign
    eq('simultaneous_spatial_cycle_order3', representation**3, s.eye(24))
    eq('actual_link_map_C3_equivariance', representation*link_map, link_map*representation)
    seen, representatives = set(), []
    for j in range(24):
        if j in seen:
            continue
        representatives.append(j)
        vector = s.eye(24)[:, j]
        for unused in range(3):
            seen.add(next(i for i in range(24) if vector[i]))
            vector = representation*vector
    check('eight_disjoint_complete_C3_orbits', len(representatives) == 8 and len(seen) == 24)
    root3 = (-1+s.sqrt(3)*s.I)/2

    def eigenbasis(value):
        return s.Matrix.hstack(*[
            s.eye(24)[:, j]+representation[:, j]/value
            +(representation**2)[:, j]/value**2 for j in representatives])

    bases = [eigenbasis(value) for value in (s.Integer(1), root3, s.conjugate(root3))]
    complete_basis = s.Matrix.hstack(*bases)
    eq('complete24_C3_basis', complete_basis.conjugate().T*complete_basis, 3*s.eye(24))
    for name, value, basis in zip(('trivial', 'complex', 'conjugate'),
                                  (s.Integer(1), root3, s.conjugate(root3)), bases):
        eq('C3_eigenbasis_'+name, representation*basis, value*basis)
        eq('C3_representative_coordinates_'+name, basis[representatives, :], s.eye(8))
    blocks = [(link_map*basis)[representatives, :] for basis in bases]
    eq('conjugate8_block_is_conjugate', blocks[2], s.conjugate(blocks[1]))

    # Rational enclosure of sqrt(2): coefficient bounds use no floating point.
    scale = 10**40
    lower_integer = isqrt(2*scale*scale)
    lower2, upper2 = s.Rational(lower_integer, scale), s.Rational(lower_integer+1, scale)
    check('rational_sqrt2_enclosure', lower2**2 < 2 < upper2**2)
    real_field = s.QQ.algebraic_field(root2)
    determinant_results = []
    for name, value, block in zip(('trivial', 'complex'), (s.Integer(1), root3), blocks[:2]):
        domain = s.QQ.algebraic_field(root2, value).poly_ring(r)
        determinant = DomainMatrix.from_Matrix(block).convert_to(domain).det()
        polynomial = s.Poly(domain.to_sympy(determinant), r, extension=[root2, value])
        degree, leading = polynomial.degree(), polynomial.LC()
        check(name+'_determinant_degree16', degree == 16)
        check(name+'_leading_coefficient_nonzero', leading != 0)
        bounds = []
        for j in range(degree):
            ratio = s.simplify(polynomial.nth(j)/leading)
            square = s.simplify(s.expand(ratio*s.conjugate(ratio)))
            square = real_field.to_sympy(real_field.from_sympy(square)).expand()
            coefficient = square.coeff(root2)
            constant = s.simplify(square-coefficient*root2)
            check(name+'_coefficient_norm_quadratic_%d' % j,
                  constant.is_Rational and coefficient.is_Rational)
            ceiling = constant+coefficient*(upper2 if coefficient >= 0 else lower2)
            check(name+'_coefficient_norm_enclosed_%d' % j, ceiling >= 0)
            bound = isqrt(int(ceiling.p//ceiling.q))+1
            check(name+'_strict_integer_norm_bound_%d' % j, bound*bound > ceiling)
            bounds.append(bound)
        tail = sum((s.Rational(bound, 30**(degree-j)) for j, bound in enumerate(bounds)), s.Integer(0))
        check(name+'_determinant_nonzero_all_r_at_least30', tail < 1)
        determinant_results.append({
            'block': name, 'degree': degree,
            'coefficients_low_to_high': [str(polynomial.nth(j)) for j in range(degree+1)],
            'coefficient_ratio_integer_bounds_low_to_high': bounds,
            'tail_upper_at_r30': str(tail),
        })

    inherited = json.loads((repo/ROOT_RECEIPT).read_text())['interval']
    dcenter, ocenter = map(s.Rational, inherited['root_center'])
    radius = s.Rational(inherited['root_radius'])
    dlow, ohigh = dcenter-radius, ocenter+radius
    check('owned_root_carrier_L8_full16_reference128',
          inherited['L'] == 8 and inherited['Fock_dimension'] == 16
          and inherited['purifying_reference_dimension'] == 128)
    check('owned_root_regular_positive_coframe', dlow > ohigh > 0)
    root_margin = 248*dlow-3612*ohigh
    check('whole_owned_root_box_implies_a_over_b_greater30', root_margin > 0)
    d, o = s.symbols('d o', real=True)
    eq('exact_root_ratio30_squared_equivalence',
       33**2*(d-o)-29**2*(d+3*o), 248*d-3612*o)

    a, b = s.symbols('a b', real=True)
    frame = (a-b)*s.eye(4)+b*s.ones(4)
    observer = s.Matrix([0, *s.symbols('nu1:4', real=True)])
    e0 = s.eye(4)[:, 0]
    variation = 2*frame*(e0*observer.T+observer*e0.T)*frame.T
    differences = s.Matrix([variation[j, j]-variation[0, 0] for j in range(1, 4)])
    jacobian = differences.jacobian(list(observer)[1:])
    eq('actual_observer_equal_diagonal_jacobian',
       jacobian, 4*b*(a-b)*(s.eye(3)-s.ones(3)))
    eq('actual_observer_jacobian_determinant', jacobian.det(), -128*b**3*(a-b)**3)
    check('eight_full16_active_column_chart_dimension255', 2*8*16-1 == 255)

    return {
        'status': 'PASS', 'check_count': len(checks), 'checks': checks,
        'retained_real_rank_at_owned_root': 27,
        'link_rank_from_grade2': 24, 'observer_rank_modulo_energy': 3,
        'ratio_domain_proved': 'a/b >= 30; the entire pinned actual root box has a/b > 30',
        'root_window': {'center_d_o': inherited['root_center'], 'radius': inherited['root_radius'],
                        'strict_248d_minus_3612o_lower_bound': str(root_margin),
                        'inherited_next_shell_gap_lower': inherited['next_shell_gap_lower'],
                        'gap_not_asserted_for_all_a_greater_b': True},
        'C3_orbit_representatives': representatives, 'determinant_blocks': determinant_results,
        'amplitude_chart': {'active_reference_columns': 8, 'full_CAR_dimension': 16,
                            'real_normalized_chart_dimension': 255, 'retained_reference_dimension': 128,
                            'only_total_Hilbert_Schmidt_normalization': True,
                            'per_momentum_weights_fixed': False,
                            'constructed_subfamily_not_full_amplitude_parameterization': True,
                            'other_reference_columns_removed_from_Euler_equations': False,
                            'rank_birth_directions_forbidden': False},
        'homogeneous_amplitude_IFT': 'rank premise verified; all unselected matter rows use the exact Delta P=epsilon P identity in the owner',
        'spatial_nonlinear_section_proved': False, 'physical_preparation_admission_proved': False,
        'Einstein_GR_proved': False, 'thermal_or_root_suite_replayed': False,
        'source_sha256': PINS, 'python': platform.python_version(), 'sympy': s.__version__,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2)+'\n'
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
