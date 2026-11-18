"""Native stopped-report discrimination. Exact field arithmetic plus outward log intervals."""
from functools import lru_cache
from fractions import Fraction as F
import json

from check_extra_work import span
from check_golden_record_race import gold, p
from check_source_price import load_control, need


def sign(x):
    # 2(a+bp)=(2a−b)+b√5. Decide exactly before making any decimal approximation.
    t,b = 2*x.a-x.b,x.b
    def s(k):
        return (k>0)-(k<0)
    if t*b>=0:
        return s(t+b)
    return s(t) if t*t>5*b*b else s(b)


def minimum(values):
    result = values[0]
    for x in values[1:]:
        if sign(x-result)<0:
            result=x
    return result


LOW,HIGH = p**2,gold(F(1,2))
P_INTERVAL = (span(5).sqrt()-1)/2


def interval(x):
    return span(x.a)+span(x.b)*P_INTERVAL


def logarithm(z):
    if z.lo>2:
        return span(2).log_positive()+logarithm(z/2)
    if z.lo>1:
        return z.log_positive()
    if z.hi<1:
        return -logarithm(1/z)
    if z.lo==z.hi==1:
        return span(0)
    raise ValueError("unresolved logarithm sign")


def kl(x,y):
    a,b = interval(x),interval(y)
    return a*logarithm(a/b)+(1-a)*logarithm((1-a)/(1-b))


@lru_cache(None)
def risk(n,s,t):
    if not n:
        return minimum((s,t))
    continuation=[]
    for x,y in ((LOW,HIGH),(HIGH,LOW)):
        continuation.append(risk(n-1,s*x,t*y)+risk(n-1,s*(1-x),t*(1-y)))
    return minimum(continuation)


def risk_table():
    rows={}
    previous=gold(1)
    for n in range(9):
        val=risk(n,gold(F(1,2)),gold(F(1,2)))
        need(sign(val)>0 and sign(previous-val)>=0,"finite-error envelope is positive and monotone")
        rows[n]=dict(power_basis=val.strings(),interval=interval(val).fmt(14))
        previous=val
    need(risk(1,HIGH,HIGH)==(1-HIGH+LOW)/2,"one-call Bayes envelope")
    # Check both orientations and the limits of using a single asymmetric base.
    corners=[(x,y) for x in (LOW,HIGH) for y in (LOW,HIGH)]
    for x,y in corners:
        a,b=(LOW,HIGH) if sign(y-x)>=0 else (HIGH,LOW)
        m0=(b*x-a*y)/(b-a)
        m1=((1-a)*y-(1-b)*x)/(b-a)
        need(all(sign(t)>=0 and sign(1-t)>=0 for t in (m0,m1)),"oriented garbling probabilities")
        need((1-a)*m0+a*m1==x and (1-b)*m0+b*m1==y,"both input laws recovered")
    backwards_m1=((1-LOW)*LOW-(1-HIGH)*HIGH)/(HIGH-LOW)
    need(sign(backwards_m1)<0,"single fixed ordered base cannot realize its reversal")
    return rows


def native_pair():
    # The archive's NPS14 and a second true native direction of its two bank calls.
    ne,digest=load_control()
    import sympy as sp
    from sympy.polys.matrices import DomainMatrix
    field=ne.GOLDEN_FIELD
    def exact_matrix(m):
        return DomainMatrix.from_Matrix(m).convert_to(field)
    v=sp.Matrix([ne.A,ne.P])
    j=exact_matrix(sp.kronecker_product(sp.eye(4),v,v,v,v))
    one,invalid,zero=sp.diag(0,0,1,0),sp.diag(0,0,0,1),sp.diag(1,1,0,0)
    observables=[exact_matrix(sp.kronecker_product(sp.eye(16),q)) for q in (one,invalid,zero)]
    q_values=(LOW+p**5,LOW+2*p**6)
    out=[]
    for wires, q, q_event in zip(((2,3),(3,2)),q_values,(LOW,2*p**3)):
        bank=ne.Gate("CX",wires)
        read=ne.Gate("CX",(2,4))
        sign_call=ne.Gate("SourceI",(2,0,1))
        tx=ne.Gate("CX",(4,5))
        gs=(bank,read,sign_call,sign_call,bank,tx,ne.Gate("G",(5,)),tx)
        ex=ne.Execution(6,(),(),gs,profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),
                        report_bits=(4,5))
        body=ne.execution_from_json(ne.canonical_json(ex),max_qubits=6,max_expanded_stages=8)
        unit=exact_matrix(ne.word_matrix(body,max_qubits=6,max_expanded_stages=8))
        w=unit*j
        need(unit.transpose()*unit==DomainMatrix.eye((64,64),field),"complete native unitary")
        need(q==LOW+p**3*q_event and sign(q-LOW)>0 and sign(HIGH-q)>0,"true interior collar")
        for effect,expected in zip(observables,(q,gold(0),1-q)):
            row=w.transpose()*effect*w
            expected_scalar=sp.Rational(expected.a)+sp.Rational(expected.b)*ne.P
            expected_matrix=exact_matrix(sp.eye(4)*expected_scalar)
            need((row-expected_matrix).is_zero_matrix,"true four-column terminal effect")
        out.append({"bank_CX":wires,"Q_in_basis_1_p":q_event.strings(),"q_in_basis_1_p":q.strings(),
                    "q_interval":interval(q).fmt(15)})
    return q_values,out,digest


def stopped_example(q0,q1):
    # First 1 or timeout at three actual reports. Keep all four leaves.
    words=("1","01","001","000")
    def mass(w,q):
        return q**w.count("1")*(1-q)**w.count("0")
    d=span(0)
    table=[]
    one=gold(1)
    for w in words:
        m0,m1=mass(w,q0),mass(w,q1)
        need(sign(m0)>0 and sign(m1)>0,"both fields give positive support at every stop")
        posterior=m1/(m0+m1)
        table.append({"word":w,"probability_0":interval(m0).fmt(13),
                      "probability_1":interval(m1).fmt(13),"posterior_H1_equal_prior":interval(posterior).fmt(13)})
        d+=interval(m0)*logarithm(interval(m0/m1))
    calls=sum((mass(w,q0)*len(w) for w in words),gold(0))
    paid=sum((mass(w,q0)*(len(w)+w.count("1")) for w in words),gold(0))
    need(sum((mass(w,q0) for w in words),gold(0))==one and
         sum((mass(w,q1) for w in words),gold(0))==one,"all complete leaf masses")
    need(calls==1+(1-q0)+(1-q0)**2 and paid==(1+q0)*calls,"true length and call count")
    theoretical=interval(calls)*kl(q0,q1)
    need(d.lo>0 and (d-theoretical).lo<=0<=(d-theoretical).hi,"likelihood stopped chain rule")
    return {"leaves":table,"mean_calls_H0":interval(calls).fmt(13),
            "literal_paid_mean_H0":interval(paid).fmt(13),"KL_stopped_nats":d.fmt(14)}


def main():
    (q0,q1),pair,digest=native_pair()
    d0,d1=kl(LOW,HIGH),kl(HIGH,LOW)
    cost0,cost1=d0/(1+interval(LOW)),d1/(1+interval(HIGH))
    need(cost0.lo>cost1.hi and d1.lo>d0.hi,"extrema for cost and for calls differ")
    demand=kl(gold(F(19,20)),gold(F(1,20)))
    cost_bound=demand/cost0
    need(cost_bound.lo>130,"five-percent errors require over 130 paid units in mean")
    print(json.dumps(dict(status="PASS",native_owner_sha256=digest,
        admissible_report_closed_envelope=["p²","1/2"],native_compiler_rows=pair,
        finite_cap_optimal_equal_prior_risk=risk_table(),
        max_KL_per_call_nats=d1.fmt(15),KL_per_literal_length_l_to_u=cost0.fmt(15),
        KL_per_literal_length_u_to_l=cost1.fmt(15),expected_paid_lower_for_5pct_errors=cost_bound.fmt(12),
        stopped_true_pair=stopped_example(q0,q1),
        conclusions={"finite_zero_error_identification":False,"conditional_likelihood_update":True,
                     "physical_total_price_identified":False,
                     "endpoint_Bernoulli_experiments_admitted_as_two_H1_geometries":False}),
        ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
