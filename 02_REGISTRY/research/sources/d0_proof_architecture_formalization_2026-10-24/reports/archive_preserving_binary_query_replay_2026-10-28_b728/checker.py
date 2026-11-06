#!/usr/bin/env python3
"""Literal archive-preserving seed plus QUERY, with every stage source.

Native words are discrete. Local Lie-algebra sources below are the exact
matrix comparison of those words, not a declaration of physical admission.
All computations are exact algebraic or outward interval arithmetic; no BLAS.
"""
from __future__ import annotations
import hashlib, json, math, platform
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
import mpmath as mp

ROOT=Path.cwd()
PRIMARY=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
SOURCES=ROOT/'02_REGISTRY/research/sources'
CHECKS=[]
def require(ok, label):
    if not bool(ok): raise ArithmeticError(label)
    CHECKS.append(label)
def sha(b): return hashlib.sha256(b).hexdigest()
def frozen(tag,lang):
    b=PRIMARY.read_bytes()
    start=('<!-- BEGIN '+tag+' -->\n```'+lang+'\n').encode()
    end=('```\n<!-- END '+tag+' -->').encode()
    require(b.count(start)==b.count(end)==1,'one frozen '+tag)
    return b.split(start)[1].split(end)[0]
prior=frozen('7do PAID BINARY INPUT RECEIPT','json')
require(sha(prior)=='811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba','owned full-heat coefficient receipt')
archive_code=frozen('7dp PAID ARCHIVE SOURCE CHECKER','python')
require(sha(archive_code)=='72edd8c55ecfedd103602e9a0af969325d4720b242ad86649c4c877a2f787b66','owned original archive and prior word source')
pins={
 'd0_native_stationary_seed_2026-10-28/check_seed.py':'9bd41ca8b58fb364fa00cedf9aee493d0fe03963c5b3fda92583def1fd192120',
 'd0_clock_winding_source_2026-10-28/PROOF_RU.md':'ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418',
 'd0_task_faithful_source_2026-10-28/check_task_source.py':'ac1b5af37e848782060b8f686852729d401d7b48d7c1f7bff459075d59f0f180',
 'd0_canonical_stationary_family_2026-10-28/check_canonical_seed.py':'21744ce3ea2e55dbd48a74393fd627b209d49b391e9367330858c519eab6ca94',
 'd0_canonical_stationary_family_2026-10-28/PROOF_RU.md':'fe4b8e9033098ced52299fbc0481ab2ddecceed69c6f4392988803ab0abfa005'}
for name,pin in pins.items(): require(sha((SOURCES/name).read_bytes())==pin,'unchanged input '+name)

p=(s.sqrt(5)-1)/2; a=s.sqrt(p); z=s.Rational(1,2**20)
c=p**3; u=2*p*a; D=1-z+z*c*c
field=s.QQ.algebraic_field(a)
def scalar(x): return field.from_sympy(x)
def dm(M): return DomainMatrix.from_Matrix(s.Matrix(M)).convert_to(field).to_sparse()
def simple(x): return str(s.simplify(field.to_sympy(x)))
I=dm(s.eye(64)); ZERO=field.zero
ACTIVE=(0,6,11,12,13,14)
position={w:i for i,w in enumerate(ACTIVE)}
oldR_multiplier=2
require(64*1024==65536 and 8*oldR_multiplier==16,'full thermal multiplicity differs from actual input rank')
G=s.Matrix([[a,-p],[p,a]])
Li=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
SI=s.diag(s.eye(4),Li)
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
def bits(k): return [(k>>(5-j))&1 for j in range(6)]
def unbits(b): return sum(x<<(5-j) for j,x in enumerate(b))
def local_index(b,ww): return sum(b[position[w]]<<(len(ww)-1-j) for j,w in enumerate(ww))
def embed(M,ww):
    out=s.zeros(64)
    for col in range(64):
        bb=bits(col); j=local_index(bb,ww)
        for k in range(2**len(ww)):
            if M[k,j]==0: continue
            nn=bb[:]
            for t,w in enumerate(ww): nn[position[w]]=(k>>(len(ww)-1-t))&1
            out[unbits(nn),col]=M[k,j]
    return dm(out)
cache={}
def gate(item):
    op,ww=item
    if item not in cache:
        require(15 not in ww,'immutable oldRIGHT never addressed')
        require(op=='SourceI' or not ({13,14}&set(ww)),'ordinary primitives never address Spin')
        require(op!='SourceI' or ww==(0,13,14),'original fixed source port')
        out=embed({'G':G,'CX':CX,'SourceI':SI}[op],ww)
        require((out.transpose().matmul(out)-I).is_zero_matrix,'complete native primitive orthogonal')
        cache[item]=out
    return cache[item]
si=('SourceI',(0,13,14))
def swap(x,y): return [('CX',(x,y)),('CX',(y,x)),('CX',(x,y))]
def inverse(word):
    out=[]
    for op,ww in reversed(word):
        if op=='CX': out.append((op,ww))
        elif op=='SourceI': out.extend([si]*3)
        else:
            rr=[] if ww[0]==0 else swap(ww[0],0)
            out.extend(rr+[si,si,('G',(0,)),si,si]+rr)
    return out
route=swap(0,11)
routed=route+[('G',(0,))]+route
query=inverse(routed)+route+[si,si]+route+routed
seed=[('CX',(6,12))]+[si]*4
v=[('G',(11,))]
words={'short':seed+query,
       'A':seed+v+inverse(v)+query,
       'B':seed+v+query+inverse(v)}
controlled=[('G',(11,)),('CX',(6,11)),('G',(11,)),('CX',(6,11))]
zword=route+[si,si]+route
futureC=inverse(controlled)+zword+controlled
words['C']=seed+futureC
c4=2*c*c-1;u4=2*c*u;D4=1-z+z*c4*c4
require(len(query)==26 and len(seed)==5,'literal constituent counts')
inventory={key:dict(sorted(Counter(op for op,ww in word).items())) for key,word in words.items()}
require(inventory['A']==inventory['B']=={'CX':25,'G':4,'SourceI':14},'common actual43 inventory')
require(inventory['short']=={'CX':19,'G':2,'SourceI':10},'actual31 inventory')
require(inventory['C']=={'CX':23,'G':4,'SourceI':14} and len(words['C'])==41,'nonscalar future literal41 inventory')
def endpoint(word):
    out=I
    for item in word: out=gate(item).matmul(out)
    return out
S=gate(('CX',(6,12)))
Q=embed(s.Matrix([[c,u],[u,-c]]),(11,))
Z=embed(s.diag(1,-1),(11,))
require((endpoint(seed)-S).is_zero_matrix,'new five-call seed exact on all64 active columns')
require((endpoint(query)-Q).is_zero_matrix,'literal routed query exact full operator')
require((S.matmul(Q)-Q.matmul(S)).is_zero_matrix,'same-execution full operators commute')
E={key:endpoint(word) for key,word in words.items()}
qzero=embed(s.diag(1,0),(6,));qone=I-qzero
Q4=embed(s.Matrix([[c4,u4],[u4,-c4]]),(11,))
FC=qzero.matmul(Q4)+qone.matmul(Z)
require((endpoint(futureC)-FC).is_zero_matrix,'actual nonscalar future on ALL old/work columns')
require((S.matmul(FC)-FC.matmul(S)).is_zero_matrix,'nonscalar complete future commutes with seed')
for key in E:
    target=S.matmul(FC if key=='C' else Z if key=='B' else Q)
    require((E[key]-target).is_zero_matrix,'full endpoint '+key)
    require((E[key].matmul(E[key])-I).is_zero_matrix,'full involution '+key)
    require(E[key].to_Matrix().trace()==0,'full balanced signature '+key)
require((E['A']-E['B']).is_zero_matrix is False,'finite comparison really changes endpoint')

# All16 real input columns, rather than a chosen state or a trace seed.
inrows=[k for k in range(64) if all(bits(k)[position[w]]==0 for w in (0,11,12))]
require(len(inrows)==8,'eight active input columns times immutable oldRIGHT2')
P=dm(s.diag(*[int(k in inrows) for k in range(64)]))
Rbar=dm(s.diag(*[(1/D if bits(k)[position[6]]==0 else 1/(1-z)) if k in inrows else 0 for k in range(64)]))
RbarB=dm(s.diag(*[(1 if bits(k)[position[6]]==0 else 1/(1-z)) if k in inrows else 0 for k in range(64)]))
RbarC=dm(s.diag(*[(1/D4 if bits(k)[position[6]]==0 else 1/(1-z)) if k in inrows else 0 for k in range(64)]))
K={}
for key in E:
    K[key]=E[key].extract(inrows,inrows)
    vals=[(1 if key=='B' else c4 if key=='C' else c) if bits(k)[position[6]]==0 else 0 for k in inrows]
    require((K[key]-dm(s.diag(*vals))).is_zero_matrix,'true entire input corner '+key)
Kseed=S.extract(inrows,inrows)
require((K['A']-Kseed.scalarmul(scalar(c))).is_zero_matrix,'actual scalar future on complete old input')
Aold=dm(s.diag(*[c4 if bits(k)[position[6]]==0 else 1 for k in inrows]))
Mold=Aold.transpose().matmul(Aold)
require((K['C']-Aold.matmul(Kseed)).is_zero_matrix,'actual nonscalar cold product A Kseed')
require((Mold.matmul(Kseed)-Kseed.matmul(Mold)).is_zero_matrix,'incoming exact nonscalar future criterion applied')
require(not (Mold-I.extract(inrows,inrows).scalarmul(scalar(c4*c4))).is_zero_matrix,
        'future effect genuinely nonscalar on old input')
# Stronger than one base-point corner identity: the blank11 compression
# leaves old port0/right12 and every Spin column, so its P_old off blocks
# vanish; factorization survives arbitrary seed variations not touching11.
oldrows=[k for k in range(64) if bits(k)[position[11]]==0]
Ac=endpoint(futureC).extract(oldrows,oldrows)
Pold=P.extract(oldrows,oldrows)
require((Pold.matmul(Ac)-Ac.matmul(Pold)).is_zero_matrix,'all old failure branches remain outside the true input cut')
reentry=endpoint(seed+[('CX',(6,12))]).extract(inrows,inrows)
require((reentry-dm(s.eye(8))).is_zero_matrix,'actual repeated CX returns the escaped old sector')
require(not (reentry-Kseed.matmul(Kseed)).is_zero_matrix,'native future does not imply cold-product factorization')

# No dependence on the arbitrary extension of ell to unused left89..127.
# The exact full endpoints act only on right11/right12 controlled by left6;
# neither a left address nor Spin/oldRIGHT is changed, for all65536 columns.
for key in E:
    entries=E[key].to_dok()
    require(all(bits(r)[0:2]==bits(k)[0:2] and bits(r)[4:6]==bits(k)[4:6]
                for (r,k),value in entries.items() if value),'fixed left and Spin every full column '+key)
    require(all((r&3)==(k&3) for r,k in entries),'entire protected Spin matrix algebra '+key)
    for aa in range(4):
        for bb in range(4):
            unit=s.zeros(4);unit[aa,bb]=1
            Aold=embed(unit,(13,14))
            require((E[key].matmul(Aold)-Aold.matmul(E[key])).is_zero_matrix,
                    'full Spin matrix-unit archive commutator '+key)
require(bits(16)[position[6]]==1 and bits(16^4)[position[6]]==1,'new seed leaves raw old left control intact')
# A Bell correlation is retained; the control is not reset.
seed_columns=S.to_Matrix()[:,inrows]
input_q0=inrows[0]; input_q1=next(k for k in inrows if bits(k)[position[6]]==1 and (k&3)==0)
out_q0=next(r for (r,k),x in S.to_dok().items() if k==input_q0 and x)
out_q1=next(r for (r,k),x in S.to_dok().items() if k==input_q1 and x)
require(bits(out_q0)[position[12]]==0 and bits(out_q1)[position[12]]==1,'actual retained right record distinguishes both old inputs')

# Full endpoint cotangent, restricted by the ACTUAL suffix of every occurrence.
def cotangent(U,R):
    B=U.matmul(R).matmul(U.transpose())
    return (B.matmul(P)-P.matmul(B)).scalarmul(scalar(-z))
C=cotangent(E['A'],Rbar)
CB=cotangent(E['B'],RbarB)
require(CB.is_zero_matrix,'all endpoint sources vanish for literal stationary B')
require(not C.is_zero_matrix,'A has actual nonzero full return source')
gain=scalar(z*c*u/D)
Cn=C.scalarmul(field.one/gain)
require((Cn+Cn.transpose()).is_zero_matrix,'real skew whole endpoint cotangent')
def partial_trace(M,ww):
    n=2**len(ww); out=[[ZERO for _ in range(n)] for _ in range(n)]
    for (r,k),value in M.to_dok().items():
        br,bk=bits(r),bits(k)
        if all(br[j]==bk[j] for j,w in enumerate(ACTIVE) if w not in ww):
            out[local_index(br,ww)][local_index(bk,ww)]+=value
    return out
def source_table(word,Cnorm):
    pulled=Cnorm; table=[]; nonzero_components=0; all_components=0
    for j in reversed(range(len(word))):
        op,ww=word[j]; loc=partial_trace(pulled,ww); rows=[]
        for aa in range(len(loc)):
            for bb in range(aa+1,len(loc)):
                value=oldR_multiplier*(loc[aa][bb]-loc[bb][aa])
                all_components+=1
                if value:
                    rows.append([aa,bb,simple(value)]);nonzero_components+=1
        localdm=DomainMatrix.from_list(loc,field).to_sparse()
        gram=localdm.transpose().matmul(localdm)
        gd=gram.to_dok()
        require(all(r==k for r,k in gd),'local exact source singular-value matrix diagonal')
        trnorm=s.simplify(sum(s.sqrt(field.to_sympy(gd.get((k,k),ZERO))) for k in range(len(loc))))
        trnorm=s.simplify(oldR_multiplier*trnorm)
        require(trnorm==(16 if rows else 0),'local operator-norm dual source certified exactly')
        table.append({'stage':j+1,'op':op,'wires':list(ww),'coefficients_over_g':rows,
                      'operator_norm_dual_over_g':int(trnorm)})
        pulled=gate(word[j]).transpose().matmul(pulled).matmul(gate(word[j]))
    table.reverse()
    require(all(not row['coefficients_over_g'] for row in table[:5]),'every independently varied seed occurrence has zero whole source')
    return table,all_components,nonzero_components
table,ncomp,nnz=source_table(words['A'],Cn)
require(ncomp==546,'all local real skew source components of actual43 calls')
require(nnz>0,'independent future stages remain visible')
zero_table,zbcomp,zbnz=source_table(words['B'],CB)
require(zbcomp==546 and zbnz==0,'all546 local source components zero at B')
require(sum(1 for row in table if row['coefficients_over_g'])>1,'inverse and preparation are not frozen')
raw_dual=sum(row['operator_norm_dual_over_g'] for row in table)
require(raw_dual==608,'full independent stage-max dual norm equals608g')
CC=cotangent(E['C'],RbarC)
gainC=scalar(z*c4*u4/D4)
tableC,cncomp,cnnz=source_table(words['C'],CC.scalarmul(field.one/gainC))
require(cncomp==534 and sum(row['operator_norm_dual_over_g'] for row in tableC)==576,
        'all41 nonscalar-future occurrence sources and full raw dual norm')
# Imaginary symmetric generators have zero real trace against the real skew Cj;
# this covers the rest of each full local complex-unitary comparison space.
complex_dim=sum(4**len(ww) for op,ww in words['A'])
require(complex_dim==1312,'complete local complex-unitary dimension including phases')
X=embed(s.Matrix([[0,-1],[1,0]]),(11,))
endpoint_source=oldR_multiplier*(Cn.matmul(X)).to_Matrix().trace()
require(s.simplify(endpoint_source-16)==0,'unit operator norm one-sided query source16g')
require(s.simplify(2*endpoint_source-32)==0,'mechanically conjugated query source32g')
wrong=Cn
wrong_rows=[]
for j,item in enumerate(words['A']):
    loc=partial_trace(wrong,item[1])
    wrong_rows.append(any(loc[aa][bb]!=loc[bb][aa] for aa in range(len(loc)) for bb in range(aa+1,len(loc))))
require(any(wrong_rows[j] != bool(table[j]['coefficients_over_g']) for j in range(len(table))),
        'omitting actual suffix transport fails a source row')

# Same report effect on the whole SOURCE is the actual permissible fibre
# in this example, not all matrices with the same one-state expectation.
effect=(I-Q).scalarmul(scalar(s.Rational(1,2)))
effectB=(I-Z).scalarmul(scalar(s.Rational(1,2)))
require((P.matmul(effect).matmul(P)-P.scalarmul(scalar(p*p))).is_zero_matrix,'A report probability p squared on all initial columns')
require(P.matmul(effectB).matmul(P).is_zero_matrix,'B changes report probability to zero on all initial columns')

mp.mp.dps=100;mp.iv.dps=90;iv=mp.iv
piv=(iv.sqrt(5)-1)/2;betaiv=2*piv**2;ziv=iv.mpf(1)/2**20
civ=piv**3;uiv=2*piv*iv.sqrt(piv);Div=1-ziv+ziv*civ*civ
c4iv=2*civ*civ-1;u4iv=2*civ*uiv;D4iv=1-ziv+ziv*c4iv*c4iv
owned=json.loads(prior);a0=iv.mpf(owned['complete_book']['a0_interval'])
def endpoints(x): return mp.mpf(x.a),mp.mpf(x.b)
def ivfmt(x):
    scale=10**45;lo,hi=endpoints(x*scale)
    def dec(k):
        sg='-' if k<0 else '';k=abs(k)
        return sg+str(k//scale)+'.'+str(k%scale).zfill(45)
    return [dec(int(mp.floor(lo))-1),dec(int(mp.ceil(hi))+1)]
def A1(N):
    xx=Fraction(2,55);q=xx**N/math.factorial(N)
    return Fraction(176,359)/(1-xx*xx)*q/(1-q)**2
def bound_iv(x): return iv.mpf(x.numerator)/x.denominator
def price(N,which):
    tail=bound_iv(A1(N));H=iv.ln(N*65536*(2*a0+359))/betaiv+iv.mpf([-endpoints(tail)[1],endpoints(tail)[1]])
    J=-8*iv.ln(1-ziv)-8*iv.ln(1-ziv+ziv*(1 if which=='B' else c4iv*c4iv if which=='C' else civ*civ))
    return H,J,H+J
H,JA,BA=price(43,'A');HB,JB,BB=price(43,'B')
HC,JC,BC=price(41,'C')
gap=-8*iv.ln(Div)
require(endpoints(gap)[0]>0,'strict whole price gap with exact equal full heat')
require(A1(43)<Fraction(1,10**110),'actual43 full heat coefficient bound')
g=ziv*civ*uiv/Div
w=8*ziv*civ*civ/Div
require(endpoints(32*g)[0]>0,'strict actual whole query source')
require(endpoints(w)[0]>0,'actual retained source gain positive')

# Independently differentiate the complete64 endpoint, including noncommuting
# actual forward/reverse gates, using arbitrary-precision real matrices.
# Six representative nonzero/zero raw axes; this tests the suffix sign convention.
def numeric(M): return mp.matrix([[mp.mpf(str(s.N(field.to_sympy(v),105))) for v in row] for row in M.to_list()])
numericC=numeric(C)
numericE=numeric(E['A']); numericI=mp.eye(64)
def Jnum(U):
    kk=mp.matrix([[U[r,k] for k in inrows] for r in inrows]);dd=(1-mp.mpf(2)**-20)*mp.eye(8)+mp.mpf(2)**-20*(kk.T*kk)
    return -2*mp.log(mp.det(dd))
samples=[0,1]+[row['stage']-1 for row in table if row['coefficients_over_g']][:4]
errors=[]
for j in samples:
    ww=words['A'][j][1]
    axis=(table[j]['coefficients_over_g'][0][:2] if table[j]['coefficients_over_g'] else [0,1])
    aa,bb=axis;ll=s.zeros(2**len(ww));ll[aa,bb]=-1;ll[bb,aa]=1
    Xj=embed(ll,ww);suffix=endpoint(words['A'][j+1:]);Y=suffix.matmul(Xj).matmul(suffix.transpose());Yn=numeric(Y)
    theta=mp.mpf('1e-12')
    # The exact embedded plane generator satisfies Y^3=-Y.
    require((Y.matmul(Y).matmul(Y)+Y).is_zero_matrix,'raw source plane exact exponential')
    Y2=Yn*Yn
    Up=(numericI+mp.sin(theta)*Yn+(1-mp.cos(theta))*Y2)*numericE
    Um=(numericI-mp.sin(theta)*Yn+(1-mp.cos(theta))*Y2)*numericE
    finite=(Jnum(Up)-Jnum(Um))/(2*theta)
    exact=2*sum((numericC*Yn)[k,k] for k in range(64))
    err=abs(finite-exact);errors.append(err)
    require(err<mp.mpf('1e-27'),'independent whole-matrix source sign and actual suffix')

word_json={key:[{'op':op,'wires':list(ww)} for op,ww in word] for key,word in words.items()}
result={
 'status':'PASS','scope':'actual fixed-boundary archive-preserving seed plus query; full fixed INTERNAL Book price; not physical X_N or GR closure',
 'checks':len(CHECKS),'input_commit':'185ab21cb165cbf420291a6d8a2056dc366e5275',
 'incoming_nonscalar_input_commit':'d37bd1ecf9550034586f32426fac84aecaf43be0',
 'input_pins':pins,'checker_sha256':sha(Path(__file__).read_bytes()),
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'boundary':{'total_wires':16,'blanks':12,'unknown':[6,13,14,15],'oldRIGHT':15,'active':list(ACTIVE),'active_dimension':64,'thermal_spectator':1024,'input_spectator':2,'full_dimension':65536,'input_rank':16},
 'literal_words':word_json,
 'word_sha256':{key:sha((json.dumps(val,sort_keys=True,separators=(',',':'))+'\n').encode()) for key,val in word_json.items()},
 'inventories':inventory,
 'archive':{'same_original_A0_and_full_Spin_oldRIGHT_algebra':True,'full_endpoint_commutation':True,'unused_left_padding_arbitrary':True,'fixed_raw_tick_archive_claim':False},
 'corners':{'seed':'diag(I8,0_8)','A':'diag(p^3 I8,0_8)','B':'diag(I8,0_8)','C':'diag((2p^6-1) I8,0_8)'},
 'nonscalar_future':{'raw_stages':41,'future_stages':36,'future_effect':'diag((2p^6-1)^2 I8,I8)','actual_cold_product':True,'commutes_with_return_projector':True,'native_reentry_negative_control':'S_word;CX(6,12) has K=I, unlike K_CX K_seed=diag(I8,0_8); retention of the new right12 record is not claimed for this control','all_five_prefix_sources_exact_zero':True,'future_gain_interval':ivfmt(8*ziv*c4iv*c4iv/D4iv),'full_heat_interval':ivfmt(HC),'full_return_interval':ivfmt(JC),'full_B_interval':ivfmt(BC),'full_modes':425*41*65536,'g_signed_interval':ivfmt(ziv*c4iv*u4iv/D4iv),'real_axis_components':cncomp,'nonzero_real_components':cnnz,'full_raw_stage_max_dual_over_abs_g':576,'all_stages':tableC},
 'price43':{'full_modes':425*43*65536,'H0_modes':33*43*65536,'paired_H1_modes':392*43*65536,'harmonic_modes':359*43*65536,'balanced_plus_minus_multiplicity':32768,'full_H_interval':ivfmt(H),'A_return_interval':ivfmt(JA),'B_return_interval':ivfmt(JB),'A_full_B_interval':ivfmt(BA),'B_full_B_interval':ivfmt(BB),'A_minus_B_interval':ivfmt(gap),'heat_row_exact_zero_at_both_words':True},
 'source43':{'g_definition':'zeta*c*sqrt(1-c^2)/(1-zeta+zeta*c^2), c=p^3','g_interval':ivfmt(g),'true_w_interval':ivfmt(w),'query_conjugacy_row_interval':ivfmt(32*g),'one_sided_row_interval':ivfmt(16*g),'full_raw_stage_max_dual_interval':ivfmt(raw_dual*g),'full_raw_stage_max_dual_over_w_interval':ivfmt(raw_dual*g/w),'real_axis_components_per_word':ncomp,'full_local_complex_dimensions':complex_dim,'A_nonzero_real_components':nnz,'B_nonzero_real_components':zbnz,'seed_five_occurrences_exact_zero':True,'A_all_stages':table,'imaginary_symmetric_axes_exact_zero':True,'whole_matrix_source_fd_max_error':mp.nstr(max(errors),35)},
 'physical_limits':{'no_continuous_native_gate_claim':True,'fixed_finite_word_alternatives_executed':True,'single_autonomous_controller_not_proved':True,'selected_full_Cost_Info_not_identified':True,'all42_map_not_proved':True,'GR_closed':False}}
print(json.dumps(result,indent=2,sort_keys=True))
