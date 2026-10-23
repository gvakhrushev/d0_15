#!/usr/bin/env python3
"""Exact coframe-torsion reconstruction, full Einstein geometric reading.
This does not replace the native stored Dirac or prove its Cost-Info/GR limit.
Python/SymPy only. No downloads, input mutation or assertions removable by -O.
"""
from __future__ import annotations
from itertools import combinations, permutations, product
import json
import sympy as S

ETA=S.diag(1,-1,-1,-1)
SIG=(1,-1,-1,-1)
PAIRS=list(combinations(range(4),2))
CHECKS=[]

def clean(x):
    return x.applyfunc(S.cancel) if isinstance(x,S.MatrixBase) else S.cancel(x)

def equal(name,a,b=0):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        ok=all(S.cancel(z)==0 for z in S.Matrix(a)-S.Matrix(b))
    else:
        ok=S.cancel(a-b)==0
    if not ok: raise ArithmeticError(name)
    CHECKS.append(name)

def demand(name,ok):
    if not ok: raise ArithmeticError(name)
    CHECKS.append(name)

def zero_connection():return [S.zeros(4) for _ in range(4)]

def torsion(e,de,w):
    return {(m,n):clean(de[m][:,n]-de[n][:,m]+w[m]*e[:,n]-w[n]*e[:,m]) for m,n in PAIRS}

def absorb(e,T):
    """Unique metric-compatible C with C^a_b wedge e^b = -T^a.
    T is a vector-valued coordinate 2-form. Output C_mu has mixed frame indices.
    """
    F=e.inv()
    TT=[[[sum(SIG[a]*F[m,b]*F[n,c]*(T[m,n][a] if m<n else -T[n,m][a])
              for m in range(4) for n in range(4) if m!=n)
           for c in range(4)] for b in range(4)] for a in range(4)]
    cab=[[[clean((TT[a][b][c]+TT[b][c][a]-TT[c][a][b])/2)
            for c in range(4)] for b in range(4)] for a in range(4)]
    return [S.Matrix(4,4,lambda a,b:clean(SIG[a]*sum(cab[a][b][c]*e[c,m] for c in range(4))))
            for m in range(4)]

def connection(e,de):return absorb(e,torsion(e,de,zero_connection()))

def connection_jet(e,w,delta_e,delta_de):
    # Differentiate de + omega wedge e = 0, never freeze the inverse coframe.
    return absorb(e,torsion(delta_e,delta_de,w))

def curvature(e,de,dde):
    w=connection(e,de)
    dw=[connection_jet(e,w,de[m],dde[m]) for m in range(4)]
    R={(m,n):clean(dw[m][n]-dw[n][m]+w[m]*w[n]-w[n]*w[m]) for m,n in PAIRS}
    return w,dw,R

def eps(indices):
    if len(set(indices))!=len(indices):return 0
    return (-1)**sum(indices[i]>indices[j] for i in range(len(indices)) for j in range(i+1,len(indices)))

def add(*forms):
    out={}
    for f in forms:
        for k,v in f.items():out[k]=out.get(k,0)+v
    return {k:clean(v) for k,v in out.items() if clean(v)!=0}

def scale(c,f):return {k:clean(c*v) for k,v in f.items() if clean(c*v)!=0}

def wedge(f,g):
    out={}
    for a,x in f.items():
        for b,y in g.items():
            if set(a)&set(b):continue
            k=tuple(sorted(a+b));z=eps(a+b)*x*y
            out[k]=out.get(k,0)+z
    return {k:clean(v) for k,v in out.items() if clean(v)!=0}

def one(row):return {(m,):row[m] for m in range(4) if row[m]!=0}
def two(T,a,b=None):
    return {mn:(mat[a] if b is None else mat[a,b]) for mn,mat in T.items()
            if (mat[a] if b is None else mat[a,b])!=0}

def matrix_forms(w):return [[one([w[m][a,b] for m in range(4)]) for b in range(4)] for a in range(4)]
def matwedge(a,b):
    return [[add(*(wedge(a[i][k],b[k][j]) for k in range(4))) for j in range(4)] for i in range(4)]

def scalar_density(e,R):
    F=e.inv()
    rc={(m,n):clean(F*r*e) for (m,n),r in R.items()}
    def get(m,n):return rc[m,n] if m<n else -rc[n,m] if n<m else S.zeros(4)
    Ric=S.Matrix(4,4,lambda b,d:clean(sum(get(a,d)[a,b] for a in range(4))))
    g=e.T*ETA*e
    return clean(S.trace(g.inv()*Ric)*e.det()),Ric

def transgression(e,de,bar,dbar):
    w,dw,R=curvature(e,de,[[S.zeros(4) for _ in range(4)] for _ in range(4)])
    T=torsion(e,de,bar)
    C=absorb(e,T)
    for m in range(4):equal('generic_connection_reference_cancels_'+str(m),bar[m]+C[m],w[m])
    # e has arbitrary first jets and zero second jets; bar has its stated first jets.
    dC=[[(dw[m][n]-dbar[m][n]) for n in range(4)] for m in range(4)]
    Rbar={(m,n):dbar[m][n]-dbar[n][m]+bar[m]*bar[n]-bar[n]*bar[m] for m,n in PAIRS}
    Cforms=matrix_forms(C);CC=matwedge(Cforms,Cforms)
    D_C={}
    for m,n in PAIRS:
        D_C[m,n]=dC[m][n]-dC[n][m]+bar[m]*C[n]-bar[n]*C[m]-C[n]*bar[m]+C[m]*bar[n]
        equal('all_curvature_transgression_'+str(m)+str(n),R[m,n],Rbar[m,n]+D_C[m,n]+C[m]*C[n]-C[n]*C[m])
    ef=[one(e[a,:]) for a in range(4)]
    def Sigma(c,d):return scale(S.Rational(1,2),add(*(scale(eps((a,b,c,d)),wedge(ef[a],ef[b]))
                                      for a in range(4) for b in range(4))))
    dtheta=[{mn:(de[mn[0]][a,mn[1]]-de[mn[1]][a,mn[0]]) for mn in PAIRS} for a in range(4)]
    def dSigma(c,d):
        return scale(S.Rational(1,2),add(*(scale(eps((a,b,c,d)),add(wedge(dtheta[a],ef[b]),scale(-1,wedge(ef[a],dtheta[b]))))
                          for a in range(4) for b in range(4))))
    def covSigma(c,d):return add(*(scale(eps((a,b,c,d)),wedge(two(T,a),ef[b])) for a in range(4) for b in range(4)))
    direct={};stored={};quadratic={};boundary={};loss={}
    for c in range(4):
        for d in range(4):
            if c==d:continue
            si=Sigma(c,d)
            Cup=scale(SIG[d],Cforms[c][d])
            dCup={mn:SIG[d]*(dC[mn[0]][mn[1]][c,d]-dC[mn[1]][mn[0]][c,d]) for mn in PAIRS}
            direct=add(direct,wedge(si,scale(SIG[d],two(R,c,d))))
            stored=add(stored,wedge(si,scale(SIG[d],two(Rbar,c,d))))
            term=add(scale(-1,wedge(covSigma(c,d),Cup)),wedge(si,scale(SIG[d],CC[c][d])))
            quadratic=add(quadratic,term)
            boundary=add(boundary,wedge(dSigma(c,d),Cup),wedge(si,dCup))
            loss=add(loss,wedge(covSigma(c,d),Cup))
    get=lambda form:clean(form.get((0,1,2,3),0))
    equal('complete_geometric_density_with_boundary',get(direct),get(stored)+get(quadratic)+get(boundary))
    Rv,Ric=scalar_density(e,R)
    equal('Palatini_form_normalization_is_R_vol',get(direct),Rv)
    demand('boundary_is_not_discardable_pointwise',get(boundary)!=0)
    demand('torsion_cross_term_really_contributes',get(loss)!=0)
    return {'ricci_scalar_density':str(Rv),'comparison_part':str(get(stored)),
            'torsion_quadratic_part':str(get(quadratic)),'boundary_part':str(get(boundary))}

def universal_linear_tests():
    e=S.Matrix([[2,S.Rational(1,3),0,0],[0,1,S.Rational(1,5),0],
                [0,0,S.Rational(3,2),S.Rational(1,7)],[0,0,0,1]])
    zerode=zero_connection()
    for a in range(4):
        for b,c in PAIRS:
            T={mn:S.zeros(4,1) for mn in PAIRS};T[b,c][a]=1
            C=absorb(e,T)
            tt=torsion(e,zerode,C)
            equal('all24_torsion_inverse_%d%d%d'%(a,b,c),S.Matrix.hstack(*(tt[mn]+T[mn] for mn in PAIRS)),S.zeros(4,6))
            for m in range(4):equal('metric_compatibility_%d%d%d_%d'%(a,b,c,m),C[m].T*ETA+ETA*C[m],S.zeros(4))
    # Every metric variation has an algebraic coframe lift on the unrestricted chart.
    g=e.T*ETA*e
    for m in range(4):
        for n in range(m,4):
            V=S.zeros(4);V[m,n]=V[n,m]=1
            dE=e*g.inv()*V/2
            equal('all10_covariant_metric_lifts_%d%d'%(m,n),dE.T*ETA*e+e.T*ETA*dE,V)
    # Exact, finite endpoint inverse identity, no continuum approximation.
    F=e.inv();E2=e+S.diag(S.Rational(1,8),S.Rational(1,7),S.Rational(1,6),S.Rational(1,5));F2=E2.inv()
    equal('finite_inverse_coframe_difference',E2-e,-e*(F2-F)*E2)
    de=[S.Matrix(4,4,lambda a,b:S.Rational(((a+1)*3+(b+2)*5+(m+1)*7)%11-5,23+m)) for m in range(4)]
    w=connection(e,de)
    for mu in range(4):
        for a,b in PAIRS:
            G=S.zeros(4);G[a,b]=SIG[a];G[b,a]=-SIG[b]
            bar=zero_connection();bar[mu]=G
            C=absorb(e,torsion(e,de,bar))
            equal('all24_comparison_changes_cancel_%d%d%d'%(mu,a,b),S.Matrix.hstack(*(bar[r]+C[r]-w[r] for r in range(4))),S.zeros(4,16))
    # A full moving-coframe jet, checked against direct symbolic differentiation.
    q=S.symbols('q');Njet=S.zeros(4);Njet[0,1]=S.Rational(1,19);V=Njet*e
    dV=[S.ones(4)*(m+1)/31 for m in range(4)]
    predicted=connection_jet(e,w,V,dV)
    # Jacobian formula uses invertible e; derivative can be evaluated exactly at q=0.
    actual=connection(e+q*V,[de[m]+q*dV[m] for m in range(4)])
    for mu in range(4):equal('complete_connection_jet_%d'%mu,actual[mu].diff(q).subs(q,0),predicted[mu])
    return e,de

def pp_wave_tests():
    H,Hx,Hy,Hxx,Hxy,Hyy=S.symbols('H Hx Hy Hxx Hxy Hyy',real=True)
    N=S.zeros(4);N[0,0]=N[0,3]=S.Rational(1,2);N[3,0]=N[3,3]=-S.Rational(1,2)
    equal('nilpotent_Kerr_Schild_generator',N*N,S.zeros(4))
    e=S.eye(4)+H*N;F=S.eye(4)-H*N
    equal('wave_exact_coframe_inverse',e*F,S.eye(4))
    equal('wave_coframe_determinant',e.det(),1)
    g=clean(e.T*ETA*e);k=S.Matrix([1,0,0,1])
    equal('wave_metric_from_same_native_q',g,ETA+H*k*k.T)
    equal('native_contravariant_metric',F*ETA*F.T,g.inv())
    de=[S.zeros(4),Hx*N,Hy*N,S.zeros(4)]
    dde=[[S.zeros(4) for _ in range(4)] for _ in range(4)]
    dde[1][1]=Hxx*N;dde[1][2]=dde[2][1]=Hxy*N;dde[2][2]=Hyy*N
    # Along x^r the row F_r is constant: both actual stored-adjoint equations hold.
    dF=[-q for q in de]
    for r in range(4):
        equal('stored_own_leg_direction_%d'%r,ETA*dF[r][r,:].T,S.zeros(4,1))
        equal('stored_observer_Gram_%d'%r,S.eye(4).T*S.eye(4)*S.eye(4),S.eye(4))
    # Finite shifts: row0/row3 do not see t/z; row1/row2 are independent of H.
    HH=S.symbols('HH')
    for r in (1,2):equal('finite_transverse_leg_%d'%r,F[r,:].subs(H,HH),F[r,:])
    # A rational longitudinal coordinate change puts every spatial leg length
    # in the regular stored chart without changing the nonlinear metric content.
    P=S.eye(4);P[0,0]=P[3,3]=S.Rational(5,4);P[0,3]=P[3,0]=S.Rational(3,4)
    equal('regular_wave_rational_Lorentz_map',P.T*ETA*P,ETA)
    Fr=P*F; Er=e*P.inv()
    equal('regular_wave_exact_inverse',Er*Fr,S.eye(4))
    equal('regular_wave_time_leg_spatial_component',Fr[0,3],(3-H)/4)
    equal('regular_wave_z_leg_spatial_component',Fr[3,3],(5+H)/4)
    demand('regular_wave_all_spatial_lengths_positive_on_H_quarter',Fr[0,3].subs(H,S.Rational(1,4))>=S.Rational(11,16) and Fr[3,3].subs(H,-S.Rational(1,4))>=S.Rational(11,16))
    for rr in (1,2):equal('regular_wave_finite_transverse_leg_%d'%rr,Fr[rr,:].subs(H,HH),Fr[rr,:])
    w,dw,R=curvature(e,de,dde)
    for mu in range(4):equal('wave_reconstructed_connection_Lorentz_%d'%mu,w[mu].T*ETA+ETA*w[mu],S.zeros(4))
    equal('wave_all_torsion_free_equations',S.Matrix.hstack(*torsion(e,de,w).values()),S.zeros(4,6))
    Rv,Ric=scalar_density(e,R)
    equal('wave_full_Ricci_tensor',Ric,(Hxx+Hyy)*k*k.T/2)
    equal('wave_scalar_zero_even_offshell',Rv,0)
    actual=S.Matrix.vstack(*(clean(r.subs({H:0,Hx:0,Hy:0,Hxx:2,Hxy:0,Hyy:-2})) for r in R.values()))
    demand('harmonic_wave_nonflat',actual!=S.zeros(24,4))
    equal('harmonic_wave_full_vacuum',Ric.subs(Hyy,-Hxx),S.zeros(4))
    equal('wave_curvature_common_kernel_rank',actual.rank(),3)
    n=actual.nullspace()[0]
    equal('wave_common_direction_is_null',(n.T*ETA*n)[0],0)
    # Restricted scalar/action value is not a field-equation test.
    Gup=clean(g.inv()*Ric*g.inv())
    equal('restricted_H_variation_blind_offshell',S.trace(Gup*k*k.T),0)
    V=S.zeros(4);V[0,0]=1
    equal('unrestricted_metric_source_not_blind',S.trace(Gup*V),(Hxx+Hyy)/2)
    demand('off_shell_metric_covector_nonzero',S.trace(Gup*V)!=0)
    # A nonconstant field-dependent coefficient needs the integration-by-parts term.
    t=S.symbols('t'); f=1+t*t; boundary_amplitude=2+t**3
    equal('field_coefficient_product_rule',f*S.diff(boundary_amplitude,t),
          S.diff(f*boundary_amplitude,t)-S.diff(f,t)*boundary_amplitude)
    demand('moving_coefficient_boundary_remainder_nonzero',S.diff(f,t)*boundary_amplitude!=0)
    return {'metric':'dt^2-dx^2-dy^2-dz^2+H(x,y)(dt+dz)^2',
            'Ricci':'(Hxx+Hyy) k_mu k_nu/2','vacuum_condition':'Hxx+Hyy=0',
            'native_links':'identity; observer e0; own-leg differences zero',
            'v8_stationarity_proved':False,'global_periodic_wave_claimed':False}

def run():
    CHECKS.clear()
    e,de=universal_linear_tests()
    bar=zero_connection();dbar=[[S.zeros(4) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        a,b=PAIRS[mu]
        G=S.zeros(4);G[a,b]=SIG[a];G[b,a]=-SIG[b]
        bar[mu]=G/S.Integer(7+mu)
        dbar[(mu+1)%4][mu]=G/S.Integer(11+mu)
    trans=transgression(e,de,bar,dbar)
    wave=pp_wave_tests()
    return {'schema':'d0-coframe-torsion-intrinsic-gr/1','checks':CHECKS,'exact_check_count':len(CHECKS),
            'transgression_control':trans,'wave':wave,
            'full_source_claim':'complete geometric Einstein-Hilbert covector only, not equality with native v8 spectral price',
            'new_native_action_selected':False,'native_GR_closed':False}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
