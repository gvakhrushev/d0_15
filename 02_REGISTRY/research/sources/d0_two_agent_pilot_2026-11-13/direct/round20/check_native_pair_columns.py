#!/usr/bin/env python3
"""Exact small native pair columns from the actual A20 source bindings."""
from pathlib import Path
import hashlib,json
import coframe_native as n
P=Path(__file__).resolve().parent;lib=json.loads((P/'COFRAME_ANGLE_LIBRARY.json').read_text());lay=n.layout()
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def cs(exponent):
    c,s=one,zero
    for _ in range(exponent):c,s=add(ma(c),neg(mp(s))),add(mp(c),ma(s))
    return c,s
def run(word,state):
    for g in word:
        op=g['op'];w=g['wires'];out={}
        if op=='G':
            for x,z in state.items():
                bit=(x>>w[0])&1;base=x&~(1<<w[0]);p=neg(mp(z)) if bit else ma(z);q=ma(z) if bit else mp(z)
                out[base]=add(out.get(base,zero),p);j=base|(1<<w[0]);out[j]=add(out.get(j,zero),q)
        elif op=='CX':
            for x,z in state.items():j=x^(((x>>w[0])&1)<<w[1]);out[j]=add(out.get(j,zero),z)
        else:
            assert op=='SourceI'
            for x,z in state.items():
                bit=(x>>w[0])&1;parity=((x>>w[1])^(x>>w[2]))&1;j=x^(bit<<w[2]);out[j]=add(out.get(j,zero),neg(z) if bit and parity else z)
        state={x:v for x,v in out.items() if v!=zero}
    return state
row=next(r for r in lib['catalogue']['f'] if r['SAM_indices'])
angle=next(iter(lib['angles'].values()));reports=[]
for mode in (1,2,3):
    for a,b,sign in n.t.fact.fock_pairs(mode):
        bound=n.pair_bound(row,lay['choi_output'][:4],a,b,angle,lay)
        mapping={w:i for i,w in enumerate(lay['choi_output'][:4])};mapping[lay['branch']]=4
        cp=[(mapping[c],p) for c,p in zip(bound['controls'],bound['pattern']) if c in mapping]
        small={'K':len(cp),'controls':[c for c,p in cp],'pattern':[p for c,p in cp],'target':mapping[bound['target']],
               'k':1,'permutation':[n.nb.gate(g['op'],*[mapping[w] for w in g['wires']]) for g in bound['permutation']]}
        slay={'port':5,'spin':[6,7]};word=[g for tree in n.unit_blocks(small,0,slay) for g in n.nb.expand(tree,100000)]
        inverse=[g for tree in n.unit_blocks(small,1,slay) for g in n.nb.expand(tree,100000)];co,si=cs(1<<small['K'])
        for col in range(512):
            state={col:one};grade=col&15
            if ((col>>4)&1) and grade in (a,b):state={col:co,col^a^b:neg(si) if grade==a else si}
            actual=run(word,{col:one});assert actual==state,(mode,a,b,col)
            if col%32==0 or grade in (a,b):assert run(inverse,actual)=={col:one}
        reports.append({'mode':mode,'pair':[a,b],'CAR_parity':sign,'exact_columns':512,'small_K':small['K'],'forward_leaves':len(word)})
out={'status':'PASS_ACTUAL_A20_PAIR_BINDINGS_EXACT_SMALL_NATIVE_COLUMNS','library_sha256':hashlib.sha256((P/'COFRAME_ANGLE_LIBRARY.json').read_bytes()).hexdigest(),
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reports':reports,'exact_full_columns':sum(r['exact_columns'] for r in reports),
     'actual_SourceI_spin':'diag(J,-J)','tested_branch_grade_port_spin_oldRIGHT_all_columns':True,
     'scope':'Small power and reduced external predicate; source large-k interval bounds and full control bindings are separately checked.',
     'full_huge_word_executed':False,'GR_closed':False}
(P/'NATIVE_PAIR_COLUMNS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'exact_full_columns':out['exact_full_columns']}))
