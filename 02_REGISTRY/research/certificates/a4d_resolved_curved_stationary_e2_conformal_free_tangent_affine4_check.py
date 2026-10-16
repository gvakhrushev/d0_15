#!/usr/bin/env python3
"""Exact affine-order-four no-go on a free-tangent conformal germ family.

Scope: selected homogeneous support 5, A=B=1, conformal lower block
(c,d)=(3/2,-3/2), occupied real Fourier mode 1100, b2=b3=e0, b1=0,
b0=z*e0. The leading solder and the two blind tangent moduli follow the
explicit rational formulas below. All solder-compatible second corrections
and all next translations are retained. Both observer-coefficient charts
q!=0 and q=0 are tested. No whole-support or finite stationary terminal.
"""
from __future__ import annotations
import ast,types
from pathlib import Path
from itertools import permutations
from time import monotonic
import sympy as s
from sympy import QQ
from sympy.polys.fields import field
st=monotonic()
def check(name,condition):
 if not condition:raise AssertionError(name)
 print('PASS_'+name,flush=True)
here=Path(__file__).resolve().parent
# Reuse the actual owned generic solder jet/range functions; do not execute
# their unrelated narrow r-family result or substitute stored proof fields.
path=here/'a4d_resolved_curved_stationary_e2_conformal_solder_order3_check.py'
tree=ast.parse(path.read_text());prefix=[]
for node in tree.body:
 if isinstance(node,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ss'for x in node.targets):break
 prefix.append(node)
ns={'__file__':str(path),'__name__':'owned_generic_solder_jet'}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(path),'exec'),ns)
o=ns['o'];q1,q2=ns['q1'],ns['q2'];t=s.Symbol('t')
phi=[-(13*t*t+144*t-212)/(40*(t-2)),(7*t*t-24*t+52)/(40*(t-2)),(t*t-62*t+56)/(10*(t-2)),-(9*t*t+42*t-56)/(20*(t-2))]
T=s.Matrix([[1,0,phi[0],phi[1]],[0,-1,phi[0],phi[1]],[phi[2],phi[2],-s.Rational(3,2),s.Rational(3,2)],[phi[3],phi[3],-s.Rational(3,2),-s.Rational(3,2)]])
q1t=(-9*t*t+58*t+16)/(10*(t-2));dn=(8*t*t+104*t-112)/(5*(t-2))
sub={q1:q1t,q2:t}
vs=[m.subs(sub)for m in ns['v']]
check('NONDEGENERATE_CRITICAL_LEADING_SOLDER',s.cancel(T.det())==-s.Rational(9,2)and ns['H0']*s.Matrix(list(T))==s.zeros(16,1))
C,rhs=ns['range_system'](T);C=C.subs(sub).applyfunc(s.cancel);rhs=rhs.subs(sub).applyfunc(s.cancel)
sol=C.gauss_jordan_solve(rhs);part=sol[0].subs({x:0 for x in sol[1]});N=s.Matrix.hstack(*C.nullspace())
check('ACTUAL_ALL_SECOND_CORRECTIONS_RANGE_COMPATIBLE',(C*part-rhs).applyfunc(s.cancel)==s.zeros(10,1))
check('UNIFORM_RANK_FIVE_MINOR',s.cancel(C.extract([0,3,8,6,9],[0,6,12,13,15]).det())==-268435456)
Ka=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,-1],[0,0,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,1]])
check('ALL_FOUR_AMPLITUDE_FREEDOMS_EXACT',N.cols==12 and N[10:,:].rank()==4 and N[10:,:].row_join(Ka).rank()==4)
for mat in (T,C,rhs,part,N):
 for a in mat:
  den=s.Poly(s.denom(s.cancel(a)),t)
  while den.degree()>0 and den.rem(s.Poly(t-2,t)).is_zero:den=den.exquo(s.Poly(t-2,t))
  assert den.degree()==0
check('RANGE_AND_KERNEL_REGULAR_FOR_EVERY_T_NE_TWO',True)
# The excluded t=2 chart is not inferred by taking a rational limit.
# The reduced actual solder equation is checked at this seam separately
# in the general range reduction; this certificate claims t!=2 only.
K,tf=field('t',QQ);zz,oo=K.zero,K.one
# Reuse the established rational-field matrix operations literally.
fp=here/'a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py'
ft=ast.parse(fp.read_text());funcs=[n for n in ft.body if isinstance(n,ast.FunctionDef)and n.name in ('mc','mz','madd','mscale','mmul','mt','minv','md')]
fns={'K':K,'zero':zz,'one':oo,'permutations':permutations}
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(fp),'exec'),fns)
f=types.SimpleNamespace(**{n.name:fns[n.name]for n in funcs})
v=[f.mc(x)for x in vs];base=[f.mc(x)for x in o.generators0];I=f.mc(s.eye(4));Z=f.mz(4);signs=(-1,-1,1,1);B=[]
for r in range(4):
 b=f.mz(4,16)
 for i in range(4):b[i][4*r+i]=oo
 B.append(b)
def ja(a,b):return [f.madd(x,y)for x,y in zip(a,b)]
def jn(a):return [f.mscale(-oo,x)for x in a]
def jm(a,b):
 out=[]
 for k in range(4):
  m=f.mz(len(a[0]),len(b[0][0]))
  for i in range(k+1):m=f.madd(m,f.mmul(a[i],b[k-i]))
  out.append(m)
 return out
def ji(a):
 out=[f.minv(a[0])]
 for k in range(1,4):
  m=f.mz(len(a[0]))
  for i in range(1,k+1):m=f.madd(m,f.mmul(a[i],out[k-i]))
  out.append(f.mscale(-oo,f.mmul(out[0],m)))
 return out
def jc(m):return [m,f.mz(len(m),len(m[0])),f.mz(len(m),len(m[0])),f.mz(len(m),len(m[0]))]
def sm(a,b):return [sum((a[i]*b[k-i]for i in range(k+1)),zz)for k in range(4)]
def jd(a):
 out=[zz]*4;n=len(a[0])
 for p in permutations(range(n)):
  z=[oo,zz,zz,zz]
  for i,c in enumerate(p):z=sm(z,[a[k][i][c]for k in range(4)])
  sign=-1 if sum(p[i]>p[j]for i in range(n)for j in range(i+1,n))%2 else 1
  out=[x+sign*y for x,y in zip(out,z)]
 return out
def jad(a):
 out=[f.mz(4)for _ in range(4)]
 for i in range(4):
  for j in range(4):
   val=jd([[[M[r][c]for c in range(4)if c!=i]for r in range(4)if r!=j]for M in a])
   for k in range(4):out[k][i][j]=(-1)**(i+j)*val[k]
 return out
def sM(a,b):
 return [f.madd(f.mz(len(b[0]),len(b[0][0])),sum_m([f.mscale(a[i],b[k-i])for i in range(k+1)]))for k in range(4)]
def sum_m(ms):
 m=f.mz(len(ms[0]),len(ms[0][0]))
 for x in ms:m=f.madd(m,x)
 return m
def resp(X):
 half=K.from_expr(s.Rational(1,2));U=[jm([f.madd(I,f.mscale(half,a)),f.mscale(half,h),f.mscale(half,x),Z],ji([f.madd(I,f.mscale(-half,a)),f.mscale(-half,h),f.mscale(-half,x),Z]))for a,h,x in zip(base,v,X)];Ui=[ji(x)for x in U];F={};T={}
 for r,ss in o.PAIRS:
  P=jm(jm(jm(U[r],U[ss]),Ui[r]),Ui[ss]);M=ja(jc(I),jn(P));F[r,ss]=(P,M,jd(M),jad(M))
  aa=ja(jc(B[r]),jm(U[r],jc(f.mscale(K.from_expr(signs[r]),B[ss]))));bb=ja(jc(B[ss]),jm(U[ss],jc(f.mscale(K.from_expr(signs[ss]),B[r]))))
  T[r,ss]=ja(aa,jn(jm(P,bb)))
 out=[[[zz,zz]for ch in range(4)]for row in range(16)]
 for ff in o.PAIRS:
  for gg in o.PAIRS:
   if ff==gg:continue
   _,M,D,A=F[ff];R=ja(sM(D,T[gg]),jn(jm(jm(F[gg][1],A),T[ff])));cls=0 if len(set(ff)&set(gg))==1 else 1
   assert R[0]==f.mz(4,16)
   for row in range(16):
    for beta,inds in enumerate(((0,),(8,12))):
     for kind,metric in enumerate(((1,-1,-1,-1),(1,1,1,1))):
      out[row][2*kind+cls][beta]+=32*sum((metric[a]*R[i][a][row]*sum((R[4-i][a][b]for b in inds),zz)for i in (1,2,3)for a in range(4)),zz)
 return out
def maps(h):
 X=[Z]*4
 half=K.from_expr(s.Rational(1,2));U=[jm([f.madd(I,f.mscale(half,a)),f.mscale(half,h),f.mscale(half,x),Z],ji([f.madd(I,f.mscale(-half,a)),f.mscale(-half,h),f.mscale(-half,x),Z]))for a,h,x in zip(base,h,X)];Ui=[ji(x)for x in U];F={};T={}
 for r,ss in o.PAIRS:
  P=jm(jm(jm(U[r],U[ss]),Ui[r]),Ui[ss]);M=ja(jc(I),jn(P));F[r,ss]=(P,M,jd(M),jad(M))
  aa=ja(jc(B[r]),jm(U[r],jc(f.mscale(K.from_expr(signs[r]),B[ss]))));bb=ja(jc(B[ss]),jm(U[ss],jc(f.mscale(K.from_expr(signs[ss]),B[r]))))
  T[r,ss]=ja(aa,jn(jm(P,bb)))
 Rall={}
 for ff in o.PAIRS:
  for gg in o.PAIRS:
   if ff==gg:continue
   _,M,D,A=F[ff];Rall[ff,gg]=ja(sM(D,T[gg]),jn(jm(jm(F[gg][1],A),T[ff])))
 return Rall

def q3(h):
 R=maps(h);out=[f.mz(2)for _ in range(4)]
 for (ff,gg),V in R.items():
  cls=0 if len(set(ff)&set(gg))==1 else 1
  for kind,metric in enumerate(((1,-1,-1,-1),(1,1,1,1))):
   betas=((0,),(8,12))
   for i in range(2):
    for j in range(2):
     out[2*kind+cls][i][j]+=16*sum((metric[a]*(sum((V[1][a][b]for b in betas[i]),zz)*sum((V[2][a][b]for b in betas[j]),zz)+sum((V[2][a][b]for b in betas[i]),zz)*sum((V[1][a][b]for b in betas[j]),zz))for a in range(4)),zz)
 return out
b0=K.from_expr(-(t*t-42*t+16)/(2048*(t-2)));gam=K.from_expr(-s.Rational(1,2048))
def tensor(R):
 out=[]
 for row in R:
  ea,eo,na,no=row
  out.append([gam*b0*(ea[0]+eo[0]),b0*(ea[0]-eo[0]),gam*(ea[1]+eo[1])+b0*(na[0]-no[0]),ea[1]-eo[1],na[1]-no[1]])
 return out
T0=tensor(resp([Z]*4));cols=[]
print('BASE_AFFINE4_TENSOR','SECONDS',monotonic()-st,flush=True)
for k,(_,role,g)in enumerate(o.SELECTED_SPECS):
 X=[f.mc(g)if r==role else Z for r in range(4)];Tk=tensor(resp(X));cols.append([[a-b for a,b in zip(x,y)]for x,y in zip(Tk,T0)])
 print('GENERAL_MODULUS_SECOND_AMPLITUDE',k,'SECONDS',monotonic()-st,flush=True)
Ka=[[K.from_expr(a)for a in row]for row in Ka.tolist()];part=[K.from_expr(a)for a in part[10:,:]]
Freedoms=[[[sum((cols[k][row][mon]*Ka[k][col]for k in range(7)),zz)for col in range(4)]for mon in range(5)]for row in range(16)]
print('ALL_SECOND_FREEDOMS_DROP',all(x==zz for row in Freedoms for mon in row for x in mon),flush=True)
source=[[T0[row][mon]+sum((cols[k][row][mon]*part[k]for k in range(7)),zz)for mon in range(5)]for row in range(16)]
p,q=s.symbols('p q');mons=(1,p,q,p*q,q*q);expr=[s.factor(sum(a.as_expr()*m for a,m in zip(row,mons)))for row in source]
for i,e in enumerate(expr):print('GENERAL_MODULUS_AFFINE4_ROW',i,e,flush=True)

check('EVERY_SOLDER_COMPATIBLE_SECOND_AMPLITUDE_DROPS',all(x==zz for row in Freedoms for mon in row for x in mon))
rowpair=[source[10][i]+source[15][i]for i in range(5)]
check('EXACT_AFFINE4_PAIR_IS_MINUS128_Q',rowpair==[zz,zz,K.from_expr(-128),zz,zz])
check('Q_NONZERO_CHART_IMPOSSIBLE',s.cancel(expr[10]+expr[15]+128*q)==0)
# Next b in this mode acts through the identically zero combined Q3.
# Other modes cannot cancel this Fourier component of the affine operator.
# Verify the Q2/Q3 combination directly below, including arbitrary b0.
R=maps(v);Q2=[f.mz(16)for _ in range(4)];Q3=[f.mz(16)for _ in range(4)]
for (ff,gg),V in R.items():
 cls=0 if len(set(ff)&set(gg))==1 else 1
 for kind,metric in enumerate(((1,-1,-1,-1),(1,1,1,1))):
  ch=2*kind+cls
  for i in range(16):
   for j in range(16):
    Q2[ch][i][j]+=16*sum((metric[a]*V[1][a][i]*V[1][a][j]for a in range(4)),zz)
    Q3[ch][i][j]+=16*sum((metric[a]*(V[1][a][i]*V[2][a][j]+V[2][a][i]*V[1][a][j])for a in range(4)),zz)
for order,M in ((2,Q2),(3,Q3)):
 print('Q',order,'eta',[X==f.mz(16)for X in M[:2]],'nDiff',M[2]==M[3],flush=True)
 assert M[0]==M[1]==f.mz(16) and M[2]==M[3]
check('ALL_FULL_MODE_Q2_Q3_ZERO_FOR_THE_FOUR_COEFFICIENT_FAMILY',True)
w=[f.mc(o.N3),Z,Z,Z]
vp=[f.madd(a,b)for a,b in zip(v,w)];vm=[f.madd(a,f.mscale(-oo,b))for a,b in zip(v,w)]
plus,minus,pure=q3(vp),q3(vm),q3(w)
D=[f.madd(f.mscale(K.from_expr(s.Rational(1,2)),f.madd(a,f.mscale(-oo,b))),f.mscale(-oo,c))for a,b,c in zip(plus,minus,pure)]
check('ETA_LEADING_N3_ZERO_FOR_ARBITRARY_B0',D[0]==D[1]==f.mz(2))
check('OBSERVER_LEADING_N3_RESPONSE',f.madd(D[2],f.mscale(-oo,D[3]))==f.mc(s.Matrix([[0,-4096],[-4096,0]])))
# Literal star N3 response at the frozen link, for this leading solder.
star=0
for face,res in ns['f'].curvature_responses(0,o.N3).items():
 u,w0=[i for i in range(4)if i not in face]
 star+=16*o.orientation(face)*(o.wedge(T[:,u],T[:,w0]).T*res)[0]
check('LITERAL_STAR_N3_SOURCE',s.cancel(star+4*(t*t-42*t+16)/(t-2))==0)
P=s.Poly(t*t-42*t+16,t)
check('ZERO_OBSERVER_SEAM_REQUIRES_P_ZERO',s.rem(s.together(star).as_numer_denom()[0],P.as_expr(),t)==0 and s.gcd(P,s.Poly(t-2,t)).degree()==0)
# In the q=0 chart, b0 is arbitrary. The field identities rowpair[0,1]=0
# force both eta beta0 contributions to vanish identically since b0 is
# a nonzero rational function. At P=0 the n beta0 term in rowpair[2]
# vanishes. The actual eta-only EL4 pair is therefore -128. This uses
# regular specialization, rather than division by a zero observer q.
for row in (source,):
 for arow in row:
  for a in arow:
   assert s.gcd(s.Poly(a.denom.as_expr(),t),P).degree()==0
check('ZERO_OBSERVER_SEAM_ACTUAL_AFFINE4_PAIR_MINUS128',rowpair[0]==rowpair[1]==zz and rowpair[2]==K.from_expr(-128))
print('EXACT_VERDICT: declared free-tangent family has no full stationary germ at necessary affine order four, for both observer charts. All second corrections and next translations retained.',flush=True)
print('SCOPE: this homogeneous leading-solder/translation family; broader conformal moduli, other Fourier translations, and finite seven-amplitude points remain open. No L3.',flush=True)
print('SECONDS',monotonic()-st,flush=True)
