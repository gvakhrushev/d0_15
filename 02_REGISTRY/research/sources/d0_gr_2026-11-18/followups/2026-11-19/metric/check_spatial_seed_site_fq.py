"""Exact scene-interval witness for a native seed+SITE CX/NC1 reader.

This is a local conditional witness, not the full ten-sign/Choi apparatus.
"""
from fractions import Fraction as F
from math import isqrt,factorial,comb,sqrt,log1p
from decimal import Decimal,localcontext
import json
import numpy as np


def need(x,msg):
    if not x: raise AssertionError(msg)


def scene_intervals(order=24,digits=30):
    # Similarity to the random-walk group matrix removes square roots and
    # preserves each diagonal entry; all integrated coefficients are >=0.
    sizes=[9,11,13]; deg=[26,24,22]
    P=[[F(sizes[j],deg[i]) if i!=j else F(0) for j in range(3)] for i in range(3)]
    C=[F(1,x) for x in deg]
    I=[[F(int(i==j)) for j in range(3)] for i in range(3)]
    Z=[[F(0) for j in range(3)] for i in range(3)]
    def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(3)),F(0)) for j in range(3)] for i in range(3)]
    def add(A,B):return [[A[i][j]+B[i][j] for j in range(3)] for i in range(3)]
    def rightC(A):return [[A[i][j]*C[j] for j in range(3)] for i in range(3)]
    cs={0:I}; diagonal=[[F(0)]*3 for _ in range(order+1)]
    for n in range(order+1):
        for r,A in cs.items():
            if r%2==0:
                for g in range(3):diagonal[n][g]+=F(comb(r,r//2),factorial(n))*A[g][g]
        nxt={}
        for r,A in cs.items():
            nxt[r]=add(nxt.get(r,Z),mm(A,P))
            nxt[r+1]=add(nxt.get(r+1,Z),rightC(A))
        cs=nxt
    den=10**digits; root=isqrt(5*den*den)
    sqrt_lo,sqrt_hi=F(root,den),F(root+1,den)
    p_lo,p_hi=(sqrt_lo-1)/2,(sqrt_hi-1)/2
    beta_lo,beta_hi=3-sqrt_hi,3-sqrt_lo
    # On the 33-node random-walk realization ||P+2C||_infty=1;
    # the positive exponential-tail bound applies to each diagonal.
    tail=beta_hi**(order+1)/factorial(order+1)/(1-beta_hi/F(order+2))
    out=[]
    for g in range(3):
        def partial(beta):
            group=sum((diagonal[n][g]*beta**n for n in range(order+1)),F(0))/sizes[g]
            within=(1-F(1,sizes[g]))*sum((F(comb(r,r//2),factorial(r))*beta**r*C[g]**r for r in range(0,order+1,2)),F(0))
            return group+within
        out.append((partial(beta_lo),partial(beta_hi)+tail))
    return p_lo,p_hi,out,tail


def dec(x):
    with localcontext() as ctx:
        ctx.prec=45
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def main():
    plo,phi,scene,tail=scene_intervals();a_lo,a_hi=scene[0];b_lo,b_hi=scene[2]
    need(a_lo>b_hi,'strict actual spatial diagonal gap')
    z0lo,z0hi=3*plo-1,3*phi-1
    z1lo,z1hi=2-2*phi,2-2*plo
    b0lo=plo*z0lo+(1-phi)*z1lo; b0hi=phi*z0hi+(1-plo)*z1hi
    b1lo=plo*z1lo+(1-phi)*z0lo; b1hi=phi*z1hi+(1-plo)*z0hi
    denlo=b0lo*a_lo+b1lo*b_lo; denhi=b0hi*a_hi+b1hi*b_hi
    nlo=(3-5*phi)*(a_hi-b_lo);nhi=(3-5*plo)*(a_lo-b_hi)
    need(nhi<0 and denlo>0,'strict sign')
    clo,chi=nlo/denlo,nhi/denhi
    need(F(-706,10**7)<clo<chi<F(-705,10**7),'certified nonzero source interval')
    p=(sqrt(5)-1)/2;a=sqrt(p);v=np.array([a,p]);G=np.array([[a,-p],[p,a]])
    # V maps protected x,u to x,u,D,tail; onsite letters are CX(X,D),
    # CX(U,D), CX(D,tail), G(tail), CX(D,tail).
    V=np.zeros((16,4))
    for x in (0,1):
      for u in (0,1):
       col=2*x+u
       for d0 in (0,1):
        d=d0^x^u
        for t0 in (0,1):
         for t1 in (0,1):
          t=t1^d
          row=8*x+4*u+2*d+t
          V[row,col]+=v[d0]*v[t0]*G[t1,t0^d]
    P0=np.diag([float((i//2)%2==0) for i in range(16)])
    P10=np.diag([float((i//2)%2==1 and i%2==0) for i in range(16)])
    P11=np.diag([float((i//2)%2==1 and i%2==1) for i in range(16)])
    def effect(Q):return np.einsum('ki,kl,lj->ij',V,Q,V,optimize=False)
    E0,E1,Ebad=map(effect,(P0,P10,P11));q=np.diag([p*p,p,p,p*p])
    need(np.max(np.abs(E1-q))<2e-15 and np.max(np.abs(E0-(np.eye(4)-q)))<2e-15,'full SITE/seed NC1 effects')
    need(np.max(np.abs(Ebad))<2e-15,'invalid 11 dark')
    FQ=E0+p*E1
    need(np.max(np.abs(FQ-(np.eye(4)-p*p*q)))<2e-15,'canonical FQ effect')
    z0,z1=1-p**4,1-p**3;w0=p*z0+p*p*z1;w1=p*z1+p*p*z0
    rows={}
    for n in (2,3,4,8):
      delta=p**(n+1)
      for k in (0,1):
       for x in (0,1):
        qsum=0.
        for h in (0,1):
         for bits in range(1<<n):
          wh=(p if h==0 else p*p)
          w=wh
          for i in range(n):w*=p*p if ((bits>>i)&1) else p
          u=h or (k and bits==0)
          qsum+=w*(p*p if (x^int(u))==0 else p)
        z=1-p*p*qsum
        expected=(w0 if x==0 else w1)+k*delta*((z1-z0) if x==0 else (z0-z1))
        need(abs(z-expected)<4e-14,'actual finite H/Z seed and CX reader')
      c=float((clo+chi)/2)
      rows[str(n)]={'delta':delta,'leading_log_contrast_over_delta':log1p(delta*c)/delta}
    out={'status':'PASS; exact rational scene-gap interval; local witness only',
      'scene_T0_interval':[dec(a_lo),dec(a_hi)],'scene_T2_interval':[dec(b_lo),dec(b_hi)],
      'T_g_definition':'exp(beta) times actual S_infinity diagonal',
      'scene_tail_upper':dec(tail),'normalized_leading_coefficient_interval':[dec(clo),dec(chi)],
      'native_CX_NC1_effect_error':float(np.max(np.abs(E1-q))),
      'canonical_FQ_effect_applied':True,'same_unweighted_scene_marginal':True,
      'weighted_scene_marginal_changes':True,'seed_finite_checks':rows,
      'physical_scene_SITE_state_admitted_by_full_D0':False,
      'original_full_geometric_bank_identified':False,'GR_closed':False}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
