#!/usr/bin/env python3
"""Conservative exact rational regularity envelope for a finite L=4 chart.

Only geometry/link/material Julia slack is bounded; this does not compile H.1
or certify its huge Hf/Hq norm, factory readiness, source marks or reader.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

d=Path(__file__).resolve().parent
s=F(1,2**30);nu=F(3,5);rho_sqrt_upper=F(3,2)
# p in (309/500,619/1000), pi^2<10, |lambda_-|<24 (owner).
assert F(24)*F(1,250)+F(3,100)<F(13,100)
# |H|<3/20 on the grid and one-cell backward stencil by the above bounds.
H_bound=F(3,20)
frame= rho_sqrt_upper*(nu*(1+H_bound/2)+4*s)
singular_lower=nu/(1+H_bound/2)-4*s
material_upper=F(1,100)*F(9,8)+2*s
slack_lower=F(309,500)**2-material_upper**2
# ||base link log||<1/25; six unit-norm null-frame Lie generators each |x|<=s.
# exp(x)<=1/(1-x) for 0<=x<1, and ||exterior(U)||<=exp(4||log U||).
link_exp=4*(F(1,25)+6*s)
link_julia_upper=1/(2*(1-link_exp))
assert frame<1 and singular_lower>F(1,2) and slack_lower>F(1,3)
assert link_exp<F(1,6) and link_julia_upper<F(3,5)
# Original n=20 PF has max 768/421<2, so sqrt(rho)<3/2.
meta=json.loads((d/'REFERENCE_METADATA.json').read_text())
assert F(meta['rho_max'])<2 and F(meta['F_h_rational'])<F(1,8)

coords=[]
sites=[(u,v,x,y) for u in range(4) for v in range(4) for x in (1,2) for y in (1,2)]
for site in sites:
    for role in range(4):
        for component in range(4):coords.append({'site':site,'kind':'coframe','role':role,'component':component})
    for role in range(4):
        for a in range(4):
            for b in range(a+1,4):coords.append({'site':site,'kind':'proper_link','role':role,'generator':[a,b]})
    for grade in (0,15):coords.append({'site':site,'kind':'matter','grade':grade})
assert len(coords)==64*42==2688
out=d/'L4_INTERIOR_CHART_COORDINATES.jsonl'
with out.open('w') as f:
    for index,coord in enumerate(coords):
        coord['sam_index']=index;f.write(json.dumps(coord,separators=(',',':'))+'\n')
result={'status':'PASS_EXACT_RATIONAL_GEOMETRIC_SLACK_NOT_FULL_H1',
        'candidate_chart':'L4, periodic u/v, fixed transverse collar, full 16+24+2 at 64 interior sites',
        'm':len(coords),'sampling_halfwidth':'2^-30',
        'chart_map':'coframe and material additive; proper links exp(sum theta_ab eta^-1(E_ab-E_ba)) U0; original PF fixed',
        'cube':'Y_b=chi^-1(chi(Y0)+s(b-p^2)); each coordinate magnitude <=s',
        'coframe_creator_norm_strict_upper':str(frame),
        'coframe_min_singular_strict_lower':str(singular_lower),
        'material_slack_strict_lower':str(slack_lower),
        'link_exterior_half_norm_strict_upper':str(link_julia_upper),
        'uses_original_owner_bounds':['309/500<p<619/1000','pi^2<10','|lambda_-|<24','rho_max<2'],
        'fixed_boundary_or_density_must_match_actual_H1_descriptor':True,
        'site_and_sign_operators_compiled':False,'complete_H1_mark_seal_ledger_emitted':False,
        'all_input_compiler_or_physical_C_proved':False,
        'coords_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'GR_closed':False}
(d/'CHART_ENVELOPE_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
