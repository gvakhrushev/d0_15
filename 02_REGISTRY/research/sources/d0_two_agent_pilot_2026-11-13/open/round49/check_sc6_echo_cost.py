#!/usr/bin/env python3
"""Count owner's complete T,Z,T* and true leafwise alternative separately."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
P=Path(__file__).resolve().parent;O=P.parent;root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13');domain=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('b49_echo_nt',domain);n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
def read(filename):return tuple(n.Gate(g['op'],tuple(g['wires'])) for g in map(json.loads,(O/'round21'/filename).read_text().splitlines()))
v=read('SC6_FORWARD.jsonl');vi=read('SC6_INVERSE.jsonl');source=n.Gate('SourceI',(19,20,21));gate=n.Gate('G',(19,));conversion=(source,source,gate,source,source);t=conversion+v
x=n.Execution(23,(),(22,),t,n.G_CX_SOURCE_I,19,(20,21));raw=n.inverse_word(x,max_qubits=23,max_expanded_stages=100000);owned=vi+(gate,);central=(source,source)
def inventory(z):return dict(Counter(g.op for g in z))
assert len(t)==18181 and len(owned)==18177 and len(raw)==58129
assert len(t+central+owned)==36360 and len(t+central+raw)==76312
assert inventory(raw)=={'G':5889,'CX':4096,'SourceI':48144}
# Owner's R loaders: 14 forward and 14 reverse, each L+16.
assert 36360+28*16==36808
out={'status':'PASS_SC6_FULL_ECHO_HISTORY_COSTS','forward_T':{'calls':len(t),'counts':inventory(t)},'owner_grouped_T_inverse':{'calls':len(owned),'counts':inventory(owned)},'leafwise_T_inverse':{'calls':len(raw),'counts':inventory(raw)},'central_Z':{'calls':len(central),'counts':inventory(central)},'T_Z_Tinverse_owner_grouped_calls':len(t+central+owned),'T_Z_Tinverse_leafwise_calls':len(t+central+raw),'SC8_owner_R_T_Z_Tinverse_Rinverse':'36808 + 28 L, assuming 28 scalar loaders each cost L+16, not full H1 banks','owner_and_leafwise_histories_identical':False,'global_H1_clock_and_marks_proved':False,'GR_closed':False}
(P/'SC6_FULL_ECHO_COST_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'owner_echo':36360,'leafwise_echo':76312}))
