#!/usr/bin/env python3
"""Exact sparse all-column checks in the owning Golden coefficient field."""
from pathlib import Path
import hashlib,importlib.util,json,random,sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"round14"))
import native_boolean as nb
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('a14_native',source);nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
K=nt.GOLDEN_FIELD;zero=K.zero;one=K.one;a=K.convert(nt.A);p=K.convert(nt.P)
N=8;PORT=4;SPIN=(5,6);OLD=(7,)


def rotation_pair(power):
    def cmul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
    out=(one,zero);base=(a,p)
    while power:
        if power&1:out=cmul(out,base)
        power//=2
        if power:base=cmul(base,base)
    return out


def rotate(state,wire,c,s):
    out={};mask=1<<(N-1-wire)
    for index,value in state.items():
        for destination,weight in [(index,c),(index^mask,-s if index&mask else s)]:
            out[destination]=out.get(destination,zero)+weight*value
    return {i:v for i,v in out.items() if v!=zero}


def run(word,state):
    for g in word:
        op=g['op'];w=g['wires']
        if op=='G':state=rotate(state,w[0],a,p);continue
        out={}
        for index,value in state.items():
            if op=='CX':
                if (index>>(N-1-w[0]))&1:index^=1<<(N-1-w[1])
            else:
                assert op=='SourceI' and w==[PORT,*SPIN]
                if (index>>(N-1-PORT))&1:
                    if ((index>>(N-1-SPIN[0]))^(index>>(N-1-SPIN[1])))&1:value=-value
                    index^=1<<(N-1-SPIN[1])
            out[index]=out.get(index,zero)+value
        state={i:v for i,v in out.items() if v!=zero}
    return state


def expected(name,k,column):
    state={column:one};target=2;aux=3
    if name in ('X','H'):
        if (column>>(N-1-target))&1:state={column:-one}
        return rotate(state,target,*rotation_pair((4 if name=='X' else 2)*k))
    control=((column>>(N-1-0))&1) and ((column>>(N-1-1))&1)
    if not control:return state
    if (column>>(N-1-target))&1:state=rotate(state,aux,*rotation_pair(8*k))
    return rotate(state,target,*rotation_pair(4*k))


reports=[]
for name in ('X','H','CCX'):
    for k in (1,2):
        tree=nb.boolean_word(name,k);nb.validate_schema(tree,N,PORT,SPIN,OLD)
        word=list(nb.expand(tree,1000))
        native=nt.Execution(N,(),OLD,tuple(nt.Gate(g['op'],tuple(g['wires'])) for g in word),nt.G_CX_SOURCE_I,PORT,SPIN)
        nt.validate_execution(native,max_qubits=N,max_expanded_stages=1000)
        # SourceI targets only declared port/Spin. No logical control can be
        # a target of either G or CX, even during routed inverse powers.
        assert all(not(g['op']=='G' and g['wires'][0] in (0,1)) and
                   not(g['op']=='CX' and g['wires'][1] in (0,1)) for g in word)
        for column in range(2**N):assert run(word,{column:one})==expected(name,k,column),(name,k,column)
        inverse=nb.inverse_literal(tree,PORT,SPIN);nb.validate_schema(inverse,N,PORT,SPIN,OLD)
        invword=list(nb.expand(inverse,1000));rng=random.Random(1400+k)
        for _ in range(16):
            column=rng.randrange(2**N);assert run(invword,run(word,{column:one}))=={column:one}
        known_forward=(4*k+8 if name=='X' else 2*k+8 if name=='H' else 12*k+92)
        known_reverse=(44*k+12 if name=='X' else 22*k+12 if name=='H' else 96*k+140)
        assert len(word)==known_forward and len(invword)==known_reverse
        reports.append({'name':name,'k':k,'all_exact_columns':2**N,'forward_counts':nb.counts(tree),
                        'literal_reverse_counts':nb.counts(inverse),'exact_inverse_cases':16})
        print(name,k,'all256 columns exact; raw inverse exact',flush=True)

# Hostile: an approximate CCX is not itself its raw inverse. It leaves a
# correlated auxiliary error even though the ideal CCX target has I_aux.
t=nb.boolean_word('CCX',1);word=list(nb.expand(t,1000))
hostile=3<<(N-2)  # both control bits 1, remaining wires 0
assert run(word,run(word,{hostile:one}))!={hostile:one}
result={'historical_checker_sha256': '4d3a358dc29b43222b5d1d4253e935c1dd5da224ead4b91de001bc8a3e5a2060', 'spin_representation': 'owned L_i=diag(J,-J), both Spin bits included', 'historical_files_modified': False, 'status':'PASS_A14_WORDS_WITH_OWNED_SPIN_REPRESENTATION','native_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'reports':reports,'all_exact_columns_total':sum(x['all_exact_columns'] for x in reports),
        'raw_reverse_total_cases':sum(x['exact_inverse_cases'] for x in reports),
        'approximate_CCX_reused_as_inverse_hostile_detected':True,
        'target_of_CCX':'CCX tensor I_aux, with arbitrary incoming aux/port/Spin/oldRIGHT',
        'scope':'Small k fully expanded actual native words; certified huge-k errors and unexpanded DAG are separate.',
        'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'A14_OWNED_SPIN_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
