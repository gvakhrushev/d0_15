"""Check the native retained parity/Bell probe and balanced LCU failure effects."""

from collections import defaultdict
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
sys.path.insert(0, str(PILOT / "open/round181"))
from check_fixed_positive_reader import a,cx,nc1,ne,one,p,power,require,with_births
from check_parity_price import action


def inverse_g(known_one,target):
    invert = cx(known_one,target)
    return invert,ne.Gate("G",(target,)),invert


def execute(state,word,width):
    for g in word:
        state=action(state,g,width)
    return state


def bell_film():
    # H=0 is the old known-one wire, T/R=1/2, F=3, tail=4.
    root=with_births({1:one},4)
    prepare=inverse_g(0,3)+(cx(1,3),cx(2,3))+nc1(3,4)
    state=execute(root,prepare,5)
    fail={idx:amp for idx,amp in state.items() if not idx&2}
    ready={idx:amp for idx,amp in state.items() if idx&2}
    ready=execute(ready,(cx(0,2),),5)
    require(ready=={18:a*p,30:a*p},"The two real marked Bell components must agree")
    failure_mass=sum((amp*amp for amp in fail.values()),one*0)
    ready_mass=sum((amp*amp for amp in ready.values()),one*0)
    require(failure_mass==p*p+power(p,4) and ready_mass==2*power(p,3),
            "Actual Bell reported success and failure")
    return {"square_word_on_success":len(prepare)+1,"births_including_probe":4,
            "actual_Bell_NC1":1,"Bell_ready_probability":"2 p^3",
            "Bell_failure_probability":"p^2+p^4"}


def rails():
    # CAR=0..3; live known-one=4; new rails=5,6.
    word=inverse_g(4,5)+inverse_g(4,6)+(cx(4,6),)+tuple(cx(i,5) for i in range(4))+(cx(5,6),)
    for col in range(16):
        odd=bin(col).count("1")%2
        root=(col<<3)|4
        state=with_births({root>>2:one},2)
        actual=execute(state,word,7)
        require(actual=={root|2*odd|(1-odd):one},"Wrong complementary rails on a literal column")
    return {"square_word":len(word),"births":2,"CAR_columns":16,
            "cold_amplitude_of_either_rail":"ap"}


def reduced(state,keep,width):
    groups=defaultdict(dict)
    keep_mask=sum(1<<(width-1-i) for i in keep)
    for idx,amp in state.items():
        groups[idx&~keep_mask][idx&keep_mask]=amp
    matrix=defaultdict(lambda:one*0)
    for group in groups.values():
        for x,y in product(group,repeat=2):
            matrix[x,y]+=group[x]*group[y]
    return {key:value for key,value in matrix.items() if value!=0}


def local_work_control():
    # CAR4, T=4, R=5, rails=6,7, known-one=8. State is scaled by sqrt(2) for Bell.
    def initial(carriers):
        out={}
        for car,coefficient in carriers:
            pi=bin(car).count("1")%2
            addr=(car<<5)+4*pi+2*(1-pi)+1
            out[addr]=coefficient
            out[addr+16+8]=coefficient
        return out
    first=initial(((0,p),(15,a),(1,one),(14,a)))
    other=initial(((0,p),(15,a),(1,one),(11,a)))
    expected=reduced(first,(4,6),9)
    require(reduced(other,(4,6),9)==expected, "Equal parity mass must give the same active state")
    G=ne.Gate("G",(4,))
    A=cx(6,4)
    inverse=inverse_g(8,4)
    # Two parity controls and two genuinely different rotations.
    for word in ((G,A,G,G,A),(G,A,G)+inverse+(A,)):
        for root in (first,other):
            state=root
            original_car=reduced(root,tuple(range(4)),9)
            for gate in word:
                state=action(state,gate,9)
                require(reduced(state,(4,6),9)==expected,
                        "Any gate-local tariff on active probe/parity sees the same density")
            require(reduced(state,tuple(range(4)),9)==original_car,
                    "Return on CAR alone cannot see the geometry after tracing retained rails")
    return {"actual_signed_words_checked":2,"CAR_filler_choices":2,
            "probe_and_first_rail_marginal_exact":True,
            "CAR_return_marginal_independent":True}


def fixed_sign_skeleton():
    # Two independent honest bits s,d label four physical branches.
    # The selected active controls are 0,1; the probe is 2. Bell's
    # reduced state is the equal mixture of probe basis inputs.
    G=ne.Gate("G",(2,))
    A,B=cx(0,2),cx(1,2)
    word=(A,B,G,B,A)
    expected={(i,i):2*one for i in (0,1,4,5)}
    # The second control instead of first has the same joint weight.
    for y in (0,1):
        deck=[]
        for d,s,t in product((0,1),repeat=3):
            alpha,beta=d^s,d^s^y
            idx=4*alpha+2*beta+t
            root={idx:one}
            state=execute(root,word,3)
            reference=action(root,G,3)
            if y:
                # Definition of the inverse as X G X, independently of alpha.
                toggled={idx^1:one}
                reference={i^1:v for i,v in action(toggled,G,3).items()}
            require(state==reference,"Two shares fail fixed signed rotation")
            deck.append(root)
        for g in word:
            deck=[action(x,g,3) for x in deck]
            for rail,weights in ((0,expected),(1,{(i,i):2*one for i in (0,1,2,3)})):
                accum=defaultdict(lambda:one*0)
                for x in deck:
                    for k,v in reduced(x,(rail,2),3).items():
                        accum[k]+=v
                require({k:v for k,v in accum.items() if v!=0}==weights, "A slot may see only one honest share and tracial probe")
    return {"same_five_slot_skeleton_all_columns":True,"individual_share_probe_marginal_exact":True}


def signs():
    iv=mp.iv
    iv.dps=75
    P=(iv.sqrt(5)-1)/2
    th=iv.asin(P) if hasattr(iv,"asin") else iv.atan2(P,iv.sqrt(P))
    t=1160*th-246*iv.pi
    z=iv.mpf(2)**-20
    h0=P**2+P**5*(P**2+P**4)
    alpha=P**9/2
    beta=2*P**2
    x=beta/11
    heat=132/(359*beta)*2*x**16/(factorial(16)*(1-x/17))
    q_examples = [(iv.mpf(1)/256,iv.mpf(1)/64),(P**2*iv.sin(566*th)**2,P**2*iv.sin(3518*th)**2)]
    def secant(q,odd):
        vals=[]
        for s in (-1,1):
            c=q*iv.cos(68*th+s*t)+(1-q)*iv.cos(odd-s*t)
            vals.append(-8*iv.ln(1-z+z*(h0+alpha*c*c)))
        return (vals[1]-vals[0]+iv.mpf([-1,1])*heat)/(2*t)
    def fmt(value):
        return [f"{float(value.a):.12e}",f"{float(value.b):.12e}"]
    out=[]
    for q0,q1 in q_examples:
        pair=[secant(q,-66*th) for q in (q0,q1)]
        require(pair[0]<0 and pair[1]>0,"Wrong guarded A89 H+J orientations")
        values=[sum(secant(q,iv.mpf(val)) for q in (q0,q1)) for val in (".007",".012")]
        require(values[0]*values[1]<0,"No bracket for a common positive calibration")
        out.append({"q":[fmt(q0),fmt(q1)],"coframe_secants":[fmt(v) for v in pair],
                    "precision_bracket":[".007",".012"]})
    q0,q1=q_examples[1]
    masked_alpha=2*P**25
    masked_min=[]
    for q in (q0,q1):
        c_plus=q*iv.cos(68*th+t)+(1-q)*iv.cos(-66*th-t)
        c_minus=q*iv.cos(68*th-t)+(1-q)*iv.cos(-66*th+t)
        delta_c=c_plus*c_plus-c_minus*c_minus
        lower=4*z*masked_alpha*abs(delta_c)/abs(t)
        require(lower>iv.mpf("1e-13") and lower>heat/(2*t),
                "Masked ready cold signal must dominate the true heat tail")
        masked_min.append(fmt(lower))
    require(heat<iv.mpf("1e-31"),"True Hodge-tail bound")
    return {"h_star":"p^2 + p^5 (p^2+p^4)","h_ready_multiplier":"p^9/2",
            "physical_ready_probability":"2 p^5","heat_abs_bound":"< 1e-31",
            "A89_parity_cases":out,
            "masked_cold_ready_multiplier":"2 p^25",
            "masked_abs_J_secant_bounds_for_published_waves":masked_min}


def balanced_lcu():
    # Coefficient quadruples in basis (1,a,p,ap), matrices stored by columns.
    tables=[
        [[(2,0,0,0),(0,0,0,0)],[(0,0,0,0),(2,0,0,0)]],
        [[(0,2,0,0),(0,0,2,0)],[(0,0,-2,0),(0,2,0,0)]],
    ]
    maxima=[max(sum(abs(row[s]) for row in col) for tab in tables for col in tab)
            for s in range(4)]
    R=1<<(sum(maxima)-1).bit_length()
    for tab in tables:
        for i,col in enumerate(tab):
            reconstructed=[]
            for s,target in enumerate(maxima):
                selected=[(j,1 if entry[s]>0 else -1)
                          for j,entry in enumerate(col) for _ in range(abs(entry[s]))]
                require((target-len(selected))%2==0,"All balance corrections must be cancelling pairs")
                new=selected+[(i,1),(i,-1)]*((target-len(selected))//2)
                require(len(new)==target,"Degree count was not balanced")
                reconstructed.append(tuple(sum(sign for idx,sign in new if idx==j) for j in range(2)))
            require(reconstructed==[tuple(entry[s] for entry in col) for s in range(4)],
                    "Balanced failures may not change the coherent operator")
    actual_joint=[]
    for g in range(8):
        joint=sum((n*power(p,3+bin(g^((1<<s)-1)).count("1"))
                   for s,n in enumerate(maxima)),one*0)
        actual_joint.append(joint)
    require(sum(actual_joint,one*0)==sum(maxima)*one,
            "All eight actual golden outcomes must exhaust the accepted labels")
    scale=sp.Rational(2,R)**2*sp.Symbol("p")**3
    return {"logical_tables":["I","G"],"term_counts_by_degree":maxima,
            "label_words":R,"scale_of_success":str(scale),
            "raw_intermediate_success_and_all_8_g_flags_scalar":True,
            "late_failure_pvm":"one genuine [Walsh label = 0] mark"}


def price_boundary():
    # The phase-XOR code changes only the weight of the sine arm.
    chart=2*p-one
    require(chart==power(p,3) and p*a!=p,"Literal extra sine charge must reverse the sign")
    return {"critical_extra_Golden_charge":"1/2",
            "one_paid_0_10_phase_XOR_can_reverse_amplitude_sign":True}


if __name__=="__main__":
    result={"Bell_preparation":bell_film(),"native_balanced_rails":rails(),
            "local_work_control":local_work_control(),
            "fixed_sign_sharing":fixed_sign_skeleton(),
            "spectral_signs":signs(),"balanced_physical_writer":balanced_lcu(),
            "full_Book_tariff_identified":False,"price_boundary":price_boundary(),
            "GR_closed":False}
    print(json.dumps(result,indent=2))
