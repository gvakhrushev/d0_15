#!/usr/bin/env python3
"""Same palette, same stage inventory: exact closed reflection comparison.

No claim of a D0-wide no-go. Tests the proposed inference from closure,
reflection-clock heat and unrestricted minimization to a selected law.
"""
from __future__ import annotations
from collections import Counter
import json
import sympy as s
import numpy as np
import mpmath as mp

checks = []
def require(value, label):
    if not bool(value):
        raise ArithmeticError(label)
    checks.append(label)

t=s.symbols('t', real=True)
minimal=t**4+t**2-1

def canon(x):
    return s.rem(s.Poly(s.expand(x),t),s.Poly(minimal,t)).as_expr()
def red(M): return M.applyfunc(canon)
def mm(A,B): return red(A*B)
def eq(A,B,label):
    require(A.shape==B.shape and red(A-B)==s.zeros(*A.shape),label)

d=8
I=s.eye(d);I4=s.eye(4);O4=s.zeros(4)
p=t**2
G=s.kronecker_product(s.Matrix([[t,-p],[p,t]]),I4)
Li=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
X=s.diag(I4,Li)
Z=mm(X,X)
P=s.diag(I4,O4);Q=I-P
for U,name in [(G,'G'),(X,'SourceI')]:eq(mm(U.T,U),I,name+' full8 orthogonal')
eq(mm(Z,G)*Z,G.T,'native XXGXX inverse')
eq(mm(mm(X,X),mm(X,X)),I,'SourceI power4')

# Words displayed in chronological order; no costless inverse primitive.
w0=['G','X','X','G','X','X','X','X']
w1=['G','X','X','X','X','G','X','X']
require(Counter(w0)==Counter(w1)==Counter({'G':2,'X':6}),'same inventory, same 8 stages')
ops={'G':G,'X':X}
def execute(word):
    prefixes=[I]
    for g in word: prefixes.append(mm(ops[g],prefixes[-1]))
    return prefixes
A0,A1=execute(w0),execute(w1)
M0,M1=A0[-1],A1[-1]
eq(M0,Z,'word0 endpoint exactly Z')
eq(M1,mm(mm(G.T,Z),G),'word1 endpoint exactly G^T Z G')
for M,name in [(M0,'0'),(M1,'1')]:
    eq(M.T,M,'endpoint '+name+' symmetric')
    eq(mm(M,M),I,'endpoint '+name+' involution')
    require(s.trace(M)==0,'endpoint '+name+' four plus four minus')
F0=mm(mm(mm(mm(P,M0),Q),M0),P)
F1=mm(mm(mm(mm(P,M1),Q),M1),P)
eq(F0,s.zeros(d),'word0 complete endpoint feedback zero')
f=canon(4*p**3)
eq(F1,red(f*P),'word1 feedback exactly 4p^3 P')

# Exact all-stage gauge intertwiner: G1 diag(G^T) G0^T.
# Q_k transports w0 stage into w1 stage, so all horizontal scene edges
# remain identity when this same stage transport is used at every vertex.
Qs=[mm(mm(A1[k],G.T),A0[k].T) for k in range(8)]
for k in range(8):
    eq(mm(mm(Qs[(k+1)%8],ops[w0[k]]),Qs[k].T),ops[w1[k]],
       'exact clock edge intertwining '+str(k))
    eq(mm(Qs[k].T,Qs[k]),I,'stage gauge orthogonal '+str(k))

# Each input's generated clock projector has an endpoint return only.
for word,prefixes,endpoint_f,label in [(w0,A0,F0,'0'),(w1,A1,F1,'1')]:
    Ps=[mm(mm(prefixes[k],P),prefixes[k].T) for k in range(8)]
    for k in range(8):
        W=ops[word[k]];Pn=Ps[(k+1)%8]
        E=mm(mm(mm(mm(Ps[k],W.T),I-Pn),W),Ps[k])
        ref=s.zeros(d) if k<7 else mm(mm(prefixes[k],endpoint_f),prefixes[k].T)
        eq(E,ref,'generated-cut stage return word'+label+' stage'+str(k))

# Full INTERNAL scene trace is evaluated by exact cycle Fourier reduction.
# The equality itself was proved by the all-column stage identities above.
mp.mp.dps=70
pmp=(mp.sqrt(5)-1)/2
pv=float(pmp);tv=float(mp.sqrt(pmp))
sub={t:tv}
Gf=np.array(G.subs(sub),dtype=float)
Xf=np.array(X,dtype=float)
Mf=[np.array(M.subs(sub),dtype=float) for M in [M0,M1]]
N=8;sr=128;beta=2*pv*pv;z=mp.mpf(2)**-20
sizes=[9,11,13];lab=np.repeat(np.arange(3),sizes)
As=(lab[:,None]!=lab[None,:]).astype(float)
deg=As.sum(1);r=1/np.sqrt(deg+2)
Bs=r[:,None]*As*r[None,:];Cs=np.diag(r*r)
require(int(As.sum()/2)==359,'actual K913 has359 edges')
require(int(359*N+33*N)==392*N,'full product edge count')
Z0=0.
for phase in [0.,np.pi]:
    for k in range(N):
        angle=(2*np.pi*k+phase)/N
        eig=np.linalg.eigvalsh(np.eye(33)-Bs-2*np.cos(angle)*Cs)
        Z0+=4*float(np.exp(-beta*eig).sum())
Z01=2*Z0+359*N*d
H=float(np.log(sr*Z01)/beta)
gap=-4*sr*mp.log1p(-z*4*pmp**3)
require(gap>0,'strict complete H+J gap')
# Positivity is symbolic: p^6+4p^3=1 and 0<p<1.
require(canon(p**6+4*p**3-1)==0,'strict positive contraction from golden identity')

# General reflection-orbit critical theorem, checked on exact 4D real cases.
# For C=PMP, F=P-C^2 and J=-logdet((1-z)I+zC^2), stationarity
# for every orthogonal-conjugacy tangent iff F^2=F.
zr=s.Rational(1,16)
P4=s.diag(1,1,0,0);I_4=s.eye(4)
reflections=[
 ('aligned',s.diag(1,-1,1,-1),True),
 ('one_max_leak',s.Matrix([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,-1]]),True),
 ('two_max_leak',s.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]),True),
 ('intermediate',s.Matrix([[s.Rational(3,5),0,s.Rational(4,5),0],[0,1,0,0],
                        [s.Rational(4,5),0,-s.Rational(3,5),0],[0,0,0,-1]]),False)
]
orbit=[]
for name,M,expected in reflections:
    require(M.T==M and M*M==I_4,'orbit fixture involution '+name)
    C=(P4*M*P4)[:2,:2]
    D=(1-zr)*s.eye(2)+zr*C*C
    grad=s.zeros(4);grad[:2,:2]=-2*zr*C*D.inv()
    critical=True
    vals=[]
    for i in range(4):
        for j in range(i+1,4):
            K=s.zeros(4);K[i,j]=1;K[j,i]=-1
            deriv=s.trace(grad*(K*M-M*K))
            vals.append(str(deriv));critical=critical and deriv==0
    F=P4*M*(I_4-P4)*M*P4
    proj=(F*F==F)
    require(critical==proj==expected,'critical iff feedback projection '+name)
    orbit.append({'name':name,'critical':critical,'feedback_idempotent':proj,'derivatives':vals})

out={
 'status':'PASS_EXACT_SAME_INVENTORY_CLOSED_SELECTION_TEST',
 'checks':len(checks),'algebra':'Q[t]/(t^4+t^2-1), t=sqrt(phi^-1)>0',
 'word_chronological_zero':''.join(w0),'word_chronological_nonzero':''.join(w1),
 'count_per_word':dict(Counter(w0)), 'full_fibre_dimension':d,'clock_length':N,
 'active_rank_without_RIGHT':4,'RIGHT_spectator':sr,
 'scene_vertices':33,'scene_edges':359,
 'H0_dimension_without_RIGHT':33*N*d,
 'H1_dimension_without_RIGHT':392*N*d,
 'extra_harmonic_count_without_RIGHT':359*N*d,
 'heat_equal_by_exact_intertwiner':True,
 'full_graded_heat_value_diagnostic':H,
 'feedback_zero':'0', 'feedback_nonzero':'4 p^3 P',
 'full_H_plus_J_difference_exact':'-512 log(1 - 2^-20 * 4 p^3)',
 'full_H_plus_J_difference_numeric':mp.nstr(gap,55),
 'orbit_critical_controls':orbit,
 'original_all42_gravity_roots_replayed':False,
 'same_mandatory_GR_task_proved':False,
 'all_D0_core_models_refuted':False,
 'unconditional_GR_closed':False,
 'scope':'Refutes automatic selection from closure+this fixed master+the cited available palette; does not forbid a justified same-task constrained GR realization.'
}
print(json.dumps(out,ensure_ascii=False,indent=2))
