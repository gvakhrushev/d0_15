#!/usr/bin/env python3
"""Exact, paid return-record completion of an already emitted native word.

Same original16-wire boundary, three unused RIGHT blanks, every work column.
The generic compiler transform is exact; no large field compiler is simulated.
"""
from __future__ import annotations
import hashlib,importlib.util,json,math,platform,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
import mpmath as mp

ROOT=Path.cwd();PAPER=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
CHECKS=[]
def require(ok,label):
    if not bool(ok):raise ArithmeticError(label)
    CHECKS.append(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def frozen(tag,language='json'):
    b=PAPER.read_bytes();start=('<!-- BEGIN '+tag+' -->\n```'+language+'\n').encode();end=('```\n<!-- END '+tag+' -->').encode()
    require(b.count(start)==b.count(end)==1,'unique input '+tag)
    return b.split(start)[1].split(end)[0]
prior_b=frozen('7dr RETAINED REPORT FIBRE RECEIPT')
require(sha(prior_b)=='c20bd62754ffaa4fb89a8ae16ab4b3f18c1c04f38112bcaa0e2e550058da3558','actual previous native word/source receipt')
prior=json.loads(prior_b)
heat_b=frozen('7do PAID BINARY INPUT RECEIPT')
require(sha(heat_b)=='811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba','unchanged original full heat coefficient')
PINS={
 '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py':'222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
 '02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md':'1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254',
 '02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md':'9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5',
 '02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for name,pin in PINS.items():require(sha((ROOT/name).read_bytes())==pin,'owned input '+name)
paper=PAPER.read_text();a0proof=paper.index('## 7cq.');z0proof=paper.index('### 9. Frozen changed code and actual receipt',a0proof)
require(sha(paper[a0proof:z0proof].encode())=='a4046500768bc3abcfc571f18aa749055449aae0d448ff041487a4fa2e538b34','exact existing field compiler/proof scope')
owner=ROOT/next(iter(PINS));spec=importlib.util.spec_from_file_location('return_record_native',owner)
ne=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ne;spec.loader.exec_module(ne)
p=ne.P;a=ne.A;c=p**3;u=2*p*a;z=s.Rational(1,2**20);az=1-z
field=ne.GOLDEN_FIELD;ZERO=field.zero;ONE=field.one
def f(x):return field.from_sympy(s.sympify(x))
def dm(m):return DomainMatrix.from_Matrix(s.Matrix(m)).convert_to(field).to_sparse()
def sparse(d,shape):return DomainMatrix.from_dok({k:v for k,v in d.items() if v},shape,field).to_sparse()
def eye(n):return sparse({(j,j):ONE for j in range(n)},(n,n))
def eq(A,B,label):require((A-B).is_zero_matrix,label)
def trace(A):return sum((v for (r,k),v in A.to_dok().items() if r==k),ZERO)

base=prior['literal_words']['unrecorded31'];seed=base[:5];pre=base[5:16];zw=base[16:24];post=base[24:]
mirror=seed+post+zw+pre
BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12);B=(0,11,12);R=(7,8,9)
require(all(w in BLANKS for w in B+R) and not set(B)&set(R),'real pre-existing ordinary work and reserve blanks')
require(not any(set(g['wires'])&set(R) for g in base),'actual reserved RIGHT wires never touched by original word')
def complete_return_record(execution,reserve):
    """A total finite transformation on its declared ordinary-blank domain.

    No allocation, reset, angle synthesis or native-owner modification.
    The caller supplies real already-initialized untouched record wires.
    """
    ne.validate_execution(execution,max_qubits=execution.qubits,max_expanded_stages=len(execution.gates))
    touched=set(w for g in execution.gates for w in g.wires)
    work=tuple(sorted(set(execution.blank_wires)&touched));reserve=tuple(reserve)
    spin=set(execution.source_spin or ())
    if (len(reserve)!=len(work) or len(set(reserve))!=len(reserve)
        or not set(reserve)<=set(execution.blank_wires) or set(reserve)&touched
        or set(work+reserve)&spin):
        raise ne.DomainError('need one untouched ordinary actual blank per used processing blank')
    cs=tuple(ne.Gate('CX',(q,r)) for q,r in zip(work,reserve))
    reports=tuple(dict.fromkeys(execution.report_bits+reserve))
    out=ne.Execution(execution.qubits,execution.blank_wires,execution.old_right,
                     cs+execution.gates+cs,execution.profile,execution.source_port,execution.source_spin,reports)
    ne.validate_execution(out,max_qubits=execution.qubits,max_expanded_stages=len(execution.gates)+2*len(work))
    return out,work
copy=[{'op':'CX','wires':[q,r]} for q,r in zip(B,R)]
upstream=post+pre
upstream_alt=post+post+seed[1:]
words={'reference31':base,'mirror31':mirror,'completed37':copy+base+copy,'mirror37':copy+mirror+copy,
       'prepared55':upstream+copy+base+copy,'prepared55_alt':upstream_alt+copy+base+copy,'one_sided34':base+copy,
       'omitted_query35':copy[:1]+copy[2:]+base+copy[:1]+copy[2:]}
inventories={k:dict(sorted(Counter(g['op'] for g in w).items())) for k,w in words.items()}
for name,word in words.items():
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in word),ne.G_CX_SOURCE_I,0,(13,14),R)
    ne.validate_execution(ex,max_qubits=16,max_expanded_stages=55)
    require(len(word)==sum(inventories[name].values()),'literal inventory '+name)
require(inventories['completed37']==inventories['mirror37']=={'CX':25,'G':2,'SourceI':10},'actual37 inventory with BOTH three-copy legs')
require(len(base)==len(mirror)==31,'exact existing and mirror seed/query call counts')
for old,new in [('reference31','completed37'),('mirror31','mirror37')]:
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in words[old]),ne.G_CX_SOURCE_I,0,(13,14))
    compiled,actual_work=complete_return_record(ex,R)
    require(actual_work==B,'constructor consumes ACTUAL old-word blank support')
    require([{'op':g.op,'wires':list(g.wires)} for g in compiled.gates]==words[new],
            'finite generic constructor emits exactly the verified native word')
for bad in [(7,8),(7,8,11),(7,8,13)]:
    try:complete_return_record(ex,bad)
    except ne.DomainError:require(True,'reject missing, already-used or unprepared record wire')
    else:raise ArithmeticError('bad reserve accepted')
require(inventories['prepared55']==inventories['prepared55_alt']=={'CX':37,'G':4,'SourceI':14},'actual equal55 preparation inventories')

# The new record uses old RIGHT7/8/9, not a new pure resource or LEFT archive bit.
# All9 active bits are explicit; the7 inactive bits are6 actual blanks+oldRIGHT.
ACTIVE=(0,6,11,12,13,14,7,8,9);POS={w:j for j,w in enumerate(ACTIVE)};NW=len(ACTIVE);DIM=2**NW;DOLD=64
I=eye(DIM);IOLD=eye(DOLD)
def bits(n):return [(n>>(NW-1-j))&1 for j in range(NW)]
def number(b):return sum(v<<(NW-1-j) for j,v in enumerate(b))
def local(b,w):return sum(b[POS[t]]<<(len(w)-1-j) for j,t in enumerate(w))
def embed(m,w):
    m=s.Matrix(m);d={}
    for col in range(DIM):
        b=bits(col);j=local(b,w)
        for row in range(2**len(w)):
            if not m[row,j]:continue
            br=b[:]
            for q,t in enumerate(w):br[POS[t]]=(row>>(len(w)-1-q))&1
            d[number(br),col]=f(m[row,j])
    return sparse(d,(DIM,DIM))
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CACHE={}
def gate(g):
    key=g['op'],tuple(g['wires'])
    if key not in CACHE:
        M=embed({'G':ne.G_LOCAL,'CX':CX,'SourceI':ne.SOURCE_I_LOCAL}[key[0]],key[1])
        eq(M.transpose().matmul(M),I,'exact full-column primitive '+repr(key));CACHE[key]=M
    return CACHE[key]
def endpoint(word):
    out=I
    for g in word:out=gate(g).matmul(out)
    return out
U={name:endpoint(word) for name,word in words.items()};Ccopy=endpoint(copy)
eq(endpoint(upstream),I,'actual paid18-call upstream identity at its original base')
eq(U['prepared55'],U['completed37'],'paid upstream base has the same COMPLETE endpoint')
eq(U['prepared55_alt'].matmul(U['prepared55_alt']),I,'the actual different preparation also gives a complete reflection')
require(trace(U['prepared55_alt'])==ZERO,'same full balanced signature at the actual equal55 clocks')
eq(Ccopy.matmul(Ccopy),I,'both actual copy products are the same exact involution')
for old,new in [('reference31','completed37'),('mirror31','mirror37')]:
    eq(U[new],Ccopy.matmul(U[old]).matmul(Ccopy),'literal paid conjugation '+new)
    eq(U[new].matmul(U[new]),I,'entire native completed endpoint is a reflection '+new)
    require(trace(U[new])==ZERO,'balanced full512 active signature '+new)
require(not (U['one_sided34'].matmul(U['one_sided34'])-I).is_zero_matrix,'one-sided copying does NOT retain the full reflection')

inputs=[j for j in range(DIM) if all(bits(j)[POS[t]]==0 for t in B+R)]
require(len(inputs)==8 and DIM*128==65536,'actual rank8 timesoldRIGHT2; full512 times128')
P=sparse({(j,j):ONE for j in inputs},(DIM,DIM))
M=sparse({(j,j):ONE for j in range(DIM) if all(bits(j)[POS[t]]==0 for t in R)},(DIM,DIM))
gap_projector=M-P;eq(gap_projector.matmul(gap_projector),gap_projector,'true success M contains original actual input P')
eq(Ccopy.matmul(P),P,'first actual COPY leg is identity on all original initialized input columns')
Told=I;Tnew=Ccopy
for j,g in enumerate(base):
    Told=gate(g).matmul(Told);Tnew=gate(g).matmul(Tnew)
    eq(Tnew.matmul(P),Told.matmul(P),'unchanged actual original prefix state at shifted clock '+str(j+1))
Q=dm(s.diag(*[int(bits(j)[POS[6]]==0) for j in inputs]));IIN=eye(8)
corners={name:mat.extract(inputs,inputs) for name,mat in U.items()}
for name in U:
    amp=c*c if name=='prepared55_alt' else c
    eq(corners[name],Q.scalarmul(f(amp)),'entire literal return corner '+name)
E={}
for name in ('completed37','mirror37','prepared55','omitted_query35'):
    W=U[name].extract(list(range(DIM)),inputs)
    E[name]=W.transpose().matmul(M).matmul(W)
    if name!='omitted_query35':
        require(gap_projector.matmul(W).is_zero_matrix,'ALL success branches return for '+name)
        eq(E[name],corners[name].transpose().matmul(corners[name]),'actual success effect equals original return effect '+name)
eq(E['omitted_query35'],Q,'omitting actual query copy loses its recorded return test')
eq(E['omitted_query35']-corners['omitted_query35'].transpose().matmul(corners['omitted_query35']),
   Q.scalarmul(f(1-c*c)),'explicit positive return gap when one active work bit is not copied')

# All8 retained flag effects, including zero/impossible events, on ALL inputs.
effects={}
for label in range(8):
    mask=sparse({(j,j):ONE for j in range(DIM) if j%8==label},(DIM,DIM))
    ef={name:U[name].transpose().matmul(mask).matmul(U[name]).extract(inputs,inputs)
        for name in ('completed37','mirror37','prepared55_alt')}
    eq(ef['completed37'],ef['mirror37'],'same entire initialized full flag effect '+str(label))
    eq(ef['completed37'],ef['prepared55_alt'],'same full flag law after the ACTUAL different upstream preparation '+str(label))
    effects[label]=ef['completed37']
total=sparse({},(8,8))
for Ef in effects.values():total=total+Ef
eq(total,IIN,'every retained outcome remains in the exact operator partition')
require(sum(not E0.is_zero_matrix for E0 in effects.values())==4,'four nonzero real flag outcomes; no postselection')
require(not (U['completed37'].extract(list(range(DIM)),inputs)-U['mirror37'].extract(list(range(DIM)),inputs)).is_zero_matrix,
        'same entire record law does not imply same coherent terminal work isometry')

# The old archive is never rewritten by the chosen RIGHT record targets.
for name in ('completed37','mirror37','prepared55_alt'):
    require(all(bits(row)[:2]==bits(col)[:2] for (row,col),v in U[name].to_dok().items() if v),
            'all-column LEFT address fixed '+name)
    for aa in range(4):
        for bb in range(4):
            e=s.zeros(4);e[aa,bb]=1;A=embed(e,(13,14))
            eq(U[name].matmul(A),A.matmul(U[name]),'all old Spin matrix units '+name)

# Generated physical cuts: original initial P, all real prefixes, final closure.
T=I;Pj=P
for j,g in enumerate(words['completed37']):
    Tn=gate(g).matmul(T);Pn=Tn.matmul(P).matmul(Tn.transpose())
    eq(Pn.matmul(gate(g)).matmul(Pj),gate(g).matmul(Pj),'actual generated cut row '+str(j+1))
    T,Pj=Tn,Pn
eq(P.matmul(T.transpose()).matmul(I-P).matmul(T).matmul(P).extract(inputs,inputs),
   IIN-corners['completed37'].transpose().matmul(corners['completed37']),'closing complement keeps all return failures')

# Complete cotangent and its one common record-source representation.
den=az+z*c*c
Rbar=sparse({(j,j):f(1/den if bits(j)[POS[6]]==0 else 1/az) for j in inputs},(DIM,DIM))
B0=U['completed37'].matmul(Rbar).matmul(U['completed37'].transpose())
Cret=(B0.matmul(P)-P.matmul(B0)).scalarmul(f(-z))
Cobs=(B0.matmul(M)-M.matmul(B0)).scalarmul(f(-z))
eq(Cret,Cobs,'WHOLE full512-column cotangent equals actual retained zero-flag source')
require(not Cret.is_zero_matrix,'real unrestricted report response is NOT removed')
for j,g in enumerate(words['completed37']):
    suffix=endpoint(words['completed37'][j+1:])
    eq(suffix.transpose().matmul(Cret).matmul(suffix),suffix.transpose().matmul(Cobs).matmul(suffix),
       'full source at actual independent occurrence '+str(j+1))

# Exact pullback on every original old control, BEFORE a field approximation.
refB=U['reference31'].matmul(Rbar).matmul(U['reference31'].transpose())
refC=(refB.matmul(P)-P.matmul(refB)).scalarmul(f(-z))
def ptrace_record(A):
    d={}
    for (r,k),v in A.to_dok().items():
        if r%8==k%8:
            key=(r//8,k//8);d[key]=d.get(key,ZERO)+v
    return sparse(d,(DOLD,DOLD))
eq(ptrace_record(Ccopy.matmul(Cret).matmul(Ccopy)),ptrace_record(refC),
   'all original endpoint-control covectors preserved exactly after paid record completion')

# Independent original-work preparation BEFORE the first copy is an additional
# source block, distinct from the physical field preparations INSIDE the old word.
Cbefore=U['completed37'].transpose().matmul(Cret).matmul(U['completed37'])
require(M.matmul(Cbefore).matmul(M).is_zero_matrix,'every upstream isometric direction inside actual blank-record sector has zero source')
require(ptrace_record(Cbefore).is_zero_matrix,'ALL original-work upstream unitary source directions vanish')
for j in range(len(upstream)):
    suffix=endpoint(words['prepared55'][j+1:]);Cj=suffix.transpose().matmul(Cret).matmul(suffix)
    require(ptrace_record(Cj).is_zero_matrix,'independent paid upstream primitive row zero '+str(j+1))

# A genuine NEW record-copy comparison row is nonzero because it changes its
# actual record effect. This local matrix curve is NOT a free native angle.
Hp=s.zeros(4);Hp[3,0]=1;Hp[0,3]=-1
H=embed(Hp,(11,8));jnew=len(copy)+len(base)+1
require(words['completed37'][jnew]=={'op':'CX','wires':[11,8]},'actual new QUERY-record copy occurrence')
suffix=endpoint(words['completed37'][jnew+1:]);X=suffix.matmul(H).matmul(suffix.transpose())
row=field.to_sympy(2*trace(Cret.matmul(X)))
require(s.simplify(row-16*z*c*u/den)==0,'new copy source equals TRUE rank16 report derivative')
de=(U['completed37'].transpose().matmul(M.matmul(X)-X.matmul(M)).matmul(U['completed37'])).extract(inputs,inputs)
eq(de,Q.scalarmul(f(-2*c*u)),'nonzero record-copy row explicitly changes zero-record effect')

# A comparator on the nonreturn query after an OMITTED copy preserves those
# remaining flags but retains a nonzero whole-price source.
Bom=U['omitted_query35'].matmul(Rbar).matmul(U['omitted_query35'].transpose())
Com=(Bom.matmul(P)-P.matmul(Bom)).scalarmul(f(-z))
Jq=embed(s.Matrix([[0,-1],[1,0]]),(11,))
eq(Jq.matmul(M),M.matmul(Jq),'omitted query rotation preserves the incomplete record law')
require(trace(Com.matmul(Jq))!=ZERO,'omitted active record retains an actual independent source')
Com_before=U['omitted_query35'].transpose().matmul(Com).matmul(U['omitted_query35'])
require(not M.matmul(Com_before).matmul(M).is_zero_matrix,'missing record also invalidates unrestricted upstream stationarity')

# Exact nonscalar control of the universal RETURN identity. It is explicitly
# a rational matrix test, not a newly emitted arbitrary native primitive.
V=s.eye(4)
for i,j,co,si in [(0,2,s.Rational(3,5),s.Rational(4,5)),(1,2,s.Rational(5,13),s.Rational(12,13)),(0,1,s.Rational(8,17),s.Rational(15,17))]:
    A=s.eye(4);A[i,i]=A[j,j]=co;A[i,j]=-si;A[j,i]=si;V=A*V
# Row order: workblank first, then arbitrary protected bit; appended record last.
C=s.zeros(8)
for k in range(8):C[k^((k>>2)&1),k]=1
Vhat=C*s.kronecker_product(V,s.eye(2))*C;i0=s.eye(4)[:,:2];ih=s.kronecker_product(i0,s.Matrix([1,0]));P0=ih*ih.T;M0=s.kronecker_product(s.eye(4),s.diag(1,0))
K=i0.T*V*i0;Kh=ih.T*Vhat*ih
require(K.T!=K,'nonscalar test is not a disguised Hermitian scalar corner')
require(Kh==K and (M0-P0)*Vhat*ih==s.zeros(8,2),'universal exact gap identity for a nonscalar nonreflection control')
require(ih.T*Vhat.T*M0*Vhat*ih==K.T*K,'actual matrix record effect is K star K without scalar assumptions')

# Absolute whole heat: same old physical boundary; only the actual clock grows.
mp.mp.dps=100;mp.iv.dps=90;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;aa=iv.sqrt(pp);cc=pp**3;uu=2*pp*aa;zz=iv.mpf(1)/2**20;beta=2*pp*pp;ab=1-zz
aheat=iv.mpf(json.loads(heat_b)['complete_book']['a0_interval'])
def ends(x):return mp.mpf(x.a),mp.mpf(x.b)
def interval(x,places=42):
    fac=10**places;lo,hi=ends(x*fac)
    def fmt(k):
        sg='-' if k<0 else '';k=abs(k);return sg+str(k//fac)+'.'+str(k%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
def heat_bound(N):
    x=Fraction(2,55);q=x**N/math.factorial(N)
    return Fraction(176,359)/(1-x*x)*q/(1-q)**2
def heat(N):
    q=heat_bound(N);er=iv.mpf(q.numerator)/q.denominator
    return iv.ln(N*65536*(2*aheat+359))/beta+iv.mpf([-ends(er)[1],ends(er)[1]])
JJ=-8*iv.ln(ab)-8*iv.ln(ab+zz*cc*cc)
prices={}
for name in ('reference31','mirror31','completed37','mirror37','prepared55','prepared55_alt','omitted_query35'):
    N=len(words[name]);HH=heat(N);Jnow=(-8*iv.ln(ab)-8*iv.ln(ab+zz*cc**4)) if name=='prepared55_alt' else JJ
    prices[name]={'N':N,'H_interval':interval(HH),'J_interval':interval(Jnow),'B_interval':interval(HH+Jnow),
                  'all_modes':425*N*65536,'unpaired_harmonic_modes':359*N*65536}
penalty=heat(37)-heat(31)
prep_delta=8*iv.ln((ab+zz*cc*cc)/(ab+zz*cc**4))
require(ends(prep_delta)[0]>0,'strict actual same-task same-inventory same-heat preparation price difference')
require(ends(penalty)[0]>0,'actual extra clock increases absolute price; no dropped baseline')
require(heat_bound(31)<Fraction(1,10**76),'full winding tails included at both actual clocks')

result={'status':'PASS','checks':len(CHECKS),'input_commit':'4b30fcb4dc743e7a04415c9701aae19a847e8dab',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':PINS,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'scope':'exact compiler completion in the declared ordinary-blank native sector; no physical X_N or GR promotion',
 'literal_words':words,'inventories':inventories,
 'word_sha256':{n:sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode()) for n,w in words.items()},
 'boundary':{'full_wires':16,'rank_input':16,'full_dimension':65536,'active_wires':ACTIVE,'active_dimension':512,'thermal_spectator':128,'input_spectator':2,'copied_processing_blanks':B,'real_unused_RIGHT_record_blanks':R,'new_supplied_blanks':0,'added_paid_CX':6},
 'universal_identities':{'return_corner_preserved_for_any_original_endpoint':True,'record_zero_effect':'K_original^* K_original','positive_gap':'exactly zero','entire_H_first_source_zero_if_original_endpoint_involution':True,'all_original_control_sources_preserved':True,'all_independent_occurrences_record_source_identity':37,'same_every_possible_future_context':False,'old_prefix_states_preserved_at_shifted_ticks':31},
 'finite_fibre_pair':{'words':['completed37','mirror37'],'all8_record_effects_equal':True,'nonzero_record_outcomes':4,'full_work_isometries_different':True,'entire_H_J_prices_exact_equal':True,'full_signature_each':{'+1':32768,'-1':32768}},
 'independent_upstream':{'literal_word':'prepared55','genuine_extra_calls':18,'every_independent_original_work_direction_zero':True,'every_actual18_prefix_occurrence_zero':True,'fresh_record_sector_kept':True,'actual_field_preparations_remain_INSIDE_copied_original_word':True,'literal_same55_alternative':'prepared55_alt','same_all8_record_effects':True,'same_entire_heat':True,'actual_full_B_alt_minus_base_interval':interval(prep_delta)},
 'new_copy_row':{'stage':jnew+1,'actual_pair':[11,8],'generator':'|11><00|-|00><11|; op norm1; matrix comparison only','effect_derivative':'-2 c u Q_return','full_source_interval':interval(16*zz*cc*uu/(ab+zz*cc*cc)),'preserves_actual_report':False},
 'negative_controls':{'one_sided34_not_involution':True,'omitted_query35_gap':'(1-c^2)Q_return','omitted_query_nonzero_source_at_fixed_incomplete_record':True,'nonscalar_control_not_emitted_as_a_native_gate':True},
 'whole_book':prices,'actual_B37_minus_B31_interval':interval(penalty),
 'compiler_transform':{'function':'complete_return_record','unchanged_original_native_validator':True,'actual_full_words_emitted':2,'rejects_uninitialized_or_used_record_wires':True},
 'remaining':{'actual_reserve_supply_for_any_larger_compiler':False,'complete_physical_X_N':False,'selected_full_Cost_Info':False,'clock_boundary_equations':False,'all42_native_refinement_admission':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
