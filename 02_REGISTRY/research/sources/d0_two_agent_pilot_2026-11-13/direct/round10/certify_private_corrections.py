#!/usr/bin/env python3
"""Independent integer interval certificate of full private corrections.

The search's floating angles/quaternions/errors are not used. Targets come
from the original Golden gate, actual NPS probability and exact recursion.
Every local supported macro is also replayed with exact algebraic entries.
"""
import hashlib,importlib.util,json,math,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import nps_private_recovery as nr
from supported_private_plane import plane

HERE=Path(__file__).resolve().parent
source=HERE/'inputs/d0_controlled_recorder_interval_20261026.py'
spec=importlib.util.spec_from_file_location('owned_private_intervals',source)
ivmod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ivmod;spec.loader.exec_module(ivmod)
iv=ivmod.Dyadic(320)
nt=nr.native;checks=[]
def ck(ok,name):
    if not bool(ok):raise ArithmeticError(name)
    checks.append(name)

def div(a,b):
    if b[0]<=0:raise ArithmeticError('division interval not certified positive')
    endpoints=[Fraction(x*iv.D,y) for x in a for y in b]
    lo,hi=min(endpoints),max(endpoints)
    return lo.numerator//lo.denominator,-((-hi.numerator)//hi.denominator)

def cmul(z,w):
    return iv.sub(iv.mul(z[0],w[0]),iv.mul(z[1],w[1])),iv.add(iv.mul(z[0],w[1]),iv.mul(z[1],w[0]))

def powi(v,n):
    out=iv.const(1)
    for _ in range(n):out=iv.mul(out,v)
    return out

p=iv.mul(iv.sub(iv.root(iv.const(5)),iv.const(1)),iv.rat(1,2));a=iv.root(p)
G=[[a,iv.neg(p)],[p,a]]
g32=iv.power(G,32);g624=iv.power(G,624)
tc,ts=g624[0][0],g624[1][0]
ck(tc[0]>iv.D//2 and tc[1]<17*iv.D//32 and ts[0]>0,'same exact native stable phase')
aa=iv.mul(iv.const(2),iv.sub(iv.const(1),tc));bb=iv.sub(iv.mul(iv.const(2),tc),iv.const(1))
q=iv.add(powi(p,2),iv.mul(iv.const(16),powi(p,12)))
bundle=json.loads((HERE/'CORRECTION_WORDS.json').read_text())
ck(bundle['fixture']['q']=='p^2+16*p^12' and bundle['fixture']['stable_phase_multiplier']==624,'actual fixture target binding')
n=bundle['fixture']['recovery_rounds']
target_cs={};failures=[]
for branch,prob in enumerate((iv.sub(iv.const(1),q),q)):
    eps=iv.sub(iv.const(1),prob);z=(iv.root(prob),iv.const(0))
    for _ in range(n):
        z=cmul(z,cmul((tc,ts),(iv.add(tc,iv.mul(aa,eps)),ts)))
        eps=iv.mul(eps,powi(iv.add(bb,iv.mul(aa,eps)),2))
    norm=iv.root(iv.sub(iv.const(1),eps))
    target_cs[f'phase_{branch}']=(div(z[0],norm),div(z[1],norm))
    failures.append(eps)
tailc=div(iv.const(1),iv.root(iv.add(iv.const(1),powi(p,4))))
target_cs['archive_tail']=(tailc,iv.mul(powi(p,2),tailc))

generators={1:iv.plane(3,0,1,g32[0][0],g32[1][0]),2:iv.plane(3,0,2,g32[0][0],g32[1][0])}
generators[-1]=iv.tr(generators[1]);generators[-2]=iv.tr(generators[2])
matrices=[];counts=[]
for index,node in enumerate(bundle['nodes']):
    kind=node['kind']
    if kind=='seq':
        mat=iv.identity(3);cc=Counter()
        for letter in node['letters']:
            if type(letter) is not int or letter not in generators:raise ValueError('letter')
            mat=iv.mm(generators[letter],mat);cc[letter]+=1
    elif kind=='inv':
        child=node['child'];ck(type(child) is int and 0<=child<index,'topological inverse')
        mat=iv.tr(matrices[child]);cc=Counter({-k:v for k,v in counts[child].items()})
    elif kind=='cat':
        mat=iv.identity(3);cc=Counter()
        for child in node['children']:
            ck(type(child) is int and 0<=child<index,'topological concatenation')
            mat=iv.mm(matrices[child],mat);cc.update(counts[child])
    else:raise ValueError('node kind')
    ck(sum(cc.values())==node['length'],'exact signed letter inventory')
    matrices.append(mat);counts.append(cc)

layout=nt.Execution(10,(0,3,4,5,6,7,8,9),(),(),nt.G_CX_SOURCE_I,0,(1,2),(5,6))
def embed(A,inds):
    M=iv.identity(8)
    for i in range(3):
        for j in range(3):M[inds[i]][inds[j]]=A[i][j]
    return M

total=Counter();reports=[];recipes=[];actual_corrections={}
for report in bundle['targets']:
    name=report['name'];root=report['root']
    ck(name in target_cs and report['abstract_letter_length']==sum(counts[root].values()),'target inventory binding')
    record_value=1 if name=='phase_1' else 0
    targets=(6,8,9) if name=='archive_tail' else (7,8,9)
    actual=iv.identity(8);ideal=iv.identity(8);c,s=target_cs[name]
    native_counts=Counter()
    for i in range(4):
        j=i+4;k=next(k for k in range(8) if k not in (i,j))
        actual=iv.mm(embed(matrices[root],(i,j,k)),actual)
        ideal=iv.mm(iv.plane(8,i,j,c,s),ideal)
        macros={}
        for letter,frequency in counts[root].items():
            endpoint=j if abs(letter)==1 else k
            word=plane(layout,targets,5,record_value,i,endpoint,1 if letter>0 else -1)
            macro_count=nr.counts(word)
            macros[str(letter)]={'i':i,'j':endpoint,'sign':1 if letter>0 else -1,'counts':macro_count}
            for op,number in macro_count.items():native_counts[op]+=frequency*number
        recipes.append({'correction':name,'record':5,'record_value':record_value,'targets':targets,
                        'SO3_root':root,'embed_indices':[i,j,k],'signed_macros':macros})
    error=iv.frobenius_upper(actual,ideal)
    actual_corrections[name]=actual
    ck(error*10**23<iv.D,'complete correction all-column error below1e-23')
    total.update(native_counts)
    reports.append({'name':name,'native_counts':dict(native_counts),'all8_column_error_upper':str(Fraction(error,iv.D)),
                    'error_upper_decimal':f'{float(Fraction(error,iv.D)):.16e}'})

# Exact literal all-column macro check, including arbitrary source/Spin input.
small=nt.Execution(7,(3,4,5,6),(),(),nt.G_CX_SOURCE_I,0,(1,2))
field=nt.GOLDEN_FIELD;one,zero=field.one,field.zero
localG=[[field.from_sympy(x) for x in row] for row in nt.G_LOCAL.tolist()]
SI=nt.SOURCE_I_LOCAL
localSI=[]
for c in range(8):
    rr=next(r for r in range(8) if SI[r,c]!=0);localSI.append((rr,field.from_sympy(SI[rr,c])))
gc,gs=one,zero
ga,gp=field.from_sympy(nt.A),field.from_sympy(nt.P)
for _ in range(32):gc,gs=ga*gc-gp*gs,gp*gc+ga*gs

def exact_columns(word):
    cols=[{c:one} for c in range(128)]
    bit=lambda w:1<<(6-w)
    for gate in word:
        nextcols=[]
        for col in cols:
            out={}
            for row,vv in col.items():
                if gate.op=='CX':
                    c,t=gate.wires;rr=row^bit(t) if row&bit(c) else row
                    out[rr]=out.get(rr,zero)+vv
                elif gate.op=='G':
                    w=gate.wires[0];old=int(bool(row&bit(w)))
                    for new in (0,1):
                        rr=(row&~bit(w))|(new*bit(w));out[rr]=out.get(rr,zero)+vv*localG[new][old]
                else:
                    old=sum(int(bool(row&bit(w)))<<(2-k) for k,w in enumerate(gate.wires))
                    new,coeff=localSI[old];rr=row
                    for k,w in enumerate(gate.wires):
                        if ((old^new)>>(2-k))&1:rr^=bit(w)
                    out[rr]=out.get(rr,zero)+coeff*vv
            nextcols.append({r:v for r,v in out.items() if v!=zero})
        cols=nextcols
    return cols

fixtures=[]
for value,i,j,sign in ((0,0,4,1),(1,5,2,-1),(1,0,1,1),(0,7,3,-1)):
    word=plane(small,(4,5,6),3,value,i,j,sign)
    actual=exact_columns(word)
    expected=[]
    for c in range(128):
        label=c&7;r=(c>>3)&1
        if r!=value or label not in (i,j):expected.append({c:one})
        else:
            other=j if label==i else i;rr=(c&~7)|other
            expected.append({c:gc,rr:sign*gs if label==i else -sign*gs})
    ck(actual==expected,'exact literal macro on all128 dirty source/Spin columns')
    fixtures.append({'value':value,'i':i,'j':j,'sign':sign,'counts':nr.counts(word),'columns':128})

# Exhaust every supported ordered plane/selector/column at the exact Fourier
# level. The literal gate primitives and dirty source frame were checked above.
for value in (0,1):
 for i in range(8):
  for j in range(8):
   if i==j:continue
   diff=[((i^j)>>(2-k))&1 for k in range(3)];pivot=next(k for k in range(3) if diff[k])
   def linear_bits(label):
    bits=[(label>>(2-k))&1 for k in range(3)]
    for k in range(3):
     if k!=pivot and diff[k]:bits[k]^=bits[pivot]
    return bits
   target=linear_bits(i);pattern=[value]+[target[k] for k in range(3) if k!=pivot]
   for sign in (-1,1):
    internal=sign*(1 if target[pivot]==0 else -1)
    for external in (0,1):
     for label in range(8):
      bits=linear_bits(label);control=[external]+[bits[k] for k in range(3) if k!=pivot]
      exponent=4*internal*sum((-1)**sum(((mask>>k)&1)*(pattern[k]+control[k]) for k in range(3)) for mask in range(8))
      oriented=exponent*(1 if bits[pivot]==0 else -1)
      expected=(32*sign if label==i else -32*sign if label==j else 0) if external==value else 0
      ck(oriented==expected,'all ordered planes have exact conditional support and orientation')

# Literal native inversion is counted on every RAW occurrence; inv(inv W)
# is not silently shortened. This reproduces the owned recurrence exactly.
base=nr.fixture();plan=nr.private_recovery(base,processor_blanks=(0,3,4),record=5,pointer=3,tail=4,rebit=7,rounds=0,protected=(6,))
def four_counts(word):
    c=nr.counts(word);return c['G'],c['CX'],c['SourceI'],sum(g.op=='G' and g.wires[0]!=0 for g in word)
G0,C0,I0,O0=four_counts(base.gates)
PG,PC,PI,PO=four_counts(plan['initial_phase']+plan['equal_phase'])
gg,cx,si,off=G0,C0,I0,O0
rows=[(gg,cx,si,off)]
for _ in range(n):
    gg,cx,si,off=3*gg+PG,3*cx+6*off+PC,5*si+4*gg+PI,2*off+PO
    rows.append((gg,cx,si,off))
recovery={'G':gg,'CX':cx+6*off,'SourceI':3*si+4*gg}
recovery['N']=sum(recovery.values())
pre=nr.counts(plan['private_preparation'])
executed=json.loads((HERE/'PRIVATE_RECOVERY_CHECK.json').read_text())
for row in executed['rounds']:
    g,c,i,o=rows[row['round']]
    expected={'G':g+pre['G'],'CX':c+6*o+pre['CX'],'SourceI':3*i+4*g+pre['SourceI']}
    expected['N']=sum(expected.values())
    ck(expected==row['actual_raw_counts'],'symbolic raw counts match actually executed lower levels')
max_fail=max(e[1] for e in failures)
state_error=2*iv.root((0,max_fail))[1]+max(Fraction(r['all8_column_error_upper']) for r in reports if r['name'].startswith('phase'))*iv.D+Fraction(next(r['all8_column_error_upper'] for r in reports if r['name']=='archive_tail'))*iv.D
state_error=Fraction(state_error,iv.D)
Nrecovery=recovery['N']+total['N']
ck(state_error>0 and state_error*(Nrecovery+229)<Fraction(1,10**8),'full actual fixture count times certified state error below1e-8')

# Actual finite corner, with the compiled correction words FROZEN. No ideal
# limiting gain is substituted. These 16 dimensions are only t,h,helper,helper;
# bank/Spin compression was proved by the full NPS recursion above.
def lift8(M,positions):
    out=[[iv.const(0) for _ in range(16)] for _ in range(16)]
    for col in range(16):
        cc=sum(((col>>(3-w))&1)<<(2-k) for k,w in enumerate(positions))
        for rr in range(8):
            row=col
            for k,w in enumerate(positions):
                if ((cc^rr)>>(2-k))&1:row^=1<<(3-w)
            out[row][col]=M[rr][cc]
    return out

init=[];bra=[]
for k in range(16):
    hbits=[(k>>(2-j))&1 for j in range(3)]
    amp=iv.const(1)
    for bit in hbits:amp=iv.mul(amp,p if bit else a)
    init.append([amp if k<8 else iv.const(0)])
    bra.append(amp)
Jinit=[[iv.const(0)] for _ in range(16)]
for col in range(16):
    row=col^4
    Jinit[row][0]=iv.neg(init[col][0]) if col&4 else init[col][0]
coeffs=[]
for branch in (0,1):
    U=lift8(actual_corrections[f'phase_{branch}'],(1,2,3))
    if branch==0:U=iv.mm(lift8(actual_corrections['archive_tail'],(0,2,3)),U)
    row=[]
    for k in range(16):
        exponent=(4 if k<8 else 6) if branch==0 else (6 if k<8 else 8)
        row.append(iv.mul(powi(p,exponent),bra[k]))
    Avec=iv.mm(U,init);Bvec=iv.mm(U,Jinit)
    ca=iv.sum(iv.mul(row[k],Avec[k][0]) for k in range(16))
    cb=iv.neg(iv.sum(iv.mul(row[k],Bvec[k][0]) for k in range(16)))
    coeffs.append((ca,cb))

def finite_corner(prob,co):
    eps=iv.sub(iv.const(1),prob);de=iv.const(-1)
    root=iv.root(prob);z=(root,iv.const(0));dz=(div(iv.rat(1,2),root),iv.const(0))
    for _ in range(n):
        fac=cmul((tc,ts),(iv.add(tc,iv.mul(aa,eps)),ts))
        dfac=cmul((tc,ts),(iv.mul(aa,de),iv.const(0)))
        newdz0=cmul(dz,fac);newdz1=cmul(z,dfac)
        dz=(iv.add(newdz0[0],newdz1[0]),iv.add(newdz0[1],newdz1[1]))
        z=cmul(z,fac)
        de=iv.mul(de,iv.mul(iv.add(bb,iv.mul(aa,eps)),iv.add(bb,iv.mul(iv.const(3),iv.mul(aa,eps)))))
        eps=iv.mul(eps,powi(iv.add(bb,iv.mul(aa,eps)),2))
    val=iv.add(iv.mul(co[0],z[0]),iv.mul(co[1],z[1]))
    derivative=iv.add(iv.mul(co[0],dz[0]),iv.mul(co[1],dz[1]))
    return iv.mul(root,val),iv.add(iv.mul(div(iv.rat(1,2),root),val),iv.mul(root,derivative))

qrad=iv.D//(1<<30)
qcollar=(q[0]-qrad,q[1]+qrad)
c0,dc0=finite_corner(iv.sub(iv.const(1),qcollar),coeffs[0])
c1,dc1=finite_corner(qcollar,coeffs[1])
cfinite=iv.add(c0,c1);dcfinite=iv.sub(dc1,dc0)
ck(cfinite[0]>0 and dcfinite[1]<0,'actual finite compiled corner has strictly positive J q-source on certified collar')
as_decimal=lambda x:[f'{float(Fraction(y,iv.D)):.17g}' for y in x]

# Complete small-fixture programme, with all births and the REAL six-copy
# reader. It is a compact executable recipe; the trillion-call word was not run.
full_layout=nt.Execution(16,(0,3,4,5,6,7,8,9,10,11,12,13,14,15),(),(),nt.G_CX_SOURCE_I,0,(1,2),(5,6))
CX=lambda c,t:nt.Gate('CX',(c,t))
SI=nt.Gate('SourceI',(0,1,2))
sw=lambda q:(CX(0,q),CX(q,0),CX(0,q))
reader=[]
for wire in range(10,16):
    zz=sw(wire)+(SI,SI)+sw(wire)
    reader+=list(zz+(nt.Gate('G',(wire,)),)+zz)
for slot,wire in enumerate((5,6,5,6)):
    reader+=list(sw(wire));reader.append(CX(0,10+slot))
    if slot>=2:reader.append(CX(6 if slot==2 else 5,10+slot+2))
    reader+=list(sw(wire))
ck(nr.counts(reader)=={'G':6,'CX':102,'SourceI':24,'N':132},'entire original six-copy reader emitted')
outer_word=tuple(nt.Gate(g.op,tuple({3:5,4:6}.get(w,w) for w in g.wires)) for g in base.gates)
nt.validate_execution(nt.Execution(16,full_layout.blank_wires,(),outer_word+tuple(reader),nt.G_CX_SOURCE_I,0,(1,2)),
                      max_qubits=16,max_expanded_stages=10000)

def gates_json(word):return [{'op':g.op,'wires':g.wires} for g in word]
descriptor={'schema':'d0.nps-private-recovery-dag/1','raw_inverse_semantics':'For amplifier/recovery raw_inverse nodes: apply native.inverse_word to the complete expanded child; do not cancel nested inverses',
 'correction_inverse_semantics':'Expand the separate SO3 DAG into signed letters first: inv reverses order and negates letters. Emit each resulting signed letter by its declared fresh plane recipe. This is not raw_inverse of a previously emitted physical macro.',
 'layout':nt.execution_to_dict(layout),'processor_blanks':[0,3,4],'outer_record':5,'outer_tail':6,
 'new_private_births':[3,4,7,8,9],'canonical_birth_vector':'(sqrt(p),p)',
 'square_NPS_base':gates_json(base.gates),'initial_phase':gates_json(plan['initial_phase']),
 'equal_phase':gates_json(plan['equal_phase']),'private_preparation':gates_json(plan['private_preparation']),
 'amplifier':{'rounds':n,'A0':'square_NPS_base','chronological_recurrence':['A_previous','equal_phase',{'raw_inverse':'A_previous'},'initial_phase','A_previous']},
 'chronological_recovery':['private_preparation',{'raw_inverse':'A_n'},'phase_0','phase_1','archive_tail'],
 'correction_bundle_sha256':hashlib.sha256((HERE/'CORRECTION_WORDS.json').read_bytes()).hexdigest(),
 'correction_recipes':recipes,'N_recovery_and_corrections_excluding_private_preparation':Nrecovery,
 'full_small_fixture':{'layout':nt.execution_to_dict(full_layout),'initial_unknown_wires':[1,2],
   'chronological_parts':[{'births':[0,5,6]},{'gates':'outer_NPS_word'},{'births':[3,4,7,8,9]},
      'chronological_recovery',{'births':[10,11,12,13,14,15]},{'gates':'archive_reader'}],
   'outer_NPS_word':gates_json(outer_word),'archive_reader':gates_json(reader)},
 'full_geometric_H1':False,'all_required_mark_transports':False}
(HERE/'PRIVATE_RECOVERY_DAG.json').write_text(json.dumps(descriptor,indent=2)+'\n')
out={'status':'PASS_EXPLICIT_PRIVATE_RECOVERY_DAG_AND_INTEGER_ERROR','checks':len(checks),'interval_bits':iv.bits,
 'recovery_rounds':n,'corrections':reports,'correction_raw_counts':dict(total),
 'exact_macro_fixtures':fixtures,'amplified_inverse_counts':recovery,'private_preparation_counts':pre,
 'phase_branch_failure_upper':[str(Fraction(e[1],iv.D)) for e in failures],
 'complete_recovery_state_error_upper':str(state_error),'state_error_upper_decimal':f'{float(state_error):.16e}',
 'N_times_state_error_upper':str(Nrecovery*state_error),'N_times_state_error_decimal':f'{float(Nrecovery*state_error):.16e}',
 'full_N_times_state_error_upper':str((Nrecovery+229)*state_error),
 'actual_finite_q_collar_radius':'2^-30','actual_finite_cold_interval':as_decimal(cfinite),
 'actual_finite_dc_dq_interval':as_decimal(dcfinite),
 'actual_finite_q_interval_integer_endpoints':[str(v) for v in qcollar],
 'actual_finite_cold_interval_integer_endpoints':[str(v) for v in cfinite],
 'actual_finite_dc_dq_interval_integer_endpoints':[str(v) for v in dcfinite],
 'interval_scale_integer':str(iv.D),
 'actual_finite_J_gain':'-2*r*z*c(q)*c_prime(q)/(1-z+z*c(q)^2)>0 for0<z<1; no physical z or geometry gain fitted',
 'full_fixture_stage_count_with_front_births_and_literal_six_copy_archive':229+Nrecovery,
 'full_fixture_clock_dimension':8741756+1024*Nrecovery,'full_fixture_final_dimension':65536,'minimum_birth_age':132,
 'raw_lower_levels_executed':[0,1,2],'full_huge_raw_word_executed':False,
 'whole_H1_or_physical_C':False,'GR_closed':False}
(HERE/'CERTIFIED_CORRECTIONS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('corrections','exact_macro_fixtures','phase_branch_failure_upper','complete_recovery_state_error_upper','N_times_state_error_upper')},indent=2))
