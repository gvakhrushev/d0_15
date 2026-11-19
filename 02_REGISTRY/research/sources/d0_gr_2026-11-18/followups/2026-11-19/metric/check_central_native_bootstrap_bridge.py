"""Common native centre, two arms, retained output and marked-clock gap.

The q-dependent words are finite; their common fixed-CX input and actual
terminal NC1 are checked. No common differentiable physical clock or complete
Book03 source is asserted.
"""
import json
import math
import numpy as np
import mpmath as mp
from check_clock_coherence import mm
p=(math.sqrt(5)-1)/2;a=math.sqrt(p);ap=a*p;theta=math.asin(p)
G=np.array([[a,-p],[p,a]]);I=np.eye(2);Z=np.diag([1.,-1.]);v=np.array([a,p]);plus=np.array([1.,1.])/math.sqrt(2);zero=np.array([1.,0.])
def gate1(mat,w,n):
    out=np.array([[1.]])
    for i in range(n):out=np.kron(out,mat if i==w else I)
    return out
def cx(control,target,n):
    M=np.zeros((1<<n,1<<n))
    for j in range(1<<n):
        bits=[(j>>(n-1-i))&1 for i in range(n)]
        if bits[control]:bits[target]^=1
        k=sum(b<<(n-1-i) for i,b in enumerate(bits));M[k,j]=1
    return M
# Wire order P,H,port. Each Z_H is implemented by physical SWAP, Z_port,
# SWAP; Z_port is the exact SourceI^2 interface with Spin untouched.
A=cx(1,2,3);B=cx(2,1,3);swap=A@B@A
zphys=swap@gate1(Z,2,3)@swap
assert np.allclose(zphys,gate1(Z,1,3),atol=1e-14)
g=gate1(G,1,3);inputstate=cx(0,1,3)@np.kron(plus,np.kron(v,zero))
# Entire unmeasured payload P,H,port differs at the first labelled clock stage.
state_diff=np.linalg.norm(g@inputstate-A@inputstate)
assert abs(state_diff-math.sqrt(2-a*p**3))<1e-14
witness=np.kron(zero,np.kron(zero,zero))
clock_lower=np.linalg.norm((g-A)@witness)
assert abs(clock_lower-math.sqrt(2*(1-a)))<1e-14
# Common NC1 of H, actual fresh v and exact G/CX sequence, retaining P,H,port,A.
N=4;ncx=cx(1,3,N);ng=gate1(G,3,N)
Pi0=np.diag([int(((j>>2)&1)==0) for j in range(16)])
Pi1=np.diag([int(((j>>2)&1)==1 and (j&1)==0) for j in range(16)])
Pid=np.diag([int(((j>>2)&1)==1 and (j&1)==1) for j in range(16)])
def full(u):
    state=mm(ncx,ng,ncx,np.kron(mm(u,inputstate),v))
    s0,s1,sd=[P@state for P in (Pi0,Pi1,Pid)]
    assert np.linalg.norm(sd)<1e-12
    return s0,s1

def record(u):
    s0,s1=full(u);out=np.zeros((32,32));out[:16,:16]=np.outer(s0,s0);out[16:,16:]=np.outer(s1,s1)
    return out,np.dot(s1,s1)
def h(x):return -x*math.log(x)-(1-x)*math.log(1-x)
L=math.log(1/p);examples=[]
for q,turn in ((19,2),(66,7),(613,65)):
    eps=q*theta-2*math.pi*turn;Gq=np.linalg.matrix_power(g,q)
    wp=zphys@zphys@Gq;wm=zphys@Gq@zphys
    centre=wm@wp;up=wp@wp;um=wm@wm
    assert np.linalg.norm(centre-np.eye(8))<1e-12
    rho0,prob0=record(centre);rhop,qp=record(up);rhom,qm=record(um)
    step=2*ap*math.sin(4*eps)
    assert abs(prob0-.5)<1e-12 and abs((qp-qm)-step)<1e-12
    assert abs(qp-(.5+ap*math.sin(4*eps)))<1e-12
    diff=rhop-rhom;tn=float(np.abs(np.linalg.eigvalsh(diff)).sum())
    assert abs(tn-2*abs(math.sin(4*eps)))<1e-12
    assert abs(tn/abs(step)-1/ap)<1e-10
    # Contrast across P-basis controls is p^3 cos(4 epsilon).
    def basis_prob(Pstate,u):
        x=cx(0,1,3)@np.kron(Pstate,np.kron(v,zero))
        y=mm(ncx,ng,ncx,np.kron(mm(u,x),v))
        return np.linalg.norm(Pi1@y)**2
    assert abs((basis_prob(np.array([0.,1.]),up)-basis_prob(np.array([1.,0.]),up))-p**3*math.cos(4*eps))<1e-12
    assert abs((basis_prob(np.array([0.,1.]),um)-basis_prob(np.array([1.,0.]),um))-p**3*math.cos(4*eps))<1e-12
    # Full CQ information is binary h(q); symmetric entropy cancels exactly.
    C=lambda y:1+y-h(y)/L
    assert abs(16*(C(qp)-C(qm))/step-16)<1e-8
    # 16 independent pure input states: product-state trace-distance upper
    # bound after the common CQ instrument; all saved outputs are kept.
    c=math.cos(4*eps)
    bound=math.sqrt(sum(c**(2*j) for j in range(16)))/ap
    assert bound<=4/ap+1e-12
    examples.append({'q':q,'turns':turn,'epsilon':eps,'descriptor_step':step,
      'retained_one_copy_norm_over_step':tn/abs(step),'sixteen_copy_bound':bound,
      'labelled_clock_norm_lower_over_step':clock_lower/abs(step)})
# The original BG rank-16 input cut and the hypothetical |+>-compressed
# rank-8 cut have different feedback, before adding a physical + preparer.
mp.mp.dps=80;pp=(mp.sqrt(5)-1)/2;aa=mp.sqrt(pp);zz=mp.mpf(1)/2**20
c0=pp**2+aa*pp**3;c1=aa*pp**2+pp**3;d0=pp**3-aa*pp**2;d1=aa*pp**3-pp**2
f=lambda c,d:-16*zz*c*d/(1-zz*(1-c*c))
j16=f(c0,d0)+f(c1,d1);j8=f((c0+c1)/2,(d0+d1)/2)
leak=(c0-c1)/2
assert abs(leak-pp**4*(1-aa)/2)<mp.mpf('1e-75') and leak>0
assert abs(j8-j16)>mp.mpf('1e-7')
print(json.dumps({'status':'PASS','clock_operator_lower':clock_lower,
 'central_plus_state_first_stage_vector_difference':state_diff,
 'matched_word_extra_G':'2q','matched_word_extra_CX':24,'matched_word_extra_SourceI':8,
 'central_word':'W+;W- = I','two_arms':'W+;W+ = R(2 epsilon), W-;W- = R(-2 epsilon)',
 'one_copy_exact_norm_over_step':1/ap,'sixteen_copy_norm_over_step_upper':4/ap,
 'recorded_CQ_cost_secant_16':16,'old_rank16_Jprime':mp.nstr(j16,25),
 'hypothetical_plus_compressed_rank8_Jprime':mp.nstr(j8,25),
 'plus_to_minus_return_amplitude':mp.nstr(leak,25),
 'plus_program_cut_invariant_under_full_return':False,
 'rank8_with_actual_plus_preparer_full_clock_rebuilt':False,
 'marked_clock_normalized_operator_bound_diverges':True,
 'complete_General_Relativity_closed':False,'examples':examples},indent=2))
