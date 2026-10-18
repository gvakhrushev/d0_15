#!/usr/bin/env python3
"""Compare the golden quantile clock with the owned recording engine.

The map algebra is recomputed as a positive control. It is not engine
execution. The owned golden-address cut is the fixed rectangle rule
``axis = len(word) % 4`` with widths ``p`` and ``p**2``. Closed record,
Fock binding, and metric chronology are scanned for a conditional-CDF
placement and are not given a new ``T_rho`` gate.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parents[4]
PIN_REF = "origin/exp/a4d-joint-response-continuation-2026-10-16"
PIN_SHA = "3e4330235b9cea8adae9bb58a2b3e045af89f5d2"
PIN_AT_LEAST = "c3ae03b735dbde690bf1774fc3761846aff93248"
ABSENT_AT = "cd077973b267dfd271d831c78dab2e9fe5b0c2fb"
CERT = "02_REGISTRY/research/certificates/a4d_golden_quantile_clock_source_check.py"
ADDRESS = (
    "02_REGISTRY/research/sources/d0_history_density_palatini_2026-10-16/"
    "check_density_palatini.py"
)
COST = "02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_check.py"
COCYCLE = "02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md"
ENGINE = (
    "02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py",
    "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py",
    "02_REGISTRY/research/certificates/a4d_native_chronological_joint_reduction_check.py",
    ADDRESS,
    COST,
)
MARKERS = (
    "quantile",
    "conditional_cdf",
    "conditional CDF",
    "t_F",
    "T_rho",
    "R_rho",
    "inverse clock",
)
OWNED_COCYCLE = "qρ(ω)=μ(ω) Tr(ρ Mω)"
RESIDUAL = (
    "lapse fixed-cell mass error eps*sin(2*pi*p)/(2*pi)"
    " = -eps*sin(pi*sqrt(5))/(2*pi);"
    " shear: engine keeps the rectangular address boundary x1=p"
    " while (Q12) moves the second boundary with x0"
    " at velocity x0*(sqrt(5)-2)/2"
)


class RetypedClockForgery(RuntimeError):
    """A retyped conditional CDF was presented as engine execution."""


def _require(name: str, ok: bool) -> None:
    if not ok:
        raise ArithmeticError(name)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _show(rev: str, path: str) -> str:
    done = _git("show", f"{rev}:{path}")
    if done.returncode != 0:
        raise RuntimeError(done.stderr.strip() or f"missing {rev}:{path}")
    return done.stdout


def _exists(rev: str, path: str) -> bool:
    return _git("cat-file", "-e", f"{rev}:{path}").returncode == 0


def forged_engine_executes_map(cdf_algebra_ok: bool) -> bool:
    """Hostile checker. Retyping the CDF must not return True."""
    if cdf_algebra_ok:
        raise RetypedClockForgery(
            "retyped conditional CDF does not make engine_executes_map true"
        )
    return False


def read_pin() -> dict[str, object]:
    pin = _git("rev-parse", PIN_REF)
    if pin.returncode != 0:
        raise RuntimeError(pin.stderr.strip() or "pin ref missing")
    sha = pin.stdout.strip()
    if sha != PIN_SHA:
        raise RuntimeError("pin tip moved; re-read before reusing this comparison")
    if len(sha) != 40:
        raise RuntimeError("pin sha is not 40 hex characters")
    ancestor = _git("merge-base", "--is-ancestor", PIN_AT_LEAST, sha)
    if ancestor.returncode != 0:
        raise RuntimeError("pin does not contain the required commit")
    address = _show(sha, ADDRESS)
    start = address.index("def split(leaf):")
    end = address.index("def mass(leaf)", start)
    body = address[start:end]
    for needle in (
        "axis=len(word)%4",
        "b[axis]=red(p*width[axis])",
        "a[axis]=red(a[axis]+p*width[axis])",
    ):
        _require(needle, needle in body)
    for forbidden in ("rho", "eps", "Jacobian", "quantile", "cdf"):
        _require("split_independent_of_" + forbidden, forbidden not in body)
    cost = _show(sha, COST)
    _require("owned_weight", "return p**cost(w)" in cost)
    cocycle = _show(sha, COCYCLE)
    _require("owned_cocycle", OWNED_COCYCLE in cocycle)
    closed = _show(sha, ENGINE[0])
    fock = _show(sha, ENGINE[1])
    chrono = _show(sha, ENGINE[2])
    _require("closed_step", "def step(state):" in closed)
    _require("fock_basis", "def record_basis():" in fock)
    _require("chrono_record", "def record(G, n, dG=None, dn=None):" in chrono)
    hits: list[str] = []
    for path in ENGINE:
        text = address if path == ADDRESS else cost if path == COST else _show(sha, path)
        if path == ENGINE[0]:
            text = closed
        elif path == ENGINE[1]:
            text = fock
        elif path == ENGINE[2]:
            text = chrono
        for marker in MARKERS:
            if marker in text:
                hits.append(f"{path}:{marker}")
    return {
        "pin_sha": sha,
        "pin_at_least": PIN_AT_LEAST,
        "certificate_present_at_tip": _exists(sha, CERT),
        "certificate_present_at_cd077973": _exists(ABSENT_AT, CERT),
        "marker_hits": hits,
        "owned_cocycle": OWNED_COCYCLE,
        "address_rule": "axis=len(word)%4; F width p, R width p**2; no density argument",
    }


def positive_control() -> dict[str, S.Expr]:
    """Recompute (Q8), (Q9), (Q12) and (Q13). This does not call the engine."""
    eps, t, x0, x1, x2, x3 = S.symbols("eps t x0 x1 x2 x3", real=True)
    p = (S.sqrt(5) - 1) / 2
    lapse = 1 + eps * S.cos(2 * S.pi * t)
    cumulative = S.integrate(lapse, (t, 0, t))
    volume = S.simplify(S.integrate(lapse, (t, 0, 1)))
    _require("lapse_volume_one", volume == 1)
    _require(
        "lapse_antiderivative",
        S.simplify(cumulative - (t + eps * S.sin(2 * S.pi * t) / (2 * S.pi))) == 0,
    )
    slope = S.diff(cumulative, t)
    d_eps = S.diff(cumulative, eps)
    dt = S.simplify((-d_eps / slope).subs({t: p, eps: 0}))
    target = S.sin(S.pi * S.sqrt(5)) / (2 * S.pi)
    _require("moving_clock_derivative", S.simplify(dt - target) == 0)
    _require("moving_clock_derivative_nonzero", S.simplify(dt) != 0)
    _require(
        "two_sine_forms",
        S.simplify(S.sin(2 * S.pi * p) + S.sin(S.pi * S.sqrt(5))) == 0,
    )
    fixed_mass = S.simplify(S.integrate(lapse, (t, 0, p)))
    lapse_error = eps * S.sin(2 * S.pi * p) / (2 * S.pi)
    equivalent = -eps * S.sin(S.pi * S.sqrt(5)) / (2 * S.pi)
    _require("fixed_cell_mass", S.simplify(fixed_mass - (p + lapse_error)) == 0)
    _require("lapse_error_forms", S.simplify(lapse_error - equivalent) == 0)
    _require("lapse_error_nonzero", S.simplify(lapse_error.subs(eps, 1)) != 0)
    rho = (1 + eps * x0 * x1) / (1 + eps / 4)
    r0 = (x0 + eps * x0**2 / 4) / (1 + eps / 4)
    r1 = (x1 + eps * x0 * x1**2 / 2) / (1 + eps * x0 / 2)
    coordinates = S.Matrix([x0, x1, x2, x3])
    transport = S.Matrix([r0, r1, x2, x3])
    jacobian = transport.jacobian(coordinates)
    _require("triangular_above_diagonal", all(
        S.simplify(jacobian[i, j]) == 0 for i in range(4) for j in range(i + 1, 4)
    ))
    _require("shear_jacobian", S.simplify(jacobian.det() - rho) == 0)
    velocity = S.Matrix([S.diff(component, eps) for component in transport]).subs(eps, 0)
    divergence = sum(S.diff(velocity[i], coordinates[i]) for i in range(4))
    dlog = S.diff(S.log(rho), eps).subs(eps, 0)
    _require("q13_components", S.simplify(velocity[0] - x0 * (x0 - 1) / 4) == 0)
    _require("q13_second", S.simplify(velocity[1] - x0 * x1 * (x1 - 1) / 2) == 0)
    _require("q13_divergence", S.simplify(divergence - (x0 * x1 - S.Rational(1, 4))) == 0)
    _require("q13_matches_log_density", S.simplify(divergence - dlog) == 0)
    d_r1 = S.diff(r1, x1)
    wall = S.simplify((-(S.diff(r1, eps)) / d_r1).subs({eps: 0, x1: p}))
    expected_wall = x0 * (S.sqrt(5) - 2) / 2
    _require("golden_cube", S.simplify(p**3 - (S.sqrt(5) - 2)) == 0)
    _require("q12_wall_velocity", S.simplify(wall - x0 * p**3 / 2) == 0)
    _require("q12_wall_closed_form", S.simplify(wall - expected_wall) == 0)
    _require("q12_wall_depends_on_x0", S.simplify(S.diff(wall, x0)) != 0)
    _require("q12_wall_not_identically_zero", S.simplify(wall.subs(x0, 1)) != 0)
    return {
        "p": p,
        "dt": dt,
        "lapse_error": lapse_error,
        "fixed_mass": fixed_mass,
        "moving_mass": p,
        "wall_velocity": wall,
        "divergence": divergence,
    }


def engine_rectangles(p: S.Expr) -> dict[str, S.Expr]:
    """Reading of the owned split. Not a conditional-CDF placement."""

    def box(word: str) -> tuple[list[S.Expr], list[S.Expr], int]:
        lo = [S.Integer(0)] * 4
        width = [S.Integer(1)] * 4
        cost = 0
        for index, letter in enumerate(word):
            axis = index % 4
            if letter == "F":
                width[axis] = S.simplify(p * width[axis])
                cost += 1
            elif letter == "R":
                lo[axis] = S.simplify(lo[axis] + p * width[axis])
                width[axis] = S.simplify((p**2) * width[axis])
                cost += 2
            else:
                raise ValueError(letter)
        mass = S.simplify(S.prod(width))
        _require("engine_box_mass_" + word, S.simplify(mass - p**cost) == 0)
        return lo, width, cost

    first = box("F")
    second = box("FF")
    _require("engine_time_interval", first[0][0] == 0 and S.simplify(first[1][0] - p) == 0)
    _require("engine_second_wall", second[0][1] == 0 and S.simplify(second[1][1] - p) == 0)
    x0 = S.symbols("x0", real=True)
    _require("engine_second_wall_ignores_x0", S.diff(second[1][1], x0) == 0)
    return {"time_end": first[1][0], "second_wall": second[1][1]}


def run() -> dict[str, object]:
    algebra = positive_control()
    try:
        forged_engine_executes_map(True)
    except RetypedClockForgery:
        forgery_rejected = True
    else:
        raise RetypedClockForgery("negative control returned without raising")
    pin = read_pin()
    if pin["marker_hits"]:
        raise RuntimeError(
            "owned engine gained a conditional-CDF marker: "
            + ",".join(pin["marker_hits"])
        )
    rectangles = engine_rectangles(algebra["p"])
    lapse_zero = S.simplify(algebra["lapse_error"]) == 0
    shear_gap = S.simplify(algebra["wall_velocity"] - 0)
    shear_zero = shear_gap == 0
    _require("engine_time_is_fixed_p", S.simplify(rectangles["time_end"] - algebra["p"]) == 0)
    _require("engine_wall_is_fixed_p", S.simplify(rectangles["second_wall"] - algebra["p"]) == 0)
    _require(
        "shear_gap_is_map_velocity",
        S.simplify(shear_gap - algebra["wall_velocity"]) == 0,
    )
    # No scanned primitive computes T_rho. Marker hits abort above.
    owned_executes = False
    sources_coincide = bool(lapse_zero and shear_zero)
    engine_executes_map = bool(owned_executes and sources_coincide)
    if engine_executes_map or sources_coincide:
        residual: object = "exact zero"
    else:
        residual = RESIDUAL
    if engine_executes_map and not (lapse_zero and shear_zero):
        raise ArithmeticError("execution flag without zero residuals")
    if sources_coincide and not (lapse_zero and shear_zero):
        raise ArithmeticError("coincidence flag without zero residuals")
    gr_derived = False
    qrho_identified_with_mu = False
    if gr_derived or qrho_identified_with_mu:
        raise ArithmeticError("forbidden identification")
    return {
        "engine_executes_map": engine_executes_map,
        "sources_coincide": sources_coincide,
        "gr_derived": gr_derived,
        "residual": residual,
        "qrho_identified_with_mu": qrho_identified_with_mu,
        "owned_cocycle": pin["owned_cocycle"],
        "pin_sha": pin["pin_sha"],
        "pin_at_least": pin["pin_at_least"],
        "certificate_present_at_tip": pin["certificate_present_at_tip"],
        "certificate_present_at_cd077973": pin["certificate_present_at_cd077973"],
        "ci_ran_absent_certificate": False,
        "marker_hits": pin["marker_hits"],
        "address_rule": pin["address_rule"],
        "forgery_rejected": forgery_rejected,
        "positive_control": True,
        "dt_tF": "sin(pi*sqrt(5))/(2*pi)",
        "lapse_mass_error": "eps*sin(2*pi*p)/(2*pi)",
        "shear_wall_velocity": "x0*(sqrt(5)-2)/2",
        "moving_cell_mass": "p",
    }


if __name__ == "__main__":
    result = run()
    print(
        "engine_executes_map={0} sources_coincide={1} gr_derived={2} residual={3}".format(
            str(result["engine_executes_map"]).lower(),
            str(result["sources_coincide"]).lower(),
            str(result["gr_derived"]).lower(),
            result["residual"],
        )
    )
