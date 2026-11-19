"""Exact polynomial identity and physical matrix-element check on the Brinkmann section."""
from functools import reduce
from itertools import combinations, product
import json

import sympy as sy


I = sy.eye(4)
Z = sy.zeros(4)
eta = sy.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
pairs = tuple(combinations(range(4), 2))
nu, hprofile, k, l, m, n = sy.symbols("nu H k l m n", real=True)


def unit(i, j):
    return I[:,i] * I[:,j].T


def wedge(u, v):
    return (u*v.T-v*u.T)*eta


def sharp(U):
    return eta*U.T*eta


def logslot(U):
    return (U-sharp(U))/2


def comm(a,b):
    return a*b-b*a


def trace(a):
    return sy.trace(a)


def nonzero(a):
    return sy.expand(a) != 0


def equality(a, b, where):
    diff = sy.expand(a-b)
    if diff != 0:
        raise ValueError((where, diff))


N2, N3 = unit(1,2)+unit(2,0), unit(1,3)+unit(3,0)
G = [wedge(I[:,i],I[:,j]) for i,j in pairs]
K = k*N2+l*N3
M = m*N2+n*N3


def expnull(A):
    return I+A+A*A/2


U,V = expnull(K),expnull(M)
frame = I + hprofile*unit(1,0)/2
ref = nu*eta
actual = ref*frame.inv().T


def linear_biv(r,s,v):
    return (wedge(ref[:,r],ref[:,s]) + wedge(v[:,r]-ref[:,r],ref[:,s])
            + wedge(ref[:,r], v[:,s]-ref[:,s]))


def proposed(r,s,v,links):
    a,b,c,d = links
    B = wedge(ref[:,r],ref[:,s])
    if r == 0 and s in (2,3):
        dB = linear_biv(r,s,v) - B
        return -(trace(B*(a+b-c-d))+trace(dB*(logslot(a)-logslot(c))))/2
    if (r,s) == (0,1):
        transported = B+comm(B,logslot(a))
        return -(trace(B*(a*sharp(c)-I))+trace(transported*(b-I))-trace(B*(d-I)))/2
    return -trace(linear_biv(r,s,v)*(a+b-c-d))/2


def direct_density_jet(r,s,v,dv,links,ds):
    # The native null surrogate and literal star density have equal 40 jets here.
    # Independently use the original cofactor, its determinant and antisymmetric curvature.
    P=links[0]*links[1]*sharp(links[2])*sharp(links[3])
    word=[links[0],links[1],sharp(links[2]),sharp(links[3])]
    delta=[ds[0],ds[1],sharp(ds[2]),sharp(ds[3])]
    dP=sum((reduce(lambda x,y:x*y,word[:i]+[delta[i]]+word[i+1:]) for i in range(4)),Z)
    B=wedge(v[:,r],v[:,s])
    dB=wedge(dv[:,r],v[:,s])+wedge(v[:,r],dv[:,s])
    det=v.det()
    ddet=det*trace(v.inv()*dv)
    # Multiply the density by nu² H_mesh² (H_mesh cancels) as in the owner.
    R=logslot(P)
    return nu**4*(trace(dB*R+B*logslot(dP))/det - trace(B*R)*ddet/det**2)/2


def section_links(r,s):
    if r != 0:
        return [I,I,I,I]
    return [U,I,U if s == 1 else V,I]


def audit_face_jets():
    counts = {"coframe": 0, "edge": 0}
    for r,s in pairs:
        links = section_links(r,s)
        equality(proposed(r,s,actual,links),0,(r,s,"value"))
        # At most quadratic in affine amplitude coordinates: coefficient via central difference.
        for i,j in product(range(4), repeat=2):
            dv=unit(i,j)
            cand=(proposed(r,s,actual+dv,links)-proposed(r,s,actual-dv,links))/2
            expected=direct_density_jet(r,s,actual,dv,links,[Z]*4)
            equality(cand,expected,(r,s,"coframe",i,j))
            counts["coframe"]+=1
        for a,Y in product(range(4),G):
            tangent=[Z]*4
            tangent[a]=Y*links[a]
            lp,lm=links[:],links[:]
            lp[a]=links[a]+tangent[a]
            lm[a]=links[a]-tangent[a]
            cand=(proposed(r,s,actual,lp)-proposed(r,s,actual,lm))/2
            expected=direct_density_jet(r,s,actual,Z,links,tangent)
            equality(cand,expected,(r,s,"link",a))
            counts["edge"]+=1
    return counts


def degree_and_coherence():
    # Use independent formal entries in each address. A common scaling variable
    # certifies the maximum total degree for each of the three formula patterns.
    t=sy.Symbol("s")
    v=sy.Matrix(4,4,lambda i,j:(i+2)*(j-3)+int(i==j))
    mats=[sy.Matrix(4,4,lambda i,j:(i-j)*(a+1)+i*a+j+int(i==j)) for a in range(4)]
    if any(sy.degree(proposed(r,s,t*v,[t*m for m in mats]).expand(),t)>2 for r,s in pairs):
        raise ValueError("degree exceeded")
    # Neighbour z+e2 in the 02 face, independent of z even after v-invariance.
    # Compare the u0 transverse derivative as its distant u-link varies on the section.
    dv=unit(0,0)
    vals=[]
    for kn in (0,1):
        links=[I,I,expnull(kn*N2),I]
        vals.append(sy.expand((proposed(0,2,ref+dv,links)-proposed(0,2,ref-dv,links))/2))
    witness=sy.simplify((vals[1]-vals[0])/nu)
    if not nonzero(witness):
        raise ValueError("dephased witness vanished")
    return str(witness)


def born_operator_audit():
    # Every symbol is the amplitude at one real address, times sqrt(D).  The
    # constant is recovered from a genuine link vacuum entry, including its 1/2.
    import runpy
    from pathlib import Path
    import numpy as np

    previous = Path(__file__).resolve().parents[2]/"round85/assembly/check_paired_source.py"
    source = runpy.run_path(str(previous))
    coordinates = sy.symbols("x0:80")
    local_nu = sy.Rational(1,2)
    variable_frame = sy.Matrix(4,4,lambda i,j:coordinates[4*j+i])
    raw_links = [sy.Matrix(4,4,lambda i,j:2*coordinates[16+16*a+4*i+j]) for a in range(4)]
    # Real full Julia fixture on the positive proper-Lorentz chart.
    rng = np.random.default_rng(419)
    columns = .39*np.eye(4)+rng.normal(scale=.025,size=(4,4))
    links = []
    for j,plane in enumerate([(0,2),(1,3),(0,1),(2,3)]):
        half=(.09+.02*j)*source["gen"](*plane)/2
        links.append(np.linalg.solve(np.eye(4)-half,np.eye(4)+half))
    blocks = [np.tensordot(columns[:,i],source["CREATORS"],axes=1) for i in range(4)]
    blocks.extend(source["exterior"](U)/2 for U in links)
    D=32*len(blocks)
    wave=np.stack([source["julia"](raw).T for raw in blocks])/np.sqrt(D)
    if abs(np.vdot(wave,wave)-1)>2e-12:
        raise ValueError("Julia state normalization")
    selected=[wave[r,0,1<<a] for r,a in product(range(4),repeat=2)]
    selected.extend(wave[4+a,1<<j,1<<i] for a,i,j in product(range(4),repeat=3))
    selected.append(wave[4,0,0])
    selected=np.array(selected)
    counts=[]
    for r,s in pairs:
        expression=proposed(r,s,variable_frame,raw_links).subs(nu,local_nu)
        poly=sy.Poly(expression,*coordinates)
        if poly.total_degree()>2:
            raise ValueError(("degree exceeds one Born pair",r,s))
        matrix=np.zeros((81,81))
        for powers,coeff in poly.terms():
            indices=[j for j,deg in enumerate(powers) for _ in range(deg)]
            unused=2-len(indices)
            i,j=(indices+[80]*unused)
            weight=D*(2**unused)*float(coeff)/2
            matrix[i,j]+=weight
            matrix[j,i]+=weight
        born=np.einsum("i,ij,j->",selected,matrix,selected)
        target=float(proposed(r,s,sy.Matrix(columns),list(map(sy.Matrix,links))).subs(nu,local_nu))
        if abs(born-target)>2e-11:
            raise ValueError(("physical one-Choi matrix element",r,s,born,target))
        counts.append(len(poly.terms()))
    return counts



if __name__=="__main__":
    counts=audit_face_jets()
    witness=degree_and_coherence()
    print(json.dumps({"face_values":6,"symbolic_coframe_jets":counts["coframe"],
                      "symbolic_link_occurrence_jets":counts["edge"],
                      "independent_null_parameters":["H","k","l","m","n","nu"],
                      "separated_address_mixed_jet_divided_by_nu":witness,
                      "exact_polynomial_terms_per_face":born_operator_audit(),
                      "geometry_choi_copies_on_owned_first_jet":1,
                      "GR_closed":False}, indent=2))
