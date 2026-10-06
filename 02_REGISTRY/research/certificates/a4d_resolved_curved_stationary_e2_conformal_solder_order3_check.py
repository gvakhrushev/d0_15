#!/usr/bin/env python3
"""Exact third-order solder obstruction on a conformal critical-solder family.

The support-5 tangent has BOTH free blind moduli q1,q2. Its active scale is
normalized to one. The parameter r labels nondegenerate homogeneous leading
solders obtained from the small leading-link balance, not channel coefficients.
Every r!=0 is obstructed at solder order three, including the rank seam r=1/3.
The separately solved r=0 leading balance with b0!=0 is obstructed too.
This certificate is independent of translations and all channel coefficients:
the selected residual channels have no solder argument. It does not classify
all critical leading solder, the full conformal locus, or finite amplitudes.
"""
from __future__ import annotations
import contextlib,importlib.util,io
from pathlib import Path
import sympy as sp

def check(name,c):
 if not c:raise AssertionError(name)
 print('PASS_'+name,flush=True)
here=Path(__file__).resolve().parent
def load(name,filename):
 s=importlib.util.spec_from_file_location(name,here/filename);m=importlib.util.module_from_spec(s)
 with contextlib.redirect_stdout(io.StringIO()):s.loader.exec_module(m)
 return m
f=load('frozen','a4d_resolved_curved_stationary_e2_support7_joint_linear_gate_check.py')
j=load('jet2','a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py');o=f.owner
q1,q2,r=sp.symbols('q1 q2 r');zero=sp.zeros(4)
v=[-4*o.K1+q2*o.N3,q2*o.N3,q1*o.K1-o.N2,o.N3]
U=[j.cayley_jet(a,h)for a,h in zip(o.generators0,v)];Ui=[j.jet_inv(u)for u in U]
Hs=[sp.zeros(16)for _ in range(3)]
for r0,s0 in o.PAIRS:
 P=j.jet_mul(j.jet_mul(j.jet_mul(U[r0],U[s0]),Ui[r0]),Ui[s0]);Pi=j.jet_inv(P)
 response=[o.G2*o.STAR*o.bivector_of_tangent((p-pi)/2)for p,pi in zip(P,Pi)]
 u,w=[i for i in range(4)if i not in (r0,s0)]
 for k in range(3):
  for a in range(4):
   for b in range(4):
    val=16*o.orientation((r0,s0))*(o.wedge(sp.eye(4)[:,a],sp.eye(4)[:,b]).T*response[k])[0]
    Hs[k][4*a+u,4*b+w]+=val;Hs[k][4*b+w,4*a+u]+=val
H0,H1,H2=[H.applyfunc(sp.expand)for H in Hs];K=sp.Matrix.hstack(*H0.nullspace());L=K.T
check('ORDER_ZERO_HESSIAN_IS_OWNED',H0==f.hessian)
# H_i are exact first generator derivatives of the solder Hessian.
Htest=[]
for _,role,g in o.SELECTED_SPECS:
 H=sp.zeros(16)
 for face,rr in f.curvature_responses(role,g).items():
  u,w=[i for i in range(4)if i not in face]
  for a in range(4):
   for b in range(4):
    val=16*o.orientation(face)*(o.wedge(sp.eye(4)[:,a],sp.eye(4)[:,b]).T*rr)[0]
    H[4*a+u,4*b+w]+=val;H[4*b+w,4*a+u]+=val
 Htest.append(H)

def range_system(T):
 t=sp.Matrix(list(T))
 assert H0*t==sp.zeros(16,1)
 solved=H0.gauss_jordan_solve(-H1*t);Y=solved[0].subs({x:0 for x in solved[1]})
 assert (H0*Y+H1*t).applyfunc(sp.cancel)==sp.zeros(16,1)
 C=sp.Matrix.hstack(L*H1*K,*[L*Hi*t for Hi in Htest]).applyfunc(sp.cancel)
 rhs=(-L*(H1*Y+H2*t)).applyfunc(sp.cancel)
 # Variables are all ten free Y-kernel entries and seven second amplitudes.
 # The next solder coefficient Z has been eliminated by the full H0 cokernel.
 return C,rhs

ss=(r*r-1)/(r*r+1);hh=6*r/(r*r+1);cc=(ss+hh)/2;dd=(ss-hh)/2
ph=sp.Matrix([[1+2*dd,1+2*cc],[1-2*cc,-1+2*dd]]).inv()*sp.Matrix([dd,cc]);ph=ph.applyfunc(sp.cancel)
T=sp.Matrix([[1,0,ph[0],ph[1]],[0,-1,ph[0],ph[1]],[0,0,dd,cc],[0,0,-cc,dd]])
check('CRITICAL_SOLDER_FAMILY_NONDEGENERACY_FORMULA',
 sp.cancel(T.det()+(r**4+34*r*r+1)/(2*(r*r+1)**2))==0)
check('NUMERATOR_HAS_STRICTLY_POSITIVE_REAL_SUM_OF_SQUARES',
 sp.Poly(r**4+34*r*r+1,r).all_coeffs()==[1,0,34,0,1])
C,R=range_system(T);check('ORDER_THREE_ALL_SECOND_CORRECTIONS_PRESENT',C.shape==(10,17))
left=C.subs({q1:0,q2:0}).T.nullspace();check('GENERIC_LEFT_KERNEL_DIMENSION_FIVE',len(left)==5)
obs=[]
for w in left:
 den=sp.lcm([sp.denom(sp.cancel(e))for e in w]);w=(den*w).applyfunc(sp.cancel)
 check('POLYNOMIAL_COKERNEL_IDENTITY', (w.T*C).applyfunc(sp.cancel)==sp.zeros(1,17))
 value=sp.factor((w.T*R)[0]);print('EXACT_COMPATIBILITY',value,flush=True)
 if value:obs.append(value)
check('FIRST_COMPATIBILITY_FORCES_Q2_ZERO',
 sp.factor(obs[0])==1024*q2*r*r/(r*r+1))
# All denominator factors are r or r^2+1; thus clearing them adds no
# real solution with r!=0. No division by 3*r-1 is used here.
for M in (T,C,R):
 for entry in M:
  den=sp.Poly(sp.denom(sp.cancel(entry)),r)
  for p in (sp.Poly(r,r),sp.Poly(r*r+1,r)):
   while den.degree()>0 and den.rem(p).is_zero:den=den.exquo(p)
  assert den.degree()==0
check('DENOMINATORS_ONLY_DECLARED_R_AND_POSITIVE_R_SQUARED_PLUS_ONE',True)
nums=[sp.expand(sp.together(value.subs(q2,0)).as_numer_denom()[0])for value in obs]
F,G=nums[1],nums[3];a,b=sp.diff(F,q1),sp.diff(G,q1)
check('TWO_COMPATIBILITIES_ARE_LINEAR_IN_Q1',sp.diff(F,q1,2)==0 and sp.diff(G,q1,2)==0)
elim=sp.Poly(sp.expand(b*F-a*G),r);P=sp.Poly(nums[2],r)
necessary=sp.gcd(P,elim).monic()
check('EXACT_ELIMINATION_LEAVES_ONLY_R_ONE_THIRD',necessary.as_expr()==r-sp.Rational(1,3))
# Generic cokernel vectors lose independence on that seam; recompute it.
Cs=C.subs(r,sp.Rational(1,3));Rs=R.subs(r,sp.Rational(1,3))
Ns=Cs.subs({q1:0,q2:0}).T.nullspace()
check('R_ONE_THIRD_KERNEL_RECOMPUTED',len(Ns)==5)
Ps=[]
for w in Ns:
 check('SPECIAL_SEAM_COKERNEL_VALID_FOR_ALL_MODULI',(w.T*Cs).applyfunc(sp.cancel)==sp.zeros(1,17))
 Ps.append(sp.factor((w.T*Rs)[0]))
check('SPECIAL_SEAM_FIRST_CONTRADICTION_ROW',Ps[1]==-256*q2/5)
check('SPECIAL_SEAM_SECOND_CONTRADICTION_ROW',sp.expand(Ps[3]+32*(29*q2+644)/45)==0)
check('SPECIAL_SEAM_CONSTANT_BEZOUT_OBSTRUCTION',sp.expand(Ps[3]-sp.Rational(29,72)*Ps[1])==-sp.Rational(20608,45))
# Separate zero-ratio leading balance (its b0 translation need not vanish).
T0=sp.Matrix([[1,0,0,0],[0,-1,0,0],[0,0,-sp.Rational(1,2),-sp.Rational(1,2)],[0,0,sp.Rational(1,2),-sp.Rational(1,2)]])
C0,R0=range_system(T0)
N0=[sp.Matrix(w)for w in (
 (0,0,0,0,0,1,0,0,0,0),
 (0,0,0,1,0,0,0,2,0,0),
 (2,2,0,1,0,0,3,0,-3,3))]
O=[]
for w in N0:
 check('ZERO_RATIO_COKERNEL_VALID_FOR_ALL_MODULI',(w.T*C0).applyfunc(sp.cancel)==sp.zeros(1,17))
 O.append(sp.factor((w.T*R0)[0]))
check('ZERO_RATIO_EXACT_THREE_COMPATIBILITIES',all(sp.expand(a-b)==0 for a,b in zip(O,[32*(2*q1+q2-6),-128*(q2+3),-64*(2*q1-q2*q2-q2-4)])) and len(O)==3)
check('ZERO_RATIO_LINEAR_ROWS_FIX_MODULI',sp.solve(O[:2],(q1,q2))=={q1:sp.Rational(9,2),q2:-3})
check('ZERO_RATIO_THIRD_ROW_NONZERO',O[2].subs({q1:sp.Rational(9,2),q2:-3})==64)
print('EXACT_RESULT: every nonzero real r in the declared conformal leading-solder family, and the separate zero-ratio balance, is blocked at solder order three for both free tangent moduli and every second amplitude/solder correction.',flush=True)
print('SCOPE: these leading-solder families only; arbitrary translations/channel coefficients cannot repair solder, but the full conformal critical-solder locus and finite seven amplitudes remain open.',flush=True)
