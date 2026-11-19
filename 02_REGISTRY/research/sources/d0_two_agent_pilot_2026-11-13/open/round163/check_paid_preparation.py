"""Check literal clock collisions and the saturated-preparation price defect."""

from fractions import Fraction
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import subprocess
import sys

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round128"))
from check_preparer_source import REPO, actual_words, exact, ne, require, verify_words

REVISION = "216c1e7d0f9bf309b3a07415436e56893126a17c"
SOURCE = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
RECEIPT_HASH = "2e0c9e190ed587e66c6e562e6cc23a0696191a0de04b723b64ce3d57d94b265a"


def pinned_receipt():
    source = subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=REPO)
    tag = b"7dx GUARD COTANGENT RETRACTION RECEIPT"
    start = b"<!-- BEGIN " + tag + b" -->\n```json\n"
    stop = b"```\n<!-- END " + tag + b" -->"
    require(source.count(start) == source.count(stop) == 1, "Wrong receipt delimiters")
    raw = source.split(start, 1)[1].split(stop, 1)[0]
    require(sha256(raw).hexdigest() == RECEIPT_HASH, "The primary receipt changed")
    return json.loads(raw)


def word_matrix(word):
    execution = ne.Execution(4, (), (), word, ne.G_CX_SOURCE_I, 0, (2, 3))
    return ne.word_matrix(execution, max_qubits=4, max_expanded_stages=18)


def least_period(word):
    return next(
        span for span in range(1, len(word) + 1)
        if word[span:] == word[:-span]
    )


def check_clock(receipt):
    prior = verify_words()
    b121 = actual_words()
    require(least_period(b121["G_Z_G_Z"]) == 9, "Unexpected repeated half-word")
    require(ne.exact_matrix_equal(word_matrix(b121["G_Z_G_Z"][:9])**2, sp.eye(16)),
            "The two laps no longer close on every input")
    opposite = sp.kronecker_product(sp.Matrix([1, -1]), sp.Matrix([ne.P, 1 + ne.A]), sp.eye(4))
    echo = b121["G_Z_G_Z"]
    require(ne.exact_matrix_equal((word_matrix(echo[:1]) + word_matrix(echo[16:17])) * opposite,
                                  sp.zeros(16, 4)),
            "The repeated phase must demand opposite outputs on the witness subspace")
    target, port, spin = 16, 0, (13, 14)
    lookup = {wire: slot for slot, wire in enumerate((port, target, *spin))}
    keys = {"identity": "literal_prefix_identity18", "rotation": "literal_prefix_rotation18"}
    words = {}
    for label, key in keys.items():
        raw = receipt[key]
        require(len(raw) == 18, "Each preparation must have 18 physical calls")
        require(set(wire for row in raw for wire in row["wires"]) == set(lookup),
                "Preparation support must exclude bit 6 and the old records")
        words[label] = tuple(ne.Gate(row["op"], tuple(lookup[w] for w in row["wires"]))
                             for row in raw)
        for earlier, later in zip(words[label][:2], words[label][16:18]):
            require(not ne.exact_matrix_equal(word_matrix((earlier,)), word_matrix((later,))),
                    "Primary 16-clock collision must be a matrix conflict")
    p = ne.P
    require(ne.exact_matrix_equal(word_matrix(words["identity"]), sp.eye(16)),
            "Identity preparation does not close on all inputs")
    rotation = words["rotation"]
    require(least_period(rotation) == 18, "The rotation word has a shorter periodic schedule")
    require(ne.exact_matrix_equal(word_matrix(rotation), word_matrix((ne.Gate("G", (1,)),))**2),
            "The primary rotation must equal G16 squared on all inputs")

    fresh = sp.eye(16)[:, :4]
    port1 = sp.diag(*([0] * 8 + [1] * 8))
    wrapped = word_matrix(rotation[:16] + rotation[:2]) * fresh
    literal = word_matrix(rotation) * fresh
    require(ne.exact_matrix_equal(literal.T * port1 * literal, sp.zeros(4)),
            "Literal port should remain blank")
    require(ne.exact_matrix_equal(wrapped.T * port1 * wrapped, 4 * p**3 * sp.eye(4)),
            "Wrapped probability should be exact on every Spin column")
    return {
        "B121": prior | {
            "least_command_period_without_distinct_cuts": 9,
            "orthogonal_gate_error_lower_bound": "sqrt(2)",
            "all_prefix_operator_error_lower_bound": "1",
        },
        "7dx_identity_collision_ticks": [[1, 17], [2, 18]],
        "7dx_rotation_collision_ticks": [[1, 17], [2, 18]],
        "7dx_rotation_least_command_period": 18,
        "7dx_rotation_port_one_on_fresh_port_and_witness_all_Spin": {
            "literal": "0", "wrapped": "4*p^3",
        },
    }


def check_defect(receipt):
    c, z, theta = sp.symbols("c z theta", positive=True)
    a = 1 - z
    k = sp.diag(c, 0)
    initial = sp.eye(3)[:, :2]
    p_cut = initial * initial.T
    z0 = a * sp.eye(2) + z * k * k.T

    for label, row in (("visible", 0), ("kernel", 1)):
        unitary = sp.eye(3)
        unitary[row, row] = unitary[2, 2] = sp.cos(theta)
        unitary[2, row], unitary[row, 2] = sp.sin(theta), -sp.sin(theta)
        compressed = initial.T * unitary * initial
        leak = (sp.eye(3) - p_cut) * unitary.T * initial * k.T
        defect = (leak.T * leak).applyfunc(sp.trigsimp)
        lhs = a * sp.eye(2) + z * k * compressed * compressed.T * k.T
        require((lhs - z0 + z * defect).applyfunc(sp.trigsimp) == sp.zeros(2),
                "Wrong finite positive defect")
        determinant = sp.det(a * sp.eye(2) + z * compressed.T * k.T * k * compressed)
        require(sp.trigsimp(determinant - sp.det(lhs)) == 0, "Sylvester determinant mismatch")
        second = sp.diff(-sp.log(determinant), theta, 2).subs(theta, 0)
        leak_slope = leak.diff(theta).subs(theta, 0)
        expected = 2 * z * sp.trace(z0.inv() * leak_slope.T * leak_slope)
        require(sp.cancel(second - expected) == 0, "Incorrect Hessian coefficient")
        require((defect == sp.zeros(2)) == (label == "kernel"),
                "Equality must test only the observed input support")

    rank = receipt["preparation"]["rank_Q_full"]
    require(rank == 8 and receipt["boundary"]["input_rank"] == 16, "Incorrect multiplicity")
    require(exact((2 * ne.P - 1), ne.P**3), "Golden rotation cosine has changed")
    q79 = Fraction(2, 55)**79 / factorial(79)
    heat_bound = Fraction(176, 359) * q79 / ((1 - Fraction(2, 55)**2) * (1 - q79)**2)
    require(heat_bound == Fraction(receipt["complete_price"]["A1_79_rational"]),
            "Wrong heat bound for the actual clock")

    mp.iv.dps = 100
    p = (mp.iv.sqrt(5) - 1) / 2
    c_val = p**3
    z_val = mp.iv.mpf(1) / 2**20
    error = 2 * mp.iv.mpf(heat_bound.numerator) / heat_bound.denominator
    cold_gap = rank * mp.iv.ln((1 - z_val + z_val * c_val**2) /
                              (1 - z_val + z_val * c_val**4))
    price_gap = cold_gap + mp.iv.mpf([-1, 1]) * error
    lo, hi = receipt["complete_price"]["rotation_minus_good"]
    require(mp.iv.mpf(lo).b < price_gap.a and price_gap.b < mp.iv.mpf(hi).a,
            "Calculated H+J interval misses the primary bounds")
    require(price_gap.a > 0, "Need a strict gap on the actual alternatives")
    return {
        "visible_and_kernel_rotation_exact_tests": True,
        "leakage_squared_for_literal_rotation": "8*c^2*(1-c^2), c=p^3",
        "gram_first_jet": "zero for the literal 18 supports; commutator for general R-preserving prep",
        "strict_actual_H_plus_J_gap_primary_enclosure": [lo, hi],
    }


def main():
    receipt = pinned_receipt()
    print(json.dumps({
        "primary_revision": REVISION,
        "primary_receipt_sha256": RECEIPT_HASH,
        "clock": check_clock(receipt),
        "return_defect": check_defect(receipt),
        "absolute_pathwise_Cost_minus_Info_cancellation_proved": False,
        "GR_closed": False,
        "status": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
