#!/usr/bin/env python3
"""D0 original true based temporal plaquette: global noncommuting SO chain.

Exact rational proper Lorentz Cayley samples, both fixed-endpoint
nonlinear holonomy constraint and complete 6N x 6(N-1) linear compatibility.
Works only on the native temporal-gauge/spatially homogeneous subcarrier,
not full 24-link K913 Book action and not an existence proof of GR.
"""
from __future__ import annotations
import json
import sympy as S

I=S.eye(4)
eta=S.diag(1,-1,-1,-1)
E=lambda i,j:S.eye(4)[:,i]*S.eye(4)[j,:]
G=[]
for j in (1,2,3):G.append(E(0,j)+E(j,0))
for i,j in ((1,2),(1,3),(2,3)):G.append(E(i,j)-E(j,i))
assert all(g.T*eta+eta*g==S.zeros(4) for g in G)

def cayley(A,t):
    B=I-t*A/2
    return (I+t*A/2)*B.inv()

def proper(U):
    return U.T*eta*U==eta and U.det()==1

def ad(U,X):return U*X*U.inv()

def coord(X):return S.Matrix([X[0,1],X[0,2],X[0,3],X[1,2],X[1,3],X[2,3]])

def from_coord(t):return sum((t[i]*G[i] for i in range(6)),S.zeros(4))

def adjacency(Ps,initial):
    nodes=[initial]
    for P in Ps:nodes.append(P*nodes[-1])
    return nodes

def product(Ps):
    res=I
    for a in Ps:res=a*res
    return res

def check():
    B,R=G[0],G[3]
    assert B*R-R*B!=S.zeros(4)
    # Four actual native links at 3 consecutive full time intervals.
    U=[I,
       cayley(B,S.Rational(1,10))*cayley(R,S.Rational(1,13)),
       cayley(R,S.Rational(1,17))*cayley(B,S.Rational(2,11)),
       cayley(B,S.Rational(1,19))*cayley(R,S.Rational(3,23))]
    N=len(U)-1
    assert all(proper(X) for X in U)
    P=[U[j+1]*U[j].inv() for j in range(N)]
    assert all(proper(X) for X in P)
    assert adjacency(P,U[0])==U
    assert product(P)==U[-1]*U[0].inv()
    # Native fixed-collar interior fields may change, but only if the
    # new PLACQUETTES obey the exact full product constraint.
    eps=S.Rational(1,1000)
    changed=[U[0],cayley(B+R,eps)*U[1],cayley(B-R,eps)*U[2],U[3]]
    target=[changed[j+1]*changed[j].inv() for j in range(N)]
    assert all(proper(X) for X in target)
    assert product(target)==product(P)
    assert adjacency(target,U[0])==changed
    assert all(X==Y for X,Y in zip(adjacency(target,U[0]),changed))
    # Changing just ONE physical plaquette violates BOTH fixed endpoints.
    bad=P[:];bad[1]=cayley(R,eps)*bad[1]
    assert product(bad)!=product(P)
    assert adjacency(bad,U[0])[-1]!=U[-1]
    # TRUE exact linearized based plaquette current:
    # c_j=dP_j P_j^-1 = Z_{j+1}-Ad(P_j)Z_j
    Z=[S.zeros(4),B+2*R,-2*B+R,S.zeros(4)]
    C=[Z[j+1]-ad(P[j],Z[j]) for j in range(N)]
    for j in range(N):
        assert (Z[j+1]*P[j]-P[j]*Z[j])*P[j].inv()==C[j]
        assert C[j].T*eta+eta*C[j]==S.zeros(4)
    Zrecover=[S.zeros(4)]
    for j in range(N):Zrecover.append(C[j]+ad(P[j],Zrecover[-1]))
    assert Zrecover==Z
    assert Zrecover[-1]==S.zeros(4)
    # EXACT nonlocal compatibility / codim-six constraint: weighted sum
    # covariantly transported C_j to final endpoint must be zero.
    obstruction=S.zeros(4)
    for j in range(N):
        suffix=product(P[j+1:])
        obstruction+=ad(suffix,C[j])
    assert obstruction==S.zeros(4)
    c_bad=C[:];c_bad[0]=c_bad[0]+B
    badob=S.zeros(4)
    for j in range(N):badob+=ad(product(P[j+1:]),c_bad[j])
    assert badob!=S.zeros(4)
    # Full exact rational 6N-by-6(N-1) linear map, not sitewise Jacobians.
    D=S.zeros(6*N,6*(N-1))
    for j in range(N):
        adblock=S.Matrix.hstack(*[coord(ad(P[j],basis)) for basis in G])
        for k in range(6):
            if j>0:
                for a in range(6):D[6*j+a,6*(j-1)+k]-=adblock[a,k]
        if j+1<N:
            for k in range(6):D[6*j+k,6*j+k]+=1
    # Last line deliberately builds all predecessor rows, no silent cut.
    assert D.rank()==6*(N-1),(D.rank(),N)
    Cvec=S.Matrix.vstack(*[coord(c) for c in C])
    Zvec=S.Matrix.vstack(*[coord(zv) for zv in Z[1:-1]])
    assert D*Zvec==Cvec
    badvec=S.Matrix.vstack(*[coord(c) for c in c_bad])
    assert D.row_join(badvec).rank()==D.rank()+1
    # Absolute first-order temporal link variations from original based-face:
    # left perturbation h^2 Z_j yields source delta(P)/h²=Z_next P-P Z.
    # An isolated interior change has a genuine O(1) curvature spike
    # after the h^-2 normalizing factor, whereas a smooth Z_j has O(h).
    hh=S.symbols('h',real=True)
    F=S.Matrix([[0,1],[-2,0]])
    Y=S.Matrix([[1,2],[3,4]])
    DY=S.Matrix([[2,3],[5,7]])
    Ph=S.eye(2)+hh*F
    isolated=-Ph*Y
    coherent=(Y+hh*DY)*Ph-Ph*Y
    assert isolated.subs(hh,0)==-Y
    assert S.expand(coherent-hh*(DY+Y*F-F*Y)-hh**2*DY*F)==S.zeros(2)
    return {
        'status':'PASS_ORIGINAL_NONCOMMUTING_TEMPORAL_BASEDFACE',
        'native_true_lorentz_eta':'diag(1,-1,-1,-1)',
        'noncommuting_based_plaquette_count':N,
        'actual_full_link_nodes':N+1,
        'exact_Lorentz_infinitesimal_rank':D.rank(),
        'actual_linearized_plaquette_rows':D.rows,
        'global_fixed_collar_cokernel_dimension':D.rows-D.rank(),
        'exact_nonlinear_reconstruction':True,
        'exact_noncommuting_ends_product_constraint':True,
        'exact_global_lie_algebra_compatibility':True,
        'single_plaquette_bad_target_rejected':True,
        'one_site_normalized_spike':'O(1)',
        'coherent_true_three_slice_curvature':'O(h)',
        'science_scope':{
            'original_temporal_gauge_sector_only':True,
            'full_24_link_system_solved':False,
            'all_16_coframe_equations_solved':False,
            'two_real_CAR_material_temporal_block_reduced_by_separate_owner':True,
            'Book03_full_native_action_selected':False,
            'GR_closed':False}}

if __name__=='__main__':print(json.dumps(check(),indent=2))
