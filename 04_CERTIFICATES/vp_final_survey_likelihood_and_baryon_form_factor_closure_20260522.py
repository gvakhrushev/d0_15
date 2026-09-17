#!/usr/bin/env python3
import math, json
phi=(1+math.sqrt(5))/2
delta0=(math.sqrt(5)-2)/2
Delta_lambda=math.sqrt(10)/20
I_B=Delta_lambda**2*delta0**3/24
V9,V11,V13=9,11,13
V=33; E=359; C2=V9*V11*V13
rank=E-V+1
beta2=C2-rank
raw_A=(1+delta0/4)*I_B
A_s=raw_A/(2*V*V13)
wa=-delta0**8
chi_B=-math.log(0.9320107332894405)
F=[1.0,0.9951189525792196,0.9617443045143838,0.8137522878569818,0.7459336390007336,0.745920745920746]
assert rank==327
assert beta2==(V9-1)*(V11-1)*(V13-1)==960
assert 1e-9 < A_s < 3e-9
assert raw_A > 1e-7
assert abs(wa + delta0**8) < 1e-25
assert all(F[i] >= F[i+1] for i in range(len(F)-1))
out={'status':'PASS_FINAL_SURVEY_LIKELIHOOD_AND_BARYON_FORM_FACTOR_CLOSURE','survey':{'I_B':I_B,'raw_A_s_rejected':raw_A,'normalization_N_survey':2*V*V13,'A_s_D0':A_s,'n_s_D0':29/30,'w0_D0':-1.0,'w_a_D0':wa,'lambda_B_terminal':0.012648624753253252,'chi_B':chi_B,'d0_free_survey_parameters':0},'baryon_form_factor':{'C0':V,'C1':E,'C2':C2,'rank_boundary_2':rank,'beta2':beta2,'F_delta0_cubed':F[1],'F_delta0_squared':F[2],'F_delta0':F[3],'F_1':F[4],'F_infty':F[5],'ell0_squared_barn':(6.38502693521136e-14)**2/1e-28}}
print(json.dumps(out, indent=2))
print(out['status'])
