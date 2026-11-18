#!/usr/bin/env python3
"""Check actual global native bindings and independent inventory formulas."""
from itertools import islice
from pathlib import Path
import json
import source_dispatcher as s
P=Path(__file__).resolve().parent
t=json.loads((P/'SOURCE_DISPATCH_TABLES.json').read_text())
c=json.loads((P/'SOURCE_DISPATCH_COMPILATION.json').read_text())
angle=json.loads((P.parent/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k'])
checks=[]
for name,walk in c['walks'].items():
    size=walk['walk_logical_wire_count'];port=size;spin=(size+1,size+2);aux=size+3;old=size+4
    count=0;leaves=0
    for tree in islice(s.native_walk_macros(t,name,k),32):
        nb=s.sys.modules['a15_native_boolean']
        nb.validate_schema(tree,size+5,port,spin,(old,))
        for leaf in nb.leaves(tree):
            leaves+=1;op=leaf['op'];w=leaf['wires']
            assert old not in w
            if op=='SourceI':assert w==[port,*spin]
            if op=='G':assert w[0] not in range(8)
            if op=='CX':assert w[1] not in range(8)
        nb.validate_schema(nb.inverse_literal(tree,port,spin),size+5,port,spin,(old,))
        count+=1
    checks.append({'root':name,'actual_chronological_native_macro_bindings':count,'syntactic_leaves_checked':leaves,'logical_wires':size,'native_wires':size+5})
v=c['ten_sign_report_controller_counts'];x,cx,cc=v['X'],v['CX'],v['CCX']
forward={'G':(4*x+12*cc)*k,'CX':cx+6*x+68*cc,'SourceI':2*x+24*cc}
reverse={'G':(4*x+12*cc)*k,'CX':cx+(24*k+6)*x+(36*k+68)*cc,'SourceI':(16*k+6)*x+(48*k+72)*cc}
assert {g:str(n) for g,n in forward.items()}==c['native_forward_inventory_per_report']
assert {g:str(n) for g,n in reverse.items()}==c['native_literal_reverse_inventory_per_report']
assert 7*(x+cc)<2**36
out={'status':'PASS_ACTUAL_GLOBAL_NATIVE_BINDINGS_AND_COUNTS','input_sha256':{n:s.digest(P/n) for n in ['source_dispatcher.py','SOURCE_DISPATCH_TABLES.json','SOURCE_DISPATCH_COMPILATION.json']},
     'bindings':checks,'full_word_executed':False,'seven_report_controller_error_strictly_below':'2^-4060',
     'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'NATIVE_DISPATCH_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'actual_macro_bindings':sum(x['actual_chronological_native_macro_bindings'] for x in checks)}))
