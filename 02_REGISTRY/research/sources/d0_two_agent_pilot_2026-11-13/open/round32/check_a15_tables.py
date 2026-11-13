#!/usr/bin/env python3
"""Independently reconstruct A15 roots, transition tables and leaf bindings."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,deque
import hashlib,json
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
load=lambda p:json.loads(p.read_text());dag=load(D/'round11/SOURCE_TENSOR_DAG.json');binding=load(D/'round11/PERIODIC_SOURCE_BINDING.json');palette=load(D/'round12/INTERNAL_SELECTOR_PALETTE.json');tables=load(D/'round15/SOURCE_DISPATCH_TABLES.json');comp=load(D/'round15/SOURCE_DISPATCH_COMPILATION.json');nodes=dag['nodes']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,digest in tables['inputs'].items():assert sha(D/rel)==digest
assert sha(D/'round15/SOURCE_DISPATCH_TABLES.json')==comp['table_sha256']
# Independent exact Q(p) signs, no import of A12 or dispatcher classes.
def qsign(a,b):
 a,b=F(a),F(b);u=2*a-b;v=b
 if not v:return (u>0)-(u<0)
 if not u:return (v>0)-(v<0)
 if (u>0)==(v>0):return 1 if u>0 else -1
 return (1 if u>0 else -1) if u*u>5*v*v else (1 if v>0 else -1)
def pack(v,w):
 shift=0;out=0
 for value,width in zip(v,w):assert 0<=value<2**width;out|=value<<shift;shift+=width
 assert len(v)==len(w);return out
TW=[5,1,9]+[15,7,2]*4;AW=[2,22,22]
assert tables['transition_widths']==TW and tables['address_widths']==AW
# Index all rows and prove unique keys, including zero-valued transitions.
def index(rows):
 m={}
 for width,key,value in rows:assert 0<=key<2**width and (width,key) not in m;m[width,key]=value
 return m
T=index(tables['transition_rows']);A=index(tables['address_rows']);R=index(tables['palette_rows'])
# Reachable DAG and independent stack/visit/copy-degree dynamic program.
reach=set();todo=list(dag['roots'].values())
while todo:
 i=todo.pop()
 if i in reach:continue
 reach.add(i);todo.extend(nodes[i].get('args',[]))
assert 0 not in reach
visits=[];depths=[];node_degree=[]
for i,n in enumerate(nodes):
 args=n.get('args',[]);assert all(x<i for x in args)
 if n['op'] in ('const','var'):
  v=1;depth=1;deg=(0,0) if n['op']=='const' else ((0,1) if n['kind']=='matter_X' else (1,0))
 elif n['op']=='add':
  v=1+max(visits[j] for j in args);depth=max(depths[j] for j in args);deg=tuple(max(node_degree[j][k] for j in args) for k in (0,1))
 else:
  assert n['op']=='mul';v=1+sum(visits[j] for j in args);depth=max(depths[j]+len(args)-i2-1 for i2,j in enumerate(args));deg=tuple(sum(node_degree[j][k] for j in args) for k in (0,1))
 assert list(deg)==n['degree'];visits.append(v);depths.append(depth);node_degree.append(deg)
expected_roots={name:{'node':i+1,'slots':visits[i],'stack_depth':depths[i],'degree':nodes[i]['degree']} for name,i in dag['roots'].items()}
assert expected_roots==tables['roots'];assert sorted((x['slots'],x['stack_depth']) for x in expected_roots.values())==[(18,4),(455,11)]
leaf={x['node']:i+1 for i,x in enumerate(binding['leaf_templates'])};assert len(leaf)==282
expectedT={};constants=[];add_rows=0;max_children=0
for i in reach:
 n=nodes[i];args=n.get('args',[]);op=n['op'];choices=enumerate(args) if op=='add' else [(None,None)]
 if op=='const':
  sg=qsign(n['a'],n['b']);assert sg;constants.append((n['a'],n['b'],sg))
 for pick,chosen in choices:
  kids=[chosen] if op=='add' else args;num=len(kids);max_children=max(max_children,num);assert num<=4
  negative=int(op=='const' and qsign(n['a'],n['b'])<0);fields=[(1^(1<<num)) if num else 0,negative,leaf.get(i,0)];c=q=0
  for j in kids:
   fields.extend([j+1,c,q])
   if op=='mul':c+=nodes[j]['degree'][0];q+=nodes[j]['degree'][1]
  fields.extend([0,0,0]*(4-num));width=22 if op=='add' else 15;key=(i+1)|(pick<<15)|(1<<21) if op=='add' else i+1
  assert (width,key) not in expectedT;expectedT[width,key]=pack(fields,TW)
  if op=='add':add_rows+=1
assert expectedT==T
assert len(constants)==7 and max_children==4
assert R=={(15,int(node)+1):int(val) for node,val in palette['node_to_palette'].items()}
# Every SITE×leaf exact physical address, with a != 0 for CAR.
expectedA={};car_nonzero=0
for site in binding['site_bindings']:
 z=site['SITE_index'];assert 0<=z<256
 for li,(node,addr) in enumerate(zip(binding['leaf_templates'],site['leaf_addresses_in_template_order'])):
  if node['kind']=='Choi':kind,a,b=1,0,(addr<<10)|(node['input']<<5)|node['output']
  else:
   assert node['kind']=='CAR';kind=2;a=(addr<<4)|node['cross_masks'][0];b=(addr<<4)|node['cross_masks'][1];car_nonzero+=int(a!=0)
  assert a!=b and 0<=a<2**22 and 0<=b<2**22
  key=z|((li+1)<<8);assert (17,key) not in expectedA;expectedA[17,key]=pack([kind,a,b],AW)
assert expectedA==A and len(A)==72192 and car_nonzero==2560
# All reachable placements: ensure add alternatives preserve parent offset;
# ordered mul children have disjoint ranges inside root capacity.
placement=0
for name,root in expected_roots.items():
 limit=root['degree'];todo=[(root['node']-1,0,0)];seen=set()
 while todo:
  i,c,q=todo.pop();key=i,c,q
  if key in seen:continue
  seen.add(key);n=nodes[i];assert c+n['degree'][0]<=limit[0] and q+n['degree'][1]<=limit[1] and c<128 and q<4;placement+=1
  args=n.get('args',[])
  if n['op']=='add':todo.extend((j,c,q) for j in args)
  elif n['op']=='mul':
   dc=dq=0
   for j in args:todo.append((j,c+dc,q+dq));dc+=nodes[j]['degree'][0];dq+=nodes[j]['degree'][1]
assert placement==76913
# Independent arithmetic QROM counts based on target-only signed controls.
def pcount(width,key):
 bits=[(key>>i)&1 for i in range(width)]
 if width==0:return Counter({'X':1})
 if width==1:return Counter({'X':1-bits[0],'CX':1})
 if width==2:return Counter({'X':(1-bits[0])*(1-bits[1]),'CX':2-bits[0]-bits[1],'CCX':1})
 return Counter({'X':2*(1-bits[0])*(1-bits[1]),'CX':2*(2-bits[0]-bits[1])+2*sum(1-b for b in bits[2:-1])+(1-bits[-1]),'CCX':2*width-3})
def qcounts(rows):
 C=Counter()
 for width,key,value in rows:
  if value:
   C.update({k:2*v for k,v in pcount(width,key).items()});C['CX']+=bin(value).count('1')
 return Counter({k:v for k,v in C.items() if v})
qc={name:qcounts(tables[name+'_rows']) for name in ('palette','transition','address')}
assert {name:dict(v) for name,v in qc.items()}==comp['lookup_gate_counts']
# Explicit child-copy/add logic: four children, each (15+3*7+3*2) CX
# and 2*(3*(7-1)+3*(2-1)) CCX; forward and inverse are paid.
def counts_step(depth):
 C=qc['palette']+qc['address']+Counter({k:2*v for k,v in qc['transition'].items()})
 C['X']+=2;C['CX']+=2*4*(15+3*7+3*2)+19;C['CCX']+=2*4*2*(3*(7-1)+3*(2-1))
 C['CCX']+=24*sum(1 for i in range(depth) for n in range(5) if i<n or i+1-n<depth)
 return C
report=Counter()
for name,root in expected_roots.items():
 calc=counts_step(root['stack_depth']);assert dict(calc)==comp['walks'][name]['step_counts']
 # Own root initialization count: two three-literal QROM rows.
 init=qcounts([[3,4,root['node']],[3,6,1<<15]])
 if name.startswith('H_q'):init['X']+=1
 assert dict(init)==comp['walks'][name]['root_initialization_counts']
 walk=Counter({op:root['slots']*v for op,v in calc.items()});walk.update(init)
 assert dict(walk)==comp['walks'][name]['one_walk_counts']
 report.update({op:(2 if name.startswith('H_f') else 8)*v for op,v in walk.items()})
assert dict(report)==comp['ten_sign_report_controller_counts']=={'X':144939804,'CX':6911538816,'CCX':9281032152}
assert 7*(report['X']+report['CCX'])<2**36 and comp['seven_report_controller_error_strictly_below']=='2^-4060'
res={'status':'PASS_INDEPENDENT_A15_TABLES_COPY_OFFSETS_AND_COUNTS','inputs':{str(f):sha(f) for f in [D/'round11/SOURCE_TENSOR_DAG.json',D/'round11/PERIODIC_SOURCE_BINDING.json',D/'round12/INTERNAL_SELECTOR_PALETTE.json',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json']},
 'DAG_nodes':len(nodes),'reachable_nodes':len(reach),'transition_rows':len(T),'add_choice_rows':add_rows,'max_children':max_children,
 'all_roots':expected_roots,'reachable_constants_checked':len(constants),'site_leaf_addresses':len(A),'CAR_with_nonzero_a':car_nonzero,
 'all_reachable_node_copy_placements':placement,'QROM_inventory_independently_recomputed':True,'report_controller_logical_counts':dict(report),
 'seven_report_error_if_A14_applies':'<2^-4060','logical_tables_are_not_quantum_SELECT':True,'full_READY_or_physical_C_proved':False,'GR_closed':False}
(P/'TABLES_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','reachable_nodes','transition_rows','site_leaf_addresses','CAR_with_nonzero_a','all_reachable_node_copy_placements']}))
