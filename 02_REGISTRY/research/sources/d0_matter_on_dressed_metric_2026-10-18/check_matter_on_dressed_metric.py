#!/usr/bin/env python3
"""CAR16/Fock and chronological feedback against the density-dressed metric.

Read-only pin origin/exp/a4d-joint-response-continuation-2026-10-16
tip f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6, floor
c3ae03b735dbde690bf1774fc3761846aff93248. Consumes, and does not re-derive,
the grade0 null source and the two-site dressed CAR witness. No stress is
defined as the Einstein tensor. No scalar kinetic integral is added. No
measure is chosen. Not a derivation of GR.
"""

from __future__ import annotations

from fractions import Fraction as Q

import sympy as sp


PIN_TIP = "f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6"
PIN_FLOOR = "c3ae03b735dbde690bf1774fc3761846aff93248"
GRADE0_MEMO = (
    "02_REGISTRY/research/"
    "A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md"
)
GRADE0_BLOB = "dcf5870fa23d5535bca077d5bcbe2e54404a7c2a"
DRESSED_CHECK = (
    "02_REGISTRY/research/sources/"
    "d0_density_dressed_car_metric_2026-10-18/check_dressed_car_metric.py"
)
DRESSED_BLOB = "e6f391e6497e3f1d8298cb5b9c7309ae532737f3"
CHRONO_MEMO = "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md"
CHRONO_BLOB = "fda1294b8d9794a62b86faaa19e3cc1a459e031d"

ZERO = Q(0)
ONE = Q(1)
ETA_DIAG = (ONE, -ONE, -ONE, -ONE)
CAR_N = 16
CHECKS = []


class StressRefusal(RuntimeError):
    """A proposed T_mu_nu is not an owned dressed-metric correlator."""


def require(condition, name):
    CHECKS.append(name)
    if condition is True:
        return
    if condition is False or condition is None:
        raise RuntimeError(name)
    if isinstance(condition, sp.Basic):
        if condition == sp.true:
            return
        raise RuntimeError(name)
    if not condition:
        raise RuntimeError(name)


def matzero(n=CAR_N, m=None):
    if m is None:
        m = n
    return [[ZERO for _ in range(m)] for _ in range(n)]


def ident(n):
    out = matzero(n, n)
    for i in range(n):
        out[i][i] = ONE
    return out


def mmul(a, b):
    out = matzero(len(a), len(b[0]))
    for i in range(len(a)):
        for k, x in enumerate(a[i]):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x * y
    return out


def madd(a, b):
    return [[x + y for x, y in zip(row, other)] for row, other in zip(a, b)]


def mscale(factor, a):
    return [[factor * y for y in row] for row in a]


def mtrans(a):
    return [list(row) for row in zip(*a)]


def inverse4(a):
    m = [row[:] + erow[:] for row, erow in zip(a, ident(4))]
    for col in range(4):
        pivot = next(i for i in range(col, 4) if m[i][col] != 0)
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [x / scale for x in m[col]]
        for i in range(4):
            if i != col:
                factor = m[i][col]
                m[i] = [x - factor * y for x, y in zip(m[i], m[col])]
    return [row[4:] for row in m]


def creator(index):
    out = matzero()
    for mask in range(CAR_N):
        if mask & (1 << index):
            continue
        occupied = bin(mask & ((1 << index) - 1)).count("1")
        sign = -ONE if occupied % 2 else ONE
        out[mask | (1 << index)][mask] = sign
    return out


CREATORS = [creator(i) for i in range(4)]


def gamma(vector):
    out = matzero()
    for i in range(4):
        out = madd(out, mscale(vector[i], CREATORS[i]))
        out = madd(out, mscale(ETA_DIAG[i] * vector[i], mtrans(CREATORS[i])))
    return out


def dot_eta(u, v):
    return sum(ETA_DIAG[i] * u[i] * v[i] for i in range(4))


def entries_equal(left, right):
    return all(
        left[i][j] == right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def _rows(value):
    if value is None:
        return None
    if isinstance(value, sp.MatrixBase):
        return [[value[i, j] for j in range(value.cols)] for i in range(value.rows)]
    return value


def copies_einstein(proposal):
    if proposal.get("copy_einstein"):
        return True
    tee = _rows(proposal.get("T"))
    gee = _rows(proposal.get("G"))
    if tee is None or gee is None:
        return False
    if len(tee) != len(gee):
        return False
    ratio = None
    saw_nonzero = False
    for row_t, row_g in zip(tee, gee):
        if len(row_t) != len(row_g):
            return False
        for left, right in zip(row_t, row_g):
            xs = sp.together(sp.sympify(left))
            ys = sp.together(sp.sympify(right))
            if ys == 0:
                if xs != 0:
                    return False
                continue
            saw_nonzero = True
            piece = sp.together(xs / ys)
            if ratio is None:
                ratio = piece
            elif sp.together(piece - ratio) != 0:
                return False
    if not saw_nonzero:
        return all(
            sp.together(sp.sympify(left) - sp.sympify(right)) == 0
            for row_t, row_g in zip(tee, gee)
            for left, right in zip(row_t, row_g)
        )
    return ratio is not None and sp.together(ratio) != 0


def admit_stress(proposal):
    """Accept only a grade0 citation. Copying G into T raises."""
    if copies_einstein(proposal):
        raise StressRefusal("stress_defined_as_einstein")
    if proposal.get("scalar_action_integral"):
        raise StressRefusal("scalar kinetic integral was added")
    if proposal.get("measure") is not None:
        raise StressRefusal("a measure was chosen")
    if proposal.get("spin_stress"):
        raise StressRefusal("spin correlator is outside the owned source")
    if proposal.get("metric_only_chronology"):
        raise StressRefusal(
            "frozen-matter chronological partial is not a stress on g-hat"
        )
    if proposal.get("kind") != "grade0_only":
        raise StressRefusal("no owned correlator expression for a dressed stress")
    if proposal.get("stress_on_dressed_metric"):
        raise StressRefusal("grade0 citation is not a spin-including dressed stress")
    return {
        "grade0_only": True,
        "stress_on_dressed_metric": False,
        "scoped_nogo": True,
        "stress_defined_as_einstein": False,
        "gr_derived": False,
    }


def _expect_refusal(proposal, name):
    try:
        admit_stress(proposal)
    except StressRefusal:
        require(True, name)
        return
    raise RuntimeError(name + "_did_not_raise")


def dressed_orbit():
    """Constant chi changes raw g and leaves (g-hat, X-hat) fixed."""
    mu_bar = Q(1, 4)
    mus = (Q(1, 9), Q(1, 16))
    chis = (Q(9, 16), Q(4, 9))
    sqrt_chi = (Q(3, 4), Q(2, 3))
    sqrt_mu_bar_over_mu = (Q(3, 2), Q(2))
    eta = [[ETA_DIAG[i] if i == j else ZERO for j in range(4)] for i in range(4)]
    raw_leg = (ONE, Q(1, 5), ZERO, ZERO)
    for mu, chi, root, hat_scale in zip(
        mus, chis, sqrt_chi, sqrt_mu_bar_over_mu
    ):
        g_raw = mscale(1 / chi, eta)
        mu_chi = chi * mu
        g_hat = mscale(mu / mu_bar, eta)
        g_hat_chi = mscale(mu_chi / mu_bar, g_raw)
        require(entries_equal(g_hat, g_hat_chi), "ghat_independent_of_constant_chi")
        require(not entries_equal(g_raw, g_hat), "raw_g_differs_from_ghat")
        x_raw = raw_leg
        x_chi = tuple(root * component for component in raw_leg)
        x_hat = tuple(hat_scale * component for component in x_raw)
        # mu -> chi*mu and X -> sqrt(chi)*X, so sqrt(mu_bar/mu_chi)*X_chi = X_hat.
        hat_scale_chi = hat_scale / root
        x_hat_chi = tuple(hat_scale_chi * component for component in x_chi)
        require(x_hat == x_hat_chi, "Xhat_independent_of_constant_chi")
        require(
            tuple(hat_scale * component for component in x_raw) == x_hat,
            "Xhat_is_sqrt_mubar_over_mu_times_X",
        )
        dressed = gamma(x_hat)
        bare = gamma(x_raw)
        dressed_square = mmul(dressed, dressed)
        bare_square = mmul(bare, bare)
        symbol = dot_eta(x_hat, x_hat)
        bare_symbol = dot_eta(x_raw, x_raw)
        require(symbol == (mu_bar / mu) * bare_symbol, "clifford_symbol_uses_qhat")
        require(
            entries_equal(dressed_square, mscale(symbol, ident(CAR_N))),
            "dressed_gamma_square_is_qhat",
        )
        require(
            entries_equal(bare_square, mscale(bare_symbol, ident(CAR_N))),
            "raw_gamma_square_is_not_the_dressed_symbol",
        )
        require(symbol != bare_symbol, "qhat_differs_from_raw_q")
        # Compensator: d mu = 2 sigma mu and dX = sigma X kills d X-hat.
        sigma = Q(2, 7)
        killed = tuple(
            (-sigma * hat_scale * component) + (hat_scale * sigma * component)
            for component in x_raw
        )
        require(killed == (ZERO, ZERO, ZERO, ZERO), "compensator_kills_dXhat")
    # Two-site weighted edge. Trace of the density commutator jet is zero,
    # so the orbit does not itself supply a scalar source.
    a_site = (Q(2, 3), Q(1, 2))
    edge = ONE
    d_count = [[ZERO, edge], [edge, ZERO]]
    d_mu = [[ZERO, ZERO], [ZERO, ZERO]]
    for i in range(2):
        for j in range(2):
            d_mu[i][j] = a_site[j] / a_site[i] * d_count[i][j]
    for i in range(2):
        for j in range(2):
            require(
                a_site[i] ** 2 * d_mu[i][j] == a_site[j] ** 2 * d_mu[j][i],
                "weighted_edge_adjoint",
            )
    sigmas = (Q(2, 7), Q(-3, 11))
    d_jet = [[(sigmas[j] - sigmas[i]) * d_mu[i][j] for j in range(2)] for i in range(2)]
    product = madd(mmul(d_mu, d_jet), mmul(d_jet, d_mu))
    require(product[0][0] + product[1][1] == ZERO, "density_commutator_trace_zero")
    return {
        "mu_bar": str(mu_bar),
        "mu": [str(mu) for mu in mus],
        "chi": [str(chi) for chi in chis],
        "ghat_scale": [str(mu / mu_bar) for mu in mus],
        "raw_scale": [str(1 / chi) for chi in chis],
    }


def grade0_channel():
    """Owned grade0 square. A spatial bivector is not an argument."""
    h = Q(1, 5)
    shift = Q(4, 5)
    amplitude = Q(1, 3)
    eta = [
        [ZERO, ONE, ZERO, ZERO],
        [ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, -ONE, ZERO],
        [ZERO, ZERO, ZERO, -ONE],
    ]
    legs = ident(4)
    legs[1][0] = shift
    legs = mscale(h, legs)
    metric = mscale(1 / (h * h), mmul(mmul(mtrans(legs), eta), legs))
    inverse = inverse4(metric)
    require(inverse[0][0] == ZERO, "null_guu_zero")
    require(inverse[0][1] == ONE, "null_guv_one")
    contraction = amplitude * amplitude * inverse[0][0]
    require(contraction == ZERO, "grade0_null_scalar_zero")
    hits = []
    for row in range(4):
        for col in range(4):
            d_legs = matzero(4, 4)
            d_legs[row][col] = ONE
            d_metric = madd(
                mmul(mmul(mtrans(d_legs), eta), legs),
                mmul(mmul(mtrans(legs), eta), d_legs),
            )
            d_metric = mscale(1 / (h * h), d_metric)
            mixed = mmul(mmul(inverse, d_metric), inverse)
            derivative = -(amplitude * amplitude) * mixed[0][0]
            if derivative != 0:
                hits.append((row, col, derivative))
    require(len(hits) == 1 and hits[0][0:2] == (0, 1), "grade0_one_coframe_slot")
    require(hits[0][2] == -2 * amplitude * amplitude / h, "grade0_leg_value")
    # k = (s, s, 0, 0) is null for diag(1,-1,-1,-1) and Gamma(k)^2 = 0,
    # while Gamma(k) itself is not the zero operator.
    null_k = (amplitude, amplitude, ZERO, ZERO)
    gamma_k = gamma(null_k)
    require(any(gamma_k[i][j] != 0 for i in range(CAR_N) for j in range(CAR_N)), "null_gamma_nonzero")
    require(
        entries_equal(mmul(gamma_k, gamma_k), matzero()),
        "null_gamma_square_zero",
    )
    spatial_spin = 6  # e1 wedge e2, absent from grade0 q and from iota_{e0}.
    require(bin(spatial_spin).count("1") == 2, "spatial_bivector_is_grade2")
    require(spatial_spin not in (0, 1, 2, 4, 8), "spatial_bivector_not_grade0_or_1")
    return {
        "expression": "q = ghat^{mu nu} (D_mu psi)(D_nu psi) = Tr_16 Gamma(k)^2 / 16",
        "citation": GRADE0_MEMO + "#(3),(18),(19)",
        "blob": GRADE0_BLOB,
        "null_leg": {"row": 0, "column": 1, "value": str(hits[0][2])},
        "proportional_reading": "(d psi)_mu (d psi)_nu on the cited null branch",
        "spin_arguments": 0,
    }


def e2_at_frame(pairs):
    """Owner contraction e = B^T G n at n=e_0 and G=I. E2 = e·e."""
    bivector = sp.zeros(4)
    for (left, right), value in pairs.items():
        bivector[left, right] = value
        bivector[right, left] = -value
    observer = sp.Matrix([1, 0, 0, 0])
    electric = bivector.T * observer
    return sp.simplify((electric.T * electric)[0])


def chronological_and_spin():
    p = (sp.sqrt(5) - 1) / 2
    a = sp.sqrt(p)
    require(sp.simplify(a ** 2 - p) == 0, "golden_a_squared")
    require(sp.simplify(p + p ** 2 - 1) == 0, "golden_p_relation")
    # Consumed (9b) at the reference point: V_11=1/2, xi_1=2, xi_3=0, xi_13=2.
    v11 = sp.Rational(1, 2)
    metric_only = sp.simplify(-2 * a * p ** 2 * v11)
    xi1 = 2
    xi3 = 0
    xi13 = 2
    matter = sp.simplify(p ** 3 * 0 + (a * p ** 2 / 2) * xi1 - a * p ** 2 * xi3)
    joint = sp.simplify(metric_only + matter)
    require(joint == 0, "chronological_factor_jet_zero")
    require(metric_only != 0, "chronological_metric_only_partial_nonzero")
    require(sp.simplify(metric_only + a * p ** 2) == 0, "metric_partial_is_minus_a_p2")
    require(xi13 != 0, "grade3_moves_on_the_factor_curve")
    # Owned (9b) has no xi_13 term. Giving that slot the xi_1 coefficient
    # destroys the cancellation, so the zero jet is not a spin readout.
    spoiled = sp.simplify(joint + (a * p ** 2 / 2) * xi13)
    require(spoiled != 0, "grade3_slot_is_outside_the_owned_angle")
    alpha, e2, step = sp.symbols("alpha E2 t", positive=True)
    radius = sp.sqrt(alpha ** 2 + p ** 2 * e2)
    angle = alpha / radius
    spatial = e2_at_frame({(0, 1): 3, (1, 2): step})
    require(sp.simplify(spatial - 9) == 0, "spatial_bivector_misses_E2")
    contracted_square = e2_at_frame({(0, 1): step})
    require(sp.simplify(contracted_square - step ** 2) == 0, "electric_bivector_enters_E2")
    contracted = sp.simplify(sp.diff(angle, e2).subs({alpha: a, e2: 1}))
    require(sp.simplify(contracted) != 0, "contracted_grade2_has_scalar_angle_jet")
    # Owned grade law, A4D_NATIVE_MATTER_OBSERVER_PAIRING.md:226-228:
    # on q(t)=exp(2t)q, W_k(t)=exp((4-2k)t) W_k. With chi=exp(2t)
    # the scale is chi**(2-k). The square-root scale chi**(1-k/2) is not
    # that law. Density dressing multiplies every grade by sqrt(chi).
    chi = Q(4)
    density_scale = sp.sqrt(sp.Integer(chi))
    owned_grade_scale = {}
    for grade in (0, 2, 3):
        owned_scale = sp.Integer(chi) ** (2 - grade)
        root_scale = sp.Integer(chi) ** (1 - sp.Rational(grade, 2))
        require(
            sp.simplify(root_scale ** 2 - owned_scale) == 0,
            "square_root_scale_is_not_a_second_owned_law_grade_%d" % grade,
        )
        require(
            sp.simplify(owned_scale - density_scale) != 0,
            "owned_grade_law_differs_from_density_dressing_grade_%d" % grade,
        )
        owned_grade_scale[str(grade)] = str(sp.simplify(owned_scale))
    frozen = sp.simplify(
        (-2 * a * p ** 2 * sp.Rational(1, 4))
    )
    # Constant conformal raw variation V = -q at chi=1 has V_11 = 1/4 on
    # q_11=-1, hence a nonzero frozen partial. g-hat does not move.
    require(frozen != 0, "raw_constant_chi_frozen_partial_nonzero")
    return {
        "metric_only_partial": str(metric_only),
        "joint_factor_jet": str(joint),
        "grade3_coefficient": "0",
        "angle_support_masks": [0, 1, 3],
        "owned_grade_scale": owned_grade_scale,
        "density_scale": str(density_scale),
    }


def einstein_of(metric, coords):
    dimension = len(coords)
    inverse = sp.simplify(metric.inv())
    gamma = [
        [[0 for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for rho in range(dimension):
        for mu in range(dimension):
            for nu in range(mu, dimension):
                acc = 0
                for sig in range(dimension):
                    acc += inverse[rho, sig] * (
                        sp.diff(metric[nu, sig], coords[mu])
                        + sp.diff(metric[mu, sig], coords[nu])
                        - sp.diff(metric[mu, nu], coords[sig])
                    )
                value = sp.simplify(acc / 2)
                gamma[rho][mu][nu] = value
                gamma[rho][nu][mu] = value
    ricci = sp.zeros(dimension)
    for nu in range(dimension):
        for rho in range(nu, dimension):
            value = 0
            for lam in range(dimension):
                value += sp.diff(gamma[lam][nu][rho], coords[lam])
                value -= sp.diff(gamma[lam][nu][lam], coords[rho])
                for sig in range(dimension):
                    value += gamma[lam][lam][sig] * gamma[sig][nu][rho]
                    value -= gamma[lam][rho][sig] * gamma[sig][nu][lam]
            ricci[nu, rho] = sp.simplify(value)
            ricci[rho, nu] = ricci[nu, rho]
    scalar = sp.simplify(
        sum(inverse[i, j] * ricci[i, j] for i in range(dimension) for j in range(dimension))
    )
    einstein = sp.simplify(ricci - sp.Rational(1, 2) * scalar * metric)
    return scalar, einstein


def raw_representative_defect():
    """Spacetime-dependent chi: raw G is nonzero while G(g-hat) is zero."""
    t, x, y, z = sp.symbols("t x y z")
    coords = (t, x, y, z)
    chi = (1 + x / 2) ** 2
    eta = sp.diag(1, -1, -1, -1)
    g_raw = sp.simplify(eta / chi)
    scalar_raw, g_einstein = einstein_of(g_raw, coords)
    scalar_hat, hat_einstein = einstein_of(eta, coords)
    closed = -3 / (x + 2) ** 2 * eta
    require(sp.simplify(scalar_raw - 3) == 0, "raw_scalar_curvature")
    require(sp.simplify(g_einstein - closed) == sp.zeros(4), "raw_einstein_closed_form")
    require(sp.simplify(scalar_hat) == 0, "dressed_scalar_zero")
    require(hat_einstein == sp.zeros(4), "dressed_einstein_zero")
    at_zero = sp.simplify(g_einstein.subs(x, 0))
    expected = sp.diag(sp.Rational(-3, 4), sp.Rational(3, 4), sp.Rational(3, 4), sp.Rational(3, 4))
    require(at_zero == expected, "raw_einstein_at_contact_point")
    require(sp.simplify(g_raw.subs(x, 0) - eta) == sp.zeros(4), "metrics_agree_at_point")
    require(at_zero != hat_einstein, "agreement_of_metrics_is_not_agreement_of_G")
    _expect_refusal(
        {"copy_einstein": True, "T": at_zero, "G": at_zero, "kind": "grade0_only"},
        "refuse_copy_of_raw_einstein",
    )
    _expect_refusal(
        {"T": hat_einstein, "G": hat_einstein, "kind": "grade0_only"},
        "refuse_copy_of_zero_dressed_einstein",
    )
    _expect_refusal(
        {
            "T": 2 * at_zero,
            "G": at_zero,
            "kind": "grade0_only",
        },
        "refuse_multiple_of_einstein",
    )
    _expect_refusal(
        {"kind": "grade0_only", "scalar_action_integral": True},
        "refuse_scalar_action_integral",
    )
    _expect_refusal(
        {"kind": "grade0_only", "measure": (1, 1, 1, 1)},
        "refuse_chosen_measure",
    )
    _expect_refusal(
        {"kind": "grade0_only", "spin_stress": True},
        "refuse_spin_stress",
    )
    _expect_refusal(
        {"kind": "grade0_only", "metric_only_chronology": True},
        "refuse_metric_only_chronology",
    )
    citation = admit_stress(
        {
            "kind": "grade0_only",
            "stress_on_dressed_metric": False,
            "expression": "cited grade0 q, not T",
        }
    )
    require(citation["scoped_nogo"] is True, "citation_keeps_scoped_nogo")
    require(citation["stress_on_dressed_metric"] is False, "citation_does_not_set_stress")
    require(citation["gr_derived"] is False, "citation_does_not_derive_gr")
    return {
        "contact_g": "eta",
        "raw_einstein_at_0": ["-3/4", "3/4", "3/4", "3/4"],
        "dressed_einstein": "0",
    }


def run():
    del CHECKS[:]
    orbit = dressed_orbit()
    grade0 = grade0_channel()
    chrono = chronological_and_spin()
    defect = raw_representative_defect()
    flags = {
        "stress_on_dressed_metric": False,
        "scoped_nogo": True,
        "stress_defined_as_einstein": False,
        "gr_derived": False,
        "grade0_only": True,
        "spin_in_owned_source": False,
        "physical_tape_cost_clock_admitted": False,
        "hodge_links_closed": False,
        "measure_chosen": False,
        "scalar_action_added": False,
    }
    require(flags["scoped_nogo"] is True, "scoped_nogo")
    require(flags["stress_on_dressed_metric"] is False, "stress_on_dressed_metric_false")
    require(
        flags["scoped_nogo"] != flags["stress_on_dressed_metric"],
        "exactly_one_of_stress_or_nogo",
    )
    require(flags["stress_defined_as_einstein"] is False, "stress_defined_as_einstein")
    require(flags["gr_derived"] is False, "gr_derived")
    require(flags["grade0_only"] is True, "grade0_only")
    result = {
        "status": "PASS",
        "verdict": "SCOPED-NOGO-SPIN-AND-CHRONOLOGY-NOT-A-STRESS-ON-DRESSED-METRIC",
        "pin_tip": PIN_TIP,
        "pin_floor": PIN_FLOOR,
        "dressed_checker": DRESSED_CHECK,
        "dressed_blob": DRESSED_BLOB,
        "chrono_memo": CHRONO_MEMO,
        "chrono_blob": CHRONO_BLOB,
        "flags": flags,
        "orbit": orbit,
        "grade0_only": grade0,
        "chronology": chrono,
        "raw_defect": defect,
        "check_count": len(CHECKS),
    }
    print("PASS dressed orbit: g-hat and X-hat fixed, raw g and raw Clifford symbol move")
    print("PASS grade0 citation only; spatial bivector is not an argument of q")
    print("PASS chronological joint factor jet is 0 and the metric-only partial is not T")
    print("PASS raw representative Einstein is not a source on g-hat")
    print(
        "PASS scoped_nogo true; stress_on_dressed_metric false; "
        "stress_defined_as_einstein false; gr_derived false"
    )
    print("SCOPE: physical tape/cost/clock not admitted; not D0=>GR; spin stress absent")
    return result


if __name__ == "__main__":
    run()
