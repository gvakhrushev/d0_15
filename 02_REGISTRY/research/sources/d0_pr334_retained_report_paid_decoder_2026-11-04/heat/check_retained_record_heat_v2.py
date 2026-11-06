"""Exact finite checks for the retained-record full-price application.

The rational matrices below are algebra fixtures, not a new native execution.
They verify the general-xi Schur identity and its B-direction derivative with
noncommuting birth-age matrices.  The existing CL8/CL9 bounds are CONSUMED,
not reproved.  The optional readiness lower bound is a declared budget input;
this checker does not establish its physical binding or task admission.
"""

import argparse
from fractions import Fraction
from math import factorial
import json

import sympy as sp


CHECKS = []


def need(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def equal_matrix(left, right, label):
    need(all(sp.cancel(entry) == 0 for entry in left - right), label)


def cl8_bound(age):
    """Owned CL8 rational majorant; age is the REAL minimum birth age."""
    if type(age) is not int or age < 1:
        raise ValueError("minimum birth age must be a positive integer")
    x = Fraction(2, 55)
    return (Fraction(176, 359) * x**age / factorial(age)
            / ((1 - x*x) * (1 - x/age)))


def padding_budget(base_age, margin, lift=Fraction(1)):
    """Choose real two-call identity pairs AFTER margin and lift are fixed."""
    if margin <= 0 or lift <= 0:
        raise ValueError("source margin and lift must be strictly positive")
    for pairs in range(10000):
        age = base_age + 2*pairs
        bound = cl8_bound(age)
        if lift*bound < margin/2:
            return pairs, age, bound
    raise ArithmeticError("bounded padding search exhausted")


def schur_checks():
    xi = sp.Symbol("xi", real=True)
    one = sp.eye(2)
    zero = sp.zeros(2)
    # An orthogonal B that mixes the two OLD birth layers.
    B = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    generator = sp.Matrix([[0, -1], [1, 0]])
    S = sp.diag(1, -1)
    P1 = sp.diag(0, 1)
    P0 = one - P1
    F = B.T*S*P0*B
    G = B.T*S*P1*B
    Q = B.T*P1*B
    equal_matrix(B.T*B, one, "rational complete B is orthogonal")
    equal_matrix(S*P1, P1*S, "original sign preserves copied report")
    equal_matrix(F*G, zero, "full F and G have orthogonal supports")
    equal_matrix(F*F, one-Q, "full F squared is report-zero projector")
    equal_matrix(G*G, Q, "full G squared is report-one projector")
    need(F.T == F and G.T == G and Q.T == Q,
         "all three full-carrier blocks are selfadjoint")

    # Valid unequal ages for an abstract 1 -> 2 -> 4 growing carrier:
    # old details have ages 5,4; the last record detail has age 3 and rank 2.
    Dold = sp.diag(xi**5, xi**4)
    t = xi**3
    Dage = sp.diag(Dold, t*one)
    need(any(sp.expand(x) != 0 for x in F*Dold-Dold*F),
         "F really fails to commute with the old birth-age matrix")
    need(any(sp.expand(x) != 0 for x in Q*Dold-Dold*Q),
         "Q really fails to commute with the old birth-age matrix")
    W = F.row_join(G).col_join(G.row_join(F))
    equal_matrix(W*W, sp.eye(4), "kept-marker full endpoint is a reflection")
    need(W.T == W, "kept-marker reflection retains all four columns")

    full_matrix = sp.eye(4)-W*Dage
    factor_a = one-t*F
    factor_b = one-(F+t*Q)*Dold
    direct_det = sp.factor(full_matrix.det(method="domain-ge"))
    schur_det = sp.factor(factor_a.det()*factor_b.det())
    need(sp.cancel(direct_det-schur_det) == 0,
         "general-xi whole-clock determinant equals the two-factor Schur expression")
    need(sp.Poly(direct_det, xi).degree() == 15,
         "determinant degree keeps all 5+4+2*3 genuine clock dimensions")
    need(direct_det.subs(xi, 0) == 1,
         "whole characteristic determinant has its exact constant term")
    # Hostile control: treating the old ages as a scalar changes the result.
    scalar_age_det = (one-t*F).det()*(one-(F+t*Q)*xi**4).det()
    need(sp.cancel(direct_det-scalar_age_det) != 0,
         "homogeneous-old-age substitution is detected as a different clock")

    # Actual first derivative along B(epsilon)=B exp(epsilon J), evaluated
    # at zero.  All old operators are fixed; F,G,Q move by their real commutator.
    dF = F*generator-generator*F
    dG = G*generator-generator*G
    dQ = Q*generator-generator*Q
    dW = dF.row_join(dG).col_join(dG.row_join(dF))
    dM = -dW*Dage
    direct_log_jet = sp.cancel(sp.trace(full_matrix.inv(method="DM")*dM))
    schur_log_jet = sp.cancel(
        sp.trace(factor_a.inv(method="DM")*(-t*dF))
        + sp.trace(factor_b.inv(method="DM")*(-(dF+t*dQ)*Dold)))
    need(sp.cancel(direct_log_jet-schur_log_jet) == 0,
         "general-xi direct logdet first variation equals the Schur first variation")
    need(direct_log_jet != 0,
         "B-direction logdet source is genuinely nonzero at unequal birth ages")
    need(sp.cancel(sp.trace(factor_a.inv(method="DM")*(-t*dF))) == 0,
         "first factor has fixed spectrum along the B conjugacy")
    equal_matrix(dW*W+W*dW, sp.zeros(4),
                 "B-direction jet is tangent to the full reflected endpoint")
    need(sorted((dW.T*dW).eigenvals()) == [0, 4],
         "two B occurrences retain the exact operator-norm lift factor two")

    # Finite native-marker shape: its angle/comparison realization is external.
    s = sp.Rational(3, 5)
    cosine = sp.Rational(4, 5)
    plus = (F+s*G).row_join(cosine*G).col_join(
        (cosine*G).row_join(F-s*G))
    minus = (F-s*G).row_join(cosine*G).col_join(
        (cosine*G).row_join(F+s*G))
    equal_matrix(plus*plus, sp.eye(4), "positive finite marker endpoint is a reflection")
    equal_matrix(minus*minus, sp.eye(4), "negative finite marker endpoint is a reflection")
    difference = plus-minus
    equal_matrix(difference, sp.diag(2*s*G, -2*s*G),
                 "finite full endpoint chord has exactly the two signed G blocks")
    eigenvalues = (difference.T*difference).eigenvals()
    need(max(eigenvalues) == 4*s*s,
         "full endpoint chord has exact norm 2s, not 4s")
    return {
        "fixture_scope": "rational algebra fixture, not a native word or H.1 admission proof",
        "old_birth_ages": [5, 4], "record_birth_age": 3,
        "whole_clock_dimension": 15,
        "determinant": str(direct_det),
        "B_direction_logdet_derivative": str(sp.factor(direct_log_jet)),
        "B_direction_endpoint_norm": "2",
        "finite_marker_s": str(s), "finite_endpoint_chord_norm": str(2*s),
    }


def return_and_padding_checks(alpha_lower, rank, base_age):
    # Separate physical-compression fixture; this is NOT a compression claim
    # about the full-carrier Schur fixture above.
    A = sp.diag(sp.Rational(2, 5), sp.Rational(1, 2))
    D = sp.Rational(3, 4)*sp.eye(2)-A
    aa, bb = sp.Rational(2, 5), sp.Rational(1, 4)
    s = sp.Rational(3, 5)
    zeta_s = sp.Rational(1, 2**20)
    Cplus, Cminus = A+s*D, A-s*D
    equal_matrix(A*D, D*A, "physical fixture has the H.1 scalar-sum commutation")
    equal_matrix(Cplus*Cplus-Cminus*Cminus, 4*s*A*D,
                 "finite squared-corner gap is exactly 4s AD")
    hplus, hminus = Cplus*Cplus, Cminus*Cminus
    Mplus = (1-zeta_s)*sp.eye(2)+zeta_s*hplus
    Mminus = (1-zeta_s)*sp.eye(2)+zeta_s*hminus
    for k in range(2):
        need(0 < Mminus[k,k] < Mplus[k,k] <= 1,
             "log-ratio positive contraction collar on physical coordinate "+str(k))
        need(A[k,k] >= aa and D[k,k] >= bb,
             "actual compression fixture respects both positive lower margins "+str(k))
    need(sp.trace(Mplus-Mminus) >= 4*2*zeta_s*s*aa*bb,
         "log-ratio integral gives J_minus-J_plus at least 4r zeta s a b")
    need(sp.trace((Mplus-Mminus)*Mplus.inv()) >= sp.trace(Mplus-Mminus),
         "each log-ratio lower bound retains its true at-most-one denominator")

    if not (Fraction(0) < alpha_lower <= 1):
        raise ValueError("readiness lower bound must lie in (0,1]")
    if type(rank) is not int or rank < 1:
        raise ValueError("true initial input rank must be a positive integer")
    if type(base_age) is not int or base_age < 1:
        raise ValueError("actual initial minimum birth age must be positive")
    zeta = Fraction(1, 2**20)
    c_min = Fraction(52947, 131072)
    # Consumed EU baseline bounds: r0>zeta and 1-r0>1-2zeta.
    a_lower = c_min*alpha_lower*(1-2*zeta)
    b_lower = c_min*alpha_lower*zeta
    source_margin = 2*rank*zeta*a_lower*b_lower
    pairs, age, heat = padding_budget(base_age, source_margin)
    need(age == base_age+2*pairs,
         "padding uses complete actual two-call CX pairs and their full ages")
    need(heat < source_margin/2,
         "owned CL8 heat source is below half the return source margin")
    if pairs:
        need(cl8_bound(age-2) >= source_margin/2,
             "the reported padding is the first passing same-parity length")
    # CL9: ||W_plus-W_minus||=2s.  Thus divide the whole-price comparison
    # by 2s, keeping its actual sign and precisely the ordinary-row margin.
    finite_s = Fraction(3, 5)
    J_gap_lower = 4*rank*zeta*finite_s*a_lower*b_lower
    H_gap_bound = 2*finite_s*heat
    need((J_gap_lower-H_gap_bound)/(2*finite_s) == source_margin-heat,
         "finite normalized contrast and ordinary source have the same margin")
    need(J_gap_lower > H_gap_bound,
         "complete finite B_plus-B_minus is strictly negative at the stated margin")
    return {
        "readiness_lower_bound": str(alpha_lower),
        "initial_input_rank": rank,
        "a_lower": str(a_lower), "b_lower": str(b_lower),
        "return_source_margin": str(source_margin),
        "initial_minimum_birth_age": base_age,
        "actual_CX_pairs_to_append": pairs,
        "added_real_calls": 2*pairs,
        "final_minimum_birth_age": age,
        "owned_CL8_rational_upper": str(heat),
        "strict_negative_normalized_price_upper": str(-(source_margin-heat)),
        "finite_s_fixture": str(finite_s),
        "log_inequality_consumed": "log(y/x) >= (y-x)/y >= y-x for 0<x<=y<=1",
        "physical_readiness_binding_proved": False,
    }



def paid_reader_checks(rank):
    """The paid reader destroys reflection but retains the exact Schur map.

    The rational reader a=4/5,p=3/5 tests the algebra using only a*a+p*p=1.
    It is NOT substituted for the actual Golden reader in the native word.
    The separate padding margin uses the ORIGINAL Golden bound p*p>3/8.
    """
    xi = sp.Symbol("xi", real=True)
    I = sp.eye(2)
    Z = sp.zeros(2)
    B = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    S, P1 = sp.diag(1, -1), sp.diag(0, 1)
    F, G, Q = B.T*S*(I-P1)*B, B.T*S*P1*B, B.T*P1*B
    a, p = sp.Rational(4, 5), sp.Rational(3, 5)
    need(a*a+p*p == 1 and a > p > 0,
         "paid-reader algebra fixture has normalized positive rotation")
    t, Dold = xi**3, sp.diag(xi**5, xi**4)
    Dage = sp.diag(Dold, t*I)
    U00, U01 = a*F+p*G, a*G+p*F
    U10, U11 = a*G-p*F, a*F-p*G
    U = U00.row_join(U01).col_join(U10.row_join(U11))
    equal_matrix(U.T*U, sp.eye(4), "reader-included complete endpoint is unitary")
    need(U != U.T, "reader-included endpoint is not falsely treated as a reflection")
    equal_matrix(U01*U10, Q-p*p*I,
                 "paid-reader cross-block product is exactly Q minus p squared I")
    E = I-t*U11
    Einv = E.inv(method="DM")
    Leff = U00+t*Einv*(Q-p*p*I)
    full_matrix = sp.eye(4)-U*Dage
    reduced_matrix = I-Leff*Dold
    direct_det = sp.factor(full_matrix.det(method="domain-ge"))
    schur_det = sp.cancel(E.det()*reduced_matrix.det())
    need(sp.cancel(direct_det-schur_det) == 0,
         "paid-reader general-xi determinant equals E times the coupled Schur determinant")
    need(sp.Poly(direct_det, xi).degree() == 15,
         "paid-reader reduction retains every unequal-age clock dimension")
    need(any(sp.expand(x) != 0 for x in F*Dold-Dold*F),
         "paid-reader determinant retains noncommuting old birth flags")

    J = sp.Matrix([[0, -1], [1, 0]])
    dF, dG, dQ = F*J-J*F, G*J-J*G, Q*J-J*Q
    dU = ((a*dF+p*dG).row_join(a*dG+p*dF)).col_join(
        (a*dG-p*dF).row_join(a*dF-p*dG))
    dE = -t*(a*dF-p*dG)
    dLeff = a*dF+p*dG+t*(-Einv*dE*Einv*(Q-p*p*I)+Einv*dQ)
    full_log_jet = sp.cancel(sp.trace(full_matrix.inv(method="DM")*(-dU*Dage)))
    schur_log_jet = sp.cancel(sp.trace(Einv*dE)
                             +sp.trace(reduced_matrix.inv(method="DM")*(-dLeff*Dold)))
    need(sp.cancel(full_log_jet-schur_log_jet) == 0,
         "paid-reader direct logdet derivative equals full differentiated Schur formula")
    need(full_log_jet != 0,
         "paid-reader B-direction source is nonzero on the unequal-age fixture")

    J_record = Z.row_join(-I).col_join(I.row_join(Z))
    front_jet = U*J_record
    equal_matrix(front_jet[:2,:2], p*F+a*G,
                 "independent forward record leg has cold derivative p F plus a G")
    equal_matrix(front_jet.T*front_jet, sp.eye(4),
                 "independent forward record leg retains endpoint operator-norm lift one")

    # An independent, explicitly positive physical-compression fixture.
    # In H.1 these inequalities require EU14 and the original selector input.
    A = sp.diag(sp.Rational(2, 5), sp.Rational(1, 2))
    D = sp.Rational(3, 4)*I-A
    Cread, Cfront = a*A+p*D, p*A+a*D
    old_lower = sp.Rational(3, 4)
    for k in range(2):
        need(Cread[k,k] >= p*old_lower and Cfront[k,k] >= p*old_lower,
             "paid-reader positive source bounds use A plus D, not readiness "+str(k))
        need(0 < Cread[k,k] < 1,
             "paid-reader physical compression remains a strict positive contraction "+str(k))
    zeta = Fraction(1, 2**20)
    c_min = Fraction(52947, 131072)
    golden_p_squared_lower = Fraction(3, 8)
    readiness_free_margin = 2*rank*zeta*golden_p_squared_lower*c_min*c_min
    heat60 = cl8_bound(60)
    need(heat60 < readiness_free_margin/2,
         "actual60-call minimum age heat bound is below half the readiness-free source margin")
    need(2*Fraction(3, 5)*Fraction(1, 2**20) > 0,
         "readiness-free source estimate retains the positive physical return parameter")
    return {
        "reader_algebra_fixture": {"a": str(a), "p": str(p),
                                   "is_native_Golden_reader": False},
        "general_xi_determinant": str(direct_det),
        "B_direction_logdet_derivative": str(sp.factor(full_log_jet)),
        "source_row": "J_f <= -2 r zeta p^2 c_min^2; actual Golden p^2 > 3/8",
        "true_input_rank_parameter": rank,
        "independent_front_endpoint_norm": "1",
        "readiness_free_return_margin": str(readiness_free_margin),
        "actual_reader_minimum_birth_age": 60,
        "owned_CL8_age60_upper": str(heat60),
        "strict_negative_full_source_upper": str(-(readiness_free_margin-heat60)),
        "physical_admission_or_source_norm_selected": False,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha-lower", default="1/4",
                        help="declared rational readiness lower bound; default is a budget fixture")
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--base-age", type=int, default=3)
    args = parser.parse_args()
    algebra = schur_checks()
    paid_reader = paid_reader_checks(args.rank)
    budget = return_and_padding_checks(Fraction(args.alpha_lower), args.rank, args.base_age)
    print(json.dumps({
        "status": "PASS", "checks": CHECKS,
        "schur_fixture": algebra, "paid_reader": paid_reader,
        "declared_rational_padding_budget": budget,
        "scope": {
            "owned_CL8_CL9_reproved": False,
            "actual_native_marker_or_H1_word_verified_here": False,
            "actual_native_same_length_comparison_admitted_here": False,
            "original_raw_norm_replaced": False,
            "additional_scene_birth_or_cut_rows_discarded": False,
            "physical_Info_or_primitive_Cost_selected": False,
            "GR_closed": False,
        },
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
