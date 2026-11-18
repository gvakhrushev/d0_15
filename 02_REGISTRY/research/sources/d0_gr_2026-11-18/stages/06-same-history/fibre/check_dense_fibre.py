"""Check the actual six-wire macros and the small finite common-layout secants."""
from collections import Counter
from fractions import Fraction as F
from math import asin, cos, isqrt, sqrt
from pathlib import Path
import hashlib, importlib.util, json, sys
import sympy as S

owner = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"frozen"/"native_execution.py"
assert hashlib.sha256(owner.read_bytes()).hexdigest()=="222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
s=importlib.util.spec_from_file_location("dense_fibre_native",owner)
ne=importlib.util.module_from_spec(s);sys.modules[s.name]=ne;s.loader.exec_module(ne)
src,e,r,t=0,3,4,5
def cx(i,j):return ne.Gate("CX",(i,j))
c=cx(e,r);d=cx(e,t);g=ne.Gate("G",(t,))
sw=(cx(src,t),cx(t,src),cx(src,t))
z=sw+(ne.Gate("SourceI",(src,1,2)),)*2+sw
mg=z+(g,)+z
def ex(word):return ne.Execution(6,(e,r,t),(),tuple(word),ne.G_CX_SOURCE_I,src,(1,2),())
def mat(g):return ne.gate_matrix(ex((g,)),g)
Z=S.eye(64)
for x in z:Z=mat(x)*Z
assert Z==S.diag(*[(-1 if i&1 else 1) for i in range(64)])
GG=mat(g);C=mat(c);D=mat(d)
assert Z*GG*Z==GG.T
assert C*C==D*D==S.eye(64)
for j in range(64):
    # Fresh basis order is (src,spin1,spin2,e,r,t).
    assert C[j^(((j>>2)&1)<<1),j]==1 and D[j^((j>>2)&1),j]==1
for i in range(32):
    assert GG[2*i:2*i+2,2*i:2*i+2]==ne.G_LOCAL
assert GG==S.kronecker_product(S.eye(32),ne.G_LOCAL)

# Exact Q[a], a^4=1-a^2, p=a^2. Full rotation pairs use ordinary complex multiplication.
zero=(0,0,0,0);one=(1,0,0,0);aa=(0,1,0,0);pp=(0,0,1,0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mult(a,b):
    z=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    for k in range(6,3,-1):
        z[k-4]+=z[k];z[k-2]-=z[k]
    return tuple(z[:4])
def cm(a,b):return (add(mult(a[0],b[0]),neg(mult(a[1],b[1]))),add(mult(a[0],b[1]),mult(a[1],b[0])))
def star(a):return a[0],neg(a[1])
unit=(one,zero)
def power(k):
    g=(aa,pp) if k>=0 else (aa,neg(pp));k=abs(k);v=unit
    while k:
        if k%2:v=cm(v,g)
        g=cm(g,g);k//=2
    return v
assert cm((aa,pp),star((aa,pp)))==unit
def allblocks(n,N):
    # Matrix X reverses the rotation on the e=1 branch.
    v=[];rr=[]
    for sector in (0,1):
        h=-1 if sector else 1
        v.append(cm(cm(power(N-n),power(h*n)),power(-N)))
        rr.append(cm(cm(power(N),power(-h*n)),power(-(N-n))))
    assert v[0]==unit and v[1]==power(-2*n)
    assert all(cm(x,y)==unit for x,y in zip(v,rr))
    # C only changes r conditioned on e. It commutes with either of these t rotations.
    assert all(a==star(b) for a,b in zip(v,rr))
def word(n,N):
    # V then C then a (possibly independently expanded) physical V adjoint.
    before=mg*N+(d,)+(g,)*n+(d,)+(g,)*(N-n)
    after=mg*(N-n)+(d,)+mg*n+(d,)+(g,)*N
    assert len(before)==18*N+2 and len(after)==18*N+2
    W=before+(c,)+after
    ne.validate_execution(ex(W),max_qubits=6,max_expanded_stages=len(W)+1)
    return W
def compact_word(n,N):
    def backwards(k):
        return z+(g,)*k+z
    before=backwards(N)+(d,)+(g,)*n+(d,)+(g,)*(N-n)
    after=backwards(N-n)+(d,)+backwards(n)+(d,)+(g,)*N
    W=before+(c,)+after
    assert len(before)+1==2*N+19 and len(W)==4*N+53
    ne.validate_execution(ex(W),max_qubits=6,max_expanded_stages=len(W)+1)
    return W
# Independent, bounded rounding of unit-circle projections using binary powers.
scale=10**50
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a):return -a[1],-a[0]
def prod(a,b):
    v=[x*y for x in a for y in b]
    return min(v)//scale,-((-max(v))//scale)
def cmI(a,b):return plus(prod(a[0],b[0]),minus(prod(a[1],b[1]))),plus(prod(a[0],b[1]),prod(a[1],b[0]))
lo=(isqrt(5*scale*scale)-scale)//2
pI=(lo,lo+1)
aI=(isqrt(scale*pI[0]),isqrt(scale*pI[1])+1)
def band(k):
    z=((scale,scale),(0,0));w=(aI,pI)
    while k:
        if k%2:z=cmI(z,w)
        w=cmI(w,w);k//=2
    return z
def strband(v,digs=12):
    fact=10**digs
    return [str(F(a,fact)) for a in (v[0]*fact//scale, -((-v[1]*fact)//scale))]
cases=[]
for den in (8,16,32):
    h=F(1,den)
    # Floating proposals are verified by outward integer arithmetic below.
    theta=asin((sqrt(5)-1)/2)
    picks=[next(k for k in range(200_000) if abs(cos(2*k*theta)-s*float(h))<float(h*h)) for s in (-1,1)]
    N=max(picks);states=[band(2*k)[0] for k in picks];words=[]
    for n,sgn,v in zip(picks,(-1,1),states):
        assert sgn*h-h*h < F(v[0],scale) <= F(v[1],scale) < sgn*h+h*h
        allblocks(n,N);words.append(word(n,N))
    assert Counter(words[0])==Counter(words[1])
    short=[compact_word(n,N) for n in picks]
    assert Counter(short[0])==Counter(short[1])
    assert Counter(op.op for op in short[0])=={"G":4*N,"CX":41,"SourceI":12}
    inventory=Counter(x.op for x in words[0])
    assert inventory=={"G":4*N,"CX":24*N+5,"SourceI":8*N}
    delta=plus(states[1],minus(states[0]))
    cases.append(dict(h=str(h),n_minus=picks[0],n_plus=picks[1],N=N,
                      minus_u=strband(states[0]),plus_u=strband(states[1]),delta_u=strband(delta),
                      compact_stages=len(short[0]),compact_central_C_one_based=2*N+19,stages=len(words[0]),central_C_one_based=18*N+3,inventory=dict(sorted(inventory.items()))))
co,si=band(512)
assert co[1]<0<si[0]
v=[F(x,y) for x in co for y in si]
assert F(-258,1000)<min(v)<max(v)<F(-257,1000)
print(json.dumps(dict(status="PASS_ACTUAL_DENSE_FIBRE",actual_gate_owner_sha256=hashlib.sha256(owner.read_bytes()).hexdigest(),
                  checked_live_basis_columns=64,ring="a^4=1-a^2,p=a^2",cases=cases,
                  literal_reporter_Re_gamma_over_Q_interval=["-0.258","-0.257"],
                  exact_X_secant_over_Re_gamma=2,exact_direct_G_NC1_paid_length_secant_over_Re_gamma="2 sqrt(p) p",
                  same_layout_unread_master_secant=0,assumes_internal_e_was_not_pinched=True),indent=2))
