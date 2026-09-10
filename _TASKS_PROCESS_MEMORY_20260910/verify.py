"""Exact endpoint/process calculations, independent of the Lean Bloch-coordinate proof."""
from pathlib import Path
import json
import sympy as s

a,p,k,l,x,y,z,u,v = s.symbols('a p k l x y z u v', real=True)
gb=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(k,l,x,y,z))
checks=0
def red(e):
    return s.factor(gb.reduce(s.expand(e))[1])
def zero(e):
    global checks
    e=s.expand(e)
    assert red(s.re(e))==0 and red(s.im(e))==0, e
    checks+=1
def checkmat(m):
    for e in m: zero(e)

I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
G=s.Matrix([[a,-p],[p,a]])
M=G.T*Z*G
c=p-p*p
def endpoint(rho, contraction):
    total=s.trace(rho)
    contrast=contraction*s.trace(M*rho)
    return s.diag((total+contrast)/2,(total-contrast)/2)
def step(rho): return endpoint(rho,1)

rho=(I+x*X+y*Y+z*Z)/2
# Universal induction step for the complete endpoint channel, not just diagonal inputs.
checkmat(step(endpoint(rho,k))-endpoint(rho,c*k))
J=s.zeros(4)
for i in range(2):
    for j in range(2):
        E=s.zeros(2); E[i,j]=1
        J[2*i:2*i+2,2*j:2*j+2]=endpoint(E,k)
J=J.applyfunc(red)
zero((l*s.eye(4)-J).det()-((l-(1+k)/2)*(l-(1-k)/2))**2)
J1=J.subs(k,1)
checkmat(J1*J1-J1)
zero(s.trace(J1)-2)

# Explicit four-Kraus endpoint realization; amplitudes u,v satisfy the weights below.
ket0=s.Matrix([1,0]); ket1=s.Matrix([0,1])
K=[u*ket0*G[0,:],v*ket1*G[0,:],v*ket0*G[1,:],u*ket1*G[1,:]]
def weights(m):
    return m.applyfunc(lambda e:s.expand(e).subs(u*u,(1+k)/2).subs(v*v,(1-k)/2))
checkmat(weights(sum((q.T*q for q in K),s.zeros(2)))-I)
checkmat(weights(sum((q*rho*q.T for q in K),s.zeros(2)))-endpoint(rho,k))

# Both two-stage processes have the same no-intervention endpoint.
checkmat(step(step(rho))-endpoint(rho,c))
fresh=s.diag(1,0)
after_A=step(fresh)
after_B=endpoint(fresh,c)
zero(s.trace(Z*after_A)-c)
zero(s.trace(Z*after_B)-c*c)
prob_gap=red(after_A[0,0]-after_B[0,0])
zero(prob_gap-(c-c*c)/2)

# Full internal check: system + two retained record bits + the prepared SWAP register.
# A common three-stage schedule is A=(Phi,id,Phi), B=(id,Phi,Phi), with SWAP
# after stage one. This equalizes the number of primitive channel uses and clock slots.
def start():
    V=s.zeros(16,2); V[0,0]=1; V[8,1]=1
    return V
def golden_record(V,record):
    out=s.zeros(16,2)
    for old in range(16):
        old_sys=(old>>3)&1
        for new_sys in range(2):
            target=(old&7)|(new_sys<<3)
            if new_sys: target^=1<<record
            for src in range(2): out[target,src]+=G[new_sys,old_sys]*V[old,src]
    return out.applyfunc(red)
def swap_prepared(V):
    out=s.zeros(16,2)
    for old in range(16):
        target=(old&6)|((old&1)<<3)|((old>>3)&1)
        out[target,:]=V[old,:]
    return out
def reduced_system(V):
    joint=V*rho*V.T
    return s.Matrix(2,2,lambda i,j:sum(joint[8*i+r,8*j+r] for r in range(8)))
VA=golden_record(swap_prepared(golden_record(start(),2)),1)
VB=golden_record(golden_record(swap_prepared(start()),2),1)
checkmat(VA.T*VA-I); checkmat(VB.T*VB-I)
checkmat(reduced_system(VA)-after_A)
checkmat(reduced_system(VB)-after_B)

phi=(1+s.sqrt(5))/2
golden_c=s.simplify(phi**-3)
result=dict(status='PASS',exact_scalar_checks=checks,
 endpoint_choi_eigenvalues=['(1+k)/2','(1+k)/2','(1-k)/2','(1-k)/2'],
 endpoint_parameter='k=c^(n-1), n>=1',endpoint_min_pure_environment_dim={'n=1':2,'n>=2':4},
 process_choi='J(step) tensor power n; projector, rank=trace=2^n',
 process_memory_scope='All intermediate interventions; pure closed dilation, no external reset or discarded records',
 reset_probability_gap_exact=str(s.simplify((golden_c-golden_c**2)/2)),
 reset_probability_gap=float((golden_c-golden_c**2)/2),
 full_internal_swap_checked=True, full_internal_dimension=16,
 endpoint_compression_scope='Fixed endpoint channel only; does not preserve the full intervention interface')
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
