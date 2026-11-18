"""Second material contrast of the complete homogeneous runtime clock of (880)."""

import json
from fractions import Fraction as F
from math import factorial
from pathlib import Path

import numpy as np
import sympy as sp


def require(test, label):
    if not test:
        raise AssertionError(label)


def alphabet():
    u = sp.symbols("u")
    f = u**4 + u**2 - 1
    require(sp.Poly(f, u).is_irreducible, "degree four")
    p = (sp.sqrt(5) - 1) / 2
    a = sp.sqrt(p)
    phi = 1 / p
    C = sp.sqrt(phi) + phi
    require(bool(C < 3) and bool(p**-6 < 18), "rational upper bounds")
    embeddings = (a, -a, sp.I * sp.sqrt(phi), -sp.I * sp.sqrt(phi))
    G = sp.Matrix([[u, -u**2], [u**2, u]])
    ident = sp.eye(2)
    cx = sp.eye(4)
    cx.row_swap(2, 3)
    g0 = sp.kronecker_product(G, ident)
    g1 = sp.kronecker_product(ident, G)

    def reduce(matrix):
        return matrix.applyfunc(lambda entry: sp.rem(entry, f, u))

    v0 = reduce(g0 * cx * g1)
    v1 = reduce(cx * g1 * g0)
    require(reduce(v0.T * v0) == sp.eye(4), "native all-column orthogonality")
    require(reduce(v1.T * v1) == sp.eye(4), "second native word orthogonality")
    diff = v0 - v1
    entries = set(diff) - {0}
    require(bool(entries), "three-stage all-column pair is distinct")
    norms = set()
    for entry in entries:
        norm = sp.resultant(f, entry, u)
        require(norm.is_Integer and norm != 0, "nonzero integral field norm")
        norms.add(abs(int(norm)))
    for index, root in enumerate(embeddings):
        def embedded(matrix):
            return np.array(matrix.subs(u, root).evalf(), dtype=complex)
        expected = 1. if index < 2 else float(C)
        require(abs(np.linalg.norm(embedded(g1), 2) - expected) < 1e-12,
                "true conjugate operator norm, not entrywise growth")
        require(np.linalg.norm(embedded(diff), 2) <= 2 * expected**3 + 1e-11,
                "conjugate word bound")
    return sorted(norms)


def material_pair():
    p = (5**0.5 - 1) / 2
    a = p**0.5
    e, slack, top = np.eye(3)
    vacuum = a * e + p * slack
    # tan(theta/2)=1/8. This is an exact (880) target, tested numerically.
    s = 16 * p / 65
    m_plus = a * e + (63 * p / 65) * slack + s * top
    m_minus = a * e + (63 * p / 65) * slack - s * top

    def source_rotation(m):
        k = np.outer(m, e) - np.outer(e, m)
        return np.eye(3) + k + k @ k / (1 + a)

    m0 = source_rotation(vacuum)
    plus, minus = (source_rotation(m) @ m0.T for m in (m_plus, m_minus))
    for op, m in ((plus, m_plus), (minus, m_minus)):
        require(np.linalg.norm(op @ vacuum - m) < 1e-14, "field reached")
        require(np.linalg.norm(op.T @ op - np.eye(3)) < 1e-14, "all columns")
    dist = np.linalg.norm(plus - minus, 2)
    require(2 * s - 1e-14 <= dist <= 2.5 * s, "real register source bound")
    # Squaring gives (8/3)/(1+a)<25/16, since a>3/4.
    require(F(8, 3) / (1 + F(3, 4)) < F(25, 16), "Lipschitz < 5/4")
    return dist / (2 * s)


def bound(n):
    x = F(2, 55)
    q = x**n / factorial(n)
    heat = F(176, 359) * q / ((1-x*x) * (1-q)**2)
    return 1152 * 18 * 81**n * heat


def main():
    pilot = Path(__file__).resolve().parents[2]
    research = pilot.parents[2]
    statute = research / "A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    owner = statute.read_text()
    for line in ("tensor I_RIGHT.       (880)", "x=2/55,q_N=x^N/N!",
                 "Compile the preparations and fixed processor separately"):
        require(line in owner, "primary pointer: " + line)
    a73 = (pilot / "round73/matter/SHIFTED_MATTER_ROOT_RU.md").read_text()
    require("0.001554" in a73, "coordinate normalization of the necessary source")
    norms = alphabet()
    dist = material_pair()
    b18 = bound(18)
    require(b18 < F(443, 10**6) < F(1554, 10**6), "strict comparison")
    require(bound(17) > F(1554, 10**6), "certification threshold for this bound")
    for n in range(18, 56):
        require(bound(n + 1) / bound(n) < F(162, 55*(n + 1)), "ratio decay")
    print(json.dumps({
        "native_nonzero_entry_absolute_norms": norms,
        "true_880_distance_over_twice_step": round(dist, 12),
        "heat_mixed_row_bound_N18": float(b18),
        "heat_mixed_row_bound_N26": float(bound(26)),
        "a73_required_max_row_strictly_above": 0.001554,
        "same_hjr_price_binding_proved": False,
        "GR_closed": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
