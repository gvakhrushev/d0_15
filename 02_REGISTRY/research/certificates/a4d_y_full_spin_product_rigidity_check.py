#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact product-plane rigidity for the full temporal SO(3) spin Cayley sector.

At z=1 use the product-plane solder S_f=I+(f-1)P_perp and a phase-0
temporal link
    K0 = C_Y(1) C_B(-d) C_R,
R = a J12 + b J13 + c J23,
with C_R the full spatial SO(3) Cayley transform. Odd temporal links and all
spatial links are identity in the local role-0 replay.

Three boost Euler rows admit an exact polynomial combination equal to a
nonnegative multiplier times
    lap = 3 f0^2 - f1^2 - f2^2 - f3^2.
For real parameters in the B-Cayley chart the multiplier vanishes only on
    d=0, a-b+c=4.
On that entire exceptional plane the spatial-role transport is identical for
both the reciprocal completion [K,I,K^-1,I] and the alternative phase-2
ordering C_Y(1)^-1 C_R with the same spin factor.  In either convention the
rotation-row linear system has kernel span(1,1,1,1), hence f1=f2=f3=f0.

This is a necessary-row no-go for temporal spatial-spin rescue on the z=1
product-plane seed. It does not exclude arbitrary transverse corrections on
spatial links or prove the global response-decoupling terminal.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_full_spin_product_rigidity_results.json"

ETA = sp.diag(1,-1,-1,-1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4),2))
GEN=[]
for p,q in PAIRS:
    X=sp.zeros(4)
    X[p,q]=1
    X[q,p]=-ETA[p,p]*ETA[q,q]
    GEN.append(X)
G2=sp.diag(*(ETA[p,p]*ETA[q,q] for p,q in PAIRS))
STAR=sp.zeros(6)
for col,(row,sign) in enumerate([(5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1)]):
    STAR[row,col]=sign

Y=GEN[3]-GEN[4]+GEN[5]
B=GEN[0]+GEN[1]+GEN[2]
P_PERP=-Y**2/3

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)

def linv(M):
    return ETA*M.T*ETA

def wedge(u,v):
    return sp.Matrix([u[p]*v[q]-u[q]*v[p] for p,q in PAIRS])

def biv(M):
    X=M*ETA
    return sp.Matrix([X[p,q] for p,q in PAIRS])

def orientation(p,q):
    seq=[p,q]+[j for j in range(4) if j not in (p,q)]
    inv=sum(seq[i]>seq[j] for i,j in PAIRS)
    return -1 if inv%2 else 1

def shift(site,role,step=1):
    x=list(site); x[role]+=step; return tuple(x)

def cayley_simple(generator,norm2,amplitude=sp.Integer(1)):
    den=4+norm2*amplitude**2
    return I4 + 4*amplitude/den*generator + 2*amplitude**2/den*generator**2

def edge_euler(solder,link,site,role,generator):
    total=sp.Integer(0)
    for p,q in PAIRS:
        if role==p:
            corners=[(site,0),(shift(site,q,-1),2)]
        elif role==q:
            corners=[(shift(site,p,-1),1),(site,3)]
        else:
            continue
        for base,corner in corners:
            places=[(base,p,False),(shift(base,p),q,False),
                    (shift(base,q),p,True),(base,q,True)]
            factors=[linv(link(x,r)) if inv else link(x,r)
                     for x,r,inv in places]
            P=factors[0]*factors[1]*factors[2]*factors[3]
            Pinv=linv(P)
            varied=list(factors)
            varied[corner]=(factors[corner]*generator if corner<2
                             else -generator*factors[corner])
            dP=varied[0]*varied[1]*varied[2]*varied[3]
            dC=(dP+Pinv*dP*Pinv)/2
            u,v=[j for j in range(4) if j not in (p,q)]
            S=solder(base)
            total += orientation(p,q)*(wedge(S[:,u],S[:,v]).T*G2*STAR*biv(dC))[0]
    return sp.factor(total)

def run(write=False):
    check("Y_PROJECTOR", P_PERP**2==P_PERP and P_PERP.rank()==2)
    check("Y_B_DISJOINT", Y*B==sp.zeros(4) and B*Y==sp.zeros(4))

    d,a,b,c=sp.symbols("d a b c", real=True)
    f0,f1,f2,f3=sp.symbols("f0 f1 f2 f3", real=True)
    R=a*GEN[3]+b*GEN[4]+c*GEN[5]
    r2=sp.expand(a*a+b*b+c*c)
    check("GENERAL_ROTATION_CUBIC", sp.expand(R**3+r2*R)==sp.zeros(4))
    CY=cayley_simple(Y,sp.Integer(3),sp.Integer(1))
    CB=cayley_simple(B,sp.Integer(-3),-d)
    CR=cayley_simple(R,r2,sp.Integer(1))
    K=sp.simplify(CY*CB*CR)

    incoming={(0,0,0,0):f0,(0,-1,0,0):f1,(0,0,-1,0):f2,(0,0,0,-1):f3}
    def solder(site):
        return I4+(incoming.get(site,f0)-1)*P_PERP
    def link(site,role):
        if role!=0:
            return I4
        return K if sum(site)%4==0 else I4

    rows=[edge_euler(solder,link,(0,0,0,0),0,GEN[j]) for j in range(3)]

    C1=(-9*a**2*d**4 + 42*a**2*d**2 + 16*a**2
        +9*a*c*d**4 -42*a*c*d**2 +40*a*c
        -9*a*d**4 +84*a*d**2 -96*a
        +9*b**2*d**4 +42*b**2*d**2 -16*b**2
        -27*b*c*d**4 +42*b*c*d**2 -8*b*c
        -45*b*d**4 +84*b*d**2 -32*b
        +18*c**2*d**4 +24*c**2 +72*c*d**4 -128*c
        +54*d**4 +128)
    C2=(9*a**2*d**4 +42*a**2*d**2 -16*a**2
        -27*a*b*d**4 +42*a*b*d**2 -8*a*b
        +45*a*d**4 -84*a*d**2 +32*a
        +18*b**2*d**4 +24*b**2
        -9*b*c*d**4 +42*b*c*d**2 -40*b*c
        -72*b*d**4 +128*b
        -9*c**2*d**4 +42*c**2*d**2 +16*c**2
        -9*c*d**4 +84*c*d**2 -96*c
        +54*d**4 +128)
    C3=(18*a**2*d**4 +24*a**2
        -9*a*b*d**4 +42*a*b*d**2 -40*a*b
        +27*a*c*d**4 -42*a*c*d**2 +8*a*c
        +72*a*d**4 -128*a
        -9*b**2*d**4 +42*b**2*d**2 +16*b**2
        +9*b*d**4 -84*b*d**2 +96*b
        +9*c**2*d**4 +42*c**2*d**2 -16*c**2
        +45*c*d**4 -84*c*d**2 +32*c
        +54*d**4 +128)

    lap=3*f0**2-f1**2-f2**2-f3**2
    s=a-b+c
    multiplier=3*d**4*(s+3)**2+4*(s-4)**2
    lhs=sp.factor(C1*rows[0]+C2*rows[1]+C3*rows[2])
    rhs=sp.factor(-2*(3*d**2+4)/(3*d**2-4)*multiplier*lap)
    check("FULL_SPIN_ROLE0_LAPLACIAN_COMBINATION", sp.factor(lhs-rhs)==0)
    check("MULTIPLIER_SUM_OF_SQUARES",
          sp.expand(multiplier-(3*d**4*(a-b+c+3)**2+4*(a-b+c-4)**2))==0)

    checks=[
        sp.factor(multiplier.subs({b:0,c:0}) -
                  (3*d**4*(a+3)**2+4*(a-4)**2)),
        sp.factor(multiplier.subs({a:0,c:0}) -
                  (3*d**4*(b-3)**2+4*(b+4)**2)),
        sp.factor(multiplier.subs({a:0,b:0}) -
                  (3*d**4*(c+3)**2+4*(c-4)**2)),
    ]
    check("J12_J13_J23_AXIS_REGRESSIONS", checks==[0,0,0])

    cex=4-a+b
    Rex=sp.expand(a*GEN[3]+b*GEN[4]+cex*GEN[5])
    r2ex=sp.expand(a*a+b*b+cex*cex)
    Kex=sp.simplify(CY*cayley_simple(Rex,r2ex,sp.Integer(1)))
    wave=[Kex,I4,linv(Kex),I4]

    fs={}
    def fsite(site):
        key=(site[1],site[2],site[3])
        if key not in fs:
            fs[key]=sp.Symbol("f_"+"_".join(map(str,key)), real=True)
        return fs[key]
    def solder_ex(site):
        return I4+(fsite(site)-1)*P_PERP
    def link_ex(site,role):
        if role!=0:
            return I4
        return wave[sum(site)%4]

    origin=(0,0,0,0)
    exceptional=[]
    for role in (1,2,3):
        for j in (3,4,5):
            exceptional.append(edge_euler(solder_ex,link_ex,origin,role,GEN[j]))

    fm0=fsite(origin)
    fm1=fsite((0,-1,0,0))
    fm2=fsite((0,0,-1,0))
    fm3=fsite((0,0,0,-1))
    vars4=(fm0,fm1,fm2,fm3)
    M=sp.Matrix([[sp.expand(expr).coeff(v) for v in vars4] for expr in exceptional])
    check("EXCEPTIONAL_ROWS_LINEAR", all(sp.Poly(expr,*vars4).total_degree()<=1 for expr in exceptional))
    check("EXCEPTIONAL_TRANSPORT_RANK3", M.rank()==3)
    ns=M.nullspace()
    check("EXCEPTIONAL_KERNEL_IS_CONSTANT_PROFILE",
          len(ns)==1 and ns[0]==sp.Matrix([1,1,1,1]))

    # Hostile phase-order control: keep the same spin factor on phase 2
    # instead of inverting the full phase-0 link.  On the exceptional plane
    # the nine spatial transport rows must remain exactly the same.
    CRex=cayley_simple(Rex,r2ex,sp.Integer(1))
    wave_alt=[Kex,I4,sp.simplify(linv(CY)*CRex),I4]
    def link_alt(site,role):
        if role!=0:
            return I4
        return wave_alt[sum(site)%4]
    exceptional_alt=[]
    for role in (1,2,3):
        for j in (3,4,5):
            exceptional_alt.append(edge_euler(solder_ex,link_alt,origin,role,GEN[j]))
    check("EXCEPTIONAL_PHASE2_SPIN_ORDER_INDEPENDENT",
          exceptional_alt==exceptional)

    result={
        "schema":"a4d-y-full-spin-product-rigidity-v1",
        "terminal":"A4D-Y-FULL-SPIN-PRODUCT-PLANE-RIGIDITY",
        "background":"z=1 product-plane solder S_f=I+(f-1)P_perp",
        "temporal_link":"C_Y(1) C_B(-d) C_R, R=a J12+b J13+c J23",
        "role0_boost_combination":"C1*E_K1+C2*E_K2+C3*E_K3 = -2*(3*d^2+4)/(3*d^2-4) * Mspin * (3*f0^2-f1^2-f2^2-f3^2)",
        "spin_multiplier":"Mspin=3*d^4*(a-b+c+3)^2+4*(a-b+c-4)^2",
        "real_multiplier_zero_locus":"d=0 and a-b+c=4",
        "exceptional_plane_control":"the 9 spatial-role rotation rows are linear in (f0,f1,f2,f3), have rank 3, and kernel span(1,1,1,1)",
        "phase2_spin_convention_control":"the exceptional transport rows are identical for reciprocal [K,I,K^-1,I] and same-spin phase2 C_Y^-1 C_R conventions",
        "conclusion":"for every real d,a,b,c in the B-Cayley chart 3*d^2!=4, stationarity inside this temporal full-SO(3)-spin ansatz forces the product profile f to be spatially constant on a connected periodic carrier",
        "scope_fence":[
            "necessary-row no-go for general spatial-rotation Cayley correction on temporal curved edges at z=1",
            "does not include arbitrary transverse corrections on spatial links",
            "does not prove a uniform nonlinear inverse for the full 136-by-96 joint operator",
            "does not establish either task-level response terminal"
        ]
    }
    if write:
        OUT.write_text(json.dumps(result,indent=2)+"\n")
        print("WROTE",OUT,flush=True)
    elif OUT.exists():
        check("RESULTS_MATCH_PINNED_JSON", result==json.loads(OUT.read_text()))
    print("TERMINAL A4D-Y-FULL-SPIN-PRODUCT-PLANE-RIGIDITY",flush=True)
    return result

if __name__=="__main__":
    import sys
    run("--write" in sys.argv[1:])
