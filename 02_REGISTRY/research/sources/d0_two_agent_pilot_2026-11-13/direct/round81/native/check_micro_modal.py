"""Most probable individual printed history, not the weight of a set of histories."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import sys

import mpmath as mp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_absolute_cycles import BOUNDARY, ring_mul, ring_sum


def histogram(length,threshold,belongs):
    # Split into the first bit incompatible with the comparison boundary, or equality.
    hist=Counter()
    for k,bit in enumerate(threshold):
        other='0' if bit=='1' else '1'
        tag=other<bit
        if tag==belongs:
            first=threshold[:k]+other
            hist.update({first.count('1')+j:comb(length-k-1,j)
                         for j in range(length-k)})
    if belongs:
        hist[threshold.count('1')]+=1
    return hist


def product_hist(a,b):
    hist=Counter()
    for i,v in a.items():
        for j,w in b.items(): hist[i+j]+=v*w
    return hist


def mass(hist,N):
    powers=[(1,0)]
    for _ in range(2*N): powers.append(ring_mul(powers[-1],(0,1)))
    out=(0,0)
    for count,n in hist.items():
        a,b=powers[N+count]
        out=ring_sum(out,(n*a,n*b))
    return out


def calibrations():
    ready=histogram(47,BOUNDARY,True)
    idle=histogram(47,BOUNDARY,False)
    assert all(ready[i]+idle[i]==comb(47,i) for i in range(48))
    assert (min(idle),idle[min(idle)])==(3,2)
    all_work=Counter({i:comb(18,i) for i in range(19)})
    for n in (12,18):
        stay=Counter({i:comb(18-n,i) for i in range(19-n)})
        turn=all_work-stay
        for a,b,m,k in [(ready,stay,0,1),(ready,turn,1,n),(idle,all_work,3,2)]:
            h=product_hist(a,b)
            assert (min(h),h[min(h)])==(m,k)
        alt=Counter({i+n//2:comb(18-n//2,i) for i in range(19-n//2)})
        assert mass(stay,18)==mass(alt,18) and min(alt)==n//2
    # Five + three *specific* distinct words to exchange, not just formal multiplicities.
    removed=[]
    for extra,number in ((1,5),(2,3)):
        for tail in list(combinations(range(3,47),extra))[:number]:
            word=''.join('1' if j in {0,1,2,*tail} else '0' for j in range(47))
            assert word>BOUNDARY
            removed.append(word)
    assert len(set(removed))==8
    new_idle=idle.copy()
    for w in removed: new_idle[w.count('1')]-=1
    new_idle[0]+=1
    assert mass(new_idle,47)==mass(idle,47) and min(new_idle)==0
    resolved={True:[],False:[]}
    for k,bit in enumerate(BOUNDARY):
        other='0' if bit=='1' else '1'
        resolved[other<bit].append(BOUNDARY[:k]+other)
    resolved[True].append(BOUNDARY)
    length=lambda w: len(w)+w.count('1')
    for key,short in ((True,'0'),(False,'111')):
        assert min(resolved[key],key=length)==short
        assert sum(length(w)==length(short) for w in resolved[key])==1
    print('65-head modes and equal-mass retaggings verified; variable-depth service minima 1 and 6')


def eight():
    p=(mp.iv.sqrt(5)-1)/2
    counts=[1,1]
    for _ in range(2,37): counts.append(counts[-1]+counts[-2])
    allocated=[5644800,4939200,4390400,3087000,1580544,548800,115200,11025]
    assert counts[36]==24157817 and counts[35]==14930352
    assert counts[36]-sum(allocated)==3840848
    assert sum(comb(36-n,n) for n in range(19))==counts[36]
    assert comb(18,18)==1
    # Published native bounds on the actual B, before deterministic sign conversion.
    qmin,qmax=p**2,p**2+6*p**10
    assert qmax.b<.432 and (1-qmax).a>.568
    assert (1-qmax).a>(p**2).b and qmin.a>0
    for cost in (36,37,65,66,68):
        print(f'p^{cost} = {float((p**cost).mid):.12g}')
    print('EIGHT exactly 3840848 idle modal transcripts; active/overshoot have a uniform gap')


if __name__=="__main__":
    mp.iv.dps=60
    calibrations()
    eight()
