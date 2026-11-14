#!/usr/bin/env python3
"""Recheck A38 powers by independent rectangle intervals, not A38 balls.

The exact target sqrt/arithmetic and rectangle rotation are independent of A38.
The rectangle routine is cross-checked with the owned native_phase at small
precisions. GMP is used for exact integer operations; no float is used.
"""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import importlib.util, json, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / ".deps"))
import gmpy2
OPEN = Path(__file__).resolve().parents[4]
# parents[4] is 02_REGISTRY; use explicit project roots to pin owned sources.
ROOT = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
DIRECT = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
A = DIRECT / '02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round38'
OWNER = ROOT / '02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/native_phase.py'
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('owner_native_phase', OWNER)
owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
BITS = 61000
S = 1 << BITS

def rectangle_rotation(k, bits):
    """Exact GMP integer rectangles, independently implemented.

    Every lower product is floor(a*b/S), every upper is ceil(a*b/S).
    Complex multiplication adds/subtracts interval endpoints; clipping at
    [-S,S] is valid since each exact power is a unit complex number.
    Binary powering preserves containment by induction; all operands are ints.
    """
    assert type(k) is int and k > 0 and bits >= 16
    z = gmpy2.mpz; scale = z(1) << bits
    def ceildiv(a,b): return -((-a)//b)
    def product(a,b):
        ps=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
        return min(ps)//scale,ceildiv(max(ps),scale)
    def clip(a):
        a=(max(-scale,a[0]),min(scale,a[1])); assert a[0]<=a[1]; return a
    def times(a,b):
        ac,bd,ad,bc=product(a[0],b[0]),product(a[1],b[1]),product(a[0],b[1]),product(a[1],b[0])
        return clip((ac[0]-bd[1],ac[1]-bd[0])),clip((ad[0]+bc[0],ad[1]+bc[1]))
    sqrt5=gmpy2.isqrt(5*scale*scale)
    p=((sqrt5-scale)//2,ceildiv(sqrt5+1-scale,2))
    a=(gmpy2.isqrt(p[0]*scale),gmpy2.isqrt(p[1]*scale)+1)
    acc=((scale,scale),(z(0),z(0))); base=(a,p)
    while k:
        if k&1: acc=times(acc,base)
        k >>= 1
        if k: base=times(base,base)
    return int(scale),tuple(map(int,acc[0])),tuple(map(int,acc[1]))

def ratio(n, d=1): return n*S//d, -((-n*S)//d)
def add(x, y): return x[0]+y[0], x[1]+y[1]
def neg(x): return -x[1], -x[0]
def sub(x, y): return add(x, neg(y))
def mul(x, y):
    p = [a*b for a in x for b in y]
    return min(p)//S, -((-max(p))//S)
def div(x, y):
    assert y[0] > 0
    q = [(a*S,b) for a in x for b in y]
    return min(a//b for a,b in q), max(-((-a)//b) for a,b in q)
def root(x):
    assert x[0] >= 0
    return isqrt(x[0]*S), isqrt(x[1]*S)+1

def targets():
    one,two=ratio(1),ratio(2)
    p=div(sub(root(ratio(5)),one),two)
    a=root(p)
    root_half=root(ratio(1,2))
    pi8=(root(div(add(one,root_half),two)),root(div(sub(one,root_half),two)))
    pi6=(div(root(ratio(3)),two),ratio(1,2))
    half=(root(div(add(one,a),two)),root(div(sub(one,a),two)))
    scale,_,sin512=owner._rotation_intervals(512,BITS)
    assert scale==S
    p7=one
    for _ in range(7): p7=mul(p7,p)
    cref=sub(one,mul(ratio(8),mul(mul(sin512,sin512),p7)))
    assert 3*cref[0]>2*S and cref[1]<=S
    denom=add(one,cref)
    beta=(root(div(cref,denom)),root(div(one,denom)))
    return {'pi8':pi8,'pi6':pi6,'half_theta':half,'beta':beta,
            'minus_beta':(beta[0],neg(beta[1])),
            'minus_half_theta':(half[0],neg(half[1])),
            'minus_theta':(a,neg(p))},cref

def read_certificate():
    data=(A/'POST_ANGLE_CERTIFICATE.json').read_bytes()
    cert=json.loads(data)
    assert cert['status']=='PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS'
    assert cert['generator_sha256']==sha256((A/'certify_post_angles.py').read_bytes()).hexdigest()
    return cert,sha256(data).hexdigest()

def main():
    for bits in (64, 127, 256):
        for k in (1,2,3,7,31,512,1023):
            assert rectangle_rotation(k,bits)==owner._rotation_intervals(k,bits)
    cert,certificate_sha=read_certificate()
    assert cert['error_bits']==20000
    rows=cert['rotations']
    target,cref=targets()
    assert set(rows)==set(target)
    exponents={n:int(v['exponent_hex'],16) for n,v in rows.items()}
    q=int(cert['candidate_proposal_not_proof']['denominator_hex'],16)
    assert exponents['minus_beta']==q-exponents['beta']
    assert exponents['minus_half_theta']==exponents['half_theta']-1
    assert exponents['minus_theta']==2*exponents['minus_half_theta']
    result={'status':'IN_PROGRESS','independent_precision_bits':BITS,
            'certificate_sha256':certificate_sha,'owner_native_phase_sha256':sha256(OWNER.read_bytes()).hexdigest(),
            'rotation_algorithm':'independent exact integer rectangles, GMP backend; owner equivalence fixtures',
            'own_checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'target_expression':'c_ref=1-8 sin²(512 theta) p^7; beta=(sqrt(c_ref/(1+c_ref)),sqrt(1/(1+c_ref)))',
            'cref_interval_hex':[hex(x) for x in cref], 'results':{},
            'physical_C_closed':False,'GR_closed':False}
    path=OUT/'B75_INDEPENDENT_ANGLE_AUDIT.json'
    for name in target:
        start=time.monotonic(); k=exponents[name]
        assert k>0 and rows[name]['exponent_bit_length']==k.bit_length()
        scale,c,s=rectangle_rotation(k,BITS); assert scale==S
        tc,ts=target[name]
        dc=max(abs(x-y) for x in c for y in tc)
        ds=max(abs(x-y) for x in s for y in ts)
        err=dc+ds
        assert err*(1<<20000)<S, (name,err.bit_length())
        result['results'][name]={'exponent_sha256':sha256(rows[name]['exponent_hex'].encode()).hexdigest(),
            'exponent_bits':k.bit_length(),'cos_width_bits':(c[1]-c[0]).bit_length(),
            'sin_width_bits':(s[1]-s[0]).bit_length(),
            'L1_error_numerator_hex':hex(err),'denominator_pow2':BITS,
            'operator_error_strict_lt':'2^-20000',
            'elapsed_seconds':round(time.monotonic()-start,3)}
        path.write_text(json.dumps(result,indent=2)+'\n')
        print('independently certified',name,k.bit_length(),flush=True)
    assert sha256((A/'POST_ANGLE_CERTIFICATE.json').read_bytes()).hexdigest()==certificate_sha
    result['status']='PASS_ALL_SEVEN_INDEPENDENT_INTEGER_INTERVALS'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],flush=True)

if __name__=='__main__': main()
