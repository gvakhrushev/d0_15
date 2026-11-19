"""Common thermal cut, two real selector arms, type switches and absolute feedback."""
from math import comb, cos, exp, log, sin, sqrt

import numpy as np

from check_modal_field import PHI, P, padding


def arms(q, n, chi, chi_slope):
    # A two-dimensional positive cut; the actual clock estimates are replayed upstream.
    s, eps = .52, .03
    K = s*np.eye(2) + eps*np.array([[cos(q),sin(q)],[sin(q),-cos(q)]])
    dK = eps*np.array([[-sin(q),cos(q)],[cos(q),sin(q)]])
    records = [[], []]
    for f, flag in enumerate([P,P**2]):
        for k in range(n+1):
            l = padding(2**n, comb(n,k))+f*k
            proba = q**k*(1-q)**(n-k)*P**l*flag
            # Same conditional state for the retained Gold branch and every permutation of the type.
            angle = q*(k+1)/n + f
            psi = np.array([cos(angle),sin(angle)])
            dpsi = (k+1)/n*np.array([-sin(angle),cos(angle)])
            kb = psi@K@psi
            dkb = 2*dpsi@K@psi + psi@dK@psi
            assert abs(kb-s) <= eps+1e-13
            state_bound = 2*(k+1)/n
            assert abs(dkb/kb) <= (eps+eps*state_bound)/(s-eps)+1e-12
            # Other Gold tails have smaller probability, with the same thermal factor here.
            value = exp(chi)*proba*kb
            slope = chi_slope+k/q-(n-k)/(1-q)+dkb/kb
            records[f].append((value,k,slope))
    return [max(row) for row in records]


def check(q,n):
    (v0,k0,d0),(v1,k1,d1) = arms(q,n,2*q,2.)
    other0, other1 = arms(q,n,-3*q,-3.)
    assert abs(other1[0]/other0[0]-v1/v0) < 2e-12
    assert abs(d0 - other0[2] - 5) < 2e-12 and abs(d1-other1[2]-5) < 2e-12
    Z = 1-(1-P)*q
    exact = -log(Z)/log(PHI)
    approx = -log((v1/P**2)/(v0/P))/(n*log(PHI))
    kappa = (.52+.03)/(.52-.03)
    assert abs(approx-exact) <= log(kappa*(n+1)/P)/(n*log(PHI))
    slope = -(d1-d0)/(n*log(PHI))
    target = (1-P)/(Z*log(PHI))
    V = max(1/q,1/(1-q))
    bound = 2*V*sqrt(2*log(kappa*(n+1)/P)/n)/log(PHI)
    bound += 2*(.03+.03*(2+2/n))/(n*(.52-.03)*log(PHI))
    assert abs(slope-target) <= bound
    for k,pi in [(k0,q),(k1,q*P/Z)]:
        assert comb(n,k)*pi**k*(1-pi)**(n-k) >= P/(kappa*(n+1)) - 1e-12
    h = 1e-7
    def objective(x):
        a,b = arms(x,n,2*x,2.)
        return -log((b[0]/P**2)/(a[0]/P))/(n*log(PHI))
    approx_slope = (objective(q+h)-objective(q-h))/(2*h)
    assert abs(approx_slope-slope) < 1e-7


if __name__ == "__main__":
    for p0 in [.231, .286, .343, .376]:
        for trials in [2, 7, 32, 128]:
            check(p0,trials)
    print("PASS 16 complete type comparisons on one cut, moving thermal states and common feedback")
