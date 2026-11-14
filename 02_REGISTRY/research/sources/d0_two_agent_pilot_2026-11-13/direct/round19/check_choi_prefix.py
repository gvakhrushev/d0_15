#!/usr/bin/env python3
"""Exact native macro columns, literal inverses and concrete prefix bindings.

Small powers are expanded in Q(a), a^4+a^2-1=0, with the actual
SourceI Spin diag(J,-J). Huge powers are checked by their interval receipt.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib,json
import numpy as np
import choi_prefix as c
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def mul(x,y):
    z=[0]*7
    for i,a in enumerate(x):
        for j,b in enumerate(y):z[i+j]+=a*b
    for d in range(6,3,-1):z[d-4]+=z[d];z[d-2]-=z[d]
    return tuple(z[:4])
def cs(n):
    x,y=one,zero
    for _ in range(n):x,y=add(ma(x),neg(mp(y))),add(mp(x),ma(y))
    return x,y
def rotate(state,w,co,si):
    out={}
    for x,v in state.items():
        for dest,weight in [(x,co),(x^(1<<w),neg(si) if (x>>w)&1 else si)]:
            out[dest]=add(out.get(dest,zero),mul(v,weight))
    return {x:v for x,v in out.items() if v!=zero}
def run(word,state):
    for op,*w in word:
        out={}
        if op=='G':
            for x,z in state.items():
                bit=(x>>w[0])&1;base=x&~(1<<w[0]);v=neg(mp(z)) if bit else ma(z);u=ma(z) if bit else mp(z)
                out[base]=add(out.get(base,zero),v);j=base|(1<<w[0]);out[j]=add(out.get(j,zero),u)
        elif op=='CX':
            for x,z in state.items():
                j=x^(((x>>w[0])&1)<<w[1]);out[j]=add(out.get(j,zero),z)
        else:
            assert op=='SourceI'
            for x,z in state.items():
                bit=(x>>w[0])&1;parity=((x>>w[1])^(x>>w[2]))&1
                j=x^(bit<<w[2]);out[j]=add(out.get(j,zero),neg(z) if bit and parity else z)
        state={x:v for x,v in out.items() if v!=zero}
    return state

cert=json.loads((P/'CHOI_PREFIX_CERTIFICATE.json').read_text());plan=json.loads((P/'CHOI_PREFIX_PLAN.json').read_text())
for f,digest in cert['input_sha256'].items():assert h(Path(f))==digest
assert h(P/'certify_choi_prefix.py')==cert['source_sha256']
assert plan['certificate_sha256']==h(P/'CHOI_PREFIX_CERTIFICATE.json')
assert plan['actual_native_resources']==c.inventory(cert)
reports=[];small={'boolean_common_power':{'k':'1'},'address_power':{'k':'1'}}
for op in ('H','X','address_rotation'):
    for K in (range(3) if op!='address_rotation' else range(2)):
        for pattern in product((0,1),repeat=K):
            lay={'aux_arbitrary':K+1,'port':K+2,'spin':[K+3,K+4]};old=K+5;N=old+1
            inst={'op':op,'controls':list(range(K)),'pattern':list(pattern),'target':K}
            tree=c.lower(inst,small,lay);back=c.nb.inverse_literal(tree,lay['port'],tuple(lay['spin']))
            c.nb.validate_schema(tree,N,lay['port'],tuple(lay['spin']),(old,))
            word=[(g['op'],*g['wires']) for g in c.nb.expand(tree,10000)]
            inv=[(g['op'],*g['wires']) for g in c.nb.expand(back,10000)]
            for col in range(1<<N):
                state={col:one};active=all(((col>>j)&1)==b for j,b in enumerate(pattern))
                if active:
                    if op!='address_rotation' and ((col>>K)&1):state=rotate(state,K+1,*cs(16))
                    state=rotate(state,K,*cs(2 if op=='address_rotation' else 4 if op=='H' else 8))
                actual=run(word,{col:one});assert actual==state,(op,K,pattern,col)
                assert run(inv,actual)=={col:one},(op,K,pattern,col,'inverse')
            reports.append({'op':op,'K':K,'pattern':pattern,'all_columns':1<<N,'forward_leaves':len(word),'literal_inverse_leaves':len(inv)})
        print('exact native prefix macro',op,'K',K,'passed',flush=True)

# Final enormous DAGs remain finite, contain only native leaves, protect SAM,
# branch controls and oldRIGHT, and retain literal paid inverse resources.
lay=c.layout();leaves=0
for controlled in (False,True):
    insts=list(c.instructions(lay,controlled));forward=list(c.prefix_blocks(cert,lay,controlled));reverse=list(c.prefix_blocks(cert,lay,controlled,True))
    assert len(insts)==len(forward)==len(reverse)==22
    for inst,tree in zip(insts,forward):
        c.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),tuple(lay['SAM']+[lay['oldRIGHT_witness']]))
        for leaf in c.nb.leaves(tree):
            if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in inst['controls']
            leaves+=1
    for f,r in zip(reversed(forward),reverse):assert r==c.nb.inverse_literal(f,lay['port'],tuple(lay['spin']))

# Diagnostic of the intended ideal address circuit, including all padding.
address=np.zeros(4096);address[0]=np.sqrt(2048/2049);address[2048]=1/np.sqrt(2049)
for target in range(11):
    new=address.copy()
    for x in range(2048):
        if (x>>target)&1:continue
        y=x|(1<<target);new[x]=(address[x]+address[y])/np.sqrt(2);new[y]=(address[x]-address[y])/np.sqrt(2)
    address=new
assert np.max(np.abs(address[:2049]-1/np.sqrt(2049)))<3e-17
assert np.count_nonzero(address[2049:])==0
bell=np.zeros((32,32));np.fill_diagonal(bell,1/np.sqrt(32))
assert np.max(np.abs(np.sum(bell*bell,axis=0)-1/32))<1e-17
assert Counter(i['op'] for i in plan['logical_schedule'])=={'address_rotation':1,'H':16,'X':5}
precision=cert['precision_bits'];e=cert['boolean_common_power']['enclosures'];errs={}
for mult,entry in [*e.items(),('address',cert['address_power']['enclosure'])]:
    intervals={key:[int(v,16) for v in entry[key]] for key in ['native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex']}
    nc,ns,tc,ts=[intervals[k] for k in ['native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex']]
    err=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]))
    assert err==int(entry['error_L1_numerator_hex'],16);errs[mult]=err
assert errs['4']+errs['16']<=1<<(precision-4096)
assert errs['8']+errs['16']<=1<<(precision-4096)
bound=errs['address']+16*(errs['4']+errs['16'])+5*(errs['8']+errs['16'])
assert bound==int(cert['prefix_error_L1_numerator_hex'],16) and bound<1<<(precision-4091)
out={'status':'PASS_NATIVE_CHOI_ADDRESS_BELL_PREFIX','certificate_sha256':h(P/'CHOI_PREFIX_CERTIFICATE.json'),
     'checker_sha256':h(Path(__file__)),'exact_small_power_cases':reports,'all_exact_columns':sum(r['all_columns'] for r in reports),
     'all_exact_literal_inverse_cases':sum(r['all_columns'] for r in reports),'actual_large_DAG_syntactic_leaves':leaves,
     'actual_SourceI_spin':'diag(J,-J)','uniform_prefix_error_lt':'2^-4091','private_clean_work':0,
     'arbitrary_aux_port_spin_and_external_entanglement':True,'padded_addresses_in_ideal_preparation_exact_zero':True,
     'full_huge_word_expanded':False,'Julia_SELECT_compiled':False,'full_Omega_preparation_compiled':False,
     'physical_C_closed':False,'GR_closed':False}
(P/'CHOI_PREFIX_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','all_exact_columns','uniform_prefix_error_lt']}))
