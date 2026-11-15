#!/usr/bin/env python3
"""Exhaustive 4^6×5 interval targets; compact per-family receipts."""
from pathlib import Path
from hashlib import sha256
import multiprocessing as mp
import json,gzip,sys,time
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import proper_link_two_bit_targets as p
PREC=4096;LIMIT=3500
iv=None
def init():
 global iv
 iv=p.Interval(PREC)
def check(item):
 name,spec=item
 f=p.base.factor(iv,spec,{})
 L=p.base.givens(iv,f['L'],spec['type'] in ('identity','ref_rot_plus','ref_rot_minus'))
 R=p.base.givens(iv,f['R'],spec['type']=='identity');diag=p.base.diagonal_targets(iv,f)
 targets=[(v['cos'],v['sin']) for v in L+R]+[(diag[k]['cos'],diag[k]['sin']) for k in ((0,0),(1,0),(0,1))]
 digest=sha256();max_width=0
 for c,s in targets:
  c=(max(-iv.S,c[0]),min(iv.S,c[1]));s=(max(-iv.S,s[0]),min(iv.S,s[1]))
  assert c[0]<=c[1] and s[0]<=s[1]
  width=max(c[1]-c[0],s[1]-s[0]);assert width<(iv.S>>LIMIT),(name,'wide target')
  # Exact target unit circle must be enclosed. Dominant midpoint has magnitude >.6.
  lower=lambda x:0 if x[0]<=0<=x[1] else min(abs(x[0]),abs(x[1]))
  upper=lambda x:max(abs(x[0]),abs(x[1]))
  assert lower(c)**2+lower(s)**2<=iv.S**2<=upper(c)**2+upper(s)**2
  assert max(lower(c),lower(s))*10>6*iv.S
  max_width=max(max_width,int(width))
  digest.update(('|'.join(hex(int(x)) for x in (*c,*s))+'\n').encode())
 return {'family':name,'angle_count':len(targets),'target_sha256':digest.hexdigest(),'max_width_bits':max_width.bit_length(),'boost_lower_gt_zero':f['zero_boost_exact'] or f['h'][0]>0,'L':len(L),'R':len(R)}
def main():
 specs,cat=p.catalogue();fixed={row['family_id'] for v in cat.values() for row in v['fixed']}
 jobs=list(p.variable_specs())+[(name,specs[name]) for name in sorted(fixed)]
 assert len(jobs)==20480+len(fixed) and len({name for name,_ in jobs})==len(jobs)
 start=time.monotonic();angles=0;maxwidth=0
 with (P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz').open('wb') as raw:
  with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
   with mp.Pool(8,initializer=init) as pool:
    for index,r in enumerate(pool.imap(check,jobs,chunksize=8),1):
     stream.write((json.dumps(r,separators=(',',':'))+'\n').encode());angles+=r['angle_count'];maxwidth=max(maxwidth,r['max_width_bits'])
     if index%1024==0:print(index,'/',len(jobs),'seconds',round(time.monotonic()-start,1),flush=True)
 out={'status':'PASS_ALL_TWO_BIT_PROPER_LINK_TARGET_FAMILIES','variable_families':20480,'fixed_families':len(fixed),'all_families':len(jobs),'angles':angles,'precision_bits':PREC,'all_angle_interval_width_lt':'2^-3500','max_width_bits':maxwidth,'family_receipts_sha256':sha256((P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz').read_bytes()).hexdigest(),'fixed_map_unchanged':True,'candidate_power_or_float_used':False,'physical_C_closed':False,'GR_closed':False}
 (P/'FULL_TARGET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
