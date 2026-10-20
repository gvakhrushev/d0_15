#!/usr/bin/env python3
"""Exact original full128 Golden/Jones/Kraus mixed source and four-arm gate.

Native CAR16 creation algebra in role order (0,2,3,1); original Walsh
32 words, Julia square-root first and mixed Sylvester derivatives, true
two-round Born probabilities. Original native p, four equal p^6 controller
strings, real normalized Jones half factor. No physical Book selection.
"""
import itertools
import numpy as np

ORDER=(0,2,3,1)
V1=np.array([-1,1,0,0],dtype=np.int64)
V2=np.array([1,0,-1,1],dtype=np.int64)
ELL=V1+V2
METRIC=[np.outer(V1,V1),np.outer(V1,V2)+np.outer(V2,V1),
        np.outer(ELL,ELL)]
LINKS=[(0,0,3),(0,0,1),(3,0,3)]
EVENTS=(17,27,59)

class Field:
  def __init__(self,q,a,imag):
    self.q=q;self.a=a;self.p=a*a%q;self.imag=imag
    assert (a**4+a*a-1)%q==0 and (imag*imag+1)%q==0
    self.z=[(0,1),(0,1),(-1,0),(0,-1)]
    self.nu=3*pow(5,-1,q)%q
    self.zero=self.m(np.zeros((16,16),dtype=np.int64))
    self.unit=self.m(np.eye(16,dtype=np.int64))
    self.C=[]
    for phys in range(4):
      role=ORDER.index(phys)
      c=np.zeros((16,16),dtype=np.int64)
      for mask in range(16):
        if not (mask>>role)&1:
          c[mask|(1<<role),mask]=(-1)**((mask&((1<<role)-1)).bit_count())
      self.C.append(self.m(c))

  def m(self,arr,imag=None):
    return M(self,arr,imag)
  def scale(self,X,s):
    if isinstance(s,tuple):
      a,b=s;return self.m(a*X.re-b*X.im,b*X.re+a*X.im)
    return self.m(X.re*s,X.im*s)
  def gramroot(self,role,left):
    pos=ORDER.index(role)
    diag=np.array([4*pow(5,-1,self.q)%self.q
       if (bool((mask>>pos)&1) if left else
           not bool((mask>>pos)&1)) else 1
       for mask in range(16)],dtype=np.int64)
    return self.m(np.diag(diag)),diag
  def sylv(self,R,diag):
    inv=np.array([[pow(int((diag[i]+diag[j])%self.q),-1,self.q)
      for j in range(16)] for i in range(16)],dtype=np.int64)
    return self.m(R.re*inv,R.im*inv)
  def root_tangent(self,P,Pt,Pu,Ptu,diag):
    A=P.adj();At=Pt.adj();Au=Pu.adj();Atu=Ptu.adj()
    rt=-(Pt@A+P@At);ru=-(Pu@A+P@Au)
    Lt=self.sylv(rt,diag);Lu=self.sylv(ru,diag)
    rtu=-(Ptu@A+P@Atu+Pt@Au+Pu@At+Lt@Lu+Lu@Lt)
    return Lt,Lu,self.sylv(rtu,diag)
  def root_four(self,P,Pt,Pu,Ptu,role,left):
    L,diag=self.gramroot(role,left)
    if left:
      Lt,Lu,Ltu=self.root_tangent(P,Pt,Pu,Ptu,diag)
    else:
      Lt,Lu,Ltu=self.root_tangent(P.adj(),Pt.adj(),Pu.adj(),Ptu.adj(),diag)
    return L,Lt,Lu,Ltu

class M:
  def __init__(self,f,re,im=None):
    self.f=f;self.re=np.asarray(re,dtype=np.int64)%f.q
    self.im=(np.zeros_like(self.re) if im is None
             else np.asarray(im,dtype=np.int64))%f.q
  def __add__(self,b):
    return self.f.m(self.re+b.re,self.im+b.im)
  def __neg__(self):
    return self.f.m(-self.re,-self.im)
  def __sub__(self,b):
    return self+-b
  def __matmul__(self,b):
    return self.f.m(self.re@b.re-self.im@b.im,
                    self.re@b.im+self.im@b.re)
  def adj(self):
    return self.f.m(self.re.T,-self.im.T)
  def mul(self,x):
    return self.f.scale(self,x)
  def scalar(self):
    assert self.re.shape==(1,1) and int(self.im[0,0])==0
    return int(self.re[0,0])

def gen_exterior(f,aa,bb):
  X=np.zeros((4,4),dtype=np.int64)
  X[aa,bb]=1;X[bb,aa]=1 if aa==0 else -1
  G=f.zero
  for i,j in itertools.product(range(4),range(4)):
    if X[i,j]:
      G=G+(f.C[i]@f.C[j].adj()).mul(int(X[i,j]))
  return G

def q_jets(f,Q,link):
  mod=f.q;p=f.p;a=f.a;nu=f.nu
  dF=np.diag([1,-1,-1,-1])@Q
  role,aa,bb=link;Xhat=gen_exterior(f,aa,bb)
  words=[]
  for r in range(4):
    C=f.C[r].mul(nu)
    Ct=f.zero
    for i in range(4):
      if int(dF[i,r]):
        Ct=Ct+f.C[i].mul(nu*int(dF[i,r]))
    P=f.scale(C,f.z[r]);Pt=f.scale(Ct,f.z[r])
    Pu=f.scale(C@Xhat,f.z[r]) if role==r else f.zero
    Ptu=f.scale(Ct@Xhat,f.z[r]) if role==r else f.zero
    L,Lt,Lu,Ltu=f.root_four(P,Pt,Pu,Ptu,r,True)
    R,Rt,Ru,Rtu=f.root_four(P,Pt,Pu,Ptu,r,False)
    # Negative/untransported word is metric-dependent but NOT link-dependent.
    pairs=[((P,L),(Pt,Lt),(Pu,Lu),(Ptu,Ltu)),
           ((P.adj(),R),(Pt.adj(),Rt),(Pu.adj(),Ru),(Ptu.adj(),Rtu)),
           ((-C,-L),(-Ct,-Lt),(f.zero,f.zero),(f.zero,f.zero)),
           ((-C.adj(),-R),(-Ct.adj(),-Rt),(f.zero,f.zero),(f.zero,f.zero))]
    for row in pairs:
      words.extend([row,row])
  N={}
  for idx in (0,8,13,29):
    label=idx//2;component=idx%2
    val=[f.zero,f.zero,f.zero,f.zero]
    for j in range(32):
      coefficient=(-1)**((label&j).bit_count())*pow(32,-1,mod)
      for k in range(4):
        val[k]=val[k]+words[j][k][component].mul(coefficient)
    N[idx]=val

  def prod(V,W):
    v0,vt,vu,vtu=V;w0,wt,wu,wtu=W
    return [v0@w0,vt@w0+v0@wt,vu@w0+v0@wu,
            vtu@w0+vt@wu+vu@wt+v0@wtu]

  A=N[0]
  B=prod([x.adj() for x in A],A)
  K0=[f.unit-B[0].mul(2*p*p),-B[1].mul(2*p*p),
      -B[2].mul(2*p*p),-B[3].mul(2*p*p)]
  psi=np.zeros((16,1),dtype=np.int64)
  psi[0,0]=-a;psi[14,0]=-a;psi[1,0]=p;psi[15,0]=p
  # Normalization 1/sqrt(2) enters every quadratic probability as 1/2.
  PSI=f.m(psi)
  in0=[x@PSI for x in K0]
  out=[]
  for event in EVENTS:
    Kraw=prod([x.adj() for x in N[event//2]],A)
    K=[x.mul(-2*p*a) for x in Kraw]  # all are original port-1 events
    v0,vt,vu,vtu=prod(K,in0)
    q=v0.adj()@v0
    qt=vt.adj()@v0+v0.adj()@vt
    qu=vu.adj()@v0+v0.adj()@vu
    qtu=vtu.adj()@v0+v0.adj()@vtu+vt.adj()@vu+vu.adj()@vt
    inv2=pow(2,-1,mod)
    out.append(tuple(x.scalar()*inv2%mod for x in (q,qt,qu,qtu)))
  return out

def detmod(a,p):
  rows=[[int(x)%p for x in row] for row in a]
  d=1
  for k in range(len(rows)):
    j=next((i for i in range(k,len(rows)) if rows[i][k]),None)
    if j is None:return 0
    if j!=k:rows[j],rows[k]=rows[k],rows[j];d=-d
    v=rows[k][k];d=d*v%p;iv=pow(v,-1,p)
    for i in range(k+1,len(rows)):
      c=rows[i][k]*iv%p
      for t in range(k,len(rows)):
        rows[i][t]=(rows[i][t]-c*rows[k][t])%p
  return d%p

def check(q,a,i,expected):
  f=Field(q,a,i)
  assert all(np.dot(v,[-1,-1,-2,-1])==0 and
             np.dot(v,[1,1,0,-1])==0 for v in (V1,V2))
  jets=[[q_jets(f,Q,link) for link in LINKS] for Q in METRIC]
  base=jets[0][0]
  assert all(jets[m][j][k][0]==base[k][0]
             for m in range(3) for j in range(3) for k in range(3))
  factor=(177053*f.p-85768)%q
  required=[243*pow(52428800000,-1,q)*factor,
            81*pow(65536000000,-1,q)*factor,
            117*pow(65536000000,-1,q)*factor]
  assert [x[0] for x in base]==[x%q for x in required]
  for m in range(3):
    for j in range(3):
      assert [x[1] for x in jets[m][j]]==[x[1] for x in jets[m][0]]
      assert [x[2] for x in jets[m][j]]==[x[2] for x in jets[0][j]]
  # Exact original Q3 (ell ell^T) first log scores from true Jones/Walsh.
  target=[-4*pow(3,-1,q),-181*pow(36,-1,q),-189*pow(52,-1,q)]
  assert [x[1] for x in jets[2][0]]==[
       (required[k]*target[k])%q for k in range(3)]
  M=np.array([[jets[m][j][0][3] for j in range(3)]
                   for m in range(3)],dtype=np.int64)
  d=detmod(M,q)
  q0=base[0][0]
  assert q0 not in (0,1)
  invq=pow(q0,-1,q);invrest=pow((1-q0)%q,-1,q)
  aa=invq*invrest%q
  bb=(2*q0-1)*aa*aa%q
  odds=np.array([[
    (aa*int(jets[m][j][0][3])+
     bb*int(jets[m][0][0][1])*int(jets[0][j][0][2]))%q
    for j in range(3)] for m in range(3)],dtype=np.int64)
  oddsdet=detmod(odds,q)
  code=np.array([-5,-3,-1],dtype=np.int64)
  four=np.array([[sum(int(jets[m][j][k][3])*int(code[k])
            for k in range(3))%q for j in range(3)]
            for m in range(3)],dtype=np.int64)
  codedet=detmod(four,q)
  p6=pow(f.p,6,q)
  assert (2*p6)%q not in (0,1) and (2*p6-f.p*f.p)%q
  pairdet=detmod(M*p6,q)
  assert pairdet==d*pow(p6,3,q)%q
  actual=(d,oddsdet,codedet,pairdet)
  assert actual==expected,(q,actual,expected)
  print('PASS',q,'roots',a,i,'metric-link source',M.tolist(),
        'source determinant',d,'matched odds',oddsdet,
        'native 4-leaf code',codedet,'four-arm positive score',pairdet)
  return actual

if __name__=='__main__':
  cases=[(101,27,10,(19,71,24,25)),
         (181,23,19,(139,103,145,180)),
         (1009,226,469,(604,550,55,2)),
         (4001,842,899,(1480,3818,2521,3377))]
  for entry in cases:check(*entry)
  print('ALL EXACT ORIGINAL GOLDEN/JONES 4-ARM MIXED SOURCE CHECKS PASS')
  print('No assertion of full recorded Book Info, controller admission,')
  print('Palatini tensor equality, positive_GR or GR_closed.')
