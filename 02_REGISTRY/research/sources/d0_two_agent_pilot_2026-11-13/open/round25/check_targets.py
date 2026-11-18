#!/usr/bin/env python3
"""Exercise complete seven-bank targets and genuine noncentral SAM vertices."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import mpmath as mp
import targets as t
import precision_name as hp
P=Path(__file__).resolve().parent;mm=t.mm
labels={'Y0':None,'b_all_zero':np.zeros(2688,dtype=np.int8),'b_all_one':np.ones(2688,dtype=np.int8),'b_alternating':np.arange(2688,dtype=np.int8)%2,'b_one_hot':np.eye(1,2688,0,dtype=np.int8)[0]}
# Verify central reconstruction against the actual 256 B21 data.
rows=[json.loads(x) for x in (t.B/'BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines()];cu,cl,cm=t.current();erru=errl=errm=0.
for row in rows:
 i=t.INDEX[tuple(row['site'])]
 erru=max(erru,float(np.max(np.abs(cu[i]-np.array(row['native_coframe_columns_approx'])))))
 errl=max(errl,float(np.max(np.abs(cl[i,0]-np.array(row['U_u_approx'])))))
 errm=max(errm,abs(cm[i,0]-float(row['psi0'])),abs(cm[i,1]-float(row['psi15'])))
assert max(erru,errl,errm)<1e-14
# Explicit warning against confusing central Y0 and the all-zero SAM label.
b0=t.current(labels['b_all_zero']);b1=t.current(labels['b_all_one']);i=t.INDEX[(0,0,1,1)]
assert abs((b0[0][i,0,0]-cu[i,0,0])-(-t.SAMP*t.PVAL**2))<1e-18
assert abs((b1[0][i,0,0]-cu[i,0,0])-t.SAMP*(1-t.PVAL**2))<1e-18
seen={};stats={};centre_fields={};all_julia=[]
for label,bits in labels.items():
 mins={'coframe_defect':1.,'link_defect':1.,'material_slack':1.,'coframe_min_singular':100.};maxlor=maxorth=maxcar=0.;nchecked=0
 for bank in t.BANKS+('current_mark',):
  fields=t.fields(bank,bits);u,links,psi=fields
  if label=='Y0':centre_fields[bank]={'u':u,'links':links,'psi':psi}
  for n in range(256):
   mins['material_slack']=min(mins['material_slack'],1-t.PVAL-float(np.dot(psi[n],psi[n])))
   mins['coframe_min_singular']=min(mins['coframe_min_singular'],float(np.linalg.svd(u[n],compute_uv=False)[-1]))
   m=t.local_m(psi[n]);M=t.car_map(psi[n]);maxcar=max(maxcar,float(np.max(np.abs(mm(M.T,M)-t.I16))),float(np.max(np.abs(M@t.MSTAR-m))))
   for r in range(4):
    mins['coframe_defect']=min(mins['coframe_defect'],1-float(np.dot(u[n,:,r],u[n,:,r])))
    L=links[n,r];maxlor=max(maxlor,float(np.max(np.abs(mm(mm(L.T,t.ETA),L)-t.ETA))))
    ext=t.exterior(L)/2;mins['link_defect']=min(mins['link_defect'],1-float(np.linalg.svd(ext,compute_uv=False)[0])**2)
  block=np.empty((2049,32,32)) if label=='Y0' else None
  for a in range(2049):
   J=t.bank_julia(fields,a);nchecked+=1
   if block is not None:block[a]=J
   k=hashlib.sha256(J.tobytes()).digest()
   if k not in seen:
    error=float(np.max(np.abs(mm(J.T,J)-t.I32)));seen[k]=error
   maxorth=max(maxorth,seen[k])
  if block is not None:all_julia.append(block)
  # all-column finite CAR local matrices at 256 internal site addresses, plus protected RIGHT identity
 assert min(mins.values())>0 and max(maxlor,maxorth,maxcar)<2e-12,(label,mins,maxlor,maxorth,maxcar)
 stats[label]={'per_bank_sites':256,'banks_including_optional_mark':8,'J32_blocks_checked':nchecked,'minima':mins,'max_lorentz_error':maxlor,'max_julia_orth_error':maxorth,'max_full_CAR_map_error':maxcar}
# Store full 32x32 target blocks of all 7 plus optional unsplit current mark bank.
archive=P/'CENTRE_JULIA32_TARGETS.npz';np.savez_compressed(archive,bank_names=np.array(t.BANKS+('current_mark',)),julia=np.array(all_julia),sites=np.array(t.SITES))
flat={}
for bank,data in centre_fields.items():
 for key,val in data.items():flat[bank+'_'+key]=val
np.savez_compressed(P/'CENTRE_FIELDS.npz',**flat)
# Full external SITE target maps the true born v^8, preserves all columns.
G=np.array([[t.ROOTP,-t.PVAL],[t.PVAL,t.ROOTP]]);born=np.array([t.ROOTP,t.PVAL])
for _ in range(7):born=np.kron(born,[t.ROOTP,t.PVAL])
site=t.site_matrix();siteorth=float(np.max(np.abs(mm(site.T,site)-np.eye(256))));siteerr=float(np.max(np.abs(np.einsum('ij,j->i',site,born)-t.CHI)))
assert max(siteorth,siteerr)<1e-12
# Exactly original Fourier Gram, completely independent of PF SITE.
F=np.array([[int(round(t.chi_ref(x,r)*128)) for r in range(128)] for x in t.SITES],dtype=np.int64)
assert np.array_equal(F.T@F,128*np.eye(128,dtype=np.int64))
# Hostile test incorrect PF multiplication disturbs the original RIGHT Gram.
wrong=2*(F.T@(t.COUNT[:,None]*F))-10946*np.eye(128,dtype=np.int64);assert wrong[19,37]!=0
# Selected precise names on all banks at center and a genuine SAM branch.
# Matrix entries at 40 dps are checked against independently evaluated double targets.
precision_checks=[]
with mp.workdps(40):
 for name,bits in [('Y0',None),('b_one_hot',labels['b_one_hot'])]:
  for bank in t.BANKS:
   data=t.fields(bank,bits);x=(0,0,1,1);n=t.INDEX[x]
   um,lm,pm=hp.at_site(bank,x,bits)
   ue=max(abs(float(um[i,j])-data[0][n,i,j]) for i in range(4) for j in range(4))
   le=max(abs(float(lm[r][i,j])-data[1][n,r,i,j]) for r in range(4) for i in range(4) for j in range(4))
   pe=max(abs(float(pm[i])-data[2][n,i]) for i in range(2))
   aa=t.ADDR_LOOKUP[('inverse_coframe_column',x,1)];a=(aa,0,1)
   oe=abs(float(hp.omega(bank,*a,bits))-t.omega_entry(data,*a))
   ce=abs(float(hp.car_entry(bank,x,0,1,bits))-t.car_map(data[2][n])[0,1])
   assert max(ue,le,pe,oe,ce)<1e-13
   precision_checks.append({'label':name,'bank':bank,'max_float_vs_40dps_error':max(ue,le,pe,oe,ce)})
 # A true sampled nontrivial proper-link Julia full entry using arbitrary-precision sqrtm.
 x=(0,0,1,1); a=t.ADDR_LOOKUP[('proper_link',x,0)];bits=labels['b_all_one'];data=t.fields('f',bits)
 z=hp.omega('f',a,16,0,bits);assert abs(float(z)-t.omega_entry(data,a,16,0))<1e-13
 # 879 O entry including active and padded states and a CAR/RIGHT fixed column.
 inp=(0,0,0);out=(a,16,0);assert abs(float(hp.O_entry('f',out,inp,bits))-t.o_entry(data,out,inp))<1e-13
 pad=(4095,31,31);assert t.o_entry(data,pad,pad)==1 and t.o_entry(data,pad,inp)==0
 cc=t.car_column(data,x,1,37);assert all(row[2]==37 for row in cc)
res={'status':'PASS_SEVEN_FULL_TARGETS_AND_REAL_SAM_FLOAT_DIAGNOSTIC','chart':'additive raw inverse-coframe; exponential proper links; material 2 grades; fixed PF','S':256,'active_A':2049,'SAM_bits':2688,
 'sample_labels':list(labels),'central_not_equal_all_zero_label':True,'centre_B21_max_errors':{'u':erru,'links':errl,'matter':errm},'sample_stats':stats,
 'complete_centred_J32_blocks':8*2049,'centre_archive_bytes':archive.stat().st_size,'centre_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
 'SITE_all_column_orth_error':siteorth,'SITE_born_mapping_error':siteerr,'Fourier_RIGHT_Gram_exact':'I_128/128','naive_PF_Right_Gram_hostile_detected':True,
 'precision_comparisons':precision_checks,'sampled_nontrivial_link_mp_sqrtm_passed':True,'all_column_O_formula_and_padding_checked':True,'CAR_RIGHT_column37_preserved':True,
 'precision_scope':'40dps diagnostic; recipe is computable, not certified native/C1 compiler','native_word':False,'GR_closed':False}
(P/'TARGET_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','sample_labels','complete_centred_J32_blocks','centre_archive_bytes','SITE_born_mapping_error']}))
