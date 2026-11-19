"""Covariance formula and its sharp general bound on the real 33-node scene."""
import json
import math
import numpy as np
from check_local_gibbs_records import scene,scene_heat


def need(x,msg):
    if not x: raise AssertionError(msg)


def main():
    p=(math.sqrt(5)-1)/2;beta=2*p*p
    B,C=scene();steps=128
    S=sum(scene_heat(B,C,2*math.cos(2*math.pi*j/steps),beta) for j in range(steps))/steps
    ev=np.linalg.eigvalsh(S);lo,hi=float(ev[0]),float(ev[-1]);rng=np.random.default_rng(20261119)
    z0,z1=1-p**4,1-p**3
    b0=p*z0+p*p*z1;b1=p*z1+p*p*z0
    Z=np.diag([b0,b1]);SO=np.kron(S,np.eye(2));ZO=np.kron(np.eye(33),Z)
    ss=hi-lo;zz=abs(b0-b1);covbound=ss*zz/4
    max_cov=0.;max_error=0.
    for _ in range(30):
        psi=rng.normal(size=66)+1j*rng.normal(size=66);psi/=np.linalg.norm(psi)
        E=lambda A:complex(np.einsum('i,ij,j->',psi.conj(),A,psi,optimize=False))
        s,z,sz=E(SO),E(ZO),E(np.kron(S,Z))
        cov=sz-s*z
        lhs=sz/z-s
        max_error=max(max_error,abs(lhs-cov/z));max_cov=max(max_cov,abs(cov))
        need(abs(lhs-cov/z)<1e-13,'covariance identity')
        need(abs(cov)<=covbound+1e-13,'Popoviciu covariance')
    # Exact witness starts in (|a,0>+|b,1>)/sqrt(2); actual a,b groups.
    psi=np.zeros(66);psi[0]=psi[2*20+1]=1/math.sqrt(2)
    def weighted(z):
        zm=np.diag(z); wm=np.kron(np.eye(33),zm)
        den=np.einsum('i,ij,j->',psi,wm,psi,optimize=False)
        numer=np.einsum('i,ij,j->',psi,np.kron(S,zm),psi,optimize=False)
        return float(numer/den)
    # Compare the same initial density and two seed programme effects.
    rows={};exact_slope=(z1-z0)*(S[0,0]-S[20,20])/(b0*S[0,0]+b1*S[20,20])
    for n in (2,4,8,20):
        delta=p**(n+1);d=delta*(z1-z0)
        A=[b0,b1];Bz=[b0+d,b1-d]
        sw0,sw1=weighted(A),weighted(Bz)
        actual=abs(math.log(sw1/sw0))/delta
        zmin=min(A+Bz);op_delta=abs(z1-z0)
        general=ss*op_delta/(lo*zmin)
        subspace=abs(S[0,0]-S[20,20])*op_delta/(min(S[0,0],S[20,20])*zmin)
        need(actual<=subspace+3e-14 and subspace<=general+3e-14,'same-input leading bounds')
        rows[str(n)]={'actual_abs_log_contrast_over_delta':actual,
            'two_scene_sector_bound':subspace,'full_scene_operator_bound':general}
    print(json.dumps({'status':'PASS; explicit operator identity, real scene and witness',
      'scene_eigen_min':lo,'scene_eigen_max':hi,'scene_spectral_width':ss,
      'fq_effect_spectral_width':zz,'maximum_sample_covariance':max_cov,
      'theoretical_covariance_upper':covbound,'max_sample_identity_error':max_error,
      'witness_limit_coefficient':exact_slope,'examples':rows,
      'full_physical_bank_and_Book_price_derived':False,'GR_closed':False},indent=2))


if __name__=='__main__':main()
