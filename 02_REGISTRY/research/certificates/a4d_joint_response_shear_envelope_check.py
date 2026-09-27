#!/usr/bin/env python3
"""Period-4 sidebands of the upper-shear character.

The shear character z=(-1,1,-1,1) generates only the sign group {±1}^4.
A one-step longer envelope replaces one sign by ±i. Those eight characters
lie outside the algebra of pure shear powers, and this certificate records
whether any of them is a joint kernel at the upper shear.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


def load_nf():
    path = Path(__file__).resolve().parent / "a4d_joint_response_nf_l4_check.py"
    spec = importlib.util.spec_from_file_location("nf_l4_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nf = load_nf()


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


SHEAR = sp.Matrix([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
BASE = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))


def generated_by_shear():
    group = {BASE}
    frontier = [BASE]
    while frontier:
        current = frontier.pop()
        nxt = tuple(current[i] * BASE[i] for i in range(4))
        if nxt not in group:
            group.add(nxt)
            frontier.append(nxt)
    return group


def neighbors():
    out = []
    for axis in range(4):
        for root in (sp.I, -sp.I):
            phase = list(BASE)
            phase[axis] = root
            out.append(tuple(phase))
    return out


def main():
    group = generated_by_shear()
    check("SHEAR_ALGEBRA_SIZE", len(group) == 2)
    check(
        "SHEAR_ALGEBRA_IS_IDENTITY_AND_ITSELF",
        group == {BASE, tuple(sp.Integer(1) for _ in range(4))},
    )
    phases = neighbors()
    check("EIGHT_PERIOD4_NEIGHBORS", len(phases) == 8)
    for phase in phases:
        check("NEIGHBOR_OUTSIDE_SHEAR_ALGEBRA", phase not in group)
        h, c = nf.joint_symbols(SHEAR, phase)
        joint = h.col_join(c)
        rank = nf.exact_rank(joint)
        print("RANK", tuple(phase), rank, flush=True)
        check("PERIOD4_NEIGHBOR_JOINT_RANK_24_" + "_".join(str(entry) for entry in phase), rank == 24)
    print("RESULT_ENVELOPE: one-step period-4 sidebands are not shear-sourced and are jointly full rank")
    print("BOUNDARY: not an arbitrary slow wavelength, and not a smooth-background NOGO")


if __name__ == "__main__":
    main()
