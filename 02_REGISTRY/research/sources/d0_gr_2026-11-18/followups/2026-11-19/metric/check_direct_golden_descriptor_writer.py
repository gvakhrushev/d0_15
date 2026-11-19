"""Direct CX(P,H), native NC1 and CAR catalog material response.

This is an exact finite logical writer with actual retained NC1 outcomes; a
continuous native preparation of P and full Book03 valuation are not built.
"""
import itertools
import json
import math
import numpy as np
import sympy as sp
import mpmath as mp

p=(math.sqrt(5)-1)/2;r=p*p;a=math.sqrt(p);contrast=p-r
v=np.array([a,p]);G=np.array([[a,-p],[p,a]])
def cnot(control,target,n=3):
    M=np.zeros((2**n,2**n))
    for j in range(2**n):
        bits=[(j>>(n-1-i))&1 for i in range(n)]
        if bits[control]:bits[target]^=1
        out=sum(b<<(n-1-i) for i,b in enumerate(bits));M[out,j]=1
    return M
I=np.eye(2)
W=cnot(1,2)@np.kron(np.kron(I,I),G)@cnot(1,2)@cnot(0,1)@np.kron(I,np.kron(v,v).reshape(4,1))
# Eight-dimensional output ordered P,H,A; true NC1 reports 0,10,11.
Pi0=np.diag([1 if ((i>>1)&1)==0 else 0 for i in range(8)])
Pi10=np.diag([1 if ((i>>1)&1)==1 and (i&1)==0 else 0 for i in range(8)])
Pi11=np.diag([1 if ((i>>1)&1)==1 and (i&1)==1 else 0 for i in range(8)])
W0,W1,Wdark=[z@W for z in (Pi0,Pi10,Pi11)]
E0,E1,Edark=[z.T@z for z in (W0,W1,Wdark)]
assert np.allclose(E0,np.diag([p,r]),atol=1e-14)
assert np.allclose(E1,np.diag([r,p]),atol=1e-14)
assert np.max(np.abs(Edark))<1e-28
assert np.allclose(W.T@W,np.eye(2),atol=1e-14)
assert abs(contrast-p**3)<1e-14
# 50 arbitrary pure, potentially entangled P/oldRIGHT states.
rng=np.random.default_rng(88433);maxerr=0.
for _ in range(50):
    vec=rng.normal(size=6)+1j*rng.normal(size=6);vec/=np.linalg.norm(vec)
    actual=np.vdot(np.kron(W1,np.eye(3))@vec,np.kron(W1,np.eye(3))@vec).real
    expected=np.vdot(vec,np.kron(E1,np.eye(3))@vec).real
    maxerr=max(maxerr,abs(actual-expected))
assert maxerr<1e-13
# Full recorded output, original P/H/tail retained; pure input -> CQ entropy h(q).
ell=math.log(1/p)
def h(x):return -x*math.log(x)-(1-x)*math.log(1-x)
def row(t):
    psi=np.array([math.sqrt(1-t),math.sqrt(t)])
    a0=W0@psi;a1=W1@psi
    q=np.vdot(a1,a1).real;q0=np.vdot(a0,a0).real
    assert abs(q-(r+contrast*t))<1e-13 and abs(q+q0-1)<1e-13
    cq=np.zeros((16,16));cq[:8,:8]=np.outer(a0,a0);cq[8:,8:]=np.outer(a1,a1)
    ev=np.linalg.eigvalsh(cq);ev=ev[ev>1e-12]
    assert np.allclose(sorted(ev),sorted([q,1-q]),atol=1e-13)
    entropy=-sum(x*math.log(x) for x in ev)
    assert abs(entropy-h(q))<1e-13
    return 1+q-entropy/ell
for t in (.1,.37,.5,.83,.9):row(t)
eps=1e-5;slope=(row(.5+eps)-row(.5-eps))/(2*eps)
assert abs(slope-contrast)<1e-9
# Independent control programmes generate product binary descriptor reports.
for bits in itertools.product((0,1),repeat=4):
    tt=[.2,.4,.6,.8];q=[r+contrast*x for x in tt]
    # Here the 16-outcome product is evaluated by each exact instrument effect.
    probs=[]
    for t,bit in zip(tt,bits):
        psi=np.array([math.sqrt(1-t),math.sqrt(t)])
        probs.append(float(psi@(E1 if bit else E0)@psi))
    assert abs(math.prod(probs)-math.prod(qi if bit else 1-qi for qi,bit in zip(q,bits)))<1e-13
# Existing two-copy matter Q and field tangent geometry at s=t=1/2.
s,t=sp.symbols('s t');B=lambda x:1-2*x+2*x*x
Q=-((B(s)-s*s)*B(t)+t*t*B(s))
assert Q.subs({s:sp.Rational(1,2),t:sp.Rational(1,2)})==-sp.Rational(1,4)
assert sp.diff(Q,s).subs({s:sp.Rational(1,2),t:sp.Rational(1,2)})==sp.Rational(1,2)
assert sp.diff(Q,t).subs({s:sp.Rational(1,2),t:sp.Rational(1,2)})==-sp.Rational(1,2)
coords=list(itertools.product(range(4),repeat=4));A=p*math.sin(712*math.asin(p))
def field(u,v):
    return A*np.array([[math.cos(math.pi/2*(y[1]+u*y[0]+v*y[2])),
                        math.sin(math.pi/2*(y[1]+u*y[0]+v*y[2]))] for y in coords])
f00,f10,f01,f11=[field(u,v) for u,v in ((0,0),(1,0),(0,1),(1,1))]
Js=.5*(f10-f00)+.5*(f11-f01);Jt=.5*(f01-f00)+.5*(f11-f10)
J=np.stack([Js.reshape(-1),Jt.reshape(-1)],axis=1)/16
assert np.allclose(J.T@J,A*A*np.eye(2),atol=1e-14)
# Math resource: 16 independent pure program inputs for each of two legs.
assert abs(2*math.sqrt(16)/contrast-8/contrast)<1e-13
astar=.914389183500843
assert A/math.sqrt(astar)<p
mp.mp.dps=100;pp=(mp.sqrt(5)-1)/2
ready=(1-pp**40)*(1-pp**384)**32
print(json.dumps({'status':'PASS','contrast_exact':'p^3','contrast':contrast,
 'K0_effect_diag':['p','p^2'],'K1_effect_diag':['p^2','p'],
 'actual_two_fresh_births_CX_G_NC1_per_descriptor':{'births':2,'CX':3,'G':1,'NC1':1},
 'dark_11':True,'max_entangled_RIGHT_error':maxerr,
 'center_q_s_q_t':[.5,.5],'two_copy_Q_center':'-1/4',
 'two_copy_Q_derivatives_s_t':['1/2','-1/2'],
 'input_t_derivatives_Q':['p^3/2','-p^3/2'],
 'center_field_gram_over_A_squared':[[1,0],[0,1]],
 'math_program_32_input_lift_norm_over_q':8/contrast,
 'math_program_32_input_lift_norm_over_transformed_field':8/(contrast*A),
 'math_program_32_input_lift_norm_over_original_field':8*math.sqrt(astar)/(contrast*A),
 'observed_CQ_code_minus_information_32':32*row(.5),
 'observed_CQ_code_minus_information_common_t_slope_16':16*contrast,
 'center_plus32_conditional_success':mp.nstr(ready,30),
 'max_orig_matter_amplitude':A/math.sqrt(astar),'original_strict_bound_p':p,
 'continuous_program_preparation_and_variations_physically_admitted':False,
 'geometry_j_all42_Book03_source_and_physical_lift_established':False,
 'same_center_as_certified_42_root':False,'GR_closed':False},indent=2))
