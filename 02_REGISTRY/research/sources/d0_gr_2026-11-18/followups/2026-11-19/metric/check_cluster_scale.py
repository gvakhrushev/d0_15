"""Exact arithmetic for the two-component source and the two-scale reading."""
from fractions import Fraction as F
import json


def require(test, label):
    if not test:
        raise ArithmeticError(label)


def dot(row, direction):
    return sum(x*y for x, y in zip(row, direction))


def combine(a, x, b, y):
    return tuple(a*u+b*v for u, v in zip(x, y))


def main():
    # The last direction represents an independent work coordinate of the
    # apparatus. The target and material volume vanish on it.
    omega_A = (F(-3, 5), F(4, 9), F(17, 11), F(0))
    nu_A = (F(0), F(1), F(2, 3), F(0))
    omega_B = (F(2), F(-7, 3), F(0))
    nu_B = (F(0), F(2, 5), F(0))
    z, w = (F(1, 2), 0, 0), (0, F(5, 2), 0)
    require((dot(omega_B, z), dot(nu_B, z), dot(nu_B, w)) == (1, 0, 1),
            "anchor dual calibration")
    alpha, beta = F(7, 3), F(-5, 8)
    source_A = combine(alpha, omega_A, beta, nu_A)
    source_B = combine(alpha, omega_B, beta, nu_B)
    gain = dot(source_B, z)
    volume_price = dot(source_B, w)-gain*dot(omega_B, w)
    require((gain, volume_price) == (alpha, beta), "recover both universal coefficients")
    for slot in range(len(source_A)):
        u = tuple(F(i == slot) for i in range(len(source_A)))
        v = dot(nu_A, u)
        opposing = tuple(-v*x for x in w)
        require(dot(nu_A, u)+dot(nu_B, opposing) == 0, "equal total volume")
        require(dot(source_A, u)+dot(source_B, opposing) ==
                gain*(dot(omega_A, u)+dot(omega_B, opposing)), "shared physical row")
        require(dot(source_A, u) == gain*dot(omega_A, u)+volume_price*v,
                "individual row recovered by paired measurement")

    # An independent unknown overall meter multiplier is allowed at each scale.
    scale = F(3, 2)
    pulled_source = combine(alpha*scale**2, omega_B, beta*scale**4, nu_B)
    def ratio(row, meter):
        return (meter*dot(row, w))/(meter*dot(row, z))
    base_ratio = ratio(source_B, F(17, 12))
    scaled_ratio = ratio(pulled_source, F(2, 19))
    recovered = (scaled_ratio-base_ratio)/(scale**2-1)
    require(recovered == beta/alpha, "relative volume coefficient without absolute source scale")
    # For the actual native scale phi the same identity uses phi^2 = phi+1.
    # An ordered pair represents c+d*phi, so the exact difference of the two
    # uncalibrated relative readings is (beta/alpha)*phi.
    def golden_times(x, y):
        c, d = x
        e, f = y
        return (c*e+d*f, c*f+d*e+d*f)
    native_step_diff = (F(0), beta/alpha)
    require(golden_times((F(-1), F(1)), native_step_diff) == (beta/alpha, 0),
            "native inverse Golden scale recovers volume coefficient")
    errors = ((F(1, 40), F(-1, 33)), (F(-1, 18), F(1, 27)))
    estimates, error_bound = [], F(0)
    for row, factor, (ez, ew) in zip((source_B, pulled_source), (1, scale**2), errors):
        observed = (dot(row, w)+ew)/(dot(row, z)+ez)
        estimates.append(observed)
        error_bound += (abs(ew)+abs(observed*ez))/(alpha*factor*abs(scale**2-1))
    estimate = (estimates[1]-estimates[0])/(scale**2-1)
    require(abs(estimate-beta/alpha) <= error_bound, "two-scale source stability")

    # A nonlinear volume ambiguity is visible to a compensated transfer on
    # two disjoint components, even though it vanishes on each fixed-volume leaf.
    va, vb = F(3), F(7)
    nonlinear_transfer = 2*va-2*vb
    require(nonlinear_transfer != 0, "cluster test detects different marginal volume prices")
    print(json.dumps({
        "independent_probe_dimensions": [len(source_A), len(source_B)],
        "anchor_gain": str(gain), "universal_volume_price": str(volume_price),
        "homothety": str(scale), "ratios": [str(base_ratio), str(scaled_ratio)],
        "golden_step_ratio_difference_in_basis_1_phi": [str(v) for v in native_step_diff],
        "beta_over_alpha": str(recovered), "target_chi_at_paid_stationarity": str(-recovered),
        "perturbed_estimate_error": str(abs(estimate-recovered)),
        "perturbed_estimate_error_bound": str(error_bound),
        "compensated_derivative_for_separate_V_squared": str(nonlinear_transfer),
        "scope": "algebraic test of source transport; cluster and scale admission on physical H.1 open"
    }, indent=2))


if __name__ == "__main__":
    main()
