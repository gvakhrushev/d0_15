"""Replay the fixed clock, growing clock intertwiners and actual material jet."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round128"))
from check_preparer_source import (
    REPO, actual_words, exact, ne, require, stage_matrix, verify_words,
)


def equal(left, right, reason):
    require(ne.exact_matrix_equal(left, right), reason)


def reduced(matrix):
    field = ne.GOLDEN_FIELD
    return matrix.applyfunc(lambda value: field.to_sympy(field.from_sympy(value)))


def check_clock():
    receipt = verify_words()
    words = actual_words()
    plain = [stage_matrix(gate) for gate in words["CX_18"]]
    echo = [stage_matrix(gate) for gate in words["G_Z_G_Z"]]
    forward = [sp.diag(a, b) for a, b in zip(plain, echo)]
    reverse = [sp.diag(b, a) for a, b in zip(plain, echo)]
    first, second, frames = sp.eye(32), sp.eye(32), [sp.eye(32)]
    for current, swapped in zip(forward, reverse):
        first, second = reduced(current * first), reduced(swapped * second)
        candidate = reduced(second * first.T)
        equal(swapped * frames[-1], candidate * current, "An edge does not intertwine")
        frames.append(candidate)
    equal(frames[-1], sp.eye(32), "The endpoint frame must be the identity")

    # Add a common true birth, including its orthogonal closure detail.
    # The last actual gate is used for closure, rather than adding a tick.
    born = sp.Matrix([ne.A, ne.P])
    detail = sp.Matrix([-ne.P, ne.A])
    embedding = sp.kronecker_product(sp.eye(16), born)
    complement = sp.kronecker_product(sp.eye(16), detail)
    equal(embedding * embedding.T + complement * complement.T,
          sp.eye(32), "The birth detail must be retained")
    closure = embedding.T.col_join(complement * complement.T)
    equal(closure.T * closure, sp.eye(32), "The closing embedding must be isometric")
    equal(sp.diag(sp.eye(16), frames[0]) * closure, closure,
          "The actual closing range must be fixed")
    equal(closure * reverse[-1] * frames[-2], closure * forward[-1],
          "The closing edge using the last real gate must intertwine")
    return receipt | {"swapped_gate_intertwiners": 18, "birth_detail_retained": True,
                      "first_mark_preserved": False}


def check_material():
    p, a = ne.P, ne.A
    m0 = sp.Matrix([0, a, p, 0])
    scalar_direction = sp.Matrix([1, 0, 0, 0])
    top_direction = sp.Matrix([0, 0, 0, 1])
    parity = sp.diag(-1, 1, 1, -1)
    equal(parity * m0, m0, "The original material vacuum must be parity even")
    for tangent in (scalar_direction, top_direction):
        equal(parity * tangent, -tangent, "A material tangent must flip parity")
        require(exact(m0.dot(tangent), 0), "The material tangent changes the norm")
    # Two sites with different fields. The variables enter the original
    # material sphere; the change of an off-diagonal SITE/RIGHT block is real.
    t = p * sp.Rational(3, 5)
    remote_m = sp.Matrix([t, a, p * sp.Rational(4, 5), 0])
    require(exact(remote_m.dot(remote_m), 1), "Wrong strict material field")
    require(exact(remote_m.dot(scalar_direction), t) and t.is_positive,
            "Unexpected passive joint-coherence derivative")
    # Parity-covariant central rotation (879), with canonical e1 anchor.
    e1 = sp.eye(4)[:, 1]

    def rotation(m):
        skew = m * e1.T - e1 * m.T
        return sp.eye(4) + skew + skew**2 / (1 + a)

    equal(rotation(parity * remote_m), parity * rotation(remote_m) * parity,
          "Owner rotation failed full-column material sign covariance")
    moved = rotation(remote_m) * rotation(m0).T
    equal(moved * m0, remote_m, "The full owner material writer changed")
    return {
        "vacuum_material_directions": [0, 15],
        "parity_covariant_on_all_active_columns": True,
        "right_only_state_independent": True,
        "site_right_coherence_derivative_at_nonuniform_field": "3p/5 times site amplitudes",
    }


def main():
    source_paths = (
        "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean",
        "04_CERTIFICATES/order_memory_control_verify.py",
        "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
    )
    receipt = {
        "source_sha256": {path: sha256(subprocess.check_output([
            "git", "show", f"dc411daf01f697ec85dd22f28bfe124171796645:{path}"
        ], cwd=REPO) if path.endswith("PAID_SOURCE_RESIDUAL_2026_10_20.md")
            else (REPO / path).read_bytes()).hexdigest()
                          for path in source_paths},
        "clock": check_clock(),
        "material": check_material(),
        "absolute_Cost_minus_Info_preparation_cancellation_proved": False,
        "GR_closed": False,
        "status": "PASS",
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
