"""Replay the pinned two-birth AF clock; check its feedback terminal and every Doob stage.
Python 3, NumPy, SymPy. Run in the source checkout or supply --repo PATH.
"""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy

import numpy as np
import sympy as sp


CLOCK = "02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/check_growing_clock.py"
LEAN = "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean"
HASHES = {CLOCK: "30d41b1d024d6a6c6cbfa387fd6f376d2176cfc91757043ee093a72d1ff9d2d8",
          LEAN: "6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7"}


def need(condition, title):
    if not condition:
        raise ValueError(title)


def repository(path):
    if path is not None:
        return path.resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / CLOCK).is_file() and (parent / LEAN).is_file():
            return parent
    raise ValueError("pass --repo pointing to the checkout with the pinned sources")


def nmul(x, y):
    return np.einsum("ij,jk->ik", x, y, optimize=False)


def spd_power(value, exponent):
    vals, vecs = np.linalg.eigh((value + value.T) / 2)
    need(vals.min() > 0, "positive definite terminal")
    return nmul(vecs * vals**exponent, vecs.T)


def check_word(data, suffix, middle, feedback):
    # These exact stages and feedback matrices come from the verified original replay.
    forward = [data[n] for n in ("G", "J0")] + [middle, data["J1"], data["G13"]]
    gates = forward + [data["last"]]
    reduce = data["mat"]
    I = sp.eye

    def product(*matrices):
        out = matrices[0]
        for x in matrices[1:]:
            out = reduce(out*x)
        return out

    def equal(x, y, title):
        need(not reduce(x-y).todok(), title)

    a = data["a"]
    a_real = data["actual_a"]
    def numeric(x):
        return np.asarray(x.subs(a, a_real).evalf(18), dtype=float)

    embedded = [I(2)]
    for g in gates:
        embedded.append(product(g, embedded[-1]))
    V = embedded[-1]
    born = data["B"][0]
    Pborn = product(born, born.T)
    C = product(born.T, V)
    M = product(C.T, C)
    z = sp.Rational(3, 5)  # The exact primary fixture checks det(I-zF) for every z.
    H = (1-z)*I(2)+z*M
    R = product(V, V.T)
    raw = (1-z)*I(13)+z*Pborn
    block_from_clock = product(data["last"], I(13)-z*feedback[-13:, -13:], data["last"].T)
    E = I(13)-z*product(R, I(13)-Pborn, R)
    equal(E, block_from_clock, "actual final block after final CX")
    equal(E, I(13)+product(V, H-I(2), V.T), "transported range formula")
    equal(product(V.T,E,V), product(V.T,raw,V), "supplied terminal compression")
    equal(product(E,V), product(V,H), "reducing range")
    need(bool(reduce(product(raw,V)-product(V,H)).todok()), "raw terminal has cross-range coupling")
    equal(feedback[:-13,:], sp.zeros(data["D"]-13,data["D"]), "all other clock rows")
    equal(feedback[:,:-13], sp.zeros(data["D"],data["D"]-13), "all other clock columns")
    nonscalar = bool(reduce(H-sp.trace(H)*I(2)/2).todok())
    need(nonscalar, "nonscalar true input corner")

    hs = [I(v.rows)+product(v,H-I(2),v.T) for v in embedded]
    equal(hs[-1], E, "terminal backward weight")
    max_error = 0.
    for k, g in enumerate(gates):
        equal(product(g.T,hs[k+1],g), hs[k], "exact backward recursion")
        equal(product(hs[k+1],g), product(g,hs[k]), "exact all-column intertwining")
        x = numeric(g)
        normalized = nmul(nmul(spd_power(numeric(hs[k+1]), .5), x), spd_power(numeric(hs[k]), -.5))
        need(np.isfinite(normalized).all(), "finite principal roots")
        max_error = max(max_error, float(np.max(np.abs(normalized-x))))
    need(max_error < 2e-12, "all principal-root stages equal native maps")
    y = numeric(V)
    B = nmul(nmul(spd_power(numeric(E), .5), y), spd_power(numeric(H), -.5))
    bell = np.eye(2).reshape(-1)/np.sqrt(2)
    need(np.max(np.abs(nmul(np.kron(B-y,np.eye(2)),bell[:,None]))) < 2e-12, "protected entangled input")
    # Scalar normalization of the sandwich with input I/2 instead prepares H/Tr(H).
    equal(product(E,V), product(V,H), "operator-normalized versus scalar sandwich")
    return {"native_variant": suffix, "exact_nontrivial_corner_is_nonscalar": nonscalar,
            "all_stage_intertwinings_exact": len(gates),
            "sampled_square_root_max_error_below": "2e-12",
            "entangled_reference_dimension": 2, "raw_terminal_has_off_range_component": True,
            "scalar_filter_changes_maximally_mixed_protected_input": nonscalar}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path)
    repo = repository(parser.parse_args().repo)
    for name, digest in HASHES.items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest() == digest, "source byte pin: "+name)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        data = runpy.run_path(str(repo / CLOCK))
    receipt = json.loads(capture.getvalue())
    need(receipt["status"] == "PASS" and receipt["full_determinant_verified"], "original replay")
    variants = [check_word(data, name, data[mid], data[fb])
                for name,mid,fb in (("first native prefix","G5a","Fplus"),("second native prefix","G5b","Fminus"))]
    print(json.dumps({"status":"PASS","input_sha256":HASHES,"primary_status":receipt["status"],
                      "stage_dimensions":receipt["stage_fibre_dimensions"],"clock_dimension":data["D"],
                      "born_cut_rank":2, "native_final_gate":receipt["terminal_native_gate"],
                      "primary_full_hodge_dimension":receipt["full_hodge_dimension"],
                      "exact_ring":"Q[a]/(a^4+a^2-1), positive physical root",
                      "stage_examples":variants, "entire_physical_Cost_Info_identified":False}, indent=2))


if __name__ == "__main__":
    main()
