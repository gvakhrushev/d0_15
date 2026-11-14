#!/usr/bin/env python3
"""Actual A32 addressed-inventory collision, consumed by source-price binding.

Does not assign a physical Cost or Info. It checks that a proposed binding
depending only on the listed identical statistics cannot reproduce A33.
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json
import sys

P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round32'))
import finite_book_comparison as pair


def inventory(node):
    op = node['op']
    if op == 'seq':
        out = Counter()
        for child in node['children']:
            out.update(inventory(child))
        return out
    if op == 'repeat':
        return Counter({k:int(node['count'])*v for k,v in inventory(node['child']).items()})
    assert op in ('G','CX')
    return Counter({(op, tuple(node['wires'])):1})


def main():
    parts = {sign:pair.endpoint_parts(sign, 2) for sign in ('plus','minus')}
    counts = {sign:sum((inventory(n) for n in value.values()), Counter()) for sign,value in parts.items()}
    assert counts['plus'] == counts['minus']
    assert parts['plus']['pre'] != parts['minus']['pre']
    assert parts['plus']['last_g'] == parts['minus']['last_g']
    nplus,nminus = pair.powers()
    assert nplus != nminus
    sam = tuple(parts['plus']['last_g']['wires'])
    assert counts['plus']['G',sam] == nplus+nminus
    plan = json.loads((D/'round32/FINITE_BOOK_COMPARISON_PLAN.json').read_text())
    assert plan['late_retention_pairs'] == 66076
    assert plan['early_canonical_RAW_births'] == 10407050782
    assert plan['initial_history']['previous_paid_stages'] == 0
    positive = json.loads((D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json').read_text())
    assert positive['actual_normalized_finite_comparison_scalar_gt'] == '2^-44'
    # Adding the identical core, birth sequence and one-G-per-late-bit tails
    # preserves exact equality of the two fully addressed inventories.
    paths = [Path(__file__), D/'round32/finite_book_comparison.py',
             D/'round32/FINITE_BOOK_COMPARISON_PLAN.json', D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json',
             D/'round33/ROOT_REVIEW_B66.json']
    out = {'status':'PASS_ACTUAL_PAIR_COUNT_ONLY_PRICE_BINDING_OBSTRUCTION',
           'actual_SAM_index':2,
           'same_complete_addressed_primitive_inventory':True,
           'same_initial_history_and_canonical_birth_sequence':True,
           'same_clock_layer_dimensions_and_final_gate':True,
           'same_canonical_RAW_birth_marginals':True,
           'different_ordered_words':True,
           'same_source_mark_ordinals_not_same_mark_states':True,
           'endpoint_only_inventory':[{ 'primitive':k[0], 'logical_wires':list(k[1]),
                                        'count_hex':hex(v)} for k,v in sorted(counts['plus'].items())],
           'operator_price_inequality_consumed':'A33/B66: (H+J)_+>(H+J)_-',
           'excluded_binding_class':'Any exact price function of only addressed primitive inventory, canonical birth marginals/sequence and clock dimensions on these histories',
           'unrestricted_Cost_Info_binding_excluded':False,
           'actual_native_Info_assigned':False,
           'primitive_code_length_or_description_length_equated_with_Book_price':False,
           'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},
           'physical_C_closed':False,'GR_closed':False}
    (P/'COUNT_ONLY_BINDING_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','same_complete_addressed_primitive_inventory','different_ordered_words')}))


if __name__ == '__main__':
    main()
