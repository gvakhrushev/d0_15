"""Full native writer NC1 + paid complementary or second golden NC1.

The downstream Fourier localization is consumed through its independently
proved scalar effect; this script checks the complete five-qubit word and
its retained outcomes. Physical Book03 prices and joint clocks remain open.
"""
import json
import math
import numpy as np


def need(x,s):
    if not x:raise AssertionError(s)


def main():
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p);v=np.array([a,p]);G=np.array([[a,-p],[p,a]])
    X=np.array([[0.,1.],[1.,0.]])
    n=5;dim=1<<n
    def mask(w):return 1<<(n-1-w)
    def one(M,w,A):
        out=np.zeros_like(M);m=mask(w)
        for j in range(dim):
          b=int(bool(j&m));base=j&~m
          for z in (0,1):out[base|(m if z else 0)]+=A[z,b]*M[j]
        return out
    def cx(M,c,t):
        out=np.zeros_like(M);cm,tm=mask(c),mask(t)
        for j in range(dim):out[j^(tm if j&cm else 0)]+=M[j]
        return out
    def proj(M,w,b):
        out=M.copy();m=mask(w)
        for j in range(dim):
          if int(bool(j&m))!=b:out[j]=0
        return out
    def nc1(M,h,tail):return cx(one(cx(M,h,tail),tail,G),h,tail)
    # Wires P,H,A,Q,B, all four fresh golden births; external h=1 is
    # independent and retained, so each conditional X below is actual CX(h,*).
    V=np.zeros((dim,2))
    for old in (0,1):
      for h,A0,Q,B in np.ndindex(2,2,2,2):
        j=(old<<4)|(h<<3)|(A0<<2)|(Q<<1)|B
        V[j,old]=v[h]*v[A0]*v[Q]*v[B]
    V=nc1(cx(V,0,1),1,2)
    branches={}
    for h in (0,1):
      pre=proj(V,1,h)
      # NC1 with h=1 has true tail A=0, test forbidden 11.
      if h:need(np.linalg.norm(proj(pre,2,1))<1e-14,'first NC1 11 dark')
      # Model 1: Q <- G^-1 Q = X_h G X_h Q, then Q ^= h and H.
      det=one(one(one(pre,3,X),3,G),3,X)
      det=one(det,3,X);det=cx(det,1,3);det=nc1(det,3,4)
      # Model 2: independent second golden reader, Q ^= P then Q ^= h.
      ind=one(cx(pre,0,3),3,X);ind=nc1(ind,3,4)
      for b in (0,1):
        branches[('det',h,b)]=proj(det,3,b)
        branches[('ind',h,b)]=proj(ind,3,b)
        if b:
          need(np.linalg.norm(proj(branches[('det',h,b)],4,1))<1e-14,'second NC1 11 dark')
          need(np.linalg.norm(proj(branches[('ind',h,b)],4,1))<1e-14,'independent NC1 11 dark')
    def eff(k):return np.einsum('ki,kj->ij',k,k,optimize=False)
    E0=np.diag([p,p*p]);E1=np.diag([p*p,p]);I=np.eye(2)
    detE={(h,b):eff(branches['det',h,b]) for h,b in np.ndindex(2,2)}
    indE={(h,b):eff(branches['ind',h,b]) for h,b in np.ndindex(2,2)}
    targetsD={(0,0):np.zeros((2,2)),(0,1):E0,(1,0):E1,(1,1):np.zeros((2,2))}
    targetsI={(0,0):p**3*I,(0,1):np.diag([p**2,p**4]),
              (1,0):np.diag([p**4,p**2]),(1,1):p**3*I}
    derr=max(float(np.max(np.abs(detE[x]-targetsD[x]))) for x in targetsD)
    ierr=max(float(np.max(np.abs(indE[x]-targetsI[x]))) for x in targetsI)
    need(derr<2e-14 and ierr<2e-14,'all four real output branches')
    for E in (detE,indE):
      need(np.max(np.abs(sum(E.values())-I))<2e-14,'full trace preserving instrument')
      weights={(0,0):.8,(0,1):.35,(1,0):.72,(1,1):.49}
      W=sum(weights[x]*E[x] for x in E)
      need(abs((W[0,0]-W[1,1])-p**3*(weights[0,1]-weights[1,0]))<2e-14,
           'arbitrary branch weights exact necessity')
    # Same code 0/10: FQ experiment uses weights p^(h+b), no extra price.
    Wd=sum(p**(h+b)*detE[h,b] for h,b in np.ndindex(2,2))
    Wi=sum(p**(h+b)*indE[h,b] for h,b in np.ndindex(2,2))
    z0=p+p**3;z1=2*p*p
    need(np.max(np.abs(Wd-p*I))<2e-14,'det complement pathwise constant')
    need(np.max(np.abs(Wi-z0*z1*I))<2e-14,'independent paired recorder effect scalar')
    # P marginal channels: sum over physically retained outcomes only after
    # checking full branch states; P block overlap retains actual environment.
    def dephase(name,weighted):
      val=0.
      for h,b in np.ndindex(2,2):
        K=branches[name,h,b];w=p**(h+b) if weighted else 1.
        val+=w*np.dot(K[:16,0],K[16:,1])
      z=p if name=='det' and weighted else z0*z1 if weighted else 1.
      return val/z
    d0=dephase('det',False);d1=dephase('det',True)
    i0=dephase('ind',False);i1=dephase('ind',True)
    need(abs(d0-2*p**1.5)<2e-14 and abs(d1-d0)<2e-14,'det recorder same P decoherence')
    need(abs(i0-4*p**3)<2e-14,'independent recorder P decoherence')
    need(abs(i1-p**3*(1+p)**2/(z0*z1))<2e-14,'independent FQ decoherence')
    # Later h-dependent factors lambda_h reintroduce gap p^4 (lambda_0-lambda_1)
    # on det branch even while both real complementary reports are retained.
    l0,l1=.4,.7
    W=p*(l0*E0+l1*E1)
    need(abs((W[0,0]-W[1,1])-p**4*(l0-l1))<2e-14,'later h-sensitive response')
    q=.5;ell=math.log(1/p);cost=3-math.log(2)/ell
    ind_tilt0=sum(p**(1+b)*indE[1,b][0,0] for b in (0,1))/(z0*z1)
    ind_tilt1=sum(p**(1+b)*indE[1,b][1,1] for b in (0,1))/(z0*z1)
    need(abs(ind_tilt0-p**3/z0)<2e-14 and abs(ind_tilt1-.5)<2e-14,'independent paired reader changes tilted H1 law')
    curvature=4*p**6/ell
    out={'status':'PASS; native retained NC1 and conditional weight algebra',
      'deterministic_branch_effect_error':derr,'independent_branch_effect_error':ierr,
      'det_joint_FQ_scalar':p,'ind_joint_FQ_scalar':z0*z1,
      'complete_comparator_FQ_scalar_excluding_eta':p*(255+p)/256,
      'arbitrary_branch_weight_effect_gap':'p^3*(w01-w10)',
      'later_h_sensitive_FQ_gap':'p^4*(lambda0-lambda1)',
      'det_unweighted_programme_coherence_multiplier':d0,
      'det_weighted_programme_coherence_multiplier':d1,
      'ind_unweighted_programme_coherence_multiplier':i0,
      'ind_weighted_programme_coherence_multiplier':i1,
      'ind_tilted_H1_prob_given_P0':ind_tilt0,
      'ind_tilted_H1_prob_given_P1':ind_tilt1,
      'det_tilted_H1_prob_given_P0':p*p,
      'det_tilted_H1_prob_given_P1':p,
      'isolated_declared_CQ_pair_cost_at_half':cost,
      'isolated_declared_CQ_pair_first_source_at_half':0.,
      'isolated_declared_CQ_pair_second_source_at_half':curvature,
      'full_Book03_weights_selected':False,'full_independent_preparation_dynamics_derived':False,
      'full_geometric_sign_and_clock_compiled':False,'GR_closed':False}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
