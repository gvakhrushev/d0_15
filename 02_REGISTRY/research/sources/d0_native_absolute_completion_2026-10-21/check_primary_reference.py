#!/usr/bin/env python3
"""Same-boundary normalization test on the original L4/CAR16/RIGHT128 input.

Only the pinned literal counting and Fourier definitions are reconstructed.
No old root or spectral suite is run. The source test applies one native
round effect, so all 128 outcomes enter through their exact completeness
and port-effect identities, not an outcome sample.
"""
from __future__ import annotations
import hashlib,itertools,json,math
from decimal import Decimal,Context
import numpy as np
from check_native_root_transport import I, PREC, sqrt_interval, require
from check_absolute_completion import creators, P

SIZE=4; RIGHT=128; SITES=tuple(itertools.product(range(SIZE),repeat=4))

def original_counts(cost,size):
    counts=np.zeros(size**4,dtype=np.int64)
    def radical_sign(a,b):
        if a==0: return (b>0)-(b<0)
        if b==0 or (a>0)==(b>0): return (a>0)-(a<0)
        difference=a*a-5*b*b
        return ((difference>0)-(difference<0))*(1 if a>0 else -1)
    def visit(remaining,depth,left,width):
        if remaining==0:
            index=0
            for axis in range(4):
                ca=2*left[axis][0]+width[axis][0];cb=2*left[axis][1]+width[axis][1]
                aa,bb=size*(2*ca-cb),size*cb;digit=0
                for cut in range(1,size):
                    if radical_sign(aa-4*cut,bb)>=0: digit=cut
                    else: break
                index=index*size+digit
            counts[index]+=1;return
        axis=depth%4;wf=width.copy();wa,wb=width[axis]
        wf[axis]=(wb,wa-wb)
        visit(remaining-1,depth+1,left.copy(),wf)
        if remaining>=2:
            lr,wr=left.copy(),width.copy();la,lb=left[axis]
            lr[axis]=(la+wb,lb+wa-wb);wr[axis]=(wa-wb,2*wb-wa)
            visit(remaining-2,depth+1,lr,wr)
    visit(cost,0,[(0,0)]*4,[(1,0)]*4)
    require(sum(counts)==10946 and min(counts)==29 and max(counts)==78,'literal cost20 native density')
    digest=hashlib.sha256(json.dumps(list(map(int,counts))).encode()).hexdigest()
    require(digest=='fbca167a01fcca76356153586a1006ad1144b612f97740b7611f163f5a3164e9','pinned original count vector')
    return counts,digest

def fourier_numerators():
    pairs=[]
    for mode in SITES:
        opposite=tuple((-x)%4 for x in mode)
        if mode<opposite: pairs.append(mode)
        if len(pairs)==64:break
    cosines,sines=(1,0,-1,0),(0,1,0,-1)
    f=[]
    for site in SITES:
        row=[]
        for mode in pairs:
            phase=sum(x*k for x,k in zip(site,mode))%4
            row.extend((cosines[phase],sines[phase]))
        f.append(row)
    f=np.asarray(f,dtype=int)
    require(np.array_equal(f.T@f,128*np.eye(128,dtype=int)),'all128 exact Fourier Gram')
    require(np.all((f*f).sum(axis=1)==64),'all128 exact local diagonal')
    return f,pairs

def neighbors():
    index={x:i for i,x in enumerate(SITES)};plus=[];minus=[]
    for r in range(4):
        pp=[];mm=[]
        for site in SITES:
            t=list(site);t[r]=(t[r]+1)%4;pp.append(index[tuple(t)])
            t=list(site);t[r]=(t[r]-1)%4;mm.append(index[tuple(t)])
        plus.append(np.array(pp));minus.append(np.array(mm))
    return plus,minus

LEGS=np.array([[.5,-.5,0,0],[1,1,0,0],[0,0,-1,0],[0,0,0,-1]])

def sqrt_I(x):
    ctx=Context(prec=PREC)
    lo=ctx.sqrt(x.lo);hi=ctx.sqrt(x.hi)
    return I(ctx.next_minus(lo),ctx.next_plus(hi))

def interval_column_energy(col,counts,nums,plus,minus):
    p=(sqrt_interval(5)-1)/2
    rootp=sqrt_I(p)
    a=[p**3*16*sqrt_interval(int(c))/sqrt_interval(10946) for c in counts]
    m={1:rootp,14:p}
    cr=creators()
    mats=np.einsum('ra,aij->rij',LEGS,np.array(cr)).real
    total=I(0)
    # All nonzero CAR output rows included, not only top/top block.
    for x in range(256):
        values=[I(0) for _ in range(16)]
        for r in range(4):
            xp=int(plus[r][x]);xm=int(minus[r][x])
            forward=a[x]*int(nums[xp,col]-nums[x,col])*4/128
            backward=(a[xm]*int(nums[xm,col])-a[x]*int(nums[x,col]))*4/128
            for mask,mass in m.items():
                for out in range(16):
                    c=mats[r,out,mask];ct=mats[r,mask,out]
                    if c: values[out]=values[out]+str(float(c))*mass*forward
                    if ct: values[out]=values[out]+str(float(ct))*mass*backward
        # squared intervals use direct multiplication; widths are tiny and
        # the resulting enclosure is conservative also when crossing zero.
        for z in values:total=total+z*z
    return total

def run():
    counts,digest=original_counts(20,4);num,pairs=fourier_numerators();plus,minus=neighbors()
    density=256*counts/10946;a=P**3*np.sqrt(density)
    m=np.zeros(16);m[1]=np.sqrt(P);m[14]=P
    C=num[:,None,:]*m[None,:,None]/128
    dc=np.zeros_like(C)
    creation=np.einsum('ra,aij->rij',LEGS,np.array(creators())).real
    for r in range(4):
        forward=np.einsum('ij,xja->xia',creation[r],C[plus[r]]-C)*a[:,None,None]
        back=np.einsum('ji,xja->xia',creation[r],a[minus[r],None,None]*C[minus[r]]-a[:,None,None]*C)
        dc+=(forward+back)*4
    cc=C.reshape(4096,128);ddc=dc.reshape(4096,128)
    gram=cc.T@cc;energy=ddc.T@ddc
    require(np.linalg.norm(gram-np.eye(128)/128)<1e-15,'full initial RIGHT Gram')
    ea=np.diag(energy);first,second=57,55
    require(first!=second and ea[second]-ea[first]>.001,'actual primary compressed effect nonscalar')
    # Fixed original columns 57 and 55; only outward interval bounds
    # certify their strict difference. No floating rank test is used.
    en0=interval_column_energy(first,counts,num,plus,minus)
    en1=interval_column_energy(second,counts,num,plus,minus)
    gap=en1-en0
    require(gap.lo>0,'outward full-CAR two-column energy gap')
    p=(sqrt_interval(5)-1)/2
    alpha=p**2/2048
    # t=log(phi), u=p, all one-round native outcomes retained. H1=I-k Delta.
    kap=2*p*alpha*(1-p)
    right_gap=-kap*gap
    require(right_gap.hi<0,'actual marked RIGHT Gram cannot equal a scalar multiple of original Gram')
    kfloat=2*P*(P**2/2048)*(1-P)
    HR=gram-kfloat*energy;Z=float(np.trace(HR))
    Rt=HR/Z;right_diff=float(np.linalg.norm(Rt-gram))
    require(right_diff>1e-7,'normalized target changes untouched RIGHT marginal')
    # First marker derivative: H1_t(0)=-2p alpha Delta.
    derivative=-2*P*(P**2/2048)*(energy-gram*np.trace(energy))
    require(np.linalg.norm(derivative)>1e-7,'original RIGHT first-jet mismatch')
    # Complete physical success+failure filter restores, rather than erases,
    # the old RIGHT state. T_raw^*T_raw=e^-t H1=p H1.
    success_gram=P*HR
    failure_gram=gram-success_gram
    require(np.linalg.eigvalsh(failure_gram).min()>0,'all retained failure-reference mass positive')
    require(np.linalg.norm(success_gram+failure_gram-gram)<1e-15,'complete archive restores fixed RIGHT')
    return {'status':'PASS','carrier':{'sites':256,'CAR':16,'oldRIGHT':128,'all_complete_Kraus_outcomes':128},
      'original_count_sha256':digest,'native_counts_total':int(sum(counts)),
      'count_range':[int(min(counts)),int(max(counts))],
      'primary_matter_amplitude':'0 (vacuum member of original primary family)',
      'two_original_Fourier_column_indices':[first,second],
      'column_modes':[list(pairs[first//2]),list(pairs[second//2])],
      'cosine_or_sine':['cos' if first%2==0 else 'sin','cos' if second%2==0 else 'sin'],
      'energy_diagonal_intervals':[en0.bounds(),en1.bounds()],
      'strict_energy_gap_interval':gap.bounds(),
      'unnormalized_RIGHT_diagonal_difference_interval':right_gap.bounds(),
      'normalized_RIGHT_difference_HS':right_diff,
      'RIGHT_marker_first_source_HS':float(np.linalg.norm(derivative)),
      'all_outcome_absolute_marked_norm':P*Z,
      'retained_failure_probability':float(np.trace(failure_gram)),
      'theorem':'no deterministic LEFT-only map with the same complete initial reference produces the normalized tilted whole record',
      'scope':'the supplied positive cost-marker t=ln(phi); no assertion of compulsory native Info, GR or all-horizon impossibility'}

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
