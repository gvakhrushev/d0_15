#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Exact finite real quarter-wave branches on all four N0 axes.

Full independent-edge and unrestricted solder Euler, not a restricted action
or Taylor extrapolation. Rational identities hold in Q(z); denominators are
nonzero near z=0. Each phase represents 64 sites of the L=4 torus.
"""
from itertools import combinations
import json
from pathlib import Path
import sympy as s
ETA=s.diag(1,-1,-1,-1)
I=s.eye(4)
PAIRS=list(combinations(range(4),2))
G2=s.diag(*(ETA[a,a]*ETA[b,b] for a,b in PAIRS))
STAR=s.zeros(6)
for j,(i,sign) in enumerate(((5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1))):
    STAR[i,j]=sign

def check(name, value):
    if not value:
        raise AssertionError(name)
    print('PASS_' + name, flush=True)

def zero(matrix):
    return all(s.cancel(x) == 0 for x in matrix)

def boost(j):
    out = s.zeros(4)
    out[0, j] = out[j, 0] = 1
    return out

def rot(a, b):
    out = s.zeros(4)
    out[a, b], out[b, a] = 1, -1
    return out

def wedge(u, v):
    return s.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])

def biv(X):
    raw = X * ETA
    return s.Matrix([raw[a, b] for a, b in PAIRS])

def orient(a, b):
    seq = [a, b] + [i for i in range(4) if i not in (a, b)]
    return (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))

def inv(U):
    return ETA * U.T * ETA

def cayley(Y, k, z):
    return (I + 4 * z / (4 + k * z**2) * Y + 2 * z**2 / (4 + k * z**2) * Y**2).applyfunc(s.cancel)

def shift(site, r, amount=1):
    out = list(site)
    out[r] += amount
    return tuple(out)

def factors_at(site, a, b, links):
    places = [(site, a, False), (shift(site, a), b, False), (shift(site, b), a, True), (site, b, True)]
    return [inv(links(x, r)) if backwards else links(x, r) for x, r, backwards in places]

def product(items):
    out = I
    for x in items:
        out = out * x
    return out

def edge_euler(site, role, X, links, solder):
    total = s.Integer(0)
    for a, b in PAIRS:
        corners = [(site, 0), (shift(site, b, -1), 2)] if role == a else ([(shift(site, a, -1), 1), (site, 3)] if role == b else [])
        for base, corner in corners:
            factors = factors_at(base, a, b, links)
            P = product(factors)
            changed = list(factors)
            changed[corner] = factors[corner] * X if corner < 2 else -X * factors[corner]
            dp = product(changed)
            dc = (dp + inv(P) * dp * inv(P)) / 2
            # The base-site solder is essential.  Freezing this at `site`
            # would silently delete the neighboring slow-background term.
            e = solder(base)
            u, v = [i for i in range(4) if i not in (a, b)]
            total += orient(a, b) * (wedge(e[:, u], e[:, v]).T * G2 * STAR * biv(dc))[0]
    return s.cancel(total)

def solder_euler(site, links, solder):
    e = solder(site)
    out = s.zeros(4)
    curvatures = {}
    for a, b in PAIRS:
        P = product(factors_at(site, a, b, links))
        curvatures[a, b] = (P - inv(P)) / 2
    for i in range(4):
        for j in range(4):
            de = s.zeros(4)
            de[i, j] = 1
            value = s.Integer(0)
            for a, b in PAIRS:
                u, v = [r for r in range(4) if r not in (a, b)]
                dw = wedge(de[:, u], e[:, v]) + wedge(e[:, u], de[:, v])
                value += orient(a, b) * (dw.T * G2 * STAR * biv(curvatures[a, b]))[0]
            out[i, j] = s.cancel(value)
    return out

GEN=[boost(j) for j in (1,2,3)]+[rot(a,b) for a,b in ((1,2),(1,3),(2,3))]
WEIGHTS=((0,0,0,1,-1,1),(0,1,-1,0,0,1),(1,0,-1,0,1,0),(1,-1,0,1,0,0))
CENSUS_IDS=(1,3,4,6)
census=json.loads(Path(__file__).with_name('a4d_joint_resonance_kernel_census.json').read_text())['n0_bases']['4']
check('OWNED_DIAGONAL_CHARACTER',census['ids']==[1,1,1,1])
expected=[]
for active,weights in enumerate(WEIGHTS):
    vector=[0]*24
    vector[6*active:6*active+6]=weights
    expected.append(vector)
check('OWNED_N0_BASIS',[[int(x) for x in v] for v in census['basis']]==expected)
z=s.symbols('z', real=True)
for active, weights in enumerate(WEIGHTS):
    Y=sum((w*g for w,g in zip(weights,GEN)),s.zeros(4))
    a,b,c=[r for r in range(4) if r!=active]
    u,v=I[:,b]-I[:,a],I[:,c]-I[:,a]
    k=(u.T*ETA*u)[0]*(v.T*ETA*v)[0]-(u.T*ETA*v)[0]**2
    check(f'AXIS_{active}_COMPLEMENT_PLANE',Y==-(u*v.T-v*u.T)*ETA)
    check(f'AXIS_{active}_SIMPLE_CUBIC',Y**3==-k*Y)
    check(f'AXIS_{active}_KAPPA',k==(3 if active==0 else -1))
    U=cayley(Y,k,z)
    check(f'AXIS_{active}_LORENTZ',zero(U.T*ETA*U-ETA))
    check(f'AXIS_{active}_TANGENT',U.diff(z).subs(z,0)==Y)
    phases=(U,I,inv(U),I)
    def links(site,role):
        return phases[sum(site)%4] if role==active else I
    for phase in range(4):
        site=(phase,0,0,0)
        ek=[edge_euler(site,role,X,links,lambda _:I) for role in range(4) for X in GEN]
        check(f'AXIS_{active}_PHASE_{phase}_ALL_24_EDGE_EULER',all(x==0 for x in ek))
        eq=solder_euler(site,links,lambda _:I)
        check(f'AXIS_{active}_PHASE_{phase}_ALL_16_SOLDER_EULER',eq==s.zeros(4))
    other=next(r for r in range(4) if r!=active)
    a,b=sorted((active,other))
    hol=product(factors_at((0,0,0,0),a,b,links))
    curvature=(hol-inv(hol))/2
    sign=1 if active==a else -1
    check(f'AXIS_{active}_EXACT_NONZERO_CURVATURE',zero(curvature-sign*4*z/(4+k*z*z)*Y))
    check(f'AXIS_{active}_CURVATURE_NONZERO',curvature.subs(z,s.Rational(1,3))!=s.zeros(4))
    # Shifting the four phases by one gives the real sine branch; it is a
    # lattice translation of the same all-phase equations, not an extra ansatz.
    check(f'AXIS_{active}_COS_TANGENT',all(phases[p].diff(z).subs(z,0)==(1,0,-1,0)[p]*Y for p in range(4)))
    check(f'AXIS_{active}_SIN_TANGENT',all(phases[(p-1)%4].diff(z).subs(z,0)==(0,1,0,-1)[p]*Y for p in range(4)))
# Hostile control: the #227 visible tangent on role 0 must not pass the metric gate.
Y=GEN[0]+GEN[1]+GEN[2]
U=(I+z*Y/2)*(I-z*Y/2).inv()
phases=(U,I,inv(U),I)
def bad_links(site,role):
    return phases[sum(site)%4] if role==0 else I
check('227_VISIBLE_TANGENT_FAILS_SOLDER_GATE',solder_euler((0,0,0,0),bad_links,lambda _:I)!=s.zeros(4))
print('J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND',flush=True)
