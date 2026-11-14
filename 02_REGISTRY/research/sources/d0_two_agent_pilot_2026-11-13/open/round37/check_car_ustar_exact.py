#!/usr/bin/env python3
"""All-column exact native verification and literal inverse for small k."""
from pathlib import Path
from hashlib import sha256
import json
import build_car_ustar as b
# Canonical integer ring: a=sqrt(p), a^4=1-a²; p=a².
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(i+j for i,j in zip(x,y))
def neg(x):return tuple(-z for z in x)
def ma(x):return (x[3],x[0],x[1]-x[3],x[2])
def mp(x):return (x[2],x[3],x[0]-x[2],x[1]-x[3])
def cs(n):
 c,s=one,zero
 for _ in range(n):c,s=add(ma(c),neg(mp(s))),add(mp(c),ma(s))
 return c,s

def run(word,state):
 for op,*w in word:
  out={}
  if op=='G':
   mask=1<<w[0]
   for x,z in state.items():
    bit=bool(x&mask);base=x&~mask;c0=neg(mp(z)) if bit else ma(z);c1=ma(z) if bit else mp(z)
    out[base]=add(out.get(base,zero),c0);y=base|mask;out[y]=add(out.get(y,zero),c1)
  elif op=='CX':
   for x,z in state.items():y=x^(((x>>w[0])&1)<<w[1]);out[y]=add(out.get(y,zero),z)
  else:
   assert op=='SourceI' and w==[4,5,6]
   for x,z in state.items():
    control=(x>>4)&1;parity=((x>>5)^(x>>6))&1;y=x^(control<<6);c=neg(z) if control and parity else z;out[y]=add(out.get(y,zero),c)
  state={x:z for x,z in out.items() if z!=zero}
 return state

def flatten(tree):return [(g['op'],*g['wires']) for g in b.nb.expand(tree,10000)]
reports=[]
for k in (1,2):
 tree=b.word(k);inverse=b.nb.inverse_literal(tree,4,(5,6));b.nb.validate_schema(tree,8,4,(5,6),(7,));b.nb.validate_schema(inverse,8,4,(5,6),(7,))
 forward=flatten(tree);back=flatten(inverse);c,s=cs(8*k)
 assert len(forward)==8*k+70 and len(back)==64*k+102
 for column in range(256):
  grade=column&15
  if grade==1:want={column:c,column^15:neg(s)}
  elif grade==14:want={column:c,column^15:s}
  else:want={column:one}
  assert run(forward,{column:one})==want,(k,column)
  assert run(back,run(forward,{column:one}))=={column:one},(k,column,'inverse')
 reports.append({'k':k,'forward_calls':len(forward),'literal_reverse_calls':len(back),'all_columns':256,'inverse_cases':256})
# The actual 4142-bit k is not expanded: validate every syntactic leaf and
# verify the exact literal reverse tree, counts and declared protected wires.
p=Path(__file__).with_name('CAR_USTAR_NATIVE.json');j=json.loads(p.read_text());k=int(j['k']);tree=j['forward_DAG'];inverse=j['literal_raw_inverse_DAG'];assert tree==b.word(k) and inverse==b.nb.inverse_literal(tree,4,(5,6))
for leaf in b.nb.leaves(tree):
 assert 7 not in leaf['wires']
 if leaf['op']=='SourceI':assert leaf['wires']==[4,5,6]
# C maps grade 1 to15 and grade14 to14, independent of other registers.
def C(x):
 for i in (1,2,3):x^=((x&1)<<i)
 return x
assert C(1)==15 and C(14)==14 and all(C(C(x))==x for x in range(16))
out={'status':'PASS_EXACT_NATIVE_ALL_SMALL_COLUMNS_AND_ACTUAL_DAG','input_sha256':sha256(p.read_bytes()).hexdigest(),'exact_field':'Z[a], a=sqrt(p), a^4+a²−1=0','literal_Spin':'diag(J,-J), both spin bits','reports':reports,'all_exact_small_k_columns':512,'all_exact_small_k_forward_then_literal_inverse':512,'actual_giant_DAG_structurally_verified':True,'actual_giant_word_expanded_or_executed':False,'identity_on_SAM_SITE_RIGHT_and_other_spectators':True,'oldRIGHT_untouched_every_primitive':True,'GR_closed':False}
Path(__file__).with_name('CAR_USTAR_EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
