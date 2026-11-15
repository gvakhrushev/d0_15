#!/usr/bin/env python3
"""Independent coverage, grid identities, and direct native-power witnesses."""
from pathlib import Path
from hashlib import sha256
from itertools import product,islice
from collections import Counter
import json,gzip,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import proper_link_two_bit_targets as t
import proper_link_two_bit_native as n
import certify_short_grid as grid
import exact_resource_inventory as inv
j=json.loads((P/'SHORT_GRID_CERTIFICATE.json').read_text());assert j==grid.build(29)
for K in (15,24,46):assert json.loads((P/f'SHORT_GRID_K{K}_E3460.json').read_text())==grid.build(K)
receipt=json.loads((P/'FULL_TARGET_CHECK.json').read_text());rp=P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz'
assert sha256(rp.read_bytes()).hexdigest()==receipt['family_receipts_sha256']
rows=[]
with gzip.open(rp,'rt') as f:
 for line in f:rows.append(json.loads(line))
names=[r['family'] for r in rows];expected={x for x,_ in t.variable_specs()};specs,cat=t.catalogue()
fixed={row['family_id'] for v in cat.values() for row in v['fixed']};assert len(fixed)==16
assert len(rows)==20496 and len(set(names))==20496 and set(names)==expected|fixed
assert sum(r['angle_count'] for r in rows)==307416 and all(r['boost_lower_gt_zero'] and r['max_width_bits']<4096-3500 for r in rows)
# Full enumeration of logical local masks, not native 2^K masks or giant powers.
count=Counter();last=None;all_names=expected|fixed
for bank in cat:
 for e in t.entries(bank,cat):
  ids=e['SAM_indices'];pat=e['SAM_pattern'];assert len(ids)==len(pat) and len(ids) in (0,12)
  if ids:
   assert ids[6:]==[2688+i for i in ids[:6]] and len(set(ids))==12
   digits=tuple(pat[i]+2*pat[i+6] for i in range(6));assert e['family_id'].endswith(''.join(map(str,digits)))
  assert e['family_id'] in all_names;count[bank]+=1;last=e
assert count['f']==1049344 and all(count[b]==1024 for b in cat if b!='f')
# The provider uses family-major order to reuse angle synthesis. Verify its
# complete count and that the reverse iterator is the literal reverse order.
for bank in cat:
 section=cat[bank];total=len(section['fixed'])+4096*len(section['variable'])
 first=list(islice(n.bank_entries(bank),32));back=list(islice(n.bank_entries(bank,True),total-32,total))
 assert first==list(reversed(back))
 assert sum(1 for _ in n.bank_entries(bank))==total==count[bank]
# Independently check real G^(2^29*k) by complex balls at 7168 bits, on
# three structurally distinct families and both controlled X targets.
iv=t.Interval(7168);S=iv.S;bits=7168
def mult(x,y):
 c,s,r=x;C,T,R=y
 return ((c*C-s*T)>>bits,(c*T+s*C)>>bits,r+R+((r*R+S-1)>>bits)+2)
a,b=iv.c['sqrtp'],iv.c['p'];powers=[(a[0],b[0],a[1]-a[0]+b[1]-b[0])]
for _ in range(n.Q.bit_length()+31):powers.append(mult(powers[-1],powers[-1]))
def power(k):
 x=(S,0,0);v=k<<29;i=0
 while v:
  if v&1:x=mult(x,powers[i])
  v>>=1;i+=1
 c,s,r=x;return (c-r,c+r),(s-r,s+r)
def verify(k,c,s):
 c=(max(-S,c[0]),min(S,c[1]));s=(max(-S,s[0]),min(S,s[1]));a,b=power(int(k));err=max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-s[1]),abs(b[1]-s[0]));assert err<S>>3456
families=['v_none_000000','v_11_123012','ref_boost'];checked=0
for name in families:
 record=n.family(name)
 if name.startswith('v_'):
  _,xy,digits=name.split('_');spec={'type':'f','xy':None if xy=='none' else tuple(map(int,xy)),'bits':tuple(map(int,digits))}
 else:spec=specs[name]
 fac=t.base.factor(iv,spec,{})
 for lab in ('L','R'):
  ident=spec['type']=='identity' or lab=='L' and spec['type'] in ('ref_rot_plus','ref_rot_minus')
  for r,v in zip(record[lab],t.base.givens(iv,fac[lab],ident)):
   assert (r['i'],r['j'])==(v['i'],v['j']);verify(r['k'],v['cos'],v['sin']);checked+=1
 for key,v in t.base.diagonal_targets(iv,fac).items():
  if key==(1,1):continue
  verify(record['diagonal'][''.join(map(str,key))]['k'],v['cos'],v['sin']);checked+=1
x=n.controlled_x();verify(x['k'],iv.zero,iv.one);verify(x['phase']['k'],iv.neg(iv.one),iv.zero);checked+=2
# Physical layout and actual lazy first blocks, no 2^29 traversal.
entry=next(e for e in t.entries('f',cat) if e['SAM_indices']);lay=inv.layout();bound=n.bind(lay,entry)
cmd=list(n.old.commands(bound,entry,n.family(entry['family_id']),n.controlled_x()))
assert max(len(q['controls'])+(1 if q['kind']=='X' else 0) for q in cmd)==29
for rev in (False,True):
 blocks=list(islice(n.sector_blocks(lay,entry,rev),3));assert len(blocks)==3
 counts=n.sector_cost(lay,entry,rev)
 if not rev:forward=counts
 else:assert +counts==+n.old.invert_cost(forward)
upper=json.loads((P/'PROPER_LINK_RESOURCE_UPPER.json').read_text());assert upper['status']=='SAFE_COMPONENTWISE_UPPER_NOT_ACTUAL_PRICE'
for rev in (False,True):
 c=n.sector_cost(lay,entry,rev)
 row=upper['bank_bounds']['f']['literal_inverse_componentwise_upper_hex' if rev else 'forward_componentwise_upper_hex']
 assert all(v<=int(row[k],16) for k,v in c.items())
out={'status':'PASS_FULL_CATALOGUE_GRID_AND_INDEPENDENT_NATIVE_POWER_WITNESSES','all_family_names_checked':len(names),'all_catalogue_sectors_checked':sum(count.values()),'bank_sector_counts':dict(count),'independent_direct_power_angles_sample':checked,'sample_scope':'three target families and controlled X; global angles guaranteed by certified uniform short grid plus exhaustive target bounds','family_major_provider_sector_counts_and_reverse_order':True,'actual_lazy_provider_smoke':True,'actual_exact_full_inventory_evaluated':False,'sourceI_replacement_compiled':False,'physical_C_closed':False,'GR_closed':False}
(P/'INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
