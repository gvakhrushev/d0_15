"""FULL TWO individually retained Golden stage flags on the same ORIGINAL
six-plaquette/42-field real-CAR N1 source, original rational h0 collar.

This changes only the reported future algebra from coarse OR to BOTH
actual two-tick factor outcomes. It has four retained positive outcomes,
the literal original F/R 0/10 code costs on BOTH flags, and the fully
measured Shannon information of that FOUR-outcome record.

Same original p=phi^-1, zeta=2^-20, sigma-minus, six based SO+(1,3)
plaquettes, full 16 coframe+24 proper link+2 real matter coordinates.
No invented Book03 H+J+R, controller, primitive writer or renormalization.
"""
from __future__ import annotations
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/"d0_full42_interval_banach_2026-10-22"
sys.path.insert(0,str(ORIGINAL))
from certified_model import CQ as OriginalCQ, COLLAR
from center_pinned import get_center

CENTER={"z42":get_center()}
assert len(CENTER["z42"])==42

class CompleteTwoFlagCQ(OriginalCQ):
    def __init__(self,ctx,weights=("1","1")):
        super().__init__(ctx,weights)
        p=self.p;zz=self.Z
        L=4*p**3
        A=L+(1-L)*L
        self.a0=zz*A
        self.b0=zz*L
        self.entfine0=self._ent(self.a0)+self._ent(self.b0)

    def _ent(self,v):
        C=self.c
        return -(v*C.log(v)+(1-v)*C.log(1-v))/self.lp

    def price(self,z):
        C=self.c
        e,U,ps=self.nodes(z)
        result=self.m(0)
        records=[]
        for j in (0,1):
            co=self.E[0] if j==0 else e
            us=self.U[0] if j==0 else U
            vs=U if j==0 else self.U[2]
            f=self.curvature(co,us,vs)
            g=(co.T*self.eta*co)**-1
            q=C.mpc(0) if C is not __import__("mpmath").mp else C.mpc(0)
            for k in (0,1):
                v=C.matrix([(ps[j+1][k]-ps[j][k])/self.h,
                           self.amp if k==1 else self.m(0),0,0])
                q+=(v.T*g*v)[0]
            rho=self.rho[j]
            # ORIGINAL canonical G2STAR sign is f_C, not null EPS_PLUS f_B.
            x=-self.tau*f/rho
            y=self.tau*q/rho
            E=self.p*self.p*(1+x)
            ell=4*E*(1-E)
            b=self.p-self.p*self.p*y
            B=4*b*b*(1-b*b)
            A=ell+(1-ell)*B
            a=self.Z*A
            bb=self.Z*B
            # Paired cost 2+a+b, entropy H(a)+H(b).
            # Original scalar normalization norm is negative; no new source
            # coefficient, no ignored flags, no field-dependent counterterm.
            result+=self.norm*rho*(self._ent(a)+self._ent(bb)-self.entfine0-
                                  ((a+bb)-(self.a0+self.b0)))
            records.append((a,bb,f,q))
        self.last_records=records
        return result

def rational_center(ctx):
    return [ctx.mpf(v) for v in CENTER["z42"]]
