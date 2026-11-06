#!/usr/bin/env python3
"""Exact all-nonblank off-copy AF frame and its independent first sources.

Run from repository root. Specified paired-port calls are not an assertion
of physical AF admission or binary-wire Execution/1 membership.
"""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as s

ROOT = Path.cwd()
PRIMARY = ROOT / '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
FRAME_PIN = 'b96babe4bcbcf3ce14d601e4079736e244389a3db04bf3ae880d0aefd85871ba'
AF_PIN = '9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee'
NATIVE_PIN = '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
PROOF_PIN = '1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254'
checks = []

def require(ok, label):
    if not bool(ok):
        raise RuntimeError(label)
    checks.append(label)

def load(name, rel, pin):
    path = ROOT / rel
    require(hashlib.sha256(path.read_bytes()).hexdigest() == pin, 'input ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

AF = load('offcopy_owned_af', '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py', AF_PIN)
N = load('offcopy_owned_native', '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py', NATIVE_PIN)
proof = ROOT / '02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md'
require(hashlib.sha256(proof.read_bytes()).hexdigest() == PROOF_PIN, 'incoming operator descent proof')
a, p = AF.a, AF.p
embedded = PRIMARY.read_text().split('<!-- BEGIN 7dg GOLDEN AF FRAME CHECKER -->\n```python\n')[1].split('```\n<!-- END 7dg GOLDEN AF FRAME CHECKER -->')[0]
require(hashlib.sha256(embedded.encode()).hexdigest() == FRAME_PIN, 'owned Golden tree code')
needed = {'mat', 'paths', 'pairs', 'rotation', 'product'}
nodes = [x for x in ast.parse(embedded).body if isinstance(x, ast.FunctionDef) and x.name in needed]
require({x.name for x in nodes} == needed, 'reuse existing tree functions only')
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<owned Golden tree>', 'exec'), globals())

def equal(A, B, label):
    require(AF.zero(A-B), label)

def layout(n, depth, work):
    sizes, fine = AF.counts(n), AF.counts(n+depth)
    segments = AF.segments(*sizes, depth)
    old = [(j,r,c) for j,d in enumerate(sizes) for r in range(d) for c in range(d)]
    coords = [(v,r,c) for v,d in enumerate(fine) for r in range(d) for c in range(d)]
    index = {x:i for i,x in enumerate(coords)}
    addresses = {(j,path):(v,off) for v,block in enumerate(segments) for j,path,off in block}
    def diagonal(j, path, r, c):
        v, off = addresses[j,path]
        return index[v,off+r,off+c]
    offpairs = {}
    for j in (0,1):
        offpairs[j] = [(v,left,right) for v,block in enumerate(segments)
                       for kind,leftpath,left in block if kind == j
                       for kind2,rightpath,right in block if kind2 == j and leftpath != rightpath]
        if len(offpairs[j]) < work-1:
            raise ValueError('INSUFFICIENT_OFFCOPY_MULTIPLICITY')
    d, D = len(old), len(coords)
    E = s.MutableSparseMatrix(D, work*d, {})
    J = s.MutableSparseMatrix(D, d, {})
    diagrows = set()
    for col,(j,r,c) in enumerate(old):
        E[diagonal(j, paths(j,depth)[0], r,c), col] = 1
        for path in paths(j,depth):
            v, off = addresses[j,path]
            row = diagonal(j,path,r,c)
            diagrows.add(row)
            J[row,col] = AF.root_weight(depth+v-j)
        for label,(v,left,right) in enumerate(offpairs[j][:work-1],1):
            E[index[v,left+r,right+c], label*d+col] = 1
    ops = []
    for j in (0,1):
        for left,right in pairs(j,depth):
            ops.append({'type':j, 'left':left, 'right':right,
                        'rows':[(diagonal(j,left,r,c),diagonal(j,right,r,c))
                                for r in range(sizes[j]) for c in range(sizes[j])]})
    D0 = s.diag(*[s.Integer(i in diagrows) for i in range(D)])
    return {'old':old, 'fine':coords, 'E':s.SparseMatrix(E), 'J':mat(J),
            'diag':s.SparseMatrix(D0), 'ops':ops,
            'capacities':[len(offpairs[j]) for j in (0,1)],
            'selected':[[[v,l,r] for v,l,r in offpairs[j][:work-1]] for j in (0,1)]}

f = layout(0,4,4)
E,J,D0,ops = f['E'],f['J'],f['diag'],f['ops']
d,D = J.cols,J.rows
B = product([rotation(D,op['rows']) for op in ops],D)
equal(E.T*E,s.eye(4*d),'all four coordinate frames orthonormal')
equal(B*E[:,:d],J,'actual four-level canonical inclusion')
equal(J.T*J,s.eye(d),'canonical inclusion isometry')
equal(B.T*B,s.eye(D),'all-column Golden frame orthogonal')
equal(D0*B,B*D0,'frame preserves diagonal-copy subspace')
equal(B*(s.eye(D)-D0),s.eye(D)-D0,'frame fixes whole off-copy complement')
equal(D0*E[:,d:],s.zeros(D,3*d),'EVERY nonblank frame is off-copy')
equal(B*E[:,d:],E[:,d:],'every nonblank frame remains fixed')
require((d,D,len(ops),f['capacities']) == (2,89,11,[26,8]),'actual depth4 dimensions and capacity')
try:
    layout(0,3,4)
except ValueError as exc:
    require(str(exc) == 'INSUFFICIENT_OFFCOPY_MULTIPLICITY','old depth3 insufficient for all three nonblank labels')
else:
    raise RuntimeError('old depth3 should not support this changed frame')

# Execute the same existing seven-stage reflected word, now in the changed
# four-level all-nonblank off-copy frame. All original Spin columns stay.
g=N.Gate('G',(0,)); cx=N.Gate('CX',(0,1)); si=N.Gate('SourceI',(0,2,3))
gates=(g,cx,si,si,g,si,si)
word=N.Execution(4,(0,1),(),gates,N.G_CX_SOURCE_I,0,(2,3))
N.validate_execution(word,max_qubits=4,max_expanded_stages=7)
def symbolic(A):
    return mat(A.xreplace({N.A:a}).xreplace({s.sqrt(5):2*p+1}))
logical=[symbolic(N.gate_matrix(word,x)) for x in gates]
W=product(logical,16)
TE=s.MutableSparseMatrix(4*D,16*d,{})
for work in range(4):
    for spin in range(4):
        for old in range(d):
            for row in range(D):
                if E[row,work*d+old]:TE[4*row+spin,(4*work+spin)*d+old]=1
TE=s.SparseMatrix(TE)
BS=s.kronecker_product(B,s.eye(4));T=mat(BS*TE)
I=s.SparseMatrix(s.eye(4*D)); DD=s.kronecker_product(D0,s.eye(4))
RE=mat(TE*TE.T);RT=mat(T*T.T)
input_map=T[:,:4*d];P=mat(input_map*input_map.T)
equal(input_map*input_map.T,s.kronecker_product(J*J.T,s.eye(4)),'unchanged canonical input cut')
branch_g=[];branch_s=[]
for op in ops:
    G=s.kronecker_product(rotation(D,op['rows']),s.eye(4))
    SI=s.MutableSparseMatrix(I)
    for first,second in op['rows']:
        for r in range(4):
            for c in range(4):SI[4*second+r,4*second+c]=N.L_I[r,c]
    branch_g.append(mat(G));branch_s.append(s.SparseMatrix(SI))
prefix=[];prefix_names=[]
for G,SI in reversed(list(zip(branch_g,branch_s))):
    prefix.extend([SI,SI,G,SI,SI]);prefix_names+=['SourceI','SourceI','G','SourceI','SourceI']
equal(product(prefix,4*D),BS.T,'all55 literal forward decoding calls')
middle=[mat(TE*s.kronecker_product(x,s.eye(d))*TE.T+I-RE) for x in logical]
schedule=prefix+middle+branch_g
names=prefix_names+[x.op for x in gates]+['G']*len(ops)
U=product(schedule,4*D)
equal(U,T*s.kronecker_product(W,s.eye(d))*T.T+I-RT,'all73 actual calls on every356 columns')
equal(U.T,U,'whole reflected endpoint')
equal(U*U,I,'whole endpoint squares to identity')
equal(P*U*P,p*P,'same positive actual corner')
equal(P*U.T*(I-P)*U*P,p*P,'same complete feedback')
equal(DD*U*DD,p*P+DD-P,'universal diagonal compression identity')
equal(DD*U*P,p*P,'all leakage is outside frame support')
equal(P*U*DD,p*P,'inverse-side compression identity')
require((s.trace(P),s.trace(I-RT),AF.red(s.trace(U)))==(8,324,340),'true rank8 complement324 spectrum348+8')
require(len(schedule)==73 and Counter(names)=={'G':24,'CX':1,'SourceI':48},'true73-call inventory')

# Every frame call has exactly the required support, including each
# independent SourceI occurrence. This, plus the three compression
# identities above, proves the statement for ALL skew generators on
# each such support, rather than sampling only one fault per stage.
frame_calls=prefix+branch_g
for i,G in enumerate(frame_calls):
    equal(DD*(G-I),G-I,'frame-call diagonal support '+str(i))
    equal((G-I)*DD,G-I,'frame-call diagonal input support '+str(i))

# Operator first-source controls. A nontrivial diagonal-supported Spin
# rotation has a NONZERO compressed skew insertion, but zero Hermitian
# source on either independently varied temporal half.
firstrow=ops[0]['rows'][0][0]
H=s.MutableSparseMatrix(4*D,4*D,{})
H[4*firstrow,4*firstrow+1]=1;H[4*firstrow+1,4*firstrow]=-1
H=s.SparseMatrix(H)
plus=mat(input_map.T*H*U*input_map)
minus=mat(-input_map.T*U*H*input_map)
require(not AF.zero(plus),'diagonal frame insertion itself is not zero')
equal(plus+plus.T,s.zeros(4*d),'independent encoder Hermitian insertion zero')
equal(minus+minus.T,s.zeros(4*d),'independent decoder Hermitian insertion zero')
equal(plus,p*input_map.T*H*input_map,'exact encoder operator formula')
equal(minus,-p*input_map.T*H*input_map,'exact decoder operator formula')

# Sharp support negative control, with the SAME full word and fixed J.
# A generator joining J to its real leakage breaks the diagonal guard.
leak=mat(U*input_map-p*input_map)
bad=mat(input_map*leak.T-leak*input_map.T)
equal(bad.T,-bad,'cross-support control is genuinely skew')
require(not AF.zero(DD*bad-bad),'cross-support control violates frame guard')
badX=mat(input_map.T*bad*U*input_map)
equal(badX,(1-p*p)*s.eye(4*d),'cross-support encoder first source is nonzero')
z=s.symbols('z',positive=True)
bad_feedback=-2*z*p*(1-p*p)*8/(1-z+z*p*p)
require(not AF.zero(s.together(bad_feedback).as_numer_denom()[0]),'wrong larger support cannot inherit zero source')

# An arbitrary nonnormal retained past does not turn a skew insertion
# into a return-price source. Differentiate the actual two-by-two
# determinant, not a uniform-trace surrogate.
t=s.symbols('t',real=True)
K=s.Matrix([[s.Rational(43,75),s.Rational(4,25)],[s.Rational(8,25),s.Rational(19,50)]])
rr=s.Rational(3,5); zz=s.Rational(1,7)
A=s.Matrix([[0,2],[-2,0]])
C=(rr*s.eye(2)+t*rr*A)*K
price_arg=(1-zz)*s.eye(2)+zz*C.T*C
derivative=s.factor(-s.diff(price_arg.det(),t).subs(t,0)/price_arg.det().subs(t,0))
require(K.T*K != K*K.T,'retained past truly nonnormal')
require(derivative==0,'complete retained-past determinant frame derivative zero')
wrong=(rr*s.eye(2)+t*s.diag(1,-1))*K
wrongD=(1-zz)*s.eye(2)+zz*wrong.T*wrong
wrongder=s.factor(-s.diff(wrongD.det(),t).subs(t,0)/wrongD.det().subs(t,0))
require(wrongder!=0,'same past detects a non-skew operator source')

result={'status':'PASS','checks':len(checks),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs':{'af':AF_PIN,'native':NATIVE_PIN,'tree':FRAME_PIN,'incoming_proof':PROOF_PIN},
        'frame':{'old_level':0,'depth':4,'work_labels':4,'old_dimension':d,'af_dimension':D,
                 'full_spin_dimension':4*D,'offcopy_capacities':f['capacities'],'selected_offcopy_addresses':f['selected'],
                 'forward_rotations':len(ops),'decode_calls':len(prefix),'independent_frame_calls':len(frame_calls)},
        'execution':{'total_calls':len(schedule),'inventory':dict(sorted(Counter(names).items())),
                     'protected_rank':8,'identity_complement':324,'positive_negative_spectrum':[348,8],
                     'corner':'p I8','feedback':'p P'},
        'source':{'encoder':'c P H_plus P, skew','decoder':'-c P H_minus P, skew',
                  'frame_feedback_first_source':'zero as an operator on actual protected input',
                  'nonnormal_past_derivative':str(derivative),'nonnormal_non_skew_control':str(wrongder),
                  'cross_support_control':'-16 z p (1-p^2)/(1-z+z p^2)',
                  'heat':'not claimed zero; retain full true-clock bound'},
        'scope':'Exact AF placement and guarded first-source extension; not physical primitive admission, all X_N, exact finite stationary word or GR closure.',
        'labels':checks}
print(json.dumps(result,indent=2,sort_keys=True))
