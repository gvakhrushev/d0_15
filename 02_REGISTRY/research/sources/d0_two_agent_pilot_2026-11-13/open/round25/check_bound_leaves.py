#!/usr/bin/env python3
"""Check A11 full source-leaf address map against actual B25 targets.
Floating diagnostics on center + genuine one-hot SAM vertex; not factory gates.
"""
from pathlib import Path
import json,numpy as np
import targets as t
P=Path(__file__).resolve().parent;data=json.loads((P/'SOURCE_LEAF_BINDING.json').read_text());refs=data['leaf_templates'];rows=data['site_bindings']
labels={'Y0':None,'b_one_hot':np.eye(1,2688,0,dtype=np.int8)[0]};maxerr=0.;N=0
for label,bits in labels.items():
 for bank in t.BANKS:
  f=t.fields(bank,bits);u,links,psi=f
  # Material target state's explicit fresh-RIGHT norm, using all 128 Fourier coordinates.
  rightmass=[sum(t.chi_ref(x,r)**2 for r in range(128)) for x in t.SITES]
  for row in rows:
   for leaf,address in zip(refs,row['leaf_addresses_in_template_order']):
    name=leaf['name'].split('/')
    if leaf['kind']=='Choi':
     addr=t.ADDR[address];si=t.INDEX[tuple(addr['site'])];direction=addr['direction'];J=t.bank_julia(f,address)
     val=J[leaf['output'],leaf['input']]*leaf['anchor_moment_multiplier']
     want=u[si,int(name[2]),int(name[1])] if name[0]=='u' else links[si,direction,int(name[3]),int(name[4])]
    else:
     si=int(address);grade=int(name[2]);m=t.local_m(psi[si]);val=2*m[1]*m[grade]*rightmass[si]
     want=2*t.ROOTP*psi[si,0 if grade==0 else 1]/256
    maxerr=max(maxerr,abs(float(val-want)));N+=1
assert N==2*7*256*282 and maxerr<1e-12,(N,maxerr)
res={'status':'PASS_BOUND_SOURCE_LEAVES_ON_ACTUAL_TARGETS','labels':list(labels),'banks':7,'sites':256,'source_leaves_per_site':282,'entries_checked':N,'max_absolute_error':maxerr,'scale':'physical source moments before A11 inverse PF','finite_native_processor_executed':False,'GR_closed':False}
(P/'BOUND_LEAF_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
