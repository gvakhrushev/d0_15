#!/usr/bin/env python3
"""Interval proof that mean-report -> Book feedback does not inherit the
certified nonflat full42 CQ root, despite the null-section source bridge.
Uses the same rational collar, root cube and outward interval engine.
"""
import json
from pathlib import Path
from mpmath import mp, iv
import certified_newton as cert
own=cert.own
ROOT=Path(__file__).resolve().parent
iv.dps=90

def supc(x):
    return max(abs(mp.mpf(x.real.a)),abs(mp.mpf(x.real.b))) + max(abs(mp.mpf(x.imag.a)),abs(mp.mpf(x.imag.b)))
def abslo(x):
    a,b=mp.mpf(x.a),mp.mpf(x.b)
    return a if a>0 else (-b if b<0 else mp.mpf(0))
def report(z,h,base):
    nodes=own.fields(z,h,base); out=[]; tau=iv.mpf('0.05')
    for j in range(2):
        e=nodes[j]['e']; vol=iv.mpf(0)
        for r,s in own.PAIRS:
            Uj=nodes[j]['U'];Un=nodes[j+1]['U']
            fac=[(j,r,False,Uj[r]),(j+1 if r==0 else j,s,False,Un[s] if r==0 else Uj[s]),(j,r,True,own.v_inv(Uj[r])),(j,s,True,own.v_inv(Uj[s]))]
            A,B,invA,invB=[x[3] for x in fac]
            prod=[own.I,A,A*B,A*B*invA,A*B*invA*invB]
            Pm=prod[-1];Pinv=own.v_inv(Pm);R=(Pm-Pinv)/2
            u,v=[k for k in range(4) if k not in (r,s)]
            beta=own.wedge(e[:,u],e[:,v]);row=iv.matrix(1,6)
            for k in range(6): row[0,k]=beta[k]*own.G2[k]
            vol+=(own.SGNS[r,s]*row*own.STAR*own.vec_b(R))[0]/h**2
        g=e.T*own.ETA*e;gi=g**-1;q=iv.mpf(0)
        for a in range(2):
            vrow=nodes[j]['v'][a,:];q+=(vrow*gi*vrow.T)[0]
        x=-tau*vol;y=tau*q;E=own.P**2*(1+x);ell=4*E*(1-E);b=own.P-own.P**2*y;B=4*b*b*(1-b*b);A=ell+(1-ell)*B
        rr=own.Z*(A+B)-own.Z**2*A*B;out.append(rr)
    return out

def main():
    certdata=json.loads((ROOT/'RIGOROUS_EXACT42_CERTIFICATE.json').read_text())
    cc=json.loads((ROOT/'mp_center.json').read_text())['center']
    h,base=own.build();c=[iv.mpf(x) for x in cc]
    R=mp.mpf('1e-7');rho=mp.mpf('1e-30');step=mp.mpf('1e-20')
    box=[iv.mpc([mp.mpf(x)-R,mp.mpf(x)+R],[-R,R]) for x in cc]
    rbox=report(box,h,base)
    M=max(supc(x) for x in rbox)
    if not M < mp.mpf('0.01'): raise AssertionError(('report holomorphic bound',M))
    center=report([iv.mpc(x) for x in c],h,base)
    # Existing certified query-chart intervals separate r0 and r1 on the whole root cube.
    ranges=certdata['record_query_chart']
    r0hi=mp.mpf(ranges[0]['report_real_max']);r1lo=mp.mpf(ranges[1]['report_real_min'])
    gap=r1lo-r0hi
    if gap <= 0: raise AssertionError(('reports not separated',gap))
    # Complex-step derivative of report 0 in coordinate 29, enclosed with outward intervals.
    z=[iv.mpc(x) for x in c];z[29]+=iv.mpc(0,step)
    shifted=report(z,h,base);d0=shifted[0].imag/step
    trunc=M*step**2/(R**3*(1-(step/R)**2))
    d0_lower=abslo(d0)-trunc
    # Cauchy bound on variation of this derivative throughout the root cube.
    dvar=42*2*M/(R**2)*rho
    d0_root_lower=d0_lower-dvar
    if d0_root_lower <= 0: raise AssertionError(('Dr0 not certified nonzero',d0_root_lower))
    # h_phi' is strictly decreasing; r0 != r1. At any CQ stationary point,
    # h'(r0)Dr0+h'(r1)Dr1=0, so D[(r0+r1)/2] != 0 in coord 29.
    # Bound h' ratio from disjoint certified intervals.
    r0lo=mp.mpf(ranges[0]['report_real_min']);r1hi=mp.mpf(ranges[1]['report_real_max'])
    phi=(1+mp.sqrt(5))/2;ell=mp.log(phi)
    hp0lo=mp.log((1-r0hi)/r0hi)/ell; hp0hi=mp.log((1-r0lo)/r0lo)/ell
    hp1lo=mp.log((1-r1hi)/r1hi)/ell; hp1hi=mp.log((1-r1lo)/r1lo)/ell
    # Ratio h'(r0)/h'(r1)>1 because r0<r1 and h' strictly decreases.
    ratio_gap=hp0lo/hp1hi-1
    if ratio_gap<=0: raise AssertionError(('h-prime ratio not separated',ratio_gap))
    mean_grad_lower=mp.mpf('0.5')*ratio_gap*d0_root_lower
    # Both H and Golden fixed-comparator derivatives are strictly positive at this tiny mean report.
    rbar_upper=(r0hi+r1hi)/2;zbook=mp.mpf(1)/2**20;p=(mp.sqrt(5)-1)/2
    jH_lower=2*zbook*(1-rbar_upper)/(1-zbook*(2*rbar_upper-rbar_upper**2))
    jG_lower=4*p*zbook*(1-2*p*rbar_upper)/(1-zbook*4*p*rbar_upper*(1-p*rbar_upper))
    if jH_lower<=0 or jG_lower<=0: raise AssertionError('Book feedback derivative sign')
    result={'status':'PASS_INTERVAL_OFF_NULL_REPORT_BRIDGE_OBSTRUCTION',
      'h':'1/4','root_cube_radius':'1e-30','complex_polydisc_radius':'1e-7',
      'report_complex_sup_bound':mp.nstr(M,18),'report_interval_gap_lower':mp.nstr(gap,18),
      'report0_D_coordinate29_interval':[str(d0.a),str(d0.b)],
      'report0_D_abs_lower_at_root':mp.nstr(d0_root_lower,18),
      'hprime_ratio_minus_one_lower':mp.nstr(ratio_gap,18),
      'mean_report_D_abs_lower_at_root':mp.nstr(mean_grad_lower,18),
      'H_comparator_Jprime_lower':mp.nstr(jH_lower,18),
      'Golden_comparator_Jprime_lower':mp.nstr(jG_lower,18),
      'conclusion':'At the exact nonflat CQ stationary root, the full CQ source is zero, but the single mean-report source is nonzero; hence a scalar mean-report Book feedback does not transfer this off-null root. This does not refute a multi-channel or full physical Book03 construction.',
      'scope':{'exact_root_used_from_interval_certificate':True,'book03_compulsory_action_selected':False,'GR_closed':False}}
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__': main()
