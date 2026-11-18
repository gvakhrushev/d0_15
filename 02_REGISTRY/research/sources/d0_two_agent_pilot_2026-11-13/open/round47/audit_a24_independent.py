#!/usr/bin/env python3
"""Independent A24 composition inventory and literal inverse skeleton audit."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round24'));import full_car_source as a
l=a.layout();nb=a.nb;port=l['port'];spin=tuple(l['spin']);banks=('y+','y-','f','0','x+','x-','q');plan=json.loads((D/'round24/FULL_CAR_SOURCE_PLAN.json').read_text())
for p,h in plan['source_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h
assert len(l['SAM'])==2688 and len(l['internal_SITE'])==8 and len(l['grade'])==4 and len(l['RIGHT'])==7 and len(a.private(l))==3
assert len(set(l['SAM']+l['internal_SITE']+l['grade']+l['RIGHT']+[l['port'],*l['spin'],l['oldRIGHT_witness'],*a.private(l),l['native_aux_arbitrary']]))==2715

def inv(t):
 op=t['op']
 if op=='seq':return nb.seq(*(inv(x) for x in reversed(t['children'])))
 if op=='repeat':return nb.repeat(int(t['count']),inv(t['child']))
 if op=='CX':return t
 if op=='SourceI':return nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];s=nb.gate('SourceI',port,*spin);core=nb.seq(s,s,nb.repeat(1,nb.gate('G',port)),s,s)
 if q==port:return core
 def swap(x,y):return nb.seq(nb.gate('CX',x,y),nb.gate('CX',y,x),nb.gate('CX',x,y))
 return nb.seq(swap(q,port),core,swap(q,port))
def invd(t,d):
 for _ in range(d):t=inv(t)
 return t
def resources(t):
 op=t['op']
 if op=='seq':
  c=Counter()
  for x in t['children']:c.update(resources(x))
  return c
 if op=='repeat':return Counter({k:v*int(t['count']) for k,v in resources(t['child']).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def inverseprice(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
def eqc(x,y):return all(x[k]==int(y.get(k,0)) for k in ('G_port','G_other','CX','SourceI'))
U,Ui,R=a.f.fixed_components(l);assert Ui==inv(U);ur=resources(U);uir=resources(Ui);rr=resources(R);assert +uir==+inverseprice(ur)
lib=a.library();material={};sectors={}
for bank in ('y+','y-','q'):
 c=Counter();n=0
 for row in lib['catalogue'][bank]:
  for rot in lib['vectors'][row['vector_id']]['rotations']:
   if rot['angle_id'] is None:continue
   # Independently calculate Gray/Walsh counts, based on declared control counts and target plane.
   other=rot['other'];diff=1^other;pivot=(diff&-diff).bit_length()-1;flips=sum((diff>>j)&1 for j in range(4) if j!=pivot)
   klen=8+len(row['SAM_indices'])+3;terms=1<<klen;assert klen in (11,13)
   gpattern=[((1 ^ (sum((1<<j) for j in range(4) if j!=pivot and diff>>j&1) if 1>>pivot&1 else 0))>>j)&1 for j in range(4) if j!=pivot]
   pattern=[(row['site']>>j)&1 for j in range(8)]+row['SAM_pattern']+gpattern
   neg=terms//2 if any(pattern) else 0;k=int(lib['angles'][rot['angle_id']]['k'])*(2**(13-klen))
   c.update({'G_port':neg*k,'G_other':(terms-neg)*k,'CX':klen*terms+6*neg+2*flips,'SourceI':4*neg});n+=1
 material[bank]=c;sectors[bank]=n
vac=json.loads((D/'round23/CAR_VACUUM_PREFIX_PLAN.json').read_text())['native_prefix_forward'] if False else a.v.inventory(l)['prefix_forward']
raw=Counter(G_port=3,CX=18,SourceI=12);checks={}
for b in banks:
 frame=ur+uir+rr+rr
 if b in material:frame+=material[b]+inverseprice(material[b])
 else:frame+=ur+uir
 total=raw+vac+frame
 for name,val in [('predicate3_RAW_to_zero',raw),('vacuum19_RAW_prefix',vac),('CAR_frame',frame),('source_forward',total),('source_literal_inverse',inverseprice(total))]:assert eqc(val,plan['all7_banks'][b]['native'][name]),(b,name)
 checks[b]=True
# Full source wrapper with a short list of real, not synthetic, emitted blocks.
# Material list includes end/start of two real controlled-rotation sectors.
samples={}
for b in ('y+','y-','q'):
 found=[]
 for row in lib['catalogue'][b]:
  for rot in lib['vectors'][row['vector_id']]['rotations']:
   if rot['angle_id'] is None:continue
   bound=a.f.m.bind_plane(row,rot,l,lib['angles']);first=next(a.f.m.pair_blocks(bound,l));last=next(a.f.m.pair_blocks(bound,l,True));found.append((first,inv(last)))
   if len(found)==2:break
  if len(found)==2:break
 samples[b]=[q for pair in found for q in pair]
# Independent blockwise wrapper proof for actual U, R, three actual RAW macros,
# actual A23 prefix samples, and material samples, at four literal depths.
from itertools import islice
vlist=list(islice(a.v.prefix_blocks(l,0,[*a.private(l),l['native_aux_arbitrary']]),4));original_material=a.f.m.preparation_blocks;original_v=a.v.prefix_blocks
reports=[]
try:
 for b in banks:
  ms=samples.get(b,[])
  def repl_mat(bank,library,lay=None,reverse=False):
   src=samples[bank];yield from ([inv(x) for x in reversed(src)] if reverse else src)
  def repl_v(lay=None,depth=0,extra_external=()):yield from [invd(x,depth) for x in (reversed(vlist) if depth%2 else vlist)]
  a.f.m.preparation_blocks=repl_mat;a.v.prefix_blocks=repl_v
  rawblocks=[nb.rotation_power(q,-1,port,spin) for q in a.private(l)]
  frame=[Ui,R,U]+([inv(x) for x in reversed(ms)] if b in samples else [Ui])+[R]+(ms if b in samples else [U])
  want=rawblocks+vlist+frame
  for depth in range(4):
   got=list(a.source_blocks(b,l,depth));assert got==want,(b,depth,len(got),len(want));reports.append({'bank':b,'depth':depth,'blocks':len(got)})
   want=[inv(x) for x in reversed(want)]
finally:a.f.m.preparation_blocks=original_material;a.v.prefix_blocks=original_v
prefix=18*Fraction(1,2**3264)+15*Fraction(1,2**4096);delta=Fraction(1,2**4096)
allerr=sum((16*(prefix+(28*delta if b in material else 0)) for b in banks),Fraction())
assert allerr==Fraction(int(plan['all112_error_numerator_hex'],16),int(plan['all112_error_denominator_hex'],16))
assert allerr<Fraction(1,2**3253)
out={'status':'PASS_A24_INDEPENDENT_WRAPPER_PRICE_AND_ERROR','source_sha256':{str(D/'round24'/x):sha256((D/'round24'/x).read_bytes()).hexdigest() for x in ('full_car_source.py','FULL_CAR_SOURCE_PLAN.json','check_full_car_source.py','FULL_CAR_SOURCE_CHECK.json')},'independent_material_sector_prices':sectors,'all7_bank_components_and_inverse_prices':checks,'actual_block_subset_wrapper_tests':reports,'all112_error_strict_lt':'2^-3253','input_scope':'arbitrary 19 source columns and external factors, predicate3 true RAW v; ideal hybrid retains predicate zero','real_full_material_stream_exhaustively_replayed':False,'real_giant_powers_expanded':False,'old_marked_prefix_bound':False,'physical_admission_and_T6_proved':False,'GR_closed':False}
(P/'A24_INDEPENDENT_COMPOSITION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'literal_depth_tests':len(reports),'material_rotations':sectors,'all112_error_strict_lt':'2^-3253'}))
