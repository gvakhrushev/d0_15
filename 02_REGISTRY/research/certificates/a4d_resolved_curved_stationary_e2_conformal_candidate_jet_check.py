#!/usr/bin/env python3
"""Exact low-order compatible non-eta candidate on support 5.

Full homogeneous link EL2, Fourier affine EL2/EL3, and all solder EL1/2/3
are checked. The leading absolute solder is nondegenerate, curvature is
nonzero, and the eight first residuals are nonzero. This is a truncated
formal compatibility result at a degenerate seed, NOT a finite stationary
witness or a theorem that a formal branch continues. Next link EL3 and
actual affine EL4 remain required.
"""
from __future__ import annotations
import contextlib,importlib.util,io
from pathlib import Path
import sympy as sp

def check(name,c):
 if not c:raise AssertionError(name)
 print('PASS_'+name,flush=True)
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('solder_order3',here/'a4d_resolved_curved_stationary_e2_conformal_solder_order3_check.py');a=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(a)
f=a.f;o=a.o;j=a.j;Z=sp.zeros(4);Z41=sp.zeros(4,1)
T=sp.Matrix([[1,0,-sp.Rational(53,20),-sp.Rational(13,20)],[0,-1,-sp.Rational(53,20),-sp.Rational(13,20)],[-sp.Rational(14,5),-sp.Rational(14,5),-sp.Rational(3,2),sp.Rational(3,2)],[-sp.Rational(7,5),-sp.Rational(7,5),-sp.Rational(3,2),-sp.Rational(3,2)]])
v=[-4*o.K1,Z,-sp.Rational(4,5)*o.K1-o.N2,o.N3]
coefficient=(sp.Rational(-1,1024),0,sp.S.One,-sp.S.One)
b=[sp.eye(4)[:,0]/256,Z41,sp.eye(4)[:,0],sp.eye(4)[:,0]]
parity=(1,1,0,0);signs=(-1,-1,1,1)
check('LEADING_SOLDER_EXACTLY_NONDEGENERATE',T.det()==-sp.Rational(9,2))
check('LEADING_SOLDER_IS_CRITICAL',a.H0*sp.Matrix(list(T))==sp.zeros(16,1))
check('SUPPORT_FIVE_ACTUAL_TANGENT',sp.Matrix(list(v[2]))==sp.Matrix(list(-sp.Rational(4,5)*o.K1-o.N2)))
cache={}
def add(x,y):return [u+w for u,w in zip(x,y)]
def kin(h):
 key=tuple(tuple(m)for m in h)
 if key in cache:return cache[key]
 U=[j.cayley_jet(x,y)for x,y in zip(o.generators0,h)];Ui=[j.jet_inv(u)for u in U];F={}
 for r,s in o.PAIRS:
  P=j.jet_mul(j.jet_mul(j.jet_mul(U[r],U[s]),Ui[r]),Ui[s]);M=j.jet_add(j.constant_jet(sp.eye(4)),j.jet_neg(P))
  F[r,s]=(P,M,j.det_jet(M),j.adj_jet(M))
 cache[key]=(U,F);return cache[key]
def residuals(data,B):
 U,F=data;tr={}
 for r,s in o.PAIRS:
  aa=j.jet_add(j.constant_jet(B[r]),j.jet_mul(U[r],j.constant_jet(signs[r]*B[s])))
  bb=j.jet_add(j.constant_jet(B[s]),j.jet_mul(U[s],j.constant_jet(signs[s]*B[r])))
  tr[r,s]=j.jet_add(aa,j.jet_neg(j.jet_mul(F[r,s][0],bb)))
 out={}
 for ff in o.PAIRS:
  _,M,D,A=F[ff]
  for gg in o.PAIRS:
   if ff==gg:continue
   out[ff,gg]=j.jet_add(j.scalar_jet_mul(D,tr[gg]),j.jet_neg(j.jet_mul(j.jet_mul(F[gg][1],A),tr[ff])))
   assert out[ff,gg][0]==sp.zeros(4,B[0].cols)
 return out
Rv=residuals(kin(v),b);estar=f.link_euler_at(T,f.RESPONSES);link2=[]
for row,(role,g)in enumerate(f.TESTS):
 w=[g if i==role else Z for i in range(4)];Rw=residuals(kin(w),b);Rm=residuals(kin(add(v,w)),b);channel=0
 for fg in Rv:
  ff,gg=fg;cls=0 if len(set(ff)&set(gg))==1 else 1;r1,r2=Rv[fg][1:];mixed=Rm[fg][2]-r2-Rw[fg][2]
  for kind,metric in enumerate((o.ETA,sp.eye(4))):
   channel+=32*coefficient[2*kind+cls]*((r2.T*metric*Rw[fg][1])[0]+(r1.T*metric*mixed)[0])
 link2.append(estar[row]+channel)
check('ALL_24_HOMOGENEOUS_LINK_EL_ORDER_TWO_ZERO',link2==[0]*24)
# Every link row is spatially constant: translations by a site vector
# multiply the entire b field by the character's sign, and the action is
# quadratic in b. Thus these are all sitewise link rows at this order,
# not a restricted subgroup test. The affine Euler output stays in the same
# Fourier mode because homogeneous links make its operator translation invariant.
B=[]
for r in range(4):
 m=sp.zeros(4,16);m[:,4*r:4*r+4]=sp.eye(4);B.append(m)
RB=residuals(kin(v),B);Q2=sp.zeros(16);Q3=sp.zeros(16)
for fg,R in RB.items():
 ff,gg=fg;cls=0 if len(set(ff)&set(gg))==1 else 1;r1,r2=R[1:]
 for kind,metric in enumerate((o.ETA,sp.eye(4))):
  c=coefficient[2*kind+cls];Q2+=16*c*r1.T*metric*r1;Q3+=16*c*(r1.T*metric*r2+r2.T*metric*r1)
check('FULL_MODE_AFFINE_EULER_ORDERS_TWO_THREE_ZERO',Q2==Q3==sp.zeros(16))
active={fg:R[1]for fg,R in Rv.items()if R[1]!=Z41}
check('FIRST_RESIDUAL_NONZERO_ON_EIGHT_PAIRS',len(active)==8 and all(R in (16*sp.Matrix([1,1,0,0]),-16*sp.Matrix([1,1,0,0]))for R in active.values()))
check('BASE_CURVATURE_NONZERO_ON_FOUR_FACES',sum(o.bivector_of_tangent((P-P.inv())/2)!=sp.zeros(6,1)for P in [o.role0[r]*o.role0[s]*o.role0[r].inv()*o.role0[s].inv()for r,s in o.PAIRS])==4)
# Every free second solder coefficient and every second amplitude enters
# the actual third solder range system; no supplied theorem fields.
C,R=a.range_system(T);sub={a.q1:-sp.Rational(4,5),a.q2:0};C=C.subs(sub);R=R.subs(sub)
check('SOLDER_ORDER_THREE_RANK_FIVE_CONSISTENT',C.rank()==C.row_join(R).rank()==5)
sol=C.gauss_jordan_solve(R);part=sol[0].subs({x:0 for x in sol[1]});kernel=sp.Matrix.hstack(*C.nullspace())
check('SOLDER_SECOND_CORRECTION_KERNEL_DIMENSION_TWELVE',kernel.shape==(17,12))
tvec=sp.Matrix(list(T));H1=a.H1.subs(sub);H2=a.H2.subs(sub)
ysol=a.H0.gauss_jordan_solve(-H1*tvec);Y0=ysol[0].subs({x:0 for x in ysol[1]});Y=Y0+a.K*part[:10,:];x2=part[10:,:]
zrhs=-H1*Y-H2*tvec-sum((x*Hi*tvec for x,Hi in zip(x2,a.Htest)),sp.zeros(16,1))
zsol=a.H0.gauss_jordan_solve(zrhs);Zcoef=zsol[0].subs({x:0 for x in zsol[1]})
check('LITERAL_SOLDER_ORDER_TWO_RECONSTRUCTION',a.H0*Y+H1*tvec==sp.zeros(16,1))
check('LITERAL_SOLDER_ORDER_THREE_RECONSTRUCTION',a.H0*Zcoef-zrhs==sp.zeros(16,1))
print('AMPLITUDE_SECOND_PARTICULAR',list(x2),flush=True)
print('FIRST_RESIDUAL_PAIRS',list(active),flush=True)
print('EXACT_CHECKPOINT: link EL2=0, affine EL2=EL3=0, solder EL1=EL2=EL3=0, R1!=0, det T=-9/2, base curvature!=0.',flush=True)
print('OPEN: link EL3, affine EL4, subsequent compatibility, finite reconstruction and hostile L3; this is not a finite vacuum or a completed formal branch.',flush=True)
