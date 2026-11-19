"""Source-free replay of two equal-inventory slots inside the literal NPS2 reader.

Python 3 standard library. Matrices have integer entries in the power basis
1,a,a^2,a^3 with a=sqrt(p) and a^4+a^2=1. All output intervals use Fractions.
"""
from collections import Counter
from fractions import Fraction as F
import json


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


O = (0, 0, 0, 0)
I = (1, 0, 0, 0)
A = (0, 1, 0, 0)
P = (0, 0, 1, 0)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def times(a, b):
    out = [0]*7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    for n in (6, 5, 4):
        out[n-4] += out[n]
        out[n-2] -= out[n]
    return tuple(out[:4])


def power(a, n):
    out = I
    for _ in range(n):
        out = times(out, a)
    return out


def scale(a, n):
    return tuple(n*x for x in a)


def add_term(out, idx, value):
    out[idx] = add(out.get(idx, O), value)
    if out[idx] == O:
        del out[idx]


def roots():
    lo, hi = F(0), F(1)
    for _ in range(224):
        mid = (lo+hi)/2
        if mid**4+mid**2 < 1:
            lo = mid
        else:
            hi = mid
    return lo, hi


AL, AH = roots()
Z = F(1, 2**20)


def enclosure(value):
    l = sum(min(c*AL**i, c*AH**i) for i, c in enumerate(value))
    h = sum(max(c*AL**i, c*AH**i) for i, c in enumerate(value))
    return l, h


def endpoints(pair, places=22):
    den = 10**places
    def fmt(n):
        sign = "-" if n < 0 else ""
        a, b = divmod(abs(n), den)
        return f"{sign}{a}.{b:0{places}d}"
    lo, hi = pair
    return [fmt((lo*den).__floor__()), fmt((hi*den).__ceil__())]


def sub_interval(left, right):
    return (left[0]-right[1], left[1]-right[0])


def phi_j(m):
    lo, hi = enclosure(m)
    need(0 <= lo and hi <= 1, "prefix mass")
    dl, dh = Z*(1-hi), Z*(1-lo)
    # -4 log(1-d) for the four original protected Spin columns.
    def terms(x):
        return 4*sum(x**k/k for k in range(1, 5))
    return terms(dl), terms(dh)+4*dh**5/(5*(1-dh))


def jump(cold, x=I):
    before, after = (times(x, times(c, c)) for c in cold)
    return sub_interval(phi_j(after), phi_j(before))


def cx(control, target):
    return ("CX", control, target)


BANK, C = cx(3, 2), cx(2, 4)
W, W_REV = cx(3, 5), cx(5, 3)
G, S = ("G", 5), ("SourceI", 2, 0, 1)
swap = [cx(2, 5), cx(5, 2), cx(2, 5)]
zt = swap+[S, S]+swap
idle, forward, backward = [G]+zt+[G]+zt, [G, G]+zt+zt, zt+[G, G]+zt
CX_RT = cx(4, 5)
original_suffix = [S, S, BANK, CX_RT, G, CX_RT]


def execute(state, gates):
    for gate in gates:
        out = {}
        for k, val in state.items():
            if gate[0] == "CX":
                ctrl, dest = gate[1:]
                idx = k^((((k>>(5-ctrl))&1))<<(5-dest))
                add_term(out, idx, val)
            elif gate == S:
                enabled = bool(k & 8)
                idx = k^(16 if enabled else 0)
                add_term(out, idx, scale(val, -1 if enabled and k&16 else 1))
            elif gate == G:
                add_term(out, k, times(A, val))
                add_term(out, k^1, scale(times(P, val), -1 if k&1 else 1))
            else:
                raise ValueError(gate)
        state = out
    return state


def birth(spin):
    return {(spin<<4)|w: times(power(A, 4-bin(w).count("1")), power(P, bin(w).count("1")))
            for w in range(16)}


BIRTH = [birth(i) for i in range(4)]


def compress(word):
    cold = []
    for j, state in enumerate(BIRTH):
        v = execute(state, word)
        col = [O]*4
        for i, vect in enumerate(BIRTH):
            for k, x in vect.items():
                col[i] = add(col[i], times(x, v.get(k, O)))
        need(all(col[i] == O for i in range(4) if i != j), "all input off-diagonals")
        cold.append(col[j])
    need(len(set(cold)) == 1, "all input diagonal entries agree")
    return cold[0]


def check_full(words):
    bare = [BANK, C]+original_suffix
    for k in range(64):
        col = {k:I}
        ref = execute(col, bare)
        need(all(execute(col, [BANK]+word+original_suffix) == ref for word in words),
             "exact original endpoint on every dirty column including unknown Spin")


def check_short():
    slots = ([W, C, W, W_REV, W_REV], [W_REV, C, W_REV, W, W])
    need(Counter(slots[0]) == Counter(slots[1]) and slots[0][1] == slots[1][1] == C,
         "same address inventory and copy tick")
    check_full(slots)
    cold = [(compress([BANK, slot[0]]), compress([BANK, slot[0], C])) for slot in slots]
    first, second = (jump(c) for c in cold)
    contrast = sub_interval(first, second)
    need(contrast[1] < 0, "different closed prefix prices at identical local copy")
    return {"expanded_slot_length":5, "copy_tick_within_slot_one_based":2,
            "exact_cold_before_after_W":cold[0], "exact_cold_before_after_W_reverse":cold[1],
            "delta_J_W":endpoints(first), "delta_J_W_reverse":endpoints(second),
            "difference_W_minus_W_reverse":endpoints(contrast)}


def check_source():
    # Endpoints of the three native cells are I, G_t^2 and G_t^-2.
    for cell in (idle, forward, backward):
        need(len(cell) == 18 and Counter(cell) == Counter(idle), "native cell address inventory")
    for k in range(64):
        col = {k:I}
        need(execute(col, zt) == {k:scale(I, -1 if k&1 else 1)}, "routed true Z on t")
        need(execute(col, idle) == col, "positive native identity")
        need(execute(col, forward) == execute(col, [G, G]), "native positive two-step")
        need(execute(col, forward+backward) == col, "inverse on every column")
    # Use the actual same fixed budget at n=0,1,2. Beyond this witness the
    # all-column cell identities above prove the result for every finite N.
    cap = 2
    slots = []
    for n in range(cap+1):
        pre = forward*n + idle*(cap-n)
        post = backward*n + idle*(cap-n)
        slots.append(pre+[C]+post)
    check_full(slots)
    need(all(Counter(slot) == Counter(slots[0]) and slot[18*cap] == C for slot in slots),
         "all materialized tilted words fix the inventory and the tick of C")
    cold = (compress([BANK]), compress([BANK, C]))
    eta = scale(times(A, P), 2)
    cb = add(P, times(power(P, 2), eta))
    ca = add(times(P, cb), times(times(power(P, 2), times(A, P)), add(I, eta)))
    need(cold == (cb, ca), "separate literal bank contraction by values of b,e")
    for n, slot in enumerate(slots):
        amplitude = compress(slot[:18*cap])
        need(compress([BANK]+slot[:18*cap]) == times(cb, amplitude) and
             compress([BANK]+slot[:18*cap+1]) == times(ca, amplitude),
             "both proper prefix contractions pick up the actual tail factor")
        if n == 1:
            need(amplitude == power(P, 3), "cos(2 theta)=p^3")
    mb, ma = times(cb, cb), times(ca, ca)
    ml, mh = enclosure(add(mb, scale(ma, -1)))
    need(ml > 0, "strict positive source on literal rank-four reader")
    slope = (4*Z*(1-Z)*ml, 4*Z*mh/(1-Z))
    x1 = power(P, 6)
    x1l, x1h = enclosure(x1)
    genuine = sub_interval(jump(cold), jump(cold, x1))
    secant = (genuine[0]/(1-x1l), genuine[1]/(1-x1h))
    need(slope[0] < secant[0] < secant[1] < slope[1], "actual finite secant inside universal derivative range")
    return {"ordinary_cold_before_after":cold, "expanded_per_cell":len(idle),
            "slot_length_at_N":"36*N+1", "address_multiplicities_per_cell":
               {"G_t":2, "CX(e,t)":8, "CX(t,e)":4, "SourceI_e":4},
            "full_endpoint_tested_n_at_N2":[0,1,2], "direct_CX_slot_tick_at_N2_one_based":37,
            "ordinary_J_increment":endpoints(jump(cold)),
            "J_increment_at_single_rotated_pair_x_equals_p6":endpoints(jump(cold, x1)),
            "certified_global_derivative_enclosure":endpoints(slope),
            "native_secant_slope_between_1_and_p6":endpoints(secant)}


GRID = 10**43


def box(lo, hi=None):
    if hi is None:
        hi = lo
    return (F((lo*GRID).__floor__(), GRID), F((hi*GRID).__ceil__(), GRID))


def plus(left, right):
    return box(left[0]+right[0], left[1]+right[1])


def minus(left, right):
    return box(left[0]-right[1], left[1]-right[0])


def mul(left, right):
    vals = [x*y for x in left for y in right]
    return box(min(vals), max(vals))


def ratio(left, right):
    need(right[0] > 0, "division by positive interval")
    return mul(left, box(1/right[1], 1/right[0]))


def geometric_loader():
    # Actual SC6 labels accept exactly the common exponent 512.  Compute
    # Goldens on the complete two-column rotation by nine certified doublings.
    a, p = box(*enclosure(A)), box(*enclosure(P))
    co, si = a, p
    two, one, z = box(2), box(1), box(Z)
    for _ in range(9):
        co, si = minus(mul(co, co), mul(si, si)), mul(two, mul(co, si))
    lam = mul(si, si)
    eta = mul(two, mul(a, p))
    u = ratio(plus(mul(a, minus(co, one)), mul(p, si)), lam)
    v = ratio(plus(mul(a, minus(co, one)), mul(eta, mul(p, si))), lam)
    x0 = box(*enclosure(power(P, 6)))
    m0 = minus(one, z)
    need(si[0]>0 and v[1]<u[0] and u[1]<0, "sign of both actual slope coefficients")
    source_gap = plus(a, mul(box(F(1, 2)), plus(u, v)))
    need(source_gap[0] > 0, "uniform positivity over Q in [0,1/2]")
    prefactor = mul(box(4), mul(z, mul(m0, minus(one, x0))))
    floor = mul(two, mul(prefactor, mul(minus(u, v), source_gap)))
    need(floor[0] > 0, "strict positive full-interval slope floor")
    pi = mul(box(4), box(*enclosure(power(P, 7))))
    q0 = mul(lam, pi)
    report = plus(box(*enclosure(power(P, 2))), mul(box(*enclosure(power(P, 3))), q0))

    def marked_slope(c, k):
        mass = mul(c, c)
        dm = mul(two, mul(c, k))
        h1 = plus(m0, mul(z, mass))
        h0 = plus(m0, mul(z, mul(x0, mass)))
        return ratio(dm, mul(h1, h0))
    before, after = (plus(a, mul(k, q0)) for k in (u, v))
    source = mul(prefactor, minus(marked_slope(before, u), marked_slope(after, v)))
    need(source[0] > floor[1] and after[1]<before[0] and after[0]>0,
         "actual PC13 centre source and strict prefix contrast")
    relative = ratio(after, before)
    crossing = mul(relative, relative)
    inverse = ratio(mul(a, minus(one, relative)), minus(mul(relative, u), v))
    need(0 < crossing[0] < crossing[1] < 1 and inverse[0] <= q0[0] <= q0[1] <= inverse[1],
         "unique interior old-independent crossing and inverse")
    # Use a strictly nonscalar, nondiagonal contraction C_old. The common
    # determinant polynomial is det(d0 I + z y C_old^t C_old) for all y.
    old = ((F(1,2), F(1,4)), (F(0), F(1,3)))
    gram = [[sum(old[k][i]*old[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]
    tr = gram[0][0]+gram[1][1]
    det = gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    need(gram[0][1] != 0 and 0 < det < tr < 1, "nonscalar old contraction")
    def old_det(y):
        return (1-Z)**2 + Z*(1-Z)*tr*y + Z**2*det*y*y
    b, d = F(4,5), F(3,5)
    x = (d/b)**2
    need(old_det(x*b*b) == old_det(d*d) and
         old_det((x-F(1,100))*b*b) < old_det(d*d) < old_det((x+F(1,100))*b*b),
         "exact equality and strict bracket without diagonalization of old archive")
    return {"required_interface":"current fresh canonical bank; R_load uncomputes on accessible bank wires and fixes e,r,t at its completed boundary; exact 512 acceptance rotation",
            "comparator":"R_load* before CX and R_load after CX, plus the balanced tail cells",
            "cos512":endpoints(co), "sin512":endpoints(si), "Q0_equals_4_lambda_p7":endpoints(q0),
            "q0_report_equals_p2_plus_p3_Q0":endpoints(report),
            "cold_before_after_at_PC13":[endpoints(before),endpoints(after)],
            "linear_in_Q_slope_before":endpoints(u), "linear_in_Q_slope_after":endpoints(v),
            "positive_floor_for_dQ_of_J_jump_contrast_Q_zero_to_half":endpoints(floor),
            "dQ_of_J_jump_contrast_at_PC13":endpoints(source),
            "old_independent_prefix_order_crossing_X_before_equals_X_after_1":endpoints(crossing),
            "old_independent_recovered_Q":endpoints(inverse),
            "same_execution_field_row":"multiply d/dQ by the actual D_Y Q, with all genuine gain/right-lift restrictions; it may vanish at a stationary field"}


def main():
    return {"schema":"d0.native-prefix-cx/1", "status":"PASS",
            "ring_basis":["1","a","a^2","a^3"], "relation":"a^4=1-a^2; a>0",
            "true_z":"2^-20", "original_native_word_length":8,
            "six_wire_order":["Spin0","Spin1","e","b","r","t"],
            "true_born_rank":4,"full_square_columns":64,
            "short_spectator_comparison":check_short(), "one_tail_source":check_source(),
            "literal_512_rotation_with_paid_loader_uncompute":geometric_loader(),
            "bounds_scope":"closed feedback action of each truncated prefix regarded as a complete circuit; endpoint equality compares histories of the same fixed padded length",
            "intermediate_marks_equal":False, "microscopic_edge_cost_identified":False,
            "einstein_source_identified":False}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
