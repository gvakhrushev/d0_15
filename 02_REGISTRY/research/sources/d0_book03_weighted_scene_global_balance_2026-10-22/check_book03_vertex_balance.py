#!/usr/bin/env python3
"""Exact 359-edge stationary tests for the 31D isospectral balance family."""
from fractions import Fraction as F
import json
import numpy as np
from check_book03_balanced_scene import (
    A, B, C, sector, i, j, actual_scene, closed_price
)

n = [A, B, C]
w0 = {(0, 1): F(13), (0, 2): F(11), (1, 2): F(9)}
d0 = [F(286), F(234), F(198)]
assert all(n[a] * d0[a] == 2574 for a in range(3))


def make_factors(seed):
    s = [F(1)] * 33
    starts = [0, A, A+B]
    for a in range(3):
        off = starts[a]
        d = F((seed+a) % 3 + 1, 8)
        s[off] += d
        s[off+1] -= d
        assert sum(s[off:off+n[a]]) == n[a]
        assert min(s[off:off+n[a]]) > 0
    return s


def test(s):
    weights = []
    max_cancel = F(0)
    for ii, jj in zip(i, j):
        ii, jj = int(ii), int(jj)
        a,b = int(sector[ii]), int(sector[jj])
        assert a < b
        weights.append(float(w0[a,b] * s[ii] * s[jj]))
        di, dj = s[ii]*d0[a],s[jj]*d0[b]
        # M_{ji}=c*s_i/n_a, M_{ij}=c*s_j/n_b;
        # (T M)_{ii}=c*s_i/n_a, (T M)_{jj}=c*s_j/n_b.
        c=F(1)
        grad=(c*s[ii]/n[a])/di + (c*s[jj]/n[b])/dj
        grad-= (c*s[ii]/n[a])/di + (c*s[jj]/n[b])/dj
        max_cancel=max(max_cancel,abs(grad))
    assert max_cancel == 0
    cost, eigen, grad = actual_scene(np.array(weights), True)
    reference = closed_price(F(1,4))
    assert abs(cost-reference)<2e-12
    target = np.array([-0.5, -0.5]+[0.]*30+[1.])
    assert np.max(np.abs(eigen-target)) < 3e-12
    assert np.max(np.abs(grad))<5e-13
    return {'complete_scene_price':cost,'full359_grad_max':float(np.max(abs(grad))),
            'full359_exact_formula_cancellation':str(max_cancel)}


def main():
    out={'status':'PASS','independent_vertex_parameters':30,
         'common_scale_parameter':1,'stationary_manifold_dimension':31,
         'Hessian_kernel_lower_bound_at_least':31,
         'edge_count':len(i),
         'trials':[test(make_factors(k)) for k in [0,1,2]],
         'scope':'exact full359 source cancellation on weighted scene manifold; no proof of global 359-edge price minimum; binary passport not admitted'}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
