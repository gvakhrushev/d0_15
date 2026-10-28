#!/usr/bin/env python3
"""Actual READY-copy/reflection recipe and its independent raw source map.

The binary middle is a native Execution/1 word. Its AF lift and the frame
are explicitly specified paired-port operations, not physical admission.
"""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as s

ROOT=Path.cwd()
PRIMARY=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
# Full pins are checked before any builder is imported.
AF_PIN='9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee'
NATIVE_PIN='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
TREE_PIN='b96babe4bcbcf3ce14d601e4079736e244389a3db04bf3ae880d0aefd85871ba'
FRAME_PIN='de29e556ac1e4fe7a4881fb5e26f7fe0287a99c85b6f2cd5c9396192a8213f88'
REGULAR_PIN='1fbef33d6a1284c2cb1c9f3db89886470ff4d18549ef4fe6a1b499b22339065f'
checks=[]
def require(ok,label):
    if not bool(ok):raise RuntimeError(label)
    checks.append(label)
def load(name,rel,pin):
    path=ROOT/rel
    require(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'input '+name)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module
AF=load('ready_compiler_af','02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py',AF_PIN)
N=load('ready_compiler_native','02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py',NATIVE_PIN)
a,p=AF.a,AF.p
source=PRIMARY.read_text()
def functions(marker,pin,names):
    code=source.split('<!-- BEGIN '+marker+' -->\n```python\n')[1].split('```\n<!-- END '+marker+' -->')[0]
    require(hashlib.sha256(code.encode()).hexdigest()==pin,'published '+marker)
    nodes=[x for x in ast.parse(code).body if isinstance(x,ast.FunctionDef) and x.name in names]
    require({x.name for x in nodes}==set(names),'requested existing builder functions '+marker)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<owned '+marker+'>','exec'),globals())
functions('7dg GOLDEN AF FRAME CHECKER',TREE_PIN,{'mat','paths','pairs','rotation','product'})
functions('7di OFFCOPY FRAME CHECKER',FRAME_PIN,{'layout'})
functions('7dj REGULAR CYCLIC SOURCE CHECKER',REGULAR_PIN,set())
def equal(A,B,label):require(AF.zero(A-B),label)
def symbolic(A):return mat(A.xreplace({N.A:a}).xreplace({s.sqrt(5):2*p+1}))
def swap(i,j):return (N.Gate('CX',(i,j)),N.Gate('CX',(j,i)),N.Gate('CX',(i,j)))

# Ordinary binary interface: port0, report1, real readiness flag2, Spin3/4.
# Its oldRIGHT spectator is then retained as a separate exact identity factor.
si=N.Gate('SourceI',(0,3,4))
def execution(word):return N.Execution(5,(0,1,2),(),tuple(word),N.G_CX_SOURCE_I,0,(3,4))
def phase(q,k):return swap(0,q)+(si,)*k+swap(0,q)
cx=N.Gate('CX',(1,2))
cz=phase(1,1)+phase(2,1)+(cx,)+phase(2,3)+(cx,)
g=(N.Gate('G',(1,)),)
ginv=N.inverse_word(execution(g),max_qubits=5,max_expanded_stages=100)
word=execution(ginv+cz+g)
N.validate_execution(word,max_qubits=5,max_expanded_stages=100)
inventory=N.inventory(word,max_qubits=5,max_expanded_stages=100)
require((len(cz),inventory.g_count,inventory.cx_count,inventory.source_i_count)==(25,2,26,9),'actual37-call binary reflection inventory')
G=symbolic(N.word_matrix(execution(g)))
Gi=symbolic(N.word_matrix(execution(ginv)))
equal(Gi,G.T,'all11 inverse stages restore helper on every column')
Q=s.diag(*[(-1 if ((i>>3)&1) and ((i>>2)&1) else 1) for i in range(32)])
CZ=symbolic(N.word_matrix(execution(cz)))
equal(CZ,Q,'all32 columns: actual parity phase is controlled Z, Spin restored')
U=symbolic(N.word_matrix(word))
equal(U,G*Q*G.T,'all37 actual middle calls equal the controlled reflection')
equal(U.T,U,'middle is an exact full-column reflection')
W=s.Matrix([[p**3,2*a*p],[2*a*p,-p**3]])
logical_true=s.kronecker_product(s.eye(2),W,s.eye(4))
idx=[[16*port+8*query+4*flag+spin for port in range(2) for query in range(2) for spin in range(4)] for flag in range(2)]
equal(U.extract(idx[0],idx[0]),s.eye(16),'exact false branch I, including all port and Spin columns')
equal(U.extract(idx[1],idx[1]),logical_true,'true branch is the existing p3 reflection')
equal(U.extract(idx[0],idx[1]),s.zeros(16),'no endpoint flag mixing')

# Literal addressed AF READY copy: one original CX per old block, choosing
# an unused diagonal path as control0 and the coordinate-zero path as control1.
f=layout(0,4,4);E,J,ops=f['E'],f['J'],f['ops'];d,D=J.cols,J.rows
B=product([rotation(D,op['rows']) for op in ops],D)
e0=E[:,:d]*E[:,:d].T;I=s.SparseMatrix(s.eye(D))
dim=8*D;ID=s.SparseMatrix(s.eye(dim));DF=s.kronecker_product(f['diag'],s.eye(8))
ready=[];ready_addresses=[]
for j in (0,1):
    zero=[r for r in range(D) if E[r,j]]
    require(len(zero)==1,'unique coordinate-zero old block '+str(j))
    zero=zero[0]
    dummy=next(r for r in range(D) if f['diag'][r,r] and r!=zero and any(r in op['rows'][0] for op in ops if op['type']==j))
    R=s.MutableSparseMatrix(ID)
    for flag in (0,1):
        for spin in range(4):
            col=8*zero+4*flag+spin
            R[col,col]=0;R[8*zero+4*(1-flag)+spin,col]=1
    ready.append(s.SparseMatrix(R));ready_addresses.append({'old_type':j,'control0_diagonal':dummy,'control1_zero':zero})
    # The whole allowed raw two-port source support, including its false port.
    support=s.diag(*[s.Integer(r//8 in (zero,dummy)) for r in range(dim)])
    equal(DF*support,support,'actual READY-CX raw support is guarded '+str(j))
M0=product(ready,dim)
X=s.Matrix([[0,1],[1,0]])
equal(M0,s.kronecker_product(I-e0,s.eye(8))+s.kronecker_product(e0,X,s.eye(4)),'two actual READY-CX calls implement full M0')

# Lift each actual middle stage, including dirty flags and Spin, by the
# already owned AF frame. Complement columns are fixed, never discarded.
TE=s.MutableSparseMatrix(dim,32*d,{})
for work in range(4):
    for flag in range(2):
        for spin in range(4):
            for old in range(d):
                r=next(r for r in range(D) if E[r,work*d+old])
                TE[8*r+4*flag+spin,(8*work+4*flag+spin)*d+old]=1
TE=s.SparseMatrix(TE);RE=TE*TE.T
logical=[symbolic(N.gate_matrix(word,x)) for x in word.gates]
middle=[mat(TE*s.kronecker_product(x,s.eye(d))*TE.T+ID-RE) for x in logical]
frame_g=[];frame_si=[]
for op in ops:
    frame_g.append(s.kronecker_product(rotation(D,op['rows']),s.eye(8)))
    S=s.MutableSparseMatrix(ID)
    for first,second in op['rows']:
        for flag in (0,1):
            for r in range(4):
                for c in range(4):S[8*second+4*flag+r,8*second+4*flag+c]=N.L_I[r,c]
    frame_si.append(s.SparseMatrix(S))
decode=[]
for R,S in reversed(list(zip(frame_g,frame_si))):decode.extend([S,S,R,S,S])
schedule=decode+ready+middle+ready+frame_g
names=['SourceI','SourceI','G','SourceI','SourceI']*len(ops)+['CX']*2+[x.op for x in word.gates]+['CX']*2+['G']*len(ops)
require(len(schedule)==107 and Counter(names)=={'G':24,'CX':30,'SourceI':53},'actual107-call AF schedule inventory')
actual=product(schedule,dim)
BS=s.kronecker_product(B,s.eye(8))
target=mat(BS*M0*(TE*s.kronecker_product(U,s.eye(d))*TE.T+ID-RE)*M0*BS.T)
equal(actual,target,'all107 specified calls on every712 AF/flag/Spin column')
equal(actual.T,actual,'whole actual107-call endpoint is a reflection')
for i,gate in enumerate(decode+ready+ready+frame_g):
    equal(DF*(gate-ID),gate-ID,'real frame and READY gate guard '+str(i))

# The true regular canonical corner is a conditional trace, not the
# working input J. Each encoded work diagonal has weight gamma=p^8.
# M0 makes work0 read flag1 and every other work column read flag0.
gamma=p**8
def corner(A,work,flag):
    rows=[8*work+4*flag+spin for spin in range(4)]
    return s.SparseMatrix(A.extract(rows,rows))
def ready_corner(A):return mat(gamma*(corner(A,0,1)+sum((corner(A,w,0) for w in (1,2,3)),s.zeros(4))))
ceff=1-gamma+gamma*p**3
equal(ready_corner(U)+(1-4*gamma)*s.eye(4),ceff*s.eye(4),'true regular corner with every encoded and complement contribution')

# Exhaust every real skew local generator on each NEW parity gadget gate.
# This retains arbitrary gate-support faults, including flag-changing and
# Spin-entangled faults, instead of declaring every new control source zero.
def local_skew(wires,u,v):
    shifts=[4-q for q in wires];out=s.MutableSparseMatrix(32,32,{})
    for column in range(32):
        loc=sum(((column>>shift)&1)<<(len(shifts)-1-pos) for pos,shift in enumerate(shifts))
        if loc not in (u,v):continue
        dest=v if loc==u else u;row=column
        for pos,shift in enumerate(shifts):row=(row&~(1<<shift))|(((dest>>(len(shifts)-1-pos))&1)<<shift)
        out[row,column]=1 if loc==u else -1
    return s.SparseMatrix(out)
prefix=[s.SparseMatrix(s.eye(32))]
for x in logical:prefix.append(mat(x*prefix[-1]))
suffix=[None]*(len(logical)+1);suffix[-1]=s.SparseMatrix(s.eye(32))
for j in reversed(range(len(logical))):suffix[j]=mat(suffix[j+1]*logical[j])
raw_count=0;nonzero_count=0
for j in range(len(ginv),len(ginv)+len(cz)):
    gate=word.gates[j]
    for u in range(2**len(gate.wires)):
        for v in range(u+1,2**len(gate.wires)):
            h=local_skew(gate.wires,u,v)
            H=mat(suffix[j+1]*h*suffix[j+1].T)
            delta=mat(H*U)
            H1=H.extract(idx[1],idx[1]);dtrue=mat(H1*logical_true)
            Xtrue=dtrue[:4,:4]
            full=ready_corner(delta)
            require(AF.zero(full+full.T-gamma*(Xtrue+Xtrue.T)),'raw parity source transports '+str((j,u,v)))
            raw_count+=1
            if not AF.zero(full+full.T):nonzero_count+=1
require(raw_count==260,'all260 new raw skew-basis control rows retained')
require(nonzero_count>0,'new raw controller graph is not automatically source neutral')

# A norm-one fault on the FINAL actual CX of the parity gadget changes
# the true report. It is supported on precisely that gate's two wires.
last=len(ginv)+len(cz)-1
h=s.MutableSparseMatrix(32,32,{})
for port in (0,1):
    for spin in range(4):
        lo=16*port+4+spin;hi=lo+8
        h[hi,lo]=1;h[lo,hi]=-1
delta=mat(suffix[last+1]*h*prefix[last+1])
neg=ready_corner(delta)
equal(neg,-2*gamma*a*p*s.eye(4),'actual independent last-CX control has nonzero first source')
equal(h.T*h,s.diag(*[s.Integer((i>>2)&1) for i in range(32)]),'hostile raw control has operator norm one')

result={'status':'PASS','checks':len(checks),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'input_pins':{'AF':AF_PIN,'native':NATIVE_PIN,'frame':FRAME_PIN,'regular_source':REGULAR_PIN},
 'binary_middle':{'stages':37,'inventory':{'G':2,'CX':26,'SourceI':9},'new_parity_stages':25,
   'parity_inventory':{'CX':20,'SourceI':5},'all32_columns_executed':True,'fresh_flag_required':True},
 'AF_schedule':{'stages':len(schedule),'inventory':dict(Counter(names)),'working_columns_executed':dim,
   'oldRIGHT_identity_factor':2,'total_working_columns':2*dim,'regular_right_multiplicities':[55,34],
   'full_regular_dimension':2*8*(55**2+34**2),'true_canonical_input_rank':16,
   'ready_CX_addresses':ready_addresses,'binary_AF_physical_admission':False},
 'source':{'raw_new_gate_basis_rows':raw_count,'nonzero_Hermitian_rows':nonzero_count,
   'actual_cold':'(1-p^8+p^11) I16','actual_gain_factor':'p^11/(1-p^8+p^11)',
   'controller_transport':'true-flag query tangent; false and mixed flags have zero Hermitian conditional source',
   'last_CX_negative_control':'D C = -2 p^8 a p I16',
   'whole_heat':'actual107-call enlarged carrier; no cancellation claimed for independent faults'},
 'scope':'Specified native binary controller and AF paired-port lift, with all raw control rows. No physical flag/actuator admission, gigantic heat or GR closure.',
 'labels':checks}
print(json.dumps(result,indent=2,sort_keys=True))
