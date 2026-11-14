#!/usr/bin/env python3
"""Independent source coverage, namespaces, bounds and native cost audit."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util,sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21');B=P.parent;sys.path.insert(0,str(D))
import choi_loader as c
files=[D/'choi_loader.py',D/'CHOI_LOADER_PLAN.json',D/'check_choi_loader.py'];hashes={str(p):sha256(p.read_bytes()).hexdigest() for p in files};plan=json.loads(files[1].read_bytes());lib=c.inputs();lay=c.layout();al=c.adapter_layout(lay)
for p,h in plan['source_and_library_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h
assert plan['layout']==lay and plan['B39_adapter_layout']==al
# Reconstruct sectors from the original JSONL addresses and 2688 coordinates,
# independent of A19/A20/B42 catalogues or A21's own coverage checker.
addr=[json.loads(x) for x in (B/'round24/TORUS_CHOI_ADDRESSES.jsonl').read_text().splitlines()];coords=[json.loads(x) for x in (B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()];assert len(addr)==2049 and len(coords)==2688
groups={}
for i,q in enumerate(coords):
 if q['kind'] in ('coframe','proper_link'):groups.setdefault((q['kind'],tuple(q['site']),q['role']),[]).append(i)
banks=('y+','y-','f','0','x+','x-','q');coverage={}
for bank in banks:
 wanted={'coframe':set(),'link':set()}
 for row in addr:
  if row['kind']=='identity_anchor':assert row['a']==0;continue
  typ='coframe' if row['kind']=='inverse_coframe_column' else 'link';group='coframe' if typ=='coframe' else 'proper_link';idx=groups.get((group,tuple(row['site']),row['direction']),[]) if bank=='f' or bank=='q' and typ=='coframe' else []
  assert len(idx) in (0,4 if typ=='coframe' else 6)
  for pat in product((0,1),repeat=len(idx)):wanted[typ].add((row['a'],tuple(idx),pat))
 for key in ('coframe','link'):
  rows=lib[key]['catalogue'][bank];got={(r['address'],tuple(r['SAM_indices']),tuple(r['SAM_pattern'])) for r in rows};assert got==wanted[key] and len(got)==len(rows)
 assert {x[0] for x in wanted['coframe']}==set(range(1,1025)) and {x[0] for x in wanted['link']}==set(range(1025,2049))
 coverage[bank]={k:len(v) for k,v in wanted.items()}
# Exact A19/B42 little-endian Choi binding: J[j,i], flag is bit4 of j.
assert lay['address']==list(range(2688,2700)) and lay['choi_input']==list(range(2700,2705)) and lay['choi_output']==list(range(2705,2710))
assert lay['modes']==lay['choi_output'][:4] and lay['julia_flag']==lay['choi_output'][4]
for i in range(32):
 for j in range(32):
  word=sum(((i>>k)&1)<<lay['choi_input'][k] for k in range(5))|sum(((j>>k)&1)<<lay['choi_output'][k] for k in range(5))
  assert sum(((word>>lay['choi_input'][k])&1)<<k for k in range(5))==i and sum(((word>>lay['choi_output'][k])&1)<<k for k in range(5))==j
# Verify prefix schedule independently: one 2049-address rotation, 11 H
# conditioned address MSB=0, then five H/CX Bell pairs in little-endian order.
ins=list(c.prefix.instructions(lay,True));expected=[{'op':'address_rotation','controls':[lay['branch']],'pattern':[1],'target':lay['address'][11]}]
for q in lay['address'][:11]:expected.append({'op':'H','controls':[lay['address'][11],lay['branch']],'pattern':[0,1],'target':q})
for i,j in zip(lay['choi_input'],lay['choi_output']):expected.extend([{'op':'H','controls':[lay['branch']],'pattern':[1],'target':i},{'op':'X','controls':[i,lay['branch']],'pattern':[1,1],'target':j}])
assert ins==expected and len(ins)==22
# Exactly disjoint physical registers, including arbitrary aux and future B35 scratch.
private=[lay['branch'],lay['phase_rebit'],*lay['comparator_scratch']];data=lay['address']+lay['choi_input']+lay['choi_output'];anchor=data+private
all_groups=[lay['SAM'],data,private,[lay['port'],*lay['spin'],lay['aux_arbitrary'],lay['oldRIGHT_witness']]];flat=sum(all_groups,[])
assert len(flat)==len(set(flat))==lay['qubits']==2739 and len(data)==22 and len(private)==24 and len(anchor)==46
outerflag=2739;outerwork=list(range(2740,2784));assert len(outerwork)==44 and not set([outerflag,*outerwork])&set(flat)
assert plan['half_vector_private_clean_wires']==private and plan['B35_outer_joint_reflection_anchor_width']==46 and plan['B35_extra_comparator_clean_wires_required']==45
# Original A13 construction actually accepts 46 input controls plus 44 fresh
# workspace and separate flag. This is the cost of this construction, not a
# lower bound on every imaginable comparator.
lg=c.adapter.logic;ops=list(lg.pattern_gate(anchor,0,outerflag,outerwork));assert all(g[-1] not in set(anchor) for g in ops) and any(outerflag in g[1:] for g in ops)
# Count DAG leaves directly, without A21 resource methods.
def actual(t,port):
 op=t['op']
 if op=='seq':
  out=Counter()
  for x in t['children']:out.update(actual(x,port))
  return out
 if op=='repeat':return Counter({k:int(t['count'])*v for k,v in actual(t['child'],port).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def inv(x):return Counter({'G_port':x['G_port']+x['G_other'],'CX':x['CX']+6*x['G_other'],'SourceI':3*x['SourceI']+4*(x['G_port']+x['G_other'])})
def update(x,n):return Counter({k:v*n for k,v in x.items()})
def selective(controls,pattern,k,kmax=23,depth=0,perm=0):
 K=len(controls);assert K<=kmax and len(pattern)==K;count=1<<K;neg=count//2 if any(pattern) else 0;power=k*(1<<(kmax-K));a=Counter({'G_port':neg*power,'G_other':(count-neg)*power,'CX':K*count+6*neg+2*perm,'SourceI':4*neg})
 for _ in range(depth):a=inv(a)
 return a
# Collect A19 prefix directly, with syntax checks on all of its finite DAGs.
readonly=set(lay['SAM']+[lay['branch']]);protected={lay['phase_rebit'],*lay['comparator_scratch'],lay['oldRIGHT_witness']};port=lay['port'];pre=Counter()
for tree in c.prefix.prefix_blocks(lib['prefix'],lay,True):
 for leaf in c.nb.leaves(tree):
  assert not set(leaf['wires'])&protected
  if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in readonly
 pre.update(actual(tree,port))
# Independent accounting of every source sector, caching only exact equality
# of source family and local control width. All patterns include branch=1.
cf_cache={};ln_cache={};lf={x['family']:x for x in lib['link']['families']};bank_inventories={};cf_units=0;link_units=0
fixed=c.adapter.fixed(al,int(lib['phase']['phase_k']),int(lib['phase']['correction_l']),lib['h_k']);H=actual(fixed['H'],port);G=sum((actual(t,port) for t in fixed['good']),Counter());ST=sum((actual(t,port) for t in fixed['start']),Counter());COR=actual(fixed['correction'],port)
for bank in banks:
 cf=Counter();ln=Counter()
 for row in lib['coframe']['catalogue'][bank]:
  key=(row['family_id'],len(row['SAM_indices']))
  if key not in cf_cache:
   z=Counter()
   for b,d in c.coframe.sector_units(row,lib['coframe'],lay):
    assert lay['branch'] in b['controls'] and b['pattern'][b['controls'].index(lay['branch'])]==1 and b['target'] not in readonly|set(lay['address'])|set(lay['choi_input'])
    assert not set(b['controls']+[b['target']])&protected
    K=b['K'];N=1<<K;neg=N//2 if any(b['pattern']) else 0;k=b['k'];v=Counter({'G_port':neg*k,'G_other':(N-neg)*k,'CX':K*N+6*neg+2*len(b['permutation']),'SourceI':4*neg})
    for _ in range(d):v=inv(v)
    z.update(v)
   cf_cache[key]=z
  cf.update(cf_cache[key]);cf_units+=1
 for row in lib['link']['catalogue'][bank]:
  key=(row['family_id'],len(row['SAM_indices']))
  if key not in ln_cache:
   local=c.link.bind_global(lay,row);z=Counter()
   for cmd in c.link.commands(local,row,lf[row['family_id']],lib['link']['controlled_X']):
    ctr=cmd['controls'];pat=cmd['pattern'];assert lay['branch'] in ctr and pat[ctr.index(lay['branch'])]==1 and cmd['target'] not in readonly|set(lay['address'])|set(lay['choi_input']) and not set(ctr+[cmd['target']])&protected
    if cmd['kind']=='fock':v=selective(ctr,pat,cmd['k'],depth=cmd['inverse_depth'],perm=0);v.update({'CX':2})
    elif cmd['kind']=='rotation':v=selective(ctr,pat,cmd['k'],depth=int(cmd.get('reverse',False)))
    else:
     assert cmd['kind']=='X';v=selective(ctr,pat,cmd['k'])+selective(ctr+[cmd['target']],pat+[1],cmd['phase_k'])
    z.update(v)
   ln_cache[key]=z
  ln.update(ln_cache[key]);link_units+=1
 cv=pre+cf+ln;cv_inv=inv(cv);half=update(H,2)+cv
 for _ in range(8):half=update(half,2)+inv(half)+G+ST
 half.update(COR);half_inv=inv(half)
 for key,value in [('Omega_forward',cv),('Omega_literal_inverse',cv_inv),('half_forward',half),('half_literal_inverse',half_inv)]:
  assert all(int(plan['banks'][bank][key][a])==value[a] for a in ('G_port','G_other','CX','SourceI')),(bank,key)
 bank_inventories[bank]={'coframe_sectors':coverage[bank]['coframe'],'link_sectors':coverage[bank]['link']}
# Actual raw v-to-zero word inventory, kept outside unitary counts.
def zero_inventory(wires):
 out=Counter()
 for q in wires:out.update(actual(c.nb.rotation_power(q,-1,lay['port'],tuple(lay['spin'])),lay['port']))
 return out
for k,wires in [('B39_new24_RAW_zero_inventory_separate',private),('input_DATA22_RAW_inverse_inventory_separate',data)]:
 got=zero_inventory(wires);assert all(got[a]==int(plan[k][a]) for a in ('G_port','G_other','CX','SourceI'))
outer_zero=zero_inventory([outerflag,*outerwork]);assert outer_zero==Counter({'G_port':45,'CX':270,'SourceI':180})
assert plan['RAW_initialization_included_in_unitary_counts'] is False
# Independent all-column max-of-disjoint SELECT error + prefix and B39 bound.
prefixcert=lib['prefix'];prefixerr=Fraction(int(prefixcert['prefix_error_L1_numerator_hex'],16),1<<prefixcert['precision_bits']);delta=Fraction(1,2**3264);selecterr=max(26*delta,101*delta);omega=prefixerr+selecterr;halferr=Fraction(1,2**3280)+6561*omega+(13122+13120*23+1)*Fraction(1,2**4096)
errs=[prefixerr,selecterr,omega,halferr];assert all(int(x,16)==e.numerator for x,e in zip(plan['error_numerators_hex'],errs)) and all(int(x,16)==e.denominator for x,e in zip(plan['error_denominators_hex'],errs));assert omega<Fraction(1,2**3250) and halferr<Fraction(1,2**3230)
for f,h in hashes.items():assert sha256(Path(f).read_bytes()).hexdigest()==h
out={'status':'PASS_INDEPENDENT_A21_COVERAGE_NAMESPACE_COUNTS_AND_ERRORS','input_sha256':hashes,'banks':coverage,'coframe_sectors':cf_units,'link_sectors':link_units,'independent_resource_classes':{'coframe':len(cf_cache),'link':len(ln_cache)},'prefix_block_count':22,'little_endian_input_output_all_1024_pairs_checked':True,'data_wires':22,'private_wires':24,'outer_joint_anchor_wires':46,'standard_outer_comparator_extra_clean_wires':45,'joint_comparator_minimality_not_claimed':True,'raw_zero_22_and_24_costs_separate_verified':True,'if_RAW_outer45_zero_inventory':{'G_port':45,'CX':270,'SourceI':180},'Omega_error_lt':'2^-3250','half_error_lt':'2^-3230','all_banks_forward_and_literal_inverse_inventories_match':True,'full_native_word_executed':False,'GR_closed':False}
(P/'A21_INDEPENDENT_INTEGRATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
