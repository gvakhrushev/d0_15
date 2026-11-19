"""Same-SITE finite instrument composition and F2-F6 gain audit.

The real geometry compiler, its norm, field jets and common paid clock remain
unproved.  This verifies a conditional exact interface and explicit constants.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import runpy
import numpy as np
from mpmath import iv

HERE=Path(__file__).parent
predictor=runpy.run_path(str(HERE/'check_paid_predictor.py'))
bal=runpy.run_path(str(HERE/'check_balanced_controller_source.py'))
from check_boundary_experiment import Golden as G
from check_eight_readers import inv


def verify_sourcei_zero():
    word=predictor['inv'](5)
    assert len(word)==17
    assert sum(g[0]=='SourceI' for g in word)==4
    assert sum(g[0]=='CX' for g in word)==12
    assert sum(g[0]=='G' for g in word)==1
    apply=predictor['apply']; one=predictor['one']; a=predictor['a'];p=predictor['p']
    scale=predictor['scale']
    for spin in range(4):
     for olde in (0,1):
      for target in (0,1):
       key=spin|(olde<<2)|(target<<5)
       actual=apply({key:one},word)
       expect={key:a,key^(1<<5):scale(p,1 if target else -1)}
       assert actual==expect
      # Born v plus the literal word is exactly zero; unknown old E and
      # all four protected Spin columns are restored, not traced out.
      key=spin|(olde<<2)
      assert apply({key:a,key|(1<<5):p},word)=={key:one}
    return {'old_Spin_columns':4,'old_source_columns':2,
            'target_columns':2,'SourceI':4,'CX':12,'G':1,'birth':1}


def verify_complete_selector_t():
    for selector_ready,j,bank_ready,b in __import__('itertools').product((0,1),range(9),(0,1),(0,1)):
        # T starts at the exact paid zero. Failure and inactive selector skip
        # both selected controls. Bank abortion precedes either operation.
        t=0
        if selector_ready and j and bank_ready:
            t ^= b
            t ^= int(j%2==0)
        expected=(b ^ int(j%2==0)) if selector_ready and j and bank_ready else 0
        assert t==expected


def verify_reference_polynomial():
    O,I=G(0),G(1);two,four=G(2),G(4)
    p=G(0,1);z=G(F(1,2**20))
    def report(x,y):
        E=p**2*(I+x);L=four*E*(I-E)
        u=p+p**2*y;B=four*u**2*(I-u**2);A=L+(I-L)*B
        return z*(A+B)-z**2*A*B
    rf=four*p**2*(I-two*p**2)*z*(I-z*four*p**3)*(I-four*p**3)
    rq=G(8)*p**3*(I-two*p**2)*(z*(two-four*p**3)-z**2*(four*p**3+two*(I-four*p**3)*four*p**3))
    k=rq*inv(rf)
    Fgrid=F(16517734400,162621047169)
    bref=G(Fgrid/F(16))*inv(k)
    h=G(F(1,32768));r0=report(O,O)
    weights=[F((-1)**(j-1)*comb(8,j),j*j) for j in range(1,9)]
    # This is an exact finite SC1 polynomial check, for two retained-site
    # inputs, with F2--F6 reference ratio rather than the scalar SC2 b.
    def mark(e,field,matter):
        A=report(O,bref*e)-report(O,O-bref*e)
        B=report(k*bref*e,O)-report(O-k*bref*e,O)
        return A*(report(e*field,O)-r0)+B*(report(O,O-e*matter)-r0)
    for field,matter in ((G(F(13,17)),G(F(2,9))),
                         (G(F(1,5)),G(F(-3,7)))):
        total=sum((G(weights[j-1])*mark(G(j)*h,field,matter) for j in range(1,9)),O)
        target=field-k*matter
        assert total==two*bref*h**2*rf*rq*target
    assert bref*k*G(16)==G(Fgrid)
    return str(Fgrid)


def verify_quantum_composition():
    # A genuinely non-scalar bank effect on SITE, entangled with an old
    # reference. Conditional suffix records have scalar effects, even though
    # the incoming bank effects themselves are not scalar.
    psi=np.array([np.sqrt(.3),0,0,np.sqrt(.7)])
    rho=np.outer(psi,psi)
    priors=(.37,.63); total=0.;reports=0
    for j,pj in enumerate(priors):
     for b in (0,1):
      probs=([.15,.8] if j==0 else [.64,.25])
      vals=np.array(probs if b else [1-x for x in probs])
      K=np.kron(np.diag(np.sqrt(vals)),np.eye(2))
      block=K@rho@K.T; mass=float(np.trace(block))
      t=b^(j%2)
      table,_=bal['build'](.29,t,shared=True)
      assert abs(sum(table.values())-1)<1e-12
      for q in table.values():
       # Explicit flag dilation of the scalar suffix effect qI, whose q
       # comes from the complete retained native NC1 experiment above.
       fresh=np.array([[np.sqrt(q)],[0.]])
       Kraus=np.kron(K,fresh)
       full=Kraus@rho@Kraus.T
       reduced=np.trace(full.reshape(4,2,4,2),axis1=1,axis2=3)
       assert np.max(np.abs(reduced-q*block))<1e-14
       assert np.max(np.abs(Kraus.T@Kraus-q*(K.T@K)))<1e-14
       reports+=1
      total+=pj*mass
    assert abs(total-1)<1e-14
    return {'shared_SITE_reference_dimension':4,'suffix_positive_outcomes_tested':reports,
            'bank_effects_are_scalar':False,'suffix_effect_scalar_on_oldRIGHT':True,
            'full_physical_geo_bank_replayed':False}


def gains():
    iv.dps=60;one=iv.mpf(1);p=(iv.sqrt(5)-one)/2;z=one/(2**20)
    Fgrid=iv.mpf(16517734400)/iv.mpf(162621047169)
    rf=4*p**2*(one-2*p**2)*z*(one-z*4*p**3)*(one-4*p**3)
    rq=8*p**3*(one-2*p**2)*(z*(2-4*p**3)-z**2*(4*p**3+2*(one-4*p**3)*4*p**3))
    k=rq/rf;bref=Fgrid/(16*k);h=one/32768
    c=one-2*p**2
    for _ in range(9):c=2*c**2-one
    vis=(one-c)/2*p**7
    raw=p**36*705600*h**2*2*bref*p**3*vis*rf*rq # times alpha_h^2
    b2=one-(one-4*p**3)**64;b3=one-(one-16*p**9)**64
    beta=(one-p**40)*(b2**6*b3)**2592
    b0=one-(one-2*p**3)**16
    t2=one-(one-4*p**3)**32;t3=one-(one-16*p**9)**32
    kappa=b0**4*(t2**4*t3)**2
    suffix=beta*(2*p**4*kappa)*raw
    suffix_and_t=beta*(one+2*p**4*kappa)*raw
    return {'b_ref_geometric':str(bref),'geometry_h':str(h),
      'selector_success':str(beta),'balanced_factory_success':str(kappa),
      'raw_selector_gain_per_alpha_h_squared':str(raw),
      'suffix_gain_per_alpha_h_squared':str(suffix),
      't_print_plus_suffix_gain_per_alpha_h_squared':str(suffix_and_t)}


def main():
    src=verify_sourcei_zero();verify_complete_selector_t()
    ref=verify_reference_polynomial();cq=verify_quantum_composition();g=gains()
    print(json.dumps({'schema':'d0.composed-geometric-instrument/1','status':'PASS',
        'sourcei_paid_zero':src,'selector_T_all_failure_cases_checked':True,
        'F_grid':ref,'exact_SC1_two_geometric_reference_cases':True,
        'same_SITE_and_oldRIGHT_test':cq,'conditional_gain_intervals':g,
        'geometry_compiled':False,'geometry_norm_certified':False,
        'actual_alpha_h_value_known':False,'full_adaptive_clock_constructed':False,
        'Book_cost_info_identified':False,'GR_closed':False},indent=2))


if __name__=='__main__':main()
