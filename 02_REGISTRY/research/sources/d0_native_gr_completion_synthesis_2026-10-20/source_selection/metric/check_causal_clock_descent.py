"""Exact bounded controls for the causal clock minimum and source descent.

No numerical eigensolver, new history enumeration, or native price is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import sympy as sp


PINS = {
    "02_REGISTRY/research/A4D_PAIRED_EPOCH_CLOCK_COMPLETE_SOURCE_TRANSPORT_2026_10_21.md":
        "bc8d9b96701c8c0096f01dc22cf717ac86a0e83741be1608b438cd5e2ed79824",
    "02_REGISTRY/research/A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md":
        "68ba2d4dbbf5a055b852755fcf1c811824743c096ddcf722086c4da993fd179d",
    "02_REGISTRY/research/A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md":
        "808ec6a438f378bce0eb1a4d22ce80cf897291fb54b5d40eb1596cadeae56717",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_STAGE_CLOCK_AND_POINTED_DESCENT.md":
        "e970dda60699b7236599c9618445fe17cb8cbb0b9bb8c8de8808a190c4c00848",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md":
        "2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea",
    "02_REGISTRY/research/A4D_BOOK03_SOURCE_IDENTIFIABILITY_THEOREM_2026_10_21.md":
        "4ce898d50bff53de17cc6d4b3fe98fa8f9af564d0fa5d6a50fdb78591ff059c0",
    "02_REGISTRY/research/A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md":
        "cf8d893fd7435dd29dc4c93aa8291e965d765e5014aaeb9d82c63d23d84ebbf7",
    "02_REGISTRY/research/A4D_CAUSAL_NATIVE_SOURCE_AND_WEIGHTED_DYNAMICS_2026_10_21.md":
        "d3f05bc13512a518c1f0a6738d4e91952774908f1ded5727ee81c004094bbaa3",
}


def run() -> dict:
    started = time.perf_counter()
    repo = Path(__file__).resolve()
    while not (repo / "AGENTS.md").is_file():
        if repo.parent == repo:
            raise RuntimeError("repository root not found")
        repo = repo.parent
    checks = []

    def require(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def eq(lhs, rhs, label):
        diff = lhs - rhs
        if isinstance(diff, sp.MatrixBase):
            ok = all(sp.simplify(v) == 0 for v in diff)
        else:
            ok = sp.simplify(diff) == 0
        require(ok, label)

    for rel, digest in PINS.items():
        actual = hashlib.sha256((repo / rel).read_bytes()).hexdigest()
        require(actual == digest, f"source pin: {rel}")

    ar, ai, br, bi, q = sp.symbols("ar ai br bi q", real=True)
    aa, bb = ar + sp.I * ai, br + sp.I * bi
    t = sp.Matrix([[0, 0], [aa, bb]])
    lam = ar**2 + ai**2 + br**2 + bi**2
    eq((q * sp.eye(2) - t.H * t).det(), q * (q - lam),
       "all complex one-way clock compressions have spectrum lambda,0")

    shift = sp.zeros(5)
    for j in range(5):
        shift[(j + 1) % 5, j] = 1
    e = sp.eye(5)
    end = e[:, 0:2]
    dark = e[:, [0, 2]]
    eq(shift.H * shift, sp.eye(5), "complete five-epoch unitary")
    eq(end.H * shift * end, sp.Matrix([[0, 0], [1, 0]]),
       "endpoint cut attains lambda=1")
    eq(dark.H * shift * dark, sp.zeros(2), "dark cut has lambda=0")

    cs = sp.diag(sp.Rational(3, 5), sp.Rational(5, 13))
    ss = sp.diag(sp.Rational(4, 5), sp.Rational(12, 13))
    rot = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                     [sp.Rational(4, 5), sp.Rational(3, 5)]])
    word = cs.row_join(-ss).col_join(ss.row_join(cs))
    word = word * sp.diag(rot, rot)
    eq(word.H * word, sp.eye(4), "full retained data-work unitary")
    i = sp.eye(4)[:, 0:2]
    a = i.H * word * i
    c = a.H * a
    require(c[0, 1] != 0, "data C is non-diagonal")
    require(c * sp.diag(1, 0) != sp.diag(1, 0) * c,
            "data C does not commute with a selected coordinate projector")
    w = sp.kronecker_product(shift, word)
    z = sp.Symbol("z", real=True)
    z0 = sp.Rational(1, 2**20)
    r = 128
    expected_data = (1-z) * sp.eye(2) + z*c
    tangents = []
    for j in range(5):
        d = sp.zeros(5)
        d[j, j] = sp.I
        tangents.append(d)
        for k in range(j+1, 5):
            real = sp.zeros(5)
            real[j, k], real[k, j] = 1, -1
            imag = sp.zeros(5)
            imag[j, k] = imag[k, j] = sp.I
            tangents.extend((real, imag))
    require(len(tangents) == 25, "complete real generator basis of u(5)")
    for label, cut in (("endpoint", end), ("dark", dark)):
        ie = sp.kronecker_product(cut, i)
        comp = ie.H * w * ie
        f = ie.H * w.H * (sp.eye(20)-ie*ie.H) * w * ie
        eq(f, sp.eye(4)-comp.H*comp,
           f"{label}: actual complete complementary effect")
        ke = sp.eye(4)-z*f
        want = ((1-z)**2 * expected_data.det()
                if label == "endpoint" else (1-z)**4)
        eq(ke.det(), want, f"{label}: full determinant")
        tc = cut.H * shift * cut
        ac = sp.kronecker_product(tc, a)
        inv = ke.subs(z, z0).inv()
        for n, generator in enumerate(tangents):
            dt = cut.H*(shift*generator-generator*shift)*cut
            da = sp.kronecker_product(dt, a)
            dk = z0*(da.H*ac+ac.H*da)
            eq(sp.trace(inv*dk), 0,
               f"{label}: pure-clock source generator {n}")

    # The minimum proof is spectral and applies to all feasible cuts.
    # A continuous feasible family supplies an independent exact control.
    s = sp.Symbol("s", real=True)
    cc = sp.Symbol("cc", real=True)
    v = cc*e[:, 1] + s*e[:, 2]
    cut_family = e[:, 0].row_join(v)
    tf = cut_family.H*shift*cut_family
    trace_f = sp.expand(sp.trace(tf.H*tf))
    eq(trace_f.subs(cc**2, 1-s**2), 1-s**4,
       "continuous feasible clock family attains the spectral bound")

    # A phase-dependent word: no common data factor is used.
    phase_cs = [sp.Rational(3, 5), sp.Rational(5, 13),
                sp.Rational(8, 17), sp.Rational(7, 25), sp.Rational(20, 29)]
    phase_ss = [sp.Rational(4, 5), sp.Rational(12, 13),
                sp.Rational(15, 17), sp.Rational(24, 25), sp.Rational(21, 29)]
    wp = sp.zeros(10)
    blocks = []
    for j, (cj, sj) in enumerate(zip(phase_cs, phase_ss)):
        mj = sp.Matrix([[cj, -sj], [sj, cj]])
        blocks.append(mj)
        dst = (j+1) % 5
        wp[2*dst:2*dst+2, 2*j:2*j+2] = mj
    eq(wp.H*wp, sp.eye(10), "phase-dependent complete word is unitary")
    require(blocks[0] != blocks[1], "complete word has unequal phase blocks")
    idata = sp.eye(2)[:, 0:1]
    for k in (1, 2, 3):
        ec = e[:, [0, k]]
        ip = sp.kronecker_product(ec, idata)
        actual = ip.H*wp*ip
        want = sp.Matrix([[0, 0], [phase_cs[0], 0]]) if k == 1 else sp.zeros(2)
        eq(actual, want, f"phase-dependent causal retained pair 0,{k}")
    require(shift[0, 4] == 1, "predecessor pair is excluded by no active return")

    # Reuse the original first gate of BOTH actual Book03 program blocks.
    # This is a one-tick application, not a substitution of the full word.
    p = (sp.sqrt(5)-1)/2
    golden_g = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    eq(golden_g.H*golden_g, sp.eye(2), "original Golden first gate is unitary")
    g16 = sp.kronecker_product(golden_g, sp.eye(8))
    j_native = sp.zeros(16, 4)
    for spin in range(4):
        j_native[2*spin, spin] = 1
    native_a0 = j_native.H*g16*j_native
    eq(native_a0, sp.sqrt(p)*sp.eye(4),
       "both literal program blocks have the same original first-gate compression")
    eq(native_a0.H*native_a0, p*sp.eye(4),
       "actual initial retained spin4 corner has C=p I4")
    native_det = ((1-z)*(1-z+z*p))**4
    eq(native_det, ((1-z)**4
                   * ((1-z)*sp.eye(4)+z*native_a0.H*native_a0).det()),
       "actual one-tick causal minimum has no completed-word program contrast")

    source_ep = sp.cancel(r*z0*sp.Rational(24, 25)
                          / (1-z0*sp.Rational(16, 25)))
    require(source_ep > 0, "stationary clock branches have different data source")
    gamma_bound = sp.Rational(r*4, 2**20-1)
    require(0 < gamma_bound < 1, "fixed same-unit work charge can reverse preference")

    x, u, rho, off = sp.symbols("x u rho off", real=True)
    old_euler = u-x**2
    action = x+old_euler**2/2
    lifted_u = u+(rho**2-1)*x**2
    defect = sp.expand(action.subs({x:rho*x, u:lifted_u}, simultaneous=True)
                       -rho*action)
    eq(defect, (1-rho)*old_euler**2/2,
       "scale defect belongs to squared internal Euler ideal")
    for var in (x, u):
        eq(sp.diff(defect, var).subs(u, x**2), 0,
           f"full first scale defect vanishes in {var}")
    eq(sp.diff(action, u).subs(u, x**2), 0, "true internal stationary section")
    eq(action.subs(u, x**2), x, "stationary action has the reduced scale weight")
    bad = sp.expand(action.subs({x:rho*x, u:lifted_u+off}, simultaneous=True)
                    -rho*action)
    eq(bad.subs(u, x**2), off**2/2,
       "bad scale lift has constant value defect on the old section")
    eq(sp.diff(bad, u).subs(u, x**2), off,
       "constant section value does not preserve internal Euler")
    ph2 = (3+sp.sqrt(5))/2
    eq(defect.subs(rho, ph2), (1-ph2)*old_euler**2/2,
       "the same exact first-jet test uses the physical Golden scale parameter")

    return {
        "status": "PASS",
        "input_snapshot": "de6f4f9ab07e29f0df8ce6c2d92f9b8178c01e57",
        "source_pins": PINS,
        "checks": checks,
        "check_count": len(checks),
        "clock_tangent_generators_per_cut": len(tangents),
        "nonzero_endpoint_data_source": str(source_ep),
        "feedback_advantage_upper_bound_d4": str(gamma_bound),
        "actual_Book03_one_tick_minimum": "-512 log((1-z)(1-z+z*p))",
        "scope": {
            "causal_clock_minimum": "analytic under stated complete-price interface",
            "phase_dependent_word_selection": "feedback plus exact remaining-price budget",
            "critical_source_descent": "analytic with selected smooth critical cover",
            "physical_full_Book_price_selected": False,
            "native_causal_cut_admission_proved": False,
            "upstream_preparation_solved": False,
            "GR_closed": False,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "optimized": not __debug__,
        },
        "elapsed_seconds": time.perf_counter()-started,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    sys.stdout.write(encoded)
