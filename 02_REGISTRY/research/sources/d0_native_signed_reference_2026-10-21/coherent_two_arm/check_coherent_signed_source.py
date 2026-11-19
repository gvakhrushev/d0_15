#!/usr/bin/env python3
"""Same-execution coherent signed-CQ price on the owned n-edge Julia dilation.

Fixed supplied coherent-input and fixed-charge/query chart ONLY.  Does NOT
establish Book03's Info valuation, native actuation of a moving Lorentz
reference, physical task selection, 42-field primitive admission or GR.
"""
import json, math, argparse
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as sp

checks=[]
def require(a,name):
    if not bool(a): raise AssertionError(name)
    checks.append(name)

p=(math.sqrt(5)-1)/2
phi=1/p
ell=math.log(phi)
n=4
c=(p**3)*(2**(-n))
eta=np.diag([1.,-1.,-1.,-1.]); I4=np.eye(4)
G=[]
for i in range(1,4):
    g=np.zeros((4,4));g[0,i]=g[i,0]=1;G.append(g)
for i,j in [(2,3),(3,1),(1,2)]:
    g=np.zeros((4,4));g[i,j]=1;g[j,i]=-1;G.append(g)
G=np.array(G)
for a in range(6):
    require(np.max(np.abs(G[a].T@eta+eta@G[a]))<1e-14,f'Lorentz generator {a}')
    for b in range(6): require(abs(np.trace(G[a].T@G[b])-2*(a==b))<1e-14,f'G Gram {a},{b}')

pp=sp.symbols('p',real=True)
pr=(sp.sqrt(5)-1)/2
require(sp.simplify(pr*pr+pr-1)==0,'exact Golden partition')
require(sp.simplify(pr**2+pr**4+pr**3-2*pr**2)==0,'Gold/fair baseline p2')
require(sp.simplify(1-pr**3-2*pr**2)==0,'1-p3=2p2 Golden choice')
q_xy={
 (1,1):sp.Rational(3,4)*pr**2+sp.Rational(1,4)*(1-pr**3),
 (0,0):sp.Rational(3,4)*pr**2+sp.Rational(1,4)*(pr**2+pr**4),
 (1,0):sp.Rational(3,4)*pr**2+sp.Rational(1,4)*pr**4,
 (0,1):sp.Rational(3,4)*pr**2+sp.Rational(1,4)*pr**4,
}
for (x,y),value in q_xy.items():
    require(sp.simplify(value-(pr**2+(x-pr**2)*(y-pr**2)/4))==0,f'Golden controlled report {x}{y}')
    require(0<float(value)<1,f'positive Golden controlled report {x}{y}')

Omega=np.eye(4).reshape(-1)/2
f=np.array([g.reshape(-1)/math.sqrt(2) for g in G])
require(abs(np.linalg.norm(Omega)-1)<1e-14,'fixed four-level Choi seed unit norm')
for a in range(6):
    require(abs(np.linalg.norm(f[a])-1)<1e-14,f'fixed grade-one reference {a} unit norm')
    require(abs(np.vdot(Omega,f[a]))<1e-14,f'flat reference orthogonality {a}')

def R(P): return (P-np.linalg.inv(P))/2

def B(P):return np.array([math.sqrt(2)*np.trace(g.T@P).real/4 for g in G])

def paths(units):
    """All 2**n original flags, with actual failure residuals at each link."""
    psi={0:Omega.astype(complex)}
    for j,U in enumerate(units):
        K=np.kron(U/2,I4).astype(complex)
        evals,v=np.linalg.eigh(np.eye(16)-K.conj().T@K)
        require(evals.min()>1e-7,f'strict original Julia positive residual {j}')
        F=(v*np.sqrt(evals))@v.conj().T
        updated={}
        for mask,x in psi.items():
            updated[mask]=K@x
            updated[mask+(1<<j)]=F@x
        psi=updated
    norm=sum(np.vdot(v,v).real for v in psi.values())
    require(abs(norm-1)<3e-13,'all 2^n original Julia flags retained')
    return psi

def loop_units(seed=0):
    # Four genuine noncommuting based edges, all within original Julia chart.
    return [la.expm(.07*G[0]),la.expm(-.09*G[4]),la.expm(.11*G[3]),la.expm(.065*G[2])]

units=loop_units()
P=I4.copy()
for U in units:P=U@P
psi=paths(units)
require(len(psi)==2**n,'full16 Julia complete flag tape')
allgood=psi[0]
require(np.linalg.norm(allgood-2**(-n)*np.kron(P,I4)@Omega)<4e-14,
        'original all-good coherent amplitude exact')
require(sum(np.vdot(x,x).real for k,x in psi.items() if k!=0)>0,
        'real Julia failure mass is positive and retained')
for a in range(6):
    zeta=np.vdot(f[a],allgood).real
    require(abs(zeta-(2**(-n))*B(P)[a])<4e-14,f'exact coherent overlap {a}')
    control_proj=p**2+p**4+2*p**3*zeta
    final=(control_proj+p**3)/2
    require(abs(final-(p**2+c*B(P)[a]))<4e-14,f'Golden-biased coherent final report {a}')
    require(0<final<1,f'complete report strictly positive {a}')

# Inversion and Frobenius duality for two distinct noncommuting proper-Lorentz words.
unitsQ=[la.expm(-.045*G[1]),la.expm(.09*G[5]),la.expm(-.075*G[0]),la.expm(.07*G[4])]
P2=I4.copy()
for U in unitsQ:P2=U@P2
for W in (P,P2):
    require(np.linalg.norm(W.T@eta@W-eta)<1e-12,'proper Lorentz product')
    require(abs(np.trace(W)-np.trace(np.linalg.inv(W)))<2e-13,'SO trace inversion')
    require(np.linalg.norm(B(np.linalg.inv(W))+B(W))<2e-13,'all six exact odd overlaps')
    require(np.linalg.norm(R(W).T@eta+eta@R(W))<2e-13,'true odd curvature is in so(1,3)')
dot=sum(B(P)[a]*B(P2)[a] for a in range(6))
fro=float(np.vdot(R(P),R(P2)).real)
require(abs(dot-fro/4)<1e-13,'exact six-generator Frobenius completeness')

# One fixed final pointer from two independent complete coherent arms.
def born_q(P,Q):
    return p*p+(c*c/32)*np.dot(B(P),B(Q))
def conditional_q(x,y):return float(q_xy[(x,y)])
def explicit_joint_for_face(x,y):
    bx=p*p+c*B(x)
    by=p*p+c*B(y)
    sumq=0.0
    for a in range(6):
        mx=float(bx[a]);my=float(by[a])
        qh=0.0
        for X in (0,1):
            for Y in (0,1):
                prob=(mx if X else 1-mx)*(my if Y else 1-my)
                qh+=prob*conditional_q(X,Y)
        sumq+=qh/8
    return sumq+2*p*p/8
q=born_q(P,P2)
require(abs(q-explicit_joint_for_face(P,P2))<3e-14,
        'entire eight-way fair/G-controlled final probability')
require(abs(q-(p*p+c*c*fro/128))<2e-14,
        'true nonlinear bi-curvature kernel on genuine noncommuting Lorentz P,Q')
require(abs(born_q(P,np.linalg.inv(P2))-(2*p*p-q))<2e-14,
        'orientation inversion reverses the one full pointer contrast')
require(0<q<1,'one full report remains strictly positive')

# Exact mixed field Hessian of the paid complete CQ price.
def hphi(z): return -(z*math.log(z)+(1-z)*math.log(1-z))/ell
def price(P,Q):return 100-hphi(born_q(P,Q))
J=c*c/64
require(J>0,'positive actual Golden/G Julia coefficient')
vals=[]
for a in range(6):
    for b in range(6):
        t=1e-3
        pp0=la.expm(t*G[a]); pm0=la.expm(-t*G[a]); qq0=la.expm(t*G[b]); qm0=la.expm(-t*G[b]);
        mixed=(price(pp0,qq0)-price(pp0,qm0)-price(pm0,qq0)+price(pm0,qm0))/(4*t*t)
        predicted=-J*(a==b)
        require(abs(mixed-predicted)<5e-9,f'mixed native source {a},{b}')
        vals.append(mixed)
H=np.block([[np.zeros((6,6)),-J*np.eye(6)],[-J*np.eye(6),np.zeros((6,6))]])
w=np.linalg.eigvalsh(H)
require(sum(w<0)==6 and sum(w>0)==6,'exact 6 negative 6 positive mixed Hessian')
require(np.max(abs(np.abs(w)-J))<1e-14,'all twelve Hessian moduli native coefficient')
require(abs((price(la.expm(.002*G[0]),I4)-price(I4,I4)))<1e-14,
        'each single arm has NO self-CQ derivative or curvature cost')

# Exact reference Q(A): R(Q)=A and Q in SO+, with no invented physical writer.
def Qref(A):
    value=la.sqrtm(np.eye(4)+A@A).astype(complex).real +A
    return value
A=sum((.01*(j-2.5)*G[j] for j in range(6)),np.zeros((4,4)))
Qr=Qref(A)
require(np.linalg.norm(R(Qr)-A)<4e-13,'canonical nonlinear reference has EXACT R(Q)=A')
require(np.linalg.norm(Qr.T@eta@Qr-eta)<4e-13,'canonical reference is Lorentz')
require(abs(np.linalg.det(Qr)-1)<4e-13,'canonical reference in proper component')
require(abs((born_q(P,Qr)-p*p)-c*c/128*np.vdot(R(P),A).real)<2e-14,
        'one-full-pointer exact Palatini dual contraction')

# Six faces: one fixed uniform index over 8 with 2 true dummy bins.
As=[sum((.003*(j+1)*(k+1)/(a+1)*G[j] for j in range(6)),np.zeros((4,4))) for a,k in enumerate(range(6))]
Ps=[la.expm((a+1)*.006*G[a]) for a in range(6)]
star=sum(np.vdot(R(Pface),Af).real for Pface,Af in zip(Ps,As))
face_q=np.mean([born_q(Pface,Qref(Af)) for Pface,Af in zip(Ps,As)]+[p*p,p*p])
gain=c*c/(128*8)
require(abs(face_q-(p*p+gain*star))<5e-14,
        'one report nonlinear six-face based-star value exact')
require(abs(price(I4,I4)-(100-hphi(p*p)))<1e-14,'native p2 baseline cost')

# Negative controls: Shannon at a fair baseline would destroy the linear source.
require(abs(math.log((1-p*p)/(p*p))/ell-1)<1e-13,
        'Golden baseline h_phi prime exactly one')
require(abs(math.log((1-.5)/.5)/ell)<1e-15,
        'wrong fair baseline gives zero linear source')
require(abs(np.vdot(f[0],allgood).real)>1e-6,
        'coherent reference genuinely accesses a Lorentz signal')
require(abs(np.vdot(psi[0],psi[0]).real-1)>1e-2,
        'dropping Julia failure labels violates norm and price')

result={'status':'PASS_COHERENT_FIXED_DEPTH_SIGNED_NATIVE_CQ',
        'checks':len(checks),'assertions':checks,
        'golden':{'p':p,'reference_success_coefficient':c,
                  'fixed_final_pointer_coupling':c*c/128,
                  'mixed_CQ_hessian_coefficient':-J,
                  'six_face_gain':gain},
        'native_four_edge':{'allgood_mass':float(np.vdot(allgood,allgood).real),
                            'fail_mass':float(1-np.vdot(allgood,allgood).real),
                            'positive_report_P_Q':float(q),
                            'six_face_report':float(face_q),
                            'six_face_star':float(star)},
        'scope':{'same_complete_coherent_CQ_only':True,
                 'all_original_Julia_failure_flags_retained':True,
                 'fixed_query_count':True,
                 'coherent_control_and_Naimark_admission_unproved':True,
                 'moving_field_reference_native_writer_unproved':True,
                 'Book03_primitive_Info_unselected':True,
                 'full_42_matter_source_unproved':True,
                 'GR_closed':False}}
parser=argparse.ArgumentParser()
parser.add_argument('--json',type=Path)
args=parser.parse_args()
serialized=json.dumps(result,sort_keys=True,indent=2)+'\n'
if args.json:args.json.write_text(serialized,encoding='utf-8')
print(serialized,end='')
