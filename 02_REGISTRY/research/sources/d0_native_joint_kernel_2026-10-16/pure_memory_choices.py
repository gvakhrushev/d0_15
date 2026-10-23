"""Choose arbitrary decimal preconditioners for the new pure-memory operator.

These choices are not a proof of inertia. A separate outward interval
consumer must validate them on the entire root rectangle. All field-only
classes and the five changed shell restrictions have a named consumer:
the remaining40806-dimensional normal operator of the rank8 critical family.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    "pure_memory_symbol.py": "1ef97d8f72d5133c75c2c071ed75b8b9ce295322c407c49e91bf589afd2af9fd",
    "field_inverse_choice.py": "1fa0f1022301d3eb529d1394a99c41849f193ea0e4980f94936674d29e7d5c8a",
}
CHANGED_SHELL = ((2, 0, 0, 0), (0, 2, 0, 0), (1, 1, 0, 0),
                 (1, 7, 0, 0), (0, 1, 1, 0))


def require(value, label):
    if not bool(value):
        raise ArithmeticError("pure_memory_choices:" + label)


def load(name):
    p = HERE / (name + ".py")
    require(hashlib.sha256(p.read_bytes()).hexdigest() == PINS[p.name], "frozen_" + name)
    spec = importlib.util.spec_from_file_location("pure_choice_" + name, p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def choose(repo=None):
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    symbol, domain = load("pure_memory_symbol"), load("field_inverse_choice")
    shared = symbol.prepare_shared(repo)
    representatives, differences = domain.domain()
    tasks = [(q, False) for q in representatives] + [(q, True) for q in CHANGED_SHELL]
    result, smallest = [], (float("inf"), None)
    for i, (q, restricted) in enumerate(tasks):
        data = symbol.pure_field_symbol(q, shared)
        indices = ([j for j, label in enumerate(data["basis"]["labels"])
                    if label[0] == "inactive_full_leg"] if restricted
                   else list(range(data["basis"]["dimension"])))
        H = data["H_pure"][np.ix_(indices, indices)]
        is_real = data["basis"]["self_conjugate_frequency"]
        if is_real:
            require(float(np.max(np.abs(H.imag))) < 1e-9, "real_self_conjugate_block")
            H = H.real
        values, vectors = np.linalg.eigh(H)
        gap = float(min(abs(values)))
        require(gap > 1e-10, "investigate_possible_extra_kernel_at_" + str(q))
        B = vectors / np.sqrt(np.abs(values))[None, :]
        signs = np.sign(values).astype(int)
        HB = np.einsum("ij,jk->ik", H, B, optimize=False)
        residual = float(np.max(np.sum(abs(np.einsum("ia,ib->ab", B.conj(), HB,
                                                      optimize=False) - np.diag(signs)), axis=1)))
        require(np.isfinite(B).all() and residual < 1e-5, "resolved_arbitrary_decimal_choice")
        decimal = [[[format(complex(z).real, ".17g"), format(complex(z).imag, ".17g")]
                    for z in row] for row in B]
        result.append({"q": list(q), "B": decimal, "signs": signs.tolist(),
                       "basis_indices": indices, "shell_kerT_restriction": restricted,
                       "orbit_size": len(domain.orbit(q)), "real_amplitudes_only": is_real,
                       "point_choice_minimum_absolute_eigenvalue": gap,
                       "point_choice_congruence_residual": residual})
        if gap < smallest[0]:
            smallest = gap, list(q)
        if (i + 1) % 25 == 0 or i + 1 == len(tasks):
            print("new pure choices %d/%d" % (i + 1, len(tasks)), file=sys.stderr, flush=True)
    for name, h in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == h,
                "no_concurrent_source_mutation")
    return {"schema": "d0-pure-memory-preconditioner-choices/1",
            "status": "ARBITRARY_NUMERICAL_CHOICES_REQUIRE_OUTWARD_VALIDATION",
            "carrier": {"L": 8, "sites": 4096, "Fock": 16, "reference": 128, "prepared_rank": 8},
            "field_only_classes": 483, "new_shell_restriction_classes": 5,
            "unchanged_opposite_spatial_shell_class": [0, 1, 7, 0],
            "root_box_inertia_or_inverse_certified": False,
            "minimum_point_choice_absolute_eigenvalue": smallest[0],
            "minimum_point_choice_q": smallest[1], "source_pins": PINS,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "choices": result, "choice_seconds": round(time.perf_counter() - start, 4)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = choose()
    args.output.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "choices"}, indent=2))
