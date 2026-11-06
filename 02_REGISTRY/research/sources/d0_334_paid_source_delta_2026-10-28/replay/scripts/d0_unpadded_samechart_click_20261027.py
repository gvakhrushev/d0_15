#!/usr/bin/env python3
"""Downstream interval application to the original certified unpadded 42-root.

Consumes the 1e-24 existence cube; does not certify another root or assert
physical selection of a Book cut, writer, cost/info or the direct-click model.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
import hashlib, json, sys
from mpmath import iv

root=Path.cwd();owner=root/'02_REGISTRY/research/sources/d0_original_unpadded42_2026-10-22'
base=root/'02_REGISTRY/research/sources/d0_full42_interval_banach_2026-10-22'
paths={'certified_unpadded':owner/'certified_unpadded.py','center_new':owner/'center_new.json','root_receipt':owner/'RESULT.json','original_model':base/'certified_model.py','original_inputs':base/'inputs.py','original_root_checker':owner/'check_unpadded42.py'}
pins={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
expected={'certified_unpadded':'30c670082ce1ee9e56d32a2d537b59bd35ea3ffed4bf27fe8aa41ec7de513246','center_new':'d2c824b170b9aba1fd4d7195c231ce034e0d54f7ccd3bb2d9a7df7c40e283f39','root_receipt':'f5a7af22e4524d06c37bbc01c6f55c6250c0d1b643180f535f32350e5bd4a175','original_model':'d617f2de4ffff8566705045091495e52d72d7df715113338c2234355a0e19ca6','original_inputs':'12c4077fa8125b10609590daa1bc6815ebbf3b22f48781b3b3148d41b066f641','original_root_checker':'6a033b87da3a3fb6f54edac9b7e3127482d2dc1ccdeb09ebf519b2ef457dba06'}
assert pins==expected, 'frozen original inputs changed'
sys.path.insert(0,str(owner))
from certified_unpadded import NativeUnpaddedCQ,CENTER,COLLAR
getcontext().prec=150
iv.dps=115
m=NativeUnpaddedCQ(iv)
def ivbound(x,a,b):
    assert x.a>iv.mpf(a) and x.b<iv.mpf(b),(str(x),a,b)
def cube(rad):
    return [iv.mpf([str(Decimal(s)-rad),str(Decimal(s)+rad)]) for s in CENTER['z42']]
ball=Decimal('1e-24');realbox=cube(ball)
assert CENTER['h']==COLLAR['h']
# IMPORTANT: original finite N1 fixture and paid-writer refinement use
# distinct actual tau. Establish the exact exponential rounding without
# replacing the click/source at one tau by that at the other.
h0=iv.mpf(CENTER['h']);p=m.p;tau_h=p**8
assert tau_h.b<(h0*h0).a and (h0*h0).b<(p**7).a
ivbound(tau_h,'0.02128','0.02130')
assert tau_h.b<m.tau.a and m.tau==iv.mpf('0.05')
assert json.loads(paths['root_receipt'].read_text())['certificate']['real_exact_root_ball_radius_infinity']=='1e-24'
# Holomorphic control on original polydisc centered at the fixed rational center:
# the evaluated original click formula has modulus <1 there. The root cube
# admits a 5e-5 disc about each point inside that same rectangle.
R=Decimal('1e-4');large=[]
for s in CENTER['z42']:
    x=Decimal(s);large.append(iv.mpc([str(x-R),str(x+R)],[str(-R),str(R)]))
m.price(large);assert all(abs(r).b<iv.mpf(1) for r in m.last_clicks)
# Strict actual click intervals over the *whole* original certified root cube.
m.price(realbox);r=[x.real for x in m.last_clicks]
ivbound(r[0],'1.85127304676926594408995e-6','1.85127304676926594408999e-6')
ivbound(r[1],'1.85123468250638593779568e-6','1.85123468250638593779579e-6')
gap=r[0]-r[1];ivbound(gap,'3.836426287999e-11','3.836426288002e-11')
# Complex step at all real inputs in the cube. A true Taylor remainder is
# bounded by M*t^2/[R0^3*(1-t/R0)] < 1e-46 (M=1,R0=5e-5,t=1e-30).
# Original model's rigorous_exp encloses its 1e-120 tail in each evaluation;
# all other interval operations are outward, including this uncertainty.
rt=Fraction(1,10**30);rr=Fraction(1,20000)
assert rt*rt/(rr**3*(1-rt/rr)) < Fraction(1,10**46)
t=iv.mpf('1e-30');v=realbox.copy();v[40]=iv.mpc(realbox[40],t);m.price(v)
err=iv.mpf(['-1e-46','1e-46']);d=[x.imag/t+err for x in m.last_clicks]
ivbound(d[0],'-3.522176119e-8','-3.522176117e-8')
ivbound(d[1],'3.522170378e-8','3.522170381e-8')
ds=d[0]+d[1];ivbound(ds,'-5.741e-14','-5.737e-14')
# Exact 0/10 price is norm Σ (hφ(r_i)-r_i) plus field-independent constants.
# hφ'(r_i)-1 >0, strictly decreasing with click; stationarity implies the
# weighted derivative is zero. Verify the actual interval weights and signs.
hp=[iv.log((1-x)/x)/m.lp-1 for x in r]
assert hp[0].a>iv.mpf(1) and hp[1].a>iv.mpf(1) and hp[0].b<hp[1].a
weighted=hp[0]*d[0]+hp[1]*d[1]
assert weighted.a<0 and weighted.b>0
# a0 is the original positive r_x at the common-null anchor. This quantity
# normalizes the comparison ONLY; no actual physical Book price is selected.
p=m.p; zz=m.Z;b0=4*p*p*(1-p*p)
a0=zz*(1-zz*b0)*4*p*p*(1-2*p*p)*(1-b0)
assert a0.a>0
normalized=ds/(a0*m.tau)
ivbound(normalized,'-0.00005991','-0.00005985')
# The unpadded robustness theorem uses the much larger radius 1e-20.
# Re-enclose the *same* derivative and normalization on that whole cube,
# independently of the root Euler equation, to test source compatibility.
robustbox=cube(Decimal('1e-20'))
m.price(robustbox);robustr=[x.real for x in m.last_clicks]
assert robustr[0].a>robustr[1].b
v=robustbox.copy();v[40]=iv.mpc(robustbox[40],t);m.price(v)
robustd=[x.imag/t+err for x in m.last_clicks]
robustsum=robustd[0]+robustd[1]
ivbound(robustsum,'-5.739033603421e-14','-5.739033603369e-14')
robustnorm=robustsum/(a0*m.tau)
ivbound(robustnorm,'-0.00005991','-0.00005985')
result={'status':'PASS_ORIGINAL_UNPADDED42_SAME_CHART_DIRECT_CLICK','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':pins,'h':CENTER['h'],'certified_root_cube_radius':'1e-24','large_complex_box_radius':'1e-4','click_box_abs_bound':'< 1','cauchy_radius_about_every_real_root_candidate':'5e-5','complex_step':'1e-30','cauchy_derivative_error_each':'< 1e-46','tau_original_N1':'0.05','tau_refinement_rule':'p^ceil(2 log_phi(1/h)); p^8 < h^2 < p^7, so tau_h=p^8','tau_refinement_actual_interval':str(tau_h),'tau_inputs_are_distinct':True,'coordinate':'z[40], first real CAR scalar amplitude at interior node; one-based 41',
'click_A_minus_click_B':'(3.836426287999e-11, 3.836426288002e-11)',
'D_click_A':'(-3.522176119e-8, -3.522176117e-8)',
'D_click_B':'(3.522170378e-8, 3.522170381e-8)',
'D_sum':'(-5.741e-14, -5.737e-14)',
'D_sum_over_a0_tau':'(-0.00005991, -0.00005985)',
'robustness_cube_radius':'1e-20',
'robustness_cube_D_sum':'(-5.739033603421e-14, -5.739033603369e-14)',
'robustness_cube_D_sum_over_a0_tau':'(-0.00005991, -0.00005985)',
'actual_outward_intervals_115dps':{'root_click_gap':str(gap),'root_D_sum':str(ds),'root_normalized':str(normalized),'robust_D_sum':str(robustsum),'robust_normalized':str(robustnorm)},
'CQ_derivative_weights':'h_phi_prime(r_i)-1 from literal 0/10 price; positive unequal; weighted interval contains zero',
'scope':'all inequalities hold throughout original root cube; direct-click normalization is a mathematical comparison, not full Book source or physical selection; no new root, heat, full128 CAR or Lean replay; GR_closed=false'}
print(json.dumps(result,indent=2,sort_keys=True))
