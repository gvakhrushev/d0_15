"""Exact scalar polynomial and bounded Golden selector for the two original SC4 addresses."""
from fractions import Fraction as F
from math import comb, lcm
import json

from check_boundary_experiment import Golden as G
from check_eight_readers import inv
from check_shared_site_union import sci


def fibonacci(m):
    f = [1, 1]  # number of compositions of price n using digits of prices 1,2
    for _ in range(2, m+1):
        f.append(f[-1]+f[-2])
    return f


def unrank(cost, rank, counts):
    assert 0 <= rank < counts[cost]
    word = []
    while cost:
        zeros = counts[cost-1]
        bit = int(rank >= zeros)
        if bit:
            rank -= zeros
        word.append(bit)
        cost -= 1+bit
    assert rank == 0
    return tuple(word)


def rank_word(word, cost, counts):
    rank = 0
    for bit in word:
        if bit:
            rank += counts[cost-1]
        cost -= 1+bit
    assert cost == 0
    return rank


def check_front(m, allocations):
    p, one = G(0,1), G(1)
    counts, n = fibonacci(m), sum(allocations)
    h,o = counts[m]//n, counts[m-1]//n
    assert G(counts[m])*p**m + G(counts[m-1])*p**(m+1) == one
    # A hit is a composition of m. An overshoot appends 1 (price 2)
    # to a composition of m-1. Precomputed boundaries compare padded words.
    for cost, copies, final in ((m,h,()),(m-1,o,(1,))):
        if not copies:
            continue
        thresholds = []
        start = 0
        for amount in allocations:
            stop = start+copies*amount
            for rank in sorted({start, max(start,stop-1)}):
                bits = unrank(cost,rank,counts)
                assert rank_word(bits,cost,counts)==rank
                front = bits+final
                assert sum(1+b for b in front[:-1]) < m <= sum(1+b for b in front)
            if stop < counts[cost]:
                bits = unrank(cost,stop,counts)+final
                thresholds.append(bits+(0,)*(m-len(bits)))
            start = stop
        assert thresholds == sorted(set(thresholds))
    return G(h)*p**m + G(o)*p**(m+1), [h,o]


def main():
    p,one,z,zero = G(0,1),G(1),G(F(1,2**20)),G(0)
    h,alpha = G(F(1,256)), G(2*10946)*p**23
    def r(x,y):
        e = p**2*(one+x)
        l = G(4)*e*(one-e)
        u = p+p**2*y
        b = G(4)*u**2*(one-u**2)
        t = l+(one-l)*b
        return z*(t+b)-z**2*t*b
    b0 = G(4)*p**3
    rf = G(4)*p**2*(one-G(2)*p**2)*z*(one-z*b0)*(one-b0)
    ry = G(8)*p**3*(one-G(2)*p**2)*(z*(G(2)-b0)-z**2*(b0+G(2)*(one-b0)*b0))
    k = ry*inv(rf)
    w = [("f",3,F(8,15)),("f",8,F(-3,40))]
    w += [("m",j,F((-1)**(j-1)*comb(8,j),j)) for j in range(1,9)]
    for tag, degree in (("f",2),("m",8)):
        for power in range(1,degree+1):
            assert sum(v*j**power for t,j,v in w if t==tag) == (power==1)
    dual = [F(73*j-11*j*j,120) for j in range(1,9)]
    assert max(map(abs,dual))==1 and dual[2]==1 and dual[7]==-1
    f_norm = sum(abs(v) for t,j,v in w if t=="f")
    assert f_norm==F(73,120)
    common = lcm(*(v.denominator for t,j,v in w))
    alloc = [int(common*abs(v)) for t,j,v in w]
    norm = sum(abs(v) for t,j,v in w)
    step, classes = check_front(42,alloc)
    active = step*G(sum(alloc))
    gain = step*G(common)*h*alpha*rf
    r0 = r(zero,zero)
    intercept = step*(G(sum(n for (t,j,v),n in zip(w,alloc) if v<0))
                     +G(common*sum(v for t,j,v in w))*alpha*r0)
    cases = [[(one,one,G(F(3,8)),G(F(1,8)))],
             [(one,p,G(F(3,11)),G(F(-1,8))),(one,p**2,G(F(2,9)),G(F(1,7)))],
             [(one,p,G(F(2,9)),G(F(1,7))),(one,p**2,G(F(3,11)),G(F(-1,8)))],
             [(G(F(1,2)),G(F(4,3)),G(F(-1,7)),G(F(2,9))),
              (G(F(1,3)),one,G(F(1,8)),G(F(1,12)))]]
    outputs = []
    for cells in cases:
        assert sum((v*rho for v,rho,f,m in cells),zero)==one
        mark = zero
        for (tag,j,co),n in zip(w,alloc):
            probability = zero
            for v,rho,f,m in cells:
                x = G(j)*h*f*inv(rho) if tag=="f" else zero
                y = G(-j)*h*m*inv(rho) if tag=="m" else zero
                probability += v*rho*alpha*r(x,y)
            mark += step*G(n)*(probability if co>0 else one-probability)
        target = sum((v*(f-k*m) for v,rho,f,m in cells),zero)
        assert mark == intercept+gain*target
        outputs.append(mark)
    assert outputs[1] == outputs[2]
    old_w = [F((-1)**(j-1)*comb(8,j),j*j) for j in range(1,9)]
    old_den = lcm(*(x.denominator for x in old_w))
    old_alloc = [int(old_den*abs(x)) for x in old_w]
    old_step, old_classes = check_front(50,old_alloc)
    original_active = G(sum(old_alloc))*p**36
    cosine = one-G(2)*p**2
    for _ in range(9):
        cosine = G(2)*cosine**2-one
    visibility = (one-cosine)*G(F(1,2))*p**7
    original_gain = p**36*G(old_den)*h**2*p**3*visibility*alpha**2*rf**2
    # This coarse lower bound avoids constructing enormous powers in Q(sqrt(5)).
    # Union bound for one known-1 allocation plus 4 M binary and M ternary subtests.
    M, retries = 42**2+2*10*42+10*10+10,120
    fail = p**32 + G(M)*(G(4)*(one-G(4)*p**3)**retries+(one-G(16)*p**9)**retries)
    print(json.dumps({"status":"PASS","settings":8,"positive_address_rows":10,
        "allocations_f3_f8_then_m1_to_m8":alloc,"normalizing_l1":str(norm),"selector_cost_front":42,
        "active_mass":sci(active),"class_repetitions":classes,"max_fixed_selector_birth_reads":42,
        "baseline_direct_composite":sci(intercept),"gain_direct_SC2":sci(gain),
        "legacy_gain_SC2":sci(original_gain),"improvement_factor":sci(gain*inv(original_gain)),
        "legacy_report_two_front_50_active":sci(G(sum(old_alloc))*old_step),"legacy_classes":old_classes,
        "legacy_selection_only_factor":sci(old_step*inv(p**36)),
        "signed_l1_selector_ceiling_ratio":sci(active),"shared_SITE_exact_cases":len(cases),
        "example_logical_Toffoli_upper_bound":M,"bounded_services_failure_union_bound":sci(fail),
        "fixed_schedule_fallback_SC_bodies":10,"paid_full_Cost_minus_Info_selected":False,
        "full_geometric_program_replayed":False},indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
