"""Failure-source budget for the m=16 native union NC1 carrier.

Cap arithmetic follows check_native_union_nc1_caps.py with delta**4.
CQ entropy/score identities are checked on a concrete isometric old-input
model and do not identify the actual Book03 stagewise tariff or lift.
"""
import json
import mpmath as mp

mp.mp.dps=160
one=mp.mpf(1);p=(mp.sqrt(5)-1)/2;ell=mp.log(1/p)

def cap(fn,budget):
    n=0
    while fn(n)>budget:n+=1
    return n

def h(x):
    if not x or x==1:return mp.mpf(0)
    return -x*mp.log(x)-(1-x)*mp.log(1-x)

def build(n):
    m=16;d=p**(n+1);Mpre=m*n+m-1;Mpost=m*(n+2)+m-1;M=Mpre+Mpost
    budget=d**4/3;sigma=16*p**9
    L1=cap(lambda k:p**k,budget)
    L2=cap(lambda k:6*M*p**(6*k),budget)
    L3=cap(lambda k:M*(1-sigma)**k,budget)
    b1=1-p**L1;b2=1-p**(6*L2);b3=1-(1-sigma)**L3;beta=b2**6*b3
    eps=1-b1*beta**M;upper=p**L1+M*(6*p**(6*L2)+(1-sigma)**L3)
    assert eps<=upper and upper<=d**4
    q=1-(1-d)**m
    # Coarse first-failure categories verify masses only. Full CQ isometry
    # applies to all actually retained fine Kraus outcomes, not automatically
    # to these coarse labels.
    branches=[('h',p**L1,mp.mpf(1))]
    for j in range(Mpre):branches.append(('pre',b1*beta**j*(1-beta),mp.mpf(j+1)/(M+1)))
    for r,qr in ((0,1-q),(1,q)):
        for j in range(Mpost):
            branches.append(('post'+str(r),b1*beta**Mpre*qr*beta**j*(1-beta),mp.mpf(j+1)/(M+1)))
        branches.append(('success'+str(r),b1*beta**M*qr,mp.mpf(0)))
    assert abs(sum(w for _,w,_ in branches)-1)<mp.mpf('1e-120')
    F=[(k,w,a) for k,w,a in branches if not k.startswith('success')]
    assert abs(sum(w for _,w,_ in F)-eps)<mp.mpf('1e-120')
    # Conditional old rho_x=diag(x,1-x) is carried isometrically for each
    # model branch; c_{f,0}=-a_f*x, c_{f,1}=+a_f*x.  Explicit eigenvalue
    # entropy of a CQ direct sum verifies S(CQ)=H(p_f)+S(rho_x).
    x=mp.mpf('0.37'); Hf=-sum(w*mp.log(w) for _,w,_ in branches)
    eigenentropy=-sum(w*x*mp.log(w*x)+w*(1-x)*mp.log(w*(1-x)) for _,w,_ in branches)
    assert abs(eigenentropy-(Hf+h(x)))<mp.mpf('1e-120')
    dx=h(x) # prevent using entropy derivative as entropy itself
    dx=mp.log((1-x)/x)
    dSfull=sum(-w*(mp.log(w*x)+1)+w*(mp.log(w*(1-x))+1) for _,w,_ in branches)
    assert abs(dSfull-dx)<mp.mpf('1e-120')
    sf0=sum(w*(-a-dx/ell) for _,w,a in F)
    sf1=sum(w*(a-dx/ell) for _,w,a in F)
    assert abs((sf1-sf0)-2*sum(w*a for _,w,a in F))<mp.mpf('1e-120')
    assert abs(sf1-sf0)<=2*eps
    # Uniform L2 cap: the Cauchy-Schwarz factor sqrt(epsilon)/delta <= delta.
    assert mp.sqrt(eps)/d<=d
    return {'N':n,'delta':mp.nstr(d,20),'M_pre':Mpre,'M_post':Mpost,'M':M,
      'L1':L1,'L2':L2,'L3':L3,'epsilon':mp.nstr(eps,20),
      'delta_fourth':mp.nstr(d**4,20),'upper':mp.nstr(upper,20),
      'success_gamma':mp.nstr(1-eps,20),
      'sqrt_epsilon_over_delta':mp.nstr(mp.sqrt(eps)/d,20),
      'pointwise_source_error_over_delta_bound':mp.nstr(2*eps/d,20),
      'model_field_tangent_entropy_derivative':mp.nstr(dSfull,20),
      'model_failure_source_difference_over_delta':mp.nstr((sf1-sf0)/d,20)}

def main():
    results=[build(n) for n in (2,8,20,40)]
    print(json.dumps({'status':'PASS','cap_exponent':4,
      'checks':'numerical caps and complete coarse first-failure masses; exact CQ identities on explicit isometric branch model',
      'isometry_and_scalar_effect_of_actual_fine_transcripts':'assumed from cited owners; not re-simulated',
      'fixed_input_field_score_for_such_scalar_transcripts':0,
      'entropy_derivative_fixed_pure_ancillas':'D S(old), for full fine registered carrier',
      'all_path_Book03_tariff_and_clock_identified':False,
      'physical_right_lift_constructed':False,'GR_closed':False,'examples':results},indent=2))

if __name__=='__main__':main()
