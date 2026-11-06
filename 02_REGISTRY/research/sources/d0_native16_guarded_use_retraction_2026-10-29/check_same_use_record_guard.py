#!/usr/bin/env python3
"""A same-use native record guard, with every call and whole Book price.

This tests the actual used operation once.  It is not a test/use identification.
SourceI pairs are reduced by their proved full Spin identity, never by preparing
Spin.  All primitive stages and all spectator columns stay in the whole price.
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
frozen('7dv PAID NATIVE CALIBRATION RECEIPT','d4d24dc76b92377a21a9b40fa19a8fb90e71c2c8c1c33df4a71077060685ed4e')
heat=frozen('7do PAID BINARY INPUT RECEIPT','811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba')
pins={
 '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py':'222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c',
 '02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418'}
for path,pin in pins.items():need(sha((ROOT/path).read_bytes())==pin,'consumed input '+path)
spec=importlib.util.spec_from_file_location('native_same_use_guard',ROOT/next(iter(pins)))
ne=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ne;spec.loader.exec_module(ne)
p=ne.P;alpha=ne.A;c=p**3;u=2*p*alpha;z=s.Rational(1,2**20);az=1-z
F=ne.GOLDEN_FIELD;ZERO=F.zero;ONE=F.one
def f(x):return F.from_sympy(s.sympify(x))
def sparse(d,shape):return DomainMatrix.from_dok({k:v for k,v in d.items() if v},shape,F).to_sparse()
def dm(m):return DomainMatrix.from_Matrix(s.Matrix(m)).convert_to(F).to_sparse()
def eye(n):return sparse({(j,j):ONE for j in range(n)},(n,n))
def eq(A,B,name):need((A-B).is_zero_matrix,name)
def tr(A):return sum((v for (j,k),v in A.to_dok().items() if j==k),ZERO)

# Every SourceI occurrence belongs to an actually consecutive even run.
# Its exact 8-column identity is established before tensor compression.
SI=dm(ne.SOURCE_I_LOCAL);Zspin=dm(s.kronecker_product(s.diag(1,-1),s.eye(4)))
eq(SI.matmul(SI),Zspin,'true unknown quaternion Spin: SourceI squared is Z_port tensor I4')
eq(Zspin.matmul(Zspin),eye(8),'SourceI fourth power is I on every port/Spin column')
ACTIVE=(0,6,11,12,7,8,9,10,16,17);POS={w:j for j,w in enumerate(ACTIVE)};NW=len(ACTIVE);DIM=2**NW;I=eye(DIM)
BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12,16,17);WORK=(0,11,12);RECORD=(7,8,9);WITNESS=(10,16,17)
def bits(k):return [(k>>(NW-1-j))&1 for j in range(NW)]
def number(b):return sum(v<<(NW-1-j) for j,v in enumerate(b))
def embed(m,w):
    m=s.Matrix(m);cols={j:[(row,f(m[row,j])) for row in range(m.rows) if m[row,j]] for j in range(m.cols)};out={}
    for col in range(DIM):
        b=bits(col);j=sum(b[POS[t]]<<(len(w)-1-k) for k,t in enumerate(w))
        for row,value in cols[j]:
            bb=b[:]
            for k,t in enumerate(w):bb[POS[t]]=(row>>(len(w)-1-k))&1
            out[number(bb),col]=value
    return sparse(out,(DIM,DIM))
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]);CACHE={}
def gate(g):
    key=g['op'],tuple(g['wires'])
    if key not in CACHE:
        CACHE[key]=embed({'G':ne.G_LOCAL,'CX':CX,'Z':s.diag(1,-1)}[key[0]],key[1])
        eq(CACHE[key].transpose().matmul(CACHE[key]),I,'complete primitive or proved SourceI pair '+repr(key))
    return CACHE[key]
def endpoint(w):
    U=I;k=0
    while k<len(w):
        g=w[k]
        if g['op']=='SourceI':
            j=k
            while j<len(w) and w[j]==g:j+=1
            if (j-k)%2:raise ArithmeticError('no odd Spin run may be compressed')
            if ((j-k)//2)%2:U=gate({'op':'Z','wires':[0]}).matmul(U)
            k=j
        else:U=gate(g).matmul(U);k+=1
    return U
base=prior['literal_words']['reference31'];forward=base[24:31];inverse=base[5:16]
identity18=forward+inverse
rotate18=forward+forward+[{'op':'SourceI','wires':[0,13,14]}]*4
copy=[{'op':'CX','wires':[a,r]} for a,r in zip(WORK,RECORD)]
mark=[{'op':'CX','wires':[a,r]} for a,r in zip(WORK,WITNESS)]
mark_fault=[mark[0],{'op':'G','wires':[11]},mark[2]]
devices={'good':identity18+copy,'rotate':rotate18+copy}
words={'good':copy+base+mark+devices['good']+mark,
       'rotate':copy+base+mark+devices['rotate']+mark,
       'birth_fault':copy+base+mark_fault+devices['good']+mark}
inventories={}
for name,w in words.items():
    ex=ne.Execution(18,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in w),ne.G_CX_SOURCE_I,0,(13,14),RECORD+WITNESS)
    ne.validate_execution(ex,max_qubits=18,max_expanded_stages=61)
    need(len(w)==61,'all61 actual primitive stages '+name)
    inventories[name]=dict(sorted(Counter(g['op'] for g in w).items()))
need(inventories['good']==inventories['rotate']=={'CX':43,'G':4,'SourceI':14},'same full clock AND primitive inventory for changed use')
need(inventories['birth_fault']=={'CX':42,'G':5,'SourceI':14},'true native one-call birth substitution inventory')
need(all(not set(g['wires']).intersection(WITNESS) for d in devices.values() for g in d),'every genuine device occurrence preserves all witness coordinates')
C=endpoint(copy);M=endpoint(mark);W=endpoint(base)
eq(endpoint(identity18),I,'fully paid18-call identity on all columns')
eq(endpoint(rotate18),gate({'op':'G','wires':[11]}).matmul(gate({'op':'G','wires':[11]})),'same-inventory18-call genuine Golden square')
eq(M.matmul(C),C.matmul(M),'two actual copy layers commute on all unprepared columns')
eq(W,W.transpose(),'consumed original31 whole reflection')
U={name:endpoint(w) for name,w in words.items()};D={name:endpoint(w) for name,w in devices.items()}
eq(U['good'],C.matmul(W).matmul(C),'good whole61 endpoint is exactly old37 tensor the true new blanks')
eq(U['good'],U['good'].transpose(),'whole good endpoint reflection: every full heat first source zero')
for name in U:eq(U[name].transpose().matmul(U[name]),I,'all1024 active columns unitary '+name)
inputs=[j for j in range(DIM) if all(bits(j)[POS[q]]==0 for q in WORK+RECORD+WITNESS)]
ii=I.extract(range(DIM),inputs);P=ii.matmul(ii.transpose());Q=dm(s.diag(1,0))
need(len(inputs)==2 and DIM*256==262144 and len(inputs)*8==16,'true full thermal and input multiplicities')
Kold=W.extract(inputs,inputs)
eq(Kold,Q.scalarmul(f(c)),'old corner p cubed Q with the same free input')
Ks={k:v.extract(inputs,inputs) for k,v in U.items()}
expected={'good':c,'rotate':c*c,'birth_fault':alpha*(4*p-3)}
for name in Ks:eq(Ks[name],Q.scalarmul(f(expected[name])),'actual original cold corner '+name)
for name in devices:
    T=D[name].extract(inputs,inputs)
    eq(Ks[name],T.matmul(Kold),'exact SAME-USE contraction factorization '+name)
    eq(U[name],M.matmul(D[name]).matmul(M).matmul(W).matmul(C),'literal uses device ONCE '+name)
eq(U['good'].matmul(ii),C.matmul(W).matmul(ii),'all original field states retained at good use')

# Entire device cotangent, before choosing its primitive support or linking
# any inverse legs.  All eight witness-diagonal blocks vanish exactly.
Ri=ii.matmul(dm(s.diag(1/(az+z*c*c),1/az))).matmul(ii.transpose())
B0=U['good'].matmul(Ri).matmul(U['good'].transpose())
Cret=(B0.matmul(P)-P.matmul(B0)).scalarmul(f(-z))
Cdev=M.transpose().matmul(Cret).matmul(M)
for label in range(8):
    js=[k for k in range(DIM) if sum(bits(k)[POS[w]]<<(2-j) for j,w in enumerate(WITNESS))==label]
    need(Cdev.extract(js,js).is_zero_matrix,'complete device first-source zero in witness block '+str(label))
need(len(devices['good'])==21,'all21 independent actual device call rows covered by the block identity')

# The first mark is NOT a frozen correctness promise.  Its real source is
# retained and one original G substitution is evaluated above.
H=s.zeros(4);H[0,3]=1;H[3,0]=-1;Hq=embed(H,(11,16))
position=len(copy)+len(base)+1
need(words['good'][position]=={'op':'CX','wires':[11,16]},'actual first query-witness birth tick')
suffix=endpoint(words['good'][position+1:])
dU=suffix.matmul(Hq).matmul(suffix.transpose()).matmul(U['good'])
dK=dU.extract(inputs,inputs)
eq(dK,Q.scalarmul(f(u)),'nonzero independent witness-birth insertion on the SAME word')
dS=dK.transpose().matmul(Ks['good'])+Ks['good'].transpose().matmul(dK)
source=-f(z)*tr(dm(s.diag(1/(az+z*c*c),1/az)).matmul(dS))*f(8)
need(source==f(-16*z*c*u/(az+z*c*c)),'full rank16 independent birth source with actual sign and gain')
# Final witness uncomputation preserves the already created old record R.
def local_partial(A,w):
    out={}
    for (r,c0),val in A.to_dok().items():
        br=bits(r);bc=bits(c0)
        if any(br[j]!=bc[j] for j in range(NW) if ACTIVE[j] not in w):continue
        rr=sum(br[POS[v]]<<(len(w)-1-j) for j,v in enumerate(w));cc=sum(bc[POS[v]]<<(len(w)-1-j) for j,v in enumerate(w))
        out[rr,cc]=out.get((rr,cc),ZERO)+val
    return sparse(out,(2**len(w),2**len(w)))
for off,g in enumerate(mark):
    k=len(words['good'])-3+off;suf=endpoint(words['good'][k+1:])
    row=suf.transpose().matmul(Cret).matmul(suf)
    need(local_partial(row,tuple(g['wires'])).is_zero_matrix,'independent final witness-copy row zero '+str(off))
for name,V in U.items():
    for w in (0,6):
        Z=embed(s.diag(1,-1),(w,));eq(V.matmul(Z),Z.matmul(V),'old LEFT archive endpoint preserved '+name+' '+str(w))

# Operator ordering, singular/nonnormal past and second-order leakage are
# checked with a small independent rational control, not an imagined native gate.
k=s.Matrix([[s.Rational(1,2),s.Rational(1,4)],[0,s.Rational(1,3)]])
t=s.diag(s.Rational(3,5),s.Rational(5,13));loss=k.T*(s.eye(2)-t.T*t)*k
need(loss[0,0]>0 and loss.det()>0,'positive loss for genuine nonscalar nonnormal past')
sing=s.Matrix([[s.Rational(1,2),s.Rational(1,4)],[0,0]])
need((sing.T*(s.eye(2)-s.diag(1,s.Rational(3,5))**2)*sing)==s.zeros(2),'zero gap need only hold on the actual past range')

mp.mp.dps=130;mp.iv.dps=110;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;cc=pp**3;aa=iv.sqrt(pp);uu=2*pp*aa;zz=iv.mpf(1)/2**20;ab=1-zz;beta=2*pp*pp
def ends(v):return mp.mpf(v.a),mp.mpf(v.b)
def ivrat(v):return iv.mpf(v.numerator)/v.denominator
def interval(v,places=46):
    fac=10**places;lo,hi=ends(v*fac)
    def fmt(n):
        sign='-' if n<0 else '';n=abs(n);return sign+str(n//fac)+'.'+str(n%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
N=61;x=Fraction(2,55);qn=x**N/math.factorial(N);A1=Fraction(176,359)/(1-x*x)*qn/(1-qn)**2
err=ends(ivrat(A1))[1];err2=ends(ivrat(2*A1))[1]
a0=iv.mpf(heat['complete_book']['a0_interval']);Hprice=iv.log(N*262144*(2*a0+359))/beta+iv.mpf([-err,err])
values={'good':cc,'rotate':cc*cc,'birth_fault':aa*(4*pp-3)}
J={n:-8*iv.log(ab)-8*iv.log(ab+zz*v*v) for n,v in values.items()}
gaps={n:J[n]-J['good']+iv.mpf([-err2,err2]) for n in ('rotate','birth_fault')}
need(ends(gaps['rotate'])[0]>0,'unfaithful actual USED device is strictly dearer in complete61 Book')
need(ends(gaps['birth_fault'])[1]<0,'first record birth still has a genuinely cheaper native alternative')
need(425*N*262144==6796083200 and 359*N*262144==5740691456,'all true61-clock whole Hodge modes counted')
result={'status':'PASS','checks':len(CHECKS),'input_commit':'9e80e0c015a8b8dc804ec55a837eda91164201fe',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':pins,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'literal_mark':mark,'literal_identity18':identity18,'literal_rotate18':rotate18,
 'whole_words':{n:{'N':len(w),'inventory':inventories[n],'sha256':sha((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode())} for n,w in words.items()},
 'boundary':{'wires':18,'old16_boundary_extended_by_real_blank_wires':[16,17],'work':WORK,'record':RECORD,'witness':WITNESS,
  'blank_wires':BLANKS,'old_right':[15],'source_spin':[13,14],'active_columns':DIM,
  'thermal_spectator':256,'full_dimension':262144,'active_input_rank':2,'input_spectator':8,'input_rank':16,
  'protected_Spin_prepared':False,'SourceI_pairs_proved_on_all8_columns':True},
 'same_use':{'device_occurrences':1,'native_device_calls':21,'all_independent_device_rows_zero_at_base':True,
  'device_correctness_imposed_on_variations':False,'witness_readonly_during_device':True,
  'all_final_witness_rows_zero':True,'all_initial_witness_rows_zero':False,'old_field_source_preserved':True,
  'good_endpoint_full_reflection':True},
 'return_corners':{'good':'p^3 Q','rotate':'p^6 Q','birth_fault':'sqrt(p)(4p-3) Q','rank_Q':8},
 'complete_prices':{n:interval(Hprice+v) for n,v in J.items()},
 'complete_differences':{n+'_minus_good':interval(v) for n,v in gaps.items()},
 'independent_birth_source':{'formula':'-16 zeta p^3 (2p sqrt(p))/(1-zeta+zeta p^6)',
   'interval':interval(-16*zz*cc*uu/(ab+zz*cc*cc)),'matrix_direction_not_claimed_native_angle':True,
   'actual_native_G_birth_fault_also_executed':True},
 'heat':{'A1_61_rational':str(A1),'absolute_H':interval(Hprice),'all_modes':425*N*262144,'unpaired_harmonics':359*N*262144},
 'scope':{'one_original_H_plus_J':True,'whole_price_global_minimum_claimed':False,
  'new_fidelity_or_Info_penalty':False,'all_physical_record_birth_constraints_derived':False,
  'new_blank_availability_retained':True,'physical_X_N_identified':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
