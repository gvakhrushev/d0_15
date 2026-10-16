#!/usr/bin/env python3
"""Exact finite inputs for the ALL-UV stationary-action/secant theorem.

Research finite control. Imports the unchanged literal A4D face/Euler
owners; does not mutate inputs. The analytic uniform theorem is in
A4D_NATIVE_FINITE_PROBE_COMPLETION.md. Finite checks are not presented as a certificate of that analysis.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import hashlib
from pathlib import Path
import sys

import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path,
                        default=Path(__file__).resolve().parents[3])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo / '02_REGISTRY/research/certificates'))
    import a4d_identity_quarter_nonlinear_response_check as N
    import a4d_stationary_response_memory_check as M

    t = sp.symbols('t', real=True)
    delta, r0, r1 = sp.symbols('delta r0 r1', real=True)
    a = ((r0+r1-2*delta)*t**3
         +(3*delta-2*r0-r1)*t**2+r0*t)
    assert sp.diff(a,t).subs(t,0) == r0
    assert sp.expand(sp.diff(a,t).subs(t,1)-r1) == 0
    integral = sp.integrate(t*(1-t)*sp.diff(a,t,3),(t,0,1))
    assert sp.expand((r0+r1)/2-integral/2-delta) == 0
    saturated = 3*t**2-2*t**3
    assert sp.diff(saturated,t).subs(t,0) == 0
    assert sp.diff(saturated,t).subs(t,1) == 0
    assert -sp.integrate(t*(1-t)*sp.diff(saturated,t,3),(t,0,1))/2 == 1
    assert sp.integrate(t*(1-t),(t,0,1)) == F(1,6)
    assert sp.integrate(t*(1-t)*sp.diff(saturated,t,3),(t,0,1))/2 != 1
    print('PASS_ENDPOINT_IDENTITY_RESIDUALS_SIGN_HALF_AND_ONE_TWELFTH', flush=True)

    h, amp, weight, rho0, rho1 = sp.symbols('h M B R0 R1', positive=True)
    # Four physical roles times six generator coordinates, on all L^4 sites.
    raw_l1 = 24*amp*h**-3
    c3 = 6912*weight
    action_error = sp.expand(h**2*c3/12*(amp*h)**2*raw_l1)
    residual_error = sp.expand(h**2*(rho0+rho1)*raw_l1/2)
    assert action_error == 13824*weight*amp**3*h
    assert sp.expand(residual_error-12*amp*(rho0+rho1)/h) == 0
    assert F(6912)*F(676,625) < 8192
    assert F(13824)*F(676,625) < 16384
    # This finite incidence is exact on each periodic physical lattice.
    for L in (4,8,12):
        links = {(x,r): 0 for x in np.ndindex((L,)*4) for r in range(4)}
        for x in np.ndindex((L,)*4):
            for r,s in N.PAIRS:
                xr=list(x);xr[r]=(xr[r]+1)%L
                xs=list(x);xs[s]=(xs[s]+1)%L
                for edge in ((x,r),(tuple(xr),s),(tuple(xs),r),(x,s)):
                    links[edge] += 1
        assert len(links) == 4*L**4
        assert set(links.values()) == {6}
    print('PASS_FULL_PHYSICAL_INCIDENCE_AND_NORMALIZATION_CONSTANTS', flush=True)

    eps, c, m3 = sp.symbols('eps C M3', positive=True)
    v0 = m3*t**3/6
    secant = (v0.subs(t,eps)+c*h-v0.subs(t,-eps)+c*h)/(2*eps)
    assert sp.expand(secant-c*h/eps-m3*eps**2/6) == 0
    d = sp.symbols('d', positive=True)
    assert sp.simplify(secant.subs({h:d**3,eps:d})-(c+m3/6)*d**2) == 0
    print('PASS_CENTERED_SECANT_BOUND_AND_H_TWO_THIRDS_SCALE', flush=True)

    y, probe = sp.symbols('y probe', real=True)
    f = 1+(1-sp.cos(2*sp.pi*y))/50
    psi = (1-sp.cos(2*sp.pi*y))/50
    canonical = sp.integrate(sp.diff(f+probe*psi,y)**2,(y,0,1))
    assert sp.expand(canonical-sp.pi**2*(1+probe)**2/1250) == 0
    difference = (canonical.subs(probe,eps)-canonical.subs(probe,-eps))/(2*eps)
    assert sp.simplify(difference-sp.pi**2/625) == 0
    integration_by_parts = -2*sp.integrate(sp.diff(f,y,2)*psi,(y,0,1))
    assert sp.simplify(difference-integration_by_parts) == 0
    assert sp.diff(canonical,probe,3) == 0
    fixed_epsilon=F(1,2)
    b=F(53,50)
    assert 1+F(3,2)*F(1,25) == b
    assert b*b < F(5,2)
    assert 20-8*b*b == F(6882,625)
    fixed_difference=canonical.subs(probe,fixed_epsilon)-canonical.subs(probe,-fixed_epsilon)
    assert sp.simplify(fixed_difference-sp.pi**2/625) == 0
    assert F(6912)*b*b < 8192
    print('PASS_LITERAL_WARP_QUADRATIC_ACTION_AND_FIXED_WIDTH_SECANT', flush=True)

    # Narrow check of the suggested extension of the owned zero-phase
    # coframe congruence: use its exact symbol constructor, not a new census.
    symbol_source=(args.repo/'02_REGISTRY/research/certificates/a4d_j2_fixed_realization_ir_check.py').read_text()
    namespace={}
    exec(symbol_source.split('check("LORENTZ_GENERATORS"')[0],namespace)
    symbol=namespace['connection_symbol']
    s=sp.symbols('s',positive=True)
    coframe=sp.diag(1,1,s,s)
    change=sp.kronecker_product(coframe.T,sp.eye(6))
    phase=[sp.Integer(1),sp.I,sp.Integer(1),sp.Integer(1)]
    defect=(change.T*symbol(coframe,phase)*change
            -coframe.det()*symbol(sp.eye(4),phase)).applyfunc(sp.factor)
    assert defect[12,13] == -sp.I*s**2*(s-1)
    assert sum(entry != 0 for entry in defect) == 8
    print('PASS_ALL_PHASE_COFRAME_CONGRUENCE_SHORTCUT_FAILURE', flush=True)

    # Complete denominator-cleared Euler polynomial for the actual #232 Y
    # family. Every term has four link factors, so degree eight is complete.
    Y = N.G[3]-N.G[4]+N.G[5]
    assert np.array_equal(Y@Y@Y,-3*Y)
    links = np.array([[N.jconst(4*N.I,8) for _ in range(4)] for _ in range(4)])
    links[:,:,2] = 3*N.I
    links[0,0,1] = 4*Y
    links[2,0,1] = -4*Y
    links[0,0,2] = links[2,0,2] = 2*Y@Y+3*N.I
    ek, eq = N.euler_links(links)
    assert not np.any(ek)
    assert not np.any(eq)
    boost_polynomial = M.full_boost_polynomial()
    print('PASS_ACTUAL_232_Y_AND_227_B_ALL_DEGREE_EULER_CONTROLS', flush=True)

    visible = np.array([0,0,0,0,-1,1,1,-1,1,-1], dtype=object)
    sigma = (1,1,-1,-1)
    qslots = np.array([F(N.SIG[i]) if i==j else F(0) for i,j in N.SYM], dtype=object)
    assert qslots@visible == 3
    _,_,_,_,_,face_weights,_ = M.face_data(N.I)
    family_ledger=[]
    for label, generator in (('232_Y_null',Y),('227_B_visible',N.G[0]+N.G[1]+N.G[2])):
        for value in (F(-1,7),F(1,5),F(1,4)):
            field=M.rational_family(generator,value)
            full_ek, full_eq=N.euler_links(field[:,:,None])
            assert not np.any(full_ek)
            local_actions=[]
            for p in range(4):
                curvature=[(plaq-N.jinv(plaq[None])[0])*F(1,2)
                           for plaq in M.plaquettes(field,p)]
                assert np.any(curvature)
                action=sum(np.sum(w*curv) for w,curv in zip(face_weights,curvature))
                assert action == qslots@full_eq[0,p]
                local_actions.append(action)
            assert sum(local_actions) == 0
            if label=='232_Y_null':
                assert not np.any(full_eq)
                assert local_actions == [0]*4
            else:
                factor=4*value/(4-3*value**2)
                assert np.array_equal(full_eq[0],np.array([s*factor*visible for s in sigma]))
                assert local_actions == [3*s*factor for s in sigma]
            family_ledger.append({'family':label,'t':str(value),
                                  'cell_action':list(map(str,local_actions)),
                                  'total_action':'0','curvature':'nonzero',
                                  'metric_response':'zero' if label=='232_Y_null' else 'nonzero'})
    for L in (4,8,12,16):
        hh=F(1,L); value=hh**2; factor=4*value/(4-3*value**2)
        assert 6*L**4*abs(factor)/hh**2 == 24*L**4/(4-3*hh**4)
        for x1 in range(L):
            transverse_sum=sum(sigma[(x0+x1+x2+x3)%4]
                               for x0,x2,x3 in np.ndindex((L,)*3))
            assert transverse_sum == 0
    print('PASS_NULL_VERSUS_VISIBLE_MEMORY_AND_EXACT_ONE_COORDINATE_CANCELLATION', flush=True)

    # A hostile inference model, NOT the A4D action. Even polynomial critical
    # values with the same bounded third log derivative need not converge in C1.
    # |T_m(q)|<=1 on [-1,1] follows from T_m(cos theta)=cos(m theta).
    a_scalar=sp.symbols('a',real=True)
    hostile=[]
    for L in (4,8,12):
        hh=sp.Rational(1,L); degree=L**2+1
        cheb=sp.chebyshevt(degree,t)
        local=cheb*(3*hh*a_scalar**2-2*a_scalar**3)
        assert sp.diff(local,a_scalar).subs(a_scalar,0) == 0
        assert sp.diff(local,a_scalar).subs(a_scalar,hh) == 0
        assert sp.expand(sp.diff(local,a_scalar,3)+12*cheb) == 0
        canonical_value=hh**-2*local.subs(a_scalar,0)
        competing=sp.expand(hh**-2*local.subs(a_scalar,hh))
        assert canonical_value == 0
        assert sp.expand(competing-hh*cheb) == 0
        derivative=sp.diff(competing,t).subs(t,0)
        assert derivative == L+hh
        hostile.append({'L':L,'degree':degree,'uniform_value_gap_bound':str(hh),
                        'infinitesimal_response_at_zero':str(derivative)})
    print('PASS_POLYNOMIAL_SMALL_CRITICAL_VALUES_LARGE_DERIVATIVES_HOSTILE_MODEL', flush=True)

    report={
        'input_head':'aed0db1782184e8318cf9b150e5134be6800b177',
        'input_sha256':{name:hashlib.sha256((args.repo/'02_REGISTRY/research/certificates'/name).read_bytes()).hexdigest() for name in ('a4d_identity_quarter_nonlinear_response_check.py','a4d_stationary_response_memory_check.py','a4d_j2_fixed_realization_ir_check.py')},
        'finite_probe_memo_audit_head':'f317a3b842b2d10c5a3a381b6b03cb9850e77f66',
        'verdict':'ALL_UV_STATIONARY_ACTION_AND_FINITE_SECANT_INPUTS_PASS',
        'proof':'A4D_NATIVE_FINITE_PROBE_COMPLETION.md; analytic theorem, finite checks only its exact inputs and hostile controls',
        'action_bound':'12*M*(R0+R1)/h + 13824*B*M^3*h',
        'fixed_warp_action_constant':'16384*M^3*h is a convenient strict upper bound',
        'secant_bound':'C*h/epsilon + M3*epsilon^2/6',
        'canonical_warp_action':'integral (f_prime)^2',
        'canonical_warp_secant':'2 integral f_prime*psi_prime = -2 integral f_second*psi',
        'fixed_width_exact_warp_probe':{
            'psi':'f-1','epsilon':'1/2','f_range':'[1,53/50]',
            'b_squared_less_than_5_over_2':True,'uniform_frozen_gap':'6882/625',
            'finite_reading':'I_h(f_plus,K_plus)-I_h(f_minus,K_minus)',
            'continuum_reading':'pi^2/625','rate':'O(h), arbitrary independent exact small-log endpoints',
            'metric_path':'nonlinear Gram path Q(t)=diag(1,-1,-(f+t*psi)^2,-(f+t*psi)^2)'},
        'all_phase_congruence_failure':{
            'solder':'diag(1,1,s,s)','phase':'(1,i,1,1)',
            'defect_entry_12_13':'-i*s^2*(s-1)','nonzero_entries':8,
            'scope':'refutes applying the owned zero-phase congruence at general phase'},
        'actual_controls':family_ledger,
        'boost_complete_polynomial':boost_polynomial,
        'hostile_polynomial_critical_values':hostile,
        'scope':'all physical link roles, generators, and frequencies; endpoint stationarity only',
        'nonclaims':['no original raw owner-norm terminal','no instantaneous Xi convergence',
                     'no full native operator intertwiner','no fixed-source joint existence',
                     'no continuation of an arbitrary central root through metric probes']}
    if args.expect or not args.output:
        expected_path=args.expect or Path(__file__).with_name('a4d_finite_probe_stationary_action_results.json')
        assert report == json.loads(expected_path.read_text()), 'pinned ledger mismatch'
        print('PASS_PINNED_LEDGER',flush=True)
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('VERDICT',report['verdict'])


if __name__=='__main__':
    main()
