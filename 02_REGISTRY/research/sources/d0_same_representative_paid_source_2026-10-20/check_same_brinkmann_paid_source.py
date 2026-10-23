#!/usr/bin/env python3
"""Same-representative original paid-port source on the exact J2 Brinkmann family.

Consumes the pinned primary all40+2 theorem, complete 128-outcome channel,
paid two-round identity and exact null-probe theorem at 313923d2.
New analytic theorem: scalar/top versus odd-clock CAR parity isolates a
nonzero paid material Hessian; no Book03 price or GR closure is selected.
Numerical sparse controls are author replay, not rigorous interval acceptance.
Dependencies: numpy and scipy. Read-only unless --output is supplied.
"""
from __future__ import annotations
import numpy as np
from scipy import sparse
from scipy.linalg import expm, solve_sylvester
from itertools import combinations
import json,time

p=(np.sqrt(5.)-1)/2
z=2.**-20
lam=-2*p**-5*((1-z*4*p**3*(1+p**6))/(1-z*4*p**3)+p**6)
eta=np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1.]],float)
I16=np.eye(16)
creators=[]
for a in range(4):
    c=np.zeros((16,16))
    for mask in range(16):
        if not mask&(1<<a):
            c[mask|(1<<a),mask]=(-1)**((mask&((1<<a)-1)).bit_count())
    creators.append(c)
creators=np.array(creators)
subsets={j:[tuple(a for a in range(4) if mask&(1<<a)) for mask in range(16) if mask.bit_count()==j] for j in range(5)}
masks={j:[mask for mask in range(16) if mask.bit_count()==j] for j in range(5)}
def wedge(U):
    out=np.zeros((16,16))
    for j in range(5):
        for im,idx in zip(masks[j],subsets[j]):
            for jm,jdx in zip(masks[j],subsets[j]):
                out[im,jm]=np.linalg.det(U[np.ix_(idx,jdx)]) if j else 1.
    return out

def root_psd(A):
    w,v=np.linalg.eigh((A+A.T.conj())/2)
    if np.min(w)<-1e-10:raise ValueError(f'outside Julia: {np.min(w)}')
    return (v*np.sqrt(np.maximum(w,0)))@v.T.conj(),float(w.min())

def E(a,b):
    v=np.zeros((4,4));v[a,b]=1.;return v
N2=E(1,2)+E(2,0)
N3=E(1,3)+E(3,0)
LIE=[(E(a,b)-E(b,a))@eta for a in range(4) for b in range(a+1,4)]


class Fixture:
    def __init__(self,L=8,amp=.01,weyl=.03,nu=.6):
        self.L=L; self.h=1/L;self.nu=nu;self.amp=amp;self.weyl=weyl
        self.k=2*np.pi;self.energy=amp**2*self.k**2
        self.ah=amp*self.k*self.h/(2*np.sin(self.k*self.h/2))
        assert self.ah**2<p*p
        self.c=-lam*self.energy
        self.eps=p*p*self.h*self.h/64
        self.sites=[(ix,iy) for ix in range(L) for iy in range(L)]
        self.xy=np.array([((ix-L//2)*self.h,(iy-L//2)*self.h) for ix,iy in self.sites])
        self.M=L*L;self.dim=16*self.M
        self.center=(L//2)*L+L//2
        def H(x,y):return self.c*(x*x+y*y)+weyl*(x*x-y*y)
        self.Hfun=H
        Hs=np.array([H(x,y) for x,y in self.xy])
        self.Hs=Hs
        V=np.tile(nu*np.array([[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1.]]),(self.M,1,1))
        V[:,1,1]=-nu*Hs/2
        self.V=V
        self.U=np.tile(np.eye(4),(4,self.M,1,1))
        for j,(x,y) in enumerate(self.xy):
            # Exact native coframe S=diag(1,1,-1,-1), hence true link sign -.
            X=-(H(x,y)-H(x-self.h,y))*N2/2-(H(x,y)-H(x,y-self.h))*N3/2
            self.U[0,j]=np.eye(4)+X+X@X/2
        ident=sparse.eye(self.M,format='csr')
        self.shift=[];self.prev=[]
        for r in range(4):
            if r<2:
                sh=ident;pr=np.arange(self.M)
            else:
                to=[];pr=[]
                for ix,iy in self.sites:
                    tx,ty=(ix+1,iy) if r==2 else (ix,iy+1)
                    to.append((tx%L)*L+(ty%L))
                    px,py=(ix-1,iy) if r==2 else (ix,iy-1)
                    pr.append((px%L)*L+(py%L))
                sh=sparse.csr_matrix((np.ones(self.M),(np.arange(self.M),to)),shape=(self.M,self.M))
                pr=np.array(pr)
            self.shift.append(sparse.kron(sh,sparse.eye(16),format='csr'));self.prev.append(pr)
        self.state=[];self.dstate=[]
        chi=np.zeros(self.M);chi[self.center]=1
        self.chi=chi
        for q in [0,1,-1]:
            w=np.zeros((self.M,16),complex);dw=w.copy()
            if q==0:
                w[:,1]=np.sqrt(p);w[:,14]=np.sqrt(p*p-self.ah**2)
                dw[:,14]=-chi*self.ah**2/np.sqrt(p*p-self.ah**2)
            else:
                w[:,0]=self.ah/2;w[:,15]=-q*1j*self.ah/2
                dw=chi[:,None]*w
            self.state.append(w.reshape(-1)/L);self.dstate.append(dw.reshape(-1)/L)
        assert abs(sum(np.vdot(v,v).real for v in self.state)-1)<1e-13
        assert abs(sum(np.vdot(v,dv).real for v,dv in zip(self.state,self.dstate)))<1e-13

    def price(self,parts,states=None,grad=False):
        if states is None:states=self.state
        R=Gamma=0.
        out=[]
        for (D,Ws),v in zip(parts,states):
            dv=D@v;ddv=D@dv
            rr=np.vdot(dv,dv).real
            t=0.;tv=np.zeros_like(v)
            for W in Ws:
                wdv=W@dv; dwdv=D@wdv
                t+=np.vdot(dwdv,dwdv).real/16
                if grad:tv+=W.conj().T@(D@dwdv)/16
            gg=t-np.vdot(ddv,ddv).real
            R+=rr;Gamma+=gg
            if grad:
                Hnv=2*p*self.eps*ddv+p*self.eps**2*(D@tv-D@(D@ddv))
                out.append(Hnv)
        excess=2*p*self.eps*R+p*self.eps**2*Gamma
        ret={'R':R,'Gamma':Gamma,'port_excess':excess,'port_price':2+excess}
        if grad:ret['state_covector']=out
        return ret

    def verify_geometry(self):
        h=self.h
        errs=[]
        for ix in range(1,self.L-1):
            for iy in range(1,self.L-1):
                x,y=self.xy[ix*self.L+iy];H=self.Hfun
                lap=(H(x+h,y)+H(x-h,y)+H(x,y+h)+H(x,y-h)-4*H(x,y))/h**2
                errs.append(lap+4*lam*self.energy)
        # exact derivative increments from same periodic finite CAR sampling
        js=np.arange(self.L)
        ps=np.stack([self.ah*np.cos(self.k*h*js),self.ah*np.sin(self.k*h*js)],axis=1)
        diff=(np.roll(ps,-1,axis=0)-ps)/h
        src=np.sum(diff**2,axis=1)
        return {'all40plus2_reduction_max_residual':float(max(abs(np.array(errs)))), 'CAR_energy_max_error':float(max(abs(src-self.energy))), 'Ric_uu':2*self.c,'Weyl_A':self.weyl, 'finite_scalar_amplitude':self.ah}

# All zero-filled matrices below are sparse, with site-index support retained.
def block_sparse(blocks,dim):
    return sparse.block_diag(list(blocks),format='csr')

def build_cached(f):
    meta=[];margin=1.
    for r in range(4):
        cb=np.einsum('za,aij->zij',f.V[:,:,r],creators)
        ub=np.array([wedge(u) for u in f.U[r]])
        pb=cb@ub
        C=sparse.block_diag(list(cb),format='csr')
        P=sparse.block_diag(list(pb),format='csr')@f.shift[r]
        root_arrays=[]
        for flag in range(4):
            arr=[]
            for j in range(f.M):
                if flag==0:A=I16-pb[j]@pb[j].T
                elif flag==1:A=I16-pb[f.prev[r][j]].T@pb[f.prev[r][j]]
                elif flag==2:A=I16-cb[j]@cb[j].T
                else:A=I16-cb[j].T@cb[j]
                w,v=np.linalg.eigh((A+A.T)/2);margin=min(margin,float(w.min()))
                assert w.min()>0
                arr.append((v*np.sqrt(w))@v.T)
            root_arrays.append(np.array(arr))
        roots=[sparse.block_diag(list(a),format='csr') for a in root_arrays]
        meta.append({'cb':cb,'ub':ub,'pb':pb,'C':C,'P':P,'root_arrays':root_arrays,'roots':roots})
    parts=[]
    for q in [0,1,-1]:
        pp=[(np.exp(1j*q*f.k*f.h) if r==0 else 1)*m['P'] for r,m in enumerate(meta)]
        dd=sum((pp[r]-meta[r]['C'] for r in range(4)),start=sparse.csr_matrix((f.dim,f.dim),dtype=complex))/f.h
        D=(dd+dd.conj().T).tocsr();Ws=[]
        for r,m in enumerate(meta):
            lp,rp,lc,rc=m['roots'];C=m['C'];P=pp[r]
            Ws.extend([P,P.conj().T,lp,rp,C,C.conj().T,lc,rc])
        parts.append((D,Ws))
    return parts,meta,margin

def generator_ext(X):
    return sum((X[a,b]*creators[a]@creators[b].T for a in range(4) for b in range(4)),start=np.zeros((16,16)))

def local_block(j,M,dim):
    # Exact placement; omit literal zeros, not small values.
    rows,cols=np.nonzero(M)
    return sparse.csr_matrix((M[rows,cols],(j*16+rows,j*16+cols)),shape=(dim,dim))

def analytic_direction(f,meta,r,kind,a):
    j=f.center;m=meta[r];C=m['cb'][j];U=m['ub'][j];B=m['pb'][j]
    dc=np.zeros((16,16));du=dc.copy()
    if kind=='coframe':dc=creators[a]
    elif kind=='link':du=generator_ext(LIE[a])@U
    else:raise ValueError(kind)
    db=dc@U+C@du
    dC=local_block(j,dc,f.dim)
    dP=local_block(j,db,f.dim)@f.shift[r]
    # Source of every genuine positive Julia square root; no root is frozen.
    roots=m['root_arrays']
    jj=int(np.where(f.prev[r]==j)[0][0])
    mats=[-(db@B.T+B@db.T),-(db.T@B+B.T@db),-(dc@C.T+C@dc.T),-(dc.T@C+C.T@dc)]
    positions=[j,jj,j,j]
    dR=[];max_error=0.
    for rootarr,A,pos in zip(roots,mats,positions):
        root=rootarr[pos]
        droot=solve_sylvester(root,root,A)
        max_error=max(max_error,float(np.max(np.abs(root@droot+droot@root-A))))
        dR.append(local_block(pos,droot,f.dim))
    result=[]
    for q in [0,1,-1]:
        phase=np.exp(1j*q*f.k*f.h) if r==0 else 1
        dpp=phase*dP
        d=(dpp-dC)/f.h
        dD=(d+d.conj().T).tocsr()
        lp,rp,lc,rc=dR
        widx=[(8*r+k,x) for k,x in enumerate([dpp,dpp.conj().T,lp,rp,dC,dC.conj().T,lc,rc])]
        result.append((dD,widx))
    return result,max_error

def cache_values(parts,states):
    cache=[]
    for (D,Ws),v in zip(parts,states):
        d=D@v;dd=D@d;ys=[];ts=[];dts=[];tau=np.zeros_like(v)
        for W in Ws:
            y=W@d;t=D@y;dt=D@t
            ys.append(y);ts.append(t);dts.append(dt)
            tau+=W.conj().T@dt/16
        cache.append({'d':d,'dd':dd,'ys':ys,'ts':ts,'dts':dts,'tau':tau})
    return cache

def field_source(f,parts,cache,jets):
    dR=dG=0.
    for (D,Ws),v,b,(dD,dWs) in zip(parts,f.state,cache,jets):
        dx=dD@v
        dR+=2*np.vdot(b['d'],dx).real
        term=0j
        for y,t in zip(b['ys'],b['ts']):term+=np.vdot(t,dD@y)/16
        for idx,dW in dWs:term+=np.vdot(b['dts'][idx],dW@b['d'])/16
        term+=np.vdot(b['tau'],dx)
        term-=np.vdot(b['dd'],dD@b['d']+D@dx)
        dG+=2*term.real
    return 2*p*f.eps*dR+p*f.eps**2*dG, dR,dG

def native_row_check(f,parts):
    # A bounded explicit reconstruction of ALL64 label/coefficient rows,
    # from exactly the original 32 paired words; no array indexed by exits only.
    D,Ws=parts[1]
    words=[]
    for r in range(4):
        P,PH,LP,RP,C,CH,LC,RC=Ws[8*r:8*r+8]
        for x,y in [(P,LP),(PH,RP),(-C,-LC),(-CH,-RC)]:
            words.extend([(x,y),(x,y)])
    rows=[]
    for label in range(32):
        signs=[(-1)**((label&j).bit_count())/32 for j in range(32)]
        for coeff in range(2):
            rows.append(sum((signs[j]*words[j][coeff] for j in range(32)),start=sparse.csr_matrix((f.dim,f.dim),dtype=complex)).tocsr())
    A=f.h*D/16
    errA=(rows[0]-A)
    Aerr=float(max(abs(errA.data),default=0))
    rng=np.random.default_rng(7121)
    v=rng.normal(size=f.dim)+1j*rng.normal(size=f.dim);v/=np.linalg.norm(v)
    row_norm=sum(np.vdot(N.conj().T@v,N.conj().T@v).real for N in rows)
    # Direct all128 channel on a pure state: total norm and mean two-round cost
    # need only the all128 first rows and the exact second-round port effect.
    psi=f.state[1]/np.linalg.norm(f.state[1]);apsi=A@psi
    norm=mean=0.
    for j,N in enumerate(rows):
        vj=N.conj().T@apsi
        for b in [0,1]:
            out=((psi if j==0 else 0)-2*p*p*vj) if b==0 else -2*p*np.sqrt(p)*vj
            w=np.vdot(out,out).real
            norm+=w
            # C_first=1+b; C_second=1 + actual second port expectation
            mean+=(2+b)*w+p*f.eps*np.vdot(D@out,D@out).real
    direct=f.price([parts[1]],states=[psi]) # price accepts general zipped parts
    return {'row_blank_A_error':Aerr,'row_completeness_random_error':abs(row_norm-1),'all128_total_mass_error':abs(norm-1),'all128_two_round_price_error':abs(mean-direct['port_price'])}


def main():
    import argparse,platform,hashlib
    import scipy
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--L',type=int,default=10)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.L<4 or args.L%2:
        parser.error('L must be even and >=4; L=10 keeps the source away from the wrap collar')
    f=Fixture(args.L,.01,.03)
    parts,meta,margin=build_cached(f)
    cost=f.price(parts,grad=True);g=cost.pop('state_covector')
    material=2*sum(np.vdot(dm,gm).real for dm,gm in zip(f.dstate,g))
    assert material>0
    cache=cache_values(parts,f.state)
    rows={};root_error=0.
    for kind,count in [('coframe',4),('link',6)]:
        rows[kind]=[]
        for r in range(4):
            for a in range(count):
                js,err=analytic_direction(f,meta,r,kind,a)
                root_error=max(root_error,err)
                value,dR,dGamma=field_source(f,parts,cache,js)
                rows[kind].append({'role':r,'component':a,'source':value,'dR':dR,'dGamma':dGamma})
    assert root_error<1e-12
    geometry=f.verify_geometry()
    assert geometry['all40plus2_reduction_max_residual']<1e-10
    assert geometry['CAR_energy_max_error']<1e-12
    # Reconstruct both full material Euler rows on all u/transverse sites.
    us=np.arange(f.L)*f.h
    ps=np.stack([f.ah*np.cos(f.k*us),f.ah*np.sin(f.k*us)],axis=1)
    b=np.sqrt(p*p-f.ah**2)
    material_rows=[]
    for j,u in enumerate(us):
        loc=sum(np.exp(1j*q*f.k*u)*v.reshape(f.M,16) for q,v in zip([0,1,-1],g))
        material_rows.append(np.stack([
            2/f.L**3*(loc[:,0]-ps[j,0]*loc[:,14]/b).real,
            2/f.L**3*(loc[:,15]-ps[j,1]*loc[:,14]/b).real],axis=-1))
    material_rows=np.array(material_rows)
    contracted=f.L*sum(np.dot(material_rows[j,f.center],ps[j]) for j in range(f.L))
    assert abs(contracted-material)<1e-18
    # Independent normalized-preparation finite difference, holding geometry fixed.
    def curve(t):
        aa=f.ah*(1+t*f.chi);out=[]
        for q in [0,1,-1]:
            w=np.zeros((f.M,16),complex)
            if q==0:
                w[:,1]=np.sqrt(p);w[:,14]=np.sqrt(p*p-aa*aa)
            else:
                w[:,0]=aa/2;w[:,15]=-q*1j*aa/2
            out.append(w.reshape(-1)/f.L)
        assert abs(sum(np.vdot(x,x).real for x in out)-1)<1e-12
        return out
    step=1e-4
    fd=(f.price(parts,curve(step))['port_excess']-f.price(parts,curve(-step))['port_excess'])/(2*step)
    assert abs(fd-material)<max(1e-17,1e-7*abs(material))
    # Same actual null probes: BOTH reference and holonomy transported by S.
    probe=.25;Nb=[E(0,2)+E(2,1),E(0,3)+E(3,1)]
    decoded=[];marks=[]
    for i,nb in enumerate(Nb):
        x,y=f.xy[f.center];xx=x+f.h*(i==0);yy=y+f.h*(i==1)
        def u(a,b):
            K=-(f.Hfun(a,b)-f.Hfun(a-f.h,b))*N2/2-(f.Hfun(a,b)-f.Hfun(a,b-f.h))*N3/2
            return np.eye(4)+K+K@K/2
        P=u(x,y)@np.linalg.inv(u(xx,yy))
        mark=p*p*np.linalg.det(np.eye(4)+expm(-probe*nb)@P)**2/256
        marks.append(float(mark))
        decoded.append(float(4/probe*((mark/(p*p))**.25-1)))
    ric=-(decoded[0]+decoded[1])/f.h**2
    weyl=(decoded[1]-decoded[0])/(2*f.h**2)
    assert abs(ric-2*f.c)<1e-8 and abs(weyl-f.weyl)<1e-8
    # Exact finite CAR parity is the analytic mixed-source proof input.
    parity=np.diag([(-1)**mask.bit_count() for mask in range(16)])
    assert all(np.array_equal(parity@c@parity,-c) for c in creators)
    flat=Fixture(4,0,0);fp,fm,_=build_cached(flat)
    assert np.linalg.norm(fp[0][0]@flat.state[0])<1e-12
    kh=flat.k*flat.h;rh=kh/(2*np.sin(kh/2))
    kin=0.
    for q,(D,_) in zip([1,-1],fp[1:]):
        w=np.zeros((flat.M,16),complex)
        w[:,0]=rh/2;w[:,15]=-q*1j*rh/2;w=w.reshape(-1)/flat.L
        kin+=np.vdot(D@w,D@w).real
    assert abs(kin-flat.nu**2*flat.k**2)<1e-12
    parity_error=0.
    for r in range(4):
        for kind,count in [('coframe',4),('link',6)]:
            for a in range(count):
                js,_=analytic_direction(flat,fm,r,kind,a)
                for dD,_ in js:
                    v=(dD@flat.state[0]).reshape(flat.M,16)
                    parity_error=max(parity_error,float(np.max(abs(v[:,[m for m in range(16) if m.bit_count()%2]]))))
    assert parity_error==0
    small=Fixture(4,.01,.03);sp,_,_=build_cached(small)
    rowcheck=native_row_check(small,sp)
    assert max(rowcheck.values())<1e-12
    # Far-collar change: the L10 compact residual does not arise at a wrap.
    collar_error=None
    if f.L>=10:
        for j,(ix,iy) in enumerate(f.sites):
            if ix==0 or iy==0:
                f.V[j,1,1]-=.02
                f.U[0,j]=expm(.03*LIE[1])@f.U[0,j]
        pp,_,_=build_cached(f)
        gg=f.price(pp,grad=True)['state_covector']
        other=2*sum(np.vdot(dm,gm).real for dm,gm in zip(f.dstate,gg))
        collar_error=abs(other-material)
        assert collar_error<1e-18
    data={
      'status':'AUTHOR_NUMERICAL_REPLAY_PASS_NOT_INTERVAL_ACCEPTANCE',
      'input_ref':'313923d2dad60bff4038d8f4414528c9f3e5ad7a',
      'main_ref':'0bf309b6260cf5b63e54d6ccabdcdae6734b950a',
      'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
      'L':f.L,'h':f.h,'full_sites':f.L**4,'CAR_grades':16,
      'state_lift':'coherent counting-site lift of the owned normalized m_j; physical G0 admission not inferred',
      'physical_reference128_purification_selected':False,
      'native_port_rounds':2,'native_scene_J2_clock_identified':False,
      'nu':f.nu,'sigma':f.amp,'lambda_J2':lam,'positive_Julia_margin':margin,
      'configured_geometric_case':geometry,'same_actual_null_probe':{'strength':probe,'marks':marks,'amplitudes':decoded,'Ricci':ric,'Weyl':weyl},
      'paid_port_cost':cost,'compact_material_source':material,'finite_difference_material_source':fd,
      'material_source_over_2p_epsilon':material/(2*p*f.eps),
      'leading_source_from_observed_Ricci':-f.nu**2*ric/(lam*f.M),
      'all_16_plus_24_column_sources':rows,
      'two_material_rows_center_u0_over_h4_2p_epsilon':(material_rows[0,f.center]/(f.h**4*2*p*f.eps)).tolist(),
      'full_material_contraction_error':abs(contracted-material),
      'Julia_root_derivative_max_residual':root_error,
      'full128_original_row_check':rowcheck,
      'parity_mixed_geometry_material_error':parity_error,
      'flat_null_material_kinetic_coefficient':kin,
      'far_fixed_collar_change_error':collar_error,
      'Book03_full_action_selected':False,'GR_closed':False,
    }
    if args.output:
        args.output.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':
    main()
