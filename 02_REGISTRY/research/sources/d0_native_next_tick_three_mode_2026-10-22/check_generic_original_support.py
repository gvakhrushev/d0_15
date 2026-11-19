#!/usr/bin/env python3
"""EXACT ORIGINAL CAR16/128 symbolic future-Kraus coordinate-support theorem.

- Genuine (0,2,3,1) CAR, phase word (i,i,-1,-i), nu=3/5.
- Original two repeated Walsh/Julia words, NO synthetic Bernoulli.
- Generic real proper boost coordinate r, formal independent Julia-root q.
- All 800 forbidden support matrix entries vanish as RATIONAL identities
  in r and q, NOT as decimal SVD tolerances.
- Entire 16x16 CAR source Delta=a†a is rational in r and splits into exactly
  eight native 2x2 pairs, each with ORIGINAL mu and d determinant.
- ACTUAL original rank at r=1/9 needed for mask EQUALITY is independently
  proved with Q(i,sqrt(24142)) algebraic DomainMatrix in the parent owner.
  This script does NOT silently claim generic rank from structural zeros.

Run: python3 check_generic_original_support.py
"""
from __future__ import annotations
import json
import sympy as S

R=S.Rational
i=S.I
r=S.symbols("r",real=True,positive=True)
q=S.symbols("q",real=True,positive=True)
nu=R(3,5)
I=S.eye(16)
ORDER=(0,2,3,1)
checks=0
def require(cond, msg):
    global checks
    checks+=1
    if not cond: raise ArithmeticError(msg)

creators=[]
for mode in range(4):
    c=S.zeros(16)
    for bits in range(16):
        if not ((bits>>mode)&1):
            prefix=ORDER[:ORDER.index(mode)]
            c[bits|(1<<mode),bits]=(-1)**sum((bits>>j)&1 for j in prefix)
    creators.append(c)
G=creators[0]*creators[1].T+creators[1]*creators[0].T
require(G**3==G,"native CAR/role-1 boost G^3=G")
U=I+2*r**2/(1-r**2)*G**2+2*r/(1-r**2)*G
phase=[i,i,-1,-i]
x1=i*nu*creators[1]*U
M=x1*x1.conjugate().T
N=x1.conjugate().T*x1
la=nu**2
lb=nu**2*(1+6*r*r+r**4)/(1-r*r)**2
# Native sqrt(I-XX*) is an interpolation polynomial on the 3 ORIGINAL
# eigenvalues 0, nu², nu² cosh(2theta), with q:=sqrt(1-lb).
c2=S.factor(((q-1)/lb-R(-1,5)/la)/(lb-la))
c1=S.factor(R(-1,5)/la-c2*la)
left=I+c1*M+c2*M*M
right=I+c1*N+c2*N*N
words=[]
for mode,c in enumerate(creators):
    base=nu*c
    x=base*(U if mode==1 else I)*phase[mode]
    l0=I-R(1,5)*c*c.T
    r0=I-R(1,5)*c.T*c
    ell=left if mode==1 else l0
    rr=right if mode==1 else r0
    for pair in ((x,ell),(x.conjugate().T,rr),(-base,-l0),(-base.T,-r0)):
        words.extend([pair,pair])
require(len(words)==32,"actual doubled 32 Golden/Julia native input words")

full=tuple(range(16))
def missing(j):
    if j%4 in (2,3): return full # exact Walsh dark labels
    if j in (1,5,17,21,25,33,37,41,49,53,57):
        return (0,4,8,12)
    if j==13: return (12,)
    if j==45: return (0,)
    if j in (29,61): return (0,12)
    return ()
total_forbidden=0
for lab in range(32):
    for port in range(2):
        j=2*lab+port
        omitted=missing(j)
        for column in omitted:
            for row in range(16):
                expr=sum(
                    (-1)**(bin(lab&word).count("1")&1)
                    *words[word][port][row,column]
                    for word in range(32)
                )/32
                require(S.cancel(expr)==0,
                        f"exact native zero Kraus column j={j},row={row},col={column}")
                total_forbidden+=1
# Dark masks are already the 32 Walsh rows with odd lab: all 16 columns
# for each => 32*16*16, PLUS 800 extra forbidden entries in LIVE rows.
require(total_forbidden==32*16*16+800,
        "all 800 EXTRA positive-branch forbidden coordinate entries plus dark")
# The genuinely original first binary Walsh row uses ONLY native X (b=0)
# and therefore has no Julia-square-root q dependence.
A=S.zeros(16)
for mode,c in enumerate(creators):
    base=nu*c
    x=base*(U if mode==1 else I)*phase[mode]
    A+=x+x.conjugate().T-base-base.T
A=A/16
Delta=A.conjugate().T*A
pairs=[(4*k,4*k+3) for k in range(4)]+[(4*k+1,4*k+2) for k in range(4)]
allowed={(x,y) for a,b in pairs for x,y in
         ((a,a),(a,b),(b,a),(b,b))}
zero_count=0
for x in range(16):
    for y in range(16):
        if (x,y) not in allowed:
            require(S.cancel(Delta[x,y])==0,
                    f"exact CAR 2x2 block structural zero {x},{y}")
            zero_count+=1
mu=9*(5*r**4+r**3-8*r*r-r+5)/(3200*(1-r*r)**2)
det=81*(23*r**4+6*r**3-32*r*r-10*r+25)/(10240000*(1-r*r)**2)
for a,b in pairs:
    block=Delta.extract([a,b],[a,b])
    require(S.cancel(block.trace()-2*mu)==0,
            f"EXACT native pair trace {a},{b}")
    require(S.cancel(block.det()-det)==0,
            f"EXACT native pair determinant {a},{b}")
deltac=9*(5*r**4+2*r**3-6*r*r-2*r+5)/(3200*(1-r*r)**2)
deltac_prime=9*(1+r*r)*(r*r+4*r-1)/(1600*(1-r*r)**3)
for ix in (3,7,11,15):
    require(S.cancel(Delta[ix,ix]-deltac)==0,
            "genuine native identical CAR local3 diagonal")
require(S.cancel(S.diff(deltac,r)-deltac_prime)==0,
        "exact native moving CAR scalar source derivative")
require(deltac.subs(r,R(1,9))==R(69489,5120000),
        "exact original boost r=1/9 third mode rational")
require(deltac_prime.subs(r,R(1,9))==-R(328779,102400000),
        "exact original third mode proper Lorentz first jet")
print(json.dumps({
    "status":"PASS_EXACT_GENERIC_ORIGINAL_NATIVE_CAR_WALSH",
    "assertions":checks,
    "generic_CAR_Walsh_dark_columns_including_nonlive":32*16*16,
    "generic_ADDITIONAL_live_forbidden_entries":800,
    "CAR_16_nonpair_zero_matrix_entries":zero_count,
    "true_original_2x2_pairs":pairs,
    "actual_rank_census_at_r_one_ninth":"CONSUMED EXACT PREVIOUS Q(i,sqrt24142) OWNER",
    "consequence":"r1/9 positive rank minor persists in an open chart; all pointer supports are the original fixed diagonal masks",
    "delta_c_formula":str(S.factor(deltac)),
    "delta_c_r_one_ninth":"69489/5120000",
    "delta_c_jet_r_one_ninth":"-328779/102400000",
    "two_ticked_physical_Book03_scene_Hodge_selected":False,
    "GR_closed":False
},indent=2))
