#!/usr/bin/env python3
"""Concrete positive Golden powers; floating point proposes, integers prove.

Ball radii enclose exact unit complex numbers.  If centres have radii r,s,
their product has radius <= r+s+rs plus the two coordinate-rounding errors.
No angular/transcendental approximation is trusted by the certificate.
"""
from pathlib import Path
from math import isqrt
from hashlib import sha256
import json, time
import mpmath as mp

P = Path(__file__).resolve().parent
ERROR_BITS = 20000
CANDIDATE_BITS = 20080


class Intervals:
    def __init__(self, bits):
        self.bits, self.S = bits, 1 << bits

    def q(self, n, d=1):
        return n*self.S//d, -((-n*self.S)//d)

    def add(self, a, b): return a[0]+b[0], a[1]+b[1]
    def neg(self, a): return -a[1], -a[0]
    def sub(self, a, b): return self.add(a, self.neg(b))

    def mul(self, a, b):
        v = [x*y for x in a for y in b]
        return min(v)//self.S, -((-max(v))//self.S)

    def div(self, a, b):
        assert b[0] > 0
        lo = min(x*self.S//y for x in a for y in b)
        hi = max(-((-x*self.S)//y) for x in a for y in b)
        return lo, hi

    def sqrt(self, a):
        assert a[0] >= 0
        return isqrt(a[0]*self.S), isqrt(a[1]*self.S)+1

    def pow(self, a, n):
        v = self.q(1)
        for _ in range(n): v = self.mul(v, a)
        return v


def native_base(I):
    p = I.div(I.sub(I.sqrt(I.q(5)), I.q(1)), I.q(2))
    return I.sqrt(p), p


def ball_mul(z, w, S):
    c, s, r = z; d, t, u = w
    bits=S.bit_length()-1
    assert S==1<<bits
    # Exact floor division by the positive binary scale, including negatives.
    return ((c*d-s*t)>>bits, (s*d+c*t)>>bits,
            r+u+-((-r*u)>>bits)+2)


def ball_power(k, bits):
    assert type(k) is int and k > 0
    I = Intervals(bits); c, s = native_base(I)
    base = c[0], s[0], c[1]-c[0]+s[1]-s[0]
    value = I.S, 0, 0
    while k:
        if k & 1: value = ball_mul(value, base, I.S)
        k >>= 1
        if k: base = ball_mul(base, base, I.S)
    return value


def targets(bits):
    I = Intervals(bits); one, two = I.q(1), I.q(2)
    root_half = I.sqrt(I.q(1, 2)); a, p = native_base(I)
    pi8 = (I.sqrt(I.div(I.add(one, root_half), two)),
           I.sqrt(I.div(I.sub(one, root_half), two)))
    pi6 = (I.div(I.sqrt(I.q(3)), two), I.q(1, 2))
    half = (I.sqrt(I.div(I.add(one, a), two)),
            I.sqrt(I.div(I.sub(one, a), two)))
    _, s512, radius = ball_power(512, bits)
    ss = (s512-radius, s512+radius)
    kappa = I.mul(ss, ss)
    cref = I.sub(one, I.mul(I.q(8), I.mul(kappa, I.pow(p, 7))))
    assert cref[0]*3 > 2*I.S and cref[1] <= I.S
    denom = I.add(one, cref)
    beta = (I.sqrt(I.div(cref, denom)), I.sqrt(I.div(one, denom)))
    return I, {'pi8':pi8, 'pi6':pi6, 'half_theta':half, 'beta':beta}


def candidates(bits=CANDIDATE_BITS):
    with mp.workprec(3*bits+256):
        p=(mp.sqrt(5)-1)/2; theta=mp.acos(mp.sqrt(p))
        gamma=theta/(2*mp.pi)
        cref=1-8*mp.sin(512*theta)**2*p**7
        turns={'pi8':mp.mpf(1)/16, 'pi6':mp.mpf(1)/12,
               'half_theta':gamma/2, 'beta':mp.atan(1/mp.sqrt(cref))/(2*mp.pi)}
        x=gamma; p0,p1,q0,q1=0,1,1,0; steps=0
        while True:
            a=int(mp.floor(x)); pn=a*p1+p0; qn=a*q1+q0; steps+=1
            if qn.bit_length()>=bits:
                inv=pow(pn,-1,qn)
                ks={name:(int(mp.floor(qn*turn+mp.mpf('0.5')))*inv)%qn
                    for name,turn in turns.items()}
                assert all(k>1 and k<qn for k in ks.values())
                return ks, qn, {'steps':steps,'numerator_hex':hex(pn),'denominator_hex':hex(qn)}
            p0,p1,q0,q1=p1,pn,q1,qn; x=1/(x-a)


def certify(ks, q, error_bits=ERROR_BITS):
    bits=max(k.bit_length() for k in [q,*ks.values()])+error_bits+128
    I, target=targets(bits); rows={}
    # Each inverse is certified directly, not assumed from a recurrence.
    exponents={name:k for name,k in ks.items()}
    exponents['minus_beta']=q-ks['beta']
    exponents['minus_half_theta']=ks['half_theta']-1
    exponents['minus_theta']=2*(ks['half_theta']-1)
    _, p = native_base(I); a=I.sqrt(p)
    target.update({'minus_beta':(target['beta'][0],I.neg(target['beta'][1])),
                   'minus_half_theta':(target['half_theta'][0],I.neg(target['half_theta'][1])),
                   'minus_theta':(a,I.neg(p))})
    for name,k in exponents.items():
        c,s,r=ball_power(k,bits); tc,ts=target[name]
        error=max(abs(c-tc[0]),abs(c-tc[1]))+max(abs(s-ts[0]),abs(s-ts[1]))+2*r
        assert error*(1<<error_bits)<I.S,(name,error.bit_length(),bits)
        rows[name]={'exponent_hex':hex(k),'exponent_bit_length':k.bit_length(),
                    'centre_cos_hex':hex(c),'centre_sin_hex':hex(s),'euclidean_radius_hex':hex(r),
                    'target_cos_interval_hex':[hex(x) for x in tc],
                    'target_sin_interval_hex':[hex(x) for x in ts],
                    'operator_error_L1_numerator_hex':hex(error),
                    'denominator_pow2':bits,'operator_error_strict_lt':f'2^-{error_bits}'}
        print('certified',name,k.bit_length(),flush=True)
    return {'precision_bits':bits,'rotations':rows}


def main():
    t=time.time(); print('proposing exact integer exponents',flush=True)
    ks,q,proposal=candidates(); print('candidate denominator bits',q.bit_length(),flush=True)
    out=certify(ks,q)
    out.update({'status':'PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS','error_bits':ERROR_BITS,
                'candidate_bits':CANDIDATE_BITS,'candidate_proposal_not_proof':proposal,
                'certificate_uses_floats':False,'certificate_uses_integer_outward_bounds':True,
                'word_uses_only_positive_integer_G_powers':True,
                'generator_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                'physical_C_closed':False,'GR_closed':False})
    (P/'POST_ANGLE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'precision_bits':out['precision_bits'],
                      'elapsed_seconds':round(time.time()-t,3)}),flush=True)


if __name__=='__main__': main()
