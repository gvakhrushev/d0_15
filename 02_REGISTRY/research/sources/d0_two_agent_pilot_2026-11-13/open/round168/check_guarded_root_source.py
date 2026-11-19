"""Replay the full registered ledger for a guard and two transparent service codes."""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import subprocess

import mpmath as mp
import sympy as sp

from check_full_support_detector import b165_owner

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PRIMARY = "2fe4d3901"
SOURCE = ("02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
          "2026-11-19/metric/spectral_tree_balance_result.json")


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def check_record_tree(q, eta, ready, split, attempts, cycles):
    rates = (q,1-q,ready,1-ready,eta,1-eta,split,1-split)
    leaves = []

    def record(path, slots, length):
        return path+slots,length

    def visit(path, length, depth):
        for bit in (0,1):
            report_slot = int(bit == 0) if depth == 0 else int(bit == 1)
            report,r_length = record(path,(report_slot,),length+1+bit)
            leaves.append(record(report,(3,),r_length+1))
            measure(report+(2,),r_length+2,depth,bit,0)

    def measure(path, length, depth, bit, attempt):
        leaves.append(record(path,(4,int(bit == 0)),length+3))
        miss,m_length = record(path,(4,int(bit == 1)),length+3)
        if depth+1 == cycles:
            leaves.append((miss,m_length))
        else:
            visit(miss,m_length,depth+1)
        for slot,size in ((6,4),(7,2)):
            service,s_length = record(path,(5,slot),length+size)
            if attempt+1 == attempts:
                leaves.append((service,s_length))
            else:
                measure(service,s_length,depth,bit,attempt+1)

    visit((),0,0)
    normalizer = mean_length = Q(0)
    entropy_coefficients = [Q(0)]*len(rates)
    for factors,length in leaves:
        mass = Q(1)
        for slot in factors:
            mass *= rates[slot]
        normalizer += mass
        mean_length += mass*length
        for slot in factors:
            entropy_coefficients[slot] += mass
    active = ready*(1-(1-eta)**attempts)
    average_attempts = active/eta
    beta = 2*q*(1-q)
    average_visits = 1+active*beta*sum((active*(1-beta))**j for j in range(cycles-1))
    expected_entropy_coefficients = [
        average_visits*(1+active)*q, average_visits*(1+active)*(1-q),
        average_visits*ready, average_visits*(1-ready),
        average_visits*average_attempts*eta, average_visits*average_attempts*(1-eta),
        average_visits*average_attempts*(1-eta)*split,
        average_visits*average_attempts*(1-eta)*(1-split),
    ]
    expected_length = average_visits*(
        2*average_attempts+active+2-q+1+ready+2*average_attempts*(1-eta)*split
    )+2*q-1
    branch = 2*(2**attempts-1)
    require(len(leaves)==(2**(attempts+2))*sum(branch**j for j in range(cycles))+branch**cycles,
            "wrong number of positive terminal copies")
    require(normalizer==1 and mean_length==expected_length, "complete coded length or mass")
    require(entropy_coefficients==expected_entropy_coefficients, "complete chain entropy")


def check_constants():
    mp.iv.dps = 50
    one = mp.iv.mpf(1)
    p = (mp.iv.sqrt(5)-1)/2
    cos16 = p**3
    for _ in range(3):
        cos16 = 2*cos16**2-one
    eta = one-cos16**2
    split = 4*p**3
    # B167's replay certifies this interval for H=0 with 2096 total G.
    off = mp.iv.mpf(["7.056e-9","7.073e-9"])
    ready = one-off
    log_phi = -mp.iv.ln(p)

    def entropy(value):
        return -(value*mp.iv.ln(value)+(one-value)*mp.iv.ln(one-value))/log_phi

    require(eta.a > mp.iv.mpf(".8914") and (ready*eta).a > mp.iv.mpf(".89"),
            "native efficiency or readiness floor")
    require(entropy(split).b < split.a, "native service split positivity")
    for alpha in (mp.iv.mpf("1.5"),mp.iv.mpf(2)):
        guard_add = one+ready-alpha*entropy(ready)
        split_add_per_attempt = (one-eta)*(2*split-alpha*entropy(split))
        require(guard_add.a > 0 and guard_add.b < 2, "guard bracket")
        require(split_add_per_attempt.a > 0 and (split_add_per_attempt/eta).b < .25,
                "transparent code bracket")
    return {"strict_guard_ledger_addition":[0,2],"strict_service_ledger_addition":[0,.25],
            "literal_codes_derivative_floor_on_q_arc":"0.109"}


def check_selected_native_words():
    _,owner = b165_owner()
    p = owner.native.P
    angle_cosine = owner.native.A
    state = sp.Matrix([1])
    for _ in range(4):
        state = sp.kronecker_product(state,sp.Matrix([angle_cosine,p]))
    initial = sp.kronecker_product(sp.eye(4),state)
    report = [column for column in range(64) if column & 2]  # actual wire 4
    for power,order in ((6,(2,3)),(9,(3,2))):
        context,segments = owner.words(order)
        require(len(segments[0])==8 and len(segments[2])==22, "equal native layout")
        matrix = owner.native.word_matrix(context,max_qubits=6,max_expanded_stages=8)
        selected = (matrix*initial).extract(report,list(range(4)))
        effect = selected.T*selected
        require(owner.native.exact_matrix_equal(effect,sp.eye(4)*(1-p**power)/2),
                "actual scalar REPORT on every Spin column")


def check_native_price_secants():
    check_selected_native_words()
    one = mp.iv.mpf(1)
    p = (mp.iv.sqrt(5)-1)/2
    log_phi = -mp.iv.ln(p)
    cos16 = p**3
    for _ in range(3):
        cos16 = 2*cos16**2-one
    eta = one-cos16**2
    ready = one-mp.iv.mpf(["7.056e-9","7.073e-9"])
    split = 4*p**3
    g = ready*eta
    q0,q1 = (one-p**6)/2,(one-p**9)/2
    z = one/2**20
    heat_beta = 2*p*p
    x = heat_beta/11
    error = 2*x**4/(24*(one-x/5))
    total_heat_kl_error = 132*error/359+error**2*mp.iv.exp(4*heat_beta)/2
    uncertainty = mp.iv.mpf([-1,1])*total_heat_kl_error

    def entropy(q):
        return -(q*mp.iv.ln(q)+(one-q)*mp.iv.ln(one-q))/log_phi

    def thermodynamic_components(q):
        visits = one+2*g*q*(one-q)  # one corrective outer cycle; one tester attempt
        length = visits*(2*ready+g+2-q+1+ready+2*ready*(one-eta)*split)+2*q-1+9*(1+q)
        hq = visits*((one+g)*entropy(q)+entropy(ready)+ready*entropy(eta)
                     +ready*(one-eta)*entropy(split))
        return length,hq

    def return_overlap(q):
        w0,w1 = p**4,p**7
        a = p**4+p**7*(p**8+p**14)
        branch = (w0+w1)*p**7*p**11
        return p**45*(one+branch)*(branch+a*(w0-(w0-w1)*q))

    delta_j = 4*mp.iv.ln((one-z+z*return_overlap(q0))/(one-z+z*return_overlap(q1)))
    require(delta_j.a > 0, "native cold secant")
    c0,h0 = thermodynamic_components(q0)
    c1,h1 = thermodynamic_components(q1)
    bounds = (("1","-.186265","-.186261"),("2","-.192707","-.192705"))
    expected = []
    for nu,lo,hi in bounds:
        nv = mp.iv.mpf(nu)
        compensation = -(c1-c0-(one+one/nv)*(h1-h0))-(delta_j+uncertainty)/(nv*log_phi)
        require(mp.iv.mpf(lo).b < compensation.a and compensation.b < mp.iv.mpf(hi).a,
                "compensation interval for native same-layout comparison")
        expected.append([lo,hi])
    return {"same_layout_two_cycle_native_fields":True,
            "q_ends":["(1-p^6)/2","(1-p^9)/2"],
            "cold_secant_strictly_positive":True,
            "required_extra_cost_secant_enclosures_nu_1_then_2":expected}


def main():
    receipt = subprocess.check_output(["git","show",f"{PRIMARY}:{SOURCE}"],cwd=REPO)
    require(json.loads(receipt)["status"]=="PASS","primary spectral ledger replay")
    cases = 0
    for q,eta,ready,split,n,m in product(
        (Q(2,5),Q(1,2),Q(3,5)),(Q(8,9),Q(9,10)),(Q(37,39),),
        (Q(15,16),),range(1,4),range(1,4)
    ):
        check_record_tree(q,eta,ready,split,n,m)
        cases+=1
    print(json.dumps({
        "status":"PASS","exact_complete_printed_and_guarded_journals":cases,
        "native_arithmetic_bounds":check_constants(),
        "physical_NPS2_comparison":check_native_price_secants(),
        "energy_ledger_binding_proved":False,"GR_closed":False,
    },indent=2))


if __name__=="__main__":
    main()
