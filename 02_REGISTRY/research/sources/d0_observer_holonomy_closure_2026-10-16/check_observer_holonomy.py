#!/usr/bin/env python3
"""Exact controls for the observer-preservation boundary and retained-path lift.
No native action, old root, torsion-free limit, or GR closure is assumed proved.
"""
from __future__ import annotations
from itertools import combinations
import json
import sympy as s

eta=s.diag(1,-1,-1,-1)
e0=s.eye(4)[:,0]
checks=[]

def reduced(z):
    return s.simplify(s.expand(z))

def equal(name,x,y=0):
    if isinstance(x,s.MatrixBase) or isinstance(y,s.MatrixBase):
        ok=all(reduced(z)==0 for z in s.Matrix(x)-s.Matrix(y))
    else:
        ok=reduced(x-y)==0
    if not ok:
        raise ArithmeticError(name)
    checks.append(name)

def require(name,ok):
    if not ok:
        raise ArithmeticError(name)
    checks.append(name)

def boost(axis,t):
    c=(1+t*t)/(1-t*t);z=2*t/(1-t*t)
    B=s.eye(4);B[0,0]=B[axis,axis]=c;B[0,axis]=B[axis,0]=z
    return B

def rotation(i,j,t):
    c=(1-t*t)/(1+t*t);z=2*t/(1+t*t)
    R=s.eye(4);R[i,i]=R[j,j]=c;R[i,j]=-z;R[j,i]=z
    return R

def h(n):
    return -eta+2*eta*n*n.T*eta

def whitener(n):
    # Input is a future unit timelike vector, not four unconstrained coordinates.
    n0=n[0];v=n[1:4,0]
    return s.Matrix([[n0]]).row_join(-v.T).col_join(
        (-v).row_join(s.eye(3)+v*v.T/(1+n0)))

def exterior(A):
    E=s.zeros(16)
    groups=[[tuple(c) for c in combinations(range(4),k)] for k in range(5)]
    for group in groups:
        for a in group:
            ia=sum(1<<x for x in a)
            for b in group:
                ib=sum(1<<x for x in b)
                E[ia,ib]=A.extract(a,b).det() if a else 1
    return E

def finite_lock():
    Bx=boost(1,s.Rational(1,5)); By=boost(2,s.Rational(-1,6)); Bz=boost(3,s.Rational(1,7))
    nx=Bx*e0;ny=By*e0;nz=Bz*e0
    Rxy=rotation(1,2,s.Rational(1,4));Ryz=rotation(2,3,s.Rational(1,5));Rzx=rotation(1,3,s.Rational(-1,6))
    Axy=Bx*Rxy*By.inv();Ayz=By*Ryz*Bz.inv();Azx=Bz*Rzx*Bx.inv()
    for j,(A,ns,nt) in enumerate(((Axy,nx,ny),(Ayz,ny,nz),(Azx,nz,nx))):
        equal('edge_Lorentz_'+str(j),A.T*eta*A,eta)
        equal('edge_positive_isometry_'+str(j),A.T*h(ns)*A,h(nt))
        equal('edge_transports_observer_'+str(j),A*nt,ns)
        O=whitener(ns)*A*whitener(nt).inv()
        equal('rest_frame_fixed_time_'+str(j),O*e0,e0)
        equal('rest_frame_orthogonal_'+str(j),O.T*O,s.eye(4))
    H=Axy*Ayz*Azx
    equal('loop_transports_same_observer',H*nx,nx)
    require('nonzero_rotation_holonomy_not_ruled_out',H!=s.eye(4))
    # A general Lorentz edge fails ONLY the additional positive-metric equality.
    A=boost(1,s.Rational(1,10))*rotation(2,3,s.Rational(1,8))
    equal('general_edge_still_Lorentz',A.T*eta*A,eta)
    v=A.inv()*nx
    defect=A.T*h(nx)*A-h(ny)
    equal('rank_one_exact_metric_defect',defect,2*eta*(v*v.T-ny*ny.T)*eta)
    require('general_edge_not_silently_in_locked_domain',defect!=s.zeros(4))
    # Arbitrarily moving site observers alone only produce a pure-gauge boost curl.
    kr,ks=s.symbols('kr ks')
    nu=s.Matrix(s.symbols('nu0:3'))
    equal('linear_observer_boost_curl_zero',ks*(kr*nu)-kr*(ks*nu),s.zeros(3,1))

def observer_history():
    A1=boost(1,s.Rational(1,5));A2=boost(2,s.Rational(1,6))
    n0=e0;n1=A1*n0;n2=A2*n1
    for j,(A,n,np) in enumerate(((A1,n0,n1),(A2,n1,n2),(A2*A1,n0,n2))):
        equal('transported_observer_normalized_'+str(j),(np.T*eta*np)[0],1)
        equal('moving_positive_fibre_'+str(j),A.T*h(np)*A,h(n))
        L=whitener(np); equal('canonical_whitening_'+str(j),L.T*L,h(np))
        equal('whitening_sends_observer_to_rest_'+str(j),L*np,e0)
    R1=whitener(n1)*A1*whitener(n0).inv()
    R2=whitener(n2)*A2*whitener(n1).inv()
    R12=whitener(n2)*A2*A1*whitener(n0).inv()
    equal('groupoid_exact_composition',R2*R1,R12)
    equal('groupoid_full_link_reconstruction',whitener(n2).inv()*R12*whitener(n0),A2*A1)
    equal('groupoid_unitary_comparison',R12.T*R12,s.eye(4))
    require('transport_does_not_reset_observer',n2!=n0)
    require('spatial_Wigner_rotation_retained',R12!=s.eye(4))
    EA=exterior(A2*A1);Eh0=exterior(h(n0));Eh2=exterior(h(n2))
    equal('full16_grade_dimensions',sum(len(list(combinations(range(4),k))) for k in range(5)),16)
    equal('full16_moving_pairing_isometry',EA.T*Eh2*EA,Eh0)
    equal('full16_exterior_functor',exterior(A2)*exterior(A1),EA)
    equal('full16_comparison_isometry',exterior(R12).T*exterior(R12),s.eye(16))
    # Moving endpoint derivative is required, not optional detector decoration.
    t=s.symbols('t',real=True)
    A=boost(1,t);n=A*e0
    residual=A.T*h(n)*A-s.eye(4)
    equal('moving_observer_complete_family',residual,s.zeros(4))
    equal('moving_observer_full_jet',residual.diff(t).subs(t,s.Rational(1,8)),s.zeros(4))
    frozen=h(n.subs(t,s.Rational(1,8)))
    require('frozen_observer_jet_is_wrong',(A.T*frozen*A).diff(t).subs(t,s.Rational(1,8))!=s.zeros(4))
    # Pure boost with rapidity eta: all16 singular values are retained.
    B=boost(1,s.Rational(1,10));Q=exterior(B).T*exterior(B)
    c=B[0,0]
    equal('owned_full16_boost_trace',s.trace(Q),16*c*c)
    require('return_without_reset_is_detectable',s.trace(Q)>16)
    equal('unit_det_does_not_make_unitary',Q.det(),1)
    require('determinant_only_reading_misses_boost',Q!=s.eye(16))

def connection_split():
    # Exact algebraic test at a point with dn=0; derivative terms are retained in the proof.
    def K(v):return v*e0.T*eta-e0*v.T*eta
    a=s.Matrix([0,1,2,0]);b=s.Matrix([0,-1,1,3])
    U=s.zeros(4);U[1,2]=1;U[2,1]=-1
    V=s.zeros(4);V[2,3]=2;V[3,2]=-2
    om0=U+K(a);om1=V+K(b)
    equal('boost_complement_is_Lorentz',K(a).T*eta+eta*K(a),s.zeros(4))
    equal('boost_complement_transports_time',K(a)*e0,a)
    equal('observer_preserving_remainder',(om0-K(a))*e0,s.zeros(4,1))
    comm=lambda x,y:x*y-y*x
    equal('all_curvature_terms_retained',comm(om0,om1),comm(U,V)+comm(U,K(b))-comm(V,K(a))+comm(K(a),K(b)))
    equal('boost_curvature_read_by_observer',comm(om0,om1)*e0,U*b-V*a)
    require('dropping_boost_complement_changes_curvature',comm(om0,om1)!=comm(U,V))
    # Values/tangential jets of a reduced action cannot determine normal equations.
    q,k=s.symbols('q k',real=True)
    S0=q*q+q**4
    S1=S0+q*k+k*k/2
    S2=S0+2*q*k+3*k*k/2
    equal('same_reduced_action',S1.subs(k,0),S2.subs(k,0))
    equal('same_all_tangential_differentials',s.diff(S1,q).subs(k,0),s.diff(S2,q).subs(k,0))
    require('different_missing_boost_equations',s.diff(S1,k).subs(k,0)!=s.diff(S2,k).subs(k,0))

def vacuum_control():
    # Vacuum pp-wave from the prior density/Palatini example, at an ordinary point.
    u,v,x,y=s.symbols('u v x y',real=True)
    coords=[u,v,x,y]
    g=s.Matrix([[x*x-y*y,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    gi=g.inv()
    Ch=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,b],coords[c])+s.diff(g[d,c],coords[b])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
           for c in range(4)] for b in range(4)] for a in range(4)]
    R=[[[[s.simplify(s.diff(Ch[a][b][d],coords[c])-s.diff(Ch[a][b][c],coords[d])+
                  sum(Ch[a][e][c]*Ch[e][b][d]-Ch[a][e][d]*Ch[e][b][c] for e in range(4)))
          for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    Ric=s.Matrix(4,4,lambda b,d:sum(R[a][b][a][d] for a in range(4)))
    equal('ppwave_is_exact_vacuum',Ric,s.zeros(4))
    curvs=[s.Matrix(4,4,lambda a,b:R[a][b][c][d]).subs({x:0,y:0}) for c,d in combinations(range(4),2)]
    H=s.Matrix.vstack(*curvs)
    equal('common_curvature_kernel_rank',H.rank(),3)
    kernel=H.nullspace()
    equal('common_curvature_kernel_is_one_dimensional',len(kernel),1)
    g0=g.subs({x:0,y:0})
    equal('only_fixed_curvature_direction_is_null',(kernel[0].T*g0*kernel[0])[0],0)
    require('vacuum_wave_not_flat',H!=s.zeros(24,4))
    # Complete 3D curvature identity: zero Ricci forces zero Riemann.
    rr=s.Matrix([[s.Symbol('r00'),s.Symbol('r01'),s.Symbol('r02')],
                 [s.Symbol('r01'),s.Symbol('r11'),s.Symbol('r12')],
                 [s.Symbol('r02'),s.Symbol('r12'),s.Symbol('r22')]])
    delta=lambda i,j:int(i==j)
    def R3(i,j,k,l):
        return delta(i,k)*rr[j,l]-delta(i,l)*rr[j,k]-delta(j,k)*rr[i,l]+delta(j,l)*rr[i,k]-s.trace(rr)*(delta(i,k)*delta(j,l)-delta(i,l)*delta(j,k))/2
    equal('three_dimensional_Riemann_Ricci_reconstruction',s.Matrix(3,3,lambda j,l:sum(R3(i,j,i,l) for i in range(3))),rr)
    zeros={a:0 for a in rr.free_symbols}
    equal('three_dimensional_vacuum_has_no_curvature',sum(R3(i,j,k,l).subs(zeros)**2 for i,j in combinations(range(3),2) for k,l in combinations(range(3),2)),0)


def run():
    checks.clear();finite_lock();observer_history();connection_split();vacuum_control()
    return {'schema':'d0-observer-holonomy-closure/1','exact_checks':len(checks),
        'checks':checks,
        'input_SOURCE':'d39d205b0cc6e7d8ce743e5698850731ed46b717',
        'new_claim':'rank-independent parallel-observer constraint; conditional torsion-free four-dimensional Ricci-flat limit is locally flat',
        'constructive_route':'retain path-dependent observer and full Lorentz link; canonical boost complement',
        'v8_action_modified':False,'matter_rank_escape_overrides_lock':False,
        'native_path_lift_admission_proved':False,'general_native_GR_closed':False,
        'old_research_replayed':False}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
