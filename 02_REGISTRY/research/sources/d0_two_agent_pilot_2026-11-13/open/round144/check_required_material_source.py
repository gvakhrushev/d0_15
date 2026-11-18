"""Certify the wave kernel and the least source required on the A73 collar."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
OWNER = HERE.parents[1] / "direct/round73/matter"
sys.path.insert(0, str(OWNER))
import check_matter_root as a73

R = sp.Rational
EPSILON = R(1, 10**7)


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def exact_dot(a, b):
    return (a.T*b)[0]


def norm_sq(vector):
    return exact_dot(vector, vector)


def ceiling_norm(vector):
    return sp.Integer(sp.ceiling(sp.sqrt(norm_sq(vector))))


def matrix_data():
    sites = a73.SITES
    active = [i for i, (u,v,x,y) in enumerate(sites)
              if u in (1, 2) and x in (1, 2) and y in (1, 2)]
    need(len(active) == 32, "A73 collar and this test use different active sites")
    waves = []
    for j in active:
        column = [0]*len(sites)
        column[j] = 1
        waves.append([a73.wave_equation(column, i) for i in active])
    wave = sp.Matrix(waves).T
    nullspace = sp.Matrix([
        [(-1)**v, (-1)**(v+u+x+y)] for u,v,x,y in (sites[i] for i in active)
    ])
    need(wave*nullspace == sp.zeros(32, 2), "Supplied alternating modes are not wave-null")
    need(nullspace.rank() == 2 and wave.rank() == 30, "Wave kernel was not exhausted")

    profile = sp.Matrix([a73.core.B(z) for z in sites])
    need(all(a73.wave_equation(profile, i) == 0 for i in active),
         "Original collar is not solved by the declared profile")
    matrix = sp.Matrix(a73.blocks("rational")[15])
    rhs = matrix[active, :]*profile
    modes = matrix[active, active]*nullspace

    # The same exact-entry budget as A73. Each input radical is floored
    # with error <=1/SCALE, and all Gram columns use the original Fourier data.
    scale = a73.SCALE
    gram_error = R(64*128**2*19, scale)
    gram_size = 64*128**2*81
    need(gram_error + 256*(3*gram_error + R(gram_size, scale)) < EPSILON,
         "Coefficient interval no longer covers the true A73 Hessian")
    rhs_error = 6*sum(map(abs, profile))*EPSILON
    modes_error = 8*32*EPSILON
    return rhs, modes, rhs_error, modes_error, active


def certify_distance(rhs, modes, rhs_error, modes_error):
    gram = modes.T*modes
    # Its smaller eigenvalue is >= det(gram)/trace(gram).
    sigma = sp.floor(sp.sqrt(gram.det()/sp.trace(gram)))
    need(sigma > modes_error, "Numerical columns are too close to degeneracy")
    center = -gram.inv()*modes.T*rhs
    value = norm_sq(rhs + modes*center)
    digits = 10**5
    floor_value = sp.floor(sp.sqrt(value*digits**2))
    lo, hi = R(floor_value, digits), R(floor_value+1, digits)
    # Locating the true minimizer needs no numerical assumption.
    # ||rhs+N beta_min|| <= ||rhs|| implies ||N beta_min|| <= 2||rhs||.
    radius = 2*(ceiling_norm(rhs)+rhs_error)/(sigma-modes_error)
    err_lo = rhs_error + modes_error*radius
    err_hi = rhs_error + modes_error*ceiling_norm(center)
    need(lo > err_lo, "No strictly positive lower bound survived coefficient errors")
    lo_final = sp.floor((lo-err_lo)*1000)
    hi_final = sp.ceiling((hi+err_hi)*1000)
    return lo_final, hi_final, center


def v_invariant_diagonal_test(rhs, modes, rhs_error, modes_error, active):
    # Average at u=1 over the true periodic coordinate v. On this slab the
    # desired collar has b*=0, and both remaining Einstein solutions alternate.
    sites = a73.SITES
    averages = sp.Matrix([
        [R(1,4) if sites[i][0] == 1 and sites[i][2:] == (x,y) else 0
         for i in active]
        for x in (1,2) for y in (1,2)
    ])
    h = averages*rhs
    h_modes = averages*modes
    # These disjoint 4-point averaging rows have norm 1/2.
    lo, hi, _ = certify_distance(h, h_modes, rhs_error/2, modes_error/2)
    return {"normal_coordinates": "u=1, average over v, four transverse sites",
            "residual_interval_in_K_units": [str(lo/1000), str(hi/1000)]}


def main():
    rhs, modes, rhs_error, modes_error, active = matrix_data()
    lo, hi, optimum = certify_distance(rhs, modes, rhs_error, modes_error)
    tau_physical = R(2*256, 10946*128**2)
    site_lower = tau_physical * R(lo, 6000)
    print(json.dumps({
        "status": "PASS",
        "source_sha256": sha256((OWNER/"check_matter_root.py").read_bytes()).hexdigest(),
        "interior_sites": 32,
        "pinned_h": "1/4",
        "wave_rank": 30,
        "wave_kernel": ["(-1)^v", "(-1)^(v+u+x+y)"],
        "minimal_required_K_norm_interval": [str(R(lo,1000)), str(R(hi,1000))],
        "diagnostic_optimal_kernel_amplitudes": [str(sp.N(value, 9)) for value in optimum],
        "K_to_D_Psi_over_t": str(tau_physical),
        "strict_single_site_D_Psi_over_t_lower_bound": str(site_lower),
        "local_diagonal_test": v_invariant_diagonal_test(rhs, modes, rhs_error, modes_error, active),
        "claimed_refinement_uniform": False,
        "selected_physical_cost_info": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
