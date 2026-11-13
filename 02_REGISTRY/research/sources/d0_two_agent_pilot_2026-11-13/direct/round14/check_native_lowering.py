#!/usr/bin/env python3
"""Check native substitution wiring on actual logical streams and all totals."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import islice
from math import isqrt
import hashlib,json
import native_boolean as nb
import lower_native_selectors as lower
P=Path(__file__).resolve().parent;A13=P.parent/'round13'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
angle=json.loads((P/'NATIVE_BOOLEAN_ANGLE.json').read_text());cert=angle['certificate'];k=int(angle['k']);bits=cert['certified_error_bits']
# Recalculate the final norm inequalities from saved outward integer endpoints;
# the owning interval routine supplies the enclosures, independently replayed
# in B30. This is not a second power-enclosure computation.
bounds={}
for multiple,row in cert['rotation_enclosures'].items():
    multiple=int(multiple);scale=2**row['denominator_power_of_two'];c=[int(v,16) for v in row['cosine_endpoints_hex']];s=[int(v,16) for v in row['sine_endpoints_hex']]
    assert -scale<=c[0]<=c[1]<=scale and -scale<=s[0]<=s[1]<=scale
    if multiple==2:
        a=isqrt(scale*scale//2);wanted_c=wanted_s=(a,a+1)
    elif multiple==4:wanted_c=(0,0);wanted_s=(scale,scale)
    else:assert multiple==8;wanted_c=(-scale,-scale);wanted_s=(0,0)
    numerator=max(abs(c[0]-wanted_c[1]),abs(c[1]-wanted_c[0]))+max(abs(s[0]-wanted_s[1]),abs(s[1]-wanted_s[0]))
    bounds[multiple]=F(numerator,scale);assert bounds[multiple]==F(row['operator_error_L1_upper'])
assert bounds[2]==F(cert['H_error_upper']) and bounds[4]==F(cert['X_error_upper'])
assert bounds[4]+bounds[8]==F(cert['CCX_error_upper'])
assert max(bounds[2],bounds[4]+bounds[8])<=F(1,2**bits)

manifest=json.loads((P/'NATIVE_SELECTOR_LOWERING.json').read_text())
assert manifest['native_macro_source_sha256']==sha(P/'native_boolean.py')
assert manifest['angle_certificate_sha256']==sha(P/'NATIVE_BOOLEAN_ANGLE.json')
assert manifest['native_library_sha256']==sha(P/'NATIVE_BOOLEAN_LIBRARY.json')
library=json.loads((P/'NATIVE_BOOLEAN_LIBRARY.json').read_text())
checked=0;schemas=[]
for row in manifest['circuits']:
    path=A13/row['logical_circuit_file'];assert sha(path)==row['logical_circuit_sha256']
    circuit=json.loads(path.read_text());key=row['circuit_dictionary_key']
    if key:circuit=circuit[key]
    N=circuit['wire_count'];port=N;spin=(N+1,N+2);aux=N+3;old=(N+4,)
    assert row['native_wire_count']==N+5 and row['port']==port and row['spin']==list(spin) and row['arbitrary_aux']==aux
    inputs=set(sum((circuit['layout'][name] for name in row['read_only_input_groups']),[]))
    words=lower.logical.first_success_word(circuit) if key else islice(lower.logical.selector_word(circuit),64)
    for gate in words:
        tree=lower.lower_gate(gate,k,port,spin,aux)
        nb.validate_schema(tree,N+5,port,spin,old)
        for leaf in nb.leaves(tree):
            op,w=leaf['op'],leaf['wires']
            assert not(op=='G' and w[0] in inputs)
            assert not(op=='CX' and w[1] in inputs)
            if op=='SourceI':assert not set(w).intersection(inputs)
        # A small expansion verifies the emitted DAG count formula without
        # attempting the astronomical certified-k native word.
        small=lower.lower_gate(gate,1,port,spin,aux)
        actual=Counter(g['op'] for g in nb.expand(small,1000))
        assert dict(actual)==nb.counts(small)
        checked+=1
    counts=circuit['terminal_gate_counts'];nx,nt,nc=counts['X'],counts['CCX'],counts['CX']
    expected={'G':(4*nx+12*nt)*k,'SourceI':2*nx+24*nt,'CX':6*nx+68*nt+nc}
    reverse={'G':expected['G'],'SourceI':(16*nx+48*nt)*k+6*nx+72*nt,
             'CX':(24*nx+36*nt)*k+6*nx+68*nt+nc}
    assert expected=={op:int(value) for op,value in row['native_forward_inventory'].items()}
    assert reverse=={op:int(value) for op,value in row['native_literal_raw_reverse_inventory'].items()}
    assert F(row['error_upper'])==F(nx+nt,2**bits)
    schemas.append({'file':row['logical_circuit_file'],'key':key,'native_wires':N+5})
known=manifest['known_seven_report_approximate_macro_occurrences']
assert known==92263351768 and known<2**37
assert F(manifest['known_seven_report_error_upper'])==F(known,2**bits)<F(1,2**(bits-37))
result={'status':'PASS_NATIVE_SELECTOR_SUBSTITUTION_AND_ERROR_TOTALS',
        'actual_logical_macro_wirings_checked':checked,'schemas':schemas,
        'norm_enclosure_arithmetic_checked':True,'integer_power_enclosure_rerun_here':False,
        'all_actual_lowered_native_stream_expanded':False,
        'full_coverage_method':'A13 whole logical stream already audited; typewise native substitution preserves distinctness/read-only plus fresh disjoint aux/port/spin. Actual samples and complete first-success streams checked.',
        'native_lowering_sha256':sha(P/'NATIVE_SELECTOR_LOWERING.json'),
        'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'NATIVE_LOWERING_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
