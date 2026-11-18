"""Full DATA, all fine rows and actually purified/closed archive. Same coframe jet."""
import json
import numpy as np
import sympy as sp
import mpmath as mp
mp.iv.dps=50
iv=mp.iv
def need(x, msg):
    if not x: raise ArithmeticError(msg)
def mul(a,b): return np.einsum("ij,jk->ik",a,b,optimize=False)
def dag(x): return x.conj().T
def ip(a,b):
    sr=0; si=0
    for x,y in zip(a.flat,b.flat):
        r,k,h,j=map(int,(x.real,x.imag,y.real,y.imag))
        sr+=r*h+k*j;si+=r*j-k*h
    return sr,si
def is_integer(a):
    return (np.array_equal(a.real,np.rint(a.real)) and np.array_equal(a.imag,np.rint(a.imag)))
def as_matrix(g):
    return sp.Matrix(16,16,lambda i,j:int(g[i,j].real)+sp.I*int(g[i,j].imag))
def sylvester(root5,rhs5):
    den=root5.diagonal()[:,None]+root5.diagonal()[None,:]
    answer=360*rhs5/den
    need(is_integer(answer),"Gaussian integer root derivative in units 1/360")
    return answer
eye=np.eye(16,dtype=complex)
order=(0,2,3,1)
creators=[]
for r in range(4):
    c=np.zeros_like(eye)
    for i in range(16):
        if not (i>>r)&1:
            c[i|(1<<r),i]=(-1)**sum((i>>j)&1 for j in order[:order.index(r)])
    creators.append(c)
words=[]; jets=[]
for r,(c,phase) in enumerate(zip(creators,(1j,1j,-1,-1j))):
    base=3*c; db=creators[0]-creators[1] if r==0 else 0*c
    x=phase*base;dx=phase*db
    proj=mul(c,dag(c))
    left,right=5*eye-proj,4*eye+proj
    dl=sylvester(left,-mul(dx,dag(x))-mul(x,dag(dx)))
    dr=sylvester(right,-mul(dag(dx),x)-mul(dag(x),dx))
    dl0=sylvester(left,-mul(db,dag(base))-mul(base,dag(db)))
    dr0=sylvester(right,-mul(dag(db),base)-mul(dag(base),db))
    fields=((x,left),(dag(x),right),(-base,-left),(-dag(base),-right))
    tangents=((360*dx,dl),(360*dag(dx),dr),(-360*db,-dl0),(-360*dag(db),-dr0))
    for w,j in zip(fields,tangents): words.extend((w,w)); jets.extend((j,j))
walsh=np.array([[(-1)**bin(n&k).count("1") for k in range(32)] for n in range(32)])
def fourier(a): return np.einsum("nj,jbkl->nbkl",walsh,np.asarray(a),optimize=False).reshape(64,16,16)
N,DN=fourier(words),fourier(jets)
uden, vden=160,11520
p=(iv.sqrt(5)-1)/2;ell=-iv.log(p);lam=iv.mpf(9)/640
kap=27*p**2/25600; required=kap*((41*iv.log(2)+16*iv.log(3)-4*iv.log(5))/ell-6*p**3)
bsq=4*p**2
H_norm_sum=iv.mpf(0);pure_pinched=iv.mpf(0);total_nor=iv.mpf(0);total_aim=iv.mpf(0)
characteristics={}; count=0;boundsum=0
for j,(n,dn) in enumerate(zip(N,DN)):
    b=mul(dag(n),N[0]);db=mul(dag(dn),N[0])+mul(dag(n),DN[0])
    kk=mul(dag(dn),n)+mul(dag(n),dn)
    need(is_integer(kk) and np.array_equal(kk,dag(kk)),"Hermitian exact DATA gradient")
    if j==0:
        need(np.array_equal(db,0*eye),"quiet original Kraus jets zero")
    if np.any(kk) and j:
        # Rational root isolation of the exact Hermitian characteristic polynomial.
        cp=as_matrix(kk).charpoly().as_poly()
        key=tuple(cp.all_coeffs())
        if key not in characteristics:
            bounds=cp.intervals(eps=sp.Rational(1,10**9))
            need(sum(k for _,k in bounds)==16,"complete certified real spectrum")
            normsum=iv.mpf(0)
            for (l,h),k in bounds:
                l,h=sp.Rational(l),sp.Rational(h)
                lower=iv.mpf(int(l.p))/int(l.q);upper=iv.mpf(int(h.p))/int(h.q)
                normsum+=k*abs(iv.mpf([lower,upper]))
            characteristics[key]=normsum
        H_norm_sum+=characteristics[key]/(uden*vden)
        count+=1
    x=iv.mpf(ip(b,b)[0])/(16*(uden**2)**2)
    v=iv.mpf(ip(db,db)[0])/(16*(uden*vden)**2)
    aim=iv.mpf(ip(b,db)[1])/(16*uden**3*vden)
    if np.any(b) and np.any(db):
        squared=x*v-aim**2
        need(squared>=0,"nonnegative pure-block variation")
        pure_pinched+=bsq*iv.sqrt(squared)
    total_nor+=bsq*v
    total_aim+=bsq*aim
tv_mixed=bsq*lam*H_norm_sum/(2*16)
tv_coherent_purified=iv.sqrt(total_nor-total_aim**2)
need(0<tv_mixed and tv_mixed<=pure_pinched and pure_pinched<=tv_coherent_purified,"trace-distance contraction")
extra=kap*iv.log(2)/ell
def span(v,objective):
    return {"sensitivity":str(v),"range_for_DATA_residual_R41":str(required/v),
            "range_for_joint_residual_R42":str((required+extra)/v),"consumer":objective}
print(json.dumps(dict(result="PASS",fine_DATA=span(tv_mixed,"R41"),fine_DATA_oldRIGHT=span(pure_pinched,"R42"),
    coherent_full128_DATA_oldRIGHT=span(tv_coherent_purified,"precommit upper bound only"),nonzero_DATA_gradient_blocks=count,
    exact_characteristic_polynomial_types=len(characteristics),physical_binding_proved=False),indent=2))
