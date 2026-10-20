#!/usr/bin/env python3
"""One direct original six-face mixed witness; no all40 theorem replay.

Consumes an immutable original checker solely for its original contractions.
No expected-result rewrite, repository mutation, broad replay, or physical
admission claim. Every condition remains active under python -O.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import sympy as sp


SOURCE_PATH = (
    "02_REGISTRY/gr_assembly/sources/d0_brinkmann_j2_2026-10-19/"
    "check_all40_arbitrary_brinkmann.py"
)
SOURCE_SHA256 = "d3d0b1bc92c25a0963a4ba851d9d587d2191f0bbd8cd8cd0ab58b664852b7026"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def same(actual, expected, message):
    remainder = sp.factor(sp.cancel(actual - expected))
    require(remainder == 0, message + ": " + str(remainder))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_file(args):
    if args.source is not None:
        return Path(args.source).resolve()
    if args.root is not None:
        return (Path(args.root).resolve() / SOURCE_PATH).resolve()
    return Path(__file__).resolve().parent / "inputs/original_all40_checker.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--root", help="Original repository or preserved path snapshot root")
    group.add_argument("--source", help="Exact byte-identical original checker snapshot")
    args = parser.parse_args()
    path = source_file(args)
    require(path.is_file(), "Missing immutable original six-face source")
    require(sha256(path) == SOURCE_SHA256, "Original source pin mismatch before execution")
    spec = importlib.util.spec_from_file_location("immutable_original_all40", path)
    require(spec is not None and spec.loader is not None, "Cannot load original source")
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)

    # Never call owner.theorem(), owner.links(), or its whole-carrier replay.
    h = owner.h
    s, r, lam, eps, wave = sp.symbols("s r lambda epsilon wave", real=True)
    z0 = (2, 0, 3, 3)
    center = (3, 3, 3)

    def chi(z):
        return int((z[0], z[2], z[3]) == center)

    def profile(z):
        x, y = h * (z[2] - 3), h * (z[3] - 3)
        return -lam * eps**2 * (x*x + y*y) + wave * (x*x - y*y) + s * chi(z)

    def link_component(z, axis):
        future = owner.sh(z, 0)
        return (profile(future) - profile(owner.sh(future, axis, -1))) / 2

    owner.H = profile
    owner.A = lambda z: link_component(z, 2)
    owner.B = lambda z: link_component(z, 3)

    def coframe(z):
        result = h * sp.eye(4)
        result[1, 0] = h * profile(z) / 2
        if z == z0:
            result[0, 1] += r
        return result

    owner.e = coframe

    # Differentiate the actual original based density, not its owned Euler row.
    terms = []
    for axis, other in owner.pairs:
        u, v = (i for i in range(4) if i not in (axis, other))
        holonomy = owner.plaque(z0, axis, other)
        curvature = (holonomy - owner.inv(holonomy)) / 2
        terms.append(
            sp.LeviCivita(axis, other, u, v)
            * owner.pair(coframe(z0), u, v, curvature)
        )
    require(len(terms) == 6, "The original six faces must all be retained")
    density = sp.factor(sum(terms))
    fhat = sp.factor(density / h**4)
    expected_fhat = r * (2 * lam * eps**2 / h + 2 * s / h**3)
    same(fhat, expected_fhat, "Direct original six-face density")
    same(sp.diff(fhat, s, r), 2 / h**3, "Original mixed gravity row")

    # Full inverse coframe metric; not a prescribed source/coupling substitute.
    E = coframe(z0) / h
    metric = E.T * owner.eta * E
    inverse_metric = metric.inv()
    covector = sp.Matrix([eps, 0, 0, 0])
    q = sp.factor((covector.T * inverse_metric * covector)[0])
    same(q, -2 * eps**2 * r / h, "Actual scalar/top CAR metric square")
    same(sp.diff(q, s, r), 0, "Matter has zero profile-normal cross term")
    same(fhat + lam*q, 2 * s * r / h**3, "Exact original source combination")
    same(sp.diff(fhat + lam*q, r).subs(s, 0), 0, "Stationary base normal row")
    same(metric.det(), -1, "Full coframe remains nondegenerate on the witness")
    same(coframe(z0).det(), h**4, "Original coframe determinant")
    same(metric[1, 1], 2*r/h, "The normal coframe variation changes the metric")

    # Fixed u/transverse collars and the necessary one-u-tick Cartan support.
    nodes = list(itertools.product(range(8), repeat=4))
    free = {2, 3, 4, 5}

    def interior(z):
        return all(z[axis] in free for axis in (0, 2, 3))

    h_support = [z for z in nodes if chi(z)]
    require(len(h_support) == 8, "H perturbation must cover precisely its periodic v orbit")
    require(all(interior(z) for z in h_support), "H perturbation touches fixed collar")
    require(interior(z0), "Normal coframe perturbation touches fixed collar")
    link_support = []
    for z in nodes:
        for axis in (2, 3):
            future = owner.sh(z, 0)
            coefficient = chi(future) - chi(owner.sh(future, axis, -1))
            if coefficient:
                link_support.append((z, axis))
                require(interior(z), "Cartan lift touches fixed collar")
                require(z[0] == 2, "Cartan lift has wrong original one-u-tick staggering")
    require(len(link_support) == 32, "Wrong exact compact Cartan link support")
    require({z[0] for z in h_support} == {3}, "Initial/final u-collar must stay fixed")
    require(all(z[0] not in {0, 1, 6, 7} for z, _ in link_support), "Initial links changed")

    # The actual shifted five-point stencil, including all four neighbors.
    future = owner.sh(z0, 0)
    stencil = (
        chi(owner.sh(future, 2)) + chi(owner.sh(future, 2, -1))
        + chi(owner.sh(future, 3)) + chi(owner.sh(future, 3, -1))
        - 4 * chi(future)
    )
    require(stencil == -4, "Original transverse spike stencil")
    mixed_at_mesh = sp.factor(sp.diff(fhat, s, r).subs(h, sp.Rational(1, 8)))
    same(mixed_at_mesh, 1024, "Explicit h=1/8 mixed coefficient")

    # Omission control: an ansatz-only variation sees no field equation.
    restricted_source = sp.factor((fhat + lam*q).subs(r, 0))
    same(restricted_source, 0, "Restricted family must have the exact flat value")
    restricted_mixed = sp.diff(restricted_source, s, r)
    require(sp.factor(restricted_mixed - 2/h**3) != 0,
            "Omitting the independent normal direction must fail the full mixed target")

    # Finite Dirichlet witness for the all-mesh energy argument, not a rank census.
    D = list(itertools.product((2, 3, 4), repeat=2))
    index = {node: i for i, node in enumerate(D)}
    lap = sp.zeros(len(D))
    x = sp.Matrix(sp.symbols("x0:9", real=True))
    energy = sp.Integer(0)
    for node, i in index.items():
        lap[i, i] = -4
        for axis in (0, 1):
            for sign in (-1, 1):
                neighbor = list(node)
                neighbor[axis] += sign
                neighbor = tuple(neighbor)
                if neighbor in index:
                    j = index[neighbor]
                    lap[i, j] += 1
                    if i < j:
                        energy += (x[i] - x[j])**2
                else:
                    energy += x[i]**2
    same(-(x.T * lap * x)[0], energy, "Exact Dirichlet edge-energy identity")
    require(lap.det() != 0, "Finite buffered Dirichlet mixed block is not injective")

    mu, b = sp.symbols("mu b", real=True)
    mixed_form = sp.Matrix([[0, mu], [mu, b]])
    same(mixed_form.det(), -mu**2, "Normal curvature cannot remove the mixed saddle")

    # The quantified remainder estimate in the proof uses these exact factors:
    # Ms <= d/4 gives |t| <= (5/4)d s^3;
    # s^3 <= 8|kappa|/(25 G d) bounds the quadratic error by |kappa|d s^3/4.
    same(sp.Rational(1, 2) * sp.Rational(5, 4)**2 * sp.Rational(8, 25),
         sp.Rational(1, 4), "Quantified scalar-score remainder coefficient")
    same(-1 + sp.Rational(1, 4) + sp.Rational(1, 4),
         -sp.Rational(1, 2), "Strict cubic descent margin")

    require(sha256(path) == SOURCE_SHA256, "Immutable original source changed")
    print(json.dumps({
        "status": "PASS",
        "source_sha256": SOURCE_SHA256,
        "original_source_unchanged": True,
        "original_all40_theorem_replayed": False,
        "original_based_faces": len(terms),
        "direct_fhat": str(fhat),
        "direct_q": str(q),
        "source_combination": str(sp.factor(fhat + lam*q)),
        "mixed_gravity": str(sp.factor(sp.diff(fhat, s, r))),
        "mixed_matter": str(sp.factor(sp.diff(q, s, r))),
        "mesh_h": "1/8",
        "mixed_gravity_at_mesh": str(mixed_at_mesh),
        "fixed_collar": [0, 1, 6, 7],
        "profile_support_sites": len(h_support),
        "normal_support_sites": 1,
        "cartan_changed_components": len(link_support),
        "dirichlet_dimension": len(D),
        "dirichlet_integer_determinant": str(lap.det()),
        "omitted_normal_control": "detected: restricted source has zero mixed row",
        "scope": "Exact finite original mixed-source witness and algebraic controls; C1 plateau proof is analytical; physical admission remains unproved."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
