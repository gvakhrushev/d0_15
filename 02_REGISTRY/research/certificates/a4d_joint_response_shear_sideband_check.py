#!/usr/bin/env python3
"""Sideband content of the period-2 shear Euler.

The frozen resonant projection at order u^5 is -432. A neighboring L=2
character can change that projection only if the pure shear mode sources it
early enough for its linear image to re-enter the resonant equation. This
certificate records the four neighbor projections of the owned jet.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


def load_cubic():
    path = Path(__file__).resolve().parent / "a4d_joint_response_shear_cubic_check.py"
    spec = importlib.util.spec_from_file_location("shear_cubic", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cubic = load_cubic()


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def side_weights(site):
    x0, x1, x2, x3 = site
    sigma = cubic.sigma(site)
    return {
        "identity": 1,
        "resonant": sigma,
        "flip1": sigma * (1 if x1 == 0 else -1),
        "flip3": sigma * (1 if x3 == 0 else -1),
        "flip0": 1 if x2 == 0 else -1,
        "flip2": 1 if x0 == 0 else -1,
    }


def projections():
    links = {(site, role): cubic.link(site, role) for site in cubic.SITES for role in range(4)}
    names = ("identity", "resonant", "flip1", "flip3", "flip0", "flip2")
    out = {name: [[0] * cubic.N for _ in range(24)] for name in names}
    for site in cubic.SITES:
        weights = side_weights(site)
        for role in range(4):
            for j, generator in enumerate(cubic.GENERATORS):
                acc = [0] * cubic.N
                for a, b in cubic.PAIRS:
                    if role == a:
                        corners = [(site, 0), (cubic.shift(site, b), 2)]
                    elif role == b:
                        corners = [(cubic.shift(site, a), 1), (site, 3)]
                    else:
                        continue
                    row = cubic.plain_row(a, b)
                    for base, corner in corners:
                        facts = [
                            links[(base, a)],
                            links[(cubic.shift(base, a), b)],
                            cubic.inv(links[(cubic.shift(base, b), a)]),
                            cubic.inv(links[(base, b)]),
                        ]
                        varied = list(facts)
                        gen = (generator,) + tuple(cubic.Z4 for _ in range(cubic.N - 1))
                        if corner < 2:
                            varied[corner] = cubic.mul(facts[corner], gen)
                        else:
                            varied[corner] = cubic.mul(cubic.smul(-1, gen), facts[corner])
                        hol = cubic.product(facts)
                        dp = cubic.product(varied)
                        mid = cubic.mul(cubic.mul(cubic.inv(hol), dp), cubic.inv(hol))
                        for k in range(cubic.N):
                            curv = (dp[k] + mid[k]) / 2
                            acc[k] += (row * cubic.bivector(curv))[0]
                slot = 6 * role + j
                for name in names:
                    for k in range(cubic.N):
                        out[name][slot][k] += weights[name] * acc[k]
    return out


def resonant_of(rows):
    values = []
    for k in range(cubic.N):
        value = 0
        for role in range(4):
            for j in range(6):
                value += cubic.WITNESS[role][j] * rows[6 * role + j][k]
        values.append(sp.expand(value))
    return values


def support(rows):
    orders = []
    for k in range(cubic.N):
        column = [sp.expand(rows[slot][k]) for slot in range(24)]
        orders.append(0 if all(entry == 0 for entry in column) else 1)
    return orders


def main():
    data = projections()
    check(
        "RESONANT_PROJECTION_VANISHES_THROUGH_U5",
        resonant_of(data["resonant"]) == [0] * cubic.N,
    )
    for name in ("flip1", "flip3", "flip0", "flip2"):
        orders = support(data[name])
        check(name + "_SILENT_THROUGH_U5", orders == [0] * cubic.N)
        print("ZETA", name, "SUPPORT", orders, flush=True)

    order_path = Path(__file__).resolve().parent / "a4d_joint_response_shear_order5_check.py"
    order_spec = importlib.util.spec_from_file_location("shear_order5", order_path)
    order5 = importlib.util.module_from_spec(order_spec)
    order_spec.loader.exec_module(order5)

    order5.ACTIVE_ETA = list(order5.ETA_CLEAN)
    order5.ACTIVE_XI = list(order5.XI_CLEAN)
    cubic.link = order5.full_link
    corrected = projections()
    check(
        "CORRECTED_RESONANT_ORDER5_IS_MINUS_432",
        resonant_of(corrected["resonant"])[5] == -432,
    )
    for name in ("flip1", "flip3", "flip0", "flip2"):
        orders = support(corrected[name])
        check(name + "_CORRECTED_SILENT_THROUGH_U5", orders == [0] * cubic.N)
        print("CORRECTED", name, "SUPPORT", orders, flush=True)
    print("RESULT_SIDEBANDS: neighbors are silent through order u^5 on the jet whose resonant value is -432")
    print("BOUNDARY: L=2 characters only; a longer envelope is still open, and this is not a smooth-background NOGO")


if __name__ == "__main__":
    main()
