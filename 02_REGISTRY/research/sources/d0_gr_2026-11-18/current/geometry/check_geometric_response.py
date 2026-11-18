"""Symbolic controls for the measurement identities (Python 3, SymPy)."""
import json
import sympy as sp


def main():
    x, y, u, v, c, d, eps, s, gain = sp.symbols("x y u v c d eps s gain")
    a = x + u
    b = y + v
    bad = c*a + d*b + eps*(a**2 + b**2)
    same = sp.diff(bad, x, u)
    other = sp.diff(bad, x, v)
    assert sp.simplify(same - 2*eps) == 0 and other == 0
    witness = {x: 1, y: 2, u: 2, v: 3, c: 1, d: 1, eps: 1}
    obstruction = same*sp.diff(bad, v) - other*sp.diff(bad, u)
    assert obstruction.subs(witness) == 22
    # A monotone non-affine target. Use a genuinely nonlinear local term.
    target = x**2 + 2*y**2 + 3*u**2 + 4*v**2
    raw = sp.log(1 + target)
    for i, j in ((x,u), (x,v), (y,u), (y,v)):
        assert sp.simplify(sp.diff(raw, i, j) + sp.diff(raw, i)*sp.diff(raw, j)) == 0
        assert sp.simplify(sp.diff(sp.exp(raw), i, j)) == 0
    # Four physical radii, with the overall scale left symbolic.
    roots = (1, gain**2, gain**4)
    P = sp.prod(s-root for root in roots)
    for i, root in enumerate(roots):
        assert sp.simplify(P.subs(s, root)) == 0
        projector = sp.prod((s-r)/(root-r) for r in roots if r != root)
        for j, value in enumerate(roots):
            assert sp.simplify(projector.subs(s, value)) == int(i == j)
        k = 2*i
        assert sp.simplify(2 - (k-2) - (4-k)) == 0
        assert sp.simplify(-(k-4) - (4-k)) == 0
    # Genuine prepared-code corner with two profiles on a common repeated input.
    q, c0, g = sp.symbols("q c0 g", nonzero=True)
    first_u, second_u, first_v, second_v = sp.symbols("a1 a2 b1 b2")
    mean_u = q*first_u + (1-q)*second_u
    mean_v = q*first_v + (1-q)*second_v
    moment = q*first_u*first_v + (1-q)*second_u*second_v
    assert sp.expand(moment - mean_u*mean_v -
                     q*(1-q)*(first_u-second_u)*(first_v-second_v)) == 0
    for copies in (1, 2, 3):
        total = (q*(c0-2*g*(first_u*u+first_v*v))**copies
                 +(1-q)*(c0-2*g*(second_u*u+second_v*v))**copies)
        at_origin = {u: 0, v: 0}
        measured_u = sp.diff(total, u).subs(at_origin)
        measured_uv = sp.diff(total, u, v).subs(at_origin)
        assert sp.simplify(measured_u+2*g*copies*c0**(copies-1)*mean_u) == 0
        predicted_uv = 4*g**2*copies*(copies-1)*c0**(copies-2)*moment
        assert sp.simplify(measured_uv-predicted_uv) == 0
    print(json.dumps(dict(log_price_common_ratio=-1, mixed_species=0,
                          equal_species="2*epsilon", obstruction_at_integer_witness=22,
                          scale_projectors=3, prepared_code_repeats=[1,2,3],
                          mark="symbolic_controls_only"), indent=2))


if __name__ == "__main__":
    main()
