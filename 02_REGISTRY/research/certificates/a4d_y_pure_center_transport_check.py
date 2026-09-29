#!/usr/bin/env python3
"""Exact pure-Y nonlinear center transport at z≈1.

Research-only certificate for PR #310.

For the four-phase Y Cayley ansatz on the standard solder, with an independent
real amplitude attached to every even-phase Role-0 link, this checker proves:

1. the unrestricted 16-row solder Euler map for independent temporal-face
   Y-curvature scalars (r1,r2,r3) has rank 2 and kernel span(1,1,1);
2. for every phase p and spatial role s=1,2,3, the literal boost-K_s edge Euler
   row factors as
       ± 8 (a-b)(a+b)/((4+3a^2)(4+3b^2)),
   where a,b are the two even-site Y amplitudes linked by that row;
3. the transport moves e_s-e_0 and e_s+e_0 generate the complete even-sum
   sublattice of Z^4 (index 2).

Hence on a connected periodic L=4m carrier, any pure-Y stationary amplitude
remaining in a fixed-sign neighborhood of z=1 is constant. This does not
exclude cancellation by transverse/non-Y connection corrections.
"""
from itertools import combinations
import math
import sympy as sp

ETA = sp.diag(1,-1,-1,-1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4),2))

GEN=[]
for a,b in PAIRS:
    X=sp.zeros(4)
    X[a,b]=1
    X[b,a]=-ETA[a,a]*ETA[b,b]
    GEN.append(X)

G2=sp.diag(*(ETA[a,a]*ETA[b,b] for a,b in PAIRS))
STAR=sp.zeros(6)
for col,(row,sign) in enumerate([(5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1)]):
    STAR[row,col]=sign

Y=GEN[3]-GEN[4]+GEN[5]

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name)

def linv(M):
    return ETA*M.T*ETA

def wedge(u,v):
    return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])

def biv(M):
    X=M*ETA
    return sp.Matrix([X[a,b] for a,b in PAIRS])

def orientation(a,b):
    seq=[a,b]+[j for j in range(4) if j not in (a,b)]
    inv=sum(seq[i]>seq[j] for i,j in PAIRS)
    return (-1)**inv

def cayley(z):
    return sp.simplify((I4-z*Y/2).inv()*(I4+z*Y/2))

bY=biv(Y)
basis=[I4[:,r] for r in range(4)]
M=sp.zeros(16,3)
for role in range(4):
    for row in range(4):
        out=4*role+row
        direction=I4[:,row]
        for col,s in enumerate((1,2,3)):
            u,v=[j for j in range(4) if j not in (0,s)]
            darea=sp.zeros(6,1)
            if role==u:
                darea += wedge(direction,basis[v])
            if role==v:
                darea += wedge(basis[u],direction)
            M[out,col]=sp.expand(
                orientation(0,s)*(darea.T*G2*STAR*bY)[0]
            )

check("Y_FACE_METRIC_MAP_RANK2", M.rank()==2)
ns=M.nullspace()
check("Y_FACE_METRIC_KERNEL_DIAGONAL",
      len(ns)==1 and ns[0]==sp.Matrix([1,1,1]))

def shift(x,r,step=1):
    y=list(x); y[r]+=step; return tuple(y)

def phase(x):
    return sum(x)%4

for p in range(4):
    for role in (1,2,3):
        values={}
        def amp(x):
            x=tuple(x)
            if x not in values:
                values[x]=sp.Symbol("z_"+"_".join(map(str,x)), real=True)
            return values[x]

        def link(x,r):
            if r!=0:
                return I4
            ph=phase(x)
            if ph==0:
                return cayley(amp(x))
            if ph==2:
                return linv(cayley(amp(x)))
            return I4

        site=(0,p,0,0)
        generator=GEN[role-1]
        total=sp.Integer(0)
        for r,s in PAIRS:
            if role==r:
                corners=[(site,0),(shift(site,s,-1),2)]
            elif role==s:
                corners=[(shift(site,r,-1),1),(site,3)]
            else:
                continue
            for base,corner in corners:
                places=[
                    (base,r,False),
                    (shift(base,r),s,False),
                    (shift(base,s),r,True),
                    (base,s,True),
                ]
                factors=[linv(link(x,q)) if inv else link(x,q)
                         for x,q,inv in places]
                P=factors[0]*factors[1]*factors[2]*factors[3]
                Pinv=linv(P)
                varied=list(factors)
                varied[corner]=(factors[corner]*generator if corner<2
                                 else -generator*factors[corner])
                dP=varied[0]*varied[1]*varied[2]*varied[3]
                dC=(dP+Pinv*dP*Pinv)/2
                u,v=[j for j in range(4) if j not in (r,s)]
                area=wedge(I4[:,u],I4[:,v])
                total += orientation(r,s)*(area.T*G2*STAR*biv(dC))[0]

        expr=sp.factor(total)
        syms=sorted(expr.free_symbols,key=str)
        check(f"PHASE{p}_ROLE{role}_USES_TWO_EVEN_AMPLITUDES", len(syms)==2)
        a,b=sp.symbols("a b", real=True)
        renamed=sp.factor(expr.subs({syms[0]:a,syms[1]:b}))
        target=sp.factor(8*(a-b)*(a+b)/((4+3*a*a)*(4+3*b*b)))
        check(f"PHASE{p}_ROLE{role}_EXACT_DIFFERENCE_FACTOR",
              sp.factor(renamed-target)==0 or sp.factor(renamed+target)==0)

e=[sp.eye(4)[:,j] for j in range(4)]
moves=[]
for s in (1,2,3):
    moves += [e[s]-e[0], e[s]+e[0]]
G=sp.Matrix.hstack(*moves)
check("TRANSPORT_MOVE_RANK4", G.rank()==4)

minors=[]
for cols in combinations(range(6),4):
    d=abs(int(G[:,cols].det()))
    if d:
        minors.append(d)
index=0
for d in minors:
    index=math.gcd(index,d)
check("TRANSPORT_LATTICE_INDEX2", index==2)
check("ALL_TRANSPORT_MOVES_HAVE_EVEN_COORDINATE_SUM",
      all(sum(int(v) for v in G[:,j])%2==0 for j in range(G.cols)))

print("EXACT_METRIC_MAP", M.tolist())
print("TRANSPORT_LATTICE_INDEX", index)
print("TERMINAL A4D-Y-PURE-CENTER-NONLINEAR-TRANSPORT-RIGIDITY")
print("SCOPE: pure-Y connection ansatz near fixed-sign z=1; transverse/non-Y corrections remain open.")
