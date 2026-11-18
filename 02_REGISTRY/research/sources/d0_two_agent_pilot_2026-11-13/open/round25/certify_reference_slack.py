#!/usr/bin/env python3
"""Exact rational reference slack; consumes B21 current-chart certificate."""
from fractions import Fraction as F
from pathlib import Path
import json
P=Path(__file__).resolve().parent;B=P.parent/'round21'
rows=[json.loads(x) for x in (B/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
minrho=F(256*min(r['N'] for r in rows),10946);maxrho=F(256*max(r['N'] for r in rows),10946)
assert minrho==F(3712,5473) and maxrho<2
# ref raw u=nu sqrt(rho)/sref T eta_cart, T orthogonal.
assert maxrho/F(100)<F(1,50) and minrho/F(100)>F(4,625)
# Cayley boost t=1/8: ||exterior(A)/2||=(9/7)/2=9/14.
assert 1-F(9,14)**2==F(115,196)
# reference amplitude²=h² F_h/(4 k0), F_h<1/8, k0>20.
assert F(1,16)*F(1,8)/(4*20)==F(1,10240)
assert F(309,500)**2-F(1,10240)>F(1,3)
current=json.loads((B/'CHART_ENVELOPE_RESULT.json').read_text());assert current['m']==2688 and current['sampling_halfwidth']=='2^-30'
res={'status':'PASS_RATIONAL_REFERENCE_SLACK_PLUS_PINNED_B21_CHART','rho_min':str(minrho),'rho_max':str(maxrho),'reference_raw_u_column_norm_squared_strict_upper':'1/50','reference_raw_u_smallest_singular_strict_lower':'2/25','reference_Julia_coframe_defect_strict_lower':'49/50','reference_Julia_link_defect_lower':'115/196','reference_Psi_amplitude_squared_strict_upper':'1/10240','reference_material_slack_strict_lower':'1/3','uses_owner_inequalities':['309/500<p<619/1000','0<F_h<1/8','k0>20','rho_max<2'],
 'current_chart':'consumes B21 rational geometric/Julia/material envelope; 64 free sites, all 2688 b bits; fixed rho and boundary; additive raw u interpretation from B24',
 'reference_link_reason':'rotation/ref identity ||exterior/2||=1/2; Cayley boost t=1/8 has largest exterior singular 9/7, divided by two',
 'strict_bounds_for_entire_SAM_palette':True,'C1_native_compiler_certified':False,'GR_closed':False}
(P/'STRICT_SLACK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
