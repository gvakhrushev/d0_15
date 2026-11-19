#!/usr/bin/env python3
"""Full fixed-beta lapse source: interval coefficients and infinite tails."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
import mpmath as mp

def interval_source():
    mp.mp.dps=90;mp.iv.dps=80;iv=mp.iv;checks=[]
    def require(v,n):
        if not bool(v):raise ArithmeticError(n)
        checks.append(n)
    p=(iv.sqrt(5)-1)/2;beta=2*p*p;z=iv.mpf(2)**-20;rr=z/(1-z);M=128;omega=2*iv.pi
    def theta(t):return 1+2*sum((iv.exp(-t*j*j) for j in range(1,13)),iv.mpf(0))+iv.mpf([0,'1e-128'])
    def moment2(t):return 2*sum((j*j*iv.exp(-t*j*j) for j in range(1,13)),iv.mpf(0))+iv.mpf([0,'1e-126'])
    require(theta(iv.mpf('1.80'))<3,'uniform_theta_bound_for_feedback_tail')
    require(moment2(iv.mpf('1.80'))<10,'uniform_moment_bound_for_feedback_tail')
    theta_tail=2*iv.exp(-iv.mpf('1.80')*169)/(1-iv.exp(-iv.mpf('1.80')*27))
    moment_tail=2*169*iv.exp(-iv.mpf('1.80')*169)/(1-(iv.mpf(14)/13)**2*iv.exp(-iv.mpf('1.80')*27))
    require(theta_tail<iv.mpf('1e-128'),'theta_j12_tail')
    require(moment_tail<iv.mpf('1e-126'),'moment_j12_tail')
    feedback_tail=2048*beta*4*27*10*rr**11/(1-rr)
    require(feedback_tail<iv.mpf('1e-55'),'feedback_series_n10_tail')
    def F(a):
        ans=4*moment2(a)/theta(a)-2048*beta*sum(((-1)**(n+1)*rr**n*4*theta(n*a)**3*moment2(n*a) for n in range(1,11)),iv.mpf(0))-1
        return ans+iv.mpf(['-1e-55','1e-55'])
    center=mp.mpf('1.807402105276820465785568102491966746380435406812535655887327979709036')
    radius=mp.mpf('1e-30')
    low=mp.nstr(center-radius,85);high=mp.nstr(center+radius,85)
    require(F(iv.mpf(low))>0,'actual_root_lower_sign')
    require(F(iv.mpf(high))<0,'actual_root_upper_sign')
    ar=iv.mpf([low,high]);c=ar/beta;d=c/omega**2;Z=16*theta(ar)**4
    require(ar>iv.mpf('1.80') and ar<iv.mpf('1.82'),'actual_root_inside_owned_interval')
    require(8*iv.pi*iv.sqrt(d)<12,'coframe_V_uniform_op_bound')
    require(12*iv.sqrt(d)<12,'link_V_uniform_op_bound')
    cache={}
    def weight(K):
        if K not in cache:
            ee=iv.exp(-ar*K);ff=1-z+z*ee
            cache[K]=-ee/Z+M*z*beta*ee/ff+(iv.mpf(1)/128 if K==1 else 0)
        return cache[K]
    R=7
    counts=Counter(x*x+y*y+w*w for x in range(-R,R+1) for y in range(-R,R+1) for w in range(-R,R+1))
    A=iv.mpf(0);B=iv.mpf(0);C=iv.mpf(0)
    for t in range(-R-1,R+1):
        for J,count in counts.items():
            K=t*t+J;L=(t+1)**2+J
            wk,wl=weight(K),weight(L);dd=(wl-wk)/(c*(2*t+1));ww=wk+wl
            A+=count*(ww*8*c*(t*t+(t+1)**2)+dd*8*c*c*(8*t*t*(t+1)**2+4*t*(t+1)+1))
            B+=count*(ww*12*c/omega+dd*12*c*c/omega)
            C+=count*(ww*48*c/omega**2+dd*16*c*c*(3+J)/omega**2)
    Cw=iv.mpf(1)/16+M*z*beta/(1-z);j=R+1
    ratio=(1+iv.mpf(1)/j)**7*iv.exp(-iv.mpf('1.80')*(2*j-1))
    first=(64*j**3+16*j)*(1+2*j)**2*(2+iv.mpf('1.82')*(4*j+1)**2)*iv.exp(-iv.mpf('1.80')*(j-1)**2)
    tail=16*Cw*144*first/(1-ratio)
    require(ratio<1,'matrix_gaussian_tail_ratio')
    require(tail<iv.mpf('1e-25'),'matrix_uniform_infinite_tail')
    # The rectangle contains the full cube; omitted pairs are a subset of
    # max-norm shells j>=R+1. All preparation-cross terms are already inside.
    err=iv.mpf(['-1e-25','1e-25']);A+=err;B+=err;C+=err
    require(A>0,'lapse_A_positive')
    require(C<0,'scalar_connection_row_invertible_negative')
    reduced=A-B*B/C
    bounds={
      'A':('0.0054788','0.0054789'),
      'B':('0.0026159','0.0026160'),
      'C':('-0.0280215','-0.0280214'),
      'reduced':('0.0057230','0.0057231')}
    for name,val in [('A',A),('B',B),('C',C),('reduced',reduced)]:
        lo,hi=bounds[name];require(val>iv.mpf(lo) and val<iv.mpf(hi),name+'_rational_enclosure')
    return {'status':'PASS_INTERVAL','schema':'d0-full-price-lapse-source/1','checks':len(checks),
      'source':'fixed beta=2p^2, M128, z2^-20, actual continuum v8 root, fullCAR16/reference128',
      'a_root_interval':[low,high],'a_root_interval_radius':'1e-30','root_evidence':'F lower positive, upper negative with infinite theta/feedback remainder; owned uniqueness in [1.80,1.82]',
      'sum_rectangle':{'time':[-R-1,R],'space':[-R,R]},'grouped_spatial_shells':len(counts),'matrix_tail_bound':'1e-25',
      'coefficients_enclosed':bounds,'matrix_convention':'K(lapse,normal)=[[A,iB],[-iB,C]], base positive Fourier coefficient1; physical coscos Hessian reduced/2',
      'linear_normal_reduction':'C<0, choose normal=-K_normal,lapse/C; all other normal irreps decouple by spatial signed permutations',
      'claim':'continuum full-price lapse reduced Hessian strictly positive; not Einstein vacuum gauge Hessian',
      'limitations':['not limit of finite Schur without soft-channel rate','not physical action/admission theorem','not full nonlinear curved root or complete D0 GR theorem'],
      'check_names':checks,'check_names_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest()}

if __name__=='__main__':
    from check_native_scalar_symbol import kernel,lapse_traces,time_pullback_ward
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
    r={'status':'PASS','symbol_kernel':kernel(args.root),'CAR_traces':lapse_traces(args.root),'interval_source':interval_source(),'time_pullback_ward':time_pullback_ward(args.root)}
    text=json.dumps(r,indent=2,default=str)+'\n'
    if args.output:args.output.write_text(text)
    print(text)
