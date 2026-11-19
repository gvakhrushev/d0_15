"""Actual L=4 Fourier/CAR reference + native neighbor comparator NC1.

Factory scalar-effect hypotheses are those of the published native interface;
this checker does not simulate its complete microscopic stopped clock.
"""
from collections import Counter
from itertools import product
import json
import math
import numpy as np
import mpmath as mp
from check_native_neighbor_phase_oracle import program
from check_fourier_fresh_localization import original_reference


def need(x,msg):
    if not x: raise AssertionError(msg)


def prefix(r):
    ops=program(r)
    i=ops.index(('ccx','a5','d7','a6'))
    return ops[:i+1]


def check_comparator(r):
    xy=np.arange(256*256,dtype=np.uint32);x=xy>>8;y=xy&255
    bits={f'x{i}':((x>>i)&1).astype(np.uint8) for i in range(8)}
    bits.update({f'y{i}':((y>>i)&1).astype(np.uint8) for i in range(8)})
    bits.update({f'{a}{i}':np.zeros(len(xy),dtype=np.uint8)
                 for a,n in [('t',8),('d',8),('a',7)] for i in range(n)})
    bits['z']=np.ones(len(xy),dtype=np.uint8)
    def apply(op):
        if op[0]=='cx':bits[op[2]]^=bits[op[1]]
        else:bits[op[3]]^=bits[op[1]]&bits[op[2]]
    ops=prefix(r)
    for op in ops:apply(op)
    flag=bits['a6'].copy();exp=x.copy()
    if r is not None:
      sh=2*r;exp=(x&~(np.uint32(3)<<np.uint32(sh)))|((((x>>sh)&3)+1 & 3)<<sh)
    need(np.array_equal(flag,(y==exp).astype(np.uint8)),'actual equality flag all columns')
    for op in reversed(ops):apply(op)
    for nm,k in [('t',8),('d',8),('a',7)]:
      for i in range(k):need(not bits[f'{nm}{i}'].any(),'all 23 scratch zero')
    need(all(np.array_equal(bits[f'x{i}'],(x>>i)&1) for i in range(8)),'SITE preserved')
    need(all(np.array_equal(bits[f'y{i}'],(y>>i)&1) for i in range(8)),'Y preserved')
    count=Counter(x[0] for x in ops)
    need(count['ccx']==7 and count['cx']==(32 if r is None else 34),'exact prefix word')
    return {'XY_columns':len(xy),'equality_columns':int(flag.sum()),
            'compute_and_uncompute_Toffoli':14,'compute_and_uncompute_CX':2*count['cx'],
            'NC1_extra_birth_G_CX':[1,1,2]}


def main():
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p);G=np.array([[a,-p],[p,a]]);v=np.array([a,p])
    CX=np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,0.,1.],[0.,0.,1.,0.]])
    U=np.einsum('ij,jk,kl->il',CX,np.kron(np.eye(2),G),CX,optimize=False)
    J=np.einsum('ij,jk->ik',U,np.kron(np.eye(2),v[:,None]),optimize=False)
    P0=np.diag([1,1,0,0]);P10=np.diag([0,0,1,0]);P11=np.diag([0,0,0,1])
    def effect(P):return np.einsum('ki,kl,lj->ij',J,P,J,optimize=False)
    need(np.max(np.abs(effect(P10)-np.diag([0,1])))<2e-15,'true NC1 equality readout')
    need(np.max(np.abs(effect(P0)-np.diag([1,0])))<2e-15 and np.max(np.abs(effect(P11)))<2e-15,'all NC1 sectors')
    cases={str(r):check_comparator(r) for r in (None,0,1,2,3)}
    pairs,_,S=original_reference();need(S==256 and len(pairs)==64,'actual Fourier reference')
    def chi(y):
        w=np.zeros(128)
        for j,k in enumerate(pairs):
            q=sum(k[i]*y[i] for i in range(4))%4
            w[2*j+(q&1)]=(-1 if q&2 else 1)/128
        return w
    theta=math.asin(p);A=p*math.sin(712*theta);c=-p*math.cos(712*theta)
    def matter(y,u,v):
        phase=math.pi/2*(y[1]+u*y[0]+v*y[2])
        m=np.zeros(16);m[1]=a;m[14]=c;m[0]=A*math.cos(phase);m[15]=A*math.sin(phase)
        return m
    normerr=0.
    for y in product(range(4),repeat=4):
      normerr=max(normerr,abs(float(np.dot(chi(y),chi(y)))-1/256))
      for u,vv in product((0,1),repeat=2):
        normerr=max(normerr,abs(float(np.dot(matter(y,u,vv),matter(y,u,vv)))-1))
    need(normerr<2e-15,'every programme and address normalized')
    # Exact environment overlap on two addresses, zero descriptor program:
    # m is unchanged between y=(0,0,0,0) and (1,0,0,0); Fourier
    # signed character overlap equals 5/16 when normalized.
    y0=(0,0,0,0);y1=(1,0,0,0)
    overlap=256*np.dot(chi(y0),chi(y1))*np.dot(matter(y0,0,0),matter(y1,0,0))
    need(abs(overlap-5/16)<1e-14,'actual Fourier state dephases SITE coherence')
    # 2 SITE values × 2 programme values × 2 oldRIGHT values; retained
    # inputs create orthogonal output slots, so the actual ready map has
    # full Gram I/256 even when program and RIGHT are entangled.
    sites=[y0,y1];progs=[(0,0),(1,1)];dim=8;K=np.zeros((dim*2048,dim))
    for xx,pr,ref in product(range(2),range(2),range(2)):
      j=(xx*2+pr)*2+ref;y=sites[xx];u,vv=progs[pr]
      K[j*2048:(j+1)*2048,j]=np.kron(matter(y,u,vv),chi(y))
    gram=np.einsum('ki,kj->ij',K,K,optimize=False)
    gerr=float(np.max(np.abs(gram-np.eye(dim)/256)))
    need(gerr<2e-16,'common SITE/program/RIGHT ready full Gram')
    rng=np.random.default_rng(20261119)
    psi=rng.normal(size=(2,dim))+1j*rng.normal(size=(2,dim));psi/=np.linalg.norm(psi)
    old=np.einsum('ai,bi->ab',psi,psi.conj(),optimize=False)
    # Gram identity yields trace over retained X/program/RIGHT AND resource.
    new=256*np.einsum('ai,ij,bj->ab',psi,gram,psi.conj(),optimize=False)
    serr=float(np.max(np.abs(new-old)));need(serr<2e-14,'arbitrary entangled scene marginal')
    mp.mp.dps=150;pp=(mp.sqrt(5)-1)/2
    b0=1-(1-2*pp**3)**16;b232=1-pp**192;b332=1-(1-16*pp**9)**32
    b264=1-pp**384;b364=1-(1-16*pp**9)**64
    Pmat=b0**226*(b232**4*b332)**113*b332**9
    Pone=Pmat*(1-pp**40)*b264**14*(b264**6*b364)**456
    b1=1-pp**40;bt=b264**6*b364;eta=Pone*b1*bt**14
    # Explicit first-failure resolution, after physical Fourier-ready input.
    total=Pone*(1-b1)+sum(Pone*b1*bt**j*(1-bt) for j in range(7))
    for q in (mp.mpf(1)/256,mp.mpf(255)/256):
      total+=sum(Pone*b1*bt**(7+j)*(1-bt)*q for j in range(7))
      total+=eta*q
    need(abs(total-Pone)<mp.mpf('1e-135'),'all comparator success and failure masses')
    out={'status':'PASS; actual native logical interfaces, conditional physical factories',
      'comparator_cases':cases,'full_resource_normalization_error':normerr,
      'finite_protected_arena_dimension':dim,'ready_effect_full_gram_error':gerr,
      'entangled_scene_marginal_error':serr,'same_reference_SITE_coherence_multiplier':overlap,
      'Fourier_resource_success_Pone':mp.nstr(Pone,45),
      'comparison_known_one_and_factories_success':mp.nstr(b1*bt**14,45),
      'joint_hardware_ready':mp.nstr(eta,45),'ready_equal_effect_scalar':mp.nstr(eta/256,45),
      'ready_not_equal_effect_scalar':mp.nstr(eta*255/256,45),
      'factory_first_failures_all_mass_error':mp.nstr(abs(total-Pone),8),
      'full_factory_dilation_and_joint_clock_simulated':False,
      'Book03_price_or_full_geometric_bank_derived':False,'GR_closed':False}
    print(json.dumps(out,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
