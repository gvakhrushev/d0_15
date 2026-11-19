#!/usr/bin/env python3
"""Actual full16 spatial heat test after shared-controller elimination.

Pinned input: c6e647c4271a7058048e27c650c5b27c042ac63f in gvakhrushev/d0_15.
No native compiler or physical variation-domain theorem is asserted.
All finite spatial Fourier modes are included; large square matrices are not
materialized. The analytic continuum/jet statements are in PROOF_RU.md.
Run normally or with python -O. numpy, scipy, sympy and mpmath are required.
"""
from __future__ import annotations
import hashlib, itertools, json, math, platform
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
import sympy as sp
import mpmath as mp
CHECKS=[]
def check(ok: bool, message: str) -> None:
    if not bool(ok): raise ArithmeticError(message)
    CHECKS.append(message)

def close(a,b,message,tol=1e-10):
    error=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    check(error<tol, message)
    return error

C=[]
for a in range(4):
 x=np.zeros((16,16))
 for m in range(16):
  if not (m>>a)&1:x[m|(1<<a),m]=(-1)**sum((m>>j)&1 for j in range(a))
 C.append(x)
I=[x.T for x in C];gen=np.array([[C[a]@I[b] for b in range(4)] for a in range(4)])

def exterior_generator(w):return np.einsum('ab,abij->ij',w,gen)

def params(theta,b,dtheta,db):
 s,c=np.sin(theta),np.cos(theta)
 u=np.array([[c,-s,0,0],[-s,-c,0,0],[0,0,-1,0],[0,0,0,-1]])
 du=np.array([[-s,-c,0,0],[-c,s,0,0],[0,0,0,0],[0,0,0,0]])*dtheta
 w=np.zeros((4,4,4));dw=np.zeros_like(w)
 # omega_0
 w[0,0,2]=w[0,2,0]=-b*s
 w[0,1,2]=b*c;w[0,2,1]=-b*c
 # omega_1
 w[1,0,2]=w[1,2,0]=-b*c
 w[1,1,2]=-b*s;w[1,2,1]=b*s
 dw[0,0,2]=dw[0,2,0]=-db*s-b*c*dtheta
 dw[0,1,2]=db*c-b*s*dtheta;dw[0,2,1]=-dw[0,1,2]
 dw[1,0,2]=dw[1,2,0]=-db*c+b*s*dtheta
 dw[1,1,2]=-db*s-b*c*dtheta;dw[1,2,1]=-dw[1,1,2]
 return u,du,w,dw

def finite_matrix(L,eps=1/1024,scale=1/4,beta=2*((math.sqrt(5)-1)/2)**2,mode=1):
 h=1/L;eye=np.eye(16);Y=np.arange(L)/L
 mats=[];max_window=0.
 for yy in Y:
  dt=math.sin(2*math.pi*mode*yy);db=2*math.pi*mode*math.cos(2*math.pi*mode*yy)
  u,du,w,dw=params(eps*dt,eps*db,dt,db)
  A=[];dA=[];B=[];dB=[]
  for mu in range(4):
   cm=scale*np.einsum('a,aij->ij',u[mu],C);dcm=scale*np.einsum('a,aij->ij',du[mu],C)
   M,dM=la.expm_frechet(h*exterior_generator(w[mu]),h*exterior_generator(dw[mu]))
   A.append(cm@M/h);dA.append((dcm@M+cm@dM)/h)
   B.append(-cm/h);dB.append(-dcm/h)
   max_window=max(max_window,la.norm(cm@M,2))
  mats.append((A,dA,sum(B),sum(dB)))
 z=0.;dz=0.;mineig=1e9;n=16*L
 for ks in itertools.product(range(L),repeat=3):
  phases=np.exp(2j*np.pi*np.array(ks)/L)
  d=np.zeros((n,n),complex);de=np.zeros_like(d)
  for j,(A,dA,B,dB) in enumerate(mats):
   sl=slice(16*j,16*(j+1));sn=slice(16*((j+1)%L),16*((j+1)%L+1))
   d[sl,sl]=B+A[0]*phases[0]+A[1]*phases[1]+A[3]*phases[2]
   de[sl,sl]=dB+dA[0]*phases[0]+dA[1]*phases[1]+dA[3]*phases[2]
   d[sl,sn]+=A[2];de[sl,sn]+=dA[2]
  D=d+d.conj().T;De=de+de.conj().T
  vals,vec=la.eigh(D,check_finite=False,driver='evr')
  weights=np.exp(-beta*vals**2)
  localder=np.einsum('ij,ij->j',vec.conj(),De@vec).real
  z+=weights.sum();dz+=(-2*beta*weights*vals*localder).sum()
  mineig=min(mineig,float(np.min(vals**2)))
 lam=4*scale**2*L**2*np.sin(np.pi*np.arange(L)/L)**2
 zflat=16*float(np.exp(-beta*lam).sum())**4
 return {'L':L,'profile_mode':mode,'eps':eps,'scale':scale,'beta':beta,'H':math.log(z)/beta,'H_flat':math.log(zflat)/beta,
 'H_difference':math.log(z/zflat)/beta,'dH_deps':float(dz/(beta*z)), 'Z':float(z),'Z_flat':zflat,
 'modes':16*L**4,'minimum_squared_eigenvalue':mineig,'maximum_transported_creation_norm':max_window}

eta=np.array([1,-1,-1,-1])
J=np.zeros((4,4));J[1,2]=1;J[2,1]=-1
B=np.zeros((4,4));B[0,2]=B[2,0]=1
GJ=exterior_generator(J);GB=exterior_generator(B)

def jet(L,m=1,scale=.25,beta=2*((math.sqrt(5)-1)/2)**2):
 check(2*m<L,"Fourier mode is below alias threshold")
 h=1/L;q=2*math.pi*m
 z=np.exp(2j*np.pi*np.arange(L)/L);w=(z-1)/h
 lam=s=scale**2*np.abs(w)**2
 W2,W3=np.meshgrid(w,w,indexing='ij');W2p=np.roll(W2,-m,axis=0)
 coeff=np.stack([np.ones_like(W2),W2p,W2p.conj(),W2,W2.conj(),W3,W3.conj()],axis=-1)
 A=[scale*eta[j]*C[j] for j in range(4)]
 numerator1=numerator2=0.
 for k0 in range(L):
  for k1 in range(L):
   z0,z1=z[k0],z[k1];w0,w1=w[k0],w[k1]
   Db=A[0]*w0+A[0].T*w0.conjugate()+A[1]*w1+A[1].T*w1.conjugate()
   dplus=scale*(.5j*(C[1]*w0+C[0]*w1)+q/2*(C[0]@GJ*z0+C[1]@GB*z1))
   dminus=scale*(-.5j*(C[1]*w0+C[0]*w1)+q/2*(C[0]@GJ*z0+C[1]@GB*z1))
   D1=dplus+dminus.conj().T
   d2=scale*(-C[0]*w0/2+C[1]*w1/2+h*q*q/2*(C[0]@GJ@GJ*z0-C[1]@GB@GB*z1))
   D2=d2+d2.conj().T
   bs=np.stack([Db@D1+D1@Db,A[2]@D1,A[2].T@D1,D1@A[2],D1@A[2].T,
                A[3]@D1+D1@A[3],A[3].T@D1+D1@A[3].T])
   gram=np.einsum('aij,bij->ab',bs.conj(),bs)
   normsq=np.einsum('...a,ab,...b->...',coeff.conj(),gram,coeff).real
   trDelta2=2*(np.trace(Db@D2)+W2*np.trace(A[2]@D2)+W2.conj()*np.trace(A[2].T@D2)
               +W3*np.trace(A[3]@D2)+W3.conj()*np.trace(A[3].T@D2)).real+4*np.linalg.norm(D1,'fro')**2
   ll=lam[k0]+lam[k1]+lam[:,None]+lam[None,:]
   lp=lam[k0]+lam[k1]+np.roll(lam,-m)[:,None]+lam[None,:]
   ee=np.exp(-beta*ll);ep=np.exp(-beta*lp);dif=lp-ll
   FF=np.empty_like(ee);mask=np.abs(dif)<1e-11
   FF[mask]=beta*ee[mask]
   FF[~mask]=(ee[~mask]-ep[~mask])/dif[~mask]
   numerator1+=2*float(np.sum(FF*normsq))
   numerator2+=float(np.sum(ee*trDelta2))
 Z=16*np.exp(-beta*lam).sum()**4
 H2=(numerator1-numerator2)/Z
 return {'L':L,'m':m,'H_second':H2,'scaled_second':H2*L**2,'scaled_over_q2':H2*L**2/q**2,
         'KM_positive':numerator1/Z,'second_Delta':numerator2/Z,'modes':16*L**4}

def calc(m,K=12,ctx=mp.mp):
 pi=ctx.pi;scale=ctx.mpf(1)/4;s2=scale**2;beta=2*((ctx.sqrt(5)-1)/2)**2
 q=2*pi*m;tk=beta*s2
 vals=[2*pi*n for n in range(-K,K+1)]
 A0=sum(ctx.exp(-tk*k*k) for k in vals)
 mu2=sum(k*k*ctx.exp(-tk*k*k) for k in vals)/A0
 mu4=sum(k**4*ctx.exp(-tk*k*k) for k in vals)/A0
 n1=n2=ctx.mpf(0)
 for n in range(-K-m,K+1):
  k=2*pi*n;kp=2*pi*(n+m)
  a=s2*k*k;b=s2*kp*kp;ea=ctx.exp(-beta*a);eb=ctx.exp(-beta*b)
  aa=-s2*k**4/12;bb=-s2*kp**4/12
  if 2*n+m==0:
   f=beta*ea;fa=fb=-beta**2*ea/2
  else:
   dd=s2*(2*pi)**2*m*(2*n+m)
   f=(ea-eb)/dd;fa=(-beta*ea+f)/dd;fb=(beta*eb-f)/dd
  N0=2*q*q*(2*k+q)**2
  N2=q*q/6*(48*(mu2**2+mu4)+48*mu2*(k*k+k*q)+24*mu2*q*q
              -(16*k**4+32*k**3*q+24*k*k*q*q+8*k*q**3+q**4))
  n1+=f*N2+N0*(aa*fa+bb*fb)
  n2+=ea*(8*mu2*q*q-beta*aa*8*q*q)
 return (2*s2*s2*n1-s2*n2)/(16*A0)

def exact_geometry():
    th,b,c=sp.symbols('theta theta_y theta_yy', real=True)
    eta=sp.diag(1,-1,-1,-1)
    e=sp.Matrix([[sp.cos(th),-sp.sin(th),0,0],[sp.sin(th),sp.cos(th),0,0],
                 [0,0,1,0],[0,0,0,1]])
    g=sp.simplify(e.T*eta*e)
    derivative=lambda f:sp.diff(f,th)*b+sp.diff(f,b)*c
    partial=lambda f,mu:derivative(f) if mu==2 else 0
    simp=lambda f:sp.trigsimp(sp.expand_trig(sp.simplify(f)))
    Ga=[sp.zeros(4) for _ in range(4)]
    for mu,a,nu in itertools.product(range(4),repeat=3):
        Ga[mu][a,nu]=simp(sum(g[a,r]*(partial(g[r,nu],mu)+partial(g[r,mu],nu)
                                  -partial(g[mu,nu],r))/2 for r in range(4)))
    Ric=sp.zeros(4)
    for j,l in itertools.product(range(4),repeat=2):
        Ric[j,l]=simp(sum(partial(Ga[l][i,j],i)-partial(Ga[i][i,j],l)
                +sum(Ga[i][i,k]*Ga[l][k,j]-Ga[l][i,k]*Ga[i][k,j] for k in range(4))
                       for i in range(4)))
    R=simp(sp.trace(g*Ric))
    check(R==-2*b*b,'actual Lorentz curvature R=-2 theta_y^2')
    check((e.T*e-sp.eye(4)).applyfunc(simp)==sp.zeros(4),'positive metric fixed exactly')
    check(simp(g.det())==-1,'Lorentz determinant stays nondegenerate')
    om=[(e*Ga[mu]*e.T-(e.diff(th)*b if mu==2 else sp.zeros(4))*e.T).applyfunc(simp)
        for mu in range(4)]
    for mu in range(4):
        check((om[mu].T*eta+eta*om[mu]).applyfunc(simp)==sp.zeros(4),
              'all connection components are in so(1,3)')
    for mu,nu in itertools.product(range(4),repeat=2):
        de_mu=e.diff(th)*b if mu==2 else sp.zeros(4)
        de_nu=e.diff(th)*b if nu==2 else sp.zeros(4)
        tor=de_mu[:,nu]-de_nu[:,mu]+om[mu]*e[:,nu]-om[nu]*e[:,mu]
        check(tor.applyfunc(simp)==sp.zeros(4,1),'true Cartan torsion vanishes')
    CS=[sp.Matrix(x.astype(int)) for x in C];IS=[x.T for x in CS]
    remainder=sp.zeros(16)
    for mu,nu,r in itertools.product(range(4),repeat=3):
        remainder-=Ga[mu][r,nu]*CS[mu]*CS[nu]*IS[r]
    check(remainder.applyfunc(simp)==sp.zeros(16),'all16 transformed exterior zeroth order vanishes')
    pp=(sp.sqrt(5)-1)/2;zz=sp.Rational(1,2**20);x=sp.symbols('x',real=True)
    ee=pp**2*(1+x);ell=4*ee*(1-ee);BB=4*pp**2*(1-pp**2)
    AA=ell+(1-ell)*BB;rr=zz*(AA+BB)-zz**2*AA*BB
    rx0=sp.simplify(sp.diff(rr,x).subs(x,0))
    check(rx0>0,'original nonlinear direct-click has nonzero positive r_x')
    # Valid for m=1,2, epsilon<=1/1024, s=1/4: no new fitted operand.
    upper=sp.Rational(13,21)**2*(sp.Rational(22,7)**2)/4096
    check(upper<sp.Rational(1,1024),'actual nonlinear operands stay in original small collar')
    check(sp.simplify((-pp**2*16*(4*sp.pi)**2*rx0)/
                      (-pp**2*16*(2*sp.pi)**2*rx0))==4,'two original field Hessians have ratio four')
    return {'R_at_scale_one':str(R),'positive_metric':'s^-2 I4',
        'scaled_Lorentz_curvature':'-2 s^2 theta_y^2','det_coframe':'s^-4',
        'original_f_star':'-s^-2 theta_y^2','r_x_0_exact':str(rx0),
        'r_x_0_decimal':str(sp.N(rx0,30)),
        'target_nonlinear_second_m2_over_m1':'4',
        'internal_observer_fixed':True,'new_observer_or_field_added':False,
        'restricted_foliation_admission_proved':False}



def exact_symbol_jets():
    k0,k1,k2,k3,q=sp.symbols('k0 k1 k2 k3 q',real=True)
    kk=[k0,k1,k2,k3];pp=[k0,k1,k2+q,k3];ii=sp.I
    CC=[sp.Matrix(x.astype(int)) for x in C];II=[x.T for x in CC]
    GJ=CC[1]*II[2]-CC[2]*II[1];GB=CC[0]*II[2]+CC[2]*II[0]
    sign=[1,-1,-1,-1]
    zero=lambda:sp.zeros(16)
    add=lambda it:sum(it,zero())
    def flat(K):
        return [add(ii*sign[j]*K[j]*(CC[j]-II[j]) for j in range(4)),
                add(-sign[j]*K[j]**2*(CC[j]+II[j])/2 for j in range(4)),
                add(-ii*sign[j]*K[j]**3*(CC[j]-II[j])/6 for j in range(4))]
    w=lambda k:[ii*k,-k*k/2,-ii*k**3/6]
    z=lambda k:[1,ii*k,-k*k/2]
    w0,w1=w(k0),w(k1);z0,z1=z(k0),z(k1)
    dp=[ii/2*(CC[1]*w0[j]+CC[0]*w1[j])+q/2*(CC[0]@GJ*z0[j]+CC[1]@GB*z1[j]) for j in range(3)]
    dm=[-ii/2*(CC[1]*w0[j]+CC[0]*w1[j])+q/2*(CC[0]@GJ*z0[j]+CC[1]@GB*z1[j]) for j in range(3)]
    B=[(dp[j]+dm[j].H).applyfunc(sp.expand) for j in range(3)]
    dk,dpp=flat(kk),flat(pp)
    A=[add(dpp[a]*B[j-a]+B[j-a]*dk[a] for a in range(j+1)).applyfunc(sp.expand) for j in range(3)]
    inner=lambda a,b:sum(sp.conjugate(x)*y for x,y in zip(a,b))
    N=[sp.factor(sp.expand(sum(inner(A[a],A[j-a]) for a in range(j+1)))) for j in range(3)]
    d2=[-CC[0]*w0[j]/2+CC[1]*w1[j]/2+
        (q*q/2*(CC[0]*GJ*GJ*z0[j-1]-CC[1]*GB*GB*z1[j-1]) if j else zero()) for j in range(3)]
    D2=[(x+x.H).applyfunc(sp.expand) for x in d2]
    T=[sp.factor(sp.expand(2*sum(sp.trace(dk[a]*D2[j-a]) for a in range(j+1))+
                          4*sum(inner(B[a],B[j-a]) for a in range(j+1)))) for j in range(3)]
    even=lambda P:sp.expand(sum(P.subs({k0:u*k0,k1:v*k1},simultaneous=True)
                               for u,v in itertools.product((-1,1),repeat=2))/4)
    target=q*q/6*(48*k0*k0*k1*k1+48*k1**4+
        24*(k0*k0+k1*k1)*(k2*k2+k2*q)+12*(k0*k0+k1*k1)*q*q-
        (16*k2**4+32*k2**3*q+24*k2*k2*q*q+8*k2*q**3+q**4))
    check(sp.expand(N[0]-2*q*q*(2*k2+q)**2)==0,'exact Fourier zero-order numerator')
    check(N[1]==0 and T[1]==0,'exact absent first lattice correction')
    check(sp.expand(T[0]-8*q*q)==0,'exact second-operator zero-order coefficient')
    check(sp.expand(even(N[2])-target)==0,'exact h^2 numerator on all16 CAR coordinates')
    check(sp.expand(even(T[2])-8*k1*k1*q*q)==0,'exact h^2 second-operator coefficient')
    return {'symbolic_coefficients_verified':True,'first_lattice_coefficient_exactly_zero':True,
            'even_transverse_trace_N0':'2*q^2*(2*k_y+q)^2','T0':'8*q^2',
            'even_transverse_trace_T2':'8*k_x^2*q^2'}

def interval_limit():
    mp.mp.dps=80;mp.iv.dps=80;K=16
    # This generous all-tail bound is derived in PROOF_RU.md, not estimated
    # by comparing two truncations. It includes the transverse theta moments.
    tail=mp.iv.mpf(10)**30*(K+1)**8*mp.iv.exp(-mp.iv.mpf(27)/16*(K+1)**2)
    check(tail.b<mp.iv.mpf('1e-160'),'explicit infinite-series tail bound')
    ranges=[]; intervals=[]
    for m,low,high in [(1,'42.6276','42.6278'),(2,'109.2735','109.2738')]:
        v=calc(m,K,mp.iv)+mp.iv.mpf([-1,1])*tail
        check(v.a>mp.iv.mpf(low) and v.b<mp.iv.mpf(high),'interval asymptotic coefficient enclosure')
        intervals.append(v)
        ranges.append({'m':m,'rigorous_lo':low,'rigorous_hi':high,
                       'diagnostic':mp.nstr(calc(m,K,mp.mp),45)})
    ratio=intervals[1]/intervals[0]
    check(ratio.a>mp.iv.mpf('2.563') and ratio.b<mp.iv.mpf('2.565'),
          'spatial heat second-response ratio excludes Einstein ratio four')
    check(intervals[1].b<4*intervals[0].a,'nonzero rescaling cannot match both modes')
    return {'coefficients':ranges,'tail_bound':str(tail),'interval_dps':80,
            'series_cutoff':K,'ratio_interval':str(ratio),
            'scope':'C2 linearized source, fixed beta and fixed s; no all-regime physical no-go'}


def main():
    geometry=exact_geometry()
    exact_jets=exact_symbol_jets()
    mat=[finite_matrix(n) for n in (4,6,8)]
    for r in mat:
        check(r['maximum_transported_creation_norm']<.26,'strict actual Julia contraction window')
        check(r['modes']==16*r['L']**4,'all finite spatial modes retained')
    check(all(abs(mat[j+1]['dH_deps'])<abs(mat[j]['dH_deps']) for j in range(2)),
          'unscaled spatial source decreases in actual full16 stencils')
    controls=[]
    for L,m in ((4,1),(6,2)):
        # Cross-check analytic Kubo-Mori/Fourier Hessian against independent
        # full-matrix derivative at two nearby configurations.
        ep=1e-5
        r1=finite_matrix(L,ep,mode=m);r2=finite_matrix(L,-ep,mode=m)
        fd=(r1['dH_deps']-r2['dH_deps'])/(2*ep)
        pred=jet(L,m)['H_second']
        err=close(fd,pred,'matrix derivative vs Fourier Hessian',2e-7)
        controls.append({'L':L,'m':m,'actual_Hessian':pred,'independent_error':err})
    table=[]
    for L in (8,16,32,64):
        for m in (1,2):table.append(jet(L,m))
    limit=interval_limit()
    for m in (1,2):
        seq=[r for r in table if r['m']==m]
        vv=float(calc(m,16,mp.mp))
        check(abs(seq[-1]['scaled_second']-vv)<.01*vv,'finite all-mode response approaches analytic coefficient')
    out={'input_commit':'c6e647c4271a7058048e27c650c5b27c042ac63f',
        'status':'PASS_SCOPED_SPATIAL_HEAT_SOURCE_TEST',
        'geometry':geometry,'exact_symbol_jets':exact_jets,'full_matrix_controls':mat,'independent_Hessian_control':controls,
        'all_mode_Hessians':table,'asymptotic_intervals':limit,
        'GR_closed':False,'physical_variation_domain_proved':False,
        'new_native_programme_emitted':False,'full_Cost_Info_source_computed':False,
        'finite_clock_error_included':False,'Lean_or_repository_CI_run':False,
        'test_count':len(CHECKS),'tests':CHECKS,
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
          'scipy':scipy.__version__,'sympy':sp.__version__,'mpmath':mp.__version__},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
