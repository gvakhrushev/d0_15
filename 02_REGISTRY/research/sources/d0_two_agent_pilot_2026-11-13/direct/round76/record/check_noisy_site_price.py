"""Outward bounds for the actual eight-CX SITE price on the primary two-site ray."""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DIRECT/"round75"/"work"))
import check_pointer_weyl as owner

I, O = owner.I, owner.O


def sum_at_site(x):
    # Exact 2-adic bisection pattern; the native outward primitive adds
    # one error enclosure per actual pair, including the 128 RIGHT columns.
    a = I(x.lo.reshape(256,-1),x.hi.reshape(256,-1))
    while a.lo.shape[1] > 1:
        a = a[:,::2]+a[:,1::2]
    return a[:,0]


def noise(values,p):
    a = values
    for bit in range(8):
        other = np.arange(256)^(1<<bit)
        a = p*a+p.square()*a[other]
    return a


LN2 = O.logarithm(I(2.))


def binary_log_endpoint(x):
    # ln(x)=k ln(2)+2 atanh((m-1)/(m+1)) for exact dyadic
    # range reduction x=2^k*m, 1<=m<2. All terms and the tail are enclosed.
    O.require(np.all(x>0),"positive output for logarithm")
    m,k = np.frexp(x)
    m = I(2*m)
    t = (m-1)/(m+1)
    power = t
    total = t
    t2 = t.square()
    for j in range(1,18):
        power = power*t2
        total = total+power*Q(1,2*j+1)
    eps = I.rational(2*Q(1,3)**37/(37*(1-Q(1,9))))
    return 2*total+I(k-1)*LN2+I(0.,float(eps.hi))


def ln(x):
    return I(binary_log_endpoint(x.lo).lo,binary_log_endpoint(x.hi).hi)


def absolute(x):
    lo = np.maximum(0.,np.maximum(x.lo,-x.hi))
    hi = np.maximum(np.abs(x.lo),np.abs(x.hi))
    return I(lo,hi)


def confirmation(raw,draw):
    rec,coh = I(0.),I(0.)
    kappa = I(3.).sqrt()-1
    # Real order of reading is low bit to high bit. Marginalize the
    # highest current bit first to reconstruct all those older prefixes.
    for j in reversed(range(8)):
        half = 1<<j
        a,b = raw[:half],raw[half:]
        da,db = draw[:half],draw[half:]
        s = a+b
        p0,p1 = a/s,b/s
        rec = rec+O.reduce_sum((1+2*p1.square())*da+(1+2*p0.square())*db)
        u = (p0*p1).sqrt()
        w = (1+2*u).sqrt()
        val = w*(1+kappa*u)
        slope = (p0-p1)/(2*u)*((1+kappa*u)/w+kappa*w)
        coh = coh+O.reduce_sum((val-p1*slope)*da+(val+p0*slope)*db)
        raw,draw = s,da+db
    return rec,coh


def main():
    p,Zbase,w,dw,fw,bw,u,du,_ = owner.site_vector()
    logphi = -O.logarithm(p)
    pop = I(np.array([bin(i).count("1") for i in range(256)],dtype=float))
    old_ent,out_ent,new_length,site_weight,htv,trace_bound = (I(0.) for _ in range(6))
    total, derivative = I(0.),I(0.)
    rec,coh = I(0.),I(0.)
    for cf in range(2):
        vals,ders = owner.actions(cf,w,dw,fw,bw,u,du)
        for j,(n,dn) in enumerate(zip(vals,ders)):
            blank = j==cf==0
            for port in ((0,1) if blank else (1,)):
                scale = -2*(p*p if port==0 else p*p.sqrt())
                z = n*scale+Zbase if blank and port==0 else n*scale
                dz = dn*scale
                sites = sum_at_site(z.square())
                dsites = 2*sum_at_site(z*dz)
                norms2 = sum_at_site(dz.square())
                scale_mass = I(1.) if blank else 1+p
                norm_product = sites*norms2
                norm_product = I(np.maximum(0.,norm_product.lo),norm_product.hi)
                trace_bound = trace_bound+scale_mass*O.reduce_sum(norm_product.sqrt())
                raw = noise(sites,p)
                draw = noise(dsites,p)
                r,c = confirmation(raw,draw)
                rec,coh = rec+scale_mass*r,coh+scale_mass*c
                for multiple in ((I(1.),) if blank else (I(1.),p)):
                    qx,dqx = sites*multiple,dsites*multiple
                    qm,dqm = raw*multiple,draw*multiple
                    qy,dy = O.reduce_sum(qx),O.reduce_sum(dqx)
                    total = total+O.reduce_sum(qm)
                    derivative = derivative+O.reduce_sum(dqm)
                    old_ent = old_ent-dy*O.logarithm(qy)
                    out_ent = out_ent-O.reduce_sum(dqm*ln(qm))
                    new_length = new_length+O.reduce_sum((8+pop)*dqm)
                    site_weight = site_weight+O.reduce_sum(pop*dqx)
                    htv = htv+O.reduce_sum(absolute(dqm))*Q(1,2)
    O.require(total.contains(1) and derivative.contains(0),"full record normalization, all raw bits")
    hm,hy = out_ent/logphi,old_ent/logphi
    dh = hm-hy
    length = site_weight*p*p*p
    O.require(max(length.lo,new_length.lo)<min(length.hi,new_length.hi),"actual bit price agreement")
    right = trace_bound*8
    O.require(right.hi<.013453,"conditional RIGHT entropy differential")
    rec_bound = 16*p*p*p*htv
    O.require(absolute(rec).hi < rec_bound.hi,"total variation bound for marginal confirmation")
    old_right_upper = I.rational(Q(-610100449,10**13))
    geometric = I.rational(Q(2204,100000))
    rows = {}
    for label,k in (("unit",I(1.)),("spectral",I(22.).sqrt())):
        for algebra,local_work in (("reported",rec),("coherent",coh)):
            inc = length-dh+k*local_work
            O.require(inc.lo>0 if label=="unit" else inc.hi<0, "increment reverses sign")
            full_lo = geometric+length-hm+k*local_work
            right_lo = geometric+length-old_right_upper-right+k*local_work
            O.require(full_lo.lo>.0217835 and right_lo.lo>.0086192,"both residuals across all depths")
            all_old_codes = I.rational(Q(-4344153,10**9))
            full_code_lo, right_code_lo = full_lo+all_old_codes,right_lo+all_old_codes
            O.require(full_code_lo.lo>.0174393 and right_code_lo.lo>.0042750,
                      "every complete 128-leaf old F/R code")
            rows[label+"_"+algebra] = {"new_relative_to_old":O.bounds(inc),
                                       "full_Y_DATA_RIGHT_lower":float(full_lo.lo),
                                       "Y_RIGHT_lower":float(right_lo.lo),
                                       "all_old_codes_full_lower":float(full_code_lo.lo),
                                       "all_old_codes_Y_RIGHT_lower":float(right_code_lo.lo)}
    result = {"D_native_new_length":O.bounds(length), "D_length_direct":O.bounds(new_length),
              "D_H_Y":O.bounds(hy),"D_H_YM":O.bounds(hm),"D_H_M_given_Y":O.bounds(dh),
              "D_added_code_minus_added_full_entropy":O.bounds(length-dh),
              "D_port_plus_new_code_minus_full_entropy_YM":O.bounds(length-hm),
              "TV_joint_raw_derivative":O.bounds(htv),"RIGHT_trace_factor":O.bounds(trace_bound),
              "D_local_full_history_record_confirmations":O.bounds(rec),
              "D_local_full_history_pure_coherent_confirmations":O.bounds(coh),
              "abs_record_confirmation_TV_upper":float(rec_bound.hi),
              "calibrated_tests":rows,
              "abs_D_incremental_entropy_if_DATA_hidden_upper":float(right.hi),
              "physical_edge_price_selected":False}
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
