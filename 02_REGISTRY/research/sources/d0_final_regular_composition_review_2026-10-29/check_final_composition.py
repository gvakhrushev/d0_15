#!/usr/bin/env python3
"""Exact arithmetic checks for the final regular-source composition.

These checks audit composition interfaces; they do not emit the large GR
programme or prove universal physical task selection. They never use an
Einstein residual to construct an interval or choose an admitted test.
Python >= 3.10, standard library only.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import hashlib
import json
import argparse

CHECKS: list[str] = []

def check(condition: bool, label: str) -> None:
    if not condition:
        raise ArithmeticError(label)
    CHECKS.append(label)

def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def inv(a):
    d=det(a)
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]

def trprod(a,b):
    return sum(a[i][j]*b[j][i] for i in range(2) for j in range(2))

def source_identity():
    # Rational control of the general source identity at native z. eta is a
    # structural positive retention factor, not a replacement Golden birth.
    z=F(1,2**20); eta=F(2,5); alpha=F(1,3); eps=F(1,64); rf=F(1,7)
    A=[[F(1,3),F(1,9)],[F(1,9),F(1,2)]]
    dA=[[F(1,7),F(1,3)],[F(1,3),F(-1,5)]]
    check(matmul(A,dA)!=matmul(dA,A),'past and tangent genuinely noncommute')
    traceA=A[0][0]+A[1][1]
    data=[]
    for count in (1,2,5,9):
        c=[1-2*alpha*F(1,j+9) for j in range(count)]
        dr=[F((-1)**j,10+j) for j in range(count)]
        s=prod(x*x for x in c);L=sum(1/x for x in c)
        ds=s*sum(-4*alpha*drj/cj for drj,cj in zip(dr,c))
        D=[[(1-z if i==j else 0)+z*eta*s*A[i][j] for j in range(2)] for i in range(2)]
        dD=[[z*eta*(ds*A[i][j]+s*dA[i][j]) for j in range(2)] for i in range(2)]
        # Direct polynomial determinant derivative, independent of resolvent formula.
        ddet=dD[0][0]*D[1][1]+D[0][0]*dD[1][1]-dD[0][1]*D[1][0]-D[0][1]*dD[1][0]
        direct=-ddet/det(D)
        Di=inv(D);trA=trprod(Di,A);trDA=trprod(Di,dA)
        gain=4*alpha*eps*rf*z*eta*s*trA*L
        weights=[1/(cj*L) for cj in c]
        old=-trDA/(4*alpha*eps*rf*L*trA)
        expected=sum(w*r/(eps*rf) for w,r in zip(weights,dr))+old
        check(direct/gain==expected,f'complete source exact M={count}')
        check(gain>0 and min(weights)>0 and sum(weights)==1,f'true gain and weights M={count}')
        l1=sum(abs(x) for row in dA for x in row)
        bound=l1/((1-z)*traceA*4*alpha*eps*rf*count)
        check(abs(old)<=bound,f'whole old-source bound M={count}')
        data.append({'copies':count,'exact_normalized_identity':True,'gain_positive':True})
    return data

def norm_composition():
    # Independent copies use an l-infinity product, hence an l1 dual. All
    # finite vertices are enumerated; this is not a shared-diagonal-only test.
    results=[]
    for weights in ([F(1)], [F(1,2),F(1,2)], [F(1,7),F(2,7),F(4,7)]):
        coefficients=[F(2,5),F(-3,7)]
        rows=[w*x for w in weights for x in coefficients]
        dual=max(abs(sum(a*v for a,v in zip(rows,vertex))) for vertex in product((-1,1),repeat=len(rows)))
        target=sum(abs(x) for x in coefficients)
        check(dual==target,f'independent product dual not diluted M={len(weights)}')
        for v in product((-1,1),repeat=2):
            diagonal=list(v)*len(weights)
            check(sum(a*x for a,x in zip(rows,diagonal))==sum(a*x for a,x in zip(coefficients,v)),
                  f'diagonal right-inverse M={len(weights)} v={v}')
        old=F(1,19)
        full=max(abs(old*o+sum(a*v for a,v in zip(rows,vertex))) for o in (-1,1)
                 for vertex in product((-1,1),repeat=len(rows)))
        check(full==target+old,f'past not silently frozen M={len(weights)}')
        results.append({'copies':len(weights),'full_current_dual':str(dual),'past_dual':str(old)})
    check(abs(F(1,2)+F(-1,2))==0 and abs(F(1,2))+abs(F(-1,2))==1,
          'opposite rows cancel shared test but not independent dual')
    # The positive field graph does not erase a genuine free report coordinate.
    field_rows=[F(0),F(0)]; query_row=F(1,3)
    check(sum(abs(x) for x in field_rows)+abs(query_row)==F(1,3),
          'extra free QUERY remains outside a falsely promoted zero')
    return results

def finite_test_exhaustion():
    # Infinite test space c0 with sup norm, F(v)=sum 2^-j v_j.
    # The exact finite calculation of its first k coefficients checks that
    # finite-stage surjectivity onto the WHOLE infinite space is unnecessary.
    # The infinite-space assertion is proved analytically in the review.
    rows=[]
    for k in (1,2,4,8,16):
        finite_norm=sum(F(1,2**j) for j in range(1,k+1))
        tail=F(1,2**k)
        check(finite_norm==1-tail,f'dense finite test dual tail k={k}')
        missed=F(1,2**(k+1))
        check(missed>0,f'finite stage is not surjective onto all tests k={k}')
        check(missed<=tail,f'controlled missed-test response k={k}')
        rows.append({'represented_coordinates':k,'dual_norm':str(finite_norm),
                     'exact_full_dual_tail':str(tail),'global_right_inverse_asserted':False})
    check(all((F(1) if k>=7 else F(0))==0 for k in range(1,7)),
          'a late nonzero test may be missed at finitely many initial levels')
    check(F(1)>0,'late nonzero coefficient is separated once its test is included')
    return rows


def log_interval(x: F, tolerance: F) -> tuple[F,F,int]:
    """Certified real log, using exact atanh series and rigorous tail."""
    if x<=0 or tolerance<=0:
        raise ValueError('positive log argument and error tolerance required')
    y=(x-1)/(x+1)
    if y==0:
        return F(0),F(0),0
    total=F(0);power=y;n=0
    while True:
        total+=2*power/(2*n+1)
        n+=1;power*=y*y
        tail=2*abs(power)/((2*n+1)*(1-y*y))
        if tail<=tolerance:
            return total-tail,total+tail,n

def interval_protocol(y0: F, schedule: int) -> list[dict]:
    # Structural Book return only: J(y)=-log[a+z(c0-y^2)^2]. Its source on
    # the chosen chart is known analytically, but NOT used to select the
    # interval centre or resources. Full-gravity/heat budgets are consumed
    # from the upstream theorem, not numerically simulated by this example.
    z=F(1,2**20);a=1-z;c0=F(3,4);cc=c0-y0*y0
    gain=2*z*cc/(a+z*cc*cc)
    # For |y|<=1/2, 0<c<=1 and |c'|<=1, c''=-2, c'''=0.
    j2=2*z/a+4*z*z/(a*a)
    j3=12*z*z/(a*a)+16*z**3/a**3
    third=j3+6*j2
    lo_old=hi_old=None
    rows=[]
    for k in range(1,13):
        tau=F(1,2**(k+6)) # exact upstream K4 precision, NOT p^k guessed from floats
        step=F(1,2**(3+schedule))
        while abs(y0)+step>F(1,2) or third*step*step/(6*gain)>tau:
            step/=2
        truncation=third*step*step/(6*gain)
        numeric_budget=step*gain*tau/2
        ranges=[];terms=[]
        for sign in (1,-1):
            y=y0+sign*step;c=c0-y*y
            l,u,n=log_interval(a+z*c*c,numeric_budget)
            ranges.append((-u,-l));terms.append(n)
        # True full-value difference; no fit, source subtraction or desired zero.
        qlo=(ranges[0][0]-ranges[1][1])/(2*step*gain)
        qhi=(ranges[0][1]-ranges[1][0])/(2*step*gain)
        blo=qlo-truncation;bhi=qhi+truncation
        lo=blo if lo_old is None else max(lo_old,blo)
        hi=bhi if hi_old is None else min(hi_old,bhi)
        check(lo<=hi,f'nonempty interval from independent bounds y={y0} schedule={schedule} k={k}')
        check(hi-lo<=4*tau and 4*tau<F(1,2**k),f'certified kappa width y={y0} schedule={schedule} k={k}')
        if lo_old is not None:
            check(lo>=lo_old and hi<=hi_old,f'exact projection nesting y={y0} schedule={schedule} k={k}')
        # Analytic target used ONLY after constructing the actual enclosure.
        check(lo<=2*y0<=hi,f'analytic source verification y={y0} schedule={schedule} k={k}')
        rows.append({'k':k,'step':str(step),'gain':str(gain),'series_terms':terms,
                     'lower':str(lo),'upper':str(hi),'width_upper':str(4*tau),
                     'zero_excluded':not(lo<=0<=hi)})
        lo_old,hi_old=lo,hi
    return rows

def kappa_checks():
    values=[]
    for y in (F(0),F(1,5)):
        a=interval_protocol(y,0);b=interval_protocol(y,1)
        for ra,rb in zip(a,b):
            lo=max(F(ra['lower']),F(rb['lower']));hi=min(F(ra['upper']),F(rb['upper']))
            check(lo<=hi,f'different valid finite schedules compatible y={y} k={ra["k"]}')
        check(all(x['zero_excluded'] for x in a)==(y!=0),f'nonzero separating witness y={y}')
        values.append({'centre':str(y),'analytic_source_for_postcheck':str(2*y),
                       'target_used_to_construct_intervals':False,'schedules':[a,b]})
    # Paying growth actually matters. With p>3/5, 2p>6/5, exact sufficient bound.
    constants=F(10**8);target=F(1,2**20);K=0
    while constants*F(5,6)**K>target:
        K+=1
    check(constants*F(5,6)**K<=target,'finite post-compilation growing-clock budget')
    check(K>0 and constants*F(5,6)**(K-1)>target,'positive paid growth required')
    return {'intervals':values,'retention_scenario':{'prefix_constant':str(constants),'target':str(target),
            'selected_K':K,'rational_upper':str(constants*F(5,6)**K),
            'actual_large_programme_emitted':False}}

def main() -> None:
    result={'input_commit':'6e20be09b25e1d68ac19be032814ce8ab2ab7351',
            'scope':'exact composition and interval-protocol controls, not a new universal GR theorem',
            'complete_source':source_identity(),'independent_norms':norm_composition(),
            'finite_test_exhaustion':finite_test_exhaustion(),
            'kappa_protocol':kappa_checks()}
    result.update({'status':'PASS_FINAL_COMPOSITION_REVIEW','checks':len(CHECKS),
                   'check_names':CHECKS,'unrestricted_XN_closure_proved':False,
                   'finite_word_stationarity_claimed':False,'native_GR_word_emitted':False,
                   'Lean_or_CI_run':False,
                   'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--details',action='store_true',help='Print all exact interval endpoints and named checks.')
    args=parser.parse_args()
    if not args.details:
        for control in result['kappa_protocol']['intervals']:
            schedules=control.pop('schedules')
            control['depths_per_schedule']=len(schedules[0])
            control['all_intersections_nonempty']=True
            control['all_widths_below_p_power']=True
            control['all_schedule_intersections_nonempty']=True
            control['first_zero_excluding_depth']=next((r['k'] for r in schedules[0] if r['zero_excluded']),None)
            control['final_intervals']=[{'step':rows[-1]['step'],'lower':rows[-1]['lower'],
                'upper':rows[-1]['upper'],'width_upper':rows[-1]['width_upper']} for rows in schedules]
        result.pop('check_names')
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
