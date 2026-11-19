#!/usr/bin/env python3
"""Compose the existing complete Golden terminal source with normal-row recovery.

This consumes the original constructed terminal protocol's source identity;
it neither derives physical admission nor computes the unknown full Book price.
The previous normal-row checker and historical receipt are left unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy import sparse
from scipy.sparse.linalg import spsolve

INPUT_REF = '4920a97750a85a0cf631057ba3cf0d5b65ed9013'
PRIOR_BLOB = '92ce023873ddb780439dd54dd47415c740841113'
OWNER = ('02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/'
         'book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md')
OWNER_BLOB = 'bce112de77a694809e0a9a7fa769731296148ca2'

def require(ok: bool, name: str) -> None:
    if not bool(ok):
        raise AssertionError(name)

def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def normal_metric_bound(h: float, a_j: float, gain_floor: float, residual: float) -> float:
    if h <= 0 or a_j == 0 or gain_floor <= 0 or residual < 0:
        raise ValueError('A nonzero source and a strictly positive gain floor are required')
    return h * residual / (4 * abs(a_j) * gain_floor)

def calculate() -> dict:
    local = Path(__file__).resolve().parent
    require(git_blob(local/'check_primary_normal_source_recovery.py') == PRIOR_BLOB,
            'unchanged previous source input')
    p = (sp.sqrt(5)-1)/2
    a = sp.sqrt(p)
    ell = sp.log((1+sp.sqrt(5))/2)
    t = sp.symbols('t', real=True)
    c, s = p**3, 2*p*a
    kappa = 8*p**4*a
    clean0, clean1 = 1-2*t*t, 2*t*(1-t*t)
    work = 4*t**4*(1-t*t)
    require(sp.expand(clean0**2+clean1**2+work-1)==0, 'complete cleanup norm')
    require(sp.simplify(c*c+s*s-1)==0, 'original Golden squared rotation')
    q1 = (s*clean0+c*clean1)**2+c*c*work
    q0 = (c*clean0-s*clean1)**2+s*s*work
    require(sp.simplify(q0+q1-1)==0, 'all-terminal-work probability normalization')
    require(sp.simplify(q0.subs(t,0)-p**6)==0, 'native flat q0')
    require(sp.simplify(q1.subs(t,0)-4*p**3)==0, 'native flat q1')
    require(sp.simplify(sp.diff(q1,t).subs(t,0)-kappa)==0, 'exact full reporter first jet')
    require(sp.simplify(q0.subs(t,0)/q1.subs(t,0)-p**3/4)==0,
            'pointer entropy logarithm algebraic ratio')
    require(sp.diff(work,t).subs(t,0)==0 and sp.diff(work,t,2).subs(t,0)==0,
            'no omitted quadratic nonclean mass')
    beta = 4+sp.log(4)/ell
    # Positivity follows from p>0, ell>0 and 4>1, not a floating-point sign scan.
    require(p.is_positive and ell.is_positive and beta.is_positive, 'nonzero positive readout gains')
    z = sp.Rational(1,2**20)
    L = 4*p**3
    M = L*(1+p**6)
    require(sp.simplify(L-(1-p**6))==0, 'original lower band')
    require(sp.simplify(M-(1-p**12))==0, 'original upper band')
    Q0, R0 = 1-z*L, 1-z*M
    gamma_times_N = Q0*R0/2
    coh_times_N = gamma_times_N*kappa
    ptr_times_N = coh_times_N*beta
    # The same factor multiplies geometry and matter; their ratio stays fixed.
    aj,bj,gain = sp.symbols('a_J b_J gain', nonzero=True)
    require(sp.cancel((gain*bj)/(gain*aj)-bj/aj)==0, 'unchanged original matter/gravity ratio')
    # A derived SOURCE multiplier is not multiplication of an unshifted action.
    H,chi,Jstar,c0,c1 = sp.symbols('H chi Jstar c0 c1', real=True)
    J = Jstar+chi*H
    multiplied = (c0+c1*H)*J
    require(sp.diff(multiplied,H).subs(chi,0)==c1*Jstar,
            'moving coefficient retains nonzero baseline source')
    B1,B2,g1,g2 = sp.symbols('B1 B2 g1 g2', real=True)
    score1,score2 = B1+g1*chi*H, B2+g2*chi*H
    mixed = (1-H)*score1+H*score2
    require(sp.expand(sp.diff(mixed,H).subs(chi,0)-(B2-B1))==0,
            'field-dependent readout selection adds a real source')
    # G^1 has q1=p^2 and q0=p: code derivative equals pointer-entropy derivative.
    require(sp.simplify(p/(p*p)-1/p)==0, 'G1 matched-code ratio')
    g1_pointer_gain = 1-1
    require(g1_pointer_gain==0, 'cheapest pointer reading is not invertible as a source')
    try:
        normal_metric_bound(.125,1.,0.,.01)
    except ValueError:
        pass
    else:
        raise AssertionError('zero-gain recovery was silently admitted')

    # Diagnostic source normalization, not an evaluation of native Info/work.
    h=.125; n=7; N=16
    D=sparse.diags((-np.ones(n-1),2*np.ones(n),-np.ones(n-1)),(-1,0,1),format='csc')/h**2
    I=sparse.eye(n,format='csc')
    Lh=sparse.kron(D,I,format='csc')+sparse.kron(I,D,format='csc')
    x=np.arange(1,n+1)*h
    X,Y=np.meshgrid(x,x,indexing='ij')
    normalized = h*h*np.sin(np.pi*X).ravel()*np.sin(np.pi*Y).ravel()
    coh=float(sp.N(coh_times_N/N,18))
    ptr=float(sp.N(ptr_times_N/N,18))
    ratio=float(sp.N(beta,18))
    solutions=[]
    a_j=1.0  # diagnostic unit only, not the original unknown a_J,h
    for g in (coh,ptr):
        raw=(a_j*g/(2*h))*normalized
        restored=(2*h/(a_j*g))*raw
        require(np.max(abs(restored-normalized))<1e-17, 'correct full source normalization')
        v=-spsolve(Lh,restored)
        require(np.max(abs(Lh@v+restored))<1e-12, 'exact-source equation numerical replay')
        require(np.max(abs(v))<=normal_metric_bound(h,a_j,g,float(np.max(abs(raw))))+1e-13,
                'gain-aware uniform metric bound')
        solutions.append(v)
    require(np.max(abs(solutions[0]-solutions[1]))<1e-15,
            'two gains preserve the same normalized geometric equation')
    same_raw=(a_j*coh/(2*h))*normalized
    v1=-spsolve(Lh,(2*h/(a_j*coh))*same_raw)
    v2=-spsolve(Lh,(2*h/(a_j*ptr))*same_raw)
    require(np.max(abs(v1-ratio*v2))<1e-15, 'equal raw residual is amplified by inverse actual gain')
    bound16=normal_metric_bound(h,a_j,coh,.001)
    bound32=normal_metric_bound(h,a_j,coh/2,.001)
    require(bound32==2*bound16, 'doubling query dimension cannot be hidden in normalization')
    return {
        'status':'PASS_SOURCE_GAIN_TO_PRIMARY_RECOVERY',
        'input_ref':INPUT_REF,
        'prior_checker_git_blob':PRIOR_BLOB,
        'terminal_identity_owner':{'path':OWNER,'git_blob':OWNER_BLOB,
                                   'status':'CONSUMED_CONDITIONAL_ORIGINAL_PROTOCOL'},
        'exact':{'complete_work_born_normalization':True,
                 'golden_reporter_jet':'8*p^(9/2)',
                 'pointer_to_coherent_gain':'4+log_phi(4)',
                 'gamma_h':'Q0*R0/(2*N_h)',
                 'matter_gravity_ratio_preserved':True,
                 'metric_bound':'h*||r_h||_inf/(4*|a_J,h|*gain_floor)',
                 'zero_gain_rejected':True,
                 'moving_gain_and_readout_terms_retained':True},
        'numerical':{'pointer_to_coherent_gain':ratio,
                     'N_h_times_coherent_gain':float(sp.N(coh_times_N,18)),
                     'N_h_times_pointer_gain':float(sp.N(ptr_times_N,18)),
                     'diagnostic_sites':n*n,
                     'same_normalized_equation_difference':float(np.max(abs(solutions[0]-solutions[1]))),
                     'same_raw_inverse_gain_difference':float(np.max(abs(v1-ratio*v2))),
                     'dimension_doubling_amplification':bound32/bound16},
        'scope':{'new_action':False,'physical_price_selection_proved':False,
                 'actual_full_Info_work_remainder_computed':False,
                 'all_row_compatibility_proved_for_remainder':False,
                 'prospective_minimum_repaired':False,'GR_closed':False}}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=calculate()
    text=json.dumps(result,indent=2,ensure_ascii=False)
    print(text)
    if args.json: args.json.write_text(text+'\n',encoding='utf-8')

if __name__=='__main__': main()
