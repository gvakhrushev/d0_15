#!/usr/bin/env python3
"""D0: uniform coframe-only SO(1,3) 42->36 Ward, genuine metric10 chart,
and full-two-scalar source control, with NO special null-support premise.
Only mathematical source reduction; Book03 selection/GR remain open.
"""
import sympy as S
A,B,C,D=S.symbols('A B C D',positive=True)
E=lambda i,j:S.eye(4)[:,i]*S.eye(4)[j,:]
e=S.diag(A,B,C,D);eta=S.diag(1,-1,-1,-1)
G=[]
for i in [1,2,3]:G.append(E(0,i)+E(i,0))
for i,j in [(1,2),(1,3),(2,3)]:G.append(E(i,j)-E(j,i))
pivots=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
assert all(x.T*eta+eta*x==S.zeros(4) for x in G)
W=S.Matrix([[(x*e)[a,b] for a,b in pivots] for x in G])
assert W==S.diag(B,C,D,C,D,D)
assert W.det()==B*C**2*D**3
# FULL two-scalar gradients arbitrary; no diagonal stress source assumed.
k0=S.Matrix(S.symbols('u0:4'));k1=S.Matrix(S.symbols('v0:4'))
g=(e.T*eta*e).inv()
q=(k0.T*g*k0)[0]+(k1.T*g*k1)[0]
s=S.symbols('s')
for X in G:
    ep=e+s*(X*e)
    gp=(ep.T*eta*ep).inv()
    dd=S.diff((k0.T*gp*k0+k1.T*gp*k1)[0],s).subs(s,0)
    assert S.simplify(dd)==0
for i,j,target in [
  (0,1,2/(A*B**2)*(k0[0]*k0[1]+k1[0]*k1[1])),
  (1,2,2/(B*C**2)*(k0[1]*k0[2]+k1[1]*k1[2]))]:
    ep=e+s*E(i,j)
    gp=(ep.T*eta*ep).inv()
    dd=S.diff((k0.T*gp*k0+k1.T*gp*k1)[0],s).subs(s,0)
    assert S.factor(dd-target)==0
# After SO6 gauge fixing: ten actual remaining lower-triangular
# coframe coordinates must be locally identical to metric10.
lower=[(a,mu) for a in range(4) for mu in range(a+1)]
metric=[(i,j) for i in range(4) for j in range(i+1)]
deta=[1,-1,-1,-1]
J=S.Matrix([[int(mu==v)*deta[a]*e[a,w]+int(mu==w)*deta[a]*e[a,v]
             for a,mu in lower] for v,w in metric])
det=S.factor(J.det())
assert det==-16*A*B**2*C**3*D**4
r=S.symbols('r',positive=True)
assert S.simplify(W.det().subs({B:1/A,C:r,D:r})-r**5/A)==0
assert S.simplify(det.subs({B:1/A,C:r,D:r})+16*r**7/A)==0
print({'status':'PASS_ORIGINAL_SO_WARD_42_TO_36_METRIC10_LINK24',
 'Lorentz_rank':6,'Ward_coframe_pivots':pivots,
 'exact_Ward_minor':str(W.det()),
 'rank2_Ward_minor':str(W.det().subs({B:1/A,C:r,D:r})),
 'lower_tetrad_to_true_metric10_det':str(det),
 'rank2_metric_det':str(det.subs({B:1/A,C:r,D:r})),
 'arbitrary_two_scalar_gradients_gauge_Ward':True,
 'old_special_Ward_42_to_12_requires_stress_support':True,
 'after_interior_two_species_elimination_geometric_slots':10+24,
 'tomographic_rank34_same_carrier_binding_proved':False,
 'full_geometric_root_proved':False,'GR_closed':False})
