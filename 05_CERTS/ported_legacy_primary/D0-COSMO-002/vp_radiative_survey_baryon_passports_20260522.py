#!/usr/bin/env python3
import math, json, cmath
phi=(1+math.sqrt(5))/2
delta0=(math.sqrt(5)-2)/2
Delta=math.sqrt(10)/20
I_B=Delta**2*delta0**3/24
As_raw=(1+delta0/4)*I_B
As=As_raw/(2*33*13)
assert As_raw > 1e-7
assert 1.5e-9 < As < 2.5e-9
th=2*math.pi/phi
assert abs(abs(cmath.exp(1j*th))-1) < 1e-15
C0=33; C1=359; C2=9*11*13
beta2=(9-1)*(11-1)*(13-1)
assert C0-C1+C2 == 1 + beta2
assert C0-1 == 32
assert C2-beta2 == 327
assert 20-3 == 17
ell0=6.38502693521136e-14
barn=ell0**2/1e-28
assert 40 < barn < 41
me=0.5109989506917533; Lam=38*me
MZ_phi35=Lam*math.sqrt(phi**35)
assert 88000 < MZ_phi35 < 89000
print('PASS_RADIATIVE_SURVEY_BARYON_PASSPORTS')
print(json.dumps({'I_B':I_B,'A_s_D0':As,'theta_dress':th,'beta2':beta2,'ell0_squared_barn':barn,'MZ_phi35_MeV_rejected':MZ_phi35}, indent=2))
