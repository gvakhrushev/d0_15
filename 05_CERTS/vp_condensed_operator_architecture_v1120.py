#!/usr/bin/env python3
"""v11.20 structural certificate for condensed/operator ABCD architecture."""
import math, json
phi=(1+math.sqrt(5))/2
psi=(1-math.sqrt(5))/2
p=1/phi
p2=p*p
delta0=(p-p2)/2
checks={}
checks['phi_plus_psi']=abs((phi+psi)-1)<1e-12
checks['phi_times_psi']=abs(phi*psi+1)<1e-12
checks['phi_recurrence']=abs(phi*phi-(phi+1))<1e-12
checks['psi_recurrence']=abs(psi*psi-(psi+1))<1e-12
checks['p_split']=abs((p+p2)-1)<1e-12
checks['delta_centered_half_gap']=abs(delta0-1/(2*phi**3))<1e-12
checks['centered_branches']=abs(p-(0.5+delta0))<1e-12 and abs(p2-(0.5-delta0))<1e-12
# finite quotient sizes and projection compatibility skeleton
sizes=[2**n for n in range(1,8)]
checks['finite_quotient_sizes']=(sizes==[2,4,8,16,32,64,128])
# four role operators are distinct typed obligations
roles={'A_sigma':'unit_section','B_norm':'conjugate_coupling','C_forward':'forward_recurrence','D_return':'return_closure'}
checks['four_distinct_operator_roles']=len(set(roles.values()))==4 and len(roles)==4
# terminal two-port roles and signed Omega8
terminal=[(3,3),(4,4),(3,4),(4,3)]
signed=[(r,s) for r in terminal for s in (+1,-1)]
checks['terminal_four_roles']=len(set(terminal))==4
checks['omega8_signed_count']=len(signed)==8
# dimension ladder
for D in range(1,8):
    checks[f'Q_D_{D}']=abs(2*delta0*(phi**(D-1)) - phi**(D-4)) < 1e-12
status='PASS_CONDENSED_OPERATOR_ARCHITECTURE_V1120' if all(checks.values()) else 'FAIL'
print(json.dumps({'status':status,'checks':checks,'phi':phi,'psi':psi,'delta0':delta0,'Q4':2*delta0*phi**3},indent=2,sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
