#!/usr/bin/env python3
"""Source-exact Fourier table, actual compact native history and phase replay."""
from pathlib import Path
from collections import Counter
from itertools import zip_longest
from math import isqrt
import hashlib,json
import numpy as np
import car_vacuum_prefix as n
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plan=json.loads((P/'CAR_VACUUM_PREFIX_PLAN.json').read_text())
for path,digest in plan['source_sha256'].items():assert h(Path(path))==digest,path
x=n.inputs();lay=n.layout();n.validate(lay);cmds=list(n.commands(x['kappa'],lay,x['phase_k']));assert len(cmds)==318
assert sum(z['coefficient'] for z in cmds)==549
# Derive every original cos/sin value from the actual emitted bit/angle
# bindings, then compare to kappa dot x in the original site enumeration.
rows=[json.loads(s) for s in (n.B/'round21/ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
assert len(rows)==256
F=np.zeros((256,128),dtype=np.int64);quadrants=Counter();max_coeff=0
by_pair={j:[z for z in cmds if z['pair']==j] for j in range(64)}
for j in range(64):
    max_coeff=max(max_coeff,sum(z['coefficient'] for z in by_pair[j]))
    for site,row in enumerate(rows):
        coord=row['site'];assert site==sum(v*(4**(3-mu)) for mu,v in enumerate(coord))
        actual=sum(z['coefficient']*((site>>z['site_bit'])&1) for z in by_pair[j])%4
        expected=sum(a*b for a,b in zip(x['kappa'][j],coord))%4;assert actual==expected
        quadrants[actual]+=1;F[site,2*j]=(1,0,-1,0)[actual];F[site,2*j+1]=(0,1,0,-1)[actual]
assert max_coeff==18 and dict(quadrants)=={0:4096,1:4096,2:4096,3:4096}
assert np.array_equal(np.einsum('xr,xs->rs',F,F,optimize=False),128*np.eye(128,dtype=np.int64))
assert np.all(np.sum(F*F,axis=1)==64)
# These are exact integer proofs of uniform internal SITE and RIGHT Gram
# I/128; no external PF weight was inserted into the internal Fourier bank.

# Independent huge-power rectangular intervals, also checking coefficients
# 2 and3 directly rather than only relying on the telescoping inequality.
cert=json.loads((P/'FOURIER_PHASE_CERTIFICATE.json').read_text());assert cert['source_sha256']==h(P/'certify_fourier_phase.py')
for path,digest in cert['input_sha256'].items():assert h(Path(path))==digest
bits=8448;S=1<<bits
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    v=[i*j for i in a for j in b];return min(v)>>bits,-((-max(v))>>bits)
def cmul(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
root=isqrt(5*S*S);pp=((root-S)//2,-((-(root+1-S))//2));aa=(isqrt(pp[0]*S),isqrt(pp[1]*S)+1)
def power(k):
    ans=((S,S),(0,0));base=(aa,pp)
    while k:
        if k&1:ans=cmul(ans,base)
        k>>=1
        if k:base=cmul(base,base)
    return ans
phase_checks=[]
for a in (1,2,3):
    co,si=power(a*128*x['phase_k']);tc=(0,-1,0)[a-1]*S;ts=(1,0,-1)[a-1]*S
    err=max(abs(co[0]-tc),abs(co[1]-tc))+max(abs(si[0]-ts),abs(si[1]-ts));assert err<=a*(S>>3264)
    if a==1:
        shift=bits-cert['denominator_power_of_two']
        for saved,got in zip((cert['native_cos_hex'],cert['native_sin_hex']),(co,si)):
            lo,hi=[int(v,16) for v in saved];assert lo<<shift<=got[0] and got[1]<=hi<<shift
    phase_checks.append({'coefficient':a,'independent_error_le':str(a)+'*2^-3264'})

# Exhaust every actual compact native block with its real huge repeat count.
# Keep only hashes for inverse comparison; never expand those repeats.
protected=set(lay['SAM']+[lay['oldRIGHT_witness']]);forward=Counter();back=Counter();inverse_hashes=[];block_number=0
digest=lambda t:hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':')).encode()).hexdigest()
for tree in n.prefix_blocks(lay):
    n.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),(lay['oldRIGHT_witness'],))
    for leaf in n.nb.leaves(tree):assert not protected.intersection(leaf['wires'])
    forward.update(n.price(tree,lay['port']));inverse_hashes.append(digest(n.nb.inverse_literal(tree,lay['port'],tuple(lay['spin']))));block_number+=1
assert block_number==40742
for expected,tree in zip_longest(reversed(inverse_hashes),n.prefix_blocks(lay,depth=1)):
    assert expected is not None and tree is not None and expected==digest(tree);back.update(n.price(tree,lay['port']))
assert +back==+n.inverse_price(forward)
for name,value in [('prefix_forward',forward),('prefix_literal_inverse',back)]:
    assert +value==+n.inventory(lay)[name]
    assert all(value[k]==int(plan['native_inventories'][name][k]) for k in ('G_port','G_other','CX','SourceI'))

# The actual full 19-wire scheduling is retained in a bounded toy-angle
# instance; independently invert the complete emitted DAG at depths0..3.
fixture=[[0]*4 for _ in range(64)];fixture[0][3]=1;saved=n.inputs
toy_reports=[]
try:
    n.inputs=lambda:{'kappa':fixture,'boolean_k':1,'phase_k':1}
    literal=n.nb.seq(*n.prefix_blocks(lay))
    for depth in range(4):
        actual=(leaf for tree in n.prefix_blocks(lay,depth) for leaf in n.nb.expand(tree,2000000));count=0
        for left,right in zip_longest(actual,n.nb.expand(literal,2000000)):
            assert left==right,(depth,count);count+=1
        toy_reports.append({'inverse_depth':depth,'literal_primitive_leaves_equal':count})
        literal=n.nb.inverse_literal(literal,lay['port'],tuple(lay['spin']))
finally:n.inputs=saved

# Ideal forward preparation diagnostic on all 2^19 amplitudes. This uses
# exact quadrant rotations, not the huge native G powers whose norm bound
# was independently certified above.
state=np.zeros(1<<19);state[0]=1
def apply_rotation(q,co,si,controls=(),pattern=()):
    global state
    base=np.arange(1<<19,dtype=np.int64);mask=(base&(1<<q))==0
    for control,bit in zip(controls,pattern):mask&=((base>>control)&1)==bit
    a=base[mask];b=a|(1<<q);u=state[a].copy();v=state[b].copy();state[a]=co*u-si*v;state[b]=si*u+co*v
def apply_cx(control,target):
    global state
    index=np.arange(1<<19,dtype=np.int64);dest=index^(((index>>control)&1)<<target);new=np.empty_like(state);new[dest]=state;state=new
for q in list(range(8))+list(range(13,19)):apply_rotation(q,2**-.5,2**-.5)
p=(np.sqrt(5)-1)/2;apply_rotation(8,np.sqrt(p),p)
for q in (9,10,11):apply_cx(8,q)
state=state[np.arange(1<<19)^(1<<8)]
small={'internal_SITE':list(range(8)),'grade':list(range(8,12)),'RIGHT':list(range(12,19))}
for z in n.commands(x['kappa'],small,x['phase_k']):
    a=z['coefficient'];apply_rotation(12,(0,-1,0)[a-1],(1,0,-1)[a-1],z['controls'],z['pattern'])
m=np.zeros(16);m[1]=np.sqrt(p);m[14]=p;expected=np.einsum('rx,g->rgx',F.T/128,m,optimize=False).reshape(-1)
error=float(np.max(abs(state-expected)));assert error<5e-17 and abs(float(np.dot(state,state))-1)<5e-15
M,e=n.error_bound()
out={'status':'PASS_ORIGINAL_CAR_VACUUM_FOURIER_NATIVE_PREFIX','plan_sha256':h(P/'CAR_VACUUM_PREFIX_PLAN.json'),'checker_sha256':h(Path(__file__)),
     'original_site_pair_quadrants_checked':16384,'quadrant_counts':{str(k):quadrants[k] for k in range(4)},
     'exact_Fourier_Gram':'F^T F=128I','exact_internal_SITE_probability':'1/256','exact_RIGHT_Gram':'I/128',
     'all19_bit_ideal_output_amplitudes_checked':1<<19,'ideal_state_diagnostic_max_error':error,
     'native_phase_independent_precision':8448,'actual_phase_power_checks':phase_checks,
     'actual_compact_native_blocks_and_literal_inverses_checked':block_number,'huge_repeats_expanded':False,'literal_toy_depth_checks':toy_reports,
     'SAM_and_unknown_oldRIGHT_untouched_by_every_primitive':True,'extra_clean_work':0,
     'operator_error_to_declared_extension_lt':'2^-3259','all112_prefix_error_lt':'2^-3252',
     'marked_original_prefix_equivalence_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'CAR_VACUUM_PREFIX_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','actual_compact_native_blocks_and_literal_inverses_checked','all19_bit_ideal_output_amplitudes_checked')}))
