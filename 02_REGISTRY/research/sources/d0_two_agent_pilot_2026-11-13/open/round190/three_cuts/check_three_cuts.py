"""Exact marked ancillary preparation and angular response of three cuts."""

from itertools import product
import json
from pathlib import Path
import sys

import sympy as sp

PILOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PILOT / "open/round186"))
from check_car_completion import A, P, lcu_amplitudes, reduce, require


def main():
    zeta = sp.Matrix([1 + A, P, 1 - A, P]) / 2
    require(reduce(zeta.dot(zeta)) == 1, "Wrong ancillary normalization")
    lcu = lcu_amplitudes([zeta], 4)
    require(lcu["common_coefficient_denominator"] == 2
            and lcu["coherent_label_bits"] == 3 and lcu["M_terms_per_lookup"] == [6],
            "The one-column B186 loader must use six of eight labels")

    r = [reduce(zeta[2*h]**2 + zeta[2*h+1]**2) for h in (0, 1)]
    require(r == [(1 + A)/2, (1 - A)/2], "Wrong head law")
    require(reduce(r[0]*r[1] - P**2/4) == 0, "Wrong geometric mean")
    gain = A + A**3  # 1/a in Q(a).
    require(reduce(A*gain) == 1 and reduce(gain**2 - 1 - P) == 0,
            "Wrong exact factor for observing one genuinely random head")

    # Dephased old outputs route the two independent ancillary states by a
    # literal basis permutation. Keep each copied head's NC1 tail coherent.
    for cosine in (False, True):
        for retained in (0, 1, 2):
            grouped = {}
            for i, j in product(range(4), repeat=2):
                outcome = (i//2, j//2)[:retained] if cosine else (0,)*retained
                grouped[outcome] = grouped.get(outcome, 0) + zeta[i]**2*zeta[j]**2
            require(reduce(sum(grouped.values())) == 1, "The old marginal changed")
            for key, mass in grouped.items():
                expected = sp.prod(r[bit] for bit in key) if cosine else 1
                require(reduce(mass - expected) == 0, "Wrong retained mark law")

    # Coefficient of sin(x) in gain^n*cos(theta+x)+sin(theta+x).
    responses = [reduce(A - gain**n*P) for n in (0, 1, 2)]
    require(responses == [A - P, 0, A - 1], "Wrong sign or cancellation")
    return {"status": "PASS", "one_ancillary_lcu": lcu,
            "one_ancillary_ideal_success": "p^3/16",
            "old_Born_marginal_identical_on_each_cut": True,
            "cosine_refinement_factor": "a^-n",
            "odd_angular_coefficients": ["a-p", "0", "a-1"],
            "Book03_full_Cost_minus_Info_identified": False, "GR_closed": False}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
