#!/usr/bin/env python3
"""Exact first-copy cotangent retraction and paid upstream preparation.

Consumes the pinned 7dw matrix-engine prefix, not its previous test suite.
Every native stage remains present and paid. Matrix tangent tests are not
new continuously adjustable Golden primitives.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast, hashlib, json, math, platform
import sympy as s
import mpmath as mp

ROOT=Path.cwd()
PAPER=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
def pinned_block(tag,language,pin):
    b=PAPER.read_bytes(); start=('<!-- BEGIN '+tag+' -->\n```'+language+'\n').encode()
    end=('```\n<!-- END '+tag+' -->').encode()
    if b.count(start)!=1 or b.count(end)!=1: raise ArithmeticError('ambiguous '+tag)
    raw=b.split(start)[1].split(end)[0]
    if hashlib.sha256(raw).hexdigest()!=pin: raise ArithmeticError('changed '+tag)
    return raw

helper_pin='e3ac0eb35ec9c4043cf51485f36d3145be3f9be988e28d38330c510599906fc3'
helper_raw=pinned_block('7dw SAME USE RECORD GUARD CHECKER','python',helper_pin)
tree=ast.parse(helper_raw); prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='base' for t in node.targets): break
    prefix.append(node)
else: raise ArithmeticError('missing pinned helper boundary')
ns={'__name__':'pinned_7dw_helpers'}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(PAPER)+'#7dw-helpers','exec'),ns)
names=('need sha frozen prior heat pins ne p alpha c u z az F ZERO ONE f sparse dm eye eq tr '
       'ACTIVE POS NW DIM I BLANKS WORK RECORD WITNESS bits number embed gate endpoint CHECKS').split()
globals().update({name:ns[name] for name in names})
guard_pin='5c183ebfa85ab0550dd5ae3caefaeb38281e5a40d45c1d8ec0e2343f6c49330c'
guard=frozen('7dw SAME USE RECORD GUARD RECEIPT',guard_pin)

base=prior['literal_words']['reference31']
copy=[{'op':'CX','wires':[a,r]} for a,r in zip(WORK,RECORD)]
mark=guard['literal_mark']; identity18=guard['literal_identity18']
good61=copy+base+mark+identity18+copy+mark
need(len(good61)==61,'exact previously owned61 word reconstructed')
need(sha((json.dumps(good61,sort_keys=True,separators=(',',':'))+'\n').encode())==guard['whole_words']['good']['sha256'],
     'reconstructed61 word has the published native hash')

# The new preparation really acts on the fresh witness16. Port0 and unknown
# Spin13,14 retain their old meanings; only the routed target11 changes.
def target16(word):
    return [{'op':g['op'],'wires':[16 if q==11 else q for q in g['wires']]} for g in word]
forward16=target16(base[24:31]); inverse16=target16(base[5:16])
prefix18=forward16+inverse16
rotate18=forward16+forward16+[{'op':'SourceI','wires':[0,13,14]}]*4
birth_fault61=list(good61)
birth_fault61[len(copy)+len(base)+1]={'op':'G','wires':[11]}
words={'good':prefix18+good61,'prepared_rotation':rotate18+good61,
       'birth_fault':prefix18+birth_fault61}
inventories={}
for name,w in words.items():
    ex=ne.Execution(18,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in w),
                    ne.G_CX_SOURCE_I,0,(13,14),RECORD+WITNESS)
    ne.validate_execution(ex,max_qubits=18,max_expanded_stages=79)
    need(len(w)==79,'all79 native stages '+name)
    inventories[name]=dict(sorted(Counter(g['op'] for g in w).items()))
need(inventories['good']==inventories['prepared_rotation']=={'CX':55,'G':6,'SourceI':18},
     'actual79 clock and primitive inventories match')
need(inventories['birth_fault']=={'CX':54,'G':7,'SourceI':18},
     'genuine one-call birth substitution retains actual inventory')
need(all(not set(g['wires']).intersection(RECORD) for g in prefix18),
     'every independent paid preparation call preserves old R')
eq(endpoint(prefix18),I,'paid new witness preparation identity on all active columns')
G16=gate({'op':'G','wires':[16]})
eq(endpoint(rotate18),G16.matmul(G16),'same inventory actual fresh witness G16 squared')

C=endpoint(copy); W=endpoint(base)
U={name:endpoint(word) for name,word in words.items()}
eq(U['good'],C.matmul(W).matmul(C),'full79 endpoint is old37 tensor unchanged new witness')
eq(U['good'],U['good'].transpose(),'all full INTERNAL heat first rows vanish at the base reflection')
for name,value in U.items(): eq(value.transpose().matmul(value),I,'whole1024 active columns unitary '+name)
inputs=[j for j in range(DIM) if all(bits(j)[POS[q]]==0 for q in WORK+RECORD+WITNESS)]
need(len(inputs)==2 and DIM*256==262144 and len(inputs)*8==16,'true thermal and protected input multiplicities')
ii=I.extract(range(DIM),inputs); P=ii.matmul(ii.transpose()); Q=dm(s.diag(1,0))
Ks={name:value.extract(inputs,inputs) for name,value in U.items()}
eq(Ks['good'],Q.scalarmul(f(c)),'original corner p cubed Q unchanged')
eq(Ks['prepared_rotation'],Q.scalarmul(f(c*c)),'fresh witness preparation changes actual corner to p sixth Q')
eq(Ks['birth_fault'],Q.scalarmul(f(alpha*(4*p-3))),
   'same79 native birth alternative retains its actual original cold corner')
Zinv=dm(s.diag(1/(az+z*c*c),1/az))
def return_source(dK):
    dS=dK.transpose().matmul(Ks['good'])+Ks['good'].transpose().matmul(dK)
    return -f(8*z)*tr(Zinv.matmul(dS))
def tangent_legs(index):
    suffix=endpoint(words['good'][index+1:])
    return suffix.extract(inputs,range(DIM)),suffix.transpose().matmul(U['good']).extract(range(DIM),inputs)
def tangent_corner(legs,H): return legs[0].matmul(H).matmul(legs[1])

# V is the real copy-on-ready embedding, not an assigned probability law.
V=s.Matrix([[1,0],[0,0],[0,0],[0,1]])
need(V.T*V==s.eye(2),'actual copy-on-ready map is isometric')
J2=s.Matrix([[0,-1],[1,0]])
old_left=C.extract(inputs,range(DIM))
old_right=W.matmul(C).extract(range(DIM),inputs)
retraction=[]; old_sources={}
for j,work in enumerate(WORK):
    old_dK=old_left.matmul(embed(J2,(work,))).matmul(old_right)
    old_sources[str(work)]=return_source(old_dK)
    position=18+len(copy)+len(base)+j
    need(words['good'][position]==mark[j],'actual independent first witness occurrence '+str(work))
    legs=tangent_legs(position)
    for a in range(4):
        for b in range(a+1,4):
            X=s.zeros(4);X[a,b]=1;X[b,a]=-1
            Y=V.T*X*V
            need(Y.T==-Y,'compressed copy generator remains a genuine old skew '+str((j,a,b)))
            dK=tangent_corner(legs,embed(X,tuple(mark[j]['wires'])))
            old=old_left.matmul(embed(Y,(work,))).matmul(old_right)
            eq(dK,old,'EXACT full cold derivative retracts '+str((j,a,b)))
            scalar=return_source(dK)
            need(scalar==return_source(old),'same full source, true rank and gain '+str((j,a,b)))
            expected=-J2 if (a,b)==(0,3) else s.zeros(2)
            need(Y==expected,'all six local so4 directions have the declared compression '+str((j,a,b)))
            retraction.append({'work':work,'witness':WITNESS[j],'basis_pair':[a,b],
                               'image':'-J2' if (a,b)==(0,3) else '0',
                               'source':str(F.to_sympy(scalar))})
need(len(retraction)==18,'all three actual births and six independent local real directions covered')
need(old_sources['0']==ZERO and old_sources['12']==ZERO,'two old terminal-work sources vanish in this fixture')
expected_query=f(16*z*c*u/(az+z*c*c))
need(old_sources['11']==expected_query and expected_query!=ZERO,'old QUERY source is retained, not falsely annulled')

# Each old terminal tangent has a lift to a DISTINCT existing body call.
# In particular QUERY uses final G0 and its actual three-CX SWAP suffix.
need(base[27]=={'op':'G','wires':[0]},'old source uses actual final G0 index27')
paid_suffix=endpoint(base[28:31])
eq(paid_suffix.matmul(embed(J2,(0,))).matmul(paid_suffix.transpose()),embed(J2,(11,)),
   'actual three paid CX gates transport G0 generator to old QUERY11')
old_position=18+len(copy)+27
old_native_dK=tangent_corner(tangent_legs(old_position),embed(J2,(0,)))
eq(old_native_dK,old_left.matmul(embed(J2,(11,))).matmul(old_right),
   'new source image is the SAME actual independently varied body occurrence')
need(return_source(old_native_dK)==expected_query,'actual paid G0 source equals old terminal QUERY source')
body_lifts={0:(30,0),11:(27,0),12:(0,12)}
for work,(index,local_wire) in body_lifts.items():
    need(local_wire in base[index]['wires'],'old image respects actual raw support '+str(work))
    H=embed(J2,(local_wire,)); suffix=endpoint(base[index+1:])
    eq(suffix.matmul(H).matmul(suffix.transpose()),embed(J2,(work,)),
       'full actual paid suffix transports the old control image '+str(work))
    eq(tangent_corner(tangent_legs(18+len(copy)+index),H),
       old_left.matmul(embed(J2,(work,))).matmul(old_right),
       'cold derivative lifts to an existing independent native body position '+str(work))
need(len({v[0] for v in body_lifts.values()})==3,
     'three existing lift positions are distinct: no hidden sum at one raw slot')

# All preparation directions BEFORE the already saturated history, including
# protected-entangled ones, are covered by the full old-R block identity.
Ri=ii.matmul(Zinv).matmul(ii.transpose())
U0=U['good']
end_cotangent=(U0.matmul(Ri).matmul(U0.transpose()).matmul(P)-
               P.matmul(U0).matmul(Ri).matmul(U0.transpose())).scalarmul(f(-z))
pre_cotangent=U0.transpose().matmul(end_cotangent).matmul(U0)
ready=[k for k in range(DIM) if all(bits(k)[POS[r]]==0 for r in RECORD)]
not_ready=[k for k in range(DIM) if k not in set(ready)]
need(pre_cotangent.extract(ready,ready).is_zero_matrix,
     'entire R-ready upstream cotangent block is zero: arbitrary protected/F mixing allowed')
need(pre_cotangent.extract(not_ready,not_ready).is_zero_matrix,
     'entire R-complement upstream cotangent block is zero')
need(not pre_cotangent.is_zero_matrix,'old R-changing upstream source is retained outside the proved preparation sector')
need(len(prefix18)==18,'all18 independent preparation raw calls covered, no linked inverse legs')

# Independent small exact control: compression also covers a protected
# two-dimensional factor and need not factor as a scalar one-wire angle.
VB=s.kronecker_product(V,s.eye(2))
XB=s.zeros(8);XB[0,7]=1;XB[7,0]=-1
YB=VB.T*XB*VB
need(YB.T==-YB and YB[0,3]==1 and YB[3,0]==-1,
     'protected-entangled skew survives as an operator on old work and protected factor')
need(any(YB[a,b]!=0 for a in range(4) for b in range(4) if a%2!=b%2),
     'protected-entangled image cannot be replaced by a scalar J2 tensor identity')
# For every X, V*X*V V*XV <= V*X*XV gives ||V*XV|| <= ||X||;
# test a nonnormal rational skew without treating this control as native.
XR=s.Matrix([[0,2,3,5],[-2,0,7,11],[-3,-7,0,13],[-5,-11,-13,0]])
YR=V.T*XR*V
defect=V.T*XR.T*(s.eye(4)-V*V.T)*XR*V
need(defect==V.T*XR.T*XR*V-YR.T*YR,'exact positive Gram defect behind norm compression')
need(defect[0,0]>=0 and defect[1,1]>=0 and defect.det()>=0,'independent rational norm control is positive semidefinite')

mp.mp.dps=130;mp.iv.dps=110;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;cc=pp**3;aa=iv.sqrt(pp);uu=2*pp*aa;zz=iv.mpf(1)/2**20;ab=1-zz;beta=2*pp*pp
def ends(v):return mp.mpf(v.a),mp.mpf(v.b)
def ivrat(v):return iv.mpf(v.numerator)/v.denominator
def interval(v,places=46):
    fac=10**places;lo,hi=ends(v*fac)
    def fmt(n):
        sign='-' if n<0 else '';n=abs(n);return sign+str(n//fac)+'.'+str(n%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
N=79;x=Fraction(2,55);qn=x**N/math.factorial(N);A1=Fraction(176,359)/(1-x*x)*qn/(1-qn)**2
err=ends(ivrat(A1))[1];err2=ends(ivrat(2*A1))[1]
a0=iv.mpf(heat['complete_book']['a0_interval'])
Hprice=iv.log(N*262144*(2*a0+359))/beta+iv.mpf([-err,err])
Jgood=-8*iv.log(ab)-8*iv.log(ab+zz*cc*cc)
Jrotate=-8*iv.log(ab)-8*iv.log(ab+zz*cc**4)
Jfault=-8*iv.log(ab)-8*iv.log(ab+zz*(aa*(4*pp-3))**2)
gap=Jrotate-Jgood+iv.mpf([-err2,err2])
fault_gap=Jfault-Jgood+iv.mpf([-err2,err2])
need(ends(gap)[0]>0,'actual independent preparation alternative has strictly larger COMPLETE79 price')
need(ends(fault_gap)[1]<0,'actual birth fault still has a strictly lower COMPLETE79 price')
clock_err=ends(ivrat(A1+Fraction(guard['heat']['A1_61_rational'])))[1]
clock_increment=iv.log(iv.mpf(79)/61)/beta+iv.mpf([-clock_err,clock_err])
need(ends(clock_increment)[0]>0,'new preparation has its actual positive79 versus61 absolute clock price')
need(425*N*262144==8801484800 and 359*N*262144==7434665984,'all actual79 clock Hodge modes and harmonics counted')

result={'status':'PASS','checks':len(CHECKS),'input_commit':'049ce1128827f8a8fc63875835e53aea19140a31',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':pins,
 'consumed_helper_sha256':helper_pin,'consumed_guard_receipt_sha256':guard_pin,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'literal_prefix_identity18':prefix18,'literal_prefix_rotation18':rotate18,
 'whole_words':{name:{'N':len(word),'inventory':inventories[name],
     'sha256':sha((json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode())} for name,word in words.items()},
 'boundary':{'wires':18,'blank_wires':BLANKS,'work':WORK,'record':RECORD,'witness':WITNESS,
     'old_right':[15],'source_spin':[13,14],'active_columns':DIM,'thermal_spectator':256,
     'full_dimension':262144,'active_input_rank':2,'input_spectator':8,'input_rank':16,
     'protected_Spin_prepared':False,'new_resources_physically_derived':False},
 'cotangent_retraction':{'embedding':'V|a>=|a,a>','map':'Y=V* X V','operator_norm_gain_upper_bound':1,
     'independent_birth_rows':retraction,'old_query_actual_body_call_zero_based':old_position,
     'old_query_body_call_in_W31_zero_based':27,'old_query_source_formula':'16 zeta p^3 (2p sqrt(p))/(1-zeta+zeta p^6)',
     'old_query_source_interval':interval(16*zz*cc*uu/(ab+zz*cc*cc)),
     'birth_00_11_source_interval':interval(-16*zz*cc*uu/(ab+zz*cc*cc)),
     'general_terminal_sum_gain_upper_bound':3,
     'literal_birth_only_raw_gate_max_lift_gain':1,'literal_joint_old_plus_birth_raw_gate_max_gain':2,
     'literal_old_body_lifts':{str(w):{'W31_index':k,'whole79_index':21+k,'local_wire':q}
                               for w,(k,q) in body_lifts.items()},
     'protected_support_preserved_as_operator':True,
     'arbitrary_old_QUERY_stationarity_proved':False},
 'preparation':{'independent_paid_calls':18,'entire_R_block_cotangent_zero':True,
     'inverse_legs_independently_variable':True,'initial_R_changing_sources_covered':False,
     'corner_good':'p^3 Q','corner_rotated':'p^6 Q','rank_Q_full':8},
 'complete_price':{'good':interval(Hprice+Jgood),'prepared_rotation':interval(Hprice+Jrotate),
     'birth_fault':interval(Hprice+Jfault),'rotation_minus_good':interval(gap),
     'birth_fault_minus_good':interval(fault_gap),'absolute_H':interval(Hprice),'A1_79_rational':str(A1),
     'good79_minus_good61':interval(clock_increment),
     'all_modes':425*N*262144,'unpaired_harmonics':359*N*262144},
 'scope':{'old_full_source_and_true_gain_preserved':True,'same_execution_all79_stages_priced':True,
     'old_SOURCE_domains_must_contain_retraction_image':True,'new_physical_selector':False,
     'new_continuous_native_angle':False,'whole_price_minimum_claimed':False,
     'all_X_N_identified':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
