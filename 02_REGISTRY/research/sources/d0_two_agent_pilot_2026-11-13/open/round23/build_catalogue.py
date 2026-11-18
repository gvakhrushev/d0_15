#!/usr/bin/env python3
"""L4 candidate full geometric-address contract + exact carrier tests.
Outputs structural targets and boundary debt; no native synthesis or physical closure.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
from collections import Counter
import json, hashlib
import numpy as np
P=Path(__file__).resolve().parent; B=P.parent/'round21'
rows=[json.loads(s) for s in (B/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
ks=json.loads((B/'ORIGINAL_FOURIER128_L4.json').read_text())['kappa']
sites=[tuple(r['site']) for r in rows]; assert len(set(sites))==256
weights=[Fraction(r['N'],10946) for r in rows]; assert sum(weights)==1
add=lambda x,r:tuple((v+1)%4 if i==r and r<2 else v+1 if i==r else v for i,v in enumerate(x))
base={(x,d) for x in sites for d in range(4)}
shift={(add(x,r),d) for x in sites for r in range(4) for d in range(4) if r!=d}
links=sorted(base|shift); halo=sorted(set(links)-base)
assert len(base)==1024 and len(links)==1408 and len(halo)==384
assert all((x[2]==4 and d!=2) or (x[3]==4 and d!=3) for x,d in halo)
addresses=[{'a':0,'kind':'identity_anchor','matrix':'I32'}]
for x in sorted(sites):
 for d in range(4):addresses.append({'a':len(addresses),'kind':'inverse_coframe_column','site':x,'direction':d,'matrix':'Julia32(C(u[x,d]))'})
for x,d in links:addresses.append({'a':len(addresses),'kind':'proper_link','site':x,'direction':d,'exterior_halo':x not in set(sites),'matrix':'Julia32(exterior(U[x,d])/2)'})
assert len(addresses)==2433
lookup={(a['kind'],tuple(a['site']),a['direction']):a['a'] for a in addresses if 'site' in a}
(P/'CHOI_ADDRESSES.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in addresses))
stencils=[]
for row in rows:
 x=tuple(row['site']); missing=[r for r in (2,3) if x[r]==3]
 face=[{'r':r,'s':s,'addresses':[lookup[('proper_link',x,r)],lookup[('proper_link',add(x,r),s)],lookup[('proper_link',add(x,s),r)],lookup[('proper_link',x,s)]]} for r in range(4) for s in range(r+1,4)]
 material=[{'r':r,'target':add(x,r),'in_original_material_256':add(x,r) in set(sites)} for r in range(4)]
 stencils.append({'site':x,'pf_count':row['N'],'is_64_free_interior':x[2] in (1,2) and x[3] in (1,2),'coframe_addresses':[lookup[('inverse_coframe_column',x,r)] for r in range(4)],'face_factors':face,'matter_forward':material,'matter_halo_directions':missing})
(P/'SITE_STENCILS.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in stencils))
assert sum(bool(t['matter_halo_directions']) for t in stencils)==112
assert sum(t['is_64_free_interior'] for t in stencils)==64
# Original Fourier matrix: exact signed integers, never mixed with external PF SITE.
c=(1,0,-1,0);s=(0,1,0,-1);F=np.zeros((256,128),dtype=np.int64)
for i,x in enumerate(sites):
 for j,k in enumerate(ks):
  z=sum(a*b for a,b in zip(k,x))%4;F[i,2*j]=c[z];F[i,2*j+1]=s[z]
assert np.array_equal(F.T@F,128*np.eye(128,dtype=np.int64))
counts=np.array([r['N'] for r in rows],dtype=np.int64)
wrong=2*(F.T@(counts[:,None]*F))-10946*np.eye(128,dtype=np.int64)
i,j=np.unravel_index(np.argmax(np.abs(wrong)),wrong.shape)
witness=Fraction(int(wrong[i,j]),128*10946)
assert (i,j)==(19,37) and witness==Fraction(-477,700544)
# Gram invariance is structural: site-orthogonality kills x != y;
# local normalized m_x does not alter sum_x chi_x chi_x^T. External SITE is separate.
# Adversarial replacement of shared SITE by independent site copies changes products.
mu=sum(w*Fraction(r['N'],128) for w,r in zip(weights,rows))
second=sum(w*Fraction(r['N'],128)**2 for w,r in zip(weights,rows));cov=second-mu*mu
assert cov>0
A=len(addresses); d=32; D=2**22
# Exact normalization and full-column SO certificate with non-sparse b:
# ||Omega||²= A*d/(A*d)=1 because each J_a has ||J_a||_F²=d.
# b_e0²=1/(A*d), and all zero padding rows are invariant by K and O.
assert A*d*d<=D and A*d*d> D//2
slots=[]
for bank in ('y+','y-','f','0','x+','x-','q'):
 for sign in ('S1','S2'):
  for k in range(82):slots.append({'bank':bank,'sign':sign,'type':'Choi','copy':k})
 for sign in ('T1','T2','T3','T4','T5','T6','T7','T8'):
  for kind in ('Choi','material'):
   for k in range(2):slots.append({'bank':bank,'sign':sign,'type':kind,'copy':k})
assert len(slots)==1372
(P/'COPY_SLOTS.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in slots))
res={'status':'EXACT_STRUCTURAL_CERTIFICATE_CONDITIONAL_GEOMETRIC_HALO_NOT_NATIVE_WORD',
 'source_site_count':256,'interior_field_rows':64,'non_interior_rows':192,'transverse_forward_halo_source_rows':112,
 'geometric_address_counts':{'identity':1,'coframe':1024,'links_on_base':1024,'links_on_halo':384,'A':A},
 'choi':{'local_dimension':32,'active_vector_coordinates':A*d*d,'padded_coordinates':D,'qubits':22,'anchor_square':str(Fraction(1,A*d)),
         'identity_block':'J_a0=I_32','input':'r=|a0=0,i0=0,j0=0>','output':'sum_{a,i,j} J_a[j,i]|a,i,j>/sqrt(32A)',
         'completion':'K=|b><r|-|r><b|; O=I+K+K²/(1+<r,b>), direct sum I on padding',
         'proof':'Each J_a orthogonal => ||b||²=1; <r,b>=1/sqrt(32A)>0; O is a rotation on span(r,b), identity on its orthogonal complement; all padded coordinates are untouched.'},
 'copy_slots':{'per_report_max_choi':180,'per_report_max_material':16,'seven_reports_max_choi':1260,'seven_reports_max_material':112,'status':'bounded template; unused identity operands retained, not a compiled factory'},
 'fourier_gram':'integer F.T F=128 I exactly; chi=F/128 => Gram I/128',
 'pf_naive_hostile':{'indices':[int(i),int(j)],'difference':str(witness),'nonzero_entries':int(np.count_nonzero(wrong))},
 'shared_site_hostile':{'test':'f_x=q_x=N_x/128, weights N_x/10946','E_fq_minus_E_f_E_q':str(cov),'strictly_positive':True},
 'required_unsettled':'the 112 CAR forward-edge rows require an explicitly owned boundary/halo binding; geometry halo alone does not provide material labels',
 'sampled_vertices_evaluated':False,'material_halo_created':False,'compiled_native_word':False,'GR_closed':False}
(P/'CERTIFICATE.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(res,ensure_ascii=False,indent=2))
