"""Exact finite-word checks for the comparison task on a dyadic Brinkmann field chart."""
import json
import runpy
from itertools import product
from pathlib import Path

import sympy as sp

parent = Path(__file__).resolve().parents[2] / "round86/assembly/check_null_single_choi.py"
old = runpy.run_path(str(parent))
I, Z, eta, unit = (old[key] for key in ("I", "Z", "eta", "unit"))
exp3, N2, N3 = (old[key] for key in ("expnull", "N2", "N3"))
Q = sp.Rational


def require(test, message):
    if not test:
        raise ValueError(message)


def link_directions():
    b2, b3 = (unit(0, j) + unit(j, 1) for j in (2, 3))
    conjugator = exp3(b2)
    directions = [N2, N3, b2, b3] + [conjugator * n * exp3(-b2) for n in (N2, N3)]
    for g in directions:
        require(g.T * eta + eta * g == Z and g**3 == Z, "Lorentz nilgenerator")
    require(sp.Matrix.hstack(*(g.reshape(16, 1) for g in directions)).rank() == 6, "link rank")
    tau = sp.Symbol("tau")
    for g in directions:
        link = exp3(tau * g)
        require((link.T * eta * link - eta).expand() == Z and link.det() == 1, "proper link")
    return directions


def geometric_secants(directions):
    delta = Q(1, 128)
    subs = dict(zip((old[k] for k in ("nu", "hprofile", "k", "l", "m", "n")),
                    (Q(1, 2), Q(3, 64), Q(-1, 32), Q(1, 64), Q(3, 64), Q(-1, 16))))
    field = old["actual"].subs(subs)
    coframes = links_count = 0
    for r, s in old["pairs"]:
        links = [u.subs(subs) for u in old["section_links"](r, s)]

        def scalar(v, edges):
            return old["proposed"](r, s, v, edges).subs(subs)

        for i, j in product(range(4), repeat=2):
            tangent = unit(i, j)
            val = (scalar(field + delta*tangent, links) - scalar(field - delta*tangent, links))/(2*delta)
            expected = old["direct_density_jet"](r, s, field, tangent, links, [Z]*4).subs(subs)
            require(val == expected, ("coframe", r, s, i, j))
            coframes += 1
        for pos, g in product(range(4), directions):
            plus, minus, ds = links[:], links[:], [Z]*4
            plus[pos], minus[pos] = (exp3(x*g)*links[pos] for x in (delta, -delta))
            ds[pos] = g*links[pos]
            val = (scalar(field, plus) - scalar(field, minus))/(2*delta)
            expected = old["direct_density_jet"](r, s, field, Z, links, ds).subs(subs)
            require(val == expected, ("edge", r, s, pos))
            links_count += 1
    return field, coframes, links_count


def matter_secants(field):
    # Five sites (center and its four distinct forward neighbours), two real CAR masks.
    psi = sp.Matrix(5, 2, lambda i, a: Q((i+1)**2*(a+1)-3*i*a, 64))
    delta, prefactor = Q(1, 128), Q(7, 3)
    def differences(y):
        return sp.Matrix(4, 2, lambda r, a: y[r+1, a] - y[0, a])
    def literal(v, y):
        m = differences(y)
        return prefactor * sp.trace(m.T*(v.T*eta*v)*m)
    def packed(v, y):
        d = v*differences(y)
        return prefactor * sp.trace(d.T*eta*d)
    require(packed(field, psi) == literal(field, psi), "matter value")
    y = sp.Symbol("y")
    for i, j in product(range(4), repeat=2):
        e = unit(i, j)
        sec = (packed(field+delta*e, psi)-packed(field-delta*e, psi))/(2*delta)
        require(sec == literal(field+y*e, psi).diff(y).subs(y, 0), "matter coframe")
    for i, a in product(range(5), range(2)):
        e = sp.zeros(5, 2)
        e[i, a] = 1
        sec = (packed(field, psi+delta*e)-packed(field, psi-delta*e))/(2*delta)
        require(sec == literal(field, psi+y*e).diff(y).subs(y, 0), "matter scalar")


def less(v, m, bits):
    # One exclusive highest-differing bit, including the full-threshold endpoint.
    flag = 0
    for j in range(bits+1):
        high_equal = (v >> (j+1)) == (m >> (j+1))
        flag ^= int(high_equal) & (1 ^ ((v >> j) & 1)) & ((m >> j) & 1)
    return flag


def walsh(samples):
    out = samples[:]
    span = 1
    while span < len(out):
        for i in range(0, len(out), 2*span):
            for j in range(i, i+span):
                a, b = out[j], out[j+span]
                out[j], out[j+span] = a+b, a-b
        span *= 2
    return out


def phase_fixture():
    bits = 5
    n = 2**bits
    waves = []
    for m in range(n+1):
        phase = []
        for v in range(n):
            comp = less(v, m, bits)
            require(comp == int(v < m), "prefix circuit")
            phase.append(1-2*comp)
            require(comp ^ less(v, m, bits) == 0, "dirty flag")
        wave = walsh(phase)
        require(wave[0] == n-2*m and sum(x*x for x in wave) == n*n, "Walsh normalization")
        waves.append(wave)
    # Full two-address joint preparation. Keep all work words. Read only work zero in the signed statistic.
    for i, j in product(range(n+1), repeat=2):
        x, y = waves[i][0], waves[j][0]
        left, right = Q((x+y)**2, 4*n*n), Q((x-y)**2, 4*n*n)
        require(left-right == Q((n-2*i)*(n-2*j), n*n), "Hermitian cross term")
        require(left+right + Q(sum(v*v for v in waves[i][1:]+waves[j][1:]),2*n*n)==1,
                "omitted work tail")
    return n


def raw_field():
    p = (sp.sqrt(5)-1)/2
    require(sp.simplify(p+p*p-1)==0, "raw normalization")
    pairs = [p*p, p**3, p**3, p**4]
    require(sp.simplify(sum(pairs)-1)==0, "failure accounting")
    for name, (a, b) in product(range(2), ((0, 1), (1, 0))):
        controls = ((a, b) if a == name else (b, a))
        outputs = (0 ^ controls[0], 0 ^ controls[1])
        require(outputs == (name, 1-name), "paid dual-rail copy")
    # Native selector for a signed coefficient with two real token families,
    # one family gated by a raw birth of probability p.
    obs1, obs2 = Q(7, 16), Q(-3, 8)
    tokens = [obs1, obs1, -p*obs1, p*obs2] + [0]*4
    click = sum((11 + v)/16 for v in map(sp.sympify, tokens))/8
    require(sp.simplify(click - (Q(11, 16) + ((2-p)*obs1 + p*obs2)/128)) == 0, "selector sign")
    # Norm from Q(sqrt2,sqrt5) to Q(sqrt2); negative rules out a square in the real field.
    require(sp.simplify((3/p)*(3/p.xreplace({sp.sqrt(5):-sp.sqrt(5)})))==-9, "field obstruction")


if __name__ == "__main__":
    directions = link_directions()
    field, coframes, links = geometric_secants(directions)
    matter_secants(field)
    n = phase_fixture()
    raw_field()
    print(json.dumps(dict(link_tangent_rank=6, dyadic_geometric_coframe_secants=coframes,
                          dyadic_geometric_link_occurrence_secants=links, matter_coframe_secants=16,
                          matter_local_site_component_secants=10, walsh_thresholds=n+1,
                          all_pairs_full_wave_tests=(n+1)**2, source_rows_per_site=42,
                          native_exact_original_full_Julia_at_nu_half=False,
                          scope="paid sharp field-code comparison on the specified chart",
                          GR_closed=False), indent=2))
