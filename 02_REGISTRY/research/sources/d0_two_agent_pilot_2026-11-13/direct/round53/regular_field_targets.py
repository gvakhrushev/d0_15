#!/usr/bin/env python3
"""Finite rational names in an open subset of the existing B21 field chart.

No Einstein predicate is used. All 2688 raw coordinates are independent.
The original fixed boundaries and reference banks are unchanged.
"""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
from functools import lru_cache
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round48'))
import two_bit_source_targets as old

COORD = old.loc.COORD
M = len(COORD)
RADIUS = F(1, 1 << 32)
SIGMA = F(1, 1 << 80)
assert M == 2688


@dataclass(frozen=True)
class FieldCentre:
    offsets: tuple = (F(0),)*M

    def __post_init__(self):
        if type(self.offsets) is not tuple or len(self.offsets) != M:
            raise ValueError('exactly 2688 centre offsets required')
        if any(type(v) not in (int, F) for v in self.offsets):
            raise ValueError('only exact rational names, no float or Boolean')
        values = tuple(F(v) for v in self.offsets)
        if any(abs(v) >= RADIUS for v in values):
            raise ValueError('centre is outside the declared open B21 subchart')
        object.__setattr__(self, 'offsets', values)

    def encode(self):
        return json.dumps([[v.numerator, v.denominator] for v in self.offsets],
                          separators=(',', ':')).encode('ascii')

    @classmethod
    def decode(cls, packet):
        rows = json.loads(packet)
        if (type(rows) is not list or len(rows) != M
                or any(type(r) is not list or len(r) != 2
                       or any(type(v) is not int for v in r) or r[1] <= 0 for r in rows)):
            raise ValueError('invalid finite field name')
        value = cls(tuple(F(*r) for r in rows))
        if value.encode() != packet:
            raise ValueError('canonical field name required')
        return value

    def selected(self, indices):
        return tuple(self.offsets[j] for j in indices)


def coframe_rows(bank):
    return old.coframe_templates()[bank]


def coframe_vector(field, row, digits, iv, constants):
    name, spec = old.coframe_spec(row, digits)
    v = old.coframe_vector(iv, constants, spec)
    indices = row['coordinates']
    assert len(indices) in (0, 4)
    if indices:
        assert row['bank'] in ('f', 'q')
        assert [COORD[j]['component'] for j in indices] == list(range(4))
        assert all(COORD[j]['kind'] == 'coframe'
                   and COORD[j]['site'] == row['site']
                   and COORD[j]['role'] == row['direction'] for j in indices)
        v = [iv.add(x, iv.rational(off.numerator, off.denominator))
             for x, off in zip(v, field.selected(indices))]
    return v, spec


def coframe_factors(field, row, digits, iv, constants):
    v, spec = coframe_vector(field, row, digits, iv, constants)
    f = old.cf.factors(iv, v, spec)
    # Emit all three fixed chart rotations. Zero-angle recognition is not
    # necessary for halting and no target-dependent loop count is hidden.
    for rotation in f['mode_rotations']:
        rotation['exact_identity'] = False
    return f


@lru_cache(None)
def material_rows(bank):
    assert bank in ('q', 'y+', 'y-')
    return tuple(old.material_catalogue()[bank])


def material_half_vector(field, bank, row, iv, constants):
    if bank == 'q':
        indices = row['SAM_indices'][::2]
        pattern = row['SAM_pattern']
        digits = [pattern[j]+2*pattern[j+1] for j in range(0, len(pattern), 2)]
        spec = {'kind': 'q', 'x0': row['site_coordinates'][0],
                'digits': digits if indices else None}
    else:
        indices = []
        spec = {'kind': 'y', 'sign': 1 if row['vector_id'] == 'y_positive' else -1}
    _, psi = old.material_half_vector(iv, constants, spec)
    if indices:
        assert len(indices) == 2
        assert [COORD[j]['grade'] for j in indices] == [0, 15]
        assert all(COORD[j]['kind'] == 'matter'
                   and COORD[j]['site'] == row['site_coordinates'] for j in indices)
        psi = [iv.add(x, iv.rational(off.numerator, off.denominator))
               for x, off in zip(psi, field.selected(indices))]
    R = iv.rational
    one = R(1)
    a = constants['sqrtp']
    slack = iv.sub(iv.sub(one, constants['p']),
                   iv.add(iv.pow(psi[0], 2), iv.pow(psi[1], 2)))
    assert slack[0] > iv.scale//3
    denominator = iv.sqrt(iv.mul(R(2), iv.add(one, a)))
    v = {1: iv.div(iv.add(one, a), denominator),
         14: iv.div(iv.sqrt(slack), denominator),
         0: iv.div(psi[0], denominator), 15: iv.div(psi[1], denominator)}
    return v, psi


def chart_bounds():
    # 3/8 < p² and 3/8 < 1-p² follow from 2<sqrt(5)<9/4.
    # |d-3p²|<3, d=0..3. Thus every centre plus CODE displacement
    # stays strictly inside the old asymmetric B21 cube.
    budget = RADIUS+3*SIGMA
    symmetric_inner = F(3, 8)*(F(1, 1 << 30))
    assert budget < symmetric_inner
    return {'centre_radius': RADIUS, 'CODE_increment_bound': 3*SIGMA,
            'maximum_total_coordinate_displacement': budget,
            'strict_old_cube_inner_radius': symmetric_inner,
            'old_cube_margin_lower': symmetric_inner-budget}
