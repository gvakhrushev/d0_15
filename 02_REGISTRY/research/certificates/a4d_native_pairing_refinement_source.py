#!/usr/bin/env python3
"""Exact weighted-pairing and refinement kernels.

Finite witnesses support the companion analytic proof. No pairing, heat,
native source, stationary equation or continuum realization is selected.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path
import sys
import sympy as s

spec = importlib.util.spec_from_file_location('pairing_joint_input',
    Path(__file__).with_name('a4d_native_joint_adjoint_source.py'))
J = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = J
spec.loader.exec_module(J)
ETA, SLOTS = J.ETA, J.SLOTS


def weighted_edge(A, nx, ny, vx, vy, mux, muy):
    data = J.edge(A, nx, ny, vx, vy)
    data['weighted_adjoint'] = mux/muy*data['adjoint']
    data['weighted_defect'] = data['stored']-data['weighted_adjoint']
    return data


@lru_cache(None)
def tangent_system(flags, native_volume=False):
    count = 43 if native_volume else 44
    variables = s.symbols('x:'+str(count))
    E = s.Matrix(4, 4, variables[:16])
    u = s.Matrix([0, *variables[16:19]])
    w = s.trace(ETA*E) if native_volume else variables[43]
    equations = []
    for r, difference in enumerate(flags):
        B = J.lorentz_jet(variables[19+6*r:25+6*r])
        equations.extend(B[:, 0]-difference*u)
        equations.extend(B[:, r]-difference*(ETA*E.row(r).T+w*s.eye(4)[:, r]))
    constraints = s.Matrix(equations).jacobian(variables)
    metric = s.Matrix([E[i,j]+E[j,i] for i,j in SLOTS]).jacobian(variables)
    return constraints, metric


def metric_rescale(H):
    return H+s.trace(ETA*H)*ETA


def metric_rescale_inverse(H):
    return H-s.trace(ETA*H)*ETA/5


def cycle_difference(L):
    """(df)_i=f_(i+1)-f_i, including the periodic final edge."""
    return s.Matrix(L, L, lambda i,j: int(j==(i+1)%L)-int(i==j))


def refinement_maps(L, c=1):
    if L < 2:
        raise ValueError('The packet uses cycles of length at least two.')
    B0 = s.eye(L).col_join(s.eye(L)[0,:])
    B1 = s.eye(L).col_join(s.zeros(1,L))
    return B0, c*B1


def rectangular_adjoint(A, Gdomain, Gcodomain):
    return Gdomain.inv()*A.conjugate().T*Gcodomain


def complex_data(L, coarse_scale=1, fine_scale=1,
                 Gc0=None, Gc1=None, Gf0=None, Gf1=None):
    c = s.sympify(fine_scale)/coarse_scale
    P0, P1 = refinement_maps(L,c)
    Gc0 = s.eye(L) if Gc0 is None else Gc0
    Gc1 = s.eye(L) if Gc1 is None else Gc1
    Gf0 = s.eye(L+1) if Gf0 is None else Gf0
    Gf1 = s.eye(L+1) if Gf1 is None else Gf1
    dc, df = coarse_scale*cycle_difference(L), fine_scale*cycle_difference(L+1)
    ac = rectangular_adjoint(dc,Gc0,Gc1)
    af = rectangular_adjoint(df,Gf0,Gf1)
    Dc = s.BlockMatrix([[s.zeros(L),ac],[dc,s.zeros(L)]]).as_explicit()
    Df = s.BlockMatrix([[s.zeros(L+1),af],[df,s.zeros(L+1)]]).as_explicit()
    return dict(L=L,c=c,P0=P0,P1=P1,dc=dc,df=df,ac=ac,af=af,
                Dc=Dc,Df=Df,P=s.diag(P0,P1),Gc=s.diag(Gc0,Gc1),
                Gf=s.diag(Gf0,Gf1),Gc0=Gc0,Gc1=Gc1,Gf0=Gf0,Gf1=Gf1)


def nonlocal_repair(L, gamma, coarse_scale=1, fine_scale=1):
    c = s.sympify(fine_scale)/coarse_scale
    B0,_ = refinement_maps(L)
    v = (s.eye(L)[:,0]+s.eye(L)[:,L-1])/2
    Gf1 = s.BlockMatrix([[s.eye(L),v],[v.T,s.Matrix([[gamma]])]]).as_explicit()
    return complex_data(L,coarse_scale,fine_scale,B0.T*B0,c*c*s.eye(L),s.eye(L+1),Gf1)


def full16_line_refinement(L, role, coarse_scale=1, fine_scale=1):
    """One tensor direction, retaining every actual ACDB exterior component."""
    C = J.P.creator(role)
    N = C*C.T
    P0,P1 = refinement_maps(L,s.sympify(fine_scale)/coarse_scale)
    dc,df = coarse_scale*cycle_difference(L),fine_scale*cycle_difference(L+1)
    Dc = s.kronecker_product(dc,C)+s.kronecker_product(dc.T,C.T)
    Df = s.kronecker_product(df,C)+s.kronecker_product(df.T,C.T)
    refinement = s.kronecker_product(P0,s.eye(16)-N)+s.kronecker_product(P1,N)
    return Dc,Df,refinement


def tensor_sector_map(L, mask, c=1):
    B0,B1 = refinement_maps(L,c)
    return s.kronecker_product(*[B1 if mask & (1<<r) else B0 for r in range(4)])


def leak_data(D, G, P):
    Q = s.eye(D.rows)-P
    return {'Q':Q,'A':P*D*P,'R':Q*D*P,
            'compressed_square':P*D*D*P,
            'leak_square':J.dagger(Q*D*P,G)*(Q*D*P)}


def moving_leak_jet(D, P, dotD, dotP):
    Q = s.eye(D.rows)-P
    return -dotP*D*P+Q*dotD*P+Q*D*dotP


if __name__ == '__main__':
    for volume in (False,True):
        A,H = tangent_system((1,1,1,1),volume)
        print('Generic metric rank, native_volume=%s:'%volume,
              A.col_join(H).rank()-A.rank())
    print('Pairing/refinement/source admission and original #310 terminal: OPEN')
