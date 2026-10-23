"""Choose fixed decimal congruences for the remaining native field inverse.

This is numerical choice data for a separate outward-error validator, not
an inertia theorem or a rank catalogue. It covers exactly the nonzero
frequencies outside Omega-Omega, modulo spatial S3 and global negation.
All momenta/Fock components and signed matter weights are retained by the
pinned new symbol algebra. No historical run() or root solve is called.

The normal Hessian inverse is consumed by the full local critical-locus
argument; finding an additional singular mode must change that argument.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import time

for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ALGEBRA_SHA = "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1"


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("field_inverse_choice:"+label)


def algebra():
    path = HERE/"nonzero_symbol_algebra.py"
    require(hashlib.sha256(path.read_bytes()).hexdigest() == ALGEBRA_SHA,
            "complete_symbol_algebra_pin")
    spec = importlib.util.spec_from_file_location("field_inverse_choice_algebra", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def orbit(q):
    q = tuple(q)
    return sorted({tuple((sign*q[i]) % 8 for i in (0,)+perm)
                   for perm in itertools.permutations((1, 2, 3))
                   for sign in (1, -1)})


def domain():
    shell = [tuple(sign*int(r == i) % 8 for r in range(4))
             for i in range(4) for sign in (1, -1)]
    differences = {tuple((l[r]-k[r]) % 8 for r in range(4))
                   for k in shell for l in shell}
    require(len(differences) == 33 and (0, 0, 0, 0) in differences,
            "complete_occupied_shell_difference_set")
    remaining = set(itertools.product(range(8), repeat=4))-differences
    representatives = sorted({tuple(orbit(q)[0]) for q in remaining})
    covered = set()
    for q in representatives:
        members = set(orbit(q))
        require(members <= remaining and not (members & covered),
                "disjoint_complete_spatial_orbits_outside_shell")
        covered |= members
    require(covered == remaining and len(covered) == 4063,
            "every_unsolved_field_frequency_covered")
    require(len(representatives) == 483, "all483_field_only_orbits")
    return representatives, differences


def choose(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    start = time.perf_counter()
    module = algebra()
    shared = module.shared_spectral_data(repo)
    representatives, differences = domain()
    choices = []
    smallest = (float("inf"), None)
    worst_congruence = 0.0
    for q in representatives:
        assembled = module.assemble_symbol(q, shared,
                                           use_stationary_root_identity=False,
                                           unit_inactive_axes=False)
        H = assembled["H"]
        values, vectors = np.linalg.eigh(H)
        gap = float(np.min(np.abs(values)))
        # Failure is a new mathematical question, not a tolerated nullspace
        # or an invitation to delete a field coordinate.
        require(gap > 1e-8, "investigate_additional_field_kernel_at_"+str(q))
        require(assembled["Hermitian_relative_error"] < 1e-10,
                "finite_Hermitian_choice_at_"+str(q))
        B = vectors/np.sqrt(np.abs(values))[None, :]
        signs = np.sign(values).astype(int)
        HB = np.einsum("ij,jk->ik", H, B, optimize=False)
        congruence = np.einsum("ia,ib->ab", B.conj(), HB, optimize=False)
        residual = float(np.max(np.sum(np.abs(congruence-np.diag(signs)), axis=1)))
        require(np.isfinite(B).all() and residual < 1e-6,
                "resolved_numerical_congruence_choice_at_"+str(q))
        exact = [[(format(z.real, ".17g"), format(z.imag, ".17g"))
                  for z in row] for row in B]
        if gap < smallest[0]:
            smallest = gap, q
        worst_congruence = max(worst_congruence, residual)
        choices.append({"q": list(q), "B": exact, "signs": signs.tolist(),
                        "orbit_size": len(orbit(q)),
                        "real_amplitudes_only": assembled["basis"]["self_conjugate_frequency"],
                        "point_choice_minimum_absolute_eigenvalue": gap,
                        "point_choice_congruence_residual": residual})
    return {"schema": "d0-native-field-inverse-decimal-choices/1",
            "status": "NUMERICAL_CHOICES_REQUIRE_SEPARATE_OUTWARD_VALIDATION",
            "consumer": "normal Hessian inverse for full local critical-locus theorem",
            "source_pins": {"nonzero_symbol_algebra.py": ALGEBRA_SHA},
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "shared_owned_input_pins": shared["source_pins"],
            "carrier": {"L": 8, "momenta": 4096, "Fock": 16, "reference": 128},
            "shell_difference_frequencies": len(differences),
            "field_only_frequencies": 4063, "field_only_representatives": 483,
            "smallest_point_choice_eigenvalue_absolute": smallest[0],
            "smallest_point_choice_q": list(smallest[1]),
            "worst_point_choice_congruence_residual": worst_congruence,
            "stationary_shortcut_used": False, "unit_inactive_axis_rescaling": False,
            "root_box_or_inertia_or_inverse_certified": False,
            "old_symbol_runs_or_root_search_called": False,
            "choices": choices, "choice_seconds": round(time.perf_counter()-start, 4)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = choose()
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":"))+"\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("choices", "shared_owned_input_pins")}, indent=2))
