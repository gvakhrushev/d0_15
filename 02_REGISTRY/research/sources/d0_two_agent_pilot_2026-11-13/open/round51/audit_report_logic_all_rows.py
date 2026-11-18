#!/usr/bin/env python3
"""Exhaust each owned finite selector/lookup row independently, never whole word."""
from pathlib import Path
from itertools import zip_longest
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import reversible_report_stream as r
s=r.s;d=r.d;logic=r.logic;h=lambda f:sha256(f.read_bytes()).hexdigest();files=[D/'round25/reversible_report_stream.py',D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round13/reversible_selectors.py'];pins={str(p):h(p) for p in files}
selectors={}
for file in ('TOP_SOURCE_SELECTOR_CIRCUIT.json','INTERNAL_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json'):
 pth=D/'round13'/file;p=json.loads(pth.read_text());pins[str(pth)]=h(pth);prefix=list(logic.prefix_word(p));assert list(r.prefix_word(p))==prefix and list(r.prefix_word(p,True))==prefix[::-1]
 total=0;multi=0;max_row=0
 for row in p['rows']:
  original=list(logic.row_word(p,row));assert list(r.row_word(p,row))==original and list(r.row_word(p,row,True))==original[::-1]
  total+=len(original);max_row=max(max_row,len(original));multi+=sum(1 for threshold,mask in row['boundaries'] if bin(mask).count('1')>1)
 selectors[file]={'all_rows':len(p['rows']),'total_owned_row_tuples':total,'max_tuples_one_row':max_row,'multi_output_boundaries':multi,'prefix_tuples':len(prefix)}
 print(json.dumps({'checked_selector':file,**selectors[file]}),flush=True)
tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());plan=d.step_plan(11);q=plan['layout'];fields=d.split_wires(q['transition'],d.TRANS_WIDTHS);leaf=fields[2];rec=d.split_wires(q['record'],plan['record_widths'])
lookup_specs={'transition_rows':(q['old_stack'][0][:15]+q['choice']+q['ready'],q['transition']),'palette_rows':(q['old_stack'][0][:15],q['palette']),'address_rows':(q['site']+leaf,sum(rec[4:],[]))};lookups={}
for name,(controls,outputs) in lookup_specs.items():
 rows=tables[name];multi=0;count=0;maxrow=0;nonzero=0
 for row in rows:
  original=list(d.lookup_word([row],controls,outputs,q['flag'][0],q['pattern_work']));forward=list(r.lookup_word([row],controls,outputs,q['flag'][0],q['pattern_work']));back=list(r.lookup_word([row],controls,outputs,q['flag'][0],q['pattern_work'],True))
  assert forward==original and back==original[::-1],(name,row);count+=len(original);maxrow=max(maxrow,len(original));nonzero+=bool(row[2]);multi+=bin(row[2]).count('1')>1
 lookups[name]={'all_rows':len(rows),'nonzero_rows':nonzero,'multi_output_rows':multi,'total_owned_tuples':count,'max_tuples_one_row':maxrow}
 print(json.dumps({'checked_lookup':name,**lookups[name]}),flush=True)
# In the real A15 transition tail, rows are reversed but OUTPUT CX are still
# ascending. Verify the branch which does not equal reversal of a whole row.
row=next(z for z in tables['transition_rows'] if bin(z[2]).count('1')>1);controls,outputs=lookup_specs['transition_rows'];owned_tail=list(d.lookup_word(reversed([row]),controls,outputs,q['flag'][0],q['pattern_work']));candidate=list(r.lookup_word([row],controls,outputs,q['flag'][0],q['pattern_work'],False,True));assert candidate==owned_tail
inverse_tail=list(r.lookup_word([row],controls,outputs,q['flag'][0],q['pattern_work'],True,True));assert inverse_tail==owned_tail[::-1] and inverse_tail!=owned_tail
for pth,digest in pins.items():assert h(Path(pth))==digest,pth
out={'status':'PASS_EXHAUSTIVE_A13_A15_FINITE_ROW_REVERSALS','source_sha256':pins,'A13_selectors':selectors,'A15_lookups':lookups,'actual_transition_tail_ascending_output_and_inverse_descending':True,'row_memory_bound':'one original logical row plus one candidate and reverse; complete giant word is not materialized','native_leaves_or_giant_G_powers_executed':False,'physical_C_or_T6_proved':False,'GR_closed':False}
(P/'A13_A15_ALL_ROWS_REVERSE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'selector_rows':sum(x['all_rows'] for x in selectors.values()),'lookup_rows':sum(x['all_rows'] for x in lookups.values())}),flush=True)
