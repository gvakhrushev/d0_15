#!/usr/bin/env python3
"""Exact product-plane rigidity for a general temporal boost at z=1."""
from itertools import combinations
import json
from pathlib import Path
import sympy as sp

OUT=Path(__file__).with_name("a4d_y_full_boost_product_rigidity_results.json")
ETA=sp.diag(1,-1,-1,-1)
I4=sp.eye(4)
PAIRS=list(combinations(range(4),2))
GEN=[]
for p,q in PAIRS:
    X=sp.zeros(4); X[p,q]=1; X[q,p]=-ETA[p,p]*ETA[q,q]; GEN.append(X)
G2=sp.diag(*(ETA[p,p]*ETA[q,q] for p,q in PAIRS))
STAR=sp.zeros(6)
for col,(row,sign) in enumerate([(5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1)]): STAR[row,col]=sign
Y=GEN[3]-GEN[4]+GEN[5]
Pperp=-Y**2/3

def check(name,ok):
    if not ok: raise AssertionError(name)
    print("PASS_"+name,flush=True)
def linv(M): return ETA*M.T*ETA
def wedge(u,v): return sp.Matrix([u[p]*v[q]-u[q]*v[p] for p,q in PAIRS])
def biv(M):
    X=M*ETA; return sp.Matrix([X[p,q] for p,q in PAIRS])
def orientation(p,q):
    seq=[p,q]+[j for j in range(4) if j not in (p,q)]
    return -1 if sum(seq[i]>seq[j] for i,j in PAIRS)%2 else 1
def cayley_simple(G,norm2,a=sp.Integer(1)):
    den=4+norm2*a*a
    return I4+4*a/den*G+2*a*a/den*(G**2)
def DR(P,dP):
    Pi=linv(P); return sp.simplify((dP+Pi*dP*Pi)/2)
def solder(f): return I4+(f-1)*Pperp

f0,f1,f2,f3=sp.symbols("f0 f1 f2 f3", real=True)
fs=[None,f1,f2,f3]
def local_role0_row(K,G):
    Ki=linv(K)
    dC0=DR(K,K*G)
    dCi=DR(Ki,-G*Ki)
    total=sp.Integer(0)
    for s in (1,2,3):
        u,v=[j for j in range(4) if j not in (0,s)]
        A0=wedge(solder(f0)[:,u],solder(f0)[:,v])
        Ai=wedge(solder(fs[s])[:,u],solder(fs[s])[:,v])
        total += orientation(0,s)*((A0.T*G2*STAR*biv(dC0))[0]+(Ai.T*G2*STAR*biv(dCi))[0])
    return sp.factor(total)

def run(write=False):
    u1,u2,u3=sp.symbols("u1 u2 u3", real=True)
    V=u1*GEN[0]+u2*GEN[1]+u3*GEN[2]
    r2=sp.expand(u1*u1+u2*u2+u3*u3)
    check("GENERAL_BOOST_CUBIC",sp.expand(V**3-r2*V)==sp.zeros(4))
    CY=cayley_simple(Y,sp.Integer(3))
    CV=cayley_simple(V,-r2)
    K=sp.simplify(CY*CV)
    rows=[local_role0_row(K,GEN[i]) for i in range(3)]

    P1=(-3*u1**4-u1**3*u2-5*u1**3*u3-u1**2*u2**2-5*u1**2*u3**2-u1*u2**3
        -5*u1*u2**2*u3-u1*u2*u3**2+24*u1*u2-5*u1*u3**3+8*u1*u3
        +2*u2**4-8*u2**2-2*u3**4-24*u3**2-64)
    P2=(-2*u1**4-5*u1**3*u2-5*u1**2*u2**2-u1**2*u2*u3-24*u1**2-5*u1*u2**3
        -5*u1*u2*u3**2+8*u1*u2-3*u2**4-u2**3*u3-u2**2*u3**2-u2*u3**3
        +24*u2*u3+2*u3**4-8*u3**2-64)
    P3=(2*u1**4-u1**3*u3-5*u1**2*u2*u3-u1**2*u3**2-8*u1**2-u1*u2**2*u3
        -u1*u3**3+24*u1*u3-2*u2**4-5*u2**3*u3-5*u2**2*u3**2-24*u2**2
        -5*u2*u3**3+8*u2*u3-3*u3**4-64)
    lap=3*f0**2-f1**2-f2**2-f3**2
    s=u1+u2+u3
    rhs=sp.factor((r2+4)*(s*s*r2+64)/(r2-4)*lap)
    lhs=sp.factor(P1*rows[0]+P2*rows[1]+P3*rows[2])
    check("GENERAL_BOOST_LAPLACIAN_COMBINATION",sp.factor(lhs-rhs)==0)
    check("STRICTLY_POSITIVE_REAL_MULTIPLIER_FORM",
          sp.factor((s*s*r2+64)-((u1+u2+u3)**2*(u1**2+u2**2+u3**2)+64))==0)
    result={
      "schema":"a4d-y-full-boost-product-rigidity-v1",
      "terminal":"A4D-Y-FULL-TEMPORAL-BOOST-PRODUCT-RIGIDITY",
      "background":"z=1 product-plane solder S_f=I+(f-1)P_perp",
      "temporal_link":"C_Y(1) C_V with V=u1*K1+u2*K2+u3*K3",
      "role0_boost_combination":"P1*E_K1+P2*E_K2+P3*E_K3=((r2+4)*(s^2*r2+64)/(r2-4))*(3*f0^2-f1^2-f2^2-f3^2)",
      "definitions":"r2=u1^2+u2^2+u3^2; s=u1+u2+u3",
      "real_multiplier":"strictly nonzero on the real boost Cayley chart r2!=4 because r2+4>0 and s^2*r2+64>=64",
      "conclusion":"every real temporal boost Cayley correction at z=1 forces the product profile f to be spatially constant on a connected periodic carrier",
      "scope_fence":[
        "temporal pure-boost correction only; simultaneous noncommuting boost+rotation factor not classified here",
        "arbitrary transverse corrections on spatial links remain open",
        "no uniform nonlinear full-joint inverse is proved",
        "no task-level response terminal is claimed"
      ]
    }
    if write:
      OUT.write_text(json.dumps(result,indent=2)+"\n")
      print("WROTE",OUT,flush=True)
    elif OUT.exists():
      check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
    print("TERMINAL A4D-Y-FULL-TEMPORAL-BOOST-PRODUCT-RIGIDITY",flush=True)
    return result
if __name__=="__main__":
    import sys
    run("--write" in sys.argv[1:])
