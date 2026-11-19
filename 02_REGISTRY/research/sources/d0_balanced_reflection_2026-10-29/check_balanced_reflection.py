#!/usr/bin/env python3
"""Canonical A2->A5 reflected source and fixed intrinsic effect.

Exact symbolic algebra is separate from floating structural checks. This is not
an emitted G/CX/SourceI program, a physically written record, or a GR closure.
Only original finite AF path spaces and their canonical input are constructed.
"""
from __future__ import annotations
import hashlib
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
import sympy as sp
import torch

P_GOLD=(math.sqrt(5)-1)/2
ZETA=2**-20
BETA=2*P_GOLD**2
PAIRS=(((0,7),(5,10),(8,2)),((0,7),(5,2)))
CHECKS=0
ERRORS={}


def check(value: bool, description: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(value):
        raise ArithmeticError(description)


def near(a,b,description,tol=2e-11):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    ERRORS[description]=max(ERRORS.get(description,0.),err)
    check(err<tol,description+': '+str(err))
    return err


def paths_and_input(d=1):
    old=(3,2)
    paths=[[(a,r) for r in range(n)] for a,n in enumerate(old)]
    for _ in range(3): paths=[paths[0]+paths[1],paths[0]]
    check(tuple(map(len,paths))==(13,8),'actual three-level sizes')
    starts={}
    for b in range(2):
        for a,n in enumerate(old):
            starts[b,a]=[i for i,v in enumerate(paths[b]) if v==(a,0)]
            for i in starts[b,a]:
                check(paths[b][i:i+n]==[(a,r) for r in range(n)],'recursive copy order')
    new=(13,8)
    J=np.zeros((233*d,13*d),complex)
    newoff=(0,169*d);oldoff=(0,9*d)
    for b,nb in enumerate(new):
        for a,na in enumerate(old):
            for start in starts[b,a]:
                for r in range(na):
                    for col in range(na):
                        for t in range(d):
                            J[newoff[b]+((start+r)*nb+start+col)*d+t,
                              oldoff[a]+(r*na+col)*d+t]=P_GOLD**((3+b-a)/2)
    near(J.conj().T@J,np.eye(13*d),'true canonical isometry')
    return paths,starts,J


def left_rep(blocks,d=1):
    pieces=[]
    for nb,B in zip((13,8),blocks):
        four=np.einsum('iakb,jl->ijaklb',B.reshape(nb,d,nb,d),np.eye(nb))
        pieces.append(four.reshape(nb*nb*d,nb*nb*d))
    return la.block_diag(*pieces)


def old_rep(blocks,d=1):
    pieces=[]
    for nb,B in zip((3,2),blocks):
        four=np.einsum('iakb,jl->ijaklb',B.reshape(nb,d,nb,d),np.eye(nb))
        pieces.append(four.reshape(nb*nb*d,nb*nb*d))
    return la.block_diag(*pieces)


def lift(C):
    d=len(C)
    near(C,C.conj().T,'Hermitian supplied corner')
    eig,V=la.eigh(C)
    check(np.max(np.abs(eig))<1,'open contraction chart')
    S=(V*np.sqrt(1-eig**2))@V.conj().T
    blocks=[]
    for nb,pairs in zip((13,8),PAIRS):
        B=np.eye(nb*d,dtype=complex)
        for a,b in pairs:
            ia=slice(a*d,(a+1)*d);ib=slice(b*d,(b+1)*d)
            B[ia,ia]=C;B[ib,ib]=-C
            B[ia,ib]=S;B[ib,ia]=S
        blocks.append(B)
    return blocks


def seed_blocks(d=1):
    return lift(np.zeros((d,d),complex))


def expected_corner(C):
    d=len(C)
    b0=la.block_diag(C,np.eye(d),-C)
    b1=np.eye(2*d)
    return old_rep([b0,b1],d)


def structural_data(d=1):
    paths,starts,J=paths_and_input(d)
    U0=left_rep(seed_blocks(d),d)
    Q=old_rep([np.kron(np.diag([0,1,0]),np.eye(d)),np.eye(2*d)],d)
    R=np.eye(13*d)-Q
    T=U0@J@R
    P=J@J.conj().T
    F0=T@T.conj().T
    M=np.eye(233*d)-F0
    near(J.conj().T@T,0,'seed failure orthogonal to canonical input')
    near(T.conj().T@T,R,'seed failure isometry on true escaping sector')
    near(F0@F0,F0,'fixed intrinsic failure projector')
    near(M@P,P,'fixed success effect contains canonical cut')
    check(round(np.trace(F0).real)==6*d,'actual failure rank 6d')
    return paths,starts,J,Q,R,P,M


def symbolic_algebra():
    p=(sp.sqrt(5)-1)/2;c,s=sp.symbols('c s',real=True)
    block=sp.Matrix([[c,s],[s,-c]])
    check(block*block==(c*c+s*s)*sp.eye(2),'reflection pair identity')
    check(sp.simplify(3*p**3+2*p**4-1)==0,'original type0 expectation weights')
    check(sp.simplify(2*p**2+p**3-1)==0,'original type1 expectation weights')
    c0=p**3;s0=2*p*sp.sqrt(p)
    check(sp.simplify(c0*c0+s0*s0-1)==0,'existing Golden query point')
    G=sp.Matrix([[sp.sqrt(p),-p],[p,sp.sqrt(p)]])
    check((G*sp.diag(1,-1)*G.T-sp.Matrix([[c0,s0],[s0,-c0]])).applyfunc(sp.simplify)==sp.zeros(2),
          'pair at native algebraic point equals original Golden query')
    alpha,gamma,x,Omega,z,d=sp.symbols('alpha gamma x Omega z d',positive=True)
    c2=1-alpha*gamma*x*(1-gamma*x)
    J=-6*d*sp.log(1-z+z*c2)
    g=6*d*z*alpha*gamma*(1-2*gamma*x)/(Omega*(1-z*alpha*gamma*x*(1-gamma*x)))
    check(sp.simplify(sp.diff(J,x)/Omega-g)==0,'original nonlinear reporter gain without fit')
    jold=-6*d*sp.log(1-z)-7*d*sp.log(1-z+z*c2)
    check(sp.simplify(sp.diff(J,x)-sp.Rational(6,7)*sp.diff(jold,x))==0,'same-source ratio to prior canonical return')
    return {'pair_signature':[1,-1],'new_AF_levels':3,'scalar_cold_blocks':['diag(c,1,-c)','I2'],
            'return_variation_multiplicity':6,'fixed_return_multiplicity':7,
            'source_ratio_to_prior_canonical_return':'6/7',
            'native_Golden_point_algebra_checked':True,'native_path_addressing_compiled':False}


def archive_and_corner():
    paths,starts,J,Q,R,P,M=structural_data()
    labels_old=([0,1,0],[0,1]);labels=[]
    for row in paths:labels.append([labels_old[a][r] for a,r in row])
    cases=[]
    for c in (0.,P_GOLD**3,.6,.93,-.4):
        B=lift(np.array([[c]]));U=left_rep(B);Y=U@J
        near(U,U.conj().T,'complete reflection Hermitian')
        near(U@U,np.eye(233),'complete reflection unitary')
        near(J.conj().T@Y,expected_corner(np.array([[c]])),'full canonical compression')
        for b,L in zip(B,labels):
            for a in (0,1):
                archive=np.diag([v==a for v in L])
                near(b@archive,archive@b,'original A0 archive preserved')
        K=J.conj().T@Y;E=Y.conj().T@M@Y
        near(E,K.conj().T@K,'intrinsic record-return saturation')
        near((M-P)@Y,0,'intrinsic zero-gap amplitude')
        near(E,Q+c*c*R,'all-input success effect law')
        eig=la.eigvalsh(U)
        check(np.sum(eig>0)==178 and np.sum(eig<0)==55,'full GNS reflection multiplicities')
        Jr=-np.log1p(-ZETA*la.eigvalsh(np.eye(13)-K.conj().T@K)).sum()
        analytic=-6*math.log1p(-ZETA*(1-c*c))
        near(Jr,analytic,'unchanged Book return determinant with real multiplicity',1e-18)
        cases.append({'c':c,'return_price':float(Jr),'full_GNS_dimension':233,'input_rank':13})
    return cases


def arbitrary_sources():
    paths,starts,J,Q,R,P,M=structural_data()
    c=.61;U=left_rep(lift(np.array([[c]])));Y=U@J;K=J.conj().T@Y
    D=(1-ZETA)*np.eye(13)+ZETA*K.conj().T@K;res=la.inv(D)
    rng=np.random.default_rng(20261029)
    tests=[]
    for n in range(6):
        Z=rng.normal(size=(233,233))+1j*rng.normal(size=(233,233))
        X=(Z-Z.conj().T)/2;X/=la.norm(X,2)
        dy=X@Y;dk=J.conj().T@dy
        de=dy.conj().T@M@Y+Y.conj().T@M@dy
        ds=dk.conj().T@K+K.conj().T@dk
        near(de,ds,'all endpoint first-source saturation')
        g1=-ZETA*np.trace(res@ds).real;g2=-ZETA*np.trace(res@de).real
        near(g1,g2,'complete cotangent pulled through fixed effect',2e-19)
        for k in range(1,7):
            uk=U if k%2 else np.eye(233)
            near(np.trace(uk@X).real,0,'every heat character first variation zero',2e-12)
        tests.append({'J_source':float(g1),'effect_source':float(g2)})
    # Genuine nonzero law-changing direction, not a stationarity claim.
    s=math.sqrt(1-c*c)
    dblocks=[]
    for nb,pairs in zip((13,8),PAIRS):
        V=np.zeros((nb,nb),complex)
        for a,b in pairs:V[a,a]=1;V[b,b]=-1;V[a,b]=V[b,a]=-c/s
        dblocks.append(V)
    dU=left_rep(dblocks);dy=dU@J;dk=J.conj().T@dy
    g=-2*ZETA*np.trace(res@K.conj().T@dk).real
    expected=-12*ZETA*c/(1-ZETA+ZETA*c*c)
    near(g,expected,'law-changing c source retained',1e-18)
    check(abs(g)>1e-7,'no false full stationarity')
    # Old A2 left rotations are neutral. Arbitrary A5 operations are NOT claimed neutral.
    old_count=0
    for a,na in enumerate((3,2)):
        for r in range(na):
            directions=[]
            X=np.zeros((na,na),complex);X[r,r]=1j;directions.append(X)
            for k in range(r):
                X=np.zeros((na,na),complex);X[r,k]=1;X[k,r]=-1;directions.append(X)
                X=np.zeros((na,na),complex);X[r,k]=X[k,r]=1j;directions.append(X)
            for X in directions:
                old_count+=1;bb=[np.zeros((3,3),complex),np.zeros((2,2),complex)];bb[a]=X
                fine=[np.zeros((13,13),complex),np.zeros((8,8),complex)]
                for b in range(2):
                    for aa,nn in enumerate((3,2)):
                        for st in starts[b,aa]:fine[b][st:st+nn,st:st+nn]=bb[aa]
                dy=left_rep(fine)@Y;dk=J.conj().T@dy
                gg=-2*ZETA*np.trace(res@K.conj().T@dk).real
                near(gg,0,'old A2 output frames neutral',2e-19)
    check(old_count==13,'all13 old-left algebra directions')
    return {'random_full_endpoint_directions':tests,'law_changing_source':float(g),
            'old_A2_left_directions':old_count,'all_A5_rows_claimed_neutral':False}


def gap_negative_control():
    _,_,J,Q,R,P,M=structural_data()
    c=.61;U=left_rep(lift(np.array([[c]])));Y=U@J
    # Rotate one genuine success vector into unused space inside M: same effect,
    # lost return. This tests second order without altering the claimed base.
    a=J[:,3] # row1 right0, fixed returning sector
    rest=M-P
    k=int(np.argmax(np.real(np.diag(rest))))
    b=rest[:,k];b/=la.norm(b)
    X=np.outer(b,a.conj())-np.outer(a,b.conj())
    near(M@X,X@M,'same-effect finite control support')
    E0=Y.conj().T@M@Y
    vals=[]
    for t in (.05,.1):
        V=la.expm(t*X);Yt=V@Y;Kt=J.conj().T@Yt
        Et=Yt.conj().T@M@Yt;gap=Et-Kt.conj().T@Kt
        near(Et,E0,'finite same-effect comparator')
        gap_norm=float(la.norm(gap,2))
        near(gap_norm,math.sin(t)**2,'true nonzero second-order return gap')
        L=(M-P)@Yt
        near(gap,L.conj().T@L,'whole positive gap identity')
        vals.append({'t':t,'gap_norm':gap_norm})
    return {'controls':vals,'new_reflection_after_perturbation_claimed':False}


def matrix_corner_control():
    _,_,J,Q,R,P,M=structural_data(2)
    C=np.array([[.3,.07j],[-.07j,.61]],complex)
    D=np.array([[.04,.03+.01j],[.03-.01j,-.02]],complex)
    check(la.norm(C@D-D@C)>1e-3,'genuinely noncommuting matrix jet')
    S=la.sqrtm(np.eye(2)-C@C).astype(complex)
    dS=la.solve_sylvester(S,S,-(C@D+D@C))
    b=lift(C);db=[]
    for nb,pairs in zip((13,8),PAIRS):
        x=np.zeros((2*nb,2*nb),complex)
        for a,k in pairs:
            ia=slice(2*a,2*a+2);ib=slice(2*k,2*k+2)
            x[ia,ia]=D;x[ib,ib]=-D;x[ia,ib]=dS;x[ib,ia]=dS
        db.append(x)
    U=left_rep(b,2);dU=left_rep(db,2);Y=U@J;dy=dU@J
    K=J.conj().T@Y;dK=J.conj().T@dy
    near(K,expected_corner(C),'matrix corner exact canonical compression')
    near(Y.conj().T@M@Y,K.conj().T@K,'matrix corner intrinsic effect')
    near(dy.conj().T@M@Y+Y.conj().T@M@dy,dK.conj().T@K+K.conj().T@dK,'matrix source with noncommuting derivative')
    res=la.inv((1-ZETA)*np.eye(26)+ZETA*K.conj().T@K)
    g=-2*ZETA*np.trace(res@K.conj().T@dK).real
    exact=-6*ZETA*np.trace(la.solve((1-ZETA)*np.eye(2)+ZETA*C@C,C@D+D@C)).real
    near(g,exact,'full matrix source multiplicity six',2e-18)
    h=2e-5
    def price(t):
        A=C+t*D
        return -6*np.log1p(-ZETA*(1-la.eigvalsh(A)**2)).sum()
    fd=(-price(2*h)+8*price(h)-8*price(-h)+price(-2*h))/(12*h)
    near(fd,g,'independent matrix scalar finite difference',2e-15)
    return {'DATA_dimension':2,'complete_GNS_dimension':466,'canonical_inputs':26,
            'actual_source':float(g),'finite_difference_error':float(abs(fd-g))}


def full_heat():
    sizes=(9,11,13);degrees=(26,24,22)
    B=np.zeros((3,3));C=np.diag(1/np.array(degrees,dtype=float))
    for i in range(3):
        for j in range(3):
            if i!=j:B[i,j]=math.sqrt(sizes[i]*sizes[j]/(degrees[i]*degrees[j]))
    def heat_angles(angles,N):
        angles=np.asarray(angles)
        x=np.cos((angles[:,None]+2*math.pi*np.arange(N))/N).reshape(-1)
        L=np.eye(3)[None]-B[None]-2*x[:,None,None]*C[None]
        eig=la.eigvalsh(L[0]) if len(x)==1 else np.linalg.eigvalsh(L)
        tr=np.exp(-BETA*eig).sum(axis=-1)
        for n,d in zip(sizes,degrees):tr+=(n-1)*np.exp(-BETA*(1-2*x/d))
        Z0=tr.sum();D=len(angles)
        Z01=2*Z0+359*N*D
        return math.log(Z01)/BETA
    angles=np.array([0.]*178+[math.pi]*55)
    records=[]
    for N in (3,4,7):
        H=heat_angles(angles,N)
        vals=[]
        for c in (.23,.61,.93):
            U=left_rep(lift(np.array([[c]])))
            computed=np.angle(la.eigvals(U))
            val=heat_angles(computed,N)
            near(val,H,'whole Hodge heat equal across family',3e-13)
            vals.append(val)
        records.append({'N':N,'H':H,'full_modes':425*N*233,'harmonic_modes':359*N*233})
    # Every heat first jet vanishes, but full heat need not stay constant on
    # arbitrary finite perturbations. Compare a genuine nonreflection +/- path.
    U=left_rep(lift(np.array([[.61]])))
    X=np.zeros((233,233),complex);X[0,0]=1j;X[5,17]=.3;X[17,5]=-.3
    a=heat_angles(np.angle(la.eigvals(la.expm(.08*X)@U)),3)
    b=heat_angles(np.angle(la.eigvals(la.expm(-.08*X)@U)),3)
    near(a,b,'full heat even on endpoint skew path',3e-13)
    return {'whole_spectrum_multiplicities':{'plus':178,'minus':55},'controls':records,
            'huge_square_Hodge_matrix_materialized':False}


def pointwise_field():
    torch.set_default_dtype(torch.float64);torch.set_num_threads(1)
    eta=torch.diag(torch.tensor([1.,-1.,-1.,-1.]))
    pairs=[(a,b) for a in range(4) for b in range(a+1,4)]
    v0=torch.tensor([1.,.1,-.2,.05]);v1=torch.tensor([.2,.4,.1,-.3])
    def I_field(y):
        e=torch.eye(4)+y[:16].reshape(4,4);ie=torch.linalg.inv(e)
        g=e.T@eta@e;gi=torch.linalg.inv(g);ws=[]
        for mu in range(4):
            rows=[]
            for a in range(4):
                row=[]
                for b in range(4):
                    if a==b:row.append(0*y[0])
                    else:
                        k=pairs.index((min(a,b),max(a,b)))
                        row.append((1 if a<b else -1)*y[16+6*mu+k]*eta[b,b])
                rows.append(torch.stack(row))
            ws.append(torch.stack(rows))
        R=0*y[0]
        for mu in range(4):
            for nu in range(4):
                F=(ws[mu]@ws[nu]-ws[nu]@ws[mu])@eta
                R+=torch.einsum('a,b,ab->',ie[mu],ie[nu],F)
        f=torch.linalg.det(e)*R/2
        q=y[40]**2*(v0@gi@v0)+y[41]**2*(v1@gi@v1)
        tau=BETA;x=tau*f;yy=tau*q
        ep=P_GOLD**2*(1+x);ell=4*ep*(1-ep);b=P_GOLD-P_GOLD**2*yy
        BB=4*b*b*(1-b*b);AA=ell+(1-ell)*BB
        return ZETA*(AA+BB)-ZETA**2*AA*BB
    _,_,J,*_=structural_data()
    J=torch.tensor(J.real)
    alpha=4*P_GOLD**2;gamma=P_GOLD**2
    y=torch.linspace(-.025,.03,42);y[40]=.19;y[41]=-.13;y.requires_grad_(True)
    P=I_field(y);c=torch.sqrt(1-alpha*gamma*P*(1-gamma*P));s=torch.sqrt(1-c*c)
    fine=[]
    for nb,pp in zip((13,8),PAIRS):
        U=torch.eye(nb)
        # Every entry is assigned using the actual full fine operator.
        for a,b in pp:
            U[a,a]=c;U[b,b]=-c;U[a,b]=s;U[b,a]=s
        fine.append(torch.kron(U,torch.eye(nb)))
    U=torch.block_diag(*fine);K=J.T@U@J
    D=(1-ZETA)*torch.eye(13)+ZETA*K.T@K
    price=-torch.linalg.slogdet(D)[1] # H is exactly constant, NOT omitted residual.
    gb=torch.autograd.grad(price,y,retain_graph=True)[0]
    gi=torch.autograd.grad(P,y,retain_graph=True)[0]
    gain=6*ZETA*alpha*gamma*(1-2*gamma*P)/(1-ZETA*alpha*gamma*P*(1-gamma*P))
    error=float(torch.max(torch.abs(gb-gain*gi)).detach())
    check(error<1e-21,'all42 full reflected-source chain')
    check(float(torch.linalg.norm(gi))>1e-9,'not testing a fitted stationary field')
    return {'coordinates':42,'I_value':float(P.detach()),'exact_full_gain':float(gain.detach()),
            'nonzero_field_gradient_norm':float(torch.linalg.norm(gi).detach()),
            'source_chain_error':error,'full_lattice_root_computed':False}


def main():
    out={'input_commit':'f8a1d89329e5f44a8f49118dac004d1bc46cc417',
         'exact':symbolic_algebra(),'canonical_cases':archive_and_corner(),
         'all_control_source':arbitrary_sources(),'negative_gap':gap_negative_control(),
         'matrix_corner':matrix_corner_control(),'whole_heat':full_heat(),'pointwise_field':pointwise_field()}
    out.update({'checks':CHECKS,'max_errors':ERRORS,'status':'PASS_CANONICAL_BALANCED_REFLECTION_SOURCE',
        'native_compiler_emitted':False,'intrinsic_effect_physically_recorded':False,
        'physical_variation_domain_derived':False,'original_full128_instrument_identified':False,
        'GR_closed':False,'Lean_or_CI_run':False,
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                       'sympy':sp.__version__,'torch':torch.__version__}})
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
