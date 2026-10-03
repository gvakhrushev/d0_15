#!/usr/bin/env python3
"""Exact source-first obstruction to raw owner convergence for weak sources.

The source is fixed explicitly before the connection is solved. The owned
complete #227 Euler identity is consumed, then its constitutive map is
inverted exactly. No new microscopic carrier is searched. The all-mesh
proof and the fixed-smooth-source exclusion are in A4D_SOURCE_IMAGE_COLLAPSE.md.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

import numpy as np
import sympy as sp
import a4d_identity_quarter_nonlinear_response_check as N
from a4d_stationary_response_memory_check import full_boost_polynomial


VISIBLE = (0, 0, 0, 0, -1, 1, 1, -1, 1, -1)
SIGNS = (1, 1, -1, -1)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def exact_source_inverse():
    # z is the required geometric-response scalar, an input rather than a
    # response read from a candidate. c denotes the positive square root.
    z, c = sp.symbols("z c", real=True)
    relation = sp.Poly(c*c - 1 - 3*z*z, c)

    def reduce_numerator(value):
        numerator, _ = sp.fraction(sp.cancel(value))
        return sp.factor(sp.rem(sp.Poly(numerator, c), relation).as_expr())

    b = N.G[0] + N.G[1] + N.G[2]
    eta = np.diag(N.SIG).astype(object)
    ck("BOOST_MINIMAL_POLYNOMIAL", np.array_equal(b @ b @ b, 3*b))
    u = N.I + z*b + (c-1)*(b @ b)/3
    ui = eta @ u.T @ eta
    ck("SOURCE_INVERSE_LORENTZ", all(
        reduce_numerator(x) == 0 for x in (u.T @ eta @ u - eta).flat))
    ck("SOURCE_INVERSE_DETERMINANT_ONE", reduce_numerator(sp.Matrix(u).det()-1) == 0)
    ck("SOURCE_INVERSE_TIME_ORIENTATION", u[0, 0] == c)
    ck("SOURCE_INVERSE_ODD_CURVATURE", all(
        reduce_numerator(x) == 0 for x in ((u-ui)/2-z*b).flat))
    t = 2*z/(1+c)
    denominator = 4 - 3*t*t
    ck("POSITIVE_CAYLEY_DENOMINATOR", reduce_numerator(denominator-8/(1+c)) == 0)
    ck("EXACT_PRESCRIBED_RESPONSE_SCALAR", reduce_numerator(4*t/denominator-z) == 0)
    cayley = N.I + (4*t*b+2*t*t*(b @ b))/denominator
    ck("IDENTIFICATION_WITH_OWNED_COMPLETE_EULER_FIELD", all(
        reduce_numerator(x) == 0 for x in (u-cayley).flat))
    ck("SOURCE_SIGN_MUTATION_IS_REJECTED", reduce_numerator(4*t/denominator+z) != 0)
    owner = full_boost_polynomial()
    ck("COMPLETE_OWNER_RESPONSE_CONVENTION",
       owner["metric_numerator"] == "4*t*D^3*sigma_p*(0,0,0,0,-1,1,1,-1,1,-1)")
    return {"source_to_response_input": "z=h^2*h^4=h^6",
            "positive_algebraic_root": "c=sqrt(1+3*z^2)",
            "link": "U=I+z*B+(c-1)*B^2/3",
            "cayley_parameter": "t=2*z/(1+c)",
            "cayley_denominator": "4-3*t^2=8/(1+c)>0",
            "complete_connection_Euler": "zero",
            "complete_metric_Euler": "z*sigma_p*m",
            "nongauge_curvature": "(U-U^(-1))/2=z*B != 0 for every h>0",
            "component": "SO^+(1,3), connected to I along z in [0,h^6]",
            "logarithm": "log(U)=asinh(sqrt(3)*z)*B/sqrt(3)=O(h^6)"}


def prescribed_source_and_norm():
    # This law contains no candidate link, amplitude, or Euler response.
    # L is divisible by four, so it defines a smooth periodic torus source.
    h, y = sp.symbols("h y", positive=True)
    omega = sp.pi/(2*h)
    source = h**4*(sp.cos(omega*y)+sp.sin(omega*y))
    phase_samples = [sp.cos(sp.pi*p/2)+sp.sin(sp.pi*p/2) for p in range(4)]
    ck("PREDECLARED_SOURCE_SAMPLES", phase_samples == list(SIGNS))
    for order in range(6):
        expected = h**4*omega**order*(
            sp.cos(omega*y+order*sp.pi/2)+sp.sin(omega*y+order*sp.pi/2))
        ck("SOURCE_DERIVATIVE_IDENTITY_"+str(order), sp.trigsimp(
            sp.diff(source, y, order)-expected) == 0)
    ck("SOURCE_C3_CONVERGES_TO_ZERO", all(
        sp.limit(h**(4-order), h, 0) == 0 for order in range(4)))
    ck("SOURCE_C4_BOUNDED_C5_UNBOUNDED", h**(4-4) == 1 and
       sp.limit(h**(4-5), h, 0) == sp.oo)
    ck("OWNER_TEN_SLOT_L1_WEIGHT", sum(map(abs, VISIBLE)) == 6)
    raw = 6*h**(-4)*h**6/h**2
    ck("ALL_MESH_NORMALIZED_RAW_GAP_SIX", sp.cancel(raw) == 6)
    ck("VOLUME_NORMALIZATION_CHANGES_TERMINAL", sp.limit(h**4*raw, h, 0) == 0)
    ck("EXACT_ZERO_SOURCE_IS_NOT_SATISFIED", h**6 != 0)
    multiplicities = []
    for length in (4, 8, 12):
        # Each coordinate-0 cycle contains every phase L/4 times; all
        # other L^3 triples merely translate the cycle.
        counts = [sum((x+offset) % 4 == p for x in range(length))
                  for p in range(4) for offset in range(4)]
        ck("PHYSICAL_MULTIPLICITY_L"+str(length), set(counts) == {length//4})
        multiplicities.append({"L": length, "sites_per_phase": length**4//4,
                               "raw_gap": str(6*length**4*F(1, length)**4)})
    return {"background": "Q_h=eta, fixed smooth nondegenerate background",
            "designated_comparator": "K_h^sm=I, Xi(K_h^sm)=0 exactly",
            "prescribed_source_law": "tau_h(x)=h^4*sigma_(sum(x) mod 4)*m",
            "continuum_source_limit": "tau=0",
            "smooth_interpolant": "h^4*(cos(pi*sum(y)/(2*h))+sin(pi*sum(y)/(2*h)))*m",
            "derivative_bound_order_k": "sqrt(2)*(pi/2)^k*h^(4-k), componentwise",
            "regularity": "tau_h -> 0 in C^3; uniformly C^4; not uniformly C^5",
            "joint_equations": "E_K=0 and Xi=h^2*tau_h exactly",
            "raw_owner_norm_gap": "h^(-2)*sum_x sum_j |Xi_j-Xi_j^sm|=6 for every L in 4N",
            "volume_normalized_owner_gap": "6*h^4 -> 0",
            "finite_multiplicity_controls": multiplicities}


def run_checks():
    inverse = exact_source_inverse()
    source = prescribed_source_and_norm()
    return {"schema": "a4d-prescribed-source-owner-topology-v1",
            "input_head": "162fe5edd07586dfdec060c8c99f335d806bd067",
            "arithmetic": "exact polynomial quotient c^2=1+3*z^2 and complete degree-eight owned Euler numerator",
            "source_first_inverse": inverse, "prescribed_source_and_norm": source,
            "verdict": "A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO",
            "scope": "raw owner l1; independently prescribed mesh-dependent sources converging to a smooth limit, even in C^3",
            "exclusions": ["not exact samples of one fixed smooth source",
                           "not the exact discrete vacuum tau_h=0",
                           "not a nonzero continuum stress or a weak-response counterexample",
                           "not a genuinely curved-background witness",
                           "does not decide the stronger fixed-smooth-source formulation"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name("a4d_prescribed_source_owner_topology_results.json")
                               if args.output is None else None)
    if expected:
        ck("PINNED_LEDGER", json.loads(expected.read_text()) == report)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+"\n")
    print("VERDICT", report["verdict"], flush=True)
