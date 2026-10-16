#!/usr/bin/env python3
"""Full16 exact CAR, curved a4 and tensor principal symbol; no GR promotion.
Inputs: the declared creator order and formulas from pinned SOURCE a1ca6f54.
No parent suite, network, file write or fitted physical coefficient.
"""
from itertools import combinations
import json
import hashlib
import sympy as s

ORDER=(0,2,3,1)
PAIRS=list(combinations(range(4),2))
checks=[]

def eq(name,a,b):
    if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):
        good=all(s.expand(z)==0 for z in s.Matrix(a)-s.Matrix(b))
    else: good=s.expand(a-b)==0
    if not good: raise ArithmeticError(name)
    checks.append(name)

def require(name,condition):
    if not condition: raise ArithmeticError(name)
    checks.append(name)

def creators():
    out=[]
    for r in range(4):
        A=s.zeros(16); pred=ORDER[:ORDER.index(r)]
        for m in range(16):
            if not m&(1<<r):
                A[m|(1<<r),m]=(-1)**sum(bool(m&(1<<j)) for j in pred)
        out.append(A)
    return out

def traceprod(a,b):
    return sum(a[i,j]*b[j,i] for i in range(a.rows) for j in range(a.cols))

def build():
    C=creators(); I=[x.T for x in C]
    gamma=[C[i]-I[i] for i in range(4)]
    hat=[C[i]+I[i] for i in range(4)]
    eye=s.eye(16); zero=s.zeros(16)
    for i in range(4):
        for j in range(4):
            eq('owned_CAR_%d%d'%(i,j),C[i]*I[j]+I[j]*C[i],int(i==j)*eye)
            eq('left_right_anticommutation_%d%d'%(i,j),gamma[i]*hat[j]+hat[j]*gamma[i],zero)
    coords=[(a,b,c) for a in range(4) for b,c in PAIRS]
    def tc(t,a,b,c):
        if b==c:return s.Integer(0)
        return t[coords.index((a,b,c))] if b<c else -t[coords.index((a,c,b))]
    ident=s.eye(24)
    v=s.Matrix(4,24,lambda c,k:sum(tc(ident[:,k],a,a,c) for a in range(4)))
    triples=list(combinations(range(4),3))
    cyc=s.Matrix(4,24,lambda i,k:tc(ident[:,k],*triples[i])+tc(ident[:,k],triples[i][1],triples[i][2],triples[i][0])+tc(ident[:,k],triples[i][2],triples[i][0],triples[i][1]))
    N=s.Matrix.hstack(*v.col_join(cyc).nullspace())
    eq('actual_tensor_dimension',N.cols,16)
    eq('tensor_trace_rows',v*N,s.zeros(4,16))
    eq('tensor_cyclic_rows',cyc*N,s.zeros(4,16))
    Zbase=[]
    for a,b,c in coords:
        Q=C[b]*C[c]*I[a];Zbase.append(-(Q+Q.T))
    Bs=[];vac=eye[:,0]
    for k in range(16):
        Z=sum((N[j,k]*Zbase[j] for j in range(24)),zero)
        B=[-(g*Z+Z*g)/2 for g in gamma]
        eq('actual_Z_from_right_connection_%02d'%k,sum((gamma[i]*B[i] for i in range(4)),zero),Z)
        eq('actual_tensor_annihilates_vacuum_%02d'%k,Z*vac,s.zeros(16,1))
        for i in range(4):
            eq('right_antihermitian_%02d_%d'%(k,i),B[i].T,-B[i])
            for j in range(4):
                eq('right_commutant_%02d_%d%d'%(k,i,j),B[i]*gamma[j],gamma[j]*B[i])
        Bs.append(B)
    return C,gamma,hat,N,Bs

def principal_symbol(N,Bs,gamma):
    metric=N.T*N
    vac=s.eye(16)[:,0]
    vm=s.Matrix(16,16,lambda a,b:sum(((Bs[a][i]*vac).T*(Bs[b][i]*vac))[0] for i in range(4)))
    eq('tensor_vacuum_norm',vm,metric/4)
    total=s.Matrix(16,16,lambda a,b:sum(traceprod(Bs[a][i].T,Bs[b][i]) for i in range(4)))
    eq('full_tensor_connection_norm',total,4*metric)
    P=s.Matrix(16,16,lambda a,b:sum(traceprod(Bs[a][i].T,Bs[b][i]) for i in (1,2,3))/3)
    J=metric.inv()*P
    eig=J.eigenvals()
    require('tensor_symbol_exact_eigenvalues',eig=={s.Rational(4,3):10,s.Rational(4,9):6})
    eq('tensor_symbol_minimal_polynomial',(J-s.eye(16)*s.Rational(4,3))*(J-s.eye(16)*s.Rational(4,9)),s.zeros(16))
    eq('tensor_symbol_exact_trace',s.trace(J),16)
    # Positivity does not come from pretending every so4 connection is tensor16.
    # One non-axis rational unit frequency tests O4 covariance, not a rank census.
    xi=s.Matrix([s.Rational(3,5),s.Rational(4,5),0,0])
    def raw(a,b):
        return sum(traceprod((xi[i]*Bs[a][j]-xi[j]*Bs[a][i]).T,
                             xi[i]*Bs[b][j]-xi[j]*Bs[b][i])
                   for i in range(4) for j in range(4))/6
    Px=s.Matrix(16,16,raw);Jx=metric.inv()*Px
    eq('non_axis_same_symbol_polynomial',(Jx-s.eye(16)*s.Rational(4,3))*(Jx-s.eye(16)*s.Rational(4,9)),s.zeros(16))
    eq('non_axis_same_symbol_trace',s.trace(Jx),16)
    return eig

def curved_heat(gamma,hat):
    zero=s.zeros(16); eye=s.eye(16)
    # Generic algebraic curvature tensor: pair symmetries and the sole 4D Bianchi row.
    R=s.Matrix(6,6,lambda i,j:s.Rational(((i+2)*(j+2)+3*(i+j))%11-5,7))
    R[0,5]=R[5,0]=R[1,4]-R[2,3]
    def ri(i,j,a,b):
        if i==j or a==b:return s.Integer(0)
        z=(1 if i<j else -1)*(1 if a<b else -1)
        return z*R[PAIRS.index(tuple(sorted((i,j)))),PAIRS.index(tuple(sorted((a,b))))]
    for i,j,k,l in [(0,1,2,3),(1,0,3,2),(2,1,3,0)]:
        eq('generic_curvature_Bianchi_%d%d%d%d'%(i,j,k,l),ri(i,j,k,l)+ri(i,k,l,j)+ri(i,l,j,k),0)
    Ric=s.Matrix(4,4,lambda j,l:sum(ri(i,j,i,l) for i in range(4)))
    sc=s.trace(Ric); ric2=traceprod(Ric,Ric); rm2=4*traceprod(R,R)
    left={}; right0={}; extra={}
    for m,(i,j) in enumerate(PAIRS):
        left[i,j]=-sum((ri(i,j,a,b)*gamma[a]*gamma[b]/2 for a,b in PAIRS),zero)
        right0[i,j]=sum((ri(i,j,a,b)*hat[a]*hat[b]/2 for a,b in PAIRS),zero)
        extra[i,j]=sum((s.Rational(((m+1)*(k+2))%7-3,11)*hat[a]*hat[b]/2
                        for k,(a,b) in enumerate(PAIRS)),zero)
    eq('actual_Lichnerowicz_left_curvature',sum((gamma[i]*gamma[j]*left[i,j] for i,j in PAIRS),zero),sc*eye/4)
    eq('right_background_curvature_trace',2*sum(traceprod(A,A) for A in right0.values()),-2*rm2)
    tau=s.Symbol('tau',real=True)
    fr={ij:right0[ij]+tau*extra[ij] for ij in PAIRS}
    E=-sc*eye/4-sum((gamma[i]*gamma[j]*fr[i,j] for i,j in PAIRS),zero)
    ordered=2*sum(traceprod(A,A) for A in fr.values())
    Om={ij:left[ij]+fr[ij] for ij in PAIRS}
    eq('full_curved_trace_E',s.trace(E),-4*sc)
    eq('full_curved_trace_E2',traceprod(E,E),sc*sc-ordered/2)
    eq('full_curved_connection_trace',2*sum(traceprod(A,A) for A in Om.values()),-2*rm2+ordered)
    actual=(16*(5*sc*sc-2*ric2+2*rm2)+60*sc*s.trace(E)+180*traceprod(E,E)+60*sum(traceprod(A,A) for A in Om.values()))/360
    expected=sc*sc/18-s.Rational(4,45)*ric2-s.Rational(7,90)*rm2-ordered/6
    eq('full_curved_a4_not_flat_substitution',actual,expected)
    base=s.Rational(1,18)*sc*sc-s.Rational(4,45)*ric2+s.Rational(23,90)*rm2
    eq('actual_Hodge_a4_baseline',actual.subs(tau,0),base)
    cross=4*sum(traceprod(right0[ij],extra[ij]) for ij in PAIRS)
    require('generic_curvature_cross_term_nonzero',cross!=0)
    eq('actual_cross_first_source',s.diff(actual,tau).subs(tau,0),-cross/6)
    # Basis-invariant polynomial re-expression; no fitted coefficients.
    W2,E4,R2=s.symbols('W2 E4 R2')
    rm,rc,rr=s.symbols('Riem2 Ric2 Rscalar2')
    decomposition=s.Rational(7,15)*(rm-2*rc+rr/3)-s.Rational(19,90)*(rm-4*rc+rr)+rr/9
    eq('Weyl_Euler_scalar_decomposition',decomposition,s.Rational(23,90)*rm-s.Rational(4,45)*rc+rr/18)
    eq('traced_derivative_coefficient',(16*12-4*60)/s.Integer(360),-s.Rational(2,15))
    # Independently evaluate the complete Hodge trace on a unit curvature 4-sphere.
    import math
    mult=[math.comb(4,k) for k in range(5)]
    Etrace=sum(-k*(4-k)*mult[k] for k in range(5))
    E2trace=sum(k*k*(4-k)**2*mult[k] for k in range(5))
    eq('constant_curvature_all_grades_trace_E',Etrace,-48)
    eq('constant_curvature_all_grades_trace_E2',E2trace,168)
    a4k=(16*(5*144-2*36+2*24)+60*12*Etrace+180*E2trace-30*4*24)/s.Integer(360)
    eq('constant_curvature_independent_full16_a4',a4k,s.Rational(164,15))
    # Unequal product-sphere radii are a non-Einstein control of the metric source.
    a,b=s.symbols('radius_a radius_b',positive=True)
    rr=2/a**2+2/b**2;rc=2/a**4+2/b**4;rm=4/a**4+4/b**4
    product_integral=s.expand(a*a*b*b*(rr*rr/18-s.Rational(4,45)*rc+s.Rational(23,90)*rm))
    eq('product_spheres_integrated_a4',product_integral,s.Rational(16,15)*(b*b/(a*a)+a*a/(b*b))+s.Rational(4,9))
    eq('Einstein_product_radius_source_a',s.diff(product_integral,a).subs(b,a),0)
    eq('Einstein_product_radius_source_b',s.diff(product_integral,b).subs(b,a),0)
    require('non_Einstein_product_metric_source_not_zero',s.diff(product_integral,a).subs({a:1,b:2})!=0)
    return {'a4_Hodge':'23/90 Riem^2 -4/45 Ric^2 +1/18 R^2 -2/15 laplacian(R)',
            'a4_curved_right':'1/18 R^2 -4/45 Ric^2 -7/90 Riem^2 -1/6 Tr16(F_right_ij F_right_ij) -2/15 laplacian(R)'}

def flat_variations(Bs,gamma,hat,N):
    zero=s.zeros(16);vac=s.eye(16)[:,0]
    # A nonconstant, periodic one-parameter tensor field has derivative + quartic terms.
    k=next(j for j,B in enumerate(Bs) if any(B[i]!=zero for i in (1,2,3)))
    B=Bs[k]
    comm=lambda a,b:a*b-b*a
    derivative=s.simplify(sum(traceprod(B[i].T,B[i]) for i in (1,2,3))/3)
    quartic=s.simplify(sum(traceprod(comm(B[i],B[j]).T,comm(B[i],B[j])) for i,j in PAIRS)/3)
    require('periodic_witness_positive_derivative',derivative>0)
    require('constant_witness_positive_quartic',quartic>0)
    eps,q=s.symbols('epsilon q',real=True)
    # f=eps cos(q*x0), average sin^2=1/2, cos^4=3/8. Mixed trace vanishes by cyclicity.
    eq('periodic_cubic_cross_vanishes',sum(traceprod(B[i].T,comm(B[0],B[i])) for i in (1,2,3)),0)
    avg=derivative*eps**2*q**2/2+s.Rational(3,8)*quartic*eps**4
    eq('periodic_all_terms_scaling_jet',s.diff(avg,eps),derivative*eps*q*q+s.Rational(3,2)*quartic*eps**3)
    # A generic pure-gauge right connection is curvature-free to first order,
    # but is NOT in the tensor subspace because the cyclic vacuum is moved.
    G=hat[1]*hat[2]/2
    pure=[G,zero,zero,zero]
    require('forbidden_pure_gauge_not_tensor_vacuum',sum((gamma[i]*pure[i] for i in range(4)),zero)*vac!=s.zeros(16,1))
    # Curvature also stays in the real right bivector representation.
    for i,j in PAIRS:
        A=comm(B[i],B[j])
        eq('right_curvature_vacuum_HS_%d%d'%(i,j),traceprod(A.T,A),16*((A*vac).T*(A*vac))[0])
    # Full nonabelian variation with homogeneous background, no integration-by-parts needed.
    B0=[Bs[0][i]+Bs[5][i]/3 for i in range(4)]
    dB=Bs[9]; t=s.Symbol('t',real=True)
    F={(i,j):comm(B0[i]+t*dB[i],B0[j]+t*dB[j]) for i,j in PAIRS}
    energy=-sum(traceprod(A,A) for A in F.values())/3
    f0={ij:F[ij].subs(t,0) for ij in PAIRS}
    df={(i,j):comm(dB[i],B0[j])+comm(B0[i],dB[j]) for i,j in PAIRS}
    eq('full_constant_connection_first_source',s.diff(energy,t).subs(t,0),-s.Rational(2,3)*sum(traceprod(f0[ij],df[ij]) for ij in PAIRS))
    return {'periodic_witness_derivative_coefficient':str(derivative),'periodic_witness_quartic_coefficient':str(quartic)}

def run():
    checks.clear();C,gamma,hat,N,Bs=build()
    eig=principal_symbol(N,Bs,gamma)
    curved=curved_heat(gamma,hat)
    periodic=flat_variations(Bs,gamma,hat,N)
    return {'schema':'d0-curved-tensor-a4/1','check_count':len(checks),'check_names_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),
       'source':'a1ca6f547b9b6876c4e31801665573a1734aa65f',
       'carrier':16,'creator_order':list(ORDER),
       'quadratic_symbol_eigenvalues':{str(k):v for k,v in eig.items()},
       'tensor_to_right_norm':'sum_i ||B_i||HS^2 =4 sum_(a,b<c) T_abc^2',
       'curved_formula':curved,'periodic_control':periodic,
       'ordinary_mathematical_carrier':'positive Riemannian G, natural measure, tracefree cycliczero tensor16',
       'full_native_stationarity_proved':False,'short_time_limit_proved':False,'lorentz_Einstein_identification_proved':False,'GR_closed':False}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
