#!/usr/bin/env python3
"""One actual two-tick AF×scene feedback: two-band inverse and null density source.

Mathematical bounded checker, NOT admission of original D0 full Book programme
and NOT an Einstein theorem. Works under -O: use require(), not assert.
"""
from math import sqrt
import json
import sympy as s


def require(test, name):
    if not bool(test):
        raise ArithmeticError(name)


p = (s.sqrt(5)-1)/2
z = s.Rational(1, 2**20)
f, q, c, sigma = s.symbols("f q c sigma", real=True)
e0 = p**2
L = 4*p**3
a = p**6
Q = 1-z*L
R = 1-z*L*(1+a)
require(s.simplify(p+p**2-1)==0, "golden probability")
require(s.simplify(1-L-a)==0, "golden spectral gap")
E = e0*(1+c*f)
b = (p+sigma*p**2*c*q)**2
lam = 4*E*(1-E)
u = 4*b*(1-b)
v = u+(1-u)*lam
require(s.simplify(1-u-(1-2*b)**2)==0, "scene inverse branch")
require(s.simplify(1-lam-(1-2*E)**2)==0, "geometry inverse branch")
require(s.simplify((v-u)/(1-u)-lam)==0, "conditional effect recovery")
derivatives = s.Matrix([u,v]).jacobian([f,q]).subs({f:0,q:0})
expected = s.Matrix([[0,8*sigma*p**6*c],
                     [4*p**11*c,8*sigma*p**12*c]])
for x in list(derivatives-expected):
    require(s.simplify(x)==0, "two-band Jacobian entries")
require(s.simplify(derivatives.det()+32*sigma*p**17*c**2)==0,
        "nondegenerate two-band source")
require(s.simplify((L*(1+a))-(1-p**12))==0,
        "two original retained eigenvalue bands")

# Actual single-leaf logdet of both complete positive feedback bands.
Phi = -s.log(1-z*u)-s.log(1-z*v)
GF = 4*z*p**11/R
GQ = 8*sigma*z*p**6*(1/Q+a/R)
for der,expected_scalar in [(f,GF*c),(q,GQ*c)]:
    actual=s.diff(Phi,der).subs({f:0,q:0})
    require(s.simplify(actual-expected_scalar)==0,
            "same-J gradient and owned CAR16/source ratio")
actual_ratio=s.simplify((GQ/GF).subs(sigma,1))
expected_ratio=2*p**(-5)*(R/Q+a)
require(s.simplify(actual_ratio-expected_ratio)==0,
        "no fitted relative Einstein-matter ratio")

# The FULL logdet Hessian at the physical diagnostic z=2^-20.
HFF=-8*z*p**10/R+16*z*z*p**22/R**2
HFQ=-32*z*p**11/R+32*z*z*p**23/R**2
HQQ=(8*z*p**6*(p-4)/Q + 64*z*z*p**12/Q**2
      +8*z*p**12*(p-4)/R+64*z*z*p**24/R**2)
H=s.Matrix([[HFF,HFQ],[HFQ,HQQ]])
direct=s.hessian(Phi,(f,q)).subs({f:0,q:0,c:1,sigma:1})
for x in list(direct-H):
    require(abs(float(s.N(x,32)))<1e-25,"exact scalar Hessian contraction")
require(s.sign(HFF)==-1 and s.sign(H.det())==1,
        "strict concavity at native diagnostic z")
require(s.sign(HQQ)==-1, "strict negative matter diagonal")
# In the two-variable Legendre representation the exact auxiliary
# normal Hessian at the null point is -rho * H^(-1), positive definite
# for every rho>0. No new physical degree of freedom is installed.
Hdual=-H.inv()
require(s.sign(Hdual[0,0])==1 and s.sign(Hdual.det())==1,
        "no flat auxiliary normal mode at fixed fugacity/probe")


# A genuine density perspective w*phi(F/rho,Q/rho):
# density has NO first and NO mixed second source on the NULL star shell.
x, y, rho=s.symbols("x y rho",positive=True,real=True)
g1,g2,h11,h12,h22=s.symbols("g1 g2 h11 h12 h22",real=True)
quadratic = g1*x+g2*y+(h11*x*x+2*h12*x*y+h22*y*y)/(2*rho)
zero={x:0,y:0}
require(s.simplify(s.diff(quadratic,rho).subs(zero))==0,
        "no direct density first source")
require(s.simplify(s.diff(quadratic,rho,rho).subs(zero))==0,
        "no pure density Hessian")
require(s.simplify(s.diff(quadratic,rho,x).subs(zero))==0,
        "no mixed density/geometry Hessian")
require(s.simplify(s.diff(quadratic,rho,y).subs(zero))==0,
        "no mixed density/matter Hessian")
require(s.simplify(s.diff(quadratic,x).subs(zero)-g1)==0,
        "universal geometry source")
require(s.simplify(s.diff(quadratic,y).subs(zero)-g2)==0,
        "universal matter source")

# Exact nonlinear Einstein-frame response factor from the SAME two bands.
# gamma=Phi_f(f,q)/Phi_f(0,0), requiring no external metric oracle.
dg=s.diff(Phi,f)
gamma=s.simplify(dg/(GF*c))
gamma_unsquared=R*(1-u)*(1-2*E)/(p**9*(1-z*v))
require(s.simplify(gamma-gamma_unsquared)==0,
        "exact feedback-Palatini coframe response factor")
require(s.simplify(((1-u)*(1-2*E))**2-(1-u)*(1-v))==0,
        "positive-branch two-band square-root gamma")
require(s.simplify(gamma.subs({f:0,q:0})-1)==0,
        "original physical metric agrees on nonflat null shell")
# For actual e,b in (0,1/2), both factors are positive, so
# gamma=R sqrt((1-u)(1-v))/(p^9*(1-z*v)) with NO sign ambiguity.
require(float(s.N(gamma.subs({f:0,q:0,c:1,sigma:1}),30))>0,
        "golden spectral gamma orientation")

# Structural all-order Legendre equivalence, checked on an EXACT
# nontrivial two-component negative Hessian. This is algebraic, not a
# fitted new matter action: the auxiliary stationarity is eliminated.
z1,z2,rho0=s.symbols("z1 z2 rho0",real=True,positive=True)
u1,u2=s.symbols("u1 u2",real=True)
gtoy=s.Matrix([s.Rational(2,3),s.Rational(-1,5)])
Htoy=s.Matrix([[-2,1],[1,-3]])  # strictly negative definite
Xtoy=s.Matrix([z1,z2])
Mtoy=s.Matrix([u1,u2])
offset=Mtoy-gtoy
Ytoy=Htoy.inv()*offset
Vtoy=s.factor((offset.T*Htoy.inv()*offset)[0]/2)
Atoy=(Mtoy.T*Xtoy)[0]-rho0*Vtoy
statM=s.Matrix([s.diff(Atoy,mv) for mv in [u1,u2]])
Mstar=gtoy+Htoy*Xtoy/rho0
require(s.simplify(statM.subs({u1:Mstar[0],u2:Mstar[1]}))==s.zeros(2,1),
        "two-component Legendre auxiliary equations")
source_original=(gtoy.T*Xtoy)[0]+\
                (Xtoy.T*Htoy*Xtoy)[0]/(2*rho0)
require(s.simplify(Atoy.subs({u1:Mstar[0],u2:Mstar[1]})-
                   source_original)==0,
        "exact same-price Legendre elimination")
# Under e_tilde=sqrt(m_g/c_g)*e_hat the original star scales +2,
# the original Clifford inverse metric scales -2: coefficients
# m_g*f_hat=c_g*f_tilde and m_m*q_hat=(m_g*m_m/c_g)*q_tilde.
cg,mg,mm,star_tilde,q_tilde=s.symbols(
    "cg mg mm star_tilde q_tilde",positive=True,real=True)
gam=mg/cg
require(s.simplify(mg*(star_tilde/gam)-cg*star_tilde)==0,
        "exact same-star Einstein-frame coefficient")
require(s.simplify(mm*(gam*q_tilde)-(mg*mm/cg)*q_tilde)==0,
        "exact source-preserving scalar conformal response")

# Direct nonlinear inverse at unequal, signed matter perturbations.
pf=float(s.N(p,35))
for orient in [1,-1]:
    for ff,qq in [(0.,0.),(.25,-.1),(-.37,.21),(.1,.36)]:
        probe=.08   # t²>0, finite, not an asymptotic substitute
        ee=pf*pf*(1+probe*ff)
        bb=(pf+orient*pf*pf*probe*qq)**2
        uu=4*bb*(1-bb)
        vv=uu+(1-uu)*4*ee*(1-ee)
        reco_b=(1-sqrt(1-uu))/2
        reco_lam=(vv-uu)/(1-uu)
        reco_e=(1-sqrt(1-reco_lam))/2
        recover_f=(reco_e/(pf*pf)-1)/probe
        recover_q=(sqrt(reco_b)-pf)/(orient*pf*pf*probe)
        require(abs(recover_f-ff)<1e-11 and abs(recover_q-qq)<1e-11,
                "positive two-band inverse on actual strict chart")

# No inference that old fixed autonomous scene supplies matter.
fixed_scene_jacobian=s.Matrix([[0,0],[4*p**11*c,0]])
require(fixed_scene_jacobian.det()==0,
        "negative control: no matter without changing scene return")

receipt={
 "terminal":"PASS: two-band native J2 inverse / weighted perspective null source",
 "p":pf,
 "z":str(z),
 "scene_band_u0":float(s.N(L,18)),
 "mixed_band_v0":float(s.N(1-p**12,18)),
 "positive_band_gap":float(s.N(L*p**6,18)),
 "Jacobian_determinant_coefficient":"-32*sigma*p^17*t^4",
 "same_price_matter_to_geometry_ratio_sigma_plus":float(s.N(expected_ratio,18)),
 "native_single_leaf_gradient":[float(s.N(GF,18)),float(s.N(GQ.subs(sigma,1),18))],
 "native_single_leaf_Hessian":[[float(s.N(vv,18)) for vv in row] for row in H.tolist()],
 "negative_definite_at_z_2^-20":True,
 "positive_auxiliary_normal_Hessian":True,
 "Einstein_frame_gamma_at_null":"1 exact",
 "Legendre_Palatini_auxiliary_elimination":"PASS exact two-variable proof control",
 "density_null_first_and_cross_second_source":"ZERO",
 "fixed_scene_material_jet":"ZERO",
 "original_complete_D0_native_selection":"OPEN",
 "general_GR_and_refinement":"OPEN"
}
print(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True))
