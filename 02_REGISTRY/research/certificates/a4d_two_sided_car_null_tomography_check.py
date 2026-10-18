#!/usr/bin/env python3
"""Exact CAR16 two-sided null-projector algebra and conformal control.

This is a finite algebraic research certificate, not an admission of new
physical effects or a D0->Einstein theorem. Uses the existing 4-mode CAR
creation/annihilation matrices in the A,C,D,B role order.
"""
from __future__ import annotations

import json
import sympy as sp

N = 16
I = sp.eye(N)
Z = sp.zeros(N)
ETA = (1, -1, -1, -1)


def require(cond, message):
    if not cond:
        raise AssertionError(message)


def rank(M):
    return M.rank()


def matrix_equal(A, B):
    return A == B


def cread(a: int) -> sp.Matrix:
    C = sp.zeros(N)
    for mask in range(N):
        if mask & (1 << a):
            continue
        parity = (mask & ((1 << a) - 1)).bit_count() % 2
        C[mask | (1 << a), mask] = (-1) ** parity
    return C


C = [cread(a) for a in range(4)]
PARITY = sp.diag(*[(-1) ** mask.bit_count() for mask in range(N)])
L = [C[a] + ETA[a] * C[a].T for a in range(4)]
R = [(C[a] - ETA[a] * C[a].T) * PARITY for a in range(4)]
A = [L[0] * L[i] for i in (1, 2, 3)]
B_RAW = [R[0] * R[i] for i in (1, 2, 3)]
# The raw right Clifford bivectors carry both relative spatial chiralities.
# Their central relative-orientation involution must be consumed explicitly:
OMEGA_A = A[0] * A[1] * A[2]
OMEGA_B = B_RAW[0] * B_RAW[1] * B_RAW[2]
RELATIVE_CHIRALITY = OMEGA_A * OMEGA_B
require(OMEGA_A*OMEGA_A == -I and OMEGA_B*OMEGA_B == -I,
        'relative chiralities must square to -1')
require(RELATIVE_CHIRALITY*RELATIVE_CHIRALITY == I and
        RELATIVE_CHIRALITY.T == RELATIVE_CHIRALITY,
        'relative chirality is selfadjoint central involution')
for M in A + B_RAW:
    require(RELATIVE_CHIRALITY*M == M*RELATIVE_CHIRALITY,
            'relative chirality centrality')
B = [-RELATIVE_CHIRALITY * Bi for Bi in B_RAW]

for a in range(4):
    for b in range(4):
        anti_l = L[a]*L[b] + L[b]*L[a]
        anti_r = R[a]*R[b] + R[b]*R[a]
        target = 2*ETA[a]*I if a==b else Z
        require(matrix_equal(anti_l, target), f'L Clifford {a},{b}')
        require(matrix_equal(anti_r, target), f'R Clifford {a},{b}')
        require(matrix_equal(L[a]*R[b], R[b]*L[a]), f'commute {a},{b}')

for i in range(3):
    for j in range(3):
        target = 2*I if i==j else Z
        require(A[i] + A[i].T == 2*A[i], f'A symmetric {i}')
        require(B[i] + B[i].T == 2*B[i], f'B symmetric {i}')
        require(A[i]*A[j] + A[j]*A[i] == target, f'A Pauli {i},{j}')
        require(B[i]*B[j] + B[j]*B[i] == target, f'B Pauli {i},{j}')
        require(A[i]*B[j] == B[j]*A[i], f'A,B commute {i},{j}')

SIGMA = sum((A[i] * B[i] for i in range(3)), Z)
SINGLET = (I - SIGMA) / 4
TRIPLET = (3*I + SIGMA) / 4
require(SIGMA*SIGMA == 3*I - 2*SIGMA, 'spin-dot minimal polynomial')
for P,name,t in [(SINGLET,'singlet',4),(TRIPLET,'triplet',12)]:
    require(P*P == P and P == P.T, name+' projector')
    require(sp.trace(P) == t, name+' dimension')
require(SINGLET*TRIPLET == Z and SINGLET+TRIPLET == I, 'split')

v = sp.Rational
DIRECTIONS = [
    (1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),
    (v(3,5),v(4,5),0),(v(3,5),0,v(4,5)),(0,v(3,5),v(4,5)),
]


def dot(s,t):
    return sum((s[i]*t[i] for i in range(3)),sp.S.Zero)


def linear_comb(s,matrices):
    return sum((s[i]*matrices[i] for i in range(3)),Z)


def projector(s,side='both'):
    require(dot(s,s) == 1,'nonunit s')
    left=(I-linear_comb(s,A))/2
    right=(I-linear_comb(s,B))/2
    return {'left':left,'right':right,'both':left*right}[side]

P = [projector(s) for s in DIRECTIONS]
PLEFT = [projector(s,'left') for s in DIRECTIONS]
for i,(s,p) in enumerate(zip(DIRECTIONS,P)):
    # The physical-measurement candidate keeps all four outcomes, not only
    # the double-minus one. They are complete commuting effects at fixed s.
    lhs=linear_comb(s,A)
    rhs=linear_comb(s,B)
    complete=[(I+sign_l*lhs)*(I+sign_r*rhs)/4
              for sign_l in (-1,1) for sign_r in (-1,1)]
    require(sum(complete,Z)==I,'four outcomes complete')
    for pi in complete:
        require(pi.T==pi and pi*pi==pi and sp.trace(pi)==4,
                'positive four-outcome projectors')
    require(complete[0]==p,'double-minus is one of four complete outcomes')
    # A singlet is invisible to the selected double-minus null flux, not to
    # its ENTIRE experiment: opposite-sign outcomes each retain 1/2 mass.
    ps=[sp.trace((SINGLET/4)*pi) for pi in complete]
    require(ps==[0,sp.Rational(1,2),sp.Rational(1,2),0],
            'complete singlet law preserves two pointer outcomes')
    require(p.T == p and p*p == p and sp.trace(p)==4, f'full projector {i}')
    require(SINGLET*p == Z and TRIPLET*p == p, f'pure triplet {i}')
    require(PLEFT[i].T == PLEFT[i] and PLEFT[i]*PLEFT[i] == PLEFT[i]
            and sp.trace(PLEFT[i])==8, f'left projector {i}')

# Spatial SO(3) naturality on the existing exterior algebra: a rational 3-4-5
# rotation changes the direction but neither the projector family nor the
# relative-chirality orientation. This is not a generic Lorentz-boost proof.
O = sp.eye(4)
O[1,1] = sp.Rational(3,5)
O[1,2] = -sp.Rational(4,5)
O[2,1] = sp.Rational(4,5)
O[2,2] = sp.Rational(3,5)
require(O.T * O == I[:4,:4] and O.det()==1,'spatial O')

def exterior_lift(M):
    out=sp.zeros(N)
    for source in range(N):
        cols=[i for i in range(4) if source & (1<<i)]
        for target in range(N):
            rows=[i for i in range(4) if target & (1<<i)]
            if len(cols)==len(rows):
                out[target,source]=M.extract(rows,cols).det() if cols else 1
    return out

U = exterior_lift(O)
require(U.T * U == I, 'exterior rotation orthogonal')
require(U*SINGLET*U.T == SINGLET and U*TRIPLET*U.T == TRIPLET,
        'spin zero/one decomposition rotationally covariant')
for s in DIRECTIONS:
    rot = tuple(sum((O[i+1,j+1]*s[j] for j in range(3)),sp.S.Zero) for i in range(3))
    require(U*projector(s)*U.T == projector(rot), 'SO3 covariance')

# Relative chirality is non-optional for the canonical 4+12 spin split.
SIGMA_RAW = sum((A[i]*B_RAW[i] for i in range(3)),Z)
SIGMA_WRONG = sum((A[i]*RELATIVE_CHIRALITY*B_RAW[i] for i in range(3)),Z)
require(SIGMA_RAW.eigenvals()=={-3:2,3:2,-1:6,1:6},'raw chirality spectrum')
require(SIGMA_WRONG.eigenvals()=={3:4,-1:12},'opposite central sign control')

for i,s in enumerate(DIRECTIONS):
    for j,t in enumerate(DIRECTIONS):
        overlap=(1+dot(s,t))**2
        require(sp.trace(P[i]*P[j])==overlap, f'overlap kernel {i},{j}')

# The Gram rank is exact, no numeric SVD or tolerance is involved.
K=sp.Matrix(9,9,lambda i,j: (1+dot(DIRECTIONS[i],DIRECTIONS[j]))**2)
Kc=K-sp.ones(9,9) # Gram of effects P-I/4 in the 16D Hilbert-Schmidt inner product.
require(K.det()!=0 and Kc.det()!=0,'full nine signal directions')
# Distinct settings are NOT a jointly measurable single-system POVM.
commutator = P[0]*P[2]-P[2]*P[0]
require(commutator != Z and sp.trace(commutator.T*commutator)==sp.Rational(3,2),
        'nine settings are noncommuting alternatives, not simultaneous readout')

# l=0,1,2 harmonic basis. On the sphere s^2=1 it is 1+3+5 dimensional.
def hrow(s):
    x,y,z=s
    return [1,x,y,z,x*x-z*z,y*y-z*z,x*y,x*z,y*z]
H=sp.Matrix([hrow(s) for s in DIRECTIONS])
require(H.det()!=0,'harmonic sample interpolation')
require(sp.Matrix(9,9,lambda i,j:sp.trace(PLEFT[i]*PLEFT[j])).rank()==4,
        'one-sided readout too large')
require(sp.Matrix(9,9,lambda i,j:sp.trace(P[i]*P[j])).rank()==9,
        'two-sided readout full rank')

# Trace-free Lorentz tensor associated with all nine native Born probabilities.
# Defined only as mathematical operational symbol; it is NOT physical stress.
# For rho, q(s)=Tr rho P(s)=w/3+v_i s_i+Q_ij s_i s_j.
def null_tensor_from_state(rho):
    require(sp.trace(rho)==1,'normalization')
    w=sp.trace(rho*TRIPLET)
    v3=[-sp.trace(rho*(A[i]+B[i]))/4 for i in range(3)]
    corr=sp.Matrix(3,3,lambda i,j: sp.trace(rho*(A[i]*B[j]+A[j]*B[i]))/8)
    quad=corr-(sp.trace(corr)/3)*sp.eye(3)
    T=sp.zeros(4)
    T[0,0]=w/4
    for i in range(3):
        T[0,i+1]=v3[i]/2
        T[i+1,0]=v3[i]/2
        for j in range(3):
            T[i+1,j+1]=quad[i,j]+(w/12 if i==j else 0)
    require(T[0,0]-sum(T[i,i] for i in range(1,4))==0,'eta tracefree')
    for s,p in zip(DIRECTIONS,P):
        k=sp.Matrix([1,*s])
        require((k.T*T*k)[0]==sp.trace(rho*p),'null tensor matches physical effects')
    return T,w

rho0=SINGLET/4
T0,w0=null_tensor_from_state(rho0)
require(T0==sp.zeros(4) and w0==0,'spin singlet is null-silent')
rho1=TRIPLET/12
T1,w1=null_tensor_from_state(rho1)
require(w1==1 and T1[0,0]==sp.Rational(1,4),'triplet w')
require(all(sp.trace(rho1*p)==sp.Rational(1,3) for p in P),'isotropic triplet signal')

# Local surjectivity: for any nine sufficiently small independent changes in
# measured Born probabilities, the original faithful CAR16 density can realize
# them. This is kinematic distinguishability, NOT an Einstein source law.
P_TRACLESS = [pi-I/4 for pi in P]
unit_target = sp.Matrix([1]+[0]*8)
coefficients=Kc.inv()*unit_target
DRHO=sum((coefficients[j]*P_TRACLESS[j] for j in range(9)),Z)
require(DRHO == DRHO.T and sp.trace(DRHO)==0,'traceless preparation tangent')
require(sp.Matrix([sp.trace(DRHO*pi) for pi in P])==unit_target,
        'exact nine-source preparation interpolation')
row_sum=max(sum(abs(DRHO[i,j]) for j in range(N)) for i in range(N))
epsilon_pos=1/(32*(row_sum+1))
RHO_SMALL=I/16 + epsilon_pos*DRHO
require(sp.trace(RHO_SMALL)==1 and RHO_SMALL==RHO_SMALL.T,
        'normalized perturbed preparation')
# Strict diagonal dominance with positive diagonal implies positive definite.
for i in range(N):
    require(RHO_SMALL[i,i]>sum(abs(RHO_SMALL[i,j]) for j in range(N) if j!=i),
            'positive exact nine-direction preparation')

# A measured address distribution can *conditionally* fix the chi-mode without
# any fitted Einstein counterterm, if and only if the native complete-code
# probabilities/source actually equal these addresses. The Hessian is Fisher,
# not part of the five-flag price unless an inherited record supplies it.
mu1,mu2,muc=sp.Rational(1,8),sp.Rational(1,4),sp.Rational(5,8)
xi1,xi2=sp.symbols('xi1 xi2',real=True)
FISHER=sp.Matrix([[mu1+mu1**2/muc,mu1*mu2/muc],
                  [mu1*mu2/muc,mu2+mu2**2/muc]])
require(FISHER[0,0]>0 and FISHER.det()>0,
        'conditional address Code-Info strictly convex in conformal preparation')
require(sp.expand((sp.Matrix([xi1,xi2]).T*FISHER*sp.Matrix([xi1,xi2]))[0]
             -mu1*xi1**2-mu2*xi2**2-(mu1*xi1+mu2*xi2)**2/muc)==0,
        'exact Fisher Hessian')

# Negative control: duplicated ninth ray loses one independent off-diagonal shear component.
Hbad=sp.Matrix([hrow(s) for s in DIRECTIONS[:8]+DIRECTIONS[:1]])
require(Hbad.rank()==8,'duplicate ninth ray must not reconstruct 9')

# Nonlinear conformal identity for every null k, specialized to the exact 
# flat/null physical counterexample of #334; no Einstein equation inserted.
u,kappa=sp.symbols('u kappa',real=True)
chi=sp.exp(2*kappa*u)
r=sp.exp(kappa*u)
conformal_null_defect=sp.simplify(sp.diff(sp.log(chi),u,2)
                                   +sp.diff(sp.log(chi),u)**2/2)
# Compute R_uu directly from the full four-index Christoffel formula for
# eta=-2 du dv + dx^2 + dy^2 and g_tilde=e^(-2 kappa u) eta.
# Since g_uu=0, G_uu=R_uu. The conformal connection coefficients are
# Gamma^lambda_mu nu = delta^lambda_mu omega_nu + delta^lambda_nu omega_mu
#                      - eta_mu nu eta^lambda rho omega_rho.
ETA_NULL = sp.Matrix([[0,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
eta_inv = ETA_NULL.inv()
omega_grad = sp.Matrix([-kappa,0,0,0])
Gamma = [[[sp.KroneckerDelta(l,m)*omega_grad[n]
           +sp.KroneckerDelta(l,n)*omega_grad[m]
           -ETA_NULL[m,n]*sum((eta_inv[l,h]*omega_grad[h] for h in range(4)),sp.S.Zero)
           for n in range(4)] for m in range(4)] for l in range(4)]
# All Christoffels are constant since omega=-kappa u is affine, so derivative
# terms of Ricci vanish here.
G_uu = sp.simplify(
    sum((Gamma[l][0][0]*Gamma[s][l][s]
         -Gamma[s][0][l]*Gamma[l][0][s]
        for l in range(4) for s in range(4)),sp.S.Zero))
require(sp.simplify(G_uu-2*kappa**2)==0,'direct conformal Ricci uu')
require(sp.simplify(conformal_null_defect-2*sp.diff(r,u,2)/r)==0,
        'square-root GNS focusing identity')
require(sp.simplify(conformal_null_defect-G_uu)==0,'#334 conformal Einstein control')
require(sp.simplify(G_uu.subs(kappa,1))!=0,'conformal mode must remain non-Einstein')

res={
    'schema':'d0-car16-two-sided-null-tomography/1',
    'status':'EXACT_ALGEBRA_PASS',
    'physics_derived':False,
    'CAR_order':'A,C,D,B',
    'carrier_dim':16,
    'left_right_clifford_commute':True,
    'spatial_SO3_covariant':True,
    'relative_chirality_repair':'-Omega_A Omega_B on right spatial Pauli generators',
    'null_effect_rank':4,
    'one_sided_effect_rank':8,
    'silent_singlet_rank':int(sp.trace(SINGLET)),
    'active_triplet_rank':int(sp.trace(TRIPLET)),
    'one_sided_span_rank':4,
    'two_sided_span_rank':9,
    'nine_harmonic_det':str(H.det()),
    'nine_effect_hs_det':str(K.det()),
    'nine_effect_traceless_hs_det':str(Kc.det()),
    'null_overlap':'Tr(P(s) P(t))=(1+s dot t)^2',
    'null_harmonic_decomposition':'l=0+1+2, ranks 1+3+5',
    'null_singlet_effect_zero':True,
    'complete_four_outcomes':True,
    'cross_setting_noncommutation':True,
    'singlet_complete_law':'(0,1/2,1/2,0)',
    'exact_state_response_local_surjectivity':True,
    'address_binding_conditional_Fisher_Hessian':str(FISHER),
    'raw_chirality_eigenspaces':'(-3)^2,(-1)^6,(+1)^6,(+3)^2',
    'triplet_isotropic_q':'1/3',
    'tracefree_lorentz_null_tensor_matches':True,
    'conformal_focusing':'G[chi^-1 g](k,k)-G[g](k,k)=2 r^-1 Hess_g(r)(k,k), r=sqrt(chi)',
    'negative_controls':['cannot combine nine different directions as one commuting measurement',
                         'naive raw relative-chirality split has four eigenvalues',
                         'opposite central orientation has no silent subspace',
                         'one-sided span rank 4, not 9',
                         'duplicated mixed sample drops rank to 8',
                         'nonconstant conformal chi leaves nonzero Einstein null defect'],
    'unproved':['physical admission of left/right projector measurements in the original Julia128 words',
                'independent inherited-address complete code prior and its source',
                'same-full-price geometric/matter source identification',
                'dynamical selection or sourcing of the conformal GNS amplitude',
                'real null-flux normalization, local stress conservation and spacetime refinement']
}
print(json.dumps(res,indent=2,ensure_ascii=False,sort_keys=True))