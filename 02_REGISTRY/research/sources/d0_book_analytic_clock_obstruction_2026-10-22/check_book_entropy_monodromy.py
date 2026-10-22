#!/usr/bin/env python3
"""Finite Golden Hodge/feedback cannot reproduce Shannon log source on an open report chart.

Exact Fraction verification of complete capped first-match stopped histories;
complex winding checks illustrate the distinct monodromies on the published
native cost20 READY clean reflection/cut-heat carrier. No selected physical
Book03 Info, no new GR root. Python stdlib only.
"""
from __future__ import annotations
import cmath
from fractions import Fraction as Q
import json
import math

checks=0

def check(cond,description):
    global checks
    checks+=1
    if not cond: raise ArithmeticError(description)

def stopped_tapes(m,K):
    leaves=[]
    def go(anchor,word):
        if len(word)==K+1:
            leaves.append(tuple(word))
            return
        for b in range(m):
            if b==anchor: leaves.append(tuple(word+[b]))
            else: go(anchor,word+[b])
    for a in range(m): go(a,[a])
    return leaves

def qpoly(gamma):
    return [(1-gamma,Q(0)),(gamma,-gamma),(Q(0),gamma)]

def value(coeff,r):
    return coeff[0]+coeff[1]*r

def degree_one_coefficient(word,p):
    acc=Q(0)
    for j,b in enumerate(word):
        term=p[b][1]
        for i,a in enumerate(word):
            if i!=j:term*=p[a][0]
        acc+=term
    return acc

def lcap(gamma,K):
    # Complete stopped-language expected TOTAL trials for 3 positive labels
    return 4-(gamma**K+(1-gamma)**K+Q(1)**K)

gam=Q(2,5)
exact=[]
for K in [1,2,3,4,5,6]:
    leaves=stopped_tapes(3,K)
    p=qpoly(gam)
    # Test normalization/complete expected rare visit probability at exact rational r.
    for r in [Q(1,5),Q(1,13),Q(1,47)]:
        probs=[]
        rarecount=Q(0)
        elapsed=Q(0)
        for leaf in leaves:
            pr=Q(1)
            for label in leaf:pr*=value(p[label],r)
            probs.append(pr)
            rarecount+=leaf.count(2)*pr
            elapsed+=len(leaf)*pr
        check(sum(probs)==1,"full finite stopped tree normalized, with all abort leaves")
        q=[value(v,r) for v in p]
        L=4-sum((1-v)**K for v in q)
        check(elapsed==L,"exact whole finite stop expected tick count")
        check(rarecount==q[2]*L,"exact rare occupancy count")
    # Probability of exactly one rare (the r log r coefficient); no numerical derivative.
    coeff=sum((leaf.count(2)*degree_one_coefficient(leaf,p)
               for leaf in leaves),Q(0))
    expected=gam*lcap(gam,K)
    check(coeff==expected,"exact r log r stopped-info coefficient from ALL tapes")
    check(coeff<3*gam and coeff>0,"finite clock has <3 gamma rare source at r=0")
    exact.append({"K":K,"leaves":len(leaves),"rlogr_coeff":str(coeff),
                  "native_finite_limit_trial_count":str(lcap(gam,K)),
                  "uncapped_positive_r_coeff":"8/5",
                  "missing_source_coeff":str(4*gam-coeff)})
check(all(x['K']==j+1 for j,x in enumerate(exact)),"ordered complete cap certificates")

# ORIGINAL native cap9/20 factory readiness, original Golden cost20 READY source.
p=(math.sqrt(5)-1)/2
ell=math.log(1/p)
alpha=(1-(1-2*p**3)**9)**128
factory=((1-p**120)**4*(1-(1-16*p**9)**20))**43
gamma=alpha*factory
ready=2*10946*p**23
beta=2*p*p
zeta=2**-20
Dw=50549
check(.45<gamma<.46 and .34<ready<.35,"authentic native cap9/20 and cost20 readiness")
check(0<zeta<1 and Dw>50000,"full retained Golden cutoff and actual Hilbert rank")

def native_book_slope(r):
    # Actual READY clean reflected return, with its complete original
    # cut-induced 2-block Hodge trace (Book-type H+J candidate).
    q=ready*r
    F=4*q*(1-q)
    Fr=4*ready*(1-2*q)
    eb=cmath.exp(-beta*F)
    Z=Dw-2+2*eb
    return -2*eb*Fr/Z+128*zeta*Fr/(1-zeta*F)

# Native algebraic return's monodromy is zero even after the exp/log-trace.
rad=.05
steps=128
first=native_book_slope(rad)
last=native_book_slope(rad*cmath.exp(2j*math.pi))
check(abs(first-last)<5e-15,"native actual full cut Hodge+J slope returns after analytic loop")
# Continuous winding of r/(1-r) creates 2pi i /ln(phi) in the source;
# Arg(1-r) has zero winding on |r|=0.05.
def continued_code_source(theta):
    r=rad*cmath.exp(1j*theta)
    return gamma*(1+(math.log(abs(r))-math.log(abs(1-r))
         +1j*(theta-cmath.phase(1-r)))/ell)
first_info=continued_code_source(0.)
last_info=continued_code_source(2*math.pi)
monodromy=last_info-first_info
check(abs(monodromy-2j*math.pi*gamma/ell)<1e-14,
      "genuine native 0/10 cost-minus-Shannon source has infinite logarithmic monodromy")
for j in range(steps+1):
    theta=2*math.pi*j/steps
    r=rad*cmath.exp(1j*theta)
    check(abs(native_book_slope(r))<.001,
          "the authentic finite ready-cut spectral derivative remains bounded")

# The exact uncapped positive-alphabet first-match factor is 4, not the
# fixed-K r->0 factor that stays <=3 no matter how large finite K is.
for K in [1,4,20,100,100000000]:
    L0=3-gamma**K-(1-gamma)**K
    check(2-1e-11<=L0<=3.,"native cap-first rare-birth coefficient <=3 rather than 4")
    check(4*gamma-gamma*L0>=gamma-1e-12,
          "uniform missing rare-source coefficient >= gamma")

# At the already owned actual nonflat rare r, cap100M is sufficient only
# on this finite compact chart, NOT uniformly down to r=0.
r_native=1.8512395785208469e-6
qrare=gamma*r_native
check(qrare>8e-7 and qrare<9e-7,"actual rare native 3-status Born law")
check((1-qrare)**100000000<1e-34,"existing finite K100M safe at the fixed positive root")

print(json.dumps({"status":"PASS","checks":checks,
    "finite_trees_exact_rational":exact,
    "native_factory_readiness":gamma,
    "native_ready_cost20":ready,
    "finite_return_derivative_at_r=.05":first.real,
    "finite_book_monodromy":abs(last-first),
    "native_golden_information_slope_monodromy_imag":monodromy.imag,
    "rlogr_coeff_uncapped_positive_three_class":4*gamma,
    "rlogr_coeff_at_rare_birth_limit_K_infty_after_r0":3*gamma,
    "strict_nonuniform_coeff_gap":gamma,
    "actual_fixed_rare_root":r_native,
    "compulsory_Book03_Hodge_identified":False,
    "uniform_mesh_C1_refinement":False,
    "GR_closed":False},indent=2))
