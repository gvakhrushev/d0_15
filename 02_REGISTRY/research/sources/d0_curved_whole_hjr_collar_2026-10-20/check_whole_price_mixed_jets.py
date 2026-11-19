"""Exact actual four-role/fullCAR16 finite-B trace-jet control, not a root solve.

Small depth3 tests the general identities used in section12. The theorem,
not this finite control, handles native m=256L^2 and uniform refinement.
Read-only by default; --output writes an independent receipt.
"""
import json, sys, hashlib, math
from pathlib import Path
from flint import fmpq, fmpq_mat

L=2
sites=16
fiber=16
n=sites*fiber
I=fmpq_mat(n,n)
for i in range(n): I[i,i]=1
zero=lambda:fmpq_mat(n,n)
tr=lambda A:sum((A[i,i] for i in range(n)),fmpq(0))
C=[]
for a in range(4):
    A=fmpq_mat(16,16)
    for mask in range(16):
        if not (mask>>a)&1:
            A[mask|(1<<a),mask]=(-1)**((mask&((1<<a)-1)).bit_count())
    C.append(A)
G=(C[0]*C[1].transpose()+C[1]*C[0].transpose())/8
eta=fmpq_mat([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]])
K=fmpq_mat(4,4);K[0,1]=K[1,0]=fmpq(1,8)
assert K.transpose()*eta+eta*K==fmpq_mat(4,4)

def add_block(A,x,y,B):
    for a in range(16):
        for b in range(16):
            if B[a,b]: A[16*x+a,16*y+b]+=B[a,b]

d0,ds,dt,dst,dtt=[zero() for _ in range(5)]
for x in range(sites):
    for r in range(4):
        add_block(d0,x,x^(1<<r),C[r]/2)
        add_block(d0,x,x,-C[r]/2)
# u_0(0)=e0/4+s e1/8; U_0(0)=exp(t B01/8).
# These are the genuine coframe/proper-link first and mixed jets.
add_block(ds,0,1,C[1]/4);add_block(ds,0,0,-C[1]/4)
add_block(dt,0,1,C[0]*G/2)
add_block(dst,0,1,C[1]*G/4)
add_block(dtt,0,1,C[0]*G*G/2)
D,Ds,Dt,Dst,Dtt=[A+A.transpose() for A in (d0,ds,dt,dst,dtt)]
Delta=D*D
Qs=D*Ds+Ds*D;Qt=D*Dt+Dt*D
Rss=2*Ds*Ds
Rst=Ds*Dt+Dt*Ds+D*Dst+Dst*D
Rtt=2*Dt*Dt+D*Dtt+Dtt*D
assert D*Ds!=Ds*D and D*Dt!=Dt*D
assert Qs*Qt!=Qt*Qs

# Independent direct product-rule jets of the literal finite B power.
alpha=fmpq(1,64);m=3;beta=m*alpha;z=fmpq(1,2**20);M=128
base=I-alpha*Delta
Bjets=(base,-alpha*Qs,-alpha*Qt,-alpha*Rss,-alpha*Rst,-alpha*Rtt)

def product(A,B):
    a,s,t,ss,st,tt=A;b,u,v,uu,uv,vv=B
    return (a*b,s*b+a*u,t*b+a*v,
            ss*b+2*s*u+a*uu,st*b+s*v+t*u+a*uv,
            tt*b+2*t*v+a*vv)

P=(I,zero(),zero(),zero(),zero(),zero())
for _ in range(m): P=product(P,Bjets)
P0,Ps,Pt,Pss,Pst,Ptt=P
Z=tr(P0);Zs=tr(Ps);Zt=tr(Pt)
F=(1-z)*I+z*P0
Fi=F.inv()
direct_first=[tr(A)/(beta*Z)-M*z*tr(Fi*A) for A in (Ps,Pt)]
direct_second=[]
for Aij,Ai,Aj in ((Pss,Ps,Ps),(Pst,Ps,Pt),(Ptt,Pt,Pt)):
    direct_second.append((tr(Aij)/Z-tr(Ai)*tr(Aj)/(Z*Z))/beta
                         -M*z*tr(Fi*Aij)+M*z*z*tr(Fi*Aj*Fi*Ai))

# Exact independent full-site Fourier basis: Delta diagonal, every CAR retained.
T=zero()
energies=[]
for k in range(sites):
    energies += [k.bit_count()]*16
    for x in range(sites):
        sign=(-1)**((x&k).bit_count())
        for a in range(16):T[16*x+a,16*k+a]=fmpq(sign,4)
assert T.transpose()*T==I
ED=T.transpose()*Delta*T
assert all(ED[i,j]==(energies[i] if i==j else 0) for i in range(n) for j in range(n))
Q=[T.transpose()*A*T for A in (Qs,Qt)]
R=[T.transpose()*A*T for A in (Rss,Rst,Rtt)]
f={e:(1-alpha*e)**m for e in range(5)}
a={e:(1-alpha*e)**(m-1) for e in range(5)}
ap={e:-alpha*(m-1)*(1-alpha*e)**(m-2) for e in range(5)}
ff={e:1-z+z*f[e] for e in range(5)}
kap={e:-a[e]/Z+M*z*beta*a[e]/ff[e] for e in range(5)}
kapprime={e:-ap[e]/Z+M*z*beta*(ap[e]/ff[e]+z*beta*a[e]**2/ff[e]**2) for e in range(5)}

def spectral_hessian(A,B,Rab):
    part1=sum((kap[energies[i]]*Rab[i,i] for i in range(n)),fmpq(0))
    part2=fmpq(0)
    for i in range(n):
        for j in range(n):
            e,fv=energies[i],energies[j]
            dd=kapprime[e] if e==fv else (kap[e]-kap[fv])/(e-fv)
            part2+=dd*A[i,j]*B[j,i]
    na=sum((a[energies[i]]*A[i,i] for i in range(n)),fmpq(0))
    nb=sum((a[energies[i]]*B[i,i] for i in range(n)),fmpq(0))
    normalizer=-beta*na*nb/(Z*Z)
    return part1+part2+normalizer,normalizer

spectral_first=[sum((kap[energies[i]]*A[i,i] for i in range(n)),fmpq(0)) for A in Q]
spectral_pairs=[spectral_hessian(A,B,Rab) for A,B,Rab in ((Q[0],Q[0],R[0]),(Q[0],Q[1],R[1]),(Q[1],Q[1],R[2]))]
spectral_second=[r[0] for r in spectral_pairs]
assert direct_first==spectral_first
assert direct_second==spectral_second
assert all(r[1]!=0 for r in spectral_pairs), 'normalizer-deletion control must be nonzero'

# Third derivation: actual DIRAC-functional Frechet calculus in the NEW theorem.
# Polynomial word derivatives implement the divided-difference operator without
# assuming rational Dirac eigenvectors or diagonalizing moving eigenvectors.
Dp=[I]
for _ in range(2*m): Dp.append(Dp[-1]*D)
coeff={2*j:fmpq(math.comb(m,j))*(-alpha)**j for j in range(m+1)}
fp=zero()
for degree,coefficient in coeff.items():
    if degree:fp+=degree*coefficient*Dp[degree-1]

def frechet_polynomial(V,derivative=0):
    out=zero()
    for degree,coefficient in coeff.items():
        if derivative:
            coefficient*=degree;degree-=1
        if degree<=0:continue
        for r in range(degree):
            out+=coefficient*(Dp[r]*V*Dp[degree-1-r])
    return out

Lf=[frechet_polynomial(V) for V in (Ds,Dt)]
Lfp=[frechet_polynomial(V,1) for V in (Ds,Dt)]
assert Lf==[Ps,Pt]
gradient=(I/(beta*Z)-M*z*Fi)*fp
dirac_first=[tr(gradient*V) for V in (Ds,Dt)]
dirac_second=[]
for i,j,Dij in ((0,0,zero()),(0,1,Dst),(1,1,Dtt)):
    Vi=(Ds,Dt)[i]
    moving_gradient=(I/(beta*Z)-M*z*Fi)*Lfp[j]+M*z*z*Fi*Lf[j]*Fi*fp
    response=tr(moving_gradient*Vi)+tr(gradient*Dij)
    response-=tr(Lf[j])*tr(fp*Vi)/(beta*Z*Z)
    dirac_second.append(response)
assert dirac_first==direct_first
assert dirac_second==direct_second

# The genuine proper exponential mixed jet is nonzero in this nonroot control.
proper_mixed=T.transpose()*(D*Dst+Dst*D)*T
proper_source=sum((kap[energies[i]]*proper_mixed[i,i] for i in range(n)),fmpq(0))
assert proper_source!=0, 'proper second-jet deletion must be detected'
# Multiplying every trace by a full16 fiber is already literal, not an inferred factor.
assert n==256 and len(energies)==256
out={'status':'EXACT_WHOLE_PRICE_MIXED_JETS_PASS','L':L,'full_sites':sites,
     'fullCAR':fiber,'dimension':n,'depth_identity_control':m,
     'alpha':str(alpha),'beta':str(beta),'z':str(z),'feedback_multiplicity':M,
     'noncommuting_D_jets':True,'noncommuting_Delta_jets':True,
     'three_independent_exact_derivations':['literal B power and Jacobi',
         'full Delta spectral divided differences','Dirac-functional polynomial Frechet calculus'],
     'first_sources':[str(v) for v in direct_first],
     'mixed_hessians_ss_st_tt':[str(v) for v in direct_second],
     'omitted_normalizer_defects':[str(r[1]) for r in spectral_pairs],
     'omitted_proper_mixed_jet_defect':str(proper_source),
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Exact finite noncommuting trace-jet identity control on actual periodic four-role fullCAR16 positive-adjoint D; depth3 is a small identity test, not the native depth/root/refinement certificate; analytic section12 proves the uniform native statement. Preparation theorem is consumed separately, not retested here.'}
if '--output' in sys.argv:
    Path(sys.argv[sys.argv.index('--output')+1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
