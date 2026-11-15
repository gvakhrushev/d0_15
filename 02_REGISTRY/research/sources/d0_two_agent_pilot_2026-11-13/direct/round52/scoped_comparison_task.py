#!/usr/bin/env python3
"""One finite A49 comparison task, with actual word/prefix/clock bindings.

The frozen centre is part of this finite packet. This is not an open-field
compiler and does not supply physical instrument or Cost-Info admission.
"""
from pathlib import Path
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round51'))
import completed_marked_prefixes as prefixes
paid = prefixes.paid
M = 2688
CODE_BITS = 2*M
ARMS = ('matched', 'Pf', 'Qf', 'Qb', 'Pb')


@dataclass(frozen=True)
class Label:
    arm: str = 'centre'
    sign: int = 0
    axis: int = 0
    plane: tuple = None

    def __post_init__(self):
        if type(self.sign) is not int or type(self.axis) is not int:
            raise ValueError('sign and axis must be literal integers')
        if self.arm == 'centre':
            valid = self.sign == 0 and self.axis == 0 and self.plane is None
        elif self.arm in ARMS:
            valid = self.sign in (-1, 1) and 0 <= self.axis < M and self.plane is None
        elif self.arm == 'post_probe':
            valid = (self.sign in (-1, 1) and self.axis == 0
                     and type(self.plane) is tuple and len(self.plane) == 2
                     and all(type(q) is int for q in self.plane)
                     and 0 <= self.plane[0] < self.plane[1] < (1 << CODE_BITS))
        else:
            valid = False
        if not valid:
            raise ValueError('label is outside the actual finite A49 catalogue')


def encode(label):
    if not isinstance(label, Label):
        raise TypeError('expected validated Label')
    return json.dumps(asdict(label), sort_keys=True, separators=(',', ':')).encode('ascii')


def decode(packet):
    obj = json.loads(packet)
    if type(obj) is not dict or set(obj) != {'arm', 'sign', 'axis', 'plane'}:
        raise ValueError('exact label schema required; no extra field or hidden input')
    if obj['plane'] is not None:
        if type(obj['plane']) is not list:
            raise ValueError('plane must be an encoded pair')
        obj['plane'] = tuple(obj['plane'])
    result = Label(**obj)
    if encode(result) != packet:
        raise ValueError('canonical finite encoding required')
    return result


def catalogue(include_post_probe=False):
    yield Label()
    for arm in ARMS:
        for axis in range(M):
            for sign in (-1, 1):
                yield Label(arm, sign, axis)
    if include_post_probe:
        # A finite but enormous lazy catalogue; production enumeration not run.
        a = 0
        while a < (1 << CODE_BITS)-1:
            b = a+1
            while b < (1 << CODE_BITS):
                yield Label('post_probe', -1, plane=(a, b))
                yield Label('post_probe', 1, plane=(a, b))
                b += 1
            a += 1


def word_blocks(label, keep_marks=False):
    # The fixed actual post is calculated once from the same centre core;
    # no endpoint, sign, axis, or post-probe label retunes its target.
    yield from paid.production_blocks(**asdict(label), keep_marks=keep_marks)


def stages(label):
    yield from paid.execution_stages(paid.production_configuration(),
                                    lambda: word_blocks(label))


def assembled_prefix(label, name, cfg, source_factory, processor_factory,
                     control_factory):
    """Actual early prefix for every independent arm, not only matched signs."""
    if name != 'SOURCE_before_Qf':
        prefixes.descriptor(name)
    signs = paid.slot_signs(label.arm, label.sign)
    yield from paid.pad.counted_pad(lambda: control_factory(label.axis, signs['Pf']),
                                   cfg['controlL'], cfg['sam'])
    yield from source_factory()
    if name == 'SOURCE_before_Qf':
        return
    yield from paid.pad.counted_pad(lambda: control_factory(label.axis, signs['Qf']),
                                   cfg['controlL'], cfg['sam'])
    yield from processor_factory(name)


def prefix_blocks(label, name):
    yield from assembled_prefix(label, name, paid.production_configuration(),
                                paid.source.source_prefix_blocks,
                                prefixes.processor_native_blocks,
                                paid.raw_control_factory)


def report_labels():
    """Existing physical label addresses; no measurement is inserted."""
    g = paid.source
    ns = g.namespace()
    local = ns['local_report']
    result = []
    for index, report in enumerate(ns['reports']):
        physical = lambda q: g.physical_wire(g.ns.report_wire(ns, report, q))
        result.append({'report': index, 'frontier': f'REPORT_{index}_complete',
                       'report_wire': physical(local['report_wire']),
                       'ready_wire': physical(local['all_READY_wire']),
                       'outcomes': [[0, 0], [0, 1], [1, 0], [1, 1]]})
    return result


def build():
    c = paid.production_configuration()
    refs = [Path(__file__), D/'round23/car_vacuum_prefix.py',
            D/'round48/two_bit_source_targets.py', D/'round48/two_bit_global_source.py',
            D/'round49/two_bit_paid_family.py', D/'round49/finite_actual_target.py',
            D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json',
            D/'round50/RESULT.json', D/'round51/completed_marked_prefixes.py',
            D/'round51/RESULT.json',
            D.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md']
    return {
        'status': 'CONCRETE_FINITE_COMPARISON_TASK_WITH_OPEN_PHYSICAL_SECTION_WITNESSES',
        'finite_task_id': 'A49_fixed_centre_four_independent_legs_and_post_probe',
        'request_labels': {'ordinary_count': 1+10*M, 'independent_axis_pairs': 4*M,
                           'matched_axis_pairs': M,
                           'post_probe_label_count_hex': hex((1 << CODE_BITS)*((1 << CODE_BITS)-1))},
        'regular_field_argument_implemented': False,
        'fixed_centre_owner': 'A48/two_bit_source_targets.py and its pinned A20/B21 inputs',
        'initial_carrier': 'H0=C; canonical RAW births, no pre-existing old tensor factor',
        'actual_early_RAW_births': c['n'], 'actual_late_retention_pairs': c['K'],
        'actual_layout': {k: hex(c[k]) for k in ('coreL', 'controlL', 'postL', 'probeL', 'Lbase', 'Nbase')},
        'clock_layers_N_hex': hex(c['Nbase']+2*c['K']),
        'clock_dimension': 'D=2^n*(Lbase-2+3*2^K)-1',
        'complete_Hodge_modes': '425D; original rank-one scene cut; both full Hodge degrees',
        'price': 'beta^-1 log(359D+2 Tr exp(-beta Delta0))-log(1-z+z C*C)',
        'price_is_the_declared_Book03_H_plus_J_not_a_proved_full_Cost_Info_binding': True,
        'p': 'positive root p^2+p-1=0', 'z': '2^-20',
        'beta': 'same fixed positive Book03 parameter as A49, no retuning across labels',
        'gain': 'same actual central positive Gamma as A49; frozen for first differences',
        'reference_graph': 'E(word)=E(actual A49 word at this label), with same birth tree/layout/input/cut',
        'tuple_includes': ['all birth boundaries and retained complements',
                           'complete square segment maps and actual final closing G',
                           'SOURCE_before_Qf at its actual time',
                           'twelve completed forward prefix maps from A51',
                           'both original B82 control cuts; no SOURCE/READY compression'],
        'prefixes': ['SOURCE_before_Qf']+[x['name'] for x in prefixes.registry()],
        'geometric_axis_jet_bound_applies_to': 'matched arms at twelve post-Qf frontiers only',
        'available_report_label_tests': report_labels(),
        'actual_registered_fine_instrument_identified': False,
        'measurement_or_free_readback_inserted': False,
        'open_Book01_witnesses': ['original fine instrument binding and real suffix/readback compatibility',
                                 'free regular-field reference family and its actual physical lift',
                                 'projection/refinement of accumulated requested histories',
                                 'all genuine logical/old/input/WORK/scene/record/Info source rows',
                                 'same-execution physical Cost-Info binding'],
        'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest() for f in refs},
        'production_catalogue_or_words_executed': False,
        'physical_C_closed': False, 'GR_closed': False}


if __name__ == '__main__':
    value = build()
    (P/'FINITE_COMPARISON_TASK.json').write_text(json.dumps(value, indent=2)+'\n')
    print(value['status'])
