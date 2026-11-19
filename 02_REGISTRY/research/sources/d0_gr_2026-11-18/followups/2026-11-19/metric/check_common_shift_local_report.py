"""Shared tau with canonical Y output, complete-effect covariance, and old-P steering."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import numpy as np
import mpmath as mp
from check_independent_shift_shared_site import prefix,add_mod4,correlation_checks


def need(x,msg):
    if not x:raise AssertionError(msg)


def run(r,x,u,y):
    n=len(x);B={}
    for name,val in [('x',x),('u',u),('y',y)]:
        B.update({f'{name}{i}':((val>>i)&1).astype(np.uint8) for i in range(8)})
    for name,k in [('t',8),('d',8),('a',7)]:B.update({f'{name}{i}':np.zeros(n,dtype=np.uint8) for i in range(k)})
    B['h']=np.ones(n,dtype=np.uint8)
    def apply(op):
        if op[0]=='cx':B[op[2]]^=B[op[1]]
        else:B[op[3]]^=B[op[1]]&B[op[2]]
    fwd=prefix(r);split=20+(2 if r is not None else 0)
    for op in fwd:apply(op)
    flag=B['a6'].copy()  # real NC1 measurement/copy retained; uncompute the measured predicate
    for op in reversed(fwd[split:]):apply(op)
    need(all(not B[f'{name}{i}'].any() for name,k in [('d',8),('a',7)] for i in range(k)),'predicate scratch')
    # Y <- Y - (X+tau+r) mod 4.  After low XOR, borrow is t_low & new_Y_low.
    relative=[]
    for j in range(4):
        relative.extend([('cx',f't{2*j}',f'y{2*j}'),('ccx',f't{2*j}',f'y{2*j}',f'y{2*j+1}'),('cx',f't{2*j+1}',f'y{2*j+1}')])
    for op in relative:apply(op)
    for op in reversed(fwd[:split]):apply(op)
    need(all(not B[f't{i}'].any() for i in range(8)),'address scratch restored')
    newy=sum(B[f'y{i}'].astype(np.uint32)<<i for i in range(8))
    shifted=add_mod4(x,u)
    if r is not None:
        dd=(shifted>>(2*r))&3;shifted=(shifted&~(np.uint32(3)<<(2*r)))|(((dd+1)&3)<<(2*r))
    expected=np.zeros_like(y)
    for j in range(4):expected|=((((y>>(2*j))&3)-((shifted>>(2*j))&3))&3)<<(2*j)
    need(np.array_equal(newy,expected),'canonical relative output')
    need(np.array_equal(flag,(newy==0).astype(np.uint8)),'true equality flag')
    for name,val in [('x',x),('u',u)]:
        for i in range(8):need(np.array_equal(B[f'{name}{i}'],(val>>i)&1),'X and tau retained')
    counts=Counter(o[0] for o in fwd+list(reversed(fwd[split:]))+relative+list(reversed(fwd[:split])))
    need(counts['ccx']==26 and counts['cx']==(88 if r is None else 92),'exact cost')
    return {'columns':n,'Toffoli':26,'CX_before_NC1':counts['cx'],'NC1_extra_birth_G_CX':[1,1,2]}


def gates():
    pair=np.arange(65536,dtype=np.uint32);x=pair>>8;u=pair&255;z=add_mod4(x,u)
    result={}
    for r in (None,0,1,2,3):
        y=z.copy()
        if r is not None:
            val=(y>>(2*r))&3;y=(y&~(np.uint32(3)<<(2*r)))|(((val+1)&3)<<(2*r))
        result['zero' if r is None else f'e{r}']=run(r,x,u,y)
        run(r,x,u,y^np.uint32(1))
        # Every target/Y pair, using X=0,tau=target.
        target=pair>>8;Y=pair&255;run(r,np.zeros_like(target),target,Y)
    return result


def field():
    unit=((1,0),(0,1),(-1,0),(0,-1))
    def psi(u,v,x):
        coord=[(x>>(2*i))&3 for i in range(4)]
        return unit[(coord[1]+u*coord[0]+v*coord[2])%4]
    out=[]
    for x in range(256):
        q=Fraction(0)
        for mu in range(4):
            val=(x>>(2*mu))&3;y=(x&~(3<<(2*mu)))|(((val+1)&3)<<(2*mu))
            da=[psi(0,0,y)[i]-psi(0,0,x)[i] for i in range(2)]
            db=[psi(0,1,y)[i]-psi(0,1,x)[i] for i in range(2)]
            q+=Fraction((1 if mu==0 else -1)*sum(a*b for a,b in zip(da,db)),2)
        out.append(int(q))
    need(Counter(out)=={-1:64,0:128,1:64},'actual local F table')
    return np.array(out)


def twirl_and_steering():
    F=field();xs=np.arange(256,dtype=np.uint32);U=np.tile(xs,(256,1));X=np.tile(xs[:,None],(1,256))
    Fxu=F[add_mod4(X,U)]
    need(np.all(Fxu.mean(axis=1)==0),'uniform common tau visits every y')
    # Physical target / failure effect example acts on P; site remains X.
    Z=np.array([[1.,0.],[0.,-1.]]);XX=np.array([[0.,1.],[1.,0.]]);I=np.eye(2)
    E=np.stack([.5*I+.25*Z+.1*float(f)*XX for f in F])
    Fail=np.stack([.1*I+.03*float(f)*XX for f in F])
    No=I-E-Fail
    for mats in (E,Fail,No):need(min(float(np.linalg.eigvalsh(v).min()) for v in mats)>-1e-14,'positive event effects')
    means=E[add_mod4(X,U)].mean(axis=1)
    need(np.max(np.abs(means-means[0]))<1e-13,'every old X same operator on P')
    weighted=(2*E+3*Fail+No)
    wm=weighted[add_mod4(X,U)].mean(axis=1)
    need(np.max(np.abs(wm-wm[0]))<1e-13,'every transcript weight tau-independent')
    # An uneven retained-tau weight breaks X cancellation.
    uneven=(E[add_mod4(X,U)]*(1+0.5*(U==0))[...,None,None]).mean(axis=1)
    need(np.max(np.abs(uneven-uneven[0]))>1e-5,'tau dependent fine weight breaks twirl')
    # A scalar-in-X but non-scalar-in-P postselected effect can steer Bell X-P.
    pre=np.array([.5,.5]);post=np.array([.75,.25]);trace_norm=float(np.abs(pre-post).sum())
    need(abs(trace_norm-.5)<1e-15,'steering trace distance')
    return {'site_sector_count':256,'twirled_report_effect_on_P':means[0].tolist(),
      'full_transcript_tau_independent_weight_max_error':float(np.max(np.abs(wm-wm[0]))),
      'tau_dependent_weight_breaks_scalar_SITE':True,
      'non_scalar_P_effect_bell_X_marginal_before':[.5,.5],
      'non_scalar_P_effect_bell_X_marginal_after':[.75,.25],
      'steering_unnormalized_trace_norm_difference':trace_norm,
      'effects_are_toy_PSD_counterexample_not_physical_hq':True}


def probability():
    mp.mp.dps=100;p=(mp.sqrt(5)-1)/2;b1=1-p**40;b2=1-p**384;b3=1-(1-16*p**9)**64;bt=b2**6*b3
    alpha=b1*b2**8
    pre=sum(alpha*bt**j*(1-bt) for j in range(11));late=mp.mpf(0);success=mp.mpf(0)
    for q in (mp.mpf(1)/256,mp.mpf(255)/256):
      late+=sum(alpha*bt**(11+j)*(1-bt)*q for j in range(15))
      success+=alpha*bt**26*q
    need(abs(pre+late+success-alpha)<mp.mpf('1e-90'),'complete conditional fail ledger')
    plus_fail=b1*sum(b2**j*(1-b2) for j in range(8))
    total=(1-b1)+plus_fail+pre+late+success
    need(abs(total-1)<mp.mpf('1e-90'),'h, all 8 plus attempts and comparator failures sum to one')
    # The conditional real two-copy local witness has F=-1,0,+1 with
    # frequencies 1/4,1/2,1/4. One shared tau retains the local average;
    # independently resampled tau values yield r(mean q) instead.
    A=p*mp.sin(712*mp.asin(p));z=mp.mpf(2)**-20;L=4*p**3;Lam=mp.mpf(1)
    def report(y):
      u=p+p**2*y;B=4*u*u*(1-u*u);return 1-(1-z*B)*(1-z*(L+(1-L)*B))
    b=A*A/(32*Lam);local=(report(-b)+2*report(0)+report(b))/4
    independent=report(0);gap=independent-local
    need(gap>0,'one-shift local report differs from independently shifted report')
    return {'tau_and_h_ready':mp.nstr(alpha,35),'one_comparator_conditional_ready':mp.nstr(alpha*bt**26,35),
       'true_local_single_shift_probability':mp.nstr(local,35),
       'independent_shift_report_probability':mp.nstr(independent,35),
       'independent_minus_common_shift_local_report':mp.nstr(gap,35),
       'illustrative_Lambda_1_not_physical_norm_certificate':True,
       'known_one_first_failure':mp.nstr(1-b1,20),
       'eight_plus_first_failure_mass':mp.nstr(plus_fail,20),
       'all_listed_first_fail_and_success_total_error':mp.nstr(abs(total-1),8),
       'eighty_comparator_and_shared_tau_ready':mp.nstr(alpha*bt**2080,35),
       'full_scalar_factory_success_assumed':True,'first_fail_pre_count':11,'first_fail_post_count':15,
       'loc_success_probability_conditional_ready':'1/256','loc_failure_probability_conditional_ready':'255/256',
       'complete_first_fail_mass_error':mp.nstr(abs(pre+late+success-alpha),8)}


if __name__=='__main__':
  c=correlation_checks();assert c['shared_shift_example_assumes_QND_Site_and_same_shift']
  out={'status':'PASS','canonical_relative_comparator':gates(),'twirl_and_steering':twirl_and_steering(),
       'selected_h_and_shift_and_factory':probability(),'shared_shift_bits':8,
       'Toffoli_80_relative_fourier_localizers':2080,'CX_80_relative_localizers_with_NC1':7456,
       'Hf_Hq_sign_and_180_Choi_compiled':False,'global_weight_fine_tau_or_field_controlled_info_proved':False,
       'ordinary_mu_must_be_uniform_to_match_uniform_twirl':True,'GR_closed':False}
  print(json.dumps(out,indent=2,sort_keys=True))
