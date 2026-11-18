"""Verify the two same-clock marks against the full native port payment and a parsed token.

Run beside master_mark_result.json with Python 3.9+ and NumPy.
The output combines analytical identities with matrix/finite-round numerical checks.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np


P = (math.sqrt(5.0) - 1.0) / 2.0
ELL = -math.log(P)
BETA = 2 * P**2
ZETA = 2.0**-20
RANK = 4
DIM = 16


def close(actual, expected, label, tolerance=4e-13):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    if not math.isfinite(error) or error > tolerance:
        raise ArithmeticError(f"{label}: discrepancy {error:g}")


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def adjoint(matrix):
    return np.swapaxes(matrix.conj(), -1, -2)


def mul(left, right):
    return np.einsum("...ij,...jk->...ik", left, right, optimize=False)


def full_port():
    """The §7gb creation operators, 64 Walsh rows and 128 NT1 Kraus labels."""
    eye = np.eye(DIM, dtype=complex)
    order = (0, 2, 3, 1)
    phases = (1j, 1j, -1, -1j)
    columns = []
    for mode, phase in enumerate(phases):
        creator = np.zeros_like(eye)
        previous = order[:order.index(mode)]
        for old in range(DIM):
            if not (old >> mode) & 1:
                creator[old | (1 << mode), old] = (-1)**sum((old >> j) & 1 for j in previous)
        # Times 5, both Julia-root columns and the original creator are Gaussian integers.
        base = 3 * creator
        projection = mul(creator, adjoint(creator))
        left, right = 5*eye-projection, 4*eye+projection
        tagged = phase*base
        for pair in ((tagged, left), (adjoint(tagged), right), (-base, -left),
                     (-adjoint(base), -right)):
            columns.extend((pair, pair))
    walsh = np.array([[(-1)**bin(j & n).count("1") for j in range(32)]
                      for n in range(32)])
    numer = np.einsum("lj,jbxy->lbxy", walsh, np.asarray(columns)).reshape(64,DIM,DIM)
    rows = numer/160
    close(np.sum(mul(adjoint(rows),rows), axis=0), eye, "complete Walsh Parseval")
    close(np.sum(mul(rows,adjoint(rows)), axis=0), eye, "second Parseval")
    a = rows[0]
    close(mul(adjoint(a),a), (9/640)*eye, "original scalar section")
    branch = mul(adjoint(rows),a)
    even, odd = -2*P**2*branch, -2*P*math.sqrt(P)*branch
    even[0] += eye
    q = 4*P**3*(9/640)
    close(np.sum(mul(adjoint(odd),odd),axis=0), q*eye, "all odd ports")
    close(np.sum(mul(adjoint(even),even),axis=0), (1-q)*eye, "all even ports")
    # Each label is a nonzero scalar times the indicated Gaussian-integer operator.
    # The distinguished even0 is a nonzero multiple of I since Lambda=(9/640)I.
    raw_pattern = mul(adjoint(numer),numer[0])
    support = np.repeat(raw_pattern, 2, axis=0)
    support[0] = eye
    largest = np.max(abs(support.real)) + np.max(abs(support.imag))
    require(DIM*largest**2 < 2**52, "Gaussian-integer pair support fits exactly in double mantissas")
    return even, odd, support, q


def port_effects(even, odd, k):
    """Dynamic sum over all labels, grouped only by number of costly ports.

    Every bin is a complete effect on initial DATA, so no memory reset or
    factorization of the 64 addresses is used in this calculation.
    """
    eye = np.eye(DIM)
    current = [eye]
    for _ in range(k):
        nxt = [np.zeros((DIM,DIM),dtype=complex) for _ in range(len(current)+1)]
        for ones, effect in enumerate(current):
            nxt[ones] += np.sum(mul(mul(adjoint(even),effect),even), axis=0)
            nxt[ones+1] += np.sum(mul(mul(adjoint(odd),effect),odd), axis=0)
        current = nxt
    close(sum(current), eye, "all unweighted final labels")
    return current


def deterministic_token():
    a = math.sqrt(P)
    golden = np.array([[a, -P], [P, a]])
    zero = np.array([1., 0.])
    born = golden @ zero
    spin_i = np.kron(np.eye(2), np.array([[0.,-1.],[1.,0.]]))
    source_i = np.block([[np.eye(4), np.zeros((4,4))],[np.zeros((4,4)), spin_i]])
    z = source_i @ source_i
    close(z, np.kron(np.diag([1.,-1.]), np.eye(4)), "physical SourceI squared")
    reset = z @ np.kron(golden,np.eye(4)) @ z
    close(reset, np.kron(golden.T,np.eye(4)), "paid Golden inverse on all columns")
    close(reset @ np.kron(born[:,None],np.eye(4)), np.kron(zero[:,None],np.eye(4)),
          "known zero with arbitrary original Spin")
    cx = np.eye(4)[[0,1,3,2]]
    writer = cx @ np.kron(np.eye(2),golden) @ cx
    out = writer @ np.kron(zero,born)
    close(out, np.kron(zero,golden@born), "NC1 retains a pure unread tail")
    close(writer @ np.kron(np.array([0.,1.]),born), [0,0,1,0], "complementary legal 10")
    parsed = np.array([np.sum(abs(out[:2])**2), abs(out[2])**2, abs(out[3])**2])
    close(parsed, [1,0,0], "0, 10 and invalid 11 sectors")
    selection_information = -math.fsum(v*math.log(v)/ELL for v in parsed if v>0)
    close(selection_information, 0, "no selection information for the deterministic report")
    close(parsed[0]+2*parsed[1]-selection_information,1,"net parsed charge at zero")
    return dict(parsed_probabilities=[1,0,0], unread_tail_probabilities=(abs(out[:2])**2).tolist(),
                parsed_length=1, selection_information=0, net_terminal_weight=P)


def conditional_after_first_failure(b, exponent):
    """Remaining success conditional on a failed first Bernoulli draw."""
    return 1 + math.expm1(exponent*math.log(b))/(1-b)


def real_mask_law(model):
    """All 64 prequery masks and their exact conditional success formulas."""
    dimension = model["clock_dimension"]
    trace = model["absolute_heat"]
    beta_envelope = math.exp(BETA/5)
    a, d = 359-66*beta_envelope, 132*beta_envelope
    heat = a*dimension/trace
    heat_probe = (trace/dimension-a)/d
    alpha = ELL/BETA
    n = math.floor(RANK*BETA)
    delta = RANK*BETA - n
    b = 1-ZETA+ZETA*model["s"]
    master = heat*b**(RANK*BETA)
    close(master, model["marked_probability_identity"], "first marked event")
    rest_feedback = conditional_after_first_failure(b, delta)
    rest_outer = conditional_after_first_failure(master, alpha)
    flags = [(a*dimension)**-alpha, a/(a+d)] + [1-ZETA]*(n+1)
    masks = []
    for bits in itertools.product((False,True), repeat=len(flags)):
        old_prob = math.prod(u if bit else 1-u for bit,u in zip(bits,flags))
        first_heat = 1. if bits[1] else (1-heat_probe)*heat
        mandatory = math.prod(1. if bit else model["s"] for bit in bits[2:2+n])
        first_draw = 1. if bits[-1] else model["s"]
        first_feedback = first_draw+(1-first_draw)*rest_feedback
        first_master = first_heat*mandatory*first_feedback
        success = first_master+(1-first_master)*rest_outer if bits[0] else 0.
        masks.append((bits,old_prob,success))
    close(math.fsum(m[1] for m in masks), 1., "complete ordinary mask law")
    close(masks[-1][2], 1., "all-bypass mask guarantees a mark")
    g = math.fsum(prob*success for _,prob,success in masks)
    close(g, math.exp(-ELL*model["B"]), "golden master mark", 1e-16)
    close(g, model["golden_weight"], "supplied master mark receipt", 1e-16)
    return masks, g


def suffix_count(mu, anchor):
    k = 1
    while mu**k >= anchor:
        k += 1
    return k


def all_leaves(masks, g, mu, suffix_mass):
    anchor = masks[-1][1]
    require(0<suffix_mass<anchor<g<1, "strict anchor and common support")
    original = g+(1-g)*suffix_mass
    new_probs = [(prob - (suffix_mass if all(bits) else 0))/(1-suffix_mass)
                 for bits,prob,_ in masks]
    require(all(prob>0 for prob in new_probs), "all original masks remain")
    close(math.fsum(new_probs), 1, "retuned probability")
    # Pay the complete suffix only on a failed mark; sum both outcomes at each mask.
    new_Z = math.fsum(prob*(success+(1-success)*suffix_mass)
                      for prob,(_,_,success) in zip(new_probs,masks))
    close(new_Z, g, "absolute retuned all-leaf moment", 5e-16)
    v = 1 - suffix_mass/anchor
    m = suffix_count(mu, v)
    long_prob = (1-v)/(1-mu**m)
    close(1-long_prob+long_prob*mu**m, v, "baseline payment mask")
    baseline_Z = (g-anchor)+anchor*(1-long_prob+long_prob*mu**m)+(1-g)*suffix_mass
    close(baseline_Z, (1-suffix_mass)*g, "one-shot baseline with field-constant gain")
    cap = 3
    surviving, repeated_sum = 1., 0.
    for _ in range(cap):
        repeated_sum += surviving*((g-suffix_mass)+(1-g)*suffix_mass)
        surviving *= suffix_mass
    capped_Z = repeated_sum+surviving*suffix_mass
    close(capped_Z, g-(g-suffix_mass)*suffix_mass**cap, "true timeout sent to negative suffix")
    return dict(mask_count=len(masks), anchor=anchor, suffix_mass=suffix_mass,
                unadjusted_moment=original, one_shot_baseline_moment=baseline_Z,
                baseline_long_visits=m, baseline_long_probability=long_prob,
                retuned_all_leaf_moment=new_Z, reconstructed_B=-math.log(new_Z)/ELL,
                repeated_cap=cap, timeout_born_mass=surviving, capped_moment=capped_Z,
                cap_error_bound=suffix_mass**cap)


def surprisal_control(even, odd, integer_patterns):
    """Two actual origin visits. Retain every reachable ordered fine pair."""
    letters = np.stack((even,odd),axis=1).reshape(128,DIM,DIM)
    mixed = np.eye(DIM)/DIM
    states = [mixed, (mixed+np.diag([1]+[0]*(DIM-1)))/2]
    positive_sets, answers, plain, probability_vectors = [], [], [], []
    for rho in states:
        # Faithful inputs make a pair positive iff the composed Kraus operator is nonzero.
        support, normalized, weighted, cancelled = [], [], [], []
        for first,k1 in enumerate(letters):
            products = mul(letters,k1)
            composed_patterns = mul(integer_patterns,integer_patterns[first])
            weights = np.trace(mul(mul(products,rho),adjoint(products)),axis1=1,axis2=2).real
            for second,pattern in enumerate(composed_patterns):
                if not np.any(pattern):
                    continue
                prob = float(weights[second])
                require(prob>0, "positive probability on fine support")
                charge = 2+(first%2)+(second%2)
                info = -math.log(prob)/ELL
                support.append((first,second,charge))
                normalized.append(prob)
                weighted.append(prob*P**charge)
                cancelled.append(prob*math.exp(-ELL*(charge-info)))
        close(math.fsum(normalized), 1., "fine pair normalization")
        absolute = math.fsum(P**depth for _,_,depth in support)
        close(math.fsum(cancelled), absolute, "full fine support cancels its surprisal", 2e-11)
        positive_sets.append(support)
        probability_vectors.append(np.asarray(normalized))
        answers.append(math.fsum(cancelled))
        plain.append(math.fsum(weighted))
    require(positive_sets[0]==positive_sets[1], "fixed actual two-visit support")
    close(answers[0],answers[1], "two distinct faithful inputs")
    change = np.linalg.norm(probability_vectors[0]-probability_vectors[1],ord=1)
    require(change>1e-8, "actual fine probabilities changed on the fixed support")
    counts = [sum((a%2,b%2)==pair for a,b,_ in positive_sets[0])
              for pair in itertools.product((0,1),repeat=2)]
    require(counts==[441]*4, "exact positive fine support by both port symbols")
    return dict(ordered_slots=128**2, positive_ordered_fine_leaves=len(positive_sets[0]),
                l1_change_of_born_fine_probabilities=float(change), born_moment_without_path_information=plain,
                positive_fine_counts_for_00_01_10_11=counts, exact_surprisal_sum="441*(p+p^2)^2=441",
                moment_with_own_fine_surprisal=answers,
                direct_sum_on_support=math.fsum(P**depth for _,_,depth in positive_sets[0]))


def main():
    with Path(__file__).with_name("master_mark_result.json").open() as stream:
        source = json.load(stream)
    require(source["result"]=="PASS" and len(source["models"])==2, "two source master receipts")
    even, odd, integer_patterns, q = full_port()
    mu = P*(1-q)+P**2*q
    close(mu,P-4*P**6*(9/640),"actual NT3 mass")
    rows = []
    for model in source["models"]:
        masks, g = real_mask_law(model)
        anchor = masks[-1][1]
        k = suffix_count(mu,anchor)
        bins = port_effects(even,odd,k)
        for j,effect in enumerate(bins):
            close(effect, math.comb(k,j)*q**j*(1-q)**(k-j)*np.eye(DIM), "actual port-count effect")
        folded = sum(effect*(P**(k+j)) for j,effect in enumerate(bins))
        close(folded, mu**k*np.eye(DIM), "full marked NT3 power")
        nt3 = all_leaves(masks,g,mu,float(folded.trace().real/DIM))
        count = suffix_count(P,anchor)
        token = all_leaves(masks,g,P,P**count)
        close(nt3["reconstructed_B"], model["B"], "NT3 full B")
        close(token["reconstructed_B"], model["B"], "deterministic-token full B")
        rows.append(dict(native_word=model["native_word"], B=model["B"], golden_weight=g,
                         port_visits=k, all_port_suffix_slots=str(128**k), native_port=nt3,
                         independent_deterministic_tokens=count, deterministic_token=token))
    delta = rows[0]["B"]-rows[1]["B"]
    require(delta>19e-9, "source contrast")
    for kind in ("native_port","deterministic_token"):
        close(rows[0][kind]["reconstructed_B"]-rows[1][kind]["reconstructed_B"],
              delta, "reconstructed true two-word contrast", 2e-14)
    return dict(result="PASS", original_port_slots=128, port_click_probability=q,
                native_port_mass=mu, deterministic_writer=deterministic_token(),
                models=rows, delta_B=delta, full_support_surprisal=surprisal_control(even,odd,integer_patterns),
                physical_complete_Cost_Info_binding_proved=False, GR_closed=False)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, allow_nan=False))
