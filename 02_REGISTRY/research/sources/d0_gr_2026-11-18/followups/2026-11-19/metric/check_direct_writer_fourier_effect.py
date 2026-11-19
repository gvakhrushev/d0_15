"""Compose native direct descriptor instrument with Fourier/SITE equality.

All effects are on old SITE, programme P and arbitrary retained RIGHT.
Conditional physical factory readiness and exact FQ weights remain hypotheses.
"""
from itertools import product
import json
import math
import numpy as np
from check_fourier_fresh_localization import original_reference
from check_local_gibbs_records import scene,scene_heat


def need(v,s):
    if not v:raise AssertionError(s)


def main():
    p=(math.sqrt(5)-1)/2;a=math.sqrt(p)
    pairs,_,size=original_reference();need(size==256 and len(pairs)==64,'original Fourier resource')
    theta=math.asin(p);A=p*math.sin(712*theta);c=-p*math.cos(712*theta)
    def chi(y):
      v=np.zeros(128)
      for j,k in enumerate(pairs):
        t=sum(k[i]*y[i] for i in range(4))%4
        v[2*j+(t&1)]=(-1 if t&2 else 1)/128
      return v
    def material(y,h):
      ph=math.pi/2*(y[1]+h*y[0]);v=np.zeros(16)
      v[1]=a;v[14]=c;v[0]=A*math.cos(ph);v[15]=A*math.sin(ph)
      return v
    sites=[(0,0,0,0),(1,0,0,0)];dim=8;block=2048;outputs=2*dim*block
    K=[np.zeros((outputs,dim)),np.zeros((outputs,dim))]
    kap=((a,p),(p,a))
    for x,b,r in product(range(2),range(2),range(2)):
      j=(x*2+b)*2+r
      for h in (0,1):
        slot=h*dim+j;aux=np.kron(material(sites[x],h),chi(sites[x]))
        K[h][slot*block:(slot+1)*block,j]=kap[h][b]*aux
    gram=[np.einsum('ki,kj->ij',k,k,optimize=False) for k in K]
    e0=np.diag([p if ((j//2)&1)==0 else p*p for j in range(dim)])
    e1=np.eye(dim)-e0;q=1/256
    err=max(float(np.max(np.abs(gram[0]-q*e0))),float(np.max(np.abs(gram[1]-q*e1))))
    need(err<1e-15,'joint retained writer, protected input and ready-effect Gram')
    need(np.max(np.abs(gram[0]+gram[1]-q*np.eye(dim)))<1e-15,'localizer alone scalar')
    z0=p+p**3;z1=2*p*p
    weighted=gram[0]+p*gram[1]
    z=np.diag([z0 if ((j//2)&1)==0 else z1 for j in range(dim)])
    need(np.max(np.abs(weighted-q*z))<1e-15,'weighting both actual writer outcomes')
    need(abs(z0-z1-p**5)<1e-15 and abs(z0-z1)>0.09,'joint FQ effect is not scalar')
    lam=(255+p)/256
    need(np.max(np.abs((e0+p*e1)-z))<1e-15,'unweighted localizer both outcomes')
    # Same SITE with P=|+>; physically keep the two H outcomes as orthogonal
    # blocks until the deliberately evaluated programme marginal is taken.
    psi=np.zeros(dim);psi[0]=psi[2]=1/math.sqrt(2)
    vectors=[np.einsum('ij,j->i',k,psi,optimize=False) for k in K]
    def pblock(v,h,b):
      j=(0*2+b)*2+0;slot=h*dim+j
      return v[slot*block:(slot+1)*block]
    def coherence(weights):
      numerator=sum(weights[h]*np.dot(pblock(vectors[h],h,0),pblock(vectors[h],h,1)) for h in (0,1))
      denominator=sum(weights[h]*np.dot(vectors[h],vectors[h]) for h in (0,1))
      return numerator/denominator
    coh=coherence((1,1));cohw=coherence((1,p))
    need(abs(coh-a*p)<1e-13 and abs(cohw-a*p)<1e-13,'no false state replacement: programme dephases')
    # Actual original 33-scene; proposed entangled scene/P initial state is a
    # mathematical witness, physical D0 admissibility remains unestablished.
    B,C=scene();beta=2*p*p
    Sinf=sum(scene_heat(B,C,2*math.cos(2*math.pi*j/128),beta) for j in range(128))/128
    sa,sb=float(Sinf[0,0]),float(Sinf[20,20]);s=(sa+sb)/2
    sw=(z0*sa+z1*sb)/(z0+z1)
    rel=sw/s-1
    need(abs(rel-(z0-z1)*(sa-sb)/((z0+z1)*(sa+sb)))<1e-14,'scene programme correlation')
    need(abs(rel)>3e-5,'actual scene gives nonzero leading effect')
    qfactor=q*lam
    for aa,bb in ((1.,1.),(.2,.7),(1.,p)):
        op=aa*e0+bb*e1
        need(abs((op[0,0]-op[2,2])-(aa-bb)*p**3)<1e-14,'general record-weight scalar iff equal')
    fq_slope=p**5/(math.log(1/p)*((z0+z1)/2))
    out={'status':'PASS; complete physical word interfaces, conditional marked hardware',
       'protected_SITE_P_RIGHT_dimension_tested':dim,'joint_physical_equality_gram_error':err,
       'equality_and_writer_effects':['q E_H0','q E_H1'],
       'localization_outcome_weights_only_effect':'lambda I',
       'both_writer_and_localizer_FQ_effect':'lambda (z0 P0 + z1 P1)',
       'q_equal':q,'lambda_both_localizer_outcomes':lam,
       'general_H_weight_effect_gap':'(a0-a1)*p^3',
       'conditional_FQ_log_weight_slope_at_t_half':fq_slope,
       'both_effect_eigenvalues_without_hardware':[lam*z0,lam*z1],
       'eigenvalue_gap_before_lambda':z0-z1,'exact_gap':'p^5',
       'actual_unchanged_input_P_pure_offdiag':.5,
       'after_normalized_equality_unweighted_offdiag':coh,
       'after_normalized_equality_H_FQ_weighted_offdiag':cohw,
       'same_input_coherence_multiplier':2*coh,
       'correlated_scene_P_witness_relative_leading_shift':rel,
       'correlated_scene_P_witness_log_leading_shift':math.log1p(rel),
       'spatial_scene_P_state_physical_admission_proved':False,
       'FQ_weights_selected_by_complete_Book03':False,
       'full_geometric_bank_or_joint_clock_compiled':False,'GR_closed':False}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
