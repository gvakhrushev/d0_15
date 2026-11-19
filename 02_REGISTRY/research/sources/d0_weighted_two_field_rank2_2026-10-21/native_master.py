"""Pinned original cap-one probability polynomial and its stationary master.

The sigma=-1 orientation is INSIDE F. Thus its second input y is the
positive signed kinetic contraction tau*q/rho, exactly as in the current
WEIGHTED_WARD_AND_DUST owner. This module is not a native gate compiler.
"""
from __future__ import annotations
import mpmath as mp


class GoldenMaster:
    def __init__(self, precision: int = 70) -> None:
        mp.mp.dps = precision
        self.p = (mp.sqrt(5)-1)/2
        self.z = mp.mpf(2)**-20
        self.lnphi = mp.log(1/self.p)
        p = self.p
        self.alpha = (1-(1-2*p**3)**9)**128
        self.beta = ((1-p**120)**4*(1-(1-16*p**9)**20))**43
        self.r0 = self.raw_probability(mp.mpf(0), mp.mpf(0))
        self.a = self.fx(0, 0)
        self.b = self.fy(0, 0)
        self.ratio = self.b/self.a
        self.kappa = -self.ratio
        self.hxx = mp.diff(lambda x: self.fx(x, 0), 0)
        self.hxy = mp.diff(lambda y: self.fx(0, y), 0)
        self.hyy = mp.diff(lambda y: self.fy(0, y), 0)
        self.k2 = self.hyy+2*self.ratio*self.hxy+self.ratio**2*self.hxx
        self.u1 = (self.hxy+self.ratio*self.hxx)/self.a

    def raw_probability(self, x, raw_y):
        p,z = self.p,self.z
        by = 4*(p+p*p*raw_y)**2*(1-(p+p*p*raw_y)**2)
        ell = 4*p*p*(1+x)*(1-p*p*(1+x))
        ax = ell+(1-ell)*by
        return 1-(1-z*by)*(1-z*ax)

    def entropy(self, r):
        if not 0 < r < 1:
            raise ValueError('Probability outside the declared faithful chart')
        return -(r*mp.log(r)+(1-r)*mp.log1p(-r))/self.lnphi

    def F(self, x, y):
        # One and only one insertion of the negative material orientation.
        return -self.alpha*self.beta*(self.entropy(self.raw_probability(x,-y))-self.entropy(self.r0))

    def fx(self, x, y):
        return mp.diff(lambda v: self.F(v,y), x)

    def fy(self, x, y):
        return mp.diff(lambda v: self.F(x,v), y)

    def section(self, t):
        t = mp.mpf(t)
        if t == 0:
            return mp.mpf(0),mp.mpf(1),mp.mpf(0),self.b
        def equations(x,u):
            return self.fx(x,u*t)/self.a-u, x-t*self.fy(x,u*t)/self.a
        x,u = mp.findroot(equations,(self.ratio*t,1+self.u1*t),tol=mp.mpf('1e-58'),maxsteps=45)
        if u <= 0:
            raise ArithmeticError('Left the positive stationary coframe chart')
        value = self.F(x,u*t)-self.a*u*x
        derivative = u*self.fy(x,u*t)
        return x,u,value,derivative
