#!/usr/bin/env python3
"""A paid native Golden echo, independent test/use controls and ONE Book price.

All emitted inverses are original forward primitives.  Unknown source Spin and
oldRIGHT remain arbitrary.  No resetting, measurement or extra fidelity price.
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
def frozen(tag,pin):
    b=PAPER.read_bytes();a=('<!-- BEGIN '+tag+' -->\n```json\n').encode();z=('```\n<!-- END '+tag+' -->').encode()
    need(b.count(a)==b.count(z)==1,'unique prior '+tag)
    raw=b.split(a)[1].split(z)[0];need(sha(raw)==pin,'pinned prior '+tag)
    return json.loads(raw)
prior=frozen('7ds RETURN RECORD COMPILER RECEIPT','5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e')
frozen('7du RECORD IMPLEMENTATION FIBRE RECEIPT','b5c6138e8ae5bd1d7cd23bc8cc9e8831448f6b6900f8ef609a84ae4154cf78b6')
heat=frozen('7do PAID BINARY INPUT RECEIPT','811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba')
pins={
 '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py':'222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
 '02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for path,pin in pins.items():need(sha((ROOT/path).read_bytes())==pin,'owned input '+path)
spec=importlib.util.spec_from_file_location('native_paid_calibration',ROOT/next(iter(pins)))
ne=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ne;spec.loader.exec_module(ne)
p=ne.P;a=ne.A;c=p**3;u=2*p*a
F=ne.GOLDEN_FIELD;ZERO=F.zero;ONE=F.one
def f(x):return F.from_sympy(s.sympify(x))
def sparse(d,shape):return DomainMatrix.from_dok({k:v for k,v in d.items() if v},shape,F).to_sparse()
def dm(m):return DomainMatrix.from_Matrix(s.Matrix(m)).convert_to(F).to_sparse()
def eye(n):return sparse({(j,j):ONE for j in range(n)},(n,n))
def eq(A,B,name):need((A-B).is_zero_matrix,name)

ACTIVE=(0,6,11,12,13,14,7,8,9,10);POS={w:j for j,w in enumerate(ACTIVE)};NW=len(ACTIVE);DIM=2**NW;I=eye(DIM)
BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12);WORK=(0,11,12);RECORD=(7,8,9);REF=10
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
        eq(CACHE[key].transpose().matmul(CACHE[key]),I,'complete native primitive '+repr(key))
    return CACHE[key]
def endpoint(w):
    U=I
    for g in w:U=gate(g).matmul(U)
    return U
base=prior['literal_words']['reference31']
copy=[{'op':'CX','wires':[q,r]} for q,r in zip(WORK,RECORD)]
probe=[{'op':'G','wires':[11]},{'op':'CX','wires':[11,10]}]
unprobe=[{'op':'CX','wires':[11,10]}]+base[5:16]
recorders={'good':[{'op':'CX','wires':[8,11]}]+copy,
           'bad':[{'op':'G','wires':[11]}]+copy}
calwords={k:probe+d+copy+unprobe for k,d in recorders.items()}
pairs=[('good','good'),('bad','bad'),('good','bad'),('bad','good')]
wholewords={t+'_'+r:calwords[t]+copy+base+recorders[r] for t,r in pairs}
allwords={('cal_'+k):v for k,v in calwords.items()};allwords.update(wholewords)
inventories={}
for name,w in allwords.items():
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in w),ne.G_CX_SOURCE_I,0,(13,14),RECORD+(REF,))
    ne.validate_execution(ex,max_qubits=16,max_expanded_stages=59)
    need(len(w)==(21 if name.startswith('cal_') else 59),'true emitted clock '+name)
    inventories[name]=dict(sorted(Counter(g['op'] for g in w).items()))
need(inventories['cal_good']=={'CX':15,'G':2,'SourceI':4},'paid21 correct inventory')
need(inventories['cal_bad']=={'CX':14,'G':3,'SourceI':4},'paid21 faulty inventory')
need(inventories['good_good']=={'CX':41,'G':4,'SourceI':14},'paid59 correct inventory')
need(inventories['bad_bad']=={'CX':39,'G':6,'SourceI':14},'paid59 faulty inventory')
need(inventories['good_bad']==inventories['bad_good']=={'CX':40,'G':5,'SourceI':14},'both independent mixed controls paid')

C=endpoint(copy);E=endpoint(probe);Ei=endpoint(unprobe);W=endpoint(base)
eq(Ei.matmul(E),I,'actual twelve-call inverse of actual two-call Golden probe on all1024 columns')
eq(endpoint(base[5:16]),gate({'op':'G','wires':[11]}).transpose(),'eleven-call routed inverse has no hidden source-Spin phase')
D={k:endpoint(w) for k,w in recorders.items()}
cal={k:endpoint(w) for k,w in calwords.items()}
for k in cal:
    eq(cal[k],Ei.matmul(C).matmul(D[k]).matmul(E),'complete chronological echo '+k)
    eq(cal[k].transpose().matmul(cal[k]),I,'full echo unitarity '+k)
eq(cal['good'],cal['good'].transpose(),'good full echo is a reflection')
need(not (cal['bad']-cal['bad'].transpose()).is_zero_matrix,'bad full echo is not a reflection')
ready=[j for j in range(DIM) if all(bits(j)[POS[w]]==0 for w in RECORD+(REF,))]
inputs=[j for j in ready if all(bits(j)[POS[w]]==0 for w in WORK)]
j=I.extract(range(DIM),ready);ii=I.extract(range(DIM),inputs)
need(len(ready)==64 and len(inputs)==8,'all ready64 and original8 active input columns')
Q=dm(s.diag(*[int(bits(k)[POS[6]]==0) for k in inputs]))
M=sparse({(k,k):ONE for k in ready},(DIM,DIM))
eq(cal['good'].matmul(ii),ii,'good paid test returns EVERY original input including unknown Spin')
eq(cal['good'].extract(inputs,inputs),eye(8),'good test original cold corner I')
eq(cal['bad'].extract(inputs,inputs),eye(8).scalarmul(f(a)),'bad test original cold corner sqrt(p) I')
eq(D['good'].matmul(j),C.matmul(j),'good use retains the entire ready recording isometry')
need(not (D['bad'].matmul(j)-C.matmul(j)).is_zero_matrix,'wrong before-copy use fails the recording isometry')

# One true faithful-probe identity on ALL query inputs in the declared local
# recorder sector.  The original quaternion Spin is a spectator, never made pure.
small_h={'good':dm(CX),'bad':dm(s.kronecker_product(s.eye(2),ne.G_LOCAL))}
# Here the small ordering is record,query, so CX is record -> query.
v=[sparse({(q,0):ONE},(4,1)) for q in (0,1)]
weights=(p,p*p)
need(f(sum(weights))==ONE,'Golden Schmidt weights normalized')
need(f(sum(1/t for t in weights))==f(p**-3),'exact faithful-probe inverse-weight constant')
for k,h in small_h.items():
    T=sum((f(weights[q])*h.to_dok().get((q,q),ZERO) for q in (0,1)),ZERO)
    variance=eye(1).scalarmul(ZERO)
    for q in (0,1):
        error=h.matmul(v[q])-v[q].scalarmul(T)
        variance=variance+error.transpose().matmul(error).scalarmul(f(weights[q]))
    eq(variance,eye(1).scalarmul(ONE-T*T),'exact positive faithful-probe variance '+k)
    need(T==(ONE if k=='good' else f(a)),'actual calibration corner equals weighted local diagonal '+k)

U={};corners={};effects={}
expected={'good_good':c,'bad_bad':4-7*p,'good_bad':a*(4*p-3),'bad_good':a*c}
for t,r in pairs:
    name=t+'_'+r
    U[name]=D[r].matmul(W).matmul(C).matmul(cal[t])
    corners[name]=U[name].extract(inputs,inputs)
    eq(corners[name],Q.scalarmul(f(expected[name])),'actual whole59 original cold corner '+name)
    out=U[name].matmul(ii)
    effects[name]=out.transpose().matmul(M).matmul(out)
    eq(effects[name],corners[name].transpose().matmul(corners[name]),'records AND real reference retain every failed return '+name)
    eq(U[name].transpose().matmul(U[name]),I,'full whole59 unitarity '+name)
eq(U['good_good'],endpoint(wholewords['good_good']),'literal emitted59 word equals composed full1024 matrix')
eq(U['bad_bad'],endpoint(wholewords['bad_bad']),'literal wrong emitted59 word equals composed full1024 matrix')
eq(U['good_good'].matmul(ii),C.matmul(W).matmul(ii),'actual good prepared field map equals original37 map')
need(f((4-7*p)**2-c*c)==f(60-97*p),'exact positive return-probability difference')
need(60-97*p>0,'wrong repeated control strictly improves total return probability')
# This remains a coherent unitary test: no branch is measured, killed or reset.
refzero=sparse({(k,k):ONE for k in range(DIM) if bits(k)[POS[REF]]==0},(DIM,DIM))
badout=cal['bad'].matmul(ii)
eq(badout.transpose().matmul(I-refzero).matmul(badout),eye(8).scalarmul(f(p*p)),
   'all wrong-calibration reference-failure probability p squared is retained')
eq(refzero.matmul(badout),ii.scalarmul(f(a)),'returning reference branch retains exact input, without conditioning the execution')

# Preserve old archive sections and the COMPLETE source-spin matrix algebra.
for name,V in {**{'cal_'+k:v for k,v in cal.items()},**U}.items():
    for w in (0,6):
        Z=embed(s.diag(1,-1),(w,))
        eq(V.matmul(Z),Z.matmul(V),'old LEFT archive observable '+str(w)+' '+name)
    # The four single-coordinate X/Z generators generate all M_4 on Spin.
    for w in (13,14):
        for lab,m in [('X',s.Matrix([[0,1],[1,0]])),('Z',s.diag(1,-1))]:
            S=embed(m,(w,))
            eq(V.matmul(S),S.matmul(V),'complete unknown source-Spin algebra '+str(w)+lab+' '+name)

# Whole heat includes every original 425 N d mode.  Never add standalone
# test and field Book prices: compute only the true N=59 monodromy and corner.
mp.mp.dps=130;mp.iv.dps=110;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;aa=iv.sqrt(pp);cc=pp**3;zz=iv.mpf(1)/2**20;beta=2*pp*pp;ab=1-zz
def ends(v):return mp.mpf(v.a),mp.mpf(v.b)
def ivrat(v):return iv.mpf(v.numerator)/v.denominator
def interval(v,places=46):
    fac=10**places;lo,hi=ends(v*fac)
    def fmt(n):
        sign='-' if n<0 else '';n=abs(n);return sign+str(n//fac)+'.'+str(n%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
def bound(N):
    x=Fraction(2,55);q=x**N/math.factorial(N)
    return Fraction(176,359)/(1-x*x)*q/(1-q)**2
a0=iv.mpf(heat['complete_book']['a0_interval']);Hs={};bounds={}
for N in (21,59):
    v=bound(N);bounds[N]=v;err=ends(ivrat(v))[1]
    Hs[N]=iv.log(N*65536*(2*a0+359))/beta+iv.mpf([-err,err])
def add_heat_error(v,N):
    err=ends(ivrat(2*bounds[N]))[1]
    return v+iv.mpf([-err,err])
Jcal={'good':iv.mpf(0),'bad':-16*iv.log(ab+zz*pp)}
ev={'good_good':cc,'bad_bad':4-7*pp,'good_bad':aa*(4*pp-3),'bad_good':aa*cc}
Jwhole={k:-8*iv.log(ab)-8*iv.log(ab+zz*t*t) for k,t in ev.items()}
calgap=add_heat_error(Jcal['bad']-Jcal['good'],21)
wholegap=add_heat_error(Jwhole['bad_bad']-Jwhole['good_good'],59)
mixgap=add_heat_error(Jwhole['good_bad']-Jwhole['good_good'],59)
need(ends(calgap)[0]>0,'wrong recorder is strictly dearer in standalone ORIGINAL21 Book')
need(ends(wholegap)[1]<0,'same wrong recorder is strictly cheaper in ONE ORIGINAL59 Book')
need(ends(mixgap)[1]<0,'successful earlier test does not certify independently changed later use')
need(425*59*65536==1643315200 and 359*59*65536==1388118016,'actual59 full and harmonic mode counts')
result={'status':'PASS','checks':len(CHECKS),'input_commit':'f23f9149c470051b35acc3fac42f3fecdba084ab',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':pins,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'literal_probe':probe,'literal_unprobe':unprobe,'literal_recorders':recorders,
 'emitted_words':{name:{'N':len(w),'inventory':inventories[name],
    'sha256':sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode())} for name,w in allwords.items()},
 'actual_boundary':{'full_wires':16,'blank_wires':BLANKS,'old_right':[15],
  'source_port':0,'source_spin':[13,14],'record_wires':RECORD,'real_reference_wire':REF,
  'extra_wires':0,'active_matrix_dimension':DIM,'thermal_spectator':64,
  'full_dimension':65536,'active_input_rank':8,'input_spectator':2,'input_rank':16},
 'exact_corners':{'cal_good':'I_16','cal_bad':'sqrt(p) I_16',
  'good_good':'p^3 Q','bad_bad':'(4-7p) Q','good_bad':'sqrt(p)(4p-3) Q','bad_good':'sqrt(p)p^3 Q','rank_Q':8},
 'faithful_probe':{'local_query_inputs_both_tested':True,'protected_unknown_input_prepared':False,
  'real_ref_used':True,'inverse_primitive_added':False,'discarded_or_reset_branches':False,
  'all_three_recorder_channels_freely_varied_and_tested':False,'same_code_equals_independent_hardware_control':False},
 'joint_map':{'good_prepared_map_equals_original37':True,'all_initial_coherences_retained':True,
  'whole_return_saturated_using_real_reference_and_records':True,'test_use_controls_kept_separate':True,
  'all_LEFT_archive_Z_sections_preserved':True,'complete_source_Spin_algebra_preserved':True},
 'whole_prices':{'cal_'+k:interval(Hs[21]+v) for k,v in Jcal.items()},
 'whole59_prices':{k:interval(Hs[59]+v) for k,v in Jwhole.items()},
 'strict_differences':{'cal_bad_minus_good':interval(calgap),
  'whole_bad_bad_minus_good_good':interval(wholegap),'whole_good_bad_minus_good_good':interval(mixgap)},
 'heat':{str(N):{'A1_rational':str(bounds[N]),'A1_approx':mp.nstr(ivrat(bounds[N]),22),
  'absolute_H_enclosure':interval(Hs[N]),'all_modes':425*N*65536,'unpaired_harmonics':359*N*65536} for N in (21,59)},
 'scope':{'one_original_H_plus_J':True,'standalone_prices_added':False,
  'new_fidelity_or_Info_penalty_added':False,'faulty_word_same_calibrated_task_competitor':False,
  'unconstrained_price_forces_correct_record_instrument':False,'physical_X_N_identified':False,
  'all_new_independent_control_sources_zero':False,'native_source_I_addressability_retained':True,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
