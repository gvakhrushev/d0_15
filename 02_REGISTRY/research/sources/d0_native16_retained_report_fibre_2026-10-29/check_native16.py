#!/usr/bin/env python3
"""A paid, retained QUERY report and the exact fixed-report control fibre.

Literal words, algebraic full-column operators, fixed-input return prices,
and matrix comparison sources are kept distinct. No physical X_N or GR claim.
"""
from __future__ import annotations
import hashlib,json,math,platform
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
def block(tag,language):
    b=PAPER.read_bytes();start=('<!-- BEGIN '+tag+' -->\n```'+language+'\n').encode();end=('```\n<!-- END '+tag+' -->').encode()
    require(b.count(start)==b.count(end)==1,'unique frozen '+tag)
    return b.split(start)[1].split(end)[0]
receipt=block('7dq ARCHIVE SEED QUERY RECEIPT','json')
require(sha(receipt)=='c1287748d2736c75959454ba716da5fab72e793848597e328322ed4e9e0790dd','literal previous complete-word receipt')
prior=json.loads(receipt)
heat_receipt=block('7do PAID BINARY INPUT RECEIPT','json')
require(sha(heat_receipt)=='811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba','unchanged full thermal coefficient')
PINS={
 'd0_task_faithful_source_2026-10-28/PROOF_RU.md':'9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5',
 'd0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md':'1db9ebd3d24b57a45b1a3a00a2c2553c2e08019cecc34d18e2e2a94d19b45254',
 'd0_canonical_stationary_family_2026-10-28/PROOF_RU.md':'fe4b8e9033098ced52299fbc0481ab2ddecceed69c6f4392988803ab0abfa005',
 'd0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for name,pin in PINS.items():require(sha((ROOT/'02_REGISTRY/research/sources'/name).read_bytes())==pin,'owned input '+name)
p=(s.sqrt(5)-1)/2;a=s.sqrt(p);c=p**3;z=s.Rational(1,2**20)
field=s.QQ.algebraic_field(a);Z0=field.zero
def f(x):return field.from_sympy(s.sympify(x))
def dm(m):return DomainMatrix.from_Matrix(s.Matrix(m)).convert_to(field).to_sparse()
def eq(A,B,label):require((A-B).is_zero_matrix,label)
ACTIVE=(0,6,10,11,12,13,14);POSITION={w:j for j,w in enumerate(ACTIVE)};DWORK=128
I=dm(s.eye(DWORK));I8=dm(s.eye(8))
G=s.Matrix([[a,-p],[p,a]]);Z=s.diag(1,-1)
Li=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
SI=s.diag(s.eye(4),Li)
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
def bits(k):return [(k>>(6-j))&1 for j in range(7)]
def number(b):return sum(v<<(6-j) for j,v in enumerate(b))
def local(b,w):return sum(b[POSITION[t]]<<(len(w)-1-j) for j,t in enumerate(w))
def embed(m,w):
    out=s.zeros(DWORK)
    for col in range(DWORK):
        b=bits(col);jj=local(b,w)
        for row in range(2**len(w)):
            if m[row,jj]==0:continue
            v=b[:]
            for j,t in enumerate(w):v[POSITION[t]]=(row>>(len(w)-1-j))&1
            out[number(v),col]=m[row,jj]
    return dm(out)
CACHE={}
def gate(g):
    op=g['op'];w=tuple(g['wires']);key=(op,w)
    if key not in CACHE:
        require(15 not in w,'immutable oldRIGHT never addressed')
        require(op=='SourceI' or not({13,14}&set(w)),'ordinary address acts outside Spin')
        require(op!='SourceI' or w==(0,13,14),'fixed original source port')
        M=embed({'G':G,'CX':CX,'SourceI':SI}[op],w)
        eq(M.transpose().matmul(M),I,'all-column native primitive orthogonal')
        CACHE[key]=M
    return CACHE[key]
def endpoint(word):
    out=I
    for g in word:out=gate(g).matmul(out)
    return out
base=prior['literal_words']['short'];require(len(base)==31,'literal previous31 calls')
seed=base[:5];pre=base[5:16];zw=base[16:24];post=base[24:]
require(len(pre)==11 and len(zw)==8 and len(post)==7,'actual forward middle inverse segmentation')
copy={'op':'CX','wires':[11,10]};g11={'op':'G','wires':[11]}
words={'unrecorded31':base,
       'recorded32':seed+pre+[copy]+zw+post,
       'low27':seed+pre+[copy]+[g11]+zw+[g11],
       'high27':seed+pre+[copy]+zw+[g11,g11],
       'completed16':seed+[copy]+zw+[g11,copy]}
inventories={k:dict(sorted(Counter(g['op'] for g in word).items())) for k,word in words.items()}
require(inventories['low27']==inventories['high27']=={'CX':14,'G':3,'SourceI':10},'actual equal27 resource inventory')
require(inventories['recorded32']=={'CX':20,'G':2,'SourceI':10},'one additional paid copy actual32 inventory')
require(inventories['completed16']=={'CX':9,'G':1,'SourceI':6} and len(words['completed16'])==16,
        'literal source-completing native16 inventory')
S=gate(seed[0]);Rq=embed(G,(11,));Zq=embed(Z,(11,));Ccopy=gate(copy)
eq(endpoint(pre),Rq.transpose(),'positive paid pre-readout G inverse')
eq(endpoint(post),Rq,'positive paid final G readback')
eq(endpoint(zw),Zq,'complete routed phase on all columns')
U={k:endpoint(word) for k,word in words.items()}
Frec=Rq.matmul(Zq).matmul(Ccopy).matmul(Rq.transpose())
eq(U['recorded32'],Frec.matmul(S),'actual full recorded endpoint')
eq(U['recorded32'].matmul(U['recorded32']),I,'recorded whole word remains involution')
eq(Frec.matmul(S),S.matmul(Frec),'real old/new full endpoints commute')
eq(U['low27'],Zq.matmul(Ccopy).matmul(Rq.transpose()).matmul(S),'low native task-fibre endpoint')
eq(U['high27'],Rq.matmul(Rq).matmul(U['low27']),'high differs only by live-query output unitary')
eq(U['completed16'],S.matmul(Ccopy).matmul(Rq).matmul(Zq).matmul(Ccopy),
   'complete native16 recording reflection on all128 columns')
eq(U['completed16'].matmul(U['completed16']),I,'completed full endpoint exact involution')
require(U['completed16'].to_Matrix().trace()==0,'completed full endpoint balanced signature')

inputs=[k for k in range(DWORK) if all(bits(k)[POSITION[w]]==0 for w in (0,10,11,12))]
require(len(inputs)==8 and DWORK*512==65536,'rank8 active times oldRIGHT2, full128 times512')
P=dm(s.diag(*[int(k in inputs) for k in range(DWORK)]))
Qinput=dm(s.diag(*[int(bits(k)[POSITION[6]]==0) for k in inputs]))
corners={k:U[k].extract(inputs,inputs) for k in U}
for name,amp in [('unrecorded31',c),('recorded32',p),('low27',a),('high27',a*c),('completed16',a)]:
    eq(corners[name],Qinput.scalarmul(f(amp)),'actual entire return corner '+name)
eq(U['completed16'].extract(list(range(DWORK)),inputs),U['low27'].extract(list(range(DWORK)),inputs),
   'completed16 has IDENTICAL whole terminal WORK isometry on actual input to low27')
Pi=embed(s.diag(0,1),(10,))
Pi_query=embed(s.diag(0,1),(11,))
prefix=endpoint(seed+pre+[copy])
event=prefix.transpose().matmul(Pi).matmul(prefix)
for name in ('recorded32','low27','high27'):
    eq(U[name].transpose().matmul(Pi).matmul(U[name]),event,'same actually retained report on ALL128 input columns '+name)
    eq(U[name].transpose().matmul(Pi).matmul(U[name]).extract(inputs,inputs),I8.scalarmul(f(p*p)),
       'actual original16 input report probability p squared '+name)
P_record_blank=I-Pi
eq(P_record_blank.matmul(prefix.transpose()).matmul(Pi).matmul(prefix).matmul(P_record_blank),
   P_record_blank.matmul(endpoint(seed+pre).transpose()).matmul(Pi_query).matmul(endpoint(seed+pre)).matmul(P_record_blank),
   'copy binds all64 SOURCE columns with the actual initial record blank to the middle test')
require(not (prefix.transpose().matmul(Pi).matmul(prefix)-
             endpoint(seed+pre).transpose().matmul(Pi_query).matmul(endpoint(seed+pre))).is_zero_matrix,
        'the report-blank hypothesis cannot be removed from the actual copying law')
eq(U['completed16'].transpose().matmul(Pi).matmul(U['completed16']).extract(inputs,inputs),
   I8.scalarmul(f(p*p)),'completed16 same actual retained report on all16 true input columns')

# Exact all-column fixed old archive, including Spin coherences.
for name in ('recorded32','low27','high27','completed16'):
    require(all(bits(r)[:2]==bits(k)[:2] for (r,k),v in U[name].to_dok().items() if v),
            'entire left address fixed at full endpoint '+name)
    for aa in range(4):
        for bb in range(4):
            e=s.zeros(4);e[aa,bb]=1;A=embed(e,(13,14))
            eq(U[name].matmul(A),A.matmul(U[name]),'complete old Spin matrix algebra '+name)

# Every single-wire matrix algebra outside live query11 is unchanged in the
# task fibre. These generate the ENTIRE other-six-wire active matrix algebra;
# the additional inactive wires/oldRIGHT are identities on both words.
for wire in ACTIVE:
    if wire==11:continue
    for aa in range(2):
        for bb in range(2):
            m=s.zeros(2);m[aa,bb]=1;A=embed(m,(wire,))
            eq(U['low27'].transpose().matmul(A).matmul(U['low27']),
               U['high27'].transpose().matmul(A).matmul(U['high27']),
               'all-input equality of retained joint observable generator')
require(not (U['low27'].transpose().matmul(Pi_query).matmul(U['low27'])-
             U['high27'].transpose().matmul(Pi_query).matmul(U['high27'])).is_zero_matrix,
        'live-query future remains distinguishable and is not erased')

# Whole generated prefix/cut recursion: no independently chosen cut at copy.
for name in ('recorded32','completed16'):
    T=I;Pj=P
    for j,g in enumerate(words[name]):
        Tn=gate(g).matmul(T);Pn=Tn.matmul(P).matmul(Tn.transpose())
        eq(Pn.matmul(gate(g)).matmul(Pj),gate(g).matmul(Pj),
           'true generated-cut zero interior leakage '+name)
        T,Pj=Tn,Pn
    eq(P.matmul(T.transpose()).matmul(I-P).matmul(T).matmul(P).extract(inputs,inputs),
       I8-corners[name].transpose().matmul(corners[name]),
       'actual closing feedback includes both copied records '+name)

# Full source completion before ANY choice of admissible tangent space.
# M records both old copy12=0 and new report10=0. Its measurable success
# contains P, and the actual native16 word saturates that operator bound.
Pi_seed=embed(s.diag(0,1),(12,));M=(I-Pi).matmul(I-Pi_seed)
GapProjector=M-P
eq(GapProjector.matmul(GapProjector),GapProjector,'retained-record success minus initial cut is a positive projector')
eq(P.matmul(M),P,'true fixed input cut is contained in the measurable joint success')
Winit=U['completed16'].extract(list(range(DWORK)),inputs)
require(GapProjector.matmul(Winit).is_zero_matrix,'all initialized success branches return: exact operator saturation')
Em=U['completed16'].transpose().matmul(M).matmul(U['completed16']).extract(inputs,inputs)
eq(Em,Qinput.scalarmul(f(p)),'actual joint-record effect p times old returning projector')
eq(Em,corners['completed16'].transpose().matmul(corners['completed16']),
   'return effect equals the observable joint-record effect on every actual input')
Em_rec=U['recorded32'].transpose().matmul(M).matmul(U['recorded32']).extract(inputs,inputs)
eq(Em_rec,Em,'actual recorded32 and completed16 have identical JOINT record effect on real input')
eq(Em_rec-corners['recorded32'].transpose().matmul(corners['recorded32']),
   Qinput.scalarmul(f(c)),'unsaturated recorded32 exact positive return gap is p cubed Q')
dp=1-z+z*p
Rcomp=dm(s.diag(*[(1/dp if bits(j)[POSITION[6]]==0 else 1/(1-z)) if j in inputs else 0 for j in range(DWORK)]))
Bcomp=U['completed16'].matmul(Rcomp).matmul(U['completed16'].transpose())
Creturn=(Bcomp.matmul(P)-P.matmul(Bcomp)).scalarmul(f(-z))
Cobservable=(Bcomp.matmul(M)-M.matmul(Bcomp)).scalarmul(f(-z))
eq(Creturn,Cobservable,'WHOLE endpoint covector equals the real retained-record source, not only a sampled tangent')
require(not Creturn.is_zero_matrix,'physical observable source is retained, not forced to zero off task')
lastComp=gate(copy)
Gwhere=next(j for j,g in enumerate(words['completed16']) if g['op']=='G')
Xs=lastComp.matmul(embed(s.Matrix([[0,-1],[1,0]]),(11,))).matmul(lastComp.transpose())
compSource=2*(Creturn.matmul(Xs)).to_Matrix().trace()
require(s.simplify(compSource-16*z*p*a/dp)==0,'actual original G occurrence source equals its paid report probability source')
eq(Creturn.matmul(embed(s.Matrix([[0,-1],[1,0]]),(11,))),
   Cobservable.matmul(embed(s.Matrix([[0,-1],[1,0]]),(11,))),
   'independent return rotation has the same full observable cotangent')
require(s.simplify((Creturn.matmul(embed(s.Matrix([[0,-1],[1,0]]),(11,)))).to_Matrix().trace())==0,
        'old independent same-record readback obstruction now vanishes exactly')
# Every actual stage source is the pullback of that ONE same effect source.
for j,g in enumerate(words['completed16']):
    suffix=endpoint(words['completed16'][j+1:])
    eq(suffix.transpose().matmul(Creturn).matmul(suffix),
       suffix.transpose().matmul(Cobservable).matmul(suffix),
       'actual occurrence retains full record-source identity')

# Same-field change after actually retaining the report, with the true trace.
t=s.symbols('t',positive=True);aa0=1-z;k=(1+t)/2
fold=-2*z*t/(aa0+z*t*t)
fnew=-z*k/(aa0+z*k*k)
mu=s.factor(k*(aa0+z*t*t)/(2*t*(aa0+z*k*k)))
require(s.cancel(fnew-mu*fold)==0,'exact positive all-field first-source transport on matched graph')
require(s.simplify((1+c)/2-p)==0,'actual retained report corner is (1+c)/2')

# Full occurrence/source restriction at the recorded centre, no echo linkage.
drec=1-z+z*p*p
Rbar=dm(s.diag(*[(1/drec if bits(j)[POSITION[6]]==0 else 1/(1-z)) if j in inputs else 0 for j in range(DWORK)]))
rot=U['recorded32'].matmul(Rbar).matmul(U['recorded32'].transpose())
Cj=(rot.matmul(P)-P.matmul(rot)).scalarmul(f(-z))
Jgen=embed(s.Matrix([[0,-1],[1,0]]),(11,))
actual_source=2*(Cj.matmul(Jgen)).to_Matrix().trace()
expected=16*z*p*p*a/drec
require(s.simplify(actual_source-expected)==0,'exact same-record final-readback source with actual oldRIGHT trace')
eq(Jgen.matmul(Pi),Pi.matmul(Jgen),'entire retained report effect stationary for the whole output-rotation curve')
for wire in ACTIVE:
    if wire==11:continue
    for aa in range(2):
        for bb in range(2):
            m=s.zeros(2);m[aa,bb]=1;A=embed(m,(wire,))
            eq(Jgen.matmul(A),A.matmul(Jgen),'same-record direction preserves every other live/old observable')
lastG=max(j for j,g in enumerate(words['recorded32']) if g['op']=='G')
suffix=endpoint(words['recorded32'][lastG+1:]);X0=embed(s.Matrix([[0,-1],[1,0]]),(0,))
eq(suffix.matmul(X0).matmul(suffix.transpose()),Jgen,'source belongs to actual final G occurrence')
# Old prefix: every original local unitary direction, including independent
# source calls, is annihilated after the literal recorded future.
old_rows=[]
for j in range(5):
    suffix=endpoint(words['recorded32'][j+1:]);localC=suffix.transpose().matmul(Cj).matmul(suffix)
    w=tuple(words['recorded32'][j]['wires']);n=2**len(w)
    out=[[Z0 for _ in range(n)] for _ in range(n)]
    for (r,col),v in localC.to_dok().items():
        br,bc=bits(r),bits(col)
        if all(br[q]==bc[q] for q,wire in enumerate(ACTIVE) if wire not in w):out[local(br,w)][local(bc,w)]+=v
    require(all(not v for row in out for v in row),'all old occurrence directions zero after actual record')
    old_rows.append(j+1)

# Exact spectrum proof of equal COMPLETE heat for the two27-call alternatives.
# The X_record eigenbasis gives one reflection and one rotation, respectively.
G2=dm(G);I2=dm(s.eye(2));Z2=dm(Z)
Lplus=Z2.matmul(G2.transpose());Lminus=G2.transpose()
Hplus=G2.matmul(G2).matmul(Z2).matmul(G2.transpose());Hminus=G2
lam=s.symbols('lambda')
for A in (Lplus,Hplus):
    eq(A.matmul(A),I2,'record-X plus block is exact reflection')
    require(A.to_Matrix().trace()==0,'record-X plus block balanced')
for A in (Lminus,Hminus):
    require(s.simplify(A.to_Matrix().trace()-2*a)==0 and s.simplify(A.to_Matrix().det()-1)==0,
            'record-X minus rotation has same characteristic polynomial')
polyL=dm(s.diag(Lplus.to_Matrix(),Lminus.to_Matrix())).charpoly()
polyH=dm(s.diag(Hplus.to_Matrix(),Hminus.to_Matrix())).charpoly()
require(polyL==polyH==[f(1),f(-2*a),f(0),f(2*a),f(-1)],'computed entire4-column future characteristic polynomials coincide')
require(s.simplify(U['recorded32'].to_Matrix().trace()-s.Rational(DWORK,4))==0,'recorded32 actual full signature5/8 plus3/8 minus')

# Nonscalar after-record criterion and explicit proof boundary.
b=s.Rational(1,3);Q=s.diag(1,0);C=s.Matrix([[0,b],[b,0]]);Cr=(s.eye(2)+C)/2
require(C*C*Q==Q*C*C,'old nonscalar future has zero prefix criterion')
require(Cr*Cr*Q!=Q*Cr*Cr,'retaining its report can create a prefix source across signs')

# Rigorous spectral/resolvent norm envelope for approximate scalar compilers.
# A small rational noncommuting case independently checks both exact gradients.
rr=4;qq=2;Q=s.diag(1,1,0,0);c0=s.Rational(3,5);eps=s.Rational(1,100)
E=s.Matrix([[0,0,1,0],[0,0,0,-1],[1,0,0,0],[0,-1,0,0]])
C=c0*s.eye(rr)+eps*E;Cr=(s.eye(rr)+C)/2
def gradient(C,half=False):
    emb=s.eye(rr)[:,:qq];DD=aa0*s.eye(qq)+z*(emb.T*C*C*emb);RB=emb*DD.inv()*emb.T
    return -z*(C*RB+RB*C)*(s.Rational(1,2) if half else 1)
mu0=mu.subs(t,c0);defect=gradient(Cr,True)-mu0*gradient(C)
L=(z/aa0)*(s.Rational(1,2)+2*mu0)*(1+2*z/aa0)
# The exact defect has identical2x2 blocks up to sign; Frobenius is a
# conservative bound for its operator norm, sufficient for this concrete check.
require(s.simplify(sum(v*v for v in defect)/(L*eps)**2)<1,'noncommuting actual return derivative obeys proved scalar-reference error bound')

mp.mp.dps=100;mp.iv.dps=90;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;av=iv.sqrt(pp);cv=pp**3;zz=iv.mpf(1)/2**20;beta=2*pp*pp;abar=1-zz
a0=iv.mpf(json.loads(heat_receipt)['complete_book']['a0_interval'])
def ends(x):return mp.mpf(x.a),mp.mpf(x.b)
def textiv(x,places=42):
    scale=10**places;lo,hi=ends(x*scale)
    def fmt(k):
        sign='-' if k<0 else '';k=abs(k);return sign+str(k//scale)+'.'+str(k%scale).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
def bound(N):
    x=Fraction(2,55);q=x**N/math.factorial(N)
    return Fraction(176,359)/(1-x*x)*q/(1-q)**2
mu_eff=(aa0+z*t*t)/(4*t*(aa0+z*(1+t)/2))
require(s.cancel(-z/(2*(aa0+z*(1+t)/2))-mu_eff*fold)==0,'derived effective scalar source ratio to owned unrecorded field source')
def Hinterval(N):
    q=bound(N);u=iv.mpf(q.numerator)/q.denominator
    return iv.ln(N*65536*(2*a0+359))/beta+iv.mpf([-ends(u)[1],ends(u)[1]])
def Jinterval(amp):return -8*iv.ln(abar)-8*iv.ln(abar+zz*amp*amp)
values={}
for name,amp in [('unrecorded31',cv),('recorded32',pp),('low27',av),('high27',av*cv),('completed16',av)]:
    n=len(words[name]);hh=Hinterval(n);jj=Jinterval(amp)
    values[name]={'N':n,'H_interval':textiv(hh),'J_interval':textiv(jj),'B_interval':textiv(hh+jj),
                 'all_modes':425*n*65536,'unpaired_harmonic_modes':359*n*65536}
delta=8*iv.ln((abar+zz*pp)/(abar+zz*pp**7))
source=16*zz*pp*pp*av/(abar+zz*pp*pp)
muv=(1+cv)*(abar+zz*cv*cv)/(4*cv*(abar+zz*((1+cv)/2)**2))
require(ends(delta)[0]>0 and ends(source)[0]>0 and ends(muv)[0]>0,'strict complete fixed-report gap and positive true graph transport')
require(bound(27)<Fraction(1,10**64),'actual finite thermal tail included')

# Independent direct finite differentiation of the actual remaining readback.
pv=(mp.sqrt(5)-1)/2;aa=mp.sqrt(pv);theta=mp.atan2(pv,aa);zv=mp.mpf(2)**-20
def ret_price(phi):return -8*mp.log1p(-zv)-8*mp.log1p(zv*((aa*mp.cos(phi))**2-1))
dt=mp.mpf('1e-14');num=(ret_price(theta+dt)-ret_price(theta-dt))/(2*dt)
analytic=16*zv*pv*pv*aa/(1-zv+zv*pv*pv)
err=abs(num-analytic);require(err<mp.mpf('1e-32'),'actual return derivative independent finite difference')

result={'status':'PASS','checks':len(CHECKS),'input_commit':'b728d85246c6bcf75b84dadaef294e91f5f50b15',
        'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':PINS,
        'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
        'scope':'same actual retained report and full old archive, full fixed INTERNAL Book H+J; no unconditional physical X_N or GR closure',
        'literal_words':words,'inventories':inventories,
        'word_sha256':{k:sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode()) for k,w in words.items()},
        'boundary':{'full_wires':16,'unknown':[6,13,14,15],'actual_blanks':12,'retained_new_report_wire':10,'live_query_wire':11,'old_copy_wire':12,'active_wires':ACTIVE,'active_dimension':128,'full_dimension':65536,'thermal_spectator':512,'input_spectator':2,'rank_input':16},
        'retained_report':{'all_initial16_event_effect':'p^2 I16','all64_SOURCE_columns_with_actual_record_blank_match_middle_test':True,'same_entire_other15_wire_output_channel_for_27_pair':True,'same_every_possible_future_context':False,'new_memory_not_erased':True},
        'whole_book':values,'exact_fixed_report_B_high_minus_low_interval':textiv(delta),
        'price_comparison_heat_exact_equal':True,'pair_future_charpoly':'(lambda^2-1)(lambda^2-2sqrt(p)lambda+1)',
        'recorded32_signature':{'+1':40960,'-1':24576},
        'source':{'paid_final_G_stage':lastG+1,'old_five_rows_exact_zero':old_rows,'same_all_other15_wire_task_tangent':True,'whole_heat_first_row_zero_at_recorded32':True,'nonzero_readback_source_interval':textiv(source),'exact_graph_gain_ratio_interval':textiv(muv),'old_gain':'8 zeta c^2/(1-zeta+zeta c^2)','new_gain':'8 zeta ((1+c)/2)^2/(1-zeta+zeta ((1+c)/2)^2)','old_w_interval':textiv(8*zz*cv*cv/(abar+zz*cv*cv)),'actual_recorded_w_interval':textiv(8*zz*pp*pp/(abar+zz*pp*pp)),'finite_difference_error':mp.nstr(err,35)},
        'nonscalar_recording':{'new_prefix_criterion':'[C,Q_return]=0 for Hermitian contraction C','old_C_squared_criterion_alone_insufficient':True},
        'approximate_graph':{'operator_gradient_defect_bound':'(zeta/a)*(1/2+2mu)*(1+2zeta/a)*epsilon','trace_direction_bound':'r times operator-gradient bound times ||D C||op; r is actual protected input rank','noncommuting_rational_control':True},
        'native_full_source_completion':{'literal_word':'completed16','same_entire_initialized_work_isometry_as':'low27','same_clock_as_low27':False,'joint_observable':'record10=0 AND seed-copy12=0','actual_joint_effect':'p Q_return','positive_return_gap_exact_zero':True,'full_H_first_source_zero_on_every_endpoint_unitary_tangent':True,'all_endpoint_source_equals_observable_pullback':True,'all16_occurrence_sources_equal_observable_pullback':True,'stationary_on_every_fixed_joint_record_effect_tangent':True,'stationarity_does_not_require_linked_inverse_legs':True,'unrestricted_source_not_zero':True,'native_G_stage':Gwhere+1,'actual_native_G_source_interval':textiv(16*zz*pp*av/(abar+zz*pp)),'return_minimum_at_fixed_joint_effect':True,'full_B_global_minimum_not_proved':True,'source_equivalent_positive_ratio_interval':textiv((abar+zz*cv*cv)/(4*cv*(abar+zz*(1+cv)/2))),'full_signature':{'+1':32768,'-1':32768},'actual_generated_prefix_cuts_verified':True,'same_joint_effect_as_recorded32':True,'recorded32_unsaturated_gap':'p^3 Q_return'},
        'remaining':{'full_physical_variation_domain':False,'autonomous_controller_admission':False,'full_selected_Cost_Info_binding':False,'all42_physical_source_and_refinement':False,'GR_closed':False}}
print(json.dumps(result,indent=2,sort_keys=True))
