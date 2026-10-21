#!/usr/bin/env python3
"""Exact equitable graph and full-359-edge source test of native 33-vertex scene.

Checks original K(9,11,13), normalized random walk, genuine full heat-plus-
feedback master at beta=2/phi**2 and z=2**-20. No assumed native weighted
admission, physical Info, controller, or GR selection.
"""
from fractions import Fraction as F
from math import sqrt, exp, log, cosh
import json
import numpy as np

A, B, C = 9, 11, 13
z = 2.0**-20
p = (sqrt(5)-1)/2
beta = 2*p*p
masses = [9, 11, 13]
sector = np.repeat(np.arange(3), masses)
i, j = np.triu_indices(33, 1)
selector = sector[i] != sector[j]
i, j = i[selector], j[selector]
assert len(i) == 359


def kappa(x, y, u):
    return F(2574)*x*y*u / ((11*u+9*y)*(13*u+9*x)*(11*x+13*y))


def closed_price(k):
    kk = float(k)
    delta = sqrt(max(0., .25-kk))
    Z = 1+30*exp(-beta)+2*exp(-1.5*beta)*cosh(beta*delta)
    Q = (1-z)*(1-2*kk*z)+kk*kk*z*z
    assert Z > 0 and Q > 0
    return log(Z)/beta - 30*log(1-z) - log(Q)


def dprice(k):
    kk = float(k)
    delta = sqrt(max(0., .25-kk))
    Z = 1+30*exp(-beta)+2*exp(-1.5*beta)*cosh(beta*delta)
    thermal = (-beta*exp(-1.5*beta)/Z if delta == 0 else
               -exp(-1.5*beta)*np.sinh(beta*delta)/delta/Z)
    Q = (1-z)*(1-2*kk*z)+kk*kk*z*z
    feedback = 2*z*(1-(1+kk)*z)/Q
    return thermal+feedback


def edge_weights(x, y, u):
    return np.where((sector[i] == 0) & (sector[j] == 1), float(x),
           np.where((sector[i] == 0) & (sector[j] == 2), float(y), float(u)))


def actual_scene(ws, with_source=False):
    mat = np.zeros((33,33))
    mat[i,j] = ws
    mat[j,i] = ws
    d = mat.sum(axis=1)
    T = mat / d[:,None]
    sym = mat/np.sqrt(d[:,None]*d[None,:])
    vals, vecs = np.linalg.eigh(sym)
    F_eig = 1-z*(1-vals**2)
    price = np.logaddexp.reduce(-beta*(1-vals))/beta - np.log(F_eig).sum()
    if not with_source:
        return price, vals
    heat_eig = np.exp(-beta*(1-vals))
    heat_eig /= heat_eig.sum()
    # T=D^-1/2 S D^1/2, and m(T) has the same similarity.
    Mt = (vecs * (heat_eig - 2*z*vals/F_eig)) @ vecs.T
    M = Mt * np.sqrt(d[None,:]/d[:,None])
    TM = T@M
    omega = M[j,i]/d[i]+M[i,j]/d[j]-TM[i,i]/d[i]-TM[j,j]/d[j]
    return price, vals, omega


def run():
    k0 = kappa(F(1),F(1),F(1))
    assert k0 == F(39,160)
    assert kappa(F(13),F(11),F(9)) == F(1,4)
    derivs = {
      'x':k0*(1-F(9,22)-F(11,24)),
      'y':k0*(1-F(9,20)-F(13,24)),
      'u':k0*(1-F(11,20)-F(13,22)),
    }
    assert derivs == {'x':F(91,2816),'y':F(13,6400),'u':F(-1209,35200)}
    assert sum(derivs.values()) == 0
    # AM-GM = κ<=1/4; t,s hyperbolic coords checked at nonsymmetric samples.
    samples = [(F(1),F(1),F(1)),(F(13),F(11),F(9)),
               (F(2),F(7),F(3)),(F(1,2),F(5,3),F(3,4)),
               (F(13,4),F(11,4),F(9,4))]
    max_closed_error = 0.
    max_spectral_error = 0.
    for x,y,u in samples:
        kk = kappa(x,y,u)
        assert 0 < kk <= F(1,4)
        t = log(float(B*x/(C*y)))
        s = log(float(A*y/(B*u)))
        k_hyper = 1/(4*cosh(t/2)*cosh(s/2)*cosh((t+s)/2))
        max_closed_error = max(max_closed_error, abs(float(kk)-k_hyper))
        price,vals = actual_scene(edge_weights(x,y,u))
        max_spectral_error=max(max_spectral_error,abs(price-closed_price(kk)))
        expected=np.array([-0.5-sqrt(float(F(1,4)-kk)),
                            -0.5+sqrt(float(F(1,4)-kk)),1.])
        got=np.concatenate([vals[:2],vals[-1:]])
        assert max(abs(got-expected)) < 2e-12, (x,y,u, got,expected)
        assert max(abs(vals[2:-1])) < 2e-12
    assert max_closed_error<2e-15 and max_spectral_error<2e-12
    # Rigorous global monotonicity bound from the proof, not these samples.
    from fractions import Fraction
    slope_lower = Fraction(7,2640)-Fraction(8,2**20)
    assert slope_lower > 0
    price_gap_lower = slope_lower / 160
    price_gap=closed_price(k0)-closed_price(F(1,4))
    assert price_gap > float(price_gap_lower) > 0
    for q in (F(1,100000),F(1,8),k0,F(1,4)):
        assert dprice(q)<-float(slope_lower)
    price, eigs, grad = actual_scene(edge_weights(13,11,9),True)
    max_gradient=float(max(abs(grad)))
    assert max_gradient<5e-13, max_gradient
    # Hessian at balance in t,s: κ_tt=κ_ss=-1/8, κ_ts=-1/16.
    Hshape = dprice(F(1,4))*np.array([[-1/8,-1/16],[-1/16,-1/8]])
    eigH=np.linalg.eigvalsh(Hshape)
    assert min(eigH)>0
    out={
       'status':'PASS','edge_count':359,'canonical_kappa':str(k0),
       'balanced_kappa':'1/4', 'canonical_partial_derivatives':{k:str(v) for k,v in derivs.items()},
       'unique_balanced_shape':'x:y:u=13:11:9',
       'analytic_global_negative_slope_upper':str(-slope_lower),
       'exact_price_gap_lower':str(price_gap_lower),
       'numerical_price_gap':price_gap,
       'canonical_slope':dprice(k0),
       'balanced_slope':dprice(F(1,4)),
       'max_full359_gradient_at_balance':max_gradient,
       'shape_hessian_eigenvalues':list(map(float,eigH)),
       'max_closed_spectrum_error':max_spectral_error,
       'max_cosh_identity_error':max_closed_error,
       'scope':'all 359 mathematical weighted edge jets; native binary passport does not admit them; no GR closure'
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return out


if __name__=='__main__':run()
