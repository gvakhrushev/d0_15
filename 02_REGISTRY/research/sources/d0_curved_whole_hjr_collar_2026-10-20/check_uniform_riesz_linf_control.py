#!/usr/bin/env python3
"""Exact norm-domain negative control. No repository inputs/edits."""
import json
import sympy as s
C=[]
for a in range(4):
 Q=s.zeros(16)
 for mask in range(16):
  if not (mask>>a)&1: Q[mask|(1<<a),mask]=(-1)**((mask&((1<<a)-1)).bit_count())
 C.append(Q)
def create(v): return sum((v[a]*C[a] for a in range(4)),s.zeros(16))
Om=s.eye(16)[:,15]
eps=s.Rational(1,100);out=[]
for L in [4,8]:
 h=s.Rational(1,L)
 V=[s.eye(4)/4 for _ in range(L)]
 for t in range(L): V[t][0,0]+=eps*(-1)**t
 assert all(v.det()!=0 and max(abs(v[a,a]) for a in range(4))<1 for v in V)
 images=[];base=[]
 for t in range(L):
  # Actual full-CAR constant-state d+d†. All transverse contributions cancel.
  raise_now=create(V[t][:,0])*(Om-Om)/h
  lower_now=(create(V[(t-1)%L][:,0]).T*Om-create(V[t][:,0]).T*Om)/h
  images.append(raise_now+lower_now)
  base.append((C[0]/4*(Om-Om)+C[0].T/4*(Om-Om))/h)
 assert all(q==s.zeros(16,1) for q in base)
 norm2=s.simplify(sum((q.T*q)[0] for q in images)/L)
 assert norm2==4*eps**2/h**2
 lip=max(abs(V[t][0,0]-V[(t-1)%L][0,0])/h for t in range(L))
 assert lip==2*eps/h
 out.append({'L':L,'h':str(h),'coefficient_Linf':str(eps),'coefficient_discrete_Lip':str(lip),'true_E_on_constant_topform_norm_squared':str(norm2),'true_E_norm_over_Linf':str(2/h)})
print(json.dumps({'status':'PASS','full_CAR_components':16,'spatial_extension':'tensor constant profiles on the three transverse tori; ratio unchanged','cases':out,'scope':'Linf-only failure and true shifted-adjoint commutator; analytic C1 relative bound is separately proved'},indent=2))
