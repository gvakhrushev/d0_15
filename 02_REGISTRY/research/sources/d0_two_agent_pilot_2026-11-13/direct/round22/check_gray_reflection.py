#!/usr/bin/env python3
"""Exact Gray-cycle native columns plus independent large-power rectangles."""
from pathlib import Path
from collections import Counter
from math import isqrt
import hashlib,json
import gray_reflection as g
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def cs(n):
    c,s=one,zero
    for _ in range(n):c,s=add(ma(c),neg(mp(s))),add(mp(c),ma(s))
    return c,s
def run(word,state):
    for leaf in word:
        op=leaf['op'];w=leaf['wires'];out={}
        if op=='G':
            for x,v in state.items():
                bit=(x>>w[0])&1;base=x&~(1<<w[0]);a=neg(mp(v)) if bit else ma(v);b=ma(v) if bit else mp(v)
                out[base]=add(out.get(base,zero),a);j=base|(1<<w[0]);out[j]=add(out.get(j,zero),b)
        elif op=='CX':
            for x,v in state.items():j=x^(((x>>w[0])&1)<<w[1]);out[j]=add(out.get(j,zero),v)
        else:
            assert op=='SourceI'
            for x,v in state.items():
                bit=(x>>w[0])&1;parity=((x>>w[1])^(x>>w[2]))&1;j=x^(bit<<w[2]);out[j]=add(out.get(j,zero),neg(v) if bit and parity else v)
        state={x:v for x,v in out.items() if v!=zero}
    return state
def resource(tree,port):
    if tree['op']=='seq':
        out=Counter()
        for child in tree['children']:out.update(resource(child,port))
        return out
    if tree['op']=='repeat':return Counter({k:int(tree['count'])*v for k,v in resource(tree['child'],port).items()})
    if tree['op']=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
    return Counter({tree['op']:1})
reports=[]
for K in range(1,5):
    controls=list(range(K));aux=K;port=K+1;spin=(K+2,K+3);old=K+4
    for k in (1,2):
        forward=list(g.blocks(controls,aux,k,port,spin,(old,)));back=list(g.blocks(controls,aux,k,port,spin,(old,),1))
        assert back==[g.nb.inverse_literal(t,port,spin) for t in reversed(forward)]
        word=[x for t in forward for x in g.nb.expand(t,10000)];inverse=[x for t in back for x in g.nb.expand(t,10000)]
        assert len(word)==(1<<K)*(k+1)
        cc,ss=cs((1<<K)*k)
        for column in range(1<<(K+5)):
            active=(column&((1<<K)-1))==0
            expected={column:cc,column^(1<<aux):neg(ss) if (column>>aux)&1 else ss} if active else {column:one}
            actual=run(word,{column:one});assert actual==expected,(K,k,column)
            assert run(inverse,actual)=={column:one}
        for depth in range(3):
            count=Counter()
            for block in g.blocks(controls,aux,k,port,spin,(old,),depth):count.update(resource(block,port))
            assert +count==+g.counts(K,k,depth)
        reports.append({'K':K,'k':k,'all_exact_columns_and_inverses':1<<(K+5),'forward_leaves':len(word)})

# Binary-reflected Gray code is a bijection on all masks. Adjacent masks
# differ in bit ctz(i); its last mask is the last control, so closure is exact.
for K in range(1,13):
    parity=0;visited=[0]
    for i in range(1,1<<K):
        parity^=1<<((i&-i).bit_length()-1);assert parity==i^(i>>1);visited.append(parity)
    assert len(set(visited))==1<<K and parity==1<<(K-1)
    parity^=1<<(K-1);assert parity==0

cert=json.loads((P/'GRAY_REFLECTION_CERTIFICATE.json').read_text())
assert cert['source_sha256']==h(P/'certify_gray_reflection.py')
for p,digest in cert['input_sha256'].items():assert h(Path(p))==digest
# Independent outward rectangular arithmetic, not the builder's disk method.
bits=8448;S=1<<bits
def q(a,b=1):return a*S//b,-((-a*S)//b)
def sqrt(x):
    assert x[0]>=0;lo=isqrt(x[0]*S);z=x[1]*S;hi=isqrt(z);return lo,hi+(hi*hi<z)
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def minus(x,y):return x[0]-y[1],x[1]-y[0]
def product(x,y):
    v=[a*b for a in x for b in y];return min(v)>>bits,-((-max(v))>>bits)
root5=sqrt(q(5));p=((root5[0]-S)//2,-((-(root5[1]-S))//2));a=sqrt(p)
def cmul(x,y):return minus(product(x[0],y[0]),product(x[1],y[1])),plus(product(x[0],y[1]),product(x[1],y[0]))
def native_power(exponent):
    result=(q(1),q(0));base=(a,p)
    while exponent:
        if exponent&1:result=cmul(result,base)
        exponent>>=1
        if exponent:base=cmul(base,base)
    return result
independent=[]
for key,entry in cert['entries'].items():
    K=int(key);k=int(entry['k']);nc,ns=native_power((1<<K)*k);tc,ts=q(-1),q(0)
    error=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]))
    assert error<=S>>3264
    own=(nc,ns);shift=bits-entry['denominator_power_of_two']
    contained=True
    for small,big in zip((entry['native_cos_hex'],entry['native_sin_hex']),own):
        lo,hi=[int(z,16) for z in small]
        assert lo<<shift<=big[1] and big[0]<=hi<<shift
        contained=contained and lo<<shift<=big[0] and big[1]<=hi<<shift
    assert entry['forward_counts']=={k:str(v) for k,v in g.counts(K,k).items()}
    independent.append({'K':K,'rectangle_error_le':'2^-3264','rectangle_inside_saved_ball_projection':bool(contained)})
out={'status':'PASS_SCRATCH_FREE_GRAY_REFLECTION_NATIVE_AND_INTERVALS','certificate_sha256':h(P/'GRAY_REFLECTION_CERTIFICATE.json'),
     'checker_sha256':h(Path(__file__)),'exact_cases':reports,'all_exact_columns_and_literal_inverses':sum(r['all_exact_columns_and_inverses'] for r in reports),
     'Gray_cycle_enumerated_K1_through_K12':True,'general_Walsh_sum':'sum_s (-1)^(b dot s)=product_j(1+(-1)^b_j)=2^K if b=0 else0',
     'independent_rectangular_precision_bits':bits,'independent_actual_large_power_checks':independent,
     'native_aux_port_Spin_oldRIGHT_arbitrary':True,'new_clean_wires':0,'off_anchor_exact_identity':True,
     'forward_SourceI_calls':0,'forward_exact_involution_claimed':False,'same_paid_history_as_A13_claimed':False,
     'full_K8_or_K46_actual_huge_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'GRAY_REFLECTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'exact_columns_and_inverses':out['all_exact_columns_and_literal_inverses'],'new_clean_work':0}))
