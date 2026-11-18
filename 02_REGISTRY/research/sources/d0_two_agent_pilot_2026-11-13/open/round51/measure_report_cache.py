#!/usr/bin/env python3
"""Measure actual cached event structures; fixed instance, not a complexity theorem."""
from pathlib import Path
from hashlib import sha256
import resource,json,sys,time
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import reversible_report_stream as r
p=D/'round25/reversible_report_stream.py';pin=sha256(p.read_bytes()).hexdigest()
def rss_bytes():
 x=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 return int(x if sys.platform=='darwin' else 1024*x)
base=rss_bytes();rows=[]
for name in ('H_f_before_inverse_PF','H_q_before_inverse_PF'):
 t=time.monotonic();v=r.walk_structure(name);events=v[1];maps=sum(len(e['map']) for e in events if 'map' in e);record=len(v[2]);rows.append({'root':name,'events_retained':len(events),'map_entries_retained':maps,'records_retained':record,'wall_seconds':round(time.monotonic()-t,3),'process_peak_rss_bytes_after_cache':rss_bytes()})
assert r.walk_structure.cache_info().currsize==2;assert sha256(p.read_bytes()).hexdigest()==pin
out={'status':'MEASURED_REPORT_EVENT_CACHE_NOT_ONE_EVENT','input_sha256':pin,'platform':sys.platform,'process_peak_rss_bytes_before':base,'after_cache':rows,'cache_entries':r.walk_structure.cache_info().currsize,'scope':'One cold local process, includes Python, imports, tables, two retained event sequences, records and instruction plan; ru_maxrss is an OS high-water mark, not exact retained heap or a portable peak guarantee.','memory_depends_on_event_maps_and_fixed_tables':True,'whole_expanded_native_word_in_memory':False,'GR_closed':False}
(P/'REPORT_CACHE_MEASUREMENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
