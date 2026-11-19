#!/usr/bin/env python3
"""Exact phase-carrier descent controls; no native-admission assertion."""
import hashlib
import json
from pathlib import Path
import sympy as S

checks=[]
def zero(name,v):
    vals=list(v) if isinstance(v,S.MatrixBase) else [v]
    if any(S.simplify(S.cancel(S.expand(t)))!=0 for t in vals):
        raise RuntimeError(name)
    checks.append(name)
def need(name,flag):
    if not flag:
        raise RuntimeError(name)
    checks.append(name)

x,y=S.symbols('x y',real=True)
ph=S.symbols('p1:5',real=True)
w=S.Matrix([S.Rational(1,4)+x,S.Rational(1,4)+y,
            S.Rational(1,4)-x-y,S.Rational(1,4)])
J=w.jacobian((x,y))
beta=S.Matrix([y,x*x])
Pi=J.T*S.Matrix(ph)-beta
coords=(x,y,*ph)
theta=S.Matrix([beta[0],beta[1],*w])
Om=S.Matrix(6,6,lambda a,b:S.diff(theta[b],coords[a])-S.diff(theta[a],coords[b]))
canonical=S.zeros(6)
for a in range(2):
    for j,q in enumerate(coords):
        canonical[a,j]+=S.diff(Pi[a],q)
        canonical[j,a]-=S.diff(Pi[a],q)
zero('whole_phase_form_including_nonconstant_beta',Om-canonical)
potential=(w.T*S.Matrix(ph))[0]
gradpot=S.Matrix([S.diff(potential,q) for q in coords])
zero('exact_boundary_one_form_identity',theta-gradpot+S.Matrix([*Pi,0,0,0,0]))
need('full_column_rank',J.rank()==2)
need('canonical_rank_twice_probability_rank',Om.rank()==4)
for i,k in enumerate(J.T.nullspace()):
    zero('full_kernel_'+str(i),Om*S.Matrix([0,0,*k]))

# Complete-simplex positive escape: every edge lies in im J.
Jcomplete=S.Matrix([[1,0],[0,1],[-1,-1]])
Projcomplete=Jcomplete*(Jcomplete.T*Jcomplete).inv()*Jcomplete.T
for b in range(3):
    for c in range(b+1,3):
        freq=S.eye(3)[:,c]-S.eye(3)[:,b]
        zero('complete_simplex_edge_'+str(b)+str(c),(S.eye(3)-Projcomplete)*freq)

# A structured lower-rank positive example and a false rank-only inference.
Jgood=S.Matrix([1,-1,0])
Jbad=S.Matrix([1,2,-3])
f=S.Matrix([-1,1,0])
Jgp=(Jgood.T*Jgood).inv()*Jgood.T
Jbp=(Jbad.T*Jbad).inv()*Jbad.T
zero('positive_selected_edge_descends',Jgood*Jgp*f-f)
zero('positive_frequency_coordinate',Jgp*f+S.Matrix([1]))
PV=S.eye(3)-Jbad*Jbp
for b in range(3):
    for c in range(b+1,3):
        ff=S.eye(3)[:,c]-S.eye(3)[:,b]
        need('bad_reader_no_edge_'+str(b)+str(c),PV*ff!=S.zeros(3,1))
k=S.Matrix([2,-1,0])
zero('bad_reader_genuine_vertical_direction',Jbad.T*k)
phi1,phi2,phi3=S.symbols('phi1 phi2 phi3',real=True)
hh=S.Rational(2,3)*S.cos(phi2-phi1)
dv=sum(ki*S.diff(hh,q) for ki,q in zip(k,(phi1,phi2,phi3)))
zero('nonzero_vertical_reaction_at_phase',dv.subs({phi1:0,phi2:S.pi/2})-2)
dist2=(f.T*PV*f)[0]
zero('exact_bad_edge_distance_squared',dist2-S.Rational(27,14))
rms2=2*S.Rational(1,9)*dist2
zero('exact_rms_vertical_source',rms2-S.Rational(3,7))

# Decoder reaction cannot alter a vertical derivative with dx=0.
c1,c2=S.symbols('c1 c2',real=True)
vertical=S.Matrix([0,0,*J.T.nullspace()[0]])
reaction=S.Matrix([c1,c2,0,0,0,0])
zero('decoder_chain_reaction_zero_on_vertical',(reaction.T*vertical)[0])

# Fixed record projector / coadjoint-flow sign, including Hermitian matrix.
u=S.Matrix([1,S.exp(S.I*phi2)])/S.sqrt(2)
rho=u*u.conjugate().T
E=S.diag(1,0)
H=S.Matrix([[0,1],[1,0]])
expect=(u.conjugate().T*H*u)[0]
# phi1 variation at zero is opposite to varying phi2.
velocity=-S.I*S.trace(rho*(E*H-H*E))
zero('probability_velocity_equals_phase_derivative',velocity+S.diff(expect,phi2))

# Exact Taylor jets illustrating the admitted limit escape, not a chosen
# native frequency or gain law. General bounds are analytic in the proof.
eps,mom=S.symbols('eps mom',real=True,nonzero=True)
K=(1-S.cos(eps*mom))/eps**2
zero('cosine_limit_value',S.limit(K,eps,0)-mom*mom/2)
zero('cosine_limit_first_source',S.limit(S.diff(K,mom),eps,0)-mom)
zero('cosine_limit_source_derivative',S.limit(S.diff(K,mom,2),eps,0)-1)
zero('finite_frequency_fourth_jet_nonzero',S.diff(K,mom,4).subs(mom,0)+eps**2)

print(json.dumps({
 'status':'PASS_EXACT_PHASE_DESCENT_CONTROLS',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'control_count':len(checks),'checks':checks,
 'structural_bad_reader_J':['1','2','-3'],
 'bad_edge_distance_squared':'27/14',
 'vertical_derivative_at_test_phase':'2',
 'rms_vertical_source_squared':'3/7',
 'complete_simplex_positive_escape':True,
 'selected_lower_rank_edge_positive_escape':True,
 'decoder_reaction_preserves_vertical_obstruction':True,
 'scope':'Exact phase-carrier mathematics consuming new 7cv846-850; no physical phase admission, selected native Hamiltonian, HDA or GR closure.'
},indent=2,sort_keys=True))
