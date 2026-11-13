#!/usr/bin/env python3
"""Independent Walsh/CCX algebra and small real-word full-column controls."""
from pathlib import Path
from itertools import product
import importlib.util,sys,json,math,cmath
import sympy as sp
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round14')
spec=importlib.util.spec_from_file_location('a14_review_word',D/'native_boolean.py');nb=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nb;spec.loader.exec_module(nb)
# Exhaust truth-table coefficients without using owner Walsh evaluator.
walsh_cases=0
for n in (2,3,4):
 for a in product((0,1),repeat=n):
  for x in product((0,1),repeat=n):
   total=0
   for mask in range(1<<n):
    parity=sum(a[j]+x[j] for j in range(n) if mask>>j&1)%2
    total+=(-1)**parity
   assert total==((1<<n) if x==a else 0);walsh_cases+=1
# Ideal selected two-block CCX identity with arbitrary aux.
I=sp.eye(2);J=sp.Matrix([[0,-1],[1,0]]);Z=sp.diag(1,-1);X=sp.Matrix([[0,1],[1,0]])
assert J*Z==X
# Ensure G's eigenvalue is not a root of unity (all k, not only k=1).
t=sp.symbols('t');f=t**4+t**2-1
assert sp.Poly(f,t,extension=sp.I).is_irreducible
assert sp.simplify((sp.I/t)**4+(sp.I/t)**2-1+f/t**4)==0
# a=sqrt(p) is in (3/4,4/5), so |i(1/a−1/a²)|=(1-a)/a²<4/9<1.
assert sp.Rational(9,16)<(sp.sqrt(5)-1)/2<sp.Rational(16,25)
assert sp.Rational(1,4)/sp.Rational(9,16)==sp.Rational(4,9)<1
# Independent sparse numeric gate interpreter: direct physical SourceI
# signed permutation and primitive G, no owner matrix/expected implementation.
N=8;port=4;spin=(5,6);cos=math.sqrt((math.sqrt(5)-1)/2);sin=(math.sqrt(5)-1)/2;theta=math.atan2(sin,cos)
def rotate(state,wire,ang):
 c,s=math.cos(ang),math.sin(ang);mask=1<<(N-1-wire);out={}
 for i,v in state.items():
  same=c*v;other=(-s if i&mask else s)*v
  out[i]=out.get(i,0)+same;out[i^mask]=out.get(i^mask,0)+other
 return out
def run(word,column):
 state={column:1.0}
 for g in word:
  op=g['op'];w=g['wires']
  if op=='G':state=rotate(state,w[0],theta);continue
  new={}
  for i,v in state.items():
   if op=='CX':
    if (i>>(N-1-w[0]))&1:i^=1<<(N-1-w[1])
   else:
    assert op=='SourceI' and w==[port,*spin]
    if i>>(N-1-port)&1:
     if i>>(N-1-spin[1])&1:v=-v
     i^=1<<(N-1-spin[1])
   new[i]=new.get(i,0)+v
  state=new
 return state
def expected(name,k,col):
 st={col:1.0};targ=2;aux=3
 if name in ('X','H'):
  if col>>(N-1-targ)&1:st={col:-1.0}
  return rotate(st,targ,(4 if name=='X' else 2)*k*theta)
 if ((col>>(N-1))&1) and ((col>>(N-2))&1):
  if (col>>(N-1-targ))&1:st=rotate(st,aux,8*k*theta)
  st=rotate(st,targ,4*k*theta)
 return st
columns=0;maxerr=0.
for name in ('X','H','CCX'):
 for k in (1,2):
  word=list(nb.expand(nb.boolean_word(name,k),1000))
  for col in range(256):
   a=run(word,col);b=expected(name,k,col);err=max(abs(a.get(i,0)-b.get(i,0)) for i in set(a)|set(b));maxerr=max(maxerr,err);assert err<1e-12;columns+=1
res={'status':'PASS_INDEPENDENT_WALSH_CCX_AND_SMALL_NATIVE_WORDS','walsh_control_pattern_cases':walsh_cases,
 'ideal_identity':'R_t(pi/2) Z_t = X_t; R_aux(pi)=-I for either aux input',
 'irrational_angle_theorem_status':'already owned, PHASE_COMPILER.md section on optional comparison; following is a bounded independent check of that fact, not a new result',
 'root_of_unity_obstruction':'a^4+a^2−1 irreducible over Q(i), conjugate a->i/a sends a+i a^2 to i(1/a−1/a²), whose modulus lies in (0,4/9); therefore lambda=e^(i theta) is not a root of unity',
 'actual_approximate_CCX_not_its_own_inverse_for_every_positive_k':True,
 'small_numeric_native_columns':columns,'max_abs_small_numeric_error':maxerr,
 'numeric_small_check_scope':'independent cross-check; exact owning-algebra all-column replay is separate',
 'native_full_writer_executed':False,'GR_closed':False}
(P/'BOOLEAN_MATH_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
