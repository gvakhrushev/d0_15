"""Retained eight-setting H.1 report and repeated native CX/NC1 noisy copies."""
import json
from fractions import Fraction as F
from math import comb
from itertools import product

from check_extra_work import centre
from check_golden_record_race import gold, p
from check_source_price import load_control, need


def native_clock():
    import sympy as sp
    ne, digest = load_control()
    g = ne.Gate
    raw = ne.Execution(3,(),(),
        (g("CX",(0,1)),g("CX",(1,2)),g("G",(2,)),g("CX",(1,2))), report_bits=(1,2))
    encoded=ne.canonical_json(raw)
    body=ne.execution_from_json(encoded,max_qubits=3,max_expanded_stages=4)
    w=ne.word_matrix(body,max_qubits=3,max_expanded_stages=4)
    need(ne.exact_matrix_equal(w.T*w,sp.eye(8)),"all eight actual columns")
    v=sp.Matrix([ne.A,ne.P])
    gv=ne.G_LOCAL*v
    outcomes=[]
    for t in (0,1):
        label=sp.eye(2)[:,t]
        out=w*sp.kronecker_product(label,v,v)
        r0,r1=(ne.A,ne.P) if t==0 else (ne.P,ne.A)
        target=sp.kronecker_product(label,sp.Matrix([r0*gv[0],r0*gv[1],r1,0]))
        need(ne.exact_matrix_equal(out,target),"fixed old control, both entire pure tails, dark 11")
        outcomes.append((p**2 if t==0 else p).strings())
    return {"native_source_sha256":digest,"raw_calls_per_copy":["CX(T,r)","CX(r,t)","G(t)","CX(r,t)"],
            "conditional_true_probability_code_10":outcomes}


def moments(max_count=8):
    one=gold(1)
    for n in range(1,max_count+1):
        for t in (0,1):
            mean,mm,pressure,probability=[gold(0)]*4
            for ds in product((0,1),repeat=n):
                # Costs are in Golden digits. l+log_phi Pr(D|T) is integral.
                exponents=[1+int(d!=t) for d in ds]
                length=n+sum(ds)
                mass=p**sum(exponents)
                net=length-sum(exponents)
                need(net==t*(2*sum(ds)-n),"pointwise paid net")
                likelihood=p**net if net>=0 else one/(p**(-net))
                mean+=mass*net
                mm+=mass*net*net
                pressure+=mass*likelihood
                probability+=mass
            need(probability==one and pressure==one,"full Born normalization and exponential ratio")
            need(mean==t*n*p**3 and mm-mean**2==t*4*n*p**3,"exact conditional moments")
    return {"all_transcripts_checked_through":max_count,"conditional_mean_in_golden_digits":"n*p^3*T",
            "conditional_variance":"4*n*p^3*T","Born_mean_phi_to_minus_net":"1"}


def retained_gain():
    q,ell=centre()
    weights=[F((-1)**(j-1)*comb(8,j),j*j) for j in range(1,9)]
    signed=sum(w*j*j for j,w in enumerate(weights,1))
    unsigned=sum(abs(w)*j*j for j,w in enumerate(weights,1))
    need((signed,unsigned)==(1,255),"signed and unsigned response")
    for power,value in ((3,1024),(4,4608)):
        need(sum(abs(w)*j**power for j,w in enumerate(weights,1))==value,
             "binomial moment in the full-field error budget")
    pd=1-((1-q)/q).log_positive()/ell
    gain=1+unsigned*pd
    need(68<gain.lo<=gain.hi<69,"strict recorded leading field source")
    return {"true_q_star":q.fmt(15),"dP_dq":pd.fmt(15),"signed_second_moment":str(signed),
            "unsigned_second_moment":str(unsigned),"complete_registered_leading_gain":gain.fmt(15)}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","golden_basis":"a+b*p, p²=1-p",
        "eight_settings":retained_gain(),"actual_reader":native_clock(),"all_histories":moments(),
        "scope":"Registered mean Cost-Info; no microscopic valuation or compiler of the selector assumed."},
        ensure_ascii=False,indent=2))
