"""Paid NC1 readout of every LIVE tail, including complete computational refinements."""
from fractions import Fraction as F
from itertools import product
import json

from check_counted_separator import analysis as previous_master, native_fronts
from check_extra_work import Span, span
from check_golden_record_race import gold, p as exact_p
from check_live_parser import controller
from check_reference_pf_path import ln_interval
from check_repeat_clock import local_native
from check_source_price import load_control, need


def validate_nc1():
    import sympy as sp
    ne, digest = load_control()
    pair = ne.Execution(2, (), (), (ne.Gate("CX",(0,1)), ne.Gate("G",(1,)), ne.Gate("CX",(0,1))))
    mat = ne.word_matrix(pair, max_qubits=2, max_expanded_stages=3)
    need(ne.exact_matrix_equal(mat, sp.diag(ne.G_LOCAL, ne.G_LOCAL.T)), "full native controlled reader")
    vec = sp.Matrix([ne.A, ne.P])
    iso = sp.kronecker_product(sp.eye(2),vec)
    need(ne.exact_matrix_equal(iso.T*mat*iso, ne.A*sp.eye(2)), "cold compression on arbitrary input")
    need(ne.exact_matrix_equal(ne.G_LOCAL.T * vec, sp.Matrix([1,0])), "deterministic valid one head")
    need(ne.exact_matrix_equal(ne.G_LOCAL*vec,sp.Matrix([ne.P**3,2*ne.A*ne.P])), "zero-head tail amplitudes")
    return digest


def fine_kernel():
    p=exact_p
    u,s=p**2,4*p**3
    def transitions(bits):
        return [(out,weight) for out in product((0,1),repeat=4)
                if (weight:=mass(bits,out))!=gold(0)]
    def mass(heads,tails):
        weight = gold(1)
        for h,f in zip(heads,tails):
            weight *= (1-f) if h else (s if f else (1-s))
        return weight
    support={}
    for herald,t in product((0,1),repeat=2):
        total=gold(0)
        expected=gold(0)
        support_size=0
        for error in (0,1):
            d=t^error
            heads=(d,herald^d,error,t)
            for old, w in transitions(heads):
                for new, y in transitions(old):
                    prob=(u if error else (1-u))*w*y
                    total+=prob
                    expected+=prob*(8+sum(heads)+sum(old))
                    support_size+=1
        mean_heads=(3*u+(3-4*u)*t) if herald==0 else (1+u+t)
        need(total==gold(1) and expected==8+mean_heads+s*(4-mean_heads), "complete paid fine joint law")
        support[f"{herald}{t}"]=support_size
    return support


def analyze():
    digest=validate_nc1()
    need(native_fronts()[0]==digest==controller()[0]==local_native(), "same source bank, LIVE and changed fronts")
    p=(span(5).sqrt()-1)/2
    ell=ln_interval(1/p)
    u,s=p**2,4*p**3
    def h(x):
        return -(x*ln_interval(x)+(1-x)*ln_interval(1-x))/ell
    piv=u+p**3*u
    Hs,Hu=h(s),h(u)
    Nheads=p*(3*u+(3-4*u)*piv)+u*(1+u+piv)
    Ntail=s*(4-Nheads)
    mean_code=8+Nheads+Ntail
    fine=Hu+(4-Nheads)*Hs+(4-Ntail)*Hs
    bit=ln_interval(span(2))/ell
    old_bound=4*bit+h(piv)+(1-piv)*Hs+Hu
    master=previous_master()
    v=Span(F(master["noise_minus"][0]),F(master["noise_minus"][1]))
    dL=u*(u-v)
    dFine=u*(h(u)-h(v))-(1-s)*Hs*dL
    dLpaid=(1-s)*dL
    budgets={}
    for nu, hidden_bits, coded_bits in ((1,24,49),(2,46,140)):
        scale=1+F(1,nu)
        D=(1+piv)+16*mean_code-scale*(old_bound+16*fine)
        paid_slope=scale*dFine-dLpaid
        extra=1-scale*Hs
        # Log cardinality in bits: avoids taking exponentially large intervals.
        free_bits=D/(scale*bit)
        compressed_bits=nu*D/bit
        need(D.lo>0 and paid_slope.lo>0 and extra.lo>0, "strict absolute and finite-source obligations")
        need(free_bits.lo>hidden_bits and compressed_bits.lo>coded_bits, "latent cardinality thresholds")
        budgets[nu]={"certified_deficit_lower_bound":D.fmt(14)[0],
                     "min_extra_entropy_as_bits_lower_bound":free_bits.fmt(12)[0],
                     "min_if_additional_Kraft_paid_as_bits_lower_bound":compressed_bits.fmt(12)[0],
                     "required_delta_extra_work_if_no_extra_labels":paid_slope.fmt(15),
                     "min_deficit_increment_per_further_NC1":extra.fmt(15)[0]}
    z=F(1,2**20)
    # Express both sides in 10^-48 units before interval multiplication.
    feedback_lower=(1-z)*p**64*span(F(master["minus_delta_feedback"][0])*10**48)
    heat_upper=span(F(6*88*10**48,359*64**15*2**64))
    gap=(feedback_lower-heat_upper)
    need(gap.lo>0, "whole two-grade heat plus feedback decreases for the PAID audit graph")
    return {"status":"PASS","native_owner":digest,"live_blocks":16,"new_readers":64,
            "added_births":64,"added_square_letters":192,"positive_fine_cells_per_H_T_one_block":fine_kernel(),
            "old_entropy_upper_phi":old_bound.fmt(14)[1],
            "paid_lengths_one_block":mean_code.fmt(14),"all_new_work_entropy_one_block_phi":fine.fmt(14),
            "all_new_tails_binary_entropy_phi":Hs.fmt(14),
            "fine_entropy_delta_including_additional_detectors":dFine.fmt(15),
            "paid_token_length_delta":dLpaid.fmt(15),"conditional_budgets":budgets,
            "verified_bounds_in_units_1e-48":{"minus_delta_J_lower":feedback_lower.fmt(6)[0],
               "abs_delta_heat_upper":heat_upper.fmt(6)[1],"minus_delta_full_RAW_lower":gap.fmt(6)[0]},
            "physical_Book_absolute_work_equals_native_TP_inferred":False}


if __name__=="__main__":
    print(json.dumps(analyze(),ensure_ascii=False,indent=2))
