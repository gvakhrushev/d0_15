#!/usr/bin/env python3
"""Arbitrary-precision evaluation of individual entries of original targets.
No float tables are used for the physical constants or field formulas.
Run in mp.workdps(precision); operations form computable precision names,
not interval certificates of a native compiler.
"""
from fractions import Fraction
from itertools import permutations
import mpmath as m
import targets as t

def constants():
 p=(m.sqrt(5)-1)/2;z=m.mpf(1)/2**20;L=4*p**3;Q=1-z*L;R=1-z*L*(1+p**6)
 k=2*p**(-5)*(R/Q+p**6); f=Fraction(t.META['F_h_rational']);F=m.mpf(f.numerator)/f.denominator
 return p,k,F

def mat(a):return m.matrix([[m.mpf(str(z)) for z in row] for row in a])
def eta():return m.matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
def transpose(a):return a.T

def at_site(bank,site,label=None):
 x=tuple(site);bits=t.canonical_label(label);p,k,F=constants();h=m.mpf(1)/4;nu=m.mpf(3)/5;Id=m.eye(4);E=eta()
 rho=m.mpf(256*int(t.COUNT[t.INDEX[x]]))/10946;z=m.mpf(1)/2**20
 xx=m.mpf(x[2])/4;yy=m.mpf(x[3])/4
 def hh(a,b):return k*(2*m.pi)**2*(m.mpf(1)/100)**2*(a*a+b*b)+m.mpf(3)/100*(a*a-b*b)
 H=hh(xx,yy);kx=(H-hh(xx-h,yy))/2;ky=(H-hh(xx,yy-h))/2
 u=m.matrix([[0,nu,0,0],[nu,-nu*H/2,0,0],[0,0,nu,0],[0,0,0,nu]])
 N2=m.matrix(4);N2[1,2]=N2[2,0]=1;N3=m.matrix(4);N3[1,3]=N3[3,0]=1
 Z=-kx*N2-ky*N3;links=[Id+Z+Z*Z/2,Id.copy(),Id.copy(),Id.copy()]
 amp=m.pi/(200*m.sqrt(2));psi=[amp*m.cos(m.pi*x[0]/2),amp*m.sin(m.pi*x[0]/2)]
 if bits is not None:
  generators=[m.matrix(4) for _ in range(4)]
  for coord,bit in zip(t.COORD,bits):
   if tuple(coord['site'])!=x:continue
   d=m.mpf(1)/2**30*(int(bit)-p*p)
   if coord['kind']=='coframe':u[coord['component'],coord['role']]+=d
   elif coord['kind']=='matter':psi[0 if coord['grade']==0 else 1]+=d
   else:
    i,j=coord['generator'];skew=m.matrix(4);skew[i,j]=1;skew[j,i]=-1;generators[coord['role']]+=d*E*skew
  links=[m.expm(generators[r])*links[r] for r in range(4)]
 if bank in ('f','q','current_mark'):
  return u,links if bank!='q' else [Id.copy() for _ in range(4)],psi if bank!='f' else [m.mpf(0),m.mpf(0)]
 T=m.matrix([[1,1,0,0],[1,-1,0,0],[0,0,m.sqrt(2),0],[0,0,0,-m.sqrt(2)]])/m.sqrt(2);C=m.diag([1,-1,-1,-1]);u=nu*m.sqrt(rho)/6*T*C;links=[Id.copy() for _ in range(4)];psi=[m.mpf(0),m.mpf(0)]
 if bank in ('y+','y-'):
  d=F/(36*k);a=h*6*m.sqrt(d)/2;psi[0]=a*(-1)**x[1 if bank=='y+' else 0]
 if bank in ('x+','x-'):
  ta=h/2;tb=h/20;ca=(1+ta*ta)/(1-ta*ta);sa=2*ta/(1-ta*ta);cb=(1-tb*tb)/(1+tb*tb);sb=2*tb/(1+tb*tb)
  ac=m.eye(4);ac[0,0]=ac[2,2]=ca;ac[0,2]=ac[2,0]=sa
  bc=m.eye(4);bc[1,1]=bc[2,2]=cb;bc[1,2]=sb;bc[2,1]=-sb
  links[0]=T*ac*T.T;links[1]=T*(bc if bank=='x+' else bc.T)*T.T
 assert bank in t.BANKS
 return u,links,psi

def exterior(U):
 rows=[[i for i in t.ORDER if (mask>>i)&1] for mask in range(16)];out=m.matrix(16)
 for i,a in enumerate(rows):
  for j,b in enumerate(rows):
   if len(a)==len(b):out[i,j]=m.det(m.matrix([[U[q,r] for r in b] for q in a])) if a else 1
 return out

def J_at(bank,site,kind,role,label=None):
 u,links,_=at_site(bank,site,label);I=m.eye(16)
 if kind=='inverse_coframe_column':
  C=sum((u[i,role]*mat(t.CREATORS[i]) for i in range(4)),m.matrix(16))
  norm2=sum(u[i,role]**2 for i in range(4));assert norm2<1
  a=1/(1+m.sqrt(1-norm2));left=I-a*C*C.T;right=I-a*C.T*C
 else:
  assert kind=='proper_link';C=exterior(links[role])/2
  left=m.sqrtm(I-C*C.T);right=m.sqrtm(I-C.T*C)
 out=m.matrix(32)
 for i in range(16):
  for j in range(16):out[i,j]=C[i,j];out[i,j+16]=left[i,j];out[i+16,j]=right[i,j];out[i+16,j+16]=-C[j,i]
 return out

def omega(bank,a,i,j,label=None):
 assert 0<=a<4096 and 0<=i<32 and 0<=j<32
 if a>=2049:return m.mpf(0)
 if a==0:return (1 if i==j else 0)/m.sqrt(32*2049)
 row=t.ADDR[a];return J_at(bank,tuple(row['site']),row['kind'],row['direction'],label)[j,i]/m.sqrt(32*2049)

def O_entry(bank,out,in_,label=None):
 r=(0,0,0);c=1/m.sqrt(32*2049);x=omega(bank,*out,label);y=omega(bank,*in_,label);dx=int(out==r);dy=int(in_==r)
 return int(out==in_)+x*dy-dx*y+(x*(c*dy-y)-dx*(dy-c*y))/(1+c)

def material(bank,site,label=None):
 p,_,_=constants();_,_,psi=at_site(bank,site,label);v=m.matrix(16,1);v[1]=m.sqrt(p);v[0]=psi[0];v[15]=psi[1];v[14]=m.sqrt(1-p-psi[0]**2-psi[1]**2);return v

def R(v,anchor=1):
 e=m.matrix(len(v),1);e[anchor]=1;k=v*e.T-e*v.T
 return m.eye(len(v))+k+k*k/(1+v[anchor])

def car_entry(bank,site,out,in_,label=None):
 p,_,_=constants();star=m.matrix(16,1);star[1]=m.sqrt(p);star[14]=p
 return (R(material(bank,site,label))*R(star).T)[out,in_]

def site_entry(out,in_):
 """All-column entry of O_chi (G^tensor8)^T for the true born-site input."""
 assert 0<=out<256 and 0<=in_<256
 p,_,_=constants();a=m.sqrt(p);G=((a,-p),(p,a));c=m.sqrt(m.mpf(int(t.COUNT[0]))/10946)
 def chi(x):return m.sqrt(m.mpf(int(t.COUNT[x]))/10946)
 def gram(brow,bcol):
  val=m.mpf(1)
  for shift in range(8):val*=G[(brow>>shift)&1][(bcol>>shift)&1]
  return val
 x=chi(out);dx=int(out==0);total=m.mpf(0)
 for z in range(256):
  y=chi(z);dz=int(z==0)
  O=int(out==z)+x*dz-dx*y+(x*(c*dz-y)-dx*(dz-c*y))/(1+c)
  total+=O*gram(in_,z)
 return total

def choi_column(bank,in_,label=None,nonzero_only=True):
 """Stream the complete 2^22-column of O_b; padded identity is included.
 No unknown source state is copied. Exact-zero decisions are numeric in mpmath;
 use nonzero_only=False if an explicit value for every output is required.
 """
 a0,i0,j0=in_;assert 0<=a0<4096 and 0<=i0<32 and 0<=j0<32
 anchor=(0,0,0);c=1/m.sqrt(32*2049);by=omega(bank,*in_,label);dy=int(in_==anchor)
 for a in range(4096):
  if a>=2049:
   if a==a0:
    for i in range(32):
     for j in range(32):
      value=int((a,i,j)==in_)
      if value or not nonzero_only:yield (a,i,j,value)
   elif not nonzero_only:
    for i in range(32):
     for j in range(32):yield (a,i,j,m.mpf(0))
   continue
  row=t.ADDR[a];J=m.eye(32) if a==0 else J_at(bank,tuple(row['site']),row['kind'],row['direction'],label)
  for i in range(32):
   for j in range(32):
    x=(a,i,j);bx=J[j,i]*c;dx=int(x==anchor)
    value=int(x==in_)+bx*dy-dx*by+(bx*(c*dy-by)-dx*(dy-c*by))/(1+c)
    if value or not nonzero_only:yield (a,i,j,value)

def car_column(bank,site,in_grade,right,label=None):
 """Stream all 16 output grades; same site and fresh RIGHT index exactly."""
 assert 0<=in_grade<16 and 0<=right<128
 p,_,_=constants();star=m.matrix(16,1);star[1]=m.sqrt(p);star[14]=p
 M=R(material(bank,site,label))*R(star).T
 for out in range(16):yield (tuple(site),out,right,M[out,in_grade])
