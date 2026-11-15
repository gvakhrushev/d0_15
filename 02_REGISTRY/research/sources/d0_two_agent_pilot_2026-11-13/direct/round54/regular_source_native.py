#!/usr/bin/env python3
"""One parameterized SOURCE profile on the original full DATA fibre.

Every field-dependent component reads the same immutable rational field.
All integer inverse depths are literal. Profiles still contain SourceI;
regular_global_source performs its paid G/CX replacement.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round53'))
import regular_source_components as component
sys.path.insert(0, str(D/'round48'))
import two_bit_source_native as old
sys.path.insert(0, str(old.B/'round103'))
import regular_link_julia as link

t = component.t
local = old.local
nb = old.nb
BANKS = old.BANKS


class Sources:
    def __init__(self, field):
        if not isinstance(field, t.FieldCentre):
            raise TypeError('one validated immutable FieldCentre required')
        self.field = field
        self.components = component.Components(field)

    def link_blocks(self, bank, lay, depth=0):
        """Original fixed sectors plus B103 variable sectors, without overlap."""
        assert bank in BANKS and type(depth) is int and depth >= 0
        _, catalogue = old.link.fixed_and_catalogue()
        section = catalogue[bank]
        assert not section['variable'] or bank == 'f'
        odd = depth % 2
        stages = ('fixed', 'variable')
        for stage in reversed(stages) if odd else stages:
            if stage == 'fixed':
                entries = section['fixed']
                for entry in reversed(entries) if odd else entries:
                    for tree in old.link.sector_blocks(lay, entry, reverse=bool(odd)):
                        yield local.invert(tree, depth-odd, lay)
            elif section['variable']:
                for tree in link.variable_bank_blocks(self.field, lay, reverse=bool(odd)):
                    yield local.invert(tree, depth-odd, lay)

    def omega_blocks(self, bank, lay=None, depth=0):
        assert bank in BANKS and type(depth) is int and depth >= 0
        lay = old.choi_layout() if lay is None else lay
        old.validate_choi(lay)
        odd = depth % 2
        stages = ('prefix', 'coframe', 'link')
        for stage in reversed(stages) if odd else stages:
            if stage == 'coframe':
                yield from self.components.coframe_blocks(bank, lay, depth)
            elif stage == 'link':
                yield from self.link_blocks(bank, lay, depth)
            else:
                for tree in old.old.prefix.prefix_blocks(old.inputs()['prefix'], lay, True, bool(odd)):
                    yield local.invert(tree, depth-odd, lay)

    def half_blocks(self, bank, lay=None, levels=9, depth=0):
        assert type(levels) is int and 0 <= levels <= 9
        assert type(depth) is int and depth >= 0
        lay = old.choi_layout() if lay is None else lay
        x = old.inputs()
        al = old.old.adapter_layout(lay)
        fixed = old.old.adapter.fixed(al, int(x['phase']['phase_k']),
                    int(x['level9']['correction_l']), x['h_k'])

        def leaf(blocks, d):
            for tree in reversed(blocks) if d % 2 else blocks:
                yield local.invert(tree, d, lay)

        def walk(level, d):
            if level == 0:
                yield from leaf([fixed['H']], d)
                yield from self.omega_blocks(bank, lay, d)
                yield from leaf([fixed['H']], d)
                return
            children = [('A', 0), ('G', 0), ('A', 1), ('S', 0), ('A', 0)]
            for kind, extra in reversed(children) if d % 2 else children:
                if kind == 'A':
                    yield from walk(level-1, d+extra)
                else:
                    yield from leaf(fixed['good'] if kind == 'G' else fixed['start'], d)

        if depth % 2:
            yield from leaf([fixed['correction']], depth)
            yield from walk(levels, depth)
        else:
            yield from walk(levels, depth)
            yield from leaf([fixed['correction']], depth)

    def choi_blocks(self, bank, lay=None, depth=0, extra_external=()):
        lay = old.choi_layout() if lay is None else lay
        old.validate_choi(lay, extra_external)
        stages = [('PRIVATE_RAW', 0), ('DATA_RAW', 0), ('R', 0),
                  ('U', 1), ('R', 0), ('U', 0)]
        for kind, intrinsic in reversed(stages) if depth % 2 else stages:
            d = depth+intrinsic
            if kind == 'PRIVATE_RAW':
                yield from old.raw_blocks(old.private(lay), lay, d)
            elif kind == 'DATA_RAW':
                yield from old.raw_blocks(old.data(lay), lay, d)
            elif kind == 'R':
                k = int(old.inputs()['fixed']['joint_reflection_pi']['k'])
                yield from old.gray.blocks(old.data(lay)+old.private(lay),
                    lay['aux_arbitrary'], k, lay['port'], tuple(lay['spin']),
                    [*lay['SAM'], lay['oldRIGHT_witness'], *extra_external], d)
            else:
                yield from self.half_blocks(bank, lay, 9, d)

    def frame_blocks(self, bank, lay=None, depth=0):
        lay = old.car_layout() if lay is None else lay
        U, _, R = local.car.fixed_components(lay)
        stages = [('STAR', 1), ('R', 0), ('STAR', 0),
                  ('M', 1), ('R', 0), ('M', 0)]
        for kind, intrinsic in reversed(stages) if depth % 2 else stages:
            d = depth+intrinsic
            if kind == 'M' and bank in ('q', 'y+', 'y-'):
                yield from self.components.material_blocks(bank, lay, d)
            else:
                yield local.invert(R if kind == 'R' else U, d, lay)

    def car_blocks(self, bank, lay=None, depth=0, extra_external=()):
        lay = old.car_layout() if lay is None else lay
        pv = [lay['predicate_flag'], *lay['predicate_work']]
        old.vac.validate(lay, [*pv, lay['native_aux_arbitrary'], *extra_external])
        assert len(lay['SAM']) == 5376
        stages = ('PRIVATE_RAW', 'VACUUM', 'FRAME')
        for stage in reversed(stages) if depth % 2 else stages:
            if stage == 'PRIVATE_RAW':
                yield from old.raw_blocks(pv, lay, depth)
            elif stage == 'VACUUM':
                yield from old.vacuum_blocks(lay, depth)
            else:
                yield from self.frame_blocks(bank, lay, depth)


def fixed_link_sector_upper():
    """B93's bound(0, False), explicitly isolated from its old variable bank."""
    native = old.link

    def select(width):
        return native.old.select_cost(list(range(width)), [1]+[0]*(width-1),
                                      native.Q, common_controls=29)

    def maxdepth(counts, top):
        rows = [counts]
        for _ in range(top):
            rows.append(native.old.invert_cost(rows[-1]))
        return Counter({k: max(r[k] for r in rows) for k in counts})

    pair = maxdepth(select(17), 2)
    pair['CX'] += 2
    return (old.times(pair, 96)+select(13)+select(14)+old.times(select(15), 4))


@lru_cache(None)
def inventory_upper():
    x = old.inputs()
    local_upper = component.componentwise_upper()
    _, catalogue = old.link.fixed_and_catalogue()
    fixed = fixed_link_sector_upper()
    result = {'Choi': {}, 'CAR': {}, 'link': {}}
    for bank in BANKS:
        section = catalogue[bank]
        assert not section['variable'] or bank == 'f'
        link_count = old.times(fixed, len(section['fixed']))
        link_count.update(link.variable_bank_cost_upper(len(section['variable'])))
        result['link'][bank] = link_count
        omega = Counter()
        for tree in old.old.prefix.prefix_blocks(x['prefix'], old.choi_layout(), True):
            omega.update(old.old.prefix.resource(tree, old.choi_layout()['port']))
        omega.update(local_upper['coframe'][bank]['forward'])
        omega.update(link_count)
        half, hi = old.old.adapter.native_budget(0, int(x['phase']['phase_k']),
            int(x['level9']['correction_l']), x['h_k'], omega, levels=9)
        reflection = old.gray.counts(46, int(x['fixed']['joint_reflection_pi']['k']))
        source = old.raw_counts(46)+old.times(reflection, 2)+half+hi
        result['Choi'][bank] = {'Omega_forward_upper': omega, 'half_forward_upper': half,
            'source_forward_upper': source, 'source_literal_inverse_upper': old.inv(source)}

        U, Ui, R = local.car.fixed_components(old.car_layout())
        price = lambda tree: local.car.resource(tree, old.car_layout()['port'])
        frame = price(U)+price(Ui)+old.times(price(R), 2)
        if bank in local_upper['material']:
            row = local_upper['material'][bank]
            frame.update(row['forward']); frame.update(row['literal_inverse'])
        else:
            frame.update(price(U)); frame.update(price(Ui))
        # Original paid vacuum, including its RAW/preparation/Fourier words.
        vacuum = old.car_inventory(bank)['vacuum_prefix_forward']
        car = old.raw_counts(3)+vacuum+frame
        result['CAR'][bank] = {'frame_forward_upper': frame, 'source_forward_upper': car,
                              'source_literal_inverse_upper': old.inv(car)}

    total = old.site.inventory(x['site'])['SITE_forward']
    for bank in BANKS:
        total.update(old.times(result['Choi'][bank]['source_forward_upper'], 180))
        total.update(old.times(result['CAR'][bank]['source_forward_upper'], 16))
    total.update(old.times(result['Choi']['f']['source_forward_upper'], 180))
    total.update(old.times(result['CAR']['q']['source_forward_upper'], 16))
    result['all_SOURCE_forward_componentwise_upper'] = total
    result['all_SOURCE_literal_inverse_componentwise_upper'] = old.inv(total)
    return result


def error_bounds():
    x = old.inputs()
    delta = F(1, 1 << 3460)
    old_delta = F(1, 1 << 3456)
    eps = F(1, 1 << 4096)
    pre = x['prefix']
    prefix = F(int(pre['prefix_error_L1_numerator_hex'], 16), 1 << pre['precision_bits'])
    # Coframe and link occupy disjoint address sectors. Fixed B93 links
    # retain their 102-delta bound; variable B103 Julia uses 498-delta.
    select = max(28*delta, 102*delta, 498*delta)
    loader = prefix+select
    levels = 3**9
    half = F(1, 1 << 9841)+levels*loader+(2*levels+(2*levels-2)*23+1)*eps
    choi = 4*half+2*old_delta
    # A53's 3-delta preparation is stronger than A48's 3-old_delta.
    # Retain the old full-frame/vacuum error including both preparations.
    car = 24*old_delta+43*eps
    site = 18*old_delta
    total = 1440*choi+128*car+site
    assert total < F(1, 1 << 3423)
    return {'controlled_Omega': loader, 'half_vector_anchor_isometry': half,
            'Choi_declared_DATA_fibre': choi, 'CAR_declared_DATA_fibre': car,
            'SITE_all_columns': site, 'all1440Choi_128CAR_SITE': total}
