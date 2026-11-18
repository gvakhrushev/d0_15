#!/usr/bin/env python3
"""All 256 B25 columns: numerical matrix diagnostic + exact rotation identity."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json
import numpy as np
import sympy as s
import site_targets as t
import site_native as n
P=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('b45_b25',t.B/'round25/targets.py');b=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b;spec.loader.exec_module(b)
lib=n.library();counts,sp,nodes=t.tree_names();iv=t.Dyadic(192);S=iv.scale;U=np.eye(256)
for node in nodes:
 cc,ss=t.targets(iv,sp[node['angle_id']],counts);co=float((cc[0]+cc[1])/(2*S));si=float((ss[0]+ss[1])/(2*S));q=node['target_bit'];pat=node['pattern'];ctrl=node['control_bits'];new=U.copy()
 for x in range(256):
  if x>>q&1 or any((x>>i)&1!=p for i,p in zip(ctrl,pat)):continue
  y=x|(1<<q);new[x,:]=co*U[x,:]-si*U[y,:];new[y,:]=si*U[x,:]+co*U[y,:]
 U=new
c=(counts[0]/sum(counts))**.5;chi=np.sqrt(np.asarray(counts)/sum(counts));r=np.zeros(256);r[0]=1;u=(r+chi)/np.sqrt(2*(1+c));assert np.max(abs(U[:,0]-u))<2e-15
R0=np.eye(256);R0[0,0]=-1
G=np.array([[b.ROOTP,-b.PVAL],[b.PVAL,b.ROOTP]]);RAW=G.T
for _ in range(7):RAW=np.kron(RAW,G.T)
actual=b.mm(b.mm(b.mm(b.mm(U,R0),U.T),R0),RAW);expected=b.site_matrix();error=float(np.max(abs(actual-expected)));assert error<5e-15
assert np.max(abs(b.mm(actual.T,actual)-np.eye(256)))<5e-15
# Exact two-plane identity, valid on the full orthogonal complement too.
x,y=s.symbols('c s',real=True);r2=s.Matrix([1,0]);chi2=s.Matrix([x,y]);Q=s.eye(2)-(r2+chi2)*(r2+chi2).T/(1+x);R=s.diag(-1,1);expected2=s.Matrix([[x,-y],[y,x]]);z=Q*R-expected2
for q in z:
 num=s.together(q).as_numer_denom()[0];assert s.rem(s.Poly(s.expand(num),y),s.Poly(y*y+x*x-1,y)).as_expr()==0
out={'status':'PASS_SITE_ALL_256_COLUMNS_NUMERIC_AND_EXACT_REFLECTION_IDENTITY','full_256_by_256_entries_checked':65536,'max_float_matrix_difference':error,'exact_householder_pair_identity':True,'PF_count_sum':sum(counts),'PF_anchor_count':counts[0],'library_sha256':sha256((P/'SITE_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'float_is_not_native_angle_certificate':True,'full_native_word_executed':False,'GR_closed':False}
(P/'SITE_MATRIX_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
