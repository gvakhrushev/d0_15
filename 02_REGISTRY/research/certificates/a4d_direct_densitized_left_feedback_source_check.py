#!/usr/bin/env python3
"""One native two-tick AF×scene J2: pressure-inclusive scalar density source.

Target: A4D_DIRECT_DENSITIZED_LEFT_FEEDBACK_EINSTEIN_SCALAR_SOURCE_2026_10_18.md.
Finite full price uses BOTH Q,R log terms and original golden constants.
This checks analytic identities and hostile scalar-pressure controls.
It does not execute a physically admitted original full D0 Book programme.
"""
from math import sqrt, log
import json

p = (sqrt(5)-1)/2
z = 2**-20
L = 4*p**3
a = p**6
Q0 = 1-z*L
R0 = 1-z*(L+a*L)
assert abs(p+p*p-1)<1e-15
assert abs(a-(1-L))<1e-15
assert Q0>0 and R0>0

C_g = z*4*p**11/R0
C_m = 8*z*p**6*(1/Q0+a/R0)
coupling = C_m/C_g
assert abs(coupling-23.416406751884075)<3e-11

def potential(u, v, sigma, t2):
    E = p*p*(1+t2*u)
    b = (p+sigma*p*p*t2*v)**2
    B = 4*b*(1-b)              # TWO actual scene ticks, not B=b
    lam = 4*E*(1-E)
    Q = 1-z*B
    R = 1-z*(lam+(1-lam)*B)
    assert Q>0 and R>0
    return -log(Q/Q0)-log(R/R0)

# Analytic first source of BOTH log terms at u=v=0.
for sg in (1, -1):
    for t2 in (.01, .25):
        h=1e-4
        du=(potential(h,0,sg,t2)-potential(-h,0,sg,t2))/(2*h)
        dv=(potential(0,h,sg,t2)-potential(0,-h,sg,t2))/(2*h)
        assert abs(du-C_g*t2)<2e-11
        assert abs(dv-sg*C_m*t2)<2e-11

# Exact grouped trace identity Σ_i π_i (A_x/w_x) = Σ_x A_x,
# and identical identity for real volume-weighted matter M_x.
weights=(.21,.37,.42)
Acell=(.03,-.02,.04)
Mcell=(-.06,.07,.05)
T=.001
for strength in (1.,.5,.25):
    J=sum(w*potential(strength*A/w,strength*M/w,1,T)
          for w,A,M in zip(weights,Acell,Mcell))
    linear=T*strength*(C_g*sum(Acell)+C_m*sum(Mcell))
    assert abs(J-linear)<2e-10

# The exact perspective derivative at its joint zero is independent
# of all δweights: d[w Φ(A/w,M/w)] = t²(Cg δA+Cm δM).
w=.3; dA=.017; dM=-.021; dw=.039
for h in (1e-4,1e-5):
    pos=(w+h*dw)*potential(h*dA/(w+h*dw),h*dM/(w+h*dw),1,T)
    neg=(w-h*dw)*potential(-h*dA/(w-h*dw),-h*dM/(w-h*dw),1,T)
    dJ=(pos-neg)/(2*h)
    expect=T*(C_g*dA+C_m*dM)
    assert abs(dJ-expect)<2e-10

# Exact finite inherited sourced pp-wave: at f=q=0,J=1,
# every coframe/link/scalar field differential is rescaled by h4/wbar,
# independently of site weight and of δdet(e) as q=0.
ws=[.2,.3,.5]
wbar=sum(ws)/3
h4=1/3
Dgeom=[2.,-1.1,3.]
Dmatter=[.5,1.2,-.7]
for wi,dg,dm in zip(ws,Dgeom,Dmatter):
    old_u=wbar*dg/wi
    old_v=wbar*dm/wi
    new_u=h4*dg/wi
    new_v=h4*dm/wi
    assert abs((new_u+coupling*new_v)
             -(h4/wbar)*(old_u+coupling*old_v))<1e-12

# Independent full scalar-pressure hostile test:
# ehat=diag(1,s,1,1), J=s, phi=alpha*t => q=alpha².
# Flat links make Pstar=0. The ORIGINAL q-only input is independent
# of spatial s (WRONG general scalar pressure); new J*q input responds.
site_w=.3; alpha2=.01; probe=.1; e=1e-4
old=lambda s:site_w*potential(0,alpha2/site_w,1,probe)
new=lambda s:site_w*potential(0,s*alpha2/site_w,1,probe)
old_pressure=(old(1+e)-old(1-e))/(2*e)
new_pressure=(new(1+e)-new(1-e))/(2*e)
linear_pressure=probe*C_m*alpha2
assert old_pressure==0
assert new_pressure>0
assert abs(new_pressure-linear_pressure)<.015*linear_pressure

# Exact mixed geometric/matter feedback Hessian at u=v=0,
# independent of input magnitudes: calculated from both Q and R logs.
B_v=8*p**6
B_vv=8*p**6*(p-4)
lambda_u=p*p*L
H_uu=-8*z*a*p**4/R0+(z*a*lambda_u/R0)**2
H_uv=-z*(1-z)*lambda_u*B_v/R0**2
H_vv=z*B_vv*(1/Q0+a/R0)+z*z*B_v**2*(1/Q0**2+a*a/R0**2)
det=H_uu*H_vv-H_uv**2
assert H_uu<0 and H_uv<0 and H_vv<0 and det>0
T2=.1; h=.02
mixed_difference=(
 potential(h,h,1,T2)-potential(h,-h,1,T2)
 -potential(-h,h,1,T2)+potential(-h,-h,1,T2)
)/(4*h*h)
assert abs(mixed_difference-H_uv*T2*T2)<4e-11

# CERTIFIED ARCHIVE JENSEN CONTROL: same full J2, actual p,p² split,
# on ONE common regular/PF projective source chart. Across different
# defining GNS trace N, separate weight comparison remains required.
wparent=p;wF=p*p;wR=p**3
assert abs(wF+wR-wparent)<3e-16
for probe2 in (.1,1.):
    u0,v0=.13,-.09
    coarse=wparent*potential(u0,v0,1,probe2)
    fine=wF*potential(u0,v0,1,probe2)+wR*potential(u0,v0,1,probe2)
    assert abs(coarse-fine)<3e-16
for dg,dm in ((.02,-.02),(.1,-.08),(.2,-.15)):
    uF,vF=dg,dm
    uR,vR=-wF/wR*dg,-wF/wR*dm
    assert abs(wF*uF+wR*uR)<2e-16
    assert abs(wF*vF+wR*vR)<2e-16
    fine=wF*potential(uF,vF,1,1)+wR*potential(uR,vR,1,1)
    assert fine<0
    if dg==.1:
        assert abs(-fine-4.1805724395e-9)<1e-12

# Rational enclosure for exact golden p, with p²+p−1 sign isolation.
# All following interval endpoints remain Fraction, not floating output.
from fractions import Fraction as F
class I:
    def __init__(self,lo,hi=None):
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def cv(x):
        return x if isinstance(x,I) else I(x)
    def __add__(self,o):
        o=self.cv(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):
        return I(-self.hi,-self.lo)
    def __sub__(self,o):
        return self+-self.cv(o)
    def __rsub__(self,o):
        return self.cv(o)+-self
    def __mul__(self,o):
        o=self.cv(o)
        v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.cv(o)
        assert o.lo>0
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):
        return self.cv(o)/self
    def __pow__(self,n):
        assert n>=0
        res=I(1)
        for _ in range(n):
            res=res*self
        return res

ip=I(F(61803398,10**8),F(61803400,10**8))
assert ip.lo*ip.lo+ip.lo<1 and ip.hi*ip.hi+ip.hi>1
iz=I(F(1,2**20));iL=4*ip**3;ia=ip**6
iQ=1-iz*iL;iR=1-iz*iL*(1+ia)
ig1=ip**2*iL;im1=8*ip**6;im2=8*ip**6*(ip-4)
ihgg=-8*iz*ia*ip**4/iR+(iz*ia*ig1/iR)**2
ihgm=-iz*(1-iz)*ig1*im1/iR**2
ihmm=iz*im2*(1/iQ+ia/iR)+iz*iz*im1*im1*(1/iQ**2+ia*ia/iR**2)
ideter=ihgg*ihmm-ihgm**2
assert ihgg.hi<0 and ihmm.hi<0 and ideter.lo>0

print(json.dumps({
  "status":"PASS",
  "scope":"single full J2 source; physical selection and whole Book OPEN",
  "native_z":"2^-20",
  "original_two_tick_scene_effect":"B=4b(1-b)",
  "relative_coupling":coupling,
  "true_pressure_old_q_only":old_pressure,
  "true_pressure_new_density":new_pressure,
  "linear_pressure_comparator":linear_pressure,
  "mixed_feedback_hessian_per_t4":[[H_uu,H_uv],[H_uv,H_vv]],
  "mixed_feedback_hessian_det_per_t8":det,
  "null_ppwave_all_Euler_transfer":"exact same first-source up to h^4/wbar",
  "uniform_C2_GR_scalar_source_limit":"conditional on bounded cell/weight ratios",
  "archive_refinement_concavity_certified": True,
  "archive_variance_sign":"fine price <= coarse price within negative-Hessian window",
  "interval_hessian_determinant":[float(ideter.lo),float(ideter.hi)],
  "GR_physically_derived":False
},indent=2,sort_keys=True))
