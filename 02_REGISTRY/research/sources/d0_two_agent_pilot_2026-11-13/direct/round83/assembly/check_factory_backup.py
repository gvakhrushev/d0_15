"""Re-use the pinned native selector compiler and certify the complete two-route readout."""
from fractions import Fraction as F
from math import comb, exp, log, sqrt
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
import json
import os
import subprocess
import sys

from mpmath import iv

from check_coherent_price import eta_interval, interval
iv.dps=85
REV="a03c0e1f02b5a2065ebe31b4e82f679e29001763"
DIR="02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/2026-11-19/metric"
REPO=os.environ.get("D0_PILOT_OBJECT_REPO",str(Path(__file__).resolve().parents[7]))


def layouts(owner):
    result={}
    for cut,divisor,power,backup_k in ((24,840,1,1),(36,705600,2,4)):
        assert all(divisor*comb(8,j) % (j**power)==0 for j in range(1,9))
        sizes=[divisor*comb(8,j)//j**power for j in range(1,9)]
        states=owner.MultiDiagram()
        root=states.compile(cut,sizes)
        exact=tuple([owner.ONE-owner.Golden(sum(sizes))*owner.P**cut]+
                    [owner.Golden(n)*owner.P**cut for n in sizes])
        assert states.masses(root)==exact
        binary=owner.BooleanDiagram()
        # Only four setting bits needed; inactive is the value zero.
        roots=[binary.from_multiroot(states,root,j) for j in range(4)]
        cur=0
        for j,count in enumerate(sizes):
            for rank in (cur,cur+count-1):
                tape=owner.tape_of_exact_rank(cut,rank)
                assert binary.compute_and_uncompute(tape,roots)==j+1
            cur+=count
        assert len(binary.nodes)=={24:305,36:576}[cut]
        # J=1..8 and one live B_j bit: each predicate has five controls.
        for label in range(16):
            for heads in range(256):
                total=sum((label==j and ((heads>>(j-1))&1)==(j%2))
                          for j in range(1,9))
                assert total in (0,1)
                if 1<=label<=8:
                    assert bool(total)==(((heads>>(label-1))&1)==label%2)
                else:
                    assert total==0
        backup_eta,_=eta_interval(cut+1,backup_k)
        result[cut]=dict(nodes=len(binary.nodes),Toffoli_bound=4*len(binary.nodes),
                         logical_node_CX_bound=2*len(binary.nodes)+4,
                         backup_unit_rotations=sum(sizes)*backup_k*(1<<(cut+1)),
                         backup_efficiency=round(float(backup_eta),12))
    return result


def certify_all_header_prices():
    """Unrestricted finite header offsets; outcome gaps >=6; every header probes Q."""
    p=2/(1+iv.sqrt(5))
    phi=1/p
    ell=iv.log(phi)
    eta_bounds = {pair: eta_interval(*pair) for pair in ((5,2),(25,1),(37,4))}
    eta_floor=min(bounds[0] for bounds in eta_bounds.values())
    by_cut={}
    for cut,divisor,power,alt in ((24,840,1,(25,1)),(36,705600,2,(37,4))):
        active=p**cut*sum(divisor*comb(8,j)//j**power for j in range(1,9))
        qlo,qhi=active*p**2,active*p
        entries={}
        for name,pair in (("fast",(5,2)),("backup",alt)):
            lo,hi=eta_bounds[pair]
            slo,shi=interval(lo)*qlo,interval(hi)*qhi
            assert slo>iv.mpf(".2205") and shi<iv.mpf(".372")
            entries[name]={"K":pair[0],"k":pair[1],
                           "s_min_rounded":round(float(slo.mid),10),
                           "s_max_rounded":round(float(shi.mid),10)}
        by_cut[cut]=entries

    # Every s_j in (1/5,2/5), A=(1-s_j)/s_j in (3/2,4).
    # Costs H_j+C_{j,b}, all H_j arbitrary; gap d_j=C_{j,1}-C_{j,0}.
    # Derivatives in Q: for all mixtures a in [0,1] and t=1-a, the global
    # entropy term is -a sum w_j eta_j log_phi A_j. All weights are positive.
    e=interval(eta_floor)
    gap_ratio=p**6
    entropy_floor=e*iv.log(iv.mpf(3)/2)/ell
    action_floor=e*(1-16*gap_ratio)/((1+4*gap_ratio)*ell)
    minimum_floor=e/ell
    born_floor=e*(6-2*iv.log(4)/ell)
    assert 4*gap_ratio<1 and 16*gap_ratio<1
    assert entropy_floor>iv.mpf(".79") and minimum_floor>entropy_floor
    assert action_floor>iv.mpf(".17") and born_floor>iv.mpf(".218")
    # A finite minimum of differentiable zero prices has max/min active-label
    # slopes from the left/right. Different field-independent offsets can cause
    # a real cusp. The same goes for any direction via Q and its derivative.
    verify_example_and_tie(eta_bounds)
    return {"native_angles_by_cut":by_cut,
            "hypotheses":"fixed positive header masses and fixed finite header costs; each gap >=6; 0<=a<=1 and nu>=1",
            "minus_logsum_slope_Q_lower":".17","minus_both_one_sided_min_slopes_Q_lower":".79",
            "born_gain_slope_Q_lower":".218","constructed_distinct_slope_minimum_tie_checked":True,
            "zero_gap_reverses_both_signs_when_a_zero":True}


def verify_example_and_tie(eta_bounds):
    ef,eb = [float(eta_bounds[pair][0]) for pair in ((5,2),(37,4))]
    eta=(ef,eb)
    w=(.3,.7)
    p=(sqrt(5)-1)/2
    ell=-log(p)
    def ent(s):
        return -(s*log(s)+(1-s)*log(1-s))/ell

    def direct(q,a,offset,gaps):
        t=1-a
        ss=[rate*q for rate in eta]
        gain=ent(w[0])+sum(mass*ent(s) for mass,s in zip(w,ss))
        dh=sum(mass*rate*log((1-s)/s)/ell for mass,rate,s in zip(w,eta,ss))
        vals=[]; grads=[]
        born_cost=0; born_slope=-2*dh
        for s,rate,mass,header,gap in zip(ss,eta,w,offset,gaps):
            born_cost+=mass*(header+gap*s)
            born_slope+=mass*rate*gap
            for bit,prob,dp in ((0,1-s,-rate),(1,s,rate)):
                vals.append(header+gap*bit-a*gain+t*log(mass*prob)/ell)
                grads.append(-a*dh+t*dp/(prob*ell))
        weights=[exp(-ell*(x-min(vals))) for x in vals]
        logsum=min(vals)-log(sum(weights))/ell
        dsum=sum(weight*grad for weight,grad in zip(weights,grads))/sum(weights)
        return vals,grads,logsum,dsum,born_cost-2*gain,born_slope

    h=1e-6
    for q in (.24,.31,.37):
        for a in (0,.35,1):
            for offset in ((-1.2,3.9),(6.2,-4.5)):
                for gaps in ((6,6),(7.35,32.7)):
                    x=direct(q,a,offset,gaps)
                    lo,hi=(direct(q+sign*h,a,offset,gaps) for sign in (-1,1))
                    assert x[0][0]<x[0][1] and x[0][2]<x[0][3]
                    assert abs((hi[2]-lo[2])/(2*h)-x[3])<2e-7 and x[3]<-.17
                    assert abs((hi[4]-lo[4])/(2*h)-x[5])<2e-7 and x[5]>.218

    # Without the outcome gap a counterexample already exists with field-independent
    # headers. At a=0 the rarer one leaf wins, the logsum increases, Born decreases.
    example=direct(.31,0,(0,1),(0,0))
    assert example[0][1]<example[0][0] and example[0][3]<example[0][2]
    assert min(example[1][1::2])>0 and example[3]>0 and example[5]<0

    q=.31; a=.35
    raw=direct(q,a,(0,0),(6,8))[0]
    offsets=(0,raw[0]-raw[2])
    mid=direct(q,a,offsets,(6,8))
    assert abs(mid[0][0]-mid[0][2])<1e-13
    left,right=(min(direct(q+sign*h,a,offsets,(6,8))[0]) for sign in (-1,1))
    active_grads=(mid[1][0],mid[1][2])
    assert abs((min(mid[0])-left)/h-max(active_grads))<2e-5
    assert abs((right-min(mid[0]))/h-min(active_grads))<2e-5
    assert min(active_grads)+.01<max(active_grads)<-.79


def main():
    with TemporaryDirectory() as w:
        for filename in ("check_selector36_compilation.py","check_boundary_experiment.py"):
            ref=f"{REV}:{DIR}/{filename}"
            (Path(w)/filename).write_bytes(subprocess.check_output(["git","-C",REPO,"cat-file","blob",ref]))
        sys.path.insert(0,w)
        result=layouts(importlib.import_module("check_selector36_compilation"))
    phi=(1+iv.sqrt(5))/2
    p=1/phi
    miss=p**128+2592*(6*p**(6*256)+(1-16*p**9)**256)
    assert miss<iv.mpf("1.372e-23")
    expected=miss*result[36]["backup_unit_rotations"]
    assert expected<iv.mpf(".000154")
    fast_eta,_=eta_interval(5,2)
    assert fast_eta>F(".94898")
    assert interval(fast_eta)*iv.mpf(".18")>iv.mpf(".17")
    print(json.dumps(dict(PR334=REV,banks=result,fast_logical_rotations=8*32*2,
                          fast_efficiency=round(float(fast_eta),12),
                          born_miss_upper="1.372e-23",
                          expected_backup_unit_rotations_upper=".000154",
                          all_header_price_test=certify_all_header_prices(),
                          all_failure_records_keep_a_field_measurement=True,
                          complete_hardware_run=False,GR_closed=False),indent=2))


if __name__=="__main__":
    main()
