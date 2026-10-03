#!/usr/bin/env python3
"""Read-only exact ingredients for the fixed cosine source obstruction.

The field-derivation theorem is a mathematical proof, not a numerical
certificate. This script independently checks its D0-specific assumptions:
Gram lift/homogeneity, curvature normalization, cyclotomic sample trace,
and controls that rule out overclaiming algebraicity of every link/readout.
"""
from __future__ import annotations
from fractions import Fraction as F
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp

N=None


def einstein_source():
    f, p, q = sp.symbols('f p q', real=True)
    g = sp.diag(1, -1, -f*f, -f*f)
    gi = g.inv()

    def d(expr, role):
        return sp.diff(expr, f)*p + sp.diff(expr, p)*q if role == 1 else 0

    gamma = np.full((4,4,4), sp.S.Zero, dtype=object)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                gamma[a,b,c] = sp.simplify(sum(gi[a,k]*(
                    d(g[k,c], b)+d(g[k,b], c)-d(g[b,c], k)
                    )/2 for k in range(4)))
    ric = sp.zeros(4)
    for a in range(4):
        for b in range(4):
            ric[a,b] = sp.simplify(sum(
                d(gamma[c,a,b],c)-d(gamma[c,a,c],b)
                +sum(gamma[c,c,k]*gamma[k,a,b]-gamma[c,b,k]*gamma[k,a,c]
                     for k in range(4))
                for c in range(4)))
    scalar = sp.simplify(sp.trace(gi*ric))
    assert sp.simplify(scalar-(4*q/f+2*p*p/(f*f))) == 0
    ein = sp.simplify(ric-scalar*g/2)
    tau_matrix = sp.simplify(f*f*gi*ein*gi/2)
    tau = [sp.simplify((1 if a == b else 2)*tau_matrix[a,b])
           for a,b in N.SYM]
    assert tau == [-f*q-p*p/2,0,0,0,p*p/2,0,0,q/(2*f),0,q/(2*f)]
    trace = sp.expand(sum(g[a,b]*t for (a,b),t in zip(N.SYM,tau)))
    assert trace == -2*f*q-p*p
    # Retain the owner normal point independently of the global trace.
    normal = [sp.simplify(t.subs({f:1,p:0})) for t in tau]
    assert normal == [-q,0,0,0,0,0,0,q/2,0,q/2]
    print('PASS_INDEPENDENT_CHRISTOFFEL_DENSITY_AND_RAISED_GRAM_SOURCE')
    return {'Q':'diag(1,-1,-f^2,-f^2)',
            'R_standard':str(scalar),'tau_raw':list(map(str,tau)),
            'trace':str(trace),
            'source_convention':'density f^2 times one-half raised standard Einstein tensor, packed as the ten Gram covector slots; this is the owner reconstructed -G/2 convention'}


def literal_homogeneity():
    eta = np.diag(N.SIG).astype(object)
    def check_frame(solder):
        q=solder.T@eta@solder
        qi=np.array(sp.Matrix(q).inv()).astype(object)
        lifts=[]
        for r,s in N.SYM:
            dq=np.zeros((4,4),dtype=object);dq[r,s]=dq[s,r]=1
            lift=solder@qi@dq*F(1,2)
            assert all(sp.expand(v)==0 for v in
                       (lift.T@eta@solder+solder.T@eta@lift-dq).flat)
            lifts.append(lift)
        action=[];readout=[[] for _ in range(10)]
        for r,s in N.PAIRS:
            u,v=[j for j in range(4) if j not in (r,s)]
            weight=N.orient(r,s)*N.weight(N.wedge(solder[:,u],solder[:,v]))
            dw=[N.orient(r,s)*N.weight(N.wedge(ds[:,u],solder[:,v])+
                                      N.wedge(solder[:,u],ds[:,v]))
                for ds in lifts]
            radial=sum((q[a,b]*row for (a,b),row in zip(N.SYM,dw)),
                        np.zeros((4,4),dtype=object))
            assert all(sp.simplify(x)==0 for x in (radial-weight).flat)
            # Both W and dW are odd under eta-adjoint. Therefore their
            # pairing sees exactly (P-eta*P.T*eta)/2 at every real link P.
            for row in [weight]+dw:
                assert all(sp.simplify(x)==0 for x in (row+eta@row.T@eta).flat)
            action.extend([sp.simplify(np.sum(weight*gen)) for gen in N.G])
            for k,row in enumerate(dw):
                readout[k].extend([sp.simplify(np.sum(row*gen)) for gen in N.G])
        return q,np.array(action,dtype=object),np.array(readout,dtype=object)
    f=sp.Symbol('f',positive=True)
    check_frame(np.diag([1,1,f,f]).astype(object))
    # A general solder control activates off-diagonal Q slots.
    general = np.array([[F(1),F(1,7),0,0],[0,1,F(1,5),0],
                        [F(1,11),0,1,F(1,3)],[0,0,0,1]],dtype=object)
    q,action,readout=check_frame(general)
    qslots = np.array([q[a,b] for a,b in N.SYM],dtype=object)
    assert np.array_equal(qslots@readout,action)
    wrong = qslots.copy()
    for i,(a,b) in enumerate(N.SYM):
        if a != b: wrong[i] *= 2
    assert not np.array_equal(wrong@readout,action)
    print('PASS_LITERAL_ALL_FACE_GRAM_HOMOGENEITY_AND_OFFDIAGONAL_CONTROL')
    return {'symbolic_warp_face_matrix_entries_checked':96,
            'odd_curvature_pairing':'all face weights and all ten Gram derivatives are odd under eta-adjoint; pairings depend exactly on the owned odd plaquette curvature',
            'all_coframes_proof':'each wedge weight is homogeneous degree two in S; Gram radial lift delta Q=Q gives delta S=S/2',
            'exact_identity':'A_h(S,K)=sum_x Q_x:pack Xi_x before imposing E_K',
            'hostile_offdiagonal_reweighting':'fails at general rational solder'}


def cyclotomic_trace():
    eps,c,c2 = sp.symbols('epsilon cos_theta cos_2theta')
    # f=1+epsilon(1-c), p=2*pi*epsilon*sin(theta), q=4*pi^2*epsilon*c.
    coefficient = sp.expand(-8*eps*(1+eps-eps*c)*c-4*eps*eps*(1-c*c))
    harmonic = sp.expand(coefficient.subs(c*c,(1+c2)/2))
    assert sp.expand(harmonic-(2*eps*eps-8*eps*(1+eps)*c+6*eps*eps*c2)) == 0
    e = F(1,50)
    z = sp.Symbol('z')
    checks = []
    for L in (3,4,8,12,16,20,28,64):
        polynomial = sp.S.Zero
        for x in range(L):
            cvalue = (z**(x%L)+z**((-x)%L))/2
            c2value = (z**((2*x)%L)+z**((-2*x)%L))/2
            polynomial += 2*e*e-8*e*(1+e)*cvalue+6*e*e*c2value
        remainder = sp.rem(sp.Poly(sp.expand(polynomial),z),
                           sp.Poly(sp.cyclotomic_poly(L,z),z)).as_expr()
        assert remainder == F(L,1250)
        checks.append({'L':L,'sum_trace_over_pi_squared':str(remainder)})
    # These identities supply the proof for every L>=3: both geometric
    # sums vanish since z^L=1 while z!=1 and z^2!=1. Finite checks do not
    # replace that all-L argument.
    assert sp.expand((z-1)*sum(z**i for i in range(7))) == z**7-1
    assert sp.expand((z*z-1)*sum(z**(2*i) for i in range(7))) == z**14-1
    assert harmonic.subs(eps,0) == 0
    print('PASS_CYCLOTOMIC_TRACE_REDUCTIONS_AND_ALL_L_GEOMETRIC_SUM_IDENTITY')
    return {'harmonic_trace_over_pi_squared':str(harmonic),
            'general_amplitude_constant':'2*epsilon^2, nonzero for every nonzero rational epsilon',
            'all_L_proof':'L>=3, z primitive L-th root: sum z^x=sum z^(2x)=0 by geometric series; conjugate sums also vanish',
            'one_line_sum':'pi^2*L/1250',
            'full_torus_sum':'pi^2*L^4/1250',
            'exact_joint_action_required':'pi^2*L^2/1250',
            'checks':checks,
            'constant_warp_control':'epsilon=0 yields zero; the transcendental-action obstruction disappears',
            'algebraic_frequency_control':'replace the pi^2 factor in this proposed source by any real algebraic lambda: the required action becomes algebraic; this arithmetic proof no longer excludes it, and does not thereby prove existence'}


def tangent_and_stationarity_controls():
    t = sp.Symbol('t',real=True)
    eta = sp.diag(*N.SIG)
    eye = sp.eye(4)
    b = sp.Matrix(N.G[0]+N.G[1]+N.G[2])
    j = sp.Matrix(N.G[3]-N.G[4])
    def cayley(generator, amplitude):
        return (eye-amplitude*generator/2).inv()*(eye+amplitude*generator/2)
    u = sp.simplify(cayley(b,t)*cayley(j,t*t))
    ui = eta*u.T*eta
    assert sp.simplify(ui*u) == eye
    x = sp.simplify(ui*u.diff(t))
    assert sp.simplify(x.T*eta+eta*x) == sp.zeros(4)
    reconstructed = sum((sp.Matrix(N.G[a])*x[r,s]
                         for a,(r,s) in enumerate(N.PAIRS)),sp.zeros(4))
    assert sp.simplify(x-reconstructed) == sp.zeros(4)
    assert sp.simplify(u*x-u.diff(t)) == sp.zeros(4)
    # Exact full-EK roots can have nonalgebraic readout entries. The
    # critical-action lemma constrains the action, not every Xi component.
    # One full denominator-cleared literal polynomial check, not a
    # parameter sample or a numerical stationary residual.
    links=np.array([[N.jconst(4*N.I,8) for _ in range(4)] for _ in range(4)])
    links[:,:,2]=-3*N.I
    b_array=N.G[0]+N.G[1]+N.G[2]
    links[0,0,1]=4*b_array;links[2,0,1]=-4*b_array
    links[0,0,2]=links[2,0,2]=2*b_array@b_array-3*N.I
    ek,eq=N.euler_links(links)
    assert not np.any(ek)
    expected=np.zeros_like(eq)
    visible = np.array([0,0,0,0,-1,1,1,-1,1,-1],dtype=object)
    for power,value in ((1,256),(3,-576),(5,432),(7,-108)):
        for phase,sign in enumerate((1,1,-1,-1)):
            expected[power,phase]=sign*value*visible
    assert np.array_equal(eq,expected)
    data={'D':'4-3*t^2','full_EK_numerator':'zero coefficientwise',
          'metric_numerator':'4*t*D^3*sigma_p*(0,0,0,0,-1,1,1,-1,1,-1)',
          'scalar_nonzero_coefficients':[[1,256],[3,-576],[5,432],[7,-108]]}
    visible = np.array([0,0,0,0,-1,1,1,-1,1,-1],dtype=object)
    qslots = np.array([N.SIG[a] if a == b else 0 for a,b in N.SYM],dtype=object)
    assert np.any(visible) and qslots@visible == 3
    assert sum(sign*(qslots@visible) for sign in (1,1,-1,-1)) == 0
    print('PASS_LORENTZ_DERIVATION_TANGENT_AND_RESPONSE_VISIBLE_GLOBAL_TRACE_NULL_CONTROL')
    return {'symbolic_rational_noncommuting_Cayley_tangent':'U^-1*dU/dt is exactly in the span of all six physical generators',
            'stationary_polynomial_control':data,
            'boost_trace_control':'sitewise traces are nonzero, but the full stationary action/trace is exactly zero after the four-phase sum',
            'nonclaim':'the lemma does not imply algebraic link entries or individual metric response slots',
            'EK_only_warp_control':'owned exact designated normal rescue remains possible: its output source is h-dependent and its stationary action is algebraic, while approximating the continuum action asymptotically; exact joint equality to the preset pi^2 trace is excluded'}


def main():
    global N
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--write-json',type=Path)
    parser.add_argument('--expect',type=Path,default=Path(__file__).with_name('a4d_fixed_source_algebraic_stationarity_results.json'))
    args=parser.parse_args()
    sys.path.insert(0,str(args.certificate_dir.resolve()))
    N=importlib.import_module('a4d_identity_quarter_nonlinear_response_check')
    pins={name:hashlib.sha1((args.certificate_dir/name).read_bytes()).hexdigest()
          for name in ('a4d_identity_quarter_nonlinear_response_check.py',
                       'a4d_designated_full_gap_check.py')}
    report = {'schema':'a4d-fixed-cosine-critical-value-source-probe-v1',
              'certificate_inputs':pins,
              'analytic_proof_owner':'02_REGISTRY/research/A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md',
              'status':'ALL_EXACT_INGREDIENT_CHECKS_PASS; FIELD_DERIVATION_THEOREM_PROVED_SEPARATELY',
              'einstein':einstein_source(),
              'homogeneity':literal_homogeneity(),
              'sampling':cyclotomic_trace(),
              'controls':tangent_and_stationarity_controls(),
              'conclusion':'No real full-link solution of E_K=0 and Xi=h^2*tau_raw exists on any L>=3 cosine-warp grid for the predeclared owner continuum source; no chart, amplitude, regularity, or normal-graph assumptions',
              'scope':'fixed-source feasibility obstruction on one smooth nonconstant background, not a response-decoupling NO-GO or a general source-image closure'}
    if args.write_json is None:
        assert report == json.loads(args.expect.read_text()),'pinned replay mismatch'
    if args.write_json:
        args.write_json.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS_FIXED_COSINE_CRITICAL_ACTION_SOURCE_INGREDIENTS')

if __name__ == '__main__':
    main()
