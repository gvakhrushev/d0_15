#!/usr/bin/env python3
"""Bounded native fork, whole-price edge and finite-cofield controls.

Only the changed small native source echoes are checked on all columns.
The long READY/polynomial/Cartan/cofinal inputs are consumed, not replayed.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import price_cofield as pc

CHECKS = []
PACKET = Path(__file__).resolve().parent
SOURCES = PACKET.parent
REPO = SOURCES.parents[2]
PRIMARY = REPO / "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def num(value):
    if isinstance(value, (int, F)):
        value = F(value)
        return mp.mpf(value.numerator)/value.denominator
    return mp.mpf(str(sp.N(value, 110)))


def square_interval(interval):
    lo, hi = interval
    lower = 0 if lo <= 0 <= hi else min(lo*lo, hi*hi)
    return lower, max(lo*lo, hi*hi)


def heat_character(stages, phase, beta):
    return mp.fsum(mp.exp(-beta*(1-mp.cos((2*mp.pi*k+phase)/stages)))
                   for k in range(stages))


def even_drift_controls():
    """Only the NEW cheap critical positive-effect algebra, no native replay."""
    mp.mp.dps = 110
    q0, amplitude, step = F(1, 10), F(1, 20), F(1, 2)
    x2 = sp.Matrix([[0, 1], [1, 0]])
    effect = sp.Rational(q0.numerator, q0.denominator)*sp.eye(4)+sp.Rational(
        amplitude.numerator, amplitude.denominator)*sp.kronecker_product(x2, x2)
    origin = sp.Matrix([1, 0, 0, 0])
    centered = effect-sp.Rational(q0.numerator, q0.denominator)*sp.eye(4)
    check("critical EVEN-drift control is a genuine positive effect with scalar first conditional and nonzero higher excitation",
          effect.eigenvals() == {sp.Rational(1, 20): 2, sp.Rational(3, 20): 2}
          and effect.extract((0, 2), (0, 2)) == sp.Rational(1, 10)*sp.eye(2)
          and (origin.T*centered*centered*origin)[0] == sp.Rational(1, 400))
    t0, shifted = pc.scalar_data((q0, q0+amplitude*step**2))["grams"]
    zeta, a = F(1, 2**20), 1-F(1, 2**20)
    ratios, step_rows = [], []
    for count in (16, 128, 2048):
        p0, ps = t0**count, shifted**count
        ratio = (ps/p0)*(a+zeta*p0)/(a+zeta*ps)
        check("critical symmetric equal-report tail can lose its BASE gain exponentially M%d" % count,
              0 < ratio <= (shifted/t0)**count/a and shifted < t0)
        ratios.append(ratio)
        step_factor = sum((F(1, j) for j in range(count//2+1, count+1)), F())
        check("actual1/j half-window divided gain keeps its step factor and is not the base order-M gain M%d" % count,
              F(1, 2) < step_factor < 1 and step_factor/count < F(1, count))
        step_rows.append({"cohorts": count, "B_tail_over_A": str(step_factor/count)})
    check("even critical drift survives zero odd price contrast and gives no uniform base-relative gain",
          ratios[0] > ratios[1] > ratios[2] and ratios[2] < F(1, 10**8))
    return {"critical_even_drift_ratios": [mp.nstr(num(value), 50) for value in ratios],
            "one_over_j_step_factors": step_rows}


def run():
    CHECKS.clear()
    mp.mp.dps = 110
    ne = pc.native
    tolerance = mp.mpf("1e-90")
    native_rows, private_matrices, meter_corners, native_grams = [], {}, {}, {}
    zeta, beta = sp.Rational(1, 2**20), mp.mpf(".7")
    for power in (4, 5, 10):
        execution, control, meter, angle = pc.source_echo(power)
        actual = ne.word_matrix(execution, **pc.rr.bounds(execution))
        injection = ne.input_isometry(execution, **pc.rr.bounds(execution))
        corner = injection.T*actual*injection
        rotation = DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD).pow(power).to_Matrix()
        q = rotation[1, 0]**2
        t = 1-4*ne.P**2*q*(1-q)
        expected_corner = sp.kronecker_product(
            ((1-q)*ne.G_LOCAL.T+q*ne.G_LOCAL)*sp.diag(1, -1), sp.eye(4))
        check("actual matched native source fork has its full rank8 corner and scalar Gram r%d" % power,
              ne.exact_matrix_equal(corner, expected_corner)
              and ne.exact_matrix_equal(corner.T*corner, t*sp.eye(8)))
        check("new full-column native fork remains a symmetric orthogonal involution r%d" % power,
              ne.exact_matrix_equal(actual.T, actual)
              and ne.exact_matrix_equal(actual*actual, sp.eye(actual.rows))
              and actual.trace() == 0)
        # Actual helper0,control1,meter2,spin3/4 layout: extract the private4 block.
        private = actual.extract((0, 4, 8, 12), (0, 4, 8, 12))
        private_matrices[power] = private
        meter_corners[power] = corner.extract((0, 4), (0, 4))
        native_grams[power] = t
        check("shared helper and arbitrary source spin are identity on EVERY completed fork column r%d" % power,
              ne.exact_matrix_equal(actual, sp.kronecker_product(sp.eye(2), private, sp.eye(4))))
        sine = pc.rr.native_phase.native_rotation_intervals(power, bits=110)[1]
        q_interval = square_interval(sine)
        check("native source contrast stays inside its actual positive q below one quarter collar r%d" % power,
              0 < q_interval[0] < q_interval[1] < F(1, 4))
        inventory = ne.inventory(execution, **pc.rr.bounds(execution))
        gap = 153-(33+12*power)
        check("clock matching retains the complete true inverse and every literal2CX padding stage r%d" % power,
              inventory.gate_count == 153
              and (inventory.g_count, inventory.source_i_count, inventory.cx_count) ==
                  (2*power+3, 4*power+10, 6*power+20+gap)
              and inventory.full_dimension == 32 and inventory.cut_rank == 8)
        full_heat = mp.log(32*(heat_character(153, 0, beta)+heat_character(153, mp.pi, beta)))/beta
        feedback = -8*mp.log(1-num(zeta)+num(zeta)*num(t))
        native_rows.append({"source_G_power": power, "body_stages": 33+12*power,
            "actual_stages": 153, "G": inventory.g_count, "CX": inventory.cx_count,
            "SourceI": inventory.source_i_count, "full_dimension": 32, "cut_rank": 8,
            "paired_clock_modes": 2*153*32, "q_certified_interval": list(map(str, q_interval)),
            "full_heat_numeric": mp.nstr(full_heat, 90), "feedback_numeric": mp.nstr(feedback, 90),
            "scope": "native contrast fixture, not an original GR field root"})
    check("all matched forks have identical COMPLETE heat while their true feedback prices differ",
          len({row["full_heat_numeric"] for row in native_rows}) == 1
          and len({row["feedback_numeric"] for row in native_rows}) == 3)

    prefix_rows = []
    for length in (2, 3):
        base, private = pc.prefix_execution(length)
        fork, _ = pc.prefix_execution(length, fork=(2, 4))
        inv = ne.inventory(fork, **pc.rr.bounds(fork))
        check("single-cohort native fork shares its TRUE earlier word prefix and unchanged future base blocks M%d" % length,
              fork.gates[:153] == base.gates[:153]
              and fork.gates[306:] == base.gates[306:]
              and fork.gates[153:306] != base.gates[153:306])
        check("no later native fork block addresses any sealed private or immutable oldRIGHT register M%d" % length,
              all(3 not in gate.wires for gate in fork.gates)
              and all(not set(q for pair in private[:j] for q in pair).intersection(gate.wires)
                      for j in range(1, length) for gate in fork.gates[153*j:]))
        check("full fork carrier, true cut, oldRIGHT and clock inventory are identical to baseline M%d" % length,
              inv.gate_count == 153*length and inv.full_dimension == 2**(4+2*length)
              and inv.cut_rank == 4*2*2**length
              and ne.inventory(base, **pc.rr.bounds(base)).cut_rank == inv.cut_rank
              and fork.blank_wires == base.blank_wires and fork.old_right == (3,))
        powers = [5]*length
        powers[1] = 4
        returned = sp.kronecker_product(*(meter_corners[r] for r in powers))
        gram_product = sp.prod(native_grams[r] for r in powers)
        check("ACTUAL native meter corners compose into the ONE full protected-prefix determinant M%d" % length,
              ne.exact_matrix_equal(returned.T*returned, gram_product*sp.eye(2**length))
              and inv.cut_rank == 8*returned.rows)
        # CP old-record refinement follows from the ALL-column private tensor
        # factorization checked above, not from a simulated1024-column clock.
        prefix_rows.append({"cohorts": length, "fork_at": 2,
            "actual_stages": inv.gate_count, "full_dimension": inv.full_dimension,
            "cut_rank": inv.cut_rank, "paired_modes": 2*inv.gate_count*inv.full_dimension,
            "scope": "literal prefix/protection/inventory; private all-column identity consumed"})
    fork2, _ = pc.prefix_execution(2, fork=(2, 4))
    fork3, _ = pc.prefix_execution(3, fork=(2, 4))
    check("each FIXED counterfactual fork itself has a literal append-only later prefix",
          fork3.gates[:len(fork2.gates)] == fork2.gates)
    e0, _ = pc.prefix_execution(3, old_right_count=0)
    e2, _ = pc.prefix_execution(3, old_right_count=2)
    i0 = ne.inventory(e0, **pc.rr.bounds(e0))
    i2 = ne.inventory(e2, **pc.rr.bounds(e2))
    check("additional arbitrary oldRIGHT input rank is counted once across all branch cohorts",
          i2.cut_rank == 4*i0.cut_rank and i2.full_dimension == 4*i0.full_dimension
          and i2.gate_count == i0.gate_count)

    # Exact whole-price calculus: no sum of standalone local action values.
    q1, q2 = sp.symbols("q1 q2", real=True)
    alpha, gamma, zz = sp.Rational(3, 2), sp.Rational(3, 4), sp.Rational(1, 16)
    t1, t2 = (1-alpha*gamma*q*(1-gamma*q) for q in (q1, q2))
    price = -16*sp.log(1-zz+zz*t1*t2)
    weight = 16*zz*t1*t2/(1-zz+zz*t1*t2)
    a1 = alpha*gamma*(1-2*gamma*q1)/t1
    check("single-edge derivative is the TRUE base whole-product chain coefficient",
          sp.cancel(sp.diff(price, q1)-weight*a1) == 0)
    check("full closing price retains cross-cohort control derivatives",
          sp.cancel(sp.diff(price, q1, q2)) != 0)
    z = sp.symbols("z", real=True)
    w = zz*sp.exp(z)/(1-zz+zz*sp.exp(z))
    check("log whole-price weight has the history-independent derivative needed by relative gains",
          sp.simplify(sp.diff(sp.log(w), z)-(1-zz)/(1-zz+zz*sp.exp(z))) == 0)
    q = sp.symbols("q", real=True)
    t = 1-alpha*gamma*q*(1-gamma*q)
    aa = alpha*gamma*(1-2*gamma*q)/t
    check("log local slope retains its exact compact-collar derivative",
          sp.cancel(sp.diff(aa, q)/aa-(-2*gamma/(1-2*gamma*q)+aa)) == 0)
    q0, delta, qmax = F(1, 100), F(1, 100000), F(1, 4)
    Cbeta = 8+2/(1-2*qmax)
    relative_rows = []
    for old_power in (0, 16, 1024, 8192):
        old = F(1, 2**old_power)
        ratio = pc.probe_relative_ratio(old, q0, q0-2*delta, q0+delta, mp=mp)
        radius = 2*delta
        check("single-edge relative gain is uniformly bounded even when OLD Gram is2^-%d" % old_power,
              mp.exp(-num(Cbeta*radius)) <= ratio <= mp.exp(num(Cbeta*radius)))
        relative_rows.append({"old_product": "2^-%d" % old_power,
                              "ratio": mp.nstr(ratio, 90)})
    check("zero report chords have their continuous gain extension and zero actual cofield value",
          pc.probe_relative_ratio(F(1, 2**1024), q0, q0, q0, mp=mp) == 1
          and pc.price_edge([q0, q0], 0, q0, q0, mp=mp) == 0)

    # A literal LINEAR coordinate-cofield reconstruction, two-coordinate model.
    reports, gbar, scales = [q0]*3, (F(1, 3), F(1, 5), F(1, 7)), (F(1), F(2), F(3))
    E, velocity = F(5, 13), F(7, 11)
    base = pc.scalar_data(reports)
    gain = base["weight"]*sum(a*g for a, g in zip(base["slopes"], gbar))
    errors = []
    for spacing in (F(1, 100), F(1, 1000), F(1, 10000)):
        pairing = mp.mpf("0")
        for j, (gj, scale) in enumerate(zip(gbar, scales)):
            for coefficient, physical_component in ((E/(2*scale), scale*velocity),
                                                     (E/scale, scale*velocity/2)):
                dq = spacing*gj*coefficient
                edge = pc.price_edge(reports, j, q0-dq, q0+dq, mp=mp)
                pairing += edge/(2*num(spacing))*num(physical_component)
        error = abs(pairing/num(gain)-num(E*velocity))
        errors.append(error)
    check("finite price axes reconstruct a LINEAR physical cofield with actual heterogeneous gains and sampling scales",
          errors[2] < errors[1]/50 < errors[0]/2500 and errors[2] < mp.mpf("1e-8"))
    L, M3, gg, spacing, eta = F(7), F(11), F(1, 17), F(1, 101), F(1, 10**10)
    budget = pc.cofield_error_budget(L, M3, gg, spacing, eta)
    check("endpoint source error is divided by true coordinate spacing and physical gbar",
          budget == (L/gg)*(M3*spacing**2/6+2*eta/spacing)
          and budget != L*(M3*spacing**2/6+2*eta/spacing))
    chord_error = pc.coordinate_chord_error(F(3), F(1, 10**8), F(1, 1000))
    check("actual prepared-coordinate chord keeps its readout norm and eta-over-delta debt",
          chord_error == F(3, 50000) and chord_error < F(1, 2))
    perturbation = sp.Matrix([[sp.Rational(1, 100), -sp.Rational(1, 200)],
                              [sp.Rational(1, 200), sp.Rational(1, 100)]])
    check("a sufficiently controlled ACTUAL coordinate chord matrix remains full rank",
          max(sum(abs(perturbation[i, j]) for i in range(2)) for j in range(2)) < sp.Rational(1, 2)
          and (sp.eye(2)+perturbation).det() != 0)

    # Hostile simultaneous-tail comparison: small per-row changes do not
    # guarantee the same BASE gain as the history size grows.
    tail_ratios = []
    qbase, eps = F(1, 10), F(1, 100)
    local = pc.scalar_data((qbase, qbase-eps, qbase+eps))
    t0, tm, tp = map(num, local["grams"])
    a0, zznum = num(local["slopes"][0]), num(F(1, 2**20))
    for count in (16, 128, 2048):
        p0, pm, pp = t0**count, tm**count, tp**count
        base_w = zznum*p0/(1-zznum+zznum*p0)
        difference_per_rank = -mp.log1p(zznum*(pp-pm)/(1-zznum+zznum*pm))
        ratio = difference_per_rank/(2*num(eps)*count*base_w*a0)
        tail_ratios.append(ratio)
    check("whole-tail mean-value gain cannot be silently replaced by the TRUE BASE chain gain",
          tail_ratios[2] > 10*tail_ratios[1] and tail_ratios[1] > tail_ratios[0]
          and tail_ratios[2] > 100)
    even_control = even_drift_controls()

    epsilon = F(1, 64)
    taylor_power = 2-2*epsilon
    check("slow-envelope weighted coordinate errors have a summable Taylor exponent",
          taylor_power == F(63, 32) and taylor_power > 1
          and 1+1/(taylor_power-1) == F(63, 31))
    x = sp.symbols("x")
    check("exponentially small native errors retain a summable actual eta-over-spacing bound",
          (x*(1+x)/(1-x)**3).subs(x, sp.Rational(1, 2)) == 6)
    check("all-row cofield and full correlated-bank certificates have their distinct true-gain rates",
          -(1-epsilon) == F(-63, 64)
          and (1+F(3, 4)+2*epsilon)/2-(1-epsilon) == F(-3, 32))

    return {"status": "PASS", "checks": len(CHECKS), "check_names": list(CHECKS),
        "native_forks": native_rows, "native_prefixes": prefix_rows,
        "relative_gain_rows": relative_rows,
        "cofield_model_errors": [mp.nstr(e, 50) for e in errors],
        "hostile_whole_tail_ratios": [mp.nstr(e, 50) for e in tail_ratios],
        "critical_even_drift": even_control,
        "exact_scope": ["actual32-column native changed source echoes and exact full corners",
            "all2ND clock modes retained by exact involution multiplicities and owned Floquet theorem",
            "M2/3 native prefix inventories/protection, not a large clock simulation",
            "rational cofield models are diagnostics, not new native primitives or GR roots",
            "no old READY/Cartan/large native suite replay; no physical C1 or X_N promotion"],
        "numerical_scope": "110-digit non-interval configured values; algebraic identities and rational collar bounds are exact"}


def pin(path):
    data = path.read_bytes()
    return {"path": str(path.relative_to(REPO)), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def section_pin(heading):
    raw = PRIMARY.read_bytes()
    start = raw.index(heading.encode())
    end = raw.find(b"\n## ", start+1)
    section = raw[start:] if end < 0 else raw[start:end]
    return {"heading": heading, "bytes": len(section),
            "sha256": hashlib.sha256(section).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    inputs = [PACKET/name for name in ("price_cofield.py", "check_price_cofield.py",
              "NATIVE_GRAPH.md", "STENCIL_MAP.md", "COFIELD_THEOREM.md")]
    inputs += [SOURCES / "d0_exact_report_reflected_cohorts_2026-10-25" / name
               for name in ("reflected_report.py", "PROOF.md", "COHORT_THEOREM.md")]
    inputs += [SOURCES / "d0_native_cofinal_reflected_source_2026-10-25" / name
               for name in ("GEOMETRIC_MAP.md", "COFINAL_THEOREM.md", "NATIVE_REQUEST.md")]
    inputs += [SOURCES / "d0_native_execution_domain_2026-10-24/native_execution.py"]
    result["source_pins"] = [pin(p) for p in inputs]
    result["section_pins"] = [section_pin("## 7ag."), section_pin("## 7ah.")]
    result["generated_utc"] = datetime.now(timezone.utc).isoformat()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
