#!/usr/bin/env python3
"""B80 outward-integer proof at 32768-bit rotation accuracy.

The candidate comes from a continued fraction of an enclosing interval's
midpoint; only the subsequently verified integer inequalities are trusted.
"""
from pathlib import Path
from hashlib import sha256
from math import gcd
import importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
sys.path.insert(0,str(O/'round80/.deps'))
import gmpy2
B80=O/'round80/certify_uniform_golden_grid.py'
spec=importlib.util.spec_from_file_location('b112_b80_arithmetic',B80)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

def build(bits=67584):
    b.BITS=bits;b.S=gmpy2.mpz(1)<<bits;S=b.S
    one=b.rational(1);two=b.rational(2)
    p=b.div(b.sub(b.root(b.rational(5)),one),two)
    x=b.root(p)
    for _ in range(6):x=b.div(x,b.add(one,b.root(b.add(one,b.mul(x,x)))))
    theta,nt=b.atan_enclosure(x);theta=b.scale(theta,64)
    a5,n5=b.atan_enclosure(b.rational(1,5));a239,n239=b.atan_enclosure(b.rational(1,239))
    pi=b.sub(b.scale(a5,16),b.scale(a239,4))
    assert 3*S<pi[0]<=pi[1]<4*S and 0<theta[0]<=theta[1]<pi[0]//2
    gamma=b.div(theta,b.scale(pi,2));lo,hi=gamma
    assert 0<lo<=hi<S//4
    # Continued fraction of (lo+hi)/(2S), certified against ALL gamma
    # in [lo/S,hi/S], not trusted merely because it is a convergent.
    aa,bb=lo+hi,2*S;p0,p1=0,1;q0,q1=1,0;steps=0
    while bb:
        quotient,aa,bb=aa//bb,bb,aa%bb
        pn=quotient*p1+p0;q=quotient*q1+q0;steps+=1
        p0,p1=p1,pn;q0,q1=q1,q
        if q>16*(gmpy2.mpz(1)<<32768):
            E=max(abs(q*lo-pn*S),abs(q*hi-pn*S))
            if gcd(int(pn),int(q))==1 and q*E<S:break
    else:raise ArithmeticError('increase dyadic precision; no certified candidate')
    pn,q,E=map(int,(pn,q,E));inv=pow(pn,-1,q)
    j8=(q+8)//16;k8=(j8*inv)%q or q
    assert abs(16*j8-q)<=8 and 1<=k8<=q
    assert 16*(1<<32768)<q and q*E<int(S)
    return {'status':'PASS_32768_POSITIVE_G_GRID_AND_PI8',
            'precision_bits':bits,'theta_series_terms':nt,'pi_series_terms':[n5,n239],
            'candidate_CF_steps':steps,'numerator_hex':hex(pn),'denominator_hex':hex(q),
            'denominator_bits':q.bit_length(),'gcd':1,
            'gamma_interval_hex':[hex(int(lo)),hex(int(hi))],
            'pi_interval_hex':[hex(int(v)) for v in pi],
            'theta_interval_hex':[hex(int(v)) for v in theta],
            'error_numerator_hex':hex(E),'strict_margin_hex':hex(int(S)-q*E),
            'pi8_cell_hex':hex(j8),'pi8_exponent_hex':hex(k8),
            'uniform_and_pi8_G_operator_error_strict_lt':'2^-32768',
            'proof':'exact B80 dyadic enclosure; gcd=1, q*E<2^bits and 16*2^32768<q',
            'proof_uses_floating_point':False,'physical_C_closed':False,'GR_closed':False,
            'input_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),B80]}}

if __name__=='__main__':
    out=build();(P/'GRID_32768_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','precision_bits','denominator_bits','candidate_CF_steps','theta_series_terms','pi_series_terms')}),flush=True)
