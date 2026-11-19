"""Check a paid rare-union report and its complete seed/descriptor CQ law."""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import sys

import mpmath as mp

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round181"))
sys.path.insert(0, str(PILOT / "open/round121"))
from check_fixed_positive_reader import a, clear, cx, for_arrow, nc1, ne, one, p, power
from check_fixed_positive_reader import require, with_births
from check_book03_identity_pair import actual_words


def registered_copy():
    # Actual known one H, sharp precomputed OR S, arbitrary old k, old RIGHT.
    # Fresh head 4 and tail 5 are real Golden births. Store both after NC1.
    word = clear(4) + (cx(1, 4),) + nc1(4, 5)
    ex = ne.Execution(6, (4, 5), (2, 3), word, ne.G_CX, report_bits=(4,))
    ne.validate_execution(ex, max_qubits=6, max_expanded_stages=len(word))
    for s, k, right in product(range(2), repeat=3):
        prefix = 8+4*s+2*k+right
        root = with_births({prefix:one}, 2)
        actual = for_arrow(root, word, 6)
        tail = (one, 0) if s else (p-p*p, 2*a*p)
        target = {4*prefix+2*s+j: z for j,z in enumerate(tail) if z != 0}
        require(actual == target, "The NC1 head must read OR with every old column unchanged")
        require(sum(z*z for z in target.values()) == one, "A reachable head must have unit norm")
    return {"births": 2, "square_calls": dict(Counter(g.op for g in word)),
            "registered_heads": 1, "old_input_basis_columns": 8,
            "requires_actual_known_H_one": True}


def early_work_control():
    # Actual PORT=0, Z-seed v, protected Spin, two paid zero ancillas.
    w = actual_words()["G_Z_G_Z"]
    g, z = w[0], w[1:9]
    p0, p1 = w, z+(g,g)+z
    a_call, d_call = cx(1,4), cx(4,5)

    def inverse(word):
        out = []
        for gate in reversed(word):
            if gate.op == "G":
                out.extend(z+(gate,)+z)
            else:
                out.extend((gate,)*(3 if gate.op == "SourceI" else 1))
        return tuple(out)

    require(Counter(gate.op for gate in p0) == Counter(gate.op for gate in p1),
            "The two paid preparations must have the same operation inventory")
    for index, prep in enumerate((p0,p1)):
        stem = prep+(g,)
        restoration = inverse(stem)
        for echo_index, echo in enumerate(((d_call,d_call,a_call,a_call),
                                            (a_call,d_call,d_call,a_call))):
            for col in range(64):
                require(for_arrow({col:one},stem+echo+restoration,6) == {col:one},
                        "The full suffix must see the exactly same live state on every column")
            for spin in range(4):
                root = {4*spin:a, 16+4*spin:p}
                state = for_arrow(root,stem,6)
                q = sum(x*x for j,x in state.items() if j & 16)
                require(q == (4*power(p,3) if index == 0 else 0), "Wrong early Z occupation")
                nonstationary = 0
                for gate in echo:
                    following = for_arrow(state,(gate,),6)
                    overlap = sum(amplitude*following.get(j,0) for j,amplitude in state.items())
                    squared = one-overlap*overlap
                    require(squared == 0 or squared == 2*q-q*q,
                            "Expected actual trace movement for toggled fresh zero")
                    nonstationary += squared != 0
                    state = following
                require(nonstationary == ((2,4)[echo_index] if index == 0 else 0),
                        "Echo order must expose a nonzero early movement double contrast")
    return {"endpoint_on_all_64_columns": "I", "preparation_calls": 18,
            "echo_calls": 4, "movement_double_contrast_first_minus_second": "-2 sqrt(1-p^12)",
            "assignment_to_original_Book_tariff_proved": False}


def masked_named_work_control():
    # Named write and read of rail zero, each charged one when it occurs.
    charges = [[int(y ^ mask == 0) + int(1 ^ mask == 0) for mask in (0,1)]
               for y in (0,1)]
    require(charges == [[1,1],[0,2]], "Actual masked rail chronology")
    positive_delta = (sum(power(p,t) for t in charges[1]) -
                      sum(power(p,t) for t in charges[0]))
    require(positive_delta == power(p,4), "Equal means must not force equal positive masses")
    return {"equal_average_named_work": 1, "matched_normalized_mask_mass_delta": "p^4/2"}


def word_weights(m, d, k, base, pow_num):
    r = base * base
    # Each returned row is one specific T-string, indexed by its number of ones.
    return [(pow_num(r,s)*pow_num(base-d,m-s),
             pow_num(r+k*d,s)*pow_num(base-k*d,m-s))
            for s in range(m+1)]


def brute_three_state(m, d, k):
    r = p*p
    cells = defaultdict(lambda: one*0)
    # (T,R) before the fixed toggle is (0,0), (1,0), or (0,1).
    elementary = ((0,0,p-d), (1,0,r), (k,1,d))
    for seeds in product(elementary, repeat=m):
        weight = one
        for _,_,value in seeds:
            weight = weight * value
        cell = max(rare for _,rare,_ in seeds), sum(bit for bit,_,_ in seeds)
        cells[cell] += weight
    return cells


def test_exact(m, n):
    d = power(p,n+1)
    q = one-power(one-d,m)
    r = p*p
    for k in (0,1):
        rows = word_weights(m,d,k,p,power)
        early = sum(comb(m,s)*mark for s,(mark,_) in enumerate(rows))
        late = sum(comb(m,s)*(all_mass-mark) for s,(mark,all_mass) in enumerate(rows))
        require(early == one-q and late == q, "The union must have the same law at both ends")
        one_mass = sum(comb(m,s)*s*all_mass for s,(_,all_mass) in enumerate(rows))
        require(one_mass == m*(r+k*d), "Wrong mean of the individually retained descriptors")
        if m <= 8:
            cells = brute_three_state(m,d,k)
            for s,(mark,all_mass) in enumerate(rows):
                require(cells[0,s] == comb(m,s)*mark
                        and cells[1,s] == comb(m,s)*(all_mass-mark),
                        "Independent seed subsectors disagree with the closed law")


def entropy(k, arrays, m, lnphi, log, zero):
    result = zero
    for s,(early,whole) in enumerate(arrays):
        if (k == 0 and s == m) or (k == 1 and s == 0):
            continue
        rare = whole-early
        result -= comb(m,s)*rare*log(rare)/lnphi
    return result


def entropy_limit(m, base, log, mpf):
    r = base*base
    return m*sum(comb(m-1,b)*r**b*base**(m-1-b)*log(mpf(m-b)/(b+1))
                 for b in range(m))/log(1/base)


def interval_check():
    ctx = mp.iv
    ctx.dps = 80
    base = (ctx.sqrt(5)-1)/2
    d = base**9
    ell = ctx.ln(1/base)
    ctxpow = lambda x,n: x**n
    values = [entropy(k,word_weights(16,d,k,base,ctxpow),16,ell,ctx.ln,ctx.mpf(0))
              for k in (0,1)]
    secant = (values[1]-values[0])/d
    limit = entropy_limit(16,base,ctx.ln,ctx.mpf)
    require(secant > ctx.mpf("14.15637") and secant < ctx.mpf("14.15638"), "Entropy secant interval")
    require(limit > ctx.mpf("14.90530") and limit < ctx.mpf("14.90531"), "Entropy limit interval")
    c_fg = 5-6*base
    only_fresh_guard = c_fg*16-2*secant
    both_codes = (1+c_fg)*16-2*secant
    require(only_fresh_guard < 0 and both_codes > 0, "The actual separate print changes the sign")
    # Rational lower estimate valid for all N >= 8 by the paired-atanh proof.
    lower = Fraction(986,1000)**15 * 30 * Fraction(224,1000) / (17 * Fraction(482,1000))
    require(lower > Fraction(66,100), "Uniform lower bound on Delta H/(16 delta)")
    return {"m16_N8_entropy_secant_interval": ["14.15637","14.15638"],
            "m16_entropy_limit_interval": ["14.90530","14.90531"],
            "m16_N_ge8_entropy_secant_per_seed_between": ["0.66","1"],
            "m16_N8_only_FG3_conditional_Bellman_delta_negative": True,
            "m16_N8_separate_T_and_FG3_conditional_Bellman_delta_positive": True}


def screen(m, n):
    base = (mp.sqrt(5)-1)/2
    ell = mp.log(1/base)
    d = base**(n+1)
    q = 1-(1-d)**m
    rows = [word_weights(m,d,k,base,pow) for k in (0,1)]
    values = [entropy(k,arr,m,ell,mp.log,mp.mpf(0)) for k,arr in enumerate(rows)]
    secant = (values[1]-values[0])/d
    tv = mp.fsum(comb(m,s)*abs(end[1]-start[1])
                 for s,(start,end) in enumerate(zip(*rows)))/2
    def fmt(value):
        return mp.nstr(value, 18)

    return {
        "seeds": m,
        "N": n,
        "delta": fmt(d),
        "born_early_anchor_conditional_on_ready": fmt(1-q),
        "entropy_delta_per_delta": fmt(secant),
        "entropy_limit_per_delta": fmt(entropy_limit(m,base,mp.log,mp.mpf)),
        "record_T_only_code_Bellman_part_per_delta": fmt(m-2*secant),
        "record_FG3_only_code_Bellman_part_per_delta": fmt(m*(5-6*base)-2*secant),
        "record_T_and_FG3_codes_Bellman_part_per_delta": fmt(m*(6-6*base)-2*secant),
        "joint_record_TV_equals_T_marginal_TV": fmt(tv),
        "exact_old_program_return_upper_bound_given_joint_record": fmt(1-tv),
    }


def main():
    for m,n in ((1,8), (2,8), (3,8), (8,8), (16,8), (16,40), (32,8)):
        test_exact(m,n)
    with mp.workdps(100):
        observations = [screen(m,n) for m,n in ((2,8), (8,8), (16,8), (16,40), (32,8))]
    result = {"OR_native_copy": registered_copy(),
              "evaluations": observations,
              "early_work_control": early_work_control(),
              "A88_masked_named_work_control": masked_named_work_control(),
              "certified_sign_intervals": interval_check(),
              "full_original_Book_tariff_proved": False,
              "GR_closed": False}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
