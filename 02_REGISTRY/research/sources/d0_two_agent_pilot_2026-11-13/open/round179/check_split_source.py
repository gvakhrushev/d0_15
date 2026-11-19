"""Literal CAR marker and exact comparisons on the present F5/F6 carriers."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys

from mpmath import iv

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
from check_parity_price import a as exact_a, action, ne, one, p as exact_p

sys.path.insert(0, str(PILOT / "open/round175/center"))
from check_centered_motion import interval_rotation, require, signs

ORIGINAL_PLAN = PILOT / "open/round174/material/RESULT.json"
REFINED_PLANS = PILOT / "open/round177/RESULT.json"
FOURIER_OWNER = PILOT / "direct/round86/clock/check_fourier_return.py"
FORWARD_OWNER = PILOT / "direct/round86/writer/FORWARD_WRITER_RU.md"


def interval(value, lo, hi):
    require(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), f"outside ({lo},{hi}): {value}")
    return [lo, hi]


def replay_marker(parity):
    controls = ((0, 3),) if parity else ((0,), (3,))
    width = 6+2*len(controls)
    born = tuple(range(6, width))
    word = []
    for i, sources in enumerate(controls):
        head, tail = born[2*i:2*i+2]
        word.extend((ne.Gate("CX", (4, head)), ne.Gate("G", (head,)), ne.Gate("CX", (4, head))))
        word.extend(ne.Gate("CX", (wire, head)) for wire in sources)
        word.extend((ne.Gate("CX", (head, tail)), ne.Gate("G", (tail,)), ne.Gate("CX", (head, tail))))
    execution = ne.Execution(width, born, (5,), tuple(word), ne.G_CX)
    ne.validate_execution(execution, max_qubits=width, max_expanded_stages=len(word))

    def append(register, bits, amplitudes):
        values = {}
        for col, coeff in register.items():
            if bits is None:
                for bit, amp in enumerate(amplitudes):
                    if amp != 0:
                        values[2*col+bit] = coeff*amp
            else:
                values[2*col+bits] = coeff
        return values

    for raw, right in product(range(16), range(2)):
        initial = {4*raw+2+right: one}
        state = initial
        for _ in born:
            state = append(state, None, (exact_a, exact_p))
        for gate in word:
            state = action(state, gate, width)

        expected = initial
        bits = ((raw >> 3) & 1, raw & 1)
        heads = (bits[0]^bits[1],) if parity else bits
        for label in heads:
            expected = append(expected, label, ())
            tail = (one, 0) if label else (exact_p-exact_p*exact_p, 2*exact_a*exact_p)
            expected = append(expected, None, tail)
        require(state == expected, "Occupied columns or untouched RIGHT changed")
    return {"exact_columns": 32, "births": len(born), "square_letters": dict(Counter(g.op for g in word))}


def entropy(weights, ell):
    return -sum(q*iv.ln(q) for q in weights)/ell


def marker_prices(p, probabilities):
    e0, e1, e14, e15 = probabilities
    g = lambda q: iv.sqrt(q*(2-q))
    d = lambda q: iv.sqrt(1-(1-(1-2*iv.sqrt(p)*p)*q)**2)
    project = lambda q: q*iv.sqrt(1-q)+(1-q)*iv.sqrt(q)
    clear = p**3+p+1
    q_high, q_low = e14+e15, e1+e15
    q_odd = e1+e14
    ell = -iv.ln(p)
    return {
        "square_parity": clear+g(q_high)+g(q_low)+d(q_odd)+p+g(q_odd),
        "square_two": 2*clear+2*(g(q_high)+g(q_low))+d(q_high)+d(q_low)+2*p,
        "proj_parity": project(q_odd),
        "proj_two": project(q_high)+(1-q_high)*project(e1/(1-q_high))+q_high*project(e15/q_high),
        "code_CQ_parity": 1+q_odd-entropy((1-q_odd,q_odd), ell),
        "code_CQ_two": 2+q_high+q_low-entropy(probabilities, ell),
    }


def f5_f6_base(p):
    b = (p*interval_rotation(p,712)[1])**2
    prices = marker_prices(p, (b/2,p,p**2-b,b/2))
    margins = {
        "square_parity": ("5.41849414078809", "5.41849414078810"),
        "square_two": ("8.69751400848043", "8.69751400848044"),
        "proj_parity": (".01125568915901", ".01125568915902"),
        "proj_two": (".69339938915186", ".69339938915187"),
        "code_CQ_parity": ("1.99730146946033", "1.99730146946034"),
        "code_CQ_two": ("1.61552878864950", "1.61552878864951"),
    }
    return b, {
        "both_literal_markers": [replay_marker(True), replay_marker(False)],
        "ideal_F5_F6_ready_active_mass": interval(b, ".00012394658731107", ".00012394658731108"),
        "identical_marker_ledger_values_F5_F6": {key: interval(prices[key], *bound)
                                                 for key,bound in margins.items()},
        "late_geometry_route_mass": interval(p**19, ".00010696331036034", ".00010696331036035"),
        "one_Choi_in_each_read_route_expected_invocations_given_ready":
            interval(b+p**19, ".00023090989767141", ".00023090989767143"),
        "three_Choi_for_geometry_one_for_matter_expected_invocations_given_ready":
            interval(b+3*p**19, ".00044483651839210", ".00044483651839211"),
        "expected_count_coin_tests_on_anchor":
            interval((1-p**18)/(1-p), "2.61758", "2.61759"),
    }


def replay_elliptic(p, anchor, powers):
    rows = []
    a = iv.sqrt(p)
    for site in range(16):
        x, y = [16*sum(k*signs(mask,site) for mask,k in enumerate(row)) for row in powers]
        state = [iv.mpf(0),a,p,iv.mpf(0)]
        for i,j,exponent in ((1,2,-16*anchor),(2,0,-x),(2,3,-y),(1,2,16*anchor),(2,3,y),(2,0,x)):
            c,s = interval_rotation(p,exponent)
            u,v = state[i],state[j]
            state[i],state[j] = c*u-s*v,s*u+c*v
        rows.append([value**2 for value in state])
    return [tuple(sum(slot)/8 for slot in zip(*rows[k:k+8])) for k in (0,8)]


def elliptic_test(p):
    input_data = json.loads(ORIGINAL_PLAN.read_text())
    ref = json.loads(REFINED_PLANS.read_text())["refinement"]
    data = {}
    for name, coeff, powers, errors in (
        ("original_B174",7596,input_data["cartesian_walsh_powers"],(("2.958e-6","2.959e-6"),("1.955e-7","1.957e-7"))),
        ("refined_B177",ref["common_anchor_power"],ref["cartesian_walsh_powers"],(("5.066e-11","5.068e-11"),("3.279e-13","3.281e-13"))),
    ):
        first,last = replay_elliptic(p,coeff,powers)
        diff_even = last[0]+last[3]-first[0]-first[3]
        data[name] = {"absolute_even_mass_delta": interval(abs(diff_even),*errors[0]),
                      "anchor_mass_absolute_defect_on_first_end": interval(abs(first[1]-p),*errors[1])}
    amplitude = (1/(128*iv.sin(iv.pi/8)))**2
    probs = [(amplitude*(1+t)/2,p,p**2-amplitude,amplitude*(1-t)/2)
             for t in (iv.mpf(3)/8,iv.mpf(5)/8)]
    lower,upper = [marker_prices(p, row) for row in probs]
    data["ideal"] = {"parity_receipt_price_jet": "0",
                     "squared_gate_movement_secant":
                         interval(4*(upper["square_parity"]-lower["square_parity"]),
                                  "-2.55e-4","-2.45e-4")}
    return data


def exact_fourier_axes():
    sites = list(product(range(4),repeat=4))
    unit = [tuple(int(i==j) for i in range(4)) for j in range(4)]
    stencil = unit+[tuple(a-b for a,b in zip(unit[i],unit[j])) for i in range(4) for j in range(i)]
    cosine = (1,0,-1,0)
    candidates = [k for k in sites if k<tuple(-j%4 for j in k)]
    chosen = sorted(candidates,key=lambda k: (-sum(cosine[sum(a*b for a,b in zip(k,d))%4]
                                                    for d in stencil),k))[:64]
    values = [Fraction(sum((-1)**k[axis] for k in chosen),64) for axis in (0,1)]
    require(values == [Fraction(-1,4),Fraction(-1,16)], "Original 64 mode pairs changed")
    table = [[1-values[axis]*(-1 if field==axis else 1) for axis in (0,1)] for field in (0,1)]
    ratio = table[0][0]*table[1][1]/(table[0][1]*table[1][0])
    require(ratio == Fraction(9,17), "True two-axis record rectangle")
    for x in sites:
        changed = (x[1]+2)%4
        require(((x[1]//2)^(changed//2)) == 1, "Full SITE sign conjugation")
    return {"half_shift_Grams": [str(g) for g in values],
            "active_report_q_over_2p3": [[str(q) for q in row] for row in table],
            "mixed_odds_ratio_against_real_stop": str(ratio)}


def cold_return(p,b):
    a,z,u = iv.sqrt(p), iv.mpf(1)/2**20, 2*p**3
    f = p**2*(a*p+p**3)**2/(p**2+p**4)
    early = f**16
    summation = lambda q,n: (1-q**n)/(1-q)
    n_h,n_phase = 2024,3028
    kappa = ((p**3*summation(f,16))**n_h*(p**3*summation(p**2,32))**n_phase
             *(p**5*summation(p**4,32))**n_h)
    q5,q6 = u*17/16,u*15/16
    v5,v6 = p-p**3*q5,p-p**3*q6
    baseline = 1-z+z*(early+kappa*(p**3*(1-b)+p**3*b*v5**2))
    delta = -iv.log1p(z*kappa*p**6*b*(q5-q6)*(v5+v6)/baseline)
    size = 2112
    beta = 2*p**2
    heat = iv.mpf(264)/(359*beta)*(beta/11)**size/factorial(size)/(1-beta/(11*(size+1)))
    require(heat.b < (iv.mpf(2)**-27500).a and (-delta).a > (iv.mpf(2)**-27349).b,
            "Parity split sign with paid original Fourier and common tail")
    return {"fresh_born_SITE_J_F6_minus_F5": interval(delta, "-6.510e-4108","-6.508e-4108"),
            "both_replacements_common_full_heat_difference_below": "2^-27500",
            "old_SITE_rank_256_exact_feedback_isospectral_for_paid_inverse": True,
            "extended_factory_reporter_run_in_full": False}


def printed_stop_scale(p):
    s0,s2,s3 = 2*p**3,4*p**3,16*p**9

    def weight(chance,digits,cap):
        stay = (1-chance)*p**digits
        return chance*p**(digits+1)*(1-stay**cap)/(1-stay)

    b = weight(s0,1,16)
    ready = b**86*weight(s2,1,32)**86*weight(s2,2,32)**86*weight(s3,1,32)**46
    lower = ((1-s0)*p)**16*(1-b**86)/(1-b)
    bounds = iv.mpf([lower.a,(lower+b**86).b])
    return {"priced_01_probability_in_A86_printed_valuation":
                interval(ready*p**4/bounds,"3.65080e-172","3.65082e-172"),
            "raw_01_probability_with_all_factories":
                interval(p*(1-(1-s0)**16)**86*(1-(1-s2)**32)**172*(1-(1-s3)**32)**46,
                         ".60155792559585",".60155792559587")}


def main():
    iv.dps = 82
    p = (iv.sqrt(5)-1)/2
    b,output = f5_f6_base(p)
    documents = (ORIGINAL_PLAN,REFINED_PLANS,FOURIER_OWNER,FORWARD_OWNER)
    print(json.dumps({
        "status": "PASS",
        "owners_sha256": {str(f.relative_to(PILOT)): sha256(f.read_bytes()).hexdigest() for f in documents},
        "ready_F5_F6": output,
        "ideal_and_literal_elliptic": elliptic_test(p),
        "exact_Fourier_record": exact_fourier_axes(),
        "matched_spectral_parity": cold_return(p,b),
        "stop_conditioning_scale": printed_stop_scale(p),
        "absolute_physical_book03_price_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
