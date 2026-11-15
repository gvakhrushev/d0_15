#!/usr/bin/env python3
"""Independent 13-arm padded schedule and growing-dimension audit."""
from pathlib import Path
from collections import Counter
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round49');sys.path.insert(0,str(D));import two_bit_paid_family as f
sam=(0,1,2);cfg={'n':5,'sam':sam,'m':3,'coreL':9,'controlL':8,'postL':5,'probeL':6,'K':3};cfg['Lbase']=9+4*8+5+6;cfg['Nbase']=cfg['n']+cfg['Lbase']
C1,C2=f.CUTS
calls=Counter()
def core():
 calls['core']+=1;yield {'op':'G','wires':[3]};yield {'op':'B82_CUT','name':C1};yield {'op':'CX','wires':[3,4]};yield {'op':'B82_CUT','name':C2};yield {'op':'G','wires':[4]}
def post():calls['post']+=1;yield {'op':'G','wires':[2]}
def control(axis,sign):
 calls['control']+=1
 for _ in range({-1:2,0:0,1:1}[sign]):yield {'op':'G','wires':[0]}
def probe(plane,sign):calls['probe']+=1;yield {'op':'G','wires':[1]}
def flattened(arm,sign):
 blocks=list(f.family_blocks(cfg,core,post,control,probe,arm=arm,sign=sign,axis=0,plane=(0,1),keep_marks=True));events=[]
 for tree in blocks:
  if tree['op']=='B82_CUT':events.append(('mark',tree['name']))
  else:events.extend((x['op'],tuple(x['wires'])) for x in f.target.e.leaves(tree))
 return events
arms=[('centre',0)]+[(k,z) for k in ('matched','Pf','Qf','Qb','Pb','post_probe') for z in (-1,1)]
for arm,sign in arms:
 calls.clear();e=flattened(arm,sign);marks=[(i,v) for i,v in enumerate(e) if v[0]=='mark'];assert [z[1][1] for z in marks]==[C1,C2]
 plain=[z for z in e if z[0]!='mark'];assert len(plain)==cfg['Lbase']
 # The two original marks occur at the same native layer in every arm.
 positions=[sum(1 for x in e[:i] if x[0]!='mark') for i,_ in marks];assert positions==[9,18]
 first=e[:marks[0][0]-1];assert len(first)==8
 qf=e[marks[0][0]+1:marks[0][0]+9];qb=e[marks[1][0]+1:marks[1][0]+9]
 # After Qb: core last G, six exact padding calls, then the Pb slot.
 pb=e[marks[1][0]+9+1+6:marks[1][0]+9+1+6+8]
 got=[sum(z==('G',(0,)) for z in span) for span in (first,qf,qb,pb)]
 signs=f.slot_signs(arm,sign);want=[{-1:2,0:0,1:1}[signs[k]] for k in ('Pf','Qf','Qb','Pb')];assert got==want,(arm,sign,got,want)
 assert calls['core']==1 and calls['post']==1 and calls['control']==4 and calls['probe']==int(arm=='post_probe')
# Compute D from the actual emitted birth/gate chronology, not the closed formula.
birth_dims=[];dim=1
for event in f.execution_stages(cfg,lambda:iter([])):
 birth_dims.append(dim)
 if event['kind']=='canonical_RAW_birth':dim*=2
# Insert L_base square stages between early births and retention.
n=cfg['n'];K=cfg['K'];actual=sum(birth_dims[:n])+cfg['Lbase']*(1<<n)+sum(birth_dims[n:])
formula=(1<<n)*(cfg['Lbase']-2+3*(1<<K))-1;assert actual==formula and dim==1<<(n+K)
out={'status':'PASS_INDEPENDENT_13_ARMS_PAD_MARKS_CLOCK','arms_checked':len(arms),'four_independent_slot_signs_and_matched_order_checked':True,'original_mark_layers_equal_in_all_arms':True,'fixed_post_and_distinct_post_probe_checked':True,'all_words_equal_exact_padded_length':True,'small_clock_dimension_directly_summed':True,'early_births':n,'retention_pairs':K,'huge_production_word_executed':False,'GR_closed':False}
(P/'FOUR_SLOT_SCHEDULE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
