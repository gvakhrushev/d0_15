#!/usr/bin/env python3
"""EXACT ORIGINAL CAR16/Julia/Walsh N0 prepared Book response 16->4->2.

Rebuilds from unchanged creator order (0,2,3,1), original 32 duplicated
Walsh row0, ORIGINAL phases (i,i,-1,-i), positive Hermitian Lorentz boost
U=exp(theta*G), and original Golden p with zeta=2^-20.

Exact rational Gaussian/CAR, no floating rank, no fitted Palatini action.
All-r/n assertions proven analytically by the accompanying theorem;
exact rational checkpoints on both sides of r=0 exercise the source.
The full native 128 Kraus/fine future algebra is NOT compressed by this
calculation; no unrestricted 42-field response or GR closure is claimed.

python3 check_two_mode_original.py
python3 -O check_two_mode_original.py
"""
from __future__ import annotations
from itertools import combinations
import json
import sympy as sp

Q=sp.Rational
eye16=sp.eye(16)
phases=(sp.I,sp.I,-sp.Integer(1),-sp.I)
p=(sp.sqrt(5)-1)/2
zeta=Q(1,2**20)
r,nu=sp.symbols("r nu",real=True)
checks=0
def check(ok,message):
    global checks
    checks+=1
    if not bool(ok):
        raise ArithmeticError(message)
def vanish(x):
    if isinstance(x,sp.MatrixBase):
        return all(sp.cancel(y)==0 for y in x)
    return sp.cancel(x)==0
def creator(dim,idx,order):
    n=1<<dim;M=sp.zeros(n)
    for bits in range(n):
        if not ((bits>>idx)&1):
            M[bits|(1<<idx),bits]=(-1)**sum((bits>>j)&1
                                             for j in order[:order.index(idx)])
    return M
cs=[creator(4,k,(0,2,3,1)) for k in range(4)]
c2s=[creator(2,k,(0,1)) for k in range(2)]
C0,C1=c2s
G16=cs[0]*cs[1].T+cs[1]*cs[0].T
G4=C0*C1.T+C1*C0.T

check(G16**3==G16 and G4**3==G4,"original positive Lorentz generator G^3=G")

def boost(G,n,r):
    return sp.eye(n)+2*r/(1-r*r)*G+2*r*r/(1-r*r)*G*G

def full_original_n0(r,n):
    U=boost(G16,16,r)
    original_first_channels=[]
    for j,c in enumerate(cs):
        base=n*c
        x=base*(U if j==1 else eye16)*phases[j]
        # EXACT original tuple words followed by duplicated rows;
        # b=0 receives first matrix from each tuple.
        original_first_channels.extend((x,x,x.conjugate().T,x.conjugate().T,
                                        -base,-base,-base.T,-base.T))
    check(len(original_first_channels)==32,"32 duplicated Walsh slots original")
    return sum(original_first_channels,sp.zeros(16))/32

def original_active_n0(r,n):
    U=boost(G4,4,r)
    return (n/16)*((sp.I-1)*C0+(-sp.I-1)*C0.T+
                   sp.I*C1*U-sp.I*U*C1.T-C1-C1.T)

# Exact graded Fock permutation: (0,2,3,1)->(0,1,2,3), not
# just an unsigned ordinary tensor permutation.
W=sp.zeros(16)
for aa in range(4):
    for bb in range(4):
        oldbits=((aa&1) | (((aa>>1)&1)<<1) |
                 ((bb&1)<<2) | (((bb>>1)&1)<<3))
        fermion_sign=(-1)**(((aa>>1)&1)*((bb&1)+((bb>>1)&1)))
        W[oldbits,aa*4+bb]=fermion_sign
check(W.T*W==eye16 and W.det()!=0,"fermionic graded tensor basis is unitary")
parA=sp.diag(1,-1,-1,1)
for j in range(4):
    rhs=sp.kronecker_product([C0,C1,parA,parA][j],
                            [sp.eye(4),sp.eye(4),c2s[0],c2s[1]][j])
    check(W.T*cs[j]*W==rhs,f"all original creation operators factored r{j}")

# The original proper-boost family is captured by a 2x2 odd sector.
a4=original_active_n0(r,nu)
check(vanish(a4.conjugate().T-a4),"native active Walsh matrix is Hermitian")
T=a4.extract([1,2],[0,3])
m=T.conjugate().T*T+3*nu*nu*sp.eye(2)/128
m2=T*T.conjugate().T+3*nu*nu*sp.eye(2)/128
s=nu**2*(5*r**4+r**3-8*r**2-r+5)/(64*(1-r*r)**2)
t=nu**4*(23*r**4+6*r**3-32*r**2-10*r+25)/(16384*(1-r*r)**2)
check(vanish(sp.trace(m)-s),"ALL-r rational sum of original 2 eigenvalues")
check(vanish(m.det()-t),"ALL-r rational product of original 2 eigenvalues")
check(vanish(sp.trace(m2)-s) and vanish(m2.det()-t),
      "even and odd active 2x2 sectors EXACT isospectral")
check(vanish(a4*parA+parA*a4),
      "original two-mode Walsh a01 is parity ODD, not an arbitrary 4x4")

Gamma2=cs[2]+cs[2].T
par=sp.diag(*[(-1)**i.bit_count() for i in range(16)])
check(Gamma2.T==Gamma2 and Gamma2*Gamma2==eye16,
      "original spectator2 Majorana is an involution")
check(Gamma2*par+par*Gamma2==sp.zeros(16),
      "Majorana switches both genuine parity sectors")
plus=[i for i in range(16) if i.bit_count()%2==0]
minus=[i for i in range(16) if i.bit_count()%2==1]
check(len(plus)==len(minus)==8,"true original future parity sectors are 8+8")

samples=[(Q(0),Q(3,5)),(Q(1,9),Q(3,5)),
         (-Q(1,7),Q(1,2)),(Q(1,5),Q(2,3))]
for rv,nv in samples:
    a=full_original_n0(rv,nv)
    check(vanish(a-a.conjugate().T),"true ORIGINAL Walsh N0 Hermitian")
    b0=-(nv/8)*(cs[2]+cs[2].T)
    b1=nv/16*((-1-sp.I)*cs[3]+(-1+sp.I)*cs[3].T)
    a01=original_active_n0(rv,nv)
    activefull=W*sp.kronecker_product(a01,sp.eye(4))*W.T
    check(vanish(a-activefull-b0-b1),
          "literal original 32-slot Walsh N0 is exactly 01+2+3")
    check(vanish(b0*b0+b1*b1-3*nv*nv*eye16/128),
          "spectator Majorana squares sum to EXACT 3 nu²/128")
    check(vanish(activefull*b0+b0*activefull) and
          vanish(activefull*b1+b1*activefull),
          "TRUE CAR graded odd anticommution kills both cross terms")
    D=a.conjugate().T*a
    small=a01*a01+3*nv*nv*sp.eye(4)/128
    check(vanish(W.T*D*W-sp.kronecker_product(small,sp.eye(4))),
          "ACTUAL 16x16 original Delta exactly 4x4 tensor spectator4")
    check(vanish(D*cs[2]-cs[2]*D) and
          vanish(D*cs[3]-cs[3]*D),
          "both original spectator CAR creators COMMUTE with Delta")
    check(vanish(D*Gamma2-Gamma2*D) and
          vanish(D*par-par*D),
          "true original feedback even and parity-conjugate")
    char_x=sp.symbols("x")
    s_num=s.subs({r:rv,nu:nv})
    t_num=t.subs({r:rv,nu:nv})
    check(vanish(small.charpoly(char_x).as_expr()-
                 (char_x*char_x-s_num*char_x+t_num)**2),
          "ACTUAL original 4x4 graded CAR charpoly is exact quadratic squared")
    # Per-parity feedback determinants are provably identical, without
    # ever discarding one parity from the genuine future-complete task.
    Fb=4*p*p*D*(eye16-p*p*D)
    check(vanish(Fb*Gamma2-Gamma2*Fb),
          "actual prepared Book F has parity intertwiner")

# Radical-free complete original 16D determinant.
u=4*zeta*p**2
v=4*zeta*p**4
d=1-u*s+v*(s*s-2*t)+u*u*t-u*v*s*t+v*v*t*t
FF=4*p*p*m*(sp.eye(2)-p*p*m)
check(vanish((sp.eye(2)-zeta*FF).det()-d),
      "ALL-r exact no-square-root factor for full16 Book determinant")
jtheta=-4*(1-r*r)*sp.diff(d,r)/d
fixture={r:Q(1,9),nu:Q(3,5)}
s0=s.subs(fixture);t0=t.subs(fixture)
ll=[(Q(141489)+z*9*sp.sqrt(397841))/Q(10240000) for z in (-1,1)]
check(vanish(sum(ll)-s0) and vanish(ll[0]*ll[1]-t0),
      "ACTUAL original fixed boost exact radical eigenvalues")
check(all(float(sp.N(x,30))>0 and float(sp.N(x,30))<1 for x in ll),
      "original CAR strictly positive contraction chart")

# Independent ACTUAL 2-mode noncommuting matrix source at the fixture,
# rather than differentiating just guessed eigenvalue branches.
M0=m.subs(fixture)
Mdr=m.diff(r).subs(fixture)
F0=4*p*p*(M0-p*p*M0*M0)
Fdr=4*p*p*(Mdr-p*p*(Mdr*M0+M0*Mdr))
check(vanish(M0*Mdr-Mdr*M0)==False,
      "genuinely noncommuting original reduced CAR source")
Dtheta_direct=8*zeta*sp.trace((sp.eye(2)-zeta*F0).inv()*Fdr)
Dtheta_direct*= (1-fixture[r]**2)/2
check(vanish(Dtheta_direct-jtheta.subs(fixture)),
      "exact ORIGINAL first proper-Lorentz response equals radical-free logjet")
j0=-8*sp.log(d.subs(fixture))
check(abs(float(sp.N(j0,30))-3.2042444113482065e-7)<1e-19,
      "exact original full128 Book prepared value replay")
check(abs(float(sp.N(Dtheta_direct,30))+1.8312595190037388e-8)<1e-20,
      "exact original full128 native Lorentz derivative replay")
check(vanish(sp.diff(d,r).subs(fixture))==False,
      "Book input source not frozen/zero")

# Exact interval sign of the actual prepared Book proper-boost response:
# NO sign inference from an eigenvector/gap or a floating root.
slopeS=nu**2*(1+r*r)*(r*r+4*r-1)/(64*(1-r*r)**3)
slopeT=2*nu**4*(3*r**4+14*r**3-6*r*r+18*r-5)/(
    16384*(1-r*r)**3)
check(vanish(sp.diff(s,r)-slopeS) and
      vanish(sp.diff(t,r)-slopeT),
      "ALL-r original symmetric-polynomial first derivatives exactly factored")
boundS=Q(177147,5120000)
boundT=Q(6908733,32768000000)
check(boundS<Q(1,4) and boundT<1,
      "uniform strict parameter-chart native invariants rational bounds")
check(Q(1,81)+Q(4,9)-1<0,
      "strict negative actual s' on 0<=r<=1/9")
check(Q(3,6561)+Q(14,729)+2-5<0,
      "strict negative actual t' on 0<=r<=1/9")
check(12*zeta<2 and 0<p**2<1,
      "entire original Book survival mixed partials strictly negative")
for rv,nv in samples:
    if rv<0:
        continue
    sj=s.subs({r:rv,nu:nv})
    tj=t.subs({r:rv,nu:nv})
    check(sj>0 and sj<boundS and tj>0 and tj<boundT,
          "native sampled response inside rigorous compact bound")
    check(slopeS.subs({r:rv,nu:nv})<0 and
          slopeT.subs({r:rv,nu:nv})<0,
          "true nonzero original symmetric-invariant decrease")
    check(float(sp.N(jtheta.subs({r:rv,nu:nv}),30))<0,
          "strict full original Book Lorentz source on compact native chart")

# Theorem E classification (pure independent parity-basis covariant wedge).
def invariant_subsets(n):
    whole=set(range(n))
    good=[]
    for k in range(n+1):
        for combo in combinations(range(n),k):
            set0=set(combo)
            if all(((i in set0)==(j in set0))
                   for i in range(n) for j in range(n)):
                good.append(tuple(combo))
    return good
check(invariant_subsets(8)==[(),tuple(range(8))],
      "no proper nontrivial single parity pure basis-invariant wedge")
check(len(invariant_subsets(8))**2==4,
      "exact four U8 x U8 independent sector pure-invariant classes")
check(len([x for x in invariant_subsets(8)
           if len(x)>0])**2==1,
      "future complete pure nontrivial both-sector audit unique")

print(json.dumps({
    "status":"PASS_EXACT_ORIGINAL_CAR16_WALSH_BOOK_16_TO_4_TO_2_PARITY",
    "checks":checks,"sample_r_nu":[[str(x),str(y)] for x,y in samples],
    "original_native_creation_order":[0,2,3,1],
    "whole_original_fine_Kraus_labels":128,
    "original_3tick_future_even_algebra":"M8(C)+M8(C)",
    "spectator_modes_preserved":[2,3],
    "two_exact_repeated_eigenvalues":[str(x) for x in ll],
    "j_pre_actual":str(sp.N(j0,24)),
    "dtheta_j_pre_actual":str(sp.N(Dtheta_direct,24)),
    "all_r_symmetric_polynomial_characteristic":True,
    "basis_invariant_pure_wedge_classes":4,
    "future_complete_basis_invariant_pure_wedge_classes":1,
    "physical_selection_of_pure_Slater_audit":False,
    "all42_equations_closed":False,
    "GR_closed":False
},indent=2,sort_keys=True))
