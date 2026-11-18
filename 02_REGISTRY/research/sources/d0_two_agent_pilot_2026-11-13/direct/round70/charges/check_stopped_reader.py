"""Exact two-event price response and certified bounds for a full stopped reader."""

from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import runpy

import sympy as sp


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def tracemul(left, right):
    return sp.expand(sum(value*right.get((j, i), 0) for (i, j), value in left.items()))


def sparse(matrix):
    return matrix.applyfunc(sp.expand).todok()


def conditional_variations(source):
    ns, dns, a, da, lam = [source[key] for key in ("ns", "dns", "a", "da", "kappa")]
    entries, fine = [], {}
    dim = a.rows
    eye, parity = sp.eye(dim), source["pi"]
    rare_effect, parity_return = sp.zeros(dim), lam*parity
    rare_indices = []
    for j, (n, dn) in enumerate(zip(ns[1:], dns[1:]), 1):
        if not sparse(n):
            continue  # Every word containing this letter has zero probability jet.
        b = n.H*a
        db = dn.H*a + n.H*da
        normalizer = lam*(1-lam)
        effect = sparse(b.H*b/normalizer)
        deffect = sparse((db.H*b+b.H*db)/normalizer)
        out = sparse(n.H*n/(1-lam))
        dout = sparse((dn.H*n+n.H*dn)/(1-lam))
        require(sparse(b*b.H/normalizer) == out and sparse((db*b.H+b*db.H)/normalizer) == dout,
                "actual outgoing conditional jet")
        entries.append((effect, deffect, out, dout))
        e = sp.MutableSparseMatrix(dim, dim, effect)
        require(tracemul(effect, parity.todok()) == 0, "parity-blind true single-label probability")
        if sparse(e - sp.trace(e)*eye/dim):
            rare_indices.append(j)
            rare_effect += e
        # B_0=Lambda=lam I. Here T(parity)/q = sum B_j parity B_j^dagger/lam.
        parity_return += b*parity*b.H/lam
        fine[j] = sp.Rational(1, dim)*sum(deffect.get((k, k), 0) for k in range(dim))
    pair = [sp.Rational(1, dim)*(tracemul(de, out) + tracemul(e, dout))
            for _, _, out, dout in entries for e, de, _, _ in entries]
    require(len(pair) == 400 and sum(fine.values()) == 0 and sum(pair) == 0, "complete first and second jets")
    t1, t2 = [F(sum(abs(x) for x in xs)/2) for xs in (fine.values(), pair)]
    require(t2 == F(122472,398161), "all 400 original two-event outcomes")
    bit_jets = [sum(val for j, val in fine.items() if (j >> bit) & 1) for bit in range(6)]
    require(rare_indices == [13,29,45,61], "four non-scalar recorded addresses")
    require(sparse(rare_effect-eye*sp.Rational(32,3155)) == {}, "scalar rare-address sum")
    parity_factor = sp.expand(parity_return[0,0])
    require(sparse(parity_return-parity_factor*parity) == {}, "true repeated odd-port transport of parity")
    return t1, t2, bit_jets, parity_factor


def main():
    here = Path(__file__).resolve().parents[2]
    path = here / "round69" / "stopped" / "primary_section_7gb.py"
    raw = path.read_bytes().replace(b'bin(lab & j).count("1")', b'(lab & j).bit_count()')
    raw = raw.replace(b'bin(bits).count("1")', b'bits.bit_count()')
    require(sha256(raw).hexdigest() == "2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66",
            "actual source bytes")
    with redirect_stdout(StringIO()):
        base = runpy.run_path(str(path))
    t1, t2, bits, parity_factor = conditional_variations(base)
    require(t1 == F(108,631), "13 nonzero first probability jets")
    p = (sp.sqrt(5)-1)/2
    k = sp.Rational(9,640)
    q = 4*p**3*k
    reader = sp.factor(p**3 * 4*p**2*k*(1-k)*sum(bits)/(1-q))
    require(sp.simplify(reader - 81*p**5/(12800*(1-q))) == 0, "actual repeated six-pointer price")
    # Upper intervals use rational arithmetic, including the alternating quiet-stop rate.
    lo, hi = F(61803398874989,10**14), F(61803398874990,10**14)
    require(lo*(1+lo) < 1 < hi*(1+hi), "Golden p bracket")
    k = F(9,640)
    a0 = 4*hi**3*k**2
    a1 = 4*hi**3*k*(1-k)
    b0 = (1-2*lo**2*k)**2
    b1 = 4*hi**4*k*(1-k)
    s = a1/(1-a0)
    w1 = (b1 + b0*s)/(1-a0)
    v1 = (a1+b1 + (a0+b0)*s)/(1-a0)
    tail = F(6,5)*s*s*(3-2*s)/(1-s)**2
    total = t1 + s*t2 + tail
    terminal, visits = w1*total, v1*total
    require(terminal < F(3677,10**6) and visits < F(5979,10**6), "stopped tariff diameters")
    require(F(1)+sum(F(482,1000)**n/sp.factorial(n) for n in range(1,5)) > 1+hi, "log(phi)<.482")
    reader_upper = 81*hi**5/(12800*(1-4*hi**3*k))
    reader_lower = 81*lo**5/(12800*(1-4*lo**3*k))
    lnphi_upper = F(482,1000)
    atan_z = lo/(2+lo)
    lnphi_lower = F(48,100)
    require(2*(atan_z+atan_z**3/3)>lnphi_lower, "lower atanh bound for log(phi)")
    for nu, lower, upper in ((1, F(3244,100000), F(3273,100000)), (2, F(4852,100000), F(4895,100000))):
        require((nu+1)*F(1636,100000)-nu*lnphi_upper*reader_upper > lower and
                (nu+1)*F(1650,100000)-nu*lnphi_lower*reader_lower < upper,
                "same-record Bellman normalization")
    require((reader_upper+9*terminal)*lnphi_upper < F(1636,100000), "reader plus nine-unit terminal tariff")
    require((reader_upper+5*visits)*lnphi_upper < F(1551,100000), "reader plus five-unit adaptive tariff")
    prep = 2*hi**3*4*hi**2*k*(1-k)*F(32,3155)/(1-4*hi**3*k)
    require(prep < F(104,10**6), "range of complete readout-price operator in input")
    print(json.dumps({
        "first_conditional_label_TV": str(t1), "two_conditional_label_TV": str(t2),
        "per_address_bit_jets": list(map(str, bits)), "six_pointer_all_visits_price_jet": "81*p^5/(12800*(1-4*p^3*lambda))",
        "reader_Golden_units_diagnostic": float(reader), "terminal_TV_upper_diagnostic": float(terminal),
        "all_visited_prefix_TV_upper_diagnostic": float(visits), "one_terminal_tariff_nine_units_insufficient_for_classical_gain": True,
        "T_odd_parity_divided_by_q": str(parity_factor), "reader_preparation_oscillation_upper_diagnostic": float(prep),
        "past_dependent_each_visit_five_units_insufficient_for_conditional_CQ_gain": True, "GR_closed": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
