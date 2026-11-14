#!/usr/bin/env python3
"""Bind the original B25 Julia SELECT to local SAM groups, not measured labels.

This is a target-sector catalogue. It does not emit the missing Julia word.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json
P=Path(__file__).resolve().parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
COORD_PATH=B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl'
ADDR_PATH=B/'round24/TORUS_CHOI_ADDRESSES.jsonl'
COORD=[json.loads(x) for x in COORD_PATH.read_text().splitlines()]
ADDR=[json.loads(x) for x in ADDR_PATH.read_text().splitlines()]
BANKS=('y+','y-','f','0','x+','x-','q')
def catalogue():
    assert len(COORD)==2688 and [r['sam_index'] for r in COORD]==list(range(2688))
    assert [r['a'] for r in ADDR]==list(range(2049))
    groups={}
    for i,row in enumerate(COORD):
        if row['kind']=='matter':continue
        key=(row['kind'],tuple(row['site']),row['role']);groups.setdefault(key,[]).append(i)
    out={}
    for bank in BANKS:
        rows=[]
        for address in ADDR:
            indices=[]
            if address['kind']!='identity_anchor':
                kind='coframe' if address['kind']=='inverse_coframe_column' else 'proper_link'
                if bank=='f' or bank=='q' and kind=='coframe':
                    indices=groups.get((kind,tuple(address['site']),address['direction']),[])
                    assert len(indices) in (0,4 if kind=='coframe' else 6)
            rows.append({**address,'SAM_indices':indices,'local_assignment_count':2**len(indices)})
        out[bank]=rows
    return out
def sectors(rows):
    for row in rows:
        for bits in product((0,1),repeat=len(row['SAM_indices'])):
            yield {**row,'SAM_pattern':list(bits),'address_pattern_little_endian':[(row['a']>>j)&1 for j in range(12)]}
def main():
    cat=catalogue();counts={}
    for bank,rows in cat.items():
        total=Counter()
        for row in rows:total[row['kind']]+=row['local_assignment_count']
        counts[bank]={'by_kind':dict(total),'all_sectors':sum(total.values())}
    assert counts['f']['all_sectors']==22017 and counts['q']['all_sectors']==5889
    assert sum(r['all_sectors'] for r in counts.values())==38151
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    out={'status':'EXACT_SOURCE_ADDRESS_AND_LOCAL_CONTROL_BINDING','source_sha256':h(Path(__file__)),
         'input_sha256':{str(p):h(p) for p in [COORD_PATH,ADDR_PATH,B/'round25/targets.py',B/'round25/precision_name.py']},
         'banks':cat,'counts':counts,'total_address_local_SAM_sectors':38151,
         'SAM_matter_bits_unused':128,'control_policy':'coherent address/SAM predicates; no measured classical field selection',
         'address0_target':'I32','padding_addresses_2049_through_4095_target':'I32 chosen for SELECT, zero ideal Omega amplitude',
         'generic_full_32_matrix_max_controls':23,'coframe_structured_max_controls':20,
         'coframe_structured_macro_bound_per_active_sector':26,'full_native_Julia_SELECT_compiled':False,
         'physical_C_closed':False,'GR_closed':False}
    (P/'JULIA_LOCAL_SECTORS.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({'status':out['status'],'counts':counts,'total':38151}))
if __name__=='__main__':main()
