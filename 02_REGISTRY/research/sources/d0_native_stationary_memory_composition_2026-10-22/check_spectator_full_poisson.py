import json
import numpy as np

ell = np.log((1 + np.sqrt(5)) / 2)
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
pauli = [I2, np.array([[0,1],[1,0]],complex),
         np.array([[0,-1j],[1j,0]],complex), np.diag([1,-1]).astype(complex)]
basis = [np.kron(a,b) / 2 for a in pauli for b in pauli]
checks = []
def check(name, ok, value=None):
    checks.append({"name":name,"pass":bool(ok),"value":None if value is None else float(value)})
    assert ok, (name,value)
def logm(a):
    vals, vec = np.linalg.eigh(a)
    assert vals.min()>0
    return (vec * np.log(vals)) @ vec.conj().T
def inner(a,b): return np.trace(a.conj().T @ b).real
def coords(a): return np.array([inner(b,a) for b in basis])
def matrix(v): return sum((x*b for x,b in zip(v,basis)),np.zeros((4,4),complex))
def ptr_d(a):
    t=a.reshape(2,2,2,2)
    return np.einsum('iaib->ab',t)
def ptr_r(a):
    t=a.reshape(2,2,2,2)
    return np.einsum('iaja->ij',t)
def setup(a=.6,b=.8):
    k=[np.diag([a,b]).astype(complex),
       np.array([[0,np.sqrt(1-b*b)],[np.sqrt(1-a*a),0]],complex)]
    rho=np.diag([(1-b*b)/(2-a*a-b*b),(1-a*a)/(2-a*a-b*b)]).astype(complex)
    return k,rho
words=[(0,0),(0,1,0),(0,1,1),(1,1),(1,0,1),(1,0,0)]
costs=[sum(1+a for a in w)+.13*len(w)**2 for w in words]
def leaves(k):
    out=[]
    for word in words:
        l=I2.copy()
        for a in word:l=k[a]@l
        out.append(l)
    return out
def score_and_grad(omega,k,gain=False):
    val=0.;m=np.zeros((4,4),complex)
    for c,l in zip(costs,leaves(k)):
        v=np.kron(l,I2); z=v@omega@v.conj().T; p=np.trace(z).real
        val+=c*p+inner(z,logm(z))/ell
        m+=c*v.conj().T@v+v.conj().T@(logm(z)+I4)@v/ell
    if gain:
        val-=inner(omega,logm(omega))/ell
        m-=(logm(omega)+I4)/ell
    return val,m
def data_grad(rho,k,gain=False):
    m=np.zeros((2,2),complex)
    for c,l in zip(costs,leaves(k)):
        z=l@rho@l.conj().T
        m+=c*l.conj().T@l+l.conj().T@(logm(z)+I2)@l/ell
    if gain:m-=(logm(rho)+I2)/ell
    return m
k,rho=setup()
omega_r=np.array([[.6,.10+.03j],[.10-.03j,.4]],complex)
omega=np.kron(rho,omega_r)
check("complete stopped tree", np.linalg.norm(sum(l.conj().T@l for l in leaves(k))-I2)<1e-13)
check("noncommuting native-type fixture",np.linalg.norm(k[0]@k[1]-k[1]@k[0])>.01)
check("stationary DATA",np.linalg.norm(sum(v@rho@v.conj().T for v in k)-rho)<1e-13)
def psi_star(m):return sum(np.kron(v.conj().T,I2)@m@np.kron(v,I2) for v in k)
def proj_star(m):return np.kron(I2,ptr_d(np.kron(rho,I2)@m))
T=np.column_stack([coords(psi_star(x)) for x in basis])
P=np.column_stack([coords(proj_star(x)) for x in basis])
check("full fixed algebra dimension 4",np.linalg.matrix_rank(np.eye(16)-T,tol=1e-10)==12)
check("spectral projection idempotent",np.linalg.norm(P@P-P)<1e-13)
check("spectral projection commutes with channel",np.linalg.norm(T@P-P)+np.linalg.norm(P@T-P)<1e-13)
inv=np.linalg.inv(np.eye(16)-T+P)
rng=np.random.default_rng(123456)
for gain in [False,True]:
    s,m=score_and_grad(omega,k,gain)
    md=data_grad(rho,k,gain)
    predicted=np.kron(md,I2)+(np.zeros((4,4),complex) if gain else np.kron(I2,logm(omega_r))/ell)
    err=np.linalg.norm(m-predicted)
    check(f"ambient tensor cotangent gain={gain}",err<1e-12,err)
    y=matrix(inv@(np.eye(16)-P)@coords(m))
    lam=-ptr_d(np.kron(rho,I2)@m)
    res=m+psi_star(y)-y+np.kron(I2,lam)
    check(f"fixed RIGHT full operator Euler gain={gain}",np.linalg.norm(res)<1e-11,np.linalg.norm(res))
    check(f"gauge zero conditional mean gain={gain}",np.linalg.norm(proj_star(y))<1e-11)
    for j in range(5):
        x=matrix(rng.normal(size=16));x-=np.trace(x).real/4*I4
        # Pure correlation tangent: both marginals zero.
        x=x-np.kron(ptr_r(x),I2/2)-np.kron(I2/2,ptr_d(x))
        h=1e-6/np.linalg.norm(x)
        fd=(score_and_grad(omega+h*x,k,gain)[0]-score_and_grad(omega-h*x,k,gain)[0])/(2*h)
        an=inner(m,x)
        check(f"ambient correlation gradient gain={gain} case={j}",abs(fd-an)<1e-7,abs(fd-an))
    mr=ptr_d(np.kron(rho,I2)@m)
    compatibility=np.linalg.norm(mr-np.trace(mr)/2*I2)
    check(f"free RIGHT compatibility gain={gain}",(compatibility<1e-11) if gain else (compatibility>.1),compatibility)

# Fully free CQ input: tracial RIGHT closes all 16 ambient operator rows.
om0=np.kron(rho,I2/2)
s0,m0=score_and_grad(om0,k,False)
y0=matrix(inv@(np.eye(16)-P)@coords(m0))
mu=inner(om0,m0)
res=m0+psi_star(y0)-y0-mu*I4
check("free CQ full operator Euler at tracial RIGHT",np.linalg.norm(res)<1e-11,np.linalg.norm(res))
# Independent RIGHT entropy Hessian, all three normalized Hermitian directions.
for j,x in enumerate(pauli[1:]):
    h=1e-4
    fplus=score_and_grad(np.kron(rho,I2/2+h*x),k,False)[0]
    fminus=score_and_grad(np.kron(rho,I2/2-h*x),k,False)[0]
    fd=(fplus-2*s0+fminus)/h**2
    expected=2*inner(x,x)/ell
    check(f"free RIGHT positive Hessian {j}",abs(fd-expected)<1e-5,fd)
# Genuine full prepared source versus Poisson source, not fixed rho derivative.
for gain in [False,True]:
    wr=omega_r if gain else I2/2
    om=np.kron(rho,wr)
    s,m=score_and_grad(om,k,gain)
    y=matrix(inv@(np.eye(16)-P)@coords(m))
    h=1e-5
    kp,rp=setup(.6+h);km,rm=setup(.6-h)
    total=(score_and_grad(np.kron(rp,wr),kp,gain)[0]-score_and_grad(np.kron(rm,wr),km,gain)[0])/(2*h)
    fixed=(score_and_grad(om,kp,gain)[0]-score_and_grad(om,km,gain)[0])/(2*h)
    dp=(sum(np.kron(v,I2)@om@np.kron(v.conj().T,I2) for v in kp)-sum(np.kron(v,I2)@om@np.kron(v.conj().T,I2) for v in km))/(2*h)
    corrected=fixed+inner(y,dp)
    check(f"whole prepared Poisson source gain={gain}",abs(total-corrected)<2e-8,abs(total-corrected))

# Hostile non-spectator work cost: incompatible RIGHT force cannot be inverted away.
bad=m0+np.kron(I2,pauli[3])
badmr=ptr_d(np.kron(rho,I2)@bad)
check("non spectator cost has genuine RIGHT obstruction",np.linalg.norm(badmr-np.trace(badmr)/2*I2)>1)
ybad=matrix(inv@(np.eye(16)-P)@coords(bad))
badres=bad+psi_star(ybad)-ybad-inner(om0,bad)*I4
check("scalar centering cannot remove non spectator force",np.linalg.norm(badres)>1)

# A correlated cost invisible on product restriction still has an ambient force.
correlated=np.kron(pauli[1],pauli[1])
check("correlated work invisible at every tracial product",abs(inner(om0,correlated))<1e-13)
check("correlated work ambient force is nonzero",np.linalg.norm(correlated)>1)
ycorr=matrix(inv@(np.eye(16)-P)@coords(correlated))
check("correlated Poisson force exact coefficient 25",np.linalg.norm(ycorr-25*correlated)<1e-10,np.linalg.norm(ycorr-25*correlated))
check("correlated full operator Euler",np.linalg.norm(correlated+psi_star(ycorr)-ycorr)<1e-11)

result={"fixture":"same rational nonunital two Kraus native-type parent, not full128", "stopped_leaves":len(words),"checks":checks,"pass_count":len(checks),"scope":"exact derived identities checked numerically; physical native selection and full128 not claimed"}
print(json.dumps(result,ensure_ascii=False,indent=2))
