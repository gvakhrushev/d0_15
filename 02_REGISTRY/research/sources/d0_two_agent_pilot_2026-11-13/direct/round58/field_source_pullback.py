#!/usr/bin/env python3
"""Exact readout of the A57 plane interpolant on the owned MG2 field lift.

The finite sums are mathematical linear readouts, not a free physical
arithmetic reader or new native control word. Production CODE order is
all low bits, then all high bits. No physical norm is assigned here.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round47'))
import full_vector_controls as mg
sys.path.insert(0, str(D/'round57'))
import full_plane_family as family

M = 2688


def checked_axis(axis, coordinates):
    if not (type(coordinates) is int and coordinates > 0
            and type(axis) is int and 0 <= axis < coordinates):
        raise ValueError('integer coordinate axis required')


def embed_spectator(spectator, axis, coordinates=M):
    """Insert zero bits at axis and coordinates+axis in A49 sam order."""
    checked_axis(axis, coordinates)
    if not (type(spectator) is int and 0 <= spectator < 1 << (2*coordinates-2)):
        raise ValueError('complete spectator index required')
    low = spectator & ((1 << axis)-1)
    middle_bits = coordinates-1
    middle = (spectator >> axis) & ((1 << middle_bits)-1)
    high = spectator >> (axis+middle_bits)
    return low | (middle << (axis+1)) | (high << (coordinates+axis+1))


def local_index(base, digit, axis, coordinates=M):
    checked_axis(axis, coordinates)
    if not (type(base) is int and 0 <= base < 1 << (2*coordinates)
            and not (base & ((1 << axis) | (1 << (coordinates+axis))))
            and type(digit) is int and 0 <= digit < 4):
        raise ValueError('zero-bit base and two-bit digit required')
    return base | ((digit & 1) << axis) | ((digit >> 1) << (coordinates+axis))


@dataclass(frozen=True)
class PlaneTerm:
    pair: tuple
    coefficient: object


def plane_terms(axis, coordinates=M):
    """All 6*2^(2m-2) terms of X_axis, without clean-spectator assumption."""
    checked_axis(axis, coordinates)
    _, _, weights = mg.mg2()
    for spectator in range(1 << (2*coordinates-2)):
        base = embed_spectator(spectator, axis, coordinates)
        for (i, j), weight in weights.items():
            a = local_index(base, i, axis, coordinates)
            b = local_index(base, j, axis, coordinates)
            assert a < b
            yield PlaneTerm((a, b), weight)


def signed_requests(field, axis):
    """Lazy pairs of existing A57 Pf requests; coefficients multiply rows."""
    if type(field) is not family.FieldCentre:
        raise TypeError('validated field centre required')
    for term in plane_terms(axis):
        yield (term.coefficient,
               family.Request(field, family.PlaneLabel('Pf', 1, term.pair)),
               family.Request(field, family.PlaneLabel('Pf', -1, term.pair)))


def bounded_raw_row(plane_value, axis, coordinates=M, *, max_terms=65536):
    """Exact diagnostic evaluation; rejects a sum exceeding declared work.

    plane_value(a,b) supplies a Q4/rational test covector only. General
    H+J price rows need not belong to Q4; they are NOT evaluated by this
    diagnostic. The signed_requests stream and mathematical sum specify
    those rows, without supplying or paying an arithmetic reader.
    """
    checked_axis(axis, coordinates)
    count = 6*(1 << (2*coordinates-2))
    if type(max_terms) is not int or not 0 <= count <= max_terms:
        raise ValueError('complete finite sum exceeds explicit evaluation budget')
    total = mg.e.Q4()
    for term in plane_terms(axis, coordinates):
        value = plane_value(*term.pair)
        if type(value) not in (int, F, mg.e.Q4):
            raise TypeError('Q4/rational diagnostic covector required, not a general price')
        total += term.coefficient*value
    return total


def pullback(raw_rows, iota):
    """Transpose application to explicit rows, any exact scalar field.

    iota has raw-coordinate rows and physical-variation columns. This is
    forward pullback only: a holonomy map with kernel is allowed, and no
    inverse or completeness of the physical variation domain is inferred.
    """
    if not raw_rows or len(raw_rows) != len(iota) or not iota:
        raise ValueError('matching nonempty raw rows and derivative required')
    n = len(iota[0])
    if not n or any(len(row) != n for row in iota):
        raise ValueError('rectangular derivative required')
    return [sum((raw_rows[j]*iota[j][k] for j in range(len(raw_rows))), 0)
            for k in range(n)]


def bound_chart_point(field, precision_bits=128):
    """Exact outward coframe names and rational theta at this A53 centre.

    Uses the owning A53/A48/A20 formula, not the rounded B21 centre export.
    Corner sampling digits are deliberately absent from the centre name.
    The returned integer endpoints have common denominator 2^precision_bits.
    """
    if type(field) is not family.FieldCentre:
        raise TypeError('validated field centre required')
    if type(precision_bits) is not int or precision_bits < 64:
        raise ValueError('at least 64 bits of outward precision required')
    target = family.prior.source.t
    iv = target.old.Dyadic(precision_bits)
    constants = target.old.cf.constants(iv)
    points = {}
    for row in target.coframe_rows('f'):
        indices = row['coordinates']
        if not indices:
            continue
        site = tuple(row['site'])
        point = points.setdefault(site, {'site': site,
            'u_intervals': [[None]*4 for _ in range(4)],
            'theta': [[None]*6 for _ in range(4)]})
        _, spec = target.old.coframe_spec(row, [0]*4)
        spec['digits'] = None
        column = target.old.coframe_vector(iv, constants, spec)
        for a, (value, index) in enumerate(zip(column, indices)):
            offset = field.offsets[index]
            point['u_intervals'][a][row['direction']] = iv.add(value, iv.rational(offset.numerator,offset.denominator))
    pairs = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    for index, coordinate in enumerate(target.COORD):
        if coordinate['kind'] == 'proper_link':
            points[tuple(coordinate['site'])]['theta'][coordinate['role']][pairs.index(tuple(coordinate['generator']))] = field.offsets[index]
    ordered = [points[site] for site in sorted(points)]
    assert len(ordered) == 64
    assert all(v is not None for pt in ordered for row in pt['u_intervals']+pt['theta'] for v in row)
    return {'field_sha256': sha256(field.encode()).hexdigest(),
            'precision_bits': precision_bits, 'sites': ordered,
            'physical_descriptor_admission_inferred': False}


def norm_budget(alpha_upper, raw_error_upper=F(1, 1 << 34)):
    """Conditional original-Vh error; alpha is evidence supplied by caller."""
    if any(type(x) is not F or x < 0 for x in (alpha_upper, raw_error_upper)):
        raise ValueError('nonnegative rational upper bounds required')
    return alpha_upper*raw_error_upper


def plan():
    return {
        'status': 'EXPLICIT_MG2_PLANE_READOUT_AND_FORWARD_FIELD_PULLBACK',
        'raw_coordinates': M, 'CODE_bits': 2*M,
        'CODE_pair_positions': '(j,2688+j), all-low then all-high',
        'raw_row_formula': 'sum_s sum_i<k lambda_ik fhat_Pf(E_embed(s,i),embed(s,k))',
        'plane_rows_per_raw_coordinate': '6*2^5374',
        'signed_native_requests_per_raw_coordinate': '12*2^5374',
        'all_2688_raw_rows_signed_requests': '32256*2^5374',
        'lift': 'Rraw(v)=(sum_j v_j X_j,0,0,0)',
        'lift_isometry': '||Rraw(v)||raw=||v||2 since Lraw Rraw=I and sqrt(2688)<52',
        'physical_source': 'fhat_physical=fhat Rraw iota',
        'point_binding': 'A53 outward u centre and exact rational theta; fixed PF/collar; no corner digits or rounded B21 centre substituted',
        'original_norm_error': '< alpha_h*2^-34, alpha_h=||iota||_(Vh->l2)',
        'physical_iota_inverse_required_for_forward_pullback': False,
        'physical_norm_numeric_normalization_supplied': False,
        'production_sum_or_physical_reader_executed': False,
        'finite_MG2_word_price_equals_plane_interpolant_claimed': False,
        'new_action_Info_weight_selector_or_geometry_root': False,
        'physical_C_closed': False, 'GR_closed': False}
