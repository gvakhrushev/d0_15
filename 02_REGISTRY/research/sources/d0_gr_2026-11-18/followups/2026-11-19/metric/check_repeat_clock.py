"""Growing-clock contrast of two real NPS2 words after QND record repetitions."""
from fractions import Fraction as F
import json

from check_extra_work import span
from check_source_price import load_control, need


def local_native():
    import sympy as sp
    from sympy.polys.matrices import DomainMatrix
    ne,digest=load_control()
    fld=ne.GOLDEN_FIELD
    def convert(m):
        return DomainMatrix.from_Matrix(m).convert_to(fld)
    def matrix(ex):
        gates=len(ex.gates)
        body=ne.execution_from_json(ne.canonical_json(ex),max_qubits=ex.qubits,
                                    max_expanded_stages=gates)
        return convert(ne.word_matrix(body,max_qubits=ex.qubits,max_expanded_stages=gates))
    p,a=ne.P,ne.A
    v=sp.Matrix([a,p])
    g=ne.Gate
    tx=g("CX",(1,2))
    suffix=ne.Execution(3,(),(),(g("CX",(0,1)),tx,g("G",(2,)),tx),report_bits=(1,2))
    w=matrix(suffix)
    j=convert(sp.kronecker_product(sp.eye(2),v,v))
    need((j.transpose()*w*j-convert(sp.diag(a,2*p**2))).is_zero_matrix,"native suffix cold sectors")
    need((w.transpose()*w-DomainMatrix.eye((8,8),fld)).is_zero_matrix,"complete native unitary")
    copy_ne=ne.Execution(2,(),(),(g("CX",(0,1)),g("CX",(1,0))),report_bits=(1,))
    call=[ne.gate_matrix(copy_ne,q,max_qubits=2,max_expanded_stages=2) for q in copy_ne.gates]
    gram=(call[0]-call[1]).T*(call[0]-call[1])
    need(gram.eigenvals()=={0:2,3:2},"trace norm of local native bank difference")
    born=convert(sp.kronecker_product(sp.eye(4),v,v,v,v))
    marks=[convert(sp.kronecker_product(sp.eye(16),q)) for q in
           (sp.diag(1,1,0,0),sp.diag(0,0,1,0),sp.diag(0,0,0,1))]
    for order,Q in (((2,3),p**2),((3,2),2*p**3)):
        bank=g("CX",order)
        sign=g("SourceI",(2,0,1))
        enc=g("CX",(4,5))
        ex=ne.Execution(6,(),(),(bank,g("CX",(2,4)),sign,sign,bank,enc,g("G",(5,)),enc),
                        profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),report_bits=(4,5))
        image=matrix(ex)*born
        pi=p**2+p**3*Q
        for proj,l,k in zip(marks,(1-pi,pi,0),
                            (a*(p-(p+a*p)*Q),a*(p**2-(p**2+a*p)*Q),0)):
            need((image.transpose()*proj*image-convert(l*sp.eye(4))).is_zero_matrix,
                 "true scalar mark effects, dark sector retained")
            need((born.transpose()*proj*image-convert(k*sp.eye(4))).is_zero_matrix,
                 "exact coherent cold response in each complete mark sector")
    return digest


def proof_bounds():
    p=(span(5).sqrt()-1)/2
    a=p.sqrt()
    z=F(1,2**20)
    k=2*p**2/a
    q0,q1=p**2,2*p**3
    need(0<k.lo<=k.hi<1 and (4*p).lo>1,"cold and heat ratios")
    positive=(1-2*a*p)/2
    need(positive.lo>0,"common cold margin on Q in [0,1/2]")
    qsum=q0+q1
    g0,g1=p+a*p,p**2+a*p
    need((2*p**2-qsum*g1).lo>0,"positive coefficient in two-bank difference")
    need((2*p-qsum*g0).lo>0,"uniform positive constant in two-bank difference")
    pref_norm=64*span(3).sqrt()
    rank=4
    def arithmetic(m):
        xi=k**m
        def cm(q):
            return a**(m+1)*(p+xi*p**2-(g0+xi*g1)*q)
        cm0,cm1=cm(q0),cm(q1)
        d0,d1=1-z+z*cm0**2,1-z+z*cm1**2
        gap=rank*(1+z*(cm0**2-cm1**2)/d1).log_positive()
        need(gap.lo>0 and d0.lo>d1.hi,"actual positive finite determinant gap")
        dim=572+64*19*(4**m-1)//3
        heat=6*pref_norm/(359*dim)
        upper=rank*z*p**m/(1-z)
        need(upper.lo>gap.hi,"initial-cut-independent determinant range")
        # Bounds: log(d0/d1)>=z*(cm0²-cm1²)/d0 >=z*(cm0²-cm1²).
        low=rank*z*p**(m+1)*(q1-q0)*g0*(2*p-qsum*g0)
        geometric_heat=18*pref_norm/(359*64*19*4**m)
        return dim,heat,gap,low,geometric_heat
    d,h,j,l,c=arithmetic(12)
    d13,h13,j13,l13,c13=arithmetic(13)
    need((j-h).lo>F(7,10**11) and l13.lo>c13.hi,"M=12 exact and geometric for every M>=13")
    dp=p**3*(q1-q0)
    need((dp-p**8).lo<=0<=(dp-p**8).hi,"distinct paid mark delta p^8")
    return {"through_control": "a^M*P0+(2p²)^M*P1; a=sqrt(p)",
        "Q_event_cuts":["p²","2p³"],"registered_probability_difference":"p^8",
        "per_copy_registered_mean_difference":"p^11","mode_clock_dimension_M12":d,
        "NPS2_prefix_stage_dimension":572,"prefix_trace_norm":pref_norm.fmt(15),
        "two_bank_M12_feedback_difference":j.fmt(20),
        "two_bank_M12_full_heat_difference_absolute_bound":h.fmt(20),
        "M12_full_master_difference_interval":[(j-h).fmt(20)[0],(j+h).fmt(20)[1]],
        "M13_feedback_geometric_lower":l13.fmt(20),"M13_heat_geometric_upper":c13.fmt(20),
        "all_M_greater_equal_12_strictly_positive":True,
        "scope":"Exact NPS2 contrast with common initial cut, rank four, native CQ records on the retained wires; full H.1 microscopic valuation open."}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","native_source_sha256":local_native(),**proof_bounds()},
                     ensure_ascii=False,indent=2))
