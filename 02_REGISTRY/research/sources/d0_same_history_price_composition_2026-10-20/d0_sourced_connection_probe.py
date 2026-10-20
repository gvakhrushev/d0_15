"""New bounded calculation: full connection jet of the owned initial clock source.
No old certificate or spectral suite is replayed.  Rational nu=3/5, b=4/5.
The continuum coefficient is expanded at H=a sin(x), omega_r=a C_r cos(x).
Only the source coefficient, not a fixed-positive-clock limit, is computed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=Path,required=True,help='original D0 repository root')
args=parser.parse_args()
checks=0
def require(condition,message):
    global checks
    if not condition:
        raise RuntimeError(message)
    checks+=1

INPUT_PINS={
 '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md':'2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
 '02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md':'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
 '02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/original_record_source.md':'3e038dd9fae47bee12e9df6c27ed2b0816c577a47e0581cf6b9f84e976f3cc0c',
 '02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/price_equivalence2_smooth.py':'393c459c5295e3e3af413f6c935b4eb4402cd4b8b714761548b7dbc7e8b0b0c8',
 '02_REGISTRY/research/A4D_BOOK_CAR_HOLST_WEYL_BRANSDICKE_EINSTEIN_UNIVERSALITY_2026_10_20.md':'c7d1c5adb00ef5f6b17e9f23c5fffe4ec649ea2194bba6d6f5dbd93847a0c7de',
 '02_REGISTRY/research/A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md':'f54810cf9cc16f2282eb602fa606381cdd9622c7f877fef5211e978c55e4956c',
 '02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/coframe_oracle_transport.md':'28a2d3db0545f1bd0dd96e9394a8f350b403db75348df590d75d035db1cc8c65',
}
def check_input_pins():
    for relative,expected_hash in INPUT_PINS.items():
        actual_hash=hashlib.sha256((args.root/relative).read_bytes()).hexdigest()
        require(actual_hash==expected_hash,f'input pin mismatch: {relative}')
check_input_pins()

nu=s.Rational(3,5); b=s.Rational(4,5); I=s.eye(16)
cre=[]
for j in range(4):
    m=s.zeros(16)
    for mask in range(16):
        if not mask>>j&1:
            m[mask|1<<j,mask]=(-1)**((mask&((1<<j)-1)).bit_count())
    cre.append(m)
Jq=cre[1]-cre[1].T; Jx=cre[2]-cre[2].T
good=[0,2,5,7,8,10,13,15]
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
gens=[]
for i,j in pairs:
    F=s.zeros(4); F[i,j]=1; F[j,i]=-1
    gens.append(eta*F)
require(gens[1][1,2]==gens[1][2,0]==1,'original N_x generator')
# Bind the actual inverse creation legs to their coframe before identifying
# Levi-Civita.  The spatial coframe signs are forced by V=eta e^{-T}.
profile,profile_prime=s.symbols('profile profile_prime',real=True)
coframe=s.Matrix([[1,0,0,0],[profile/2,1,0,0],[0,0,-1,0],[0,0,0,-1]])/nu
native_legs=nu*s.Matrix([[0,1,0,0],[1,-profile/2,0,0],[0,0,1,0],[0,0,0,1]])
require(eta*coframe.inv().T==native_legs,'literal native inverse-coframe map')
def cartan_torsion(null_coefficient):
    omega=[null_coefficient*gens[1],s.zeros(4),s.zeros(4),s.zeros(4)]
    derivatives=[s.zeros(4),s.zeros(4),coframe.diff(profile)*profile_prime,s.zeros(4)]
    return [derivatives[r][:,q]-derivatives[q][:,r]+omega[r]*coframe[:,q]-omega[q]*coframe[:,r]
            for r in range(4) for q in range(r+1,4)]
require(all(T==s.zeros(4,1) for T in cartan_torsion(-profile_prime/2)),
        'all Cartan torsion components at the actual LC sign')
require(any(T!=s.zeros(4,1) for T in cartan_torsion(profile_prime/2)),
        'old plus-sign LC interpretation must be rejected')
Qs=[]
for role in [1,0,2,3]:
    for G in gens:
        Gf=sum((G[i,j]*cre[i]*cre[j].T for i in range(4) for j in range(4)),s.zeros(16))
        X=cre[role]*Gf
        Qs.append(X+X.T)
t=s.symbols('t0:24',real=True)
Q=sum((x*A for x,A in zip(t,Qs)),s.zeros(16))
D0=nu*Jq  # actual D_0 = i D0

def inner(A,B):
    return sum((A[i,j]*B[i,j] for i in range(16) for j in good),s.S.Zero)/8

# Real matrices represent A1=i*(real A1), and A0,A2 are real.
Gexpr=s.S.Zero
for role,axis in enumerate([1,0,2,3]):
    c=cre[axis]; cv=nu*c
    Ws=[cv,cv.T,I+(b-1)*c*c.T,I+(b-1)*c.T*c]
    if role==1:
        d=cre[1]
        WH=[-nu*d/2,-nu*d.T/2,
            -(b-1)*(d*c.T+c*d.T)/2,
            -(b-1)*(d.T*c+c.T*d)/2]
        b2=-nu**2/(4*b)
        WHH=[s.zeros(16),s.zeros(16),
             b2*c*c.T+(b-1)*(d*d.T-c*c.T)/2,
             b2*c.T*c+(b-1)*(d.T*d-c.T*c)/2]
    else:
        WH=WHH=[s.zeros(16) for _ in range(4)]
    for W,dW,ddW in zip(Ws,WH,WHH):
        A0=-D0*W*D0
        A2=nu**2*Q*W*Q/2-D0*ddW*D0/4
        val=2*inner(A0,A2)
        for sign in [-1,1]:
            Dside=nu*(Jq+sign*Jx)
            A1=Dside*W*(nu*Q/2)+(nu*Q/2)*W*D0+sign*Dside*dW*D0/2
            val+=inner(A1,A1)
        Gexpr+=val/8
B2=nu**2*Q*Q/2
Gexpr-=2*inner(nu**2*I,B2)
for sign in [-1,1]:
    B1=nu*(Jq+sign*Jx)*(nu*Q/2)+(nu*Q/2)*D0
    Gexpr-=inner(B1,B1)
Gexpr=s.Poly(s.expand(Gexpr),t)
zero={x:0 for x in t}
const=Gexpr.eval(zero)
lin=s.Matrix([Gexpr.diff(x).eval(zero) for x in t])
Hn=s.Matrix([[Gexpr.diff(x).diff(y).eval(zero) for y in t] for x in t])
ratio=s.symbols('r',real=True)
slice_value=s.expand(Gexpr.as_expr().subs({x:(ratio if i==1 else 0) for i,x in enumerate(t)}))
slice_expected=nu**4/s.Integer(16)*((1-b)/2+(nu**2/2)*ratio+nu**2*ratio**2)
require(s.expand(slice_value-slice_expected)==0,'owned one-null-link slice')

# Independent forward Fourier-jet evaluation of the actual operator expression
# Tr rho [sum_j (D W_j D)^*(D W_j D)/8 - (D²)^*(D²)].
# Unlike the compact expression above, this propagates every amplitude jet
# and includes the mixed coframe/connection D2 term before taking the trace.
def direct_fourier_jet(values):
    Qv=Q.subs(dict(zip(t,values)))
    Gv=sum((values[6+j]*G for j,G in enumerate(gens)),s.zeros(4))
    Gvf=sum((Gv[i,j]*cre[i]*cre[j].T for i in range(4) for j in range(4)),s.zeros(16))
    X=cre[1]*Gvf; QH=-(X+X.T)/2
    def apply(vec,kind,W=None,dW=None,ddW=None):
        out={}
        def add(deg,mode,A,v):
            if deg<=2:
                out[deg,mode]=out.get((deg,mode),s.zeros(16,1))+A*v
        for (degree,mode),v in vec.items():
            if kind=='D':
                add(degree,mode,s.I*nu*(Jq+mode*Jx),v)
                for sign in [-1,1]:
                    add(degree+1,mode+sign,nu*Qv/2,v)
                    add(degree+2,mode+2*sign,-s.I*sign*nu*QH/4,v)
            else:
                add(degree,mode,W,v)
                add(degree+2,mode,ddW/4,v)
                for sign in [-1,1]:
                    add(degree+1,mode+sign,-s.I*sign*dW/2,v)
                    add(degree+2,mode+2*sign,-ddW/8,v)
        return out
    def norm2(v):
        ans=s.S.Zero
        for (degree,mode),x in v.items():
            if degree==1: ans+=(x.conjugate().T*x)[0]
            if degree==0 and (2,mode) in v:
                y=v[2,mode]; ans+=(x.conjugate().T*y+y.conjugate().T*x)[0]
        return ans
    ans=s.S.Zero
    for mask in good:
        initial={(0,0):I[:,mask]}
        Dpsi=apply(initial,'D')
        ans-=norm2(apply(Dpsi,'D'))/8
        for role,axis in enumerate([1,0,2,3]):
            c=cre[axis]; d=cre[1]
            Ws=[nu*c,nu*c.T,I+(b-1)*c*c.T,I+(b-1)*c.T*c]
            if role==1:
                WH=[-nu*d/2,-nu*d.T/2,-(b-1)*(d*c.T+c*d.T)/2,-(b-1)*(d.T*c+c.T*d)/2]
                b2=-nu**2/(4*b)
                WHH=[s.zeros(16),s.zeros(16),b2*c*c.T+(b-1)*(d*d.T-c*c.T)/2,b2*c.T*c+(b-1)*(d.T*d-c.T*c)/2]
            else: WH=WHH=[s.zeros(16) for _ in range(4)]
            for W,dW,ddW in zip(Ws,WH,WHH):
                ans+=norm2(apply(apply(Dpsi,'W',W,dW,ddW),'D'))/64
    return s.factor(ans)
direct_checks=[]
for values in [tuple(-s.Rational(1,2) if i==1 else 0 for i in range(24)),
               tuple(s.Rational(i%3-1,20) for i in range(24))]:
    actual=direct_fourier_jet(values)
    expected=Gexpr.eval(dict(zip(t,values)))
    require(actual==expected,f'independent Fourier jet: {actual} != {expected}')
    direct_checks.append(str(actual))

# Full original Palatini scalar contorsion Hessian; its diagonal on a sole
# coordinate connection component is zero, but the 24x24 form is invertible.
Hg=s.zeros(24)
role_signs=[1,1,-1,-1]
for i in range(24):
    r,j=divmod(i,6)
    for k in range(24):
        q,l=divmod(k,6)
        Hg[i,k]=2*role_signs[r]*role_signs[q]*((gens[j]*gens[l]-gens[l]*gens[j])*eta)[r,q]
require(Hg==Hg.T,'Palatini Hessian symmetry')
require(Hg.det()==2**32,'Palatini Hessian exact determinant')
lc=s.zeros(24,1); lc[1]=-s.Rational(1,2)
# Independent direct pp Palatini expansion.  e+=du/nu,
# e-=(dv+H du/2)/nu, ex=-dx/nu, ey=-dy/nu. The actual coframe sign
# makes the derivative-curvature cross term +((omega_v eta)[+,x])/2
# after averaging sin²(x). This must equal
# the linear term of (t-lc)^T Hg (t-lc)/4, not a guessed K² penalty.
direct_geom_linear=s.zeros(24,1)
for j,G in enumerate(gens):
    direct_geom_linear[6+j]=(G*eta)[0,2]/2
require(direct_geom_linear==-Hg*lc/2,'actual coframe/derivative curvature cross term')
require((lc.T*Hg*lc)[0]==0,'LC pp scalar quadratic')
spin=lin+Hn*lc
Hgi=Hg.inv()
relative_bound=max(sum(abs(x) for x in row) for row in (Hgi*Hn).tolist())
at_lc=s.factor(const+(lin.T*lc)[0]+(lc.T*Hn*lc)[0]/2)
correction=s.factor((spin.T*Hgi*spin)[0])
known_only=s.zeros(24,1); known_only[1]=spin[1]
component={i for i,x in enumerate(spin) if x!=0}
while True:
    nxt=component|{j for i in component for j in range(24) if Hg[i,j]!=0 or Hn[i,j]!=0}
    if nxt==component: break
    component=nxt
component=sorted(component)
zeta=s.symbols('zeta',real=True)
Ag=Hg.extract(component,component); An=Hn.extract(component,component)
jn=spin.extract(component,[0])
solution=(Ag+zeta*An).inv()*jn
spin_resolvent=s.factor((jn.T*solution)[0])
effective=s.factor(at_lc-zeta*spin_resolvent/2)
complete_solution=s.zeros(24,1)
for j,i in enumerate(component): complete_solution[i]=-zeta*solution[j]
for index,residual in enumerate((Hg+zeta*Hn)*complete_solution+zeta*spin):
    require(s.factor(residual)==0,f'full connection row {index}')
# Strict rational lower bound on the induced pp coefficient for EVERY real
# paid/geometric ratio; no sign or magnitude is tuned to obtain it.
lower=s.Rational(1,2000)
num,den=s.fraction(s.factor(effective-lower))
np=s.Poly(num,zeta); dp=s.Poly(den,zeta)
require(np.degree()==2 and np.LC()>0 and s.discriminant(np.as_expr(),zeta)<0,'strict bound numerator')
require(dp.degree()==2 and dp.LC()>0 and s.discriminant(dp.as_expr(),zeta)<0,'strict bound denominator')
# All remaining full-connection blocks are checked, not discarded.  They
# receive zero forcing here; the actual solution above satisfies every row.
unused=set(range(24)); blocks=[]
while unused:
    part={min(unused)}
    while True:
        grow=part|{j for i in part for j in unused if Hg[i,j]!=0 or Hn[i,j]!=0}
        if grow==part: break
        part=grow
    unused-=part; ids=sorted(part)
    blocks.append({'indices':ids,'det':str(s.factor((Hg+zeta*Hn).extract(ids,ids).det()))})
check_input_pins()
out={
 'status':'PASS','checks':checks,'input_pins':INPUT_PINS,
 'nu':str(nu),'b':str(b),'native_gamma_quadratic_constant':str(const),
 'native_coframe_spatial_signs':[-1,-1],'lc_null_ratio':'-1/2',
 'owned_pp_slice':str(slice_value),'owned_pp_slice_expected':str(slice_expected),
 'palatini_torsion_hessian_det':str(Hg.det()),
 'palatini_null_K_diagonal':str(Hg[1,1]),
 'gamma_at_lc':str(at_lc),
 'native_full_connection_spin_at_lc':[(i,str(x)) for i,x in enumerate(spin) if x!=0],
 'spin_Hg_inverse_spin':str(correction),
 'single_K_spin_Hg_inverse_spin':str((known_only.T*Hgi*known_only)[0]),
 'source_component_indices':component,
 'source_block_geometric_hessian':[[str(x) for x in row] for row in Ag.tolist()],
 'source_block_native_hessian':[[str(x) for x in row] for row in An.tolist()],
 'source_block_det':str(s.factor((Ag+zeta*An).det())),
 'spin_resolvent':str(spin_resolvent),
 'combined_geometric_plus_paid_stationary_coefficient_per_paid_weight':str(effective),
 'torsion_shift_per_zeta':[(i,str(s.factor(-solution[j]))) for j,i in enumerate(component) if solution[j]!=0],
 'induced_pp_lower_bound_strict':str(lower),
 'lower_bound_numerator':str(num),
 'lower_bound_denominator':str(den),
 'all_connection_block_determinants':blocks,
 'Hn_rank':Hn.rank(),
 'native_vs_Palatini_operator_infinity_bound':str(relative_bound),
 'sufficient_full_connection_invertibility':f'abs(zeta) < {1/relative_bound}',
 'independent_forward_fourier_checks':direct_checks,
 'scope':'initial clock coefficient at the homogeneous pp jet; actual fixed protected8 preparation; all 24 Lorentz connection components in the stated single transverse Fourier jet; no full native action identification or uniform fixed-clock limit',
}
print(json.dumps(out,indent=2))
