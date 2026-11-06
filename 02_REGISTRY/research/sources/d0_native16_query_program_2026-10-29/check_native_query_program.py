#!/usr/bin/env python3
"""A literal two-QUERY native processor, independent preparations and full price.

All SourceI columns are kept explicitly, including at each independent raw
source insertion. This is not a free controlled-G or a native smooth angle.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast,hashlib,json,math,platform
import sympy as s
import mpmath as mp

ROOT=Path.cwd();PAPER=ROOT/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
def block(tag,lang,pin):
    raw=PAPER.read_bytes();a=('<!-- BEGIN '+tag+' -->\n```'+lang+'\n').encode();b=('```\n<!-- END '+tag+' -->').encode()
    if raw.count(a)!=1 or raw.count(b)!=1:raise ArithmeticError('ambiguous '+tag)
    data=raw.split(a)[1].split(b)[0]
    if hashlib.sha256(data).hexdigest()!=pin:raise ArithmeticError('changed '+tag)
    return data
helper_pin='e3ac0eb35ec9c4043cf51485f36d3145be3f9be988e28d38330c510599906fc3'
tree=ast.parse(block('7dw SAME USE RECORD GUARD CHECKER','python',helper_pin));prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='base' for t in node.targets):break
    prefix.append(node)
else:raise ArithmeticError('missing helper boundary')
ns={'__name__':'native_program_helpers'}
exec(compile(ast.Module(body=prefix,type_ignores=[]),str(PAPER)+'#7dw-helper','exec'),ns)
names=('need sha frozen prior heat pins ne p alpha c u z az F ZERO ONE f sparse dm eye eq tr embed CHECKS').split()
globals().update({k:ns[k] for k in names})
frozen('7dx GUARD COTANGENT RETRACTION RECEIPT','2e0c9e190ed587e66c6e562e6cc23a0696191a0de04b723b64ce3d57d94b265a')
program_owner='02_REGISTRY/research/A4D_INTERNAL_PROGRAM_AND_GLOBAL_QUERY_STATIONARITY_2026_10_28.md'
program_pin='ed2323c7610f94994868a947fd17be6a50f0170e29b33c260a8441bd3087dc04'
need(sha((ROOT/program_owner).read_bytes())==program_pin,'pinned abstract internal programme source owner')
pins=dict(pins);pins[program_owner]=program_pin

# Actual original16-wire boundary. The formerly idle RIGHT10 is the code;
# its thermal columns were ALREADY present. Spin13/14 stays arbitrary.
ACTIVE=(0,6,10,11,12,7,8,9,13,14);POS={q:j for j,q in enumerate(ACTIVE)};NW=len(ACTIVE);DIM=2**NW
ns.update(ACTIVE=ACTIVE,POS=POS,NW=NW,DIM=DIM)
I=eye(DIM);BLANKS=(0,1,2,3,4,5,7,8,9,10,11,12);WORK=(0,11,12);RECORD=(7,8,9)
bits=ns['bits'];number=ns['number']
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
cache={}
def gate(g):
    key=g['op'],tuple(g['wires'])
    if key not in cache:
        cache[key]=embed({'G':ne.G_LOCAL,'CX':CX,'SourceI':ne.SOURCE_I_LOCAL}[key[0]],key[1])
        eq(cache[key].transpose().matmul(cache[key]),I,'primitive all1024 columns '+repr(key))
    return cache[key]
def endpoint(word):
    out=I
    for g in word:out=gate(g).matmul(out)
    return out
def cx(a,b):return {'op':'CX','wires':[a,b]}
def gg(a):return {'op':'G','wires':[a]}
si={'op':'SourceI','wires':[0,13,14]}
swap=[cx(0,10),cx(10,0),cx(0,10)]
base=prior['literal_words']['reference31'];copy=[cx(a,r) for a,r in zip(WORK,RECORD)]
inverse10=[{'op':g['op'],'wires':[10 if q==11 else q for q in g['wires']]} for g in base[5:16]]
prepare_I=[gg(10)]+inverse10
prepare_R=swap+[gg(0),gg(0)]+[si]*4+swap
prepare_Rinv=swap+[si]*2+[gg(0),gg(0)]+[si]*2+swap
prepares={'I':prepare_I,'R':prepare_R,'Rinv':prepare_Rinv}
for name,word in prepares.items():
    need(len(word)==12,'all12 preparation calls '+name)
    need(Counter(g['op'] for g in word)=={'G':2,'CX':6,'SourceI':4},'identical real preparation inventory '+name)
    need(all(not set(g['wires']).intersection(RECORD+(11,12,6)) for g in word),
         'preparation acts only on real port/code/Spin '+name)
G10=gate(gg(10));R=G10.matmul(G10)
eq(endpoint(prepare_I),I,'actual12-call identity preparation')
eq(endpoint(prepare_R),R,'actual12-call G10 squared preparation')
eq(endpoint(prepare_Rinv),R.transpose(),'actual12-call inverse square, with no inverse primitive')

# Existing exact even-G control, applied to the specific old QUERY.
# At code0 the echo is G11 squared; at code1 it is identity.
controlled_even=[gg(11),cx(10,11),gg(11),cx(10,11)]
processor=base[:5]+base[16:24]+controlled_even
need(len(processor)==17,'actual17-stage processor includes seed and routed Z11')
Ctrl=endpoint(processor);W0=endpoint(base)
Z11=endpoint(base[16:24]);W1=Z11.matmul(endpoint(base[:5]))
Pcode0=embed(s.diag(1,0),(10,));Pcode1=I-Pcode0
eq(Ctrl,Pcode0.matmul(W0)+Pcode1.matmul(W1),'exact native controlled oldQUERY/Z on ALL columns')
eq(Ctrl,Ctrl.transpose(),'full controlled processor is a reflection')
eq(Ctrl.matmul(Pcode0),Pcode0.matmul(Ctrl),'code label is retained by the same fixed processor')

words={'pure':copy+prepare_I+processor+prepare_I+copy,
       'before_only':copy+prepare_R+processor+prepare_I+copy,
       'after_only':copy+prepare_I+processor+prepare_Rinv+copy,
       'echo':copy+prepare_R+processor+prepare_Rinv+copy}
inventories={};U={}
for name,word in words.items():
    ex=ne.Execution(16,BLANKS,(15,),tuple(ne.Gate(g['op'],tuple(g['wires'])) for g in word),
                    ne.G_CX_SOURCE_I,0,(13,14),RECORD+(10,))
    ne.validate_execution(ex,max_qubits=16,max_expanded_stages=47)
    need(len(word)==47,'all47 native stages '+name)
    inventories[name]=dict(sorted(Counter(g['op'] for g in word).items()))
    need(inventories[name]=={'CX':27,'G':6,'SourceI':14},'whole clock and inventory match '+name)
    U[name]=endpoint(word)
    eq(U[name].transpose().matmul(U[name]),I,'whole all1024-column unitarity '+name)
C=endpoint(copy);old37=C.matmul(W0).matmul(C)
eq(U['pure'],C.matmul(Ctrl).matmul(C),'same fixed processor, pure programme base')
eq(U['pure'],U['pure'].transpose(),'pure programme complete endpoint reflection')
eq(U['echo'],R.transpose().matmul(U['pure']).matmul(R),'FULL echo conjugacy including every old record')
eq(U['echo'],U['echo'].transpose(),'echo endpoint also a full reflection')
need(tr(U['pure'])==ZERO and tr(U['echo'])==ZERO and tr(old37)==ZERO,
     'balanced full reflections: old37, pure and echo heat multiplicities coincide')

inputs=[k for k in range(DIM) if all(bits(k)[POS[w]]==0 for w in (0,10,11,12)+RECORD)]
need(len(inputs)==8 and 8*2==16 and DIM*64==65536,'all arbitrary Spin input columns and actual thermal spectators')
ii=I.extract(range(DIM),inputs);P=ii.matmul(ii.transpose())
Q=dm(s.diag(*[1 if bits(k)[POS[6]]==0 else 0 for k in inputs]))
need(tr(Q)==f(4),'rank_Q active4, full8 with oldRIGHT')
eq(U['pure'].matmul(ii),old37.matmul(ii),'same complete prepared output as old37 for EVERY protected input')
Ks={name:value.extract(inputs,inputs) for name,value in U.items()}
b=1-c*c+c**3
values={'pure':c,'before_only':c*c,'after_only':c*c,'echo':b}
for name,value in values.items():eq(Ks[name],Q.scalarmul(f(value)),'actual full cold corner '+name)
need(f(b-c)!=ZERO and f(1-b)!=ZERO,'mixed code corner is strictly distinct from either pure law')

# Complete primitive source cotangents. No SourceI pair is merged here:
# each of its actual eight local columns is retained at the raw stage.
Zinv=dm(s.diag(*[1/(az+z*c*c) if bits(k)[POS[6]]==0 else 1/az for k in inputs]))
Ri=ii.matmul(Zinv).matmul(ii.transpose());U0=U['pure']
B0=U0.matmul(Ri).matmul(U0.transpose())
cov=(B0.matmul(P)-P.matmul(B0)).scalarmul(f(-2*z))
def partial(A,wires):
    out={};chosen={POS[w] for w in wires}
    for (r0,c0),v in A.to_dok().items():
        br,bc=bits(r0),bits(c0)
        if any(br[j]!=bc[j] for j in range(NW) if j not in chosen):continue
        r=sum(br[POS[w]]<<(len(wires)-1-j) for j,w in enumerate(wires))
        c0=sum(bc[POS[w]]<<(len(wires)-1-j) for j,w in enumerate(wires))
        out[r,c0]=out.get((r,c0),ZERO)+v
    return sparse(out,(2**len(wires),2**len(wires)))
rows=[];pulled=cov
for j in range(46,-1,-1):
    g=words['pure'][j];local=partial(pulled,tuple(g['wires']))
    eq(local.transpose(),-local,'true local raw cotangent is skew '+str(j))
    entries=[]
    for (a0,b0),value in sorted(local.to_dok().items()):
        if a0<b0 and value:
            entries.append({'pair':[a0,b0],'source_Xab':str(F.to_sympy(-f(2)*value))})
    rows.append({'stage_zero_based':j,'gate':g,'nonzero_real_skew_sources':entries})
    G=gate(g);pulled=G.transpose().matmul(pulled).matmul(G)
rows.reverse()
prep_indices=list(range(3,15))+list(range(32,44))
need(all(not rows[j]['nonzero_real_skew_sources'] for j in prep_indices),
     'all24 independent actual preparation calls have zero full first source')
need(sum((2**len(g['wires']))*(2**len(g['wires'])-1)//2 for g in words['pure'])==560,
     'all local real generators covered, including28 per SourceI occurrence')

J2=s.Matrix([[0,-1],[1,0]])
expected=f(16*z*c*u/(az+z*c*c))
for j in (28,30):
    need(words['pure'][j]==gg(11),'genuine selected-branch hardware G11 '+str(j))
    row=rows[j]['nonzero_real_skew_sources']
    need(len(row)==1 and f(s.sympify(row[0]['source_Xab']))==-expected,
         'old positive J2 QUERY source survives at this actual independent G call '+str(j))

# The new controlled-CX raw sources retract through their ACTUAL selected
# code block, including all five directions with zero cold derivative.
def tangent_corner(index,H):
    suffix=endpoint(words['pure'][index+1:])
    return suffix.extract(inputs,range(DIM)).matmul(H).matmul(
        suffix.transpose().matmul(U0).extract(range(DIM),inputs))
old_query_dK=tangent_corner(30,embed(J2,(11,)))
controller_retraction=[]
for index in (29,31):
    need(words['pure'][index]==cx(10,11),'actual controlled-CX occurrence '+str(index))
    for a0 in range(4):
        for b0 in range(a0+1,4):
            X=s.zeros(4);X[a0,b0]=1;X[b0,a0]=-1
            image=X[:2,:2]
            target=old_query_dK.scalarmul(-ONE) if (a0,b0)==(0,1) else sparse({},(8,8))
            eq(tangent_corner(index,embed(X,(10,11))),target,
               'new controlled-CX cold derivative equals selected old QUERY image '+str((index,a0,b0)))
            need(image==(-J2 if (a0,b0)==(0,1) else s.zeros(2)),
                 'actual code compression, no fitted source coefficient '+str((index,a0,b0)))
            controller_retraction.append({'stage':index,'pair':[a0,b0],
                                          'image':'-J2' if (a0,b0)==(0,1) else '0'})

# Whole code-off-diagonal endpoint directions have zero first source, but
# within the selected branch query directions above remain nonzero.
code0=[k for k in range(DIM) if bits(k)[POS[10]]==0]
code1=[k for k in range(DIM) if bits(k)[POS[10]]==1]
need(cov.extract(code0,code1).is_zero_matrix and cov.extract(code1,code0).is_zero_matrix,
     'full endpoint code-off-diagonal cotangent is zero including protected entanglement')
need(cov.extract(code1,code1).is_zero_matrix,'unprepared code branch has zero feedback first cotangent')
need(not cov.extract(code0,code0).is_zero_matrix,'selected branch source is not erased by internal programming')

mp.mp.dps=130;mp.iv.dps=110;iv=mp.iv
pp=(iv.sqrt(5)-1)/2;cc=pp**3;uu=2*pp*iv.sqrt(pp);zz=iv.mpf(1)/2**20;ab=1-zz;beta=2*pp*pp
bb=1-cc*cc+cc**3
def ends(v):return mp.mpf(v.a),mp.mpf(v.b)
def ivrat(v):return iv.mpf(v.numerator)/v.denominator
def interval(v,places=46):
    fac=10**places;lo,hi=ends(v*fac)
    def fmt(n):
        sign='-' if n<0 else '';n=abs(n);return sign+str(n//fac)+'.'+str(n%fac).zfill(places)
    return [fmt(int(mp.floor(lo))-1),fmt(int(mp.ceil(hi))+1)]
N=47;x=Fraction(2,55);qn=x**N/math.factorial(N);A1=Fraction(176,359)/(1-x*x)*qn/(1-qn)**2
err=ends(ivrat(A1))[1];err2=ends(ivrat(2*A1))[1]
Hprice=iv.log(N*65536*(2*iv.mpf(heat['complete_book']['a0_interval'])+359))/beta+iv.mpf([-err,err])
v={'pure':cc,'before_only':cc*cc,'after_only':cc*cc,'echo':bb}
J={name:-8*iv.log(ab)-8*iv.log(ab+zz*value*value) for name,value in v.items()}
gaps={name:J[name]-J['pure']+(iv.mpf([0,0]) if name=='echo' else iv.mpf([-err2,err2]))
      for name in ('before_only','after_only','echo')}
need(ends(gaps['before_only'])[0]>0 and ends(gaps['after_only'])[0]>0,
     'each actual one-sided preparation is dearer in complete47 price')
need(ends(gaps['echo'])[1]<0,'actual complete coherent programme change is cheaper, with EXACT heat cancellation')
need(ends(bb-cc)[0]>0 and ends(1-bb)[0]>0,'actual programmed corner remains strictly interior')
echo_hessian=-32*zz*cc*(1-cc)/(ab+zz*cc*cc)
one_sided_hessian=16*zz*cc*cc/(ab+zz*cc*cc)
A2=2*Fraction(176,359)/(1-x*x)*qn*qn/(1-qn)**3+Fraction(4,5)*A1*A1
hess_err=ends(ivrat(A1+A2))[1]
one_sided_full_hessian=one_sided_hessian+iv.mpf([-hess_err,hess_err])
need(ends(echo_hessian)[1]<0 and ends(one_sided_hessian)[0]>0,
     'correct paired echo and independent one-sided feedback Hessians have opposite signs')
need(ends(one_sided_full_hessian)[0]>0,'whole heat second derivative retained in positive one-sided Hessian')
need(425*N*65536==1309081600 and 359*N*65536==1105788928,'all actual47 clock modes and harmonics counted')
q37=x**37/math.factorial(37);A137=Fraction(176,359)/(1-x*x)*q37/(1-q37)**2
clockerr=ends(ivrat(A1+A137))[1]
clockgap=iv.log(iv.mpf(47)/37)/beta+iv.mpf([-clockerr,clockerr])
need(ends(clockgap)[0]>0,'native processor and both preparations retain their positive absolute clock increment')

result={'status':'PASS','checks':len(CHECKS),'input_commit':'442ddd86c96a4298efea7dc69e803f2ef1f6cd45',
 'checker_sha256':sha(Path(__file__).read_bytes()),'input_pins':pins,'consumed_helper_sha256':helper_pin,
 'runtime':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},
 'literal_processor17':processor,'literal_preparations12':prepares,
 'whole_words':{name:{'N':len(word),'inventory':inventories[name],
     'sha256':sha((json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode())} for name,word in words.items()},
 'boundary':{'wires':16,'blank_wires':BLANKS,'program':10,'work':WORK,'record':RECORD,
     'source_spin':[13,14],'old_right':[15],'active_columns':1024,'thermal_spectator':64,
     'full_dimension':65536,'active_input_rank':8,'input_spectator':2,'input_rank':16,
     'new_thermal_factor_for_existing_program':False,'protected_Spin_prepared':False},
 'independent_raw_sources':rows,'source_summary':{'total_raw_calls':47,'local_real_generator_count':560,
     'all24_preparation_rows_zero':True,'code_off_diagonal_sources_zero':True,
     'selected_branch_G11_indices':[28,30],
     'each_G11_J2_source_interval':interval(16*zz*cc*uu/(ab+zz*cc*cc)),
     'all_hardware_rows_solved':False},
 'controlled_CX_cold_derivative_retractions':controller_retraction,
 'return_corners':{'pure':'c Q','before_only':'c^2 Q','after_only':'c^2 Q','echo':'(1-c^2+c^3) Q','c':'p^3','rank_Q_full':8},
 'complete_prices':{name:interval(Hprice+value) for name,value in J.items()},
 'complete_differences':{name+'_minus_pure':interval(value) for name,value in gaps.items()},
 'heat':{'absolute_H':interval(Hprice),'A1_47_rational':str(A1),'all_modes':425*N*65536,
     'unpaired_harmonics':359*N*65536,'pure_and_echo_heat_exactly_equal':True,
     'pure47_minus_old37':interval(clockgap)},
 'matrix_comparison_hessians':{'echo':interval(echo_hessian),'one_sided':interval(one_sided_hessian),
     'one_sided_complete_price':interval(one_sided_full_hessian),'heat_second_derivative_bound_rational':str(A1+A2),
     'claimed_continuous_native_angle':False,'independent_legs_not_identified':True},
 'scope':{'actual_native_controlled_QUERY_compiled':True,'same_prepared_base_output_as_old37':True,
     'old_all_prefix_history_equivalence_claimed':False,'all_programming_sources_are_hardware_sources':False,
     'fixed_processor_choice_physically_forced':False,'all_physical_X_N_identified':False,
     'new_Info_or_action_term':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
