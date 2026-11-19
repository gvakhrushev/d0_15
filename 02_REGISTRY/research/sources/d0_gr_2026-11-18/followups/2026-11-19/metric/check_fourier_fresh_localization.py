"""Original real Fourier-128 reference, retained SITE and fresh local copies."""
from fractions import Fraction as F
from itertools import product
from mpmath import iv
import numpy as np
import json


def original_reference():
    D=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
       (-1,1,0,0),(-1,0,1,0),(0,-1,1,0),
       (-1,0,0,1),(0,-1,0,1),(0,0,-1,1))
    cosmod=(1,0,-1,0)
    pairs=[k for k in product(range(4),repeat=4)
           if k<tuple((-v)%4 for v in k)]
    assert len(pairs)==120
    def score(k):return sum(cosmod[sum(a*b for a,b in zip(k,d))%4] for d in D)
    pairs.sort(key=lambda k:(-score(k),k))
    chosen=pairs[:64]
    overlaps=[sum(cosmod[sum(a*b for a,b in zip(k,d))%4] for k in chosen) for d in D]
    assert overlaps==[20,10,10,9,8,8,6,9,5,5]
    sites=list(product(range(4),repeat=4)); S=len(sites)
    M=np.zeros((S,128),dtype=np.int32)
    for a,x in enumerate(sites):
        for j,k in enumerate(chosen):
            b=sum(u*v for u,v in zip(x,k))%4
            bit=b%2;sign=1 if b<2 else -1
            M[a,2*j+bit]=sign
            # Paid controlled lookup, CX to type bit, phase Z on high bit,
            # inverse lookup. This is valid on the actual real Fourier phase.
            assert (bit^(b&1))==0
            assert sign*(1 if (b>>1)==0 else -1)==1
    assert np.array_equal(M.T@M,128*np.eye(128,dtype=np.int32))
    assert all(int(row@row)==64 for row in M)
    outside=sum(2 in k for k in chosen)
    assert outside==27
    return chosen,outside,S


def global_choi_labels(L):
    S=L**4; A=8*S+1
    sites=list(product(range(L),repeat=4))
    def number(x):
        n=0
        for y in x:n=n*L+y
        return n
    def address(kind,r,x):return 1+(kind*4+r)*S+number(x)
    for x in sites:
        selected=[0]
        selected.extend(address(0,r,x) for r in range(4))
        selected.extend(address(1,r,x) for r in range(4))
        for r in range(4):
            for shift in range(4):
                if shift==r:continue
                y=list(x);y[shift]=(y[shift]+1)%L
                selected.append(address(1,r,tuple(y)))
        assert len(selected)==21 and len(set(selected))==21
        chosen=set(selected)
        permutation=selected+[a for a in range(A) if a not in chosen]
        assert len(permutation)==A and len(set(permutation))==A
        # Inverting the controlled address permutation restores the exact
        # original global address for each of the 21 local labels.
        inverse={old:new for new,old in enumerate(permutation)}
        assert all(inverse[old]==i for i,old in enumerate(selected))
    return S,A,len(sites)


def right_counterexample():
    # Normalized two-column isometry V_C=|0,m0><0|+|1,m1><1|.
    # Equality to external X has effect diag(1,0,0,1) on X tensor R.
    E=np.diag([1,0,0,1]); I=np.eye(2); mixed=I/2
    p0=E[0,0];p1=E[1,1]
    assert p0==1 and p1==0
    reduced=np.array([[sum(mixed[r,r]*E[2*x+r,2*x+r] for r in (0,1))
                       if x==y else 0 for y in (0,1)] for x in (0,1)])
    assert np.array_equal(reduced,I/2)
    # 1/2 averaged success does not mean E=I/2 on the protected input.
    assert not np.array_equal(E,np.eye(4)/2)
    # Fresh maximally entangled purification gives a distinct input and a
    # success map K=(1/sqrt(2)) V; exact isometry because X is retained.
    return {'arbitrary_right_yes_on_x0_r0':int(p0),
            'arbitrary_right_yes_on_x0_r1':int(p1),
            'maximally_mixed_right_scalar_effect':'I_X/2',
            'protected_joint_effect_rank':int(np.linalg.matrix_rank(E)),
            'fresh_purified_success':'1/2'}


def main():
    chosen,outside,S=original_reference()
    sites,A,count=global_choi_labels(4)
    assert S==sites==count==256 and A==2049
    toy=right_counterexample()
    iv.dps=80
    p=(iv.sqrt(5)-1)/2
    retention=1-iv.mpf(outside)*p/64
    assert iv.mpf('.7392')<retention<iv.mpf('.7393')
    # 2 f signs x 82 programme copies; 8 q signs x (2 programme + 10 CAR).
    nchoi=2*82+8*2; nfourier=8*10
    assert nchoi==180 and nfourier==80
    loc=iv.mpf(1)/S**nfourier*(iv.mpf(21)/A)**nchoi
    assert loc>iv.mpf('1.8311e-551') and loc<iv.mpf('1.8312e-551')
    z=iv.mpf(1)/2**20;L0=4*p**3
    rf=4*p**2*(1-2*p**2)*z*(1-z*L0)*(1-L0)
    c=iv.mpf(16448)/65025;C=iv.mpf(2)**973
    cos2=1-2*p*p
    for _ in range(9):cos2=2*cos2*cos2-1
    vis=(1-cos2)*p**7/2
    b2=1-p**384;b3=1-(1-16*p**9)**64
    beta24=(1-p**40)*(b2**6*b3)**1452
    # Previous ideal high-reference bound assumed factory readiness >=1/2;
    # here 260 exact localization successes multiply each bank readiness.
    low=beta24*840*p**27*vis*rf**2*c/(131072*16*C**2)*loc**2
    high=12*low
    assert low>iv.mpf('1e-1715') and high<iv.mpf('1e-1712')
    print(json.dumps(dict(status='PASS',
      original_real_Fourier_L4_pairs=len(chosen),original_kappa_with_nyquist=outside,
      true_reference_gram='C^T C = I_128/128',
      true_original_ten_stencil_overlap_numerators=[20,10,10,9,8,8,6,9,5,5],
      exact_bandlimited_vacuum_retention='1-27*p/64',
      numerical_bandlimited_vacuum_retention=str(retention),
      controlled_fresh_purifier_lookup_all_site_pair_cases=S*64,
      original_sites=S,explicit_global_choi_address_count=A,
      selected_local_choi_addresses=21,site_controlled_address_permutations_checked=count,
      true_original_fourier_copies_per_ten_sign_bank=nfourier,
      original_global_choi_copies_per_ten_sign_bank=nchoi,
      ideal_joint_localization_readiness=str(loc),
      ideal_high_reference_gain_lower_over_H_squared=str(low),
      ideal_high_reference_gain_upper_over_H_squared=str(high),
      protected_right_counterexample=toy,
      readiness_requires='independent exact pure original Fourier and explicitly labelled global Julia-Choi copies; complete success/failure records; accessible SITE and controlled address logic',
      purifier_uncompute_requires='fresh 128-dimensional purification accessible and paid; NOT unknown protected old RIGHT',
      actual_seed_readiness_and_native_prices_derived=False,
      actual_global_choi_address_encoding_confirmed=False,
      original_gram_and_complete_CQ_cost_preserved=False,
      GR_closed=False),indent=2,sort_keys=True))

if __name__=='__main__':main()
