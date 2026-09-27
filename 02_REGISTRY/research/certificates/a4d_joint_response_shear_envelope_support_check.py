#!/usr/bin/env python3
"""The period-2 shear jet has no root-of-unity envelope outside its sign group.

Every link in the bare jet and in the corrected order-u^5 jet depends on the
site only through sigma(x)=(-1)^{x0+x2}. A function of that form, extended
from the period-2 lattice to any even cyclic grid, has Fourier support inside
the sign characters. The jet itself uses only the identity and the shear
character (-1,1,-1,1). No root of unity outside that pair is present.
"""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(
        name, HERE / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cubic = load("a4d_joint_response_shear_cubic_check")
order5 = load("a4d_joint_response_shear_order5_check")


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def series_equal(left, right):
    return all(sp.expand(left[k] - right[k]) == sp.zeros(4) for k in range(cubic.N))


def depends_only_on_sigma(link_fn, label):
    classes = {}
    for site in cubic.SITES:
        sign = cubic.sigma(site)
        for role in range(4):
            value = link_fn(site, role)
            key = (sign, role)
            if key not in classes:
                classes[key] = value
            else:
                check(
                    f"{label}_SIGMA_CLASS_{sign}_{role}",
                    series_equal(value, classes[key]),
                )
    differs = [
        role for role in range(4)
        if not series_equal(classes[(1, role)], classes[(-1, role)])
    ]
    check(f"{label}_SOME_ROLE_CARRIES_SIGMA", differs != [])
    print(label, "SIGMA_ROLES", differs, flush=True)


def fourier(link_fn, phase):
    acc = [sp.zeros(4) for _ in range(cubic.N)]
    for site in cubic.SITES:
        weight = 1
        for axis, coord in enumerate(site):
            weight *= phase[axis] ** coord
        for role in range(4):
            series = link_fn(site, role)
            for k in range(cubic.N):
                acc[k] += weight * series[k]
    return acc


def support_characters(link_fn):
    alive = []
    signs = (sp.Integer(1), sp.Integer(-1))
    for phase in product(signs, repeat=4):
        acc = fourier(link_fn, phase)
        if any(sp.expand(term) != sp.zeros(4) for term in acc):
            alive.append(phase)
    return alive


def geometric_factor(length, exponent):
    """Sum over one even-grid fiber. Zero unless the exponent is a sign."""
    half = length // 2
    if exponent % half == 0:
        return sp.Integer(half)
    root = sp.exp(2 * sp.pi * sp.I * sp.Rational(exponent, half))
    return sp.simplify((root**half - 1) / (root - 1))


def main():
    order5.ACTIVE_ETA = list(order5.ETA_CLEAN)
    order5.ACTIVE_XI = list(order5.XI_CLEAN)
    jets = {
        "BARE": cubic.link,
        "CORRECTED": order5.full_link,
    }
    identity = tuple(sp.Integer(1) for _ in range(4))
    shear = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))
    for label, link_fn in jets.items():
        depends_only_on_sigma(link_fn, label)
        alive = support_characters(link_fn)
        check(f"{label}_FOURIER_SUPPORT", set(alive) == {identity, shear})
        print(label, "SUPPORT", alive, flush=True)

    for length in (6, 8, 10, 12, 16):
        half = length // 2
        check(
            f"L{length}_SIGN_EXPONENT_SURVIVES",
            geometric_factor(length, 0) == half
            and geometric_factor(length, half) == half,
        )
        check(
            f"L{length}_PRIMITIVE_EXPONENT_VANISHES",
            geometric_factor(length, 1) == 0,
        )
        check(
            f"L{length}_OFFSET_EXPONENT_VANISHES",
            geometric_factor(length, half + 1) == 0,
        )
    print()
    print("RESULT: the period-2 shear jet is a function of (-1)^{x0+x2} only.")
    print("  On every even cyclic grid its Fourier support is the identity")
    print("  and (-1,1,-1,1). No root of unity outside that pair is present.")
    print("BOUNDARY: the pure period-2 ansatz, bare and corrected through")
    print("  order u^5. A slow amplitude u(hx) is not this ansatz and stays")
    print("  open. This is not a smooth-background NOGO.")


if __name__ == "__main__":
    main()
