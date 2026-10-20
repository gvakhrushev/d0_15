#!/usr/bin/env python3
"""Original 718-edge scalar Book CP amplitude: sign of exact Perron source.
No physical alpha identification, no actual full Book03/GR action.
"""
import mpmath as m
m.mp.dps=70
ell=m.log((1+m.sqrt(5))/2)
S=m.mpf(359); B0=m.mpf(2574)
def calc(e):
    B=B0*m.cosh(3*ell*e)
    rho=m.findroot(lambda r:r**3-S*r-B,22)
    D=3*rho*rho-S
    a=1-m.log(rho)/ell
    deriv=-3*B0*m.sinh(3*ell*e)/(rho*D)
    return a,deriv,rho,D
assert abs(calc(0)[1])<m.mpf('1e-65')
a2=-9*ell*B0/(calc(0)[2]*calc(0)[3])
assert abs(a2+m.mpf('0.4763744515526456'))<m.mpf('1e-12')
for ep in ['0.0004152168623563978651658360647953866','.01','.1','.5','.99']:
    e=m.mpf(ep)
    assert calc(e)[1]<0 and calc(-e)[1]>0
    assert abs(calc(e)[0]-calc(-e)[0])<m.mpf('1e-60')
    assert abs(m.diff(lambda x:calc(x)[0], e)-calc(e)[1])<m.mpf('1e-55')
print('PASS_CP_SCALAR_BOOK_STABILITY_NOGO')
print('A_second_0=',m.nstr(a2,50))
print('A_prime_abs_Delta_alpha=',m.nstr(calc(m.mpf('0.0004152168623563978651658360647953866'))[1],50))
print('FIREWALL: full physically selected action, actual epsilon field freedom and GR unproved')
