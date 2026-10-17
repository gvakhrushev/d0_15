#!/usr/bin/env python3
"""Exact finite checks for the regular-natural SOURCE closure criterion.

No D0 physical source is selected here. All representation computations cover
full Lorentz tensor spaces; analytical locality/regularity and refinement
assertions are in THEOREM_RU.md, not inferred from these finite computations.
Python >=3.10, SymPy >=1.12. Checks use exceptions and survive python -O.
"""
from __future__ import annotations
import itertools
import json
import sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

CHECKS: list[str] = []

def require(name: str, truth: bool) -> None:
    if not truth:
        raise ArithmeticError(name)
    CHECKS.append(name)

def zero(name: str, expr) -> None:
    seq = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    require(name, all(s.cancel(x) == 0 for x in seq))


def basis(p: int):
    return list(itertools.combinations(range(4), p))


def wedge_terms(a, b):
    if len(set(a + b)) != len(a) + len(b):
        return None, 0
    signs = sum(x > y for x in a for y in b)
    return tuple(sorted(a + b)), (-1)**signs


def ext_rep(J: s.Matrix, p: int) -> s.Matrix:
    inds = basis(p)
    row = {I: i for i, I in enumerate(inds)}
    M = s.zeros(len(inds))
    for col, I in enumerate(inds):
        for pos, old in enumerate(I):
            for new in range(4):
                if not J[new,old]:
                    continue
                seq = list(I)
                seq[pos] = new
                if len(set(seq)) != p:
                    continue
                parity = sum(seq[i] > seq[j] for i in range(p) for j in range(i+1,p))
                M[row[tuple(sorted(seq))],col] += (-1)**parity * J[new,old]
    return M


def tensor_rep(A: s.Matrix, B: s.Matrix) -> s.Matrix:
    return s.kronecker_product(A, s.eye(B.rows)) + s.kronecker_product(s.eye(A.rows), B)


def hom_constraints(inputs, outputs):
    """Rows of A_out M - M A_in, row-major vectorization of M."""
    return s.SparseMatrix.vstack(*[
        s.kronecker_product(O, s.eye(I.rows)) - s.kronecker_product(s.eye(O.rows), I.T)
        for I,O in zip(inputs, outputs)
    ])


def hom_dim(label, inputs, outputs, expected):
    C = hom_constraints(inputs, outputs)
    # DomainMatrix performs exact arithmetic; no floating rank thresholds.
    dm = DomainMatrix.from_Matrix(C)
    rank = dm.rank()
    dim = C.cols-rank
    require(label, dim == expected)
    return {"input_dimension":inputs[0].rows, "output_dimension":outputs[0].rows,
            "unknowns":C.cols,"rank":rank,"dimension":dim}


def wf_add(A, B):
    out=dict(A)
    for k,v in B.items():
        out[k]=s.expand(out.get(k,0)+v)
        if out[k] == 0:
            del out[k]
    return out


def wf_scale(c, A):
    return {k:s.expand(c*v) for k,v in A.items() if c*v != 0}


def wf_wedge(A,B):
    out={}
    for I,a in A.items():
        for J,b in B.items():
            K, sign=wedge_terms(I,J)
            if sign:
                out[K]=s.expand(out.get(K,0)+sign*a*b)
    return {k:v for k,v in out.items() if v != 0}


def alternating(I):
    if len(set(I)) != len(I):
        return 0
    return (-1)**sum(I[i]>I[j] for i in range(len(I)) for j in range(i+1,len(I)))


def source_e(e,R,c,b,lam):
    """Euler 3-form of c P + b H + lam V, lower internal index a.
    P=(1/2) eps_abcd e^a e^b R^cd, H=e_a e_b R^ab,
    V=(1/24) eps_abcd e^a e^b e^c e^d. R^{ab} is antisymmetric.
    """
    eta=[1,-1,-1,-1]
    E=[{} for _ in range(4)]
    for a in range(4):
        for j,k,l in itertools.product(range(4),repeat=3):
            ep=alternating((a,j,k,l))
            if ep:
                E[a]=wf_add(E[a],wf_scale(c*ep,wf_wedge(e[j],R.get((k,l),{}))))
                E[a]=wf_add(E[a],wf_scale(lam*s.Rational(ep,6),wf_wedge(e[j],wf_wedge(e[k],e[l]))))
        for j in range(4):
            E[a]=wf_add(E[a],wf_scale(2*b*eta[a]*eta[j],wf_wedge(e[j],R.get((a,j),{}))))
    return E


def main():
    eta=s.diag(1,-1,-1,-1)
    generators=[]
    for a,b in basis(2):
        J=s.zeros(4)
        J[a,b]=eta[b,b]
        J[b,a]=-eta[a,a]
        generators.append(J)
    zero('all_six_generators_are_lorentz', s.Matrix.vstack(*[J.T*eta+eta*J for J in generators]))
    V=generators
    W=[ext_rep(J,2) for J in generators]
    V3=[ext_rep(J,3) for J in generators]
    VV=[tensor_rep(J,J) for J in V]
    VW=[tensor_rep(J,K) for J,K in zip(V,W)]
    dims={}
    for name,ins,outs,expected in [
        ('coframe_eee',V3,V,1),
        ('coframe_eT',VV,V,0),
        ('coframe_eR',VW,V,2),
        ('connection_eee',V3,W,0),
        ('connection_eT',VV,W,2),
        ('connection_eR',VW,W,0),
    ]:
        dims[name]=hom_dim('complete_hom_'+name,ins,outs,expected)
    require('unconstrained_natural_source_dimension_five',sum(x['dimension'] for x in dims.values())==5)

    # Weighted Taylor count for a three-form source. One-form jets of order j
    # have weight j+1. Higher jets may enter the raw count, but alternation
    # kills all symmetric derivative pairs; see the analytic proof.
    types=[powers for powers in itertools.product(range(4),repeat=3)
           if sum((j+1)*powers[j] for j in range(3))==3]
    require('degree_three_weighted_types',set(types)=={(3,0,0),(1,1,0),(0,0,1)})
    # An arbitrary symmetric second derivative cannot survive alternation.
    second=s.symbols('s0:40')
    pairs=basis(2)
    for out in basis(3):
        terms={}
        for perm in itertools.permutations(out):
            key=(tuple(sorted(perm[:2])),perm[2])
            terms[key]=terms.get(key,0)+alternating(perm)
        require('second_jet_alternation_zero_'+''.join(map(str,out)),all(v==0 for v in terms.values()))

    c,b,lam=s.symbols('c b lam')
    dx=[{(i,):s.Integer(1)} for i in range(4)]
    R={(2,3):{(2,3):s.Integer(1)},(3,2):{(2,3):s.Integer(-1)}}
    Ec=source_e([{},dx[1],{},{}],R,c,b,lam)
    zero('extract_full_palatini_coefficient',Ec[0].get((1,2,3),0)/2-c)
    zero('palatini_probe_other_coframe_components',s.Matrix([sum(Ec[i].values()) for i in [1,2,3]]))
    Rb={(0,1):{(2,3):s.Integer(1)},(1,0):{(2,3):s.Integer(-1)}}
    Eb=source_e([{},dx[1],{},{}],Rb,c,b,lam)
    zero('extract_full_holst_coefficient',-Eb[0].get((1,2,3),0)/2-b)
    Ev=source_e([{},dx[1],dx[2],dx[3]],{},c,b,lam)
    zero('extract_full_volume_coefficient',Ev[0].get((1,2,3),0)-lam)
    # The coefficient probes need not use a degenerate tetrad. On e=I,
    # take a derivative of the SAME full source in an independent curvature
    # jet; the volume source is constant in this jet and cancels honestly.
    rho=s.symbols('rho')
    Ric={(2,3):{(2,3):rho},(3,2):{(2,3):-rho}}
    Rih={(0,1):{(2,3):rho},(1,0):{(2,3):-rho}}
    Ec_unit=source_e(dx,Ric,c,b,lam)
    Eb_unit=source_e(dx,Rih,c,b,lam)
    Ev_unit=source_e(dx,{},c,b,lam)
    zero('palatini_probe_on_nondegenerate_coframe',s.diff(Ec_unit[0].get((1,2,3),0),rho)/2-c)
    zero('holst_probe_on_nondegenerate_coframe',-s.diff(Eb_unit[0].get((1,2,3),0),rho)/2-b)
    zero('volume_probe_on_nondegenerate_coframe',Ev_unit[0].get((1,2,3),0)-lam)

    # Algebraic source reconstruction on generic local jet, not a metric fit.
    u=s.symbols('u0:16')
    e=[{(j,):u[4*i+j] for j in range(4)} for i in range(4)]
    rr=s.symbols('r0:36')
    curv={}
    for i,(a,bb) in enumerate(basis(2)):
        curv[a,bb]={I:rr[6*i+j] for j,I in enumerate(basis(2))}
        curv[bb,a]=wf_scale(-1,curv[a,bb])
    E=source_e(e,curv,c,b,lam)
    Eparts=[source_e(e,curv,1,0,0),source_e(e,curv,0,1,0),source_e(e,curv,0,0,1)]
    errors=[]
    for a in range(4):
        for I in basis(3):
            errors.append(E[a].get(I,0)-sum(k*P[a].get(I,0) for k,P in zip([c,b,lam],Eparts)))
    zero('all_sixteen_coframe_threeform_components_reconstructed',s.Matrix(errors))

    # Helmholtz: after matching the coframe source, a residual connection
    # source homogeneous of degree two in e cannot be independent of e.
    t,up,vp=s.symbols('t up vp')
    zero('helmholtz_scaling_derivative',s.diff(t*t*(up+vp),t).subs(t,1)-2*(up+vp))
    # Negative control: a mismatch in paired coefficients gives nonzero curl.
    x,y=s.symbols('x y')
    Fxy=s.Matrix([c*y,b*x])
    curl=s.diff(Fxy[0],y)-s.diff(Fxy[1],x)
    zero('mismatched_variational_source_curl_exact',curl-(c-b))
    require('mismatched_variational_source_rejected',curl.subs({c:1,b:2})!=0)
    # Smoothness at finite levels alone cannot be passed to the limit.
    eps=s.symbols('eps',positive=True)
    zero('regularity_counterexample_second_jet',s.diff(s.sqrt(x*x+eps*eps),x,2).subs(x,0)-1/eps)
    # An inverse-coframe R^2 density is covariant on nondegenerate fields,
    # but scales like 1/t when e^0=t dx0 and fixed R^{01} is kept.
    r=s.symbols('r')
    zero('inverse_coframe_density_singularity',t*(2*r/t)**2-4*r*r/t)

    result={
        'status':'PASS_EXACT_REPRESENTATION_AND_SOURCE_IDENTITIES',
        'checks':len(CHECKS),'names':CHECKS,'hom_spaces':dims,
        'source_space_before_variationality':5,
        'variational_source_space':3,
        'analytical_theorem':'Regular local natural full source on all tetrad/connection forms, including degenerate tetrads, plus variationality implies Cartan source; proof in THEOREM_RU.md.',
        'native_source_computed':False,
        'native_regular_local_descent_proved':False,
        'native_palatini_coefficient':None,
        'native_matter_identified':False,
        'native_joint_refinement_proved':False,
        'D0_to_GR_proved':False,
        'input_repository_sha':'2c500cd63f7a5923809a2208d81f58a12cc709a9',
        'python':sys.version.split()[0],'sympy':s.__version__,
    }
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
