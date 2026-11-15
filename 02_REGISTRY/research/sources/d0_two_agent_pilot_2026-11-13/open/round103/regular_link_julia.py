#!/usr/bin/env python3
"""Certified Julia32 target for the original B25 proper link on a local chart.

Input offsets are six exact Fractions in B42 GEN order. Digits are six
integers in 0..3 or None for the exact chart centre. No SVD, eigenvector,
zero-boost division, exact-zero oracle, or tie-breaking by equality.
"""
from pathlib import Path
from fractions import Fraction
from itertools import permutations, product
from hashlib import sha256
from math import comb
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'round93'))
import proper_link_two_bit_targets as t
import proper_link_two_bit_native as native
base=t.base
GEN=base.GEN
ORDER=(0,2,3,1)

class MorePrecision(Exception):pass

def validate(offsets,digits,xy):
    if type(offsets) not in (tuple,list) or len(offsets)!=6:raise ValueError('six offsets required')
    if any(type(q) is not Fraction for q in offsets):raise TypeError('offsets must be exact Fraction objects')
    if any(abs(q)>=Fraction(1,2**32) for q in offsets):raise ValueError('strict centre chart |offset|<2^-32')
    if digits is not None and (type(digits) not in (tuple,list) or len(digits)!=6 or any(type(z) is not int or not 0<=z<4 for z in digits)):
        raise ValueError('digits must be None or six literal integers in 0..3')
    if xy is not None and (type(xy) not in (tuple,list) or any(type(v) is not int for v in xy) or tuple(xy) not in ((1,1),(1,2),(2,1),(2,2))):
        raise ValueError('xy must be None or one original B25 f-link baseline')

def exp_at(iv,offsets,digits):
    # B42 null-frame generators eta(Eij-Eji), exactly B25 GEN order.
    eta=((0,1,0,0),(1,0,0,0),(0,0,-1,0),(0,0,0,-1))
    theta=[[iv.zero for _ in range(4)] for _ in range(4)]
    p2=iv.square(iv.c['p'])
    for index,((i,j),off) in enumerate(zip(GEN,offsets)):
        x=iv.R(off.numerator,off.denominator)
        if digits is not None:
            x=iv.add(x,iv.mul(iv.R(1,2**80),iv.sub(iv.R(digits[index]),iv.scalar(p2,3))))
        for k in range(4):
            if eta[k][i]:theta[k][j]=iv.add(theta[k][j],iv.scalar(x,eta[k][i]))
            if eta[k][j]:theta[k][i]=iv.sub(theta[k][i],iv.scalar(x,eta[k][j]))
    # Each row has at most 3 coefficients, so ||theta||inf<2^-30;
    # use weaker 2^-29 and a strict geometric/factorial tail < one ulp.
    term=iv.eye(4);out=term;fact=1;n=0
    while True:
        n+=1;fact*=n
        term=iv.mscale(iv.mm(term,theta),iv.R(1,n));out=iv.madd(out,term)
        if 29*(n+1)+(fact*(n+1)).bit_length()-1>=iv.bits+18:break
    return [[(x[0]-1,x[1]+1) for x in row] for row in out],n

def det(iv,A):
    n=len(A)
    if not n:return iv.one
    out=iv.zero
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        v=iv.one
        for i,j in enumerate(p):v=iv.mul(v,A[i][j])
        out=iv.add(out,iv.neg(v) if inversions%2 else v)
    return out

def exterior_blocks(iv,U):
    masks=[[m for m in range(16) if bin(m).count('1')==k] for k in range(5)]
    indices={m:[i for i in ORDER if (m>>i)&1] for group in masks for m in group}
    blocks=[]
    for group in masks:
        rows=[]
        for i in group:
            rr=[]
            for j in group:
                sub=[[U[a][b] for b in indices[j]] for a in indices[i]]
                rr.append(iv.mul(det(iv,sub),iv.R(1,2)))
            rows.append(rr)
        blocks.append(rows)
    return masks,blocks

def msub(iv,A,B):return [[iv.sub(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]

def sqrt_iterations(target_bits):
    # e_n <= (15/16)^(2^n) < 2^(-target_bits-16).
    n=0
    while (15**(1<<n))*(1<<(target_bits+16)) >= 16**(1<<n):n+=1
    return n

def sqrt_defect(iv,D,target_bits):
    n=len(D);I=iv.eye(n);Z=I
    iterations=sqrt_iterations(target_bits)
    for _ in range(iterations):
        Z=iv.mscale(iv.mm(Z,msub(iv,iv.mscale(I,iv.R(3)),iv.mm(D,iv.mm(Z,Z)))),iv.R(1,2))
    S=iv.mm(D,Z)
    # Exact SPD spectrum in [1/16,1] belongs to B91's original chart.
    # Every true entry of sqrt(D) differs from D Z by <2^-(target_bits+16).
    e=-((-iv.S)//(1<<(target_bits+16)))
    return [[(x[0]-e,x[1]+e) for x in row] for row in S],iterations

def target_intervals(offsets,digits,xy,bits,target_bits):
    validate(offsets,digits,xy)
    if bits<target_bits+20:raise ValueError('insufficient interval guard bits')
    iv=t.Interval(bits);E,terms=exp_at(iv,offsets,digits)
    U=iv.mm(E,iv.baseline(None if xy is None else tuple(xy)))
    masks,blocks=exterior_blocks(iv,U)
    C=[[iv.zero for _ in range(16)] for _ in range(16)]
    left=[[iv.zero for _ in range(16)] for _ in range(16)]
    right=[[iv.zero for _ in range(16)] for _ in range(16)]
    iterations=[]
    for group,B in zip(masks,blocks):
        n=len(group);I=iv.eye(n);Bt=iv.transpose(B)
        dl=msub(iv,I,iv.mm(B,Bt));dr=msub(iv,I,iv.mm(Bt,B))
        sl,nl=sqrt_defect(iv,dl,target_bits);sr,nr=sqrt_defect(iv,dr,target_bits)
        iterations.append((nl,nr))
        for i,a in enumerate(group):
            for j,b in enumerate(group):C[a][b]=B[i][j];left[a][b]=sl[i][j];right[a][b]=sr[i][j]
    Ct=iv.transpose(C)
    J=[C[i]+left[i] for i in range(16)]+[right[i]+[iv.neg(v) for v in Ct[i]] for i in range(16)]
    return iv,J,{'exp_terms':terms,'sqrt_iterations':iterations}

def point_matrix(J,S,target_bits):
    # A is exactly dyadic, and ||A-J||op <=32 max |entry error|.
    A=[];maxrad=0
    for row in J:
        rr=[]
        for lo,hi in row:
            mid=(lo+hi)//2;maxrad=max(maxrad,mid-lo,hi-mid);rr.append((mid,mid))
        A.append(rr)
    if 32*maxrad*(1<<target_bits)>S:raise MorePrecision('target width')
    return A,maxrad

def interval_qr(iv,A,target_bits):
    """Stable deterministic pivot, QR for the dyadic A; no largest comparison."""
    N=32;Q=[row[:] for row in A];angles=[];S=iv.S
    for col in range(N-1):
        candidates=[]
        for j in range(col,N):
            lo,_=iv.absbounds(Q[j][col])
            if 8*lo>S:candidates.append(j)
        if not candidates:raise MorePrecision('pivot threshold')
        pivot=candidates[0]
        rows=([pivot] if pivot!=col else [])+[j for j in range(col+1,N) if j!=pivot]
        for j in rows:
            a,b=Q[col][col],Q[j][col]
            rad=iv.sqrt(iv.add(iv.square(a),iv.square(b)))
            if 8*rad[0]<=S:raise MorePrecision('rotation radius')
            c=iv.div(a,rad);s=iv.neg(iv.div(b,rad))
            # G=[[c,-s],[s,c]], G(a,b)=(r,0).
            row0=Q[col][:];row1=Q[j][:]
            for k in range(col,N):
                Q[col][k]=iv.sub(iv.mul(c,row0[k]),iv.mul(s,row1[k]))
                Q[j][k]=iv.add(iv.mul(s,row0[k]),iv.mul(c,row1[k]))
            # This entry is algebraically zero for the exact dyadic A.
            Q[j][col]=iv.zero
            angles.append({'i':col,'j':j,'cos':c,'sin':iv.neg(s)})
    # Compact posterior certificate: ||R-I||op <=32 max entry deviation.
    maxdev=0
    for i,row in enumerate(Q):
        for j,entry in enumerate(row):
            z=iv.sub(entry,iv.one if i==j else iv.zero)
            maxdev=max(maxdev,iv.absbounds(z)[1])
    if 32*maxdev*(1<<target_bits)>S:raise MorePrecision('QR residual')
    assert len(angles)==496
    return list(reversed(angles)),maxdev

def target_rotations(offsets,digits,xy,target_bits=3460,work_bits=None):
    """Return outward rotations and certificates; precision increases finitely.

    Returned angle intervals have scale 2^bits. They refer to a known dyadic
    A and its exact Givens QR, and compose within 2*2^-target_bits of J.
    """
    validate(offsets,digits,xy)
    if type(target_bits) is not int or target_bits<16:raise ValueError('target_bits >= 16')
    bits=max(target_bits+128,128) if work_bits is None else work_bits
    if bits<target_bits+20:raise ValueError('work precision must exceed target precision')
    retries=0
    while True:
        iv,J,meta=target_intervals(offsets,digits,xy,bits,target_bits)
        try:
            A,rad=point_matrix(J,iv.S,target_bits)
            angles,res=interval_qr(iv,A,target_bits)
            return {'input':{'offsets_fraction':[[str(q.numerator),str(q.denominator)] for q in offsets],
                             'digits':None if digits is None else list(digits),
                             'xy':None if xy is None else list(xy)},
                    'bits':bits,'target_bits':target_bits,'angle_intervals':angles,
                    'target_max_entry_error_ulps':int(rad),'qr_max_residual_ulps':int(res),
                    'iterations':meta,'precision_retries':retries,
                    'matrix_operator_error_upper':'2^(1-target_bits)',
                    'rotation_count':len(angles),'all_32_columns':True}
        except MorePrecision:
            bits*=2;retries+=1

def native_rotations(offsets,digits,xy,target_bits=3460):
    """Convert all target rotations to actual fixed B93 grid G-powers.

    Angle cells can remain unresolved at a given interval precision even
    when the QR residual already passed. Restart at higher precision; ties
    between target/rounding cells need no exact equality decision.
    """
    validate(offsets,digits,xy)
    bits=max(target_bits+128,128);attempt=0
    while True:
        data=target_rotations(offsets,digits,xy,target_bits,work_bits=bits)
        bits=data['bits'];out=[];S=1<<bits
        try:
            for row in data['angle_intervals']:
                i,j=row['i'],row['j'];pivot=((i^j)&-(i^j)).bit_length()-1
                sin=row['sin'];cos=row['cos']
                if (i>>pivot)&1:sin=(-sin[1],-sin[0])
                def low(a):return 0 if a[0]<=0<=a[1] else min(abs(a[0]),abs(a[1]))
                if 10*max(low(cos),low(sin))<=6*S:raise MorePrecision('angle quadrant')
                k=native.power_for(cos,sin,bits)
                out.append({'i':i,'j':j,'k':int(k)})
            digest=sha256();width=(native.Q.bit_length()+7)//8
            for item in out:
                digest.update(bytes((item['i'],item['j'])))
                digest.update(item['k'].to_bytes(width,'big'))
            data['grid_precision_retries']=attempt
            data['angle_powers_sha256']=digest.hexdigest()
            return data,out
        except (MorePrecision,native.a41.e.NeedPrecision):
            bits*=2;attempt+=1

def sector_blocks(global_layout,entry,angles,reverse=False):
    """Literal 29-control native word for one fixed address/CODE sector."""
    lay=native.bind(global_layout,entry);controls,pattern=native.old.sector_controls(lay,entry)
    basis=lay['modes']+[lay['julia_flag']]
    if len(basis)!=5 or len(set(basis))!=5:raise ValueError('five distinct Julia bits required')
    for row in (reversed(angles) if reverse else angles):
        a,b,k=row['i'],row['j'],row['k'];diff=a^b
        if not (0<=a<b<32 and diff and k>0):raise ValueError('invalid rotation')
        pivot=(diff&-diff).bit_length()-1
        flips=[j for j in range(5) if j!=pivot and (diff>>j)&1]
        transformed=a
        for j in flips:
            if (transformed>>pivot)&1:transformed^=1<<j
        perm=[native.old.nb.gate('CX',basis[pivot],basis[j]) for j in flips]
        cs=controls+[basis[j] for j in range(5) if j!=pivot]
        ps=pattern+[(transformed>>j)&1 for j in range(5) if j!=pivot]
        assert len(cs)<=29
        yield from perm
        yield from native.old.selective_terms(cs,ps,basis[pivot],k,lay,common_controls=29,reverse=reverse)
        yield from reversed(perm)

def sector_cost(global_layout,entry,angles,reverse=False):
    """Exact compressed inventory of this emitted sector, not a bank total."""
    from collections import Counter
    lay=native.bind(global_layout,entry);controls,pattern=native.old.sector_controls(lay,entry)
    basis=lay['modes']+[lay['julia_flag']];total=Counter()
    for row in angles:
        a,b,k=row['i'],row['j'],row['k'];diff=a^b
        if not (0<=a<b<32 and k>0):raise ValueError('invalid rotation')
        pivot=(diff&-diff).bit_length()-1
        flips=[j for j in range(5) if j!=pivot and (diff>>j)&1]
        transformed=a
        for j in flips:
            if (transformed>>pivot)&1:transformed^=1<<j
        cs=controls+[basis[j] for j in range(5) if j!=pivot]
        ps=pattern+[(transformed>>j)&1 for j in range(5) if j!=pivot]
        total.update(native.old.select_cost(cs,ps,k,common_controls=29,reverse=reverse))
        total.update({'CX':2*len(flips)})
    return total

def variable_entry(group,digits):
    """B93 f-bank group -> exact 12-wire CODE pattern in B42 GEN order."""
    if type(digits) not in (tuple,list) or len(digits)!=6 or any(type(z) is not int or not 0<=z<4 for z in digits):
        raise ValueError('six base-4 CODE digits required')
    ids=group['indices_by_generator']
    if len(ids)!=6 or len(set(ids))!=6 or any(type(j) is not int or not 0<=j<2688 for j in ids):
        raise ValueError('six distinct physical coordinate indices required')
    return {'address':group['address'],'SAM_indices':ids+[2688+j for j in ids],
            'SAM_pattern':[d&1 for d in digits]+[(d>>1)&1 for d in digits]}

def variable_bank_cost_upper(group_count,reverse=False):
    """Conservative bound for 4096 CODE sectors per B93 variable group.

    Covers the 496 direct Julia rotations, maximum four CX permutations on
    each side and k<=Q. Does not include B93 fixed sectors, other source
    components, post, initial births, or SourceI replacement.
    """
    from collections import Counter
    if type(group_count) is not int or group_count<0:raise ValueError('nonnegative group count required')
    one=native.old.select_cost(list(range(29)),[1]+[0]*28,native.Q,common_controls=29,reverse=reverse)
    one.update({'CX':8})
    n=group_count*4096*496
    return Counter({key:n*value for key,value in one.items()})


def variable_bank_entries(field,reverse=False):
    """All original B93 f-variable groups, with each group's own Y offsets.

    ``field`` supplies selected(indices)->six Fractions (A53 FieldCentre).
    This enumerates logical sectors only; it does not compile any gate.
    """
    _,cat=t.catalogue();groups=cat['f']['variable']
    digit_words=list(product(range(4),repeat=6))
    for group in (reversed(groups) if reverse else groups):
        offsets=tuple(field.selected(group['indices_by_generator']))
        validate(offsets,None,group['xy'])
        for digits in (reversed(digit_words) if reverse else digit_words):
            yield {'offsets':offsets,'digits':digits,'xy':group['xy'],
                   'entry':variable_entry(group,digits)}


def variable_bank_blocks(field,global_layout,reverse=False):
    """Actual lazy native provider for all f-variable sectors only.

    Every sector is evaluated from its own exact centre offsets. On reverse,
    both logical sector order and each physically emitted word are inverted.
    The fixed/reference bank sectors, births and SourceI replacement remain
    the caller's separate paid components.
    """
    for sector in variable_bank_entries(field,reverse):
        _,angles=native_rotations(sector['offsets'],sector['digits'],sector['xy'])
        yield from sector_blocks(global_layout,sector['entry'],angles,reverse)
