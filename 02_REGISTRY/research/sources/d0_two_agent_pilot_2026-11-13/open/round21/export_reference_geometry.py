#!/usr/bin/env python3
"""Export original finite L=4 Brinkmann reference and H.1 reference constants.

Numerical central-field diagnostics only.  This is not compiled H.1 nor a
certification of the full sampled chart, all source operators, or its marks.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,math
import mpmath as mp
import numpy as np

HERE=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (HERE/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
assert len(rows)==256
mp.mp.dps=80;p=(mp.sqrt(5)-1)/2;alpha=mp.sqrt(p);z=mp.mpf(1)/2**20
L0=4*p**3;Q=1-z*L0;R=1-z*L0*(1+p**6)
rx=4*z*Q*p**11;ry=8*z*p**6*(R+Q*p**6);k0=ry/rx
assert abs(k0-2*p**(-5)*(R/Q+p**6))<mp.mpf('1e-70')
lam=-k0;h=mp.mpf(1)/4;sigma=mp.mpf(1)/100;aw=mp.mpf(3)/100;nu=mp.mpf(3)/5
energy=(2*mp.pi)**2*sigma**2;rh=(2*mp.pi*h)/(2*mp.sin(mp.pi*h))
amplitude=sigma*rh
assert p**2-amplitude**2>0
rho_max=max(Fraction(r['rho_numerator'],r['rho_denominator']) for r in rows)
sref=mp.mpf(6);nu_bound=mp.mpf(1)
assert sref>4*nu_bound*mp.sqrt(mp.mpf(rho_max.numerator)/rho_max.denominator)

# H.1 F2-F4, exactly rational Cayley data for h=1/4, chi_h=1.
tf=Fraction(1,8);vf=Fraction(1,80)
ca=(1+tf*tf)/(1-tf*tf);sa=2*tf/(1-tf*tf)
cb=(1-vf*vf)/(1+vf*vf);sb=2*vf/(1+vf*vf)
Fh=sa*sb*(2+(ca-1)*(1-cb))/(2*Fraction(1,4)**2)
Fmp=mp.mpf(Fh.numerator)/Fh.denominator
kappa=mp.sin(512*mp.atan2(p,alpha))**2
delta_times_Lambda=Fmp/(64*sref*sref*k0)
gain_times_Lambda2_over_alpha2=2*kappa*p**7*(Fmp/(sref*sref*k0))*rx*ry/64**2

eta=np.array([[0.,1.,0.,0.],[1.,0.,0.,0.],[0.,0.,-1.,0.],[0.,0.,0.,-1.]])
N2=np.zeros((4,4));N2[1,2]=1;N2[2,0]=1
N3=np.zeros((4,4));N3[1,3]=1;N3[3,0]=1
assert np.linalg.norm(N2@N3-N3@N2)<1e-15
max_lorentz=0.;max_link_norm=0.;max_creator_norm=0.;min_slack=1.;max_abs_H=0.

def H(x,y):return -lam*energy*(x*x+y*y)+aw*(x*x-y*y)
fmt=lambda x:mp.nstr(x,36)
outpath=HERE/'BRINKMANN_L4_CENTRE.jsonl'
with outpath.open('w') as out:
    for row in rows:
        iu,iv,ix,iy=row['site']
        rho=mp.mpf(row['rho_numerator'])/row['rho_denominator']
        x,y=ix*h,iy*h
        hh=H(x,y);kx=(hh-H(x-h,y))/2;ky=(hh-H(x,y-h))/2
        generator=-float(kx)*N2-float(ky)*N3
        link=np.eye(4)+generator+generator@generator/2
        coframe=np.zeros((4,4));coframe[1,0]=float(nu);coframe[0,1]=float(nu)
        coframe[1,1]=-float(nu*hh/2);coframe[2,2]=coframe[3,3]=float(nu)
        psi0=amplitude*mp.cos(2*mp.pi*iu/4);psi15=amplitude*mp.sin(2*mp.pi*iu/4)
        slack=p**2-psi0**2-psi15**2
        max_lorentz=max(max_lorentz,float(np.max(np.abs(link.T@eta@link-eta))))
        max_link_norm=max(max_link_norm,float(np.linalg.norm(link,2)))
        max_creator_norm=max(max_creator_norm,max(float(np.linalg.norm(coframe[:,j])*mp.sqrt(rho)) for j in range(4)))
        min_slack=min(min_slack,float(slack));max_abs_H=max(max_abs_H,float(abs(hh)))
        obj={'site':row['site'],'is_transverse_interior':ix in (1,2) and iy in (1,2),
             'rho_num':row['rho_numerator'],'rho_den':row['rho_denominator'],
             'H':fmt(hh),'Kx':fmt(kx),'Ky':fmt(ky),
             'native_coframe_columns_approx':coframe.tolist(),
             'U_u_approx':link.tolist(),'U_vxy':'I4',
             'psi0':fmt(psi0),'psi15':fmt(psi15),'material_slack':fmt(slack)}
        out.write(json.dumps(obj,separators=(',',':'))+'\n')
assert max_lorentz<1e-12 and max_link_norm<2 and max_creator_norm<1 and min_slack>0
# One explicitly permitted ORIGINAL Fourier128 subfamily from the owner:
# 64 selected ± k pairs, no Walsh substitution or fabricated uniform PF.
deltas=[]
for j in range(4):
    v=[0]*4;v[j]=1;deltas.append(v)
for j in range(1,4):
    for i in range(j):
        v=[0]*4;v[j]=1;v[i]=-1;deltas.append(v)
cos4=(1,0,-1,0)
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
representatives=[]
for k in product(range(4),repeat=4):
    opposite=tuple((-x)%4 for x in k)
    if k<opposite:representatives.append(k)
assert len(representatives)==120
score=lambda k:sum(cos4[dot(k,d)%4] for d in deltas)
selected=sorted(representatives,key=lambda k:(-score(k),k))[:64]
overlaps=[sum(cos4[dot(k,delta)%4] for k in selected) for delta in deltas]
assert overlaps==[20,10,10,9,8,8,6,9,5,5]
fourier=HERE/'ORIGINAL_FOURIER128_L4.json'
fourier.write_text(json.dumps({'selection':'original 64 ordered real cosine/sine pairs',
                               'L':4,'kappa':selected,'overlap_numerators':overlaps},indent=2)+'\n')
metadata={'status':'REFERENCE_CENTRE_EXPORTED_NOT_FULL_H1',
          'representative':'owner section 7.2 Brinkmann formulas with L=4, sigma=1/100, AW=3/100, nu=3/5',
          'site_count':len(rows),'interior_sites':sum(r['site'][2] in (1,2) and r['site'][3] in (1,2) for r in rows),
          'coordinates':'u,v periodic; transverse x,y fixed collar; exterior stencil values from original H polynomial',
          'n20_PF_counts_reused':True,'rho_max':str(rho_max),'L':4,'h':'1/4','chi_h':'1',
          'reference_s_ref':'6','nu_bound_assumed_for_chart':'1',
          'F_h_rational':str(Fh),'k0_original':fmt(k0),'r_x':fmt(rx),'r_y':fmt(ry),
          'delta_h_times_Lambda_h':fmt(delta_times_Lambda),
          'g_times_Lambda_h_squared_over_alpha_h_squared':fmt(gain_times_Lambda2_over_alpha2),
          'max_lorentz_error_float':max_lorentz,'max_link_operator_norm_float':max_link_norm,
          'max_pf_dressed_coframe_vector_norm_float':max_creator_norm,
          'min_material_slack_float':min_slack,'max_abs_H_float':max_abs_H,
          'interior_sampler_radius_certified':False,'actual_Lambda_h_computed':False,
          'full_factory_alpha_h_computed':False,'compiled_banks_or_marks_emitted':False,
          'geometry_sha256':hashlib.sha256(outpath.read_bytes()).hexdigest(),
          'fourier_sha256':hashlib.sha256(fourier.read_bytes()).hexdigest(),'GR_closed':False}
(HERE/'REFERENCE_METADATA.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(metadata,ensure_ascii=False))
