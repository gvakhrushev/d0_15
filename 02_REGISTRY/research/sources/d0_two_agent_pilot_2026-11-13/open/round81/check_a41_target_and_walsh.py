#!/usr/bin/env python3
"""Exact small all-column A41 checks; never requests a production vector."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A=D/'round41';sys.path.insert(0,str(A))
import exact_target as e
import sam_only_compiler as c
planfile=A/'SAM_ONLY_COMPILER_PLAN.json';plan=json.loads(planfile.read_text())
assert plan['status']=='MATHEMATICALLY_CONSTRUCTIVE_SAM_ONLY_FULL_COLUMN_COMPILER'
assert plan['production_target_table_or_words_evaluated'] is False
assert all(sha256(Path(f).read_bytes()).hexdigest()==h for f,h in plan['source_sha256'].items())
# The production guard must not purport to create a 2^2688 Python sequence.
for f in (e.production_target,c.production_word):
    try:f()
    except NotImplementedError:pass
    else:raise AssertionError('production guard absent')
try:len(range(1<<100))
except OverflowError:pass
else:raise AssertionError('unexpected platform sequence semantics')

# Q(a): a^4+a^2−1=0; exact G satisfies c²+s²=1.
a=e.A;p=e.SIN
assert a**4+a**2==e.Q4(1) and a*a+p*p==e.Q4(1)
c2,s2=e.rotation_power(2)
assert c2==2*p-e.Q4(1) and s2==2*a*p
# Exact actual-word compression on both SAM basis controls. No scalar oracle.
def W():
    yield {'op':'G','wires':[1]};yield {'op':'CX','wires':[0,1]}
    yield {'op':'G','wires':[1]};yield {'op':'CX','wires':[0,1]}
assert e.compressed_entry(2,(0,),0,W)==2*p-e.Q4(1)
assert e.compressed_entry(2,(0,),1,W)==e.Q4(1)

# A positive 4D nontrivial case with chi, xi exact rational, d>1/2, and
# h=(chi+xi)/||chi+xi||. Convert Expr to exact symbolic algebraic values.
alpha=s.sqrt((s.sqrt(5)-1)/2)
def to_sym(t,cache=None):
    if cache is None:cache={}
    if t in cache:return cache[t]
    if t.op=='field':v=sum(s.Rational(x.numerator,x.denominator)*alpha**i for i,x in enumerate(t.args[0].v))
    else:
        xs=[to_sym(x,cache) for x in t.args]
        v={'add':lambda x,y:x+y,'neg':lambda x:-x,'mul':lambda x,y:x*y,
           'div':lambda x,y:x/y,'sqrt':s.sqrt}[t.op](*xs)
    cache[t]=v;return v
chi=s.Matrix([s.Rational(1,2)]*4)
xi=s.Matrix([s.Rational(15,26)]*3+[s.Rational(1,26)])
h=(chi+xi)/s.sqrt((chi+xi).dot(chi+xi));d=(chi.T*xi)[0]
assert d==s.Rational(23,26) and all(x>0 for x in xi)
chiex=[e.expr(F(1,2)) for _ in range(4)]
hden=e.root(13);hexpr=[e.expr(2)/hden]*3+[e.expr(1)/hden]
assert all(s.simplify(to_sym(x)-y)==0 for x,y in zip(hexpr,h))
star=s.eye(4)
for j,ce,se in c.target_stars(chiex,hexpr):
    cc,ss=to_sym(ce),to_sym(se)
    R=s.eye(4);R[0,0]=cc;R[0,j]=-ss;R[j,0]=ss;R[j,j]=cc
    star=R*star
star=s.simplify(star)
Rchi=s.eye(4)-2*chi*chi.T;Rh=s.eye(4)-2*h*h.T
K=chi*xi.T-xi*chi.T
A37=s.eye(4)+K+K*K/(1+d)
assert s.simplify(star-Rchi*Rh)==s.zeros(4)
assert s.simplify(star-A37)==s.zeros(4)
assert s.simplify(star*xi-chi)==s.zeros(4,1)
assert s.simplify(star.T*star)==s.eye(4) and s.simplify(star.det())==1

# Full actual star-block all-column semantics at m=2..4 using an exact
# rational sample rotation, same word order and no extra wires. A target
# plane angle is L*k times the elementary G angle by zero-pattern Walsh.
def apply_gates(blocks,bits,k):
    D=1<<bits;Fmat=[[F(i==j) for j in range(D)] for i in range(D)]
    elementary=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
    ops=[]
    for gate in blocks:
        if gate['op']=='repeat':
            assert int(gate['count'],16)==k and gate['child']['op']=='G'
            ops += [gate['child']]*k
        else:ops.append(gate)
    for gate in ops:
        op=gate['op'];w=gate['wires'];assert op in ('G','CX') and all(q in range(bits) for q in w)
        if op=='CX':
            x,y=w; perm=[i^((1<<y) if i>>x&1 else 0) for i in range(D)]
            Fmat=[Fmat[i] for i in perm]
        else:
            q=w[0]
            for row in range(D):
                if row>>q&1:continue
                i,j=Fmat[row],Fmat[row|(1<<q)]
                Fmat[row]=[elementary[0][0]*u+elementary[0][1]*v for u,v in zip(i,j)]
                Fmat[row|(1<<q)]=[elementary[1][0]*u+elementary[1][1]*v for u,v in zip(i,j)]
    return Fmat,ops
for bits in (2,3,4):
    D0=1<<bits
    for j in range(1,D0):
        mat,ops=apply_gates(c.star_blocks(range(bits),j,2),bits,2)
        G=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])**(2*(1<<(bits-1)))
        want=[[F(i==k) for k in range(D0)] for i in range(D0)]
        for x,y,u,v in ((0,0,0,0),(0,j,0,1),(j,0,1,0),(j,j,1,1)):
            want[x][y]=F(int(G[u,v].p),int(G[u,v].q))
        assert mat==want,(bits,j)

# Dyadic expression domain and positivity: evaluate an actual 2-SAM target
# with strictly positive Q(a) table, checking all components and norm bounds.
table=[e.Q4(F(4,5)),e.Q4(F(3,4)),e.Q4(F(9,10)),e.Q4(F(7,8))]
ct,xt,ht,r=e.target_vectors(table,2,0,0)
ctx=e.Dyadic(384); cv=ctx.evaluate(ct); xv=ctx.evaluate(xt); hv=ctx.evaluate(ht)
assert all(z[0]>0 for z in cv+xv+hv)
for vs in (cv,xv,hv):
    total=ctx.rat(0)
    for v in vs:total=ctx.add(total,ctx.mul(v,v))
    assert total[0]<=ctx.S<=total[1]

# Counts independently derived for m=2688 and q from the strict grid.
pn,q,grid=c.uniform_grid();bits=2688;D0=1<<bits;L=1<<(bits-1);stars=4*(D0-1)
actual_bound=stars*L*F(1,2**20000)
assert actual_bound<F(1,2**14623)
CX=4*((D0-1)*(bits-1)*L+2*(bits*L-D0+1))
Gmax=stars*L*q
assert Gmax+CX<1<<25458

out={'status':'PASS_A41_SMALL_EXACT_ALL_COLUMN_AND_BOUND_FIXTURES',
     'exact_target_sha256':sha256((A/'exact_target.py').read_bytes()).hexdigest(),
     'compiler_sha256':sha256((A/'sam_only_compiler.py').read_bytes()).hexdigest(),
     'plan_sha256':sha256(planfile.read_bytes()).hexdigest(),
     'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'Q4_field_and_literal_small_actual_compression_checked':True,
     'nontrivial_4d_star_sequence_equals_full_A37_matrix':True,
     'all_small_stars_m2_to_m4_all_columns_exact':True,
     'small_dyadic_normalization_and_positive_branches_checked':True,
     'full_target_error_strict_lt':'2^-14623',
     'upper_call_count_strict_lt':'2^25458',
     'production_API_explicitly_guarded_as_not_implemented':True,
     'actual_production_target_evaluated_or_word_emitted':False,
     'full_H1_admission_or_clock_source_proved':False,'physical_C_closed':False,'GR_closed':False}
(HERE/'B81_TARGET_WALSH_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
