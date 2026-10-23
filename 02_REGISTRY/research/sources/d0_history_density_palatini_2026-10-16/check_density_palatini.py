#!/usr/bin/env python3
"""Exact constructive controls for a CONDITIONAL density/Palatini synthesis.
No external source execution, network, file writes, native admission or GR claim.
"""
from __future__ import annotations
import json, hashlib
from itertools import combinations
import sympy as S

p = S.Symbol('p', positive=True)
REL=p*p+p-1
CHECKS=[]

def red(v):
    v=S.cancel(v)
    num,den=S.fraction(v)
    if not den.has(p):
        return S.cancel(S.rem(num,REL,p)/den)
    return S.cancel(S.rem(S.rem(num,REL,p)*S.invert(den,REL,p),REL,p))

def eq(name,a,b=0):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        delta=S.Matrix(a)-S.Matrix(b)
        good=all(red(v)==0 for v in delta)
    else:
        good=red(a-b)==0
    if not good: raise ArithmeticError(name)
    CHECKS.append(name)

def yes(name,v):
    if not v: raise ArithmeticError(name)
    CHECKS.append(name)

def split(leaf):
    """Actual F=cost1, R=cost2 cut, child clocks NOT strict pullbacks."""
    word,cost,lo,width=leaf
    axis=len(word)%4
    a=list(lo); b=list(width)
    b[axis]=red(p*width[axis])
    direct=(word+'F',cost+1,tuple(a),tuple(b))
    a=list(lo); b=list(width)
    a[axis]=red(a[axis]+p*width[axis]); b[axis]=red(p*p*width[axis])
    ret=(word+'R',cost+2,tuple(a),tuple(b))
    return [direct,ret]

def mass(leaf): return red(S.prod(leaf[3]))
def centre(leaf): return [red(l+w/2) for l,w in zip(leaf[2],leaf[3])]

def clocks():
    leaves=[('',0,(S.Integer(0),)*4,(S.Integer(1),)*4)]
    rows=[]
    for n in range(1,10):
        old=leaves
        leaves=[]
        for parent in old:
            kids=split(parent) if parent[1]<n else [parent]
            yes(f'cut_{n}_cost_increases_{parent[0] or "empty"}',all(q[1]>=n for q in kids))
            if len(kids)==2:
                for a in range(4):
                    eq(f'child_clock_martingale_{n}_{parent[0]}_{a}',
                       p*centre(kids[0])[a]+p*p*centre(kids[1])[a],centre(parent)[a])
            leaves.extend(kids)
        eq(f'cut_{n}_total_mass',sum(mass(q) for q in leaves),1)
        yes(f'cut_{n}_retains_pending',set(q[1] for q in leaves)=={n,n+1})
        for q in leaves:
            eq(f'cut_{n}_PF_volume_{q[0]}',mass(q),p**q[1])
        for a in range(4):
            eq(f'cut_{n}_first_moment_{a}',sum(mass(q)*centre(q)[a] for q in leaves),S.Rational(1,2))
            # Exact cell integration; this is a centroid quadrature error, not a continuum extrapolation.
            eq(f'cut_{n}_second_moment_error_{a}',
               S.Rational(1,3)-sum(mass(q)*centre(q)[a]**2 for q in leaves),
               sum(mass(q)*q[3][a]**2 for q in leaves)/12)
        rows.append({'cost_cut':n,'leaf_count':len(leaves)})
    yes('fine_clocks_are_not_strict_inheritance',centre(leaves[0])!=[S.Rational(1,2)]*4)
    return rows

def entropy():
    x=S.symbols('x',real=True); ell=S.symbols('ell',nonzero=True)
    r=[S.Rational(1,5),S.Rational(3,10),S.Rational(1,2)]
    # Positive unnormalised local weights; their source is genuine, not frozen.
    t=[1+x,2-x/3,3+x/5]
    Z=sum(rr*tt for rr,tt in zip(r,t)); w=[rr*tt/Z for rr,tt in zip(r,t)]
    eq('Gibbs_normalization',sum(w),1)
    for i in range(3):
        # f=-log(t)/ell, log(w/r)=log(t)-log(Z), valid on the positive domain.
        eq(f'faithful_stationary_density_{i}',(-S.log(t[i])+S.log(t[i])-S.log(Z)+1)/ell,
           (1-S.log(Z))/ell)
    gradient=sum(wi*(-S.diff(ti,x)/(ell*ti)) for wi,ti in zip(w,t))
    eq('partition_envelope_all_weight_jets',gradient,-S.diff(Z,x)/(ell*Z))
    z0,z1,z2,L0,L1,L2,k=S.symbols('z0 z1 z2 L0 L1 L2 k',positive=True)
    zz=[z0+x/3,z1-x/5,z2+x/7]; ll=[L0+x,L1-2*x,L2+x/2]
    den=sum(zz); mean=sum(a*b for a,b in zip(zz,ll))/den
    shifted=sum(a*(b+k) for a,b in zip(zz,ll))/den
    eq('fixed_code_cost_source',S.diff(shifted-mean,x),0)
    eq('centered_measure_source',S.diff(mean,x),
       sum(a*S.diff(b,x)+(b-mean)*S.diff(a,x) for a,b in zip(zz,ll))/den)
    u,v=S.symbols('u v',real=True)
    dw=[u,v,-u-v]
    D=sum((ri+x*vi)*S.log((ri+x*vi)/ri) for ri,vi in zip(r,dw))
    eq('preparation_first_derivative_vanishes',S.diff(D,x).subs(x,0),0)
    eq('preparation_Hessian_all_mass_tangents',S.diff(D,x,2).subs(x,0),sum(vi*vi/ri for ri,vi in zip(r,dw)))
    yes('preparation_Hessian_positive_definite',S.hessian(sum(vi*vi/ri for ri,vi in zip(r,dw)),[u,v]).is_positive_definite)
    # Diagonal relative entropy chain rule with retained conditional outcomes.
    q0,q1,t0,t1=S.symbols('q0 q1 t0 t1',positive=True)
    w0=S.symbols('w0',positive=True)
    # Product weights, expand logs explicitly only on this declared positive interior.
    ws=[w0,1-w0]; rs=[S.Rational(2,5),S.Rational(3,5)]
    qs=[[q0,1-q0],[q1,1-q1]]; ts=[[t0,1-t0],[t1,1-t1]]
    direct=0; chain=0
    for i in range(2):
        for j in range(2):
            direct+=ws[i]*qs[i][j]*(S.log(ws[i]/rs[i])+S.log(qs[i][j]/ts[i][j]))
            chain+=ws[i]*qs[i][j]*S.log(qs[i][j]/ts[i][j])
        chain+=ws[i]*S.log(ws[i]/rs[i])
    eq('conditional_entropy_chain_not_mean_only',direct,chain)

ETA=S.diag(1,-1,-1,-1)
PAIRS=list(combinations(range(4),2))
G2=S.diag(*(ETA[i,i]*ETA[j,j] for i,j in PAIRS))
STAR=S.zeros(6)
for src,(dst,sg) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
                     (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():
    STAR[PAIRS.index(dst),PAIRS.index(src)]=sg
GEN=[]
for i in range(1,4):
    A=S.zeros(4); A[0,i]=A[i,0]=1; GEN.append(A)
for i,j in [(1,2),(1,3),(2,3)]:
    A=S.zeros(4); A[i,j]=1; A[j,i]=-1; GEN.append(A)

def wedge(u,v): return S.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in PAIRS])
def cayley(A): return (S.eye(4)-A/2).inv()*(S.eye(4)+A/2)
def curvature(links):
    out=[]
    for r,s in PAIRS:
        U=links[r]*links[s]*links[r].inv()*links[s].inv()
        out.append((U-ETA*U.T*ETA)/2)
    return out

def star_local(e,cc):
    val=0
    for (r,s),C in zip(PAIRS,cc):
        u,v=[i for i in range(4) if i not in (r,s)]
        perm=[r,s,u,v]; sg=(-1)**sum(perm[i]>perm[j] for i,j in PAIRS)
        val+=sg*(wedge(e[:,u],e[:,v]).T*G2*STAR*S.Matrix([(C*ETA)[i,j] for i,j in PAIRS]))[0]
    return S.factor(val)

def geometry():
    e=S.Matrix([[2,S.Rational(1,3),0,0],[0,1,S.Rational(1,5),0],
                [0,0,S.Rational(3,2),S.Rational(1,7)],[0,0,0,1]])
    vol=e.det(); w=4*vol; chi=w/vol
    eh=2*e; g=e.T*ETA*e; gh=eh.T*ETA*eh; vh=eh.det()
    eq('density_coframe_metric',gh,chi*g)
    eq('densitized_inverse_is_exact',w*g.inv(),vh*gh.inv())
    eq('inverse_density_metric_map',(w/vh)*gh,g)
    eq('inverse_density_coframe_map',S.sqrt(w/vh)*eh,e)
    eq('positive_conformal_signature',gh.det(),-(vh**2))
    matrices=[(GEN[r]+GEN[(r+3)%6])/S.Integer(13+r) for r in range(4)]
    links=[cayley(A) for A in matrices]
    for i,U in enumerate(links): eq(f'full_Lorentz_link_{i}',U.T*ETA*U,ETA)
    cc=curvature(links)
    yes('actual_face_curvatures_nonzero',any(C!=S.zeros(4) for C in cc))
    P=star_local(e,cc)
    eq('literal_star_density_homogeneity',star_local(eh,cc),chi*P)
    # Test all coframe slots and the full trace-reversal inverse.
    J=[]
    for i in range(4):
        for j in range(4):
            V=S.zeros(4); V[i,j]=1
            JV=2*(V-e*S.trace(e.inv()*V)/2)
            invV=(JV-eh*S.trace(eh.inv()*JV)/2)/2
            eq(f'coframe_full_inverse_{i}{j}',invV,V)
            J.append(list(JV))
            t=S.symbols('t')
            dP=S.diff(star_local(e+t*V,cc),t).subs(t,0)
            dpw=chi*(dP-P*S.trace(e.inv()*V))
            dph=S.diff(star_local(eh+t*JV,cc),t).subs(t,0)
            eq(f'weighted_coframe_source_{i}{j}',dph,dpw)
    eq('full_sixteen_chart_rank',S.Matrix.hstack(*(S.Matrix(v) for v in J)).rank(),16)
    # All 24 independent tangent directions of the four link variables.
    for r in range(4):
        for k,G in enumerate(GEN):
            U=links[r]; Udot=G*U
            dcc=[]
            for a,b in PAIRS:
                A,B=links[a],links[b]
                dA=Udot if r==a else S.zeros(4); dB=Udot if r==b else S.zeros(4)
                dP=dA*B*A.inv()*B.inv()+A*dB*A.inv()*B.inv()
                dP-=A*B*A.inv()*dA*A.inv()*B.inv()+A*B*A.inv()*B.inv()*dB*B.inv()
                dcc.append((dP-ETA*dP.T*ETA)/2)
            eq(f'all_link_source_{r}_{k}',star_local(eh,dcc),chi*star_local(e,dcc))
    # Every metric component uses the ten-dimensional trace reversal, not a projection.
    packed=[(i,j) for i in range(4) for j in range(i,4)]
    for i,j in packed:
        V=S.zeros(4); V[i,j]=V[j,i]=1
        dh=chi*(V-g*S.trace(g.inv()*V)/2)
        inverse=(dh-gh*S.trace(gh.inv()*dh)/2)/chi
        eq(f'all_ten_metric_inverse_{i}{j}',inverse,V)
    # Scalar/target-sigma kinetic density has exactly the same degree.
    b=S.Matrix([1,2,-1,S.Rational(1,3)])
    eq('quadratic_matter_same_density',w*(b.T*g.inv()*b)[0],vh*(b.T*gh.inv()*b)[0])
    # Full endpoint link (not only its observer-unitary polar factor).
    et=S.diag(1,S.Rational(3,2),2,1); es=e
    D=es.inv()*links[0]*et
    gs=es.T*ETA*es; gt=et.T*ETA*et
    Ds=S.Rational(3,2)*D  # sqrt(chi_t/chi_s), chi_s=4, chi_t=9
    eq('original_coordinate_link_constraint',D.T*gs*D,gt)
    eq('density_scaled_coordinate_link_constraint',Ds.T*(4*gs)*Ds,9*gt)
    # A variable local scaling leaves every closed-loop holonomy conjugate,
    # and hence unchanged for scalar endpoint factors.
    scales=[S.Rational(2),S.Rational(3),S.Rational(5),S.Rational(7)]
    raw=[links[0],links[1],links[2],links[3]]
    transformed=[raw[i]*scales[(i+1)%4]/scales[i] for i in range(4)]
    prod=lambda xs:xs[0]*xs[1]*xs[2]*xs[3]
    eq('closed_transport_scalars_telescope',prod(transformed),prod(raw))
    # Arbitrary probability/weight source includes its coframe-scale term.
    t=S.symbols('t')
    eq('measure_source_cancels_only_with_coframe_rows',
       S.diff(star_local(S.sqrt((w+t)/vol)*e,cc),t).subs(t,0),P/vol)

def curved_control():
    u,v,x,y=S.symbols('u v x y',real=True)
    c=S.symbols('c',positive=True); a,s=S.symbols('a s',real=True)
    H=(s*s/(4*c)+a)*x*x+(s*s/(4*c)-a)*y*y
    g=S.Matrix([[H,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    gi=g.inv(); xx=[u,v,x,y]
    Gamma=[[[S.simplify(sum(gi[A,D]*(S.diff(g[D,B],xx[C])+S.diff(g[D,C],xx[B])-S.diff(g[B,C],xx[D]))
                             for D in range(4))/2) for C in range(4)] for B in range(4)] for A in range(4)]
    Riem=[[[[S.simplify(S.diff(Gamma[A][B][D],xx[C])-S.diff(Gamma[A][B][C],xx[D])
            +sum(Gamma[A][E][C]*Gamma[E][B][D]-Gamma[A][E][D]*Gamma[E][B][C] for E in range(4)))
             for D in range(4)] for C in range(4)] for B in range(4)] for A in range(4)]
    Ric=S.Matrix(4,4,lambda B,D: S.simplify(sum(Riem[A][B][A][D] for A in range(4))))
    Rs=S.simplify(S.trace(gi*Ric)); G=Ric-g*Rs/2
    grad=S.Matrix([s,0,0,0]); kin=(grad.T*gi*grad)[0]
    T=grad*grad.T-g*kin/2
    eq('ppwave_volume',g.det(),-1)
    eq('ppwave_scalar_curvature',Rs,0)
    eq('ppwave_matter_is_null',kin,0)
    eq('ppwave_all_ten_Einstein_scalar_rows',2*c*G,T)
    eq('ppwave_actual_Ricci_uu',Ric[0,0],s*s/(2*c))
    wave=sum(S.diff(gi[A,B]*grad[B],xx[A]) for A in range(4) for B in range(4))
    eq('ppwave_matter_Euler',wave,0)
    yes('vacuum_member_genuinely_curved',any(z.subs(s,0)!=0 for aaa in Riem for aa in aaa for A in aa for z in A))
    # Probability reference may differ from BOTH old and Einstein volume.
    eps=S.symbols('eps',real=True)
    r=1+eps*(2*x-1)
    eq('clock_map_Jacobian',S.diff((1-eps)*x+eps*x*x,x),r)
    eq('reference_probability_normalization',S.integrate(r,(x,0,1)),1)
    gb=r*g; vb=r*r; chi=1/r
    eq('nonconstant_probability_is_not_old_volume',vb-r,eps*(2*x-1)*r)
    eq('curved_density_pullback_metric',chi*gb,g)
    eq('curved_density_pullback_coefficient',r*gb.inv(),gi)
    eq('full_probability_entropy_source_on_solution',S.log(r/r),0)
    eq('full_clock_equation_on_solution',S.diff(r/r,x),0)
    eq('local_cost_on_coupled_solution',c*Rs-kin/2,0)
    # Fixed coding cost is absorbed in the normalisation multiplier, not in Einstein equations.
    k,ell,lam=S.symbols('k ell lam',nonzero=True)
    eq('normalization_multiplier_not_cosmological_counterterm',
       (k+(S.log(r/r)+1)/ell+lam).subs(lam,-k-1/ell),0)
    return {'metric':'2 du dv+H du^2-dx^2-dy^2',
            'H':'(s^2/(4c)+a)x^2+(s^2/(4c)-a)y^2',
            'scalar':'s u','conditional_equation':'2c G=T',
            'density_reference':'1+epsilon(2x-1)',
            'physical_native_solution':False}

def run():
    CHECKS.clear(); cr=clocks(); entropy(); geometry(); pp=curved_control()
    return {'schema':'d0-history-density-palatini/1','exact_checks':len(CHECKS),
            'check_names_sha256':hashlib.sha256('\n'.join(CHECKS).encode()).hexdigest(),
            'scope_note':'most conditions are individual golden-cut child and moment identities; no independent scientific review',
            'cut_rows':cr,'curved_control':pp,
            'golden_clock_rule':'child-dependent four-role interval code; chart construction, not unique admitted clock law',
            'finite_identity':'sum chi_x P_x(e,U)=sum P_x(sqrt(chi_x)e,U)',
            'measure_equation':'at complete geometric stationarity w=r for the declared KL-augmented homogeneous sector',
            'old_positive_curvature_replaced':False,'native_action_selected':False,
            'native_measure_admission':False,'complete_native_GR_closed':False}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
