#!/usr/bin/env python3
"""A fixed all-input recording instrument, real native implementations,
and a strict whole-heat distinction despite identical initialized histories.
No original field solver, compiler catalogue or large Hodge matrix is run.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,importlib.util,json,math,platform,sys
import sympy as s
from sympy.polys.matrices import DomainMatrix
import mpmath as mp

ROOT=Path.cwd();PAPER=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
CHECKS=[]
def need(ok,name):
    if not bool(ok):raise ArithmeticError(name)
    CHECKS.append(name)
def sha(b):return hashlib.sha256(b).hexdigest()
def frozen(tag):
    b=PAPER.read_bytes();a=('<!-- BEGIN '+tag+' -->\n```json\n').encode();z=('```\n<!-- END '+tag+' -->').encode()
    need(b.count(a)==b.count(z)==1,'unique prior '+tag)
    return b.split(a)[1].split(z)[0]
prior_b=frozen('7ds RETURN RECORD COMPILER RECEIPT')
need(sha(prior_b)=='5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e','original complete literal word')
prior=json.loads(prior_b)
step_b=frozen('7dt ONE SIDED PRICE GRAPH RECEIPT')
need(sha(step_b)=='b4e52e9d777135388051c2e5908e99a3110816b256be7d5769315a985dffbfe3','published price-graph result')
heat_b=frozen('7do PAID BINARY INPUT RECEIPT')
need(sha(heat_b)=='811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba','original all-mode heat coefficient')
pins={
 '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py':'222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
 '02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for path,pin in pins.items():need(sha((ROOT/path).read_bytes())==pin,'consumed input '+path)
spec=importlib.util.spec_from_file_location('native_instrument_fibre',ROOT/next(iter(pins)))
ne=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ne;spec.loader.exec_module(ne)
p=ne.P;a=ne.A;c=p**3;u=2*p*a;z=s.Rational(1,2**20);az=1-z
F=ne.GOLDEN_FIELD;ZERO=F.zero;ONE=F.one
def f(x):return F.from_sympy(s.sympify(x))
def sparse(d,shape):return DomainMatrix.from_dok({k:v for k,v in d.items() if v},shape,F).to_sparse()
def dm(m):return DomainMatrix.from_Matrix(s.Matrix(m)).convert_to(F).to_sparse()
def eye(n):return sparse({(j,j):ONE for j in range(n)},(n,n))
def eq(A,B,name):need((A-B).is_zero_matrix,name)
def tr(A):return sum((v for (j,k),v in A.to_dok().items() if j==k),ZERO)

ACTIVE=(0,6,11,12,13,14,7,8,9);POS={w:j for j,w in enumerate(ACTIVE)};NW=len(ACTIVE);DIM=2**NW;I=eye(DIM)
BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12);WORK=(0,11,12);RECORD=(7,8,9)
def bits(k):return [(k>>(NW-1-j))&1 for j in range(NW)]
def number(b):return sum(v<<(NW-1-j) for j,v in enumerate(b))
def embed(m,w):
    m=s.Matrix(m);out={}
    for col in range(DIM):
        b=bits(col);j=sum(b[POS[t]]<<(len(w)-1-k) for k,t in enumerate(w))
        for row in range(2**len(w)):
            if not m[row,j]:continue
            bb=b[:]
            for k,t in enumerate(w):bb[POS[t]]=(row>>(len(w)-1-k))&1
            out[number(bb),col]=f(m[row,j])
    return sparse(out,(DIM,DIM))
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]);CACHE={}
def gate(g):
    key=g['op'],tuple(g['wires'])
    if key not in CACHE:
        CACHE[key]=embed({'G':ne.G_LOCAL,'CX':CX,'SourceI':ne.SOURCE_I_LOCAL}[key[0]],key[1])
        eq(CACHE[key].transpose().matmul(CACHE[key]),I,'all-column native primitive '+repr(key))
    return CACHE[key]
def endpoint(w):
    U=I
    for g in w:U=gate(g).matmul(U)
    return U
base=prior['literal_words']['reference31']
copy=[{'op':'CX','wires':[a,r]} for a,r in zip(WORK,RECORD)]
ha={'op':'CX','wires':[8,11]};hb={'op':'CX','wires':[8,0]}
instruments={'A':[ha]+copy,'B':[hb]+copy,'fault':copy+[{'op':'G','wires':[11]}]}
words={name:base+inst for name,inst in instruments.items()}
inventory={name:dict(sorted(Counter(g['op'] for g in w).items())) for name,w in words.items()}
for name,w in words.items():
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in w),ne.G_CX_SOURCE_I,0,(13,14),RECORD)
    ne.validate_execution(ex,max_qubits=16,max_expanded_stages=35)
    need(len(w)==35,'actual equal35 clock '+name)
need(inventory['A']==inventory['B']=={'CX':23,'G':2,'SourceI':10},'real matched inventory of both correct implementations')
ready=[j for j in range(DIM) if j%8==0]
inputs=[j for j in ready if all(bits(j)[POS[q]]==0 for q in WORK)]
J=I.extract(range(DIM),ready);ii=I.extract(range(DIM),inputs)
Pi=J.matmul(J.transpose());P=ii.matmul(ii.transpose());M=Pi
need(len(ready)==64 and len(inputs)==8,'complete pre-record ready carrier64 versus original input8')
C=endpoint(copy);Uold=endpoint(base)
R={name:endpoint(inst) for name,inst in instruments.items()}
U={name:R[name].matmul(Uold) for name in R}
target=C.matmul(J)
# One structural entanglement witness for the primitive-count theorem.
# Sum all eight A basis inputs with other old work zero and R zero; its
# output coefficient matrix across A|R is exactly I_8 (normalization omitted).
schmidt={}
for label in range(8):
    bs=[0]*NW
    for k,w in enumerate(WORK):bs[POS[w]]=(label>>(2-k))&1
    column=number(bs)
    for (row,col),value in C.to_dok().items():
        if col!=column:continue
        br=bits(row); old=sum(br[POS[w]]<<(2-k) for k,w in enumerate(WORK))
        rec=sum(br[POS[w]]<<(2-k) for k,w in enumerate(RECORD))
        schmidt[old,rec]=schmidt.get((old,rec),ZERO)+value
eq(sparse(schmidt,(8,8)),eye(8),'exact rank8 Schmidt witness for three necessary cross-CX calls')
def implementation_member(ex):
    ne.validate_execution(ex,max_qubits=16,max_expanded_stages=4)
    w=[{'op':g.op,'wires':list(g.wires)} for g in ex.gates]
    return (endpoint(w).matmul(J)-target).is_zero_matrix
for name,inst in instruments.items():
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in inst),ne.G_CX_SOURCE_I,0,(13,14),RECORD)
    need(implementation_member(ex)==(name!='fault'),'decidable SAME complete instrument predicate '+name)
for name in ('A','B'):
    eq(R[name].matmul(J),target,'universal all64-input recording map '+name)
    T=C.transpose().matmul(R[name])
    eq(T.matmul(Pi),Pi,'completion unitary fixes entire ready space pointwise '+name)
    eq(T.matmul(Pi),Pi.matmul(T),'true block decomposition of completion '+name)
need(not (R['A']-R['B']).is_zero_matrix,'native completion operators really differ')
eq(U['A'].matmul(J),U['B'].matmul(J),'same COMPLETE initialized field/body map on all64 inputs')
Va=I;Vb=I
for k,(ga,gb) in enumerate(zip(words['A'],words['B'])):
    Va=gate(ga).matmul(Va);Vb=gate(gb).matmul(Vb)
    eq(Va.matmul(J),Vb.matmul(J),'same every actual prepared prefix at tick '+str(k+1))

# Full operator readouts, including all input coherences and all retained outcomes.
for label in range(8):
    mask=sparse({(j,j):ONE for j in range(DIM) if j%8==label},(DIM,DIM))
    effects={n:R[n].matmul(J).transpose().matmul(mask).matmul(R[n].matmul(J)) for n in R}
    eq(effects['A'],effects['B'],'same universal pointer effect '+str(label))
    eq(effects['A'],effects['fault'],'pointer effect alone misses wrong post-state '+str(label))
Q=dm(s.diag(*[int(bits(j)[POS[6]]==0) for j in inputs]))
K={n:U[n].extract(inputs,inputs) for n in U}
E={n:U[n].matmul(ii).transpose().matmul(M).matmul(U[n].matmul(ii)) for n in U}
for name in ('A','B'):
    eq(K[name],Q.scalarmul(f(c)),'correct original return corner '+name)
    eq(E[name],K[name].transpose().matmul(K[name]),'exact return saturation '+name)
eq(K['fault'],Q.scalarmul(f(a*c)),'native post-copy Golden fault changes the return corner')
eq(E['fault'],Q.scalarmul(f(c*c)),'fault preserves actual retained record')
eq(E['fault']-K['fault'].transpose().matmul(K['fault']),Q.scalarmul(f((1-p)*c*c)),
   'actual positive gap invisible in the pointer law')
need(not (R['fault'].matmul(J)-target).is_zero_matrix,'fault not in universal instrument fibre')
eq(gate(instruments['fault'][-1]).matmul(M),M.matmul(gate(instruments['fault'][-1])),
   'fault preserves re-reading of the pointer itself')

# The new genuine finite heat witness uses the first full spectral character.
delta=tr(U['A'])-tr(U['B'])
need(delta==f(16*u),'exact full512-column first-character difference16u')
need(delta*f(128)==f(2048*u),'actual full65536 character difference2048u')
need(f(u*u)==f(1-c*c),'exact positive sine identity')
need(s.Rational(3,5)<p<s.Rational(2,3) and a>s.Rational(3,4),'rational positive-embedding enclosure')
need(u>s.Rational(9,10),'strict normalized character lower bound')
N=35;x=Fraction(2,55);q=x**N/math.factorial(N);ef=1/(1-x*x)
A1=Fraction(176,359)*ef*q/(1-q)**2
leading=Fraction(99,320)*Fraction(3,104)**N/math.factorial(N)
tail=66*ef*q*q/(1-q)
L=leading-tail
need(L>0,'first all-column character dominates the ENTIRE higher-winding tail')
lower=L/85;upper=2*A1
need(0<lower<upper,'strict rational WHOLE heat/price gap interval')

mp.mp.dps=130;mp.iv.dps=110;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;cc=pp**3;zz=iv.mpf(1)/2**20;beta=2*pp*pp;ab=1-zz
def ivrat(v):return iv.mpf(v.numerator)/v.denominator
def ends(v):return mp.mpf(v.a),mp.mpf(v.b)
def interval(v,places=46):
    fac=10**places;lo,hi=ends(v*fac)
    def fmt(n):
        sign='-' if n<0 else '';n=abs(n);return sign+str(n//fac)+'.'+str(n%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
a0=iv.mpf(json.loads(heat_b)['complete_book']['a0_interval'])
er=ends(ivrat(A1))[1];H=iv.log(N*65536*(2*a0+359))/beta+iv.mpf([-er,er])
Jgood=-8*iv.log(ab)-8*iv.log(ab+zz*cc*cc)
Jfault=-8*iv.log(ab)-8*iv.log(ab+zz*pp*cc*cc)
gapJ=Jfault-Jgood;err=ends(ivrat(2*A1))[1];gapB=gapJ+iv.mpf([-err,err])
need(ends(gapB)[0]>0,'same-clock actual Golden fault has strictly higher complete price')
fmtfrac=lambda v:mp.nstr(mp.mpf(v.numerator)/v.denominator,28)
result={'status':'PASS','checks':len(CHECKS),'input_commit':'22b4e3f430ddb7d8dd7af6e734f5e63225edd056',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':pins,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'record_implementations':instruments,'complete_words':{name:{'N':len(w),'inventory':inventory[name],
     'sha256':sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode())} for name,w in words.items()},
 'actual_boundary':{'full_wires':16,'record_ready_wires':RECORD,'copied_work_wires':WORK,'new_blanks':0,
  'active_matrix_dimension':512,'active_ready_dimension':64,'active_initial_rank':8,
  'full_dimension':65536,'input_rank':16,'thermal_spectator':128,'input_spectator':2},
 'same_task':{'universal_record_isometry_on_ALL_ready_inputs':True,'all35_prepared_prefixes_equal':True,
  'all_generated_cuts_equal':True,'same_every_terminal_test_on_the_actual_input':True,
  'same_full_operator_on_unprepared_records':False,'native_field_compiler_lookup_used':False,
  'minimal_correct_recorder_calls':3,'minimal_three_call_operator_is_C':True},
 'strict_full_price_separation':{'J_A_equals_J_B_exactly':True,'first_full_character_A_minus_B':'2048u, u=2p sqrt(p)',
  'H_A_minus_H_B_strictly_positive':True,'lower_bound_rational':str(lower),'upper_bound_rational':str(upper),
  'lower_bound_approx':fmtfrac(lower),'upper_bound_approx':fmtfrac(upper),
  'all_higher_windings_bounded':True,'A1_35_rational':str(A1),'A1_35_approx':fmtfrac(A1)},
 'whole_absolute_price':{'same_N':35,'all_modes':425*35*65536,'unpaired_harmonics':359*35*65536,
  'common_enclosure_H_A_H_B':interval(H),'common_enclosure_B_A_B_B':interval(H+Jgood),
  'J_A_J_B':interval(Jgood),'fault_B':interval(H+Jfault),'fault_B_minus_good_B':interval(gapB)},
 'negative_control':{'native_word': 'fault','all_pointer_effects_unchanged_on_every_ready_input':True,
  'pointer_rereading_unchanged':True,'correct_full_record_instrument':False,'return_gap':'(1-p)p^6 Q',
  'J_fault_minus_J_good':interval(gapJ)},
 'scope':{'physical_X_N_identified':False,'instrument_specification_forced_by_Book02_alone':False,
  'additional_cost_or_selector_added':False,'exact_heat_gauge_claimed':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
