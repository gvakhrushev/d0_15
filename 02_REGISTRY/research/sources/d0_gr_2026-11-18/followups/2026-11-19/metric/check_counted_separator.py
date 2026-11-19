"""Full two-H comparison on a genuine NPS2 history and fixed LIVE parser clocks."""
from collections import Counter
from fractions import Fraction as F
import json

from check_extra_work import span
from check_reference_pf_path import ln_interval
from check_repeat_clock import local_native
from check_live_parser import controller
from check_source_price import load_control, need


def native_fronts():
    import sympy as sp
    from sympy.polys.matrices import DomainMatrix
    ne,digest=load_control()
    fld=ne.GOLDEN_FIELD
    def dm(m):
        return DomainMatrix.from_Matrix(m).convert_to(fld)
    S=ne.Gate("SourceI",(2,0,1))
    G=ne.Gate("G",(2,))
    def cx(x,y):
        return ne.Gate("CX",(x,y))
    # Local order: Spin0,Spin1,port,H,fresh D. Other wires are spectators.
    sw=[cx(2,4),cx(4,2),cx(2,4)]
    def leg(n):
        return [G]*((14+n)//2)+[S,S]+[G]*((14-n)//2)+[S,S]
    gate=dm(ne.G_LOCAL)
    ans=[]
    identity=DomainMatrix.eye((2,2),fld)
    for n in (0,14):
        gates=sw+leg(n)+[cx(3,2)]+leg(-n)+[cx(3,2)]+sw
        ex=ne.Execution(5,(),(),tuple(gates),profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(0,1))
        ex=ne.execution_from_json(ne.canonical_json(ex),max_qubits=5,max_expanded_stages=44)
        need(Counter(g.op for g in ex.gates)=={"CX":8,"G":28,"SourceI":8},"common paid inventory")
        # Multiplication in the exact algebraic field avoids radical expression swell.
        W=DomainMatrix.eye((32,32),fld)
        local={}
        for g in ex.gates:
            k=(g.op,g.wires)
            if k not in local:
                local[k]=dm(ne.gate_matrix(ex,g,max_qubits=5,max_expanded_stages=44))
            W=local[k]*W
        block=gate**(2*n) if n else identity
        for i in range(16):
            for j in range(16):
                v=W[2*i:2*i+2,2*j:2*j+2]
                if i==j:
                    need((v-(block if i%2 else identity)).is_zero_matrix,"all dirty H and port columns")
                else:
                    need(v.is_zero_matrix,"old Spin, port and herald are preserved")
        ans.append([[g.op,*g.wires] for g in ex.gates])
    return digest,ans


def analysis():
    p=(span(5).sqrt()-1)/2
    a=p.sqrt()
    ell=(1/p).log_positive()
    z=F(1,2**20)
    q=p**2
    u=p**2
    cc,ss=span(1),span(0)
    for i in range(29):
        cc,ss=cc*a-ss*p,ss*a+cc*p
    v=ss**2
    need(0<ss.lo<=ss.hi<p.lo and cc.lo>0,"positive small-angle 29-rotation witness")
    J0=a*(p-(p+a*p)*q)
    J1=a*(p**2-(p**2+a*p)*q)
    old=J0+J1
    need(min(J0.lo,J1.lo)>0,"both actual, unselected NPS2 old cold sectors positive")
    big=a**5*p*(a+p)
    small=a**5*p*(cc+ss)
    inactive0=a**4*(p*a+p**3)
    inactive1=a**4*(p**2+a*p**2)
    K=15
    cinactive=p*(J0*inactive0**(K+1)+J1*inactive1**(K+1))
    cplus=cinactive+p**2*big**K*big*old
    cminus=cinactive+p**2*big**K*small*old
    gap=4*(1+z*(cplus**2-cminus**2)/(1-z+z*cminus**2)).log_positive()
    heat=span(F(6*88,359*64**K))
    need((gap-heat).lo>0,"strict full master sign at K=15")
    k16=16
    lower=4*z*p**4*(big**(2*k16))*old**2*(big**2-small**2)
    heat16=span(F(6*88,359*64**k16))
    need(lower.lo>heat16.hi and (64*big**2).lo>1,"uniform geometric separation for all K>=16")
    dkl=v*ln_interval(v/u)+(1-v)*ln_interval((1-v)/(1-u))
    dcode=-(p**2)*dkl/ell
    need(dcode.hi<0,"complete retained cq code decrease with no postselection")
    R=(u/v+(1-u)/(1-v))/2
    cscale=(span(5).sqrt())/2
    need(R.lo>1,"strict counted pressure increase")
    # Illustrative absolute comparison if all four fixed old weights have unit value.
    # Results also proved for all strictly positive fixed old weights.
    alpha=1/(1+cscale**(K+1))
    dcount=(1+alpha*(R-1)).log_positive()/ell
    need(dcount.lo>0,"four old sectors all summed")
    qfield=2*p**3
    G0=p*inactive0**(K+1)+p**2*big**(K+1)
    G1=p*inactive1**(K+1)+p**2*big**(K+1)
    fieldcold=a*(p-(p+a*p)*qfield)*G0+a*(p**2-(p**2+a*p)*qfield)*G1
    fieldj=4*(1+z*(cplus**2-fieldcold**2)/(1-z+z*fieldcold**2)).log_positive()
    fieldheat=6*64*span(3).sqrt()/(359*8192*64**K)
    need((fieldj-fieldheat).lo>0,"independent original-bank field direction has positive full spectral response")
    pi0,pi1=(p**2+p**3*Q for Q in (q,qfield))
    def paid(x):
        return 1+x+(x*ln_interval(x)+(1-x)*ln_interval(1-x))/ell
    fieldcode=paid(pi1)-paid(pi0)+(K+1)*(p*(3-4*u)+p**2)*(pi1-pi0)
    need(fieldcode.lo>0,"old code and every new active and inactive receipt on the field pair")
    for k in range(2,24):
        for n1 in range(1,k):
            for t in (p,p**2):
                x=span(F(n1,k))-t
                absx=x if x.lo>0 else -x
                need(absx.lo>(p**2/(k*k)).hi,"integer-multiplicity discrepancy")
    return {"q_event_old":"p²","noise_minus":v.fmt(16),"noise_plus":u.fmt(16),
        "positive_initial_return_amplitudes":[J0.fmt(16),J1.fmt(16)],
        "later_fixed_copies":K,"true_old_control_is_summed":True,
        "delta_RAW_upper_and_lower":[(-gap-heat).fmt(36)[0],(-gap+heat).fmt(36)[1]],
        "minus_delta_feedback":gap.fmt(36),"absolute_heat_upper":heat.fmt(36),
        "delta_complete_report_code":dcode.fmt(14),
        "active_count_mass_ratio_minus_over_plus":R.fmt(14),
        "example_delta_count_pressure_unit_old_weights":dcount.fmt(14),
        "example_active_fraction_plus":alpha.fmt(14),
        "independent_native_field_contrast_RAW":[(fieldj-fieldheat).fmt(36)[0],(fieldj+fieldheat).fmt(36)[1]],
        "independent_native_field_contrast_CQ":fieldcode.fmt(14),
        "cone_scope":"fixed nonnegative coefficients on a finite secant; local row requires the stipulated physical tangent and its heat norm",
        "book_vertex_self_information_inferred":False}


if __name__=="__main__":
    digest,fronts=native_fronts()
    need(local_native()==digest and controller()[0]==digest,"replay both original native bank and parser owners")
    print(json.dumps({"status":"PASS","pinned_source":digest,"changed_fronts_local_wires":fronts,**analysis()},
                     ensure_ascii=False,indent=2))
