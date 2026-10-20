#!/usr/bin/env python3
"""Independent exact S3 fixed-space and collar curvature review; no repo edits."""
import itertools,json
import sympy as s
I=s.eye(4);eta=s.diag(1,-1,-1,-1)
def E(i,j):
 A=s.zeros(4);A[i,j]=1;return A
B=[E(0,i)+E(i,0) for i in range(1,4)]
R=[E(i,j)-E(j,i) for i in range(1,4) for j in range(i+1,4)]
lie=B+R
perms=list(itertools.permutations([1,2,3]))
Ps=[]
for pm in perms:
 p=[0]+list(pm);P=s.zeros(4)
 for j in range(4): P[p[j],j]=1
 assert P.T*eta*P==eta
 Ps.append((p,P))
C=[E(0,0),sum((E(0,i)-E(i,0) for i in range(1,4)),s.zeros(4)),sum((E(i,i) for i in range(1,4)),s.zeros(4)),sum((E(i,j) for i in range(1,4) for j in range(1,4) if i!=j),s.zeros(4)),sum(B,s.zeros(4))]
assert all(P*A*P.T==A for _,P in Ps for A in C)
mc=[E(i,j) for i in range(4) for j in range(4)]
cm=s.Matrix.vstack(*[s.Matrix.hstack(*[s.Matrix(P*A*P.T-A).reshape(16,1) for A in mc]) for _,P in Ps])
assert len(cm.nullspace())==5 and s.Matrix.hstack(*[s.Matrix(A).reshape(16,1) for A in C]).rank()==5
lb=[]
for role in range(4):
 for X in lie:
  row=[s.zeros(4) for _ in range(4)];row[role]=X;lb.append(row)
rows=[]
for p,P in Ps:
 cols=[]
 for l in lb:
  v=s.Matrix.vstack(*[s.Matrix(P*l[r]*P.T-l[p[r]]).reshape(16,1) for r in range(4)])
  cols.append(v)
 rows.append(s.Matrix.hstack(*cols))
lm=s.Matrix.vstack(*rows)
assert len(lm.nullspace())==4
fixed=[]
x=[s.zeros(4) for _ in range(4)];x[0]=sum(B,s.zeros(4));fixed.append(x)
x=[s.zeros(4)]+B;fixed.append(x)
x=[s.zeros(4)]+[sum((B[j-1] for j in range(1,4) if j!=i),s.zeros(4)) for i in range(1,4)];fixed.append(x)
x=[s.zeros(4)]+[sum((E(i,j)-E(j,i) for j in range(1,4) if j!=i),s.zeros(4)) for i in range(1,4)];fixed.append(x)
assert all(P*l[r]*P.T==l[p[r]] for p,P in Ps for l in fixed for r in range(4))
assert s.Matrix.hstack(*[s.Matrix.vstack(*[s.Matrix(a).reshape(16,1) for a in l]) for l in fixed]).rank()==4
im=s.Matrix.vstack(*[s.Matrix.hstack(*[s.Matrix(P*A*P.T-A).reshape(16,1) for A in lie]) for _,P in Ps])
assert len(im.nullspace())==1
# Exact noncommuting finite proper-link curvature control.
U0=I.copy();U0[0,0]=U0[1,1]=s.Rational(5,4);U0[0,1]=U0[1,0]=s.Rational(3,4)
Ui=I.copy();Ui[0,0]=Ui[2,2]=s.Rational(13,12);Ui[0,2]=Ui[2,0]=s.Rational(5,12)
assert U0.T*eta*U0==eta and Ui.T*eta*Ui==eta and U0*Ui!=Ui*U0
P=U0*I*U0.inv()*Ui.inv()
assert P==Ui.inv() and P!=I
print(json.dumps({'status':'PASS','full_spatial_S3_elements':len(Ps),'invariant_interior_coframe_dimension':5,'invariant_outgoing_proper_link_family_dimension':4,'invariant_incoming_u_link_dimension':1,'total_restricted_unknowns':10,'spatial_translations_and_fixed_t1_Ui_imply':'P_0i(t0)=Ui(t0)^-1 exactly','noncommuting_finite_proper_link_control':True,'scope':'symmetry and graph-domain reduction only; nonsingular Riesz-reduced Hessian is separate'},indent=2))
