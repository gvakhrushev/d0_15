#!/usr/bin/env python3
"""Numerical diagnostics of B35 identities on all seven materialized centres."""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys,math
import numpy as np
P=Path(__file__).resolve().parent; B=P.parent/'round25';data=B/'CENTRE_JULIA32_TARGETS.npz';fields=B/'CENTRE_FIELDS.npz'
spec=importlib.util.spec_from_file_location('b35_targets',B/'targets.py');t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
npz=np.load(data);julia=npz['julia'];names=list(npz['bank_names']);fld=np.load(fields);p=t.PVAL;rootp=math.sqrt(p);A=2049;active=32*A*32;D=2**22;c=1/math.sqrt(32*A)
assert list(names[:7])==list(t.BANKS) and julia.shape==(8,2049,32,32)
rng=np.random.default_rng(3500);probe=rng.standard_normal(D);probe/=np.linalg.norm(probe)
maxerr=0;maxnorm=0;anchors=[]
for z,name in enumerate(names[:7]):
 # flattened label is (address,input,output), J[output,input].
 b=np.zeros(D);b[:active]=julia[z].transpose(0,2,1).reshape(-1)/math.sqrt(32*A)
 assert np.array_equal(julia[z,0],np.eye(32))
 anchors.append(float(b[0]));maxnorm=max(maxnorm,abs(np.dot(b,b)-1));assert abs(b[0]-c)<1e-15 and not np.any(b[active:])
 u=b.copy();u[0]+=1;u/=math.sqrt(2*(1+c));assert abs(np.dot(u,u)-1)<1e-12
 # O=I+K+K²/(1+c), acting on a full 2^22 random column.
 bx=float(np.dot(b,probe));x0=probe[0];y=probe+b*x0;y[0]-=bx;y+=(b*(c*x0-bx));y[0]-=(x0-c*bx);y-=(b*(c*x0-bx))*(c/(1+c));y[0]+=(x0-c*bx)*(c/(1+c))
 # Equivalent clean expression for K² division above, checked separately.
 y2=probe+b*x0;y2[0]-=bx;k2=b*(c*x0-bx);k2[0]-=(x0-c*bx);y2+=k2/(1+c);assert np.max(np.abs(y-y2))<1e-15
 reflected=probe.copy();reflected[0]*=-1;reflected-=2*u*np.dot(u,reflected)
 err=float(np.linalg.norm(reflected-y2));maxerr=max(maxerr,err);assert err<1e-11
 # All padded basis vectors are fixed by O itself; raw G† layer is distinct.
 assert np.count_nonzero(u[active:])==0
 del b,u,y,y2,k2,reflected
# CAR M=R_um R_u*, all seven centre banks and all 256 sites.
r=np.eye(16)[:,1];star=np.zeros(16);star[1]=rootp;star[14]=p;ustar=(r+star)/math.sqrt(2*(1+rootp));Hstar=np.eye(16)-2*np.outer(ustar,ustar);carerr=0;carcases=0
for bank in t.BANKS:
 for psi in fld[bank+'_psi']:
  m=t.local_m(psi);assert abs(np.dot(m,m)-1)<1e-14 and abs(m[1]-rootp)<1e-15
  um=(r+m)/math.sqrt(2*(1+rootp));got=t.mm(np.eye(16)-2*np.outer(um,um),Hstar)
  err=float(np.max(np.abs(got-t.car_map(psi))));carerr=max(carerr,err);assert err<2e-14;carcases+=1
# Distinguish the reference centre from genuine SAM vertices; verify q CAR
# at all internal sites for four actual b labels. These are diagnostics,
# not exhaustive SAM testing or a physical controlled preparation.
vertex_cases=0;vertex_difference=0.;centre_psi=fld['q_psi']
labels=[np.zeros(2688,dtype=np.int8),np.ones(2688,dtype=np.int8),np.arange(2688,dtype=np.int8)%2,np.eye(1,2688,0,dtype=np.int8).reshape(-1)]
for label in labels:
 psi_table=t.fields('q',label)[2];vertex_difference=max(vertex_difference,float(np.max(np.abs(psi_table-centre_psi))))
 for psi in psi_table:
  m=t.local_m(psi);um=(r+m)/math.sqrt(2*(1+rootp));got=t.mm(np.eye(16)-2*np.outer(um,um),Hstar)
  assert np.max(np.abs(got-t.car_map(psi)))<2e-14;vertex_cases+=1
assert vertex_difference>0
# True born v is not |0>; G^T maps each RAW wire to |0>.
v=np.array([rootp,p]);G=np.array([[rootp,-p],[p,rootp]]);assert np.linalg.norm(t.mm(G.T,v.reshape(2,1)).ravel()-np.array([1,0]))<1e-15 and abs(p)>0
out={'status':'PASS_B25_CENTRE_REFLECTION_DIAGNOSTICS','centre_banks':list(t.BANKS),'choi_full_dimension':D,'active_choi_amplitudes':active,'A_active':A,'anchor_c':'1/sqrt(32*2049)','centre_choi_full_random_columns':7,'max_centre_choi_reflection_error_l2':maxerr,'max_centre_choi_norm_error':maxnorm,'CAR_centre_bank_site_maps':carcases,'max_CAR_reflection_error':carerr,'four_SAM_vertex_q_CAR_site_maps':vertex_cases,'centre_distinct_from_SAM_vertex':vertex_difference>0,'raw_v_mapped_to_zero_by_actual_G_transpose':True,'exactness_note':'floating point diagnostics only; full all-column and all SAM conclusions follow from algebra, not this sample','input_sha256':{'CENTRE_JULIA32_TARGETS.npz':sha256(data.read_bytes()).hexdigest(),'CENTRE_FIELDS.npz':sha256(fields.read_bytes()).hexdigest(),'targets.py':sha256((B/'targets.py').read_bytes()).hexdigest()},'GR_closed':False}
(P/'B25_REFLECTION_TARGETS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
