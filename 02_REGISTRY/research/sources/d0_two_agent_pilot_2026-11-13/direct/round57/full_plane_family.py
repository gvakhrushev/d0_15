#!/usr/bin/env python3
"""Four independent native CODE-plane families on a new common paid clock.

The source and its actual fixed post are inherited per field. A new
high-precision CODE-only plane compiler changes control length and K.
The resulting full covector is the linear interpolant of plane contrasts,
not the price of a jointly compiled arbitrary real skew operator.
"""
from pathlib import Path
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from hashlib import sha256
from functools import lru_cache
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round55'))
import regular_comparison_task as prior
sys.path.insert(0, str(D/'round56'))
import complete_code_source as analytic
O = prior.source.s.old.B
sys.path.insert(0, str(O/'round112'))
import plane_grid_32768 as grid

FieldCentre = prior.FieldCentre
LegacyLabel = prior.Label
paid = prior.paid.paid
CODE_BITS = 5376
STEP_BITS = 6000
PLANE_BITS = 32768
ARMS = ('Pf', 'Qf', 'Qb', 'Pb')


@dataclass(frozen=True)
class PlaneLabel:
    arm: str
    sign: int
    plane: tuple

    def __post_init__(self):
        if not (self.arm in ARMS and type(self.sign) is int and self.sign in (-1, 1)
                and type(self.plane) is tuple and len(self.plane) == 2
                and all(type(x) is int for x in self.plane)
                and 0 <= self.plane[0] < self.plane[1] < (1 << CODE_BITS)):
            raise ValueError('finite signed CODE-plane label required')


@dataclass(frozen=True)
class Request:
    field: FieldCentre
    label: object = LegacyLabel()

    def __post_init__(self):
        if not isinstance(self.field, FieldCentre) or type(self.label) not in (LegacyLabel, PlaneLabel):
            raise TypeError('validated field and declared label required')

    def encode(self):
        return json.dumps({'field': json.loads(self.field.encode()),
                           'family': 'plane' if type(self.label) is PlaneLabel else 'A55',
                           'label': asdict(self.label)},
                          sort_keys=True, separators=(',', ':')).encode('ascii')

    @classmethod
    def decode(cls, packet):
        if type(packet) is not bytes:
            raise TypeError('canonical bytes required')
        obj = json.loads(packet)
        if type(obj) is not dict or set(obj) != {'field', 'family', 'label'}:
            raise ValueError('exact request schema required')
        field = FieldCentre.decode(json.dumps(obj['field'], separators=(',', ':')).encode('ascii'))
        if obj['family'] == 'A55':
            label = prior.original.decode(json.dumps(obj['label'], sort_keys=True,
                                          separators=(',', ':')).encode('ascii'))
        elif obj['family'] == 'plane':
            value = obj['label']
            if (type(value) is not dict or set(value) != {'arm', 'sign', 'plane'}
                    or type(value['plane']) is not list):
                raise ValueError('exact plane label required')
            label = PlaneLabel(value['arm'], value['sign'], tuple(value['plane']))
        else:
            raise ValueError('unknown comparison family')
        result = cls(field, label)
        if result.encode() != packet:
            raise ValueError('noncanonical request')
        return result


def configuration(base):
    """Actual padded lengths; old SOURCE/post words keep their own precision."""
    c = dict(base)
    _, q, _ = grid.uniform_grid()
    macro = grid.Macros()
    plane_upper = paid.old.plane_upper(len(c['sam']), q, macro.ks['pi8'])
    # Every active original word leaves at least four calls for exact
    # identity padding. Existing A55 controlL already includes its reserve.
    c['old_controlL'] = c['controlL']
    c['controlL'] = max(c['controlL'], sum(plane_upper.values())+4)
    c['plane_upper'] = plane_upper
    c['plane_q'] = q
    c['plane_k8'] = macro.ks['pi8']
    c['Lbase'] = c['coreL']+c['postL']+c['probeL']+4*c['controlL']
    c['Nbase'] = c['n']+c['Lbase']
    c['K'] = 4*(c['Nbase'].bit_length()+17375)
    return c


@lru_cache(None)
def plane_power(sign, m=CODE_BITS):
    return grid.plane_power(sign, m=m, step_bits=STEP_BITS)


class FullPlaneTask:
    def __init__(self, field):
        self.bound = prior.FieldTask(field)
        self.field = field
        self.cfg = configuration(self.bound.family.cfg)

    def validate(self, request):
        if type(request) is not Request or request.field != self.field:
            raise ValueError('request belongs to another field or family')
        self.bound.family._guard()

    def native_plane_blocks(self, plane, sign):
        if sign == 0:
            return
        if sign not in (-1, 1):
            raise ValueError('signed plane control required')
        k = plane_power(sign, len(self.cfg['sam']))
        yield from paid.old.plane_blocks(*plane, k, self.cfg['sam'], grid.Macros())

    def control_provider(self, label):
        if type(label) is PlaneLabel:
            return lambda axis, sign: self.native_plane_blocks(label.plane, sign)
        return paid.raw_control_factory

    @staticmethod
    def legacy_shape(label):
        if type(label) is PlaneLabel:
            return LegacyLabel(label.arm, label.sign, 0)
        return label

    def word_blocks(self, request, keep_marks=False):
        self.validate(request)
        label = self.legacy_shape(request.label)
        family = self.bound.family
        yield from paid.family_blocks(self.cfg, family.source.compiled_core_with_cuts,
                    family.actual_post_blocks, self.control_provider(request.label),
                    family.actual_probe_blocks, **asdict(label), keep_marks=keep_marks)

    def stages(self, request):
        self.validate(request)
        yield from paid.execution_stages(self.cfg, lambda: self.word_blocks(request))

    def prefix_blocks(self, request, name):
        self.validate(request)
        yield from prior.original.assembled_prefix(self.legacy_shape(request.label), name,
            self.cfg, self.bound.family.source.source_prefix_blocks,
            self.bound.processor_native_blocks, self.control_provider(request.label))

    def packet(self, request):
        self.validate(request)
        c = self.cfg
        return {
            'request_sha256': sha256(request.encode()).hexdigest(),
            'field_name_sha256': sha256(self.field.encode()).hexdigest(),
            'family': 'plane' if type(request.label) is PlaneLabel else 'A55',
            'label': asdict(request.label),
            'same_actual_core_and_post_as_bound_A55': True,
            'actual_post_factory': 'bound A54 core at this field, frozen across all labels',
            'RAW_early_births': c['n'], 'late_retention_pairs': c['K'],
            'actual_padded_lengths_hex': {k: hex(c[k]) for k in
                    ('coreL', 'controlL', 'postL', 'probeL', 'Lbase', 'Nbase')},
            'clock_layers_N_hex': hex(c['Nbase']+2*c['K']),
            'clock_dimension_formula': '2^n*(Lbase-2+3*2^K)-1',
            'closing_gate': f'G on {c["n"]+c["K"]-1}',
            'new_plane_step': '2^-6000', 'legacy_MG2_step': '2^-1700',
            'price': 'original Book H+J; all 425D modes and proper propagated cut',
            'gain': 'actual Gamma(Y,K_new), frozen across each comparison pair',
            'physical_C_closed': False, 'GR_closed': False}


def bounds(cfg, *, normalized_reading_error=F(0)):
    """Finite plane interpolant versus the full analytic source, in raw norm.

    Reading error is zero for exact mathematical prices. A supplied
    nonzero value is an additional bound on each normalized price row;
    it does not execute or pay a physical arithmetic reader.
    """
    if type(normalized_reading_error) is not F or normalized_reading_error < 0:
        raise ValueError('nonnegative rational reading-error bound required')
    m = len(cfg['sam'])
    t, gs, z = (F(1, 1 << k) for k in (STEP_BITS, 3208, 20))
    gamma0 = F(8, 3)*z*gs
    mu = F((1 << (m-1))+40*m, 1 << PLANE_BITS)
    bracket = 8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
    taylor = t*t*(bracket/16+F(1, 6))/gs
    control = 2*mu/(t*gs)
    heat = F(6*cfg['Nbase'], 359)/(t*gamma0)*F(1, 1 << (cfg['K']//4))
    analytic_heat_row = F(6, 359)/gamma0*F(1, 1 << (cfg['K']//4))
    row = taylor+control+heat+analytic_heat_row+normalized_reading_error
    factor = 208*(1 << (m+(m+1)//2))
    extra = factor*row
    feedback = analytic.bounds()['feedback_full_raw_dual']
    full_analytic = feedback+208*analytic_heat_row
    combined = full_analytic+extra
    assert mu < F(1, 1 << 27392)
    assert max(taylor, control, heat, analytic_heat_row) < F(1, 1 << 8149)
    if normalized_reading_error <= F(1, 1 << 8150):
        assert extra < F(1, 1 << 75)
        assert combined < F(1, 1 << 34)
    return {'plane_operator_error': mu, 'finite_Taylor_and_Cayley': taylor,
            'native_control_error': control, 'finite_heat_per_plane': heat,
            'analytic_heat_per_plane': analytic_heat_row,
            'normalized_reading_error': normalized_reading_error,
            'finite_vs_analytic_row': row, 'dimension_factor': factor,
            'finite_vs_analytic_full_raw_dual': extra,
            'full_analytic_target_error': full_analytic,
            'finite_full_raw_target_error': combined}


def build():
    instance = FullPlaneTask(FieldCentre())
    cfg = instance.cfg
    bounds(cfg)
    bounds(cfg, normalized_reading_error=F(1, 1 << 8150))
    paths = [Path(__file__), D/'round55/regular_comparison_task.py',
             D/'round55/REGULAR_COMPARISON_TASK.json',
             D/'round56/complete_code_source.py', D/'round56/RESULT.json',
             D/'round49/paid_padding.py', D/'round49/two_bit_paid_family.py',
             D/'round42/fixed_post_paid_family.py',
             O/'round105/regular_paid_family.py',
             O/'round109/B109_FULL_SKEW_RECOVERY_CHECK.json',
             O/'round110/B110_ANALYTIC_HEAT_STATISTICAL_CHECK.json',
             O/'round111/B111_A56_AUDIT_CHECK.json',
             O/'round112/plane_grid_32768.py', O/'round112/GRID_32768_CERTIFICATE.json',
             O/'round112/B112_PLANE_PRECISION_CHECK.json']
    return {
        'status': 'FOUR_NATIVE_CODE_PLANE_FAMILIES_ON_REMEASURED_COMMON_CLOCK',
        'example_bound_request': instance.packet(Request(instance.field, PlaneLabel('Pf', 1, (0, 1)))),
        'CODE_bits': CODE_BITS,
        'new_plane_label_count': '4*2^5376*(2^5376-1)',
        'all_label_count_per_field': '26881+5*2^5376*(2^5376-1)',
        'field_names_are_infinite_union_of_finite_requests': True,
        'plane_power_upper_hex': hex(cfg['plane_q']),
        'plane_pi8_power_hex': hex(cfg['plane_k8']),
        'plane_native_call_upper_hex': {k: hex(v) for k, v in cfg['plane_upper'].items()},
        'new_Nbase_bit_length': cfg['Nbase'].bit_length(),
        'new_K': cfg['K'], 'original_A55_control_length_hex': hex(cfg['old_controlL']),
        'source_core_post_and_probes_unchanged_as_words': True,
        'full_covector_type': 'linear interpolant of all four native plane finite contrasts',
        'raw_norm': 'max(||ell(Pf)-ell(Qf)/2+ell(Qb)/2||_2,max_a||X_a||op/52)',
        'native_interpolant_vs_analytic_full_raw_dual_error_lt': '2^-75',
        'native_interpolant_target_DI_tau_composed_L_raw_dual_error_lt': '2^-34',
        'optional_normalized_price_reading_error_per_row_lt': '2^-8150',
        'physical_arithmetic_reader_executed_or_free': False,
        'arbitrary_X_joint_native_finite_theorem_claimed': False,
        'physical_iota_Vh_or_Cost_Info_identified': False,
        'physical_C_closed': False, 'GR_closed': False,
        'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    out = build()
    (P/'FULL_PLANE_FAMILY_PLAN.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('status', 'new_Nbase_bit_length', 'new_K')}, indent=2))
