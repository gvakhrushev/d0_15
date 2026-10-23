#!/usr/bin/env python3
"""Exact Newton/Girard allblank complete Stinespring Book/Hodge source test.

This is an adversarial rational d=4 FOUR-distinct-eigenvalue fixture for the
UNIVERSAL native-positive-blank theorem, deliberately not the old two-eigen
CAR16 special point. Python stdlib Fraction ONLY, no numerical root solver,
no physical M1 cut/Hodge selection, no 42-field GR promotion. All abort/
nonblank outcomes remain in the parent CPTP instrument.

Run: python3 02_REGISTRY/research/sources/d0_native_two_blank_hodge_recursion_2026-10-22/check_universal_blank_newton.py
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import reduce
from math import factorial
import json

CHECKS = 0
def require(ok, label):
    global CHECKS
    CHECKS += 1
    if not bool(ok):
        raise ArithmeticError(label)

# Rational strict positive BLANK squared eigenvalues x_i; d=4 distinct.
xs=[F(1,5),F(2,5),F(3,5),F(4,5)]
# True moving first jets of a supplied positive spectral native chart.
velocities=[F(i,200) for i in (1,2,3,4)]
d=len(xs)
zeta=F(1,2**20)
moments=[F(d)]
dmoments=[F(0)]
elementary=[F(1)]
delementary=[F(0)]
for k in range(1,d+1):
    moments.append(sum(x**k for x in xs))
    dmoments.append(sum(k*x**(k-1)*velocities[i]
                        for i,x in enumerate(xs)))
    elementary.append(sum((-1)**(j-1)*elementary[k-j]*moments[j]
                          for j in range(1,k+1))/k)
    delementary.append(sum((-1)**(j-1)*
                           (delementary[k-j]*moments[j]
                            +elementary[k-j]*dmoments[j])
                            for j in range(1,k+1))/k)
    require(elementary[k]>0,"genuine positive elementary coefficient")
for x in xs:
    require(sum((-1)**k*elementary[k]*x**(d-k)
                for k in range(d+1))==0,
            "EXACT original-type positive blank characteristic polynomial")

# 89 future allblank power moments and EVERY first derivative from FIRST FOUR only.
for k in range(d+1,90):
    moments.append(sum((-1)**(j-1)*elementary[j]*moments[k-j]
                       for j in range(1,d+1)))
    dmoments.append(sum((-1)**(j-1)*
                    (delementary[j]*moments[k-j]+elementary[j]*dmoments[k-j])
                    for j in range(1,d+1)))
for n in range(1,90):
    require(moments[n]==sum(x**n for x in xs),
            "allblank first four moments determine every later source VALUE")
    require(dmoments[n]==sum(n*x**(n-1)*velocities[i]
                             for i,x in enumerate(xs)),
            "allblank four source JETS determine every later native jet")

# FULL literal r128 oldRIGHT feedback determinant, not just one recovered eigenvalue.
for n in (1,2,3,7,21):
    en=[F(1)]
    den=[F(0)]
    for k in range(1,d+1):
        en.append(sum((-1)**(j-1)*en[k-j]*moments[n*j]
                       for j in range(1,k+1))/k)
        den.append(sum((-1)**(j-1)*
                          (den[k-j]*moments[n*j]+en[k-j]*dmoments[n*j])
                        for j in range(1,k+1))/k)
    ratio=zeta/(1-zeta)
    reconstructed=(1-zeta)**d*sum(en[k]*ratio**k for k in range(d+1))
    reconstructed_jet=(1-zeta)**d*sum(den[k]*ratio**k
                                      for k in range(d+1))
    direct=F(1)
    for x in xs:
        direct*=1-zeta+zeta*x**n
    direct_jet=F(0)
    for i,x in enumerate(xs):
        other=F(1)
        for j,y in enumerate(xs):
            if i!=j:
                other*=1-zeta+zeta*y**n
        direct_jet+=zeta*n*x**(n-1)*velocities[i]*other
    require(reconstructed==direct,
            "exact FULL Book determinant from native d original allblank events")
    require(reconstructed_jet==direct_jet,
            "exact WHOLE oldRIGHT128 Book first source, no eigenvector branch")
    require(reconstructed>0,
            "original Book positive pencil whole output")
    book_jet=-128*reconstructed_jet/reconstructed
    actual_book_jet=-128*direct_jet/direct
    require(book_jet==actual_book_jet,
            "exact Golden original oldRIGHT multiplier keeps source unchanged")

# Original beta fixed positive in a representative rational Golden-compatible
# mathematical control; the real original beta=2p² stays in research theorem.
beta=F(3,4)
oldRIGHT=128
K=20
tail_bound=2*oldRIGHT*d*beta**(K+1)/factorial(K+1)
require(F(0)<tail_bound<F(1,10**12),
        "finite all-Hodge zero-mode preserving heat Poisson-tail budget")

# SHARPNESS: three generic d=4 moments cannot see this REAL first source.
# Vandermonde null tangent: sum x_i^k / product_{j!=i}(x_i-x_j)=0 for k<d-1,
# but equals 1 for k=d-1. Thus m_1,m_2,m_3 have zero derivatives while m_4 moves.
invisible=[]
for i,x in enumerate(xs):
    denom=reduce(lambda v,w:v*w,(x-xs[j] for j in range(d) if j!=i),F(1))
    invisible.append(1/denom)
for k in range(1,d):
    require(sum(k*xs[i]**(k-1)*invisible[i] for i in range(d))==0,
            "hostile moving spectral tangent invisible to only d−1 blank events")
require(sum(d*xs[i]**(d-1)*invisible[i] for i in range(d))==d,
        "same hostile tangent CHANGES last necessary original blank event source")
vandermonde=factorial(d)
for i in range(d):
    for j in range(i+1,d):
        vandermonde*=xs[j]-xs[i]
require(vandermonde!=0,
        "exact full four-blank source Jacobian is nonsingular Vandermonde")
print(json.dumps({
    "status":"PASS_EXACT_FRACTION",
    "checks":CHECKS,
    "data_dimension":d,
    "strictly_positive_distinct_original_type_blank_x":
         [str(x) for x in xs],
    "first_d_probabilities":[str(moments[k]/d) for k in range(1,d+1)],
    "later_exact_moments_and_sources_through":89,
    "whole_oldRIGHT128_feedback_determinants_checked_at_n":[1,2,3,7,21],
    "entire_Hodge_Poisson_tail_upper_at_K20":str(tail_bound),
    "d_minus_1_moments_insufficient_even_for_first_source":True,
    "nonzero_last_moment_null_tangent_jet":str(d),
    "vandermonde_full_rank":True,
    "actual_complete_128_Kraus_matrix_replay_in_this_script":False,
    "original_128_Kraus_consumed_in_sibling_checker":True,
    "selected_physical_Book03_scene_Hodge":False,
    "original_all42_GR_closed":False
},indent=2))
