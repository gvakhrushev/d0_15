"""Reproduce the exact full128 jet and bound every late fine record.

Requires Python >= 3.9, SymPy and the vendored, hash-checked PR334 constructor.
"""

from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path

import sympy as sp


SOURCE = "076d5d5a7b366c0dd0970f388df7a9e6895498c4"
DIGEST = "2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66"


def require(truth, message):
    if not truth:
        raise ArithmeticError(message)


def original_jet():
    path = Path(__file__).resolve().parents[1] / "stopped" / "primary_section_7gb.py"
    script = path.read_bytes()
    # The vendored version spells popcount in the form supported by Python 3.9.
    original = script.replace(b'bin(lab & j).count("1")', b'(lab & j).bit_count()')
    original = original.replace(b'bin(bits).count("1")', b'bits.bit_count()')
    require(sha256(original).hexdigest() == DIGEST, "pinned full128 constructor")
    namespace = {"__name__": "__main__"}
    with redirect_stdout(StringIO()) as out:
        exec(compile(script, str(path), "exec"), namespace)
    require(json.loads(out.getvalue())["strictly_positive_by_integer_comparison"], "owner jet")
    return namespace


def main():
    owner = original_jet()
    ns, dns, a, da = [owner[key] for key in ("ns", "dns", "a", "da")]
    k = owner["kappa"]
    # All 63 slots including center-dark rows and their actual derivatives.
    # Skip the pair at j=0, whose two Kraus operators have zero jet here.
    squared = 0
    first_sum = sp.zeros(16)
    for n, dn in zip(ns[1:], dns[1:]):
        m = n.H * a
        dm = dn.H * a + n.H * da
        squared += sum(sp.expand(x * sp.conjugate(x)) for x in dm)
        first_sum += dm.H * m + m.H * dm
    require(first_sum.applyfunc(sp.expand) == sp.zeros(16), "conditional instrument zero normalization jet")
    h2 = sp.factor(squared / (16 * k * (1-k)))
    require(0 < h2 < sp.Rational(36, 25), "normalized Frobenius insertion norm h < 6/5")

    p = (sp.sqrt(5) - 1) / 2
    quiet_continue = 4 * p**3 * k**2
    active_continue = 4 * p**3 * k * (1-k)
    quiet_stop = (1 - 2 * p**2 * k)**2
    active_stop = 4 * p**4 * k * (1-k)
    require(sp.simplify(quiet_continue + active_continue + quiet_stop + active_stop - 1) == 0,
            "four true type probabilities")
    s = active_continue / (1-quiet_continue)
    w0 = quiet_stop / (1-quiet_continue)
    w1 = (active_stop + active_continue*w0) / (1-quiet_continue)
    require(sp.simplify(w0 + w1 / (1-s) - 1) == 0, "all counts normalized")
    visit_active = active_stop + active_continue
    delta = owner["answer"] / visit_active
    expected = sp.Rational(12,631) * (41*sp.log(2) + 16*sp.log(3)-4*sp.log(5))
    require(sp.simplify(delta-expected) == 0, "one conditional active jet")

    # log(2)>2/3 by the atanh(1/3) series. log(2)<7/10 by the exp series.
    require(2**41 * 3**16 > 2**56 * 5**4, "strict lower one-event logarithm")
    require(sum(F(7,10)**n / sp.factorial(n) for n in range(4)) > 2, "upper log bound")
    p_upper = F(31,50)
    require((2*p_upper+1)**2 > 5, "upper golden p")
    lam = F(9,640)
    s_upper = F(1,74)
    require(4*p_upper**3*lam/(1-4*p_upper**3*lam**2) < s_upper, "upper continuation")
    late = 2*F(6,5) * (F(21,5)*((1+s_upper)/(1-s_upper)**3-1)
                        + 2*((1-s_upper)**-2-1))
    one_lower = F(448,631)
    require(late == F(6751836,9725425) and one_lower > late, "strict all-length sign")
    print(json.dumps({
        "source_commit": SOURCE, "full128_original_checker": DIGEST,
        "conditional_insert_norm_squared": str(h2),
        "late_bound_divided_by_w1": str(late),
        "first_lower_divided_by_w1": str(one_lower),
        "strict_lower_divided_by_w1": str(one_lower-late),
        "zero_active_probability_diagnostic": float(w0),
        "one_active_probability_diagnostic": float(w1),
        "next_active_ratio_diagnostic": float(s),
        "full_stopped_fine_source_strictly_positive": True,
        "native_paid_port_source_on_same_tangent": 0,
        "selected_Book_Info": False, "GR_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
