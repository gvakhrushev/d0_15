#!/usr/bin/env python3
"""Certify A38 numerator/denominator against theta/(2pi), integer-only.

All interval endpoints are dyadic integers with one common scale 2**BITS.
Uses GMP exact integers; no floating point or prior candidate calculation is
part of the proof. See B80_UNIFORM_GOLDEN_GRID_RU.md for the interval proof.
"""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
from math import gcd
import json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'.deps'))
import gmpy2

DIRECT=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
OPEN=HERE.parent
INPUT=DIRECT/'round38/POST_ANGLE_CERTIFICATE.json'
PHASE=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/PHASE_COMPILER.md')
BITS=41024
S=gmpy2.mpz(1)<<BITS

def ceildiv(a,b):return -((-a)//b)
def rational(n,d=1):
    assert d>0
    return (n*S//d,ceildiv(n*S,d))
def add(x,y):return x[0]+y[0],x[1]+y[1]
def sub(x,y):return x[0]-y[1],x[1]-y[0]
def scale(x,n):
    assert n>=0
    return n*x[0],n*x[1]
def mul(x,y):
    ps=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1])
    return min(ps)>>BITS,ceildiv(max(ps),S)
def div(x,y):
    assert y[0]>0
    nums=[(a*S,b) for a in x for b in y]
    return min(a//b for a,b in nums),max(ceildiv(a,b) for a,b in nums)
def root(x):
    assert x[0]>=0
    low=gmpy2.isqrt(x[0]*S);high=gmpy2.isqrt(x[1]*S)
    if high*high<x[1]*S:high+=1
    return low,high

def atan_enclosure(x):
    """Outward alternating Taylor interval for every x in [xlo,xhi]."""
    assert 0<=x[0]<=x[1]<S
    x2=mul(x,x);power=x;lo=hi=gmpy2.mpz(0);k=0
    while power[1]>(gmpy2.mpz(1)<<128):
        d=2*k+1; lower=power[0]//d;upper=ceildiv(power[1],d)
        if k%2==0:lo+=lower;hi+=upper
        else:lo-=upper;hi-=lower
        power=mul(power,x2);k+=1
    # The alternating-series remainder after k terms is at most the first
    # omitted positive magnitude, valid for each real x in the input interval.
    rem=ceildiv(power[1],2*k+1)
    return (lo-rem,hi+rem),k

def certificate():
    raw=INPUT.read_bytes();data=json.loads(raw)
    assert data['status']=='PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS'
    assert data['generator_sha256']==sha256((DIRECT/'round38/certify_post_angles.py').read_bytes()).hexdigest()
    row=data['candidate_proposal_not_proof']
    pn=int(row['numerator_hex'],16); q=int(row['denominator_hex'],16)
    assert 0<pn<q and q.bit_length()==20080 and gcd(pn,q)==1
    one=rational(1);two=rational(2)
    p=div(sub(root(rational(5)),one),two)
    x=root(p)
    assert 0<x[0]<=x[1]<S
    # tan(theta/2)=tan(theta)/(1+sqrt(1+tan(theta)^2)).
    for _ in range(6):x=div(x,add(one,root(add(one,mul(x,x)))))
    at,nt=atan_enclosure(x);theta=scale(at,64)
    # Machin identity, with elementary alternating series at rational 1/5,1/239.
    a5,n5=atan_enclosure(rational(1,5));a239,n239=atan_enclosure(rational(1,239))
    pi=sub(scale(a5,16),scale(a239,4))
    assert 3*S<pi[0]<=pi[1]<4*S
    assert 0<theta[0]<=theta[1]<pi[0]//2
    gamma=div(theta,scale(pi,2))
    assert 0<gamma[0]<=gamma[1]<S//4
    # For each gamma in the interval: |q gamma - pn| <= err/S.
    err=max(abs(q*gamma[0]-pn*S),abs(q*gamma[1]-pn*S))
    strict_margin=S-q*err
    assert strict_margin>0, '1/q² inequality not established at this precision'
    # For every target circle angle the closest of q rational grid points is
    # <=1/(2q); actual orbit k gamma differs by <1/q, including k=q for 0.
    # Norm error <3pi/q<12/q<2^-20075 from q>=2^20079.
    assert 12*(1<<20075)<q
    # For a computably approximated target using <=1/q grid rounding error,
    # operator error <4pi/q<16/q<2^-20075.
    assert 16*(1<<20075)<=q
    return {'status':'PASS_RIGOROUS_UNIFORM_POSITIVE_GOLDEN_POWER_GRID',
       'proof_uses_float':False,'proof_integer_backend':'gmpy2 '+gmpy2.version(),
       'precision_bits':BITS,'series_terms':{'theta_reduced':nt,'atan_1_over_5':n5,'atan_1_over_239':n239},
       'candidate_source_certificate_sha256':sha256(raw).hexdigest(),
       'candidate_source_generator_sha256':sha256((DIRECT/'round38/certify_post_angles.py').read_bytes()).hexdigest(),
       'owner_phase_compiler_sha256':sha256(PHASE.read_bytes()).hexdigest(),
       'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
       'numerator_hex':hex(pn),'denominator_hex':hex(q),'denominator_bits':q.bit_length(),
       'gcd':1,'theta_interval_hex':[hex(int(t)) for t in theta],
       'pi_interval_hex':[hex(int(t)) for t in pi],
       'gamma_interval_hex':[hex(int(t)) for t in gamma],
       'abs_qgamma_minus_numerator_bound_numerator_hex':hex(int(err)),
       'abs_qgamma_minus_numerator_bound_denominator_pow2':BITS,
       'strict_1_over_q_squared_margin_hex':hex(int(strict_margin)),
       'gamma_approximation':'abs(gamma-pn/q)<1/q^2',
       'uniform_positive_exponent_range':'1 <= k <= q',
       'uniform_rotation_operator_error_strict_lt':'2^-20075',
       'computable_target_selection_operator_error_strict_lt':'2^-20075',
       'all_target_noncomputable_selection':'existence, or computable relative to target oracle',
       'full_SO_2m_compiler_or_A41_claimed':False,'physical_C_closed':False,'GR_closed':False}

if __name__=='__main__':
    out=certificate();(HERE/'UNIFORM_GOLDEN_GRID_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'precision_bits':BITS,'terms':out['series_terms'],
                      'denominator_bits':out['denominator_bits']}),flush=True)
