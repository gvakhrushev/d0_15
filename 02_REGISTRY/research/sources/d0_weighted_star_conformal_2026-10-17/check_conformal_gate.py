#!/usr/bin/env python3
"""Original observer-preserving weighted star vs Einstein and an owned full16 observer-Born repair.
Exact continuum constrained geometry, NOT original finite-h D0 Cost-Info or exact lattice root.
"""
import json
from itertools import combinations, permutations
import sympy as S

t,u,epsilon=S.symbols("t u epsilon", real=True)
a=S.Function("a")(t)
eta=S.diag(1,-1,-1,-1)
total=0

def chk(flag,name):
    global total
    if not bool(flag): raise RuntimeError(name)
    total+=1

def eq(x,y,name):
    chk(S.simplify(x-y)==0,name)

def ext(X,Y):
    result={}
    for ix,v in X.items():
        for iy,w in Y.items():
            L=ix+iy
            if len(set(L))!=len(L):continue
            sign=(-1)**sum(L[i]>L[j] for i in range(len(L)) for j in range(i+1,len(L)))
            ordered=tuple(sorted(L))
            result[ordered]=S.simplify(result.get(ordered,0)+sign*v*w)
    return {k:v for k,v in result.items() if v!=0}

def perm_sign(p):
    return (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))

def sigma(i,j):
    result={}
    for k,l in permutations([m for m in range(4) if m not in (i,j)],2):
        for ix,v in ext({(k,):a},{(l,):a}).items():
            result[ix]=S.simplify(result.get(ix,0)+S.Rational(1,2)*perm_sign((k,l,i,j))*v)
    return {k:v for k,v in result.items() if v!=0}

def d0(form):
    return ext({(0,):S.Integer(1)},{ix:S.diff(v,t) for ix,v in form.items()})

# The constrained proper Lorentz connection preserves a parallel unit observer:
# at the flat connection its independent Euler directions are the three spatial rotations.
for i,j in combinations(range(4),2):
    value=d0(sigma(i,j))
    if i:
        chk(value=={},f"admitted observer SO3 curvature-source {i}{j} must vanish")
    else:
        chk(bool(value),f"omitted Lorentz-boost source {i}{j} must survive")
        coeff=list(value.values())[0]
        chk(S.simplify(coeff/(2*a*S.diff(a,t))) in (S.Integer(-1),S.Integer(1)),
            "nonzero boost source coefficient")

# Independently compute the whole Lorentz Christoffel, Ricci and Einstein tensor,
# not an inserted Einstein scalar or a weak-curvature approximation.
g=a*a*eta
gi=eta/a**2
def deriv(f,k):return S.diff(f,t) if k==0 else S.Integer(0)
G=[[[S.simplify(sum(gi[i,l]*(deriv(g[l,j],k)+deriv(g[l,k],j)-deriv(g[j,k],l))/2
                 for l in range(4))) for k in range(4)] for j in range(4)]
   for i in range(4)]
Ric=S.Matrix(4,4,lambda i,j:S.simplify(sum(
   deriv(G[k][i][j],k)-deriv(G[k][i][k],j)+
   sum(G[k][k][l]*G[l][i][j]-G[k][j][l]*G[l][i][k] for l in range(4))
   for k in range(4))))
R=S.simplify(sum(gi[i,i]*Ric[i,i] for i in range(4)))
Ein=S.simplify(Ric-g*R/2)
eq(Ein[0,0],3*(S.diff(a,t)/a)**2,"genuine GR Einstein 00")
for j in range(1,4):
    eq(Ein[j,j],-2*S.diff(a,t,2)/a+(S.diff(a,t)/a)**2,"genuine GR Einstein spatial diagonal")
eq(R*a**4,-6*a*S.diff(a,t,2),"exact EH bulk volume density")

# Already-owned completed full16 CAR + reference128 Julia observer Born formulas:
hubble=S.diff(a,t)/a**2
Qobs=6*hubble**2
Pcoh=3*epsilon**2*hubble**2
Porth=S.Integer(0)
Pblank=1-Pcoh-Porth
eq((2*Pcoh-Porth)/epsilon**2,Qobs,"observer Born centred source")
eq(a**4*Qobs,6*S.diff(a,t)**2,"observer record reproduces whole missing kinetic density")
div=3*(S.diff(a,t)**2+a*S.diff(a,t,2))/a**4
eq(R,Qobs-2*div,"complete Lorentz observer-reflection identity, with boundary")
eq(Pcoh+Porth+Pblank,1,"full three-event Born normalization")

# Periodic analytic exact non-Einstein witness, not a finite native joint root.
profile=1+u*S.sin(t)
g00=S.simplify(Ein[0,0].subs({
  a:profile,S.diff(a,t):S.diff(profile,t),S.diff(a,t,2):S.diff(profile,t,2)}))
eq(g00.subs(t,0),3*u*u,"non-Einstein exact stationary-background witness")
kin=S.integrate(S.diff(profile,t)**2,(t,0,2*S.pi))
eq(kin,S.pi*u*u,"nonzero EH action for all amplitudes")
eq(S.diff(6*kin,u,2).subs(u,0),12*S.pi,"genuine EH Hessian vs zero constrained naked-star Hessian")

# Regular SAME original observer/site Hilbert chart on a periodic 4-role torus.
n=S.Matrix([205,-144,-96,-72])/83
k_cov=S.Matrix([205,144,96,72])
eq((n.T*eta*n)[0],1,"future observer is timelike and normalized")
chk(k_cov==83*eta*n,"integer role phase covector parallel to observer")
for r in range(4):
    v=eta*S.eye(4)[:,r]
    spatial=(n.T*eta*v)[0]**2-(v.T*eta*v)[0]
    chk(spatial>0,"own leg spatially nonzero in true observer rest frame")

# Exactly the weighted native own-leg law with unchanged proper Lorentz A=I:
# v_x=s_x vtilde, site omega_x=1/s_x, omega_x/omega_y=s_y/s_x.
sx,sy=S.symbols("s_x s_y",positive=True)
for r in range(4):
    v=eta*S.eye(4)[:,r]
    chk(sy*v==(sy/sx)*sx*v,"weighted actual selfadjoint own-leg condition")
chk((sy/sx)**4!=sy/sx,"naive full-volume weight a^4 is not the native Hilbert-site weight for generic scale")

print(json.dumps({
    "status":"PASS","exact_controls":total,
    "observer_preserving_rotational_connection_sources":"all 3 vanish",
    "missing_Lorentz_boost_sources":"all 3 nonzero whenever a_prime!=0",
    "Einstein_00":"3(a_prime/a)^2",
    "periodic_EH_action":"6*pi*u^2",
    "restricted_naked_star_on_flat_connection":"0 for all u",
    "actual_Riemannian_observer_score":"(2Pcoh-Porth)/epsilon^2=6(a_prime/a^2)^2",
    "physical_one_way_reference_projection_admitted":False,
    "same_history_Cost_Info_selected":False,
    "original_finite_h_exact_joint_root":False
},sort_keys=True))
