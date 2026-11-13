#!/usr/bin/env python3
"""Compile every A12 palette into a fixed finite reversible circuit grammar."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import reversible_selectors as r

P=Path(__file__).resolve().parent
A12=P.parent/'round12'
INPUTS=['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json']


def row_counts(plan,row):
    q=plan['layout'];width=len(q['fair'])+len(q['rank'])
    pattern=row['palette'] | row['kind']<<len(q['palette'])
    counts=Counter(r.counts_of(r.pattern_gate(q['palette']+q['kind'],pattern,q['row_flag'][0],q['pattern_work'])))
    counts.update(counts.copy())
    for threshold,mask in row['boundaries']:
        threshold=int(threshold)
        if not threshold:continue
        if threshold==2**width:counts['X']+=2
        else:
            counts['X']+=4*bin(threshold).count('1')
            counts['CX']+=4*width+2
            counts['CCX']+=4*width
        counts['CCX']+=bin(mask).count('1')
    return dict(sorted((k,v) for k,v in counts.items() if v))


def circuit_counts(plan):
    total=Counter(r.counts_of(r.prefix_word(plan)));total.update(total.copy())
    for row in plan['rows']:total.update(row_counts(plan,row))
    return dict(sorted(total.items()))


def main():
    compiled={}
    hashes={}
    for name in INPUTS:
        source=A12/name;palette=json.loads(source.read_text());plan=r.make_plan(palette)
        plan['input_palette_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
        plan['terminal_gate_counts']=circuit_counts(plan)
        output=name.replace('PALETTE','CIRCUIT')
        raw=json.dumps(plan,separators=(',',':'))+'\n'
        (P/output).write_text(raw)
        hashes[output]=hashlib.sha256(raw.encode()).hexdigest()
        compiled[name]={'circuit_file':output,'wire_count':plan['wire_count'],
                        'terminal_gate_counts':plan['terminal_gate_counts'],
                        'input_palette_sha256':plan['input_palette_sha256']}
        print(output,plan['wire_count'],plan['terminal_gate_counts'],flush=True)
    success={}
    for label,width in [('internal',6),('top',2)]:
        plan=r.first_success_plan(7,width);plan['terminal_gate_counts']=r.counts_of(r.first_success_word(plan))
        success[label]=plan
    (P/'FIRST_SUCCESS_CIRCUITS.json').write_text(json.dumps(success,indent=2)+'\n')
    hashes['FIRST_SUCCESS_CIRCUITS.json']=hashlib.sha256((P/'FIRST_SUCCESS_CIRCUITS.json').read_bytes()).hexdigest()
    # Counts only for the fixed selector decoders/label routing, not the missing
    # node-stack interpreter, payload routing, fair factories, or physical gate realization.
    slots=json.loads((A12/'SELECTOR_COMPILATION.json').read_text())['padded_interpreter_slots_per_ten_sign_report']
    total=Counter()
    for name,multiplicity in zip(INPUTS,[slots*7,10*7,1]):
        total.update({k:v*multiplicity for k,v in compiled[name]['terminal_gate_counts'].items()})
    for label,multiplicity in [('internal',slots),('top',10)]:
        total.update({k:v*multiplicity for k,v in success[label]['terminal_gate_counts'].items()})
    result={'status':'EXPLICIT_FINITE_X_CX_CCX_SELECTOR_CIRCUIT_GRAMMARS',
            'circuits':compiled,'output_sha256':hashes,'decoder_label_routing_counts_per_report':dict(total),
            'counts_scope':'Only fixed decoder copies and first-success classical labels, conditional on supplied palette-index controls and computational-zero work.',
            'full_word_iterator':'reversible_selectors.selector_word(plan), each yielded gate is X/CX/CCX with integer wire indices; no data-dependent Python branch',
            'full_flat_gate_stream_materialized':False,
            'all_grammar_rows_emitted':True,'native_gate_word':False,
            'source_DAG_stack_interpreter_compiled':False,
            'fair_quantum_payload_router_compiled':False,
            'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'CIRCUIT_COMPILATION.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
