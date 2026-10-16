#!/usr/bin/env python3
"""New exact full16 first-shell test; no old checker entrypoints or root replay."""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
PINS = {
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py':
        'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/sources/d0_causal_cone_source_2026-10-16/check_causal_cone_source.py':
        '3dd6e594e106f7bb5f6453bf9ab5f1bfc34dd4cf891d7d2fa83531b6353c059a',
}


def run():
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    for path, digest in PINS.items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest,
                'input_pin_' + Path(path).name)
    path = ROOT / next(iter(PINS))
    nodes = [node for node in ast.parse(path.read_text()).body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and
              t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    require(len(nodes) == 2, 'only_creator_and_order_definitions_extracted')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
    c = [scope['creator'](j) for j in range(4)]
    b = [ci.T for ci in c]
    zero, ident = s.zeros(16), s.eye(16)
    gamma = [c[j]-b[j] for j in range(4)]
    require(all(c[i]*b[j]+b[j]*c[i] == (ident if i == j else zero)
                for i in range(4) for j in range(4)), 'actual_full16_CAR')

    def lift(a):
        return sum((a[i,j]*c[i]*b[j] for i in range(4) for j in range(4)
                    if a[i,j] != 0), s.zeros(16))

    def elementary(i,j):
        a = s.zeros(4)
        a[i,j] = 1
        return a

    # Fourier powers exp(i*k*y), theta=y on the 2pi-periodic torus.
    # These are the coordinate-covector proper LC generators of the cone owner.
    e = elementary
    mr = [
        {2: e(0,2)/(2*s.I)-e(1,2)/2,
         -2: -e(0,2)/(2*s.I)-e(1,2)/2, 0: e(2,1)},
        {2: -e(0,2)/2-e(1,2)/(2*s.I),
         -2: -e(0,2)/2+e(1,2)/(2*s.I), 0: -e(2,0)},
        {0: e(0,1)-e(1,0)}, {},
    ]
    h = [{k: lift(a) for k,a in m.items()} for m in mr]
    require(all(sum((c[r]*h[r].get(k, zero) for r in range(4)),
                    s.zeros(16)) == zero for k in (-2,0,2)),
            'full16_Cartan_cancellation_in_continuum_raising_part')
    require(all(k == 0 or r != 2 for r,m in enumerate(h) for k in m),
            'each_connection_coefficient_constant_in_its_own_edge_direction')
    qcoef = [{k: c[r]*a-a.T*b[r] for k,a in m.items()}
             for r,m in enumerate(h)]
    potential = {}
    for r,m in enumerate(h):
        for j,a in m.items():
            for k,bb in m.items():
                potential[j+k] = potential.get(j+k, s.zeros(16)) + (
                    c[r]*a*bb+a.T*bb.T*b[r])/2

    shell = [tuple(sign if r == j else 0 for r in range(4))
             for j in range(4) for sign in (-1,1)]

    def same_transverse(q,p):
        return all(q[r] == p[r] for r in (0,1,3))

    def d0(p):
        return s.I*sum((gamma[r]*p[r] for r in range(4)), s.zeros(16))

    def d1_direct(q,p, omit_quadratic=False):
        if not same_transverse(q,p):
            return s.zeros(16)
        k = q[2]-p[2]
        out = (s.zeros(16) if omit_quadratic else
               potential.get(k, s.zeros(16)).copy())
        out += s.I*sum((p[r]*qcoef[r].get(k, zero)
                         for r in range(4)), s.zeros(16))
        if k == 0:
            out -= sum(((c[r]+b[r])*p[r]**2/2 for r in range(4)), s.zeros(16))
        return out

    def raising_first(q,p):
        # Independent Taylor of exp(h*Gamma(M_r))*exp(i*h*p_r).
        # The adjoint is applied only after assembling Fourier matrix entries.
        if not same_transverse(q,p):
            return s.zeros(16)
        k = q[2]-p[2]
        out = s.zeros(16)
        for r,m in enumerate(h):
            square = sum((a*bb for j,a in m.items() for ell,bb in m.items()
                          if j+ell == k), s.zeros(16))
            out += c[r]*(square/2+s.I*p[r]*m.get(k, zero))
            if k == 0:
                out -= c[r]*p[r]**2/2
        return out

    def assemble(omit_quadratic=False):
        return s.BlockMatrix([[(d0(q)*d1_direct(q,p,omit_quadratic) +
                                d1_direct(q,p,omit_quadratic)*d0(p))
                               .applyfunc(s.expand) for p in shell]
                              for q in shell]).as_explicit()

    require(all(d1_direct(q,p) == (raising_first(q,p) +
                s.conjugate(raising_first(p,q).T)).applyfunc(s.expand)
                for q in shell for p in shell),
            'all64_D1_blocks_match_independent_forward_Taylor_and_true_adjoint')
    a = assemble()
    require(a == s.conjugate(a.T), 'full128_shell_A1_Hermitian')
    require(s.trace(a) == 0, 'faithful_trace_zero_does_not_imply_matrix_zero')
    require(s.trace(a*a) == 52, 'exact_full128_squared_resonant_norm_52')
    require(a[0,5] == s.I/2 and a[2,4] == 1,
            'two_nonzero_exact_resonant_witnesses')
    require(a[0:16,0:16] != zero and a[64:80,80:96] != zero,
            'diagonal_and_opposite_y_momentum_blocks_both_retained')
    # The same operator and faithful purification have real cos/sin coordinates.
    u2 = s.Matrix([[1,s.I],[1,-s.I]])/s.sqrt(2)
    u = s.diag(*[s.kronecker_product(u2,ident) for _ in range(4)])
    ar = (s.conjugate(u.T)*a*u).applyfunc(s.simplify)
    require(s.conjugate(u.T)*u == s.eye(128) and
            ar == ar.T and s.conjugate(ar) == ar,
            'real_full128_cosine_sine_preparation_chart')
    require(s.trace(ar*ar)/128 == s.Rational(13,32),
            'minimum_faithful_first_amplitude_residual_squared_13_over_32')
    bad = assemble(omit_quadratic=True)
    require(bad != a and s.trace((a-bad)*s.conjugate((a-bad).T)) > 0,
            'hostile_omit_actual_connection_square_rejected')
    require(s.trace(a*a) != s.trace(a)**2/128,
            'hostile_replace_matrix_by_scalar_trace_rejected')
    require(a[64:80,80:96] != zero,
            'hostile_drop_opposite_momentum_coupling_rejected')
    return {
        'status': 'PASS', 'checks': checks, 'exact_check_groups': len(checks),
        'source_pins': PINS, 'full_Fock_components': 16,
        'shell_momenta': [list(p) for p in shell], 'reference_dimension':128,
        'base_torus': '(R/2pi Z)^4', 'theta': 'y', 'positive_metric': 's^2 I4',
        'geometry': 'exact proper LC links, no h-dependent field counterjet',
        'A1_shell_trace_at_s1': '0', 'A1_shell_squared_trace_at_s1': '52',
        'faithful_amplitude_residual_squared': '13/(32 s^4)',
        'first_amplitude_Euler_residual_squared': '13/(8 s^4)',
        'scope': 'excludes a differentiable faithful-full-shell stationary amplitude continuation on this fixed exact-LC sampled cone; arbitrary amplitude C1 cannot cancel the resonant block',
        'not_excluded': ['changed first geometric or link jets', 'other leading preparations',
                         'other shells or cones', 'all native joint branches',
                         'original fixed-g fixed-tau h^-2 comparator'],
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
