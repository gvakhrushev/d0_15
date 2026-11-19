"""Native short selectors and independent checks for matched READY."""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

from mpmath import iv
import sympy as sp

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
from check_parity_price import a, action, ne, one, p

SOURCE = PILOT / "open/round179/RESULT.json"


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def power(value, n):
    result = one
    for _ in range(n):
        result = result*value
    return result


def enclosed(value, lo, hi):
    require(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), f"outside ({lo},{hi}): {value}")
    return [lo, hi]


def native_flags():
    def make(extra):
        # Source wire 0 is arbitrary protected old RIGHT. Fresh head/tail are 1,2.
        word = (ne.Gate("G",(1,)),)*extra + (
            ne.Gate("CX",(1,2)),ne.Gate("G",(2,)),ne.Gate("CX",(1,2)))
        execution = ne.Execution(3,(1,2),(0,),word,ne.G_CX)
        ne.validate_execution(execution,max_qubits=3,max_expanded_stages=len(word))
        probabilities = []
        for owner in (0,1):
            state = {4*owner+2*head+tail: hv*tv
                     for (head,hv),(tail,tv) in product(enumerate((a,p)),repeat=2)}
            for gate in word:
                state = action(state,gate,3)
            require(all((col>>2)==owner for col in state), "Flag touched protected RIGHT")
            masses = [sum(value*value for col,value in state.items()
                          if (col&3) in pattern)
                      for pattern in ((0,1),(2,),(3,))]
            require(masses[2] == 0 and sum(masses) == one, "All raw NC1 stops retained")
            probabilities.append(masses)
        require(probabilities[0] == probabilities[1], "Old-reference scalar")
        return probabilities[0]

    standard, doubled, fourth = (make(k) for k in (0,1,3))
    p6 = power(p,6)
    s2,s3 = 4*power(p,3),16*power(p,9)
    require(standard[0] == p and doubled[:2] == [p6,s2] and fourth[1]==s3,
            "Owned Golden rates")
    g0 = power(p,19)
    prefix = power(p6,3)
    prefix_complete = sum(power(p6,k)*(one-p6) for k in range(3)) + prefix
    require(prefix_complete==one and prefix*p==g0, "Finite stop and shared pass")
    geom = prefix*p
    matter = prefix*p*power(p,2)
    require(geom+matter==g0*(one+power(p,2)), "Fixed reach")
    require(s2*power(2*power(p,3),2)==s3,
            "Independent plus-ready filter gives maximal CZ/CCZ match")
    return {
        "native_flag_words_extra_G": [0,1,3],
        "raw_NC1_head_one_masses": ["p^2", "4p^3", "16p^9"],
        "three_short_prefix_pass_mass": "p^18",
        "three_short_prefix_bright_leaf_stages": 21,
        "previous_bright_leaf_stages_with_18_standard_NC1": 108,
        "supplier_call_per_ready_CAR": "p^19(1+p^2)",
        "common_signed_gain_before_shared_READY": "p^19 / Lambda",
        "exact_constant_thinning_CZ_to_CCZ": "two fair-pair heralds before CZ",
    }


def joint_covariance():
    t = sp.Symbol("t",real=True)
    totals = [0]*5
    for x0,x1,x2 in product(range(2),repeat=3):
        probability = (1+t*(-1)**(x0^x2))/8
        f,q,report = 1-x0,1-x1,(-1)**x2
        for i,v in enumerate((f,q,f*q,report,f*q*report)):
            totals[i] += v*probability
    expected = [sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,4),0,t/4]
    require([sp.expand(z) for z in totals]==expected, "Physical SITE-conditioned counterexample")

    z = (sp.sqrt(5)-1)/2
    P = sp.diag(1,0)
    G = sp.Matrix([[sp.sqrt(z),-z],[z,sp.sqrt(z)]])
    Q = G.T*P*G
    for matrix,wanted in ((P*Q*P,z*P),(Q*P*Q,z*Q)):
        require((matrix-wanted).applyfunc(sp.simplify)==sp.zeros(2), "Two actual orderings")
    Z = sp.diag(1,-1)/2
    require(sp.simplify(sp.trace(Z*z*(P-Q))-z**3)==0, "Equal rates but different derivatives")
    return {
        "same_SITE_affine_family_ALL_rates": ["1/2","1/2","1/4"],
        "desired_unconditional_signed_score": "0",
        "true_cross_ready_signed_score": "t/4",
        "G_rotated_projector_order_reference_distance": "p",
        "G_rotated_projector_order_effect_norm_difference": "p^2",
        "G_rotated_projector_order_jet_difference": "p^3",
    }


def actual_readiness_numbers():
    t = (iv.sqrt(5)-1)/2
    g0 = t**19
    code = t**6
    beta = 4*t**3
    cc = 16*t**9
    # Native NC1 phase packet cold end: zero head p^2, successful head p^3.
    def packet(cap):
        abort = t**(2*cap)
        success = t**3*(1-abort)/(1-t**2)
        return abort,success

    d16,s16 = packet(16)
    d32,s32 = packet(32)
    difference = (d16+s16*d32)-(d32+s32*d16)
    require(abs(difference-t*(d16-d32)).b < iv.mpf("1e-67"),
            "All genuine early cold aborts are order-sensitive")
    qcap = 1-(1-cc)**32
    ccap = 1-(1-beta)**32
    tie = t**2+t**4
    rate_1 = 2*t**3*(1-tie)
    rate_4 = 2*t**3*(1-tie**4)
    return {
        "short_prefix_expected_attempts": enclosed(1+code+code**2,"1.05883371001598","1.05883371001599"),
        "supplier_reach_one_Choi_each_arm": enclosed(g0*(1+t**2),".00014781965936879",".00014781965936880"),
        "expected_Choi_three_on_geo_one_on_q": enclosed(g0*(3+t**2),".00036174628008947",".00036174628008949"),
        "expected_Choi_three_on_each_common_dispatch":
            enclosed(3*g0*(1+t**2),".00044345897810636",".00044345897810640"),
        "gate_pre_rate_CZ_CCZ_cap32_product": enclosed(qcap*ccap,".99948066637875",".99948066637876"),
        "unequal_native_caps_cold_order_difference": enclosed(difference,"1.26e-7","1.29e-7"),
        "balanced_CZ_vs_fair_pair_rate_with_one_comparison": enclosed(rate_1,".22291",".22292"),
        "balanced_CZ_vs_fair_pair_rate_with_four_comparisons": enclosed(rate_4,".43547",".43549"),
    }


def two_pass_words():
    def evaluate(bits):
        length = 0
        visits = one-one
        stop_mass = one-one
        for bit in map(int,bits):
            visits = visits+power(p,length)
            stop_mass = stop_mass+power(p,length+2-bit)
            length += 1+bit
        born_pass = power(p,length)
        require(stop_mass+born_pass==one, "Every first mismatch is retained")
        return length,visits,len(bits)

    first,second = evaluate("0"*18),evaluate("0"*10+"1"*4)
    require(first[0] == second[0] == 18, "Same Born coverage")
    require(2+first[0]+first[2] == 6+second[0]+second[2] == 38,
            "Same combined passive scale")

    r=(iv.sqrt(5)-1)/2
    visits_delta=sum(r**j for j in range(18))-sum(r**j for j in (*range(10),10,12,14,16))
    require(visits_delta.a > (r**18).b, "Native visits differ at fixed pass and cold")
    return {
        "canonical_pass_words": ["0^18","0^10 1^4"],
        "equal_Born_pass": "p^18",
        "equal_passive_after_marker": "p^38",
        "literal_code_minus_CQ_on_each_independent_selector": "0",
        "visits_gap": enclosed(visits_delta,".00795754",".00795756"),
    }


def block_balance():
    def statistics(accepts_early):
        # The two schedules execute the same test 2 iff test 1 says 0.
        rows = ((2,1,accepts_early,3), (2,2,not accepts_early,4), (3,2,False,5))
        pass_born = sum(power(p,length) for length,calls,accept,cold in rows if accept)
        visits = sum(calls*power(p,length) for length,calls,accept,cold in rows)
        histogram = {(length,accept): power(p,length) for length,calls,accept,cold in rows}
        passive = sum(power(p,cold) for length,calls,accept,cold in rows if accept)
        return pass_born,visits,histogram,passive

    active,padded = statistics(False),statistics(True)
    require(active[:3]==padded[:3] and active[0]==power(p,2) and active[1]==one+p,
            "Equal Born, work and complete code length and status law")
    require(active[3]==power(p,4) and padded[3]==power(p,3), "Correct passive pass")
    require(power(active[3],4)*power(p,22)==power(padded[3],4)*power(p,26)==power(p,38),
            "Ready cold scale after four blocks and ten prefix zeros")

    t,R,K,K3 = sp.symbols("t R K K3", positive=True)
    z_active = K*t+K*t*t*R+K3*t*t
    z_padded = K*t*R+K*t*t+K3*t*t
    require(sp.expand(z_active-z_padded-K*t*(1-t)*(1-R))==0,"Nonlinear price gap")
    z = sp.Symbol("p")
    left,right = sp.Integer(1),sp.Integer(1)
    for _ in range(4):
        left = (z**2*t+z**3*t*t)+z**2*t*t*left
        right = (z**2+z**3)*t*t+z**2*t*right
    difference = (z*t)**10*(left-right)
    reduce = lambda expr: sp.rem(sp.expand(expr),z**2+z-1,z)
    require(reduce(sp.diff(difference,t).subs(t,1))==0,"Whole chronology mean")
    variance_gap = 2*z**11*(1+2*z*z+3*z**4)
    require(reduce(sp.diff(difference,t,2).subs(t,1)-variance_gap)==0,
            "Whole chronology exponential ledger sees the higher moments")
    return {
        "two_bit_blocks_have_same_Born_and_expected_native_calls": ["p^2","1+p"],
        "per_block_passive_pass": ["p^4","p^3"],
        "two_ten_zero_prefix_four_block_trees_pass": "p^18",
        "passive_after_CAR_mark": "p^38",
        "nonlinear_economic_subsums_difference": "K t (1-t)(1-R)",
        "whole_native_visit_variance_gap_A_minus_filler": "2 p^11 (1+2p^2+3p^4)",
        "classical_controller_and_actual_reports_executed_together": False,
    }


def main():
    iv.dps = 78
    print(json.dumps({
        "status": "PASS",
        "B179_receipt_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "literal_fresh_gates_and_budget": native_flags(),
        "ready_balance_checks": actual_readiness_numbers(),
        "born_and_passive_matched_but_work_not": two_pass_words(),
        "born_passive_and_mean_work_all_matched": block_balance(),
        "matched_marginals_not_enough": joint_covariance(),
        "full_new_Choi_dispatch_executed": False,
        "full_Book03_valuation_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
