#!/usr/bin/env python3
"""One fixed constructor, finite field-name requests and actual marked words.

Field data vary at fixed constructor c. Each rational request is finite;
the union of all field names is not claimed to be one finite catalogue.
This binds the declared A54/B105 operation, not a physical Cost-Info law.
"""
from pathlib import Path
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from hashlib import sha256
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round54'))
import regular_global_source as source
sys.path.insert(0, str(source.s.old.B/'round105'))
import regular_paid_family as paid
sys.path.insert(0, str(D/'round52'))
import scoped_comparison_task as original

FieldCentre = source.t.FieldCentre
Label = original.Label
prefixes = original.prefixes
M = 2688


@dataclass(frozen=True)
class Request:
    field: FieldCentre
    label: Label = Label()

    def __post_init__(self):
        if not isinstance(self.field, FieldCentre) or not isinstance(self.label, Label):
            raise TypeError('validated finite field and comparison label required')

    def encode(self):
        return json.dumps({'field': json.loads(self.field.encode()),
                           'label': json.loads(original.encode(self.label))},
                          sort_keys=True, separators=(',', ':')).encode('ascii')

    @classmethod
    def decode(cls, packet):
        if type(packet) is not bytes:
            raise TypeError('canonical finite packet must be bytes')
        obj = json.loads(packet)
        if type(obj) is not dict or set(obj) != {'field', 'label'}:
            raise ValueError('exact field/label request schema required')
        field_bytes = json.dumps(obj['field'], separators=(',', ':')).encode('ascii')
        label_bytes = json.dumps(obj['label'], sort_keys=True, separators=(',', ':')).encode('ascii')
        request = cls(FieldCentre.decode(field_bytes), original.decode(label_bytes))
        if request.encode() != packet:
            raise ValueError('noncanonical request encoding')
        return request


class FieldTask:
    def __init__(self, field):
        if not isinstance(field, FieldCentre):
            raise TypeError('validated immutable field required')
        self.field = field
        self.family = paid.RegularPaidFamily(source, field,
                         source.upper_inventory_and_error()['W_G_CX_upper'])

    def validate(self, request):
        if not isinstance(request, Request) or request.field != self.field:
            raise ValueError('request is bound to another field')
        self.family._guard()

    def word_blocks(self, request, keep_marks=False):
        self.validate(request)
        yield from self.family.blocks(**asdict(request.label), keep_marks=keep_marks)

    def stages(self, request):
        self.validate(request)
        yield from self.family.execution_stages(**asdict(request.label))

    def processor_native_blocks(self, name):
        self.family._guard()
        selected = prefixes.processor_stages()[:prefixes.descriptor(name)['processor_stage_count']]
        assert all(x['kind'] not in ('SOURCE', 'SITE', 'SIGMA') for x in selected)

        def profile():
            for stage in selected:
                yield from self.family.source.stage_blocks(stage)

        for tree in source.compiler().stream(profile()):
            yield source.physical_tree(tree)

    def prefix_blocks(self, request, name):
        self.validate(request)
        # The body is literally a prefix of THIS B105 history. Core padding
        # still occurs after return; no post or Qb/Pb is moved before a mark.
        yield from original.assembled_prefix(request.label, name, self.family.cfg,
            self.family.source.source_prefix_blocks, self.processor_native_blocks,
            paid.paid.raw_control_factory)

    def packet(self, request):
        self.validate(request)
        c = self.family.cfg
        return {'request_sha256': sha256(request.encode()).hexdigest(),
                'field_name_sha256': sha256(self.field.encode()).hexdigest(),
                'label': asdict(request.label),
                'same_post_for_all_labels_at_this_field': True,
                'actual_post_target_factory': 'this field-bound source.core_blocks',
                'RAW_early_births': c['n'], 'late_retention_pairs': c['K'],
                'actual_padded_lengths_hex': {k: hex(c[k]) for k in
                    ('coreL', 'controlL', 'postL', 'probeL', 'Lbase', 'Nbase')},
                'clock_layers_N_hex': hex(c['Nbase']+2*c['K']),
                'clock_dimension_formula': '2^n*(Lbase-2+3*2^K)-1',
                'input_rank': 1, 'initial_carrier': 'H0=C',
                'closing_gate': 'G on n+K-1',
                'physical_C_closed': False, 'GR_closed': False}


def frontier_bounds():
    """Consume uniform B91/A47 chart bounds with the NEW actual e_SOURCE."""
    u = source.upper_inventory_and_error()
    ctrl = paid.paid.control
    d = ctrl.a47.source_derivative_enclosure()
    eP = ctrl.decode(ctrl.control_plan()['control_vs_exp_tX_error'])
    sigma, step = F(1, 1 << 80), F(1, 1 << 1700)
    M1 = d['full_bank_M1']
    eB = u['full_SOURCE_DATA_fibre_prefix_error']
    extra = (eB+2*eP)/(sigma*step)+F(4, 3)*104*M1*step**2
    source_jet = d['two_bit_ideal_axis_jet_error']+extra
    report = json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    known = report['seven_report_all_known_approximate_macros']
    assert known % 7 == 0
    eD = F(8*(known//7), 1 << 4096)+u['replacement_error']
    jet = source_jet+eD*M1
    centre = sigma*104*M1+eB+eD
    midpoint = centre+2*eP+2*step**2
    effect = 2*jet+2*M1*midpoint
    assert extra < F(1, 1 << 1642)
    assert eD < F(1, 1 << 4058)
    assert centre < F(1, 1 << 62) and midpoint < F(1, 1 << 62)
    assert source_jet < F(1, 1 << 44) and jet < F(1, 1 << 44)
    assert effect < F(1, 1 << 43)
    return {'new_SOURCE_prefix_error': eB, 'actual_control_jet_extra': extra,
            'uniform_SOURCE_full_axis_jet': source_jet,
            'all_completed_processor_prefix_error': eD,
            'full_prefix_centre_error': centre, 'full_prefix_midpoint_error': midpoint,
            'full_prefix_finite_axis_jet_error': jet,
            'norm_one_joint_effect_finite_axis_jet_error': effect}


def build():
    task = FieldTask(FieldCentre())
    packet = task.packet(Request(task.field))
    paths = [Path(__file__), D/'round54/regular_global_source.py',
        D/'round54/regular_source_native.py', D/'round54/REGULAR_GLOBAL_SOURCE_PLAN.json',
        D/'round54/RESULT.json', source.s.old.B/'round105/regular_paid_family.py',
        source.s.old.B/'round105/B105_REGULAR_PAID_CHECK.json',
        source.s.old.B/'round106/B106_A54_AUDIT_CHECK.json',
        D/'round52/scoped_comparison_task.py', D/'round51/completed_marked_prefixes.py',
        D/'round47/full_vector_controls.py', D/'round47/FULL_VECTOR_CONTROL_PLAN.json',
        source.s.old.B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
        source.s.old.B/'round100/B100_A51_INDEPENDENT_AUDIT_RU.md',
        source.s.old.B/'round107/B107_OFF_SHELL_FOUR_AXIS_SOURCE_RECOVERY_RU.md',
        source.s.old.B/'round107/B107_REGULAR_SOURCE_RECOVERY_CHECK.json']
    # Require the original filename rather than silently dropping an input.
    for p in paths:
        assert p.is_file(), p
    return {'status': 'REGULAR_FIELD_REQUESTS_BOUND_TO_ACTUAL_PAID_MARKED_FAMILY',
        'fixed_constructor': 'A54 SOURCE + B105 actual field-bound post and uniform paid clock',
        'field_data_vary_at_fixed_constructor': True,
        'rational_field_coordinates': M, 'field_open_radius': '2^-32',
        'ordinary_catalogue_count_per_fixed_field': 26881,
        'post_probe_catalogue_count_per_fixed_field': '2^5376*(2^5376-1)',
        'total_catalogue_count_per_fixed_field': '26881+2^5376*(2^5376-1)',
        'all_field_names_claimed_one_finite_catalogue': False,
        'finite_quotient_scope': 'each request reads its finite canonical field-name/label packet; locally over task data',
        'common_actual_clock_example': packet,
        'price': 'beta^-1 log(359D+2 Tr exp(-beta Delta0))-log(1-z+z C*C)',
        'full_Hodge_modes': '425D',
        'p_z_beta': 'same original p, z=2^-20, fixed positive beta; no retuning',
        'gain': 'actual Gamma(Y), fixed for comparisons within one field; normalize DB, not D(B/Gamma)',
        'reference_graph': 'E(word)=E(actual compiled reference(c,Y,label)) with the same full birth/layout/input/cut/marks',
        'all_twelve_post_Qf_marks': prefixes.registry(),
        'SOURCE_before_Qf_retained_separately': True,
        'prefix_provider_for_every_independent_label': True,
        'available_original_REPORT_READY_pairs': original.report_labels(),
        'uniform_matched_full_vector_axis_jet_error_lt': '2^-44',
        'uniform_unconditioned_norm_one_effect_axis_jet_error_lt': '2^-43',
        'uniform_full_prefix_midpoint_error_lt': '2^-62',
        'B107_off_shell_price_recovery': {
            'target_covector': ['DI_tau(Y)', '-DI_tau(Y)/2', 'DI_tau(Y)/2', '0'],
            'four_2688_axis_recovery_Euclidean_error_lt': '2^-102',
            'scope': 'fixed-y MG2 control covector with actual Gamma(Y); not all logical sources or a zero-source claim'},
        'bounds': {k: source.s.old.encode_error(v) for k, v in frontier_bounds().items()},
        'jet_scope': 'matched controls only, twelve completed marks, selected A23 full DATA/private RAW fibre with external reference',
        'independent_or_pre_Qf_jets_claimed_geometric': False,
        'physical_fine_instrument_registered_or_measurement_inserted': False,
        'parser_compiler_or_readback_execution_cost_claimed_free': False,
        'all_logical_sources_or_Vh_norm_or_Cost_Info_closed': False,
        'production_words_executed': False, 'physical_C_closed': False, 'GR_closed': False,
        'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    result = build()
    (P/'REGULAR_COMPARISON_TASK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])
