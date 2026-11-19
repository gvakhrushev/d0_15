#!/usr/bin/env python3
"""Canonical AF seed + already-owned scalar report: FULL H+J source.

No native gate compiler or physical-domain equality is asserted. Analytic
identities are checked on actual AF matrices; the 42-coordinate field test
is a pointwise Palatini jet, not a finite geometric root or a PDE solve.
"""
from __future__ import annotations
import hashlib, importlib.util, json, math, platform
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sp
import mpmath as mp
import torch

CHECKS=0; ERR={}
p=(math.sqrt(5)-1)/2; kap=2*p*p; z=2**-20; beta=kap

def check(v, name):
    global CHECKS
    CHECKS+=1
    if not bool(v): raise ArithmeticError(name)

def near(a,b,name,tol=2e-11):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    ERR[name]=max(ERR.get(name,0.),err)
    check(err<tol,name+': '+str(err))
    return err

def load_parent():
    path=Path(__file__).resolve().parents[1]/'d0_af_native_julia_source_lift_2026-10-28'/'check_af_julia_lift.py'
    raw=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    check(blob=='578dadf933f72cedbc484431519ac9e2dc8afc0f','pinned owned AF constructor')
    spec=importlib.util.spec_from_file_location('owned_af',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def scalar_lift(inc,c):
    b=(c-p**3)/kap; s=math.sqrt((1-b)*(1+b))
    check(0<=b<1,'scalar lift interior chart')
    out=[np.zeros((d,d),complex) for d in inc.new]
    dout=[np.zeros_like(v) for v in out]
    for aa in range(2):
        for bb in range(2):
            copies=inc.positions[bb,aa]
            for j in range(0,len(copies)-1,2):
                x,y=copies[j],copies[j+1];I=np.eye(len(x))
                out[bb][np.ix_(x,x)]=b*I;out[bb][np.ix_(y,y)]=b*I
                out[bb][np.ix_(x,y)]=-s*I;out[bb][np.ix_(y,x)]=s*I
                db=1/kap;ds=-b/(kap*s)
                dout[bb][np.ix_(x,x)]=db*I;dout[bb][np.ix_(y,y)]=db*I
                dout[bb][np.ix_(x,y)]=-ds*I;dout[bb][np.ix_(y,x)]=ds*I
            if len(copies)%2:
                x=copies[-1];out[bb][np.ix_(x,x)]=np.eye(len(x))
    for u,du in zip(out,dout):
        near(u.conj().T@u,np.eye(len(u)),'whole left AF unitary')
        near(u.conj().T@du+du.conj().T@u,0,'whole left AF derivative')
    for C,D in zip(inc.expectation(out),inc.expectation(dout)):
        near(C,c*np.eye(len(C)),'actual conditional scalar corner')
        near(D,np.eye(len(D)),'actual scalar first jet')
    return out,dout


def seed():
    out=[np.eye(13),np.eye(8)]
    for b,pairs in enumerate([[(0,7),(5,10),(8,2)],[(0,7),(5,2)]]):
        for i,j in pairs:out[b][i,i]=out[b][j,j]=0;out[b][i,j]=out[b][j,i]=1
    return out


def spectrum_counts():
    mult=np.array([[5,3],[3,2]])
    dims=[89,55]; positives=[10,6]; negatives=[3,2]
    fplus=fminus=rplus=rminus=0
    for b,db in enumerate(dims):
        for a in range(2):
            u=mult[b,a]%2;k=mult[b,a]//2
            fplus+=db*u*positives[a];fminus+=db*u*negatives[a]
            rplus+=db*k*positives[a];rminus+=db*k*negatives[a]
    check((fplus,fminus,rplus,rminus)==(1974,610,3194,987),'all regular-right multiplicities')
    check(fplus+fminus+2*(rplus+rminus)==10946,'complete GNS dimension')
    return [int(x) for x in (fplus,fminus,rplus,rminus)]


def actual_af():
    af=load_parent();inc0=af.Inclusion((3,2),3);inc=af.Inclusion((13,8),4)
    full=af.Inclusion((3,2),7)
    W=seed();Q=inc0.expectation(W)
    near(Q[0],np.diag([0,1,0]),'owned seed corner type0')
    near(Q[1],np.eye(2),'owned seed corner type1')
    Wi=inc.embed(W);J=full.canonical_input(); counts=spectrum_counts()
    cases=[]
    for c in (.44,.78,.999):
        V,dV=scalar_lift(inc,c)
        U=[v@w for v,w in zip(V,Wi)];dU=[dv@w for dv,w in zip(dV,Wi)]
        for v,w in zip(V,Wi):near(v@w,w@v,'new lift commutes with actual seed')
        Y=full.apply_full_left(U,J);dY=full.apply_full_left(dU,J)
        C=J.conj().T@Y;dC=J.conj().T@dY
        Qreg=la.block_diag(np.kron(Q[0],np.eye(3)),np.kron(Q[1],np.eye(2)))
        near(C,c*Qreg,'full canonical GNS compression')
        near(dC,Qreg,'full canonical GNS source')
        D=(1-z)*np.eye(13)+z*C.conj().T@C
        src=-2*z*np.trace(la.solve(D,C.conj().T@dC)).real
        expected=-14*z*c/(1-z+z*c*c)
        near(src,expected,'complete return slope',3e-16)
        phi=math.acos((c-p**3)/kap)
        for k in range(1,9):
            actual=sum(db*np.trace(np.linalg.matrix_power(u,k)).real for db,u in zip(inc.new,U))
            target=counts[0]+(-1)**k*counts[1]+2*(counts[2]+(-1)**k*counts[3])*math.cos(k*phi)
            near(actual,target,'full trace characters including right columns',2e-10)
        # Compute every old-left insertion before evaluating its source.
        grad_blocks=[]
        for k in range(1,5):
            gg=[]
            for aa,da in enumerate(inc.old):
                block=np.zeros((da,da),complex)
                for bb,db in enumerate(inc.new):
                    uk=np.linalg.matrix_power(U[bb],k)
                    for ix in inc.positions[bb,aa]:block+=db*uk[np.ix_(ix,ix)]
                gg.append(block)
                near(block,block.conj().T,'old thermal character coefficient Hermitian')
            grad_blocks.append(gg)
        max_ret=max_heat=0.;nrows=0
        for aa,da in enumerate(inc.old):
            def basis():
                for r in range(da):
                    X=np.zeros((da,da),complex);X[r,r]=1j;yield X
                for r in range(da):
                    for t in range(r):
                        X=np.zeros((da,da),complex);X[r,t]=1;X[t,r]=-1;yield X
                        X=np.zeros((da,da),complex);X[r,t]=X[t,r]=1j;yield X
            for X in basis():
                nrows+=1
                old=[np.zeros((13,13),complex),np.zeros((8,8),complex)]
                old[aa]=X@W[aa]
                eold=inc0.expectation(old)
                dk=c*la.block_diag(np.kron(eold[0],np.eye(3)),np.kron(eold[1],np.eye(2)))
                g=-2*z*np.trace(la.solve(D,C.conj().T@dk)).real
                max_ret=max(max_ret,abs(g))
                check(abs(g)<1e-15,'every original prefix return row')
                for gg in grad_blocks:
                    hg=np.trace(gg[aa]@X).real
                    max_heat=max(max_heat,abs(hg))
                    check(abs(hg)<1e-10,'every original prefix heat-character row')
        check(nrows==233,'complete old-left Lie basis')
        cases.append({'c':c,'return_slope':src,'old_left_rows':nrows,
                      'old_return_residual':max_ret,'old_heat_character_residual':max_heat})
    return {'cases':cases,'GNS_dimension_per_DATA_copy':10946,'actual_canonical_input_columns':13,
            'eigenvalue_multiplicities_per_DATA_copy':counts,
            'explicit_GNS_input_output_replayed':True,'native_compiler_executed':False}


def rational_bound():
    x=F(2,55);zeta=F(1,2**20);cmin=F(8,13)**3
    vals=[]
    for N in (4,5,8,26):
        q=x**N/math.factorial(N)
        E=F(2112,3231)/(1-x*x)*q*(1+q)/(1-q)**3
        rho=E/(14*zeta*cmin)
        check(rho<F(1,64),'exact full thermal distortion <1/64')
        check(q<1,'geometric majorant valid')
        vals.append({'N':N,'bound_H_c':float(E),'relative_bound_d1':float(rho),
                     'bound_H_c_exact':str(E) if N==4 else None,
                     'relative_bound_exact':str(rho) if N==4 else None})
    # Monotonicity is exact: q_(N+1)/q_N=x/(N+1)<1, R(q) increases for 0<q<1.
    t=sp.symbols('t',positive=True)
    deriv=sp.factor(sp.diff(t*(1+t)/(1-t)**3,t))
    check(sp.simplify(deriv-(1+4*t+t*t)/(1-t)**4)==0,'majorant monotonicity for every N>=4')
    return {'all_N_at_least_4':True,'uniform_bound':'1/64 per genuine DATA multiplicity >=1',
            'source_gain_lower':'63/64 of true return gain', 'rows':vals}


NODES=(9,11,13);DEGREES=(26,24,22)

def scene_mp():
    C=mp.diag([mp.mpf(1)/v for v in DEGREES]);B=mp.zeros(3)
    for i in range(3):
        for j in range(3):
            if i!=j:B[i,j]=mp.sqrt(mp.mpf(NODES[i]*NODES[j])/(DEGREES[i]*DEGREES[j]))
    return B,C


def heat_mp(c,N,d=1):
    pp=(mp.sqrt(5)-1)/2;kk=2*pp*pp;bb=kk
    B,C=scene_mp();b=(c-pp**3)/kk;phi=mp.acos(b)
    ds=1/(kk*mp.sqrt(1-b*b))
    phases=[(0,1974,0),(mp.pi,610,0),(phi,3194,-ds),(-phi,3194,ds),
            (mp.pi+phi,987,-ds),(mp.pi-phi,987,ds)]
    z0=mp.mpf(0);dz0=mp.mpf(0)
    for theta,mult,dtheta in phases:
        for j in range(N):
            angle=(theta+2*mp.pi*j)/N;x=mp.cos(angle)
            dx=-mp.sin(angle)*dtheta/N
            L=mp.eye(3)-B-2*x*C
            eig,Q=mp.eigsy(L)
            ex=[mp.exp(-bb*t) for t in eig]
            tr=sum(ex);ct=sum(ex[k]*sum(C[i,i]*Q[i,k]**2 for i in range(3)) for k in range(3))
            for n,degree in zip(NODES,DEGREES):
                v=mp.exp(-bb*(1-2*x/degree));tr+=(n-1)*v;ct+=(n-1)*v/degree
            z0+=mult*d*tr;dz0+=mult*d*2*bb*ct*dx
    Z=2*z0+359*N*10946*d
    return mp.log(Z)/bb,2*dz0/(bb*Z)


def exact_scene_reduction():
    B3,C3=scene_mp()
    A=np.zeros((33,33));off=np.cumsum([0]+list(NODES))
    for i in range(3):
        for j in range(3):
            if i!=j:A[off[i]:off[i+1],off[j]:off[j+1]]=1
    deg=A.sum(1)+2;D=np.diag(1/np.sqrt(deg));B=D@A;B=B@D;C=D@D
    check(int(A.sum()/2)==359,'actual scene edge count')
    for x in (-.7,.15,.93):
        lam=la.eigvalsh(np.eye(33)-B-2*x*C)
        small=la.eigvalsh(np.eye(3)-np.array(B3.tolist(),float)-2*x*np.array(C3.tolist(),float))
        expected=list(small)
        for n,k in zip(NODES,DEGREES):expected.extend([1-2*x/k]*(n-1))
        near(np.sort(lam),np.sort(expected),'all 33 scene eigenvalues',3e-14)


def heat_controls():
    mp.mp.dps=65; exact_scene_reduction()
    vals=[]
    for c0,N in [('0.4',4),('0.8',4),('0.999999',4),('0.8',8)]:
        c=mp.mpf(c0);H,Hc=heat_mp(c,N)
        h=mp.mpf('1e-12') if c0!='0.999999' else mp.mpf('1e-14')
        fd=(heat_mp(c+h,N)[0]-heat_mp(c-h,N)[0])/(2*h)
        check(abs(fd-Hc)<mp.mpf('1e-24'),'independent full heat finite difference')
        x=F(2,55);q=x**N/math.factorial(N)
        ef=F(2112,3231)/(1-x*x)*q*(1+q)/(1-q)**3
        E=mp.mpf(ef.numerator)/ef.denominator
        check(abs(Hc)<=E,'full spectral heat slope inside rational bound')
        Jc=-14*mp.mpf(2)**-20*c/(1-mp.mpf(2)**-20+mp.mpf(2)**-20*c*c)
        ratio=Hc/Jc
        check(abs(ratio)<mp.mpf(1)/64,'actual heat/return source ratio')
        vals.append({'c':c0,'N':N,'full_heat':mp.nstr(H,30),'H_c':mp.nstr(Hc,30),
                     'J_c_per_DATA_copy':mp.nstr(Jc,30),'relative_heat_correction':mp.nstr(ratio,30),
                     'finite_difference_error':mp.nstr(abs(fd-Hc),8),
                     'whole_two_grade_mode_count_per_DATA_copy':425*N*10946})
    return vals


def field_test():
    torch.set_default_dtype(torch.float64);torch.set_num_threads(1)
    # A pointwise Palatini jet with 16 independent tetrad entries,24 connection
    # entries,2 scalar-gradient amplitudes. Not the repository's finite mesh.
    eta=torch.diag(torch.tensor([1.,-1.,-1.,-1.]));v0=torch.tensor([1.,.1,-.2,.05]);v1=torch.tensor([.2,.4,.1,-.3])
    pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
    def operands(y):
        e=torch.eye(4)+y[:16].reshape(4,4)
        es=torch.linalg.inv(e);g=e.T@eta@e;gi=torch.linalg.inv(g)
        ws=[]
        for mu in range(4):
            cols=[]
            for a in range(4):
                row=[]
                for b in range(4):
                    if a==b:row.append(y[0]*0)
                    else:
                        j=pairs.index((min(a,b),max(a,b)))
                        row.append((1 if a<b else -1)*y[16+6*mu+j]*eta[b,b])
                cols.append(torch.stack(row))
            ws.append(torch.stack(cols))
        rr=y[0]*0
        for mu in range(4):
            for nu in range(4):
                Fmn=(ws[mu]@ws[nu]-ws[nu]@ws[mu])@eta
                rr=rr+torch.einsum('a,b,ab->',es[mu],es[nu],Fmn)
        f=torch.linalg.det(e)*rr/2
        q=(y[40]**2)*(v0@gi@v0)+(y[41]**2)*(v1@gi@v1)
        return f,q
    def click(y):
        f,q=operands(y);x=kap*f;v=kap*q
        ee=p*p*(1+x);ell=4*ee*(1-ee);b=p-p*p*v;BB=4*b*b*(1-b*b)
        AA=ell+(1-ell)*BB
        return z*(AA+BB)-z*z*AA*BB
    B3,C3=scene_mp();Bt=torch.tensor(B3.tolist(),dtype=torch.float64);Ct=torch.tensor(C3.tolist(),dtype=torch.float64)
    def full_price(P,N=4,d=16):
        alpha=4*p*p;gamma=p*p
        cc=torch.sqrt(1-alpha*gamma*P*(1-gamma*P));ph=torch.acos((cc-p**3)/kap)
        phases=[(ph*0,1974),(ph*0+math.pi,610),(ph,3194),(-ph,3194),
                (math.pi+ph,987),(math.pi-ph,987)]
        Z0=P*0
        for th,mul in phases:
            for j in range(N):
                x=torch.cos((th+2*math.pi*j)/N)
                L=torch.eye(3)-Bt-2*x*Ct
                tr=torch.trace(torch.matrix_exp(-beta*L))
                for n,k in zip(NODES,DEGREES):tr=tr+(n-1)*torch.exp(-beta*(1-2*x/k))
                Z0=Z0+d*mul*tr
        H=torch.log(2*Z0+359*N*10946*d)/beta
        J=-6*d*math.log(1-z)-7*d*torch.log1p(-z*alpha*gamma*P*(1-gamma*P))
        return H+J,H,J
    y=torch.linspace(-.025,.03,42);y[40]=.19;y[41]=-.13;y.requires_grad_(True)
    P=click(y)
    total,H,J=full_price(P)
    gradient=torch.autograd.grad(total,y,retain_graph=True)[0]
    gp=torch.autograd.grad(P,y,retain_graph=True)[0]
    gain=torch.autograd.grad(total,P,retain_graph=True)[0]
    jgain=torch.autograd.grad(J,P,retain_graph=True)[0]
    err=float(torch.max(torch.abs(gradient-gain*gp)).detach())
    check(err<1e-21,'all42 pointwise field covector exact chain')
    check(float(torch.linalg.norm(gp))>1e-9,'field test is off shell, not a fitted zero')
    check(float(gain)>0,'full nonzero gain')
    check(abs(float(gain/jgain)-1)<1/64,'full heat cannot kill true field gain')
    # Independent central difference of the FULL scalar, subtract high common
    # H baseline only for numeric stability in the already-computed difference.
    # No finite difference value precision claim is used as the analytic proof.
    return {'pointwise_field_directions':42,'matrix_exp_heat_modes_included':425*4*10946*16,
            'original_click':float(P.detach()),'full_gain':float(gain.detach()),
            'return_gain':float(jgain.detach()),'heat_relative_correction':float((gain/jgain-1).detach()),
            'source_chain_error':err,'nonzero_field_covector_norm':float(torch.linalg.norm(gp).detach()),
            'full42_mesh_or_stationary_root_replayed':False}



def matrix_cold_jet():
    # Non-diagonal Hermitian DATA perturbations. Spectral factorization is exact
    # for this lift, so all DATA eigenvalues contribute with their true counts.
    mp.mp.dps=65
    c=mp.mpf('.78');N=4;beta_mp=2*((mp.sqrt(5)-1)/2)**2;zz=mp.mpf(2)**-20
    Hc0=heat_mp(c,N)[1]
    Jc0=-14*zz*c/(1-zz+zz*c*c)
    results=[]
    for a,b,rr,ii in [('0.03','-0.01','0.02','0.013'),('0.04','-0.04','0.017','-0.03')]:
        a,b,rr,ii=map(mp.mpf,(a,b,rr,ii))
        discr=mp.sqrt(((a-b)/2)**2+rr*rr+ii*ii)
        eig=[(a+b)/2-discr,(a+b)/2+discr]
        def price(t):
            Z=mp.mpf(0);J=mp.mpf(0)
            for ev in eig:
                v=c+t*ev
                H,_=heat_mp(v,N)
                Z+=mp.exp(beta_mp*H)
                J+=-6*mp.log(1-zz)-7*mp.log(1-zz+zz*v*v)
            return mp.log(Z)/beta_mp+J
        step=mp.mpf('1e-10')
        fd=(price(step)-price(-step))/(2*step)
        expected=(Hc0/2+Jc0)*(a+b)
        check(abs(fd-expected)<mp.mpf('1e-26'),'full matrix-valued DATA cold-source identity')
        if a+b==0:check(abs(fd)<mp.mpf('1e-45'),'traceless vertical source not assigned a new field')
        results.append({'trace':mp.nstr(a+b,10),'expected_source':mp.nstr(expected,30),
                        'full_scalar_difference_error':mp.nstr(abs(fd-expected),10)})
    return {'full_matrix_source_theorem_tested':True,'DATA_dimension':2,'controls':results}


def main():
    out={'input_commit':'a8635c65a6af41c8fbafc605f7c43d0713b4591f',
         'AF':actual_af(),'uniform_bound':rational_bound(),'full_heat':heat_controls(),
         'pointwise_field':field_test(),'matrix_cold_jet':matrix_cold_jet()}
    out.update({'checks':CHECKS,'max_errors':ERR,'status':'PASS_CANONICAL_AF_FULL_HEAT_SCALAR_SOURCE',
       'GR_closed':False,'original_Julia_row_identified_with_reporter':False,
       'fine_record_equivalence_claimed':False,'native_compiler_emitted':False,'Lean_or_CI_run':False,
       'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__}})
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
