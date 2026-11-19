"""One supplied Fourier128, real phase readout and nearest-edge energy. Python 3 + numpy."""
import cmath
from itertools import product
import json
import math

import numpy as np


def check(test, description):
    if not test:
        raise ValueError(description)


def char4(k, site):
    return (1, 1j, -1, -1j)[sum(x*y for x, y in zip(k, site)) % 4]


def primary_frame():
    axes = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    stencil = axes + [tuple(a-b for a, b in zip(axes[j], axes[i]))
                      for j in range(4) for i in range(j)]
    representatives = [k for k in product(range(4), repeat=4) if k < tuple(-x % 4 for x in k)]
    pairs = sorted(representatives, key=lambda k: (-sum(char4(k, u).real for u in stencil), k))[:64]
    check([sum(char4(k, u).real for k in pairs) for u in stencil] ==
          [20, 10, 10, 9, 8, 8, 6, 9, 5, 5], "wrong original ranking")
    return [f for k in pairs for f in (k, tuple(-x % 4 for x in k))]


def shear(t, a):
    lo = a & 1
    hi = (a >> 1) ^ (lo & (t & 1)) ^ ((t >> 1) & 1)
    return (hi << 1) | (lo ^ (t & 1))


def transverse_filter():
    survivors = []
    check(all(shear(t, a) == (t+a) % 4 for t, a in product(range(4), repeat=2)), "shear")
    for k in primary_frame():
        outcomes = []
        for t in range(4):
            amps = [0j, 0j]
            for a, b, c in product(range(4), repeat=3):
                aa = shear(t, a)
                sgn = (-1)**((aa >> 1) + (b & 1) + (c & 1))
                amps[aa & 1] += sgn*char4(k, (t, a, b, c))
            outcomes.append(amps)
        if any(outcomes[0]):
            check(all(x == outcomes[0] for x in outcomes), "retained carrier still depends on time")
            check(sum(abs(x)**2 for x in outcomes[0]) == 2048, "conditional five-Walsh mass")
            survivors.append(k)
        else:
            check(all(a == [0j, 0j] for a in outcomes), "accidental cancellation at time zero")
    check(survivors == [(1, 1, 2, 2), (3, 3, 2, 2)], "wrong transversely selected source pair")
    return survivors


def controlled_shift(t, head, power, bits):
    for q in range(bits-1, power, -1):
        if head and all((t >> z) & 1 for z in range(power, q)):
            t ^= 1 << q
    return t ^ (head << power)


def check_native_words():
    for bits in range(2, 8):
        n = 1 << bits
        for t, h, j in product(range(n), (0, 1), range(bits)):
            check(controlled_shift(t, h, j, bits) == (t+h*(1 << j)) % n, "controlled sum")
    n = 8
    J = np.array([[0., -1.], [1., 0.]])
    check(np.array_equal(J @ J, -np.eye(2)), "real quadrature unit")
    shift = np.roll(np.eye(n), 1, axis=0)
    wave = np.array([1., 2., -3., 1., 0., -1., 2., 3.])
    wave /= np.linalg.norm(wave)
    weights = abs(np.fft.fft(wave))**2/n
    sequence = [(0, 1), (1, 1), (0, 0), (2, 0), (1, 0)]
    total = 0.
    for signs in product((-1, 1), repeat=len(sequence)):
        state = np.kron(wave, [1., 0.])
        for (j, use_j), sign in zip(sequence, signs):
            word = np.kron(np.linalg.matrix_power(shift, 1 << j), J if use_j else np.eye(2))
            state = (state + sign*(word @ state))/2
        direct = np.dot(state, state)
        model = sum(weights[k]/2*math.prod(
            (1+out*(cmath.exp(1j*2*math.pi*k*(1 << j)/n) *
                       (1j*sigma if use_j else 1)).real)/2
            for (j, use_j), out in zip(sequence, signs))
                    for k in range(n) for sigma in (-1, 1))
        check(abs(direct-model) < 2e-14, "shared real phase-bit law")
        total += direct
    check(abs(total-1) < 2e-14, "missing reports")


def majority(p, copies):
    p = min(1., max(0., p))
    return sum(math.comb(copies, z)*p**z*(1-p)**(copies-z)
               for z in range(copies//2 + 1, copies+1))


def decoder_probability(k, out, bits, repeats):
    probability = 1.
    for i in range(bits):
        half = 1 << i
        period = 2*half
        lower = out % half
        # Ties are resolved to cosine using integer arithmetic.
        residue = (8*lower) % (4*period)
        use_cos = min(residue, 4*period-residue) <= period
        f = math.cos if use_cos else math.sin
        direction = 1 if f(2*math.pi*lower/period) >= 0 else -1
        mean = f(2*math.pi*(k % period)/period)
        sign = direction*(1 if out & half == 0 else -1)
        probability *= majority((1+sign*mean)/2, repeats)
    return probability


def confusion(bits, repeats):
    length = 1 << bits
    size = length//2 + 1
    P = np.zeros((size, size))
    for k in range(size):
        for out in range(length):
            prob = sum(decoder_probability(s*k, out, bits, repeats) for s in (-1, 1))/2
            P[k, min(out, length-out)] += prob
    check(np.max(abs(P.sum(axis=1)-1)) < 2e-13, "output law normalized")
    err = max(1-np.diag(P))
    check(err < bits*math.exp(-repeats/4) + 1e-14, "majority risk bound")
    return P, err


def eigenvalues(length):
    return np.array([4*length**2*math.sin(math.pi*k/length)**2 for k in range(length)])


def finite_energy(bits, repeats):
    n = 1 << bits
    lam = eigenvalues(n)
    P, risk = confusion(bits, repeats)
    tariff = np.linalg.solve(P, lam[:n//2+1])
    check(np.max(abs(P @ tariff-lam[:n//2+1])) < 1e-10, "exact linear calibration")
    t = 2*np.pi*np.arange(n)/n
    matter = np.stack((.17*np.cos(t)+.013*np.sin(3*t), .08*np.sin(2*t)+.007*np.cos(5*t)), axis=1)
    p = (math.sqrt(5)-1)/2
    filler = np.sqrt(p*p - np.sum(matter*matter, axis=1))
    check(np.allclose(p+filler*filler+np.sum(matter*matter, axis=1), 1), "CAR normalization")
    spec = np.sum(abs(np.fft.fft(matter, axis=0)/n)**2, axis=1)
    cls = np.bincount(np.minimum(np.arange(n), (-np.arange(n)) % n), spec)
    ready = .72
    g = 1/64
    paid_mass = ready*g*(cls @ P)
    total_price = np.dot(paid_mass, tariff/(ready*g))
    target = np.mean(np.sum((n*(np.roll(matter, -1, axis=0)-matter))**2, axis=1))
    second_energy = np.mean(np.sum((n**2*(np.roll(matter, -1, axis=0)
                                            -2*matter+np.roll(matter, 1, axis=0)))**2, axis=1))
    check(abs(total_price-target) < 2e-12 and abs(np.dot(lam*lam, spec)-second_energy)<2e-11,
          "DFT, two CARs, inactive and abort")
    approx = np.dot(cls @ P, lam[:n//2+1])
    check(abs(approx-target) < max(lam)*risk + 1e-12, "approximate tariff")
    if bits == 4:
        # All readouts are classical before pricing. A rounded payable tally may be tested on all rows.
        scores = np.r_[0., tariff/(ready*g)]
        masses = np.r_[1-sum(paid_mass), paid_mass]
        shift = max(0., -min(scores))
        scale = 29
        tickets = np.rint(scale*(scores+shift)).astype(np.int64)
        check(min(tickets) >= 0 and abs(masses @ tickets/scale - shift-target) <= .5/scale+1e-12,
              "rounded absolute slots including aborts")
    return {"L": n, "worst_misclassification": round(float(risk), 10),
            "nearest_energy": round(float(target), 10),
            "exact_calibrated_mean_including_abort": round(float(total_price), 10),
            "raw_decoder_bias": round(float(approx-target), 10),
            "second_moment_corrected_score_at_readiness_0.72":
                round(float(np.dot(paid_mass, (tariff/(ready*g))**2)), 7)}


def arbitrary_transverse():
    n = 32
    t = np.arange(n)/n
    # Two distinct transverse columns, with low- and high-temporal harmonics.
    cols = np.column_stack((.1*np.cos(2*np.pi*t)+.002*np.sin(22*np.pi*t),
                            .16*np.sin(4*np.pi*t)+.004*np.cos(18*np.pi*t)))
    lam = eigenvalues(n)
    weight = np.mean(abs(np.fft.fft(cols, axis=0)/n)**2, axis=1)
    folded = np.minimum(np.arange(n)%(n//4), (-np.arange(n))%(n//4))
    approx, exact = np.dot(weight, lam[folded]), np.dot(weight, lam)
    bound = np.dot(weight, lam*lam)/(4*n*n*math.sin(math.pi/8)**2)
    check(0 < exact-approx < bound, "positivity and quadratic alias estimate")
    # Every true RIGHT branch shifts the temporal spectrum by a multiple of n/4.
    for k in primary_frame():
        shifted = np.roll(weight, (n//4)*k[0])
        check(abs(np.dot(shifted, lam[folded])-approx) < 2e-13, "hidden temporal alias")
    return {"full_energy": round(float(exact), 10), "folded_nearest": round(float(approx), 10),
            "upper_bound_on_deficit": round(float(bound), 10)}


def entropy(probabilities):
    return -sum(z*math.log(z) for z in probabilities if z > 0.)


def contract(left, right):
    # Explicit small tensor contractions also work with BLAS backends that report sticky FP flags.
    return np.einsum("ij,j...->i...", left, right, optimize=False)


def weighted_walk():
    length, tickets = 8, 8
    thresholds = np.array([4, 6, 5, 4, 3, 2, 4, 4])
    dim = 2*tickets*length
    perm = np.zeros((dim, dim))
    embed = np.zeros((dim, length))
    for t, direction, z in product(range(length), range(2), range(tickets)):
        x = (t*2+direction)*tickets+z
        edge = t if direction == 0 else (t-1)%length
        if z < thresholds[edge]:
            dest = (t+(1 if direction == 0 else -1))%length
            y = (dest*2+1-direction)*tickets+z
        else:
            y = x
        perm[y, x] = 1
        embed[x, t] = 1/math.sqrt(2*tickets)
    check(np.array_equal(contract(perm, perm), np.eye(dim)), "physical step B is not an involution")
    diff = length*(np.roll(np.eye(length), -1, axis=0)-np.eye(length))
    laplacian = contract(diff.T, (thresholds/tickets)[:, None]*diff)
    check(np.max(abs(contract(embed.T, contract(perm, embed)) -
                     (np.eye(length)-laplacian/(2*length**2))))<1e-14, "compressed actual shifts")
    walk = contract(2*contract(embed, embed.T)-np.eye(dim), perm)
    hplus, hminus = (np.eye(dim)+walk)/2, (np.eye(dim)-walk)/2
    amps = .13*np.array([1., .5, -.3, -1., -.7, .5, -.4, 1.])/math.sqrt(length)
    target = amps @ laplacian @ amps
    energy2 = np.dot(laplacian @ amps, laplacian @ amps)
    eig, basis = np.linalg.eigh(laplacian)
    q = np.clip(eig/(4*length**2), 0., 1.)
    spectral_mass = (basis.T @ amps)**2
    risk_squares = (1/64)*(energy2+4*target)
    max_history_error = 0.
    for ones in product((0, 1), repeat=5):
        v = contract(embed, amps)
        for one in ones:
            v = contract(hminus if one else hplus, v)
        k = sum(ones)
        expected = spectral_mass @ (q**k*(1-q)**(5-k))
        max_history_error = max(max_history_error, abs(v @ v - expected))
    check(max_history_error < 1e-13, "unread mode and repeated measurements on one copy")
    # Actual retained-prefix example, including early caps, the five-sector and CAR residuals.
    M = length**2
    stops = [(0, .05), (9, .12), (29, .16), (M, .67)]
    activation = 1/64
    lambdabar = activation*target
    mean_count = second_raw = count_entropy = ordered_entropy = 0.
    for m, prob in stops:
        mass = np.array([activation*np.dot(spectral_mass, math.comb(m,k)*(q**k)*((1-q)**(m-k)))
                         for k in range(m+1)])
        mass[0] += 1 - activation*sum(spectral_mass)
        check(abs(sum(mass)-1)<3e-14, "lost abort or inactive sector")
        mean_count += prob*sum(k*f for k,f in enumerate(mass))
        second_raw += prob*sum((4*k)**2*f for k,f in enumerate(mass))
        count_entropy += prob*entropy(mass)
        ordered_entropy += prob*(entropy(mass)+sum(mass[k]*math.log(math.comb(m,k)) for k in range(m+1)))
    mean_coverage = sum(m*prob for m,prob in stops)/M
    check(abs(mean_count - mean_coverage*lambdabar/4) < 2e-15, "full retained-prefix source")
    check(second_raw <= risk_squares+1e-13, "second moment on actual histories")
    check(count_entropy <= ordered_entropy and ordered_entropy > 0, "lost order of rare recorded events")
    uniform = np.ones(length)
    cost_slope = -np.sum((diff@amps)**2*((thresholds/tickets)-.5))
    for eps in (.125, .25):
        w = thresholds/tickets-.5
        plus = np.dot(.5*uniform-eps*w, (diff@amps)**2)
        minus = np.dot(.5*uniform+eps*w, (diff@amps)**2)
        check(abs((plus-minus)/(2*eps)-cost_slope)<1e-14, "complemented geometric tangent")
    return {"L": length, "real_permutation_dimension": dim, "Ramsey_histories_length_5": 32,
            "nearest_weighted_energy": round(float(target), 12),
            "actual_prefix_mean_coverage": round(mean_coverage, 12),
            "excess_literal_length_with_aborts": round(float(mean_count), 12),
            "second_moment_four_counts": round(float(second_raw), 12),
            "second_moment_upper_bound": round(float(risk_squares), 12),
            "ordered_entropy_conditional_on_stop_nats": round(float(ordered_entropy), 12),
            "count_only_entropy_conditional_on_stop_nats": round(float(count_entropy), 12)}


def pure_wave_sources():
    length = 8
    t = np.arange(length)
    wave = np.cos(2*math.pi*t/length)
    wave /= np.linalg.norm(wave)
    diff = np.roll(np.eye(length), -1, axis=0)-np.eye(length)
    base = .5*contract(diff.T, diff)/4
    q = .5*math.sin(math.pi/length)**2
    wprime = np.array([1., -.25, .5, .75, 1., -.5, .25, .5])
    tangent = contract(diff.T, wprime[:,None]*diff)/4
    check(np.linalg.norm(contract(base, wave)-q*wave)<1e-14 and
          np.linalg.norm(contract(base,tangent)-contract(tangent,base))>.005,
          "noncommuting material perturbation")
    dq = wave @ contract(tangent, wave)
    ident = np.eye(length)
    observed_slope = 0.
    ell = math.log((1+math.sqrt(5))/2)
    for row in product((0, 1), repeat=5):
        value, slope = wave.copy(), np.zeros(length)
        for bit in row:
            oper, doper = (base, tangent) if bit else (ident-base,-tangent)
            slope, value = contract(oper,slope)+contract(doper,value), contract(oper,value)
        prob, dp = wave@value, wave@slope
        k = sum(row)
        check(abs(dp - prob*dq*(k/q-(len(row)-k)/(1-q))) < 2e-14,
              "ordered probability differential")
        observed_slope += dp*(k+(math.log(prob)+1)/ell)
    expected = 5*dq*(1+math.log(q/(1-q))/ell)
    check(abs(observed_slope-expected)<3e-14, "registered entropy source including every leaf")
    rows = []
    for L in (16, 256, 4096, 1048576):
        ql = .5*math.sin(math.pi/L)**2
        # ratio of complemented, log-M-normalized derivative to its positive limiting coefficient.
        ratio = -(ell+math.log(ql/(1-ql)))/math.log(L**2)
        rows.append({"L":L, "ratio_to_positive_asymptotic_gain":round(ratio,8)})
    check(all(a["ratio_to_positive_asymptotic_gain"] < b["ratio_to_positive_asymptotic_gain"]
              for a,b in zip(rows,rows[1:])) and .92 < rows[-1]["ratio_to_positive_asymptotic_gain"] < 1,
          "finite-graph gain on increasing periods")
    return {"noncommuting_ordered_leaf_differential":round(observed_slope,12),
            "one_frequency_complemented_gain":rows}


def main():
    pair = transverse_filter()
    check_native_words()
    rows = [finite_energy(bits, 9) for bits in (3, 4, 5)]
    print(json.dumps({"frame_survivors": pair, "factor": "1/64", "native_Ramsey_branches_checked": 32,
                      "weighted_native_walk": weighted_walk(), "genuine_single_mode_tangent": pure_wave_sources(), "finite_grid_confusion_9": rows, "arbitrary_transverse": arbitrary_transverse(),
                      "full_Book_price_identified": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
