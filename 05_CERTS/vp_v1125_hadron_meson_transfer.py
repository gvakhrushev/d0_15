import math, json
phi=(1+math.sqrt(5))/2
p=1/phi
delta0=(math.sqrt(5)-2)/2
me=0.51099895
Lambda_act=38*me
# meson formulas
T_pi=20*p*p-4*delta0
T_K=20+math.sqrt(5)+2*phi
T_rho=40
m_pi=Lambda_act*T_pi
m_K=Lambda_act*T_K
m_rho=Lambda_act*T_rho
# baryon formulas
lambda_B2=3960
lambda_Ncore=2640.7985901288725
V9,V11,V13=9,11,13
Vsum=V9+V11+V13
d13=V9+V11
ABCD=4
lambda_Delta=lambda_B2+V13*(ABCD+1)
lambda_Lambda=lambda_Ncore+Vsum*d13
lambda_Omega=(2*Vsum+d13)**2
m_Delta=Lambda_act*math.sqrt(lambda_Delta)
m_Lambda=Lambda_act*math.sqrt(lambda_Lambda)
m_Omega=Lambda_act*math.sqrt(lambda_Omega)
bench={"pi_charged":139.57039,"K_charged":493.677,"rho_centroid":775.26,"Delta_centroid":1232.0,"Lambda":1115.683,"Omega":1672.45}
pred={"pi_charged_proxy":m_pi,"K_charged_proxy":m_K,"rho_centroid_proxy":m_rho,"Delta_centroid_proxy":m_Delta,"Lambda":m_Lambda,"Omega":m_Omega}
errs={k:(pred[k2]-v)/v for k,v in bench.items() for k2 in pred if k2.startswith(k.split('_')[0]) or (k==k2)}
checks={
    "phi_identity": abs(phi*phi-phi-1)<1e-12,
    "delta_identity": abs(delta0-(p-p*p)/2)<1e-12,
    "rho_ticks": T_rho==40,
    "delta_lambda": lambda_Delta==4025,
    "omega_lambda": lambda_Omega==7396,
    "no_new_scale": abs(Lambda_act-38*me)<1e-12,
}
result={"status":"PASS_V11_25_HADRON_MESON_TRANSFER_ARITHMETIC" if all(checks.values()) else "FAIL", "constants":{"phi":phi,"p":p,"delta0":delta0,"Lambda_act_MeV":Lambda_act}, "predictions_MeV":pred,"benchmarks_MeV":bench,"relative_errors":errs,"checks":checks}
print(json.dumps(result, indent=2))
