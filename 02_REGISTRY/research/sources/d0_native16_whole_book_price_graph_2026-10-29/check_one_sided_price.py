#!/usr/bin/env python3
"""Changed native post-record compiler and complete literal Book price.

Consumes frozen earlier witnesses; no old checker, field solver or Lean replay.
All finite controls below are actual Golden/CX/SourceI words. Matrix tangents
are labelled ambient comparisons, not continuously tunable Golden primitives.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib, importlib.util, json, math, platform, sys
import sympy as s
from sympy.polys.matrices import DomainMatrix
import mpmath as mp

ROOT=Path.cwd()
PAPER=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
CHECKS=[]
def need(ok, label):
    if not bool(ok): raise ArithmeticError(label)
    CHECKS.append(label)
def sha(b): return hashlib.sha256(b).hexdigest()
def frozen(tag):
    b=PAPER.read_bytes(); start=('<!-- BEGIN '+tag+' -->\n```json\n').encode()
    end=('```\n<!-- END '+tag+' -->').encode()
    need(b.count(start)==b.count(end)==1, 'unique frozen '+tag)
    return b.split(start)[1].split(end)[0]
old_b=frozen('7ds RETURN RECORD COMPILER RECEIPT')
need(sha(old_b)=='5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e', 'published compiler receipt')
old=json.loads(old_b)
heat_b=frozen('7do PAID BINARY INPUT RECEIPT')
need(sha(heat_b)=='811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba','original heat coefficient receipt')
pins={
 '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py':'222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
 '02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for path,pin in pins.items(): need(sha((ROOT/path).read_bytes())==pin,'unchanged consumed '+path)
spec=importlib.util.spec_from_file_location('native_post_record',ROOT/next(iter(pins)))
ne=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ne;spec.loader.exec_module(ne)
p=ne.P; a=ne.A; c=p**3; u=2*p*a; z=s.Rational(1,2**20); az=1-z
F=ne.GOLDEN_FIELD; Z=F.zero; O=F.one
def f(x): return F.from_sympy(s.sympify(x))
def sparse(d,shape): return DomainMatrix.from_dok({k:v for k,v in d.items() if v},shape,F).to_sparse()
def dm(A): return DomainMatrix.from_Matrix(s.Matrix(A)).convert_to(F).to_sparse()
def eye(n): return sparse({(j,j):O for j in range(n)},(n,n))
def eq(A,B,label): need((A-B).is_zero_matrix,label)
def tr(A): return sum((v for (j,k),v in A.to_dok().items() if j==k),Z)
BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12); WORK=(0,11,12); RECORD=(7,8,9)
base=old['literal_words']['reference31']; mirror=old['literal_words']['mirror31']
copies=[{'op':'CX','wires':[b,r]} for b,r in zip(WORK,RECORD)]
up=old['literal_words']['prepared55'][:18]
up_alt=old['literal_words']['prepared55_alt'][:18]
def execution(w):
    return ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in w),ne.G_CX_SOURCE_I,0,(13,14),RECORD)
def post_record(ex,work,reserve):
    """One FIXED support layout for the entire comparison catalogue."""
    ne.validate_execution(ex,max_qubits=ex.qubits,max_expanded_stages=len(ex.gates))
    work=tuple(work); reserve=tuple(reserve); touched={q for g in ex.gates for q in g.wires}
    if (len(set(work))!=len(work) or len(set(reserve))!=len(reserve)
        or len(work)!=len(reserve) or set(work)&set(reserve)
        or not set(work+reserve)<=set(ex.blank_wires)
        or set(reserve)&touched or not (set(ex.blank_wires)&touched)<=set(work)
        or set(work+reserve)&set(ex.source_spin or ())):
        raise ne.DomainError('need fixed support covering every used ordinary blank and untouched initialized records')
    final=tuple(ne.Gate('CX',(q,r)) for q,r in zip(work,reserve))
    out=ne.Execution(ex.qubits,ex.blank_wires,ex.old_right,ex.gates+final,ex.profile,ex.source_port,ex.source_spin,tuple(dict.fromkeys(ex.report_bits+reserve)))
    ne.validate_execution(out,max_qubits=ex.qubits,max_expanded_stages=len(ex.gates)+len(work))
    return out
words={'post34':base+copies,'mirror34':mirror+copies,'prepared52':up+base+copies,
       'prepared52_alt':up_alt+base+copies,'old_two_sided37':old['literal_words']['completed37'],
       'copy_fault34':base+[copies[0],{'op':'CX','wires':[8,11]},copies[2]]}
for name,w in words.items(): ne.validate_execution(execution(w),max_qubits=16,max_expanded_stages=52)
for name,w in [('post34',base),('mirror34',mirror),('prepared52',up+base),('prepared52_alt',up_alt+base)]:
    out=post_record(execution(w),WORK,RECORD)
    need([{'op':g.op,'wires':list(g.wires)} for g in out.gates]==words[name],'actual constructor '+name)
for bad_work,bad_record in [((0,12),(7,9)),(WORK,(7,8,11)),(WORK,(7,8,13))]:
    try: post_record(execution(base),bad_work,bad_record)
    except ne.DomainError: need(True,'reject unsupported layout '+repr((bad_work,bad_record)))
    else: raise ArithmeticError('bad layout accepted')
inventories={n:dict(sorted(Counter(g['op'] for g in w).items())) for n,w in words.items()}
need(inventories['prepared52']==inventories['prepared52_alt']=={'CX':34,'G':4,'SourceI':14},'true matched52 inventories')
need(inventories['post34']==inventories['mirror34']=={'CX':22,'G':2,'SourceI':10},'true matched34 inventories')
ACTIVE=(0,6,11,12,13,14,7,8,9); POS={w:j for j,w in enumerate(ACTIVE)}; n=len(ACTIVE); D=2**n; I=eye(D)
def bits(k): return [(k>>(n-1-j))&1 for j in range(n)]
def number(b): return sum(v<<(n-1-j) for j,v in enumerate(b))
def embed(m,w):
    m=s.Matrix(m); out={}
    for j in range(D):
        b=bits(j); q=sum(b[POS[x]]<<(len(w)-1-k) for k,x in enumerate(w))
        for r in range(2**len(w)):
            if not m[r,q]: continue
            bb=b[:]
            for k,x in enumerate(w): bb[POS[x]]=(r>>(len(w)-1-k))&1
            out[number(bb),j]=f(m[r,q])
    return sparse(out,(D,D))
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CACHE={}
def gate(g):
    key=g['op'],tuple(g['wires'])
    if key not in CACHE:
        CACHE[key]=embed({'G':ne.G_LOCAL,'CX':CX,'SourceI':ne.SOURCE_I_LOCAL}[key[0]],key[1])
        eq(CACHE[key].transpose().matmul(CACHE[key]),I,'all-column primitive '+repr(key))
    return CACHE[key]
def endpoint(w):
    V=I
    for g in w: V=gate(g).matmul(V)
    return V
U={name:endpoint(w) for name,w in words.items()}
inds=[j for j in range(D) if all(bits(j)[POS[x]]==0 for x in WORK+RECORD)]
P=sparse({(j,j):O for j in inds},(D,D)); M=sparse({(j,j):O for j in range(D) if j%8==0},(D,D)); gap=M-P
i=I.extract(range(D),inds); Q=dm(s.diag(*[int(bits(j)[POS[6]]==0) for j in inds])); I8=eye(8)
K={name:V.extract(inds,inds) for name,V in U.items()}
E={name:V.matmul(i).transpose().matmul(M).matmul(V.matmul(i)) for name,V in U.items()}
for name in ('post34','mirror34','prepared52','prepared52_alt'):
    eq(E[name],K[name].transpose().matmul(K[name]),'finite exact record/return on entire input '+name)
    need(gap.matmul(U[name].matmul(i)).is_zero_matrix,'all successful branches return '+name)
eq(K['post34'],Q.scalarmul(f(c)),'same original corner after single copy layer')
eq(K['prepared52_alt'],Q,'actual independent preparation changes corner to Q')
eq(E['prepared52_alt'],Q,'actual finite preparation changes the retained report law')
eq(U['post34'].matmul(i),U['old_two_sided37'].matmul(i),'same full initial isometry after deleting first copies')
need(not (U['post34'].matmul(U['post34'])-I).is_zero_matrix,'no reflection assumption for shorter word')
need(not (U['prepared52_alt'].matmul(U['prepared52_alt'])-I).is_zero_matrix,
     'whole alternative52 remains nonreflective; seed/copy do not commute on unused columns')
eq(E['copy_fault34'],Q,'same-clock real copy reversal loses query record')
eq(E['copy_fault34']-K['copy_fault34'].transpose().matmul(K['copy_fault34']),Q.scalarmul(f(1-c*c)),'actual finite copy fault has positive gap')
eq(K['copy_fault34'],K['post34'],'copy fault retains old corner: gap term cannot be erased')
for r in range(8):
    mr=sparse({(j,j):O for j in range(D) if j%8==r},(D,D))
    def ef(name):
        V=U[name].matmul(i); return V.transpose().matmul(mr).matmul(V)
    eq(ef('post34'),ef('mirror34'),'same actual record effect at fixed34 '+str(r))
need(not (U['post34'].matmul(i)-U['mirror34'].matmul(i)).is_zero_matrix,'same record fibre has different coherent work state')

# Full arbitrary endpoint cotangent identity, not sampled basis evidence.
inv=dm(s.diag(*[1/(az+z*c*c) if bits(j)[POS[6]]==0 else 1/az for j in inds]))
V=U['post34'].matmul(i); B0=V.matmul(inv).matmul(V.transpose())
CR=(B0.matmul(P)-P.matmul(B0)).scalarmul(f(-z))
CE=(B0.matmul(M)-M.matmul(B0)).scalarmul(f(-z))
eq(CR,CE,'all independent endpoint tangents have exact feedback/report source identity')
H=embed(s.Matrix([[0,-1],[1,0]]),(11,))
dU=U['post34'].matmul(H); dK=dU.extract(inds,inds)
dE=dU.matmul(i).transpose().matmul(M).matmul(V)+V.transpose().matmul(M).matmul(dU.matmul(i))
eq(dE,Q.scalarmul(f(2*c*u)),'independent upstream query comparison changes actual report')
source=-2*f(z)*tr(inv.matmul(K['post34'].transpose()).matmul(dK))*f(2)
need(source==f(-16*z*c*u/(az+z*c*c)),'true input-rank16 independent preparation source')
need(source!=Z,'upstream preparation was retained, not silently frozen')
suffix=I
for j in range(33,-1,-1):
    eq(suffix.transpose().matmul(CR).matmul(suffix),suffix.transpose().matmul(CE).matmul(suffix),'actual independent occurrence pullback '+str(j+1))
    suffix=suffix.matmul(gate(words['post34'][j]))
eq(suffix,U['post34'],'all suffix frames retain actual chronological order')

# Positive gap gives an exact finite excess. In this real code fault it is
# 8[-log(a+z c^2)] and is bounded by (z/a) Tr Delta including oldRIGHT.
mp.mp.dps=110; mp.iv.dps=95; iv=mp.iv
pp=(iv.sqrt(5)-1)/2; cc=pp**3; uu=2*pp*iv.sqrt(pp); zz=iv.mpf(1)/2**20; ab=1-zz; beta=2*pp*pp
def endpoints(x): return mp.mpf(x.a),mp.mpf(x.b)
def interval(x,places=48):
    fac=10**places; lo,hi=endpoints(x*fac)
    def fmt(k):
        sg='-' if k<0 else ''; k=abs(k); return sg+str(k//fac)+'.'+str(k%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
def bound(N):
    x=Fraction(2,55); q=x**N/math.factorial(N)
    return Fraction(176,359)/(1-x*x)*q/(1-q)**2
def ivrat(x): return iv.mpf(x.numerator)/x.denominator
a0=iv.mpf(json.loads(heat_b)['complete_book']['a0_interval'])
def heat(N):
    err=endpoints(ivrat(bound(N)))[1]
    return iv.log(N*65536*(2*a0+359))/beta+iv.mpf([-err,err])
J0=-8*iv.log(ab)-8*iv.log(ab+zz*cc*cc); J1=-8*iv.log(ab)
prices={}
for name in ('post34','prepared52','prepared52_alt','old_two_sided37'):
    N=len(words[name]); J=J1 if name=='prepared52_alt' else J0
    prices[name]={'N':N,'H':interval(heat(N)),'J':interval(J),'B':interval(heat(N)+J),
                 'full_modes':425*N*65536,'harmonic_modes':359*N*65536}
saving=iv.log(iv.mpf(37)/34)/beta
err=endpoints(ivrat(bound(34)+bound(37)))[1]; saving+=iv.mpf([-err,err])
deltaJ=J1-J0; err52=endpoints(ivrat(2*bound(52)))[1]; deltaB=deltaJ+iv.mpf([-err52,err52])
need(endpoints(saving)[0]>0,'actual37 costs strictly more than terminally identical34')
need(endpoints(deltaB)[1]<0,'actual same-clock52 preparation has strict full price decrease and changed report')
excess=-8*iv.log(ab+zz*cc*cc); excess_upper=8*zz*(1-cc*cc)/ab
need(endpoints(excess)[0]>0 and endpoints(excess_upper-excess)[0]>0,'full rank16 copy-fault excess and exact positive-gap upper bound')
need(bound(34)<Fraction(2,10**88) and bound(52)<Fraction(9,10**144),
     'outward rational envelopes of actual full-source remainders')
result={'status':'PASS','checks':len(CHECKS),'input_commit':'418afd58c','checker_sha256':sha(Path(__file__).read_bytes()),
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},'input_pins':pins,
 'boundary':{'wires':16,'old_right':[15],'fixed_work':WORK,'actual_existing_records':RECORD,'new_blanks':0,
             'active_dimension':512,'full_dimension':65536,'rank_input':16,'input_spectator':2,'thermal_spectator':128},
 'words':{name:{'length':len(w),'inventory':inventories[name],
          'sha256':sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode())} for name,w in words.items()},
 'exact':{'all_initial_states_same_34_37':True,'all_record_effects_equal_post34_mirror34':True,
          'post34_is_reflection':False,'all34_occurrence_feedback_record_identity':True,
          'prep52_base_corner':'p^3 Q','prep52_alt_corner':'Q','prep52_alt_changes_report':True,'prep52_alt_is_reflection':False,
          'copy_fault_gap':'(1-p^6)Q','fault_gap_excess':interval(excess),'fault_gap_excess_upper':interval(excess_upper)},
 'ambient_upstream_source':{'not_a_native_continuous_gate':True,'feedback':interval(-16*zz*cc*uu/(ab+zz*cc*cc)),
                             'full_heat_error_at_52_bound':str(bound(52))},
 'heat_source_bounds':{str(N):{'exact_rational':str(bound(N)),'scientific_approx':mp.nstr(mp.mpf(bound(N).numerator)/bound(N).denominator,20)} for N in (34,37,52)},
 'whole_price':prices,'B37_minus_B34':interval(saving),'B52_alt_minus_B52_base':interval(deltaB),
 'scope':{'literal_original_H_plus_J':True,'extra_Info_added':False,'native_grammar_membership_verified':True,
          'full_physical_X_N_identified':False,'finite_stationary_root_proved':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
