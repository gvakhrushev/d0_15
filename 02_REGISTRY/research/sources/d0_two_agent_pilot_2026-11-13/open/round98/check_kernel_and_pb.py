#!/usr/bin/env python3
"""Exact symbolic all-skew kernel identity and Pb-before-post orientation."""
from pathlib import Path
import json,sympy as s
P=Path(__file__).resolve().parent;R=s.Rational;I=s.eye
# Three CODE labels, two WORK dimensions, all three independent skew entries.
u=[s.Matrix([1,0]),s.Matrix([R(3,5),R(4,5)]),s.Matrix([R(5,13),R(12,13)])]
S=s.Matrix([[R(3,5),R(4,5)],[R(4,5),-R(3,5)]]);assert S.T==S and S*S==I(2)
def controlled_vectors(v):
 M=s.zeros(6,3)
 for b in range(3):M[2*b:2*b+2,b]=v[b]
 return M
V=controlled_vectors(u);J=controlled_vectors([u[0]]*3);Delta=V-J
assert V.T*V==I(3) and J.T*J==I(3)
a,b,c=s.symbols('a b c',real=True);Y=s.Matrix([[0,-a,-b],[a,0,-c],[b,c,0]])
phi=lambda W:V.T*s.kronecker_product(W,S)*V
D=phi(I(3));A=Delta.T*s.kronecker_product(I(3),S)*Delta
lhs=phi(Y)-(D*Y+Y*D)/2
rhs=Delta.T*s.kronecker_product(Y,S)*Delta-(A*Y+Y*A)/2
assert s.simplify(lhs-rhs)==s.zeros(3) and s.simplify(lhs.T+lhs)==s.zeros(3)
# Nonsymmetric actual kernel from distinct left/source states, not B^T.
small=s.Matrix([[R(9999,10001),-R(200,10001)],[R(200,10001),R(9999,10001)]])
W=controlled_vectors([small*u[0],u[1],u[2]])
actual=lambda X:W.T*s.kronecker_product(X,S)*V
M=actual(I(3));K=actual(Y);assert M==s.diag(*list(M.diagonal())) and s.simplify(K.T+K)!=s.zeros(3)
# Exact analytic q vs 1/2 Pf identity including symmetric actual residue.
chi=s.Matrix([R(1,3),R(2,3),R(2,3)]);assert (chi.T*chi)[0]==1
Es=(K-K.T)/2-(M*Y+Y*M)/2;As=(K+K.T)/2
q=-(chi.T*M*K*chi)[0]/2;pf=-(chi.T*M*M*Y*chi)[0]/2
assert s.simplify(q-pf/2+(chi.T*M*(Es+As)*chi)[0]/2)==0
mu=s.symbols('mu',real=True);assert s.simplify((chi.T*Es*chi)[0])==0
assert s.simplify((chi.T*M*Es*chi)[0]-(chi.T*(M-mu*I(3))*Es*chi)[0])==0
# Pb BEFORE fixed post U* mapping xi to chi: zero at exact target. Use
# irrational but symbolic exact r; a different arbitrary post is a negative.
chi2=s.Matrix([R(3,5),R(4,5)]);M2=s.diag(1,R(119,169));r=s.sqrt((chi2.T*M2*M2*chi2)[0]);xi=M2*chi2/r
rot=lambda v:s.Matrix([[v[0],-v[1]],[v[1],v[0]]]);U=rot(chi2)*rot(xi).T;J2=s.Matrix([[0,-1],[1,0]])
assert s.simplify(U*xi-chi2)==s.zeros(2,1)
pb=s.simplify(-(chi2.T*U*J2*M2*chi2)[0]);assert pb==0
wrong=s.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
assert (chi2.T*wrong*J2*M2*chi2)[0]!=0
# A non-identical CODE probe AFTER U is a different body generator; do not
# identify the two tangent coordinates just because both target zero at U*.
pre=U*J2;after=J2*U;assert s.simplify(pre-after)==s.zeros(2) # 2D SO(2) commutes
# A third-dimensional CODE rotation makes the distinction observable.
U3=s.Matrix([[R(3,5),-R(4,5),0],[R(4,5),R(3,5),0],[0,0,1]])
X3=s.Matrix([[0,0,-1],[0,0,0],[1,0,0]]);assert U3*X3!=X3*U3
out={'status':'PASS_SYMBOLIC_DIMENSION_FREE_KERNEL_AND_PB_SLOT','ideal_reflected_kernel_identity_all_3_skew_generators':True,'actual_nonsymmetric_kernel_decomposition':True,'skew_residual_scalar_centering':True,'Pb_before_fixed_post_exact_target_derivative_zero':True,'arbitrary_post_negative_control':True,'post_probe_and_Pb_body_directions_distinct_in_3D':True,'full_production_kernel_evaluated':False,'GR_closed':False}
(P/'KERNEL_AND_PB_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
