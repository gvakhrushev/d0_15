#!/usr/bin/env python3
"""Exact affine-order-four no-go on an independent-translation-ratio family.

Scope: selected homogeneous support 5, A=B=1, conformal lower block
conformal lower block, occupied real Fourier mode 1100, b2=r*e0, b3=e0, b1=0,
b0=z*e0. The leading solder and the two blind tangent moduli follow the declared rational range family. All solder-compatible second corrections
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

K,uf,tf=field('u,t',QQ);zz,oo=K.zero,K.one
fp=here/'a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py'
ft=ast.parse(fp.read_text());funcs=[n for n in ft.body if isinstance(n,ast.FunctionDef)and n.name in ('mc','mz','madd','mscale','mmul','mt','minv','md')]
fns={'K':K,'zero':zz,'one':oo,'permutations':permutations};exec(compile(ast.Module(body=funcs,type_ignores=[]),str(fp),'exec'),fns)
f=types.SimpleNamespace(**{n.name:fns[n.name]for n in funcs})
u,t=s.symbols('u t');v=[f.mc(m)for m in [-4*o.K1+t*o.N3,t*o.N3,u*o.K1-o.N2,o.N3]]
base=[f.mc(x)for x in o.generators0];I=f.mc(s.eye(4));Z=f.mz(4);signs=(-1,-1,1,1);B=[]
for role in range(4):
 b=f.mz(4,16)
 for i in range(4):b[i][4*role+i]=oo
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
 out=[[[zz,zz,zz]for ch in range(4)]for row in range(16)]
 for ff in o.PAIRS:
  for gg in o.PAIRS:
   if ff==gg:continue
   _,M,D,A=F[ff];R=ja(sM(D,T[gg]),jn(jm(jm(F[gg][1],A),T[ff])));cls=0 if len(set(ff)&set(gg))==1 else 1
   assert R[0]==f.mz(4,16)
   for row in range(16):
    for beta,inds in enumerate(((0,),(8,),(12,))):
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


R0=resp([Z]*4);cols=[]
for k,(_,role,g)in enumerate(o.SELECTED_SPECS):
 X=[f.mc(g)if i==role else Z for i in range(4)];Rk=resp(X)
 cols.append([[[a-b for a,b in zip(x,y)]for x,y in zip(rowk,row0)]for rowk,row0 in zip(Rk,R0)])
 print('EXACT_INDEPENDENT_RATIO_SECOND_COLUMN',k,flush=True)
r,p,q,z=s.symbols('r p q z');Gamma=-1/(512*(r*r+1));coef=(Gamma/2+p,Gamma/2-p,q,-q)
def response(row,raw):
 return s.cancel(sum(coef[ch]*(z*raw[ch][0].as_expr()+r*raw[ch][1].as_expr()+raw[ch][2].as_expr())for ch in range(4)))
E=[response(row,R0[row])for row in range(16)]
C=s.Matrix([[response(row,col[row])for col in cols]for row in range(16)])
check('FOUR_NECESSARY_AFFINE_ROWS_INDEPENDENT_OF_EVERY_SECOND_AMPLITUDE',C[[10,11,14,15],:]==s.zeros(4,7))
check('UNIVERSAL_RATIO_AFFINE_ROW_SUM',s.cancel(E[10]+E[15]+128*(r+1)/(r*r+1))==0)
def q3(h):
 R=maps(h);out=[f.mz(3)for _ in range(4)]
 for (ff,gg),V in R.items():
  cls=0 if len(set(ff)&set(gg))==1 else 1
  for kind,metric in enumerate(((1,-1,-1,-1),(1,1,1,1))):
   betas=((0,),(8,),(12,))
   for i in range(3):
    for j in range(3):
     out[2*kind+cls][i][j]+=16*sum((metric[a]*(sum((V[1][a][b]for b in betas[i]),zz)*sum((V[2][a][b]for b in betas[j]),zz)+sum((V[2][a][b]for b in betas[i]),zz)*sum((V[1][a][b]for b in betas[j]),zz))for a in range(4)),zz)
 return out


# Infer the eta sum and lower conformal block from necessary literal leading
# link rows, rather than supplying a preferred coefficient or coframe.
beta=s.Matrix([z,r,1]);aa,bb=s.symbols('aa bb');channels={}
for role,gen in ((2,o.N2),(2,o.N3),(3,o.N2),(3,o.N3),(0,o.N3)):
 w=[f.mc(gen)if i==role else Z for i in range(4)]
 vp=[f.madd(x,y)for x,y in zip(v,w)];vm=[f.madd(x,f.mscale(-oo,y))for x,y in zip(v,w)]
 plus,minus,pure=q3(vp),q3(vm),q3(w)
 deriv=[f.madd(f.mscale(K.from_expr(s.Rational(1,2)),f.madd(x,f.mscale(-oo,y))),f.mscale(-oo,c0))for x,y,c0 in zip(plus,minus,pure)]
 vals=[s.factor((beta.T*s.Matrix([[x.as_expr()for x in row]for row in M])*beta)[0])for M in deriv]
 channel=s.factor(aa*vals[0]+bb*vals[1]+q*(vals[2]-vals[3]));channels[role,str(gen)]=channel
 expected={ (2,str(o.N2)):-98304*r*(aa+bb),(2,str(o.N3)):32768*(aa+bb),(3,str(o.N2)):32768*r*r*(aa+bb),(3,str(o.N3)):-98304*r*(aa+bb),(0,str(o.N3)):-4096*q*z*(r+1)}[role,str(gen)]
 check(f'LITERAL_LEADING_NORMAL_CHANNEL_ROLE_{role}_{len(channels)}',s.cancel(channel-expected)==0)
cc,dd,gamma=s.symbols('cc dd gamma');freephi=s.symbols('p3 p4 p5 p7')
Tgeneral=s.Matrix([[1,0,freephi[0],freephi[1]],[0,-1,freephi[0],freephi[1]],[freephi[2],freephi[2],dd,cc],[freephi[3],freephi[3],-cc,dd]])
Es=ns['f'].link_euler_at(Tgeneral,ns['f'].RESPONSES)
check('NECESSARY_LEADING_ETA_SUM_FIXED',s.expand(Es[17]+Es[22]+32768*gamma*(1+r*r)-64-32768*gamma*(1+r*r))==0)
Mlead,Blead=s.linear_eq_to_matrix([Es[17]+32768*gamma,Es[22]+32768*r*r*gamma,Es[16]-98304*r*gamma],(cc,dd,gamma))
unit=s.cancel(Mlead.det()/(1+r*r));check('NECESSARY_LEADING_GAMMA_AND_CONFORMAL_BLOCK_UNIQUE',unit.is_Rational and unit!=0)
check('CORRECT_LITERAL_CONFORMAL_SUM',s.cancel((Es[17]+32768*Gamma).subs({cc:(r*r-1+6*r)/(2*(1+r*r)),dd:(r*r-1-6*r)/(2*(1+r*r))}))==0)
check('CORRECT_LITERAL_CONFORMAL_DIFFERENCE',s.cancel((Es[16]-98304*r*Gamma).subs({cc:(r*r-1+6*r)/(2*(1+r*r)),dd:(r*r-1-6*r)/(2*(1+r*r))}))==0)
# Residual activation at this mode forces the observer sum to vanish:
# Q2_eta=0, Q2_n_adj=Q2_n_opp is strictly positive on b3=e0.
Rlead=maps(v);N2norm=[s.zeros(3)for _ in range(2)]
for (ff,gg),V in Rlead.items():
 cls=0 if len(set(ff)&set(gg))==1 else 1
 for i,bi in enumerate((0,8,12)):
  for j,bj in enumerate((0,8,12)):
   N2norm[cls][i,j]+=16*sum((V[1][a][bi]*V[1][a][bj]for a in range(4)),zz).as_expr()
check('LEADING_TWO_OBSERVER_NORMS_EQUAL',N2norm[0]==N2norm[1])
pos=s.factor((beta.T*N2norm[0]*beta)[0]/(1+r*r))
check('NONZERO_LEADING_RESIDUAL_FORCES_OBSERVER_SUM_ZERO',pos.is_Rational and pos>0)
print('LEADING_OBSERVER_Q2_POSITIVE_NORM',pos*(1+r*r),flush=True)

# Thus every real stationary member requires r=-1. Observer-zero is
# excluded even there: the other literal row requires r=+1.
check('ZERO_OBSERVER_FOUR_ROWS_IMPOSSIBLE',s.cancel(E[11].subs(q,0)+64*(r-1)/(r*r+1))==0)
check('MINUS_RATIO_FIRST_ROW_FORCES_Z_MINUS_FOUR',s.cancel(E[10].subs(r,-1)+32768*q*(z+4))==0)
check('MINUS_RATIO_SECOND_ROW_FIXES_Q_U',s.cancel(E[11].subs({r:-1,z:-4})-64*(1-512*q*(u-2)))==0)
c=-s.Rational(3,2);d=s.Rational(3,2);p3,p4,p5,p7,dn,ss,tt=s.symbols('p3 p4 p5 p7 dn ss tt');Tg=s.Matrix([[1,0,p3,p4],[0,-1,p3,p4],[p5,p5,d,c],[p7,p7,-c,d]]);Cg,Rg=ns['range_system'](Tg);D=Cg[:,:10];W=s.Matrix.hstack(*D.T.nullspace());CR=(W.T*Cg[:,10:]).applyfunc(s.expand);RR=(W.T*Rg).applyfunc(s.expand);Ka=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,-1],[0,0,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,1]]);assert CR*Ka==s.zeros(8,4);EQ=CR*s.Matrix([0,0,ss,dn,0,tt,0])-RR;sol=s.solve([EQ[6],EQ[7]],(ss,tt));EQ=[s.factor(a.subs(sol))for a in EQ[:6]];phi=s.solve(EQ[2:6],(p3,p4,p5,p7));F=s.factor(EQ[0].subs(phi));star=ns['f'].link_euler_at(Tg,ns['f'].RESPONSES)[5];G=s.factor(star.subs(phi));check('ACTUAL_MINUS_RATIO_SOLDER_ELIMINATION',s.linear_eq_to_matrix(EQ[2:6],(p3,p4,p5,p7))[0].det()!=0 and D.rank()==2 and W.cols==8)
check('ALL_SECOND_AMPLITUDES_QUOTIENT_RETAINED',Ka.row_join(s.Matrix.hstack(s.eye(7)[:,2],s.eye(7)[:,3],s.eye(7)[:,5])).rank()==7);uv=s.solve([F,G],(q1,dn));check('EXCEPTIONAL_T_TWO_ACTUAL_RANGE_OBSTRUCTION',s.factor(F.subs(q2,2))==512)
check('MINUS_RATIO_NECESSARY_FIRST_TANGENT',s.cancel(uv[q1]+(5*q2*q2-90*q2+32)/(6*(q2-2)))==0)


# Recompute the surviving r=-1 solder range without inferring a limiting
# value of a generic rational rank. All second freedoms are present.
ut=-(5*t*t-90*t+32)/(6*(t-2));qt=1/(512*(ut-2))
phi=[(5*t*t-84*t+20)/(24*(t-2)),-(13*t*t-96*t-20)/(24*(t-2)),-(t*t+18*t-8)/(12*(t-2)),(5*t*t-30*t+8)/(6*(t-2))]
T=s.Matrix([[1,0,phi[0],phi[1]],[0,-1,phi[0],phi[1]],[phi[2],phi[2],s.Rational(3,2),-s.Rational(3,2)],[phi[3],phi[3],s.Rational(3,2),s.Rational(3,2)]])
check('MINUS_RATIO_NONDEGENERATE_CRITICAL_SOLDER',s.cancel(T.det())==-s.Rational(9,2)and ns['H0']*s.Matrix(list(T))==s.zeros(16,1))
Cr,rhs=ns['range_system'](T);sub={q1:ut,q2:t};Cr=Cr.subs(sub).applyfunc(s.cancel);rhs=rhs.subs(sub).applyfunc(s.cancel)
rows=[0,3,8,6,9];picked=[0,6,12,13,15];small=Cr.extract(rows,picked)
check('MINUS_RATIO_UNIFORM_ACTUAL_RANK_MINOR',s.cancel(small.det())==536870912)
part=s.zeros(17,1);pv=small.inv()*rhs.extract(rows,[0])
for i,k in enumerate(picked):part[k]=s.cancel(pv[i])
check('LITERAL_FULL_SOLDER_ORDER3_COMPATIBLE',(Cr*part-rhs).applyfunc(s.cancel)==s.zeros(10,1))
N=s.Matrix.hstack(*Cr.nullspace());Ka=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,-1],[0,0,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,1]])
check('ALL_SECOND_AMPLITUDE_FREEDOMS_PRESENT',N.cols==12 and N[10:,:].rank()==4 and N[10:,:].row_join(Ka).rank()==4)
sub={r:-1,z:-4,u:ut,q:qt};Cp=C.subs(sub).applyfunc(s.cancel);Ep=s.Matrix(E).subs(sub).applyfunc(s.cancel)
check('ALL_SOLDER_COMPATIBLE_FREEDOMS_DROP',(Cp*Ka).applyfunc(s.cancel)==s.zeros(16,4))
source=(Ep+Cp*part[10:,:]).applyfunc(s.cancel);den=5*t*t-78*t+8
check('LITERAL_AFFINE_ROW_TWO',s.cancel(source[2]-384*(t-2)*(t+4)/den)==0)
check('LITERAL_AFFINE_ROW_THREE',s.cancel(source[3]+64*(5*t*t-102*t+56)/den)==0)
check('THE_TWO_NECESSARY_NUMERATORS_ARE_COPRIME',s.gcd(s.Poly((t-2)*(t+4),t),s.Poly(5*t*t-102*t+56,t)).degree()==0)
# t=2 is outside the declared rational family. The other denominator is
# a genuine unit: u=2 is already impossible by the exact second row.
# Combined Q2/Q3 vanish in the complete occupied affine mode, so b1 or
# any unoccupied next-translation mode cannot repair these equations.
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
check('ALL_FULL_MODE_LOWER_FORMS_ZERO_FOR_BOTH_TANGENT_MODULI',True)

print('EXACT_SCOPED_VERDICT: entire declared independent-ratio range family excluded at necessary affine order four: r!=-1 has a fixed nonzero row sum; q=0 is inconsistent; r=-1,q!=0 gives two coprime necessary numerator equations.',flush=True)
print('SCOPE: A=B=1, specified common top solder block, conformal ratio family, single occupied mode 1100 and translations along e0. General solders, other translations/modes, and finite support-5 points remain open. No L3.',flush=True)
print('SECONDS',monotonic()-st,flush=True)
