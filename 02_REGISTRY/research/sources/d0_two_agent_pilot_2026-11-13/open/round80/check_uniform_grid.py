#!/usr/bin/env python3
"""Replay, rational fixtures, Machin identity and modular-grid witness."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
p=P/'certify_uniform_golden_grid.py'
spec=importlib.util.spec_from_file_location('b80_certificate',p);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
certpath=P/'UNIFORM_GOLDEN_GRID_CERTIFICATE.json'
a=json.loads(certpath.read_text());assert a==c.certificate()
q=int(a['denominator_hex'],16);pn=int(a['numerator_hex'],16);err=int(a['abs_qgamma_minus_numerator_bound_numerator_hex'],16)
assert err*q < 1<<a['precision_bits']
assert pow(pn,-1,q)*pn%q==1
# Machin: (5+i)^4(239-i)=114244(1+i), with both argument factors positive.
def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
z=(1,0)
for _ in range(4):z=cmul(z,(5,1))
z=cmul(z,(239,-1));assert z==(114244,114244)
# Cross-check interval sums against exact rational alternating-series
# enclosures at small dyadic precision. No float/trig is used.
c.BITS=256;c.S=c.gmpy2.mpz(1)<<256
for num,den,N in ((1,5,100),(1,239,30),(3,4,500)):
    x=F(num,den);partial=sum(((-1)**i*x**(2*i+1)/F(2*i+1) for i in range(N)),F())
    remainder=x**(2*N+1)/F(2*N+1)
    bounds,terms=c.atan_enclosure(c.rational(num,den));lo,hi=(F(int(k),1<<256) for k in bounds)
    assert lo<=partial-remainder<partial+remainder<=hi
    assert terms>0
# Elementary half-angle relation on a rational x, using interval arithmetic.
x=c.rational(3,4);one=c.rational(1);y=c.div(x,c.add(one,c.root(c.add(one,c.mul(x,x)))))
recovered=c.div(c.scale(y,2),c.sub(one,c.mul(y,y)))
assert recovered[0]<=x[0] and recovered[1]>=x[1]
# Modular selection fixture: deterministic rounding, zero mapped to q.
def circ(x):return min(x%1,(-x)%1)
for Q,N in ((13,5),(17,7),(29,11)):
    gamma=F(N,Q)+F(1,2*Q*Q)
    assert abs(gamma-F(N,Q))<F(1,Q*Q)
    for i in range(101):
        tau=F(i,101);x=Q*tau
        j=(2*x.numerator+x.denominator)//(2*x.denominator)%Q
        k=(j*pow(N,-1,Q))%Q
        if k==0:k=Q
        assert 1<=k<=Q and circ(k*gamma-tau)<F(3,2*Q)
print(json.dumps({'status':'PASS_B80_REPLAY_INTEGER_FIXTURES_AND_MODULAR_GRID',
                  'certificate_sha256':sha256(certpath.read_bytes()).hexdigest()}))
