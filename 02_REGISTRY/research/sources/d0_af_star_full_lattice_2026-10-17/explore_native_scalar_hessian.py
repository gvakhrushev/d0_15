#!/usr/bin/env python3
"""Exploratory full finite-B Fourier scalar Hessian. No old root replay."""
import argparse,ast,hashlib,importlib.util,json,time
from pathlib import Path
import numpy as np
import sympy as s

def run(root,q_index=1,L=8,R=None):
    np.seterr(divide='raise',over='raise',invalid='raise');root=Path(root).resolve();stamp=time.perf_counter()
    creator_path=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node=next(n for n in ast.parse(creator_path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    if pin!='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4':raise ValueError('creator drift')
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if j&(1<<i)) for j in range(16)]}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(creator_path),'exec'),ns)
    C=np.array([np.array(ns['creator'](s.eye(4)[:,i])).astype(float) for i in range(4)])
    v8=root/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    center=next(ast.literal_eval(n.value) for n in ast.parse(v8.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CENTER' for t in n.targets))
    d,o=map(float,center);ell=1/L;p=(np.sqrt(5)-1)/2;alpha=p*p/(128*L*L);m=256*L*L;beta=m*alpha;z=2**-20;M=128
    a0=np.sqrt(d-o);b0=(np.sqrt(d+3*o)-a0)/4;F=a0*np.eye(4)+b0*np.ones((4,4));eta=np.diag([1.,-1.,-1.,-1.]);U=eta@F.T
    grid=np.indices((L,)*4).reshape(4,-1).T;ng=len(grid)
    t=np.exp(2j*np.pi*grid/L);zet=t-1
    ind=((grid+np.array([q_index,0,0,0]))%L)
    li=np.ravel_multi_index(ind.T,(L,)*4)
    AA=L*L*np.sum(np.abs(zet)**2,axis=1);CC=L*L*(np.abs(np.sum(zet,axis=1))**2-np.sum(np.abs(zet)**2,axis=1))
    target=4*L*L*np.sin(np.pi/L)**2
    def source(d,o):
        en=d*AA+o*CC;bn=1-alpha*en;ee=np.exp(m*np.log1p(-alpha*en));zn=np.sum(ee);rr=z*ee/(1-z+z*ee)
        feat=np.array([AA,CC]);mu=np.einsum('ik,k->i',feat,ee/bn)/zn
        fun=mu-2048*beta*np.einsum('ik,k->i',feat,rr/bn)-np.array([target,0.])
        jac=(alpha-beta)*np.einsum('ik,jk,k->ij',feat,feat,ee/bn**2)/zn+beta*np.outer(mu,mu)
        jac-=2048*beta*np.einsum('ik,jk,k->ij',feat,feat,rr*(alpha-beta*(1-rr))/bn**2)
        return fun,jac
    if L!=8:
        d=.060; o=0.
        for _ in range(8):
            fun,jac=source(d,o);step=np.linalg.solve(jac,fun);d-=step[0];o-=step[1]
            if np.max(np.abs(step))<1e-15:break
        a0=np.sqrt(d-o);b0=(np.sqrt(d+3*o)-a0)/4;F=a0*np.eye(4)+b0*np.ones((4,4));U=eta@F.T
    root_source=source(d,o)[0]
    Cu=np.einsum('ar,aij->rij',U,C)
    E=d*AA+o*CC
    B=1-alpha*E;ee=np.exp(m*np.log1p(-alpha*E));aa=ee/B;ZZ=16*np.sum(ee);ff=1-z+z*ee
    chi=(np.sum((grid!=0),axis=1)==1)&np.any((grid==1)|(grid==L-1),axis=1)
    if chi.sum()!=8:raise ArithmeticError('occupied shell')
    kap=-aa/ZZ+M*z*beta*aa/ff;weights=kap+chi/128
    de=E[li]-E;lr=np.log1p(-alpha*de/B)
    da=aa*np.expm1((m-1)*lr);dee=ee*np.expm1(m*lr)
    dk=-da/ZZ+M*z*beta*(da*ff-aa*z*dee)/(ff[li]*ff)
    ap=-alpha*(m-1)*ee/B**2;fp=-z*beta*aa
    slope=-ap/ZZ+M*z*beta*(ap/ff-aa*fp/ff**2)
    dd=np.empty(ng);ok=np.abs(de)>1e-12
    dd[ok]=(dk[ok]+(chi[li].astype(int)-chi.astype(int))[ok]/128)/de[ok]
    dd[~ok]=slope[~ok]
    if np.any(chi[li][~ok]!=chi[~ok]):raise ArithmeticError('partial energy shell')
    S=[]
    x=np.zeros((4,4));x[0,0]=1;S.append(x)
    x=np.zeros((4,4));x[0,1:]=1;x[1:,0]=-1;S.append(x)
    x=np.diag([0.,1.,1.,1.]);S.append(x)
    x=np.zeros((4,4));x[1:,1:]=1-np.eye(3);S.append(x)
    x=np.zeros((4,4));x[0,1:]=1;x[1:,0]=1;S.append(x)
    modpath=root/'02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/check_native_scalar_link_block.py'
    spec=importlib.util.spec_from_file_location('scalar_basis',modpath);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    families=np.array(module.scalar_link_basis()).astype(float)
    link_left=[]
    for family in families:
        gam=np.einsum('rab,aik,bkj->rij',family,C,C.transpose(0,2,1))
        link_left.append(np.einsum('rij,rjk->rik',Cu,gam,optimize=False))
    signed=np.where(grid<=L//2,grid,grid-L)
    selected=np.arange(ng) if R is None else np.flatnonzero(np.max(np.abs(signed),axis=1)<=R)
    term1=np.zeros((9,9),complex);term2=term1.copy();normalizer_A=np.zeros(9,complex)
    for off in range(0,len(selected),256):
        ix=selected[off:off+256];ll=li[ix]
        Dk=(np.einsum('kr,rij->kij',zet[ix],Cu)+np.einsum('kr,rji->kij',zet[ix].conj(),Cu))/ell
        Dl=(np.einsum('kr,rij->kij',zet[ll],Cu)+np.einsum('kr,rji->kij',zet[ll].conj(),Cu))/ell
        V=[]
        for X in S:
            dc=np.einsum('ar,aij->rij',X@U,C)
            V.append((np.einsum('kr,rij->kij',zet[ix],dc)+np.einsum('kr,rji->kij',zet[ll].conj(),dc))/ell)
        for left in link_left:
            V.append((np.einsum('kr,rij->kij',t[ix],left)+np.einsum('kr,rij->kij',t[ll].conj(),left.transpose(0,2,1)))/ell)
        V=np.array(V)
        Q=np.einsum('kij,akjl->akil',Dl,V,optimize=False)+np.einsum('akij,kjl->akil',V,Dk,optimize=False)
        term1+=np.einsum('akij,bkij,k->ab',V.conj(),V,weights[ix]+weights[ll],optimize=False)
        term2+=np.einsum('akij,bkij,k->ab',Q.conj(),Q,dd[ix],optimize=False)
        if q_index==0:normalizer_A+=np.einsum('k,akii->a',aa[ix],Q,optimize=False)
    K=term1+term2
    if q_index==0:K-=beta/ZZ**2*np.outer(normalizer_A.conj(),normalizer_A)
    Herm=np.max(np.abs(K-K.conj().T));K=(K+K.conj().T)/2
    Kn=K[4:,4:];Cmix=K[4:,:4];red=K[:4,:4]-Cmix.conj().T@np.linalg.solve(Kn,Cmix)
    star=np.array([-(a0+b0),((a0+b0)/np.sqrt(3)-b0)/2,-b0/np.sqrt(3),-b0/np.sqrt(3)])
    normals=-np.linalg.solve(Kn,Cmix@star)
    nulls=[np.array([1.,0,0,0]),star]
    moments=np.einsum('k,kr,ks->rs',weights,zet,zet.conj())
    def mat(a):return {'real':a.real.tolist(),'imag':a.imag.tolist()}
    return {'status':'EXPLORATORY_FLOAT64','L':L,'q':[q_index,0,0,0],'carrier_momenta':ng,'CAR':16,'reference':128,'root_center':center,'accepted_root_radius':'1e-12' if L==8 else 'UNVALIDATED_NEWTON','d':d,'o':o,'source_residual':root_source.tolist(),'matrix_momenta':len(selected),'matrix_cutoff':R,
       'input_pins':{str(creator_path.relative_to(root)):pin,str(v8.relative_to(root)):hashlib.sha256(v8.read_bytes()).hexdigest()},
       'normalization':'base +q coefficient1; real Hessian=1/2 [[ReK,ImK],[-ImK,ReK]] for +cos,+sin amplitudes',
       'calibrations':{'alpha':alpha,'m':m,'beta':beta,'z':z,'M':M},'coframe_basis':'E00, sum(E0i-Ei0), Isp, offdiagSp, sum(E0i+Ei0); deltaU=S U',
       'root_moment_max':float(np.max(np.abs(moments))),'Hermitian_error':float(Herm),'minimum_paired_energy_difference':float(np.min(np.abs(de))),
       'K':mat(K),'term1':mat(term1),'term2':mat(term2),'link4_eigenvalues':np.linalg.eigvalsh(K[5:,5:]).tolist(),
       'normal5_eigenvalues':np.linalg.eigvalsh(Kn).tolist(),'scalar9_eigenvalues':np.linalg.eigvalsh(K).tolist(),
       'metric4_reduced':mat(red),'metric4_eigenvalues':np.linalg.eigvalsh(red).tolist(),'star_metric':star.tolist(),
       'star_reduced_source':mat(red@star),'star_normal_response':mat(normals),'star_quadratic':float(np.real(star@red@star)),
       'soft_s':float(np.real(K[4,4]-K[4,5:]@np.linalg.solve(K[5:,5:],K[5:,4]))),'soft_t':mat(K[4,:4]-K[4,5:]@np.linalg.solve(K[5:,5:],K[5:,:4])),
       'source_without_observer_normal':mat((K[:4,:4]-K[:4,5:]@np.linalg.solve(K[5:,5:],K[5:,:4]))@star),
       'elapsed_seconds':time.perf_counter()-stamp,'proof_scope':'float64 exploration only; not interval-certified inertia or curved roots; full finiteB and both phases retained'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--q',type=int,default=1);ap.add_argument('--L',type=int,default=8);ap.add_argument('--R',type=int);args=ap.parse_args()
    out=run(args.root,args.q,args.L,args.R);txt=json.dumps(out,indent=2)+'\n'
    if args.output:args.output.write_text(txt)
    print(json.dumps({k:out[k] for k in ['status','normal5_eigenvalues','metric4_eigenvalues','star_reduced_source','star_quadratic','root_moment_max','Hermitian_error','elapsed_seconds']},indent=2))
