#!/usr/bin/env python3
"""Full small signed columns, actual addresses, routed copy and sign checks."""
from collections import Counter
from pathlib import Path
from itertools import product
import cmath,hashlib,json,math,random
import source_select as s
P=Path(__file__).resolve().parent
rng=random.Random(1633)


def run(word,state):
    phase=1
    for op,*w in word:
        if op=='X':state^=1<<w[0]
        elif op=='CX':state^=((state>>w[0])&1)<<w[1]
        elif op=='CCX':state^=(((state>>w[0])&(state>>w[1]))&1)<<w[2]
        elif op=='Z':phase*=(-1)**((state>>w[0])&1)
        elif op=='CZ':phase*=(-1)**(((state>>w[0])&(state>>w[1]))&1)
        else:raise ValueError(op)
    return state,phase


def prepare_pair(plan,a,b,x,h,delta):
    state=0;q=plan['layout']
    for key,value in [('a',a),('b',b),('data',x),('h',h),('delta',delta)]:state=s.logic.put(state,q[key],value)
    return state


def expected_pair(plan,a,b,x,h,delta,state):
    member=(x==a)^(x==b)
    dest=x^(a^b) if h and member else x
    phase=-1 if h and delta and not member else 1
    return s.logic.put(state,plan['layout']['data'],dest),phase


small_cases=0
for n in (2,3,4):
    plan=s.pair_plan(n);word=list(s.ideal_gates(plan['logical_IR']))
    readonly=set(plan['layout']['a']+plan['layout']['b']+plan['layout']['h']+plan['layout']['delta'])
    assert all(g[-1] not in readonly for g in word)
    for a,b,x,h,delta in product(range(1<<n),range(1<<n),range(1<<n),(0,1),(0,1)):
        initial=prepare_pair(plan,a,b,x,h,delta)
        actual=run(word,initial);expected=expected_pair(plan,a,b,x,h,delta,initial)
        assert actual==expected,(n,a,b,x,h,delta)
        back,phase2=run(list(s.ideal_gates(plan['logical_IR'],True)),actual[0])
        assert back==initial and phase2*actual[1]==1
        small_cases+=1

binding=json.loads((P.parent/'round11/PERIODIC_SOURCE_BINDING.json').read_text())
pairs=[]
for site in binding['site_bindings']:
    for leaf,address in zip(binding['leaf_templates'],site['leaf_addresses_in_template_order']):
        if leaf['kind']=='Choi':pairs.append((22,0,(address<<10)|(leaf['input']<<5)|leaf['output']))
        else:pairs.append((12,*[(address<<4)|mask for mask in leaf['cross_masks']]))
plans={n:s.pair_plan(n) for n in (12,22)}
words={n:list(s.ideal_gates(plans[n]['logical_IR'])) for n in plans}
actual_cases=0
selected=[pairs[i] for i in range(0,len(pairs),173)]+[p for p in pairs[-282:] if p[0]==12]
for n,a,b in selected:
    assert a!=b
    complement=(1<<n)-1
    if complement in (a,b):complement=2
    for x,h,delta in product([a,b,complement],(0,1),(0,1)):
        initial=prepare_pair(plans[n],a,b,x,h,delta)
        # A separate dirty spectator demonstrates that it is never addressed.
        initial|=1<<plans[n]['wire_count']
        assert run(words[n],initial)==expected_pair(plans[n],a,b,x,h,delta,initial)
        actual_cases+=1

# Whole fixed instruction: selected copy, negative phase, immutable fields,
# independent delta per copy and identity on all CAR RIGHT spectators.
plan=s.instruction_plan([2,2]);q=plan['layout'];tree=s.instruction_ir(plan);word=list(s.ideal_gates(tree))
record=sum([q[key] for key in ['negative','leaf','coffset','qoffset','kind','a','b']],[])
readonly=set(record+q['h']+q['delta_choi']+q['delta_car']+sum(q['CAR_RIGHT'],[]))
assert all(g[-1] not in readonly for g in word)
instruction_cases=0
for trial in range(1600):
    n,a,b=pairs[rng.randrange(len(pairs))];kind=1 if n==22 else 2
    if trial%13==0:kind=3  # Defined invalid-kind extension: only constant phase.
    index=trial%4;negative=trial%2;h=(trial//2)%2
    fields=[negative,trial%283,index,index,kind,a,b]
    initial=s.logic.put(0,record,s.dispatch.pack(fields,[1,9,7,2,2,22,22]))
    initial=s.logic.put(initial,q['h'],h)
    for reg in q['choi']+q['car']+q['CAR_RIGHT']:
        initial=s.logic.put(initial,reg,rng.getrandbits(len(reg)))
    for key in ['delta_choi','delta_car']:initial=s.logic.put(initial,q[key],rng.randrange(4))
    want_phase=(-1)**(h*negative);wanted=initial
    if kind in (1,2) and index<2:
        data=q['choi'][index] if kind==1 else q['car'][index]
        delta=q['delta_choi'][index] if kind==1 else q['delta_car'][index]
        x=[a,b,(1<<len(data))-1][trial%3]
        initial=s.logic.put(initial,data,x);wanted=initial
        member=(x==a)^(x==b)
        if h and member:wanted=s.logic.put(wanted,data,x^(a^b))
        if h and ((initial>>delta)&1) and not member:want_phase*=-1
    assert run(word,initial)==(wanted,want_phase),(trial,kind,index,a,b)
    instruction_cases+=1


def quantum_gate(state,gate):
    op,*w=gate;out={}
    if op=='H':
        q=w[0]
        for x,z in state.items():
            base=x&~(1<<q);bit=(x>>q)&1
            for y,c in [(base,1/math.sqrt(2)),(base|(1<<q),(-1)**bit/math.sqrt(2))]:out[y]=out.get(y,0)+z*c
    else:
        for x,z in state.items():
            y,phase=run([gate],x);out[y]=out.get(y,0)+z*phase
    return {x:z for x,z in out.items() if abs(z)>1e-14}


# Target Hadamard test including the A12 convention bit=1 means plus sign.
hadamard_cases=0
plan=s.pair_plan(3);q=plan['layout'];word=list(s.ideal_gates(plan['logical_IR']));h=q['h'][0]
for a,b,delta in [(0,7,0),(2,5,1)]:
    outside=next(i for i in range(8) if i not in (a,b))
    for coeff in [{a:1},{outside:1},{a:1/math.sqrt(2),b:1/math.sqrt(2)},
                  {a:1/math.sqrt(2),b:-1/math.sqrt(2)},{a:1/math.sqrt(2),b:1j/math.sqrt(2)}]:
        initial={prepare_pair(plan,a,b,x,0,delta):z for x,z in coeff.items()}
        target=sum(z.conjugate()*coeff.get(x^(a^b),0) if x in (a,b) else (-1)**delta*abs(z)**2 for x,z in coeff.items()).real
        state=initial
        for g in [('H',h)]+word+[('H',h),('X',h)]:state=quantum_gate(state,g)
        expectation=sum((1 if (x>>h)&1 else -1)*abs(z)**2 for x,z in state.items())
        assert abs(expectation-target)<2e-13,(expectation,target)
        assert abs(sum(abs(z)**2 for z in state.values())-1)<2e-13
        hadamard_cases+=1

compiled=json.loads((P/'SOURCE_SELECT_COMPILATION.json').read_text());library=json.loads((P/'DYNAMIC_PAIR_LIBRARY.json').read_text());k=int(library['k'])
assert compiled['source_sha256']==hashlib.sha256((P/'source_select.py').read_bytes()).hexdigest()
for name,w in compiled['walks'].items():
    plan=s.instruction_plan(w['root']['degree']);counts=Counter(g[0] for g in s.ideal_gates(s.instruction_ir(plan)))
    assert dict(counts)==w['instruction_logical_counts']
for n in (12,22):
    p=library['templates'][str(n)];c=Counter(g[0] for g in s.ideal_gates(p['logical_IR']))
    assert c==Counter({'X':8,'CX':24*n-4,'CCX':10*n-8,'Z':1,'CZ':1})
    assert p['logical_gate_counts']==dict(c)
    port=p['native_layout']['port'];spin=tuple(p['native_layout']['spin'])
    actual=s.native_resource(p['native_forward_DAG'],port)
    assert s.encode_resource(actual)==p['native_forward_resources']
    inverse=s.nb.inverse_literal(p['native_forward_DAG'],port,spin)
    assert inverse==p['native_literal_reverse_DAG']
    assert s.native_resource(inverse,port)==s.raw_reverse_resource(actual)

out={'status':'PASS_DYNAMIC_PAIR_COPY_SELECT_AND_HADAMARD_CONVENTION',
 'input_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['source_select.py','DYNAMIC_PAIR_LIBRARY.json','SOURCE_SELECT_COMPILATION.json']},
 'all_clean_work_small_columns_n2_to4':small_cases,'actual_A11_address_signed_columns':actual_cases,
 'whole_instruction_copy_phase_cases':instruction_cases,'Hadamard_sign_tests':hadamard_cases,
 'exact_pair_logical_counts':'X=8, CX=24n-4, CCX=10n-8, Z=1, CZ=1 for n>=3',
 'literal_native_reverse_shape_checked':True,'huge_native_word_executed':False,
 'full_global_physical_assembler':False,'full_source_alpha_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'SOURCE_SELECT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ['status','all_clean_work_small_columns_n2_to4','actual_A11_address_signed_columns','whole_instruction_copy_phase_cases','Hadamard_sign_tests']}))
