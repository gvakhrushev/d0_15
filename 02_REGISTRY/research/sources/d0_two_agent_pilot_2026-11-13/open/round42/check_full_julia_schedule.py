#!/usr/bin/env python3
"""Numeric 32-column diagnostic of actual sector schedule against B25."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json
import numpy as np
import proper_link_targets as p
import proper_link_native as n
B=p.loc.B
spec=importlib.util.spec_from_file_location('b42_b25_numeric',B/'round25/targets.py');t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
lib=n.library();iv=p.Interval(192);cache={};families={r['family']:r for r in lib['families']};entry={}
for bank,rows in lib['catalogue'].items():
 for row in rows:entry.setdefault(row['family_id'],row)
specs,_=p.catalogue();maximum=0;cases=0
def midpoint(z):return float((z[0]+z[1])/(2*iv.S))
for name,specification in specs.items():
 f=p.factor(iv,specification,cache);family=families[name];l=p.givens(iv,f['L'],specification['type'] in ('identity','ref_rot_plus','ref_rot_minus'));r=p.givens(iv,f['R'],specification['type']=='identity');d=p.diagonal_targets(iv,f);mp={}
 for name0,rs in [('L',l),('R',r)]:
  for src,record in zip(rs,family[name0]):mp[int(record['k'])]=(midpoint(src['cos']),midpoint(src['sin']))
 for key,pattern in [('00',(0,0)),('10',(1,0)),('01',(0,1))]:mp[int(family['diagonal'][key]['k'])]=(midpoint(d[pattern]['cos']),midpoint(d[pattern]['sin']))
 e=entry[name];lay=n.layout(len(e['SAM_pattern']));controls,pat=n.sector_controls(lay,e);external=sum(bit<<wire for wire,bit in zip(controls,pat));modes=lay['modes'];flag=lay['julia_flag'];M=np.eye(32)
 def full(ix):
  out=external|(((ix>>4)&1)<<flag)
  for bit,q in enumerate(modes):out|=((ix>>bit)&1)<<q
  return out
 def match(ix,cs,ps):
  z=full(ix);return all(((z>>q)&1)==b for q,b in zip(cs,ps))
 def bitpos(q):return 4 if q==flag else modes.index(q)
 def apply_cx(control,target):
  ci=bitpos(control);ti=bitpos(target);perm=[x^(((x>>ci)&1)<<ti) for x in range(32)];return M[perm,:].copy()
 def apply_rotation(q,c,s,cs,ps):
  pos=bitpos(q);new=M.copy()
  for x in range(32):
   if x>>pos&1 or not match(x,cs,ps):continue
   y=x|(1<<pos);new[x,:]=c*M[x,:]-s*M[y,:];new[y,:]=s*M[x,:]+c*M[y,:]
  return new
 for cmd in n.commands(lay,e,family,lib['controlled_X']):
  if cmd['kind']=='fock':M=apply_cx(cmd['cx_control'],cmd['cx_target'])
  if cmd['kind']=='X':
   pos=bitpos(cmd['target']);perm=[x^(1<<pos) if match(x,cmd['controls'],cmd['pattern']) else x for x in range(32)];M=M[perm,:].copy()
  else:
   c,s=mp[cmd['k']];s=-s if int(cmd.get('inverse_depth',cmd.get('reverse',False)))%2 else s;M=apply_rotation(cmd['target'],c,s,cmd['controls'],cmd['pattern'])
  if cmd['kind']=='fock':M=apply_cx(cmd['cx_control'],cmd['cx_target'])
 U=np.array([[midpoint(v) for v in row] for row in f['source']]);actual=t.link_julia_cached(np.ascontiguousarray(U).tobytes());err=float(np.max(abs(M-actual)));assert err<2e-12,(name,err);maximum=max(maximum,err);cases+=1
out={'status':'PASS_ALL_32_COLUMN_JULIA_SCHEDULE_DIAGNOSTIC','families':cases,'max_float32_matrix_difference':maximum,'angle_library_sha256':sha256((Path(n.__file__).parent/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'native_emitter_sha256':sha256(Path(n.__file__).read_bytes()).hexdigest(),'float_is_not_certificate':True,'actual_huge_native_word_executed':False,'GR_closed':False}
Path(__file__).with_name('FULL_JULIA_SCHEDULE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
