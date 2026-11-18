#!/usr/bin/env python3
"""Finite native coframe/CAR emitters for every admitted rational centre.

Uses certified short uniform Golden grids, not frozen angle tables or a
floating target guess. SourceI remains in this component profile; global
G/CX replacement and the new whole paid clock are separate obligations.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import gcd
from itertools import product
from collections import Counter
import hashlib
import json
import sys
import regular_field_targets as t

P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round48'))
import two_bit_local_native as local
import source_angle_certifier as arithmetic
sys.path.insert(0, str(D/'round41'))
import sam_only_compiler as compiler
nb = local.nb


@lru_cache(None)
def context(bits):
    iv = arithmetic.Dyadic(bits)
    return iv, t.old.cf.constants(iv), compiler.e.Dyadic(bits)


class UniformAngles:
    def __init__(self, controls):
        assert controls in (15, 24)
        self.controls = controls
        self.path = t.old.loc.B/'round93'/f'SHORT_GRID_K{controls}_E3460.json'
        cert = json.loads(self.path.read_text())
        source = t.old.loc.B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json'
        raw = source.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == cert['original_grid_sha256']
        original = json.loads(raw)
        self.q = int(cert['denominator_hex'], 16)
        self.pn = int(cert['numerator_hex'], 16)
        precision = cert['precision_bits']
        lo, hi = [int(x, 16) << controls for x in original['gamma_interval_hex']]
        error = max(abs(self.q*lo-self.pn*(1 << precision)),
                    abs(self.q*hi-self.pn*(1 << precision)))
        assert cert['walsh_common_controls'] == controls
        assert error == int(cert['error_numerator_hex'], 16)
        assert gcd(self.pn, self.q) == 1 and self.q*error < 1 << precision
        assert 16*(1 << 3460) < self.q
        self.inverse = pow(self.pn, -1, self.q)

    def at_precision(self, cosine, sine, bits):
        iv, constants, ctx = context(bits)
        scale = ctx.S
        c = (max(-scale, int(cosine[0])), min(scale, int(cosine[1])))
        s = (max(-scale, int(sine[0])), min(scale, int(sine[1])))
        low = lambda x: 0 if x[0] <= 0 <= x[1] else min(abs(x[0]), abs(x[1]))
        use_cosine = low(c) >= low(s)
        major, minor = (c, s) if use_cosine else (s, c)
        if low(major)*10 <= 6*scale:
            raise compiler.e.NeedPrecision('unit-circle component not yet enclosed away from zero')
        negative = major[1] < 0
        if negative:
            major, minor = ctx.neg(major), ctx.neg(minor)
        ratio = ctx.div(minor, major)
        if not -2*scale < ratio[0] <= ratio[1] < 2*scale:
            raise compiler.e.NeedPrecision('dominant component ratio unresolved')
        half = ctx.div(ratio, ctx.add(ctx.rat(1),
                       ctx.sqrt(ctx.add(ctx.rat(1), ctx.mul(ratio, ratio)))))
        angle = (2*compiler.atan_signed(ctx, half[0])[0],
                 2*compiler.atan_signed(ctx, half[1])[1])
        pi = tuple(int(x) for x in constants['pi'])
        halfpi = (pi[0]//2, -((-pi[1])//2))
        if use_cosine:
            if negative:
                angle = ctx.add(pi, angle)
        else:
            angle = ctx.add(ctx.neg(halfpi) if negative else halfpi, ctx.neg(angle))
        turn = ctx.div(angle, (2*pi[0], 2*pi[1]))
        if 2*self.q*(turn[1]-turn[0]) > scale:
            raise compiler.e.NeedPrecision('target interval too wide for uniform grid')
        cell = (self.q*(turn[0]+turn[1])+scale)//(2*scale)
        k = int((cell*self.inverse) % self.q) or self.q
        return {'k': str(k), 'native_exponent_multiplier': 1 << self.controls,
                'certified_error_bits': 3460, 'working_precision': bits}

    def select(self, target_factory, initial_bits=4096):
        """Select every angle in a finite family; no exact-zero/tie oracle."""
        bits = initial_bits
        while True:
            iv, constants, _ = context(bits)
            try:
                targets, metadata = target_factory(iv, constants)
                records = {key: self.at_precision(c, s, bits) for key, c, s in targets}
                return records, metadata
            except compiler.e.NeedPrecision:
                bits *= 2


class Components:
    def __init__(self, field):
        if not isinstance(field, t.FieldCentre):
            raise TypeError('validated finite field centre required')
        self.field = field
        self.coframe_angles = UniformAngles(24)
        self.material_angles = UniformAngles(15)

    @lru_cache(None)
    def controlled_x(self):
        records, _ = self.coframe_angles.select(
            lambda iv, c: ([('X', iv.rational(0), iv.rational(1))], None))
        # The same doubled angle supplies the controlled pi phase.
        # Total X error is <3*2^-3460, keeping its arbitrary aux all-columns.
        return records['X']

    def coframe_library(self, row, digits):
        def targets(iv, c):
            factors = t.coframe_factors(self.field, row, digits, iv, c)
            return list(t.old.cf.native_angle_targets(iv, factors)), factors
        angles, factors = self.coframe_angles.select(targets)
        refs = [{'factor': list(key), 'angle_id': str(key)} for key in angles]
        return {'families': {'current_sector': {
                    'mode_rotations': [{'mode': r['mode'], 'exact_identity': False}
                                       for r in factors['mode_rotations']],
                    'angle_bindings': refs}},
                'angles': {**{str(key): value for key, value in angles.items()},
                           'X': self.controlled_x()},
                'controlled_X_power': {'rotation_angle_id': 'X'}}

    def coframe_units(self, row, digits, lay=None, depth=0):
        lay = local.coframe_layout() if lay is None else lay
        bound = {'address': row['address'], 'family_id': 'current_sector',
                 'SAM_indices': t.old.code_indices(row['coordinates']),
                 'SAM_pattern': t.old.code_pattern(digits)}
        return local.coframe_units(bound, self.coframe_library(row, digits), lay,
                                   controlled=True, depth=depth)

    def coframe_blocks(self, bank, lay=None, depth=0):
        assert type(depth) is int and depth >= 0
        lay = local.coframe_layout() if lay is None else lay
        rows = t.coframe_rows(bank)
        for row in reversed(rows) if depth % 2 else rows:
            assignments = list(product(range(4), repeat=len(row['coordinates'])))
            for digits in reversed(assignments) if depth % 2 else assignments:
                for bound, inverse_depth in self.coframe_units(row, digits, lay, depth):
                    yield from local.cf.unit_blocks(bound, inverse_depth, lay)

    def material_library(self, bank, row):
        def targets(iv, c):
            vector, _ = t.material_half_vector(self.field, bank, row, iv, c)
            rotations = t.old.mat.rotations(iv, vector)
            targets = []
            for rotation in rotations:
                sine = rotation['sin']
                if local.prep.plane_geometry(rotation['other'])['orientation'] == -1:
                    sine = iv.neg(sine)
                targets.append((rotation['other'], rotation['cos'], sine))
            return targets, rotations
        angles, rotations = self.material_angles.select(targets)
        return {'rotations': [{'other': r['other'], 'angle_id': str(r['other'])}
                              for r in rotations],
                'angles': {str(key): value for key, value in angles.items()}}

    def material_units(self, bank, row, lay=None, depth=0):
        lay = local.material_layout() if lay is None else lay
        lib = self.material_library(bank, row)
        rotations = lib['rotations']
        order = reversed(rotations) if depth % 2 else rotations
        return [(local.bind_material(row, rotation, lay, lib['angles']), depth)
                for rotation in order]

    def material_blocks(self, bank, lay=None, depth=0):
        assert type(depth) is int and depth >= 0
        lay = local.material_layout() if lay is None else lay
        rows = t.material_rows(bank)
        for row in reversed(rows) if depth % 2 else rows:
            for bound, inverse_depth in self.material_units(bank, row, lay, depth):
                yield from local.cf.unit_blocks(bound, inverse_depth, lay)


def componentwise_upper():
    """Uniform bounds, not claims that an unpadded word has this length."""
    q24, q15 = UniformAngles(24).q, UniformAngles(15).q
    pair24 = Counter(G_port=(1 << 25)*q24, G_other=(1 << 25)*q24,
                     CX=29*(1 << 25)+8, SourceI=1 << 26)
    # In a forward coframe sector some units are already literal inverses.
    per_coframe = pair24+local.prep.raw_inverse_counts(pair24)
    per_coframe = Counter({k: 27*v for k, v in per_coframe.items()})
    pair15 = Counter(G_port=(1 << 15)*q15, G_other=(1 << 15)*q15,
                     CX=18*(1 << 15)+8, SourceI=1 << 16)
    per_material = Counter({k: 3*v for k, v in pair15.items()})
    result = {'coframe_per_sector': per_coframe, 'material_per_sector': per_material,
              'coframe': {}, 'material': {}}
    for bank in t.old.loc.BANKS:
        count = sum(4**len(r['coordinates']) for r in t.coframe_rows(bank))
        forward = Counter({k: count*v for k, v in per_coframe.items()})
        result['coframe'][bank] = {'sectors': count, 'forward': forward,
                                  'literal_inverse': local.prep.raw_inverse_counts(forward)}
    for bank in ('q', 'y+', 'y-'):
        count = len(t.material_rows(bank))
        forward = Counter({k: count*v for k, v in per_material.items()})
        result['material'][bank] = {'sectors': count, 'forward': forward,
                                   'literal_inverse': local.prep.raw_inverse_counts(forward)}
    return result


def build_plan():
    upper = componentwise_upper()
    def encode(value):
        if isinstance(value, Counter):
            return {key: hex(int(v)) for key, v in value.items()}
        if isinstance(value, dict):
            return {key: encode(v) for key, v in value.items()}
        if isinstance(value, F):
            return {'numerator': value.numerator, 'denominator': value.denominator}
        return value
    paths = [Path(__file__), P/'regular_field_targets.py',
             D/'round48/two_bit_source_targets.py', D/'round48/two_bit_local_native.py',
             D/'round48/source_angle_certifier.py', D/'round20/coframe_targets.py',
             D/'round20/coframe_native.py', D/'round18/material_targets.py',
             D/'round18/material_preparation.py', D/'round41/sam_only_compiler.py',
             t.old.loc.COORD_PATH, t.old.loc.ADDR_PATH,
             t.old.loc.B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
             t.old.loc.B/'round93/SHORT_GRID_K15_E3460.json',
             t.old.loc.B/'round93/SHORT_GRID_K24_E3460.json',
             compiler.CERT]
    return {'status': 'PARAMETERIZED_COFRAME_AND_CAR_NATIVE_COMPONENTS_ON_OPEN_B21_SUBCHART',
            'independent_exact_rational_centre_coordinates': t.M,
            'centre_open_radius': '2^-32', 'CODE_step': '2^-80',
            'chart_bounds': encode(t.chart_bounds()),
            'references_and_boundary_coordinates_fixed': True,
            'zero_and_pivot_equality_oracle_used': False,
            'coframe_rotations_always_three_plus_base_and_controlled_X': True,
            'CAR_half_vector_rotations_always_three': True,
            'native_angle_global_operator_error_lt': '2^-3460',
            'controlled_X_operator_error_lt': '3*2^-3460',
            'coframe_full_SELECT_uniform_operator_error_lt': '2^-3455',
            'CAR_half_vector_preparation_uniform_operator_error_lt': '2^-3458',
            'error_is_max_over_disjoint_address_CODE_sectors_not_sum': True,
            'profiles_use': ['G', 'CX', 'SourceI'],
            'literal_integer_inverse_depth_preserved': True,
            'all_source_columns_scope': 'original coframe Julia full32 / CAR preparation full16 maps with original controls, aux and protected spectators; later SOURCE-private fibre unchanged',
            'uniform_componentwise_inventory_upper': encode(upper),
            'full_SOURCE_G_CX_replacement_and_paid_clock_rebound': False,
            'proper_link_component_integrated': False,
            'field_name_approximation_inherited_bounds': {
                'sup_coordinate_error_eta_full_SOURCE_value_error_lt': '2^17*eta',
                'sup_coordinate_error_eta_full_SOURCE_first_derivative_error_lt': '2^28*eta',
                'scope': 'ideal B91 full SOURCE on same convex B21 chart; not derivative of discrete compiler'},
            'full_physical_cost_info_or_free_field_source_proved': False,
            'production_words_executed': False,
            'physical_C_closed': False, 'GR_closed': False,
            'source_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}}


if __name__ == '__main__':
    plan = build_plan()
    (P/'REGULAR_SOURCE_COMPONENT_PLAN.json').write_text(json.dumps(plan, indent=2)+'\n')
    print(plan['status'])
