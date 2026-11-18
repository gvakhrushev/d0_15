#!/usr/bin/env python3
"""Exact finite native phase witness, not a Book03 admissibility theorem."""
import importlib.util, json, sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('native_execution', root/'native_execution.py')
nt = importlib.util.module_from_spec(spec); sys.modules[spec.name] = nt; spec.loader.exec_module(nt)
p, a, F, G, gate = nt.P, nt.A, nt.GOLDEN_FIELD, nt.G_LOCAL, nt.Gate
v = s.Matrix([a,p]); I = s.eye; Z = s.diag(1,-1)
def eq(x,y): return F.from_sympy(s.expand(x-y)) == F.zero
def meq(x,y): return x.shape == y.shape and all(eq(z,0) for z in x-y)
checks = []
def need(condition, name):
 if not condition: raise AssertionError(name)
 checks.append(name)
def cx(i,j): return gate('CX',(i,j))
def swap(i,j): return (cx(i,j),cx(j,i),cx(i,j))
src = gate('SourceI',(0,1,2))
twist = swap(0,3)+(src,src)+swap(0,3)
pad = (cx(0,3),cx(0,3))*4
core = (cx(0,3),src,src,cx(3,4),gate('G',(4,)),cx(3,4))
def ex(word,n=6,old=(5,)):
 return nt.Execution(n,(),old,word,nt.G_CX_SOURCE_I,0,(1,2))
def matrix(word,n=6,old=(5,)):
 return nt.word_matrix(ex(word,n,old),max_qubits=n,max_expanded_stages=40)
need(len(twist)==len(pad)==8, 'equal paid eight-gate prefixes')
need(meq(matrix(twist,4,()),s.kronecker_product(I(8),Z)), 'twist is exact Z on pointer and identity on every source/spin column')
need(meq(matrix(pad,4,()),I(16)), 'padding is identity on all columns')
U, U2 = matrix(pad+core), matrix(twist+core)
J = s.kronecker_product(v,I(4),v,v,I(2))
Pr = s.kronecker_product(I(8),s.diag(0,1),I(4))
bad = s.kronecker_product(I(8),s.diag(0,1),s.diag(0,1),I(2))
Pj = s.kronecker_product(v*v.T,I(32))
effect = lambda U,P: J.T*U.T*P*U*J
q = (1-p**6)/2
for name, Ux in [('original',U),('twisted',U2)]:
 need(meq(effect(Ux,Pr),q*I(8)),name+' original marked report')
 need(meq(effect(Ux,bad),s.zeros(8)),name+' invalid report exactly zero')
 need(meq(effect(Ux,I(64)),I(8)),name+' isometric on protected inputs')
gap=2*a*p*(1-p**6)
need(meq(effect(U2,Pj)-effect(U,Pj),gap*I(8)), 'subsequent live-port P_v separates after ignoring mark')
# Equality of the classical r,t label probabilities. It does not imply that
# coherent r,t off-diagonal entries agree, or that every future reader agrees.
for i in range(4):
 unit=s.zeros(4); unit[i,i]=1
 A=s.kronecker_product(I(8),unit,I(2))
 need(meq(effect(U,A),effect(U2,A)),f'rt label {i}')
# Supported inverse G on live source port, as an all-column macro.
inv=(src,src,gate('G',(0,)),src,src)
need(meq(matrix(inv,3,()),s.kronecker_product(G.T,I(4))), 'five-gate inverse G on source and arbitrary Spin')
# A born flag targeted by CX has effect diag(p²,p) for flag outcome 1.
X=s.Matrix([[0,1],[1,0]])
flag_effect=s.diag(p**2,p)
need(meq(flag_effect,p**2*I(2)+p**3*s.diag(0,1)), 'paid born flag effect')
need(meq(G*flag_effect*G.T,p**2*I(2)+p**3*(I(2)-v*v.T)), 'inverse-G then flag implements live-state contrast')
need(meq(p**3*(effect(U2,Pj)-effect(U,Pj)),2*a*p**4*(1-p**6)*I(8)), 'paid flag difference')
need(eq(2*a*p**4*(1-p**6),8*a*p**7), 'closed exact positive gap')
# Actual E0 tail, fresh v, flag 1 never yields tail 1. It uses three gates.
C=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
E0=C*s.kronecker_product(I(2),G)*C
need(meq(E0*s.kronecker_product(s.Matrix([0,1]),v),s.Matrix([0,0,1,0])), 'actual fine tail flag1 has no invalid tail')
need(eq(q,2*p**3),'closed mark probability')
# Conditional two-positive-multiplier ansatz. The equation is stated with
# symbolic c; c != 0, positive x and normalized probabilities are hypotheses.
x, c = s.symbols('x c', real=True)
u,d=(a+p)/2,(a-p)/2
R=2*u**2
N=R*x**2+(1-R)
numerator=u**2*x**2+d**2-2*u*d*x*c
target=s.Rational(1,2)-2*u*d*c
def polyzero(expr, *variables):
 return all(eq(coefficient,0) for coefficient in s.Poly(s.expand(expr),*variables).coeffs())
need(polyzero(numerator-target*N-2*u*d*c*(N-x),x,c), 'conditional mark equation reduces to N=x')
need(polyzero(N-x-R*(x-1)*(x-(1-R)/R),x), 'two positive ratio roots factor exactly')
need(eq((1-R)/R,d**2/u**2),'second ratio is phase-twist root')
need(eq(u*d,p**3/4),'coherent interference coefficient')
# At ONE original splitter, native amplitudes (sqrt(p),p) have Born law
# (p,p²). A different hypothesis reads (p,p²) themselves as amplitudes.
naive0=p**2/(p**2+p**4); naive1=p**4/(p**2+p**4)
need(eq(naive0/naive1,1/p**2),'hypothetical p,p² amplitude odds')
need(eq(p/p**2,1/p),'original G born odds')
need(not eq(naive0,p),'no common normalization fixes naive amplitudes')
need(eq((a/p)**2,p/p**2),'native amplitude ratio squares to native probability ratio')
assert float(s.N(gap))>0
print(json.dumps({'status':'PASS_EXACT','check_count':len(checks),'checks':checks,
 'fixture':{'mark_q':float(s.N(q,16)),'live_projector_gap':float(s.N(gap,16)),
 'born_flag_gap':float(s.N(8*a*p**7,16)), 'original_and_twisted_primitives':14,
 'extra_reader_primitives':9,'extra_reader_births':2,
 'original_splitter_born':[float(s.N(p,16)),float(s.N(p**2,16))],
 'hypothetical_pp2_as_amplitudes_born':[float(s.N(naive0,16)),float(s.N(naive1,16))]},
 'scope':'finite native source-I fixture, not general H1 admissibility, Book03 price law or full source',
 'physical_cost_info_binding_proved':False,'GR_closed':False},indent=2))
