#!/usr/bin/env python3
"""Finite exact count algorithm. Expensive: evaluates all lazy k; supports shards.

Outputs exact G/CX/SourceI counts of B93 proper-link only. Does not expand words.
"""
from pathlib import Path
from collections import Counter
import json,argparse,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import proper_link_two_bit_native as n
import proper_link_two_bit_targets as t

def layout():
 d=n.old.prefix_compatible_global_layout()
 def shift(v):
  if isinstance(v,list):return [q+2688 for q in v]
  return v+2688
 d={k:(list(range(5376)) if k=='all_SAM' else shift(v)) for k,v in d.items()}
 return d

def work(shard,shards):
 specs,cat=t.catalogue();gl=layout();groups={}
 for bank,section in cat.items():
  for e in section['fixed']:
   name=e['family_id'];g=groups.setdefault((name,0),{'entry':e,'weight':Counter()});g['weight'][bank]+=1
  for template in section['variable']:
   xy=template['xy'];ids=template['indices_by_generator']
   from itertools import product
   for digits in product(range(4),repeat=6):
    name=t.family_id(xy,digits);e={'address':template['address'],'SAM_indices':ids+[2688+i for i in ids],'SAM_pattern':[d&1 for d in digits]+[(d>>1)&1 for d in digits],'family_id':name}
    g=groups.setdefault((name,12),{'entry':e,'weight':Counter()});g['weight'][bank]+=1
 keys=sorted(groups);assert len(keys)==20496
 fwd={b:Counter() for b in cat};rev={b:Counter() for b in cat};processed=0
 for idx,key in enumerate(keys):
  if idx%shards!=shard:continue
  g=groups[key];f=n.sector_cost(gl,g['entry']);r=n.sector_cost(gl,g['entry'],True)
  assert +r==+n.old.invert_cost(f)
  for bank,w in g['weight'].items():
   fwd[bank].update({k:w*v for k,v in f.items()});rev[bank].update({k:w*v for k,v in r.items()})
  processed+=1
  if processed%32==0:print('shard',shard,'families',processed,flush=True)
 out={'status':'EXACT_SHARDED_PROPER_LINK_ONLY_NATIVE_INVENTORY','shard':shard,'shards':shards,'processed_family_classes':processed,'bank_forward':{b:{k:hex(v) for k,v in c.items()} for b,c in fwd.items()},'bank_literal_inverse':{b:{k:hex(v) for k,v in c.items()} for b,c in rev.items()},'sourceI_replacement_included':False,'complete_history_included':False,'GR_closed':False}
 path=P/f'EXACT_INVENTORY_SHARD_{shard}_OF_{shards}.json';path.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--shard',type=int,default=0);ap.add_argument('--shards',type=int,default=1);args=ap.parse_args();assert 0<=args.shard<args.shards;work(args.shard,args.shards)
