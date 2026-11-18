#!/usr/bin/env python3
"""All target names replayed independently at 4352-bit versus 4096-bit intervals."""
from pathlib import Path
from hashlib import sha256
import multiprocessing as mp
import json,gzip,sys,time
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import proper_link_two_bit_targets as t
lo=hi=None
def init():
 global lo,hi
 lo=t.Interval(4096);hi=t.Interval(4352)
def targets(iv,spec):
 f=t.base.factor(iv,spec,{})
 L=t.base.givens(iv,f['L'],spec['type'] in ('identity','ref_rot_plus','ref_rot_minus'))
 R=t.base.givens(iv,f['R'],spec['type']=='identity');D=t.base.diagonal_targets(iv,f)
 key=lambda v:[(q['i'],q['j'],q['selected_pivot']) for q in v]
 arr=[(v['cos'],v['sin']) for v in L+R]+[(D[k]['cos'],D[k]['sin']) for k in ((0,0),(1,0),(0,1))]
 return key(L),key(R),arr
def check(item):
 (name,spec),rec=item;assert name==rec['family'];a,b,A=targets(lo,spec);c,d,B=targets(hi,spec);assert a==c and b==d and len(A)==len(B)==rec['angle_count'];digest=sha256()
 for (C,S),(C1,S1) in zip(A,B):
  C=(max(-lo.S,C[0]),min(lo.S,C[1]));S=(max(-lo.S,S[0]),min(lo.S,S[1]));C1=(max(-hi.S,C1[0]),min(hi.S,C1[1]));S1=(max(-hi.S,S1[0]),min(hi.S,S1[1]))
  for x,y in ((C,C1),(S,S1)):assert (x[0]<<256)<=y[0]<=y[1]<=(x[1]<<256),(name,'containment')
  digest.update(('|'.join(hex(int(v)) for v in (*C,*S))+'\n').encode())
 assert digest.hexdigest()==rec['target_sha256'];return len(A)
def main():
 specs,cat=t.catalogue();fixed={row['family_id'] for v in cat.values() for row in v['fixed']};jobs=list(t.variable_specs())+[(name,specs[name]) for name in sorted(fixed)]
 with gzip.open(P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz','rt') as f:rows=[json.loads(line) for line in f]
 assert len(jobs)==len(rows)==20496;start=time.monotonic();total=0
 with mp.Pool(8,initializer=init) as pool:
  for i,k in enumerate(pool.imap(check,zip(jobs,rows),chunksize=8),1):
   total+=k
   if i%2048==0:print(i,'/',len(jobs),'seconds',round(time.monotonic()-start,1),flush=True)
 assert total==307416
 out={'status':'PASS_ALL_FAMILIES_REPLAY_4352_BITS','families':len(jobs),'angles':total,'every_4096bit_target_sha256_matches':True,'every_4352bit_target_interval_contained':True,'pivot_and_orientation_match':True,'methods':'replay of same exact target algebra at greater precision, not independent physical source proof','family_receipts_sha256':sha256((P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz').read_bytes()).hexdigest(),'GR_closed':False}
 (P/'FULL_PRECISION_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
