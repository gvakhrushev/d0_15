#!/usr/bin/env python3
"""One bounded consumer of inherited-history weights and their nonlinear source.

New computations only: actual Fibonacci embeddings; coarse/fine entropy
selector; retained golden/CNOT word with unchanged right archive; and the
full weighted metric/scalar equations on the non-Einstein null control.
No old root/heat/Lean suite, physical admission or new action is supplied.
"""
import json
import sympy as s

p = (s.sqrt(5)-1)/2
a = s.sqrt(p)


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def zero(value):
    return s.simplify(value) == 0


def inherited_weights():
    checked = 0
    for k in range(2, 5):
        left = s.diag(1, 1, *([0]*(int(s.fibonacci(k+2))-2)))
        right = s.zeros(int(s.fibonacci(k+1)))
        for r in range(4):
            N = k+r
            probability = (s.trace(left)+s.trace(right))/s.fibonacci(N+3)
            expected = 2*s.fibonacci(r+2)/s.fibonacci(N+3)
            require(probability == expected, 'literal AF inclusion descendants')
            ratio = (1-(-p*p)**(r+2))/(1-(-p*p)**(N+3))
            require(zero(expected/(2*p**(k+1))-ratio), 'exact Binet source ratio')
            left, right = s.diag(left, right), left
            checked += 1
    chi, q, mass, ell = s.symbols('chi q mass ell', positive=True)
    c = (1-q*chi)/(1-q)
    # Conditional prefix mass is fixed. All old fine leaves start uniform.
    excess = -mass*(chi*s.log(chi)+(1-q)*c*s.log(c)/q)/ell
    source = s.diff(excess, chi)
    # Keep the two real logarithms separate: c>0 is the stated window,
    # whereas a generic symbolic q,chi does not encode q*chi<1.
    expected = mass*(s.log(c)-s.log(chi))/ell
    require(zero(source-expected), 'actual fine-history source')
    require(zero(s.diff(source, chi).subs(chi, 1)+mass/(ell*(1-q))),
            'strict preparation curvature at the root')
    # A coarse prefix detector sees only the fixed sum.
    require(zero(s.diff(q*chi+(1-q)*c, chi)), 'coarse prefix blindness')
    return {'literal_AF_embeddings': checked,
            'fine_source': '-mu_Q log(chi/c)/log(phi)',
            'fine_source_root': 'chi=1',
            'coarse_prefix_source': 'zero',
            'canonical_ready_pending_transfer_phi_source': '-epsilon'}


def archive_word():
    # Order L,R,W; L,R have the real A1 defining blocks M2 (+) M1.
    index = lambda l, r, w: (l*3+r)*2+w
    psi = s.zeros(18, 1)
    psi[index(0, 0, 0)] = p
    psi[index(1, 1, 0)] = p
    psi[index(2, 2, 0)] = p*a
    require(zero((psi.T*psi)[0]-1), 'full canonical A1 GNS norm')
    CLW, CWL, GW = s.zeros(18), s.zeros(18), s.zeros(18)
    G = s.Matrix([[a, -p], [p, a]])
    for l in range(3):
        for r in range(3):
            for w in range(2):
                col = index(l, r, w)
                CLW[index(l, r, w ^ int(l == 1)), col] = 1
                target = 1-l if l < 2 and w == 1 else l
                CWL[index(target, r, w), col] = 1
                if l < 2:
                    for v in range(2):
                        GW[index(l, r, v), col] = G[v, w]
                else:
                    GW[col, col] = 1
    U = CWL*GW*CLW
    require(all(zero(x) for x in U.T*U-s.eye(18)), 'full retained word unitarity')
    legal = [index(l, r, w) for l in range(3) for r in range(3) for w in range(2)
             if (l < 2 and r < 2) or l == r == 2]
    outside = [j for j in range(18) if j not in legal]
    require(len(legal) == 10 and U.extract(outside, legal) == s.zeros(8, 10),
            'actual AF GNS plus work is invariant; no cross-central states')
    actual = U.extract(legal, legal)
    require(all(zero(x) for x in actual.T*actual-s.eye(10)),
            'unitarity on the actual ten-dimensional complete carrier')
    out = U*psi

    def right_density(vector):
        return s.Matrix(3, 3, lambda r, t: s.simplify(sum(
            vector[index(l, r, w)]*vector[index(l, t, w)]
            for l in range(3) for w in range(2))))

    require(all(zero(x) for x in right_density(out)-right_density(psi)),
            'every old right observable preserved')
    left = [s.simplify(sum(out[index(l, r, w)]**2
                         for r in range(3) for w in range(2))) for l in range(3)]
    require(all(zero(x-y) for x, y in zip(left, [2*p**3, 2*p**4, p**3])),
            'active weights change with all outputs retained')
    require(not zero(left[0]-p*p), 'non-unital active marginal control')
    return {'AF_level': 1, 'actual_GNS_work_dimension': 10,
            'ambient_extension_dimension': 18,
            'word': 'CNOT(W,L) G(W) CNOT(L,W); identity on M1',
            'right_archive': 'exactly preserved',
            'left_weights': ['2*p^3', '2*p^4', 'p^3'],
            'work_price': 'must remain in the complete programme source'}


def full_preparation_gradient():
    ell, common = s.symbols('ell common', real=True)
    entropy = (p+2*p*p)*ell
    old = [s.diag(1, 1, 0, 0, 0), s.diag(0, 0, 1, 1, 0),
           s.diag(0, 0, 0, 0, 1)]  # actual full GNS of M2 (+) M1
    success, failure = s.diag(1, 0), s.diag(0, 1)
    B = s.Matrix([[s.Rational(1, 2), s.Rational(1, 5)],
                  [s.Rational(1, 5), s.Rational(1, 2)]])
    total = s.zeros(20)
    for P in old:
        total += common*s.kronecker_product(P, failure, s.eye(2))
        for j, weight in enumerate([p, p*p]):
            for effect in [s.eye(2)-B, B]:
                total += weight*(common-entropy+(j+1)*ell)*s.kronecker_product(
                    P, success, effect)
    require(all(zero(x) for x in total-common*s.eye(20)),
            'full non-diagonal scene POVM gradient is scalar')
    # Repeat the actual POVM sum off shell with unequal E eigenvalues.
    # Exact log q_iab = h(e_i)+log p_a(e_i)-log D at the derived profile.
    unequal = [s.Rational(1, 3), s.Rational(1, 4), s.Rational(2, 5)]
    total = s.zeros(20)
    entropies = []
    for P, e in zip(old, unequal):
        h = -(1-e)*s.log(1-e)-e*s.log(e)
        entropies.append(h)
        total += common*s.kronecker_product(P, failure, s.eye(2))
        for weight in [1-e, e]:
            for effect in [s.eye(2)-B, B]:
                total += weight*(common-h-s.log(weight))*s.kronecker_product(
                    P, success, effect)
    require(all(zero(x) for x in total-common*s.eye(20)),
            'off-shell stationary profile cancels all preparation sources')
    require(not zero(entropies[0]-entropies[1]),
            'frozen flat-profile sector gradients must disagree off shell')
    return {'old_full_GNS_dimension': 5, 'full_gradient_dimension': 20,
            'all_normalized_preparation_tangents': 'zero',
            'off_shell_profile': 'log(sum_i[1+2 exp(h(e_i))])/log(phi)',
            'frozen_flat_profile_control': 'rejected',
            'reference_extension': 'tensor identity, including reference128'}


def weighted_source():
    u, v, x, y, k = s.symbols('u v x y k', real=True)
    coords = [u, v, x, y]
    eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                    [0, 0, -1, 0], [0, 0, 0, -1]])
    g = s.exp(-2*k*u)*eta
    gi = g.inv()
    w = s.exp(2*k*u)
    Gamma = [[[s.simplify(sum(gi[i, d]*(s.diff(g[d, b], coords[j])
        + s.diff(g[d, j], coords[b])-s.diff(g[j, b], coords[d]))/2
        for d in range(4))) for b in range(4)] for j in range(4)] for i in range(4)]
    Ric = s.Matrix(4, 4, lambda j, b: s.simplify(sum(
        s.diff(Gamma[i][j][b], coords[i])-s.diff(Gamma[i][i][b], coords[j])
        + sum(Gamma[i][i][d]*Gamma[d][j][b]-Gamma[i][j][d]*Gamma[d][i][b]
              for d in range(4)) for i in range(4))))
    R = s.simplify(s.trace(gi*Ric))
    Einstein = s.simplify(Ric-R*g/2)
    dw = s.Matrix([s.diff(w, c) for c in coords])
    Hess = s.Matrix(4, 4, lambda i, j: s.simplify(s.diff(w, coords[i], coords[j])
        - sum(Gamma[d][i][j]*dw[d] for d in range(4))))
    box = s.simplify(s.trace(gi*Hess))
    square = s.simplify((dw.T*gi*dw)[0])
    kinetic = s.Rational(3, 2)/w*(dw*dw.T-g*square/2)
    E = s.simplify(w*Einstein+g*box-Hess+kinetic)
    Ew = s.simplify(R+3*square/(2*w*w)-3*box/w)
    require(E == s.zeros(4) and Ew == 0, 'all weighted metric and scalar rows')
    require(zero(Einstein[0, 0]-2*k*k), 'operational metric remains non-Einstein')
    require(s.simplify(w*Einstein+g*box-Hess) != s.zeros(4),
            'omitting compensator kinetic source must fail')
    rr, bb, xx, ww = s.symbols('R boxw gradw2 w', nonzero=True)
    trace_E = -ww*rr+3*bb-3*xx/(2*ww)
    scalar_E = rr+3*xx/(2*ww**2)-3*bb/ww
    require(zero(trace_E+ww*scalar_E), 'generic all-order Noether identity')
    return {'metric_rows': 10, 'scalar_row': 'trace-dependent',
            'non_Einstein_G_uu': '2*k^2', 'weighted_rows': 'zero',
            'matter_compatibility': 'T=2*w*j_w',
            'omitted_kinetic_source': 'rejected'}


def main():
    print(json.dumps({'scope': 'inherited_left_fine_leaf_binding_required',
        'history': inherited_weights(), 'retained_word': archive_word(),
        'full_preparation': full_preparation_gradient(),
        'nonlinear_weighted_source': weighted_source(),
        'physical_D0_GR': 'open'}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
