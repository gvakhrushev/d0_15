#!/usr/bin/env python3
"""Stream actual H.1-owned comparator and original n20/L4 PF addresses.

This emits exact components, NOT a complete H.1 geometric bank or mark ledger.
The 23-wire map is the owner's local comparator interface, not the global H.1
register allocation. No scalar loader is substituted for the seven banks.
"""
from collections import Counter
from fractions import Fraction
from math import isqrt
from pathlib import Path
import hashlib,importlib.util,json,sys
import mpmath as mp
import numpy as np

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent
native=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('h1_native',native)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
PORT,SPIN,OLD=19,(20,21),22
terms=[(1,0,2),(1,1,3),(-1,0,3),(-1,1,2),
       (1,4,6),(1,5,3),(-1,4,3),(-1,5,6)]
selectors=[w for w in range(32) if bin(w).count('1')==2][:8]
gate=lambda op,*w:nt.Gate(op,tuple(w))

def rotation(k):
    if k>=0: return [gate('G',PORT)]*k
    z=[gate('SourceI',PORT,*SPIN)]*2
    return z+[gate('G',PORT)]*(-k)+z

def fwt(values):
    a=values[:];step=1
    while step<len(a):
        for start in range(0,len(a),2*step):
            for j in range(step):
                x,y=a[start+j],a[start+j+step]
                a[start+j],a[start+j+step]=x+y,x-y
        step*=2
    return a

forward=[];blocks=[];term_rows=[]
gray=[j^(j>>1) for j in range(512)]
for selected,(sign,ia,ib) in zip(selectors,terms):
    wires=list(range(5))+[5+2*ia,6+2*ia,5+2*ib,6+2*ib]
    vals=[int((b>>4)==selected and (((b&15)==15) if sign==1 else ((b&15)!=15))) for b in range(512)]
    spectrum=fwt(vals)
    local=[]
    for j,g in enumerate(gray):
        c=spectrum[g];bit=(g^gray[(j+1)%512]).bit_length()-1
        control=wires[8-bit];local+=rotation(c)+[gate('CX',control,PORT)]
        blocks.append((c,control))
    # Independently read the literal word on all 512 control columns,
    # tracking X/Z signs of the port plus the Spin-central sign.
    address=np.arange(512,dtype=np.int64);angle=np.zeros(512,dtype=np.int64)
    xb=np.zeros(512,dtype=np.int64);zb=xb.copy();sgn=np.ones(512,dtype=np.int64)
    i=0
    while i<len(local):
        g=local[i]
        if g.op=='G': angle+=1;i+=1
        elif g.op=='CX':
            bit=(address>>(8-wires.index(g.wires[0])))&1
            angle*=1-2*bit;xb^=bit;i+=1
        else:
            assert local[i+1]==g
            angle=-angle;sgn*=1-2*xb;zb^=1;i+=2
    assert np.array_equal(angle,512*np.array(vals)) and not xb.any() and not zb.any() and np.all(sgn==1)
    forward+=local
    term_rows.append({'selector':format(selected,'05b'),'sign':sign,'calls':[ia,ib],
                      'control_addresses':wires,'truth_table_size':512})
inverse=[]
for c,control in reversed(blocks):inverse+=[gate('CX',control,PORT)]+rotation(-c)
want=Counter({'G':5888,'CX':4096,'SourceI':8192})
assert Counter(x.op for x in forward)==want==Counter(x.op for x in inverse)
for word in (forward,inverse):
    layout=nt.Execution(23,(),(OLD,),tuple(word),nt.G_CX_SOURCE_I,PORT,SPIN)
    nt.validate_execution(layout,max_qubits=23,max_expanded_stages=len(word))

def write_gates(name,word):
    with (HERE/name).open('w') as out:
        for g in word:out.write(json.dumps({'op':g.op,'wires':g.wires},separators=(',',':'))+'\n')
write_gates('SC6_FORWARD.jsonl',forward)
write_gates('SC6_INVERSE.jsonl',inverse)

# Original n=20 cost words on L=4 Role cells; exact Q(p) box arithmetic.
# p lies strictly between p_lo and p_hi by integer-square-root certification.
N=10**35;root=isqrt(5*N*N);den=2*N
plo,phi=root-N,root+1-N
add=lambda x,y:(x[0]+y[0],x[1]+y[1])
mul_p=lambda x:(x[1],x[0]-x[1])
mul_p2=lambda x:(x[0]-x[1],2*x[1]-x[0])
def cell(left,width):
    aa=2*left[0]+width[0];bb=2*left[1]+width[1]
    lo=2*(aa*den+bb*(plo if bb>=0 else phi))
    hi=2*(aa*den+bb*(phi if bb>=0 else plo))
    assert lo//den==hi//den and 0<=lo//den<4
    return lo//den

counts=Counter();leaves=0
with (HERE/'ORIGINAL_F_R_N20_L4.jsonl').open('w') as out:
    def visit(rem,axis,left,width,path):
        global leaves
        if rem==0:
            site=tuple(cell(left[i],width[i]) for i in range(4));counts[site]+=1;leaves+=1
            out.write(json.dumps({'word':path,'site':site},separators=(',',':'))+'\n');return
        q=axis%4; wf=width.copy();wf[q]=mul_p(wf[q])
        visit(rem-1,axis+1,left,wf,path+'F')
        if rem>=2:
            lr=left.copy();lr[q]=add(lr[q],mul_p(width[q]))
            wr=width.copy();wr[q]=mul_p2(wr[q])
            visit(rem-2,axis+1,lr,wr,path+'R')
    visit(20,0,[(0,0)]*4,[(1,0)]*4,'')
assert leaves==10946 and len(counts)==256 and min(counts.values())>0
owner=ROOT/'02_REGISTRY/gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/check_balanced_native_source.py'
spc=importlib.util.spec_from_file_location('original_pf',owner)
mod=importlib.util.module_from_spec(spc);spc.loader.exec_module(mod)
assert counts==mod.original_cost_words(20,4)
with (HERE/'ORIGINAL_PF_N20_L4.jsonl').open('w') as out:
    for site,n in sorted(counts.items()):
        rho=Fraction(256*n,10946)
        out.write(json.dumps({'site':site,'N':n,'rho_numerator':rho.numerator,'rho_denominator':rho.denominator},separators=(',',':'))+'\n')

# Only the original reference calibration, explicitly not the s>0 H.1 mean.
mp.mp.dps=80;p=(mp.sqrt(5)-1)/2;alpha=mp.sqrt(p)
kappa=mp.sin(512*mp.atan2(p,alpha))**2
Qref=4*kappa*p**7;qref=p**2+p**3*Qref
mp.iv.dps=90;iv=mp.iv;pi=(iv.sqrt(5)-1)/2;ai=iv.sqrt(pi)
re,im,cr,ci,n=iv.mpf(1),iv.mpf(0),ai,pi,512
while n:
    if n&1:re,im=re*cr-im*ci,re*ci+im*cr
    cr,ci=cr*cr-ci*ci,2*cr*ci;n//=2
ki=im*im;Qi=4*ki*pi**7;qi=pi**2+pi**3*Qi
assert ki>iv.mpf('0.93793197770933667') and ki<iv.mpf('0.93793197770933668')
files=['SC6_FORWARD.jsonl','SC6_INVERSE.jsonl','ORIGINAL_F_R_N20_L4.jsonl','ORIGINAL_PF_N20_L4.jsonl']
result={'status':'PARTIAL_H1_EXACT_OWNED_COMPONENTS',
        'comparator':{'interface_width':23,'port':PORT,'spin':SPIN,'oldright':OLD,'terms':term_rows,
                      'forward_calls':len(forward),'inverse_calls':len(inverse),'counts':dict(want),
                      'per_term_all_column_controls_checked':512},
        'original_site_addresses':{'L':4,'n':20,'actual_cost_words':leaves,'sites':len(counts),
                                  'min_count':min(counts.values()),'max_count':max(counts.values()),
                                  'all_box_cell_decisions_certified_by_rational_root_interval':True},
        'reference_only':{'kappa_512':mp.nstr(kappa,45),'Q_ref_zero_Xi':mp.nstr(Qref,45),
                          'noisy_q_ref_zero_Xi':mp.nstr(qref,45),
                          'kappa_outward_interval':str(ki),'Q_ref_outward_interval':str(Qi),
                          'noisy_q_ref_outward_interval':str(qi),
                          'is_full_interior_sampler_q':False},
        'not_emitted':['full geometric banks','SITE/SAM compiler','complete H1 mark-address/future-reader/seal ledger',
                       'full real READY factory','calibrated positive-s H1 q and source','full H1 word'],
        'GR_closed':False,
        'sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files}}
(HERE/'COMPONENT_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('sha256','comparator')},ensure_ascii=False))
