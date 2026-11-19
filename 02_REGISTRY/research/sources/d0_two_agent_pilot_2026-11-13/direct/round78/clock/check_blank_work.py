"""Three consecutive real blank outcomes, with a conditional and a realized payment."""
import json
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode=True
DIRECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DIRECT/"round75/work"))
import check_pointer_weyl as source

I,O=source.I,source.O


def jet_ratio(x,dx,y,dy):
    q=x/y
    return q,(dx-q*dy)/y


def reveal_range(leaves,local_leaves,target,target_a):
    # All 127s below refer to one seven-bit label, not to paths on independent data.
    def prefixes(rates):
        return [(sum(q for y,q,_ in rates if not y & mask),
                 sum(dq for y,_,dq in rates if not y & mask)) for mask in range(128)]
    p2,p3=map(prefixes,leaves[1:])
    a2,a3=map(prefixes,local_leaves)
    out={}
    separate=[]
    prev=0
    for i in range(7):
        mask=prev|(1<<i)
        dv=jet_ratio(*p2[mask],*p2[prev])[1]-jet_ratio(*p3[mask],*p3[prev])[1]
        da=jet_ratio(*a2[mask],*a2[prev])[1]-jet_ratio(*a3[mask],*a3[prev])[1]
        separate.append((dv,da))
        prev=mask
    # Individual field-independent prices per named bit are a wider class
    # than nonnegative mixtures of complete, equally calibrated schedules.
    solutions=[]
    for i,(di,ai) in enumerate(separate):
        for j,(dj,aj) in enumerate(separate[:i]):
            delta=di*aj-dj*ai
            if not delta.contains(0):
                wi=(target*aj-dj*target_a)/delta
                wj=(di*target_a-target*ai)/delta
                if wi.lo>0 and wj.lo>0:
                    solutions.append((max(float(wi.hi),float(wj.hi)),j,O.bounds(wj),i,O.bounds(wi)))
    out["fit_with_bit_specific_scales"]=min(solutions) if solutions else None
    for singleton in (True,False):
        least,most={0:(0.,[])},{0:(0.,[])}
        det_intervals={0:(np.array([0.]),np.array([0.]))}
        for mask in range(1,128):
            lo,hi=[],[]
            dlo,dhi=[],[]
            prev=(mask-1)&mask
            while True:
                new=mask^prev
                if not singleton or not (new & (new-1)):
                    _,second=jet_ratio(*p2[mask],*p2[prev])
                    _,third=jet_ratio(*p3[mask],*p3[prev])
                    edge=second-third
                    _,second_a=jet_ratio(*a2[mask],*a2[prev])
                    _,third_a=jet_ratio(*a3[mask],*a3[prev])
                    determinant=edge*target_a-(second_a-third_a)*target
                    dl,dh=det_intervals[prev]
                    dlo.append(np.nextafter(dl+determinant.lo,-np.inf))
                    dhi.append(np.nextafter(dh+determinant.hi,np.inf))
                    lo.append((float((I(least[prev][0])+edge).lo),least[prev][1]+[new]))
                    hi.append((float((I(most[prev][0])+edge).hi),most[prev][1]+[new]))
                if not prev:
                    break
                prev=(prev-1)&mask
            least[mask],most[mask]=min(lo),max(hi)
            det_intervals[mask]=(np.concatenate(dlo),np.concatenate(dhi))
        dl,dh=det_intervals[127]
        separated=np.maximum(dl,-dh)
        out["7_separate" if singleton else "all_ordered_partitions"]={
            "outer_range":[least[127][0],most[127][0]],
            "orders":len(dl), "positive_det":int(np.sum(dl>0)),
            "negative_det":int(np.sum(dh<0)), "min_separation":float(np.min(separated)),
            "unresolved_orders":int(np.sum(separated<=0)),
            "extreme_chains":[least[127][1],most[127][1]]}
    return out


def certificate():
    p,state,w,dw,fw,bw,u,du,_=source.site_vector()
    zero=I(np.zeros_like(state.lo))
    mask=np.zeros(256)
    mask[source.car.site_index((1,3,2,2))]=-1.
    wa=w*I(mask)
    def a(v,weights=w):
        return source.dirac(v,weights,fw,bw)
    dstate,dastate=zero,zero
    history=[(I(1.),I(0.),I(0.))]
    leaves=[]
    local_leaves=[]
    def fine_rates(state,dstate,u,du,dw,prior,prior_dot):
        rates=[]
        for coefficient in range(2):
            values,ders=source.actions(coefficient,w,dw,fw,bw,u,du)
            for j,(v,dv) in enumerate(zip(values,ders)):
                blank=(j==0 and coefficient==0)
                for port in ((0,1) if blank else (1,)):
                    f=-2*(p*p if port==0 else p*p.sqrt())
                    z=v*f+state if blank and port==0 else v*f
                    dz=dv*f+dstate if blank and port==0 else dv*f
                    q,dq=jet_ratio(O.reduce_sum(z.square()),2*O.reduce_sum(z*dz),
                                   prior,prior_dot)
                    address=8*j+2*coefficient+port
                    rates.append((address,q,dq))
                    if not blank:
                        rates.append((address-1,p*q,p*dq))
            del values,ders
        O.require(len(rates)==64 and sum(q for _,q,_ in rates).contains(1.)
                  and sum(dq for _,_,dq in rates).contains(0.),"all active actual labels")
        return rates
    for i in range(3):
        # Prior complete blank word has one Kraus map B^i. Keep the
        # unnormalised old state; all fine rows will share its actual trace.
        if i:
            u=a(state)
            du=a(dstate)+a(state,dw)
        dua=a(dastate)+a(state,wa)
        next_state=state-2*p*p*a(u)
        next_dstate=dstate-2*p*p*(a(du)+a(u,dw))
        next_dastate=dastate-2*p*p*(a(dua)+a(u,wa))
        prior,prior_dot,prior_a=history[-1]
        rates=fine_rates(state,dstate,u,du,dw,prior,prior_dot)
        if i:
            local_leaves.append(fine_rates(state,dastate,u,dua,wa,prior,prior_a))
        leaves.append(rates)
        history.append((O.reduce_sum(next_state.square()),2*O.reduce_sum(next_state*next_dstate),
                        2*O.reduce_sum(next_state*next_dastate)))
        state,dstate,dastate=next_state,next_dstate,next_dastate
    metrics=[]
    for i,(now,last,rates) in enumerate(zip(history[1:], history[:-1],leaves),1):
        s,ds=jet_ratio(now[0],now[1],last[0],last[1])
        _,dsa=jet_ratio(now[0],now[2],last[0],last[2])
        s0,ds0=next((q,dq) for y,q,dq in rates if y==0)
        O.require((s-s0).contains(0) and (ds-ds0).contains(0) and s.lo>.99
                  and all(q.hi<.25 for y,q,dq in rates if y),"true blank dominates full128")
        c=I(1.)-s
        root3=I(3.).sqrt()
        full=s.sqrt()+root3*c.sqrt()
        full_prime=(I(1.)/s.sqrt()-root3/c.sqrt())/2
        metric={"s":s,"Ds":ds,"partial_A_s":dsa,
                "paid_record":(I(2.)-s,-ds),"paid_coherent":(full,full_prime*ds),
                "mean_record_binary":(1+2*s*c,2*(I(1.)-2*s)*ds),
                "mean_record_full128":(I(2.)-sum(q.square() for _,q,_ in rates),
                                       -2*sum(q*dq for _,q,dq in rates)),
                "mean_coherent_full128":(s*full+2*c,(full+s*full_prime-2)*ds)}
        # The rare complementary coarse branch and every actual nonblank label
        # are in the same constant-distance regime of the full two-tick algebra.
        metrics.append(metric)
    rates2,rates3=metrics[1],metrics[2]
    det=rates2["Ds"]*rates3["partial_A_s"]-rates3["Ds"]*rates2["partial_A_s"]
    logphi=-O.logarithm(p)
    target=-(rates3["Ds"]/rates3["s"]-rates2["Ds"]/rates2["s"])/logphi
    target_a=-(rates3["partial_A_s"]/rates3["s"]-rates2["partial_A_s"]/rates2["s"])/logphi
    O.require(target.lo>-4.14503e-6 and target.hi<-4.14502e-6,"primary three-length target")
    report={"true_success_probabilities_and_derivatives":[
            [O.bounds(m[k]) for k in ("s","Ds","partial_A_s")] for m in metrics],
            "det_ds2_ds3_in_d_A_basis":O.bounds(det),"economic_target":O.bounds(target),
            "registered_confirmations_grouping_original_bits":reveal_range(leaves,local_leaves,target,target_a)}
    for name in ("paid_record","paid_coherent","mean_record_binary","mean_record_full128",
                 "mean_coherent_full128"):
        src=rates3[name][1]-rates2[name][1]
        report[name]={"single_round_conditional":[[O.bounds(v) for v in m[name]] for m in metrics],
                      "three_lengths_D":O.bounds(src),"D_at_sqrt22":O.bounds(I(22.).sqrt()*src),
                      "required_scale_on_d":O.bounds(target/src)}
    groups=report["registered_confirmations_grouping_original_bits"]
    O.require(det.lo> -3.22623e-11 and det.hi< -3.22622e-11,
              "independent physical conditional probabilities")
    for key,count in (("7_separate",5040),("all_ordered_partitions",47293)):
        row=groups[key]
        O.require(row["orders"]==count==row["negative_det"] and row["min_separation"]>4.0976e-17
                  and row["outer_range"][0]>-1.992255e-6 and row["outer_range"][1]<-1.989538e-6,
                  "all complete registered schedules in one open half-plane")
    return report


if __name__=="__main__":
    print(json.dumps(certificate(),indent=2,sort_keys=True))
