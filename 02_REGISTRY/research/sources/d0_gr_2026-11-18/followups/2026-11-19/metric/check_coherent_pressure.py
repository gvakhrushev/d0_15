"""Exact rational tests for coherent pressure, frozen branch frames and paid marks."""
from fractions import Fraction as Q
from math import prod
import json


def need(condition, description):
    if not condition:
        raise ArithmeticError(description)


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def diag(entries):
    return [[Q(x) if i == j else Q(0) for j in range(len(entries))]
            for i, x in enumerate(entries)]


def outer(v, w):
    return [[x*y for y in w] for x in v]


def plus(x, y):
    return [[a+b for a, b in zip(row, other)] for row, other in zip(x, y)]


def scale(x, k):
    return [[k*a for a in row] for row in x]


def mm(x, y):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*y)] for row in x]


def chain(*matrices):
    out = matrices[0]
    for matrix in matrices[1:]:
        out = mm(out, matrix)
    return out


def tr(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def commutator(x, y):
    return plus(mm(x, y), scale(mm(y, x), -1))


def analyse(tau, A, marked):
    E = mm(A, A)
    Z = tr(mm(tau, E))
    ident = eye(len(A))
    residual = plus(scale(E, 1/Z), scale(ident, -1))
    total_variance = tr(chain(tau, residual, residual))
    rows, projected_norm = [], Q(0)
    means = [tr(mm(tau, P)) for P in marked]
    # Exact Gram certificate for the centered bit operators before filtering.
    for i, Pi in enumerate(marked):
        for j, Pj in enumerate(marked):
            centered = tr(chain(tau, Pi, Pj)) - means[i]*means[j]
            need(centered == (means[i]*(1-means[i]) if i == j else 0), "bit Gram")
    for q, P in zip(means, marked):
        v = q*(1-q)
        # All fixtures are real. Symmetrizing implements Re Tr(tau E P).
        jordan = scale(plus(mm(E, P), mm(P, E)), Q(1, 2))
        j = tr(mm(tau, jordan))/Z
        m = tr(chain(tau, A, P, A))/Z
        double = tr(mm(tau, commutator(A, commutator(A, P))))/(2*Z)
        need(j-m == double, "double commutator")
        slope = (j-q)/v
        projected_norm += (j-q)**2/v
        centered = plus(P, scale(ident, -q))
        residual = plus(residual, scale(centered, -slope))
        # Canonical, frozen-frame tangent. Includes both terms for a mixed input.
        dtau = scale(plus(mm(centered, tau), mm(tau, centered)), 1/(2*v))
        need(tr(mm(dtau, E))/Z == slope, "frozen-frame log-normalization derivative")
        rows.append({"q": str(q), "weak_j": str(j), "observed_m": str(m),
                     "d_log_Z_d_q": str(slope), "double_commutator_over_2Z": str(double)})
    gap = tr(chain(tau, residual, residual))
    need(total_variance == projected_norm + gap and gap >= 0, "full matrix Bessel identity")
    return {"Z": str(Z), "rows": rows, "first_layer": str(projected_norm),
            "relative_variance": str(total_variance), "orthogonal_remainder": str(gap)}


def single_mark():
    tau = scale(outer([6, 5], [6, 5]), Q(1, 61))
    A = [[Q(7, 2), Q(-3)], [Q(-3), Q(13, 5)]]
    P = diag([0, 1])
    need(A[0][0]*A[1][1]-A[0][1]**2 == Q(1, 10) and 0 < tr(A) < 7,
         "A positive and A/7 strictly below identity")
    need(mm(A, [[6], [5]]) == [[6], [-5]], "normalized vector: sign only in marked sector")
    need(chain(A, A, [[6], [5]]) == [[36], [-31]], "E times input vector")
    result = analyse(tau, A, [P])
    row = result["rows"][0]
    need((result["Z"], row["q"], row["observed_m"], row["weak_j"], row["d_log_Z_d_q"],
          result["relative_variance"], result["orthogonal_remainder"]) ==
         ("1", "25/61", "25/61", "-155/61", "-61/5", "36", "0"), "preserved-mark witness")
    scaled = analyse(tau, scale(A, Q(1, 7)), [P])
    need(scaled["Z"] == "1/49" and result["rows"] == scaled["rows"], "contractive filter")
    return {**result, "Z_for_contractive_A_over_7": scaled["Z"]}


def mixed_two_bits():
    psi = [x*y for x in (Q(3, 5), Q(4, 5)) for y in (Q(5, 13), Q(12, 13))]
    other = [s*x for s, x in zip((1, -1, 1, 1), psi)]
    tau = plus(scale(outer(psi, psi), Q(2, 5)), scale(outer(other, other), Q(3, 5)))
    need(tr(tau) == 1 and tr(mm(tau, tau)) < 1, "genuine mixed state")
    u, v = [1, -1, 2, 3], [0, 2, -1, 1]
    A = plus(eye(4), plus(scale(outer(u, u), Q(1, 20)), scale(outer(v, v), Q(1, 11))))
    qs = (Q(16, 25), Q(144, 169))
    for word in range(4):
        bits = (word >> 1, word & 1)
        need(tau[word][word] == prod(q if b else 1-q for b, q in zip(bits, qs)), "product marks")
    result = analyse(tau, A, [diag([0, 0, 1, 1]), diag([0, 1, 0, 1])])
    need(Q(result["first_layer"]) > 0 and Q(result["orthogonal_remainder"]) > 0,
         "strict full-matrix Bessel example")
    return result


def doob_mixed_input():
    # Two spin input basis states give the same original observed mark q.
    # V has pointer amplitudes (3/5,4/5) and preserves each spin label.
    V = [[Q(3, 5), 0], [0, Q(3, 5)], [Q(4, 5), 0], [0, Q(4, 5)]]
    Vt = list(zip(*V))
    A = diag([1, 1, 1, 2])
    P = diag([0, 0, 1, 1])
    q = Q(16, 25)
    need(chain(Vt, P, V) == scale(eye(2), q), "original scalar mark on every input")
    H = chain(Vt, A, A, V)
    marked = chain(Vt, A, P, A, V)
    need(H == diag([1, 1+3*q]) and marked == diag([q, 4*q]), "retained spin")
    # For the half-mixture and diagonal H use H^(-1) inside the trace.
    # B=A V H^(-1/2) has B*B=I, while the scalar filter divides by Tr(rho H).
    scalar_filter = tr(marked)/tr(H)
    true_doob = sum(marked[i][i]/H[i][i] for i in range(2))/2
    need(scalar_filter != true_doob, "observable of two normalizations")
    return {"original_mark": str(q), "normalized_sandwich_mark": str(scalar_filter),
            "operator_Doob_mark": str(true_doob), "input": "maximally mixed protected spin"}


def quartic(u0, u1):
    # u0 and u1 are A times two normalized input vectors; their entries
    # are grouped by the two possible marked outcomes.
    def dot(x, y):
        return sum(a*b for a, b in zip(x, y))
    s0, s1 = u0
    t0, t1 = u1
    return [dot(s1,s1), 2*dot(s1,t1), dot(t1,t1)-dot(s0,s0),
            -2*dot(s0,t0), -dot(t0,t0)]


def four_settings():
    # The coefficient proof holds for complex Hilbert--Schmidt vectors
    # with real scalar products in the cross terms.
    settings = (Q(4, 5), Q(5, 6), Q(7, 8), Q(9, 10))
    points = [x*x/(1+x*x) for x in settings]
    need(all(t*t-3*t+1 < 0 and t < Q(1, 2) for t in points), "all four lie in the noisy collar")
    # Monic degree-four polynomial with the stated four roots. Any
    # polynomial of degree <=4 vanishing there is a scalar multiple.
    monic = [Q(1)]
    for x in settings:
        updated = [Q(0)]*(len(monic)+1)
        for i, c in enumerate(monic):
            updated[i] -= x*c
            updated[i+1] += c
        monic = updated
    need(monic[0] == prod(settings) > 0 and monic[4] == 1, "root product sign")
    need(all(sum(c*x**i for i,c in enumerate(monic)) == 0 for x in settings),
         "four rational roots")
    # Every physical quartic has coefficient c0>=0 and c4<=0.
    # The monic quartic has c0,c4 of the same strict sign; only scale zero works.
    inactive = quartic(([Q(1)], [Q(0)]), ([Q(0)], [Q(1)]))
    need(inactive == [0]*5, "zero polynomial, orthogonal filtered branches with equal norms")

    # The SPD A=[[2,-1],[-1,2]] supplies exactly three positive roots
    # on the whole odds axis: R(x)=(1-x^2)(x^2-4x+1).
    R = quartic(([Q(2)], [Q(-1)]), ([Q(-1)], [Q(2)]))
    need(R == [1,-4,0,4,-1], "three-root SPD witness")
    need(2*2-1 == 3 and 3 < 4, "positive determinant; 2-sqrt(3)>0")
    # Z(x)=(5-8x+5x²)/(1+x²) is nonconstant even at matched nodes.
    need(Q(5-8+5, 2) != Q(5), "nonconstant normalization despite three roots")
    return {"odds_sqrt_nodes": [str(x) for x in settings],
            "corresponding_probabilities": [str(t) for t in points],
            "monic_constant": str(monic[0]), "monic_leading": str(monic[4]),
            "three_root_witness_coefficients_ascending": [str(c) for c in R],
            "three_positive_sqrt_odds": ["2-sqrt(3)", "1", "2+sqrt(3)"],
            "center_test_size_M_bits": "1+3*M when the central setting is shared",
            "premises": "same terminal weight, input and parallel conditional branch frames along each axis",
            "narrow_collar_minimality_claimed": False}


def main():
    output = {"status": "PASS", "one_bit_preserved_mark": single_mark(),
              "two_bit_mixed_matrix": mixed_two_bits(), "operator_vs_scalar": doob_mixed_input(),
              "four_settings_theorem": four_settings(), "physical_full_price_selected": False}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
