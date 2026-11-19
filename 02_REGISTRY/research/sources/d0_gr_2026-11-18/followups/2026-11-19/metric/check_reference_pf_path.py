"""Rooted Fibonacci reference on parsed H.1 tokens and on the two raw slots."""
from collections import defaultdict
from itertools import product
import json

from check_extra_work import centre, span
from check_golden_record_race import gold, p
from check_source_price import load_control, need


def zero():
    return gold(0)


def mark(bits):
    return "".join("10" if b else "0" for b in bits)


def path_trace(word):
    # The positive right profile is (1,p); state R follows 0, P follows 1.
    if "11" in word:
        return zero()
    return p**(len(word)+int(word.endswith("1")))


def finite_serialization():
    outputs={}
    for n in range(1,11):
        sigma=defaultdict(zero)
        for bits in product((0,1),repeat=n):
            length=n+sum(bits)
            word=mark(bits)
            cylinder=p**length
            need(path_trace(word)==cylinder,"actual complete-return path weight")
            # Each complete cylinder already gives n or more serialized letters.
            sigma[word[:n]]+=cylinder
        legal=[word for word in map("".join,product("01",repeat=n)) if "11" not in word]
        need(set(legal)==set(sigma) and sum(sigma.values(),zero())==gold(1),"complete prefix cube")
        for word in legal:
            need(sigma[word]==path_trace(word),"measured token stream has the full Parry marginal")
            need(path_trace(word)==path_trace(word+"0")+path_trace(word+"1"),"central trace refinement")
        outputs[n]=len(legal)
    need([path_trace(k) for k in ("00","01","10","11")]==[p**2,p**3,p**2,zero()],
         "normalized READY-root corner weights")
    return outputs


def neutral_writer():
    ne,digest=load_control()
    import sympy as sp
    e=ne.Execution(2,(),(),(ne.Gate("CX",(0,1)),ne.Gate("G",(1,)),ne.Gate("CX",(0,1))),
                   report_bits=(0,1))
    body=ne.execution_from_json(ne.canonical_json(e),max_qubits=2,max_expanded_stages=3)
    w=ne.word_matrix(body,max_qubits=2,max_expanded_stages=3)
    v=sp.Matrix([ne.A,ne.P])
    out=w*sp.kronecker_product(v,v)
    expected=sp.Matrix([ne.A*ne.P**3,2*ne.A**2*ne.P,ne.P,0])
    need(ne.exact_matrix_equal(out,expected),"actual NC1 all four amplitudes")
    need(ne.exact_matrix_equal(w.T*w,sp.eye(4)),"no dirty column removed")
    need(ne.exact_matrix_equal(w[2:,2:],ne.G_LOCAL.T),"exact zero from coherent cancellation")
    need(ne.exact_matrix_equal(sp.Matrix([out[0]*out[2]]),sp.Matrix([ne.A*ne.P**4])),
         "measurable READY matrix unit has nonzero coherence before dephasing r")
    law=[p**7,4*p**4,p**2,zero()]
    need(sum(law,zero())==gold(1) and law[0]+law[1]==p,"paid 0/10 neutral word law")
    return {"owner_sha256":digest,"raw_00_01_10_11":[x.strings() for x in law],
            "READY_00_10_coherence_before_dephasing_r":"sqrt(p)*p^4",
            "parsed_marks":[p.strings(),(p**2).strings()]}


def ln_interval(z):
    if z.lo>2:
        return span(2).log_positive()+ln_interval(z/2)
    if z.lo>1:
        return z.log_positive()
    if z.hi<1:
        return -ln_interval(1/z)
    if z.lo==z.hi==1:
        return span(0)
    raise ValueError("interval log crossings")


def binary_kl(q,r):
    return q*ln_interval(q/r)+(1-q)*ln_interval((1-q)/(1-r))


def overlap(a,b):
    return max(a.lo,b.lo)<=min(a.hi,b.hi)


def entropy_and_seams():
    q,ell=centre()
    pg=(span(5).sqrt()-1)/2
    l=pg**2
    k=4*pg**3
    ready=[pg**2,pg**3,pg**2]
    d0=binary_kl(q,l)
    dk=binary_kl(k,l)
    fine=[(1-q)*(1-k),(1-q)*k,q]
    direct=sum((x*ln_interval(x/y) for x,y in zip(fine,ready)),span(0))
    need(overlap(direct,d0+(1-q)*dk),"full three-path relative entropy decomp")
    recovered=[(1-q)*pg,(1-q)*l,q]
    rec=sum((x*ln_interval(x/y) for x,y in zip(recovered,ready)),span(0))
    need(overlap(rec,d0),"recovered AF trace divergence equals parsed divergence")
    affinity= (q*l).sqrt()+((1-q)*pg).sqrt()
    loss=(1-q)*l*q
    raw_loss=(1-q)*k*q
    need(0<loss.lo<loss.hi<raw_loss.lo and affinity.hi<1,"forbidden seam and mutual separation")
    return {"H1_q":q.fmt(15),"parsed_KL_nats":d0.fmt(15),"parsed_KL_golden":(d0/ell).fmt(15),
            "extra_NC1_raw_slot_KL_nats":((1-q)*dk).fmt(15),
            "recovered_KL_nats":rec.fmt(15),"NC1_whole_two_slot_KL_nats":direct.fmt(15),
            "return_Hellinger_affinity_per_label":affinity.fmt(15),
            "TV_bound_for_100_registered_labels":(1-affinity**100).fmt(15),
            "probability_11_seam_LC4":loss.fmt(15),"probability_11_seam_NC1":raw_loss.fmt(15)}


def complete_cylinders():
    # A field-independent stopping task reads a first 1 or stops at the third report.
    tokens=((1,),(0,1),(0,0,1),(0,0,0))
    physical=2*p**3   # exact ordered-bank q of the previously certified native pair
    need(physical==p**2+p**5,"ordered CX(e,b) native bank gives this registered q")
    surplus=zero()
    for w in tokens:
        m=physical**sum(w)*(1-physical)**(len(w)-sum(w))
        surplus+=m*len(w)
        need(path_trace(mark(w))==p**(len(w)+sum(w)),"complete stopping antichain trace")
    need(sum((path_trace(mark(w)) for w in tokens),zero())==gold(1),"exhaustive stop")
    need(surplus==1+(1-physical)+(1-physical)**2,"all paid stopping alternatives")
    # Even at calibrated q=p² the next real cell can begin with 1 after prior tail=1.
    seam=p*p**2*p**2
    need(seam==p**5 and seam!=zero(),"pair of calibrated two-slot laws violates the raw subshift")
    k=4*p**3
    need(k!=p**2 and p**6+k==gold(1),"conditional tail law differs on full real writer")
    return {"true_q":physical.strings(),"stopped_PF_weights_on_1_01_001_000":
            [path_trace(mark(w)).strings() for w in tokens],"mean_stopped_reports":surplus.strings(),
            "calibrated_recovered_raw_seam":seam.strings()}


def main():
    print(json.dumps({"status":"PASS","exact_power_basis":"1,p; p²+p=1",
        "prefix_counts":finite_serialization(),"neutral_NC1":neutral_writer(),
        "true_raw_and_parsed":entropy_and_seams(),"stopped_cylinders":complete_cylinders(),
        "claimed_scope":"operational report and explicit rooted corner; no full RAW/Book price binding"},
        ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
