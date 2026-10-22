#!/usr/bin/env python3
"""D0 original full N1 Golden price: 2-field flux elimination, rank-2 global
Schur completion and high-precision source check on real original six-face
rank-two time samples with a genuine off-diagonal coframe perturbation.
Research: the supplied CQ field price is not compulsory Book03 action.
"""
import mpmath as mp
mp.mp.dps=75
p=(mp.sqrt(5)-1)/2
z=mp.mpf(2)**-20
tau=mp.mpf(1)/20
lnphi=mp.log(1/p)
kappa=2*p**(-5)*( (1-z*4*p**3*(1+p**6))/(1-z*4*p**3)+p**6 )
amp=1/mp.sqrt(2*kappa)
F_NATIVE=[mp.mpf(s) for s in ('0.006509748179395618','0.012353000790314306','0.015961057861161802')]
X_NATIVE=[mp.mpf(s) for s in ('0.7788007830714048','0.7768506338626323','0.7717112422953042')]
SHIFT=[mp.mpf(s) for s in ('0.037575', '0.023455','0.012888')]
N=3;h=mp.mpf('0.12253434977211948')

def one_report(x,y):
    E=p*p*(1+x);ell=4*E*(1-E)
    u=p-p*p*y;B=4*u*u*(1-u*u)
    A=ell+(1-ell)*B
    rr=1-(1-z*B)*(1-z*A)
    return rr,ell,B,A,E,u

def der_report(x,y):
    rr,ell,B,A,E,u=one_report(x,y)
    drx=z*(1-z*B)*(1-B)*4*p*p*(1-2*E)
    dy=-8*p*p*u*(1-2*u*u)
    dry=z*dy*((1-z*A)+(1-z*B)*(1-ell))
    return rr,drx,dry
r0,ax,ay=der_report(0,0)
hp0=mp.log((1-r0)/r0)/lnphi
hphi=lambda r: -(r*mp.log(r)+(1-r)*mp.log1p(-r))/lnphi

def geometry(theta,j):
    fj,X,k=theta[3*j:3*j+3]
    a=X**(-2)-k*k
    b=X*k*amp
    c=-X*X*amp*amp
    return fj,X,k,a,b,c

def sq_q(theta,j,u):
    f,X,k,a,b,c=geometry(theta,j)
    return a*(u[0]**2+u[1]**2)+2*b*u[1]+c

def vv(x,y):
    rr,dx,dy=der_report(x,y)
    hp=mp.log((1-rr)/rr)/lnphi
    return -hp*dy/(hp0*ax)

def cell_price(theta,j,u,rhos):
    f,X,k,a,b,c=geometry(theta,j)
    rr=one_report(-tau*f/rhos[j],tau*sq_q(theta,j,u)/rhos[j])[0]
    return -rhos[j]*(hphi(rr)-hphi(r0))/(tau*hp0*ax)

def current(theta,j,u,rhos):
    f,X,k,a,b,c=geometry(theta,j)
    w=vv(-tau*f/rhos[j],tau*sq_q(theta,j,u)/rhos[j])
    return mp.matrix([w*a*u[0],w*(a*u[1]+b)])

def seed(rho):
    theta=mp.matrix([x for row in zip(F_NATIVE,X_NATIVE,SHIFT) for x in row])
    U=mp.matrix([[amp*X_NATIVE[j]**2,amp*mp.mpf('.23')*X_NATIVE[j]**2*(1+mp.mpf('.04')*j)] for j in range(N)])
    Delta=mp.matrix([h*sum(U[j,i] for j in range(N)) for i in range(2)])
    return theta,U,Delta

def solve(theta,rho,U0,Delta):
    def fromj(q):
        U=[]
        for j in range(N):
            def func(uu,vv):
                x=current(theta,j,mp.matrix([uu,vv]),rho)
                return (x[0]-q[0],x[1]-q[1])
            a,b=mp.findroot(func,(U0[j,0],U0[j,1]),tol=mp.mpf('1e-65'),maxsteps=20)
            U.append(mp.matrix([a,b]))
        return U
    guess=current(theta,0,mp.matrix([U0[0,0],U0[0,1]]),rho)
    def balance(a,b):
        q=mp.matrix([a,b]);U=fromj(q)
        return tuple(h*sum(U[j][i] for j in range(N))-Delta[i] for i in range(2))
    j0,j1=mp.findroot(balance,(guess[0],guess[1]),tol=mp.mpf('1e-58'),maxsteps=20)
    J=mp.matrix([j0,j1]);U=fromj(J)
    assert max(abs(h*sum(U[j][i] for j in range(N))-Delta[i]) for i in range(2))<mp.mpf('1e-55')
    return U,J

def reduced_gradient(theta,rho,U0,Delta):
    U,_=solve(theta,rho,U0,Delta)
    res=[]
    for j in range(N):
        for k in range(3):
            pos=3*j+k
            def local(t):
                v=theta.copy();v[pos]=t
                return cell_price(v,j,U[j],rho)
            res.append(mp.diff(local,theta[pos]))
    return mp.matrix(res)

def check(weights):
    rho=[mp.mpf(x) for x in weights]
    theta,U0,Delta=seed(rho)
    U,J=solve(theta,rho,U0,Delta)
    before=[current(theta,j,mp.matrix([U0[j,0],U0[j,1]]),rho) for j in range(N)]
    after=[current(theta,j,U[j],rho) for j in range(N)]
    before_res=max(abs(before[j][i]-before[j+1][i]) for j in range(N-1) for i in range(2))
    after_res=max(abs(after[j][i]-after[j+1][i]) for j in range(N-1) for i in range(2))
    # Differentiating the full original entropy, not the current formula:
    psi=[mp.matrix([0,0])]
    for j in range(N):psi.append(psi[-1]+h*U[j])
    def action_psix(x,k):
        pst=[v.copy() for v in psi];pst[k]=pst[k].copy();pst[k][x[1]]=x[0]
        uu=[(pst[j+1]-pst[j])/h for j in range(N)]
        return sum(cell_price(theta,j,uu[j],rho) for j in range(N))
    pr=[]
    for k in range(1,N):
        for i in range(2):
            pr.append(mp.diff(lambda q:action_psix((q,i),k),psi[k][i]))
    assert max(abs(v) for v in pr)<mp.mpf('1e-55')
    M=3*N
    Kfixed=mp.zeros(M)
    BB=[];HH=[];invHH=[]
    for j in range(N):
        def Jloc(ut):return current(theta,j,ut,rho)
        hj=mp.matrix([[mp.diff(lambda a:Jloc(mp.matrix([a, U[j][1]]))[r], U[j][0]) if s==0 else mp.diff(lambda a:Jloc(mp.matrix([U[j][0],a]))[r], U[j][1]) for s in range(2)] for r in range(2)])
        Bj=mp.matrix([[mp.diff(lambda a:current(mp.matrix([theta[i] if i!=3*j+k else a for i in range(M)]),j,U[j],rho)[r],theta[3*j+k]) for k in range(3)] for r in range(2)])
        HH.append(hj);BB.append(Bj);invHH.append(hj**-1)
        for a in range(3):
            for b in range(3):
                def deriv(x,y):
                    zz=theta.copy();zz[3*j+a]=x;zz[3*j+b]=y
                    return cell_price(zz,j,U[j],rho)
                if a!=b:
                    Kfixed[3*j+a,3*j+b]=mp.diff(lambda xx,yy:deriv(xx,yy),(theta[3*j+a],theta[3*j+b]),(1,1))
                else:
                    Kfixed[3*j+a,3*j+a]=mp.diff(lambda xx:deriv(xx,xx),theta[3*j+a],2)
    W=sum(invHH,mp.zeros(2));C=mp.zeros(2,M);Hloc=mp.zeros(M)
    for j in range(N):
        cb=invHH[j]*BB[j]
        for a in range(2):
            for b in range(3):C[a,3*j+b]=cb[a,b]
        tmp=BB[j].T*invHH[j]*BB[j]
        for a in range(3):
            for b in range(3):Hloc[3*j+a,3*j+b]=tmp[a,b]
    K0=Kfixed-2*Hloc
    Kupd=2*C.T*W**-1*C
    Kschur=K0+Kupd
    # Truly independent reduced-source secant with every matter current
    # freshly solved for the +/- perturbed metric/holonomy coordinates.
    eps=mp.mpf('1e-18')
    Gsec=mp.zeros(M)
    for k in range(M):
        up=theta.copy();dn=theta.copy();up[k]+=eps;dn[k]-=eps
        gp=reduced_gradient(up,rho,U0,Delta);gm=reduced_gradient(dn,rho,U0,Delta)
        for i in range(M):Gsec[i,k]=(gp[i]-gm[i])/(2*eps)
    err=max(abs(Kschur[i,j]-Gsec[i,j]) for i in range(M) for j in range(M))
    assert err<mp.mpf('1e-25'),('Schur analytical high precision',mp.nstr(err,20))
    # Rank TWO, not isotropic rank-one, because the original Lorentzian
    # coframe has a genuine nonzero g^{01} shift, linked to scalar2 x-flow.
    assert abs(C[0,2]*C[1,5]-C[1,2]*C[0,5])>mp.mpf('1e-10')
    vec=mp.matrix([(i+1)/mp.mpf(M) for i in range(M)])
    direct=Kschur**-1*vec
    small=W+2*C*K0**-1*C.T
    wood=K0**-1*vec-2*K0**-1*C.T*small**-1*C*K0**-1*vec
    woody=max(abs(direct[i]-wood[i]) for i in range(M))
    assert woody<mp.mpf('1e-55')
    eigmin=min(float(mp.eigsy((h+h.T)/2,eigvals_only=True)[0]) for h in HH)
    print({'PF':list(map(float,rho)),'before':float(before_res),'after':float(after_res),
      'independent_full_entropy_scalar_Euler':float(max(abs(x) for x in pr)),
      'smallest_real_material_flux_eigen':eigmin,
      'full_nonlin_mat2_current':[float(J[0]),float(J[1])],
      'native_geometry_parameters':M,'rank_two_update_witness':float(abs(C[0,2]*C[1,5]-C[1,2]*C[0,5])),
      'Schur_full_independent_source_max_error':mp.nstr(err,8),
      'Woodbury_two_component_max_error':mp.nstr(woody,8)})
    return err

if __name__=='__main__':
    check([1,1,1]);check([1,2,1])
